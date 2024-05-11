## refs: refs：

- https://www.kdnuggets.com/2023/09/hopsworks-unify-batch-ml-systems-feature-training-inference-pipelines https://www.kdnuggets.com/2023/09/hopsworks-unify-batch-ml-systems-feature-training-inference-pipelines

# Unify Batch and ML Systems with Feature/Training/Inference Pipelines 特徴/学習/推論パイプラインでバッチとMLシステムを統合する

By Jim Dowling, Co-Founder & CEO, Hopsworks
ジム・ダウリング（ホップワークス共同設立者兼CEO）著

## Introduction

This article introduces a unified architectural pattern for building both Batch and Real-Time machine learning (ML) Systems.
この記事では、バッチとリアルタイムの両方の機械学習（ML）システムを構築するための統一されたアーキテクチャ・パターンを紹介する。
We call it the FTI (Feature, Training, Inference) pipeline architecture.
私たちはこれを**FTI(Feature, Training, Inference) pipelines architecture**と呼んでいます。
FTI pipelines break up the monolithic ML pipeline into 3 independent pipelines, each with clearly defined inputs and outputs, where each pipeline can be developed, tested, and operated independently.
FTI pipelinesは、monolithicなMLパイプラインを**3つの独立したパイプラインに分割**し、それぞれのパイプラインには明確に定義された入力と出力があり、各パイプラインを独立して開発、テスト、運用できるようにします。
For a historical perspective on the evolution of the FTI Pipeline architecture, you can read the full in-depth mental map for MLOps article.
FTI Pipelineアーキテクチャの進化に関する歴史的な視点については、[MLOpsの詳細なメンタルマップの記事](https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines)をお読みください。

In recent years, Machine Learning Operations (MLOps) has gained mindshare as a development process, inspired by DevOps principles, that introduces automated testing, versioning of ML assets, and operational monitoring to enable ML systems to be incrementally developed and deployed.
近年、**Machine Learning Operations（MLOps）**は、DevOpsの原則に触発された開発プロセスとして、自動化されたテスト、**ML assetsのバージョニング**、運用モニタリングを導入し、MLシステムを段階的に開発・展開することを可能にするとして注目を集めています。
(assets: 資産、資本、財産。MLOpsにおいては、データセット, モデル, コード, モデルパラメータ, configファイル, ドキュメント, etc...!:thinking:)
However, existing MLOps approaches often present a complex and overwhelming landscape, leaving many teams struggling to navigate the path from model development to production.
しかし、既存のMLOpsのアプローチは、しばしば複雑で圧倒的な状況を提示し、多くのチームがモデル開発から本番環境への道筋を辿るのに苦労しています。
In this article, we introduce a fresh perspective on building ML systems through the concept of FTI pipelines.
本稿では、FTIパイプラインの概念を通じてMLシステムを構築する新しい視点を紹介します。
The FTI architecture has empowered countless developers to create robust ML systems with ease, reducing cognitive load, and fostering better collaboration across teams.
FTIアーキテクチャは、数え切れないほどの開発者に、堅牢なMLシステムを簡単に作成する力を与え、認知的負荷を軽減し、チーム間のより良いコラボレーションを促進します。
We delve into the core principles of FTI pipelines and explore their applications in both batch and real-time ML systems.
**FTIパイプラインの核となる原理を掘り下げ、バッチとリアルタイムの両方のMLシステムでの応用を探る**。

## Unified Architecture for ML Systems as Feature/Traing/Inference Pipelines 特徴／学習／推論パイプラインとしてのMLシステムの統一アーキテクチャ

The FTI approach for this architectural pattern has been used to build hundreds of ML systems.
このアーキテクチャパターンのFTIアプローチは、何百ものMLシステムの構築に使われてきた。
The pattern is as follows - a ML system consists of three independently developed and operated ML pipelines:
このパターンは次の通りです。**MLシステムは、3つの独立して開発・運用されるMLパイプラインで構成**されています。

