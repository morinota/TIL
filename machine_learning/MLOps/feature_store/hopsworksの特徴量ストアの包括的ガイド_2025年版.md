
# Feature Store: The Definitive Guide 特徴ストア: 決定版ガイド  

## What is a feature store? 特徴ストアとは何ですか？

A feature store is a data platform that supports the development and operation of machine learning systems by managing the storage and efficient querying of feature data. 
特徴ストアは、特徴データのストレージと効率的なクエリ処理を管理することによって、機械学習システムの開発と運用をサポートするデータプラットフォームです。
Machine learning systems can be real-time, batch or stream processing systems, and the feature store is a general purpose data platform that supports a multitude of write and read workloads, including batch and streaming writes, to batch and point read queries, and even approximate nearest neighbour search. 
**機械学習システムはリアルタイム、バッチ、またはストリーム処理システム**であり、特徴ストアはバッチおよびストリーミング書き込みからバッチおよびポイント読み取りクエリ、さらには近似最近傍検索まで、多様な書き込みおよび読み取りワークロードをサポートする汎用データプラットフォームです。
Feature stores also provide compute support to ML pipelines that create and use features, including ensuring the consistent computation of features in different (offline and online) ML pipelines. 
特徴ストアは、特徴を作成および使用するMLパイプラインに計算サポートも提供し、異なる（オフラインおよびオンラインの）MLパイプラインにおける特徴の一貫した計算を保証します。

<!-- ここまで読んだ! --> 

## What is a feature and why do I need a specialized store for them? 特徴とは何か、そしてなぜそれらのための専門のストアが必要なのか？

A feature is a measure property of some entity that has predictive power for a machine learning model. 
特徴量(feature)とは、ある対象(entity)の属性(property)を数値化したもので、かつ機械学習モデルの予測に役立つものである。
Feature data is used to train ML models, and make predictions in batch ML systems and online ML systems. 
特徴量データは、MLモデルのトレーニングや、バッチMLシステムおよびオンラインMLシステムでの予測に使用されます。
Features can be computed either when they are needed or in advance and used later for training and inference. 
**特徴は、必要なときに計算することも、事前に計算して後でトレーニングや推論に使用することもできます**。
Some of the advantages of storing features is that they can be easily discovered and reused in different models, reducing the cost and time required to build new machine learning systems. 
**特徴を保存することの利点の一部は、それらが簡単に発見され、異なるモデルで再利用できるため、新しい機械学習システムを構築するために必要なコストと時間を削減できることです**。
For real-time ML systems, the feature store provides history and context to (stateless) online models. 
リアルタイムMLシステムにおいて、特徴ストアは（ステートレス）オンラインモデルに履歴とコンテキストを提供します。
Online models tend to have no local state, but the feature store can enrich the set of features available to the model by providing, for example, historical feature data about users (retrieved with the user’s ID) as well as contextual data, such as what’s trending. 
オンラインモデルはローカルステートを持たない傾向がありますが、特徴ストアは、例えばユーザに関する履歴の特徴データ（ユーザのIDで取得）や、トレンド情報などのコンテキストデータを提供することで、モデルに利用可能な特徴のセットを豊かにすることができます。
(これってどういう意味だろう。local stateを持たない傾向、って部分。perplexityに聞いてみた感じ、各ユーザやリクエストの履歴・状態をモデル本体やサーバーのメモリ内に溜め込まず、**「今来たリクエスト」に含まれる情報だけをそのまま使う傾向がある**、みたいなイメージっぽい??:thinking:)
The feature store also reduces the time required to make online predictions, as these features do not need to be computed on-demand, - they are precomputed. 
特徴ストアは、これらの特徴がオンデマンドで計算される必要がないため、オンライン予測に必要な時間を短縮します。- それらは事前に計算されています。

## How does the feature store relate to MLOps and ML systems? 特徴ストアはMLOpsおよびMLシステムとどのように関連していますか？

In a MLOps platform, the feature store is the glue that ties together different ML pipelines to make a complete ML system: 
MLOpsプラットフォームにおいて、**特徴ストアは異なるMLパイプラインを結びつけて完全なMLシステムを作る接着剤**です。

- feature pipelines compute features and then write those features (and labels/targets) to it; 
  - 特徴パイプラインは特徴を計算し、それらの特徴（およびラベル/ターゲット）を書き込みます；

- training pipelines read features (and labels/targets) from it; 
  - トレーニングパイプラインはそこから特徴（およびラベル/ターゲット）を読み取ります；

- Inference pipelines can read precomputed features from it. 
  - 推論パイプラインはそこから事前計算された特徴を読み取ることができます。

The main goals of MLOps are to decrease model iteration time, improve model performance, ensure governance of ML assets (feature, models), and improve collaboration. 
MLOpsの主な目標は、モデル試行錯誤のiteractionを短縮し、モデルのパフォーマンスを向上させ、ML資産（特徴、モデル）のガバナンスを確保し、コラボレーションを改善することです。
(結果としてiterationをよりいい感じに回せるようになることが、成果のスケールに繋がるから、って解釈できそう...!:thinking:)
By decomposing your ML system into separate feature, training, and inference (FTI) pipelines, your system will be more modular with 3 pipelines that can be independently developed, tested, and operated. 
MLシステムを特徴、トレーニング、推論（FTI）パイプラインに分解することで、システムはよりモジュール化され、3つのパイプラインが独立して開発、テスト、運用できるようになります。
This architecture will scale from one developer to teams that take responsibility for the different ML pipelines: 
このアーキテクチャは、1人の開発者から異なるMLパイプラインの責任を持つチームにスケールします：
data engineers and data scientists typically build and operate feature pipelines; 
データエンジニアとデータサイエンティストは通常、特徴量パイプラインを構築し運用します；
data scientists build and operate training pipelines, 
データサイエンティストはトレーニングパイプラインを構築し運用し、
while ML engineers build and operate inference pipelines. 
一方、MLエンジニアは推論パイプラインを構築し運用します。
The feature store enables the FTI pipeline architecture, enabling improved communication within and between data, ML, and operations teams. 
**特徴量ストアはFTIパイプラインアーキテクチャを可能にし**、データ、ML、およびオペレーションチーム内および間のコミュニケーションを改善します。

<!-- ここまで読んだ! -->

## What problems does a feature store solve? 特徴ストアはどのような問題を解決するのか？

The feature store solves many of the challenges that you typically face when you (1) deploy models to production, and (2) scale the number of models you deploy to production, and (3) scale the size of your ML teams, including:
特徴ストアは、モデルを本番環境にデプロイする際、デプロイするモデルの数をスケールする際、そしてMLチームの規模を拡大する際に直面する多くの課題を解決します。これには以下が含まれます：

1. Support for collaborative development of ML systems based on centralized, governed access to feature data, along with a new unified architecture for ML systems as feature, training and inference pipelines;
   - 中央集権的で管理された特徴データへのアクセスに基づくMLシステムの共同開発をサポートし、特徴、トレーニング、推論パイプラインとしての新しい統一アーキテクチャを提供します。

2. Manage incremental datasets of feature data. You should be able to easily add new, update existing, and delete feature data using DataFrames. Feature data should be transparently and consistently replicated between the offline and online stores;
   - 特徴データの増分データセットを管理します。新しいデータを簡単に追加し、既存のデータを更新し、DataFramesを使用して特徴データを削除できる必要があります。特徴データは、オフラインストアとオンラインストアの間で透明かつ一貫して複製されるべきです。

3. Backfill feature data from data sources using a feature pipeline and backfill training data using a training pipeline;
   - 特徴パイプラインを使用してデータソースから特徴データをバックフィルし、トレーニングパイプラインを使用してトレーニングデータをバックフィルします。

4. Provide history and context to stateless interactive (online) ML applications;
   - ステートレスなインタラクティブ（オンライン）MLアプリケーションに履歴とコンテキストを提供します。(=これはさっきのlocal stateを持たない傾向、に関連してる話!)

