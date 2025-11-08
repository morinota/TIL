refs: https://www.hopsworks.ai/post/the-10-fallacies-of-mlops


# The 10 Fallacies of MLOps  MLOpsの10の誤謬
(誤謬: 考え・知識などのあやまり...!:thinking:)

## TL;DR 要約
MLOps was born from the need to build infrastructural software to support production AI systems. 
MLOpsは、プロダクションAIシステムをサポートするためのインフラストラクチャソフトウェアを構築する必要から生まれました。
In 2025, 52% of AI systems will not make it to production. 
**2025年には、AIシステムの52%がプロダクションに到達しない**でしょう。(厳しさの中にあるな...!:thinking:)
One of the reasons is that developers make false assumptions when building AI systems. 
その理由の一つは、**開発者がAIシステムを構築する際に誤った仮定をすること**です。
This article introduces 10 fallacies of MLOps that should help developers understand and identify potential problems ahead of time, enabling them to build better AI systems and get more models in production. 
この記事では、**開発者が事前に潜在的な問題を理解し特定するのに役立つMLOpsの10の誤謬**を紹介し、より良いAIシステムを構築し、**より多くのモデルをプロダクションに投入できるように**します。

<!-- いいテーマ! -->

## Top 10 Fallacies of MLOps MLOpsの10の誤謬

MLOps is a set of principles and practices that guide developers when building any type of AI system - from batch to real-time to LLM-powered systems. 
MLOpsは、バッチからリアルタイム、LLM駆動システムまで、あらゆるタイプのAIシステムを構築する際に開発者を導く原則と実践のセットです。しかし、MLOpsの基盤は深くありません。 
There are no biblical commandments internalized by the members of its church. 
その教会のメンバーによって内面化された聖書の戒律は存在しません。 
Many members of the MLOps church worship false gods - fallacies that cause AI systems to never make it to production. 
MLOpsの教会の多くのメンバーは、AIシステムが本番環境に到達できない原因となる誤謬という偽の神を崇拝しています。
These fallacies are inspired by a more mature computer discipline, distributed systems, that has a core set of tenants that developers agree on - the 8 fallacies of distributed computing. 
これらの誤謬は、開発者が合意するコアな原則を持つ、より成熟したコンピュータ分野である分散システムに触発されています - [分散コンピューティングの8つの誤謬](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)です。

The ten fallacies of MLOps listed below have been informed through my experience in building AI systems on Hopsworks used by everything from Fortune-500 companies to AI-powered startups, teaching a course on MLOps at KTH University, making the world’s first free MLOps course that built batch and real-time AI systems, and writing a book on Building AI Systems for O’Reilly. 
以下に挙げるMLOpsの10の誤謬は、フォーチュン500企業からAI駆動のスタートアップまであらゆるものに使用されるHopsworks上でAIシステムを構築した経験、KTH大学でMLOpsに関するコースを教えた経験、バッチおよびリアルタイムAIシステムを構築した世界初の無料MLOpsコースを作成した経験、O'Reilly向けに「Building AI Systems」という本を書いた経験から得られたものです。

<!-- ここまで読んだ! -->

### 1. Do it all in one ML Pipeline すべてを1つのMLパイプラインで行う

When you write your first batch AI system, it is possible to write it as a single program that can be parameterized to run in either training or inference modes. 
最初のバッチAIシステムを書くとき、それをトレーニングモードまたは推論モードで実行できるようにパラメータ化された単一のプログラムとして書くことが可能です。
This can lead to the false assumption that you can run any AI system in a single ML pipeline. 
これにより、**任意のAIシステムを単一のMLパイプラインで実行できるという誤った仮定**が生じる可能性があります。
You cannot run a real-time AI system as a single ML pipeline. 
リアルタイムAIシステムを単一のMLパイプラインとして実行することはできません。
It consists of at least an offline training pipeline that is run when you train a new version of the model and an online inference pipeline that runs 24/7. 
それは、モデルの新しいバージョンをトレーニングするときに実行されるオフライントレーニングパイプラインと、24時間365日稼働するオンライン推論パイプラインの**少なくとも2つで構成**されています。
This leads to confusion as to what exactly a ML pipeline is. 
これにより、**MLパイプラインとは正確に何かという混乱**が生じます。
What are its inputs and outputs? 
その入力と出力は何ですか？
Are data pipelines that create feature data also ML pipelines? 
特徴量データを生成するデータパイプラインもMLパイプラインですか？
They create the features (the inputs to our ML models). 
それらは特徴（私たちのMLモデルへの入力）を生成します。

