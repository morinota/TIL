<!-- タイトル: Feature Store調べてたらレイクハウスアーキテクチャと繋がったのでIcebergテーブルフォーマットについて調べた! パーティション戦略編! -->

<!-- 

ブログ構造の検討

- TL;DR
- はじめに: なんでこの記事を書いたの??
- Icebergのパーティショニングの仕組み (Hidden Partitioning) の話
- Icebergのパーティショニング戦略のtips
  - 「どのカラムをどう変換して分割すべきか」をクエリパターンから逆算して設計するのが基本!
- おわりに
- 参考文献

-->

## TL;DR

- Icebergテーブルのパフォーマンスを最大化するための重要な要素の一つに、**パーティショニング(partitioning)戦略**がある。本記事はそれについて調査したもの。
- hoge

## はじめに: なんでこの記事を??

- なぜIcebergテーブルフォーマットを??
  - 要約すると、自分はMLOpsに関心があってFeature Storeの本を読んでたら、オフラインストアの実装にレイクハウスアーキテクチャが採用されることが多いと書いてあったので、その中核技術であるIcebergテーブルフォーマットについて調べている、という感じ。
    - より詳細は、前回の記事([Feature Store調べてたらレイクハウスアーキテクチャと繋がったのでIcebergテーブルフォーマットについて調べた! スキーマ進化編!](https://qiita.com/morinota/items/a670abb84cf5aca480b2))へ!
- なぜIcebergのパーティショニング戦略を??
  - Feature Store (のオフラインストア) がビジネスで価値を発揮するための要件として、**大量or大きな特徴量レコード達に対してなるべく高速 & 安価なクエリ**を実現することが重要。
    - (注意点として、リアルタイムで低レイテンシアクセスできるほど高速、という意味ではないです!その役割はオフラインストアではなくオンラインストアが担うので。ここでは寧ろ、学習用/バッチ推論用に大きなデータセットを作成する際のクエリ性能の話をしてます!)
    - もし学習データセット作成時の**クエリが遅い or 高コストになってしまうと**、データサイエンティストが特徴量の探索やモデルのトレーニングを行う際のフィードバックループが遅くなってしまい、**結果的にモデルの品質向上やプロジェクトの成功に悪影響を与えてしまう可能性も高い**はず。
    - 特にMLプロジェクトの種類によっては、**データサイズの大きい埋め込み表現などのベクトル型の特徴量**を扱うことも多いので、何も気にしてないとクエリ性能が大幅に低下 or コスト爆増の可能性は十分に高いと思われる。
  - そして、**Icebergテーブルのクエリ性能を最大化するための重要な要素の一つに、パーティショニング(partitioning)戦略がある。**
- よって本記事にて、Icebergのパーティショニングの仕組み、パーティショニング戦略のtipsなどを調査した結果をまとめて見てます!

## Icebergのパーティショニングの仕組み (Hidden Partitioning) の話

- Icebergのパーティショニングは、**hidden partitioning**と呼ばれるアプローチを採用している。
  - hidden partitioning = ユーザにpartitionの認識を追わせることなく、クエリパフォーマンスを向上させる**メタデータ駆動型アプローチ**。
    - 背景として、従来のデータレイク(Hiveテーブル形式など)のパーティショニングの仕組みでは、partitioningをユーザに公開し、ストレージレイアウトを理解し、クエリ内でpartition列を明示的に参照することを強制してた。
  - クエリ描く人がpartition keyを意識しなくて良いっぽい...!:thinking:

## Icebergのパーティショニング戦略のtips

「**どのカラムをどう変換して分割すべきか**」を**クエリパターンから逆算**して設計するのが基本!

- 基本的には、「よく使うWhere句(i.e. filter条件)」と「テーブルサイズ」から決める感じ!
- (1) そもそもpartitionすべきかの判断!
  - 全体で1TB未満くらいのテーブルだったら、無理にpartition切らない方がシンプルで良いことも多い。
  - パーティション進化できるので、データサイズの増加に応じて途中からpartition切るのも全然あり...!:thinking:
- (2) 時系列イベントテーブルなら...
  - まずは`day(event_time)`や`hour(event_time)`でpartition切るのが無難。
  - 1日にどれくらいデータ入るか見て、日次で多すぎるなら時間単位に、少なすぎるなら月単位を検討する感じ。
- (3) ユーザ/テナント単位のアクセスが多いなら...
  - 日付 + `bucket(user_id, 16)`みたいな、複合partitionを検討。
  - Nは「1partitionあたりの数百MB〜数GB」くらいに落ち着くように試す。
  - ただ個人的に、この `bucket()` という変換関数はあんまり意味ない気がしてる...!!:thinking:
    - **結局ハッシュに基づいて分割するだけなので、あんまりpartitioning pruningでクエリ性能を向上させるという効果は薄い**っぽい。

## Partition Transform Functions（パーティション変換関数）

Iceberg は、列の値をパーティション値に変換する組み込みの変換関数を提供します。

### Temporal Transforms（時間変換）

- `years(timestamp)` - 年単位でパーティション
- `months(timestamp)` - 月単位でパーティション
- `days(timestamp)` - 日単位でパーティション
- `hours(timestamp)` - 時間単位でパーティション

### Bucketing and Truncation（バケット化と切り捨て）

- `bucket(N, col)` - N 個のバケットにハッシュパーティション
- `truncate(width, col)` - 指定された幅に文字列または数値を切り捨て
- `identity(col)` - 変換なし（そのまま使用）

これらの変換は、パーティション値が書き込み時に導出され、メタデータにのみ保存され、データファイルに重複して保存されないことを保証します。

### 多次元パーティショニングの例

```sql
CREATE TABLE user_activity (
   user_id BIGINT,
   session_id STRING,
   activity_time TIMESTAMP,
   region STRING,
   activity_data STRING
) PARTITIONED BY (
   days(activity_time),
   truncate(2, region),
   bucket(user_id, 32)
);
```

この戦略により、不要なデータをスキャンすることなく、時間範囲、地理的地域、および特定のユーザにわたる効率的なクエリが可能になります。

## Partition Evolution（パーティションの進化）

Hidden Partitioning の重要な利点の一つは、**データを再書き込みすることなくパーティションスキームを進化させる能力**です。

```sql
-- 初期: 日単位のパーティショニング
CREATE TABLE metrics (
  metric_id BIGINT,
  timestamp TIMESTAMP,
  value DOUBLE
)
PARTITIONED BY (days(timestamp));

-- 後で: 時間単位のパーティショニングに進化
ALTER TABLE metrics
DROP PARTITION FIELD days(timestamp);

ALTER TABLE metrics
ADD PARTITION FIELD hours(timestamp);
```

### Version-Based Partition Specs

Iceberg は、各パーティション仕様に一意の ID を割り当て、各データファイルにどの仕様が使用されたかを追跡します。

**Netflixの事例では、パーティション進化を使用して、マルチペタバイトテーブルのパーティションスキームをダウンタイムや重大なパフォーマンスへの影響なしに移行できたそうです!** すごい...!!

### パフォーマンスへの影響

- 古いデータは日単位のパーティションのまま
- 新しいデータの書き込みは時間単位のパーティショニングを使用
- クエリは自動的に両方のスキームを活用
- データの書き換えは不要（Zero-Copy Evolution）

## パフォーマンス最適化のベストプラクティス

### 1. 適切なパーティション列の選択

**低カーディナリティの列を選び、比較的一様な分布を持つもの**を選択します。

推奨される列の例：

- 時系列データ: `days(timestamp)`, `hours(timestamp)`
- カテゴリカルデータ: `region`, `product_category`, `customer_segment`
- 高カーディナリティ列の場合: `bucket(user_id, N)`

避けるべき列：

- `user_id`, `transaction_id` などの高カーディナリティ列（バケット化を使わない場合）

### 2. 過剰なパーティショニングを避ける

**推奨されるパーティションサイズ**：

- 最低: パーティションごとに 1GB - 10GB
- 理想: パーティションごとに 10GB - 100GB
- 個々のファイルサイズ: 100MB 以上

**テーブルサイズの考慮**：

- テーブルの全体的なファイルサイズは、パーティションを利用する前に少なくとも 1TB であるべき
- 各追加次元は、パーティション数を乗算的に増加させる
- 例: 365日 × 128バケット = 46,720パーティション
  - 各パーティションに128MBのファイル1つを持つには、6TBのデータが必要
  - 低ボリュームテーブルでは数千の小さなファイルが生成され、メタデータオーバーヘッドが増加

### 3. 時間ベースのパーティショニング進化戦略

データ量に応じて、パーティションの粒度を調整します。

```sql
-- 戦略例:
-- 0-90日: 時間単位のパーティション（最近のデータ、高いクエリ頻度）
-- 91-365日: 日次パーティション（中程度の年齢のデータ）
-- 365日以上: 月次パーティション（アーカイブデータ、まれなクエリ）

-- 初期: 時間単位
PARTITIONED BY (hours(timestamp));

-- 90日後: 日次パーティショニングに進化
ALTER TABLE metrics ADD PARTITION FIELD days(timestamp);
ALTER TABLE metrics DROP PARTITION FIELD hours(timestamp);
```

### 4. ファイル管理とコンパクション

**Small Files Problem（小ファイル問題）**：

Iceberg は、データセットが変更されるたびに新しいメタデータとデータファイルを生成します。これにより、多数の小さなファイルが増殖し、時間の経過とともにパフォーマンスが低下します。

#### 問題の検出

```sql
-- 100MB 未満のファイルを特定
SELECT COUNT(*) as small_files
FROM "catalog"."schema"."table$files"
WHERE file_size_in_bytes < 100000000;
```

#### コンパクションの実行

```sql
-- Trino の optimize コマンドで小さなファイルを統合
ALTER TABLE catalog.schema.table
EXECUTE optimize(file_size_threshold => '100MB');
```

#### コンパクションのベストプラクティス

- 頻繁にクエリされるテーブルを優先する
- 特定のパーティションを圧縮するためにフィルターを使用する
- クエリワークロードに影響を与えないように、別のクラスターで実行することを検討
- 時間ベースのパーティショニングでは、データファイルがもはや変更されなくなった時点で圧縮を停止

### 5. スナップショット管理

時間が経つにつれて、Iceberg は古いスナップショットと関連するメタデータを蓄積します。これらは Time Travel 機能を可能にしますが、ストレージを消費し、クエリ計画のパフォーマンスに影響を与える可能性があります。

#### スナップショットの期限切れ

```sql
-- 7日より古いスナップショットを削除
ALTER TABLE catalog.schema.table
EXECUTE expire_snapshots(retention_threshold => '7d');
```

#### 孤立したファイルの削除

```sql
-- どのスナップショットにも参照されなくなったデータファイルを削除
ALTER TABLE catalog.schema.table
EXECUTE remove_orphan_files(retention_threshold => '3d');
```

#### マニフェストの再書き込み

```sql
-- マニフェストファイルを統合してクエリ計画の効率を向上
ALTER TABLE catalog.schema.table
EXECUTE rewrite_manifests;
```

これにより、クエリエンジンが読み取る必要のあるマニフェストファイルの数が減少し、クエリ計画の効率が向上します。

## 2025年のパフォーマンス向上（Iceberg 1.5+）

### Position Delete Performance (Iceberg 1.5)

Iceberg 1.5 では、行レベルの削除を持つテーブルのパフォーマンスを劇的に改善する最適化されたポジション削除処理が導入されました。

```sql
-- Position Deletes がパーティション対応になり、より効率的に
DELETE FROM events
WHERE event_timestamp = '2024-06-15'
  AND event_type = 'duplicate';
```

以前は、Position Deletes がすべてのパーティションにわたってクエリパフォーマンスに影響を与える可能性がありました。1.5 の最適化により、削除ファイルがパーティションを認識するようになり、削除を含まない全パーティションをスキップできるようになります。

### Advanced Statistics Collection (Iceberg 1.6+)

Iceberg 1.6 では、統計収集が強化されました：

- より良い述語プッシュダウンのための列レベルの NULL カウント
- HyperLogLog スケッチを使用した異なる値の推定
- 高カーディナリティ列のための Bloom フィルター（オプション）

```sql
CREATE TABLE enhanced_events (
  user_id BIGINT,
  event_data STRING,
  event_timestamp TIMESTAMP
)
PARTITIONED BY (days(event_timestamp))
TBLPROPERTIES (
  'write.metadata.metrics.column.user_id'='full',
  'write.metadata.metrics.column.event_data'='counts'
);
```

### REST Catalog Standard

REST カタログは、2025 年のデプロイメントに推奨されるカタログ実装となりました。Hive Metastore や AWS Glue とは異なり、REST カタログは以下を提供します：

- すべての Iceberg 実装にわたる標準化された API
- 高同時実行ワークロードに対するより良いスケーラビリティ
- テーブル間の原子的操作のためのマルチテーブルトランザクション
- セキュアなデータアクセスのための組み込みの資格情報販売

## ストリーミングエコシステムとの統合

### Apache Kafka with Iceberg

ストリーミング書き込みには、慎重なパーティション戦略の設計が必要です。

```sql
-- ストリーミングデータに最適なパーティショニング
CREATE TABLE kafka_events (
    event_key STRING,
    event_value STRING,
    event_timestamp TIMESTAMP,
    kafka_partition INT,
    kafka_offset BIGINT
) PARTITIONED BY (hours(event_timestamp));
```

ベストプラクティス：

- ストリーミングデータには時間単位のパーティショニングを使用
- ストリーミングジョブで自動圧縮を有効にする
- コミット前にデータをバッファリングするように設定
- パーティションの基数を監視して、過剰なパーティショニングを避ける

### Flink and Spark Streaming

```python
# Spark Structured Streaming to Iceberg
df.writeStream \
  .format("iceberg") \
  .outputMode("append") \
  .option("fanout-enabled", "true") \
  .option("target-file-size-bytes", "536870912") \
  .partitionBy("days(event_timestamp)") \
  .toTable("events")
```

`fanout-enabled` オプションは、複数のタスクが同時に同じパーティションに書き込む際のライター競合を防ぎます。ファナウトモードがない場合、パーティションへの同時書き込みを行うライターは、同じマニフェストファイルを更新するために競争し、リトライやスループットの低下を引き起こします。

## パフォーマンス調整チェックリスト

### 1. 適切なパーティションの粒度を選択

- 高ボリュームテーブル: 時間単位またはバケットベース
- 中ボリューム: 日単位
- 低ボリューム: 月単位またはパーティショニングなし

### 2. ファイルサイズを監視

- 目標: ファイルあたり 128MB - 1GB
- 100MB 未満のファイルには圧縮を使用
- 必要に応じて大きなファイルを分割

### 3. パーティションの進化を活用

- 粗い粒度から始め、データが増えるにつれて洗練させる
- 古いデータをより粗い粒度のパーティションにアーカイブ

### 4. メタデータキャッシングを有効化

- マニフェストファイルのカタログキャッシングを設定
- クエリ計画のオーバーヘッドを削減

### 5. カラム統計を使用

- 統計収集が有効であることを確認
- パーティションレベルのフィルタリングを超えたファイルを削除

### 6. クエリパターンをテスト

- クエリ実行計画を分析
- パーティションとファイルの削除効果を確認

## パフォーマンス監視

**測定しないものは改善できません。**

### ファイル統計

```sql
-- ファイルの数とサイズを監視
SELECT
  COUNT(*) as file_count,
  AVG(file_size_in_bytes) / 1024 / 1024 as avg_size_mb,
  MIN(file_size_in_bytes) / 1024 / 1024 as min_size_mb,
  MAX(file_size_in_bytes) / 1024 / 1024 as max_size_mb
FROM "catalog"."schema"."table$files";
```

### Table Health Indicators

Iceberg のメタデータテーブルを使用してテーブルの状態を理解します：

- `$files` – データファイルのサイズと数を表示
- `$manifests` – マニフェストファイルの健康状態と統合の必要性を追跡
- `$snapshots` – スナップショットの蓄積を監視し、期限切れスケジュールを計画

### クエリパフォーマンスメトリック

- クエリの実行時間を追跡
- スキャンされたデータと処理された行を監視
- 劣化パターン（時間の経過とともに操作が徐々に遅くなること）を探し、メンテナンスが必要であることを示す

## (補足) すべてのデータが Iceberg にある必要があるわけではない

調べていて興味深かったポイントとして、「全部のデータをIcebergに移行しなくてもいい」という話がありました!

データの集中化は万能ではありません。以下のようなデータセットを優先的にIcebergに移行することを検討すると良いそうです:

- **ビジネスにとって重要**なデータ
- **異なるユースケースで複数のユーザーによって頻繁にアクセスされる**データ
- **Icebergの高度な機能から最も利益を得ることができる**データ

パフォーマンスの向上が必要でない場合はデータをフェデレートのままにしておき、**移行が新しいプロジェクトの障害にならないように**しましょう。

段階的なアプローチが推奨されています:

1. Trinoなどのクエリツールを使用して、デフォルトで分散データにアクセス
2. そこから、高価値データセットを特定して移動

個人的には、Feature Storeの文脈では、モデル学習や推論で頻繁にアクセスする特徴量テーブルは優先的にIcebergに移行する価値がありそうだと思いました! :thinking:

## おわりに

## 参考資料

- [What is Hidden Partitioning in Apache Iceberg?](https://www.stackgazer.com/p/what-is-hidden-partitioning-in-apache-iceberg)
- [Iceberg Partitioning and Performance Optimization (Conduktor)](https://conduktor.io/glossary/iceberg-partitioning-and-performance-optimization)
- [Best Practices for Optimizing Apache Iceberg Performance (Starburst)](https://www.starburst.io/blog/best-practices-for-optimizing-apache-iceberg-performance/)
- [Iceberg Partitioning vs. Hive Partitioning](https://olake.io/iceberg/hive-partitioning-vs-iceberg-partitioning/)
