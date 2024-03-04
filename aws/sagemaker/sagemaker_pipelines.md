## refs

- [Get started with SageMaker Pipelines](https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-pipelines/index.html)
- [Orchestrate Jobs to Train and Evaluate Models with Amazon SageMaker Pipelines](https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-pipelines/tabular/abalone_build_train_deploy/sagemaker-pipelines-preprocess-train-evaluate-batch-transform.html)

# AWS Sagemaker Pipelines

## Sagemaker Pipelines とは?

- Sagemakekジョブをorchestrateし、再現可能なMLパイプラインを開発・運用するためのサービス。
- Sagemaker Pipelinesは、直接的には、JSON形式の**Sagemaker Pipeline DSL(ドメイン固有言語)**で定義される。
  - このDSLでは、パイプラインパラメータとSagemakerジョブのdirected acyclic graph(DAG、有向非巡回グラフ)を定義する。
  - Sagemaker Python SDK(Software Development Kit)を使えば慣れ親しんだPythonコードでSagemaker Pipeline DSLの生成が可能。
    - (ここはcdkみたいな感じか...!!)

## Sagemaker Pipelines の機能:

サポートする機能は以下:

- Pipelines
- Processing job steps
- Training job steps
- Conditional execution steps
- Registering model steps
- hogehoge