So what should you do? 
では、何をすべきでしょうか？
You should decompose your AI system into feature/training/inference pipelines (FTI pipelines) that are connected together to make up your AI system, see Figure 1. 
**AIシステムを、AIシステムを構成するために接続された特徴/トレーニング/推論パイプライン（FTIパイプライン）に分解すべき**です。図1を参照してください。(若干position talkの最も含まれうることを意識して読む...!:thinking:)
Feature pipelines transform data from many different sources into features. 
特徴パイプラインは、さまざまなソースからのデータを特徴量に変換します。
Training pipelines take features/labels as input and output a trained model. 
トレーニングパイプラインは、特徴/ラベルを入力として受け取り、トレーニングされたモデルを出力します。
Inference pipelines take one or more trained models as input and feature data and output predictions. 
推論パイプラインは、1つまたは複数のトレーニングされたモデルと特徴データを入力として受け取り、予測を出力します。
Further decomposition of these pipelines is also possible - generally following the principle that you name the ML pipeline after its output. 
これらのパイプラインのさらなる分解も可能であり、**一般的には出力に基づいてMLパイプラインに名前を付ける原則に従います。**
For example, feature pipelines can be classified as stream processing (streaming) feature pipelines, batch transformation pipelines, feature validation pipelines, and vector embedding pipelines (that transform source data into vector embeddings and store them in a vector index). 
例えば、**特徴パイプラインは、ストリーム処理（ストリーミング）特徴パイプライン、バッチ変換パイプライン、特徴検証パイプライン、ベクトル埋め込みパイプライン（ソースデータをベクトル埋め込みに変換し、ベクトルインデックスに保存する）に分類**できます。
Similarly, training pipelines can be further decomposed into training dataset creation pipelines (useful for CPU-bound image/video/audio deep learning training pipelines, where you shift-left data transformations to a separate pipeline run on CPUs, not GPUs), model validation pipelines, and model deployment pipelines. 
同様に、トレーニングパイプラインは、トレーニングデータセット作成パイプライン（CPUに依存する画像/動画/音声の深層学習トレーニングパイプラインに役立ち、データ変換をCPU上で実行される別のパイプラインにシフトします）、モデル検証パイプライン、モデルデプロイメントパイプラインにさらに分解できます。
Inference pipelines can be decomposed into batch inference pipelines and online inference pipelines. 
推論パイプラインは、バッチ推論パイプラインとオンライン推論パイプラインに分解できます。

![The feature/training/inference pipeline architecture is a unified architecture for creating batch/real-time/LLM AI systems. The ML pipelines are connected via well-defined APIs to the feature store and model registry.]()

Reference: https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines
参考文献: https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines

<!-- ここまで読んだ! -->

### 2. All Data Transformations for AI are Created Equal AIのための全てのデータ変換は同一で作られる

In a real-time AI system, a client issues a prediction request with some parameters. 
リアルタイムAIシステムでは、クライアントがいくつかのパラメータを持つ予測リクエストを発行します。
A model deployment receives the prediction request and can use any provided entity ID(s) to retrieve precomputed features for that entity. 
モデルデプロイメントは予測リクエストを受け取り、提供されたエンティティIDを使用してそのエンティティの事前計算された特徴を取得できます。
Precomputing features reduces online prediction latency by removing the need to compute them at prediction time. 
**特徴を事前に計算することで、予測時にそれらを計算する必要がなくなり、オンライン予測のレイテンシが減少**します。
However, some features require data only available as part of the prediction request, and need to be computed at request time. 
**しかし、一部の特徴は予測リクエストの一部としてのみ利用可能なデータを必要とし、リクエスト時に計算する必要があります**。(うんうん...!:thinking:)
If we precompute features, we would like them to be reusable across different models. 
特徴を事前に計算する場合、それらが異なるモデル間で再利用可能であることを望みます。(うんうん...!:thinking:)
But my decision tree model doesn’t need to scale the numerical feature, while my deep learning model needs it to be zero-centered and normalized. 
**しかし、私の決定木モデルは数値特徴をスケーリングする必要がない一方で、私の深層学習モデルはそれをゼロ中心化し、正規化する必要があります**。(あ、気になってたところだ! 正規化する前と後のどちらをFeature Storeに保存すべきか...!多分「再利用可能である」という観点からは前者だろうけど...!:thinking:)
Similarly, my CatBoost model can take the categorical string as input, but XGBoost requires me to encode the string before inputting it to the model. 
同様に、私のCatBoostモデルはカテゴリカル文字列を入力として受け取ることができますが、XGBoostはモデルに入力する前に文字列をエンコードする必要があります。

![]()

There is a data transformation taxonomy for AI that has three different types of data transformation: 
AIには、3つの異なるタイプのデータ変換を持つデータ変換の分類法があります。
(taxonomyって「分類法」って訳すのか...!:thinking:)

- model-independent transformations are the same as those found in feature pipelines that create reusable feature data, 
  - モデル非依存の変換は、再利用可能な特徴データを作成する特徴パイプラインに見られるものと同じです。
- model-dependent transformations are often parameterized by the training dataset or are more generally model-specific. 
  - モデル依存の変換は、トレーニングデータセットによってパラメータ化されることが多いか、より一般的にはモデル特有のものです。
   They are performed in both offline training and batch/online inference pipelines. 
   これらは、**オフライントレーニングとバッチ/オンライン推論パイプラインの両方で実行**されます。(つまりfeature storeから取得した後に行うってこと!:thinking:)
   If there is any difference between the implementations in the offline and online pipelines, this skew can introduce subtle but devastating bugs. 
   オフラインとオンラインのパイプラインの実装に違いがある場合、この偏りは微妙だが壊滅的なバグを引き起こす可能性があります。

