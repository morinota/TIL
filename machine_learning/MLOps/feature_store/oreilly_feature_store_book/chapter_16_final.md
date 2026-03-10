
## 1. The Dirty Dozen of Fallacies of MLOps MLOpsの誤謬のダーティダース

There are a number of fallacies (bad assumptions) that MLOps practitioners often make that cause AI systems to never make it to production. 
**MLOpsの実践者がしばしば犯す誤謬（悪い仮定）がいくつかあり、それがAIシステムが本番環境に到達しない原因**となります。
We have covered these fallacies in earlier chapters, but I present them here as a refresher to show you what happens if you fall for a fallacy: 
これらの誤謬については以前の章で取り上げましたが、ここでは誤謬に陥った場合に何が起こるかを示すために再確認として提示します。

### 1.1. _1. Do it all in one monolithic ML pipeline_ 
_1. すべてを一つのモノリシックなMLパイプラインで行う_

We saw that you can write a batch ML system as a single monolithic pipeline (parameterized to run in either training or inference mode). 
バッチMLシステムを単一のモノリシックパイプラインとして記述できることを見ました（トレーニングモードまたは推論モードで実行するようにパラメータ化されています）。
However, you cannot run a real-time ML system as a single ML pipeline, nor can you build an agentic RAG system with a single program. 
しかし、リアルタイムMLシステムを単一のMLパイプラインとして実行することはできず、単一のプログラムでエージェント的なRAGシステムを構築することもできません。

_The effects of this fallacy and how to overcome it: Without a unified architecture for building AI systems, building every new batch or real-time AI system will be like starting from scratch. 
_この誤謬の影響とそれを克服する方法：AIシステムを構築するための統一されたアーキテクチャがないと、すべての新しいバッチまたはリアルタイムAIシステムを構築することは、ゼロから始めるようなものになります。
This makes it difficult for developers to transition from building one type of AI system to another. 
これにより、開発者があるタイプのAIシステムから別のタイプのAIシステムに移行することが難しくなります。
You overcome this challenge by decomposing your AI system into feature/training/inference pipelines (FTI pipelines) that are connected to make up your batch/real-time/LLM AI system. 
この課題を克服するためには、AIシステムを特徴/トレーニング/推論パイプライン（FTIパイプライン）に分解し、それらを接続してバッチ/リアルタイム/LLM AIシステムを構成します。

### 1.2. _2. Data for AI is static_ 
_2. AIのためのデータは静的である_

Data scientists who learned to train models with static datasets are accustomed to models that only make predictions, and create value, once. 
静的データセットでモデルをトレーニングすることを学んだデータサイエンティストは、一度だけ予測を行い、価値を生み出すモデルに慣れています。
In the real world, AI systems work with dynamic data sources and repeatedly create value from new data as it arrives. 
実世界では、AIシステムは動的データソースで機能し、新しいデータが到着するたびに繰り返し価値を生み出します。

_The effects of this fallacy and how to overcome it: Developers have difficulty working with dynamic data sources if they don’t have the skills needed to extract and manage data from them. 
_この誤謬の影響とそれを克服する方法：開発者は、動的データソースからデータを抽出し管理するために必要なスキルを持っていない場合、動的データソースで作業するのが難しいです。
Developers have difficulty distinguishing between batch ML systems that make predictions on a schedule and real-time ML systems that make predictions in response to prediction requests. 
開発者は、スケジュールに基づいて予測を行うバッチMLシステムと、予測リクエストに応じて予測を行うリアルタイムMLシステムを区別するのが難しいです。
You overcome this by following the FTI architecture when building your AI system.  
AIシステムを構築する際にFTIアーキテクチャに従うことで、この問題を克服します。

### 1.3. _3. All data transformations for AI are created equal_ 
_3. AIのためのすべてのデータ変換は平等に作成される_

Data transformations are not all the same. 
データ変換はすべて同じではありません。
Model-independent transformations create reusable feature data in feature pipelines. 
モデルに依存しない変換は、特徴パイプラインで再利用可能な特徴データを作成します。
Model-dependent transformations are performed after reading data from the feature store and need to be implemented consistently in both training and inference pipelines. 
モデルに依存する変換は、フィーチャーストアからデータを読み取った後に実行され、トレーニングパイプラインと推論パイプラインの両方で一貫して実装する必要があります。
On-demand transformations create features using request-time data. 
オンデマンド変換は、リクエスト時のデータを使用して特徴を作成します。
They are performed in both feature pipelines when backfilling with historical data and online inference pipelines on request-time data. 
それらは、履歴データでバックフィルする際のフィーチャーパイプラインと、リクエスト時データに基づくオンライン推論パイプラインの両方で実行されます。
There should be no skew between the feature pipeline and online inference pipeline implementations of on-demand transformations. 
オンデマンド変換のフィーチャーパイプラインとオンライン推論パイプラインの実装の間に偏りがあってはなりません。

