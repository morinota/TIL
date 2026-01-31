refs: https://www.starburst.io/blog/best-practices-for-optimizing-apache-iceberg-performance/

タイトル: Best Practices for Optimizing Apache Iceberg Performance　Apache Icebergパフォーマンス最適化のためのベストプラクティス

You’ve heard the promise. Iceberg delivers warehouse-like performance on data lake infrastructure. 
あなたはその約束を聞いたことがあるでしょう。Icebergはデータレイクインフラストラクチャ上で倉庫のようなパフォーマンスを提供します。
It handles petabyte-scale Apache Iceberg tables. 
それはペタバイト規模のApache Icebergテーブルを処理します。
It’s faster than Hive. 
それはHiveよりも速いです。

But there’s a problem with this. 
しかし、これには問題があります。
Potential doesn’t equal actual. 
可能性は実際とは等しくありません。
Getting peak performance from Iceberg isn’t automatic. 
**Icebergからピークパフォーマンスを得ることは自動的ではありません。**
It requires intentional data architectural design choices, a robust data maintenance strategy, and consistent upkeep. 
それには意図的なデータアーキテクチャ設計の選択、堅牢なデータメンテナンス戦略、および一貫した維持管理が必要です。
Without proper optimization strategies, even the most promising data platform can fall short of expectations. 
**適切な最適化戦略がなければ、最も有望なデータプラットフォームでさえ期待を下回ることがあります。**

In this article, we’ll look at why Iceberg has become central to lakehouse architecture and how to ensure you continue to get the best performance from your implementation. 
この記事では、なぜIcebergがレイクハウスアーキテクチャの中心になったのか、そして実装から最高のパフォーマンスを得続けるための方法を見ていきます。
We’ll also explore automation options that reduce the heavy lifting for data engineering teams. 
また、データエンジニアリングチームの負担を軽減する自動化オプションについても探ります。

<!-- ここまで読んだ! -->

## 1. The benefits of Apache Iceberg Apache Icebergの利点

Let’s start at the beginning. 
まずは始めましょう。
Apache Iceberg is a data lakehouse open table format. 
Apache Icebergはデータレイクハウスのオープンテーブルフォーマットです。
It’s not a storage system itself but rather a layer on top of your existing data lake storage. 
**それ自体はストレージシステムではなく、既存のデータレイクストレージの上にあるレイヤー**です。(うんうん、トランザクション&メタデータレイヤー、という呼ばれ方をしてた...!:thinking:)

Iceberg adds several critical features that address some of the key shortcomings of its predecessors, namely Apache Hive. 
Icebergは、前任者であるApache Hiveのいくつかの主要な欠点に対処するための重要な機能をいくつか追加しています。

Specifically: 
具体的には：

- A metadata-driven approach with table metadata that yields better overall performance when compared to Hive. 
  メタデータ駆動型のアプローチで、テーブルメタデータを使用することで、Hiveと比較して全体的なパフォーマンスが向上します。
  Iceberg metadata provides efficient query planning through its enhanced metadata collection. 
  Icebergのメタデータは、強化されたメタデータ収集を通じて効率的なクエリ計画を提供します。

- ACID transactions to guarantee consistent operations across partitions, enabling reliable real-time data ingestion and updates. 
  ACIDトランザクションにより、パーティション間で一貫した操作を保証し、信頼性の高いリアルタイムデータの取り込みと更新を可能にします。

- Easy schema evolution, allowing you to alter and change your table structures without expensive migration as your business changes over time. 
  **簡単なスキーマ進化**により、ビジネスの変化に応じて高額な移行なしにテーブル構造を変更できます。

- Time travel and rollbacks, enabled by detailed snapshotting whenever an Iceberg table changes. 
  Icebergテーブルが変更されるたびに詳細なスナップショットを取得することで、タイムトラベルとロールバックが可能になります。
  This functionality allows you to query historical states in a dataset easily. 
  この機能により、データセット内の過去の状態を簡単にクエリできます。

<!-- ここまで読んだ! -->

### 1.1. Iceberg + Trino Iceberg + Trino

