refs: https://www.stackgazer.com/p/what-is-hidden-partitioning-in-apache-iceberg


# Already have an account?Sign in
# What is Hidden Partitioning in Apache Iceberg? 
# すでにアカウントをお持ちですか？サインイン

### Iceberg - built at Netflix, succeeded in abstracting partitioning logic from users of the data, making it a powerful force in the big-data industry. How did they do it though?
### Iceberg - Netflixで開発され、データのパーティショニングロジックをユーザから抽象化することに成功し、ビッグデータ業界で強力な存在となりました。彼らはどのようにそれを実現したのでしょうか？

Dixyantar Panda  
Dixyantar Panda

Apache Iceberg was initially developed at Netflix to address limitations in the Hive table format, particularly for large-scale analytics workloads.  
Apache Icebergは、特に大規模な分析ワークロードにおけるHiveテーブルフォーマットの制限に対処するために、Netflixで最初に開発されました。

It became an Apache top-level project in 2020 and has gained significant adoption across major companies like Netflix, Apple, and LinkedIn due to its innovative approach to table management.  
2020年にApacheのトップレベルプロジェクトとなり、テーブル管理における革新的なアプローチにより、Netflix、Apple、LinkedInなどの主要企業で大きな採用を得ています。

Traditional data lake partitioning schemes expose partitioning to users, forcing them to understand storage layout and explicitly reference partition columns in queries.  
従来のデータレイクのパーティショニングスキームは、パーティショニングをユーザに公開し、ストレージレイアウトを理解し、クエリ内でパーティション列を明示的に参照することを強制します。

Apache Iceberg introduces hidden partitioning—a metadata-driven approach that improves query performance without burdening users with partition awareness.  
Apache Icebergは、ユーザにパーティションの認識を負わせることなくクエリパフォーマンスを向上させるメタデータ駆動型アプローチであるhidden partitioning（隠れたパーティショニング）を導入します。



## What is the Conventional Data-Partitioning Approach? 従来のデータパーティショニングアプローチとは？

In traditional database and data lake systems, partitioning is explicitly visible in both the storage layout and query interface. 
従来のデータベースおよびデータレイクシステムでは、パーティショニングはストレージレイアウトとクエリインターフェースの両方に明示的に表示されます。このモデルは、いくつかの重要な課題を生み出します。

### Directory-Based Physical Organization ディレクトリベースの物理的組織

Traditional systems like Hive implement partitioning through a hierarchical directory structure, where each partition value creates a new directory in the filesystem. 
Hiveのような従来のシステムは、階層的なディレクトリ構造を通じてパーティショニングを実装し、各パーティション値がファイルシステム内に新しいディレクトリを作成します。

For example, in a date-based partitioning, directories are created at year, month and day levels. 
例えば、日付ベースのパーティショニングでは、年、月、日レベルでディレクトリが作成されます。

```
/table/year=2025/month=04/day=01/data1.parquet 
/table/year=2025/month=04/day=02/data2.parquet 
/table/year=2025/month=05/day=01/data3.parquet
```

*Hive uses Parquet file format - an open source columnar storage format. 
*HiveはParquetファイル形式を使用しています - これはオープンソースのカラムストレージ形式です。

### Query-Time Partition Awareness クエリ時のパーティション認識

With traditional partitioning, users must explicitly include partition columns in their queries to achieve partition pruning. 
従来のパーティショニングでは、ユーザーはパーティションプルーニングを達成するために、クエリにパーティション列を明示的に含める必要があります。

Without partition columns specified you trigger a scan of the entire dataset. 
パーティション列が指定されていない場合、データセット全体のスキャンがトリガーされます。

```
SELECT * FROM events
WHERE event_timestamp = '2025-04-01';
```

With partition columns, irrelevant directories are excluded from the scan. 
パーティション列を使用すると、無関係なディレクトリがスキャンから除外されます。

```
SELECT * FROM events
WHERE year = 2025 AND month = 4 AND day = 1;
```

This approach pushes the complexity of understanding the physical data layout onto users and application developers, creating a tight coupling between physical organization and logical queries. 
このアプローチは、物理データレイアウトを理解する複雑さをユーザーやアプリケーション開発者に押し付け、物理的な組織と論理的なクエリの間に密接な結合を生み出します。

Partitioning is a vast topic with numerous considerations and approaches. 
パーティショニングは広範なトピックであり、多くの考慮事項とアプローチがあります。

