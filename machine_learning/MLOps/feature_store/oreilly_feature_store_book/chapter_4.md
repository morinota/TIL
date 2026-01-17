Part 2: Feature Stores

## 1. CHAPTER 4: Feature Stores 第4章: フィーチャーストア

As we have seen in the first three chapters, data management is one of the most challenging aspects of building and operating AI systems. 
最初の3章で見たように、**データ管理はAIシステムの構築と運用において最も困難な側面の1つ**です。
In the last chapter, we used a feature store to build our air quality forecasting system. 
前の章では、フィーチャーストアを使用して空気質予測システムを構築しました。
The feature store stored the output of the feature pipelines, provided training data for the training pipeline, and provided inference data for the batch inference pipeline. 
フィーチャーストアはフィーチャーパイプラインの出力を保存し、トレーニングパイプラインのためのトレーニングデータを提供し、バッチ推論パイプラインのための推論データを提供しました。
The feature store is a central data platform that stores, manages, and serves features for both training and inference. 
フィーチャーストアは、トレーニングと推論の両方のためのフィーチャーを保存、管理、提供する中央データプラットフォームです。
It also ensures consistency between features used in training and inference, and it enables the construction of modular AI systems by providing a shared data layer and well-defined APIs to connect FTI pipelines. 
また、トレーニングと推論で使用されるフィーチャー間の一貫性を確保し、FTIパイプラインを接続するための共有データレイヤーと明確に定義されたAPIを提供することで、モジュラーAIシステムの構築を可能にします。

<!-- ここから読んだ! -->

In this chapter, we will dive deeper into feature stores and answer the following questions: 
この章では、フィーチャーストアについてさらに深く掘り下げ、以下の質問に答えます。

- What problems does the feature store solve, and when do I need one? 
  - フィーチャーストアはどのような問題を解決し、いつ必要ですか？
- What is a feature group, how does it store data, and how do I write to one? 
  - フィーチャーグループとは何か、どのようにデータを保存し、どのように書き込むのですか？
- How do I design a data model for feature groups? 
  - フィーチャーグループのデータモデルをどのように設計しますか？
- How do I read feature data spread over many feature groups for training or inference? 
  - トレーニングまたは推論のために、多くのフィーチャーグループに分散したフィーチャーデータをどのように読み取りますか？

We will look at how feature stores are built from a columnar store, a row-oriented store, and a vector index. 
**フィーチャーストアがカラムストア、行指向ストア、ベクトルインデックスからどのように構築されるか**を見ていきます。
We will describe how feature stores solve challenges related to feature reuse, how to manage time-series data, and how to prevent skew between FTI pipelines. 
フィーチャーストアがフィーチャーの再利用に関連する課題をどのように解決し、時系列データをどのように管理し、FTIパイプライン間の偏りをどのように防ぐかを説明します。
And throughout the chapter, we will also weave in a motivating example of a real-time ML system that predicts credit card fraud. 
章全体を通して、クレジットカード詐欺を予測するリアルタイムMLシステムの動機付けとなる例も織り交ぜます。

<!-- ここまで読んだ! -->

### 1.1. A Feature Store for Fraud Prediction 詐欺予測のためのフィーチャーストア

We start by presenting the problem of how to design a feature store for an ML system that makes real-time fraud predictions for credit card transactions. 
まず、**クレジットカード取引のリアルタイム詐欺予測を行うMLシステムのためのフィーチャーストアをどのように設計するか**という問題を提示します。
The ML system card for the system is shown in Table 4-1. 
システムのMLシステムカードは表4-1に示されています。

![]()
_Table 4-1. ML system card for our real-time credit card fraud prediction service_ 
表4-1. リアルタイムクレジットカード詐欺予測サービスのMLシステムカード

The source data for our ML system comes from a data mart consisting of a data warehouse and an event-streaming platform, such as Apache Kafka or AWS Kinesis (see Figure 4-1). 
私たちのMLシステムのソースデータは、**データウェアハウスとApache KafkaやAWS Kinesisなどのイベントストリーミングプラットフォームで構成されるデータマート**から来ています（図4-1を参照）。
(基本的にはどこも同じような感じな気がする...!!:thinkink:)

![]()
_Figure 4-1. We design our feature store by identifying and creating features from the data sources, organizing the features into tables called feature groups, selecting features from different feature groups for use in a model by creating a feature view, and creating training/inference data with the feature view._  
図4-1. データソースからフィーチャーを特定し作成し、フィーチャーをフィーチャーグループと呼ばれるテーブルに整理し、モデルで使用するために異なるフィーチャーグループからフィーチャーを選択し、フィーチャービューを作成し、フィーチャービューを使用してトレーニング/推論データを作成します。

Starting from our data sources, we will learn how to build a feature store in four main steps: 
**データソースから始めて、フィーチャーストアを構築する方法を4つの主要なステップで**学びます。

1. Identify entities and features for those entities. 
   1. エンティティとそのエンティティのフィーチャーを特定します。

2. Organize entities into tables of features (feature groups) and identify relationships between feature groups.  
   1. エンティティをフィーチャーのテーブル（フィーチャーグループ）に整理し、フィーチャーグループ間の関係を特定します。

3. Select the features for a model, from potentially different feature groups, in a feature view. 
   1. フィーチャービュー内で、異なるフィーチャーグループからモデルのためのフィーチャーを選択します。

4. Retrieve data for model training and batch/online inference with the feature view. 
   1. フィーチャービューを使用してモデルのトレーニングとバッチ/オンライン推論のためのデータを取得します。

(上記の4ステップを意識しておきたい...!:thinking:)

This chapter will provide more details on what feature groups and feature views are, but before that, we will look at the history of feature stores, what makes up a feature store (its anatomy), and when you may need a feature store. 
この章では、フィーチャーグループとフィーチャービューが何であるかについての詳細を提供しますが、その前にフィーチャーストアの歴史、フィーチャーストアを構成するもの（その解剖学）、およびフィーチャーストアが必要な場合について見ていきます。

<!-- ここまで読んだ! -->

### 1.2. Brief History of Feature Stores フィーチャーストアの簡単な歴史

As mentioned in Chapter 1, Uber introduced the first feature store as part of its Michelangelo platform. 
第1章で述べたように、**UberはMichelangeloプラットフォームの一部として最初のフィーチャーストアを導入**しました。
Michelangelo includes a feature store (called Palette), a model registry, and model serving capabilities. 
Michelangeloにはフィーチャーストア（Paletteと呼ばれる）、モデルレジストリ、およびモデルサービング機能が含まれています。
Michelangelo also introduced a domain-specific language (DSL) to define feature pipelines. 
Michelangeloはまた、フィーチャーパイプラインを定義するためのドメイン特化型言語（DSL）を導入しました。
In the DSL, you define what type of feature to compute on what data source (such as counting the number of user clicks in the last seven days using a clicks table), and Michelangelo transpiles your feature definition into a Spark program and runs it on a schedule (for example, hourly or daily). 
DSLでは、どのデータソースでどのタイプのフィーチャーを計算するかを定義します（例えば、クリックテーブルを使用して過去7日間のユーザクリック数をカウントするなど）、そして**Michelangeloはフィーチャー定義をSparkプログラムに変換し、スケジュールに従って実行します（例えば、毎時または毎日）**。

<!-- ここまで読んだ! -->

In late 2018, Hopsworks introduced the first open source feature store. 
2018年末に、Hopsworksは最初のオープンソースフィーチャーストアを導入しました。
Hopsworks was also the first API-based feature store, where external pipelines read and write feature data using a DataFrame API and there is no built-in pipeline orchestration. 
**Hopsworksはまた、外部パイプラインがDataFrame APIを使用してフィーチャーデータを読み書きする最初のAPIベースのフィーチャーストア**であり、組み込みのパイプラインオーケストレーションはありません。
The API-based feature store enables you to write pipelines in different frameworks/languages (for example, Flink, PySpark, and Pandas). 
APIベースのフィーチャーストアは、異なるフレームワーク/言語（例えば、Flink、PySpark、Pandas）でパイプラインを書くことを可能にします。
In late 2019, the open source Feast feature store adopted the same API-based architecture for reading/writing feature data. 
2019年末に、オープンソースのFeastフィーチャーストアはフィーチャーデータの読み書きのために同じAPIベースのアーキテクチャを採用しました。
Now, feature stores from GCP, AWS, and Databricks follow the API-based architecture, while the most popular DSL-based feature store is Tecton. 
現在、GCP、AWS、Databricksのフィーチャーストアは**APIベースのアーキテクチャ**に従っており、最も人気のあるDSLベースのフィーチャーストアはTectonです。
In the rest of this chapter, we describe the common functionality offered by both API-based and DSL-based feature stores, while in the next chapter, we will look at the Hopsworks feature store, which is representative of API-based feature stores. 
この章の残りの部分では、APIベースとDSLベースのフィーチャーストアの両方が提供する共通機能について説明しますが、次の章ではAPIベースのフィーチャーストアの代表例であるHopsworksフィーチャーストアを見ていきます。

---
(コラム)
The term feature platform has been used to describe feature stores that support managed feature pipelines. 
フィーチャープラットフォームという用語は、管理されたフィーチャーパイプラインをサポートするフィーチャーストアを説明するために使用されています。
Most feature stores, including Hopsworks, are also feature platforms based on this definition. 
Hopsworksを含むほとんどのフィーチャーストアは、この定義に基づくフィーチャープラットフォームでもあります。
Finally, an AI lakehouse is a feature store that uses lakehouse tables as its offline store and has an integrated online store for building real-time ML systems. 
最後に、AIレイクハウスは、レイクハウステーブルをオフラインストアとして使用し、リアルタイムMLシステムを構築するための統合オンラインストアを持つフィーチャーストアです。

-----

<!-- ここまで読んだ! -->

### 1.3. The Anatomy of a Feature Store フィーチャーストアの解剖学

A feature store is a factory that produces and stores feature data. 
フィーチャーストアはフィーチャーデータを生成し保存する工場です。
It enables the faster production of higher-quality features by managing the storage and transformation of data for training and inference, and it allows you to reuse features in any model. 
トレーニングと推論のためのデータの保存と変換を管理することで、**高品質のフィーチャーをより迅速に生産でき、任意のモデルでフィーチャーを再利用できるように**します。
In Figure 4-2, we can see the main inputs and outputs and the data transformations managed by a feature store. 
図4-2では、フィーチャーストアが管理する主な入力と出力、およびデータ変換を見ることができます。

![]()
_Figure 4-2. Feature stores help transform and store feature data. A feature store organizes the data transformations to create consistent snapshots of training data for models, as well as the batches of inference data for batch ML systems and the online inference data for real-time ML systems._  
図4-2. フィーチャーストアはフィーチャーデータの変換と保存を助けます。フィーチャーストアは、モデルのためのトレーニングデータの一貫したスナップショットを作成するためのデータ変換を整理し、バッチMLシステムのための推論データのバッチとリアルタイムMLシステムのためのオンライン推論データを作成します。

<!-- ここまで読んだ! -->

_Feature pipelines are programs that feed a feature store with feature data. 
フィーチャーパイプラインは、フィーチャーストアにフィーチャーデータを供給するプログラムです。
They take new data or historical data as input and transform it into reusable feature data, using model-independent transformations (MITs). 
**新しいデータまたは履歴データを入力として受け取り、モデルに依存しない変換（MIT）を使用して再利用可能なフィーチャーデータに変換**します。
On-demand transformations (ODTs) can also be applied to historical data in feature pipelines. 
オンデマンド変換（ODT）もフィーチャーパイプラインの履歴データに適用できます。
Feature pipelines can be batch or streaming programs, and they update feature data over time. 
フィーチャーパイプラインはバッチまたはストリーミングプログラムであり、時間の経過とともにフィーチャーデータを更新します。
That is, the feature store stores mutable feature data. 
つまり、**フィーチャーストアはmutableなフィーチャーデータを保存**します。
For supervised ML, labels can also be stored in a feature store and are treated as feature data until they are used to create training or inference data, in which case, the feature store is aware of which columns are features and which columns are labels. 
**教師ありMLの場合、ラベルもフィーチャーストアに保存でき、トレーニングまたは推論データを作成するまでフィーチャーデータとして扱われます**。この場合、フィーチャーストアはどの列がフィーチャーでどの列がラベルであるかを認識しています。
(まあラベルは基本的にはオフラインストアだけで十分だよね。それだったらコストも安いしいいかも:thinking: event_timeでpartitioningとかしておけば、必要な期間のラベルだけ効率的に読み出せるし...!)

<!-- ここまで読んだ! -->

Feature stores enable the creation of versioned training datasets by taking a point-in-time consistent snapshot of feature data (see “For Time-Series Data” on page 80) and then applying model-dependent transformations (MDTs) to the features (and labels). 
フィーチャーストアは、**フィーチャーデータの時点で一貫したスナップショットを取得することによってバージョン管理されたトレーニングデータセットの作成を可能**にし（「時系列データについて」80ページ参照）、その後、フィーチャー（およびラベル）にモデル依存の変換（MDT）を適用します。
Training datasets are used to train models, and the feature store should store the lineage of the training dataset for models.
トレーニングデータセットはモデルのトレーニングに使用され、フィーチャーストアはモデルのトレーニングデータセットの系譜を保存する必要があります。

<!-- ここまで読んだ! -->

A feature store also creates point-in-time consistent snapshots of feature data for batch inference, which should have the same MDTs applied to them as were applied when creating the training data for the model used in batch inference. 
フィーチャーストアはまた、バッチ推論のためのフィーチャーデータの時点で一貫したスナップショットを作成します。これには、バッチ推論に使用されるモデルのトレーニングデータを作成する際に適用されたのと同じMDTが適用されるべきです。
A feature store also provides low-latency feature data to online applications or services. 
フィーチャーストアは、オンラインアプリケーションやサービスに低遅延のフィーチャーデータも提供します。
Model deployments receive prediction requests, and parameters from the prediction request can be used to compute on-demand features and retrieve precomputed rows of feature data from the feature store. 
モデルのデプロイメントは予測リクエストを受け取り、予測リクエストからのパラメータを使用してオンデマンドフィーチャーを計算し、フィーチャーストアから事前計算されたフィーチャーデータの行を取得できます。
Any on-demand and precomputed features are merged into a feature vector that can have further MDTs applied to it (the same as those applied in training) before the model makes a prediction with the transformed feature vector. 
**すべてのオンデマンドおよび事前計算されたフィーチャーは、フィーチャーベクトルに統合され、モデルが変換されたフィーチャーベクトルで予測を行う前に、さらにMDTを適用できます**（トレーニングで適用されたものと同じ）。

<!-- ここまで読んだ! -->

Feature stores support and organize the data transformations in the taxonomy from Chapter 2. 
フィーチャーストアは、章2の分類法におけるデータ変換をサポートし、整理します。
MITs are applied only in feature pipelines on new or historical data to produce reusable feature data. 
MITは、新しいデータまたは履歴データのフィーチャーパイプラインでのみ適用され、再利用可能なフィーチャーデータを生成します。
ODTs are a special class of MIT that is applied in both feature pipelines and online inference pipelines—feature stores should guarantee that exactly the same transformation is executed in the feature and online inference pipelines; otherwise, there is a risk of skew. 
ODTは、フィーチャーパイプラインとオンライン推論パイプラインの両方に適用されるMITの特別なクラスです。フィーチャーストアは、フィーチャーとオンライン推論パイプラインでまったく同じ変換が実行されることを保証する必要があります。そうでなければ、偏りのリスクがあります。
MDTs are applied in training pipelines, batch inference pipelines, and online inference pipelines. 
MDTは、トレーニングパイプライン、バッチ推論パイプライン、およびオンライン推論パイプラインに適用されます。

