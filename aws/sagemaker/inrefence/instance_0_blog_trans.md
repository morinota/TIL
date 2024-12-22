
# Unlock cost savings with the new scale down to zero feature in SageMaker Inference SageMaker推論における新しいゼロスケールダウン機能でコスト削減を実現

Today at AWS re:Invent 2024, we are excited to announce a new feature for Amazon SageMaker inference endpoints: the ability to scale SageMaker inference endpoints to zero instances.
2024年のAWS re:Inventで、私たちはAmazon SageMaker推論エンドポイントの新機能、すなわちSageMaker推論エンドポイントをゼロインスタンスにスケールダウンする機能を発表できることを嬉しく思います。

This long-awaited capability is a game changer for our customers using the power of AI and machine learning (ML) inference in the cloud.
この待望の機能は、クラウドにおけるAIおよび機械学習（ML）推論の力を利用する顧客にとって、ゲームチェンジャーとなります。

Previously, SageMaker inference endpoints maintained a minimum number of instances to provide continuous availability, even during periods of low or no traffic.
以前は、SageMaker推論エンドポイントは、トラフィックが少ないまたは全くない期間でも継続的な可用性を提供するために、最小限のインスタンス数を維持していました。

With this update, available when using SageMaker inference components, you have more options to align your resource usage with your specific needs and traffic patterns.
この更新により、SageMaker推論コンポーネントを使用する際に、リソース使用を特定のニーズやトラフィックパターンに合わせるための選択肢が増えました。

Refer to the accompanying notebooks to get started with the new scale down to zero feature.
新しいゼロスケールダウン機能を始めるには、付随するノートブックを参照してください。

The new feature expands the possibilities for managing SageMaker inference endpoints.
この新機能は、SageMaker推論エンドポイントの管理の可能性を広げます。

It allows you to configure the endpoints so they can scale to zero instances during periods of inactivity, providing an additional tool for resource management.
これにより、非アクティブな期間中にエンドポイントをゼロインスタンスにスケールダウンできるように設定でき、リソース管理のための追加ツールを提供します。

With this feature, you can closely match your compute resource usage to your actual needs, potentially reducing costs during times of low demand.
この機能を使用することで、コンピュートリソースの使用を実際のニーズに密接に合わせることができ、需要が低い時期にコストを削減する可能性があります。

This enhancement builds upon the existing auto scaling capabilities in SageMaker, offering more granular control over resource allocation.
この強化は、SageMakerの既存のオートスケーリング機能を基にしており、リソース割り当てに対するより詳細な制御を提供します。

You can now configure your scaling policies to include scaling to zero, allowing for more precise management of your AI inference infrastructure.
これにより、スケーリングポリシーをゼロスケールダウンを含むように設定でき、AI推論インフラストラクチャのより正確な管理が可能になります。

The scale down to zero feature presents new opportunities for how businesses can approach their cloud-based ML operations.
ゼロスケールダウン機能は、企業がクラウドベースのMLオペレーションにアプローチする新しい機会を提供します。

It provides additional options for managing resources across various scenarios, from development and testing environments to production deployments with variable traffic patterns.
開発およびテスト環境から、変動するトラフィックパターンを持つ本番展開に至るまで、さまざまなシナリオでリソースを管理するための追加オプションを提供します。

As with any new feature, you are encouraged to carefully evaluate how it fits into your overall architecture and operational needs, considering factors such as response times and the specific requirements of your applications.
新機能と同様に、応答時間やアプリケーションの特定の要件などの要素を考慮しながら、全体のアーキテクチャや運用ニーズにどのように適合するかを慎重に評価することをお勧めします。

In this post, we explore the new scale to zero feature for SageMaker inference endpoints, demonstrating how to implement and use this capability to optimize costs and manage resources more effectively.
この記事では、SageMaker推論エンドポイントの新しいゼロスケールダウン機能を探求し、コストを最適化し、リソースをより効果的に管理するためにこの機能を実装し使用する方法を示します。

We cover the key scenarios where scaling to zero is beneficial, provide best practices for optimizing scale-up time, and walk through the step-by-step process of implementing this functionality.
ゼロスケールダウンが有益な主要なシナリオをカバーし、スケールアップ時間を最適化するためのベストプラクティスを提供し、この機能を実装するためのステップバイステップのプロセスを説明します。

Additionally, we discuss how to set up scheduled scaling actions for predictable traffic patterns and test the behavior of your scaled-to-zero endpoints.
さらに、予測可能なトラフィックパターンのためのスケジュールされたスケーリングアクションの設定方法と、ゼロにスケールダウンしたエンドポイントの動作をテストする方法についても説明します。

## Determining when to scale to zero ゼロスケールのタイミングの決定

Before we dive into the implementation details of the new scale to zero feature, it’s crucial to understand when and why you should consider using it.
新しいゼロスケール機能の実装詳細に入る前に、いつ、なぜそれを使用するべきかを理解することが重要です。

Although the ability to scale SageMaker inference endpoints to zero instances offers significant cost-saving potential, it’s crucial to understand when and how to apply this feature effectively.
SageMaker推論エンドポイントをゼロインスタンスにスケールダウンする能力は、重要なコスト削減の可能性を提供しますが、この機能を効果的に適用するタイミングと方法を理解することが重要です。

Not all scenarios benefit equally from scaling to zero, and in some cases, it may even impact the performance of your applications.
すべてのシナリオがゼロスケールから同じように利益を得るわけではなく、場合によってはアプリケーションのパフォーマンスに影響を与えることさえあります。

Let’s explore why it’s important to carefully consider when to implement this feature and how to identify the scenarios where it provides the most value.
この機能を実装するタイミングを慎重に考慮することがなぜ重要であり、最も価値を提供するシナリオを特定する方法を探っていきましょう。

The ability to scale SageMaker inference endpoints to zero instances is particularly beneficial in three key scenarios:
SageMaker推論エンドポイントをゼロインスタンスにスケールダウンする能力は、特に3つの重要なシナリオで有益です。