5. Feature reuse is made easy by enabling developers to select existing features and reuse them for training and inference in a ML model;
   - 開発者が既存の特徴を選択し、MLモデルのトレーニングと推論に再利用できるようにすることで、特徴の再利用が容易になります。

6. Support for diverse feature computation frameworks - including batch, streaming, and request-time computation. This enables ML systems to be built based on their feature freshness requirements;
   - **バッチ、ストリーミング、リクエスト時計算**を含む多様な特徴計算フレームワークをサポートします。これにより、MLシステムは特徴の新鮮さの要件に基づいて構築できます。

7. Validate feature data written and monitor new feature data for drift;
   - 書き込まれた特徴データを検証し、新しい特徴データのドリフトを監視します。

8. A taxonomy for data transformations for machine learning based on the type of feature computed (a) reusable features are computed by model-independent transformations, (b) features specific to one model are computed by model-dependent transformations, and (c) features computed with request-time data are on-demand transformations. The feature store provide abstractions to prevent skew between data transformations performed in more than one ML pipeline.
   - 機械学習のためのデータ変換の分類法は、計算された特徴のタイプに基づいています。(a) 再利用可能な特徴はモデルに依存しない変換によって計算され、(b) 特定のモデルに特有の特徴はモデルに依存する変換によって計算され、(c) リクエスト時データで計算された特徴はオンデマンド変換です。特徴ストアは、複数のMLパイプラインで実行されるデータ変換の偏りを防ぐための抽象化を提供します。

9. A point-in-time consistent query engine to create training data from historical time-series feature data, potentially spread over many tables, without future data leakage;
   - **将来のデータ漏洩なしに、歴史的な時系列特徴データからトレーニングデータを作成するための時点整合性のあるクエリエンジンを提供**します。これは、多くのテーブルにまたがる可能性があります。

10. A query engine to retrieve and join precomputed features at low latency for online inference using an entity key;
    - エンティティキーを使用してオンライン推論のために、低遅延で事前計算された特徴を取得し、結合するためのクエリエンジンを提供します。

11. A query engine to find similar feature values using embedding vectors.
    - 埋め込みベクトルを使用して類似の特徴値を見つけるためのクエリエンジンを提供します。

The table below shows you how the feature store can help you with common ML deployment scenarios.
以下の表は、特徴ストアが一般的なMLデプロイメントシナリオでどのように役立つかを示しています。

![]()

For just putting ML in production, the feature store helps with managing incremental datasets, feature validation and monitoring, where to perform data transformations, and how to create point-in-time consistent training data. 
(バッチの)MLを本番環境にデプロイするだけの場合、特徴ストアは増分データセットの管理、特徴の検証と監視、データ変換を行う場所、時点整合性のあるトレーニングデータを作成する方法を支援します。
Real-Time ML extends the production ML scenario with the need for history and context information for stateless online models, low latency retrieval of precomputed features, online similarity search, and the need for either stream processing or on-demand feature computation. 
リアルタイムMLは、ステートレスなオンラインモデルのための履歴とコンテキスト情報、事前計算された特徴の低遅延取得、オンライン類似検索、ストリーム処理またはオンデマンド特徴計算のいずれかの必要性を伴って、製品MLシナリオを拡張します。
For the ML at large scale, there is also the challenge of enabling collaboration between teams of data engineers, data scientists, and ML engineers, as well as the reuse of features in many models.
大規模なMLでは、データエンジニア、データサイエンティスト、MLエンジニアのチーム間でのコラボレーションを可能にし、多くのモデルでの特徴の再利用を促進するという課題もあります。

<!-- ここまで読んだ! -->

### Collaborative Development コラボレーティブ開発

Feature stores are the key data layer in a MLOps platform. 
フィーチャーストアは、MLOpsプラットフォームにおける重要なデータ層です。
The main goals of MLOps are to decrease model iteration time, improve model performance, ensure governance of ML assets (feature, models), and improve collaboration. 
MLOpsの主な目標は、モデルの反復時間を短縮し、モデルのパフォーマンスを向上させ、ML資産（フィーチャー、モデル）のガバナンスを確保し、コラボレーションを改善することです。
（これさっきも言ってた!）
The feature store enables different teams to take responsibility for the different ML pipelines: data engineers and data scientists typically build and operate feature pipelines; data scientists build and operate training pipelines, while ML engineers build and operate inference pipelines. 
**フィーチャーストアは、異なるチームが異なるMLパイプラインの責任を持つことを可能にします**：データエンジニアとデータサイエンティストは通常フィーチャーパイプラインを構築・運用し、データサイエンティストはトレーニングパイプラインを構築・運用し、MLエンジニアは推論パイプラインを構築・運用します。
（これはFTI Pipelines Architectureの効用な気がする!まあニアリーイコールか！）

![]()

They enable the sharing of ML assets and improved communication within and between teams. 
これにより、ML資産の共有とチーム内およびチーム間のコミュニケーションの改善が可能になります。
Whether teams are building batch machine learning systems or real-time machine learning systems, they can use shared language around feature, training, and inference pipelines to describe their responsibilities and interfaces. 
チームがバッチ機械学習システムを構築している場合でも、リアルタイム機械学習システムを構築している場合でも、フィーチャー、トレーニング、推論パイプラインに関する共通の言語を使用して、責任とインターフェースを説明できます。
A more detailed Feature Store Architecture is shown in the figure below. 
より詳細なフィーチャーストアアーキテクチャは、以下の図に示されています。

![]()

Its historical feature data is stored in an offline store (typically a columnar data store), its most recent feature data that is used by online models in an online store (typically a row-oriented database or key-value store), and if indexed embeddings are supported, they are stored in a vector database. 
その履歴フィーチャーデータはオフラインストア（通常はカラム型データストア）に保存され、オンラインモデルで使用される最新のフィーチャーデータはオンラインストア（通常は行指向データベースまたはキー・バリューストア）に保存され、インデックス付き埋め込みがサポートされている場合は、ベクトルデータベースに保存されます。
(**あ、オンラインストアに全ての特徴量を保存する必要はなくて、リアルタイム推論で使うもの、かつ最新のversionの特徴量レコードのみで良さそう...!! :thinking:**)
Some feature stores provide the storage layer as part of the platform, some have partial or full pluggable storage layers. 
一部のフィーチャーストアは、プラットフォームの一部としてストレージ層を提供し、一部は部分的または完全にpluggableなストレージ層を持っています。
(=一部のFeature Storeはストレージ層をそれ自体が持ち、また別のFeature Storeはそれ自体がストレージ層を持たずに別のストレージ層と接続する、みたいな??:thinking:)

The machine learning pipelines (feature pipelines, training pipelines, and inference pipelines) read and write features/labels from/to the feature store, and prediction logs are typically also stored there to support feature/model monitoring and debugging. 
機械学習パイプライン（フィーチャーパイプライン、トレーニングパイプライン、推論パイプライン）は、**フィーチャーストアからフィーチャー/ラベルを読み書きし**、予測ログも通常そこに保存されて、フィーチャー/モデルの監視とデバッグをサポートします。
(予測結果もfeature storeに保存する想定なのか...!:thinking:)
Different data transformations (model-independent, model-dependent, and on-demand) are performed in the different ML pipelines, see the Taxonomy of Data Transformations for more details. 
異なるデータ変換（モデル非依存、モデル依存、オンデマンド）が異なるMLパイプラインで実行されます。詳細については、データ変換の分類を参照してください。
(うんうん、複数本のFeature pipelineが動くよね、って話...!:thinking:)

<!-- ここまで読んだ! -->

### Incremental Datasets 増分データセット

Feature pipelines keep producing feature data as long as your ML system is running. 
フィーチャーパイプラインは、MLシステムが稼働している限り、フィーチャーデータを生成し続けます。 
Without a feature store, it is non-trivial to manage the mutable datasets updated by feature pipelines - as the datasets are stored in the different offline/online/vector-db stores. 
フィーチャーストアがないと、フィーチャーパイプラインによって更新される可変データセットを管理することは簡単ではありません。データセットは異なるオフライン/オンライン/ベクトルDBストアに保存されているためです。 
Each store has its own drivers, authentication and authorization support, and the synchronization of updates across all stores is challenging. 
各ストアには独自のドライバー、認証および認可のサポートがあり、すべてのストア間での更新の同期は困難です。 

