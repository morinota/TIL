refs: https://www.uber.com/en-JP/blog/michelangelo-machine-learning-platform/

# Meet Michelangelo: Uber’s Machine Learning Platform
# ミケランジェロに出会う：ウーバーの機械学習プラットフォーム

September 5, 2017/Global
2017年9月5日/グローバル

Uber Engineering is committed to developing technologies that create seamless, impactful experiences for our customers. 
ウーバーエンジニアリングは、顧客にシームレスで影響力のある体験を提供する技術の開発に取り組んでいます。
We are increasingly investing in artificial intelligence (AI) and machine learning (ML) to fulfill this vision. 
私たちは、このビジョンを実現するために、人工知能（AI）と機械学習（ML）への投資を増やしています。
At Uber, our contribution to this space is Michelangelo, an internal ML-as-a-service platform that democratizes machine learning and makes scaling AI to meet the needs of business as easy as requesting a ride. 
ウーバーにおける私たちの貢献は、機械学習を民主化し、ビジネスのニーズに応じてAIをスケールすることを、乗車をリクエストするのと同じくらい簡単にする内部のML-as-a-serviceプラットフォームであるミケランジェロです。

Michelangelo enables internal teams to seamlessly build, deploy, and operate machine learning solutions at Uber’s scale. 
ミケランジェロは、内部チームがウーバーの規模で機械学習ソリューションをシームレスに構築、展開、運用できるようにします。
It is designed to cover the end-to-end ML workflow: manage data, train, evaluate, and deploy models, make predictions, and monitor predictions. 
これは、データの管理、モデルのトレーニング、評価、展開、予測の実施、予測の監視というエンドツーエンドのMLワークフローをカバーするように設計されています。
The system also supports traditional ML models, time series forecasting, and deep learning. 
このシステムは、従来のMLモデル、時系列予測、深層学習もサポートしています。

Michelangelo has been serving production use cases at Uber for about a year and has become the de-facto system for machine learning for our engineers and data scientists, with dozens of teams building and deploying models. 
ミケランジェロは、ウーバーで約1年間にわたり本番のユースケースに対応しており、エンジニアやデータサイエンティストにとっての事実上の機械学習システムとなり、数十のチームがモデルを構築し展開しています。
In fact, it is deployed across several Uber data centers, leverages specialized hardware, and serves predictions for the highest loaded online services at the company. 
実際、これは複数のウーバーデータセンターに展開され、専門のハードウェアを活用し、会社の最も負荷の高いオンラインサービスに対して予測を提供しています。

In this article, we introduce Michelangelo, discuss product use cases, and walk through the workflow of this powerful new ML-as-a-service system. 
この記事では、ミケランジェロを紹介し、製品のユースケースについて議論し、この強力な新しいML-as-a-serviceシステムのワークフローを説明します。

<!-- ここまで読んだ -->

### Motivation behind Michelangelo 

Before Michelangelo, we faced a number of challenges with building and deploying machine learning models at Uber related to the size and scale of our operations. 
Michelangelo以前、私たちはUberにおける機械学習モデルの構築と展開に関して、運用の規模とサイズに関連するいくつかの課題に直面していました。
While data scientists were using a wide variety of tools to create predictive models (R, scikit-learn, custom algorithms, etc.), separate engineering teams were also building bespoke one-off systems to use these models in production. 
データサイエンティストは、予測モデルを作成するためにさまざまなツール（R、scikit-learn、カスタムアルゴリズムなど）を使用していましたが、別のエンジニアリングチームもこれらのモデルを本番環境で使用するための特注の一回限りのシステムを構築していました。
As a result, the impact of ML at Uber was limited to what a few data scientists and engineers could build in a short time frame with mostly open source tools. 
その結果、**Uberにおける機械学習の影響は、数人のデータサイエンティストとエンジニアが主にオープンソースツールを使用して短期間で構築できるものに限られていました**。

Specifically, there were no systems in place to build reliable, uniform, and reproducible pipelines for creating and managing training and prediction data at scale. 
**具体的には、大規模なトレーニングおよび予測データを作成・管理するための信頼性が高く、均一で再現可能なパイプラインを構築するためのシステムが存在しませんでした**。
Prior to Michelangelo, it was not possible to train models larger than what would fit on data scientists’ desktop machines, and there was neither a standard place to store the results of training experiments nor an easy way to compare one experiment to another. 
Michelangelo以前は、データサイエンティストのデスクトップマシンに収まる以上のサイズのモデルをトレーニングすることは不可能であり、トレーニング実験の結果を保存するための標準的な場所も、1つの実験を別の実験と比較するための簡単な方法もありませんでした。
Most importantly, there was no established path to deploying a model into production–in most cases, the relevant engineering team had to create a custom serving container specific to the project at hand. 
最も重要なことは、モデルを本番環境に展開するための確立された手順がなく、ほとんどの場合、関連するエンジニアリングチームはプロジェクトに特化したカスタムサービングコンテナを作成する必要がありました。
At the same time, we were starting to see signs of many of the ML anti-patterns documented by Scully et al. 
同時に、私たちは**Scullyらによって文書化された多くの機械学習のアンチパターンの兆候**を見始めていました。(後で見る...!:thinking:)
https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf?uclick_id=a913986d-0cf2-421e-8456-1e51d52efbc3

Michelangelo is designed to address these gaps by standardizing the workflows and tools across teams though an end-to-end system that enables users across the company to easily build and operate machine learning systems at scale. 
Michelangeloは、**チーム間のワークフローとツールを標準化**することによって、これらのギャップに対処するように設計されており、会社全体のユーザーが大規模な機械学習システムを簡単に構築し運用できるエンドツーエンドのシステムを提供します。
Our goal was not only to solve these immediate problems, but also create a system that would grow with the business. 
私たちの目標は、これらの即時の問題を解決するだけでなく、ビジネスと共に成長するシステムを作成することでした。

When we began building Michelangelo in mid 2015, we started by addressing the challenges around scalable model training and deployment to production serving containers. 
2015年中頃にMichelangeloの構築を始めたとき、私たちはスケーラブルなモデルのトレーニングと本番サービングコンテナへの展開に関する課題に取り組み始めました。
Then, we focused on building better systems for managing and sharing feature pipelines. 
次に、私たちは**特徴パイプラインを管理し共有するためのより良いシステムの構築**に焦点を当てました。
More recently, the focus shifted to developer productivity–how to speed up the path from idea to first production model and the fast iterations that follow. 
最近では、開発者の生産性に焦点が移り、アイデアから最初の本番モデルへの道をどのように迅速化し、その後の迅速な反復を実現するかに取り組んでいます。

In the next section, we look at an example application to understand how Michelangelo has been used to build and deploy models to solve specific problems at Uber. 
次のセクションでは、Michelangeloがどのように使用されて特定の問題を解決するためのモデルを構築し展開しているかを理解するための例アプリケーションを見ていきます。
While we highlight a specific use case for UberEATS, the platform manages dozens of similar models across the company for a variety of prediction use cases. 
私たちはUberEATSの特定のユースケースを強調しますが、このプラットフォームは、さまざまな予測ユースケースのために会社全体で数十の類似モデルを管理しています。

<!-- ここまで読んだ -->

### Use case: UberEATS estimated time of delivery model 使用例: UberEATSの配達時間予測モデル

