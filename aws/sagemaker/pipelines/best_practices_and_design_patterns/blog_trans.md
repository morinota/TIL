## 0.1. refs: refs

- <https://aws.amazon.com/jp/blogs/machine-learning/best-practices-and-design-patterns-for-building-machine-learning-workflows-with-amazon-sagemaker-pipelines/> <https://aws.amazon.com/jp/blogs/machine-learning/best-practices-and-design-patterns-for-building-machine-learning-workflows-with-amazon-sagemaker-pipelines/>

# 1. Best practices and design patterns for building machine learning workflows with Amazon SageMaker Pipelines Amazon SageMaker Pipelinesで機械学習ワークフローを構築するためのベストプラクティスとデザインパターン

Amazon SageMaker Pipelines is a fully managed AWS service for building and orchestrating machine learning (ML) workflows.
**Amazon SageMaker Pipelinesは、機械学習（ML）ワークフローの構築とオーケストレーションのためのフルマネージドAWSサービス**です。
SageMaker Pipelines offers ML application developers the ability to orchestrate different steps of the ML workflow, including data loading, data transformation, training, tuning, and deployment.
SageMaker Pipelines は、ML アプリケーション開発者に、データロード、データ変換、トレーニング、チューニング、デプロイメントなど、**ML ワークフローのさまざまなステップをオーケストレーションする機能を提供**します。(Orchestratorだ...!)
You can use SageMaker Pipelines to orchestrate ML jobs in SageMaker, and its integration with the larger AWS ecosystem also allows you to use resources like AWS Lambda functions, Amazon EMR jobs, and more.
SageMaker Pipelines を使用して、SageMaker で ML ジョブをオーケストレーションすることができます。また、より大きな AWS エコシステムとの統合により、AWS Lambda 関数や Amazon EMR ジョブなどのリソースを使用することもできます。
(Amazon EMR(Elastic MapReduce) = AWSで大きなデータを分散処理させるためのサービスっぽい。Apache HadoopやApache Sparkなどのオープンソースフレームワークを使う。)
This enables you to build a customized and reproducible pipeline for specific requirements in your ML workflows.
これにより、MLワークフローにおける特定の要件に合わせてカスタマイズされた再現可能なパイプラインを構築することができる。

In this post, we provide some best practices to maximize the value of SageMaker Pipelines and make the development experience seamless.
この記事では、**SageMaker Pipelines の価値を最大化し、開発体験をシームレスにするためのベストプラクティス**を紹介します。
We also discuss some common design scenarios and patterns when building SageMaker Pipelines and provide examples for addressing them.
また、SageMaker Pipelines を構築する際の一般的な設計シナリオとパターンについて説明し、それらに対処するための例を示します。

## 1.1. Best practices for SageMaker Pipelines SageMakerパイプラインのベストプラクティス

In this section, we discuss some best practices that can be followed while designing workflows using SageMaker Pipelines.
このセクションでは、SageMaker Pipelines を使用してワークフローを設計する際のベストプラクティスについて説明します。
Adopting them can improve the development process and streamline the operational management of SageMaker Pipelines.
これらを採用することで、SageMaker Pipelines の開発プロセスを改善し、運用管理を効率化することができます。

### 1.1.1. Use Pipeline Session for lazy loading of the pipeline パイプラインの遅延ロードにはパイプライン・セッションを使用する

Pipeline Session enables lazy initialization of pipeline resources (the jobs are not started until pipeline runtime).
**パイプライン・セッションは、パイプライン・リソースのlazy initialization (遅延初期化)を可能にします**(ジョブはパイプライン実行時まで開始されません)
The PipelineSession context inherits the SageMaker Session and implements convenient methods for interacting with other SageMaker entities and resources, such as training jobs, endpoints, input datasets in Amazon Simple Storage Service (Amazon S3), and so on.
`PipelineSession` コンテキストは SageMaker Session を継承し、トレーニングジョブ、エンドポイント、Amazon Simple Storage Service (Amazon S3) 内の入力データセットなど、他の SageMaker エンティティやリソースとやり取りするための便利なメソッドを実装しています。
When defining SageMaker Pipelines, you should use PipelineSession over the regular SageMaker Session:
SageMaker のパイプラインを定義する場合は、通常の SageMaker セッションよりも PipelineSession を使用する必要があります：

```python
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.sklearn.processing import SKLearnProcessor
role = sagemaker.get_execution_role()
pipeline_session = PipelineSession()
sklearn_processor = SKLearnProcessor(
    framework_version=’0.20.0’,
    instance_type=’ml.m5.xlarge’,
    instance_count=1,
    base_job_name="sklearn-abalone-process",
    role=role,
    sagemaker_session=pipeline_session, # Use PipelineSession
)
```

