## refs

- https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/

# Process Amazon Redshift data and schedule a training pipeline with Amazon SageMaker Processing and Amazon SageMaker Pipelines

Customers in many different domains tend to work with multiple sources for their data: object-based storage like Amazon Simple Storage Service (Amazon S3), relational databases like Amazon Relational Database Service (Amazon RDS), or data warehouses like Amazon Redshift. Machine learning (ML) practitioners are often driven to work with objects and files instead of databases and tables from the different frameworks they work with. They also prefer local copies of such files in order to reduce the latency of accessing them.

Nevertheless, ML engineers and data scientists might be required to directly extract data from data warehouses with SQL-like queries to obtain the datasets that they can use for training their models.

In this post, we use the Amazon SageMaker Processing API to run a query against an Amazon Redshift cluster, create CSV files, and perform distributed processing. As an extra step, we also train a simple model to predict the total sales for new events, and build a pipeline with Amazon SageMaker Pipelines to schedule it.

## Prerequisites

This post uses the sample data that is available when creating a Free Tier cluster in Amazon Redshift. As a prerequisite, you should create your cluster and attach to it an AWS Identity and Access Management (IAM) role with the correct permissions. For instructions on creating the cluster with the sample dataset, see Using a sample dataset. For instructions on associating the role with the cluster, see Authorizing access to the Amazon Redshift Data API.

You can then use your IDE of choice to open the notebooks. This content has been developed and tested using SageMaker Studio on a ml.t3.medium instance. For more information about using Studio, refer to the following resources:

Onboard to Amazon SageMaker Domain
Clone a Git Repository in SageMaker Studio
Change an Instance Type

## Define the query

Now that your Amazon Redshift cluster is up and running, and loaded with the sample dataset, we can define the query to extract data from our cluster. According to the documentation for the sample database, this application helps analysts track sales activity for the fictional TICKIT website, where users buy and sell tickets online for sporting events, shows, and concerts. In particular, analysts can identify ticket movement over time, success rates for sellers, and the best-selling events, venues, and seasons.

Analysts may be tasked to solve a very common ML problem: predict the number of tickets sold given the characteristics of an event. Because we have two fact tables and five dimensions in our sample database, we have some data that we can work with. For the sake of this example, we try to use information from the venue in which the event takes place as well as its date. The SQL query looks like the following:

```sql
SELECT sum(s.qtysold) AS total_sold, e.venueid, e.catid, d.caldate, d.holiday
from sales s, event e, date d
WHERE s.eventid = e.eventid and e.dateid = d.dateid
GROUP BY e.venueid, e.catid, d.caldate, d.holiday
```

We can run this query in the query editor to test the outcomes and change it to include additional information if needed.

## Extract the data from Amazon Redshift and process it with SageMaker Processing

Now that we’re happy with our query, we need to make it part of our training pipeline.

A typical training pipeline consists of three phases:

Preprocessing – This phase reads the raw dataset and transforms it into a format that matches the input required by the model for its training
Training – This phase reads the processed dataset and uses it to train the model
Model registration – In this phase, we save the model for later usage

Our first task is to use a SageMaker Processing job to load the dataset from Amazon Redshift, preprocess it, and store it to Amazon S3 for the training model to pick up. SageMaker Processing allows us to directly read data from different resources, including Amazon S3, Amazon Athena, and Amazon Redshift. SageMaker Processing allows us to configure access to the cluster by providing the cluster and database information, and use our previously defined SQL query as part of a RedshiftDatasetDefinition. We use the SageMaker Python SDK to create this object, and you can check the definition and the parameters needed on the GitHub page. See the following code:

```python
from sagemaker.dataset_definition.inputs import RedshiftDatasetDefinition

rdd = RedshiftDatasetDefinition(
    cluster_id="THE-NAME-OF-YOUR-CLUSTER",
    database="THE-NAME-OF-YOUR-DATABASE",
    db_user="YOUR-DB-USERNAME",
    query_string="THE-SQL-QUERY-FROM-THE-PREVIOUS-STEP",
    cluster_role_arn="THE-IAM-ROLE-ASSOCIATED-TO-YOUR-CLUSTER",
    output_format="CSV",
    output_s3_uri="WHERE-IN-S3-YOU-WANT-TO-STORE-YOUR-DATA"
)
```

Then, you can define the DatasetDefinition. This object is responsible for defining how SageMaker Processing uses the dataset loaded from Amazon Redshift:

```python
from sagemaker.dataset_definition.inputs import DatasetDefinition

dd = DatasetDefinition(
    data_distribution_type='ShardedByS3Key', # This tells SM Processing to shard the data across instances
    local_path='/opt/ml/processing/input/data/', # Where SM Processing will save the data in the container
    redshift_dataset_definition=rdd # Our ResdhiftDataset
)
```