- on-demand (real-time) transformations to create features using request-time data. 
  - オンデマンド（リアルタイム）変換は、リクエスト時データを使用して特徴を作成します。
   They are performed in both feature pipelines (when backfilling with historical data) and online inference pipelines (on request-time data). 
   これらは、特徴パイプライン（履歴データでバックフィリングする際）とオンライン推論パイプライン（リクエスト時データに対して）で実行されます。
   If there is any difference between the implementations in the offline and online pipelines, this skew can introduce subtle but devastating bugs. 
   オフラインとオンラインのパイプラインの実装に違いがある場合、この偏りは微妙だが壊滅的なバグを引き起こす可能性があります。

Model-independent transformations are the same as those found in data pipelines (extract-transform-load (ETL) pipelines). 
モデル非依存の変換は、データパイプライン（抽出-変換-ロード（ETL）パイプライン）に見られるものと同じです。
However, if you want to support real-time AI systems, you need to support on-demand transformations. 
しかし、リアルタイムAIシステムをサポートしたい場合は、オンデマンド変換をサポートする必要があります。
They enable both real-time feature computation and offline feature computation using historical data - to backfill feature data in feature pipelines. 
これにより、リアルタイムの特徴計算と履歴データを使用したオフラインの特徴計算が可能になり、特徴パイプラインでの特徴データのバックフィリングが行えます。
If you want to support feature reuse, you need model-dependent transformations, delaying scaling/encoding feature data until it is used. 
特徴の再利用をサポートしたい場合は、モデル依存の変換が必要であり、特徴データのスケーリング/エンコーディングを使用されるまで遅延させる必要があります。
If you don’t have explicit support for all three transformations, you will not be able to log untransformed feature data in your inference pipelines. 
3つの変換すべてに対する明示的なサポートがない場合、推論パイプラインで未変換の特徴データをログに記録することはできません。
For example, Databricks only support two of the three transformations and their inference tables store the inputs to models - the scaled/encoded feature data. 
例えば、Databricksは3つの変換のうち2つしかサポートしておらず、彼らの推論テーブルはモデルへの入力（スケーリング/エンコーディングされた特徴データ）を保存します。
That makes it very hard to monitor and debug your features and predictions. 
これにより、特徴や予測を監視し、デバッグすることが非常に難しくなります。
For example, if you are predicting credit card fraud, and the transaction action is 0.78, there is no real-world interpretability for that value. 
例えば、クレジットカード詐欺を予測していて、取引アクションが0.78である場合、その値には実世界での解釈可能性がありません。
What’s more, model monitoring frameworks like NannyML work best with untransformed feature data (from the original feature space). 
さらに、NannyMLのようなモデル監視フレームワークは、未変換の特徴データ（元の特徴空間から）で最も効果的に機能します。

To enable observability for AI systems, untangle your data transformations by following the data transformation taxonomy. 
**AIシステムの可観測性を実現するために、データ変換の分類法に従ってデータ変換を整理**してください。

<!-- ここまで読んだ! -->

### 3. There is no need for a Feature Store 特徴ストアは必要ない

The feature store is the data layer that connects the feature pipelines and the model training/inference pipelines. 
特徴ストアは、特徴パイプラインとモデルのトレーニング/推論パイプラインを接続するデータ層です。
It is possible to build a batch AI system without a feature store if you do not care about reusing features, and you are willing to implement your own solutions for governance, lineage, feature/prediction logging, and monitoring. 
特徴を再利用することにこだわらず、ガバナンス、系譜、特徴/予測のログ記録、監視のための独自のソリューションを実装する意欲があれば、特徴ストアなしでバッチAIシステムを構築することは可能です。
However, if you are working with time-series data, you will also have to roll your own solution for creating point-in-time correct training data from your tables. 
ただし、**時系列データを扱う場合は、テーブルから時点に正しいトレーニングデータを作成するための独自のソリューションを構築する必要があります**。
If you are building a real-time AI system, you will need a feature store (or build one yourself) to provide precomputed features (as context/history) for online models. 
リアルタイムAIシステムを構築する場合は、オンラインモデルのために事前計算された特徴量（コンテキスト/履歴として）を提供するために、特徴ストアが必要です（または自分で構築する必要があります）。
The feature store also ensures there is no skew between your model-dependent and on-demand transformations, see Figure 3. 
特徴ストアは、モデル依存の変換とオンデマンド変換の間に偏りがないことを保証します（図3を参照）。
It also helps you backfill feature data from historical data sources. 
また、歴史的データソースから特徴データをバックフィルするのにも役立ちます。

![]()

<!-- ここまで読んだ! -->

