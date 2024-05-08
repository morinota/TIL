## refs: refs：

- https://www.kdnuggets.com/2023/09/hopsworks-unify-batch-ml-systems-feature-training-inference-pipelines https://www.kdnuggets.com/2023/09/hopsworks-unify-batch-ml-systems-feature-training-inference-pipelines

# Unify Batch and ML Systems with Feature/Training/Inference Pipelines 特徴/学習/推論パイプラインでバッチとMLシステムを統合する

By Jim Dowling, Co-Founder & CEO, Hopsworks
ジム・ダウリング（ホップワークス共同設立者兼CEO）著

## Introduction 

This article introduces a unified architectural pattern for building both Batch and Real-Time machine learning (ML) Systems.
この記事では、バッチとリアルタイムの両方の機械学習（ML）システムを構築するための統一されたアーキテクチャ・パターンを紹介する。
We call it the FTI (Feature, Training, Inference) pipeline architecture.
私たちはこれをFTI（Feature, Training, Inference）パイプライン・アーキテクチャと呼んでいる。
FTI pipelines break up the monolithic ML pipeline into 3 independent pipelines, each with clearly defined inputs and outputs, where each pipeline can be developed, tested, and operated independently.
FTIパイプラインは、モノリシックなMLパイプラインを3つの独立したパイプラインに分割し、それぞれが明確に定義された入力と出力を持ち、各パイプラインは独立して開発、テスト、運用することができます。
For a historical perspective on the evolution of the FTI Pipeline architecture, you can read the full in-depth mental map for MLOps article.
FTI Pipelineアーキテクチャの進化に関する歴史的な視点については、MLOpsの詳細なメンタルマップの記事をお読みください。

In recent years, Machine Learning Operations (MLOps) has gained mindshare as a development process, inspired by DevOps principles, that introduces automated testing, versioning of ML assets, and operational monitoring to enable ML systems to be incrementally developed and deployed.
近年、機械学習オペレーション（MLOps）は、DevOpsの原則に触発された開発プロセスとして注目を集め、自動テスト、ML資産のバージョン管理、MLシステムのインクリメンタルな開発とデプロイを可能にする運用監視を導入している。
However, existing MLOps approaches often present a complex and overwhelming landscape, leaving many teams struggling to navigate the path from model development to production.
しかし、既存のMLOpsのアプローチは、複雑で圧倒されるような状況を提示することが多く、多くのチームがモデル開発から生産までの道のりをナビゲートするのに苦労している。
In this article, we introduce a fresh perspective on building ML systems through the concept of FTI pipelines.
本稿では、FTIパイプラインの概念を通じて、MLシステム構築の新たな視点を紹介する。
The FTI architecture has empowered countless developers to create robust ML systems with ease, reducing cognitive load, and fostering better collaboration across teams.
FTIアーキテクチャは、数え切れないほどの開発者に、堅牢なMLシステムを簡単に作成する力を与え、認知的負荷を軽減し、チーム間のより良いコラボレーションを促進します。
We delve into the core principles of FTI pipelines and explore their applications in both batch and real-time ML systems.
FTIパイプラインの核となる原理を掘り下げ、バッチとリアルタイムの両方のMLシステムでの応用を探る。

## Unified Architecture for ML Systems as Feature/Traing/Inference Pipelines 特徴／学習／推論パイプラインとしてのMLシステムの統一アーキテクチャ

The FTI approach for this architectural pattern has been used to build hundreds of ML systems.
このアーキテクチャパターンのFTIアプローチは、何百ものMLシステムの構築に使われてきた。
The pattern is as follows - a ML system consists of three independently developed and operated ML pipelines:
MLシステムは、独立して開発・運用される3つのMLパイプラインから構成される：

a feature pipeline that takes as input raw data that it transforms into features (and labels)
生データを入力として特徴（とラベル）に変換する特徴パイプライン

a training pipeline that takes as input features (and labels) and outputs a trained model, and
特徴（およびラベル）を入力とし、学習済みモデルを出力する学習パイプラインと

an inference pipeline that takes new feature data and a trained model and makes predictions.
新しい特徴データと学習済みモデルを受け取り、予測を行う推論パイプライン。

In this FTI, there is no single ML pipeline.
このFTIでは、単一のMLパイプラインは存在しない。
The confusion about what the ML pipeline does (does it feature engineer and train models or also do inference or just one of those?) disappears.
MLパイプラインが何をするのか（フィーチャーエンジニアリングとモデルの訓練なのか、推論もするのか、それともどちらか一方だけなのか）についての混乱はなくなる。
The FTI architecture applies to both batch ML systems and real-time ML systems.
FTIアーキテクチャは、バッチMLシステムにもリアルタイムMLシステムにも適用できる。