Now for the interesting part, connecting Iceberg and Trino. 
さて、面白い部分、IcebergとTrinoを接続することです。
Iceberg on its own is impressive, but to really shine, it needs to be used in the appropriate data ecosystem. 
Icebergは単独でも印象的ですが、**本当に輝くためには適切なデータエコシステムで使用する必要**があります。
This is particularly true when combined with a distributed SQL query engine like Trino. 
これは、Trinoのような**分散SQLクエリエンジンと組み合わせたときに特に当てはまります。** 
Iceberg is designed to support tables with petabytes of data; meanwhile, Trino is designed to process them at scale. 
**Icebergはペタバイトのデータを持つテーブルをサポートするように設計**されており、一方でTrinoはそれらをスケールで処理するように設計されています。
When combined, Iceberg and Trino provide a powerful solution for managing and querying large-scale data lakes.
組み合わせることで、IcebergとTrinoは大規模なデータレイクを管理およびクエリするための強力なソリューションを提供します。
Together, they create the Icehouse data architecture (which we’ve written on extensively in the past). 
これらを組み合わせることで、Icehouseデータアーキテクチャが作成されます（私たちは過去にこれについて広範に執筆しています）。

- メモ: 分散SQLクエリエンジン(distributed SQL query engine)とは?
  - **1つのSQLクエリを、複数のノード(サーバー)に分散して並列実行するクエリエンジン**。
  - AthenaとかSnowflakeとかも、これに当てはまる?? :thinking:
    - AthenaはドンピシャでYes! Snowflakeも広義でYes!
  - 代表例を分類:
    - OSS/自前ホスティング系
      - Trino, Presto, etc.
    - マネージド分散SQLサービス系
      - **Athena**, BigQuery, Redshift Serverless, etc.
      - (これらは中身で上述のPresto/Trino系が動いてるらしい...!!:thinking:)
    - DWH型 (独自エンジン)
      - Snowflake
      - 完全に独自実装だが、中身は分散SQLクエリエンジンの一種と考えられる。
      - Icebergも「外部テーブル」として扱える。
  - まあもちろんPyIcebergで十分な時もあるだろうが、それこそ書き込みの時とか。readなどで真価を発揮するのはAthenaなどの分散SQLクエリエンジンなのか...!:thinking:

<!-- ここまで読んだ! -->

### 1.2. How Iceberg optimizes query performance Icebergがクエリパフォーマンスを最適化する方法

How does Iceberg achieve its half of the optimization equation? 
Icebergは最適化の方程式の半分をどのように達成するのでしょうか？
The answer lies in its value for data discovery, coupled with its ability to adapt and change easily, as a result of its metadata collection and ACID compliance. 
その答えは、**データ発見の価値と、メタデータ収集およびACID準拠の結果として容易に適応し変化する能力**にあります。
The result is not only versatile, but also performant. 
その結果は、単に多用途であるだけでなく、パフォーマンスも優れています。

How much faster is Iceberg? 
Icebergはどれくらい速いのでしょうか？
According to the Apache Iceberg project, when managed well, Iceberg can yield 10x performance improvements over Hive. 
Apache Icebergプロジェクトによると、適切に管理されている場合、IcebergはHiveに対して10倍のパフォーマンス向上をもたらすことができます。
We’ve written on Iceberg performance before, and we continue to see Iceberg outperform other data architectures, especially when coupled with Trino. 
私たちは以前にIcebergのパフォーマンスについて執筆しており、特にTrinoと組み合わせたときにIcebergが他のデータアーキテクチャを上回るのを引き続き確認しています。

<!-- ここまで読んだ! -->

## 2. Key performance optimizations for Apache Iceberg　Apache Icebergのための主要なパフォーマンス最適化

Again, though, this isn’t a given. 
しかし、これは当然のことではありません。
Iceberg has many inherent advantages that make it capable of high performance, but to get this level of performance, you need to take certain steps in your data architecture to achieve this potential.
Icebergには高いパフォーマンスを実現するための多くの固有の利点がありますが、このレベルのパフォーマンスを得るためには、データアーキテクチャにおいて特定の手順を踏む必要があります。

### 2.1. What steps do you need to take to ensure that Iceberg performs optimally?　Icebergが最適に動作することを保証するために、どのような手順を踏む必要がありますか？

There are many ways to fine-tune Iceberg. 
Icebergを微調整する方法はいくつもあります。
One starting point is to ensure that all tables are structured properly. 
一つの出発点は、すべてのテーブルが適切に構造化されていることを確認することです。
This includes partitioning, and Iceberg handles partitioning very differently than other technologies like Hive. 
これにはパーティショニングが含まれ、IcebergはHiveのような他の技術とは非常に異なる方法でパーティショニングを処理します。
To get results, the right partitioning strategy, query patterns, and maintenance routines make all the difference.
結果を得るためには、**適切なパーティショニング戦略、クエリパターン、およびメンテナンスルーチンが重要**です。
(S3 Tablesの場合は、メンテナンスルーチンは任せられるのかな...!!:thinking:)

