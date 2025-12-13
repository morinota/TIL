refs: https://netflixtechblog.com/incremental-processing-using-netflix-maestro-and-apache-iceberg-b8ba072ddeeb

# Incremental Processing using Netflix Maestro and Apache Iceberg Netflix MaestroとApache Icebergを用いたインクリメンタル処理

byJun He,Yingyi Zhang, andPawan Dixit
著者: Jun He, Yingyi Zhang, Pawan Dixit

Incremental processing is an approach to process new or changed data in workflows. 
**インクリメンタル処理は、ワークフローにおいて新しいデータや変更されたデータを処理するアプローチ**です。
The key advantage is that it only incrementally processes data that are newly added or updated to a dataset, instead of re-processing the complete dataset. 
**主な利点は、完全なデータセットを再処理するのではなく、新たに追加または更新されたデータのみをインクリメンタルに処理すること**です。
This not only reduces the cost of compute resources but also reduces the execution time in a significant manner. 
これにより、計算リソースのコストが削減されるだけでなく、実行時間も大幅に短縮されます。
When workflow execution has a shorter duration, chances of failure and manual intervention reduce. 
ワークフローの実行時間が短くなると、失敗や手動介入の可能性が減少します。
It also improves the engineering productivity by simplifying the existing pipelines and unlocking the new patterns. 
また、既存のパイプラインを簡素化し、新しいパターンを解放することで、エンジニアリングの生産性も向上します。

<!-- ここまで読んだ! -->

In this blog post, we talk about the landscape and the challenges in workflows at Netflix. 
このブログ記事では、Netflixにおけるワークフローの状況と課題について説明します。
We will show how we are building a clean and efficient incremental processing solution (IPS) by using Netflix Maestro and Apache Iceberg. 
私たちが**Netflix MaestroとApache Icebergを使用して、クリーンで効率的なインクリメンタル処理ソリューション（Incremental Processing Solution、IPS）を構築している方法**を紹介します。(Maestroは、たぶんワークフローオーケストレーションプラットフォームのこと...!:thinking:)
IPS provides the incremental processing support with data accuracy, data freshness, and backfill for users and addresses many of the challenges in workflows. 
IPSは、データの正確性、データの新鮮さ、ユーザーのためのバックフィルを伴うインクリメンタル処理のサポートを提供し、ワークフローにおける多くの課題に対処します。
IPS enables users to continue to use the data processing patterns with minimal changes. 
IPSは、ユーザーが最小限の変更でデータ処理パターンを引き続き使用できるようにします。

<!-- ここまで読んだ! -->

## Introduction はじめに

Netflix relies on data to power its business in all phases. 
Netflixは、すべてのフェーズでビジネスを支えるためにデータに依存しています。
Whether in analyzing A/B tests, optimizing studio production, training algorithms, investing in content acquisition, detecting security breaches, or optimizing payments, well structured and accurate data is foundational. 
A/Bテストの分析、スタジオ制作の最適化、アルゴリズムのトレーニング、コンテンツ取得への投資、セキュリティ侵害の検出、または支払いの最適化において、構造化され正確なデータは基盤となります。
As our business scales globally, the demand for data is growing and the needs for scalable low latency incremental processing begin to emerge. 
**私たちのビジネスがグローバルに拡大するにつれて、データの需要が高まり、スケーラブルで低遅延のインクリメンタル処理のニーズが現れ始めています。**
There are three common issues that the dataset owners usually face. 
データセットの所有者が通常直面する**3つの一般的な問題**があります。

- **Data Freshness**: Large datasets from Iceberg tables needed to be processed quickly and accurately to generate insights to enable faster product decisions. 
- データの新鮮さ：Icebergテーブルからの大規模データセットは、迅速かつ正確に処理され、迅速な製品決定を可能にする洞察を生成する必要があります。
The hourly processing semantics along with valid–through-timestamp watermark or data signals provided by the Data Platform toolset today satisfies many use cases, but is not the best for low-latency batch processing. 
現在のData Platformツールセットが提供する有効なタイムスタンプのウォーターマークやデータ信号とともに、時間単位の処理セマンティクスは多くのユースケースを満たしますが、低遅延バッチ処理には最適ではありません。
Before IPS, the Data Platform did not have a solution for tracking the state and progression of data sets as a single easy to use offering. 
IPS以前は、Data Platformにはデータセットの状態と進行状況を追跡するための単一の使いやすいソリューションがありませんでした。
This has led to a few internal solutions such as Psyberg. 
これにより、Psybergなどのいくつかの内部ソリューションが生まれました。
These internal libraries process data by capturing the changed partitions, which works only on specific use cases. 
これらの内部ライブラリは、変更されたパーティションをキャプチャすることによってデータを処理しますが、特定のユースケースでのみ機能します。
Additionally, the libraries have tight coupling to the user business logic, which often incurs higher migration costs, maintenance costs, and requires heavy coordination with the Data Platform team. 
さらに、これらのライブラリはユーザビジネスロジックに密接に結合しており、しばしば高い移行コストやメンテナンスコストが発生し、Data Platformチームとの重い調整が必要です。

- **Data Accuracy**: Late arriving data causes datasets processed in the past to become incomplete and as a result inaccurate. 
- データの正確性：遅れて到着するデータは、過去に処理されたデータセットを不完全にし、その結果不正確になります。
To compensate for that, ETL workflows often use a lookback window, based on which they reprocess the data in that certain time window. 
これを補うために、ETLワークフローはしばしばルックバックウィンドウを使用し、そのウィンドウ内のデータを再処理します。
For example, a job would reprocess aggregates for the past 3 days because it assumes that there would be late arriving data, but data prior to 3 days isn’t worth the cost of reprocessing. 
例えば、ジョブは過去3日間の集計を再処理します。なぜなら、遅れて到着するデータがあると仮定するからですが、3日前のデータは再処理のコストに見合わないのです。