By carefully evaluating your specific use case against these scenarios, you can make informed decisions about implementing scale to zero functionality.
これらのシナリオに対して特定のユースケースを慎重に評価することで、ゼロスケール機能の実装に関する情報に基づいた決定を下すことができます。

This approach makes sure you maximize cost savings without compromising on the performance and availability requirements of your ML applications.
このアプローチは、MLアプリケーションのパフォーマンスと可用性の要件を損なうことなく、コスト削減を最大化することを保証します。

It’s important to note that although scaling to zero can provide significant benefits, it also introduces a trade-off in terms of initial response time when scaling back up.
ゼロスケールが重要な利点を提供できる一方で、スケールアップ時の初期応答時間に関するトレードオフも生じることに注意が必要です。

Therefore, it’s crucial to assess whether your application can tolerate this potential delay and to implement appropriate strategies to manage it.
したがって、アプリケーションがこの潜在的な遅延に耐えられるかどうかを評価し、それを管理するための適切な戦略を実装することが重要です。

In the following sections, we dive deeper into each scenario and provide guidance on how to determine if scaling to zero is the right choice for your specific needs.
次のセクションでは、各シナリオをさらに詳しく掘り下げ、ゼロスケールが特定のニーズに適した選択であるかどうかを判断する方法についてのガイダンスを提供します。

We also discuss best practices for implementation and strategies to mitigate potential drawbacks.
また、実装のベストプラクティスや潜在的な欠点を軽減するための戦略についても議論します。

Scale down to zero is only supported when using inference components.
ゼロスケールは、推論コンポーネントを使用している場合にのみサポートされています。

For more information on inference components, see Reduce model deployment costs by 50% on average using the latest features of Amazon SageMaker.
推論コンポーネントに関する詳細は、最新のAmazon SageMakerの機能を使用してモデル展開コストを平均50％削減することを参照してください。

Now that we understand when to use the scale to zero feature, let’s dive into how to optimize its performance and implement it effectively.
ゼロスケール機能を使用するタイミングが理解できたので、そのパフォーマンスを最適化し、効果的に実装する方法に入っていきましょう。

Scaling up from zero instances to serving traffic introduces a brief delay (cold start), which can impact your application’s responsiveness.
ゼロインスタンスからトラフィックを提供するためにスケールアップすることは、アプリケーションの応答性に影響を与える可能性のある短い遅延（コールドスタート）を引き起こします。

To mitigate this, we first explore best practices for minimizing scale-up time.
これを軽減するために、まずスケールアップ時間を最小限に抑えるためのベストプラクティスを探ります。

Then we walk through the step-by-step process of implementing the scale to zero functionality for your SageMaker inference endpoints.
次に、SageMaker推論エンドポイントのゼロスケール機能を実装するためのステップバイステップのプロセスを説明します。

## Optimizing scale-up time best practices スケールアップ時間の最適化ベストプラクティス

When using the scale to zero feature, it’s crucial to minimize the time it takes for your endpoint to scale up and begin serving requests.
スケールゼロ機能を使用する際には、エンドポイントがスケールアップしてリクエストを処理し始めるまでの時間を最小限に抑えることが重要です。

The following are several best practices you can implement to decrease the scale-out time for your SageMaker inference endpoints:
以下は、SageMaker推論エンドポイントのスケールアウト時間を短縮するために実装できるいくつかのベストプラクティスです。

By implementing these best practices, you can help make sure your SageMaker inference endpoints can scale out quickly and efficiently to meet changes in traffic, providing a responsive and reliable experience for your end-users.
これらのベストプラクティスを実装することで、SageMaker推論エンドポイントがトラフィックの変化に迅速かつ効率的にスケールアウトできるようになり、エンドユーザーに対して応答性が高く信頼性のある体験を提供できるようになります。

## Solution overview ソリューションの概要

With these best practices in mind, let’s now walk through the process of enabling your SageMaker inference endpoints to scale down to zero instances.
これらのベストプラクティスを念頭に置いて、SageMaker推論エンドポイントをゼロインスタンスにスケールダウンできるようにするプロセスを見ていきましょう。

This process involves a few key steps that are crucial for optimizing your endpoint’s performance and cost-efficiency:
このプロセスには、エンドポイントのパフォーマンスとコスト効率を最適化するために重要な幾つかの主要なステップが含まれています。

By implementing these scaling policies, you create a flexible and cost-effective infrastructure that can automatically adjust to your workload demands and scale to zero when needed.
これらのスケーリングポリシーを実装することで、ワークロードの要求に自動的に調整し、必要に応じてゼロにスケールダウンできる柔軟でコスト効率の高いインフラストラクチャを構築します。

Now let’s see how to use this feature step by step.
それでは、この機能をステップバイステップで使用する方法を見ていきましょう。

## Set up your endpoint エンドポイントの設定

The first crucial step in enabling your SageMaker endpoint to scale to zero is properly configuring the endpoint and its associated components.
SageMakerエンドポイントをゼロにスケールさせるための最初の重要なステップは、エンドポイントとその関連コンポーネントを適切に設定することです。このプロセスは、主に3つのステップで構成されています。

```

sagemaker_client.create_endpoint_config(EndpointConfigName=endpoint_config_name,ExecutionRoleArn=role,ProductionVariants=[{"VariantName":variant_name,"InstanceType":instance_type,"InitialInstanceCount":1,"ModelDataDownloadTimeoutInSeconds":model_data_download_timeout_in_seconds,"ContainerStartupHealthCheckTimeoutInSeconds":container_startup_health_check_timeout_in_seconds,"ManagedInstanceScaling":{"Status":"ENABLED","MinInstanceCount":0,"MaxInstanceCount":max_instance_count,},"RoutingConfig":{"RoutingStrategy":"LEAST_OUTSTANDING_REQUESTS"},}],)

```

```

sagemaker_client.create_endpoint(EndpointName=endpoint_name,EndpointConfigName=endpoint_config_name,)

```

