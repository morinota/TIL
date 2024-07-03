## refs:

https://aws.amazon.com/jp/blogs/machine-learning/creating-a-machine-learning-powered-rest-api-with-amazon-api-gateway-mapping-templates-and-amazon-sagemaker/

# Creating a machine learning-powered REST API with Amazon API Gateway mapping templates and Amazon SageMaker

July 2022: Post was reviewed for accuracy.

Amazon SageMaker enables organizations to build, train, and deploy machine learning models. Consumer-facing organizations can use it to enrich their customers’ experiences, for example, by making personalized product recommendations, or by automatically tailoring application behavior based on customers’ observed preferences. When building such applications, one key architectural consideration is how to make the runtime inference endpoint available to client software running on consumer devices. Typically, the endpoint is fronted as part of a broader API, based on a conventional web-friendly approach, such as REST, which offers a complete set of application functions to client software.

Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. API Gateway can be used to present an external-facing, single point of entry for Amazon SageMaker endpoints, with the following benefits:

Insulates clients from the specifics of the underlying implementation by translating between a client-facing REST API and the underlying Amazon SageMaker runtime inference API
Supports authentication and authorization of client requests
Manages client requests through the use of throttling, rate-limiting, and quota management
Uses firewall features as provided by AWS WAF
Enables cost savings and operational optimization through caching and request validation
Makes it easier to create canary deployments to introduce model changes safely
In this post, I show how API Gateway can be used to front an Amazon SageMaker inference endpoint as (part of) a REST API, by making use of an API Gateway feature called mapping templates. This feature makes it possible for the REST API to be integrated directly with an Amazon SageMaker runtime endpoint, thereby avoiding the use of any intermediate compute resource (such as AWS Lambda or Amazon ECS containers) to invoke the endpoint. The result is a solution that is simpler, faster, and cheaper to run.

This direct integration approach is especially useful for consumer applications that exhibit high traffic volumes at peak demand times. Amazon SageMaker supports automatic scaling for inference endpoints, and API Gateway automatically scales to match demand, ensuring that there is always sufficient capacity to process incoming requests, and that you only pay for what you use.

Note: This post focuses on direct integration with Amazon SageMaker, but you can also use mapping templates in combination with an intermediate compute layer (based, for example, on AWS Lambda), in which case you can use them to reduce load on the compute layer by reshaping payloads at the gateway itself.

I demonstrate the approach using a console-based walk through, starting with deployment of an Amazon SageMaker model endpoint, and then stepping through the creation of an Amazon API Gateway integration with this endpoint.

## Overview of solution
For illustration purposes, this post employs a use case in which a TV app requests ratings predictions for a list of movies. Whenever the app displays a page of movies, it should display them so that movies with a higher ratings prediction are more prominent on the page. In this example, every user and movie can be identified by a numeric ID, and predicted ratings are on a scale of 1 to 5, with a higher rating indicating a stronger likelihood that the user will like a particular movie.


### Architecture

The following diagram summarizes the architecture, key components, and interactions in the solution. End-users interact with a client application (using a web browser or mobile device) that sends a REST-style request to an API Gateway endpoint. API Gateway maps this to the request format required by the Amazon SageMaker endpoint, and invokes the endpoint to obtain an inference from the model. API Gateway subsequently receives the response from the Amazon SageMaker endpoint and maps it to a response that is sent back to the client.

### Request and response formats

The solution incorporates a REST API that supports a single resource (predicted-ratings) and a GET method. The request takes the form:

```shell
GET /<api-path>/predicted-ratings/{user_id}?items=id1,id2,…,idn&
```

where the path parameter user_id represents the user for which ratings are required, and the query string parameter items contains a comma-separated list of item identifiers.

If the request is processed successfully, the returned HTTP response has response code 200, and the body is a JSON object containing a list of predicted ratings for the specified items as follows:

```shell
{
  "ratings": [
    rating_1,
    rating_2,
    …,
    rating_n
  ]
}
```

For example, you could enter the following request:

```shell
% curl "https://<api-path>/predicted-ratings/321?items=101,131,162&"
```


This would return with a response similar to the below:

```shell
{
  "ratings": [
    3.527499437332153,    
    3.951640844345093,    
    3.658416271209717    
  ]
}
```

### Amazon SageMaker model input and output formats

The rating predictor solution is based on a sample model that comes supplied with Amazon SageMaker, specifically: object2vec_movie_recommendation.ipynb. This model inference endpoint supports a POST method, and expects the request body to contain a JSON payload as follows:

```shell
{
  "instances": [
    {"in0": [863], "in1": [882]},
    {"in0": [278], "in1": [311]},
    {"in0": [705], "in1": [578]},
    …
  ]
}
```

where in0 represents a user ID, and in1 represents a movie ID.

The model inference returns the following output:

```shell
{
  "predictions": [
    {"scores": [3.047305107116699]},
    {"scores": [3.58427882194519]},
    {"scores": [4.356469631195068]},
    …
  ]
}
```

You can use mapping templates to map the GET request format received by the REST API to the POST input format expected by the Amazon SageMaker model endpoint, and conversely map the model output format to the response format required by the REST API.

### Amazon API Gateway method integration
When you use API Gateway to create a REST API, you need to define the following configuration models for each API method:

Method request – Defines the data model for the REST request format, and specifies validation and authorization checks to be performed on the received REST request.
Integration request – Details how the REST request and associated parameters map to the format expected by the backend service endpoint (which in this example is an Amazon SageMaker inference endpoint).
Integration response – Details how the response received from the backend service (including errors) map to the response format expected by API Gateway.
Method Response – Defines the data model and response format expected by the REST API.
The following diagram depicts the processing flow, and shows how an example request and response are transformed at each stage.

### Mapping Templates
As part of the integration request and response configurations, the solution defines mapping templates using the Apache Velocity Template Language (VTL). VTL is a templating language that was originally designed for web development, but can also be used as a data format transformation tool to convert from one JSON format to another. With mapping templates, you can use VTL templates to convert from the REST request format to the model input format, and to convert the model output to the REST response format.

## Walkthrough steps
The walkthrough contains the following key steps:

Build and deploy an Amazon SageMaker model
Test the Amazon SageMaker model endpoint using the AWS CLI
Create an IAM execution role for the REST API
Build an API Gateway endpoint for the REST API
Create a mapping template for request integration
Create a mapping template for response integration
Deploy and test the API Gateway endpoint

## Prerequisites
To follow this walkthrough, you need to meet the following prerequisites:

Access to an AWS account – You need sufficient IAM permissions to work with IAM roles, Amazon SageMaker, Amazon S3, and API Gateway.
AWS CLI – Install the latest version.
Curl utility – Use version 7.52 onwards.

## Step 1: Building and deploying the Amazon SageMaker model
For this step, you need an S3 bucket to store the model data. You can use an existing bucket or create a new one. Record the name of your bucket as you shall need it later.

Create your model using an Amazon SageMaker Notebook instance. Complete the following steps:

Log in to your AWS account using the AWS Management Console.
On the Amazon SageMaker dashboard, under Notebook Instances, choose Create Notebook Instance.
Under Notebook instance settings, specify a name for your notebook.
For this example, you can set the instance type to ml.t2.medium, which is the most cost-effective option. In practice, you would select the instance type based on the size of the dataset and the nature of the data transformation.

Under Permissions and Encryption, set the IAM role to Create a new role.
Ensure that S3 buckets you specify is selected, specify the bucket name for your bucket, and select Create role.
Leave the remaining settings with the default value.
Choose Create notebook instance.
It takes a few minutes to create your instance. When the status changes from Pending to InService, your notebook instance is ready to use.

Under Actions, choose Open JupyterLab.
A new browser tab opens for your Jupyter notebook.

From the left navigation bar, choose the icon for Amazon SageMaker sample notebooks (hover over the icon to see the label).
From the list of sample notebooks, select object2vec_movie_recommendation.ipynb. as shown below:

The sample notebook you opened is read-only, so you need to create a writeable copy.

Choose Create a Copy at the top right of the pane.
When prompted to Select Kernel use conda_python3.
You are now ready to build and train the model in your notebook. This notebook creates two model inference endpoints (one for ratings prediction, and one for recommendations). You only need the first one, so you do not need to execute all the cells in the notebook.

Before executing any cells, complete the following steps:

In your notebook, scroll down to the section Model training and inference (just over half-way down the notebook). In the first cell (labeled Define S3 bucket that hosts data and model, and upload data to S3), set the bucket name to your choice of S3 bucket as identified earlier.

Starting from the top, use your notebook to execute all cells in order until you get to just before the Recommendation task section (which is about three-quarters of the way down the notebook).

You can either do this by stepping through one cell at a time, or by selecting the first cell in the Recommendation task section and then, under Run, choose Run All Above Selected Cell (see below).

Model training and deployment takes approximately 10 minutes. When it is complete, proceed with the following steps:

On the Amazon SageMaker console, under Inference, choose Endpoints.
Verify that you can see the runtime endpoint.
Record the endpoint name and ARN as you will need these later.

## Step 2: Testing the Amazon SageMaker model endpoint using the AWS CLI
You can test the inference endpoint using the AWS CLI as follows:

```shell
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name <endpoint-name> \
  --body '{"instances": [{"in0":[863],"in1":[882]}]}' \
  --content-type application/json \
  --accept application/json \
  results
```

Note: the above assumes you are using a bash-compatible shell. If you are using the standard Windows command line, replace the outer single quotes with double quotes for the body parameter, and escape the double quotes characters within the JSON.

