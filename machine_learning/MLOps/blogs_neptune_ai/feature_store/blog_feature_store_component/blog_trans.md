<!-- 後で読む -->

## 0.1. link リンク

https://neptune.ai/blog/data-ingestion-and-feature-store-component-mlops-stack
https://neptune.ai/blog/data-ingestion-and-feature-store-component-mlops-stack

## 0.2. title タイトル

How to Solve the Data Ingestion and Feature Store Component of the MLOps Stack
MLOpsスタックのデータ・インジェストとフィーチャー・ストアのコンポーネントを解決する方法

# 1. Introduction はじめに

As every practitioner in the Data Science space knows, Data is the primary fuel for Machine Learning.
データ・サイエンス分野の実務者なら誰もが知っているように、データは機械学習の主要な燃料である。
A trustworthy data sourcing and high-quality data collection and processing can empower a vast range of potential ML use cases.
信頼できるデータソーシングと質の高いデータ収集・処理によって、**MLの潜在的なユースケースを大幅に拡大することができる**。
But having a well-governed Data Warehouse requires a thorough devotion from every team in the organization to look after and curate every data point that they produce, ingest, analyze or exploit.
しかし、きちんと管理されたデータウェアハウスを持つには、組織内のすべてのチームが、作成、取り込み、分析、利用するすべてのデータポイントを管理し、キュレーションすることに徹底して取り組む必要がある。
Data quality responsibility spreads across everyone.
データ品質に対する責任は全員に及ぶ。
It is not only dependent on the Data Engineering team.
データ・エンジニアリング・チームだけに依存しているわけではない。

![Main properties of Data Quality](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-1.png?resize=668%2C353&ssl=1)

The most common data architecture nowadays in organizations is Lambda Architecture.
現在、組織で最も一般的なデータ・アーキテクチャは**Lambda Architecture**だ。
It is characterized by having independent batch and streaming pipelines ingesting data into the Data Lake, which consists of a landing or raw stage where ELT processes dump raw data objects, such as events or database record dumps.
その特徴は、**バッチとストリーミングの独立したパイプラインがデータをデータレイクに取り込む**ことだ、
データレイクは、ELTプロセスがイベントやデータベースレコードダンプなどのローデータオブジェクトをダンプするランディングまたはローステージで構成される。

- メモ: Lambda Architecture
  - バッチ処理とストリーム処理の両方の手法を活用する、データ処理のアーキテクチャ。
  - 3つの層から構成される: batch layer, speed layer, serving layer

This raw data is later ingested and wrangled into more organized Data Lake tables (Parquet files, for example), and then it is enriched to be ingested into the Data Warehouse.
この未加工データは後にインジェストされ、より整理されたデータレイクのテーブル（例えばパーケットファイル）に取り込まれ、データウェアハウスにインジェストされるためにエンリッチされる。(Data lakeがrawデータが入るやつで、DWが各usecase用に加工されたデータが入るやつ??)
The data that gets into the DW is logically organised information for different business domains called Data Marts.
DWに取り込まれるデータは、データ・マートと呼ばれる**ビジネス・ドメインごとに論理的に整理された情報**である。(↑なんとなく認識合ってた...!data martは、data lakeやDWのようなデータの置き場というよりは、データそのもの??)
These data marts are easily queried by Data Analysts and explored by Business Stakeholders.
これらのデータマートは、データアナリストによって容易に照会され、ビジネス利害関係者によって探索される。
Each data mart could be related to different business units or product domains (Marketing, Subscriptions, Registrations, Product, Users …).
各データマートは、異なるビジネスユニットまたは製品ドメイン（マーケティング、サブスクリプション、登録、製品、ユーザー...）に関連する可能性があります。

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-2.png?resize=840%2C411&ssl=1)

There are also other reference architecture patterns such as the Kappa or Delta, the latter getting a lot of traction with commercial products such as Databricks and Delta Lake.
KappaやDeltaのような**リファレンス・アーキテクチャ・パターン**(?)もある、
後者はDatabricksやDelta Lakeのような商用製品で多くの支持を得ている。

These foundational data architectural patterns have paved the way for analytical workloads.
これらの基本的なデータアーキテクチャパターンは、分析ワークロードへの道を開いた。
OLAP databases and processing engines for Big Data, such as Spark and Dask, among others, have enabled the decoupling of the storage and computing hardware, allowing Data practitioners to interact with massive amounts of data for doing Data Analytics and Data Science.
OLAPデータベースや、SparkやDaskなどのビッグデータ処理エンジンは、ストレージとコンピューティングハードウェアの分離を可能にし、データ実務者がデータ分析やデータサイエンスを行うために大量のデータを扱うことを可能にした。

With the rise of MLOps, DataOps, and the importance of Software Engineering in production Machine Learning, different startups and products have emerged to solve the issue of serving features such as Tecton, HopsWorks, Feast, SageMaker Feature Store, Databricks Feature Store, Vertex AI Feature Store… (check out Featurestore.org to see all the players in this field).
MLOps、DataOpsの台頭、そしてプロダクション機械学習におけるソフトウェアエンジニアリングの重要性に伴い、Tecton、HopsWorks、Feast、**SageMaker Feature Store**、Databricks Feature Store、Vertex AI Feature Store...など、機能提供の問題を解決するためにさまざまな新興企業や製品が登場している（この分野のすべてのプレイヤーを見るにはFeaturestore.orgをチェック）。

