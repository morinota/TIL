O'Reilly Feature Store Book 第2章: MLパイプラインの分類と設計

## 1. 元記事情報

- **タイトル(原文)**: CHAPTER 2: Machine Learning Pipelines
- **書籍**: O'Reilly Feature Store for Machine Learning (著者不明)
- **種類**: 技術書籍の章
- **元ファイル**: [machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_2.md](../machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_2.md)

---

## 2. 概要

「MLパイプライン」という用語は曖昧すぎて有害である。本章では、AIシステムを構成する具体的なパイプライン(Feature-Training-Inference Pipeline: FTI)と、それぞれのパイプラインで実行すべきデータ変換の分類(MIT/MDT/ODT)を明確に定義する。また、最小限の実行可能な予測サービス(MVPS)開発プロセスと、モジュラーなコード設計のベストプラクティスを紹介する。

## 3. 背景・課題

### 3.1. MLパイプラインという用語の曖昧性

10人のデータサイエンティストに「MLパイプライン」の定義を尋ねると、10通りの異なる答えが返ってくる。ChatGPTはMLパイプラインが「データ収集、特徴量エンジニアリング、モデル訓練、評価、デプロイ、監視、推論、メンテナンス」のすべてを行うと説明するが、これは「素晴らしくて魔法のような単一のMLパイプライン」という非現実的なものだ。

この曖昧さは、AIシステムの構築についてコミュニケーションを取る際に「有害と見なされる」可能性がある。

### 3.2. 本書のアプローチ

本書では、より厳密なアプローチを取る:

- **パイプライン**: 明確に定義された入力と出力(インターフェース)を持ち、スケジュールまたは継続的に実行されるコンピュータプログラム
- **MLパイプライン**: AIシステムで使用されるMLアーティファクトを出力する任意のパイプライン
- **具体的なMLパイプライン**: 作成または変更するMLアーティファクトにちなんで命名される

MLパイプラインの例:
- **Feature Pipeline**: 特徴を出力
- **Vector Embedding Pipeline**: 埋め込みを出力
- **Training Pipeline**: トレーニングされたモデルを出力
- **Inference Pipeline**: 予測を出力
- **Model Validation Pipeline**: モデルを未検証から検証済みに移行
- **Model Deployment Pipeline**: モデルを本番環境にデプロイ

## 4. 主要なポイント

### 4.1. MVPS(最小限の実行可能な予測サービス)開発プロセス

MVPSプロセスは、できるだけ早く動作するAIシステムに到達することを目指す:

![図2-1: MVPSプロセス](images/figure_2_1_mvps_process.svg)

#### 4.1.1. 特定フェーズ

1. **予測問題**: 解決したい問題を定義
2. **KPIメトリクス**: 改善したいビジネス指標
3. **データソース**: 使用可能なデータ
4. **ML proxy metric**: 予測問題をMLが最適化するターゲットにマッピング(最も難しいステップ)

#### 4.1.2. 実装フェーズ

以下の手順でMVPSを構築することになる。
(ただし、予測問題、KPI、データソースを再定義する必要がある場合は、いつでも前のフェーズに戻ることができる)

- 手順1: **最小限の特徴量パイプライン(feature pipeline)**: 
  - 過去のデータをバックフィルし、増分のproductionデータを特徴量ストアに書き込むことができること。
- 手順2: **最小限のトレーニングパイプライン**: 
  - カスタムモデルが必要な場合(事前訓練済みモデルを使う場合はスキップ)
- 手順3: **最小限の推論パイプライン**:
  - モデルを使用して予測を行うための推論パイプライン。これはバッチプログラム or オンライン推論プログラム or LLMアプリケーション or エージェントである可能性。
- 手順4: **最小限のUI or ダッシュボード**:
  - ステークホルダーがMVPSを試すことができること。開発者がそれを見てシステムをiterativeに改善できること。

(個人的には、MVPSの中にちゃんと「手順4: 最小限のUI or ダッシュボード」が含めることが重要だと思った! やはり、実際に動かせるものを早期に見せることがステークホルダーとの共通認識を作る上で有効であり、逆に開発メンバーしか見えない状態だと不十分! 「隠してたらダメになる」とも言うし、最速でオープンな状態にしたい気持ち...!!:thinking:)

#### 4.1.3. カンバンボードを使ったMVPSの可視化

![図2-2: MVPSカンバンボード](images/figure_2_2_mvps_kanban.svg)

