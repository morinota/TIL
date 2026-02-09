CHAPTER 8: Batch Feature Pipelines 第8章: バッチフィーチャーパイプライン

In the previous two chapters, we looked at how to implement data transformations to create reusable features and model-specific features. 
前の2章では、再利用可能な特徴とモデル固有の特徴を作成するためのデータ変換の実装方法を見てきました。
Now we’ll look at how to productionize the creation of reusable feature data using batch feature pipelines. 
ここでは、バッチフィーチャーパイプラインを使用して再利用可能なフィーチャーデータの作成をプロダクション化する方法を見ていきます。
A batch feature pipeline is a program that reads data from data sources, applies MITs to the extracted data, and stores the computed feature data in the feature store. 
**バッチフィーチャーパイプラインは、データソースからデータを読み取り、抽出されたデータにMITを適用し、計算されたフィーチャーデータをフィーチャーストアに保存するプログラム**です。
The batch feature pipeline can run on a schedule, for example, once per hour or day, incrementally processing new data as it becomes available for processing. 
バッチフィーチャーパイプラインは、例えば1時間または1日ごとにスケジュールで実行され、新しいデータが処理可能になると、それをインクリメンタルに処理します。
It can also be run on demand to transform a large volume of historical data into features, in a process known as backfilling. 
また、バックフィリングと呼ばれるプロセスで、大量の履歴データをフィーチャーに変換するために、オンデマンドで実行することもできます。

<!-- ここまで読んだ! -->

The goal of a batch feature pipeline is to automate feature creation in what is known as batch processing, which is efficient in its use of resources compared with processing a single record at a time. 
バッチフィーチャーパイプラインの目的は、バッチ処理として知られるフィーチャー作成を自動化することであり、**これは1レコードずつ処理する場合と比較してリソースの使用が効率的**です。
For example, imagine comparing the time it takes to empty a dishwasher one glass or plate at a time with unloading batches of plates and glasses. 
例えば、食器洗い機を1つのグラスや皿ずつ空にするのにかかる時間と、皿やグラスのバッチを一度に空にするのにかかる時間を比較してみてください。
Similarly, in data processing, processing batches of data is much more efficient than processing one record at a time. 
同様に、データ処理においても、データのバッチを処理することは、1レコードずつ処理するよりもはるかに効率的です。
Also, if batch processing is performed daily, you can take advantage of lower-cost off-peak processing time at night. 
**また、バッチ処理が毎日行われる場合、夜間のオフピーク処理時間を利用してコストを削減**できます。
Another operational benefit, compared with stream processing, is that errors only need to be fixed before the next scheduled run of your batch feature pipeline—you might not need to be woken up by your pager to fix your pipeline. 
ストリーム処理と比較した場合のもう1つの運用上の利点は、エラーはバッチフィーチャーパイプラインの次のスケジュールされた実行前に修正するだけで済むため、パイプラインを修正するためにページャーで起こされる必要がないかもしれません。
The downside of batch processing is that your feature data is only guaranteed to be as fresh as the time interval between batch processing runs. 
バッチ処理の欠点は、フィーチャーデータがバッチ処理の実行間隔と同じだけ新鮮であることが保証されるだけであることです。

<!-- ここまで読んだ! -->

In this chapter, you will also learn how to create synthetic data for our credit card fraud data mart by prompting an LLM to create a program that generates the synthetic data. 
この章では、LLMに合成データを生成するプログラムを作成させることで、クレジットカード詐欺データマートのための合成データを作成する方法も学びます。
You will also learn how to write a batch feature pipeline that can be parameterized against data sources to run in either backfill or production (incremental data processing) mode. 
また、バックフィルまたはプロダクション（インクリメンタルデータ処理）モードで実行するためにデータソースに対してパラメータ化できるバッチフィーチャーパイプラインを書く方法も学びます。
We will introduce orchestrators for running batch feature pipelines. 
バッチフィーチャーパイプラインを実行するためのオーケストレーターを紹介します。
Finally, you will learn how to design a data contract for groups by providing data quality guarantees. 
最後に、データ品質保証を提供することで、グループのためのデータ契約を設計する方法を学びます。
This will involve validating feature data before it is stored in the feature store by using Great Expectations and performing data governance checks using schematized tags for feature groups. 
これは、Great Expectationsを使用してフィーチャーデータがフィーチャーストアに保存される前に検証し、フィーチャーグループのためのスキーマ化されたタグを使用してデータガバナンスチェックを実施することを含みます。

<!-- ここまで読んだ! -->

## 1. Batch Feature Pipelines バッチフィーチャーパイプライン

Feature pipelines are a type of data pipeline—a program that automates the transfer and transformation of data from one or more data sources to a destination data store, known as the data sink. 
フィーチャーパイプラインは、データパイプラインの一種であり、1つまたは複数のデータソースからデータを転送および変換し、データシンクとして知られる宛先データストアに自動化するプログラムです。
In Chapter 4, we introduced two popular classes of data pipelines, ETL and ELT pipelines. 
第4章では、**ETLとELTパイプラインという2つの人気のあるデータパイプラインのクラスを紹介**しました。(そうだっけ??:thinking:)
ETL pipelines transform the data before it is written to the destination, while ELT pipelines write the data to the destination and then transform the data in place (typically using SQL in a data warehouse). 
**ETLパイプラインは、データを宛先に書き込む前に変換しますが、ELTパイプラインはデータを宛先に書き込み、その後データをその場で変換します（通常はデータウェアハウスでSQLを使用）。**
Data pipelines are operational services that need to either run on a schedule (in which case they are called batch data pipelines) or run 24/7 (in which case they are called streaming data pipelines). 
データパイプラインは、スケジュールで実行する必要がある運用サービス（この場合はバッチデータパイプラインと呼ばれます）または24時間365日実行する必要があるサービス（この場合はストリーミングデータパイプラインと呼ばれます）です。
Batch feature pipelines are batch data pipelines that transform source data into feature data and typically store their output in a feature store. 
バッチフィーチャーパイプラインは、ソースデータをフィーチャーデータに変換し、通常はその出力をフィーチャーストアに保存するバッチデータパイプラインです。

Batch feature pipelines can be implemented as ELT or ETL pipelines, but they are most commonly ETL pipelines. 
バッチフィーチャーパイプラインはELTまたはETLパイプラインとして実装できますが、最も一般的なのはETLパイプラインです。
ELT pipelines are SQL programs, and they are efficient and easy to use to create popular features such as aggregations, statistical features, and lagged features. 
ELTパイプラインはSQLプログラムであり、集約、統計的特徴、遅延特徴などの人気のある特徴を作成するために効率的で使いやすいです。
However, SQL is limited in its feature engineering capabilities, and most batch feature pipelines are ETL programs. 
**しかし、SQLはフィーチャーエンジニアリングの能力に制限があり、ほとんどのバッチフィーチャーパイプラインはETLプログラムです。**
Batch feature pipelines as ETL programs are typically Python programs (Pandas, Polars, PySpark) and support richer feature creation capabilities by leveraging the Python ecosystem of data transformation libraries. 
**ETLプログラムとしてのバッチフィーチャーパイプラインは、通常はPythonプログラム（Pandas、Polars、PySpark）であり、Pythonのデータ変換ライブラリのエコシステムを活用することで、より豊富なフィーチャー作成機能をサポート**します。
For example, there are Python libraries for creating vector embeddings, web scraping, reading from third-party APIs, and easy API integration with LLMs for data processing and information retrieval. 
例えば、ベクトル埋め込みの作成、ウェブスクレイピング、サードパーティAPIからの読み取り、データ処理および情報取得のためのLLMとの簡単なAPI統合のためのPythonライブラリがあります。

<!-- ここまで読んだ! -->

Batch feature pipelines as ETL programs have a common structure: 
ETLプログラムとしてのバッチフィーチャーパイプラインは、共通の構造を持っています。

1. An execution run of the program is scheduled or triggered by an orchestrator. 
   1. プログラムの実行は、オーケストレーターによってスケジュールまたはトリガーされます。

2. Input data is read from one or more data sources with start/end timestamps for the time range of input data to process for this run. 
   1. 入力データは、**今回の実行で処理する入力データの時間範囲の開始/終了タイムスタンプ**を持つ1つまたは複数のデータソースから読み取られます。

3. A directed acyclic graph (DAG) of MITs creates feature data for feature groups. 
   1. MITの有向非巡回グラフ（DAG）がフィーチャーグループのためのフィーチャーデータを作成します。

4. A set of data and schema validation checks are applied to the feature data. 
   1. フィーチャーデータに対してデータおよびスキーマの検証チェックが適用されます。

5. Feature data is saved to one or more feature groups. 
   1. フィーチャーデータは1つまたは複数のフィーチャーグループに保存されます。

We will start by looking at different types of data sources for feature pipelines (for both batch and streaming). 
私たちは、フィーチャーパイプラインのためのさまざまなタイプのデータソース（バッチとストリーミングの両方）を見ていくことから始めます。

## 2. Feature Pipeline Data Sources フィーチャーパイプラインデータソース

Ground zero for data for AI systems consists of the applications, services, and devices connected to users, machines, and the real world. 
AIシステムのデータの出発点は、ユーザー、機械、現実世界に接続されたアプリケーション、サービス、デバイスで構成されています。
They produce data that is stored in operational databases, lakehouses or data warehouses (on object stores), and event-streaming platforms. 
これらは、**運用データベース、レイクハウスまたはデータウェアハウス（オブジェクトストア上）、およびイベントストリーミングプラットフォームに保存されるデータを生成**します。
These data stores are the main data sources for feature pipelines, and they fall into one of three classes: batch sources, (event) stream sources, and API sources (see Figure 8-1). 
これらのデータストアはフィーチャーパイプラインの主要なデータソースであり、**バッチソース、（イベント）ストリームソース、APIソースの3つのクラスのいずれかに分類**されます（図8-1を参照）。

![]()
_Figure 8-1. Simplified architecture of data stores and data flows to (batch and streaming) feature pipelines. Feature pipelines can process data from batch data sources, stream data sources, and API sources._  
_図8-1. データストアと（バッチおよびストリーミング）フィーチャーパイプラインへのデータフローの簡略化されたアーキテクチャ。フィーチャーパイプラインは、バッチデータソース、ストリームデータソース、およびAPIソースからデータを処理できます。_

- メモ: 図8-1の内容
  - feature pipelineへのデータの流れ
    - 1. まずアプリケーションやサービスが出発点。
    - 2. それらがデータ生成し、Operational DBやイベントバスにデータを生成する。
    - 3. Operational DBやイベントバスからDWHやデータレイクにもデータが流れる。
    - 4. 2と3のデータソースから、batch feature pipelineやstreaming feature pipelineがデータを取得し、feature storeにfeature dataを書き込む。

Backfilling typically uses batch data sources (column-oriented databases, row-oriented databases, object stores) to read historical data. 
バックフィリングは通常、バッチデータソース（列指向データベース、行指向データベース、オブジェクトストア）を使用して履歴データを読み取ります。
Scheduled batch feature pipelines or streaming feature pipelines read new incremental data from any or all of the batch, stream, and API data sources. 
スケジュールされたバッチフィーチャーパイプライン(=backfillじゃないやつ!)またはストリーミングフィーチャーパイプラインは、バッチ、ストリーム、およびAPIデータソースのいずれかまたはすべてから新しいインクリメンタルデータを読み取ります。
Feature pipelines, through ODTs, can use external APIs as data sources. 
フィーチャーパイプラインは、ODTを通じて外部APIをデータソースとして使用できます。
Streaming feature pipelines typically have an event-streaming platform (stream source) as the main data source. 
ストリーミングフィーチャーパイプラインは通常、イベントストリーミングプラットフォーム（ストリームソース）を主要なデータソースとしています。

<!-- ここまで読んだ! -->

### 2.1. Batch Data Sources バッチデータソース

