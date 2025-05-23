refs: https://medium.com/pinterest-engineering/how-pinterest-accelerates-ml-feature-iterations-via-effective-backfill-d67ea125519c

# How Pinterest Accelerates ML Feature Iterations via Effective Backfill
# Pinterestが効果的なバックフィルを通じてML機能の反復を加速する方法

Pinterest EngineeringFollow
Pinterest Engineering
Pinterestエンジニアリングをフォロー

Authors: Kartik Kapur, Tech Lead, Sr Software Engineer | Matthew Jin, Sr Software Engineer | Qingxian Lai, Staff Software Engineer
著者: Kartik Kapur, テックリード、シニアソフトウェアエンジニア | Matthew Jin, シニアソフトウェアエンジニア | Qingxian Lai, スタッフソフトウェアエンジニア

# Context 背景

At Pinterest, our mission is to inspire users to curate a life they love. 
Pinterestでは、私たちの使命はユーザーが愛する生活をキュレーションするようにインスパイアすることです。
To achieve this, we rely on state-of-the-art Recommendation and Ads models trained on tens of petabytes of data over the span of many months of engagement logs. 
これを達成するために、私たちは数十ペタバイトのデータを使用して、**数ヶ月にわたるエンゲージメントログで訓練された最先端の推薦および広告モデルに依存**しています。
These models drive personalized recommendations, showing users content that resonates with their interests. 
これらのモデルは、ユーザーの興味に共鳴するコンテンツを表示するパーソナライズされた推薦を推進します。
These models show significantly better performance when trained on large datasets with events spanning over many months of events. 
これらのモデルは、数ヶ月にわたるイベントを含む大規模データセットで訓練されると、著しく良いパフォーマンスを示します。

Our ML Models are trained on a wide range of features, including Pin, user, advertiser-level, and session-based features. 
私たちの機械学習モデルは、**Pin(=アイテム??)、ユーザー、広告主レベル、セッションベースの特徴を含む幅広い特徴量**で訓練されています。
Experimenting with these features is a common task, and the first step in this process is integrating new features into the training dataset. 
これらの特徴量を使った実験は一般的な作業であり、**このプロセスの最初のステップは新しい特徴量を訓練データセットに統合すること**です。
(うんうん、だからbackfillしやすさが重要って話かな...!:thinking:)

The most straightforward method of incorporating features into the training dataset is through Forward Logging: adding the features into our serving logs and waiting for it to accumulate enough data for training. 
特徴を訓練データセットに組み込む最も簡単な方法は、Forward Loggingを通じて行うことです。これは、特徴量をサービングログに追加し、訓練に十分なデータが蓄積されるのを待つことです。
(backfillしないで一番簡単なのは、新しいfeature pipelineをリリースして本番稼働させて、学習データ期間分が溜まるのを待つって意味...!:thinking:)

However, this method presents several challenges: 
しかし、この方法にはいくつかの課題があります。

- High Calendar Day Cost: Every iteration takes 3~6 months to be hydrated in the training dataset. 高いカレンダー日コスト：各イテレーションは、訓練データセットに反映されるまでに3〜6ヶ月かかります。
- High Development Time Cost: Introducing new features in logging touches multiple systems, including training and serving logic. 高い開発時間コスト：ログに新しい特徴量を導入することは、訓練およびサービングロジックを含む複数のシステムに影響を与えます。
- Lack of isolation: Production and experimental features share the logging pipeline. In some cases, adding large experimental features can inadvertently cause data loss incidents. 孤立性の欠如：本番環境と実験的な特徴がログパイプラインを共有します。場合によっては、大きな実験的特徴を追加することで、意図せずデータ損失のインシデントを引き起こすことがあります。(これはシステムの設計次第な気がする...!:thinking:)
- Resource wastage and instability: As experimental features are added directly to the production logs and training datasets, it makes the end-to-end data pipeline expensive. リソースの無駄遣いと不安定性：実験的特徴が本番ログや訓練データセットに直接追加されるため、エンドツーエンドのデータパイプラインが高価になります (まあ確かに、価値を発揮するか分からない特徴量を作るpipelineを、何ヶ月も本番で動かすのは無駄だよね...!:thinking:)

Feature Backfill is an alternative to forward logging that is commonly used to address these challenges. 
**Feature Backfill**は、これらの課題に対処するために一般的に使用されるForward Loggingの代替手段です。
Feature backfill involves counter-factually computing the historical feature values and joining it with production training data using offline batch processing. 
Feature Backfillは、歴史的な特徴値を反実仮想的に計算し、オフラインバッチ処理を使用して本番の訓練データと結合することを含みます。
Feature backfill allows us to greatly cut down calendar day costs, enabling faster iteration and more efficient use of our engineering resources. 
**Feature Backfillは、calendar day costを大幅に削減し、より迅速なイテレーションとエンジニアリングリソースのより効率的な使用を可能にします**。

In this blog post, we’ll explore how we’ve created our Feature Backfill Solution, leveraging various techniques to reduce costs and iteration time by up to 90x¹. 
このブログ記事では、**コストとイテレーション時間を最大90倍削減するため**に、さまざまな技術を活用して私たちのFeature Backfillソリューションをどのように作成したかを探ります。

<!-- ここまで読んだ! -->

# Structure of Recommender / Ads Training Datasets 推奨システム/広告トレーニングデータセットの構造

Below is a simplified representation of the datasets we are dealing with. 
以下は、私たちが扱っているデータセットの簡略化された表現です。
Feature groups are collections of logically and physically related features in a Feature Store, designed to be produced, updated, and stored together. 
**フィーチャーグループは、フィーチャーストア内の論理的および物理的に関連するフィーチャーのコレクションであり、一緒に生成、更新、保存されるように設計されています**(うんうん、 Feature Groupを切り分けるときの考え方として参考になりそう...!:thinking:)。
These groups are keyed by specific entity identifiers, such as advertiser IDs or user IDs. 
これらのグループは、広告主IDやユーザーIDなどの特定のエンティティ識別子によってキー付けされています。
For the remainder of this blog post, we will specify user id as the entity key. 
このブログ記事の残りの部分では、ユーザーIDをエンティティキーとして指定します。

