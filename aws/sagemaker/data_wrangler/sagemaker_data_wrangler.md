## refs:

- [Amazon SageMaker Data Wrangler で Snowflake データへの直接接続が可能に](https://aws.amazon.com/jp/about-aws/whats-new/2023/06/amazon-sagemaker-data-wrangler-direct-connection-snowflake-data/)
- Sagemaker PipelinesとRedshiftの連携例: [Process Amazon Redshift data and schedule a training pipeline with Amazon SageMaker Processing and Amazon SageMaker Pipelines](https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/)
- Amazon SageMaker Data Wranglerの公式docs:[Amazon SageMaker Data Wrangler](https://aws.amazon.com/jp/sagemaker/data-wrangler/)

# Amazon SageMaker Data Wranglerとは??
- Data Wranglerとは?
  - Sagemaker Studio上の機能で、ML向けの前処理を行うサービス。
  - ほとんどコーディングなしで、データ前処理と特徴量エンジニアリングを簡素化・効率化できる。
  - また、様々なソース(ex. S3、Athena、Redshift)や40以上のサードパーティのデータソースにアクセスすることが可能。
- SageMaker Data Wrangler(データラングラー)でできること:
  - 1. **様々なデータソース**に迅速にアクセスしてデータを取得できる。
    - データソースの例: Amazon Simple Storage Service [Amazon S3]、Amazon Athena、Amazon Redshift、AWS Lake Formation、Amazon EMR、Snowflake、and Databricks Delta Lake, etc.
    - また、**SQLでデータソースへのクエリを記述しSagemakerにデータを直接importする事もできる**。
  - 2. data insightの生成とデータ品質の把握:
    - データ品質(欠損値, 重複行, データ型, etc.)を自動的に検証し、データの以上(外れ値, クラスの不均衡)を検出するのに役立つ、data quality and insights reportを生成できる。
  - 3. データの効率的な変換:
    - Data wranglerは、PySparkベースのbuild-inデータ変換機能を300種類以上提供している。
      - ex. jsonファイルの平坦化, 重複行の削除, 平均値や中央値による欠損データ補完, one-hot encoding, etc.
    - なので、コードを1行も記述せずにデータ変換するpreprocessを実装できる。
    - また、PySpark, SQL, Pandasでカスタムtransformationsを実装する事もできる。

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
