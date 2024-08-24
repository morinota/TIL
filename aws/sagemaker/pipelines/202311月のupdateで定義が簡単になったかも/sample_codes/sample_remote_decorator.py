import boto3
import sagemaker
import os
from pathlib import Path
from sagemaker.remote_function import remote

# 実験用の環境変数をグローバル変数として取得
MY_AWS_PROFILE = os.getenv("MY_AWS_PROFILE")
MY_AWS_PIPELINE_BUCKET = os.getenv("MY_AWS_PIPELINE_BUCKET")
MY_SAGEMAKER_ROLE = os.getenv("MY_SAGEMAKER_ROLE")
MY_REDSHIFT_ROLE = os.getenv("MY_REDSHIFT_ROLE")

# Sagemakerがconfigファイルを参照できるように、yamlが存在するディレクトリを環境変数に保存する
os.environ["SAGEMAKER_USER_CONFIG_OVERRIDE"] = str(Path(__file__).parent)

SAGEMAKER_SESSION = sagemaker.Session(
    boto_session=boto3.Session(profile_name=MY_AWS_PROFILE)
)


@remote(instance_type="ml.m5.large", sagemaker_session=SAGEMAKER_SESSION)
def divide(x: float, y: float) -> float:
    return x / y


if __name__ == "__main__":
    print(divide(2.0, 3.0))
