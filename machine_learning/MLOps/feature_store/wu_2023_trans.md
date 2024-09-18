## refs 審判

- <https://blog.det.life/build-your-own-feature-store-with-streaming-databases-5cae907cd0a6> <https://blog.det.life/build-your-own-feature-store-with-streaming-databases-5cae907cd0a6>

# Build Your Own Feature Store with Streaming Databases ストリーミング・データベースで独自のフィーチャーストアを構築しよう

With the increasing popularity of machine learning, a growing number of businesses are implementing it to address their operational challenges.
機械学習の人気が高まるにつれ、業務上の課題を解決するために機械学習を導入する企業が増えている。
As the volume of data continues to expand, organizations are encountering more issues related to data management than those associated with machine learning algorithms.
データ量が拡大し続ける中、**組織は機械学習アルゴリズムに関連する問題よりも、データ管理に関連する問題に遭遇している**。(なんとなくわかってきたかも...!:thinking:)
The feature store is a crucial tool that companies leverage to tackle data-related difficulties.
**フィーチャーストアは、企業がデータ関連の問題に取り組む際に活用する重要なツール**だ。

To incorporate a feature store, one can opt for a cloud-based solution.
フィーチャーストアを組み込むには、クラウドベースのソリューションを選択することができる。
For instance, Amazon’s Sagemaker offers a feature store.
例えば、AmazonのSagemakerは機能ストアを提供している。
Tecton is another renowned feature engineering platform.
テクトンも有名なフィーチャー・エンジニアリング・プラットフォームだ。
Additionally, there are several other alternatives, such as Claypot, Fennel, and Chalk, to name a few.
さらに、クレイポット、フェンネル、チョークなど、他の選択肢もいくつかある。

Nonetheless, what if someone wants to construct a feature store from the ground up utilizing open-source technologies? In this article, we discuss how to build a minimal feature store using a streaming database.
とはいえ、オープンソースの技術を利用して、一からフィーチャーストアを構築したい人がいるとしたらどうだろう？**この記事では、ストリーミング・データベースを使って最小限のフィーチャーストアを構築する方法**について説明する。

## What is a feature store? フィーチャーストアとは？

Feature stores serve as a crucial component of a data platform, designed to address several pivotal challenges, including but not limited to:
フィーチャーストアは、データプラットフォームの重要なコンポーネントであり、以下のようないくつかの重要な課題に対処するように設計されている：

- **Data Consistency**: In a large organization, multiple teams may work on similar tasks but utilize different tools, data, and features.
データの一貫性： 大きな組織では、複数のチームが同じようなタスクに取り組んでいても、異なるツール、データ、特徴量を利用していることがある。
This approach can cause inconsistencies in features, complicating comparisons of results or the scaling of solutions.
このアプローチは、特徴量に一貫性がなく、結果の比較やソリューションのスケーリングを複雑にする可能性がある。
A feature store works as a centralized repository of features, thereby ensuring uniformity across the entire organization.
**フィーチャーストアは、特徴量の一元的なリポジトリとして機能する**ため、組織全体の統一性が確保される。

- Feature Reusability: Data scientists typically dedicate a substantial amount of time to engineering features for their machine learning models.
特徴の再利用性： データ・サイエンティストは通常、機械学習モデルのフィーチャー・エンジニアリングにかなりの時間を割く。
Unfortunately, this effort is often replicated across various teams and projects.
残念なことに、この努力はさまざまなチームやプロジェクトで繰り返されることが多い。
A feature store facilitates the reuse of features crafted by others, thereby minimizing redundant efforts and accelerating the model development process.
**フィーチャーストアは、他の人が作成したフィーチャーの再利用を容易にし、それによって冗長な作業を最小限に抑え、モデル開発プロセスを加速**する。

