## refs:

- [SnowflakeからGlue Data Catalogを使ってIcebergテーブルにアクセスしてみる](https://qiita.com/Himeka_Kawaguchi/items/00f41e6e9f2ddf942c0a)
- [Snowflake と Glue Data Catalog をカタログ統合し自動リフレッシュの動作を確認する](https://dev.classmethod.jp/articles/snowflake-catalog-integration-with-glue-data-catalog-and-auto-refresh/)

## これは何??

- Sagemaker Feature Storeのオフラインストアに保存されている特徴量データに、Snowflakeから参照可能にする方法について調べたメモ。
- できるはずという認識は元々ある。
  - Glue Data Catalogで管理されるS3上のテーブルデータを、Snowflakeから参照する仕組みはすでに存在してて。ブログもある。
  - そして、Sagemaker Feature Storeのオフラインストアは、Iceberg形式にしろGlue Table形式にしろ、Glue Data Catalogで管理されるS3上のテーブルデータとして保存されてる。
  - じゃあできるはずだよね...!:thinking:

## 事前情報として知っておくべきこと

### Sagemaker側

- Sagemaker Feature Storeのオフラインストアは、Glue Data Catalogで管理されるS3上のテーブルデータとして保存されてる。
  - テーブル形式は2種類ある:
    - Glue Table形式: Hive互換のGlueテーブル形式（**Hive Table形式**）
      - デフォルトはこれで、Glue Data Catalogに普通のHiveタイプのテーブルとして登録されるやつ。
    - Iceberg形式: **Apache Icebergテーブル形式**
      - 最新のやつで、Glue Data CatalogにIcebergテーブル（Iceberg形式: open table format）として登録される。
    - どちらもGlue Data Catalog管理だが、Icebergの方が新しいデータレイク用の技術になってるらしい。

### Snowflake側

- Catalog Integration（カタログ統合）
  - SnowflakeとAWS Glue Data CatalogやS3データレイクをつなぐ認証付きの定義。
  - 超重要な設定項目。
- External Volume（外部ボリューム）
  - S3上のデータにSnowflakeからアクセスするためのストレージ定義。
  - 「どのS3バケットのどのディレクトリを使う？」ってやつをまとめる箱みたいなイメージ。
- CATALOG_NAMESPACE/CATALOG_TABLE_NAME
  - Glue Data Catalog内の「どのデータベース・テーブルを参照するか？」を指定するパラメータ。
- GLUE_REGION/GLUE_CATALOG_ID
  - Glue Data CatalogのAWSリージョンやアカウントID指定。

## ざっくりやり方!

### 手順1: Snowflake側でCatalog Integration(カタログ統合)を作成する

以下のSQLを実行してAWS Glueのカタログ統合を作成する。

```sql
--Glueのカタログ統合を作成
CREATE OR REPLACE CATALOG INTEGRATION <カタログ統合の名前>
  CATALOG_SOURCE = GLUE
  TABLE_FORMAT = ICEBERG
  GLUE_AWS_ROLE_ARN = '<IAMロールのARN>'
  GLUE_CATALOG_ID = '<Glue Data Catalog を管理する AWS アカウント ID>'
  GLUE_REGION = '<Glue Data Catalog の AWS リージョン>'
  CATALOG_NAMESPACE = '<Glue Data Catalog のデータベース名>'  
  ENABLED = TRUE -- そのカタログ統合を有効にするか否か(連携ON/OFFの切り替え)
;
```

作成したカタログ統合をDESCRIBEして、**AWSに渡す情報を取得**する。

- GLUE_AWS_IAM_USER_ARN
  - SnowflakeアカウントにあるAWS IAMエンティティ
- GLUE_AWS_EXTERNAL_ID
  - 信頼関係を確立するために必要な外部ID


```sql
DESCRIBE CATALOG INTEGRATION <カタログ統合の名前>;
```

SnowflakeのAWS IAMエンティティにAWS側で用意したロールを引き渡すため、IAMロールの信頼関係にSnowflakeの情報を追加する。
これによりSnowflakeからAWSにアクセス出来るようになる。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "< SnowflakeのGLUE_AWS_IAM_USER_ARN の値 >"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": [
                        "< SnowflakeのGLUE_AWS_EXTERNAL_ID の値 >"
                    ]
                }
            }
        }
    ]
}
```

## 手順2: Snowflake側でExternal Volume(外部ボリューム)を作成する

以下のSQLを実行して、AWSに保存されているデータにアクセスするため外部ボリュームを作成する。

```sql
CREATE OR REPLACE EXTERNAL VOLUME <外部ボリュームの名前>
   STORAGE_LOCATIONS =
      (
         (
            NAME = '<名前>'
            STORAGE_PROVIDER = 'S3'
            STORAGE_BASE_URL = 's3://<作成したs3バケット>'
            STORAGE_AWS_ROLE_ARN = '<IAMロールのARN>'
            STORAGE_AWS_EXTERNAL_ID = 'iceberg_table_external_id'
         )
      )
      ALLOW_WRITES = FALSE; --読み取り専用に
