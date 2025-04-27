import os
from datetime import datetime

import boto3
import polars as pl
import sagemaker
from sagemaker.feature_store.feature_definition import FeatureDefinition, FeatureTypeEnum
from sagemaker.feature_store.feature_group import FeatureGroup
from sagemaker.feature_store.inputs import FeatureValue

BUCKET_NAME = os.getenv("MY_SAMPLE_BUCKET")
ROLE_ARN = os.getenv("MY_SAGEMAKER_ROLE")


def main():
    aws_profile = os.getenv("MY_AWS_PROFILE")
    session = boto3.Session(profile_name=aws_profile)
    sagemaker_session = sagemaker.Session(boto_session=session)

    # 特徴量としてnews_embedding_dfを読み込む
    news_embedding_df = pl.read_parquet("/tmp/news_embeddings/")
    print(f"{news_embedding_df=}")

    # レコードの生成時刻を表す列を追加
    """
    - Sagemaker Feature Storeのオフラインストアでは、特徴量データをparquet形式でS3に保存する。
    - データは「特徴量グループ」ごとにS3内の専用パス(prefix)に分けて格納される。
    - イベントタイム(年/月/日/時)ごとにパーティション分割される。
    """
    output_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    news_embedding_df = news_embedding_df.with_columns(pl.lit(output_date).alias("timestamp"))
    print(f"{news_embedding_df=}")

    # feature storeに保存するための設定値
    record_identifier_name = "content_id"  # レコードの識別子
    event_time_feature_name = "timestamp"  # レコードの生成時刻を表す列名
    feature_group_name = "temp_news_embeddings2"  # Feature Groupの名前

    # create_or_update_feature_group(
    #     feature_group_name=feature_group_name,
    #     sagemaker_session=sagemaker_session,
    #     # news_embedding_df=news_embedding_df,
    #     record_identifier_name=record_identifier_name,
    #     event_time_feature_name=event_time_feature_name,
    # )

    # insert_feature(
    #     feature_group_name=feature_group_name,
    #     sagemaker_session=sagemaker_session,
    #     news_embedding_df=news_embedding_df,
    # )

    fetch_feature(
        feature_group_name=feature_group_name,
        sagemaker_session=sagemaker_session,
    )


def create_or_update_feature_group(
    feature_group_name: str,
    sagemaker_session: sagemaker.Session,
    # news_embedding_df: pl.DataFrame,
    record_identifier_name: str,
    event_time_feature_name: str,
) -> None:
    """Feature Groupを作成 or すでに存在するなら一度消して再作成する関数"""
    # 特徴量を保存するためのFeature Groupを設定
    prefix = f"{feature_group_name}"

    # load_feature_definitionsを使用してFeature Definitionsのスキーマを自動で識別させる
    # feature_group_auto = FeatureGroup(name=feature_group_name, sagemaker_session=sagemaker_session)
    # print(f"{feature_group_auto=}")
    # try:
    #     # dataframeからFeature Definitionsを自動で生成
    #     feature_group_auto.load_feature_definitions(data_frame=news_embedding_df.to_pandas())
    # except ValueError as e:
    #     print(e)
    # print(f"{feature_group_auto.feature_definitions=}")
    # del feature_group_auto

    # 自分で定義したFeature Definitionsのスキーマを使用する
    my_feature_definitions = [
        FeatureDefinition(feature_name="content_id", feature_type=FeatureTypeEnum.STRING),
        FeatureDefinition(feature_name="embedding", feature_type=FeatureTypeEnum.STRING),
        FeatureDefinition(feature_name="timestamp", feature_type=FeatureTypeEnum.STRING),
    ]
    feature_group_original = FeatureGroup(
        name=feature_group_name,
        sagemaker_session=sagemaker_session,
        feature_definitions=my_feature_definitions,
    )
    print(f"{feature_group_original.feature_definitions=}")

    # Feature Groupを作成
    feature_group_original.create(
        s3_uri=f"s3://{BUCKET_NAME}/{prefix}",  # offline feature store でデータを保存する S3 URI
        record_identifier_name=record_identifier_name,  # レコード識別子のカラム名
        event_time_feature_name=event_time_feature_name,  # レコードの生成時刻を表すカラム名
        role_arn=ROLE_ARN,  # IAM Role ARN
        enable_online_store=False,  # オンラインストアを作成するかどうか
        description="Feature group for news embeddings",  # Feature Groupの説明
        tags=[
            {"Key": "service", "Value": "embedding-engine"},
            {"Key": "application", "Value": "sagemaker feature store"},
            {"Key": "env", "Value": "dev"},
            {"Key": "env_cost", "Value": "dev"},
        ],
        # Sagemaker Feature Storeは、デフォルトでAWS Glue Data Catalogを使って
        # 特徴量グループのメタデータを管理する。
        # これにより、Athenaや他のSQLクエリエンジンから、S3上のオフラインストアデータをテーブルとしてクエリできる!
        # AWS Glueテーブル形式か、Icebergテーブル形式か、の2択みたい。デフォルトは前者。
        disable_glue_table_creation=False,
    )


def insert_feature(
    feature_group_name: str,
    sagemaker_session: sagemaker.Session,
    news_embedding_df: pl.DataFrame,
) -> None:
    """Feature Groupにデータを登録
    2種類の登録方法がある。
    - put_record: 1レコードを登録。
    - ingest: DataFrameのレコードをまとめて登録。
    """
    # put_recordを使用して1レコードを登録
    record = [
        FeatureValue("content_id", "N:123"),
        FeatureValue("embedding", "[0.1,0.2,0.3,0.4,0.5]"),
        FeatureValue("timestamp", f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}"),
    ]
    FeatureGroup(
        name=feature_group_name,
        sagemaker_session=sagemaker_session,
    ).put_record(record)

    # ingestを使用してDataFrameのレコードをまとめて登録(ingestはsagemaker Python SDKにしかないみたい)
    FeatureGroup(
        name=feature_group_name,
        sagemaker_session=sagemaker_session,
    ).ingest(data_frame=news_embedding_df.to_pandas()[0:1000], max_workers=1, wait=True)
    print("Feature Groupにデータを登録しました。")