- Data Transformation: Raw data often necessitates transformation into a format that is conducive for machine learning models.
データの変換： 生データは、機械学習モデルに適した形式に変換する必要がある場合が多い。
Such transformations can be computationally demanding and time-intensive.
このような変換は、計算量が多く、時間がかかる。
A feature store permits the pre-computation of features and their storage in an optimized format, thereby diminishing the time and computational resources required during model training.
フィーチャーストアは、特徴量の事前計算と最適化された形式での保存を可能にし、モデルのトレーニング中に必要な時間と計算リソースを削減する。

- Feature Versioning: Over time, the methodologies for computing features may evolve.
機能のバージョン管理： 時間の経過とともに、フィーチャーを計算する手法は進化する可能性がある。
It is imperative to document these modifications to ensure reproducibility and to comprehend the implications of changes on model performance.
再現性を確保し、モデル性能への変更の影響を理解するためには、これらの変更を文書化することが重要である。
A feature store encompasses versioning capabilities to administrate alterations to features over time.
フィーチャーストアは、時間の経過に伴うフィーチャーの変更を管理するためのバージョン管理機能を備えている。

<!-- ここまで読んだ! -->

## Feature Store in Action 機能ストアの動き

Before diving deep into building a feature store with streaming databases, let’s first take a look at how feature store works.
ストリーミング・データベースを使ってフィーチャーストアを構築する前に、まずフィーチャーストアの仕組みを見てみよう。

Essentially, a feature store is a repository designed to store various features and fetch specific ones as needed, thereby facilitating data services.
基本的に、**フィーチャーストアは様々なフィーチャーを保存し、必要に応じて特定のフィーチャーをフェッチするように設計されたリポジトリ**であり、それによってデータサービスを促進する。
It is required to offer two distinct categories of data services to accommodate different users: offline features and online features.
**さまざまなユーザーに対応するため、2つの異なるカテゴリーのデータサービスを提供する必要がある： オフライン機能とオンライン機能**。(i.e. オフラインストアとオンラインストア...??:thinking:)
These categories have unique attributes, as detailed below.
これらのカテゴリーには、以下に詳述するような独自の属性がある。

- Offline Features: These are tailored for the machine learning training phase, which typically demands a substantial quantity of data.
オフライン特徴量： これは機械学習の学習段階用に作られたもので、通常、かなりの量のデータを必要とする。
However, only a select few specific features are necessary for this process.
しかし、このプロセスに必要なのは、一部の特定の特徴のみである。
Since the training is carried out offline, there is no pressing need for fast query execution.
**トレーニングはオフラインで行われるため、クエリの高速実行は急務ではない。**

- Online Features: These are designed for the machine learning prediction phase and usually involve returning either all or a subset of the features of a small number of records.
オンライン特徴： これらは機械学習の予測フェーズ用に設計されており、通常、少数のレコードの特徴のすべてまたはサブセットを返します。
While the data required for online features is considerably less compared to offline features, there is a higher emphasis on fast query responses and real-time data availability.
オンライン機能に必要なデータはオフライン機能に比べてかなり少ないが、**クエリへの応答が速く、データがリアルタイムで利用可能であることがより重視されている**。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zMNmzMXYt9Hj5icXTCRa1w.png)

Now let’s consider building an application predicting taxi fare based on locations.
ここで、場所に基づいてタクシー料金を予測するアプリケーションを構築することを考えてみよう。
We use a public online dataset: <https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-green?tabs=azureml-opendatasets>.
公開オンラインデータセットを使用： <https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-green?tabs=azureml-opendatasets。>

We need to first preprocess the data.
まずデータを前処理する必要がある。
In this dataset, there are many columns, and they can be broadly divided into three categories:
このデータセットには多くの列があり、それらは大きく3つのカテゴリーに分けられる：