- a feature pipeline that takes as input raw data that it transforms into features (and labels)
  生データを入力として特徴（とラベル）に変換する**feature pipeline**
- a training pipeline that takes as input features (and labels) and outputs a trained model, and
  特徴（およびラベル）を入力とし、学習済みモデルを出力する**training pipeline**
- an inference pipeline that takes new feature data and a trained model and makes predictions.
  新しい特徴データと学習済みモデルを受け取り、予測を行う**infernece pipeline**

In this FTI, there is no single ML pipeline.
このFTIでは、単一のMLパイプラインは存在しない。
The confusion about what the ML pipeline does (does it feature engineer and train models or also do inference or just one of those?) disappears.
MLパイプラインが何をするのかの混乱はなくなる。(フィーチャーエンジニアリングとモデルのトレーニングを行うのか、推論を行うのか、それともそのうちの1つだけを行うのか？)
The FTI architecture applies to both batch ML systems and real-time ML systems.
FTIアーキテクチャは、バッチMLシステムにもリアルタイムMLシステムにも適用できる。

![figure1]()
Figure 1: The Feature/Training/Inference (FTI) pipelines for building ML Systems
図1: MLシステムを構築するためのFeature/Training/Inference（FTI）パイプライン

The feature pipeline can be a batch program or a streaming program.
**featureパイプラインはbatchプログラムまたはstreamingプログラムでも良い**。
The training pipeline can output anything from a simple XGBoost model to a parameter-efficient fine-tuned (PEFT) large-language model (LLM), trained on many GPUs.
training pipelineは、単純なXGBoostモデルから、多数のGPUでトレーニングされたパラメータ効率の良いファインチューニング（PEFT）大規模言語モデル(LLM)まで、何でも出力できる。
Finally, the inference pipeline can be a batch program that produces a batch of predictions to an online service that takes requests from clients and returns predictions in real-time.
最後に、inference pipelineは、クライアントからのリクエストを受け取り、リアルタイムで予測を返す**オンラインサービスでも良いし**、予測のバッチを生成する**バッチプログラムでも良い**。

One major advantage of FTI pipelines is that it is an open architecture.
FTIパイプラインの大きな利点は、**オープンアーキテクチャであること**です。
You can use Python, Java or SQL.
Python、Java、SQLを使うことができる。
If you need to do feature engineering on large volumes of data, you can use Spark or DBT or Beam.
大量のデータに対して feature engineering を行う必要がある場合、Spark、DBT、Beamを使うことができる。
Training will typically be in Python using some ML framework, and batch inference could be in Python or Spark, depending on your data volumes.
トレーニングは通常、何らかのMLフレームワークを使ってPythonで行い、バッチ推論はデータ量に応じてPythonかSparkで行う。
Online inference pipelines are, however, nearly always in Python as models are typically training with Python.
しかし、オンライン推論パイプラインは、モデルの学習が通常Pythonで行われるため、ほぼ常にPythonで行われる。(よっぽどシンプルな推論の仕組みだったら多言語でもOKだと思うが...!:thinking:)

![figure2]()
Figure 2: Choose the best orchestrator for your ML pipeline/service.

The FTI pipelines are also modular and there is a clear interface between the different stages.
**FTIパイプラインはmodularであり、異なるステージ間には明確なインターフェイスがある**。
Each FTI pipeline can be operated independently.
それぞれのFTIパイプラインは独立して操作できる。
Compared to the monolithic ML pipeline, different teams can now be responsible for developing and operating each pipeline.
モノリシックなMLパイプラインに比べて、異なるチームがそれぞれのパイプラインの開発と運用を担当できるようになった。
The impact of this is that for orchestration, for example, one team could use one orchestrator for a feature pipeline and a different team could use a different orchestrator for the batch inference pipeline.
この影響は、例えばオーケストレーションの場合、あるチームはあるオーケストレーターを feature pipeline に使用し、別のチームはbatch inference pipeline に別のオーケストレーターを使用することができる。
Alternatively, you could use the same orchestrator for the three different FTI pipelines for a batch ML system.
あるいは、batch MLシステムの場合、3つの異なるFTIパイプラインに同じオーケストレーターを使用することもできる。
Some examples of orchestrators that can be used in ML systems include general-purpose, feature-rich orchestrators, such as Airflow, or lightweight orchestrators, such as Modal, or managed orchestrators offered by feature platforms.
MLシステムで使用できるオーケストレーターの例には、Airflowなどの汎用性が高く機能が豊富なオーケストレーターや、Modalなどの軽量なオーケストレーター、または特徴量プラットフォームが提供する管理されたオーケストレーターがあります。(Databricksのorcherstratorもこれに該当するっぽい??:thinking:)