Furthermore, every company doing production data science at a considerable scale, if not using one of the tools named before, has built their in-house feature store (e.g., Uber was of the first to publish their own approach for building an ML platform, followed by Airbnb).
さらに、かなりの規模でプロダクション・データ・サイエンスを実施している企業は、先に挙げたツールのいずれかを使用していないとしても、**自社でフィーチャーストアを構築している**（例えば、[MLプラットフォームを構築するための独自のアプローチを最初に公開したのはUber](https://www.uber.com/blog/michelangelo-machine-learning-platform/)であり、Airbnbがそれに続く）。

In this article, we will explain some of the concepts and issues that feature stores solve as if it was an in-house platform.
本記事では、**フィーチャーストアが自社プラットフォームであるかのように解決する概念と課題のいくつか**を説明する。
This is because we think it is easier to understand the underlying components and the conceptual and technical relationships among them.
これは、基礎となる構成要素や、構成要素間の概念的・技術的な関係を理解しやすいと考えるからである。
We won’t dive deep into commercial products.
市販品については深入りしない。

We will also discuss the tension between build and buy, which is a hot topic among practitioners in the industry today and what’s the best way to approach this decision.
また、現在業界の実務家の間で話題となっている、ビルドとバイの間の緊張感と、この決断にアプローチする最善の方法についても議論する。

Bookmark for later
後でブックマークする

[How to Solve the Model Serving Component of the MLOps Stack](https://neptune.ai/blog/model-serving-component-mlops-stack)
[MLOpsスタックのモデル・サーヴィング・コンポーネントの解決方法](https://neptune.ai/blog/model-serving-component-mlops-stack)

# 2. What is a feature store? フィーチャーストアとは何か？

Last year, some blogs and influential people in the ML world named 2021 as the year of the feature store.
昨年、いくつかのブログやML界で影響力のある人々は、2021年をフィーチャーストアの年と命名した。
We will argue in the next sections the reason behind this.
その理由については、次節で論じる。
But then, what is a feature store?
しかし、ではフィーチャーストアとは何なのか？

A short definition given by Featurestore.org is:
Featurestore.orgによる簡単な定義は以下の通り:

> “A data management layer for machine learning that allows to share & discover features and create more effective machine learning pipelines.”
> 特徴量を共有・発見し、より効果的な機械学習パイプラインを作成できる機械学習用データ管理レイヤー"

That’s pretty accurate.
かなり正確だ。
To briefly expand on some details, feature stores are composed of a set of technological, architectural, conceptual, and semantic components that enable ML practitioners to create, ingest, discover and fetch features for doing offline experiments and developing online production services.
簡単に詳細を説明すると、フィーチャーストアは技術的、アーキテクチャ的、概念的、セマンティックなコンポーネントで構成され、**MLの実務家がオフラインで実験したり、オンラインでプロダクションサービスを開発したりするために、フィーチャーをcreate(作成)、ingest(データをfeature storeに追加したりre-uploadしたりする)、discover(利用可能な特徴量を探す)、fetch(feature storeから取得する)することを可能にする**。

## 2.1. Components of a feature store フィーチャーストアの構成要素

![Components of a feature store](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-3.png?ssl=1)

We should start defining what is a feature vector as it’s the core entity that feature stores deal with.
フィーチャーストアが扱う核となるエンティティなので、**フィーチャーベクターとは何かを定義すること**から始めるべきだ。

- Feature Vector: This is a data element that contains an entity identifier and a set of properties or characteristics that describe that element at a certain point in time. For example, the entity identifier can be a user ID and the properties could contain the following values: (time_since_registration, n_purchases, ltv_value, is_free_trial, average_purchases_per_month, accumulated_purchases, last_purchase_ts etc)
- フィーチャー・ベクター：これは、**entity識別子と、ある時点におけるそのelementを記述するpropertiesまたはcharacteristicsの集合を含む data elements**である。
  - ex.) entity識別子はユーザIDであり、プロパティには以下の値が含まれる：(time_since_registration, n_purchases, ltv_value, is_free_trial, average_purchases_per_month, accumulated_purchases, last_purchase_ts etc.)
  - (想像した通りの特徴量ベクトルっぽい?:thinking:)

Let’s explain now which are the different storage components that host these feature vectors:
では、これらの特徴ベクトルをホストするさまざまな**storage components**を説明しよう:

- **Offline Store**: This is meant to be an analytical database that can ingest, store and serve feature vectors for offline workloads such as data science experiments or batch production jobs. In general, each row contains a feature vector uniquely identified by the entity ID and a given timestamp. This component is usually materialized as S3, Redshift, BigQuery, Hive, etc. オフライン・ストア: これは、データサイエンス実験やバッチ生産ジョブのようなオフラインのワークロードのために、特徴ベクトルを取り込み、保存し、提供できる分析データベースである。 一般に、各行には、エンティティIDと所定のタイムスタンプによって一意に識別される特徴ベクトルが含まれる。 このコンポーネントは通常、S3、Redshift、BigQuery、Hiveなどとして実体化される。

- **Online Store**: Also referred to as hot data, this storage layer is meant to serve features for low latency prediction services. This database is now used to fetch features at millisecond speed. Redis, DynamoDB, or Cassandra are the common candidates to play this role. Key-Value databases are the best option as complex queries and join are not often needed at runtime. オンラインストア: ホットデータとも呼ばれるこのストレージレイヤーは、低遅延予測サービスのための機能を提供する。 **このデータベースは現在、ミリ秒単位のスピードで特徴量をfetchするために使われている**。 Redis、DynamoDB、Cassandraがこの役割を果たす一般的な候補だ。 キー・バリュー・データベースは、複雑なクエリーやジョインが実行時にあまり必要とされないため、最良の選択肢である。

- **Feature Catalog or Registry**: Ideally, this is presented as a nice UI that enables features and training datasets discoverability. フィーチャー・カタログまたはレジストリ: 理想的には、フィーチャーとトレーニングデータセットの発見を可能にする素晴らしいUIとして提示される。

- **Feature Store SDK**: This is a Python library that abstracts access patterns for online and offline stores. フィーチャーストアSDK：オンラインストアとオフラインストアのアクセスパターンを抽象化したPythonライブラリです。

- **Metadata Management**: This component is used to track access from different users or pipelines, ingestion processes, schema changes, and this type of information. メタデータ管理：このコンポーネントは、異なるユーザーやパイプラインからのアクセス、取り込みプロセス、スキーマの変更、およびこの種の情報を追跡するために使用される。

- **Offline and Online Serving API**: This is a proxy service that sits in between the SDK and the online and feature hardware to facilitate feature access. オフラインおよびオンライン・サーヴィングAPI：これは、SDKとオンラインおよび機能ハードウェアの間に位置し、機能へのアクセスを容易にするプロキシ・サービスです。

In the following chronological diagram, we can see a summary of the key milestones around feature store since 2017, when Uber released its famous Michelangelo.
以下の時系列図では、ウーバーが有名なミケランジェロをリリースした2017年以降、フィーチャーストアをめぐる主要なマイルストーンをまとめて見ることができる。
A couple of years later, after several commercial and OS products launched, we’ve already seen a wide acceptance of the concept of feature store by industry practitioners.
それから数年後、いくつかの商用製品やOS製品が発売された後、我々はすでに業界関係者にフィーチャーストアのコンセプトが広く受け入れられていることを目の当たりにした。
Several organizations such as featurestore.org and mlops.community have emerged in response to this.
これに対して、featurestore.orgやmlops.communityなどいくつかの組織が立ち上がった。

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-4.png?ssl=1)

In relationship with MLOps, feature stores are themselves affected and affect other components of the stack such as the Data Warehouse, Data Lake, the data job schedulers, production databases, etc.
MLOpsとの関係では、フィーチャーストアはそれ自体が影響を受け、データウェアハウス、データレイク、データジョブスケジューラ、プロダクションデータベースなどのスタックの他のコンポーネントに影響を与える。
as well.
も同様だ。
We will discuss this relationship in detail later, i.e., where does a feature store sit in the big picture of the MLOps framework?
**MLOpsフレームワークの全体像の中で、フィーチャーストアはどのような位置づけにあるのか**？

Now, let’s discuss some of the major issues that ML Engineers face around production feature engineering.
それでは、MLエンジニアが直面するproduction環境での特徴量エンジニアリングに関する主な問題について説明しよう。

# 3. Hassles around feature store feature store周辺での手間

## 3.1. Standardization of features ingestion and fetching 特徴量のingestionとfetchingの標準化

Before the existence of a proper feature store, each data science team stored and fetched features using very different tools.
**適切なフィーチャーストアが存在する以前は、データサイエンスチームはそれぞれ全く異なるツールを使ってフィーチャーを保存し、フェッチしていた**。
These kinds of jobs have been treated traditionally as part of Data Engineering pipelines.
この種の仕事は従来、データエンジニアリングのパイプラインの一部として扱われてきた。
Therefore, the libraries, SDKs, and tooling around these jobs are the ones used by data engineers.
したがって、これらのジョブに関連するライブラリ、SDK、ツールは、データエンジニアが使用するものである。
They can be quite diverse depending on the team’s expertise, maturity level, and background.
チームの専門知識、成熟度、経歴によって、その内容はかなり多岐にわたる。

For example, you could see the following situation in the same organization:
例えば、同じ組織で次のような状況が考えられる:

- Team A: The team is not very knowledgeable in data engineering. They use bare pandas and SQL scripts with psycopg connectors to store offline features in Redshift and boto to store online features in DynamoDb. チームA：このチームはデータエンジニアリングの知識があまりない。 Redshiftにオフラインフィーチャーを保存するためにpsycopgコネクタを持つベアpandasとSQLスクリプトを使用し、DynamoDbにオンラインフィーチャーを保存するためにbotoを使用しています。

- Team B: The team is mature and autonomous. They built a library for abstracting connections to several data sources using sqlalchemy or PySpark for big data jobs. They also have custom wrappers for sending data to DynamoDb and other hot databases. チームB：チームは成熟し、自律している。 彼らはビッグデータジョブのために、sqlalchemyやPySparkを使って複数のデータソースへの接続を抽象化するライブラリを構築した。 また、DynamoDbやその他のホットなデータベースにデータを送信するためのカスタムラッパーもある。

(要はチーム毎に、特徴量データのingestionとfetchingの方法が異なる、って状況かな:thinking:)

This is very typical in large organizations where the ML teams are not fully centralized, or ML cross-teams don’t exist.
**これは、MLチームが完全に中央集権化されていなかったり、MLのクロスチームが存在しないような大組織ではよくあること**だ。

Teams operating with the same databases over different projects tend to build wrappers around them so that they can abstract the connectors and encapsulate common utilities or domain definitions.
異なるプロジェクトで同じデータベースを使用しているチームは、コネクタを抽象化し、共通のユーティリティやドメイン定義をカプセル化できるように、その周りにラッパーを構築する傾向がある。
This problem is already solved by Team B.
この問題はチームBがすでに解決している。
But Team A is not so skilled, and they might develop another in-house library to work with their features in a simpler way.
しかし、チームAはそれほど熟練していないので、よりシンプルな方法で自分たちの機能と連携する別の社内ライブラリを開発するかもしれない。

This causes friction among teams because they want to impose their tool across the organization.
そのため、**組織全体に自分たちのツールを押し付けようとするため、チーム間に摩擦が生じる**。
It also lowers productivity levels across teams because each one is reinventing the wheel in its own manner, coupling developers to projects.
また、**各チームが独自のやり方で車輪を再発明し、開発者をプロジェクトに密結合させるため、チーム全体の生産性レベルも低下する**。

By introducing a Feature Store SDK, both teams could leverage the same interface for interacting with Redshift and DynamoDb, and other data sources too.
フィーチャーストアSDKを導入することで、**両チームはRedshiftとDynamoDb、そして他のデータソースとやり取りするために同じインターフェイスを活用することができる**。
The learning curve will be steeper for Team A, but they will maintain the same standard for operating them.
学習曲線はチームAにとってより険しいものになるだろうが、彼らは同じ基準で運用を続けるだろう。
So overall productivity will be increased.
だから、全体的な生産性は向上する。
This allows for better feature governance.
これにより、より優れた特徴量ガバナンスが可能になる。
SDKs usually hide other API calls to log user requests, and version datasets, allowing for rollbacks, etc.
SDKは通常、他のAPIコールを隠し、ユーザリクエストやバージョンデータセットを記録し、ロールバックなどを可能にする。

Most commercial feature stores provide specific SDKs for interacting with their central service.
ほとんどの商用フィーチャーストアは、**セントラル・サービスと相互作用するための特定のSDKを提供**している。(いいね!)
For example, in the next snippet, you could see how to build a dataset fetching features from Feast.
例えば、次のスニペットでは、Feastから特徴量をfetchしてデータセットを構築する方法を見ることができる。

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-5.png?resize=840%2C651&ssl=1)