Columnar stores, row-oriented stores, object stores, and NoSQL stores are canonical examples of batch data sources. 
**列指向ストア、行指向ストア、オブジェクトストア、およびNoSQLストアは、バッチデータソースの典型的な例**です。
Batch data is read as structured data, and your batch program reads data from it using both a driver library (a dependency you often have to install) and connection details (the hostname/port, database, and credentials for authentication). 
バッチデータは構造化データとして読み取られ、バッチプログラムはドライバライブラリ（通常インストールする必要がある依存関係）と接続詳細（ホスト名/ポート、データベース、および認証のための資格情報）を使用してデータを読み取ります。

The most important batch data sources for building AI systems include: 
AIシステムを構築するための最も重要なバッチデータソースには以下が含まれます。

_Relational databases_ These store rows of data in tables.  
_リレーショナルデータベース_ これらはデータをテーブルに行として保存します。

_Object stores and filesystems_ These store data as files in directories. Files can contain either unstructured data (e.g., text in PDF files, images in PNG files) or structured data (e.g., JSON files or Parquet files in lakehouse tables).  
_オブジェクトストアとファイルシステム_ これらはデータをディレクトリ内のファイルとして保存します。ファイルには、非構造化データ（例：PDFファイル内のテキスト、PNGファイル内の画像）または構造化データ（例：レイクハウステーブル内のJSONファイルやParquetファイル）が含まれる場合があります。

_NoSQL data stores_ These are scalable operational data stores that store specialized types of data:  
_NoSQLデータストア_ これらは、特定の種類のデータを保存するスケーラブルな運用データストアです。

- Key-value stores (such as DynamoDB and Redis) are designed for low latency and scale. Clients can read values by providing one or more keys.  
  - キー-バリューストア（DynamoDBやRedisなど）は、低遅延とスケールのために設計されています。クライアントは1つまたは複数のキーを提供することで値を読み取ることができます。

- Document-oriented stores (such as OpenSearch and Elasticsearch) are designed for free-text search of text within documents.  
  - ドキュメント指向ストア（OpenSearchやElasticsearchなど）は、ドキュメント内のテキストのフリーテキスト検索のために設計されています。

- JSON-like document stores (such as MongoDB) are designed for low latency and scale, where clients can read and write JSON objects.  
  - JSONライクなドキュメントストア（MongoDBなど）は、低遅延とスケールのために設計されており、クライアントはJSONオブジェクトを読み書きできます。

- Graph databases (such as Neo4j) are designed to store and query data structured as a graph of nodes and edges.  
  - グラフデータベース（Neo4jなど）は、ノードとエッジのグラフとして構造化されたデータを保存およびクエリするために設計されています。

- Vector databases (such as Weaviate and Qdrant) are designed for similarity search on compressed data, where clients can store and search with vector embeddings.  
  - ベクトルデータベース（WeaviateやQdrantなど）は、圧縮データに対する類似性検索のために設計されており、クライアントはベクトル埋め込みを使用して保存および検索できます。

One significant difference among the batch data sources is whether they provide data with a schema (known as structured data or tabular data) or data that does not have a schema (called unstructured data).  
**バッチデータソース間の重要な違いの1つは、スキーマを持つデータ（構造化データまたは表形式データとして知られる）を提供するか、スキーマを持たないデータ（非構造化データと呼ばれる）を提供するか**です。
For example, PDF files contain text and images, but they do not have a schema.  
例えば、PDFファイルにはテキストと画像が含まれていますが、スキーマはありません。
Video and image data is also considered to be unstructured data.  
ビデオおよび画像データも非構造化データと見なされます。
In contrast, much of the data from both SQL and NoSQL data sources is structured/tabular data.  
対照的に、SQLおよびNoSQLデータソースのデータの多くは構造化/表形式データです。
A table in a relational database has a schema containing named/typed columns.  
リレーショナルデータベースのテーブルには、名前付き/型付きの列を含むスキーマがあります。
A JSON object contains (nested) key-value pairs, where the keys are strings and the values can be strings, numbers, objects, arrays, Booleans, or null.  
JSONオブジェクトには（ネストされた）キー-バリューペアが含まれており、キーは文字列で、値は文字列、数値、オブジェクト、配列、ブール値、またはnullである可能性があります。
An event in an event-streaming platform can either be a JSON object or have an Avro schema (like a table with named/typed columns).  
イベントストリーミングプラットフォームのイベントは、JSONオブジェクトであるか、Avroスキーマを持つことができます（名前付き/型付きの列を持つテーブルのように）。
A vector embedding has a data type (a floating-point number with a fixed number of dimensions).  
ベクトル埋め込みにはデータ型（固定次元数の浮動小数点数）が存在します。

<!-- ここまで読んだ! -->

Figure 8-2 shows a lakehouse as a batch data source for a batch or streaming feature pipeline.  
図8-2は、バッチまたはストリーミングフィーチャーパイプラインのためのバッチデータソースとしてのレイクハウスを示しています。

![]()
_Figure 8-2. Batch feature pipeline performing feature engineering on data from a batch_ _data source (a lakehouse table) and writing the feature data to a feature group in the_ _feature store._
_Figure 8-2. バッチフィーチャーパイプラインがバッチデータソース（レイクハウステーブル）からデータに対してフィーチャーエンジニアリングを行い、フィーチャーデータをフィーチャーストアのフィーチャーグループに書き込む。_

The lakehouse table is stored in daily partitions, and when the batch program runs once per day, it reads and processes only yesterday’s data, bounding the amount of data that needs to be processed.
**レイクハウステーブルは日次パーティションに保存されており、バッチプログラムが1日1回実行されると、昨日のデータのみを読み込み処理し、処理する必要のあるデータの量を制限**します。(静的なエンティティデータも日次でパーティション切られてた方がいいのかな...!!:thinking:)
When the batch program backfills from historical data, it will need more resources as it will read and process many more partitions of data. 
**バッチプログラムが履歴データからバックフィルを行うときは、より多くのリソースが必要になります。なぜなら、より多くのデータパーティションを読み込み処理するからです。** (わかるよ〜:thinking:)
If the size of a batch exceeds the memory or processing capacity of a single machine, you will need to use a distributed batch-processing program, such as PySpark, that can scale up to process larger batches using many parallel workers. 
バッチのサイズが単一のマシンのメモリまたは処理能力を超える場合は、PySparkのような分散バッチ処理プログラムを使用する必要があります。これにより、多くの並列ワーカーを使用してより大きなバッチを処理することができます。
An alternative is to rerun the batch program for every partition, but this will be an order of magnitude slower than using PySpark. 
**別の方法は、すべてのパーティションに対してバッチプログラムを再実行することですが、これはPySparkを使用するよりも桁違いに遅くなります。** 
(こうやって順番にbackfillするよりも、並列化できるならした方が高速だよね...!:thinking:)
For this reason, my advice is to choose a batch-processing framework that meets your maximum expected load during backfilling.
このため、私のアドバイスは、バックフィル中の最大予想負荷に対応するバッチ処理フレームワークを選択することです。
You won’t have the same resource challenges when backfilling with a streaming program, as they process data incrementally. 
ストリーミングプログラムでバックフィルを行う場合は、データをインクリメンタルに処理するため、同じリソースの課題はありません。
Note that they exit immediately after finishing backfilling. 
バックフィルを完了した後、すぐに終了することに注意してください。

<!-- ここまで読んだ! -->

In this example, the batch feature pipeline is an ETL program. 
この例では、バッチフィーチャーパイプラインはETLプログラムです。
However, if you have a SQL data source, you can create features by pushing SQL queries down to the database or data warehouse. 
ただし、SQLデータソースがある場合は、SQLクエリをデータベースまたはデータウェアハウスにプッシュすることでフィーチャーを作成できます。
This works fine if the data sink for the features is only the offline store. 
フィーチャーのデータシンクがオフラインストアのみである場合、これは問題ありません。
For example, in Hopsworks an external feature group can be a table in an external lakehouse. 
たとえば、Hopsworksでは、外部フィーチャーグループは外部レイクハウスのテーブルである可能性があります。
However, if you need to load the feature data into the online store or vector index, an ETL program is needed. 
ただし、フィーチャーデータをオンラインストアまたはベクトルインデックスにロードする必要がある場合は、ETLプログラムが必要です。

The advice here for partitioning holds for columnar stores, but it does not translate to operational databases as batch data sources. 
ここでのパーティショニングに関するアドバイスはカラムストアに当てはまりますが、バッチデータソースとしての運用データベースには当てはまりません。
For row-oriented data stores, partitioning of data by time interval is less common. 
行指向データストアでは、時間間隔によるデータのパーティショニングはあまり一般的ではありません。
Instead, indexes can be defined over columns in the table to speed up read queries. 
その代わりに、テーブル内の列にインデックスを定義して読み取りクエリを高速化できます。
If you want to backfill from a row-oriented table, it should have a timestamp column (event time) and you should have an index on that column; otherwise, incremental and backfill runs will read all records in the table. 
行指向テーブルからバックフィルを行いたい場合は、タイムスタンプ列（イベント時間）を持ち、その列にインデックスを持っている必要があります。そうでないと、インクリメンタルおよびバックフィルの実行はテーブル内のすべてのレコードを読み取ります。
This is known as a _full table scan and should be avoided at all_ costs. 
**これはフルテーブルスキャンとして知られ、あらゆるコストで回避すべきです。**
It can consume so many resources in the database that it jeopardizes the database’s ability to serve other concurrent clients. 
これにより、データベース内のリソースが消費されすぎて、他の同時クライアントにサービスを提供するデータベースの能力が危険にさらされる可能性があります。

<!-- ここまで読んだ! -->

### 2.2. Streaming Data Sources　ストリーミングデータソース

_Event streams are continuous data sources and building blocks for real-time ML sys‐_ _tems. 
イベントストリームは連続データソースであり、リアルタイムMLシステムの構成要素です。
Event-streaming platforms are stores for event data, transporting events between a producer and a consumer. 
イベントストリーミングプラットフォームはイベントデータのストレージであり、プロデューサーとコンシューマーの間でイベントを輸送します。(ex. AWSでいうと、Kinesisとか?)
For example, the producer could be an application or a service, while the consumer could be a streaming or batch feature pipeline (see Figure 8-3). 
たとえば、**プロデューサーはアプリケーションやサービスであり、コンシューマーはストリーミングまたはバッチフィーチャーパイプライン**である可能性があります（図8-3を参照）。

![]()
_Figure 8-3. Streaming feature pipelines continuously consume events from an event-_ _streaming platform, compute features, and write the computed features to the feature_ _store. Batch feature pipelines can also compute features from event stream sources._ 
_Figure 8-3. ストリーミングフィーチャーパイプラインは、イベントストリーミングプラットフォームからイベントを継続的に消費し、フィーチャーを計算し、計算されたフィーチャーをフィーチャーストアに書き込みます。バッチフィーチャーパイプラインもイベントストリームソースからフィーチャーを計算できます。_

Event streams are continuously processed as unbounded (potentially infinite) input data, and the output features written to the feature store are also unbounded in size. 
イベントストリームは、無限の可能性を持つ入力データとして継続的に処理され、フィーチャーストアに書き込まれる出力フィーチャーもサイズに制限がありません。
The most popular event-streaming platforms for storing and publishing events are Apache Kafka, RabbitMQ, Amazon Kinesis, Google Cloud Pub/Sub, and Azure Event Hubs. 
イベントを保存および公開するための最も人気のあるイベントストリーミングプラットフォームは、Apache Kafka、RabbitMQ、Amazon Kinesis、Google Cloud Pub/Sub、およびAzure Event Hubsです。