For a more comprehensive understanding, you can refer to Martin Kleppmann's in-depth treatment in Chapter 6 of "Designing Data-Intensive Applications" and the groundbreaking work on workload-aware partitioning in the Schism paper by Curino et al. 
より包括的な理解のためには、Martin Kleppmannの「Designing Data-Intensive Applications」の第6章の詳細な解説や、CurinoらによるSchism論文のワークロード認識パーティショニングに関する画期的な研究を参照してください。



## Icebergのパーティショニングアプローチとそのメタデータアーキテクチャ

Iceberg's hidden partitioning capability is built on a multi-tiered metadata architecture that separates table state from data files. 
Icebergの隠れたパーティショニング機能は、テーブルの状態とデータファイルを分離する多層メタデータアーキテクチャに基づいています。この分離により、Icebergは物理的な組織を通じてではなく、メタデータレベルでパーティション情報を追跡することができます。

The architecture consists of three key components.
このアーキテクチャは、3つの主要なコンポーネントで構成されています。

- Metadata Files: Store table schema, partition specifications, snapshots, and configuration
- メタデータファイル: テーブルスキーマ、パーティション仕様、スナップショット、および設定を保存します。
- Manifest Lists: Track all manifests for a snapshot, including partition value ranges for each manifest
- マニフェストリスト: スナップショットのすべてのマニフェストを追跡し、各マニフェストのパーティション値の範囲を含みます。
- Manifest Files: Contain data file details, including partition values and column-level statistics
- マニフェストファイル: データファイルの詳細を含み、パーティション値や列レベルの統計を含みます。

This architecture enables crucial separation between how data is physically stored and how it's logically represented. 
このアーキテクチャは、データが物理的にどのように保存されているかと、論理的にどのように表現されているかの重要な分離を可能にします。The query engine handles all partitioning logic using the metadata layer—effectively abstracting it from users.
クエリエンジンは、メタデータレイヤーを使用してすべてのパーティショニングロジックを処理し、ユーザーから効果的に抽象化します。

### Partition Transforms

At the heart of hidden partitioning are partition transforms—functions that convert column values into partition values. 
隠れたパーティショニングの中心には、パーティション変換があり、これは列の値をパーティションの値に変換する関数です。Unlike traditional partitioning where partition columns must be explicitly included in the data, Iceberg applies transforms to existing data columns when writing and reading.
従来のパーティショニングではパーティション列をデータに明示的に含める必要があるのに対し、Icebergは書き込みおよび読み取り時に既存のデータ列に変換を適用します。

Iceberg implements several transform types as captured in this table below:
Icebergは、以下の表に示すいくつかの変換タイプを実装しています。

- Identity transform does no transformation.
- アイデンティティ変換は変換を行いません。
- Bucket transform, Truncate transform & Temporal transform — each use simple functions.
- バケット変換、切り捨て変換、時間変換 — 各々が単純な関数を使用します。

Research by Novotny et al. concludes that transform-based partitioning can reduce query execution time by up to 60% compared to traditional approaches when properly aligned with query patterns.
Novotnyらの研究によると、変換ベースのパーティショニングは、クエリパターンに適切に整合させた場合、従来のアプローチと比較してクエリ実行時間を最大60%削減できることがわかりました。

### Multi-Level Filtering Algorithm

Iceberg uses a multi-level filtering algorithm that progressively narrows down the set of files to read.
Icebergは、読み取るファイルのセットを段階的に絞り込む多層フィルタリングアルゴリズムを使用しています。

#### Manifest List Filtering

The first filtering stage uses partition value ranges stored in the manifest list.
最初のフィルタリング段階では、マニフェストリストに保存されたパーティション値の範囲を使用します。This stage provides an O(1) filtering operation compared to the O(n) operation of listing all files in a traditional data lake, where n grows with table size.
この段階では、従来のデータレイクでのすべてのファイルをリストするO(n)操作と比較して、O(1)のフィルタリング操作を提供します。ここで、nはテーブルサイズに応じて増加します。

#### Manifest-Level Filtering

The second stage applies exact partition value matching.
第2段階では、正確なパーティション値の一致を適用します。

#### Data File Selection

The final stage uses file-level statistics for further filtering.
最終段階では、さらなるフィルタリングのためにファイルレベルの統計を使用します。In a performance study by Wang et al., this multi-level filtering approach reduced data scan volume by up to 95% compared to traditional partitioning schemes for certain query patterns.
Wangらによるパフォーマンス研究では、この多層フィルタリングアプローチが特定のクエリパターンに対して従来のパーティショニングスキームと比較してデータスキャン量を最大95%削減したことが示されています。

### Partition Evolution Design

