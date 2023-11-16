## link

https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines

## title

From MLOps to ML Systems with Feature/Training/Inference Pipelines

The Mental Map for MLOps to align your Data-ML-Product Teams

## abstract

Maps help us navigate the world, and communicate ideas, helping us get faster to our destination. Somewhere along the way, MLOps got lost in promoting “waterfall software architecture” maps for ML Systems that include a kitchen sink of requirements. Existing approaches to MLOps prevent teams from following DevOps principles of starting with a small working system and iteratively improving it. In this article, we present a new mental map for ML Systems as three independent ML pipelines: feature pipelines, training pipelines, and inference pipelines that share a common storage layer for the ML artifacts they produce and consume (features, models). In contrast to existing MLOps architectures, we provide a unified architecture that describes both batch ML systems and real-time ML systems. This makes it easier for developers to move to/from batch and real-time systems, and provides clear interfaces between the ML pipelines, enabling easier collaboration between the data, ML, and product teams that work together to develop and operate ML systems. Compared to existing MLOps architectures, the feature/training/inference pipeline architecture helps you get faster to a minimal working ML system that can be iteratively improved, while following best practices for automated testing, versioning, and monitoring. There are now hundreds of ML systems that have been built by the community based on our architecture, showing that building and shipping ML systems is easier if you follow a mental map that starts with building pipelines rather than starting by building ML infrastructure.

# Introduction

“It's impressive how far you can go with contemporary tools like @modal_labs, @huggingface, and @hopsworks! In 2017, having a shared pipeline for training and prediction data that updated automatically and made models available as a UI and an API was a groundbreaking stack at Uber. Now, it's a standard part of a well-done student project.” Charles Frye, Full Stack Deep Learning course leader.

In a course I gave at KTH in 2022/23, students developed a full ML system in only 2 weeks that solved a prediction problem for a novel non-static data source of their choice. As Charles suggests in the above quote, leveraging ML infrastructure makes it easier to build ML systems. You can write a Python program that scrapes data from the Internet and, with a few annotations, runs on a daily schedule with Modal. The program can write the features it computes as DataFrames to Hopsworks Feature Store. From there, a notebook can be used to train a model that is saved in Hopsworks (or any model registry). And, finally, a third Python program uses the trained model to make predictions with new inference data (for example, the data scraped today) read from the Feature Store, and displays the predictions in a nice UI or Dashboard (e.g., written in the Streamlit or Taipy). Some examples of prediction problems were predicting air quality, water levels, snow depth, football scores, electricity demand, and sentiment for posts.

But in my course analysis, the conclusion I drew was that the key reason why students could go from zero to a working ML system in less than 2 weeks was not just the new frameworks. It was, more importantly, the clear mental map of what they needed to do (see Figure 1):

build a feature pipeline to continually create features from your novel data source, save those features as a DataFrame to Hopsworks Feature Store;
write a training pipeline that reads training data from the Feature Store, trains your model and saves the trained model in the model registry,
write a batch inference pipeline or online inference pipeline that downloads the trained model, then takes new feature data, either from the feature store or computes it from user requests, and makes predictions consumed by the ML-enabled product (often a simple UI written in Python using Streamlit or Gradio).
After the students have built their first MVP (Minimum Viable Product), they could add automated unit tests for features, data validation tests, and versioning for their features and models. That is, they could easily follow best practices for MLOps.

However, even with recent advances in MLOps tooling, many teams are failing in getting models to production. According to Gartner, between 2020 and 2022, companies only increased the percentage of models that make it from prototype to production from 53% to 54%. Tooling will only get you so far, if you don’t have good processes for how to get there. As such, this starts with a brief, idiosyncratic historical overview of ML systems and MLOps, a critique of current “best practices”, and then we present our FTI (feature/training/inference) pipeline architecture for ML systems and its advantages over current approaches.

# Pre-MLOps - Move fast and ship it

In the early days of ML Systems, it quickly became common knowledge that building ML systems was much more than just training a model.

The diagram in Figure 3 spread fast and wide and the message was clear to Data Scientists - building ML systems is hard and much more than just training a model.

In the era before MLOps practices merged, the first generation of ML systems many different architecture patterns were proposed to help build batch and real-time ML systems.

Broadly speaking, there are two types of ML systems: batch ML systems and real-time ML systems. An example of a batch ML system would be Spotify weekly. It produces predictions for every user once per week on what songs to recommend to each user. The results are stored in a key-value store, and when you login to Spotify, it downloads the predictions to your client and shows you the recommendations. An example of a real-time ML system would be TikTok. Every click or swipe you make is used to compute features in near real-time about your user history and context (e.g., what’s trending) that are, in turn, used to personalize recommendations for upcoming videos.