Apache Kafka is a popular open source event-streaming platform that stores events created by producers in a queue called a _topic. 
Apache Kafkaは、プロデューサーによって作成されたイベントをトピックと呼ばれるキューに保存する人気のあるオープンソースのイベントストリーミングプラットフォームです。
Consumers can listen to a topic for new events and process them as they become available. 
コンシューマーはトピックで新しいイベントをリッスンし、利用可能になるとそれらを処理できます。
Consumers can also reconnect to a topic and read all events that arrived since the last time they (the consum‐ ers) were connected. 
コンシューマーはトピックに再接続し、前回接続してから到着したすべてのイベントを読み取ることもできます。
For example, Spark Structured Streaming applications can run continuously, consuming events from a Kafka topic, computing features, and writing 
たとえば、Spark Structured Streamingアプリケーションは継続的に実行され、Kafkaトピックからイベントを消費し、フィーチャーを計算し、書き込みます。
them to the feature store. 
それらをフィーチャーストアに。
Similarly, a PySpark batch application can run on a sched‐ ule, consume the latest events that have arrived on the topic, compute features, write them to the feature store, and then exit. 
同様に、PySparkバッチアプリケーションはスケジュールに従って実行され、トピックに到着した最新のイベントを消費し、フィーチャーを計算し、それらをフィーチャーストアに書き込み、その後終了します。
If your AI system requires fresh feature data from the event stream source, you should write a streaming feature pipeline (see Chapter 9), and if it doesn’t have strict feature freshness requirements, a batch feature pipeline may be easier to operate and more efficient to run. 
**AIシステムがイベントストリームソースから新鮮なフィーチャーデータを必要とする場合は、ストリーミングフィーチャーパイプラインを書くべき**です（第9章を参照）。**厳密なフィーチャーの新鮮さの要件がない場合は、バッチフィーチャーパイプラインの方が操作が簡単で、効率的に実行できる**かもしれません。
(うんうん! だから基本的には、「まずはバッチシステムで要件を満たせるか??」を考えるのが良いよね...!:thinking:)

### 2.3. Unstructured Data in Object Stores and Filesystems オブジェクトストアとファイルシステムの非構造化データ

Text data, image data, video data, and much scientific data (such as medical imaging data and Earth observation data) are collectively called _unstructured data. 
テキストデータ、画像データ、ビデオデータ、および多くの科学データ（医療画像データや地球観測データなど）は、総称して非構造化データと呼ばれます。
It is unstructured as it lacks a schema—that is, it is not tabular data with typed columns. 
これはスキーマが欠如しているため非構造化であり、すなわち型付き列を持つ表形式データではありません。
Unstructured data is typically stored as files in either an object store or a filesystem. 
非構造化データは通常、オブジェクトストアまたはファイルシステムのいずれかにファイルとして保存されます。

Batch feature pipelines that process unstructured data as files are run on a time-based schedule or can be triggered by an alert that new files are available for processing. 
**非構造化データをファイルとして処理するバッチフィーチャーパイプラインは、時間ベースのスケジュールで実行されるか、新しいファイルが処理可能であるというアラートによってトリガーされる**ことがあります。
Object stores and some filesystems provide a CDC API to provide such notifications. 
オブジェクトストアや一部のファイルシステムは、そのような通知を提供するCDC APIを提供します。
Figure 8-4 shows the files in the object store organized into time-stamped directories to enable efficient backfilling and incremental processing. 
Figure 8-4は、オブジェクトストア内のファイルがタイムスタンプ付きのディレクトリに整理されており、効率的なバックフィルとインクリメンタル処理を可能にしていることを示しています。
For example, if the batch program is parameterized with the latest date for files already processed, it can prune the files it processes to those directories containing files added after the provided date. 
たとえば、**バッチプログラムが既に処理されたファイルの最新の日付でパラメータ化されている場合、提供された日付以降に追加されたファイルを含むディレクトリに処理するファイルを絞り込むことができます**。

<!-- ここまで読んだ! -->

_Figure 8-4. Incremental preprocessing of unstructured data. Typically, this is done in_ _batch jobs. For text documents and LLMs, you can clean text, update vector indexes,_ _and create instruction datasets for fine-tuning. For image processing, you can clean_ _images, augment them, and create training/inference tensor data (e.g., TFRecord files)_ _from them._ 
_Figure 8-4. 非構造化データのインクリメンタル前処理。通常、これはバッチジョブで行われます。テキスト文書やLLMの場合、テキストをクリーンアップし、ベクトルインデックスを更新し、ファインチューニング用の指示データセットを作成できます。画像処理の場合、画像をクリーンアップし、拡張し、トレーニング/推論用のテンソルデータ（例：TFRecordファイル）を作成できます。_

Audio, video, and image data are typically stored as compressed files in a filesystem or object store. 
音声、ビデオ、および画像データは通常、ファイルシステムまたはオブジェクトストアに圧縮ファイルとして保存されます。
Batch feature pipelines transform these files into new files as well as rows in feature groups. 
バッチフィーチャーパイプラインは、これらのファイルを新しいファイルおよびフィーチャーグループ内の行に変換します。
The new files, stored in the object store, can contain tensor data (such as TFRecord files for training and inference) or new files containing augmented/transformed/cleaned data. 
オブジェクトストアに保存された新しいファイルは、テンソルデータ（トレーニングおよび推論用のTFRecordファイルなど）や、拡張/変換/クリーンアップされたデータを含む新しいファイルを含むことができます。
Metadata can be extracted from the image/video/audio files, and vector embeddings can be computed from them, and this tabular data can be stored in feature groups. 
**メタデータは画像/ビデオ/音声ファイルから抽出でき、ベクトル埋め込みを計算でき、この表形式データはフィーチャーグループに保存できます。**
As such, feature groups can be used to index audio, video, and image data, enabling similarity search with the vector index and filtering/lookup with metadata columns. 
そのため、フィーチャーグループは音声、ビデオ、および画像データをインデックス化するために使用でき、ベクトルインデックスを使用した類似検索やメタデータ列を使用したフィルタリング/ルックアップを可能にします。

<!-- ココまで読んだ! -->

