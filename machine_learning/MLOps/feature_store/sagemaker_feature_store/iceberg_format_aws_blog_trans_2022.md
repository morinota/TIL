refs: https://aws.amazon.com/jp/blogs/machine-learning/speed-ml-development-using-sagemaker-feature-store-and-apache-iceberg-offline-store-compaction/

# Speed ML development using SageMaker Feature Store and Apache Iceberg offline store compaction 
SageMaker Feature StoreとApache Icebergオフラインストアの圧縮を使用したML開発の加速

by Arnaud Lauer, Brandon Chatham, Ioan Catana, and Mark Roy  
著者: アルノー・ローラー、ブランドン・チャサム、イオアン・カタナ、マーク・ロイ

on 21 DEC 2022  
日付: 2022年12月21日

in Advanced (300), Amazon SageMaker, Artificial Intelligence  
分野: Advanced (300)、Amazon SageMaker、人工知能

Today, companies are establishing feature stores to provide a central repository to scale ML development across business units and data science teams.  
今日、企業は、ビジネスユニットやデータサイエンスチーム全体でML開発を拡張するための中央リポジトリを提供するために、フィーチャーストアを設立しています。
As feature data grows in size and complexity, data scientists need to be able to efficiently query these feature stores to extract datasets for experimentation, model training, and batch scoring.  
**フィーチャーデータがサイズと複雑さの両方で増加するにつれて、データサイエンティストは、実験、モデル訓練、およびバッチスコアリングのためのデータセットを抽出するために、これらのフィーチャーストアを効率的にクエリできる必要があります**。

Amazon SageMaker Feature Store is a purpose-built feature management solution that helps data scientists and ML engineers securely store, discover, and share curated data used in training and prediction workflows.  
Amazon SageMaker Feature Storeは、データサイエンティストとMLエンジニアがトレーニングおよび予測ワークフローで使用されるキュレーションデータを安全に保存、発見、共有するのを支援するために特別に設計されたフィーチャー管理ソリューションです。
SageMaker Feature Store now supports Apache Iceberg as a table format for storing features.  
SageMaker Feature Storeは、フィーチャーを保存するためのテーブルフォーマットとしてApache Icebergをサポートするようになりました。
This accelerates model development by enabling faster query performance when extracting ML training datasets, taking advantage of Iceberg table compaction.  
これは、**Icebergテーブルの圧縮を利用してMLトレーニングデータセットを抽出する際のクエリパフォーマンスを向上**させることで、モデル開発を加速します。
Depending on the design of your feature groups and their scale, you can experience training query performance improvements of 10x to 100x by using this new capability.  
フィーチャーグループの設計とその規模に応じて、この新しい機能を使用することで、**トレーニングクエリのパフォーマンスが10倍から100倍向上する**ことがあります。

By the end of this post, you will know how to create feature groups using the Iceberg format, execute Iceberg’s table management procedures using Amazon Athena, and schedule these tasks to run autonomously.  
この記事の終わりまでに、Icebergフォーマットを使用してフィーチャーグループを作成し、**Amazon Athenaを使用**してIcebergのテーブル管理手順を実行し、これらのタスクを自動的に実行するようにスケジュールする方法を知ることができます。(Athenaを使うのは変わらないんだな...!:thinking:)
If you are a Spark user, you’ll also learn how to execute the same procedures using Spark and incorporate them into your own Spark environment and automation.  
Sparkユーザーであれば、同じ手順をSparkを使用して実行し、それを自分のSpark環境や自動化に組み込む方法も学ぶことができます。(なるほど、必ずしもAthena一択、って訳でもないのか:thinking:)

<!-- ここまで読んだ!    -->

## SageMaker Feature StoreとApache Iceberg

Amazon SageMaker Feature Storeは、特徴量と関連するメタデータのための集中型ストアであり、異なるプロジェクトやMLモデルに取り組むデータサイエンティストチームが特徴量を簡単に発見し再利用できるようにします。