_The effects of this fallacy and how to overcome it: If you don’t support model-dependent transformations, you won’t reuse features in your feature store. 
_この誤謬の影響とそれを克服する方法：モデルに依存する変換をサポート(=考慮)しない場合、フィーチャーストアで特徴を再利用することはできません。
If you don’t support on-demand transformations, you won’t have the same code to compute real-time features from prediction request parameters and backfill feature data in feature pipelines. 
オンデマンド変換をサポート(=考慮)しない場合、予測リクエストパラメータからリアルタイム特徴を計算し、フィーチャーパイプラインで特徴データをバックフィルするための同じコードを持つことはできません。
If you don’t support both model-dependent and on-demand transformations, you’ll have difficulty building an observable AI system that logs/monitors interpretable features. 
モデルに依存する変換とオンデマンド変換の両方をサポート(=考慮)しない場合、解釈可能な特徴をログ/監視する可観測なAIシステムを構築するのが難しくなります。
The solution is to untangle your data transformations into model-independent, model-dependent, and on-demand transformations. 
解決策は、データ変換をモデルに依存しない、モデルに依存する、オンデマンドの変換に分解することです。

### 1.4. _4. There is no need for a feature store_ 
_4. フィーチャーストアは必要ない_

The feature store is the data layer that connects the feature pipelines and the training/inference pipelines. 
フィーチャーストアは、フィーチャーパイプラインとトレーニング/推論パイプラインを接続するデータ層です。
Building a batch ML system without a feature store is possible if you do not care about reusing features and are willing to implement your own solutions for governance, lineage, feature/prediction logging, and monitoring. 
フィーチャーストアなしでバッチMLシステムを構築することは、特徴を再利用することを気にせず、ガバナンス、系譜、特徴/予測ログ、監視のための独自のソリューションを実装することを厭わない場合は可能です。
However, if you are working with time-series data, you will also have to roll your own solution for creating point-in-time correct training data from your tables. 
**ただし、時系列データを扱っている場合は、テーブルから時点に正しいトレーニングデータを作成するための独自のソリューションを構築する必要があります。**
If you are building a real-time ML system, you will need to have a feature store (or build one yourself) to provide precomputed features (as context/history) for online models. 
リアルタイムMLシステムを構築している場合は、オンラインモデルのために事前計算された特徴（コンテキスト/履歴として）を提供するためにフィーチャーストアを持つ必要があります（または自分で構築する必要があります）。
The feature store also ensures there is no skew between your offline and online transformations. 
フィーチャーストアは、オフラインとオンラインの変換の間に偏りがないことを保証します。
In short, without a feature store, you may be able to roll out your first batch ML system, but your velocity for each additional batch model will not improve. 
要するに、フィーチャーストアなしで最初のバッチMLシステムを展開することはできるかもしれませんが、追加のバッチモデルごとの速度は向上しません。
For real-time ML systems, you will need a feature store to provide history/context to online models and infrastructure to ensure correct, governed, and observable features. 
リアルタイムMLシステムの場合、オンラインモデルに履歴/コンテキストを提供し、正確でガバナンスされた可観測な特徴を確保するためのインフラストラクチャを持つためにフィーチャーストアが必要です。

_The effects of this fallacy and how to overcome it: You will end up building the feature store capabilities yourself, spending much of your time figuring out how to work correctly with mutable data, how to create point-in-time correct training data, and how to synchronize data in columnar datastores with low-latency row-oriented stores for online inference. 
_この誤謬の影響とそれを克服する方法：フィーチャーストアの機能を自分で構築することになり、可変データで正しく作業する方法、時点に正しいトレーニングデータを作成する方法、オンライン推論のために列指向ストアと低遅延の行指向ストアでデータを同期する方法を見つけるのに多くの時間を費やすことになります。
You will use fewer features in your online models because of the effort required to make them available as precomputed features. 
事前計算された特徴として利用可能にするために必要な労力のため、オンラインモデルで使用する特徴は少なくなります。
You will not normalize your data models (in a snowflake schema), as it will be too hard. 
データモデルを正規化することは（スノーフレークスキーマで）、あまりにも難しいため、行いません。
The cost to build and deploy every new model will always be high and not go down over time. 
新しいモデルを構築して展開するコストは常に高く、時間が経つにつれて下がることはありません。
The solution is to use a feature store. 
解決策は、フィーチャーストアを使用することです。

