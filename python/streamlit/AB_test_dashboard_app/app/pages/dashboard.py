import streamlit as st
from data.repository import Repository

DAU_QUERY = """
    with
    _user_variant_mapping as (
        select
            user_id,
            variant
        from
            user_variant_mapping
        where
            abtest_id = [abtest_id]
    )
    , dau_summary as (
        select
            a.timestamp::date
            , _user_variant_mapping.variant as variant
            , count(distinct a.user_id) as dau
        from
            app_launch_log as a
        join _user_variant_mapping
            on a.user_id = _user_variant_mapping.user_id
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


def display(abtest_id: int) -> None:
    st.header(f"ABテスト (abtest_id={abtest_id}) の結果")

    # データソースへのアクセスを抽象化したRepositoryクラスを初期化
    repository = Repository()

    # metricsの計算
    dau_result = repository.query(DAU_QUERY.replace("[abtest_id]", str(abtest_id)))
    print(dau_result)

    # 結果の表示
    st.write("DAU")
    # dataframeとして表示
    st.write(dau_result.to_pandas())

    # グラフの表示
    st.line_chart(dau_result.to_pandas(), x="日付", y="DAU", color="バリアント")


if __name__ == "__main__":
    display(abtest_id=1001)
