## CHAPTER 2: Machine Learning Pipelines 第2章: 機械学習パイプライン

In one of my favorite episodes of _The Simpsons, when Homer Simpson heard that_ bacon, ham, and pork chops all came from the same animal, he couldn’t believe it: “Yeah, right, Lisa, a wonderful, magical animal.” 
私のお気に入りの『ザ・シンプソンズ』のエピソードの一つで、ホーマー・シンプソンがベーコン、ハム、ポークチョップがすべて同じ動物から来ていると聞いたとき、彼は信じられなかった。「そうだね、リサ、素晴らしくて魔法のような動物だ」と彼は言った。
I had the same reaction when I asked ChatGPT 4.1 for a definition of an ML pipeline. 
私も同じ反応を示しました。ChatGPT 4.1にMLパイプラインの定義を尋ねたときです。
It told me that an ML pipeline performs data collection, feature engineering, model training, model evaluation, model deployment, model monitoring, inference, and maintenance. 
それは、MLパイプラインがデータ収集、特徴量エンジニアリング、モデルのトレーニング、モデルの評価、モデルのデプロイ、モデルの監視、推論、メンテナンスを行うと教えてくれました。
“Yeah, right, GPT, a wonderful, magical monolithic ML pipeline,” I thought. 
「そうだね、GPT、素晴らしくて魔法のような単一のMLパイプラインだ」と私は思いました。
It even claimed its ML pipeline was modular! 
それは、MLパイプラインがモジュラーであるとさえ主張しました！

<!-- ここまで読んだ! -->

It’s no wonder that when I ask 10 different data scientists for a definition of an ML pipeline, I typically get 10 different answers. 
**10人の異なるデータサイエンティストにMLパイプラインの定義を尋ねると、通常10通りの異なる答えが返ってくる**のも不思議ではありません。
There is no agreement on what its inputs and outputs are. 
その入力と出力が何であるかについての合意はありません。
If a developer tells you they built their AI system using an ML pipeline, what information can you glean from that? 
もし開発者がMLパイプラインを使用してAIシステムを構築したと言った場合、そこからどのような情報を得ることができるでしょうか？
In my opinion, the term ML pipeline, as it is currently used, could be “considered harmful” when communicating about building AI systems.[1] 
**私の意見では、現在の使われ方では、MLパイプラインという用語はAIシステムの構築についてコミュニケーションを取る際に「有害と見なされる」可能性があります。**
In this book, we strive to be more rigorous. 
この本では、私たちはより厳密であることを目指しています。
We describe AI systems in terms of concrete pipelines used to build them. 
私たちは、**AIシステムを構築するために使用される具体的なパイプラインの観点**から説明します。
We reserve the use of the term ML pipeline to describe any individual pipeline or group of pipelines in an AI system. 
私たちは、AIシステム内の個々のパイプラインまたはパイプラインのグループを説明するためにMLパイプラインという用語の使用を留保します。

<!-- ここまで読んだ! -->

A pipeline is a computer program that has clearly defined inputs and outputs (that is, it has a well-defined interface) and runs either on a schedule or continuously. 
**パイプラインとは、明確に定義された入力と出力（つまり、明確に定義されたインターフェースを持つ）を持ち、スケジュールに従ってまたは継続的に実行されるコンピュータプログラム**です。
An ML _pipeline is any pipeline that outputs ML artifacts used in an AI system. 
MLパイプラインとは、AIシステムで使用されるMLアーティファクトを出力する任意のパイプラインです。
We name a_ concrete ML pipeline after the ML artifact(s) it creates or modifies. 
私たちは、具体的なMLパイプラインを、**それが作成または変更するMLアーティファクトにちなんで**名付けます。
ML pipelines that create ML artifacts include a feature pipeline that outputs features, a vector embedding pipeline that outputs embeddings, a training pipeline that outputs a trained model, and an inference pipeline that outputs predictions. 
MLアーティファクトを作成するMLパイプラインには、特徴を出力する特徴パイプライン、埋め込みを出力するベクトル埋め込みパイプライン、トレーニングされたモデルを出力するトレーニングパイプライン、予測を出力する推論パイプラインが含まれます。
(あ、FTI以外にも vector embedding pipelineという用語も出てきた...!!:thinking:)
ML pipelines that modify ML artifacts include a model validation pipeline that transitions a model from unvalidated to validated and a model deployment pipeline that deploys a model to production. 
MLアーティファクトを変更するMLパイプラインには、モデルを未検証から検証済みに移行する**モデル検証パイプライン(model validation pipeline)**と、モデルを本番環境にデプロイする**モデルデプロイメントパイプライン(model deployment pipeline)**が含まれます。
In this chapter, we cover many of the different possible ML pipelines, but we will double-click on the most important ML pipelines for building an AI system— feature pipelines, training pipelines, and inference pipelines. 
この章では、さまざまな可能なMLパイプラインについて説明しますが、AIシステムを構築するための最も重要なMLパイプライン—特徴パイプライン、トレーニングパイプライン、推論パイプライン—に焦点を当てます。
Three pipelines and the truth. 
三つのパイプラインと真実。

<!-- ここまで読んだ! -->
　
### Building ML Systems with ML Pipelines　MLパイプラインを使用したMLシステムの構築

