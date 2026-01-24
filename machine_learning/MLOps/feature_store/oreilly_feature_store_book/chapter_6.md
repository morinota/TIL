# 1. CHAPTER 6: Model-Independent Transformations 第6章：モデル非依存の変換

Our focus now switches to how to write the data transformation logic for feature pipelines. 
私たちの焦点は、**フィーチャーパイプラインのデータ変換ロジック**を書く方法に移ります。
As we explained in Chapter 2, feature pipelines are the programs that execute model-independent data transformations to produce reusable features that are stored in the feature store. 
第2章で説明したように、**フィーチャーパイプラインは、フィーチャーストアに保存される再利用可能な特徴を生成するためにモデル非依存のデータ変換を実行するプログラム**です。
That is, the feature data created could be used by potentially many different models—not just the first model you are developing the feature pipeline for. 
つまり、作成されたフィーチャーデータは、フィーチャーパイプラインのために開発している**最初のモデルだけでなく、潜在的に多くの異なるモデルで使用される可能性**があります。
Feature reuse results in higher-quality features through increased usage and testing, reduced storage costs, and reduced feature development and operational costs. 
**フィーチャーの再利用は、使用とテストの増加、ストレージコストの削減、フィーチャー開発および運用コストの削減を通じて、より高品質のフィーチャーをもたらします**。
And remember, the lowest-cost feature pipeline is the one you don’t have to create. 
そして、最もコストのかからないフィーチャーパイプラインは、作成する必要がないものです。

Examples of model-independent transformations (MITs) include the extraction, validation, aggregation, compression (EVAC) transformations: 
**モデル非依存の変換（MIT）の例には、抽出(extraction)、検証(validation)、集約(aggregation)、圧縮(compression)（EVAC）変換**が含まれます。
(モデル非依存変換は、四種類の変換操作に分類できるのか...!:thinking:)

- Feature extraction (lagged features, binning, and chunking for LLMs) 
  - フィーチャー抽出（遅延フィーチャー、ビニング、LLM用のチャンク化）
- Data validation (with Great Expectations) and data cleaning 
  - データ検証（Great Expectationsを使用）およびデータクリーニング
- Aggregation (counts and sums for time windows) 
  - 集約（時間ウィンドウのカウントと合計）
- Compression (vector embeddings) 
  - 圧縮（ベクトル埋め込み）

We will also look at how we can compose transformations in feature pipelines to improve the modularity, testability, and performance of your feature pipelines. 
私たちはまた、フィーチャーパイプライン内で変換を構成して、フィーチャーパイプラインのモジュール性、テスト可能性、およびパフォーマンスを向上させる方法を見ていきます。
However, we will start by setting up our development process—how to organize the source code into packages and what technologies we can use to implement our transformations in feature pipelines. 
ただし、最初に開発プロセスを設定します—ソースコードをパッケージに整理する方法と、フィーチャーパイプラインで変換を実装するために使用できる技術についてです。

<!-- ここまで読んだ -->

## 1.1. Source Code Organization ソースコードの整理

We will use the source code for our credit card fraud project as a template for how to organize source code so that it follows production best practices for developing ML pipelines. 
私たちは、クレジットカード詐欺プロジェクトのソースコードを、MLパイプラインを開発するための生産ベストプラクティスに従うようにソースコードを整理する方法のテンプレートとして使用します。
We need to move beyond just writing notebooks if we are to build production-quality pipelines, and that means following software engineering practices such as test-driven development with continuous integration and continuous deployment (CI/CD). 
**production品質のパイプラインを構築するためには、単にノートブックを書くことを超える必要があり、それはテスト駆動開発や継続的インテグレーションおよび継続的デプロイメント（CI/CD）などのソフトウェア工学のプラクティスに従うことを意味します。**
If you make changes to your source code, tests will give you increased confidence that the changes you made will not break either a pipeline or a client that is dependent on an artifact created by your pipeline—whether that artifact is a feature, a training dataset, a model, or a prediction. 
ソースコードに変更を加えると、テストは、あなたが行った変更がパイプラインや、あなたのパイプラインによって作成されたアーティファクト（フィーチャー、トレーニングデータセット、モデル、または予測）に依存するクライアントを壊さないという自信を高めます。
By automating the execution of the tests, you will not slow down your iteration speed when developing. 
**テストの実行を自動化することで、開発時の反復速度を遅くすることはありません。**
If you have never written a unit test before, don’t worry—LLMs (such as ChatGPT) can help you get started creating unit tests. 
ユニットテストを書いたことがない場合でも心配しないでください—LLM（ChatGPTのような）は、ユニットテストの作成を始めるのに役立ちます。

<!-- ここまで読んだ -->

We use a directory structure that organizes all the source code we need to build, test, and run our entire credit card fraud prediction system (see Figure 6-1). 
私たちは、クレジットカード詐欺予測システム全体を構築、テスト、実行するために必要なすべてのソースコードを整理するディレクトリ構造を使用します（図6-1を参照）。

```bash
credit_card_fraud_project/
├── notebooks/ # EDA, reports, etc.
├── requirements.txt # Global pip dependencies for project
├── project-name # package name
│   ├── pipelines # Feature/training/inference pipelines
│   │   ├── features/ # Features computed in functions
│   └── tests/
│       ├── feature-tests # Unit tests for feature functions
│       └── pipeline-tests # End-to-end tests for pip
└── scripts # Batch scripts: run notebooks and tests
```
_Figure 6-1. For an AI system built with Python, we organize our source code for produc‐_ _tion by placing the different programs, functions, and tests into different directories, sep‐_ _arating production code in the project from EDA in notebooks and helper scripts._ 
_図6-1. Pythonで構築されたAIシステムの場合、異なるプログラム、関数、およびテストを異なるディレクトリに配置することで、プロダクション用のソースコードを整理し、プロジェクト内のプロダクションコードをノートブックやヘルパースクリプトのEDAから分離します。_

<!-- ここまで読んだ -->

The source code for the different FTI pipelines is stored in a pipelines directory. 
異なるFTIパイプラインのソースコードは、pipelinesディレクトリに保存されています。
For easier maintenance, we will store the _tests in separate files in a dedicated directory_ outside of our pipeline programs, as this separates the code for our pipelines from the code for testing. 
メンテナンスを容易にするために、私たちはパイプラインプログラムの外に専用のディレクトリに_テストを別のファイルに保存します_。これにより、パイプラインのコードとテストのコードが分離されます。
We will have two different types of tests: feature tests, which are unit tests for computing features, and pipeline tests, which are end-to-end tests for pipelines. 
私たちは、**特徴を計算するためのユニットテストである特徴テストと、パイプラインのエンドツーエンドテストであるパイプラインテストの2種類のテストを用意**します。
Similarly, it is a good idea to separate the functions used to compute features from the programs that implement the FTI pipelines. 
**同様に、FTIパイプラインを実装するプログラムから特徴を計算するために使用される関数を分離することは良い考え**です。(うんうん。SQL側では生データを取得するようにする場合は、feature functionを単体テストで振る舞い保証しやすいよね...!:thinking:)
We place feature functions in the _features directory. 
私たちは特徴量関数 (feature functions) をfeaturesディレクトリに配置します。
If you follow this code structure, you will be able to iterate_ quickly and not have to later refactor your code for production. 
このコード構造に従えば、迅速に反復作業ができ、後で本番用にコードをリファクタリングする必要がなくなります。

<!-- ここまで読んだ -->

We call this type of project structure a monorepo, as the source code for our entire AI system is in a single source code repository. 
この種のプロジェクト構造をモノレポと呼びます。なぜなら、私たちのAIシステム全体のソースコードが単一のソースコードリポジトリにあるからです。
The advantage of a monorepo over separate repositories for the FTI pipelines is that we don’t have to create and manage installable Python libraries for any shared code between the ML pipelines. 
**FTIパイプラインのための別々のリポジトリに対するモノレポの利点は、MLパイプライン間の共有コードのためにインストール可能なPythonライブラリを作成および管理する必要がないこと**です。
The monorepo also does not hinder creating separate production-quality deployments for the FTI pipelines. 
モノレポは、FTIパイプラインのための別々のproduction-qualityのデプロイを作成することを妨げません。
For example, each ML pipeline can have its own requirements.txt file in its own directory that will be used to build an executable container image for the ML pipeline. 
例えば、各MLパイプラインは、自身のディレクトリに独自のrequirements.txtファイルを持ち、これがMLパイプラインの実行可能なコンテナイメージを構築するために使用されます。

<!-- ここまで読んだ -->

Notice that notebooks is a separate directory. 
notebooksは別のディレクトリであることに注意してください。
It is typically not part of the production code in the project. 
通常、プロジェクトの本番コードの一部ではありません。
It is there to create insights into creating production code—to perform EDA to understand the data and the prediction problem and to communicate those insights to other stakeholders. 
**それは、本番コードを作成するための洞察を生み出すために存在します。データと予測問題を理解するためのEDAを実行し、その洞察を他の利害関係者に伝えるため**です。(うん。notebook自体を書いちゃだめ、って話ではないんだよな...!:thinking:)
That said, on some platforms (like Hopsworks and Databricks), you can run notebooks as jobs, so you can run feature, training, and batch inference pipelines as jobs, if you really want to. 
とはいえ、HopsworksやDatabricksのような一部のプラットフォームでは、ノートブックをジョブとして実行できるため、必要であれば特徴、トレーニング、およびバッチ推論パイプラインをジョブとして実行できます。
The scripts directory is not production code and is there to store utility shell scripts for running tests on pipelines during development. 
scriptsディレクトリは本番コードではなく、**開発中にパイプラインのテストを実行するためのユーティリティシェルスクリプトを保存するために存在**します。(じゃあ本番デプロイ用のスクリプトをここに置くのは微妙なのかな...?:thinking:)

Python library dependencies are needed to containerize ML pipeline programs and are included in the project directory as at least one global requirements.txt file (for all ML pipelines). 
MLパイプラインプログラムをコンテナ化するためにはPythonライブラリの依存関係が必要であり、プロジェクトディレクトリには少なくとも1つのグローバルrequirements.txtファイル（すべてのMLパイプライン用）が含まれています。
Most of you who have had some experience developing in Python will have already opened the gates of pip dependency hell. 
Pythonでの開発経験があるほとんどの方は、すでにpip依存関係の地獄の扉を開いていることでしょう。
It’s part of the rite of passage for Python developers to have some library you never heard of cause your program to fail because of a non-backward-compatible upgrade. 
Python開発者にとって、聞いたことのないライブラリが非後方互換のアップグレードのためにプログラムを失敗させることは、通過儀礼の一部です。
So please, version your Python dependencies. 
ですので、Pythonの依存関係にバージョンを付けてください。

<!-- ここまで読んだ -->

In our credit card fraud project, I included versioned Python library dependencies for each of our three ML pipelines in a single _requirements.txt file. 
私たちのクレジットカード詐欺プロジェクトでは、3つのMLパイプラインそれぞれのバージョン付きPythonライブラリ依存関係を単一の_requirements.txtファイルに含めました。
You can install the_ Python dependencies in your virtual environment by calling: 
あなたは次のコマンドで仮想環境にPython依存関係をインストールすることができます：

```bash
uv pip install -r requirements.txt
```