### 1.1.2. Run pipelines in local mode for cost-effective and quick iterations during development 開発中のパイプラインをローカルモードで実行し、費用対効果に優れた迅速なiteration を行う

You can run a pipeline in local mode using theLocalPipelineSession context.
`LocalPipelineSession` コンテキストを使用して、**ローカルモードでパイプラインを実行でき**ます。
In this mode, the pipeline and jobs are run locally using resources on the local machine, instead of SageMaker managed resources.
このモードでは、パイプラインとジョブは SageMaker が管理するリソースではなく、ローカルマシン上のリソースを使用してローカルに実行されます。
Local mode provides a cost-effective way to iterate on the pipeline code with a smaller subset of data.
ローカル・モードは、**データのより少ないsubset(部分集合)でパイプラインコードをiterationするため**の費用対効果の高い方法を提供します。
After the pipeline is tested locally, it can be scaled to run using the PipelineSession context.
**パイプラインがローカルでテストされた後、PipelineSession コンテキストを使用して実行するようにスケーリングでき**ます。

```python
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.pipeline_context import LocalPipelineSession
local_pipeline_session = LocalPipelineSession()
role = sagemaker.get_execution_role()
sklearn_processor = SKLearnProcessor(
    framework_version=’0.20.0’,
    instance_type=’ml.m5.xlarge,
    instance_count=1,
    base_job_name="sklearn-abalone-process",
    role=role,
    sagemaker_session=local_pipeline_session, # Use LocalPipelineSession
)
```

### 1.1.3. Manage a SageMaker pipeline through versioning バージョン管理による SageMaker パイプラインの管理

Versioning of artifacts and pipeline definitions is a common requirement in the development lifecycle.
**成果物(artifact)とパイプライン定義のバージョニングは、開発ライフサイクルにおける一般的な要件**である。(=つまり必要条件ってことか!)
You can create multiple versions of the pipeline by naming pipeline objects with a unique prefix or suffix, the most common being a timestamp, as shown in the following code:
次のコードに示すように、パイプラインオブジェクトに一意の接頭辞または接尾辞(最も一般的なのはタイムスタンプ)を付けることで、複数のバージョンのパイプラインを作成できる:
(不要になったpipelineは削除していかないとコストがかかりそう...! Sagemaker Pipelines自体にはコストがかからないので、S3のコスト??:thinking:)

```python
from sagemaker.workflow.pipeline_context import PipelineSession
import time

current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
pipeline_name = "pipeline_" + current_time # ここでパイプライン名にタイムスタンプを付けている
pipeline_session = PipelineSession()
pipeline = Pipeline(
    name=pipeline_name,
    steps=[step_process, step_train, step_eval, step_cond],
    sagemaker_session=pipeline_session,
)
```

### 1.1.4. Organize and track SageMaker pipeline runs by integrating with SageMaker Experiments SageMaker Experiments と統合することで、SageMaker パイプラインの実行を整理および追跡

SageMaker Pipelines can be easily integrated with SageMaker Experiments for organizing and tracking pipeline runs.
**SageMaker Pipelines は SageMaker Experiments と簡単に統合でき、パイプラインの実行を整理および追跡できる**。
This is achieved by specifying PipelineExperimentConfig at the time of creating a pipeline object.
これは、パイプラインオブジェクトの作成時に `PipelineExperimentConfig` を指定することで実現できます。
With this configuration object, you can specify an experiment name and a trial name.
**このconfigオブジェクトを使用すると、experiment名とtrial名を指定できる**。
(experiment = 一連のTrialをまとめる為のコンテナ。特定のMLタスクやプロジェクト全体を表す事ができ、それに関連する全てのTrialをまとめる。Experimentの概念を使用する事で、特定の目的に対して実行された様々なアプローチを一元管理できる。)
(trial = Experiment内の1回の試みや実行を表す。Experiment内の1つのTrialは、1つ以上のTrialComponentを持つ。)
(trial component = trialの中の個々のstepやタスクを表す。各trial componentは、その操作の入出力、使用されたパラメータ、得られたmetricsなどの詳細情報を記録する。)
The run details of a SageMaker pipeline get organized under the specified experiment and trial.
**SageMaker パイプラインの実行の詳細は、指定されたexperimentとtrialの下に整理される。**
If you don’t explicitly specify an experiment name, a pipeline name is used for the experiment name.
experiment名を明示的に指定しない場合は、パイプライン名がexperiment名に使用される。(なるほど...! じゃあ基本的にはexperiment名を指定すべきかな...!)
Similarly, if you don’t explicitly specify a trial name, a pipeline run ID is used for the trial or run group name.
同様に、trial名を明示的に指定しない場合は、pipeline run IDがtrial名またはrun group名に使用されます。
(pipeline run ID = pipelineの1度の実行毎の識別子っぽい:thinking:)
(Sagemaker Experimentsにおいて、run group nameという概念は存在しないようなので、trial名の言い換えの意味っぽい...!:thinking:)
(trial内の各trial componentの名前は、trial名+pipeline step名みたいな感じになるのかな...!:thinking:)
See the following code:
次のコードを参照：