Amazon SageMaker Feature Storeは、特徴量を管理するためのオンラインモードとオフラインモードで構成されています。オンラインストアは、低遅延のリアルタイム推論ユースケースに使用されます。**オフラインストアは、主にバッチ予測とモデル訓練に使用**されます。オフラインストアは**追加専用のストア**であり、履歴の特徴量データを保存およびアクセスするために使用できます。オフラインストアを使用することで、ユーザーは探索とバッチスコアリングのために特徴量を保存および提供し、**モデル訓練のための時点正確なデータセットを抽出できます**。

オフラインストアのデータは、AWSアカウント内のAmazon Simple Storage Service (Amazon S3) バケットに保存されます。SageMaker Feature Storeは、特徴量グループの作成時に自動的にAWS Glue Data Catalogを構築します。顧客は、Sparkランタイムを使用してオフラインストアのデータにアクセスし、ML特徴量分析や特徴量エンジニアリングのユースケースのためにビッグデータ処理を実行することもできます。

**テーブルフォーマット(Table formats)は、データファイル(データレイク内の...!:thinking:)をテーブルとして抽象化する方法を提供**します。
これまでの数年間で、ACIDトランザクション、ガバナンス、およびカタログのユースケースをサポートするために**多くのテーブルフォーマットが登場**しました。
Apache Icebergは、非常に大きな分析データセットのためのオープンテーブルフォーマットです。
**Icebergは、大規模なファイルコレクションをテーブルとして管理し、レコードレベルの挿入、更新、削除、タイムトラベルクエリなどの現代的な分析データレイク操作をサポート**します。Icebergは、ディレクトリではなくテーブル内の個々のデータファイルを追跡します。これにより、ライターはデータファイルをその場で作成でき（ファイルは移動または変更されません）、**明示的なコミットでのみファイルをテーブルに追加**します。(自前でparquetファイルをS3に置くだけではIcebergテーブルには追加されない、ってことか...!:thinking:)
テーブルの状態はメタデータファイルに保持されます。
テーブルの状態に対するすべての変更は、新しいメタデータファイルバージョンを作成し、古いメタデータをatomicに置き換えます。
テーブルメタデータファイルは、テーブルスキーマ、パーティショニング構成、およびその他のプロパティを追跡します。

<!-- ここまで読んだ!    -->

IcebergはAWSサービスとの統合を持っています。たとえば、AWS Glue Data CatalogをIcebergテーブルのメタストアとして使用でき、AthenaはApache Parquetフォーマットのデータを使用するApache Icebergテーブルに対して、読み取り、タイムトラベル、書き込み、およびDDLクエリをサポートします。

SageMaker Feature Storeを使用すると、デフォルトの標準Glueフォーマットの代わりにIcebergテーブルフォーマットを使用して特徴量グループを作成できるようになります。これにより、顧客は新しいテーブルフォーマットを活用して、Icebergのファイル圧縮およびデータプルーニング機能を使用し、ユースケースおよび最適化要件を満たすことができます。Icebergはまた、顧客が**削除、タイムトラベルクエリ、高同時実行トランザクション、および高パフォーマンスクエリを実行できるように**します。

Icebergをテーブルフォーマットとして、テーブルメンテナンス操作（圧縮など）と組み合わせることで、顧客はオフライン特徴量グループを大規模に扱う際にクエリパフォーマンスを向上させ、ML訓練データセットをより迅速に構築できるようになります。

次の図は、Icebergをテーブルフォーマットとして使用したオフラインストアの構造を示しています。

![](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2022/12/16/Screenshot-2022-12-16-at-17.37.19.png)

次のセクションでは、Icebergフォーマットを使用して特徴量グループを作成する方法、AWS Athenaを使用してIcebergのテーブル管理手順を実行する方法、これらのタスクをオンデマンドまたはスケジュールに従って実行するためにAWSサービスを使用する方法を学びます。Sparkユーザーの場合、同じ手順をSparkを使用して実行する方法も学びます。
ステップバイステップの指示については、GitHubにあるサンプルノートブックも提供しています。この投稿では、最も重要な部分を強調します。