Some of the FTI pipelines, however, will not need orchestration.
しかし、FTIパイプラインの一部はオーケストレーションを必要としない。
Training pipelines can be run on-demand, when a new model is needed.
トレーニングパイプラインは、新しいモデルが必要なときにon-demandで実行できる。(on-demand = 需要に応じてマニュアルで??:thinking:)
Streaming feature pipelines and online inference pipelines run continuously as services, and do not require orchestration.
ストリーミング・フィーチャー・パイプラインとオンライン推論パイプラインはサービスとして継続的に実行され、オーケストレーションは必要ない。
Flink, Spark Streaming, and Beam are run as services on platforms such as Kubernetes, Databricks, or Hopsworks.
Flink、Spark Streaming、Beamは、Kubernetes、Databricks、Hopsworksなどのプラットフォーム上でサービスとして実行される。
Online inference pipelines are deployed with their model on model serving platforms, such as KServe (Hopsworks), Seldon, Sagemaker, and Ray.
online infrrence pipelineは、KServe(Hopsworks)、Seldon、Sagemaker、Rayなどのモデルサービングプラットフォームにモデルとともにデプロイされる。
The main takeaway here is that the ML pipelines are modular with clear interfaces, enabling you to choose the best technology for running your FTI pipelines.
ここでの主なポイントは、**MLパイプラインがモジュラーで明確なインターフェースを持ち、FTIパイプラインを実行するための最適なテクノロジーを選択できるようになる**ことです。(うんうん...!:thinking:)

![]()
Figure 3: Connect your ML pipelines with a Feature Store and Model Registry
図3: フィーチャーストアとモデルレジストリを使ってMLパイプラインを接続する

Finally, we show how we connect our FTI pipelines together with a stateful layer to store the ML artifacts - features, training/test data, and models.
最後に、FTIパイプラインを、**MLの成果物(特徴量, トレーニング／テストデータ, モデル)を保存する stateful layer**と接続する方法を示します。(statefull layer = 永続化層??:thinking:)
Feature pipelines store their output, features, as DataFrames in the feature store.
フィーチャー・パイプラインは、その出力であるフィーチャーをDataFramesとしてフィーチャーストアに保存する。
Incremental tables store each new update/append/delete as separate commits using a table format (we use Apache Hudi in Hopsworks).
incremental tablesは、新しい更新/追加/削除ごとに別々のコミットとして保存され、テーブル形式を使用する（HopsworksではApache Hudiを使用）。
(incremental tableってなんだ??:thinking:)
Training pipelines read point-in-time consistent snapshots of training data from Hopsworks to train models with and output the trained model to a model registry.
トレーニングパイプラインは、Hopsworks (=特徴量ストア?) からポイントインタイムで一貫性のあるトレーニングデータのスナップショットを読み込んでモデルをトレーニングし、トレーニング済みモデルをモデルレジストリに出力する。
You can include your favorite model registry here, but we are biased towards Hopsworks’ model registry.
ここにお好きな model registry を含めることができますが、私たちはHopsworksの model registry に偏っています。(そりゃHopsworkのCEOだもんね...!:thinking:)
Batch inference pipelines also read point-in-time consistent snapshots of inference data from the feature store, and produce predictions by applying the model to the inference data.
バッチ推論パイプラインはまた、特徴量ストアから推論データのポイント・イン・タイム一貫性のあるスナップショットを読み込み、推論データにモデルを適用して予測を生成する。
Online inference pipelines compute on-demand features and read precomputed features from the feature store to build a feature vector that is used to make predictions in response to requests by online applications/services.
オンライン推論パイプラインは、on-demand特徴量(=これはリアルタイムで渡される特徴量っぽい...!:thinking:)を計算し、フィーチャーストアから事前計算された特徴量を読み込むことで特徴量ベクトルを組み立てる。そして、 オンラインアプリケーション/サービスからのリクエストに応じて予測を行うために使用される。