Files can be written with organization strategies such as sorting and bucketing to improve performance when access patterns are well understood.
アクセスパターンがよく理解されている場合、ファイルはソートやバケット化などの組織戦略を用いて書き込むことができ、パフォーマンスを向上させます。

<!-- ここまで読んだ! -->

### 2.2. Why you need to maintain Iceberg properly Icebergを適切に維持する必要がある理由

Additionally, you need to ensure that performance does not degrade over time due to a phenomenon known as the small files problem.
さらに、**パフォーマンスが時間とともに劣化しないように、small files problem（小ファイル問題）として知られる現象に対処する必要があります。**
This problem occurs due to the frequency and volume of data modifications and how those changes are implemented with versioning strategies, including Merge-on-Read (MOR).
この問題は、データの変更頻度と量、そしてそれらの変更がMerge-on-Read（MOR）を含むバージョニング戦略でどのように実装されるかによって発生します。
While data updates via MOR help maintain lineage for the table snapshots that make Iceberg so valuable, they do represent a maintenance challenge if left unchecked.
MORを介したデータの更新は、Icebergを非常に価値のあるものにするテーブルスナップショットの系譜を維持するのに役立ちますが、放置するとメンテナンスの課題を引き起こします。

Without regular maintenance, you can encounter performance decreases as tables change.
**定期的なメンテナンスがないと、テーブルが変更されるにつれてパフォーマンスが低下する可能性**があります。
Understanding these trade-offs between flexibility and optimization is essential for data engineering teams.
柔軟性と最適化の間のこれらのトレードオフを理解することは、データエンジニアリングチームにとって不可欠です。

We love Iceberg. 
私たちはIcebergが大好きです。
And we’ve spent a lot of time leveraging its power for our customers. 
私たちはその力を顧客のために活用するために多くの時間を費やしてきました。
We’ve consistently identified the following optimization strategies as yielding the biggest performance bang for your buck:
**私たちは、次の最適化戦略が最も大きなパフォーマンス向上をもたらすことを一貫して特定しています：**

- Partitioning (まあめちゃ効果的だよね...!!:thinking:)
- Sorted tables (なんだろ??:thinking:)
- File management and compaction ファイル管理と圧縮 (これはS3 Tablesにお任せできるのかな...!!:thinking:)
- Snapshot management スナップショット管理 (これもS3 Tablesにお任せできるのかな...!!:thinking:)
- Monitoring and measuring performance パフォーマンスの監視と測定 (これもS3 Tablesにお任せできるのかな...!!:thinking:)

Let’s look at each one in turn.
それぞれを順に見ていきましょう。

<!-- ここまで読んだ! -->

### 2.3. Partitioning パーティショニング

Good partitioning acts as a filtering system at the directory level. 
良いパーティショニングは、ディレクトリレベルでのフィルタリングシステムとして機能します。
When you partition tables correctly, Iceberg enables partition pruning during query scanning, dramatically reducing the files that need to be read.
テーブルを正しくパーティショニングすると、Icebergはクエリスキャン中にパーティションプルーニングを可能にし、読み取る必要のあるファイルを大幅に削減します。

Not all tables are big enough to partition. 
すべてのテーブルがパーティショニングするのに十分な大きさであるわけではありません。
Generally, a table’s overall file size footprint should be at least 1TB before utilizing partitions.
**一般的に、テーブルの全体的なファイルサイズは、パーティションを利用する前に少なくとも1TBであるべき**です。
(ん？？合計で1TB未満のテーブルはパーティショニングしないほうが良い、という意味...??:thinking:)

<!-- ここまで読んだ! -->

#### 2.3.1. Choose efficient partition columns　効率的なパーティション列を選択する

Pick low-cardinality columns with fairly uniform distributions. 
**低カーディナリティの列を選び、比較的一様な分布を持つもの**を選択します。(なるほど、じゃあbucket()とかもまさに一様分布だ...!!:thinking:)
Time-series data works well: partition by month or day using timestamp columns, depending on your data volume.
**時系列データはうまく機能します：データ量に応じて、タイムスタンプ列を使用して月または日でパーティションを分けます。**
Columns like region, product_category, or customer_segment can also be effective. 
region、product_category、customer_segmentのような列も効果的です。
(product_categoryって、アイテムの種別か...!! partition用のカラムとして追加してもいいかも。:thinking:)
Avoid high-cardinality columns, such as user IDs or transaction IDs, as they create too many partitions.
ユーザーIDやトランザクションIDのような高カーディナリティの列は避けてください。これらはあまりにも多くのパーティションを作成します。