- Backfill: Backfilling datasets is a common operation in big data processing. 
- **バックフィル**：データセットのバックフィルは、ビッグデータ処理における一般的な操作です。
This requires repopulating data for a historical time period which is before the scheduled processing. 
これは、スケジュールされた処理の前の歴史的な期間のデータを再補充することを必要とします。
The need for backfilling could be due to a variety of factors, e.g. 
**バックフィルの必要性は、さまざまな要因**による可能性があります。例えば、
(1) upstream data sets got repopulated due to changes in business logic of its data pipeline, 
(1) 上流データセットがデータパイプラインのビジネスロジックの変更により再補充された、
(2) business logic was changed in a data pipeline, 
(2) データパイプライン内のビジネスロジックが変更された、
(3) a new metric was created that needs to be populated for historical time ranges, 
(3) 歴史的な時間範囲に対して補充する必要がある新しいメトリックが作成された、
(4) historical data was found missing, etc. 
(4) 歴史的データが欠落していることが判明した、などです。

(うんうん。全部あるね〜:thinking:)

These challenges are currently addressed in suboptimal and less cost efficient ways by individual local teams to fulfill the needs, such as 
これらの課題は、現在、個々のローカルチームによって最適でない、コスト効率の低い方法で対処されています。例えば、

- Lookback: This is a generic and simple approach that data engineers use to solve the data accuracy problem. 
- **ルックバック**：これは、データエンジニアがデータの正確性の問題を解決するために使用する一般的でシンプルなアプローチです。
Users configure the workflow to read the data in a window (e.g. past 3 hours or 10 days). 
ユーザは、ワークフローを構成してウィンドウ内のデータを読み取ります（例：過去3時間または10日）。
The window is set based on users’ domain knowledge so that users have a high confidence that the late arriving data will be included or will not matter (i.e. data arrives too late to be useful). 
ウィンドウは、ユーザのドメイン知識に基づいて設定され、遅れて到着するデータが含まれるか、重要でない（つまり、データが役に立つには遅すぎる）という高い信頼を持つことができます。
It ensures the correctness with a high cost in terms of time and compute resources. 
これは、時間と計算リソースの観点で高いコストをかけて正確性を保証します。

- Foreach pattern: Users build backfill workflows using Maestro foreach support. 
- **Foreachパターン**：ユーザーは、Maestroのforeachサポートを使用してバックフィルワークフローを構築します。
It works well to backfill data produced by a single workflow. 
これは、単一のワークフローによって生成されたデータのバックフィルにうまく機能します。
If the pipeline has multiple stages or many downstream workflows, users have to manually create backfill workflows for each of them and that requires significant manual work. 
パイプラインに複数のステージや多くの下流ワークフローがある場合、ユーザーはそれぞれのバックフィルワークフローを手動で作成する必要があり、それにはかなりの手作業が必要です。

<!-- ここまで読んだ! -->

The incremental processing solution (IPS) described here has been designed to address the above problems. 
ここで説明するインクリメンタル処理ソリューション（IPS）は、上記の問題に対処するために設計されています。
The design goal is to provide a clean and easy to adopt solution for the Incremental processing to ensure data freshness, data accuracy, and to provide easy backfill support. 
設計目標は、データの新鮮さ、データの正確性を確保し、**簡単なバックフィルサポート**を提供するためのインクリメンタル処理のクリーンで採用しやすいソリューションを提供することです。

- Data Freshness: provide the support for scheduling workflows in a micro batch fashion (e.g. 15 min interval) with state tracking functionality 
  - データの新鮮さ：状態追跡機能を備えた**マイクロバッチ方式（例：15分間隔）**でワークフローのスケジューリングをサポートします。
- Data Accuracy: provide the support to process all late arriving data to achieve data accuracy needed by the business with significantly improved performance in terms of multifold time and cost efficiency 
  - データの正確性：ビジネスに必要なデータの正確性を達成するために、すべての遅れて到着するデータを処理するサポートを提供し、**時間とコスト効率の面で大幅に改善されたパフォーマンスを実現**します。
- Backfill: provide managed backfill support to build, monitor, and validate the backfill, including automatically propagating changes from upstream to downstream workflows, to greatly improve engineering productivity (i.e. a few days or weeks of engineering work to build backfill workflows vs one click for managed backfill) 
  - バックフィル：バックフィルを構築、監視、検証するための管理されたバックフィルサポートを提供し、上流から下流のワークフローへの変更を自動的に伝播させることで、エンジニアリングの生産性を大幅に向上させます（すなわち、バックフィルワークフローを構築するための数日または数週間のエンジニアリング作業に対して、管理されたバックフィルのための1クリック）。

<!-- ここまで読んだ! -->

## Approach Overview アプローチの概要

### General Concept 一般的な概念

Incremental processing is an approach to process data in batch — but only on new or changed data. 
インクリメンタル処理は、データをバッチで処理するアプローチですが、**新しいデータや変更されたデータのみに適用**されます。 
To support incremental processing, we need an approach for not only capturing incremental data changes but also tracking their states (i.e. whether a change is processed by a workflow or not). 
インクリメンタル処理をサポートするためには、インクリメンタルデータの変更をキャプチャするだけでなく、それらの状態（すなわち、変更がワークフローによって処理されたかどうか）を追跡するアプローチが必要です。 
It must be aware of the change and can capture the changes from the source table(s) and then keep tracking those changes. 
それは変更を認識し、ソーステーブルからの変更をキャプチャし、その変更を追跡し続けることができなければなりません。 
Here, changes mean more than just new data itself. 
ここで、変更は単に新しいデータそのもの以上の意味を持ちます。 
For example, a row in an aggregation target table needs all the rows from the source table associated with the aggregation row. 
**例えば、集約ターゲットテーブルの行は、集約行に関連するソーステーブルのすべての行を必要とします。** (ex. ターゲット = 新しいユーザとすると、集約時に関連するソース = そのユーザの視聴履歴とか? :thinking:)
Also, if there are multiple source tables, usually the union of the changed data ranges from all input tables gives the full change data set. 
また、複数のソーステーブルがある場合、通常、すべての入力テーブルからの変更データ範囲の和集合が完全な変更データセットを提供します。 
Thus, change information captured must include all related data including those unchanged rows in the source table as well. 
したがって、キャプチャされた変更情報には、ソーステーブルの変更されていない行を含むすべての関連データが含まれている必要があります。 
Due to previously mentioned complexities, change tracking cannot be simply achieved by using a single watermark. 
前述の複雑さのため、変更追跡は単一のウォーターマークを使用するだけでは簡単には達成できません。 
IPS has to track those captured changes in finer granularity. 
IPSは、キャプチャされた変更をより細かい粒度で追跡する必要があります。 

<!-- ここまで読んだ! -->

