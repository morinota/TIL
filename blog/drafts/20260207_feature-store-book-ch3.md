O'Reilly Feature Store Book 第3章: 空気質予測サービスの構築

## 1. 元記事情報

- **タイトル(原文)**: CHAPTER 3: Your Friendly Neighborhood Air Quality Forecasting Service
- **書籍**: O'Reilly Feature Store for Machine Learning
- **種類**: 技術書籍の章(ハンズオンプロジェクト)
- **元ファイル**: [machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_3.md](../machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_3.md)

---

## 2. 概要

第1章、第2章で学んだMLシステムアーキテクチャを実践する最初のプロジェクト。世界中のIoT愛好家が公開する空気質センサーデータと天気予報データを使用して、自分の近隣地域の空気質(PM2.5)を予測するAIシステムを構築する。GitHub ActionsとHopsworksの無料サーバーレスサービスを使用し、コストゼロで持続可能な公共サービスを実現する。

## 3. 背景・課題

### 3.1. 個人的な動機

著者は嚢胞性線維症(主に肺に影響を与える遺伝性疾患)を持つ2人の息子がおり、空気質予測サービスは彼らや同様の疾患を持つコミュニティにとって非常に有用なサービスとなる。

### 3.2. データソース

- **空気質センサー**: 世界中のIoT愛好家が庭やバルコニーに設置したセンサー
  - ストックホルム: 30以上の公共センサー
  - ダブリン: 40以上の公共センサー
  - データソース: aqicn.org(World Air Quality Index)

### 3.3. 技術的な課題

**Microsoft Auroraの限界**:

2024年、Microsoft AIは世界全体の大気汚染を予測する深層学習モデル「Aurora」を構築した。EUのCopernicusプロジェクトの物理モデルと比較して大きな前進と称賛されたが、**実際の都市レベル(例: ストックホルム)では予測精度が低い**。

**本プロジェクトの挑戦**:

- Auroraよりも優れた空気質予測をコストの一部で実現
- **高品質なデータ + 決定木MLモデルが深層学習を上回ることを証明**

### 3.4. Wow Factor: GenAIの活用

LLMによる音声駆動UIを持つ「親しみやすい」空気質予測サービスを構築する。

## 4. 主要なポイント

### 4.1. AIシステムカード(Prediction Service Card)

プロジェクト承認の最も簡単な方法は**AIシステムカード**を作成すること。これは第2章のMVPSカンバンボードの簡略版で、以下を含む:

- **予測問題**: 何を予測するか(PM2.5レベル)
- **データソース**: 空気質センサー、天気予報API
- **予測の消費方法**: UI or API
- **監視方法**: パフォーマンス監視の方法

**PM2.5の選択理由**:

- 直径2.5マイクロメートル以下の微細粒子
- 低出生体重、心臓病、肺疾患のリスクを高める
- 視界を悪化させ、空気がかすんで見える

**予測に使用する特徴**:

PM2.5は**風速/風向、温度、降水量**と相関するため、天気予報データを使用:

- 風向きが特定方向 → 空気質が良好(特に混雑した道路の近く)
- 寒い天候 → 空気質悪化(冷たい空気は密度が高く動きが遅い、通勤時の車利用増加)

### 4.2. システムアーキテクチャ

#### 4.2.1. 使用技術

**無料サーバーレスサービス**:

- GitHub Actions/Pages
- Hopsworks

**実装する5つのPythonプログラム**:

1. **Feature Groups作成 + Backfill**: 歴史的データでデータを初期化
2. **Feature Pipeline(日次)**: 新しいデータを取得し Feature Store に保存
3. **Training Pipeline**: XGBoost回帰モデルを訓練し Model Registry に保存
4. **Batch Inference Pipeline**: モデルで予測を行い、予測/ヒンドキャストグラフを生成
5. **LLM-powered UI**: Streamlit + Whisper(音声→テキスト) + LLM(テキスト→関数呼び出し)

**使用ライブラリ/技術**:

- REST APIs: 空気質・天気データ取得
- Pandas: データ処理
- Hopsworks: Feature Store + Model Registry
- XGBoost: 勾配ブースト決定木
- GitHub Actions: スケジュール実行(日次)
- GitHub Pages: ダッシュボード表示
- Streamlit: 音声/テキストUI
- Whisper: 音声認識
- LLM: Function Calling

