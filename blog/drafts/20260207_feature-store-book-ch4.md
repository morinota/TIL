O'Reilly Feature Store Book 第4章: Feature Storeの基礎

## 1. 元記事情報

- **タイトル(原文)**: CHAPTER 4: Feature Stores
- **書籍**: O'Reilly Feature Store for Machine Learning (Part 2の開始)
- **種類**: 技術書籍の章
- **元ファイル**: [machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_4.md](../machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_4.md)

---

## 2. 概要

Part 2の開始章。Feature Storeの歴史、構造(Anatomy)、必要性、Feature Group、Feature View、データモデリングなど、Feature Storeの基礎を包括的に解説する。クレジットカード詐欺予測のリアルタイムMLシステムを例に、スター・スキーマやスノーフレーク・スキーマによるデータモデリング、Point-in-Time Correct Joinなどの実践的なトピックを扱う。

## 3. 背景・課題

### 3.1. データ管理の困難さ

**データ管理はAIシステムの構築と運用において最も困難な側面の1つ**

第3章の空気質予測システムでは、Feature Storeが以下の役割を果たした:

- Feature Pipelineの出力を保存
- Training Pipelineにトレーニングデータを提供
- Batch Inference Pipelineに推論データを提供

### 3.2. Feature Storeの定義

**Feature Store**: トレーニングと推論の両方のための特徴を保存、管理、提供する中央データプラットフォーム

**主な機能**:

- トレーニングと推論で使用される特徴間の一貫性を確保
- FTIパイプラインを接続するための共有データレイヤーと明確なAPIを提供
- モジュラーAIシステムの構築を可能にする

### 3.3. 本章で答える問いかけ

1. Feature Storeはどのような問題を解決し、いつ必要か?
2. Feature Groupとは何か、どのようにデータを保存し、書き込むのか?
3. Feature Groupのデータモデルをどのように設計するか?
4. 多くのFeature Groupに分散した特徴データをトレーニング/推論のためにどのように読み取るか?

### 3.4. 動機付けの例: クレジットカード詐欺予測

**MLシステムカード**:

- **予測問題**: クレジットカード取引のリアルタイム詐欺予測
- **データソース**: データウェアハウス + イベントストリーミングプラットフォーム(Kafka/Kinesis)
- **予測の消費**: リアルタイムAPI

**Feature Store構築の4ステップ**:

1. エンティティとその特徴を特定
2. エンティティを特徴のテーブル(Feature Group)に整理し、Feature Group間の関係を特定
3. Feature Viewで異なるFeature Groupからモデルのための特徴を選択
4. Feature Viewでモデルトレーニングとバッチ/オンライン推論のためのデータを取得

## 4. 主要なポイント

### 4.1. Feature Storeの歴史

#### 4.1.1. Uber Michelangelo(最初のFeature Store)

- **Feature Store(Palette)** + Model Registry + Model Serving
- **DSL(Domain-Specific Language)**によるFeature Pipeline定義
  - 特徴定義をSparkプログラムにトランスパイル
  - スケジュール実行(毎時/毎日)

#### 4.1.2. Hopsworks(最初のオープンソースFeature Store、2018年末)

- **APIベースのFeature Store**(初)
- 外部パイプラインがDataFrame APIで特徴データを読み書き
- 組み込みパイプラインオーケストレーションなし
- 異なるフレームワーク/言語でパイプライン記述可能(Flink、PySpark、Pandas)

#### 4.1.3. Feast(2019年末)

- Hopsworksと同じAPIベースアーキテクチャを採用

#### 4.1.4. 現在の状況

- **APIベース**: GCP、AWS、Databricks、Hopsworks、Feast
- **DSLベース**: Tecton(最も人気)

**用語**:

- **Feature Platform**: 管理されたFeature Pipelineをサポートする Feature Store
- **AI Lakehouse**: レイクハウステーブルをOffline Storeとして使用し、統合Online Storeを持つFeature Store

### 4.2. Feature Storeの構造(Anatomy)

**Feature Store = 特徴データを生成し保存する工場**

#### 4.2.1. 主な入出力

**入力**:

- Feature Pipeline: 新規/履歴データ → MIT(Model-Independent Transformations)で再利用可能な特徴データに変換
- Feature Storeは**mutableな特徴データ**を保存

**出力**:

- **Training Data**: Point-in-Time Consistent Snapshot + MDT(Model-Dependent Transformations)
- **Batch Inference Data**: 特徴データ + MDT
- **Online Inference Data**: 低レイテンシアクセス

#### 4.2.2. ラベルの扱い

教師ありMLの場合、**ラベルもFeature Storeに保存**:

- トレーニング/推論データ作成まで特徴データとして扱われる
- Feature Storeはどの列が特徴でどの列がラベルかを認識

### 4.3. Feature Storeが必要な7つの理由

#### 4.3.1. リアルタイムMLシステムにおけるコンテキストと履歴

リアルタイムMLシステムは以下を必要とする:

- **リクエスト時パラメータ**(例: ユーザーID)
- **事前計算された特徴**(例: 過去30日間の平均支出)

Feature StoreのOnline Store(行指向ストア)が低レイテンシで事前計算特徴を提供。

#### 4.3.2. 時系列データのためのPoint-in-Time Correct Join

**Data Leakage(データリーケージ)**の防止:

- 訓練データ作成時に、**ラベルのタイムスタンプ以降の特徴を使用してしまう問題**
- Feature Storeは**Point-in-Time Correct Join**を提供:
  - 各ラベルのタイムスタンプ時点で利用可能だった特徴のみを使用
  - 時系列データの整合性を保証

#### 4.3.3. FTIパイプラインアーキテクチャによるコラボレーション改善

Feature Storeが共有データレイヤーとして機能:

- データエンジニア: Feature Pipeline
- データサイエンティスト: Training Pipeline
- MLエンジニア/IT運用: Inference Pipeline

各チームが独立して作業可能。

#### 4.3.4. MLシステムのガバナンス

Feature Storeが以下を提供:

- **メタデータ管理**(特徴の説明、データ型、統計情報)
- **リネージ**(特徴の生成元、使用モデル)
- **アクセス制御**
- **監査ログ**

#### 4.3.5. AI資産の発見と再利用

Feature Storeが特徴カタログとして機能:

- 既存特徴の検索
- 特徴の再利用によるTime-to-Marketの短縮

#### 4.3.6. Offline-Online Feature Skewの排除

**Training-Serving Skew**の防止:

- Offline Store(訓練用)とOnline Store(推論用)で同じ特徴データを保証
- Feature Storeが両ストアへの書き込みを管理

#### 4.3.7. AIのためのデータを単一プラットフォームに集中化

Feature Storeが以下を統合:

- **Offline Store**(列指向): 訓練データ、バッチ推論
- **Online Store**(行指向): リアルタイム推論
- **Vector Index**: ベクトル埋め込み(RAG、類似検索)

### 4.4. Feature Group

**Feature Group**: 特徴のテーブル(論理的なグループ)

#### 4.4.1. 特徴の未変換データを保存

Feature GroupはMIT適用後の「再利用可能な特徴」を保存:

- MDT(正規化、エンコーディング)は**適用しない**
- 元の値(例: $74,580)を保存 → EDA(探索的データ分析)が容易

#### 4.4.2. Feature GroupへのWrite操作

**3つのCommitタイプ**:

1. **Append**: 新しい行を追加
2. **Update**: 既存の行を更新
3. **Delete**: 行を削除

**Upsert(Update + Insert)**:

- Primary Keyが存在 → Update
- Primary Keyが存在しない → Insert

#### 4.4.3. 特徴の新鮮さ(Feature Freshness)

**Feature Freshness**: 特徴が最後に更新されてからの最大許容時間

- バッチFeature Pipeline: 毎日更新 → 24時間の新鮮さ
- ストリーミングFeature Pipeline: 数秒〜数分の新鮮さ

#### 4.4.4. データ検証(Data Validation)

Feature Pipelineでのデータ品質保証:

- スキーマ検証
- 統計的異常検知
- カスタム検証ルール

### 4.5. データモデリング

#### 4.5.1. 次元モデリング(Dimension Modeling)

**データウェアハウスの標準的手法**:

- **Fact Table(事実テーブル)**: トランザクション、イベント
- **Dimension Table(次元テーブル)**: コンテキスト情報

**Feature Storeでは**:

- **ラベル = Fact**(例: 詐欺フラグ)
- **特徴 = Dimension**(例: ユーザー情報、マーチャント情報)

#### 4.5.2. SCD(Slowly Changing Dimensions)

**Type 1**: 上書き(履歴なし)
**Type 2**: 履歴保持(バージョニング)

Feature Storeは**Type 2 SCD**をサポート:

- `valid_from`、`valid_to`タイムスタンプ
- Point-in-Time Correct Joinで適切なバージョンを選択

#### 4.5.3. スター・スキーマ(Star Schema)

**構造**:

- 中心にFact Table
- 周囲にDimension Table
- Fact TableからDimension Tableへの外部キー

**例: クレジットカード詐欺予測**:

- **Fact**: `transactions`(取引)
- **Dimensions**: `credit_cards`、`users`、`merchants`

**利点**:

- シンプルな構造
- クエリが高速
- 理解しやすい

#### 4.5.4. スノーフレーク・スキーマ(Snowflake Schema)

**構造**:

- スター・スキーマの正規化版
- Dimension Tableをさらに分解

**例**:

- `users` → `users` + `user_addresses`
- `merchants` → `merchants` + `merchant_categories`

**利点**:

- ストレージ効率
- 更新の一貫性

**欠点**:

- Joinが増える → クエリが複雑
- パフォーマンス低下の可能性

### 4.6. 推論のためのFeature Storeデータモデル

#### 4.6.1. Online Inference

**Online Store(行指向)**:

- Primary Keyでの高速ルックアップ
- 低レイテンシ(ミリ秒単位)
- リクエスト時パラメータ(例: `card_id`) → 特徴取得

**データモデル**:

- Fact Tableは不要(リアルタイム推論ではトランザクションはまだ発生していない)
- Dimension Tablesのみ(ユーザー、カード、マーチャント情報)

#### 4.6.2. Batch Inference

**Offline Store(列指向)**:

- 大量データの一括処理
- スター・スキーマまたはスノーフレーク・スキーマ

**処理フロー**:

1. 新しいトランザクションデータ(Fact)を取得
2. Dimension Tablesから特徴をJoin
3. バッチ予測実行

### 4.7. Feature View

**Feature View**: モデルが使用する特徴の選択とクエリ定義

#### 4.7.1. 機能

- 異なるFeature Groupから特徴を選択
- Join条件を定義
- ラベルを指定(訓練用)
- トレーニング/推論データの一貫性を保証

#### 4.7.2. Point-in-Time Correct Training Data

**問題**:

- 単純なJoinでは、ラベルのタイムスタンプ時点で利用不可能な特徴を含む可能性

**解決策**:

Feature ViewのPoint-in-Time Correct Join:

1. ラベルの`event_time`を基準
2. 各Feature Groupから`event_time`以前の最新の特徴を取得
3. Data Leakageを防止

**例**:

```
Label: 2024-01-15 10:00の詐欺フラグ
→ User特徴: 2024-01-15 09:55の最新値を使用
→ Card特徴: 2024-01-14 23:00の最新値を使用
```

#### 4.7.3. Online Inferenceとの整合性

Feature Viewは訓練と推論の両方で使用:

- **訓練時**: Point-in-Time Correct Join
- **推論時**: 最新特徴を取得

同じFeature Viewを使用 → Training-Serving Skewを防止

## 5. 技術的な詳細

### 5.1. Feature Storeの3層ストレージ

1. **Offline Store(列指向)**: Apache Hudi、Delta Lake、Iceberg
2. **Online Store(行指向)**: Redis、DynamoDB、RocksDB
3. **Vector Index**: Pinecone、Milvus、Weaviate

### 5.2. Feature Groupのスキーマ

```python
# 例: Transactionsテーブル
Feature Group: transactions
Primary Key: transaction_id
Event Time: transaction_time
Features:
  - transaction_id (string)
  - card_id (string)         # FK to credit_cards
  - merchant_id (string)     # FK to merchants
  - amount (float)
  - transaction_time (timestamp)
  - is_fraud (boolean)       # Label
```

