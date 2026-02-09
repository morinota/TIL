refs: https://aws.amazon.com/jp/blogs/big-data/how-ancestry-optimizes-a-100-billion-row-iceberg-table/?utm_source=chatgpt.com

# How Ancestry optimizes a 100-billion-row Iceberg table Ancestryが1000億行のIcebergテーブルを最適化する方法

by Thomas Cardenas, Robert Fisher, and Harsh Vardhan Singh Gaur
著者：トーマス・カルデナス、ロバート・フィッシャー、ハーシュ・ヴァルダン・シン・ガウル
on 27 AUG 2025
2025年8月27日

Ancestry, the global leader in family history and consumer genomics, uses family trees, historical records, and DNA to help people on their journeys of personal discovery.
Ancestryは、家族の歴史と消費者ゲノミクスのグローバルリーダーであり、家系図、歴史的記録、DNAを使用して、人々の個人的な発見の旅を支援しています。

Ancestry has the largest collection of family history records, consisting of 40 billion records.
Ancestryは、400億の記録からなる家族歴史記録の最大のコレクションを持っています。

They serve more than 3 million subscribers and have over 23 million people in their growing DNA network.
彼らは300万人以上の加入者にサービスを提供し、成長するDNAネットワークには2300万人以上の人々がいます。

Their customers can use this data to discover their family story.
顧客はこのデータを使用して、自分の家族の物語を発見することができます。

Ancestry is proud to connect users with their families past and present.
Ancestryは、ユーザーを過去と現在の家族とつなげることを誇りに思っています。

They help people learn more about their own identity by learning about their ancestors.
彼らは、人々が先祖について学ぶことで、自分自身のアイデンティティについてより多くを学ぶ手助けをしています。

Users build a family tree through which we surface relevant records, historical documents, photos, and stories that might contain details about their ancestors.
ユーザーは家系図を構築し、それを通じて先祖に関する詳細を含む可能性のある関連記録、歴史的文書、写真、物語を提示します。

These artifacts are surfaced through Hints.
これらのアーティファクトは、Hintsを通じて提示されます。

The Hints dataset is one of the most interesting datasets at Ancestry.
Hintsデータセットは、Ancestryで最も興味深いデータセットの一つです。

It’s used to alert users that potential new information is available.
これは、ユーザーに新しい情報が利用可能であることを通知するために使用されます。

The dataset has multiple shards, and there are currently 100 billion rows being used by machine learning models and analysts.
データセットは複数のシャードを持ち、現在、機械学習モデルやアナリストによって1000億行が使用されています。

Not only is the dataset large, it also changes rapidly.
データセットは大きいだけでなく、急速に変化します。

In this post, we share the best practices that Ancestry used to implement an Apache Iceberg-based hints table capable of handling 100 billion rows with 7 million hourly changes.
この投稿では、Ancestryが1000億行と700万件の時間ごとの変更を処理できるApache Icebergベースのヒントテーブルを実装するために使用したベストプラクティスを共有します。

The optimizations covered here resulted in cost reductions of 75%.
ここで取り上げる最適化により、75%のコスト削減が実現しました。



## Overview of solution ソリューションの概要

Ancestry’s Enterprise Data Management (EDM) team faced a critical challenge—how to provide a unified, performant data ecosystem that could serve diverse analytical workloads across financial, marketing, and product analytics teams. 
Ancestryのエンタープライズデータ管理（EDM）チームは、財務、マーケティング、製品分析チームの多様な分析ワークロードに対応できる統一された高性能データエコシステムを提供するという重要な課題に直面しました。

The ecosystem needed to support everything from data scientists training recommendation models to geneticists developing population studies—all requiring access to the same Hints data. 
このエコシステムは、推薦モデルを訓練するデータサイエンティストから、集団研究を行う遺伝学者まで、すべてをサポートする必要があり、すべてが同じHintsデータへのアクセスを必要としました。

The ecosystem around Hints data had been developed organically, without a well-defined architecture. 
Hintsデータに関するエコシステムは、有効に定義されたアーキテクチャなしに有機的に開発されてきました。

Teams independently accessed Hints data through direct service calls, Kafka topic subscriptions, or warehouse queries, creating significant data duplication and unnecessary system load. 
チームは、直接サービスコール、Kafkaトピックのサブスクリプション、またはデータウェアハウスのクエリを通じて独立してHintsデータにアクセスし、重大なデータの重複と不必要なシステム負荷を生み出しました。

