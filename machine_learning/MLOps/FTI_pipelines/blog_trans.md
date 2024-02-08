## 0.1. link リンク

https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines
https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines

## 0.2. title タイトル

From MLOps to ML Systems with Feature/Training/Inference Pipelines
MLOpsから特徴/学習/推論パイプラインによるMLシステムへ

The Mental Map for MLOps to align your Data-ML-Product Teams
データ-ML-プロダクト・チームを調整するMLOpsのためのメンタル・マップ

## 0.3. abstract 抄録

Maps help us navigate the world, and communicate ideas, helping us get faster to our destination.
地図は私たちが世界をナビゲートし、アイデアを伝え、目的地により早く到達するのに役立つ。
Somewhere along the way, MLOps got lost in promoting “waterfall software architecture” maps for ML Systems that include a kitchen sink of requirements.
MLOpsは、MLシステムのための「ウォーターフォール・ソフトウェア・アーキテクチャ」マップを推進するうちに、いつの間にか、要求事項の台所の流し台のようなものを含むようになった。
Existing approaches to MLOps prevent teams from following DevOps principles of starting with a small working system and iteratively improving it.
MLOpsに対する既存のアプローチでは、チームは、小さな稼働中のシステムから始めてそれを反復的に改善するというDevOpsの原則に従うことができない。
In this article, we present a new mental map for ML Systems as three independent ML pipelines: feature pipelines, training pipelines, and inference pipelines that share a common storage layer for the ML artifacts they produce and consume (features, models).
本稿では、MLシステムの新しいメンタルマップを**3つの独立したMLパイプライン**として提示する： **特徴量パイプライン、学習パイプライン、推論パイプラインは、それぞれが生成・消費するML成果物（特徴、モデル）に対して共通のストレージレイヤーを共有する**。
In contrast to existing MLOps architectures, we provide a unified architecture that describes both batch ML systems and real-time ML systems.
既存のMLOpsアーキテクチャとは対照的に、我々は**バッチMLシステムとリアルタイムMLシステムの両方を記述する統一アーキテクチャ**を提供する。
This makes it easier for developers to move to/from batch and real-time systems, and provides clear interfaces between the ML pipelines, enabling easier collaboration between the data, ML, and product teams that work together to develop and operate ML systems.
これにより、開発者はバッチシステムとリアルタイムシステムの行き来が容易になり、MLパイプライン間の明確なインターフェイスが提供されるため、MLシステムの開発・運用に協力するデータチーム、MLチーム、製品チーム間のコラボレーションが容易になります。
Compared to existing MLOps architectures, the feature/training/inference pipeline architecture helps you get faster to a minimal working ML system that can be iteratively improved, while following best practices for automated testing, versioning, and monitoring.
既存のMLOpsアーキテクチャと比較して、**機能/トレーニング/推論のパイプラインアーキテクチャ**は、自動テスト、バージョニング、およびモニタリングのベストプラクティスに従いながら、iterativelyに改善できる最小限の実用的なMLシステムに迅速に到達するのに役立ちます。
There are now hundreds of ML systems that have been built by the community based on our architecture, showing that building and shipping ML systems is easier if you follow a mental map that starts with building pipelines rather than starting by building ML infrastructure.
私たちのアーキテクチャに基づいてコミュニティによって構築されたMLシステムは、現在数百にのぼります。これは、**MLインフラストラクチャの構築から始めるよりも、パイプラインの構築から始めるメンタルマップに従った方が、MLシステムの開発とデプロイが容易であることを示しています**。

# 1. Introduction はじめに

> “It's impressive how far you can go with contemporary tools like @modal_labs, @huggingface, and @hopsworks! In 2017, having a shared pipeline for training and prediction data that updated automatically and made models available as a UI and an API was a groundbreaking stack at Uber.
> 「@modal_labs、@huggingface、@hopsworksのような現代的なツールでどこまでできるかは印象的だ！2017年、自動的に更新され、モデルをUIとAPIとして利用可能にするトレーニングデータと予測データの共有パイプラインを持つことは、Uberにおける画期的なスタックだった。
> Now, it's a standard part of a well-done student project.” Charles Frye, Full Stack Deep Learning course leader.
> 今では、よくできた学生プロジェクトの標準的な部分です」。チャールズ・フライ、フルスタック・ディープラーニングコースリーダー。