A key advantage of hidden partitioning is the ability to evolve partition schemes without rewriting data—something impossible with traditional partitioning where partition columns are embedded in directory structures.
隠れたパーティショニングの重要な利点は、データを再書き込みすることなくパーティションスキームを進化させる能力です。これは、パーティション列がディレクトリ構造に埋め込まれている従来のパーティショニングでは不可能です。Netflix has been able to migrate partition schemes for multi-petabyte tables without any downtime or significant performance impact using partition evolution.
Netflixは、パーティション進化を使用して、マルチペタバイトテーブルのパーティションスキームをダウンタイムや重大なパフォーマンスへの影響なしに移行することができました。

#### Version-Based Partition Specs

Iceberg assigns a unique ID to each partition specification and tracks which spec was used for each data file.
Icebergは、各パーティション仕様に一意のIDを割り当て、各データファイルにどの仕様が使用されたかを追跡します。

#### Handling Multiple Active Partition Schemes

The query planning process accounts for multiple partition schemes.
クエリ計画プロセスは、複数のパーティションスキームを考慮します。

### Optimizations

Iceberg uses caching like any other data storage offering. 
Icebergは、他のデータストレージと同様にキャッシングを使用します。In addition, it also does metadata size optimizations to achieve maximum efficiency in this additional layer that it introduces.
さらに、Icebergは、導入したこの追加レイヤーで最大の効率を達成するためにメタデータサイズの最適化も行います。Some optimizations include:
いくつかの最適化には以下が含まれます。

1. Manifest lists store partition value ranges in compressed form.
2. マニフェストリストは、圧縮形式でパーティション値の範囲を保存します。
3. Manifests are grouped by partition to minimize the number of files.
4. マニフェストは、ファイル数を最小限に抑えるためにパーティションごとにグループ化されます。
5. Column statistics use appropriate precision to balance size and effectiveness.
6. 列統計は、サイズと効果のバランスを取るために適切な精度を使用します。

By moving partition management to the metadata layer, Iceberg delivers significant advantages in certain query patterns and becomes an apt solution for systems seeking simpler but more dynamic big data solutions.
パーティション管理をメタデータレイヤーに移動することで、Icebergは特定のクエリパターンにおいて重要な利点を提供し、よりシンプルでダイナミックなビッグデータソリューションを求めるシステムに適したソリューションとなります。

Are you using Apache Iceberg for your product? Share your experiences in the comments.
あなたは製品にApache Icebergを使用していますか？コメントであなたの経験を共有してください。And if you enjoyed this take on hidden partitioning, consider subscribing to Stackgazer for more thoughtful analysis at the intersection of technology, philosophy, and human experience.
そして、隠れたパーティショニングに関するこの考察を楽しんだなら、技術、哲学、人間の経験の交差点におけるより深い分析のためにStackgazerを購読することを検討してください。

Subscribe
https://docs.oracle.com/en/database/oracle/oracle-database/21/vldbg/partition-pruning.html
C. Curino, Y. Zhang, E. P. C. Jones, and S. Madden, “Schism: a workload-driven approach to database replication and partitioning,” Proceedings of the VLDB Endowment, Vol. 3, No. 1-2, pp. 48-57, 2010.
C. Curino, Y. Zhang, E. P. C. Jones, and S. Madden, “Schism: a workload-driven approach to database replication and partitioning,”
, Vol. 3, No. 1-2, pp. 48-57, 2010.
Apache Iceberg - A Table Format for Huge Analytic Datasets
Y. Cheng, F. Rusu, "Scan Planning in Iceberg Tables," 2022 IEEE 38th International Conference on Data Engineering (ICDE), 2022.
Y. Cheng, F. Rusu, "Scan Planning in Iceberg Tables,"
, 2022.
X. Wang, T. Rabl, et al., "Analyzing and Comparing Open Source Data Lake Table Formats," CIDR 2023, Conference on Innovative Data Systems Research, 2023.
X. Wang, T. Rabl, et al., "Analyzing and Comparing Open Source Data Lake Table Formats,"
, 2023.
J. Russell, R. Blue, "Evolution of Partition Management for Netflix Data Platform," Data+AI Summit 2022, 2022.
J. Russell, R. Blue, "Evolution of Partition Management for Netflix Data Platform,"
, 2022.
#### Subscribe to Stackgazer
購読する
#### Discussion about this post
この投稿についての議論
### Ready for more?
もっと知りたいですか？
Subscribe
購読する
© 2026 Dixyantar Panda
·
∙
Substack
·
∙
∙
Datadog Analytics
End Datadog Analytics
Cloudflare Web Analytics
End Cloudflare Web Analytics
Fallback tracking pixels