**重要な示唆**:

> 素晴らしい音楽が3つのコードで作られるように、多くの素晴らしいAIシステムは**Feature Pipeline、Training Pipeline、Inference Pipeline**から作られる。

### 4.3. データ取得

#### 4.3.1. 空気質データ

**データソース**: aqicn.org

**注意点**:

- コミュニティサービスのためデータ品質保証なし
- センサー選択基準:
  1. 歴史的データが利用可能(数年分が理想)
  2. 信頼できる測定値(一定期間オフや故障しない)
- 2025年中頃時点で歴史的データのAPI呼び出しは利用不可 → 手動ダウンロード
- APIキー作成が必要(最新データ取得用)

**CSVファイル処理**:

- 列名確認: `pm25`と`date`列が必要
- 一部のファイルは`min/max/median/stdev`列 → `median`を`pm25`にリネーム

#### 4.3.2. 天気データ

天気予報データを使用してPM2.5を予測。

### 4.4. 探索的データ分析(EDA)

データの理解と前処理:

- データの可視化
- 欠損値の確認
- 相関分析
- 外れ値の検出

### 4.5. Feature Groups作成とBackfilling

**Feature Group**:

- Feature Storeにデータを保存するための論理的なグループ
- Offline Store(履歴データ、モデル訓練用)
- Online Store(リアルタイムデータ、推論用)

**Backfilling**:

- 歴史的データでFeature Groupを初期化
- 一度だけ実行

### 4.6. Feature Pipeline(日次実行)

**処理フロー**:

1. 空気質センサーAPIから最新データ取得
2. 天気予報APIから予報データ取得
3. データ前処理
4. Feature Storeに保存

**スケジュール**:

- GitHub Actionsで毎日実行
- Cron式で実行時刻指定

### 4.7. Training Pipeline

**処理フロー**:

1. Feature Storeから訓練データ読み込み
2. Train/Test Split
3. XGBoost回帰モデル訓練
4. Model Registryに保存

**実行タイミング**:

- オンデマンド実行
- モデル性能が劣化した際に再訓練

### 4.8. Batch Inference Pipeline

**処理フロー**:

1. Model Registryからモデルダウンロード
2. Feature Storeから最新特徴データ読み込み
3. 予測実行
4. 予測/ヒンドキャストグラフ生成(PNG)

**出力**:

- Forecast(予測): 今後の空気質予測
- Hindcast(ヒンドキャスト): 過去の予測と実測値の比較

**スケジュール**:

- GitHub Actionsで毎日実行

### 4.9. パイプラインのスケジューリング

#### 4.9.1. GitHub Actions

**YAMLワークフロー定義**:

```yaml
name: air-quality-daily
on:
  schedule:
    - cron: '11 6 * * *'  # 毎日6:11 UTC実行
```

**実行順序**:

1. Feature Pipeline
2. Batch Inference Pipeline

#### 4.9.2. GitHub Pages

**ダッシュボード構築**:

- 静的HTMLページとして予測/ヒンドキャストグラフを表示
- GitHub Pagesで無料ホスティング

### 4.10. LLMを用いた Function Calling

**音声駆動UI**:

1. ユーザーが音声で質問
2. Whisperモデルが音声→テキスト変換
3. LLMがテキスト→関数呼び出しに変換
4. AIシステムの関数を実行
5. 結果をユーザーに返す

**Function Calling**:

- LLMに利用可能な関数リスト(スキーマ)を提供
- LLMが適切な関数と引数を選択
- 自然言語インターフェースを実現

## 5. 技術的な詳細

### 5.1. 空気質データの特性

**PM2.5と天気の相関**:

- 風向き: 特定方向で空気質改善(汚染源からの風上)
- 温度: 寒い天候で空気質悪化(空気の密度・移動速度)
- 降水量: 雨が汚染物質を洗い流す

### 5.2. XGBoost回帰モデル

**選択理由**:

- 勾配ブースト決定木
- 表形式データに強い
- 解釈可能性が高い
- 深層学習より高品質データで優れた性能

### 5.3. Feature Storeの役割