In short, without a feature store, you may be able to roll out your first batch AI system, without any platform for collaboration, governance, or reuse of features, but your velocity for each additional batch model will not improve. 
要するに、特徴ストアなしで最初のバッチAIシステムを展開することは可能ですが、コラボレーション、ガバナンス、または特徴の再利用のためのプラットフォームがないため、追加のバッチモデルごとの速度は向上しません。
Building batch AI systems without a feature store would be akin to analytics without a data warehouse. 
特徴ストアなしでバッチAIシステムを構築することは、データウェアハウスなしでの分析に似ています。
It can work, but won’t scale. 
**機能することはありますが、スケールしません。**
For real-time AI systems, you will need a feature store to provide history/context to online models and infrastructure for ensuring correct, governed, and observable features. 
リアルタイムAIシステムには、オンラインモデルに履歴/コンテキストを提供し、正確でガバナンスされた観察可能な特徴を確保するためのインフラストラクチャを提供するために、特徴ストアが必要です。

<!-- ここまで読んだ! -->

### 4. Experiment Tracking is part of MLOps 実験追跡はMLOpsの一部である

Many teams erroneously believe that the starting point for building AI systems is installing an experiment tracking service. 
多くのチームは、AIシステムを構築するための出発点は実験追跡サービスのインストールであると誤って信じています。
Making experiment tracking a prerequisite will slow you down in getting to your first minimal viable AI system. 
実験追跡を前提条件にすると、最初の最小限の実用的なAIシステムに到達するのが遅くなります。
Experiment tracking is premature optimization in MLOps. 
**実験追跡はMLOpsにおける早すぎる最適化です。**
For operational needs, such as model storage, governance, model performance/bias evaluation, and model cards, you should use a model registry. 
モデルの保存、ガバナンス、モデルのパフォーマンス/バイアス評価、モデルカードなどの運用ニーズには、モデルレジストリを使用すべきです。
Experiment tracking is primarily for research. 
実験追跡は主に研究のためのものです。
However, like the monkey ladder experiment, where monkeys continue to beat up any monkey that tries to climb the rope (even though they don’t know why they do it), many ML engineers believe the starting point in MLOps is to install an experiment tracking service. 
しかし、猿の梯子実験のように、猿たちがロープを登ろうとする猿を殴り続ける（なぜそうするのかは知らないにもかかわらず）ように、多くのMLエンジニアはMLOpsの出発点は実験追跡サービスのインストールであると信じています。
(まあ確かに、実験trackingサービスが最初ではない、というのは共感するかな。オンライン評価がすでにできる状況の場合はそっちでやればいいし...!:thinking:)

<!-- ここまで読んだ! -->

### 5. MLOpsはMLのためのDevOpsに過ぎない

DevOps is a software development process where you write unit, integration, and systems tests for your software, and whenever you make changes to your source code, you automatically execute those tests using a continuous integration continuous deployment (CI/CD) process. 
DevOpsは、ソフトウェアのためにユニットテスト、統合テスト、システムテストを作成し、ソースコードに変更を加えるたびに、継続的インテグレーション・継続的デプロイメント（CI/CD）プロセスを使用して自動的にそれらのテストを実行するソフトウェア開発プロセスです。
This typically involves a developer pushing source code changes to a source code repository that then triggers automated tests on a CI/CD service that checks out your source code onto containers, compiles/builds the code, runs the tests, packages the binaries, and deploys the binaries if all the tests are successful. 
通常、開発者はソースコードの変更をソースコードリポジトリにプッシュし、それがCI/CDサービス上で自動テストをトリガーします。このサービスは、ソースコードをコンテナにチェックアウトし、コードをコンパイル/ビルドし、テストを実行し、バイナリをパッケージし、すべてのテストが成功した場合にバイナリをデプロイします。

MLOps, however, is more than DevOps. 
しかし、MLOpsはDevOps以上のものです。
In MLOps, in addition to the automated testing of the source code for your machine learning pipelines, you also need to version and test the input data. 
MLOpsでは、**機械学習パイプラインのソースコードの自動テストに加えて、入力データのバージョン管理とテストも必要**です。
Data tests could be evals for LLMs that test whether changes in your prompt template, multi-shot prompts, RAG, or LLM improve or worsen the performance of your AI system. 
データテストは、プロンプトテンプレート、マルチショットプロンプト、RAG、またはLLMの変更がAIシステムのパフォーマンスを改善または悪化させるかどうかをテストするLLM用のevalsである可能性があります。
Similarly, data validation tests for classical ML systems prevent garbage-in (training data) producing garbage-out (from models). 
同様に、古典的なMLシステムのデータ検証テストは、ゴミデータ（トレーニングデータ）がゴミ出力（モデルから）を生成するのを防ぎます。
There is also the challenge that AI system performance tends to degrade over time, due to data drift and model drift. 
また、AIシステムのパフォーマンスは、データドリフトやモデルドリフトのために時間とともに劣化する傾向があるという課題もあります。
For this, you need to monitor the distribution of inference data and model predictions. 
これに対処するためには、推論データとモデル予測の分布を監視する必要があります。
(まああとは「継続的学習」を前提とした仕組みで対処するとかかな〜:thinking:)

<!-- ここまで読んだ! -->