<!-- ここまで読んだ! -->

## Creating feature groups using Iceberg table format

新しいフィーチャグループを作成する際には、Icebergをテーブルフォーマットとして選択する必要があります。
A new optional parameter TableFormat can be set either interactively using Amazon SageMaker Studio or through code using the API or the SDK. 
**新しいオプションのパラメータ`TableFormat`**は、Amazon SageMaker Studioを使用してインタラクティブに設定するか、APIまたはSDKを使用してコードを通じて設定できます。
This parameter accepts the values ICEBERG or GLUE (for the current AWS Glue format). 
このパラメータは、**ICEBERGまたはGLUE（現在のAWS Glueフォーマット）という値**を受け入れます。
The following code snippet shows you how to create a feature group using the Iceberg format and FeatureGroup.create API of the SageMaker SDK. 
以下のコードスニペットは、Icebergフォーマットを使用してフィーチャグループを作成する方法と、SageMaker SDKのFeatureGroup.create APIを示しています。

The table will be created and registered automatically in the AWS Glue Data Catalog. 
**テーブルは自動的に作成され、AWS Glueデータカタログに登録**されます。

Now that the orders_feature_group_iceberg is created, you can ingest features using your ingestion pipeline of choice. 
orders_feature_group_icebergが作成されたので、**好みの取り込みパイプラインを使用してフィーチャを取り込む**ことができます。(= `ingest` APIの他にも公式で色んな方法がある、ってこと...??:thinking:)
In this example, we ingest records using the FeatureGroup.ingest() API, which ingests records from a Pandas DataFrame. 
この例では、Pandas DataFrameからレコードを取り込む`FeatureGroup.ingest()` APIを使用してレコードを取り込みます。
You can also use the FeatureGroup().put_record API to ingest individual records or to handle streaming sources. 
また、FeatureGroup().put_record APIを使用して、個々のレコードを取り込むことやストリーミングソースを処理することもできます。
Spark users can also ingest Spark dataframes using our Spark Connector. 
Sparkユーザーは、私たちのSparkコネクタを使用してSparkデータフレームを取り込むこともできます。

You can verify that the records have been ingested successfully by running a query against the offline feature store. 
オフラインフィーチャストアに対してクエリを実行することで、レコードが正常に取り込まれたことを確認できます。
You can also navigate to the S3 location and see the new folder structure. 
また、S3の場所に移動して新しいフォルダ構造を見ることもできます。

<!-- ここまで読んだ! -->

## Executing Iceberg table management procedures アイスバーグテーブル管理手順の実行

Amazon Athena is a serverless SQL query engine that natively supports Iceberg management procedures. 
**Amazon Athenaは、アイスバーグ管理手順をネイティブにサポートするサーバーレスSQLクエリエンジン**です。
In this section, you will use Athena to manually compact the offline feature group you created. 
このセクションでは、**Athenaを使用して、作成したオフラインフィーチャーグループを手動で圧縮**します。
Note you will need to use Athena engine version 3. 
Athenaエンジンのバージョン3を使用する必要があります。
For this, you can create a new workgroup, or configure an existing workgroup, and select the recommended Athena engine version 3. 
そのためには、新しいワークグループを作成するか、既存のワークグループを構成し、推奨されるAthenaエンジンバージョン3を選択できます。
For more information and instructions for changing your Athena engine version, refer to Changing Athena engine versions. 
Athenaエンジンのバージョンを変更するための詳細情報と手順については、「Changing Athena engine versions」を参照してください。

<!-- ここまで読んだ! -->

As data accumulates into an Iceberg table, queries may gradually become less efficient because of the increased processing time required to open additional files. 
**データがアイスバーグテーブルに蓄積されるにつれて、追加のファイルを開くために必要な処理時間が増加するため、クエリの効率が徐々に低下する可能性**があります。
Compaction optimizes the structural layout of the table without altering table content. 
**圧縮は、テーブルの内容を変更することなく、テーブルの構造的レイアウトを最適化**します。
(なるほど、データが溜まる時にたまにparquetファイルをまとめる、ってことか...!:thinking:)