### 1.5. _5. Experiment tracking is required for MLOps_ 
_5. 実験追跡はMLOpsに必要である_

Many teams erroneously believe that installing an experiment-tracking service is the starting point for building AI systems. 
多くのチームは、実験追跡サービスをインストールすることがAIシステムを構築するための出発点であると誤って信じています。
Experiment tracking will slow you down in getting to your first MVPS. 
実験追跡は、最初のMVPSに到達するのを遅くします。
Experiment tracking is premature optimization in MLOps. 
**実験追跡はMLOpsにおける早すぎる最適化です。**
You can use a model registry for operational needs, such as model storage, governance, model performance/bias evaluation, and model cards. 
モデルストレージ、ガバナンス、モデルのパフォーマンス/バイアス評価、モデルカードなどの運用ニーズには、モデルレジストリを使用できます。
Experiment tracking is a research journal for model training. 
実験追跡はモデルトレーニングのための研究ジャーナルです。

_The effects of this fallacy and how to overcome it: Just like the monkey rope experiment, in which monkeys continue to beat up any monkey that tries to climb the rope (even though none of the monkeys know why they are not supposed to climb the rope), many ML engineers think that the start of an MLOps project is to install an experiment-tracking service. 
_この誤謬の影響とそれを克服する方法：猿のロープ実験のように、猿たちはロープを登ろうとする猿を叩き続けます（どの猿もなぜロープを登ってはいけないのかを知らないにもかかわらず）、多くのMLエンジニアはMLOpsプロジェクトの開始は実験追跡サービスをインストールすることだと考えています。
The solution is to start with the model registry to store required metadata about models and their training runs, until you actually need an experiment-tracking service (which most ML engineers will probably never need). 
解決策は、モデルとそのトレーニング実行に関する必要なメタデータを保存するためにモデルレジストリから始めることです。実際に実験追跡サービスが必要になるまで（ほとんどのMLエンジニアはおそらく必要ないでしょう）。

<!-- ここまで読んだ! -->

### 1.6. _6. MLOps is just DevOps for ML_ 
_6. MLOpsはMLのためのDevOpsに過ぎない_

Like DevOps, MLOps requires the automated testing of the source code for your pipelines, but unlike DevOps, in MLOps you also need to version and test the input data. 
DevOpsと同様に、MLOpsはパイプラインのソースコードの自動テストを必要としますが、DevOpsとは異なり、MLOpsでは入力データのバージョン管理とテストも必要です。
Data validation tests prevent garbage in from producing garbage out. 
データ検証テストは、ゴミが入ることを防ぎ、ゴミが出ることを防ぎます。
Similarly, model validation tests have no corollary in DevOps. 
同様に、モデル検証テストはDevOpsには相当するものがありません。
There is also the difference that AI system performance tends to degrade over time, due to data and model drift. 
**AIシステムのパフォーマンスは、データとモデルのドリフトにより、時間とともに劣化する傾向があります。**

_The effects of this fallacy and how to overcome it: Without data tests, your training or inference data may get contaminated. 
_この誤謬の影響とそれを克服する方法：データテストがないと、トレーニングデータや推論データが汚染される可能性があります。
Without model tests, your models may have bias or poor performance. 
モデルテストがないと、モデルにバイアスやパフォーマンスの低下が生じる可能性があります。
Your AI system’s performance may degrade over time due to a lack of feature monitoring and model performance monitoring. 
特徴の監視やモデルパフォーマンスの監視が不足しているため、AIシステムのパフォーマンスが時間とともに劣化する可能性があります。
Follow MLOps best practices for offline data validation, model validation, and feature/model monitoring. 
オフラインデータ検証、モデル検証、特徴/モデル監視のためのMLOpsのベストプラクティスに従ってください。

<!-- ここまで読んだ! -->

### 1.7. _7. Versioning models is enough for safe upgrade/rollback_ 
_7. モデルのバージョン管理だけでは安全なアップグレード/ロールバックには不十分である_

For a stateful, real-time ML system, the model deployment is tightly coupled to the versioned feature views that provide it with precomputed features. 
状態を持つリアルタイムMLシステムでは、モデルのデプロイメントは、事前計算された特徴を提供するバージョン管理されたフィーチャービューに密接に結びついています。
When you upgrade a model deployment, it is not enough to just update the model version. 
モデルのデプロイメントをアップグレードする際には、モデルのバージョンを更新するだけでは不十分です。
You may also need to upgrade the version of the feature view used by the model deployment. 
モデルのデプロイメントで使用されるフィーチャービューのバージョンもアップグレードする必要があります。

