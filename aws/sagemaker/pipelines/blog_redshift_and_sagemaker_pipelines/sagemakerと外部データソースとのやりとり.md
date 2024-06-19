## refs:

- https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/
- [redshift-connectorの公式document](https://docs.aws.amazon.com/ja_jp/redshift/latest/mgmt/python-connect-examples.html)
- [SageMaker の Processing job で VPC 内の Redshift に接続できない理由を教えてください](https://dev.classmethod.jp/articles/tsnote-how-to-connect-to-redshift-with-sagemaker-processing-job/)
- [Sagemaker Examples: Ingest data with Redshift](https://sagemaker-examples.readthedocs.io/en/latest/ingest_data/ingest-with-aws-services/ingest_data_with_Redshift.html)
- [sagemaker と snowflake の連携例のnotebook](https://github.com/aws-samples/amazon-sagemaker-w-snowflake-as-datasource/blob/main/snowflake-load-dataset.ipynb)
- [別の VPC にある Amazon SageMaker ノートブックインスタンスから Amazon RDS DB インスタンスに接続するにはどうすればよいですか?](https://repost.aws/ja/knowledge-center/sagemaker-connect-rds-db-different-vpc)
- feature storeを調べると色々わかりそう?[Amazon SageMaker Feature Store を使用してカスタムデータソースから ML 特徴量パイプラインを構築](https://aws.amazon.com/jp/about-aws/whats-new/2023/10/build-ml-feature-pipelines-custom-data-sources-amazon-sagemaker-feature-store/)

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

### RDSに関しては、psycopg2とかmysql-connector-pythonとか使える??

# sagemaker feature storeでcustom data sourcesを使う