The feature pipeline can be a batch program or a streaming program.
フィーチャー・パイプラインは、バッチ・プログラムでもストリーミング・プログラムでもよい。
The training pipeline can output anything from a simple XGBoost model to a parameter-efficient fine-tuned (PEFT) large-language model (LLM), trained on many GPUs.
トレーニング・パイプラインは、単純なXGBoostモデルから、多数のGPUでトレーニングされたパラメータ効率の良いファインチューニング（PEFT）ラージ・ランゲージ・モデル（LLM）まで出力できる。
Finally, the inference pipeline can be a batch program that produces a batch of predictions to an online service that takes requests from clients and returns predictions in real-time.
最後に、推論パイプラインは、クライアントからのリクエストを受けてリアルタイムで予測を返すオンラインサービスに対して、予測のバッチを生成するバッチプログラムとすることができる。

One major advantage of FTI pipelines is that it is an open architecture.
FTIパイプラインの大きな利点は、オープン・アーキテクチャであることだ。
You can use Python, Java or SQL.
Python、Java、SQLを使うことができる。
If you need to do feature engineering on large volumes of data, you can use Spark or DBT or Beam.
大量のデータに対してフィーチャーエンジニアリングを行う必要がある場合は、SparkやDBT、Beamを使うことができる。
Training will typically be in Python using some ML framework, and batch inference could be in Python or Spark, depending on your data volumes.
トレーニングは通常、何らかのMLフレームワークを使ってPythonで行い、バッチ推論はデータ量に応じてPythonかSparkで行う。
Online inference pipelines are, however, nearly always in Python as models are typically training with Python.
しかし、オンライン推論パイプラインは、モデルの学習が通常Pythonで行われるため、ほぼ常にPythonで行われる。

The FTI pipelines are also modular and there is a clear interface between the different stages.
FTIパイプラインはモジュール化されており、異なるステージ間には明確なインターフェイスがある。
Each FTI pipeline can be operated independently.
それぞれのFTIパイプラインは独立して操作できる。
Compared to the monolithic ML pipeline, different teams can now be responsible for developing and operating each pipeline.
モノリシックなMLパイプラインに比べて、異なるチームがそれぞれのパイプラインの開発と運用を担当できるようになった。
The impact of this is that for orchestration, for example, one team could use one orchestrator for a feature pipeline and a different team could use a different orchestrator for the batch inference pipeline.
この影響は、例えばオーケストレーションの場合、あるチームはあるオーケストレーターを機能パイプラインに使い、別のチームは別のオーケストレーターをバッチ推論パイプラインに使うことができる。
Alternatively, you could use the same orchestrator for the three different FTI pipelines for a batch ML system.
あるいは、バッチMLシステムの3つの異なるFTIパイプラインに同じオーケストレーターを使うこともできる。
Some examples of orchestrators that can be used in ML systems include general-purpose, feature-rich orchestrators, such as Airflow, or lightweight orchestrators, such as Modal, or managed orchestrators offered by feature platforms.
MLシステムで使用可能なオーケストレータの例としては、Airflowのような汎用的で機能豊富なオーケストレータや、Modalのような軽量なオーケストレータ、あるいは機能プラットフォームが提供するマネージド・オーケストレータなどがある。

Some of the FTI pipelines, however, will not need orchestration.
しかし、FTIパイプラインの一部はオーケストレーションを必要としない。
Training pipelines can be run on-demand, when a new model is needed.
トレーニングパイプラインは、新しいモデルが必要なときにオンデマンドで実行できる。
Streaming feature pipelines and online inference pipelines run continuously as services, and do not require orchestration.
ストリーミング・フィーチャー・パイプラインとオンライン推論パイプラインはサービスとして継続的に実行され、オーケストレーションは必要ない。
Flink, Spark Streaming, and Beam are run as services on platforms such as Kubernetes, Databricks, or Hopsworks.
Flink、Spark Streaming、Beamは、Kubernetes、Databricks、Hopsworksなどのプラットフォーム上でサービスとして実行される。
Online inference pipelines are deployed with their model on model serving platforms, such as KServe (Hopsworks), Seldon, Sagemaker, and Ray.
オンライン推論パイプラインは、KServe（Hopsworks）、Seldon、Sagemaker、Rayなどのモデル提供プラットフォーム上にモデルとともに展開される。
The main takeaway here is that the ML pipelines are modular with clear interfaces, enabling you to choose the best technology for running your FTI pipelines.
ここでの主なポイントは、MLパイプラインは明確なインターフェイスを備えたモジュール式であり、FTIパイプラインの実行に最適なテクノロジーを選択できるということです。

