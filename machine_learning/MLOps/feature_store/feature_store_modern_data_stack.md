## link

https://www.moderndatastack.xyz/category/feature-store

# What is a Feature Store?

Feature stores orchestrate the data processes that power ML models. ML models have unique data access requirements to facilitate both model training and production inference. The Feature Store serves an abstraction between your raw data, and the interfaces required by the model. Feature Stores create this abstraction by enabling data scientists to automate the processing of feature values, generate training datasets, and serve features online with production-grade service levels.

# Why do I need a Feature Store?

ML models will only ever be as good as the data that we feed to them. To deploy a model to production, data teams have to build production data pipelines to transform and serve features online. These production ML pipelines are different from traditional analytics pipelines. They need to process both historical data for training, and fresh data for online serving. They must ensure training/serving parity, and provide point-in-time correctness. Features must be served online at high scale and low latency to support production workloads. These challenges are difficult to tackle with traditional data orchestration tools, and can often add weeks or months to the delivery time of new ML projects.

Feature Stores solve these problems by enabling data teams to:

- Build a library of features collaboratively using standard feature definitions
- Generate accurate training datasets with just a few lines of code
- Deploy features to production instantly using DevOps-like engineering best practices
- Share, discover and re-use features across an organizatio

# Common Components of Feature Stores

The Feature Store is a relatively new concept, and so the exact definition is still evolving. The key components of a feature store commonly include:

- Feature Registry: Features are defined as version-controlled code. The feature registry contains a central catalog of all the feature definitions and feature metadata. It allows data scientists to search, discover, and collaborate on new features.
- Transformations: Feature stores orchestrate data pipelines to transform raw data into feature values. They can consume batch, streaming, and real-time data to combine historical context with the freshest information available.
- Storage: Feature values are organized in feature storage. Feature stores provide both online storage for low-latency retrieval at scale, and offline storage to curate historical datasets cost-effectively.
- Feature Serving: Feature stores provide an API endpoint to serve online feature values at low latency.
- Monitoring: Feature stores monitor both data quality and operational metrics. They can validate data for correctness and detect data drift. They also monitor essential metrics related to feature storage (capacity, staleness) and feature serving (latency, throughput).

# What to Look for When Choosing a Feature Store

Users now have plenty of feature store offerings to choose from. AWS, Databricks, Google Cloud, Tecton, and Feast (open source) all come to mind. However, not all feature stores are created equal. The main things a user should pay attention to when choosing an offering are:

- Ecosystem and integrations: Some feature stores are tightly integrated with a very specific ecosystem. The AWS SageMaker feature store, for example, is designed to work well with the SageMaker ecosystem. Other feature stores, like Feast, are not tied to a specific ecosystem and work across clouds. Are you fully bought into a specific ecosystem or looking for a more flexible solution?
- Delivery model: Some feature stores, like Tecton, are offered as fully-managed services. Other feature stores, like Feast, need to be self-deployed and managed. Do you prefer the flexibility of self-managed solutions or the ease of fully-managed services?
- Data infrastructure: Most feature stores are designed to orchestrate data flows on top of existing infrastructure. The Databricks feature store, for example, is designed to operate on Delta Lake. Some feature stores include their own data infrastructure including object storage and key-value stores. Do you prefer to re-use existing data infrastructure, or deploy new data infrastructure from scratch?
- Scope of feature management: The majority of feature stores are focused on solving the serving problem. They provide a consistent way to store and serve feature values, but those feature values have to be processed outside of the feature store. Other feature stores, like Tecton, manage the complete lifecycle of features - including feature transformations and automated pipelines. The latter is particularly useful if you’re doing complex transformations like streaming or real-time features.

Want to learn more? You can check out Tecton’s ‘What is a Feature Store’ blog, or compare some of the leading offerings at the MLOps Community’s great feature store evaluation page here.