![]()

<!-- ここまで読んだ! -->

# [2022–2024] Features Backfiller v1: Full Backfill per Feature Group

In 2022, we developed our initial backfill solution using Spark to materialize features within our training tables. 
2022年に、私たちはトレーニングテーブル内の特徴を具現化するためにSparkを使用して初期のバックフィルソリューションを開発しました。
This solution operates as a reusable Airflow DAG that is triggered by ML Engineers on Demand. 
このソリューションは、MLエンジニアによってオンデマンドでトリガーされる再利用可能なAirflow DAGとして機能します。
Each Airflow DAG run contains multiple Spark jobs that each run the backfill application on the target training tables. 
各Airflow DAGの実行には、ターゲットトレーニングテーブル上でバックフィルアプリケーションを実行する複数のSparkジョブが含まれています。
The backfill application itself does the following work: 
バックフィルアプリケーション自体は、以下の作業を行います。

1. Extracts feature groups from the Features Store (features are materialized in offline storage optimized for batch read), alongside the training dataset, aligning them by a common partitioning key (e.g. date). 
1. 特徴ストアから特徴グループを抽出し（特徴はバッチ読み取りに最適化されたオフラインストレージに具現化されます）、トレーニングデータセットと共に、共通のパーティショニングキー（例：日付）で整列させます。

2. Joins the feature groups with the training dataset using entity keys (e.g. user id). 
2. エンティティキー（例：ユーザーID）を使用して、特徴グループをトレーニングデータセットと結合します。

3. Overwrites the same partitions in the training dataset with the new output. 
3. 新しい出力でトレーニングデータセット内の同じパーティションを上書きします。

The overall process then looks as follows: 
全体のプロセスは次のようになります。

![]()

The majority of computational effort occurs during the join stage, where both datasets are shuffled and partitioned for each feature group. 
**計算の大部分は、両方のデータセットがシャッフルされ、各特徴グループのためにパーティション分けされる結合ステージで発生**します。

# OnDemand Features

The backfill approach listed above works effectively when the feature is already stored in a feature store. 
**上記のバックフィルアプローチは、特徴がすでにフィーチャーストアに保存されている場合に効果的に機能**します。(なんかpoint-in-time correct joinしてるみたいな話だったな...!:thinking:)
However, if the feature is not yet materialized, engineers face the additional challenge of backfilling their features in the feature store before they can perform the training data backfill. 
しかし、特徴がまだ具現化されていない場合、エンジニアはトレーニングデータのバックフィルを実行する前に、フィーチャーストアで特徴をバックフィルするという追加の課題に直面します。
(あ、なるほど! 前セクションの話は学習データのbackfill的な意味合いなのか...!!:thinking:)
This additional step can add up to three weeks of calendar time. 
この追加のステップは、最大で3週間のカレンダー時間を追加する可能性があります。
(じゃあ結局、新しい特徴量を追加した場合はそれが貯まるまで3週間待つって話。特徴量生成のbackfillはできてないじゃん...!!:thinking:)
(まあ特徴量生成パイプラインをbackfillしたのち、学習パイプラインにて学習データとjoinすればもうそれで良い気がする...!:thinking:)

To remove this bottleneck, we introduced a concept of on demand features. 
このボトルネックを解消するために、私たちはオンデマンドフィーチャーの概念を導入しました。
Users express a feature in terms of a Spark transform and run the computation prior to joining the training table with their features without ever materializing the intermediary output. 
ユーザーは、特徴をSpark変換の形で表現し、中間出力を具現化することなく、トレーニングテーブルと特徴を結合する前に計算を実行します。
With this approach, engineers no longer have to wait for a full backfill to the feature store before proceeding with their iteration. 
このアプローチにより、エンジニアはイテレーションを進める前にフィーチャーストアへの完全なバックフィルを待つ必要がなくなります。

The transformation code that is utilized to backfill the feature becomes a part of the feature definition allowing for seamless integration and no user interface difference when initiating the backfill. 
**特徴をバックフィルするために利用される変換コードは、特徴定義の一部となり**、バックフィルを開始する際にシームレスな統合とユーザーインターフェースの違いがないことを可能にします。
(そういう考え方ね...! たぶん事前計算されてるか否かは関係ない、みたいな思想かな...! この場合はきっと、Feature Storeが特徴量生成の役割を含んでる考え方だ...!:thinking:)

# Key Functionalities 主要機能

To enhance the utility of this backfiller, we made several iterations to address critical aspects. 
このバックフィラーの有用性を高めるために、私たちは重要な側面に対処するためにいくつかの反復を行いました。
Below are some key learnings from the backfiller v1. 
以下は、バックフィラーv1からのいくつかの重要な学びです。

**Time Correctness Alignment Tuning**: Proper alignment between feature group partitions and the training dataset is crucial. 
時間的正確性の整合性調整：特徴グループのパーティションとトレーニングデータセットとの適切な整合性が重要です。
Misalignment can cause feature leakage (future events leaking into current partitions) or feature lagging (irrelevant features entering training data). 
不整合は、特徴漏洩（将来のイベントが現在のパーティションに漏れ出す）や特徴遅延（無関係な特徴がトレーニングデータに入る）を引き起こす可能性があります。
Our backfillers provide various partition alignment strategies, allowing users to choose based on specific use cases. 
私たちのバックフィラーは、さまざまなパーティション整合性戦略を提供しており、ユーザーは特定のユースケースに基づいて選択できます。