To perform compaction, you use the OPTIMIZE table REWRITE DATA compaction table maintenance command in Athena. 
圧縮を実行するには、**Athenaで`OPTIMIZE table REWRITE DATA`圧縮テーブルメンテナンスコマンドを使用**します。
The following syntax shows how to optimize the data layout of a feature group stored using the Iceberg table format. 
以下の構文は、アイスバーグテーブル形式を使用して保存されたフィーチャーグループのデータレイアウトを最適化する方法を示しています。
The sagemaker_featurestore represents the name of the SageMaker Feature Store database, and orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334 is our feature group table name. 
`sagemaker_featurestore`はSageMaker Feature Storeデータベースの名前を表し、`orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334`は私たちのフィーチャーグループテーブル名です。

```bash
OPTIMIZE sagemaker_featurestore.orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334 REWRITE DATA USING BIN_PACK
```

<!-- ここまで読んだ! -->

After running the optimize command, you use the VACUUM procedure, which performs snapshot expiration and removes orphan files. 
最適化コマンドを実行した後、VACUUM手順を使用します。これにより、スナップショットの有効期限が切れ、孤立したファイルが削除されます。
These actions reduce metadata size and remove files that are not in the current table state and are also older than the retention period specified for the table. 
これらのアクションは、メタデータのサイズを削減し、現在のテーブル状態にないファイルや、テーブルに指定された保持期間よりも古いファイルを削除します。

```
VACUUM sagemaker_featurestore.orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334
```

Bash

Note that table properties are configurable using Athena’s ALTER TABLE. 
テーブルプロパティは、AthenaのALTER TABLEを使用して構成可能であることに注意してください。

For an example of how to do this, see the Athena documentation. 
これを行う方法の例については、Athenaのドキュメントを参照してください。

For VACUUM, vacuum_min_snapshots_to_keep and vacuum_max_snapshot_age_seconds can be used to configure snapshot pruning parameters. 
VACUUMの場合、`vacuum_min_snapshots_to_keep`および`vacuum_max_snapshot_age_seconds`を使用してスナップショットのプルーニングパラメータを構成できます。

Let’s have a look at the performance impact of running compaction on a sample feature group table. 
サンプルフィーチャーグループテーブルで圧縮を実行した際のパフォーマンスへの影響を見てみましょう。

For testing purposes, we ingested the same orders feature records into two feature groups, orders-feature-group-iceberg-pre-comp-02-11-03-06-1669979003 and orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334, using a parallelized SageMaker processing job with Scikit-Learn, which results in 49,908,135 objects stored in Amazon S3 and a total size of 106.5 GiB. 
テスト目的で、同じ注文フィーチャーレコードを2つのフィーチャーグループ、`orders-feature-group-iceberg-pre-comp-02-11-03-06-1669979003`と`orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334`に取り込みました。これは、Scikit-Learnを使用した並列化されたSageMaker処理ジョブを使用して行われ、Amazon S3に49,908,135オブジェクトが保存され、合計サイズは106.5 GiBです。

We run a query to select the latest snapshot without duplicates and without deleted records on the feature group orders-feature-group-iceberg-pre-comp-02-11-03-06-1669979003. 
フィーチャーグループ`orders-feature-group-iceberg-pre-comp-02-11-03-06-1669979003`で、重複や削除されたレコードなしで最新のスナップショットを選択するクエリを実行します。

Prior to compaction, the query took 1hr 27mins. 
圧縮前は、クエリの実行に1時間27分かかりました。

We then run compaction on orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334 using the Athena OPTIMIZE query, which compacted the feature group table to 109,851 objects in Amazon S3 and a total size of 2.5 GiB. 
次に、AthenaのOPTIMIZEクエリを使用して`orders-feature-group-iceberg-post-comp-03-14-05-17-1670076334`で圧縮を実行し、フィーチャーグループテーブルをAmazon S3に109,851オブジェクト、合計サイズ2.5 GiBに圧縮しました。