_The effects of this fallacy and how to overcome it: You can introduce subtle bugs if you do not couple model deployment versions with feature versions. 
_この誤謬の影響とそれを克服する方法：モデルデプロイメントのバージョンをフィーチャーバージョンと結びつけないと、微妙なバグを引き起こす可能性があります。
For example, if your new deployment uses the old feature version but the new feature group version is schema compatible with the previous version, the system will appear to work as before. 
例えば、新しいデプロイメントが古いフィーチャーバージョンを使用しているが、新しいフィーチャーグループバージョンが前のバージョンとスキーマ互換性がある場合、システムは以前と同様に機能しているように見えます。
However, its performance will suffer, and it will be a hard bug to find. 
しかし、そのパフォーマンスは低下し、バグを見つけるのが難しくなります。
The solution is to tightly couple the version of the model deployment with the feature view that feeds it. 
解決策は、モデルデプロイメントのバージョンをそれにフィードするフィーチャービューと密接に結びつけることです。

<!-- ここまで読んだ! -->

### 1.8. _8. There is no need for data versioning_ 
_8. データのバージョン管理は必要ない_

Reproducibility of training data requires data versioning. 
トレーニングデータの再現性にはデータのバージョン管理が必要です。

_The effects of this fallacy and how to overcome it: Without data versioning, if you re-create a training dataset and late data arrives since the creation of the first training dataset, the late data will be included in subsequent training dataset creation. 
_この誤謬の影響とそれを克服する方法：データのバージョン管理がないと、トレーニングデータセットを再作成し、最初のトレーニングデータセットの作成以降に遅れてデータが到着した場合、遅れて到着したデータがその後のトレーニングデータセットの作成に含まれることになります。
This is because there is no ingestion timestamp for late-arriving data. 
これは、遅れて到着したデータに対する取り込みタイムスタンプがないためです。
The solution is to support data versioning, as with lakehouse tables, and it includes ingestion timestamps for data points. 
解決策は、レイクハウステーブルのようにデータのバージョン管理をサポートし、データポイントに対する取り込みタイムスタンプを含めることです。
This enables you to re-create the training data exactly as it was at the point in time when it was originally created. 
これにより、元々作成された時点でのトレーニングデータを正確に再作成することができます。

<!-- ここまで読んだ! -->

### 1.9. _9. The model signature is the API for model deployments_ 
_9. モデルシグネチャはモデルデプロイメントのAPIである_

A real-time ML system uses a model deployment that makes predictions in response to prediction requests. 
リアルタイムMLシステムは、予測リクエストに応じて予測を行うモデルデプロイメントを使用します。
The parameters sent by the client to the model deployment API are typically not the same as the input parameters to the model (the model signature). 
クライアントがモデルデプロイメントAPIに送信するパラメータは、通常、モデルへの入力パラメータ（モデルシグネチャ）とは異なります。

_The effects of this fallacy and how to overcome it: Developers may mistake the model deployment API for the model signature. 
_この誤謬の影響とそれを克服する方法：開発者はモデルデプロイメントAPIをモデルシグネチャと誤解する可能性があります。
Without explicit support for a deployment API, developers will be forced to read source code to infer it. 
デプロイメントAPIの明示的なサポートがない場合、開発者はそれを推測するためにソースコードを読むことを余儀なくされます。
You need to explicitly define the API (or schema) for a deployment. 
デプロイメントのAPI（またはスキーマ）を明示的に定義する必要があります。
Without explicit support for a deployment API, developers will be forced to read source code to infer it. 
明示的なデプロイメントAPIのサポートがない場合、開発者はそれを推測するためにソースコードを読むことを余儀なくされます。
You need to explicitly define the API (or schema) for a deployment. 
デプロイメントのためのAPI（またはスキーマ）を明示的に定義する必要があります。

(これどういう話だっけ...!:thinking:)
<!-- ここまで読んだ! -->

### 1.10. _10. Online prediction latency is the time taken for the model prediction_ 
_10. オンライン予測レイテンシは、モデル予測にかかる時間です。_

When you serve a model behind a network endpoint, you typically have to perform a lot of operations before you finally call `model.predict()` with the final `feature vector(s)` as input. 
ネットワークエンドポイントの背後でモデルを提供する場合、最終的な`feature vector(s)`を入力として`model.predict()`を呼び出す前に、多くの操作を実行する必要があります。