- **カンバンボード**: データソース、FTI技術、予測消費者の種類を可視化
  - そもそも「カンバンボード」って？？
    - 一言でいうと「**タスクの流れを見える化するボード**」のこと。
      - 列 = タスクの状態(未着手/作業中/レビュー中/完了など)
      - カード = 1タスク(チケット,issue, 作業単位)
      - 基本的には列がメインだが、「行 = 人, 優先度, スプリント」などで意味を持たせる場合もある。
    - 由来: 
      - トヨタの生産方式(製造業)発祥
      - 「必要なものを、必要な分だけ、必要なタイミングで」それを見える化したのがカンバン。
  - AIシステムを実装する前にMVPSカンバンボードを埋める事は、構築してるAIシステムの概要を把握する上で非常に有効。
    - まず、カンバンボードのタイトルをAIシステムが解決する予測問題の名前にする。
    - 次に、データソース、予測を消費するAIアプリケーション、FTIパイプラインを実装するために使う予定の技術を記入する。
    - 別のカンバンレーン(=行)を使って、非機能要件を注釈することもできる。
      - ex. 特徴量パイプラインのボリューム・速度・新鮮さの要件、オンライン推論パイプラインの応答時間のSLOなど。

### 4.2. モジュラーコードの記述

- 成功したAIシステムは、長期間にわたって維持・更新される必要がある -> 維持・更新を容易にするために、モジュラー性の高さが重要!
  - 具体的には、ソースコードに以下の変更を加えることになる:
    - 特徴量の追加・削除・変更、データソースの変更
    - モデルのアーキテクチャ・学習方法・ハイパーパラメータの変更
    - バッチAIシステムの場合、予測頻度の変更、予測の保存先の変更
    - オンラインAIシステムの場合、応答速度や特徴量の新鮮さの要件の変更
    - LLMアプリケーションやエージェントの場合、コンテキストエンジニアリング、ツールセット、LLMモデルバージョンの変更。

- システムアーキテクチャレベルの話:
  - AIシステムを3つ(orそれ以上)のパイプライン達に分割することでモジュラー性を高める事ができる。i.e. feature/training/inference pipelines architecture (FTIアーキテクチャ)
  - この高いモジュラー性により、**各パイプラインのデータ契約を破らない限り**、各パイプラインを独立して変更できる。
    - 「各パイプラインのデータ契約」の例: 
      - パイプラインの入力/出力スキーマ
      - 特徴量パイプラインのデータvalidationルール
      - 学習パイプラインのモデル性能SLO
      - 推論パイプラインの応答時間SLO