We are using `uv pip as it is much faster than` `pip. 
**私たちは`uv pip`を使用しています。なぜなら、`pip`よりもはるかに速いからです。**　(そうなのか...!:thinking:)
It is also possible to use a more` [feature-rich dependency management library, such as Poetry. 
より多機能な依存関係管理ライブラリ（Poetryなど）を使用することも可能です。
Poetry is great for large](https://oreil.ly/wHcmd) projects, and it manages the Python virtual environment lifecycle using a _pypro‐_ _ject.toml file. 
Poetryは大規模なプロジェクトに最適で、_pyproject.tomlファイルを使用してPython仮想環境のライフサイクルを管理します。
We will use uv/pip and requirements.txt files, as they have a lower bar‐_ rrier to entry and better integration with platforms that build container images from _requirements.txt files._ 
私たちはuv/pipとrequirements.txtファイルを使用します。なぜなら、これらは参入障壁が低く、requirements.txtファイルからコンテナイメージを構築するプラットフォームとの統合が優れているからです。
(uv pipって初めて聞いたな...!:thinking:)

<!-- ここまで読んだ -->

## 1.2. Feature Pipelines 特徴パイプライン

Feature pipelines read data from some data sources, transform that data to create fea‐ tures, and write their output feature data to the feature store. 
**特徴パイプラインは、いくつかのデータソースからデータを読み込み、そのデータを変換して特徴を作成し、出力された特徴データをフィーチャーストアに書き込みます。**
Before we dive deep into feature engineering, we will look at a number of popular open source data transfor‐ mation engines. 
特徴エンジニアリングに深く入る前に、いくつかの人気のあるオープンソースデータ変換エンジンを見ていきます。
Given a group of features you want to compute together (and write to a feature group), you should understand the trade-offs between using different available engines, based on the expected data volume and the freshness requirements for the features. 
一緒に計算したい(そしてfeature groupに書き込みたい)特徴量のグループを考慮すると、予想されるデータ量と特徴の新鮮さの要件に基づいて、利用可能なさまざまなエンジンを使用することのトレードオフを理解する必要があります。
Most compute engines for feature engineering fall into one of the fol‐ lowing computing paradigms: 
**特徴エンジニアリングのためのほとんどの計算エンジンは、以下の計算パラダイムのいずれかに分類されます。**

- Stream processing for streaming feature pipelines (Python, Java, or SQL) 
  - ストリーミング特徴パイプラインのためのストリーム処理（Python、Java、またはSQL）
- DataFrames for batch feature pipelines (Python) 
  - バッチ特徴パイプラインのためのDataFrames（Python）
- Data warehouses for batch feature pipelines (SQL) 
  - バッチ特徴パイプラインのためのデータウェアハウス（SQL）

There are also other specialist compute engines for feature engineering, including some that leverage GPUs, but due to space considerations, we restrict ourselves to widely adopted open source engines: Pandas, Polars, Apache Spark, Apache Flink, and Feldera (a stream processing engine using SQL). 
特徴エンジニアリングのための他の専門的な計算エンジンもあり、GPUを活用するものもありますが、スペースの都合上、広く採用されているオープンソースエンジン（Pandas、Polars、Apache Spark、Apache Flink、SQLを使用したストリーム処理エンジンであるFeldera）に制限します。
In Figure 6-2, you can see how to select the best data processing frameworks, organized by whether they: 
図6-2では、最適なデータ処理フレームワークを選択する方法を示しています。これは、次のように整理されています。

- Scale to process data that is too big to be processed by a single server (Apache Spark, Apache Flink) 
  - 単一のサーバで処理できないほど大きなデータを処理するためにスケールする（Apache Spark、Apache Flink）
- Are stream processing frameworks (Feldera, Apache Flink, Spark Structured Streaming) 
  - ストリーム処理フレームワークである（Feldera、Apache Flink、Spark Structured Streaming）
- Support real-time computation of feature data in prediction requests (Python UDFs) 
  - 予測リクエストにおける特徴データのリアルタイム計算をサポートする（Python UDF）
- Are batch data transformations (Pandas, Polars, DuckDB, and PySpark)  
  - バッチデータ変換である（Pandas、Polars、DuckDB、PySpark）

![]()
_Figure 6-2. Data transformations in different DataFrame, SQL, and stream processing_ _frameworks have different latency and scalability properties. 
_Figure 6-2. 異なるDataFrame、SQL、およびストリーム処理フレームワークにおけるデータ変換は、異なるレイテンシとスケーラビリティの特性を持っています。
For each feature pipeline,_ _you should select the best framework, given the scale and latency requirements of the_ _features it creates._ 
**各特徴パイプラインに対して、作成する特徴のスケールとレイテンシ要件を考慮して、最適なフレームワークを選択する必要があります。**

<!-- ここまで読んだ -->

For stream processing, Apache Flink and Spark Structured Streaming are widely used as distributed, scalable frameworks. 
ストリーム処理において、Apache FlinkとSpark Structured Streamingは、分散型でスケーラブルなフレームワークとして広く使用されています。
Both, however, have steep learning curves and high operational overhead. 
しかし、どちらも急な学習曲線と高い運用コストがあります。
Feldera is a single-machine stream processing engine with support for incremental computation with SQL and a lower barrier to entry (see Chapter 9). 
Felderaは、SQLによる増分計算をサポートする単一マシンのストリーム処理エンジンであり、参入障壁が低いです（第9章を参照）。

For batch processing with DataFrames, Pandas, Polars, and PySpark are the main frameworks that we will work with in this chapter. 
DataFramesを使用したバッチ処理では、Pandas、Polars、およびPySparkがこの章で扱う主要なフレームワークです。
Batch processing with SQL can be performed in data warehouses (such as Snowflake, BigQuery, Databricks Photon, and Redshift) or on single-host SQL engines (such as DuckDB). 
SQLを使用したバッチ処理は、データウェアハウス（Snowflake、BigQuery、Databricks Photon、Redshiftなど）や単一ホストのSQLエンジン（DuckDBなど）で実行できます。
The dbt framework has become popular for orchestrating feature engineering pipelines as a series of SQL commands. 
dbtフレームワークは、一連のSQLコマンドとして特徴エンジニアリングパイプラインをオーケストレーションするために人気を博しています。
Table 6-1 provides a guide to when you should choose one engine over another.  
表6-1は、**どのエンジンを選択すべきかのガイド**を提供します。

![]()
_Table 6-1. Frameworks for computing features at different data volumes and feature freshness_ _levels_ 
_表6-1. 異なるデータボリュームと特徴の新鮮さレベルで特徴を計算するためのフレームワーク_

- メモ: 表6-1の内容
  - データボリューム=Large, 特徴量の新鮮さ=1-3 secsの場合
    - フレームワーク = Flink (Java)
    - 例: 大規模 recsys のクリックストリーム
  - データボリューム=Small-Medium, 特徴量の新鮮さ=1-3 secsの場合
    - フレームワーク = Feldera (SQL)
    - 例: リアルタイム物流、小規模クリックストリーム処理、サイバーセキュリティイベント
  - データボリューム=Small, 特徴量の新鮮さ=1-3 secsの場合
    - フレームワーク = Python: Pathway and Quix
    - 例: 侵入検知、Industry 4.0、エッジコンピューティング
  - データボリューム=Large, 特徴量の新鮮さ=Mins to hrsの場合
    - フレームワーク = PySpark or dbt/SQL
    - 例: パーソナライズされたマーケティングキャンペーンとセグメンテーション、バッチ詐欺、顧客離脱、クレジットスコアリング、需要予測
  - データボリューム=Large unstructured, 特徴量の新鮮さ=Mins to hrsの場合
    - フレームワーク = PySpark
    - 例: 画像拡張、テキスト処理（例：チャンク化）、ビデオ前処理（PySpark）
  - データボリューム=Small-Medium, 特徴量の新鮮さ=Mins to hrsの場合
    - フレームワーク = Pandas, Polars, and DuckDB
    - 例: APIからのデータ取得のための小規模データボリューム
  - データボリューム=Small-Large, 特徴量の新鮮さ=Mins to hrsの場合
    - フレームワーク = Optionally with GPUs: Pandas, Polars, and PySpark
    - 例: RAGのためのベクトル埋め込みテキストチャンクパイプラインおよびビデオ前処理

<!-- ここまで読んだ! -->

In general, you should choose stream processing if you are building a real-time ML system that needs fresh precomputed features. 
一般的に、リアルタイムMLシステムを構築していて、新鮮な事前計算された特徴が必要な場合は、ストリーム処理を選択すべきです。
If feature freshness is not important, you should probably write a batch feature pipeline, as it will have lower operational costs. 
**特徴の新鮮さが重要でない場合は、バッチ特徴パイプラインを書くべきです。なぜなら、それは運用コストが低くなるから**です。
You should prefer DataFrame compute engines (Pandas/Polars/PySpark) over SQL when: 
次のような場合は、**SQLよりもDataFrame計算エンジン（Pandas/Polars/PySpark）を好むべき**です。(あ、この判断機になる...!:thinking:)

- You need to fetch data from APIs. 
  - APIからデータを取得する必要がある場合。
- Extensive data cleaning is required. 
  - 大規模なデータクリーニングが必要な場合。
- You need to transform unstructured data (images, video, text). 
  - 非構造化データ（画像、ビデオ、テキスト）を変換する必要がある場合。
- You need to use feature engineering libraries that are only available in Python. 
  - Pythonでのみ利用可能な特徴エンジニアリングライブラリを使用する必要がある場合。
- You need to write transformations with custom logic. 
  - カスタムロジックで変換を書く必要がある場合。

You can scale up feature engineering with DataFrames on a single machine by switch‐ ing from Pandas to Polars, which makes better use of available memory and CPUs. 
**PandasからPolarsに切り替えることで、単一のマシン上でDataFramesを使用した特徴エンジニアリングをスケールアップできます。Polarsは利用可能なメモリとCPUをより良く活用します。**
When data volumes are too large for a single machine, you can use PySpark, which can be scaled out over many workers to TB- or PB-sized workloads. 
データボリュームが単一のマシンには大きすぎる場合は、PySparkを使用できます。これは、多くのワーカーにスケールアウトしてTBまたはPBサイズのワークロードを処理できます。

<!-- ここまで読んだ -->

We will now briefly cover SQL for feature engineering. 
次に、特徴エンジニアリングのためのSQLについて簡単に説明します。
You should use SQL over DataFrames when you have a batch feature pipeline, all of the source data is in the data warehouse or lakehouse, and your feature engineering can be implemented in SQL. 
**バッチ特徴パイプラインがあり、すべてのソースデータがデータウェアハウスまたはレイクハウスにあり、特徴エンジニアリングをSQLで実装できる場合は、DataFramesよりもSQLを使用すべき**です。
SQL-based feature engineering is declarative, leveraging the power of relational operations and the scale of data warehouses or query engines on top of lakehouse tables. 
SQLベースの特徴エンジニアリングは宣言的であり、**リレーショナル操作の力とデータウェアハウスやレイクハウステーブルの上にあるクエリエンジンのスケールを活用します。** (SQLで書けるものは書いた方が、基本的にパフォーマンス良さそうってことか...!:thinking:)

For example, in Hopsworks, you can run SQL-based transformations against either an external feature group or a feature group stored in Hopsworks. 
例えば、Hopsworksでは、外部フィーチャーグループまたはHopsworksに保存されたフィーチャーグループに対してSQLベースの変換を実行できます。
For external feature groups, you can write feature pipelines in dbt/SQL directly in the source data warehouse. 
外部フィーチャーグループの場合、ソースデータウェアハウス内で直接dbt/SQLで特徴パイプラインを書くことができます。
These transform the data in the external table directly. 
これにより、外部テーブル内のデータが直接変換されます。
If the external feature group is online-enabled, you need a Python model to your dbt workflow that writes the updated data to the online feature group. 
外部フィーチャーグループがオンライン対応の場合、更新されたデータをオンラインフィーチャーグループに書き込むdbtワークフローにPythonモデルが必要です。
For feature groups in Hopsworks, you can use Spark SQL or DuckDB. 
Hopsworksのフィーチャーグループには、Spark SQLまたはDuckDBを使用できます。
Spark SQL can be used to transform data in Spark DataFrames, and then you write the transformed DataFrame to a feature group in Hopsworks. 
Spark SQLを使用してSpark DataFrames内のデータを変換し、変換されたDataFrameをHopsworksのフィーチャーグループに書き込みます。
For DuckDB, you can perform transformations using SQL in a Python program and pass the final feature data as an Arrow table to a Pandas or Polars Data‐ Frame that is then written to the feature group. 
DuckDBの場合、Pythonプログラム内でSQLを使用して変換を実行し、最終的な特徴データをArrowテーブルとしてPandasまたはPolars DataFrameに渡し、それをフィーチャーグループに書き込みます。

<!-- ここまで読んだ -->

## 1.3. Data Transformations for DataFrames データフレームのデータ変換

Feature engineering with both DataFrames and SQL tables involves performing rowwise and column-wise transformations on the data. 
DataFramesとSQLテーブルの両方を使用した特徴エンジニアリングは、データに対して行単位および列単位の変換を実行することを含みます。
One useful way to understand each data transformation is to study how it transforms the rows and columns in your DataFrame(s) or SQL table(s). 
各データ変換を理解するための有用な方法は、それがDataFrameまたはSQLテーブル内の行と列をどのように変換するかを研究することです。

You need to know what the result of the data transformations will be—will they add or remove columns, reduce the number of rows, or add more rows? 
データ変換の結果がどうなるかを知る必要があります。列を追加または削除するのか、行数を減らすのか、または行を追加するのか？
Figure 6-3 shows the different classes of transformations that can be performed on tabular data. 
図6-3は、表形式データに対して実行できるさまざまな変換のクラスを示しています。
In the discussion that follows, we will restrict ourselves to data transformations on Data‐ Frames 
以下の議論では、DataFramesに対するデータ変換に制限します。
The code snippets are in a mix of PySpark, Pandas, and Polars. 
コードスニペットは、PySpark、Pandas、およびPolarsの混合です。
Similar to Pandas, Polars is a DataFrame engine that runs on a single machine, but it scales to handle much larger data volumes thanks to better memory management and multi‐ core support. 
**Pandasと同様に、Polarsは単一のマシンで動作するDataFrameエンジンですが、より良いメモリ管理とマルチコアサポートのおかげで、はるかに大きなデータボリュームを処理するためにスケール**します。
There are a number of important classes of transformations that we cover: 
私たちが扱う重要な変換のクラスがいくつかあります：

- Expressions (df.with_columns(..)) are available in both Polars and PySpark. 
  - 表現（df.with_columns(..)）は、PolarsとPySparkの両方で利用可能です。
- Pandas user-defined functions (UDFs) are available in PySpark. 
  - Pandasのユーザー定義関数（UDF）は、PySparkで利用可能です。
- Python UDFs (apply) are available in Pandas and Polars. 
  - Python UDF（apply）は、PandasとPolarsで利用可能です。
- filter and join transformations are available in Polars, Pandas, and PySpark. 
  - filterおよびjoin変換は、Polars、Pandas、およびPySparkで利用可能です。
- groupBy (group_by in Polars) and aggregate are available in Polars, Pandas, and PySpark.  
  - groupBy（Polarsではgroup_by）および集約は、Polars、Pandas、およびPySparkで利用可能です。

![]()
_Figure 6-3. Data transformations produce output DataFrames that often do not match_ _the shape of the input DataFrame(s). 
_Figure 6-3. **データ変換は、出力DataFrameが入力DataFrameの形状と一致しないことが多いこと**を示しています。
Some transformations add rows and/or columns, some keep the same number of rows, and some reduce the number of rows and/or columns._ 
いくつかの変換は行や列を追加し、いくつかは同じ数の行を保持し、いくつかは行や列の数を減少させます。

We can classify DataFrame transformations into the following cardinalities: 
**DataFrameの変換を以下のカーディナリティに分類**できます：

- **Row size–preserving transformation (行サイズを保持する変換)**
With this, you add a new column to an existing DataFrame without changing the number of rows. 
これにより、行数を変更せずに既存のDataFrameに新しい列を追加します。
Feature extraction is a typical example of one such data transformation. 
特徴抽出は、そのようなデータ変換の典型的な例です。

- **Row/column size–reducing transformation (行/列サイズを削減する変換)**
With this, the input DataFrame has more rows than the output DataFrame. 
これにより、入力DataFrameの行数は出力DataFrameの行数よりも多くなります。
Examples of such transformations include _group by aggregations,_ _filtering, and_ data compression (vector embeddings and principal component analysis).  
このような変換の例には、_group by集約、_フィルタリング、および_データ圧縮（ベクトル埋め込みおよび主成分分析）が含まれます。

- **Row/column size–increasing transformation (行/列サイズを増加させる変換)**
With this, the input DataFrame has fewer rows than the output DataFrame. 
これにより、入力DataFrameの行数は出力DataFrameの行数よりも少なくなります。
A common example is feature extraction that involves exploding JSON objects, lists, or dicts stored in columns in DataFrames. 
一般的な例は、DataFrameの列に格納されたJSONオブジェクト、リスト、または辞書を展開する特徴抽出です。
Cross-joins also belong here, as do user-defined table functions (in PySpark). 
クロスジョインもここに含まれ、ユーザー定義テーブル関数（PySparkで）も含まれます。

- **Join transformations (結合変換)**
These involve merging together two input DataFrames to produce a single Data‐ Frame (with more columns than either of the input DataFrames). 
これには、2つの入力DataFrameをマージして、1つのDataFrameを生成することが含まれます（入力DataFrameのいずれよりも多くの列を持つ）。
Joins are needed when you have data from different sources and you want to compute fea‐ tures using data from both sources. 
**異なるソースからのデータがあり、両方のソースのデータを使用して特徴を計算したい場合、結合が必要**です。
Joins are sometimes needed to build the final DataFrame that is written to a feature group. 
結合は、特徴グループに書き込まれる最終的なDataFrameを構築するために時々必要です。

<!-- ここまで読んだ! -->

### 1.3.1. Row Size–Preserving Transformations (行サイズを保持する変換)

Here is an example of a row size–preserving transformation, implemented as a Pan‐ das function operating on a Series (column in the DataFrame) that identifies rows that include outliers by setting a Boolean value for is_outlier in a new column in the DataFrame: 
ここに、行サイズを保持する変換の例があります。これは、DataFrameの列であるSeriesに対して動作するPandas関数として実装されており、DataFrameの新しい列でis_outlierのブール値を設定することによって外れ値を含む行を特定します：

```python
def detect_outliers(value_series: pd.Series) -> pd.Series: 
  """Add a column that indicates whether the row is an outlier""" 
  mean = value_series.mean() 
  std_dev = value_series.std() 
  z_scores = (value_series - mean) / std_dev 
  return np.abs(z_scores) > 3   
df["is_outlier"] = detect_outliers(df["value"])
``` 

We may compose this transformation in Pandas with a row-reducing transformation that removes the rows that are considered outliers: 
この変換をPandasで、外れ値と見なされる行を削除する行削減変換と組み合わせることができます：

```python
def remove_outliers(df: pd.DataFrame) -> pd.DataFrame: 
  """Remove the rows in the DataFrame where is_outlier is True""" 
  return df[df["is_outlier"] == False]   
df_filtered = remove_outliers(df)
``` 

Other examples of row size–preserving data transformations include: 
行サイズを保持するデータ変換の他の例には、以下が含まれます：

- Applying a UDF as a lambda function in Polars (or an apply in Pandas, or a Pan‐ das UDF in PySpark). 
PolarsでUDFをラムダ関数として適用すること（またはPandasでapply、またはPySparkでPandas UDF）。
This Polars code that stores the squared value of a column in `new_col applies the lambda function to` `col1 using the` `map_elements func‐` tion. 
このPolarsコードは、`new_col`に列の平方値を格納し、`map_elements`関数を使用して`col1`にラムダ関数を適用しす。
Note that map_elements executes Python functions row by row and is not vectorized: 
**map_elementsはPython関数を行ごとに実行し、ベクトル化されていないことに注意**してください：

```python
df = df.with_columns(       
  pl.col("col1").map_elements(lambda x: x * 2).alias("new_col")     
)
```

- A rolling window expression in Polars that computes the mean amount spent on a credit card for the previous three days: 
過去3日間のクレジットカードでの支出の平均額を計算するPolarsのローリングウィンドウ式：

```python
df.with_columns(       
  (col("amount").rolling_mean(3).over("cc_num")).alias("rolling_avg")     
)
```

- Conditional transformations (when, `then,` `otherwise,` `select). 
条件付き変換（when、`then`、`otherwise`、`select）。
Here, if` `col is 0,` then set new_col to positive. 
ここでは、`col`が0の場合、`new_col`をpositiveに設定します。
If not, then set it to non_positive: 
そうでない場合は、non_positiveに設定します：

```
     df.with_columns(       
       (pl.when(df["col"]==0)       
       .then("positive").otherwise("non_positive"))       
       .alias("new_col")     
     )
```

- Temporal transformations that capture time-related information about the data. 
データに関する時間関連情報をキャプチャする時間的変換。
Here, we compute the number of days since the bank’s credit rating was last changed: 
ここでは、銀行の信用評価が最後に変更されてからの日数を計算します：

```python    
df.with_columns(       
  (pl.lit(datetime.now()) - pl.col("last_modified"))       
  .dt.total_days()       
  .alias("days_since_bank_cr_changed")     
)
```  

- Sorting and ranking. 
ソートとランキング。
This code computes in rank_col the rank of each value in `col: 
このコードは、`col`の各値のランクをrank_colに計算します：

```python
df.with_columns(pl.col("col").rank().alias("rank_col"))
```  

- Mathematical transformations. 
数学的変換。
Here, we store the sum of `col1 and` `col2 in` `sum_col: 
ここでは、`col1`と`col2`の合計を`sum_col`に格納します：

```     
df.with_columns((pl.col("col1") + pl.col("col2")).alias("sum_col"))
```  

- String transformations. 
文字列変換。
This transformation uppercases the string in `name and` stores it in uppercase_name: 
この変換は、`name`の文字列を大文字にし、`uppercase_name`に格納します：

``` 
df.with_columns(uppercase_name = pl.col("name").str.to_uppercase())
```  

- Lag and lead. 
ラグとリード。
This code stores yesterday’s pm25 value in lagged_pm25: 
このコードは、昨日のpm25値を`lagged_pm25`に格納します：

```     
df.with_columns(lagged_pm25 = pl.col("pm25").shift(1))
```  

<!-- ここまで読んだ! -->

### 1.3.2. Row and Column Size–Reducing Transformations (行および列サイズを削減する変換)

_Aggregations are examples of a well-known data transformation that reduces the_ 
_ number of rows from the input DataFrame (or table). 
集約は、入力DataFrame（またはテーブル）から行数を減少させるよく知られたデータ変換の例です。
Aggregations summarize data over a column and optionally an additional time window (a time range of data), cap‐ turing trends or temporal patterns. 
**集約は、列にわたってデータを要約し、オプションで追加の時間ウィンドウ（データの時間範囲）を指定し、トレンドや時間的パターンを捉えます。**
Aggregations are useful in AI systems with sparse data and temporal patterns, such as fraud detection, recommendation engines, and predictive maintenance applications. 
**集約は、詐欺検出、推薦エンジン、予測保守アプリケーションなど、スパースデータと時間的パターンを持つAIシステムで有用**です。(参考になりそう...!:thinking:)

<!-- ここまで読んだ! -->

Aggregations are functions that summarize a window of data. 
集約は、データのウィンドウを要約する関数です。
The data could include all of the input data or a time window, which is a period over which the aggregation is performed. 
データには、すべての入力データまたは集約が行われる期間である時間ウィンドウが含まれる場合があります。
Common aggregation functions include: 
一般的な集約関数には以下が含まれます：

- _Count_ Number of events 
  _Count_ イベントの数

- _Sum_ Total value (e.g., total transaction amount) 
  _Sum_ 合計値（例：総取引額）

- _Mean/median_ Average value 
  _Mean/median_ 平均値

- _Max/min_ Extreme values 
  _Max/min_ 極端な値

- _Standard deviation/variance_ Measure of variability 
  _Standard deviation/variance_ 変動性の測定

- _Percentiles_ Specific thresholds, such as the 90th percentile 
  _Percentiles_ 特定の閾値（例：90パーセンタイル）

Aggregations are computed for entities, for example: 
**集約は、例えば以下のエンティティに対して計算**されます：
(うん。色んな粒度で集約できるよね...!:thinking:)

- Per credit card 
  - クレジットカードごと
- Per customer 
  - 顧客ごと
- Per merchant/bank 
  - 商人/銀行ごと
- Per product/item 
  - 製品/アイテムごと

<!-- ここまで読んだ! -->

In SQL and PySpark you use `group_by and a` _window. 
SQLやPySparkでは、`group_by`と`window`を使用します。(確かに、集約関数の適用は、基本的に group by関数かwindow関数を使うことになるのか...!:thinking:)
Polars supports grouping by_ time windows through the `groupby_rolling and` `groupby_dynamic methods and` then applying aggregations.
**Polarsは、`groupby_rolling`および`groupby_dynamic`メソッドを通じて時間ウィンドウによるグルーピングをサポートし、その後集約を適用します。**
Pandas supports time-based grouping through resample and rolling, which can be combined with aggregation functions. 
Pandasは、リサンプリングとロールを通じて時間ベースのグルーピングをサポートしており、集約関数と組み合わせることができます。
Here is an example aggregation in Polars without a time window that handles missing data by filling missing values with the forward fill strategy (replacing null values with the last valid nonnull value that appeared earlier in the data), before grouping and summing the amount: 
以下は、時間ウィンドウなしでのPolarsにおける集約の例で、欠損データを前方埋め戦略（null値をデータ内で以前に出現した最後の有効な非null値で置き換える）で処理し、グルーピングと合計を行う前のものです：

```Python 
filled_df = (df.with_columns(pl.col("amount").fill_null(strategy="forward"))          
.group_by("cc_num", maintain_order=True)          
.agg([            
pl.col("event_time"),            
pl.col("amount").sum().alias("total_amount")          
])          
.explode(["event_time"]))
```

<!-- ここまで読んだ! -->

In the previous code snippet, the output DataFrame, filled_df, includes the event_time column from df and adds the new total_amount column containing the result of the aggregation. All other columns from df were not retained, as aggrega‐ tions typically reduce the number of columns. For example, if you are computing the sum of the transactions for a credit card number, it is not meaningful to retain the category column in that transformation. If you want to compute an aggregate for the category column, you perform a separate transformation on that column.
前のコードスニペットでは、出力DataFrameであるfilled_dfにはdfからのevent_time列が含まれ、集約の結果を含む新しいtotal_amount列が追加されます。dfの他のすべての列は保持されません。なぜなら、集約は通常、列数を減少させるからです。例えば、クレジットカード番号の取引の合計を計算している場合、その変換でcategory列を保持することは意味がありません。category列の集約を計算したい場合は、その列に対して別の変換を実行します。

<!-- ここまで読んだ! -->

Aggregations support different types of time windows, some of which are row-size reducing and some of which are not. 
集約は異なるタイプの時間ウィンドウをサポートしており、その中には行サイズを減少させるものとそうでないものがあります。
Rolling window aggregations compute an out‐ 
ロールウィンドウ集約は、出力を計算します。
put for every row in the source DataFrame and are therefore not row-size reducing. 
ソースDataFrameのすべての行に対して出力を計算し、したがって行サイズを減少させません。
In contrast, tumbling windows compute an output for all events in a window length, so they typically reduce the number of rows. 
対照的に、タンブリングウィンドウはウィンドウの長さ内のすべてのイベントに対して出力を計算するため、通常は行数を減少させます。
For example, if your window length is one week and there are, on average, 20 transactions per week, you will reduce the number of rows, on average, by a factor of 20. 
例えば、ウィンドウの長さが1週間で、平均して週に20件の取引がある場合、平均して行数を20倍に減少させます。

Sometimes aggregations require composing transformations. 
時には、集約が変換の構成を必要とします。
For example, suppose we want to compute the following: “Find the maximum amount for each cc_num that has two or more transactions from the same category.” 
例えば、次の計算を行いたいとします：「同じカテゴリから2件以上の取引がある各`cc_num`の最大金額を見つける。」
First, we need to group by ``` cc_num, then we have to remove those transactions that have only one entry for a 
まず、`cc_num`でグループ化し、次に特定のカテゴリに対して1件のみの取引を持つものを削除する必要があります。
given category, and then for each remaining category (with >1 transaction), we have to find the maximum amount. 
特定のカテゴリに対して、残りのカテゴリ（取引が1件以上）ごとに最大金額を見つける必要があります。
This may seem like a complex example, but it is not uncommon when you need to find specific signals in the data that are predictive for your problem at hand. 
これは複雑な例に思えるかもしれませんが、手元の問題に対して予測的な特定の信号をデータ内で見つける必要がある場合は珍しくありません。
Polars lets us elegantly and efficiently compose `group_by` aggregations and expressions: 
Polarsは、`group_by`集約と式を優雅かつ効率的に構成することを可能にします：

```Python
df3 = df.group_by("cc_num").agg(     
    # 1つより多いトランザクションを持つカテゴリのamountの最大値を見つける
    pl.col("amount").filter(pl.col("category").count() > 1).max()   
)
```

<!-- ここまで読んだ! -->

Vector embeddings are another data transformation type that compresses input data into a smaller number of rows and columns. 
**ベクトル埋め込みは、入力データをより少ない行と列に圧縮する別のデータ変換タイプ**です。
(ex. Two-towerモデルは、複数の列を受け取って固定長のベクトルに圧縮するタイプのデータ変換とみなせるかな...!:thinking:)
You create a vector embedding from some high-dimensional input data (rows and columns) by passing it through an _embedding model that then outputs a vector. 
高次元の入力データ（行と列）からベクトル埋め込みを作成するには、_embedding modelを通して渡し、その後ベクトルを出力します。
The vector is a fixed-sized array (its_ length is known as its _dimension) containing (normally 32-bit) floating-point num‐_ bers. 
**ベクトルは固定サイズの配列で（その長さは次元として知られています）**、通常は32ビットの浮動小数点数を含みます。
The embedding model is a deep learning model, so if you are transforming a large volume of data into vector embeddings, you may be able to speed up the process considerably by performing the data transformations on GPUs rather than CPUs. 
埋め込みモデルは深層学習モデルであるため、大量のデータをベクトル埋め込みに変換する場合、CPUではなくGPUでデータ変換を行うことでプロセスを大幅に加速できる可能性があります。
In the following example code, we encode the explanation string for a fraudulent credit card transaction with the SentenceTransformer embedding model: 
以下の例のコードでは、SentenceTransformer埋め込みモデルを使用して不正なクレジットカード取引の説明文字列をエンコードします：

```Python  
from sentence_transformers import SentenceTransformer   
model = SentenceTransformer('all-MiniLM-L6-v2')   
embeddings = model.encode(df["explanation"].to_list())   
df = df.with_columns(embedding_explanation=pl.lit(embeddings))
```

If you write this vector embedding to a vector database (or a feature group in Hops‐ works), you can then search for records with similar explanation strings using _k-nearest neighbors (kNN) search. 
このベクトル埋め込みをベクトルデータベース（またはHopsworksのフィーチャーグループ）に書き込むと、_k-nearest neighbors (kNN) searchを使用して、類似の説明文字列を持つレコードを検索できます。
kNN search is a probabilistic algorithm that returns_ _k records containing vector embeddings that are semantically close to the provided_ vector embedding. 
kNN検索は、提供されたベクトル埋め込みに意味的に近いベクトル埋め込みを含む_k件のレコードを返す確率的アルゴリズムです。
The size of k can range from a few to a few hundred records. 
kのサイズは、数件から数百件のレコードまでの範囲になります。

<!-- ここまで読んだ! -->

### 1.3.3. Row/Column Size–Increasing Transformations 　(行/列サイズを増加させる変換)

It is becoming more common to store JSON objects in columns in tables. 
**テーブルの列にJSONオブジェクトを保存することが一般的になりつつあります。**
To create features from values in the JSON object, you may need to first extract the values in the JSON object as new columns and/or new rows. 
JSONオブジェクトの値から特徴を作成するには、まずJSONオブジェクト内の値を新しい列および/または新しい行として抽出する必要があります。
You can do this by exploding the column containing the JSON object. 
これは、JSONオブジェクトを含む列を爆発させることで行うことができます。
In Polars, this involves calling unnest to explode the struct into separate columns: 
Polarsでは、unnestを呼び出して**構造体(struct)を別々の列に展開すること**が含まれます：

```Python
df = pl.DataFrame({     
    "json_col": [       
    {"name": "Alice", "age": 25, "city": "Palo Alto"},       
    {"name": "Bob", "age": 30, "city": "Dublin"},     
]})   
df_exploded = df.unnest("json_col")
```

If you have JSON objects in a column, in Polars, you can define them first as a struct and then `unnest the column to explode details into separate columns. 
列にJSONオブジェクトがある場合、Polarsでは、最初にそれらを構造体として定義し、その後`unnest`を使用して詳細を別々の列に爆発させることができます。
At the end, `df_exploded contains the columns ["name", "age", "city"]. 
最終的に、`df_exploded`には["name", "age", "city"]の列が含まれます。

In PySpark, user-defined table functions (UDTFs) are functions that transform a sin‐ 
PySparkでは、ユーザー定義テーブル関数（UDTF）は、単一の入力行を複数の出力行に変換する関数です。
gle input row into multiple output rows. 
単一の入力行を複数の出力行に変換します。
In contrast, UDFs work on a row-to-row basis. 
対照的に、UDFは行対行で動作します。
UDTFs can, for example, explode a JSON structure in a column to multiple rows based on deeply nested fields. 
UDTFは、例えば、深くネストされたフィールドに基づいて列内のJSON構造を複数の行に爆発させることができます。
UDTFs are not available in Polars or Pandas. 
UDTFはPolarsやPandasでは利用できません。
UDTFs execute in parallel across Spark tasks. 
UDTFはSparkタスク全体で並行して実行されます。
PySpark has supported custom UDTFs since Spark 3.5. 
PySparkはSpark 3.5以降、カスタムUDTFをサポートしています。
As of Spark 4.0, UDTFs support both vectorized execution via Apache Arrow (for higher performance) and polymorphic schemas (where the out‐ 
Spark 4.0以降、UDTFはApache Arrowを介したベクトル化実行（より高いパフォーマンスのため）と多相スキーマをサポートしています。
put schema can depend on input parameters). 
出力スキーマは入力パラメータに依存する場合があります）。
For maximum performance, custom UDTFs can be written in Java/Scala Spark. 
最大のパフォーマンスを得るために、カスタムUDTFはJava/Scala Sparkで記述できます。

Exploding JSON objects is not the only row size–increasing data transformation. 
JSONオブジェクトを展開することは、行サイズを増加させるデータ変換の唯一の方法ではありません。
Imagine we want to create a feature for the total spending of each customer per transaction category. 
**各取引カテゴリごとの各顧客の総支出の特徴量を作成したい**と想像してください。
(ニュースアプリでも、各ユーザの、各カテゴリごとの直近半年の記事閲覧数とか、記事滞在時間とか、そういう特徴量を作りたいことは多そう...!:thinking:)
However, transactions are organized by cc_num (entity ID), so we need to pivot the DataFrame to transform columns into rows and compute a ``` spend_category column: 
しかし、取引はcc_num（エンティティID）によって整理されているため、DataFrameをピボットして列を行に変換し、spend_category列を計算する必要があります：

```Python
# 各cc_num(=顧客id的なやつ)ごとに「カテゴリ別の支出」という特徴量を作成したい
pivot = (     
  # cc_numとcategoryでグループ化
  df.group_by(["cc_num", "category"])
    # 支出額の合計を計算
    .agg(pl.col("amount").sum())     
    # category列を行に変換
    .pivot(on="category", values="amount", index="cc_num")
    # null値を0で埋める
    .fill_null(0)   
)

# 各カラムがspend_<category_name>になるようにリネーム
pivot = pivot.rename(     
{col: f"spend_{col}" for col in pivot.columns if col != "cc_num"}   
)
```

Similarly, we also unpivot columns into rows using unpivot: 
同様に、unpivotを使用して列を行に戻すこともできます：

```Python  
dv_unpivot = df.unpivot(index=["cc_num"], on=["category"])
```

<!-- ここまで読んだ! -->

### 1.3.4. Join Transformations 

A common requirement when selecting features for a model is to include features that “belong” to different entities. 
モデルの特徴を選択する際の一般的な要件は、「異なるエンティティに属する」特徴を含めることです。
For example, say that you could have features in different feature groups with different entity IDs (e.g., cc_num, account_id), but you would like to use features from both feature groups in your model. 
例えば、異なるエンティティID（例：cc_num、account_id）を持つ異なるフィーチャーグループに特徴がある場合、両方のフィーチャーグループから特徴をモデルで使用したいとします。

In this case, you’ll often need to join two or more DataFrames together using a common join key. 
この場合、共通の結合キーを使用して2つ以上のDataFrameを結合する必要があります。

The following is an example of joining two DataFrames together in Polars. 
以下は、Polarsで2つのDataFrameを結合する例です。

Note that Pandas uses the merge method instead of join for this operation (PySpark uses join): 
Pandasはこの操作に対してjoinの代わりにmergeメソッドを使用することに注意してください（PySparkはjoinを使用します）：

```  
merged_df = transaction_df.join(account_df, on="cc_num", how="inner")
```

Here, we perform an inner join, which will take every row in transaction_df and look for a matching cc_num in account_df. 
ここでは、inner joinを実行し、transaction_dfのすべての行を取得し、account_dfで一致するcc_numを探します。

It will skip rows in transaction_df that do not have a matching cc_num in account_df. 
account_dfに一致するcc_numがないtransaction_dfの行はスキップされます。

But what if there is no account information for a transaction and we still would like to include the transaction (as we can infer reason‐ 
しかし、取引に対するアカウント情報がない場合、取引を含めたい場合（合理的な値をトレーニングや推論中に推測できるため）、どうすればよいでしょうか？

able values for the account during training or inference)? 
アカウントの合理的な値をトレーニングや推論中に推測できる場合はどうすればよいでしょうか？

In that case, we can change the policy to a left (outer) join, with how="left". 
その場合、ポリシーを左（外部）結合に変更し、how="left"とします。

INNER JOIN and LEFT JOIN are the most widely used joins for feature engineering. 
INNER JOINとLEFT JOINは、特徴エンジニアリングで最も広く使用される結合です。

Note that a LEFT (OUTER) JOIN will be a row size–preserving transformation for the left-hand DataFrame in the join opera‐ 
LEFT（OUTER）JOINは、結合操作における左側のDataFrameに対して行サイズを保持する変換になります。

tion, but an `INNER JOIN will be either a row size–preserving or row size–reducing` transformation, depending on whether there are matching rows in the right-hand DataFrame for all rows in the left-hand DataFrame (preserving) or not (reducing). 
しかし、`INNER JOIN`は、左側のDataFrameのすべての行に対して右側のDataFrameに一致する行があるかどうかに応じて、行サイズを保持するか行サイズを減少させる変換になります（保持する場合）またはそうでない場合（減少する場合）。

###### 1.3.4.0.0.1. DAG of Feature Functions 
###### 1.3.4.0.0.2. 特徴関数のDAG

In Chapter 2, we argued that feature logic (transformations) should be factored into feature functions to improve code modularity and make transformations unittestable. 
第2章では、特徴ロジック（変換）は特徴関数に分割されるべきであり、コードのモジュール性を向上させ、変換をユニットテスト可能にするべきだと主張しました。

A feature pipeline is a series of well-defined steps that transform source data into features that are written in the feature store: 
フィーチャーパイプラインは、ソースデータをフィーチャーストアに書き込まれる特徴に変換する一連の明確に定義されたステップです：

1. Read data from one or more data sources into one or more DataFrames. 
1. 1つ以上のデータソースから1つ以上のDataFrameにデータを読み込みます。

2. Apply feature functions to transform data into features and to join features together. 
2. 特徴関数を適用してデータを特徴に変換し、特徴を結合します。

3. Write a DataFrame containing featurized data to the corresponding feature group.  
3. 特徴化されたデータを含むDataFrameを対応するフィーチャーグループに書き込みます。

You should parametrize the feature pipeline by its data input so that you can run the feature pipeline either with historical data or with new incremental data. 
フィーチャーパイプラインは、そのデータ入力によってパラメータ化するべきであり、そうすることで、フィーチャーパイプラインを過去のデータまたは新しい増分データのいずれかで実行できるようにします。

Assuming your data source supports data skipping, you should only select the columns you need and filter out the rows you don’t need. 
データソースがデータスキップをサポートしていると仮定すると、必要な列のみを選択し、必要のない行をフィルタリングするべきです。

If you work with small data, you may be able to get away with reading all the data from your data source into a DataFrame and then dropping the extra columns and filtering out the data you don’t need. 
小さなデータを扱う場合、データソースからすべてのデータをDataFrameに読み込み、その後余分な列を削除し、必要のないデータをフィルタリングすることで済むかもしれません。



. However, with large data volumes, this is not possible, and you’ll need to push down your selec‐ tions and filters to the data source.
しかし、大量のデータがある場合、これは不可能であり、選択やフィルタをデータソースにプッシュダウンする必要があります。

Once you have read your source data into DataFrame(s), the feature pipeline organi‐ zes the feature functions in a dataflow graph. 
ソースデータをDataFrameに読み込むと、フィーチャーパイプラインはフィーチャー関数をデータフローグラフに整理します。

A dataflow graph is a directed acyclic graph (DAG) that has inputs (data sources), nodes (DataFrames), edges (feature func‐ tions), and outputs (feature groups). 
データフローグラフは、入力（データソース）、ノード（DataFrame）、エッジ（フィーチャー関数）、および出力（フィーチャーグループ）を持つ有向非巡回グラフ（DAG）です。

Figure 6-4 shows three different feature func‐ tions—g(), h(), and j()—in which df is read from the data source and g() is applied to df to produce df1. 
図6-4は、データソースからdfが読み込まれ、g()がdfに適用されてdf1が生成される3つの異なるフィーチャー関数—g()、h()、j()—を示しています。

Then, h() and j() are applied to (potentially different) columns in df1 in parallel, producing dfM and dfN, respectively. 
次に、h()とj()がdf1の（異なる可能性のある）列に並行して適用され、それぞれdfMとdfNが生成されます。

(Note that PySpark and Polars support parallel executions, while Pandas does not.)
（PySparkとPolarsは並行実行をサポートしていますが、Pandasはサポートしていません。）

_Figure 6-4. A feature pipeline reads new data or backfill data into a DataFrame (df)_
_図6-4. フィーチャーパイプラインは新しいデータまたはバックフィルデータをDataFrame（df）に読み込み、_

_and then applies a DAG of data transformations on df using feature functions f, g, h,_ 
_そして、dfに対してフィーチャー関数f、g、hを使用してデータ変換のDAGを適用します。_

_and j. The output of each feature function g, h, and j is a DataFrame that is written to_ 
_各フィーチャー関数g、h、jの出力は、_

_feature group 1, M, and N, respectively._ 
それぞれフィーチャーグループ1、M、Nに書き込まれるDataFrameです。

The graph structure inherently represents dependencies among the transformations, as one featurized DataFrame can be the input to another. 
グラフ構造は、変換間の依存関係を本質的に表現しており、1つのフィーチャー化されたDataFrameが別のDataFrameの入力となることができます。

When the output of one transformation is used as the input to another transformation, we say that the data transformations have been composed, as presented in Chapter 4. 
1つの変換の出力が別の変換の入力として使用されるとき、データ変換が合成されたと言います（第4章で説明されています）。

Both intermediate and leaf nodes in the DAG can write DataFrames to feature groups. 
DAGの中間ノードと葉ノードの両方がDataFrameをフィーチャーグループに書き込むことができます。

Here, df1 is writ‐ ten to feature group 1, dfM is written to feature group M, and dfN is written to feature group N. 
ここでは、df1がフィーチャーグループ1に書き込まれ、dfMがフィーチャーグループMに、dfNがフィーチャーグループNに書き込まれます。

###### 1.3.4.0.0.3. Lazy DataFrames
###### 1.3.4.0.0.4. レイジーDataFrames

Pandas supports _eager evaluation of operations on DataFrames. 
PandasはDataFrameに対する操作の_即時評価をサポートしています。

Each command is_ processed right away, and in a Jupyter notebook, you can view the result of the opera‐ tion directly after it has been executed. 
各コマンドはすぐに処理され、Jupyterノートブックでは、操作が実行された直後にその結果を直接見ることができます。

This is a powerful approach for learning to write data transformations in Pandas. 
これは、Pandasでデータ変換を書くことを学ぶための強力なアプローチです。

In contrast, DataFrame frameworks that sup‐ port lazy evaluation, such as Polars and PySpark, can wait across multiple steps before the commands are executed. 
対照的に、PolarsやPySparkのようにレイジー評価をサポートするDataFrameフレームワークは、コマンドが実行される前に複数のステップで待機することができます。

Waiting provides the possibility to optimize the execu‐ tion of the steps. 
待機することで、ステップの実行を最適化する可能性が提供されます。

But how long do you wait before executing? 
しかし、実行する前にどれくらい待つべきでしょうか？

Lazy DataFrames are like a quantum state, in which the act of observing gives you the result. 
レイジーDataFramesは量子状態のようなもので、観察する行為が結果をもたらします。

With Lazy DataFrames, an action (reading the contents of a DataFrame or writing it to external storage) triggers the execution of the transformations on it. 
レイジーDataFramesでは、アクション（DataFrameの内容を読み取ることや外部ストレージに書き込むこと）が、その上での変換の実行をトリガーします。

While eager evaluation is great for beginners, it is not great for performance. 
即時評価は初心者には素晴らしいですが、パフォーマンスには向いていません。

As data volumes inexorably increase, you should learn to work with Lazy DataFrames. 
データ量が避けられないほど増加するにつれて、レイジーDataFramesを使いこなすことを学ぶべきです。

Both Polars and PySpark are built around Lazy DataFrames. 
PolarsとPySparkの両方は、レイジーDataFramesを中心に構築されています。

The following code snippet in Polars creates a Lazy DataFrame from a CSV file, com‐ putes the `mean value of the` `amount column, and then computes the` `devia` 
以下のPolarsのコードスニペットは、CSVファイルからレイジーDataFrameを作成し、`amount`列の`平均値を計算し、次に` `devia`を計算します。

``` 
tion_from_mean by subtracting the mean from the amount. This is a useful feature in 
平均からamountを引くことによって`devia`を計算します。これは、クレジットカード詐欺を検出するのに役立つ機能です。

detecting credit card fraud. However, all of these steps are only executed when the code reaches the last line—where there is an action, collect(), to read its contents: 
ただし、これらのすべてのステップは、コードが最後の行に達したとき、つまり内容を読み取るアクションであるcollect()があるときにのみ実行されます：

```   
# 2. Lazy loading with pl.scan_csv   
# 3. pl.scan_csvを使用したレイジーローディング   
lazy_df = pl.scan_csv("transactions.csv")   
lazy_df = lazy_df.with_columns([     
    (pl.col("amount") - pl.col("amount").mean()).alias("deviation_from_mean")   
])   
result = lazy_df.collect() 
# 4. 平均からの偏差のための新しい列を作成し、平均を計算します。   
# 5. 実行をトリガーし、結果を収集します   
```

###### Vectorized Compute, Multicore, and Arrow
###### ベクトル化計算、マルチコア、およびArrow

For performance reasons, we avoid writing data transformation code using Data‐ Frames and native Python language features such as `for/while loops, list compre‐` 
パフォーマンスの理由から、DataFrameや`for/whileループ、リスト内包表記、`のようなネイティブPython言語機能を使用してデータ変換コードを書くことを避けます。

hensions, and map/reduce functions. 
hensions、およびmap/reduce関数を使用します。

The code examples we have introduced thus far are based on idioms such as `with_columns(...) and Pandas UDFs. 
これまでに紹介したコード例は、`with_columns(...)やPandas UDFs`のようなイディオムに基づいています。

DataFrame transformations that follow these idioms are executed by a vectorized compute engine and not executed in native Python code. 
これらのイディオムに従ったDataFrameの変換は、ベクトル化計算エンジンによって実行され、ネイティブPythonコードでは実行されません。

They are orders of magnitude faster
それらは桁違いに速いです。



than native Python code for two main reasons. 
ネイティブPythonコードよりも2つの主な理由で遅くなります。

First, Python’s standard execution model is interpreted bytecode that lacks native vectorization. 
第一に、Pythonの標準実行モデルは、ネイティブベクトル化を欠いた解釈されたバイトコードです。

Second, Python programs are constrained by the Global Interpreter Lock, which prevents efficient scalability on multiple CPU cores. 
第二に、Pythonプログラムはグローバルインタプリタロックによって制約されており、複数のCPUコアでの効率的なスケーラビリティを妨げます。

A vectorized compute engine performs operations on large arrays or data structures by applying single instructions to multiple data points simultaneously. 
ベクトル化された計算エンジンは、単一の命令を複数のデータポイントに同時に適用することによって、大きな配列やデータ構造に対して操作を実行します。

This process is called _single instruction, multiple data (SIMD). 
このプロセスは「単一命令・複数データ（SIMD）」と呼ばれます。

These operations can also be parallelized across multiple CPU cores to further improve scalability. 
これらの操作は、さらにスケーラビリティを向上させるために、複数のCPUコアにわたって並列化することもできます。

Pandas, Polars, and PySpark all have vectorized compute engines. 
Pandas、Polars、およびPySparkはすべて、ベクトル化された計算エンジンを持っています。

Polars and PySpark both have good multicore support, while Pandas 2.x with PyArrow backend has some multicore support. 
PolarsとPySparkはどちらも優れたマルチコアサポートを持っていますが、Pandas 2.xはPyArrowバックエンドを使用することで一部のマルチコアサポートを提供しています。

You should write your data transformations so that they are executed in the vectorized compute engine rather than run in Python as interpreted bytecode (see Figure 6-5). 
データ変換は、Pythonで解釈されたバイトコードとして実行されるのではなく、ベクトル化された計算エンジンで実行されるように記述するべきです（図6-5を参照）。

A trivial example would be writing a for loop to process a Pandas DataFrame. 
単純な例としては、Pandas DataFrameを処理するためにforループを書くことが挙げられます。

Please, don’t do this. 
これをしないでください。

A more common performance bottleneck in Pandas is a Python UDF that you apply to a DataFrame. 
Pandasにおけるより一般的なパフォーマンスのボトルネックは、DataFrameに適用するPython UDFです。

This will involve the data being copied from the backing store (which is Arrow-supported in Pandas v2) into Python objects, where the UDF is executed and then converted back to Arrow format. 
これは、データがバックストア（Pandas v2でArrowに対応）からPythonオブジェクトにコピーされ、そこでUDFが実行され、その後Arrow形式に戻されることを含みます。

_Figure 6-5. Native Python transformations are much slower than native vectorized transformations. 
図6-5. ネイティブPython変換は、ネイティブベクトル化変換よりもはるかに遅いです。

Pandas and PySpark support Arrow transformations with Pandas UDFs. 
PandasとPySparkは、Pandas UDFを使用したArrow変換をサポートしています。

Polars and DuckDB also natively process Arrow data. 
PolarsとDuckDBもArrowデータをネイティブに処理します。

Arrow enables zero-copy data transfers between compute engines._ 
Arrowは、計算エンジン間でのゼロコピーデータ転送を可能にします。

For example, the following Python UDF, executed with `apply in Pandas, takes 7.35 seconds on my laptop (Windows Subsystem for Linux, 32 GB RAM, 8 CPUs): 
例えば、次のPython UDFは、Pandasで`apply`を使用して実行すると、私のノートパソコン（Windows Subsystem for Linux、32 GB RAM、8 CPU）で7.35秒かかります：

```  
   num_rows = 10_000_000   
   df = pd.DataFrame({ 'value': np.random.rand(num_rows) * 100})   
   def python_udf(val: float) -> float:     
       return val * 1.1 + math.sin(val)   
   df['apply_result'] = df['value'].apply(python_udf)
``` 
```
Pandas 2.x supports either NumPy or Arrow as a backing vectorized compute engine. 
Pandas 2.xは、NumPyまたはArrowをバックエンドのベクトル化計算エンジンとしてサポートしています。

If I rewrite the same UDF as a native UDF with NumPy, it completes in only 0.28 seconds: 
同じUDFをNumPyを使用したネイティブUDFとして書き直すと、わずか0.28秒で完了します：

```  
   import numpy as np   
   def numpy_udf(series: pd.Series) -> pd.Series:     
       return series * 1.1 + np.sin(series)   
   df['pandas_udf_result'] = numpy_udf(df['value'])
``` 
```
I can also rewrite the same code as an expression in Polars, and it will have roughly the same execution time as the vectorized UDF in Pandas: 
同じコードをPolarsの式として書き直すこともでき、Pandasのベクトル化UDFとほぼ同じ実行時間になります：

```  
   import polars as pl   
   df_polars = pl.DataFrame({'value': np.random.rand(num_rows) * 100})   
   df_polars_expr = df.with_columns(     
       (pl.col("value") * 1.1 + pl.col("value").sin()).alias("result")   
   )
``` 
```
In this case, the Polars code is not faster than Pandas. 
この場合、PolarsのコードはPandasよりも速くありません。

Polars has good multicore support, but this code is not easily parallelized. 
Polarsは優れたマルチコアサポートを持っていますが、このコードは簡単には並列化できません。

Polars, however, has better memory management for larger data volumes. 
しかし、Polarsは大きなデータボリュームに対してより良いメモリ管理を提供します。

I can run this Polars code with 500M rows, but the Pandas code crashes at that scale. 
このPolarsコードは500M行で実行できますが、その規模ではPandasコードがクラッシュします。

I can also rewrite the above code as a PySpark program with a Pandas UDF. 
上記のコードをPandas UDFを使用したPySparkプログラムとして書き直すこともできます。

PySpark supports lazy evaluation, withColumn expressions, and Pandas UDFs: 
PySparkは遅延評価、withColumn式、およびPandas UDFをサポートしています：

```  
   from pyspark.sql.functions import pandas_udf, col   
   df = spark.createDataFrame(     
       pd.DataFrame({'value': np.random.rand(num_rows) * 100})   
   )   
   @pandas_udf("double")   
   def sample_pandas_udf(value: pd.Series) -> pd.Series:     
       return value * 1.1 + np.sin(value)   
   df = df.withColumn("pandas_udf_result", sample_pandas_udf(col("value")))
``` 
```
The preceding code uses Arrow to efficiently transfer data between PySpark’s Java Virtual Machine (JVM) and Python. 
前述のコードは、Arrowを使用してPySparkのJava仮想マシン（JVM）とPython間でデータを効率的に転送します。

We can also rewrite the previous code in PySpark as a withColumn expression: 
前のコードをPySparkでwithColumn式として書き直すこともできます：

```  
   from pyspark.sql.functions import col, sin   
   df = df.withColumn(     
       "result", (col("value") * 1.1 + sin(col("value")))   
   )
``` 
```
This code uses PySpark’s SQL expression API and is performed natively in the Spark JVM engine, without the need to transfer data from the JVM to the Pandas UDF. 
このコードはPySparkのSQL式APIを使用し、Spark JVMエンジン内でネイティブに実行され、JVMからPandas UDFにデータを転送する必要はありません。

Lastly, we can rewrite the above code in Python using DuckDB, a high-performance embedded SQL engine: 
最後に、DuckDBという高性能の埋め込みSQLエンジンを使用して、上記のコードをPythonで書き直すことができます：

```  
   import duckdb   
   con = duckdb.connect()   
   con.register("input_df", df)   
   result_df = con.execute("""     
       SELECT       
           value,       
           value * 1.1 + SIN(value) AS result     
       FROM input_df   
   """).fetchdf()
``` 
```
This returns result_df as a Pandas DataFrame and transfers data to and from Pandas using Arrow. 
これにより、result_dfがPandas DataFrameとして返され、Arrowを使用してPandasとの間でデータが転送されます。

Pandas, Polars, PySpark, and DuckDB all can natively exchange their data as Arrow tables, in what is known as _zero (memory) copy. 
Pandas、Polars、PySpark、およびDuckDBはすべて、データをArrowテーブルとしてネイティブに交換でき、これを「ゼロ（メモリ）コピー」と呼びます。

So you can move DataFrames among Pandas, Polars, and DuckDB by reading the source DataFrame as an Arrow table and then creating a DataFrame from that Arrow table in your target framework. 
したがって、ソースDataFrameをArrowテーブルとして読み取り、そのArrowテーブルからターゲットフレームワークでDataFrameを作成することによって、Pandas、Polars、およびDuckDB間でDataFrameを移動できます。

This way, you can write feature pipelines that perform some data transformations in DuckDB, some in Pandas, and some in Polars—without any overhead when moving DataFrames among the different engines. 
このようにして、DuckDBでいくつかのデータ変換を行い、Pandasでいくつかを行い、Polarsでいくつかを行うフィーチャーパイプラインを書くことができ、異なるエンジン間でDataFrameを移動する際のオーバーヘッドはありません。

PySpark, in contrast, is a distributed compute engine, where DataFrames are partitioned across workers. 
対照的に、PySparkは分散計算エンジンであり、DataFrameはワーカー間で分割されます。

Converting a PySpark DataFrame to a Pandas DataFrame requires first collecting the distributed PySpark DataFrame on the driver node—a process that can potentially overload the driver, resulting in an out-of-memory error. 
PySpark DataFrameをPandas DataFrameに変換するには、まず分散PySpark DataFrameをドライバーノードで収集する必要があります。このプロセスは、ドライバーを過負荷にし、メモリエラーを引き起こす可能性があります。

The following code snippet demonstrates how to build a feature pipeline that performs processing steps in different compute engines, efficiently transferring data among them using Arrow: 
次のコードスニペットは、異なる計算エンジンで処理ステップを実行し、Arrowを使用してデータを効率的に転送するフィーチャーパイプラインを構築する方法を示しています：

```  
   import pyarrow as pa   
   pdf = pd.DataFrame({     
       'name': ['Alice', 'Bob', 'Charlie', 'David'],     
       'age': [25, 30, 35, 40],     
       'salary': [50000, 60000, 75000, 90000]   
   })   
   # 6. Convert Pandas DataFrame to PyArrow Table (zero-copy if possible)   
   # 7. Zero-copy if all columns are already Arrow-compatible types   
   arrow_table = pa.Table.from_pandas(pdf)   
   # 8. Convert to Polars DataFrame (zero-copy)   
   pldf = pl.from_arrow(arrow_table)   
   pldf_transformed = pldf.with_columns([     
       pl.when(pl.col('age') < 35)     
       .then(pl.lit('Young'))     
       .otherwise(pl.lit('GettingOn'))     
       .alias('age_category')   
   ])   
   arrow_table_transformed = pldf_transformed.to_arrow()   
   con = duckdb.connect()   
   con.register('employee_table', arrow_table_transformed)   
   # 9. Transform salary to categorical in DuckDB SQL   
   result_df = con.execute("""
``` 
```
```     
       SELECT name, age_category,       
           CASE         
               WHEN salary < 60000 THEN 'Junior'         
               WHEN salary BETWEEN 60000 AND 80000 THEN 'Senior'         
               ELSE 'Staff'       
           END as salary_band     
       FROM employee_table   
   """).df()   
   con.close()   
   fg.insert(result_df)
``` 
```
First, we create a Pandas DataFrame, `pdf, containing employees’ names, ages, and salaries. 
まず、従業員の名前、年齢、給与を含むPandas DataFrame `pdf`を作成します。

Then we convert it to a PyArrow Table, `arrow_table, with (typically) zero copy. 
次に、通常ゼロコピーでPyArrowテーブル`arrow_table`に変換します。

Next, we load this into Polars and transform the employee’s age into a new categorical column, age_category. 
次に、これをPolarsに読み込み、従業員の年齢を新しいカテゴリ列`age_category`に変換します。

After that, we convert the Polars DataFrame back to Arrow and register it as a table in DuckDB, where we add a categorical variable, `salary_band (junior, senior, or staff), using SQL. 
その後、Polars DataFrameをArrowに戻し、DuckDBにテーブルとして登録し、SQLを使用してカテゴリ変数`salary_band（ジュニア、シニア、またはスタッフ）`を追加します。

The final result is a DataFrame that we insert into a feature group. 
最終的な結果は、フィーチャーグループに挿入されるDataFrameです。

###### Data Types
###### データ型

When you write code in ML pipelines, you work with the corresponding Polars/Pandas/PySpark/SQL data types. 
MLパイプラインでコードを書くときは、対応するPolars/Pandas/PySpark/SQLデータ型を使用します。

However, ML pipelines interoperate via a shared data layer, the feature store, and every feature store has its own set of supported data types. 
しかし、MLパイプラインは共有データレイヤーであるフィーチャーストアを介して相互運用し、各フィーチャーストアには独自のサポートされているデータ型のセットがあります。

One complication can arise if you use frameworks in the feature pipeline that are different from those you use with the training/inference pipelines. 
フィーチャーパイプラインで使用するフレームワークが、トレーニング/推論パイプラインで使用するものと異なる場合、1つの複雑さが生じる可能性があります。

For example, the feature pipeline could run in PySpark, while the training pipeline could use Pandas to feed samples to the model. 
例えば、フィーチャーパイプラインはPySparkで実行される可能性がありますが、トレーニングパイプラインはPandasを使用してモデルにサンプルを供給することができます。

However, PySpark supports a set of data types that’s different from the one Pandas supports. 
ただし、PySparkはPandasがサポートするものとは異なるデータ型のセットをサポートしています。

The feature store connects these two pipelines by storing data in its native data types and casting data to/from the framework’s data types. 
フィーチャーストアは、データをネイティブデータ型で保存し、フレームワークのデータ型にデータをキャストすることによって、これら2つのパイプラインを接続します。

For example, imagine your PySpark feature pipeline writes to a feature group a Spark DataFrame with four columns of type: `TimestampType,` `DateType,` `StringType, and` `BinaryType. 
例えば、PySparkフィーチャーパイプラインが、`TimestampType`、`DateType`、`StringType`、および`BinaryType`の4つの列を持つSpark DataFrameをフィーチャーグループに書き込むと想像してください。

The training and batch inference pipelines read these features into Pandas DataFrames. 
トレーニングおよびバッチ推論パイプラインは、これらのフィーチャーをPandas DataFrameに読み込みます。

These pipelines should read data with compatible data types from the offline feature groups. 
これらのパイプラインは、オフラインフィーチャーグループから互換性のあるデータ型のデータを読み込む必要があります。

Hopsworks stores offline feature data with Hive data types, so when a Pandas client reads the features using the Hopsworks API, they are cast to the Pandas data types to become `datetime64[ns],` `datetime64[ns],` `object, and` `object. 
HopsworksはオフラインフィーチャーデータをHiveデータ型で保存するため、PandasクライアントがHopsworks APIを使用してフィーチャーを読み込むと、Pandasデータ型にキャストされて`datetime64[ns]`、`datetime64[ns]`、`object`、および`object`になります。

The feature store is responsible for storing the feature data in its native data types and ensuring that different combinations of frameworks can read and write data as expected. 
フィーチャーストアは、フィーチャーデータをネイティブデータ型で保存し、異なるフレームワークの組み合わせが期待通りにデータを読み書きできるようにする責任があります。

It should ensure that, irrespective of whether you use SQL, Pandas, Polars, PySpark, or Flink for the feature pipeline, the training and inference pipelines will be 
それは、フィーチャーパイプラインにSQL、Pandas、Polars、PySpark、またはFlinkを使用するかどうかにかかわらず、トレーニングおよび推論パイプラインが



able to read the feature data in supported DataFrame engines. 
サポートされているDataFrameエンジンでフィーチャーデータを読み取ることができます。

There is one exception you may encounter, however. 
ただし、1つの例外が発生する可能性があります。

There is potential for a loss of precision for some data types if your feature pipeline compute engine supports higher-precision data types than the feature store or if a training/inference pipeline compute engine supports lower-precision data types than the feature store. 
フィーチャーパイプラインの計算エンジンがフィーチャーストアよりも高精度のデータ型をサポートしている場合や、トレーニング/推論パイプラインの計算エンジンがフィーチャーストアよりも低精度のデータ型をサポートしている場合、一部のデータ型で精度の損失が発生する可能性があります。

There is also the added complication that the feature store stores data in both offline tables and online tables, each of which may support different data types. 
さらに、フィーチャーストアはオフラインテーブルとオンラインテーブルの両方にデータを保存しており、それぞれ異なるデータ型をサポートしている可能性があるという複雑さもあります。

In Hopsworks, the offline table uses Hive data types while the online table uses MySQL data types. 
Hopsworksでは、オフラインテーブルはHiveデータ型を使用し、オンラインテーブルはMySQLデータ型を使用します。

The details of the mappings from Spark and Pandas data types to the respective Hive and MySQL data types are found in the [Hopsworks](https://oreil.ly/NkGat) [documentation.](https://oreil.ly/NkGat) 
SparkおよびPandasデータ型からそれぞれのHiveおよびMySQLデータ型へのマッピングの詳細は、[Hopsworks](https://oreil.ly/NkGat)の[ドキュメント](https://oreil.ly/NkGat)にあります。

###### Arrays, structs, maps, and tensors
###### 配列、構造体、マップ、およびテンソル

Hopsworks stores the expected primitive data types (int, `string,` `boolean,` `float,` ``` double, long, decimal, timestamp, date) as well as complex data types, such as arrays, structs, and maps. 
Hopsworksは、期待される基本データ型（int、`string`、`boolean`、`float`、``` double、long、decimal、timestamp、date）および配列、構造体、マップなどの複雑なデータ型を保存します。

Vector embeddings are stored as an array of floats. 
ベクトル埋め込みは、浮動小数点数の配列として保存されます。

The other main data structure in machine learning is the tensor. 
機械学習におけるもう1つの主要なデータ構造はテンソルです。

A tensor is a multidimensional numerical data structure that can represent data in one or more dimensions. 
テンソルは、1つ以上の次元でデータを表現できる多次元数値データ構造です。

Unlike traditional matrices, which are two-dimensional, tensors extend to three or more dimensions. 
従来の行列が二次元であるのに対し、テンソルは三次元以上に拡張されます。

In deep learning, tensors are commonly constructed from unstructured data, such as images (for 3D tensors), videos (for 4D tensors), and audio signals (for 1D tensors), enabling the representation and processing of complex data formats (see Figure 6-6). 
深層学習では、テンソルは一般的に、画像（3Dテンソル用）、動画（4Dテンソル用）、音声信号（1Dテンソル用）などの非構造化データから構築され、複雑なデータ形式の表現と処理を可能にします（図6-6を参照）。

_Figure 6-6. Tensor data structures generalize to store anything from scalars to arrays and matrices and higher-dimensional data._ 
_図6-6. テンソルデータ構造は、スカラーから配列、行列、さらには高次元データまでを保存するために一般化されます。_

Audio data is 1D as audio input is sampled and quantized, although it can be stored as 2D data when you have many tracks, such as left and right channels for stereo sound. 
音声データは、音声入力がサンプリングされ量子化されるため1Dですが、ステレオ音声の左チャンネルと右チャンネルのように多くのトラックがある場合は2Dデータとして保存できます。

Image data typically contains pixels with an X, Y offset and a color channel—making it three-dimensional (3D) data. 
画像データは通常、X、Yオフセットとカラーチャンネルを持つピクセルを含んでおり、三次元（3D）データになります。

Video data has an additional channel for the frame number—making it 4D data. 
動画データにはフレーム番号用の追加のチャンネルがあり、これにより4Dデータになります。

Audio, images, and videos can be transformed into tensor data and used for training and inference in deep learning.  
音声、画像、動画はテンソルデータに変換され、深層学習のトレーニングと推論に使用できます。

PyTorch is the most popular framework for deep learning. 
PyTorchは深層学習の最も人気のあるフレームワークです。

PyTorch represents tensors as instances of the `torch.Tensor class, with the default data type being` ``` torch.float32 (torch.int64 is the default for integer tensors). 
PyTorchはテンソルを`torch.Tensor`クラスのインスタンスとして表現し、デフォルトのデータ型は``` torch.float32（整数テンソルのデフォルトはtorch.int64）です。

You can print the shape of a tensor by using the `shape attribute of` `torch.Tensor:` ``` print(tensor.shape). 
テンソルの形状は、`torch.Tensor`の`shape`属性を使用して印刷できます：``` print(tensor.shape)。

We typically do not store tensors in a feature store. 
通常、フィーチャーストアにテンソルを保存することはありません。

Instead, training/inference pipelines transform unstructured data (in compressed file formats such as PNG, MP4, and MP3 for images, video, and sound, respectively) into tensors after it has been read from files: 
代わりに、トレーニング/推論パイプラインは、ファイルから読み取った後に非構造化データ（画像、動画、音声用のPNG、MP4、MP3などの圧縮ファイル形式）をテンソルに変換します：

```  
import torch  
from torchvision import transforms  
from PIL import Image  
image = Image.open("path/to/your/image.png")  
# 10. Define a transformation pipeline to convert the image into a tensor  
transform = transforms.Compose([ transforms.ToTensor() ])  
image_tensor = transform(image)  
```

It is, however, sometimes desirable to preprocess the files in a training dataset pipeline that outputs tensors as files, such as in TFRecord files. 
ただし、TFRecordファイルのように、テンソルをファイルとして出力するトレーニングデータセットパイプラインでファイルを前処理することが望ましい場合があります。

TFRecord is a file format that natively stores serialized tensors. 
TFRecordは、シリアライズされたテンソルをネイティブに保存するファイル形式です。

Using TFRecord files can reduce the amount of CPU preprocessing needed in training pipelines by removing the need to transform unstructured data into tensors. 
TFRecordファイルを使用することで、非構造化データをテンソルに変換する必要がなくなるため、トレーニングパイプラインで必要なCPU前処理の量を減らすことができます。

This can help improve GPU utilization levels— assuming CPU preprocessing is a bottleneck in the training pipeline. 
これにより、GPUの利用率を向上させることができます—CPU前処理がトレーニングパイプラインのボトルネックであると仮定した場合。

###### Implicit or explicit schemas for feature groups
###### フィーチャーグループの暗黙的または明示的なスキーマ

In Chapter 5, we described how the schema of a feature group can be inferred from the first DataFrame inserted into it. 
第5章では、フィーチャーグループのスキーマが最初に挿入されたDataFrameから推測できる方法について説明しました。

You may already have written programs that read CSV files into DataFrames in Pandas, Polars, or PySpark and noticed that they don’t always infer the “correct” data types. 
すでにPandas、Polars、またはPySparkでCSVファイルをDataFrameに読み込むプログラムを書いたことがあり、必ずしも「正しい」データ型を推測しないことに気付いているかもしれません。

By correct, we mean the data type you wanted, not the one you got. 
ここで言う「正しい」とは、あなたが望んでいたデータ型のことであり、得られたデータ型のことではありません。

For example, Pandas can infer the schema of columns when reading CSV files, but if one of the columns is a datetime column, Pandas by default infers it is an object (string) dtype. 
たとえば、PandasはCSVファイルを読み込む際に列のスキーマを推測できますが、列の1つがdatetime列である場合、Pandasはデフォルトでそれをオブジェクト（文字列）dtypeとして推測します。

You can fix this by passing a parameter with the columns that contains dates (parse_dates=['col1',..,'colN']). 
これを修正するには、日付を含む列を持つパラメータを渡すことで（parse_dates=['col1',..,'colN']）、修正できます。

PySpark is not much better at parsing CSV files, as it assumes all columns are strings, unless you set ``` inferSchema=True. 
PySparkはCSVファイルの解析においてあまり改善されておらず、すべての列が文字列であると仮定します。`inferSchema=True`を設定しない限り。

In production feature pipelines, it is generally considered best practice to explicitly specify the schema for a feature group, which helps to prevent any type inference errors or precision errors when inferring data types. 
本番環境のフィーチャーパイプラインでは、フィーチャーグループのスキーマを明示的に指定することが一般的にベストプラクティスと見なされており、データ型を推測する際の型推測エラーや精度エラーを防ぐのに役立ちます。

If in doubt, spell it (the schema) out. 
疑問がある場合は、スキーマを明示的に記述してください。

Here is an example of how to specify an explicit schema for a feature group in Hopsworks:  
Hopsworksでフィーチャーグループの明示的なスキーマを指定する方法の例を示します：

```  
from hsfs.feature import Feature  
features = [  
    Feature(name="id",type="int", online_type="int"),  
    Feature(name="name",type="string",online_type="varchar(2000)")  
]  
fg = fs.create_feature_group(name="fg_with_explicit_schema",  
                  features=features,  
                  …)  
fg.save(features)  
```

Note that you can also explicitly define the data types for the offline store (type="..") and the online store (online_type="..") as part of the feature group schema. 
オフラインストア（type=".."）およびオンラインストア（online_type=".."）のデータ型をフィーチャーグループスキーマの一部として明示的に定義することもできます。

###### Credit Card Fraud Features
###### クレジットカード詐欺機能

We now look at MITs to create features for our credit card fraud detection system. 
ここでは、クレジットカード詐欺検出システムのための機能を作成するためのMITを見ていきます。

We start by noting the data-related challenges in building a robust credit card fraud detection system. 
堅牢なクレジットカード詐欺検出システムを構築する際のデータ関連の課題に注目します。

They include: 
これには以下が含まれます：

_Class imbalance_ We have very few examples of fraud compared with nonfraud transactions. 
_クラスの不均衡_ 詐欺の例は、非詐欺のトランザクションと比較して非常に少ないです。

_Nonstationary prediction problems_ Fraudsters constantly come up with novel strategies for fraud, so we will need to frequently retrain our model on the latest data. 
_非定常予測問題_ 詐欺師は常に新しい詐欺戦略を考案するため、最新のデータでモデルを頻繁に再トレーニングする必要があります。

_Data drift_ This arises where unseen patterns in transaction activity are common. 
_データドリフト_ これは、トランザクション活動における未見のパターンが一般的な場合に発生します。

_ML fraud models_ These are typically used in addition to rule-based approaches that detect simple fraud schemes and patterns. 
_機械学習詐欺モデル_ これらは通常、単純な詐欺スキームやパターンを検出するルールベースのアプローチに加えて使用されます。

In Chapter 4, we introduced the features we want to create from our source data. 
第4章では、ソースデータから作成したい機能を紹介しました。

We now present the MITs used to create those features. 
ここでは、これらの機能を作成するために使用されるMITを示します。

Figure 6-7 shows the feature pipeline that uses the tables (and event-streaming platform) in our data mart as the data sources. 
図6-7は、データマート内のテーブル（およびイベントストリーミングプラットフォーム）をデータソースとして使用するフィーチャーパイプラインを示しています。

The data mart includes credit card transactions as events in an event-streaming platform, a fact table that the credit card transaction events are persisted to, the four dimension “details” tables, and the cc_fraud table that contains labels.  
データマートには、イベントストリーミングプラットフォーム内のイベントとしてのクレジットカードトランザクション、クレジットカードトランザクションイベントが永続化されるファクトテーブル、4つの次元「詳細」テーブル、およびラベルを含むcc_fraudテーブルが含まれています。

_Figure 6-7. Dataflow graph from the data mart to the feature groups via MITs. Notice that some data transformations are composed from other transformations (the input of a transformation is the output of another transformation) and that joins bring features from different entities (cards, accounts, merchants) together._ 
_図6-7. データマートからフィーチャーグループへのデータフローグラフ（MITを介して）。いくつかのデータ変換が他の変換から構成されていることに注意してください（変換の入力は別の変換の出力です）および結合が異なるエンティティ（カード、アカウント、商人）から機能をまとめることを示しています。_

We will now take a new approach to defining our transformation logic. 
これから、変換ロジックを定義する新しいアプローチを取ります。

Instead of presenting the source code, we will present the prompts that I used to create the transformation logic by using an LLM. 
ソースコードを提示する代わりに、LLMを使用して変換ロジックを作成するために使用したプロンプトを提示します。

Table 6-2 shows the prompts I used to create the transformation code in the book’s source code repository. 
表6-2は、書籍のソースコードリポジトリで変換コードを作成するために使用したプロンプトを示しています。

As of mid-2025, LLMs are very good at generating Pandas, Polars, and PySpark source code from natural language instructions. 
2025年中頃の時点で、LLMは自然言語の指示からPandas、Polars、およびPySparkのソースコードを生成するのが非常に得意です。

You may have to prepend the logical models for your tables (see Chapter 8) so that the LLM understands the data types and the semantics of the columns it is working with. 
LLMが作業している列のデータ型と意味を理解できるように、テーブルの論理モデルを前に追加する必要があるかもしれません（第8章を参照）。

Hopsworks provides its own LLM assistant, Brewer, that provides details of data sources and feature groups, making it easier to develop the transformation logic.  
Hopsworksは、データソースとフィーチャーグループの詳細を提供する独自のLLMアシスタントBrewerを提供しており、変換ロジックの開発を容易にします。

_Table 6-2. LLM prompts that create Polars code to create features from our data sources_ 
_表6-2. データソースから機能を作成するためのPolarsコードを生成するLLMプロンプト_

**Feature** **Prompt to write code for feature** 
**機能** **機能のコードを書くためのプロンプト**

``` 
chargeback_rate_prev_week 
```
From merchant_details, write Polars code to compute a 7-day tumbling window using chargeback_rate_prev_day. 
merchant_detailsから、chargeback_rate_prev_dayを使用して7日間のタムブリングウィンドウを計算するPolarsコードを書いてください。

Read up from the FG with overlap for the 7 days before our start date, as we don’t want empty first. 
最初が空でないように、開始日より前の7日間のオーバーラップを持つFGから読み取ります。

We want this feature function to take start/end dates, so it can both backfill and take new data.  
この機能関数には開始日と終了日を受け取らせたいので、バックフィルと新しいデータを取得できるようにします。

`time_since_last_trans` 
`time_since_last_trans` 

Join cc_trans_aggs_fg with cc_trans_fg, using cc_num to produce DataFrame df. 
cc_trans_aggs_fgとcc_trans_fgをcc_numを使用して結合し、DataFrame dfを生成します。

Then, compute time_since_last_trans in a Python UDF, using Polars by subtracting prev_ts_transaction from event_time. 
次に、prev_ts_transactionをevent_timeから引いてPolarsを使用してPython UDFでtime_since_last_transを計算します。

Apply the Python UDF to df to compute the new feature.  
新しい機能を計算するためにPython UDFをdfに適用します。

`days_to_card_expiry` 
`days_to_card_expiry` 

Join card_details with cc_trans_fg, using cc_num to produce DataFrame df. 
card_detailsとcc_trans_fgをcc_numを使用して結合し、DataFrame dfを生成します。

Then, compute days_to_card_expiry in a Pandas UDF by subtracting event_time from cc_expiry_date. 
次に、event_timeをcc_expiry_dateから引いてPandas UDFでdays_to_card_expiryを計算します。

Apply the Pandas UDF to df to compute the new feature.  
新しい機能を計算するためにPandas UDFをdfに適用します。

There are many other data transformations for our credit card example system that you can find in the book’s source code repository. 
書籍のソースコードリポジトリには、クレジットカードの例システムに対する他の多くのデータ変換があります。

The features are a mix of simple features (copied directly from the source table), some that were computed by using map functions (days_since_credit_rating_changed), and a lot of features that require maintaining state across data transformations, such as those that summarize observed events over windows of time (like an hour, minute, or day). 
機能は、ソーステーブルから直接コピーされた単純な機能、マップ関数を使用して計算された機能（days_since_credit_rating_changed）、および時間のウィンドウ（1時間、1分、1日など）にわたって観察されたイベントを要約するために状態を維持する必要がある多くの機能の組み合わせです。

In particular, all the features computed for the cc_trans_aggs_fg feature group require stateful data transformations. 
特に、cc_trans_aggs_fgフィーチャーグループのために計算されたすべての機能は、状態を持つデータ変換を必要とします。

In Chapter 9, we will look at how to implement these model-independent data transformations in streaming feature pipelines. 
第9章では、ストリーミングフィーチャーパイプラインにおけるこれらのモデル非依存のデータ変換を実装する方法を見ていきます。

When writing the data transformations with the help of LLMs, consider that sometimes the generated code has bugs. 
LLMの助けを借りてデータ変換を書くときは、生成されたコードにバグがあることがあることを考慮してください。

For example, sometimes GPT-4o hallucinates that Polars DataFrames support the widely used Pandas DataFrame apply function, which is used to apply a UDF to the DataFrame. 
たとえば、時々GPT-4はPolars DataFrameが広く使用されているPandas DataFrameのapply関数をサポートしていると誤認識し、これはUDFをDataFrameに適用するために使用されます。

When I get errors, I paste the error log into my LLM’s prompt and ask it to fix the bug. 
エラーが発生したときは、エラーログをLLMのプロンプトに貼り付けてバグを修正するように頼みます。

Generally, this works. 
一般的に、これは機能します。

But you still need to understand the code produced. 
しかし、生成されたコードを理解する必要があります。

Ultimately, you sign off on the code being correct. 
最終的には、コードが正しいことを確認します。



. Generally, this works. But you still need to understand the code produced. 
一般的に、これは機能します。しかし、生成されたコードを理解する必要があります。

Ultimately, you sign off on the code being correct. 
最終的には、あなたがそのコードが正しいと承認します。

For this reason, unit testing your feature functions becomes even more critical. 
この理由から、あなたの機能関数の単体テストはさらに重要になります。

Again, I use LLMs to generate the unit tests for the feature functions I write. 
再度、私は自分が書いた機能関数の単体テストを生成するためにLLMsを使用します。

Again, I inspect the generated unit tests for correctness before I incorporate them. 
再度、私はそれらを組み込む前に生成された単体テストの正確性を確認します。

###### Composition of Transformations 変換の構成

In batch pipelines, we often compute aggregations (such as min, max, mean, median, and standard deviation) over a window of time, such as an hour or a day. 
バッチパイプラインでは、通常、1時間や1日などの時間ウィンドウにわたって集約（最小値、最大値、平均、中央値、標準偏差など）を計算します。

Often more than one time window contains useful predictive signals for models. 
しばしば、1つ以上の時間ウィンドウがモデルにとって有用な予測信号を含んでいます。

For example, we could compute aggregates once per day but also trailing 7-day and trailing 30-day aggregates, as shown in Figure 6-8. 
例えば、私たちは1日に1回集約を計算することもできますが、トレーリング7日間およびトレーリング30日間の集約も計算できます（図6-8に示されています）。



_Figure 6-8. We can compute single-day and multiday aggregations in the same feature pipeline. Multiday aggregations combine the current daily aggregation with the historical daily aggregations read from the feature store._
_Figure 6-8. 同じフィーチャーパイプラインで単日および複数日集計を計算できます。複数日集計は、現在の1日集計とフィーチャーストアから読み取った過去の1日集計を組み合わせます。_

Ideally, we should compute the larger windows (30-day and 7-day) from the smallest window (1-day) to reduce the amount of work needed to compute aggregations.
理想的には、集計を計算するために必要な作業量を減らすために、最小のウィンドウ（1日）から大きなウィンドウ（30日および7日）を計算するべきです。

Table 6-3 shows how to compute popular aggregations for larger windows from smaller windows.
表6-3は、より小さなウィンドウからより大きなウィンドウの人気のある集計を計算する方法を示しています。

_Table 6-3. Roll-up of common aggregations from 1-day windows to 7-day windows_
**集計** **1日集計から7日集計を計算する方法**
count Sum the previous 7 days together.
count 過去7日間の合計を計算します。

sum Sum the previous 7 days together.
sum 過去7日間の合計を計算します。

max/min Get the max/min over all the previous 7 days.
max/min 過去7日間の最大値/最小値を取得します。

stddev We need to compute and store additional daily data. For each day, we also need the count of records. Then, we can compute the 7-day aggregate using the sum of squares.
stddev 追加の1日データを計算して保存する必要があります。各日について、レコードのカウントも必要です。次に、平方和を使用して7日集計を計算できます。

mean We need to compute and store additional daily data. For each day, we also need the count of records. Then, we can compute the 7-day aggregate as a weighted mean.
mean 追加の1日データを計算して保存する必要があります。各日について、レコードのカウントも必要です。次に、加重平均として7日集計を計算できます。

approxQuantile We need to compute and store complete sorted lists of daily values. With approximate summaries like TDigests or histograms, we can approximate 7-day quantiles by merging daily distributions.
approxQuantile 完全にソートされた日次値のリストを計算して保存する必要があります。TDigestsやヒストグラムのような近似要約を使用すると、日次分布をマージすることで7日分位数を近似できます。

distinct count For an accurate result, we need to store the unique values for each day and perform a set union.
distinct count 正確な結果を得るためには、各日のユニークな値を保存し、集合の和を実行する必要があります。 
Approximate answers are possible with HyperLogLog (memory efficient but worst accuracy) or Bitmap/Bloom Filters (moderate memory efficiency and better accuracy).
近似的な回答は、HyperLogLog（メモリ効率が良いが精度が最悪）またはBitmap/Bloom Filters（中程度のメモリ効率とより良い精度）を使用することで可能です。

For example, in PySpark, we can compute a multiday mean using the weighted mean approach. The PySpark code looks as follows:
例えば、PySparkでは、加重平均アプローチを使用して複数日の平均を計算できます。PySparkのコードは次のようになります：

```   
def compute_mean(days):     
    window_spec = \       
        Window.partitionBy("user_id").orderBy("date").rowsBetween(-days, 0)       
    df = df.withColumn(f"{days}d_avg",       
        F.sum(F.col("daily_mean") * F.col("daily_count")).over(window_spec) /       
        F.sum("daily_count").over(window_spec))
```

The sum of squares is an alternative approach we could have used, but it requires an additional column storing the sum of squares, so we prefer the weighted mean approach, as it requires one less column to store in our daily aggregations feature group.
平方和は私たちが使用できた代替アプローチですが、平方和を保存する追加の列が必要です。そのため、日次集計フィーチャーグループに保存する列が1つ少なくて済む加重平均アプローチを好みます。

###### 10.0.0.0.0.1. Summary and Exercises
###### 10.0.0.0.0.2. 要約と演習

In this chapter, we introduced guidelines for writing model-independent transformations in feature pipelines. 
この章では、フィーチャーパイプラインにおけるモデル非依存の変換を書くためのガイドラインを紹介しました。

We began by describing best practices for how to organize the source code for your system in a monorepo, what the common data sources for feature pipelines are, and the data types you need to work with when writing feature pipelines.
私たちは、モノレポ内でシステムのソースコードを整理するためのベストプラクティス、フィーチャーパイプラインの一般的なデータソース、フィーチャーパイプラインを書く際に扱う必要があるデータ型について説明しました。

We looked at different classes of data transformations for DataFrames, depending on how they add or remove columns and/or rows.
私たちは、列や行を追加または削除する方法に応じて、DataFrameのデータ変換の異なるクラスを見ました。

We also looked at data transformation examples in Pandas, Polars, and PySpark and how Arrow can efficiently transfer data among these different engines.
また、Pandas、Polars、PySparkにおけるデータ変換の例と、Arrowがこれらの異なるエンジン間でデータを効率的に転送できる方法についても見ました。

We finally introduced examples of model-independent data transformations for our credit card fraud system, including binning for categorical data, mapping functions, RFM features, and aggregations.
最後に、カテゴリデータのビニング、マッピング関数、RFM特徴、集計を含む、クレジットカード詐欺システムのためのモデル非依存のデータ変換の例を紹介しました。

The following exercises will help you learn how to design and write MITs:
以下の演習は、MITを設計し、書く方法を学ぶのに役立ちます：

- You are tasked with developing a credit card fraud detection ML system. The credit card issuer estimates that there will be at most 50K transactions per day for the current year, growing to at most 100K transactions per day for the next two years. You have 12 months of historical transaction data. Your team does not have a strong data engineering background. Your data mart tables are stored on Iceberg on S3. Which data engineering framework would you choose to write your batch feature pipelines?
- クレジットカード詐欺検出MLシステムを開発する任務があります。クレジットカード発行者は、今年は1日あたり最大50Kのトランザクションがあると見積もっており、次の2年間で最大100Kのトランザクションに成長すると予想しています。あなたは12ヶ月の過去のトランザクションデータを持っています。あなたのチームは強力なデータエンジニアリングのバックグラウンドを持っていません。あなたのデータマートテーブルはS3のIcebergに保存されています。バッチフィーチャーパイプラインを書くためにどのデータエンジニアリングフレームワークを選びますか？

- Answer the previous question again, but this time when data volumes are 10 million transactions per day.
- 前の質問に再度答えてください。ただし、データ量が1日あたり1000万トランザクションの場合です。

- Assume you have a new column, `email, in the` `account_details table. Use an` LLM to help write a feature function that transforms an email address into a numerical feature that represents the quality of the email address. Hint: use an LLM, tell it to use the email-validator Python library, and tell it to use the email address domain name to help determine the “score” for the email address.
- 新しい列`email`が`account_details`テーブルにあると仮定します。LLMを使用して、メールアドレスを数値的な特徴に変換するフィーチャー関数を書くのを手伝ってください。この数値的な特徴は、メールアドレスの品質を表します。ヒント：LLMを使用し、email-validator Pythonライブラリを使用するように指示し、メールアドレスのドメイン名を使用してメールアドレスの「スコア」を決定するのを手伝ってください。