**Version Control and Rollback Support**: Because backfilled data overwrites production data, it’s essential to protect the integrity of the training dataset. 
バージョン管理とロールバックサポート：バックフィルされたデータは本番データを上書きするため、トレーニングデータセットの整合性を保護することが不可欠です。
The backfilling process may introduce bugs or misconfigurations, and regenerating production data is often costly and time-consuming. 
バックフィリングプロセスはバグや設定ミスを引き起こす可能性があり、本番データを再生成することはしばしば高コストで時間がかかります。
We implemented partition-level version control and rollback tooling to recover data during incidents. 
私たちは、インシデント時にデータを回復するために、**パーティションレベルのバージョン管理**とロールバックツールを実装しました。(そもそもこれがFeature Storeによる恩恵の一つでは??)

**Standard Feature Statistics**: Verifying backfill data quality is another critical requirement. 
標準特徴統計：バックフィルデータの品質を検証することは、もう一つの重要な要件です。
By computing standard feature statistics based on feature types and generating reports, users can quickly assess feature quality before model training and evaluation. 
特徴タイプに基づいて標準特徴統計を計算し、レポートを生成することで、ユーザーはモデルのトレーニングと評価の前に特徴の品質を迅速に評価できます。

**Workflow Templates**: Backfill is a standard data processing task, yet a common operation. 
ワークフローテンプレート：バックフィルは標準的なデータ処理タスクであり、一般的な操作です。
We’ve built workflow templates to streamline backfill launching, reducing human error during configuration. 
私たちは、バックフィルの開始を効率化するためのワークフローテンプレートを構築し、設定中の人的エラーを減少させました。
Users simply provide feature groups and a backfill data range to trigger new backfill operations. 
ユーザーは、特徴グループとバックフィルデータ範囲を提供するだけで、新しいバックフィル操作をトリガーできます。

**Utilizing S3 Persist**: Backfill jobs are extraordinarily expensive and are very disk intensive due to the large amount of shuffles between multiple tables, as well as large quantities of cached data going to disk and long spark lineages. 
S3 Persistの利用：バックフィルジョブは非常に高価であり、複数のテーブル間の大量のシャッフルや、ディスクに送られる大量のキャッシュデータ、長いスパークの系譜のために非常にディスク集約的です。
To alleviate the issues, we initially tried using native Spark Checkpointing; however, we found this had inefficiencies for tabular data compared to reading and writing Parquet files, namely it became extremely difficult to prevent rate limits and read times ballooned since data was stored in heavily serialized java byte arrays with checkpoint. 
これらの問題を軽減するために、最初はネイティブSpark Checkpointingを使用しようとしましたが、Parquetファイルの読み書きと比較して、表形式データに対して非効率的であることがわかりました。具体的には、レート制限を防ぐことが非常に難しくなり、データがチェックポイント付きの重度にシリアライズされたJavaバイト配列に保存されていたため、読み取り時間が膨れ上がりました。
We then created our own “S3 checkpointing,” which writes the intermediate data to parquet with short retention. 
その後、短期間の保持で中間データをParquetに書き込む独自の「S3チェックポイント」を作成しました。
This helped solve our issues by pruning lineage completely and alleviated disk issues. 
これにより、系譜を完全に剪定し、ディスクの問題を軽減することで、私たちの問題を解決するのに役立ちました。

<!-- ここまで読んだ! -->

# Challenges 課題

While this backfiller provides features more quickly than the number of days being backfilled, several challenges remain:
このバックフィラーは、バックフィルされる日数よりも早く機能を提供しますが、いくつかの課題が残っています。

1. No Concurrent Backfills: Since each backfill writes data in place, multiple backfills cannot occur simultaneously on the same partition. This necessitates organizing a queue to manage the sequence of backfills.
1. 同時バックフィルなし: 各バックフィルがデータをその場で書き込むため、同じパーティションで複数のバックフィルを同時に行うことはできません。これにより、バックフィルの順序を管理するためのキューを整理する必要があります。

2. High Compute Cost: Backfills can be extremely expensive, with costs exceeding $X million in EC2 expenses. This is primarily due to significant data shuffling, upwards of 90 Tib per job, during joins, which imposes heavy demands on network and disk resources, leading to elevated compute costs and job instability.
2. 高い計算コスト: バックフィルは非常に高価であり、EC2の費用が$X百万を超えることがあります。これは主に、ジョイン中に90Tibを超える大規模なデータシャッフルが発生し、ネットワークおよびディスクリソースに重い負担をかけるためであり、計算コストの上昇とジョブの不安定性を引き起こします。

3. Manual Partition Management: The current versioning and rollback system requires manual partition management in the Hive table, precluding the use of Hive’s dynamic insertion functionality. This creates significant overhead during data commits. For instance, hourly partitioning requires 24 insertions per day’s backfill. Since feature sources are often daily-partitioned, these inefficiencies add unnecessary computation. Some datasets contain even more partitions, impairing job performance.
3. 手動パーティション管理: 現在のバージョン管理およびロールバックシステムは、Hiveテーブル内での手動パーティション管理を必要とし、Hiveの動的挿入機能の使用を妨げます。これにより、データコミット中に大きなオーバーヘッドが発生します。たとえば、時間ごとのパーティショニングでは、1日のバックフィルごとに24回の挿入が必要です。機能ソースはしばしば日次パーティション化されているため、これらの非効率性は不必要な計算を追加します。一部のデータセットにはさらに多くのパーティションが含まれており、ジョブのパフォーマンスを損ないます。