**2つのストア**:

- **Offline Store**: 履歴データ、モデル訓練用(列指向ストア)
- **Online Store**: リアルタイムデータ、推論用(行指向ストア)

**利点**:

- Feature PipelineとTraining/Inference Pipelineの分離
- 特徴の再利用性
- データ品質保証

### 5.4. GitHub Actions + Hopsworksの無料運用

**コストゼロで運用可能**:

- GitHub Actions: 月2000分無料(パブリックリポジトリは無制限)
- Hopsworks: 無料プラン(35GB)
- GitHub Pages: 無料ホスティング

**持続可能性**:

- サーバー管理不要
- スケーラビリティ
- 高可用性

### 5.5. Whisper + LLMのUIアーキテクチャ

**Whisper(OpenAI)**:

- オープンソースの音声認識モデル
- 多言語対応
- 高精度

**LLM Function Calling**:

- 関数スキーマをLLMに提供
- LLMが自然言語→構造化呼び出しに変換
- 例: 「明日の空気質は?」 → `get_air_quality_forecast(date="tomorrow")`

### 5.6. Forecast vs Hindcast

**Forecast(予測)**:

- 未来の空気質を予測
- ユーザーに提供する主要な価値

**Hindcast(ヒンドキャスト)**:

- 過去の予測と実測値の比較
- モデル性能の監視
- モデル再訓練の判断材料

## 6. 学びと考察

### 6.1. 学んだこと

1. **MVPSプロセスの実践**: 第2章の理論を実際のプロジェクトに適用。AIシステムカードによる事前設計の重要性。

2. **深層学習 vs 高品質データ + 決定木**: Microsoft Auroraのような大規模深層学習モデルよりも、ローカルな高品質データと適切なモデル(XGBoost)の組み合わせが優れた性能を発揮する場合がある。**データエンジニアリングの重要性**。

3. **無料サーバーレスの威力**: GitHub Actions + Hopsworksでコストゼロの持続可能な公共サービスを構築可能。サーバー管理の負担がない。

4. **Feature Storeの実践的価値**: Offline/Online Storeの分離により、Feature Pipeline、Training Pipeline、Inference Pipelineが独立して動作。モジュラー性の実現。

5. **LLM Function Callingによるアクセシビリティ向上**: 音声駆動UIにより、技術的な知識がないユーザーでもサービスを利用可能。Whisper + LLMの組み合わせは強力。

### 6.2. 自分の考察

#### 6.2.1. 「3つのコード」の比喩の深さ

> 素晴らしい音楽が3つのコードで作られるように、多くの素晴らしいAIシステムはFeature Pipeline、Training Pipeline、Inference Pipelineから作られる。

この比喩は、複雑さを追求するのではなく、**シンプルで明確なアーキテクチャの価値**を示している。多くの技術者が「最新の深層学習」「複雑なアーキテクチャ」を追求しがちだが、実際には**適切なデータ + シンプルなモデル + 明確なパイプライン**が持続可能なシステムを生む。

#### 6.2.2. データ品質 > モデル複雑性

Microsoft Auroraは世界規模の深層学習モデルだが、都市レベルの予測精度が低い。一方、ローカルセンサーデータ + 天気予報 + XGBoostの組み合わせは優れた性能を発揮する。

**示唆**:

- **「データは新しい石油」ではなく「高品質なデータは新しい石油」**
- 大規模モデルよりも、問題に適したデータソースの選定が重要
- データエンジニアリングのスキルが競争優位性を生む

#### 6.2.3. コミュニティデータの価値

世界中のIoT愛好家が公開するセンサーデータは、データ品質保証がないにもかかわらず、実用的なAIシステム構築に十分。**オープンデータの民主化**により、個人や小規模チームでも価値あるサービスを構築できる時代。

社会のデジタル化 → データソースの増加 → AIシステム構築の民主化

#### 6.2.4. 無料サーバーレスの破壊力

GitHub Actions + Hopsworksでコストゼロの運用が可能。これは、**個人や非営利団体が持続可能な公共サービスを提供できる**ことを意味する。

従来: サーバーコスト・管理負担 → 企業・大学のみが運用可能
現在: 無料サーバーレス → 個人が公共サービスを提供可能

