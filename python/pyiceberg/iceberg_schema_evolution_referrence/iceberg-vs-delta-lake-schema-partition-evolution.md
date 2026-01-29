refs: https://www.chaosgenius.io/blog/iceberg-vs-delta-lake-schema-partition/

# 1. Apache Iceberg vs Delta Lake (II): Schema and Partition Evolution Apache Iceberg vs Delta Lake（II）：スキーマとパーティションの進化

In part one of Apache Iceberg vs Delta Lake we compared Apache Iceberg vs Delta Lake across origin, architecture, metadata management, query engine compatibility, and ACID transactions.
Apache Iceberg vs Delta Lakeの第1部では、起源、アーキテクチャ、メタデータ管理、クエリエンジンの互換性、ACIDトランザクションに関してApache IcebergとDelta Lakeを比較しました。
Now, in this second part, we’ll compare them on schema evolution, partition evolution, data skipping and indexing, performance, scalability, ecosystem, and use cases.
さて、この第2部では、スキーマの進化、パーティションの進化、データスキップとインデックス作成、パフォーマンス、スケーラビリティ、エコシステム、ユースケースについて比較します。

## 1.1. Schema Evolution—Apache Iceberg vs Delta Lake スキーマの進化—Apache Iceberg vs Delta Lake

### 1.1.1. Apache Iceberg

Apache Iceberg is great at schema evolution, allows adding, dropping, and reordering columns, and widening column types.
**Apache Icebergはスキーマ進化に優れており、列の追加、削除、並べ替え、列の型の拡張を許可**します。
These changes are stored in the metadata files so you can query historical data even after schema changes.
これらの変更はメタデータファイルに保存されるため、スキーマ変更後でも履歴データをクエリできます。
This is critical for long-term data management as it avoids having to rewrite data files when schema changes happen.
これは、スキーマ変更が発生した際にデータファイルを再書き込みする必要がなくなるため、長期的なデータ管理にとって重要です。

<!-- ここまで読んだ! -->

### 1.1.2. Delta Lake Delta Lake

Delta Lake also supports schema evolution but it’s limited compared to Iceberg.
**Delta Lakeもスキーマの進化をサポートしていますが、Icebergと比較すると制限があります。**(あ、そうなのか...!:thinking:)
It allows adding columns and widening column types but has restrictions on other types of changes.
列の追加や列の型の拡張は可能ですが、他の種類の変更には制限があります。
Schema changes in Delta Lake are stored in the delta log which tracks all changes to the table’s schema and data.
Delta Lakeのスキーマ変更は、テーブルのスキーマとデータへのすべての変更を追跡するデルタログに保存されます。

<!-- ここまで読んだ! -->

## 1.2. Partition Evolution—Apache Iceberg vs Delta Lake パーティションの進化—Apache Iceberg vs Delta Lake

### 1.2.1. Apache Iceberg

One of the coolest features of Apache Iceberg is partition evolution.
**Apache Icebergの最も素晴らしい機能の1つは、パーティション進化**です。
You can change the partitioning scheme of a table without having to rewrite the data.
データを再書き込みすることなく、テーブルのパーティショニングスキームを変更できます。
This is especially useful for large tables where repartitioning would be too expensive.
これは、再パーティショニングが高コストになる大規模なテーブルに特に便利です。
Iceberg does this through its manifest files which store detailed metadata about the partitions and data files.
Icebergは、パーティションとデータファイルに関する詳細なメタデータを保存するマニフェストファイルを通じてこれを実現します。

### 1.2.2. Delta Lake

Delta Lake has been working on partition evolution but it’s not as featureful or integrated as Iceberg’s.
**Delta Lakeはパーティションの進化に取り組んでいますが、Icebergのように機能が豊富で統合されているわけではありません。**(この点もIcebergの方が進んでるのか...!:thinking:)
While recent versions have added some support, Apache Iceberg is still more advanced in this area.
最近のバージョンではいくつかのサポートが追加されましたが、Apache Icebergはこの分野で依然としてより進んでいます。

## 1.3. Data Skipping and Indexing—Apache Iceberg vs Delta Lake データスキップとインデックス作成—Apache Iceberg vs Delta Lake

Both Apache Iceberg vs Delta Lake use data skipping to improve query performance but they do it in slightly different ways:
Apache IcebergとDelta Lakeの両方は、クエリパフォーマンスを向上させるためにデータスキップを使用しますが、わずかに異なる方法で行います。(partition pruningの話かな...?:thinking:)

### 1.3.1. Apache Iceberg 