If your endpoint is working correctly, you should see a file called results that contains output similar to the following:

```shell
{"predictions":[{"scores":[2.433111906051636]}]}
```

Now that you have a working Amazon SageMaker endpoint, you can build a REST API in front of it.

## Creating an execution role for the REST API
Before you build the REST API, you need to create an execution role that gives your API the necessary permission to invoke your Amazon SageMaker endpoint. Complete the following steps:

On the IAM console, under Roles, choose Create Role.
For Select type of trusted entity, select AWS Service.
Choose the service API Gateway.
Choose Next until you reach the Review.
You can see that a policy has been included which allows API Gateway to push logs to CloudWatch.

Give your role a name, for example, APIGatewayAccessToSageMaker.
Choose Create Role.
You now need to add permissions so your role can invoke the Amazon SageMaker endpoint.

Use the role filter to find the role you just created.
Choose the role you created to see the role summary screen.
Choose Add Inline Policy.
On the Create Policy screen, select the service SageMaker and the action InvokeEndpoint.
For Resources, select Specific and enter the ARN for your Amazon SageMaker endpoint.
Choose Review Policy.
Give your policy a name, for example, SageMakerEndpointInvokeAccess.
Choose Create Policy.
On the role summary page, record the ARN for the role as you will need this later.

## Step 4: Building an API Gateway endpoint
In this section, you build your REST API.

### Creating an API
Complete the following steps:

On the API Gateway console, choose Create API.
Choose REST.
Choose New API.
Give your API a name, for example, RatingsPredictor.
For Endpoint Type, choose Regional.
Choose Create API.
Note: In a production system, you should consider whether you would benefit from the Edge Optimized option.

### Creating a resource
In the Resources editor, from the Actions menu, choose CreateResource.
For Resource Name, enter predicted-ratings.
Ensure that the Resource Path field also contains predicted-ratings.
Choose Create Resource.
You should see the predicted-ratings resource appear in the navigation tree.

Choose the predicted-ratings resource you created.
From the Actions menu, choose Create Resource.
For Resource Path, enter {user_id}.
For Resource Name, enter user_id.
Choose Create Resource.
The resource navigation tree should now be similar to the following screenshot, and show /predicted-ratings/{user_id}.

### Creating a GET method
The next step is to create a GET method on the resource path /predicted-ratings/{user_id} and integrate it with your Amazon SageMaker endpoint. Complete the following steps:

From the Actions menu, choose {user_id}.
Choose Create Method.
From the drop-down that appears under the {user_id} resource, select GET and confirm by clicking the tick mark.
The right-hand pane now displays a Setup screen. See the following screenshot.

For Request Integration type, choose AWS Service.
For AWS Region, enter your Region.
For AWS Service, choose SageMaker Runtime.
Leave AWS Subdomain blank.
For HTTP method, choose POST.
For Action Type, choose Use Path override.
For Path override, enter the Amazon SageMaker endpoint path using the format endpoints/<sagemaker-endpoint-name>/invocations.
For Execution role, enter the ARN of the role you created earlier.
For Content Handling, choose Passthrough.
Select Use Default Timeout.
Choose Save.

You have created a GET endpoint in the REST API, and mapped it to a POST endpoint. In the next step, you use mapping templates to map parameters passed in the GET request (from the path and query-string) into the right places in the POST request expected by the Amazon SageMaker endpoint.

## Step 5: Create a mapping template for request integration
You should now see a Method Execution screen in the right-hand pane. See the following screenshot.

This contains a diagram showing how requests flow from your REST API to the Amazon SageMaker runtime and how responses flow back.

### Creating a VTL mapping template
In this next step, create a VTL mapping template to convert GET requests received on the REST API to POST requests expected by the Amazon SageMaker runtime. Complete the following steps:

Choose Integration Request.
Expand the Mapping Templates.
Select Request Body Passthrough: Never.
You can safely ignore the warning because it disappears after you specify a mapping template.

Choose Add mapping template.
For Content-Type, specify application/json and click the tick box to confirm.
If you scroll down, you see a multi-line text entry field. This is where you add your VTL template.

Enter the following template:

```shell
{
  "instances": [
#set( $user_id = $input.params("user_id") )
#set( $items = $input.params("items") )
#foreach( $item in $items.split(",") )
    {"in0": [$user_id], "in1": [$item]}#if( $foreach.hasNext ),#end
    $esc.newline
#end
  ]
}
```

Choose Save.
The template defines what goes into the body of the POST request. The first two lines are copied into the request body exactly as specified. The third line uses a #set directive to extract and store the user_id path parameter in the variable $user_id. The fourth line extracts the query string parameter items and places it in the variable $items. This is stored as a single string containing a comma-separated list of items.