- 1. User input and output.
ユーザーの入力と出力。
In this example, the inputs are the taxi’s starting point (pu_location_id) and destination (do_location_id).
この例では、入力はタクシーの出発地（pu_location_id）と目的地（do_location_id）である。
We will use location_id to represent both in the following paragraphs.
以下の段落では、location_idを使って両者を表現する。
The output, or result, is the total fare (fare_amount).
出力（結果）は、運賃総額（fare_amount）である。
We need to keep these data intact for use during training;
トレーニング中に使用するため、これらのデータはそのままにしておく必要がある；

- 2. Data that can be used for feature extractions.
特徴抽出に使用できるデータ。
The so-called features refer to the attributes that are relevant to the prediction.
いわゆる特徴量とは、予測に関連する属性のことである。
For instance, if we want to predict the total fare, the average tip for starting from a particular location would be an essential feature.
例えば、総運賃を予測したい場合、特定の場所から出発した場合の平均チップは不可欠な特徴となる。
We need to extract features from these data and save them;
これらのデータから特徴を抽出して保存する必要がある；

- 3. Some data irrelevant to prediction.
予測に無関係なデータもある。
We need to filter out this data to prevent feature contamination.
特徴の混入を防ぐために、このデータをフィルタリングする必要がある。

After processing the data according to the above steps, we can use the features and the corresponding total fares to train machine learning.
上記のステップに従ってデータを処理した後、特徴量と対応する運賃総額を機械学習の学習に使用することができる。
We can also import features into a well-trained model for prediction.
また、十分に訓練された予測モデルに特徴をインポートすることもできる。

<!-- ここまで読んだ! -->

## Why Streaming Database? なぜストリーミング・データベースなのか？

A streaming database is a type of database designed to handle real-time data by processing streams of data in real-time or near-real-time.
**streaming databaseは、リアルタイムまたはほぼリアルタイムでデータストリームを処理することで、リアルタイムデータを処理するために設計されたデータベースの一種**です。
Traditional databases are designed to handle data at rest, which means the data is stored and then queried or analyzed.
従来のデータベースは、データを静止状態で扱うように設計されている。つまり、データは保存された後、照会や分析が行われる。
In contrast, a streaming database processes data on the fly as it arrives, without needing to store it first.
対照的に、ストリーミング・データベースは、最初にデータを保存する必要なく、データが到着するとその場で処理する。

In the context of a streaming database, a materialized view is a view of the data that is pre-computed and stored, rather than computed on demand.
ストリーミング・データベースのコンテキストでは、マテリアライズド・ビューは、必要に応じて計算されるのではなく、事前に計算されて保存されたデータのビューです。
Materialized views in streaming databases are incrementally updated as new data arrives, which allows them to reflect the current state of the data without the need to recompute the entire view.
ストリーミング・データベースのmaterialized viewは、新しいデータが到着するたびに増分的に更新されるため、ビュー全体を再計算する必要なく、データの現在の状態を反映することができる。

Streaming databases are a perfect match for feature stores for several reasons:
**ストリーミング・データベースがフィーチャーストアに最適な理由**はいくつかある：

- Real-time feature computation: Machine learning models often require real-time features to make predictions.
リアルタイムの特徴計算： 機械学習モデルは、予測を行うためにリアルタイムの特徴を必要とすることが多い。
For example, a fraud detection model may need the most recent transactions of a user to detect any fraudulent activities.
例えば、不正検知モデルは、不正行為を検知するために、ユーザーの直近の取引を必要とするかもしれない。
A streaming database can compute and update features in real time as data is ingested into the system, which ensures that the machine learning models always have access to the most up-to-date features.
ストリーミング・データベースは、データがシステムに取り込まれるとリアルタイムで特徴を計算し更新することができるため、機械学習モデルは常に最新の特徴にアクセスすることができる。

- Consistency: Maintaining consistency between the features used for training and serving the machine learning models is crucial for model performance.
一貫性： 機械学習モデルの学習と提供に使用される特徴間の一貫性を維持することは、モデルのパフォーマンスにとって極めて重要である。
A streaming database can ensure that the same set of features and transformations are used both for training and serving the models.
ストリーミング・データベースは、モデルの学習と提供の両方に、同じ特徴量と変換のセットが使用されることを保証する。