<!-- ここまで読んだ! -->

#### 2.3.2. Avoid over-partitioning　過剰なパーティショニングを避ける

At a minimum, your total file size per partition should be in the 1GB – 10GB range, but ideally be 10GB – 100GB.
**最低でも、パーティションごとの総ファイルサイズは1GBから10GBの範囲であるべきですが、理想的には10GBから100GBであるべき**です。
Individual file sizes themselves should be targeted at 100MB+ each to maintain optimal read performance.
**個々のファイルサイズは、最適な読み取りパフォーマンスを維持するために100MB以上を目指すべき**です。(これ、小さめのテーブルだとなってないかも...!!:thinking:)
This keeps the number of files in the range of 100-1000 files.
これにより、ファイルの数は100〜1000ファイルの範囲に保たれます。

Too many small partitions hurt more than they help. 
**あまりにも多くの小さなパーティションは、助けるよりも害を及ぼします。**
If your daily data is only 2GB, partition by month instead.
**もし日々のデータがわずか2GBであれば、月ごとにパーティションを分けるべき**です。
(でもクエリシナリオ的に、日付単位でクエリすることが多いんだとしたら、日付単位でpartitionしたほうがデータスキャン量は減るよなあ。:thinking:)
(あと、1つのパーティションあたり1GB〜10GBの範囲であるべき、なら2GB/日なら日付単位でpartitionしてもいいのでは??:thinking:)

#### 2.3.3. Leverage hidden partitioning hidden partitioningを活用する

Unlike Hive, Iceberg doesn’t force users to think about partition columns in their queries. 
Hiveとは異なり、Icebergはユーザーにクエリ内でパーティション列を考慮させることを強制しません。
Hidden partitioning automatically routes queries to the right partitions based on filter predicates. 
隠れたパーティショニングは、フィルタ述語に基づいてクエリを適切なパーティションに自動的にルーティングします。
This prevents user errors and simplifies query writing.
これにより、ユーザーエラーが防止され、クエリの記述が簡素化されます。

#### 2.3.4. Consider partition evolution パーティション進化を考慮する

As your use cases change, Iceberg allows you to modify your partitioning strategy without rewriting data, adapting to new query patterns as your workloads evolve.
ユースケースが変化するにつれて、**Icebergはデータを再書き込みすることなくパーティショニング戦略を変更できる**ようになっています。ワークロードが進化するにつれて、新しいクエリパターンに適応します。(うんうん、これがIcebergの強みの1つだよなあ...!!:thinking:)

<!-- ここまで読んだ! -->

### 2.4. Sorted tables and bucketing ソートされたテーブルとバケット化

Data written in sorted order by one or more columns enables aggressive file skipping during queries.
**1つまたは複数の列でソートされた順序で書き込まれたデータは、クエリ中に積極的なファイルスキップを可能にします。**
Sorted tables are one of Iceberg’s most powerful performance features and a well-used strategy when looking for a range of values on the sorted column.
**sorted tableは、Icebergの最も強力なパフォーマンス機能の1つ**であり、ソートされた列の値の範囲を探す際に良く使用される戦略です。
(sorted table機能、認識してなかったな。partitionとは別のアプローチがあったのか。それこそ静的特徴量はテーブル定義内でnews_id的なカラムでsortされるようににしておくと、後からreadする時に効果的そう...!:thinking:)

An alternate strategy is bucketing. 
別の戦略はバケット化です。(=これはpartition機能の1つで、transformとしてbucket()を使うやつだよな...!!:thinking:)
Bucketing helps to eliminate data skew by clumping all distinct values of a high cardinality column (such as customer ID) into a given “bucket” file.
**バケット化は、高カーディナリティの列（顧客IDなど）のすべての異なる値を特定の「バケット」ファイルにまとめることで、データの偏りを排除するのに役立ちます。**
Each bucket will contain many distinct values, but again, all rows of that column’s value will be in the same bucket.
各バケットには多くの異なる値が含まれますが、再度、その列の値のすべての行は同じバケットに存在します。

<!-- ここまで読んだ! -->