def fetch_feature(
    feature_group_name: str,
    sagemaker_session: sagemaker.Session,
) -> None:
    """Feature Groupからデータを取得
    - online storeから取得する場合:
        - get_recordメソッド。entityカラムの値と取得したい特徴量名を指定する。
    - offline storeから取得する場合:
        - 方法1: Amazon Athenaを使用したSQLクエリ
            - select *だと、返り値として特徴量 & entity_id & event_timeの他に、write_time & api_invocation_time, is_deletedカラムがついてくるみたい。
            - これらは自動付与されるカラム。
                - write_time: データがFeature Storeに書き込まれた時間
                - api_invocation_time: データを書き込むAPIリクエストを受けた時間
                - is_deleted: データが削除済かどうか。
                    - しかしオフラインストアの場合はS3にappend-only保存だから、deleteリクエストがきても物理的にはレコードが消えない。
                    - その代わりにis_deletedがTrueになり、レコードが無効化される。
            - 基本的に学習 & 推論時は、方法2の方が使うのかな。特徴量を元に新しい特徴量を作る、みたいな時は、方法1も使ったりする??
        - 方法2: FeatureStore.create_dataset()メソッド。多分point-in-timeな特徴量取得はこれを使うのが抽象化されててシンプルそう。
        - 方法3: S3上のparquetファイルを直接読み込む。
    """
    # 特徴量を取得
    feature_group = FeatureGroup(
        name=feature_group_name,
        sagemaker_session=sagemaker_session,
    )
    print(f"{feature_group=}")
    # 今回のFeature Groupはオンラインストアを無効にしてるのでコメントアウト。
    # response = feature_group.get_record(record_identifier_value_as_string="N:123", feature_names=["embedding"])

    # offline storeからAthenaクエリを利用して特徴量を取得してみる
    feature_store_query = feature_group.athena_query()  # Glue Data Catalogに登録してないとエラーになる
    feature_store_table = feature_store_query.table_name
    query_string = f"""
SELECT *
FROM "{feature_store_table}" LIMIT 5
"""
    feature_store_query.run(query_string, output_location=f"s3://{BUCKET_NAME}/tmp/query_results/")
    feature_store_query.wait()
    fetched_feature_pd_df = feature_store_query.as_dataframe()
    feature_df = pl.from_pandas(fetched_feature_pd_df)
    print(f"{feature_df=}")


def fetch_feature_with_point_in_time_join(
    feature_group_name: str,
    sagemaker_session: sagemaker.Session,
) -> None:
    """(主に学習時に使われる?) point-in-time joinを使用してデータセットを取得する。
    - point-in-time joinの振る舞い = baseの各entityのevent_timeよりも古い、かつその中で最も新しい特徴量をjoinしてすること。
    - refs: https://aws.amazon.com/jp/blogs/machine-learning/build-machine-learning-ready-datasets-from-the-amazon-sagemaker-offline-feature-store-using-the-amazon-sagemaker-python-sdk/

    - create_dataset()メソッドの更に高度な設定もあるみたい(個人的には、めっちゃ複雑な特徴量使うなら活用しうるのかな、ってくらい)
        - 最新N件の特徴量取得: dataset_builder.with_number_of_recent_records_by_record_identifier()メソッド。
        - 特徴量取得期間のフィルタリング: dataset_builder.with_event_time_range()メソッド。
    - バッチ学習の場合は上記のようになるとして、バッチ推論の場合はどんな感じの実装になるんだろ??
        - たぶん、推論処理を行う現在時刻が全entityのevent_timeになって、各entityに紐づく最新の特徴量がjoinされるイメージっぽい。
        - point_in_time_accurate_join()を指定しない場合は、デフォルトで現在時刻から最新の特徴量がjoinされそう。
    """
    from sagemaker.feature_store.feature_store import FeatureStore

    feature_store = FeatureStore(sagemaker_session=sagemaker_session)

    # event_timeとレコード識別子を含むベースデータを用意(これに特徴量がjoinされる)
    entity_df = pl.DataFrame(
        {
            "content_id": ["N:123", "N:456", "N:789"],
            "event_time": ["2023-01-10T09:30:00Z", "2023-01-11T14:15:00Z", "2023-01-12T16:40:00Z"],
            "reward": [1, 2, 3],
        }
    )

    # DatasetBuilderの初期化
    dataset_builder = feature_store.create_dataset(
        base=entity_df.to_pandas(),
        event_time_identifier_feature_name="event_time",
        record_identifier_feature_name="content_id",
        output_path=f"s3://{BUCKET_NAME}/point_in_time_join/",
    ).point_in_time_accurate_join()

    # baseにpoint-in-time joinしたい特徴量を指定
    dataset_builder = dataset_builder.with_feature_group(
        feature_group=FeatureGroup(name=feature_group_name, sagemaker_session=sagemaker_session),
        target_feature_name_in_base="content_id",
    )

    # joinされたデータセットの生成
    dataset_pandas_df, executed_query = dataset_builder.to_dataframe()
    dataset_df = pl.from_pandas(dataset_pandas_df)
    print(f"{dataset_df=}")


if __name__ == "__main__":
    main()
