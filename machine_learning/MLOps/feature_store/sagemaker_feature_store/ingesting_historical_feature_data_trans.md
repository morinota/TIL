

# Ingesting Historical Feature Data into SageMaker Feature Store 歴史的特徴データをSageMaker Feature Storeに取り込む方法    
How to backfill the SageMaker Offline Feature Store by writing directly into S3 S3に直接書き込むことでSageMakerオフラインFeature Storeをバックフィルする方法

## What is this about? これは何についてですか？

Amazon SageMaker Feature Storeis a fully managed, purpose-built repository to store, update, retrieve, and share machine learning (ML) features. 
Amazon SageMaker Feature Storeは、機械学習（ML）機能を保存、更新、取得、共有するための完全に管理された、purpose-built(=特定の目的に特化した)リポジトリです。
It was introduced at AWS re:Invent in December 2020 and has quickly become one of the most popular services within the SageMaker family. 
これは2020年12月のAWS re:Inventで導入され、**SageMakerファミリー内で最も人気のあるサービスの1つとなりました**。(あ、人気なんだ!:thinking:)
Many AWS customers I have spoken to since re:Invent expressed their interest in SageMaker Feature Store (SMFS). 
re:Invent以降に話をした多くのAWS顧客は、SageMaker Feature Store（**SMFS**）への関心を示しました。

Some of these customers have historical feature data they would like to migrate to the SMFS offline store which can store large volumes of feature data that is used to keep track of historical feature values and to create train/test data for model development or by batch applications. 
これらの顧客の中には、**SMFSオフラインストアに移行したい歴史的な特徴データを持っている**顧客もいます。SMFSオフラインストアは、歴史的な特徴値を追跡し、モデル開発やバッチアプリケーションのためのトレーニング/テストデータを作成するために使用される大量の特徴データを保存できます。
(はいはい、過去に別の場所に保存してた特徴量レコード達をSMFSオフラインストアに移行したい、って話ね...!:thinking:)

A major challenge when ingesting historical data into SMFS offline store is that users will get charged when using the ingestion APIs, even if they only want to backfill historical data. 
**SMFSオフラインストアにhistoricalデータを取り込む際の大きな課題は、ユーザーが取り込みAPIを使用すると課金されること**です。これは、歴史的なデータをバックフィルしたいだけの場合でも同様です。(やっぱり大きな課題なんだ...!:thinking:)
These charges can grow quickly if customers have Terabytes of data they want to migrate to SMFS. 
**顧客がSMFSに移行したいテラバイトのデータを持っている場合、これらの料金は急速に増加する可能性があります**。(そうだよね!:thinking:)

In this blog post I show how to write historical feature data directly into S3, which is the backbone of the SMFS offline store. 
このブログ記事では、SMFSオフラインストアのバックボーンであるS3に歴史的な特徴データを直接書き込む方法を示します。
Using this methodology circumvents the ingestion APIs and saves costs substantially. 
この方法論を使用することで、取り込みAPIを回避し、コストを大幅に削減できます。