```python
Pipeline(
    name="MyPipeline",
    parameters=[...],
    pipeline_experiment_config=PipelineExperimentConfig(
        experiment_name = ExecutionVariables.PIPELINE_NAME,
        trial_name = ExecutionVariables.PIPELINE_EXECUTION_ID
        ), # difine experiment and trial names
    steps=[...]
)
```

### 1.1.5. Securely run SageMaker pipelines within a private VPC プライベート VPC 内で SageMaker パイプラインを安全に実行します

(本番運用の可能性が出てきた気がするので、この辺りの理解が必要になってきた...!:thinking:)

To secure the ML workloads, it’s a best practice to deploy the jobs orchestrated by SageMaker Pipelines in a secure network configuration within a private VPC, private subnets, and security groups.
ML ワークロードを保護するために、**SageMaker Pipelines によってオーケストレーションされたジョブを、プライベート VPC、プライベートサブネット、およびセキュリティグループ内の安全なネットワーク構成で展開することがベストプラクティス**です。
(pipeline自体をVPC内にデプロイする、というよりは、pipelineによって指揮されるジョブをVPC内で動かす、みたいなイメージだろうか...?:thinking:)
(なるほど...?? この様なsecureなネットワーク構成を取る事で、データの漏洩や不正アクセスから守れるってことか...! 逆に言えば、この指定をしなければ、Sagemaker Pipelinesで情報漏洩や不正アクセスのリスクがあるということ...??)
To ensure and enforce the usage of this secure environment, you can implement the following AWS Identity and Access Management (IAM) policy for the SageMaker execution role (this is the role assumed by the pipeline during its run).
**このセキュアな環境の使用を保証し強制するために**、SageMaker 実行ロール(=これはパイプラインの実行にassumeされるロール) に対して、次の AWS Identity and Access Management (IAM) ポリシーを実装できます。
You can also add the policy to run the jobs orchestrated by SageMaker Pipelines in network isolation mode.
SageMaker Pipelines でオーケストレーションされたジョブをネットワーク分離モードで実行するポリシーを追加することもできます。

(なるほど、pipelineに移譲されるIAM roleにこの条件を追加しておく事で、TrainingJobなどを実行させる時にVPCの指定をしないとエラーを返すようになるってことだよね...!:thinking:)

```python
# IAM Policy to enforce execution within a private VPC

{

    "Action": [

        "sagemaker:CreateProcessingJob",
        "sagemaker:CreateTrainingJob",
        "sagemaker:CreateModel"
    ],
    "Resource": "*",
    "Effect": "Deny",
    "Condition": {
        "Null": {
            "sagemaker:VpcSubnets": "true"
        }
    }
}

# IAM Policy to enforce execution in network isolation mode
{

    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": [
                "sagemaker:Create*"
            ],
            "Resource": "*",
            "Condition": {
                "StringNotEqualsIfExists": {
                    "sagemaker:NetworkIsolation": "true"
                }
            }
        }
    ]
}
```

### 1.1.6. Monitor the cost of pipeline runs using tags タグを使用してパイプラインの実行コストを監視する

Using SageMaker pipelines by itself is free; you pay for the compute and storage resources you spin up as part of the individual pipeline steps like processing, training, and batch inference.
SageMakerパイプラインの使用自体は無料です。しかし、processing、training、batch inferenceなどの個々のパイプラインステップの一部としてspin up(=起動する)したコンピュートリソースとストレージリソースに対して支払いが発生します。
(spin up = サーバや計算リソースを起動する、立ち上げる、という意味。特にcloud computingの文脈で使われることが多い。通常、クラウド上のリソースを起動して実行状態にする行動を指す。)
To aggregate the costs per pipeline run, you can include tags in every pipeline step that creates a resource.
パイプライン実行ごとのコストを集計するには、**リソースを作成するすべてのパイプラインステップにタグを含めます**。
These tags can then be referenced in the cost explorer to filter and aggregate total pipeline run cost, as shown in the following example:
これらのタグをコストエクスプローラーで参照することで、以下の例に示すように、パイプラインの実行コストをフィルタリングして集計することができます。

