## refs:

- [SnowflakeからGlue Data Catalogを使ってIcebergテーブルにアクセスしてみる](https://qiita.com/Himeka_Kawaguchi/items/00f41e6e9f2ddf942c0a)
- [Snowflake と Glue Data Catalog をカタログ統合し自動リフレッシュの動作を確認する](https://dev.classmethod.jp/articles/snowflake-catalog-integration-with-glue-data-catalog-and-auto-refresh/)

## これは何??

- Sagemaker Feature Storeのオフラインストアに保存されている特徴量データに、Snowflakeから参照可能にする方法について調べたメモ。
- できるはずという認識は元々ある。
  - Glue Data Catalogで管理されるS3上のテーブルデータを、Snowflakeから参照する仕組みはすでに存在してて。ブログもある。
  - そして、Sagemaker Feature Storeのオフラインストアは、Iceberg形式にしろGlue Table形式にしろ、Glue Data Catalogで管理されるS3上のテーブルデータとして保存されてる。
  - じゃあできるはずだよね...!:thinking:




