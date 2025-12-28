## これは何??

- AWS Lake Formationをよく知らなかったので、概要を調査したメモ

## refs

- [AWS Lake Formationの概要を図と用語で整理する](https://qiita.com/sot528/items/8a4c3adf9ba5c2da3fa9)
- [Overview of Lake Formation permissions](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-overview.html)
- [PyIcebergを使ってLambdaからS3 TablesのIcebergテーブルに書き込んでみる](https://dev.classmethod.jp/articles/tried-to-write-to-iceberg-tables-in-s3-tables-from-lambda-using-pyiceberg/)

## ざっくりAWS Lake Formationとは?

- AWSでデータレイクを構築・管理するためのマネージドサービス。
  - 実体は、ほぼAWSの各種サービス(Glue, IAM, S3, etc.)をwrapしたもの。
  - **データレイク専用にアクセス制御を行うために、IAMとは別に独自の権限管理機構を持つ**。
- **Lake FormationはGlueとデータカタログを共有する**。

## Icebergテーブルへのアクセス権限の話

- IAMロールへの権限付与だけではIcebergテーブルへアクセスできないっぽい。
  - Lake Formationでも、実行ロールに対して、Icebergテーブルへのアクセス権限を付与する必要があるっぽい。
- なんで必要? なんでIAM権限だけでは不十分なの??
  - IAM -> LFによる二段階チェックになるから。両方passしないとアクセスできない。
  - ざっくり以下のような分担になってるイメージ:
    - 1. IAM: 「どのAWS APIを叩いていいか」を決める大枠の権限管理。
      - ex. IAM「Glue/Lake Formation / S3にアクセスしていいよ！」
    - 2. Lake Formation: 「そのデータレイク内のどのデータに、どの操作をしていいか」を決める詳細な権限管理。
      - ex. LF「その中のhogeテーブルに書き込みしていいよ！」

### LF側で特定のIAMロールに権限を付与する方法

特定のS3テーブルバケットへのアクセス権限を付与する場合の手順:

```bash
## データベースへの権限付与
## AWS_PRINCIPAL_ARN は、Lambda関数にアタッチするIAMロールのARN
aws lakeformation grant-permissions \
  --catalog-id "${AWS_ACCOUNT_ID}" \
  --principal "{\"DataLakePrincipalIdentifier\": \"${AWS_PRINCIPAL_ARN}\"}" \
  --resource "{\"Database\": {\"CatalogId\": \"${AWS_ACCOUNT_ID}:s3tablescatalog/${TABLE_BUCKET_NAME}\", \"Name\": \"main\" }}" \
  --permissions "ALL"
```

```bash
## テーブルへの権限付与
aws lakeformation grant-permissions \
  --catalog-id "${AWS_ACCOUNT_ID}" \
  --principal "{\"DataLakePrincipalIdentifier\": \"${AWS_PRINCIPAL_ARN}\"}" \
  --resource "{\"Table\": {\"CatalogId\": \"${AWS_ACCOUNT_ID}:s3tablescatalog/${TABLE_BUCKET_NAME}\", \"DatabaseName\": \"main\", \"TableWildcard\": {} }}" \　## ここでは特定のバケット内の全テーブルに対して権限を付与している
  --permissions "ALL" 
```