Apache Iceberg stores statistics about each data file in the manifest files, including min/max values for columns and null counts.
Apache Icebergは、列の最小/最大値やNULLカウントを含む各データファイルの統計をマニフェストファイルに保存します。
This allows the query engine to skip entire data files, and speed up the query.
これにより、クエリエンジンはデータファイル全体をスキップでき、クエリを高速化します。
This distributed approach allows Iceberg to manage metadata more efficiently.
この分散アプローチにより、Icebergはメタデータをより効率的に管理できます。

### 1.3.2. Delta Lake

Delta Lake also collects statistics and stores them in the delta log.
Delta Lakeも統計を収集し、それをデルタログに保存します。
These can be used for data skipping but the centralized nature of the delta log can make it less efficient than Iceberg’s distributed approach.
これらはデータスキップに使用できますが、**デルタログの集中型の性質はIcebergの分散アプローチよりも効率が悪くなる可能性**があります。
Delta Lake relies on checkpoint files to summarize these statistics periodically which adds some overhead.
Delta Lakeは、これらの統計を定期的に要約するためにチェックポイントファイルに依存しており、これがいくつかのオーバーヘッドを追加します。

<!-- ここまで読んだ! -->

## 1.4. Performance and Scalability—Apache Iceberg vs Delta Lake パフォーマンスとスケーラビリティ—Apache Iceberg vs Delta Lake

When comparing Apache Iceberg vs Delta Lake for performance and scalability, there are several key differences to consider, based on their architectures and feature sets.
Apache IcebergとDelta Lakeのパフォーマンスとスケーラビリティを比較する際には、アーキテクチャと機能セットに基づいて考慮すべきいくつかの重要な違いがあります。

### 1.4.1. Apache Iceberg Performance　

- Metadata Management: Iceberg has great metadata management.
  - メタデータ管理：Icebergは優れたメタデータ管理を提供します。
    By breaking down metadata into manifest files, manifest list files, and metadata files, Iceberg can plan and execute queries efficiently.
    **メタデータをマニフェストファイル、マニフェストリストファイル、メタデータファイルに分解することで、Icebergは効率的にクエリを計画し実行できます。**
    This allows Iceberg to prune partitions well, which helps with query performance, especially for highly selective queries.
    これにより、Icebergはパーティションを適切にプルーニングでき、特に選択性の高いクエリのパフォーマンス向上に寄与します。

- Write Strategy: Iceberg's primary write strategy for updates and deletes is Copy-on-Write (CoW).
  - 書き込み戦略：**Icebergの更新および削除の主な書き込み戦略はCopy-on-Write（CoW）**です。
    In this approach, when data is modified, the affected data files are rewritten entirely.
    このアプローチでは、**データが変更されると、影響を受けたデータファイルが完全に再書き込みされます。** (overwriteとかってことだよね...! 単にappendの場合は新しいデータファイルが増えるはず:thinking:)
    While this can lead to write amplification for frequent updates, reads are generally fast as they only process valid, non-overlapping data files. 
    **これは頻繁な更新に対して書き込み増幅を引き起こす可能性がありますが**、読み取りは一般的に速く、有効な非重複データファイルのみを処理します。
    Iceberg also offers an optional Merge-on-Read (MoR) strategy, especially beneficial for streaming workloads or high write throughput, where changes are recorded as 'diffs' and merged at read time, though this can increase read complexity. 
    Icebergは、オプションのMerge-on-Read（MoR）戦略も提供しており、特にストリーミングワークロードや高い書き込みスループットに有益です。ここでは、変更が「diff」として記録され、読み取り時にマージされますが、これにより読み取りの複雑さが増す可能性があります。

<!-- ここまで読んだ! -->

### 1.4.2. Delta Lake Performance Delta Lakeのパフォーマンス

- Data Skipping and Compaction: Delta Lake has data skipping and automatic compaction. 
データスキップとコンパクション：Delta Lakeはデータスキップと自動コンパクションを備えています。
It categorizes data files by metadata to skip unnecessary data during queries. 
メタデータによってデータファイルを分類し、クエリ中に不要なデータをスキップします。
It also compacts small Parquet files into larger ones periodically, reducing the overhead of managing many small files and thus query performance. 
また、**小さなParquetファイルを定期的に大きなファイルに圧縮**し、多くの小さなファイルを管理するオーバーヘッドを削減し、クエリパフォーマンスを向上させます。

