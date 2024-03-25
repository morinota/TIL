## refs 審判

- https://docs.aws.amazon.com/sagemaker/latest/dg/kubernetes-sagemaker-components-for-kubeflow-pipelines.html https://docs.aws.amazon.com/sagemaker/latest/dg/kubernetes-sagemaker-components-for-kubeflow-pipelines.html

# SageMaker Components for Kubeflow Pipelines KubeflowパイプラインのためのSageMakerコンポーネント

This document outlines how to use SageMaker Components for Kubeflow Pipelines.
このドキュメントでは、Kubeflowパイプライン用のSageMakerコンポーネントの使用方法について概説します。
With these pipeline components, you can create and monitor native SageMaker training, tuning, endpoint deployment, and batch transform jobs from your Kubeflow Pipelines.
これらのパイプラインコンポーネントを使用すると、KubeflowパイプラインからネイティブのSageMakerトレーニング、チューニング、エンドポイントデプロイ、バッチ変換ジョブを作成および監視できます。
By running Kubeflow Pipeline jobs on SageMaker, you move data processing and training jobs from the Kubernetes cluster to SageMaker's machine learning-optimized managed service.
SageMaker 上で Kubeflow Pipeline ジョブを実行することで、データ処理とトレーニングのジョブを Kubernetes クラスタから SageMaker の機械学習に最適化されたマネージドサービスに移動します。
This document assumes prior knowledge of Kubernetes and Kubeflow.
このドキュメントでは、KubernetesとKubeflowに関する予備知識を前提としている。

Contents
内容

What are Kubeflow Pipelines?
Kubeflowパイプラインとは？

What are Kubeflow Pipeline components?
Kubeflow Pipelineのコンポーネントとは？

Why use SageMaker Components for Kubeflow Pipelines?
なぜKubeflowパイプラインにSageMaker Componentsを使うのか？

SageMaker Components for Kubeflow Pipelines versions
Kubeflow パイプライン用 SageMaker コンポーネント バージョン

List of SageMaker Components for Kubeflow Pipelines
Kubeflowパイプライン用SageMakerコンポーネント一覧

IAM permissions
IAMパーミッション

Converting pipelines to use SageMaker
SageMaker を使用するようにパイプラインを変換する

Install Kubeflow Pipelines
Kubeflowパイプラインのインストール

Use SageMaker components
SageMakerコンポーネントを使用する

## What are Kubeflow Pipelines? Kubeflowパイプラインとは？

Kubeflow Pipelines (KFP) is a platform for building and deploying portable, scalable machine learning (ML) workflows based on Docker containers.
Kubeflow Pipelines（KFP）は、Dockerコンテナをベースとした、ポータブルでスケーラブルな機械学習（ML）ワークフローを構築・デプロイするためのプラットフォームです。
The Kubeflow Pipelines platform consists of the following:
Kubeflow Pipelinesプラットフォームは以下のように構成されている：

A user interface (UI) for managing and tracking experiments, jobs, and runs.
実験、ジョブ、ランを管理・追跡するためのユーザーインターフェース（UI）。

An engine (Argo) for scheduling multi-step ML workflows.
マルチステップのMLワークフローをスケジューリングするためのエンジン（Argo）。

An SDK for defining and manipulating pipelines and components.
パイプラインとコンポーネントを定義し、操作するためのSDK。

Notebooks for interacting with the system using the SDK.
SDKを使用してシステムとやり取りするためのノートブック。

A pipeline is a description of an ML workflow expressed as a directed acyclic graph.
パイプラインとは、MLのワークフローを有向非循環グラフで表現したものである。
Every step in the workflow is expressed as a Kubeflow Pipeline component, which is a AWS SDK for Python (Boto3) module.
ワークフローの各ステップは、AWS SDK for Python（Boto3）モジュールであるKubeflow Pipelineコンポーネントとして表現される。

For more information on Kubeflow Pipelines, see the Kubeflow Pipelines documentation.
Kubeflow Pipelinesの詳細については、Kubeflow Pipelinesのドキュメントを参照してください。

## What are Kubeflow Pipeline components? Kubeflowパイプラインコンポーネントとは？

