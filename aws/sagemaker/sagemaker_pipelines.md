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
  - まずProcessingJobを定義するために、Processorオブジェクトを定義する。

## 学習のためのTraining stepを定義する

- Training stepを定義するには、`sagemaker.workflow.steps.TrainingStep`クラスを使う。
- 手順:
  - Jobを定義するためにEstimatorオブジェクトを定義する。
  - TrainingStepの引数としてestimator.fit()の出力を使用する。
    - **`sagemaker_session`引数にpipeline_sessionを渡す事で、`fit()`を呼び出してもTrainingJobは起動されない**。代わりに、pipelineの1つのstepとしてジョブを実行する為に必要な情報が返される。
    - fitメソッドの`inputs`引数として、前のProcessingStepの出力を渡すようにする。
      - **PipelineStepクラスの`properties`属性**は、describe callのレスポンスのオブジェクトモデル(=`DescribeHogehogeJob`APIのjsonレスポンス?)と合致する。
    - (たぶん、`fit()`や`run()`の返り値を渡さずにPipelineStepオブジェクトを定義する方法もあるっぽい...??引数を見た感じ)

## モデル評価の為のProcessing stepを定義する

- モデル評価stepでやりたいことは、例えば以下:
  - 1. モデルをloadする。
  - 2. テスト用データをreadする。
  - 3. モデルにテストデータを推論させる。
  - 4. モデルの性能を評価したレポートを作成する。
  - 5. 評価ディレクトリにレポートを保存する。
- 手順:

  - ProcessingJobで走らせる用の、モデル評価用のコードを実際に用意しておく(これはTrainingJobも同様)
  - **ScriptProcessorオブジェクト**を初期化して、ProcessingJobを定義する。
  - (前述のprocessing step, training stepと同様)`sagemaker_session`にPipelineSessionオブジェクトを渡しているので、`run()`を呼び出してもProcessingJobは起動されない。代わりに、pipelineの1つのstepとしてジョブを実行する為に必要な情報が返される。
  - 評価ジョブの入力として、前のTrainingStepの出力と、更に前のProcessingStepの出力を渡す。
    - PipelineStepクラスの`properties`属性を使って指定する。

- (メモ)ScriptProcessorとProcessorオブジェクトと何が違うんだ??
  - Processorクラスは、ProcessingJobを生成する為の**汎用的なAPI**。
  - ScriptProcessorクラスは、Processorクラスを継承しており、Pythonスクリプトを実行しやすいようにデザインされた**特化型API**。
    - (コードを渡してProcessingJobを実行するようなusecaseに特化したAPIって事っぽい?:thinking:)
    - (TrainingJobの場合は、各フレームワークの特化型APIが同様の役割を担ってるっぽい...!)

## モデルリソースを作成する為のCreateModel stepを定義する

## batch推論する為のTransform stepを定義する

## モデルパッケージを作る為のRegisterModel stepを定義する

## pipelineの処理を打ち切り、失敗を通知する為のfail stepを定義する

## モデル精度の評価結果に基づいて、条件付きで後続の処理を実行させる為のcondition stepを定義する

## pipelineパラメータ、各step、conditionを組み合わせて、Pipelineを定義する。

## (Optional) Pipeline定義を調査する。

# Pipelineのデプロイ方法 & マニュアルでの実行方法

## Pipelineのデプロイ方法

# Pipelineのスケジュール実行

- いくつか方法がありそう:
  - AWS EventBridgeを使用する方法。
    - EventBridgeのルールを使って、定期的にpipelineを実行する。
  - それ以外の方法(https://github.com/aws-samples/scheduling-sagemaker-processing-with-sagemaker-pipelines)

## refs:

- EventBridgeを使う方法: [パイプライン実行をスケジュールする](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/pipeline-eventbridge.html)
- それ以外の方法??[Scheduling a daily processing job with Amazon SageMaker Processing and Amazon SageMaker Pipelines](https://github.com/aws-samples/scheduling-sagemaker-processing-with-sagemaker-pipelines)

## 方法1: AWS EventBridgeを使用する方法

- Amazon EventBridgeとは?
  - 

## 方法2: それ以外の方法

- hoge