The changes from the source tables might affect the transformed result in the target table in various ways. 
ソーステーブルからの変更は、ターゲットテーブルの変換結果にさまざまな方法で影響を与える可能性があります。 

- If one row in the target table is derived from one row in the source table, newly captured data change will be the complete input dataset for the workflow pipeline. 
- **ターゲットテーブルの1行がソーステーブルの1行から派生している場合**、新たにキャプチャされたデータの変更はワークフローパイプラインの完全な入力データセットとなります。 

- If one row in the target table is derived from multiple rows in the source table, capturing new data will only tell us the rows have to be re-processed. 
- **ターゲットテーブルの1行がソーステーブルの複数の行から派生している場合**、新しいデータをキャプチャすることは、再処理が必要な行を示すだけです。 
But the dataset needed for ETL is beyond the change data itself. 
しかし、ETLに必要なデータセットは変更データそのものを超えています。 
For example, an aggregation based on account id requires all rows from the source table about an account id. 
例えば、アカウントIDに基づく集約は、そのアカウントIDに関するソーステーブルのすべての行を必要とします。 
The change dataset will tell us which account ids are changed and then the user business logic needs to load all data associated with those account ids found in the change data. 
変更データセットは、どのアカウントIDが変更されたかを示し、その後、ユーザーのビジネスロジックは変更データに見つかったそれらのアカウントIDに関連するすべてのデータをロードする必要があります。 

- If one row in the target table is derived based on the data beyond the changed data set, e.g. joining source table with other tables, newly captured data is still useful and can indicate a range of data to be affected. 
- ターゲットテーブルの1行が変更データセットを超えたデータに基づいて派生している場合（例えば、ソーステーブルを他のテーブルと結合する場合）、新たにキャプチャされたデータは依然として有用であり、影響を受けるデータの範囲を示すことができます。 
Then the workflow will re-process the data based on the range. 
その後、ワークフローはその範囲に基づいてデータを再処理します。 
For example, assuming we have a table that keeps the accumulated view time for a given account partitioned by the day. 
例えば、特定のアカウントの累積視聴時間を日ごとに保持するテーブルがあると仮定します。 
If the view time 3-days ago is updated right now due to late arriving data, then the view time for the following two days has to be re-calculated for this account. 
もし3日前の視聴時間が遅れて到着したデータのために今更新された場合、このアカウントの次の2日間の視聴時間は再計算される必要があります。 
In this case, the captured late arriving data will tell us the start of the re-calculation, which is much more accurate than recomputing everything for the past X days by guesstimate, where X is a cutoff lookback window decided by business domain knowledge. 
この場合、キャプチャされた遅れて到着したデータは再計算の開始を示し、Xがビジネスドメイン知識によって決定されたカットオフの回顧ウィンドウである過去X日間のすべてを推測で再計算するよりもはるかに正確です。 

<!-- ここまで読んだ! -->

Once the change information (data or range) is captured, a workflow has to write the data to the target table in a slightly more complicated way because the simple INSERT OVERWRITE mechanism won’t work well. 
変更情報（データまたは範囲）がキャプチャされると、ワークフローはデータをターゲットテーブルに少し複雑な方法で書き込む必要があります。なぜなら、単純なINSERT OVERWRITEメカニズムはうまく機能しないからです。 
There are two alternatives: 
2つの代替案があります。 

- Merge pattern: In some compute frameworks, e.g. Spark 3, it supports MERGE INTO to allow new data to be merged into the existing data set. 
- マージパターン：いくつかの計算フレームワーク（例：Spark 3）では、MERGE INTOをサポートしており、新しいデータを既存のデータセットにマージすることができます。 
That solves the write problem for incremental processing. 
これにより、インクリメンタル処理のための書き込み問題が解決されます。 
Note that the workflow/step can be safely restarted without worrying about duplicate data being inserted when using MERGE INTO. 
MERGE INTOを使用する場合、ワークフロー/ステップは重複データが挿入されることを心配せずに安全に再起動できます。 

- Append pattern: Users can also use append only write (e.g. INSERT INTO) to add the new data to the existing data set. 
- アペンドパターン：ユーザーは、アペンド専用の書き込み（例：INSERT INTO）を使用して、新しいデータを既存のデータセットに追加することもできます。 
Once the processing is completed, the append data is committed to the table. 
処理が完了すると、アペンドデータはテーブルにコミットされます。 
If users want to re-run or re-build the data set, they will run a backfill workflow to completely overwrite the target data set (e.g. INSERT OVERWRITE). 
ユーザーがデータセットを再実行または再構築したい場合、彼らはターゲットデータセットを完全に上書きするためにバックフィルワークフローを実行します（例：INSERT OVERWRITE）。 

Additionally, the IPS will naturally support the backfill in many cases. 
さらに、IPSは多くの場合、自然にバックフィルをサポートします。 
Downstream workflows (if there is no business logic change) will be triggered by the data change due to backfill. 
下流のワークフロー（ビジネスロジックの変更がない場合）は、バックフィルによるデータ変更によってトリガーされます。 
This enables auto propagation of backfill data in multi-stage pipelines. 
これにより、マルチステージパイプラインにおけるバックフィルデータの自動伝播が可能になります。 
Note that the backfill support is skipped in this blog. 
このブログではバックフィルサポートは省略されています。 
We will talk about IPS backfill support in another following blog post. 
次のブログ投稿でIPSのバックフィルサポートについて話します。

<!-- ここまで読んだ! -->

### Netflix Maestro

Maestro is the Netflix data workflow orchestration platform built to meet the current and future needs of Netflix. 
Maestroは、Netflixの現在および将来のニーズに応えるために構築されたNetflixのデータワークフローオーケストレーションプラットフォームです。
It is a general-purpose workflow orchestrator that provides a fully managed workflow-as-a-service (WAAS) to the data platform users at Netflix. 
これは、Netflixのデータプラットフォームユーザーに完全に管理されたワークフロー・アズ・ア・サービス（WAAS）を提供する汎用ワークフローオーケストレーターです。
It serves thousands of users, including data scientists, data engineers, machine learning engineers, software engineers, content producers, and business analysts, in various use cases. 
データサイエンティスト、データエンジニア、機械学習エンジニア、ソフトウェアエンジニア、コンテンツプロデューサー、ビジネスアナリストなど、さまざまなユースケースで数千人のユーザーにサービスを提供しています。
Maestro is highly scalable and extensible to support existing and new use cases and offers enhanced usability to end users. 
Maestroは、高いスケーラビリティと拡張性を持ち、既存および新しいユースケースをサポートし、エンドユーザーに対して使いやすさを向上させます。

