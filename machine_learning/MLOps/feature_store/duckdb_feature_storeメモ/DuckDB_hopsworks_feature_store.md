refs: https://www.hopsworks.ai/post/python-centric-feature-service-with-arrowflight-and-duckdb
<!-- なんかHopswork特徴量ストアが、内部でDuckDBをどのように使うようになったか、という話なので、あんまり読まなくて良さそう...!:thinking: -->

# Faster reading from the Lakehouse to Python with DuckDB/ArrowFlight  
# レイクハウスからPythonへの高速な読み取り：DuckDB/ArrowFlightを使用して

## TL;DR
In this article, we outline how we leveraged ArrowFlight with DuckDB to build a new service that massively improves the performance of Python clients reading from lakehouse data in the Hopsworks Feature Store. 
この記事では、DuckDBとArrowFlightを活用して、Hopsworks Feature Storeのレイクハウスデータを読み取るPythonクライアントのパフォーマンスを大幅に向上させる新しいサービスを構築した方法を概説します。
We present benchmarks and results comparing Hopsworks to cloud provider feature stores, showing from 8X to 45X higher throughput. 
Hopsworksとクラウドプロバイダーのフィーチャーストアを比較したベンチマークと結果を示し、スループットが8倍から45倍高いことを示します。
Our analysis suggests the performance improvements are due to (1) using Arrow end-to-end (for both data transport and query processing in DuckDB, removing expensive serialization/deserialization), and (2) replacing ODBC/JDBC with ArrowFlight, removing expensive row-wise to column-wise transformations.
私たちの分析は、パフォーマンスの向上が（1）Arrowをエンドツーエンドで使用すること（DuckDBにおけるデータ輸送とクエリ処理の両方において、高価なシリアル化/デシリアル化を排除する）および（2）ODBC/JDBCをArrowFlightに置き換えること（高価な行単位から列単位への変換を排除する）によるものであることを示唆しています。

## Introduction はじめに

Feature stores provide APIs for retrieving consistent snapshots of feature data for both model training and model inference. 
**フィーチャーストアは、モデルのトレーニングとモデルの推論のために、一貫したフィーチャーデータのスナップショットを取得するためのAPI**を提供します。
(「一貫した」と「特徴量のスナップショットを取得」というのがポイントっぽい...!:thinking:)
Feature stores are typically implemented as dual datastores, with a row-oriented database providing low latency access to the latest values of feature data for online models via an Online API, and a column-oriented data warehouse or lakehouse providing access to historical and new feature data for training and batch inference, respectively, via an Offline API. 
**フィーチャーストアは通常、二重データストアとして実装**されており、行指向データベースがオンラインモデルの最新のフィーチャーデータの値に低遅延でアクセスするための**Online API**を介して提供し、列指向データウェアハウスまたはレイクハウスがトレーニングおよびバッチ推論のために歴史的および新しいフィーチャーデータにアクセスするための**Offline API**を介して提供します。
These two databases are typically called the Online Store and the Offline Store, respectively. 
これらの**二つのデータベースは通常、それぞれOnline StoreとOffline Storeと呼ばれます**。

![]()
Figure 1: Arrow is now used end-to-end from the Lakehouse to Python clients that use an Offline API to read feature data for training models and for making batch predictions (inference)
図1：Arrowは、レイクハウスからPythonクライアントまでエンドツーエンドで使用されており、Offline APIを使用してモデルのトレーニングやバッチ予測（推論）のためのフィーチャーデータを読み取ります。

Similar to other feature stores, Hopsworks has used Spark to implement the Offline API. 
他のフィーチャーストアと同様に、HopsworksはOffline APIを実装するためにSparkを使用しています。
This is great for large datasets, but for small or moderately sized datasets (think of the size of data that would fit in a Pandas DataFrame in your local Python environment), the overhead of a Spark job and transferring the data to Python clients can be significant. 
これは大規模なデータセットには適していますが、小規模または中規模のデータセット（ローカルのPython環境でPandas DataFrameに収まるデータのサイズを考えてみてください）に対しては、SparkジョブのオーバーヘッドやデータをPythonクライアントに転送する際のオーバーヘッドが大きくなる可能性があります。
In this article, we introduce a new service in Hopsworks, ArrowFlight with DuckDB, that gives massive performance improvements for Python clients when reading data from the lakehouse via the Offline API. 
この記事では、Hopsworksにおける新しいサービス、ArrowFlight with DuckDBを紹介します。これは、Offline APIを介してレイクハウスからデータを読み取る際に、Pythonクライアントに大幅なパフォーマンス向上をもたらします。
This improves the iteration speed of Python developers working with a feature store, opening up feature stores as a general purpose data platform usable by the wider Python community.  
これにより、フィーチャーストアで作業するPython開発者の反復速度が向上し、フィーチャーストアがより広範なPythonコミュニティによって使用可能な汎用データプラットフォームとして開かれます。

