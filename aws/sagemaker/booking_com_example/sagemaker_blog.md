## link

- https://aws.amazon.com/jp/blogs/machine-learning/how-booking-com-modernized-its-ml-experimentation-framework-with-amazon-sagemaker/

# How Booking.com modernized its ML experimentation framework with Amazon SageMaker

This post is co-written with Kostia Kofman and Jenny Tokar from Booking.com.

As a global leader in the online travel industry, Booking.com is always seeking innovative ways to enhance its services and provide customers with tailored and seamless experiences. The Ranking team at Booking.com plays a pivotal role in ensuring that the search and recommendation algorithms are optimized to deliver the best results for their users.

Sharing in-house resources with other internal teams, the Ranking team machine learning (ML) scientists often encountered long wait times to access resources for model training and experimentation – challenging their ability to rapidly experiment and innovate. Recognizing the need for a modernized ML infrastructure, the Ranking team embarked on a journey to use the power of Amazon SageMaker to build, train, and deploy ML models at scale.

Booking.com collaborated with AWS Professional Services to build a solution to accelerate the time-to-market for improved ML models through the following improvements:

Reduced wait times for resources for training and experimentation
Integration of essential ML capabilities such as hyperparameter tuning
A reduced development cycle for ML models
Reduced wait times would mean that the team could quickly iterate and experiment with models, gaining insights at a much faster pace. Using SageMaker on-demand available instances allowed for a tenfold wait time reduction. Essential ML capabilities such as hyperparameter tuning and model explainability were lacking on premises. The team’s modernization journey introduced these features through Amazon SageMaker Automatic Model Tuning and Amazon SageMaker Clarify. Finally, the team’s aspiration was to receive immediate feedback on each change made in the code, reducing the feedback loop from minutes to an instant, and thereby reducing the development cycle for ML models.

In this post, we delve into the journey undertaken by the Ranking team at Booking.com as they harnessed the capabilities of SageMaker to modernize their ML experimentation framework. By doing so, they not only overcame their existing challenges, but also improved their search experience, ultimately benefiting millions of travelers worldwide.

## Approach to modernization

The Ranking team consists of several ML scientists who each need to develop and test their own model offline. When a model is deemed successful according to the offline evaluation, it can be moved to production A/B testing. If it shows online improvement, it can be deployed to all the users.

The goal of this project was to create a user-friendly environment for ML scientists to easily run customizable Amazon SageMaker Model Building Pipelines to test their hypotheses without the need to code long and complicated modules.

One of the several challenges faced was adapting the existing on-premises pipeline solution for use on AWS. The solution involved two key components:

Modifying and extending existing code – The first part of our solution involved the modification and extension of our existing code to make it compatible with AWS infrastructure. This was crucial in ensuring a smooth transition from on-premises to cloud-based processing.
Client package development – A client package was developed that acts as a wrapper around SageMaker APIs and the previously existing code. This package combines the two, enabling ML scientists to easily configure and deploy ML pipelines without coding.

## SageMaker pipeline configuration

Customizability is key to the model building pipeline, and it was achieved through config.ini, an extensive configuration file. This file serves as the control center for all inputs and behaviors of the pipeline.

Available configurations inside config.ini include:

Pipeline details – The practitioner can define the pipeline’s name, specify which steps should run, determine where outputs should be stored in Amazon Simple Storage Service (Amazon S3), and select which datasets to use
AWS account details – You can decide which Region the pipeline should run in and which role should be used
Step-specific configuration – For each step in the pipeline, you can specify details such as the number and type of instances to use, along with relevant parameters
The following code shows an example configuration file:

config.ini is a version-controlled file managed by Git, representing the minimal configuration required for a successful training pipeline run. During development, local configuration files that are not version-controlled can be utilized. These local configuration files only need to contain settings relevant to a specific run, introducing flexibility without complexity. The pipeline creation client is designed to handle multiple configuration files, with the latest one taking precedence over previous settings.

## SageMaker pipeline steps

The pipeline is divided into the following steps:

Train and test data preparation – Terabytes of raw data are copied to an S3 bucket, processed using AWS Glue jobs for Spark processing, resulting in data structured and formatted for compatibility.
Train – The training step uses the TensorFlow estimator for SageMaker training jobs. Training occurs in a distributed manner using Horovod, and the resulting model artifact is stored in Amazon S3. For hyperparameter tuning, a hyperparameter optimization (HPO) job can be initiated, selecting the best model based on the objective metric.
Predict – In this step, a SageMaker Processing job uses the stored model artifact to make predictions. This process runs in parallel on available machines, and the prediction results are stored in Amazon S3.
Evaluate – A PySpark processing job evaluates the model using a custom Spark script. The evaluation report is then stored in Amazon S3.
Condition – After evaluation, a decision is made regarding the model’s quality. This decision is based on a condition metric defined in the configuration file. If the evaluation is positive, the model is registered as approved; otherwise, it’s registered as rejected. In both cases, the evaluation and explainability report, if generated, are recorded in the model registry.
Package model for inference – Using a processing job, if the evaluation results are positive, the model is packaged, stored in Amazon S3, and made ready for upload to the internal ML portal.
Explain – SageMaker Clarify generates an explainability report.
Two distinct repositories are used. The first repository contains the definition and build code for the ML pipeline, and the second repository contains the code that runs inside each step, such as processing, training, prediction, and evaluation. This dual-repository approach allows for greater modularity, and enables science and engineering teams to iterate independently on ML code and ML pipeline components.

The following diagram illustrates the solution workflow.

## Automatic model tuning

Training ML models requires an iterative approach of multiple training experiments to build a robust and performant final model for business use. The ML scientists have to select the appropriate model type, build the correct input datasets, and adjust the set of hyperparameters that control the model learning process during training.

The selection of appropriate values for hyperparameters for the model training process can significantly influence the final performance of the model. However, there is no unique or defined way to determine which values are appropriate for a specific use case. Most of the time, ML scientists will need to run multiple training jobs with slightly different sets of hyperparameters, observe the model training metrics, and then try to select more promising values for the next iteration. This process of tuning model performance is also known as hyperparameter optimization (HPO), and can at times require hundreds of experiments.

The Ranking team used to perform HPO manually in their on-premises environment because they could only launch a very limited number of training jobs in parallel. Therefore, they had to run HPO sequentially, test and select different combinations of hyperparameter values manually, and regularly monitor progress. This prolonged the model development and tuning process and limited the overall number of HPO experiments that could run in a feasible amount of time.

With the move to AWS, the Ranking team was able to use the automatic model tuning (AMT) feature of SageMaker. AMT enables Ranking ML scientists to automatically launch hundreds of training jobs within hyperparameter ranges of interest to find the best performing version of the final model according to the chosen metric. The Ranking team is now able choose between four different automatic tuning strategies for their hyperparameter selection:

Grid search – AMT will expect all hyperparameters to be categorical values, and it will launch training jobs for each distinct categorical combination, exploring the entire hyperparameter space.
Random search – AMT will randomly select hyperparameter values combinations within provided ranges. Because there is no dependency between different training jobs and parameter value selection, multiple parallel training jobs can be launched with this method, speeding up the optimal parameter selection process.
Bayesian optimization – AMT uses Bayesian optimization implementation to guess the best set of hyperparameter values, treating it as a regression problem. It will consider previously tested hyperparameter combinations and its impact on the model training jobs with the new parameter selection, optimizing for smarter parameter selection with fewer experiments, but it will also launch training jobs only sequentially to always be able to learn from previous trainings.
Hyperband – AMT will use intermediate and final results of the training jobs it’s running to dynamically reallocate resources towards training jobs with hyperparameter configurations that show more promising results while automatically stopping those that underperform.
AMT on SageMaker enabled the Ranking team to reduce the time spent on the hyperparameter tuning process for their model development by enabling them for the first time to run multiple parallel experiments, use automatic tuning strategies, and perform double-digit training job runs within days, something that wasn’t feasible on premises.

## Model explainability with SageMaker Clarify

Model explainability enables ML practitioners to understand the nature and behavior of their ML models by providing valuable insights for feature engineering and selection decisions, which in turn improves the quality of the model predictions. The Ranking team wanted to evaluate their explainability insights in two ways: understand how feature inputs affect model outputs across their entire dataset (global interpretability), and also be able to discover input feature influence for a specific model prediction on a data point of interest (local interpretability). With this data, Ranking ML scientists can make informed decisions on how to further improve their model performance and account for the challenging prediction results that the model would occasionally provide.

SageMaker Clarify enables you to generate model explainability reports using Shapley Additive exPlanations (SHAP) when training your models on SageMaker, supporting both global and local model interpretability. In addition to model explainability reports, SageMaker Clarify supports running analyses for pre-training bias metrics, post-training bias metrics, and partial dependence plots. The job will be run as a SageMaker Processing job within the AWS account and it integrates directly with the SageMaker pipelines.

