from typing import TypedDict

import boto3
import polars as pl
from loguru import logger

BATCH_SIZE = 25
TABLE_NAME = "TempBatchRecommendations"
dynamoDB = boto3.resource("dynamodb")


class BatchRecommendation(TypedDict):
    user_id: str
    model_unique_name: str
    recommendation: str


def batch_write_items(items: list[BatchRecommendation]) -> None:
    try:
        table = dynamoDB.Table(TABLE_NAME)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
    except Exception as error:
        logger.error(f"Error: {error}")


def main():
    # polarsのDataFrameを準備（例）
    df = pl.DataFrame(
        {
            "user_id": ["user1", "user2", "user1"],
            "model_unique_name": ["model1", "model1", "model2"],
            "recommendation": ["[item1, item2]", "[item3, item4]", "[item5, item6]"],
        }
    )
    print(df)
    items = df.to_dicts()
    print(items)
    batch_write_items(items)


if __name__ == "__main__":
    main()