Feature stores make the management of mutable datasets of features, called feature groups, easy by providing CRUD (create/read/update/delete) APIs. 
**フィーチャーストアは、CRUD（作成/読み取り/更新/削除）APIを提供**することで、フィーチャーの可変データセット（フィーチャーグループと呼ばれる）の管理を容易にします。(ざっくりCRUDがfeature storeの抽象化されたinterfaceと言えそう...!:thinking:)
The following code snippet shows how to append, update & delete feature data in a feature group using a Pandas DataFrame in Hopsworks. 
以下のコードスニペットは、HopsworksのPandas DataFrameを使用してフィーチャーグループにフィーチャーデータを追加、更新、および削除する方法を示しています。 
The updates are transparently synchronized across all of the underlying stores - the offline/online/vector-db stores. 
更新は、すべての基盤となるストア（オフライン/オンライン/ベクトルDBストア）間で透過的に同期されます。
(たぶん、オフラインストアにだけあればOKなデータは、Createフェーズで定義しておくんだろうな...!:thinking:)

```python
df = # read from data source, then perform feature engineering
fg = fs.get_or_create_feature_group(name="query_terms_yearly",
                              version=1,
                              description="Count of search term by year",
                              primary_key=['year', 'search_term'],
                              partition_key=['year'],
                              online_enabled=True
                              )
fg.insert(df) # insert or update
fg.commit_delete_record(df) # delete
```

We can also update the same feature group using a stream processing client (streaming feature pipeline). 
同じ特徴グループをストリーム処理クライアント（ストリーミングフィーチャーパイプライン）を使用して更新することもできます。(同じ特徴量グループを、バッチでもストリームでも更新できるよ、って話か。まあそりゃそうな気がする...!:thinking:)
The following code snippet uses PySpark streaming to update a feature group in Hopsworks. 
以下のコードスニペットは、Hopsworksの特徴グループを更新するためにPySparkストリーミングを使用します。
It computes the average amount of money spent on a credit card, for all transactions on the credit card, every 10 minutes. 
これは、クレジットカードのすべての取引に対して、10分ごとにクレジットカードで使われた平均金額を計算します。
It reads its input data as events from a Kafka cluster. 
入力データはKafkaクラスターからのイベントとして読み取ります。

```python
df_read = spark.readStream.format("kafka")...option("subscribe", 
KAFKA_TOPIC_NAME).load()
 
# Deserialize data from Kafka and create streaming query
df_deser = df_read.selectExpr(....).select(...)
 
# 10 minute window
windowed10mSignalDF = df_deser \
    .selectExpr(...)\
    .withWatermark(...) \
    .groupBy(window("datetime", "10 minutes"), "cc_num").agg(avg("amount")) \
    .select(...)
 
card_transactions_10m_agg =fs.get_feature_group("card_transactions_10m_agg", version=1)
 
query_10m = card_transactions_10m_agg.insert_stream(windowed10mSignalDF)
```

Some feature stores also support defining columns as embeddings that are indexed for similarity search.  
**いくつかのフィーチャーストアは、類似検索のためにインデックス化された埋め込みとして列を定義することもサポート**しています。 (vector型のカラムがこれなのかな...!:thinking:)
The following code snippet writes a DataFrame to a feature group in Hopsworks, and indexes the “embedding_body” column in the vector database.  
以下のコードスニペットは、DataFrameをHopsworksのフィーチャーグループに書き込み、“embedding_body”列をベクトルデータベースにインデックス化します。  
You need to create the vector embedding using a model, add it as a column to the DataFrame, and then write the DataFrame to Hopsworks.  
モデルを使用してベクトル埋め込みを作成し、それをDataFrameの列として追加し、その後DataFrameをHopsworksに書き込む必要があります。  

```python
from hsfs import embedding
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

df = # read from data source, then perform feature engineering


embeddings_body = model.encode(df["Article"])
df["embedding_body"] = pd.Series(embeddings_body.tolist())

emb = embedding.EmbeddingIndex()
emb.add_embedding("embedding_body", len(df["embedding_body"][0]))

news_fg = fs.get_or_create_feature_group(
    name="news_fg",
    embedding_index=emb,
    primary_key=["id"],
    version=1,
    online_enabled=True
)
news_fg.insert(df)
```

<!-- ここまで読んだ! -->

### Backfill feature data and Training Data バックフィル機能データとトレーニングデータ

Backfilling is the process of recomputing datasets from raw, historical data. 
**バックフィリングは、生の履歴データからデータセットを再計算するプロセス**です。
When you backfill feature data, backfilling involves running a feature pipeline with historical data to populate the feature store. 
特徴量データをバックフィルする際、バックフィリングは履歴データを使用して特徴量ストアを埋めるために特徴量パイプラインを実行することを含みます。
This requires users to provide a start_time and an end_time for the range of data that is to be backfilled, and the data source needs to support timestamps, e.g., Type 2 slowly changing dimensions in a data warehouse table. 
これには、**ユーザーがバックフィルするデータの範囲のためにstart_timeとend_timeを提供する必要があり**、データソースはタイムスタンプをサポートする必要があります。例えば、データウェアハウスのテーブルにおけるType 2の徐々に変化する次元などです。

- 思ったことメモ:
  - 毎回全ユーザ分の特徴量を作る系のパイプラインだったら、backfillはあくまで学習用データセットを作るため、という用途になりそう...!:thinking:
  - 特定期間内に追加・更新されたアイテムだけの特徴量を作る系のパイプラインだったら、学習用だけじゃなくて推論用のデータを作る目的でもbackfillしそう。
  - まあすでに既存の特徴量パイプライン達が運用されてる状況だったらbackfillってのはあんまりする必要はなくて、**どちらにせよ、特徴量グループに新しい特徴量を追加したり既存特徴量の作り方を変更した場合などにbackfillすることになるはず**:thinking:
  - backfill可能なデータパイプラインである為には、やはり無状態 & 冪等性を持つパイプラインを意識する必要がありそう...!:thinking:

The same feature pipeline used to backfill features should also process “live” data. 
特徴量のbackfillに使用されるのと同じ特徴量パイプラインは、「ライブ」データも処理する必要があります。(うんうん、リアルタイムで現在収集してるデータも同じパイプラインで処理させようね、という話。ここで実装が別になってしまってるとバグの温床なんだよね...!:thinking:)
You just point the feature pipeline at the data source and the range of data to backfill (e.g., backfill the daily partitions with all users for the last 180 days). 
単に特徴量パイプラインを、データソースとバックフィルするデータの範囲（例：過去180日間のすべてのユーザーの毎日のパーティションをバックフィル）にポイントすればOKです。
(要するに、**わざわざ「バックフィル用の特別なパイプライン」を別で作るのはやめようね**、って話だと思ってる! backfill時は、対象データ期間を「過去データの範囲に切り替えて」動かすだけ! :thinking:)
Both batch and streaming feature pipelines should be able to backfill features. 
バッチおよびストリーミング特徴量パイプラインの両方が特徴量をバックフィルできる必要があります。(**ストリーミングパイプラインもbackfillできるようにしておこうね**、という話か...!ストリームのreplay設計っていうらしい...!:thinking:) 
(でも結局、大量の期間のデータをbackifillする際には、バッチというかバルクで一気に処理できる設計になってた方がいいよな...**単一のパイプラインをバッチでもストリームでも実行できるようにしておくのが運用上最強ってことでは**...!:thinking:)
Backfilling features is important because you may have existing historical data that can be leveraged to create training data for a model. 
特徴量をバックフィルすることは重要です。なぜなら、モデルのトレーニングデータを作成するために活用できる既存の履歴データがあるかもしれないからです。(逆にbackfillできないと、今から集めたデータだけを使って学習用・推論用データを作らなきゃいけなくなっちゃう。あ、下に同じことが書いてあった...!:thinking:)
If you couldn’t backfill features, you could start logging features in your production system and wait until sufficient data has been collected before you start training your model. 
もし特徴量をバックフィルできなければ、プロダクションシステムで機能のログを取り始め、モデルのトレーニングを開始する前に十分なデータが収集されるのを待つことになります。
<!-- ここまで読んだ! -->