- Event time processing: Machine learning models often require features to be computed based on event time (the time when an event actually occurred) rather than processing time (the time when the event is processed by the system).
イベント時間の処理： **機械学習モデルは多くの場合、processing time（=イベントがシステムによって処理される時間）ではなく、event time（=イベントが実際に発生した時間）に基づいて特徴を計算する必要がある**。(??)
Streaming databases often provide support for event time processing, which ensures that the features are computed accurately even if there are delays in data ingestion or processing.
ストリーミング・データベースは、多くの場合、イベント・タイム処理をサポートしており、データの取り込みや処理に遅延があっても、特徴が正確に計算されるようになっている。

- Data freshness: For many applications, the value of data decreases rapidly with time.
データの鮮度： 多くのアプリケーションでは、データの価値は時間とともに急速に低下する。
For example, the most recent transactions of a user are often more relevant for fraud detection than transactions that occurred several days ago.
例えば、あるユーザの最新の取引は、数日前に発生した取引よりも不正検知にとってより関連性が高いことがよくある。(特徴量の鮮度が、精度に大きく影響する...!:thinking:)
A streaming database can ensure that the features in the feature store are always fresh and up-to-date.
**ストリーミング・データベースは、フィーチャー・ストアの特徴量を常に新鮮で最新の状態に保つことができる**。

By leveraging a streaming database, organizations can build a robust and scalable infrastructure for managing features and serving machine learning models in real time.
ストリーミング・データベースを活用することで、企業は特徴を管理し、機械学習モデルをリアルタイムで提供するための、堅牢でスケーラブルなインフラを構築することができる。
This can lead to more accurate and timely predictions, which is crucial for many applications.
これは、より正確でタイムリーな予測につながり、多くのアプリケーションにとって重要である。

<!-- ここまで読んだ! -->

## Build a feature store with a streaming database ストリーミングデータベースでフィーチャーストアを構築する

We now use a streaming database to build a feature store, e.g.RisingWave, a popular open-source streaming database.
例えば、オープンソースのストリーミング・データベースとして有名な RisingWave などである。
Users can create materialized views (MV) in RisingWave using SQL statements to build streaming pipelines for feature transformation and computation.
ユーザーは、SQLステートメントを使用してRisingWaveで **materialized view（MV）**を作成し、特徴量の変換と計算のためのストリーミング・パイプラインを構築することができる。
(materialized viewがよくわかってない...:thinking:)

- メモ: materialized viewとは??
  - データベースにおけるviewの一種。
    - view: DB内の仮想テーブルで、クエリの結果を保持しておくこと??
  - materialized view:
    - 物理的なデータの保存:
      - 通常のviewとは異なり、クエリの結果をテーブルのようにディスク上に保存する。従って、再度クエリを実行する必要がなく、データの取得が高速になる。
    - データの更新:
      - materialized viewのデータは、元のテーブルの更新とは同期しない。そのため、定期的にリフレッシュする必要がある。
    - パフォーマンスの向上:
      - 複雑なクエリを頻繁に実行する場合、materialized viewを使用することでパフォーマンスが大幅に向上する。特に集計クエリや結合クエリに有効。

In the taxi fare example, we ingest data into RisingWave through Apache Kafka.
タクシー料金の例では、Apache Kafkaを通じてRisingWaveにデータを取り込む。
RisingWave will extract features in real time and perform transformations according to the predefined logic expressed in materialized views.
RisingWaveはリアルタイムで特徴を抽出し、マテリアライズド・ビューで表現された定義済みのロジックに従って変換を実行する。
The results are then saved in RisingWave’s storage.
結果はライジングウェーブのストレージに保存される。
To perform ML serving, users can directly query materialized views to fetch features in real time.
MLサービングを実行するために、ユーザーはマテリアライズド・ビューに直接クエリーを実行し、リアルタイムで特徴を取得することができる。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Thi1F6WDK_PPtuX05VZH0w.png)

