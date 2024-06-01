from datetime import datetime
import polars as pl
from data.data_models import (
    AppLaunchLogSchema,
    UserVariantMappingSchema,
    UserMetadataSchema,
)
import numpy as np


def generate_mock_app_launch_log_table(num_rows: int) -> pl.DataFrame:
    # アプリ起動ログテーブル
    return pl.DataFrame(
        {
            # user_id 1~4をランダムに
            "user_id": np.random.randint(1, 5, num_rows),
            # 2024-01-01, 2024-01-02, 2024-01-03, 2024-01-04をランダムに(時刻は00:00:00)
            "timestamp": [
                datetime(2024, 1, i) for i in np.random.randint(1, 5, num_rows)
            ],
            # iOS, Androidをランダムに
            "os": np.random.choice(["iOS", "Android"], num_rows),
        }
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
