## refs:

- https://sagemaker.readthedocs.io/en/stable/overview.html#run-machine-learning-code-on-sagemaker-using-remote-function
- [developerガイドの詳細](https://docs.aws.amazon.com/sagemaker/latest/dg/train-remote-decorator.html)
- [remote functionについて](https://sagemaker.readthedocs.io/en/stable/remote_function/sagemaker.remote_function.html)

# ローカルのMLコードをサクッとSagemaker上のインスタンスで実行できる`remote`デコレータ

- `@remote`デコレータを使うと、wrapしたローカルのMLコードをSagemakerのTrainingJobとして実行できる。
  - instance typeはデコレータの引数で指定できる。
  - **ローカルのワークスペース環境 & 関連するデータ処理コード & データセットを**、Sagemaker Trainingプラットフォーム上で実行するSagemaker TrainingJobに自動的に変換。
- 永続キャッシュ機能を有効にすると、以前にダウンロードした依存パッケージをキャッシュでき、ジョブの起動待ち時間を短縮できる。
  - この機能による時間短縮は、Sagemaker managed warmpoolによる短縮よりも大きな効果になる?


```python
import boto3
import sagemaker
from sagemaker.remote_function import remote

sm_session = sagemaker.Session(boto_session=boto3.Session(profile="MY_PROFILE"))
settings = dict(
    sagemaker_session=sm_session,
    role=<The IAM role name>,
    instance_type="ml.m5.xlarge",
    dependencies="auto_capture"
)

@remote(**settings)
def divide(x, y):
    return x / y


if __name__ == "__main__":
    print(divide(2, 3.0))
```