### Point-in-Time Correct Training Data 時点正確なトレーニングデータ

If you want to create training data from time-series feature data without any future data leakage, you will need to perform a temporal join, sometimes called a point-in-time correct join.
時系列特徴データから未来のデータ漏洩なしにトレーニングデータを作成したい場合、時点正確な結合（point-in-time correct join）と呼ばれる時間的結合を行う必要があります。

For example, in the figure below, we can see that for the (red) label value, the correct feature values for Feature A and Feature B are 4 and 6, respectively.
例えば、以下の図では、（赤い）ラベル値に対して、特徴Aと特徴Bの正しい特徴値はそれぞれ4と6であることがわかります。
Data leakage would occur if we included feature values that are either the pink (future data leakage) or orange values (stale feature data).
ピンク（未来のデータ漏洩）またはオレンジの値（古い特徴データ）のいずれかの特徴値を含めると、データ漏洩が発生します。(古い特徴量も確かにそうか、これもデータリークって言うのか...!::thinking:)
If you do not create point-in-time correct training data, your model may perform poorly and it will be very difficult to discover the root cause of the poor performance.
時点正確なトレーニングデータを作成しないと、モデルのパフォーマンスが悪化し、その悪化の根本原因を特定することが非常に難しくなります。

If your offline store supports AsOf Joins, feature retrieval involves joining Feature A and Feature B from their respective tables AsOf the timestamp value for each row in the Label table.
オフラインストアがAsOf Joinsをサポートしている場合、特徴の取得は、ラベルテーブルの各行のタイムスタンプ値に基づいて、特徴Aと特徴Bをそれぞれのテーブルから結合することを含みます。
The SQL query to create training data is an “AS OF LEFT JOIN”, as this query enforces the invariant that for every row in your Label table, there should be a row in your training dataset, and if there are missing feature values for a join, we should include NULL values (we can later impute missing values in model-dependent transformations).
トレーニングデータを作成するためのSQLクエリは「AS OF LEFT JOIN」であり、このクエリは**ラベルテーブルの各行に対してトレーニングデータセットに行が存在するべきであるという不変条件を強制**します。また、結合に対して欠損している特徴値がある場合はNULL値を含めるべきです（後でモデル依存の変換で欠損値を補完できます）。
If your offline store does not support AsOf Joins, you can write alternative windowing code using state tables.
オフラインストアがAsOf Joinsをサポートしていない場合、状態テーブルを使用して代替のウィンドウコードを書くことができます。
(まあ基本サポートしてる気がする...!:thinking:)

![]()

As both AsOf Left joins and window tables result in complex SQL queries, many feature stores provide domain-specific language (DSL) support for executing the temporal query.
AsOf Left joinsとウィンドウテーブルの両方が複雑なSQLクエリを生成するため、多くのフィーチャーストアは時間的クエリを実行するためのドメイン固有言語（DSL）サポートを提供しています。
The following code snippet, in Hopsworks, creates point-in-time-consistent training data by first creating a feature view.
以下のコードスニペットは、Hopsworksで最初にフィーチャービューを作成することによって、時点正確なトレーニングデータを作成します。
The code starts by (1) selecting the columns to use as features and label(s) to use for the model, then (2) creates a feature view with the selected columns, defining the label column(s), and (3) uses the feature view object to create a point-in-time correct snapshot of training data.
コードは、（1）モデルに使用する特徴およびラベルとして使用する列を選択し、次に（2）選択した列でフィーチャービューを作成し、ラベル列を定義し、（3）フィーチャービューオブジェクトを使用して**時点正確なトレーニングデータのスナップショットを作成**します。

```python
fg_loans = fs.get_feature_group(name="loans", version=1)
fg_applicants = fs.get_feature_group(name="applicants", version=1)
select= fg_loans.select_except(["issue_d", "id"]).join(\
            fg_applicants.select_except(["earliest_cr_line", "id"]))
 
fv = fs.create_feature_view(name="loans_approvals", 
            version=1,
            description="Loan applicant data",
            labels=["loan_status"],
            query=select
            )
X_train, X_test, y_train, y_test = fv.train_test_split(test_size=0.2)
#....
model.fit(X_train, y_train)
```

The following code snippet, in Hopsworks, uses the feature view we just defined to create point-in-time consistent batch inference data.
以下のコードスニペットは、Hopsworksで、先ほど定義したフィーチャービューを使用して、時点正確なバッチ推論データを作成します。
The model makes predictions using the DataFrame df containing the batch inference data.
モデルは、バッチ推論データを含むDataFrame dfを使用して予測を行います。
(バッチ推論の場合は、event_timeは一律で現在時刻でいいはず...!:thinking:)

```python
fv = fs.get_feature_view(name="loans_approvals", version=fv_version) 
df = fv.get_batch_data(start_time=”2023-12-23 00:00”, end_time=NOW)

predictions_df = model.predict(df)
```

<!-- ここまで読んだ! -->


### History and Context for Online Models オンラインモデルの歴史と文脈

Online models are often hosted in model-serving infrastructure or stateless (AI-enabled) applications. 
オンラインモデルは、モデル提供インフラストラクチャやステートレス（AI対応）アプリケーションでホストされることが多いです。
In many user-facing applications, the actions taken by users are “information poor”, but we would still like to use a trained model to make an intelligent decision. 
多くのユーザー向けアプリケーションでは、ユーザーが取る行動は「情報が乏しい」ですが、それでも訓練されたモデルを使用してインテリジェントな決定を下したいと考えています。
For example, in Tiktok, a user click contains a limited amount of information - you could not build the world’s best real-time recommendation system using just a single user click as an input feature. 
**例えば、Tiktokでは、ユーザのクリックには限られた情報しか含まれておらず、単一のユーザクリックを入力特徴として使用するだけでは、世界最高のリアルタイム推薦システムを構築することはできません**。

The solution is to use the user’s ID to retrieve precomputed features from the online store containing the user's personal history as well as context features (such as what videos or searches are trending). 
解決策は、ユーザのIDを使用して、ユーザの個人履歴やコンテキスト特徴（どの動画や検索がトレンドになっているかなど）を含むオンラインストアから事前計算された特徴を取得することです。
The precomputed features returned enrich any features that can be computed from the user input to build a rich feature vector that can be used to train complex ML models. 
返された事前計算された特徴は、ユーザー入力から計算できる特徴を豊かにし、複雑な機械学習モデルを訓練するために使用できる豊富な特徴ベクトルを構築します。
For example, in Tiktok, you can retrieve precomputed features about the 10 most recent videos you looked at - their category, how long you engaged for, what’s trending, what your friends are looking at, and so on. 
**例えば、Tiktokでは、最近見た10本の動画に関する事前計算された特徴量を取得できます - それらのカテゴリ、どれくらいの時間関与したか、何がトレンドになっているか、友達が何を見ているかなど**です。
In many examples of online models, the entity is a simple user or product or booking. 
多くのオンラインモデルの例では、エンティティは単純なユーザー、製品、または予約です。
However, often you will need more complex data models, and it is beneficial if your online store supports multi-part primary keys (see Uber talk). 
しかし、しばしばより複雑なデータモデルが必要となり、**オンラインストアが複数部分の主キーをサポートしていると有益**です（Uberのトークを参照）。
(例えば(user_id, item_id)みたいな複数カラムの主キーってことだろうか?? Sagemaker Feature Storeだと単一カラムの主キーしか対応してなさそう:thinking:)

<!-- ここまで読んだ! -->

### Feature Reuse 特徴の再利用
(Feature Storeがあれば、特徴量の使い回しできてめっちゃ楽だよ！って話)