```

先ほどのカタログ統合の場合と同様に、`describe`して、AWS側に渡す情報を取得する。

- `STORAGE_AWS_EXTERNAL_ID`
  - 信頼関係を確立するために必要な外部ID

```sql
DESCRIBE EXTERNAL VOLUME <外部ボリュームの名前>;
```

先ほどのカタログ統合の場合と同様に、IAMロールの信頼関係にSnowflakeの情報を追加する。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "< SnowflakeのGLUE_AWS_IAM_USER_ARN の値 >"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": [
                        "< SnowflakeのGLUE_AWS_EXTERNAL_ID の値 >",
                        // ここに新たに追加!
                        "< SnowflakeのSTORAGE_AWS_EXTERNAL_ID の値 >"
                    ]
                }
            }
        }
    ]
}
```

AWSの認証が上手くいっているか確認のため、外部ボリュームにアクセスできるか試す。

```sql
SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('<外部ボリューム名>');
-- "success":trueが返却されれば成功!
```

## 手順3: Snowflake側でIcebergテーブルを定義する

Snowflakeでテーブルを作成する前に、IAMポリシー に s3:GetObjectを追加します。これにより、外部ボリュームを使用してS3にあるデータへアクセス出来るようになる。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowGlueCatalogTableAccess", 
            "Effect": "Allow",
            "Action": [
                "glue:GetTable",
                "glue:GetTables"
            ],
            "Resource": [
                "arn:aws:glue:*:xxxxx:table/*/*",
                "arn:aws:glue:*:xxxxx:catalog",
                "arn:aws:glue:*:xxxxx:database/default"
            ]
        },
        {
            "Sid": "AllowS3BucketAccess", // ここを追加!
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "<S3のURL>/*"
        }
    ]
}
```

続いて以下のSQLを実行して、Snowflake側にIcebergテーブルを作成する。
(データの実体はS3上、テーブルメタデータはGlue Data Catalogにあるので、あくまでエイリアスを作る的なイメージ...!:thinking:)

```sql
--データベース、スキーマ作成
USE DATABASE db;
USE SCHEMA sc;
--Icebergテーブル作成
CREATE ICEBERG TABLE db.sc.<テーブル名>
  EXTERNAL_VOLUME='<作成した外部ボリューム>' -- データの実体はS3上にあるので、そのS3URLを指す外部ボリュームを指定
  CATALOG='<作成したカタログ統合>' -- テーブルのメタデータはGlue Data Catalogで管理されているので、そのGlue Data Catalogにアクセスするためのカタログ統合を指定
  CATALOG_TABLE_NAME='<Glue Data Catalogにあるテーブル名>';
```

IcebergテーブルをSELECTしデータが取得できるか確認する。

```sql
SELECT * from db.sc.<テーブル名>;
```

無事にGlue Data Catalogに作成したIcebergテーブルのデータがSELECTできたら完了!

## ちなみに、これに伴う利用料金ってどこで発生しそう??

- Snowflake側の利用料金:
  - Iceberg（外部テーブル）読みにも、Snowflakeの「仮想ウェアハウス（コンピュート）の利用料」がかかる！つまりクエリを実行した分だけ処理リソース課金。
    - たぶん全体の中で、ここのウェアハウス(計算リソース)のサイズと稼働時間が一番インパクトある!
  - なお、Snowflakeのストレージ課金は今回は発生しない。external tableなので。
- S3の利用料金:
  - S3のストレージ容量とAPI（GetObject等）利用料は、AWS課金として別途発生する。
- Glueの利用料金:
  - Glue Data Catalogのメタデータ参照やAPIコール（GetTable等）は大抵無料か激安だけど、大量アクセスでAPIコール数が多ければ微妙に増える可能性アリ。

もしオフラインストアのデータ量が増えた場合はどこに影響出る??

- おそらくはSnowflake側のウェアハウス利用料金が一番影響出る。
  - 大量データを処理するために、同じサイズのウェアハウスでもクエリにより長い時間がかかるようになるかもしれないので。 -> 結果的にウェアハウスの稼働時間が増える。
  - クエリの複雑さやスキャン対象のデータ量が増えれば増えるほど、ウェアハウスサイズを上げるか、実行時間が伸びる＝料金UPって超わかりやすいシンプル課金。