```

sagemaker_client.create_inference_component(InferenceComponentName=inference_component_name,EndpointName=endpoint_name,VariantName=variant_name,Specification={"ModelName":model_name,"StartupParameters":{"ModelDataDownloadTimeoutInSeconds":3600,"ContainerStartupHealthCheckTimeoutInSeconds":3600,},"ComputeResourceRequirements":{"MinMemoryRequiredInMb":1024,"NumberOfAcceleratorDevicesRequired":1,},},RuntimeConfig={"CopyCount":1,},)

```  

## Add scaling policies スケーリングポリシーの追加

After the endpoint is deployed and InService, you can add the necessary scaling policies:
エンドポイントがデプロイされ、InService（稼働中）になった後、必要なスケーリングポリシーを追加できます：

### Scaling policy for inference components model copies 推論コンポーネントモデルコピーのスケーリングポリシー

After you create your SageMaker endpoint and inference components, you register a new auto scaling target for Application Auto Scaling.
SageMakerエンドポイントと推論コンポーネントを作成した後、Application Auto Scalingのために新しい自動スケーリングターゲットを登録します。

In the following code block, you set MinCapacity to 0, which is required for your endpoint to scale down to zero:
以下のコードブロックでは、MinCapacityを0に設定します。これは、エンドポイントがゼロにスケールダウンするために必要です。

```

# Register scalable target

resource_id = f"inference-component/{inference_component_name}"
service_namespace = "sagemaker"
scalable_dimension = "sagemaker:inference-component:DesiredCopyCount"
aas_client.register_scalable_target(
    ServiceNamespace=service_namespace,
    ResourceId=resource_id,
    ScalableDimension=scalable_dimension,
    MinCapacity=0,
    MaxCapacity=max_copy_count,  # Replace with your desired maximum number of model copies
)

```

After you have registered your new scalable target, the next step is to define your target tracking policy.
新しいスケーラブルターゲットを登録した後、次のステップはターゲットトラッキングポリシーを定義することです。

In the following code example, we set the TargetValue to 5.
以下のコード例では、TargetValueを5に設定します。

This setting instructs the auto scaling system to increase capacity when the number of concurrent requests per model reaches or exceeds 5.
この設定は、モデルごとの同時リクエスト数が5に達するかそれを超えたときに、自動スケーリングシステムに容量を増やすよう指示します。

```

# Create Target Tracking Scaling Policy

aas_client.put_scaling_policy(
    PolicyName="inference-component-target-tracking-scaling-policy",
    PolicyType="TargetTrackingScaling",
    ServiceNamespace=service_namespace,
    ResourceId=resource_id,
    ScalableDimension=scalable_dimension,
    TargetTrackingScalingPolicyConfiguration={
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "SageMakerInferenceComponentConcurrentRequestsPerCopyHighResolution",
        },
        # Low TPS + load TPS
        "TargetValue": 5,  # you need to adjust this value based on your use case
        "ScaleInCooldown": 300,  # default
        "ScaleOutCooldown": 300,  # default
    },
)

```

Application Auto Scaling creates two CloudWatch alarms per scaling target.
Application Auto Scalingは、各スケーリングターゲットに対して2つのCloudWatchアラームを作成します。

The first triggers scale-out actions after 1 minute (using one 1-minute data point), and the second triggers scale-in after 15 minutes (using 90 10-second data points).
最初のアラームは1分後にスケールアウトアクションをトリガーし（1分間のデータポイントを使用）、2番目は15分後にスケールインをトリガーします（90個の10秒データポイントを使用）。

The time to trigger the scaling action is usually 1–2 minutes longer than those minutes because it takes time for the endpoint to publish metrics to CloudWatch, and it also takes time for AutoScaling to react.
スケーリングアクションをトリガーするまでの時間は、通常、これらの分数よりも1〜2分長くなります。これは、エンドポイントがCloudWatchにメトリクスを公開するのに時間がかかり、AutoScalingが反応するのにも時間がかかるためです。

### Scale out from zero model copies policy ゼロモデルコピーからのスケールアウトポリシー

To enable your endpoint to scale out from zero instances, complete the following steps:
エンドポイントがゼロインスタンスからスケールアウトできるようにするには、以下の手順を完了してください。

```

aas_client.put_scaling_policy(PolicyName="inference-component-step-scaling-policy",PolicyType="StepScaling",ServiceNamespace=service_namespace,ResourceId=resource_id,ScalableDimension=scalable_dimension,StepScalingPolicyConfiguration={"AdjustmentType":"ChangeInCapacity","MetricAggregationType":"Maximum","Cooldown":60,"StepAdjustments":[{"MetricIntervalLowerBound":0,"ScalingAdjustment":1# you need to adjust this value based on your use case}]},)

```

When triggered, the alarm initiates the previously defined scaling policy.
トリガーされると、アラームは以前に定義されたスケーリングポリシーを開始します。
For more information about the NoCapacityInvocationFailures metric, see documentation.
NoCapacityInvocationFailuresメトリックに関する詳細は、ドキュメントを参照してください。

We have also set the following:
私たちは以下の設定も行いました：

This results in waiting approximately 1 minute for the step scaling policy to trigger after our endpoint receives a single request.
これにより、エンドポイントが単一のリクエストを受け取った後、ステップスケーリングポリシーがトリガーされるまで約1分待機することになります。

```

cw_client.put_metric_alarm(AlarmName='ic-step-scaling-policy-alarm',AlarmActions=<step_scaling_policy_arn>,# Replace with your actual ARNMetricName='NoCapacityInvocationFailures',Namespace='AWS/SageMaker',Statistic='Maximum',Dimensions=[{'Name':'InferenceComponentName','Value':inference_component_name# Replace with actual InferenceComponentName}],Period=30,EvaluationPeriods=1,DatapointsToAlarm=1,Threshold=1,ComparisonOperator='GreaterThanOrEqualToThreshold',TreatMissingData='missing')

```

Replace <STEP_SCALING_POLICY_ARN> with the Amazon Resource Name (ARN) of the scaling policy you created in the previous step.
<STEP_SCALING_POLICY_ARN>を、前のステップで作成したスケーリングポリシーのAmazonリソース名（ARN）に置き換えてください。