Q: I’m only here for the code, where can I find it?
A: [Here](https://github.com/marshmellow77/sm-feature-store-backfill/) you go :)
(サンプルコードはここにあるよ的なことが書いてる??)

<!-- ここまで読んだ! -->

## A quick back-of-the-envelope cost calculation 簡易コスト計算

This notebook is a good example showing how to ingest data into SMFS using the dedicated ingestion API. 
このノートブックは、**専用のingestion API**(Sagemaker Python SDKのやつ!)を使用してSMFSにデータを取り込む方法を示す良い例です。
According to the Amazon SageMaker Pricing website, users will be charged $1.25 per million write requests units (this is for region US East N. Virginia— different charges may apply in different regions). 
Amazon SageMakerの料金ウェブサイトによると、**ユーザーは100万件の書き込みリクエスト単位ごとに$1.25が請求**されます（これは米国東部バージニア州の料金であり、地域によって異なる料金が適用される場合があります）。
(そうそう...!:thinking:)

One write request is equivalent to 1KB of data, so therefore each Gigabyte (= 1 million KB) costs $1.25 to write into SMFS. 
1件の書き込みリクエストは1KBのデータに相当するため、したがって1ギガバイト（= 100万KB）をSMFSに書き込むのに$1.25かかります。
I have spoken to customers that have Terabytes of historical feature data who just want to backfill the SMFS offline store. 
私は、**SMFSオフラインストアをバックフィルしたいだけのテラバイトの履歴機能データを持つ顧客**と話をしました。
They would be charged thousands of USD if they were to use the API for backfilling this data. 
彼らは、このデータを**バックフィルするためにAPIを使用すると、数千ドルが請求される**ことになります。
In contrast, putting files directly into S3 is much cheaper ($0.005 per 1,000 files in US East N. Virginia). 
**対照的に、ファイルを直接S3に置く方がはるかに安価**です（米国東部バージニア州では1,000ファイルあたり$0.005）。

<!-- ここまで読んだ! -->

## How to write feature data directly into S3 S3に特徴データを直接書き込む方法

The game plan is straightforward: We will create a feature group, amend the corresponding dataset, and save it directly in S3 according to the SMFS offline store data format. 
計画は簡単です：私たちは特徴グループを作成し、対応するデータセットを修正し、**[SMFSオフラインストアデータ形式](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-offline.html)に従ってそれを直接S3に保存**します。 
As a result this dataset will then become available in the SMFS offline store.
その結果、このデータセットはSMFSオフラインストアで利用可能になります。
(よしよしよし...!:thinking:)

<!-- ここまで読んだ! -->

### Preparing the data データの準備

For this exercise I will use a synthetic dataset that represents credit card transactions. 
この演習では、クレジットカード取引を表す合成データセットを使用します。
The dataset is publicly available in the SageMaker Sample S3 bucket: 
データセットは、SageMaker Sample S3バケットで公開されています。

Some of the columns are of type object and we need to convert them to strings so that SMFS accepts the data (see this page for SMFS supported data types): 
いくつかの列はオブジェクト型であり、**SMFSがデータを受け入れるためにそれらを文字列に変換する必要**があります（SMFSがサポートするデータ型についてはこのページを参照してください）。

Each dataset in SMFS requires a timestamp for each data point. 
SMFSの各データセットには、各データポイントのタイムスタンプが必要です。

Since our dataset doesn’t have a timestamp, we need to add it manually: 
私たちのデータセットにはタイムスタンプがないため、手動で追加する必要があります。

### Creating a feature group 特徴グループの作成

The dataset is now ready and we can create the corresponding feature group. 
データセットは準備が整い、対応する特徴グループを作成できます。
To do so, we first define the feature group like so: 
そのために、まず次のように特徴グループを定義します。

Now we are ready to create the feature group. 
これで、特徴グループを作成する準備が整いました。
Note that creating the feature group is different from ingesting the data and will not incur charges. 
**特徴グループを作成することは、データを取り込むこととは異なり、料金は発生しません。**(ほうほう...!:thinking:)
The feature group will be registered with SMFS, but it will remain empty until we fill it with data. 
特徴グループはSMFSに登録されますが、データで埋めるまで空のままです。(うんうん...!:thinking:)
We also need to provide the name of the column that uniquely identifies a record, i.e. the primary key and the name of the column that contains the timestamp for each record: 
また、レコードを一意に識別する列の名前、すなわちプライマリキーと各レコードのタイムスタンプを含む列の名前を提供する必要があります。

Up until this point we have followed the same steps as as you would when ingesting data into SMFS via the API. 
ここまでの段階では、APIを介してSMFSにデータを取り込む際と同じ手順を踏んできました。(うんうん...!:thinking:)
Now we will ingest our data directly into S3. 
これから、データを直接S3に取り込みます。

<!-- ここまで読んだ! -->

### Writing the data into S3 S3へのデータ書き込み

The key to writing data into S3 so it becomes available in SMFS is this documentation. 
S3にデータを書き込んでSMFSで利用可能にするための鍵は、[このドキュメント](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-offline.html)です。(はいはい、オフラインストアのデータ形式についてのドキュメントね...!:thinking:)
We are in particular interested in the naming convention that is used to organise files in the offline store: 
私たちは特に、**オフラインストアでファイルを整理するために使用される命名規則に**興味があります。

```
s3://<bucket-name>/<customer-prefix>/<account-id>/sagemaker/<aws-region>/offline-store/<feature-group-name>-<feature-group-creation-time>/data/<year>/<month>/<day>/<hour>/<file-name>
```

To reconstruct this corresponding S3 file path we only need the table name, as well as year, month, day, and hour of the event timestamp we created earlier: 
この対応するS3ファイルパスを再構築するには、テーブル名と、以前に作成したイベントのタイムスタンプの年、月、日、時間が必要です。

It is important to note that additional fields will be created by SMFS when using the ingestion API: 
取り込みAPIを使用する際に、**SMFSによって追加のフィールドが作成されることに注意することが重要**です。(うんうん、確か3つくらいあったよね...!:thinking:)
Because we aren’t using the API, we need to add those additional fields manually. 
APIを使用していないため、これらの追加フィールドを手動で追加する必要があります。
The two timestamps (api_invocation_time and write_time) are different from the event timestamp we created earlier. 
2つのタイムスタンプ（api_invocation_timeとwrite_time）は、以前に作成したイベントのタイムスタンプとは異なります。
However, for demonstration purposes it’s OK to reuse the same timestamp: 
ただし、デモンストレーションの目的では、同じタイムスタンプを再利用しても問題ありません。

To create a valid file name for the data we can concatenate the event time and a random 16 alpha numeric code. 
データの有効なファイル名を作成するために、イベント時間とランダムな16桁の英数字コードを連結することができます。
As a final step we can now save the data as a parquet file in S3: 
最後のステップとして、データをS3にparquetファイルとして保存できます。

<!-- ここまで読んだ! -->

### Checking if the ingestion was successful データ取り込みが成功したかの確認

The SMFS offline store is accessed via Athena queries, so the quickest way to check if the data ingestion was successful is to write an Athena SQL query that retrieves the data from the feature store:
SMFSオフラインストアはAthenaクエリを介してアクセスされるため、**データ取り込みが成功したかを確認する最も迅速な方法は、フィーチャーストアからデータを取得するAthena SQLクエリを書くこと**です。(うんうん)


If the ingestion was successful, the dataset retrieved from feature store will be the same as the dataset we have uploaded.
データ取り込みが成功していれば、フィーチャーストアから取得したデータセットは、私たちがアップロードしたデータセットと同じになります。

## Conclusion 結論

We have successfully backfilled the SageMaker Offline Feature Store with historical data without using the ingestion API. 
私たちは、**取り込みAPIを使用せずに、SageMakerオフラインフィーチャーストアに履歴データを正常にバックフィル**しました。
We did so by amending the dataset, setting up the appropriate S3 folder structure, and uploading the dataset directly to S3. 
これは、データセットを修正し、適切なS3フォルダ構造を設定し、データセットを直接S3にアップロードすることによって行いました。
This methodology allows users to save the ingestion API charges, which can be substantial for large amounts of historical data. 
この方法論により、**ユーザーは取り込みAPIの料金を節約でき、大量の履歴データに対してはかなりの額になる可能性**があります。

[EDIT on 29/04/2021: A follow-up blog post discussing more advanced scenarios can be found here] 
[2021年4月29日の編集: より高度なシナリオについて議論したフォローアップブログ記事はこちらにあります]

<!-- ここまで読んだ! -->

