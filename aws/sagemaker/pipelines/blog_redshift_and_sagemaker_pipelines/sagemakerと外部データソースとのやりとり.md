## refs:

- https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/
- [redshift-connectorの公式document](https://docs.aws.amazon.com/ja_jp/redshift/latest/mgmt/python-connect-examples.html)
- [SageMaker の Processing job で VPC 内の Redshift に接続できない理由を教えてください](https://dev.classmethod.jp/articles/tsnote-how-to-connect-to-redshift-with-sagemaker-processing-job/)
- [Sagemaker Examples: Ingest data with Redshift](https://sagemaker-examples.readthedocs.io/en/latest/ingest_data/ingest-with-aws-services/ingest_data_with_Redshift.html)

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
  
