import os
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.function_step import step
from sagemaker.workflow.pipeline_context import PipelineSession
import boto3
from pipeline_steps import news_encoder, item2item_recommender, data_loader
from loguru import logger
import polars as pl

MY_AWS_PROFILE = os.getenv("MY_AWS_PROFILE")
# config.yamlの場所を上書きして明示的に指定することもできる。
# os.environ["SAGEMAKER_USER_CONFIG_OVERRIDE"] = (
#     "aws/sagemaker/pipelines/202311月のupdateで定義が簡単になったかも/sample_codes/sagemaker_pipelines_with_step_decorator/sample_my_config.yaml"
# )


def main(pipeline_session: PipelineSession) -> None:

    news_metadata_df = load_news_metadata_step(
        parquet_s3_uri="my-s3-bucket/news_metadata.parquet"
    )

    news_vector_df = news_encode_step(news_metadata_df=news_metadata_df)

    item2item_recommendation_df = item2item_recommend_step(
        target_vector_df=news_vector_df,
        candidate_vector_df=news_vector_df,
    )

    # pipelineを定義
    pipeline = Pipeline(
        name="news2news-batch-recommendation-pipeline",
        steps=[news_metadata_df, news_vector_df, item2item_recommendation_df],
        sagemaker_session=pipeline_session,
    )
    logger.debug(pipeline)

    pipeline.upsert()


@step(name="load_news_metadata", keep_alive_period_in_seconds=100)
def load_news_metadata_step(parquet_s3_uri: str) -> pl.DataFrame:
    import polars as pl

    return pl.read_parquet(parquet_s3_uri)


@step(name="encode_news", keep_alive_period_in_seconds=100)
def news_encode_step(news_metadata_df: pl.DataFrame) -> pl.DataFrame:
    import polars as pl

    pass


@step(name="recommend_news_to_news")
def item2item_recommend_step(
    target_vector_df: pl.DataFrame,
    candidate_vector_df: pl.DataFrame,
) -> pl.DataFrame:
    import polars as pl

    pass


if __name__ == "__main__":
    # profileを指定してpipeline_sessionを作成
    pipeline_session = PipelineSession(
        boto_session=boto3.Session(profile_name=MY_AWS_PROFILE)
    )
    main(pipeline_session)
