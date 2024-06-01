import abc
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


class RepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def query(self, query: str) -> pl.DataFrame:
        raise NotImplementedError


class Repository:
    def __init__(self):
        app_launch_log_table = generate_mock_app_launch_log_table()
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
    DAU_QUERY = f"""
    with
    user_variant_mapping2 as (
        select
            user_id,
            variant
        from
            user_variant_mapping
        where
            abtest_id = 1001
    )
    , dau_summary as (
        select
            a.timestamp::date
            , user_variant_mapping2.variant as variant
            , count(distinct a.user_id) as dau
        from
            app_launch_log as a
        join user_variant_mapping2
            on a.user_id = user_variant_mapping2.user_id
        group by 1, 2
    )
    select
        timestamp as '日付'
        , variant as 'バリアント'
        , dau as 'DAU'
    from
        dau_summary
    order by timestamp, variant
    """
    repo = Repository()
    # print(
    #     repo.query(
    #         """
    #         with
    #         _user_variant_mapping as (
    #             select
    #                 user_id,
    #                 variant
    #             from
    #                 user_variant_mapping
    #             where
    #                 abtest_id = 1001
    #         )
    #         select
    #             u.*
    #         from
    #             app_launch_log as a
    #         join _user_variant_mapping as u
    #             on a.user_id = u.user_id
    #         """
    #     )
    # )
    # print(repo.query("select * from user_variant_mapping where abtest_id = 1001"))
    # print(repo.query("select * from user_metadata where age >= 30"))
    print(repo.query(DAU_QUERY))
