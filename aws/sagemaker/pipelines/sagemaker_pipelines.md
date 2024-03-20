## 0.1. refs

- [Get started with SageMaker Pipelines](https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-pipelines/index.html)
- [Orchestrate Jobs to Train and Evaluate Models with Amazon SageMaker Pipelines](https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-pipelines/tabular/abalone_build_train_deploy/sagemaker-pipelines-preprocess-train-evaluate-batch-transform.html)
- [いつどこで課金が発生してる？Amazon SageMakerの動きと料金体系をセットで考える](https://dev.classmethod.jp/articles/sagemaker-pricing/)

# 1. AWS Sagemaker Pipelinesとは?

## 1.1. Sagemaker Pipelines って何?

- Sagemakerジョブをorchestrateし、再現可能なMLパイプラインを開発・運用するためのサービス。
- Sagemaker Pipelinesは、直接的には、JSON形式の**Sagemaker Pipeline DSL(Domain Specific Language, ドメイン固有言語)**で定義される。
  - このDSLでは、**パイプラインパラメータとSagemakerジョブのDAG(Directed acyclic graph, S有向非巡回グラフ)を定義**する。
  - Sagemaker Python SDK(Software Development Kit)を使えば、**慣れ親しんだPythonコードによって、Sagemaker Pipeline DSLの生成ができる**。
    - (ここはcdkみたいな感じか...!!:thinking:)
- Sagemaker Pipelinesの利用自体は無料。ProcessingJobなどでインスタンスを起動した際にその分の料金がかかる仕組みみたい。

## 1.2. Sagemaker Pipelines の機能:

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
  - 学習で得られたmodel artifactを使って、model resourceを作成するstep。(=batch推論や推論エンドポイントではmodel resourceを使うので...!)
- Transform job steps:
  - create model stepで作成したモデルリソースを使って、バッチ変換ジョブを実行するstep。
- Wait steps
- Fail steps:
  - pipelineの実行を停止し、実行失敗として通知するstep.
  - エラーメッセージとか指定できる。

(最後に、定義したpipeline(DAG)にはパラメータを渡す事ができるよ、という話)

- Parametrized Pipeline executions: 定義したpipeline(DAG)にはパラメータを定義する事ができるよ、実行時に渡されたパラメータの値によって実行内容を変化させられるよ、という話。

# 2. Pipelineの定義方法

Sagemaker Python SDKを使って定義する場合は、`sagemaker.workflow`パッケージ以下のクラスを使って定義するっぽい...!

## 2.1. pipeline実行をparametrizedする為に、パラメータを定義する

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

## 2.2. 特徴量生成のためのProcessing stepを定義する

- Processing stepを定義するには、`sagemaker.workflow.steps.ProcessingStep`クラスを使う。
- Processing stepを定義していく:
  - まずProcessingJobを定義するために、Processorオブジェクトを定義する。

## 2.3. 学習のためのTraining stepを定義する

- Training stepを定義するには、`sagemaker.workflow.steps.TrainingStep`クラスを使う。
- 手順:
  - Jobを定義するためにEstimatorオブジェクトを定義する。
  - TrainingStepの引数としてestimator.fit()の出力を使用する。
    - **`sagemaker_session`引数にpipeline_sessionを渡す事で、`fit()`を呼び出してもTrainingJobは起動されない**。代わりに、pipelineの1つのstepとしてジョブを実行する為に必要な情報が返される。
    - fitメソッドの`inputs`引数として、前のProcessingStepの出力を渡すようにする。
      - **PipelineStepクラスの`properties`属性**は、describe callのレスポンスのオブジェクトモデル(=`DescribeHogehogeJob`APIのjsonレスポンス?)と合致する。
    - (たぶん、`fit()`や`run()`の返り値を渡さずにPipelineStepオブジェクトを定義する方法もあるっぽい...??引数を見た感じ)

## 2.4. モデル評価の為のProcessing stepを定義する

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

## 2.5. model resourceを作成する為のCreateModel stepを定義する

- 学習したモデルを使ってbatch推論する為の準備として、モデルリソースを作成するstepを定義する。
- モデルリソースを作成するstepを定義するには、`sagemaker.workflow.model_step.ModelStep`クラスを使う。
  - CreateModel stepクラスを定義する際には`sagemaker.model.Model`オブジェクトの`create()`メソッドの返り値を`step_args`として渡す。
  - Modelオブジェクトを初期化する際は、training jobの出力である`S3ModelArtifacts`を指定する。(TrainingStepのproperties属性を使って指定する)

```python
from sagemaker.model import Model

model = Model(
    image_uri=image_uri,
    model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
    sagemaker_session=pipeline_session,
    role=role,
)

from sagemaker.inputs import CreateModelInput
from sagemaker.workflow.model_step import ModelStep

step_create_model = ModelStep(
    name="AbaloneCreateModel",
    step_args=model.create(instance_type="ml.m5.large", accelerator_type="ml.eia1.medium"),
)
```

## 2.6. batch推論する為のTransform stepを定義する

- バッチ推論を実行するstepを定義するには、`sagemaker.workflow.steps.TransformStep`クラスを使う。
- TransformStepクラスを定義する際には、`sagemaker.transformer.Transformer`オブジェクトを引数として渡す必要がある。
- Transformerオブジェクトを初期化する際は、create model stepのproperties属性を使って指定する。

```python
from sagemaker.transformer import Transformer


transformer = Transformer(
    model_name=step_create_model.properties.ModelName,
    instance_type="ml.m5.xlarge",
    instance_count=1,
    output_path=f"s3://{default_bucket}/AbaloneTransform",
)

from sagemaker.inputs import TransformInput
from sagemaker.workflow.steps import TransformStep


step_transform = TransformStep(
    name="AbaloneTransform", transformer=transformer, inputs=TransformInput(data=batch_data)
)
```

## 2.7. model packageを作る為のRegisterModel stepを定義する

- model package
  - 推論に必要な全ての要素をpackage化した、再利用可能なmodel artifactの抽象化された概念。
- model package groupとは?
  - model packageのコレクション。
  - model package groupは、特定のMLビジネス問題において一つ作成でき、新しいバージョンのmodel packageを追加できる。
  - ex.) MLビジネス問題に対して事前にModelpackageGroupを用意しておき、学習pipelineを実行させる度に、model packageのバージョンをグループに追加しておく。