In a course I gave at KTH in 2022/23, students developed a full ML system in only 2 weeks that solved a prediction problem for a novel non-static data source of their choice.
私が2022年から23年にかけてKTHで行ったコースでは、**[学生たちはわずか2週間で完全なMLシステムを開発](https://id2223kth.github.io/assignments/project/ServerlessMLProjectsID22232023.html)**し、自分たちが選んだ新しい非静的データソースの予測問題を解決した。
As Charles suggests in the above quote, leveraging ML infrastructure makes it easier to build ML systems.
チャールズが上記の引用で示唆しているように、MLインフラを活用することで、MLシステムの構築が容易になる。
You can write a Python program that scrapes data from the Internet and, with a few annotations, runs on a daily schedule with Modal.
インターネットからデータをスクレイピングするPythonプログラムを書いて、いくつかのannotationを加えれば、Modalを使って毎日のスケジュールで実行することができる。
The program can write the features it computes as DataFrames to Hopsworks Feature Store.
プログラムは、計算したフィーチャーをDataFramesとしてHopsworks [Feature Store](https://www.hopsworks.ai/dictionary/feature-store)に書き込むことができます。
From there, a notebook can be used to train a model that is saved in Hopsworks (or any [model registry](https://www.hopsworks.ai/dictionary/model-registry)).
(model registry = モデルやモデルに関連するartifactsを保存するバージョン管理システム)
そこからノートブックを使って、Hopsworks（または任意のモデル登録）に保存されたモデルをトレーニングすることができる。
And, finally, a third Python program uses the trained model to make predictions with new inference data (for example, the data scraped today) read from the Feature Store, and displays the predictions in a nice UI or Dashboard (e.g., written in the Streamlit or Taipy).
そして最後に、3つ目のPythonプログラムが、Feature Storeから読み込んだ新しい[推論データ](https://www.hopsworks.ai/dictionary/inference-data)（ex. 今日スクレイピングされたデータ）を使って予測を行うために学習済みモデルを使用し、（StreamlitやTaipyで書かれた）素敵なUIやダッシュボードに予測を表示する。
Some examples of prediction problems were predicting air quality, water levels, snow depth, football scores, electricity demand, and sentiment for posts.
予測問題の例としては、大気の質、水位、雪の深さ、サッカーの得点、電力需要、投稿の感情などを予測するものがあった。

![figure1]()

Figure 1: Feature Pipelines, Training Pipelines, Inference Pipelines are the independent ML Pipelines that together make up a ML System.

But in my course analysis, the conclusion I drew was that the key reason why students could go from zero to a working ML system in less than 2 weeks was not just the new frameworks.
しかし、私のコース分析で導き出された結論は、学生たちが2週間足らずでゼロからMLシステムを使えるようになった主な理由は、新しいフレームワークだけではないということだった。
It was, more importantly, the clear mental map of what they needed to do (see Figure 1):
さらに重要なのは、彼らが**何をすべきかという明確なメンタルマップ**だった(図1参照)

- build a feature pipeline to continually create features from your novel data source, save those features as a DataFrame to Hopsworks Feature Store; **新規データソースから継続的にフィーチャーを作成するフィーチャーパイプラインを構築**し、フィーチャーをDataFrameとしてHopsworksフィーチャーストアに保存します;

- write a training pipeline that reads training data from the Feature Store, trains your model and saves the trained model in the model registry, トレーニングパイプラインを作成し、Feature Storeからトレーニングデータを読み込み、モデルをトレーニングし、**トレーニング済みモデルをモデルレジストリに保存します**、

- write a batch inference pipeline or online inference pipeline that downloads the trained model, then takes new feature data, either from the feature store or computes it from user requests, and makes predictions consumed by the ML-enabled product (often a simple UI written in Python using Streamlit or Gradio). **バッチ推論パイプラインまたはオンライン推論パイプラインを作成**し、学習済みモデルをダウンロードし、新しい特徴量データを特徴ストアから取得するか、ユーザリクエストから計算し、ML対応プロダクト（多くの場合、StreamlitまたはGradioを使用してPythonで書かれたシンプルなUI）で消費される予測を行います。

After the students have built their first MVP (Minimum Viable Product), they could add automated unit tests for features, data validation tests, and versioning for their features and models.
生徒たちは最初の**MVP(Minimum Viable Product)**を作った後、特徴量(作成処理)の自動ユニットテスト、データ検証テスト、特徴量やモデルのバージョニングを追加することができる。
That is, they could easily follow best practices for MLOps.
つまり、**MLOpsのベストプラクティスに簡単に従うことができる**のだ。

![figure2]()
Figure 2: Feature Pipelines, Training Pipelines, and Inference Pipelines are all examples of ML Pipelines. Note ML Pipelines now describes an abstract grouping, not a concrete pipeline.
Feature pipelines、Training pipelines、Inference pipelinesはすべてML pipelines の例です。ML pipelines は、具体的なパイプラインではなく、抽象的なグループ(=独立したpipelineの集合?)を表すようになりました。

However, even with recent advances in MLOps tooling, many teams are failing in getting models to production.
しかし、最近のMLOpsツールの進歩にもかかわらず、多くのチームがモデルをproductionに移すことに失敗している。
According to Gartner, between 2020 and 2022, companies only increased the percentage of models that make it from prototype to production from 53% to 54%.
ガートナーによると、2020年から2022年にかけて、プロトタイプから製品化されるモデルの割合が53％から54％に増加するだけだという。
Tooling will only get you so far, if you don’t have good processes for how to get there.
ツールは、そこに到達するための良いプロセスを持っていなければ、そこまでしか到達できない。
As such, this starts with a brief, idiosyncratic historical overview of ML systems and MLOps, a critique of current “best practices”, and then we present our **FTI (feature/training/inference) pipeline architecture** for ML systems and its advantages over current approaches.
そのため、MLシステムとMLOpsの簡単で特異な歴史的概観、現在の「ベストプラクティス」の批評から始まり、MLシステムのための我々の**FTI(feature/training/inference)パイプラインアーキテクチャ**と、現在のアプローチに対する優位性を紹介する。

# 2. Pre-MLOps - Move fast and ship it プレMLOPS - 迅速な行動と出荷

In the early days of ML Systems, it quickly became common knowledge that building ML systems was much more than just training a model.
MLシステムの黎明期には、MLシステムの構築は単にモデルをトレーニングする以上のものであることはすぐに常識となった。

![](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502ad4eb9b805fbe60281f4_figure%203_lightbox.png)
Figure 3: This diagram from 2015 is from a canonical paper by Google on Hidden Technical Debt in Machine Learning Systems. [Image Source]
図3：この図は2015年のGoogleの機械学習システムにおける隠れた技術的負債に関する権威ある論文からのものです。[画像ソース]

(あ、よく引用されてる図だ!:thinking:)

The diagram in Figure 3 spread fast and wide and the message was clear to Data Scientists - building ML systems is hard and much more than just training a model.
図3の図は瞬く間に広まり、データサイエンティストへのメッセージは明確なものとなった。**MLシステムの構築は難しく、単にモデルをトレーニングするだけでは済まない**。

In the era before MLOps practices merged, the first generation of ML systems many different architecture patterns were proposed to help build batch and real-time ML systems.
MLOpsのプラクティスが融合(一般化?)する前の時代、MLシステムの第一世代では、バッチおよびリアルタイムのMLシステムを構築するのに役立つ[多くの異なるアーキテクチャパターン](https://www.oreilly.com/library/view/machine-learning-design/9781098115777/)が提案された。(ふむふむ...!)

Broadly speaking, there are two types of ML systems: batch ML systems and real-time ML systems.
大まかに言って、MLシステムには2つのタイプがある： **バッチMLシステムとリアルタイムMLシステム**である。
An example of a batch ML system would be Spotify weekly.
バッチMLシステムの例としては、Spotify weeklyがある。
It produces predictions for every user once per week on what songs to recommend to each user.
週に一度、各ユーザにどんな曲を推薦するかの予測を作成する。
The results are stored in a key-value store, and when you login to Spotify, it downloads the predictions to your client and shows you the recommendations.
結果はkey-valueストアに保存され、Spotifyにログインすると、予測がクライアントにダウンロードされ、おすすめが表示される。
An example of a real-time ML system would be TikTok.
リアルタイムMLシステムの例としては、TikTokがある。
Every click or swipe you make is used to compute features in near real-time about your user history and context (e.g., what’s trending) that are, in turn, used to personalize recommendations for upcoming videos.
あなたがクリックやスワイプをするたびに、あなたのユーザ履歴とコンテキスト(例えば、何がトレンドか)について、ほぼリアルタイムで特徴量を計算するために使用されます。

![](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502ad7d387cfe977467717b_figure%204_lightbox.png)

In figure 4, you can see a quick-and-dirty batch ML system.
図4は、バッチMLシステムである。
This anti-pattern is for a production batch ML system that runs on a schedule to make predictions that are consumed by some prediction consumer, such as a dashboard or an operational system.
このアンチパターンは、ダッシュボードや業務システムのような予測コンシューマによって消費される予測を行うために、スケジュールに基づいて実行されるバッチMLシステムのためのものである。
The pattern solves one problem - it ensures consistent features for training and inference by including training and inference in the same program.
このパターンは、ある問題を解決する。つまり、トレーニングと推論を同じプログラムに含めることで、トレーニングと推論の一貫した特徴量を保証するのだ。
You run the program with a boolean flag that decides whether it runs in TRAIN or INFERENCE mode.
**TRAIN モードで実行するか INFERENCE モードで実行するかを決定するbooleanフラグ**でプログラムを実行する。
However, features created here are not easily reused in other models and there is very little modularity - if data volumes increase beyond what your Python program can process, you can’t easily switch to PySpark.
しかし、ここで作成された特徴量は他のモデルで簡単に再利用できないし、モジュール性もほとんどない。Pythonプログラムで処理できる量を超えてデータ量が増えても、簡単にPySparkに切り替えることはできない。

![fig5]()

Figure 5: A real-time ML system requires separate offline training and online inference pipelines.
図5：リアルタイムMLシステムには、オフラインのトレーニングとオンラインの推論パイプラインが別々に必要です。

In figure 5, you can see an operational ML system that receives requests from clients and responds with predictions in real-time.
図5では、クライアントからのリクエストを受け、リアルタイムで予測結果を返すMLシステムが運用されているのがわかる。
This is a very different architecture from our previous batch ML system, which makes it challenging for developers to move from batch to real-time systems.
これは、以前のバッチMLシステムとは全く異なるアーキテクチャであり、開発者にとってバッチからリアルタイムシステムへの移行は困難である。
There are also new challenges here.
ここにも新たな挑戦がある。
Now, you need two separate systems - an offline training pipeline, and an online model serving service.
オフラインのトレーニングパイプラインと、オンラインのモデル提供サービスだ。
You can no longer ensure consistent features between training and serving by having a single monolithic program.
単一の一枚岩のプログラムでは、もはやトレーニングからサーブまで一貫した特徴量を確保することはできない。(これも問題は、Trainingパイプラインに特徴量作成を含めてしまってるからかな)
One solution is to version the feature creation source code and ensure both training and serving use the same version.
一つの解決策は、特徴量作成のソースコードをバージョン管理し、トレーニングとサービングの両方が同じバージョンを使用するようにすることである。
In this architecture, the features in the online inference pipeline are computed using data provided by the request - the models have no access to history or context, all state used to create features should come in the request.
このアーキテクチャでは、オンライン推論パイプラインの特徴量は、リクエストによって提供されるデータを使って計算される。
An example of such a system would be a LLM chatbot.
このようなシステムの例としては、LLMチャットボットがある。
The user provides a query and the LLM provides a response, with the online inference pipeline tokenizing the input text.
オンライン推論パイプラインが入力テキストをトークン化する。

![figure6]()

Figure 6: Many real-time ML systems also require history and context, and the feature store provides them as precomputed features to online models. This now requires three separate pipelines - feature creation, model training, and online model inference.
図6：多くのリアルタイムMLシステムは、履歴とコンテキストも必要とするが、特徴ストアはそれらをオンラインモデルに事前計算された特徴として提供する。このため、特徴作成、モデル学習、オンラインモデル推論の3つの独立したパイプラインが必要になる。

In our first real-time ML system, the online inference pipeline was stateless - it had no access to historical data or context data.
私たちの最初のリアルタイムMLシステムでは、オンライン推論パイプラインはステートレスだった。ユーザ履歴やconxtextにアクセスしない。
Figure 6 shows the architecture of a real-time ML System with the feature store providing history and context, enabling richer feature vectors for models.
図6は、特徴量ストアが履歴とコンテキストを提供し、モデルのためのより豊富な特徴量ベクトルを可能にするリアルタイムMLシステムのアーキテクチャを示している。
The feature store provides low-latency access to pre-computed features (historical and contextual information) by the online inference pipeline looking features up with entity IDs (userID, sessionID, productID, etc) provided by the client at request-time.
**特徴量ストア**は、オンライン推論パイプラインがリクエスト時にクライアントから提供されたエンティティID(userID、sessionID、productIDなど)を使って特徴量を検索することで、事前に計算された特徴量(履歴情報とコンテキスト情報)への低レイテンシーアクセスを提供する。

At this point, we have introduced 3 different architectures for building production ML systems.
ここまで、プロダクションMLシステムを構築するための3つの異なるアーキテクチャを紹介してきた。
The challenge for ML platform teams has been how to easily communicate these architectural patterns to the data/ML/ops/product teams who collaborate to build production ML systems.
MLプラットフォームチームにとっての課題は、本番MLシステムを共同で構築するデータ/ML/運用/製品チームに、これらのアーキテクチャパターンをいかに簡単に伝えるかである。

# 3. The Kitchen-Sink Mental Maps for MLOps MLOpsのための「キッチンシンク・メンタルマップ

In 2020, the term MLOps came to be adopted as the set of patterns and processes that ML platforms teams should use to productionize ML systems.
2020年には、MLプラットフォームチームがMLシステムをプロダクション化するために使用すべき一連のパターンとプロセスとして、MLOpsという用語が採用されるようになった。
MLOps was inspired by the DevOps movement which brought software engineers closer to production by ensuring that they automate and test the deployment of their software in production environments.
MLOpsはDevOpsムーブメントに触発されたものである。DevOpsムーブメントは、本番環境でのソフトウェアのデプロイを自動化し、テストすることで、ソフトウェア・エンジニアがより本番環境に近づけるようにした。
Wouldn’t it be great if we could do the same for ML systems? However, ML systems are more complex than classical software products - they have to manage both the code used to build them and the data used for training and inference.
MLシステムでも同じことができれば素晴らしいと思わないだろうか？しかし、**MLシステムは古典的なソフトウェア製品よりも複雑**で、構築するために使われるコードと、学習や推論に使われるデータの**両方を管理しなければならない**。
Our nascent MLOps Community badly needed some guidance on best practices and processes for teams - we needed a map to build ML systems.
私たちの新興MLOpsコミュニティは、チームのベストプラクティスとプロセスに関するガイダンスをひどく必要としていた。

There is a long history of bad maps leading people astray.
悪い地図が人々を迷わせた長い歴史がある。

![figure7]()
Figure 7: Mercator Projection Maps make Greenland look much bigger than it is. Mercator Projection Maps suck.

Personally, since a very young age, I have had an unreasonable dislike for Mercator Projection maps (see figure 7).
個人的には、幼い頃からメルカトル図法(図7参照)の地図が理不尽に嫌いだった。

The first MLOps maps for building ML systems have similar deficiencies to Mercator Maps - they try to project a view of ML systems that doesn’t reflect the reality of building a ML system.
**MLシステム構築のための最初のMLOpsマップには、メルカトル図法のような欠陥がある。MLシステム構築の現実を反映していないMLシステムの見方を投影しようとしているのだ**。
The maps are a kitchen sink of requirements collected by consultants from all the different stakeholders and thrown unthinkingly into one huge diagram.
マップは、コンサルタントがさまざまな利害関係者から集めた要求の台所の流しであり、1つの巨大な図に無造作に投げ込まれている。

![figure8]()
Figure 8: Google’s MLOps Map to help you build ML Systems [Source]

As you can, Google started by asking the operations teams - who said they needed separate dev and prod environments.
お分かりのように、グーグルはまず運用チームに尋ねた。彼らは開発環境とプロダクション環境を分ける必要があると言った。
The data teams wanted clean data.
データチームはクリーンなデータを求めていた。
The ML teams want hyperparameter tuning and models to be validated.
MLチームは、ハイパーパラメーターのチューニングとモデルの検証を望んでいる。
The product teams got forgotten in this MLOps map.
このMLOpsマップでは、製品チームは忘れ去られている。

![figure9]()
Figure 9: Databricks MLOps map to build ML Systems [Source]

Databricks, however, were not to be outdone.
しかし、データブリックも負けてはいなかった。
Google forgot a staging environment! But where is the mythical ML pipeline here? There are no names for the pipelines, no easy way to build your first ML system in a couple of weeks.
グーグルはステージング環境を忘れていた！しかし、神話のようなMLパイプラインはどこにあるのだろうか？パイプラインの名前もないし、最初のMLシステムを数週間で構築する簡単な方法もない。
The barrier to entry is too high - only a very few people have the software engineering, operations, and data science knowledge to navigate these maps.
参入障壁が高すぎるのだ。ソフトウェアエンジニアリング、オペレーション、データサイエンスの知識を持ち、これらのマップをナビゲートできるのは、ごく少数の人間だけである。
For other mortals - Data Scientists, Data Engineers, ML Engineers - the maps might as well be a riddle for finding buried treasure.
データ・サイエンティスト、データ・エンジニア、MLエンジニアといった他の人間にとって、地図は埋もれた宝を見つけるための謎解きのようなものかもしれない。

![figure10](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502aeb3d68f1808344bea82_figure%2010_lightbox.png)
Figure 10: ML Systems are fed new data with pipelines enabling them to continually drive business value.
図10: MLシステムは、ビジネス価値を継続的に生み出すために、パイプラインを使って新しいデータを供給される。

Let’s take a step back and examine the problem of making ML systems from first principles.
一歩引いて、**第一原理からMLシステムを作る問題**を検証してみよう。
We will skip static datasets where you only make one-off predictions on a static dataset - this is not a ML System.
**静的なデータセットで1回きりの予測だけを行うような静的なデータセットはスキップします - これはMLシステムではありません。**(うんうん...!:thinking:)

Firstly, a ML System uses a trained ML model to make predictions on new data to solve a “prediction problem” of interest.
まず第一に、MLシステムは、興味のある「予測問題」を解決するために、新しいデータに対して予測を行うために学習されたMLモデルを使用する。
That new data and the historical data for training is fed by pipelines.
その新しいデータとトレーニングのための過去のデータは、パイプラインによって供給される。
Pipelines continually feed data to models to enable ML Systems to make predictions on new data, and to collect training data.
パイプラインは、MLシステムが新しいデータに対して予測を行い、トレーニングデータを収集できるように、**継続的にデータをモデルに供給する**。
Pipelines also enable automation - to retrain models, to monitor model performance, to log data for debugging.
パイプラインはまた、モデルの再トレーニング、**モデルのパフォーマンスの監視**、デバッグのためのデータログなどの自動化を可能にする。

Batch pipelines enable both batch ML Systems, such as dashboards, and operational ML systems, such as Spotify weekly, where recommendations for songs are updated once per week and consumed by the user when they login to Spotify.
batchパイプラインは、ダッシュボードのようなバッチMLシステムと、Spotify weeklyのような運用MLシステムの両方を可能にする。
Streaming feature pipelines and features computed at request-time (on-demand features) enable interactive ML systems that are updated in real-time, enabling systems such as personalized recommendations or search.
streaming feature pipelines とリクエスト時に計算される特徴量(=on-demand features)は、リアルタイムで更新されるinteractiveなMLシステムを可能にし、パーソナライズされた推薦や検索などのシステムを実現する。

# 4. Unified Architecture for ML Systems as Feature/Training/Inference Pipelines 特徴／学習／推論パイプラインとしてのMLシステムの統一アーキテクチャ

There is, however, an easier mental map that can help you build ML systems.
しかし、MLシステムの構築に役立つ、もっと簡単なメンタルマップがある。
This architectural pattern has been used to build hundreds of ML systems by ordinary developers (here, here, here, and here).
このアーキテクチャ・パターンは、一般の開発者が何百ものMLシステムを構築するのに使われてきた(ここ、ここ、ここ、そしてここ)。
The pattern is as follows: a ML system consists of three independently developed and operated ML pipelines:
そのパターンは以下の通りである： MLシステムは、**独立に開発・運用される3つのMLパイプラインから構成される**：

- a feature pipeline that takes as input raw data that it transforms into features (and labels)
  生データを入力として特徴（とラベル）に変換する特徴パイプライン

- a training pipeline that takes as input features (and labels) and outputs a trained model, and
  特徴（およびラベル）を入力とし、学習済みモデルを出力する学習パイプラインと

- an inference pipeline that takes new feature data and a trained model and makes predictions.
  新しい特徴データと学習済みモデルを受け取り、予測を行う推論パイプライン。

In this FTI (feature, training, inference) architecture, there is no single ML pipeline.
このFTI(特徴量、トレーニング、推論)アーキテクチャでは、単一のMLパイプラインは存在しない。
The confusion about what the ML pipeline does (does it feature engineer and train models or also do inference or just one of those?) disappears.
**MLパイプラインが何をするのかについての混乱はなくなる**。（フィーチャーエンジニアリングとモデルの訓練なのか、推論もするのか、それともどちらか一方だけなのか）
The FTI map is the same for both batch ML systems and real-time ML systems.
**FTIマップはバッチMLシステムでもリアルタイムMLシステムでも同じである。**

![figure11](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502aeee69553d37d6d1197a_figure%2011_lightbox.png)

The feature pipeline can be a batch program or a streaming program.
フィーチャー・パイプラインは、バッチ・プログラムでもストリーミング・プログラムでもよい。(うんうん...!)
The training pipeline can output anything from a simple XGBoost model to a fine-tuned large-language model (LLM), trained on many GPUs.
トレーニング・パイプラインは、単純なXGBoostモデルから、多数のGPUでトレーニングされた、微調整された大規模言語モデル（LLM）まで、何でも出力することができる。
Finally, the inference pipeline can be a batch program that produces a batch of predictions to an online service that takes requests from clients and returns predictions in real-time.
最後に、推論パイプラインは、クライアントからのリクエストを受けてリアルタイムで予測を返すオンラインサービス、もしくは予測のバッチを生成するバッチプログラムとすることができる。

![figure12]()
Figure 12: Choose the best language/framework for your ML pipelines.
図12：MLパイプラインに最適な言語/フレームワークを選択する。

One major advantage of FTI pipelines is it is an open architecture.
**FTIパイプラインの大きな利点は、オープン・アーキテクチャ**であることだ。(とは??)
You can use Python, Java or SQL.
Python、Java、SQLを使うことができる。
If you need to do feature engineering on large volumes of data, you can use Spark or DBT or Beam.
大量のデータに対してフィーチャーエンジニアリングを行う必要がある場合は、SparkやDBT、Beamを使うことができる。
Training will typically be in Python using some ML framework, and batch inference could be in Python or Spark, depending on your data volumes.
トレーニングは通常、何らかのMLフレームワークを使ってPythonで行い、バッチ推論はデータ量に応じてPythonかSparkで行う。
Online inference pipelines are, however, nearly always in Python as models are typically training with Python.
しかし、オンライン推論パイプラインは、モデルの学習が通常Pythonで行われるため、ほぼ常にPythonで行われる。

![figure13]()
Figure 13: Pick the best framework for your feature pipeline based on your requirements. If you have small data to process, Pandas may be fine, but when data volumes exceed what a single node can process, you may move to PySpark. If you need “fresh” features, use a stream processing engine.
図13：要件に基づいて特徴量パイプラインに最適なフレームワークを選択する。データ処理するのが小さい場合はPandasでも問題ないかもしれませんが、データ量が単一ノードで処理できる量を超えると、PySparkに移行するかもしれません。新鮮な特徴が必要な場合は、ストリーム処理エンジンを使用します。

In figure 13, we can see the value of pluggable feature pipelines.
図13を見ると、pluggableな(i.e. 自由に着脱や拡張が可能な??)フィーチャー・パイプラインの価値がわかる。
For a given feature ingestion problem, you can easily pick the best framework, depending on the size of the data that will be ingested in a pipeline run and the freshness requirements for the feature data created - use streaming or on-demand features if you need very fresh (near real-time) feature data.
あるフィーチャインジェストの問題に対して、パイプライン実行でインジェストされるデータのサイズと、作成されるフィーチャデータの鮮度要件に応じて、最適なフレームワークを簡単に選択できます。

![figure14]()
Figure 14: Choose the best orchestrator for your ML pipeline/service.
図14：MLパイプライン/サービスに最適なorcheestratorを選択する。

The FTI pipelines are also modular and there is a clear interface between the different stages.
FTIパイプラインはモジュール化されており、**異なるステージ間には明確なインターフェイスがある**。(=ポートアンドアダプター...!)
Each FTI pipeline can be operated independently.
それぞれのFTIパイプラインは独立して操作できる。
Compared to the monolithic ML pipeline, different teams can now be responsible for developing and operating each pipeline.
**モノリシックなMLパイプラインに比べて、異なるチームがそれぞれのパイプラインの開発と運用を担当できるようになった**。
The impact of this is that for orchestration, for example, one team could use one orchestrator for a feature pipeline and a different team could use a different orchestrator for the batch inference pipeline.
この影響は、例えばorchestrationの場合、あるチームがフィーチャーパイプラインに1つのorchestratorを使い、別のチームがバッチ推論パイプラインに別のorchestratorを使うことができるということです。
(orchestrator = 複数のcomponentやserviceが連動して動作するシステムやアプリケーションにおいて、それらの部品の実行順序や相互作用を自動で管理・調整する役割を担うもの。)
Alternatively, you could use the same orchestrator for the three different FTI pipelines for a batch ML system.
あるいは、バッチMLシステムの3つの異なるFTIパイプラインに同じオーケストレーターを使うこともできる。
Some examples of orchestrators that can be used in ML systems include general-purpose, feature-rich orchestrators, such as Airflow, or lightweight orchestrators, such as Modal, or managed orchestrators offered by feature platforms.
MLシステムで使用可能なorchesratorの例としては、Airflowのような汎用性が高く機能が豊富なorchesrator、Modalのような軽量なorchesrator、特徴量プラットフォームが提供する管理されたorchesratorなどがあります。

Some of our FTI pipelines, however, will not need orchestration.
しかし、FTIパイプラインの中には、orchestrationを必要としないものもある。
Training pipelines can be run on-demand, when a new model is needed.
トレーニングパイプラインは、新しいモデルが必要なときにオンデマンドで実行できる。
Streaming feature pipelines and online inference pipelines run continuously as services, and do not require orchestration.
ストリーミング・フィーチャー・パイプラインとオンライン推論パイプラインは**サービスとして継続的に実行され**、オーケストレーションは必要ない。(batch処理の自動化とかは必要ないけど、サーバの台数増やしたりとかもorchestoratorの役割に含まれるのでは??)
Flink, Spark Streaming, and Beam are run as services on platforms such as Kubernetes, Databricks, or Hopsworks.
Flink、Spark Streaming、Beamは、Kubernetes、Databricks、Hopsworksなどのプラットフォーム上でサービスとして実行される。
Online inference pipelines are deployed with their model on model serving platforms, such as KServe (Hopsworks), Seldon, Sagemaker, and Ray.
オンライン推論パイプラインは、KServe（Hopsworks）、Seldon、Sagemaker、Rayなどのモデル提供プラットフォーム上にモデルとともに展開される。
The main takeaway here is that the ML pipelines are modular with clear interfaces, enabling you to choose the best technology for running your FTI pipelines.
ここでの主なポイントは、**MLパイプライン達は明確なインターフェイスを備えたモジュラーなものであり、FTIパイプラインの実行に最適なテクノロジーを選択できるということ**です。
(モジュラー性が高いよ!)

![figure15]()
Figure 15: Connect your ML pipelines with a Feature Store and Model Registry

Finally, we show how we connect our FTI pipelines together with a stateful layer to store the ML artifacts - features, training/test data, and models.
最後に、FTIパイプラインを、MLの成果物（特徴、トレーニング／テストデータ、モデル）を保存する**ステートフルレイヤー(=保存先?)とどのように接続するか**を示します。
Feature pipelines store their output, features, as DataFrames in the feature store.
フィーチャー・パイプラインは、その出力であるフィーチャーをDataFramesとして**フィーチャーストアに保存**する。
Incremental tables store each new update/append/delete as separate commits using a table format (we use Apache Hudi in Hopsworks).
インクリメンタルテーブルは、各新規更新/追加/削除を、テーブルフォーマットを使って別々のコミットとして保存する（HopsworksではApache Hudiを使っている）。
Training pipelines read point-in-time consistent snapshots of training data from Hopsworks to train models with and output the trained model to a model registry.
トレーニングパイプラインは、Hopsworksからポイントインタイムで一貫性のあるトレーニングデータのスナップショットを読み込んでモデルをトレーニングし、トレーニング済みモデルを**モデルレジストリ**に出力する。
You can include your favorite model registry here, but we are biased towards Hopsworks’ model registry.
ここにお好きなモデル登録を入れることができますが、私たちはホップワークスのモデル登録に偏っています。
Batch inference pipelines also read point-in-time consistent snapshots of inference data from the feature store, and produce predictions by applying the model to the inference data.
バッチ推論パイプラインはまた、特徴ストアから推論データのポイント・イン・タイム一貫性のあるスナップショットを読み込み、推論データにモデルを適用して予測を生成する。
Online inference pipelines compute on-demand features and read precomputed features from the feature store to build feature vectors that are used to make predictions in response to requests by online applications/services.
オンライン推論パイプラインは、オンデマンド特徴量を計算し、特徴量ストアから事前計算された特徴量を読み出して特徴ベクトルを構築し、オンラインアプリケーション/サービスからの要求に応じて予測を行う。

## 4.1. A Zoomable Map ズーム可能な地図

As with any good map, the FTI pipelines architecture hides complexity at a high level, but allows you to zoom in on any part of the map to discover important implementation details.
優れたマップと同様に、**FTIパイプライン・アーキテクチャは複雑さを高いレベルで隠し**ますが、マップのどの部分にもズームインして重要な実装の詳細を発見することができます。
Here, we enumerate some of the important questions on implementing the different pipelines that can be handled internally within the team implementing the pipeline.
ここでは、さまざまなパイプラインの実装に関する重要な質問のうち、パイプラインを実装するチーム内で処理できるものを列挙する。
In contrast, the MLOps 1.0 mental maps leaked all concepts across all teams making it hard for teams to know where their responsibilities started and ended as part of a very complex bigger picture.
対照的に、MLOps 1.0のメンタルマップでは、**すべてのチームにわたってすべての概念が漏れていたため**(=つまりモジュラー性が低くて、凝集度も低かった??)、非常に複雑な全体像の一部として、自分たちの責任の始まりと終わりがどこにあるのかをチームが把握するのが困難だった。

## 4.2. Feature Pipelines フィーチャー・パイプライン

Feature pipelines read data from data sources, compute features and ingest them to the feature store.
フィーチャー・パイプラインは、データ・ソースからデータを読み込み、フィーチャーを計算し、フィーチャー・ストアにインジェストする。
Some of the questions that need to be answered for any given feature pipeline include:
あるフィーチャー・パイプラインについて答えなければならない質問には、次のようなものがある：

- Is the feature pipeline batch or streaming?
  フィーチャーパイプラインはバッチかストリーミングか？

- Are feature ingestions incremental or full-load operations?
  フィーチャー・インジェストはインクリメンタルなのか、フルロードなのか？

- What framework/language is used to implement the feature pipeline?
  フィーチャー・パイプラインの実装には、どのようなフレームワーク／言語が使われていますか？

- Is there data validation performed on the feature data before ingestion?
  インジェストの前に、フィーチャーデータに対してデータバリデーションが行われているか。

- What orchestrator is used to schedule the feature pipeline?
  フィーチャー・パイプラインのスケジューリングには、どのオーケストレーターが使われていますか？(digdagとか??)

- If some features have already been computed by an upstream system (e.g., a data warehouse), how do you prevent duplicating that data, and only read those features when creating training or batch inference data?
  上流のシステム（データウェアハウスなど）ですでに計算済みの特徴量がある場合、そのデータの重複を防ぎ、トレーニングデータやバッチ推論データを作成する際に、それらの特徴量だけを読み込むにはどうすればよいでしょうか？

## 4.3. Training Pipelines トレーニングパイプライン

In training pipelines some of the details that can be discovered on double-clicking are:
トレーニングパイプラインでは、ダブルクリックで発見できる詳細がいくつかある：

- What framework/language is used to implement the training pipeline?
  トレーニングパイプラインの実装には、どのようなフレームワーク／言語が使用されていますか？

- What experiment tracking platform is used?
  どのような実験追跡プラットフォームを使用しているのか？

- Is the training pipeline run on a schedule (if so, what orchestrator is used), or is it run on-demand (e.g., in response to performance degradation of a model)?
  トレーニングパイプラインはスケジュールで実行されるのか（実行される場合、どのようなオーケストレーターが使用されるのか）、それともオンデマンドで実行されるのか（モデルのパフォーマンス低下に対応するなど）。

- Are GPUs needed for training? If yes, how are they allocated to training pipelines?
  トレーニングにGPUは必要ですか？必要な場合、トレーニングパイプラインにどのように割り当てますか？

- What feature encoding/scaling is done on which features? (We typically store feature data unencoded in the feature store, so that it can be used for EDA (exploratory data analysis).
  どのフィーチャーに対して、どのようなフィーチャーエンコーディング/スケーリングが行われるのか？(EDA(探索的データ分析)に使用できるように、通常、特徴データはエンコードされずに特徴ストアに保存されます。
  Encoding/scaling is performed in a consistent manner training and inference pipelines).
  エンコード/スケーリングは、一貫した方法で行われる トレーニングと推論パイプライン）。
  Examples of feature encoding techniques include scikit-learn pipelines or declarative transformations in feature views (Hopsworks).
  特徴エンコーディング技術の例としては、scikit-learnパイプラインや特徴ビューの宣言的変換（Hopsworks）などがある。

- What model evaluation and validation process is used?
  どのようなモデル評価・検証プロセスを用いているのか？

- What model registry is used to store the trained models?
  学習済みモデルの保存には、どのようなモデルレジストリを使用するのですか？(S3でOK??)

## 4.4. Inference Pipelines 推論パイプライン

Inference pipelines are as diverse as the applications they AI-enable.
推論パイプラインは、AIを可能にするアプリケーションと同様に多様である。
In inference pipelines, some of the details that can be discovered on double-clicking are:
推論パイプラインでは、ダブルクリックで発見できる(=簡単ってこと?)詳細がいくつかある：

- What is the prediction consumer - is it a dashboard, online application - and how does it consume predictions?
  予測消費者とは何か、それはダッシュボードなのか、オンライン・アプリケーションなのか、そしてどのように予測を消費するのか。

- Is it a batch or online inference pipeline?
  推論パイプラインはバッチかオンラインか？

- What type of feature encoding/scaling is done on which features?
  どのフィーチャーに対して、どのようなフィーチャーエンコーディング／スケーリングが行われるのか？

- For batch inference pipelines: what framework/language is used? What orchestrator is used to run it on a schedule? What sink is used to consume the predictions produced?
  バッチ推論パイプラインの場合、どのようなフレームワーク／言語が使われているか？それをスケジュールで実行するために、どのオーケストレーターが使われるか？生成された予測を消費するためにどのようなシンクが使われるか？

- For online inference pipelines: what model serving server is used to host the deployed model? How is the online inference pipeline implemented - as a predictor class or with a separate transformer step? Are GPUs needed for inference? Is there a SLA (service-level agreements) for how long it takes to respond to prediction requests?
  オンライン推論パイプラインの場合、デプロイされたモデルをホストするために、どのようなモデル・サービング・サーバーを使用しますか？オンライン推論パイプラインはどのように実装されますか？推論にGPUは必要か？予測リクエストに応答するのにかかる時間に関するSLA（サービス・レベル・アグリーメント）はありますか？

# 5. What are the fundamental principles of MLOps? MLOpsの基本原則とは？

The existing mantra is that MLOps is about automating continuous integration (CI), continuous delivery (CD), and continuous training (CT) for ML systems.
既存のマントラでは、**MLOpsはMLシステムの継続的インテグレーション（CI）、継続的デリバリー（CD）、継続的トレーニング（CT）を自動化すること**だとされている。
But that is too abstract for many developers.
しかし、多くの開発者にとっては抽象的すぎる。
MLOps is really about continual development of ML-enabled products that evolve over time.
**MLOpsとは、時間と共に進化するML対応プロダクトの継続的な開発のことである**。
The available input data (features) changes over time, the target you are trying to predict changes over time.
**利用可能な入力データ（特徴量）は時間とともに変化し、予測しようとする対象も時間とともに変化する**。
You need to make changes to the source code, and you want to ensure that any changes you make do not break your ML system or degrade its performance.
ソースコードに変更を加える必要があり、その変更がMLシステムを壊したり、性能を低下させたりしないようにしたい。
And you want to accelerate the time required to make those changes and test before those changes are automatically deployed to production.
そして、その変更が本番環境に自動的にデプロイされる前に、その変更とテストに必要な時間を短縮したい。

So, from our perspective, a more pithy definition of MLOps that enables ML Systems to be safely evolved over time is that it requires, at a minimum, automated testing, versioning, and monitoring of ML artifacts.
つまり、私たちの観点からは、MLシステムを安全に時間とともに進化させるために、少なくともMLの成果物の自動テスト、バージョン管理、モニタリングが必要であるという、より簡潔なMLOpsの定義が必要である。
MLOps is about automated testing, versioning, and monitoring of ML artifacts.
**MLOpsとは、MLの成果物の自動テスト、バージョン管理、モニタリングのこと**である。

![figure16]()

In figure 16, we can see that more levels of testing are needed in ML systems than in traditional software systems.
図16を見ると、MLシステムでは従来のソフトウェアシステムよりも多くのレベルのテストが必要であることがわかる。
Small bugs in data or code can easily cause a ML model to make incorrect predictions.
データやコードの小さなバグは、MLモデルが間違った予測をする原因になりやすい。
From a testing perspective, if web applications are propeller-driven airplanes, ML systems are jet-engines.
テストの観点から言えば、ウェブアプリケーションがプロペラ機なら、MLシステムはジェットエンジンだ。
It takes significant engineering effort to test and validate ML Systems to make them safe!
MLシステムを安全なものにするためのテストと検証には、多大なエンジニアリングの労力を要する！

At a high level, we need to test both the source-code and data for ML Systems.
高いレベルでは、**MLシステムのソースコードとデータの両方をテストする必要がある**。
The features created by feature pipelines can have their logic tested with unit tests and their input data checked with data validation tests (e.g., Great Expectations).
featureパイプラインによって作成された特徴量は、ユニットテストでそのロジックをテストし、データバリデーションテスト（例えば[Great Expectations](https://www.hopsworks.ai/post/data-validation-for-enterprise-ai-using-great-expectations-with-hopsworks)）で入力データをチェックすることができる。(great expectationsってなんだ??)
The models need to be tested for performance, but also for a lack of bias against known groups of vulnerable users.
モデルの性能だけでなく、既知の弱者グループに対する偏りがないかどうかもテストする必要がある。
Finally, at the top of the pyramid, ML-Systems need to test their performance with A/B tests before they can switch to use a new model.
最後に、ピラミッドの頂点に位置するMLシステムは、新しいモデルの使用に切り替える前に、A/Bテストでパフォーマンスをテストする必要がある。

When a ML system runs in production, you can also add feature monitoring and model monitoring support to it to try and identify and correct problems in their performance.
MLシステムが本番稼動する際には、**特徴量モニタリングやモデルモニタリング**のサポートを追加して、パフォーマンスの問題を特定して修正することもできます。
For example, monitoring can identify issues such as drift in feature values or a changing prediction target for a ML model.
例えば、モニタリングは、特徴量のドリフトやMLモデルの予測ターゲットの変化といった問題を特定することができる。

![figure18]()

Finally, we need to version ML artifacts so that the operators of ML systems can safely update and rollback versions of deployed models.
最後に、MLシステムのオペレータが、**配備されたモデルのバージョンを安全に更新したりロールバックしたりできるように、MLの成果物をバージョン管理する**必要がある。
System support for the push-button upgrade/downgrade of models is one of the holy grails of MLOps.
プッシュボタンによるモデルのアップグレード／ダウングレードのシステムサポートは、MLOpsの聖杯のひとつである。
But models need features to make predictions, so model versions are connected to feature versions and models and features need to be upgraded/downgraded synchronously.
しかし、モデルは予測を行うために特徴量を必要とする。そのため、**モデルのバージョンは特徴量のバージョンと連動し、モデルと特徴量は同期してアップグレード／ダウングレードされる必要がある**。(なるほど確かに)
Luckily, you don’t need a year in rotation as a Google SRE to easily upgrade/downgrade models - platform support for versioned ML artifacts should make this a straightforward ML system maintenance operation.
幸いなことに、モデルのアップグレードやダウングレードを簡単に行うために、Google SREとして1年間ローテーションを組む必要はない。プラットフォームがバージョン管理されたML成果物をサポートすることで、MLシステムのメンテナンスが容易になるはずだ。

# 6. Example ML Systems built with FTI Pipelines FTI パイプラインで構築された ML システムの例

Here is a sample of some of the open-source ML systems available built on the FTI architecture.
以下は、FTIアーキテクチャで構築されたオープンソースのMLシステムの一部である。
They have been built mostly by practitioners and students.
これらは主に練習生や学生によって作られてきた。

## 6.1. Batch ML Systems バッチMLシステム

Electricity Demand Prediction (452 github stars)
電力需要予測 (452 github stars)

NBA Game Prediction (152 github stars)
NBAの試合予想（githubスター152個）

Premier league football score predictions (101 github stars)
サッカーのプレミアリーグのスコア予想 (101 github stars)

Churn prediction (113 github stars)
解約予測 (113 github stars)

## 6.2. Real-Time ML System リアルタイムMLシステム

Online Credit Card Fraud (113 github stars)
オンラインクレジットカード詐欺 (113 github stars)

Crypto Price Prediction (65 github stars)
暗号通貨価格予測 (65 github stars)

Loan application approval (113 github stars)
ローン申請承認 (113 github stars)

# 7. Summary 要約

This blog post introduces a new mental map for MLOps, the FTI pipeline architecture.
このブログ記事では、MLOpsの新しいメンタル・マップ、FTIパイプライン・アーキテクチャを紹介する。
The architecture has enabled hundreds of developers to build maintainable ML Systems in a short period of time.
このアーキテクチャにより、何百人もの開発者が短期間で保守可能なMLシステムを構築できるようになった。
In our experience, compared to MLOps 1.0, the architecture leads to reduced cognitive load when designing and describing a ML system.
我々の経験では、MLOps 1.0と比較して、このアーキテクチャはMLシステムを設計・記述する際の認知的負荷を軽減する。
In enterprise settings, the architecture enables better communication across teams by providing clear interfaces between teams, leading to better collaboration and higher quality ML systems, faster.
企業環境では、このアーキテクチャはチーム間に明確なインターフェイスを提供することで、チーム間のより良いコミュニケーションを可能にし、より良いコラボレーションとより高品質なMLシステムの迅速な実現につながる。
The architecture hides complexity at a high level, but you can easily drill down to the different feature/training/inference components to examine the details.
アーキテクチャーは高いレベルで複雑さを隠しているが、異なる特徴量/トレーニング/推論のコンポーネントにドリルダウンして詳細を調べることは簡単にできる。
Our hope is that the FTI pipeline architecture can help more teams work better together and get more models into production, quicker, accelerating the transformation of society by AI.
私たちの願いは、**FTIパイプライン・アーキテクチャが、より多くのチームがよりよく協力し、より多くのモデルをより早くproductionに移し、AIによる社会の変革を加速させること**です。

## 7.1. Resources リソース

The serverless ML community (with >2k discord members in August 2023) dedicated to building ML systems using the FTI pipeline architecture.
サーバーレスMLコミュニティ（2023年8月に2k人以上のdiscordメンバーを持つ）FTIパイプラインアーキテクチャを使用したMLシステムの構築に特化。

There is a serverless ML course, given by Jim Dowling and Hopsworks, that introduces the FTI pipeline architecture and how to build ML systems using free serverless technologies.
ジム・ダウリングとホップワークスによるサーバーレスMLコースがあり、FTIパイプライン・アーキテクチャと無料のサーバーレス技術を使ったMLシステムの構築方法を紹介している。