この変化は、**AIシステムの民主化**において極めて重要。

#### 6.2.5. AIシステムカードの実用性

MVPSカンバンボードの簡略版として、AIシステムカードは以下の利点:

- プロジェクト承認の効率化
- ステークホルダーとのコミュニケーション
- 実現可能性の早期検証(データソースの存在確認)

実務で積極的に活用したい。特に「予測の消費方法(UI or API)」を事前に定義することで、インターフェース設計が明確になる。

#### 6.2.6. Hindcastの監視価値

予測(Forecast)だけでなく、ヒンドキャスト(Hindcast)を生成することで:

- モデル性能のリアルタイム監視
- 再訓練のトリガー判断
- ステークホルダーへの信頼性の提示

「予測が当たっているか」を可視化することは、AIシステムの信頼性を高める上で重要。

#### 6.2.7. Function Callingの可能性

LLM Function Callingは、**技術的なインターフェース(API)と自然言語インターフェース(UI)の境界を曖昧にする**。

従来: API仕様書を読み、正確なリクエストを構築
現在: 自然言語で質問、LLMが適切な関数呼び出しに変換

この技術は、AIシステムのアクセシビリティを劇的に向上させる。特に、音声駆動UI(Whisper + LLM)は、視覚障害者や高齢者にとっても有用。

#### 6.2.8. 個人的動機の力

著者の2人の息子の疾患が、このプロジェクトの原動力となっている。**個人的な動機が、優れた公共サービスを生み出す**好例。

技術書籍でこのような個人的背景を明示することは珍しいが、読者に「なぜこのプロジェクトが重要か」を伝える上で非常に効果的。

#### 6.2.9. 5つのPythonプログラムの役割分離

1. Backfill: 初期化(一度だけ)
2. Feature Pipeline: データ収集(日次)
3. Training Pipeline: モデル訓練(オンデマンド)
4. Inference Pipeline: 予測(日次)
5. UI: ユーザーインターフェース(常時)

この役割分離は、**各プログラムを独立してテスト・デバッグ・改善できる**ため、メンテナンス性が高い。FTIアーキテクチャの実践的な価値を示している。

#### 6.2.10. 歴史的データAPIの欠如

2025年中頃時点で、歴史的データのAPI呼び出しが利用できない。これは**コミュニティデータソースの限界**を示している。

一方で、手動ダウンロードという「一度だけの手間」を許容することで、その後の自動化が可能。完璧なAPIを待つよりも、利用可能なデータで素早く構築する姿勢が重要。

## 7. まとめ

本章は、第1章・第2章の理論を実践する最初のプロジェクト。空気質予測サービスを通じて、Feature/Training/Inference Pipelineのアーキテクチャを学び、無料サーバーレスサービスでコストゼロの持続可能な公共サービスを構築した。

**重要な教訓**:

- 高品質なデータ + 適切なモデル > 大規模深層学習
- Feature Storeによるモジュラー性の実現
- GitHub Actions + Hopsworksによる無料運用
- LLM Function Callingによるアクセシビリティ向上
- 個人的動機が優れた公共サービスを生む

## 8. 演習

### 演習1: ラグ付きPM2.5特徴の追加

- 昨日のPM2.5値を特徴として追加
- 2日前、3日前の値も試し、モデル精度への影響を確認

### 演習2: 歴史的PM2.5値のリスク評価

- 将来のPM2.5予測に過去のPM2.5値を使用することのリスクを考察
- データリーケージ(Data Leakage)の可能性

## 9. 参考リンク

- [元ファイル](../machine_learning/MLOps/feature_store/oreilly_feature_store_book/chapter_3.md)
- [World Air Quality Index](https://aqicn.org/)
- [Hopsworks](https://www.hopsworks.ai/)
- [GitHub Actions](https://github.com/features/actions)
- [GitHub Pages](https://pages.github.com/)
- [XGBoost](https://xgboost.readthedocs.io/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Streamlit](https://streamlit.io/)

## 10. 次に読むべき章

- **第4章**: Feature Storeの詳細(Part 2の開始)
- **第6章**: Model-Independent Transformations(MIT)の詳細
- **第8章**: Batch Feature Pipelineの深掘り