- (たぶんmodel packageもmodel package groupも、モデルレジストリの概念っぽい??:thinking:)

- create model stepと同様に、registorModel stepも`sagemaker.workflow.model_step.ModelStep`クラスを使って定義する。
  - RegistorModel stepクラスを定義する際には、create model stepと同様の`sagemaker.model.Model`オブジェクトを用いて、`register()`メソッドの返り値を`step_args`として渡す。
  - `register()`メソッドの引数として、ModelMetricsオブジェクトを渡したりできる。
- hoge

## 2.8. pipelineの処理を打ち切り、失敗を通知する為のfail stepを定義する

- 実行失敗の原因を示す、カスタマイズされたエラーメッセージ付きのFailStepを定義する。

```python
from sagemaker.workflow.fail_step import FailStep
from sagemaker.workflow.functions import Join

step_fail = FailStep(
    name="AbaloneMSEFail",
    error_message=Join(on=" ", values=["Execution failed due to MSE >", mse_threshold]),
)
```

## 2.9. モデル精度の評価結果に基づいて、条件付きで後続の処理を実行させる為のcondition stepを定義する

- evaluation stepによって出力されたモデル精度が、指定されたしきい値を超えているかどうかを判定し、条件に応じて後続の処理を実行させる。
- condition stepを定義するには、`sagemaker.workflow.condition_step.ConditionStep`クラスを使う。
- 手順:
  - `ConditionLessThanOrEqualTo`オブジェクトを使って、hogehoge
  - `ConditionStep`クラスを初期化する。
    - `conditions`引数に`ConditionLessThanOrEqualTo`オブジェクトを渡す。
    - `if_steps`引数に、条件がTrueの場合に実行されるstepのlistを渡す。
    - `else_steps`引数に、条件がFalseの場合に実行されるstepのlistを渡す。

```python
from sagemaker.workflow.conditions import ConditionLessThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet


cond_lte = ConditionLessThanOrEqualTo(
    left=JsonGet(
        step_name=step_eval.name,
        property_file=evaluation_report,
        json_path="regression_metrics.mse.value",
    ),
    right=mse_threshold,
)

step_cond = ConditionStep(
    name="AbaloneMSECond",
    conditions=[cond_lte],
    if_steps=[step_register, step_create_model, step_transform],
    else_steps=[step_fail],
)
```

## 2.10. pipelineパラメータ、各step、conditionを組み合わせて、Pipelineを定義する。

- 定義した全てのPipelineStepを組み合わせて、Pipelineを定義する。
- Pipelineは`name`, `parameters`, `steps`を必要とする。
  - Pipeline名は`(account, region)`ペア内でユニークである必要がある。
