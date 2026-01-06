## CHAPTER 11: Inference Pipelines 推論パイプライン

Inference pipelines define the type of AI system you are building. 
推論パイプラインは、構築しているAIシステムの種類を定義します。

Batch inference pipelines are batch AI systems, online inference pipelines are real-time AI systems, and agentic workflows are LLM-powered AI systems. 
バッチ推論パイプラインはバッチAIシステムであり、オンライン推論パイプラインはリアルタイムAIシステムであり、エージェントワークフローはLLM（大規模言語モデル）駆動のAIシステムです。

An inference pipeline is a program that acquires inference data, applies transformations to the input data to produce one or more feature vectors, and then feeds the feature vector(s) to one or more models that output predictions. 
推論パイプラインは、推論データを取得し、入力データに変換を適用して1つ以上の特徴ベクトルを生成し、その後、特徴ベクトルを1つ以上のモデルに供給して予測を出力させるプログラムです。

Inference pipelines can be anything from a batch/streaming/embedded program, to a network service with SLOs, to an agent that uses LLMs and tools to achieve a goal. 
推論パイプラインは、バッチ/ストリーミング/組み込みプログラムから、SLO（サービスレベル目標）を持つネットワークサービス、LLMやツールを使用して目標を達成するエージェントまで、さまざまな形態を取ることができます。

Inference pipelines log their inputs and outputs so that you can monitor and debug their performance. 
推論パイプラインは、その入力と出力をログに記録し、パフォーマンスを監視およびデバッグできるようにします。

This chapter covers challenges in writing batch, online, embedded, and streaming inference programs. 
この章では、バッチ、オンライン、組み込み、ストリーミングの推論プログラムを書く際の課題について説明します。

Agents and LLM workflows are covered in Chapter 12. 
エージェントとLLMワークフローについては、第12章で説明します。

You will learn how to design batch inference pipelines and scale them out with PySpark. 
バッチ推論パイプラインを設計し、PySparkを使用してスケールアウトする方法を学びます。

You will learn how to write online inference pipelines that retrieve context/history from the feature store and how to deploy models in model-serving infrastructure behind a deployment API. 
フィーチャーストアからコンテキスト/履歴を取得するオンライン推論パイプラインを書く方法と、デプロイメントAPIの背後にあるモデル提供インフラストラクチャにモデルをデプロイする方法を学びます。

You will learn how to embed a model in a stream-processing application and write a user interface for your AI system in Python. 
ストリーム処理アプリケーションにモデルを埋め込み、PythonでAIシステムのユーザーインターフェースを書く方法を学びます。

###### Batch Inference Pipelines バッチ推論パイプライン

Batch inference pipelines make non-time-critical predictions, run on a schedule, and output predictions to some kind of inference store, from which consumers asynchronously retrieve their predictions. 
バッチ推論パイプラインは、時間に敏感でない予測を行い、スケジュールに従って実行し、何らかの推論ストアに予測を出力し、そこから消費者が非同期的に予測を取得します。

They typically retrieve their inference data by querying the feature store. 
通常、フィーチャーストアをクエリして推論データを取得します。

For example, in the air quality system from Chapter 3, our daily batch inference pipeline reads weather forecast data from the feature store, makes air quality predictions, and logs predictions/features to the feature store. 
例えば、第3章の空気質システムでは、私たちの日次バッチ推論パイプラインがフィーチャーストアから天気予報データを読み込み、空気質の予測を行い、予測/特徴をフィーチャーストアにログします。

The _inference store is any data store that stores predictions from batch inference pipelines._ 
推論ストアとは、バッチ推論パイプラインからの予測を保存する任意のデータストアです。

It can be anything from a database to a feature store, an object store, or an event-streaming platform. 
データベースからフィーチャーストア、オブジェクトストア、イベントストリーミングプラットフォームまで、何でも可能です。

Your batch inference pipeline does not have to write to an inference store—the air quality system could have just published its dashboard and not written the predictions (and not published a hindcast). 
バッチ推論パイプラインは推論ストアに書き込む必要はありません。空気質システムはダッシュボードを公開するだけで、予測を書き込まなかった（および過去の予測を公開しなかった）可能性があります。

But in production systems, your dashboards are typically created from predictions in the inference store, while operational systems (like the Spotify Discovery Weekly example from Chapter 1) and monitoring systems (hindcasts for our air quality system) also consume predictions in the inference store. 
しかし、実稼働システムでは、ダッシュボードは通常、推論ストアの予測から作成され、運用システム（第1章のSpotify Discovery Weeklyの例のように）や監視システム（空気質システムの過去の予測）も推論ストアの予測を消費します。

A typical batch inference pipeline performs the following steps: 
典型的なバッチ推論パイプラインは、以下のステップを実行します。

1. Read/query precomputed inference (precomputed feature) data with a feature view from lakehouse tables. 
1. レイクハウステーブルからフィーチャービューを使用して、事前計算された推論（事前計算された特徴）データを読み取る/クエリします。

2. Apply MDTs to the inference data. 
2. 推論データにMDT（モデル駆動型テスト）を適用します。

3. Call model.predict(..) with the transformed inference data. 
3. 変換された推論データを使用してmodel.predict(..)を呼び出します。

The inference data is feature data that is used to make predictions. 
推論データは、予測を行うために使用される特徴データです。

How you query the inference data depends on what type of batch inference problem you are solving. 
推論データをクエリする方法は、解決しているバッチ推論問題の種類によって異なります。

In the following sections, we describe batch inference pipelines that make predictions: 
次のセクションでは、予測を行うバッチ推論パイプラインについて説明します。

- Based on a time range of inference data (such as data that arrived yesterday or forecasts for the next seven days) 
- 推論データの時間範囲に基づいて（昨日到着したデータや次の7日間の予測など）

- For entities, such as predictions for all customers or predictions for all products in stock 
- エンティティに対して、すべての顧客の予測や在庫のすべての製品の予測など

We will also look at how to scale out batch inference pipelines using PySpark and how to refactor your data model to improve performance when writing to lakehouse tables. 
また、PySparkを使用してバッチ推論パイプラインをスケールアウトする方法や、レイクハウステーブルに書き込む際のパフォーマンスを向上させるためにデータモデルをリファクタリングする方法についても見ていきます。

###### Batch Predictions for a Time Range 時間範囲に対するバッチ予測

Figure 11-1 shows how you can use a feature view to retrieve both training data and batches of inference data for time ranges. 
図11-1は、フィーチャービューを使用して、時間範囲のトレーニングデータとバッチの推論データの両方を取得する方法を示しています。

Each batch of data is read using a query (see Chapter 5). 
各データのバッチは、クエリを使用して読み取られます（第5章を参照）。

In v1, the query includes start and end times for the training data. 
v1では、クエリにはトレーニングデータの開始時刻と終了時刻が含まれています。

In v2, the query also includes a filter for data where the country is the US. 
v2では、クエリには国が米国であるデータのフィルタも含まれています。

Note that if you train a model with only data from the `US, your inference data should also retrieve` only data from the US. 
モデルを米国のデータのみでトレーニングした場合、推論データも米国のデータのみを取得する必要があります。

The same filter should be applied in both training and inference. 
同じフィルタは、トレーニングと推論の両方に適用する必要があります。

This applies to both batch and online inference. 
これは、バッチ推論とオンライン推論の両方に適用されます。

_Figure 11-1. With a feature view, you can read a batch of inference data that has arrived in a given time range, such as the week of March 17–24, 2025._ 
_図11-1. フィーチャービューを使用すると、2025年3月17日から24日の週など、特定の時間範囲に到着した推論データのバッチを読み取ることができます。_

The same feature view (name and version) that created the training data for our model is used to read batch inference data for the model as follows: 
私たちのモデルのトレーニングデータを作成したのと同じフィーチャービュー（名前とバージョン）が、モデルのバッチ推論データを読み取るために使用されます。

```  
model_mr = model_registry.get_model(name="cc_fraud", version=1)  
model_dir = model_mr.download()  
model.load_model(model_dir + "/cc_fraud.json")  
fv = model_mr.get_feature_view()  
df = fv.get_batch_data(start_time ="YYYYMMDD HH:mm", end_time="YYYYMMDD HH:mm")  
predictions = model.predict(df)
```  
開始時刻と終了時刻のパラメータは、文字列またはdatetimeオブジェクトのいずれかにすることができます。

The feature view ensures the same filters are applied when retrieving inference data using a training_dataset_version. 
フィーチャービューは、training_dataset_versionを使用して推論データを取得する際に同じフィルタが適用されることを保証します。

When you get the feature view from the model, the model returns a feature view that has been initialized with the training_dataset_version registered with the model. 
モデルからフィーチャービューを取得すると、モデルに登録されたtraining_dataset_versionで初期化されたフィーチャービューが返されます。

That means any additional filters used when creating the model’s training dataset will also be applied when reading inference data. 
これは、モデルのトレーニングデータセットを作成する際に使用された追加のフィルタも、推論データを読み取る際に適用されることを意味します。

The filters are applied when reading either batch or online inference data with the feature view. 
フィルタは、フィーチャービューを使用してバッチまたはオンラインの推論データを読み取る際に適用されます。

For example, in your training pipeline, you can attach a filter, such as one that says the country is the US, and then explicitly store the training_dataset_version with the model as follows: 
例えば、トレーニングパイプラインで、国が米国であるというフィルタを添付し、次のようにモデルとともにtraining_dataset_versionを明示的に保存できます。

```  
features, labels = feature_view.training_data(train_start="...", \  
train_end="...", extra_filter=(fg.gender == "Male"))  
training_dataset_version = feature_view.get_last_accessed_training_dataset()  
…  
model = mr.python.create_model(...  
feature_view=feature_view,  
training_dataset_version=training_dataset_version)
```  
トレーニングデータを読み取る際、フィーチャービューはクエリの追加メタデータを保存するためのtraining_dataset_versionも作成します。

The query metadata includes the commit_ids of the source feature groups and any additional filters applied at training data creation time. 
クエリメタデータには、ソースフィーチャーグループのcommit_idsや、トレーニングデータ作成時に適用された追加のフィルタが含まれます。

The training_dataset_version identifies the training data used. 
training_dataset_versionは、使用されたトレーニングデータを特定します。



to train a model. 
モデルをトレーニングするために。

When you register a model in the model registry, you can either provide its training_dataset_version explicitly, as shown in the previous example, or just register the `feature_view, in which case it registers the most recent` `train` `ing_dataset_version created by that feature view.`
モデルレジストリにモデルを登録する際、前の例に示したように、トレーニングデータセットバージョンを明示的に提供するか、単に`feature_view`を登録することができます。この場合、最も最近作成された`train` `ing_dataset_version`がそのフィーチャービューによって登録されます。

``` 
When you implement the batch inference pipeline, you download the model from the model registry and get the `feature_view from the downloaded model. 
バッチ推論パイプラインを実装する際、モデルレジストリからモデルをダウンロードし、ダウンロードしたモデルから`feature_view`を取得します。

Before the` model returns the feature_view, it initializes it with the training_dataset_version registered with the model. 
モデルが`feature_view`を返す前に、モデルに登録されたトレーニングデータセットバージョンで初期化します。

You can explicitly initialize the feature view with a ``` training_dataset_version for batch inference by calling: 
バッチ推論のために、`training_dataset_version`でフィーチャービューを明示的に初期化することができます。

feature_view.init_batch_scoring( 
feature_view.init_batch_scoring( 

training_dataset_version=training_dataset_version 
training_dataset_version=training_dataset_version 

) 
) 

Or, in an online inference pipeline, call this initialization function: 
また、オンライン推論パイプラインでは、この初期化関数を呼び出します。

``` 
feature_view.init_serving(training_dataset_version=training_dataset_version) 
feature_view.init_serving(training_dataset_version=training_dataset_version) 

If you are using Hopsworks’ model registry, you probably won’t need to call the previ‐ ously listed initialization methods (the examples shown so far have not needed to ini‐ tialize feature views, as they are automatically initialized when retrieved). 
Hopsworksのモデルレジストリを使用している場合、以前にリストされた初期化メソッドを呼び出す必要はないでしょう（これまでに示した例では、フィーチャービューは自動的に初期化されるため、初期化する必要はありません）。

However, if you are using a different model registry than Hopsworks, you will need to call them. 
ただし、Hopsworksとは異なるモデルレジストリを使用している場合は、それらを呼び出す必要があります。

If you don’t initialize the feature_view, its training_dataset_version defaults to 1. 
フィーチャービューを初期化しない場合、そのトレーニングデータセットバージョンはデフォルトで1になります。

###### Batch Predictions for Entities 
###### エンティティのバッチ予測

Lakehouse tables that store the offline feature data for batch inference are often parti‐ tioned by time (e.g., hour or day, depending on the incoming data velocity). 
バッチ推論のためのオフラインフィーチャーデータを保存するレイクハウステーブルは、しばしば時間（例：時間または日）でパーティション分けされています（受信データの速度に応じて）。

This ena‐ bles efficient querying of feature data by time ranges. 
これにより、時間範囲によるフィーチャーデータの効率的なクエリが可能になります。

However, if your table is partitioned by time and you want to retrieve either the latest feature data for an entity or feature data for an entity over a specific time range, this will process all rows in the table. 
ただし、テーブルが時間でパーティション分けされていて、エンティティの最新のフィーチャーデータまたは特定の時間範囲のエンティティのフィーチャーデータを取得したい場合、テーブル内のすべての行を処理します。

A full table scan is very expensive if the table contains a large number of rows. 
テーブルに大量の行が含まれている場合、フルテーブルスキャンは非常に高価です。

For example, in our credit card system, if you want to read the latest transaction for each credit card, you could run the following code that returns the most recent trans‐ action for each credit card: 
例えば、私たちのクレジットカードシステムでは、各クレジットカードの最新の取引を読み取りたい場合、次のコードを実行して各クレジットカードの最も最近の取引を返すことができます。

``` 
df = feature_view.get_batch_data(latest_features=True) 
df = feature_view.get_batch_data(latest_features=True) 
```

If you have a more complex logic for retrieving inference data, you may need to exe‐ cute a SQL query directly on the lakehouse tables. 
推論データを取得するためのより複雑なロジックがある場合、レイクハウステーブルに対して直接SQLクエリを実行する必要があるかもしれません。

For example, the following query reads the three most recent transactions for each credit card and then joins features from the merchants table (using a temporal join), including a new avg_daily_spend feature in merchants_fg: 
例えば、次のクエリは各クレジットカードの3つの最も最近の取引を読み取り、その後、マーチャントテーブルからのフィーチャーを結合します（時間的結合を使用）、merchants_fgに新しいavg_daily_spendフィーチャーを含めます。

``` 
WITH latest_transactions AS ( 
WITH latest_transactions AS ( 

SELECT cc_num, ts, amount, merchant_id 
SELECT cc_num, ts, amount, merchant_id 
```

``` 
FROM ( 
FROM ( 

SELECT 
SELECT 

cc_num, ts, amount, merchant_id, 
cc_num, ts, amount, merchant_id, 

ROW_NUMBER() OVER (PARTITION BY cc_num ORDER BY ts DESC) AS rn 
ROW_NUMBER() OVER (PARTITION BY cc_num ORDER BY ts DESC) AS rn 

FROM cc_trans_fg 
FROM cc_trans_fg 
) t 
) t 

WHERE rn <= 3 
WHERE rn <= 3 
) 
) 