- Write Strategy (Copy-on-Write): Delta Lake primarily uses a Copy-on-Write (CoW) strategy for updates and deletes, where modified data records result in new files being written, and old files are marked for removal. 
書き込み戦略（Copy-on-Write）：Delta Lakeは主に更新と削除のためにCopy-on-Write（CoW）戦略を使用しており、変更されたデータレコードは新しいファイルの書き込みを引き起こし、古いファイルは削除のためにマークされます。
This approach ensures transactional consistency and simplifies read operations, as readers only see the latest, consistent version of the data. 
このアプローチはトランザクションの一貫性を確保し、リーダーがデータの最新で一貫したバージョンのみを表示するため、読み取り操作を簡素化します。
While it can lead to write amplification, Delta Lake's optimizations help manage this effectively. 
書き込み増幅を引き起こす可能性がありますが、Delta Lakeの最適化はこれを効果的に管理するのに役立ちます。

<!-- ここまで読んだ! -->

### 1.4.3. Apache Iceberg Scalability　Apache Icebergのスケーラビリティ

- Scalability: Apache Iceberg can handle petabyte-scale datasets easily, supports partition evolution and schema evolution without having to rewrite a lot of data. 
  - スケーラビリティ：**Apache Icebergはペタバイト規模のデータセットを容易に処理でき、データを多く書き換えることなくパーティションの進化とスキーマの進化をサポート**します。
This makes Iceberg very scalable and can handle a lot of data without performance degradation. 
これにより、Icebergは非常にスケーラブルであり、パフォーマンスの低下なしに大量のデータを処理できます。

- Flexibility: Apache Iceberg’s architecture can be used with various data processing engines and storage formats, Avro, ORC, and Parquet, so flexible in integration and scalability across different environments. 
  - 柔軟性：Apache Icebergのアーキテクチャは、さまざまなデータ処理エンジンやストレージフォーマット（Avro、ORC、Parquet）と共に使用できるため、異なる環境での統合とスケーラビリティに柔軟です。

<!-- ここまで読んだ! -->

### 1.4.4. Delta Lake Scalability Delta Lakeのスケーラビリティ

- High Scalability: Delta Lake is known for its high scalability and reliability, good for large-scale data processing. 
  - 高いスケーラビリティ：Delta Lakeはその高いスケーラビリティと信頼性で知られており、大規模データ処理に適しています。
  It can handle complex operations and large datasets well, partly because of its robust transaction log and checkpointing mechanism which maintains data consistency and integrity. 
  複雑な操作や大規模データセットをうまく処理できるのは、データの一貫性と整合性を維持する堅牢なトランザクションログとチェックポイントメカニズムのおかげです。

- Compaction and Optimization: Delta Lake’s continuous optimization, auto-compaction and data skipping, helps it scale well. 
  - コンパクションと最適化：Delta Lakeの継続的な最適化、自動コンパクション、データスキップは、スケーラビリティを向上させます。
  These ensures the data lake remains performant even as data grows. 
  これにより、データが増加してもデータレイクのパフォーマンスが維持されます。

<!-- ここまで読んだ! -->

## 1.5. Ecosystem and Community Support—Apache Iceberg vs Delta Lake　エコシステムとコミュニティサポート—Apache Iceberg対Delta Lake

In the open source world, the strength of a project often lies in its community. 
**オープンソースの世界では、プロジェクトの強さはしばしばそのコミュニティにあります。**(なるほど確かにね...!:thinking:)
Let’s take a look at the ecosystems surrounding Apache Iceberg vs Delta Lake. 
Apache IcebergとDelta Lakeを取り巻くエコシステムを見てみましょう。

### 1.5.1. Apache Iceberg—A Diverse Community 多様なコミュニティ

Since being adopted by the Apache Software Foundation, Apache Iceberg has grown its contributor base exponentially. 
Apache Software Foundationに採用されて以来、Apache Icebergはその貢献者ベースを急速に拡大しています。
What was a Netflix project now has contributors from many companies including: 
元々はNetflixのプロジェクトでしたが、現在は以下のような多くの企業からの貢献者がいます：

- Apple
- Amazon Web Services
- Alibaba
- Dremio
- Cloudera
- LinkedIn

The Iceberg community is open and collaborative. 
**Icebergコミュニティはオープンで協力的**です。
Regular community meetings, active mailing lists, and a welcoming attitude towards new contributors has created a thriving ecosystem around the project. 
定期的なコミュニティミーティング、活発なメーリングリスト、新しい貢献者に対する歓迎の姿勢が、プロジェクトの周りに活気あるエコシステムを生み出しています。

<!-- ここまで読んだ! -->

### 1.5.2. Delta Lake—Databricks-Led but Growing Delta Lake—Databricks主導だが成長中

