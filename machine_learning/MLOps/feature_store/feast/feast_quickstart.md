# Quickstart クイックスタート  
## What is Feast? Feastとは何ですか？

Feast (Feature Store) is an open-source feature store designed to facilitate the management and serving of machine learning features in a way that supports both batch and real-time applications.
Feast（フィーチャーストア）は、バッチおよびリアルタイムアプリケーションの両方をサポートする方法で、機械学習の特徴の管理と提供を容易にするために設計されたオープンソースのフィーチャーストアです。

- For Data Scientists: Feast is a a tool where you can easily define, store, and retrieve your features for both model development and model deployment. 
- データサイエンティスト向け：Feastは、モデル開発とモデルデプロイメントの両方のために、特徴を簡単に定義、保存、取得できるツールです。
By using Feast, you can focus on what you do best: build features that power your AI/ML models and maximize the value of your data.
Feastを使用することで、あなたは自分が得意とすることに集中できます：AI/MLモデルを支える特徴を構築し、データの価値を最大化することです。

- For MLOps Engineers: Feast is a library that allows you to connect your existing infrastructure (e.g., online database, application server, microservice, analytical database, and orchestration tooling) that enables your Data Scientists to ship features for their models to production using a friendly SDK without having to be concerned with software engineering challenges that occur from serving real-time production systems. 
- MLOpsエンジニア向け：Feastは、既存のインフラストラクチャ（例：オンラインデータベース、アプリケーションサーバー、マイクロサービス、分析データベース、オーケストレーションツール）を接続できるライブラリであり、データサイエンティストがリアルタイムのプロダクションシステムから発生するソフトウェアエンジニアリングの課題を気にせずに、フレンドリーなSDKを使用してモデルの特徴をプロダクションに出荷できるようにします。
By using Feast, you can focus on maintaining a resilient system, instead of implementing features for Data Scientists.
Feastを使用することで、データサイエンティストのための機能を実装するのではなく、レジリエントなシステムの維持に集中できます。

- For Data Engineers: Feast provides a centralized catalog for storing feature definitions allowing one to maintain a single source of truth for feature data. 
- データエンジニア向け：Feastは、特徴定義を保存するための中央カタログを提供し、特徴データの単一の真実のソースを維持できるようにします。
It provides the abstraction for reading and writing to many different types of offline and online data stores. 
**さまざまなタイプのオフラインおよびオンラインデータストアへの読み書きのための抽象化を提供**します。
Using either the provided python SDK or the feature server service, users can write data to the online and/or offline stores and then read that data out again in either low-latency online scenarios for model inference, or in batch scenarios for model training.
提供されたPython SDKまたはフィーチャーサーバーサービスを使用して、**ユーザーはオンラインおよび/またはオフラインストアにデータを書き込み**、その後、**モデル推論のための低遅延オンラインシナリオまたはモデルトレーニングのためのバッチシナリオでそのデータを再度読み取ることができます**。

- For AI Engineers: Feast provides a platform designed to scale your AI applications by enabling seamless integration of richer data and facilitating fine-tuning. 
- AIエンジニア向け：Feastは、より豊富なデータのシームレスな統合を可能にし、ファインチューニングを促進することで、AIアプリケーションをスケールさせるために設計されたプラットフォームを提供します。
With Feast, you can optimize the performance of your AI models while ensuring a scalable and efficient data pipeline.
Feastを使用することで、スケーラブルで効率的なデータパイプラインを確保しながら、AIモデルのパフォーマンスを最適化できます。