SELECT 
SELECT 

t.cc_num, 
t.cc_num, 

t.ts, 
t.ts, 

t.amount, 
t.amount, 

t.merchant_id, 
t.merchant_id, 

m.avg_daily_spend 
m.avg_daily_spend 

FROM latest_transactions t 
FROM latest_transactions t 

ASOF LEFT JOIN merchants_fg m 
ASOF LEFT JOIN merchants_fg m 

ON t.merchant_id = m.merchant_id 
ON t.merchant_id = m.merchant_id 

AND m.merchants_ts <= t.ts 
AND m.merchants_ts <= t.ts 

ORDER BY t.cc_num, t.ts DESC; 
ORDER BY t.cc_num, t.ts DESC; 
```

The query processes all rows in cc_trans_fg (in a full table scan). 
このクエリは、cc_trans_fg内のすべての行を処理します（フルテーブルスキャンで）。

As cc_trans_fg is a lakehouse table, you can directly add a Z-order secondary index to a column (in Apache Hudi and Delta Lake), ordering rows within a partition. 
cc_trans_fgはレイクハウステーブルであるため、カラムにZ-orderセカンダリインデックスを直接追加することができます（Apache HudiおよびDelta Lakeで）、パーティション内の行を順序付けます。

Similarly, in Apache Iceberg, you can add sort ordering to a partitioned table. 
同様に、Apache Icebergでは、パーティション化されたテーブルにソート順を追加できます。

However, all files will still be read with this query. 
ただし、このクエリではすべてのファイルがまだ読み取られます。

A recent alternative for Delta Lake is to skip Hive-style parti‐ tioning and use liquid clustering to add a secondary index on cc_num, which may help improve query performance for queries based on `cc_num. 
Delta Lakeの最近の代替手段は、Hiveスタイルのパーティショニングをスキップし、cc_numにセカンダリインデックスを追加するためにリキッドクラスタリングを使用することです。これにより、`cc_num`に基づくクエリのパフォーマンスが向上する可能性があります。

However, you can only` define a single liquid-clustering index per table, so this can increase latency for quer‐ ies that filter by a time range. 
ただし、テーブルごとに単一のリキッドクラスタリングインデックスしか定義できないため、時間範囲でフィルタリングするクエリのレイテンシが増加する可能性があります。

But what if you don’t need to scan the tables to discover the entity IDs (and time‐ stamps) that you need for your predictions because you retrieved them from another data source? 
しかし、別のデータソースから取得したため、予測に必要なエンティティID（およびタイムスタンプ）を発見するためにテーブルをスキャンする必要がない場合はどうなりますか？

In that case, you can provide the entity IDs and timestamps directly in a _Spine DataFrame. 
その場合、エンティティIDとタイムスタンプを直接_Spine DataFrameで提供できます。

We introduced Spine Groups in Chapter 5, and if your root feature_ group in a feature view is a Spine Group, you need to provide a DataFrame contain‐ ing the entity IDs and timestamps for the child feature groups. 
第5章でSpine Groupsを紹介しましたが、フィーチャービュー内のルートフィーチャーグループがSpine Groupである場合、子フィーチャーグループのエンティティIDとタイムスタンプを含むDataFrameを提供する必要があります。

It is your responsibil‐ ity to build the DataFrame containing the IDs. 
IDを含むDataFrameを構築するのはあなたの責任です。

For example, in our credit card fraud example, you might want to make a prediction for all the credit cards used at a merchant with merchant_id=12. 
例えば、私たちのクレジットカード詐欺の例では、merchant_id=12のマーチャントで使用されたすべてのクレジットカードの予測を行いたいかもしれません。

In this case, you would write code as follows: 
この場合、次のようにコードを書くことができます。

``` 
input_df = cc_transactions_fg.filter(Feature('merchant_id')==12)\ 
input_df = cc_transactions_fg.filter(Feature('merchant_id')==12)\ 
.select(['cc_num', 'merchant_id', 'ts']).read() 
.select(['cc_num', 'merchant_id', 'ts']).read() 

output_df = feature_view.get_batch_data(spine=input_df) 
output_df = feature_view.get_batch_data(spine=input_df) 

predictions = model.predict(output_df) 
predictions = model.predict(output_df) 
```

In this code snippet, we still have a full table scan of `transactions. 
このコードスニペットでは、`transactions`のフルテーブルスキャンがまだあります。

In reality, you only use Spine DataFrames if you have a more efficient way to read the required entity IDs (probably, from an external system). 
実際には、必要なエンティティIDを読み取るためのより効率的な方法がある場合にのみSpine DataFramesを使用します（おそらく外部システムから）。

###### Scaling Batch Inference with PySpark 
###### PySparkによるバッチ推論のスケーリング

What if you have billions or more rows of batch inference data, such that it doesn’t fit in memory on a single host? 
数十億行以上のバッチ推論データがあり、それが単一のホストのメモリに収まらない場合はどうしますか？

You can scale out batch inference with a distributed data processing framework like PySpark or Ray. 
PySparkやRayのような分散データ処理フレームワークを使用してバッチ推論をスケールアウトできます。

In Figure 11-2, we show how to scale out batch inference programs with Spark by having each Spark executor (a) download a local copy of the model from the model registry, (b) read a partition of the batch inference data from the feature groups (lakehouse tables), and (c) make predictions with the model and save them to an inference store (such as a feature group). 
図11-2では、各Sparkエグゼキュータが（a）モデルレジストリからモデルのローカルコピーをダウンロードし、（b）フィーチャーグループ（レイクハウステーブル）からバッチ推論データのパーティションを読み取り、（c）モデルで予測を行い、それを推論ストア（フィーチャーグループなど）に保存することで、Sparkを使用してバッチ推論プログラムをスケールアウトする方法を示しています。

_Figure 11-2. Distributed batch inference with PySpark and an embedded model (down‐_ _loaded from the model registry). Output predictions are stored in an inference store._ 
_図11-2. PySparkと埋め込まれたモデル（モデルレジストリからダウンロード）を使用した分散バッチ推論。出力予測は推論ストアに保存されます。_

In PySpark, it is also possible to read the model in the driver and then broadcast the serialized model to executors. 
PySparkでは、ドライバでモデルを読み取り、その後、シリアライズされたモデルをエグゼキュータにブロードキャストすることも可能です。

However, XGBoost models are not natively fully serial‐ izable using Python’s pickle or cloudpickle. 
ただし、XGBoostモデルはPythonのpickleやcloudpickleを使用してネイティブに完全にシリアライズ可能ではありません。

PyTorch and TensorFlow models are simi‐ larly problematic. 
PyTorchやTensorFlowモデルも同様に問題があります。

You could transform an XGBoost model into JSON and broadcast it to the workers, but instead we leverage the HopsFS FUSE client to broadcast a local path to all workers who can then load the model from their local FUSE directory (the model is read from HopsFS via the FUSE client): 
XGBoostモデルをJSONに変換してワーカーにブロードキャストすることもできますが、代わりにHopsFS FUSEクライアントを利用して、すべてのワーカーにローカルパスをブロードキャストし、ワーカーはその後ローカルFUSEディレクトリからモデルをロードできます（モデルはFUSEクライアントを介してHopsFSから読み取られます）。

``` 
model_name = "example_model" 
model_name = "example_model" 

mr_model= model_registry.get_model(name=model_name, version=1) 
mr_model= model_registry.get_model(name=model_name, version=1) 

fv = mr_model.get_feature_view() 
fv = mr_model.get_feature_view() 

model_dir = mr_model.download_model() # Download into hopsfs-FUSE client path 
model_dir = mr_model.download_model() # Hopsfs-FUSEクライアントパスにダウンロード 

model_path = f"{model_dir}/{model_name}.json" 
model_path = f"{model_dir}/{model_name}.json" 

broadcasted_model_path = spark.sparkContext.broadcast(model_path) 
broadcasted_model_path = spark.sparkContext.broadcast(model_path) 

@pandas_udf(returnType=FloatType()) 
@pandas_udf(returnType=FloatType()) 

def pred_udf(features: pd.Series) -> pd.Series: 
def pred_udf(features: pd.Series) -> pd.Series: 

xgb_model = xgb.XGBClassifier() 
xgb_model = xgb.XGBClassifier() 

xgb_model.load_model(broadcasted_model_path.value) 
xgb_model.load_model(broadcasted_model_path.value) 

feature_array = pd.DataFrame(features.tolist()).values 
feature_array = pd.DataFrame(features.tolist()).values 

predictions = xgb_model.predict(feature_array) 
predictions = xgb_model.predict(feature_array) 

return pd.Series(predictions, dtype=float) 
return pd.Series(predictions, dtype=float) 

yesterday=datetime.today() - timedelta(days=1) 
yesterday=datetime.today() - timedelta(days=1) 

df = fv.get_batch_data(start_date=yesterday, primary_key=True) 
df = fv.get_batch_data(start_date=yesterday, primary_key=True) 

df = df.select("id", pred_udf(struct(col("f1"), col("f2"))).alias("prediction")) 
df = df.select("id", pred_udf(struct(col("f1"), col("f2"))).alias("prediction")) 

# store inference results in an inference store feature group 
# 推論結果を推論ストアフィーチャーグループに保存 

fg = fs.get_or_create_feature_group(name="inference_store", version=1, 
fg = fs.get_or_create_feature_group(name="inference_store", version=1, 

description = "Inference store for predictions", 
description = "予測のための推論ストア", 

primary_key=["id"]) 
primary_key=["id"]) 

fg.insert(df) 
fg.insert(df) 
```

In this code snippet, the Spark executors all execute pred_udf as a Pandas UDF, load‐ ing the XGBoost model from the broadcast path. 
このコードスニペットでは、Sparkエグゼキュータはすべてpred_udfをPandas UDFとして実行し、ブロードキャストパスからXGBoostモデルをロードします。

Then xgb_model makes predictions by calling predict() on the Pandas DataFrame features. 
その後、xgb_modelはPandas DataFrameのフィーチャーに対してpredict()を呼び出して予測を行います。

The predictions are stored in a new prediction column that is added to the original features, and then they are written to an `inference_store feature group for later consumption. 
予測は元のフィーチャーに追加された新しい予測列に保存され、その後、後で使用するために`inference_storeフィーチャーグループに書き込まれます。

The perfor‐ mance of this code can be further improved by caching xgb_model, so that it is loaded once per Spark application, instead of once per partition. 
このコードのパフォーマンスは、xgb_modelをキャッシュすることでさらに改善でき、パーティションごとではなく、Sparkアプリケーションごとに1回だけロードされるようになります。

###### Data Modeling for Batch Inference 
###### バッチ推論のためのデータモデリング

Batch inference programs typically only process data from lakehouse tables. 
バッチ推論プログラムは通常、レイクハウステーブルからのデータのみを処理します。

It is impor‐ tant to understand certain properties of the open table formats (OTFs) to design more efficient data models. 
より効率的なデータモデルを設計するためには、オープンテーブルフォーマット（OTFs）の特定の特性を理解することが重要です。

For example, our real-time credit card fraud system could easily be modified to work as a batch AI system—every night, you schedule a batch inference program that identifies transactions from the previous day that are suspected of fraud. 
例えば、私たちのリアルタイムクレジットカード詐欺システムは、バッチAIシステムとして機能するように簡単に変更できます。毎晩、前日からの詐欺が疑われる取引を特定するバッチ推論プログラムをスケジュールします。

Many organizations start with batch predictions to gain organizational acceptance of AI, before moving on to building real-time AI systems. 
多くの組織は、リアルタイムAIシステムの構築に進む前に、AIの組織的な受け入れを得るためにバッチ予測から始めます。

When reports of credit card fraud arrive, weeks or months later, you run a Spark job to update the is_fraud col‐ umn value for affected rows in the cc_trans_fg table. 
クレジットカード詐欺の報告が数週間または数ヶ月後に届くと、影響を受けた行のcc_trans_fgテーブルのis_fraud列の値を更新するためにSparkジョブを実行します。

However, the job takes an inor‐ dinate amount of time to complete and updates a massive amount of data. 
ただし、そのジョブは完了するのに非常に長い時間がかかり、大量のデータを更新します。

Your ``` cc_trans_fg table has many billions of rows, but your Spark job is only updating a few 
あなたの`cc_trans_fg`テーブルには数十億行が含まれていますが、Sparkジョブはわずか数千行しか更新していません。

``` 
thousand rows. 
数千行です。

Why does it rewrite 25% of the Parquet files in the lakehouse table? 
なぜレイクハウステーブルの25%のParquetファイルを書き換えるのですか？