Delta Lake’s community is growing but still heavily Databricks-led. 
Delta Lakeのコミュニティは成長していますが、依然としてDatabricks主導です。
This isn’t necessarily a bad thing – Databricks expertise has been instrumental in shaping Delta Lake. 
これは必ずしも悪いことではありません。Databricksの専門知識はDelta Lakeの形成において重要な役割を果たしています。
But it means the project’s direction is more tied to Databricks roadmap than Iceberg is to any one company. 
しかし、これはプロジェクトの方向性がIcebergが特定の企業に結びついているよりも、Databricksのロードマップにより結びついていることを意味します。
But Delta Lake is building a more diverse community. 
しかし、Delta Lakeはより多様なコミュニティを構築しています。
IBM and Walmart have contributed to the project. 
IBMやWalmartがこのプロジェクトに貢献しています。
Open sourcing has also opened the door for smaller companies and individual contributors to get involved. 
オープンソース化により、小規模企業や個人の貢献者が関与する機会も広がりました。
One benefit of Delta Lake being Databricks-led is the availability of commercial support and tooling. 
Delta LakeがDatabricks主導であることの利点の一つは、商業的なサポートとツールの利用可能性です。
For companies already in the Databricks ecosystem, this is a big plus. 
すでにDatabricksエコシステムにいる企業にとって、これは大きな利点です。

<!-- ここまで読んだ! -->

## 1.6. Data Manipulation (DML Operations)—Apache Iceberg vs Delta Lake　データ操作（DML操作）—Apache Iceberg対Delta Lake

Both Apache Iceberg and Delta Lake provide full Data Manipulation Language (DML) support, including INSERT, UPDATE, DELETE, and MERGE operations, enabling transactional capabilities directly on data lake storage. 
**Apache IcebergとDelta Lakeの両方は、INSERT、UPDATE、DELETE、MERGE操作を含む完全なデータ操作言語（DML）サポートを提供**し、データレイクストレージ上で直接トランザクション機能を可能にします。

### 1.6.1. Apache Iceberg　

Iceberg supports INSERT INTO, MERGE INTO, and INSERT OVERWRITE statements. 
IcebergはINSERT INTO、MERGE INTO、INSERT OVERWRITE文をサポートしています。
When executing UPDATE or DELETE operations, Iceberg primarily uses a Copy-on-Write (CoW) approach by default. 
UPDATEまたはDELETE操作を実行する際、**IcebergはデフォルトでCopy-on-Write（CoW）アプローチ**を主に使用します。
This means if even a single row in a data file is modified or deleted, the entire data file is rewritten, and the new snapshot points to the rewritten file. 
**これは、データファイル内の単一の行が変更または削除された場合でも、データファイル全体が再書き込みされ、新しいスナップショットが再書き込みされたファイルを指すこと**を意味します。
For DELETE operations where an entire partition or set of files can be pruned by the filter, Iceberg can perform a metadata-only delete without rewriting data. 
フィルターによって全体のパーティションまたはファイルセットを剪定できるDELETE操作の場合、Icebergはデータを書き換えることなくメタデータのみの削除を実行できます。

Iceberg also offers an optional Merge-on-Read (MoR) strategy for row-level updates and deletes. 
Icebergは、**行レベルの更新と削除のためのオプションのMerge-on-Read（MoR）戦略**も提供しています。
In MoR, instead of rewriting data files immediately, a "delete file" is generated to track which records need to be ignored (positional deletes) or which values have changed (equality deletes). 
MoRでは、データファイルを即座に書き換えるのではなく、無視する必要があるレコード（位置削除）や変更された値（等価削除）を追跡するための「削除ファイル」が生成されます。
This can reduce write amplification, particularly for frequent small updates or streaming workloads, but queries may incur additional overhead to merge data and delete files at read time. 
これにより、特に頻繁な小規模更新やストリーミングワークロードに対して書き込み増幅を減少させることができますが、クエリは読み取り時にデータと削除ファイルをマージするための追加のオーバーヘッドが発生する可能性があります。
MERGE INTO operations are supported by rewriting affected data files in an overwrite commit. 
MERGE INTO操作は、上書きコミットで影響を受けるデータファイルを書き換えることによってサポートされています。

<!-- ここまで読んだ! -->

### 1.6.2. Delta Lake　