A common problem faced by organizations when they build their first ML models is that there is a lot of bespoke tooling, extracting data from existing backend systems so that it can be used to train a ML model. 
**組織が最初の機械学習（ML）モデルを構築する際に直面する一般的な問題は、多くの特注ツールが必要であり、既存のバックエンドシステムからデータを抽出してMLモデルのトレーニングに使用すること**です。
Then, when it comes to productionizing the ML model, more data pipelines are needed to continually extract new data and compute features so that the model can make continual predictions on the new feature data. 
次に、MLモデルを本番環境に展開する際には、新しいデータを継続的に抽出し、特徴を計算するために、さらに多くのデータパイプラインが必要になります。これにより、モデルは新しい特徴データに基づいて継続的に予測を行うことができます。

- 上記の内容の例:
  - 最初にMLモデルを作るとき...
    - 「うわー、バックエンドDBから直接データ引っこ抜いて…」
    - 「CSVこねくり回して…」
    - 「学習用の特徴量作った〜！やった〜！」
  - → で、モデルを本番運用するときに、
    - 「あ、リアルタイムでこの特徴量作らないとダメじゃん」
    - 「本番用に別パイプライン作るか〜」
  - みたいな感じで、トレーニング用・本番用で別々にデータ準備しちゃうことが多い!

However, after the first set of pipelines have been written for the first model, organizations soon notice that one or more features used in an earlier model are needed in a new model. 
しかし、最初のモデルのために最初の一連のパイプラインが書かれた後、組織はすぐに、以前のモデルで使用された1つまたは複数の特徴が新しいモデルに必要であることに気付きます。
Metareported that in their feature store “most features are used by many models”, and that the most popular 100 features are reused in over 100 different models. 
**Metaは、彼らの特徴ストアで「ほとんどの特徴は多くのモデルで使用されている」と報告し、最も人気のある100の特徴が100以上の異なるモデルで再利用されていることを示しました。**
(よって、使い回す前提で設計した方が絶対とく...!:thinking:)
However, for expediency, developers typically rewrite the data pipelines for the new model. 
しかし、迅速さのために、開発者は通常、新しいモデルのためにデータパイプラインを再作成します。
Now you have different models re-computing the same feature(s) with different pipelines. This leads to waste, and a less maintainable (non-DRY) code base. 
これにより、**異なるモデルが異なるパイプラインで同じ特徴を再計算することになります。これは無駄を生じさせ、メンテナンスが難しい（非DRY）コードベースにつながります。**
(無駄なストレージ、無駄な計算資源...!:thinking:)

The benefits of feature reuse with a feature store include higher quality features through increased usage and scrutiny, reduced storage costs - and less feature pipelines. 
特徴ストアを使用した特徴の再利用の利点には、使用頻度と精査の増加による高品質な特徴、ストレージコストの削減、そして特徴パイプラインの削減が含まれます。
In fact, the feature store decouples the number of models you run in production from the number of feature pipelines you have to maintain. 
**実際、特徴ストアは、本番環境で実行するモデルの数と、維持しなければならない特徴パイプラインの数を切り離します**。(この観点大事だ...! 言い換えるとFTI Pipelines Architectureの利点でもある!)
Without a feature store, you typically write at least one feature pipeline per model. 
特徴ストアがない場合、通常はモデルごとに少なくとも1つの特徴パイプラインを書く必要があります。
With a (large enough) feature store, you may not need to write any feature pipeline for your model if the features you need are already available there. 
（十分に大きな）特徴ストアがあれば、必要な特徴がすでにそこに存在する場合、モデルのために特徴パイプラインを書く必要がないかもしれません。

<!-- ここまで読んだ! -->

### Multiple Feature Computation Models 複数の特徴計算モデル

The feature pipeline typically does not need GPUs, may be a batch program or streaming program, and may process small amounts of data with Pandas or Polars or large amounts of data with a framework such as Spark or DBT/SQL.
特徴パイプラインは通常、GPUを必要とせず、バッチプログラムまたはストリーミングプログラムであり、PandasやPolarsを使用して少量のデータを処理するか、SparkやDBT/SQLのようなフレームワークを使用して大量のデータを処理することがあります。
Streaming feature pipelines can be implemented in Python (Bytewax) or more commonly in distributed frameworks such as PySpark, with its micro-batch computation model, or Flink/Beam with their lower latency per-event computation model.
ストリーミング特徴パイプラインは、Python（Bytewax）で実装することもできますが、より一般的には、マイクロバッチ計算モデルを持つPySparkや、イベントごとの低遅延計算モデルを持つFlink/Beamのような分散フレームワークで実装されます。

The training pipeline is typically a Python program, as most ML frameworks are written in Python.
トレーニングパイプラインは通常、Pythonプログラムであり、ほとんどの機械学習フレームワークはPythonで書かれています。
It reads features and labels as input, trains a model and outputs the trained model (typically to a model registry).
それは特徴とラベルを入力として読み込み、モデルをトレーニングし、トレーニングされたモデルを出力します（通常はモデルレジストリに）。

An inference pipeline then downloads a trained model and reads features as input (some may be computed from the user’s request, but most will be read as precomputed features from the feature store).
次に、推論パイプラインはトレーニングされたモデルをダウンロードし、特徴を入力として読み込みます（**いくつかはユーザのリクエストから計算される場合がありますが、ほとんどは特徴ストアから事前計算された特徴として読み込まれます**）。
Finally, it uses the features as input to the model to make predictions that are either returned to the client who requested them or stored in some data store (often called an inference store) for later retrieval.
最後に、それは特徴をモデルへの入力として使用して予測を行い、それらはリクエストしたクライアントに返されるか(リアルタイム推論...!)、**後で取得するために何らかのデータストア（しばしば推論ストアと呼ばれる）に保存されます(バッチ推論...!)**。

<!-- ここまで読んだ! -->

### Validate Feature Data and Monitor for Drift 特徴データの検証とドリフトの監視

Garbage-in, garbage out is a well known adage in the data world. 
「ゴミが入ればゴミが出る」というのはデータの世界でよく知られた格言です。
Feature stores can provide support for validating feature data in feature pipelines. 
フィーチャーストアは、**フィーチャーパイプラインにおけるフィーチャーデータの検証**をサポートすることができます。
(feature validationはfeature pipelineの中でやるべきなのかな...??:thinking:)
The following code snippet uses the Great Expectations library to define a data validation rule that is applied when feature data is written to a feature group in Hopsworks. 
以下のコードスニペットは、Great Expectationsライブラリを使用して、**フィーチャーデータがHopsworksのフィーチャーグループに書き込まれるときに適用されるデータ検証ルール**を定義します。(feature storeに書き込まれるタイミングでvalidationするんだ...!:thinking:)

```python
df = # read from data source, then perform feature engineering


# define data validation rules in Great Expectations
ge_suite = ge.core.ExpectationSuite(
    expectation_suite_name="expectation_suite_101"
    )

ge_suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column":"'search_term'"}
    )
)

fg = fs.get_or_create_feature_group(name="query_terms_yearly",
                              version=1,
                              description="Count of search term by year",
                              primary_key=['year', 'search_term'],
                              partition_key=['year'],
                              online_enabled=True,
                              expectation_suite=ge_suite
                              )
fg.insert(df) # data validation rules executed in client before insertion
```

The data validation results can then be viewed in the feature store, as shown below. 
データ検証結果は、以下に示すようにフィーチャーストアで確認できます。
In Hopsworks, you can trigger alerts if data validation fails, and you can decide whether to allow the insertion or fail the insertion of data, if data validation fails. 
Hopsworksでは、データ検証が失敗した場合にアラートをトリガーすることができ、データ検証が失敗した場合に挿入を許可するか、挿入を失敗させるかを決定できます。

