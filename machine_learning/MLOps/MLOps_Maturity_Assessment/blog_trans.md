## 0.1. link リンク

https://mlops.community/mlops-maturity-assessment/
https://mlops.community/mlops-maturity-assessment/

## 0.2. title: MLOps Maturity Assessment MLOps成熟度評価

As more and more companies rely on machine learning to run their daily operations, it’s becoming important to adopt MLOps best practices.
日々の業務を機械学習に頼る企業が増えるにつれ、MLOpsのベストプラクティスを採用することが重要になっている。
However, it can be hard to find structured information on what those best practices actually are and how a company can become more mature in terms of MLOps if they decide to start on that journey.
しかし、そうしたベストプラクティスが実際にどのようなものなのか、また、企業がMLOpsの旅に出ようと決めた場合、どのようにすればMLOpsをより成熟させることができるのかについて、構造化された情報を見つけるのは難しいかもしれない。

![](https://mlops.community/wp-content/uploads/2023/04/image-4.png)

Microsoft’s MLOps maturity model or Google’s definition of MLOps levels is a good start, but they don’t necessarily offer actionable insights on how a project can go from being MLOps immature to achieving 100% MLOps maturity.
マイクロソフトの**MLOps maturity(成熟度) model**やグーグルの**MLOps levels**の定義は良いスタートだが、プロジェクトがMLOpsの未成熟な状態から100％のMLOps成熟度を達成する方法について、必ずしも実用的な洞察を提供してくれるわけではない。(maturityの度合いはわかるが、じゃあどのように高める事ができるのって話か:thinking:)
That’s why we decided to create a questionnaire that can help evaluate MLOps maturity on a project level.
そこで、プロジェクト・レベルでMLOpsの成熟度を評価するのに役立つアンケートを作成することにした。
Our questionnaire covers a wide range of MLOps aspects, making it a valuable resource for teams looking to improve their MLOps practices.
当社のアンケートはMLOpsの幅広い側面をカバーしており、MLOpsの実践を改善したいと考えているチームにとって貴重な資料となっている。

1. Documentation ドキュメンテーション

2. Traceability & Reproducibility トレーサビリティと再現性

3. Code quality コードの品質

4. Monitoring & Support モニタリング＆サポート

5. Data transformation pipelines & Feature store データ変換パイプラインとフィーチャーストア

6. Model explainability モデルの説明可能性

7. A/B testing & Feedback loop A/Bテストとフィードバック・ループ

We believe that a machine learning project can be considered MLOps mature if all statements in sections 1–4 (documentation, traceability & reproducibility, code quality, monitoring & support) can be answered with “yes”.
**セクション1-4（文書化、トレーサビリティと再現性、コード品質、モニタリングとサポート）のすべての記述に「はい」と答えることができれば**、機械学習プロジェクトはMLOpsとして成熟しているとみなすことができると考えている。
This is the bare minimum required to deploy a machine learning project reliably in production.
これは、機械学習プロジェクトを本番環境で確実にデプロイするために必要な最低限のものである。
Sections 5–7 go beyond basic MLOps maturity, and it is possible to work on its implementation while some of the statements in sections 1–4 haven’t been covered.
セクション5-7は、基本的なMLOpsの成熟度を超えており、セクション1-4の記述の一部がカバーされていない間に、その実装に取り組むことは可能である。
However, we encourage everyone to prioritize the basics before moving on to advanced MLOps practices.
しかし、高度なMLOpsの実践に移る前に、基本(条件1~4か...:thinking:)を優先することを皆さんにお勧めします。

This questionnaire makes MLOps actionable by clearly highlighting areas for improvement: If some of the statements are answered with a “no,” it’s a clear indicator of what needs to be addressed to improve your MLOps maturity.
このアンケートは、改善すべき領域を明確に示すことで、MLOpsを実行可能なものにします：
記述のいくつかが「いいえ」で答えられた場合、MLOpsの成熟度を向上させるために取り組むべきことが明確に示されます。

# 1. Documentation ドキュメント

## 1.1. Project Documentation プロジェクト・ドキュメンテーション

1. Business goals and KPIs of an ML project are documented and kept up to date. MLプロジェクトのビジネスゴールとKPIは文書化され、常に最新の状態に保たれる。

2. Overview of all team members involved in a machine learning project including their responsibilities are created and kept up to date. 機械学習プロジェクトに関与するすべてのチームメンバーの概要（各自の責任も含む）を作成し、常に最新の状態に保つ。

3. ML model risk evaluation is created, documented, and kept up to date. MLモデルのリスク評価を作成し、文書化し、最新の状態に保つ。

## 1.2. ML model documentation MLモデルのドキュメント

1. Steps of gathering, analyzing, and cleaning data including motivation for each step should be documented. データの収集、分析、クリーニングのステップは、各ステップの動機を含めて文書化されるべきである。

2. Data definition (what features are used in an ML model and what these features mean) is documented. データ定義(MLモデルでどのような特徴量が使われ、その特徴量が何を意味するのか)が文書化されている。

3. Choice of machine learning model is documented and justified. 機械学習モデルの選択が文書化され、正当性が証明されている。

## 1.3. Technical documentation 技術文書

1. For real time inference use cases, API is documented: request & response structure and definition, data types. リアルタイム推論のユースケースのために、APIは文書化されている：リクエストとレスポンスの構造と定義、データ型。

2. Software architecture design is documented and kept up to date. ソフトウェア・アーキテクチャ設計は文書化され、常に最新の状態に保たれている。

# 2. Traceability and reproducibility トレーサビリティと再現性

## 2.1. Infrastructure traceability and reproducibility インフラストラクチャーのトレーサビリティと再現性

1. Infrastructure is defined as code, later referenced as IaC. インフラはコードと定義され、後にIaCと呼ばれる。

2. IaC is stored in a version control system. IaCはバージョン管理システムに保存される。

3. Pull request process is used to create changes in IaC. プル・リクエスト・プロセスは、IaCに変更を加えるために使用される。

4. When pull request is merged, changes will be automatically applied to corresponding environments through a CD pipeline. **プルリクエストがマージされると、CDパイプラインを通じて変更が対応する環境に自動的に適用され**ます。

5. Only CD pipelines can deploy changes, individual developers do not have rights to deploy infrastructure. 変更をデプロイできるのはCDパイプラインだけで、個々の開発者はインフラをデプロイする権限を持っていない。(ふむふむ...!)

6. ML projects should have at least two environments (preproduction and production) which are exact copies of each other. MLプロジェクトは、少なくとも2つの環境(preproductionとproduction)を持つべきです。(pre-production = dev環境って見做して良いんだろうか??:thinking:)

7. All environments related to a ML project should have (read and/or write) access to production data (data should be the same at any moment of time). MLプロジェクトに関連するすべての環境は、本番データ(データはどの時点でも同じであるべき)への(読み書き可能な)アクセス権を持っていなければならない。(そりゃそうではない??:thinking:)

## 2.2. ML code traceability and reproducibility

1. Code for gathering, analyzing, and cleaning data should be stored in a version control system. データを収集、分析、クリーニングするためのコードは、バージョン管理システムに保存されるべきである。

2. ML model code is stored in the version control system, together with data preparation code and API code (if applicable). MLモデルコードは、データ準備コードやAPIコード（該当する場合）とともに、バージョン管理システムに保存されます。

3. Pull requests (PR) are used to make changes in any code related to an ML project. プルリクエスト(PR)は、MLプロジェクトに関連するコードを変更するために使われます。

4. When PR is merged, changes will be automatically applied to corresponding environments through a CD pipeline. PRがマージされると、CDパイプラインを通じて変更が対応する環境に自動的に適用されます。(うんうん...!!:thinking:)

5. Environment is defined as code and is reproducible. 環境はコードとして定義され、再現可能である。(うんうん...!)

6. ML model code should not require changes to run in different environments. The processes of deployment of an ML model to all environments should be the same. MLモデルのコードは、異なる環境で実行するために変更を必要とすべきではない。 MLモデルをすべての環境に展開するプロセスは同じであるべきだ。

7. For any given machine learning model run/deployment in any environment it is possible to look up unambiguously: 1. corresponding code/ commit on git, 2. infrastructure used for training and serving, 3. environment used for training and serving, 4. ML model artifacts, 5. what data was used to train the model. どのような環境でも、与えられた機械学習モデルの実行／展開について、**一義的に調べることが可能である**(ふむふむ): 1. 対応するコード/git上のコミット、2. トレーニングや給仕に使われるインフラ、3. トレーニングや給仕に使用される環境、4. MLモデルの成果物、5. どのようなデータがモデルの訓練に使われたのか。

8. ML model retraining strategy is present and motivated. MLモデルの再トレーニング戦略(=たぶんモデルのオンライン更新ってこと?:thinking:)が存在し、その動機付けがある(?)

9. Roll-back strategy is present to be able to revert to the previous ML model version. ロールバック戦略により、以前のMLモデルのバージョンに戻すことができる。(なるほど...)

# 3. Code Quality コード・クオリティ

## 3.1. Infrastructure code quality requirements インフラコードの品質要件

1. CI pipeline that includes configuration files validation and running automated tests is triggered at pull request creation. 設定ファイルの検証や自動テストの実行を含むCIパイプラインは、プルリクエスト作成時にトリガーされる。(うんうんやりたい...!)

2. Other team members (e.g., developers / security specialists) must review and approve changes before merging a pull request. プルリクエストをマージする前に、他のチームメンバー（開発者やセキュリティスペシャリストなど）が変更をレビューし、承認する必要があります。(うんうん...!)

## 3.2. ML model code quality requirements MLモデルコードの品質要件

1. Pre-commit hooks are implemented to ensure that code follows the code quality guidelines before it is pushed to a version control system. **Pre-commit hook**(=commitが実行される前にコードの品質チェックを行う仕組み、らしい:thinking:)は、コードがバージョン管理システムにプッシュされる前に、コード品質ガイドラインに従っていることを確認するために実装されている。

2. ML model code contains tests for all steps in an ML process (data processing, ML model training, API deployment). MLモデルのコードには、MLプロセスのすべてのステップ（データ処理、MLモデルのトレーニング、APIのデプロイ）のテストが含まれています。(学習はどんなテストを用意すべきなんだろう...)

3. CI pipeline that includes running automated tests is triggered at pull request creation. 自動テストの実行を含むCIパイプラインは、プルリクエスト作成時にトリガーされる。

4. Other team members (for example, developers/ security specialists) must approve changes before merging a pull request. プルリクエストをマージする前に、他のチームメンバー（例えば、開発者やセキュリティスペシャリスト）が変更を承認する必要があります。

5. For real time inference use cases, strategy should be present to perform API load and stress tests regularly and make sure API meets latency requirements. リアルタイムの推論ユースケースでは、APIの負荷テストとストレステストを定期的に実施し、**APIがレイテンシー要件を満たしていることを確認する戦略**が必要である。

6. For real time inference use cases, authentication and networking should follow security guidelines. リアルタイム推論のユースケースでは、認証とネットワークはセキュリティガイドラインに従うべきである。

7. ML model code should be documented (documentation as code). MLモデルのコードは文書化されるべきである(コードとしての文書化)。(あ、自然言語かと思った...!:thinking:)

8. Release notes should be created every time there is a new release of an ML model code. リリースノートは、MLモデルコードの新しいリリースがあるたびに作成されるべきです。(なるほど...!)

# 4. Monitoring & Support モニタリング＆サポート

## 4.1. Infrastructure monitoring requirements インフラモニタリングの要件

1. Tracking of infrastructure costs is set up; cost estimation is done regularly for an ML project. インフラ・コストのトラッキングが設定され、**MLプロジェクトでは定期的にコスト見積もり**が行われる。(大事...!)

2. Health of infrastructure resources is monitored. Alerting is set up in case problems occur. インフラ資源の健全性を監視する。**問題が発生した場合に備えて、アラートが設定**されている。

## 4.2. Application monitoring requirements アプリケーション監視の要件

1. For real-time inference use cases, all API requests and responses should be logged, API response time, response codes, and health status should be monitored. リアルタイムの推論ユースケースの場合、すべてのAPIリクエストとレスポンスがログに記録され、APIのレスポンスタイム、レスポンスコード、ヘルスステータスが監視されるべきである。

2. For batch use cases, continuity of delivery to the target system should be monitored. バッチのユースケースの場合、ターゲットシステムへの配信の継続性を監視する必要がある。(??)

## 4.3. KPI & model performance monitoring requirements KPIとモデル・パフォーマンス・モニタリングの要件

1. Offline evaluation metrics (for example, F1 score computed on historical data for classification tasks) is stored and monitored. オフラインの評価指標（例えば、分類タスクの過去のデータで計算されたF1スコア）が保存され、監視される。

2. Feedback loop is used to evaluate and constantly monitor KPIs that were defined together with the business stakeholders for this ML project. フィードバック・ループは、このMLプロジェクトのためにビジネス利害関係者とともに定義されたKPIを評価し、常に監視するために使用される。

## 4.4. Data drift & Outliers monitoring データ・ドリフトと異常値のモニタリング

1. Distributions of important model features are recalculated on a regular basis, alerts are created if a significant change in distribution that affects the target is detected. 重要なモデルの特徴量の分布は定期的に再計算され、ターゲットに影響を与える**分布の重大な変化が検出された場合はアラートが作成される**。

2. Outlier detection is set up, cases when machine learning models are returning predictions with low certainty are regularly reviewed. 異常値検出が設定されており、機械学習モデルが確実性の低い予測を返す場合は、定期的に見直される。(=ex. 応答分布分析...!:thinking:)

# 5. Data transformation pipelines & Feature store データ変換パイプラインとフィーチャーストア

1. Features are pre-computed in a Feature store and/or imported as code shareable across projects. 特徴量は、feature store(?)で事前に計算されるか、プロジェクト間で共有可能なコードとしてインポートされる。(csvやjsonとかでって事かな。)

2. The offline training data and online prediction data is transformed with the same code. オフラインのトレーニングデータとオンラインの予測データは同じコードで変換される。

3. All the model features are sourced from the feature store or external libraries. すべてのモデル特徴量は、feature storeまたは外部ライブラリから取得されます。

4. Data scientist can add features to the feature store with a PR. データサイエンティストはPRでfeature storeに特徴量を追加できる。

5. Feature dependency is automatically managed by the feature store. フィーチャー依存性は、フィーチャーストアが自動的に管理する。

6. The feature store keeps track of the feature usage per model. feature storeは、モデルごとの特徴量の使用量を記録している。(??)

7. The feature configuration is separated from its code. 特徴量configuration(??)はコードから分離されている。(=たぶんハードコーディングされないべきって事??:thinking:)

# 6. Model Explainability モデルの説明可能性

1. The AI system is capable of providing an explanation for its outputs, with evidence to support the explanation. AIシステムは、その出力を、説明を裏付ける証拠とともに説明することができる。

2. The AI system explanation is meaningful if a user of the system can understand the explanation. AIシステムの説明は、システムの利用者がその説明を理解できれば意味がある。

3. The AI system is able to clearly describe how it arrived at its decision outputs. AIシステムは、どのようにしてその判断結果に至ったかを明確に説明することができる。

4. The AI system operates within its knowledge limits and knows when it is operating outside of those limits. AIシステムは、その知識の限界の範囲内で作動し、その限界の範囲外で作動しているときはそれを知っている。

# 7. A/B testing & feedback loop A/Bテストとフィードバック・ループ

1. The inputs and outputs of the model are stored automatically. モデルの入力と出力は自動的に保存される。

2. A/B testing is performed regularly. A/Bテストは定期的に行われている。

3. When doing A/B testing, it can be guaranteed that the same customer will get predictions based on the same version of the model during the whole experiment. A/Bテストを行う場合、実験全体を通じて、同じ顧客が同じバージョンのモデルに基づいて予測を得ることが保証される。(ユーザ単位でABテストしろよ、それより細かい単位はダメって意味??:thinking:)