When it comes to offline features, we have multiple solutions to consider:
オフライン機能に関しては、私たちは複数のソリューションを用意しています：

- RisingWave offers native batch processing capability.
RisingWaveはネイティブのバッチ処理機能を提供します。
This allows users to use SQL queries in RisingWave for batch data processing.
これにより、ユーザーはRisingWaveでSQLクエリを使用してバッチデータ処理を行うことができます。

- If we need enhanced batch processing capabilities, RisingWave can connect with data warehouses (like Redshift and Snowflake) or other OLAP systems (like ClickHouse) tailored for batch processing through a sink connection.
強化されたバッチ処理機能が必要な場合、RisingWaveはシンク接続を通じて、バッチ処理用に調整されたデータウェアハウス（RedshiftやSnowflakeなど）や他のOLAPシステム（ClickHouseなど）と接続することができる。

Now, let’s delve deeper into the feature engineering process within RisingWave.
では、ライジングウェーブのフィーチャー・エンジニアリング・プロセスをさらに掘り下げてみよう。
Let’s reconsider the taxi fare example.
タクシー料金の例をもう一度考えてみよう。
As data pours into RisingWave, it first undergoes a filtering process.
ライジングウェーブにデータが流れ込むと、まずフィルタリング処理が行われる。
This removes any irrelevant data and channels the refined data into a designated Filter MV (Materialized View).
これにより、無関係なデータが削除され、精製されたデータが指定されたフィルターMV（マテリアライズド・ビュー）に流されます。
Following this, we establish two types of MVs:
続いて、2種類のMVを設定する：

- User MV: This captures both the user’s input and desired outputs, like the starting and ending points of a taxi ride (represented by location_id) and the associated fare (fare_amount).
ユーザーMV： これはユーザーの入力と希望する出力の両方をキャプチャします。たとえば、タクシーに乗る開始点と終了点（location_idで表されます）、関連する料金（fare_amount）などです。

- Feature MV: This is designed to save features derived from the validated data.
フィーチャーMV： 検証されたデータから得られたフィーチャーを保存するためのもの。
For simplicity during both training and prediction, the taxi’s origin and destination serve as the primary keys.
訓練と予測の両方を簡単にするため、タクシーの出発地と目的地が主キーとなる。

Both MVs are constantly updated as new data comes in, and users can always see consistent and fresh online features.
どちらのMVも、新しいデータが入ると常に更新され、ユーザーは常に一貫した新鮮なオンライン機能を見ることができる。

For the training phase, we input the desired feature names.
学習段階では、目的の特徴名を入力する。
We then pull the required offline features from the Feature MV and couple it with the corresponding fare amount from the User MV to train our model.
次に、Feature MVから必要なオフライン特徴を取り出し、User MVから対応する運賃額と組み合わせてモデルを訓練する。
When predicting, by just inputting the location_id, we can fetch the related online features from the Feature MV and employ our trained model for accurate predictions.
予測時には、location_idを入力するだけで、Feature MVから関連するオンラインFeatureを取得し、学習したモデルを用いて正確な予測を行うことができる。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*lDI33iqrbcv6nzJzpZiPQA.png)

<!-- ここまで読んだ! -->

## Demo: How to use RisingWave to build a feature store デモ RisingWaveを使ってフィーチャーストアを構築する方法

We now get our hands dirty and demonstrate how to use RisingWave to build a feature store.
RisingWaveを使ってフィーチャーストアを構築する方法を紹介しよう。

### Step 1: Fetch source code ステップ 1： ソースコードを取得する

```shell
git clone <https://github.com/risingwavelabs/risingwave.git>
cd integration_tests/nyc-taxi-feature-store-demo
```

### Step 2: Deploy using Docker ステップ 2： Dockerを使用してデプロイする

```shell
docker compose up --build
```