```python
sklearn_processor = SKLearnProcessor(
    framework_version=’0.20.0’,
    instance_type=’ml.m5.xlarge,
    instance_count=1,
    base_job_name="sklearn-abalone-process",
    role=role,
    tags=[{'Key':'pipeline-cost-tag', 'Value':'<<tag_parameter>>'}]# Include tags in the processor
)

step_process = ProcessingStep(
    name="AbaloneProcess",
    processor=sklearn_processor,
    ...
)
```

From the cost explorer, you can now get the cost filtered by the tag:
コスト・エクスプローラーから、タグでフィルタリングされたコストを取得できるようになりました：

```python
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': '2023-07-01',
        'End': '2023-07-15'
        },
    Metrics=['BLENDED_COST','USAGE_QUANTITY','UNBLENDED_COST'],
    Granularity='MONTHLY',
    Filter={
        'Dimensions': {
            'Key':'USAGE_TYPE',
            'Values': [
                ‘SageMaker:Pipeline’
            ]
        },
        'Tags': { # Filter by the tag
            'Key': 'keyName',
            'Values': [
                'keyValue',
                ]
        }
    }
)
```

<!-- ここまで読んだ! -->

## 1.2. Design patterns for some common scenarios よくあるシナリオのデザインパターン

In this section, we discuss design patterns for some common use cases with SageMaker Pipelines.
このセクションでは、SageMaker Pipelines の一般的な使用例に関するデザインパターンについて説明します。

### 1.2.1. Run a lightweight Python function using a Lambda step ラムダステップを使って軽量なPython関数を実行する

Python functions are omnipresent in ML workflows; they are used in preprocessing, postprocessing, evaluation, and more.
Python関数は、MLのワークフローにおいて、前処理、後処理、評価など、あらゆる場面で使用されている。
Lambda is a serverless compute service that lets you run code without provisioning or managing servers.
**Lambdaはserverless compute serviceで、サーバのprovisioningや管理をすることなくコードを実行できる**。(TrainingJobとかもserverless compute serviceって言えるよね...!:thinking:)
(provisioning = サービスを提供するためにサーバや関連リソースを準備、設定、配備する一連のプロセス、の意味...!:thinking:)
With Lambda, you can run code in your preferred language that includes Python.
Lambdaを使えば、Pythonを含む好みの言語でコードを実行できる。
You can use this to run custom Python code as part of your pipeline.
パイプラインの一部としてカスタムPythonコードを実行するために使用できます。
A Lambda step enables you to run Lambda functions as part of your SageMaker pipeline.
Lambda ステップでは、SageMaker パイプラインの一部として Lambda 関数を実行できます。
Start with the following code:
次のコードから始めよう：

```python
%%writefile lambdafunc.py # AWS Lambdaで実行するPythonコードを書く

import json

def lambda_handler(event, context):
    str1 = event["str1"]
    str2 = event["str2"]
    str3 = str1 + str2
    return {
        "str3": str3
    }
```

Create the Lambda function using the SageMaker Python SDK’s Lambda helper:
**SageMaker Python SDK の Lambda ヘルパー**を使用して Lambda 関数を作成します：(そんなのあるんだ...!)

```python
from sagemaker.lambda_helper import Lambda # Lambdaヘルパーをインポート

def create_lambda(function_name, script, handler):
    response = Lambda(
        function_name=function_name,
        execution_role_arn=role,
        script= script,
        handler=handler,
        timeout=600,
        memory_size=10240,
    ).upsert() # ここでupsertして Lambda 関数を作成してる

    function_arn = response['FunctionArn'] # 作成したLambda関数のARNを取得
    return function_arn

fn_arn = create_Lambda("func", "lambdafunc.py", handler = "lambdafunc.lambda_handler")
```

Call the Lambda step:
ラムダ・ステップを呼び出す:
(Pipeline内にLambdaステップを追加してる)

```python
from sagemaker.lambda_helper import Lambda
from sagemaker.workflow.lambda_step import (
    LambdaStep,
    LambdaOutput,
    LambdaOutputTypeEnum
) # こういうLambda用のヘルパー用のクラスがあるんだ...!

str3 = LambdaOutput(output_name="str3", output_type=LambdaOutputTypeEnum.String)

# Lambda Step
step_lambda1 = LambdaStep(
    name="LambdaStep1",
    lambda_func=Lambda(
        function_arn=fn_arn
    ),
    inputs={
        "str1": "Hello",
        "str2": " World"
    },
    outputs=[str3],
)
```

