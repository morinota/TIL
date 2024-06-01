from enum import Enum
from data.repository import RepositoryInterface


DAU_QUERY = f"""
with
    user_variant_mapping as (
        select
            user_id,
            variant
        from
            user_variant_mapping
        where
            abtest_id = 1001
    )
    select
        timestamp::date
        , count(distinct user_id) as dau
    from
        app_launch_log
    group by 1
"""


def calc_metric(query: str, repo: RepositoryInterface) -> float:
    return repo.query(query)
