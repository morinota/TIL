<!-- (番外編)MLOps勉強会で推薦システム関連の発表を聞いて知らない用語を調べる!:MLOps Maturity Assessment -->

# MLOps Maturity Assessment

published date: 18 April 2023,
authors: Vechtomova Maria
url(paper): https://mlops.community/mlops-maturity-assessment/
(勉強会発表者: morinota)

---

(論文じゃないですが、いつもと同じフォーマットっぽく書いてみます。)

## どんなもの?

- 2023/10のMLOps勉強会の[発表](https://speakerdeck.com/masatakashiwagi/di-35hui-mlops-mian-qiang-hui-komiyuniteipuratutohuomunobatutirekomendowozhi-eruji-jie-xue-xi-ji-pan)にて引用されており気になったので、MLOps周りのcatch upとして読んでみました...!
- あるprojectのMLOpsの成熟度を評価するのに役立つアンケート。
- MLOpsの幅広い側面をカバーしていて、MLOpsの実践を改善したいと考えてるチームにとって有効な資料??
  - 7つのセクションに分かれており、セクション1~4の全ての問にYesと答える事ができれば、プロジェクトはMLOpsの観点で成熟しているとみなせる。
    - (i.e. セクション1~4が、MLプロジェクトを本番環境で確実にデプロイする為の必要条件)
    - セクション5~7は、MLOps成熟度の必要条件を超えた項目。
  - 「No」と答えた観点が、プロジェクトのMLOps成熟度を向上させる為に組織が取り組むべき事になる。

## 先行研究と比べて何がすごい？

- 機械学習をプロダクトに導入する上で、MLOpsのベストプラクティスを採用することが重要。
- しかし、MLOpsのベストプラクティスが実際にどのようなものなのか、また、開発組織のMLOpsをより成熟させるにはどのようにすればよいのか、について構造化された情報を見つけるのは難しい。
- 既存のMicrosoftの [MLOps maturity model](hoge) やGoogleの [MLOps levels](hoge) もあるが、MLOps未成熟な状態からいかに100%の成熟度を達成する方法について、必ずしも有効な洞察を与えてくれるわけではない。(これらは、強く大きなテック組織を前提としてる感がある??:thinking:)
- MLOps Maturity Assessmentは、hogehoge。

## 技術や手法の肝は？

- 本アンケートは、以下の7つのセクションに分かれている:
  - Documentation
  - Traceability & Reproducibility
  - Code quality
  - Monitoring & Support
  - Data transformation pipelines & Feature store
  - Model explainability
  - A/B testing & Feedback loop
- セクション1~4の全ての問にYesと答える事ができれば、プロジェクトはMLOpsの観点で成熟しているとみなせる。
  - (i.e. セクション1~4が、MLプロジェクトを本番環境で確実にデプロイする為の必要条件)
- セクション5~7は、MLOps成熟度の必要条件を超えた項目。
- 本アンケートでは、高度なMLOps(=section 5~7)の実践に移る前に、基本条件(=section 1~4)を優先する事を推奨している。
- 本アンケートにて「No」と答えた観点が、プロジェクトのMLOps成熟度を向上させる為に組織が取り組むべき事になる。

以下は、各セクション1 ~ 7にざっくり書かれている事。(+自分の感想:thinking:)

### セクション1: Documentation

- 1.1. Project Documentation(MLプロジェクトに関する文書化)
  - MLプロジェクトのビジネスゴールとKPI、MLモデルのリスク評価等の結果を文書化し、常に最新の状態に保ちましょう、みたいな話。
    - (MLモデルのリスク評価=MLモデルの推論結果が誤ってる場合のビジネス損失...??:thinking:)
- 1.2. ML model documentation
  - 学習・推論用データの取得方法、前処理方法、データ定義(MLモデルで採用されている特徴量 & 各特徴量の意味)などの仕様とそのモチベーションを文書化し、常に最新の状態に保ちましょう、みたいな話。
- 1.3. Technical documentation
  - リアルタイム推論用のAPIの仕様やMLシステムのアーキテクチャ設計を文書化し、常に最新の状態に保ちましょう、みたいな話。

### セクション2: Traceability(=) and reproducibility(再現性)

(Traceability: 開発に関する情報や成果物の履歴、所在を追跡できること?:thinking:)

#### 2.1. Infrastructure traceability and reproducibility

- インフラをコード(i.e. IaC)として定義し、バージョン管理しましょう。インフラをリリースする為のCDパイプラインを用意して継続的にリリースできる状態にしましょう。MLプロジェクトは少なくとも2つの環境(pre-productionとproduction)を用意し、どの環境も本番データへのアクセス権(read and/or write)を持たせましょう、みたいな話。
  - pre-production環境(i.e. dev環境?)でも本番のデータを使って学習できたらいいよなぁ...でもwrite権限を与えるのは怖い気がする...?:thinking:

#### 2.2. ML code traceability and reproducibility

- 学習・推論用データの取得、前処理、MLモデルの学習・推論のためのコードをバージョン管理し、CDパイプラインを用意して継続的にリリースできる状態にしましょう。MLモデルの実行環境をコードとして定義し、再現性を保ちましょう。必要に応じて、以前のバージョンのMLモデルにrollbackできるようにしましょう。ある1つのMLモデルの実行/デプロイについて、使用されたコード・実行環境・入出力データなどを一義的に調べることができるようにしておきましょう、みたいな話。

### セクション3: Code Quality(コード品質)

#### 3.1. インフラのコード品質

- IaC変更のPR作成時にconfigファイルの検証や自動テスト等のCIパイプラインがちゃんと実行されるか、とかの話。

#### 3.2. MLモデルのコード品質

- MLモデルのコードがcommitされる前に Pre-commit hookによってコード品質ガイドラインに従っている事を確認しましょう。学習データの前処理、学習、推論APIなど、MLモデルの全てのプロセスのテストを用意しましょう。CIパイプライン用意しましょう。リアルタイム推論用のAPIは、負荷テストなどを行いレイテンシー要件を満たしていることを確認できるようにしましょう。MLモデルコードの新しいリリースがあるたびにリリースノートを作りましょう、みたいな話。
  - Pre-commit hook: commitが実行される前にコードの品質チェックを行う仕組み、らしい。formatterとかlinterとかの話??:thinking:
  - MLモデルの学習・推論はどんなテストによって品質を保証すべきなんだろ。まあ学習は「損失関数がちゃんと減少してるか」とか? 推論は応答分布分析とか?:thinking:
    - (2023/11のMLOps勉強会で、メタモルフィックテスティングとか紹介されていた...!)
  - MLモデルコードの新しいリリースがあるたびにリリースノートを作る、なるほど...!:thinking:

### セクション4: Monitoring & Support

#### 4.1. Infrastructure monitoring requirements(インフラのモニタリング要件)

- インフラコストをtrackingし、定期的にMLプロジェクトのコスト見積もりを行いましょう。インフラリソースの健康状態を監視し、問題が発生した場合に備えて、アラートを設定しましょう、みたいな話。
  - どっちも大事だ...!:thinking:

#### 4.2. Application monitoring requirements(アプリケーションのモニタリング要件)

- リアルタイム推論のusecaseでは、全てのAPIリクエストとレスポンスをログに記録し、APIの応答時間、レスポンスコード、ヘルスステータスを監視しましょう。バッチ推論のusecaseの場合、ターゲットシステムへの継続性を監視しましょう、みたいな話。
  - 後者の話は、batch推論の結果が後続のシステム(DBとか推論サーバ上のキャッシュとか)へ想定通りに渡す事ができているか、って話かな:thinking:

#### 4.3. KPI & model performance monitoring requirements(KPIとMLモデル性能のモニタリング要件)

- オフライン評価指標を保存し、監視しましょう(batch学習 & online学習が走るたびに??:thinking:)。KPIを常に評価・監視しましょう、みたいな話。

#### 4.4. Data drift & Outliers monitoring (データの乖離と異常値のモニタリング)

- 重要な特徴量の分布は定期的に再計算・監視し、モデル出力値に影響を与え得る分布の重大な変化が検出された場合はアラートが出るようにしよう。MLモデルの推論結果の品質が低下した際に異常値検出できるようにしよう、みたいな話。
  - MLモデルの推論結果の異常値検出、応答分布分析とか?:thinking:

### セクション5: Data transformation pipelines & Feature store

- 特徴量は、Feature storeで管理するなどして、異なるプロジェクト間で共有可能にしましょう。学習・推論データの前処理(i.e. データ変換)プロセスは共通化して同じ変換処理が走る事を保証しましょう。特徴量の設定はコードから分離しましょう(=ハードコーディングするなって話?:thinking:)、などの話。

### セクション6: Model Explainability

- MLモデルの説明可能性の話。MLシステムの出力結果の理由を、そのユーザが理解できるようになれば価値があるよね。あと、MLシステムは学習した知識の範囲内で動作し、もし知識の範囲外で動作している時はそれを検知できるようにしましょう、みたいな話。
  - (めちゃ難しそう...!:thinking:)

### セクション7: A/B testing & feedback loop

- MLモデルの入力と出力は自動的に保存されるようにしましょう。A/Bテストを定期的に行いましょう。A/Bテストを行う際は、実験全体を通して、同じユーザが同じバージョンのMLモデルに基づいてサービスを受ける事を保証しましょう、みたいな話。
  - 最後の話は、ユーザ単位でABテストしようね、それより細かい単位はダメって意味? もしくは単に、A/Bテスト後の評価の為にちゃんと実験管理しようね、みたいな意味かな??:thinking:

## 次に読むべき論文は？

- 同じく2023/10のMLOps勉強会の発表にて引用されていた、[FTI(Feature/Training/Inference) Pipelines architectureのブログ](https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines)とか?[RecSysOps](https://netflixtechblog.medium.com/recsysops-best-practices-for-operating-a-large-scale-recommender-system-95bbe195a841)のブログとか?
