O'Reilly Feature Store Book 第6章: Model-Independent Transformations(MIT)

## 1. 元記事情報

- **タイトル(原文)**: CHAPTER 6: Model-Independent Transformations
- **書籍**: O'Reilly Feature Store for Machine Learning
- **種類**: 技術書籍の章
- **元ファイル**: [machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_6.md](../machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_6.md)

---

## 2. 概要

Feature Pipelineで実行するモデル非依存の変換(MIT)の実装方法を解説する章。ソースコードのモノレポ構成、DataFrame変換の分類、Pandas/Polars/PySparkの使い分け、Feature Functionのベストプラクティスを扱う。EVAC(抽出・検証・集約・圧縮)変換の具体例として、クレジットカード詐欺予測システムの特徴量を実装する。

## 3. 背景・課題

### 3.1. Feature Pipelineの役割

**Feature Pipeline**: Feature Storeに保存される再利用可能な特徴を生成するためにモデル非依存のデータ変換(MIT)を実行するプログラム

**重要な特性**:

- 作成された特徴データは、**最初のモデルだけでなく、潜在的に多くの異なるモデルで使用される可能性**
- 特徴の再利用 → 高品質な特徴(使用とテストの増加) + ストレージコスト削減 + 開発/運用コスト削減
- **最もコストのかからないFeature Pipelineは、作成する必要がないもの**(既存特徴の再利用)

### 3.2. Model-Independent Transformations(MIT)の定義

**EVAC変換**(Extraction, Validation, Aggregation, Compression):

1. **Extraction(抽出)**: Lagged Features、Binning、Chunking for LLMs
2. **Validation(検証)**: Data Validation(Great Expectations)、Data Cleaning
3. **Aggregation(集約)**: Counts/Sums for Time Windows
4. **Compression(圧縮)**: Vector Embeddings

### 3.3. Production品質の要件

**Notebookを超える必要性**:

- テスト駆動開発(TDD)
- 継続的インテグレーション/デプロイメント(CI/CD)
- テストによる変更への自信
- 自動化されたテスト実行 → 反復速度を遅くしない

LLM(ChatGPT)がUnit Test作成を支援可能。

## 4. 主要なポイント

### 4.1. ソースコード構成(Monorepo)

#### 4.1.1. ディレクトリ構造

```bash
credit_card_fraud_project/
├── notebooks/              # EDA, reports(本番コードではない)
├── requirements.txt        # グローバルpip依存関係
├── project-name/           # パッケージ名
│   ├── pipelines/          # Feature/Training/Inference Pipelines
│   │   ├── features/       # Feature Functions
│   └── tests/
│       ├── feature-tests   # Feature Functionsのユニットテスト
│       └── pipeline-tests  # Pipelineのエンドツーエンドテスト
└── scripts/                # Batch scripts
```

#### 4.1.2. 設計原則

**分離の原則**:

1. **Feature Functions vs Pipeline Programs**: 特徴計算関数とパイプライン実装を分離
2. **Production Code vs EDA**: 本番コードとNotebookを分離
3. **Unit Tests vs E2E Tests**: 特徴テストとパイプラインテストを分離

**Monorepoの利点**:

- FTIパイプライン間の共有コードのためにPythonライブラリを作成/管理する必要がない
- 各MLパイプラインが独自の`requirements.txt`を持てる
- 別々のProduction-qualityデプロイが可能

**Notebookの役割**:

- 本番コードの一部ではない
- EDAによるデータ・予測問題の理解
- 洞察のステークホルダーへの伝達

### 4.2. Feature Pipelineのデータソース

#### 4.2.1. 主なデータソース

1. **Data Warehouse(データウェアハウス)**
2. **Event-Streaming Platform(イベントストリーミングプラットフォーム)**: Kafka、Kinesis
3. **Object Store(オブジェクトストア)**: S3、GCS、Azure Blob
4. **Lakehouse Tables(レイクハウステーブル)**: Delta Lake、Iceberg、Hudi

#### 4.2.2. フレームワークの選択

**データサイズによる選択**:

- **< 1GB**: Pandas
- **10s GBs**: Polars
- **TBs**: Apache Spark、SQL、dbt
- **Streaming**: Feldera(SQL)、Apache Flink、Spark Structured Streaming

### 4.3. DataFrame変換の分類

#### 4.3.1. Row Size-Preserving Transformations(行数保持変換)

**定義**: 行数は変わらず、列を追加/変更/削除

**例**:

- 新しい列の追加: `df['total'] = df['price'] * df['quantity']`
- 列の変換: `df['price_usd'] = df['price_eur'] * exchange_rate`
- 列の削除: `df.drop('unnecessary_col')`
- データ型変換: `df['date'] = pd.to_datetime(df['date'])`

**用途**: Feature Pipeline で最も一般的な変換

#### 4.3.2. Row and Column Size-Reducing Transformations(行列削減変換)

**定義**: 行または列(またはその両方)を削減

**例**:

- **フィルタリング**: `df[df['amount'] > 100]`
- **サンプリング**: `df.sample(frac=0.1)`
- **列選択**: `df[['col1', 'col2']]`
- **重複削除**: `df.drop_duplicates()`
- **Null行削除**: `df.dropna()`

**用途**: データクリーニング、サンプリング

#### 4.3.3. Row/Column Size-Increasing Transformations(行列増加変換)

**定義**: 行または列(またはその両方)を増加

**例**:

- **Pivoting**: カテゴリ列を複数の列に展開

```python
# カテゴリ別の支出を列に展開
df_pivot = df.pivot_table(
    index='cc_num',
    columns='category',
    values='spend',
    aggfunc='sum'
).rename(columns=lambda x: f'spend_{x}')
```

- **Exploding**: 配列列を複数行に展開
- **One-Hot Encoding**: カテゴリを複数のバイナリ列に

**用途**: カテゴリ特徴の展開、配列データの行展開

#### 4.3.4. Join Transformations(Join変換)

**定義**: 複数のDataFrameを結合

**種類**:

- **Inner Join**: 両方に存在する行のみ
- **Left Join**: 左側のすべての行
- **Right Join**: 右側のすべての行
- **Outer Join**: 両方のすべての行

**Point-in-Time Correct Join**: Feature Storeが提供(第4章)

### 4.4. DAG of Feature Functions

#### 4.4.1. Feature Functionsのベストプラクティス

**Apache Hamiltonのアイデア**: 各特徴を独立した関数として定義

**非モジュラー(BAD)**:

```python
def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    if config["region"] == "UK":
        df["holidays"] = is_uk_holiday(df["year"], df["week"])
    else:
        df["holidays"] = is_holiday(df["year"], df["week"])
    df["avg_3wk_spend"] = df["spend"].rolling(3).mean()
    # ...
    return df
```

**モジュラー(GOOD)**:

```python
def avg_3wk_spend(spend: pd.Series) -> pd.Series:
    """3週間の平均支出を計算"""
    return spend.rolling(3).mean()

def acquisition_cost(spend: pd.Series, signups: pd.Series) -> pd.Series:
    """ユーザー獲得コスト = 総支出 / サインアップ数"""
    return spend / signups
```

**メリット**:

- 各特徴の独立したユニットテスト
- 関数が契約(Contract)を強制 → 破壊的変更を検知
- ドキュメント化が容易
- デバッグが容易
- 再利用可能

#### 4.4.2. Lazy DataFrames(Polars)

**Lazy Evaluation**: クエリを即座に実行せず、最適化してから実行

```python
import polars as pl

# Lazy読み込み
df = pl.scan_csv("data.csv")

# 変換をチェーン(まだ実行されない)
result = (df
    .filter(pl.col("amount") > 100)
    .group_by("category")
    .agg(pl.col("amount").sum())
)

# 実行をトリガー
result.collect()
```

**利点**:

- クエリ最適化(不要な列読み込みスキップ、フィルタの先行実行)
- メモリ効率

#### 4.4.3. Vectorized Compute, Multicore, Arrow

**Vectorized Compute**:

- Pandas、Polars、PySparkはベクトル化計算をサポート
- ループより高速

**Multicore**:

- Polars: デフォルトでマルチコア活用
- Pandas: 一部の操作のみ
- PySpark: 分散処理

**Apache Arrow**:

- 異なるDataFrameエンジン間の効率的なデータ転送
- ゼロコピー読み取り
- Pandas ↔ Polars ↔ PySpark の相互運用性

#### 4.4.4. データ型

**基本型**:

- Numerical: int、float、double
- Categorical: string、enum、boolean
- Temporal: date、datetime、timestamp

**複合型**:

- **Array**: リスト、ベクトル埋め込み
- **Struct**: ネストされたフィールド
- **Map**: Key-Valueペア
- **Tensor**: 多次元配列(画像、動画)

**スキーマ**:

- **暗黙的スキーマ**: データから自動推論(Pandas)
- **明示的スキーマ**: 事前定義(PySparkの`StructType`)

明示的スキーマ推奨 → データ品質保証、パフォーマンス向上

### 4.5. クレジットカード詐欺予測の特徴量

#### 4.5.1. Binning(ビニング)

連続値をカテゴリに変換:

```python
def age_bin(age: int) -> str:
    if age < 18:
        return "under_18"
    elif age < 65:
        return "18_to_65"
    else:
        return "over_65"
```

**用途**: 年齢、金額、距離などのグループ化

#### 4.5.2. Mapping Functions(マッピング関数)

値を変換:

```python
def day_of_week(datetime: pd.Timestamp) -> str:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return days[datetime.dayofweek]
```

**用途**: 時間特徴(曜日、時間帯)、カテゴリマッピング

#### 4.5.3. RFM Features(Recency, Frequency, Monetary)

顧客行動の3つの軸:

- **Recency(最近性)**: 最後の取引からの日数
- **Frequency(頻度)**: 期間内の取引回数
- **Monetary(金銭的価値)**: 期間内の総支出額

```python
def rfm_features(transactions_df: pd.DataFrame) -> pd.DataFrame:
    return transactions_df.groupby('customer_id').agg({
        'transaction_date': lambda x: (datetime.now() - x.max()).days,  # Recency
        'transaction_id': 'count',  # Frequency
        'amount': 'sum'  # Monetary
    }).rename(columns={
        'transaction_date': 'recency',
        'transaction_id': 'frequency',
        'amount': 'monetary'
    })
```

**用途**: カスタマーセグメンテーション、詐欺検知

#### 4.5.4. Aggregations(集約)

時間ウィンドウでの集約:

```python
def last_30d_spend(transactions_df: pd.DataFrame) -> pd.DataFrame:
    cutoff_date = datetime.now() - timedelta(days=30)
    return (transactions_df[transactions_df['date'] >= cutoff_date]
        .groupby('card_id')
        .agg({'amount': 'sum'})
        .rename(columns={'amount': 'last_30d_spend'}))
```

**用途**: 移動平均、カウント、最大/最小値

### 4.6. 変換の構成(Composition)

#### 4.6.1. Feature Functionのチェーン

```python
def create_customer_features(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """複数のFeature Functionを組み合わせ"""
    df = add_age_bin(transactions_df)
    df = add_day_of_week(df)
    df = add_rfm_features(df)
    df = add_last_30d_spend(df)
    return df
```

#### 4.6.2. DAG(Directed Acyclic Graph)構造

Feature Function間の依存関係をDAGとして表現:

- 各関数が明確な入力/出力
- 依存関係を追跡可能
- テスタビリティの向上
- 並列実行可能性

## 5. 技術的な詳細

### 5.1. Pandas vs Polars vs PySparkの比較

| 特性 | Pandas | Polars | PySpark |
|------|--------|--------|---------|
| データサイズ | < 1GB | 10s GBs | TBs |
| マルチコア | 一部のみ | デフォルト | 分散処理 |
| Lazy Eval | No | Yes | Yes |
| Arrow互換 | Yes | Yes | Yes |
| 学習曲線 | 低 | 中 | 高 |

### 5.2. Great Expectationsによるデータ検証

```python
import great_expectations as gx

context = gx.get_context()

# Expectation定義
df.expect_column_values_to_not_be_null("card_id")
df.expect_column_values_to_be_between("amount", min_value=0, max_value=10000)
```

