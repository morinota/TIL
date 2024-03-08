## refs:

- [Amazon SageMaker Data Wrangler で Snowflake データへの直接接続が可能に](https://aws.amazon.com/jp/about-aws/whats-new/2023/06/amazon-sagemaker-data-wrangler-direct-connection-snowflake-data/)
- Sagemaker PipelinesとRedshiftの連携例: [Process Amazon Redshift data and schedule a training pipeline with Amazon SageMaker Processing and Amazon SageMaker Pipelines](https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/)

# Sagemaker PipelinesとRedshiftの連携例:

## introduction

- 開発者は様々なデータソースを扱うケースが多い。
  - ex.) S3のようなobject-basedストレージ、RDSのようなリレーショナルデータベース、Redshiftのようなデータウェアハウス、DynamoDBのようなNoSQLデータベース, etc.
- MLシステムの開発者は多くの場合、DBやテーブルの代わりにobjectsやfileを使うように駆り立てられる。
  - (なんで? SagemakerがS3からとしかやり取りしないようになってるから? アクセス速度が早いから??)
- とはいえ、場合によっては、SQL等のクエリを使ってDBからモデルの学習に使うデータを取得する必要があるかもしれない。
- ## このページは、**Sagemaker ProcessingJobを使用してRedshiftクラスタに対してクエリを実行し**、csvファイルを作成し、分散処理を実行する。

## 実装例

- まずは、Redshiftクラスタに対してデータを抽出するクエリを定義する。
- Sagemaker ProcessingJobでは、Amazon S3, Amazon Athena, Amazon Redshiftなど、様々なリソースからデータを直接readする事ができる。(そうなの...??! S3だけかと思ってた...!)
  - ProcessingJobでは、clusterとDBの情報を提供する事でclusterへのアクセスを構成できる。
  - そして`RedshiftDatasetDefinition`の一部として事前に定義したSQLクエリを実行できる。

実装例は以下:

- まずは、`RedshiftDatasetDefinition`オブジェクトを定義する。(ここでRedshiftクラスタの情報や、実行したいクエリを提供する感じか...!)

```python
from sagemaker.dataset_definition.inputs import RedshiftDatasetDefinition

rdd = RedshiftDatasetDefinition(
    cluster_id="THE-NAME-OF-YOUR-CLUSTER",
    database="THE-NAME-OF-YOUR-DATABASE",
    db_user="YOUR-DB-USERNAME",
    query_string="THE-SQL-QUERY-FROM-THE-PREVIOUS-STEP",
    cluster_role_arn="THE-IAM-ROLE-ASSOCIATED-TO-YOUR-CLUSTER",
    output_format="CSV",
    output_s3_uri="WHERE-IN-S3-YOU-WANT-TO-STORE-YOUR-DATA"
)
```

- 次に`DatasetDefinition`オブジェクトを定義する。
  - このオブジェクトは、Redshiftから取得したデータセットを、ProcessingJobがどのように使用するかを定義する役割。

```python
from sagemaker.dataset_definition.inputs import DatasetDefinition

dd = DatasetDefinition(
    data_distribution_type='ShardedByS3Key', # This tells SM Processing to shard the data across instances
    local_path='/opt/ml/processing/input/data/', # Where SM Processing will save the data in the container
    redshift_dataset_definition=rdd # Our ResdhiftDataset
)
```

- 最後に、この`DatasetDefinition`オブジェクトを使って、`Processor`オブジェクトの入力データ`ProcessingInput`オブジェクトを定義する。

```python
processor = Processor(
    framework_version='0.23-1',
    role=get_execution_role(),
    instance_type='ml.m5.large',
    instance_count=1
)
processor.run(
    code='processing/processing.py',
    inputs=[ProcessingInput(
        dataset_definition=dd,
        destination='/opt/ml/processing/input/data/',
        s3_data_distribution_type='ShardedByS3Key'
    )],
    outputs = [
        ProcessingOutput(
            output_name="train",
            source="/opt/ml/processing/train"
        ),
        ProcessingOutput(
            output_name="test",
            source="/opt/ml/processing/test"
        ),
    ],
)
```

- (ちなみに、このProcessingJobは学習データセットを `train` と `test` に分割するジョブを想定)
- ちなみに、上で定義したProcessingJobのoutputを、以下のようにTrainingJobの入力として定義できる。

```python
estimator = Estimator(
    entry_point='training/script.py',
    framework_version='0.23-1',
    instance_type='ml.m5.large',
    instance_count=1,
    role=get_execution_role()
)
estimator.fit({
    'train':processor.latest_job.outputs[0].destination,
    'test':processor.latest_job.outputs[1].destination
})
```

## まとめ

- **追加の設定やサービスを必要とせずに、RedshiftからnativeにデータをSagemakerジョブにreadさせる**事ができる...!
  (- Redshift Data APIっていうのもあるっぽい? これをSagemaker Job内で呼ぶアプローチもあるのかな...??:thinking_face:)