![]()

In tables 1,2, you can see a summary of the speedup we observed when using DuckDB/ArrowFlight for moderately sized data, compared to existing feature stores. 
表1および2では、既存のフィーチャーストアと比較して、中規模データに対してDuckDB/ArrowFlightを使用した際に観察されたスピードアップの概要を示しています。
The details are in the benchmark section below. 
詳細は以下のベンチマークセクションにあります。

## ArrowFlight with DuckDB Service

Firstly, let’s introduce the technologies. 
まず、技術を紹介しましょう。
DuckDB is a lightweight and efficient database management system that has a columnar-vectorized query execution engine which is optimized for analytical workloads. 
DuckDBは、分析ワークロードに最適化されたカラム指向ベクトル化クエリ実行エンジンを持つ軽量で効率的なデータベース管理システムです。
It comes with a zero-copy integration with Pandas and Pyarrow and lots of flexibility in terms of input formats and storage connectors. 
PandasおよびPyarrowとのゼロコピー統合を提供し、入力フォーマットやストレージコネクタに関して多くの柔軟性を持っています。
Our service uses DuckDB to read from tables on object storage and perform point-in-time correct Joins over tables. 
私たちのサービスは、オブジェクトストレージ上のテーブルからDuckDBを使用して読み取り、テーブル間で時点正確な結合を実行します。
However, as we built a network service, we needed to enable data to flow securely from DuckDB to Pandas clients without unnecessary serialization/deserialization (thanks Arrow!) or conversion of data from column-oriented to row-oriented and back again (bye bye JDBC!). 
しかし、ネットワークサービスを構築するにあたり、DuckDBからPandasクライアントへのデータの流れを、不要なシリアル化/デシリアル化（ありがとうArrow！）やカラム指向から行指向へのデータ変換を行わずに安全に実現する必要がありました（さようならJDBC！）。
For this, we used ArrowFlight, a high-performance client-server framework for building applications that transfer arrow data over the network. 
これを実現するために、私たちはArrowFlightを使用しました。ArrowFlightは、ネットワーク上でArrowデータを転送するアプリケーションを構築するための高性能なクライアント-サーバーフレームワークです。
Independent benchmarks show that ArrowFlight outperforms existing database network protocols such as ODBC by up to 30x for arrow data. 
独立したベンチマークは、ArrowFlightがODBCなどの既存のデータベースネットワークプロトコルに対して、Arrowデータにおいて最大30倍の性能を発揮することを示しています。

Figure 1 shows how ArrowFlight, DuckDB, and Pandas come together in our new Hopsworks service (here with a Hudi tables as the offline store). 
図1は、ArrowFlight、DuckDB、およびPandasが私たちの新しいHopsworksサービス（ここではオフラインストアとしてHudiテーブルを使用）でどのように統合されるかを示しています。
By leveraging Apache Arrow we have zero-copy data transfer on server- as well as on client-side, while being able to use ArrowFlight as a high-performance data transfer protocol. 
Apache Arrowを活用することで、サーバー側とクライアント側の両方でゼロコピーデータ転送を実現し、ArrowFlightを高性能なデータ転送プロトコルとして使用することができます。
We secure data transfers using mutual TLS for client authentication and encryption in-flight and we build on Hopsworks’ existing authorization framework for access control. 
私たちは、クライアント認証とデータ転送中の暗号化のために相互TLSを使用してデータ転送を保護し、アクセス制御のためにHopsworksの既存の認可フレームワークを基に構築しています。

<!-- ここまで読んだ! -->

## High Performance Python-native Access to Lakehouse Data 高性能なPythonネイティブのLakehouseデータへのアクセス

Apache Hudi is a parquet-based Lakehouse format that is the default offline store in Hopsworks. 
Apache Hudiは、HopsworksのデフォルトのオフラインストアであるparquetベースのLakehouseフォーマットです。
Whenever a feature store client reads Pandas DataFrames containing either training data or batch inference data, the data is read from Hudi tables (feature groups) and ends up in a Pandas DataFrame, which is then used as model input for training or batch inference. 
フィーチャーストアクライアントがトレーニングデータまたはバッチ推論データを含むPandas DataFrameを読み込むと、データはHudiテーブル（フィーチャーグループ）から読み込まれ、最終的にPandas DataFrameに格納され、これがトレーニングまたはバッチ推論のモデル入力として使用されます。