To reduce cost and improve performance, EDM implemented a centralized Apache Iceberg data lake on Amazon Simple Storage Service (Amazon S3), with Amazon EMR providing the processing power. 
コストを削減し、パフォーマンスを向上させるために、EDMはAmazon Simple Storage Service（Amazon S3）上に中央集権的なApache Icebergデータレイクを実装し、Amazon EMRが処理能力を提供しました。

This architecture, shown in the following image, creates a single source of truth for the Hints dataset while using Iceberg’s ACID transactions, schema evolution, and partition evolution capabilities to handle scale and update frequency. 
このアーキテクチャは、以下の画像に示されているように、Hintsデータセットの単一の真実のソースを作成し、IcebergのACIDトランザクション、スキーマ進化、およびパーティション進化機能を使用してスケールと更新頻度を処理します。

Hints table management architecture
Hintsテーブル管理アーキテクチャ

Managing datasets exceeding one billion rows presents unique challenges, and Ancestry faced this challenge with the trees collection of 20–100 billion rows across multiple tables. 
10億行を超えるデータセットの管理は独自の課題を提示し、Ancestryは複数のテーブルにわたる20〜100億行のツリーコレクションでこの課題に直面しました。

At this scale, dataset updates require careful execution to control costs and prevent memory issues. 
この規模では、データセットの更新にはコストを制御し、メモリの問題を防ぐために慎重な実行が必要です。

To solve these challenges, EDM chose Amazon EMR on Amazon EC2 running Spark to write Iceberg tables on Amazon S3 for storage. 
これらの課題を解決するために、EDMはAmazon EC2上でSparkを実行するAmazon EMRを選択し、IcebergテーブルをAmazon S3に書き込んでストレージを確保しました。

With large and steady Amazon EMR workloads, running the clusters on Amazon EC2, as opposed to Serverless, proved cost effective. 
大規模で安定したAmazon EMRワークロードを持つ中、サーバーレスではなくAmazon EC2上でクラスターを実行することがコスト効果的であることが証明されました。

EDM has scheduled an Apache Spark job to run every hour on their Amazon EMR on EC2. 
EDMは、EC2上のAmazon EMRで毎時実行されるApache Sparkジョブをスケジュールしました。

This job uses the merge operation to update the Iceberg table with recently changed rows. 
このジョブは、マージ操作を使用して最近変更された行でIcebergテーブルを更新します。

Performing updates like this on such a large dataset can easily lead to runaway costs and out-of-memory errors. 
このような大規模データセットでの更新を行うと、簡単にコストの急増やメモリエラーを引き起こす可能性があります。



## Key optimization techniques 主要な最適化技術

The engineers needed to enable fast, row-level updates without impacting query performance or incurring substantial cost. 
エンジニアは、クエリパフォーマンスに影響を与えず、 substantial cost（大きなコスト）をかけずに、迅速な行レベルの更新を可能にする必要がありました。 
To achieve this, Ancestry used a combination of partitioning strategies, table configurations, Iceberg procedures, and incremental updates. 
これを実現するために、Ancestryはパーティショニング戦略、テーブル構成、Iceberg手順、およびインクリメンタル更新の組み合わせを使用しました。 
The following is covered in detail: 
以下の内容が詳細に説明されています：
- Partitioning 
- パーティショニング
- Sorting 
- ソート
- Merge-on-read 
- マージオンリード
- Compaction 
- コンパクション
- Snapshot management 
- スナップショット管理
- Storage-partitioned joins 
- ストレージパーティション結合

### Partitioning strategy パーティショニング戦略

