import json
from pathlib import Path
from typing import TypeAlias
import numpy as np
import polars as pl
import patito as pt
from type_aliases import Vector


class ContentVector(pt.Model):
    content_id: str = pt.Field(unique=True)
    vector: list[float]


def load_vectors_parquet(parquet_dir: Path) -> dict[str, Vector]:

    vector_df_list = [
        pl.read_parquet(parquet_file) for parquet_file in parquet_dir.glob("*.parquet")
    ]
    vector_df: pl.DataFrame = pl.concat(vector_df_list)

    # vector列を文字列からnp.ndarrayに変換
    vector_df = vector_df.with_columns(
        pl.col("vector").map_elements(
            _vector_from_str, return_dtype=pl.List(pl.Float64)
        )
    )
    ContentVector.validate(vector_df)

    vector_by_id = dict(zip(vector_df["content_id"], vector_df["vector"]))

    return {content_id: np.array(vector) for content_id, vector in vector_by_id.items()}


def _vector_from_str(vec_str: str) -> list[float]:
    if vec_str == "[]":
        return []
    return json.loads(vec_str)