With ArrowFlight and DuckDB we provide a fast Python-native API to the Hudi tables as well as high performance point-in-time correct Joins for reading consistent snapshots of feature data that span many tables. 
ArrowFlightとDuckDBを使用して、Hudiテーブルへの高速なPythonネイティブAPIを提供するとともに、多くのテーブルにまたがるフィーチャーデータの一貫したスナップショットを読み取るための高性能な時点正確な結合を提供します。
While Hudi is Parquet-based and DuckDB features a very efficient Parquet reader, DuckDB does not support reading Hudi Tables directly. 
HudiはParquetベースであり、DuckDBは非常に効率的なParquetリーダーを備えていますが、DuckDBはHudiテーブルを直接読み取ることをサポートしていません。
We therefore developed a custom reader for Hudi Copy-on-Write tables. 
したがって、Hudi Copy-on-Writeテーブル用のカスタムリーダーを開発しました。
For all supported offline stores, such as Snowflake or BigQuery, we will provide a different Arrow reader for DuckDB. 
SnowflakeやBigQueryなど、すべてのサポートされているオフラインストアに対して、DuckDB用の異なるArrowリーダーを提供します。

<!-- ここまで読んだ! -->


## Hudi Reader for DuckDB in Detail Hudi Reader for DuckDBの詳細

Apache Hudi’s storage format is based on parquet files and additional metadata that are stored on HopsFS. 
Apache Hudiのストレージフォーマットは、parquetファイルとHopsFSに保存される追加のメタデータに基づいています。

One Feature Group is typically not stored as a single parquet file, but the data is broken down into individual files by partitions (based on the Feature Group’s partition key), and then, depending on the file size, further divided into smaller slices within each partition. 
1つのFeature Groupは通常、単一のparquetファイルとして保存されるのではなく、データはパーティション（Feature Groupのパーティションキーに基づく）によって個々のファイルに分割され、その後、ファイルサイズに応じて各パーティション内でさらに小さなスライスに分割されます。

Each slice has a unique name and is associated with a particular commit-timestamp. 
各スライスにはユニークな名前が付けられ、特定のコミットタイムスタンプに関連付けられています。

When a new commit is made (`fg.insert(df)`), Hudi will quickly identify the latest version of all slices that are affected by the insert/upsert using a bloom filter index and then create updated copies of those slices. 
新しいコミットが行われると（`fg.insert(df)`）、Hudiはbloomフィルターインデックスを使用して挿入/アップサートによって影響を受けるすべてのスライスの最新バージョンを迅速に特定し、それらのスライスの更新されたコピーを作成します。

Hudi will also create a new .commit metadata file, which contains the list of files that have been updated by the commit. 
Hudiはまた、コミットによって更新されたファイルのリストを含む新しい.commitメタデータファイルを作成します。

That file will be retained for up to 30 commits. 
そのファイルは最大30回のコミットまで保持されます。

To read the latest snapshot view of a Hudi Table (most up-to-date version of the data), the latest versions of all slices have to be identified and all slices have to be read and unioned into a single Table. 
Hudiテーブルの最新スナップショットビュー（データの最も最新のバージョン）を読み取るには、すべてのスライスの最新バージョンを特定し、すべてのスライスを読み取って1つのテーブルに統合する必要があります。

Figure 2 shows how Hudi data is organized in HopsFS. 
図2は、HudiデータがHopsFS内でどのように整理されているかを示しています。

Files in Hopsworks are stored in cloud native object storage (S3 on AWS, GCS on GCP, Blob Storage on Azure) but accessed via a fast cache with a HDFS API, called HopsFS. 
Hopsworks内のファイルは、クラウドネイティブオブジェクトストレージ（AWSのS3、GCPのGCS、AzureのBlob Storage）に保存されますが、HopsFSと呼ばれるHDFS APIを介して高速キャッシュにアクセスされます。

To read a Hudi Table/Feature Group with DuckDB, we make a recursive file listing in HopsFS to retrieve all parquet-files that belong to a certain Hudi Table. 
DuckDBでHudiテーブル/Feature Groupを読み取るために、HopsFS内で再帰的なファイルリストを作成し、特定のHudiテーブルに属するすべてのparquetファイルを取得します。

Based on the listing, we identify the latest commit timestamp (which is part of the filename) for each parquet file slice. 
リストに基づいて、各parquetファイルスライスの最新のコミットタイムスタンプ（ファイル名の一部）を特定します。

Slices that are currently in-flight, meaning they belong to a commit that is currently in-progress, are discarded. 
現在進行中のコミットに属するスライス（現在進行中のもの）は破棄されます。