Again, the feature store should ensure that the same transformation is executed in the training and inference pipelines, preventing skew. 
再度、フィーチャーストアは、トレーニングと推論パイプラインで同じ変換が実行されることを保証し、偏りを防ぐ必要があります。

<!-- ここまで読んだ! -->

Feature stores support the composition of MITs, MDTs, and ODTs in pipelines by enforcing the constraint that MDTs always come after model-independent (and on-demand) transformations. 
フィーチャーストアは、**MDTが常にモデルに依存しない（およびオンデマンド）変換の後に来るという制約を強制する**ことによって、パイプライン内でのMIT、MDT、およびODTの構成をサポートします。
That is, MDTs are always the last transformations in a directed acyclic graph (DAG), just before the model is called. 
つまり、**MDTは常に有向非巡回グラフ（DAG）内の最後の変換であり、モデルが呼び出される直前**です。
Also, ODTs typically come after MITs in a DAG, as MITs are precomputed features and ODTs can only be computed at request time (and can take precomputed features as parameters). 
また、**ODTは通常DAG内のMITの後に来ます**。MITは事前計算されたフィーチャーであり、ODTはリクエスト時にのみ計算でき（事前計算されたフィーチャーをパラメータとして受け取ることができます）、この章は主にフィーチャーデータの保存、モデリング、およびクエリに関するものです。
Chapters 6 and 7 will address the MITs, MDTs, and ODTs. 
第6章と第7章では、MIT、MDT、およびODTについて扱います。

<!-- ここまで読んだ! -->

### 1.4. When Do You Need a Feature Store? フィーチャーストアはいつ必要ですか？

When is it appropriate for you to use a feature store? 
フィーチャーストアを使用するのに適切なタイミングはいつですか？
Many organizations already have operational databases, an object store, and a data warehouse or lakehouse. 
多くの組織はすでに運用データベース、オブジェクトストア、およびデータウェアハウスまたはレイクハウスを持っています。
Why would they need a new data platform? 
なぜ新しいデータプラットフォームが必要なのでしょうか？
The following are scenarios where a feature store can help. 
以下は、フィーチャーストアが役立つシナリオです。

<!-- ここまで読んだ! -->

#### 1.4.1. For Context and History in Real-Time ML Systems リアルタイムMLシステムにおけるコンテキストと履歴のために

We saw in Chapter 1 how real-time ML systems need history and context to make personalized predictions 
第1章で、リアルタイムMLシステムがパーソナライズされた予測を行うために履歴とコンテキストが必要であることを見ました。
In general, when you have a real-time prediction problem but the prediction request has low information content, you can benefit from a feature store to provide context and history to enrich the prediction request. 
一般的に、リアルタイム予測問題があり、予測リクエストの情報量が少ない場合、フィーチャーストアを利用して文脈や履歴を提供し、予測リクエストを豊かにすることができます。
For example, a credit card transaction has limited information in the prediction request—only the credit card number, the merchant ID (unique identifier), the timestamp, the IP address for the transaction location, data on whether the credit card purchase was at a terminal or online (meaning whether the card was present or not), and the amount of money spent. 
例えば、クレジットカード取引は予測リクエストにおいて限られた情報しか持っていません—クレジットカード番号、マーチャントID（ユニーク識別子）、タイムスタンプ、取引場所のIPアドレス、クレジットカード購入が端末で行われたかオンラインで行われたか（カードが存在したかどうかを意味します）、および支出金額のみです。
Building an accurate credit card fraud prediction service with AI by using only that input data is almost impossible, as you would be missing historical information about credit card transactions. 
**その入力データのみを使用して正確なクレジットカード詐欺予測サービスをAIで構築することはほぼ不可能です。なぜなら、クレジットカード取引に関する履歴情報が欠けているから**です。
But with a feature store, you can enrich the prediction request at runtime with history and context information about the credit card’s recent usage, the customer details, the issuing bank’s details, and the merchant’s details, thus enabling a powerful model for predicting fraud. 
しかし、**フィーチャーストアを使用することで、クレジットカードの最近の使用状況、顧客の詳細、発行銀行の詳細、マーチャントの詳細に関する履歴と文脈情報で予測リクエストを実行時に豊かにすることができ、詐欺を予測するための強力なモデルを実現**できます。

<!-- ここまで読んだ! -->

#### 1.4.2. For Time-Series Data 時系列データのために

Many retail, telecommunications, and financial ML systems are built on time-series data. 
**多くの小売、通信、金融の機械学習システムは時系列データに基づいて構築**されています。
The air quality and weather data from Chapter 3 is time-series data that we update once per day and store in feature groups along with the timestamps for each observation or forecast. 
第3章の空気質と気象データは時系列データであり、私たちはこれを1日1回更新し、各観測または予測のタイムスタンプとともにフィーチャーグループに保存します。
Time-series data is a sequence of data points for successive points in time. 
時系列データは、連続する時間のデータポイントのシーケンスです。
A major challenge in using time-series data for ML is how to read (query) feature data that is spread over many tables—you want to read point-in-time correct training data from the different tables without introducing future data leakage or including any stale feature values (see Figure 4-3).  
機械学習における時系列データの使用における主要な課題は、**多くのテーブルに分散しているフィーチャーデータをどのように読み取る（クエリする）か**です—異なるテーブルから未来のデータリークを引き起こしたり、古いフィーチャー値を含めたりすることなく、時点に正しいトレーニングデータを読み取る必要があります（図4-3を参照）。

![]()
_Figure 4-3. Creating point-in-time correct training data from time-series data that’s spread over different relational tables is hard. The solution starts from the table containing the labels/targets (Fraud Label), pulling in columns (features) from the tables containing the features (Transactions and Bank). If you include feature values from the future, you have future data leakage. If you include a feature value that is stale, you also have data leakage._  
_図4-3. **異なるリレーショナルテーブルに分散している時系列データから時点に正しいトレーニングデータを作成するのは難しい**です。解決策は、ラベル/ターゲット（Fraud Label）を含むテーブルから始まり、フィーチャーを含むテーブル（TransactionsとBank）から列（フィーチャー）を引き込むことです。未来のフィーチャー値を含めると、未来のデータリークが発生します。古いフィーチャー値を含めると、データリークが発生します。_

Feature stores provide support for reading point-in-time correct training data from different tables containing time-series feature data. 
フィーチャーストアは、時系列フィーチャーデータを含む異なるテーブルから時点に正しいトレーニングデータを読み取るためのサポートを提供します。
The solution, described later in this chapter, is to query data with temporal joins. 
この章の後半で説明する解決策は、**時間的結合(temporal joins)**を使用してデータをクエリすることです。
Writing correct temporal joins is hard, but feature stores make it easier by providing APIs for reading consistent snapshots of feature data using temporal joins. 
正しい時間的結合を書くのは難しいですが、フィーチャーストアは時間的結合を使用してフィーチャーデータの一貫したスナップショットを読み取るためのAPIを提供することで、これを容易にします。

<!-- ここまで読んだ! -->

---
(コラム)
You may have previously encountered data leakage in the context of training models. 
以前にモデルのトレーニングの文脈でデータリークに遭遇したことがあるかもしれません。
For example, if you leak data from your test set or any external dataset into your training dataset, your model may perform better during testing than when it is used in production on unseen data. 
**例えば、テストセットや外部データセットからトレーニングデータセットにデータが漏れた場合、モデルはテスト中により良いパフォーマンスを発揮するかもしれませんが、未見のデータで本番環境で使用されるときにはそうではありません。**
Future data leakage occurs when you build training datasets from time-series data and incorrectly introduce one or more feature data points from the future. 
未来のデータリークは、時系列データからトレーニングデータセットを構築し、未来の1つまたは複数のフィーチャーデータポイントを誤って導入する場合に発生します。
_Stale features include a feature value that is older than the actual feature value at the time of an observation._ 
_古いフィーチャーには、観測時の実際のフィーチャー値よりも古いフィーチャー値が含まれます。_

---

#### 1.4.3. For Improved Collaboration with the FTI Pipeline Architecture FTIパイプラインアーキテクチャによるコラボレーションの改善のために

An important reason many models do not reach production is that organizations have silos around the teams that collaborate to develop and operate AI systems. 
**多くのモデルが本番環境に到達しない重要な理由は、組織内にAIシステムを開発・運用するために協力するチームの周りにサイロが存在すること**です。
In Figure 4-4, you can see a siloed organization where the data engineering team has a metaphorical wall between it and the data science team and there is a similar wall between the data science team and the ML engineering team. 
図4-4では、データエンジニアリングチームとデータサイエンスチームの間に比喩的な壁があり、データサイエンスチームとMLエンジニアリングチームの間にも同様の壁があるサイロ型の組織を見ることができます。
In this siloed organization, collaboration involves data and models being thrown over the wall from one team to another. 
このサイロ型の組織では、コラボレーションはデータとモデルが一つのチームから別のチームに投げ渡されることを含みます。

![]()
_Figure 4-4. If you are a data scientist in an organization with this method of collaboration (where you receive dumps of data and you throw models over the wall to production), Conway’s Law implies you will only ever train models and not contribute to production systems._  
_図4-4. このようなコラボレーション方法の組織にいるデータサイエンティストであれば（データのダンプを受け取り、モデルを本番環境に投げ渡す場合）、コンウェイの法則は、あなたがモデルをトレーニングするだけで、本番システムに貢献しないことを示唆しています。_

The system for collaboration at this organization is an example of _Conway’s Law,_ according to which the process of collaboration (throwing assets over walls) mirrors the siloed communication structure among teams. 
**この組織におけるコラボレーションのシステムは、_コンウェイの法則_の例であり、コラボレーションのプロセス（資産を壁越しに投げること）がチーム間のサイロ型コミュニケーション構造を反映**しています。
The feature store solves the organizational challenges of collaboration among teams by providing a shared platform for collaboration when building and operating AI systems. 
フィーチャーストアは、**AIシステムを構築・運用する際にチーム間のコラボレーションのための共有プラットフォームを提供することで、組織のコラボレーションに関する課題を解決**します。
The FTI pipelines from Chapter 2 also help with collaboration. 
第2章のFTIパイプラインもコラボレーションに役立ちます。
They decompose an AI system into modular pipelines that use the feature store, acting as the shared data layer connecting the pipelines. 
これらは、フィーチャーストアを使用するモジュール式パイプラインにAIシステムを分解し、**パイプラインを接続する共有データ層**として機能します。
The responsibilities for the FTI pipelines map cleanly onto the teams that develop and operate production AI systems: 
FTIパイプラインの責任は、本番AIシステムを開発・運用するチームに明確にマッピングされます：

- Data scientists and data engineers collaborate to build and operate feature pipelines. 
  - データサイエンティストとデータエンジニアは、フィーチャーパイプラインを構築・運用するために協力します。
- Data scientists train and evaluate the models. 
  - データサイエンティストはモデルをトレーニングし、評価します。
- Data scientists and operations engineers write inference pipelines and integrate models with external systems.  
  - データサイエンティストとオペレーションエンジニアは推論パイプラインを作成し、モデルを外部システムと統合します。

But if a data scientist helps build operational pipelines and deploy models to production, they are no longer a data scientist, they are an ML engineer. 
しかし、データサイエンティストが運用パイプラインの構築を手伝い、モデルを本番環境にデプロイする場合、彼らはもはやデータサイエンティストではなく、MLエンジニアです。
This is, I believe, the future for most data scientists working today. 
これは、私が考えるに、今日働いているほとんどのデータサイエンティストの未来です。
You have to be able to build and operate AI systems or your employer will find an ML engineer who will do it for you. 
**AIシステムを構築・運用できる必要があります。さもなければ、雇用主はあなたのためにそれを行うMLエンジニアを見つけるでしょう。**

<!-- ここまで読んだ! -->

#### 1.4.4. For Governance of ML Systems MLシステムのガバナンスのため

Feature stores help ensure that an organization’s governance processes keep feature data secure and accountable throughout its lifecycle. 
フィーチャーストアは、組織のガバナンスプロセスがフィーチャーデータをそのライフサイクル全体で安全かつ説明責任を持って保持することを確保するのに役立ちます。
That means auditing actions taken in your feature store for accountability and tracking lineage from source data to features to models. 
つまり、フィーチャーストアで行われたアクションを監査して説明責任を果たし、ソースデータからフィーチャー、モデルへの系譜を追跡することを意味します。
Feature stores manage mutable data that needs to comply with regulatory requirements, such as the European Union’s AI Act that categorizes AI systems into four different risk levels: unacceptable, high, limited, and minimal. 
フィーチャーストアは、AIシステムを受け入れられない、高リスク、制限付き、最小限の4つの異なるリスクレベルに分類する欧州連合のAI法など、規制要件に準拠する必要がある可変データを管理します。

Beyond data storage, a feature store also needs support for _lineage for compliance_ with other legal and regulatory requirements involving tracking the origin, history, and use of data sources, features, training data, and models in AI systems. 
データストレージを超えて、フィーチャーストアは、AIシステムにおけるデータソース、フィーチャー、トレーニングデータ、モデルの起源、履歴、使用を追跡する他の法的および規制要件に準拠するための lineage for compliance_ のサポートも必要です。(lineage for compliance = 簡単にいうと...コンプライアンスを守るための系譜管理？:thinking:)
Lineage also enables the reproducibility of features, training data, and models; improved debugging through quicker root cause analysis; and usage analysis for features. 
系譜は、フィーチャー、トレーニングデータ、モデルの再現性を可能にし、迅速な根本原因分析を通じてデバッグを改善し、フィーチャーの使用分析を可能にします。
Lineage tells you where AI assets are used, but it does not tell you whether a particular feature is allowed to be used in a particular model—for example, a high-risk AI system. 
**系譜はAI資産がどこで使用されているかを教えてくれますが**、特定のフィーチャーが特定のモデル（例えば、高リスクのAIシステム）で使用することが許可されているかどうかは教えてくれません。
Access control, while necessary, does not help here either, as it only informs you whether you have the right to read/write the data, not whether your model will be compliant if you use a certain feature. 
アクセス制御は必要ですが、ここでは役に立ちません。なぜなら、それはデータを読み書きする権利があるかどうかを知らせるだけであり、特定のフィーチャーを使用した場合にモデルが準拠するかどうかは知らせないからです。
For compliance, feature stores support custom metadata to describe the scope and context under which a feature can be used. 
**コンプライアンスのために、フィーチャーストアはフィーチャーが使用できる範囲と文脈を説明するカスタムメタデータをサポートします。**
For example, you might tag features that have personally identifiable information (PII). 
**例えば、個人を特定できる情報（PII）を含むフィーチャーにタグを付ける**ことができます。(自前でこれをやるのは結構大変かも。テーブル粒度ならまだしも、フィーチャー粒度でやるのは...:thinking:)
With lineage (from data sources, to features, to training data, to models) and PII metadata tags for features, you can easily identify which models use features containing PII data. 
系譜（データソースからフィーチャー、トレーニングデータ、モデルまで）とフィーチャーのPIIメタデータタグを使用することで、どのモデルがPIIデータを含むフィーチャーを使用しているかを簡単に特定できます。