Since the last blog on Maestro, we have migrated all the workflows to it on behalf of users with minimal interruption. 
前回のMaestroに関するブログ以来、私たちはユーザーのためにすべてのワークフローを最小限の中断で移行しました。
Maestro has been fully deployed in production with 100% workload running on it. 
Maestroは本番環境に完全に展開され、100%のワークロードがそれ上で稼働しています。
IPS is built upon Maestro as an extension by adding two building blocks, i.e. a new trigger mechanism and step job type, to enable incremental processing for all workflows. 
IPSは、すべてのワークフローのインクリメンタル処理を可能にするために、新しいトリガーメカニズムとステップジョブタイプという2つのビルディングブロックを追加することで、Maestroの拡張として構築されています。
It is seamlessly integrated into the whole Maestro ecosystem with minimal onboarding cost. 
それは、最小限のオンボーディングコストで、Maestroエコシステム全体にシームレスに統合されています。

<!-- ここまでラフに読んだ! -->

### Apache Iceberg

Iceberg is a high-performance format for huge analytic tables. 
**Icebergは、大規模な分析テーブルのための高性能フォーマット**です。
Iceberg brings the reliability and simplicity of SQL tables to big data, while making it possible for engines like Spark, Trino, Flink, Presto, Hive and Impala to safely work with the same tables, at the same time. 
Icebergは、SQLテーブルの信頼性とシンプルさをビッグデータに持ち込み、Spark、Trino、Flink、Presto、Hive、Impalaなどの**多様なエンジンが同じテーブルで安全に同時に作業**できるようにします。
It supports expressive SQL, full schema evolution, hidden partitioning, data compaction, and time travel & rollback. 
それは、表現力豊かなSQL、完全なスキーマ進化、隠れパーティショニング、データ圧縮、タイムトラベルおよびロールバックをサポートします。
In the IPS, we leverage the rich features provided by Apache Iceberg to develop a lightweight approach to capture the table changes. 
IPSでは、Apache Icebergが提供する豊富な機能を活用して、テーブルの変更をキャプチャする軽量なアプローチを開発します。

### Incremental Change Capture Design 増分変更キャプチャ設計

Using Netflix Maestro and Apache Iceberg, we created a novel solution for incremental processing, which provides the incremental change (data and range) capture in a super lightweight way without copying any data. 
私たちは、Netflix MaestroとApache Icebergを使用して、データをコピーすることなく、**非常に軽量な方法で増分変更（データと範囲）をキャプチャ**するための新しいソリューションを作成しました。
During our exploration, we see a huge opportunity to improve cost efficiency and engineering productivity using incremental processing. 
私たちの探求の中で、増分処理を使用することでコスト効率とエンジニアリング生産性を向上させる大きな機会があることがわかりました。

Here is our solution to achieve incremental change capture built upon Apache Iceberg features. 
以下は、Apache Icebergの機能に基づいて増分変更キャプチャを実現するための私たちのソリューションです。
As we know, an iceberg table contains a list of snapshots with a set of metadata data. 
**ご存知のように、アイスバーグテーブルは一連のメタデータを持つスナップショットのリストを含んでいます。**
Snapshots include references to the actual immutable data files. 
スナップショットには、実際の不変データファイルへの参照が含まれています。
A snapshot can contain data files from different partitions. 
スナップショットは、異なるパーティションからのデータファイルを含むことができます。

![]()

The graph above shows that s0 contains data for Partition P0 and P1 at T1. 
上のグラフは、s0がT1でパーティションP0とP1のデータを含んでいることを示しています。
Then at T2, a new snapshot s1 is committed to the table with a list of new data files, which includes late arriving data for partition P0 and P1 and data for P2. 
次に、T2で新しいスナップショットs1がテーブルにコミットされ、新しいデータファイルのリストが含まれています。これには、パーティションP0とP1の遅れて到着したデータとP2のデータが含まれています。

- メモ: 
  - 時点t1にて、スナップショット s0 が、パーティション P0 と P1 のdata file を含んでる。
  - 時点t2にて、スナップショット s1 がコミットされ、新しい data file のリストが含まれている。この中には、パーティション P0 と P1 に加えて P2 のデータも含まれてる。

We implemented a lightweight approach to create an iceberg table (called ICDC table), which has its own snapshot but only includes the new data file references from the original table without copying the data files. 
私たちは、**アイスバーグテーブル（ICDCテーブルと呼ばれる）を作成するための軽量なアプローチを実装**しました。このテーブルは独自のスナップショットを持っていますが、データファイルをコピーすることなく、元のテーブルからの新しいデータファイルの参照のみを含んでいます。
It is highly efficient with a low cost. 
これは非常に効率的で、コストが低いです。
Then workflow pipelines can just load the ICDC table to process only the change data from partition P0, P1, P2 without reprocessing the unchanged data in P0 and P1. 
その後、ワークフローパイプラインはICDCテーブルをロードして、P0およびP1の変更されていないデータを再処理することなく、パーティションP0、P1、P2からの変更データのみを処理できます。
Meanwhile, the change range is also captured for the specified data field as the Iceberg table metadata contains the upper and lower bound information of each data field for each data file. 
同時に、変更範囲も指定されたデータフィールドのためにキャプチャされます。アイスバーグテーブルのメタデータには、各データファイルの各データフィールドの上限および下限情報が含まれています。
Moreover, IPS will track the changes in data file granularity for each workflow. 
さらに、IPSは各ワークフローのデータファイルの粒度での変更を追跡します。

<!-- ここまで読んだ! -->