If we then run the same query after compaction, its runtime decreased to 1min 13sec. 
圧縮後に同じクエリを実行すると、実行時間は1分13秒に短縮されました。

With Iceberg file compaction, the query execution time improved significantly. 
アイスバーグファイルの圧縮により、クエリの実行時間が大幅に改善されました。

For the same query, the run time decreased from 1h 27mins to 1min 13sec, which is 71 times faster. 
同じクエリに対して、実行時間は1時間27分から1分13秒に短縮され、71倍速くなりました。



## Scheduling Iceberg compaction with AWS services
アイスバーグコンパクションのスケジューリングとAWSサービス

In this section, you will learn how to automate the table management procedures to compact your offline feature store. 
このセクションでは、オフラインフィーチャーストアをコンパクトにするためのテーブル管理手順を自動化する方法を学びます。

The following diagram illustrates the architecture for creating feature groups in Iceberg table format and a fully automated table management solution, which includes file compaction and cleanup operations. 
以下の図は、Icebergテーブル形式でフィーチャーグループを作成するためのアーキテクチャと、ファイルのコンパクションおよびクリーンアップ操作を含む完全自動化されたテーブル管理ソリューションを示しています。

At a high level, you create a feature group using the Iceberg table format and ingest records into the online feature store. 
高いレベルでは、Icebergテーブル形式を使用してフィーチャーグループを作成し、オンラインフィーチャーストアにレコードを取り込みます。

Feature values are automatically replicated from the online store to the historical offline store. 
フィーチャー値は、オンラインストアから履歴のオフラインストアに自動的に複製されます。

Athena is used to run the Iceberg management procedures. 
Athenaは、Iceberg管理手順を実行するために使用されます。

To schedule the procedures, you set up an AWS Glue job using a Python shell script and create an AWS Glue job schedule. 
手順をスケジュールするために、Pythonシェルスクリプトを使用してAWS Glueジョブを設定し、AWS Glueジョブスケジュールを作成します。



### AWS Glue Job setup AWS Glueジョブの設定

You use an AWS Glue job to execute the Iceberg table maintenance operations on a schedule. 
AWS Glueジョブを使用して、Icebergテーブルのメンテナンス操作をスケジュールに従って実行します。

First, you need to create an IAM role for AWS Glue to have permissions to access Amazon Athena, Amazon S3, and CloudWatch. 
まず、AWS GlueがAmazon Athena、Amazon S3、およびCloudWatchにアクセスするための権限を持つIAMロールを作成する必要があります。

Next, you need to create a Python script to run the Iceberg procedures. 
次に、Iceberg手続きを実行するためのPythonスクリプトを作成する必要があります。

You can find the sample script in GitHub. 
サンプルスクリプトはGitHubで見つけることができます。

The script will execute the OPTIMIZE query using boto3. 
このスクリプトは、boto3を使用してOPTIMIZEクエリを実行します。

```
optimize_sql=f"optimize {database}.{table} rewrite data using bin_pack"
```
```
optimize_sql=f"optimize {database}.{table} rewrite data using bin_pack"
```

The script has been parametrized using the AWS Glue getResolvedOptions(args, options) utility function that gives you access to the arguments that are passed to your script when you run a job. 
このスクリプトは、AWS GlueのgetResolvedOptions(args, options)ユーティリティ関数を使用してパラメータ化されており、ジョブを実行する際にスクリプトに渡される引数にアクセスできます。

In this example, the AWS Region, the Iceberg database and table for your feature group, the Athena workgroup, and the Athena output location results folder can be passed as parameters to the job, making this script reusable in your environment. 
この例では、AWSリージョン、機能グループのためのIcebergデータベースとテーブル、Athenaワークグループ、およびAthena出力場所の結果フォルダをジョブにパラメータとして渡すことができ、このスクリプトを環境内で再利用可能にします。

Finally, you create the actual AWS Glue job to run the script as a shell in AWS Glue. 
最後に、スクリプトをAWS Glue内でシェルとして実行する実際のAWS Glueジョブを作成します。