Feature monitoring is another useful capability provided by many feature stores. 
**Feature monitoringは、多くのフィーチャーストアが提供するもう一つの便利な機能**です。(あ、これはvalidationというよりはdrift監視みたいな話か...!前者は特徴量ストアに保存するときに実行されて、後者は特徴量ストアの中で定期的もしくはon-demandで実行されるイメージかな...!:thinking:)
Whether you build a batch ML system or an online ML system, you should be able to monitor inference data for the system’s model to see if it is statistically significantly different from the model’s training data (data drift). 
バッチMLシステムを構築する場合でもオンラインMLシステムを構築する場合でも、システムのモデルに対する**推論データを監視し、それがモデルのトレーニングデータ（データドリフト）と統計的に有意に異なるかどうかを確認できる必要があります**。
If it is, you should alert users and ideally kick-off the retraining of the model using more recent training data. 
もし異なる場合は、ユーザ(=開発者)にアラートを通知し、**理想的にはより最近のトレーニングデータを使用してモデルの再トレーニングを開始するべき**です。

Here is an example code snippet from Hopsworks for defining a feature monitoring rule for the feature “amount” in the model’s prediction log (available for both batch and online ML systems). 
以下は、モデルの予測ログにおけるフィーチャー「amount」のフィーチャー監視ルールを定義するためのHopsworksからのコードスニペットの例です（バッチおよびオンラインMLシステムの両方で利用可能です）。
A job is run once per day to compare inference data for the last week for the amount feature, and if its mean value deviates more than 50% from the mean observed in the model’s training data, data drift is flagged and alerts are triggered. 
**ジョブは、amountフィーチャーの過去1週間の推論データを比較するために1日1回実行され、その平均値がモデルのトレーニングデータで観測された平均から50%以上逸脱した場合、データドリフトがフラグされ、アラートがトリガーされます**。
(この場合のデータdriftの監視は、バッチで行われるイメージなんだ。理想的にはこれもストリーミング的に実行される方が良い、というブログを見たな...!:thinking:)

```python
# Compute statistics on a prediction log as a detection window
fg_mon = pred_log.create_feature_monitoring("name", 
    feature_name = "amount", job_frequency = "DAILY")
    .with_detection_window(row_percentage=0.8, time_offset ="1w")

# Compare feature statistics with a reference window - e.g., training data
fg_mon.with_reference_training_dataset(version=1).compare_on(
    metric = "mean", threshold=50)
```

<!-- ここまで読んだ! -->

### Taxonomy of Data Transformations データ変換の分類

When data scientists and data engineers talk about data transformations, they are not talking about the same thing. 
データサイエンティストとデータエンジニアがデータ変換について話すとき、彼らは同じことを話しているわけではありません。
This can cause problems in communication, but also in the bigger problem of feature reuse in feature stores. 
これはコミュニケーションの問題を引き起こす可能性がありますが、フィーチャーストアにおけるフィーチャー再利用のより大きな問題にもつながります。 
There are 3 different types of data transformations, and they belong in different ML pipelines. 
**データ変換には3つの異なるタイプがあり、それぞれ異なるMLパイプラインに属します**。 

![]()

Data transformations, as understood by data engineers, is a catch-all term that covers data cleansing, aggregations, and any changes to your data to make it consumable by BI or ML. 
データエンジニアが理解するデータ変換は、データクレンジング、集約、およびBIやMLで消費可能にするためのデータの変更を含む包括的な用語です。 
These data transformations are called model-independent transformations as they produce features that are reusable by many models. 
これらのデータ変換は、**さまざまなモデルで再利用可能な特徴を生成するため、model-independent transformations(モデル非依存な変換)**と呼ばれます。
(i.e. どのモデルでも再利用できる汎用的な特徴量を作る処理!:thinking:)

In data science, data transformations are a more specific term that refers to encoding a variable (categorical or numerical) into a numerical format, scaling a numerical variable, or imputing a value for a variable, with the goal of improving the performance of your ML model training. 
データサイエンスにおいて、データ変換は、変数（カテゴリカルまたは数値）を数値形式にエンコードしたり、数値変数をスケーリングしたり、変数の値を補完したりすることを指すより具体的な用語であり、MLモデルのトレーニングのパフォーマンスを向上させることを目的としています。 
These data transformations are called model-dependent transformations and they are specific to one model. 
これらのデータ変換は**model-dependent transformations(モデル依存な変換)**と呼ばれ、特定の1つのモデルに特有です。 
(カテゴリ変数をone-hot encodingしたり、数値特徴量を標準化したり、欠損値を埋めたり...は、各モデルの精度を上げるために個別に細かくチューニングするもの...!:thinking:)

Finally, there are data transformations that can only be performed at runtime for online models as they require parameters only available in the prediction request. 
最後に、オンラインモデルの実行時にのみ実行できるデータ変換があり、これは予測リクエストでのみ利用可能なパラメータを必要とします。 
These data transformations are called on-demand transformations, but they may also be needed in feature pipelines if you want to backfill feature data from historical data. 
これらのデータ変換は**on-demand transformations(オンデマンド変換)**と呼ばれますが、**過去のデータからフィーチャーデータをバックフィルする場合、フィーチャーパイプラインでも必要になることがある**。
(ここどうしても難しそうだな...! なるべく同じ特徴量生成ロジックを維持できるようにしないと...!ロジックをPythonモジュール化して同じ関数を呼び出すようにするとか。:thinking:)

The feature store architecture diagram from earlier shows that model-independent transformations are only performed in feature pipelines (whether batch or streaming pipelines). 
前述のフィーチャーストアアーキテクチャ図は、**モデル非依存変換がフィーチャーパイプライン（バッチまたはストリーミングパイプラインのいずれか）でのみ実行されること**を示しています。(つまり学習 & 推論パイプラインには含まれるべきではない!)
However, model-dependent transformations are performed in both training and inference pipelines, and on-demand transformations can be applied in both feature and online inference pipelines. 
しかし、**モデル依存変換はトレーニングパイプラインと推論パイプラインの両方で実行され**(つまりfeature pipelineには含まれるべきではない!)、**オンデマンド変換はフィーチャーパイプラインとオンライン推論パイプラインの両方に適用**できます。
You need to ensure that equivalent transformations are performed in both pipelines - if there is skew between the transformations, you will have model performance bugs that will be very hard to identify and debug. 
両方のパイプラインで同等の変換が実行されることを確認する必要があります。変換間に偏りがある場合、モデルのパフォーマンスバグが発生し、特定やデバッグが非常に困難になります。 
Feature stores help prevent this problem of online-offline skew. 
フィーチャーストアは、オンラインとオフラインの偏りの問題を防ぐのに役立ちます。 
For example, model-dependent transformations can be performed in scikit-learn pipelines or in feature views in Hopsworks, ensuring consistent transformations in both training and inference pipelines. 
たとえば、モデル依存変換はscikit-learnパイプラインやHopsworksのフィーチャービューで実行でき、トレーニングパイプラインと推論パイプラインの両方で一貫した変換が保証されます。
(まあ同じ関数を呼び出せるようにする、ってことだよね...!:thinking:)
Similarly, on-demand transformations are version-controlled Python or Pandas user-defined functions (UDFs) in Hopsworks that are applied in both feature and online inference pipelines. 
同様に、オンデマンド変換はHopsworksのバージョン管理されたPythonまたはPandasのユーザー定義関数（UDF）であり、フィーチャーパイプラインとオンライン推論パイプラインの両方に適用されます。
(これもまあ同じ関数を呼び出せるようにする、ってことだよね...!:thinking:)

<!-- ここまで読んだ! -->

- つまり...この辺りが整理して運用できてないと...
  - モデル依存変換の場合は学習パイプラインと推論パイプラインで、on-demand変換の場合は推論パイプラインとfeature pipelineで、特徴量作成ロジックにズレが生じうる...!
  - -> 学習時と推論時で data skew問題が発生する...!

<!-- ここまで読んだ! --> 

### Query Engine for Point-in-Time Consistent Feature Data for Training トレーニング用の時点整合性のある特徴データのためのクエリエンジン