The global interpretability report will be automatically generated in the job output and displayed in the Amazon SageMaker Studio environment as part of the training experiment run. If this model is then registered in SageMaker model registry, the report will be additionally linked to the model artifact. Using both of these options, the Ranking team was able to easily track back different model versions and their behavioral changes.

To explore input feature impact on a single prediction (local interpretability values), the Ranking team enabled the parameter save_local_shap_values in the SageMaker Clarify jobs and was able to load them from the S3 bucket for further analyses in the Jupyter notebooks in SageMaker Studio.

The preceding images show an example of how a model explainability would look like for an arbitrary ML model.

## Training optimization

The rise of deep learning (DL) has led to ML becoming increasingly reliant on computational power and vast amounts of data. ML practitioners commonly face the hurdle of efficiently using resources when training these complex models. When you run training on large compute clusters, various challenges arise in optimizing resource utilization, including issues like I/O bottlenecks, kernel launch delays, memory constraints, and underutilized resources. If the configuration of the training job is not fine-tuned for efficiency, these obstacles can result in suboptimal hardware usage, prolonged training durations, or even incomplete training runs. These factors increase project costs and delay timelines.

Profiling of CPU and GPU usage helps understand these inefficiencies, determine the hardware resource consumption (time and memory) of the various TensorFlow operations in your model, resolve performance bottlenecks, and, ultimately, make the model run faster.

Ranking team used the framework profiling feature of Amazon SageMaker Debugger (now deprecated in favor of Amazon SageMaker Profiler) to optimize these training jobs. This allows you to track all activities on CPUs and GPUs, such as CPU and GPU utilizations, kernel runs on GPUs, kernel launches on CPUs, sync operations, memory operations across GPUs, latencies between kernel launches and corresponding runs, and data transfer between CPUs and GPUs.

Ranking team also used the TensorFlow Profiler feature of TensorBoard, which further helped profile the TensorFlow model training. SageMaker is now further integrated with TensorBoard and brings the visualization tools of TensorBoard to SageMaker, integrated with SageMaker training and domains. TensorBoard allows you to perform model debugging tasks using the TensorBoard visualization plugins.

With the help of these two tools, Ranking team optimized the their TensorFlow model and were able to identify bottlenecks and reduce the average training step time from 350 milliseconds to 140 milliseconds on CPU and from 170 milliseconds to 70 milliseconds on GPU, speedups of 60% and 59%, respectively.

## Business outcomes

The migration efforts centered around enhancing availability, scalability, and elasticity, which collectively brought the ML environment towards a new level of operational excellence, exemplified by the increased model training frequency and decreased failures, optimized training times, and advanced ML capabilities.

Model training frequency and failures
The number of monthly model training jobs increased fivefold, leading to significantly more frequent model optimizations. Furthermore, the new ML environment led to a reduction in the failure rate of pipeline runs, dropping from approximately 50% to 20%. The failed job processing time decreased drastically, from over an hour on average to a negligible 5 seconds. This has strongly increased operational efficiency and decreased resource wastage.

### Optimized training time

The migration brought with it efficiency increases through SageMaker-based GPU training. This shift decreased model training time to a fifth of its previous duration. Previously, the training processes for deep learning models consumed around 60 hours on CPU; this was streamlined to approximately 12 hours on GPU. This improvement not only saves time but also expedites the development cycle, enabling faster iterations and model improvements.

### Advanced ML capabilities

Central to the migration’s success is the use of the SageMaker feature set, encompassing hyperparameter tuning and model explainability. Furthermore, the migration allowed for seamless experiment tracking using Amazon SageMaker Experiments, enabling more insightful and productive experimentation.

Most importantly, the new ML experimentation environment supported the successful development of a new model that is now in production. This model is deep learning rather than tree-based and has introduced noticeable improvements in online model performance.

## Conclusion

This post provided an overview of the AWS Professional Services and Booking.com collaboration that resulted in the implementation of a scalable ML framework and successfully reduced the time-to-market of ML models of their Ranking team.

The Ranking team at Booking.com learned that migrating to the cloud and SageMaker has proved beneficial, and that adapting machine learning operations (MLOps) practices allows their ML engineers and scientists to focus on their craft and increase development velocity. The team is sharing the learnings and work done with the entire ML community at Booking.com, through talks and dedicated sessions with ML practitioners where they share the code and capabilities. We hope this post can serve as another way to share the knowledge.

AWS Professional Services is ready to help your team develop scalable and production-ready ML in AWS. For more information, see AWS Professional Services or reach out through your account manager to get in touch.
