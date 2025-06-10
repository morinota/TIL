# Q&A for Ingesting Historical Data into SageMaker Feature Store SageMaker Feature Storeへの履歴データの取り込みに関するQ&A


Answering questions on how to ingest data into SageMaker Offline Feature Store by directly writing into S3
S3に直接書き込むことによって、SageMaker Offline Feature Storeにデータを取り込む方法に関する質問に答えます。

In a previous blog post I showed how to ingest data into SageMaker Offline Feature Store by writing directly into S3. 
以前のブログ投稿では、S3に直接書き込むことによってSageMaker Offline Feature Storeにデータを取り込む方法を示しました。
I have received feedback and suggestions for advanced scenarios which I will discuss in this Q&A.
私は、このQ&Aで議論する高度なシナリオに関するフィードバックと提案を受け取りました。

## Q: How can I ingest historical data where feature records have different timestamps? Q: 異なるタイムスタンプを持つ特徴レコードの履歴データをどのように取り込むことができますか？

I simplified my previous example by assigning each feature record the same timestamp. 
私は、**各特徴レコードに同じタイムスタンプを割り当てる**ことで、前の例を簡略化しました。(まあバッチのfeature pipelineによるingestの場合は、大抵全レコードのevent_timeは同じになりそうだよね...!:thinking:)
However, in a real-word scenario it is much more likely that historical feature records have different timestamps. 
**しかし、実際のシナリオでは、履歴の特徴レコードが異なるタイムスタンプを持つ可能性がはるかに高い**です。(まあ、すでにどこかに保存されてる特徴量レコードをSageMaker Feature Storeに取り込む場合、全然event_timeが異なるレコードを一気にingestすることも多いか...!:thinking:)
In that case we can use the same approach, but we have to be a bit more sophisticated when it comes to setting up the S3 folder structure and we have to split the dataset according to their timestamps. 
その場合、同じアプローチを使用できますが、**S3フォルダ構造の設定に関してはもう少し洗練させる必要があり、データセットをタイムスタンプに従って分割する必要があります**。(うんうん、わかる...!:thinking:)


Let’s start by creating a feature dataset with different timestamps per record: 
まず、各レコードに異なるタイムスタンプを持つ特徴データセットを作成しましょう：

This code creates appends random timestamps between 1 Jan 2021, 8pm and 2 Jan 2021, 10am to the dataset. 
このコードは、2021年1月1日午後8時から2021年1月2日午前10時の間のランダムなタイムスタンプをデータセットに追加します。

The documentation on the S3 folder structure for the Offline Store tells us that we have to create a different folder for each unique combination of year, month, day, and hour of those timestamps. 
**オフラインストアのS3フォルダ構造に関するドキュメントによれば、これらのタイムスタンプの年、月、日、時間のユニークな組み合わせごとに異なるフォルダを作成する必要があります**。(うんうん、そうだよね...!:thinking:)
It also tells us that the filename for each feature subset requires the timestamp of the latest timestamp in the file: 
また、**各特徴サブセットのファイル名には、ファイル内の最新のタイムスタンプのタイムスタンプが必要**であることも教えてくれます。(あ、parquetファイルの名前にもタイムスタンプが必要なんだ...!:thinking:)

```sh
s3:://<bucket-name>/<customer-prefix>/<account-id>/sagemaker/<aws-region>/offline-store/<feature-group-name>-<feature-group-creation-time>/data/year=<event-time-year>/month=<event-time-month>/day=<event-time-day>/hour=<event-time-hour>/_<timestamp_of_latest_event_time_in_file>_<16-random-alphanumeric-digits->.parquet
```

To accomplish this we need to create a key for each record in the dataset. 
これを達成するために、**データセット内の各レコードに対してキーを作成する**必要があります。
This key will be in format YYYY-MM-DD-HH, representing the year, month, day, and hour of the timestamp for this record. 
このキーは、**YYYY-MM-DD-HH形式で、レコードのタイムスタンプの年、月、日、時間を表します**。(うんうん、ディレクトリ構造を作るためのキーだね...!:thinking:)
We then group together all feature records with the same keys: 
次に、同じキーを持つすべての特徴レコードをグループ化します。

![]()

For each subset we also need to identify the corresponding filename. 
**各サブセットに対して、対応するファイル名を特定**する必要があります。(ここ面倒くさそう...!:thinking:)
To do so, we need to identify the latest timestamp within each subset. 
そのためには、各サブセット内の最新のタイムスタンプを特定する必要があります。
In the example shown above, the filename for subset with key 2021–01–01–22 would start with "_20210101224453__", since the latest entry in this subset is from 22:44:53. 
上記の例では、キー2`021–01–01–22`を持つサブセットのファイル名は"_20210101224453__"で始まります。これは、このサブセットの最新のエントリが22:44:53からのものであるためです。(うんうん、最新のevent_timeをファイル名に入れる必要がある...!:thinking:)

The following code generates the keys as well as S3 paths and filenames for each subset: 
以下のコードは、各サブセットのキー、S3パス、およびファイル名を生成します。

To split the dataset according to their timestamp keys and save them to S3 in the corresponding S3 path we can simply leverage the groupby() method of pandas: 
データセットをタイムスタンプキーに従って分割し、対応するS3パスにS3に保存するには、pandasの**groupby()メソッドを単純に利用できます**。

### Conclusion 結論