Finally, we show how we connect our FTI pipelines together with a stateful layer to store the ML artifacts - features, training/test data, and models.
最後に、FTIパイプラインを、MLの成果物（特徴、トレーニング／テストデータ、モデル）を保存するステートフルレイヤーとどのように接続するかを示します。
Feature pipelines store their output, features, as DataFrames in the feature store.
フィーチャー・パイプラインは、その出力であるフィーチャーをDataFramesとしてフィーチャーストアに保存する。
Incremental tables store each new update/append/delete as separate commits using a table format (we use Apache Hudi in Hopsworks).
インクリメンタルテーブルは、各新規更新/追加/削除を、テーブルフォーマットを使って別々のコミットとして保存する（HopsworksではApache Hudiを使っている）。
Training pipelines read point-in-time consistent snapshots of training data from Hopsworks to train models with and output the trained model to a model registry.
トレーニングパイプラインは、Hopsworksからポイントインタイムで一貫性のあるトレーニングデータのスナップショットを読み込んでモデルをトレーニングし、トレーニング済みモデルをモデルレジストリに出力する。
You can include your favorite model registry here, but we are biased towards Hopsworks’ model registry.
ここにお好きなモデル登録を入れることができますが、私たちはホップワークスのモデル登録に偏っています。
Batch inference pipelines also read point-in-time consistent snapshots of inference data from the feature store, and produce predictions by applying the model to the inference data.
バッチ推論パイプラインはまた、特徴ストアから推論データのポイント・イン・タイム一貫性のあるスナップショットを読み込み、推論データにモデルを適用して予測を生成する。
Online inference pipelines compute on-demand features and read precomputed features from the feature store to build a feature vector that is used to make predictions in response to requests by online applications/services.
オンライン推論パイプラインは、オンデマンド特徴量を計算し、特徴量ストアから事前計算された特徴量を読み出して特徴量ベクトルを構築し、オンラインアプリケーション/サービスからの要求に応じて予測を行う。

### Feature Pipelines フィーチャー・パイプライン

Feature pipelines read data from data sources, compute features and ingest them to the feature store.
フィーチャー・パイプラインは、データ・ソースからデータを読み込み、フィーチャーを計算し、フィーチャー・ストアにインジェストする。
Some of the questions that need to be answered for any given feature pipeline include:
あるフィーチャー・パイプラインについて答えなければならない質問には、次のようなものがある：

Is the feature pipeline batch or streaming?
フィーチャーパイプラインはバッチかストリーミングか？

Are feature ingestions incremental or full-load operations?
フィーチャー・インジェストはインクリメンタルなのか、フルロードなのか？

What framework/language is used to implement the feature pipeline?
フィーチャー・パイプラインの実装には、どのようなフレームワーク／言語が使われていますか？

Is there data validation performed on the feature data before ingestion?
インジェストの前に、フィーチャーデータに対してデータバリデーションが行われているか。

What orchestrator is used to schedule the feature pipeline?
フィーチャー・パイプラインのスケジューリングには、どのオーケストレーターが使われていますか？

If some features have already been computed by an upstream system (e.g., a data warehouse), how do you prevent duplicating that data, and only read those features when creating training or batch inference data?
上流のシステム（データウェアハウスなど）ですでに計算されている特徴量がある場合、そのデータの重複を防ぎ、トレーニングデータやバッチ推論データを作成するときに、それらの特徴量だけを読み込むにはどうすればよいでしょうか？

### Training Pipelines トレーニングパイプライン

In training pipelines some of the details that can be discovered on double-clicking are:
トレーニングパイプラインでは、ダブルクリックで発見できる詳細がいくつかある：

What framework/language is used to implement the training pipeline?
トレーニングパイプラインの実装には、どのようなフレームワーク／言語が使用されていますか？

What experiment tracking platform is used?
どのような実験トラッキング・プラットフォームを使用しているのか？

Is the training pipeline run on a schedule (if so, what orchestrator is used), or is it run on-demand (e.g., in response to performance degradation of a model)?
トレーニングパイプラインはスケジュールで実行されるのか（実行される場合、どのようなオーケストレーターが使用されるのか）、それともオンデマンドで実行されるのか（モデルのパフォーマンス低下に対応するなど）。

Are GPUs needed for training? If yes, how are they allocated to training pipelines?
トレーニングにGPUは必要ですか？必要な場合、トレーニングパイプラインにどのように割り当てますか？

