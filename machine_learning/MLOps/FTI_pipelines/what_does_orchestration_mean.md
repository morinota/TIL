## link

https://www.hopsworks.ai/dictionary/orchestration#:~:text=Orchestration%20of%20ML%20pipelines%20refers,of%20the%20different%20ML%20pipelines.

# Orchestration

What does the orchestration of ML pipelines mean?
‍The orchestration of ML pipelines is crucial to making ML pipelines run without human intervention, and run reliably, even in the event of hardware or software errors.

Orchestration of ML pipelines refers to the process of automating the execution of the feature/training/inference pipeline. Ideally, a single orchestrator tool should manage the execution of the different ML pipelines.

Which ML pipelines need to be orchestrated?
‍The different ML pipelines have different orchestration requirements. Batch feature and inference pipelines need to be orchestrated and training pipelines can also be orchestrated:

both batch feature pipelines and batch inference pipelines are operational pipelines that are typically either scheduled to run at a well-defined cadence or run when data arrives and is ready for processing as features;
training pipelines are not necessarily operational pipelines but can still be orchestrated - they can be run on-demand when a new model is needed, for example, because the existing one has been marked as stale, or they can run periodically to keep models up-to-date,
Online inference and streaming ML pipelines do not need to be orchestrated:

online inference pipelines are run as part of a service: either the model serving infrastructure or embedded in the ML-enabled application itself,
streaming feature pipelines and streaming inference pipelines are run 24x7 and do not need to be orchestrated.
What are examples of orchestration tools for ML pipelines?
A good orchestrator will:

identify if errors occur and alert the pipeline owner,
be easy to debug in case of error,
enabled failed runs to be easily re-run without any side-effects (idempotent),
and pipeline runs should scale to handle any data input size by scaling the amount of resources needed for that run.
Examples of tools and frameworks used for ML pipeline orchestration include Apache Airflow, Flyte, Kubeflow, Azure Data Factory, and AWS Step Functions. These tools provide a range of features, such as workflow scheduling, monitoring, fault tolerance, and version control, that can help orchestrate ML pipelines. Simpler cron-based scheduling is available from platforms like Github Actions and Modal that are useful when prototyping.

Does this content look outdated? If you are interested in helping us maintain this, feel free to contact us.
