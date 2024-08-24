## refs

- [AWSコスト削減のためのスポットインスタンス活用術](https://www.stylez.co.jp/aws_columns/aws_cost_optimization_and_pdca_cycle/how_to_use_spot_instances_to_reduce_aws_costs/#:~:text=%E3%81%BE%E3%81%A8%E3%82%81-,%E3%82%B9%E3%83%9D%E3%83%83%E3%83%88%E3%82%A4%E3%83%B3%E3%82%B9%E3%82%BF%E3%83%B3%E3%82%B9%E3%81%A3%E3%81%A6%E4%BD%95%EF%BC%9F,%E3%82%AA%E3%83%97%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE1%E3%81%A4%E3%81%A7%E3%81%99%E3%80%82)
- AWS公式のTrainingJobにSpot Instanceを使用するブログ[Managed Spot Training: Save Up to 90% On Your Amazon SageMaker Training Jobs](https://aws.amazon.com/jp/blogs/aws/managed-spot-training-save-up-to-90-on-your-amazon-sagemaker-training-jobs/)
- DevelopersIOさんの記事 [【備忘録】Sagemakerの学習にスポットインスタンスを使う【超カンタン】](https://dev.classmethod.jp/articles/how-to-training-with-spot-instance/)

# スポットインスタンスをTrainingJobで使いたい

## 何それ?

- マネージドスポットインスタンスとは??
  - TrainingJobを実行する際に、スポットインスタンスを使ってコストを削減する機能。70%~90%のコスト削減が可能。
- スポットインスタンスなので当然中断することもある。しかし、MLの場合は途中までの結果をチェックポイントとして保存できるので、中断しても再スタートさせれば良い。
- ちなみに、TrainingJobはマネージドスポットインスタンス対応してるけど、ProcessingJobは対応してないみたい。

## 使い方

- 簡単。
- Sagemaker Python SDKの場合は、Estimatorのコードにスポットインスタンス用の設定を3つ、追加してあげるだけ。
  - `use_spot_instances=True`: スポットインスタンスを使う、という宣言。
  - `max_run`: トレーニングジョブを回す最大秒数。
  - `max_wait`: スポットインスタンスでトレーニングジョブを待つ最大秒数。
  - スポットインスタンスで実行する際は、中断してる間も`max_wait`の秒間だけ待ち続けることになるので、`max_wait`は`max_run`と同じか、より大きい値に設定する必要がある。

```python
estimator = PyTorch(entry_point='train.py',
                            source_dir='source_dir',
                            hyperparameters=hyper_param,
                            role=role,
                            framework_version='1.0.0',
                            py_version="py3",
                            instance_count=1,
                            instance_type='ml.p3.2xlarge',
                            max_run=20000, # 追加1(トレーニングジョブを最大どれだけ回すか)
                            use_spot_instances=True, # スポットインスタンスを使う、という宣言
                            max_wait=20000, # スポットインスタンスでトレーニングジョブをどれだけ回すか
                            output_path=s3_output_data)
```

- AWS Console上でのTrainingJobの表示は以下のような感じになる。
  - 「Training time(seconds)」= 実際にトレーニングジョブが回っていた時間(ex. 15028)
  - 「billable time(seconds)」= 利用料金が発生する時間(ex. 4509)
    - managed spot trainingのおかげで減ってる!
  - 「Managed spot training savings」= スポットインスタンスを使ったことによるコスト削減比率(ex. 70%)

## step decoratorとかでも使える?

- 使えるみたい。step decoratorの引数に同様の設定を追加すれば良い。
  - 参考: [公式ドキュメント](https://sagemaker.readthedocs.io/en/stable/workflows/pipelines/sagemaker.workflow.pipelines.html#step-decorator)

```python
function_step.step(*, name=None, display_name=None, description=None, retry_policies=None, dependencies=None, pre_execution_commands=None, pre_execution_script=None, environment_variables=None, image_uri=None, instance_count=1, instance_type=None, job_conda_env=None, job_name_prefix=None, keep_alive_period_in_seconds=0, max_retry_attempts=1, 
max_runtime_in_seconds=86400, # ここ!
role=None, security_group_ids=None, subnets=None, tags=None, volume_kms_key=None, volume_size=30, encrypt_inter_container_traffic=None, spark_config=None, use_spot_instances=False, # これと!
max_wait_time_in_seconds=None # ここ!
)
```