The correct list of latest parquet files is then passed to DuckDB where we register a unionized temporary table based on all the latest files. 
最新のparquetファイルの正しいリストはDuckDBに渡され、そこで最新のすべてのファイルに基づいて統合された一時テーブルが登録されます。

This table represents the exact same data we would get with a Hudi Snapshot read via Spark. 
このテーブルは、Sparkを介してHudiスナップショットを読み取った場合と正確に同じデータを表します。

If we execute a query (e.g. for creating a training dataset), this process is repeated for all Feature Groups that are required by the query. 
クエリを実行する場合（例：トレーニングデータセットの作成）、このプロセスはクエリで必要なすべてのFeature Groupに対して繰り返されます。

After the table registration, the input query will simply be executed by the DuckDB SQL engine on the previously registered tables. 
テーブルの登録後、入力クエリは以前に登録されたテーブル上でDuckDB SQLエンジンによって単純に実行されます。

Incremental file listing updates After the initial full file listing is established, we can keep the listing in-memory and update it incrementally whenever a new commit is made, using information from the Hudi .commit file. 
初期の完全なファイルリストが確立された後、リストをメモリ内に保持し、新しいコミットが行われるたびにHudiの.commitファイルからの情報を使用してインクリメンタルに更新できます。

While file listings in HopsFS are very efficient, this further improves read performance on Feature Groups with deeply nested partition keys and/or a high number of commits. 
HopsFS内のファイルリストは非常に効率的ですが、これにより、深くネストされたパーティションキーや多数のコミットを持つFeature Groupの読み取りパフォーマンスがさらに向上します。

Filter Pushdown When Hudi Feature Groups are partitioned and you have defined a filter on the partition column in your Query, we leverage that to prune out paths from the full file listing that do not match the filter condition, before registering them in DuckDB. 
フィルタープッシュダウン Hudi Feature Groupがパーティション化され、クエリのパーティション列にフィルターを定義している場合、私たちはそれを利用して、DuckDBに登録する前にフィルター条件に一致しないフルファイルリストからパスを削除します。

This can significantly reduce the memory requirements and query runtime for DuckDB. 
これにより、DuckDBのメモリ要件とクエリ実行時間を大幅に削減できます。

DuckDB’s HopsFS access Since data is stored on HopsFS, DuckDB needs to be able to read files directly from HopsFS. 
DuckDBのHopsFSアクセス データがHopsFSに保存されているため、DuckDBはHopsFSから直接ファイルを読み取る必要があります。

For this we leverage the extensibility of DuckDB’s filesystem layer via fsspec. 
これには、fsspecを介してDuckDBのファイルシステム層の拡張性を活用します。

Thanks to fsspec’s Hadoop File System Implementation, and HopsFS’s compatibility with HDFS, we can achieve that with minimal friction. 
fsspecのHadoopファイルシステム実装とHopsFSのHDFSとの互換性のおかげで、最小限の摩擦でそれを実現できます。



## Read Training Datasets at Higher Throughput 高スループットでのトレーニングデータセットの読み込み

With ArrowFlight and DuckDB, Python clients can read feature groups, batch inference data, as well as create in-memory training datasets at higher throughput than with Spark. 
ArrowFlightとDuckDBを使用することで、Pythonクライアントはフィーチャーグループやバッチ推論データを読み込み、Sparkよりも高いスループットでインメモリトレーニングデータセットを作成できます。
Furthermore, users can also read materialized training datasets in Hopsworks at improved throughput compared to the previous REST API solution.
さらに、ユーザーは以前のREST APIソリューションと比較して、Hopsworksでマテリアライズされたトレーニングデータセットを改善されたスループットで読み込むこともできます。



## Client Integration クライアント統合

There are no API changes needed for Hopsworks clients to use ArrowFlight with DuckDB in the Python client, beyond upgrading to Hopsworks 3.3+. 
HopsworksクライアントがPythonクライアントでDuckDBとArrowFlightを使用するために必要なAPIの変更は、Hopsworks 3.3+へのアップグレードを除いてありません。

All notebooks and Python scripts you built with Hopsworks can remain the same. 
Hopsworksで作成したすべてのノートブックとPythonスクリプトは、そのまま使用できます。

Once a cluster is deployed with “ArrowFlight Server'' (see installation guide), the following operations will automatically be performed by the new service: 
「ArrowFlight Server」（インストールガイドを参照）でクラスターが展開されると、次の操作が新しいサービスによって自動的に実行されます。