UberEATS has several models running on Michelangelo, covering meal delivery time predictions, search rankings, search autocomplete, and restaurant rankings. 
UberEATSは、Michelangelo上で複数のモデルを運用しており、食事の配達時間予測、検索ランキング、検索オートコンプリート、レストランランキングをカバーしています。
The delivery time models predict how much time a meal will take to prepare and deliver before the order is issued and then again at each stage of the delivery process. 
配達時間モデルは、注文が発行される前に食事の準備と配達にかかる時間を予測し、その後、配達プロセスの各段階で再度予測します。

Predicting meal estimated time of delivery (ETD) is not simple. 
食事の推定配達時間（ETD）を予測することは簡単ではありません。
When an UberEATS customer places an order it is sent to the restaurant for processing. 
UberEATSの顧客が注文をすると、それはレストランに処理のために送信されます。
The restaurant then needs to acknowledge the order and prepare the meal which will take time depending on the complexity of the order and how busy the restaurant is. 
レストランはその後、注文を確認し、食事を準備する必要がありますが、これは注文の複雑さやレストランの混雑具合によって時間がかかります。
When the meal is close to being ready, an Uber delivery-partner is dispatched to pick up the meal. 
食事が準備完了に近づくと、Uberの配達パートナーが食事を受け取るために派遣されます。
Then, the delivery-partner needs to get to the restaurant, find parking, walk inside to get the food, then walk back to the car, drive to the customer’s location (which depends on route, traffic, and other factors), find parking, and walk to the customer’s door to complete the delivery. 
その後、配達パートナーはレストランに行き、駐車場を見つけ、食べ物を受け取りに中に入り、再び車に戻り、顧客の場所まで運転します（これはルート、交通、その他の要因によって異なります）、駐車場を見つけ、顧客のドアまで歩いて配達を完了させる必要があります。
The goal is to predict the total duration of this complex multi-stage process, as well as recalculate these time-to-delivery predictions at every step of the process. 
目標は、この複雑な多段階プロセスの総所要時間を予測し、プロセスの各ステップでこれらの配達時間予測を再計算することです。

On the Michelangelo platform, the UberEATS data scientists use gradient boosted decision tree regression models to predict this end-to-end delivery time. 
Michelangeloプラットフォーム上で、UberEATSのデータサイエンティストは、エンドツーエンドの配達時間を予測するために勾配ブースティング決定木回帰モデルを使用しています。
Features for the model include information from the request (e.g., time of day, delivery location), historical features (e.g. average meal prep time for the last seven days), and near-realtime calculated features (e.g., average meal prep time for the last one hour). 
**モデルの特徴には、リクエストからの情報（例：時間帯、配達場所）、過去の特徴（例：過去7日間の平均食事準備時間）、およびほぼリアルタイムで計算された特徴（例：過去1時間の平均食事準備時間）が含まれます**。
Models are deployed across Uber’s data centers to Michelangelo model serving containers and are invoked via network requests by the UberEATS microservices. 
モデルは、Uberのデータセンター全体に展開され、Michelangeloモデルサービングコンテナに配置され、UberEATSのマイクロサービスによってネットワークリクエストを介して呼び出されます。
These predictions are displayed to UberEATS customers prior to ordering from a restaurant and as their meal is being prepared and delivered. 
これらの予測は、顧客がレストランから注文する前や、食事が準備され配達される際にUberEATSの顧客に表示されます。

<!-- ここまで読んだ -->

### System architecture システムアーキテクチャ

Michelangelo consists of a mix of open source systems and components built in-house. 
Michelangeloは、オープンソースシステムと社内で構築されたコンポーネントの混合で構成されています。
The primary open sourced components used are HDFS, Spark, Samza, Cassandra, MLLib, XGBoost, and TensorFlow. 
主に使用されるオープンソースコンポーネントは、HDFS、Spark、Samza、Cassandra、MLLib、XGBoost、およびTensorFlowです。
We generally prefer to use mature open source options where possible, and will fork, customize, and contribute back as needed, though we sometimes build systems ourselves when open source solutions are not ideal for our use case. 
私たちは、可能な限り成熟したオープンソースの選択肢を使用することを好み、必要に応じてフォーク、カスタマイズ、そして貢献しますが、オープンソースのソリューションが私たちのユースケースに理想的でない場合は、時には自分たちでシステムを構築することもあります。

Michelangelo is built on top of Uber’s data and compute infrastructure, providing a data lake that stores all of Uber’s transactional and logged data, Kafka brokers that aggregate logged messages from all Uber’s services, a Samza streaming compute engine, managed Cassandra clusters, and Uber’s in-house service provisioning and deployment tools. 
Michelangeloは、Uberのデータおよび計算インフラストラクチャの上に構築されており、Uberのすべてのトランザクションデータとログデータを保存するデータレイク、Uberのすべてのサービスからのログメッセージを集約するKafkaブローカー、Samzaストリーミング計算エンジン、管理されたCassandraクラスター、およびUberの社内サービスプロビジョニングとデプロイメントツールを提供します。

In the next section, we walk through the layers of the system using the UberEATS ETD models as a case study to illustrate the technical details of Michelangelo. 
次のセクションでは、UberEATS ETDモデルをケーススタディとして使用し、Michelangeloの技術的詳細を示すためにシステムの層を説明します。

<!-- ここまで読んだ -->

### Machine learning workflow 機械学習ワークフロー

The same general workflow exists across almost all machine learning use cases at Uber regardless of the challenge at hand, including classification and regression, as well as time series forecasting. 
**Uberのほぼすべての機械学習ユースケースにおいて、分類や回帰、時系列予測を含む課題に関係なく、同じ一般的なワークフローが存在します**。
The workflow is generally implementation-agnostic, so easily expanded to support new algorithm types and frameworks, such as newer deep learning frameworks. 
このワークフローは一般的に実装に依存しないため、新しいアルゴリズムタイプやフレームワーク（新しい深層学習フレームワークなど）をサポートするために簡単に拡張できます。
It also applies across different deployment modes such as both online and offline (and in-car and in-phone) prediction use cases. 
また、オンラインおよびオフライン（車内および電話内）予測ユースケースなど、さまざまなデプロイメントモードに適用されます。

We designed Michelangelo specifically to provide scalable, reliable, reproducible, easy-to-use, and automated tools to address the following six-step workflow: 
私たちは、スケーラブルで信頼性が高く、再現可能で使いやすく、自動化されたツールを提供するために、Michelangeloを特に設計しました。以下の6ステップのワークフローに対応します。

1. Manage data
2. データ管理

3. Train models
4. モデルのトレーニング

5. Evaluate models
6. モデルの評価

7. Deploy models
8. モデルのデプロイ

9. Make predictions
10. 予測の実施

11. Monitor predictions
12. 予測の監視

Next, we go into detail about how Michelangelo’s architecture facilitates each stage of this workflow. 
次に、Michelangeloのアーキテクチャがこのワークフローの各ステージをどのように促進するかについて詳しく説明します。

<!-- ここまで読んだ -->

#### Manage data データ管理

Finding good features is often the hardest part of machine learning and we have found that building and managing data pipelines is typically one of the most costly pieces of a complete machine learning solution. 
良い特徴を見つけることはしばしば機械学習の最も難しい部分であり、データパイプラインの構築と管理が通常、完全な機械学習ソリューションの中で最もコストがかかる部分の1つであることがわかりました。