Lakehouse tables are not efficient for frequent, small updates. 
Lakehouseテーブルは、頻繁で小さな更新には効率的ではありません。

They suffer from write amplification, where updating a single row could cause an entire Parquet file (of anything from 128 MB to 1 GB) to be rewritten. 
それらは書き込み増幅の影響を受け、単一の行を更新することで、128 MBから1 GBの範囲の全体のParquetファイルが再書き込みされる可能性があります。

For this reason, OTFs support accumulating updates in row-oriented files (in Avro file format), and when a query arrives, it merges those Avro files with the Parquet files in a process known as merge on read. 
このため、OTFは行指向ファイル（Avroファイル形式）での更新の蓄積をサポートし、クエリが到着すると、これらのAvroファイルをParquetファイルとマージする「マージ・オン・リード」と呼ばれるプロセスを実行します。

As Avro files accumulate, your queries slow down because Avro is a row-oriented format and the queries are faster on columnar data. 
Avroファイルが蓄積されると、Avroが行指向形式であり、クエリが列指向データでより速いため、クエリが遅くなります。

To overcome this, a background compaction job or table service can be scheduled to run (once per hour/day/week) to merge the Avro files into the Parquet files and merge any small Parquet files. 
これを克服するために、AvroファイルをParquetファイルにマージし、小さなParquetファイルをマージするために、バックグラウンド圧縮ジョブまたはテーブルサービスを（1時間/日/週に1回）実行するようにスケジュールできます。

However, another way you can often reduce write amplification is by refactoring your data model to isolate updates to smaller tables. 
しかし、書き込み増幅を減らすもう一つの方法は、データモデルをリファクタリングして、更新を小さなテーブルに隔離することです。

In our credit card fraud example, we can move the is_fraud labels to cc_fraud_fg, a new child feature group of the root feature group, as shown in Figure 11-3. 
クレジットカード詐欺の例では、is_fraudラベルをcc_fraud_fgに移動できます。これは、ルートフィーチャーグループの新しい子フィーチャーグループです（図11-3に示されています）。

The new cc_fraud_fg table is connected by the t_id foreign key to the root feature group. 
新しいcc_fraud_fgテーブルは、t_id外部キーによってルートフィーチャーグループに接続されています。

_Figure 11-3. For batch inference, we refactor the labels into a new child feature group of the root feature group._ 
_図11-3. バッチ推論のために、ラベルをルートフィーチャーグループの新しい子フィーチャーグループにリファクタリングします。_

With this new data model, when fraud reports arrive, we only need to append them to `cc_fraud_fg`, which has no write amplification. 
この新しいデータモデルでは、詐欺報告が到着したとき、書き込み増幅がない`cc_fraud_fg`にそれらを追加するだけで済みます。

You will, however, have to add `cc_fraud_fg` to your feature view and update your feature pipeline to write labels to `cc_fraud_fg`. 
ただし、`cc_fraud_fg`をフィーチャービューに追加し、ラベルを`cc_fraud_fg`に書き込むためにフィーチャーパイプラインを更新する必要があります。

Queries for training data and batch inference data with your new feature view will have an additional join operation for the new table, adding some overhead to your query engine. 
新しいフィーチャービューを使用したトレーニングデータおよびバッチ推論データのクエリには、新しいテーブルに対する追加の結合操作があり、クエリエンジンにいくらかのオーバーヘッドが追加されます。

###### Batch Inference for Neural Networks
###### ニューラルネットワークのバッチ推論

Batch inference with deep learning models can benefit from GPU acceleration. 
深層学習モデルを使用したバッチ推論は、GPUアクセラレーションの恩恵を受けることができます。

Data is loaded in batches, preprocessed into tensors, and passed through the model in evaluation mode (model.eval()) to disable dropout. 
データはバッチで読み込まれ、テンソルに前処理され、ドロップアウトを無効にするために評価モード（model.eval()）でモデルを通過します。

The batch size for inference data should be tuned for available GPU memory to avoid OOM errors. 
推論データのバッチサイズは、OOMエラーを避けるために利用可能なGPUメモリに合わせて調整する必要があります。

The same feature and preprocessing transformations used in training should be applied before inference to ensure consistency. 
トレーニングで使用されるのと同じフィーチャーおよび前処理変換は、一貫性を確保するために推論の前に適用する必要があります。

Finally, using `torch.inference_mode()` is essential to maximize performance and avoid unnecessary gradient computation. 
最後に、`torch.inference_mode()`を使用することは、パフォーマンスを最大化し、不必要な勾配計算を避けるために不可欠です。

We now show how we do batch inference for our MNIST example from Chapter 10. 
ここでは、Chapter 10のMNIST例に対するバッチ推論の方法を示します。

First, we get our model from the model registry. 
まず、モデルレジストリからモデルを取得します。

From it, we download and unpickle our model weights (state) and MDTs (transform) and retrieve the hyperparameters from training_metrics. 
そこから、モデルの重み（状態）とMDT（変換）をダウンロードしてアンピクルし、training_metricsからハイパーパラメータを取得します。

We get the model’s feature view to retrieve batch inference data (all new images since MNIST was originally released). 
モデルのフィーチャービューを取得して、バッチ推論データ（MNISTが最初にリリースされて以来のすべての新しい画像）を取得します。

Our CustomMnist returns logits from its forward pass that we transform into probabilities by applying a soft max function to the predictions: 
私たちのCustomMnistは、フォワードパスからロジットを返し、それを予測にソフトマックス関数を適用して確率に変換します：

```python
model_mr = model_registry.get_model("mnist", version=1)
artifact_dir = model_mr.download()
state = joblib.load(os.path.join(artifact_dir, "model.pkl"))
transform = joblib.load(os.path.join(artifact_dir, "transform.pkl"))
fv = model_mr.get_feature_view()
layer_sz = model_mr.training_metrics.get("layer_sz")
dropout = model_mr.training_metrics.get("dropout")
model = CustomMnist(layer_sz=layer_sz, dropout=dropout) # from Chapter 10
model.load_state_dict(state)
model.eval() # disable Dropout
df = fv.get_batch_data(start_time="19980301 00:00") # inference images
dataset = ImageDataset(transform, df) # from Chapter 10
loader = DataLoader(dataset, batch_size=64, shuffle=False)
top1_probs = []
with torch.inference_mode(): # disable gradient computation
    for imgs in loader:
        logit_preds = model(imgs)
        probs = torch.softmax(logit_preds, dim=1)
        top1_probs.extend(probs.max(dim=1).values.tolist())
print(top1_probs)
```

###### Batch Inference for LLMs
###### LLMのバッチ推論

You can write batch inference programs with Pandas, Polars, or PySpark. 
Pandas、Polars、またはPySparkを使用してバッチ推論プログラムを書くことができます。

A simple such program reads the batch inference data, applies it to a prompt template, sends the batch inference requests to an LLM, and stores the outputs in an inference store. 
そのようなシンプルなプログラムは、バッチ推論データを読み込み、それをプロンプトテンプレートに適用し、バッチ推論リクエストをLLMに送信し、出力を推論ストアに保存します。

The easiest way to get started is to use an LLM via an API. 
始める最も簡単な方法は、APIを介してLLMを使用することです。

It is also possible, but less common, to download an open-foundation LLM. 
オープンファウンデーションLLMをダウンロードすることも可能ですが、一般的ではありません。

If you want to download the best open source LLM in 2025, DeepSeek V3 671B with full 32bit weights (~2.543 TB), you will require the equivalent of eight B200 NVIDIA GPUs. 
2025年に最高のオープンソースLLMであるDeepSeek V3 671B（フル32ビット重み、約2.543 TB）をダウンロードしたい場合、8台のB200 NVIDIA GPUに相当するものが必要です。

Even the quantized 4-bit version requires ~436 GB of GPU memory. 
量子化された4ビットバージョンでも、約436 GBのGPUメモリが必要です。

For this reason, we will look at batch inference with LLMs via API calls. 
このため、API呼び出しを介してLLMを使用したバッチ推論を見ていきます。

In inference, LLMs can give better and more predictable results through providing more task-specific information in the context window (prompt). 
推論において、LLMはコンテキストウィンドウ（プロンプト）により多くのタスク特有の情報を提供することで、より良く予測可能な結果を得ることができます。

You can also provide examples of the task in the context window, thus enabling the LLM to learn, using in-context learning, how to solve the task. 
また、コンテキストウィンドウにタスクの例を提供することで、LLMがインコンテキスト学習を使用してタスクを解決する方法を学ぶことができます。

The following terms are widely used to refer to how many examples an LLM gets in the prompt as part of the context window: 
以下の用語は、コンテキストウィンドウの一部としてLLMがプロンプトで受け取る例の数を指すために広く使用されています：

_Zero-shot_ This gives the LLM only the task description with no examples. 
_ゼロショット_ これは、LLMに例なしでタスクの説明のみを与えます。

_Single-shot_ This gives the LLM one example before the task description. 
_シングルショット_ これは、タスクの説明の前にLLMに1つの例を与えます。

_Few-shot_ This gives the LLM multiple examples before the task description. 
_フューショット_ これは、タスクの説明の前にLLMに複数の例を与えます。

You design your LLM query using a prompt template, as it makes it easier for you to add examples to the context window as shown. 
プロンプトテンプレートを使用してLLMクエリを設計すると、示されているようにコンテキストウィンドウに例を追加しやすくなります。

The context window contains the query sent to the LLM and includes the task description and any examples or additional context information. 
コンテキストウィンドウには、LLMに送信されるクエリが含まれ、タスクの説明や例、追加のコンテキスト情報が含まれます。

When you design your LLM batch inference pipeline, it should include the following steps: 
LLMバッチ推論パイプラインを設計する際は、以下のステップを含める必要があります：

1. Read batch inference data from your data source(s). 
1. データソースからバッチ推論データを読み取ります。

2. For each row of batch inference data, use the prompt template to build a query that may contain one-shot or few-shot examples. 
2. バッチ推論データの各行について、プロンプトテンプレートを使用して、ワンショットまたはフューショットの例を含む可能性のあるクエリを構築します。

3. Send your queries one at a time to the LLM API endpoint until all inference data has been processed (consider API rate limits, cost, and limits on the size of data the LLM will process for you per minute/hour). 
3. すべての推論データが処理されるまで、クエリを1つずつLLM APIエンドポイントに送信します（APIのレート制限、コスト、およびLLMが1分/時間あたりに処理するデータのサイズの制限を考慮します）。

4. Save LLM responses to an inference store for analysis/processing or eagerly execute actions when a batch of responses is received. 
4. LLMの応答を推論ストアに保存して分析/処理するか、応答のバッチを受信したときに即座にアクションを実行します。

Here is a more detailed code example that uses an OpenAI LLM to answer questions that arrived in the last 10 minutes. 
以下は、過去10分間に到着した質問に答えるためにOpenAI LLMを使用する詳細なコード例です。

We read our inference data from an offline feature group, `questions`. 
オフラインフィーチャーグループ`questions`から推論データを読み取ります。

We send those questions to the LLM endpoint and save the responses to an offline responses feature group for later consumption: 
これらの質問をLLMエンドポイントに送信し、応答をオフライン応答フィーチャーグループに保存して後で使用します：

```python
from tenacity import retry, wait_exponential, stop_after_attempt
from openai import OpenAI

questions_fg = fs.get_feature_group("questions", version=1)
responses_fg = fs.get_feature_group("responses", version=1)
openai_api_key = proj.get_secrets_api().get_secret("OPENAI_API_KEY").value
client = OpenAI(api_key=openai_api_key)
ten_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=10)
df = questions_fg.filter(questions_fg["ts"] > ten_minutes_ago).read()
model = "gpt-5"
max_tokens = 500
temperature = 0.7

def generate_prompt(question, example):
    return (
        "Answer the question clearly and accurately.\n\n"
        f"Example: \n{example}\n"
        f"Q: {question}\nA:"
    )

@retry(wait=wait_exponential(min=4, max=60), stop=stop_after_attempt(5))
def single_predict(question, example):
    prompt = generate_prompt(question, example)
    response = client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=max_tokens,
        temperature=temperature,
        reasoning={"effort": "minimal"}
    )
    return response.output_text.strip()

df['response'] = df.apply(
    lambda row: single_predict(row['question'], row['example']), axis=1
)
responses_fg.insert(df[["question", "response"]])
```

This code sends prediction requests one at a time to the LLM API endpoint. 
このコードは、予測リクエストを1つずつLLM APIエンドポイントに送信します。

It includes a single-shot prompt (with one example of how to answer the question). 
これは、質問に答える方法の1つの例を含むシングルショットプロンプトです。

We write the answers to a separate feature group, instead of an answer column in `questions`, as appending to a lakehouse table is far more efficient than updating the existing lakehouse table. 
私たちは、`questions`の回答列ではなく、別のフィーチャーグループに回答を書き込みます。これは、レイクハウステーブルに追加する方が、既存のレイクハウステーブルを更新するよりもはるかに効率的だからです。



The code uses annotations, defined using the _tenacity library, to prevent you from_ exceeding API rate limits and token quotas. 
このコードは、_tenacityライブラリを使用して定義されたアノテーションを使用し、APIのレート制限やトークンの割り当てを超えないようにします。_

The token quota is the maximum number of tokens permitted within a specified time frame, for example, daily. 
トークンの割り当ては、特定の時間枠内で許可される最大トークン数、例えば日次のことです。

The `tempera` ``` ture parameter controls the randomness of OpenAI’s model outputs. 
`tempera` ``` tureパラメータは、OpenAIのモデル出力のランダム性を制御します。

Lower values produce more deterministic responses, while higher values result in more diverse and creative answers. 
低い値はより決定論的な応答を生成し、高い値はより多様で創造的な回答をもたらします。

You may have to adjust these parameters for your use case, LLM provider agreement, and load. 
これらのパラメータは、あなたのユースケース、LLMプロバイダーの契約、および負荷に応じて調整する必要があるかもしれません。