This is not only valuable for standardizing feature store operations but also for abstracting the online and offline stores’ hardware.
これは**フィーチャーストアのオペレーションを標準化**するだけでなく、**オンラインストアとオフラインストアのハードウェアを抽象化**(??)する上でも価値がある。
Data Scientists don’t need to know if the offline store is a BigQuery or Redshift database.
**データサイエンティストは、オフラインストアがBigQueryデータベースかRedshiftデータベースかを知る必要はない**。
This is a great benefit as you could use a different source depending on the use case, data, etc.
ユースケースやデータなどに応じて異なるソースを使うことができるので、これは大きなメリットだ。

## 3.2. Time-travel data タイムトラベルデータ

If we want to predict whether a user will buy a product or not, we have to build a dataset with features until that specific moment.
ユーザが商品を買うか買わないかを予測したい場合、その特定の瞬間までの特徴量を持つデータセットを構築しなければならない。
We need to be very careful regarding not introducing future data as this can lead to Data Leakage.
データ漏えいにつながる可能性があるため、将来のデータを持ち込まないように細心の注意を払う必要がある。
But how?
でも、どうやって？

If we introduce future data into the training dataset with respect to each observation, the Machine Learning model will learn unreliable patterns.
もし各観測に関して将来のデータを訓練データセットに導入すれば、機械学習モデルは信頼できないパターンを学習することになる。(うんうん)
When putting the model into real-time production, it won’t have access to the same features (unless you can travel to the future), and its prediction capabilities will deteriorate.
そのモデルをリアルタイムの生産に投入すると、（未来に移動できない限り）同じ機能を利用できなくなり、予測能力が低下する。