Feature stores can use existing columnar data stores and data processing engines, such as Spark, to create point-in-time correct training data. 
フィーチャーストアは、既存のカラム型データストアやデータ処理エンジン（例：Spark）を使用して、時点整合性のある正しいトレーニングデータを作成できます。 
However, as of December 2023, Spark, BigQuery, Snowflake, and Redshift do not support the ASOF LEFT JOIN query that is used to create training data from feature groups. 
**しかし、2023年12月現在、Spark、BigQuery、Snowflake、およびRedshiftは、フィーチャーグループからトレーニングデータを作成するために使用されるASOF LEFT JOINクエリをサポートしていません**。(あ、そうなのか!:thinking:)
Instead, they have to implement stateful windowed approaches. 
その代わりに、状態を持つウィンドウアプローチを実装する必要があります。 

![]()

The other main performance bottleneck with many current data warehouses is that they provide query interfaces to Python with either a JDBC or ODBC API. 
現在の多くのデータウェアハウスにおけるもう一つの主要なパフォーマンスボトルネックは、JDBCまたはODBC APIを介してPythonにクエリインターフェースを提供していることです。 
These are row-oriented protocols, and data from the offline store needs to be pivoted from columnar format to row-oriented, and then back to column-oriented in Pandas. 
これらは行指向のプロトコルであり、オフラインストアからのデータはカラム型フォーマットから行指向にピボットされ、その後Pandasで再びカラム指向に戻す必要があります。 
Arrow is now the backing data format for Pandas 2.+. 
Arrowは現在、Pandas 2.+のバックデータフォーマットです。 

In open-source, reproducible benchmarks by KTH, Karolinska, and Hopsworks, they showed the throughput improvements over a specialist DuckDB/ArrowFlight feature query engine that returns Pandas DataFrames to Python clients in training and batch inference pipelines. 
KTH、Karolinska、およびHopsworksによるオープンソースの再現可能なベンチマークでは、トレーニングおよびバッチ推論パイプラインでPandas DataFrameをPythonクライアントに返す専門のDuckDB/ArrowFlightフィーチャークエリエンジンに対するスループットの改善が示されました。 
We can see from the table below that throughput improvements of 10-45X JDBC/ODBC-based query engines can be achieved. 
以下の表から、10-45倍のJDBC/ODBCベースのクエリエンジンのスループット改善が達成できることがわかります。

![]()

<!-- ここまで読んだ! -->

### Query Engine for Low Latency Feature Data for Online Inference
### オンライン推論のための低遅延フィーチャーデータのクエリエンジン

The online feature store is typically built on existing low latency row-oriented data stores. 
**オンラインフィーチャーストアは、通常、既存の低遅延の行指向データストアに基づいて構築**されます。
These could be key-value stores such as Redis or Dynamo or a key-value store with a SQL API, such as RonDB for Hopsworks. 
これには、RedisやDynamoのようなキー-バリューストア、またはHopsworksのためのSQL APIを持つキー-バリューストア（例：RonDB）が含まれます。

The process of building the feature vector for an online model also involves more than just retrieving precomputed features from the online feature store using an entity ID. 
**オンラインモデルのためのフィーチャーベクトルを構築するプロセスは、エンティティIDを使用してオンラインフィーチャーストアから事前計算されたフィーチャーを取得するだけではありません**。(前述されてた3つの分類のうちの、リアルタイム変換の話か...!)
Some features may be passed as request parameters directly and some features may be computed on-demand - using either request parameters or data from some 3rd party API, only available at runtime. 
いくつかのフィーチャーはリクエストパラメータとして直接渡される場合があり、他のフィーチャーはオンデマンドで計算される場合があります - リクエストパラメータまたは実行時にのみ利用可能なサードパーティAPIからのデータを使用します。
These on-demand transformations may even need historical feature values, inference helper columns, to be computed. 
これらのオンデマンド変換は、計算される必要がある履歴フィーチャー値や推論ヘルパーカラムを必要とする場合もあります。

In the code snippet below, we can see how an online inference pipeline takes request parameters in the predict method, computes an on-demand feature, retrieves precomputed features using the request supplied id, and builds the final feature vector used to make the prediction with the model. 
以下のコードスニペットでは、オンライン推論パイプラインがpredictメソッドでリクエストパラメータを受け取り、オンデマンドフィーチャーを計算し、リクエストで提供されたidを使用して事前計算されたフィーチャーを取得し、モデルで予測を行うために使用される最終的なフィーチャーベクトルを構築する方法を示しています。

```python
def loc_diff(event_ts, cur_loc) :
    return grid_loc(event_ts, cur_loc)

def predict(id, event_ts, cur_loc, amount) :
    f1 = loc_diff(event_ts, cur_loc)
    df = feature_view.get_feature_vector(
        entry = {"id": id},
        passed_features = {"f1": f1, "amount": amount}
    )
    return model.predict(df)
```

In the figure below, we can see important system properties for online feature stores. 
以下の図では、オンラインフィーチャーストアの重要なシステム特性を見ることができます。
If you are building your online AI application on top of an online feature store, it should have LATS properties (low Latency, high Availability, high Throughput, and scalable Storage), and it should also support fresh features (through streaming feature pipelines). 
オンラインフィーチャーストアの上にオンラインAIアプリケーションを構築している場合、それはLATS特性（低遅延、高可用性、高スループット、スケーラブルストレージ）を持ち、また新鮮なフィーチャー（ストリーミングフィーチャーパイプラインを通じて）をサポートする必要があります。

![]()

Some other important technical and performance considerations here for the online store are: 
オンラインストアに関する他の重要な技術的およびパフォーマンスの考慮事項は次のとおりです：

- Projection pushdown can massively reduce network traffic and latency. プロジェクションプッシュダウンは、ネットワークトラフィックと遅延を大幅に削減できます。
When you have popular features in feature groups with lots of columns, your model may only require a few features. 
多くのカラムを持つフィーチャーグループに人気のフィーチャーがある場合、モデルは数個のフィーチャーのみを必要とするかもしれません。
Projection pushdown only returns the features you need. 
プロジェクションプッシュダウンは、必要なフィーチャーのみを返します。
Without projection pushdown (e.g., most key-value stores), the entire row is returned and the filtering is performed in the client. 
プロジェクションプッシュダウンがない場合（例：ほとんどのキー-バリューストア）、全行が返され、フィルタリングはクライアントで行われます。
For rows of 10s of KB, this could mean 100s of times more data is transferred than needed, negatively impacting latency and throughput (and potentially also cost). 
10sのKBの行の場合、必要なデータの100倍以上のデータが転送される可能性があり、遅延とスループットに悪影響を及ぼす（そして潜在的にコストにも影響を与える）可能性があります。

- Your feature store should support a normalized data model, not just a star schema. 
- フィーチャーストアは、スタースキーマだけでなく、正規化されたデータモデルをサポートする必要があります。
For example, if your user provides a booking reference number that is used as the entity ID, can your online store also return features for the user and products referenced in the booking, or does either the user or application have to provide the user ID and product ID? 
例えば、ユーザーがエンティティIDとして使用される予約参照番号を提供した場合、オンラインストアは予約に参照されるユーザーや製品のフィーチャーも返すことができますか、それともユーザーまたはアプリケーションのいずれかがユーザーIDと製品IDを提供する必要がありますか？
For high performance, your online store should support pushdown LEFT JOINs to reduce the number of database round trips for building features from multiple feature groups. 
高パフォーマンスのために、オンラインストアは複数のフィーチャーグループからフィーチャーを構築するためのデータベースの往復回数を減らすために、プッシュダウンLEFT JOINをサポートする必要があります。

<!-- ここまで読んだ! 良くわからんかった! -->

### Query Engine to find similar Feature Data using Embeddings 埋め込みを使用して類似の特徴データを見つけるクエリエンジン

Real-time ML systems often use similarity search as a core functionality. 
リアルタイムの機械学習システムは、しばしば類似性検索をコア機能として使用します。 
For example, personalized recommendation engines typically use similarity search to generate candidates for recommendation, and then use a feature store to retrieve features for the candidates, before a ranking model personalizes the candidates for the user.
例えば、パーソナライズされた推薦エンジンは、通常、類似性検索を使用して推薦候補を生成し、その後、フィーチャーストアを使用して候補の特徴を取得し、最後にランキングモデルがユーザーのために候補をパーソナライズします。(うんうん、2-stages推薦ね。:thinking:)