Developing an effective partitioning strategy was crucial for the 100-billion-row Hints table. 
効果的なパーティショニング戦略の開発は、1000億行のHintsテーブルにとって重要でした。 
Iceberg supports various partition transforms including column value, temporal functions (year, month, day, hour), and numerical transforms (bucket, truncate). 
Icebergは、列値、時間関数（年、月、日、時間）、および数値変換（バケット、切り捨て）を含むさまざまなパーティション変換をサポートしています。 
Following AWS best practices, Ancestry carefully analyzed query patterns to identify a partitioning approach that would support these queries while balancing these two competing considerations: 
AWSのベストプラクティスに従い、Ancestryはクエリパターンを慎重に分析し、これらのクエリをサポートしながら、次の2つの競合する考慮事項のバランスを取るパーティショニングアプローチを特定しました：
- Too few partitions would force queries to scan excessive data, degrading performance and increasing costs. 
- パーティションが少なすぎると、クエリは過剰なデータをスキャンすることになり、パフォーマンスが低下し、コストが増加します。
- Too many partitions would create small files and excessive metadata, causing management overhead and slower query planning. 
- パーティションが多すぎると、小さなファイルと過剰なメタデータが生成され、管理オーバーヘッドが発生し、クエリ計画が遅くなります。 
It’s generally best to avoid parquet files smaller than 100 MB. 
一般的に、100 MB未満のparquetファイルは避けるのが最善です。 
Through query pattern analysis, Ancestry discovered that most analytical queries filtered on hintstatus (particularly pendingstatus) and hinttype. 
クエリパターン分析を通じて、Ancestryはほとんどの分析クエリがhintstatus（特にpendingstatus）とhinttypeでフィルタリングされていることを発見しました。 
This insight led us to implement a two-level partitioning strategy - first on status and then on type, which dramatically reduced the amount of data scanned during typical queries. 
この洞察により、私たちは2層のパーティショニング戦略を実装しました - まずstatusで、次にtypeで、これにより通常のクエリ中にスキャンされるデータ量が劇的に減少しました。

### Sorting ソート

To further optimize query performance, Ancestry implemented strategic data organization within partitions using Iceberg’s sort orders. 
クエリパフォーマンスをさらに最適化するために、AncestryはIcebergのソート順を使用してパーティション内のデータの戦略的な組織を実装しました。 
While Iceberg doesn’t maintain perfect ordering, even approximate sorting significantly improves data locality and compression ratios. 
Icebergは完全な順序を維持しませんが、近似的なソートでもデータのローカリティと圧縮比を大幅に改善します。 
For the Hints table with 100 billion rows, Ancestry faced a unique challenge: the primary identifiers (PersonId and HintId) are high-cardinality numeric columns that would be prohibitively expensive to sort completely. 
1000億行のHintsテーブルに対して、Ancestryは独自の課題に直面しました：主要な識別子（PersonIdとHintId）は高カーディナリティの数値列であり、完全にソートするには非常に高コストです。 
The solution uses Iceberg’s truncate transform function to support sorting on just a portion of the number, effectively creating another partition by grouping a collection of IDs together. 
この解決策は、Icebergのtruncate変換関数を使用して、数値の一部だけをソートすることをサポートし、IDのコレクションをグループ化することで別のパーティションを効果的に作成します。 
For example, we can specify truncate(100_000_000, hintId) to create groups of 100 million hint IDs, greatly improving the performance of queries that specify that column. 
例えば、truncate(100_000_000, hintId)を指定することで、1億のhint IDのグループを作成し、その列を指定するクエリのパフォーマンスを大幅に向上させることができます。

### Merge on read マージオンリード

With 7 million changes to the Hints table occurring hourly, optimizing write performance became critical to the architecture. 
Hintsテーブルに毎時700万件の変更が発生する中、書き込みパフォーマンスの最適化はアーキテクチャにとって重要になりました。 
In addition to making sure queries performed well, Ancestry also needed to make sure our frequent updates would perform well in both time and cost. 
クエリがうまく機能することを確認するだけでなく、Ancestryは頻繁な更新が時間とコストの両方でうまく機能することを確認する必要がありました。 
It was quickly discovered that the default copy-on-write (CoW) strategy, which copies an entire file when any part of it changes, was too slow and expensive for their use case. 
デフォルトのコピーオンライト（CoW）戦略は、ファイルの一部が変更されるとファイル全体をコピーするため、彼らのユースケースには遅すぎて高コストであることがすぐに発見されました。 
Ancestry was able to get the performance we needed by instead specifying the merge-on-read (MoR) update strategy, which maintains new information in diff files that are reconciled on read. 
Ancestryは、代わりにマージオンリード（MoR）更新戦略を指定することで、必要なパフォーマンスを得ることができました。この戦略は、新しい情報を読み取り時に調整されるdiffファイルに保持します。 
The large updates that happen every hour led us to choose faster updates at the cost of slower reads. 
毎時発生する大規模な更新により、私たちは遅い読み取りのコストでより高速な更新を選択することになりました。

### File compaction ファイルコンパクション