<!-- ここまで読んだ! -->

### 1.2.2. Pass data between steps ステップ間のデータの受け渡し

(この辺りの小技を紹介してくれるのいいね...!:thinking:)
Input data for a pipeline step is either an accessible data location or data generated by one of the previous steps in the pipeline.
**パイプラインステップの入力データは、アクセス可能なdata locationまたはパイプライン内の前のステップで生成されたデータのいずれかです**。(うんうん...!)
You can provide this information as a ProcessingInput parameter.
この情報は、 `ProcessingInput` パラメータとして提供できる。
Let’s look at a few scenarios of how you can use ProcessingInput.
**`ProcessingInput` の使い方のいくつかのシナリオ**を見てみよう。

#### Scenario 1: Pass the output (primitive data types) of a Lambda step to a processing step シナリオ1： ラムダ・ステップの出力（プリミティブ・データ型）を処理ステップに渡す

Primitive data types refer to scalar data types like string, integer, Boolean, and float.
Primitive data typesとは、文字列、整数、ブール値、浮動小数点数などのscalar data typesのことです。
(primitive = 原始的な、基本的な、という意味。プログラミングの文脈では、基本的なデータ型を指すことが多い。)

The following code snippet defines a Lambda function that returns a dictionary of variables with primitive data types.
以下のコード・スニペットは、**プリミティブなデータ型を持つ変数の辞書を返すラムダ関数**を定義しています。(異種コレクションだ...!ロバストPythonでは避けたいやつ...!:thinking:)
Your Lambda function code will return a JSON of key-value pairs when invoked from the Lambda step within the SageMaker pipeline.
Lambda 関数コードは、SageMaker パイプライン内の Lambda ステップから呼び出されると、key-value ペアの JSON を返します。(S3に出力される??:thinking:)

```python
def handler(event, context):
    ...
    return {
        "output1": "string_value",
        "output2": 1,
        "output3": True,
        "output4": 2.0,
    }
```

In the pipeline definition, you can then define SageMaker pipeline parameters that are of a specific data type and set the variable to the output of the Lambda function:
パイプライン定義では、**特定のデータ型の SageMaker Pipeline parametersを定義し、その変数を Lambda 関数の出力に設定できます**:
(なるほど...! pipeline parametersって、pipeline実行に指定するハイパーパラメータ的な使い方しかできないと思っていた...! この使い方よさそう...!:thinking:)

(あ、下記の実装を見た感じでは、`sagemaker.workflow.parameters`モジュールを使ってパラメータ定義してるわけでは無さそう...??)

```python
from sagemaker.workflow.lambda_step import (
    LambdaStep,
    LambdaOutput,
    LambdaOutputTypeEnum
)
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.sklearn.processing import SKLearnProcessor

role = sagemaker.get_execution_role()
pipeline_session = PipelineSession()

# 1. Define the output params of the Lambda Step

str_outputParam = LambdaOutput(output_name="output1", output_type=LambdaOutputTypeEnum.String)
int_outputParam = LambdaOutput(output_name"output2", output_type=LambdaOutputTypeEnum.Integer)
bool_outputParam = LambdaOutput(output_name"output3", output_type=LambdaOutputTypeEnum.Boolean)
float_outputParam = LambdaOutput(output_name"output4", output_type=LambdaOutputTypeEnum.Float)

# 2. Lambda step invoking the lambda function and returns the Output (invoke = 呼び出す)

step_lambda = LambdaStep(
    name="MyLambdaStep",
    lambda_func=Lambda(
        function_arn="arn:aws:lambda:us-west-2:123456789012:function:sagemaker_test_lambda",
        session=PipelineSession(),
        ),
    inputs={"arg1": "foo", "arg2": "foo1"},
    outputs=[
        str_outputParam, int_outputParam, bool_outputParam, float_outputParam
        ],
)

# 3. Extract the output of the Lambda
#  (ん?? str_outputParamをmutableに扱ってる?)
# (そうそう、stepオブジェクトのpropertiesから色んな情報を取得できるんだよね...!)
str_outputParam = step_lambda.properties.Outputs["output1"]

# 4. Use it in a subsequent step. For ex. Processing step

sklearn_processor = SKLearnProcessor(
    framework_version="0.23-1",
    instance_type="ml.m5.xlarge",
    instance_count=1,
    sagemaker_session=pipeline_session,
    role=role
)

processor_args = sklearn_processor.run(
    code="code/preprocess.py", #python script to run
    arguments=["--input-args", str_outputParam] # Lambda stepの出力を引数として渡してる
)

step_process = ProcessingStep(
    name="processstep1",
    step_args=processor_args,
)
```