### 5.3. 特徴テストの例

```python
def test_avg_3wk_spend():
    # Arrange
    spend = pd.Series([100, 200, 300, 400])

    # Act
    result = avg_3wk_spend(spend)

    # Assert
    assert result[2] == 200  # (100 + 200 + 300) / 3
```

## 6. 学びと考察

### 6.1. 学んだこと

1. **EVAC変換の分類**: 抽出・検証・集約・圧縮という明確な分類により、Feature Pipelineの設計が体系化される。

2. **Monorepoの価値**: FTIパイプライン間の共有コードを簡単に管理できる。Pythonライブラリの作成/管理オーバーヘッドを回避。

3. **Feature Functionsの重要性**: Apache Hamiltonのアイデアに基づく「1特徴 = 1関数」アプローチは、テスタビリティと再利用性を劇的に向上させる。

4. **Pandas vs Polars vs PySparkの使い分け**: データサイズが明確な選択基準。チームのデータエンジニアリング背景も考慮。

5. **Lazy Evaluationの威力**: Polars/PySparkのLazy Evaluationは、クエリ最適化とメモリ効率の両方を実現。

### 6.2. 自分の考察

#### 6.2.1. 「最もコストのかからないFeature Pipelineは作成しないもの」の深さ

この一文は、Feature Storeの本質を端的に表している。特徴の再利用を前提とすることで:

- 開発コスト削減
- 品質向上(使用回数 ∝ テスト回数)
- ストレージコスト削減(重複計算の排除)

Feature Catalogによる発見可能性が、この再利用を実現する鍵。

#### 6.2.2. Notebookの位置づけ

「NotebookはProduction codeではない」という明確な線引きが重要。Notebookの役割:

- EDA(探索的データ分析)
- 洞察の伝達
- プロトタイピング

Notebookで検証 → Feature Function/Pipelineに移行 → テスト作成、というワークフローが理想的。

#### 6.2.3. Feature Functionsのテスタビリティ

「1特徴 = 1関数」アプローチの最大の価値は、**ユニットテストの容易さ**。

従来: 巨大な`compute_features`関数 → テストが困難
改善: 独立したFeature Functions → 個別にテスト可能

これにより、リファクタリング時の自信が劇的に向上。CI/CDが現実的になる。

#### 6.2.4. Polarsの台頭

Pandasの後継としてPolarsが注目されている理由:

- Lazy Evaluation(PySparkのような最適化)
- マルチコア活用(Pandasの弱点克服)
- Arrow互換性(エコシステムとの相互運用)
- シンプルなAPI(学習曲線が低い)

データサイズが10s GBsの中規模データでは、SparkよりPolarsの方が適切なケースが増えている。

#### 6.2.5. データサイズによるフレームワーク選択の実用性

「< 1GB: Pandas、10s GBs: Polars、TBs: Spark」という基準は非常に実用的。

ただし、追加の考慮事項:

- **チームスキル**: データエンジニアリング背景がない → Pandas/Polars
- **既存インフラ**: Sparkクラスターがある → Sparkを活用
- **将来のスケール**: 今は10s GBsだが数年でTBsに成長 → 最初からSpark

最適なフレームワークは「現在のデータサイズ + チーム + インフラ + 将来予測」の総合判断。

#### 6.2.6. Arrowの重要性

Apache Arrowが異なるDataFrameエンジン間のデータ転送を効率化:

- Pandas → Polars: ゼロコピー
- Polars → PyS park: ゼロコピー

これにより、「Pandasで試作 → Polarsで本番化 → Sparkにスケールアップ」という段階的な移行が現実的になる。

#### 6.2.7. RFM特徴の汎用性

Recency/Frequency/Monetaryは、**多くのビジネスドメインで有用な汎用特徴**:

- Eコマース: 顧客セグメンテーション
- 金融: 詐欺検知、与信判断
- SaaS: チャーンリスク予測

この種の「ドメイン横断的な有用特徴」のカタログを構築することが、Feature Storeの価値を高める。

#### 6.2.8. Binn ingのトレードオフ