The frequent updates mean files are constantly needing to be re-written to maintain performance. 
頻繁な更新は、パフォーマンスを維持するためにファイルを常に再書き込みする必要があることを意味します。 
Iceberg provides the rewrite_data_files procedure for compaction, but default configurations proved insufficient for our scale. 
Icebergはコンパクションのためにrewrite_data_files手順を提供しますが、デフォルトの構成は私たちのスケールには不十分でした。 
Leaving the default configuration in place, the rewrite operation wrote to five partitions at a time and didn’t meet our performance objective. 
デフォルトの構成をそのままにしておくと、再書き込み操作は一度に5つのパーティションに書き込み、私たちのパフォーマンス目標を満たしませんでした。 
We found that increasing the concurrent writes improved performance. 
同時書き込みを増やすことでパフォーマンスが向上することがわかりました。 
We used the following set of parameters, setting a relatively high max-concurrent-file-group-rewrites value of 100 to more efficiently deal with our thousands of partitions. 
次のパラメータセットを使用し、比較的高いmax-concurrent-file-group-rewrites値を100に設定して、数千のパーティションをより効率的に処理しました。 
The default of rewriting only one file at a time couldn’t keep up with the frequency of our updates. 
一度に1つのファイルのみを再書き込みするデフォルトでは、私たちの更新の頻度に追いつくことができませんでした。

```
CALL datalake.system.rewrite_data_files(
table => ‘database.table’,
strategy => ‘binpack’,
options => map (
'max-concurrent-file-group-rewrites','100',
'partial-progress.enabled','true',
'rewrite-all','true'
)
)
```

Code コード
Key optimizations in Ancestry’s approach include: 
Ancestryのアプローチにおける主要な最適化には以下が含まれます：
- High concurrency: We increased max-concurrent-file-group-rewrites from the default 5 to 100, enabling parallel processing of our thousands of partitions. 
- 高い同時実行性：デフォルトの5からmax-concurrent-file-group-rewritesを100に増やし、数千のパーティションの並列処理を可能にしました。 
This increased compute costs but was necessary to help ensure that the jobs finished. 
これにより計算コストは増加しましたが、ジョブが完了することを確実にするために必要でした。 
- Resilience at scale: We enabled partial-progress to create compaction checkpoints, essential when operating at our scale where failures are particularly costly. 
- スケールでのレジリエンス：partial-progressを有効にしてコンパクションチェックポイントを作成しました。これは、失敗が特に高コストである私たちのスケールで運用する際に不可欠です。 
- Comprehensive delta elimination: Setting rewrite-all to true helps ensure that both data files and delete files are compacted, preventing the accumulation of delete files. 
- 包括的なデルタ排除：rewrite-allをtrueに設定することで、データファイルと削除ファイルの両方がコンパクト化され、削除ファイルの蓄積を防ぎます。 
By default, the delete files created as part of this strategy aren’t re-written and would continue to accumulate, slowing queries. 
デフォルトでは、この戦略の一部として作成された削除ファイルは再書き込みされず、蓄積し続け、クエリを遅くします。 
We arrived at these optimizations through successive trials and evaluations. 
これらの最適化には、連続的な試行と評価を通じて到達しました。 
For example, with our very large dataset, we discovered that we could use a WHERE clause to limit re-writes to a single partition. 
例えば、非常に大きなデータセットを使用している場合、WHERE句を使用して再書き込みを単一のパーティションに制限できることがわかりました。 
Based on the partitions, we see varied execution times and resource utilization. 
パーティションに基づいて、さまざまな実行時間とリソース利用状況が見られます。 
For some partitions, we needed to reduce concurrency to avoid running into out of memory errors. 
一部のパーティションでは、メモリエラーを回避するために同時実行性を減らす必要がありました。

### Snapshot management スナップショット管理

Iceberg tables maintain snapshots to preserve the history of the table, allowing you to time travel through the changes. 
Icebergテーブルはスナップショットを維持してテーブルの履歴を保存し、変更を通じてタイムトラベルを可能にします。 
As these snapshots accrue, they add to storage costs and degrade performance. 
これらのスナップショットが蓄積されると、ストレージコストが増加し、パフォーマンスが低下します。 
This is why maintaining an Iceberg table requires you to periodically call the expire_snapshots procedure. 
これが、Icebergテーブルを維持するために定期的にexpire_snapshots手順を呼び出す必要がある理由です。 
We found we needed to enable concurrency for snapshot management so that it would complete in a timely manner: 
スナップショット管理のために同時実行性を有効にする必要があることがわかりました。そうすることで、タイムリーに完了します：