While these issues are not unique to feature backfill, the process is particularly vulnerable due to the complexity and volume involved.
これらの問題は機能バックフィルに特有のものではありませんが、プロセスは関与する複雑さとボリュームのために特に脆弱です。
Feature backfilling often deals with large, intricate datasets, such as extensive user sequence features, which are particularly costly and resource-intensive to manage.
機能バックフィリングは、広範なユーザーシーケンス機能などの大規模で複雑なデータセットを扱うことが多く、特に管理にコストがかかり、リソースを消費します。
For instance, four developers each backfilling a feature group into the training dataset over a 120-day range currently face a cumulative 140-day completion time —clearly suboptimal.
たとえば、4人の開発者がそれぞれ120日間にわたってトレーニングデータセットに機能グループをバックフィルしている場合、現在の累積完了時間は140日であり、明らかに最適ではありません。

<!-- ここまで読んだ! -->

# [2024–2025] Features Backfiller v2: Two-Stage Backfill

To address the challenges we encountered with our v1 backfiller, we developed a v2 version, adopting a two-stage backfill approach. 
私たちは、v1バックフィラーで直面した課題に対処するために、v2バージョンを開発し、二段階バックフィルアプローチを採用しました。この新しい方法は、プロセスを2つの主要なステージに簡素化します。

Stage1: Feature Staging  
ステージ1: フィーチャーステージング  
In this first stage, the feature group is joined with the IDs of the main training table. 
この最初のステージでは、フィーチャーグループがメインのトレーニングテーブルのIDと結合されます。  
The resulting data — consisting only of primary keys and features — is output to an intermediate Staging Table.  
結果として得られるデータは、主キーとフィーチャーのみで構成され、インターメディエイトステージングテーブルに出力されます。

Stage2: Feature Promotion  
ステージ2: フィーチャープロモーション  
In this stage, multiple intermediate staging tables are collectively joined into the main training table in a batch process.  
このステージでは、複数のインターメディエイトステージングテーブルがバッチ処理でメインのトレーニングテーブルにまとめて結合されます。  

Visually, Stage 1 looks as follows:  
視覚的に、ステージ1は以下のようになります:  
After multiple stage 1 backfills complete, we perform stage 2:  
複数のステージ1バックフィルが完了した後、ステージ2を実行します:  

This two-stage approach has advantages in addressing the challenges faced previously:  
この二段階アプローチには、以前直面した課題に対処するための利点があります:  
1. Stage 1 is designed for parallel execution.  
   ステージ1は並列実行のために設計されています。  
   Multiple backfills for the same dataset can occur simultaneously without blocking each other, leading to enhanced collaboration and reduced wait times.  
   同じデータセットの複数のバックフィルが同時に発生し、お互いをブロックすることなく、コラボレーションが向上し、待機時間が短縮されます。  
2. Compared to the full backfill, the stage 1 operations are much more lightweight because they join only a subset of ID columns rather than the entire dataset.  
   フルバックフィルと比較して、ステージ1の操作は、全データセットではなくID列のサブセットのみを結合するため、はるかに軽量です。  
   This minimizes data shuffling, reducing computational costs and time.  
   これによりデータのシャッフルが最小限に抑えられ、計算コストと時間が削減されます。  
3. Since Stage 2 operations are only done after many Stage 1s have completed, the cost of performing adding any single set of features goes down by a factor equal to the number of tables being promoted.  
   ステージ2の操作は多くのステージ1が完了した後にのみ行われるため、単一のフィーチャーセットを追加するコストは、昇格されるテーブルの数に等しい因子で減少します。  
4. By separating the intermediate table from the main production table, we mitigate the risk of inadvertently affecting production data.  
   中間テーブルをメインのプロダクションテーブルから分離することで、プロダクションデータに意図せず影響を与えるリスクを軽減します。  
   Feature statistics can be easily computed on this intermediate staging table, and only verified features proceed to the production dataset during Stage 2.  
   フィーチャー統計はこのインターメディエイトステージングテーブルで簡単に計算でき、検証されたフィーチャーのみがステージ2でプロダクションデータセットに進みます。  

For the same example where engineers took 140 days to backfill their features, the new 2 step backfill approach took a total of 26 days — an overall 82% improvement.  
エンジニアがフィーチャーをバックフィルするのに140日かかった同じ例では、新しい2ステップバックフィルアプローチは合計26日かかり、全体で82%の改善が見られました。  



# Optimization: Enhanced Two-Stage Backfill with Iceberg Table Format 最適化：Icebergテーブルフォーマットを用いた強化された二段階バックフィル

Another architectural change in the Backfiller v2 is switching the data warehouse engine from Hive to Iceberg. 
Backfiller v2のもう一つのアーキテクチャの変更は、データウェアハウスエンジンをHiveからIcebergに切り替えることです。 

This shift brought several key benefits: 
この変更により、いくつかの重要な利点がもたらされました：

1. Iceberg enables dynamic partition insertion functionalities, allowing us to commit multiple partitions within the span of a single data epoch. 
1. Icebergは動的パーティション挿入機能を可能にし、単一のデータエポック内で複数のパーティションをコミットできるようにします。 

This significantly reduces the manual overhead of inserting into individual partitions, diminishing costs and resolving the major bottleneck during write. 
これにより、個々のパーティションへの挿入にかかる手動の負担が大幅に軽減され、コストが削減され、書き込み時の主要なボトルネックが解消されます。 

Previously, per-partition insertion would take 12 hours; dynamic partition insertion reduces this to just one hour — an impressive 12x improvement. 
以前は、パーティションごとの挿入に12時間かかっていましたが、動的パーティション挿入によりこれがわずか1時間に短縮され、驚異的な12倍の改善が達成されました。 

2. We enhanced our version control and rollback support by leveraging Iceberg’s flexible snapshot management system. 
2. Icebergの柔軟なスナップショット管理システムを活用することで、バージョン管理とロールバックサポートを強化しました。 

We implement this rollback support by cherrypicking data partitions from previous snapshots to overwrite the current snapshot. 
このロールバックサポートは、以前のスナップショットからデータパーティションを選択して現在のスナップショットを上書きすることで実装しています。 