<!-- ここまで読んだ! -->

### Feature Pipelines フィーチャー・パイプライン

Feature pipelines read data from data sources, compute features and ingest them to the feature store.
フィーチャー・パイプラインは、データ・ソースからデータを読み込み、フィーチャーを計算し、フィーチャー・ストアにインジェストする。
Some of the questions that need to be answered for any given feature pipeline include:
あるフィーチャー・パイプラインについて答えなければならない質問には、次のようなものがある：

- Is the feature pipeline batch or streaming?
  フィーチャーパイプラインはバッチかストリーミングか？
- Are feature ingestions incremental or full-load operations?
  feature ingestions(フィーチャーの取り込み)は、増分操作かフルロード操作か？
- What framework/language is used to implement the feature pipeline?
  feature pipelineの実装には、どのようなフレームワーク／言語が使用されていますか？
- Is there data validation performed on the feature data before ingestion?
  **ingestion(取り込み)前にフィーチャーデータに対してデータ検証が行われていますか?** (成果物のvalidaiton...!:thinking:)
- What orchestrator is used to schedule the feature pipeline?
  feature pipelineのスケジューリングには、どのオーケストレーターが使われていますか?
- If some features have already been computed by an upstream system (e.g., a data warehouse), how do you prevent duplicating that data, and only read those features when creating training or batch inference data?
  もし、一部のフィーチャーがすでに上流システム（例：データウェアハウス）で計算されている場合、そのデータの重複を防ぎ、トレーニングやバッチ推論データを作成する際には、それらのフィーチャーだけを読み込むようにするにはどうすればよいか？

(ここで"ingestion"は、feature pipelineで得られた成果物を、feature storeにingestするみたいな意味合いっぽい...!:thinking:)

<!-- ここまで読んだ! -->

### Training Pipelines トレーニングパイプライン

In training pipelines some of the details that can be discovered on double-clicking are:
トレーニングパイプラインでは、ダブルクリックで発見できる詳細がいくつかある:

- What framework/language is used to implement the training pipeline?
  トレーニングパイプラインの実装には、どのようなフレームワーク／言語が使用されていますか？
- What experiment tracking platform is used?
  どのような実験トラッキング・プラットフォームを使用しているのか？
- Is the training pipeline run on a schedule (if so, what orchestrator is used), or is it run on-demand (e.g., in response to performance degradation of a model)?
  トレーニングパイプラインはスケジュールで実行されるのか（実行される場合、どのようなオーケストレーターが使用されるのか）、それともオンデマンドで実行されるのか（モデルのパフォーマンス低下に対応するなど）。
- Are GPUs needed for training? If yes, how are they allocated to training pipelines?
  トレーニングにGPUは必要ですか？必要な場合、トレーニングパイプラインにどのように割り当てますか？