A platform should provide standard tools for building data pipelines to generate feature and label data sets for training (and re-training) and feature-only data sets for predicting. 
プラットフォームは、トレーニング（および再トレーニング）のための特徴とラベルデータセットを生成し、予測のための特徴のみのデータセットを生成するためのデータパイプラインを構築するための標準ツールを提供する必要があります。

These tools should have deep integration with the company’s data lake or warehouses and with the company’s online data serving systems. 
これらのツールは、会社のデータレイクや倉庫、会社のオンラインデータ提供システムと深く統合されている必要があります。

The pipelines need to be scalable and performant, incorporate integrated monitoring for data flow and data quality, and support both online and offline training and predicting. 
パイプラインはスケーラブルで高性能である必要があり、データフローとデータ品質の統合監視を組み込み、オンラインおよびオフラインのトレーニングと予測の両方をサポートする必要があります。

Ideally, they should also generate the features in a way that is shareable across teams to reduce duplicate work and increase data quality. 
理想的には、重複作業を減らしデータ品質を向上させるために、チーム間で共有可能な方法で特徴を生成する必要があります。

They should also provide strong guard rails and controls to encourage and empower users to adopt best practices (e.g., making it easy to guarantee that the same data generation/preparation process is used at both training time and prediction time). 
また、ユーザーがベストプラクティスを採用することを奨励し、支援するための強力なガードレールとコントロールを提供する必要があります（例：トレーニング時と予測時に同じデータ生成/準備プロセスが使用されることを保証するのを容易にすること）。

The data management components of Michelangelo are divided between online and offline pipelines. 
Michelangeloのデータ管理コンポーネントは、オンラインパイプラインとオフラインパイプラインに分かれています。

Currently, the offline pipelines are used to feed batch model training and batch prediction jobs and the online pipelines feed online, low latency predictions (and in the near future, online learning systems). 
現在、オフラインパイプラインはバッチモデルのトレーニングとバッチ予測ジョブに供給され、オンラインパイプラインはオンラインの低遅延予測（および近い将来にはオンライン学習システム）に供給されます。

In addition, we added a layer of data management, a feature store that allows teams to share, discover, and use a highly curated set of features for their machine learning problems. 
さらに、データ管理のレイヤーとして、チームが機械学習の問題に対して高度にキュレーションされた特徴のセットを共有、発見、使用できるフィーチャーストアを追加しました。

We found that many modeling problems at Uber use identical or similar features, and there is substantial value in enabling teams to share features between their own projects and for teams in different organizations to share features with each other. 
私たちは、Uberの多くのモデリング問題が同一または類似の特徴を使用していることを発見し、チームが自分たちのプロジェクト間で特徴を共有し、異なる組織のチームが互いに特徴を共有できるようにすることに大きな価値があると考えています。

##### Offline オフライン

Uber’s transactional and log data flows into an HDFS data lake and is easily accessible via Spark and Hive SQL compute jobs. 
UberのトランザクションデータとログデータはHDFSデータレイクに流れ込み、SparkやHive SQL計算ジョブを介して簡単にアクセスできます。

We provide containers and scheduling to run regular jobs to compute features which can be made private to a project or published to the Feature Store (see below) and shared across teams, while batch jobs run on a schedule or a trigger and are integrated with data quality monitoring tools to quickly detect regressions in the pipeline–either due to local or upstream code or data issues. 
私たちは、プロジェクトにプライベートにすることができる特徴を計算するための定期的なジョブを実行するためのコンテナとスケジューリングを提供し、フィーチャーストア（下記参照）に公開してチーム間で共有します。一方、バッチジョブはスケジュールまたはトリガーで実行され、データ品質監視ツールと統合されて、パイプライン内の回帰を迅速に検出します（ローカルまたは上流のコードやデータの問題によるもの）。

##### Online オンライン

Models that are deployed online cannot access data stored in HDFS, and it is often difficult to compute some features in a performant manner directly from the online databases that back Uber’s production services (for instance, it is not possible to directly query the UberEATS order service to compute the average meal prep time for a restaurant over a specific period of time). 
オンラインにデプロイされたモデルはHDFSに保存されたデータにアクセスできず、Uberのプロダクションサービスを支えるオンラインデータベースから直接パフォーマンス良く一部の特徴を計算することはしばしば困難です（例えば、特定の期間におけるレストランの平均食事準備時間を計算するためにUberEATSの注文サービスを直接クエリすることはできません）。

Instead, we allow features needed for online models to be precomputed and stored in Cassandra where they can be read at low latency at prediction time. 
その代わりに、オンラインモデルに必要な特徴を事前に計算し、Cassandraに保存して、予測時に低遅延で読み取ることを許可します。

We support two options for computing these online-served features, batch precompute and near-real-time compute, outlined below: 
これらのオンライン提供される特徴を計算するための2つのオプション、バッチ事前計算と近リアルタイム計算をサポートしています。以下に概説します。

- Batch precompute. The first option for computing is to conduct bulk precomputing and loading historical features from HDFS into Cassandra on a regular basis. 
- バッチ事前計算。計算の最初のオプションは、HDFSからCassandraに歴史的特徴を定期的にバルク事前計算してロードすることです。

This is simple and efficient, and generally works well for historical features where it is acceptable for the features to only be updated every few hours or once a day. 
これはシンプルで効率的であり、一般的に、特徴が数時間ごとまたは1日に1回のみ更新されることが許容される歴史的特徴に対してうまく機能します。

This system guarantees that the same data and batch pipeline is used for both training and serving. 
このシステムは、トレーニングと提供の両方に同じデータとバッチパイプラインが使用されることを保証します。

UberEATS uses this system for features like a ‘restaurant’s average meal preparation time over the last seven days.’ 
UberEATSは、このシステムを「過去7日間のレストランの平均食事準備時間」のような特徴に使用しています。

- Near-real-time compute. The second option is to publish relevant metrics to Kafka and then run Samza-based streaming compute jobs to generate aggregate features at low latency. 
- 近リアルタイム計算。2番目のオプションは、関連するメトリックをKafkaに公開し、その後、Samzaベースのストリーミング計算ジョブを実行して低遅延で集約特徴を生成することです。

These features are then written directly to Cassandra for serving and logged back to HDFS for future training jobs. 
これらの特徴は、その後、提供のためにCassandraに直接書き込まれ、将来のトレーニングジョブのためにHDFSにログされます。

Like the batch system, near-real-time compute ensures that the same data is used for training and serving. 
バッチシステムと同様に、近リアルタイム計算は、トレーニングと提供の両方に同じデータが使用されることを保証します。

To avoid a cold start, we provide a tool to “backfill” this data and generate training data by running a batch job against historical logs. 
コールドスタートを避けるために、私たちはこのデータを「バックフィル」し、歴史的ログに対してバッチジョブを実行することによってトレーニングデータを生成するツールを提供します。

UberEATS uses this near-realtime pipeline for features like a ‘restaurant’s average meal preparation time over the last one hour.’ 
UberEATSは、この近リアルタイムパイプラインを「過去1時間のレストランの平均食事準備時間」のような特徴に使用しています。