Here, we launch RisingWave, Kafka, and Feature Store within the Docker cluster.
ここでは、RisingWave、Kafka、Feature StoreをDockerクラスタ内で起動する。
RisingWave primarily consists of front-end nodes, computation nodes, metadata nodes, and MinIO.
ライジングウェーブは主に、フロントエンドノード、計算ノード、メタデータノード、MinIOで構成されている。
For this demo cluster, the data from the materialized views will reside in the MinIO instance, with relevant SQL statements outlined below.
このデモクラスタでは、マテリアライズド・ビューからのデータはMinIOインスタンスに存在し、関連するSQLステートメントの概要は次のとおりです。
The core components of the Feature Store are the Server and Simulator.
フィーチャーストアのコアコンポーネントは、サーバーとシミュレーターである。
Once a Kafka node is established, topics are generated automatically.
Kafkaノードが確立されると、トピックは自動的に生成される。

Here’s what the Feature Store system will sequentially undertake:
フィーチャーストアのシステムが順次請け負うことは以下の通りだ：

- It will channel simulated offline data to Kafka, followed by RisingWave, and from there, derive both behavior and feature tables;
シミュレーションされたオフラインデータをKafkaに流し、RisingWaveがそれに続く；

- By joining these tables, it retrieves the appropriate offline training data to initiate model training;
これらのテーブルを結合することで、適切なオフライン学習データを取得し、モデルの学習を開始する;

- It introduces the simulated online feature data to Kafka and subsequently to RisingWave;
シミュレーションされたオンライン機能データをKafkaに導入し、その後RisingWaveに導入する；

- Leveraging the do_location_id (end location) and pu_location_id (start location), the system fetches the freshest online features from RisingWave.
do_location_id（終了位置）とpu_location_id（開始位置）を活用して、システムはライジングウェーブから最も新鮮なオンライン機能をフェッチする。
Using these features, predictions are made with the trained model.
これらの特徴を用いて、学習済みモデルによる予測が行われる。

### Step 3: Retrieve system logs ステップ3： システムログの取得

The sample logs are as follows.
サンプルログは以下の通り。
Since this article is solely to showcase the Feature Store built on RisingWave, the model parameters used in the demonstration have not been optimized, and the data volume is relatively small.
この記事は、RisingWave上に構築されたFeature Storeを紹介するためだけのものであるため、デモで使用されたモデルパラメータは最適化されておらず、データ量も比較的少ない。
Therefore, the prediction accuracy might not meet production requirements.
そのため、予測精度が生産要件を満たさない可能性がある。
It can be expanded as needed.
必要に応じて拡張できる。

At this moment, RisingWave stores the following online features.
現在、ライジングウェーブには以下のオンライン機能があります。
It can be observed that the online data has been extracted based on the relevant window for corresponding features and saved in RisingWave.
オンラインデータは、対応する特徴の関連ウィンドウに基づいて抽出され、RisingWaveに保存されていることが確認できる。

## Conclusion 結論

In the evolving landscape of machine learning, optimal data management is indispensable, spotlighting the significance of feature stores.
機械学習の進化において、最適なデータ管理は必要不可欠であり、フィーチャーストアの重要性が浮き彫りになっている。
While solutions such as Amazon’s Sagemaker and Tecton are readily available, utilizing open-source streaming databases to engineer a custom feature store offers granular control and adaptability.
**AmazonのSagemakerやTectonのようなソリューションはすぐに利用できるが、オープンソースのストリーミングデータベースを利用してカスタムフィーチャーストアを設計することで、きめ細かなコントロールと適応性が得られる**。
For teams aiming for deep architectural control and system integration, architecting their own feature store presents a technically robust approach.
**深いアーキテクチャー制御とシステム統合を目指すチームにとって、独自のフィーチャーストアをアーキテクチャーすることは、技術的にロバストなアプローチとなる**。

<!-- ここまで読んだ! -->