### 6. Versioning Models is enough for Safe Upgrade/Rollbacks バージョン管理モデルは安全なアップグレード/ロールバックに十分である

For a real-time AI system (with a model deployment), your versioned model should be tightly coupled to any versioned precomputed feature data (feature group) it uses. 
モデルデプロイメントを伴うリアルタイムAIシステムでは、バージョン管理されたモデルは使用する任意のバージョン管理された事前計算された特徴量データ（フィーチャーグループ）と密接に結びついている必要があります。
It is not enough to just upgrade the version of your model. 
モデルのバージョンを単にアップグレードするだけでは不十分です。
You need to upgrade the model version in sync with upgrading the version of the feature group used by the online model. 
**オンラインモデルで使用されるフィーチャーグループのバージョンをアップグレードするのと同期して、モデルのバージョンをアップグレードする必要があります。**(なるほど?? でもまあモデル新旧バージョンの違いの内容にもよるけど...!:thinking:)

![]()

In Figure 4, you can see that when you upgrade the airquality model to v2, you need to connect it to the precomputed features in v2 of the air_quality Feature Group. 
図4では、airqualityモデルをv2にアップグレードする際に、air_qualityフィーチャーグループのv2にある事前計算された特徴に接続する必要があることがわかります。
V1 of the model was connected to v1 of the air_quality Feature Group. 
モデルのv1は、air_qualityフィーチャーグループのv1に接続されていました。
The same is true for rolling back a model to a previous version, this needs to be done in sync with the feature group version. 
モデルを以前のバージョンにロールバックする場合も同様で、これもフィーチャーグループのバージョンと同期して行う必要があります。
(これはモデル新旧バージョンの違いの内容にもよるけど...!:thinking:)

<!-- ここまで読んだ! -->

### 7. データバージョニングは不要　(timestampでの管理ってことね...!:thinking:)

Reproducibility of training data (often needed for compliance) requires data versioning. 
トレーニングデータの再現性（しばしばコンプライアンスのために必要）はデータバージョニングを必要とします。
For example, consider Figure 5 where we have late arriving data after Training Dataset v1 was created. 
例えば、トレーニングデータセットv1が作成された後に遅れて到着したデータがあるFigure 5を考えてみましょう。
Without data versioning, if you re-create training dataset V1 at a later point in time using only the date of the desired Air Quality Measurements, the late measurements that arrived just after V1 was created will be included in the training data. 
データバージョニングがなければ、望ましい空気質測定の日時のみを使用して後の時点でトレーニングデータセットV1を再作成すると、V1が作成された直後に到着した遅れた測定値がトレーニングデータに含まれてしまいます。
Data versioning enables you to re-create the training data exactly as it was at the point-in-time when it was originally created. 
データバージョニングにより、元々作成された時点でのトレーニングデータを正確に再作成することが可能になります。
Data versioning requires a data layer that knows about the ingestion time for data points and the event-time of data points. 
データバージョニングには、データポイントの取り込み時間とイベント時間を把握しているデータレイヤーが必要です。

### 誤謬8. The Model Signature is the API for Model Deployments モデルシグネチャはモデルデプロイメントのAPIである

(ここでの主張 = 「APIとモデルを分離しておけば、裏のモデルを変えてもクライアント側を作り直す必要ない」って話??:thinking:)

A real-time AI system uses a model deployment that makes predictions in response to prediction requests.  
リアルタイムAIシステムは、予測リクエストに応じて予測を行うモデルデプロイメントを使用します。
The parameters that are sent by the client to the Model Deployment API are typically not the same as the input parameters to the model (the model signature).  
クライアントがModel Deployment APIに送信するパラメータは、通常、モデルへの入力パラメータ（モデルシグネチャ）とは異なります。
In Figure 6, you can see an example of an online inference pipeline for a credit card fraud detection model.  
図6では、クレジットカード不正検出モデルのオンライン推論パイプラインの例を見ることができます。
You can see here that the Deployment API includes details about the credit card transaction (amount, credit_card_number, ip_address (of the payment provider)).  
ここでは、Deployment APIがクレジットカード取引に関する詳細（amount、credit_card_number、ip_address（支払いプロバイダーの））を含んでいることがわかります。
This is the interface between clients and the model deployment.  
これは、クライアントとモデルデプロイメントの間のインターフェースです。
Following the information hiding principle, you could redeploy a new version of the model (even changing its signature), without requiring clients to be rebuilt if the deployment API remains unchanged.  
情報隠蔽の原則に従えば、デプロイメントAPIが変更されない限り、クライアントを再構築することなく、モデルの新しいバージョン（シグネチャを変更することさえも）を再デプロイすることができます。
In this example, the parameters sent by the client are used to lookup precomputed features (1hr_spend, 1day_spend), compute on-demand features (card_present, location), and a model-dependent transformation is applied to one of the features (normalize the amount).  
この例では、クライアントから送信されたパラメータは、事前計算された特徴（1hr_spend、1day_spend）を検索し、オンデマンドで特徴（card_present、location）を計算し、特徴の1つにモデル依存の変換（amountの正規化）を適用するために使用されます。
The model’s deployment API is decoupled from the API to the model - the model signature.  
モデルのデプロイメントAPIは、モデルへのAPI（モデルシグネチャ）から切り離されています。