Coming back to the example of the product purchase prediction, let’s say you want to use specific characteristics about the users, for example, the number of items saved in the cart.
商品購入予測の例に戻ると、例えば、カートに保存された商品の数など、ユーザに関する特定の特徴量を使用したいとします。
The training dataset will contain events about users who saw and bought the product (positive label) and users who saw but didn’t buy the product (negative label).
トレーニング・データセットには、商品を見て購入したユーザ（ポジティブ・ラベル）と、商品を見て購入しなかったユーザ（ネガティブ・ラベル）のイベントが含まれる。
If you want to use the number of items in the cart as a feature, you would need to query specifically for the events that log every item added to the cart within the same session and just before the purchase/seen event.
カートの中のアイテム数を機能として使用したい場合は、同じセッション内で、購入/見たイベントの直前にカートに追加されたすべてのアイテムをログに記録するイベントを特別にクエリする必要があります。

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-6.png?ssl=1)

Hence, when building such a dataset, we need to query specifically for the features that were available at that point in time with respect to each event.
したがって、このようなデータセットを構築する際には、各イベントに関して、その時点で利用可能であった特徴量を特別に照会する必要がある。
It’s necessary to have a representation of the world in which that event occurred.
その出来事が起こった世界の表現が必要なのだ。(オフラインでの実験の時とかのケースを想定してるのかな...! 過去のログデータで学習・評価する上で、その時点での特徴量を用意する必要がある、みたいな。)

### 3.2.1. How to have an accurate picture? 正確な写真を撮るには？

- **Log and wait**: You just have to log specific features, such as n_cumulative_items_in_the_cart, and then we’ll know how many items the user had at that point in time. The main drawback is that this feature collection strategy needs time to gather enough data points for the use case. But on the other hand, it is easy to implement. ログを取って待つ: n_cumulative_items_in_the_cartのような特定の機能をログに記録するだけで、その時点でユーザが持っていたアイテムの数を知ることができる。 主な欠点は、この特徴収集戦略では、ユースケースに十分なデータポイントを集めるのに時間がかかることだ。 しかし、その一方で導入は簡単だ。

- **Backfilling**: This technique basically aims to reconstruct the desired features at a given point in time. For example, by looking at logged events, we could add all the items added to the cart before each purchase. However, this might become very complex as we have to select the time window cutoff for every feature. These queries are commonly known as point-in-time joins. 埋め戻し：この技法は基本的に、ある時点における所望の特徴を再構築することを目的としている。 例えば、ログされたイベントを見ることで、各購入の前にカートに追加されたすべてのアイテムを追加することができる。 しかし、これは非常に複雑になる可能性がある。すべての特徴に対して時間窓のカットオフを選択しなければならないからだ。 これらのクエリは一般的にポイントインタイムジョインとして知られている。

- **Snapshotting**: It is based on dumping the state of a production database periodically. This allows having features at any given point in time, with the drawback that the data changes between consecutive snapshots wouldn’t be available. スナップショット：本番データベースの状態を定期的にダンプすることに基づく。 これにより、任意の時点の特徴を持つことができるが、連続したスナップショット間のデータ変化が利用できなくなるという欠点がある。

## 3.3. Features availability for production

Experienced ML engineers tend to think about what features are available at run time (online) when a new ML use case is proposed.
**経験豊富なMLエンジニアは、新しいMLユースケースが提案されると、実行時(オンライン)にどのような機能が利用可能かを考える傾向がある**。
Engineering the systems behind enabling features is the most time-consuming piece of the ML architecture in most cases.
ほとんどの場合、MLアーキテクチャの中で最も時間がかかるのは、特徴量を実現するシステムのエンジニアリングである。

Having an up-to-date feature vector ready to be fed to ML models to make a prediction is not an easy task.
MLモデルに予測をさせるために、**最新の**特徴ベクトルを用意することは簡単なことではない。
Lots of components are involved, and special care is required to glue them all together.
多くの部品が関わっており、それらを接着するには特別な注意が必要だ。

Features in production can come from very different sources.
プロダクションにおける特徴量は、実に**さまざまなソースからもたらされる**。(特に推論時の話っぽい!学習時はもう少しソースのバリエーションは減りそう...!:thinking:)
They can be fed to the algorithm within the request body parameters, they can be fetched from a specific API, retrieved from a SQL or NoSQL database, from a Kafka topic event, from a Key-Value store, or they can be computed and derived on-the-fly from other data.
それらは、リクエスト・ボディ・パラメーターの中でアルゴリズムに与えることもできるし、特定のAPIからフェッチすることも、SQLやNoSQLデータベースから取得することも、Kafkaトピック・イベントから取得することも、Key-Valueストアから取得することも、他のデータからその場で計算して導き出すこともできる。
Each of them implies different levels of complexity and resource capacity.
それぞれ、複雑さとリソースの容量が異なる。

### 3.3.1. What are these sources? その情報源とは？

1. Request Body Parameters リクエスト・ボディ・パラメータ

This is the simplest way of receiving features for prediction.
これは予測のための特徴量を受け取る最も簡単な方法である。
The responsibility of obtaining these features and passing them to the ML model is delegated to the client or consumer of the inference API Web Service.
これらの機能を取得し、MLモデルに渡す責任は、推論APIウェブサービスのクライアントまたはコンシューマに委ねられる。
Nevertheless, this is not the most common way of feeding features.
とはいえ、これは最も一般的な給餌方法ではない。
In fact, request parameters tend to contain unique identifiers that are needed to fetch feature vectors from other sources.
実際、リクエストパラメータには、他のソースから特徴ベクトルをフェッチするために必要な一意の識別子が含まれる傾向がある。(うんうん、user-idとか...!)
These are usually user IDs, content IDs, timestamps, search queries, etc.
これらは通常、ユーザーID、コンテンツID、タイムスタンプ、検索クエリなどである。

