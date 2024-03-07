## refs

- [Get started with SageMaker Pipelines](https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-pipelines/index.html)
- [Orchestrate Jobs to Train and Evaluate Models with Amazon SageMaker Pipelines](https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-pipelines/tabular/abalone_build_train_deploy/sagemaker-pipelines-preprocess-train-evaluate-batch-transform.html)
- [いつどこで課金が発生してる？Amazon SageMakerの動きと料金体系をセットで考える](https://dev.classmethod.jp/articles/sagemaker-pricing/)

# AWS Sagemaker Pipelinesとは?

## Sagemaker Pipelines って何?

- Sagemakerジョブをorchestrateし、再現可能なMLパイプラインを開発・運用するためのサービス。
- Sagemaker Pipelinesは、直接的には、JSON形式の**Sagemaker Pipeline DSL(Domain Specific Language, ドメイン固有言語)**で定義される。
  - このDSLでは、**パイプラインパラメータとSagemakerジョブのDAG(Directed acyclic graph, S有向非巡回グラフ)を定義**する。
  - Sagemaker Python SDK(Software Development Kit)を使えば、**慣れ親しんだPythonコードによって、Sagemaker Pipeline DSLの生成ができる**。
    - (ここはcdkみたいな感じか...!!:thinking:)

## Sagemaker Pipelines の機能:

サポートする活動は以下:

- Pipelines:
  - Sagemakerのジョブとリソース作成をorchestrateする為の**DAG(steps & conditions)**を定義する。

(たぶん以下は、DAG内でこういうstepを定義できますよ、って話:thinking:)

- Processing job steps
- Training job steps
- Conditional execution step:
  - pipeline内の分岐の条件付き実行のstep。
  - 例えば、前のstepのoutput内容に基づいて、あるstepを実行するか別のstepを実行するかを制御するような使い方ができる。
- Registering model steps:
  - 学習で得られたmodel artifactを使って、モデルパッケージを作りレジストリに登録するstep。
- Create model steps:
  - 学習で得られたmodel artifactを使って、モデルリソースを作成するstep。
- Transform job steps:
  - create model stepで作成したモデルリソースを使って、バッチ変換ジョブを実行するstep。
- Wait steps
- Fail steps:
  - pipelineの実行を停止し、実行失敗として通知するstep.
  - エラーメッセージとか指定できる。

(最後に、定義したpipeline(DAG)にはパラメータを渡す事ができるよ、という話)

- Parametrized Pipeline executions: 定義したpipeline(DAG)にはパラメータを定義する事ができるよ、実行時に渡されたパラメータの値によって実行内容を変化させられるよ、という話。

# Pipelineの定義方法

Sagemaker Python SDKを使って定義する場合は、`sagemaker.workflow`パッケージ以下のクラスを使って定義するっぽい...!

## pipeline実行をparametrizedする為に、パラメータを定義する

- parameterを定義すると、pipeline定義を変更する事なく、pipelineの実行をカスタムしたりスケジュールの設定ができたりする。
- パラメータの定義には、`sagemaker.workflow.parameters`モジュールを使う。
- サポートしてるパラメータのタイプは以下:
  - `ParameterString`: 文字列型のパラメータ。
  - `ParameterInteger`: 整数型のパラメータ。
  - `ParameterFloat`: 浮動小数点型のパラメータ。
  - 各パラメータにはデフォルト値を設定できる。
    - デフォルト値のデータ型は、パラメータのデータ型と一致している必要あり!
- 定義するパラメータ例:
  - `processing_instance_count`: Processing jobのインスタンス数。
  - `instance_type`: `ml.*`で始まるtraining jobやprocessing jobのインスタンスタイプ。
  - `model_approval_status`: 学習済みモデルに登録する承認ステータス。(CI/CDで使う?)(たぶんモデルレジストリを使った事あったら自明な概念なのかも??)
  - `input_data`: 学習データのS3URI。
  - `batch_data`: バッチデータのS3URI。(バッチ推論用)
  - `mse_threshold`: モデル精度を検証するためのMSEの閾値。

実装例は以下:

```python
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
    ParameterFloat,
)

processing_instance_count = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
instance_type = ParameterString(name="TrainingInstanceType", default_value="ml.m5.xlarge")
model_approval_status = ParameterString(
    name="ModelApprovalStatus", default_value="PendingManualApproval"
)
input_data = ParameterString(
    name="InputData",
    default_value=input_data_uri,
)
batch_data = ParameterString(
    name="BatchData",
    default_value=batch_data_uri,
)
mse_threshold = ParameterFloat(name="MseThreshold", default_value=6.0)
```

![]()
(これでpipelineを表すDAGの図の一番左側を定義できた!)

## 特徴量生成のためのProcessing stepを定義する

- Processing stepを定義するには、`sagemaker.workflow.steps.ProcessingStep`クラスを使う。
- Processing stepを定義していく:
  - まずPr