##### Shared feature store 共有フィーチャーストア

We found great value in building a centralized Feature Store in which teams around Uber can create and manage canonical features to be used by their teams and shared with others. 
私たちは、Uberの周りのチームが自分たちのチームで使用し、他のチームと共有できる標準的な特徴を作成し管理できる中央集権的なフィーチャーストアを構築することに大きな価値があると考えました。

At a high level, it accomplishes two things: 
高いレベルで、これは2つのことを達成します。

1. It allows users to easily add features they have built into a shared feature store, requiring only a small amount of extra metadata (owner, description, SLA, etc.) on top of what would be required for a feature generated for private, project-specific usage. 
1. ユーザーが自分たちが構築した特徴を共有フィーチャーストアに簡単に追加できるようにし、プライベートなプロジェクト特有の使用のために生成された特徴に必要なものに加えて、少量の追加メタデータ（所有者、説明、SLAなど）を必要とします。

2. Once features are in the Feature Store, they are very easy to consume, both online and offline, by referencing a feature’s simple canonical name in the model configuration. 
2. 一度特徴がフィーチャーストアに入ると、それらはモデル構成内の特徴のシンプルな標準名を参照することによって、オンラインおよびオフラインの両方で非常に簡単に利用できます。

Equipped with this information, the system handles joining in the correct HDFS data sets for model training or batch prediction and fetching the right value from Cassandra for online predictions. 
この情報を持って、システムはモデルのトレーニングやバッチ予測のために正しいHDFSデータセットを結合し、オンライン予測のためにCassandraから正しい値を取得します。

At the moment, we have approximately 10,000 features in Feature Store that are used to accelerate machine learning projects, and teams across the company are adding new ones all the time. 
現在、フィーチャーストアには約10,000の特徴があり、機械学習プロジェクトを加速するために使用されており、会社全体のチームが常に新しいものを追加しています。

Features in the Feature Store are automatically calculated and updated daily. 
フィーチャーストア内の特徴は自動的に計算され、毎日更新されます。

In the future, we intend to explore the possibility of building an automated system to search through Feature Store and identify the most useful and important features for solving a given prediction problem. 
将来的には、フィーチャーストアを検索し、特定の予測問題を解決するために最も有用で重要な特徴を特定する自動化システムを構築する可能性を探るつもりです。

##### Domain specific language for feature selection and transformation 特徴選択と変換のためのドメイン特化言語

Often the features generated by data pipelines or sent from a client service are not in the proper format for the model, and they may be missing values that need to be filled. 
データパイプラインによって生成された特徴やクライアントサービスから送信された特徴は、モデルに適した形式でないことが多く、埋める必要がある値が欠けている場合があります。

Moreover, the model may only need a subset of features provided. 
さらに、モデルは提供された特徴のサブセットのみを必要とする場合があります。

In some cases, it may be more useful for the model to transform a timestamp into an hour-of-day or day-of-week to better capture seasonal patterns. 
場合によっては、モデルがタイムスタンプを時間帯や曜日に変換して季節的なパターンをよりよく捉える方が有用なことがあります。

In other cases, feature values may need to be normalized (e.g., subtract the mean and divide by standard deviation). 
他の場合では、特徴値を正規化する必要があるかもしれません（例：平均を引いて標準偏差で割る）。

To address these issues, we created a DSL (domain specific language) that modelers use to select, transform, and combine the features that are sent to the model at training and prediction times. 
これらの問題に対処するために、私たちはモデル作成者がトレーニング時と予測時にモデルに送信される特徴を選択、変換、結合するために使用するDSL（ドメイン特化言語）を作成しました。

The DSL is implemented as sub-set of Scala. 
DSLはScalaのサブセットとして実装されています。

It is a pure functional language with a complete set of commonly used functions. 
これは、一般的に使用される関数の完全なセットを持つ純粋な関数型言語です。

With this DSL, we also provide the ability for customer teams to add their own user-defined functions. 
このDSLを使用して、顧客チームが独自のユーザー定義関数を追加できる機能も提供します。

There are accessor functions that fetch feature values from the current context (data pipeline in the case of an offline model or current request from client in the case of an online model) or from the Feature Store. 
現在のコンテキスト（オフラインモデルの場合はデータパイプライン、オンラインモデルの場合はクライアントからの現在のリクエスト）またはフィーチャーストアから特徴値を取得するアクセサ関数があります。

It is important to note that the DSL expressions are part of the model configuration and the same expressions are applied at training time and at prediction time to help guarantee that the same final set of features is generated and sent to the model in both cases. 
DSLの式はモデル構成の一部であり、同じ式がトレーニング時と予測時の両方に適用され、同じ最終的な特徴セットが生成され、モデルに送信されることを保証するのに役立つことに注意することが重要です。

#### Train models モデルのトレーニング

We currently support offline, large-scale distributed training of decision trees, linear and logistic models, unsupervised models (k-means), time series models, and deep neural networks. 
現在、私たちはオフラインでの大規模分散トレーニングをサポートしており、決定木、線形およびロジスティックモデル、教師なしモデル（k-means）、時系列モデル、深層ニューラルネットワークを含みます。

We regularly add new algorithms in response to customer need and as they are developed by Uber’s AI Labs and other internal researchers. 
私たちは、顧客のニーズに応じて新しいアルゴリズムを定期的に追加し、UberのAIラボや他の内部研究者によって開発されます。

In addition, we let customer teams add their own model types by providing custom training, evaluation, and serving code. 
さらに、顧客チームが独自のモデルタイプを追加できるように、カスタムトレーニング、評価、および提供コードを提供します。

The distributed model training system scales up to handle billions of samples and down to small datasets for quick iterations. 
分散モデルトレーニングシステムは、数十億のサンプルを処理するためにスケールアップし、迅速な反復のために小さなデータセットにスケールダウンします。

A model configuration specifies the model type, hyper-parameters, data source reference, and feature DSL expressions, as well as compute resource requirements (the number of machines, how much memory, whether or not to use GPUs, etc.). 
モデル構成は、モデルタイプ、ハイパーパラメータ、データソース参照、特徴DSL式、および計算リソース要件（マシンの数、メモリの量、GPUを使用するかどうかなど）を指定します。

It is used to configure the training job, which is run on a YARN or Mesos cluster. 
これは、YARNまたはMesosクラスターで実行されるトレーニングジョブを構成するために使用されます。

After the model is trained, performance metrics (e.g., ROC curve and PR curve) are computed and combined into a model evaluation report. 
モデルがトレーニングされた後、パフォーマンスメトリック（例：ROC曲線およびPR曲線）が計算され、モデル評価レポートにまとめられます。

At the end of training, the original configuration, the learned parameters, and the evaluation report are saved back to our model repository for analysis and deployment. 
トレーニングの最後に、元の構成、学習されたパラメータ、および評価レポートが分析とデプロイのために私たちのモデルリポジトリに保存されます。

In addition to training single models, Michelangelo supports hyper-parameter search for all model types as well as partitioned models. 
単一モデルのトレーニングに加えて、Michelangeloはすべてのモデルタイプのハイパーパラメータ検索とパーティションモデルをサポートしています。