If you can either find or create a small enough fine-tuned model for your task, it may also be possible to switch from API-based batch inference to batch inference with an embedded model. 
もしあなたがタスクに対して十分に小さなファインチューニングされたモデルを見つけるか作成できれば、APIベースのバッチ推論から埋め込みモデルを使用したバッチ推論に切り替えることも可能です。

There are also new libraries appearing for batch inference with LLMs, such as [fenic, where LLM inference is a column operation on DataFrames](https://oreil.ly/OG-oO) (map/classify/extract/semantic.join). 
LLMを使用したバッチ推論のための新しいライブラリも登場しており、例えば[fenic](https://oreil.ly/OG-oO)では、LLM推論がDataFrame上の列操作として行われます（map/classify/extract/semantic.join）。

###### Online Inference Pipelines
###### オンライン推論パイプライン

Probably the most aspirational phrase used by budding ML engineers is “deploying a model.” 
おそらく、これからのMLエンジニアが使う最も野心的なフレーズは「モデルをデプロイする」です。

But you rarely deploy just a model. 
しかし、単にモデルをデプロイすることはほとんどありません。

What you normally deploy is an online _inference pipeline—an operational service that runs 24/7 behind a network endpoint,_ accepting prediction requests and outputting predictions and logs. 
通常デプロイするのは、オンライン_推論パイプライン—ネットワークエンドポイントの背後で24時間365日稼働する運用サービスで、予測リクエストを受け入れ、予測とログを出力します。

If the model is not behind a remote API, then online inference pipelines first download the model from the model registry into a model-serving service, making the model callable via the online inference pipeline’s API (not the model’s own signature). 
モデルがリモートAPIの背後にない場合、オンライン推論パイプラインは最初にモデルレジストリからモデルをモデル提供サービスにダウンロードし、オンライン推論パイプラインのAPI（モデル自身のシグネチャではなく）を介してモデルを呼び出せるようにします。

Online inference pipelines are also connected to a feature store that provides precomputed features, similarity search, and logging. 
オンライン推論パイプラインは、事前計算された特徴、類似性検索、およびログを提供するフィーチャーストアにも接続されています。

###### Ensure Offline-Online Consistency for Libraries
###### ライブラリのオフライン-オンライン整合性を確保する

In Chapter 2, we stated that you need to ensure there is no skew between offline and online implementations of ODTs and MDTs. 
第2章では、ODTsとMDTsのオフラインおよびオンライン実装間に偏りがないことを確認する必要があると述べました。

However, you also have to ensure that the libraries used by the ODTs/MDTs in the feature/training/inference pipelines are compatible with one another. 
しかし、フィーチャー/トレーニング/推論パイプライン内のODTs/MDTsによって使用されるライブラリが互換性があることも確認する必要があります。

For example, if you pickle a model with joblib 1.2 in your training pipeline and try to download and unpickle it in your (batch or online) inference pipeline with joblib 1.1, you will likely get an error.  
例えば、トレーニングパイプラインでjoblib 1.2を使用してモデルをピクルし、joblib 1.1を使用して（バッチまたはオンライン）推論パイプラインでそれをダウンロードしてピクル解除しようとすると、エラーが発生する可能性があります。

Figure 11-4 shows how Hopsworks stores ODTs in feature groups and MDTs in feature views. 
図11-4は、HopsworksがODTsをフィーチャーグループに、MDTsをフィーチャービューにどのように保存するかを示しています。

When you use a feature view in your inference pipeline, it downloads the Python source code for the ODT or MDT transparently, ensuring the same function (and its state) is used in inference. 
推論パイプラインでフィーチャービューを使用すると、ODTまたはMDTのPythonソースコードが透過的にダウンロードされ、同じ関数（およびその状態）が推論で使用されることが保証されます。

_Figure 11-4. Hopsworks ODTs are stored in feature groups, and MDTs are stored in fea‐_ _ture views. Each Hopsworks project provides feature/training/inference base container_ _images to help ensure there is no incompatibility between library versions in the offline-_ _online pipelines._ 
_図11-4. Hopsworks ODTはフィーチャーグループに保存され、MDTはフィーチャービューに保存されます。各Hopsworksプロジェクトは、オフライン-オンラインパイプラインにおけるライブラリバージョン間の互換性がないことを保証するために、フィーチャー/トレーニング/推論のベースコンテナイメージを提供します。_

The figure also shows how Hopsworks provides base containers for FTI pipelines with compatible versions of libraries across the three different pipelines. 
この図はまた、Hopsworksが3つの異なるパイプライン全体でライブラリの互換性のあるバージョンを持つFTIパイプラインのためのベースコンテナをどのように提供しているかを示しています。

If you customize your container by adding Python dependencies or if you are not running ML pipelines on Hopsworks, you need to ensure that you install compatible versions of your libraries across your FTI pipelines.  
Pythonの依存関係を追加してコンテナをカスタマイズする場合や、HopsworksでMLパイプラインを実行していない場合は、FTIパイプライン全体でライブラリの互換性のあるバージョンをインストールすることを確認する必要があります。

###### Model Deployments with FastAPI
###### FastAPIを使用したモデルのデプロイ

A simplified model deployment is shown in Figure 11-5. 
図11-5に、簡略化されたモデルのデプロイが示されています。

It uses the FastAPI frame‐ work to make the model callable via an HTTP API. 
これは、モデルをHTTP APIを介して呼び出せるようにするためにFastAPIフレームワークを使用しています。

_Figure 11-5. A model deployment implemented using the FastAPI framework in Python._ 
_図11-5. PythonでFastAPIフレームワークを使用して実装されたモデルのデプロイ。_

FastAPI is a high-performance web framework for building HTTP-based service APIs in Python. 
FastAPIは、PythonでHTTPベースのサービスAPIを構築するための高性能なWebフレームワークです。

It is built on the [Pydantic framework, with type hints to validate,](https://oreil.ly/s3iBY) serialize, and deserialize prediction requests and responses. 
これは、予測リクエストとレスポンスを検証、シリアライズ、およびデシリアライズするための型ヒントを持つ[Pydanticフレームワーク](https://oreil.ly/s3iBY)の上に構築されています。

In FastAPI, you define the schema for a model deployment using `PredictionRequest and` `PredictionRes` ``` ponse (Pydantic classes). 
FastAPIでは、`PredictionRequest`および`PredictionResponse`（Pydanticクラス）を使用してモデルデプロイのスキーマを定義します。

These are the parameters and return types for the deploy‐ ment schema, respectively. 
これらは、それぞれデプロイメントスキーマのパラメータと戻り値の型です。

The following shows example code for a FastAPI: 
以下にFastAPIの例コードを示します：

```  
from fastapi import FastAPI  
from pydantic import BaseModel  
app = FastAPI()  
mr = hopsworks.login().get_model_registry()  
model_dir = mr.get_model("simple_model", version=1).download()  
model = XGBRegressor()  
model.load_model(os.path.join(model_dir, "model.json"))  
class PredictionRequest(BaseModel):  
    features: list[float]  
class PredictionResponse(BaseModel):  
    prediction: float  
@app.post("/predict", response_model=PredictionResponse)  
def predict(request: PredictionRequest):  
    prediction = model.predict([request.features])[0]  
    return PredictionResponse(prediction=float(prediction))
```

First, the model is downloaded to a local directory from the model registry, then it is loaded as an XGBoost regression model from _model.json. 
まず、モデルはモデルレジストリからローカルディレクトリにダウンロードされ、その後_model.jsonからXGBoost回帰モデルとしてロードされます。

The `predict method` extracts the parameters from the `PredictionRequest object as input features to` ``` model.predict(), and it returns prediction, a float. 
`predict`メソッドは、`PredictionRequest`オブジェクトからパラメータを抽出し、`model.predict()`への入力特徴として使用し、予測をfloatとして返します。

In this simple example, the deployment API and the model signature (the ordered input and return types for the model) are identical. 
このシンプルな例では、デプロイメントAPIとモデルシグネチャ（モデルのための順序付き入力および戻り値の型）は同一です。

###### LLM Deployments
###### LLMのデプロイ

Could you use FastAPI to serve an LLM of any size? 
FastAPIを使用して任意のサイズのLLMを提供できますか？

Yes, you could. 
はい、可能です。

But you would need GPU(s), lots of memory, and high-performance storage and networking. 
しかし、GPU、たくさんのメモリ、高性能なストレージとネットワーキングが必要です。

The easiest way to start serving LLMs is to use a pretrained model. 
LLMを提供する最も簡単な方法は、事前学習済みモデルを使用することです。

Hugging Face is a pop‐ ular marketplace for pretrained models, and you can use its transformers library to download models directly from their website. 
Hugging Faceは事前学習済みモデルの人気のあるマーケットプレイスであり、そのtransformersライブラリを使用して、彼らのウェブサイトから直接モデルをダウンロードできます。

For example, you can download a model and its tokenizer and then register both of them together in Hopworks’ model registry as follows: 
例えば、モデルとそのトークナイザーをダウンロードし、次に両方をHopsworksのモデルレジストリに一緒に登録することができます：

```  
from transformers import AutoTokenizer, AutoModelForCausalLM  
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3")  
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-V3")  
deepseek_local_dir = "deepseek_dir"  
model.save_pretrained(deepseek_local_dir)  
tokenizer.save_pretrained(deepseek_local_dir)  
deepseek = mr.llm.create_model(  
    name="deepseek-V3",  
    description="DeepSeek-V3 671B model (via HF)"  
)  
deepseek.save(deepseek_local_dir)
```

This code downloads DeepSeek V3 (with 671 billion parameters and FP8 precision) as files in the _.safetensors file format, as well as its tokenizer. 
このコードは、DeepSeek V3（6710億パラメータとFP8精度を持つ）を_.safetensorsファイル形式のファイルとしてダウンロードし、そのトークナイザーもダウンロードします。

In total, there are 163 .safetensor files. 
合計で163の.safetensorファイルがあります。

Nearly all of the files are 4.3 GB in size, and the model is, in total, around 700 GB on disk. 
ほとんどすべてのファイルは4.3 GBのサイズで、モデルは合計で約700 GBのディスクを占めています。

As this model is so large, it is best to save it in your local model registry once, rather than download it from Hugging Face every time you want to deploy it for serving. 
このモデルは非常に大きいため、提供のためにデプロイするたびにHugging Faceからダウンロードするのではなく、一度ローカルモデルレジストリに保存するのが最良です。

The Hopsworks model registry stores model files in HopsFS, a tiered distributed filesystem that supports temporal caching of recent files on the local (NVMe) disks of HopsFS data nodes. 
Hopsworksモデルレジストリは、HopsFSにモデルファイルを保存します。HopsFSは、HopsFSデータノードのローカル（NVMe）ディスク上で最近のファイルの時間的キャッシングをサポートする階層型分散ファイルシステムです。

The HopsFS long-term storage layer is an S3 object store. 
HopsFSの長期ストレージ層はS3オブジェクトストアです。

NVMe disks are needed to store and load massive LLM files to prevent training and inference pipelines being disk I/O bound. 
トレーニングおよび推論パイプラインがディスクI/Oに制約されないようにするために、大規模なLLMファイルを保存およびロードするにはNVMeディスクが必要です。

DeepSeek introduced its own distributed filesystem, called Fire-Flyer File System (3FS), that uses NVMe disks to optimize filesystem performance during training. 
DeepSeekは、トレーニング中のファイルシステムパフォーマンスを最適化するためにNVMeディスクを使用する独自の分散ファイルシステムであるFire-Flyer File System (3FS)を導入しました。

###### Deployment API for Models and Feature Views
###### モデルとフィーチャービューのためのデプロイメントAPI

In most online inference pipelines, the (model) deployment API and model signature differ, as not all features come via the prediction request. 
ほとんどのオンライン推論パイプラインでは、（モデル）デプロイメントAPIとモデルシグネチャは異なります。なぜなら、すべての特徴が予測リクエストを介して提供されるわけではないからです。

Features may be retrieved from the feature store or computed on demand. 
特徴はフィーチャーストアから取得されるか、必要に応じて計算されることがあります。

For example, when a model requires history/context information, entity ID(s) can be sent in the prediction request and used to retrieve precomputed features from the feature store, using those entity IDs. 
例えば、モデルが履歴/コンテキスト情報を必要とする場合、エンティティIDを予測リクエストに送信し、それらのエンティティIDを使用してフィーチャーストアから事前計算された特徴を取得することができます。

For LLMs, you could add extra text to the user-provided prompt with a prompt template or use RAG to retrieve text chunks from a vector index. 
LLMの場合、プロンプトテンプレートを使用してユーザー提供のプロンプトに追加のテキストを追加するか、RAGを使用してベクトルインデックスからテキストチャンクを取得することができます。

The text in the final prompt also needs to be tokenized before it is sent to the LLM. 
最終的なプロンプトのテキストは、LLMに送信される前にトークン化する必要があります。

The deployment API for an LLM should be clear text input and output, while the LLM’s model signature expects encoded text as input and produces clear text as output. 
LLMのデプロイメントAPIは明確なテキストの入力と出力であるべきですが、LLMのモデルシグネチャはエンコードされたテキストを入力として期待し、明確なテキストを出力します。

The deployment API defines the interface to the online inference pipeline that clients send prediction requests to. 
デプロイメントAPIは、クライアントが予測リクエストを送信するオンライン推論パイプラインへのインターフェースを定義します。

Figure 11-6 shows a simplified example of a model deployment for our credit card system. 
図11-6は、私たちのクレジットカードシステムのモデルデプロイの簡略化された例を示しています。

The deployment API takes the parameters for a credit card transaction (see our data mart in Figure 4-9). 
デプロイメントAPIは、クレジットカード取引のパラメータを受け取ります（図4-9のデータマートを参照）。

The deployment API has two different types of parameters: 
デプロイメントAPIには2種類の異なるパラメータがあります：

_Serving keys_ Used to read precomputed features from the online feature store 
_サービングキー_ オンラインフィーチャーストアから事前計算された特徴を読み取るために使用されます。

_Request parameters_ Used as either parameters to ODTs or passed features (feature values that go directly in the feature vector, overriding any precomputed feature value that may have been returned from the feature store) 
_リクエストパラメータ_ ODTへのパラメータとして使用されるか、フィーチャー値（フィーチャーベクターに直接入るフィーチャー値で、フィーチャーストアから返された事前計算されたフィーチャー値を上書きします）として渡されます。



An online inference pipeline is implemented as a Python program that loads the model and any dependencies on startup, then provides one or more predict methods to make predictions on the model. 
オンライン推論パイプラインは、モデルとその依存関係を起動時にロードし、モデルに対して予測を行うための1つ以上のpredictメソッドを提供するPythonプログラムとして実装されます。

In Hopsworks, the code that implements the online inference pipeline could be implemented as follows in what is called a predictor script: 
Hopsworksでは、オンライン推論パイプラインを実装するコードは、以下のように「predictor script」と呼ばれる形で実装できます：

```  
class Predictor():     
    def __init__(self):       
        mr = hopsworks.login().get_model_registry()       
        mr_model = mr.get_model("cc_model", version=1)       
        self.model = XGBClassifier()       
        self.model.load_model(os.path.join(mr_model.download(), "model.json"))       
        self.fv = mr_model.get_feature_view()     
    def predict(self, inputs):       
        features = self.fv.get_feature_vector(         
            serving_keys = {"cc_num": inputs[0]["cc_num"],                 
                            "merchant_id": inputs[0]["merchant_id"]},         
            passed_features = {"amount": inputs[0]["amount"],              
                               "card_present": inputs[0]["card_present"]},         
            request_parameters = {"ts": inputs[0]["ts"],                    
                                  "ip_addr": inputs[0]["ip_addr"]}       
        )       
        prediction = self.model.predict(features)       
        self.fv.log(features, predictions = prediction)       
        return prediction
``` 
```  
クラスPredictor():     
    def __init__(self):       
        mr = hopsworks.login().get_model_registry()       
        mr_model = mr.get_model("cc_model", version=1)       
        self.model = XGBClassifier()       
        self.model.load_model(os.path.join(mr_model.download(), "model.json"))       
        self.fv = mr_model.get_feature_view()     
    def predict(self, inputs):       
        features = self.fv.get_feature_vector(         
            serving_keys = {"cc_num": inputs[0]["cc_num"],                 
                            "merchant_id": inputs[0]["merchant_id"]},         
            passed_features = {"amount": inputs[0]["amount"],              
                               "card_present": inputs[0]["card_present"]},         
            request_parameters = {"ts": inputs[0]["ts"],                    
                                  "ip_addr": inputs[0]["ip_addr"]}       
        )       
        prediction = self.model.predict(features)       
        self.fv.log(features, predictions = prediction)       
        return prediction
``` 

The Predictor.init() method is called once on startup, and it downloads the model and retrieves the feature view. 
Predictor.init()メソッドは起動時に1回呼び出され、モデルをダウンロードし、特徴ビューを取得します。

In the code for `predict(),` `fv.get_feature_vec` performs the following steps: 
`predict()`のコードでは、`fv.get_feature_vec`が以下のステップを実行します：

```  
1. Retrieve the precomputed features from the online feature store. 
2. Merge precomputed and passed feature values. 
3. Compute ODTs using request_parameters and precomputed features. 
4. Compute MDTs defined on the feature view. 
5. Drop any index columns and/or inference helper columns. 
6. Return the transformed feature vector as a DataFrame or list. 
```  
```  
1. オンラインフィーチャーストアから事前計算された特徴を取得します。 
2. 事前計算された特徴値と渡された特徴値をマージします。 
3. request_parametersと事前計算された特徴を使用してODTsを計算します。 
4. 特徴ビューで定義されたMDTsを計算します。 
5. インデックス列および/または推論ヘルパー列を削除します。 
6. 変換された特徴ベクトルをDataFrameまたはリストとして返します。 
``` 

Here, `cc_num` and `merchant_id` are the serving keys, while we need to explicitly define which parameters to predict are passed features and which ones are request parameters for transformation functions. 
ここで、`cc_num`と`merchant_id`はサービングキーであり、どのパラメータが予測される渡された特徴で、どのパラメータが変換関数のリクエストパラメータであるかを明示的に定義する必要があります。

Both amount and card_present are passed features, while ts and ip_addr are parameters for ODTs. 
amountとcard_presentは渡された特徴であり、tsとip_addrはODTsのパラメータです。

The precomputed features prev_ip and prev_ts are parameters for ODTs but are not features for the model. 
事前計算された特徴であるprev_ipとprev_tsはODTsのパラメータですが、モデルの特徴ではありません。

For this reason, they are defined as inference helper columns in the feature view. 
この理由から、これらは特徴ビュー内の推論ヘルパー列として定義されます。

As precomputed features are returned as either a list or a DataFrame, inference helper columns need to be dropped from the list or DataFrame. 
事前計算された特徴はリストまたはDataFrameのいずれかとして返されるため、推論ヘルパー列はリストまたはDataFrameから削除する必要があります。

The features and prediction are also logged before the prediction is returned to the client. 
特徴と予測は、予測がクライアントに返される前にログに記録されます。

In Hopsworks, logs are written asynchronously to a logging feature group for the feature view. 
Hopsworksでは、ログは特徴ビューのためのロギングフィーチャーグループに非同期で書き込まれます。

The previous Predictor deployment program is quite complex, but luckily, you can automatically generate it by calling: 
前述のPredictorデプロイメントプログラムは非常に複雑ですが、幸運なことに、次のように呼び出すことで自動的に生成できます：

```  
deployment = model.deploy(passed_features=["amount","card_present"]) 
```  
```  
deployment = model.deploy(passed_features=["amount","card_present"]) 
``` 

This will create a predictor.py Python source code file, containing the Predictor class with init() and predict() methods and all the above calls to retrieve the model and the feature view, and then create the feature vector from the request parameters, precomputed features, and transformations. 
これにより、Predictorクラスを含むpredictor.pyというPythonソースコードファイルが作成され、init()およびpredict()メソッドと、モデルと特徴ビューを取得するためのすべての呼び出しが含まれ、リクエストパラメータ、事前計算された特徴、および変換から特徴ベクトルが作成されます。

You can also create a feature view as a deployment in Hopsworks, without a model. 
モデルなしでHopsworksにデプロイメントとして特徴ビューを作成することもできます。

This is useful if your model serving infrastructure is distinct from your feature store. 
これは、モデルサービングインフラストラクチャがフィーチャーストアとは異なる場合に便利です。

You can call `deploy a feature view`, and it will create the same deployment as a model deployment, minus the model itself. 
`deploy a feature view`を呼び出すと、モデル自体を除いたモデルデプロイメントと同じデプロイメントが作成されます。

The feature view deployment computes the transformations, logs feature values, and returns the transformed feature vector to the client where the model prediction is performed. 
特徴ビューのデプロイメントは変換を計算し、特徴値をログに記録し、モデル予測が行われるクライアントに変換された特徴ベクトルを返します。

The predictor script is then deployed to model serving infrastructure (KServe/vLLM) on Hopsworks as a model deployment with a REST or gRPC endpoint, ready to accept prediction requests. 
その後、predictorスクリプトは、RESTまたはgRPCエンドポイントを持つモデルデプロイメントとしてHopsworksのモデルサービングインフラストラクチャ（KServe/vLLM）にデプロイされ、予測リクエストを受け入れる準備が整います。

You can also check the API to your deployment using: 
デプロイメントのAPIを確認するには、次のようにします：

```  
print(deployment.schema) 
```  
```  
print(deployment.schema) 
``` 

It will print out the request parameters, passed parameters, serving keys, and return type for your deployment. 
これにより、デプロイメントのリクエストパラメータ、渡されたパラメータ、サービングキー、および返り値の型が出力されます。

This is the API that your client applications should depend on. 
これは、クライアントアプリケーションが依存すべきAPIです。

The deployment API should be more stable than the model signature. 
デプロイメントAPIはモデルシグネチャよりも安定しているべきです。

The deployment API follows the information-hiding principle. 
デプロイメントAPIは情報隠蔽の原則に従います。

So long as the request parameters, serving keys, and return type are unchanged, you can safely make changes in how the predictor is implemented. 
リクエストパラメータ、サービングキー、および返り値の型が変更されない限り、predictorの実装方法を安全に変更できます。

Another advantage of the deployment API is that the model version can change over time without breaking the client. 
デプロイメントAPIのもう一つの利点は、モデルのバージョンが時間とともに変わってもクライアントが壊れないことです。

For example, you could upgrade an XGBoost model or replace a precomputed feature with an on-demand computed feature without requiring changes to the client. 
例えば、XGBoostモデルをアップグレードしたり、事前計算された特徴をオンデマンド計算された特徴に置き換えたりしても、クライアントに変更を要求する必要はありません。

The deployment API is a contract that not only includes a schema but should also have an SLO, defining how much downtime is acceptable per day/month/year and p99 latency for responses. 
デプロイメントAPIは、スキーマを含むだけでなく、1日/月/年あたりの許容ダウンタイムと応答のp99レイテンシを定義するSLOも持つ契約です。

The p99 value is a latency threshold where 99% of requests must complete under that latency threshold; otherwise, there is a violation of the SLO. 
p99値は、99%のリクエストがそのレイテンシ閾値内で完了しなければならないレイテンシ閾値であり、そうでなければSLOの違反となります。

For example, in real-time 
例えば、リアルタイムで



recommendations, 99% of requests should return in under 10 ms. 
推奨事項として、99%のリクエストは10ミリ秒未満で返されるべきです。

In contrast, for an LLM, the p99 could be as high as tens of seconds. 
対照的に、LLMの場合、p99は数十秒に達する可能性があります。

In Hopsworks, you can also create feature view deployments that are accessible by external clients via a REST or gRPC API. 
Hopsworksでは、外部クライアントがRESTまたはgRPC APIを介してアクセスできるフィーチャービューのデプロイメントを作成することもできます。

This is useful if you host your model on model-serving infrastructure outside Hopsworks but want to use Hopsworks as a feature store. 
これは、モデルをHopsworksの外部にあるモデルサービングインフラストラクチャでホストしているが、Hopsworksをフィーチャーストアとして使用したい場合に便利です。

You deploy a feature view as follows: 
フィーチャービューは次のようにデプロイします：

```  
fv_deployment = fv.deploy(passed_features=["amount","card_present"],       
resources={"instances"="1", "cores": 0.5, "memory_mb": 1024*2})
```

The prediction script code generated is identical to the model-serving case, except the model-related code is omitted. 
生成される予測スクリプトのコードは、モデルサービングの場合と同じですが、モデル関連のコードは省略されています。

The code to deploy a model or feature view also allocates the container for the deployment. 
モデルまたはフィーチャービューをデプロイするためのコードは、デプロイメント用のコンテナも割り当てます。

You should configure the correct amount of resources (including the number of container instances) and per container resources: the number of CPUs, amount of memory, and number of GPUs. 
適切なリソースの量（コンテナインスタンスの数を含む）と、コンテナごとのリソース（CPUの数、メモリの量、GPUの数）を設定する必要があります。

You can also avail yourself of autoscaling to increase/decrease the number of active containers in response to changes in metrics, such as the number of prediction requests per second. 
また、予測リクエストの数などのメトリクスの変化に応じて、アクティブなコンテナの数を増減させるためにオートスケーリングを利用することもできます。

###### Model-Serving Frameworks with KServe
###### KServeを使用したモデルサービングフレームワーク

FastAPI lacks many enterprise capabilities, such as GPU allocation, elastic scalability, authentication, access control, and auditing. 
FastAPIは、GPUの割り当て、弾力的なスケーラビリティ、認証、アクセス制御、監査など、多くのエンタープライズ機能が欠けています。

These capabilities are typically provided by model-serving platforms. 
これらの機能は通常、モデルサービングプラットフォームによって提供されます。

We will look primarily at KServe, an open source Kubernetes-based model serving platform that supports a variety of backends to cater to different ML frameworks and use cases. 
私たちは主に、さまざまなMLフレームワークやユースケースに対応するためのさまざまなバックエンドをサポートするオープンソースのKubernetesベースのモデルサービングプラットフォームであるKServeを見ていきます。

KServe provides: 
KServeは以下を提供します：

_A pluggable model-serving backend_ 
_プラグイン可能なモデルサービングバックエンド_

You can use a lightweight framework, like FastAPI, for smaller decision tree models; NVIDIA Triton as a higher-performance all-rounder for models that require GPUs; and vLLM for serving the largest LLMs. 
小さな決定木モデルにはFastAPIのような軽量フレームワークを使用し、GPUを必要とするモデルにはNVIDIA Tritonを高性能なオールラウンダーとして使用し、最大のLLMを提供するためにはvLLMを使用できます。

_A/B testing_ 
_A/Bテスト_

You can route requests between two versions (blue and green) of a model, enabling their performance comparison before traffic can finally be switched to the new model version, assuming its behavior is acceptable. 
モデルの2つのバージョン（青と緑）間でリクエストをルーティングでき、トラフィックが最終的に新しいモデルバージョンに切り替えられる前に、そのパフォーマンスを比較することができます。

_Multimodel serving_ 
_マルチモデルサービング_

Multiple models can be deployed in a single container. 
複数のモデルを単一のコンテナにデプロイできます。

_Serverless deployments_ 
_サーバーレスデプロイメント_

Deployments are autoscaled based on request load, including scaling down to zero and scaling out by creating container instances and load balancing over them. 
デプロイメントはリクエスト負荷に基づいてオートスケールされ、ゼロにスケールダウンしたり、コンテナインスタンスを作成してそれらに負荷分散することでスケールアウトします。

_Metrics, monitoring, and logging_ 
_メトリクス、モニタリング、およびロギング_

These provide observability for model deployments. 
これらはモデルデプロイメントの可視性を提供します。

By monitoring and alerting on request-processing latency, you can support an SLO for your model deployment. 
リクエスト処理のレイテンシを監視し、アラートを出すことで、モデルデプロイメントのSLOをサポートできます。

KServe also enables you to decompose your online inference pipeline into two Python programs: a _transformer and a_ _predictor. 
KServeは、オンライン推論パイプラインを2つのPythonプログラム、_transformer_と_predictor_に分解することも可能にします。

In the previous section, we introduced a Predictor class that performed preprocessing, model prediction, and post-processing steps. 
前のセクションでは、前処理、モデル予測、および後処理ステップを実行するPredictorクラスを紹介しました。

In KServe, it is possible to refactor out the preprocessing and postprocessing steps into a separate _transformer container, with the_ _predictor container only performing model prediction. 
KServeでは、前処理と後処理のステップを別の_transformer_コンテナにリファクタリングし、_predictor_コンテナはモデル予測のみを実行することが可能です。

The transformer is useful if you have computationally complex preprocessing or postprocessing tasks that do not require a GPU but your predictor requires a GPU. 
トランスフォーマーは、GPUを必要としない計算的に複雑な前処理または後処理タスクがあり、予測器がGPUを必要とする場合に便利です。

Mixing CPU-intensive and GPU-intensive operations using only a predictor can reduce GPU utilization levels. 
予測器のみを使用してCPU集約型とGPU集約型の操作を混合すると、GPUの利用率が低下する可能性があります。

Together, a transformer and a predictor are called an inference service (InferenceService). 
トランスフォーマーと予測器を合わせて、推論サービス（InferenceService）と呼びます。

[In Figure 11-7, you can see a model deployment on KServe with both a transformer](https://oreil.ly/MbMQO) and a predictor, connected to a number of infrastructural services in Hopsworks. 
[図11-7では、トランスフォーマーと予測器の両方を持つKServe上のモデルデプロイメントが、Hopsworksのいくつかのインフラサービスに接続されているのを見ることができます。]

_Figure 11-7. Model deployments on KServe can use infrastructural services provided by_ _Hopsworks, including security, logging, monitoring, RAG, feature store, and GPU_ _management._  
_図11-7. KServe上のモデルデプロイメントは、Hopsworksが提供するインフラサービスを利用でき、セキュリティ、ロギング、モニタリング、RAG、フィーチャーストア、GPU管理を含みます。_

The predictor is a model-serving framework. 
予測器はモデルサービングフレームワークです。

KServe’s supported backends include: 
KServeがサポートするバックエンドには以下が含まれます：

_TensorFlow Serving_ 
_TensorFlow Serving_

Optimized for serving TensorFlow models, this backend provides high-performance inference and supports features like versioning and A/B testing. 
TensorFlowモデルの提供に最適化されており、このバックエンドは高性能な推論を提供し、バージョン管理やA/Bテストなどの機能をサポートします。

_TorchServe_ 
_TorchServe_

Designed for PyTorch models, TorchServe offers multimodel serving, logging, and metrics and supports both REST and gRPC protocols. 
PyTorchモデル向けに設計されたTorchServeは、マルチモデルサービング、ロギング、メトリクスを提供し、RESTおよびgRPCプロトコルの両方をサポートします。

_ONNX Runtime_ 
_ONNX Runtime_

This supports models in the Open Neural Network Exchange (ONNX) format, enabling cross-platform interoperability and optimized performance across different hardware. 
これはOpen Neural Network Exchange（ONNX）形式のモデルをサポートし、異なるハードウェア間でのクロスプラットフォーム相互運用性と最適化されたパフォーマンスを可能にします。

_Python server_ 
_Pythonサーバー_

This is a flexible, low-overhead, ML framework–agnostic backend that is often used to serve XGBoost and Scikit-Learn models. 
これは柔軟で低オーバーヘッドのMLフレームワークに依存しないバックエンドで、XGBoostやScikit-Learnモデルを提供するためにしばしば使用されます。

It is built on a FastAPI server. 
FastAPIサーバー上に構築されています。

_NVIDIA Triton Inference Server_ 
_NVIDIA Triton Inference Server_

This is a high-performance model-serving platform that supports multiple frameworks, primarily on GPUs. 
これは高性能なモデルサービングプラットフォームで、主にGPU上で複数のフレームワークをサポートします。

_vLLM_ 
_vLLM_

This is optimized for serving LLMs. 
これはLLMを提供するために最適化されています。

Triton and vLLM are the two highest-performance backends, offering advanced features like dynamic batching and optimized memory management, which can significantly enhance throughput and reduce latency for specific workloads. 
TritonとvLLMは、動的バッチ処理や最適化されたメモリ管理などの高度な機能を提供する2つの最高性能のバックエンドであり、特定のワークロードに対してスループットを大幅に向上させ、レイテンシを低下させることができます。

KServe InferenceServices need to be connected to the infrastructure services needed by its model deployments. 
KServe InferenceServicesは、そのモデルデプロイメントに必要なインフラサービスに接続する必要があります。

Hopsworks instruments KServe for logging and metrics (OpenSearch for logs and Prometheus for metrics), adds authentication and access control, manages KServe containers for deployments, and connects deployments to a feature store, model registry, and vector index. 
Hopsworksは、ログとメトリクスのためにKServeを設定し（ログ用のOpenSearchとメトリクス用のPrometheus）、認証とアクセス制御を追加し、デプロイメントのためのKServeコンテナを管理し、デプロイメントをフィーチャーストア、モデルレジストリ、およびベクトルインデックスに接続します。

Finally, while KServe is the API we are using here to deploy models, you may also have to configure the backend model-serving framework. 
最後に、KServeはここでモデルをデプロイするために使用しているAPIですが、バックエンドのモデルサービングフレームワークを設定する必要がある場合もあります。

For example, to deploy the pretrained DeepSeek V3 model that we earlier registered with the model registry, you must provide an additional YAML file for the vLLM backend, such as: 
たとえば、以前にモデルレジストリに登録した事前学習済みのDeepSeek V3モデルをデプロイするには、vLLMバックエンド用の追加のYAMLファイルを提供する必要があります。次のように：

```  
path_to_config_file = "deepseek_vllmconfig.yaml"   
deepseek_depl = deepseek.deploy(     
name="deepseek-V3",     
config_file=path_to_config_file,     
resources={"num_instances": 1,     
"requests": {"cores": 24, "memory_mb": 1024*512, "gpus": 8}},   
)
```

###### Performance and Failure Handling
###### パフォーマンスと障害処理

We will look at how to write ODTs and MDTs in Python, so they can be run with lower latency as Python UDFs in online inference pipelines and with higher throughput as Pandas UDFs in feature pipelines. 
ODTsとMDTsをPythonでどのように記述するかを見ていきます。これにより、オンライン推論パイプラインでPython UDFとして低レイテンシで実行でき、フィーチャーパイプラインでPandas UDFとして高スループットで実行できます。

If you need even lower-latency ODTs, we will look at native functions. 
さらに低レイテンシのODTsが必要な場合は、ネイティブ関数を見ていきます。

###### Mixed-Mode UDFs
###### 混合モードUDFs

To estimate the difference in latency between Python UDFs and Pandas UDFs, I wrote a simple function that calculates the square of the input number. 
Python UDFとPandas UDFのレイテンシの違いを推定するために、入力数の平方を計算する簡単な関数を書きました。

I benchmarked this function as a Python UDF versus a Pandas UDF on my eight-core Linux laptop. 
私はこの関数をPython UDFとPandas UDFとして、8コアのLinuxラップトップでベンチマークしました。

The Python UDF version took one thousandth of the time of the Pandas UDF for a single row (including the time required to create the DataFrame). 
Python UDFバージョンは、単一の行に対してPandas UDFの1000分の1の時間（DataFrameを作成するために必要な時間を含む）を要しました。

For example, here is a transformation function that returns the maximum value from three parameters. 
たとえば、ここに3つのパラメータから最大値を返す変換関数があります。

Note that because of the hopsworks.udf decorator, we cannot invoke the function directly, but rather, we must invoke it via the invoke() wrapper function call: 
hopsworks.udfデコレーターのため、関数を直接呼び出すことはできず、invoke()ラッパー関数呼び出しを介して呼び出す必要があります：

```  
import numpy as np   
@hopsworks.udf(float)   
def max_param(param1, param2, param3):     
result = np.maximum.reduce([param1, param2, param3])     
return result   

# Example usage as a Python UDF   
result_python = max_param.invoke(1.0, 2.0, 3.0)   
batch_size = 2500000   
data = pd.DataFrame(np.random.rand(batch_size, 3),              
columns=['param1', 'param2', 'param3'])   

# Example usage as a Pandas UDF on a batch of rows   
results_batch = \     
max_param.invoke(data['param1'], data['param2'], data['param3'])
```

This code can be executed in mixed Python/Pandas UDF mode thanks to dynamic typing in Python. 
このコードは、Pythonの動的型付けのおかげで、混合Python/Pandas UDFモードで実行できます。

We do not explicitly define the types of parameters. 
パラメータの型を明示的に定義することはありません。

In effect, the Python interpreter infers the type of `param1,` `param2, and` `param3 as a` `Union[float,` ``` pd.Series]. 
実際には、Pythonインタープリタは`param1`、`param2`、および`param3`の型を`Union[float, pd.Series]`として推論します。

That is, param1/2/3 are floats when executed as a Python UDF and pd.Series when executed as a Pandas UDF. 
つまり、param1/2/3はPython UDFとして実行されるときはfloatであり、Pandas UDFとして実行されるときはpd.Seriesです。

The Python UDF takes 0.0598 ms to execute on my laptop, while the Pandas UDF that processes 2.5M rows takes only 60.8871 ms. 
Python UDFは私のラップトップで0.0598ミリ秒で実行されるのに対し、2.5M行を処理するPandas UDFはわずか60.8871ミリ秒で実行されます。

Running `max_param as a Python UDF with 2.5M rows takes 5,663.67 ms—100` times slower than the Pandas UDF. 
2.5M行でPython UDFとして`max_param`を実行すると5,663.67ミリ秒かかり、Pandas UDFの100倍遅くなります。

This means the preceding code has low-ish latency for the online inference pipeline but can scale to backfill lots of feature data in a feature pipeline. 
これは、前述のコードがオンライン推論パイプラインに対して比較的低いレイテンシを持っていることを意味しますが、フィーチャーパイプラインで多くのフィーチャーデータをバックフィルするためにスケールすることができます。



Sometimes, however, the transformation logic cannot be written such that it can be executed in mixed mode. 
しかし、時には、変換ロジックを混合モードで実行できるように書くことができない場合があります。

For example, in the following snippet, we create 250 rows and 20 columns of synthetic data (mixed strings and ints). 
例えば、以下のスニペットでは、250行20列の合成データ（混合された文字列と整数）を作成します。

The transformation sorts the rows by a column and returns the top five rows. 
この変換は、列によって行をソートし、上位5行を返します。

If we want to run this code as a Python UDF, we should pass our rows in as an array. 
このコードをPython UDFとして実行したい場合、行を配列として渡す必要があります。

In contrast, a Pandas UDF should take in a DataFrame or Series and operate on it using vectorized Pandas operations, rather than looping over individual rows: 
対照的に、Pandas UDFはDataFrameまたはSeriesを受け取り、個々の行をループするのではなく、ベクトル化されたPandas操作を使用してそれに対して操作する必要があります：

```  
def process_rows_array(rows, sort_column_index):     
    sorted_rows = sorted(rows, key=lambda x: x[sort_column_index], reverse=True)     
    return sorted_rows[:5]   
def process_rows_pandas(df, sort_col_name):     
    return df.sort_values(sort_col_name, ascending=False).head(5)   
rows, cols = 250, 20   
col_names, data, sort_col_name, sort_col_index = generate_sample_data(rows, cols)   
top5_array = process_rows_array(data, sort_col_index)   
df = pd.DataFrame(data, columns=col_names)   
top5_pandas = process_rows_pandas(df, sort_col_name)
```

The Python UDF takes 0.076 ms to execute on my laptop, while the Pandas UDF takes 0.621 ms. 
Python UDFは私のラップトップで0.076ミリ秒で実行されるのに対し、Pandas UDFは0.621ミリ秒かかります。

However, the preceding code does not include the cost of creating the Pandas DataFrame. 
ただし、前述のコードにはPandas DataFrameを作成するコストは含まれていません。

The Hopsworks online feature store returns precomputed features in row-oriented format, by default as an array. 
Hopsworksのオンラインフィーチャーストアは、デフォルトで配列として行指向形式で事前計算された特徴を返します。

There is always a cost in loading and transposing row-oriented records into a columnar Pandas DataFrame. 
行指向のレコードを列指向のPandas DataFrameに読み込み、転置するには常にコストがかかります。

If Pandas UDFs introduce too much latency but you still need ODTs in your feature pipeline, you should support two different implementations, ensuring both implementations produce equivalent results. 
Pandas UDFがあまりにも多くのレイテンシを引き起こす場合でも、フィーチャーパイプラインにODTが必要な場合は、2つの異なる実装をサポートし、両方の実装が同等の結果を生成することを確認する必要があります。

Write a unit test to ensure that both functions return the same results for typical input parameters. 
ユニットテストを書いて、両方の関数が典型的な入力パラメータに対して同じ結果を返すことを確認してください。

If you do not need to use the ODT in your feature pipeline, you can reduce transformation latency even further with native UDFs. 
フィーチャーパイプラインでODTを使用する必要がない場合、ネイティブUDFを使用することで変換レイテンシをさらに減少させることができます。

###### Native UDFs and Log-and-Wait
###### ネイティブUDFとログ・アンド・ウェイト

If you need the lowest-latency UDFs for ODTs, you should implement them in a compiled language such as C, C++, or Rust. 
ODTのために最低レイテンシのUDFが必要な場合は、C、C++、またはRustなどのコンパイル言語で実装する必要があります。

The main disadvantage of implementing feature functions in native code is that there is currently no open source scalable DataFrame library that can easily execute them in a feature or training pipeline. 
ネイティブコードでフィーチャー関数を実装する主な欠点は、現在、フィーチャーまたはトレーニングパイプラインで簡単に実行できるオープンソースのスケーラブルなDataFrameライブラリが存在しないことです。

That is, you won’t easily be able to run your feature functions against historical data. 
つまり、履歴データに対してフィーチャー関数を簡単に実行することはできません。

However, this is not a problem if you never need to create features from historical data— that is, if you can log the output of your feature function from your online system and wait until enough feature data has been collected so that you have sufficient training data for your model. 
ただし、履歴データからフィーチャーを作成する必要がない場合、つまり、オンラインシステムからフィーチャー関数の出力をログに記録し、十分なフィーチャーデータが収集されるまで待つことができる場合は、これは問題ではありません。

At the Feature Store Summit in 2023, Jin Shang introduced WeChat’s real-time feature compute engine, where they define feature functions in C++ and the engine adaptively picks one of two compute engines to execute feature functions, with the goal of minimizing compute latency. 
2023年のフィーチャーストアサミットで、Jin ShangはWeChatのリアルタイムフィーチャー計算エンジンを紹介しました。ここでは、フィーチャー関数をC++で定義し、エンジンが計算レイテンシを最小限に抑えることを目的として、2つの計算エンジンのいずれかを適応的に選択してフィーチャー関数を実行します。

When a feature request arrives with a small batch size (typically less than eight rows), it executes native C++ functions. 
フィーチャーリクエストが小さなバッチサイズ（通常は8行未満）で到着すると、ネイティブC++関数を実行します。

For larger batch sizes, it uses an LLVM just-in-time (JIT) engine (Gandiva) to compile the feature function as a vectorized Arrow function. 
より大きなバッチサイズの場合、LLVMのジャストインタイム（JIT）エンジン（Gandiva）を使用して、フィーチャー関数をベクトル化されたArrow関数としてコンパイルします。

For smaller batch sizes, the vectorized Arrow function(s) increase latency compared with the native version, while for larger batch sizes, the vectorized execution reduces latency compared with the native version. 
小さなバッチサイズの場合、ベクトル化されたArrow関数はネイティブバージョンと比較してレイテンシを増加させますが、大きなバッチサイズの場合、ベクトル化された実行はネイティブバージョンと比較してレイテンシを減少させます。

###### Handling Failures in Online Inference Pipelines
###### オンライン推論パイプラインにおける障害処理

Model deployments are operational services that need to be robust to data problems, failing or slow feature pipelines, and request failures. 
モデルのデプロイメントは、データの問題、失敗または遅いフィーチャーパイプライン、リクエストの失敗に対して堅牢である必要がある運用サービスです。

Your online inference pipeline should be robust to missing or late feature data and failures in calls to external services. 
オンライン推論パイプラインは、欠落または遅延したフィーチャーデータや外部サービスへの呼び出しの失敗に対して堅牢である必要があります。

Firstly, online inference programs contain logic and read data from potentially many different sources. 
まず、オンライン推論プログラムはロジックを含み、潜在的に多くの異なるソースからデータを読み取ります。

You should log actions (including errors) in your code to standard output (stdout) and standard error (stderr), so that the logs for all deployments are shipped to a centralized logging platform. 
コード内のアクション（エラーを含む）を標準出力（stdout）および標準エラー（stderr）にログに記録する必要があります。これにより、すべてのデプロイメントのログが中央集約型のログプラットフォームに送信されます。

Hopsworks transparently logs `stdout/stderr for deployments to OpenSearch, aggregating the logs and making them searchable via OpenSearch Dashboards. 
Hopsworksは、デプロイメントのために`stdout/stderr`をOpenSearchに透過的にログに記録し、ログを集約してOpenSearch Dashboardsを介して検索可能にします。

Splunk and Elastic are two popular alternative log management systems you could use. 
SplunkとElasticは、使用できる2つの人気のある代替ログ管理システムです。

Log management systems enable alerting when there are errors, real-time troubleshooting, and root-cause analysis for errors in deployments. 
ログ管理システムは、エラーが発生したときのアラート、リアルタイムのトラブルシューティング、およびデプロイメントのエラーに対する根本原因分析を可能にします。

The second main cause of failures is data. 
失敗の主な原因の2つ目はデータです。

Online inference pipelines can receive data from a number of different sources and can be faced with problems such as: 
オンライン推論パイプラインは、さまざまなソースからデータを受け取ることができ、次のような問題に直面する可能性があります：

- Request parameter values may be missing. 
- リクエストパラメータの値が欠落している可能性があります。

- Precomputed features may be missing or delayed because of problems in feature pipelines—feature pipelines may allow missing data or may themselves be slow/delayed. 
- 事前計算されたフィーチャーが欠落しているか、フィーチャーパイプラインの問題により遅延している可能性があります。フィーチャーパイプラインは欠落データを許可する場合があり、遅延することもあります。

- Precomputed features or RAG data may be missing due to the feature store or vector index being inaccessible (due to network or server problems). 
- 事前計算されたフィーチャーやRAGデータは、フィーチャーストアやベクトルインデックスがアクセスできないために欠落している可能性があります（ネットワークやサーバーの問題による）。

- ODTs may have missing or invalid parameter values. 
- ODTには欠落または無効なパラメータ値がある可能性があります。

- MDTs may have missing or invalid parameter values. 
- MDTには欠落または無効なパラメータ値がある可能性があります。

- Third-party API calls may time out or return bad data. 
- サードパーティAPIの呼び出しがタイムアウトしたり、不正なデータを返したりする可能性があります。

Bad data challenges should be handled by data validation logic in feature pipelines for precomputed features. 
不正なデータの課題は、事前計算されたフィーチャーのフィーチャーパイプライン内のデータ検証ロジックによって処理されるべきです。

Your online inference pipeline should handle missing values for request parameters and calls to third-party APIs. 
オンライン推論パイプラインは、リクエストパラメータとサードパーティAPIへの呼び出しの欠落値を処理する必要があります。

You should log missing values to stdout/stderr so that you can identify and troubleshoot problems, but you will still need to design fallback strategies, such as: 
欠落値をstdout/stderrにログに記録して問題を特定し、トラブルシューティングできるようにする必要がありますが、次のようなフォールバック戦略を設計する必要があります：

- Impute missing values: 
- 欠落値を補完する：

— Using mean/median/mode from the training dataset for a numerical feature 
— 数値フィーチャーのためにトレーニングデータセットから平均/中央値/最頻値を使用する

— Model-based imputation using a lightweight predictive model 
— 軽量な予測モデルを使用したモデルベースの補完

- Replace missing values with default values. 
- 欠落値をデフォルト値で置き換えます。

- Use cached or historical values if you cannot retrieve the latest value for features from the feature store. 
- フィーチャーストアから最新のフィーチャー値を取得できない場合は、キャッシュまたは履歴値を使用します。

For example, you could add a threadsafe dict where the key is the serving key(s) for your feature view and the value is the most recently returned row for the serving key(s). 
例えば、フィーチャービューのサービングキーがキーで、サービングキーに対して最も最近返された行が値であるスレッドセーフな辞書を追加できます。

You should only take the most recent value from the cache if the latest feature value(s) cannot be retrieved from the feature store. 
最新のフィーチャー値をフィーチャーストアから取得できない場合は、キャッシュから最も最近の値のみを取得する必要があります。

- Fall back to a simpler model if data is missing. 
- データが欠落している場合は、より単純なモデルにフォールバックします。

###### Model Deployment SLOs
###### モデルデプロイメントのSLO

Model prediction latency can be low when testing but high in a deployed model. 
モデルの予測レイテンシは、テスト時には低いが、デプロイされたモデルでは高くなる可能性があります。

Why is that? 
なぜでしょうか？

Figure 11-8 shows that the total latency is the sum of the time taken for all the steps in your online inference pipeline. 
図11-8は、総レイテンシがオンライン推論パイプライン内のすべてのステップにかかる時間の合計であることを示しています。

_Figure 11-8. Breakdown of the latency for the different steps in an online model prediction._ 
_図11-8. オンラインモデル予測におけるさまざまなステップのレイテンシの内訳。_

You may need to retrieve precomputed features from a feature store or a vector index, create features from request parameters with ODTs, apply MDTs, call predict on the model, and log feature values and the prediction(s), before returning the prediction response. 
フィーチャーストアまたはベクトルインデックスから事前計算されたフィーチャーを取得し、ODTを使用してリクエストパラメータからフィーチャーを作成し、MDTを適用し、モデルに対して予測を呼び出し、フィーチャー値と予測をログに記録してから、予測応答を返す必要があります。

All of these steps add latency to the prediction request, as does network latency from the client to the model deployment. 
これらすべてのステップは、予測リクエストにレイテンシを追加し、クライアントからモデルデプロイメントへのネットワークレイテンシも同様です。

In KServe, if you split your InferenceService into transformer and predictor containers, it will also add latency. 
KServeでは、InferenceServiceをトランスフォーマーと予測器のコンテナに分割すると、レイテンシが追加されます。

For lower latency, use only a predictor container, if possible. 
レイテンシを低くするためには、可能であれば予測器コンテナのみを使用してください。

Hopsworks’ library implements a number of the techniques to reduce feature retrieval latency: 
Hopsworksのライブラリは、フィーチャー取得レイテンシを減少させるためのいくつかの技術を実装しています：

- Issuing parallel primary key lookups to tables for multiple serving keys in a feature view 
- フィーチャービュー内の複数のサービングキーに対してテーブルへの並列プライマリキーのルックアップを発行する

- Pushing down `LEFT JOINs to RonDB when you have a snowflake schema data model 
- スノーフレークスキーマデータモデルを持つ場合、RonDBに`LEFT JOIN`をプッシュダウンする

- Pushing down projections in RonDB to only read the features you need from the feature group(s) represented in the feature view 
- フィーチャービューに表されるフィーチャーグループから必要なフィーチャーのみを読み取るためにRonDBにプロジェクションをプッシュダウンする

- Pushing down aggregations to RonDB for request-time aggregations 
- リクエスト時の集計のためにRonDBに集計をプッシュダウンする

- Asynchronous nonblocking logging in a separate thread of control 
- 別の制御スレッドでの非同期ノンブロッキングログ

For RAG, you can reduce latency by reducing k, the number of responses in similarity search. 
RAGの場合、類似検索における応答の数kを減少させることでレイテンシを減少させることができます。

For function calling with LLMs, you need to be careful that the function or tool you are calling provides a response or returns with an error within the bounded amount of time. 
LLMを使用した関数呼び出しの場合、呼び出している関数やツールが制限された時間内に応答を提供するか、エラーを返すことに注意する必要があります。

For any data retrieval steps that make network calls, you need to set low timeouts for failures due to a network failure or service failure. 
ネットワーク呼び出しを行うデータ取得ステップについては、ネットワーク障害やサービス障害による失敗のために低いタイムアウトを設定する必要があります。

If the timeout expires without a response, your online inference pipeline should catch the exception, and depending on whether the SLO allows it, it can either retry the call or impute the missing feature data. 
タイムアウトが応答なしに期限切れになった場合、オンライン推論パイプラインは例外をキャッチし、SLOが許可するかどうかに応じて、呼び出しを再試行するか、欠落したフィーチャーデータを補完することができます。

###### Inference with Embedded Models
###### 埋め込みモデルによる推論

Many AI-enabled applications cannot afford or tolerate network calls to retrieve precomputed features or third-party data. 
多くのAI対応アプリケーションは、事前計算されたフィーチャーやサードパーティデータを取得するためのネットワーク呼び出しを許容できません。

For example, self-driving vehicles, robots, and high-frequency trading systems require model predictions to return within some latency bound, such as 1 ms or 50 μs. 
例えば、自動運転車、ロボット、高頻度取引システムは、モデルの予測が1ミリ秒または50マイクロ秒などのレイテンシ制約内で返されることを要求します。

Even though many developers believe “fast” is synonymous with real time, real-time systems are characterized primarily by their requirement that operations complete within a fixed time interval. 
多くの開発者が「速い」ということはリアルタイムと同義であると考えていますが、リアルタイムシステムは主に、操作が固定された時間間隔内で完了する必要があるという要件によって特徴付けられます。

The best way to ensure bounded latency is to use either an embedded model or a host-local model. 
制限されたレイテンシを確保する最良の方法は、埋め込みモデルまたはホストローカルモデルのいずれかを使用することです。

You typically need to remove dependencies on unreliable networks (the internet only provides best-effort guarantees) or distributed services (that can fail or be slow). 
通常、信頼性のないネットワーク（インターネットは最善の努力の保証のみを提供します）や分散サービス（失敗したり遅くなったりする可能性がある）への依存を取り除く必要があります。

Applications with embedded models can either distribute the models with the application package, such as by adding the models to your container, or download the models from a model registry to local storage. 
埋め込みモデルを持つアプリケーションは、アプリケーションパッケージと一緒にモデルを配布するか（たとえば、モデルをコンテナに追加する）、モデルレジストリからローカルストレージにモデルをダウンロードすることができます。

Figure 11-9 shows how a model is downloaded from a model registry to a local disk and then loaded either directly in the application or in a model-serving process used by the application. 
図11-9は、モデルがモデルレジストリからローカルディスクにダウンロードされ、その後アプリケーション内で直接またはアプリケーションによって使用されるモデルサービングプロセスで読み込まれる様子を示しています。

_Figure 11-9. High-performance, edge, and embedded applications typically use a model either loaded into the application’s process address space or via interprocess communication (IPC) to a process on the same host that serves prediction requests to the client application._ 
_図11-9. 高性能、エッジ、および埋め込みアプリケーションは、通常、アプリケーションのプロセスアドレス空間に読み込まれたモデルまたは同じホスト上のプロセスへのプロセス間通信（IPC）を介してクライアントアプリケーションに予測リクエストを提供するモデルを使用します。_

By loading the model from local disk (on startup), the application or model-serving process avoids being dependent on the remote model registry being available and accessible. 
ローカルディスクからモデルを読み込むことで（起動時）、アプリケーションまたはモデルサービングプロセスは、リモートモデルレジストリが利用可能でアクセス可能であることに依存することを回避します。



. When designing your embedded model, you need to take into considera‐ tion the limitations of the application’s device. 
埋め込みモデルを設計する際には、アプリケーションのデバイスの制限を考慮する必要があります。

Model predictions are made using the application’s hardware, so if the model needs hardware acceleration, you need to make sure that it will be available on the host.
モデルの予測はアプリケーションのハードウェアを使用して行われるため、モデルがハードウェアアクセラレーションを必要とする場合は、ホストでそれが利用可能であることを確認する必要があります。

###### Embedded AI-Enabled Applications
###### 埋め込みAI対応アプリケーション

Most high-performance and edge applications are not written in Python but rather in compiled languages such as C/C++, Rust, Go, and Java. 
ほとんどの高性能およびエッジアプリケーションはPythonではなく、C/C++、Rust、Go、Javaなどのコンパイル言語で記述されています。

Some ML frameworks are supported in these languages. 
これらの言語ではいくつかのMLフレームワークがサポートされています。

For example, there are C++ libraries and Java Native Interface (JNI) bindings for XGBoost/LightGBM. 
例えば、XGBoost/LightGBMのためのC++ライブラリやJava Native Interface (JNI) バインディングがあります。

You can keep your feature/training pipelines in Python but still use C/C++/Java for embedded inference by loading the model directly into your applications using the language-native library. 
特徴量/トレーニングパイプラインをPythonに保持しつつ、言語ネイティブライブラリを使用してモデルをアプリケーションに直接ロードすることで、埋め込み推論にC/C++/Javaを使用することができます。

Similarly, the ONNX format provides a C++ API, again enabling C++ and Java applications to invoke deep learning models (that typically also require hardware acceleration for good performance).  
同様に、ONNXフォーマットはC++ APIを提供しており、C++およびJavaアプリケーションがディープラーニングモデルを呼び出すことを可能にします（これらは通常、良好なパフォーマンスのためにハードウェアアクセラレーションを必要とします）。

-----
###### Stream-Processing AI-Enabled Applications
###### ストリーム処理AI対応アプリケーション

Stream-processing programs can use embedded models to make predictions on streams of incoming data. 
ストリーム処理プログラムは、埋め込みモデルを使用して、受信データのストリームに対して予測を行うことができます。

For example, network intrusion detection systems process real-time network traffic logs/events from an event-streaming platform to predict whether the current network activity is anomalous (an intrusion attempt) or normal.
例えば、ネットワーク侵入検知システムは、イベントストリーミングプラットフォームからのリアルタイムネットワークトラフィックログ/イベントを処理して、現在のネットワーク活動が異常（侵入試行）か正常かを予測します。

A stream-processing application, written in a framework such as Apache Flink or Spark Structured Streaming, can use an embedded XGBoost classifier to make highthroughput, low-latency predictions for the traffic streams.
Apache FlinkやSpark Structured Streamingなどのフレームワークで記述されたストリーム処理アプリケーションは、埋め込みXGBoost分類器を使用してトラフィックストリームに対して高スループット、低レイテンシの予測を行うことができます。

The following code snippet shows a stream-processing pipeline in Spark Structured Streaming that includes an embedded model to make predictions: 
以下のコードスニペットは、埋め込みモデルを含むSpark Structured Streamingのストリーム処理パイプラインを示しています：

```   
# to enable workers to reuse the cached model persists across tasks, set   
# spark.conf.set("spark.python.worker.reuse", "true")   
schema = StructType([     
    StructField("duration", FloatType(), True),     
    StructField("src_bytes", FloatType(), True),     
    StructField("dst_bytes", FloatType(), True),     
    StructField("flag", StringType(), True)   
])   
xgb_path = # path to model on S3 or HopsFS   
bcast_model_path = spark.sparkContext.broadcast(xgb_path)   
_xgb_model = None   
# Load the model once per worker, instead of once per partition   
def _get_model_once():     
    global _xgb_model     
    if _xgb_model is None:       
        m = xgb.XGBClassifier()       
        m.load_model(bcast_model_path.value)       
        _xgb_model = m     
    return _xgb_model   

@pandas_udf(DoubleType())   
def predict_udf(duration, src_bytes, dst_bytes, flag):     
    features_df = pd.DataFrame({       
        'duration': duration,       
        'src_bytes': src_bytes,       
        'dst_bytes': dst_bytes,       
        'flag': flag     
    })     
    model = _get_model_once()     
    predictions = model.predict(features_df)     
    return pd.Series(predictions, dtype="float64")   

raw_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "IP_ADDRESS_KAFKA_BROKER:9092") \     
    .option("subscribe", "network-traffic") \     
    .option("startingOffsets", "latest") \     
    .load()   

json_stream = raw_stream.selectExpr("CAST(value AS STRING) as json") \     
    .select(from_json(col("json"), schema).alias("data")) \     
    .select("data.*")   

predictions_stream = json_stream.withColumn("prediction",     
    predict_udf(       
        col("duration"), col("src_bytes"), col("dst_bytes"), col("flag")     
    )   
)   

fg_sink = fs.get_feature_group("predictions_fg", version=1)   
query = fg_sink.insert_stream(predictions_stream)   
query.awaitTermination()
```

This program reads data from the network-traffic Kafka topic, including the duration of the traffic flow, the number of bytes that are sent by the source (src_bytes), the number of bytes sent by the destination (dst_bytes), and a flag that represents the state of the connection at the transport layer (typically TCP)—successful, rejected, reset, and so on. 
このプログラムは、ネットワークトラフィックKafkaトピックからデータを読み取り、トラフィックフローの持続時間、送信元が送信したバイト数（src_bytes）、宛先が送信したバイト数（dst_bytes）、およびトランスポート層（通常はTCP）での接続の状態を表すフラグ（成功、拒否、リセットなど）を含みます。

For example, a connection with a long duration where src_bytes is very high and dst_bytes is nearly zero may indicate data exfiltration or a denial-ofservice attack. 
例えば、持続時間が長く、src_bytesが非常に高く、dst_bytesがほぼゼロの接続は、データの流出やサービス拒否攻撃を示す可能性があります。

Similarly, if there are a lot of traffic flows in a short time window from the source IP that has a flag indicating rejected connections, it may indicate port scanning. 
同様に、拒否された接続を示すフラグを持つ送信元IPから短時間に多くのトラフィックフローがある場合、それはポートスキャンを示す可能性があります。

For more details on network intrusion detection with AI, see Sarika [Choudhary and Nishtha Kesswani’s article “Analysis of KDD-Cup’99, NSL-KDD and](https://oreil.ly/Aa2YS) [UNSW-NB15 Datasets using Deep Learning in IoT”.](https://oreil.ly/Aa2YS)
AIを用いたネットワーク侵入検知の詳細については、Sarika [ChoudharyとNishtha Kesswaniの「KDD-Cup’99、NSL-KDDおよび](https://oreil.ly/Aa2YS) [UNSW-NB15データセットの分析に関する記事」を参照してください。](https://oreil.ly/Aa2YS)

###### UIs for AI-Enabled Applications in Python
###### PythonにおけるAI対応アプリケーションのUI

Often, you need to develop a quick UI for your AI system to provide feedback to stakeholders about how the system will work. 
しばしば、AIシステムの動作についてステークホルダーにフィードバックを提供するために、迅速なUIを開発する必要があります。

The heavyweight production approach is to deploy your model on model-serving infrastructure and write a UI in JavaScript. 
重厚な生産アプローチは、モデルをモデル提供インフラストラクチャにデプロイし、UIをJavaScriptで記述することです。

But what if you can’t program in JavaScript? 
しかし、JavaScriptでプログラムできない場合はどうしますか？

Luckily, you can write a UI in Python, download the model, and perform inference locally in the Python program. 
幸いなことに、PythonでUIを記述し、モデルをダウンロードし、Pythonプログラム内でローカルに推論を行うことができます。

Python applications with a UI can be quickly developed using frameworks like Streamlit, Gradio, and Taipy. 
UIを持つPythonアプリケーションは、Streamlit、Gradio、Taipyなどのフレームワークを使用して迅速に開発できます。

Each framework has its own strong points. 
各フレームワークにはそれぞれの強みがあります。

Streamlit simplifies UI creation through declarative, script-based coding. 
Streamlitは、宣言的でスクリプトベースのコーディングを通じてUIの作成を簡素化します。

Gradio programs have a more concise, function-based style, making them more beginner-friendly. 
Gradioプログラムは、より簡潔で関数ベースのスタイルを持ち、初心者に優しいものとなっています。

Taipy enables better integration of JavaScript and CSS to build more sophisticated UIs. 
Taipyは、JavaScriptとCSSのより良い統合を可能にし、より洗練されたUIを構築します。

As Python programs, they can download a model from the model registry and use it as an embedded model. 
Pythonプログラムとして、モデルレジストリからモデルをダウンロードし、埋め込みモデルとして使用することができます。

This is often the quickest UI you can build for your AI system, and sometimes, it can even be the final UI for your AI system.
これは、AIシステムのために構築できる最も迅速なUIであり、時にはAIシステムの最終的なUIとなることさえあります。



For our credit card fraud system, there is a Streamlit UI in the book’s source repository. 
私たちのクレジットカード詐欺システムには、本のソースリポジトリにStreamlit UIがあります。

The UI allows you to generate synthetic credit card transactions and notifies you when the model flags transactions as fraudulent. 
このUIでは、合成クレジットカード取引を生成でき、モデルが取引を詐欺としてフラグ付けしたときに通知されます。

One challenge with Streamlit is that it is not easy to refresh selected parts of the UI. 
Streamlitの課題の一つは、UIの選択した部分を簡単に更新できないことです。

Streamlit refreshes the whole UI at the same time, which results in the execution of all of the Python code in your UI program. 
StreamlitはUI全体を同時に更新するため、UIプログラム内のすべてのPythonコードが実行されます。

The code is structured at a high level as follows: 
コードは高レベルで次のように構成されています：

```   
   import streamlit as st   
   @st.cache_data()   
   def download_model():     
     …   
   @st.cache_resource()   
   def read_batch_inference_data():      
     …   
   if submit_button:     
     df["prediction"] = model.predict(df)     
     st.dataframe(df)
```

Decorators are used here to cache function outputs so that they don’t get recomputed on every rerun: 
ここでは、デコレーターを使用して関数の出力をキャッシュし、再実行のたびに再計算されないようにしています：

- @st.cache_data is used on pure, deterministic functions and caches the return values. 
- @st.cache_dataは、純粋で決定論的な関数に使用され、戻り値をキャッシュします。

- @st.cache_resource is used by functions that return stateful (resource-heavy) objects such as a DataFrame of inference data read from the feature store. 
- @st.cache_resourceは、フィーチャーストアから読み取った推論データのDataFrameのような状態を持つ（リソース集約型の）オブジェクトを返す関数によって使用されます。

For our credit card fraud example, you should cache the model and feature view objects, so you don’t have to redownload them every time the UI is refreshed. 
クレジットカード詐欺の例では、モデルとフィーチャービューオブジェクトをキャッシュする必要があります。そうすれば、UIが更新されるたびに再ダウンロードする必要がありません。

###### Summary and Exercises 要約と演習

This chapter examined batch, online, embedded, and streaming inference pipelines. 
この章では、バッチ、オンライン、埋め込み、ストリーミング推論パイプラインを検討しました。

For batch inference, we looked at how to retrieve a time range of inference data and inference data for entities using feature views, as well as how to scale batch inference with PySpark. 
バッチ推論では、フィーチャービューを使用して推論データの時間範囲やエンティティの推論データを取得する方法、さらにPySparkを使用してバッチ推論をスケールする方法を見ました。

For online inference pipelines, we introduced deployment APIs to hide model signatures, and we looked at how to optimize online inference for latency and throughput with Python/Pandas/native UDFs, handling failures, and meeting SLOs. 
オンライン推論パイプラインでは、モデルのシグネチャを隠すためのデプロイメントAPIを導入し、Python/Pandas/native UDFsを使用してレイテンシとスループットの最適化、障害処理、SLOの達成方法を見ました。

For LLMs, we looked at API-based batch inference and GPU-serving with KServe.  
LLMについては、APIベースのバッチ推論とKServeを使用したGPUサービングを見ました。

Do the following exercises to help you learn how to scale your inference pipelines: 
以下の演習を行い、推論パイプラインをスケールする方法を学びましょう：

- Build a batch inference pipeline for product recommendations. 
- 製品推薦のためのバッチ推論パイプラインを構築します。

Your model was trained only on products available in the US—your products table has a “country” column (i.e., `country = 'US'). 
あなたのモデルは、米国で利用可能な製品のみで訓練されました—あなたの製品テーブルには「country」列があります（つまり、`country = 'US'）。

Describe how you would ensure that only correct batch inference data is retrieved for batch inference. 
バッチ推論のために正しいバッチ推論データのみが取得されることをどのように保証するかを説明してください。

- When you use PySpark and an XGBoost model for batch inference, what are the trade-offs between broadcasting the model as a JSON string and loading it from distributed storage on each executor? 
- PySparkとXGBoostモデルを使用してバッチ推論を行う場合、モデルをJSON文字列としてブロードキャストすることと、各エグゼキュータで分散ストレージからロードすることのトレードオフは何ですか？

- You want to deploy an online inference pipeline for real-time credit card fraud predictions with p99 10 ms. 
- p99 10 msのリアルタイムクレジットカード詐欺予測のためのオンライン推論パイプラインをデプロイしたいと考えています。

Describe how you would minimize latency across the pipeline, considering transformation functions, model loading, feature retrieval, and logging.  
変換関数、モデルのロード、フィーチャーの取得、ロギングを考慮して、パイプライン全体のレイテンシをどのように最小化するかを説明してください。



