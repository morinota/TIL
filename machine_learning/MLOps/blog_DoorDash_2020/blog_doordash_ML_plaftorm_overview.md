# DoorDashのMLプラットフォーム - 始まり
# DoorDash’s ML Platform – The Beginning

April 23, 2020  
2020年4月23日  

Param Reddy  
パラム・レディ  

DoorDash uses Machine Learning (ML) at various places like inputs to Dasher Assignment Optimization, balancing Supply & Demand, Fraud prediction, Search Ranking, Menu classification, Recommendations etc.  
DoorDashは、Dasher Assignment Optimizationへの入力、供給と需要のバランス、詐欺予測、検索ランキング、メニュー分類、推薦など、さまざまな場所で機械学習（ML）を使用しています。  
As the usage of ML models increased, there grew a need for a holistic ML Platform to increase the productivity of shipping ML-based solutions.  
MLモデルの使用が増えるにつれて、MLベースのソリューションを提供する生産性を向上させるための包括的なMLプラットフォームの必要性が高まりました。  
This kick-started an effort to build an ML Platform for DoorDash.  
これにより、DoorDashのためのMLプラットフォームを構築する取り組みが始まりました。  
The ML Platform consists of two critical pieces: first the infrastructure needed for ML to work at scale, and second a productive environment for engineers and data scientists to build their models.  
MLプラットフォームは、2つの重要な要素で構成されています。まず、MLがスケールで機能するために必要なインフラストラクチャ、次にエンジニアとデータサイエンティストがモデルを構築するための生産的な環境です。  
Scalability and productivity are the key driving factors in the decision making process for us.  
**スケーラビリティと生産性は、私たちの意思決定プロセスにおける重要な推進要因**です。  

### Scenarios and Requirements シナリオと要件

As we dug into ML usage at DoorDash, the following key scenarios for ML emerged:
**DoorDashにおけるMLの使用を掘り下げる中で、以下の主要なシナリオ達が浮かび上がりました**。

- Online models- This is the scenario where we make predictions live in production in the critical path of the user experience. 
   オンラインモデル - これは、ユーザエクスペリエンスの重要な経路で本番環境でリアルタイムに予測を行うシナリオです。(要するに**リアルタイム推論のシナリオ!**:thinking:)
   In this scenario the models and frameworks need to be performant and have a low memory footprint. 
   このシナリオでは、モデルとフレームワークは高性能であり、メモリフットプリントが小さい必要があります。
   We also need to understand both the modeling frameworks and services frameworks, most in-depth here. 
   また、ここではモデリングフレームワークとサービスフレームワークの両方を深く理解する必要があります。
   Consequently, this is where the restrictions about which ML frameworks to support and how complex models will be stringent. 
   したがって、どのMLフレームワークをサポートするか、またどのように複雑なモデルを扱うかに関する制約が厳しくなります。
   Examples of these at DoorDash include food preparation time predictions, quoted delivery time predictions, search ranking, etc.
   DoorDashにおけるこれらの例には、食品準備時間の予測、見積もり配達時間の予測、検索ランキングなどがあります。

- Offline models- These predictions are used in production, but predictions are not done in the request/response paths. 
   オフラインモデル - これらの予測は本番環境で使用されますが、リクエスト/レスポンスの経路では予測が行われません。(i.e. **バッチ推論のシナリオ**!:thinking:)
   In this scenario runtime performance is secondary. 
   このシナリオでは、ランタイムパフォーマンスは二次的なものです。
   Since these predictions are still used in production, we need the calculations to be persisted in the warehouse. 
   これらの予測は依然として本番環境で使用されるため、**計算結果をデータウェアハウスに保存**する必要があります。(DoorDashだとDWHなんだ...!)
   Examples of these at DoorDash are demand predictions, supply predictions, etc.
   DoorDashにおけるこれらの例には、需要予測、供給予測などがあります。

- Exploratory models- This is where people explore hypotheses, but the model or its output are not used in production. 
   探索モデル - これは、人々が仮説を探求する場所ですが、モデルやその出力は本番環境で使用されません。(i.e. **PoCやadhocな分析などのシナリオ**かな...!:thinking:)
   Use cases include exploring potential production models, analysis for some identifying business opportunities, etc. 
   ユースケースには、潜在的な生産モデルの探求や、ビジネス機会を特定するための分析などが含まれます。
   We are explicitly not placing any restrictions on frameworks here.
   **ここでは、フレームワークに対して明示的に制約を設けていません。**

These brought out the following requirements for the ML Platform:
これらはMLプラットフォームに対する以下の**要件**を引き出しました。