- reading Feature Groups 
- Feature Groupsの読み込み
- reading Queries 
- クエリの読み込み
- reading Training Datasets 
- トレーニングデータセットの読み込み
- creating In-Memory Training Datasets 
- インメモリトレーニングデータセットの作成
- reading Batch Inference Data 
- バッチ推論データの読み込み

For larger datasets, clients can still make use of the Spark/Hive backend by explicitly setting read_options={"use_hive": True}. 
大規模なデータセットの場合、クライアントは明示的に`read_options={"use_hive": True}`を設定することで、Spark/Hiveバックエンドを引き続き利用できます。



## Offline Feature Store Benchmarks オフラインフィーチャーストアのベンチマーク

We benchmarked the main four publicly available cloud-native feature stores using the NYC Taxi Dataset. 
私たちは、NYCタクシーデータセットを使用して、主な4つの公開されているクラウドネイティブフィーチャーストアをベンチマークしました。 
We omitted open-source feature stores, as they require manual configuration for their offline data lake/warehouse, or feature stores that are not generally accessible. 
オープンソースのフィーチャーストアは、オフラインデータレイク/ウェアハウスの手動設定が必要であるため、または一般的にアクセスできないフィーチャーストアを省略しました。 
You can reproduce this benchmark using the code published on github. 
このベンチマークは、GitHubに公開されたコードを使用して再現できます。

The “Offline API” to a feature store is a batch API for reading point-in-time consistent feature data. 
フィーチャーストアへの「オフラインAPI」は、時点整合性のあるフィーチャーデータを読み取るためのバッチAPIです。 
The Offline API is used by both training pipelines (you read feature data and output a trained model) and batch inference pipelines (you read a batch of new feature data and the model, and then output the model’s predictions on the batch of new feature data). 
オフラインAPIは、トレーニングパイプライン（フィーチャーデータを読み取り、トレーニングされたモデルを出力する）とバッチ推論パイプライン（新しいフィーチャーデータのバッチとモデルを読み取り、そのバッチの新しいフィーチャーデータに対するモデルの予測を出力する）の両方で使用されます。

There are typically two versions of the Offline API: 
オフラインAPIには通常、2つのバージョンがあります：
1. read the feature data directly as a Pandas DataFrame or 
1. フィーチャーデータを直接Pandas DataFrameとして読み取ること、または
2. create a batch of feature (and label) data as (parquet or csv) files that will be used by either a subsequent model training pipeline or batch inference pipeline. 
2. 次のモデルトレーニングパイプラインまたはバッチ推論パイプラインで使用される（parquetまたはcsv）ファイルとしてフィーチャー（およびラベル）データのバッチを作成することです。 
As such, we provide benchmarks for both (1) the Read an In-Memory Pandas DataFrame use case and the (2) create feature data (training data) as files. 
そのため、（1）メモリ内Pandas DataFrameの読み取りユースケースと（2）ファイルとしてフィーチャーデータ（トレーニングデータ）を作成するためのベンチマークを提供します。

In figure 4, we can see that Hopsworks has the lowest time required to read 5m, 10m, 20m, and 50m rows as a Pandas DataFrame. 
図4では、Hopsworksが5百万、10百万、20百万、50百万行をPandas DataFrameとして読み取るのに最も少ない時間を要することがわかります。 
The performance differences can be explained by a combination of 
パフォーマンスの違いは、以下の組み合わせで説明できます：
1. no serialization/deserialization in Hopsworks due to use of Arrow end-to-end, 
1. Arrowをエンドツーエンドで使用することによるHopsworksでのシリアル化/デシリアル化の不在、
2. no conversions from columnar-to-row-oriented or row-oriented-to-columnar (as happens when you use JDBC/ODBC), and 
2. 列指向から行指向、または行指向から列指向への変換がないこと（JDBC/ODBCを使用する場合に発生するように）、および
3. DuckDB is a higher performance point-in-time-join engine. 
3. DuckDBは高性能な時点結合エンジンです。