Before we look at how to develop ML pipelines, we will look at a development process for building AI systems. 
MLパイプラインを開発する方法を見る前に、AIシステムを構築するための開発プロセスを見ていきます。
AI systems are software systems, and software engineering methodologies help guide you when building software systems. 
AIシステムはソフトウェアシステムであり、ソフトウェア工学の手法はソフトウェアシステムを構築する際の指針となります。
The first generation of software development processes for ML, such as Microsoft’s [Team Data Science](https://oreil.ly/HO-FD) [Process, concentrated primarily on data collection and modeling but did not address](https://oreil.ly/HO-FD) how to build AI systems. 
MLのためのソフトウェア開発プロセスの第一世代は、Microsoftの[Team Data Science](https://oreil.ly/HO-FD) [Processのように、主にデータ収集とモデリングに集中していましたが、AIシステムの構築方法には触れていませんでした。](https://oreil.ly/HO-FD)
As such, those processes were quickly superseded by MLOps, which focuses on automation, versioning, and collaboration between developers and operations to build AI systems. 
そのため、これらのプロセスはすぐにMLOpsに取って代わられました。MLOpsは、AIシステムを構築するための自動化、バージョン管理、開発者と運用の協力に焦点を当てています。

<!-- ここまで読んだ! -->

#### Minimal Viable Prediction Service 最小限の実行可能な予測サービス

We introduce here a minimal MLOps development methodology based on getting as quickly as possible to a minimal viable AI system, or minimal viable prediction service (MVPS). 
ここでは、**最小限の実行可能なAIシステム、または最小限の実行可能な予測サービス（MVPS）にできるだけ早く到達すること**に基づいた最小限のMLOps開発手法を紹介します。
I followed this MVPS process in my course on building AI systems at KTH, and it has enabled students to get to a working AI system (that uses a novel data source to solve a novel prediction problem) within a few days, at most.
私はKTHでのAIシステム構築に関するコースでこのMVPSプロセスを実践し、**学生たちは数日以内に（新しいデータソースを使用して新しい予測問題を解決する）動作するAIシステムに到達することができました。**

<!-- ここまで読んだ! -->

---
(コラム的なやつ!)

ML artifacts include models, features, training data, vector indexes, model deployments, and prediction/context logs. 
**MLアーティファクトには、モデル、特徴、トレーニングデータ、ベクトルインデックス、モデルデプロイメント、予測/コンテキストログが含まれます。**
ML artifacts are stateful objects that are produced by ML pipelines and are managed by your ML infrastructure services. 
MLアーティファクトは、MLパイプラインによって生成され、MLインフラストラクチャサービスによって管理される状態を持つオブジェクトです。
Most ML artifacts are immutable, with the exception of feature data, vector indexes, and model deployments that can be updated in place. 
**ほとんどのMLアーティファクトは不変ですが、特徴データ、ベクトルインデックス、およびその場で更新可能なモデルデプロイメントは例外です。**

---

<!-- ここまで読んだ! -->

The MVPS development process, shown in Figure 2-1, starts with identifying: 
図2-1に示すMVPS開発プロセスは、以下の特定から始まります：

- The prediction problem you want to solve 
  - 解決したい予測問題
- The KPI metrics you want to improve 
  - 改善したいKPIメトリクス
- The data sources you have available for use 
  - 使用可能なデータソース

Once you have identified these three pillars that make up your AI system, you will need to map your prediction problem to an ML proxy metric—a target you will optimize in your AI system. 
**AIシステムを構成するこれらの三つの柱**を特定したら、**予測問題をML proxy metric、つまりAIシステムで最適化するターゲットにマッピング**する必要があります。
This is often the most challenging step. 
これは**しばしば最も難しいステップ**です。(DSの腕が問われる部分...!!:thinking:)
The ML proxy metric should also positively correlate with the KPI(s). 
**ML proxy metricはKPIと正の相関を持つべき**です。

![]()
_Figure 2-1. The MVPS process for developing ML systems starts in the leftmost circle by_ _identifying a prediction problem, how to measure its success using KPIs, and how to map_ _it onto an ML proxy metric. Based on the identified prediction problem and data sour‐_ _ces, you implement the FTI pipeline, as well as either a user interface or integration with_ _an external system that consumes the prediction. The arcs connecting the circles repre‐_ _sent the iterative nature of the development process, where you often revise your pipe‐_ _lines based on user feedback and changes to requirements._ 
_Figure 2-1. MLシステムを開発するためのMVPSプロセスは、最も左の円から始まり、予測問題を特定し、KPIを使用してその成功を測定する方法、そしてそれをMLプロキシメトリックにマッピングする方法を示します。特定された予測問題とデータソースに基づいて、FTIパイプラインを実装し、予測を消費するユーザーインターフェースまたは外部システムとの統合を行います。円をつなぐ弧は、開発プロセスの反復的な性質を表しており、ユーザーのフィードバックや要件の変更に基づいてパイプラインを修正することがよくあります。_

<!-- ここまで読んだ! -->

Next comes the implementation phase, where you typically work from left to right, but at any time you can circle back if you need to redefine your prediction problem, KPIs, or data sources. 
次に実装フェーズがあり、通常は左から右に作業しますが、予測問題、KPI、またはデータソースを再定義する必要がある場合は、いつでも戻ることができます。
The implementation steps are: 
実装手順は以下の通りです：

1. Develop a minimal feature pipeline that can both backfill historical data and write incremental production data to your feature store. 
   1. 過去のデータをバックフィルし、増分のproductionデータを特徴量ストアに書き込むことができる**最小限の特徴量パイプラインを開発**します。

2. Develop a minimal training pipeline if you need a custom model (skip this step if you are using a pretrained model, such as an LLM). 
   1. カスタムモデルが必要な場合は、最小限のトレーニングパイプラインを開発します（事前トレーニングされたモデル、例えばLLMを使用している場合はこのステップをスキップします）。

3. Develop an inference pipeline to make predictions with your model. This could be a batch program, an online inference program, an LLM application, or an agent. 
   1. モデルを使用して予測を行うための推論パイプラインを開発します。これはバッチプログラム、オンライン推論プログラム、LLMアプリケーション、またはエージェントである可能性があります。

4. Develop a UI or dashboard so stakeholders can try out your MVPS and you can iteratively improve it. 
   1. **ステークホルダーがMVPSを試すことができ、あなたがそれを反復的に改善できるようにUIまたはダッシュボードを開発**します。

<!-- ここまで読んだ! -->

Let’s start at the beginning with an example ecommerce store where you want to predict items or content that a user is interested in. 
ユーザーが興味を持つアイテムやコンテンツを予測したいeコマースストアの例から始めましょう。
For recommending items in an ecommerce store, the KPI could be increased conversion as measured by users placing items in their shopping cart. 
eコマースストアでアイテムを推薦する場合、**KPIはユーザーがアイテムをショッピングカートに入れることによって測定されるコンバージョンの増加**である可能性があります。
For content, a measurable business KPI could be maximized user engagement, as measured by the time a user spends on the service. 
コンテンツの場合、測定可能なビジネスKPIは、ユーザーがサービスに費やす時間によって測定されるユーザーエンゲージメントの最大化である可能性があります。
Your goal as a data scientist or ML engineer is to take the prediction problem and business KPIs and translate them into an AI system that optimizes some ML metric (or _target). 
データサイエンティストまたはMLエンジニアとしてのあなたの目標は、**予測問題とビジネスKPIを設定し、それらをいくつかのML metric (もしくはtarget)を最適化するAIシステムに変換すること**です。
The ML metric might be a direct match to a business KPI, such as the_ probability that a user places an item in a shopping cart, or the ML metric might be a proxy metric for the business KPI, such as the expected time a user will engage with a recommended piece of content (which is a proxy for increasing user engagement on the platform).
**MLメトリックは、ユーザーがアイテムをショッピングカートに入れる確率のようにビジネスKPIと直接一致する場合もあれば、ユーザが推薦されたコンテンツにどれだけの時間関与するかの期待値のようにビジネスKPIのプロキシメトリックである場合もあります**（これはプラットフォーム上のユーザーエンゲージメントの増加のプロキシです）。

<!-- ここまで読んだ! -->

Once you have your prediction problem, KPIs, and ML target, you need to think about how to create training data with features that have predictive power for your target, based on your available data. 
予測問題、KPI、およびMLターゲットが決まったら、**利用可能なデータに基づいて、ターゲットに対して予測力を持つ特徴を持つトレーニングデータを作成する方法を考える必要があります。**
You should start by enumerating and obtaining access to the data sources that feed your AI system. 
まず、AIシステムにデータを供給するデータソースを列挙し、アクセスを取得することから始めるべきです。
You then need to understand the data, so that you can effectively create features from that data.
**次に、そのデータを理解する必要があります。そうすれば、そのデータから効果的に特徴量を作成できます。**
Exploratory data analysis (EDA) is a first step you’ll often take to gain an understanding of your data, its quality, and whether there is a dependency between any features and the target variable. 
**探索的データ分析（EDA）は、データ、その品質、および特徴量とターゲット変数の間に依存関係があるかどうかを理解するためにしばしば行う最初のステップ**です。
EDA typically helps develop domain knowledge of the data, if you are not yet familiar with the domain. 
**EDAは通常、データのドメイン知識を発展させるのに役立ちます。もしまだそのドメインに不慣れであれば。**
It can help you identify which variables could or should be used or created for a model and their predictive power for the model. 
それは、モデルに使用または作成されるべき変数を特定し、それらのモデルに対する予測力を明らかにするのに役立ちます。
You can start EDA by examining your data and its distributions using an LLM-powered assistant, such as Hopsworks Brewer, or ingesting your data into a feature store that computes data statistics on ingestion. 
EDAは、Hopsworks BrewerのようなLLM駆動のアシスタントを使用してデータとその分布を調べるか、データを取り込む際にデータ統計を計算する特徴ストアにデータを取り込むことで開始できます。
If needed, you can perform more detailed EDA in notebooks by analyzing the data visually and using statistics. 
必要に応じて、ノートブックでデータを視覚的に分析し、統計を使用してより詳細なEDAを実施できます。

<!-- ここまで読んだ! -->

The next (unavoidable) step is to identify the different technologies you will use to build the FTI pipelines (see Figure 2-2). 
次の（避けられない）ステップは、FTIパイプラインを構築するために使用するさまざまな技術を特定することです（図2-2を参照）。
We recommend using a kanban board for this. 
これには**カンバンボード**の使用をお勧めします。
A _kanban board is a visual tool that will track work as it moves through the_ MVPS process, featuring columns for different stages and cards for individual tasks. 
カンバンボードは、MVPSプロセスを通じて作業を追跡する視覚的なツールであり、異なるステージのための列と個々のタスクのためのカードを特徴としています。
Atlassian Jira and GitHub Projects are examples of kanban boards widely used by developers. 
Atlassian JiraやGitHub Projectsは、開発者によく使用されるカンバンボードの例です。

![]()
_Figure 2-2. The kanban board for our MVPS identifies the potential data sources, tech‐_ _nologies used for ML pipelines, and types of consumers of predictions produced by AI_ _systems. Here, we show some of the possible data sources, frameworks, and orchestrators_ _used in ML pipelines and AI apps that consume predictions._ 
_Figure 2-2. 私たちのMVPSのカンバンボードは、潜在的なデータソース、MLパイプラインに使用される技術、およびAIシステムによって生成される予測の消費者の種類を特定します。ここでは、MLパイプラインおよび予測を消費するAIアプリで使用される可能性のあるデータソース、フレームワーク、およびオーケストレーターのいくつかを示します。_

<!-- ここまで読んだ! -->

It is a good activity to fill in the MVPS kanban board before you start to implement your AI system, to get an overview of the AI system you’re building. 
AIシステムを実装する前にMVPSカンバンボードを埋めることは、構築しているAIシステムの概要を把握するための良い活動です。
You should make the title of the kanban board the name of the prediction problem your AI system solves, and then you should fill in the data sources, the AI applications that will consume the predictions, and the technologies you intend to use to implement the FTI pipelines. 
カンバンボードのタイトルをAIシステムが解決する予測問題の名前にし、次にデータソース、予測を消費するAIアプリケーション、およびFTIパイプラインを実装するために使用する予定の技術を記入するべきです。
You can also annotate the different kanban lanes with nonfunctional requirements, such as the volume, velocity, and freshness requirements for the feature pipelines or the service-level objective (SLO) for the response times for an online inference pipeline. 
**異なるカンバンレーンに、特徴パイプラインのボリューム、速度、新鮮さの要件や、オンライン推論パイプラインの応答時間に関するサービスレベル目標（SLO）などの非機能要件を注釈することもできます。**
After you have produced a draft of your system architecture, you can move on to writing code. 
**システムアーキテクチャのドラフトを作成した後、コードの記述に進むことができます。**
You may later change the technologies chosen and the nonfunctional requirements, but it’s good practice to have a vision for where you want to go. 
後で選択した技術や非機能要件を変更することもありますが、**どこに行きたいのかのビジョンを持つことは良い習慣**です。

<!-- ここまで読んだ! -->

At this point, you have an understanding of your data and the features you need, so now you have to extract both the target observations (or labels) and features from your data sources. 
この時点で、データと必要な特徴を理解しているので、データソースからターゲット観測（またはラベル）と特徴の両方を抽出する必要があります。
This involves building feature pipelines from your data sources.
これは、データソースから特徴パイプラインを構築することを含みます。
The output of your feature pipelines will be the features and observations/labels that are stored in a feature store. 
**特徴パイプラインの出力は、フィーチャーストアに保存される特徴と観測値/ラベル**になります。
(ラベルも特徴量ストアに保存すべきなのかな〜...!! 少なくともラベルはオンラインストアに保存する必要はないよね...!!:thinking:)
If you have an existing feature store and you are fortunate enough that it already contains the target(s) and/or features you need, you can skip implementing the feature pipelines.
既存のフィーチャーストアがあり、必要なターゲットや特徴がすでに含まれている場合は、特徴パイプラインの実装をスキップできます。

From the feature store, you can create your training data and then implement a training pipeline to train your model that you save to a model registry.
フィーチャーストアからトレーニングデータを作成し、モデルレジストリに保存するモデルをトレーニングするためのトレーニングパイプラインを実装できます。
Finally, you implement an inference pipeline that uses your model and new feature data to make predictions, and you add a UI or dashboard to create your MVPS. 
最後に、モデルと新しいフィーチャーデータを使用して予測を行う推論パイプラインを実装し、MVPSを作成するためのUIまたはダッシュボードを追加します。
This MVPS development process is iterative, as you incrementally improve the FTI pipelines. 
**このMVPS開発プロセスは反復的であり、FTIパイプラインを段階的に改善します。**
You add testing, validation, and automation. 
テスト、検証、自動化を追加します。
You can later add different environments for development, staging, and production.
**後で開発、ステージング、プロダクション用の異なる環境を追加できます。**

<!-- ここまで読んだ! -->

#### Writing Modular Code for ML Pipelines MLパイプラインのためのモジュラーコードの記述

A successful AI system will need to be updated and maintained over time. 
成功したAIシステムは、時間の経過とともに更新および維持される必要があります。
That means you will need to make any changes to your source code, such as:
つまり、ソースコードに次のような変更を加える必要があります：

- The set of features computed or the data they are computed from
  - 計算された特徴量のセットまたはそれらが計算されるデータ
- How you train the model (its model architecture or hyperparameters) to improve its performance or reduce any bias
  - パフォーマンスを改善したり、バイアスを減らしたりするために、モデルのトレーニング方法（モデルアーキテクチャまたはハイパーパラメータ）
- For batch ML systems, making predictions more (or less) frequently or changing the sink where you save your predictions
  - バッチMLシステムの場合、予測をより頻繁（または少なく）行うか、予測を保存する先を変更する
- For online ML systems, changes in the request latency or feature freshness requirements
  - オンラインMLシステムの場合、リクエストのレイテンシやフィーチャーの新鮮さの要件の変更
- For LLM applications and agents, changes in context engineering, tools, or LLM versions
  - LLMアプリケーションやエージェントの場合、コンテキストエンジニアリング、ツール、またはLLMバージョンの変更

<!-- ここまで読んだ! -->

At the system architecture level, we can modularize the AI system into our three (or more) pipelines—the feature pipeline, training pipeline, and inference pipeline. 
**システムアーキテクチャのレベルでは、AIシステムを3つ（またはそれ以上）のパイプライン、すなわちフィーチャーパイプライン、トレーニングパイプライン、推論パイプラインにモジュール化できます。**
This level of modularity enables you to develop each pipeline independently—so long as you don’t break the data contract for each pipeline. 
このモジュール性のレベルにより、各パイプラインを独立して開発できるようになります—**各パイプラインのデータ契約を破らない限り。**
The data contract for each pipeline includes its input/output schema and any nonfunctional requirements, such as data validation rules for feature pipelines, model performance or bias for a training pipeline, or the SLO for an online inference pipeline. 
各パイプラインのデータ契約には、その入力/出力スキーマや、フィーチャーパイプラインのデータ検証ルール、トレーニングパイプラインのモデル性能やバイアス、オンライン推論パイプラインのSLOなどの非機能要件が含まれます。

However, inside each ML pipeline, you also need to write modular code that follows best practices in software engineering. 
しかし、各MLパイプライン内では、ソフトウェア工学のベストプラクティスに従ったモジュラーコードを書く必要があります。
Your source code should be tested and easy to maintain, and it should be DRY (“Do not repeat yourself”). 
ソースコードはテストされ、メンテナンスが容易であるべきであり、DRY（「繰り返さない」）であるべきです。
If the source code for your ML pipelines is a bunch of spaghetti notebooks, it will be hard to build reliable ML pipelines. 
**MLパイプラインのソースコードがスパゲッティノートブックの集まりである場合、信頼性の高いMLパイプラインを構築するのは難しくなります。**
How will you test the code in your notebooks to make sure any changes you make work correctly before you deploy them to production? 
ノートブック内のコードをどのようにテストして、変更が本番環境にデプロイする前に正しく機能することを確認しますか？
How will you onboard new developers to work on the codebase? 
新しい開発者をどのようにコードベースに参加させますか？

<!-- ここまで読んだ! -->

The approach that we recommend you take when writing ML pipelines in Python is to refactor your source code into functions or classes. 
私たちがPythonでMLパイプラインを書く際に推奨するアプローチは、ソースコードを関数またはクラスにリファクタリングすることです。
You decompose the steps in your ML pipeline into a set of functions that, when composed together, implement the ML pipeline program. 
**MLパイプラインのステップを一連の関数に分解し、それらを組み合わせることでMLパイプラインプログラムを実装**します。
Each function should encapsulate a manageable piece of related work, and functions can be reused in different parts of your codebase. 
各関数は関連する作業の管理可能な部分をカプセル化し、関数はコードベースの異なる部分で再利用できます。
You hide the implementation of the function (with all of its complexity) behind an interface. 
関数の実装（そのすべての複雑さ）をインターフェースの背後に隠します。
In Python, the interface to a function is the function’s signature—its name, parameters, and return type(s). 
Pythonでは、関数へのインターフェースは関数のシグネチャ—その名前、パラメータ、および戻り値の型です。

<!-- ここまで読んだ! -->

---
(コラム的なやつ)
Notebooks as ML Pipelines? MLパイプラインとしてのノートブック？

It is best practice to store feature functions in Python modules (not in notebooks), so they can be independently unit-tested and reused in different ML pipelines. 
フィーチャー関数はPythonモジュールに保存するのがベストプラクティスです（ノートブックではなく）、これにより独立してユニットテストが可能で、異なるMLパイプラインで再利用できます。
However, the ML pipeline program can still be a notebook that imports and uses the feature functions. 
ただし、MLパイプラインプログラムは、フィーチャー関数をインポートして使用するノートブックであることもできます。
If you want to run an ML pipeline as a notebook, you will need to use a platform that supports scheduling notebooks as jobs (such as Jupyter Notebooks on Hopsworks). 
MLパイプラインをノートブックとして実行したい場合は、ノートブックをジョブとしてスケジュールすることをサポートするプラットフォーム（HopsworksのJupyter Notebooksなど）を使用する必要があります。
We don’t recommend using Google Colaboratory (Colab) notebooks, as they do not work well with Git. 
Google Colaboratory（Colab）ノートブックの使用は推奨しません。なぜなら、Gitとの相性が良くないからです。
Without Git support, it is hard to import Python modules from files in your GitHub repository into your Colab notebook. 
Gitのサポートがないと、GitHubリポジトリ内のファイルからPythonモジュールをColabノートブックにインポートするのが難しくなります。

---

We start by looking at some example feature engineering code that we want to refactor to make it easier to test and more maintainable. 
テストしやすく、メンテナンスしやすくするためにリファクタリングしたいフィーチャーエンジニアリングコードの例を見ていきます。
In the following feature pipeline code, there is a compute_features function that performs data transformations on a Pandas DataFrame. 
以下のフィーチャーパイプラインコードには、Pandas DataFrame上でデータ変換を行うcompute_features関数があります。
It is an example of nonmodular feature engineering in Pandas: 
これは、Pandasにおける**非モジュラーなフィーチャーエンジニアリングの例**です：

```python
import pandas as pd

def compute_features(df: pd.DataFrame) -> pd.DataFrame:   
    if config["region"] == "UK":   
        df["holidays"] = is_uk_holiday (df["year"], df["week"])   
    else:   
        df["holidays"] = is_holiday (df["year"], df ["week"])   
    df["avg_3wk_spend"] = df["spend"].rolling (3).mean()   
    df["acquisition_cost"] = df["spend"]/df["signups"]   
    df["spend_shift_3weeks"] = df["spend"].shift(3)   
    df["special_feature1"] = compute_bespoke_feature(df)   
    return df   

df = pd.read_parquet("my_table.parquet")   
df = compute_features(df)
```

This code is not modular, as one function computes five features (holidays, avg_3wk_spend, acquisition_cost, spend_shift_3weeks, and special_feature1). 
**このコードはモジュラーではなく、1つの関数が5つの特徴（holidays、avg_3wk_spend、acquisition_cost、spend_shift_3weeks、special_feature1）を計算**しています。
It is difficult to write independent tests for each of the individual features, there is no dedicated documentation for each feature, and debugging requires understanding the whole compute_features function.
各個別の特徴に対して独立したテストを書くのが難しく、各特徴に専用のドキュメントがなく、デバッグにはcompute_features関数全体を理解する必要があります。

<!-- ここまで読んだ! -->

A solution to these problems is to refactor this code as feature functions that update a DataFrame containing the features. 
これらの問題に対する解決策は、**特徴を含むDataFrameを更新する特徴関数としてこのコードをリファクタリングすること**です。
This idea comes originally from Apache Hamilton. 
**このアイデアは元々Apache Hamiltonから**来ています。
For each feature computed, you define a new feature function. 
計算された各特徴に対して、新しい特徴関数を定義します。
You can create the features as columns in a DataFrame (Pandas, PySpark, or Polars) by applying the feature functions in the correct order. 
特徴関数を正しい順序で適用することによって、DataFrame（Pandas、PySpark、またはPolars）の列として特徴を作成できます。
For example, here, we compute the column `acquisition_cost` as the spend divided by the number of users who sign up for our service (signups): 
例えば、ここでは、列`acquisition_cost`を支出を私たちのサービス（サインアップ）にサインアップするユーザーの数で割ったものとして計算します：

```python
df['acquisition_cost'] = df['spend'] / df['signups']
```

We refactor the logic used to compute the `acquisition_cost` into a function as follows: 
`acquisition_cost`を計算するために使用されるロジックを次のように関数にリファクタリングします：

```python
def acquisition_cost(spend: pd.Series, signups: pd.Series) -> pd.Series: 
    """Acquisition cost per user is total spend divided by number of signups.""" 
    return spend / signups
```

We also write functions for the other four features. 
他の4つの特徴のための関数も作成します。
At first glance, this increases the number of lines of code we have to write. 
一見すると、これにより書かなければならないコードの行数が増えます。
However, we now have a documented function that can potentially be reused within the same program or by different programs. 
しかし、これにより、同じプログラム内または異なるプログラムによって再利用される可能性のある文書化された関数を持つことができます。
We can now write a unit test for `acquisition_cost`, as follows: 
これで、`acquisition_cost`のユニットテストを次のように書くことができます:
(確かにSQL等でまとめて複数の特徴量を計算する場合って、単体テストとかで特徴量生成の動作は保証できないよなぁ...:thinking:)

```python
@pytest.fixture 
def get_spends(self) -> pd.DataFrame: 
    return pd.DataFrame([20, 40], [5, 4], [4, 10], 
                         columns=["spends", "signups", "acquisition_cost"]) 

def test_spend_per_signup(get_spends: Callable): 
    df = get_spends() 
    df["res"] = acquisition_cost(df["spends"], df["signups"]) 
    pd.testing.assert_series_equal(df["res"], df["acquisition_cost"])
```

This unit test enforces a contract for how `acquisition_cost` is computed. 
このユニットテストは、**`acquisition_cost`がどのように計算されるかの契約を強制**します。
If anybody changes how `acquisition_cost` is computed, the unit test will fail, indicating that its contract is broken for downstream clients that use the `acquisition_cost feature.` 
誰かが`acquisition_cost`の計算方法を変更すると、ユニットテストは失敗し、`acquisition_cost feature`を使用する下流のクライアントに対してその契約が破損していることを示します。
You can, of course, still update the feature logic for `acquisition_cost`, but that should typically be performed by creating a new version of the feature, and the new version would require a new unit test. 
**もちろん、`acquisition_cost`の特徴ロジックを更新することはできますが、通常は特徴の新しいバージョンを作成することによって行われるべきであり、新しいバージョンには新しいユニットテストが必要です。** (なるほど。だからロジックを更新するたびに、新しい特徴量カラムが追加されていく運用を推奨してるのかな...!!:thinking:)
We will cover versioning features in Chapter 5. 
特徴のバージョン管理については第5章で説明します。(気になる...!!:thinking:)

<!-- ここまで読んだ! -->

In this example, our functions are data transformations on a DataFrame in a feature pipeline. 
この例では、私たちの関数は特徴パイプライン内のDataFrameに対するデータ変換です。
How does the feature pipeline save the final DataFrame to a feature store?
特徴パイプラインは最終的なDataFrameを特徴ストアにどのように保存するのでしょうか？
Feature stores typically provide DataFrame APIs (Pandas, Apache Spark, Polars) for ingesting DataFrames in a feature group, which is a table in which feature stores save their data. 
特徴ストアは通常、特徴グループ内のDataFrameを取り込むためのDataFrame API（Pandas、Apache Spark、Polars）を提供します。特徴グループは、特徴ストアがデータを保存するテーブルです。
Our approach to writing modular feature engineering is to build a DataFrame containing feature data (a featurized DataFrame) using feature functions (see Figure 2-3).  
modular feature engineeringを書くための私たちのアプローチは、特徴関数を使用して特徴データを含むDataFrame（特徴化されたDataFrame）を構築することです（図2-3を参照）。

![]()
_Figure 2-3. A Python-centric approach to writing feature pipelines involves building a DataFrame using feature functions and then writing it to a feature group in the feature store. The data can later be read from feature groups by training and inference pipelines using a feature query engine._  
図2-3. 特徴パイプラインを書くためのPython中心のアプローチは、feature functionsを使用してDataFrameを構築し、それを特徴ストアの特徴グループに書き込むことを含みます。データは後で、特徴クエリエンジンを使用してトレーニングおよび推論パイプラインによって特徴グループから読み取ることができます。

<!-- ここまで読んだ! -->

Each featurized DataFrame is written to a feature group in the feature store as a commit (append/update/delete). 
各特徴化されたDataFrameは、コミット（追加/更新/削除）として特徴ストアの特徴グループに書き込まれます。
The feature group stores the mutable set of features created over time. 
特徴グループは、時間の経過とともに作成された可変の特徴セットを保存します。
Training and inference pipelines can later use a feature query service to read a consistent snapshot of feature data from one or more feature groups to train a model or to make predictions, respectively. 
トレーニングおよび推論パイプラインは、後で特徴クエリサービスを使用して、1つまたは複数の特徴グループから特徴データの一貫したスナップショットを読み取り、モデルをトレーニングしたり予測を行ったりすることができます。

In this book, we will apply the feature functions approach to modularizing Python code for data transformations. 
この本では、**データ変換のためのPythonコードをモジュール化するためにfeature functionsアプローチを適用**します。
Although our previous example covered a feature pipeline, we will follow the same coding practice of encapsulating data transformations in functions in both training and inference pipelines. 
前の例では特徴パイプラインをカバーしましたが、トレーニングパイプラインと推論パイプラインの両方でデータ変換を関数にカプセル化する同じコーディングプラクティスに従います。
In the next section, we will see that some data transformations still need to be performed in training and inference pipelines, depending on the type of feature you are creating: a reusable feature, a model-specific feature, or a real-time feature. 
次のセクションでは、**作成している特徴のタイプ（再利用可能な特徴、モデル固有の特徴、またはリアルタイムの特徴）に応じて、トレーニングおよび推論パイプラインでまだ実行する必要があるデータ変換があること**を見ていきます。

<!-- ここまで読んだ! -->

### A Taxonomy for Data Transformations in ML Pipelines MLパイプラインにおけるデータ変換の分類

ML pipelines consist of a sequence of data transformations. 
**MLパイプラインは、一連のデータ変換で構成されています** (学習も推論も、全てデータ変換とみなせるのか...!!:thinking:)
From data sources, to features, to models and predictions, data is successively transformed from one format into another, until the final predictions are consumed by clients. 
データソースから特徴、モデル、予測に至るまで、データは次々と異なる形式に変換され、最終的な予測がクライアントによって消費されるまで続きます。
However, not all data transformations in ML pipelines are the same. 
しかし、MLパイプライン内のすべてのデータ変換が同じであるわけではありません。
Firstly, the feature store stores feature data that can be reused across many models. 
まず第一に、特徴ストアは多くのモデルで再利用できる特徴データを保存します。
That means feature pipelines that write feature data to the feature store should perform data transformations that create reusable features.  
つまり、**特徴データを特徴ストアに書き込む特徴パイプラインは、再利用可能な特徴を作成するデータ変換を実行する必要があります。**

Some data transformations, however, produce features that are not reusable across models. 
しかし、いくつかのデータ変換は、モデル間で再利用できない特徴を生成します。
For example, many ML frameworks require you to transform strings into a numerical representation before they can be used as input. 
例えば、多くのMLフレームワークでは、**文字列を入力として使用する前に数値表現に変換する必要**があります。
This transformation is known as encoding a categorical variable and is parameterized by the set of categories found in the model’s training dataset. 
この変換は、カテゴリ変数のエンコーディングとして知られ、モデルのトレーニングデータセットに見つかるカテゴリのセットによってパラメータ化されます。
If you train two models on two different training datasets, each with a different set of categories, they will encode the strings differently. 
**異なるカテゴリのセットを持つ2つの異なるトレーニングデータセットで2つのモデルをトレーニングすると、それぞれが文字列を異なる方法でエンコードします。**
The data transformation is, therefore, specific to the model and its training dataset. 
したがって、このデータ変換はモデルとそのトレーニングデータセットに特有のものです。
Similarly, for numerical variables, we have data transformations that are parameterized by a model’s training dataset and, therefore, not reusable across models. 
同様に、**数値変数についても、モデルのトレーニングデータセットによってパラメータ化されたデータ変換があり、したがってモデル間で再利用できません**。
You can normalize or scale a numerical value using its mean/minimum/maximum/standard deviation that you calculate from values in the training data. 
例えばトレーニングデータの値から計算した平均/最小/最大/標準偏差を使用して、数値を正規化またはスケーリングできます。
Some models need normalized numerical variables, such as gradient-descent models (deep learning), while others, such as decision trees, do not benefit from normalization. 
一部のモデルは正規化された数値変数を必要とします（勾配降下モデル（深層学習）など）が、決定木などの他のモデルは正規化から利益を得ません。

<!-- ここまで読んだ! -->

Another data transformation that is performed outside of a feature pipeline is a real-time data transformation that’s performed in real-time ML systems. 
特徴パイプラインの外で実行される別のデータ変換は、リアルタイムMLシステムで実行されるリアルタイムデータ変換です。
Feature pipelines precompute features, but online models may need data transformations on parameters to a prediction request. 
**特徴パイプラインは特徴を事前計算しますが、オンラインモデルは予測リクエストのパラメータに対するデータ変換を必要とする場合があります。** (例えば検索クエリとか?? 推論の時間帯などのcontextとか??:thinking:)
These on-demand transformations are performed in online inference pipelines, for example, in a Python user-defined function. 
これらのオンデマンド変換は、例えばPythonのユーザー定義関数内のオンライン推論パイプラインで実行されます。

<!-- ここまで読んだ! -->

To address both of these challenges, we now introduce a taxonomy for data transformations in ML pipelines that use a feature store. 
**これらの2つの課題**に対処するために、特徴ストアを使用するMLパイプラインにおけるデータ変換の分類を紹介します。
The taxonomy organizes data transformations into three different classes: model-dependent, model-independent, and on-demand transformations. 
この分類は、**データ変換を3つの異なるクラスに整理します：モデル依存、モデル非依存、オンデマンド変換**です。
This classification helps inform you in which ML pipeline(s) to implement the data transformation. 
この分類は、**どのMLパイプラインでそのデータ変換を実装するか**を知らせるのに役立ちます。
But, before looking at the taxonomy, we will first introduce feature types. 
しかし、分類を見る前に、まず特徴のタイプを紹介します。

<!-- ここまで読んだ! -->

#### Feature Types and Model-Dependent Transformations 特徴タイプとモデル依存変換

A data type for a variable in a programming language defines the set of valid operations on that variable—invalid operations will cause an error, at either compile time (in Java and Rust) or runtime (in Python). 
プログラミング言語における変数のデータ型は、その変数に対する有効な操作のセットを定義します—無効な操作は、コンパイル時（JavaやRust）または実行時（Python）にエラーを引き起こします。
Feature types are data type extensions that are useful for understanding the set of valid transformations on a variable in ML. 
**特徴タイプは、MLにおける変数の有効な変換のセットを理解するのに役立つデータ型の拡張**です。
For example, we can encode a categorical variable, but we cannot encode a numerical feature. 
例えば、カテゴリ変数をエンコードできますが、数値特徴をエンコードすることはできません。
Similarly, we can tokenize a string (categorical) input into an LLM but not a numerical feature. 
同様に、文字列（カテゴリ）入力をLLMにトークン化できますが、数値特徴はできません。
We can normalize, standardize, or scale a numerical variable but not a categorical variable. 
数値変数を正規化、標準化、またはスケーリングできますが、カテゴリ変数はできません。

<!-- ここまで読んだ! -->

In Figure 2-4, we define the set of feature types as categorical variables (strings, enums, booleans), numerical variables (int, float, double), and arrays (lists, vector embeddings). 
図2-4では、**特徴タイプのセットをカテゴリ変数（文字列、列挙型、ブール値）、数値変数（int、float、double）、および配列（リスト、ベクトル埋め込み）として定義**します。
In ML literature, arrays are not often described as a feature type. 
ML文献では、配列は特徴タイプとしてあまり説明されません。
However, they are now ubiquitous in AI systems, in particular as vector embeddings. 
しかし、現在、配列はAIシステムにおいて普遍的であり、特にベクトル埋め込みとして使用されています。
A vector embedding is a fixed-size array of either floating-point numbers or integers that stores a compressed representation of some higher-dimensional data. 
ベクトル埋め込みは、浮動小数点数または整数の固定サイズの配列であり、いくつかの高次元データの圧縮表現を保存します。
Lists and vector embeddings are now widely supported as data types in feature stores—and they have well-defined sets of valid transformations. 
リストとベクトル埋め込みは、現在、特徴ストアでデータ型として広くサポートされており、明確に定義された有効な変換のセットを持っています。
For example, taking the three most recent entries in a list is a valid operation on a list, as is indexing/querying a vector embedding. 
例えば、リスト内の3つの最新のエントリを取得することはリストに対する有効な操作であり、ベクトル埋め込みのインデックス付け/クエリも同様です。

![]()
_Figure 2-4. Feature types in ML can be categorized into one of three different classes: categorical, numerical, or an array. Within those categories, there are further subclasses. Ordinal variables have a natural order (e.g., low/medium/high), while nominal variables do not. Ratio variables have a defined zero point, while interval variables do not. Arrays can be lists of values or embedding vectors._  
図2-4. MLにおける特徴タイプは、3つの異なるクラスのいずれかに分類できます：カテゴリ、数値、または配列。そのカテゴリ内にはさらにサブクラスがあります。順序変数には自然な順序があります（例：低/中/高）が、名義変数にはありません。比率変数には定義されたゼロ点がありますが、区間変数にはありません。配列は値のリストまたは埋め込みベクトルです。

<!-- ここまで読んだ! -->

Feature types lack programming language support; instead, they are supported in ML frameworks and libraries. 
**特徴タイプはプログラミング言語のサポートが不足しています。代わりに、MLフレームワークやライブラリでサポートされています。**
For example, in Python, you may use an ML framework such as Scikit-Learn, TensorFlow, XGBoost, or PyTorch, and each framework has its own implementation of the encoding/scaling/normalization/min-max scaling transformations for their own feature types. 
例えば、Pythonでは、Scikit-Learn、TensorFlow、XGBoost、またはPyTorchなどのMLフレームワークを使用することができ、各フレームワークはそれぞれの特徴タイプに対するエンコーディング/スケーリング/正規化/最小-最大スケーリング変換の独自の実装を持っています。

These transformations are specific to ML. 
これらの変換はMLに特有のものです。
They make feature data compatible with a particular ML framework or improve model performance, such as normalization that improves convergence of gradient-descent-based ML algorithms. 
これにより、特徴データは特定のMLフレームワークと互換性があり、勾配降下ベースのMLアルゴリズムの収束を改善する正規化など、モデルのパフォーマンスを向上させます。
As described earlier, these transformations are not reusable across other models, and for this reason, we call these transformations model-dependent transformations (MDTs). 
前述のように、**これらの変換は他のモデル間で再利用できず、この理由から、これらの変換をモデル依存変換（MDT）と呼びます。**

The transformations are dependent on the model and/or its training data. 
これらの変換はモデルおよび/またはそのトレーニングデータに依存しています。
You should not perform these transformations in feature pipelines, before the feature store. 
これらの変換は、特徴ストアの前に特徴パイプラインで実行すべきではありません。
Instead, you should apply MDTs twice: first in the training pipeline, when creating training data, and second in the inference pipeline. 
**代わりに、MDTを2回適用する必要があります：最初はトレーニングデータを作成する際のトレーニングパイプラインで、2回目は推論パイプラインでです。** (だよね...!:thinking:)
And as the training and inference pipelines are different programs, you need to make sure there is no skew between the implementation of your MDTs in the training and inference pipelines. 
トレーニングパイプラインと推論パイプラインは異なるプログラムであるため、**トレーニングパイプラインと推論パイプラインにおけるMDTの実装間に偏りがないことを確認する必要**があります。
If there is skew, your model may perform poorly, and it will be difficult to identify the cause of the poor performance. 
偏りがあると、モデルのパフォーマンスが低下し、パフォーマンスの低下の原因を特定するのが難しくなります。

<!-- ここまで読んだ! -->

Another problem with MDTs is that the transformed feature data is not amenable to EDA. 
MDTのもう一つの問題は、変換された特徴データがEDA（探索的データ分析）に適していないことです。
For example, if you normalize the annual income variable, you make the data hard to analyze: it is easier for a data scientist to understand and visualize an income of $74,580 than its normalized value of 0.541. 
例えば、年収変数を正規化すると、データの分析が難しくなります。データサイエンティストにとって、$74,580の収入を理解し視覚化する方が、正規化された値0.541を理解するよりも簡単です。
There is also a problem with storing normalized/scaled/encoded feature data in the feature store. 
**正規化された/スケーリングされた/エンコードされた特徴データをフィーチャーストアに保存することにも問題があります。**
For example, if you have a feature group (table) that stores normalized new annual income data, every time you add/remove/update rows in that table, you have to recompute all of the existing annual income feature data, as the new data changes the mean/standard deviation for existing rows. 
例えば、正規化された新しい年収データを保存するフィーチャーグループ（テーブル）がある場合、そのテーブルに行を追加/削除/更新するたびに、既存の年収特徴データをすべて再計算する必要があります。新しいデータが既存の行の平均/標準偏差を変更するためです。
This makes even very small writes to a feature group very expensive (this is called write amplification). 
**これにより、フィーチャーグループへの非常に小さな書き込みでさえも非常に高価になります。これを書き込み増幅（write amplification）と呼びます。**

<!-- ここまで読んだ! -->

#### Reusable Features with Model-Independent Transformations モデル非依存変換による再利用可能な特徴

Data engineers are typically not very familiar with the MDTs introduced in the last section, as they are specific to ML. 
データエンジニアは、通常、前のセクションで紹介されたMDTにあまり精通していません。これはMLに特有のものだからです。
The types of data transformations that data engineers are familiar with that are widely used in feature engineering are (windowed) aggregations (such as the max/min of some numerical variable), windowed counts (for example, the number of clicks per day), and any transformations to create recency, frequency, monetary value (RFM) features. 
データエンジニアがよく知っている特徴エンジニアリングで広く使用されるデータ変換の種類は、**（ウィンドウ化された）集約（例えば、数値変数の最大/最小）、ウィンドウ化されたカウント（例えば、1日のクリック数）、および最近性、頻度、金銭的価値（RFM）特徴を作成するための変換**です。
These transformations create features that can be reused across many models and are called model-independent transformations (MITs). 
これらの変換は、**多くのモデルで再利用できる特徴を作成し、モデル非依存変換（MIT）**と呼ばれます。
MITs are computed once in batch or streaming feature pipelines, and the reusable feature data produced by them is stored in the feature store, to be used later by downstream training and inference pipelines. 
MITは、バッチまたはストリーミングフィーチャーパイプラインで一度計算され、それによって生成された再利用可能な特徴データはフィーチャーストアに保存され、後で下流のトレーニングおよび推論パイプラインで使用されます。

<!-- ここまで読んだ! -->

#### Real-Time Features with On-Demand Transformations オンデマンド変換によるリアルタイム特徴

What if I have a real-time ML system and the data required to compute my feature is only available as part of a prediction request? 
リアルタイムMLシステムがあり、**特徴を計算するために必要なデータが予測リクエストの一部としてのみ利用可能な場合**はどうなりますか？(まさに検索クエリとかだね...!!:thinking:)
In that case, I will have to compute the feature in the online inference pipeline in what is called an on-demand transformation (ODT). 
その場合、**オンライン推論パイプラインで特徴を計算する必要があり、これをオンデマンド変換（ODT）**と呼びます。
Often, the prediction requests and their parameters are logged for later use. 
**しばしば、予測リクエストとそのパラメータは後で使用するためにログに記録されます。**
For example, you may want to reuse the same input data to create reusable feature data for the feature store. 
例えば、同じ入力データを再利用してフィーチャーストアの再利用可能な特徴データを作成したい場合があります。
Or you could use that historical data as inputs for MDTs. 
また、その履歴データをMDTの入力として使用することもできます。
We will see in Chapter 7 how you can implement ODTs as user-defined functions (UDFs). 
第7章では、ODTをユーザー定義関数（UDF）として実装する方法を見ていきます。
And the same UDF used in an online inference pipeline can be reused in a feature pipeline to create reusable features from historical data. 
**オンライン推論パイプラインで使用される同じUDFは、フィーチャーパイプラインで再利用され、履歴データから再利用可能な特徴を作成できます。** (上述されてるように、予測リクエストとそのパラメータはログに記録されるから...!!:thinking:)
Our approach will prevent skew—there should be no difference between the data transformation in the online inference pipeline and the data in the feature pipeline.
私たちのアプローチは、スキューを防ぎます。オンライン推論パイプラインのデータ変換とフィーチャーパイプラインのデータの間に違いがあってはなりません。(UDFで共通化してるから??:thinking:)

<!-- ここまで読んだ! -->

#### The ML Transformation Taxonomy and ML Pipelines ML変換の分類とMLパイプライン

Now that we have introduced the three different types of features and the three different data transformations that create them (model-independent, model-dependent, and on-demand), we can present a taxonomy for data transformations in ML (see Figure 2-5). 
異なる3種類の特徴と、それらを生成する3種類のデータ変換（モデル非依存、モデル依存、オンデマンド）を紹介したので、MLにおけるデータ変換の分類を提示できます（図2-5を参照）。
Our taxonomy includes:
私たちの分類には以下が含まれます：

- Model-independent transformations that produce reusable features that are stored in a feature store
  - 再利用可能な特徴を生成し、フィーチャーストアに保存されるモデル非依存変換
- Model-dependent transformations that produce features specific to a single model
  - 単一のモデルに特有の特徴を生成するモデル依存変換
- On-demand transformations that require request-time data to be computed in online inference pipelines but can also be computed in feature pipelines on historical data
  - リクエスト時のデータをオンライン推論パイプラインで計算する必要があるオンデマンド変換ですが、履歴データのフィーチャーパイプラインでも計算できます。

![]()
_Figure 2-5. The taxonomy of data transformations for ML that create reusable features, model-specific features, and real-time features._
_図2-5. 再利用可能な特徴、モデル特有の特徴、リアルタイム特徴を生成するMLのデータ変換の分類。_

<!-- ここまで読んだ! -->

In Figure 2-6, we can see how the different data transformations in our taxonomy map onto our FTI pipelines. 
図2-6では、私たちの分類における異なるデータ変換がFTIパイプラインにどのようにマッピングされるかを見ることができます。

![]()
_Figure 2-6. Data transformations for ML and the ML pipelines they are performed in._
_図2-6. MLのデータ変換とそれが実行されるMLパイプライン。_

Notice that MITs are only performed in feature pipelines. 
**MITはフィーチャーパイプラインでのみ実行されることに注意**してください。
However, MDTs are performed in both the training and inference pipelines. 
しかし、MDTはトレーニングパイプラインと推論パイプラインの両方で実行されます。
On-demand transformations are also performed in two different pipelines—the online inference pipeline and the feature pipeline. 
オンデマンド変換は、オンライン推論パイプラインとフィーチャーパイプラインの2つの異なるパイプラインでも実行されます。
Batch inference pipelines do not support ODTs, as they do not have request-time parameters—their precomputed features are computed in feature pipelines, and any inference time transformations are MDTs. 
**バッチ推論パイプラインはODTをサポートしていません。リクエスト時のパラメータがないためです。**事前計算された特徴はフィーチャーパイプラインで計算され、推論時の変換はMDTです。
Whenever the same data transformation is performed in different pipelines, you need to ensure there is no skew between the different implementations. 
**異なるパイプラインで同じデータ変換が実行される場合、異なる実装間にスキューがないことを確認する必要があります。**
One final point to note is that MDTs can also be applied to request parameters in online inference pipelines, but they differ from ODTs in that they cannot be applied in feature pipelines. 
**最後に注意すべき点は、MDTはオンライン推論パイプラインのリクエストパラメータにも適用できますが、フィーチャーパイプラインには適用できないため、ODTとは異なります。** (ふむふむなるほど...!!:thinking:)
So some real-time features can be model-independent features, while others are model-dependent. 
したがって、**一部のリアルタイム特徴はモデル非依存特徴であり、他はモデル依存特徴**です。
We call the real-time, model-independent features the on-demand features. 
**リアルタイムのモデル非依存特徴をオンデマンド特徴**と呼びます。

Now that we have introduced our classification of data transformations, we can dive into more details on our three ML pipelines, starting with the feature pipeline. 
データ変換の分類を紹介したので、フィーチャーパイプラインから始めて、3つのMLパイプラインの詳細に入っていきましょう。

<!-- ここまで読んだ! -->

### Feature Pipelines フィーチャーパイプライン

A feature pipeline is a program that orchestrates the execution of a dataflow graph of model-independent and on-demand data transformations. 
フィーチャーパイプラインは、モデル非依存およびオンデマンドデータ変換のデータフローグラフの実行を調整するプログラムです。
These transformations include extracting data from a source, data validation and cleaning, feature extraction, aggregation, dimensionality reduction (such as creating vector embeddings), binning, feature crossing, and other feature engineering steps on input data to create and/or update feature data. 
これらの変換には、ソースからデータを抽出すること、データの検証とクリーニング、特徴抽出、集約、次元削減（ベクトル埋め込みの作成など）、ビニング、特徴交差、および入力データに対するその他の特徴エンジニアリングステップが含まれ、特徴データを作成および/または更新します。

A batch or streaming feature pipeline can apply some or all of these types of data transformations to create features that are stored in a feature store, as shown in Figure 2-7. 
バッチまたはストリーミングフィーチャーパイプラインは、これらのデータ変換のいくつかまたはすべてを適用して、フィーチャーストアに保存される特徴を作成できます（図2-7参照）。
The figure also shows two other specialized feature pipelines: a vector embedding pipeline, which creates vector embeddings that are stored in a vector index (in the feature store), and the feature data validation pipeline, which is an asynchronous program that runs data validation rules against feature data stored in a feature store. 
この図には、**ベクトル埋め込みを作成し、ベクトルインデックス（フィーチャーストア内）に保存するベクトル埋め込みパイプラインと、フィーチャーストアに保存された特徴データに対してデータ検証ルールを実行する非同期プログラムであるフィーチャーデータ検証パイプラインの2つの専門的なフィーチャーパイプライン達**も示されています。

![]()
_Figure 2-7. Classes of feature pipeline._
_図2-7. フィーチャーパイプラインのクラス。_

<!-- ここまで読んだ! -->

A feature pipeline is, however, more than just a program that executes data transformations. 
しかし、**フィーチャーパイプラインは単にデータ変換を実行するプログラム以上のもの**です。
It has to be able to connect and read data from the data sources, it needs to save its feature data to a feature store, and it also has nonfunctional requirements, such as: 
データソースからデータを接続して読み取ることができ、フィーチャーデータをフィーチャーストアに保存する必要があり、また、以下のような**非機能要件**もあります：

- _Backfilling or incremental data_ 
The same feature pipeline should be able to create feature data using historical data or new data (production) that arrives in batches or as a stream of incoming data. 
_バックフィリングまたは増分データ_ 同じフィーチャーパイプラインは、履歴データまたはバッチまたはストリーミングで到着する新しいデータ（プロダクション）を使用してフィーチャーデータを作成できる必要があります。

- Fault tolerance フォールトトレランス
Failures and retries in feature pipelines should not result in corrupt or duplicate data. 
**フィーチャーパイプラインでの失敗や再試行は、破損したデータや重複データを生じるべきではありません。**

- Scalability スケーラビリティ
You must ensure that the feature pipeline is provisioned with enough resources to process the expected data volume. 
フィーチャーパイプラインが予想されるデータ量を処理するために十分なリソースを確保していることを確認する必要があります。

- Feature freshness フィーチャーの新鮮さ
What is the maximum permissible age of precomputed feature data used by clients? 
**クライアントが使用する事前計算されたフィーチャーデータの最大許容年齢はどのくらいですか？**
Do feature freshness requirements mean you have to implement the feature pipeline as a stream processing program, or can it be a batch program? 
フィーチャーの新鮮さの要件は、フィーチャーパイプラインをストリーム処理プログラムとして実装する必要があることを意味しますか、それともバッチプログラムとして実装できますか？

- Governance and security requirements ガバナンスとセキュリティ要件
Where can the data be processed, who can process the data, will processing create a tamperproof audit log, and will the features be organized and tagged for discoverability? 
データはどこで処理できますか？誰がデータを処理できますか？処理は改ざん防止の監査ログを作成しますか？特徴は整理され、発見可能性のためにタグ付けされますか？

- Data quality guarantees データ品質保証
Does your feature pipeline validate data before it is written to the feature store or asynchronously, after the data has landed in the feature store? 
フィーチャーパイプラインは、データがフィーチャーストアに書き込まれる前にデータを検証しますか、それともデータがフィーチャーストアに到着した後に非同期で検証しますか？(今は前者でやってるな〜...!!:thinking:)

<!-- ここまで読んだ! -->

Let’s start with the data sources for your feature pipeline—where do they come from?
フィーチャーパイプラインのデータソースはどこから来るのか、始めましょう。
Imagine developing a new feature pipeline and getting data from a source you’ve never parsed before (for example, an existing table in a data warehouse). 
新しいフィーチャーパイプラインを開発し、以前に解析したことのないソース（例えば、データウェアハウス内の既存のテーブル）からデータを取得することを想像してください。
The table may have been gathering data for a while, so you could run your data transformations against the historical data in the table to backfill feature data into your feature store.
そのテーブルはしばらくデータを収集していた可能性があるため、テーブル内の履歴データに対してデータ変換を実行して、フィーチャーストアにフィーチャーデータをバックフィルすることができます。
You may also want to change the data transformations in your feature pipeline, so again, you’ll want to backfill feature data from the source table (with your new transformations). 
**フィーチャーパイプラインのデータ変換を変更したい場合もあるため、再度、ソーステーブルからフィーチャーデータをバックフィルしたいと思うでしょう（新しい変換を使用して）。** (これめっちゃあるんだよなぁ...!!:thinking:)
Your data warehouse table will also probably have new data available at some cadence (for example, hourly or daily). 
**データウェアハウステーブルには、一定の間隔（例えば、毎時または毎日）で新しいデータが利用可能になる可能性**もあります。
In this case, your feature pipeline should be able to extract the new data from the table, compute the new feature data, and make incremental updates (appends, deletes, or updates) to the feature data in the feature store. 
この場合、フィーチャーパイプラインはテーブルから新しいデータを抽出し、新しいフィーチャーデータを計算し、フィーチャーストア内のフィーチャーデータに対して増分更新（追加、削除、または更新）を行うことができる必要があります。

<!-- ここまで読んだ! -->

What does the feature data that is created by your feature pipeline look like? 
フィーチャーパイプラインによって作成されるフィーチャーデータはどのようなものですか？
The output feature data is typically in tabular format (one or more DataFrame[s] or table[s]) and is typically stored in a feature group(s) in the feature store. 
出力フィーチャーデータは通常、表形式（1つ以上のDataFrameまたはテーブル）であり、通常はフィーチャーストアのフィーチャーグループに保存されます。
Feature groups store feature data in tables that are used by clients for both training and inference (both online applications and batch programs). 
フィーチャーグループは、トレーニングと推論（オンラインアプリケーションとバッチプログラムの両方）にクライアントが使用するテーブルにフィーチャーデータを保存します。

<!-- ここまで読んだ! -->

Ideally, feature pipelines should be tolerant of failures by being idempotent and making atomic updates to feature groups. 
**理想的には、フィーチャーパイプラインは冪等性を持ち、フィーチャーグループに対して原子的な更新を行うことで、失敗に対して耐性を持つべき**です。
_Idempotence implies they should produce the same result even if they are run more than once._ 
_冪等性は、複数回実行されても同じ結果を生成する必要があることを意味します。_
_Atomicity implies that updates should be applied all at once, so if a feature pipeline fails before completion, partial updates with corrupted or missing data should not be applied to feature groups._ 
_原子性は、更新が一度に適用されるべきであり、フ**ィーチャーパイプラインが完了する前に失敗した場合、破損したデータや欠損データを含む部分的な更新がフィーチャーグループに適用されるべきではないこと**を意味します。_
The benefit of idempotence and atomicity is that you can safely rerun a feature pipeline in the event of a failure. 
**冪等性と原子性の利点は、失敗が発生した場合にフィーチャーパイプラインを安全に再実行できること**です。

<!-- ここまで読んだ! -->

You can address scalability and feature freshness requirements by implementing a feature pipeline in one of a number of different frameworks and languages. 
スケーラビリティとフィーチャーの新鮮さの要件に対処するために、さまざまなフレームワークや言語のいずれかでフィーチャーパイプラインを実装できます。
You have to select the best technology based on your feature freshness requirements, your data input sizes, and the skills available in your team. 
フィーチャーの新鮮さの要件、データ入力サイズ、およびチームに利用可能なスキルに基づいて、最適な技術を選択する必要があります。

Different data processing engines have different capabilities for (1) efficient processing, (2) scalable processing, and (3) ease of development and operation. 
異なるデータ処理エンジンは、（1）効率的な処理、（2）スケーラブルな処理、（3）開発と運用の容易さに対して異なる能力を持っています。

For example, if your batch feature pipeline processes less than 1 GB per execution, Pandas is a good framework to start with. 
例えば、バッチフィーチャーパイプラインが1回の実行で1GB未満を処理する場合、Pandasは良いフレームワークの出発点です。

For workloads up to 10s of GBs, Polars is a good choice. 
10GBまでのワークロードには、Polarsが良い選択です。

And for TB-scale workloads, Apache Spark and SQL are popular choices. 
TBスケールのワークロードには、Apache SparkとSQLが人気の選択肢です。

While we have looked at DataFrame processing frameworks so far, dbt is also a popular framework for executing feature pipelines defined in SQL. 
これまでDataFrame処理フレームワークを見てきましたが、dbtもSQLで定義されたフィーチャーパイプラインを実行するための人気のフレームワークです。



. While we have looked at DataFrame processing frameworks so far, dbt is also a popular framework for executing feature pipelines defined in SQL. 
これまでDataFrame処理フレームワークを見てきましたが、dbtはSQLで定義されたフィーチャーパイプラインを実行するための人気のあるフレームワークでもあります。

The dbt framework adds some modularity to SQL by enabling transformations to be defined in separate files (dbt calls them models) as a form of pipeline. 
dbtフレームワークは、変換を別のファイル（dbtではモデルと呼ばれます）で定義できるようにすることで、SQLにいくつかのモジュール性を追加します。

The pipelines can then be chained together to implement a feature pipeline, with the final output to a feature group in a feature store. 
これにより、パイプラインを連結してフィーチャーパイプラインを実装でき、最終的な出力はフィーチャーストアのフィーチャーグループに送られます。

When your AI system needs fresh feature data, you may need to use stream processing to compute features. 
AIシステムが新鮮なフィーチャーデータを必要とする場合、フィーチャーを計算するためにストリーム処理を使用する必要があるかもしれません。

For stream processing feature pipelines that produce the freshest features, Feldera is an open source SQL-based engine that has a low barrier to entry, while larger-scale workloads can use Apache Flink, which scales to PB-sized workloads. 
最新のフィーチャーを生成するストリーム処理フィーチャーパイプラインには、FelderaというオープンソースのSQLベースのエンジンがあり、参入障壁が低い一方で、大規模なワークロードにはPBサイズのワークロードにスケールするApache Flinkを使用できます。

If you want Python-based streaming feature pipelines, then Spark Structured Streaming is a reasonable choice, although it introduces more latency than either Feldera or Flink due to the fact that it processes events in batches (instead of per event). 
Pythonベースのストリーミングフィーチャーパイプラインを希望する場合、Spark Structured Streamingは合理的な選択ですが、イベントをバッチで処理するため（イベントごとではなく）、FelderaやFlinkよりも遅延が大きくなります。

We cover batch feature pipelines in Chapter 8 and streaming feature pipelines in Chapter 9. 
バッチフィーチャーパイプラインについては第8章で、ストリーミングフィーチャーパイプラインについては第9章で説明します。

###### Training Pipelines
###### トレーニングパイプライン

A training pipeline is a program that performs tasks from reading feature data from a feature store, to applying model-dependent transformations to the feature data, to training a model with an ML framework, to validating the trained model for performance and absence of bias, to publishing the model to a model registry, and finally to deploying the model to production for inference. 
トレーニングパイプラインは、フィーチャーストアからフィーチャーデータを読み取り、モデル依存の変換をフィーチャーデータに適用し、MLフレームワークでモデルをトレーニングし、トレーニングされたモデルの性能とバイアスの有無を検証し、モデルをモデルレジストリに公開し、最終的に推論のためにモデルを本番環境にデプロイするタスクを実行するプログラムです。

Training pipelines are run either on demand or on a schedule (for example, new models could be retrained and redeployed once per day or week). 
トレーニングパイプラインは、オンデマンドまたはスケジュールに従って実行されます（たとえば、新しいモデルは1日または1週間に1回再トレーニングおよび再デプロイされる可能性があります）。

Figure 2-8 shows four different classes of training pipeline. 
図2-8は、4つの異なるトレーニングパイプラインのクラスを示しています。

The first class is the complete training pipeline that performs all of the training pipeline tasks. 
最初のクラスは、トレーニングパイプラインのすべてのタスクを実行する完全なトレーニングパイプラインです。

It starts by selecting, filtering, and joining the feature data it needs from the feature store, and it completes when it has uploaded a trained and validated model to the model registry. 
これは、フィーチャーストアから必要なフィーチャーデータを選択、フィルタリング、結合することから始まり、トレーニングされ検証されたモデルをモデルレジストリにアップロードしたときに完了します。

_Figure 2-8. Classes of training pipelines._
_Figure 2-8. トレーニングパイプラインのクラス_

Other specialized training pipelines can perform subsets of these tasks. 
他の専門的なトレーニングパイプラインは、これらのタスクのサブセットを実行できます。

A model deployment pipeline downloads a model from a model registry and deploys it for batch or online serving. 
モデルデプロイメントパイプラインは、モデルレジストリからモデルをダウンロードし、バッチまたはオンラインサービス用にデプロイします。

For online models, the model is typically deployed to model serving infrastructure. 
オンラインモデルの場合、モデルは通常、モデルサービスインフラストラクチャにデプロイされます。

It is often a separate pipeline from the training pipeline, as it is an operational step that may require human approval and may need to be reverted if there is a problem with the deployment. 
これは、デプロイメントに問題が発生した場合に人間の承認が必要であったり、元に戻す必要がある運用ステップであるため、トレーニングパイプラインとは別のパイプラインであることが多いです。

Model deployment often involves A/B tests, in which the model is first deployed as a shadow version and later promoted to the active version if it demonstrates good enough performance and behavior. 
モデルデプロイメントには、A/Bテストが含まれることが多く、モデルは最初にシャドーバージョンとしてデプロイされ、十分な性能と動作を示した場合にアクティブバージョンに昇格されます。

Model validation can also be performed in its own model validation pipeline, where the model is asynchronously evaluated for performance and compliance after it has been saved to the model registry. 
モデル検証は、モデルがモデルレジストリに保存された後に性能とコンプライアンスが非同期に評価されるモデル検証パイプラインでも実行できます。

This is useful when model validation is a computationally intensive step that does not require GPUs but the model training pipeline uses GPUs. 
これは、モデル検証がGPUを必要としない計算集約的なステップであり、モデルトレーニングパイプラインがGPUを使用する場合に便利です。

This way, model training can complete and release the GPUs, and model validation can run later on cheaper CPUs. 
このようにして、モデルトレーニングは完了し、GPUを解放でき、モデル検証は後でより安価なCPUで実行できます。

For models with large training datasets that take time to materialize, the training pipeline can be further decomposed into a training dataset pipeline, which selects, filters, and joins feature data from a feature store, applies model-dependent transformations to the feature data, and saves the final training data as files. 
大規模なトレーニングデータセットを持ち、具現化に時間がかかるモデルの場合、トレーニングパイプラインはさらにトレーニングデータセットパイプラインに分解でき、フィーチャーストアからフィーチャーデータを選択、フィルタリング、結合し、モデル依存の変換をフィーチャーデータに適用し、最終的なトレーニングデータをファイルとして保存します。

The files are stored in a filesystem or an object store (such as S3). 
ファイルはファイルシステムまたはオブジェクトストア（S3など）に保存されます。

###### Inference Pipelines
###### 推論パイプライン

An inference pipeline is a program that reads in new feature data (either precomputed or as parameters in a prediction request), applies transformations to the feature data (on-demand and/or model-dependent transformations), and outputs predictions with the model. 
推論パイプラインは、新しいフィーチャーデータ（事前計算されたものまたは予測リクエストのパラメータとして）を読み込み、フィーチャーデータに変換を適用し（オンデマンドおよび/またはモデル依存の変換）、モデルを使用して予測を出力するプログラムです。

Depending on whether the ML system is a real-time (interactive) ML system or a batch ML system, your inference pipeline will be either a batch program or a program invoked by a prediction request on the model serving infrastructure. 
MLシステムがリアルタイム（インタラクティブ）MLシステムであるかバッチMLシステムであるかに応じて、推論パイプラインはバッチプログラムまたはモデルサービスインフラストラクチャ上の予測リクエストによって呼び出されるプログラムのいずれかになります。

Agents are mostly interactive AI systems, where client queries trigger a loop of LLM calls and external tool executions before a response is returned. 
エージェントは主にインタラクティブなAIシステムであり、クライアントのクエリがLLM呼び出しと外部ツールの実行のループをトリガーし、応答が返される前に実行されます。

Figure 2-9 shows three classes of inference pipelines: batch inference pipelines, online inference pipelines, and agentic pipelines. 
図2-9は、バッチ推論パイプライン、オンライン推論パイプライン、およびエージェントパイプラインの3つのクラスを示しています。

_Figure 2-9. Classes of inference pipeline._
_Figure 2-9. 推論パイプラインのクラス_

The batch inference pipeline reads inference data as precomputed features from the feature store, downloads the model from the model registry, and outputs predictions using the inference data as input into the model. 
バッチ推論パイプラインは、フィーチャーストアから事前計算されたフィーチャーとして推論データを読み込み、モデルレジストリからモデルをダウンロードし、推論データをモデルへの入力として使用して予測を出力します。

Batch inference pipelines are typically implemented as Python programs using Pandas, Polars, or Spark, although some data warehouses now support batch inference with UDFs using SQL. 
バッチ推論パイプラインは通常、Pandas、Polars、またはSparkを使用したPythonプログラムとして実装されますが、一部のデータウェアハウスは現在、SQLを使用したUDFでバッチ推論をサポートしています。

Batch inference pipelines are run on a schedule by some orchestrator (such as Apache Airflow) and make predictions for all the rows in the input DataFrame (or SQL table) using the model, and the predictions are typically stored in a table in a database, from where consumers use those predictions. 
バッチ推論パイプラインは、Apache Airflowなどのオーケストレーターによってスケジュールに従って実行され、モデルを使用して入力DataFrame（またはSQLテーブル）のすべての行に対して予測を行い、予測は通常データベースのテーブルに保存され、消費者はそれらの予測を使用します。

An example of a batch inference ML system was a daily surf height prediction service I wrote for a beach in Ireland (Lahinch), where I have surfed a lot. 
バッチ推論MLシステムの例として、私がアイルランドのビーチ（ラヒンチ）で書いた日々のサーフ高さ予測サービスがあります。私はそこでたくさんサーフィンをしました。

It scrapes data from weather and ocean swell forecast websites and publishes a dashboard every day. 
これは、天気と海のうねり予測のウェブサイトからデータをスクレイピングし、毎日ダッシュボードを公開します。

Batch inference pipelines tend not to have a large number of parameters. 
バッチ推論パイプラインは、多くのパラメータを持たない傾向があります。

Maybe they will be parameterized by a start_time and end_time or the last_processed_timestamp for inference data. 
おそらく、推論データのstart_timeとend_time、またはlast_processed_timestampでパラメータ化されるでしょう。

Or maybe the inference data will be a set of entities (such as users), in which case we pass the entity IDs as a parameter. 
または、推論データがエンティティのセット（ユーザーなど）である場合、その場合はエンティティIDをパラメータとして渡します。

An online inference pipeline takes the request parameters, reads any precomputed features from the feature store if needed, performs any data transformations on the precomputed features and request parameters to create a feature vector, calls the model with the feature vector, logs the prediction and features (for monitoring and debugging), and finally returns the prediction to the client. 
オンライン推論パイプラインは、リクエストパラメータを受け取り、必要に応じてフィーチャーストアから事前計算されたフィーチャーを読み込み、事前計算されたフィーチャーとリクエストパラメータに対してデータ変換を行い、フィーチャーベクトルを作成し、フィーチャーベクトルを使用してモデルを呼び出し、予測とフィーチャーをログに記録（監視とデバッグ用）し、最終的に予測をクライアントに返します。

An online inference pipeline is a network-hosted service that makes predictions in response to prediction requests. 
オンライン推論パイプラインは、予測リクエストに応じて予測を行うネットワークホストサービスです。

It is typically a Python program and has an API called the deployment API, which is described in Chapter 11. 
これは通常Pythonプログラムであり、Chapter 11で説明されているデプロイメントAPIと呼ばれるAPIを持っています。

The deployment API includes ID(s) for the entities the prediction is being made for, as well as any parameters required to compute real-time features for the model. 
デプロイメントAPIには、予測が行われるエンティティのIDと、モデルのリアルタイムフィーチャーを計算するために必要なパラメータが含まれています。

The ID(s) are used to retrieve precomputed features for the entities. 
IDは、エンティティの事前計算されたフィーチャーを取得するために使用されます。

The Python program for the online inference pipeline is typically deployed alongside the model on a model serving infrastructure, such as KServe or a FastAPI server. 
オンライン推論パイプラインのPythonプログラムは、通常、KServeやFastAPIサーバーなどのモデルサービスインフラストラクチャ上でモデルと一緒にデプロイされます。

See Chapter 11 for details. 
詳細については第11章を参照してください。

Finally, the agentic pipeline is similar to an online inference pipeline in that it is a network-hosted Python program that has a deployment API for client queries and responses. 
最後に、エージェントパイプラインは、クライアントのクエリと応答のためのデプロイメントAPIを持つネットワークホストのPythonプログラムである点で、オンライン推論パイプラインに似ています。

The agent itself is typically written in an agentic framework, such as LlamaIndex, LangGraph, LangChain, or CrewAI. 
エージェント自体は通常、LlamaIndex、LangGraph、LangChain、またはCrewAIなどのエージェントフレームワークで記述されます。

The agent program has an LLM and access to a set of tools along with the schema for each tool. 
エージェントプログラムはLLMを持ち、各ツールのスキーマとともにツールのセットにアクセスします。

A tool is an action the agent can execute (such as making an external API call or querying a [RAG] data source). 
ツールは、エージェントが実行できるアクションです（外部API呼び出しや[RAG]データソースのクエリなど）。

The set of available tools is either statically defined or discovered by the agent at runtime. 
利用可能なツールのセットは、静的に定義されるか、エージェントが実行時に発見します。

After the agent receives a query from a client, it runs in a loop performing the following actions until it returns a response to the client. 
エージェントがクライアントからのクエリを受け取った後、クライアントに応答を返すまで、次のアクションを実行するループで実行されます。

First, it sends the LLM the query and the list of available tools, and it asks the LLM what tool it should use. 
最初に、LLMにクエリと利用可能なツールのリストを送信し、どのツールを使用すべきかをLLMに尋ねます。

The LLM returns with either one or more tools to use and the parameters for those tools or the final response to the client. 
LLMは、使用するツールとそのツールのパラメータ、またはクライアントへの最終応答を返します。

If the LLM responds with a tool to use, the agent executes the tool and sends the result, along with previous tool use history, to the LLM. 
LLMが使用するツールを返した場合、エージェントはそのツールを実行し、結果を以前のツール使用履歴とともにLLMに送信します。

The agent keeps looping in tool use/response steps until the LLM indicates a final response should be sent to the client. 
エージェントは、LLMがクライアントに最終応答を送信する必要があることを示すまで、ツール使用/応答ステップのループを続けます。

###### Titanic Survival as an ML System Built with ML Pipelines
###### MLパイプラインを使用して構築されたMLシステムとしてのタイタニック生存

We now introduce our first example ML system, which we built with our three ML pipelines, using one of the best-known ML problems—predicting the probability of a passenger surviving the sinking of the Titanic. 
ここで、私たちの3つのMLパイプラインを使用して構築した最初の例のMLシステムを紹介します。これは、最もよく知られたML問題の1つであるタイタニックの沈没から乗客が生存する確率を予測するものです。

The Titanic passenger survival data is a static dataset. 
タイタニックの乗客生存データは静的データセットです。

An ML model is trained and evaluated on the static dataset. 
MLモデルは静的データセットでトレーニングされ、評価されます。

That makes it a good introductory dataset for learning ML, as you skip the step of creating the training data. 
これにより、トレーニングデータを作成するステップをスキップできるため、MLを学ぶための良い入門データセットとなります。

But we want to move beyond the idea of just training models with a static data dump. 
しかし、私たちは単に静的データダンプでモデルをトレーニングするという考えを超えたいと考えています。

In Figure 2-10, we see the outline of our ML system in a kanban board, including its data sources, its final output (a dashboard), and the technologies used to implement our ML system. 
図2-10では、データソース、最終出力（ダッシュボード）、およびMLシステムを実装するために使用される技術を含む、カンバンボード上のMLシステムの概要を示しています。

_Figure 2-10. The MVPS kanban board for our Titanic passenger survival ML system._
_Figure 2-10. タイタニック乗客生存MLシステムのMVPSカンバンボード_

We will use the Titanic Survival dataset for historical data, as shown in Figure 2-11. 
図2-11に示すように、歴史的データにはタイタニック生存データセットを使用します。

_Figure 2-11. Our Titanic Survival dataset. The passenger_id column uniquely identifies each row—it is not a feature. We augmented the dataset with the datetime column—the original dataset has 891 rows with the date of the Titanic disaster, while each new (synthetic) row has the datetime of its creation._
_Figure 2-11. 私たちのタイタニック生存データセット。passenger_id列は各行を一意に識別します—これはフィーチャーではありません。私たちはdatetime列でデータセットを拡張しました—元のデータセットにはタイタニックの災害の日付を持つ891行があり、各新しい（合成）行にはその作成日時があります。_

We will then write a synthetic data creation function that creates new passengers for the Titanic. 
次に、タイタニックの新しい乗客を作成する合成データ作成関数を書きます。

The synthetic passenger feature values are drawn from the same distribution as the original dataset, so we will not have any problems with feature drift or any need to retrain our model. 
合成乗客のフィーチャー値は元のデータセットと同じ分布から引き出されるため、フィーチャードリフトの問題やモデルを再トレーニングする必要はありません。

It’s an overly simplified example but still a useful one for getting started with dynamic data. 
これは過度に単純化された例ですが、動的データを始めるためには依然として有用です。

We will write both the historic and new feature data to a single feature group in the Hopsworks feature store with a feature pipeline written in Python using Pandas. 
私たちは、Pandasを使用してPythonで書かれたフィーチャーパイプラインを使用して、歴史的データと新しいフィーチャーデータの両方をHopsworksフィーチャーストアの単一のフィーチャーグループに書き込みます。



We will write both the historic and new feature data to a single feature group in the Hopsworks feature store with a feature pipeline written in Python using Pandas. 
私たちは、Pythonを使用してPandasで書かれたフィーチャーパイプラインを使用して、Hopsworksフィーチャーストアの単一のフィーチャーグループに歴史的および新しいフィーチャーデータの両方を書き込みます。

We will then schedule the feature pipeline to run once per day, creating one new passenger for the Titanic for that day: 
次に、フィーチャーパイプラインを1日1回実行するようにスケジュールし、その日に対してTitanicの新しい乗客を1人作成します：

```   
import pandas as pd   
import hopsworks   
BACKFILL=True   

def get_new_synthetic_passenger():     
    # see github repo for details   

if BACKFILL==True:     
    df = pd.read_csv("titanic.csv")     
    # Remove columns that are not predictive of passenger survival   
else:     
    df = get_new_synthetic_passenger()   

fs = hopsworks.login().get_feature_store()   
fg = fs.get_or_create_feature_group(name="titanic", version=1, \     
    primary_keys=['id'], description="Titanic passengers")   
fg.insert(df)
``` 

Our training pipeline starts by selecting the features we want to use in our model and creating a feature view to represent the input features and output labels/targets for our model. 
私たちのトレーニングパイプラインは、モデルで使用したい特徴を選択し、入力特徴と出力ラベル/ターゲットを表すフィーチャービューを作成することから始まります。

We use the feature view to read training data, which is randomly split into 20% test set and 80% train set, from the Titanic passenger survival data. 
私たちはフィーチャービューを使用して、Titanicの乗客生存データからトレーニングデータを読み込みます。このデータはランダムに20％のテストセットと80％のトレーニングセットに分割されます。

We will then train the model with XGBoost, a gradient-boosted decision tree library in Python. 
次に、Pythonの勾配ブースト決定木ライブラリであるXGBoostを使用してモデルをトレーニングします。

Finally, we save our trained model to Hopsworks’ model registry: 
最後に、トレーニングしたモデルをHopsworksのモデルレジストリに保存します：

```   
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

We will write a batch inference pipeline that is scheduled to run once per day. 
私たちは、1日1回実行されるようにスケジュールされたバッチ推論パイプラインを書きます。

It will read any new synthetic passengers from the feature store, download our trained model from the model registry, use the model to predict whether the synthetic passengers survived or not, and log predictions with the feature view to the feature store: 
このパイプラインは、フィーチャーストアから新しい合成乗客を読み込み、モデルレジストリからトレーニング済みモデルをダウンロードし、モデルを使用して合成乗客が生存したかどうかを予測し、フィーチャービューを使用してフィーチャーストアに予測を記録します：

```   
retrieved_model = mr.get_model(name="titanic", version=1)   
saved_model_dir = retrieved_model.download()   
model = xgboost.XGBClassifier()   
model.load_model(saved_model_dir + "/model.json")   

row_data = # get row of features for new passenger   
prediction = model.predict(row_data)
```

This ML system solves what is called a counterfactual (what-if) prediction problem. 
このMLシステムは、反事実（what-if）予測問題と呼ばれるものを解決します。

What if there were a passenger who was male, was 49 years old, and traveled third class on the Titanic—what’s the probability he would have survived? 
もしTitanicに男性で49歳の乗客がいて、3等に乗っていたとしたら、彼が生存した確率はどれくらいでしょうか？

The full source code for this “Titanic passenger survival as an ML system” example is found in the book’s source code repository in GitHub. 
この「Titanic乗客生存をMLシステムとして」の例の完全なソースコードは、書籍のソースコードリポジトリのGitHubにあります。

It also includes an interactive UI written in Python using Gradio to ask the model what-if questions about passenger survival probabilities. 
また、乗客の生存確率に関するwhat-if質問をモデルに尋ねるために、Gradioを使用してPythonで書かれたインタラクティブなUIも含まれています。

To get started with this example, you will need to install the Hopsworks Python client library. 
この例を始めるには、Hopsworks Pythonクライアントライブラリをインストールする必要があります。

On Linux and Apple, this involves calling: 
LinuxおよびAppleでは、次のコマンドを実行します：

```   
pip install hopsworks[python]
``` 

In Windows, you first need to pip install the Twofish library, before you install the Hopsworks library. 
Windowsでは、最初にTwofishライブラリをpipでインストールし、その後Hopsworksライブラリをインストールする必要があります。

You will also need to create an account on Hopsworks Serverless, and you will also need to obtain a Hopsworks API key (User → Account → API) and save it to an .env file in the root of the course repository, so that you can securely read from and write to Hopsworks. 
また、Hopsworks Serverlessでアカウントを作成し、Hopsworks APIキー（ユーザー→アカウント→API）を取得して、コースリポジトリのルートにある.envファイルに保存する必要があります。これにより、Hopsworksから安全に読み書きできます。

You can run the first notebook and let it prompt you to create a Hopsworks API key, or you can follow the docs. 
最初のノートブックを実行して、Hopsworks APIキーを作成するように促されるか、ドキュメントに従うことができます。

Hopsworks offers a free forever serverless tier with 35 GB of free storage, which is more than enough to complete the projects in this book. 
Hopsworksは、35GBの無料ストレージを持つ永続的な無料サーバーレスプランを提供しており、これはこの本のプロジェクトを完了するのに十分です。

###### Summary 要約

When building AI systems, we start with the ML pipelines and the data transformations performed in the feature, training, and inference pipelines. 
AIシステムを構築する際、私たちはMLパイプラインとフィーチャー、トレーニング、推論パイプラインで行われるデータ変換から始めます。

We introduced a taxonomy for data transformations for ML pipelines based around reusable features (created by model-independent transformations in feature pipelines), model-specific features (created by model-dependent transformations in training/inference pipelines), and real-time features (created by on-demand transformations in online inference pipelines that can also be applied to historical data to create features in feature pipelines). 
私たちは、MLパイプラインのデータ変換の分類法を導入しました。これは、再利用可能な特徴（フィーチャーパイプラインでのモデル非依存の変換によって作成）、モデル特有の特徴（トレーニング/推論パイプラインでのモデル依存の変換によって作成）、およびリアルタイム特徴（オンライン推論パイプラインでのオンデマンド変換によって作成され、フィーチャーパイプラインでの特徴を作成するために歴史的データにも適用できる）に基づいています。

We closed out the chapter with our first ML system—a dynamic data version of the Titanic passenger survival prediction problem. 
私たちは、Titanic乗客生存予測問題の動的データバージョンである最初のMLシステムで章を締めくくりました。

We showed how to build both batch and interactive ML systems for Titanic passenger survival. 
私たちは、Titanic乗客生存のためのバッチおよびインタラクティブなMLシステムの構築方法を示しました。

In the next chapter, we will go one step further and you will build an AI system for your neighborhood or region. 
次の章では、さらに一歩進んで、あなたの近所や地域のためのAIシステムを構築します。

You will build an air quality prediction service for the neighborhood you live in, and we will use the same frameworks used in the Titanic example—Python, Pandas, XGBoost, and Gradio. 
あなたは、住んでいる近所のための空気質予測サービスを構築し、Titanicの例で使用されるのと同じフレームワーク—Python、Pandas、XGBoost、Gradioを使用します。



