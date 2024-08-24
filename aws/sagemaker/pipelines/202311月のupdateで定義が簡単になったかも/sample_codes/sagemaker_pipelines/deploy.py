import os

import boto3.session

from pipelines.news_vectorizer_5minutely_pipeline import (
    define_news_vectorizer_5_minutely_pipeline,
)
from sagemaker.workflow.pipeline_context import PipelineSession

import boto3
from sagemaker.feature_store.feature_definition import FeatureTypeEnum


# 実験用の環境変数をグローバル変数として取得
MY_AWS_PROFILE = os.getenv("MY_AWS_PROFILE")
MY_AWS_PIPELINE_BUCKET = os.getenv("MY_AWS_PIPELINE_BUCKET")
MY_SAGEMAKER_ROLE = os.getenv("MY_SAGEMAKER_ROLE")
MY_REDSHIFT_ROLE = os.getenv("MY_REDSHIFT_ROLE")

# Sagemakerがconfigファイルを参照できるように、yamlが存在するディレクトリを環境変数に保存する
os.environ["SAGEMAKER_USER_CONFIG_OVERRIDE"] = (
    "aws/sagemaker/pipelines/202311月のupdateで定義が簡単になったかも/sample_codes/sagemaker_pipelines/config.yaml"
)


def main() -> None:
    print(MY_AWS_PIPELINE_BUCKET)
    print(os.environ["SAGEMAKER_USER_CONFIG_OVERRIDE"])

    # profileを指定してpipeline_sessionを作成
    pipeline_session = PipelineSession(
        boto_session=boto3.Session(profile_name=MY_AWS_PROFILE),
        default_bucket=MY_AWS_PIPELINE_BUCKET,
    )

    pipeline = define_news_vectorizer_5_minutely_pipeline(
        pipeline_session=pipeline_session,
        role_arn=MY_SAGEMAKER_ROLE,
    )
    print(pipeline.definition())


if __name__ == "__main__":
    main()