With partitioned models, we automatically partition the training data based on configuration from the user and then train one model per partition, falling back to a parent model when needed (e.g. training one model per city and falling back to a country-level model when an accurate city-level model cannot be achieved). 
パーティションモデルでは、ユーザーからの構成に基づいてトレーニングデータを自動的にパーティション分割し、各パーティションごとに1つのモデルをトレーニングし、必要に応じて親モデルにフォールバックします（例：都市ごとに1つのモデルをトレーニングし、正確な都市レベルのモデルが達成できない場合は国レベルのモデルにフォールバックします）。

Training jobs can be configured and managed through a web UI or an API, often via Jupyter notebook. 
トレーニングジョブは、Web UIまたはAPIを介して構成および管理でき、しばしばJupyterノートブックを介して行われます。

Many teams use the API and workflow tools to schedule regular re-training of their models. 
多くのチームはAPIとワークフローツールを使用して、モデルの定期的な再トレーニングをスケジュールしています。

#### Evaluate models モデルの評価

Models are often trained as part of a methodical exploration process to identify the set of features, algorithms, and hyper-parameters that create the best model for their problem. 
モデルはしばしば、問題に対して最良のモデルを作成するための特徴、アルゴリズム、およびハイパーパラメータのセットを特定するための体系的な探索プロセスの一部としてトレーニングされます。

Before arriving at the ideal model for a given use case, it is not uncommon to train hundreds of models that do not make the cut. 
特定のユースケースに対して理想的なモデルに到達する前に、基準を満たさない数百のモデルをトレーニングすることは珍しくありません。

Though not ultimately used in production, the performance of these models guide engineers towards the model configuration that results in the best model performance. 
最終的に本番環境で使用されない場合でも、これらのモデルのパフォーマンスはエンジニアを最良のモデルパフォーマンスをもたらすモデル構成に導きます。

Keeping track of these trained models (e.g. who trained them and when, on what data set, with which hyper-parameters, etc.), evaluating them, and comparing them to each other are typically big challenges when dealing with so many models and present opportunities for the platform to add a lot of value. 
これらのトレーニングされたモデルを追跡すること（例：誰がいつ、どのデータセットで、どのハイパーパラメータでトレーニングしたかなど）、それらを評価し、互いに比較することは、これほど多くのモデルを扱う際の大きな課題であり、プラットフォームが多くの価値を追加する機会を提供します。

For every model that is trained in Michelangelo, we store a versioned object in our model repository in Cassandra that contains a record of: 
Michelangeloでトレーニングされたすべてのモデルについて、Cassandraのモデルリポジトリにバージョン管理されたオブジェクトを保存し、以下の記録を含みます。

- Who trained the model
- モデルをトレーニングしたのは誰か

- Start and end time of the training job
- トレーニングジョブの開始時刻と終了時刻

- Full model configuration (features used, hyper-parameter values, etc.)
- 完全なモデル構成（使用された特徴、ハイパーパラメータの値など）

- Reference to training and test data sets
- トレーニングおよびテストデータセットへの参照

- Distribution and relative importance of each feature
- 各特徴の分布と相対的重要性

- Model accuracy metrics
- モデルの精度メトリック

- Standard charts and graphs for each model type (e.g. ROC curve, PR curve, and confusion matrix for a binary classifier)
- 各モデルタイプの標準的なチャートとグラフ（例：ROC曲線、PR曲線、バイナリ分類器の混同行列）

- Full learned parameters of the model
- モデルの完全な学習パラメータ

- Summary statistics for model visualization
- モデルの視覚化のための要約統計

The information is easily available to the user through a web UI and programmatically through an API, both for inspecting the details of an individual model and for comparing one or more models with each other. 
この情報は、個々のモデルの詳細を検査するためや、1つ以上のモデルを互いに比較するために、Web UIを介して、またAPIを介してユーザーに簡単に提供されます。

#### Model accuracy report モデル精度レポート

The model accuracy report for a regression model shows standard accuracy metrics and charts. 
回帰モデルのモデル精度レポートは、標準的な精度メトリックとチャートを示します。

Classification models would display a different set, as depicted below in Figures 4 and 5: 
分類モデルは、以下の図4および5に示すように、異なるセットを表示します。

##### Decision tree visualization 決定木の視覚化

For important model types, we provide sophisticated visualization tools to help modelers understand why a model behaves as it does, as well as to help debug it if necessary. 
重要なモデルタイプに対して、モデル作成者がモデルがどのように動作するかを理解し、必要に応じてデバッグを支援するための高度な視覚化ツールを提供します。

In the case of decision tree models, we let the user browse through each of the individual trees to see their relative importance to the overall model, their split points, the importance of each feature to a particular tree, and the distribution of data at each split, among other variables. 
決定木モデルの場合、ユーザーが各個別の木を閲覧して、全体モデルに対する相対的重要性、分割点、特定の木に対する各特徴の重要性、および各分割でのデータの分布などの変数を確認できるようにします。

The user can specify feature values and the visualization will depict the triggered paths down the decision trees, the prediction per tree, and the overall prediction for the model, as pictured in Figure 6 below: 
ユーザーは特徴値を指定でき、視覚化は決定木の下でトリガーされたパス、各木ごとの予測、およびモデル全体の予測を示します。以下の図6に示されています。

##### Feature report 特徴レポート

Michelangelo provides a feature report that shows each feature in order of importance to the model along with partial dependence plots and distribution histograms. 
Michelangeloは、モデルに対する重要性の順に各特徴を示し、部分依存プロットと分布ヒストグラムを提供する特徴レポートを提供します。

Selecting two features lets the user understand the feature interactions as a two-way partial dependence diagram, as showcased below: 
2つの特徴を選択することで、ユーザーは特徴の相互作用を二方向の部分依存図として理解できます。以下に示します。

#### Deploy models モデルのデプロイ

Michelangelo has end-to-end support for managing model deployment via the UI or API and three modes in which a model can be deployed: 
Michelangeloは、UIまたはAPIを介してモデルデプロイメントを管理するためのエンドツーエンドのサポートを提供し、モデルをデプロイできる3つのモードを持っています。

1. Offline deployment. The model is deployed to an offline container and run in a Spark job to generate batch predictions either on demand or on a repeating schedule. 
1. オフラインデプロイメント。モデルはオフラインコンテナにデプロイされ、Sparkジョブで実行され、オンデマンドまたは繰り返しスケジュールでバッチ予測を生成します。

2. Online deployment. The model is deployed to an online prediction service cluster (generally containing hundreds of machines behind a load balancer) where clients can send individual or batched prediction requests as network RPC calls. 
2. オンラインデプロイメント。モデルはオンライン予測サービスクラスターにデプロイされ（通常はロードバランサーの背後に数百台のマシンを含む）、クライアントは個別またはバッチの予測リクエストをネットワークRPC呼び出しとして送信できます。

3. Library deployment. We intend to launch a model that is deployed to a serving container that is embedded as a library in another service and invoked via a Java API. (It is not shown in Figure 8, below, but works similarly to online deployment). 
3. ライブラリデプロイメント。別のサービスにライブラリとして埋め込まれ、Java APIを介して呼び出されるサービングコンテナにデプロイされるモデルを立ち上げる予定です。（以下の図8には示されていませんが、オンラインデプロイメントと同様に機能します）。