- 考慮点:
  - Pipeline内のstep達で使用されるパラメータは、全て `parameters`引数で指定されなければならない。
  - Pipeline定義時に指定する`steps`引数は、**実行順にlistされている必要はない**。
    - `steps`引数に指定されたstep達は、DAG内で依存関係に基づいて自動的にソートされる。
    - (でも基本的には、実行順の方が可読性は高そう)
  - Pipeline step listとすべての条件ステップ if/else リスト全体において、`steps`は一意である必要がある。
    - つまり、同じstepを複数回指定する事はできないってこと?:thinking:
    - ex.) 内容が同じstepを、最初と最後に実行したい場合、それぞれ異なる名前のPipelineStepとして定義する必要があるってこと??:thinking:
    - ex.) condition step以降のif_stepsとelse_stepsに同じ名前のPipelineStepを指定する事はできないってこと??:thinking:

```python
from sagemaker.workflow.pipeline import Pipeline


pipeline_name = f"AbalonePipeline"
pipeline = Pipeline(
    name=pipeline_name,
    parameters=[
        processing_instance_countf,
        instance_type,
        model_approval_status,
        input_data,
        batch_data,
        mse_threshold,
    ],
    steps=[step_process, step_train, step_eval, step_cond],
)
```

## 2.11. (Optional) Pipeline定義を調査する。

- パイプライン定義のJSONを調べて、Pipelineが正しく定義され、parametersとstep propertiesが正しく解決されていることを確認することができる。

```python
import json


definition = json.loads(pipeline.definition())
definition
```

## ParallelStepっていう概念もあるらしい...!

- hogehoge

# 3. Pipelineのデプロイ方法 & マニュアルでの実行方法

## 3.1. Pipelineのデプロイ方法

- パイプライン定義をPipelineサービスに送信する。
  - Pipelineサービスは、渡されたroleを使用して、ステップで定義されたすべてのジョブを作成する。

```python
pipeline.upsert(role_arn=role)
```

- 全てデフォルトのparameterで、パイプラインを実行開始する。

```python
execution = pipeline.start()
```

- パラメータを指定して、パイプラインを実行開始する。

```python
execution = pipeline.start(
    parameters=dict(
        ModelApprovalStatus="Approved",
    )
)
```

## Pipeline操作

## 評価結果の確認

## Lineageの確認

# 4. Pipelineのスケジュール実行

- いくつか方法がありそう:
  - AWS EventBridgeを使用する方法。
    - EventBridgeのルールを使って、定期的にpipelineを実行する。
  - それ以外の方法(https://github.com/aws-samples/scheduling-sagemaker-processing-with-sagemaker-pipelines)

## 4.1. refs:

- EventBridgeを使う方法: [パイプライン実行をスケジュールする](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/pipeline-eventbridge.html)
- それ以外の方法??[Scheduling a daily processing job with Amazon SageMaker Processing and Amazon SageMaker Pipelines](https://github.com/aws-samples/scheduling-sagemaker-processing-with-sagemaker-pipelines)

## 4.2. 方法1: AWS EventBridgeを使用する方法

- Amazon EventBridgeはターゲットとして`StartPipelineExecution`アクションをサポートしている。
  - なので、**EventBridge ruleを作成すれば、event bus内の任意のイベントに基づいてpipeline実行を開始できる...!**
- pre-requirsites(事前準備):
  - EventBridgeが`Sagemaker::StartPipelineExecution`アクションの権限をassumeできるrole。
    - (たぶんEvantBridge自体がアクション権限を所持できればOK??:thinking:)
    - EventBridgeコンソールからEventBridge ruleを作成する場合は、自動で必要なアクション権限を持ったroleが紐づくみたい??
  - 指定したいsagemaker pipeline。
- EventBridge ruleの作成方法はいくつかある:
  - AWS Management ConsoleのEventBridgeコンソールを使う方法。
  - AWS CLIを使用する方法。

## 4.3. 方法2: それ以外の方法

> EventBridgeを使わずに、Sagemaker Pipelinesの特定のpipelineをトリガーする事は可能ですか?
> ChatGPT はい、EventBridgeを使わずにSageMaker Pipelinesの特定のパイプラインをトリガーすることは可能です。SageMaker Python SDKを使用して、スクリプトやアプリケーションから直接パイプラインの実行を開始することができます。この方法では、start_pipeline_executionメソッドを使用してパイプラインの実行をプログラム的にトリガーできます。また、AWS CLIを使用してコマンドラインからパイプラインを実行することも可能です。これにより、**EventBridgeを使用しない他のスケジューリングツールやトリガーメカニズムと組み合わせて、パイプラインの実行を自動化することができます**。

- 要は別のorchestratorやschedulerからSagemakerのAPIを叩くってことか...! :thinking:
