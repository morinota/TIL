## refs:

- https://aws.amazon.com/jp/blogs/machine-learning/best-practices-and-design-patterns-for-building-machine-learning-workflows-with-amazon-sagemaker-pipelines/

# Best practices and design patterns for building machine learning workflows with Amazon SageMaker Pipelines

Amazon SageMaker Pipelines is a fully managed AWS service for building and orchestrating machine learning (ML) workflows. SageMaker Pipelines offers ML application developers the ability to orchestrate different steps of the ML workflow, including data loading, data transformation, training, tuning, and deployment. You can use SageMaker Pipelines to orchestrate ML jobs in SageMaker, and its integration with the larger AWS ecosystem also allows you to use resources like AWS Lambda functions, Amazon EMR jobs, and more. This enables you to build a customized and reproducible pipeline for specific requirements in your ML workflows.

In this post, we provide some best practices to maximize the value of SageMaker Pipelines and make the development experience seamless. We also discuss some common design scenarios and patterns when building SageMaker Pipelines and provide examples for addressing them.

## Best practices for SageMaker Pipelines

In this section, we discuss some best practices that can be followed while designing workflows using SageMaker Pipelines. Adopting them can improve the development process and streamline the operational management of SageMaker Pipelines.

### Use Pipeline Session for lazy loading of the pipeline

Pipeline Session enables lazy initialization of pipeline resources (the jobs are not started until pipeline runtime). The PipelineSession context inherits the SageMaker Session and implements convenient methods for interacting with other SageMaker entities and resources, such as training jobs, endpoints, input datasets in Amazon Simple Storage Service (Amazon S3), and so on. When defining SageMaker Pipelines, you should use PipelineSession over the regular SageMaker Session:

```python
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.sklearn.processing import SKLearnProcessor
role = sagemaker.get_execution_role()
pipeline_session = PipelineSession()
sklearn_processor = SKLearnProcessor(
    framework_version=’0.20.0’,
    instance_type=’ml.m5.xlarge’,
    instance_count=1,
    base_job_name="sklearn-abalone-process",
    role=role,
    sagemaker_session=pipeline_session,
)
```

### Run pipelines in local mode for cost-effective and quick iterations during development

You can run a pipeline in local mode using theLocalPipelineSession context. In this mode, the pipeline and jobs are run locally using resources on the local machine, instead of SageMaker managed resources. Local mode provides a cost-effective way to iterate on the pipeline code with a smaller subset of data. After the pipeline is tested locally, it can be scaled to run using the PipelineSession context.

```python
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.pipeline_context import LocalPipelineSession
local_pipeline_session = LocalPipelineSession()
role = sagemaker.get_execution_role()
sklearn_processor = SKLearnProcessor(
    framework_version=’0.20.0’,
    instance_type=’ml.m5.xlarge,
    instance_count=1,
    base_job_name="sklearn-abalone-process",
    role=role,
    sagemaker_session=local_pipeline_session,
)
```

### Manage a SageMaker pipeline through versioning

Versioning of artifacts and pipeline definitions is a common requirement in the development lifecycle. You can create multiple versions of the pipeline by naming pipeline objects with a unique prefix or suffix, the most common being a timestamp, as shown in the following code:

```python
from sagemaker.workflow.pipeline_context import PipelineSession
import time

current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
pipeline_name = "pipeline_" + current_time
pipeline_session = PipelineSession()
pipeline = Pipeline(
    name=pipeline_name,
    steps=[step_process, step_train, step_eval, step_cond],
    sagemaker_session=pipeline_session,
)
```

### Organize and track SageMaker pipeline runs by integrating with SageMaker Experiments

SageMaker Pipelines can be easily integrated with SageMaker Experiments for organizing and tracking pipeline runs. This is achieved by specifying PipelineExperimentConfig at the time of creating a pipeline object. With this configuration object, you can specify an experiment name and a trial name. The run details of a SageMaker pipeline get organized under the specified experiment and trial. If you don’t explicitly specify an experiment name, a pipeline name is used for the experiment name. Similarly, if you don’t explicitly specify a trial name, a pipeline run ID is used for the trial or run group name. See the following code:

```python
Pipeline(
    name="MyPipeline",
    parameters=[...],
    pipeline_experiment_config=PipelineExperimentConfig(
        experiment_name = ExecutionVariables.PIPELINE_NAME,
        trial_name = ExecutionVariables.PIPELINE_EXECUTION_ID
        ),
    steps=[...]
)
```

### Securely run SageMaker pipelines within a private VPC

To secure the ML workloads, it’s a best practice to deploy the jobs orchestrated by SageMaker Pipelines in a secure network configuration within a private VPC, private subnets, and security groups. To ensure and enforce the usage of this secure environment, you can implement the following AWS Identity and Access Management (IAM) policy for the SageMaker execution role (this is the role assumed by the pipeline during its run). You can also add the policy to run the jobs orchestrated by SageMaker Pipelines in network isolation mode.

```python
# IAM Policy to enforce execution within a private VPC

{

    "Action": [

        "sagemaker:CreateProcessingJob",
        "sagemaker:CreateTrainingJob",
        "sagemaker:CreateModel"
    ],

    "Resource": "*",
    "Effect": "Deny",
    "Condition": {
        "Null": {
            "sagemaker:VpcSubnets": "true"
        }
    }
}

# IAM Policy to enforce execution in network isolation mode
{

    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": [
                "sagemaker:Create*"
            ],
            "Resource": "*",
            "Condition": {
                "StringNotEqualsIfExists": {
                    "sagemaker:NetworkIsolation": "true"
                }
            }
        }
    ]
}
```

### Monitor the cost of pipeline runs using tags

Using SageMaker pipelines by itself is free; you pay for the compute and storage resources you spin up as part of the individual pipeline steps like processing, training, and batch inference. To aggregate the costs per pipeline run, you can include tags in every pipeline step that creates a resource. These tags can then be referenced in the cost explorer to filter and aggregate total pipeline run cost, as shown in the following example:

```python
sklearn_processor = SKLearnProcessor(
    framework_version=’0.20.0’,
    instance_type=’ml.m5.xlarge,
    instance_count=1,
    base_job_name="sklearn-abalone-process",
    role=role,
    tags=[{'Key':'pipeline-cost-tag', 'Value':'<<tag_parameter>>'}]
)

step_process = ProcessingStep(
    name="AbaloneProcess",
    processor=sklearn_processor,
    ...
)
```

From the cost explorer, you can now get the cost filtered by the tag:

```python
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': '2023-07-01',
        'End': '2023-07-15'
        },
    Metrics=['BLENDED_COST','USAGE_QUANTITY','UNBLENDED_COST'],
    Granularity='MONTHLY',
    Filter={
        'Dimensions': {
            'Key':'USAGE_TYPE',
            'Values': [
                ‘SageMaker:Pipeline’
            ]
        },
        'Tags': {
            'Key': 'keyName',
            'Values': [
                'keyValue',
                ]
        }
    }
)
```

## Design patterns for some common scenarios

In this section, we discuss design patterns for some common use cases with SageMaker Pipelines.

### Run a lightweight Python function using a Lambda step

Python functions are omnipresent in ML workflows; they are used in preprocessing, postprocessing, evaluation, and more. Lambda is a serverless compute service that lets you run code without provisioning or managing servers. With Lambda, you can run code in your preferred language that includes Python. You can use this to run custom Python code as part of your pipeline. A Lambda step enables you to run Lambda functions as part of your SageMaker pipeline. Start with the following code:

```python
%%writefile lambdafunc.py

import json

def lambda_handler(event, context):
    str1 = event["str1"]
    str2 = event["str2"]
    str3 = str1 + str2
    return {
        "str3": str3
    }
```

Create the Lambda function using the SageMaker Python SDK’s Lambda helper:

```python
from sagemaker.lambda_helper import Lambda

def create_lambda(function_name, script, handler):
    response = Lambda(
        function_name=function_name,
        execution_role_arn=role,
        script= script,
        handler=handler,
        timeout=600,
        memory_size=10240,
    ).upsert()

    function_arn = response['FunctionArn']
    return function_arn

fn_arn = create_Lambda("func", "lambdafunc.py", handler = "lambdafunc.lambda_handler")
```

Call the Lambda step:

```python
from sagemaker.lambda_helper import Lambda
from sagemaker.workflow.lambda_step import (
    LambdaStep,
    LambdaOutput,
    LambdaOutputTypeEnum
)

str3 = LambdaOutput(output_name="str3", output_type=LambdaOutputTypeEnum.String)

# Lambda Step
step_lambda1 = LambdaStep(
    name="LambdaStep1",
    lambda_func=Lambda(
        function_arn=fn_arn
    ),
    inputs={
        "str1": "Hello",
        "str2": " World"
    },
    outputs=[str3],
)
```

### Pass data between steps

Input data for a pipeline step is either an accessible data location or data generated by one of the previous steps in the pipeline. You can provide this information as a ProcessingInput parameter. Let’s look at a few scenarios of how you can use ProcessingInput.

Scenario 1: Pass the output (primitive data types) of a Lambda step to a processing step
Primitive data types refer to scalar data types like string, integer, Boolean, and float.

The following code snippet defines a Lambda function that returns a dictionary of variables with primitive data types. Your Lambda function code will return a JSON of key-value pairs when invoked from the Lambda step within the SageMaker pipeline.

```python
def handler(event, context):
    ...
    return {
        "output1": "string_value",
        "output2": 1,
        "output3": True,
        "output4": 2.0,
    }
```

In the pipeline definition, you can then define SageMaker pipeline parameters that are of a specific data type and set the variable to the output of the Lambda function:

```python
from sagemaker.workflow.lambda_step import (
    LambdaStep,
    LambdaOutput,
    LambdaOutputTypeEnum
)
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.sklearn.processing import SKLearnProcessor

role = sagemaker.get_execution_role()
pipeline_session = PipelineSession()

# 1. Define the output params of the Lambda Step

str_outputParam = LambdaOutput(output_name="output1", output_type=LambdaOutputTypeEnum.String)
int_outputParam = LambdaOutput(output_name"output2", output_type=LambdaOutputTypeEnum.Integer)
bool_outputParam = LambdaOutput(output_name"output3", output_type=LambdaOutputTypeEnum.Boolean)
float_outputParam = LambdaOutput(output_name"output4", output_type=LambdaOutputTypeEnum.Float)

# 2. Lambda step invoking the lambda function and returns the Output

step_lambda = LambdaStep(
    name="MyLambdaStep",
    lambda_func=Lambda(
        function_arn="arn:aws:lambda:us-west-2:123456789012:function:sagemaker_test_lambda",
        session=PipelineSession(),
        ),
    inputs={"arg1": "foo", "arg2": "foo1"},
    outputs=[
        str_outputParam, int_outputParam, bool_outputParam, float_outputParam
        ],
)

# 3. Extract the output of the Lambda

str_outputParam = step_lambda.properties.Outputs["output1"]

# 4. Use it in a subsequent step. For ex. Processing step

sklearn_processor = SKLearnProcessor(
    framework_version="0.23-1",
    instance_type="ml.m5.xlarge",
    instance_count=1,
    sagemaker_session=pipeline_session,
    role=role
)

processor_args = sklearn_processor.run(
    code="code/preprocess.py", #python script to run
    arguments=["--input-args", str_outputParam]
)

step_process = ProcessingStep(
    name="processstep1",
    step_args=processor_args,
)
```

Scenario 2: Pass the output (non-primitive data types) of a Lambda step to a processing step
Non-primitive data types refer to non-scalar data types (for example, NamedTuple). You may have a scenario when you have to return a non-primitive data type from a Lambda function. To do this, you have to convert your non-primitive data type to a string:

```python
# Lambda function code returning a non primitive data type

from collections import namedtuple

def lambda_handler(event, context):
    Outputs = namedtuple("Outputs", "sample_output")
    named_tuple = Outputs(
                    [
                        {'output1': 1, 'output2': 2},
                        {'output3': 'foo', 'output4': 'foo1'}
                    ]
                )
return{
    "named_tuple_string": str(named_tuple)
}
#Pipeline step that uses the Lambda output as a “Parameter Input”

output_ref = step_lambda.properties.Outputs["named_tuple_string"]
```

Then you can use this string as an input to a subsequent step in the pipeline. To use the named tuple in the code, use eval() to parse the Python expression in the string:

```python
# Decipher the string in your processing logic code

import argparse
from collections import namedtuple

Outputs = namedtuple("Outputs", "sample_output")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--named_tuple_string", type=str, required=True)
    args = parser.parse_args()
    #use eval to obtain the named tuple from the string
    named_tuple = eval(args.named_tuple_string)
```

Scenario 3: Pass the output of a step through a property file
You can also store the output of a processing step in a property JSON file for downstream consumption in a ConditionStep or another ProcessingStep. You can use the JSONGet function to query a property file. See the following code:

```python
# 1. Define a Processor with a ProcessingOutput
sklearn_processor = SKLearnProcessor(
    framework_version="0.23-1",
    instance_type="ml.m5.xlarge",
    instance_count=1,
    base_job_name="sklearn-abalone-preprocess",
    sagemaker_session=session,
    role=sagemaker.get_execution_role(),
)

step_args = sklearn_processor.run(

                outputs=[
                    ProcessingOutput(
                        output_name="hyperparam",
                        source="/opt/ml/processing/evaluation"
                    ),
                ],
            code="./local/preprocess.py",
            arguments=["--input-data", "s3://my-input"],
)

# 2. Define a PropertyFile where the output_name matches that with the one used in the Processor
hyperparam_report = PropertyFile(
    name="AbaloneHyperparamReport",
    output_name="hyperparam",
    path="hyperparam.json",
)
```

Let’s assume the property file’s contents were the following:

```json
{
  "hyperparam": {
    "eta": {
      "value": 0.6
    }
  }
}
```

In this case, it can be queried for a specific value and used in subsequent steps using the JsonGet function:

```python
# 3. Query the property file
eta = JsonGet(
    step_name=step_process.name,
    property_file=hyperparam_report,
    json_path="hyperparam.eta.value",
)
```

### Parameterize a variable in pipeline definition

Parameterizing variables so that they can be used at runtime is often desirable—for example, to construct an S3 URI. You can parameterize a string such that it is evaluated at runtime using the Join function. The following code snippet shows how to define the variable using the Join function and use that to set the output location in a processing step:

```python
# define the variable to store the s3 URI
s3_location = Join(
    on="/",
    values=[
        "s3:/",
        ParameterString(
            name="MyBucket",
            default_value=""
        ),
        "training",
        ExecutionVariables.PIPELINE_EXECUTION_ID
    ]
)

# define the processing step
sklearn_processor = SKLearnProcessor(
    framework_version="1.2-1",
    instance_type="ml.m5.xlarge",
    instance_count=processing_instance_count,
    base_job_name=f"{base_job_prefix}/sklearn-abalone-preprocess",
    sagemaker_session=pipeline_session,
    role=role,
)

# use the s3uri as the output location in processing step
processor_run_args = sklearn_processor.run(
    outputs=[
        ProcessingOutput(
            output_name="train",
            source="/opt/ml/processing/train",
            destination=s3_location,
        ),
    ],
    code="code/preprocess.py"
)

step_process = ProcessingStep(
    name="PreprocessingJob”,
    step_args=processor_run_args,
)
```

### Run parallel code over an iterable

Some ML workflows run code in parallel for-loops over a static set of items (an iterable). It can either be the same code that gets run on different data or a different piece of code that needs to be run for each item. For example, if you have a very large number of rows in a file and want to speed up the processing time, you can rely on the former pattern. If you want to perform different transformations on specific sub-groups in the data, you might have to run a different piece of code for every sub-group in the data. The following two scenarios illustrate how you can design SageMaker pipelines for this purpose.

#### Scenario 1: Implement a processing logic on different portions of data

You can run a processing job with multiple instances (by setting instance_count to a value greater than 1). This distributes the input data from Amazon S3 into all the processing instances. You can then use a script (process.py) to work on a specific portion of the data based on the instance number and the corresponding element in the list of items. The programming logic in process.py can be written such that a different module or piece of code gets run depending on the list of items that it processes. The following example defines a processor that can be used in a ProcessingStep:

```python
sklearn_processor = FrameworkProcessor(
    estimator_cls=sagemaker.sklearn.estimator.SKLearn,
    framework_version="0.23-1",
    instance_type='ml.m5.4xlarge',
    instance_count=4, #number of parallel executions / instances
    base_job_name="parallel-step",
    sagemaker_session=session,
    role=role,
)

step_args = sklearn_processor.run(
    code='process.py',
    arguments=[
        "--items",
        list_of_items, #data structure containing a list of items
        inputs=[
            ProcessingInput(source="s3://sagemaker-us-east-1-xxxxxxxxxxxx/abalone/abalone-dataset.csv",
                    destination="/opt/ml/processing/input"
            )
        ],
    ]
)
```

#### Scenario 2: Run a sequence of steps

When you have a sequence of steps that need to be run in parallel, you can define each sequence as an independent SageMaker pipeline. The run of these SageMaker pipelines can then be triggered from a Lambda function that is part of a LambdaStep in the parent pipeline. The following piece of code illustrates the scenario where two different SageMaker pipeline runs are triggered:

```python
import boto3
def lambda_handler(event, context):
    items = [1, 2]
    #sagemaker client
    sm_client = boto3.client("sagemaker")

    #name of the pipeline that needs to be triggered.
    #if there are multiple, you can fetch available pipelines using boto3 api
    #and trigger the appropriate one based on your logic.
    pipeline_name = 'child-pipeline-1'

    #trigger pipeline for every item
    response_ppl = sm_client.start_pipeline_execution(
                        PipelineName=pipeline_name,
                        PipelineExecutionDisplayName=pipeline_name+'-item-%d' %(s),
                    )
    pipeline_name = 'child-pipeline-2'
    response_ppl = sm_client.start_pipeline_execution(
                        PipelineName=pipeline_name,
                        PipelineExecutionDisplayName=pipeline_name+'-item-%d' %(s),
                    )
return
```

## Conclusion

In this post, we discussed some best practices for the efficient use and maintenance of SageMaker pipelines. We also provided certain patterns that you can adopt while designing workflows with SageMaker Pipelines, whether you are authoring new pipelines or are migrating ML workflows from other orchestration tools. To get started with SageMaker Pipelines for ML workflow orchestration, refer to the code samples on GitHub and Amazon SageMaker Model Building Pipelines.