- Standardizing ML frameworks: Given the number of ML frameworks available, for example LightGBM, XGBoost, PyTorch, Tensorflow, it is hard to develop expertise within a company for many of them. 
   **MLフレームワークの標準化**: 利用可能なMLフレームワークの数を考えると、例えばLightGBM、XGBoost、PyTorch、Tensorflowなど、企業内で多くのフレームワークに対する専門知識を開発することは困難です。
   So there is a need to standardize on a minimal set of frameworks which covers the breadth of use-cases that are typically encountered at DoorDash.
   したがって、**DoorDashで一般的に遭遇するユースケースの幅をカバーする最小限のフレームワークに標準化**する必要があります。

- Model lifecycle: Support for end to end model life-cycle consisting of hypothesizing improvements, training the model, preserving the training scripts, offline evaluation, online shadow testing (making predictions online for the sole purpose of evaluation), A/B testing and finally shipping the model.
   モデルライフサイクル: 改善の仮説、モデルのトレーニング、トレーニングスクリプトの保存、オフライン評価、**オンラインシャドウテスト（評価のためだけにオンラインで予測を行うこと）、A/Bテスト**、そして最終的にモデルを出荷するというエンドツーエンドのモデルライフサイクルをサポートします。

- Features: There are two kinds of features we use. 
   特徴量: 私たちが使用する**特徴量には2種類**あります。
   One kind is request level features, which capture request-specific information, for example the number of items in an order, request time etc. 
   **1つ目はリクエストレベルの特徴量**で、リクエスト特有の情報をキャプチャします。例えば、注文のアイテム数、リクエスト時間などです。
   The second kind is environmental features which capture the environment under which DoorDash is operating. 
   2つ目は環境特徴量で、DoorDashが運営されている環境をキャプチャします。
   For example, average wait times in a store, number of orders in the last 30 mins in a store, numbers of orders from a customer in the last 3 months, etc. 
   例えば、店舗での平均待機時間、店舗での過去30分間の注文数、過去3ヶ月間の顧客からの注文数などです。
   Environmental features are common across all requests. 
   環境特徴量はすべてのリクエストに共通しています。
   We need a good way to compute and store environmental features.
   環境特徴量を計算し、保存するための良い方法が必要です。
   (こういう特徴量の分類の考え方もあるのか...!:thinking:)

<!-- ここまで読んだ! --> 

### Standardizing on Supported ML Frameworks サポートされるMLフレームワークの標準化

The first step towards an ML Platform was to standardize the ML frameworks which will be supported.  
MLプラットフォームへの第一歩は、サポートされるMLフレームワークを標準化することでした。
Supporting any framework requires a deep understanding of it, both in terms of the API it provides and its quality and performance tuning.  
**任意のフレームワークをサポートするには、その提供するAPIや品質、パフォーマンス調整に関して深い理解が必要**です。
As an organization we are better off knowing a few frameworks deeply than many in a shallow fashion.  
**組織としては、多くのフレームワークを浅く知るよりも、いくつかのフレームワークを深く知る方が良い**です。(ふむふむなるほど...!:thinking:)
This helps us run better services for ML as well as help leverage organizational knowhow.  
これにより、MLのためのより良いサービスを運営し、組織のノウハウを活用するのに役立ちます。
The goal was to arrive at the sweet spot where we make appropriate tradeoffs in selecting frameworks.  
目標は、フレームワークを選択する際に適切なトレードオフを行う理想的なポイントに到達することでした。
For example, if there is some pre-trained model in some framework which is not available in currently supported frameworks and building one is going to take considerable effort, it makes sense to support a different framework.  
**例えば、現在サポートされているフレームワークにはない事前学習済みモデルがあり、それを構築するのにかなりの労力がかかる場合、別のフレームワークをサポートすることは理にかなっています**。
After completing an internal survey on currently used model types and how they might evolve over time, we arrived at the conclusion that we need to support one tree based model framework and one neural network based modeling framework.  
**現在使用されているモデルタイプとそれが時間とともにどのように進化するかについての内部調査を完了した後、私たちは1つの木ベースのモデルフレームワークと1つのニューラルネットワークベースのモデリングフレームワークをサポートする必要があるという結論に達しました**。(ふむふむ...!:thinking:)
Also given the standardization of DoorDash's tech stack to Kotlin, we needed something that had a simple C/C++ API at the prediction time to hook up into the Kotlin-based prediction service using JNI.  
また、DoorDashの技術スタックがKotlinに標準化されたことを考慮し、予測時にKotlinベースの予測サービスにJNIを使用して接続するためのシンプルなC/C++ APIを持つものが必要でした。
For tree based models we evaluated XGBoost, LightGBM, and CatBoost, measuring the quality of the model (using PR AUC) and training/prediction times on production models we already have.  
木ベースのモデルについては、XGBoost、LightGBM、CatBoostを評価し、モデルの品質（PR AUCを使用）と、既存のプロダクションモデルにおけるトレーニング/予測時間を測定しました。
The accuracy of models were almost the same for use cases we had.  
私たちの使用ケースにおいて、モデルの精度はほぼ同じでした。
For training, we found that LightGBM was fastest.  
トレーニングに関しては、LightGBMが最も速いことがわかりました。
For predictions, XGBoost was slightly faster than LightGBM but not by a huge margin.  
予測に関しては、XGBoostがLightGBMよりもわずかに速かったですが、大きな差ではありませんでした。
Given the fact that the set of current models were already in LightGBM, we ended up selecting LightGBM as the framework for tree based models.  
現在のモデルセットがすでにLightGBMにあったことを考慮し、私たちは**木ベースのモデルのフレームワークとしてLightGBMを選択しました**。