- What feature encoding/scaling is done on which features?
  どのフィーチャーに対して、どのようなフィーチャーエンコーディング／スケーリングが行われるのか?
  (We typically store feature data unencoded in the feature store, so that it can be used for EDA (exploratory data analysis). Encoding/scaling is performed in a consistent manner training and inference pipelines).
  (通常、フィーチャーデータはエンコードされていない状態でフィーチャーストアに保存されるため、EDA（探索的データ分析）に使用できる。エンコード／スケーリングは、トレーニングと推論パイプラインで一貫して実行される。)
  Examples of feature encoding techniques include scikit-learn pipelines or declarative transformations in feature views (Hopsworks).
  フィーチャーエンコーディング技術の例には、scikit-learnパイプラインやフィーチャービュー（Hopsworks）での宣言的変換が含まれる。
  (feature encoding/scalingは、feature pipelineで行ったほうが、TとIの一貫性を保証できるんじゃない...?:thinking:)
- What model evaluation and validation process is used?
  どのようなモデル評価・検証プロセスを用いているのか?
- What model registry is used to store the trained models?
  学習済みモデルの保存には、どのようなモデルレジストリを使用するのですか?

<!-- ここまで読んだ! -->

### Inference Pipelines 推論パイプライン

Inference pipelines are as diverse as the applications they AI-enable.
**inference pipelinesは、AIを有効にするアプリケーションと同様に多様です。**
In inference pipelines, some of the details that can be discovered on double-clicking are:
推論パイプラインでは、ダブルクリックで発見できる詳細がいくつかある:

- What is the prediction consumer - is it a dashboard, online application - and how does it consume predictions?
  **予測消費者は何か**、それはダッシュボードなのか、オンライン・アプリケーションなのか、そしてどのように予測を消費するのか。
- Is it a batch or online inference pipeline?
  推論パイプラインはバッチかオンラインか？
- What type of feature encoding/scaling is done on which features?
  どのフィーチャーに対して、どのようなフィーチャーエンコーディング／スケーリングが行われるのか？
  (これはfeature pipelinesに任せてはダメなのかなぁ...:thinking:)
- For a batch inference pipeline, what framework/language is used? What orchestrator is used to run it on a schedule? What sink is used to consume the predictions produced?
  バッチ推論パイプラインでは、どのようなフレームワーク／言語が使われるのか？それをスケジュールで実行するために、どのオーケストレーターが使われるのか？**生成された予測を消費するためにどのようなシンクが使われるか**？
- For an online inference pipeline, what model serving server is used to host the deployed model? How is the online inference pipeline implemented - as a predictor class or with a separate transformer step? Are GPUs needed for inference? Is there a SLA (service-level agreements) for how long it takes to respond to prediction requests?
  オンライン推論パイプラインでは、**デプロイされたモデルをホストするためにどのモデルサービングサーバが使われるか？**オンライン推論パイプラインは、predictorクラスとして実装されるか、別のtransformerステップとして実装されるか？推論にGPUは必要ですか？**予測リクエストに対して応答するのにどれくらい時間がかかるかについてのSLA（サービスレベル契約）はありますか?**

<!-- ここまで読んだ! -->

## MLOps Principles

The existing mantra is that MLOps is about automating continuous integration (CI), continuous delivery (CD), and continuous training (CT) for ML systems.
既存のmantra(=真言)は、**MLOpsはMLシステムのための継続的インテグレーション（CI）、継続的デリバリー（CD）、継続的トレーニング（CT）を自動化することだ**ということです。(continous integrationはCDの概念の一つだと思ってるけど...!:thinking:)
But that is too abstract for many developers.
しかし、多くの開発者にとっては抽象的すぎる。
MLOps is really about continual development of ML-enabled products that evolve over time.
**MLOpsとは、時間と共に進化するML対応プロダクトの継続的な開発についてである**。(なるほど...! MLOps = 持続可能なMLプロダクト開発のための概念ってこと?? :thinking:)
The available input data (features) changes over time, the target you are trying to predict changes over time.
**利用可能な入力データ（特徴量）は時間とともに変化し、予測しようとする対象も時間とともに変化する**。
You need to make changes to the source code, and you want to ensure that any changes you make do not break your ML system or degrade its performance.
**ソースコードに変更を加える必要があり、その変更がMLシステムを壊したり、パフォーマンスを低下させたりしないようにしたい**。
And you want to accelerate the time required to make those changes and test before those changes are automatically deployed to production.
そして、**変更を加えるために必要な時間を短縮したい**。そして、それらの変更が自動的に本番環墴にデプロイされる前にテストを行いたい。

