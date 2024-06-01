from datetime import datetime
import polars as pl
from data.data_models import (
    AppLaunchLogSchema,
    UserVariantMappingSchema,
    UserMetadataSchema,
)
import numpy as np


def generate_mock_app_launch_log_table() -> pl.DataFrame:
    # アプリ起動ログテーブル
    return pl.DataFrame(
        [
            {"user_id": 1, "timestamp": datetime(2021, 1, 1, 0, 0, 0), "os": "iOS"},
            {"user_id": 2, "timestamp": datetime(2021, 1, 1, 0, 0, 0), "os": "Android"},
            {"user_id": 3, "timestamp": datetime(2021, 1, 1, 0, 0, 0), "os": "iOS"},
            {"user_id": 4, "timestamp": datetime(2021, 1, 1, 0, 0, 0), "os": "Android"},
            {"user_id": 1, "timestamp": datetime(2021, 1, 2, 0, 0, 0), "os": "iOS"},
            {"user_id": 2, "timestamp": datetime(2021, 1, 2, 0, 0, 0), "os": "Android"},
            {"user_id": 3, "timestamp": datetime(2021, 1, 2, 0, 0, 0), "os": "iOS"},
            {"user_id": 4, "timestamp": datetime(2021, 1, 2, 0, 0, 0), "os": "Android"},
            {"user_id": 1, "timestamp": datetime(2021, 1, 3, 0, 0, 0), "os": "iOS"},
            {"user_id": 2, "timestamp": datetime(2021, 1, 3, 0, 0, 0), "os": "Android"},
            {"user_id": 3, "timestamp": datetime(2021, 1, 3, 0, 0, 0), "os": "iOS"},
            # user_id 4は2021-01-03にアプリを起動してない。
            {"user_id": 1, "timestamp": datetime(2021, 1, 4, 0, 0, 0), "os": "iOS"},
            {"user_id": 2, "timestamp": datetime(2021, 1, 4, 0, 0, 0), "os": "Android"},
            {"user_id": 3, "timestamp": datetime(2021, 1, 4, 0, 0, 0), "os": "iOS"},
            {"user_id": 4, "timestamp": datetime(2021, 1, 4, 0, 0, 0), "os": "Android"},
        ]
    )


def generate_mock_user_variant_mapping_table() -> pl.DataFrame:
    # user_id-variantのmappingテーブル
    # user_id 1~4, abtest_id 1001 or 1002, variant control or treatment
    return pl.DataFrame(
        [
            {"user_id": 1, "abtest_id": 1001, "variant": "controll"},
            {"user_id": 2, "abtest_id": 1001, "variant": "controll"},
            {"user_id": 3, "abtest_id": 1001, "variant": "treatment"},
            {"user_id": 4, "abtest_id": 1001, "variant": "treatment"},
            {"user_id": 1, "abtest_id": 1002, "variant": "controll"},
            {"user_id": 2, "abtest_id": 1002, "variant": "treatment"},
            {"user_id": 3, "abtest_id": 1002, "variant": "controll"},
            {"user_id": 4, "abtest_id": 1002, "variant": "treatment"},
        ]
    )


def generate_mock_user_metadata_table() -> pl.DataFrame:
    # ユーザのメタデータテーブル
    return pl.DataFrame(
        [
            {"user_id": 1, "is_paid_user": True, "age": 20, "sex": "male"},
            {"user_id": 2, "is_paid_user": False, "age": 30, "sex": "female"},
            {"user_id": 3, "is_paid_user": True, "age": 30, "sex": "female"},
            {"user_id": 4, "is_paid_user": False, "age": 40, "sex": "male"},
        ]
    )