This lightweight approach is seamlessly integrated with Maestro to allow all (thousands) scheduler users to use this new building block (i.e. incremental processing) in their tens of thousands of workflows. 
この軽量なアプローチはMaestroとシームレスに統合されており、すべての（数千の）スケジューラユーザーが数万のワークフローでこの新しいビルディングブロック（すなわち、増分処理）を使用できるようにします。
Each workflow using IPS will be injected with a table parameter, which is the table name of the lightweight ICDC table. 
IPSを使用する各ワークフローには、軽量ICDCテーブルのテーブル名であるテーブルパラメータが注入されます。
The ICDC table contains only the change data. 
ICDCテーブルには変更データのみが含まれています。
Additionally, if the workflow needs the change range, a list of parameters will be injected to the user workflow to include the change range information. 
さらに、ワークフローが変更範囲を必要とする場合、変更範囲情報を含むためにパラメータのリストがユーザーワークフローに注入されます。
The incremental processing can be enabled by a new step job type (ICDC) and/or a new incremental trigger mechanism. 
増分処理は、新しいステップジョブタイプ（ICDC）および/または新しい増分トリガーメカニズムによって有効にできます。
Users can use them together with all existing Maestro features, e.g. foreach patterns, step dependencies based on valid–through-timestamp watermark, write-audit-publish templatized pattern, etc. 
ユーザーは、foreachパターン、有効なタイムスタンプウォーターマークに基づくステップ依存関係、書き込み・監査・公開のテンプレート化されたパターンなど、すべての既存のMaestro機能と一緒にそれらを使用できます。

### Main Advantages 主な利点

With this design, user workflows can adopt incremental processing with very low efforts. 
この設計により、ユーザのワークフローは非常に少ない労力でインクリメンタル処理を採用できます。
The user business logic is also decoupled from the IPS implementation. 
ユーザのビジネスロジックは、IPSの実装からも切り離されています。
Multi-stage pipelines can also mix the incremental processing workflows with existing normal workflows. 
マルチステージパイプラインは、インクリメンタル処理のワークフローと既存の通常のワークフローを混在させることもできます。
We also found that user workflows can be simplified after using IPS by removing additional steps to handle the complexity of the lookback window or calling some internal libraries. 
また、IPSを使用することで、ユーザのワークフローは、ルックバックウィンドウの複雑さを処理するための追加ステップや内部ライブラリの呼び出しを削除することで簡素化できることがわかりました。



## Get Netflix Technology Blog’s stories in your inbox

Join Medium for free to get updates from this writer.
Netflix Maestroにインクリメンタル処理機能を新しい機能/ビルディングブロックとして追加することで、ユーザーは自分のワークフローをより効率的に構築でき、遅れて到着するデータの処理など、多くの難しい問題をより簡単に解決するためのギャップを埋めることができます。



## Emerging Incremental Processing Patterns 新たなインクリメンタル処理パターン

While onboarding user pipelines to IPS, we have discovered a few incremental processing patterns:
ユーザーパイプラインをIPSにオンボーディングする際に、いくつかのインクリメンタル処理パターンを発見しました：



### Incrementally process the captured incremental change data and directly append them to the target table
キャプチャされた増分変更データを段階的に処理し、ターゲットテーブルに直接追加します。

This is the straightforward incremental processing use case, where the change data carries all the information needed for the data processing. 
これは、変更データがデータ処理に必要なすべての情報を持つ、明確な増分処理のユースケースです。

Upstream changes (usually from a single source table) are propagated to the downstream (usually another target table) and the workflow pipeline only needs to process the change data (might join with other dimension tables) and then merge into (usually append) to the target table. 
上流の変更（通常は単一のソーステーブルから）は下流（通常は別のターゲットテーブル）に伝播され、ワークフローパイプラインは変更データを処理するだけで済みます（他の次元テーブルと結合することもあります）そして、ターゲットテーブルにマージ（通常は追加）します。

This pattern will replace lookback window patterns to take care of late arriving data. 
このパターンは、遅れて到着するデータに対処するために、ルックバックウィンドウパターンを置き換えます。

Instead of overwriting past X days of data completely by using a lookback window pattern, user workflows just need to MERGE the change data (including late arriving data) into the target table by processing the ICDC table. 
ルックバックウィンドウパターンを使用して過去X日間のデータを完全に上書きする代わりに、ユーザのワークフローはICDCテーブルを処理することによって変更データ（遅れて到着するデータを含む）をターゲットテーブルにMERGEするだけで済みます。



### Use captured incremental change data as the row level filter list to remove unnecessary transformation
キャプチャされた増分変更データを行レベルのフィルタリストとして使用して、不必要な変換を削除します。

ETL jobs usually need to aggregate data based on certain group-by keys. 
ETLジョブは通常、特定のグループ化キーに基づいてデータを集約する必要があります。

Change data will disclose all the group-by keys that require a re-aggregation due to the new landing data from the source table(s). 
変更データは、ソーステーブルからの新しい着地データにより再集約が必要なすべてのグループ化キーを明らかにします。

Then ETL jobs can join the original source table with the ICDC table on those group-by keys by using ICDC as a filter to speed up the processing to enable calculations of a much smaller set of data. 
その後、ETLジョブは、ICDCをフィルタとして使用して、元のソーステーブルとICDCテーブルをこれらのグループ化キーで結合し、処理を高速化してはるかに小さなデータセットの計算を可能にします。

There is no change to business transform logic and no re-design of ETL workflow. 
ビジネス変換ロジックに変更はなく、ETLワークフローの再設計もありません。

ETL pipelines keep all the benefits of batch workflows.
ETLパイプラインは、バッチワークフローのすべての利点を保持します。



### Use the captured range parameters in the business logic ビジネスロジックにおけるキャプチャされた範囲パラメータの使用

This pattern is usually used in complicated use cases, such as joining multiple tables and doing complex processings. 
このパターンは、複数のテーブルを結合したり、複雑な処理を行ったりするような複雑なユースケースで通常使用されます。

In this case, the change data do not give the full picture of the input needed by the ETL workflow. 
この場合、変更データはETLワークフローに必要な入力の全体像を示しません。

Instead, the change data indicates a range of changed data sets for a specific set of fields (might be partition keys) in a given input table or usually multiple input tables. 
代わりに、変更データは、特定のフィールドのセット（パーティションキーである可能性があります）に対する変更されたデータセットの範囲を、特定の入力テーブルまたは通常は複数の入力テーブルに示します。

Then, the union of the change ranges from all input tables gives the full change data set needed by the workflow. 
次に、すべての入力テーブルからの変更範囲の和集合が、ワークフローに必要な完全な変更データセットを提供します。

Additionally, the whole range of data usually has to be overwritten because the transformation is not stateless and depends on the outcome result from the previous ranges. 
さらに、変換がステートレスではなく、前の範囲からの結果に依存するため、通常はデータの全範囲を上書きする必要があります。