- Navigate to the AWS Glue console. 
- AWS Glueコンソールに移動します。

- Choose the Jobs tab under AWS Glue Studio. 
- AWS Glue StudioのJobsタブを選択します。

- Select Python Shell script editor. 
- Python Shellスクリプトエディタを選択します。

- Choose Upload and edit an existing script. Click Create. 
- 既存のスクリプトをアップロードして編集することを選択します。作成をクリックします。

- The Job details button lets you configure the AWS Glue job. 
- Job detailsボタンを使用して、AWS Glueジョブを構成できます。

You need to select the IAM role you created earlier. 
以前に作成したIAMロールを選択する必要があります。

Select Python 3.9 or the latest available Python version. 
Python 3.9または最新の利用可能なPythonバージョンを選択します。

- In the same tab, you can also define a number of other configuration options, such as Number of retries or Job timeout. 
- 同じタブで、リトライ回数やジョブタイムアウトなど、他のいくつかの構成オプションを定義することもできます。

In Advanced properties, you can add job parameters to execute the script, as shown in the example screenshot below. 
Advanced propertiesでは、以下の例のスクリーンショットに示すように、スクリプトを実行するためのジョブパラメータを追加できます。

- Click Save. 
- 保存をクリックします。

In the Schedules tab, you can define the schedule to run the feature store maintenance procedures. 
Schedulesタブでは、機能ストアのメンテナンス手続きを実行するスケジュールを定義できます。

For example, the following screenshot shows you how to run the job on a schedule of every 6 hours. 
例えば、以下のスクリーンショットは、6時間ごとにジョブを実行する方法を示しています。

You can monitor job runs to understand runtime metrics such as completion status, duration, and start time. 
ジョブの実行を監視して、完了状況、所要時間、開始時刻などの実行時メトリクスを理解できます。

You can also check the CloudWatch Logs for the AWS Glue job to check that the procedures run successfully. 
また、AWS GlueジョブのCloudWatch Logsを確認して、手続きが正常に実行されたかどうかを確認できます。



### Executing Iceberg table management tasks with Spark Icebergテーブル管理タスクの実行

Customers can also use Spark to manage the compaction jobs and maintenance methods. 
顧客は、Sparkを使用して圧縮ジョブやメンテナンス方法を管理することもできます。 
For more detail on the Spark procedures, see the Spark documentation. 
Sparkの手順の詳細については、Sparkのドキュメントを参照してください。

You first need to configure some of the common properties. 
最初に、いくつかの一般的なプロパティを設定する必要があります。

```
%%configure-f{"conf":{"spark.sql.catalog.smfs":"org.apache.iceberg.spark.SparkCatalog","spark.sql.catalog.smfs.catalog-impl":"org.apache.iceberg.aws.glue.GlueCatalog","spark.sql.catalog.smfs.warehouse":"<YOUR_ICEBERG_DATA_S3_LOCATION>","spark.sql.extensions":"org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions","spark.sql.catalog.smfs.glue.skip-name-validation":"true"}}
```
-f
{
"conf"
:
{
"spark.sql.catalog.smfs"
:
"org.apache.iceberg.spark.SparkCatalog"
"spark.sql.catalog.smfs.catalog-impl"
:
"org.apache.iceberg.aws.glue.GlueCatalog"
"spark.sql.catalog.smfs.warehouse"
:
"<YOUR_ICEBERG_DATA_S3_LOCATION>"
"spark.sql.extensions"
:
"org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
"spark.sql.catalog.smfs.glue.skip-name-validation"
:
"true"
}
}
Bash
The following code can be used to optimize the feature groups via Spark. 
以下のコードは、Sparkを介してフィーチャーグループを最適化するために使用できます。