The other feature stores use distributed query engines, Spark/Photon (Databricks), Athena (Sagemaker), and BigQuery (Vertex). 
他のフィーチャーストアは、分散クエリエンジン、Spark/Photon（Databricks）、Athena（Sagemaker）、およびBigQuery（Vertex）を使用しています。 
The Python APIs for these frameworks act as wrappers for ease-of-use but there is significant overhead when using these systems. 
これらのフレームワークのPython APIは、使いやすさのためのラッパーとして機能しますが、これらのシステムを使用する際には大きなオーバーヘッドがあります。 
While Spark, Athena, and BigQuery do support Arrow as a data interchange format, it is not enough in these cases to remove the additional overhead that comes with a distributed and serverless engine. 
Spark、Athena、およびBigQueryはArrowをデータインターチェンジフォーマットとしてサポートしていますが、これらのケースでは分散型およびサーバーレスエンジンに伴う追加のオーバーヘッドを取り除くには不十分です。 
Spark is designed to handle large-scale data processing across multiple nodes in a cluster. 
Sparkは、クラスター内の複数のノードで大規模データ処理を処理するように設計されています。 
While this architecture allows Spark to scale horizontally and process massive datasets, it introduces additional overhead in data distribution and communication between nodes. 
このアーキテクチャにより、Sparkは水平にスケールし、大規模なデータセットを処理できますが、データの分配とノード間の通信に追加のオーバーヘッドが発生します。 
Often, Spark can require data to be repartitioned across workers to enable parallel processing. 
しばしば、Sparkは並列処理を可能にするためにデータをワーカー間で再分割する必要があります。 
This additional step called shuffling can introduce significant latency in the process affecting performance. 
この追加のステップであるシャッフルは、プロセスにおいてパフォーマンスに影響を与える重大なレイテンシを引き起こす可能性があります。 
Once Spark is finished doing transformations, there is an additional wait for it to collect all the data from each of its executors and then convert that data to a Pandas DataFrame. 
Sparkが変換を完了すると、各エグゼキュータからすべてのデータを収集し、そのデータをPandas DataFrameに変換するまでの追加の待機時間があります。 
With Databricks Photon integration with Spark we see also that Photon is a library loaded into the JVM from where it communicates with Spark via the Java Native Interface (JNI), passing data pointers to off-heap memory. 
Databricks PhotonがSparkと統合されていることで、PhotonはJVMにロードされたライブラリであり、Java Native Interface（JNI）を介してSparkと通信し、オフヒープメモリにデータポインタを渡すことがわかります。 
Despite Photon itself being written in C++ as a native, vectorized engine, it passes data back through the Spark pathway before it reaches the client. 
Photon自体はC++でネイティブなベクトル化エンジンとして書かれていますが、クライアントに到達する前にデータをSparkの経路を通じて渡します。 
With BigQuery we see another issue when materializing data as a DataFrame. 
BigQueryでは、データをDataFrameとしてマテリアライズする際に別の問題が発生します。 
BigQuery doesn’t materialize directly to the client. 
BigQueryはクライアントに直接マテリアライズしません。 
Instead, a temporary, intermediate table is first created which acts as the materialization source from which the DataFrame is then served and the table is deleted after use. 
代わりに、一時的な中間テーブルが最初に作成され、これがマテリアライズソースとして機能し、そこからDataFrameが提供され、使用後にテーブルが削除されます。 
This introduces a latency almost equivalent to doing a file write for in-memory datasets. 
これにより、メモリ内データセットのファイル書き込みを行うのとほぼ同等のレイテンシが導入されます。 
Sagemaker’s Athena does somewhat better, but is doing row-oriented to/from columnar conversions. 
SagemakerのAthenaはやや良好ですが、行指向から列指向への変換を行っています。

Given the improved performance in Hopsworks, we can see that there is a clear benefit when data processing engines are optimized for the storage format against which they are interacting. 
Hopsworksでのパフォーマンスの向上を考慮すると、データ処理エンジンが相互作用するストレージフォーマットに最適化されている場合に明確な利点があることがわかります。 
DuckDB optimizes query execution with filter pushdowns and predicate scans and is partition-aware. 
DuckDBは、フィルタープッシュダウンと述語スキャンを使用してクエリ実行を最適化し、パーティションを認識しています。 
Additionally, DuckDB can operate directly on Arrow Tables and stream Arrow data back and forth which allows it to utilize Arrow’s zerocopy data transfer mechanism for fast data transfer. 
さらに、DuckDBはArrowテーブル上で直接操作し、Arrowデータを双方向にストリーミングできるため、Arrowのゼロコピーデータ転送メカニズムを利用して高速データ転送を実現します。 
With a format-aware and storage-optimized engine consistently using Arrow from lakehouse all the way to the client we can see data transfer happening at near network-line speeds. 
フォーマットを認識し、ストレージに最適化されたエンジンが、レイクハウスからクライアントまで一貫してArrowを使用することで、データ転送がネットワークライン速度に近い速度で行われることがわかります。 
Arrow Flight securely transfers data across all languages and frameworks without requiring any serialization/deserialization. 
Arrow Flightは、すべての言語とフレームワーク間でデータを安全に転送し、シリアル化/デシリアル化を必要としません。 
Arrow Flight achieves this by operating directly on Arrow RecordBatch streams and does not require accessing data on a row level as opposed to JDBC/ODBC protocols. 
Arrow Flightは、Arrow RecordBatchストリーム上で直接操作することにより、これを実現し、JDBC/ODBCプロトコルとは異なり、行レベルでデータにアクセスする必要がありません。 
Our higher performance results are not surprising as VoltronData have shown how the ADBC protocol massively outperforms JDBC/ODBC for columnar datastores. 
私たちの高いパフォーマンス結果は驚くべきことではなく、VoltronDataがADBCプロトコルが列指向データストアに対してJDBC/ODBCを大幅に上回ることを示しています。

