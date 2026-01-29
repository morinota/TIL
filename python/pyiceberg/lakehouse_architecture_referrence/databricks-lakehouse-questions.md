refs: https://www.databricks.com/blog/2021/08/30/frequently-asked-questions-about-the-data-lakehouse.html

# Frequently Asked Questions About the Data Lakehouse データレイクハウスに関するよくある質問



## Question Index 質問インデックス

What is a Data Lakehouse? 
Data Lakehouseとは何ですか？ 
What is a Data Lake? 
Data Lakeとは何ですか？ 
What is a Data Warehouse? 
Data Warehouseとは何ですか？ 
How is a Data Lakehouse different from a Data Warehouse? 
Data LakehouseはData Warehouseとどのように異なりますか？ 
How is the Data Lakehouse different from a Data Lake? 
Data LakehouseはData Lakeとどのように異なりますか？ 
How easy is it for data analysts to use a Data Lakehouse? 
データアナリストがData Lakehouseを使用するのはどれくらい簡単ですか？ 
How do Data Lakehouse systems compare in performance and cost to data warehouses? 
Data Lakehouseシステムは、パフォーマンスとコストの面でData Warehouseとどのように比較されますか？ 
What data governance functionality do Data Lakehouse systems support? 
Data Lakehouseシステムはどのようなデータガバナンス機能をサポートしていますか？ 
Does the Data Lakehouse have to be centralized or can it be decentralized into a Data Mesh? 
Data Lakehouseは集中型でなければならないのか、それともData Meshに分散させることができるのか？ 
How does the Data Mesh relate to the Data Lakehouse? 
Data MeshはData Lakehouseとどのように関連していますか？

## What is a Data Lakehouse? Data Lakehouseとは何ですか？

In short, a Data Lakehouse is an architecture that enables efficient and secure Artificial Intelligence (AI) and Business Intelligence (BI) directly on vast amounts of data stored in Data Lakes. 
簡単に言うと、Data Lakehouseは、Data Lakesに保存された膨大なデータに対して効率的かつ安全な人工知能（AI）とビジネスインテリジェンス（BI）を直接実現するアーキテクチャです。 

