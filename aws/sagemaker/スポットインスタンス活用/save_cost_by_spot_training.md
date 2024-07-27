## refs:

- [Managed Spot Training: Save Up to 90% On Your Amazon SageMaker Training Jobs](https://aws.amazon.com/jp/blogs/aws/managed-spot-training-save-up-to-90-on-your-amazon-sagemaker-training-jobs/)

# Managed Spot Training: Save Up to 90% On Your Amazon SageMaker Training Jobs

Amazon SageMaker is a fully-managed, modular machine learning (ML) service that enables developers and data scientists to easily build, train, and deploy models at any scale. With a choice of using built-in algorithms, bringing your own, or choosing from algorithms available in AWS Marketplace, it’s never been easier and faster to get ML models from experimentation to scale-out production.

One of the key benefits of Amazon SageMaker is that it frees you of any infrastructure management, no matter the scale you’re working at. For instance, instead of having to set up and manage complex training clusters, you simply tell Amazon SageMaker which Amazon Elastic Compute Cloud (Amazon EC2) instance type to use, and how many you need: the appropriate instances are then created on-demand, configured, and terminated automatically once the training job is complete. As customers have quickly understood, this means that they will never pay for idle training instances, a simple way to keep costs under control.

Introducing Managed Spot Training
Going one step further, we’re extremely happy to announce Managed Spot Training for Amazon SageMaker, a new feature based on Amazon EC2 Spot Instances that will help you lower ML training costs by up to 90% compared to using on-demand instances in Amazon SageMaker. Launched almost 10 years ago, Spot Instances have since been one of the cornerstones of building scalable and cost-optimized IT platforms on AWS. Starting today, not only will your Amazon SageMaker training jobs run on fully-managed infrastructure, they will also benefit from fully-managed cost optimization, letting you achieve much more with the same budget. Let’s dive in!

Managed Spot Training is available in all training configurations:

All instance types supported by Amazon SageMaker,
All models: built-in algorithms, built-in frameworks, and custom models,
All configurations: single instance training, distributed training, and automatic model tuning.
Setting it up is extremely simple, as it should be when working with a fully-managed service:

If you’re using the console, just switch the feature on.
If you’re working with the Amazon SageMaker SDK, just set the train_use_spot_instances to true in the Estimator constructor.
That’s all it takes: do this, and you’ll save up to 90%. Pretty cool, don’t you think?

Interruptions and Checkpointing
There’s an important difference when working with Managed Spot Training. Unlike on-demand training instances that are expected to be available until a training job completes, Managed Spot Training instances may be reclaimed at any time if we need more capacity.

With Amazon Elastic Compute Cloud (Amazon EC2) Spot Instances, you would receive a termination notification 2 minutes in advance, and would have to take appropriate action yourself. Don’t worry, though: as Amazon SageMaker is a fully-managed service, it will handle this process automatically, interrupting the training job, obtaining adequate spot capacity again, and either restarting or resuming the training job. This makes Managed Spot Training particularly interesting when you’re flexible on job starting time and job duration. You can also use the MaxWaitTimeInSeconds parameter to control the total duration of your training job (actual training time plus waiting time).

To avoid restarting a training job from scratch should it be interrupted, we strongly recommend that you implement checkpointing, a technique that saves the model in training at periodic intervals. Thanks to this, you can resume a training job from a well-defined point in time, continuing from the most recent partially trained model:

Built-in frameworks and custom models: you have full control over the training code. Just make sure that you use the appropriate APIs to save model checkpoints to Amazon Simple Storage Service (Amazon S3) regularly, using the location you defined in the CheckpointConfig parameter and passed to the SageMaker Estimator. Please note that TensorFlow uses checkpoints by default. For other frameworks, you’ll find examples in our sample notebooks and in the documentation.
Built-in algorithms: computer vision algorithms support checkpointing (Object Detection, Semantic Segmentation, and very soon Image Classification). As they tend to train on large data sets and run for longer than other algorithms, they have a higher likelihood of being interrupted. Other built-in algorithms do not support checkpointing for now.
Alright, enough talk, time for a quick demo!

Training a Built-in Object Detection Model with Managed Spot Training
Reading from this sample notebook, let’s use the AWS console to train the same job with Managed Spot Training instead of on-demand training. As explained before, I only need to take care of two things:

Enable Managed Spot Training (obviously).
Set MaxWaitTimeInSeconds.

First, let’s name our training job, and make sure it has appropriate AWS Identity and Access Management (IAM) permissions (no change).

Then, I select the built-in algorithm for object detection.

Then, I select the instance count and instance type for my training job, making sure I have enough storage for the checkpoints.

The next step is to set hyper parameters, and I’ll use the same ones as in the notebook. I then define the location and properties of the training data set.

I do the same for the validation data set.

I also define where model checkpoints should be saved. This is where Amazon SageMaker will pick them up to resume my training job should it be interrupted.

This is where the final model artifact should be saved.

Good things come to those who wait! This is where I enable Managed Spot Training, configuring a very relaxed 48 hours of maximum wait time.

I’m done, let’s train this model. Once training is complete, cost savings are clearly visible in the console.

As you can see, my training job ran for 2423 seconds, but I’m only billed for 837 seconds, saving 65% thanks to Managed Spot Training! While we’re on the topic, let me explain how pricing works.

Pricing
A Managed Spot training job is priced for the duration for which it ran before it completed, or before it was terminated.

For built-in algorithms and AWS Marketplace algorithms that don’t use checkpointing, we’re enforcing a maximum training time of 60 minutes (MaxWaitTimeInSeconds parameter).

Last but not least, no matter how many times the training job restarts or resumes, you only get charged for data download time once.

Now Available!
This new feature is available in all regions where Amazon SageMaker is available, so don’t wait and start saving now!

As always, we’d love to hear your feedback: please post it to the AWS forum for Amazon SageMaker, or send it through your usual AWS contacts.