Another example is that the aggregated record in the target table or window function in the query has to be updated based on the whole data set in the partition (e.g. calculating a medium across the whole partition). 
別の例として、ターゲットテーブルの集約レコードやクエリ内のウィンドウ関数は、パーティション内の全データセットに基づいて更新する必要があります（例：パーティション全体の中央値を計算する）。

Basically, the range derived from the change data indicates the dataset to be re-processed. 
基本的に、変更データから導出された範囲は、再処理されるべきデータセットを示します。



## Use cases 使用例

Data workflows at Netflix usually have to deal with late arriving data which is commonly solved by using lookback window pattern due to its simplicity and ease of implementation. 
Netflixのデータワークフローは通常、遅れて到着するデータに対処する必要があり、これはその単純さと実装の容易さからlookback windowパターンを使用することで一般的に解決されます。

In the lookback pattern, the ETL pipeline will always consume the past X number of partition data from the source table and then overwrite the target table in every run. 
lookbackパターンでは、ETLパイプラインは常にソーステーブルから過去のX個のパーティションデータを消費し、毎回ターゲットテーブルを上書きします。

Here, X is a number decided by the pipeline owners based on their domain expertise. 
ここで、Xはパイプラインの所有者がそのドメインの専門知識に基づいて決定する数です。

The drawback is the cost of computation and execution time. 
欠点は、計算コストと実行時間です。

It usually costs almost X times more than the pipeline without considering late arriving data. 
遅れて到着するデータを考慮しないパイプラインと比較して、通常はほぼX倍のコストがかかります。

Given the fact that the late arriving data is sparse, the majority of the processing is done on the data that have been already processed, which is unnecessary. 
遅れて到着するデータがまばらであるという事実を考慮すると、処理の大部分はすでに処理されたデータに対して行われるため、これは不必要です。

Also, note that this approach is based on domain knowledge and sometimes is subject to changes of the business environment or the domain expertise of data engineers. 
また、このアプローチはドメイン知識に基づいており、時にはビジネス環境やデータエンジニアのドメイン専門知識の変化の影響を受けることに注意してください。

In certain cases, it is challenging to come up with a good constant number. 
特定のケースでは、良い定数を考え出すことが難しいです。

Below, we will use a two-stage data pipeline to illustrate how to rebuild it using IPS to improve the cost efficiency. 
以下では、コスト効率を改善するためにIPSを使用して再構築する方法を示すために、二段階データパイプラインを使用します。

We will observe a significant cost reduction (> 80%) with little changes in the business logic. 
ビジネスロジックにほとんど変更を加えずに、顕著なコスト削減（> 80%）を観察します。

In this use case, we will set the lookback window size X to be 14 days, which varies in different real pipelines. 
この使用例では、lookbackウィンドウのサイズXを14日間に設定しますが、これは異なる実際のパイプラインで異なります。



### Original Data Pipeline with Lookback Window オリジナルデータパイプラインとルックバックウィンドウ

- playback_table: an iceberg table holding playback events from user devices ingested by streaming pipelines with late arriving data, which is sparse, only about few percents of the data is late arriving.
- playback_table: ユーザーデバイスからの再生イベントを保持するアイスバーグテーブルで、ストリーミングパイプラインによって取り込まれ、遅れて到着するデータはまばらで、遅れて到着するデータは全体の数パーセント程度です。
  
- playback_daily_workflow: a daily scheduled workflow to process the past X days playback_table data and write the transformed data to the target table for the past X days
- playback_daily_workflow: 過去X日間のplayback_tableデータを処理し、変換されたデータを過去X日間のターゲットテーブルに書き込むための毎日スケジュールされたワークフローです。

- playback_daily_table: the target table of the playback_daily_workflow and get overwritten every day for the past X days
- playback_daily_table: playback_daily_workflowのターゲットテーブルで、過去X日間毎日上書きされます。

- playback_daily_agg_workflow: a daily scheduled workflow to process the past X days’ playback_daily_table data and write the aggregated data to the target table for the past X days
- playback_daily_agg_workflow: 過去X日間のplayback_daily_tableデータを処理し、集約データを過去X日間のターゲットテーブルに書き込むための毎日スケジュールされたワークフローです。

- playback_daily_agg_table: the target table of the playback_daily_agg_workflow and get overwritten every day for the past 14 days.
- playback_daily_agg_table: playback_daily_agg_workflowのターゲットテーブルで、過去14日間毎日上書きされます。

We ran this pipeline in a sample dataset using the real business logic and here is the average execution result of sample runs
このパイプラインを実際のビジネスロジックを使用してサンプルデータセットで実行し、サンプル実行の平均実行結果は以下の通りです。

- The first stage workflow takes about 7 hours to process playback_table data
- 第一段階のワークフローは、playback_tableデータを処理するのに約7時間かかります。

- The second stage workflow takes about 3.5 hours to process playback_daily_table data
- 第二段階のワークフローは、playback_daily_tableデータを処理するのに約3.5時間かかります。



### New Data Pipeline with Incremental Processing 新しいデータパイプラインとインクリメンタル処理

Using IPS, we rewrite the pipeline to avoid re-processing data as much as possible. 
IPSを使用して、データの再処理をできるだけ避けるようにパイプラインを書き換えます。

The new pipeline is shown below. 
新しいパイプラインは以下に示されています。

Stage 1: 
ステージ1：

- ips_playback_daily_workflow: it is the updated version of playback_daily_workflow. 
- ips_playback_daily_workflow：これはplayback_daily_workflowの更新版です。

- The workflow spark sql job then reads an incremental change data capture (ICDC) iceberg table (i.e.playback_icdc_table), which only includes the new data added into the playback_table. 
- ワークフローのSpark SQLジョブは、incremental change data capture (ICDC)アイスバーグテーブル（すなわちplayback_icdc_table）を読み込みます。このテーブルには、playback_tableに追加された新しいデータのみが含まれています。

It includes the late arriving data but does not include any unchanged data from playback_table. 
遅れて到着したデータは含まれますが、playback_tableから変更されていないデータは含まれません。

- The business logic will replace INSERT OVERWRITE by MERGE INTO SQL query and then the new data will be merged into the playback_daily_table. 
- ビジネスロジックはINSERT OVERWRITEをMERGE INTO SQLクエリに置き換え、その後新しいデータがplayback_daily_tableにマージされます。

