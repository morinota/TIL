import json
from pathlib import Path
import numpy as np

import polars as pl
import patito as pt


class ContentVector(pt.Model):
    content_id: str = pt.Field(unique=True)
    # 現時点でvectorは文字列で保存されているため、入力時はstr型で受け取る
    vector: str


def load_content_vectors_as_df(sql_query: str, unload_s3uri: str) -> pl.DataFrame:
    """Redshiftからコンテンツベクトルを読み込んでpl.DataFrameとして返す"""
    success_unload = _unload_as_parquet_from_redshift(
        sql_query=sql_query,
        s3uri=unload_s3uri,
        role_arn="hoge",
        cluster_id="hoge",
        database_name="hoge",
        user_name="hoge",
    )
    if not success_unload:
        raise Exception("Failed to unload content vectors from redshift")

    return _load_content_vectors_from_parquet(Path(unload_s3uri))


def _load_content_vectors_from_parquet(parquet_dir: Path) -> pl.DataFrame:
    vector_df_list = [
        pl.read_parquet(parquet_file) for parquet_file in parquet_dir.glob("*.parquet")
    ]

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


def _unload_as_parquet_from_redshift(
    sql_query: str,
    s3uri: str,
    role_arn: str,
    cluster_id: str,
    database_name: str,
    user_name: str,
) -> bool:
    import boto3
    import time
    from loguru import logger

    unload_query = f"""
        begin;

        unload ('{sql_query}') 
        to '{s3uri}' 
        parquet
        parallel off
        iam_role '{role_arn}'
        allowoverwrite;

        commit;
        """
    logger.debug(f"{unload_query=}")

    session = boto3.Session()
    client = session.client("redshift-data")

    # Launch the sql query with redshift data api
    execution_id = client.execute_statement(
        ClusterIdentifier=cluster_id,
        Database=database_name,
        DbUser=user_name,
        Sql=unload_query,
    )["Id"]

    # wait for completion
    status = client.describe_statement(Id=execution_id)["Status"]
    logger.debug(f"{status=}")

    # fetch data
    while status not in ["FINISHED", "FAILED"]:
        time.sleep(5)
        status = client.describe_statement(Id=execution_id)["Status"]
        logger.debug(f"{status=}")

    if status == "FAILED":
        logger.error(client.describe_statement(Id=execution_id)["Error"])
        return False

    return True