So, from our perspective, a more pithy definition of MLOps that enables ML Systems to be safely evolved over time is that it requires, at a minimum, automated testing, versioning, and monitoring of ML artifacts.
つまり、私たちの視点から見ると、**MLシステムを安全に時間とともに進化させるためには**、最低限、MLの成果物の自動テスト、バージョン管理、モニタリングが必要であるという、より簡潔なMLOpsの定義が必要です。
MLOps is about automated testing, versioning, and monitoring of ML artifacts.
**MLOpsとは、MLの成果物の自動テスト、バージョン管理、モニタリングについてです**。(だいぶ簡潔になった! :thinking:)

![figure4]()
Figure 4: The testing pyramid for ML Artifacts
図4: ML成果物のテストピラミッド

In figure 4, we can see that more levels of testing are needed in ML systems than in traditional software systems.
図4を見ると、**MLシステムでは従来のソフトウェア・システムよりも多くのレベルのテストが必要である**ことがわかる。
Small bugs in data or code can easily cause a ML model to make incorrect predictions.
データやコードの小さなバグは、MLモデルが間違った予測をする原因になりやすい。
From a testing perspective, if web applications are propeller-driven airplanes, ML systems are jet-engines.
テストの観点から言えば、ウェブアプリケーションがプロペラ駆動の飛行機であるなら、MLシステムはジェットエンジンです。
It takes significant engineering effort to test and validate ML Systems to make them safe!
MLシステムを安全なものにするためのテストと検証には、かなりのエンジニアリング努力が必要です！