In figure 4, you can see a quick-and-dirty batch ML system. This anti-pattern is for a production batch ML system that runs on a schedule to make predictions that are consumed by some prediction consumer, such as a dashboard or an operational system. The pattern solves one problem - it ensures consistent features for training and inference by including training and inference in the same program. You run the program with a boolean flag that decides whether it runs in TRAIN or INFERENCE mode. However, features created here are not easily reused in other models and there is very little modularity - if data volumes increase beyond what your Python program can process, you can’t easily switch to PySpark.

In figure 5, you can see an operational ML system that receives requests from clients and responds with predictions in real-time. This is a very different architecture from our previous batch ML system, which makes it challenging for developers to move from batch to real-time systems. There are also new challenges here. Now, you need two separate systems - an offline training pipeline, and an online model serving service. You can no longer ensure consistent features between training and serving by having a single monolithic program. One solution is to version the feature creation source code and ensure both training and serving use the same version. In this architecture, the features in the online inference pipeline are computed using data provided by the request - the models have no access to history or context, all state used to create features should come in the request. An example of such a system would be a LLM chatbot. The user provides a query and the LLM provides a response, with the online inference pipeline tokenizing the input text.

In our first real-time ML system, the online inference pipeline was stateless - it had no access to historical data or context data. Figure 6 shows the architecture of a real-time ML System with the feature store providing history and context, enabling richer feature vectors for models. The feature store provides low-latency access to pre-computed features (historical and contextual information) by the online inference pipeline looking features up with entity IDs (userID, sessionID, productID, etc) provided by the client at request-time.

At this point, we have introduced 3 different architectures for building production ML systems. The challenge for ML platform teams has been how to easily communicate these architectural patterns to the data/ML/ops/product teams who collaborate to build production ML systems.

# The Kitchen-Sink Mental Maps for MLOps

In 2020, the term MLOps came to be adopted as the set of patterns and processes that ML platforms teams should use to productionize ML systems. MLOps was inspired by the DevOps movement which brought software engineers closer to production by ensuring that they automate and test the deployment of their software in production environments. Wouldn’t it be great if we could do the same for ML systems? However, ML systems are more complex than classical software products - they have to manage both the code used to build them and the data used for training and inference. Our nascent MLOps Community badly needed some guidance on best practices and processes for teams - we needed a map to build ML systems.

There is a long history of bad maps leading people astray.

Personally, since a very young age, I have had an unreasonable dislike for Mercator Projection maps (see figure 7).

The first MLOps maps for building ML systems have similar deficiencies to Mercator Maps - they try to project a view of ML systems that doesn’t reflect the reality of building a ML system. The maps are a kitchen sink of requirements collected by consultants from all the different stakeholders and thrown unthinkingly into one huge diagram.

As you can, Google started by asking the operations teams - who said they needed separate dev and prod environments. The data teams wanted clean data. The ML teams want hyperparameter tuning and models to be validated. The product teams got forgotten in this MLOps map.

Databricks, however, were not to be outdone. Google forgot a staging environment! But where is the mythical ML pipeline here? There are no names for the pipelines, no easy way to build your first ML system in a couple of weeks. The barrier to entry is too high - only a very few people have the software engineering, operations, and data science knowledge to navigate these maps. For other mortals - Data Scientists, Data Engineers, ML Engineers - the maps might as well be a riddle for finding buried treasure.

Let’s take a step back and examine the problem of making ML systems from first principles. We will skip static datasets where you only make one-off predictions on a static dataset - this is not a ML System.

Firstly, a ML System uses a trained ML model to make predictions on new data to solve a “prediction problem” of interest. That new data and the historical data for training is fed by pipelines. Pipelines continually feed data to models to enable ML Systems to make predictions on new data, and to collect training data. Pipelines also enable automation - to retrain models, to monitor model performance, to log data for debugging.

Batch pipelines enable both batch ML Systems, such as dashboards, and operational ML systems, such as Spotify weekly, where recommendations for songs are updated once per week and consumed by the user when they login to Spotify. Streaming feature pipelines and features computed at request-time (on-demand features) enable interactive ML systems that are updated in real-time, enabling systems such as personalized recommendations or search.

# Unified Architecture for ML Systems as Feature/Training/Inference Pipelines

There is, however, an easier mental map that can help you build ML systems. This architectural pattern has been used to build hundreds of ML systems by ordinary developers (here, here, here, and here). The pattern is as follows: a ML system consists of three independently developed and operated ML pipelines:

a feature pipeline that takes as input raw data that it transforms into features (and labels)
a training pipeline that takes as input features (and labels) and outputs a trained model, and
an inference pipeline that takes new feature data and a trained model and makes predictions.
In this FTI (feature, training, inference) architecture, there is no single ML pipeline. The confusion about what the ML pipeline does (does it feature engineer and train models or also do inference or just one of those?) disappears. The FTI map is the same for both batch ML systems and real-time ML systems.

The feature pipeline can be a batch program or a streaming program. The training pipeline can output anything from a simple XGBoost model to a fine-tuned large-language model (LLM), trained on many GPUs. Finally, the inference pipeline can be a batch program that produces a batch of predictions to an online service that takes requests from clients and returns predictions in real-time.

One major advantage of FTI pipelines is it is an open architecture. You can use Python, Java or SQL. If you need to do feature engineering on large volumes of data, you can use Spark or DBT or Beam. Training will typically be in Python using some ML framework, and batch inference could be in Python or Spark, depending on your data volumes. Online inference pipelines are, however, nearly always in Python as models are typically training with Python.

In figure 13, we can see the value of pluggable feature pipelines. For a given feature ingestion problem, you can easily pick the best framework, depending on the size of the data that will be ingested in a pipeline run and the freshness requirements for the feature data created - use streaming or on-demand features if you need very fresh (near real-time) feature data.

The FTI pipelines are also modular and there is a clear interface between the different stages. Each FTI pipeline can be operated independently. Compared to the monolithic ML pipeline, different teams can now be responsible for developing and operating each pipeline. The impact of this is that for orchestration, for example, one team could use one orchestrator for a feature pipeline and a different team could use a different orchestrator for the batch inference pipeline. Alternatively, you could use the same orchestrator for the three different FTI pipelines for a batch ML system. Some examples of orchestrators that can be used in ML systems include general-purpose, feature-rich orchestrators, such as Airflow, or lightweight orchestrators, such as Modal, or managed orchestrators offered by feature platforms.

Some of our FTI pipelines, however, will not need orchestration. Training pipelines can be run on-demand, when a new model is needed. Streaming feature pipelines and online inference pipelines run continuously as services, and do not require orchestration. Flink, Spark Streaming, and Beam are run as services on platforms such as Kubernetes, Databricks, or Hopsworks. Online inference pipelines are deployed with their model on model serving platforms, such as KServe (Hopsworks), Seldon, Sagemaker, and Ray. The main takeaway here is that the ML pipelines are modular with clear interfaces, enabling you to choose the best technology for running your FTI pipelines.

Finally, we show how we connect our FTI pipelines together with a stateful layer to store the ML artifacts - features, training/test data, and models. Feature pipelines store their output, features, as DataFrames in the feature store. Incremental tables store each new update/append/delete as separate commits using a table format (we use Apache Hudi in Hopsworks). Training pipelines read point-in-time consistent snapshots of training data from Hopsworks to train models with and output the trained model to a model registry. You can include your favorite model registry here, but we are biased towards Hopsworks’ model registry. Batch inference pipelines also read point-in-time consistent snapshots of inference data from the feature store, and produce predictions by applying the model to the inference data. Online inference pipelines compute on-demand features and read precomputed features from the feature store to build feature vectors that are used to make predictions in response to requests by online applications/services.

## A Zoomable Map

As with any good map, the FTI pipelines architecture hides complexity at a high level, but allows you to zoom in on any part of the map to discover important implementation details. Here, we enumerate some of the important questions on implementing the different pipelines that can be handled internally within the team implementing the pipeline. In contrast, the MLOps 1.0 mental maps leaked all concepts across all teams making it hard for teams to know where their responsibilities started and ended as part of a very complex bigger picture.

## Feature Pipelines

Feature pipelines read data from data sources, compute features and ingest them to the feature store. Some of the questions that need to be answered for any given feature pipeline include:

Is the feature pipeline batch or streaming?
Are feature ingestions incremental or full-load operations?
What framework/language is used to implement the feature pipeline?
Is there data validation performed on the feature data before ingestion?
What orchestrator is used to schedule the feature pipeline?
If some features have already been computed by an upstream system (e.g., a data warehouse), how do you prevent duplicating that data, and only read those features when creating training or batch inference data?

## Training Pipelines

In training pipelines some of the details that can be discovered on double-clicking are:

What framework/language is used to implement the training pipeline?
What experiment tracking platform is used?
Is the training pipeline run on a schedule (if so, what orchestrator is used), or is it run on-demand (e.g., in response to performance degradation of a model)?
Are GPUs needed for training? If yes, how are they allocated to training pipelines?
What feature encoding/scaling is done on which features? (We typically store feature data unencoded in the feature store, so that it can be used for EDA (exploratory data analysis). Encoding/scaling is performed in a consistent manner training and inference pipelines). Examples of feature encoding techniques include scikit-learn pipelines or declarative transformations in feature views (Hopsworks).
What model evaluation and validation process is used?
What model registry is used to store the trained models?

## Inference Pipelines

Inference pipelines are as diverse as the applications they AI-enable. In inference pipelines, some of the details that can be discovered on double-clicking are:

What is the prediction consumer - is it a dashboard, online application - and how does it consume predictions?
Is it a batch or online inference pipeline?
What type of feature encoding/scaling is done on which features?
For batch inference pipelines: what framework/language is used? What orchestrator is used to run it on a schedule? What sink is used to consume the predictions produced?
For online inference pipelines: what model serving server is used to host the deployed model? How is the online inference pipeline implemented - as a predictor class or with a separate transformer step? Are GPUs needed for inference? Is there a SLA (service-level agreements) for how long it takes to respond to prediction requests?

# What are the fundamental principles of MLOps?

The existing mantra is that MLOps is about automating continuous integration (CI), continuous delivery (CD), and continuous training (CT) for ML systems. But that is too abstract for many developers. MLOps is really about continual development of ML-enabled products that evolve over time. The available input data (features) changes over time, the target you are trying to predict changes over time. You need to make changes to the source code, and you want to ensure that any changes you make do not break your ML system or degrade its performance. And you want to accelerate the time required to make those changes and test before those changes are automatically deployed to production.

So, from our perspective, a more pithy definition of MLOps that enables ML Systems to be safely evolved over time is that it requires, at a minimum, automated testing, versioning, and monitoring of ML artifacts. MLOps is about automated testing, versioning, and monitoring of ML artifacts.

In figure 16, we can see that more levels of testing are needed in ML systems than in traditional software systems. Small bugs in data or code can easily cause a ML model to make incorrect predictions. From a testing perspective, if web applications are propeller-driven airplanes, ML systems are jet-engines. It takes significant engineering effort to test and validate ML Systems to make them safe!

At a high level, we need to test both the source-code and data for ML Systems. The features created by feature pipelines can have their logic tested with unit tests and their input data checked with data validation tests (e.g., Great Expectations). The models need to be tested for performance, but also for a lack of bias against known groups of vulnerable users. Finally, at the top of the pyramid, ML-Systems need to test their performance with A/B tests before they can switch to use a new model.

When a ML system runs in production, you can also add feature monitoring and model monitoring support to it to try and identify and correct problems in their performance. For example, monitoring can identify issues such as drift in feature values or a changing prediction target for a ML model.

Finally, we need to version ML artifacts so that the operators of ML systems can safely update and rollback versions of deployed models. System support for the push-button upgrade/downgrade of models is one of the holy grails of MLOps. But models need features to make predictions, so model versions are connected to feature versions and models and features need to be upgraded/downgraded synchronously. Luckily, you don’t need a year in rotation as a Google SRE to easily upgrade/downgrade models - platform support for versioned ML artifacts should make this a straightforward ML system maintenance operation.

# Example ML Systems built with FTI Pipelines

Here is a sample of some of the open-source ML systems available built on the FTI architecture. They have been built mostly by practitioners and students.

## Batch ML Systems

Electricity Demand Prediction (452 github stars)
NBA Game Prediction (152 github stars)
Premier league football score predictions (101 github stars)
Churn prediction (113 github stars)

## Real-Time ML System

Online Credit Card Fraud (113 github stars)
Crypto Price Prediction (65 github stars)
Loan application approval (113 github stars)

# Summary

This blog post introduces a new mental map for MLOps, the FTI pipeline architecture. The architecture has enabled hundreds of developers to build maintainable ML Systems in a short period of time. In our experience, compared to MLOps 1.0, the architecture leads to reduced cognitive load when designing and describing a ML system. In enterprise settings, the architecture enables better communication across teams by providing clear interfaces between teams, leading to better collaboration and higher quality ML systems, faster. The architecture hides complexity at a high level, but you can easily drill down to the different feature/training/inference components to examine the details. Our hope is that the FTI pipeline architecture can help more teams work better together and get more models into production, quicker, accelerating the transformation of society by AI.

## Resources

The serverless ML community (with >2k discord members in August 2023) dedicated to building ML systems using the FTI pipeline architecture.
There is a serverless ML course, given by Jim Dowling and Hopsworks, that introduces the FTI pipeline architecture and how to build ML systems using free serverless technologies.