For neural network models, we looked at TensorFlow and PyTorch.  
ニューラルネットワークモデルについては、TensorFlowとPyTorchを検討しました。
Here again, for our use cases we did not find a significant difference in quality of the models produced between these two.  
ここでも、私たちの使用ケースにおいて、これら二つの間で生成されたモデルの品質に大きな違いは見られませんでした。
PyTorch was slower to train on CPU's compared to Tensorflow, however on GPUs both had similar training speeds.  
PyTorchはCPUでのトレーニングがTensorFlowに比べて遅かったですが、GPUでは両者のトレーニング速度は似ていました。
For predictions, both of these had similar predictions per minute numbers.  
予測に関しては、両者ともに1分あたりの予測数は似ていました。
We then looked at the API set for Tensorflow and PyTorch for both training and prediction time and concluded that PyTorch gave a more coherent API set.  
次に、トレーニングと予測時間の両方に対するTensorFlowとPyTorchのAPIセットを調査し、PyTorchがより一貫したAPIセットを提供していると結論付けました。
With the launch of TorchScript C++ support in PyTorch, we had the right API set needed to build the prediction service using PyTorch.  
PyTorchでのTorchScript C++サポートの開始により、PyTorchを使用して予測サービスを構築するために必要な適切なAPIセットが得られました。

#### Pillars of the ML Platform MLプラットフォームの柱(i.e. コンポーネント)たち

After the ML framework decision, based on prediction scenarios and requirements, the following four pillars emerged:  
MLフレームワークの決定後、予測シナリオと要件に基づいて、次の**4つの柱**が浮かび上がりました：

1. **Modeling library**- A python library for training/evaluating models, creating model artifacts which can be loaded by the Prediction Service, and making offline predictions.  
   モデリングライブラリ - モデルのトレーニング/評価、予測サービスによって読み込まれるモデルアーティファクトの作成、およびオフライン予測を行うためのPythonライブラリ。

1. **Model Training Pipeline**- A build pipeline where models will be trained for production usage. Once a model training script is submitted into git repo, this pipeline takes care of training the model and uploading the artifacts to the Model Store. The analogy here is if the modeling library is the compiler that produces the model, then the model training pipeline is the build system.  
   モデルトレーニングパイプライン - モデルがプロダクション使用のためにトレーニングされるビルドパイプライン。モデルトレーニングスクリプトがgitリポジトリに提出されると、このパイプラインがモデルのトレーニングとアーティファクトのモデルストアへのアップロードを担当します。ここでのアナロジーは、モデリングライブラリがモデルを生成するコンパイラであるならば、モデルトレーニングパイプラインはビルドシステムです。

1. Features Service- To capture the environment state needed for making the predictions, we need feature computation, feature storage and feature serving. Feature computations are either historical or in real time.  
   フィーチャーサービス - 予測を行うために必要な環境状態をキャプチャするために、フィーチャー計算、フィーチャー保存、フィーチャー提供が必要です。フィーチャー計算は、履歴的またはリアルタイムのいずれかです。

1. Prediction Service- This service is responsible for loading models from the model store, evaluating the model upon getting a request, fetching features from the Feature Store, generating the prediction logs, supporting shadowing and A/B testing.  
   予測サービス - このサービスは、モデルストアからモデルを読み込み、リクエストを受け取った際にモデルを評価し、フィーチャーストアからフィーチャーを取得し、予**測ログを生成し、シャドウイングとA/Bテストをサポートする責任があります**。

<!-- ここまで読んだ! -->

### Architecture of the DoorDash ML Platform DoorDash MLプラットフォームのアーキテクチャ