Delta Lake fully supports UPDATE, DELETE, and MERGE INTO operations, treating them as atomic transactions. 
Delta LakeはUPDATE、DELETE、MERGE INTO操作を完全にサポートしており、これらを原子的なトランザクションとして扱います。
For DELETE operations, Delta Lake first identifies data files containing rows that match the predicate. 
DELETE操作の場合、Delta Lakeは最初に述語に一致する行を含むデータファイルを特定します。
It then rewrites these files, excluding the deleted rows, and marks the old files as "tombstoned" in the transaction log. 
次に、削除された行を除外してこれらのファイルを書き換え、古いファイルをトランザクションログで「墓石」としてマークします。
UPDATE operations follow a similar Copy-on-Write (CoW) mechanism: files containing updated rows are rewritten with the new values. 
UPDATE操作は、同様のCopy-on-Write（CoW）メカニズムに従います：更新された行を含むファイルは新しい値で書き換えられます。(じゃあここはIcebergと同じくCoWなんだね:thinking:)

The MERGE INTO operation in Delta Lake is powerful, allowing for upserts (update or insert), deletes, and inserts based on join conditions between a source and target table. 
Delta LakeのMERGE INTO操作は強力で、ソーステーブルとターゲットテーブル間の結合条件に基づいてアップサート（更新または挿入）、削除、挿入を可能にします。
Delta Lake performs a two-step MERGE process: an inner join to identify files with matches, followed by an outer join to write out updated, deleted, or inserted data. 
Delta Lakeは二段階のMERGEプロセスを実行します：一致するファイルを特定するための内部結合の後、更新された、削除された、または挿入されたデータを書き出すための外部結合を行います。
Performance for these DML operations in Delta Lake can be optimized by adding more predicates to narrow down the search space, especially on partition columns. 
Delta LakeにおけるこれらのDML操作のパフォーマンスは、検索空間を狭めるためにより多くの述語を追加することで最適化できます。特にパーティション列においてです。

<!-- ここまで読んだ! -->

## 1.7. Use Cases and Adoption—Apache Iceberg vs Delta Lake　ユースケースと採用—Apache Iceberg対Delta Lake

Both Apache Iceberg vs Delta Lake aim to solve similar problems. 
Apache IcebergとDelta Lakeの両方は、類似の問題を解決することを目指しています。
But, their different approaches and strengths make them better for certain use cases. 
しかし、彼らの異なるアプローチと強みは、特定のユースケースにおいてより適しています。
Let's explore some key considerations: 
いくつかの重要な考慮事項を探ってみましょう。

### 1.7.1. Apache Iceberg

Apache Iceberg is designed for big data management at scale, especially in the cloud. 
Apache Icebergは、大規模なビッグデータ管理のために設計されており、特にクラウドでの使用に適しています。
It shines in high-performance analytics and transactional consistency. 
高性能な分析とトランザクションの一貫性において優れています。
Here are some use cases: 
以下は、いくつかのユースケースです：

1) Transactional Data Lakes トランザクショナルデータレイク

As we have already mentioned, Apache Iceberg supports ACID transactions so it’s great for building transactional data lakes. 
前述のように、Apache IcebergはACIDトランザクションをサポートしているため、**トランザクショナルデータレイクの構築に最適**です。
It allows for reliable data ingestion and transformation with robust support for updates, deletes, and merges. 
更新、削除、マージの堅牢なサポートにより、信頼性の高いデータの取り込みと変換を可能にします。

2) Data Versioning and Time Travel データバージョニングとタイムトラベル

It keeps historical versions of the data so you can do data versioning and time travel for auditing and compliance. 
**データの履歴バージョンを保持**するため、監査やコンプライアンスのためのデータバージョニングやタイムトラベルが可能です。

3) Incremental Processing 増分処理

Apache Iceberg’s incremental processing helps with efficient ETL workflows by only processing the changed data, reducing compute cost and time. 
**Apache Icebergの増分処理は、変更されたデータのみを処理することで効率的なETLワークフローを支援**し、計算コストと時間を削減します。
(これでストリーミング的な増分処理がやりやすくなってるのか...! 新しく更新された特徴量レコードだけを抜き出す、とかが容易ってことだよね...!!:thinking:)


4) パーティションの進化

Apache Iceberg allows for dynamic partitioning and evolution without hurting query performance which is great for large and evolving datasets. 
Apache Icebergは、クエリパフォーマンスを損なうことなく動的なパーティショニングと進化を可能にし、大規模で進化するデータセットに最適です。
Apache Iceberg is used across many industries because of its flexibility and support for multiple data processing engines. 
**Apache Icebergは、その柔軟性と複数のデータ処理エンジンへのサポートにより、多くの業界で使用されています。**
Notable users include Netflix (its original developer), Apple, LinkedIn, Airbnb and many more. 
著名なユーザーには、Netflix（元の開発者）、Apple、LinkedIn、Airbnbなどが含まれます。
The open source and community backing has led to its inclusion in multiple cloud platforms so it can be used in enterprise environments. 
オープンソースとコミュニティの支援により、複数のクラウドプラットフォームへの組み込みが実現し、企業環境で使用できるようになりました。

