import json
from pathlib import Path
import numpy as np

import polars as pl
import patito as pt


class ContentVector(pt.Model):
    content_id: str = pt.Field(unique=True)
    vector: str


def load_vectors(parquet_dir: Path) -> pl.DataFrame:
    vector_df_list = []
    for parquet_file in parquet_dir.glob("*.parquet"):
        partial_vector_df = pl.read_parquet(parquet_file)
        vector_df_list.append(partial_vector_df)

    vector_df: pl.DataFrame = pl.concat(vector_df_list)
    ContentVector.validate(vector_df)

    # vector列を文字列からnp.ndarrayに変換
    vector_df = vector_df.with_columns(
        pl.col("vector").apply(_vector_from_str).alias("vector")
    )
    return vector_df


def _vector_from_str(vec_str: str) -> np.ndarray:
    if vec_str == "[]":
        return np.nan
    return np.array(json.loads(vec_str))


class News(pt.Model):
    content_id: str = pt.Field(unique=True)
    title: str
    summary: str


def load_news(news_dir: Path) -> pl.DataFrame:
    news_df_list = [
        pl.read_parquet(parquet_file) for parquet_file in news_dir.glob("*.parquet")
    ]
    news_df = pl.concat(news_df_list)
    News.validate(news_df)
    return news_df


if __name__ == "__main__":
    # newsのサンプルデータを/tmp/input/news/000.parquetに保存
    news_df = pl.DataFrame(
        [
            {
                "content_id": "xxxx",
                "title": "hogehogeが新商品を発売",
                "summary": "hogehoge商社が新商品を発売しました",
            },
            {
                "content_id": "yyyy",
                "title": "fugafugaが上場",
                "summary": "fugafugaが上場しました",
            },
            {
                "content_id": "zzzz",
                "title": "piyopiyoがTOBを実施",
                "summary": "piyopiyoがTOBを実施しました",
            },
        ]
    )
    news_df.write_parquet("/tmp/input/news/000.parquet")