At a high level, we need to test both the source-code and data for ML Systems.
**高いレベルでは、MLシステムのソースコードとデータの両方をテストする必要がある**。
The features created by feature pipelines can have their logic tested with unit tests and their input data checked with data validation tests (e.g., Great Expectations).
**feature pipelineで作成された特徴量は、ユニットテストでそのロジックをテスト**し、**データ検証テスト(例：Great Expectations)で入力データをチェック**できる。(例: https://www.hopsworks.ai/post/data-validation-for-enterprise-ai-using-great-expectations-with-hopsworks)
The models need to be tested for performance, but also for a lack of bias against known groups of vulnerable users.
モデルの性能だけでなく、既知の弱者グループに対する偏りがないかどうかもテストする必要がある。
Finally, at the top of the pyramid, ML-Systems need to test their performance with A/B tests before they can switch to use a new model.
最後に、ピラミッドの頂点に位置するMLシステムは、**新しいモデルを使用する前にA/Bテストでパフォーマンスをテストする必要がある**。(そりゃそうじゃない...??:thinking:)

Finally, we need to version ML artifacts so that the operators of ML systems can safely update and rollback versions of deployed models.
最後に、**MLシステムのオペレータが、配備されたモデルのバージョンを安全に更新したりロールバックしたりできるように、MLの成果物をバージョン管理する必要がある**。
System support for the push-button upgrade/downgrade of models is one of the holy grails of MLOps.
**プッシュボタンによるモデルの upgrade/downgrade をサポートするシステム**は、MLOpsの聖杯の1つです。(必須ってこと...?:thinking:)
But models need features to make predictions, so model versions are connected to feature versions and models and features need to be upgraded/downgraded synchronously.
しかし、モデルは予測を行うために特徴量が必要なので、モデルのバージョンは特徴量のバージョンに接続され、**モデルと特徴量は同期してアップグレード/ダウングレードする必要がある**。(なるほど確かに...!:thinking:)
Luckily, you don’t need a year in rotation as a Google SRE to easily upgrade/downgrade models - platform support for versioned ML artifacts should make this a straightforward ML system maintenance operation.
幸いなことに、Google SREとしての1年間の経験がなくても、モデルのアップグレード/ダウングレードは簡単に行える - **バージョン管理されたML成果物をサポートするプラットフォームが、これを簡単なMLシステムのメンテナンス操作にするはず**です。(なるほど。SagemakerとかDatabricksとか頼む...!:thinking:)

<!-- ここまで読んだ! -->

## Example ML Systems MLシステムの例

Here is a sample of some of the open-source ML systems available built on the FTI architecture.
以下は、FTIアーキテクチャで構築されたオープンソースのMLシステムの一部である。
They have been built mostly by practitioners and students.
これらは主に練習生や学生によって作られてきた。

### Batch ML Systems

バッチMLシステム

Electricity Demand Prediction (452 github stars)
電力需要予測 (452 github stars)

NBA Game Prediction (152 github stars)
NBAの試合予想（githubスター152個）

Premier league football score predictions (101 github stars)
サッカーのプレミアリーグのスコア予想 (101 github stars)

Churn prediction (113 github stars)
解約予測 (113 github stars)

### Real-Time ML System

リアルタイムMLシステム

Online Credit Card Fraud (113 github stars)
オンラインクレジットカード詐欺 (113 github stars)

Crypto Price Prediction (65 github stars)
暗号通貨価格予測 (65 github stars)

Loan application approval (113 github stars)
ローン申請承認 (113 github stars)

## Summary 要約

This article introduces the FTI pipeline architecture for MLOps, which has empowered numerous developers to efficiently create and maintain ML systems.
この記事では、多くの開発者がMLシステムを効率的に作成・保守できるようにした、MLOpsのためのFTIパイプライン・アーキテクチャを紹介する。
Based on our experience, this architecture significantly reduces the cognitive load associated with designing and explaining ML systems, especially when compared to traditional MLOps approaches.
我々の経験に基づくと、このアーキテクチャは、従来のMLOpsアプローチと比較して、**MLシステムの設計と説明に関連する認知負荷を大幅に軽減する**。
In corporate environments, it fosters enhanced inter-team communication by establishing clear interfaces, thereby promoting collaboration and expediting the development of high-quality ML systems.
企業環境においては、**明確なインターフェースを確立することで**、チーム間のコミュニケーションを向上させ、協力を促進し、高品質なMLシステムの開発を迅速化する。
While it simplifies the overarching complexity, it also allows for in-depth exploration of the individual pipelines.
全体的な複雑さを簡素化する一方で、個々のパイプラインの詳細な探索も可能になる。
Our goal for the FTI pipeline architecture is to facilitate improved teamwork and quicker model deployment, ultimately expediting the societal transformation driven by AI.
FTIのパイプライン・アーキテクチャの目標は、チームワークの向上とモデルの迅速なデプロイメントを促進し、AIによって推進される社会の変革を加速することです。

Read more about the fundamental principles and elements that constitute the FTI Pipelines architecture in our full in-depth mental map for MLOps.
FTI Pipelinesアーキテクチャを構成する基本原則と要素については、[MLOps向けの詳細なメンタルマップ](https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines)をご覧ください。

### More On This Topic このトピックに関する詳細

Feature Store Summit 2022: A free conference on Feature Engineering
フィーチャーストア・サミット2022 フィーチャーエンジニアリングに関する無料カンファレンス

How causal inference lifts augmented analytics beyond flatland
因果推論がオーグメンテッド・アナリティクスを平地から解放する方法

Building Machine Learning Pipelines using Snowflake and Dask
SnowflakeとDaskを使った機械学習パイプラインの構築

Answering Questions with HuggingFace Pipelines and Streamlit
HuggingFaceパイプラインとStreamlitで質問に答える

Development & Testing of ETL Pipelines for AWS Locally
ローカルAWS向けETLパイプラインの開発とテスト

The Prefect Way to Automate & Orchestrate Data Pipelines
データパイプラインの自動化とオーケストレーションに最適な方法

<!-- ここまで読んだ! -->