<!-- ここまで読んだ! -->

### 1.7.2. Delta Lake

Delta Lake by is all about reliability and performance for data lakes. 
Delta Lakeは、データレイクの信頼性とパフォーマンスに関するものです。
It’s tightly integrated with Apache Spark so it’s great for: 
Apache Sparkと密接に統合されているため、以下の用途に最適です：

1) Real-time Data Processing リアルタイムデータ処理

Delta Lake’s ACID transactions and support for both batch and streaming data workloads means real-time data processing and analytics for modern data pipelines. 
Delta LakeのACIDトランザクションとバッチおよびストリーミングデータワークロードの両方のサポートにより、現代のデータパイプラインにおけるリアルタイムデータ処理と分析が可能になります。

2) Data Warehousing データウェアハウジング

It has robust data warehousing capabilities with schema enforcement, data validation and indexing for high query performance and data integrity. 
スキーマの強制、データ検証、インデックス作成を備えた堅牢なデータウェアハウジング機能があり、高いクエリパフォーマンスとデータの整合性を実現します。

3) Unified Batch and Streaming バッチとストリーミングの統合

It supports both batch and real-time streaming data processing, making it suitable for real-time analytics and ETL pipelines. 
バッチとリアルタイムストリーミングデータ処理の両方をサポートしており、リアルタイム分析やETLパイプラインに適しています。

4) Machine Learning Pipelines 機械学習パイプライン

Delta Lake’s integration with Databricks and Spark makes it easy to create and manage machine learning pipelines and data preparation and model training. 
Delta LakeのDatabricksおよびSparkとの統合により、機械学習パイプラインやデータ準備、モデル訓練の作成と管理が容易になります。

5) Data Lakehouse Architectures

Delta Lake supports the data lakehouse architecture combining the flexibility of data lakes with the performance and ACID transactions of data warehouses for diverse analytical workloads. 
Delta Lakeは、データレイクの柔軟性とデータウェアハウスのパフォーマンスおよびACIDトランザクションを組み合わせたデータレイクハウスアーキテクチャをサポートし、多様な分析ワークロードに対応します。

6) Time Travel and Data Versioning タイムトラベルとデータバージョニング

Delta Lake allows time travel capabilities, enabling users to query historical data and rollback to previous versions, which is crucial for debugging and auditing purposes. 
Delta Lakeはタイムトラベル機能を提供し、ユーザーが履歴データをクエリし、以前のバージョンにロールバックできるようにします。これはデバッグや監査の目的において重要です。
Delta Lake has seen wide adoption especially within Databricks users. 
Delta Lakeは特にDatabricksユーザーの間で広く採用されています。
Its tight integration with Spark makes it the choice for companies that need scalable and performant data lakes. 
Sparkとの密接な統合により、スケーラブルでパフォーマンスの高いデータレイクを必要とする企業にとっての選択肢となっています。
The feature set and backing from Databricks is growing its adoption in data driven companies. 
機能セットとDatabricksからの支援により、データ駆動型企業での採用が増加しています。

<!-- ここまで読んだ! -->

## 1.8. Choosing Between Apache Iceberg vs Delta Lake Apache IcebergとDelta Lakeの選択

You made it to the end! We’ve covered the similarities and differences between Apache Iceberg vs Delta Lake.
最後までお読みいただきありがとうございます！Apache IcebergとDelta Lakeの類似点と相違点について説明しました。
Now which one should you choose?
さて、どちらを選ぶべきでしょうか？

### 1.8.1. Use Apache Iceberg if: Apache Icebergを使用する場合：

- Your use case involves complex data types or rapidly evolving schemas.
  - あなたのユースケースが複雑なデータ型や**急速に進化するスキーマを含む場合**。
- You need a vendor-neutral, community-driven solution that integrates with a wide range of technologies.
  - 幅広い技術と統合できるベンダーニュートラルでコミュニティ主導のソリューションが必要です。
- Scalability and robust metadata management are priorities for your data architecture.
  - スケーラビリティと堅牢なメタデータ管理がデータアーキテクチャの優先事項である場合。

### 1.8.2. Use Delta Lake if: Delta Lakeを使用する場合：

- You require strict data consistency and versioning, along with time travel capabilities.
  - 厳密なデータの一貫性とバージョニング、さらにタイムトラベル機能が必要な場合。