Consider a real-world example from TPC-DS 1TB benchmark testing:
TPC-DS 1TB[ベンチマークテスト](https://www.starburst.io/blog/improving-performance-with-iceberg-sorted-tables/)からの実世界の例を考えてみましょう：

- Unsorted table: 1.4 billion rows read, 8.09GB data scanned
  - ソートされていないテーブル：14億行が読み取られ、8.09GBのデータがスキャンされました
- Sorted table: 387 million rows read, 2.4GB data scanned
  - ソートされたテーブル：3.87億行が読み取られ、2.4GBのデータがスキャンされました
- Result: Nearly 50% reduction in data processed
  - 結果：処理されたデータがほぼ50％削減されました (ん?? 8.09GB -> 2.4GBは70%近く減ってるような...!!謙遜してほぼ50%ってこと??:thinking:)

<!-- ここまで読んだ! -->

Use sorted tables and bucketing on:
sorted table機能やバケット化の対象となるカラムの選び方の例:

- Columns frequently used in WHERE clauses (WHERE句で頻繁に使用される列)
- Join keys (結合キー)
- Filter predicates in common queries (一般的なクエリのフィルタ述語)
- Date/timestamp columns for range queries (範囲クエリ用の日付/タイムスタンプ列)

**Maintain sorted tables through automation.** 
自動化を通じてsorted tableを維持します。
When you stream or micro-batch data into Iceberg, use the OPTIMIZE command to preserve sort order.
データをIcebergにストリーミングまたはマイクロバッチ処理する際は、**OPTIMIZEコマンドを使用してソート順を保持**します。
(S3 Tablesはこの後から最適化するやつを自動でやってくれるはず...?? だからテーブル定義でsorted orderを定義しておけさえすればいい??:thinking:)
This combines small files while maintaining the sorted structure. 
これにより、小さなファイルが結合され、ソートされた構造が維持されます。
It’s essential for keeping sorted tables effective as data grows.
データが増えるにつれてソートされたテーブルを効果的に保つために不可欠です。

The benefits compound. 
**その利点は累積**します。(=どんどん効果が出てくる、という意味かな...!!:thinking:)
Less data scanned means lower storage costs from fewer Amazon S3 GET operations. 
スキャンされるデータが少ないということは、Amazon S3 GET操作が少なくなるため、ストレージコストが低くなることを意味します。
It also means lower compute requirements. 
また、計算要件が低くなることも意味します。
Your queries run faster and cheaper.
**あなたのクエリはより速く、より安価に実行**されます。

<!-- ここまで読んだ! -->

### 2.5. File management and compaction ファイル管理と圧縮

Iceberg offers a number of high-level features, including time travel and cross-version analysis. 
Icebergは、タイムトラベルやバージョン間分析を含む多くの高レベル機能を提供します。
Tracking these changes requires keeping old versions of files intact through manifest lists and metadata files. 
これらの変更を追跡するには、**マニフェストリストとメタデータファイルを通じて古いバージョンのファイルをそのまま保持する必要があります。**

The downside to this is that files deteriorate over time. 
これに対する欠点は、ファイルが時間とともに劣化することです。
Iceberg generates new metadata and data files whenever a dataset is modified. 
Icebergは、データセットが変更されるたびに新しいメタデータとデータファイルを生成します。
This leads to the proliferation of a number of small files that must be opened and merged on the fly to get the complete picture of a dataset. That leads to performance slowdowns over time.
これにより、**データセットの全体像を把握するために、オンザフライで開いてマージする必要がある多数の小さなファイルが増殖します。これにより、時間の経過とともにパフォーマンスが低下**します。 (S3 Tablesはこれの剪定を結構自動でやってくれてる感:thinking:)

This makes file management one of the central tenets of good Iceberg performance. 
これにより、**ファイル管理は良好なIcebergパフォーマンスの中心的な要素の一つ**となります。
There are several ways to address the problem. 
この問題に対処する方法はいくつかあります。

**Small files hurt performance.** 
小さなファイルはパフォーマンスを損ないます。
Each file has a fixed open/read cost. 
各ファイルには固定のオープン/リードコストがあります。
Thousands of small files mean thousands of I/O operations. 
何千もの小さなファイルは、何千ものI/O操作を意味します。
This becomes a bottleneck even with good metadata. 
これは、良好なメタデータがあってもボトルネックになります。

![]()

In the example above, the query engine has to read 26 smaller “blue” files instead of 2 larger “green” files that represent the exact same data spread out differently. 
上記の例では、クエリエンジンは、異なる方法で分散された同じデータを表す2つの大きな「緑」ファイルの代わりに、26の小さな「青」ファイルを読み取る必要があります。

How to detect the problem. 
問題を検出する方法。
Use the $files metadata table to identify files under 100MB: 
**$filesメタデータテーブルを使用して、100MB未満のファイルを特定**します：

```SQL
SELECT COUNT(*) as small_files FROM "catalog"."schema"."table$files" WHERE file_size_in_bytes < 100000000;
```

Using compaction. 
圧縮を使用します。
You can solve this problem using compaction. 
この問題は圧縮を使用して解決できます。
To do this, use the optimize() command in Trino to consolidate small files into larger ones: 
これを行うには、Trinoの**optimize()コマンド**を使用して小さなファイルを大きなファイルに統合します：

```sql
ALTER TABLE catalog.schema.table EXECUTE optimize(file_size_threshold => '100MB');
```

You should target 100MB file sizes as a best practice, though you can adjust the target file size based on your specific workloads. 
ベストプラクティスとして100MBのファイルサイズを目指すべきですが、特定のワークロードに基づいてターゲットファイルサイズを調整することもできます。
The optimize command is smart—it won’t compact files that don’t need it. 
**optimizeコマンドは賢く、必要のないファイルは圧縮しません。**

<!-- ここまで読んだ! -->

Best practices for compaction: 
圧縮のベストプラクティス：

- Prioritize frequently-queried tables over recently-added data 
  - 最近追加されたデータよりも頻繁にクエリされるテーブルを優先する
- Use filters to compact specific partitions 
  - 特定のパーティションを圧縮するためにフィルターを使用する
- Record filters used during compaction to avoid overlap in future runs 
  - 将来の実行での重複を避けるために、圧縮中に使用したフィルターを記録する
- Consider running compaction on a separate cluster to avoid impacting query workloads 
  - クエリワークロードに影響を与えないように、別のクラスターで圧縮を実行することを検討する
- With time-based partitioning, you can stop compacting data files once it is no longer being modified 
  - 時間ベースのパーティショニングを使用すると、データファイルがもはや変更されなくなった時点で圧縮を停止できます。

(基本的には、S3 Tablesにお任せできると思いつつ、どんな事を裏でやってるのかはざっと認識しておいた方がよさそう、もしパフォーマンスの低下が見られた時に調査しやすいように...!!:thinking:)

<!-- ここまで読んだ! -->

### 2.6. Snapshot management スナップショット管理

Over time, Iceberg accumulates old snapshots and associated metadata. 
時間が経つにつれて、Icebergは古いスナップショットと関連するメタデータを蓄積します。
While these enable time travel functionality, they also consume storage and can impact query planning performance. 
これらはタイムトラベル機能を可能にしますが、ストレージを消費し、クエリ計画のパフォーマンスに影響を与える可能性があります。
Managing snapshots is a critical but often overlooked aspect of Iceberg maintenance. 
スナップショットの管理は、Icebergのメンテナンスにおいて重要ですが、しばしば見落とされる側面です。

Expire snapshots regularly. 
**スナップショットを定期的に期限切れにします。**　(S3 Tablesやってくれてる!ありがとう!:thinking:)
Use the expire_snapshots procedure to remove old snapshots beyond your retention requirements: 
expire_snapshots手続きを使用して、保持要件を超える古いスナップショットを削除します：

```sql
ALTER TABLE catalog.schema.table EXECUTE expire_snapshots(retention_threshold => '7d');
```

Snapshot expiration removes metadata for old versions while preserving the current state and recent history. 
スナップショットの期限切れは、古いバージョンのメタデータを削除し、現在の状態と最近の履歴を保持します。
This cleans up metadata being saved, but more importantly the underlying data files that the expired snapshots were referencing. 
これにより、**保存されているメタデータがクリーンアップされますが、より重要なのは、期限切れのスナップショットが参照していた基盤となるデータファイ**ルです。
Without this, your data lakehouse would continue to hold more and more data files. 
これがなければ、データレイクハウスはますます多くのデータファイルを保持し続けることになります。

Remove orphaned files. 
**孤立したファイルを削除**します。
After snapshot expiration, you may have data files no longer referenced by any snapshot. 
スナップショットの期限切れ後、どのスナップショットにも参照されなくなったデータファイルが存在する可能性があります。
Use remove_orphan_files to reclaim this space: 
remove_orphan_filesを使用してこのスペースを回収します：

```sql
ALTER TABLE catalog.schema.table EXECUTE remove_orphan_files(retention_threshold => '3d');
```

Rewrite manifests periodically. 
マニフェストを定期的に再書き込みます。
As tables evolve, manifest files can become fragmented. 
テーブルが進化するにつれて、マニフェストファイルが断片化する可能性があります。
Use rewrite_manifests to consolidate them: 
rewrite_manifestsを使用してそれらを統合します：

```sql
ALTER TABLE catalog.schema.table EXECUTE rewrite_manifests;
```

This reduces the number of manifest files the query engine must read, improving query planning efficiency. 
これにより、**クエリエンジンが読み取る必要のあるマニフェストファイルの数が減少**し、クエリ計画の効率が向上します。(=クエリ計画にかかる時間が減る、という意味かな...!!:thinking:)

<!-- ここまで読んだ! -->

### 2.7. Monitoring and measuring performance　パフォーマンスの監視と測定

You can’t improve what you don’t measure. 
**測定しないものは改善できません。** (これは結構真理だな〜ダンスとかで自分の動画を撮ってみるのも同じだ...!:thinking:)
Track these metrics consistently to understand your table health and query performance: 
これらのメトリックを一貫して追跡して、テーブルの健康状態とクエリパフォーマンスを理解します：

File statistics.
ファイル統計。
Monitor file counts and sizes over time. 
時間の経過とともにファイルの数とサイズを監視します。
Watch for the proliferation of small files using the $files metadata table. 
$filesメタデータテーブルを使用して小さなファイルの増殖に注意してください。

Query performance metrics. 
クエリパフォーマンスメトリック。
Track query execution times, data scanned, and rows processed. 
クエリの実行時間、スキャンされたデータ、および処理された行を追跡します。
Look for degradation patterns—operations steadily slowing down over time—that indicate maintenance is needed. 
劣化パターン（時間の経過とともに操作が徐々に遅くなること）を探し、メンテナンスが必要であることを示します。

Table health indicators. 
テーブルの健康指標。
Use Iceberg’s metadata tables to understand table state: 
Icebergのメタデータテーブルを使用してテーブルの状態を理解します：

- $files – View data file sizes and counts 
  - $files – データファイルのサイズと数を表示
- $manifests – Track manifest file health and consolidation needs 
  - $manifests – マニフェストファイルの健康状態と統合の必要性を追跡
- $snapshots – Monitor snapshot accumulation and plan expiration schedules 
  - $snapshots – スナップショットの蓄積を監視し、期限切れスケジュールを計画します

Regular monitoring helps you catch performance problems before they impact users and allows you to optimize proactively rather than reactively. 
定期的な監視は、パフォーマンスの問題をユーザーに影響を与える前にキャッチし、反応的ではなく積極的に最適化することを可能にします。

<!-- ここまで読んだ! -->

## 3. Not all data needs to be in Iceberg　すべてのデータがIcebergにある必要があるわけではありません。

This leaves one question unaddressed.
これにより、一つの質問が未解決のまま残ります。

**Should your data even be in Iceberg?　あなたのデータは本当にIcebergにあるべきでしょうか？**

Years of focusing on data centralization as a panacea for data silos have led many of us to view it as the default position.
データのサイロに対する万能薬としてデータの集中化に焦点を当てた何年もの間、多くの人々はそれをデフォルトの立場と見なすようになりました。
In practice, mass centralization is a massive endeavor that often runs over time and budget.
実際には、大規模な集中化は膨大な努力を要し、しばしば時間と予算を超過します。

Ironically, mass centralization often results in more data siloes.
皮肉なことに、大規模な集中化はしばしばより多くのデータサイロを生む結果となります。
That’s because business teams, frustrated by the slow pace of migration, go off and invent their own solutions.
**それは、移行の遅いペースに苛立ったビジネスチームが、自分たちの解決策を考案するから**です。

Centralization may not even be practical given today’s legal realities.
集中化は、今日の法的現実を考えると実用的でないかもしれません。
For example, data sovereignty laws mean some data can never leave a given country’s borders.
例えば、データ主権法は、特定のデータが特定の国の境界を越えることができないことを意味します。

We advocate a more incremental approach.
私たちは、より段階的なアプローチを提唱します。
Use query tools like Trino to access distributed data by default.
Trinoのようなクエリツールを使用して、デフォルトで分散データにアクセスします。
From there, identify high-value datasets to move over.
そこから、移動させる高価値データセットを特定します。
These are datasets that:
これらは以下のようなデータセットです：

- Are critical to the business.
  - ビジネスにとって重要です。
- Are frequently accessed by multiple users across different use cases.
  - **異なるユースケースで複数のユーザーによって頻繁にアクセス**されます。
  - (共通化されるべき特徴量たちとか...!:thinking:)
- Will most benefit from Iceberg’s advanced features.
  - **Icebergの高度な機能から最も利益を得ることができます。**
  - (これもYesのはず! 大規模だし、高頻度で読み書きするし...! 後でもう少し言語化したい:thinking:)

In other words, leave data federated if it doesn’t need the performance boost.
言い換えれば、パフォーマンスの向上が必要でない場合はデータをフェデレートのままにしておきます。
Don’t let migration become a blocker to new projects.
**移行が新しいプロジェクトの障害にならないように**しましょう。
(これは肝に銘じるべきか...!!:thinking:)

<!-- ここまで読んだ! -->

## 4. The Icehouse: Delivering performance + flexibility　Icehouse：パフォーマンスと柔軟性の提供

(この章は、本ブログを書いてるStarburst社の、ポジショントーク的な内容っぽいので、ざっくり読む感じでいいかも...!!:thinking:)

Starburst Icehouse architecture implements precisely this level of choice with data centralization.
Starburst Icehouseアーキテクチャは、データの集中化によってまさにこのレベルの選択肢を実現します。
Driven by the combination of Iceberg and Trino, the Icehouse serves as the central nervous system of your data platform. 
IcebergとTrinoの組み合わせによって推進されるIcehouseは、あなたのデータプラットフォームの中枢神経系として機能します。
It connects your data applications and key data processing tools to your data, no matter where it lives.
それは、あなたのデータアプリケーションと主要なデータ処理ツールを、データがどこにあってもあなたのデータに接続します。
In short, the Icehouse is all about choice. 
要するに、Icehouseは選択肢に関するものです。
Your data, your way, when and how you need it.
あなたのデータ、あなたの方法で、必要なときに、必要な方法で。
You can build an Icehouse architecture yourself. 
あなた自身でIcehouseアーキテクチャを構築することもできます。
Or you can use Starburst, which implements the Icehouse along with several performance-boosting features for Iceberg:
または、Icehouseを実装し、Icebergのためのいくつかのパフォーマンス向上機能を備えたStarburstを使用することもできます。
Automated Iceberg data maintenance. 
自動化されたIcebergデータメンテナンス。
Starburst data maintenance scheduling enables you to configure regular maintenance tasks—including compaction, snapshot expiration, and orphan file removal—so your tables remain query-ready at all times. 
Starburstのデータメンテナンススケジューリングにより、定期的なメンテナンスタスク（圧縮、スナップショットの有効期限、孤立ファイルの削除など）を設定できるため、テーブルは常にクエリ可能な状態を維持します。
This automation eliminates the manual overhead that data engineering teams typically face.
この自動化により、データエンジニアリングチームが通常直面する手動の負担が排除されます。
Warp Speed. 
ワープスピード。
A proprietary caching and indexing layer that boosts query performance by up to 7x and reduces cloud computing costs by as much as 40% through intelligent read performance optimization.
クエリパフォーマンスを最大7倍向上させ、インテリジェントな読み取りパフォーマンス最適化を通じてクラウドコンピューティングコストを最大40%削減する独自のキャッシングおよびインデックス層です。
Managed Iceberg Pipelines. 
管理されたIcebergパイプライン。
When you are ready to migrate data to Iceberg, Starburst makes it easy with zero-ops managed pipelines. 
データをIcebergに移行する準備ができたとき、Starburstはゼロオペレーションの管理パイプラインで簡単にします。
Managed Iceberg Pipelines produce production-ready workflows that result in 10x faster queries and a 66% reduction in data costs. 
管理されたIcebergパイプラインは、10倍速いクエリとデータコストの66%削減を実現する生産準備完了のワークフローを生成します。
Ingest data from Kafka Streaming or from AWS S3 using our new file ingest, which makes it easier than ever to keep your Iceberg tables hydrated with fresh data.
新しいファイルインジェストを使用して、Kafka StreamingまたはAWS S3からデータを取り込み、Icebergテーブルを新鮮なデータで常に潤すことがこれまで以上に簡単になります。
To learn more about how Starburst can give you both choice and performance for Apache Iceberg, contact us today.
StarburstがApache Icebergに対して選択肢とパフォーマンスの両方を提供できる方法について詳しく知りたい場合は、今日中にお問い合わせください。

<!-- ここまで読んだ! -->
