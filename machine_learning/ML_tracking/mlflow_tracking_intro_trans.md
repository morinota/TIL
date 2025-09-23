refs: https://www.mlflow.org/docs/latest/ml/tracking/

# MLflow Tracking

The MLflow Tracking is an API and UI for logging parameters, code versions, metrics, and output files 
MLflow Trackingは、機械学習コードを実行する際に、パラメータ、コードバージョン、メトリクス、出力ファイルをログに記録し、後で結果を視覚化するためのAPIおよびUIです。
when running your machine learning code and for later visualizing the results.
MLflow Tracking provides Python, REST, R, and Java APIs.
MLflow Trackingは、Python、REST、R、およびJavaのAPIを提供します。

![]()

A screenshot of the MLflow Tracking UI, showing a plot of validation loss metrics during model training.
モデル訓練中の検証損失メトリクスのプロットを示すMLflow Tracking UIのスクリーンショット。

## Quickstart クイックスタート

If you haven't used MLflow Tracking before, we strongly recommend going through the following quickstart tutorial.
MLflow Trackingを以前に使用したことがない場合は、以下のクイックスタートチュートリアルを通過することを強くお勧めします。

MLflow Tracking QuickstartA great place to start to learn the fundamentals of MLflow Tracking! Learn in 5 minutes how to log, register, and load a model for inference.
MLflow Tracking Quickstartは、MLflow Trackingの基本を学ぶための素晴らしい出発点です！ 5分でモデルをログ、登録、推論のためにロードする方法を学びましょう。

<!-- ここまで読んだ! -->

## Concepts 概念  
### Runs 実行

MLflow Tracking is organized around the concept of runs, which are executions of some piece of data science code, for example, a single python train.py execution.  
MLflow Trackingは、実行（runs）の概念に基づいて構成されており、これはデータサイエンスコードの一部の実行を指します。例えば、単一のpython train.pyの実行です。
Each run records metadata (various information about your run such as metrics, parameters, start and end times) and artifacts (output files from the run such as model weights, images, etc).  
**各実行は、メタデータ（メトリクス、パラメータ、開始および終了時刻など、実行に関するさまざまな情報）とアーティファクト（モデルの重み、画像など、実行からの出力ファイル）を記録**します。

<!-- ここまで読んだ! -->

### Models モデル

Models represent the trained machine learning artifacts that are produced during your runs. 
モデルは、実行中に生成される訓練済みの機械学習アーティファクトを表します。
Logged Models contain their own metadata and artifacts similar to runs. 
ログされたモデルは、実行と同様のメタデータとアーティファクトを含んでいます。

### Experiments 実験