For more info refer to Introduction to feast
詳細については、[Introduction to feast](https://docs.feast.dev/getting-started/quickstart#:~:text=Introduction%20to%20feast)を参照してください。


## Prerequisites 前提条件

- Ensure that you have Python (3.9 or above) installed.
- Python（3.9以上）がインストールされていることを確認してください。
- It is recommended to create and work in a virtual environment:
- 仮想環境を作成し、その中で作業することをお勧めします：

```shell
# create & activate a virtual environment 仮想環境の作成とアクティベート
python -m venv venv/  
source venv/bin/activate  
```

## Overview 概要

In this tutorial we will:
このチュートリアルでは、以下のことを行います。

1. Deploy a local feature store with a Parquet file offline store and Sqlite online store.
ParquetファイルのオフラインストアとSqliteオンラインストアを使用して、ローカルフィーチャーストアを展開します。(あ、オンラインストアでSqlite使えるのか...!!:thinking:)

2. Build a training dataset using our time series features from our Parquet files.
Parquetファイルからの時系列フィーチャーを使用して、トレーニングデータセットを構築します。

3. Ingest batch features ("materialization") and streaming features (via a Push API) into the online store.
バッチフィーチャー（「マテリアライゼーション」）とストリーミングフィーチャー（Push API経由）をオンラインストアに取り込みます。

4. Read the latest features from the offline store for batch scoring.
バッチスコアリングのためにオフラインストアから最新のフィーチャーを読み取ります。

5. Read the latest features from the online store for real-time inference.
リアルタイム推論のためにオンラインストアから最新のフィーチャーを読み取ります。

6.  Explore the (experimental) Feast UI.
（実験的な）Feast UIを探索します。

Note- Feast provides a python SDK as well as an optional hosted service for reading and writing feature data to the online and offline data stores. 
注意 - Feastは、オンラインおよびオフラインデータストアにフィーチャーデータを読み書きするためのPython SDKと**オプションのホスティングサービス**を提供します。
The latter might be useful when non-python languages are required.
**後者は、非Python言語が必要な場合に便利**です。(なるほど...!:thinking:)

For this tutorial, we will be using the python SDK.
このチュートリアルでは、Python SDKを使用します。

In this tutorial, we'll use Feast to generate training data and power online model inference for a ride-sharing driver satisfaction prediction model.
このチュートリアルでは、Feastを使用してトレーニングデータを生成し、ライドシェアのドライバー満足度予測モデルのオンラインモデル推論を行います。
Feast solves several common issues in this flow:
Feastは、このフローにおけるいくつかの一般的な問題を解決します。

1. Training-serving skew and complex data joins: Feature values often exist across multiple tables. 
トレーニングとサービングのずれと複雑なデータ結合：フィーチャー値はしばしば複数のテーブルに存在します。
Joining these datasets can be complicated, slow, and error-prone.
これらのデータセットを結合することは、複雑で遅く、エラーが発生しやすい場合があります。
Feast joins these tables with battle-tested logic that ensures point-in-time correctness so future feature values do not leak to models.
Feastは、**将来のフィーチャー値がモデルに漏れないように、時点正確性を保証**する実績のあるロジックでこれらのテーブルを結合します。

2. Online feature availability: At inference time, models often need access to features that aren't readily available and need to be precomputed from other data sources.
オンラインフィーチャーの可用性：推論時に、モデルはしばしばすぐに利用できないフィーチャーにアクセスする必要があり、他のデータソースから事前に計算する必要があります。
Feast manages deployment to a variety of online stores (e.g. DynamoDB, Redis, Google Cloud Datastore) and ensures necessary features are consistently available and freshly computed at inference time.
Feastは、さまざまなオンラインストア（例：DynamoDB、Redis、Google Cloud Datastore）への展開を管理し、推論時に必要なフィーチャーが一貫して利用可能で新鮮に計算されることを保証します。

3. Feature and model versioning: Different teams within an organization are often unable to reuse features across projects, resulting in duplicate feature creation logic.
フィーチャーとモデルのバージョン管理：組織内の異なるチームは、プロジェクト間でフィーチャーを再利用できないことが多く、重複したフィーチャー作成ロジックが生じます。
Models have data dependencies that need to be versioned, for example when running A/B tests on model versions.
モデルには、データ依存関係があり、モデルバージョンでA/Bテストを実行する際にバージョン管理が必要です。
   - Feast enables discovery of and collaboration on previously used features and enables versioning of sets of features (via feature services).
    Feastは、以前に使用されたフィーチャーの発見とコラボレーションを可能にし、フィーチャーサービスを介してフィーチャーのセットのバージョン管理を可能にします。
   - (Experimental) Feast enables light-weight feature transformations so users can re-use transformation logic across online / offline use cases and across models.
    （実験的）Feastは、ユーザーがオンライン/オフラインのユースケースやモデル間で変換ロジックを再利用できるように、軽量のフィーチャー変換を可能にします。

## Step 1: Install Feast ステップ 1: Feastのインストール

Install the Feast SDK and CLI using pip: 
pipを使用してFeast SDKとCLIをインストールします：

- In this tutorial, we focus on a local deployment. 
このチュートリアルでは、ローカルデプロイメントに焦点を当てます。
- For a more in-depth guide on how to use Feast with Snowflake / GCP / AWS deployments, see Running Feast with Snowflake/GCP/AWS 
FeastをSnowflake / GCP / AWSデプロイメントで使用する方法についての詳細なガイドは、[Running Feast with Snowflake/GCP/AWS](https://docs.feast.dev/how-to-guides/feast-snowflake-gcp-aws)を参照してください。

```
pip install feast
```

## Step 2: Create a feature repository ステップ2: フィーチャーリポジトリの作成

Bootstrap a new feature repository using `feast init` from the command line.
コマンドラインから `feast init` を使用して新しいフィーチャーリポジトリをブートストラップします。

```
feast init my_project
cd my_project/feature_repo
```

```
Creating a new Feast repository in /home/Jovyan/my_project.
```

Let's take a look at the resulting demo repo itself. It breaks down into
結果として得られるデモリポジトリを見てみましょう。それは以下のように分かれています。
- `data/` contains raw demo parquet data. `data/` には生のデモパーケットデータが含まれています
- `example_repo.py` contains demo feature definitions. `example_repo.py` にはデモフィーチャー定義が含まれています
- `feature_store.yaml` contains a demo setup configuring where data sources are. `feature_store.yaml` にはデータソースの設定を構成するデモセットアップが含まれています
- `test_workflow.py` showcases how to run all key Feast commands, including defining, retrieving, and pushing features.`test_workflow.py` では、フィーチャーの定義、取得、プッシュを含むすべての主要な Feast コマンドを実行する方法が紹介されています。

You can run this with `python test_workflow.py`.
これを実行するには `python test_workflow.py` を使用できます。

```yml:feature_store.yaml
project: my_project
# By default, the registry is a file (but can be turned into a more scalable SQL-backed registry)
registry: data/registry.db
# The provider primarily specifies default offline / online stores & storing the registry in a given cloud
provider: local
online_store:
  type: sqlite
  path: data/online_store.db
entity_key_serialization_version: 2
```

The feature_store.yaml file configures the key overall architecture of the feature store. 
**feature_store.yamlファイルは、フィーチャーストアの全体的なアーキテクチャの主要な設定を構成**します。 

The provider value sets default offline and online stores. 
provider値は、デフォルトのオフラインおよびオンラインストアを設定します。 
- The offline store provides the compute layer to process historical data (for generating training data & feature values for serving). オフラインストアは、履歴データを処理するための計算レイヤーを提供します（トレーニングデータと提供用のフィーチャー値を生成するため）。 
- The online store is a low latency store of the latest feature values (for powering real-time inference). オンラインストアは、最新のフィーチャー値の低遅延ストアです（リアルタイム推論を支えるため）。 

Valid values for provider in feature_store.yaml are: 
feature_store.yamlのproviderの有効な値は次のとおりです： 
- local: use a SQL registry or local file registry. By default, use a file / Dask based offline store + SQLite online store. local: SQLレジストリまたはローカルファイルレジストリを使用します。デフォルトでは、ファイル/Daskベースのオフラインストア + SQLiteオンラインストアを使用します。 
- gcp: use a SQL registry or GCS file registry. By default, use BigQuery (offline store) + Google Cloud Datastore (online store). gcp: SQLレジストリまたはGCSファイルレジストリを使用します。デフォルトでは、BigQuery（オフラインストア） + Google Cloud Datastore（オンラインストア）を使用します。 
- aws: use a SQL registry or S3 file registry. By default, use Redshift (offline store) + DynamoDB (online store) . aws: SQLレジストリまたはS3ファイルレジストリを使用します。デフォルトでは、Redshift（オフラインストア） + DynamoDB（オンラインストア）を使用します。

Note that there are many other offline / online stores Feast works with, including Spark, Azure, Hive, Trino, and PostgreSQL via community plugins. 
**Feastが対応している他の多くのオフライン/オンラインストア（Spark、Azure、Hive、Trino、PostgreSQLなどのコミュニティプラグインを介して）があります**ので注意してください。 
See Third party integrations for all supported data sources. 
すべてのサポートされているデータソースについては、[サードパーティ統合](https://docs.feast.dev/getting-started/third-party-integrations)を参照してください。 
A custom setup can also be made by following Customizing Feast. 
[Feastのカスタマイズ](https://docs.feast.dev/getting-started/quickstart#:~:text=made%20by%20following-,Customizing%20Feast,-.)に従うことで、カスタムセットアップも可能です。 

<!-- ここまで読んだ! -->

### Inspecting the raw data 生データの検査

The raw feature data we have in this demo is stored in a local parquet file. 
このデモで使用する生の特徴データは、ローカルのparquetファイルに保存されています。

The dataset captures hourly stats of a driver in a ride-sharing app.
このデータセットは、ライドシェアアプリにおけるドライバーの時間ごとの統計を記録しています。

```
import pandas as pd
pd.read_parquet("data/driver_stats.parquet")
```


## Step 3: Run sample workflow ステップ3: サンプルワークフローの実行

There's an included test_workflow.py file which runs through a full sample workflow: 
含まれている test_workflow.py ファイルは、完全なサンプルワークフローを実行します。

1. Register feature definitions through feast apply 
feast apply を通じてフィーチャー定義を登録します。

2. Generate a training dataset (using get_historical_features) 
トレーニングデータセットを生成します（get_historical_features を使用）。

3. Generate features for batch scoring (using get_historical_features) 
バッチスコアリング用のフィーチャーを生成します（get_historical_features を使用）。

4. Ingest batch features into an online store (using materialize_incremental) 
バッチフィーチャーをオンラインストアに取り込みます（materialize_incremental を使用）。

5. Fetch online features to power real time inference (using get_online_features) 
リアルタイム推論を行うためにオンラインフィーチャーを取得します（get_online_features を使用）。

6.  Ingest streaming features into offline / online stores (using push) 
ストリーミングフィーチャーをオフライン/オンラインストアに取り込みます（push を使用）。

7.  Verify online features are updated / fresher 
オンラインフィーチャーが更新されているか、新しいかを確認します。

We'll walk through some snippets of code below and explain 
以下にいくつかのコードスニペットを示し、説明します。

### Step 4: Register feature definitions and deploy your feature store
### ステップ4: フィーチャー定義を登録し、フィーチャーストアをデプロイする

The apply command scans python files in the current directory for feature view/entity definitions, registers the objects, and deploys infrastructure. 
`apply`コマンドは、現在のディレクトリ内のPythonファイルをスキャンしてフィーチャービュー/エンティティ定義を探し、オブジェクトを登録し、インフラストラクチャをデプロイします。
In this example, it reads example_repo.py and sets up SQLite online store tables. 
この例では、`example_repo.py`を読み込み、SQLiteオンラインストアのテーブルを設定します。

Note that we had specified SQLite as the default online store by configuring online_store in feature_store.yaml. 
`feature_store.yaml`で`online_store`を設定することにより、SQLiteをデフォルトのオンラインストアとして指定していることに注意してください。

```shell
feast apply
```

```shell
# output
Created entity driver
Created feature view driver_hourly_stats
Created feature view driver_hourly_stats_fresh
Created on demand feature view transformed_conv_rate
Created on demand feature view transformed_conv_rate_fresh
Created feature service driver_activity_v3
Created feature service driver_activity_v1
Created feature service driver_activity_v2

Created sqlite table my_project_driver_hourly_stats_fresh
Created sqlite table my_project_driver_hourly_stats
```

### Step 5: Generating training data or powering batch scoring models
### ステップ5: トレーニングデータの生成またはバッチスコアリングモデルの強化

To train a model, we need features and labels. 
モデルをトレーニングするには、特徴量とラベルが必要です。
Often, this label data is stored separately (e.g. you have one table storing user survey results and another set of tables with feature values). 
**このラベルデータはしばしば別々に保存されます**（例: ユーザ調査結果を保存するテーブルと特徴量の値を持つ別のテーブルがあります）。
Feast can help generate the features that map to these labels. 
Feastは、これらのラベルにマッピングされる特徴量を生成するのに役立ちます。

Feast needs a list of entities (e.g. driver ids) and timestamps. 
**Feastは、エンティティのリスト（例: ドライバーID）とタイムスタンプを必要とします**。
Feast will intelligently join relevant tables to create the relevant feature vectors. 
Feastは、関連するテーブルをインテリジェントに結合して、関連する特徴ベクトルを作成します。
There are two ways to generate this list: 
この**リストを生成する方法は2つ**あります。

1. The user can query that table of labels with timestamps and pass that into Feast as an entity dataframe for training data generation. 
ユーザは、**タイムスタンプ付きのラベルのテーブルをクエリし、それをFeastにエンティティデータフレームとして渡して**トレーニングデータを生成できます。

2. The user can also query that table with a SQL query which pulls entities. 
ユーザは、エンティティを引き出すSQLクエリを使用してそのテーブルをクエリすることもできます。
See the documentation on feature retrieval for details. 
詳細については、[特徴量取得に関するドキュメント](https://docs.feast.dev/getting-started/concepts/feature-retrieval)を参照してください。

- Note that we include timestamps because we want the features for the same driver at various timestamps to be used in a model. 
- タイムスタンプを含める理由は、同じドライバーのさまざまなタイムスタンプでの特徴量をモデルで使用したいためです。(point-in-time機能のためだよね...!:thinking:)

<!-- ここまで読んだ -->

#### Generating training data トレーニングデータの生成

```python
from datetime import datetime
import pandas as pd

from feast import FeatureStore

# Note: see https://docs.feast.dev/getting-started/concepts/feature-retrieval for 
# more details on how to retrieve for all entities in the offline store instead
entity_df = pd.DataFrame.from_dict(
    {
        # entity's join key -> entity values
        "driver_id": [1001, 1002, 1003],
        # "event_timestamp" (reserved key) -> timestamps
        "event_timestamp": [
            datetime(2021, 4, 12, 10, 59, 42),
            datetime(2021, 4, 12, 8, 12, 10),
            datetime(2021, 4, 12, 16, 40, 26),
        ],
        # (optional) label name -> label values. Feast does not process these
        "label_driver_reported_satisfaction": [1, 5, 3],
        # values we're using for an on-demand transformation
        "val_to_add": [1, 2, 3],
        "val_to_add_2": [10, 20, 30],
    }
)

store = FeatureStore(repo_path=".")

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
        "transformed_conv_rate:conv_rate_plus_val1",
        "transformed_conv_rate:conv_rate_plus_val2",
    ],
).to_df()

print("----- Feature schema -----\n")
print(training_df.info())

print()
print("----- Example features -----\n")
print(training_df.head())
```

#### Run offline inference (batch scoring) オフライン推論を実行する（バッチスコアリング）

To power a batch model, we primarily need to generate features with the get_historical_features call, but using the current timestamp
バッチモデルを動かすためには、主にget_historical_features呼び出しで特徴を生成する必要がありますが、**現在のタイムスタンプを使用**します。

```python
entity_df["event_timestamp"] = pd.to_datetime("now", utc=True)
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
        "transformed_conv_rate:conv_rate_plus_val1",
        "transformed_conv_rate:conv_rate_plus_val2",
    ],
).to_df()

print("\n----- Example features -----\n")
print(training_df.head()) # training_dfっていうか、inference_dfじゃない??:thinking:
```

<!-- ここまで読んだ! -->

### Step 6: Ingest batch features into your online store ステップ6: バッチ特徴をオンラインストアに取り込む(バッチのput)

We now serialize the latest values of features since the beginning of time to prepare for serving. 
私たちは、サービス提供の準備のために、時間の始まりからの特徴の最新の値をシリアライズします。
Note, materialize_incremental serializes all new features since the last materialize call, or since the time provided minus the ttl timedelta. 
注意してください。`materialize_incremental`は、最後のmaterialize呼び出し以降のすべての新しい特徴をシリアライズします。または、提供された時間からttlタイムデルタを引いた時間以降のものです。
In this case, this will be CURRENT_TIME - 1 day (ttl was set on the FeatureView instances in feature_repo/feature_repo/example_repo.py). 
この場合、これはCURRENT_TIME - 1日になります（ttlはfeature_repo/feature_repo/example_repo.pyのFeatureViewインスタンスに設定されていました）。

```bash
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S") feast materialize-incremental $CURRENT_TIME
```

```bash
Materializing 2 feature views to 2024-04-19 10:59:58-04:00 into the sqlite online store. 
2024-04-19 10:59:58-04:00にsqliteオンラインストアに2つの特徴ビューをマテリアライズしています。

driver_hourly_stats from 2024-04-18 15:00:46-04:00 to 2024-04-19 10:59:58-04:00: 
2024-04-18 15:00:46-04:00から2024-04-19 10:59:58-04:00までのdriver_hourly_stats:

100%|████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 370.32it/s] 
100%|████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 370.32it/s] 
```

### Step 7: Fetching feature vectors for inference 推論のための特徴ベクトルの取得(リアルタイムのget)

At inference time, we need to quickly read the latest feature values for different drivers (which otherwise might have existed only in batch sources) from the online feature store using get_online_features(). 
推論時には、オンラインフィーチャーストアから`get_online_features()`を使用して、異なるドライバーの最新のフィーチャー値を迅速に読み取る必要があります（そうでなければバッチソースにのみ存在している可能性があります）。 
These feature vectors can then be fed to the model. 
これらの特徴ベクトルは、その後モデルに供給されます。

```python
from pprint import pprint
from feast import FeatureStore

store = FeatureStore(repo_path=".")
feature_vector = store.get_online_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
    entity_rows=[
        # {join_key: entity_value}
        {"driver_id": 1004},
        {"driver_id": 1005},
    ],
).to_dict()

pprint(feature_vector)
```

```md
<!-- Output -->
<!-- あ、今回は2件分をリアルタイムでgetしたのか。まあ実際は基本1件ずつなのかな -->
{
 'acc_rate': [0.25351759791374207, 0.8949751853942871],
 'avg_daily_trips': [712, 791],
 'conv_rate': [0.5038306713104248, 0.9839504361152649],
 'driver_id': [1004, 1005]
 }
```

### Step 8: Using a feature service to fetch online features instead. ステップ8: フィーチャーサービスを使用してオンラインフィーチャーを取得する

<!-- これはPython SDKを使わないケースの話かな?? もしくはPython SDKの別メソッドの話?? -->
<!-- 後者の話だった! -->

You can also use feature services to manage multiple features, and decouple feature view definitions and the features needed by end applications. 
複数のフィーチャーを管理するためにフィーチャーサービスを使用し、フィーチャービューの定義とエンドアプリケーションが必要とするフィーチャーを切り離すこともできます。
The feature store can also be used to fetch either online or historical features using the same API below. 
フィーチャーストアは、以下の同じAPIを使用してオンラインまたは履歴のフィーチャーを取得するためにも使用できます。
More information can be found here. 
詳細情報は[ここ](https://docs.feast.dev/getting-started/concepts/feature-retrieval)にあります。

The driver_activity_v1 feature service pulls all features from the driver_hourly_stats feature view: 
driver_activity_v1フィーチャーサービスは、driver_hourly_statsフィーチャービューからすべてのフィーチャーを取得します：

```python
from feast import FeatureService
driver_stats_fs = FeatureService(
    name="driver_activity_v1", features=[driver_stats_fv]
)
```

```python 
from pprint import pprint
from feast import FeatureStore
feature_store = FeatureStore('.')  # Initialize the feature store

feature_service = feature_store.get_feature_service("driver_activity_v1")
feature_vector = feature_store.get_online_features(
    features=feature_service,
    entity_rows=[
        # {join_key: entity_value}
        {"driver_id": 1004},
        {"driver_id": 1005},
    ],
).to_dict()
pprint(feature_vector)
```


```md
{
 'acc_rate': [0.5732735991477966, 0.7828438878059387],
 'avg_daily_trips': [33, 984],
 'conv_rate': [0.15498852729797363, 0.6263588070869446],
 'driver_id': [1004, 1005]
}
```

## Step 9: Browse your features with the Web UI (experimental) ステップ9: Web UIを使って機能をブラウズする（実験的）

View all registered features, data sources, entities, and feature services with the Web UI. 
Web UIを使用して、すべての登録された**特徴量、データソース、エンティティ、および特徴量サービスを表示**します。(この辺りのfeastの概念、まだよくわかってない...!:thinking:)
One of the ways to view this is with the `feast ui` command. 
これを表示する方法の一つは、`feast ui`コマンドを使用することです。

```bash
feast ui
```

```bash
INFO:     Started server process [66664]08/17/2022 01:25:49 PM uvicorn.error INFO: Started server process [66664]INFO:     Waiting for application startup.08/17/2022 01:25:49 PM uvicorn.error INFO: Waiting for application startup.INFO:     Application startup complete.08/17/2022 01:25:49 PM uvicorn.error INFO: Application startup complete.INFO:     Uvicorn running on http://0.0.0.0:8888 (Press CTRL+C to quit)08/17/2022 01:25:49 PM uvicorn.error INFO: Uvicorn running on http://0.0.0.0:8888 (Press CTRL+C to quit)
```

## Step 10: Re-examinetest_workflow.py ステップ10: test_workflow.pyの再検討

Take a look attest_workflow.pyagain. 
test_workflow.pyを再度見てみましょう。
It showcases many sample flows on how to interact with Feast. 
これは、Feastとどのように対話するかの多くのサンプルフローを示しています。
You'll see these show up in the upcoming concepts + architecture + tutorial pages as well. 
これらは、今後の概念 + アーキテクチャ + チュートリアルページにも表示されるでしょう。

## Next steps 次のステップ

- Read theConceptspage to understand the Feast data model.
- Feastデータモデルを理解するために、[Conceptsページ](https://docs.feast.dev/getting-started/quickstart#:~:text=Read%20the-,Concepts,-page%20to%20understand)を読んでください。
- Read theArchitecturepage.
- Architectureページを読んでください。
- Check out ourTutorialssection for more examples on how to use Feast.
- Feastの使用方法に関するさらなる例については、[Tutorials](https://docs.feast.dev/getting-started/quickstart#:~:text=Check%20out%20our-,Tutorials,-section%20for%20more)セクションをチェックしてください。
- Follow ourRunning Feast with Snowflake/GCP/AWSguide for a more in-depth tutorial on using Feast.
- Feastの使用に関するより詳細なチュートリアルについては、[Running Feast with Snowflake/GCP/AWSガイド](https://docs.feast.dev/how-to-guides/feast-snowflake-gcp-aws)に従ってください。

<!-- ここまで読んだ! -->