Notice the "MinInstanceCount": 0 setting in the endpoint configuration, which allows the endpoint to scale down to zero instances.
エンドポイント設定の "MinInstanceCount": 0 設定に注意してください。これにより、エンドポイントはゼロインスタンスまでスケールダウンできます。
With the scaling policy, CloudWatch alarm, and minimum instances set to zero, your SageMaker inference endpoint will now be able to automatically scale down to zero instances when not in use.
スケーリングポリシー、CloudWatchアラーム、および最小インスタンスがゼロに設定されていることで、SageMaker推論エンドポイントは、使用されていないときに自動的にゼロインスタンスまでスケールダウンできるようになります。

## Test the solution 解決策のテスト

When our SageMaker endpoint doesn’t receive requests for 15 minutes, it will automatically scale down to zero the number of model copies:
私たちのSageMakerエンドポイントが15分間リクエストを受け取らない場合、モデルのコピーの数は自動的にゼロにスケールダウンします：

```

time.sleep(500)whileTrue:desc=sagemaker_client.describe_inference_component(InferenceComponentName=inference_component_name)status=desc["InferenceComponentStatus"]print(status)sys.stdout.flush()ifstatusin["InService","Failed"]:breaktime.sleep(30)desc=sagemaker_client.describe_inference_component(InferenceComponentName=inference_component_name)print(desc)

```

After 10 additional minutes of inactivity, SageMaker automatically stops all underlying instances of the endpoint, eliminating all associated instance costs.
さらに10分間の非アクティブ状態の後、SageMakerはエンドポイントのすべての基盤となるインスタンスを自動的に停止し、関連するインスタンスコストをすべて排除します。

If we try to invoke our endpoint while instances are scaled down to zero, we get a validation error:
インスタンスがゼロにスケールダウンしている間にエンドポイントを呼び出そうとすると、検証エラーが発生します：

An error occurred (ValidationError) when calling the InvokeEndpoint operation: Inference Component has no capacity to process this request. ApplicationAutoScaling may be in-progress (if configured) or try to increase the capacity by invoking UpdateInferenceComponentRuntimeConfig API.
InvokeEndpoint操作を呼び出す際にエラーが発生しました（ValidationError）：推論コンポーネントにはこのリクエストを処理する能力がありません。ApplicationAutoScalingが進行中である可能性があります（設定されている場合）または、UpdateInferenceComponentRuntimeConfig APIを呼び出して容量を増やそうとしてください。

```

sagemaker_client.invoke_endpoint(EndpointName=endpoint_name,InferenceComponentName=inference_component_name,Body=json.dumps({"inputs":"The diamondback terrapin was the first reptile to be","parameters":{"do_sample":True,"max_new_tokens":256,"min_new_tokens":256,"temperature":0.3,"watermark":True,},}),ContentType="application/json",)["Body"].read().decode("utf8")

```

However, after 1 minute, our step scaling policy should start. SageMaker will then start provisioning a new instance and deploy our inference component model copy to handle requests.
しかし、1分後に、私たちのステップスケーリングポリシーが開始されるべきです。SageMakerは新しいインスタンスのプロビジョニングを開始し、リクエストを処理するために推論コンポーネントのモデルコピーをデプロイします。

## Schedule scaling down to zero スケジュールのスケーリングをゼロにする

In some scenarios, you might observe consistent weekly traffic patterns: a steady workload Monday through Friday, and no traffic on weekends.
いくつかのシナリオでは、一貫した週次トラフィックパターンを観察することがあります。月曜日から金曜日までの安定した作業負荷と、週末のトラフィックがないことです。
You can optimize costs and performance by configuring scheduled actions that align with these patterns:
これらのパターンに合わせてスケジュールされたアクションを設定することで、コストとパフォーマンスを最適化できます。

You can scale your endpoint to zero in two ways.
エンドポイントをゼロにスケールダウンする方法は2つあります。
The first method is to set the number of model copies to zero in your inference component using the UpdateInferenceComponentRuntimeConfig API.
最初の方法は、UpdateInferenceComponentRuntimeConfig APIを使用して推論コンポーネントのモデルコピー数をゼロに設定することです。
This approach maintains your endpoint configuration while eliminating compute costs during periods of inactivity.
このアプローチは、エンドポイントの構成を維持しながら、非アクティブな期間中の計算コストを排除します。

```

sagemaker_client.update_inference_component_runtime_config(InferenceComponentName=inference_component_name, DesiredRuntimeConfig={'CopyCount':0})

```

Amazon EventBridge Scheduler can automate SageMaker API calls using cron/rate expressions for recurring schedules or one-time invocations.
Amazon EventBridge Schedulerは、定期的なスケジュールや一度きりの呼び出しのためにcron/rate式を使用してSageMaker API呼び出しを自動化できます。
To function, EventBridge Scheduler requires an execution role with appropriate permissions to invoke the target API operations on your behalf.
EventBridge Schedulerが機能するためには、ターゲットAPI操作をあなたの代わりに呼び出すための適切な権限を持つ実行ロールが必要です。
For more information about how to create this role, see Set up the execution role.
このロールの作成方法の詳細については、「実行ロールの設定」を参照してください。
The specific permissions needed depend on the target API being called.
必要な特定の権限は、呼び出されるターゲットAPIによって異なります。

The following code creates two scheduled actions for the inference component during 2024–2025.
以下のコードは、2024年から2025年の間に推論コンポーネントのための2つのスケジュールされたアクションを作成します。
The first schedule scales in the CopyCount to zero every Friday at 18:00 UTC+1, and the second schedule restores model capacity every Monday at 07:00 UTC+1.
最初のスケジュールは、毎週金曜日の18:00 UTC+1にCopyCountをゼロにスケールダウンし、2番目のスケジュールは毎週月曜日の07:00 UTC+1にモデルの容量を復元します。
The schedule will start on November 29, 2024, end on December 31, 2025, and be deleted after completion.
このスケジュールは2024年11月29日に開始し、2025年12月31日に終了し、完了後に削除されます。

