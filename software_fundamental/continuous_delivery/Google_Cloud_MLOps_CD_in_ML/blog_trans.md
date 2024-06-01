## refs: refs：

https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

# MLOps: Continuous delivery and automation pipelines in machine learning MLOps： 機械学習における継続的デリバリーと自動化パイプライン

This document discusses techniques for implementing and automating continuous integration (CI), continuous delivery (CD), and continuous training (CT) for machine learning (ML) systems.
この文書では、**機械学習（ML）システムの continuous integration (CI)、continuous delivery (CD)、continuous training (CT) を実装し自動化するためのテクニック**について説明します。

Data science and ML are becoming core capabilities for solving complex real-world problems, transforming industries, and delivering value in all domains.
データサイエンスとMLは、現実世界の複雑な問題を解決し、産業を変革し、あらゆる領域で価値を提供するための中核的な能力となりつつある。
Currently, the ingredients for applying effective ML are available to you:
現在、効果的なMLを適用するための材料は入手可能である：

- Large datasets
  大規模データセット
- Inexpensive on-demand compute resources
  **安価なオンデマンド・コンピューティング・リソース**(なるほど、Sagemakerしかり...!:thinking:)
- Specialized accelerators for ML on various cloud platforms
  様々なクラウドプラットフォーム上のMLに特化したアクセラレータ
- Rapid advances in different ML research fields (such as computer vision, natural language understanding, and recommendations AI systems).
  さまざまなML研究分野（コンピュータビジョン、自然言語理解、レコメンデーションAIシステムなど）の急速な進歩。

Therefore, many businesses are investing in their data science teams and ML capabilities to develop predictive models that can deliver business value to their users.
そのため、多くの企業がデータサイエンスチームとML機能に投資し、ユーザーにビジネス価値を提供できる予測モデルを開発している。

This document is for data scientists and ML engineers who want to apply DevOps principles to ML systems (MLOps).
このドキュメントは、DevOpsの原則をMLシステム（MLOps）に適用したいと考えているデータサイエンティストやMLエンジニアのためのものです。
MLOps is an ML engineering culture and practice that aims at unifying ML system development (Dev) and ML system operation (Ops).
MLOpsは、MLシステム開発（Dev）とMLシステム運用（Ops）の一体化を目指すMLエンジニアリングの文化と実践である。
Practicing MLOps means that you advocate for automation and monitoring at all steps of ML system construction, including integration, testing, releasing, deployment and infrastructure management.
**MLOpsを実践するということは、統合、テスト、リリース、デプロイメント、インフラ管理など、MLシステム構築のすべてのステップで自動化と監視を提唱するということ**だ。(MLOpsの実践 = MLシステム構築のすべてのステップでの自動化と監視を提唱すること??:thinking:)