#### Scenario 2: Pass the output (non-primitive data types) of a Lambda step to a processing step シナリオ2： Lambdaステップの出力（非プリミティブデータ型）を処理ステップに渡す

Non-primitive data types refer to non-scalar data types (for example, NamedTuple).
**Non-primitiveデータ型とは、スカラーでないデータ型のことである**（例えば、NamedTuple）。(あ、build-inなデータ型でも、scalarじゃなかったらnon-primitive型なのか...!)
You may have a scenario when you have to return a non-primitive data type from a Lambda function.
ラムダ関数から非プリミティブなデータ型を返さなければならないシナリオがあるかもしれない。
To do this, you have to convert your non-primitive data type to a string:
そのためには、non-primitiveデータ型を文字列に変換する必要がある：

```python
# Lambda function code returning a non primitive data type

from collections import namedtuple

def lambda_handler(event, context):
    Outputs = namedtuple("Outputs", "sample_output") # Define a named tuple class
    named_tuple = Outputs(
                    [
                        {'output1': 1, 'output2': 2},
                        {'output3': 'foo', 'output4': 'foo1'}
                    ]
                )
    return{
        "named_tuple_string": str(named_tuple) # Lambda関数を定義する際に、non-primitiveデータ型を文字列に変換して返してる...!
    }
#Pipeline step that uses the Lambda output as a “Parameter Input”

output_ref = step_lambda.properties.Outputs["named_tuple_string"]
```

Then you can use this string as an input to a subsequent step in the pipeline.
そして、**この文字列をパイプラインの後続ステップの入力として使うことができる**。 (逆に、strに変換しないと、後続のステップで使いづらいのかな。というかそもそも、AWS Lambda Stepの出力はprimitive型しか受け渡しできないのかな...??)

To use the named tuple in the code, use eval() to parse the Python expression in the string:
コード内で名前付きタプルを使用するには、`eval()`を使用して文字列内のPython式を解析する：

```python
# Decipher the string in your processing logic code
# プロセッシングロジックコード内で文字列を解読する

import argparse
from collections import namedtuple

Outputs = namedtuple("Outputs", "sample_output") # ここでも同じNamedTupleを定義している。このデータ型を知らないとparseできないもんね...!

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--named_tuple_string", type=str, required=True)
    args = parser.parse_args()
    #use eval to obtain the named tuple from the string
    named_tuple = eval(args.named_tuple_string)
```

#### Scenario 3: Pass the output of a step through a property file シナリオ 3： プロパティファイルを通してステップの出力を渡す

(AWS LambdaをPipelineに組み込まない場合は、このシナリオが基本だよね...!:thinking:)

You can also store the output of a processing step in a property JSON file for downstream consumption in a ConditionStep or another ProcessingStep.
**また、処理ステップの出力をproperty JSONファイルに保存して、ConditionStep または別の ProcessingStep で下流で使用することもできます**。(property jsonファイル...?? これは、S3に保存されるのかな...??)
You can use the JSONGet function to query a property file.
JSONGet関数を使用すると、propertyファイルを参照できる。
See the following code:
以下のコードを参照：

```python
# 1. Define a Processor with a ProcessingOutput
sklearn_processor = SKLearnProcessor(
    framework_version="0.23-1",
    instance_type="ml.m5.xlarge",
    instance_count=1,
    base_job_name="sklearn-abalone-preprocess",
    sagemaker_session=session,
    role=sagemaker.get_execution_role(),
)

step_args = sklearn_processor.run(

                outputs=[
                    ProcessingOutput(
                        output_name="hyperparam",
                        source="/opt/ml/processing/evaluation"
                    ),
                ],
            code="./local/preprocess.py",
            arguments=["--input-data", "s3://my-input"],
)

# 2. Define a PropertyFile where the output_name matches that with the one used in the Processor
hyperparam_report = PropertyFile(
    name="AbaloneHyperparamReport",
    output_name="hyperparam", # output_nameはProcessorで指定したものと一致させる必要がある?
    path="hyperparam.json",
)
```

Let’s assume the property file’s contents were the following:
プロパティファイルの内容が以下のようなものだったとしよう：
(これがProcessingJobの成果物だよね...!:thinking:)

```json
{
  "hyperparam": {
    "eta": {
      "value": 0.6
    }
  }
}
```

In this case, it can be queried for a specific value and used in subsequent steps using the JsonGet function:
この場合、JsonGet関数を使用して特定の値を照会し、後続のステップで使用することができます：