_The effects of this fallacy and how to overcome it: You cannot assume that prediction latency for network-hosted models is only the time taken for the model prediction._ 
_この誤謬の影響とそれを克服する方法：ネットワークホストモデルの予測レイテンシは、モデル予測にかかる時間だけであると仮定してはいけません。_ 
You have to include the time for all preprocessing (building feature vectors, RAG, etc.) and postprocessing (feature/prediction logging). 
すべての前処理（特徴ベクトルの構築、RAGなど）と後処理（特徴/予測のログ記録）の時間を含める必要があります。

### 1.11. _11. LLMOps is different fr MLOps_ 
_11. LLMOpsはMLOpsとは異なります。_

LLMs need GPUs for inference and fine-tuning. 
LLMは推論とファインチューニングのためにGPUを必要とします。
Similarly, LLMs need support for scalable compute, scalable storage, and scalable model serving. 
同様に、LLMはスケーラブルなコンピュート、スケーラブルなストレージ、およびスケーラブルなモデル提供のサポートが必要です。
However, many MLOps platforms do not support either GPUs or scale, and the result is that LLMs are often seen as outside of MLOps and part of a new LLMOps discipline. 
しかし、多くのMLOpsプラットフォームはGPUやスケールをサポートしておらず、その結果、LLMはしばしばMLOpsの外部にあるものと見なされ、新しいLLMOpsの分野の一部と見なされます。
However, LLMs still follow the same FTI architecture. 
しかし、LLMは依然として同じFTIアーキテクチャに従います。
If your MLOps platform supports GPUs and scale, LLMOps is just MLOps with LLMs. 
**あなたのMLOpsプラットフォームがGPUとスケールをサポートしている場合、LLMOpsは単にLLMを持つMLOpsです。**
Feature pipelines are used to chunk, clean, and score text for instruction and alignment datasets. 
特徴パイプラインは、指示および整列データセットのためにテキストをチャンク化、クリーンアップ、およびスコアリングするために使用されます。
They are also used to compute vector embeddings stored in a vector index for RAG. 
それらはまた、RAGのためにベクトルインデックスに保存されたベクトル埋め込みを計算するためにも使用されます。
Training pipelines are used to fine-tune and align foundation LLMs. 
トレーニングパイプラインは、基盤となるLLMをファインチューニングおよび整列させるために使用されます。
Tokenization is a model-dependent transformation that needs to be consistent between training and inference—without platform support, users often slip up, using the wrong version of the tokenizer for their LLM in inference. 
**トークン化は、トレーニングと推論の間で一貫性が必要なモデル依存の変換**です。プラットフォームのサポートがない場合、ユーザーはしばしば間違ったバージョンのトークナイザーを推論で使用してしまいます。
Agents and workflows are found in online inference pipelines, as are calls to external systems with RAG and function calling. 
エージェントとワークフローはオンライン推論パイプラインに見られ、RAGや関数呼び出しを伴う外部システムへの呼び出しもあります。
Your MLOps team should be able to bring the same architecture and tooling to bear on LLM systems as it does with batch and real-time ML systems. 
**あなたのMLOpsチームは、バッチおよびリアルタイムのMLシステムと同様に、LLMシステムに同じアーキテクチャとツールを適用できるべき**。(これは意識すべき...!!:thinking:)

_The effects of this fallacy and how to overcome it: You may duplicate your AI infrastructure by supporting a separate LLMOps stack from your MLOps stack._ 
_この誤謬の影響とそれを克服する方法：MLOpsスタックとは別のLLMOpsスタックをサポートすることで、AIインフラストラクチャを重複させる可能性があります。_

If you treat LLMOps as MLOps at scale, developers should be able to easily transition from batch/real-time ML systems to an LLM AI system—if you follow the FTI architecture. 
LLMOpsをスケールでのMLOpsとして扱う場合、開発者はFTIアーキテクチャに従えば、バッチ/リアルタイムのMLシステムからLLM AIシステムに簡単に移行できるはずです。

### 1.12. _12. You require an ML orchestrator for ML pipelines_ 
_12. MLパイプラインにはMLオーケストレーターが必要です。_

