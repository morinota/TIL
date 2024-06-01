from data.data_models import (
    AppLaunchLogSchema,
    UserVariantMappingSchema,
    UserMetadataSchema,
)
from data.mock_data import (
    generate_mock_app_launch_log_table,
    generate_mock_user_variant_mapping_table,
    generate_mock_user_metadata_table,
)
import polars as pl


class Repository:
    def __init__(self):
        app_launch_log_table = generate_mock_app_launch_log_table(100)
        user_variant_mapping_table = generate_mock_user_variant_mapping_table()
        user_metadata_table = generate_mock_user_metadata_table()

        # validation
        AppLaunchLogSchema.validate(app_launch_log_table)
        UserVariantMappingSchema.validate(user_variant_mapping_table)
        UserMetadataSchema.validate(user_metadata_table)

        # register tables as attributes
        self.app_launch_log = app_launch_log_table
        self.user_variant_mapping = user_variant_mapping_table
        self.user_metadata = user_metadata_table

        # register tables as temporary tables
        self.ctx = pl.SQLContext(
            app_launch_log=app_launch_log_table,
            user_variant_mapping=user_variant_mapping_table,
            user_metadata=user_metadata_table,
        )

    def query(self, query: str) -> pl.DataFrame:
        return self.ctx.execute(query, eager=True)


if __name__ == "__main__":
    repo = Repository()
    print(repo.query("select * from app_launch_log where timestamp >= '2024-01-02'"))
    print(repo.query("select * from user_variant_mapping where abtest_id = 1001"))
    print(repo.query("select * from user_metadata where age >= 30"))