- High performance in data processing and query efficiency is crucial.
  - データ処理とクエリ効率において高いパフォーマンスが重要です。
- You are deeply integrated into the Databricks ecosystem or require seamless integration with specific cloud platforms and big data tools.
  - **Databricksエコシステムに深く統合されているか**、特定のクラウドプラットフォームやビッグデータツールとのシームレスな統合が必要な場合。

---

Here is the overall summary:
全体の要約は以下の通りです：

![]()

<!-- ここまで読んだ! -->

## 1.9. Conclusion 結論

And that's a wrap! 
これでおしまいです！
Apache Iceberg and Delta Lake are both powerful open table formats for data lakehouses. 
Apache IcebergとDelta Lakeは、データレイクハウスのための強力なオープンテーブルフォーマットです。
Iceberg shines in schema evolution, complex data types, and vendor neutrality. 
**Icebergは、スキーマの進化、複雑なデータ型、ベンダーの中立性において優れています。**
Delta Lake excels in ACID compliance, performance optimization, and Databricks integration. 
Delta Lakeは、ACID準拠、パフォーマンス最適化、Databricksとの統合において優れています。
Choose based on your project's specific requirements, existing ecosystem, and desired features. 
プロジェクトの特定の要件、既存のエコシステム、および望ましい機能に基づいて選択してください。

<!-- ここまで読んだ! -->

## 1.10. FAQs よくある質問

- How does Apache Iceberg handle schema evolution?

Apache Iceberg allows adding, dropping, and reordering columns, and widening column types. 
Apache Icebergは、列の追加、削除、並べ替え、列の型の拡張を可能にします。 
These changes are stored in metadata files, enabling queries on historical data even after schema changes.
これらの変更はメタデータファイルに保存され、スキーマ変更後でも履歴データに対するクエリを可能にします。

- What are the limitations of Delta Lake in terms of schema evolution?

Delta Lake supports adding columns and widening column types but has restrictions on other types of changes. 
Delta Lakeは列の追加と列の型の拡張をサポートしていますが、他の種類の変更には制限があります。 
Schema changes are stored in the delta log.
スキーマ変更はデルタログに保存されます。

- What is the Delta Log in Delta Lake?

Delta Log is a transaction log that records every change to Delta Lake tables, ensuring data integrity and enabling features like time travel.
Delta Logは、Delta Lakeテーブルへのすべての変更を記録するトランザクションログであり、データの整合性を確保し、タイムトラベルのような機能を可能にします。

- How does Apache Iceberg handle metadata management?

Apache Iceberg uses a three-tier metadata architecture consisting of the Iceberg catalog, metadata files, and data files.
Apache Icebergは、Icebergカタログ、メタデータファイル、およびデータファイルからなる三層のメタデータアーキテクチャを使用します。

- What is partition evolution, and how does Apache Iceberg implement it?

Partition evolution allows changing the partitioning scheme of a table without rewriting data. 
パーティション進化は、データを書き換えることなくテーブルのパーティショニングスキームを変更することを可能にします。 
Iceberg implements this through manifest files which store detailed metadata about partitions and data files.
Icebergは、パーティションとデータファイルに関する詳細なメタデータを保存するマニフェストファイルを通じてこれを実装します。

- How does Delta Lake handle data skipping?

Delta Lake uses data skipping by collecting statistics and storing them in the delta log, which can be used to skip unnecessary data during queries.
Delta Lakeは、統計を収集し、それをデルタログに保存することでデータスキップを実現し、クエリ中に不要なデータをスキップすることができます。

- How does Apache Iceberg implement data skipping to improve query performance?

Iceberg stores statistics about each data file in manifest files, including min/max values for columns and null counts. 
Icebergは、各データファイルに関する統計をマニフェストファイルに保存し、列の最小/最大値やNULLカウントを含みます。 
This allows query engines to skip entire data files, speeding up queries.
これにより、クエリエンジンは全データファイルをスキップでき、クエリの速度が向上します。

- What approach does Delta Lake use for data skipping?

Delta Lake collects statistics and stores them in the delta log. 
Delta Lakeは統計を収集し、それをデルタログに保存します。 
It uses checkpoint files to summarize these statistics periodically.
定期的にこれらの統計を要約するためにチェックポイントファイルを使用します。

- What is the key difference in metadata management between Apache Iceberg vs Delta Lake? メタデータ管理におけるApache IcebergとDelta Lakeの主な違いは何ですか？

Iceberg uses a distributed approach with manifest files, while Delta Lake uses a centralized approach with the delta log.
Icebergはマニフェストファイルを使用した分散アプローチを採用しているのに対し、Delta Lakeはデルタログを使用した集中型アプローチを採用しています。