You may think that LLM AI systems are exempt from this fallacy, but LLM deployment APIs that use retrieval augmented generation (RAG) or function calling often have both the prompt text as well as non-text parameters that used to retrieve examples that are included in the final encoded prompt.  
LLM AIシステムはこの誤謬から免れていると思うかもしれませんが、retrieval augmented generation（RAG）や関数呼び出しを使用するLLMデプロイメントAPIは、最終的にエンコードされたプロンプトに含まれる例を取得するために使用されるプロンプトテキストと非テキストパラメータの両方を持つことがよくあります。
The LLM signature is the encoded prompt.  
LLMシグネチャはエンコードされたプロンプトです。

<!-- ここまで読んだ! -->

### 9. Prediction Latency is the Time taken for the Model Prediction 予測レイテンシはモデル予測にかかる時間です
(あ、特徴量の取得とかモデル依存変換とかも含めた全体の時間ってことね...!:thinking:)

Model prediction can be fast on your laptop but slow in a deployed model. 
モデルの予測は、あなたのラップトップでは速いかもしれませんが、デプロイされたモデルでは遅くなることがあります。
Why is that? 
なぜでしょうか？
When you serve a model behind a network endpoint, you typically have to perform a lot of operations before you finally call model.predict() with the final feature vector(s) as input. 
ネットワークエンドポイントの背後でモデルを提供する場合、最終的な特徴ベクトルを入力としてmodel.predict()を呼び出す前に、多くの操作を実行する必要があります。
You may need to retrieve precomputed features from a feature store or a vector index, create features from request parameters with on-demand transformations, encode/scale/shift feature values with model-dependent transformations, log untransformed feature values, and finally call predict on the model, before returning a result. 
事前に計算された特徴をフィーチャーストアやベクトルインデックスから取得したり、リクエストパラメータからオンデマンド変換を用いて特徴を作成したり、モデル依存の変換を用いて特徴値をエンコード/スケール/シフトしたり、変換されていない特徴値をログに記録したりして、結果を返す前にモデルでpredictを呼び出す必要があります。
All of these steps add latency to the prediction request, as does the client latency to the model deployment network endpoint, see Figure 7. 
これらすべてのステップは予測リクエストにレイテンシを追加し、モデルデプロイメントネットワークエンドポイントへのクライアントレイテンシも同様です。図7を参照してください。

<!-- ここまで読んだ! -->

### 10. LLMOpsはMLOpsではない

LLMs need GPUs for inference and fine-tuning. 
LLMは推論とファインチューニングのためにGPUを必要とします。
Similarly, LLMs need support for scalable compute, scalable storage, and scalable model serving. 
同様に、LLMはスケーラブルなコンピューティング、スケーラブルなストレージ、およびスケーラブルなモデル提供のサポートを必要とします。
However, many MLOps platforms do not support either GPUs or scale, and the result is that LLMs are often seen as outside of MLOps, part of a new LLMOps discipline. 
しかし、多くのMLOpsプラットフォームはGPUやスケールをサポートしておらず、その結果、LLMはしばしばMLOpsの外にあるものと見なされ、新しいLLMOpsの分野の一部とされています。
However, LLMs still follow the same FTI architecture, see Figure 8. 
しかし、LLMは依然として同じFTIアーキテクチャに従います。図8を参照してください。

![Figure 8. The FTI architecture applied to LLM systems. The only real change is syntactic - online inference pipelines are now called agents. ]()

If your MLOps platform supports GPUs and scale, LLMOps is just MLOps with LLMs. 
もしあなたのMLOpsプラットフォームがGPUとスケールをサポートしているなら、LLMOpsは単にLLMを用いたMLOpsです。
Feature pipelines are used to chunk, clean, and score text for instruction and alignment datasets. 
フィーチャーパイプラインは、指示および整列データセットのためにテキストをチャンク化、クリーンアップ、スコアリングするために使用されます。
They are also used to compute vector embeddings that are stored in a vector index for RAG. 
また、RAGのためにベクトルインデックスに保存されるベクトル埋め込みを計算するためにも使用されます。
Training pipelines are used to fine-tune and align foundation LLMs. 
トレーニングパイプラインは、基盤となるLLMをファインチューニングし、整列させるために使用されます。
Tokenization is a model-dependent transformation that needs to be consistent between training and inference - without platform support, users often slip up using the wrong version of the tokenizer for their LLM in inference. 
トークン化はモデル依存の変換であり、トレーニングと推論の間で一貫性が必要です。プラットフォームのサポートがない場合、ユーザーはしばしば推論時に自分のLLMに対して間違ったバージョンのトークナイザーを使用してしまいます。
Agents and workflows are found in online inference pipelines, as are calls to external systems with RAG and function calling. 
エージェントとワークフローはオンライン推論パイプラインに存在し、RAGや関数呼び出しを伴う外部システムへの呼び出しもあります。
Your MLOps team should be able to bring the same architecture and tools to bear on LLM systems as it does with batch and real-time AI systems. 
**あなたのMLOpsチームは、バッチおよびリアルタイムAIシステムと同様に、LLMシステムに対しても同じアーキテクチャとツールを適用できるべき**です。