Since these operations are primarily metadata-only operations, they can be performed swiftly and efficiently, ensuring quick recovery and minimal downtime. 
これらの操作は主にメタデータのみの操作であるため、迅速かつ効率的に実行でき、迅速な回復と最小限のダウンタイムを確保します。 

3. The Iceberg format offers great support for table partitioning schemas, enabling the development of a bucketing partitioning strategy. 
3. Icebergフォーマットはテーブルパーティショニングスキーマに対して優れたサポートを提供し、バケッティングパーティショニング戦略の開発を可能にします。 

This allows for efficient storage-partitioned joins, which significantly reduce shuffling during both Stage 1 and Stage 2 operations. 
これにより、効率的なストレージパーティション結合が可能になり、ステージ1およびステージ2の操作中のシャッフルが大幅に削減されます。 

Our observations indicate up to a 3x speed increase for backfills. 
私たちの観察によれば、バックフィルの速度が最大3倍向上することが示されています。 

4. By leveraging bucketing and local bucket sorting, data compression potential is unlocked. 
4. バケッティングとローカルバケットソートを活用することで、データ圧縮の可能性が引き出されます。 

Tables’ sizes are compressed to as little as 25% of their original size, achieved through sorting and bucketing by UserId. 
テーブルのサイズは、UserIdによるソートとバケッティングを通じて、元のサイズのわずか25%に圧縮されます。 

This organization allows grouping of user-sequence features adjacent to each other, facilitating effective Delta Encoding for these sequences. 
この構成により、ユーザーシーケンス特徴が隣接してグループ化され、これらのシーケンスに対する効果的なデルタエンコーディングが促進されます。 

The Stage 1 process utilizing Iceberg looks as follows (Inputs contains multiple partitions and leverage dynamic partition insertion to overwrite the corresponding output): 
Icebergを利用したステージ1のプロセスは以下のようになります（入力には複数のパーティションが含まれ、動的パーティション挿入を活用して対応する出力を上書きします）： 

The Stage 2 Feature Promotion Process then visually looks as follows (Used storage partition join to replace the full shuffle join): 
次に、ステージ2の特徴プロモーションプロセスは以下のように視覚的に表現されます（ストレージパーティション結合を使用してフルシャッフル結合を置き換えます）： 

Furthermore, to streamline the initiation of new backfills, the team has developed a dedicated backfiller UI, making the process straightforward and user-friendly. 
さらに、新しいバックフィルの開始を効率化するために、チームは専用のバックフィラーUIを開発し、プロセスを簡素化し、ユーザーフレンドリーにしました。



# [2025+] Training Time “Backfill” via Ray Bucket Join

How can we further enhance the backfiller experience? 
バックフィラーの体験をさらに向上させるにはどうすればよいでしょうか？

While we’ve already achieved considerable efficiency gains with the two-stage backfill approach and by leveraging Iceberg, the Stage 2 process still requires users to materialize the full training dataset before model training which can take multiple days for a large training window. 
私たちはすでに二段階のバックフィルアプローチとIcebergを活用することでかなりの効率向上を達成していますが、ステージ2のプロセスでは、モデルのトレーニングの前にユーザーが完全なトレーニングデータセットを具現化する必要があり、大きなトレーニングウィンドウの場合、数日かかることがあります。

Imagine if we could entirely bypass Stage 2 and proceed to train models directly using the intermediate staging tables produced in Stage 1. 
もしステージ2を完全にバイパスし、ステージ1で生成された中間ステージングテーブルを使用して直接モデルをトレーニングできるとしたらどうでしょうか。

Achieving this would require a data loader capable of joining the training data with these staging tables on the fly. 
これを実現するには、トレーニングデータとこれらのステージングテーブルを即座に結合できるデータローダーが必要です。

This led us to build the next generation training time backfill with Ray. 
これにより、私たちはRayを使用して次世代のトレーニング時間バックフィルを構築することになりました。

Ray is an open-source framework that excels in building distributed applications. 
Rayは、分散アプリケーションの構築に優れたオープンソースのフレームワークです。

It provides the flexibility to manage heterogeneous types of instances and distribute the workload in a resource-aware manner. 
異種のインスタンスを管理し、リソースを意識した方法で作業負荷を分散する柔軟性を提供します。

Since 2023, Pinterest has been utilizing Ray to build our training platform (more details in our previous blogs posts: Last Mile Data Processing⁵, Ray Infrastructure at Pinterest⁶, Ray Batch Inference at Pinterest⁷) and leverage Ray’s data component aids in optimizing data loading speeds, enabling us to horizontally scale CPU resources for data loading workers and unlock various training-time data processing capabilities, such as joining staging tables with the training dataset. 
2023年以降、PinterestはRayを利用してトレーニングプラットフォームを構築しており（詳細は以前のブログ投稿をご覧ください：Last Mile Data Processing⁵、Ray Infrastructure at Pinterest⁶、Ray Batch Inference at Pinterest⁷）、Rayのデータコンポーネントを活用してデータロード速度を最適化し、データローディングワーカーのCPUリソースを水平にスケールし、トレーニングデータセットとステージングテーブルを結合するなど、さまざまなトレーニング時間データ処理機能を解放しています。

However, Ray’s data processing emphasizes a streaming execution paradigm, which is not well-suited for the typical data shuffling required by hash join workloads. 
しかし、Rayのデータ処理はストリーミング実行パラダイムを強調しており、ハッシュジョインワークロードに必要な典型的なデータシャッフルには適していません。

This limitation was one of the motivations for adopting Iceberg in Backfiller v2 and implement bucketing partitioning on the training dataset. 
この制限は、Backfiller v2でIcebergを採用し、トレーニングデータセットにバケットパーティショニングを実装する動機の一つでした。