In this example we have ingested historical feature records with different timestamps into SageMaker Offline Feature Store. 
この例では、異なるタイムスタンプを持つ履歴の特徴レコードをSageMaker Offline Feature Storeに取り込みました。
We have split the data according to the feature record timestamps, created S3 paths according to the documentation, and stored each subset in its corresponding S3 location. 
私たちは、特徴レコードのタイムスタンプに従ってデータを分割し、ドキュメントに従ってS3パスを作成し、各サブセットを対応するS3ロケーションに保存しました。
A complete example with code can be found in this notebook. 
コードを含む完全な例は、このノートブックにあります。

<!-- ここまで読んだ! -->

## Q: I have several versions for each feature record. I want to ingest the historical feature records into the Offline Store, but also have the latest version of each feature record synced with the Online Store. How do I do that?
Q: 各フィーチャーレコードに複数のバージョンがあります。過去のフィーチャーレコードをオフラインストアに取り込みたいのですが、**各フィーチャーレコードの最新バージョンもオンラインストアと同期させたい**です。どうすればよいですか？
(そうか、本来はこれをやってくれるのがPutRecord APIだからか...!:thinking:)

In this scenario we will have to identify the latest version of each feature record based on the event timestamp. 
このシナリオでは、イベントのタイムスタンプに基づいて各フィーチャーレコードの最新バージョンを特定する必要があります。
We will then backfill all versions older than the latest one by writing those records directly into S3. 
次に、**最新のものより古いすべてのバージョンをS3に直接書き込むことでバックフィル**します。
The subset with the latest records we will ingest using the regular ingestion API. 
**最新のレコードを含むサブセットは、通常の取り込みAPIを使用して取り込みます**。(はいはいなるほどね...!:thinking:)
In the end we will have the latest version of each record in the online and the offline feature store. 
最終的に、**オンラインストアとオフラインストアの両方に各レコードの最新バージョンが存在する**ことになります。
All other (historical) records will be available in the offline store only.
他のすべての（過去の）レコードはオフラインストアにのみ存在します。(これはFeature Storeとしてあるべき姿のはず...!:thinking:)

Let’s start by creating a dataset to reflect this scenario. 
このシナリオを反映するデータセットを作成することから始めましょう。
The code below creates 3 records per transaction, each with a different timestamp:
以下のコードは、各トランザクションごとに異なるタイムスタンプを持つ3つのレコードを作成します。

The resulting dataset has 6,000 records, three for each transaction. 
結果として得られるデータセットには6,000レコードがあり、各トランザクションに対して3つのレコードがあります。
Now we want to split the data into two groups:
さて、**データを2つのグループに分割**したいと思います。

The first subset (_dfonline) contains the latest version for each transaction. 
最初のサブセット（_dfonline）は、各トランザクションの最新バージョンを含みます。
This one we will ingest using the API call. 
このサブセットはAPIコールを使用して取り込みます。
The second subset (_dfoffline) contains the older versions of each feature record. 
2つ目のサブセット（_dfoffline）は、各フィーチャーレコードの古いバージョンを含みます。
This one we will ingest directly into S3 in the same way as above.
このサブセットは、上記と同様にS3に直接取り込みます。

![splitting feature data into historical and current subsets]()

Because the code for populating the offline store is the same as above, I won’t go through it again here, but you can find it in this notebook. 
オフラインストアをポピュレートするためのコードは上記と同じなので、ここでは再度説明しませんが、このノートブックで見つけることができます。
One difference I want to point out explicitly is that when creating the feature group we need to make sure that the online store is enabled:
私が明示的に指摘したい違いは、フィーチャーグループを作成する際にオンラインストアが有効になっていることを確認する必要があるということです。

Once the S3 backfilling is complete we can just ingest the latest version for each feature record with the API. 
S3のバックフィルが完了したら、APIを使用して各フィーチャーレコードの最新バージョンを取り込むことができます。
This will write the subset into the online store as well as the offline store:
これにより、サブセットがオンラインストアとオフラインストアの両方に書き込まれます。

Writing to the online store is immediate and we can test it right away by calling the GetRecord API:
オンラインストアへの書き込みは即時であり、GetRecord APIを呼び出すことですぐにテストできます。

Writing to the offline store via the API takes a few minutes. 
APIを介してオフラインストアに書き込むには数分かかります。
After waiting for ~5–10 minutes, we can test whether the offline store is now populated correctly:
約5〜10分待った後、オフラインストアが正しくポピュレートされているかどうかをテストできます。

If everything worked correctly, you should see three records, two of which we have ingested by writing to S3 directly and one via the API:
すべてが正しく機能していれば、3つのレコードが表示されるはずで、そのうちの2つはS3に直接書き込むことで取り込み、1つはAPIを介して取り込んだものです。

### Conclusion 結論

In this section we have backfilled historical feature records into the offline store by writing directly to S3. 
このセクションでは、過去のフィーチャーレコードをS3に直接書き込むことでオフラインストアにバックフィルしました。
We have also synced the current version of the feature records with the online store by using the ingestion API. 
また、取り込みAPIを使用してフィーチャーレコードの現在のバージョンをオンラインストアと同期させました。
In the end we have all feature records in the offline store and the most current version in the online store. 
最終的に、**オフラインストアにはすべてのフィーチャーレコードがあり、オンラインストアには最新のバージョンがあります**。
The entire code for this example can be found in this notebook.
この例の全コードはこのノートブックにあります。

Thanks to everyone who reached out with feedback and suggestions. 
フィードバックや提案をいただいた皆様に感謝します。
And if you still have any questions or feedback, please feel free to reach out.
まだ質問やフィードバックがある場合は、お気軽にご連絡ください。

Written By
著者

<!-- ここまで読んだ! -->