Similarly, when we create files containing feature data, for training data or for batch inference data, we can see similar performance gains using Hopsworks, compared to other feature stores. 
同様に、トレーニングデータやバッチ推論データを含むフィーチャーデータのファイルを作成する際にも、他のフィーチャーストアと比較してHopsworksを使用することで同様のパフォーマンス向上が見られます。



## Performance Benefits for Python Developers in Hopsworks Python開発者のためのHopsworksにおけるパフォーマンスの利点

To provide a more concrete example for Python developers, we compare the runtime of our Hopsworks Fraud Detection Batch Tutorial using ArrowFlight w. DuckDB against Spark (see Table 1). 
Python開発者のために、より具体的な例を提供するために、私たちはArrowFlight w. DuckDBを使用したHopsworks Fraud Detection Batch Tutorialの実行時間をSparkと比較します（表1を参照）。

The total runtime of all compute-intensive tasks goes down from 4.6 minutes to less than 16 seconds. 
すべての計算集約型タスクの合計実行時間は、4.6分から16秒未満に短縮されます。

Instead of waiting 10s for a training dataset to load, it now only takes 0.4s and feels almost instantaneous, which demonstrates the practical benefits that our new service brings to interactive Python client environments. 
トレーニングデータセットの読み込みに10秒待つ代わりに、今ではわずか0.4秒で済み、ほぼ瞬時に感じられます。これは、私たちの新しいサービスがインタラクティブなPythonクライアント環境にもたらす実際の利点を示しています。

This will significantly improve the iteration speed for Python developers working with feature data in Hopsworks. 
これは、Hopsworksで特徴データを扱うPython開発者の反復速度を大幅に向上させるでしょう。

Note, we are big fans of Spark - we have worked hard on improving Point-in-Time Join performance in Spark, but for Python clients and moderately sized data, ArrowFlight and DuckDB is a better fit. 
なお、私たちはSparkの大ファンです - SparkにおけるPoint-in-Time Joinのパフォーマンス向上に努めてきましたが、Pythonクライアントと中程度のサイズのデータに対しては、ArrowFlightとDuckDBの方が適しています。



## Support for Other Offline Stores 他のオフラインストアへのサポート

We are soon going to add support for DuckDB reading from External Feature Groups (external tables in Snowflake, BigQuery, etc). 
私たちは、DuckDBがExternal Feature Groups（Snowflake、BigQueryなどの外部テーブル）から読み取るサポートを間もなく追加する予定です。
This will include the support of creating point-in-time correct training datasets across Hudi Feature Groups and External Feature Groups.
これには、Hudi Feature GroupsとExternal Feature Groups全体で時点に正しいトレーニングデータセットを作成するサポートが含まれます。



## PyArrow-backed Pandas 2.0 DataFrames

Arrow already supports zero-copy conversion from Arrow tables to Pandas 1.x DataFrames for a limited subset of types (foremost int and float types). 
Arrowは、限られたタイプのサブセット（主にintおよびfloatタイプ）に対して、ArrowテーブルからPandas 1.x DataFrameへのゼロコピー変換をすでにサポートしています。
Other types, such as strings, usually come with a minor runtime and memory overhead for the conversion (<10% end-to-end for an in-memory training dataset with 50M rows and 3 numeric, 2 string columns). 
文字列などの他のタイプは、通常、変換に対してわずかなランタイムおよびメモリオーバーヘッドが伴います（50M行と3つの数値、2つの文字列列を持つインメモリトレーニングデータセットの場合、エンドツーエンドで10%未満）。
With Pandas 2.0’s PyArrow-backed Pandas DataFrames this overhead can be fully alleviated. 
Pandas 2.0のPyArrowバックのPandas DataFrameを使用することで、このオーバーヘッドは完全に軽減されます。
Since downstream libraries like scikit-learn do not fully support such types, yet, we will maintain support of regular Pandas types by default and offer PyArrow-backed DataFrames as an optional feature in the future. 
scikit-learnのような下流ライブラリがまだそのようなタイプを完全にはサポートしていないため、私たちはデフォルトで通常のPandasタイプのサポートを維持し、将来的にはPyArrowバックのDataFrameをオプション機能として提供します。