Bucketing partitioning allows the data to be partitioned by on a hash modulo operation on specified columns (e.g. request_id): 
バケットパーティショニングにより、データを指定された列（例：request_id）に対するハッシュモジュロ操作でパーティション分けできます：

$$
bucket(request_id, 16) → hash(request_id) \% 16
$$

With standardized bucketing across staging tables and training tables, we can effectively implement a map side bucket join inside Ray data loader workers. 
ステージングテーブルとトレーニングテーブル全体で標準化されたバケットを使用することで、Rayデータローダーワーカー内でマップサイドバケットジョインを効果的に実装できます。

The idea is simple: during training, data loader workers analyze the data distribution, bucketing information from both the training dataset and the staging table. 
アイデアはシンプルです：トレーニング中、データローダーワーカーはトレーニングデータセットとステージングテーブルの両方からデータ分布とバケット情報を分析します。

Assuming both tables have the same bucketing schema, the data loader worker then selectively loads files from corresponding buckets across multiple tables, dynamically joining them into a single data block. 
両方のテーブルが同じバケットスキーマを持っていると仮定すると、データローダーワーカーは対応するバケットから複数のテーブルのファイルを選択的にロードし、それらを動的に単一のデータブロックに結合します。

This block is then sent to the trainer for processing or training. 
このブロックは、その後、処理またはトレーニングのためにトレーナーに送信されます。

Although this method demands additional computational resources, Ray allows us to scale up CPU resources effectively, ensuring that training speed remains consistent and unaffected. 
この方法は追加の計算リソースを必要としますが、RayはCPUリソースを効果的にスケールアップできるため、トレーニング速度が一貫して維持され、影響を受けないことを保証します。

While adopting Ray and Iceberg offers substantial benefits, it’s important to acknowledge the technical complexities involved, which can be more challenging than they initially appear. 
RayとIcebergを採用することは大きな利点を提供しますが、関与する技術的な複雑さを認識することも重要であり、これは最初に見えるよりも難しい場合があります。

For example, implementing bucketing and sorting can alter dataset distributions, and migrating the entire existing training stack to a new platform is a significant undertaking that could warrant an entire chapter in itself. 
たとえば、バケット化とソートを実装するとデータセットの分布が変わる可能性があり、既存のトレーニングスタック全体を新しいプラットフォームに移行することは、独自の章を必要とする重要な作業です。

Our teams are actively addressing these challenges. 
私たちのチームはこれらの課題に積極的に取り組んでいます。

Stay tuned for future blog posts as we unveil more about this journey. 
この旅についての詳細を明らかにする今後のブログ投稿にご期待ください。

With the inclusion of in-trainer join functionality, we can streamline and speed up our feature testing process significantly. 
トレーナー内結合機能の追加により、私たちは機能テストプロセスを大幅に合理化し、加速することができます。

New feature experiments begin with a quick Stage 1 backfill using a dedicated UI. 
新しい機能の実験は、専用のUIを使用した迅速なステージ1バックフィルから始まります。

Once these features are verified, they can be directly used for model training in offline evaluations. 
これらの機能が確認されると、オフライン評価でのモデルトレーニングに直接使用できます。

If the features meet the evaluation criteria, users can proceed with the Stage 2 operation to promote them to the production dataset and initiate online experiments. 
機能が評価基準を満たす場合、ユーザーはステージ2の操作を進めてそれらを本番データセットに昇格させ、オンライン実験を開始できます。



# Summary 概要

Our multi-year journey in enhancing Pinterest’s feature backfilling experience reflects a commitment to innovation and efficiency, transitioning from forward logging to a refined two-stage backfill process. 
Pinterestの機能バックフィリング体験を向上させるための私たちの数年にわたる旅は、革新と効率へのコミットメントを反映しており、フォワードロギングから洗練された二段階バックフィルプロセスへと移行しました。

Feature Backfiller v1 used Spark for full backfills, significantly reducing calendar day costs and accelerating feature iteration, though it also highlighted the need for further optimization. 
Feature Backfiller v1は、完全なバックフィルにSparkを使用し、カレンダー日コストを大幅に削減し、機能の反復を加速しましたが、さらなる最適化の必要性も浮き彫りにしました。

This led to Feature Backfiller v2, featuring a two-stage process that optimized parallel execution and minimized data shuffling, supported by the Iceberg table format for enhanced partition management and version control. 
これにより、Feature Backfiller v2が生まれ、並列実行を最適化し、データのシャッフルを最小限に抑える二段階プロセスが特徴となり、パーティション管理とバージョン管理を強化するためにIcebergテーブルフォーマットがサポートされました。

These advancements resulted in a 90 times speed up in completion times and improved data compression by up to 75%. 
これらの進展により、完了時間が90倍速くなり、データ圧縮が最大75%改善されました。

As we look ahead, our training-time “backfill” approach with Ray aims to further streamline processes by enabling on-the-fly data joins during model training, ensuring that our recommendation systems continue to deliver inspiring, personalized experiences efficiently. 
今後を見据え、Rayを用いたトレーニング時間の「バックフィル」アプローチは、モデルのトレーニング中にオンザフライのデータ結合を可能にすることでプロセスをさらに効率化し、私たちの推薦システムが引き続き刺激的でパーソナライズされた体験を効率的に提供できるようにすることを目指しています。



# Acknowledgements 謝辞

This project represents a collaborative effort across many teams at Pinterest. 
このプロジェクトは、Pinterestの多くのチームによる共同作業を表しています。
We wish to acknowledge and thank them for their significant contributions to this workstream. 
私たちは、彼らのこの作業の流れへの重要な貢献に感謝の意を表したいと思います。

