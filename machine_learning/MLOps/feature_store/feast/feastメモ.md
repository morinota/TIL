## refs

- [Feastに入門する](https://qiita.com/f6wbl6/items/a07493db66512ef22234)
- [Feast duckDBのやつ](https://docs.feast.dev/reference/offline-stores/duckdb)
- [機械学習システムのフィーチャ管理基盤、Feastの紹介](https://recruit.gmo.jp/engineer/jisedai/blog/feast_introduction/)

# Feastメモ

## 主要な概念・コンポーネント達

- Entity: 特徴量が関連づけられるキー (ex. ユーザID, 商品ID)
- Data Source: 特徴量の元となるデータが格納されてる場所(ex. parquetファイル, BigQueryテーブルなど)。
- Feature View: 特定のEntityとData Sourceに基づいて定義された特徴量の集合。各Feature Viewには、1つ以上のFeatureが含まれる。Feature Viewには必ずData Sourceが必要。
- Project: Feast内の**最上位の名前空間**。開発者はProject内で1つ以上のFeature Viewを定義する。
  - Projectはインフラレベルで特徴量ストアを**完全に分離**する。**単一のリクエストで、複数のProjectから特徴量を取得することはできない**。
  - 1つの環境(dev, staging, prod)毎に、1つのProject(1つのFeature Store)を作ることを推奨。


## メソッド一覧

- apply: 特徴量の定義を登録
- 