Lines 5-8 loop through all the items and generate the required JSON for each one. The template converts the string held in $items to an array using the string split() method, and iterates through this using a #foreach directive. A comma separator is inserted between JSON objects, with no comma after the last entry.

Testing the mapping
You can now test this mapping using the API Gateway built-in test harness. Complete the following steps:

Choose Method Execution.
Choose Test.
For Path parameter {user_id}, enter 321.
For Query Strings parameter, enter items=101,131,162&.
Choose Test.
If everything is working correctly, you should see response code 200, with a response body that contains a JSON object similar to the below:

```shell
{
  "predictions": [
    {"scores": [3.527499437332153]},
    {"scores": [3.951640844345093]},
    {"scores": [3.658416271209717]}
  ]
}
```

You can also scroll through the logs to verify the sequence of events. You should see something similar to the following:

```shell
<timestamp>: Endpoint request body after transformations: {
  "instances": [
    {"in0": [321], "in1": [101]},
    {"in0": [321], "in1": [131]},
    {"in0": [321], "in1": [162]}
  ]
}
<timestamp> : Sending request to https://runtime.sagemaker.eu-west-1.amazonaws.com/endpoints/recs/invocations
<timestamp> : Received response. Status: 200, Integration latency: 232 ms
```

This proves that the REST request converted successfully to the input format required by the model, and that the model runtime executed successfully. However, the returned response body is still not in the format stipulated for the REST API. By default, API Gateway sets up the response integration to pass the response through unaltered. In the next step, you add a second mapping template to convert the model response to the required REST API format.

## Step 6: Creating a mapping template for response integration
To add a mapping template for the response, complete the following steps:

On the Method Execution screen, choose Integration Response.
You should see a single entry with HTTP status regex set to the single character, with method response 200. This is the default response rule, which returns a 200 response code and passes the response through unaltered.

Expand this rule.
Under Mapping Templates, choose application/json.
Enter the following mapping template

```shell
{
  "ratings": [
#set( $predictions = $input.path("$.predictions") )
#foreach( $item in $predictions )
    $item.scores[0]#if( $foreach.hasNext ),#end
    $esc.newline
#end
  ]
}
```

This template iterates through the list of predictions returned by the model, and produces output that is compliant with the format required by the REST API.

Choose Save.
You can test this again by following the same procedure you used earlier, and this time you should see the output in the required response format.

## Step 7: Deploying and testing the API Gateway endpoint

You are now ready to deploy your REST API. Complete the following steps:

On the Method Execution screen, under Actions, choose Deploy API.
For Deployment stage, choose [New Stage].
Give your stage a name, such as test.
Enter the required descriptions for this stage and deployment.
Choose Deploy.
You should now see a Stage Editor in the right-hand pane, with an Invoke URL endpoint for your deployed API. You can use curl to test your deployed endpoint.

At the command line, enter the following:

```shell
curl "<invoke-url>/predicted-ratings/321?items=101,131,162&"
```

Replace <invoke-url> with the URL for your endpoint.

You should see output similar to the below:

```shell
{
  "ratings": [
    3.527499437332153,
    3.951640844345093,
    3.658416271209717
  ]
}
```

You now have a deployed, working REST API that is integrated with your Amazon SageMaker runtime.

## Additional considerations
This post focused on how to use API Gateway mapping templates to transform requests and responses between formats required by the REST API and model runtime. API Gateway provides numerous additional features that you can use to implement authorization, request validation, caching, response error code mapping, and throttling. When you are designing your overall architecture, consider how best to use these features.

This post used an example in which you could map requests and responses directly without the need for any intermediate compute resource. This may not be possible in all situations, such as when you need to enrich the request body with additional data from another source. In such cases, you can still use VTL-based mapping templates to pre-process requests and post-process responses, which reduces the load on any intermediate compute layer.

## Cleaning up
When you are finished experimenting with your setup, clean up the various resources that you used on API Gateway, S3, and Amazon SageMaker. Make sure that you delete the Amazon SageMaker endpoint so you don’t continue to accrue charges.

If you wish to retain the model and API Gateway setup for further experimentation at a later time, you can re-create the endpoint when required. Remember to update the API Gateway request integration if you use a different endpoint name.

## Conclusion
This post demonstrated how to use API Gateway to create a public RESTful endpoint for an Amazon SageMaker inference. Specifically, it showed how to use mapping templates and VTL to transform requests and responses to match the formats expected by the public-facing REST endpoint and the internal inference endpoint.

Mapping templates can help you avoid using intermediate compute resources between API Gateway and Amazon SageMaker. As a result, you reduce the latency and operational complexity of your application. API Gateway Mapping templates are also useful in situations in which you cannot avoid intermediate compute; you can still use them to perform pre- and post-processing to reduce load on the compute layer.

This approach is especially useful for use cases characterized by high-volume peak demand with low-latency inference, as typically seen in consumer applications.