2. Databases データベース

Depending on the evolvability requirements of the features schemas and latency, features can be live in different databases such as Cassandra, DynamoDb, Redis, PostgreSQL, or any other fast NoSQL or SQL database.
機能スキーマの進化可能性の要件とレイテンシーに応じて、機能はCassandra、DynamoDb、Redis、PostgreSQL、またはその他の高速NoSQLまたはSQLデータベースなどの異なるデータベースでライブにすることができます。
Fetching these features from an online service is quite straightforward.
オンラインサービスからこれらの機能を取得するのは非常に簡単だ。
You can use any Python library like boto for DynamoDb, pyredis for Redis, psycopg2 for PostgreSQL, mysql-connector-python for MySQL, cassandra-driver for Cassandra, and so on.
DynamoDbにはboto、Redisにはpyredis、PostgreSQLにはpsycopg2、MySQLにはmysql-connector-python、Cassandraにはcassandra-driverなど、どんなPythonライブラリでも使うことができる。

![Redis database](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-7.png?ssl=1)

Each row in the database will have a primary key or index that will be available at runtime for each prediction request.
データベース内の各行は、各予測リクエストの実行時に利用可能な主キーまたはインデックスを持つ。
The rest of the columns or values will be the features that you can use.
残りの列や値は、あなたが使用できる特徴量になります。

To fill up these tables we can use different approaches depending on the nature of the features to compute:
これらのテーブルを埋めるため(=特徴量を作成・更新する為に)に、計算する特徴量の性質によって異なるアプローチを使うことができる:

- **Batch jobs**: These are compute-intensive, heavy, and “slow”, that’s why they only serve a certain type of features defined by how fresh they need to be. When building different use cases, you realise that not every model needs real-time features. If you’re using the average rating of a product, you don’t need to compute the average every second. Most of the features like this just need a daily computation. If the feature requires higher update frequency than 1 day, you should start thinking about a batch job. バッチジョブ：これらは計算集約的で、重く、"遅い"。そのため、**どれだけ新鮮である必要があるか**によって定義される、ある種の特徴量にのみ対応する。 さまざまなユースケースを構築するとき、すべてのモデルにリアルタイムの特徴量が必要なわけではないことに気づく。 商品の平均評価を使うのであれば、毎秒平均を計算する必要はない。 このような特徴量のほとんどは、日々の計算が必要なだけだ。 もし、その特徴量が1日以上の更新頻度を必要とするのであれば、バッチジョブについて考え始めるべきである。

![An exapmle of a batch processing](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-8.png?ssl=1)

Talking about common tech stacks, old friends come into play for serving different purposes and scales:
一般的な技術スタックといえば、さまざまな目的や規模に対応するために旧友たちが登場する: (workiflow engine的な話??)

- Airflow + DBT or Python is a great first start to schedule and run these jobs. Airflow + DBTまたはPythonは、これらのジョブをスケジューリングして実行するための素晴らしい最初のスタートです。

- If more scale is needed in terms of distributed memory, we can start thinking about Kubernetes Clusters to execute Spark or Dask jobs. 分散メモリの面でよりスケールが必要な場合は、SparkやDaskのジョブを実行するためのKubernetesクラスタについて考え始めることができる。