```

import json
scheduler = boto3.client('scheduler')
flex_window = {"Mode": "OFF"}

# We specify the SageMaker target API for the scale in schedule

scale_in_target = {
    "RoleArn": role,
    "Arn": "arn:aws:scheduler:::aws-sdk:sagemaker:updateInferenceComponentRuntimeConfig",
    "Input": json.dumps({"DesiredRuntimeConfig": {"CopyCount": 0}, "InferenceComponentName": inference_component_name})
}

# Scale in our endpoint to 0 every Friday at 18:00 UTC+1, starting on November 29, 2024

scheduler.create_schedule(
    Name="scale-to-zero-schedule",
    ScheduleExpression="cron(00 18 ? * 6 2024-2025)",
    ScheduleExpressionTimezone="UTC+1",
    # Set the correct timezone for your application
    Target=scale_in_target,
    FlexibleTimeWindow=flex_window,
    ActionAfterCompletion="DELETE",
    StartDate="2024-11-29T00:00:00",
    EndDate="2025-12-31T23:59:59"
)

# Specify the SageMaker target API for the scale out schedule

scale_out_target = {
    "RoleArn": role,
    "Arn": "arn:aws:scheduler:::aws-sdk:sagemaker:updateInferenceComponentRuntimeConfig",
    "Input": json.dumps({"DesiredRuntimeConfig": {"CopyCount": 2}, "InferenceComponentName": inference_component_name})
}

# Scale out our endpoint every Monday at 07:00 UTC+1

scheduler.create_schedule(
    Name="scale-out-schedule",
    ScheduleExpression="cron(00 07 ? * 2 2024-2025)",
    ScheduleExpressionTimezone="UTC+1",
    # Set the correct timezone for your application
    Target=scale_out_target,
    FlexibleTimeWindow=flex_window,
    ActionAfterCompletion="DELETE",
    StartDate="2024-11-29T00:00:00",
    EndDate="2025-12-31T23:59:59"
)

```

The second method is to delete the inference components by calling the DeleteInferenceComponent API.
2番目の方法は、DeleteInferenceComponent APIを呼び出して推論コンポーネントを削除することです。
This approach achieves the same cost-saving benefit while completely removing the components from your configuration.
このアプローチは、構成からコンポーネントを完全に削除しながら、同じコスト削減の利点を達成します。
The following code creates a scheduled action that automatically deletes the inference component every Friday at 18:00 UTC during 2024–2025.
以下のコードは、2024年から2025年の間に毎週金曜日の18:00 UTCに推論コンポーネントを自動的に削除するスケジュールされたアクションを作成します。
It also creates a complementary scheduled action that recreates the inference component every Monday at 07:00 UTC+1.
また、毎週月曜日の07:00 UTC+1に推論コンポーネントを再作成する補完的なスケジュールされたアクションも作成します。

```

import json
scheduler = boto3.client('scheduler')
flex_window = {"Mode": "OFF"}

# We specify the SageMaker target API for the scale in schedule

scale_in_target = {
    "RoleArn": role,
    "Arn": "arn:aws:scheduler:::aws-sdk:sagemaker:deleteInferenceComponent",
    "Input": json.dumps({"InferenceComponentName": inference_component_name})
}

# Scale in our endpoint by deleting the IC every Friday at 18:00 UTC+1

scheduler.create_schedule(
    Name="scale-to-zero-schedule",
    ScheduleExpression="cron(00 18 ? * 6 2024-2025)",
    ScheduleExpressionTimezone="UTC+1",
    # Set the correct timezone for your application
    Target=scale_in_target,
    FlexibleTimeWindow=flex_window,
    ActionAfterCompletion="DELETE",
    StartDate="2024-11-29T00:00:00",
    EndDate="2025-12-31T23:59:59"
)

# Specify the SageMaker target API for the scale up schedule

input_config = {
    "EndpointName": endpoint_name,
    "InferenceComponentName": inference_component_name,
    "RuntimeConfig": {"CopyCount": 2},
    "Specification": {
        "ModelName": model_name,
        "StartupParameters": {
            "ModelDataDownloadTimeoutInSeconds": 3600,
            "ContainerStartupHealthCheckTimeoutInSeconds": 3600,
        },
        "ComputeResourceRequirements": {
            "MinMemoryRequiredInMb": 1024,
            "NumberOfAcceleratorDevicesRequired": 1
        }
    },
    "VariantName": variant_name
}
scale_out_target = {
    "RoleArn": role,
    "Arn": "arn:aws:scheduler:::aws-sdk:sagemaker:createInferenceComponent",
    "Input": json.dumps(input_config)
}

# Scale out our endpoint by recreating the IC every Monday at 07:00 UTC+1

scheduler.create_schedule(
    Name="scale-out-schedule",
    ScheduleExpression="cron(00 07 ? * 2 2024-2025)",
    ScheduleExpressionTimezone="UTC+1",
    # Set the correct timezone for your application
    Target=scale_out_target,
    FlexibleTimeWindow=flex_window,
    ActionAfterCompletion="DELETE",
    StartDate="2024-11-29T00:00:00",
    EndDate="2025-12-31T23:59:59"
)

```

To scale to zero on an endpoint with multiple inference components, all components must be either set to 0 or deleted.
複数の推論コンポーネントを持つエンドポイントをゼロにスケールダウンするには、すべてのコンポーネントを0に設定するか、削除する必要があります。
You can also automate this process by using EventBridge Scheduler to trigger an AWS Lambda function that handles either deletion or zero-setting of all inference components.
このプロセスは、EventBridge Schedulerを使用してAWS Lambda関数をトリガーし、すべての推論コンポーネントの削除またはゼロ設定を処理することで自動化することもできます。

## Performance evaluation パフォーマンス評価