```
CALL datalake.system.expire_snapshots(
table => '`database`.table',
retain_last => 1,
max_concurrent_deletes => 20)
```

Code コード
Consider how to balance performance, cost, and the need to keep historical records depending on your use case. 
使用ケースに応じて、パフォーマンス、コスト、および履歴記録を保持する必要性のバランスを考慮してください。 
When you do so, note that there is a table-level setting for maximum snapshot age which can override the retain_last parameter and retain only the active snapshot. 
その際、最大スナップショット年齢のテーブルレベル設定があり、retain_lastパラメータを上書きしてアクティブなスナップショットのみを保持できることに注意してください。

### Reducing shuffle with Storage-Partitioned Joins ストレージパーティション結合によるシャッフルの削減

We use Storage-Partitioned Joins (SPJ) in Iceberg tables to minimize expensive shuffles during data processing. 
Icebergテーブルでは、データ処理中の高コストなシャッフルを最小限に抑えるためにストレージパーティション結合（SPJ）を使用します。 
SPJ is an advanced Iceberg feature (available in Spark 3.3 or later with Iceberg 1.2 or later) that uses the physical storage layout of tables to eliminate shuffle operations entirely. 
SPJは、テーブルの物理ストレージレイアウトを使用してシャッフル操作を完全に排除する高度なIceberg機能（Iceberg 1.2以降のSpark 3.3以降で利用可能）です。 
For our Hints update pipeline, this optimization was transformational. 
私たちのHints更新パイプラインにとって、この最適化は変革的でした。 
SPJ is especially useful during MERGE INTO operations, where datasets have identical partitioning. 
SPJは、データセットが同一のパーティショニングを持つMERGE INTO操作中に特に便利です。 
Proper configuration helps ensure effective use of SPJ to optimize joins. 
適切な構成は、結合を最適化するためにSPJを効果的に使用するのに役立ちます。 
SPJ has a few requirements such as both tables must be Iceberg partitioned the same way and joined on the partition key. 
SPJにはいくつかの要件があり、両方のテーブルは同じ方法でIcebergパーティションされ、パーティションキーで結合される必要があります。 
Then Iceberg will know that it doesn’t have to shuffle the data when the tables are loaded. 
そうすれば、Icebergはテーブルがロードされるときにデータをシャッフルする必要がないことを知ります。 
This even works when there are a different number of partitions on either side. 
これは、片側に異なる数のパーティションがある場合でも機能します。 
Updates to the Hints database are first staged in the Hint Changes database where data is transformed from the original Kafka data format into how it will look in the target (Hints) table. 
Hintsデータベースへの更新は、最初にHint Changesデータベースでステージされ、データは元のKafkaデータ形式からターゲット（Hints）テーブルでの見え方に変換されます。 
This is a temporary Iceberg table where we are able to perform audits using Write-Audit-Publish (WAP) pattern. 
これは一時的なIcebergテーブルで、Write-Audit-Publish（WAP）パターンを使用して監査を実行できます。 
In addition to using the WAP pattern we are able to use the SPJ functionality. 
WAPパターンを使用することに加えて、SPJ機能を使用することもできます。 
The Hints data pipeline 
Hintsデータパイプライン

### Reducing full-table scans フルテーブルスキャンの削減

Another strategy to reduce shuffle is minimizing the data involved in joins by dynamically pushing down filters. 
シャッフルを減らすための別の戦略は、フィルタを動的にプッシュダウンすることによって結合に関与するデータを最小限に抑えることです。 
In production, these filters vary between batches, so a multi-step operation is often necessary for setting up merges. 
本番環境では、これらのフィルタはバッチ間で異なるため、マージを設定するために多段階の操作が必要になることがよくあります。 
The following example code first limits its scope by setting minimum and maximum values for the ID, then performs an update or delete to the target table depending on whether a target value exists. 
以下の例コードは、最初にIDの最小値と最大値を設定してスコープを制限し、次にターゲット値が存在するかどうかに応じてターゲットテーブルに更新または削除を実行します。