Based on the above, the architecture for the online predictions flow (with brief description of components) looks like: 
上記に基づいて、オンライン予測フローのアーキテクチャ（コンポーネントの簡単な説明付き）は次のようになります。

![]()

#### Feature Store 

- Low latency store from which Prediction Service reads common features needed for evaluating the model. Supports numerical, categorical, and embedding features. 
- モデル評価に必要な共通の特徴をPrediction Serviceが読み取る**低遅延ストア**。数値、カテゴリ、埋め込み特徴をサポートします。

(要するにFTI Pipelinesアーキテクチャにおける特徴量ストア(オンラインストア)か...!!:thinking:)
(RedisとかDynamoDBに実装してるのかな...! オフラインストアはSnowflakeと書いてあったけど...!:thinking:)

#### Realtime Feature Aggregator 

- Listens to a stream of events and aggregates them into features in realtime and stores them in the Feature Store. These are for features such as historic store wait time in the past 30 mins, recent driving speeds, etc. 
- イベントのストリームを監視し、リアルタイムで特徴に集約してFeature Storeに保存します。これには、過去30分の店舗の待機時間、最近の運転速度などの特徴が含まれます。
(ストリミーミングの特徴量生成パイプラインか...!:thinking:)

#### Historical Aggregator

- This runs offline to compute features which are longer-term aggregations like 1W, 3M, etc. These calculations run offline. Results are stored in the Feature Warehouse and also uploaded to the Feature Store. 
- これはオフラインで実行され、1W、3Mなどの長期的な集約の特徴を計算します。これらの計算はオフラインで実行され、**結果はFeature Warehouseに保存され、Feature Storeにもアップロード**されます。(あ、オフラインの特徴量ストアを、feature warehouseと呼んでるっぽい...??:thinking:)

(要するにFTI Pipelinesアーキテクチャにおけるバッチの特徴量生成パイプラインか...!:thinking:)

#### Prediction Logs

- This stores the predictions made from the prediction service including the features used when the prediction was made and the id of the model used to make the prediction. This is useful for debugging as well as for training data for the next model refresh. 
- これは、**予測サービスから行われた予測を保存し、予測が行われたときに使用された特徴と、予測を行うために使用されたモデルのIDを含みます**。これはデバッグや次のモデルのリフレッシュのためのトレーニングデータに役立ちます。

#### Model Training Pipeline

- All the production models will be built with this pipeline. The training script must be in the repository. Only this training pipeline will have access to write models into the Model Store to generate a trace of changes going into the Model Store for security and audit. The training pipeline will eventually support auto-retraining of models periodically and auto-deploy/monitoring. This is equivalent to the CI/CD system for ML Models. 
- すべてのプロダクションモデルはこのパイプラインで構築されます。トレーニングスクリプトはリポジトリに存在する必要があります。このトレーニングパイプラインのみがモデルストアにモデルを書き込むアクセス権を持ち、セキュリティと監査のためにモデルストアに入る変更のトレースを生成します。トレーニングパイプラインは最終的にモデルの自動再トレーニングと自動デプロイ/監視をサポートします。これはMLモデルのCI/CDシステムに相当します。

(要するにFTI Pipelinesアーキテクチャにおける学習パイプラインか...!:thinking:)

#### Model Store

- Stores the model files and metadata. Metadata identifies which model is currently active for certain predictions, defines which models are getting shadow traffic. 
- モデルファイルとメタデータを保存します。メタデータは、特定の予測に対して現在アクティブなモデルを特定し、どのモデルがシャドウトラフィックを受けているかを定義します。

(要するにFTI Pipelinesアーキテクチャにおけるモデルレジストリ...!:thinking:)

#### Prediction Service

- Serves predictions in production for various use cases. Given a request with request features, context (store id, consumer id, etc) and prediction name (optionally including override model id to support A/B testing), generates the prediction. 
- 様々なユースケースに対してプロダクションで予測を提供します。リクエスト特徴、コンテキスト（店舗ID、消費者IDなど）、および予測名（A/BテストをサポートするためにオーバーライドモデルIDを含むことも可能）を含むリクエストが与えられると、予測を生成します。

(要するにFTI Pipelinesアーキテクチャにおける推論パイプライン...!:thinking:)
--- 

We are just starting to execute on this plan, there is still a lot of work to do in building, scaling and operating this. 
私たちはこの計画を実行し始めたばかりで、構築、スケーリング、運用に関してまだ多くの作業があります。
If you are passionate about building the ML Platform which powers DoorDash, do not hesitate to reach us. 
DoorDashを支えるMLプラットフォームの構築に情熱を持っている方は、ぜひご連絡ください。

<!-- ここまで読んだ! -->