<!-- ここまで読んだ! -->

#### 1.4.5. For Discovery and Reuse of AI Assets AI資産の発見と再利用のために

_[Feature reuse is a much advertised benefit of feature stores. Meta reported that “most](https://oreil.ly/tIf4d)_ features are used by many models” in their feature store, and the most popular one hundred features are reused in over a hundred different models each. 
[**フィーチャーの再利用はフィーチャーストアの大きな利点として宣伝されています。Metaは「ほとんどのフィーチャーが多くのモデルで使用されている」と報告しており、最も人気のある100のフィーチャーはそれぞれ100以上の異なるモデルで再利用されています。**
The benefits of feature reuse include improvements in the quality of features through increased usage and scrutiny, reduced storage cost, and reduced feature development and operational costs, as models that reuse features do not need new feature pipelines. 
**フィーチャーの再利用の利点には、使用と精査の増加を通じたフィーチャーの質の向上、ストレージコストの削減、フィーチャー開発および運用コストの削減が含まれます**。フィーチャーを再利用するモデルは新しいフィーチャーパイプラインを必要としません。
Computed features are stored in the feature store and published to a feature registry, enabling users to easily discover and understand features. 
計算されたフィーチャーはフィーチャーストアに保存され、フィーチャーレジストリに公開され、**ユーザーがフィーチャーを簡単に発見し理解できるように**します。
The feature registry is a component in a feature store that has an API and UI to browse and search for available features, feature definitions, statistics on feature data, and metadata describing features.  
**フィーチャーレジストリは、利用可能なフィーチャー、フィーチャー定義、フィーチャーデータの統計、およびフィーチャーを説明するメタデータをブラウズおよび検索するためのAPIとUIを持つフィーチャーストアのコンポーネント**です。(これも自前で作るのは一定工数必要だから、まあSnowsightで代用して問題があれば別途考える、みたいな感じかな〜:thinking:)


#### 1.4.6. For Elimination of Offline-Online Feature Skew　オフライン-オンラインフィーチャースキューの排除のために

_Feature skew occurs when significant differences exist between the data transformation code in either an ODT or an MDT in an offline pipeline (a feature pipeline or a training pipeline, respectively) and the data transformation code for the ODT or MDT in the corresponding inference pipeline. 
**feature skewは、オフラインパイプライン（フィーチャーパイプラインまたはトレーニングパイプライン）内のODTまたはMDTのデータ変換コードと、対応する推論パイプライン内のODTまたはMDTのデータ変換コードの間に重要な違いが存在する場合に発生**します。
Feature skew can result in silently degraded model performance that is difficult to discover. 
**フィーチャースキューは、発見が難しい静かなモデルパフォーマンスの低下**をもたらす可能性があります。
It may show up as the model not generalizing well to the new data during inference due to the discrepancies in the data transformations. 
データ変換の不一致により、推論中にモデルが新しいデータにうまく一般化しないことが示される場合があります。
Without a feature store, it is easy to write different implementations for an ODT or MDT—one implementation for the feature or training pipeline and a different one for the inference pipeline. 
**フィーチャーストアがないと、ODTまたはMDTの異なる実装を書くのは簡単**です—フィーチャーまたはトレーニングパイプライン用の1つの実装と、推論パイプライン用の異なる実装です。
In software engineering, we say that such data transformation code is not DRY. 
ソフトウェアエンジニアリングでは、**そのようなデータ変換コードはDRYではない**と言います。
Feature stores support the definition and management of ODTs and MDTs, and they ensure that the same function is applied in the offline and inference pipelines. 
フィーチャーストアはODTとMDTの定義と管理をサポートし、オフラインパイプラインと推論パイプラインで同じ機能が適用されることを保証します。

<!-- ここまで読んだ! -->

#### 1.4.7. For Centralizing Your Data for AI in a Single Platform　AIのためのデータを単一プラットフォームに集中化するために

Feature stores aspire to be a central platform that manages all data needed to train and operate AI systems. 
**フィーチャーストアは、AIシステムをトレーニングおよび運用するために必要なすべてのデータを管理する中央プラットフォームを目指しています。** (必要な全てのデータってことはラベルもか...!:thinking:)
Existing feature stores have a hybrid architecture, including an offline store and an online store with a vector index to store vector embeddings and support similarity search. 
既存のフィーチャーストアは、オフラインストアと、ベクトルインデックスを備えたオンラインストアを含むハイブリッドアーキテクチャを持っています。ベクトルインデックスは、ベクトル埋め込みを保存し、類似性検索をサポートします。

An online store is used by online applications to retrieve feature vectors for entities. 
オンラインストアは、オンラインアプリケーションによってエンティティのフィーチャーベクトルを取得するために使用されます。
It is a row-oriented data store, where data is stored in relational tables or in a NoSQL data structure (like key-value pairs or JSON objects). 
これは行指向のデータストアであり、データはリレーショナルテーブルまたはNoSQLデータ構造（キー-バリューのペアやJSONオブジェクトなど）に保存されます。
The key properties of row-oriented data stores are:
**行指向データストアの主な特性**は次のとおりです。

- Low-latency and high-throughput CRUD (create, read, update, delete) operations using either SQL or NoSQL
  - SQLまたはNoSQLを使用した低遅延で高スループットのCRUD（作成、読み取り、更新、削除）操作
- Support for primary keys to retrieve features for specific entities
  - 特定のエンティティの特徴を取得するための主キーのサポート
- Support for time to live (TTL) for tables and/or rows to expire stale feature data
  - **古い特徴データを期限切れにするためのテーブルおよび/または行の生存時間（TTL）のサポート**
- High availability through replication and data integrity through ACID (atomicity, consistency, isolation, durability) transactions
  - レプリケーションによる高可用性とACID（原子性、一貫性、隔離性、耐久性）トランザクションによるデータ整合性の確保
- Support for secondary indexes to support more complex queries (such as online aggregations)
  - より複雑なクエリ（オンライン集計など）をサポートするためのセカンダリインデックスのサポート

<!-- ここまで読んだ! -->

An offline store is a columnar store. 
一方で、**オフラインストアは列指向ストア**です。
Column-oriented data stores:
列指向データストアは次のようになります。

- Are central data platforms that store historical data for analytics
  - 分析のための**履歴データ**を保存する中央データプラットフォームです。
- Provide low-cost storage for large volumes of data (including columnar compression of data) at the cost of high latency for row-based retrieval of data
  - **行ベースのデータ取得に高遅延を伴う代わりに、大量のデータ（データの列指向圧縮を含む）に対して低コストのストレージを提供**します。
- Enable faster complex queries than do row-oriented stores through more efficient data pruning and data movement, aided by data models designed to support complex queries
  - 複雑なクエリをサポートするように設計されたデータモデルによって支援され、より効率的なデータプルーニングとデータ移動を通じて、**行指向ストアよりも高速な複雑なクエリを可能に**します。

The offline stores for existing feature stores are lakehouses. 
**既存のフィーチャーストアのオフラインストアはレイクハウス**です。
A lakehouse is a combination of a data lake for storage and a data warehouse for querying the data. 
**レイクハウスは、データの保存のためのデータレイクとデータのクエリのためのデータウェアハウスの組み合わせ**です。
In contrast to a data warehouse, a lakehouse is an open platform that separates the storage of columnar data from the query engines that use it. 
データウェアハウスとは対照的に、**レイクハウスは列指向データのストレージをそれを使用するクエリエンジンから分離するオープンプラットフォーム**です。(なるほど、じゃあS3 TablesにIcebergテーブルを作って、Athenaやsnowflake等でクエリする設計は、レイクハウスの一例と言えるのか...!:thinking:)
Lakehouse tables can be queried by many different query engines. 
**レイクハウスのテーブルは、多くの異なるクエリエンジンによってクエリされることができます。*
(=これが「レイクハウス」か否かの本質か...!! オフラインストアはレイクハウスであるべき:thinking:)
The main open source standards for a lakehouse are the open table formats (OTFs) for data storage (Apache Iceberg, Delta Lake, Apache Hudi). 
レイクハウスの主なオープンソース標準は、データストレージのための**オープンテーブルフォーマット（OTF）**（**Apache Iceberg**、Delta Lake、Apache Hudi）です。
An OTF consists of data files (Parquet files) and metadata that enables ACID updates to the Parquet files—a commit for every batch append/update/delete operation. 
OTFは、データファイル（Parquetファイル）と、ParquetファイルへのACID更新を可能にするメタデータで構成されており、バッチの追加/更新/削除操作ごとにコミットが行われます。
The commit history is stored as metadata and enables time-travel support for lakehouse tables, where you can query historical versions of tables (using a commit ID or timestamp). 
コミット履歴はメタデータとして保存され、レイクハウスのテーブルに対するタイムトラベルサポートを可能にし、テーブルの履歴バージョンをクエリすることができます（コミットIDまたはタイムスタンプを使用）。
Lakehouse tables also support schema evolution (you can add columns to your table without breaking clients), as well as partitioning, indexing, and data skipping for faster queries. 
レイクハウスのテーブルは、スキーマの進化（クライアントを壊すことなくテーブルに列を追加できる）や、パーティショニング、インデクシング、データスキッピングによる高速クエリもサポートしています。

<!-- ここまで読んだ! -->

An offline and/or online store may also support storing vector embeddings in a vector index that supports approximate nearest neighbor (ANN) search for feature data. 
**オフラインおよび/またはオンラインストアは、特徴データのための近似最近傍（ANN）検索をサポートするベクトルインデックスにベクトル埋め込みを保存することもサポートする場合**があります。
Feature stores include either a separate standalone vector database (such as Weaviate or Pinecone) or an existing row-oriented database that supports a vector index and ANN search (such as Postgres PGVector, OpenSearch, or MongoDB). 
フィーチャーストアには、独立したスタンドアロンのベクトルデータベース（WeaviateやPineconeなど）またはベクトルインデックスとANN検索をサポートする既存の行指向データベース（**Postgres PGVector**、OpenSearch、MongoDBなど）が含まれます。
Now that we have covered why and when you may need a feature store, we will look into storing data in feature stores in feature groups. 
フィーチャーストアが必要な理由とタイミングを説明したので、フィーチャーストアにおけるデータの保存方法をフィーチャーグループで見ていきます。

<!-- ここまで読んだ! -->


### 1.5. Feature Groups フィーチャーグループ

Feature stores use feature groups to hide the complexity of writing and reading data to/from the different offline and online data stores. 
フィーチャーストアは、異なるオフラインおよびオンラインデータストアへのデータの書き込みと読み取りの複雑さを隠すためにフィーチャーグループを使用します。
We encountered feature groups in Chapters 2 and 3, but we haven’t formally defined them. 
私たちは第2章と第3章でフィーチャーグループに出会いましたが、正式に定義していませんでした。
Feature groups are tables in which the features are columns and the feature data is stored in offline and online stores. 
フィーチャーグループは、特徴が列であり、フィーチャーデータがオフラインおよびオンラインストアに保存されるテーブルです。
Not all feature stores use the term feature groups—some vendors call them feature sets or feature tables, but they refer to the same concept. 
**すべてのフィーチャーストアがフィーチャーグループという用語を使用するわけではありません。一部のベンダーはそれらをフィーチャーセットまたはフィーチャーテーブルと呼びますが、同じ概念を指しています。**
We prefer the term feature group, as the data is potentially stored in a group of tables, in more than one store. 
私たちは**フィーチャーグループという用語を好みます。なぜなら、データは複数のストアにわたるテーブルのグループに保存される可能性があるから**です。
(なるほどね、もし「feature table」だと、オフラインストア用のテーブルと、オンラインストア用のテーブルが両方あるから、混乱を招くもんなぁ...!:thinking:)
We will cover the most salient and fundamental properties of feature groups, but note that your feature store might have some differences, so consult its documentation before building your feature pipelines. 
**フィーチャーグループの最も重要で基本的な特性**をカバーしますが、あなたのフィーチャーストアにはいくつかの違いがあるかもしれないので、フィーチャーパイプラインを構築する前にそのドキュメントを参照してください。
Caveat emptor.
購入者注意。

<!-- ここまで読んだ! -->

A feature group consists of a schema, metadata, a table in an offline store, an optional table in an online store, and an optional vector index. 
**フィーチャーグループは、スキーマ、メタデータ、オフラインストアのテーブル、オンラインストアのオプションのテーブル、およびオプションのベクトルインデックスで構成**されます。
The metadata typically contains the feature group’s:
メタデータには通常、フィーチャーグループの次の情報が含まれます。

- name
  - 名前
- version (a number)
  - バージョン（数値）
- entity_id (a primary key, defined over one or more columns)
  - entity_id（主キー、1つ以上の列に対して定義される）
- online_enabled—whether the feature group’s online table is used or not
  - online_enabled—フィーチャーグループのオンラインテーブルが使用されているかどうか
- event_time column (optional)
  - event_time列（オプション）
- Tags to help with discovery and governance
  - 発見とガバナンスを助けるためのタグ

The entity_id is needed to retrieve rows of online feature data and prevent duplicate data, while the version number enables support for A/B tests of features by different models and enables schema-breaking changes to feature groups. 
**entity_idはオンラインフィーチャーデータの行を取得し、重複データを防ぐために必要**であり、**バージョン番号は異なるモデルによるフィーチャーのA/Bテストをサポート**(なるほど...まあ新しいカラムを追加するでもいいのかな...?:thinking:)し、フィーチャーグループに対するスキーマを破る変更を可能にします。
The event_time column is used by the feature store to create point-in-time consistent training data from time-series feature data. 
**event_time列は、フィーチャーストアが時系列フィーチャーデータから時点で一貫したトレーニングデータを作成するために使用**されます。
Depending on your feature store, a feature group may support some or all of the following:
フィーチャーストアによっては、フィーチャーグループが以下のいずれかまたはすべてをサポートする場合があります。
(へぇ〜 foreign keyも...!:thinking:)

- foreign_key columns (references to a primary key in another feature group)
  - foreign_key列（別のフィーチャーグループの主キーへの参照）
- A partition_key column (used for faster queries through partition pruning)
  - partition_key列（パーティショニングプルーニングを通じて高速クエリに使用される）
- vector embedding features that are indexed for similarity search
  - 類似検索のためにインデックスされたベクトル埋め込みフィーチャー
- feature definitions that define the data transformations used to create the features stored in the feature group
  - フィーチャーグループに保存されるフィーチャーを作成するために使用されるデータ変換を定義するフィーチャー定義

In Figure 4-5, we can see a feature group containing different columns related to credit card transactions. 
図4-5では、クレジットカード取引に関連する異なる列を含むフィーチャーグループを見ることができます。
You will notice that most columns are not feature columns.
**ほとんどの列がフィーチャー列ではないこと**に気付くでしょう。

![]()
_Figure 4-5. Rows are uniquely identified with a combination of the entity ID and the_ ``` event_time. 
_図4-5. 行は、entity IDと``` event_timeの組み合わせで一意に識別されます。
You can have a foreign key that points to a row in a different feature group and a partition key that is used for push-down filters for faster queries. 
別のフィーチャーグループの行を指す外部キーと、高速クエリのためのプッシュダウンフィルターに使用されるパーティションキーを持つことができます。
The index columns are not features. 
インデックス列はフィーチャーではありません。
Any feature could be used as a label when creating training data from the feature group.
フィーチャーグループからトレーニングデータを作成する際に、任意のフィーチャーをラベルとして使用することができます。

<!-- ここまで読んだ! -->

The first four columns are collectively known as _index columns—the_ `cc_num is the` entity ID, ts is the timestamp for the transaction (its event time), the account_id is a foreign key to `account_fg` (not shown), and day is a partition key column enabling` queries that filter by `day to be faster by only reading the needed data (for example,` reading yesterday’s feature data will not read all rows, only the rows where the `day` value is yesterday).
**最初の4つの列は、総称して index columns** として知られています。`cc_num` はエンティティIDであり、`ts` は取引のタイムスタンプ（そのイベント時間）であり、`account_id` は `account_fg` への外部キーです（表示されていません）。`day` はパーティションキー列であり、`day` でフィルタリングするクエリを可能にし、必要なデータのみを読み取ることで高速化します（例えば、昨日のフィーチャーデータを読む場合、すべての行を読むのではなく、`day` 値が昨日の行のみを読み取ります）。
The next three columns (amount, category, and embedding_col) are features—the embedding_col is a vector embedding that is indexed for similarity search in the vector index.
次の3つの列（`amount`、`category`、および `embedding_col`）は特徴です。`embedding_col` はベクトル埋め込みであり、ベクトルインデックスでの類似性検索のためにインデックスされています。
Finally, the is_fraud column is also a feature column but is identified as a label in the figure.
最後に、`is_fraud` 列も特徴列ですが、図ではラベルとして識別されています。
That is because features can also be labels—the `is_fraud` column could be a label in one model but a feature in another model.
**これは、特徴がラベルにもなり得るためです。`is_fraud` 列は、あるモデルではラベルであり、別のモデルでは特徴である可能性があります。**(なるほど...! semantic modelの出力とかは、ラベルであり特徴量でもある、みたいな感じかな...!:thinking:)
For this reason, labels are not defined in feature groups but are only defined when you select the features and labels for your model.
このため、ラベルは特徴グループでは定義されず、モデルの特徴とラベルを選択する際にのみ定義されます。

<!-- ここまで読んだ! -->

You can perform inserts, updates, and deletes on feature groups, either via a batch (DataFrame) API or a streaming API (for real-time ML systems).
特徴グループに対しては、バッチ（DataFrame）APIまたはストリーミングAPI（リアルタイムMLシステム用）を介して挿入、更新、削除を行うことができます。
As a feature group has a schema, your feature store defines the set of supported data types for features—strings, integers, arrays, and so on.
特徴グループにはスキーマがあるため、特徴ストアは特徴のためのサポートされるデータ型のセット（文字列、整数、配列など）を定義します。
In most features, either you can explicitly define the schema for a feature group or the feature store will infer its schema using the first DataFrame written to it.
ほとんどの特徴では、特徴グループのスキーマを明示的に定義するか、特徴ストアが最初に書き込まれたDataFrameを使用してそのスキーマを推測します。
If a feature group contains time-series data, the event_time column value should capture the timestamp for when the feature values in that row were valid (not when the row of data was ingested).
特徴グループに時系列データが含まれている場合、`event_time` 列の値は、その行の特徴値が有効であった時刻のタイムスタンプをキャプチャする必要があります（データの行が取り込まれた時ではありません）。
If the feature group contains non-time-series data, you can omit the event_time column.
**特徴グループに非時系列データが含まれている場合、`event_time` 列を省略できます**。(うんうん、そうあるべきだよな...!:thinking:)

The entity ID is a unique identifier for an entity that has feature values.
エンティティIDは、**特徴値を持つエンティティの一意の識別子**です。
The entity ID can be either a natural key or a surrogate key.
エンティティIDは、自然キーまたは代理キーのいずれかです。
An example of a natural key is an email address or Social Security number for a user, while an example of a surrogate key is a sequential number, such as an auto-increment number, representing a user.
自然キーの例は、ユーザーのメールアドレスや社会保障番号であり、代理キーの例は、ユーザーを表す自動インクリメント番号などの連続番号です。

<!-- ここまで読んだ! -->

#### 1.5.1. Feature Groups Store Untransformed Feature Data　特徴グループは未変換の特徴データを保存します

Feature pipelines write untransformed feature data to feature groups.
特徴パイプラインは、未変換の特徴データを特徴グループに書き込みます。
The untransformed feature data becomes transformed feature data after MDTs are applied to feature data read in training and inference pipelines.
未変換の特徴データは、トレーニングおよび推論パイプラインで読み取られた特徴データにMDTが適用された後、変換された特徴データになります。
In general, feature groups should not store transformed feature values (that is, MDTs should not have been applied) because:
**一般的に、特徴グループは変換された特徴値を保存すべきではありません（つまり、MDTは適用されていないはずです）**理由は以下の通りです：

- The feature data is not reusable across models (model-specific transformations transform the data for use by a single model or set of related models).
  - 特徴データはモデル間で再利用できません（モデル固有の変換は、単一のモデルまたは関連するモデルのセットで使用するためにデータを変換します）。

- It can introduce _write amplification. If the MDT is parameterized by training_ data, such as standardizing a numerical feature, the time taken to perform a write becomes proportional to the number of rows in the feature group, not the num‐ ber of rows being written.
  - **書き込み増幅を引き起こす可能性があります。MDTがトレーニングデータによってパラメータ化されている場合（例えば、数値特徴の標準化など）、書き込みを実行するのにかかる時間は、書き込まれる行の数ではなく、特徴グループ内の行の数に比例**します。
    In the case of standardization, this is because updates first require reading all existing rows, recomputing the mean and standard deviation, and then updating the values of all rows with the new mean and standard deviation.
    標準化の場合、これは、更新が最初にすべての既存の行を読み取り、平均と標準偏差を再計算し、その後新しい平均と標準偏差で全ての行の値を更新する必要があるためです。

- Exploratory data analysis works best with unencoded feature data—it is hard for a data scientist to understand descriptive statistics for a numerical feature that has been scaled.
  - **探索的データ分析は、エンコードされていない特徴データで最も効果的に機能します。**スケーリングされた数値特徴の記述統計をデータサイエンティストが理解するのは難しいです。

<!-- ここまで読んだ! -->

#### 1.5.2. Feature Definitions and Feature Groups　 特徴定義と特徴グループ

A feature definition is the source code that defines the data transformations used to create one or more features in a feature group.
**特徴量定義は、特徴グループ内の1つ以上の特徴を作成するために使用されるデータ変換を定義するソースコード**です。(=feature pipelineの実装コード?? :thinking:)
In API-based feature stores, this is the source code for your MITs (and ODTs) in your feature pipelines.
APIベースの特徴ストアでは、これは特徴パイプライン内のMIT（およびODT）のためのソースコードです。
For example, it could be a Pandas, Polars, or Spark program for a batch feature pipeline.
例えば、**バッチ特徴パイプラインのためのPandas、Polars、またはSparkプログラム**である可能性があります。
In DSL-based feature stores, a feature definition is not just the declarative transformations that create the features but also the specification for the feature pipeline (batch, streaming, or on-demand).
DSLベースの特徴ストアでは、特徴定義は特徴を作成する宣言的変換だけでなく、特徴パイプライン（バッチ、ストリーミング、またはオンデマンド）の仕様でもあります。

<!-- ここまで読んだ! -->

#### 1.5.3. Writing to Feature Groups 特徴グループへの書き込み

Feature stores provide an API to ingest feature data.
特徴ストアは、特徴データを取り込むためのAPIを提供します。
The feature store manages the complexity of updating the feature data after ingestion in the offline store, online store, and vector index on your behalf—the updates in the background are transpar‐ ent to you as a developer.
**特徴ストアは、オフラインストア、オンラインストア、およびベクトルインデックスでの取り込み後の特徴データの更新の複雑さをあなたの代わりに管理**します。バックグラウンドでの更新は、開発者であるあなたには透明です。
Figure 4-6 shows two different types of APIs for ingesting feature data.
図4-6は、**特徴データを取り込むための2つの異なるタイプのAPI**を示しています。
In Figure 4-6(a), you have a single batch API for clients to write feature data to the offline store.
図4-6(a)では、クライアントが特徴データをオフラインストアに書き込むための単一のバッチAPIがあります。
The offline store is normally a lakehouse table, and it pro‐ [vides change data capture (CDC) APIs where you can read the data changes for the](https://oreil.ly/3jlEE) latest commit.
オフラインストアは通常、レイクハウステーブルであり、最新のコミットのデータ変更を読み取ることができる変更データキャプチャ（CDC）APIを提供します。
A background process runs either periodically or continually, reads any new commits since the last time it ran, and copies them to the online store and/or vector index.
**バックグラウンドプロセスは、定期的または継続的に実行され、最後に実行された時からの新しいコミットを読み取り、それらをオンラインストアおよび/またはベクトルインデックスにコピー**します。(prodのオフラインストア-devのオフラインストア間のデータコピーも、こういう感じでcommitを見てやると良かったりするのかな...!:thinking:)
For feature groups storing time-series data, the online store only stores the latest feature data for each entity (the row with the most recent event_time key value for each primary key).
**時系列データを保存する特徴グループの場合、オンラインストアは各エンティティの最新の特徴データのみを保存**します（各主キーに対して最も最近の `event_time` キー値を持つ行）。(うんうん、以前の気づきの認識通り...!:thinking:)

![]()
_Figure 4-6. Two different feature store architectures. In (a), clients write to the offline_ _feature store, and updates are periodically synchronized to the online store and vector_ _index. In (b), clients can also write via a stream API to an event-streaming platform,_ _after which updates are streamed to the online store and vector index and then periodi‐_ _cally synchronized to the offline store._
図4-6. 2つの異なる特徴ストアアーキテクチャ。(a)では、クライアントがオフライン特徴ストアに書き込み、更新が定期的にオンラインストアおよびベクトルインデックスに同期されます。(b)では、クライアントがイベントストリーミングプラットフォームへのストリームAPIを介して書き込むこともでき、その後、更新がオンラインストアおよびベクトルインデックスにストリーミングされ、定期的にオフラインストアに同期されます。

<!-- ここまで読んだ! -->

In Figure 4-6(b), there are two APIs: a batch API and a stream API.
図4-6(b)では、バッチAPIとストリームAPIの2つのAPIがあります。
Clients can use the batch API to write to only the offline store.
クライアントは、バッチAPIを使用してオフラインストアにのみ書き込むことができます。
If a feature group is online_enabled, clients write to the stream API.
特徴グループが `online_enabled` の場合、クライアントはストリームAPIに書き込みます。
Clients that write to the stream API can be either batch programs (Spark, Pandas, Polars) or stream processing programs (Flink, Spark Structured Streaming).
**ストリームAPIに書き込むクライアントは、バッチプログラム（Spark、Pandas、Polars）またはストリーム処理プログラム（Flink、Spark Structured Streaming）のいずれか**です。
Clients can use the stream API to write directly to the online store and vector index (here via an event-streaming platform), and updates are mate‐ rialized periodically to the offline store.
クライアントは、ストリームAPIを使用してオンラインストアおよびベクトルインデックスに直接書き込むことができ（ここではイベントストリーミングプラットフォームを介して）、**更新は定期的にオフラインストアにマテリアライズ**されます。
(なるほど、先にオンラインストアに書き込んで、オフラインストアには後で定期的にまとめて書き込む、という設計か...!:thinking:)
Feature data is available at lower latency in the online store via the stream API—that is, the stream API enables fresher features.
特徴データは、ストリームAPIを介してオンラインストアで低遅延で利用可能です。つまり、ストリームAPIは新鮮な特徴を可能にします。
For feature groups storing time-series data, the online store can again store either the latest feature data for each entity (the row with the most recent event_time key value for each primary key) or all feature data for entities subject to a TTL.
時系列データを保存する特徴グループの場合、オンラインストアは再び各エンティティの最新の特徴データ（各主キーに対して最も最近の `event_time` キー値を持つ行）またはTTLの対象となるエンティティのすべての特徴データを保存できます。
That is, a TTL can be specified for each row or feature group so that feature data is removed when its TTL has expired.
つまり、各行または特徴グループにTTLを指定でき、TTLが期限切れになると特徴データが削除されます。

###### 1.5.3.0.1. Feature freshness
###### 1.5.3.0.2. 特徴の新鮮さ

The freshness of feature data in feature groups is defined as the total time taken from when an event is first read by a feature pipeline to when the computed feature becomes available for use in an inference pipeline (see Figure 4-7).
特徴グループ内の特徴データの新鮮さは、イベントが特徴パイプラインによって最初に読み取られてから、計算された特徴が推論パイプラインで使用可能になるまでの総時間として定義されます（図4-7を参照）。

It includes the time taken for feature data to land in the online feature store and the time taken to read from the online store.
これには、特徴データがオンライン特徴ストアに到着するまでの時間と、オンラインストアから読み取るのにかかる時間が含まれます。

_Figure 4-7. Feature freshness is the time taken from when data is ingested to a feature_ _pipeline to when the computed feature or features become available for reading by_ _clients._
図4-7. 特徴の新鮮さは、データが特徴パイプラインに取り込まれてから、計算された特徴がクライアントによって読み取れるようになるまでの時間です。

Fresh features for real-time ML systems typically require streaming feature pipelines that update the feature store via a stream API.
リアルタイムMLシステムの新鮮な特徴は、通常、ストリームAPIを介して特徴ストアを更新するストリーミング特徴パイプラインを必要とします。

In Chapter 15, we will implement a TikTok-like recommender system, where features are created in streaming feature pipelines using information about your viewing activity.
第15章では、視聴活動に関する情報を使用してストリーミング特徴パイプラインで特徴が作成されるTikTokのようなレコメンダーシステムを実装します。

Within a second of a user action, feature values are created and made available as precomputed features in feature groups for predictions.
ユーザーアクションの1秒以内に、特徴値が作成され、予測のために特徴グループ内の事前計算された特徴として利用可能になります。

If it took minutes, instead of seconds, TikTok’s recommender would not feel like it tracks your intent in real time—the AI would feel too laggy to be useful as a recommender.
もしそれが秒ではなく分かかると、TikTokのレコメンダーはリアルタイムであなたの意図を追跡しているようには感じられません。AIはレコメンダーとして有用であるには遅すぎると感じられるでしょう。

###### 1.5.3.0.3. Data validation
###### 1.5.3.0.4. データ検証

Some feature stores support _data validation when writing feature data to feature_ groups.
一部の特徴ストアは、特徴データを特徴グループに書き込む際の _データ検証_ をサポートしています。

For each feature group, you specify constraints for valid feature data values.
各特徴グループに対して、有効な特徴データ値の制約を指定します。

For example, if the feature is an adult user’s age, you might specify that the age should be greater than 17 and less than 125.
例えば、特徴が成人ユーザーの年齢である場合、年齢は17歳より大きく125歳未満であるべきと指定することができます。

Data validation helps avoid problems with data quality in feature groups.
データ検証は、特徴グループ内のデータ品質の問題を回避するのに役立ちます。

Note that there are some exceptions to the general “garbage in, garbage out” principle.
一般的な「ゴミが入ればゴミが出る」原則にはいくつかの例外があることに注意してください。

For example, it is often OK to have missing feature values in a feature group, as you can impute those missing values later in your training and inference pipelines.
例えば、特徴グループに欠損特徴値があることはしばしば問題ありません。なぜなら、トレーニングおよび推論パイプラインで後でそれらの欠損値を補完できるからです。

Now that we’ve covered what a feature group is, what it stores, and how you update one, let’s now look at how to design a data model for feature groups.
特徴グループが何であるか、何を保存するか、どのように更新するかを説明したので、次に特徴グループのデータモデルを設計する方法を見てみましょう。

###### 1.5.3.0.5. Data Models for Feature Groups
###### 1.5.3.0.6. 特徴グループのデータモデル

If the feature store is to be the source of our data for AI, we need to understand how to model the data stored in its feature groups.
特徴ストアがAIのデータソースとなる場合、その特徴グループに保存されているデータをどのようにモデル化するかを理解する必要があります。

Data modeling for feature stores is the process of deciding:
特徴ストアのデータモデリングは、以下を決定するプロセスです：

- What features to create for which entities and what features to include in feature groups
- どのエンティティに対してどの特徴を作成し、特徴グループにどの特徴を含めるか

- What relationships between the feature groups look like
- 特徴グループ間の関係はどのようなものか

- What the freshness requirements for feature data is
- 特徴データの新鮮さの要件は何か

- What type of queries will be performed on the feature groups
- 特徴グループに対してどのようなクエリが実行されるか

Data modeling includes the design of a data model.
データモデリングには、データモデルの設計が含まれます。

Data model is a term from data‐ base theory that refers to how we decompose our data into different feature groups (tables), with the goals of:
データモデルは、データベース理論からの用語であり、データを異なる特徴グループ（テーブル）に分解する方法を指し、以下の目標を持っています：

- Ensuring the integrity of the data
- データの整合性を確保すること

- Improving the performance of writing the data
- データの書き込み性能を向上させること

- Improving the performance of reading (querying) the data
- データの読み取り（クエリ）性能を向上させること

- Improving the scalability of the system as data volumes and/or throughput increases
- データ量やスループットが増加するにつれてシステムのスケーラビリティを向上させること

You may have heard of entity-relationship diagrams (see Figure 4-8, for example) from relational databases.
リレーショナルデータベースからのエンティティ-リレーションシップ図（例えば、図4-8）を聞いたことがあるかもしれません。

Such diagrams provide a way to identify _entities (such as_ credit card transactions, user accounts, bank details, and merchant details) and the relationships among those entities.
そのような図は、エンティティ（クレジットカード取引、ユーザーアカウント、銀行の詳細、商人の詳細など）を特定し、それらのエンティティ間の関係を示す方法を提供します。

For example, a credit card transaction could have a reference (foreign key) to the credit card owner’s account, the bank that issued the card, and the merchant that performed the transaction.
例えば、クレジットカード取引は、クレジットカード所有者のアカウント、カードを発行した銀行、および取引を行った商人への参照（外部キー）を持つことができます。

In the relational data model, entities typically map to tables and relationships typically map to foreign keys.
リレーショナルデータモデルでは、エンティティは通常テーブルにマッピングされ、関係は通常外部キーにマッピングされます。


```md
In the relational data model,  
リレーショナルデータモデルでは、  

entities typically map to tables and relationships typically map to foreign keys. 
エンティティは通常テーブルにマッピングされ、関係は通常外部キーにマッピングされます。 

Simi‐ larly, in feature stores, an entity maps to a feature group and relationships map to foreign keys in a feature group. 
同様に、フィーチャーストアでは、エンティティはフィーチャーグループにマッピングされ、関係はフィーチャーグループ内の外部キーにマッピングされます。 

What is the process of going from requirements and data sources to a data model for feature groups, such as an entity-relationship diagram? 
要件とデータソースからフィーチャーグループのデータモデル（エンティティ-リレーションシップ図など）に移行するプロセスは何ですか？ 

There are two basic tech‐ niques we can use: 
私たちが使用できる基本的な技術は2つあります： 

_Normalization_ Reduce data redundancy and improve data integrity. 
_正規化_ データの冗長性を減らし、データの整合性を向上させます。 

_Denormalization_ Improve query performance by increasing data redundancy and endangering data integrity. 
_非正規化_ データの冗長性を増やし、データの整合性を危険にさらすことでクエリパフォーマンスを向上させます。 

These two techniques produce data models that can be categorized into one of two types: denormalized data models that include redundant (duplicated) data and nor‐ malized data models that eliminate redundant data. 
これらの2つの技術は、冗長（重複）データを含む非正規化データモデルと冗長データを排除する正規化データモデルの2つのタイプに分類できるデータモデルを生成します。 

The benefits and drawbacks of both approaches are shown in Table 4-2. 
両方のアプローチの利点と欠点は、表4-2に示されています。 

_Table 4-2. Comparison of denormalized data models with normalized data models_ 
_表4-2. 非正規化データモデルと正規化データモデルの比較_ 

**Denormalized data model** **Normalized data model**  
**非正規化データモデル** **正規化データモデル**  

Data storage costs Higher, due to redundant data in the (row-oriented) online store  
データストレージコストは、（行指向）オンラインストアに冗長データがあるため高くなります。  

Lower, due to no redundant data  
冗長データがないため低くなります。  

Query complexity Lower, due to less need for joins when reading from the online store  
クエリの複雑さは、オンラインストアから読み取る際の結合の必要が少ないため低くなります。  

Higher, due to more joins needed when querying data  
データをクエリする際に必要な結合が多いため高くなります。  

In general, denormalized data models are more prevalent in columnar data stores (lakehouses and data warehouses), as they can often efficiently compress redundant data in columns with columnar compression techniques like run-length encoding. 
一般的に、非正規化データモデルはカラム型データストア（レイクハウスやデータウェアハウス）でより一般的であり、カラム圧縮技術（ランレングスエンコーディングなど）を使用してカラム内の冗長データを効率的に圧縮できます。 

On the other hand, row-oriented data stores cannot efficiently compress redundant data, and they therefore favor normalized data models. 
一方、行指向データストアは冗長データを効率的に圧縮できないため、正規化データモデルを好みます。 

Before we start identifying entities, features, and feature groups for entities/features, we should consider the types of AI systems that will use the feature data: 
エンティティ/フィーチャーのためのエンティティ、フィーチャー、およびフィーチャーグループを特定する前に、フィーチャーデータを使用するAIシステムの種類を考慮する必要があります： 

- Batch ML systems 
- バッチMLシステム 

- Real-time ML systems (including LLMs/agents) 
- リアルタイムMLシステム（LLM/エージェントを含む） 

For batch ML systems, feature groups only need to store data in their offline store. 
バッチMLシステムでは、フィーチャーグループはオフラインストアにデータを保存するだけで済みます。 

As such, for columnar stores we could consider existing data models, such as the star schema or snowflake schema that are widely used in analytical and business intelli‐ gence environments. 
そのため、カラム型ストアでは、分析やビジネスインテリジェンス環境で広く使用されているスタースキーマやスノーフレークスキーマなどの既存のデータモデルを考慮できます。 

For real-time ML systems, we have feature groups with tables in both the offline and online store. 
リアルタイムMLシステムでは、オフラインストアとオンラインストアの両方にテーブルを持つフィーチャーグループがあります。 

Note that we don’t need to consider vector indexes here, as they are just columns in existing online tables.  
ここではベクトルインデックスを考慮する必要はありません。なぜなら、それらは既存のオンラインテーブルの列に過ぎないからです。 

If we want a general-purpose data model that works equally well for both batch and real-time queries, we will see in the next section that the snowflake schema (a nor‐ malized data model) is our preferred methodology for data modeling in feature stores. 
バッチとリアルタイムのクエリの両方に対して同様に機能する汎用データモデルを望む場合、次のセクションでスノーフレークスキーマ（正規化データモデル）がフィーチャーストアにおけるデータモデリングの好ましい方法論であることがわかります。 

Some feature stores only support the star schema, however, so we will intro‐ duce both data models. 
ただし、一部のフィーチャーストアはスタースキーマのみをサポートしているため、両方のデータモデルを紹介します。 

The star schema and snowflake schema are data models that organize data into a fact table that connects to dimension tables. 
スタースキーマとスノーフレークスキーマは、データをファクトテーブルに整理し、次元テーブルに接続するデータモデルです。 

In the star schema, columns in the dimension tables can be redundant (duplicated), but the snowflake schema extends the star schema to enable dimension tables to be connected to other dimension tables, enabling a normalized data model with no redundant data. 
スタースキーマでは、次元テーブルの列は冗長（重複）である可能性がありますが、スノーフレークスキーマはスタースキーマを拡張して次元テーブルを他の次元テーブルに接続できるようにし、冗長データのない正規化データモデルを可能にします。 

We will now look at how to design a star schema or snowflake schema data model with fact and dimension tables using dimension modeling. 
次に、次元モデリングを使用してファクトテーブルと次元テーブルを持つスタースキーマまたはスノーフレークスキーマデータモデルを設計する方法を見ていきます。 

Other popular data models used in columnar stores include the _data vault model (used to efficiently handle data ingestion, where_ data can arrive late and schema changes happen frequently) and the one big table (OBT) data model (which simplifies data modeling by storing as much data as possible in a single wide table). 
カラム型ストアで使用される他の人気のあるデータモデルには、_データボールトモデル（データの取り込みを効率的に処理するために使用され、データが遅れて到着したり、スキーマ変更が頻繁に発生する場合）_や、1つの大きなテーブル（OBT）データモデル（できるだけ多くのデータを単一の広いテーブルに保存することでデータモデリングを簡素化します）が含まれます。 

OBT is not suitable for AI systems because it would store all the labels and features in a single denormalized table, which would explode stor‐ age requirements in the (row-oriented) online store, and it is not suited for storing feature values that change over time. 
OBTは、すべてのラベルとフィーチャーを単一の非正規化テーブルに保存するため、AIシステムには適しておらず、（行指向）オンラインストアでのストレージ要件が爆発的に増加し、時間とともに変化するフィーチャー値を保存するのにも適していません。 

You can [learn more about data modeling in the book Fundamentals of Data](https://learning.oreilly.com/library/view/fundamentals-of-data/9781098108298/) _[Engineering by Joe Reis and Matt Housley (O’Reilly, 2022).](https://learning.oreilly.com/library/view/fundamentals-of-data/9781098108298/)_ 
データモデリングについては、[書籍『Fundamentals of Data Engineering』](https://learning.oreilly.com/library/view/fundamentals-of-data/9781098108298/) _（Joe ReisとMatt Housley著、O’Reilly、2022年）_で詳しく学ぶことができます。 

###### Dimension Modeling with a Credit Card Data Mart 
###### クレジットカードデータマートを用いた次元モデリング 

The most popular data modeling technique in data warehousing is dimension model‐ ing that categorizes data as facts and dimensions. 
データウェアハウジングで最も人気のあるデータモデリング技術は、データをファクトと次元に分類する次元モデリングです。 

Facts are usually measured quanti‐ ties, but they can also be qualitative. 
ファクトは通常測定可能な量ですが、定性的であることもあります。 

_Dimensions are attributes of facts. Some_ dimensions change in value over time and are called _slowly changing dimensions_ (SCD). 
_次元はファクトの属性です。一部の_ 次元は時間とともに値が変化し、_徐々に変化する次元_（SCD）と呼ばれます。 

Let’s look at an example of facts and dimensions in a credit card transactions _data mart. A data mart is a subset of a data warehouse (or lakehouse) that contains_ data focused on a specific business line, team, or product. 
クレジットカード取引の_データマートにおけるファクトと次元の例を見てみましょう。データマートは、特定のビジネスライン、チーム、または製品に焦点を当てたデータを含むデータウェアハウス（またはレイクハウス）のサブセットです。 

In our example, the credit card transactions are the facts and the dimensions are data about the credit card transactions, such as the card holder, their account details, the bank details, and the merchant details. 
私たちの例では、クレジットカード取引がファクトであり、次元はカード保有者、アカウントの詳細、銀行の詳細、商人の詳細など、クレジットカード取引に関するデータです。 

We will use this data mart to power a real-time ML system for predicting credit card fraud. 
このデータマートを使用して、クレジットカード詐欺を予測するリアルタイムMLシステムを構築します。 

But first, let’s look at our data mart, as illustrated in an entity-relationship diagram in Figure 4-8 using a snowflake schema data model.  
しかしまず、スノーフレークスキーマデータモデルを使用して、図4-8のエンティティ-リレーションシップ図に示されているデータマートを見てみましょう。 

_Figure 4-8. The credit card transaction facts and the dimension tables, organized in a_ _snowflake schema data model. The lines between the tables represent the foreign keys_ _that link the tables to one another. For example, card_details includes a reference to_ _the account that owns the card (account_details) and the bank that issued the card_ _(bank_details)._ 
_図4-8. クレジットカード取引のファクトと次元テーブル、スノーフレークスキーマデータモデルで整理されています。テーブル間の線は、テーブルを相互にリンクする外部キーを表しています。たとえば、card_detailsには、カードを所有するアカウント（account_details）とカードを発行した銀行（bank_details）への参照が含まれています。_

The _fact table stores_ `credit_card_transactions, a unique ID for the transaction` (t_id), the credit card number (cc_num), a timestamp for the transaction (ts), the amount spent (amount), the IP address of the merchant, and code indicating whether the transaction was online or physical (card_present). 
_ファクトテーブルには、`credit_card_transactions、取引の一意のID`（t_id）、クレジットカード番号（cc_num）、取引のタイムスタンプ（ts）、支出額（amount）、商人のIPアドレス、および取引がオンラインか物理的かを示すコード（card_present）が保存されます。_

The dimension tables for the credit card transactions are: 
クレジットカード取引の次元テーブルは次のとおりです： 

``` card_details 
``` cardのexpiry_dateとissue_date、カードの種類（クレジット、デビット、プリペイド、またはバーチャル）、そのステータス（アクティブ、ブロック、または紛失/盗難）、およびアカウントおよび銀行の詳細テーブルへの外部キー（外部キーにより、これはスノーフレークスキーマデータモデルになります） 
``` account_details 
``` アカウント保有者の名前と住所、前月末の負債、アカウントが作成された日と閉鎖された日（end_date）、および行が最後に変更された日 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 
``` 



``` bank_details
``` The bank’s `credit_rating, its` `country, and the date when a row was` ```   last_modified merchant_details
``` A count of chargebacks for the merchant on the previous day (chargeback_prev_day), the merchant’s category code (category), its `country,` and the date when a row was last_modified
```
``` bank_details
``` 銀行の `信用格付け、国、` および行が最後に変更された日付 ``` merchant_details
``` 前日のマーチャントのチャージバックのカウント（chargeback_prev_day）、マーチャントのカテゴリコード（category）、その `国、` および行が最後に変更された日付
```

The credit card transactions table is populated using the _event sourcing pattern,_ whereby once per hour, an ETL Spark job reads all the credit card transactions that arrived in Kafka during the previous hour and persists the events as rows in the ``` credit_card_transactions table. 
クレジットカード取引テーブルは、_イベントソーシングパターン_を使用して構築されており、1時間ごとにETL Sparkジョブが前の1時間にKafkaに到着したすべてのクレジットカード取引を読み取り、イベントを``` credit_card_transactions テーブルの行として永続化します。

The dimension tables are updated by ETL (extract, transform, load) or ELT (extract, load, transform) pipelines that read changes to dimensions for operational databases (not shown). 
次元テーブルは、運用データベースの次元の変更を読み取るETL（抽出、変換、ロード）またはELT（抽出、ロード、変換）パイプラインによって更新されます（表示されていません）。

We will now see how we can use the credit card transaction events in Kafka and the dimension tables to build our realtime fraud detection ML system. 
これから、Kafka内のクレジットカード取引イベントと次元テーブルを使用して、リアルタイムの不正検出MLシステムを構築する方法を見ていきます。

###### 1.5.3.0.7. Labels are facts, and features are dimensions
###### 1.5.3.0.8. ラベルは事実であり、特徴は次元です

In a feature store, the facts are the labels (or targets/observations) for our models, while the features are dimensions for the labels. 
フィーチャーストアでは、事実はモデルのラベル（またはターゲット/観察）であり、特徴はラベルの次元です。

Like facts, the labels are immutable events that often have a timestamp associated with them. 
事実と同様に、ラベルは不変のイベントであり、しばしばそれに関連付けられたタイムスタンプがあります。

For example, in our credit card fraud model, we will have an is_fraud label for a given credit card transaction and a timestamp for when the credit card transaction took place. 
例えば、私たちのクレジットカード不正モデルでは、特定のクレジットカード取引に対してis_fraudラベルがあり、クレジットカード取引が行われた時刻のタイムスタンプがあります。

The features for that model will be the card usage statistics, details about the card itself (the expiry date), the cardholder, the bank, and the merchant. 
そのモデルの特徴は、カード使用統計、カード自体の詳細（有効期限）、カード保有者、銀行、およびマーチャントです。

These features are dimensions for the labels, and they are often mutable data. 
これらの特徴はラベルの次元であり、しばしば可変データです。

Sometimes they are SCDs, but in real-time ML systems, they might be fast-changing dimensions. 
時にはそれらはSCD（ Slowly Changing Dimensions ）ですが、リアルタイムMLシステムでは、迅速に変化する次元である可能性があります。

Irrespective of whether the feature values change slowly or quickly, if we want to use a feature as training data for a model, it is crucial to save all values for features at all points in time. 
特徴値が遅く変化するか早く変化するかにかかわらず、モデルのトレーニングデータとして特徴を使用したい場合は、すべての時点での特徴のすべての値を保存することが重要です。

If you don’t know when and how a feature changes its value over time, then training data created using that feature could have future data leakage or include stale feature values. 
特徴が時間の経過とともにいつどのように値を変更するかがわからない場合、その特徴を使用して作成されたトレーニングデータは、将来のデータリークを引き起こしたり、古い特徴値を含む可能性があります。

###### 1.5.3.0.9. Feature stores and SCD types
###### 1.5.3.0.10. フィーチャーストアとSCDタイプ

Dimension modeling in data warehousing introduced SCD types to store changing values of dimensions (features). 
データウェアハウジングにおける次元モデリングは、次元（特徴）の変更される値を保存するためにSCDタイプを導入しました。

There are at least five well-known ways to implement SCDs (SCD types), each optimized for different ways a dimension could change. 
SCD（SCDタイプ）を実装するための少なくとも5つのよく知られた方法があり、それぞれが次元が変更される異なる方法に最適化されています。

Implementing different SCD types in a data mart is a challenging job. 
データマートで異なるSCDタイプを実装することは困難な作業です。

However, we can massively simplify managing SCDs for feature stores for two reasons. 
しかし、フィーチャーストアのSCDを管理することは、2つの理由から大幅に簡素化できます。

Firstly, as feature values are observations of measurable quantities, each new feature value replaces the old feature value (a feature cannot have multiple alternative values at the same time). 
第一に、特徴値は測定可能な量の観察であるため、各新しい特徴値は古い特徴値を置き換えます（特徴は同時に複数の代替値を持つことはできません）。

Secondly, there are a limited number of query patterns for reading feature data—you read training data and batch inference data from the offline store and rows of feature vectors from the online store. 
第二に、特徴データを読み取るためのクエリパターンは限られています—オフラインストアからトレーニングデータとバッチ推論データを読み取り、オンラインストアから特徴ベクトルの行を読み取ります。

That is, feature stores do not need to support all five SCD types; instead, they need a very specific set of SCD types (0, 2, and 4), and you can unobtrusively add support for those types to feature groups by simply specifying the event_time column in your feature group. 
つまり、フィーチャーストアは5つのSCDタイプすべてをサポートする必要はなく、非常に特定のSCDタイプ（0、2、および4）を必要とし、フィーチャーグループ内でevent_time列を指定するだけで、それらのタイプをフィーチャーグループに目立たず追加できます。

In this way, feature stores simplify support for SCDs compared with general-purpose data warehouses. 
このようにして、フィーチャーストアは汎用データウェアハウスと比較してSCDのサポートを簡素化します。

Table 4-3 shows how feature stores implement SCD Types 0, 2, and 4 with the relatively straightforward approach of specifying the feature group column that stores the ``` event_time.
``` 
表4-3は、フィーチャーストアが``` event_timeを保存するフィーチャーグループ列を指定する比較的簡単なアプローチでSCDタイプ0、2、および4を実装する方法を示しています。

**SCD** **type**
**SCD** **タイプ**

**Usage** **Description** **Feature store**
**使用法** **説明** **フィーチャーストア**

Type 0 Immutable feature data
Type 0 不変の特徴データ

Type 2 Mutable feature data used by batch ML systems
Type 2 バッチMLシステムで使用される可変特徴データ

Type 4 Online features for real-time ML systems; offline data for training
Type 4 リアルタイムMLシステムのオンライン特徴; トレーニング用のオフラインデータ

No history is kept for feature data, so this type is suitable for features that are immutable. 
特徴データの履歴は保持されないため、このタイプは不変の特徴に適しています。

When a feature value is updated for an entity ID, a new row is created with a new event_time (but the same entity ID). 
エンティティIDの特徴値が更新されると、新しいevent_time（ただし同じエンティティID）で新しい行が作成されます。

Each new row is a new version of the feature data. 
各新しい行は特徴データの新しいバージョンです。

Features are stored as records in two different tables—a table in the online store with the latest feature values and a table in the offline store with historical feature values. 
特徴は2つの異なるテーブルにレコードとして保存されます—オンラインストアの最新の特徴値を持つテーブルと、オフラインストアの履歴的な特徴値を持つテーブルです。

Feature group, no ``` event_time
```
フィーチャーグループ、``` event_timeなし

Offline feature group with event_time  
event_timeを持つオフラインフィーチャーグループ

Online/offline feature group with ``` event_time
```
``` event_timeを持つオンライン/オフラインフィーチャーグループ

Type 0 SCD is a feature group that stores immutable feature data. 
Type 0 SCDは不変の特徴データを保存するフィーチャーグループです。

If you do not define the event_time column for your feature group, you have a feature group with Type 0 SCD. 
フィーチャーグループにevent_time列を定義しない場合、Type 0 SCDを持つフィーチャーグループがあります。

Type 2 SCD is an offline-only feature group (for batch ML systems), where we have the historical records for the time-series data. 
Type 2 SCDはオフライン専用のフィーチャーグループ（バッチMLシステム用）で、時系列データの履歴レコードを持っています。

In classical Type 2 SCD, it is assumed that rows need both an `end_date and an` `effective_date (as multiple` dimension values may be valid at any point in time). 
古典的なType 2 SCDでは、行には`end_date`と`effective_date`の両方が必要であると仮定されます（複数の次元値が任意の時点で有効である可能性があるため）。

However, in the feature store, we don’t need an end_date—only the effective_date, called the event_time, as only a single feature value is valid at any given point in time. 
しかし、フィーチャーストアでは、end_dateは必要ありません—有効な特徴値は任意の時点で1つだけであるため、event_timeと呼ばれるeffective_dateのみが必要です。

Type 4 SCD is implemented as a feature group, backed by tables in both the online and offline stores. 
Type 4 SCDはフィーチャーグループとして実装され、オンラインストアとオフラインストアの両方のテーブルによってサポートされます。

A table in the online store stores the latest feature data values, and a table with the same name and schema in the offline store stores all of the historical feature data values. 
オンラインストアのテーブルは最新の特徴データ値を保存し、オフラインストアの同じ名前とスキーマのテーブルはすべての履歴的な特徴データ値を保存します。

In traditional Type 4 SCD, the historical table does not store the latest values, but feature stores support a variant of Type 4 SCD where the offline store stores both the latest feature values and the historical values. 
従来のType 4 SCDでは、履歴テーブルは最新の値を保存しませんが、フィーチャーストアはオフラインストアが最新の特徴値と履歴値の両方を保存するType 4 SCDのバリアントをサポートしています。

Feature stores hide the complexity of designing a data model that implements these three different SCD types by implementing the data models in their read/write APIs. 
フィーチャーストアは、読み取り/書き込みAPIでデータモデルを実装することによって、これらの3つの異なるSCDタイプを実装するデータモデルの設計の複雑さを隠します。

For example, in the AWS SageMaker feature store (an API-based feature store), you only need to specify the event_time column when defining a feature group:
例えば、AWS SageMakerフィーチャーストア（APIベースのフィーチャーストア）では、フィーチャーグループを定義する際にevent_time列を指定するだけで済みます：



feature_group.create(     description = "Some info about the feature group",     feature_group_name = "feature_group_name",     event_time_feature_name = event_time_feature_name,     enable_online_store = True,     ...
tags = ["tag1","tag2"]   )
feature_group.create(     description = "フィーチャーグループに関する情報",     feature_group_name = "feature_group_name",     event_time_feature_name = event_time_feature_name,     enable_online_store = True,     ...
tags = ["tag1","tag2"]   )

Writes to this feature group will create Type 4 SCD features, with the latest feature data in a key-value store (ElastiCache or DynamoDB), and historical feature data in a columnar store (Apache Iceberg).
このフィーチャーグループへの書き込みは、最新のフィーチャーデータをキー-バリューストア（ElastiCacheまたはDynamoDB）に、過去のフィーチャーデータをカラムストア（Apache Iceberg）に格納するType 4 SCDフィーチャーを作成します。

###### Real-Time Credit Card Fraud Detection ML System
###### リアルタイムクレジットカード不正検知MLシステム

Let’s now start designing our real-time ML system to predict whether a credit card transaction is fraudulent. 
それでは、クレジットカード取引が不正であるかどうかを予測するためのリアルタイムMLシステムの設計を始めましょう。

This operational ML system (online inference pipeline) has a service-level objective (SLO) of 50 ms latency or lower to make the decision on whether there is suspicion of fraud or not. 
この運用MLシステム（オンライン推論パイプライン）は、不正の疑いがあるかどうかの決定を下すために、50ms以下のレイテンシーというサービスレベル目標（SLO）を持っています。

It receives a prediction request with the credit card transaction details, retrieves precomputed features from the feature store, computes ODTs, merges the precomputed and real-time features in a single feature vector, applies any MDTs, makes the prediction, logs the prediction and the features, and returns the prediction (fraud or not fraud) to the client.
このシステムは、クレジットカード取引の詳細を含む予測リクエストを受け取り、フィーチャーストアから事前計算されたフィーチャーを取得し、ODTsを計算し、事前計算されたフィーチャーとリアルタイムフィーチャーを単一のフィーチャーベクターに統合し、任意のMDTsを適用し、予測を行い、予測とフィーチャーをログに記録し、予測（不正または不正でない）をクライアントに返します。

To build this system and meet our SLO, we will need to write a streaming feature pipeline to create features directly from the events from Kafka, as shown in Figure 4-8. 
このシステムを構築し、SLOを満たすために、Kafkaからのイベントから直接フィーチャーを作成するストリーミングフィーチャーパイプラインを書く必要があります（図4-8を参照）。

Stream processing enables us to compute aggregations on recent historical activity on credit cards, such as how often a card has been used in the last 5 minutes, 15 minutes, or hour. 
ストリーム処理により、クレジットカードの最近の履歴活動に基づいて集計を計算することが可能になります。たとえば、過去5分、15分、または1時間にカードがどのくらい使用されたかを計算できます。

These features are called _windowed aggregations, as they com‐_ pute an aggregation over events that happen in a window of time. 
これらのフィーチャーは「ウィンドウ集計」と呼ばれ、特定の時間ウィンドウ内で発生するイベントに基づいて集計を計算します。

It would not be possible to compute these features within our SLO if we only used the `credit_card_transactions` table in our data mart, as it is only updated hourly. 
データマート内の`credit_card_transactions`テーブルのみを使用した場合、これらのフィーチャーをSLO内で計算することは不可能です。なぜなら、このテーブルは1時間ごとにしか更新されないからです。

We can, however, compute other features from the data mart, such as the credit rating of the bank that issued the credit card and the number of chargebacks for the merchant that processed the credit card transaction.
しかし、データマートからは、クレジットカードを発行した銀行の信用評価や、クレジットカード取引を処理した商人のチャージバック数など、他のフィーチャーを計算することができます。

We will also create real-time features from the input request data with ODTs. 
また、ODTsを使用して入力リクエストデータからリアルタイムフィーチャーも作成します。

A feature with good predictive power for geographic fraud attacks is the distance and time between consecutive credit card transactions. 
地理的な不正攻撃に対して良好な予測力を持つフィーチャーは、連続するクレジットカード取引間の距離と時間です。

If the distance is large and the time is short, that is often indicative of fraud. 
距離が大きく、時間が短い場合、それはしばしば不正を示すものです。

For this, we compute `haversine_distance` and `time_since_last_transaction` features.
このために、`haversine_distance`と`time_since_last_transaction`フィーチャーを計算します。

We have described here an ML system that contains a mix of features computed using stream processing, batch processing, and ODTs. 
ここでは、ストリーム処理、バッチ処理、およびODTsを使用して計算されたフィーチャーの混合を含むMLシステムについて説明しました。

However, when we want to train models with these features, the training data will be stored in feature groups in the feature store. 
ただし、これらのフィーチャーを使用してモデルをトレーニングしたい場合、トレーニングデータはフィーチャーストアのフィーチャーグループに保存されます。

So we need to identify the features and then design a data model for the feature groups.
したがって、フィーチャーを特定し、その後フィーチャーグループのデータモデルを設計する必要があります。

###### Data model for our real-time fraud detection ML system
###### リアルタイム不正検知MLシステムのデータモデル

We are using a supervised ML model for predicting fraud, so we will need to have some labeled observations of fraud. 
私たちは不正を予測するために教師ありMLモデルを使用しているため、不正のラベル付き観察がいくつか必要です。

For this, there is a new `cc_fraud` table, not in the data mart, with a `t_id` column (the unique identity for credit card transactions) that contains the credit card transactions identified as fraudulent, along with columns for the person who reported the fraud and an explanation for why the transaction is marked as fraudulent. 
これには、データマートには存在しない新しい`cc_fraud`テーブルがあり、`t_id`列（クレジットカード取引の一意の識別子）が含まれており、不正と特定されたクレジットカード取引が含まれています。また、不正を報告した人と、なぜその取引が不正としてマークされているのかの説明が含まれています。

The fraud team updates the `cc_fraud` table weekly in a Postgres database it manages. 
不正チームは、管理しているPostgresデータベース内の`cc_fraud`テーブルを毎週更新します。

Using the `cc_fraud` table, the data mart, and the event-streaming platform, we can create features that have predictive power for fraud and the labels, as shown in Table 4-4.
`cc_fraud`テーブル、データマート、およびイベントストリーミングプラットフォームを使用することで、表4-4に示すように、不正に対する予測力を持つフィーチャーとラベルを作成できます。

_Table 4-4. Features we can create from our data mart and event-streaming platform for credit card fraud_
_表4-4. クレジットカード不正に対してデータマートとイベントストリーミングプラットフォームから作成できるフィーチャー_

**Data sources** **Simple features** **Engineered features**
**データソース** **シンプルなフィーチャー** **エンジニアリングされたフィーチャー**

``` credit_card_transactions account_details cc_fraud credit_card_transactions credit_card_transactions card_details
``` 
``` credit_card_transactions account_details cc_fraud credit_card_transactions credit_card_transactions card_details
```

``` ``` amount ip_address card_present card_type status
``` ``` amount ip_address card_present card_type status
```

``` ``` {num}/{sum}_trans_last_10_mins {num}/{sum}_trans_last_hour {num}/{sum}_trans_last_day {num}/{sum}_trans_last_week prev_ts_transaction prev_ip_transaction prev_card_present_transaction haversine_distance time_since_last_transaction
``` ``` {num}/{sum}_trans_last_10_mins {num}/{sum}_trans_last_hour {num}/{sum}_trans_last_day {num}/{sum}_trans_last_week prev_ts_transaction prev_ip_transaction prev_card_present_transaction haversine_distance time_since_last_transaction
```

``` ``` is_fraud
``` ``` is_fraud
```

``` ``` days_to_card_expiry
``` ``` days_to_card_expiry
```

``` ``` account_details zipcode
``` ``` account_details zipcode
```

``` ``` merchant_details category chargeback_rate_prev_month chargeback_rate_prev_week bank_details credit_rating days_since_bank_cr_changed
``` ``` merchant_details category chargeback_rate_prev_month chargeback_rate_prev_week bank_details credit_rating days_since_bank_cr_changed
```

There are many frameworks and programming languages that we could use to create these features, and we will look at source code for them in the next few chapters. 
これらのフィーチャーを作成するために使用できる多くのフレームワークやプログラミング言語がありますが、次の章ではそれらのソースコードを見ていきます。

For now, we are interested in the data model for our feature groups that we will design to store and query these features, as well as the fraud labels. 
今のところ、これらのフィーチャーと不正ラベルを保存およびクエリするために設計するフィーチャーグループのデータモデルに興味があります。

The feature groups will need to be stored in both online and offline stores, as we will, respectively, use these features in our real-time ML system for inference and in our offline training pipeline.
フィーチャーグループは、リアルタイムMLシステムで推論に使用するためのオンラインストアと、オフライントレーニングパイプラインで使用するためのオフラインストアの両方に保存する必要があります。

We will now design two different data models, first using the star schema and then using the snowflake schema.
それでは、最初にスター・スキーマを使用し、次にスノーフレーク・スキーマを使用して、2つの異なるデータモデルを設計します。

###### 1.5.3.0.11. Star schema data model
###### 1.5.3.0.12. スター・スキーマデータモデル

The star schema data model is supported by all major feature stores. 
スター・スキーマデータモデルは、すべての主要なフィーチャーストアでサポートされています。

In Figure 4-9, we can see that the `cc_trans_fg` feature group containing the fraud labels is called a label feature group.
図4-9では、不正ラベルを含む`cc_trans_fg`フィーチャーグループがラベルフィーチャーグループと呼ばれていることがわかります。

_Figure 4-9. Star schema data model for our credit card fraud prediction ML system._ 
_図4-9. クレジットカード不正予測MLシステムのためのスター・スキーマデータモデル。_

_Labels (and on-demand features) are the facts, while feature groups are the dimension tables._
_ラベル（およびオンデマンドフィーチャー）は事実であり、フィーチャーグループは次元テーブルです。_

The feature group that contains the labels for our credit card transaction (fraud or not fraud) is known as the label feature group. 
クレジットカード取引（不正または不正でない）のラベルを含むフィーチャーグループは、ラベルフィーチャーグループとして知られています。

In practice, a label feature group is just a normal feature group. 
実際には、ラベルフィーチャーグループは通常のフィーチャーグループに過ぎません。

As we will see later, it is only when we select the features and labels for our model that we need to identify the columns in feature groups as either a feature or a label.
後で見るように、モデルのためにフィーチャーとラベルを選択する際にのみ、フィーチャーグループ内の列をフィーチャーまたはラベルとして特定する必要があります。

In the star schema data model, you can see that the label feature group contains foreign keys to the four feature groups that contain features computed from the data mart tables and the event-streaming platform. 
スター・スキーマデータモデルでは、ラベルフィーチャーグループがデータマートテーブルとイベントストリーミングプラットフォームから計算されたフィーチャーを含む4つのフィーチャーグループへの外部キーを含んでいることがわかります。

These feature groups are all updated independently in separate feature pipelines that run on their own schedule. 
これらのフィーチャーグループはすべて、独自のスケジュールで実行される別々のフィーチャーパイプラインで独立して更新されます。

For example, the `cc_trans_aggs_fg` feature group is computed by a streaming feature pipeline, while the `account_fg`, `bank_fg`, and `merchant_fg` feature groups are computed by batch jobs that run daily. 
たとえば、`cc_trans_aggs_fg`フィーチャーグループはストリーミングフィーチャーパイプラインによって計算され、一方で`account_fg`、`bank_fg`、および`merchant_fg`フィーチャーグループは毎日実行されるバッチジョブによって計算されます。

Note that we follow an idiom of appending _fg to feature group names to differentiate them from the tables in our data mart.
フィーチャーグループ名に_fgを追加して、データマート内のテーブルと区別するという慣用句に従っていることに注意してください。

###### 1.5.3.0.13. Snowflake schema data model
###### 1.5.3.0.14. スノーフレーク・スキーマデータモデル

The snowflake schema is a data model that, like the star schema, consists of tables containing labels and features. 
スノーフレーク・スキーマは、スター・スキーマと同様に、ラベルとフィーチャーを含むテーブルで構成されるデータモデルです。

In contrast to the star schema, however, in the snowflake schema the feature data is normalized, making the snowflake schema suitable as a data model for both online and offline tables. 
ただし、スター・スキーマとは異なり、スノーフレーク・スキーマではフィーチャーデータが正規化されているため、オンラインおよびオフラインテーブルのデータモデルとして適しています。

Each feature is split until it is normalized (see Figure 4-10). 
各フィーチャーは正規化されるまで分割されます（図4-10を参照）。

That is, there is no redundancy in the feature tables—no duplicated features.
つまり、フィーチャーテーブルには冗長性がなく、重複したフィーチャーはありません。

_Figure 4-10. Snowflake schema data model for our feature store for credit card fraud prediction._
_図4-10. クレジットカード不正予測のためのフィーチャーストアのスノーフレーク・スキーマデータモデル。_

In the snowflake schema, you can see that the label feature group now only has two foreign keys, compared to four foreign keys in the star schema data model. 
スノーフレーク・スキーマでは、ラベルフィーチャーグループが現在、スター・スキーマデータモデルの4つの外部キーに対して、わずか2つの外部キーしか持っていないことがわかります。

As we will see in the next section, the advantage of the snowflake schema here over the star schema is clearest when building a real-time ML system. 
次のセクションで見るように、リアルタイムMLシステムを構築する際に、スノーフレーク・スキーマの利点がスター・スキーマに対して最も明確になります。

In a real-time ML system, the foreign keys in the label feature groups need to be provided as part of prediction requests by clients. 
リアルタイムMLシステムでは、ラベルフィーチャーグループの外部キーは、クライアントによって予測リクエストの一部として提供する必要があります。

With a snowflake schema, clients only need to provide the `cc_num` and `merchant_id` as request parameters to retrieve all of the features—features from the nested tables are retrieved with a subquery. 
スノーフレーク・スキーマを使用すると、クライアントはすべてのフィーチャーを取得するために`cc_num`と`merchant_id`のみをリクエストパラメータとして提供すればよく、ネストされたテーブルからのフィーチャーはサブクエリで取得されます。

In the star schema, however, our real-time ML system needs to additionally provide the `bank_id` and `account_id` as request parameters. 
しかし、スター・スキーマでは、リアルタイムMLシステムは追加で`bank_id`と`account_id`をリクエストパラメータとして提供する必要があります。

This makes the real-time ML system more complex—either the client provides the values for `bank_id` and `account_id` as parameters or you have to maintain an additional mapping table from `cc_num` to `bank_id` and `account_id`.
これにより、リアルタイムMLシステムがより複雑になります。クライアントが`bank_id`と`account_id`の値をパラメータとして提供するか、`cc_num`から`bank_id`および`account_id`への追加のマッピングテーブルを維持する必要があります。

###### 1.5.3.0.15. Feature Store Data Model for Inference
###### 1.5.3.0.16. 推論のためのフィーチャーストアデータモデル

Labels are obviously not available during inference—our model predicts them. 
ラベルは推論中には明らかに利用できません—私たちのモデルがそれらを予測します。

Similarly, the index columns, the event time, and features in our label feature group (`cc_trans_fg`) are not available as precomputed features at online inference time. 
同様に、インデックス列、イベント時間、およびラベルフィーチャーグループ（`cc_trans_fg`）内のフィーチャーは、オンライン推論時に事前計算されたフィーチャーとしては利用できません。

They can all be passed as parameters in a prediction request (the foreign keys to the
これらはすべて、予測リクエストのパラメータとして渡すことができます（外部キーとして）。



###### 1.5.3.0.17. feature groups and the `amount features), resolved via mapping tables (for star sche‐` mas), or computed with ODTs (time_since_last_trans, haversine_distance, and ``` days_to_card_expiry) or MDTs. Label feature groups do not store inference data for
###### 1.5.3.0.18. 特徴グループと`amount features`は、マッピングテーブル（スタースキーマ用）を介して解決されるか、ODTs（time_since_last_trans、haversine_distance、及び``` days_to_card_expiry）またはMDTsで計算されます。ラベル特徴グループは、推論データを保存しません。

``` features. The label feature group is offline only, storing only historical data for fea‐ tures to create offline training data.
ラベル特徴グループはオフライン専用で、オフラインのトレーニングデータを作成するための特徴の履歴データのみを保存します。

###### Online Inference
###### オンライン推論

For online inference, a prediction request includes as parameters entity IDs (foreign keys), any passed feature values (for features in the label feature group), and any parameters needed to compute on-demand features (see Figure 4-11). 
オンライン推論では、予測リクエストには、エンティティID（外部キー）、ラベル特徴グループの特徴に対して渡された特徴値、およびオンデマンド特徴を計算するために必要なパラメータが含まれます（図4-11を参照）。

The online inference pipeline uses the foreign keys to retrieve all the precomputed features from child online feature groups. 
オンライン推論パイプラインは、外部キーを使用して子オンライン特徴グループからすべての事前計算された特徴を取得します。

Feature stores provide either language-level APIs (such as Python) or a REST API to retrieve the precomputed features.
特徴ストアは、事前計算された特徴を取得するために、言語レベルのAPI（Pythonなど）またはREST APIを提供します。

_Figure 4-11. During online inference, the rows in the label feature group are not avail‐_ _able as precomputed values. Instead, the parameters in a prediction request should_ _include the foreign keys (cc_num and merchant_id) and the passed features (amount,_ ``` ip_address, and card_present). The other features from the label feature group are
_Figure 4-11. オンライン推論中、ラベル特徴グループの行は事前計算された値として利用できません。代わりに、予測リクエストのパラメータには、外部キー（cc_numおよびmerchant_id）と渡された特徴（amount、``` ip_address、及びcard_present）を含める必要があります。ラベル特徴グループの他の特徴は

``` _computed with ODTs (haversine_distance, time_since_last_trans,_ ``` days_to_card_expiry).
``` ODTs（haversine_distance、time_since_last_trans、``` days_to_card_expiry）で計算されます。

###### Batch Inference
###### バッチ推論

Batch inference has data modeling challenges that are similar to those you’ll encounter with online inference. 
バッチ推論には、オンライン推論で直面するのと同様のデータモデリングの課題があります。

Imagine our real-time credit card fraud prediction problem as a batch ML system that predicts whether each of yesterday’s credit card transactions were fraudulent or not. 
私たちのリアルタイムのクレジットカード詐欺予測問題を、昨日の各クレジットカード取引が詐欺であったかどうかを予測するバッチMLシステムとして考えてみてください。

In this case, the labels are not available, of course. 
この場合、ラベルはもちろん利用できません。

We could replace the streaming feature pipeline that updates `cc_trans_fg` with a batch feature pipeline. 
`cc_trans_fg`を更新するストリーミング特徴パイプラインをバッチ特徴パイプラインに置き換えることができます。

Alternatively, we could use the `credit_card_transac` ``` tions table in our data mart and reimplement the three ODTs as MDTs (in the train‐
``` ングおよびバッチ推論パイプラインで）。

Feature stores often support batch inference data APIs, such as:
特徴ストアは、次のようなバッチ推論データAPIをサポートすることがよくあります。

- Read all feature data that has arrived in a given time frame.
- 特定の時間枠内に到着したすべての特徴データを読み取ります。

- Read all the latest feature data for a batch of entities (such as all active users).
- エンティティのバッチ（すべてのアクティブユーザーなど）に対する最新の特徴データをすべて読み取ります。

An alternative API is to allow batch inference clients to provide a Spine DataFrame containing the foreign keys and timestamps for features. 
別のAPIは、バッチ推論クライアントが特徴の外部キーとタイムスタンプを含むSpine DataFrameを提供できるようにすることです。

The feature store takes the Spine DataFrame and joins columns containing the feature values from the feature groups (using the foreign keys and timestamps to retrieve the correct feature values).
特徴ストアはSpine DataFrameを受け取り、特徴グループからの特徴値を含む列を結合します（外部キーとタイムスタンプを使用して正しい特徴値を取得します）。

The Spine DataFrame approach does not work well for case (1) but works well for case (2). 
Spine DataFrameアプローチはケース（1）にはうまく機能しませんが、ケース（2）にはうまく機能します。

Spine DataFrames also only work with star schema data models. 
Spine DataFrameはスタースキーマデータモデルでのみ機能します。

You have to do the work of adding all foreign keys to the Spine DataFrame, which is easy if we want to read the latest feature values for all users, and we pass a Spine DataFrame containing all user IDs. 
すべての外部キーをSpine DataFrameに追加する作業を行う必要があります。これは、すべてのユーザーの最新の特徴値を読み取る場合には簡単で、すべてのユーザーIDを含むSpine DataFrameを渡します。

However, reading all feature data since yesterday requires a more complex query over feature groups, and here, dedicated batch inference APIs to support such queries are helpful.
しかし、昨日以降のすべての特徴データを読み取るには、特徴グループに対してより複雑なクエリが必要であり、ここでそのようなクエリをサポートする専用のバッチ推論APIが役立ちます。

###### Reading Feature Data with a Feature View
###### 特徴ビューを使用した特徴データの読み取り

After you have designed a data model for your feature store, you need to be able to query it to read training and inference data. 
特徴ストアのデータモデルを設計した後、トレーニングデータと推論データを読み取るためにクエリを実行できる必要があります。

Feature stores do not provide full SQL query support for reading feature data. 
特徴ストアは、特徴データを読み取るための完全なSQLクエリサポートを提供しません。

Instead, they provide language-level APIs (Python, Java, etc.) and/or a REST API for retrieving training data, batch inference data, and online inference data. 
代わりに、トレーニングデータ、バッチ推論データ、およびオンライン推論データを取得するための言語レベルのAPI（Python、Javaなど）および/またはREST APIを提供します。

But, reading precomputed feature data is not the only task for a feature store. 
しかし、事前計算された特徴データを読み取ることは、特徴ストアの唯一のタスクではありません。

The feature store should also apply any MDTs and ODTs before returning feature data to clients.
特徴ストアは、クライアントに特徴データを返す前に、すべてのMDTsおよびODTsを適用する必要があります。

Feature stores provide an abstraction that hides the complexity of retrieving/comput‐ ing features for training and inference for a specific model (or group of related mod‐ els) called a feature view.  
特徴ストアは、特定のモデル（または関連するモデルのグループ）に対するトレーニングと推論のための特徴を取得/計算する複雑さを隠す抽象化を提供します。これを特徴ビューと呼びます。

The feature view is a selection of features and, optionally, labels to be used by one or more models for training and inference. 
特徴ビューは、1つまたは複数のモデルによるトレーニングと推論に使用される特徴と、オプションでラベルの選択です。

The features in a feature view may come from one or more feature groups.
特徴ビュー内の特徴は、1つまたは複数の特徴グループから来る場合があります。

When you have defined a feature view, you can typically use it to:
特徴ビューを定義したら、通常は次のように使用できます。

- Retrieve point-in-time correct training data
- 時点に正しいトレーニングデータを取得します。

- Retrieve point-in-time correct batch inference data
- 時点に正しいバッチ推論データを取得します。

- Retrieve precomputed features using foreign keys (entity IDs)
- 外部キー（エンティティID）を使用して事前計算された特徴を取得します。

- Apply MDTs to features when reading feature data for training and inference
- トレーニングと推論のために特徴データを読み取る際にMDTsを特徴に適用します。

- Apply ODTs in online inference pipelines
- オンライン推論パイプラインでODTsを適用します。

The feature view prevents skew between training and inference by ensuring that the same ordered sequence of features is returned when reading training and inference data, and that the same MDTs are applied to the training and inference data read from the feature store. 
特徴ビューは、トレーニングデータと推論データを読み取る際に同じ順序の特徴が返されることを保証し、特徴ストアから読み取ったトレーニングデータと推論データに同じMDTsが適用されることを保証することで、トレーニングと推論の間の偏りを防ぎます。

Feature views also apply ODTs in online inference pipelines and ensure they are consistent with the feature pipeline.
特徴ビューは、オンライン推論パイプラインでもODTsを適用し、特徴パイプラインと一貫性があることを保証します。

For training and batch inference data, feature stores support reading data as either DataFrames or files. 
トレーニングおよびバッチ推論データの場合、特徴ストアはデータをDataFrameまたはファイルとして読み取ることをサポートします。

For small data volumes, Pandas DataFrames are popular, but when data volumes exceed a few GBs, some feature stores support reading to Polars and/or Spark DataFrames. 
小さなデータボリュームの場合、Pandas DataFramesが人気ですが、データボリュームが数GBを超えると、一部の特徴ストアはPolarsおよび/またはSpark DataFramesへの読み取りをサポートします。

Spark DataFrames are, however, not that widely used in training pipelines, and when they are, they typically call `df.to_pandas() to trans‐` form the Spark DataFrame into a Pandas DataFrame. 
ただし、Spark DataFramesはトレーニングパイプラインで広く使用されているわけではなく、使用される場合は通常、`df.to_pandas()`を呼び出してSpark DataFrameをPandas DataFrameに変換します。

For large amounts of data (that don’t fit in a Polars or Pandas DataFrame), feature stores support creating training data as files in an external filesystem or object store, in file formats such as Parquet, CSV, and TFRecord (TensorFlow’s row-oriented file format that is also supported by PyTorch).
大量のデータ（PolarsまたはPandas DataFrameに収まらないデータ）については、特徴ストアは外部ファイルシステムまたはオブジェクトストアにファイルとしてトレーニングデータを作成することをサポートし、Parquet、CSV、TFRecord（TensorFlowの行指向ファイル形式で、PyTorchでもサポートされています）などのファイル形式を使用します。

Different feature stores use different names for feature views, including _Feature‐_ _Lookup (Databricks) and FeatureService (Feast, Tecton). 
異なる特徴ストアは、特徴ビューに異なる名前を使用しており、_Feature‐_ _Lookup（Databricks）やFeatureService（Feast、Tecton）などがあります。

I prefer the term feature view due to its close relationship to views from relational databases—a feature view is a selection of columns from different feature groups, and it is metadata-only (feature views do not store data). 
私は、特徴ビューという用語を好みます。これは、リレーショナルデータベースのビューとの密接な関係があるためです。特徴ビューは異なる特徴グループからの列の選択であり、メタデータのみです（特徴ビューはデータを保存しません）。

A feature view is also not a service when it is used in train‐ ing or batch inference pipelines, and it is not just a selection of features (as implied by a FeatureLookup). 
特徴ビューは、トレーニングまたはバッチ推論パイプラインで使用されるときにサービスではなく、単なる特徴の選択ではありません（FeatureLookupが示唆するように）。

In online inference, a feature view can be either deployed as a net‐ work service or embedded inside a model deployment. 
オンライン推論では、特徴ビューはネットワークサービスとしてデプロイされるか、モデルデプロイメント内に埋め込まれることができます。

For these reasons, we use the term feature view.  
これらの理由から、私たちは特徴ビューという用語を使用します。

Feature views can be extended to support client-side transformations (MDTs and ODTs). 
特徴ビューは、クライアント側の変換（MDTsおよびODTs）をサポートするように拡張できます。

For example, Hopsworks has support for declaratively attaching MDTs to selected features in a feature view, and feature views transparently compute both MDTs and ODTs when reading data from the feature store.
例えば、Hopsworksは、特徴ビュー内の選択された特徴にMDTsを宣言的に添付するサポートを提供しており、特徴ビューは特徴ストアからデータを読み取る際にMDTsとODTsの両方を透過的に計算します。

###### Point-in-Time Correct Training Data with Feature Views
###### 特徴ビューを使用した時点に正しいトレーニングデータの作成

When creating training data from time-series features, the goal is to ensure point-in_time correctness: every feature value joined to a label must be the one that was avail‐_ able at the label’s event time, without including future data or stale values. 
時系列特徴からトレーニングデータを作成する際の目標は、時点に正しいことを保証することです：ラベルに結合されたすべての特徴値は、未来のデータや古い値を含めずに、ラベルのイベント時間に利用可能であったものでなければなりません。

This is typically done using a temporal join.
これは通常、時間的結合を使用して行われます。

A temporal join starts from the table containing labels, then joins in features from other tables based on matching entity IDs and event-time alignment. 
時間的結合は、ラベルを含むテーブルから始まり、次に一致するエンティティIDとイベント時間の整合性に基づいて他のテーブルから特徴を結合します。

The following apply to each label row:
以下は各ラベル行に適用されます：

1. The join includes only feature rows whose event_time is less than or equal to the label’s event_time.
1. 結合には、event_timeがラベルのevent_time以下の特徴行のみが含まれます。

2. From those, you select the row with the most recent event_time before or equal to the label’s timestamp.
2. その中から、ラベルのタイムスタンプ以前または同時の最も最近のevent_timeを持つ行を選択します。

3. If no feature rows meet the condition, the join returns `NULL values for those` features.
3. 条件を満たす特徴行がない場合、結合はそれらの特徴に対して`NULL値を返します。

The temporal join is implemented as an `ASOF LEFT JOIN. The` `ASOF condition` ensures that there is no future data leakage for the joined feature values, and the LEFT ``` JOIN ensures that label rows are preserved even when no matching feature rows exist.
時間的結合は`ASOF LEFT JOIN`として実装されます。`ASOF条件`は、結合された特徴値に対する未来のデータ漏洩がないことを保証し、LEFT ``` JOINは、一致する特徴行が存在しない場合でもラベル行が保持されることを保証します。

The number of rows in the training data should be the same as the number of rows in the table containing the labels.
トレーニングデータの行数は、ラベルを含むテーブルの行数と同じであるべきです。

The ASOF keyword is not yet part of the ANSI SQL standard. 
ASOFキーワードはまだANSI SQL標準の一部ではありません。

As a consequence, some databases (such as ClickHouse and Feldera) use ```        LEFT ASOF JOIN, others (such as DuckDB) use ASOF LEFT JOIN,
その結果、一部のデータベース（ClickHouseやFelderなど）は``` LEFT ASOF JOINを使用し、他のデータベース（DuckDBなど）はASOF LEFT JOINを使用します。

and Snowflake supports ASOF JOIN (it can only be a left join).
SnowflakeはASOF JOINをサポートしています（左結合のみです）。

In Figure 4-12, we can see how the `ASOF LEFT JOIN creates the training data from` four different feature groups (we omitted account_fg for brevity). 
図4-12では、`ASOF LEFT JOINが4つの異なる特徴グループからトレーニングデータを作成する様子を見ることができます（簡潔さのためにaccount_fgは省略しました）。

Starting from the label feature group (cc_trans_fg), it joins in features from the other three feature groups (cc_trans_aggs_fg, `bank_fg,` `merchant_fg), as of the` `event_time in` ``` cc_trans.
ラベル特徴グループ（cc_trans_fg）から始まり、他の3つの特徴グループ（cc_trans_aggs_fg、`bank_fg、` `merchant_fg）から特徴を結合します。これは、``` cc_transのevent_timeに基づいています。
```



. For each row in the
各行に対して、最終出力の中で、結合された行は、ラベル特徴グループの``` event_tsの値に最も近いが、それよりも小さいevent_tsを持っています。これはLEFT JOINであり、INNER JOINではありません。なぜなら、INNER JOINは、ラベルテーブルの外部キーが特徴テーブルの行と一致しない場合、トレーニングデータから行を除外するからです。

###### 1.5.3.0.19. Online Inference with a Feature View
###### 1.5.3.0.20. 特徴ビューを用いたオンライン推論
In online inference, the feature view provides APIs for retrieving precomputed features, similarity search with vector indexes, and computing ODTs and MDTs. 
オンライン推論では、特徴ビューが事前計算された特徴を取得するためのAPI、ベクトルインデックスを用いた類似検索、ODTsおよびMDTsの計算を提供します。 
In the credit card fraud example ML system, there are two queries required to retrieve the features from our data model at request time:
クレジットカード詐欺の例のMLシステムでは、リクエスト時にデータモデルから特徴を取得するために必要な2つのクエリがあります：
- A primary key lookup for the merchant features using merchant_id
- merchant_idを使用したマーチャント特徴の主キー検索
- A left join to read the aggregation and bank features using cc_num
- cc_numを使用して集約および銀行の特徴を読み取るための左結合
The feature view provides a single API call, `get_feature_vector(), that executes` both of these queries and also applies any ODTs and MDTs before returning a feature vector: 
特徴ビューは、これらの2つのクエリを実行し、特徴ベクトルを返す前にODTsおよびMDTsを適用する単一のAPI呼び出し`get_feature_vector()`を提供します：
```  
feature_vector = feature_view.get_feature_vector(  
entry = [{"cc_num": 1234567811112222, "merchant_id": 212}]  
)  
``` 
The feature_vector could be of the list type, a NumPy array, or even a DataFrame, depending on the input format expected by the model.  
特徴ベクトルは、モデルが期待する入力形式に応じて、リスト型、NumPy配列、またはDataFrameである可能性があります。

-----
###### 1.5.3.0.21. Summary and Exercises
###### 1.5.3.0.22. まとめと演習
Feature stores are the data layer for AI systems. 
フィーチャーストアはAIシステムのデータ層です。 
We dived deep into the anatomy of a feature store, and we looked at when it is appropriate for you to use one. 
私たちはフィーチャーストアの構造を深く掘り下げ、いつそれを使用するのが適切かを見てきました。 
We looked at how feature groups store feature data in multiple data stores: row-oriented, column-oriented, and vector indexes. 
フィーチャーグループが行指向、列指向、ベクトルインデックスの複数のデータストアにフィーチャーデータをどのように保存するかを見ました。 
We also learned about how to organize your feature data in a data model for batch and real-time ML systems. 
バッチおよびリアルタイムのMLシステムのためにフィーチャーデータをデータモデルでどのように整理するかについても学びました。 
We introduced feature views and described how they query feature data for training and inference without skew. 
フィーチャービューを紹介し、トレーニングと推論のためにフィーチャーデータを歪みなくクエリする方法を説明しました。 
In the next chapter, we will look at a specific feature store, the Hopsworks feature store.
次の章では、特定のフィーチャーストアであるHopsworksフィーチャーストアを見ていきます。 
The following exercises will help you learn how to design your own data models. 
以下の演習は、独自のデータモデルを設計する方法を学ぶのに役立ちます。 
In each exercise, ask yourself if you need to add a new feature group or new foreign keys to existing feature groups, how you will compute the new feature (batch or streaming), and so on:
各演習で、新しいフィーチャーグループを追加する必要があるか、既存のフィーチャーグループに新しい外部キーを追加する必要があるか、新しいフィーチャーをどのように計算するか（バッチまたはストリーミング）、などを自問してください：
- Describe the feature pipeline that you would use to compute a new feature: average merchant spend per month. 
- 新しいフィーチャーを計算するために使用するフィーチャーパイプラインを説明してください：月ごとの平均マーチャント支出。 
What are its inputs/outputs and batch/streaming, and where would you add the feature to our data model?
その入力/出力は何で、バッチ/ストリーミングはどうなっていて、どこにそのフィーチャーをデータモデルに追加しますか？
- Add a total credit card lifetime spend feature.
- クレジットカードの生涯支出の合計フィーチャーを追加してください。 
- A new device ID becomes available as part of each credit card transaction. 
- 新しいデバイスIDが各クレジットカード取引の一部として利用可能になります。 
How will you update your data model for your feature groups? 
フィーチャーグループのためにデータモデルをどのように更新しますか？ 
What new features could you use?  
どのような新しいフィーチャーを使用できますか？