### 5.3. Point-in-Time Correct Joinのアルゴリズム

1. ラベルのタイムスタンプ`t_label`を取得
2. 各Feature Groupで`event_time <= t_label`の最新レコードを選択
3. Primary Key/Foreign Keyでレコードを結合

### 5.4. Feature Freshnessの監視

Feature Storeが各Feature Groupの最終更新時刻を追跡:

- 現在時刻 - 最終更新時刻 > 許容時間 → アラート
- Feature Pipeline障害の早期検知

## 6. 学びと考察

### 6.1. 学んだこと

1. **Feature Storeは単なるデータ保存場所ではない**: トレーニング-推論の一貫性、Point-in-Time Correct Join、ガバナンスなど、多くの問題を解決する統合プラットフォーム。

2. **APIベース vs DSLベースの歴史**: Uber Michelangelo(DSL) → Hopsworks(API) → 現在は両方が共存。APIベースが主流化している背景には、フレームワーク/言語の柔軟性がある。

3. **ラベルもFeature Storeに保存**: 教師ありMLのラベルを特徴データとして扱うことで、データ管理が統一される。Offline Storeにのみ保存すればコスト効率的。

4. **Point-in-Time Correct Joinの重要性**: Data Leakageは時系列データで非常に起こりやすい。Feature Storeがこれを自動的に防ぐ機能は極めて価値が高い。

5. **データモデリングの2つのアプローチ**: スター・スキーマ(シンプル、高速)とスノーフレーク・スキーマ(正規化、ストレージ効率)。用途に応じて選択する。

### 6.2. 自分の考察

#### 6.2.1. Feature Storeの中心性の再確認

第1章で「Feature StoreはFTIパイプラインの中心」と学んだが、本章でその具体的な理由が明確になった:

- 共有データレイヤー(チーム間コラボレーション)
- 一貫性の保証(Training-Serving Skew防止)
- ガバナンス(メタデータ、リネージ、アクセス制御)
- 時系列データの整合性(Point-in-Time Correct Join)

Feature Storeは「データの保存場所」ではなく、「AIシステムのデータガバナンスプラットフォーム」として理解すべき。

#### 6.2.2. APIベースの勝利?

DSLベース(Tecton)は依然として人気があるものの、GCP、AWS、Databricksという主要クラウドプロバイダーがAPIベースを採用している事実は重要。

**APIベースの利点**:

- フレームワーク非依存(Flink、Spark、Pandas、Polars、DuckDB)
- 既存パイプラインオーケストレーションツールとの統合(Airflow、Prefect、Dagster)
- 学習曲線が低い(既存のDataFrame APIを使用)

**DSLベースの利点**:

- 宣言的な特徴定義
- 自動最適化
- 運用の簡素化

個人的には、APIベースの柔軟性を重視したい。

#### 6.2.3. Point-in-Time Correct Joinの実装難易度

Point-in-Time Correct Joinは概念的にはシンプルだが、実装は非常に複雑:

- 大量の時系列データに対する効率的なクエリ
- 複数Feature Groupのタイムスタンプ整合性
- パフォーマンス最適化

Feature Storeがこれを提供することで、データサイエンティストはData Leakageの心配なくモデル開発に集中できる。**Feature Storeの最大の価値の1つ**と感じる。

#### 6.2.4. ラベルの保存場所に関する考察

第2章で「ラベルの保存場所」について疑問を持っていたが、本章で明確になった:

- ラベルはFeature Storeに保存(Offline Storeのみ)
- 特徴データとして扱われる(トレーニング/推論データ作成時にラベルとして識別)
- Online Storeには保存しない(推論時に不要、コスト削減)

この設計は合理的。ラベルと特徴を統一的に管理することで、データパイプラインが簡素化される。

#### 6.2.5. Feature Freshnessの重要性

Feature Freshnessは「特徴が古すぎる」問題を定量化する指標。これを監視することで:

- Feature Pipeline障害の早期検知
- モデル性能劣化の予防
- SLO(Service Level Objective)の設定

実務では、Feature Freshnessを明示的に定義し、監視アラートを設定すべき。