```
spark.sql(f"""CALL smfs.system.rewrite_data_files(table=>'{DATABASE}.`{ICEBERG_TABLE}`')""")
```
(
""
(
=
>
'{DATABASE}.`{ICEBERG_TABLE}`'
)
""
)
Bash
You can then execute the next two table maintenance procedures to remove older snapshots and orphan files that are no longer needed. 
次に、古いスナップショットともはや必要のない孤立ファイルを削除するために、次の2つのテーブルメンテナンス手順を実行できます。

```
spark.sql(f"""CALL smfs.system.expire_snapshots(table=>'{DATABASE}.`{ICEBERG_TABLE}`', older_than=>TIMESTAMP'{one_day_ago}', retain_last=>1)""")spark.sql(f"""CALL smfs.system.remove_orphan_files(table=>'{DATABASE}.`{ICEBERG_TABLE}`')""")
```
(
""
(
=
>
'{DATABASE}.`{ICEBERG_TABLE}`'
=
>
'{one_day_ago}'
=
>
1
)
""
)
(
""
(
=
>
'{DATABASE}.`{ICEBERG_TABLE}`'
)
""
)
Bash
You can then incorporate the above Spark commands into your Spark environment. 
その後、上記のSparkコマンドをSpark環境に組み込むことができます。 
For example, you can create a job that performs the optimization above on a desired schedule or in a pipeline after ingestion. 
たとえば、希望のスケジュールで上記の最適化を実行するジョブを作成するか、取り込み後のパイプラインで実行することができます。 
To explore the complete code example, and try it out in your own account, see the GitHub repo. 
完全なコード例を探求し、自分のアカウントで試すには、GitHubリポジトリを参照してください。



## Conclusion 結論

SageMaker Feature Store provides a purpose-built feature management solution to help organizations scale ML development across data science teams. 
SageMaker Feature Storeは、組織がデータサイエンスチーム全体でML開発をスケールさせるための目的特化型の特徴管理ソリューションを提供します。
In this post, we explained how you can leverage Apache Iceberg as a table format and table maintenance operations such as compaction to benefit from significantly faster queries when working with offline feature groups at scale and, as a result, build training datasets faster. 
この投稿では、Apache Icebergをテーブルフォーマットとして活用し、圧縮などのテーブルメンテナンス操作を利用することで、オフラインフィーチャーグループを大規模に扱う際に、クエリを大幅に高速化し、その結果、トレーニングデータセットをより早く構築する方法を説明しました。
Give it a try, and let us know what you think in the comments. 
ぜひ試してみて、コメントであなたの意見を教えてください。



### About the authors 著者について

Arnaud Lauer is a Senior Partner Solutions Architect in the Public Sector team at AWS. 
Arnaud Lauerは、AWSの公共部門チームのシニアパートナーソリューションアーキテクトです。 
He enables partners and customers to understand how best to use AWS technologies to translate business needs into solutions. 
彼は、パートナーや顧客がビジネスニーズをソリューションに変換するためにAWS技術をどのように最適に使用するかを理解できるようにします。 
He brings more than 17 years of experience in delivering and architecting digital transformation projects across a range of industries, including public sector, energy, and consumer goods. 
彼は、公共部門、エネルギー、消費財などのさまざまな業界でデジタルトランスフォーメーションプロジェクトを提供し、設計する17年以上の経験を持っています。 
Arnaud holds 12 AWS certifications, including the ML Specialty Certification. 
Arnaudは、MLスペシャリティ認定を含む12のAWS認定を保持しています。

Ioan Catana is an Artificial Intelligence and Machine Learning Specialist Solutions Architect at AWS. 
Ioan Catanaは、AWSの人工知能および機械学習スペシャリストソリューションアーキテクトです。 
He helps customers develop and scale their ML solutions in the AWS Cloud. 
彼は、顧客がAWSクラウドでMLソリューションを開発し、スケールさせるのを支援します。 
Ioan has over 20 years of experience mostly in software architecture design and cloud engineering. 
Ioanは、主にソフトウェアアーキテクチャ設計とクラウドエンジニアリングにおいて20年以上の経験を持っています。

