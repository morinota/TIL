<!-- タイトル: Feature Store調べてたらレイクハウスアーキテクチャと繋がったのでIcebergテーブルフォーマットについて調べた! パーティション戦略編! -->

## はじめに: なんでこの記事を書いたの??

Icebergテーブルフォーマットについて調べた経緯については前回の記事([Feature Store調べてたらレイクハウスアーキテクチャと繋がったのでIcebergテーブルフォーマットについて調べた! スキーマ進化編!](https://qiita.com/morinota/items/a670abb84cf5aca480b2))で書いたのですが、本記事はその続きで、**Icebergのパーティション戦略**について調べた内容をまとめたものになります。

Feature Storeのオフラインストアとしてレイクハウスアーキテクチャを採用する場合、大量or大きな特徴量レコード達に対してなるべく高速 & 安価なクエリを実現することが重要です。
(注意点として、リアルタイムで低レイテンシアクセスできるほど高速、という意味ではないです!その役割はオフラインストアではなくオンラインストアが担うので。ここでは寧ろ、学習用/バッチ推論用に大きなデータセットを作成する際のクエリ性能の話をしています。)

もし学習データセット作成時のクエリが遅い or 高コストになってしまうと、データサイエンティストが特徴量の探索やモデルのトレーニングを行う際のフィードバックループが遅くなってしまい、結果的にモデルの品質向上やプロジェクトの成功に悪影響を与えてしまう可能性も高いでしょう。
特にMLプロジェクトの種類によっては、データサイズの大きい埋め込み表現などのベクトル型の特徴量を扱うことも多いので、何も気にしてないとクエリ性能が大幅に低下する可能性は十分に高いです。

Icebergテーブルのクエリ性能を最大化するための重要な要素の一つが、**パーティション戦略**です。
調べてみると、Apache Icebergの**Hidden Partitioning(隠れたパーティショニング)**という機能が、従来のHiveのパーティショニングと比べて圧倒的に柔軟で、かつパフォーマンスも良いらしい...!!:thinking:
そこで本記事では、Icebergのパーティショニングの仕組み、最適化戦略、そしてベストプラクティスについて、複数の参考資料を基に整理してみました!

### 参考資料

- [What is Hidden Partitioning in Apache Iceberg?](https://www.stackgazer.com/p/what-is-hidden-partitioning-in-apache-iceberg)
- [Iceberg Partitioning and Performance Optimization (Conduktor)](https://conduktor.io/glossary/iceberg-partitioning-and-performance-optimization)
- [Best Practices for Optimizing Apache Iceberg Performance (Starburst)](https://www.starburst.io/blog/best-practices-for-optimizing-apache-iceberg-performance/)
- [Iceberg Partitioning vs. Hive Partitioning](https://olake.io/iceberg/hive-partitioning-vs-iceberg-partitioning/)

## 本論: Hidden Partitioning とは何か

### 従来のパーティショニングアプローチの課題

まず、Icebergの前に、従来のデータレイクシステム（Hiveなど）のパーティショニングがどんな感じだったかを見てみましょう!

従来の方式では、パーティショニングはディレクトリベースの物理的な組織として実装されます。

```
/table/year=2025/month=04/day=01/data1.parquet
/table/year=2025/month=04/day=02/data2.parquet
/table/year=2025/month=05/day=01/data3.parquet
```

この方式では、**ユーザがクエリ内でパーティション列を明示的に参照する必要**があります。

```sql
-- パーティション列を明示的に指定しないとフルスキャンが発生
SELECT * FROM events
WHERE event_timestamp = '2025-04-01';

-- パーティション列を指定することで、無関係なディレクトリを除外
SELECT * FROM events
WHERE year = 2025 AND month = 4 AND day = 1;
```

この方式の問題点：

- 物理データレイアウトを理解する複雑さがユーザに押し付けられる
- パーティショニングスキームとクエリが密結合してしまう
- パーティション戦略の変更が困難 (i.e. パーティション進化ができない)

### Iceberg の Hidden Partitioning の仕組み

ではIcebergはどうでしょうか? Icebergは、**メタデータ駆動型アプローチ**により、パーティショニングをユーザから抽象化します!

```sql
-- Iceberg のテーブル作成
CREATE TABLE events (
    event_id BIGINT,
    user_id BIGINT,
    event_timestamp TIMESTAMP,
    event_type STRING
) PARTITIONED BY (
    days(event_timestamp),
    bucket(user_id, 16)
);

-- ユーザは元の列に対してクエリを実行するだけ
SELECT * FROM events
WHERE event_timestamp >= '2024-01-01' AND user_id = 12345;
```

**Iceberg のクエリプランナーが自動的に述語をパーティションフィルターに変換**し、関連するデータファイルのみを読み取ります。これにより：

- ユーザはパーティショニングスキームを意識する必要がない
- パーティション戦略の変更がクエリに影響しない
- パフォーマンスは自動的に最適化される

## Iceberg のメタデータアーキテクチャ

Iceberg の Hidden Partitioning は、多層のメタデータアーキテクチャに基づいています。

### 3つの主要コンポーネント

1. **Metadata Files（メタデータファイル）**
   - テーブルスキーマ、パーティション仕様、スナップショット、設定を保存

2. **Manifest Lists（マニフェストリスト）**
   - スナップショットのすべてのマニフェストを追跡
   - 各マニフェストのパーティション値の範囲を含む

3. **Manifest Files（マニフェストファイル）**
   - データファイルの詳細を含む
   - パーティション値や列レベルの統計を含む

このアーキテクチャにより、データが物理的にどのように保存されているかと、論理的にどのように表現されているかを分離できます。

### Multi-Level Filtering Algorithm（多層フィルタリングアルゴリズム）

Iceberg は、読み取るファイルのセットを段階的に絞り込む 3 段階のフィルタリングを実行します。

#### 1. Manifest List Filtering

マニフェストリストに保存されたパーティション値の範囲を使用して、最初のフィルタリングを実行します。

- O(1) のフィルタリング操作（従来の O(n) と比較）
- テーブルサイズに応じた n の増加を回避

#### 2. Manifest-Level Filtering

正確なパーティション値の一致を適用します。

#### 3. Data File Selection

ファイルレベルの統計を使用してさらなるフィルタリングを実行します。

Wang et al.のパフォーマンス研究では、この多層フィルタリングアプローチが、**特定のクエリパターンに対してデータスキャン量を最大95%削減**したことが示されています! すごい効果...!!

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

## 学びと考察

本記事でIcebergのパーティショニング戦略について調べてみて、以下のことを学びました!

### 学んだこと

- **Hidden Partitioningの革新性**: Icebergは、パーティショニングをユーザから完全に抽象化することで、Hiveの根本的な制限を克服しています
  - ユーザは元の列に対してクエリを書くだけで、Icebergが自動的にパーティションフィルターに変換してくれる! これは本当に便利...!!
- **Partition Evolutionの柔軟性**: データを再書き込みすることなくパーティションスキームを変更できることは、プロダクション環境で非常に重要です
  - 例えば、データ量が増えてきたら日次パーティションから時間単位のパーティションに変更する、といった進化が簡単にできる!
  - Netflixの事例では、マルチペタバイトテーブルのパーティションスキームをダウンタイムなしで移行できたらしい...すごい...!!
- **多層最適化の重要性**: パーティショニングだけでなく、ファイル管理、スナップショット管理を組み合わせることで、真のパフォーマンス向上が得られます
  - 小ファイル問題の解決(コンパクション)、古いスナップショットの削除、マニフェストの再書き込みなど、定期的なメンテナンスが重要
- **過剰なパーティショニングのリスク**: パーティション数を増やすことが常に良いとは限らず、各パーティションに十分なデータ量が必要です
  - 推奨: パーティションごとに10GB-100GB、個々のファイルサイズは100MB以上
  - 低ボリュームテーブルで過剰にパーティションを切ると、数千の小さなファイルが生成されメタデータオーバーヘッドが増加する...!

### Feature Storeへの応用を考えてみた

Feature Storeの設計においても、Icebergのパーティション戦略は有効そうです! :thinking:

- **静的特徴量(Static Features)**: `news_id`などのIDでソートされたテーブルとして設計し、範囲クエリを最適化
  - `PARTITIONED BY (truncate(1000, news_id))`のように、IDの範囲でパーティション分割するのが良さそう
- **動的特徴量(Dynamic Features)**: 時間ベースのパーティショニングと`bucket(entity_id, N)`を組み合わせた多次元パーティショニングを活用
  - 例: `PARTITIONED BY (days(event_timestamp), bucket(user_id, 32))`
  - 時間範囲とユーザIDでフィルタリングするクエリを高速化できる!
- **アクセスパターンに応じた進化**: 最初は無難なパーティション設定で始め、クエリパフォーマンスの問題が出てきたらPartition Evolutionで調整
  - 粗い粒度(月次など)から始めて、データが増えるにつれて細かい粒度(日次、時間単位)に進化させる戦略が良さそう

### AWS S3 Tablesとの関係

調べていて気づいたのですが、AWS S3 Tablesは、Icebergのメンテナンス作業(コンパクション、スナップショット管理、孤立ファイル削除など)を自動化するマネージドサービスなんですね! :thinking:

- 定期的なメンテナンスタスクから解放され、パーティション戦略とスキーマ設計に集中できる
- ただし、裏で何が行われているかを理解しておくことで、パフォーマンス低下時の調査が容易になる
- つまり、本記事で学んだIcebergの内部の仕組みを理解しておけば、S3 Tablesをより効果的に使えるということ...!!

## おわりに

本記事では、Apache Icebergのパーティショニング戦略について以下の内容をまとめました!

- Hidden Partitioningとは何か? 従来のHiveとの違いは?
- Icebergのメタデータアーキテクチャと多層フィルタリング
- パーティション変換関数の使い方
- Partition Evolution(パーティション進化)の仕組み
- パフォーマンス最適化のベストプラクティス
- Feature Storeへの応用を考えてみた

Icebergのパーティショニング機能のポイントは以下の通り:

- **Hidden Partitioning**: ユーザはパーティションスキームを意識せず、元の列に対してクエリを書くだけ。Icebergが自動的に最適化してくれる!
- **Partition Evolution**: データを再書き込みすることなく、パーティションスキームを進化させられる。Zero-Copy Evolutionで柔軟な運用が可能!
- **多層フィルタリング**: マニフェストリスト→マニフェスト→データファイルの3段階でフィルタリングし、データスキャン量を最大95%削減できる!
- **適切な粒度の選択**: パーティションごとに10GB-100GB、ファイルあたり100MB以上が推奨。過剰なパーティショニングは逆効果!

研究によると:

- 変換ベースのパーティショニングは、クエリパターンに適切に整合させた場合、従来のアプローチと比較してクエリ実行時間を最大60%削減できる(Novotny et al.)
- 多層フィルタリングアプローチは、特定のクエリパターンに対してデータスキャン量を最大95%削減(Wang et al.)
- 適切に管理されたIcebergは、Hiveに対して10倍のパフォーマンス向上をもたらす(Apache Icebergプロジェクト)

次回は、実際にPyIcebergを使ってパーティショニングを試してみたいと思います! :muscle:

## 参考リンク

- [What is Hidden Partitioning in Apache Iceberg?](https://www.stackgazer.com/p/what-is-hidden-partitioning-in-apache-iceberg)
- [Iceberg Partitioning and Performance Optimization (Conduktor)](https://conduktor.io/glossary/iceberg-partitioning-and-performance-optimization)
- [Best Practices for Optimizing Apache Iceberg Performance (Starburst)](https://www.starburst.io/blog/best-practices-for-optimizing-apache-iceberg-performance/)
- [Apache Iceberg Documentation - Partitioning](https://iceberg.apache.org/docs/latest/partitioning/)
- [Apache Iceberg - Partition Evolution](https://iceberg.apache.org/docs/latest/evolution/#partition-evolution)