In all cases, the required model artifacts (metadata files, model parameter files, and compiled DSL expressions) are packaged in a ZIP archive and copied to the relevant hosts across Uber’s data centers using our standard code deployment infrastructure. 
すべての場合において、必要なモデルアーティファクト（メタデータファイル、モデルパラメータファイル、およびコンパイルされたDSL式）はZIPアーカイブにパッケージされ、私たちの標準的なコードデプロイメントインフラストラクチャを使用してUberのデータセンター全体の関連ホストにコピーされます。

The prediction containers automatically load the new models from disk and start handling prediction requests. 
予測コンテナは自動的にディスクから新しいモデルをロードし、予測リクエストの処理を開始します。

Many teams have automation scripts to schedule regular model retraining and deployment via Michelangelo’s API. 
多くのチームは、MichelangeloのAPIを介して定期的なモデル再トレーニングとデプロイメントをスケジュールするための自動化スクリプトを持っています。

In the case of the UberEATS delivery time models, training and deployment are triggered manually by data scientists and engineers through the web UI. 
UberEATSの配達時間モデルの場合、トレーニングとデプロイメントはデータサイエンティストとエンジニアによってWeb UIを介して手動でトリガーされます。

#### Make predictions 予測の実施

Once models are deployed and loaded by the serving container, they are used to make predictions based on feature data loaded from a data pipeline or directly from a client service. 
モデルがデプロイされ、サービングコンテナによってロードされると、データパイプラインからロードされた特徴データまたはクライアントサービスから直接のデータに基づいて予測を行うために使用されます。

The raw features are passed through the compiled DSL expressions which can modify the raw features and/or fetch additional features from the Feature Store. 
生の特徴は、コンパイルされたDSL式を通過し、生の特徴を変更したり、フィーチャーストアから追加の特徴を取得したりすることができます。

The final feature vector is constructed and passed to the model for scoring. 
最終的な特徴ベクトルが構築され、モデルにスコアリングのために渡されます。

In the case of online models, the prediction is returned to the client service over the network. 
オンラインモデルの場合、予測はネットワークを介してクライアントサービスに返されます。

In the case of offline models, the predictions are written back to Hive where they can be consumed by downstream batch jobs or accessed by users directly through SQL-based query tools, as depicted below: 
オフラインモデルの場合、予測はHiveに書き戻され、下流のバッチジョブによって消費されるか、ユーザーがSQLベースのクエリツールを介して直接アクセスできるようになります。以下に示します。

#### Referencing models モデルの参照

More than one model can be deployed at the same time to a given serving container. 
同じサービングコンテナに複数のモデルを同時にデプロイすることができます。

This allows safe transitions from old models to new models and side-by-side A/B testing of models. 
これにより、古いモデルから新しいモデルへの安全な移行と、モデルの並行A/Bテストが可能になります。

At serving time, a model is identified by its UUID and an optional tag (or alias) that is specified during deployment. 
提供時に、モデルはそのUUIDとデプロイ時に指定されたオプションのタグ（またはエイリアス）によって識別されます。

In the case of an online model, the client service sends the feature vector along with the model UUID or model tag that it wants to use; in the case of a tag, the container will generate the prediction using the model most recently deployed to that tag. 
オンラインモデルの場合、クライアントサービスは使用したいモデルUUIDまたはモデルタグとともに特徴ベクトルを送信します。タグの場合、コンテナはそのタグに最近デプロイされたモデルを使用して予測を生成します。

In the case of batch models, all deployed models are used to score each batch data set and the prediction records contain the model UUID and optional tag so that consumers can filter as appropriate. 
バッチモデルの場合、すべてのデプロイされたモデルが各バッチデータセットをスコアリングするために使用され、予測レコードにはモデルUUIDとオプションのタグが含まれているため、消費者は適切にフィルタリングできます。

If both models have the same signature (i.e. expect the same set of features) when deploying a new model to replace an old model, users can deploy the new model to the same tag as the old model and the container will start using the new model immediately. 
新しいモデルを古いモデルに置き換えるためにデプロイする際に、両方のモデルが同じシグネチャ（つまり、同じ特徴のセットを期待する）を持っている場合、ユーザーは新しいモデルを古いモデルと同じタグにデプロイでき、コンテナは新しいモデルを直ちに使用し始めます。

This allows customers to update their models without requiring a change in their client code. 
これにより、顧客はクライアントコードの変更を必要とせずにモデルを更新できます。

Users can also deploy the new model using just its UUID and then modify a configuration in the client or intermediate service to gradually switch traffic from the old model UUID to the new one. 
ユーザーは新しいモデルをそのUUIDだけを使用してデプロイし、その後、クライアントまたは中間サービスの構成を変更して、古いモデルUUIDから新しいモデルUUIDにトラフィックを徐々に切り替えることもできます。

For A/B testing of models, users can simply deploy competing models either via UUIDs or tags and then use Uber’s experimentation framework from within the client service to send portions of the traffic to each model and track performance metrics. 
モデルのA/Bテストの場合、ユーザーはUUIDまたはタグを介して競合するモデルをデプロイし、クライアントサービス内からUberの実験フレームワークを使用して各モデルにトラフィックの一部を送信し、パフォーマンスメトリックを追跡できます。

#### Scale and latency スケールとレイテンシ

Since machine learning models are stateless and share nothing, they are trivial to scale out, both in online and offline serving modes. 
機械学習モデルはステートレスで何も共有しないため、オンラインおよびオフラインの提供モードの両方でスケールアウトするのは簡単です。

In the case of online models, we can simply add more hosts to the prediction service cluster and let the load balancer spread the load. 
オンラインモデルの場合、予測サービスクラスターにホストを追加し、ロードバランサーに負荷を分散させることができます。

In the case of offline predictions, we can add more Spark executors and let Spark manage the parallelism. 
オフライン予測の場合、より多くのSparkエグゼキュータを追加し、Sparkに並列処理を管理させることができます。

Online serving latency depends on model type and complexity and whether or not the model requires features from the Cassandra feature store. 
オンライン提供のレイテンシは、モデルのタイプと複雑さ、モデルがCassandraフィーチャーストアから特徴を必要とするかどうかに依存します。

In the case of a model that does not need features from Cassandra, we typically see P95 latency of less than 5 milliseconds (ms). 
Cassandraから特徴を必要としないモデルの場合、通常、P95レイテンシは5ミリ秒（ms）未満です。

In the case of models that do require features from Cassandra, we typically see P95 latency of less than 10ms. 
Cassandraから特徴を必要とするモデルの場合、通常、P95レイテンシは10ms未満です。

The highest traffic models right now are serving more than 250,000 predictions per second. 
現在、最もトラフィックの多いモデルは、250,000件以上の予測を毎秒提供しています。

#### Monitor predictions 予測の監視

When a model is trained and evaluated, historical data is always used. 
モデルがトレーニングされ評価されるとき、常に歴史的データが使用されます。

To make sure that a model is working well into the future, it is critical to monitor its predictions so as to ensure that the data pipelines are continuing to send accurate data and that production environment has not changed such that the model is no longer accurate. 
モデルが将来も正常に機能していることを確認するためには、その予測を監視し、データパイプラインが正確なデータを送信し続けていること、そして生産環境が変わってモデルがもはや正確でなくなっていないことを確認することが重要です。