<!-- ここまで読んだ! -->

## The Effects of the Fallacies 誤謬の影響

1. Without a unified architecture for building AI systems, every new batch or real-time AI system you build will be like starting from scratch. 
   統一されたAIシステム構築のアーキテクチャがないと、新しいバッチまたはリアルタイムのAIシステムを構築するたびに、ゼロから始めることになります。 
   This makes it difficult for developers to transition from building one type of AI system to another. 
   これにより、開発者はある種のAIシステムから別のシステムに移行するのが難しくなります。 
   Without a clear architecture, data scientists only learn to fit training data to models, not how to create features from non-static data sources and build inference data for predictions. 
   明確なアーキテクチャがないと、データサイエンティストはトレーニングデータをモデルに適合させることだけを学び、非静的データソースから特徴を作成し、予測のための推論データを構築する方法を学びません。 
   (“Data is not static” was another fallacy we considered, but was considered a bit too obvious for inclusion). 
   （「データは静的ではない」というのも考慮した誤謬でしたが、あまりにも明白すぎるため、含めるには適さないと判断されました）。

2. Good luck building an observable AI system (that logs untransformed feature data) when you have tangled data transformations. 
   複雑なデータ変換があるときに、観測可能なAIシステム（変換されていない特徴データをログする）を構築するのは大変です。 
   If you don’t untangle your data transformations into model-independent, model-dependent, and on-demand transformations, 
   **データ変換をモデルに依存しない、モデルに依存する、オンデマンドの変換に整理しないと**、 
   you will have difficulty building an observable AI system that logs/monitors interpretable features. 
   解釈可能な特徴をログ/監視する観測可能なAIシステムを構築するのが難しくなります。

3. You will end up building your own AI platform and spending most of your time figuring out how to manage mutable data, 
   結局、自分自身のAIプラットフォームを構築し、可変データを管理する方法を見つけるのにほとんどの時間を費やすことになります。 
   how to create point-in-time correct training data, 
   **時点に正しいトレーニングデータを作成する方法**、 
   how to synchronize data in columnar datastores with low-latency row-oriented stores for online inference. 
   **オンライン推論のために、列指向データストアと低遅延の行指向ストアのデータを同期する方法を見つけることになります**。 
   You will use less features in your online models, because of the pain in making them available as precomputed features. 
   事前計算された特徴として利用可能にするのが難しいため、オンラインモデルで使用する特徴は少なくなります。 
   The cost to build and deploy every new model will always be high and not go down over time as fast as it would with a feature store. 
   新しいモデルを構築して展開するコストは常に高く、フィーチャーストアがあった場合のように時間とともに下がることはありません。

4. Developers will not know the API to a model deployment. 
   開発者はモデル展開のAPIを知らないでしょう。 
   Some developers will think it is the same as the ordered set of input data types for the model - the model signature. 
   一部の開発者は、モデルの入力データ型の順序付きセット、すなわちモデルシグネチャと同じだと思うでしょう。 
   You will not have an explicit schema for accessing the deployment, 
   展開にアクセスするための明示的なスキーマがないため、 
   and mistakes will be made in using the model deployment and whenever maintenance or upgrades occur. 
   モデル展開の使用やメンテナンス、アップグレードの際にミスが発生します。

5. Your data layer for your AI system may get contaminated with bad data if you do not validate data ingested. 
   データを検証しないと、AIシステムのデータ層が不良データで汚染される可能性があります。 
   Your AI system performance may degrade over time due to a lack of feature monitoring and model performance monitoring. 
   特徴の監視やモデルのパフォーマンス監視が不足しているため、AIシステムのパフォーマンスは時間とともに低下する可能性があります。

6. You will show your boss loss curves for model training to show your progress. 
   あなたは進捗を示すために、モデルトレーニングの損失曲線を上司に見せるでしょう。 
   But your boss will know that experiment tracking side tracks you from real MLOps - building your minimal viable AI system. 
   しかし、上司は**実験追跡があなたを本当のMLOps、すなわち最小限の実用的なAIシステムの構築から逸らすこと**を知っています。 
   Experiment tracking should be the last capability you add, not the first. 
   **実験追跡は最初に追加すべき機能ではなく、最後に追加すべき**です。 
   You should focus on adding value first through data-centric AI, 
   **まずはdata-centric AIを通じて価値を追加することに集中すべき**です、 
   and only progress to model-centric AI (and experiment tracking) when you have to. 
   そして、**必要なときにのみモデル中心のAI（および実験追跡）に進むべき**です。

