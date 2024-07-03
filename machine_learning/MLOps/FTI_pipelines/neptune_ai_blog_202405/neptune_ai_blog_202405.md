## refs:

https://neptune.ai/blog/building-ml-systems-with-feature-store

# How to Build Machine Learning Systems With a Feature Store

Training and evaluating models is just the first step toward machine-learning success. To generate value from your model, it should make many predictions, and these predictions should improve a product or lead to better decisions. For this, we have to build an entire machine-learning system around our models that manages their lifecycle, feeds properly prepared data into them, and sends their output to downstream systems.

This can seem daunting. Luckily, we have tried and trusted tools and architectural patterns that provide a blueprint for reliable ML systems. In this article, I’ll introduce you to a unified architecture for ML systems built around the idea of FTI pipelines and a feature store as the central component. We’ll see how this architecture applies to different classes of ML systems, discuss MLOps and testing aspects, and look at some example implementations.

## Understanding machine learning pipelines

Machine learning (ML) pipelines are a key component of ML systems. But what is an ML pipeline? Ask four ML engineers, and you will likely get four different answers. Some will say that an ML pipeline trains models, another says it makes predictions, and another says it does both in a single run. None of them are wrong, but you can already tell that just saying “ML pipeline” can easily lead to miscommunication. We’ll have to be more precise.

An ML system needs to transform the data into features, train models, and make predictions. Each of these tasks can be performed by a pipeline: A program that runs on some schedule with well-defined inputs and outputs.

In this article, we define a machine learning system as consisting of three ML pipelines:

A feature pipeline that transforms its input data into features/labels as output,
a training pipeline that transforms its input features/labels into trained models as output,
and an inference pipeline that uses these trained models to transform its input features into predictions as output.
Collectively, these three ML pipelines are known as the FTI pipelines: feature, training, and inference.

## Machine learning systems with feature stores

Machine learning (ML) systems manage the data transformations, model training, and predictions made on ML models. They transform data into features, train ML models using features and labels, and use trained models to make predictions.

As you’re building an ML system, you’ll find that matching the outputs of your feature pipeline with the inputs of the training and inference pipelines becomes a challenge. Keeping track of how exactly the incoming data (the feature pipeline’s input) has to be transformed and ensuring that each model receives the features precisely how it saw them during training is one of the hardest parts of architecting ML systems.

This is where feature stores come in. A feature store is a data platform that supports the creation and use of feature data throughout the lifecycle of an ML model, from creating features that can be reused across many models to model training to model inference (making predictions).

A feature store typically comprises a feature repository, a feature serving layer, and a metadata store. The feature repository is essentially a database storing pre-computed and versioned features. The serving layer facilitates real-time access to these features during model training and inference. It can also transform incoming data on the fly. The metadata store manages the metadata associated with each feature, such as its origin and transformations. Together, these components form a specialized infrastructure to streamline feature data management in ML workflows.

Many ML systems benefit from having the feature store as their data platform, including:

Interactive ML systems receive a user request and respond with a prediction. An interactive ML system either downloads a model and calls it directly or calls a model hosted in a model-serving infrastructure. The inputs to the model – the features – can be computed on-demand from request parameters or be precomputed and read at runtime. Both scenarios are supported by feature stores.
Batch ML systems run on a schedule or are triggered when a new batch of data arrives. They download a model from a model registry, compute predictions, and store the results to be later consumed by AI-enabled applications. Batch ML systems can retrieve a new batch of inference data from a feature store as a batch of precomputed features created by the feature pipelines.
Stream-processing ML systems typically use a model downloaded from a model registry to make predictions on streaming data. Features are typically computed on-demand but may also be enriched with precomputed features retrieved from a feature store. (It is also possible for stream-processing systems to use an externally hosted model, although less common due to the higher latency it introduces).
There are ML systems, such as embedded systems in self-driving cars, that do not use feature stores as they require real-time safety-critical decisions and cannot wait for a response from an external database.

## A unified architecture for ML systems

One of the challenges in building machine-learning systems is architecting the system. As you’ll likely have experienced yourself, there is no one right way that fits every situation. But there are some common patterns and best practices, which we’ll explore in this section.

Figure 1. Overview of the high-level architecture of an ML system centered around a feature store. The feature pipeline retrieves data from outside sources, transforms them, and loads them into the feature store. The training pipeline fetches data from the feature store for model training, sends training metadata to an experiment tracker for later analysis, and places the resulting model in the model registry. The inference pipeline loads a model from the model registry. It uses the feature store to retrieve properly transformed features, which it feeds to the model to make predictions that it exposes to downstream applications. In most ML systems, the feature and inference pipeline are always active, while the training pipeline is only invoked occasionally.
The feature pipeline ingests data. In the most straightforward case, you’ll load complete datasets at once, reading them from CSV or Parquet files. But often, you’ll want to load data incrementally, adding new samples to datasets that already exist in the system. When you have to comply with GDPR or similar regulations, you’ll also need the ability to delete samples.

The feature store is the stateful layer to manage your features (and training labels) for your ML system. It stores the features created in feature pipelines and provides APIs to retrieve them.

For model training, it’s paramount that the training pipeline can easily load snapshots of training data from tables of features (feature groups). In particular, a feature store should provide point-in-time consistent snapshots of feature data so that your models do not suffer from future data leakage.

For batch and interactive ML systems where features are pre-computed, the feature store provides batch and point APIs enabling the inference pipeline to retrieve a batch of precomputed features in a DataFrame or a row of precomputed features in a feature vector.

In real-time ML systems, some features may be based on information that only becomes available right when a prediction is requested. These features are computed on-demand using feature functions. A feature store helps ensure that the features calculated online match those used in the training pipeline.

The model registry connects your training and inference pipeline. It stores the trained models created by training pipelines and provides an API for inference pipelines to download the trained models.

This high-level design around a feature store and a model registry as central components provides a unified architecture for batch, interactive, and streaming ML systems. It also enables developers to concentrate on building the ML pipelines rather than the ML infrastructure.

The following table shows the different technologies that can be used to build the FTI pipelines, depending on the type of machine-learning system you want to develop:

Table 1. Reference table for which technologies to use for your FTI pipelines for each ML system.

## MLOps and FTI pipelines testing

Once you have built an ML system, you have to operate, maintain, and update it. Typically, these activities are collectively called “MLOps.”

One of the core principles of MLOps is automation. Many ML engineers dream of having a big green button and a big red button. Press the green button to upgrade and the red button to roll back an upgrade. Achieving this dream requires versioning of artifacts – model versions are connected to specific feature versions – and comprehensive testing to increase the user’s confidence that the new model will work well.

Figure 2. Testing machine learning systems is a hierarchical process spanning data, features, models, and ML-enabled applications. The testing pyramid shows that a reliable ML app requires reliable models, which in turn require reliable features derived from the raw data.
Aside from testing a pipeline’s implementation prior to its deployment, testing has to happen while operating the ML system:

In feature pipelines, we validate the incoming data and the data written to the feature store.
In training pipelines, we validate the model performance and validate that the model is free from bias and other undesirable behavior.
In inference pipelines, we can use A/B testing to validate the models. Instead of deploying a new model directly, we can deploy it in “shadow mode,” evaluating its performance compared to the old model. When we’re happy enough with the new version, we can replace the previous version with the new version.
Versioning of features and models enables the online upgrade of ML systems. A specific model version is linked to a particular feature version. Thus, during operation, the inference pipeline can retrieve precisely the kind of features it was trained on.

When the model is upgraded to a new version, the inference pipeline will simultaneously start requesting the associated new feature versions. If there is a problem after upgrading, you can immediately go back to using the previous model and feature versions. (This is the “big red button” I mentioned above).

Figure 3 shows an example of how all of this comes together.

Figure 3. Example of an ML system that uses model and feature versioning to facilitate seamless and reliable upgrades. An air quality model has been upgraded from version 1 to version 2. The airquality model uses weather and airquality features from the feature store. As part of the upgrade from version 1 to version 2, we needed a new version of the air quality features (air_quality_v2). Upgrading a model involves synchronizing the upgrade of both the model and the features.

## Examples of ML systems with feature stores and FTI pipelines

To truly understand an abstract concept, I always find it best to look at some concrete examples.

In Table 1 below, I’ve compiled a list of different ML systems that follow the unified architecture. Most of them were built by people who took my free online serverless machine learning course or my Scalable Machine Learning and Deep Learning course at KTH Royal Institute of Technology in Stockholm.

The ML systems mostly follow the same structure. They have a non-static data source (new data will arrive at some cadence), train an ML model to solve a prediction problem, and have a user interface that allows users to consume the predictions. Some ML systems use deep learning, while others utilize more classical models like decision trees or XGBoost.

They are all serverless systems, i.e., they don’t require any computational resources when no pipeline is actively running. All of them are written in Python. The systems run their pipelines on GitHub Actions or with Cloud Composer, the managed Apache Airflow offering on the Google Cloud Platform. They store their feature data in Hopsworks’ free serverless platform, app.hopsworks.ai.

## How to get started with FTI pipelines and feature stores

To learn more about designing ML systems using FTI pipelines and feature stores, check out my free open-source course at serverless-ml.org. It covers the principles and practices of creating an ML system (both batch and interactive) in Python using free serverless services. Python is the only prerequisite for the course, and your first ML system will consist of just three different Python scripts. We also have a discord channel dedicated to serverless machine learning with over 2,500 members where you can ask questions and discuss what you learned with fellow participants.

The course uses Hopsworks as the serverless feature store, GitHub Actions to schedule batch Python programs, and HuggingFace Spaces to host a UI for your machine-learning systems. You can use Neptune as your experiment tracking system and model registry for the course, just like in the NBA Score Predictions example I shared above.

I’m also working on a book about building machine-learning systems with a feature store. It will be published by O’Reilly in the summer of 2025. You can already read the first few chapters on our website.

If you make the leap from training models, to building ML systems, please do share what you’ve built on the discord channel with all the other builders – when we learn together, we learn faster and better.