To address this, Michelangelo can automatically log and optionally hold back a percentage of the predictions that it makes and then later join those predictions to the observed outcomes (or labels) generated by the data pipeline. 
これに対処するために、Michelangeloは自動的に予測の一部をログに記録し、オプションで保持し、その後、これらの予測をデータパイプラインによって生成された観測結果（またはラベル）に結合することができます。

With this information, we can generate ongoing, live measurements of model accuracy. 
この情報を使用して、モデルの精度の継続的なライブ測定を生成できます。

In the case of a regression model, we publish R-squared/coefficient of determination, root mean square logarithmic error (RMSLE), root mean square error (RMSE), and mean absolute error metrics to Uber’s time series monitoring systems so that users can analyze charts over time and set threshold alerts, as depicted below: 
回帰モデルの場合、R二乗/決定係数、平方根平均対数誤差（RMSLE）、平方根平均二乗誤差（RMSE）、および平均絶対誤差メトリックをUberの時系列監視システムに公開し、ユーザーが時間の経過に伴ってチャートを分析し、しきい値アラートを設定できるようにします。以下に示します。

coefficient of determination
決定係数

root mean square logarithmic error
平方根平均対数誤差

root mean square error
平方根平均二乗誤差

mean absolute error metrics
平均絶対誤差メトリック

#### Management plane, API, and web UI 管理プレーン、API、およびWeb UI

The last important piece of the system is an API tier. 
システムの最後の重要な部分はAPI層です。

This is the brains of the system. 
これはシステムの中枢です。

It consists of a management application that serves the web UI and network API and integrations with Uber’s system monitoring and alerting infrastructure. 
これは、Web UIとネットワークAPIを提供する管理アプリケーションと、Uberのシステム監視およびアラートインフラストラクチャとの統合で構成されています。

This tier also houses the workflow system that is used to orchestrate the batch data pipelines, training jobs, batch prediction jobs, and the deployment of models both to batch and online containers. 
この層には、バッチデータパイプライン、トレーニングジョブ、バッチ予測ジョブ、およびバッチおよびオンラインコンテナへのモデルのデプロイメントを調整するために使用されるワークフローシステムも含まれています。

Users of Michelangelo interact directly with these components through the web UI, the REST API, and the monitoring and alerting tools. 
Michelangeloのユーザーは、Web UI、REST API、および監視およびアラートツールを介してこれらのコンポーネントと直接対話します。



### Building on the Michelangelo platform
### Michelangeloプラットフォームの構築

Building on the Michelangelo platform
Michelangeloプラットフォームの構築

In the coming months, we plan to continue scaling and hardening the existing system to support both the growth of our set of customer teams and Uber’s business overall. 
今後数ヶ月で、私たちは既存のシステムのスケーリングと強化を続け、顧客チームの成長とUber全体のビジネスをサポートする計画です。

As the platform layers mature, we plan to invest in higher level tools and services to drive democratization of machine learning and better support the needs of our business:
プラットフォームのレイヤーが成熟するにつれて、私たちは機械学習の民主化を推進し、ビジネスのニーズをより良くサポートするために、より高レベルのツールとサービスに投資する計画です：

- AutoML. 
- AutoML。 

This will be a system for automatically searching and discovering model configurations (algorithm, feature sets, hyper-parameter values, etc.) that result in the best performing models for given modeling problems. 
これは、特定のモデリング問題に対して最もパフォーマンスの良いモデルを生成するモデル構成（アルゴリズム、特徴セット、ハイパーパラメータ値など）を自動的に検索し発見するシステムです。

The system would also automatically build the production data pipelines to generate the features and labels needed to power the models. 
このシステムは、モデルを動かすために必要な特徴とラベルを生成するための生産データパイプラインも自動的に構築します。

We have addressed big pieces of this already with our Feature Store, our unified offline and online data pipelines, and hyper-parameter search feature. 
私たちはすでにFeature Store、統合されたオフラインおよびオンラインデータパイプライン、ハイパーパラメータ検索機能を使用して、この大部分に対処しています。

We plan to accelerate our earlier data science work through AutoML. 
私たちはAutoMLを通じて以前のデータサイエンスの作業を加速する計画です。

The system would allow data scientists to specify a set of labels and an objective function, and then would make the most privacy-and security-aware use of Uber’s data to find the best model for the problem. 
このシステムは、データサイエンティストが一連のラベルと目的関数を指定できるようにし、その後、Uberのデータを最もプライバシーとセキュリティを考慮した形で使用して問題に最適なモデルを見つけます。

The goal is to amplify data scientist productivity with smart tools that make their job easier.
目標は、データサイエンティストの生産性を向上させ、彼らの仕事を容易にするスマートツールを提供することです。

- Model visualization. 
- モデルの可視化。

Understanding and debugging models is increasingly important, especially for deep learning. 
モデルを理解しデバッグすることはますます重要になっており、特に深層学習においてはそうです。

While we have made some important first steps with visualization tools for tree-based models, much more needs to be done to enable data scientists to understand, debug, and tune their models and for users to trust the results. 
私たちは木構造モデルの可視化ツールでいくつかの重要な第一歩を踏み出しましたが、データサイエンティストがモデルを理解し、デバッグし、調整できるようにし、ユーザーが結果を信頼できるようにするためには、さらに多くの作業が必要です。

- Online learning. 
- オンライン学習。

Most of Uber’s machine learning models directly affect the Uber product in real time. 
Uberの機械学習モデルのほとんどは、リアルタイムでUberの製品に直接影響を与えます。

This means they operate in the complex and ever-changing environment of moving things in the physical world. 
これは、物理的な世界で物を移動させるという複雑で常に変化する環境で動作することを意味します。

To keep our models accurate as this environment changes, our models need to change with it. 
この環境が変化するにつれてモデルの精度を保つために、私たちのモデルもそれに合わせて変化する必要があります。

Today, teams are regularly retraining their models in Michelangelo. 
現在、チームはMichelangeloで定期的にモデルを再訓練しています。

A full platform solution to this use case involves easily updateable model types, faster training and evaluation architecture and pipelines, automated model validation and deployment, and sophisticated monitoring and alerting systems. 
このユースケースに対する完全なプラットフォームソリューションは、簡単に更新可能なモデルタイプ、より迅速なトレーニングおよび評価アーキテクチャとパイプライン、自動化されたモデル検証とデプロイメント、そして高度な監視およびアラートシステムを含みます。

Though a big project, early results suggest substantial potential gains from doing online learning right. 
大きなプロジェクトではありますが、初期の結果はオンライン学習を正しく行うことで大きな潜在的利益が得られることを示唆しています。

- Distributed deep learning. 
- 分散深層学習。

An increasing number of Uber’s machine learning systems are implementing deep learning technologies. 
Uberの機械学習システムの数が増えるにつれて、深層学習技術が実装されています。

The user workflow of defining and iterating on deep learning models is sufficiently different from the standard workflow such that it needs unique platform support. 
深層学習モデルを定義し反復するユーザーワークフローは、標準的なワークフローとは十分に異なるため、独自のプラットフォームサポートが必要です。

Deep learning use cases typically handle a larger quantity of data, and different hardware requirements (i.e. GPUs) motivate further investments into distributed learning and a tighter integration with a flexible resource management stack. 
深層学習のユースケースは通常、より大量のデータを扱い、異なるハードウェア要件（つまり、GPU）が分散学習へのさらなる投資と柔軟なリソース管理スタックとの緊密な統合を促進します。

