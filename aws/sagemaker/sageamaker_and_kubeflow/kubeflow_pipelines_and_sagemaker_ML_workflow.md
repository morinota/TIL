## refs

https://medium.com/@ashwin.mudhol/kubeflow-pipelines-and-sagemaker-ml-workflow-f077679c4b66

# Kubeflow pipelines and SageMaker ML workflow

This post shows how to build your first Kubeflow pipeline with Amazon Sagemaker components using the Kubeflow Pipelines SDK.

## Introduction:

What is kubeflow pipelines?
Kubeflow Pipelines (KFP) is a platform for building and deploying portable and scalable machine learning (ML) workflows using Docker containers.

Below diagram explains a simple basic pipeline:

Check out how to write your pipeline:
https://www.kubeflow.org/docs/components/pipelines/v2/hello-world/

What Is Amazon SageMaker?
Amazon SageMaker is a fully managed machine learning service. With SageMaker, data scientists and developers can quickly and easily build and train machine learning models, and then directly deploy them into a production-ready hosted environment.
https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html

Now where does Amazon’s SageMaker and Kubeflow both come in the together??

Suppose you want to experiment on the dataset you have prepared and quickly get the model trained and test it. You would need to request a GPU resource to MLOps/Infra team and shut it down once the training is completed.
ML ops teams need to manage a Kubernetes cluster with CPU and GPU instances, and keep its utilization high at all times to provide the best return on investment.

All this quickly adds the overhead to both Data Scientists/ML developer and MLOps teams.

With Amazon SageMaker Components for Kubeflow Pipelines, you can take advantage of powerful Amazon SageMaker features such as fully managed services, including data labeling, large-scale hyperparameter tuning and distributed training jobs easily.

## Tutorial:

Lets see how we can write kubeflow pipelines with sagemaker components.

For this we will take a basic example of MNIST dataset.
We will look at:

Data Preparation.
Model Training in SageMaker.
Model Deployment in SageMaker.
Before we build the Pipeline, lets walk-through the IAM’s dark forest for setting up the sagemaker access.

Run the following commands from your cloud9 console with aws cli is configured:

Create a IAM user for this task.

Create an access key and export them as env variable.

Create an IAM execution role for Sagemaker and S3 so that the job can assume this role in order to perform Sagemaker and S3 actions. Make a note of this role as you will need it during pipeline creation step.

Create Kubernetes secrets aws-secret with Sagemaker and S3 policies. Please make sure to create `aws-secret` in your kubeflow user namespace.

Let’s assign sagemaker:InvokeEndpoint permission to Worker node IAM role.

Now we are ready to run the pipeline.
Go Ahead and download the example notebook from here.

Our pipeline will look like below once completed.

Initialize your kfp_client and create an experiment

Get the Xgboost Model uri and initialise the constants.

3. Download the Sample MNIST data and Upload it to S3 Bucket.

4. Data Set Preprocessing (Splitting into Train, validation and test set).

5. Download Sagemaker components yaml and initialize.