What feature encoding/scaling is done on which features? (We typically store feature data unencoded in the feature store, so that it can be used for EDA (exploratory data analysis).
どのフィーチャーに対して、どのようなフィーチャーエンコーディング/スケーリングが行われるのか？(EDA(探索的データ分析)に使用できるように、通常、特徴データはエンコードされずに特徴ストアに保存されます。
Encoding/scaling is performed in a consistent manner training and inference pipelines).
エンコード/スケーリングは、一貫した方法で行われる トレーニングと推論パイプライン）。
Examples of feature encoding techniques include scikit-learn pipelines or declarative transformations in feature views (Hopsworks).
特徴エンコーディング技術の例としては、scikit-learnパイプラインや特徴ビューの宣言的変換（Hopsworks）などがある。

What model evaluation and validation process is used?
どのようなモデル評価・検証プロセスを用いているのか？

What model registry is used to store the trained models?
学習済みモデルの保存には、どのようなモデルレジストリを使用するのですか？

### Inference Pipelines 推論パイプライン

Inference pipelines are as diverse as the applications they AI-enable.
推論パイプラインは、AIを可能にするアプリケーションと同様に多様である。
In inference pipelines, some of the details that can be discovered on double-clicking are:
推論パイプラインでは、ダブルクリックで発見できる詳細がいくつかある：

What is the prediction consumer - is it a dashboard, online application - and how does it consume predictions?
予測消費者とは何か、それはダッシュボードなのか、オンライン・アプリケーションなのか、そしてどのように予測を消費するのか。

Is it a batch or online inference pipeline?
推論パイプラインはバッチかオンラインか？

What type of feature encoding/scaling is done on which features?
どのフィーチャーに対して、どのようなフィーチャーエンコーディング／スケーリングが行われるのか？

For a batch inference pipeline, what framework/language is used? What orchestrator is used to run it on a schedule? What sink is used to consume the predictions produced?
バッチ推論パイプラインでは、どのようなフレームワーク／言語が使われるのか？それをスケジュールで実行するために、どのオーケストレーターが使われるのか？生成された予測を消費するためにどのようなシンクが使われるか？

For an online inference pipeline, what model serving server is used to host the deployed model? How is the online inference pipeline implemented - as a predictor class or with a separate transformer step? Are GPUs needed for inference? Is there a SLA (service-level agreements) for how long it takes to respond to prediction requests?
オンライン推論パイプラインでは、どのモデル・サービング・サーバーがデプロイされたモデルをホストするために使用されますか？オンライン推論パイプラインはどのように実装されますか? 推論にGPUは必要ですか？予測リクエストに応答するのにかかる時間に関するSLA（サービス・レベル・アグリーメント）はありますか？

## MLOps Principles 

The existing mantra is that MLOps is about automating continuous integration (CI), continuous delivery (CD), and continuous training (CT) for ML systems.
既存のマントラは、MLOpsはMLシステムの継続的インテグレーション（CI）、継続的デリバリー（CD）、継続的トレーニング（CT）を自動化することである。
But that is too abstract for many developers.
しかし、多くの開発者にとっては抽象的すぎる。
MLOps is really about continual development of ML-enabled products that evolve over time.
MLOpsとは、時間と共に進化するML対応製品の継続的な開発のことである。
The available input data (features) changes over time, the target you are trying to predict changes over time.
利用可能な入力データ（特徴量）は時間とともに変化し、予測しようとする対象も時間とともに変化する。
You need to make changes to the source code, and you want to ensure that any changes you make do not break your ML system or degrade its performance.
ソースコードに変更を加える必要があり、その変更がMLシステムを壊したり、性能を低下させたりしないようにしたい。
And you want to accelerate the time required to make those changes and test before those changes are automatically deployed to production.
そして、その変更が本番環境に自動的にデプロイされる前に、その変更とテストに必要な時間を短縮したい。

So, from our perspective, a more pithy definition of MLOps that enables ML Systems to be safely evolved over time is that it requires, at a minimum, automated testing, versioning, and monitoring of ML artifacts.
つまり、MLシステムを長期にわたって安全に進化させることを可能にするMLOpsの定義とは、最低限、ML成果物の自動テスト、バージョン管理、モニタリングが必要だということだ。
MLOps is about automated testing, versioning, and monitoring of ML artifacts.
MLOpsとは、MLの成果物の自動テスト、バージョン管理、モニタリングのことである。

![figure4]()

In figure 4, we can see that more levels of testing are needed in ML systems than in traditional software systems.
図4を見ると、MLシステムでは従来のソフトウェア・システムよりも多くのレベルのテストが必要であることがわかる。
Small bugs in data or code can easily cause a ML model to make incorrect predictions.
データやコードの小さなバグは、MLモデルが間違った予測をする原因になりやすい。
From a testing perspective, if web applications are propeller-driven airplanes, ML systems are jet-engines.
テストの観点から言えば、ウェブアプリケーションがプロペラ機なら、MLシステムはジェットエンジンだ。
It takes significant engineering effort to test and validate ML Systems  to make them safe!
MLシステムを安全なものにするためのテストと検証には、多大なエンジニアリングの労力を要する！

At a high level, we need to test both the source-code and data for ML Systems.
高いレベルでは、MLシステムのソースコードとデータの両方をテストする必要がある。
The features created by feature pipelines can have their logic tested with unit tests and their input data checked with data validation tests (e.g., Great Expectations).
フィーチャー・パイプラインで作成されたフィーチャーは、そのロジックをユニットテストでテストし、入力データをデータ検証テスト（Great Expectationsなど）でチェックすることができる。
The models need to be tested for performance, but also for a lack of bias against known groups of vulnerable users.
モデルの性能だけでなく、既知の弱者グループに対する偏りがないかどうかもテストする必要がある。
Finally, at the top of the pyramid, ML-Systems need to test their performance with A/B tests before they can switch to use a new model.
最後に、ピラミッドの頂点に位置するMLシステムは、新しいモデルの使用に切り替える前に、A/Bテストでパフォーマンスをテストする必要がある。

Finally, we need to version ML artifacts so that the operators of ML systems can safely update and rollback versions of deployed models.
最後に、MLシステムのオペレータが、配備されたモデルのバージョンを安全に更新したりロールバックしたりできるように、MLの成果物をバージョン管理する必要がある。
System support for the push-button upgrade/downgrade of models is one of the holy grails of MLOps.
プッシュボタンによるモデルのアップグレード／ダウングレードのシステムサポートは、MLOの聖杯のひとつである。
But models need features to make predictions, so model versions are connected to feature versions and models and features need to be upgraded/downgraded synchronously.
しかし、モデルは予測を行うためにフィーチャーを必要とする。そのため、モデルのバージョンはフィーチャーのバージョンと連動し、モデルとフィーチャーは同期してアップグレード／ダウングレードされる必要がある。
Luckily, you don’t need a year in rotation as a Google SRE to easily upgrade/downgrade models - platform support for versioned ML artifacts should make this a straightforward ML system maintenance operation.
幸いなことに、モデルのアップグレードやダウングレードを簡単に行うために、Google SREとして1年間ローテーションを組む必要はない。

## Example ML Systems MLシステムの例

Here is a sample of some of the open-source ML systems available built on the FTI architecture.
以下は、FTIアーキテクチャで構築されたオープンソースのMLシステムの一部である。
They have been built mostly by practitioners and students.
これらは主に練習生や学生によって作られてきた。

Batch ML Systems
バッチMLシステム

Electricity Demand Prediction (452 github stars)
電力需要予測 (452 github stars)

NBA Game Prediction (152 github stars)
NBAの試合予想（githubスター152個）

Premier league football score predictions (101 github stars)
サッカーのプレミアリーグのスコア予想 (101 github stars)

Churn prediction (113 github stars)
解約予測 (113 github stars)

Real-Time ML System
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
我々の経験によれば、このアーキテクチャは、特に従来のMLOpsアプローチと比較して、MLシステムの設計と説明に関連する認知的負荷を大幅に軽減する。
In corporate environments, it fosters enhanced inter-team communication by establishing clear interfaces, thereby promoting collaboration and expediting the development of high-quality ML systems.
企業環境においては、明確なインターフェースを確立することでチーム間のコミュニケーションを促進し、コラボレーションを促進し、高品質なMLシステムの開発を促進する。
While it simplifies the overarching complexity, it also allows for in-depth exploration of the individual pipelines.
包括的な複雑さを簡素化する一方で、個々のパイプラインを深く掘り下げることもできる。
Our goal for the FTI pipeline architecture is to facilitate improved teamwork and quicker model deployment, ultimately expediting the societal transformation driven by AI.
FTIのパイプライン・アーキテクチャの目標は、チームワークの向上と迅速なモデル展開を促進し、最終的にAIによる社会変革を促進することです。

Read more about the fundamental principles and elements that constitute the FTI Pipelines architecture in our full in-depth mental map for MLOps.
FTI Pipelinesアーキテクチャを構成する基本原則と要素については、MLOps向けの詳細なメンタルマップをご覧ください。

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