If you are interesting in tackling machine learning challenges that push the limits of scale, consider applying for a role on our team! 
スケールの限界を押し広げる機械学習の課題に取り組むことに興味がある場合は、私たちのチームの役割に応募することを検討してください！

Jeremy Hermann
Jeremy Hermann

Jeremy Hermann is an engineering manager on Uber's Michelangelo team. 
Jeremy HermannはUberのMichelangeloチームのエンジニアリングマネージャーです。

Posted by Jeremy Hermann, Mike Del Balso
投稿者：Jeremy Hermann、Mike Del Balso

Data / ML
データ / ML



### Related articles 関連記事



### Advancing Invoice Document Processing at Uber using GenAI
ウーバーにおけるGenAIを用いた請求書文書処理の進展
April 17 / Global
4月17日 / グローバル



### Uber’s Journey to Ray on Kubernetes: Resource Management
### UberのKubernetes上のRayへの旅: リソース管理

April 10 / Global
4月10日 / グローバル



### Uber’s Journey to Ray on Kubernetes: Ray Setup
UberのKubernetes上のRayへの旅: Rayのセットアップ
April 3 / Global
4月3日 / グローバル



### Enhancing Personalized CRM Communication with Contextual Bandit Strategies
パーソナライズされたCRMコミュニケーションを文脈バンディット戦略で強化する

March 27 / Global
3月27日 / グローバル



### How Uber Uses Ray® to Optimize the Rides Business
### UberがどのようにRay®を使用してライドビジネスを最適化しているか
January 9 / Global
1月9日 / グローバル



## Most popular 最も人気のある

Transit, Universities
交通機関、大学

March 3/Global
3月3日/グローバル



### A beginner’s guide to Uber vouchers for riders 初心者向けのライダー向けUberバウチャーガイド

Engineering, Backend エンジニアリング、バックエンド  
March 13/Global 3月13日/グローバル



### Automating Efficiency of Go programs with Profile-Guided Optimizations
Goプログラムの効率をプロファイルガイド最適化で自動化する
Engineering, Backend, Data / ML, Uber AI
エンジニアリング、バックエンド、データ / ML、Uber AI
March 27/Global
3月27日/グローバル



### Enhancing Personalized CRM Communication with Contextual Bandit Strategies
パーソナライズされたCRMコミュニケーションを文脈バンディット戦略で強化する

Transit, Universities
トランジット、大学

April 2/Global
4月2日/グローバル



### How medical schools support the next generation of doctors with Uber

医学校が次世代の医師をUberで支援する方法

View more stories
さらにストーリーを見る

Visit Help Center
ヘルプセンターを訪問

- About us
- 私たちについて
- Our offerings
- 提供サービス
- Newsroom
- ニュースルーム
- Investors
- 投資家
- Blog
- ブログ
- Careers
- キャリア
- Uber AI
- Uber AI
- Gift cards
- ギフトカード

About us
私たちについて

Our offerings
提供サービス

Newsroom
ニュースルーム

Investors
投資家

Blog
ブログ

Careers
キャリア

Uber AI
Uber AI

Gift cards
ギフトカード

- Ride
- 乗車
- Drive
- ドライブ
- Deliver
- 配達
- Eat
- 食事
- Uber for Business
- ビジネス向けUber
- Uber Freight
- Uber Freight

Ride
乗車

Drive
ドライブ

Deliver
配達

Eat
食事

Uber for Business
ビジネス向けUber

Uber Freight
Uber Freight

- Safety
- 安全
- Sustainability
- 持続可能性

Safety
安全

Sustainability
持続可能性

- Reserve
- 予約
- Airports
- 空港
- Cities
- 都市

Reserve
予約

Airports
空港

Cities
都市

- facebook
- フェイスブック
- twitter
- ツイッター
- youtube
- ユーチューブ
- linkedin
- リンクトイン
- instagram
- インスタグラム

- GlobeEnglish
- GlobeEnglish
- Location markerTokyo
- 場所マーカー東京
Tokyo
東京

©2025Uber Technologies Inc.
©2025 Uber Technologies Inc.

©2025
©2025

- Privacy
- プライバシー
- Accessibility
- アクセシビリティ
- Terms
- 利用規約

Privacy
プライバシー

Accessibility
アクセシビリティ

Terms
利用規約



## Select your preferred language 言語を選択してください

English
英語



## Sign up to drive ドライブにサインアップする



## Sign up to ride サインアップして乗る

- ProductsRideExperiences and information for people on the moveBusinessTransforming the way companies move and feed their peopleTransitExpanding the reach of public transportation
- 製品乗る体験と移動する人々のための情報ビジネス企業が人々を移動させ、食事を提供する方法を変革する交通公共交通機関の範囲を拡大する
- RideExperiences and information for people on the move
- 乗る体験と移動する人々のための情報
- BusinessTransforming the way companies move and feed their people
- ビジネス企業が人々を移動させ、食事を提供する方法を変革する
- TransitExpanding the reach of public transportation
- 交通公共交通機関の範囲を拡大する
- CompanyCareersExplore how Uber employees from around the globe are helping us drive the world forward at work and beyondEngineeringThe technology behind Uber EngineeringNewsroomUber news and updates in your countryUber.comProduct, how-to, and policy content—and more
- 会社キャリア世界中のUberの従業員がどのように私たちが仕事やその先で世界を前進させる手助けをしているかを探るエンジニアリングUberエンジニアリングの背後にある技術ニュースルームあなたの国のUberのニュースと更新Uber.com製品、ハウツー、ポリシーコンテンツなど
- CareersExplore how Uber employees from around the globe are helping us drive the world forward at work and beyond
- キャリア世界中のUberの従業員がどのように私たちが仕事やその先で世界を前進させる手助けをしているかを探る
- EngineeringThe technology behind Uber Engineering
- エンジニアリングUberエンジニアリングの背後にある技術
- NewsroomUber news and updates in your country
- ニュースルームあなたの国のUberのニュースと更新
- Uber.comProduct, how-to, and policy content—and more
- Uber.com製品、ハウツー、ポリシーコンテンツなど



### Products 製品

- RideExperiences and information for people on the move
- Ride 移動中の人々のための体験と情報
- BusinessTransforming the way companies move and feed their people
- Business 企業が人々を移動させ、食事を提供する方法を変革する
- TransitExpanding the reach of public transportation
- Transit 公共交通機関の利用範囲を拡大する



### Company 会社

- CareersExplore how Uber employees from around the globe are helping us drive the world forward at work and beyond
- Careers
世界中のUberの従業員が、仕事やその先で私たちが世界を前進させる手助けをしている様子を探ります。

- EngineeringThe technology behind Uber Engineering
- Engineering
Uberエンジニアリングの背後にある技術。

- NewsroomUber news and updates in your country
- Newsroom
あなたの国におけるUberのニュースと最新情報。

- Uber.comProduct, how-to, and policy content—and more
- Uber.com
製品、使い方、ポリシーに関するコンテンツなど。



## Select your preferred language 言語を選択してください

English
英語



## Sign up to drive ドライブにサインアップする



## Sign up to ride 乗車のためのサインアップ
