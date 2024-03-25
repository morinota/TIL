## refs

- https://docs.aws.amazon.com/sagemaker/latest/dg/kubernetes-sagemaker-components-for-kubeflow-pipelines.html

# SageMaker Components for Kubeflow Pipelines

This document outlines how to use SageMaker Components for Kubeflow Pipelines. With these pipeline components, you can create and monitor native SageMaker training, tuning, endpoint deployment, and batch transform jobs from your Kubeflow Pipelines. By running Kubeflow Pipeline jobs on SageMaker, you move data processing and training jobs from the Kubernetes cluster to SageMaker's machine learning-optimized managed service. This document assumes prior knowledge of Kubernetes and Kubeflow.

Contents
What are Kubeflow Pipelines?
What are Kubeflow Pipeline components?
Why use SageMaker Components for Kubeflow Pipelines?
SageMaker Components for Kubeflow Pipelines versions
List of SageMaker Components for Kubeflow Pipelines
IAM permissions
Converting pipelines to use SageMaker
Install Kubeflow Pipelines
Use SageMaker components

## What are Kubeflow Pipelines?

Kubeflow Pipelines (KFP) is a platform for building and deploying portable, scalable machine learning (ML) workflows based on Docker containers. The Kubeflow Pipelines platform consists of the following:

A user interface (UI) for managing and tracking experiments, jobs, and runs.

An engine (Argo) for scheduling multi-step ML workflows.

An SDK for defining and manipulating pipelines and components.

Notebooks for interacting with the system using the SDK.

A pipeline is a description of an ML workflow expressed as a directed acyclic graph. Every step in the workflow is expressed as a Kubeflow Pipeline component, which is a AWS SDK for Python (Boto3) module.

For more information on Kubeflow Pipelines, see the Kubeflow Pipelines documentation.

## What are Kubeflow Pipeline components?

A Kubeflow Pipeline component is a set of code used to execute one step of a Kubeflow pipeline. Components are represented by a Python module built into a Docker image. When the pipeline runs, the component's container is instantiated on one of the worker nodes on the Kubernetes cluster running Kubeflow, and your logic is executed. Pipeline components can read outputs from the previous components and create outputs that the next component in the pipeline can consume. These components make it fast and easy to write pipelines for experimentation and production environments without having to interact with the underlying Kubernetes infrastructure.

You can use SageMaker Components in your Kubeflow pipeline. Rather than encapsulating your logic in a custom container, you simply load the components and describe your pipeline using the Kubeflow Pipelines SDK. When the pipeline runs, your instructions are translated into a SageMaker job or deployment. The workload then runs on the fully managed infrastructure of SageMaker.

## Why use SageMaker Components for Kubeflow Pipelines?

SageMaker Components for Kubeflow Pipelines offer an alternative to launching your compute-intensive jobs from SageMaker. The components integrate SageMaker with the portability and orchestration of Kubeflow Pipelines. Using the SageMaker Components for Kubeflow Pipelines, you can create and monitor your SageMaker resources as part of a Kubeflow Pipelines workflow. Each of the jobs in your pipelines runs on SageMaker instead of the local Kubernetes cluster allowing you to take advantage of key SageMaker features such as data labeling, large-scale hyperparameter tuning and distributed training jobs, or one-click secure and scalable model deployment. The job parameters, status, logs, and outputs from SageMaker are still accessible from the Kubeflow Pipelines UI.

The SageMaker components integrate key SageMaker features into your ML workflows from preparing data, to building, training, and deploying ML models. You can create a Kubeflow Pipeline built entirely using these components, or integrate individual components into your workflow as needed. The components are available in one or two versions. Each version of a component leverages a different backend. For more information on those versions, see SageMaker Components for Kubeflow Pipelines versions.

There is no additional charge for using SageMaker Components for Kubeflow Pipelines. You incur charges for any SageMaker resources you use through these components.

## SageMaker Components for Kubeflow Pipelines versions

SageMaker Components for Kubeflow Pipelines come in two versions. Each version leverages a different backend to create and manage resources on SageMaker.

The SageMaker Components for Kubeflow Pipelines version 1 (v1.x or below) use Boto3 (AWS SDK for Python (Boto3)) as backend.

The version 2 (v2.0.0-alpha2 and above) of SageMaker Components for Kubeflow Pipelines use SageMaker Operator for Kubernetes (ACK).

AWS introduced ACK to facilitate a Kubernetes-native way of managing AWS Cloud resources. ACK includes a set of AWS service-specific controllers, one of which is the SageMaker controller. The SageMaker controller makes it easier for machine learning developers and data scientists using Kubernetes as their control plane to train, tune, and deploy machine learning (ML) models in SageMaker. For more information, see SageMaker Operators for Kubernetes

Both versions of the SageMaker Components for Kubeflow Pipelines are supported. However, the version 2 provides some additional advantages. In particular, it offers:

A consistent experience to manage your SageMaker resources from any application; whether you are using Kubeflow pipelines, or Kubernetes CLI (kubectl) or other Kubeflow applications such as Notebooks.

The flexibility to manage and monitor your SageMaker resources outside of the Kubeflow pipeline workflow.

Zero setup time to use the SageMaker components if you deployed the full Kubeflow on AWS release since the SageMaker Operator is part of its deployment.

## List of SageMaker Components for Kubeflow Pipelines

The following is a list of all SageMaker Components for Kubeflow Pipelines and their available versions. Alternatively, you can find all SageMaker Components for Kubeflow Pipelines in GitHub.

## IAM permissions

Deploying Kubeflow Pipelines with SageMaker components requires the following three layers of authentication:

An IAM role granting your gateway node (which can be your local machine or a remote instance) access to the Amazon Elastic Kubernetes Service (Amazon EKS) cluster.

The user accessing the gateway node assumes this role to:

Create an Amazon EKS cluster and install KFP

Create IAM roles

Create Amazon S3 buckets for your sample input data

The role requires the following permissions:

CloudWatchLogsFullAccess

AWSCloudFormationFullAccess

IAMFullAccess

AmazonS3FullAccess

AmazonEC2FullAccess

AmazonEKSAdminPolicy (Create this policy using the schema from Amazon EKS Identity-Based Policy Examples)

A Kubernetes IAM execution role assumed by Kubernetes pipeline pods (kfp-example-pod-role) or the SageMaker Operator for Kubernetes controller pod to access SageMaker. This role is used to create and monitor SageMaker jobs from Kubernetes.

The role requires the following permission:

AmazonSageMakerFullAccess

You can limit permissions to the KFP and controller pods by creating and attaching your own custom policy.

A SageMaker IAM execution role assumed by SageMaker jobs to access AWS resources such as Amazon S3 or Amazon ECR (kfp-example-sagemaker-execution-role).

SageMaker jobs use this role to:

Access SageMaker resources

Input Data from Amazon S3

Store your output model to Amazon S3

The role requires the following permissions:

AmazonSageMakerFullAccess

AmazonS3FullAccess

## Converting pipelines to use SageMaker

You can convert an existing pipeline to use SageMaker by porting your generic Python processing containers and training containers. If you are using SageMaker for inference, you also need to attach IAM permissions to your cluster and convert an artifact to a model.