Stage 2: 
ステージ2：

- IPS captures the changed data of playback_daily_table and also keeps the change data in an ICDC source table (playback_daily_icdc_table). 
- IPSはplayback_daily_tableの変更データをキャプチャし、ICDCソーステーブル（playback_daily_icdc_table）に変更データを保持します。

So we don’t need to hard code the lookback window in the business logic. 
したがって、ビジネスロジックにおいてルックバックウィンドウをハードコーディングする必要はありません。

If there are only Y days having changed data in playback_daily_table, then it only needs to load data for Y days. 
playback_daily_tableに変更データがあるのがY日だけであれば、Y日分のデータのみをロードする必要があります。

- In ips_playback_daily_agg_workflow, the business logic will be the same for the current day’s partition. 
- ips_playback_daily_agg_workflowでは、ビジネスロジックは現在の日のパーティションに対して同じになります。

We then need to update business logic to take care of late arriving data by 
次に、遅れて到着したデータに対処するためにビジネスロジックを更新する必要があります。

- JOIN the playback_daily table with playback_daily_icdc_table on the aggregation group-by keys for the past 2 to X days, excluding the current day (i.e. day 1) 
- 過去2日からX日までの集約グループ化キーに基づいて、playback_daily_tableとplayback_daily_icdc_tableをJOINし、現在の日（すなわち1日目）を除外します。

- Because late arriving data is sparse, JOIN will narrow down the playback_daily_table data set so as to only process a very small portion of it. 
- 遅れて到着したデータはまばらであるため、JOINはplayback_daily_tableのデータセットを絞り込み、ごく小さな部分のみを処理することになります。

- The business logic will use MERGE INTO SQL query then the change will be propagated to the downstream target table 
- ビジネスロジックはMERGE INTO SQLクエリを使用し、その後変更が下流のターゲットテーブルに伝播されます。

- For the current day, the business logic will be the same and consume the data from playback_daily_table and then write the outcome to the target table playback_daily_agg_table using INSERT OVERWRITE because there is no need to join with the ICDC table. 
- 現在の日については、ビジネスロジックは同じで、playback_daily_tableからデータを取得し、その後結果をターゲットテーブルplayback_daily_agg_tableにINSERT OVERWRITEを使用して書き込みます。ICDCテーブルとJOINする必要はありません。

With these small changes, the data pipeline efficiency is greatly improved. 
これらの小さな変更により、データパイプラインの効率が大幅に向上しました。

In our sample run, 
私たちのサンプル実行では、

- The first stage workflow takes just about 30 minutes to process X day change data from playback_table. 
- 第一ステージのワークフローは、playback_tableからX日分の変更データを処理するのに約30分かかります。

- The second stage workflow takes about 15 minutes to process change data between day 2 to day X from playback_daily_table by joining with playback_daily_cdc_table data and takes another 15 minutes to process the current day (i.e. day 1) playback_daily_table change data. 
- 第二ステージのワークフローは、playback_daily_tableからday 2からday Xまでの変更データをplayback_daily_cdc_tableデータとJOINして処理するのに約15分かかり、さらに現在の日（すなわち1日目）のplayback_daily_tableの変更データを処理するのに15分かかります。

Here the spark job settings are the same in original and new pipelines. 
ここで、Sparkジョブの設定は元のパイプラインと新しいパイプラインで同じです。

So in total, the new IPS based pipeline overall needs around 10% of resources (measured by the execution time) to finish. 
したがって、全体として新しいIPSベースのパイプラインは、完了するのに約10％のリソース（実行時間で測定）を必要とします。



## Looking Forward 今後の展望

We will improve IPS to support more complicated cases beyond append-only cases. 
私たちは、IPSを改善し、追加のみのケースを超えたより複雑なケースをサポートできるようにします。

IPS will be able to keep track of the progress of the table changes and support multiple Iceberg table change types (e.g. append, overwrite, etc.). 
IPSは、テーブルの変更の進捗を追跡し、複数のIcebergテーブル変更タイプ（例：追加、上書きなど）をサポートできるようになります。

We will also add managed backfill support into IPS to help users to build, monitor, and validate the backfill. 
また、ユーザーがバックフィルを構築、監視、検証できるように、IPSに管理されたバックフィルサポートを追加します。

We are taking Big Data Orchestration to the next level and constantly solving new problems and challenges, please stay tuned. 
私たちはビッグデータオーケストレーションを次のレベルに引き上げ、新しい問題や課題を常に解決していますので、今後の情報にご期待ください。

If you are motivated to solve large scale orchestration problems, please join us. 
大規模なオーケストレーションの問題を解決する意欲がある方は、ぜひ私たちに参加してください。



## Acknowledgements 謝辞

Thanks to our Product Manager Ashim Pokharel for driving the strategy and requirements. 
私たちのプロダクトマネージャーであるAshim Pokharelに、戦略と要件を推進してくれたことに感謝します。

We’d also like to thank Andy Chu, Kyoko Shimada, Abhinaya Shetty, Bharath Mummadisetty, John Zhuge, Rakesh Veeramacheneni, and other stunning colleagues at Netflix for their suggestions and feedback while developing IPS. 
また、IPSの開発中に提案やフィードバックをくださったAndy Chu、Kyoko Shimada、Abhinaya Shetty、Bharath Mummadisetty、John Zhuge、Rakesh Veeramacheneni、そしてNetflixの他の素晴らしい同僚たちにも感謝します。

We’d also like to thank Prashanth Ramdas, Eva Tse, Charles Smith, and other leaders of Netflix engineering organizations for their constructive feedback and suggestions on the IPS architecture and design. 
さらに、IPSのアーキテクチャとデザインに関する建設的なフィードバックと提案をくださったPrashanth Ramdas、Eva Tse、Charles Smith、そしてNetflixの他のエンジニアリング組織のリーダーたちにも感謝します。



## Published inNetflix TechBlog Netflix TechBlogに掲載

Published inNetflix TechBlog 
Netflix TechBlogに掲載

175K followers 
175Kフォロワー

· 
·

Learn about Netflix’s world class engineering efforts, company culture, product developments and more. 
Netflixの世界クラスのエンジニアリング努力、企業文化、製品開発などについて学びましょう。

Follow 
フォロー



## Written byNetflix Technology Blog

Written byNetflix Technology Blog
Netflix Technology Blogによって執筆されました。