- What is the difference between merge-on-read and merge-on-write? マージオンリードとマージオンライトの違いは何ですか？

Merge-on-read (used by Iceberg) merges changes during read time, while merge-on-write (used by Delta Lake) writes changes to new files immediately.
Merge-on-read（Icebergが使用）では、読み取り時に変更をマージしますが、merge-on-write（Delta Lakeが使用）では、変更を新しいファイルに即座に書き込みます。

- What is merge-on-read, and which system uses this approach? マージオンリードとは何で、どのシステムがこのアプローチを使用していますか？

Merge-on-read is where read operations only fetch what's needed and changes are merged during read time. 
Merge-on-readは、読み取り操作が必要なものだけを取得し、変更が読み取り時にマージされることです。 
Apache Iceberg uses this approach.
Apache Icebergはこのアプローチを使用しています。

- Which query engines are compatible with Apache Iceberg? Apache Icebergと互換性のあるクエリエンジンは何ですか？

Apache Iceberg is compatible with Apache Spark, Apache Flink, Presto/Trino, Apache Hive, Apache Impala, and Dremio.
Apache Icebergは、Apache Spark、Apache Flink、Presto/Trino、Apache Hive、Apache Impala、およびDremioと互換性があります。

- What is Iceberg partitioning? Icebergパーティショニングとは何ですか？

Iceberg partitioning uses hidden partitioning techniques that dynamically partition data based on query patterns and usage. 
Icebergパーティショニングは、クエリパターンと使用に基づいてデータを動的にパーティショニングする隠れたパーティショニング技術を使用します。 
This approach allows for efficient query performance, minimizing the amount of data scanned and reducing latency compared to traditional static partitioning methods.
このアプローチにより、効率的なクエリパフォーマンスが可能になり、スキャンされるデータ量が最小限に抑えられ、従来の静的パーティショニング手法と比較してレイテンシが低減されます。

- What is the difference between Iceberg partitioning and Hive partitioning? IcebergパーティショニングとHiveパーティショニングの違いは何ですか？

Iceberg partitioning uses hidden partitioning, allowing dynamic partitioning without explicitly specifying partitions, leading to more efficient queries and reduced data scanning. 
Icebergパーティショニングは、隠れたパーティショニングを使用し、パーティションを明示的に指定することなく動的パーティショニングを可能にし、より効率的なクエリとデータスキャンの削減を実現します。 
However, Hive partitioning requires manual partition specification, which can be less flexible and slower for query performance due to extensive file listing operations.
ただし、Hiveパーティショニングは手動でのパーティション指定が必要であり、広範なファイルリスト操作のために柔軟性が低く、クエリパフォーマンスが遅くなる可能性があります。

<!-- ここまで読んだ! -->

- How does Delta Lake ensure data durability? Delta Lakeはどのようにデータの耐久性を確保していますか？

Delta Lake inherits durability guarantees from the underlying storage system (like S3 or HDFS) and uses Parquet-formatted checkpoint files to preserve historical data changes.
Delta Lakeは、基盤となるストレージシステム（S3やHDFSなど）から耐久性の保証を継承し、Parquet形式のチェックポイントファイルを使用して履歴データの変更を保持します。

How does Delta Lake's merge-on-write approach affect read and write performance?
Merge-on-write makes writes faster and more consistent but introduces some latency during reads.
Merge-on-writeは書き込みをより速く、一貫性のあるものにしますが、読み取り時にいくつかのレイテンシを導入します。

How does Apache Iceberg handle scalability for large datasets?
Iceberg can handle petabyte-scale datasets, supports partition and schema evolution without extensive data rewriting, and works with various data processing engines and storage formats.
Icebergはペタバイト規模のデータセットを処理でき、広範なデータの書き換えなしにパーティションとスキーマの進化をサポートし、さまざまなデータ処理エンジンやストレージフォーマットで動作します。

What features contribute to Delta Lake's scalability?
Delta Lake's scalability is supported by its robust transaction log, checkpointing mechanism, continuous optimization, auto-compaction, and data skipping.
Delta Lakeのスケーラビリティは、その堅牢なトランザクションログ、チェックポイントメカニズム、継続的な最適化、自動圧縮、およびデータスキップによって支えられています。

Which companies are notable contributors to the Apache Iceberg project?
Notable contributors include Apple, Amazon Web Services, Alibaba, Dremio, Cloudera, LinkedIn and more.
著名な貢献者には、Apple、Amazon Web Services、Alibaba、Dremio、Cloudera、LinkedInなどが含まれます。