We evaluated the performance implications of the Scale to Zero feature by conducting tests using a Llama3-8B instruct model.
私たちは、Llama3-8B instructモデルを使用して、Scale to Zero機能のパフォーマンスへの影響を評価するためのテストを実施しました。
These tests utilized container caching and optimized model loading techniques, and were performed with both Target Tracking and Step Scaling policies in place.
これらのテストは、コンテナキャッシングと最適化されたモデルロード技術を利用し、Target TrackingポリシーとStep Scalingポリシーの両方を適用して実施されました。
Our findings for Llama3-8B instruct show that when using the Target Tracking policy, SageMaker will scale the endpoint to zero model copies in approximately 15 minutes, and then take an additional 10 minutes to fully scale down the underlying instances, for a total scale-in time of 25 minutes.
Llama3-8B instructに関する私たちの発見は、Target Trackingポリシーを使用する場合、SageMakerはエンドポイントをゼロモデルコピーにスケールダウンするのに約15分かかり、その後、基盤となるインスタンスを完全にスケールダウンするのに追加で10分かかり、合計で25分のスケールイン時間がかかることを示しています。
Conversely, when scaling the endpoint back up from zero, the Step Scaling policy triggers the provisioning of new instances in around 1 minute, followed by provisioning the instance(s) in ~1.748 minutes.
逆に、エンドポイントをゼロから再スケールアップする際には、Step Scalingポリシーが新しいインスタンスのプロビジョニングを約1分でトリガーし、その後、インスタンスのプロビジョニングが約1.748分で行われます。
Scaling out of model copies in approximately 2.28 minutes, resulting in a total scale-out time of around 5.028 minutes.
モデルコピーのスケールアウトは約2.28分で行われ、合計スケールアウト時間は約5.028分となります。

The performance tests on LLaMa3.1 models (8B and 70B variants) demonstrate SageMaker’s Scale to Zero feature’s effectiveness, with intentionally conservative scaling times to prevent endpoint thrashing and accommodate spiky traffic patterns.
LLaMa3.1モデル（8Bおよび70Bバリアント）に対するパフォーマンステストは、エンドポイントのスラッシングを防ぎ、スパイキーなトラフィックパターンに対応するために意図的に保守的なスケーリング時間を持つSageMakerのScale to Zero機能の効果を示しています。
For both model sizes, scaling in takes a total of 25 minutes, allowing a 15-minute buffer before initiating scale-down and an additional 10 minutes to fully decommission instances.
両方のモデルサイズにおいて、スケールインには合計25分かかり、スケールダウンを開始する前に15分のバッファを設け、インスタンスを完全に廃止するのに追加で10分かかります。
This cautious approach helps avoid premature scaling during temporary lulls in traffic.
この慎重なアプローチは、一時的なトラフィックの減少中に早期のスケーリングを避けるのに役立ちます。
When scaling out, the 8B model takes about 5 minutes, while the 70B model needs approximately 6 minutes.
スケールアウトする際、8Bモデルは約5分かかり、70Bモデルは約6分必要です。
These times include a 1-minute trigger delay, followed by instance provisioning and model copy instantiation.
これらの時間には1分のトリガー遅延が含まれ、その後にインスタンスのプロビジョニングとモデルコピーのインスタンス化が行われます。
The slightly longer scale-out times, especially for larger models, provide a balance between responsiveness and stability, ensuring the system can handle sudden traffic increases without constantly scaling up and down.
特に大きなモデルにおいては、わずかに長いスケールアウト時間が応答性と安定性のバランスを提供し、システムが突然のトラフィックの増加に対応できるようにし、常にスケールアップとスケールダウンを繰り返すことがないようにします。
This measured approach to scaling helps maintain consistent performance and cost-efficiency in environments with variable workloads.
このようなスケーリングに対する慎重なアプローチは、変動するワークロードを持つ環境において、一貫したパフォーマンスとコスト効率を維持するのに役立ちます。

### Scale up Trials スケールアップ試験

If you want more customization and faster scaling, consider using step scaling to scale model copies instead of target tracking.
より多くのカスタマイズと迅速なスケーリングを望む場合は、ターゲットトラッキングの代わりにステップスケーリングを使用してモデルコピーをスケールアップすることを検討してください。

## Customers testimonials 顧客の証言

The new Scale to Zero feature for SageMaker inference endpoints has sparked considerable interest across customers.
SageMaker推論エンドポイントの新しいScale to Zero機能は、顧客の間でかなりの関心を呼び起こしています。
We gathered initial reactions from companies who have previewed and evaluated this capability, highlighting its potential impact on AI and machine learning operations.
私たちは、この機能をプレビューし評価した企業からの初期反応を集め、そのAIおよび機械学習運用への潜在的な影響を強調しました。

Atlassian, headquartered in Sydney, Australia, is a software company specializing in collaboration tools for software development and project management:
オーストラリアのシドニーに本社を置くAtlassianは、ソフトウェア開発とプロジェクト管理のためのコラボレーションツールを専門とするソフトウェア会社です：
“The new Scale to Zero feature for SageMaker inference strongly aligns with our commitment to efficiency and innovation.
「SageMaker推論の新しいScale to Zero機能は、私たちの効率性と革新へのコミットメントと強く一致しています。
We’re enthusiastic about its potential to revolutionize how we manage our machine learning inference resources, and we look forward to integrating it into our operations”
私たちは、機械学習推論リソースの管理方法を革命的に変える可能性に熱心であり、これを私たちの業務に統合することを楽しみにしています」
– Guarav Awadhwal – Senior Engineering Manager at Atlassian
– Guarav Awadhwal – Atlassianのシニアエンジニアリングマネージャー

iFood is a Latin American online food delivery firm based in Brazil.
iFoodはブラジルに本社を置くラテンアメリカのオンラインフードデリバリー企業です。
It works with over 300,000 restaurants, connecting them with millions of customers every month.
毎月300,000以上のレストランと提携し、数百万の顧客とつなげています。
“The Scale to Zero feature for SageMaker Endpoints will be fundamental for iFood’s Machine Learning Operations.
「SageMakerエンドポイントのScale to Zero機能は、iFoodの機械学習運用にとって基本的なものとなるでしょう。
Over the years, we’ve collaborated closely with the SageMaker team to enhance our inference capabilities.
これまでの数年間、私たちはSageMakerチームと密接に協力して推論能力を向上させてきました。
This feature represents a significant advancement, as it allows us to improve cost efficiency without compromising the performance and quality of our ML services, given that inference constitutes a substantial part of our infrastructure expenses.”
この機能は重要な進展を示しており、推論が私たちのインフラストラクチャ費用の大部分を占めるため、MLサービスのパフォーマンスと品質を損なうことなくコスト効率を向上させることができます。」
– Daniel Vieira, MLOps Engineer Manager at iFood
– Daniel Vieira, iFoodのMLOpsエンジニアマネージャー