Data scientists can implement and train an ML model with predictive performance on an offline holdout dataset, given relevant training data for their use case.
データサイエンティストは、usecaseに関連するトレーニングデータがあれば、オフラインのホールドアウトデータセットで予測性能の高いMLモデルを実装してトレーニングできる。
However, the real challenge isn't building an ML model, the challenge is building an integrated ML system and to continuously operate it in production.
しかし、**本当の挑戦はNLモデルを構築することではなく、統合されたMLシステムを構築し、それを本番環境で継続的に運用すること**だ。
With the long history of production ML services at Google, we've learned that there can be many pitfalls in operating ML-based systems in production.
グーグルにおける本番環境でのMLサービスの長い歴史の中で、**MLベースのシステムを本番環境で運用する際に多くの落とし穴がある**ことを学びました。
Some of these pitfalls are summarized in Machine Learning: The high-interest credit card of technical debt.
これらの落とし穴のいくつかは、[Machine Learning: The high-interest credit card of technical debt](https://ai.google/research/pubs/pub43146) で要約されています。(技術的負債論文だ! 結局のところ、bebtではなく落とし穴やdifficultyの話な気がしてきた...!:thinking:)

As shown in the following diagram, only a small fraction of a real-world ML system is composed of the ML code.
以下の図に示すように、実際のMLシステムでは、MLコードで構成されるのはごく一部である。
The required surrounding elements are vast and complex.
必要とされる**周囲の要素は膨大で複雑**だ。(自分はここにもっと精通して強くなりたい...!:thinking:)

![figure1]()
Figure 1. Elements for ML systems. Adapted from Hidden Technical Debt in Machine Learning Systems.
図1. MLシステムの要素。[Hidden Technical Debt in Machine Learning Systems](https://ai.google/research/pubs/pub43146) から適応。

In this diagram, the rest of the system is composed of configuration, automation, data collection, data verification, testing and debugging, resource management, model analysis, process and metadata management, serving infrastructure, and monitoring.
この図では、システムの残りの部分は、configuration(設定)、automation(自動化)、data collection(データ収集)、data verification(データ検証)、testing and debugging(テストとデバッグ)、resource management(リソース管理)、model analysis(モデル分析)、process and metadata management(プロセスとメタデータ管理)、serving infrastructure(提供インフラ)、monitoring(モニタリング)で構成されている。(うん、これらの要素には納得感がある...:thinking:)

To develop and operate complex systems like these, you can apply DevOps principles to ML systems (MLOps).
このような複雑なシステムを開発・運用するには、DevOpsの原則をMLシステムに適用すればよい（MLOps）。
This document covers concepts to consider when setting up an MLOps environment for your data science practices, such as CI, CD, and CT in ML.
**このドキュメントでは、CI、CD、CTなどのデータサイエンスプラクティスのためのMLOps環境を設定する際に考慮すべき概念について説明します**。(GCPを使った具体的なsolutionの話じゃなくて良かった...!:thinking:)

The following topics are discussed:
以下のトピックが取り上げられている：

- DevOps versus MLOps
  DevOpsとMLOpsの比較
- Steps for developing ML models
  MLモデル開発のステップ
- MLOps maturity levels
  MLOpsの成熟度レベル

<!-- ここまで読んだ! -->

## DevOps versus MLOps DevOps対MLOps

DevOps is a popular practice in developing and operating large-scale software systems.
DevOpsは、大規模なソフトウェア・システムを開発・運用する際によく使われる手法だ。
This practice provides benefits such as shortening the development cycles, increasing deployment velocity, and dependable releases.
この実践は、開発サイクルの短縮、デプロイ速度の向上、信頼性の高いリリースといったメリットをもたらす。
To achieve these benefits, you introduce two concepts in the software system development:
これらのメリットを実現するために、ソフトウェア・システム開発では**2つの概念を導入**する：

- Continuous Integration (CI, 継続的インテグレーション)
- Continuous Delivery (CD, 継続的デリバリー)
  - (継続的デリバリーは、継続的インテグレーションを包含した概念な気がしてるので、うーむ:thinking:)

An ML system is a software system, so similar practices apply to help guarantee that you can reliably build and operate ML systems at scale.
MLシステムはソフトウェア・システムであるため、同様の手法が適用され、スケールで信頼性の高いMLシステムを構築・運用できるようになる。(MLエンジニアである前にソフトウェアエンジニアである...!:thinking:)

However, ML systems differ from other software systems in the following ways:
**しかし、MLシステムは他のソフトウェアシステムとは以下の点で異なる**:

- **Team skills**: In an ML project, the team usually includes data scientists or ML researchers, who focus on exploratory data analysis, model development, and experimentation.
  チームのスキル： MLプロジェクトでは通常、チームにはデータサイエンティストやML研究者が含まれ、彼らは探索的データ分析、モデル開発、実験に集中する。(**チームのスキル分布が通常のソフトウェア開発チームと異なる、みたいな??**:thinking:)
  These members might not be experienced software engineers who can build production-class services.
  これらのメンバーは、本番クラスのサービスを構築できる経験豊富なソフトウェア・エンジニアではないかもしれない。
- Development: ML is experimental in nature.
  開発： **MLは実験的な性質を持つ**。
  You should try different features, algorithms, modeling techniques, and parameter configurations to find what works best for the problem as quickly as possible.
  さまざまな機能、アルゴリズム、モデリング技術、パラメータ構成を試して、問題に最適なものをできるだけ早く見つける必要がある。
  The challenge is tracking what worked and what didn't, and maintaining reproducibility while maximizing code reusability.
  課題は、**何がうまくいったか、何がうまくいかなかったかを追跡**し、コードの再利用性を最大化しながら再現性を維持することだ。(実験のtrackingか～)
- Testing: Testing an ML system is more involved than testing other software systems.
  テスト： **MLシステムのテストは、他のソフトウェアシステムのテストよりも手間がかかる**。
  In addition to typical unit and integration tests, you need data validation, trained model quality evaluation, and model validation.
  典型的な単体テストと統合テストに加えて、データの検証、学習済みモデルの品質評価、モデルの検証が必要です。(最後のmodel validationは、モデルの品質評価と同じ意味に感じちゃうけど、なんだろう。想定通りの構造になってるかの検証とか??:thinking:)
- Deployment: In ML systems, deployment isn't as simple as deploying an offline-trained ML model as a prediction service.
  デプロイメント： MLシステムでは、オフラインでトレーニングされたMLモデルを予測サービスとしてデプロイするだけでは済まない。
  ML systems can require you to deploy a multi-step pipeline to automatically retrain and deploy model.
  MLシステムでは、**モデルを自動的に再トレーニングしてデプロイするためのマルチステップパイプラインをデプロイする必要がある**。(ex. 学習->学習済みモデルのpackaging-> 推論サーバにデプロイメントとか...??:thinking:)
  This pipeline adds complexity and requires you to automate steps that are manually done before deployment by data scientists to train and validate new models.
  このパイプラインは複雑さを増し、**データサイエンティストが新しいモデルをトレーニングして検証するためにデプロイメント前に手動で行っていたステップを自動化する必要がある**。(確かに...!:thinking:)
- Production: ML models can have reduced performance not only due to suboptimal coding, but also due to constantly evolving data profiles.
  生産： MLモデルは、最適でないコーディングのためだけでなく、**常に進化するデータ・プロファイルのためにパフォーマンスが低下する可能性がある**。(MLシステムは、外の世界と相互作用する特徴を持つから??debt論文でも主張されてた!!:thinking:)
  In other words, models can decay in more ways than conventional software systems, and you need to consider this degradation.
  **言い換えれば、モデルは従来のソフトウェアシステムよりも多くの方法で劣化する可能性があり、この劣化を考慮する必要がある**。(この言い換えが解釈しやすくて好き...!:thinking:)
  Therefore, you need to track summary statistics of your data and monitor the online performance of your model to send notifications or roll back when values deviate from your expectations.
  したがって、データの要約統計を追跡し、モデルのオンラインパフォーマンスを監視して、値が期待値から逸脱した場合に通知を送ったり、ロールバックしたりする必要がある。

ML and other software systems are similar in continuous integration of source control, unit testing, integration testing, and continuous delivery of the software module or the package.
MLと他のソフトウェアシステムは、ソースコントロールの継続的インテグレーション(=ソースコードの管理??:thinking:)、単体テスト、統合テスト、ソフトウェアモジュールやパッケージの継続的デリバリーにおいて類似している。
However, in ML, there are a few notable differences:
しかし、MLではいくつかの顕著な違いがある:

- CI is no longer only about testing and validating code and components, but also testing and validating data, data schemas, and models.
  CIはもはや、コードやコンポーネントのテストと検証だけでなく、データ、データスキーマ、モデルのテストと検証も含んでいる。
- CD is no longer about a single software package or a service, but a system (an ML training pipeline) that should automatically deploy another service (model prediction service).
  CDは、もはや単一のソフトウェアパッケージやサービスのことではなく、別のサービス(モデル予測サービス)を自動的にデプロイするシステム(MLトレーニングパイプライン)のことである。
  (Training pipelineを実行したら、prediction serviceに新しいendpointが追加される、みたいな感じ?? もしくはAPIのparameterで指定できるmodelの種類が追加されるみたいな感じかな:thinking:)
- CT is a new property, unique to ML systems, that's concerned with automatically retraining and serving the models.
  **CTは、MLシステム特有の新しい特性で、モデルを自動的に再トレーニングして提供することに関係している**。(モデルの性能低下を検知して、再トレーニング、みたいな事だよね。もしくはschedulingされたバッチでもいいし:thinking:)

<!-- ここまで読んだ! -->

The following section discusses the typical steps for training and evaluating an ML model to serve as a prediction service.
以下のセクションでは、prediction service (=推論API?)として機能するMLモデルをトレーニングして評価するための典型的なステップについて説明します。

## Data science steps for ML MLのためのデータサイエンスのステップ

In any ML project, after you define the business use case and establish the success criteria, the process of delivering an ML model to production involves the following steps.
どのようなMLプロジェクトにおいても、ビジネスユースケースを定義し、成功基準を確立した後、MLモデルを本番環境に提供するプロセスには以下のステップが含まれる。
These steps can be completed manually or can be completed by an automatic pipeline.
これらのステップは、手動で完了させることもできるし、自動パイプラインで完了させることもできる:

1. **Data extraction**: You select and integrate the relevant data from various data sources for the ML task.
   データ抽出： MLタスクのために、様々なデータソースから関連するデータを選択し、統合する。
2. **Data analysis**: You perform exploratory data analysis (EDA) to understand the available data for building the ML model.
   データ分析： MLモデルを構築するために利用可能なデータを理解するために、探索的データ分析（EDA）を行う。
   This process leads to the following:
   このプロセスは次のような結果をもたらす：
   - Understanding the data schema and characteristics that are expected by the model.
     モデルが期待するデータスキーマと特性を理解する。(data schema = データ構造、とみなして良さそう。)
   - Identifying the data preparation and feature engineering that are needed for the model.
     モデルに必要なデータ準備とフィーチャーエンジニアリングを特定する。
3. **Data preparation**: The data is prepared for the ML task.
   データの準備： データはMLタスクのために準備される。
   This preparation involves data cleaning, where you split the data into training, validation, and test sets.
   この準備には、データをトレーニングセット、検証セット、テストセットに分けるデータクリーニングが含まれる。
   You also apply data transformations and feature engineering to the model that solves the target task.
   また、対象のタスクを解決するモデルに、データ変換とフィーチャーエンジニアリングを適用する。
   The output of this step are the data splits in the prepared format.
   このステップの出力は、準備されたフォーマットでのデータ分割である。
4. **Model training**: The data scientist implements different algorithms with the prepared data to train various ML models.
   モデルのトレーニング： データサイエンティストは、様々なMLモデルを訓練するために、準備されたデータを使って様々なアルゴリズムを実装する。
   In addition, you subject the implemented algorithms to hyperparameter tuning to get the best performing ML model.
   さらに、実装されたアルゴリズムをハイパーパラメータ・チューニングにかけることで、最高のパフォーマンスを持つMLモデルを得ることができます。
   The output of this step is a trained model.
   このステップの出力は学習済みモデルである。
5. **Model evaluation**: The model is evaluated on a holdout test set to evaluate the model quality.
   モデルの評価： モデルの品質を評価するために、ホールドアウトテストセットでモデルを評価する。
   The output of this step is a set of metrics to assess the quality of the model.
   このステップの出力は、モデルの品質を評価するための一連のメトリクスである。
6. **Model validation**: The model is confirmed to be adequate for deployment—that its predictive performance is better than a certain baseline.
   モデルの検証： モデルがデプロイメントに適していることが確認される。つまり、その予測性能がある基準よりも優れていることが確認される。(評価した結果からvalidationするってことね:thinking:)
7. **Model serving**: The validated model is deployed to a target environment to serve predictions.
   モデルの提供： 検証されたモデルは、ターゲット環境に配備され、予測を提供する。
   This deployment can be one of the following:
   **このデプロイは以下のいずれかになる**：
   - Microservices with a REST API to serve online predictions.
     オンライン予測を提供するREST APIを備えたマイクロサービス。
   - An embedded model to an edge or mobile device.
     エッジデバイスやモバイルデバイスへの組み込みモデル。
   - Part of a batch prediction system.
     batch predictionシステムの一部。
8. **Model monitoring**: The model predictive performance is monitored to potentially invoke a new iteration in the ML process.
   モデルのモニタリング： モデルの予測性能は、MLプロセスの新しいイテレーションを呼び起こす可能性があるため、モニタリングされる。(i.e. モデルの性能低下やデータの特性のdriftが検知された場合には、それをtriggerとしてモデルの再学習が実行される、みたいな感じっぽい:thinking:)

The level of automation of these steps defines the maturity of the ML process, which reflects the velocity of training new models given new data or training new models given new implementations.
**これらのステップの自動化のレベルは、MLプロセスの成熟度を定義する**。そしてそれは、新しいデータを与えられた場合の新しいモデルのトレーニングの速度や、新しい実装を与えられた場合の新しいモデルのトレーニングの速度を反映している。
The following sections describe three levels of MLOps, starting from the most common level, which involves no automation, up to automating both ML and CI/CD pipelines.
以下のセクションでは、自動化を伴わない最も一般的なレベルから、MLとCI/CDパイプラインの両方を自動化するレベルまで、**MLOpsの(成熟度の)3つのレベルについて**説明する。

<!-- ここまで読んだ! -->

## MLOps level 0: Manual process MLOps レベル 0： 手動プロセス

Many teams have data scientists and ML researchers who can build state-of-the-art models, but their process for building and deploying ML models is entirely manual.
多くのチームには、最先端のモデルを構築できるデータサイエンティストやML研究者がいるが、**MLモデルの構築とデプロイのプロセスはすべて手作業**だ。
This is considered the basic level of maturity, or level 0.
これは成熟度の基本レベル、つまりレベル0とみなされる。
The following diagram shows the workflow of this process.
次の図は、このプロセスのワークフローを示している。

![figure2]()
Figure 2. Manual ML steps to serve the model as a prediction service.
図2. モデルを予測サービスとして提供するための手動MLステップ。

### Characteristics 特徴

The following list highlights the characteristics of the MLOps level 0 process, as shown in Figure 2:
以下のリストは、図2に示すMLOpsレベル0プロセスの特徴を強調したものである：

- **Manual, script-driven, and interactive process**: Every step is manual, including data analysis, data preparation, model training, and validation.
  手動、スクリプト駆動、対話型プロセス： データ分析、データ準備、モデルのトレーニング、検証など、すべてのステップが手動で行われる。
  It requires manual execution of each step, and manual transition from one step to another.
  各ステップを手動で実行し、あるステップから別のステップへ手動で移行する必要がある。
  This process is usually driven by experimental code that is written and executed in notebooks by data scientist interactively, until a workable model is produced.
  このプロセスは通常、データサイエンティストがノートブックで書かれ、実行される実験コードによって駆動され、作業可能なモデルが生成されるまで対話的に行われる。
- **Disconnection between ML and operations**: The process separates data scientists who create the model and engineers who serve the model as a prediction service.
  MLと運用の断絶： このプロセスでは、**モデルを作成するデータサイエンティストと、predictionサービスとしてモデルを提供するエンジニアが分離している**。
  The data scientists hand over a trained model as an artifact to the engineering team to deploy on their API infrastructure.
  データサイエンティストは、学習済みのモデルを成果物としてエンジニアリングチームに渡し、APIインフラにデプロイしてもらう。
  This handoff can include putting the trained model in a storage location, checking the model object into a code repository, or uploading it to a models registry.
  この引き渡しには、学習済みモデルをストレージ場所に配置したり、モデルオブジェクトをコードリポジトリにチェックインしたり、モデルレジストリにアップロードしたりすることが含まれる。
  Then engineers who deploy the model need to make the required features available in production for low-latency serving, which can lead to training-serving skew.
  そうなると、モデルをデプロイするエンジニアは、低レイテンシーの提供のために本番環境で必要な特徴量を利用可能にする必要があり、[training-serving skew](https://developers.google.com/machine-learning/guides/rules-of-ml/#training-serving_skew)につながる可能性がある。(=training時とserving時における性能の差)
- **Infrequent release iterations**: The process assumes that your data science team manages a few models that don't change frequently—either changing model implementation or retraining the model with new data.
  頻繁にリリースを繰り返さない： このプロセスは、データサイエンスチームが、モデルの実装を変更したり、新しいデータでモデルを再トレーニングしたりするような、頻繁に変更されない少数のモデルを管理していることを想定している。
  A new model version is deployed only a couple of times per year.
  **新バージョンの投入は年に2、3回しかない。**
- **No CI**: Because few implementation changes are assumed, CI is ignored.
  CIなし： 実装の変更がほとんど想定されないため、**CIは無視される**。(自動テスト的なことを意味してる??:thinking:)
  Usually, testing the code is part of the notebooks or script execution.
  通常、コードのテストはノートブックやスクリプトの実行の一部である。
  The scripts and notebooks that implement the experiment steps are source controlled, and they produce artifacts such as trained models, evaluation metrics, and visualizations.
  実験ステップを実装するスクリプトやノートブックはソースコントロールされ(i.e. バージョン管理され?)、学習済みモデル、評価メトリクス、視覚化などの成果物を生成する。
- **No CD**: Because there aren't frequent model version deployments, CD isn't considered.
  CDはない： モデル・バージョンの頻繁なデプロイはないため、CDは考慮されない。(自動デプロイもないってこと??:thinking:)
- Deployment refers to the prediction service: The process is concerned only with deploying the trained model as a prediction service (for example, a microservice with a REST API), rather than deploying the entire ML system.
  **デプロイメントとは、予測サービスのことである**： このプロセスは、MLシステム全体をデプロイするのではなく、学習済みモデルを予測サービス(ex. REST APIを持つマイクロサービス)としてデプロイすることに関心がある。(=CT pipelineをデプロイするのではなく、マニュアルで作ったモデルを推論サーバにデプロイする、みたいな事??:thinking:)
- Lack of active performance monitoring: The process doesn't track or log the model predictions and actions, which are required in order to detect model performance degradation and other model behavioral drifts.
  **能動的な性能モニタリングの欠如**: このプロセスでは、モデルの予測やアクションを追跡したり、ログに記録したりすることができません。これは、モデルの性能低下やその他のモデルの動作のドリフトを検出するために必要です。

The engineering team might have their own complex setup for API configuration, testing, and deployment, including security, regression, and load and canary testing.
エンジニアリングチームは、セキュリティ、退行、負荷、カナリアテストを含むAPIの設定、テスト、デプロイメントのための複雑なセットアップを持っているかもしれません。
In addition, production deployment of a new version of an ML model usually goes through A/B testing or online experiments before the model is promoted to serve all the prediction request traffic.
さらに、新しいバージョンのMLモデルの本番デプロイメントは、**通常、モデルがすべての予測リクエストトラフィックを提供する前に、A/Bテストやオンライン実験を経て行われます**。(これはいいことな気がする!!:thinking:)

### Challenges 課題

MLOps level 0 is common in many businesses that are beginning to apply ML to their use cases.
MLOpsレベル0は、MLをusecaseに適用し始める多くのビジネスで一般的です。
This manual, data-scientist-driven process might be sufficient when models are rarely changed or trained.
モデルの変更や訓練がめったに行われない場合は、このような**手動のデータサイエンティスト駆動プロセス**で十分かもしれません。
In practice, models often break when they are deployed in the real world.
**実際のところ、モデルは実戦に投入されると壊れてしまうことが多い**。
The models fail to adapt to changes in the dynamics of the environment, or changes in the data that describes the environment.
モデルは、環境のダイナミクスの変化や、環境を記述するデータの変化に適応できないことがあります。
For more information, see Why Machine Learning Models Crash and Burn in Production.
詳しくは、[Why Machine Learning Models Crash and Burn in Production](https://www.forbes.com/sites/forbestechcouncil/2019/04/03/why-machine-learning-models-crash-and-burn-in-production/)を参照してください。

To address these challenges and to maintain your model's accuracy in production, you need to do the following:
このような課題に対処し、**本番でモデルの精度を維持するためには**、以下のことを行う必要があります：

- Actively monitor the quality of your model in production: Monitoring lets you detect performance degradation and model staleness.
  **プロダクションでのモデルの品質を積極的に監視する**： モニタリングにより、パフォーマンスの低下やモデルの陳腐化を検出できます。
  It acts as a cue to a new experimentation iteration and (manual) retraining of the model on new data.
  これは、新たな実験iterationと、新たなデータに対するモデルの(手作業による)再トレーニングへの手がかりとして機能する。
- Frequently retrain your production models: To capture the evolving and emerging patterns, you need to retrain your model with the most recent data.
  **productionモデルを頻繁に再トレーニングする**: 進化するパターンや新興パターンを捉えるためには、最新のデータでモデルを再トレーニングする必要がある。
- Continuously experiment with new implementations to produce the model: To harness the latest ideas and advances in technology, you need to try out new implementations such as feature engineering, model architecture, and hyperparameters.
  モデルを生成するために、**新しい実装で継続的に実験する**： 最新のアイデアや技術の進歩を活用するためには、フィーチャーエンジニアリング、モデルアーキテクチャ、ハイパーパラメータなどの新しい実装を試す必要がある。
  For example, if you use computer vision in face detection, face patterns are fixed, but better new techniques can improve the detection accuracy.
  例えば、顔検出でコンピューター・ビジョンを使用する場合、顔のパターンは固定されているが、より優れた新しい技術によって検出精度を向上させることができる。

To address the challenges of this manual process, MLOps practices for CI/CD and CT are helpful.
この手動プロセスの課題に対処するには、CI/CDとCTのためのMLOpsプラクティスが役に立つ。(=これがlevel 1っぽい。)
By deploying an ML training pipeline, you can enable CT, and you can set up a CI/CD system to rapidly test, build, and deploy new implementations of the ML pipeline.
**ML trainingパイプラインをデプロイする**ことで、CTを可能にし、CI/CDシステムを設定して、MLパイプラインの新しい実装を迅速にテスト、ビルド、デプロイすることができる。
These features are discussed in more detail in the next sections.
これらの特徴については、次のセクションで詳しく説明する。

<!-- ここまで読んだ! -->

## MLOps level 1: ML pipeline automation MLOpsレベル1： MLパイプラインの自動化

The goal of level 1 is to perform continuous training of the model by automating the ML pipeline; this lets you achieve continuous delivery of model prediction service.
レベル1の目標は、**MLパイプラインを自動化することにより、モデルの継続的な学習を行うこと**です。これにより、モデル予測サービスの継続的な提供を実現できます。(CTを達成できてたらlevel 1??)
To automate the process of using new data to retrain models in production, you need to introduce automated data and model validation steps to the pipeline, as well as pipeline triggers and metadata management.
新しいデータを使用して本番でモデルを再トレーニングするプロセスを自動化するには、パイプラインに自動化されたデータとモデルの検証ステップ、パイプライントリガーとメタデータ管理を導入する必要があります。

The following figure is a schematic representation of an automated ML pipeline for CT.
次の図は、CTのための自動化されたMLパイプラインの概略図である。
(あ、GoogleのMLOps Mapじゃん!どこから手を付けていいか分かりづらいやつ...!:thinking:)

![figure3]()
Figure 3. ML pipeline automation for CT.

### Characteristics 特徴

The following list highlights the characteristics of the MLOps level 1 setup, as shown in Figure 3:
以下のリストは、**図3に示すMLOpsレベル1のセットアップの特徴**を強調したものである：

- Rapid experiment: The steps of the ML experiment are orchestrated.
  **迅速な実験**： ML実験のステップはオーケストレーションされる。
  The transition between steps is automated, which leads to rapid iteration of experiments and better readiness to move the whole pipeline to production.
  ステップ間の移行は自動化されており、実験の迅速な反復と、パイプライン全体を本番に移行させる準備の良さにつながっている。
  (もっと迅速にできるように頑張りたい...!:thinking:)
- CT of the model in production: The model is automatically trained in production using fresh data based on live pipeline triggers, which are discussed in the next section.
  **本番環境におけるモデルの CT**： モデルは、次のセクションで説明するライブ・パイプライン・トリガーに基づく新鮮なデータを使用して、本番環境で自動的にトレーニングされる。
- Experimental-operational symmetry: The pipeline implementation that is used in the development or experiment environment is used in the preproduction and production environment, which is a key aspect of MLOps practice for unifying DevOps.
  **実験と運用の対称性**： **開発または実験環境で使用されるパイプラインの実装は、プリプロダクションおよびプロダクション環境でも使用される**。これは、DevOpsを統一するためのMLOpsプラクティスの重要な側面である。
  (これは本当にそう! 以前の recommendation industry talksの懇親会で喋って納得してた話...!:thinking:)
- Modularized code for components and pipelines: To construct ML pipelines, components need to be reusable, composable, and potentially shareable across ML pipelines.
  **コンポーネントとパイプラインのためのモジュール化されたコード**： MLパイプラインを構築するためには、**コンポーネントはreusable(再利用可能)で、composable(=組み合わせ可能)であり、MLパイプライン全体で共有可能である必要がある**。(=pipelineを生やすスピードを高める為にも、各componentのreusable性とcomposable性は必要だよな...!:thinking:)
  Therefore, while the EDA code can still live in notebooks, the source code for components must be modularized.
  そのため、EDAコードはノートブックに残すことができますが、コンポーネントのソースコードはモジュール化されている必要があります。
  In addition, components should ideally be containerized to do the following:
  **さらに、以下の事を満たせるように、コンポーネントは理想的にはコンテナ化されるべき**：
  - Decouple the execution environment from the custom code runtime.
    実行環境をカスタムコードのruntimeから切り離す。(i.e. コードがどの環境でも一貫して動作するようにする?:thinking:)
  - Make code reproducible between development and production environments.
    開発環境と本番環境でコードの再現性を高める。
    (コンテナはコードとその依存関係をpackagingする為、devとprodで同じコンテナを使用することで再現性が高まる?:thinking:)
  - Isolate each component in the pipeline.
    パイプラインの各コンポーネントを分離する。
    Components can have their own version of the runtime environment, and have different languages and libraries.
    **各componentsは独自のバージョンのランタイム環境を持つことができ**、異なる言語やライブラリを持つことができる。(=runtime環境やcomputing resourceをcomponent毎に最適化できる、みたいな??:thinking:)
- Continuous delivery of models: An ML pipeline in production continuously delivers prediction services to new models that are trained on new data.
  **モデルの継続的デリバリー**： 本番稼動中のMLパイプラインは、新しいデータでトレーニングされた新しいモデルに予測サービスを継続的に提供する。(たぶんCT pipelineの後半のstepに、推論APIへのモデルデプロイのstepが含まれている、って話...!:thinking:)
  The model deployment step, which serves the trained and validated model as a prediction service for online predictions, is automated.
  モデルデプロイメントステップは、train & validate されたモデルをオンライン予測用の予測サービスとして提供するために自動化されている。
- Pipeline deployment: In level 0, you deploy a trained model as a prediction service to production.
  パイプラインデプロイメント： レベル0では、トレーニングされたモデルを(マニュアルで)予測サービスとして本番環境にデプロイする。
  For level 1, you deploy a whole training pipeline, which automatically and recurrently runs to serve the trained model as the prediction service.
  レベル1では、**トレーニングパイプライン全体をデプロイし**、自動的に繰り返し実行して、トレーニングされたモデルを予測サービスとして提供する。

<!-- ここまで読んだ! -->

### Additional components 追加コンポーネント

This section discusses the components that you need to add to the architecture to enable ML continuous training.
このセクションでは、**MLのCTを可能にするためにアーキテクチャに追加する必要があるコンポーネント**について説明します。

#### Data and model validation データとモデルの検証

When you deploy your ML pipeline to production, one or more of the triggers discussed in the ML pipeline triggers section automatically executes the pipeline.
MLパイプラインを本番環境にデプロイすると、[MLパイプラインのトリガーセクション](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning#ml_pipeline_triggers)で説明した1つ以上のトリガーが自動的にパイプラインを実行します。
The pipeline expects new, live data to produce a new model version that is trained on the new data (as shown in Figure 3).
パイプラインは、新しいデータでトレーニングされた新しいモデルのバージョンを生成するために、新しいライブデータを期待する（図3に示すように）。
Therefore, automated data validation and model validation steps are required in the production pipeline to ensure the following expected behavior:
したがって、以下のような期待される挙動を保証するために、**自動化されたデータ検証およびモデル検証ステップがプロダクションパイプラインで必要**とされる：

- Data validation: This step is required before model training to decide whether you should retrain the model or stop the execution of the pipeline.
  データ検証： このステップはモデルトレーニングの前に必要で、**モデルを再トレーニングするかパイプラインの実行を停止するかを決定**する。(有効な学習データじゃなければ、pipelineを停止する...!:thinking:)
  This decision is automatically made if the following was identified by the pipeline.
  この決定は、パイプラインによって以下のことが確認された場合に自動的に行われる。
  - Data schema skews: These skews are considered anomalies in the input data, which means that the downstream pipeline steps, including data processing and model training, receives data that doesn't comply with the expected schema.
    **データスキーマ(i.e. データ構造)の歪み**： これらのスキューは入力データの異常とみなされ、データ処理やモデル学習を含む下流のパイプラインステップが、期待されるスキーマに準拠していないデータを受け取ることを意味する。
    In this case, you should stop the pipeline so the data science team can investigate.
    この場合、**データサイエンスチームが調査できるように、パイプラインを止めるべきである**。(うんうん、何かしらバグがあるってことだもんね...!:thinking:)
    The team might release a fix or an update to the pipeline to handle these changes in the schema.
    チームは、スキーマの変更を処理するために、パイプラインの修正やアップデートをリリースするかもしれない。
    Schema skews include receiving unexpected features, not receiving all the expected features, or receiving features with unexpected values.
    スキーマの歪みには、予期せぬ特徴量の受信、期待されるすべての特徴量の受信がない、または予期しない値の特徴量の受信が含まれる。
  - Data values skews: These skews are significant changes in the statistical properties of data, which means that data patterns are changing, and you need to trigger a retraining of the model to capture these changes.
    **データ値の歪み**： これはデータのパターンが変化していることを意味し、これらの変化を捉えるためにモデルの再トレーニングを行う必要があります。(**driftってやつだ、そうか、逆にdriftが発生してなければCT pipelineを早期終了すればいいのか**...!:thinking:)
- Model validation: This step occurs after you successfully train the model given the new data.
  **モデルの検証**： このステップは、新しいデータを使ってモデルの訓練に成功した後に行われる。
  You evaluate and validate the model before it's promoted to production.
  本番稼動前にモデルを評価し、検証する。
  This offline model validation step consists of the following.
  このオフラインのモデル検証ステップは、以下のように構成されている。
  - Producing evaluation metric values using the trained model on a test dataset to assess the model's predictive quality.
    モデルの予測品質を評価するために、テストデータセット上で学習済みモデルを使用して評価指標値を生成する。
  - Comparing the evaluation metric values produced by your newly trained model to the current model, for example, production model, baseline model, or other business-requirement models.
    **新しく学習したモデルによって生成された評価指標値を、現在のモデル（たとえば、生産モデル、ベースラインモデル、または他のビジネス要件モデル）と比較**します。
    You make sure that the new model produces better performance than the current model before promoting it to production.
    新モデルが現行モデルよりも優れたパフォーマンスを発揮することを確認してから、生産に移行する。
  - Making sure that the performance of the model is consistent on various segments of the data.
    モデルの性能がデータの様々なセグメントで一貫していることを確認する。(特定のセグメントに特化したモデルになってないか、を確認する??:thinking:)
    For example, your newly trained customer churn model might produce an overall better predictive accuracy compared to the previous model, but the accuracy values per customer region might have large variance.
    例えば、新しくトレーニングされた顧客解約(customer churn)モデルは、以前のモデルと比較して全体的な予測精度が向上するかもしれませんが、顧客地域ごとの精度値には大きな分散があるかもしれません。
  - Making sure that you test your model for deployment, including infrastructure compatibility and consistency with the prediction service API.
    インフラの互換性や予測サービスAPIとの整合性など、デプロイのためのモデルのテストを確実に行うこと。

In addition to offline model validation, a newly deployed model undergoes online model validation—in a canary deployment or an A/B testing setup—before it serves prediction for the online traffic.
オフラインでのモデル検証に加えて、新しくデプロイされたモデルは、オンライントラフィックの予測を提供する前に、**カナリアデプロイメントまたはA/Bテストのセットアップでオンラインモデル検証を受けます**。
(これは、新しい予測モデルにいきなり全てのtrafficを流さないって事だよね。ABテストなり、rolloutなりで徐々にtrafficを増やしていく方が安全:thinking:)

<!-- ここまで読んだ! -->

#### Feature store 特徴量ストア

An optional additional component for level 1 ML pipeline automation is a feature store.
レベル1のMLパイプライン自動化のための**optionalな追加コンポーネントは、特徴量ストア**です。
A feature store is a centralized repository where you standardize the definition, storage, and access of features for training and serving.
フィーチャーストアは、トレーニングやサービングのためのフィーチャーの定義、保存、アクセスを標準化する一元化されたリポジトリです。
A feature store needs to provide an API for both high-throughput batch serving and low-latency real-time serving for the feature values, and to support both training and serving workloads.
特徴量ストアは、特徴量の値に対して**高スループットのバッチサービングと低遅延のリアルタイムサービングの両方のAPIを提供**し、トレーニングとサービングのワークロードの両方をサポートする必要があります。(あ、これがfeature storeが持つべき特徴の1つかも...!:thinking:)

The feature store helps data scientists do the following:
フィーチャーストアは、データサイエンティストが以下のことを行うのに役立つ:

- Discover and reuse available feature sets for their entities, instead of re-creating the same or similar ones. 
  - 同じもしくは類似のものを再作成するのではなく、entities(=複数のMLモデル?)に利用可能な特徴量集合を発見し、再利用する。
- Avoid having similar features that have different definitions by maintaining features and their related metadata.
  - 特徴量とその関連メタデータを維持することで、異なる定義を持つ類似の特徴量を持たないようにする。(**車輪の再発明を防ぐ**、みたいな...!:thinking:)
- Serve up-to-date feature values from the feature store.
  - フィーチャーストアから最新の特徴量の値を提供する。
- Avoid training-serving skew by using the feature store as the data source for experimentation, continuous training, and online serving. 実験、継続的なトレーニング、オンラインサービングのデータソースとしてフィーチャーストアを使用することで、**training-serving skew (トレーニングとサービングのズレ)を回避**する。 This approach makes sure that the features used for training are the same ones used during serving: このアプローチは、トレーニングに使用される特徴量がサービング中に使用されるものと同じであることを保証する:
  - For experimentation, data scientists can get an offline extract from the feature store to run their experiments. 実験のために、データサイエンティストは、実験を実行するためにフィーチャーストアからオフライン抽出を取得できる。
  - For continuous training, the automated ML training pipeline can fetch a batch of the up-to-date feature values of the dataset that are used for the training task. 継続的なトレーニングの場合、自動化されたMLトレーニングパイプラインは、トレーニングタスクに使用されるデータセットの最新の特徴量値のバッチを取得できる。
  - For online prediction, the prediction service can fetch in a batch of the feature values related to the requested entity, such as customer demographic features, product features, and current session aggregation features. オンライン予測の場合、予測サービスは、リクエストされたエンティティに関連する特徴量のバッチを取得できる。たとえば、顧客の人口統計特徴、製品特徴、および現在のセッション集約特徴など。

<!-- ここまで読んだ! -->

#### Metadata management メタデータ管理

Information about each execution of the ML pipeline is recorded in order to help with data and artifacts lineage, reproducibility, and comparisons.
MLパイプラインの各実行に関する情報は、**データと成果物の系譜、再現性、比較を支援するために記録されます**。
It also helps you debug errors and anomalies.
また、エラーや異常のデバッグにも役立つ。
Each time you execute the pipeline, the ML metadata store records the following metadata:
**パイプラインを実行するたびに、MLメタデータストアは以下のメタデータを記録します**：
(実験だけじゃなくて、定期実行をtrackingする...!:thinking:)

- The pipeline and component versions that were executed.  実行されたパイプラインとコンポーネントのバージョン。
- The start and end date, time, and how long the pipeline took to complete each of the steps. 開始日と終了日、時間、パイプラインが各ステップを完了するのに要した時間。
- The executor of the pipeline. パイプラインの実行者。
- The parameter arguments that were passed to the pipeline. パイプラインに渡されたパラメータ引数。
- The pointers to the artifacts produced by each step of the pipeline, such as the location of prepared data, validation anomalies, computed statistics, and extracted vocabulary from the categorical features. パイプラインの各ステップで生成された成果物へのポインタ(=成果物のpath??)。例えば、準備されたデータの場所、検証の異常、計算された統計、カテゴリ特徴から抽出された語彙、など。 Tracking these intermediate outputs helps you resume the pipeline from the most recent step if the pipeline stopped due to a failed step, without having to re-execute the steps that have already completed. **これらの中間出力を追跡することで、パイプラインが失敗したステップによって停止した場合、すでに完了したステップを再実行することなく、最新のステップからパイプラインを再開することができます**。(pipelineの途中の任意のstepから再実行できる方がいいよな...:thinking:)
- A pointer to the previous trained model if you need to roll back to a previous model version or if you need to produce evaluation metrics for a previous model version when the pipeline is given new test data during the model validation step. 前回のトレーニングされたモデルへのポインタ。**以前のモデルバージョンにロールバックする必要がある場合**や、モデル検証ステップで新しいテストデータが与えられたときに、以前のモデルバージョンの評価メトリクスを生成する必要がある場合に使用します。
- The model evaluation metrics produced during the model evaluation step for both the training and the testing sets. トレーニングセットとテストセットの両方に対して、モデル評価ステップ中に生成されたモデル評価メトリクス。These metrics help you compare the performance of a newly trained model to the recorded performance of the previous model during the model validation step. これらのメトリクスは、モデル検証ステップ中に、新しくトレーニングされたモデルのパフォーマンスを以前のモデルの記録されたパフォーマンスと比較するのに役立ちます。

<!-- ここまで読んだ -->

#### ML pipeline triggers MLパイプラインのトリガー

You can automate the ML production pipelines to retrain the models with new data, depending on your use case:
**ユースケースに応じて**、新しいデータでモデルを再トレーニングするためにML本番パイプラインを自動化することができます：
(確かに、pipelineのtriggerはusecaseによって色々変わるよね...!:thinking:)

- **On demand**: Ad-hoc manual execution of the pipeline. オンデマンド： パイプラインのアドホックな手動実行。
- **On a schedule**: New, labelled data is systematically available for the ML system on a daily, weekly, or monthly basis. スケジュール通りに： 新しい、ラベル付けされたデータは、毎日、毎週、または毎月、MLシステムで体系的に利用可能です。 The retraining frequency also depends on how frequently the data patterns change, and how expensive it is to retrain your models. 再トレーニングの頻度は、データパターンがどれくらい頻繁に変化するか、モデルを再トレーニングするのがどれくらいコストがかかるかにも依存します。
- **On availability of new training data**: New data isn't systematically available for the ML system and instead is available on an ad-hoc basis when new data is collected and made available in the source databases. 新しいトレーニングデータが利用可能になったとき： 新しいデータは、MLシステムに体系的に利用可能ではなく、新しいデータが収集され、ソースデータベースで利用可能になったときにアドホックな基準で利用可能です。 
- On model performance degradation: The model is retrained when there is noticeable performance degradation. モデルのパフォーマンスが低下したとき： パフォーマンスが著しく低下したときにモデルを再トレーニングします。

- On significant changes in the data distributions (concept drift). **データ分布の著しい変化（コンセプトドリフト）が発生した時**。 It's hard to assess the complete performance of the online model, but you notice significant changes on the data distributions of the features that are used to perform the prediction. オンラインモデルの完全なパフォーマンスを評価するのは難しいですが、予測を行うために使用される特徴量のデータ分布に著しい変化があることに気づきます。 These changes suggest that your model has gone stale, and that needs to be retrained on fresh data. **これらの変化は、モデルが古くなったことを示しており**、新鮮なデータで再トレーニングする必要があることを示しています。

<!-- ここまで読んだ! -->

### Challenges 課題

Assuming that new implementations of the pipeline aren't frequently deployed and you are managing only a few pipelines, you usually manually test the pipeline and its components.
**新しいパイプラインの実装が頻繁にデプロイされず、数本のパイプラインのみを管理していると仮定すると**、通常、パイプラインとそのコンポーネントを手動でテストします。
In addition, you manually deploy new pipeline implementations.
さらに、新しいパイプラインの実装を手動でデプロイします。
You also submit the tested source code for the pipeline to the IT team to deploy to the target environment.
また、テスト済みのパイプラインのソースコードをITチームに提出して、ターゲット環境にデプロイします。
This setup is suitable when you deploy new models based on new data, rather than based on new ML ideas.
この設定は、新しいデータに基づいて新しいモデルをデプロイする場合に適していますが、新しいMLのアイデアに基づいてデプロイする場合には適していません。

However, you need to try new ML ideas and rapidly deploy new implementations of the ML components.
**しかし、新しいMLのアイデアを試して、MLコンポーネントの新しい実装を迅速にデプロイする必要があります**。(新しいアイデアをすぐに試せてデプロイできるようにしたい...!:thinking:)
If you manage many ML pipelines in production, you need a CI/CD setup to automate the build, test, and deployment of ML pipelines.
本番環境で多くのMLパイプラインを管理する場合、MLパイプラインのビルド、テスト、デプロイメントを自動化するためのCI/CDセットアップが必要です。

<!-- ここまで読んだ! -->

## MLOps level 2: CI/CD pipeline automation MLOpsレベル2 CI/CDパイプラインの自動化

For a rapid and reliable update of the pipelines in production, you need a robust automated CI/CD system.
**本番環境でパイプラインを迅速かつ確実に更新するには、堅牢な自動CI/CDシステムが必要**です。
This automated CI/CD system lets your data scientists rapidly explore new ideas around feature engineering, model architecture, and hyperparameters.
この自動化されたCI/CDシステムにより、データ・サイエンティストは、フィーチャー・エンジニアリング、モデル・アーキテクチャ、ハイパー・パラメータに関する**新しいアイデアを迅速に探求することができます。**(迅速にしたい...!:thinking:)
They can implement these ideas and automatically build, test, and deploy the new pipeline components to the target environment.
**これらのアイデアを実装し、新しいパイプラインコンポーネントを自動的にビルド、テストし、ターゲット環境にデプロイすることができる。**

The following diagram shows the implementation of the ML pipeline using CI/CD, which has the characteristics of the automated ML pipelines setup plus the automated CI/CD routines.
以下の図は、CI/CDを使用したMLパイプラインの実装を示しており、自動化されたMLパイプラインのセットアップに加えて、自動化されたCI/CDルーチンの特性を持っています。
(FTI pipelinesのブログで引用されてた、わかりづらい MLOps mapだ!:thinking:)

![figure4]()

This MLOps setup includes the following components:
このMLOpsセットアップには、以下のコンポーネントが含まれる：

- Source control
- Test and build services サービスのテストと構築
- Deployment services デプロイメント・サービス
- Model registry
- Feature store
- ML metadata store
- ML pipeline orchestrator

<!-- ここまで読んだ! -->

### Characteristics 特徴

The following diagram shows the stages of the ML CI/CD automation pipeline:
以下の図は、MLのCI/CD自動化パイプラインの段階を示している:

![figure5]()
Figure 5. Stages of the CI/CD automated ML pipeline.
図5. CI/CD自動化MLパイプラインのステージ。

The pipeline consists of the following stages:
パイプラインは以下のステージで構成されている: (このpipelineは、**CD pipeline**のこと...!)

- 1. Development and experimentation: You iteratively try out new ML algorithms and new modeling where the experiment steps are orchestrated.
開発と実験： 新しいMLアルゴリズムや新しいモデリングを繰り返し試し、実験ステップがオーケストレーションされる。The output of this stage is the source code of the ML pipeline steps that are then pushed to a source repository. この段階の出力は、MLパイプラインステップのソースコードであり、ソースリポジトリにプッシュされる。
- 2. Pipeline continuous integration: You build source code and run various tests. パイプラインの継続的インテグレーション： ソースコードをビルドし、様々なテストを実行する。 The outputs of this stage are pipeline components (packages, executables, and artifacts) to be deployed in a later stage. この段階の出力は、後の段階でデプロイされるパイプラインコンポーネント（パッケージ、実行可能ファイル、成果物）である。
- 3. Pipeline continuous delivery: You deploy the artifacts produced by the CI stage to the target environment.
パイプラインによる継続的デリバリー： **CIステージで作成された成果物をターゲット環境にデプロイする**。 The output of this stage is a deployed pipeline with the new implementation of the model. このステージのアウトプットは、モデルの新しい実装を含むデプロイされたパイプラインである。
- 4. Automated triggering: The pipeline is automatically executed in production based on a schedule or in response to a trigger. 自動トリガー： パイプラインは、スケジュールに基づいて、またはトリガーに応答して、プロダクションで自動的に実行される。 The output of this stage is a trained model that is pushed to the model registry. この段階の出力は、モデル登録にプッシュされる学習済みモデルである。
- 5. **Model continuous delivery**: You serve the trained model as a prediction service for the predictions. モデルの継続的デリバリー： 学習済みのモデルを予測サービスとして提供する。 The output of this stage is a deployed model prediction service. この段階の出力は、展開されたモデル予測サービスである。
- 6. Monitoring: You collect statistics on the model performance based on live data. モニタリング： ライブデータに基づいてモデルのパフォーマンスに関する統計を収集します。 The output of this stage is a trigger to execute the pipeline or to execute a new experiment cycle. このステージの出力は、パイプラインの実行や新しい実験サイクルの実行のトリガーとなる。

(なるほど、MLシステムのoperationだから、step4とstep５とstep6があるのか:thinking:)

The data analysis step is still a manual process for data scientists before the pipeline starts a new iteration of the experiment.
データ分析ステップは、パイプラインが実験の新しい反復を開始する前に、データサイエンティストにとって依然として手作業のプロセスである。
The model analysis step is also a manual process.
モデル分析のステップも手作業だ。

<!-- ここまで読んだ! -->

### Continuous integration 継続的インテグレーション

In this setup, the pipeline and its components are built, tested, and packaged when new code is committed or pushed to the source code repository.
このセットアップでは、新しいコードがソースコード・リポジトリにコミットまたはプッシュされると、パイプラインとそのコンポーネントがビルド、テスト、パッケージ化される。
Besides building packages, container images, and executables, the CI process can include the following tests:
パッケージ、コンテナイメージ、実行可能ファイルをビルドするだけでなく、**CIプロセスには以下のテストが含まれることがあります**：

- Unit testing your feature engineering logic. フィーチャーエンジニアリングロジックのユニットテスト
- Unit testing the different methods implemented in your model. モデルに実装されたさまざまなメソッドのユニットテスト For example, you have a function that accepts a categorical data column and you encode the function as a one-hot feature. 例えば、カテゴリーデータ列を受け入れる関数があり、その関数をワンホット特徴としてエンコードするとする。
- Testing that your model training converges (that is, the loss of your model goes down by iterations and overfits a few sample records). モデル学習が収束する（つまり、モデルの損失が反復によって減少し、いくつかのサンプルレコードをオーバーフィットする）ことをテストする。
- Testing that your model training doesn't produce NaN values due to dividing by zero or manipulating small or large values. モデル学習が、ゼロで割ったり、大小の値を操作したりすることによってNaN値を生成しないことをテストする。
- Testing that each component in the pipeline produces the expected artifacts. **パイプラインの各コンポーネントが期待される成果物を生成することをテストする**。
- Testing integration between pipeline components. **パイプラインコンポーネント間の統合テスト**

(後半2つのテストしたいな。)

<!-- ここまで読んだ! -->

### Continuous delivery 継続的デリバリー

In this level, your system continuously delivers new pipeline implementations to the target environment that in turn delivers prediction services of the newly trained model.
このレベルでは、システムは新しいパイプラインの実装をターゲット環境に継続的に提供し、その結果、新しく学習されたモデルの予測サービスが提供される。
For rapid and reliable continuous delivery of pipelines and models, you should consider the following:
パイプラインとモデルの迅速かつ信頼性の高い継続的デリバリーのためには、以下を考慮すべきである：

- Verifying the compatibility of the model with the target infrastructure before you deploy your model. **モデルをデプロイする前に、ターゲットインフラストラクチャとモデルの互換性を検証する**。 For example, you need to verify that the packages that are required by the model are installed in the serving environment, and that the required memory, compute, and accelerator resources are available. たとえば、モデルに必要なパッケージがサービング環境にインストールされていること、必要なメモリ、計算、アクセラレータリソースが利用可能であることを検証する必要があります。

- Testing the prediction service by calling the service API with the expected inputs, and making sure that you get the response that you expect. 予想される入力でサービスAPIを呼び出し、予想されるレスポンスが得られることを確認することで、**予測サービスをテスト**する。 This test usually captures problems that might occur when you update the model version and it expects a different input. このテストは通常、モデルのバージョンを更新し、異なる入力を期待した場合に発生する可能性のある問題を捕捉する。
- Testing prediction service performance, which involves load testing the service to capture metrics such as queries per seconds (QPS) and model latency. **予測サービスのパフォーマンスをテストする**。これには、クエリ数（QPS）やモデルのレイテンシなどのメトリクスをキャプチャするためにサービスの負荷テストが含まれる。
- Validating the data either for retraining or batch prediction. **再トレーニングまたはバッチ予測のためのデータを検証**する。
- Verifying that models meet the predictive performance targets before they are deployed. **モデルがデプロイされる前に、予測性能目標を満たしていることを検証**する。
- Automated deployment to a test environment, for example, a deployment that is triggered by pushing code to the development branch. **テスト環境への自動デプロイメント**。たとえば、コードを開発ブランチにプッシュすることでトリガーされるデプロイメント。(CI的な自動テストみたいな?)
- Semi-automated deployment to a pre-production environment, for example, a deployment that is triggered by merging code to the main branch after reviewers approve the changes. **本番前の環境への半自動デプロイメント**。たとえば、レビュアーが変更を承認した後、コードをメインブランチにマージすることでトリガーされるデプロイメント。
- Manual deployment to a production environment after several successful runs of the pipeline on the pre-production environment. 本番前の環境でパイプラインを数回実行し成功した後、**本番環境に手動でデプロイする**。(あ、まあAPIだもんね。本番へはちゃんと検証が全て通ってから手動でgoサインを出すべき、ってことか)

To summarize, implementing ML in a production environment doesn't only mean deploying your model as an API for prediction.
要約すると、本番環境でMLを実装することは、予測用のAPIとしてモデルをデプロイすることだけを意味しない。
Rather, it means deploying an ML pipeline that can automate the retraining and deployment of new models.
そうではなく、新しいモデルの再トレーニングとデプロイメントを自動化できるMLパイプラインをデプロイすることを意味する。
Setting up a CI/CD system enables you to automatically test and deploy new pipeline implementations.
CI/CDシステムをセットアップすることで、新しいパイプラインの実装を自動的にテストし、デプロイすることができる。
This system lets you cope with rapid changes in your data and business environment.
このシステムにより、データやビジネス環境の急速な変化に対応することができます。
You don't have to immediately move all of your processes from one level to another.
すべてのプロセスをあるレベルから別のレベルにすぐに移す必要はない。
You can gradually implement these practices to help improve the automation of your ML system development and production.
これらのプラクティスを徐々に導入することで、MLシステムの開発と生産の自動化を改善することができる。

### What's next 次の記事

Learn more about Architecture for MLOps using TensorFlow Extended, Vertex AI Pipelines, and Cloud Build.
TensorFlow Extended、Vertex AI Pipelines、Cloud Buildを使用したMLOpsのためのアーキテクチャの詳細については、こちらをご覧ください。

Learn about the Practitioners Guide to Machine Learning Operations (MLOps).
機械学習オペレーション（MLOps）プラクティショナーズガイドをご覧ください。

Learn more about Setting up a CI/CD pipeline for your data-processing workflow.
データ処理ワークフローにCI/CDパイプラインを設定する」の詳細をご覧ください。

Watch the MLOps Best Practices on Google Cloud (Cloud Next '19) on YouTube.
Google CloudにおけるMLOpsのベストプラクティス（Cloud Next '19）をYouTubeでご覧ください。

For more reference architectures, diagrams, and best practices, explore the Cloud Architecture Center.
リファレンス・アーキテクチャ、ダイアグラム、ベスト・プラクティスについては、クラウド・アーキテクチャ・センターをご覧ください。