```python
# 3. Query the property file
eta = JsonGet(
    step_name=step_process.name,
    property_file=hyperparam_report,
    json_path="hyperparam.eta.value",
)
```

<!-- ここまで読んだ! property fileはよく分かってない...!:thinking: -->

### 1.2.3. Parameterize a variable in pipeline definition パイプライン定義で変数をパラメータ化する

Parameterizing variables so that they can be used at runtime is often desirable—for example, to construct an S3 URI.
実行時に使用できるように変数をパラメータ化することは、S3のURIを構築する場合など、しばしば望ましい。
You can parameterize a string such that it is evaluated at runtime using the Join function.
Join関数を使えば、**実行時に評価されるように文字列をパラメータ化することができる**。(お...!)
The following code snippet shows how to define the variable using the Join function and use that to set the output location in a processing step:
次のコード・スニペットは、Join関数を使って変数を定義し、それを使って処理ステップで出力場所を設定する方法を示している:

```python
# define the variable to store the s3 URI
# (これは単に、複数のstrを"/"でjoinしてるってこと??)
s3_location = Join(
    on="/",
    values=[
        "s3:/",
        ParameterString(
            name="MyBucket",
            default_value=""
        ),
        "training",
        ExecutionVariables.PIPELINE_EXECUTION_ID # pipelineの実行毎にユニークなid
    ]
)

# define the processing step
sklearn_processor = SKLearnProcessor(
    framework_version="1.2-1",
    instance_type="ml.m5.xlarge",
    instance_count=processing_instance_count,
    base_job_name=f"{base_job_prefix}/sklearn-abalone-preprocess",
    sagemaker_session=pipeline_session,
    role=role,
)

# use the s3uri as the output location in processing step
processor_run_args = sklearn_processor.run(
    outputs=[
        ProcessingOutput(
            output_name="train",
            source="/opt/ml/processing/train",
            destination=s3_location, # ここで出力先のs3 URIを指定している
        ),
    ],
    code="code/preprocess.py"
)

step_process = ProcessingStep(
    name="PreprocessingJob”,
    step_args=processor_run_args,
)
```

<!-- ここまで読んだ! -->

### 1.2.4. Run parallel code over an iterable iterable(反復可能?)なコードに対して並列コードを実行する

Some ML workflows run code in parallel for-loops over a static set of items (an iterable).
いくつかのMLワークフローは、**静的なアイテムの集合(反復可能なもの)に対して、並列のforループでコードを実行する**。(ユーザ集合に対して、各ユーザのベクトルを推論する時とか??)
It can either be the same code that gets run on different data or a different piece of code that needs to be run for each item.
それは、**異なるデータに対して実行される同じコードであるか、各アイテムに対して実行する必要がある異なるコードであるかもしれない**。(うんうん...!)
For example, if you have a very large number of rows in a file and want to speed up the processing time, you can rely on the former pattern.
例えば、ファイル内の行数が非常に多く、処理時間を短縮したい場合は、前者のパターンに頼ることができる。(ex. ユーザ集合に対して、各ユーザのベクトルを推論する時とか??)
If you want to perform different transformations on specific sub-groups in the data, you might have to run a different piece of code for every sub-group in the data.
データ内の特定のサブグループに対して異なる変換を行いたい場合、データ内のサブグループごとに異なるコードを実行しなければならないかもしれない。(これは後者のパターン?)
The following two scenarios illustrate how you can design SageMaker pipelines for this purpose.
次の 2 つのシナリオは、この目的のために SageMaker パイプラインを設計する方法を示しています。

#### 1.2.4.1. Scenario 1: Implement a processing logic on different portions of data シナリオ1：データの異なる部分(集合)に処理ロジックを実装する

(これは前者のパターンの話?? あれ? 後者??)

You can run a processing job with multiple instances (by setting instance_count to a value greater than 1).
複数のインスタンスで処理ジョブを実行できます(`instance_count` を1より大きい値に設定することで)
This distributes the input data from Amazon S3 into all the processing instances.
**これは、Amazon S3からの入力データをすべての処理インスタンスに分散する**。
You can then use a script (process.py) to work on a specific portion of the data based on the instance number and the corresponding element in the list of items.
その後、スクリプト(`process.py`)を使用して、**インスタンス番号とアイテムのリスト内の対応する要素に基づいて**、データの特定の部分に作用することができます。(ex. instance番号 = 1は user_id = 0 ~ 1000, instance番号 = 2は user_id = 1001 ~ 2000 みたいな感じ?? この対応表って、こちらが明示的に指定する必要があるのかな??:thinking:)
The programming logic in process.py can be written such that a different module or piece of code gets run depending on the list of items that it processes.
process.pyのプログラミングロジックは、処理するアイテムのリストに応じて、異なるモジュールやコードの一部が実行されるように書くことができます。(ここは普通にPython力か。)
The following example defines a processor that can be used in a ProcessingStep:
以下の例では、ProcessingStep で使用できる processor を定義しています:

```python
sklearn_processor = FrameworkProcessor(
    estimator_cls=sagemaker.sklearn.estimator.SKLearn,
    framework_version="0.23-1",
    instance_type='ml.m5.4xlarge',
    instance_count=4, #number of parallel executions / instances
    base_job_name="parallel-step",
    sagemaker_session=session,
    role=role,F
)

step_args = sklearn_processor.run(
    code='process.py',
    arguments=[
        "--items",
        list_of_items, #data structure containing a list of items
        # arguments引数の中でinputsって定義されなくない??ミスっぽい。
        inputs=[
            ProcessingInput(source="s3://sagemaker-us-east-1-xxxxxxxxxxxx/abalone/abalone-dataset.csv",
                    destination="/opt/ml/processing/input"
            ) # 処理したいデータの実体はこっちにあるんだよね?? コマンドライン引数として渡されるlist_of_itemsの役割は??:thinking:
        ],
    ]
)
```

#### 1.2.4.2. Scenario 2: Run a sequence of steps シナリオ2： 一連のステップを実行する

(これは、pipelineの実行全体を並列化するシナリオ??)

When you have a sequence of steps that need to be run in parallel, you can define each sequence as an independent SageMaker pipeline.
**並行して実行する必要がある一連のステップがある場合**、各sequenceを独立した SageMaker パイプラインとして定義できます。
The run of these SageMaker pipelines can then be triggered from a Lambda function that is part of a LambdaStep in the parent pipeline.
これらの SageMaker パイプラインの実行は、**親パイプライン**の一部である LambdaStep からトリガーされる Lambda 関数から実行できます。
The following piece of code illustrates the scenario where two different SageMaker pipeline runs are triggered:
次のコードは、**2 つの異なる SageMaker パイプラインの実行がトリガーされるシナリオ**を示しています:
(つまりこれは、2つのpipelineを同時に実行したいシナリオってこと?? EventBridgeで両方を同じルールに登録すればよくない??)

```python
import boto3

# pilelineをTriggerするLambda関数っぽい!
def lambda_handler(event, context):
    items = [1, 2]
    #sagemaker client
    sm_client = boto3.client("sagemaker")

    #name of the pipeline that needs to be triggered.(トリガーするパイプラインの名前)
    #if there are multiple, you can fetch available pipelines using boto3 api (もし複数ある場合は、boto3 apiを使って利用可能なパイプラインを取得できます。)
    #and trigger the appropriate one based on your logic. (そして、ロジックに基づいて適切なものをトリガーします。)
    pipeline_name = 'child-pipeline-1'

    #trigger pipeline for every item
    response_ppl = sm_client.start_pipeline_execution(
                        PipelineName=pipeline_name,
                        PipelineExecutionDisplayName=pipeline_name+'-item-%d' %(s),
                    )
    pipeline_name = 'child-pipeline-2'
    response_ppl = sm_client.start_pipeline_execution(
                        PipelineName=pipeline_name,
                        PipelineExecutionDisplayName=pipeline_name+'-item-%d' %(s),
                    )
return
```

## 1.3. Conclusion 結論

In this post, we discussed some best practices for the efficient use and maintenance of SageMaker pipelines.
この投稿では、**SageMakerパイプラインの効率的な使用と保守のためのベストプラクティス**について説明しました。
We also provided certain patterns that you can adopt while designing workflows with SageMaker Pipelines, whether you are authoring new pipelines or are migrating ML workflows from other orchestration tools.
また、**新しいパイプラインを作成する場合でも、他のオーケストレーションツールから ML ワークフローを移行する場合でも、SageMaker Pipelines でワークフローを設計する際に採用できる特定のパターン**も提供しました。
To get started with SageMaker Pipelines for ML workflow orchestration, refer to the code samples on GitHub and Amazon SageMaker Model Building Pipelines.
ML ワークフローのオーケストレーションに SageMaker Pipelines を使い始めるには、[GitHub のコードサンプル](https://github.com/aws/amazon-sagemaker-examples/tree/main/sagemaker-pipelines)と [Amazon SageMaker Model Building Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html) を参照してください。

<!-- ここまで読んだ! -->