A Kubeflow Pipeline component is a set of code used to execute one step of a Kubeflow pipeline.
Kubeflow Pipelineコンポーネントは、Kubeflowパイプラインの1ステップを実行するために使用されるコードのセットです。
Components are represented by a Python module built into a Docker image.
コンポーネントは、Dockerイメージに組み込まれたPythonモジュールで表される。
When the pipeline runs, the component's container is instantiated on one of the worker nodes on the Kubernetes cluster running Kubeflow, and your logic is executed.
パイプラインが実行されると、コンポーネントのコンテナがKubeflowを実行しているKubernetesクラスタ上のワーカーノードの1つにインスタンス化され、あなたのロジックが実行される。
Pipeline components can read outputs from the previous components and create outputs that the next component in the pipeline can consume.
パイプラインコンポーネントは、前のコンポーネントから出力を読み取り、パイプラインの次のコンポーネントが消費できる出力を作成することができます。
These components make it fast and easy to write pipelines for experimentation and production environments without having to interact with the underlying Kubernetes infrastructure.
これらのコンポーネントにより、基盤となるKubernetesインフラストラクチャとやり取りすることなく、実験および本番環境用のパイプラインを迅速かつ簡単に記述できる。

You can use SageMaker Components in your Kubeflow pipeline.
Kubeflow パイプラインで SageMaker Components を使用できます。
Rather than encapsulating your logic in a custom container, you simply load the components and describe your pipeline using the Kubeflow Pipelines SDK.
カスタムコンテナにロジックをカプセル化するのではなく、Kubeflow Pipelines SDKを使用してコンポーネントをロードし、パイプラインを記述するだけです。
When the pipeline runs, your instructions are translated into a SageMaker job or deployment.
パイプラインが実行されると、あなたの指示が SageMaker のジョブまたはデプロイメントに変換されます。
The workload then runs on the fully managed infrastructure of SageMaker.
ワークロードは、SageMaker の完全に管理されたインフラストラクチャ上で実行されます。

## Why use SageMaker Components for Kubeflow Pipelines? なぜ Kubeflow パイプラインに SageMaker Components を使うのか？

SageMaker Components for Kubeflow Pipelines offer an alternative to launching your compute-intensive jobs from SageMaker.
SageMaker Components for Kubeflow Pipelines は、SageMaker から計算負荷の高いジョブを起動するための代替手段を提供します。
The components integrate SageMaker with the portability and orchestration of Kubeflow Pipelines.
このコンポーネントは、SageMakerをKubeflowパイプラインの移植性とオーケストレーションと統合します。
Using the SageMaker Components for Kubeflow Pipelines, you can create and monitor your SageMaker resources as part of a Kubeflow Pipelines workflow.
SageMaker Components for Kubeflow Pipelines を使用すると、Kubeflow Pipelines ワークフローの一部として SageMaker リソースを作成および監視できます。
Each of the jobs in your pipelines runs on SageMaker instead of the local Kubernetes cluster allowing you to take advantage of key SageMaker features such as data labeling, large-scale hyperparameter tuning and distributed training jobs, or one-click secure and scalable model deployment.
パイプラインの各ジョブは、ローカルのKubernetesクラスタではなくSageMaker上で実行されるため、データラベリング、大規模なハイパーパラメータチューニング、分散トレーニングジョブ、またはワンクリックで安全かつスケーラブルなモデルデプロイメントなどのSageMakerの主要機能を利用できます。
The job parameters, status, logs, and outputs from SageMaker are still accessible from the Kubeflow Pipelines UI.
SageMakerからのジョブパラメータ、ステータス、ログ、出力は、Kubeflow Pipelines UIから引き続きアクセス可能です。

The SageMaker components integrate key SageMaker features into your ML workflows from preparing data, to building, training, and deploying ML models.
SageMaker コンポーネントは、データの準備から ML モデルの構築、トレーニング、デプロイまで、SageMaker の主要な機能を ML ワークフローに統合します。
You can create a Kubeflow Pipeline built entirely using these components, or integrate individual components into your workflow as needed.
これらのコンポーネントを完全に使用してKubeflowパイプラインを作成することも、必要に応じて個々のコンポーネントをワークフローに統合することもできます。
The components are available in one or two versions.
コンポーネントは1つまたは2つのバージョンで利用できる。
Each version of a component leverages a different backend.
コンポーネントのバージョンごとに、異なるバックエンドを利用する。
For more information on those versions, see SageMaker Components for Kubeflow Pipelines versions.
これらのバージョンの詳細については、「SageMaker Components for Kubeflow Pipelines versions」を参照してください。

There is no additional charge for using SageMaker Components for Kubeflow Pipelines.
SageMaker Components for Kubeflow Pipelines を使用するための追加料金はかかりません。
You incur charges for any SageMaker resources you use through these components.
これらのコンポーネントを通じて使用する SageMaker リソースには料金が発生します。

## SageMaker Components for Kubeflow Pipelines versions Kubeflowパイプライン用SageMakerコンポーネントのバージョン

SageMaker Components for Kubeflow Pipelines come in two versions.
SageMaker Components for Kubeflow Pipelinesには2つのバージョンがあります。
Each version leverages a different backend to create and manage resources on SageMaker.
各バージョンでは、SageMaker 上でリソースを作成および管理するために、異なるバックエンドを利用しています。

The SageMaker Components for Kubeflow Pipelines version 1 (v1.x or below) use Boto3 (AWS SDK for Python (Boto3)) as backend.
SageMaker Components for Kubeflow Pipelines バージョン1（v1.x以下）では、バックエンドとしてBoto3（AWS SDK for Python（Boto3））を使用しています。

The version 2 (v2.0.0-alpha2 and above) of SageMaker Components for Kubeflow Pipelines use SageMaker Operator for Kubernetes (ACK).
SageMaker Components for Kubeflow Pipelines のバージョン 2 (v2.0.0-alpha2 以上) では、SageMaker Operator for Kubernetes (ACK) を使用します。

AWS introduced ACK to facilitate a Kubernetes-native way of managing AWS Cloud resources.
AWSはACKを導入し、AWSクラウドのリソースをKubernetesネイティブに管理できるようにした。
ACK includes a set of AWS service-specific controllers, one of which is the SageMaker controller.
ACKには、AWSサービス固有のコントローラのセットが含まれており、その1つがSageMakerコントローラである。
The SageMaker controller makes it easier for machine learning developers and data scientists using Kubernetes as their control plane to train, tune, and deploy machine learning (ML) models in SageMaker.
SageMakerコントローラは、Kubernetesをコントロールプレーンとして使用する機械学習開発者やデータ科学者が、SageMakerで機械学習（ML）モデルをトレーニング、チューニング、デプロイすることを容易にします。
For more information, see SageMaker Operators for Kubernetes
詳細については、SageMaker Operators for Kubernetesを参照してください。

Both versions of the SageMaker Components for Kubeflow Pipelines are supported.
SageMaker Components for Kubeflow Pipelines の両方のバージョンがサポートされています。
However, the version 2 provides some additional advantages.
しかし、バージョン2にはさらにいくつかの利点がある。
In particular, it offers:
特に、それは提供される：

A consistent experience to manage your SageMaker resources from any application; whether you are using Kubeflow pipelines, or Kubernetes CLI (kubectl) or other Kubeflow applications such as Notebooks.
Kubeflow パイプライン、Kubernetes CLI (kubectl)、Notebooks などの Kubeflow アプリケーションのいずれを使用していても、どのアプリケーションからでも SageMaker リソースを一貫して管理できます。

The flexibility to manage and monitor your SageMaker resources outside of the Kubeflow pipeline workflow.
Kubeflowパイプラインワークフローの外側でSageMakerリソースを管理・監視できる柔軟性。

Zero setup time to use the SageMaker components if you deployed the full Kubeflow on AWS release since the SageMaker Operator is part of its deployment.
Kubeflow on AWSのフルリリースをデプロイした場合、SageMaker Operatorはそのデプロイの一部であるため、SageMakerコンポーネントを使用するためのセットアップ時間はゼロです。

## List of SageMaker Components for Kubeflow Pipelines Kubeflowパイプライン用SageMakerコンポーネント一覧

The following is a list of all SageMaker Components for Kubeflow Pipelines and their available versions.
以下は、Kubeflowパイプライン用のすべてのSageMakerコンポーネントと利用可能なバージョンの一覧です。
Alternatively, you can find all SageMaker Components for Kubeflow Pipelines in GitHub.
または、Kubeflowパイプライン用のすべてのSageMakerコンポーネントをGitHubで見つけることができます。

## IAM permissions IAMパーミッション

Deploying Kubeflow Pipelines with SageMaker components requires the following three layers of authentication:
SageMaker コンポーネントで Kubeflow パイプラインをデプロイするには、以下の 3 層の認証が必要です：

An IAM role granting your gateway node (which can be your local machine or a remote instance) access to the Amazon Elastic Kubernetes Service (Amazon EKS) cluster.
ゲートウェイノード（ローカルマシンでもリモートインスタンスでも可）にAmazon Elastic Kubernetes Service（Amazon EKS）クラスタへのアクセスを許可するIAMロール。

The user accessing the gateway node assumes this role to:
ゲートウェイノードにアクセスするユーザーは、この役割を担う：

Create an Amazon EKS cluster and install KFP
Amazon EKSクラスタを作成し、KFPをインストールする。

Create IAM roles
IAMロールの作成

Create Amazon S3 buckets for your sample input data
サンプル入力データ用にAmazon S3バケットを作成します。

The role requires the following permissions:
この役割には以下の権限が必要です：

CloudWatchLogsFullAccess
CloudWatchLogsFullAccess

AWSCloudFormationFullAccess
AWSCloudFormationFullAccess

IAMFullAccess
IAMFullAccess

AmazonS3FullAccess
AmazonS3フルアクセス

AmazonEC2FullAccess
アマゾンEC5C

AmazonEKSAdminPolicy (Create this policy using the schema from Amazon EKS Identity-Based Policy Examples)
AmazonEKSAdminPolicy (Amazon EKS Identity-Based Policy Examples のスキーマを使用してこのポリシーを作成する)

A Kubernetes IAM execution role assumed by Kubernetes pipeline pods (kfp-example-pod-role) or the SageMaker Operator for Kubernetes controller pod to access SageMaker.
Kubernetesパイプラインポッド（kfp-example-pod-role）またはSageMakerにアクセスするためのKubernetesコントローラポッド用のSageMaker Operatorによって想定されるKubernetes IAM実行ロール。
This role is used to create and monitor SageMaker jobs from Kubernetes.
このロールは、Kubernetes から SageMaker ジョブを作成および監視するために使用されます。

The role requires the following permission:
この役割には以下の許可が必要である：

AmazonSageMakerFullAccess
AmazonSageMakerフルアクセス

You can limit permissions to the KFP and controller pods by creating and attaching your own custom policy.
独自のカスタムポリシーを作成して添付することで、KFPとコントローラポッドへの権限を制限できます。

A SageMaker IAM execution role assumed by SageMaker jobs to access AWS resources such as Amazon S3 or Amazon ECR (kfp-example-sagemaker-execution-role).
SageMaker ジョブが Amazon S3 や Amazon ECR などの AWS リソースにアクセスするために想定する SageMaker IAM 実行ロール (kfp-example-sagemaker-execution-role) 。

SageMaker jobs use this role to:
SageMaker のジョブは、このロールを次のように使用します：

Access SageMaker resources
SageMakerリソースへのアクセス

Input Data from Amazon S3
アマゾンS3からの入力データ

Store your output model to Amazon S3
出力モデルをAmazon S3に保存する

The role requires the following permissions:
この役割には以下の権限が必要です：

AmazonSageMakerFullAccess
AmazonSageMakerフルアクセス

AmazonS3FullAccess
AmazonS3フルアクセス

## Converting pipelines to use SageMaker パイプラインを SageMaker に変換する

You can convert an existing pipeline to use SageMaker by porting your generic Python processing containers and training containers.
汎用の Python 処理コンテナとトレーニングコンテナを移植することで、既存のパイプラインを SageMaker を使用するように変換できます。
If you are using SageMaker for inference, you also need to attach IAM permissions to your cluster and convert an artifact to a model.
推論に SageMaker を使用している場合は、クラスタに IAM パーミッションをアタッチし、アーティファクトをモデルに変換する必要もあります。