Some alternatives for orchestration tools are Prefect, Dagster, Luigi, or Flyte.
オーケストレーションツールの代替品としては、Prefect、Dagster、Luigi、Flyteなどがある。
Have a look at a comparison of Data Science orchestration and workflow tools.
データサイエンスの[オーケストレーションとワークフローツール](https://neptune.ai/blog/best-workflow-and-pipeline-orchestration-tools)の比較を見てみましょう。

- **Streaming Ingestion**: Features that need streaming or (near) real-time computations are time-sensitive. Common use cases that need real-time features are fraud detection, real-time product recommendation, predictive maintenance, dynamic pricing, voice assistants, chatbots, and more. For such use cases, we would need a very fast data transformation service. ストリーミング・インジェスト：ストリーミングや（リアルタイムに近い）計算を必要とする特徴量は、時間に敏感である。 リアルタイム機能を必要とする一般的なユースケースは、詐欺検出、リアルタイム製品推薦、予測メンテナンス、ダイナミックプライシング、音声アシスタント、チャットボットなどである。 このようなユースケースでは、非常に高速なデータ変換サービスが必要になる。

![Building ML pipeline with Feature](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-10.png?ssl=1)
Source

There are two important dimensions to take into account here – frequency and complexity.
ここで考慮すべき2つの重要な次元がある。
For example, computing the “standard deviation of the current price versus the average monthly price” on an individual transaction is both a real-time and complex aggregation.
例えば、個々の取引について「月平均価格に対する現在価格の標準偏差」を計算することは、リアルタイムかつ複雑な集計である。

![Amazon SageMaker Feature Store Streaming Ingestion](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-11.png?ssl=1)

Apart from having a streaming tool in place for collecting events (Kafka), we would also need a high-speed and scalable (to handle any volume of events per second) function-as-a-service (such as AWS Lambda) to read and process those events.
イベントを収集するためのストリーミング・ツール（Kafka）を用意する以外に、これらのイベントを読み込んで処理するために、高速でスケーラブルな（1秒間に大量のイベントを処理できる）function-as-a-service（AWS Lambdaなど）も必要だ。
More importantly, the transformation service needs to support aggregations, grouping, joins, custom functions, filters, sliding windows to calculate data over a given time period every X minutes or hours, etc.
さらに重要なことは、変換サービスは、集計、グループ化、結合、カスタム関数、フィルター、X分または時間ごとに指定された期間のデータを計算するスライディングウィンドウなどをサポートする必要があるということだ。

# 4. Where does the feature store sit in the MLOps architecture? フィーチャーストアはMLOpsアーキテクチャのどこに位置するのか？

The feature store is an inherent part of ML Platforms.
フィーチャーストアはMLプラットフォーム固有のものだ。
As said previously, it has been a part of it since the first ML models were put in production, but it wasn’t until a few years ago when the concept acquired its own identity within the MLOps world.
前述したように、feature storeは最初のMLモデルが生産されたときからその一部であったが、このコンセプトがMLOpsの世界で独自のアイデンティティを獲得したのは数年前のことである。

Features data sources can get tracked with Experiment Tracking tools such as Neptune, MLFlow, or SageMaker Experiments.
特徴量データソースは、Neptune、MLFlow、SageMaker ExperimentsなどのExperiment Trackingツールで追跡できます。
That is, let’s say you’re training a fraud detection model and you’ve used some shared Features that another team has built.
つまり、不正検知モデルをトレーニングしているときに、他のチームが構築した共有featureを使ったとしよう。
If you logged those features metadata as parameters, then they will be versioned along with your experiment results and code when tracking the experiments.
もし、これらのfeatureのメタデータをパラメータとして記録すれば、実験を追跡する際に、実験結果やコードと一緒にバージョン管理される。

Orchestrating Spark ML Pipelines and MLflow for Production
Spark MLパイプラインと本番用MLflowのオーケストレーション

The Killer Feature Store: Orchestrating Spark ML Pipelines and MLflow for Production | Source
キラーフィーチャーストア
Spark MLパイプラインとMLflowを本番環境でオーケストレーションする

Besides, they become a critical piece when the model is in the production stage.
その上、モデルが生産段階に入ると、重要なピースとなる。
There are several components that need to be synchronised and closely monitored when being live.
production環境では、**いくつかのコンポーネントを同期させ、綿密に監視する必要がある**。
If one fails, predictions could degrade pretty quickly.
どれかが失敗すれば、予測はあっという間に悪化する。(特徴量のcreate, ingestion, fetch, )
These components are the features computation & ingestion pipelines and features consumption from the production services.
**これらのコンポーネントは、特徴量計算とingestionパイプライン、およびプロダクションサービスからの特徴量消費**です。
The computation pipelines need to run at a specific frequency so that features’ freshness doesn’t affect the online predictions.
計算パイプラインは、特徴の鮮度がオンライン予測に影響を与えないように、特定の頻度で実行する必要がある。
E.g.: if a recommendation system needs to know the film you viewed yesterday, the feature pipeline should run before you go into the media streaming service again!
例えば、レコメンデーションシステムが、あなたが昨日見た映画を知る必要がある場合、あなたが再びメディアストリーミングサービスに入る前に、フィーチャーパイプラインが実行されなければならない！

# 5. How to implement a feature store? フィーチャーストアを実装するには？

In this section, we will discuss different architectures that can be implemented for different stages and sizes of Data Science teams.
このセクションでは、**データ・サイエンス・チームの段階や規模に応じて実装できるさまざまなアーキテクチャ**について説明する。
In this very nice article, you can see how the author uses the Hierarchy of Needs to very explicitly show which are the main pillars you need to solve.
[この素晴らしい記事](https://eugeneyan.com/writing/feature-stores/)では、著者が「ニーズの階層」を使って、解決すべき主要な柱がどれであるかを明確に示している。
He places the Access need, which encompasses transparency and lineage, as more foundational than Serving.
彼は、透明性と血統を包括するアクセスの必要性を、サービングよりも基礎的なものと位置づけている。
I don’t completely agree as the features availability in production unlocks higher business value.
本番で利用可能な特徴量は、より高いビジネス価値を引き出すものだからだ。

The suggestions presented below will be based on AWS services (although they are easily interchangeable with other public cloud services).
以下に紹介する提案は、AWSのサービスに基づいている(ただし、他のパブリック・クラウド・サービスとの互換性は高い)。

## 5.1. The simplest solution 最もシンプルな解決策

This architecture is based on managed services, which require less maintenance overhead and are better suited for small teams that can operate quickly.
このアーキテクチャはマネージド・サービスをベースにしており、メンテナンスのオーバーヘッドが少なく、小規模なチームで迅速に運用するのに適している。

My initial setup would be Redshift as an offline store, DynamoDB as an online key value store, Airflow to manage batch feature computation jobs.
私の最初のセットアップは、オフラインストアとしてRedshift、オンラインキーバリューストアとしてDynamoDB、バッチ機能計算ジョブを管理するためのAirflowです。
Also, Pandas as data processing engine for both options.
また、データ処理エンジンとしてPandasを使用することもできる。
In this architecture, all feature computation pipelines are scheduled in Airflow and would need to ingest data by using Python scripts that fetch data from Redshift or S3, transforms it, and put it into DynamoDB for online services and then in Redshift again for the offline feature storage.
このアーキテクチャでは、すべての特徴計算パイプラインはAirflowでスケジューリングされ、Pythonスクリプトを使用してデータを取り込む必要があります。このスクリプトは、**RedshiftまたはS3からデータをフェッチし、変換し、オンラインサービスのためにDynamoDBに入れ、オフラインの特徴ストレージのために再びRedshiftに入れます。**

![The initial setup chart](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-13.png?resize=850%2C416&ssl=1)

## 5.2. Medium-size feature store 中型フィーチャーストア

If you’re already dealing with big data, near real-time needs for features, and reusability necessities across data science teams, then you are probably looking for more standardization across feature pipelines and some degree of reusability.
ビッグデータ、リアルタイムに近い特徴量ニーズ、データサイエンスチーム間での再利用性の必要性をすでに扱っているのであれば、おそらく特**徴量パイプライン間の標準化とある程度の再利用性**を求めていることだろう。

In this situation, I would recommend starting using third-party feature store vendors when the data science team size is relatively big (let’s say, more than 8-10 data scientists).
このような状況では、**データサイエンス・チームの規模が比較的大きくなってから(例えば、8～10人以上のデータサイエンティスト)、サードパーティのフィーチャーストア・ベンダーの利用を開始することをお勧めする**。
First, I would explore Feast as it’s the most used open-source solution out there, and it can work on top of existing infrastructure.
まず、オープンソースのソリューションとして最も利用されているのがFeastで、既存のインフラストラクチャの上で動作させることができる。
You could use Redshift as an offline feature store and DynamoDB or Redis as an online feature store.
オフラインのフィーチャーストアとしてRedshiftを使い、オンラインのフィーチャーストアとしてDynamoDBやRedisを使うこともできる。
The latter is faster for online prediction services with lower latency requirements.
後者の方が、待ち時間の少ないオンライン予測サービスでは高速だ。
Feast will help to catalogue and serve features through their SDK and web UI (still experimental, though).
Feastは、SDKとウェブUI（まだ実験的だが）を通じて、機能のカタログ化と提供を支援する。
If you want a fully managed commercial tool, I implore you to try out Tecton.
完全に管理された商用ツールをお望みなら、ぜひテクトンをお試しいただきたい。

Feature computation pipelines can now be developed using plain Python or Spark if there are big data requirements, leveraging Feast SDK for managing data ingestion.
フィーチャー計算パイプラインは、ビッグデータ要件があれば、PythonやSparkを使用して開発することができます。

![Running Feast in production](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-14.png?ssl=1)

It’s also pretty likely that at this size, there are some use cases with real-time features freshness necessities.
また、**この規模になると、リアルタイムの特徴量鮮度が必要なユースケースも出てくるだろう**。
In this case, we need a streaming service that ingests features directly into the online feature store.
この場合、オンラインフィーチャーストアに直接フィーチャーを取り込むストリーミングサービスが必要になる。
We could use Kinesis services and AWS Lambda to write feature vectors into Redis or DynamoDB directly.
**KinesisサービスとAWS Lambdaを使って、特徴ベクトルをRedisやDynamoDBに直接書き込むことができる**。(batchではなくstream処理で特徴量を作るほうほう!)
If window aggregations are needed, then Kinesis Data Analytics, KafkaSQL, or Spark Streaming might be reasonable options.
ウィンドウ集計が必要な場合は、Kinesis Data Analytics、KafkaSQL、またはSpark Streamingが合理的な選択肢になるかもしれない。

## 5.3. Enterprise-level feature store エンタープライズレベルの機能ストア

At this stage, we assume the company has plenty of data scientists creating different types of models for different business or technical domains.
この段階では、**企業にはビジネスや技術領域ごとに異なるタイプのモデルを作成するデータサイエンティストが多数いる**と仮定する。(大規模な組織??)
One key principle when setting architectures for development teams of this size is to provide a reliable, scalable, secure, and standardized data platform.
この規模の開発チームのためにアーキテクチャを設定する際の重要な原則のひとつは、**信頼性が高く、スケーラブルで、安全で、標準化されたデータプラットフォームを提供すること**である。
Therefore, SLAs, GDPR, Audit, and Access Control Lists are mandatory requirements to put in place.
したがって、SLA、GDPR、監査、アクセス・コントロール・リストは、設置が義務付けられている必須要件である。
These are always important points to cover at every organization size, but in this case, they play a critical role.
これらはどの組織規模でも常にカバーすべき重要なポイントだが、今回は重要な役割を果たす。

![feature store explained](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-15.png?ssl=1)

Most of the big players in the tech space have built their own feature stores according to their own needs, security principles, existing infrastructure, and managed availability themselves to avoid having a single point of failure if the service is fully managed.
技術分野の大手企業のほとんどは、サービスが完全に管理されている場合、単一障害点が発生しないように、自社のニーズ、セキュリティ原則、既存のインフラ、管理された可用性に応じて、独自のフィーチャーストアを構築している。

But if this is not the case and you’re running a public cloud-heavy workload, using AWS SageMaker Feature Store or GCP Vertex AI Feature Store can be good options to start with.
しかし、そうではなく、**パブリッククラウドを多用するワークロードを実行している場合は、AWS SageMakerフィーチャーストアやGCP Vertex AIフィーチャーストアを使用するのが良い選択肢となる**。(かなり大規模になってからの話なのか...!)
Their API is very similar to their open source counterparts, and if you’re already using SageMaker or Vertex, setting up their feature store services should be straightforward.
APIはオープンソースのものとよく似ており、**すでにSageMakerやVertexを使っているのであれば、フィーチャーストア・サービスのセットアップも簡単だろう**。(簡単ならやってもいいのかな。)

![Amazon SageMaker Feature Store for machine learning](https://i0.wp.com/neptune.ai/wp-content/uploads/2022/10/how-to-solve-the-data-ingestion-and-feature-store-component-of-the-MLOps-stack-16.png?ssl=1)

Databricks also offers an embedded Feature Store service, which is also a good option and would be perfectly compatible with a tool like MLFlow.
Databricksはフィーチャーストアの組み込みサービスも提供しており、これも良いオプションで、MLFlowのようなツールと完全に互換性がある。

Databricks Feature Store | Source
Source

# 6. The buy versus build question ♪買うか作るかの問題

The MLOps landscape has been dominated and shaped by big players such as Facebook, Netflix, Uber, Spotify, etc., throughout these years with their very influential staff engineers and blogs.
MLOpsの状況は、フェイスブック、ネットフリックス、ウーバー、スポティファイなどの大企業が、影響力のあるスタッフ・エンジニアやブログによって支配し、形成してきた。
But ML teams should be able to recognize the contexts in which they operate in their own organizations, teams, and business domains.
しかし、MLチームは、自分たちの組織、チーム、ビジネス・ドメインにおいて、自分たちが活動しているコンテクストを認識することができるはずだ。
A 200,000 users app doesn’t need the scale, standardization, and rigidity of a 20-million one.
20万ユーザーのアプリには、2000万ユーザーのアプリのような規模、標準化、厳格さは必要ない。
That’s why MLOps at reasonable scale is a hot topic that is sticking around senior practitioners not working at FAANG-like companies.
だからこそ、それなりの規模でのMLOpsは、FAANGのような企業に勤めていない上級実務家たちの間で固着しているホットな話題なのだ。

Read also
あわせて読みたい

Setting up MLOps at a Reasonable Scale With Jacopo Tagliabue
ヤコポ・タリアブエとMLOを合理的な規模で立ち上げる

Explanation of a feature store | Source
Source

## 6.1. Who should build a feature store? 誰がフィーチャーストアを作るべきか？

As mentioned at the start of this article, there’s a constant tussle between building a feature store-like platform in-house or buying a commercial or open source product like Feast, Hopsworks, or Tecton.
この記事の冒頭で述べたように、フィーチャーストアのようなプラットフォームを自社で構築するか、Feast、Hopsworks、Tectonのような商用またはオープンソースの製品を購入するか、常に葛藤がある。
This tension exists primarily because these products can be opinionated to some degree in their architecture and their SDKs.
このような緊張が存在するのは、主にこれらの製品がそのアーキテクチャやSDKにおいてある程度意見が分かれる可能性があるためだ。
Thus, most of these tools need to have a central service to handle feature serving on top of online stores, which becomes a single point of failure for production ML services.
したがって、これらのツールのほとんどは、オンライン・ストアの上で機能提供を処理する中央サービスを持つ必要があり、これは本番MLサービスの単一障害点となる。

In addition, some other products are full SaaS, becoming an uncertain critical piece for some teams.
さらに、他の製品の中には完全なSaaS型のものもあり、チームによっては不確実な重要部品となっている。
Thus, ML Engineers are skeptical to bet and adhere too early to one of these tools in their MLOps journey.
従って、MLエンジニアは、MLOpsの旅において、これらのツールのいずれかに早くから賭けて固執することに懐疑的である。

It is very common that ML and Data Engineering teams share the same technology stack in small or medium size companies or startups.
中小企業や新興企業では、MLチームとデータエンジニアリング・チームが同じテクノロジー・スタックを共有することはよくあることだ。
For that reason, migrating to a feature store might cause a big headache and expose some hidden costs.
そのため、フィーチャーストアへの移行は大きな頭痛の種となり、隠れたコストが発生する可能性がある。
In terms of planning, legacy maintenance, operationality, duplicities, etc., it becomes another piece of infrastructure with specific SDKs which are different from the traditional Data Engineering ones.
計画、レガシー・メンテナンス、運用性、重複などの点で、従来のデータエンジニアリングとは異なる特定のSDKを持つ、もうひとつのインフラとなる。

## 6.2. Who should buy a feature store? 誰がフィーチャーストアを買うべきか？

To extract the most value from a commercial feature store, your use cases and data science teams’ setup need to be aligned with the core benefits that they provide.
商用フィーチャーストアから最大の価値を引き出すには、ユースケースとデータサイエンスチームのセットアップを、フィーチャーストアが提供するコアベネフィットと一致させる必要があります。
Products that are heavily reliant on real-time complex ML use cases such as recommendation systems, dynamic pricing, or fraud detection are the ones that can leverage these tools the most.
レコメンデーションシステム、ダイナミックプライシング、不正検知など、リアルタイムの複雑なMLユースケースに大きく依存している製品は、これらのツールを最も活用できるものである。

A big team of Data Scientists is also a good reason to have a feature store, as it will increase productivity and features reusability.
データサイエンティストの大規模なチームは、生産性と機能の再利用性を向上させるため、フィーチャーストアを持つ良い理由でもある。
Apart from that, they usually provide a nice UI to discover and explore features.
それとは別に、彼らは通常、機能を発見し探索するための素晴らしいUIを提供している。
Nonetheless, commercial Feature Store SDKs and APIs provide a set of standards for a more homogeneous way of ingesting and retrieving features.
それにもかかわらず、商用のフィーチャーストアSDKとAPIは、フィーチャーを取り込み、検索する、より均質な方法のための一連の標準を提供する。
And as a by-product, the data is governed, and reliable metadata is always logged.
そして副産物として、データは管理され、信頼できるメタデータが常に記録される。

In the very wide variety of ML teams domains, the situation described above is not always met, and setting up these new commercial stacks is sometimes just a personal development desire of the engineers to stay up-to-date with respect to new technology.
非常に多種多様なMLチームのドメインでは、上記のような状況が常に満たされるとは限らず、このような新しい商用スタックをセットアップすることは、新しいテクノロジーに関して常に最新でありたいというエンジニアの個人的な開発欲求に過ぎないこともある。

That’s why there are teams still who haven’t migrated to a full-packaged feature store and, instead, still rely on the existing data engineering stack for running their production feature engineering layer.
そのため、フルパッケージのフィーチャーストアに移行せず、既存のデータエンジニアリングスタックに依存してフィーチャーエンジニアリングレイヤーを運用しているチームもある。
This is totally valid, in my opinion.
これはまったく妥当だと私は思う。

All in all, feature stores just add a convenient shell on top of the existing data engineering stack to provide unified access APIs, a nice UI to discover and govern feature sets, guarantee consistency between online and feature stores, etc.
全体として、フィーチャーストアは既存のデータエンジニアリングスタックの上に便利なシェルを追加するだけで、統一されたアクセスAPI、フィーチャーセットを発見し管理するための優れたUI、オンラインとフィーチャーストア間の一貫性の保証などを提供する。
But all these features are not critical for every ML team’s use case.
しかし、これらの機能は、すべてのMLチームのユースケースにとって重要なものではない。

# 7. Conclusion 結論

I hope that this article has provided a broad view of what feature store are.
この記事で、フィーチャーストアとは何なのか、大まかにご理解いただけただろうか。
But more importantly, the reason they’re necessary and the key components that need to be addressed when building one.
しかし、それ以上に重要なのは、それが必要な理由と、それを構築する際に取り組むべき重要な要素である。

Feature stores are necessary for levelling up the production services in the data science industry.
フィーチャーストアは、データサイエンス業界におけるプロダクションサービスのレベルアップに必要なものだ。
But you need engineers behind them.
しかし、その背後にはエンジニアが必要だ。
The ML Engineer role is critical for dealing with feature pipelines as they are just a specific type of data transformation and ingestion process.
MLエンジニアの役割は、フィーチャー・パイプラインを扱う上で非常に重要だ。フィーチャー・パイプラインは、データ変換と取り込みプロセスの特定のタイプに過ぎないからだ。
Hybrid roles like that allow Data Scientists to focus more on the experimentation side and also guarantee high-quality deliverables.
このようなハイブリッドな役割を担うことで、データサイエンティストは実験により集中することができ、また高品質の成果物を保証することができる。

In addition, I paid special attention to explaining the build versus buy dilemma.
加えて、作るか買うかのジレンマを説明することに特に注意を払った。
From my personal experience, this question arises sooner or later within any mature ML team.
私の個人的な経験からすると、この疑問は成熟したMLチームであれば遅かれ早かれ生じるものだ。
I have tried to describe the situations in which they are key for achieving velocity and standardisation, but also left some thoughts on why context awareness is necessary regarding implementing this new technology.
私は、ベロシティと標準化を達成するためにそれらが鍵となる状況を説明しようとしたが、同時に、この新しいテクノロジーを導入する上で、なぜコンテクストを意識することが必要なのかについての考えも残した。
Experienced and senior roles should take into consideration the stage of the MLOps journey in which they operate.
経験豊富な上級職は、MLOpsの旅のステージを考慮する必要がある。

The feature store (commercial and open source) world is still young, and there is not yet a uniform and accepted way of dealing with all the different use cases and needs.
フィーチャー・ストア（商用およびオープンソース）の世界はまだ歴史が浅く、すべての異なるユースケースやニーズに対応する統一された受け入れられやすい方法はまだない。
So try all the approaches before settling down with one.
だから、1つに決める前に、すべてのアプローチを試してみてほしい。
