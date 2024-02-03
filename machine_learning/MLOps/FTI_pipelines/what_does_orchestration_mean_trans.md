## link リンク

https://www.hopsworks.ai/dictionary/orchestration#:~:text=Orchestration%20of%20ML%20pipelines%20refers,of%20the%20different%20ML%20pipelines.
https://www.hopsworks.ai/dictionary/orchestration#:~:text=Orchestration%20of%20ML%20pipelines%20refers,of%20different%20ML%20pipelines。

# Orchestration オーケストレーション

## What does the orchestration of ML pipelines mean?

MLパイプラインのオーケストレーションは何を意味するのか？

‍The orchestration of ML pipelines is crucial to making ML pipelines run without human intervention, and run reliably, even in the event of hardware or software errors.
MLパイプラインのオーケストレーションは、MLパイプラインを人間の介入なしに実行し、ハードウェアやソフトウェアにエラーが発生した場合でも確実に実行するために極めて重要です。

Orchestration of ML pipelines refers to the process of automating the execution of the feature/training/inference pipeline.
**MLパイプラインのオーケストレーションとは、特徴/学習/推論パイプラインの実行を自動化するプロセス**を指す。
Ideally, a single orchestrator tool should manage the execution of the different ML pipelines.
理想的には、単一のオーケストレーター・ツールが異なるMLパイプラインの実行を管理すべきである。

## Which ML pipelines need to be orchestrated?

どのMLパイプラインをオーケストレーションする必要があるのか？

‍The different ML pipelines have different orchestration requirements.
**異なるMLパイプラインには異なるorchestration requirements(要件)があります**。
Batch feature and inference pipelines need to be orchestrated and training pipelines can also be orchestrated:
batch特徴量パイプラインと推論パイプラインはオーケストレーションする必要があり、学習パイプラインもオーケストレーションすることができます。(FTI pipelineのブログでも、学習パイプラインはオーケストレーション不要かもね、みたいなこと書いてあったな...!:thinking:)

- both batch feature pipelines and batch inference pipelines are operational pipelines that are typically either scheduled to run at a well-defined cadence or run when data arrives and is ready for processing as features;
  バッチ特徴量パイプラインとバッチ推論パイプラインの両方は、通常、明確に定義された周期で実行されるようにスケジュールされるか、データが到着し、フィーチャとして処理する準備ができたときに実行される運用パイプラインである；

- training pipelines are not necessarily operational pipelines but can still be orchestrated - they can be run on-demand when a new model is needed, for example, because the existing one has been marked as stale, or they can run periodically to keep models up-to-date,
  トレーニングパイプラインは必ずしも運用パイプラインではないが、オーケストレーションすることができる。例えば、既存のモデルが古いとマークされたために新しいモデルが必要になったときにオンデマンドで実行することもできるし、モデルを最新の状態に保つために定期的に実行することもできる。(モデルの品質が低下してると判断されたら、自動で学習が走る、みたいな感じかな??)

Online inference and streaming ML pipelines do not need to be orchestrated:
オンライン推論とストリーミングMLパイプラインはオーケストレーションする必要がない:

- online inference pipelines are run as part of a service: either the model serving infrastructure or embedded in the ML-enabled application itself,
  オンライン推論パイプラインは、サービスの一部として実行される: オンライン推論パイプラインはサービスの一部として実行されます. (基本的にサーバーを常に起動させておく感じだから不要ってこと??)

  (推論サーバのインスタンスの台数増やすとか、そういう役割はorchestratorには含まれないのかな??:thinking:)

- streaming feature pipelines and streaming inference pipelines are run 24x7 and do not need to be orchestrated.
  ストリーミング・フィーチャー・パイプラインとストリーミング推論パイプラインは**24時間365日稼働**しており、オーケストレーションの必要はない。

## What are examples of orchestration tools for ML pipelines?

MLパイプライン用のオーケストレーション・ツールにはどのようなものがありますか？

A good orchestrator will:
優れたオーケストレーターはそうする：

- identify if errors occur and alert the pipeline owner,
  エラーの発生を特定し、パイプラインの所有者に警告する、

- be easy to debug in case of error,
  エラー発生時のデバッグが容易である、

- enabled failed runs to be easily re-run without any side-effects (idempotent),
  失敗した実行は、副作用なしに簡単に再実行できるようになった（idempotent）、

- and pipeline runs should scale to handle any data input size by scaling the amount of resources needed for that run.
  とパイプラインの実行は、その実行に必要なリソースの量をスケーリングすることによって、どのようなデータ入力サイズにも対応できるようにスケーリングされるべきである。

Examples of tools and frameworks used for ML pipeline orchestration include Apache Airflow, Flyte, Kubeflow, Azure Data Factory, and AWS Step Functions.
MLパイプラインのオーケストレーションに使われるツールやフレームワークの例としては、Apache Airflow、Flyte、Kubeflow、Azure Data Factory、AWS Step Functionsなどがある。
These tools provide a range of features, such as workflow scheduling, monitoring, fault tolerance, and version control, that can help orchestrate ML pipelines.
これらのツールは、ワークフローのスケジューリング、モニタリング、fault tolerance、バージョン管理などの機能を提供し、MLパイプラインのオーケストレーションを支援することができる。
(fault tolerance=障害許容性。システムが障害やエラーが発生した場合でも、中断することなく動作を継続する能力。具体的には、エラーハンドリングや自動recovery、冗長化などが含まれる。)
Simpler cron-based scheduling is available from platforms like Github Actions and Modal that are useful when prototyping.
Github ActionsやModalのようなプラットフォームからは、よりシンプルなcronベースのスケジューリングが利用でき、プロトタイピングの際に便利です。
(cron-basedって?? = UNIX系OSで使用される`cron`というプログラムを使って、定期的に実行するジョブをスケジューリングする方法のこと。)

Does this content look outdated? If you are interested in helping us maintain this, feel free to contact us.
このコンテンツは古く見えますか？このコンテンツのメンテナンスにご興味のある方は、お気軽にご連絡ください。