#### 6.2.6. スター vs スノーフレーク

データウェアハウスの世界では長年の議論だが、Feature Storeの文脈では:

- **スター・スキーマ推奨**: シンプル、高速、理解しやすい
- **スノーフレーク・スキーマは必要に応じて**: ストレージコスト削減、更新頻度が高いDimensionの正規化

個人的には、まずスター・スキーマで設計し、パフォーマンス/コストの問題が顕在化してからスノーフレーク化を検討するアプローチが良いと考える。

#### 6.2.7. Feature Groupの粒度設計

Feature Groupをどの粒度で分割すべきか:

- **エンティティごと**: ユーザー、カード、マーチャント
- **更新頻度ごと**: リアルタイム更新、日次更新、週次更新
- **データソースごと**: Kafka、DWH、外部API

複数の軸を考慮する必要があり、正解はケースバイケース。スター・スキーマのFact/Dimensionの考え方が指針になる。

#### 6.2.8. Feature Storeなしのリアルタイム推論の困難さ

Feature Storeがない場合、リアルタイム推論は以下が必要:

1. リクエスト時パラメータから特徴を計算(オンデマンド)
2. 事前計算特徴を自前の行指向DBから取得
3. Training-Serving Skewを手動で防ぐ

特に(3)は非常に困難。Feature Storeの価値を実感する。

#### 6.2.9. AI Lakehouseの概念

「レイクハウステーブルをOffline Storeとして使用」という定義は興味深い。

従来: Feature Store + Data Lakehouse(別々)
現在: AI Lakehouse(統合)

DatabricksやHopsworksがこの方向に進んでいる。データプラットフォームの統合化は、運用複雑性を減らす上で重要。

#### 6.2.10. Feature Viewの抽象化レベル

Feature Viewは「モデルが使用する特徴の選択」を抽象化:

- データサイエンティスト: どの特徴を使うか決める
- Feature Store: Point-in-Time Correct Join、Training-Serving Skew防止を自動処理

この抽象化により、データサイエンティストはビジネスロジック(どの特徴が予測に有用か)に集中できる。

## 7. まとめ

本章はFeature Storeの包括的な入門。歴史、構造、必要性、Feature Group、Feature View、データモデリングなど、Feature Storeを理解するために必要な基礎概念を網羅している。

**重要な教訓**:

- Feature StoreはAIシステムのデータガバナンスプラットフォーム
- Point-in-Time Correct JoinによるData Leakage防止
- Training-Serving Skew防止による一貫性保証
- スター・スキーマ/スノーフレーク・スキーマによるデータモデリング
- Offline/Online/Vectorの3層ストレージ

## 8. 演習

### 演習1: 平均マーチャント支出/月の特徴

新しい特徴「月ごとの平均マーチャント支出」を計算するFeature Pipelineを設計:

- **入力**: `transactions`テーブル
- **出力**: `merchants`テーブルに新しい列`avg_monthly_spend`
- **バッチ/ストリーミング**: バッチ(月次集計)
- **データモデル**: `merchants` Feature Groupに追加

### 演習2: クレジットカード生涯支出の合計

- `credit_cards` Feature Groupに`lifetime_spend`列を追加
- ストリーミングFeature Pipelineで`transactions`から集計

### 演習3: デバイスIDの追加

新しいデバイスIDが利用可能になった場合:

- **データモデル更新**:
  - `transactions`テーブルに`device_id`列を追加
  - 新しいFeature Group `devices`を作成(デバイス情報)
- **新しい特徴**:
  - デバイスごとの取引回数
  - デバイスごとの平均取引額
  - デバイスの最終使用日時

## 9. 参考リンク

- [元ファイル](../machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_4.md)
- [Uber Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/)
- [Hopsworks](https://www.hopsworks.ai/)
- [Feast](https://feast.dev/)
- [Tecton](https://www.tecton.ai/)

## 10. 次に読むべき章

- **第5章**: Hopsworks Feature Storeの詳細(APIベースFeature Storeの代表例)
- **第6章**: Model-Independent Transformations(MIT)の詳細
- **第7章**: Model-Dependent/On-Demand Transformationsの詳細