```
val stats: Dataset[Row] = session.read.table("catalog.database.source").agg(min(col("id")).as("min_value"), max(col("id")).as("max_value"))
val statRow: Row = stats.head
val minId: String = statRow.getInt(0)
val maxId: String = statRow.getInt(1)
session.sql(s"""
MERGE INTO catalog.database.target t
USING (SELECT * FROM catalog.database.source) s
ON (t.id BETWEEN $minId AND $maxId)
AND (t.id = s.id)
WHEN MATCHED
THEN UPDATE SET *
WHEN NOT MATCHED
THEN INSERT *
""")
```

[
Row
]
=
session
.
read
.
table
(
"catalog.database.source"
)
.
(
min
(
(
"id"
)
)
.
as
(
"min_value"
)
,
max
(
(
"id"
)
)
.
as
(
"max_value"
)
)
Row
=
.
=
.
(
0
)
=
.
(
1
)
session
.
sql
(
"""
MERGE INTO catalog.database.target t
USING (SELECT * FROM catalog.database.source) s
ON (t.id BETWEEN $minId AND $maxId)
AND (t.id = s.id)
WHEN MATCHED
THEN UPDATE SET *
WHEN NOT MATCHED
THEN INSERT *
"""
)
SQL
This technique reduces cost in several ways: the bounded merge reduces the number of affected rows, it allows for predicate pushdown optimization, which filters at the storage layer, and it reduces shuffle operations when compared with a join. 
この技術は、いくつかの方法でコストを削減します：バウンデッドマージは影響を受ける行数を減らし、ストレージ層でフィルタリングする述語プッシュダウン最適化を可能にし、結合と比較してシャッフル操作を減少させます。

### Additional insights 追加の洞察

Apart from the Hints table, we have implemented over 1,000 Iceberg tables in our data ecosystem. 
Hintsテーブル以外にも、私たちはデータエコシステムに1,000以上のIcebergテーブルを実装しました。 
The following are some key insights that we observed: 
以下は、私たちが観察したいくつかの重要な洞察です：
- Updating a table using MERGE is typically the most expensive action, so this is where we spent the most time optimizing. 
- MERGEを使用してテーブルを更新することは通常最も高コストなアクションであるため、ここに最も多くの時間をかけて最適化しました。 
- It was still our best option. 
- それでも私たちの最良の選択肢でした。 
- Using complex data types can help co-locate similar data in the table. 
- 複雑なデータ型を使用することで、テーブル内の類似データを共同配置するのに役立ちます。 
- Monitor costs of each pipeline because while following good practice you can stumble across things you miss that are causing costs to increase. 
- 各パイプラインのコストを監視してください。良いプラクティスに従っているときに、コストを増加させる原因となる見落としがあることに気づくことがあります。



## Conclusion 結論

Organizations can use Apache Iceberg tables on Amazon S3 with Amazon EMR to manage massive datasets with frequent updates. 
組織は、Amazon S3上のApache IcebergテーブルをAmazon EMRと共に使用して、頻繁に更新される大規模データセットを管理できます。

Many customers will be able to achieve excellent performance with a low maintenance burden by using the AWS Glue table optimizer for automatic, asynchronous compaction. 
多くの顧客は、AWS Glueテーブルオプティマイザーを使用して自動的かつ非同期的にコンパクションを行うことで、低いメンテナンス負担で優れたパフォーマンスを達成できるでしょう。

Some customers, like Ancestry, will require custom optimizations of their maintenance procedures to meet their cost and performance goals. 
Ancestryのような一部の顧客は、コストとパフォーマンスの目標を達成するために、メンテナンス手順のカスタム最適化が必要になります。

These customers should start with a careful assessment of query patterns to develop a partitioning strategy to minimize the amount of data that needs to be read and processed. 
これらの顧客は、クエリパターンの慎重な評価から始め、読み取りおよび処理する必要のあるデータ量を最小限に抑えるためのパーティショニング戦略を策定すべきです。

Update frequency and latency requirements will dictate other choices, like whether merge-on-read or copy-on-write is the better strategy. 
更新頻度とレイテンシ要件は、merge-on-readまたはcopy-on-writeのどちらがより良い戦略であるかといった他の選択肢を決定します。

If your organization faces similar challenges with high volumes of data requiring frequent updates, you can use a combination of Apache Iceberg’s advanced features with AWS services like Amazon EMR Serverless, Amazon S3, and AWS Glue to build a truly modern data lake that delivers the scale, performance, and cost-efficiency you need. 
もしあなたの組織が頻繁な更新を必要とする大量のデータに関して同様の課題に直面しているなら、Apache Icebergの高度な機能とAmazon EMR Serverless、Amazon S3、AWS GlueなどのAWSサービスを組み合わせて、必要なスケール、パフォーマンス、コスト効率を提供する真に現代的なデータレイクを構築することができます。