You do not require an ML-specific orchestrator, such as Kubeflow/Metaflow/ZenML/SageMaker Pipelines, to run your ML pipelines. 
MLパイプラインを実行するために、Kubeflow/Metaflow/ZenML/SageMaker PipelinesのようなML特有のオーケストレーターは必要ありません。
ML orchestrators were designed for batch ML systems and are often limited to running only a few different data processing and ML frameworks. 
MLオーケストレーターはバッチMLシステムのために設計されており、通常は異なるデータ処理およびMLフレームワークをいくつかしか実行できません。
For example, you can’t run a Spark feature pipeline in Kubeflow. 
例えば、KubeflowではSparkの特徴パイプラインを実行できませ
Also, ML orchestrators do not run streaming feature pipelines. 
また、MLオーケストレーターはストリーミング特徴パイプラインを実行しません。
If you want to support batch, real-time, and even LLM AI systems in one platform, not all ML pipelines or services can be managed by your ML orchestrator. 
**バッチ、リアルタイム、さらにはLLM AIシステムを1つのプラットフォームでサポートしたい場合、すべてのMLパイプラインやサービスをMLオーケストレーターで管理できるわけではありません。** (うんうん。だよね...!:thiniking:)
The implication of this is that ML orchestrators are not aware of all lineage information for all AI systems. 
これは、MLオーケストレーターがすべてのAIシステムのすべての系譜情報を把握していないことを意味します。
In contrast, the data layers (feature store, model registry) are aware of all lineage information for all classes of ML pipeline and should typically be the source of truth for lineage. 
対照的に、データレイヤー（特徴ストア、モデルレジストリ）は、すべてのクラスのMLパイプラインの系譜情報を把握しており、通常は系譜の真実の源であるべきです。

That leaves you free to use the orchestrator that best suits the requirements of your FTI pipelines. 
これにより、FTIパイプラインの要件に最も適したオーケストレーターを自由に使用できます。

_The effects of this fallacy and how to overcome it: Since its inception, MLOps has been associated with ML orchestrators, such as Kubeflow._ 
_この誤謬の影響とそれを克服する方法：MLOpsはその発足以来、KubeflowのようなMLオーケストレーターと関連付けられてきました。_

But the recent Cambrian explosion in batch and stream-processing data engines means that you may want to use a specialist framework for feature pipelines, like Apache Flink, Feldera, or Polars. 
しかし、バッチおよびストリーム処理データエンジンの最近のカンブリア爆発により、Apache Flink、Feldera、またはPolarsのような特徴パイプラインのための専門的なフレームワークを使用したいかもしれませ
ML orchestrators can’t keep up. 
MLオーケストレーターは追いつけません。
They were also originally designd to store lineage information. 
彼らはもともと系譜情報を保存するために設計されていました。
If you run an ML pipeline outside your ML orchestrator, lineage information will be lost to it. 
MLオーケストレーターの外でMLパイプラインを実行すると、系譜情報は失われます。
Instead, lineage information should be managed by the feature store and model registry, not by the orchestrator. 
代わりに、系譜情報はオーケストレーターではなく、特徴ストアとモデルレジストリによって管理されるべきです。
You are free to use the best orchestrator for each of your ML pipelines. 
**各MLパイプラインに最適なオーケストレーターを自由に使用**できます。

<!-- ここまで読んだ! -->

## 2. The Ethical Responsibilities of AI Builders AIビルダーの倫理的責任

Finally, a word on your ethical responsibilities when you build an AI system. 
最後に、AIシステムを構築する際の倫理的責任について一言。
Before you dive into building an AI system, you should always consider any potential negative impacts of the system. 
AIシステムの構築に取り掛かる前に、システムの潜在的な悪影響を常に考慮すべきです。
It is not only your responsibility to comply with laws and regulations but also to ensure you do not cause direct or indirect harm. 
法律や規制に従うことはあなたの責任であるだけでなく、直接的または間接的な害を引き起こさないことを保証することもあなたの責任です。
For example, personalized recommender systems must be responsible AI systems. 
例えば、パーソナライズされたレコメンダーシステムは責任あるAIシステムでなければなりません。
An investigation by RTÉ Ireland Prime Time in May 2024 discovered that “by the end of an hour of scrolling, TikTok’s recommender system was showing a stream of videos almost exclusively related to depression, self-harm, and suicidal thoughts to the users it believed to be 13 years old.” 
2024年5月にRTÉ Ireland Prime Timeによる調査では、「1時間のスクロールの終わりまでに、TikTokのレコメンダーシステムは、13歳だと信じているユーザーに対して、ほぼ独占的に抑うつ、自傷行為、そして自殺の考えに関連する動画のストリームを表示していた」と発見されました。
If you work in a company that builds an AI system like that, fix the system or leave the company and whistleblow. 
そのようなAIシステムを構築する会社で働いている場合は、システムを修正するか、会社を辞めて内部告発してください。
It is not honorable to build software that is lawful but unethical. 
合法であるが倫理的でないソフトウェアを構築することは名誉あることではありません