VIDA, headquartered in Jakarta, Indonesia, is a leading digital identity provider that enable individuals and business to conduct business in a safe and secure digital environment.
インドネシアのジャカルタに本社を置くVIDAは、個人と企業が安全でセキュアなデジタル環境でビジネスを行うことを可能にする主要なデジタルアイデンティティプロバイダーです。
“SageMaker’s new Scale to Zero feature for GPU inference endpoints shows immense promise for deep fake detection operations.
「SageMakerのGPU推論エンドポイント向けの新しいScale to Zero機能は、ディープフェイク検出操作に対して非常に大きな可能性を示しています。
The potential to efficiently manage our face liveness and document verification inference models while optimizing infrastructure costs aligns perfectly with our goals.
インフラストラクチャコストを最適化しながら、顔の生存確認や文書検証の推論モデルを効率的に管理する可能性は、私たちの目標と完全に一致しています。
We’re excited to leverage this capability to enhance our identity verification solutions.”
私たちは、この機能を活用してアイデンティティ検証ソリューションを強化することに興奮しています。」
– Keshav Sharma, ML Platform Architect at VIDA
– Keshav Sharma, VIDAのMLプラットフォームアーキテクト

APOIDEA Group is a leading AI-focused FinTech ISV company headquartered in Hong Kong.
APOIDEA Groupは、香港に本社を置くAIに焦点を当てた主要なFinTech ISV企業です。
Leveraging cutting-edge generative AI and deep learning technologies, the company develops innovative AI FinTech solutions for multinational banks.
最先端の生成AIと深層学習技術を活用して、同社は多国籍銀行向けの革新的なAI FinTechソリューションを開発しています。
APOIDEA’s products automate repetitive human analysis tasks, extracting valuable financial insights from extensive financial documents to accelerate AI-driven transformation across the industry.
APOIDEAの製品は、繰り返しの人間の分析タスクを自動化し、広範な金融文書から貴重な金融インサイトを抽出して、業界全体のAI駆動の変革を加速します。
“SageMaker’s Scale to Zero feature is a game changer for our AI financial analysis solution in operations.
「SageMakerのScale to Zero機能は、私たちのAI金融分析ソリューションの運用においてゲームチェンジャーです。
It delivers significant cost savings by scaling down endpoints during quiet periods, while maintaining the flexibility we need for batch inference and model testing.
静かな期間中にエンドポイントを縮小することで大幅なコスト削減を実現し、バッチ推論やモデルテストに必要な柔軟性を維持します。
This capability is transforming how we manage our GenAI workloads and evaluate new models.
この機能は、私たちのGenAIワークロードの管理方法と新しいモデルの評価方法を変革しています。
We’re eager to harness its power to further optimize our deep learning and NLP model deployments.”
私たちは、この機能の力を活用して、深層学習とNLPモデルの展開をさらに最適化することを楽しみにしています。」
– Mickey Yip, VP of Product at APOIDEA Group
– Mickey Yip, APOIDEA Groupの製品担当副社長

Fortiro, based in Melbourne, Australia, is a FinTech company specializing in automated document fraud detection and financial verification for trusted financial institutions.
オーストラリアのメルボルンに本社を置くFortiroは、信頼できる金融機関向けの自動文書詐欺検出と金融検証を専門とするFinTech企業です。
“The new Scale-to-Zero capability in SageMaker is a game-changer for our MLOps and delivers great cost savings.
「SageMakerの新しいScale-to-Zero機能は、私たちのMLOpsにとってゲームチェンジャーであり、大きなコスト削減を実現します。
Being able to easily scale inference endpoints and GPUs means we can take advantage of a fast, highly responsive environment, without incurring unnecessary costs.
推論エンドポイントとGPUを簡単にスケールできることは、不要なコストをかけることなく、迅速で高い応答性のある環境を活用できることを意味します。
Our R&D teams constantly experiment with new AI-based document fraud detection methods, which involves a lot of testing and repeating.
私たちのR&Dチームは、新しいAIベースの文書詐欺検出方法を常に実験しており、多くのテストと繰り返しを伴います。
This capability empowers us to do this both faster and more efficiently.”
この機能は、私たちがこれをより早く、より効率的に行うことを可能にします。」
– Amir Vahid, Chief Technology Officer at Fortiro
– Amir Vahid, Fortiroの最高技術責任者

These testimonials underscore the anticipation for SageMaker’s Scale to Zero feature.
これらの証言は、SageMakerのScale to Zero機能への期待を強調しています。
As organizations begin to implement this capability, we expect to see innovative applications that balance cost efficiency with performance in machine learning deployments.
組織がこの機能を実装し始めると、コスト効率とパフォーマンスのバランスを取った革新的なアプリケーションが見られることを期待しています。

## Conclusion 結論

In this post, we introduced the new scale to zero feature in SageMaker, an innovative capability that enables you to optimize costs by automatically scaling in your inference endpoints when they’re not in use.
本稿では、SageMakerの新しいスケール・トゥ・ゼロ機能を紹介しました。この革新的な機能は、推論エンドポイントが使用されていないときに自動的にスケールダウンすることでコストを最適化することを可能にします。

We guided you through the detailed process of implementing this feature, including configuring endpoints, setting up auto scaling policies, and managing inference components for both automatic and scheduled scaling scenarios.
この機能を実装するための詳細なプロセス、エンドポイントの設定、自動スケーリングポリシーの設定、そして自動およびスケジュールされたスケーリングシナリオのための推論コンポーネントの管理について説明しました。

