import multiprocessing
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import boto3
import polars as pl
import pydantic
from loguru import logger

TABLE_NAME = "TempBatchRecommendations"
dynamoDB = boto3.resource("dynamodb")

# 並列処理のスレッド数（環境に応じて調整）
MAX_WORKERS = 8


class BatchRecommendation(pydantic.BaseModel):
    user_id: str
    model_unique_name: str
    recommendation: str


def transform_df_to_batch_recommendation(ranking_df: pl.DataFrame) -> pl.DataFrame:
    # ユーザーごとに ranked_content_id をリスト化
    transformed_df = ranking_df.group_by("user_id").agg(
        [
            pl.lit("model1").alias("model_unique_name"),  # model1 を固定
            pl.col("ranked_content_id").alias("recommendation"),
        ]
    )
    # user_idカラムを文字列に
    transformed_df = transformed_df.with_columns(transformed_df["user_id"].cast(pl.String))
    return transformed_df


def batch_write_items(items: list[BatchRecommendation]) -> None:
    """DynamoDBへのバッチ書き込みを実行する"""
    item_dicts = [item.model_dump() for item in items]
    logger.debug(f"{len(item_dicts)=}")

    try:
        table = dynamoDB.Table(TABLE_NAME)
        with table.batch_writer() as batch:
            for item_dict in item_dicts:
                batch.put_item(Item=item_dict)
    except Exception as error:
        logger.error(f"Error: {error}")


def batch_write_items_with_multi_threads(items: list[BatchRecommendation]) -> None:
    """DynamoDBへのバッチ書き込みをマルチスレッドで実行する"""
    if not items:
        return

    # 100件以下の場合はシングルスレッドで処理
    if len(items) <= 100:
        batch_write_items(items)
        return

    # 100件以上の場合はマルチスレッドで処理
    chunks = _chunkify(items, num_chunks=MAX_WORKERS)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(batch_write_items, chunks)


def batch_write_items_with_concurrent(items: list[BatchRecommendation]) -> None:
    """DynamoDBへのバッチ書き込みを並列処理(Concurrent)で実行する"""
    if not items:
        return

    # 100件以下の場合はシングルスレッドで処理
    if len(items) <= 100:
        batch_write_items(items)
        return

    # 100件以上の場合はマルチスレッドで処理
    num_cores = multiprocessing.cpu_count()
    with multiprocessing.Pool(num_cores) as pool:
        chunks = _chunkify(items, num_chunks=num_cores)
        pool.map(batch_write_items, chunks)


def _chunkify(items: list[BatchRecommendation], num_chunks: int) -> list[list[BatchRecommendation]]:
    """リストを num_chunks の個数に均等に分割する"""
    avg = len(items) // num_chunks
    chunks = [items[i * avg : (i + 1) * avg] for i in range(num_chunks)]
    remainder = len(items) % num_chunks
    for i in range(remainder):
        chunks[i].append(items[num_chunks * avg + i])
    return chunks


def main():
    # polarsのDataFrameを準備（例）
    ranking_path = "/Users/masato.morita/Downloads/personalized_movie_rankings.parquet"
    ranking_df = pl.read_parquet(ranking_path)
    df = transform_df_to_batch_recommendation(ranking_df)
    print(df)

    items = [
        BatchRecommendation(
            user_id=row["user_id"],
            model_unique_name=row["model_unique_name"],
            # list[str]を"[str, str, str]"の形式に変換
            recommendation=str(row["recommendation"]),
        )
        for row in df.to_dicts()
    ]
    print(f"{len(items)}")
    print(items[0:2])
    # itemsのデータサイズを取得 (60万itemで5.0MBくらい)
    data_size = sys.getsizeof(items)
    print(f"data_size: {data_size} bytes ({data_size / 1000**2} MB)")

    items = items[:1000]

    # DynamoDBへの書き込み時間を計測
    start_time = time.perf_counter()
    batch_write_items_with_multi_threads(items)
    end_time = time.perf_counter()

    logger.info(f"DynamoDB書き込み時間: {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    main()
    """
    - データサイズ: 5MB
    - アイテム数: 60万件

    上記のデータをBatchWriteItemでDynamoDBに書き込む場合のコストを考える。

    - 1アイテムあたりのデータサイズは...5MB / 60万件 = 0.0083 bytes/item
    - on-demand capacity modeでStandardテーブルクラスの場合、100万WRUあたり0.715USD
    - 標準書き込みリクエストの場合、1WRUで最大1KBまでのitemを書き込むことができる。
        - BatchWriteItemだろうと、PutItemだろうと、利用料金の仕組みは同じで1 itemごとに課金されるっぽい。


    """