<!-- ここまで読んだ! -->

We can learn from history, and the story of the Vasa ship in Sweden is both a warning and a lesson to engineers everywhere. 
私たちは歴史から学ぶことができ、スウェーデンのバサ船の物語は、エンジニアにとって警告であり教訓でもあります。

King Gustavus Adolphus wanted a warship with 64 heavy cannons (the most in the world in 1627). 
グスタフス・アドルフ王は、64門の重砲を備えた戦艦を望みました（1627年に世界で最も多い）
The experts told him it wasn’t possible. 
専門家たちはそれが不可能だと告げました。

Still, shipbuilders built it, knowing their work was both futile and dangerous. 
それでも、造船業者たちは、自分たちの仕事が無駄で危険であることを知りながら、それを建造しました。

The engineers were as spineless as the ship itself. 
エンジニアたちは船そのものと同じくらい臆病でした。

The Vasa sank on launch, with the loss of around 30 souls. 
バサは進水時に沈没し、約30人の命が失われました。

Don’t be the developer who builds the AI system that does harm. 
害を及ぼすAIシステムを構築する開発者にならないでください。

Together, we can make AI a force for good, but without help from the law, we will need an agreed-upon ethical code for that to happen. 
共に、私たちはAIを善の力にすることができますが、法律の助けがなければ、それを実現するためには合意された倫理コードが必要です。

Follow that ethical code and help enforce it, and you will thank yourself for it when you later reflect back on your life. 
その倫理コードに従い、それを施行する手助けをすれば、後に自分の人生を振り返ったときに自分を感謝することになるでしょう。

## 3. Summary要約

This chapter introduced a case study of building your own TikTok-like personalized recommendation service for videos. 
この章では、動画のための自分自身のTikTokのようなパーソナライズされたレコメンデーションサービスを構築するケーススタディを紹介しました。
It covered the retrieval-and-ranking architecture, which builds on the two-tower embedding model for retrieval and a ranking model for personalizing recommendations. 
それは、取得のための2タワー埋め込みモデルと、レコメンデーションをパーソナライズするためのランキングモデルに基づく取得とランキングのアーキテクチャをカバーしました。
We covered the streaming, batch, and vector embedding feature pipelines for our system; the training pipelines for the user- and video-embedding models and the ranking model; and the online inference pipeline to implement retrieval and ranking for user requests. 
私たちは、システムのためのストリーミング、バッチ、およびベクトル埋め込み特徴パイプライン、ユーザーおよび動画埋め込みモデルとランキングモデルのためのトレーニングパイプライン、ユーザーリクエストのための取得とランキングを実装するオンライン推論パイプラインをカバーしました。
We finished with a flourish, adding an agent to support free-text search across and within videos, powered by LLMs. 
私たちは、LLMによって駆動される動画全体および内部での自由形式検索をサポートするエージェントを追加して、華やかに締めくくりました。
Finally, we concluded the book with a dirty dozen of fallacies for MLOps and LLMOps that you should avoid if you want to be successful in building AI systems. 
最後に、AIシステムを構築する際に成功したいのであれば避けるべきMLOpsとLLMOpsの誤謬のダーティダズンで本書を締めくくりました。
And there is no more important time in history for building AI systems than today. 
そして、AIシステムを構築するための歴史の中で、今日ほど重要な時はありません。
Given the rate of improvements, today will always be the most important day for building AI systems. 
**改善の速度を考えると、今日がAIシステムを構築するための最も重要な日であり続ける**でしょう。
Go forth and create, and may the force be with you. 
前進して創造力があなたと共にあらんことを。

## 4. About the Author
**Jim Dowling is CEO of Hopsworks and a former associate professor at KTH Royal** Institute of Technology
###### 4.0.0.0.1. 著者について
**ジム・ダウリングはHopsworksのCEOであり、KTH王立工科大学の元准教授です。**



. He has led the development of Hopsworks, including the first open-source feature store for machine learning. 
彼はHopsworksの開発を主導し、機械学習のための最初のオープンソースフィーチャーストアを含んでいます。


He has a unique background in the intersection of data and AI. 
彼はデータとAIの交差点において独自のバックグラウンドを持っています。

For data, he worked at MySQL and later led the development of HopsFS, a distributed filesystem that won the IEEE Scale Prize in 2017. 
データに関しては、彼はMySQLで働き、その後2017年にIEEE Scale Prizeを受賞した分散ファイルシステムHopsFSの開発を主導しました。