Mark Roy is a Principal Machine Learning Architect for AWS, helping customers design and build AI/ML solutions. 
Mark Royは、AWSのプリンシパル機械学習アーキテクトであり、顧客がAI/MLソリューションを設計し、構築するのを支援しています。 
Mark’s work covers a wide range of ML use cases, with a primary interest in computer vision, deep learning, and scaling ML across the enterprise. 
Markの仕事は、コンピュータビジョン、深層学習、企業全体でのMLのスケーリングに主に関心を持ち、幅広いMLユースケースをカバーしています。 
He has helped companies in many industries, including insurance, financial services, media and entertainment, healthcare, utilities, and manufacturing. 
彼は、保険、金融サービス、メディアとエンターテインメント、ヘルスケア、ユーティリティ、製造業など、多くの業界の企業を支援してきました。 
Mark holds six AWS certifications, including the ML Specialty Certification. 
Markは、MLスペシャリティ認定を含む6つのAWS認定を保持しています。 
Prior to joining AWS, Mark was an architect, developer, and technology leader for over 25 years, including 19 years in financial services. 
AWSに参加する前、Markは25年以上にわたりアーキテクト、開発者、テクノロジーリーダーとして活動しており、そのうち19年間は金融サービスに従事していました。

Brandon Chatham is a software engineer with the SageMaker Feature Store team. 
Brandon Chathamは、SageMaker Feature Storeチームのソフトウェアエンジニアです。 
He’s deeply passionate about building elegant systems that bring big data and machine learning to people’s fingertips. 
彼は、大規模データと機械学習を人々の手の届くところに届ける洗練されたシステムを構築することに深い情熱を持っています。



### Resources リソース
- Getting Started 始めに
- What's New 新着情報



### Blog Topics ブログトピック
- Amazon Bedrock
- Amazon Comprehend
- Amazon Kendra
- Amazon Lex
- Amazon Polly
- Amazon Q
- Amazon Rekognition
- Amazon SageMaker
- Amazon Textract



### Follow フォロー

- Twitter
- Facebook
- LinkedIn
- Twitch
- Email Updates
- メール更新
Create an AWS account
AWSアカウントを作成



## Learn 学ぶ

- What Is AWS? 
- AWSとは何ですか？

- What Is Cloud Computing? 
- クラウドコンピューティングとは何ですか？

- What Is Generative AI? 
- ジェネレーティブAIとは何ですか？

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
- AWS Solutions Library AWSソリューションライブラリ
- Architecture Center アーキテクチャセンター
- Product and Technical FAQs 製品および技術に関するFAQ
- Analyst Reports アナリストレポート
- AWS Partners AWSパートナー
- AWS Inclusion, Diversity & Equity AWSの包括性、多様性、平等



## Developers 開発者

- Developer Center 開発者センター
- SDKs & Tools SDKおよびツール
- .NET on AWS AWS上の.NET
- Python on AWS AWS上のPython
- Java on AWS AWS上のJava
- PHP on AWS AWS上のPHP
- JavaScript on AWS AWS上のJavaScript



## Help ヘルプ
- Contact Us お問い合わせ
- File a Support Ticket サポートチケットを提出する
- AWS re:Post AWS re:Post
- Knowledge Center ナレッジセンター
- AWS Support Overview AWSサポートの概要
- Get Expert Help 専門家の支援を受ける
- AWS Accessibility AWSアクセシビリティ
- Legal 法的情報
English 英語
Amazon is an Equal Opportunity Employer: Minority / Women / Disability / Veteran / Gender Identity / Sexual Orientation / Age.
アマゾンは平等な機会を提供する雇用主です：少数派 / 女性 / 障害者 / 退役軍人 / 性別のアイデンティティ / 性的指向 / 年齢。
facebook
linkedin
instagram
twitch
youtube
podcasts
email
- Privacy プライバシー
- Site terms サイト利用規約
- Cookie Preferences クッキーの設定
© 2025, Amazon Web Services, Inc. or its affiliates. All rights reserved.
© 2025年、アマゾンウェブサービス株式会社またはその関連会社。全著作権所有。