Text data is widely used in AI systems for _natural language processing (NLP) and_ LLMs, with examples of massively popular AI-powered services including Google Translate and OpenAI’s ChatGPT. 
テキストデータは、自然言語処理（NLP）やLLMのためにAIシステムで広く使用されており、Google翻訳やOpenAIのChatGPTなどの非常に人気のあるAI駆動サービスの例があります。
The text data (and now also image data) used to [train LLMs is massive—“Llama 3 is pretrained on over 15T tokens that were all col‐](https://oreil.ly/9NgTG) lected from publicly available sources,” consisting of hundreds of millions of text files or more. 
LLMをトレーニングするために使用されるテキストデータ（そして現在は画像データも）は膨大です。「Llama 3は、すべて公開されているソースから収集された15Tトークン以上で事前トレーニングされています。」これは数億のテキストファイル以上で構成されています。
This includes HTML, PDF, MD, and other file formats. 
これにはHTML、PDF、MD、およびその他のファイル形式が含まれます。
Batch feature pipelines can transform these text files into chunks of text stored as columns in feature groups. 
バッチフィーチャーパイプラインは、これらのテキストファイルをフィーチャーグループの列として保存されるテキストのチャンクに変換できます。
For example, you could extract paragraphs of text from PDF files and, for every paragraph, add to separate columns in your feature group the source filename, page number, paragraph number, and a vector embedding for the paragraph text. 
**たとえば、PDFファイルからテキストの段落を抽出し、各段落について、フィーチャーグループの別々の列にソースファイル名、ページ番号、段落番号、および段落テキストのベクトル埋め込みを追加できます。**
Then, you could easily search for paragraphs with free-text search using the vector index. 
その後、ベクトルインデックスを使用してフリーテキスト検索で段落を簡単に検索できます。
You could make the filename, page number, and paragraph number as a primary key, enabling filtering and fast lookup for text. 
ファイル名、ページ番号、および段落番号を主キーとして設定することで、テキストのフィルタリングと迅速なルックアップを可能にできます。

<!-- ここまで読んだ! -->

### 2.4. API and SaaS Sources　APIおよびSaaSソース

With the emergence of SaaS and microservice architectures, an increasing amount of enterprise data is only accessible via APIs, often HTTP/REST APIs. 
SaaSおよびマイクロサービスアーキテクチャの出現により、企業データの増加は、しばしばHTTP/REST APIを介してのみアクセス可能です。
Popular enterprise SaaS APIs include Salesforce and HubSpot, where many enterprises store their sales and marketing data, respectively. 
人気のある企業向けSaaS APIにはSalesforceやHubSpotがあり、多くの企業がそれぞれの販売およびマーケティングデータを保存しています。
In general, API sources are not a great fit for feature pipelines, as popular technologies for feature pipelines (such as Spark and Python) often have to issue blocking REST calls that slow down feature pipelines. 
**一般的に、APIソースはフィーチャーパイプラインに適していません。なぜなら、フィーチャーパイプラインのための人気のある技術（SparkやPythonなど）は、しばしばフィーチャーパイプラインを遅くするブロッキングREST呼び出しを発行しなければならないから**です。
A more common architectural pattern in industry is to have historical data scraped from APIs first written to a data warehouse or event-streaming platform by a data integration platform. 
業界でより一般的なアーキテクチャパターンは、APIからスクレイピングされた履歴データが、データ統合プラットフォームによって最初にデータウェアハウスまたはイベントストリーミングプラットフォームに書き込まれることです。
Data integration platforms are ETL or ELT tools that can backfill and incrementally copy data from hundreds of data sources to centralized data platforms, such as lakehouses. 
データ統合プラットフォームは、ETLまたはELTツールであり、数百のデータソースから中央集約型データプラットフォーム（レイクハウスなど）にデータをバックフィルおよびインクリメンタルにコピーできます。
Popular open source data integration platforms include [dltHub and Airbyte. 
人気のあるオープンソースのデータ統合プラットフォームには、dltHubやAirbyteが含まれます。
However, there may be use cases where the source data used to](https://oreil.ly/HMvVO) compute online features must be retrieved via a (HTTP) API at runtime. 
ただし、オンラインフィーチャーを計算するために使用されるソースデータをランタイムで（HTTP）APIを介して取得する必要があるユースケースもあります。
For these cases, feature stores provide support for ODTs that can read the source data from the API and create the feature(s) at request time. 
これらのケースでは、フィーチャーストアはAPIからソースデータを読み取り、リクエスト時にフィーチャーを作成できるODTをサポートします。

<!-- ここまで読んだ! -->

## 3. Synthetic Credit Card Data with LLMs　LLMを用いた合成クレジットカードデータ

Now that we have introduced the common data sources, we will build the data mart for our credit card fraud prediction system. 
一般的なデータソースを紹介したので、クレジットカード詐欺予測システムのためのデータマートを構築します。
Synthetic data is gaining adoption as a data source for building and experimenting with AI systems, particularly in regulated industries, where real data may be scarce or there are restrictions on working with privacy-sensitive data. 
合成データは、特に実データが不足しているか、プライバシーに敏感なデータの取り扱いに制限がある規制産業において、AIシステムの構築や実験のためのデータソースとして採用が進んでいます。
Many companies now provide synthetic data for purchase in such regulated industries. 
多くの企業が、こうした規制産業向けに合成データを販売しています。
Synthetic data is also increasingly being used to train LLMs, as they are hitting a scaling wall, having used up all globally available text data‐ sets as training data. 
合成データは、LLMのトレーニングにもますます使用されており、これまでに利用可能なすべてのテキストデータセットをトレーニングデータとして使い果たしたため、スケーリングの壁に直面しています。

<!-- ここまで読んだ! -->

### 3.1. A Logical Model for the Data Mart and the LLM　データマートとLLMのための論理モデル

Currently, there are no high-quality public datasets containing credit card transaction data with which to build our fraud detection system. 
現在、私たちの詐欺検出システムを構築するためのクレジットカード取引データを含む高品質の公開データセットは存在しません。
For reasons of data privacy, credit card issuers do not make credit card transaction details public. 
データプライバシーの理由から、クレジットカード発行会社はクレジットカード取引の詳細を公開していません。
To overcome this, we will generate synthetic data using an LLM and some domain knowledge I have from working on problems in this space. 
**これを克服するために、私たちはLLMを使用して合成データを生成し、この分野での問題に取り組んできた経験から得たドメイン知識を活用**します。

First, we need to describe clearly the synthetic data we want to create. 
まず、私たちが作成したい合成データを明確に説明する必要があります。
LLMs will fill in any gaps if your description is ambiguous, which is an easy trap to fall into with natural language. 
LLMは、説明があいまいな場合にギャップを埋めてくれますが、これは自然言語で陥りやすい罠です。
What we will do instead of using natural language is define a _logical_ _model for the credit card data mart and ask the LLM to create the synthetic data for_ that logical model. 
**私たちが自然言語を使用する代わりに行うのは、クレジットカードデータマートのための_論理モデル_を定義し、その論理モデルのためにLLMに合成データを作成するよう依頼すること**です。
The logical model is an extension of the entity-relationship (ER) diagram from Figure 4-8. 
論理モデルは、図4-8のエンティティ-リレーションシップ（ER）ダイアグラムの拡張です。
Defining a logical model is a typical step in database design after conceptual design, but before you create the actual tables (the physical model). 
論理モデルを定義することは、概念設計の後、実際のテーブル（物理モデル）を作成する前のデータベース設計における典型的なステップです。
The logical model adds details on columns—their data type, cardinality, and distribution, and whether they are primary keys or foreign keys. 
論理モデルは、列の詳細（データ型、基数、分布、主キーまたは外部キーであるかどうか）を追加します。
We will also add details to the tables, such as a description and how many rows it should contain. 
また、テーブルに対して、説明や含むべき行数などの詳細も追加します。

After adding our logical model to the LLM’s prompt, we will ask it to write code to create synthetic data for the tables and store that data in feature groups in Hops‐ works. 
**論理モデルをLLMのプロンプトに追加**した後、テーブルの合成データを作成するためのコードを書かせ、そのデータをHopsworksのフィーチャーグループに保存するよう依頼します。
Our logical model is a comprehensive description of the tables, including:
私たちの論理モデルは、テーブルの包括的な説明であり、以下を含みます：

- The name and description of the table, including the number of rows
  - テーブルの名前と説明、行数を含む
- The name, data type, and description of each column in the table
  - テーブル内の各列の名前、データ型、および説明
- If a column is an index column, one of the following types: primary key, foreign key (including the relationship: one-to-one or one-to-many), partition key, or event time
  - 列がインデックス列である場合、次のいずれかのタイプ：主キー、外部キー（関係：一対一または一対多を含む）、パーティションキー、またはイベント時間
- If the column is a categorical variable, a listing of all of the categories (including their relative percentage distribution)
  - 列がカテゴリ変数である場合、すべてのカテゴリのリスト（相対的なパーセンテージ分布を含む）
- The cardinality of a column (the number of unique values present in that column)
  - 列の基数（その列に存在するユニークな値の数）
- The shape of the distribution of values in a numerical column
  - 数値列の値の分布の形状
- The format of dates and timestamps (for example, a credit card expiry date includes only the year and month)
  - 日付とタイムスタンプの形式（例えば、クレジットカードの有効期限は年と月のみを含む）
- Any missing values (including what percentage of values are null)
  - 欠損値（値がnullである割合を含む）

We need to define a logical model for the five tables in our data mart as well as the ``` cc_fraud table containing the labels. 
私たちは、データマート内の5つのテーブルと、ラベルを含む``` cc_fraudテーブルの論理モデルを定義する必要があります。
An example of the logical model for one of six tables is shown here. 
6つのテーブルのうちの1つの論理モデルの例がここに示されています。
The other logical models can be found in the book’s source code repository. 
他の論理モデルは、書籍のソースコードリポジトリにあります。

```md
**Merchant Details:**
**Name:** `merchant_details`
**Description: Details about merchants that execute transactions.**
**Size: 5,000 rows**
**Columns:**
**商人の詳細:**
**名前:** `merchant_details`
**説明: 取引を実行する商人に関する詳細。**
**サイズ: 5,000行**
**列:**
- merchant_id: string (primary key)
- merchant_id: 文字列（主キー）
— Description: Unique identifier for each merchant
— 説明: 各商人のユニークな識別子
— Cardinality: 5,000 unique merchants
— 基数: 5,000のユニークな商人
- last_modified: datetime (primary key)
- last_modified: 日時（主キー）
— Distribution: uniform 0 to 3 years before the current date
— 分布: 現在の日付の3年前から0年までの均一分布
- country: string
- country: 文字列
— Description: Country where merchant resides
— 説明: 商人が居住する国
— Cardinality: 160 largest countries in the world, excluding North Korea
— 基数: 北朝鮮を除く世界の160の大国
- cnt_chrgeback_prev_day: decimal(10,2)
- cnt_chrgeback_prev_day: decimal(10,2)
— Description: Number of chargebacks for this merchant during the previous day (Monday–Sunday)
— 説明: 前日（月曜日から日曜日）にこの商人に対して発生したチャージバックの数
```

We now craft a prompt for the LLM to ask it to create the tables as DataFrames and use _Polars, instead of Pandas, as it scales better for generating millions of rows of_ data.  
私たちは今、LLMにテーブルをDataFrameとして作成するよう依頼するプロンプトを作成し、_Pandasの代わりにPolarsを使用します。Polarsは数百万行のデータを生成するのにスケールが優れています。  

<!-- ここまで読んだ! -->

### 3.2. LLM Prompts to Generate the Synthetic Data

I tested on the following prompt on GPT 4.1, and it creates a Python program that generates the synthetic data for our tables:
私はGPT 4.1で次のプロンプトをテストし、テーブルの合成データを生成するPythonプログラムを作成しました：

```
Below these instructions, you will find 6 different logical models for database tables. Write a Polars program to generate the data for these tables as DataFrames. Try to use Polars expressions for efficiency. If you can’t, it’s ok to use the Faker library. Write the DataFrames you created to new feature groups that you create in Hopsworks.
<PASTE THE LOGICAL MODELS FOR THE 6 TABLES HERE>

```

The Python program output by our LLM creates the DataFrames in the following order:

1. The leaf nodes in our snowflake schema data model: account_details, bank_details, and merchant_details
2. The inner nodes (in order from lowest to highest): card_details
3. The root node: credit_card_transactions and then its dependent cc_fraud

The synthetic data does not include any fraudulent transactions. We need to add some fraudulent transactions to the tables so our model can learn to identify them. For this, we can write a prompt such as the following:

```
Write a loop that repeats 1,000 times. Select a random credit card number from the card_details, and create a fraudulent transaction for that card that represents a geo‐ graphic attack—where the location of the IP addresses is so far apart and the time between the transactions is so low that the card holder could not realistically travel between the two locations within the time between the transactions. The card_present field should be true for the transaction and cc_fraud should add it as a row.
Select another random credit card number from the card_details, and create a fraudu‐ lent transaction for that card where the card is used to make many small payments (between 5 and 50) within a short period of time (between 15 minutes and 1 hour). Add the transaction as a fraudulent transaction in cc_fraud.
```

Now we have some synthetic data for historical credit card transactions. We want to simulate updates to our data mart. Account, bank, and merchant details tables will be updated overnight as a batch job (they are slowly changing dimensions). The outline of a prompt for our LLM that generates a Polars program that runs daily is as follows:

```
Write a Polars program to read the contents of the credit_card_transactions feature group for the previous day as a Polars DataFrame. Then read all of the contents of the bank_details, card_details, account_details, and merchant_details feature groups.
Then modify the DataFrames as follows and save them back as updates to feature groups in Hopsworks:
Keep 0.001% of the cards rows with card status ‘Active’ and change that status to either ‘Blocked’ or ‘Lost/Stolen’ (choose uniformly at random). For the transactions table, group them by merchants, sum the amount of transactions for each merchant and then multiply that number by a uniform random number between 0.01% and 0.1%. The result is cnt_chrgeback_prev_day for that merchant. Update the merchants_fg with the new value result for cnt_chrgeback_prev_day and also update last_modified to the cur‐ rent time.
```

You should schedule the resultant program to run once per day; see the book’s source code repository. Finally, you need to prompt your LLM to generate a Python program that runs continuously, writing synthetic credit card transactions to the Apache Kafka topic in your data mart. Again, see the book’s source code repository for details.

<!-- ここまで読んだ! -->

## 4. Backfilling and Incremental Updates バックフィルとインクリメンタル更新

With our new synthetic data generation programs, we can now run them to:
私たちの新しい合成データ生成プログラムを使用して、次のことを実行できます：

• Create historical data for our data mart, including fraudulent transactions.
• Update the slowly changing tables daily.
• Continuously add new credit card transactions to Apache Kafka.

We will use this synthetic data to create feature data for our feature groups, using the transformations from Chapters 6 and 7. In Chapter 9, we will look at streaming fea‐ ture pipelines that update the cc_trans_aggs_fg feature group. Now, we focus on the batch feature pipelines containing the MITs.

---
(コラム)
In data engineering, the term full load is often used instead of back‐ filling, and incremental load is preferred to incremental processing. A full load drops an existing table and then recomputes its data from the data source(s). With the adoption of lakehouse tables that support updates and deletes (not just appends), full loads have become less common. We prefer the term backfilling over full loads, as it is a more expansive term that covers recomputing all feature data (full loads) as well as recomputing missing data.
---

We start by backfilling our feature groups. You backfill when you create new feature data from historical data. This may be because you have no existing data in your fea‐ ture group and you need feature data to train a model, or because there are gaps in your production feature data due to an upstream data failure or a maintenance window. After backfilling your feature groups for the first time, you need to keep your feature groups up-to-date by processing newly arrived or changed data. 
ウィンドウ。最初にフィーチャーグループをバックフィルした後は、新しく到着したデータや変更されたデータを処理することでフィーチャーグループを最新の状態に保つ必要があります。

We will use incremental processing to process only the data that has changed since the most recent run of a batch feature pipeline. 
私たちは、バッチフィーチャーパイプラインの最も最近の実行以降に変更されたデータのみを処理するために、インクリメンタル処理を使用します。

Incremental processing is an efficient mechanism for processing any newly arrived data, allowing for frequent and manageable updates. 
インクリメンタル処理は、新しく到着したデータを処理するための効率的なメカニズムであり、頻繁で管理可能な更新を可能にします。

Your batches of incremental data should be processed at a frequency that: 
インクリメンタルデータのバッチは、以下の頻度で処理されるべきです：

- Ensures that feature freshness requirements (or other SLOs) are met for your downstream training and inference pipelines 
- フィーチャーの新鮮さ要件（または他のSLO）が、下流のトレーニングおよび推論パイプラインに対して満たされることを保証します。

- Ensures that your batch pipeline processing capacity matches the rate of arrival of new data—that the pipeline is not overwhelmed with too much data for one time interval (causing out-of-memory errors or not processing data in time) or overpro‐ visioned with excessive CPU and memory resources for other time intervals. 
- バッチパイプラインの処理能力が新しいデータの到着率と一致することを保証します。つまり、パイプラインが一度の時間間隔に対して過剰なデータで圧倒されること（メモリエラーを引き起こしたり、データを時間内に処理できなかったりする）や、他の時間間隔に対して過剰なCPUおよびメモリリソースを持つことがないようにします。

###### 4.0.0.0.1. Polling and CDC for Incremental Data
###### 4.0.0.0.2. インクリメンタルデータのためのポーリングとCDC

When you run any feature pipeline against a data source, you need to identify the data it should process. 
データソースに対してフィーチャーパイプラインを実行する際には、処理すべきデータを特定する必要があります。

The two most common methods of identifying which data has changed in the data source are: 
データソース内でどのデータが変更されたかを特定する最も一般的な2つの方法は次のとおりです：

_Polling_ A user-defined column in each table containing the last modified timestamp for the row. 
_ポーリング_ 各テーブルにおいて、行の最終更新タイムスタンプを含むユーザー定義の列です。

This is essentially the event time for feature groups. 
これは本質的にフィーチャーグループのイベント時間です。

The batch program retrieves records with timestamps higher than its most recently processed row. 
バッチプログラムは、最も最近処理された行よりも高いタイムスタンプを持つレコードを取得します。

_Change data capture (CDC)_ A system-managed timestamp (and/or commit ID) storing the ingestion time for each row. 
_変更データキャプチャ（CDC）_ 各行の取り込み時間を保存するシステム管理のタイムスタンプ（および/またはコミットID）です。

System-managed timestamps/commits are usually exposed via a CDC API, where a client can read all the data that has changed since a particular com‐ mit ID or timestamp. 
システム管理のタイムスタンプ/コミットは通常CDC APIを介して公開され、クライアントは特定のコミットIDまたはタイムスタンプ以降に変更されたすべてのデータを読み取ることができます。

Many row-oriented and column-oriented databases—such as Postgres and Snowflake, respectively—support CDC APIs. 
多くの行指向および列指向のデータベース（PostgresやSnowflakeなど）は、CDC APIをサポートしています。

Even lakehouses, such as Apache Hudi, provide CDC APIs. 
Apache HudiのようなレイクハウスでもCDC APIを提供しています。

Your batch feature pipeline that performs incremental processing should use either polling or CDC. 
インクリメンタル処理を行うバッチフィーチャーパイプラインは、ポーリングまたはCDCのいずれかを使用する必要があります。

In general, CDC is preferable to polling, as polling can miss changes while CDC captures all changes. 
一般的に、CDCはポーリングよりも好ましいです。なぜなら、ポーリングは変更を見逃す可能性がある一方で、CDCはすべての変更をキャプチャするからです。

###### 4.0.0.0.3. Polling
###### 4.0.0.0.4. ポーリング

Polling is only used for batch data sources. 
ポーリングはバッチデータソースにのみ使用されます。

You define what data to read (with a query) and how often to run it against the data source (the _polling interval). 
どのデータを読み取るか（クエリを使用）と、データソースに対してどのくらいの頻度で実行するか（_ポーリング間隔_）を定義します。

The query should set a `start_time` and `end_time` for the event time index or partition key, so that only the requested data is read and returned to the client. 
クエリは、イベント時間インデックスまたはパーティションキーのために`start_time`と`end_time`を設定する必要があります。これにより、要求されたデータのみが読み取られ、クライアントに返されます。

Partition pruning is needed when you have large tables, as the alternative of the client reading all data and filtering out the new data will cause out-of-memory errors. 
大きなテーブルがある場合、パーティションプルーニングが必要です。クライアントがすべてのデータを読み取り、新しいデータをフィルタリングする代替手段は、メモリエラーを引き起こすからです。

For polling: 
ポーリングの場合：

- You need a default row fetch size to prevent out-of-memory errors. 
- メモリエラーを防ぐために、デフォルトの行取得サイズが必要です。

- Polling can miss updates to tables—for example, if a row is added and removed within a polling interval, polling will never see it. 
- ポーリングはテーブルの更新を見逃す可能性があります。たとえば、ポーリング間隔内に行が追加されて削除された場合、ポーリングはそれを決して見ることができません。

- Polling can also miss late-arriving data in columnar tables if the client only reads the most recent partition (hour/day), as late-arriving data may be stored in earlier partitions. 
- ポーリングは、クライアントが最新のパーティション（時間/日）しか読み取らない場合、列指向テーブルの遅れて到着したデータを見逃す可能性があります。遅れて到着したデータは、以前のパーティションに保存されている可能性があるからです。

###### 4.0.0.0.5. Change data capture
###### 4.0.0.0.6. 変更データキャプチャ

CDC resolves the problems of missing (or ghost) rows within a polling interval and late-arriving data. 
CDCは、ポーリング間隔内の欠落（またはゴースト）行や遅れて到着したデータの問題を解決します。

CDC APIs are built on change logs that contain immutable events for every insertion, deletion, or update event in the table or database. 
CDC APIは、テーブルまたはデータベース内のすべての挿入、削除、または更新イベントに対する不変のイベントを含む変更ログに基づいて構築されています。

For example, if you insert a row and then delete the same row, there will be two separate events in the CDC history. 
たとえば、行を挿入してから同じ行を削除すると、CDC履歴には2つの別々のイベントが記録されます。

Late-arriving data will also be events in the CDC history. 
遅れて到着したデータもCDC履歴のイベントとなります。

Most lakehouse tables (Apache Hudi, Delta Lake, and Apache Iceberg), cloud data warehouses (Snowflake, BigQuery, Redshift), and row-oriented databases (Postgres, MySQL) provide CDC APIs. 
ほとんどのレイクハウステーブル（Apache Hudi、Delta Lake、Apache Iceberg）、クラウドデータウェアハウス（Snowflake、BigQuery、Redshift）、および行指向データベース（Postgres、MySQL）はCDC APIを提供しています。

For example, in Hopsworks feature groups, you can read the changes in a feature group between a start_timestamp and an end_timestamp by using: 
たとえば、Hopsworksフィーチャーグループでは、次のようにしてstart_timestampとend_timestampの間のフィーチャーグループの変更を読み取ることができます：

```  
df = fg.asof(end_timestamp, exclude_until=start_timestamp).read()
```

###### 4.0.0.0.7. Backfill and Incremental Processing in One Program
###### 4.0.0.0.8. バックフィルとインクリメンタル処理を1つのプログラムで

A batch feature pipeline that is parameterized to be run against either historical data or incremental data requires abstracting out the data source, so that the query that reads from the data source can be given a start_time and an end_time for the range of data to be processed. 
歴史的データまたはインクリメンタルデータに対して実行されるようにパラメータ化されたバッチフィーチャーパイプラインは、データソースを抽象化する必要があります。これにより、データソースから読み取るクエリに対して処理するデータの範囲のためにstart_timeとend_timeを指定できます。

Apart from that difference, the same batch program should be able to process either historical or incremental data, assuming it has been provided enough resources (memory and compute). 
その違いを除けば、同じバッチプログラムは、十分なリソース（メモリと計算）が提供されていると仮定して、歴史的データまたはインクリメンタルデータのいずれかを処理できるはずです。

In Hopsworks, we can simplify the problem by mounting tables from databases, lakehouses, and data warehouses as external feature groups. 
Hopsworksでは、データベース、レイクハウス、データウェアハウスからのテーブルを外部フィーチャーグループとしてマウントすることで問題を簡素化できます。

The external feature group has a connector to an external data source, provides a schema for the data it can read with a query, and has an `event_time` column that we use to read a time range of data with polling. 
外部フィーチャーグループは外部データソースへのコネクタを持ち、クエリで読み取ることができるデータのスキーマを提供し、ポーリングでデータの時間範囲を読み取るために使用する`event_time`列を持っています。

When you read data from the external feature group, you specify the `start_time` and optionally an `end_time`. 
外部フィーチャーグループからデータを読み取るときは、`start_time`を指定し、オプションで`end_time`を指定します。

If you omit the `end_time`, it will read all available records with `event_time` values greater than the `start_time. 
`end_time`を省略すると、`start_time`よりも大きい`event_time`値を持つすべての利用可能なレコードを読み取ります。

If you omit both `start_time` and `end_time`, it will read all available data. 
`start_time`と`end_time`の両方を省略すると、すべての利用可能なデータを読み取ります。

The feature pipeline can be written in Pandas or Polars for data volumes that can be processed on a single machine. 
フィーチャーパイプラインは、単一のマシンで処理できるデータボリュームに対してPandasまたはPolarsで記述できます。

For larger data volumes, you should use PySpark. 
より大きなデータボリュームの場合は、PySparkを使用する必要があります。

The start and end times can be provided as command-line arguments or environment variables (shown here) when running the program: 
プログラムを実行する際に、startとendの時間はコマンドライン引数または環境変数（ここに示す）として提供できます：

```  
start_time = os.environ.get('START_TIME')  
end_time = os.environ.get('END_TIME')  
df = credit_card_transactions_fg.read(start_time=start_time, end_time=end_time)
```

There is one type of data transformation you do have to account for, though, when writing a batch feature pipeline that can process variable amounts of data—time window aggregations. 
ただし、可変量のデータを処理できるバッチフィーチャーパイプラインを書く際には、考慮しなければならないデータ変換の一種があります。それは、時間ウィンドウ集約です。

When you create time window aggregations, it is important to note that the batch of data you read for processing needs to be large enough to compute the windows, and you need to “slide” over the batch, computing new windows for every day in the batch. 
時間ウィンドウ集約を作成する際には、処理のために読み取るデータのバッチがウィンドウを計算するのに十分な大きさである必要があり、バッチ内の毎日について新しいウィンドウを計算するためにバッチを「スライド」させる必要があることに注意することが重要です。

For example, if you have read 30 days of data in your batch, for time windows with a length of 3 days, you can compute time window aggregations for only 28 days. 
たとえば、バッチ内で30日分のデータを読み取った場合、長さ3日の時間ウィンドウに対して、時間ウィンドウ集約を計算できるのは28日分のみです。

The oldest 2 days in the batch do not have the previous 3 days of transactions, so you can’t compute window aggregations for them. 
バッチ内の最も古い2日間には前の3日間のトランザクションがないため、それらに対してウィンドウ集約を計算することはできません。

So adjust your start and end times accordingly. 
したがって、start_timeとend_timeを適切に調整してください。

We move on now to look at orchestrators that manage the scheduling and execution of batch programs. 
次に、バッチプログラムのスケジューリングと実行を管理するオーケストレーターについて見ていきます。

Job schedulers support cron-based scheduling of batch programs, but sometimes you need more capable workflow schedulers to schedule and manage the execution of DAGs of programs (tasks). 
ジョブスケジューラーはバッチプログラムのcronベースのスケジューリングをサポートしますが、時にはプログラム（タスク）のDAGの実行をスケジュールおよび管理するために、より高機能なワークフロースケジューラーが必要です。

###### 4.0.0.0.9. Job Orchestrators
###### 4.0.0.0.10. ジョブオーケストレーター

In Chapter 3, we used GitHub Actions to run both a feature pipeline and a batch inference pipeline on a daily schedule. 
第3章では、GitHub Actionsを使用してフィーチャーパイプラインとバッチ推論パイプラインの両方を毎日スケジュールで実行しました。

The reason we used GitHub Actions is that it supports cron-based scheduling of Python programs with its free tier. 
GitHub Actionsを使用した理由は、無料プランでPythonプログラムのcronベースのスケジューリングをサポートしているからです。

It is not, how‐ ever, an orchestrator—it is a serverless DevOps platform. 
ただし、オーケストレーターではなく、サーバーレスDevOpsプラットフォームです。

An orchestrator is a service that schedules and coordinates the execution of programs with logging and fault tolerance. 
オーケストレーターは、プログラムの実行をスケジュールし、ログ記録とフォールトトレランスを持って調整するサービスです。

The goal of orchestration is to streamline and optimize the execution of fre‐ quent, repeatable processes and thus to help data teams more easily manage complex tasks and workflows. 
オーケストレーションの目標は、頻繁で繰り返し可能なプロセスの実行を合理化し最適化することであり、データチームが複雑なタスクやワークフローをより簡単に管理できるようにすることです。

A job orchestrator schedules the execution of Pandas/Polars/PySpark programs. 
ジョブオーケストレーターは、Pandas/Polars/PySparkプログラムの実行をスケジュールします。

There are many open source, serverless, and embedded job orchestrators you can choose from to manage the execution of your batch feature pipelines (and batch inference pipelines). 
バッチフィーチャーパイプライン（およびバッチ推論パイプライン）の実行を管理するために選択できる多くのオープンソース、サーバーレス、埋め込み型のジョブオーケストレーターがあります。

Job schedulers include more than just the ability to run programs. 
ジョブスケジューラーは、プログラムを実行する能力だけでなく、以下の機能も含まれます：

- A way to package your program with all its dependencies, for example, as containers 
- プログラムをすべての依存関係と共にパッケージ化する方法、たとえば、コンテナとして

- Support for one or more execution runtimes, for example, Kubernetes or AWS Fargate 
- 1つ以上の実行ランタイムのサポート、たとえば、KubernetesやAWS Fargate

- Support for executing and monitoring programs from different languages and frameworks, such as Pandas, Polars, and PySpark 
- Pandas、Polars、PySparkなど、異なる言語やフレームワークからプログラムを実行および監視するためのサポート

- Logs for execution runs 
- 実行のログ

Some job schedulers also provide resource monitoring for jobs, alerting for failed jobs, and retry of failed jobs. 
一部のジョブスケジューラーは、ジョブのリソース監視、失敗したジョブのアラート、および失敗したジョブの再試行も提供します。

The things you have to define for your job (or each execution) include: 
ジョブ（または各実行）に対して定義する必要があるものは次のとおりです：

- The program and its dependencies (or a container) to be executed 
- 実行されるプログラムとその依存関係（またはコンテナ）

- The program arguments and environment variables, such as the start_time and end_time for incremental processing 
- プログラム引数と環境変数、たとえば、インクリメンタル処理のためのstart_timeとend_time

- The resources requested (number of CPUs, number of GPUs, and amount of memory) 
- 要求されるリソース（CPUの数、GPUの数、メモリの量）

If the job is a Python program, you need either the Python program and its depen‐ dencies (requirements.txt file) or the program packaged as a container. 
ジョブがPythonプログラムである場合、Pythonプログラムとその依存関係（requirements.txtファイル）またはプログラムをコンテナとしてパッケージ化する必要があります。

If your job is a PySpark job, you will also need to define any files that need to be distributed with the program, such as JAR files, Python modules, and drivers. 
ジョブがPySparkジョブである場合、JARファイル、Pythonモジュール、ドライバーなど、プログラムと共に配布する必要があるファイルも定義する必要があります。

We will look now at two different job schedulers: Modal and Hopsworks. 
これから、2つの異なるジョブスケジューラー、ModalとHopsworksについて見ていきます。

###### 4.0.0.0.11. Modal
###### 4.0.0.0.12. モーダル

Modal is a developer-friendly serverless platform to deploy, schedule, and manage Python jobs. 
Modalは、Pythonジョブをデプロイ、スケジュール、および管理するための開発者に優しいサーバーレスプラットフォームです。

Modal supports automatic containerization. 
Modalは自動コンテナ化をサポートしています。

That is, there is no need to write and compile your own container images. 
つまり、自分のコンテナイメージを作成してコンパイルする必要はありません。

Instead, you add decorators to your Python functions to indicate: 
代わりに、Python関数にデコレーターを追加して次のことを示します：

- What family of Linux operating system you want to use (e.g., Debian) 
- 使用したいLinuxオペレーティングシステムのファミリー（例：Debian）

- How many resources the image will use (CPUs, GPUs, memory) 
- イメージが使用するリソースの量（CPU、GPU、メモリ）

- What pip-versioned Python libraries your function uses 
- 関数が使用するpipバージョンのPythonライブラリ

- How many instances of this function you want to execute in parallel 
- この関数を並行して実行したいインスタンスの数

- Where to read shared secrets from 
- 共有シークレットをどこから読み取るか

- A cron schedule for running the Python program 
- Pythonプログラムを実行するためのcronスケジュール



When you run a program for the first time, Modal will compile containers for it and cache them. 
プログラムを初めて実行すると、Modalはそのためのコンテナをコンパイルし、キャッシュします。

If you don’t make changes that invalidate your container images, subsequent program runs will have very fast startup times. 
コンテナイメージを無効にする変更を行わなければ、以降のプログラム実行は非常に速い起動時間を持ちます。

When you run a Modal program from the command line, `stdout and` `stderr for its containers are streamed` back to your console. 
コマンドラインからModalプログラムを実行すると、そのコンテナの`stdout`と`stderr`がコンソールにストリーミングされます。

Here is an example of a Modal-orchestrated batch feature pipeline that, once per day, downloads weather data and writes it as a Pandas DataFrame to Hopsworks: 
以下は、Modalによって調整されたバッチフィーチャーパイプラインの例で、1日1回、天気データをダウンロードし、それをPandas DataFrameとしてHopsworksに書き込むものです：

```   
   import modal   
   image = modal.Image.debian_slim(python_version="3.12").pip_install("hopsworks")   
   secret = modal.Secret.from_name(     
     "hopsworks-secret",     
     required_keys=["HOPSWORKS_API_KEY"],   
   )   
   app = modal.App("hopsworks-feature-group")   
   @app.function(     
     schedule=modal.Period(days=1),     
     image=image,     
     cpu=4.0,     
     memory=8192,     
     secrets=[secret]   
   )   
   def daily_hopsworks_job():     
     import hopsworks     
     import pandas as pd     
     fs = hopsworks.login().get_feature_store()     
     weather_forecast_df = # call remote API     
     fg = fs.get_feature_group(name="weather", version=1)     
     fg.insert(weather_forecast_df)   
   if __name__ == "__main__":     
     app.deploy()
``` 

Modal programs are opinionated, fast to start, and easy to debug with logs going to `stdout and stderr. 
Modalプログラムは意図が明確で、起動が速く、`stdout`と`stderr`にログが出力されるため、デバッグが容易です。

All the dependencies are defined in your Python program, and with _automatic containerization (see_ Chapter 13), Modal manages the packaging of your program and its execution as a container on your behalf. 
すべての依存関係はPythonプログラム内で定義されており、_自動コンテナ化（第13章を参照）_により、Modalはプログラムのパッケージングとその実行をあなたの代わりにコンテナとして管理します。

Modal charges based on compute/memory/GPU used per second. 
Modalは、使用したコンピュート/メモリ/GPUに基づいて課金されます。

###### 4.0.0.0.13. Hopsworks Jobs
Hopsworks jobs run on the same Kubernetes cluster Hopsworks is installed on and can be Python (Pandas, Polars, etc.) or PySpark batch programs. 
Hopsworksジョブは、Hopsworksがインストールされている同じKubernetesクラスター上で実行され、Python（Pandas、Polarsなど）またはPySparkバッチプログラムであることができます。

Hopsworks jobs are not available on Hopsworks Serverless, which is used by this book, but they are available on the commercial offering. 
Hopsworksジョブは、この本で使用されているHopsworks Serverlessでは利用できませんが、商業版では利用可能です。

Jobs are executed as containers in the same Kubernetes namespace as is used by the Hopsworks project your job belongs to. 
ジョブは、あなたのジョブが属するHopsworksプロジェクトで使用されるのと同じKubernetesネームスペース内でコンテナとして実行されます。



Modal, Hopsworks supports automatic containerization, and there is no need to compile (Docker) containers, as Hopsworks builds them in the background when you install/remove Python dependencies from one of the many different Python environ‐ ments in your project. 
Modalでは、Hopsworksが自動コンテナ化をサポートしており、（Docker）コンテナをコンパイルする必要はありません。Hopsworksは、プロジェクト内のさまざまなPython環境のいずれかからPython依存関係をインストール/削除するときに、バックグラウンドでそれらを構築します。

You can customize one of the feature, training, or inference base container images by using the Hopsworks UI or API, and it can be reused by many different jobs. 
HopsworksのUIまたはAPIを使用して、機能、トレーニング、または推論の基本コンテナイメージの1つをカスタマイズでき、さまざまなジョブで再利用できます。

When you create a job, you need to specify:
ジョブを作成する際には、次のことを指定する必要があります：

- The program, its arguments, and the container image it will use
- プログラム、その引数、および使用するコンテナイメージ
- For PySpark jobs, any additional file dependencies or configuration parameters
- PySparkジョブの場合、追加のファイル依存関係や構成パラメータ
- Resources for the program (CPUs, GPUs, memory):
- プログラムのリソース（CPU、GPU、メモリ）：
— For Pandas/Polars jobs, this is the number of CPUs and amount of memory.
— Pandas/Polarsジョブの場合、これはCPUの数とメモリの量です。
— For PySpark jobs, you specify the CPUs and memory (for both the driver and the executors) and the number of executors (a static number or a dynamic number that scales up at runtime with increasing workload size).
— PySparkジョブの場合、CPUとメモリ（ドライバとエグゼキュータの両方）およびエグゼキュータの数（静的な数またはワークロードサイズの増加に伴ってランタイムでスケールアップする動的な数）を指定します。
- An optional cron schedule for running the program
- プログラムを実行するためのオプションのcronスケジュール

Here is an example of how to create and schedule a PySpark job in Hopsworks: 
以下は、HopsworksでPySparkジョブを作成し、スケジュールする方法の例です：

```  
job_api = hopsworks.login().get_job_api()  
spark_config = job_api.get_configuration('PYSPARK')  
spark_config['appPath'] = '/projects/ccfraud/Resources/f_pipeline.py'  
spark_config['spark.driver.memory'] = 2048  
spark_config['spark.driver.cores'] = 1  
spark_config['spark.executor.memory'] = 8192  
spark_config['spark.executor.cores'] = 1  
spark_config['spark.dynamicAllocation.maxExecutors']= 2  
spark_config['spark.dynamicAllocation.enabled'] = True  
job = job_api.create_job('my_spark_job', spark_config)  
job.schedule(     
    cron_expression="0 */5 * ? * * *",     
    start_time=datetime.datetime.now(tz=timezone.utc)   
)  
job.save()  
execution = job.run()  
print(execution.success)  
out_log_path, err_log_path = execution.download_logs()
```

Many workflow orchestrators, such as Airflow, capture and visual‐ ize lineage information for the DAGs they compute. 
Airflowなどの多くのワークフローオーケストレーターは、計算するDAGの系譜情報をキャプチャし、可視化します。

Job orchestra‐ tors often delegate DAG visualization to the data processing framework. 
ジョブオーケストレーターは、DAGの可視化をデータ処理フレームワークに委任することがよくあります。

For example, PySpark supports DAG visualization, but Polars, Pandas, and DuckDB do not. 
たとえば、PySparkはDAGの可視化をサポートしていますが、Polars、Pandas、およびDuckDBはサポートしていません。

To overcome this, Hopsworks allows you to explicitly define lineage information when you create a feature group, by indicating in the parents parameter in the con‐ structor which feature groups are upstream of your current feature group. 
これを克服するために、Hopsworksでは、フィーチャーグループを作成する際に、コンストラクタのparentsパラメータで現在のフィーチャーグループの上流にあるフィーチャーグループを示すことによって、系譜情報を明示的に定義できます。

This lineage information is visualized in the Hopsworks UI and accessible via the Hopsworks API. 
この系譜情報はHopsworksのUIで可視化され、Hopsworks APIを介してアクセス可能です。

###### 4.0.0.0.14. Workflow Orchestrators
###### 4.0.0.0.15. ワークフローオーケストレーター

In contrast to job orchestrators that execute a single program, workflow orchestrators orchestrate the execution of many programs (or tasks), organized in a DAG. 
単一のプログラムを実行するジョブオーケストレーターとは対照的に、ワークフローオーケストレーターはDAGに整理された多くのプログラム（またはタスク）の実行を調整します。

Multi‐step workflows decompose batch feature pipelines into tasks with dependencies between the tasks, making it easy to schedule, execute, and monitor pipelines where tasks rely on the success or failure of previous steps. 
マルチステップワークフローは、バッチフィーチャーパイプラインをタスクに分解し、タスク間の依存関係を持たせることで、タスクが前のステップの成功または失敗に依存するパイプラインを簡単にスケジュール、実行、監視できるようにします。

Workflow orchestrators are use‐ ful for breaking down larger programs into smaller tasks and providing observability and support for retry when tasks fail. 
ワークフローオーケストレーターは、大きなプログラムを小さなタスクに分解し、タスクが失敗したときに観測性を提供し、再試行をサポートするのに役立ちます。

The tasks can also be implemented using differ‐ ent frameworks (Spark, Polars, dbt, etc.). 
タスクは、異なるフレームワーク（Spark、Polars、dbtなど）を使用して実装することもできます。

Often, however, a single program is good enough as a batch feature pipeline, and using a workflow orchestrator is typically overkill. 
しかし、しばしば単一のプログラムがバッチフィーチャーパイプラインとして十分であり、ワークフローオーケストレーターを使用することは通常過剰です。

For example, Polars and PySpark programs are also implemented as a DAG of transformations, and it is often faster and more resource efficient to execute a sin‐ gle program than a DAG of many different tasks. 
たとえば、PolarsおよびPySparkプログラムも変換のDAGとして実装されており、多くの異なるタスクのDAGを実行するよりも単一のプログラムを実行する方が速く、リソース効率が良いことがよくあります。

Having said that, there are many orchestrators that are designed to execute ML pipe‐ lines. 
とはいえ、MLパイプラインを実行するために設計された多くのオーケストレーターがあります。

However, given the confusion of many vendors on what an ML pipeline is, many of these frameworks consider feature pipelines to be data pipelines and outside the scope of ML pipelines. 
しかし、多くのベンダーがMLパイプラインとは何かについて混乱しているため、これらのフレームワークの多くはフィーチャーパイプラインをデータパイプラインと見なし、MLパイプラインの範囲外としています。

The ML pipeline orchestrators include:
MLパイプラインオーケストレーターには以下が含まれます：

_Kubeflow_ 
_Kubeflow_ 
This is a Kubernetes native orchestrator for ML pipelines that was originally developed by Google but is now maintained by the community. 
これは、元々Googleによって開発されたMLパイプライン用のKubernetesネイティブオーケストレーターですが、現在はコミュニティによって維持されています。

Kubeflow is designed for training pipelines; it does not scale for feature pipelines or batch inference pipelines. 
Kubeflowはトレーニングパイプライン用に設計されており、フィーチャーパイプラインやバッチ推論パイプラインにはスケールしません。

_Metaflow_ 
_Metaflow_ 
This was originally developed by Netflix, and it defines a workflow as a DAG in Python and supports automatic containerization similar to Modal, but it can run on Kubernetes. 
これは元々Netflixによって開発され、ワークフローをPythonのDAGとして定義し、Modalに似た自動コンテナ化をサポートしますが、Kubernetes上で実行できます。

It lacks native support for scalable feature pipelines. 
スケーラブルなフィーチャーパイプラインに対するネイティブサポートが欠けています。

_Flyte_ 
_Flyte_ 
This was originally developed at Lyft, and it supports running containers in Kubernetes as training and batch inference pipelines. 
これは元々Lyftで開発され、トレーニングおよびバッチ推論パイプラインとしてKubernetesでコンテナを実行することをサポートします。

It lacks support for scalable feature pipelines. 
スケーラブルなフィーチャーパイプラインに対するサポートが欠けています。

_ZenML_ 
_ZenML_ 
This is an open source ML pipeline orchestrator similar to Metaflow, and it runs on Kubernetes and has good integrations with cloud platforms. 
これはMetaflowに似たオープンソースのMLパイプラインオーケストレーターで、Kubernetes上で実行され、クラウドプラットフォームとの良好な統合があります。

It lacks support for scalable feature pipelines. 
スケーラブルなフィーチャーパイプラインに対するサポートが欠けています。

_Vertex AI Pipelines, Azure ML, and SageMaker Pipelines_ 
_Vertex AI Pipelines、Azure ML、およびSageMaker Pipelines_ 
These are all specialized for training pipelines, rather than feature/batch inference pipelines. 
これらはすべて、フィーチャー/バッチ推論パイプラインではなく、トレーニングパイプラインに特化しています。

They use containers with prebuilt binaries for popular ML frameworks, but you also can create your own container images manually. 
これらは人気のあるMLフレームワーク用の事前構築されたバイナリを持つコンテナを使用しますが、自分でコンテナイメージを手動で作成することもできます。

There are workflow orchestrators that are popular within data engineering that can be used to run ML pipelines, including:
データエンジニアリング内で人気のあるワークフローオーケストレーターがあり、MLパイプラインを実行するために使用できます。これには以下が含まれます：

- Cloud native Python-based workflow orchestrators, such as Dagster and Prefect
- DagsterやPrefectなどのクラウドネイティブなPythonベースのワークフローオーケストレーター
- Databricks Workflows, Snowflake tasks, and Google Dataform, which are all orchestrators for running more scalable Spark or SQL jobs
- Databricks Workflows、Snowflakeタスク、およびGoogle Dataformは、すべてよりスケーラブルなSparkまたはSQLジョブを実行するためのオーケストレーターです

We will look now at the most popular Python workflow orchestrator, Airflow, a general-purpose workflow orchestrator, and cloud provider workflow orchestrators for Azure, AWS, and GCP. 
これから、最も人気のあるPythonワークフローオーケストレーターであるAirflow、汎用ワークフローオーケストレーター、およびAzure、AWS、GCPのクラウドプロバイダーのワークフローオーケストレーターを見ていきます。

###### 4.0.0.0.16. Airflow
###### 4.0.0.0.17. Airflow

Apache Airflow is a popular open source orchestrator that allows you to define, schedule, and monitor workflows. 
Apache Airflowは、ワークフローを定義、スケジュール、および監視することを可能にする人気のオープンソースオーケストレーターです。

Airflow’s workflows are written in Python as a DAG of tasks, where each task can be a program in its own right executed by an oper‐ ator. 
Airflowのワークフローは、タスクのDAGとしてPythonで記述されており、各タスクはオペレーターによって実行される独自のプログラムであることができます。

Airflow supports a rich variety of operators, including a Spark operator to run PySpark programs and a Kubernetes operator to run (Python) programs on Kuber‐ netes. 
Airflowは、PySparkプログラムを実行するためのSparkオペレーターや、Kubernetes上で（Python）プログラムを実行するためのKubernetesオペレーターなど、豊富な種類のオペレーターをサポートしています。

There is also a Hopsworks job operator to run Hopsworks jobs. 
Hopsworksジョブを実行するためのHopsworksジョブオペレーターもあります。

Airflow is a general-purpose workflow scheduler with rich scheduling options and a user inter‐ face to inspect runs and logs and to schedule new runs. 
Airflowは、豊富なスケジューリングオプションを持つ汎用ワークフロースケジューラーであり、実行やログを検査し、新しい実行をスケジュールするためのユーザーインターフェースを提供します。

DAGs and tasks can be sched‐ uled using cron expressions or based on events with _sensors that determine when a_ task can be scheduled. 
DAGとタスクは、cron式を使用してスケジュールするか、タスクをスケジュールできるタイミングを決定するセンサーに基づいてスケジュールできます。

For example, a FileSensor (or S3KeySensor) can be used to run a task only after a particular file is created in a specific directory. 
たとえば、FileSensor（またはS3KeySensor）を使用して、特定のディレクトリに特定のファイルが作成された後にのみタスクを実行できます。

Other popular sensors are an HttpSensor (which polls an HTTP endpoint until a specific response is received) and an ExternalTaskSensor (which checks for the completion of a tag in a different DAG). 
他の人気のあるセンサーには、特定の応答が受信されるまでHTTPエンドポイントをポーリングするHttpSensorや、別のDAGでタグの完了を確認するExternalTaskSensorがあります。

You can define dependencies between tasks directly in the Python program that defines your DAG. 
DAGを定義するPythonプログラム内で、タスク間の依存関係を直接定義できます。

###### 4.0.0.0.18. Cloud Provider Workflow Orchestrators
###### 4.0.0.0.19. クラウドプロバイダーのワークフローオーケストレーター

Azure Data Factory (ADF) is a generic workflow orchestrator that you can use to run Spark, Pandas, and Polars programs on Azure. 
Azure Data Factory（ADF）は、Azure上でSpark、Pandas、およびPolarsプログラムを実行するために使用できる汎用ワークフローオーケストレーターです。

ADF organizes workflows into pipe‐ lines, which define a series of steps or activities needed for data integration or trans‐ formation. 
ADFは、データ統合または変換に必要な一連のステップまたはアクティビティを定義するパイプラインにワークフローを整理します。

Each pipeline can contain a sequence of activities, such as data movement, data transformation, and triggering external systems. 
各パイプラインは、データ移動、データ変換、外部システムのトリガーなどのアクティビティのシーケンスを含むことができます。

ADF orchestrates these activi‐ ties in a specific order, handling dependencies and conditional branching within a single pipeline. 
ADFは、これらのアクティビティを特定の順序で調整し、単一のパイプライン内での依存関係や条件分岐を処理します。

AWS Step Functions is a general-purpose serverless workflow orchestrator for AWS, and it’s used to coordinate multiple AWS services and build workflows with frame‐ works like PySpark, Polars, Pandas, and DuckDB. 
AWS Step Functionsは、AWS用の汎用サーバーレスワークフローオーケストレーターであり、複数のAWSサービスを調整し、PySpark、Polars、Pandas、DuckDBなどのフレームワークを使用してワークフローを構築するために使用されます。

Google Cloud Composer is a fully managed orchestration service on GCP that is built on Airflow. 
Google Cloud Composerは、Airflowに基づいたGCP上の完全に管理されたオーケストレーションサービスです。

It allows users to connect and orchestrate various Google Cloud services and APIs, including BigQuery commands, Spark jobs on Dataproc, and ML pipelines on GCP Vertex. 
これにより、ユーザーはBigQueryコマンド、Dataproc上のSparkジョブ、GCP Vertex上のMLパイプラインなど、さまざまなGoogle CloudサービスやAPIを接続し、調整できます。

Many workflow orchestrators come with built-in lineage informa‐ tion for tasks in their DAGs. 
多くのワークフローオーケストレーターには、DAG内のタスクに対する組み込みの系譜情報が付属しています。

That lineage information, however, is typically not connected to artifacts, such as feature groups, models, and deployments in an ML system. 
ただし、その系譜情報は通常、MLシステム内のフィーチャーグループ、モデル、デプロイメントなどのアーティファクトに接続されていません。

Lineage information for ML assets is stored in MLOps platforms, such as Hopsworks, Vertex, Databricks, and SageMaker. 
ML資産の系譜情報は、Hopsworks、Vertex、Databricks、SageMakerなどのMLOpsプラットフォームに保存されます。

###### 4.0.0.0.20. Data Contracts
###### 4.0.0.0.21. データ契約

Data contracts for feature groups have aims that are similar to those of interface con‐ tracts in software engineering. 
フィーチャーグループのデータ契約は、ソフトウェア工学におけるインターフェース契約の目的に似ています。

They should ensure that clients read and write data that conforms to the interface (or schema). 
それらは、クライアントがインターフェース（またはスキーマ）に準拠したデータを読み書きすることを保証する必要があります。

That is, the names and types of the col‐ umns in a DataFrame should match the names and types of columns in the corre‐ sponding feature group being written to or read from. 
つまり、DataFrame内の列の名前と型は、書き込まれるまたは読み取られる対応するフィーチャーグループ内の列の名前と型と一致する必要があります。

For example, Hopsworks performs schema validation on writing data to feature groups—checking that data values correspond to the data types defined in the feature group schema and that strings and rows do not exceed their maximum length. 
たとえば、Hopsworksはフィーチャーグループにデータを書き込む際にスキーマ検証を行い、データ値がフィーチャーグループスキーマで定義されたデータ型に対応していること、および文字列や行が最大長を超えないことを確認します。

Schema checking also vali‐ dates integrity constraints, such as ensuring there are no missing primary key values or missing event_time values (if the feature group stores time-series data). 
スキーマチェックは、主キー値が欠落していないことや、event_time値が欠落していないこと（フィーチャーグループが時系列データを保存している場合）など、整合性制約も検証します。

In addition to schema validation, data contracts should provide guarantees on the quality of data and its timely delivery to data consumers. 
スキーマ検証に加えて、データ契約はデータの品質とデータ消費者へのタイムリーな配信に関する保証を提供する必要があります。

Many data sources for AI systems do not provide such guarantees, so it becomes the responsibility of the AI system to provide data quality and timeliness guarantees by answering the follow‐ ing questions:  
AIシステムの多くのデータソースはそのような保証を提供しないため、AIシステムがデータ品質とタイムリーな配信の保証を提供する責任を負うことになります。以下の質問に答えることによって：

- What are the service-level objectives (SLOs) for a feature group?
- フィーチャーグループのサービスレベル目標（SLO）は何ですか？
- What is the domain (valid range) of values for any given feature?
- 任意のフィーチャーの値のドメイン（有効範囲）は何ですか？
- What is the expected and worst-case freshness for feature data?
- フィーチャーデータの期待される新鮮さと最悪のケースは何ですか？
- How late can data arrive before it should be discarded?
- データはどれくらい遅れて到着することができ、廃棄されるべきですか？
- What percentage of missing values can be tolerated for a given feature?
- 特定のフィーチャーに対して許容できる欠損値の割合はどれくらいですか？

In Hopsworks, you can describe the SLO for a feature group using tags. 
Hopsworksでは、タグを使用してフィーチャーグループのSLOを記述できます。

You then need to implement the mechanisms to enforce the SLO defined in a tag. 
次に、タグで定義されたSLOを強制するためのメカニズムを実装する必要があります。



. You then need to implement the mechanisms to enforce the SLO defined in a tag. 
次に、タグで定義されたSLOを強制するためのメカニズムを実装する必要があります。

Chapters 13 and 14 introduce techniques from MLOps that can help you implement custom data contracts. 
第13章と第14章では、カスタムデータ契約を実装するのに役立つMLOpsの技術を紹介します。

You can also design governance policies with tags, such as whether or not a feature group is allowed to contain personally identifiable information (PII). 
また、タグを使用してガバナンスポリシーを設計することもできます。たとえば、フィーチャーグループが個人を特定できる情報（PII）を含むことが許可されているかどうかです。

In the following, we show how to attach metadata to a feature group using a tag: 
以下に、タグを使用してフィーチャーグループにメタデータを添付する方法を示します。

```  
fg = fs.get_feature_group("cc_trans_fg", version=1)   
fg.add_tag(name="PII", value="false")
```

You can enforce a governance policy in code by checking whether the correct tags and/or tag values are set for an asset, such as a feature group, a feature view, a model, or a deployment. 
フィーチャーグループ、フィーチャービュー、モデル、またはデプロイメントなどの資産に対して、正しいタグおよび/またはタグ値が設定されているかどうかを確認することで、コード内でガバナンスポリシーを強制できます。

For example, here we search in the feature store for all feature groups, feature views, or features that have the tag “PII”: 
たとえば、ここではフィーチャーストア内で「PII」タグを持つすべてのフィーチャーグループ、フィーチャービュー、またはフィーチャーを検索します。

```  
search_api = project.get_search_api()   
tag_search_result = search_api.featurestore_search("PII")   
tag_search_result.to_dict()
```

We can then check whether the returned ML assets conform to the governance policy or not and send an alert if there is a violation. 
その後、返されたML資産がガバナンスポリシーに準拠しているかどうかを確認し、違反があればアラートを送信できます。

###### 4.0.0.0.22. Data Validation with Great Expectations in Hopsworks
###### 4.0.0.0.23. HopsworksにおけるGreat Expectationsを用いたデータ検証

Data quality guarantees are part of data contracts and require data validation. 
データ品質の保証はデータ契約の一部であり、データ検証を必要とします。

In data engineering, it is often OK to validate data asynchronously after it has been written to a data warehouse. 
データエンジニアリングでは、データがデータウェアハウスに書き込まれた後に非同期でデータを検証することがよくあります。

This is because many dashboards are updated on a schedule, and so long as data is validated before the dashboards are updated, you are not at risk of displaying garbage. 
これは、多くのダッシュボードがスケジュールに従って更新されるため、ダッシュボードが更新される前にデータが検証されていれば、無意味なデータを表示するリスクはありません。

Figure 8-5 shows how ML shifts the data validation work to earlier in the data lifecycle, compared with data engineering for business intelligence. 
図8-5は、MLがビジネスインテリジェンスのためのデータエンジニアリングと比較して、データライフサイクルの早い段階にデータ検証作業を移す方法を示しています。

Data is validated before it is written to feature groups, as one bad data point could fail a training or inference run. 
データはフィーチャーグループに書き込まれる前に検証されます。なぜなら、1つの不良データポイントがトレーニングや推論の実行を失敗させる可能性があるからです。



_Figure 8-5. Data quality for ML requires shifting left data validation in the development process and therefore validating data earlier in its lifecycle than in traditional data engineering. ML requires more monitoring of operational data than business intelligence systems._
_Figure 8-5. MLのデータ品質は、開発プロセスにおけるデータ検証を左にシフトさせ、従来のデータエンジニアリングよりもデータのライフサイクルの早い段階で検証することを必要とします。MLは、ビジネスインテリジェンスシステムよりも運用データの監視を多く必要とします。_

###### 4.0.0.0.24. WAP Pattern
###### 4.0.0.0.25. WAPパターン
In data engineering, data validation is shifted right in the data lifecycle compared with ML. 
データエンジニアリングでは、データライフサイクルにおけるデータ検証はMLと比較して右にシフトします。

For example, the write-audit-publish (WAP) pattern involves first ingesting all source data unaltered to a landing area, often in an immutable format. 
例えば、write-audit-publish (WAP)パターンでは、すべてのソースデータを変更せずにランディングエリアに取り込み、しばしば不変の形式で保存します。

In the audit phase, one or more data pipelines apply data validation rules, detect anomalies, and identify duplicates. 
監査フェーズでは、1つ以上のデータパイプラインがデータ検証ルールを適用し、異常を検出し、重複を特定します。

In the publish phase, pipelines transform the validated data to a consumable layer for downstream applications. 
公開フェーズでは、パイプラインが検証されたデータを下流アプリケーション用の消費可能なレイヤーに変換します。

The medallion architecture is a variation of this pattern with bronze, silver, and gold tables. 
メダリオンアーキテクチャは、このパターンの変種であり、ブロンズ、シルバー、ゴールドのテーブルがあります。

As introduced in Chapter 3, in Hopsworks, we can implement the data validation rules as an expectation suite in Great Expectations. 
第3章で紹介したように、Hopsworksでは、データ検証ルールをGreat Expectationsの期待スイートとして実装できます。

Another important part of data contracts are governance policies that should be enforced before inserting data. 
データ契約のもう一つの重要な部分は、データを挿入する前に施行されるべきガバナンスポリシーです。

Governance requires both a way to define a policy and a mechanism to enforce it. 
ガバナンスには、ポリシーを定義する方法と、それを施行するメカニズムの両方が必要です。

Hopsworks provides tags and schematized tags (see Chapter 13) to define policies and attach them to feature groups. 
Hopsworksは、ポリシーを定義し、フィーチャーグループに添付するためのタグとスキーマ化されたタグ（第13章参照）を提供します。

Figure 8-6 shows a feature pipeline that performs data transformations and then applies both data validation checks and governance policy enforcement checks before ingesting data into a feature group.
_Figure 8-6. データをフィーチャーストアに書き込む前に、データ品質（Great Expectationsで記述されたポリシー）とデータガバナンスポリシーが遵守されていることを確認します。問題を通知するアラート。_

You define data validation rules for features in an expectation suite defined in Great Expectations. 
フィーチャーのデータ検証ルールは、Great Expectationsで定義された期待スイートで定義します。

We saw in Chapter 3 that you can attach an expectation suite to a feature group when you create it. 
第3章で、フィーチャーグループを作成する際に期待スイートを添付できることを見ました。

You can also add an expectation suite to an existing feature group and remove the expectation suite from a feature group as follows: 
既存のフィーチャーグループに期待スイートを追加したり、フィーチャーグループから期待スイートを削除したりすることもできます。

```  
expectation_suite = ge.core.ExpectationSuite( .. )  
fg.save_expectation_suite(  
    expectation_suite, run_validation=True, validation_ingestion_policy="ALWAYS"  
)  
1. remove the expectation suite from the feature group  
fg.delete_expectation_suite()  
```  
ここでは、`validation_ingestion_policy`を`ALWAYS`に設定しており、この場合、データ検証ルールが失敗してもデータがフィーチャーグループに書き込まれます。

The default policy is STRICT, in which case the feature pipeline will fail if any data validation rule fails— no data will be written to the feature group. 
デフォルトのポリシーはSTRICTであり、この場合、データ検証ルールが失敗するとフィーチャーパイプラインは失敗し、データはフィーチャーグループに書き込まれません。

In feature pipelines, we can define governance policies as tags and implement our own enforcement checks. 
フィーチャーパイプラインでは、ガバナンスポリシーをタグとして定義し、自分自身の施行チェックを実装できます。

For example, we can define a NO_PII tag and attach it to a feature group. 
例えば、NO_PIIタグを定義し、それをフィーチャーグループに添付できます。

The policy is that this feature group should not contain PII data. 
このフィーチャーグループにはPIIデータを含めてはいけないというポリシーです。

We can implement a check_for_pii_data() function that enforces this policy. 
このポリシーを施行するcheck_for_pii_data()関数を実装できます。

First, we check whether the policy applies to the feature group by checking whether it has the NO_PII tag. 
まず、NO_PIIタグがあるかどうかを確認することで、ポリシーがフィーチャーグループに適用されるかどうかを確認します。

If it does, we pass the data into check_for_pii_data(), and if the data contains PII data, we raise an alert: 
もしそうであれば、データをcheck_for_pii_data()に渡し、データにPIIデータが含まれている場合はアラートを発生させます。

```  
if fg.contains_tag("NO_PII"):  
    if check_for_pii_data(df):  
        fg.create_alert(receiver="email", severity="warning",  
            status=f"PII data")  
```  
The `check_for_pii_data()` function can be implemented using a library such as DataProfiler. 
`check_for_pii_data()`関数は、DataProfilerなどのライブラリを使用して実装できます。

In the near future, LLMs will probably be used to aid PII checks. 
近い将来、LLMがPIIチェックを支援するために使用される可能性があります。

###### 4.0.0.0.26. Summary and Exercises
###### 4.0.0.0.27. 要約と演習
Batch feature pipelines are programs that run on a schedule, applying MITs to data read from batch/streaming/API sources to create reusable feature data that should be validated before it is written to a feature group. 
バッチフィーチャーパイプラインは、スケジュールに従って実行されるプログラムであり、バッチ/ストリーミング/APIソースから読み取ったデータにMITを適用して、フィーチャーグループに書き込む前に検証されるべき再利用可能なフィーチャーデータを作成します。

In this chapter, we started by investigating the different types of data sources for batch feature pipelines, and we moved on to generating synthetic data for our credit card fraud data mart using LLMs. 
この章では、バッチフィーチャーパイプラインのさまざまなデータソースを調査することから始め、LLMを使用してクレジットカード詐欺データマートの合成データを生成することに移りました。

We showed how to design a batch feature pipeline for our credit card fraud problem that is parameterized by a start_time and an end_time, enabling it to either backfill historical feature data or perform incremental processing on newly arrived data. 
クレジットカード詐欺の問題に対するバッチフィーチャーパイプラインを、start_timeとend_timeでパラメータ化して設計する方法を示し、歴史的なフィーチャーデータをバックフィルするか、新しく到着したデータに対して増分処理を行うことができるようにしました。

We also looked at how to run batch feature pipelines using job orchestrators or workflow orchestrators. 
また、ジョブオーケストレーターやワークフローオーケストレーターを使用してバッチフィーチャーパイプラインを実行する方法も見ました。

Finally, we introduced data contracts and looked at how to ensure that our feature pipelines provide SLOs for feature group data through data validation and data governance policy enforcement. 
最後に、データ契約を紹介し、データ検証とデータガバナンスポリシーの施行を通じて、フィーチャーパイプラインがフィーチャーグループデータに対してSLOを提供することを保証する方法を見ました。

The following exercises will help you learn how to compose MITs into batch feature pipelines: 
以下の演習は、MITをバッチフィーチャーパイプラインに組み込む方法を学ぶのに役立ちます。

- Write the code in PySpark to compute standard deviation for multiday aggregations using one-day aggregations by computing sum, count, and daily sum-of-squares aggregations. 
- 複数日の集計に対して標準偏差を計算するためのPySparkのコードを書いてください。これは、合計、カウント、および日次の二乗和集計を計算することによって、1日の集計を使用します。 

Note: the variance (standard deviation is the square root of the variance) over a period of multiple days can be computed using the following formula: 
注：複数日の期間にわたる分散（標準偏差は分散の平方根）は、次の式を使用して計算できます。

Variance = [∑] _[x][2]_ ∑ _x_  
_n_ [−] _n_  
2  

- Write a Polars program that uses HyperLogLog to compute an approximate multi-day distinct count for credit card transactions using single-day distinct count aggregations. 
- HyperLogLogを使用して、単日固有カウント集計を使用してクレジットカード取引の近似的な複数日固有カウントを計算するPolarsプログラムを書いてください。datasketchライブラリを使用します。