This cost-saving functionality presents new possibilities for how you can approach your ML operations.
このコスト削減機能は、機械学習（ML）オペレーションへのアプローチに新たな可能性をもたらします。

With this feature, you can closely align your compute resource usage with actual needs, potentially reducing costs during periods of low demand.
この機能を使用することで、コンピューティングリソースの使用を実際のニーズに密接に合わせることができ、需要が低い期間中のコストを削減する可能性があります。

We encourage you to try this capability and start optimizing your SageMaker inference costs today.
この機能を試し、今日からSageMakerの推論コストを最適化することをお勧めします。

To help you get started quickly, we’ve prepared a comprehensive notebooks containing an end-to-end example of how to configure an endpoint to scale to zero.
迅速に始められるように、エンドポイントをスケール・トゥ・ゼロに設定する方法のエンドツーエンドの例を含む包括的なノートブックを用意しました。

We encourage you to try this capability and start optimizing your SageMaker inference costs today!
この機能を試し、今日からSageMakerの推論コストを最適化することをお勧めします！

### About the authors 著者について

Marc Karpis an ML Architect with the Amazon SageMaker Service team.
Marc Karpisは、Amazon SageMakerサービスチームのMLアーキテクトです。
He focuses on helping customers design, deploy, and manage ML workloads at scale.
彼は、顧客が大規模なMLワークロードを設計、展開、管理するのを支援することに注力しています。
In his spare time, he enjoys traveling and exploring new places.
余暇には、旅行や新しい場所の探索を楽しんでいます。

Christian Kamwangalais an AI/ML and Generative AI Specialist Solutions Architect at AWS, based in Paris, France.
Christian Kamwangalaは、フランス・パリに拠点を置くAWSのAI/MLおよび生成AIスペシャリストソリューションアーキテクトです。
He helps enterprise customers architect and implement cutting-edge AI solutions using AWS’s comprehensive suite of tools, with a focus on production-ready systems that follow industry best practices.
彼は、業界のベストプラクティスに従った生産準備が整ったシステムに焦点を当て、AWSの包括的なツール群を使用して企業顧客が最先端のAIソリューションを設計し、実装するのを支援しています。
In his spare time, Christian enjoys exploring nature and spending time with family and friends.
余暇には、自然を探索したり、家族や友人と過ごすことを楽しんでいます。

Saurabh Trikandeis a Senior Product Manager for Amazon Bedrock and SageMaker Inference.
Saurabh Trikandeは、Amazon BedrockおよびSageMaker Inferenceのシニアプロダクトマネージャーです。
He is passionate about working with customers and partners, motivated by the goal of democratizing AI.
彼は、AIの民主化を目指して顧客やパートナーと協力することに情熱を注いでいます。
He focuses on core challenges related to deploying complex AI applications, inference with multi-tenant models, cost optimizations, and making the deployment of Generative AI models more accessible.
彼は、複雑なAIアプリケーションの展開、多テナントモデルによる推論、コスト最適化、生成AIモデルの展開をよりアクセスしやすくすることに関連する主要な課題に焦点を当てています。
In his spare time, Saurabh enjoys hiking, learning about innovative technologies, following TechCrunch, and spending time with his family.
余暇には、ハイキングや革新的な技術について学ぶこと、TechCrunchをフォローすること、家族と過ごすことを楽しんでいます。

Raghu Rameshais a Senior GenAI/ML Solutions Architect on the Amazon SageMaker Service team.
Raghu Rameshは、Amazon SageMakerサービスチームのシニアGenAI/MLソリューションアーキテクトです。
He focuses on helping customers build, deploy, and migrate ML production workloads to SageMaker at scale.
彼は、顧客が大規模にMLプロダクションワークロードをSageMakerに構築、展開、移行するのを支援することに注力しています。
He specializes in machine learning, AI, and computer vision domains, and holds a master’s degree in computer science from UT Dallas.
彼は、機械学習、AI、コンピュータビジョンの分野を専門としており、UTダラスでコンピュータサイエンスの修士号を取得しています。
In his free time, he enjoys traveling and photography.
自由な時間には、旅行や写真撮影を楽しんでいます。

Melanie Li, PhD, is a Senior Generative AI Specialist Solutions Architect at AWS based in Sydney, Australia, where her focus is on working with customers to build solutions leveraging state-of-the-art AI and machine learning tools.
Melanie Li博士は、オーストラリア・シドニーに拠点を置くAWSのシニア生成AIスペシャリストソリューションアーキテクトであり、最先端のAIおよび機械学習ツールを活用したソリューションを顧客と共に構築することに注力しています。
She has been actively involved in multiple Generative AI initiatives across APJ, harnessing the power of Large Language Models (LLMs).
彼女は、APJ全体で複数の生成AIイニシアチブに積極的に関与し、大規模言語モデル（LLMs）の力を活用しています。
Prior to joining AWS, Dr. Li held data science roles in the financial and retail industries.
AWSに入社する前、Li博士は金融および小売業界でデータサイエンスの役割を担っていました。

Raj Vippaguntais a Principal Engineer at Amazon SageMaker Machine Learning(ML) platform team in AWS.
Raj Vippaguntaは、AWSのAmazon SageMaker機械学習（ML）プラットフォームチームのプリンシパルエンジニアです。
He uses his vast experience of 18+ years in large-scale distributed systems and his passion for machine learning to build practical service offerings in the AI and ML space.
彼は、18年以上の大規模分散システムにおける豊富な経験と機械学習への情熱を活かして、AIおよびML分野で実用的なサービス提供を構築しています。
He has helped build various at-scale solutions for AWS and Amazon.
彼は、AWSおよびAmazonのためにさまざまな大規模ソリューションの構築を支援してきました。
In his spare time, he likes reading books, pursue long distance running and exploring new places with his family.
余暇には、読書や長距離ランニングを楽しんだり、家族と新しい場所を探索することが好きです。

### Resources リソース

### Blog Topics ブログのトピック

### Follow フォロー

### Learn About AWS AWSについて学ぶ

### Resources for AWS AWSのリソース

### Developers on AWS AWS上の開発者

### Help ヘルプ