An experiment groups together runs and models for a specific task. 
**実験は、特定のタスクのためにランとモデルをグループ化**します。
You can create an experiment using the CLI, API, or UI. 
CLI、API、またはUIを使用して実験を作成できます。
The MLflow API and UI also let you create and search for experiments. 
MLflowのAPIとUIを使用すると、実験を作成したり検索したりすることもできます。
See Organizing Runs into Experiments for more details on how to organize your runs into experiments. 
ランを実験に整理する方法の詳細については、「[Organizing Runs into Experiments](https://www.mlflow.org/docs/latest/ml/tracking/tracking-api/#experiment-organization)」を参照してください。

## Tracking Runs 実行の追跡

MLflow Tracking APIs provide a set of functions to track your runs. 
MLflow Tracking APIは、実行を追跡するための一連の関数を提供します。
For example, you can call mlflow.start_run() to start a new run, 
例えば、`mlflow.start_run()`を呼び出して新しい実行を開始できます。
then call Logging Functions such as mlflow.log_param() and mlflow.log_metric() to log parameters and metrics respectively. 
次に、`mlflow.log_param()`や`mlflow.log_metric()`などのロギング関数を呼び出して、それぞれパラメータとメトリクスを記録します。
Please visit the Tracking API documentation for more details about using these APIs. 
これらのAPIの使用に関する詳細は、Tracking APIのドキュメントをご覧ください。


```python
import mlflow
with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    # your ML code
    ...
    mlflow.log_metric("val_loss", val_loss)


```

Alternatively, `Auto-logging` offers an ultra-quick setup for starting MLflow tracking.
一方で、`Auto-logging`はMLflowトラッキングを開始するための超迅速なセットアップを提供します。
This powerful feature allows you to log metrics, parameters, and models without the need for explicit log statements -
この強力な機能により、明示的なログステートメントを必要とせずに、メトリクス、パラメータ、およびモデルをログに記録できます。
all you need to do is callmlflow.autolog()before your training code. 
必要なのは、トレーニングコードの前に`mlflow.autolog()`を呼び出すことだけです。
Auto-logging supports popular
libraries such asScikit-learn,XGBoost,PyTorch,Keras,Spark, and more. 
Auto-loggingは、Scikit-learn、XGBoost、PyTorch、Keras、Sparkなどの人気ライブラリをサポートしています。
SeeAutomatic Logging Documentationfor supported libraries and how to use auto-logging APIs with each of them.
サポートされているライブラリと、それぞれのライブラリでauto-logging APIを使用する方法については、Automatic Logging Documentationを参照してください。

  
```python
import mlflow
mlflow.autolog()  # Your training code...
```  

---
Note

By default, without any particular server/database configuration, MLflow Tracking logs data to the localmlrunsdirectory.
デフォルトでは、特別なサーバー/データベースの設定がない場合、MLflow Trackingはデータをlocalの `mlruns` ディレクトリにログします。
If you want to log your runs to a different location, such as a remote database and cloud storage, in order to share your results with your team, follow the instructions in theSet up MLflow Tracking Environmentsection.
**結果をチームと共有するために、リモートデータベースやクラウドストレージなど、別の場所に実行をログに記録したい場合は、「[Set up MLflow Tracking Environment](https://www.mlflow.org/docs/latest/ml/tracking/#tracking-setup)」セクションの指示に従ってください。**

---

<!-- ここまで読んだ! -->

### Searching Logged Models Programmatically プログラムによるログモデルの検索

MLflow 3 introduces powerful model search capabilities through mlflow.search_logged_models().
MLflow 3は、`mlflow.search_logged_models()`を通じて強力なモデル検索機能を導入します。
This API allows you to find specific models across your experiments based on performance metrics, parameters, and model attributes using SQL-like syntax. 
このAPIを使用すると、パフォーマンスメトリック、パラメータ、およびモデル属性に基づいて、実験全体から特定のモデルをSQLのような構文で見つけることができます。

```python
import mlflow

# Find high-performing models across experiments
top_models = mlflow.search_logged_models(
    experiment_ids=["1", "2"],
    filter_string="metrics.accuracy > 0.95 AND params.model_type = 'RandomForest'",
    order_by=[{"field_name": "metrics.f1_score", "ascending": False}],
    max_results=5,
)

# Get the best model for deployment
best_model = mlflow.search_logged_models(
    experiment_ids=["1"],
    filter_string="metrics.accuracy > 0.9",
    max_results=1,
    order_by=[{"field_name": "metrics.accuracy", "ascending": False}],
    output_format="list",
)[0]

# Load the best model directly
loaded_model = mlflow.pyfunc.load_model(f"models:/{best_model.model_id}")
```

Key Features: 主な機能:

- SQL-like filtering: Use metrics., params., and attribute prefixes to build complex queries
  - SQLライクなフィルタリング: metrics.、params.、および属性プレフィックスを使用して複雑なクエリを構築します。
- Dataset-aware search: Filter metrics based on specific datasets for fair model comparison
  - データセットを考慮した検索: 特定のデータセットに基づいてメトリクスをフィルタリングし、公平なモデル比較を行います。
- Flexible ordering: Sort by multiple criteria to find the best models
  - 柔軟な順序付け: 複数の基準でソートして最良のモデルを見つけます。
- Direct model loading: Use the new models:/<model_id> URI format for immediate model access
  - 直接モデル読み込み: 新しい models:/<model_id> URI形式を使用して、即座にモデルにアクセスします。

For comprehensive examples and advanced search patterns, see the Search Logged Models Guide.
包括的な例や高度な検索パターンについては、[Search Logged Models Guide](https://www.mlflow.org/docs/latest/ml/search/search-models/)を参照してください。

<!-- ここまで読んだ! -->

### Querying Runs Programmatically プログラムによるランのクエリ

You can also access all of the functions in the Tracking UI programmatically with MlflowClient.
Tracking UIのすべての機能にプログラム的にアクセスすることもできます。これは、`MlflowClient`を使用して行います。

For example, the following code snippet search for runs that has the best validation loss among all runs in the experiment.
例えば、以下のコードスニペットは、実験内のすべてのランの中で最も良い検証損失を持つランを検索します。

```python
client = mlflow.tracking.MlflowClient()
experiment_id = "0"
best_run = client.search_runs(
    experiment_id, order_by=["metrics.val_loss ASC"], max_results=1
)[0]
print(best_run.info)
# {'run_id': '...', 'metrics': {'val_loss': 0.123}, ...}
```

<!-- ここまで読んだ! -->

## Tracking Models モデルの追跡

MLflow 3 introduces enhanced model tracking capabilities that allow you to log multiple model checkpoints within a single run and track their performance against different datasets. 
MLflow 3は、単一の実行内で複数のモデルチェックポイントをログに記録し、異なるデータセットに対するパフォーマンスを追跡するための強化されたモデル追跡機能を導入します。 
This is particularly useful for deep learning workflows where you want to save and compare model checkpoints at different training stages.
これは、異なるトレーニング段階でモデルチェックポイントを保存し、比較したい深層学習ワークフローに特に便利です。

### Logging Model Checkpoints モデルチェックポイントのログ記録

You can log model checkpoints at different steps during training using the step parameter in model logging functions. 
トレーニング中の異なるステップでモデルチェックポイントをログ記録するには、モデルログ記録関数のstepパラメータを使用できます。
Each logged model gets a unique model ID that you can use to reference it later. 
ログ記録された各モデルには、後で参照するために使用できる一意のモデルIDが付与されます。

<!-- ここまで読んだ! -->

```
import mlflow
import mlflow.pytorch
with mlflow.start_run() as run:
    for epoch in range(100):
        # Train your model
        train_model(model, epoch)
        # Log model checkpoint every 10 epochs
        if epoch % 10 == 0:
            model_info = mlflow.pytorch.log_model(
                pytorch_model=model,
                name=f"checkpoint-epoch-{epoch}",
                step=epoch,
                input_example=sample_input,
            )
            # Log metrics linked to this specific model checkpoint
            accuracy = evaluate_model(model, validation_data)
            mlflow.log_metric(
                key="accuracy",
                value=accuracy,
                step=epoch,
                model_id=model_info.model_id,  # Link metric to specific model
                dataset=validation_dataset,
            )
```
``` 



# Train your model モデルの訓練

train_model(model,epoch)  
train_model  
(  
model  
,  
epoch  
)  



# Log model checkpoint every 10 epochs モデルのチェックポイントを10エポックごとに記録する

if epoch % 10 == 0:  
if  
epoch  
%  
10  
==  
0:  
model_info = mlflow.pytorch.log_model(  
model_info  
=  
mlflow  
.  
pytorch  
.  
log_model  
(  
pytorch_model = model,  
pytorch_model  
=  
model  
,  
name = f"checkpoint-epoch-{epoch}",  
name  
=  
f"checkpoint-epoch-  
{  
epoch  
}  
"  
,  
step = epoch,  
step  
=  
epoch  
,  
input_example = sample_input,  
input_example  
=  
sample_input  
,  
)  
)  



# Log metrics linked to this specific model checkpoint この特定のモデルチェックポイントに関連するログメトリック

accuracy=evaluate_model(model,validation_data) 
accuracy = evaluate_model(model, validation_data) 
mlflow.log_metric( 
mlflow.log_metric( 
key="accuracy", 
key = "accuracy", 
value=accuracy, 
value = accuracy, 
step=epoch, 
step = epoch, 
model_id=model_info.model_id, # Link metric to specific model 
model_id = model_info.model_id, 



# Link metric to specific model 特定のモデルへのリンクメトリック

dataset=validation_dataset,
dataset
=
validation_dataset
,
)
)



### Linking Metrics to Models and Datasets モデルとデータセットへのメトリクスのリンク

MLflow 3 allows you to link metrics to specific model checkpoints and datasets, providing better traceability of model performance:
MLflow 3は、メトリクスを特定のモデルチェックポイントおよびデータセットにリンクすることを可能にし、モデルのパフォーマンスのトレーサビリティを向上させます。

```
# Create a dataset referencetrain_dataset=mlflow.data.from_pandas(train_df,name="training_data")# Log metric with model and dataset linksmlflow.log_metric(key="f1_score",value=0.95,step=epoch,model_id=model_info.model_id,# Links to specific model checkpointdataset=train_dataset,# Links to specific dataset)
```



# Create a dataset reference データセット参照の作成

train_dataset=mlflow.data.from_pandas(train_df,name="training_data")  
train_dataset=mlflow.data.from_pandas(train_df,name="training_data")  



# Log metric with model and dataset links モデルとデータセットのリンクを持つログメトリック

mlflow.log_metric(
mlflow
.
log_metric
(
key="f1_score",
key
=
"f1_score"
,
value=0.95,
value
=
0.95
,
step=epoch,
step
=
epoch
,
model_id=model_info.model_id,# Links to specific model checkpoint
model_id
=
model_info
.
model_id
,



# Links to specific model checkpoint 特定のモデルチェックポイントへのリンク

dataset=train_dataset,# Links to specific dataset
dataset
=
train_dataset
,



# Links to specific dataset 特定のデータセットへのリンク
)
)



### Searching and Ranking Model Checkpoints モデルチェックポイントの検索とランキング

Usemlflow.search_logged_models()to search and rank model checkpoints based on their performance metrics:
`mlflow.search_logged_models()`を使用して、パフォーマンスメトリクスに基づいてモデルチェックポイントを検索およびランキングします。

```
# Search for all models in a run, ordered by accuracy
# 精度で順序付けられたラン内のすべてのモデルを検索
ranked_models=mlflow.search_logged_models(filter_string=f"source_run_id='{run.info.run_id}'",order_by=[{"field_name":"metrics.accuracy","ascending":False}],output_format="list",)

# Get the best performing model
# 最もパフォーマンスの良いモデルを取得
best_model=ranked_models[0]
print(f"Best model:{best_model.name}")
print(f"Accuracy:{best_model.metrics[0].value}")

# Load the best model for inference
# 推論のために最良のモデルをロード
loaded_model=mlflow.pyfunc.load_model(f"models:/{best_model.model_id}")
```



# Search for all models in a run, ordered by accuracy  
# 精度で並べられた実行内のすべてのモデルを検索

ranked_models=mlflow.search_logged_models(  
ranked_models=mlflow.search_logged_models(  
filter_string=f"source_run_id='{run.info.run_id}'",  
filter_string=f"source_run_id='{run.info.run_id}'",  
order_by=[{"field_name":"metrics.accuracy","ascending":False}],  
order_by=[{"field_name":"metrics.accuracy","ascending":False}],  
output_format="list",  
output_format="list",  
)  
)  



# Get the best performing model 最良のモデルを取得する

best_model=ranked_models[0]  
best_model=ranked_models[0]  
print(f"Best model:{best_model.name}")  
print(f"最良のモデル: {best_model.name}")  
print(f"Accuracy:{best_model.metrics[0].value}")  
print(f"精度: {best_model.metrics[0].value}")  



# Load the best model for inference 最良モデルの読み込み

loaded_model=mlflow.pyfunc.load_model(f"models:/{best_model.model_id}")
loaded_model
=
mlflow
.
pyfunc
.
load_model
(
f"models:/
{
best_model
.
model_id
}
"
)



### Model URIs in MLflow 3 MLflow 3におけるモデルURI

MLflow 3 introduces a new model URI format that uses model IDs instead of run IDs, providing more direct model referencing:
MLflow 3は、モデルIDを使用する新しいモデルURIフォーマットを導入し、ランIDの代わりにより直接的なモデル参照を提供します。

```
# New MLflow 3 model URI formatmodel_uri=f"models:/{model_info.model_id}"loaded_model=mlflow.pyfunc.load_model(model_uri)# This replaces the older run-based URI format:# model_uri = f"runs:/{run_id}/model_path"
```
```
# 新しいMLflow 3モデルURIフォーマット
model_uri=f"models:/{model_info.model_id}"
loaded_model=mlflow.pyfunc.load_model(model_uri)
# これは古いランベースのURIフォーマットに置き換わります：
# model_uri = f"runs:/{run_id}/model_path"
```  



# New MLflow 3 model URI format 新しいMLflow 3モデルURIフォーマット

model_uri=f"models:/{model_info.model_id}"  
model_uri=f"models:/{model_info.model_id}"  

loaded_model=mlflow.pyfunc.load_model(model_uri)  
loaded_model=mlflow.pyfunc.load_model(model_uri)  



# This replaces the older run-based URI format:  
# これは古いランベースのURIフォーマットを置き換えます：



# model_uri = f"runs:/{run_id}/model_path"  
# model_uri = f"runs:/{run_id}/model_path"
This new approach provides several advantages:
この新しいアプローチは、いくつかの利点を提供します：
- Direct model reference: No need to know the run ID and artifact path
- 直接モデル参照：ランIDやアーティファクトパスを知る必要がありません
- Better model lifecycle management: Each model checkpoint has its own unique identifier
- より良いモデルライフサイクル管理：各モデルチェックポイントには独自の識別子があります
- Improved model comparison: Easily compare different checkpoints within the same run
- モデル比較の改善：同じラン内の異なるチェックポイントを簡単に比較できます
- Enhanced traceability: Clear links between models, metrics, and datasets
- トレーサビリティの向上：モデル、メトリクス、データセット間の明確なリンク



## Tracking Datasets トラッキングデータセット

MLflow offers the ability to track datasets that are associated with model training events. 
MLflowは、モデルトレーニングイベントに関連するデータセットをトラッキングする機能を提供します。
These metadata associated with the Dataset can be stored through the use of themlflow.log_input()API.
データセットに関連するこれらのメタデータは、`mlflow.log_input()` APIを使用して保存できます。
To learn more, please visit theMLflow data documentationto see the features available in this API.
詳細については、MLflowのデータドキュメントを訪れて、このAPIで利用可能な機能を確認してください。



## Explore Runs, Models, and Results 探索実行、モデル、および結果  
### Tracking UI トラッキングUI
The Tracking UI lets you visually explore your experiments, runs, and models, as shown on top of this page.  
トラッキングUIは、実験、実行、およびモデルを視覚的に探索できるようにします。このページの上部に示されています。

- Experiment-based run listing and comparison (including run comparison across multiple experiments)  
- 実験ベースの実行リストと比較（複数の実験間での実行比較を含む）

- Searching for runs by parameter or metric value  
- パラメータまたはメトリック値による実行の検索

- Visualizing run metrics  
- 実行メトリックの視覚化

- Downloading run results (artifacts and metadata)  
- 実行結果（アーティファクトとメタデータ）のダウンロード

These features are available for models as well, as shown below.  
これらの機能は、以下に示すようにモデルにも利用可能です。

A screenshot of the MLflow Tracking UI on the models tab, showing a list of models under the experiment.  
実験の下にあるモデルのリストを示すモデルタブのMLflowトラッキングUIのスクリーンショット。

If you log runs to a local mlruns directory, run the following command in the directory above it,  
ローカルのmlrunsディレクトリに実行を記録する場合は、その上のディレクトリで次のコマンドを実行します。

then access http://127.0.0.1:5000 in your browser.  
その後、ブラウザで http://127.0.0.1:5000 にアクセスします。

```
mlflow ui --port 5000
```
```
mlflow ui --port 5000
```
mlflow ui  
--port  
5000  

Alternatively, the MLflow Tracking Server serves the same UI and enables remote storage of run artifacts.  
また、MLflowトラッキングサーバーは同じUIを提供し、実行アーティファクトのリモートストレージを可能にします。

In that case, you can view the UI at http://<IP address of your MLflow tracking server>:5000 from any machine that can connect to your tracking server.  
その場合、トラッキングサーバーに接続できる任意のマシンから http://<MLflowトラッキングサーバーのIPアドレス>:5000 でUIを表示できます。



## Set up the MLflow Tracking Environment MLflowトラッキング環境の設定

If you just want to log your experiment data and models to local files, you can skip this section.
もし単に実験データやモデルをローカルファイルに記録したいだけであれば、このセクションはスキップしても構いません。

MLflow Tracking supports many different scenarios for your development workflow. 
MLflow Trackingは、開発ワークフローのさまざまなシナリオをサポートしています。

This section will guide you through how to set up the MLflow Tracking environment for your particular use case.
このセクションでは、特定のユースケースに対してMLflowトラッキング環境を設定する方法を案内します。

From a bird's-eye view, the MLflow Tracking environment consists of the following components.
俯瞰的に見ると、MLflowトラッキング環境は以下のコンポーネントで構成されています。



### Components コンポーネント  
#### MLflow Tracking APIs  
You can call MLflow Tracking APIs in your ML code to log runs and communicate with the MLflow Tracking Server if necessary.  
MLflow Tracking APIをMLコード内で呼び出して、実行をログに記録し、必要に応じてMLflow Tracking Serverと通信することができます。  



#### Backend Store バックエンドストア

The backend store persists various metadata for eachRun, such as run ID, start and end times, parameters, metrics, etc.
バックエンドストアは、各実行（eachRun）のためのさまざまなメタデータを永続化します。これには、実行ID、開始および終了時刻、パラメータ、メトリクスなどが含まれます。

MLflow supports two types of storage for the backend:file-system-basedlike local files anddatabase-basedlike PostgreSQL.
MLflowは、バックエンドのために2種類のストレージをサポートしています：ファイルシステムベース（ローカルファイルのような）とデータベースベース（PostgreSQLのような）です。

Additionally, if you are interfacing with a managed service (such as Databricks or Azure Machine Learning), you will be interfacing with a
REST-based backend store that is externally managed and not directly accessible.
さらに、管理されたサービス（DatabricksやAzure Machine Learningなど）とインターフェースしている場合、外部で管理されており直接アクセスできないRESTベースのバックエンドストアとインターフェースすることになります。



#### Artifact Store アーティファクトストア

Artifact store persists (typically large) artifacts for each run, such as model weights (e.g. a pickled scikit-learn model), images (e.g. PNGs), model and data files (e.g. Parquet file). 
アーティファクトストアは、各実行のために（通常は大きな）アーティファクトを永続化します。これには、モデルの重み（例：ピクル化されたscikit-learnモデル）、画像（例：PNG）、モデルおよびデータファイル（例：Parquetファイル）が含まれます。

MLflow stores artifacts in a local file (mlruns) by default, but also supports different storage options such as Amazon S3 and Azure Blob Storage. 
MLflowは、デフォルトでローカルファイル（mlruns）にアーティファクトを保存しますが、Amazon S3やAzure Blob Storageなどの異なるストレージオプションもサポートしています。

For models which are logged as MLflow artifacts, you can refer the model through a model URI of format: models:/<model_id>, where 'model_id' is the unique identifier assigned to the logged model. 
MLflowアーティファクトとしてログされたモデルについては、モデルURIの形式models:/<model_id>を通じてモデルを参照できます。ここで'model_id'は、ログされたモデルに割り当てられた一意の識別子です。

This replaces the older runs:/<run_id>/<artifact_path> format and provides more direct model referencing. 
これは、古い形式runs:/<run_id>/<artifact_path>を置き換え、より直接的なモデル参照を提供します。

If the model is registered in the MLflow Model Registry, you can also refer the model through a model URI of format: models:/<model-name>/<model-version>, see MLflow Model Registry for details. 
モデルがMLflowモデルレジストリに登録されている場合、モデルURIの形式models:/<model-name>/<model-version>を通じてモデルを参照することもできます。詳細についてはMLflowモデルレジストリを参照してください。



#### MLflow Tracking Server(Optional) MLflow Tracking Server（オプション）

MLflow Tracking Server is a stand-alone HTTP server that provides REST APIs for accessing backend and/or artifact store. 
MLflow Tracking Serverは、バックエンドおよび/またはアーティファクトストアにアクセスするためのREST APIを提供するスタンドアロンのHTTPサーバーです。

Tracking server also offers flexibility to configure what data to server, govern access control, versioning, and etc. 
トラッキングサーバーは、どのデータをサーバーに提供するかを設定し、アクセス制御、バージョン管理などを管理する柔軟性も提供します。

Read MLflow Tracking Server documentation for more details. 
詳細については、MLflow Tracking Serverのドキュメントを参照してください。



### Common Setups 一般的なセットアップ

By configuring these components properly, you can create an MLflow Tracking environment suitable for your team's development workflow.  
これらのコンポーネントを適切に構成することで、チームの開発ワークフローに適したMLflow Tracking環境を作成できます。

The following diagram and table show a few common setups for the MLflow Tracking environment.  
以下の図と表は、MLflow Tracking環境のいくつかの一般的なセットアップを示しています。



## Other Configuration with MLflow Tracking Server その他の設定とMLflowトラッキングサーバー

MLflow Tracking Server provides customizability for other special use cases. 
MLflowトラッキングサーバーは、他の特別なユースケースに対してカスタマイズ性を提供します。
Please follow Remote Experiment Tracking with MLflow Tracking Server for learning the basic setup and continue to the following materials for advanced configurations to meet your needs.
基本的なセットアップを学ぶために「Remote Experiment Tracking with MLflow Tracking Server」を参照し、ニーズに応じた高度な設定のために以下の資料を続けてください。

- Local Tracking Server
- ローカルトラッキングサーバー
- Artifacts-only Mode
- アーティファクト専用モード
- Direct Access to Artifacts
- アーティファクトへの直接アクセス



#### Using MLflow Tracking Server Locally MLflow Tracking Serverをローカルで使用する

You can of course run MLflow Tracking Server locally. 
もちろん、MLflow Tracking Serverをローカルで実行することができます。

While this doesn't provide much additional benefit over directly using the local files or database, 
これは、ローカルファイルやデータベースを直接使用することに比べて、あまり追加の利点を提供しませんが、

might useful for testing your team development workflow locally or running your machine learning code on a container environment. 
チームの開発ワークフローをローカルでテストしたり、コンテナ環境で機械学習コードを実行するのに役立つかもしれません。



#### Running MLflow Tracking Server in Artifacts-only Mode MLflow Tracking Serverのアーティファクト専用モードでの実行

MLflow Tracking Server has an--artifacts-onlyoption which allows the server to handle (proxy) exclusively artifacts, without permitting the processing of metadata. 
MLflow Tracking Serverには、--artifacts-onlyオプションがあり、サーバーがメタデータの処理を許可せずに、アーティファクトのみを専用に処理（プロキシ）できるようにします。 
This is particularly useful when you are in a large organization or are training extremely large models. 
これは特に、大規模な組織にいる場合や、非常に大きなモデルをトレーニングしている場合に便利です。 
In these scenarios, you might have high artifact transfer volumes and can benefit from splitting out the traffic for serving artifacts to not impact tracking functionality. 
これらのシナリオでは、高いアーティファクト転送量が発生する可能性があり、アーティファクトを提供するためのトラフィックを分割することで、トラッキング機能に影響を与えないようにすることができます。 
Please read Optionally using a Tracking Server instance exclusively for artifact handling for more details on how to use this mode. 
このモードの使用方法の詳細については、「アーティファクト処理専用のTracking Serverインスタンスのオプション使用」をお読みください。



#### Disable Artifact Proxying to Allow Direct Access to Artifacts アーティファクトプロキシを無効にしてアーティファクトへの直接アクセスを許可する

MLflow Tracking Server, by default, serves both artifacts and only metadata. 
MLflow Tracking Serverは、デフォルトでアーティファクトとメタデータの両方を提供します。しかし、いくつかのケースでは、プロキシのオーバーヘッドを避けつつメタデータトラッキングの機能を保持するために、リモートアーティファクトストレージへの直接アクセスを許可したい場合があります。 
This can be done by disabling artifact proxying by starting server with --no-serve-artifacts option. 
これは、`--no-serve-artifacts`オプションを使用してサーバーを起動することでアーティファクトプロキシを無効にすることによって実現できます。 
Refer to Use Tracking Server without Proxying Artifacts Access for how to set this up. 
この設定方法については、「Use Tracking Server without Proxying Artifacts Access」を参照してください。



## FAQ よくある質問  
### Can I launch multiple runs in parallel?  
Yes, MLflow supports launching multiple runs in parallel e.g. multi processing / threading.  
はい、MLflowは複数の実行を並行して開始することをサポートしています。例えば、マルチプロセッシングやスレッディングです。  
SeeLaunching Multiple Runs in One Programfor more details.  
詳細については、「One Programでの複数の実行の開始」を参照してください。  



### How can I organize many MLflow Runs neatly? 多くのMLflowランを整然と整理するにはどうすればよいですか？

MLflow provides a few ways to organize your runs:  
MLflowは、ランを整理するためのいくつかの方法を提供します：

- Organize runs into experiments- Experiments are logical containers for your runs.  
- ランを実験に整理する - 実験は、あなたのランの論理的なコンテナです。 

You can create an experiment using the CLI, API, or UI.  
CLI、API、またはUIを使用して実験を作成できます。

- Create child runs- You can create child runs under a single parent run to group them together.  
- 子ランを作成する - 単一の親ランの下に子ランを作成して、それらをグループ化できます。

For example, you can create a child run for each fold in a cross-validation experiment.  
例えば、クロスバリデーション実験の各フォールドに対して子ランを作成できます。

- Add tags to runs- You can associate arbitrary tags with each run, which allows you to filter and search runs based on tags.  
- ランにタグを追加する - 各ランに任意のタグを関連付けることができ、タグに基づいてランをフィルタリングおよび検索できます。



### Can I directly access remote storage without running the Tracking Server? リモートストレージにTracking Serverを実行せずに直接アクセスできますか？

Yes, while it is best practice to have the MLflow Tracking Server as a proxy for artifacts access for team development workflows, you may not need that if you are using it for personal projects or testing. 
はい、チーム開発ワークフローのためにアーティファクトアクセスのプロキシとしてMLflow Tracking Serverを持つことが最良の方法ですが、個人プロジェクトやテストに使用する場合はそれが必要ないかもしれません。

You can achieve this by following the workaround below: 
以下の回避策に従うことでこれを実現できます：

1. Set up artifacts configuration such as credentials and endpoints, just like you would for the MLflow Tracking Server. 
1. MLflow Tracking Serverと同様に、資格情報やエンドポイントなどのアーティファクト設定を行います。

See configure artifact storage for more details. 
詳細については、アーティファクトストレージの設定を参照してください。

2. Create an experiment with an explicit artifact location, 
2. 明示的なアーティファクトの場所を指定して実験を作成します。

```
experiment_name="your_experiment_name"
mlflow.create_experiment(experiment_name, artifact_location="s3://your-bucket")
mlflow.set_experiment(experiment_name)
```
```
experiment_name="your_experiment_name"
mlflow.create_experiment(experiment_name, artifact_location="s3://your-bucket")
mlflow.set_experiment(experiment_name)
```

Your runs under this experiment will log artifacts to the remote storage directly. 
この実験の下でのあなたの実行は、アーティファクトをリモートストレージに直接ログします。



#### How to integrate MLflow Tracking with Model Registry? MLflow TrackingとModel Registryを統合する方法

To use the Model Registry functionality with MLflow tracking, you must use database backed store such as PostgresQL and log a model using the log_model methods of the corresponding model flavors. 
MLflowトラッキングでModel Registry機能を使用するには、PostgresQLなどのデータベースバックストアを使用し、対応するモデルフレーバーのlog_modelメソッドを使用してモデルをログに記録する必要があります。

Once a model has been logged, you can add, modify, update, or delete the model in the Model Registry through the UI or the API. 
モデルがログに記録されると、UIまたはAPIを通じてModel Registry内のモデルを追加、変更、更新、または削除できます。

See Backend Stores and Common Setups for how to configure backend store properly for your workflow. 
バックエンドストアと一般的なセットアップを参照して、ワークフローに適したバックエンドストアの設定方法を確認してください。



#### How to include additional description texts about the run? 
#### 実行に関する追加の説明テキストを含める方法は？

A system tag mlflow.note.content can be used to add descriptive note about this run. 
システムタグ `mlflow.note.content` を使用して、この実行に関する説明的なノートを追加できます。

While the other system tags are set automatically, this tag is not set by default and users can override it to include additional information about the run. 
他のシステムタグは自動的に設定されますが、このタグはデフォルトでは設定されておらず、ユーザーはそれを上書きして実行に関する追加情報を含めることができます。

The content will be displayed on the run's page under the Notes section. 
その内容は、実行のページのノートセクションに表示されます。

- Quickstart
- クイックスタート
- Concepts Runs Models Experiments
- 概念 実行 モデル 実験
- Runs
- 実行
- Models
- モデル
- Experiments
- 実験
- Tracking Runs Searching Logged Models Programmatically Querying Runs Programmatically
- 実行の追跡 ログされたモデルのプログラムによる検索 プログラムによる実行のクエリ
- Searching Logged Models Programmatically
- ログされたモデルのプログラムによる検索
- Querying Runs Programmatically
- プログラムによる実行のクエリ
- Tracking Models Logging Model Checkpoints Linking Metrics to Models and Datasets Searching and Ranking Model Checkpoints Model URIs in MLflow 3
- モデルの追跡 モデルチェックポイントのログ メトリクスをモデルとデータセットにリンクする モデルチェックポイントの検索とランキング MLflow 3のモデルURI
- Logging Model Checkpoints
- モデルチェックポイントのログ
- Linking Metrics to Models and Datasets
- メトリクスをモデルとデータセットにリンクする
- Searching and Ranking Model Checkpoints
- モデルチェックポイントの検索とランキング
- Model URIs in MLflow 3
- MLflow 3のモデルURI
- Tracking Datasets
- データセットの追跡
- Explore Runs, Models, and Results Tracking UI
- 実行、モデル、結果の探索 追跡UI
- Tracking UI
- 追跡UI
- Set up the MLflow Tracking Environment Components Common Setups
- MLflow追跡環境の設定 コンポーネント 一般的なセットアップ
- Components
- コンポーネント
- Common Setups
- 一般的なセットアップ
- Other Configuration with MLflow Tracking Server
- MLflowトラッキングサーバーによるその他の設定
- FAQ Can I launch multiple runs in parallel? How can I organize many MLflow Runs neatly? Can I directly access remote storage without running the Tracking Server?
- FAQ 複数の実行を並行して開始できますか？ 多くのMLflow実行をきれいに整理するにはどうすればよいですか？ トラッキングサーバーを実行せずにリモートストレージに直接アクセスできますか？
- Can I launch multiple runs in parallel?
- 複数の実行を並行して開始できますか？
- How can I organize many MLflow Runs neatly?
- 多くのMLflow実行をきれいに整理するにはどうすればよいですか？
- Can I directly access remote storage without running the Tracking Server?
- トラッキングサーバーを実行せずにリモートストレージに直接アクセスできますか？
- Runs
- 実行
- Models
- モデル
- Experiments
- 実験
- Searching Logged Models Programmatically
- ログされたモデルのプログラムによる検索
- Querying Runs Programmatically
- プログラムによる実行のクエリ
- Logging Model Checkpoints
- モデルチェックポイントのログ
- Linking Metrics to Models and Datasets
- メトリクスをモデルとデータセットにリンクする
- Searching and Ranking Model Checkpoints
- モデルチェックポイントの検索とランキング
- Model URIs in MLflow 3
- MLflow 3のモデルURI
- Tracking UI
- 追跡UI
- Components
- コンポーネント
- Common Setups
- 一般的なセットアップ
- Can I launch multiple runs in parallel?
- 複数の実行を並行して開始できますか？
- How can I organize many MLflow Runs neatly?
- 多くのMLflow実行をきれいに整理するにはどうすればよいですか？
- Can I directly access remote storage without running the Tracking Server?
- トラッキングサーバーを実行せずにリモートストレージに直接アクセスできますか？