- ML Platform: Rubin Ferguson, Yi He, Matthew Almeida, Andrew Yu
- Ads ML Infrastructure: Chao Huang, Harshal Dahake, Xinyi Zhang, Haoyu He
- Core ML Infrastructure: Laksh Bhasin, Jiahuan Liu, Henry Feng, Alekhya Pyla, Dave Chen
- Big Data Platform: Ashish Singh, Pucheng Yang
- Analytics Platform: Surya Karri
- Leadership support: Se Won Jang, Joey Wang, Shun-ping Chiu, Colin Leatherbury, Archer Liu, Shu Zhang, David Liu



# References 参考文献

¹Pinterest Internal Data March 25, 2024
¹Pinterest内部データ 2024年3月25日

²Apache Software Foundation. “pyspark.sql.DataFrame.checkpoint.” Apache Spark Documentation, Version 3.5.0, 2024, https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.checkpoint.html
²Apache Software Foundation. 「pyspark.sql.DataFrame.checkpoint.」Apache Sparkドキュメント、バージョン3.5.0、2024年、https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.checkpoint.html

³Pinterest Engineering. “Large-Scale User Sequences at Pinterest.” Medium, 6 Sept. 2023, https://medium.com/pinterest-engineering/large-scale-user-sequences-at-pinterest-78a5075a3fe9
³Pinterestエンジニアリング. 「Pinterestにおける大規模ユーザーシーケンス。」Medium、2023年9月6日、https://medium.com/pinterest-engineering/large-scale-user-sequences-at-pinterest-78a5075a3fe9

⁴Apache Parquet. “Delta Encoding (DELTA_BINARY_PACKED).” Parquet Documentation, 2024, https://parquet.apache.org/docs/file-format/data-pages/encodings/#delta-encoding-delta_binary_packed
⁴Apache Parquet. 「デルタエンコーディング (DELTA_BINARY_PACKED).」Parquetドキュメント、2024年、https://parquet.apache.org/docs/file-format/data-pages/encodings/#delta-encoding-delta_binary_packed

⁵Pinterest Engineering. “Last-mile Data Processing with Ray.” Medium, 13 Oct. 2023, https://medium.com/pinterest-engineering/last-mile-data-processing-with-ray-629affbf34ff.
⁵Pinterestエンジニアリング. 「Rayを用いたラストマイルデータ処理。」Medium、2023年10月13日、https://medium.com/pinterest-engineering/last-mile-data-processing-with-ray-629affbf34ff.

⁶Pinterest Engineering. “Ray infrastructure at Pinterest.” Medium, 19 Oct. 2023, https://medium.com/pinterest-engineering/ray-infrastructure-at-pinterest-0248efe4fd52.
⁶Pinterestエンジニアリング. 「PinterestにおけるRayインフラストラクチャ。」Medium、2023年10月19日、https://medium.com/pinterest-engineering/ray-infrastructure-at-pinterest-0248efe4fd52.

⁷Pinterest Engineering. “Ray Batch Inference at Pinterest (Part 3).” Medium, 14 Mar. 2024, https://medium.com/pinterest-engineering/ray-batch-inference-at-pinterest-part-3-4faeb652e385.
⁷Pinterestエンジニアリング. 「PinterestにおけるRayバッチ推論 (パート3).」Medium、2024年3月14日、https://medium.com/pinterest-engineering/ray-batch-inference-at-pinterest-part-3-4faeb652e385.



## Sign up to discover human stories that deepen your understanding of the world. 
世界の理解を深める人間の物語を発見するためにサインアップしてください。



## Free 無料

Distraction-free reading. No ads.  
気を散らさない読書。広告なし。

Organize your knowledge with lists and highlights.  
リストやハイライトで知識を整理しましょう。

Tell your story. Find your audience.  
あなたの物語を語りましょう。聴衆を見つけましょう。

Sign up for free  
無料でサインアップ



## Membership メンバーシップ

Read member-only stories
メンバー限定のストーリーを読む

Support writers you read most
最もよく読む作家をサポートする

Earn money for your writing
自分の執筆でお金を稼ぐ

Listen to audio narrations
オーディオナレーションを聞く

Read offline with the Medium app
Mediumアプリでオフラインで読む

Try for $5/month
月額$5でお試し



## Published in Pinterest Engineering Blog Pinterest Engineering Blogに掲載

Published in Pinterest Engineering Blog
Pinterest Engineering Blogに掲載

15.9K followers
15.9K フォロワー

·
·

Inventive engineers building the first visual discovery engine, 300 billion ideas and counting.
発明的なエンジニアが初のビジュアルディスカバリーエンジンを構築中、3000億のアイデアが進行中。

Follow
フォロー



## Written by Pinterest Engineering 著者: Pinterestエンジニアリング

Written by Pinterest Engineering
Pinterestエンジニアリングによって書かれました。

59K followers
59Kフォロワー

·
·

https://medium.com/pinterest-engineering| Inventive engineers building the first visual discovery engine
https://medium.com/pinterest-engineering | 最初のビジュアルディスカバリーエンジンを構築する創造的なエンジニア

https://careers.pinterest.com/
https://careers.pinterest.com/
Follow
フォロー



## No responses yet まだ応答はありません

Write a response 応答を書く
What are your thoughts? あなたの考えは何ですか？
What are your thoughts? あなたの考えは何ですか？



## More from Pinterest Engineering and Pinterest Engineering Blog Pinterest Engineering Blogからのさらなる情報

In
Pinterest Engineering Blog
Pinterest Engineeringによる



