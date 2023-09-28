## link

https://mlops.community/mlops-maturity-assessment/

# MLOps Maturity Assessment

As more and more companies rely on machine learning to run their daily operations, it’s becoming important to adopt MLOps best practices. However, it can be hard to find structured information on what those best practices actually are and how a company can become more mature in terms of MLOps if they decide to start on that journey.

Microsoft’s MLOps maturity model or Google’s definition of MLOps levels is a good start, but they don’t necessarily offer actionable insights on how a project can go from being MLOps immature to achieving 100% MLOps maturity. That’s why we decided to create a questionnaire that can help evaluate MLOps maturity on a project level. Our questionnaire covers a wide range of MLOps aspects, making it a valuable resource for teams looking to improve their MLOps practices.

1. Documentation
2. Traceability & Reproducibility
3. Code quality
4. Monitoring & Support
5. Data transformation pipelines & Feature store
6. Model explainability
7. A/B testing & Feedback loop

We believe that a machine learning project can be considered MLOps mature if all statements in sections 1–4 (documentation, traceability & reproducibility, code quality, monitoring & support) can be answered with “yes”. This is the bare minimum required to deploy a machine learning project reliably in production. Sections 5–7 go beyond basic MLOps maturity, and it is possible to work on its implementation while some of the statements in sections 1–4 haven’t been covered. However, we encourage everyone to prioritize the basics before moving on to advanced MLOps practices.

This questionnaire makes MLOps actionable by clearly highlighting areas for improvement: If some of the statements are answered with a “no,” it’s a clear indicator of what needs to be addressed to improve your MLOps maturity.

# Documentation

## Project Documentation

1. Business goals and KPIs of an ML project are documented and kept up to date.
2. Overview of all team members involved in a machine learning project including their responsibilities are created and kept up to date.
3. ML model risk evaluation is created, documented, and kept up to date.

## ML model documentation

1. Steps of gathering, analyzing, and cleaning data including motivation for each step should be documented.
2. Data definition (what features are used in an ML model and what these features mean) is documented.
3. Choice of machine learning model is documented and justified.

## Technical documentation

1. For real time inference use cases, API is documented: request & response structure and definition, data types.
2. Software architecture design is documented and kept up to date.

# Traceability and reproducibility

## Infrastructure traceability and reproducibility

1. Infrastructure is defined as code, later referenced as IaC.
2. IaC is stored in a version control system.
3. Pull request process is used to create changes in IaC.
4. When pull request is merged, changes will be automatically applied to corresponding environments through a CD pipeline.
5. Only CD pipelines can deploy changes, individual developers do not have rights to deploy infrastructure.
6. ML projects should have at least two environments (preproduction and production) which are exact copies of each other.
7. All environments related to a ML project should have (read and/or write) access to production data (data should be the same at any moment of time).

## ML code traceability and reproducibility

1. Code for gathering, analyzing, and cleaning data should be stored in a version control system.
2. ML model code is stored in the version control system, together with data preparation code and API code (if applicable).
3. Pull requests (PR) are used to make changes in any code related to an ML project.
4. When PR is merged, changes will be automatically applied to corresponding environments through a CD pipeline.
5. Environment is defined as code and is reproducible.
6. ML model code should not require changes to run in different environments. The processes of deployment of an ML model to all environments should be the same.
7. For any given machine learning model run/deployment in any environment it is possible to look up unambiguously: 1. corresponding code/ commit on git, 2. infrastructure used for training and serving, 3. environment used for training and serving, 4. ML model artifacts, 5. what data was used to train the model.
8. ML model retraining strategy is present and motivated.
9. Roll-back strategy is present to be able to revert to the previous ML model version.

# Code Quality

## Infrastructure code quality requirements

1. CI pipeline that includes configuration files validation and running automated tests is triggered at pull request creation.
2. Other team members (e.g., developers / security specialists) must review and approve changes before merging a pull request.

## ML model code quality requirements

1. Pre-commit hooks are implemented to ensure that code follows the code quality guidelines before it is pushed to a version control system.
2. ML model code contains tests for all steps in an ML process (data processing, ML model training, API deployment).
3. CI pipeline that includes running automated tests is triggered at pull request creation.
4. Other team members (for example, developers/ security specialists) must approve changes before merging a pull request.
5. For real time inference use cases, strategy should be present to perform API load and stress tests regularly and make sure API meets latency requirements.
6. For real time inference use cases, authentication and networking should follow security guidelines.
7. ML model code should be documented (documentation as code).
8. Release notes should be created every time there is a new release of an ML model code.

# Monitoring & Support

## Infrastructure monitoring requirements

1. Tracking of infrastructure costs is set up; cost estimation is done regularly for an ML project.
2. Health of infrastructure resources is monitored. Alerting is set up in case problems occur.

## Application monitoring requirements

1. For real-time inference use cases, all API requests and responses should be logged, API response time, response codes, and health status should be monitored.
2. For batch use cases, continuity of delivery to the target system should be monitored.

## KPI & model performance monitoring requirements

1. Offline evaluation metrics (for example, F1 score computed on historical data for classification tasks) is stored and monitored.
2. Feedback loop is used to evaluate and constantly monitor KPIs that were defined together with the business stakeholders for this ML project.

## Data drift & Outliers monitoring

1. Distributions of important model features are recalculated on a regular basis, alerts are created if a significant change in distribution that affects the target is detected.
2. Outlier detection is set up, cases when machine learning models are returning predictions with low certainty are regularly reviewed.

# Data transformation pipelines & Feature store

1. Features are pre-computed in a Feature store and/or imported as code shareable across projects.
2. The offline training data and online prediction data is transformed with the same code.
3. All the model features are sourced from the feature store or external libraries.
4. Data scientist can add features to the feature store with a PR.
5. Feature dependency is automatically managed by the feature store.
6. The feature store keeps track of the feature usage per model.
7. The feature configuration is separated from its code.

# Model Explainability

1. The AI system is capable of providing an explanation for its outputs, with evidence to support the explanation.
2. The AI system explanation is meaningful if a user of the system can understand the explanation.
3. The AI system is able to clearly describe how it arrived at its decision outputs.
4. The AI system operates within its knowledge limits and knows when it is operating outside of those limits.

# A/B testing & feedback loop

1. The inputs and outputs of the model are stored automatically.
2. A/B testing is performed regularly.
3. When doing A/B testing, it can be guaranteed that the same customer will get predictions based on the same version of the model during the whole experiment.