446K followers
446Kのフォロワー

·
·

Learn more about how Netflix designs, builds, and operates our systems and engineering organizations
Netflixがどのようにシステムとエンジニアリング組織を設計、構築、運用しているかについて詳しく学びましょう。

Follow
フォロー



## Responses (10) 反応（10）

Write a response
反応を書く

What are your thoughts?
あなたの考えは何ですか？

What are your thoughts?
あなたの考えは何ですか？



## More from Netflix Technology Blog and Netflix TechBlog Netflix Technology BlogおよびNetflix TechBlogからのさらなる情報

In
Netflix TechBlog
by
Netflix Technology Blog
において



## AV1—Now Powering 30% of Netflix Streaming  
## AV1—現在Netflixストリーミングの30%を支える  

### Liwei Guo, Zhi Li, Sheldon Radford, Jeff Watts  
### Liwei Guo、Zhi Li、Sheldon Radford、Jeff Watts  

4d agoA clap icon69A response icon1  
4日前、拍手アイコン69、応答アイコン1  

69  
69  

1  
1  

In  
に  

Netflix TechBlog  
Netflixテクブログ  

by  
による  

Netflix Technology Blog  
Netflixテクノロジーブログ  



## How and Why Netflix Built a Real-Time Distributed Graph: Part 1—Ingesting and Processing Data…  
## ネットフリックスがリアルタイム分散グラフを構築した方法と理由：パート1 - データの取り込みと処理…

### Authors: Adrian Taruc and James Dalton  
### 著者：アドリアン・タルクとジェームズ・ダルトン

Oct 18A clap icon952A response icon21  
10月18日　拍手アイコン952　応答アイコン21

Oct 18  
10月18日

952  
952

21  
21

In  
に

Netflix TechBlog  
ネットフリックステックブログ

by  
によって

Netflix Technology Blog  
ネットフリックステクノロジーブログ



## Supercharging the ML and AI Development Experience at Netflix  
### Netflix accelerates ML/AI development with Metaflow’s new spin command, enabling notebook-like iteration in production-ready workflows.
## NetflixにおけるMLおよびAI開発体験の強化  
### Netflixは、Metaflowの新しいspinコマンドを使用してML/AI開発を加速し、プロダクション準備が整ったワークフローでノートブックのような反復を可能にします。
Nov 5A clap icon347A response icon4  
11月5日　拍手アイコン347　応答アイコン4  
Nov 5  
11月5日  
347  
347  
4  
4  
Netflix Technology Blog  
Netflixテクノロジーブログ  



## Mount Mayhem at Netflix: Scaling Containers on Modern CPUs  
### Authors: Harshad Sane, Andrew Halaney  
## Mount Mayhem at Netflix: 現代CPU上でのコンテナのスケーリング  
### 著者: ハーシャド・サネ、アンドリュー・ハラネイ  



## Recommended from Medium おすすめのMediumから

Yamishift
Yamishift



## DuckDB Object-Store Caching: Parquet Metadata, Statistics, and Millisecond Warm Starts  
### DuckDBが「冷たい」S3スタイルのデータレイクを、まるでローカルデータベースのように感じさせる方法。

5日前A clap icon34
34
In
Data Engineer Things
by
Vu Trinh



## How does DoorDash evolve realtime processing platform with Iceberg  
### Apache Flink + Apache Iceberg
DoorDashは、Icebergを使用してリアルタイム処理プラットフォームを進化させる方法について説明します。
### Apache Flink + Apache Iceberg



## AWS re:Invent 2025—Key Apache Iceberg Announcements  
### Apache Iceberg was one of the biggest themes at AWS re:Invent 2025. 
Apache Icebergは、AWS re:Invent 2025で最も重要なテーマの一つでした。
With major updates across EMR, Glue, Lake Formation, Catalog… 
EMR、Glue、Lake Formation、Catalogなどにおける主要なアップデートがありました。

4d agoA clap icon5  
4日前に、拍手アイコン5
5  
In  
AWS in Plain English  
AWSを平易な英語で  
by  
Taffarel de Lima Oliveira  
著者：タファレル・デ・リマ・オリベイラ  



## How to build a Data Lakehouse using Kafka, Flink, Iceberg, and Nessie  
### Kafka、Flink、Iceberg、Nessieを使用してデータレイクハウスを構築する方法

Utilizing a data warehouse provided enhanced performance and user-friendliness, whereas data lake analytics offered cost efficiency…
データウェアハウスを利用することで、パフォーマンスとユーザーフレンドリーさが向上し、一方でデータレイク分析はコスト効率を提供しました…

Aug 19A clap icon1  
8月19日　拍手アイコン1

In  
に

Netflix TechBlog  
Netflixテクブログ

by  
によって

Netflix Technology Blog  
Netflixテクノロジーブログ



## From Facts & Metrics to Media Machine Learning: Evolving the Data Engineering Function at Netflix  
### By Dao Mi, Pablo Delgado, Ryan Berti, Amanuel Kahsay, Obi-Ike Nwoke, Christopher Thrailkill, and Patricio Garza
## 事実と指標からメディア機械学習へ：Netflixにおけるデータエンジニアリング機能の進化  
### Dao Mi、Pablo Delgado、Ryan Berti、Amanuel Kahsay、Obi-Ike Nwoke、Christopher Thrailkill、Patricio Garzaによる
Aug 22A clap icon245A response icon10  
8月22日　拍手アイコン245　応答アイコン10
Aug 22  
8月22日
245  
245
10  
10
In  
fresha-data-engineering  
by  
Anton Borisov  
fresha-data-engineeringにて  
Anton Borisovによる



## Iceberg MoR the Hard Way: StarRocks Code Dive  
## Iceberg MoRをハードウェイで: StarRocksコードダイブ

### How I Learned to Stop Worrying and Love the Delete Files: A Journey into StarRocks’ Iceberg MoR Implementation  
### 心配するのをやめて削除ファイルを愛することを学んだ方法: StarRocksのIceberg MoR実装への旅

Sep 3A clap icon108  
9月3日　拍手アイコン108

Sep 3  
9月3日

108  
108

Help  
ヘルプ

Status  
ステータス

About  
概要

Careers  
キャリア

Press  
プレス

Blog  
ブログ

Privacy  
プライバシー

Rules  
ルール

Terms  
利用規約

Text to speech  
テキスト読み上げ