## Further reading さらなる読み物
- How Iceberg works
- Build a high-performance, ACID compliant, evolving data lake using Apache Iceberg on Amazon EMR
### About the authors 著者について
### Thomas Cardenas
Thomas is a Staff Software Engineer at Ancestry. 
トーマスはAncestryのスタッフソフトウェアエンジニアです。
He focuses on building data lake infrastructure and improving data quality for financial reporting and analytics. 
彼はデータレイクインフラストラクチャの構築と、財務報告および分析のためのデータ品質の向上に注力しています。
He loves building the technical foundations that help millions of people discover their family history. 
彼は何百万人もの人々が自分の家族の歴史を発見するのを助ける技術的基盤を構築することが大好きです。

### Robert Fisher
Robert is an AWS Sr. Solutions Architect. 
ロバートはAWSのシニアソリューションアーキテクトです。
He has over twenty years experience designing software solutions and leading software engineering teams. 
彼はソフトウェアソリューションの設計とソフトウェアエンジニアリングチームのリーダーシップに20年以上の経験があります。
He is passionate about helping customers use technology to achieve their business objectives. 
彼は顧客が技術を活用してビジネス目標を達成するのを助けることに情熱を注いでいます。

### Harsh Vardan
Harsh is an AWS Solutions Architect, specializing in big data and analytics. 
ハーシュはAWSのソリューションアーキテクトで、ビッグデータと分析を専門としています。
He has a decade of experience working in the field of data science. 
彼はデータサイエンスの分野で10年の経験があります。
He is passionate about helping customers adopt best practices and discover insights from their data. 
彼は顧客がベストプラクティスを採用し、データから洞察を発見するのを助けることに情熱を注いでいます。

Apache Iceberg
### Resources リソース
- Amazon Athena
- Amazon EMR
- Amazon Kinesis
- Amazon MSK
- Amazon QuickSight
- Amazon Redshift
- AWS Glue
### Follow フォロー
- Twitter
- Facebook
- LinkedIn
- Twitch
- Email Updates
Create an AWS account
AWSアカウントを作成



## Learn 学ぶ

- What Is AWS? 
- AWSとは何ですか？

- What Is Cloud Computing? 
- クラウドコンピューティングとは何ですか？

- What Is Agentic AI? 
- エージェンティックAIとは何ですか？

- Cloud Computing Concepts Hub 
- クラウドコンピューティング概念ハブ

- AWS Cloud Security 
- AWSクラウドセキュリティ

- What's New 
- 新着情報

- Blogs 
- ブログ

- Press Releases 
- プレスリリース



## Resources リソース

- Getting Started 始めに
- Training トレーニング
- AWS Trust Center AWSトラストセンター
- AWS Solutions Library AWSソリューションライブラリ
- Architecture Center アーキテクチャセンター
- Product and Technical FAQs 製品および技術に関するFAQ
- Analyst Reports アナリストレポート
- AWS Partners AWSパートナー



## Developers 開発者

- Builder Center
- SDKs & Tools
- .NET on AWS
- Python on AWS
- Java on AWS
- PHP on AWS
- JavaScript on AWS



## Help ヘルプ
- Contact Us お問い合わせ
- File a Support Ticket サポートチケットを提出
- AWS re:Post AWS re:Post
- Knowledge Center ナレッジセンター
- AWS Support Overview AWSサポートの概要
- Get Expert Help 専門家の支援を受ける
- AWS Accessibility AWSアクセシビリティ
- Legal 法的情報
English 英語
Amazon is an Equal Opportunity Employer: Minority / Women / Disability / Veteran / Gender Identity / Sexual Orientation / Age. 
アマゾンは平等な機会を提供する雇用主です：少数派 / 女性 / 障害者 / 退役軍人 / 性別のアイデンティティ / 性的指向 / 年齢。
x
facebook facebook
linkedin linkedin
instagram instagram
twitch twitch
youtube youtube
podcasts ポッドキャスト
email メール
- Privacy プライバシー
- Site terms サイト利用規約
- Cookie Preferences クッキーの設定
© 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved. 
© 2025年、アマゾンウェブサービス株式会社またはその関連会社。全著作権所有。