7. If you do not couple model versions with feature data versions, you can introduce subtle bugs. 
   モデルバージョンと特徴データバージョンを結びつけないと、微妙なバグを引き起こす可能性があります。 
   For example, if your new model uses the old feature version data, 
   例えば、新しいモデルが古い特徴バージョンのデータを使用する場合、 
   but the new feature group version is schema compatible with the previous version, 
   しかし、新しい特徴グループバージョンが前のバージョンとスキーマ互換性がある場合、 
   then the system will appear to work as before. 
   その場合、システムは以前と同じように動作しているように見えます。 
   However, as the implementation of one or more features differs, its performance will suffer and it will be a hard bug to find. 
   しかし、1つ以上の特徴の実装が異なるため、そのパフォーマンスは低下し、バグを見つけるのが難しくなります。

8. AI regulation is coming, and the source of bias in many models is their training data. 
   AI規制が進んでおり、多くのモデルにおけるバイアスの原因はトレーニングデータです。 
   If you cannot provide lineage to training datasets and you cannot recreate them from their source data, 
   トレーニングデータセットの系譜を提供できず、元のデータから再作成できない場合、 
   you may be in legal jeopardy. 
   法的な危険にさらされる可能性があります。 
   If you only depend on the event-time of your data when creating training datasets, 
   **トレーニングデータセットを作成する際にデータのイベント時間のみに依存すると、** 
   it will not recreate training data or batch inference data ASOF the point-in-time it was originally created. 
   元々作成された時点のトレーニングデータやバッチ推論データを再作成することはできません。 
   Your data storage system needs support for time-travel with ingestion time to support reproducible training datasets. 
   **再現可能なトレーニングデータセットをサポートするために、データストレージシステムは取り込み時間でのタイムトラベルをサポートする必要があります。**
   (ここまだよくわかってないんだよなぁ...event_timeだけでは不十分なケースってあるっけ??:thinking:)
   

9. You cannot assume that prediction latency for network hosted models is only the time taken for the model prediction. 
   ネットワークホストモデルの予測レイテンシがモデル予測にかかる時間だけであると仮定してはいけません。 
   You have to include the time for all pre-processing (building feature vectors, RAG, etc) and post-processing (feature/prediction logging). 
   すべての前処理（特徴ベクトルの構築、RAGなど）および後処理（特徴/予測のログ記録）にかかる時間を含める必要があります。

10. You may duplicate your AI infrastructure by supporting a separate LLMOps stack from your MLOps stack. 
    **MLOpsスタックとは別にLLMOpsスタックをサポートすることで、AIインフラストラクチャを重複させる可能性があります。** 
    For example, most feature stores now support vector indexes - you do not need a separate vector DB for RAG. 
    例えば、ほとんどのフィーチャーストアは現在ベクトルインデックスをサポートしているため、RAG用に別のベクトルDBは必要ありません。 
    Similarly, LLMs and deep learning models both require GPUs and they should be managed in the same platform (to improve GPU utilization levels). 
    同様に、LLMと深層学習モデルはどちらもGPUを必要とし、同じプラットフォームで管理されるべきです（GPUの利用率を向上させるため）。 
    Finally, developers should be able to easily transition from batch/real-time AI systems to a LLM AI system - if you follow the FTI architecture. 
    最後に、開発者はバッチ/リアルタイムのAIシステムからLLM AIシステムに簡単に移行できるべきです - FTIアーキテクチャに従う場合は。

<!-- ここまで読んだ! -->

## Summary 概要

The MLOps fallacies presented here are assumptions that architects and designers of AI systems can make that work against the main goals of MLOps - to get to a working AI system as quickly as possible, to tighten the development loop, and to improve system quality through continuous delivery and automated testing and versioning. 
ここで示されるMLOpsの誤謬は、AIシステムのアーキテクトやデザイナーが行う可能性のある仮定であり、**MLOpsの主な目標である「できるだけ早く動作するAIシステムを構築すること」「開発ループを短縮すること」「継続的なデリバリー、自動テスト、バージョン管理を通じてシステムの品質を向上させること」に反するもの**です。
Falling for the MLOps fallacies results in AI projects either taking longer to reach production or failing to reach production.
**MLOpsの誤謬に陥ると、AIプロジェクトは生産に到達するのに時間がかかるか、生産に到達できない結果になります。**
Thanks to the following people for reviewing a draft of this post:Raphaël Hoogvliets,Maria Vechtemova,Paul Izustin,Miguel Otero Pedrido, andAurimas Griciūnas.
この投稿のドラフトをレビューしてくれた以下の方々に感謝します：Raphaël Hoogvliets、Maria Vechtemova、Paul Izustin、Miguel Otero Pedrido、そしてAurimas Griciūnas。

<!-- ここまで読んだ! -->

## References 参考文献
### Interested for more? もっと興味がありますか？
- 🤖 Register for free on Hopsworks Serverless 
- 🌐 Read about the open, disaggregated AI Lakehouse stack 
- 📚 Get your early copy: O'Reilly's 'Building Machine Learning Systems' book 
- 🛠️ Explore all Hopsworks Integrations 
- 🧩 Get started with codes and examples 
- ⚖️ Compare other Feature Stores with Hopsworks 


<!-- ここまで読んだ! -->