For AI, his PhD introduced collaborative reinforcement learning, and he developed and taught the first course on deep learning in Sweden in 2016. 
AIに関しては、彼の博士号は協調強化学習を紹介し、2016年にスウェーデンで深層学習に関する最初のコースを開発し、教えました。

He also released a popular online course on serverless machine learning using Python at serverless-ml.org. 
彼はまた、serverless-ml.orgでPythonを使用したサーバーレス機械学習に関する人気のオンラインコースをリリースしました。

This combined background of data and AI helped him realize the vision of a feature store for machine learning based on general-purpose programming languages, rather than the earlier feature store work at Uber on DSLs. 
このデータとAIの組み合わせたバックグラウンドは、彼が一般目的プログラミング言語に基づく機械学習のためのフィーチャーストアのビジョンを実現するのに役立ちました。これは、以前のUberでのDSLに関するフィーチャーストアの作業とは異なります。

He was the first evangelist for feature stores, helping to create the feature store product category through talks at industry conferences (like Data/AI Summit, PyData, and OSDC) and educational articles on feature stores. 
彼はフィーチャーストアの最初のエバンジェリストであり、業界会議（Data/AI Summit、PyData、OSDCなど）での講演やフィーチャーストアに関する教育的な記事を通じてフィーチャーストア製品カテゴリの創出を助けました。
He is the organizer of the annual feature store summit conference and the featurestore.org community, as well as co-organizer of PyData Stockholm. 
彼は年次フィーチャーストアサミット会議とfeaturestore.orgコミュニティの主催者であり、PyData Stockholmの共同主催者でもあります。

<!-- ここまで読ん -->

## 5. Colophon コロフォン

The animal on the cover of Building Machine Learning Systems with a Feature Store is a red-breasted pygmy parrot (Micropsitta bruijnii), native to the Maluku Islands and Melanesia. 
『フィーチャーストアを用いた機械学習システムの構築』の表紙に描かれている動物は、マルク諸島とメラネシアに生息する赤胸のピグミーオウム（Micropsitta bruijnii）です。
This parrot is a member of the smallest genus of parrot, with an average length of eight centimeters (a little over three inches). 
このオウムは最も小さなオウムの属に属し、平均長は8センチメートル（約3インチ強）です。

Unlike many other pygmy parrots, it lives in high-altitude environments and nests in tree hollows or stumps. 
他の多くのピグミーオウムとは異なり、高地環境に生息し、木の空洞や切り株に巣を作ります。

It feeds on lichen and moves in short, jerky movements, often climbing along the bark of trees. 
地衣類を食べ、短くて不規則な動きで移動し、しばしば木の樹皮に沿って登ります。

As with many birds, the red-breasted pygmy parrot exhibits sexual dimorphism, where the male and female differ in appearance: both are green but the male has a red chest and pink-orange throat while the female is primarily green with a blue crown and white face. 
多くの鳥と同様に、赤胸のピグミーオウムは性二形性を示し、オスとメスで外見が異なります。どちらも緑色ですが、オスは赤い胸とピンクオレンジの喉を持ち、メスは主に緑色で青い冠と白い顔をしています。

Its lifespan is similar to that of other small parrots, up to ten years. 
その寿命は他の小型オウムと同様で、最大10年です。

Unlike some other parrots, this species does not do well in captivity. 
他のいくつかのオウムとは異なり、この種は飼育下ではうまくいきません。

Its IUCN status is of Least Concern. 
そのIUCNのステータスは「低危険」です。

Many of the animals on O’Reilly covers are endangered; all of them are important to the world. 
O'Reillyの表紙に描かれている動物の多くは絶滅危惧種であり、すべてが世界にとって重要です。

The cover illustration is by José Marzan Jr., based on an antique line engraving from _Lydekker’s Royal Natural History. 
表紙のイラストはJosé Marzan Jr.によるもので、_Lydekker’s Royal Natural History_の古い線画に基づいています。

The series design is by Edie Freedman, Ellie Volckhausen, and Karen Montgomery. 
シリーズデザインはEdie Freedman、Ellie Volckhausen、Karen Montgomeryによるものです。

The cover fonts are Gilroy Semibold and Guardian Sans. 
表紙のフォントはGilroy SemiboldとGuardian Sansです。

The text font is Adobe Minion Pro; the heading font is Adobe Myriad Condensed; and the code font is Dalton Maag’s Ubuntu Mono. 
本文フォントはAdobe Minion Pro、見出しフォントはAdobe Myriad Condensed、コードフォントはDalton MaagのUbuntu Monoです。
<!-- ここまで読んだ! -->