## How we built Text-to-SQL at Pinterest  
### Adam Obeng | Data Scientist, Data Platform Science; J.C. Zhong | Tech Lead, Analytics Platform; Charlie Gu | Sr. Manager, Engineering
PinterestにおけるText-to-SQLの構築方法  
### Adam Obeng | データサイエンティスト、データプラットフォームサイエンス; J.C. Zhong | テックリード、アナリティクスプラットフォーム; Charlie Gu | シニアマネージャー、エンジニアリング
Apr 3, 2024A clap icon2.6KA response icon23  
2024年4月3日　拍手アイコン2.6K　応答アイコン23
Apr 3, 2024  
2024年4月3日
2.6K  
2.6K
23  
23
In  
Pinterest Engineering Blog  
Pinterest Engineering Blogにて
by  
Pinterest Engineering  
Pinterest Engineeringによる



## Multi-gate-Mixture-of-Experts (MMoE) model architecture and knowledge distillation in Ads…  
### Authors: Jiacheng Li | Machine Learning Engineer II, Ads Ranking; Matt Meng | Staff Machine Learning Engineer, Ads Ranking; Kungang Li |…

Multi-gate-Mixture-of-Experts (MMoE)モデルアーキテクチャと広告における知識蒸留…
### 著者: Jiacheng Li | 機械学習エンジニア II, 広告ランキング; Matt Meng | スタッフ機械学習エンジニア, 広告ランキング; Kungang Li |…

Apr 25A clap icon111  
4月25日　拍手アイコン111

Apr 25  
4月25日

In  
に

Pinterest Engineering Blog  
Pinterestエンジニアリングブログ

by  
によって

Pinterest Engineering  
Pinterestエンジニアリング



## Migrating 3.7 Million Lines of Flow Code to TypeScript  
### Authors: Jack Hsu | Staff Software Engineer, Core Web Platform; Mark Molinaro | Staff Software Engineer, Code and Language Runtime
3.7百万行のFlowコードをTypeScriptに移行する  
### 著者: Jack Hsu | スタッフソフトウェアエンジニア、コアウェブプラットフォーム; Mark Molinaro | スタッフソフトウェアエンジニア、コードおよび言語ランタイム

Apr 17A clap icon638A response icon4  
4月17日　拍手アイコン638　応答アイコン4

In  
Pinterest Engineering Blog  
にて  
Pinterest Engineering  



## Improving Pinterest Search Relevance Using Large Language Models  
Pinterestの検索関連性を大規模言語モデルを使用して改善する

### Han Wang | Machine Learning Engineer, Relevance & Query Understanding; Mukuntha Narayanan | Machine Learning Engineer, Relevance & Query…  
ハン・ワン | 機械学習エンジニア、関連性とクエリ理解; ムクンタ・ナラヤナン | 機械学習エンジニア、関連性とクエリ…

Apr 5A clap icon208A response icon1  
4月5日　拍手アイコン208　応答アイコン1
Apr 5  
4月5日
208  
208
1  
1



## Recommended from Medium おすすめのMediumから

In
Coding Beauty
by
Tari Ibaba
において



## This new IDE from Google is an absolute game changer この新しいIDEはGoogleからの絶対的なゲームチェンジャーです  
### This new IDE from Google is seriously revolutionary. この新しいIDEはGoogleからの本当に革命的です。
Mar 12 3月12日
A clap icon5.6K 拍手アイコン5.6K
A response icon335 反応アイコン335
Mar 12 3月12日
5.6K 5.6K
335 335
In 在
Level Up Coding Level Up Coding
by 著者
Rahul Sharma ラフル・シャルマ



## SQL Is Dead, NoSQL Is Dying, and NewSQL Is Quietly Taking Over  
SQLは死に、NoSQLは衰退し、NewSQLが静かに台頭している

### You are developing the backend infrastructure of an extensive financial system. 
あなたは、大規模な金融システムのバックエンドインフラを開発しています。

The system operates as either a hedge fund, payment…
そのシステムは、ヘッジファンドまたは支払いシステムとして機能します…



## Why Our CTO Banned Rust After One Rewrite なぜ私たちのCTOは一度の書き換えの後にRustを禁止したのか

At our company, Rust was a dream. Fast, safe, modern. We were excited. 
私たちの会社では、Rustは夢のような存在でした。速く、安全で、現代的でした。私たちは興奮していました。

We’d read the blogs. Watched the conference talks. Saw the memes…
私たちはブログを読み、カンファレンスの講演を見て、ミームを見ました…



## 500X Scalability of Experiment Metric Computing with Unified Dynamic Framework  
### Xinyue Cao | Software Engineer Tech Lead; Bojun Lin | Software Engineer
500Xスケーラビリティの実験メトリック計算のための統一動的フレームワーク  
### Xinyue Cao | ソフトウェアエンジニア テックリード; Bojun Lin | ソフトウェアエンジニア

May 14A clap icon41  
5月14日 A clap icon41

May 14  
5月14日

41  
41

The Latency Gambler  
レイテンシーギャンブラー



## Scaling to 1 Million Users: The Architecture I Wish I Knew Sooner 100万人のユーザーへのスケーリング：もっと早く知っておきたかったアーキテクチャ  
### When we launched, we were happy just having 100 daily users. 立ち上げたとき、私たちは100人のデイリーユーザーがいるだけで満足していました。 
But within months, we hit 10,000, then 100,000. しかし数ヶ月以内に、私たちは10,000人、次に100,000人に達しました。 
And scaling problems piled up… そして、スケーリングの問題が積み重なっていきました…  
May 10A clap icon1.2KA response icon32 5月10日　拍手アイコン1.2K　応答アイコン32  
May 10 5月10日  
1.2K 1.2K  
32 32  
Nathan Rosidi ナサン・ロシディ  



## Matplotlib Alternatives That Actually Save You Time Matplotlibの代替手段で実際に時間を節約する方法

### If you find Matplotlib leaving a lot to be desired, you’re not the only one. 
### Matplotlibに不満を感じているのはあなただけではありません。

While it’s not a bad library, you might find these five… 
悪いライブラリではありませんが、これらの5つの代替手段を見つけるかもしれません…
