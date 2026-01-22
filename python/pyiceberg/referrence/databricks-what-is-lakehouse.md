refs: https://www.databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html


# What Is a Lakehouse? 

Published:January 30, 2020
2020年1月30日
Platform
6 min read
byBen Lorica,Michael Armbrust,Reynold Xin,Matei ZahariaandAli Ghodsi

---

Over the past few years at Databricks, we've seen a new data management architecture that emerged independently across many customers and use cases: the lakehouse. 
ここ数年、Databricksでは、**多くの顧客やユースケースで独立して現れた新しいデータ管理アーキテクチャである「[レイクハウス](https://www.databricks.com/blog/2021/08/30/frequently-asked-questions-about-the-data-lakehouse.html)」**を目の当たりにしてきました。
In this post we describe this new architecture and its advantages over previous approaches.
この記事では、この新しいアーキテクチャと従来のアプローチに対する利点について説明します。

Data warehouses have a long history in decision support and business intelligence applications. 
データウェアハウスは、意思決定支援およびビジネスインテリジェンスアプリケーションにおいて長い歴史を持っています。
Since its inception in the late 1980s, data warehouse technology continued to evolve and MPP architectures led to systems that were able to handle larger data sizes. 
1980年代後半に始まって以来、データウェアハウス技術は進化を続け、MPPアーキテクチャはより大きなデータサイズを処理できるシステムを生み出しました。
But while warehouses were great for structured data, a lot of modern enterprises have to deal with unstructured data, semi-structured data, and data with high variety, velocity, and volume. 
しかし、ウェアハウスは構造化データには優れていましたが、多くの現代企業は非構造化データ、半構造化データ、そして多様性、速度、ボリュームが高いデータに対処しなければなりません。
Data warehouses are not suited for many of these use cases, and they are certainly not the most cost efficient.
データウェアハウスはこれらの多くのユースケースには適しておらず、確かに最もコスト効率が良いわけではありません。

<!-- ここまで読んだ! -->

As companies began to collect large amounts of data from many different sources, architects began envisioning a single system to house data for many different analytic products and workloads. 
企業がさまざまなソースから大量のデータを収集し始めると、アーキテクトはさまざまな分析製品やワークロードのためにデータを格納する単一のシステムを構想し始めました。
About a decade ago companies began building data lakes - repositories for raw data in a variety of formats. 
約10年前、企業はさまざまな形式の生データを格納するリポジトリであるデータレイクの構築を始めました。
While suitable for storing data, data lakes lack some critical features: they do not support transactions, they do not enforce data quality, and their lack of consistency / isolation makes it almost impossible to mix appends and reads, and batch and streaming jobs. 
**データを保存するには適していますが、データレイクは重要な機能がいくつか欠けています：トランザクションをサポートせず、データ品質を強制せず、一貫性/隔離が欠如しているため、追加と読み取り、バッチとストリーミングジョブを混在させることがほぼ不可能**です。
For these reasons, many of the promises of the data lakes have not materialized, and in many cases leading to a loss of many of the benefits of data warehouses.
これらの理由から、データレイクの多くの約束は実現せず、多くの場合、データウェアハウスの多くの利点を失う結果となっています。

<!-- ここまで読んだ! -->

The need for a flexible, high-performance system hasn't abated. 
柔軟で高性能なシステムの必要性は衰えていません。
Companies require systems for diverse data applications including SQL analytics, real-time monitoring, data science, and machine learning. 
企業は、**SQL分析、リアルタイムモニタリング、データサイエンス、機械学習などの多様なデータアプリケーションのためのシステム**を必要としています。
Most of the recent advances in AI have been in better models to process unstructured data (text, images, video, audio), but these are precisely the types of data that a data warehouse is not optimized for. 
最近のAIの進展のほとんどは、非構造化データ（テキスト、画像、ビデオ、音声）を処理するためのより良いモデルに関するものであり、これらはまさにデータウェアハウスが最適化されていないデータの種類です。
A common approach is to use multiple systems - a data lake, several data warehouses, and other specialized systems such as streaming, time-series, graph, and image databases. 
一般的なアプローチは、データレイク、いくつかのデータウェアハウス、ストリーミング、時系列、グラフ、画像データベースなどの他の専門システムを使用することです。
Having a multitude of systems introduces complexity and more importantly, introduces delay as data professionals invariably need to move or copy data between different systems.
**多くのシステムを持つことは複雑さをもたらし、さらに重要なことに、データ専門家は異なるシステム間でデータを移動またはコピーする必要があるため、遅延を引き起こします。**

<!-- ここまで読んだ! -->

## What is a lakehouse? レイクハウスとは？

New systems are beginning to emerge that address the limitations of data lakes. 
新しいシステムがデータレイクの限界に対処するために登場し始めています。
A lakehouse is a new, open architecture that combines the best elements of data lakes and data warehouses. 
レイクハウスは、データレイクとデータウェアハウスの最良の要素を組み合わせた新しいオープンアーキテクチャです。
Lakehouses are enabled by a new system design: implementing similar data structures and data management features to those in a data warehouse directly on top of low cost cloud storage in open formats. 
レイクハウスは、新しいシステム設計によって実現されます。これは、オープンフォーマットの低コストクラウドストレージの上に、データウェアハウスにあるのと同様のデータ構造とデータ管理機能を直接実装することを意味します。
They are what you would get if you had to redesign data warehouses in the modern world, now that cheap and highly reliable storage (in the form of object stores) are available. 
これは、安価で非常に信頼性の高いストレージ（オブジェクトストアの形で）が利用可能になった現代の世界で、データウェアハウスを再設計する必要がある場合に得られるものです。

A lakehouse has the following key features: 
**レイクハウスには以下の主要な特徴**があります：
(この主要な特徴を満たしていれば、「あ、これレイクハウスっぽい!」って判断できそう...!:thinking:)

- Transaction support: In an enterprise lakehouse many data pipelines will often be reading and writing data concurrently. 
トランザクションサポート：エンタープライズレイクハウスでは、多くのデータパイプラインが同時にデータを読み書きすることがよくあります。
Support for ACID transactions ensures consistency as multiple parties concurrently read or write data, typically using SQL. 
ACIDトランザクションのサポートは、複数の当事者が同時にデータを読み書きする際の一貫性を保証し、通常はSQLを使用します。

- Schema enforcement and governance: The Lakehouse should have a way to support schema enforcement and evolution, supporting DW schema architectures such as star/snowflake-schemas. 
スキーマの強制とガバナンス：レイクハウスは、スキーマの強制と進化をサポートする方法を持つべきであり、星型/スノーフレークスキーマなどのDWスキーマアーキテクチャをサポートします。
The system should be able to reason about data integrity, and it should have robust governance and auditing mechanisms. 
システムはデータの整合性について考慮できる必要があり、堅牢なガバナンスと監査メカニズムを持つべきです。

- BI support: Lakehouses enable using BI tools directly on the source data. 
BIサポート：レイクハウスは、BIツールをソースデータに直接使用できるようにします。
This reduces staleness and improves recency, reduces latency, and lowers the cost of having to operationalize two copies of the data in both a data lake and a warehouse. 
これにより、データの古さが減少し、最新性が向上し、レイテンシが減少し、データレイクとデータウェアハウスの両方にデータの2つのコピーを運用化するコストが低下します。

- Storage is decoupled from compute: In practice this means storage and compute use separate clusters, thus these systems are able to scale to many more concurrent users and larger data sizes. 
**ストレージはコンピュートから分離**されています：実際には、ストレージとコンピュートが別々のクラスターを使用することを意味し、これによりこれらのシステムは多くの同時ユーザーや大きなデータサイズにスケールできるようになります。
Some modern data warehouses also have this property. 
一部の現代のデータウェアハウスもこの特性を持っています。

- Openness: The storage formats they use are open and standardized, such as Parquet, and they provide an API so a variety of tools and engines, including machine learning and Python/R libraries, can efficiently access the data directly. 
オープン性：**彼らが使用するストレージフォーマットはオープンで標準化されており、Parquetなどの形式が含まれます。また、さまざまなツールやエンジン（機械学習やPython/Rライブラリを含む）がデータに直接効率的にアクセスできるようにAPIを提供**します。

- Support for diverse data types ranging from unstructured to structured data: The lakehouse can be used to store, refine, analyze, and access data types needed for many new data applications, including images, video, audio, semi-structured data, and text. 
様々なデータタイプのサポート：レイクハウスは、画像、動画、音声、半構造化データ、テキストなど、多くの新しいデータアプリケーションに必要なデータタイプを保存、精製、分析、アクセスするために使用できます。

- Support for diverse workloads: including data science, machine learning, and SQL and analytics. 
多様なワークロードのサポート：データサイエンス、機械学習、SQLおよび分析を含みます。
Multiple tools might be needed to support all these workloads but they all rely on the same data repository. 
これらすべてのワークロードをサポートするためには複数のツールが必要になるかもしれませんが、すべてが同じデータリポジトリに依存しています。

- End-to-end streaming: Real-time reports are the norm in many enterprises. 
エンドツーエンドのストリーミング：リアルタイムレポートは多くの企業で標準となっています。
Support for streaming eliminates the need for separate systems dedicated to serving real-time data applications. 
ストリーミングのサポートにより、リアルタイムデータアプリケーションを提供するための専用システムが不要になります。

<!-- ここまで読んだ! -->

These are the key attributes of lakehouses. 
これらがレイクハウスの主要な属性です。
Enterprise grade systems require additional features. 
エンタープライズグレードのシステムには追加の機能が必要です。
Tools for security and access control are basic requirements. 
セキュリティとアクセス制御のためのツールは基本的な要件です。
Data governance capabilities including auditing, retention, and lineage have become essential particularly in light of recent privacy regulations. 
監査、保持、系譜を含むデータガバナンス機能は、特に最近のプライバシー規制を考慮すると不可欠になっています。
Tools that enable data discovery such as data catalogs and data usage metrics are also needed. 
データカタログやデータ使用メトリクスなど、データ発見を可能にするツールも必要です。
With a lakehouse, such enterprise features only need to be implemented, tested, and administered for a single system. 
レイクハウスを使用すると、そのようなエンタープライズ機能は単一のシステムに対してのみ実装、テスト、管理する必要があります。

Read the full research paper on the inner workings of the Lakehouse. 
レイクハウスの内部動作に関する完全な研究論文をお読みください。

## Some early examples いくつかの初期の例

The Databricks Lakehouse Platform has the architectural features of a lakehouse. 
Databricks Lakehouseプラットフォームは、**レイクハウスのアーキテクチャ的特徴**を持っています。
Microsoft's Azure Synapse Analytics service, which integrates with Azure Databricks, enables a similar lakehouse pattern. 
MicrosoftのAzure Synapse Analyticsサービスは、Azure Databricksと統合され、類似のレイクハウスパターンを可能にします。
Other managed services such as BigQuery and Redshift Spectrum have some of the lakehouse features listed above, but they are examples that focus primarily on BI and other SQL applications. 
BigQueryやRedshift Spectrumなどの他のマネージドサービスは、上記のいくつかのレイクハウス機能を持っていますが、主にBIや他のSQLアプリケーションに焦点を当てた例です。
Companies who want to build and implement their own systems have access to open source file formats (Delta Lake, Apache Iceberg, Apache Hudi) that are suitable for building a lakehouse. 
独自のシステムを構築・実装したい企業は、レイクハウスの構築に適したオープンソースのファイルフォーマット（Delta Lake、Apache Iceberg、Apache Hudi）にアクセスできます。

Merging data lakes and data warehouses into a single system means that data teams can move faster as they are able to use data without needing to access multiple systems. 
データレイクとデータウェアハウスを単一のシステムに統合することは、データチームが複数のシステムにアクセスすることなくデータを使用できるため、より迅速に動けることを意味します。
The level of SQL support and integration with BI tools among these early lakehouses are generally sufficient for most enterprise data warehouses. 
これらの初期のレイクハウスにおけるSQLサポートのレベルとBIツールとの統合は、一般的にほとんどのエンタープライズデータウェアハウスにとって十分です。
Materialized views and stored procedures are available but users may need to employ other mechanisms that aren't equivalent to those found in traditional data warehouses. 
マテリアライズドビューやストアドプロシージャは利用可能ですが、ユーザーは従来のデータウェアハウスに見られるものと同等ではない他のメカニズムを使用する必要があるかもしれません。
The latter is particularly important for "lift and shift scenarios", which require systems that achieve semantics that are almost identical to those of older, commercial data warehouses. 
後者は特に「リフトアンドシフトシナリオ」にとって重要であり、これは古い商用データウェアハウスとほぼ同一の意味論を達成するシステムを必要とします。

What about support for other types of data applications? 
他のタイプのデータアプリケーションに対するサポートはどうでしょうか？
Users of a lakehouse have access to a variety of standard tools (Spark, Python, R, machine learning libraries) for non BI workloads like data science and machine learning. 
レイクハウスのユーザーは、データサイエンスや機械学習のような非BIワークロードのために、さまざまな標準ツール（Spark、Python、R、機械学習ライブラリ）にアクセスできます。
Data exploration and refinement are standard for many analytic and data science applications. 
データの探索と洗練は、多くの分析およびデータサイエンスアプリケーションにおいて標準的です。
Delta Lake is designed to let users incrementally improve the quality of data in their lakehouse until it is ready for consumption. 
Delta Lakeは、ユーザーがレイクハウス内のデータの品質を段階的に向上させ、消費可能な状態になるまで改善できるように設計されています。

A note about technical building blocks. 
技術的なビルディングブロックについての注意点です。
While distributed file systems can be used for the storage layer, objects stores are more commonly used in lakehouses. 
分散ファイルシステムはストレージ層に使用できますが、**オブジェクトストアはレイクハウスでより一般的に使用されます。**
Object stores provide low cost, highly available storage, that excel at massively parallel reads - an essential requirement for modern data warehouses. 
**オブジェクトストアは、低コストで高可用性のストレージを提供し、大規模な並列読み取りに優れています - これは現代のデータウェアハウスにとって不可欠な要件**です。(S3は並列読み取りに優れてるのか...!:thinking:)

<!-- ここまで読んだ! -->

## From BI to AI

The lakehouse is a new data management architecture that radically simplifies enterprise data infrastructure and accelerates innovation in an age when machine learning is poised to disrupt every industry. 
レイクハウスは、企業のデータインフラを根本的に簡素化し、機械学習がすべての業界を変革しようとしている時代において、革新を加速させる新しいデータ管理アーキテクチャです。
In the past most of the data that went into a company's products or decision making was structured data from operational systems, whereas today, many products incorporate AI in the form of computer vision and speech models, text mining, and others. 
過去には、企業の製品や意思決定に使用されるデータのほとんどは、運用システムからの構造化データでしたが、今日では、多くの製品がコンピュータビジョンや音声モデル、テキストマイニングなどの形でAIを取り入れています。
Why use a lakehouse instead of a data lake for AI? 
**AIのためにデータレイクの代わりにレイクハウスを使用する理由は何でしょうか？**
A lakehouse gives you data versioning, governance, security and ACID properties that are needed even for unstructured data. 
レイクハウスは、非構造化データに必要なデータのバージョニング、ガバナンス、セキュリティ、およびACID特性を提供します。

Current lakehouses reduce cost but their performance can still lag specialized systems (such as data warehouses) that have years of investments and real-world deployments behind them. 
**現在のレイクハウスはコストを削減しますが、数年の投資と実世界での展開がある専門的なシステム（データウェアハウスなど）に対してパフォーマンスが劣ることがあります。**
Users may favor certain tools (BI tools, IDEs, notebooks) over others so lakehouses will also need to improve their UX and their connectors to popular tools so they can appeal to a variety of personas. 
ユーザーは特定のツール（BIツール、IDE、ノートブック）を他のツールよりも好む場合があるため、レイクハウスはさまざまなユーザーにアピールできるように、UXや人気ツールへのコネクタを改善する必要があります。
These and other issues will be addressed as the technology continues to mature and develop. 
これらおよびその他の問題は、技術が成熟し発展し続けるにつれて対処されるでしょう。
Over time lakehouses will close these gaps while retaining the core properties of being simpler, more cost efficient, and more capable of serving diverse data applications. 
時間が経つにつれて、レイクハウスはこれらのギャップを埋めつつ、よりシンプルでコスト効率が高く、多様なデータアプリケーションに対応できるというコア特性を保持します。
Read the FAQ on Data Lakehouse for more details. 
詳細については、Data Lakehouseに関するFAQをお読みください。

<!-- ここまで読んだ! -->