- 各MLパイプラインのコードレベルの話:
  - ソフトウェア工学のベストプラクティスに従ったモジュラーコード設計が必要。
    - ソースコードはテストされ、メンテナンスが容易で、DRY(Don't Repeat Yourself)であるべき。
  - **MLパイプラインのソースコードがスパゲッティノートブックの集まりである場合、信頼性の高いMLパイプラインを構築するのは難しくなる**...!!

- 

#### 4.2.1. 問題: スパゲッティノートブック

ノートブックにすべてのコードを詰め込むと:
- テストが困難
- 新しい開発者のオンボーディングが困難
- メンテナンスが困難

#### 4.2.2. 解決策: Feature Functions

Apache Hamiltonのアイデアに基づき、各特徴を個別の関数として定義:

**非モジュラー**:
```python
def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    if config["region"] == "UK":
        df["holidays"] = is_uk_holiday(df["year"], df["week"])
    else:
        df["holidays"] = is_holiday(df["year"], df["week"])
    df["avg_3wk_spend"] = df["spend"].rolling(3).mean()
    df["acquisition_cost"] = df["spend"]/df["signups"]
    # ...
    return df
```

**モジュラー**:
```python
def acquisition_cost(spend: pd.Series, signups: pd.Series) -> pd.Series:
    """Acquisition cost per user is total spend divided by number of signups."""
    return spend / signups
```

#### 4.2.3. メリット

- 各特徴の独立したユニットテストが可能
- 関数が契約(contract)を強制し、破壊的変更を検知
- ドキュメント化が容易
- デバッグが容易
- 再利用可能

#### 4.2.4. Feature Functionのワークフロー

![図2-3: Feature Pipelineアーキテクチャ](images/figure_2_3_feature_pipeline_arch.svg)

1. DataFrameを構築(feature functionsを適用)
2. Feature Groupに書き込み(commit: append/update/delete)
3. Training/Inference PipelineがFeature Query Serviceで読み取り

### 4.3. データ変換の分類(Taxonomy)

MLパイプラインは一連のデータ変換で構成される。本章では、データ変換を3つのクラスに分類する:

![図2-5: データ変換の分類](images/figure_2_5_transformation_taxonomy.svg)

#### 4.3.1. 3.1 Model-Independent Transformations (MIT)

**定義**: 多くのモデルで再利用できる特徴を作成する変換

**例**:
- ウィンドウ化された集約(max/min)
- ウィンドウ化されたカウント(1日のクリック数)
- RFM特徴(最近性、頻度、金銭的価値)

**実行場所**: Feature Pipelineでのみ実行

**保存先**: Feature Storeに保存され、下流のTraining/Inference Pipelineで使用

#### 4.3.2. 3.2 Model-Dependent Transformations (MDT)

**定義**: 特定のモデルとそのトレーニングデータに依存する変換

**例**:
- カテゴリ変数のエンコーディング(訓練データのカテゴリセットに依存)
- 数値変数の正規化/スケーリング(訓練データの平均/標準偏差に依存)

**実行場所**:
- Training Pipeline(訓練データ作成時)
- Inference Pipeline(推論時)
- **Feature Pipelineでは実行しない**(重要!)

**理由**:
1. **再利用不可**: モデルごとに異なる変換が必要
2. **EDA困難**: 正規化された値(0.541)より元の値($74,580)の方が分析しやすい
3. **Write Amplification**: 正規化された特徴をFeature Storeに保存すると、新しいデータの追加時に既存データの再計算が必要

**注意点**: Training PipelineとInference Pipelineの実装間にスキューがないことを確認する必要がある

#### 4.3.3. 3.3 On-Demand Transformations (ODT)

**定義**: リクエスト時のデータを使って計算される変換

**例**:
- 検索クエリのトークン化
- リクエスト時刻からの時間帯特徴の計算

**実行場所**:
- Online Inference Pipeline(リクエスト時)
- Feature Pipeline(履歴データから再利用可能な特徴を作成)

**重要**: 同じUDFを両方のパイプラインで使用することでスキューを防ぐ

**制約**: Batch Inference Pipelineはリクエスト時パラメータがないため、ODTをサポートしない

#### 4.3.4. 特徴タイプとの関係

![図2-4: Feature Typesの分類](images/figure_2_4_feature_types.svg)

**Feature Types**:
- **Categorical**: 文字列、列挙型、ブール値
- **Numerical**: int、float、double
- **Array**: リスト、ベクトル埋め込み

各特徴タイプに対して有効な変換が定義される:
- Categoricalはエンコード可能だが正規化不可
- Numericalは正規化可能だがエンコード不可
- Arrayはインデックス/クエリ可能

![図2-6: FTIパイプラインとデータ変換のマッピング](images/figure_2_6_fti_transformation_mapping.svg)

### 4.4. 3つの主要なMLパイプライン

#### 4.4.1. 4.1 Feature Pipeline

**定義**: Model-IndependentおよびOn-Demand変換のデータフローグラフを実行するプログラム

**主要な変換**:
- データ抽出
- データ検証とクリーニング
- 特徴抽出
- 集約
- 次元削減(ベクトル埋め込み)
- ビニング、特徴交差

**特殊なFeature Pipeline**:
- **Vector Embedding Pipeline**: ベクトル埋め込みを作成しVector Indexに保存
- **Feature Data Validation Pipeline**: 非同期でデータ検証ルールを実行

**非機能要件**:
1. **Backfilling/Incremental Data**: 同じパイプラインで履歴データと新規データを処理
2. **Fault Tolerance**: 失敗/再試行で破損・重複データを生じない(冪等性と原子性)
3. **Scalability**: データ量に応じたリソース確保
4. **Feature Freshness**: クライアントが使用する特徴の最大許容年齢
5. **Governance & Security**: 処理場所、権限、監査ログ、タグ付け
6. **Data Quality**: 事前検証 vs 事後検証

**技術選択**:
- **< 1GB**: Pandas
- **10s GBs**: Polars
- **TBs**: Apache Spark、SQL、dbt
- **Streaming**: Feldera(SQL)、Apache Flink、Spark Structured Streaming

![図2-7: Feature Pipelineのクラス](images/figure_2_7_feature_pipeline_classes.svg)

#### 4.4.2. 4.2 Training Pipeline

**定義**: Feature Storeから特徴を読み取り、MDTを適用し、モデルを訓練し、検証し、Model Registryに公開し、本番環境にデプロイするプログラム

**実行タイミング**: オンデマンドまたはスケジュール(例: 1日/週1回)

**4つのクラス**:
1. **Complete Training Pipeline**: すべてのタスクを実行
2. **Model Deployment Pipeline**: Model RegistryからモデルをダウンロードしてDeployment(A/Bテスト含む)
3. **Model Validation Pipeline**: 非同期でモデルを評価(GPUとCPUの分離でコスト効率化)
4. **Training Dataset Pipeline**: 大規模データセット用に訓練データをファイルとして保存

![図2-8: Training Pipelineのクラス](images/figure_2_8_training_pipeline_classes.svg)

#### 4.4.3. 4.3 Inference Pipeline

**定義**: 新しい特徴データを読み込み、変換を適用し、モデルで予測を出力するプログラム

**3つのクラス**:

1. **Batch Inference Pipeline**
   - 実装: Pandas、Polars、Spark、SQL UDF
   - 入力: Feature Storeから事前計算された特徴
   - 出力: データベースのテーブルに予測を保存
   - 実行: スケジュール実行(例: 毎日)
   - パラメータ: start_time/end_time、entity IDs

2. **Online Inference Pipeline**
   - 実装: Python(FastAPI、KServe)
   - 入力: リクエストパラメータ + Feature Storeから事前計算された特徴
   - 処理フロー:
     1. リクエストパラメータ受信
     2. Feature Storeから特徴読み込み
     3. ODT/MDTを適用してFeature Vector作成
     4. モデル呼び出し
     5. 予測とFeatureをログ記録
     6. クライアントに予測を返却
   - API: Deployment API(entity IDs + リアルタイム特徴パラメータ)

3. **Agentic Pipeline**
   - 実装: LlamaIndex、LangGraph、LangChain、CrewAI
   - 構成: LLM + Tools(schema付き)
   - 実行フロー:
     1. クライアントからクエリ受信
     2. LLMにクエリとツールリストを送信
     3. LLMがツールまたは最終応答を返す
     4. ツールの場合: 実行して結果をLLMに送信(ループ)
     5. 最終応答をクライアントに返却

![図2-9: Inference Pipelineのクラス](images/figure_2_9_inference_pipeline_classes.svg)

### 4.5. 実例: Titanic Survival MLシステム

#### 4.5.1. システム設計

![図2-10: Titanic生存予測 MVPSカンバンボード](images/figure_2_10_titanic_kanban.svg)

- **予測問題**: タイタニック乗客の生存確率
- **データソース**: Titanic Survival Dataset(静的) + 合成データ生成関数
- **KPI**: Counterfactual予測("もし〜だったら"シナリオ)
- **技術スタック**: Python(Pandas)、XGBoost、Hopsworks Feature Store、Gradio UI

![図2-11: Titanicデータセット構造](images/figure_2_11_titanic_dataset.svg)

#### 4.5.2. Feature Pipeline

```python
import pandas as pd
import hopsworks
BACKFILL=True

def get_new_synthetic_passenger():
    # 元のデータセットと同じ分布から合成データを生成

if BACKFILL==True:
    df = pd.read_csv("titanic.csv")
else:
    df = get_new_synthetic_passenger()

fs = hopsworks.login().get_feature_store()
fg = fs.get_or_create_feature_group(name="titanic", version=1, \
    primary_keys=['id'], description="Titanic passengers")
fg.insert(df)
```

- **スケジュール**: 1日1回実行、1人の新しい合成乗客を作成
- **データ拡張**: datetime列を追加(元データはTitanic災害日、新規データは作成日時)

#### 4.5.3. Training Pipeline

```python
import xgboost

fg = fs.get_feature_group(name="titanic", version=1)
fv = fs.get_or_create_feature_view(name="titanic", version=1, \
    labels=['survived'], \
    query=fg.select_features()
)

X_train, X_test, y_train, y_test = fv.train_test_split(test_size=0.2)
model = xgboost.XGBClassifier()
model.fit(X_train, y_train)
model.save_model("model_dir/model.json")

mr = hopsworks.login().get_model_registry()
mr_model = mr.python.create_model(
    name="titanic",
    feature_view=fv,
)
mr_model.save("model_dir")
```

- **Feature View**: 入力特徴と出力ラベルを表現(特徴量-ラベルがjoinされたキャッシュ的な概念)
- **Train/Test Split**: 80%訓練、20%テスト
- **モデル**: XGBoost勾配ブースト決定木

#### 4.5.4. Batch Inference Pipeline

```python
retrieved_model = mr.get_model(name="titanic", version=1)
saved_model_dir = retrieved_model.download()
model = xgboost.XGBClassifier()
model.load_model(saved_model_dir + "/model.json")

row_data = # 新しい乗客の特徴行を取得
prediction = model.predict(row_data)
```

- **スケジュール**: 1日1回実行
- **処理**: 新しい合成乗客の生存を予測し、Feature Viewに記録

#### 4.5.5. インタラクティブUI

- **フレームワーク**: Gradio(Python)
- **機能**: "What-if"質問(例: 男性、49歳、3等クラスの乗客の生存確率は?)

## 5. 技術的な詳細

### 5.1. MLアーティファクトの定義

**MLアーティファクト**: MLパイプラインが生成し、MLインフラサービスが管理する状態を持つオブジェクト

**種類**:
- モデル
- 特徴
- トレーニングデータ
- ベクトルインデックス
- モデルデプロイメント
- 予測/コンテキストログ

**特性**:
- ほとんどは不変(immutable)
- 例外: 特徴データ、ベクトルインデックス、モデルデプロイメントは更新可能

### 5.2. データ変換分類の実践的な影響

#### 5.2.1. MIT(Model-Independent Transformations)

**実行場所**: Feature Pipelineのみ

**メリット**:
- 1回計算すれば複数モデルで再利用可能
- Feature Storeで管理
- EDAに適した形式で保存

#### 5.2.2. MDT(Model-Dependent Transformations)

**実行場所**: Training Pipeline + Inference Pipeline

**課題とソリューション**:
- **Training-Serving Skew**: 同じ実装を両方のパイプラインで使用
- **Write Amplification回避**: Feature Storeには保存しない
- **バージョニング**: ロジック変更時は新バージョンの特徴を作成

#### 5.2.3. ODT(On-Demand Transformations)

**実行場所**: Online Inference Pipeline + Feature Pipeline(履歴データ)

**実装**:
- UDF(User-Defined Function)として実装
- 同じUDFを両パイプラインで再利用してスキューを防止

### 5.3. Feature Pipelineの設計パターン

#### 5.3.1. BackfillとIncremental Update

同じパイプラインで両方をサポート:

```python
BACKFILL = True  # または False

if BACKFILL:
    # 履歴データ全体を処理
    df = read_historical_data()
else:
    # 新規データのみを処理
    df = read_incremental_data(last_processed_timestamp)

fg.insert(df)  # Commitとして追加
```

#### 5.3.2. Idempotence(冪等性)

- 複数回実行しても同じ結果
- 失敗時に安全に再実行可能

#### 5.3.3. Atomicity(原子性)

- 更新が一度に適用される
- 失敗時に部分的な更新が適用されない

### 5.4. Training Pipelineの分離パターン

#### 5.4.1. パターン1: Complete Pipeline

すべてを1つのパイプラインで実行(シンプルなケース)

#### 5.4.2. パターン2: 役割分離

1. **Training Dataset Pipeline**: データ準備(CPU)
2. **Model Training**: モデル訓練(GPU)
3. **Model Validation Pipeline**: 検証(CPU)
4. **Model Deployment Pipeline**: デプロイ(運用)

**メリット**:
- GPUとCPUの効率的な利用
- 人間承認のポイント追加
- ロールバック可能

### 5.5. Hopsworks環境のセットアップ

#### 5.5.1. インストール

**Linux/macOS**:
```bash
pip install hopsworks[python]
```

**Windows**:
```bash
pip install twofish
pip install hopsworks[python]
```

#### 5.5.2. アカウント設定

1. Hopsworks Serverlessでアカウント作成(無料プランあり: 35GB)
2. APIキー取得(User → Account → API)
3. `.env`ファイルに保存

## 6. 学びと考察

### 6.1. 学んだこと

1. **用語の明確化の重要性**: "MLパイプライン"という曖昧な用語ではなく、Feature/Training/Inference Pipelineと具体的に命名することで、コミュニケーションが明確になる

2. **データ変換の適切な配置**: MIT/MDT/ODTの分類により、どのパイプラインでどの変換を行うべきかが明確になる
   - Feature PipelineでMDTを実行すると、再利用性とコスト効率が損なわれる
   - Training-Serving Skewを防ぐには、MDTとODTの実装を共通化する

3. **Feature Functionsアプローチ**: 各特徴を独立した関数として定義することで、テスト可能性、再利用性、メンテナンス性が向上する

4. **MVPS開発プロセス**: 予測問題→KPI→ML proxy metric→データソースの順に定義し、FTIパイプラインを段階的に実装することで、早期に動作するシステムを構築できる

5. **非機能要件の重要性**: スケーラビリティ、フォールトトレランス、特徴の新鮮さなどの非機能要件を、カンバンボードで早期に可視化することが重要

### 6.2. 自分の考察

#### 6.2.1. Feature Storeの中心性

本章で明確になったのは、Feature StoreがFTIパイプライン間の「契約(contract)」を定義する中心的な役割を果たすことだ。Feature Storeは単なるデータ保存場所ではなく:

1. **再利用可能な特徴の管理**: MITで生成された特徴を一元管理
2. **スキーマとデータ契約の強制**: 下流パイプラインが依存できる安定したインターフェース
3. **バージョニング**: 特徴ロジック変更時の影響範囲を制御

#### 6.2.2. ラベルの保存場所について

疑問点として、ラベル(target)もFeature Storeに保存すべきかという点がある。本章の実例では、Feature ViewでラベルとFeatureを結合している。

- **メリット**: Training Pipelineでの取得が簡単
- **デメリット**: Online Storeにラベルを保存する必要性は低い(推論時には不要)

おそらく、Offline Storeにのみラベルを保存し、Online StoreにはFeatureのみを保存する設計が合理的だろう。

#### 6.2.3. MDTのバージョニング戦略

MDTのロジック変更時に「新しいバージョンの特徴を作成する」という推奨は興味深い。これは:

- 既存モデルへの影響を防ぐ
- A/Bテストを可能にする
- Feature Storeに蓄積される特徴カラムが増える

この運用では、Feature Storeのストレージコストとクエリ複雑性のトレードオフを考慮する必要がある。不要になった古いバージョンの特徴を削除するガベージコレクションプロセスも重要だろう。

#### 6.2.4. Streaming処理の必要性判断

Feature Freshnessの要件によって、Batch vs Streaming処理を選択する。判断基準:

- **Batch**: 毎時/毎日の更新で十分(例: 日次レコメンデーション)
- **Micro-Batch**: 数分の遅延が許容(例: Spark Structured Streaming)
- **True Streaming**: 秒単位の新鮮さが必要(例: Feldera、Flink)

コスト・複雑性・新鮮さのトレードオフを慎重に評価すべきだ。

#### 6.2.5. SQL vs Pythonの選択

Feature Pipelineの実装にSQLとPythonの両方が使われる。

**SQL(dbt)の適合性**:
- データエンジニアのスキルセット
- データウェアハウス内でのデータ変換
- モジュール性(dbt models)

**Pythonの適合性**:
- 複雑な変換ロジック
- MLフレームワークとの統合
- UDFの再利用(ODT)

プロジェクトによって、チームのスキルとデータの場所を考慮して選択すべきだ。

#### 6.2.6. Titanic例の教育的価値

Titanic Survivalの例は、静的データセットから動的システムへの移行を示す点で教育的だ。合成データ生成関数を使うことで:

- Feature Pipelineのバックフィル/増分更新の両方を体験
- Batch Inference Pipelineのスケジュール実行を学習
- 動的データの概念を理解

実務では、実際のストリーミングデータソースやリアルタイム予測が必要になるが、学習の第一歩としては優れている。

## 7. 参考リンク

- [Apache Hamilton](https://github.com/dagworks-inc/hamilton): Feature Functionsアプローチのベース
- [Hopsworks](https://www.hopsworks.ai/): Feature Store & Model Registry
- [Feldera](https://www.feldera.com/): SQL-based Streaming Feature Pipeline Engine
- [Gradio](https://www.gradio.app/): PythonでWeb UIを作成するフレームワーク
- [書籍GitHubリポジトリ](https://github.com/featurestore): Titanic例の完全なソースコード

## 8. 次に読むべき章

- **第5章**: 特徴のバージョニング詳細
- **第7章**: ODTのUDF実装
- **第8章**: バッチFeature Pipeline
- **第9章**: ストリーミングFeature Pipeline
- **第11章**: Online Inference PipelineとDeployment API