## Summary 概要

This blog post introduces a new service in Hopsworks, ArrowFlight with DuckDB, which offers significant performance improvements for Python clients reading/writing with feature data. 
このブログ記事では、Hopsworksにおける新しいサービス、DuckDBを用いたArrowFlightを紹介します。このサービスは、機能データの読み書きを行うPythonクライアントに対して、重要なパフォーマンス向上を提供します。

We chose to build a service rather than making our feature store clients heavier by embedding DuckDB and the drivers required to access the many different offline stores supported in Hopsworks. 
私たちは、Hopsworksでサポートされているさまざまなオフラインストアにアクセスするために必要なDuckDBとドライバを埋め込むことで、機能ストアクライアントを重くするのではなく、サービスを構築することを選びました。

We showed in benchmarks up to 45X throughput improvements compared to existing feature stores, showing the value of working with Arrow data end-to-end, from the lakehouse to Pandas clients. 
私たちは、ベンチマークで既存の機能ストアと比較して最大45倍のスループット向上を示し、レイクハウスからPandasクライアントまで、Arrowデータをエンドツーエンドで扱うことの価値を示しました。

We have built a bridge for Python-native access to Lakehouse Data in Hopsworks, and we hope it will enable Python developers to be more productive working with our feature store. 
私たちは、HopsworksにおけるレイクハウスデータへのPythonネイティブアクセスのためのブリッジを構築しました。これにより、Python開発者が私たちの機能ストアを使ってより生産的に作業できることを期待しています。



## References 参考文献
### Interested for more? もっと興味がありますか？
- 🤖 Register for free on Hopsworks Serverless 
- 🌐 Read about the open, disaggregated AI Lakehouse stack 
- 📚 Get your early copy: O'Reilly's 'Building Machine Learning Systems' book 
- 🛠️ Explore all Hopsworks Integrations 
- 🧩 Get started with codes and examples 
- ⚖️ Compare other Feature Stores with Hopsworks 



### More blogs もっとブログ

#### Common Error Messages in Pandas Pandasにおける一般的なエラーメッセージ
We go through the most common errors messages in Pandas and offer solutions to these errors as well as provide efficiency tips for Pandas code. 
私たちはPandasにおける最も一般的なエラーメッセージを解説し、これらのエラーに対する解決策を提供するとともに、Pandasコードの効率化のためのヒントを提供します。

#### Migrating from AWS to a European Cloud - How We Cut Costs by 62% AWSからヨーロッパのクラウドへの移行 - 62%のコスト削減方法
This post describes how we successfully migrated our serverless offering from AWS US-East to OVHCloud North America, reducing our monthly spend from $8,000 to $3,000 with no loss in service quality. 
この投稿では、私たちがAWS US-EastからOVHCloud North Americaにサーバーレスサービスを成功裏に移行し、月々の支出を$8,000から$3,000に削減した方法を説明します。サービス品質の低下はありません。

#### Hopsworks 3.0: The Python-Centric Feature Store Hopsworks 3.0: Python中心のフィーチャーストア
Hopsworks is the first feature store to extend its support from the traditional Big Data platforms to the Pandas-sized data realm, where Python reigns supreme. A new Python API is also provided. 
Hopsworksは、従来のビッグデータプラットフォームからPandasサイズのデータ領域にサポートを拡張した最初のフィーチャーストアです。ここではPythonが優位に立っています。また、新しいPython APIも提供されています。

© Hopsworks 2025. All rights reserved. Various trademarks held by their respective owners. 
© Hopsworks 2025. 全著作権所有。さまざまな商標はそれぞれの所有者に帰属します。

Google Tag Manager (noscript) 
Google Tag Manager (noscript)

End Google Tag Manager (noscript) 
Google Tag Manager (noscript)の終了

Cloudflare Web Analytics 
Cloudflare Web Analytics

End Cloudflare Web Analytics 
Cloudflare Web Analyticsの終了



## Notice お知らせ

We   and selected third parties   use cookies or similar technologies for technical purposes and, with your consent, for other purposes as specified in the cookie policy.
私たちと選ばれた第三者は、技術的目的のためにクッキーまたは類似の技術を使用し、あなたの同意に基づいて、クッキー方針に記載された他の目的のためにも使用します。
Use the “Accept” button to consent. Use the “Reject” button or close this notice to continue without accepting.
「受け入れる」ボタンを使用して同意してください。「拒否する」ボタンを使用するか、この通知を閉じて受け入れずに続行してください。
