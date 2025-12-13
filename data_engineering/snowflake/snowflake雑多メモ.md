## Catalog Linked Database 機能について

### refs:
  - [Oct 17, 2025: Write support for externally managed Apache Iceberg™ tables and catalog-linked databases (General availability)](https://docs.snowflake.com/en/release-notes/2025/other/2025-10-17-iceberg-external-writes-cld-ga)
  - [外部管理 Apache Iceberg™ テーブルへの書き込みサポート](https://docs.snowflake.com/ja/user-guide/tables-iceberg-externally-managed-writes)
  - [カタログリンクデータベースでのIcebergテーブルの作成](https://docs.snowflake.com/ja/user-guide/tables-iceberg-externally-managed-writes#create-an-iceberg-table-in-a-catalog-linked-database)
  - [Use a catalog-linked database for Apache Iceberg™ tables](https://docs.snowflake.com/en/user-guide/tables-iceberg-catalog-linked-database)

### ざっくり

- 外部のカタログ(ex. AWS Glue Data Catalogなど)を**Snowflake内に仮想DBとしてリンク**して、そのまま**普通のSnowflakeテーブルっぽくクエリできる**機能。
- 外部カタログで管理されてるIcebergテーブルなどを、ネイティブに扱える。
- イメージ:
  - Icebergカタログ ---リンク---> Snowflake内の仮想DB --> 普通のSnowflakeテーブルっぽくクエリできる。
  - ここでSnowflakeはあくまで"ビュー+メタデータ同期エンジン"みたいな動きで、データファイル自体はS3などをそのまま参照するイメージ。
- メリット:
- メタデータをSnowflakeが自動で同期.
  - (icebergテーブルのmetadata.jsonをSnowflake側で自動で取り込んでくれるイメージ)
- Data copy不要 (zero-copyアーキテクチャ)
- select時にSnowflake側のクエリ最適化を効かせる事ができる(Iceberg側のstatistic情報を利用)。

### 2025/10/17 のアップデートで追加されたみたい！

- 外部カタログで管理されたIcebergテーブルへの書き込みが正式提供(GA, general availability)になった!
  - 外部のIceberg RESTカタログ (ex. AWS Glue Data Catalog)と繋げるcatalog linked databaseもGAになった!
  - **Snowflake を通して、外部カタログ上に 新規 Iceberg テーブルの作成、および INSERT / UPDATE / DELETE / MERGE といった通常の DML 操作が可能になった。つまり、データレイクや Iceberg エコシステムと双方向でやり取りできるようになった。**
- 同日にGAされた関連機能:
  - Iceberg テーブルへのパーティション付き書き込み(partitioned writes)のサポート。外部 or Snowflake 内部の Iceberg テーブルの両方に対して。
  - ターゲットparquetファイルサイズの指定。

### 特定のデータベースが、catalog-linked database かどうかの確認方法

```sql
-- 対象のDBが、catalog-linked databaseか否か確認(KINDカラム)
SHOW DATABASES LIKE '<my_database_name>';
```

出力の`KIND`カラムが `CATALOG-LINKED DATABASE` かその他か。

もしcatalog-linked database の場合は、以下のクエリで状態を確認できる。

```sql
-- 対象catalog linked databaseの状態を確認
SELECT SYSTEM$CATALOG_LINK_STATUS('<my_database_name>');
```

- catalog linked DBじゃない名前を渡すとエラーになる。
- JSONが帰ってきて、`executionState`が`RUNNING`なら、ちゃんと外部カタログとlinkできてる状態。
  - 

### Icebergテーブルの作成方法。

Snowflakeから外部管理Icebergテーブルを作成する場合、使用するデータベースの種類によって、以下の2通りの方法がある。

- catalog linked database を使用する場合
  - [CREATE ICEBERG TABLE（カタログリンクデータベース）](https://docs.snowflake.com/ja/sql-reference/sql/create-iceberg-table-rest.html#label-tables-iceberg-external-write-create-table-syntax)コマンドを使用する。
- 標準のSnowflake database を使用する(catalog linked databaseを使用しない)場合。
  - 先にリモートカタログにテーブルを作成する必要がある。
    - 例えば、Spark やpyicebergなどを使用してIcebergテーブルをOpen Catalog上に作成する。
  - リモートカタログにテーブルが存在する状態で、`CREATE ICEBERG TABLE` コマンドを使用する。
    - [CREATE ICEBERG TABLE (Iceberg REST カタログ)](https://docs.snowflake.com/ja/sql-reference/sql/create-iceberg-table-rest)

```sql
-- 対象catalog linked databaseに切り替え
USE DATABASE my_catalog_linked_db;

-- 対象スキーマに切り替え
USE SCHEMA my_namespace;

-- Icebergテーブルの作成
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  first_name STRING,
  last_name STRING,
  amount INT,
  create_date DATE
)
TARGET_FILE_SIZE = '64MB'
PARTITION BY (first_name);
```

#### 遭遇したエラーたち

- 外部カタログがAWS Glue Data Catalogの場合、lowercaseでダブルクォート付きの識別子名だけが許可されてる (テーブル名もカラム名も)