連続値のBinning(カテゴリ化)のトレードオフ:

**メリット**:

- 非線形関係の捉え方(決定木に有利)
- 外れ値の影響軽減
- 解釈可能性向上

**デメリット**:

- 情報の損失
- ビンの境界設定が恣意的

モデルタイプ(決定木 vs 線形モデル)とビジネス要件(解釈可能性の重要度)に応じて判断。

#### 6.2.9. Monorepo vs Polyrepoの議論

本章はMonorepoを推奨するが、Polyrepo(FTI Pipeline別リポジトリ)のメリットも存在:

**Monorepoのメリット**:

- 共有コードの管理が簡単
- 単一のCI/CDパイプライン
- リファクタリングが容易

**Polyrepoのメリット**:

- 各Pipelineの独立デプロイ
- アクセス制御の粒度
- チーム間の責任分離

個人的には、**初期はMonorepo、組織が大きくなったらPolyrepoも検討**するアプローチが現実的。

#### 6.2.10. LLMによるユニットテスト生成

「LLM(ChatGPT)がユニットテスト作成を支援」という記述は、2024年以降のML開発の現実を反映:

- ユニットテストのボイラープレートをLLMが生成
- テストケースのアイデアをLLMが提案
- Edge Caseを見落とさない

これにより、テスト未経験者でもTDDを実践しやすくなる。

## 7. まとめ

本章はFeature PipelineのModel-Independent Transformations(MIT)の実装ガイド。Monorepo構成、DataFrame変換の分類、Pandas/Polars/PySparkの使い分け、Feature Functionsのベストプラクティスを網羅。

**重要な教訓**:

- Monorepoによる共有コード管理の簡素化
- 「1特徴 = 1関数」によるテスタビリティ向上
- データサイズによるフレームワーク選択(Pandas < 1GB、Polars 10s GBs、Spark TBs)
- EVAC変換(抽出・検証・集約・圧縮)の体系化
- Apache Arrowによるエンジン間相互運用性

## 8. 演習

### 演習1: フレームワーク選択(50K〜100K transactions/day)

**条件**:

- トランザクション: 50K/日(現在) → 100K/日(2年後)
- 履歴データ: 12ヶ月
- チーム: データエンジニアリング背景なし
- データマート: S3上のIceberg

**推奨**: **Polars**

**理由**:

- データサイズ: 数GB〜数十GB(Polarsの適用範囲)
- 学習曲線: Sparkより低い
- Iceberg互換: Arrowで効率的に読み込み可能

### 演習2: フレームワーク選択(10M transactions/day)

**条件**: 1000万トランザクション/日

**推奨**: **Apache Spark** または **dbt + SQL**

**理由**:

- データサイズ: 数TB(Sparkの領域)
- スケーラビリティ: 分散処理が必須

### 演習3: Email品質スコア特徴

LLMを使用してメールアドレスの品質を数値化:

```python
from email_validator import validate_email, EmailNotValidError

def email_quality_score(email: str) -> float:
    """メールアドレスの品質スコア(0.0〜1.0)を計算"""
    try:
        valid = validate_email(email)
        domain = valid.domain

        # ドメインベースのスコアリング
        if domain in ['gmail.com', 'yahoo.com', 'outlook.com']:
            return 0.8  # 一般的なフリーメール
        elif domain.endswith('.edu'):
            return 1.0  # 教育機関
        elif domain.endswith('.gov'):
            return 1.0  # 政府機関
        else:
            return 0.6  # その他
    except EmailNotValidError:
        return 0.0  # 無効なメール
```

## 9. 参考リンク

- [元ファイル](../machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_6.md)
- [Apache Hamilton](https://github.com/dagworks-inc/hamilton)
- [Polars](https://www.pola.rs/)
- [Apache Arrow](https://arrow.apache.org/)
- [Great Expectations](https://greatexpectations.io/)

## 10. 次に読むべき章

- **第7章**: Model-Dependent/On-Demand Transformations(MDT/ODT)の詳細
- **第8章**: Batch Feature Pipelineの実装
- **第9章**: Streaming Feature Pipelineの実装
