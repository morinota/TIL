## refs:

- https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/
- [redshift-connectorの公式document](https://docs.aws.amazon.com/ja_jp/redshift/latest/mgmt/python-connect-examples.html)
- [SageMaker の Processing job で VPC 内の Redshift に接続できない理由を教えてください](https://dev.classmethod.jp/articles/tsnote-how-to-connect-to-redshift-with-sagemaker-processing-job/)
- [Sagemaker Examples: Ingest data with Redshift](https://sagemaker-examples.readthedocs.io/en/latest/ingest_data/ingest-with-aws-services/ingest_data_with_Redshift.html)
- [sagemaker と snowflake の連携例のnotebook](https://github.com/aws-samples/amazon-sagemaker-w-snowflake-as-datasource/blob/main/snowflake-load-dataset.ipynb)
- [別の VPC にある Amazon SageMaker ノートブックインスタンスから Amazon RDS DB インスタンスに接続するにはどうすればよいですか?](https://repost.aws/ja/knowledge-center/sagemaker-connect-rds-db-different-vpc)
- feature storeを調べると色々わかりそう?[Amazon SageMaker Feature Store を使用してカスタムデータソースから ML 特徴量パイプラインを構築](https://aws.amazon.com/jp/about-aws/whats-new/2023/10/build-ml-feature-pipelines-custom-data-sources-amazon-sagemaker-feature-store/)
- Sagemaker notebookからRedshiftにアクセスするsample notebook: [Discovery: how to use Data API to query RedShift from Python](https://github.com/aws-samples/sagemaker-processing-reading-data-from-redshift-to-sagemaker-pipelines/blob/main/extra-content/data-api-discovery.ipynb)
- まさに今回のためのaws-sampleリポジトリ?? [Process Amazon RedShift data and schedule a training pipeline with Amazon SageMaker Processing and Amazon SageMaker Pipelines](https://github.com/aws-samples/sagemaker-processing-reading-data-from-redshift-to-sagemaker-pipelines/tree/main)
- aws re:Postのまさに自分が知りたい質問: [Sagemaker and Data on Databases](https://repost.aws/questions/QUh_P30-iXTKmzZv0D4vtLOA/sagemaker-and-data-on-databases)

# Sagemakerのみでなんとか外部データソースと入出力のやりとりできる??

## sagemaker.dataset_definition周りを確認


## Sagemaker Data Wranglerを使える??

## 普通にProcessingJob内で、外部データソースにアクセスする処理を書く??

### Redshiftに関しては、redshift_connectorが使える??

サンプルコード

```python
import redshift_connector
conn = redshift_connector.connect(
     host='examplecluster.abc123xyz789.us-west-1.redshift.amazonaws.com',
     database='dev',
     port=5439,
     user='awsuser',
     password='my_password'
  )
```

### Snowflakeに関しては、snowflake-connector-pythonが使える??

- サンプルノートブックを見ると、`snowflake-connector-python`と`pyarrow`を使っている。
  - 参考:
    - [sagemaker と snowflakeの連携例のnotebook](https://github.com/aws-samples/amazon-sagemaker-w-snowflake-as-datasource/blob/main/snowflake-load-dataset.ipynb)
    - Sagemakerのブログ　[Use Snowflake as a data source to train ML models with Amazon SageMaker](https://aws.amazon.com/jp/blogs/machine-learning/use-snowflake-as-a-data-source-to-train-ml-models-with-amazon-sagemaker/)

```python
snowflake-connector-python
pyarrow
```

# Sagemaker notebookからRedshiftにアクセスするsample notebookのメモ:

- わかったことメモ:
  - アクセスに必要な情報:
    - cluster_id, database, db_userの3つのconfigを指定すると、認証情報が一意に決まる?
    - Sagemakerに渡すroleに必要な条件:
      - 対象の認証情報のリソースに対して`redshift:GetClusterCredentials`アクションの権限を持ってる必要がある。
      - 参考: https://dev.classmethod.jp/articles/authorizing-access-to-redshift-data-api-and-deny-ip/
    - unloadクエリやcopyクエリを実行する時に指定するiam_roleに必要な条件:
      - S3に対する必要なアクション権限を持ってる必要がある。
      - かつ、Redshiftのクラスターの`roles`に登録されている必要がある。(これは初知りだった...!:thinking:)
        - cdkでRedshiftのクラスターを定義してるところで指定したroleが、Redshiftのクラスターに紐づくroleとして有効になるっぽい...!:thinking:
        - 参考: https://dev.classmethod.jp/articles/amazon-redshift-iam-role/

- まず準備:
  - クラスターアクセス、ロールARN、出力S3 uriなどの設定を用意する。

```python
###### CLUSTER CONFIGURATION
cluster_id = input("The name of your Redshift cluster:")
database = input("The database of your Redshift cluster (default: dev)") or 'dev'
db_user = input("The user of your Redshift cluster (default: awsuser)") or 'awsuser'
```

(上記の3つの情報があればOK??:thinking:)
Redshiftクラスターに接続するためのconfigを用意できたら、boto3を使ってアクセスできる。

```python
import boto3
import time

query_string = """
select * from hogehoge_table limit 5;
"""

# Execute the Data API query
client = boto3.client('redshift-data')
execution_id = client.execute_statement(
    ClusterIdentifier=cluster_id,
    Database=database,
    DbUser=db_user,
    Sql=query_string,
)['Id']
print(f'Execution started with ID {execution_id}')

# クエリの実行が終わるまで待つ
status = client.describe_statement(Id=execution_id)['Status']
while status not in ['FINISHED','ABORTED','FAILED']:
    time.sleep(10)
    status = client.describe_statement(Id=execution_id)['Status']
print(f'Execution {execution_id} finished with status {status}')

# 結果を取得
if status == 'FINISHED':
    columns = [c['label'] for c in client.get_statement_result(Id=execution_id)['ColumnMetadata']]
    records = client.get_statement_result(Id=execution_id)['Records']
    print(f'SUCCESS. Found {len(records)} records')
else:
    print(f'Failed with Error: {client.describe_statement(Id=execution_id)["Error"]}')
```

# Sagemaker から プライベートサブネット内のRDSにアクセスする方法

- 参考:
  - [Connect to RDS from basic SageMaker Studio domain?](https://repost.aws/ja/questions/QUksj1ZyvgQbCveN6a8laexA/connect-to-rds-from-basic-sagemaker-studio-domain)
- 上記資料によると以下のことがわかった。
  - デフォルトのquick setupで作られる Sagemaker Domain では、public internet accessになる。(i.e. direct-to-internet)
    - direct-to-internetのSagemaker Domainは、RDSインスタンスがinternetからアクセスできる場合にのみ、ノートブックからアクセスできるようになる。
    - よってこの場合、private subnetにあるRDSインスタンスにはアクセスできない。
  - -> **private subnetにあるRDSにアクセス可能にするためには、quick setupではなくstandard setupを選択してSagemaker Domainを作る必要がある**。
    - ざっくり以下のことを準備しておく必要がありそう.
      - VPCの設定: Sagemaker  Studioが同じVPC内にあるか、RDSインスタンスがあるVPCとVPC peeringが設定されている必要がある。
      - セキュリティグループの設定: RDSインスタンスに関連づけられているセキュリティグループに、Sagemaker Studioのセキュリティグループからのアクセスを許可する必要がある。
        - ex. Sagemaker Studioが所属するVPCのCIDRブロックからのinboundアクセスを許可する。