Explore why lakehouses are the data architecture of the future with the father of the data warehouse, Bill Inmon. 
データウェアハウスの父であるビル・インモンと共に、[なぜレイクハウスが未来のデータアーキテクチャであるのかを探求](https://www.databricks.com/resources/ebook/rise-data-lakehouse?itm_data=faqdl-blog-riselakehousebook)してください。 

Today, the vast majority of enterprise data lands in data lakes, low-cost storage systems that can manage any type of data (structured or unstructured) and have an open interface that any processing tool can run against. 
**今日、企業データの大多数は、あらゆる種類のデータ（構造化データまたは非構造化データ）を管理できる低コストのストレージシステムであるデータレイクに保存**されています。 
These data lakes are where most data transformation and advanced analytics workloads (such as AI) run to take advantage of the full set of data in the organization. 
これらのデータレイクは、組織内のデータの完全なセットを活用するために、ほとんどのデータ変換および高度な分析ワークロード（AIなど）が実行される場所です。 
Separately, for Business Intelligence (BI) use cases, proprietary data warehouse systems are used on a much smaller subset of the data that is structured. 
**一方、ビジネスインテリジェンス（BI）のユースケースでは、構造化データのはるかに小さなサブセットに対して、独自のデータウェアハウスシステムが使用**されます。 
These data warehouses primarily support BI, answering historical analytical questions about the past using SQL (e.g., what was my revenue last quarter), while the data lake stores a much larger amount of data and supports analytics using both SQL and non-SQL interfaces, including predictive analytics and AI (e.g. which of my customers will likely churn, or what coupons to offer at what time to my customers). 
これらのデータウェアハウスは主にBIをサポートし、SQLを使用して過去の歴史的な分析質問に答えます（例：前四半期の収益は何でしたか）。一方、データレイクははるかに多くのデータを保存し、SQLおよび非SQLインターフェースを使用した分析をサポートします。予測分析やAI（例：どの顧客が離脱する可能性が高いか、どのタイミングで顧客にどのクーポンを提供するか）を含みます。 
Historically, to accomplish both AI and BI, you would have to have multiple copies of the data and move it between data lakes and data warehouses. 
**歴史的に、AIとBIの両方を実現するためには、データの複数のコピーを持ち、データレイクとデータウェアハウスの間で移動させる必要がありました。** 
Today, the vast majority of enterprise data lands in 
今日、企業データの大多数はデータレイクに保存されています。

<!-- ここまで読んだ! -->

The Data Lakehouse enables storing all your data once in a data lake and doing AI and BI on that data directly. 
**Data Lakehouseは、すべてのデータを一度データレイクに保存し、そのデータに対して直接AIとBIを実行できるようにします。** (うんうん、これがレイクハウスアーキテクチャの思想なんだろうな :thinking:)
It has specific capabilities to efficiently enable both AI and BI on all the enterprise's data at a massive scale. 
それは、企業のすべてのデータに対してAIとBIの両方を効率的に実現するための特定の機能を持っています。 
Namely, it has the SQL and performance capabilities (indexing, caching, MPP processing) to make BI work fast on data lakes. 
具体的には、データレイク上でBIを迅速に機能させるためのSQLおよびパフォーマンス機能（インデックス作成、キャッシング、MPP処理）を備えています。 
It also has direct file access and direct native support for Python, data science, and AI frameworks without ever forcing it through a SQL-based data warehouse. 
また、SQLベースのデータウェアハウスを介さずに、直接ファイルアクセスとPython、データサイエンス、AIフレームワークへのネイティブサポートを提供します。 
The key technologies used to implement Data Lakehouses are open source, such as Delta Lake, Hudi, and Iceberg. 
**Data Lakehouseを実装するために使用される主要な技術は、Delta Lake、Hudi、Icebergなどのオープンソース**です。(一番活発なのはIcebergらしい!)
Vendors who focus on Data Lakehouses include, but are not limited to Databricks, AWS, Dremio, and Starburst. 
**Data Lakehouseに焦点を当てているベンダーには、Databricks、AWS、Dremio、Starburstなど**があります。(AWSはS3 Tablesとか??:thinking:)
Vendors who provide Data Warehouses include, but are not limited to, Teradata, Snowflake, and Oracle. 
データウェアハウスを提供するベンダーには、Teradata、Snowflake、Oracleなどがあります。 
Recently, Bill Inmon, widely considered the father of data warehousing, published a blog post on the Evolution of the Data Lakehouse explaining the unique ability of the lakehouse to manage data in an open environment while combining the data science focus of the data lake with the end-user analytics of the data warehouse.
最近、データウェアハウスの父と広く見なされているビル・インモンが、[データレイクハウスの進化に関するブログ記事](https://www.databricks.com/blog/2021/05/19/evolution-to-the-data-lakehouse.html)を公開し、データレイクのデータサイエンスの焦点とデータウェアハウスのエンドユーザー分析を組み合わせながら、**オープンな環境でデータを管理するレイクハウスの独自の能力**を説明しました。

<!-- ここまで読んだ! -->

## What is a Data Lake? 

A data lake is a low-cost, open, durable storage system for any data type - tabular data, text, images, audio, video, JSON, and CSV. 
データレイクは、**あらゆるデータタイプ（表形式データ、テキスト、画像、音声、動画、JSON、CSV）のための低コストでオープンな耐久性のあるストレージシステム**です。
In the cloud, every major cloud provider leverages and promotes a data lake, e.g. AWS S3, Azure Data Lake Storage (ADLS), Google Cloud Storage (GCS).
**クラウドでは、すべての主要なクラウドプロバイダーがデータレイクを活用し、推進**しています（例：AWS S3、Azure Data Lake Storage（ADLS）、Google Cloud Storage（GCS））。 
As a result, the vast majority of the data of most organizations is stored in cloud data lakes. 
その結果、ほとんどの組織のデータの大多数はクラウドデータレイクに保存されています。 
Over time, most organizations store their data in an open standardized format, typically either Apache Parquet format or ORC format. 
**時間が経つにつれて、ほとんどの組織はデータをオープンな標準形式（通常はApache Parquet形式またはORC形式）で保存します。** 
As a result, a large ecosystem of tools and applications can directly work with these open data formats. 
その結果、大規模なツールとアプリケーションのエコシステムがこれらのオープンデータ形式と直接連携できます。 
This approach of storing data in open formats, at a very low cost has enabled organizations to amass large quantities of data in data lakes while avoiding vendor lock-in. 
**オープン形式でデータを非常に低コストで保存するこのアプローチにより**、組織はデータレイクに大量のデータを蓄積し、ベンダーロックインを回避することができました。

<!-- ここまで読んだ! -->

At the same time, data lakes have suffered from three main problems - security, quality, and performance despite these advantages. 
同時に、データレイクはこれらの利点にもかかわらず、**主に3つの問題（セキュリティ、品質、パフォーマンス）**に悩まされています。 
Since all the data is stored and managed as files, it does not provide fine-grained access control on the contents of files, but only coarse-grained access governing who can access what files or directories. 
すべてのデータがファイルとして保存および管理されているため、ファイルの内容に対する詳細なアクセス制御を提供せず、誰がどのファイルやディレクトリにアクセスできるかを管理する粗いアクセス制御のみを提供します。
The query performance is poor because the formats are not optimized for fast access, and listing files is computationally expensive.
フォーマットが高速アクセスに最適化されていないため、クエリパフォーマンスは悪く、ファイルのリスト表示は計算コストが高くなります。
In short, organizations end up moving data into other systems to make use of the data, unless the applications can tolerate noise (i.e. machine learning). 
要するに、アプリケーションがノイズ（すなわち機械学習）を許容できない限り、組織はデータを利用するために他のシステムにデータを移動させることになります。 
Finally, quality is a challenge because it's hard to prevent data corruption and manage schema changes as more and more data gets ingested to the data lake. 
最後に、データレイクにますます多くのデータが取り込まれるにつれて、データの破損を防ぎ、スキーマの変更を管理するのが難しいため、品質が課題となります。 
Similarly, it is challenging to ensure atomic operations when writing a group of files, and no mechanism to roll back changes. 
同様に、一連のファイルを書き込む際にアトミック操作を保証するのが難しく、変更を元に戻すメカニズムがありません。 
As a result, many argue that most data lakes end up becoming data "swamps". 
その結果、多くの人がほとんどのデータレイクがデータ「沼」になってしまうと主張しています。 
Consequently, most organizations move subsets of this data into Data Warehouses, which do not have these three problems, but suffer from other problems. 
そのため、ほとんどの組織はこのデータのサブセットをData Warehouseに移動させますが、Data Warehouseはこれらの3つの問題を抱えていないものの、他の問題に悩まされています。

### What is a Data Warehouse? 
### Data Warehouseとは何ですか？
What is a Data Warehouse? 
Data Warehouseとは何ですか？ 
Data warehouses are proprietary systems that are built to store and manage only structured or semi-structured (primarily JSON format) data for SQL-based analytics and business intelligence. 
データウェアハウスは、SQLベースの分析およびビジネスインテリジェンスのために、構造化データまたは半構造化データ（主にJSON形式）のみを保存および管理するために構築された独自のシステムです。 
The most valuable business data is curated and uploaded to data warehouses, which are optimized for high performance, concurrency, and reliability but at a much higher cost, as any data processing will have to be at more expensive SQL rates rather than cheap data lake access rates. 
最も価値のあるビジネスデータはキュレーションされ、データウェアハウスにアップロードされます。データウェアハウスは高いパフォーマンス、同時実行性、信頼性のために最適化されていますが、データ処理は安価なデータレイクアクセス料金ではなく、より高価なSQL料金で行わなければなりません。 
Historically, data warehouses were capacity constrained and could not support simultaneous ETL and BI queries; much less real-time streaming. 
歴史的に、データウェアハウスは容量に制約があり、同時にETLおよびBIクエリをサポートできず、リアルタイムストリーミングはなおさら困難でした。 
Since data warehouses were primarily built for structured data, they do not support unstructured data such as images, sensor data, documents, videos, etc. 
データウェアハウスは主に構造化データのために構築されているため、画像、センサーデータ、文書、動画などの非構造化データをサポートしていません。 
They have limited support for machine learning and cannot directly support popular open source libraries and tools (TensorFlow, PyTorch, and other Python-based libraries) natively. 
機械学習に対するサポートは限られており、人気のあるオープンソースライブラリやツール（TensorFlow、PyTorch、その他のPythonベースのライブラリ）をネイティブに直接サポートすることはできません。 
As a result, most organizations end up keeping these data sets in a data lake, moving subsets into a data warehouse for fast concurrent BI and SQL use cases. 
その結果、ほとんどの組織はこれらのデータセットをデータレイクに保持し、サブセットをデータウェアハウスに移動させて迅速な同時BIおよびSQLユースケースに利用します。

### How is a Data Lakehouse different from a Data Warehouse? 
### Data LakehouseはData Warehouseとどのように異なりますか？
How is a Data Lakehouse different from a Data Warehouse 
Data LakehouseはData Warehouseとどのように異なりますか？
The lakehouse builds on top of existing data lakes, which often contain more than 90% of the data in the enterprise. 
レイクハウスは、既存のデータレイクの上に構築されており、これらのデータレイクにはしばしば企業内のデータの90％以上が含まれています。



. While most data warehouses support "external table" functionality to access that data, they have severe functionality limitations (e.g., only supporting read operations) and performance limitations when doing so. 
ほとんどのデータウェアハウスは、そのデータにアクセスするための「外部テーブル」機能をサポートしていますが、機能的な制限（例：読み取り操作のみをサポート）やパフォーマンスの制限があります。

Lakehouse instead adds traditional data warehousing capabilities to existing data lakes, including ACID transactions, fine-grained data security, low-cost updates and deletes, first-class SQL support, optimized performance for SQL queries, and BI style reporting. 
Lakehouseは、既存のデータレイクに従来のデータウェアハウス機能を追加し、ACIDトランザクション、細粒度のデータセキュリティ、低コストの更新と削除、ファーストクラスのSQLサポート、SQLクエリの最適化されたパフォーマンス、BIスタイルのレポーティングを含みます。

By building on top of a data lake, the Lakehouse stores and manages all existing data in a data lake, including all varieties of data, such as text, audio and video, in addition to structured data in tables. 
データレイクの上に構築することで、Lakehouseは、テーブル内の構造化データに加えて、テキスト、音声、ビデオなどのすべての種類のデータを含む、データレイク内のすべての既存データを保存および管理します。

Lakehouse also natively supports data science and machine learning use cases by providing direct access to data using open APIs and supporting various ML and Python/R libraries, such as PyTorch, Tensorflow or XGBoost, unlike data warehouses. 
Lakehouseは、オープンAPIを使用してデータへの直接アクセスを提供し、PyTorch、Tensorflow、XGBoostなどのさまざまなMLおよびPython/Rライブラリをサポートすることで、データウェアハウスとは異なり、データサイエンスや機械学習のユースケースをネイティブにサポートします。

Thus, Lakehouse provides a single system to manage all of an enterprise's data while supporting the range of analytics from BI and AI. 
したがって、Lakehouseは、BIおよびAIからの分析の範囲をサポートしながら、企業のすべてのデータを管理するための単一のシステムを提供します。

The lakehouse builds on top of existing data lakes, which often contain more than 90% of the data in the enterprise. 
Lakehouseは、既存のデータレイクの上に構築されており、これらはしばしば企業内のデータの90％以上を含んでいます。

While most data warehouses support "external table" functionality to access that data, they have severe functionality limitations (e.g., only supporting read operations) and performance limitations when doing so. 
ほとんどのデータウェアハウスは、そのデータにアクセスするための「外部テーブル」機能をサポートしていますが、機能的な制限（例：読み取り操作のみをサポート）やパフォーマンスの制限があります。

Lakehouse instead adds traditional data warehousing capabilities to existing data lakes, including 
Lakehouseは、既存のデータレイクに従来のデータウェアハウス機能を追加します。

A 5X LEADER
### Gartner: Databricks Cloud Database Leader
5倍のリーダー
### ガートナー：Databricks Cloud Databaseリーダー

On the other hand, data warehouses are proprietary data systems that are purpose-built for SQL-based analytics on structured data, and certain types of semi-structured data. 
一方、データウェアハウスは、構造化データおよび特定の種類の半構造化データに対するSQLベースの分析のために特別に構築された独自のデータシステムです。

Data warehouses have limited support for machine learning and cannot support running popular open source tools natively without first exporting the data (either through ODBC/JDBC or to a data lake). 
データウェアハウスは機械学習のサポートが限られており、データを最初にエクスポートしない限り（ODBC/JDBCを介してまたはデータレイクに）、人気のあるオープンソースツールをネイティブに実行することはできません。

Today, no data warehouse system has native support for all the existing audio, image, and video data that is already stored in data lakes. 
今日、どのデータウェアハウスシステムも、すでにデータレイクに保存されているすべてのオーディオ、画像、ビデオデータをネイティブにサポートしていません。

### How is the Data Lakehouse different from a Data Lake?
### データレイクハウスはデータレイクとどのように異なるのか？

The most common complaint about data lakes is that they can become data swamps. 
データレイクに関する最も一般的な不満は、データスワンプ（データの沼）になり得ることです。

Anybody can dump any data into a data lake; there is no structure or governance to the data in the lake. 
誰でもデータレイクに任意のデータを投入できますが、湖のデータには構造やガバナンスがありません。

Performance is poor, as data is not organized with performance in mind, resulting in limited analytics on data lakes. 
パフォーマンスは悪く、データがパフォーマンスを考慮して整理されていないため、データレイクでの分析が制限されます。

As a result, most organizations use data lakes as a landing zone for most of their data due to the underlying low-cost object storage data lakes use and then move the data to different downstream systems such as data warehouses to extract value. 
その結果、ほとんどの組織は、データレイクが使用する低コストのオブジェクトストレージに基づいて、ほとんどのデータのランディングゾーンとしてデータレイクを使用し、その後、データをデータウェアハウスなどの異なる下流システムに移動して価値を抽出します。

Lakehouse tackles the fundamental issues that make data swamps out of data lakes. 
Lakehouseは、データレイクをデータスワンプにする根本的な問題に取り組みます。

It adds ACID transactions to ensure consistency as multiple parties concurrently read or write data. 
複数の当事者が同時にデータを読み書きする際の一貫性を確保するために、ACIDトランザクションを追加します。

It supports DW schema architectures like star/snowflake-schemas and provides robust governance and auditing mechanisms directly on the data lake. 
スター/スノーフレークスキーマのようなDWスキーマアーキテクチャをサポートし、データレイク上で直接堅牢なガバナンスと監査メカニズムを提供します。

It also leverages various performance optimization techniques, such as caching, multi-dimensional clustering, and data skipping, using file statistics and data compaction to right-size the files enabling fast analytics. 
キャッシング、マルチディメンションクラスタリング、データスキッピングなどのさまざまなパフォーマンス最適化技術を活用し、ファイル統計とデータ圧縮を使用してファイルのサイズを適切に調整し、高速な分析を可能にします。

And it adds fine-grained security and auditing capabilities for data governance. 
さらに、データガバナンスのための細粒度のセキュリティと監査機能を追加します。

By adding data management and performance optimizations to the open data lake, lakehouse can natively support BI and ML applications. 
オープンデータレイクにデータ管理とパフォーマンス最適化を追加することで、LakehouseはBIおよびMLアプリケーションをネイティブにサポートできます。

### How easy is it for data analysts to use a Data Lakehouse?
### データアナリストがデータレイクハウスを使用するのはどれくらい簡単か？

Data lakehouse systems implement the same SQL interface as traditional data warehouses, so analysts can connect to them in existing BI and SQL tools without changing their workflows. 
データレイクハウスシステムは、従来のデータウェアハウスと同じSQLインターフェースを実装しているため、アナリストはワークフローを変更することなく、既存のBIおよびSQLツールで接続できます。

For example, leading BI products such as Tableau, PowerBI, Qlik, and Looker can all connect to data lakehouse systems, data engineering tools like Fivetran and dbt can run against them, and analysts can export data into desktop tools such as Microsoft Excel. 
たとえば、Tableau、PowerBI、Qlik、Lookerなどの主要なBI製品はすべてデータレイクハウスシステムに接続でき、Fivetranやdbtなどのデータエンジニアリングツールはそれに対して実行でき、アナリストはデータをMicrosoft Excelなどのデスクトップツールにエクスポートできます。

Lakehouse's support for ANSI SQL, fine-grained access control, and ACID transactions enables administrators to manage them the same way as data warehouse systems but cover all the data in their organization in one system. 
LakehouseのANSI SQL、細粒度のアクセス制御、ACIDトランザクションのサポートにより、管理者はデータウェアハウスシステムと同じ方法で管理でき、組織内のすべてのデータを1つのシステムでカバーできます。

One important advantage of Lakehouse systems in simplicity is that they manage all the data in the organization, so data analysts can be granted access to work with raw and historical data as it arrives instead of only the subset of data loaded into a data warehouse system. 
Lakehouseシステムのシンプルさにおける重要な利点の1つは、組織内のすべてのデータを管理するため、データアナリストはデータウェアハウスシステムにロードされたデータのサブセットだけでなく、到着する生データや履歴データを扱うためのアクセス権を付与されることです。

An analyst can therefore easily ask questions that span multiple historical datasets or establish a new pipeline for working with a new dataset without blocking on a database administrator or data engineer to load the appropriate data. 
したがって、アナリストは複数の履歴データセットにまたがる質問を簡単に行ったり、新しいデータセットで作業するための新しいパイプラインを確立したりできます。

Built-in support for AI also makes it easy for analysts to run AI models built by a machine learning team on any data. 
AIの組み込みサポートにより、アナリストは機械学習チームが構築したAIモデルを任意のデータで簡単に実行できます。

### How do Data Lakehouse systems compare in performance and cost to data warehouses?
### データレイクハウスシステムは、パフォーマンスとコストの面でデータウェアハウスとどのように比較されるか？

Data Lakehouse systems are built around separate, elastically scaling compute and storage to minimize their cost of operation and maximize performance. 
データレイクハウスシステムは、運用コストを最小限に抑え、パフォーマンスを最大化するために、分離された弾力的にスケーリングするコンピュートとストレージを中心に構築されています。

Recent systems provide comparable or even better performance per dollar to traditional data warehouses for SQL workloads, using the same optimization techniques inside their engines (e.g., query compilation and storage layout optimizations). 
最近のシステムは、SQLワークロードに対して従来のデータウェアハウスと同等かそれ以上のパフォーマンスを提供し、エンジン内で同じ最適化技術（例：クエリコンパイルやストレージレイアウトの最適化）を使用しています。

In addition, Lakehouse systems often take advantage of cloud provider cost-saving features such as spot instance pricing (which requires the system to tolerate losing worker nodes mid-query) and reduced prices for infrequently accessed storage, which traditional data warehouse engines have usually not been designed to support. 
さらに、Lakehouseシステムは、クラウドプロバイダーのコスト削減機能（スポットインスタンスの価格設定など）を活用することが多く、これはシステムがクエリの途中でワーカーノードを失うことを許容する必要があります。また、従来のデータウェアハウスエンジンは通常サポートするように設計されていない、アクセス頻度の低いストレージの価格が削減されます。

### What data governance functionality do Data Lakehouse systems support?
### データレイクハウスシステムはどのようなデータガバナンス機能をサポートしているか？

By adding a management interface on top of data lake storage, Lakehouse systems provide a uniform way to manage access control, data quality, and compliance across all of an organization's data using standard interfaces similar to those in data warehouses. 
データレイクストレージの上に管理インターフェースを追加することで、Lakehouseシステムは、データウェアハウスの標準インターフェースに類似した標準インターフェースを使用して、組織内のすべてのデータに対するアクセス制御、データ品質、およびコンプライアンスを管理するための一貫した方法を提供します。

Modern Lakehouse systems support fine-grained (row, column, and view level) access control via SQL, query auditing, attribute-based access control, data versioning, and data quality constraints and monitoring. 
現代のLakehouseシステムは、SQLを介した細粒度（行、列、ビューレベル）のアクセス制御、クエリ監査、属性ベースのアクセス制御、データバージョン管理、データ品質制約および監視をサポートします。

These features are generally provided using standard interfaces familiar to database administrators (for example, SQL GRANT commands) to allow existing personnel to manage all the data in an organization in a uniform way. 
これらの機能は、データベース管理者に馴染みのある標準インターフェース（たとえば、SQL GRANTコマンド）を使用して提供され、既存のスタッフが組織内のすべてのデータを一貫した方法で管理できるようにします。



. Centralizing all the data in a Lakehouse system with a single management interface also reduces the administrative burden and potential for error that comes with managing multiple separate systems.
Lakehouseシステムにおいて、すべてのデータを単一の管理インターフェースで集中管理することは、複数の別々のシステムを管理する際に伴う管理負担やエラーの可能性を減少させます。

By adding a management interface on top of data lake storage, Lakehouse systems provide a uniform way to manage access control, data quality, and compliance across all of an organization's data using standard interfaces similar to those in data warehouses.
データレイクストレージの上に管理インターフェースを追加することで、Lakehouseシステムは、データウェアハウスに似た標準インターフェースを使用して、組織のすべてのデータに対するアクセス制御、データ品質、およびコンプライアンスを管理するための一貫した方法を提供します。

Modern Lakehouse systems support fine-grained (row, column, and view level) access control via SQL, query auditing, attribute-based access control, data versioning, and data quality constraints and monitoring.
現代のLakehouseシステムは、SQLを介した細粒度（行、列、ビューレベル）のアクセス制御、クエリ監査、属性ベースのアクセス制御、データバージョニング、およびデータ品質制約と監視をサポートしています。

These features are generally provided using standard interfaces familiar to database administrators (for example, SQL GRANT commands) to allow existing personnel to manage all the data in an organization in a uniform way.
これらの機能は、一般的にデータベース管理者に馴染みのある標準インターフェース（例えば、SQL GRANTコマンド）を使用して提供され、既存の人員が組織内のすべてのデータを一貫した方法で管理できるようにします。

Centralizing all the data in a Lakehouse system with a single management interface also reduces the administrative burden and potential for error that comes with managing multiple separate systems.
Lakehouseシステムにおいて、すべてのデータを単一の管理インターフェースで集中管理することは、複数の別々のシステムを管理する際に伴う管理負担やエラーの可能性を減少させます。

### Does the Data Lakehouse have to be centralized or can it be decentralized into a Data Mesh?
### データレイクハウスは集中化する必要があるのか、それともデータメッシュに分散化できるのか？

Does the Data Lakehouse have to be centralized or can it be decentralized into a Data Mesh?
データレイクハウスは集中化する必要があるのか、それともデータメッシュに分散化できるのか？

No, organizations do not need to centralize all their data in one Lakehouse.
いいえ、組織はすべてのデータを1つのLakehouseに集中化する必要はありません。

Many organizations using the Lakehouse architecture take a decentralized approach to store and process data but take a centralized approach to security, governance, and discovery.
Lakehouseアーキテクチャを使用している多くの組織は、データを保存および処理するために分散型アプローチを採用していますが、セキュリティ、ガバナンス、および発見に関しては集中型アプローチを取ります。

Depending on organizational structure and business needs, we see a few common approaches:
組織の構造やビジネスニーズに応じて、いくつかの一般的なアプローチが見られます：

- Each business unit builds its own Lakehouse to capture its business' complete view – from product development to customer acquisition to customer service.
- 各ビジネスユニットは、自社のビジネスの完全なビューを捉えるために独自のLakehouseを構築します - 製品開発から顧客獲得、顧客サービスまで。

- Each functional area, such as product manufacturing, supply chain, sales, and marketing, could build its own Lakehouse to optimize operations within its business area.
- 製品製造、サプライチェーン、販売、マーケティングなどの各機能領域は、自分のビジネスエリア内での運用を最適化するために独自のLakehouseを構築することができます。

- Some organizations also spin up a new Lakehouse to tackle new cross-functional strategic initiatives such as customer 360 or unexpected crises like the COVID pandemic to drive fast, decisive action.
- 一部の組織は、顧客360のような新しいクロスファンクショナルな戦略的イニシアチブや、COVIDパンデミックのような予期しない危機に対処するために、新しいLakehouseを立ち上げて迅速かつ決定的な行動を促進します。

Each business unit builds its own Lakehouse to capture its business' complete view – from product development to customer acquisition to customer service.
各ビジネスユニットは、自社のビジネスの完全なビューを捉えるために独自のLakehouseを構築します - 製品開発から顧客獲得、顧客サービスまで。

Each functional area, such as product manufacturing, supply chain, sales, and marketing, could build its own Lakehouse to optimize operations within its business area.
製品製造、サプライチェーン、販売、マーケティングなどの各機能領域は、自分のビジネスエリア内での運用を最適化するために独自のLakehouseを構築することができます。

Some organizations also spin up a new Lakehouse to tackle new cross-functional strategic initiatives such as customer 360 or unexpected crises like the COVID pandemic to drive fast, decisive action.
一部の組織は、顧客360のような新しいクロスファンクショナルな戦略的イニシアチブや、COVIDパンデミックのような予期しない危機に対処するために、新しいLakehouseを立ち上げて迅速かつ決定的な行動を促進します。

The unified nature of the Lakehouse architecture enables data architects to build simpler data architectures that align with the business needs without complex orchestration of data movement across siloed data stacks for BI and ML.
Lakehouseアーキテクチャの統一された性質は、データアーキテクトがビジネスニーズに合ったシンプルなデータアーキテクチャを構築できるようにし、BIやMLのためにサイロ化されたデータスタック間でのデータ移動の複雑なオーケストレーションを必要としません。

Furthermore, the openness of the Lakehouse architecture enables organizations to leverage the growing ecosystem of open technologies without fear of lock-in to addressing the unique needs of the different business units or functional areas.
さらに、Lakehouseアーキテクチャのオープン性は、組織が異なるビジネスユニットや機能領域のユニークなニーズに対応するためのロックインを恐れずに、成長するオープンテクノロジーのエコシステムを活用できるようにします。

Because Lakehouse systems are usually built on separated, scalable cloud storage, it is also simple and efficient to let multiple teams access each lakehouse.
Lakehouseシステムは通常、分離されたスケーラブルなクラウドストレージ上に構築されているため、複数のチームが各Lakehouseにアクセスすることも簡単で効率的です。

Recently, Delta Sharing proposed an open and standard mechanism for data sharing across Lakehouses with support from many different vendors.
最近、Delta Sharingは、多くの異なるベンダーのサポートを受けて、Lakehouses間でのデータ共有のためのオープンで標準的なメカニズムを提案しました。

The unified nature of the Lakehouse architecture enables data architects to build simpler data architectures that align with the business needs without complex orchestration of data movement across siloed data stacks for BI and ML.
Lakehouseアーキテクチャの統一された性質は、データアーキテクトがビジネスニーズに合ったシンプルなデータアーキテクチャを構築できるようにし、BIやMLのためにサイロ化されたデータスタック間でのデータ移動の複雑なオーケストレーションを必要としません。

### How does the Data Mesh relate to the Data Lakehouse?
### データメッシュはデータレイクハウスとどのように関連していますか？

How does the Data Mesh relate to the Data Lakehouse?
データメッシュはデータレイクハウスとどのように関連していますか？

Zhamak Dehghani has outlined four fundamental organizational principles that embody any data mesh implementation.
Zhamak Dehghaniは、データメッシュの実装を具現化する4つの基本的な組織原則を概説しています。

The Data Lakehouse architecture can be used in implementing these organizational principles:
データレイクハウスアーキテクチャは、これらの組織原則を実装するために使用できます：

- Domain-oriented decentralized data ownership and architecture: As discussed in the previous section, the lakehouse architecture takes a decentralized approach to data ownership.
- ドメイン指向の分散型データ所有権とアーキテクチャ：前のセクションで述べたように、Lakehouseアーキテクチャはデータ所有権に対して分散型アプローチを取ります。

Organizations can create many different lakehouses to serve the individual needs of the business groups.
組織は、ビジネスグループの個々のニーズに応えるために、多くの異なるLakehouseを作成できます。

Based on their needs, they can store and manage various data – images, video, text, structured tabular data, and related data assets such as machine learning models and associated code to reproduce transformations and insights.
ニーズに応じて、画像、動画、テキスト、構造化された表形式データ、機械学習モデルや関連するコードなどのデータ資産を保存および管理できます。

- Data as a product: The lakehouse architecture helps organizations manage data as a product by providing different data team members in domain-specific teams complete control over the data lifecycle.
- データを製品として：Lakehouseアーキテクチャは、ドメイン特化型チームの異なるデータチームメンバーにデータライフサイクルに対する完全な制御を提供することで、組織がデータを製品として管理するのを助けます。

Data team comprising of a data owner, data engineers, analysts, and data scientists can manage data (structured, semi-structured, and unstructured with proper lineage and security controls), code (ETL, data science notebooks, ML training, and deployment), and supporting infrastructure (storage, compute, cluster policies, and various analytics and ML engines).
データオーナー、データエンジニア、アナリスト、データサイエンティストで構成されるデータチームは、データ（構造化、半構造化、非構造化で適切な系譜とセキュリティ制御を持つ）、コード（ETL、データサイエンスノートブック、MLトレーニング、デプロイメント）、およびサポートインフラストラクチャ（ストレージ、コンピュート、クラスター方針、さまざまな分析およびMLエンジン）を管理できます。

Lakehouse platform features such as ACID transactions, data versioning, and zero-copy cloning make it easy for these teams to publish and maintain their data as a product.
ACIDトランザクション、データバージョニング、ゼロコピークローンなどのLakehouseプラットフォーム機能により、これらのチームはデータを製品として公開および維持することが容易になります。

- Self-serve data infrastructure as a platform: The lakehouse architecture provides an end-to-end data platform for data management, data engineering, analytics, data science, and machine learning with integrations to a broad ecosystem of tools.
- 自己サービスデータインフラストラクチャをプラットフォームとして：Lakehouseアーキテクチャは、データ管理、データエンジニアリング、分析、データサイエンス、機械学習のためのエンドツーエンドのデータプラットフォームを提供し、広範なツールのエコシステムとの統合を行います。

Adding data management on top of existing data lakes simplifies data access and sharing – anyone can request access, the requester pays for cheap blob storage and gets immediate secure access.
既存のデータレイクの上にデータ管理を追加することで、データアクセスと共有が簡素化されます - 誰でもアクセスをリクエストでき、リクエスターは安価なBlobストレージの料金を支払い、即座に安全なアクセスを得ることができます。

In addition, using open data formats and enabling direct file access, data teams can use best-of-breed analytics and ML frameworks on the data.
さらに、オープンデータフォーマットを使用し、直接ファイルアクセスを可能にすることで、データチームはデータに対して最高の分析およびMLフレームワークを使用できます。

- Federated computational governance: The governance in the lakehouse architecture is implemented by a centralized catalog with fine-grained access controls (row/column level), enabling easy discovery of data and other artifacts like code and ML models.
- フェデレーテッド計算ガバナンス：Lakehouseアーキテクチャにおけるガバナンスは、細粒度のアクセス制御（行/列レベル）を持つ集中型カタログによって実装されており、データやコード、MLモデルなどの他のアーティファクトの容易な発見を可能にします。

Organizations can assign different administrators to different parts of the catalog to decentralize control and management of data assets.
組織は、データ資産の制御と管理を分散化するために、カタログの異なる部分に異なる管理者を割り当てることができます。

This hybrid approach of a centralized catalog with federated control preserves the independence and agility of the local domain-specific teams while ensuring data asset reuse across these teams and enforcing a common security and governance model globally.
集中型カタログとフェデレーテッドコントロールのこのハイブリッドアプローチは、ローカルのドメイン特化型チームの独立性と機動性を保持しつつ、これらのチーム間でのデータ資産の再利用を確保し、グローバルに共通のセキュリティおよびガバナンスモデルを強制します。

Keep up with us
私たちについていってください

Recommended for you
あなたにおすすめ

Product
製品

August 30, 2021/12 min read
2021年8月30日/12分の読書

#### Frequently Asked Questions About the Data Lakehouse
#### データレイクハウスに関するよくある質問
Share this post
この投稿を共有する



## Never miss a Databricks post Databricksの投稿を見逃さない




## Sign up サインアップ

By clicking “Subscribe” I understand that I will receive Databricks communications, and I agree to Databricks processing my personal data in accordance with its Privacy Policy.
「購読」をクリックすることで、私はDatabricksからの通信を受け取ることを理解し、Databricksがそのプライバシーポリシーに従って私の個人データを処理することに同意します。
Subscribe
購読



## What's next? 次は何ですか？
### More from the Authors 著者からのさらなる情報
- Databricks Named a Leader in 2021 Gartner Magic Quadrant for Data Science and Machine Learning Platforms
- Bringing Lakehouse to the Citizen Data Scientist: Announcing the Acquisition of 8080 Labs
- 2025 DLT Update: Intelligent, fully governed data pipelines
- Databricksは2021年のGartner Magic Quadrant for Data Science and Machine Learning Platformsでリーダーに選ばれました。
- Lakehouseを市民データサイエンティストに提供する：8080 Labsの買収を発表
- 2025 DLTアップデート：インテリジェントで完全に管理されたデータパイプライン

Data Warehousing
データウェアハウジング
July 24, 2024/7 min read
/
2024年7月24日/7分で読める
#### Primary Key and Foreign Key constraints are GA and now enable faster queries
#### プライマリキーと外部キー制約がGAとなり、より高速なクエリを可能にしました。

Product
製品
September 12, 2024/7 min read
/
2024年9月12日/7分で読める
#### Five Simple Steps for Implementing a Star Schema in Databricks With Delta Lake
#### Delta Lakeを使用してDatabricksにスター・スキーマを実装するための5つの簡単なステップ

Why Databricks
なぜDatabricksなのか
Discover
発見
- For Executives
- For Startups
- Lakehouse Architecture
- Mosaic Research
- 経営者向け
- スタートアップ向け
- レイクハウスアーキテクチャ
- モザイクリサーチ

Customers
顧客
- Customer Stories
- 顧客のストーリー

Partners
パートナー
- Cloud Providers
- Technology Partners
- Data Partners
- Built on Databricks
- Consulting & System Integrators
- C&SI Partner Program
- Partner Solutions
- クラウドプロバイダー
- テクノロジーパートナー
- データパートナー
- Databricks上に構築
- コンサルティングおよびシステムインテグレーター
- C&SIパートナープログラム
- パートナーソリューション

Discover
発見
- For Executives
- For Startups
- Lakehouse Architecture
- Mosaic Research
- 経営者向け
- スタートアップ向け
- レイクハウスアーキテクチャ
- モザイクリサーチ

Customers
顧客
- Customer Stories
- 顧客のストーリー

Partners
パートナー
- Cloud Providers
- Technology Partners
- Data Partners
- Built on Databricks
- Consulting & System Integrators
- C&SI Partner Program
- Partner Solutions
- クラウドプロバイダー
- テクノロジーパートナー
- データパートナー
- Databricks上に構築
- コンサルティングおよびシステムインテグレーター
- C&SIパートナープログラム
- パートナーソリューション

Product
製品
Databricks Platform
Databricksプラットフォーム
- Platform Overview
- Sharing
- Governance
- Artificial Intelligence
- Business Intelligence
- Database
- Data Management
- Data Warehousing
- Data Engineering
- Data Science
- Application Development
- プラットフォーム概要
- 共有
- ガバナンス
- 人工知能
- ビジネスインテリジェンス
- データベース
- データ管理
- データウェアハウジング
- データエンジニアリング
- データサイエンス
- アプリケーション開発

Pricing
価格設定
- Pricing Overview
- Pricing Calculator
- 価格設定概要
- 価格計算機

Integrations and Data
統合とデータ
- Marketplace
- IDE Integrations
- Partner Connect
- マーケットプレイス
- IDE統合
- パートナー接続

Databricks Platform
Databricksプラットフォーム
- Platform Overview
- Sharing
- Governance
- Artificial Intelligence
- Business Intelligence
- Database
- Data Management
- Data Warehousing
- Data Engineering
- Data Science
- Application Development
- プラットフォーム概要
- 共有
- ガバナンス
- 人工知能
- ビジネスインテリジェンス
- データベース
- データ管理
- データウェアハウジング
- データエンジニアリング
- データサイエンス
- アプリケーション開発

Pricing
価格設定
- Pricing Overview
- Pricing Calculator
- 価格設定概要
- 価格計算機

Integrations and Data
統合とデータ
- Marketplace
- IDE Integrations
- Partner Connect
- マーケットプレイス
- IDE統合
- パートナー接続

Solutions
ソリューション
Databricks For Industries
Databricksの業界向け
- Communications
- Financial Services
- Healthcare and Life Sciences
- Manufacturing
- Media and Entertainment
- Public Sector
- Retail
- View All
- 通信
- 金融サービス
- ヘルスケアおよびライフサイエンス
- 製造
- メディアおよびエンターテインメント
- 公共部門
- 小売
- すべて表示

Cross Industry Solutions
業界横断的ソリューション
- Cybersecurity
- Marketing
- サイバーセキュリティ
- マーケティング

Databricks For Industries
Databricksの業界向け
- Communications
- Financial Services
- Healthcare and Life Sciences
- Manufacturing
- Media and Entertainment
- Public Sector
- Retail
- View All
- 通信
- 金融サービス
- ヘルスケアおよびライフサイエンス
- 製造
- メディアおよびエンターテインメント
- 公共部門
- 小売
- すべて表示

Cross Industry Solutions
業界横断的ソリューション
- Cybersecurity
- Marketing
- サイバーセキュリティ
- マーケティング

Resources
リソース
Learning
学習
- Training
- Certification
- Free Edition
- University Alliance
- Databricks Academy Login
- トレーニング
- 認定
- 無料版
- 大学提携
- Databricksアカデミーログイン

Events
イベント
- Data + AI Summit
- Data + AI World Tour
- Data Intelligence Days
- Event Calendar
- データ + AIサミット
- データ + AIワールドツアー
- データインテリジェンスデイズ
- イベントカレンダー

Blog and Podcasts
ブログとポッドキャスト
- Databricks Blog
- Databricks Mosaic Research Blog
- Data Brew Podcast
- Champions of Data & AI Podcast
- Databricksブログ
- Databricksモザイクリサーチブログ
- Data Brewポッドキャスト
- データとAIのチャンピオンポッドキャスト

Learning
学習
- Training
- Certification
- Free Edition
- University Alliance
- Databricks Academy Login
- トレーニング
- 認定
- 無料版
- 大学提携
- Databricksアカデミーログイン

Events
イベント
- Data + AI Summit
- Data + AI World Tour
- Data Intelligence Days
- Event Calendar
- データ + AIサミット
- データ + AIワールドツアー
- データインテリジェンスデイズ
- イベントカレンダー

Blog and Podcasts
ブログとポッドキャスト
- Databricks Blog
- Databricks Mosaic Research Blog
- Data Brew Podcast
- Champions of Data & AI Podcast
- Databricksブログ
- Databricksモザイクリサーチブログ
- Data Brewポッドキャスト
- データとAIのチャンピオンポッドキャスト

About
会社について
Company
会社
- Who We Are
- Our Team
- Databricks Ventures
- Contact Us
- 私たちについて
- 私たちのチーム
- Databricksベンチャーズ
- お問い合わせ

Careers
キャリア
- Open Jobs
- Working at Databricks
- オープンジョブ
- Databricksでの働き方

Press
プレス
- Awards and Recognition
- Newsroom
- 受賞歴と認識
- ニュースルーム

Company
会社
- Who We Are
- Our Team
- Databricks Ventures
- Contact Us
- 私たちについて
- 私たちのチーム
- Databricksベンチャーズ
- お問い合わせ

Careers
キャリア
- Open Jobs
- Working at Databricks
- オープンジョブ
- Databricksでの働き方

Press
プレス
- Awards and Recognition
- Newsroom
- 受賞歴と認識
- ニュースルーム

Databricks Inc.160 Spear Street, 15th FloorSan Francisco, CA 941051-866-330-0121
Databricks Inc. 160 Spear Street, 15階 サンフランシスコ, CA 94105 1-866-330-0121

See Careers at Databricks
Databricksでのキャリアを見る

© Databricks2026. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the Apache Software Foundation.
© Databricks 2026. 全著作権所有。Apache、Apache Spark、Spark、Sparkロゴ、Apache Iceberg、Iceberg、およびApache IcebergロゴはApache Software Foundationの商標です。

2026
- Privacy Notice
- |Terms of Use
- |Modern Slavery Statement
- |California Privacy
- |Your Privacy Choices
- プライバシー通知
- |利用規約
- |現代の奴隷制に関する声明
- |カリフォルニアプライバシー
- |あなたのプライバシーの選択



## We Care About Your Privacy 私たちはあなたのプライバシーを大切にします



## Privacy Preference Center プライバシー設定センター

- Your Privacy あなたのプライバシー
- Strictly Necessary Cookies 厳密に必要なクッキー
- Performance Cookies パフォーマンスクッキー
- Functional Cookies 機能的クッキー
- Targeting Cookies ターゲティングクッキー
- TOTHR

### Your Privacy あなたのプライバシー

When you visit any website, it may store or retrieve information on your browser, mostly in the form of cookies. 
ウェブサイトを訪れると、ブラウザに情報を保存または取得することがあります。これは主にクッキーの形で行われます。 
This information might be about you, your preferences or your device and is mostly used to make the site work as you expect it to. 
この情報はあなたやあなたの好み、デバイスに関するものであり、主にサイトがあなたの期待通りに機能するために使用されます。 
The information does not usually directly identify you, but it can give you a more personalized web experience. 
この情報は通常、あなたを直接特定するものではありませんが、よりパーソナライズされたウェブ体験を提供することができます。 
Because we respect your right to privacy, you can choose not to allow some types of cookies. 
私たちはあなたのプライバシーの権利を尊重するため、いくつかの種類のクッキーを許可しないことを選択できます。 
Click on the different category headings to find out more and change our default settings. 
異なるカテゴリの見出しをクリックして、詳細を確認し、デフォルト設定を変更してください。 
However, blocking some types of cookies may impact your experience of the site and the services we are able to offer. 
ただし、いくつかの種類のクッキーをブロックすると、サイトの体験や提供できるサービスに影響を与える可能性があります。

Opting out of sales, sharing, and targeted advertising
販売、共有、ターゲット広告からのオプトアウト

Depending on your location, you may have the right to opt out of the “sale” or “sharing” of your personal information or the processing of your personal information for purposes of online “targeted advertising.” 
あなたの所在地に応じて、個人情報の「販売」または「共有」からオプトアウトする権利や、オンラインの「ターゲット広告」の目的で個人情報を処理することからオプトアウトする権利がある場合があります。 
You can opt out based on cookies and similar identifiers by disabling optional cookies here. 
ここでオプションのクッキーを無効にすることで、クッキーや類似の識別子に基づいてオプトアウトできます。 
To opt out based on other identifiers (such as your email address), submit a request in our Privacy Request Center. 
他の識別子（メールアドレスなど）に基づいてオプトアウトするには、プライバシーリクエストセンターにリクエストを送信してください。 
More information
詳細情報

#### Opting out of sales, sharing, and targeted advertising
#### 販売、共有、ターゲット広告からのオプトアウト

#### Strictly Necessary Cookies 厳密に必要なクッキー

These cookies are necessary for the website to function and cannot be switched off in our systems. 
これらのクッキーは、ウェブサイトが機能するために必要であり、私たちのシステムでオフにすることはできません。 
They assist with essential site functionality such as setting your privacy preferences, logging in or filling in forms. 
これらは、プライバシー設定の設定、ログイン、フォームの記入など、基本的なサイト機能を支援します。 
You can set your browser to block or alert you about these cookies, but some parts of the site will no longer work. 
ブラウザを設定してこれらのクッキーをブロックまたは警告することができますが、サイトの一部は機能しなくなります。

#### Performance Cookies パフォーマンスクッキー

These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. 
これらのクッキーは、訪問数やトラフィックソースをカウントすることを可能にし、サイトのパフォーマンスを測定および改善することができます。 
They help us to know which pages are the most and least popular and see how visitors move around the site. 
これにより、どのページが最も人気があり、どのページが最も人気がないかを知り、訪問者がサイト内をどのように移動するかを確認できます。

#### Functional Cookies 機能的クッキー

These cookies enable the website to provide enhanced functionality and personalization. 
これらのクッキーは、ウェブサイトが強化された機能性とパーソナライズを提供することを可能にします。 
They may be set by us or by third party providers whose services we have added to our pages. 
これらは、私たちがページに追加したサービスを提供する第三者によって設定される場合があります。 
If you do not allow these cookies then some or all of these services may not function properly. 
これらのクッキーを許可しない場合、これらのサービスの一部またはすべてが正しく機能しない可能性があります。

#### Targeting Cookies ターゲティングクッキー

These cookies may be set through our site by our advertising partners. 
これらのクッキーは、私たちのサイトを通じて広告パートナーによって設定される場合があります。 
They may be used by those companies to build a profile of your interests and show you relevant advertisements on other sites. 
これらの企業は、あなたの興味のプロファイルを構築し、他のサイトで関連する広告を表示するために使用する場合があります。 
If you do not allow these cookies, you will experience less targeted advertising. 
これらのクッキーを許可しない場合、ターゲット広告が少なくなります。

#### TOTHR

TOTHR

### Cookie List クッキーリスト

Consent 同意
Leg.Interest 法的利益
checkbox label チェックボックスラベル
label ラベル
checkbox label チェックボックスラベル
label ラベル
checkbox label チェックボックスラベル
label ラベル
- checkbox labellabel チェックボックスラベル
checkbox label チェックボックスラベル
label ラベル