The example code snippet below is from Hopsworks, and shows how you can search for similar rows in a feature group with the text “Happy news for today” in the embedding_body column.
以下の例のコードスニペットはHopsworksからのもので、embedding_body列に「Happy news for today」というテキストを含むフィーチャーグループ内で類似の行を検索する方法を示しています。
(ちなみにSagemaker Feature Storeは近似近傍探索の機能はなさそうだった)

```python
news_desc="Happy news for today"
df=news_fg.find_neighbors(model.encode(news_desc), k=3)
# df now contains rows with 'news_desc' values that are most similar to 'news_desc'
```

<!-- ここまで読んだ! -->

## Do I need a feature store? 特徴ストアは必要ですか？

Feature stores have historically been part of big data ML platforms, such as Uber’s Michelangelo, that manage the entire ML workflow, from specifying feature logic, to creating and operating feature pipelines, training pipelines, and inference pipelines.
特徴ストアは、これまでのところ、UberのMichelangeloのようなビッグデータMLプラットフォームの一部であり、特徴ロジックの指定から、特徴パイプライン、トレーニングパイプライン、推論パイプラインの作成と運用まで、MLワークフロー全体を管理します。

More recent open-source feature stores provide open APIs enabling easy integration with existing ML pipelines written in Python, Spark, Flink, or SQL.
最近のオープンソースの特徴ストアは、Python、Spark、Flink、またはSQLで書かれた既存のMLパイプラインとの簡単な統合を可能にするオープンAPIを提供します。
Serverless feature stores further reduce the barriers of adoption for smaller teams.
サーバーレス特徴ストアは、より小規模なチームの採用の障壁をさらに低くします。
The key features needed by most teams include APIs for consistent reading/writing of point-in-time correct feature data, monitoring of features, feature discovery and reuse, and the versioning and tracking of feature data over time.
**ほとんどのチームが必要とする主要な機能には、時点で正確な特徴データの一貫した読み書きのためのAPI、特徴の監視、特徴の発見と再利用、そして時間の経過に伴う特徴データのバージョン管理と追跡**が含まれます。
Basically, feature stores are needed for MLOps and governance.
基本的に、特徴ストアはMLOpsとガバナンスに必要です。
Do you need Github to manage your source code? No, but it helps.
ソースコードを管理するためにGithubは必要ですか？いいえ、しかし役に立ちます。
Similarly, do you need a feature store to manage your features for ML? No, but it helps.
同様に、MLのために特徴を管理するために特徴ストアは必要ですか？いいえ、しかし役に立ちます。

<!-- ここまで読んだ! -->

## What is the difference between a feature store and a vector database? 　特徴ストアとベクトルデータベースの違いは何ですか？

Both feature stores and vector databases are data platforms used by machine learning systems. 
特徴ストアとベクトルデータベースは、どちらも機械学習システムで使用されるデータプラットフォームです。
The feature store stores feature data and provides query APIs for efficient reading of large volumes feature data (for model training and batch inference) and low latency retrieval of feature vectors (for online inference). 
特徴ストアは特徴データを保存し、大量の特徴データ（モデルのトレーニングやバッチ推論用）を効率的に読み取るためのクエリAPIと、特徴ベクトル（オンライン推論用）を低遅延で取得するためのクエリAPIを提供します。
In contrast, a vector database provides a query API to find similar vectors using approximate nearest neighbour (ANN) search. 
対照的に、**ベクトルデータベースは近似最近傍（ANN）検索を使用して類似ベクトルを見つけるためのクエリAPIを提供**します。

The indexing and data models used by feature stores and vector databases are very different. 
特徴ストアとベクトルデータベースで使用されるインデックスとデータモデルは非常に異なります。
The feature store has two data stores - an offline store, typically a data warehouse/lakehouse, that is a columnar database with indexes to help improve query performance such as (file) partitioning based on a partition column, skip indexes (skip files when reading data using file statistics), and bloom filters (which files to skip when looking for a row). 
**特徴ストアには2つのデータストアがあります**。オフラインストアは通常、データウェアハウス/レイクハウスであり、クエリパフォーマンスを向上させるためのインデックスを持つ列指向データベースです。これには、パーティション列に基づく（ファイル）パーティショニング、スキップインデックス（ファイル統計を使用してデータを読み取る際にスキップするファイル）、およびブルームフィルター（行を探すときにスキップするファイル）が含まれます。
The online store is a row-oriented database with indexes to help improve query performance such as a hash index to lookup a row, a tree index (such as a b-tree) for efficient range queries and row lookups, and a log-structured merge-tree (for improved write performance). 
オンラインストアは、行を検索するためのハッシュインデックス、効率的な範囲クエリと行検索のためのツリーインデックス（b-treeなど）、および書き込みパフォーマンスを向上させるためのログ構造マージツリーを持つ行指向データベースです。
In contrast, the vector database stores its data in a vector index that supports ANN search, such as FAISS (Facebook AI Similarity Search) or ScaNN by Google. 
対照的に、ベクトルデータベースは、FAISS（Facebook AI Similarity Search）やGoogleのScaNNなど、**ANN検索をサポートするベクトルインデックスにデータを保存**します。
(と言っても、HopsworksのFeature Storeは機能の一つとして、ベクトルDBをサポートしてるってことだよね...!:thinking:)

<!-- ここまで読んだ! -->

## Is there an integrated feature store and vector database? 統合されたフィーチャーストアとベクターデータベースは存在するか？

Hopsworks is a feature store with an integrated vector database. 
Hopsworksは、統合されたベクターデータベースを持つフィーチャーストアです。(だよね!)
You store tables of feature data in feature groups, and you can index a column that contains embeddings in a built-in vector database. 
フィーチャーグループにフィーチャーデータのテーブルを保存し、組み込みのベクターデータベースに埋め込みを含む列をインデックス化することができます。
This means you can search for rows of similar features using embeddings and ANN search. 
これは、埋め込みとANN検索を使用して、類似のフィーチャーの行を検索できることを意味します。
Hopsworks also supports filtering, so you can search for similar rows, but provide conditions on what type of data to return (e.g., only users whose age>18). 
Hopsworksはフィルタリングもサポートしているため、類似の行を検索できますが、返すデータの種類に条件を指定することができます（例：年齢が18歳以上のユーザーのみ）。

<!-- ここまで読んだ! -->

## Resources on feature stores 特徴ストアに関するリソース

Our research paper,"The Hopsworks Feature Store for Machine Learning", is the first feature store to appear at the top-tier database or systems conference SIGMOD 2024. 
私たちの研究論文「機械学習のためのHopsworksフィーチャーストア」は、SIGMOD 2024というトップレベルのデータベースまたはシステム会議に登場した最初のフィーチャーストアです。
This article series is describing in lay terms concepts and results from this study.
この記事シリーズでは、この研究からの概念と結果を平易な言葉で説明しています。

- Part 1: Modularity & Composability for AI Systems
- Part 1: AIシステムのためのモジュラリティとコンポーザビリティ
- Part 2: The Taxonomy for Data Transformations in AI Systems
- Part 2: AIシステムにおけるデータ変換の分類
- Part 3: Use all features: Snowflake Schema
- Part 3: すべての特徴を使用する：スノーフレークスキーマ
- Part 4: The Feature Store Makes Your Data Warehouse Easy to Use for AI
- Part 4: フィーチャーストアはデータウェアハウスをAIにとって使いやすくします
- Part 5: From Lakehouse to AI Lakehouse with a Python-Native Query Engine
- Part 5: レイクハウスからAIレイクハウスへ：Pythonネイティブクエリエンジンを使用して
- Part 6: RonDB: A Real-Time Database for Real-Time AI Systems
- Part 6: RonDB：リアルタイムAIシステムのためのリアルタイムデータベース
- Part 7: Reproducible Data for the AI Lakehouse
- Part 7: AIレイクハウスのための再現可能なデータ

<!-- ここまで読んだ! -->
