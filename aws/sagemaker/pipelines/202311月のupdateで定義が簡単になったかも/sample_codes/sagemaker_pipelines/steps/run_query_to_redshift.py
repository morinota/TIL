import argparse
import boto3
from loguru import logger
import time

# OUTPUT_DATA_DIR = "/opt/ml/processing/output"
OUTPUT_DATA_DIR = "/tmp/output"
CLUSTER_ID = "my-redshift-cluster-id"
DATABASE_NAME = "my-database-name"
USER_NAME = "my-user-name"


def main(params: argparse.Namespace) -> None:
    """Redshiftに対してクエリを実行する"""
    session = boto3.Session()
    redshift_client = session.client("redshift-data")

    # sql ファイルを読み込む
    with open(params.sql_query_path, "r") as f:
        sql_query = f.read()

    # Launch the sql query with redshift data api
    execution_id = redshift_client.execute_statement(
        ClusterIdentifier=CLUSTER_ID,
        Database=DATABASE_NAME,
        DbUser=USER_NAME,
        Sql=sql_query,
    )["Id"]

    # wait for completion
    status = redshift_client.describe_statement(Id=execution_id)["Status"]
    logger.debug(f"{status=}")

    # fetch data
    while status not in ["FINISHED", "FAILED"]:
        time.sleep(5)
        status = redshift_client.describe_statement(Id=execution_id)["Status"]
        logger.debug(f"{status=}")

    if status == "FAILED":
        logger.error(redshift_client.describe_statement(Id=execution_id)["Error"])
        raise Exception("Failed to execute query")

    logger.info("Query executed successfully")


if __name__ == "__main__":
    # コマンドライン引数をパースする
    parser = argparse.ArgumentParser()

    # モデルのハイパーパラメータ引数
    parser.add_argument(
        "--sql_query_path",
        type=str,
        default="/query/sample_query.sql",
        help="Redshiftに対して実行したいクエリのファイルパス",
    )
    params, _ = parser.parse_known_args()
    main(params)