Finally, you can use this object as input of your processor of choice. For this post, we wrote a very simple scikit-learn script that cleans the dataset, performs some transformations, and splits the dataset for training and testing. You can check the code in the file processing.py.

We can now instantiate the SKLearnProcessor object, where we define the framework version that we plan on using, the amount and type of instances that we spin up as part of our processing cluster, and the execution role that contains the right permissions. Then, we can pass the parameter dataset_definition as the input of the run() method. This method accepts our processing.py script as the code to run, given some inputs (namely, our RedshiftDatasetDefinition), generates some outputs (a train and a test dataset), and stores both to Amazon S3. We run this operation synchronously thanks to the parameter wait=True:

```python
from sagemaker.sklearn import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker import get_execution_role

skp = SKLearnProcessor(
    framework_version='0.23-1',
    role=get_execution_role(),
    instance_type='ml.m5.large',
    instance_count=1
)
skp.run(
    code='processing/processing.py',
    inputs=[ProcessingInput(
        dataset_definition=dd,
        destination='/opt/ml/processing/input/data/',
        s3_data_distribution_type='ShardedByS3Key'
    )],
    outputs = [
        ProcessingOutput(
            output_name="train",
            source="/opt/ml/processing/train"
        ),
        ProcessingOutput(
            output_name="test",
            source="/opt/ml/processing/test"
        ),
    ],
    wait=True
)
```

With the outputs created by the processing job, we can move to the training step, by means of the sagemaker.sklearn.SKLearn() Estimator:

```python
from sagemaker.sklearn import SKLearn

s = SKLearn(
    entry_point='training/script.py',
    framework_version='0.23-1',
    instance_type='ml.m5.large',
    instance_count=1,
    role=get_execution_role()
)
s.fit({
    'train':skp.latest_job.outputs[0].destination,
    'test':skp.latest_job.outputs[1].destination
})
```

To learn more about the SageMaker Training API and Scikit-learn Estimator, see Using Scikit-learn with the SageMaker Python SDK.

## Define a training pipeline

Now that we have proven that we can read data from Amazon Redshift, preprocess it, and use it to train a model, we can define a pipeline that reproduces these steps, and schedule it to run. To do so, we use SageMaker Pipelines. Pipelines is the first purpose-built, easy-to-use continuous integration and continuous delivery (CI/CD) service for ML. With Pipelines, you can create, automate, and manage end-to-end ML workflows at scale.

Pipelines are composed of steps. These steps define the actions that the pipeline takes, and the relationships between steps using properties. We already know that our pipelines are composed of three steps:

A processing phase, defined in ProcessingStep
A training phase, defined in TrainingStep
A registration phase, defined in CreateModelStep
Furthermore, to make the pipeline definition dynamic, Pipelines allows us to define parameters, which are values that we can provide at runtime when the pipeline starts.

The following code is a snippet that shows the definition of a processing step. The step requires the definition of a processor, which is very similar to the one defined previously during the preprocessing discovery phase, but this time using the parameters of Pipelines. The others parameters, code, inputs, and outputs are the same as we have defined previously:

Very similarly, we can define the training step, but we use the outputs from the processing step as inputs:

Finally, let’s add the model step, which registers the model to SageMaker for later use (for real-time endpoints and batch transform):

With all the pipeline steps now defined, we can define the pipeline itself as a pipeline object comprising a series of those steps. ParallelStep and Condition steps also are possible. Then we can update and insert (upsert) the definition to Pipelines with the .upsert() command:

After we upsert the definition, we can start the pipeline with the pipeline object’s start() method, and wait for the end of its run:

After the pipeline starts running, we can view the run on the SageMaker console. In the navigation pane, under Components and registries, choose Pipelines. Choose the Redshift2Pipeline pipeline, and then choose the specific run to see its progress. You can choose each step to see additional details such as the output, logs, and additional information. Typically, this pipeline should take about 10 minutes to complete.

## Conclusions

In this post, we created a SageMaker pipeline that reads data from Amazon Redshift natively without requiring additional configuration or services, processed it via SageMaker Processing, and trained a scikit-learn model. We can now do the following:

Schedule the pipeline to run with Amazon EventBridge rules (see Automating Amazon SageMaker with Amazon EventBridge)
Create a new scheduled pipeline for inference with the TransformStep
Use the model to update an existing real-time endpoint manually or as part of a SageMaker project
If you want additional notebooks to play with, check out the following:

Use the Amazon Redshift Data API from within a SageMaker notebook: extra-content/data-api-discovery.ipynb
Integrate the Amazon Redshift Data API in an AWS Lambda function to have more granular control, and add this step to a SageMaker pipeline: extra-content/pipeline.ipynb
