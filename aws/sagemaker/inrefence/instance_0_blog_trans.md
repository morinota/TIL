# 1. Unlock cost savings with the new scale down to zero feature in SageMaker Inference SageMaker推論における新しいゼロスケールダウン機能でコスト削減を実現

Today at AWS re:Invent 2024, we are excited to announce a new feature for Amazon SageMaker inference endpoints: the ability to scale SageMaker inference endpoints to zero instances.
2024年のAWS re:Inventで、私たちはAmazon SageMaker推論エンドポイントの新機能、すなわち**SageMaker推論エンドポイントをゼロインスタンスにスケールダウンする機能**を発表できることを嬉しく思います。

This long-awaited capability is a game changer for our customers using the power of AI and machine learning (ML) inference in the cloud.
この待望の機能は、クラウドにおけるAIおよび機械学習（ML）推論の力を利用する顧客にとって、ゲームチェンジャーとなります。

Previously, SageMaker inference endpoints maintained a minimum number of instances to provide continuous availability, even during periods of low or no traffic.
以前は、SageMaker推論エンドポイントは、**トラフィックが少ないまたは全くない期間でも継続的な可用性を提供するため**に、最小限のインスタンス数を維持していました。
(それはそう。インスタンス数0だとコールドスタートはどうしても発生するだろうし...:thinking:)

With this update, available when using SageMaker inference components, you have more options to align your resource usage with your specific needs and traffic patterns.
この更新により、**SageMaker推論コンポーネントを使用する際に、リソース使用を特定のニーズやトラフィックパターンに合わせるための選択肢が増えました**。

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
これにより、**スケーリングポリシーをゼロスケールダウンを含むように設定でき**、AI推論インフラストラクチャのより正確な管理が可能になります。

The scale down to zero feature presents new opportunities for how businesses can approach their cloud-based ML operations.
ゼロスケールダウン機能は、企業がクラウドベースのMLオペレーションにアプローチする新しい機会を提供します。

It provides additional options for managing resources across various scenarios, from development and testing environments to production deployments with variable traffic patterns.
**開発およびテスト環境から、変動するトラフィックパターンを持つ本番展開に至るまで**、さまざまなシナリオでリソースを管理するための追加オプションを提供します。

As with any new feature, you are encouraged to carefully evaluate how it fits into your overall architecture and operational needs, considering factors such as response times and the specific requirements of your applications.
新機能と同様に、応答時間やアプリケーションの特定の要件などの要素を考慮しながら、全体のアーキテクチャや運用ニーズにどのように適合するかを慎重に評価することをお勧めします。

In this post, we explore the new scale to zero feature for SageMaker inference endpoints, demonstrating how to implement and use this capability to optimize costs and manage resources more effectively.
この記事では、SageMaker推論エンドポイントの新しいゼロスケールダウン機能を探求し、コストを最適化し、リソースをより効果的に管理するためにこの機能を実装し使用する方法を示します。

We cover the key scenarios where scaling to zero is beneficial, provide best practices for optimizing scale-up time, and walk through the step-by-step process of implementing this functionality.
**ゼロスケールダウンが有益になる主要なシナリオ**をカバーし、スケールアップ時間を最適化するためのベストプラクティスを提供し、この機能を実装するためのステップバイステップのプロセスを説明します。

Additionally, we discuss how to set up scheduled scaling actions for predictable traffic patterns and test the behavior of your scaled-to-zero endpoints.
さらに、予測可能なトラフィックパターンのためのスケジュールされたスケーリングアクションの設定方法と、ゼロにスケールダウンしたエンドポイントの動作をテストする方法についても説明します。

<!-- ここまで読んだ -->

## 1.1. Determining when to scale to zero ゼロスケールのタイミングの決定

Before we dive into the implementation details of the new scale to zero feature, it’s crucial to understand when and why you should consider using it.
新しいゼロスケール機能の実装詳細に入る前に、いつ、なぜそれを使用するべきかを理解することが重要です。

Although the ability to scale SageMaker inference endpoints to zero instances offers significant cost-saving potential, it’s crucial to understand when and how to apply this feature effectively.
SageMaker推論エンドポイントをゼロインスタンスにスケールダウンする能力は、重要なコスト削減の可能性を提供しますが、この機能を効果的に適用するタイミングと方法を理解することが重要です。

Not all scenarios benefit equally from scaling to zero, and in some cases, it may even impact the performance of your applications.
**すべてのシナリオがゼロスケールから同じように利益を得るわけではなく、場合によってはアプリケーションのパフォーマンスに影響を与えることさえあります**。(うんうん)

Let’s explore why it’s important to carefully consider when to implement this feature and how to identify the scenarios where it provides the most value.
この機能を実装するタイミングを慎重に考慮することがなぜ重要であり、最も価値を提供するシナリオを特定する方法を探っていきましょう。

The ability to scale SageMaker inference endpoints to zero instances is particularly beneficial in three key scenarios:
SageMaker推論エンドポイントをゼロインスタンスにスケールダウンする能力は、**特に3つの重要なシナリオで有益**です。

- 1. **Predictable traffic patterns** – If your inference traffic is predictable and follows a consistent schedule, you can use this scaling functionality to automatically scale down to zero during periods of low or no usage. This eliminates the need to manually delete and recreate inference components and endpoints.
  - もしあなたの推論トラフィックが予測可能で一貫したスケジュールに従う場合、このスケーリング機能を使用して、使用量が少ないまたは全くない期間に自動的にゼロにスケールダウンすることができます。これにより、推論コンポーネントとエンドポイントを手動で削除して再作成する必要がなくなります。
- 2. **Sporadic or variable traffic** – For applications that experience sporadic or variable inference traffic patterns, scaling down to zero instances can provide significant cost savings. However, scaling from zero instances back up to serving traffic is not instantaneous. During the scale-out process, any requests sent to the endpoint will fail, and these NoCapacityInvocationFailures will be captured in Amazon CloudWatch.
  - スポラディックまたは変動するトラフィック – スポラディックまたは変動する推論トラフィックパターンを経験するアプリケーションの場合、ゼロインスタンスにスケールダウンすることで、大幅なコスト削減が可能です。ただし、ゼロインスタンスからトラフィックを提供するためにスケールアップすることは即座に行われるわけではありません。**スケールアウトプロセス中にエンドポイントに送信されたリクエストはすべて失敗**し、これらの `NoCapacityInvocationFailures` はAmazon CloudWatchでキャプチャされます。
- 3. **Development and testing environments** – The scale to zero functionality is also beneficial when testing and evaluating new ML models. During model development and experimentation, you might create temporary inference endpoints to test different configurations. However, it’s possible to forget to delete these endpoints when you’re done. Scaling down to zero makes sure these test endpoints automatically scale back to zero instances when not in use, preventing unwanted charges. This allows you to freely experiment without closely monitoring infrastructure usage or remembering to manually delete endpoints. The automatic scaling to zero provides a cost-effective way to test out ideas and iterate on your ML solutions
  - 開発およびテスト環境 – スケールゼロ機能は、新しいMLモデルをテストおよび評価する際にも有益です。モデルの開発と実験中に、異なる構成をテストするために一時的な推論エンドポイントを作成することがあります。ただし、完了したらこれらのエンドポイントを削除し忘れる可能性があります。ゼロにスケールダウンすることで、これらのテストエンドポイントが使用されていないときに自動的にゼロインスタンスにスケールバックすることができ、不要な料金が発生するのを防ぎます。これにより、インフラストラクチャの使用状況を密接に監視する必要がなく、エンドポイントを手動で削除することを覚えておく必要がなくなります。ゼロへの自動スケーリングは、アイデアをテストし、MLソリューションを繰り返し実行するための費用対効果の高い方法を提供します。

By carefully evaluating your specific use case against these scenarios, you can make informed decisions about implementing scale to zero functionality.
これらのシナリオに対して特定のユースケースを慎重に評価することで、ゼロスケール機能の実装に関する情報に基づいた決定を下すことができます。

This approach makes sure you maximize cost savings without compromising on the performance and availability requirements of your ML applications.
このアプローチは、MLアプリケーションのパフォーマンスと可用性の要件を損なうことなく、コスト削減を最大化することを保証します。

It’s important to note that although scaling to zero can provide significant benefits, it also introduces a trade-off in terms of initial response time when scaling back up.
**ゼロスケールが重要な利点を提供できる一方で、スケールアップ時の初期応答時間に関するトレードオフも生じることに注意が必要**です。(うんうん...!)

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
**ゼロインスタンスからトラフィックを提供するためにスケールアップすることは、アプリケーションの応答性に影響を与える可能性のある短い遅延（コールドスタート）を引き起こし**ます。
(インスタンス台数を0から1にすることは、「スケールアウト」ではなく「スケールアップ」って表現されるのか...!:thinking:)

To mitigate this, we first explore best practices for minimizing scale-up time.
これを軽減するために、**まずスケールアップ時間を最小限に抑えるためのベストプラクティス**を探ります。

Then we walk through the step-by-step process of implementing the scale to zero functionality for your SageMaker inference endpoints.
次に、SageMaker推論エンドポイントのゼロスケール機能を実装するためのステップバイステップのプロセスを説明します。

<!-- ここまで読んだ -->

## 1.2. Optimizing scale-up time best practices スケールアップ時間最適化のベストプラクティス

When using the scale to zero feature, it’s crucial to minimize the time it takes for your endpoint to scale up and begin serving requests.
スケールゼロ機能を使用する際には、エンドポイントがスケールアップしてリクエストを処理し始めるまでの時間を最小限に抑えることが重要です。
The following are several best practices you can implement to decrease the scale-out time for your SageMaker inference endpoints:
以下は、**SageMaker推論エンドポイントのスケールアウト時間を短縮するために実装できるいくつかのベストプラクティス**です：

### 1.2.1. Decrease model or container download time モデルまたはコンテナのダウンロード時間を短縮する

Use uncompressed model format to reduce the time it takes to download the model artifacts when scaling up
スケールアップ時にモデルアーティファクトをダウンロードする時間を短縮するために、非圧縮モデル形式を使用します。
Compressed model files may save storage space, but they require additional time to uncompress and files can’t be downloaded in parallel, which can slow down the scale-up process.
圧縮されたモデルファイルはストレージスペースを節約できますが、解凍に追加の時間がかかり、ファイルは並行してダウンロードできないため、スケールアッププロセスが遅くなる可能性があります。
To learn more, see Supercharge your auto scaling for generative AI inference – Introducing Container Caching in SageMaker Inference.
詳細については、「生成AI推論のための自動スケーリングを強化する – SageMaker Inferenceにおけるコンテナキャッシングの導入」を参照してください。

<!-- ここまで読んだ!! -->

### 1.2.2. Reduce model server startup time モデルサーバーの起動時間を短縮する

Look for ways to optimize the startup and initialization of your model server container.
モデルサーバーコンテナの起動と初期化を最適化する方法を探ります。
This could include techniques like building in packages into the image, using multi-threading, or minimizing unnecessary initialization steps.
これには、イメージにパッケージを組み込む、マルチスレッドを使用する、または不要な初期化ステップを最小限に抑えるといった技術が含まれます。
For more details, see Introducing Fast Model Loader in SageMaker Inference: Accelerate autoscaling for your Large Language Models (LLMs) – part 1.
詳細については、「SageMaker Inferenceにおけるファストモデルローダーの導入：大規模言語モデル（LLM）の自動スケーリングを加速する – パート1」を参照してください。

<!-- ここまで読んだ -->

### 1.2.3. Use faster auto scaling metrics より高速な自動スケーリングメトリクスを使用する

(これは、スケールアウト/イン時のタイミングを判断するmetricsの選択の話っぽい??:thinking:)

Take advantage of more granular auto scaling metrics like ConcurrentRequestsPerCopy to more accurately monitor and react to changes in inference traffic.
ConcurrentRequestsPerCopyのようなより詳細な自動スケーリングメトリクスを活用して、推論トラフィックの変化をより正確に監視し、反応します。
These sub-minute metrics can help trigger scale-out actions more precisely, reducing the number of NoCapacityInvocationFailures your users might experience.
これらのサブミニットメトリクスは、スケールアウトアクションをより正確にトリガーするのに役立ち、ユーザーが経験する可能性のあるNoCapacityInvocationFailuresの数を減少させます。
For more information, see Amazon SageMaker inference launches faster auto scaling for generative AI models.
詳細については、「Amazon SageMaker推論が生成AIモデルのためのより迅速な自動スケーリングを開始」を参照してください。

<!-- ここまで読んだ -->

### 1.2.4. Handle failed requests 失敗したリクエストを処理する

When scaling from zero instances, there will be a brief period where requests fail due to NoCapacityInvocationFailures because SageMaker provisions resources.
ゼロインスタンスからスケールアップする際、SageMakerがリソースをプロビジョニングするため、リクエストがNoCapacityInvocationFailuresにより失敗する短い期間があります。
To handle this, you can use queues or implement client-side retries:
これを処理するために、**キューを使用するか、クライアント側の再試行**を実装できます：

#### 1.2.4.1. Use a serverless queue like Amazon Simple Queue Service (Amazon SQS) to buffer requests during scale-out

Amazon Simple Queue Service（Amazon SQS）のようなサーバーレスキューを使用して、スケールアウト中にリクエストをバッファリングします。
When a failure occurs, enqueue the request and dequeue after the model copies have scaled up from zero.
失敗が発生した場合、リクエストをキューに入れ、モデルコピーがゼロからスケールアップした後にデキューします。

#### 1.2.4.2. Alternatively, have your client reject failed requests, but then retry after some time after the model copies have scaled

あるいは、クライアントに失敗したリクエストを拒否させ、その後モデルコピーがスケールした後に再試行させることもできます。
You can retrieve the number of copies of an inference component at any time by making the DescribeInferenceComponent API call and checking the CurrentCopyCount.
`DescribeInferenceComponent` APIコールを行い、CurrentCopyCountを確認することで、推論コンポーネントのコピー数をいつでも取得できます。
This allows time for the model copies to scale out from zero, transparently handling the transition for end-users.
これにより、モデルコピーがゼロからスケールアウトするための時間が確保され、エンドユーザーに対する移行が透過的に処理されます。

---

By implementing these best practices, you can help make sure your SageMaker inference endpoints can scale out quickly and efficiently to meet changes in traffic, providing a responsive and reliable experience for your end-users.
これらのベストプラクティスを実装することで、SageMaker推論エンドポイントがトラフィックの変化に迅速かつ効率的にスケールアウトできるようにし、エンドユーザーに対して応答性が高く信頼性のある体験を提供できます。

<!-- ここまで読んだ -->

## 1.3. Solution overview ソリューションの概要

With these best practices in mind, let’s now walk through the process of enabling your SageMaker inference endpoints to scale down to zero instances.
これらのベストプラクティスを念頭に置いて、SageMaker推論エンドポイントをゼロインスタンスにスケールダウンするプロセスを見ていきましょう。

This process involves a few key steps that are crucial for optimizing your endpoint’s performance and cost-efficiency:
このプロセスには、エンドポイントのパフォーマンスとコスト効率を最適化するために重要な数ステップが含まれています。

- Configure your endpoint– The first and most critical step is to enable managed instance scaling for your SageMaker endpoint.
- エンドポイントの設定– 最初で最も重要なステップは、SageMakerエンドポイントのためにマネージドインスタンススケーリングを有効にすることです。

This is the foundational action that allows you to implement advanced scaling features, including scaling to zero.
これは、ゼロへのスケーリングを含む高度なスケーリング機能を実装するための基盤となるアクションです。

By enabling managed instance scaling, you’re creating an inference component endpoint, which is essential for the fine-grained control over scaling behaviors we discuss later in this post.
マネージドインスタンススケーリングを有効にすることで、後でこの投稿で説明するスケーリング動作の詳細な制御に不可欠な推論コンポーネントエンドポイントを作成します。

After you configure managed instance scaling, you then configure the SageMaker endpoint to set the MinInstanceCount parameter to 0.
マネージドインスタンススケーリングを設定した後、SageMakerエンドポイントを設定して、MinInstanceCountパラメータを0に設定します。

This parameter allows the endpoint to scale all the way down to zero instances when not in use, maximizing cost-efficiency.
このパラメータにより、エンドポイントは使用されていないときにゼロインスタンスまでスケールダウンでき、コスト効率を最大化します。

Enabling managed instance scaling and setting MinInstanceCount to 0 work together to provide a highly flexible and cost-effective endpoint configuration.
マネージドインスタンススケーリングを有効にし、MinInstanceCountを0に設定することで、非常に柔軟でコスト効果の高いエンドポイント構成を提供します。

However, scaling up from zero will introduce cold starts, potentially impacting response times for initial requests after periods of inactivity.
ただし、ゼロからスケールアップするとコールドスタートが発生し、非アクティブ期間後の初回リクエストの応答時間に影響を与える可能性があります。

The inference component endpoint created through managed instance scaling serves as the foundation for implementing the sophisticated scaling policies we explore in the next step.
マネージドインスタンススケーリングを通じて作成された推論コンポーネントエンドポイントは、次のステップで探求する高度なスケーリングポリシーを実装するための基盤となります。

- Define scaling policies– Next, you need to create two scaling policies that work in tandem to manage the scaling behavior of your endpoint effectively:
- スケーリングポリシーの定義– 次に、エンドポイントのスケーリング動作を効果的に管理するために連携して機能する2つのスケーリングポリシーを作成する必要があります：

Scaling policy for inference component copies– This target tracking scaling policy will manage the scaling of your inference component copies.
推論コンポーネントコピーのためのスケーリングポリシー– このターゲットトラッキングスケーリングポリシーは、推論コンポーネントコピーのスケーリングを管理します。

It’s a dynamic policy that adjusts the number of copies based on a specified metric, such as CPU utilization or request count.
これは、CPU使用率やリクエスト数などの指定されたメトリックに基づいてコピーの数を調整する動的ポリシーです。

The policy is designed to scale the copy count to zero when there is no traffic, making sure you’re not paying for unused resources.
このポリシーは、トラフィックがないときにコピー数をゼロにスケールダウンするように設計されており、未使用のリソースに対して支払わないようにします。

Conversely, it will scale back up to your desired capacity when needed, allowing your endpoint to handle incoming requests efficiently.
逆に、必要に応じて希望の容量までスケールアップし、エンドポイントが受信リクエストを効率的に処理できるようにします。

When configuring this policy, you need to carefully choose the target metric and threshold that best reflect your workload patterns and performance requirements.
このポリシーを設定する際には、ワークロードパターンとパフォーマンス要件を最もよく反映するターゲットメトリックとしきい値を慎重に選択する必要があります。

Scale out from zero policy– This policy is crucial for enabling your endpoint to scale out from zero model copies when traffic arrives.
ゼロからのスケールアウトポリシー– このポリシーは、トラフィックが到着したときにエンドポイントがゼロのモデルコピーからスケールアウトできるようにするために重要です。

It’s implemented as a step scaling policy that adds model copies when triggered by incoming requests.
これは、受信リクエストによってトリガーされるとモデルコピーを追加するステップスケーリングポリシーとして実装されています。

This allows SageMaker to provision the necessary instances to support the model copies and handle the incoming traffic.
これにより、SageMakerはモデルコピーをサポートし、受信トラフィックを処理するために必要なインスタンスをプロビジョニングできます。

When configuring this policy, you need to consider factors such as the expected traffic patterns, the desired responsiveness of your endpoint, and the potential cold start latency.
このポリシーを設定する際には、予想されるトラフィックパターン、エンドポイントの望ましい応答性、および潜在的なコールドスタートのレイテンシを考慮する必要があります。

You may want to set up multiple steps in your policy to handle different levels of incoming traffic more granularly.
異なるレベルの受信トラフィックをより詳細に処理するために、ポリシーに複数のステップを設定することを検討するかもしれません。

By implementing these scaling policies, you create a flexible and cost-effective infrastructure that can automatically adjust to your workload demands and scale to zero when needed.
これらのスケーリングポリシーを実装することで、ワークロードの要求に自動的に調整し、必要に応じてゼロにスケールダウンできる柔軟でコスト効果の高いインフラストラクチャを作成します。

Now let’s see how to use this feature step by step.
では、この機能をステップバイステップで使用する方法を見ていきましょう。

## 1.4. Set up your endpoint エンドポイントの設定

The first crucial step in enabling your SageMaker endpoint to scale to zero is properly configuring the endpoint and its associated components.
SageMakerエンドポイントをゼロにスケールさせるための最初の重要なステップは、エンドポイントとその関連コンポーネントを適切に構成することです。

This process involves three main steps:
このプロセスは、主に3つのステップで構成されています。

1. Create the endpoint configuration and set `MinInstanceCount` to 0.
   エンドポイント構成を作成し、`MinInstanceCount`を0に設定します。
   This allows the endpoint to scale down all the way to zero instances when not in use.
   これにより、エンドポイントは使用されていないときにインスタンスをゼロまでスケールダウンできます。

   ```python
   sagemaker_client.create_endpoint_config(
       EndpointConfigName=endpoint_config_name,
       ExecutionRoleArn=role,
       ProductionVariants=[{
           "VariantName": variant_name,
           "InstanceType": instance_type,
           "InitialInstanceCount": 1,
           "ModelDataDownloadTimeoutInSeconds": model_data_download_timeout_in_seconds,
           "ContainerStartupHealthCheckTimeoutInSeconds": container_startup_health_check_timeout_in_seconds,
           "ManagedInstanceScaling": {
               "Status": "ENABLED",
               "MinInstanceCount": 0,
               "MaxInstanceCount": max_instance_count,
           },
           "RoutingConfig": {
               "RoutingStrategy": "LEAST_OUTSTANDING_REQUESTS"
           },
       }],
   )
   ```

2. Create the SageMaker endpoint:
   SageMakerエンドポイントを作成します。

   ```python
   sagemaker_client.create_endpoint(
       EndpointName=endpoint_name,
       EndpointConfigName=endpoint_config_name,
   )
   ```

3. Create the inference component for your endpoint:
   エンドポイントの推論コンポーネントを作成します。

   ```python
   sagemaker_client.create_inference_component(
       InferenceComponentName=inference_component_name,
       EndpointName=endpoint_name,
       VariantName=variant_name,
       Specification={
           "ModelName": model_name,
           "StartupParameters": {
               "ModelDataDownloadTimeoutInSeconds": 3600,
               "ContainerStartupHealthCheckTimeoutInSeconds": 3600,
           },
           "ComputeResourceRequirements": {
               "MinMemoryRequiredInMb": 1024,
               "NumberOfAcceleratorDevicesRequired": 1,
           },
       },
       RuntimeConfig={
           "CopyCount": 1,
       },
   )
   ```

## 1.5. Add scaling policies スケーリングポリシーの追加

After the endpoint is deployed and InService, you can add the necessary scaling policies:
エンドポイントがデプロイされ、InService（サービス中）になった後、必要なスケーリングポリシーを追加できます：

- Atarget tracking policy that can scale down the copy count for our inference component model copies to zero, and from 1 to n
  - モデルコピーのコピー数をゼロにスケールダウンし、1からnまでスケールアップできるターゲットトラッキングポリシー
- A step scaling policy that will allow the endpoint to scale up from zero
  - エンドポイントがゼロからスケールアップできるステップスケーリングポリシー

### 1.5.1. Scaling policy for inference components model copies 推論コンポーネントモデルコピーのスケーリングポリシー

After you create your SageMaker endpoint and inference components, you register a new auto scaling target for Application Auto Scaling.
SageMakerエンドポイントと推論コンポーネントを作成した後、Application Auto Scalingのために新しい自動スケーリングターゲットを登録します。

In the following code block, you set MinCapacity to 0, which is required for your endpoint to scale down to zero:
以下のコードブロックでは、MinCapacityを0に設定します。これは、エンドポイントがゼロにスケールダウンするために必要です。

```
# Register scalable target
resource_id=f"inference-component/{inference_component_name}"
service_namespace="sagemaker"
scalable_dimension="sagemaker:inference-component:DesiredCopyCount"
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
この設定は、モデルごとの同時リクエスト数が5に達するかそれを超えたときに、自動スケーリングシステムに容量を増加させるよう指示します。

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
スケーリングアクションをトリガーするまでの時間は通常、これらの分数よりも1〜2分長くなります。これは、エンドポイントがCloudWatchにメトリクスを公開するのに時間がかかり、AutoScalingが反応するのにも時間がかかるためです。

### 1.5.2. Scale out from zero model copies policy ゼロモデルコピーからのスケールアウトポリシー

To enable your endpoint to scale out from zero instances, complete the following steps:
エンドポイントがゼロインスタンスからスケールアウトできるようにするために、以下の手順を完了してください。

1. Create a step scaling policy that defines when and how to scale out from zero.
   ゼロからスケールアウトするタイミングと方法を定義するステップスケーリングポリシーを作成します。
   This policy will add one model copy when triggered, enabling SageMaker to provision the instances required to handle incoming requests after being idle.
   このポリシーは、トリガーされたときに1つのモデルコピーを追加し、SageMakerがアイドル状態の後に受信リクエストを処理するために必要なインスタンスをプロビジョニングできるようにします。
   The following code shows you how to define a step scaling policy.
   以下のコードは、ステップスケーリングポリシーを定義する方法を示しています。
   Here we have configured to scale from zero to one model copy ("ScalingAdjustment": 1).
   ここでは、ゼロから1つのモデルコピーにスケールするように設定しています（"ScalingAdjustment": 1）。
   Depending on your use case, you can adjust ScalingAdjustment as required.
   使用ケースに応じて、ScalingAdjustmentを必要に応じて調整できます。

   ```python
   aas_client.put_scaling_policy(PolicyName="inference-component-step-scaling-policy",PolicyType="StepScaling",ServiceNamespace=service_namespace,ResourceId=resource_id,ScalableDimension=scalable_dimension,StepScalingPolicyConfiguration={"AdjustmentType":"ChangeInCapacity","MetricAggregationType":"Maximum","Cooldown":60,"StepAdjustments":[{"MetricIntervalLowerBound":0,"ScalingAdjustment":1# you need to adjust this value based on your use case}]},)
   ```

2. Create a CloudWatch alarm with the metric NoCapacityInvocationFailures.
   メトリック NoCapacityInvocationFailures を使用して CloudWatch アラームを作成します。

   ```python
   aas_client.put_scaling_policy(PolicyName="inference-component-step-scaling-policy",PolicyType="StepScaling",ServiceNamespace=service_namespace,ResourceId=resource_id,ScalableDimension=scalable_dimension,StepScalingPolicyConfiguration={"AdjustmentType":"ChangeInCapacity","MetricAggregationType":"Maximum","Cooldown":60,"StepAdjustments":[{"MetricIntervalLowerBound":0,"ScalingAdjustment":1# you need to adjust this value based on your use case}]},)
   ```

   When triggered, the alarm initiates the previously defined scaling policy.
   トリガーされると、アラームは以前に定義したスケーリングポリシーを開始します。
   For more information about the NoCapacityInvocationFailures metric, see documentation.
   NoCapacityInvocationFailures メトリックの詳細については、ドキュメントを参照してください。
   We have also set the following:
   また、以下の設定も行いました：
   - EvaluationPeriods to 1
   - DatapointsToAlarm to 1
   - ComparisonOperator to GreaterThanOrEqualToThreshold
   これにより、エンドポイントが単一のリクエストを受信した後、ステップスケーリングポリシーがトリガーされるまで約1分待機します。

   ```python
   cw_client.put_metric_alarm(AlarmName='ic-step-scaling-policy-alarm',AlarmActions=<step_scaling_policy_arn>,# Replace with your actual ARNMetricName='NoCapacityInvocationFailures',Namespace='AWS/SageMaker',Statistic='Maximum',Dimensions=[{'Name':'InferenceComponentName','Value':inference_component_name# Replace with actual InferenceComponentName}],Period=30,EvaluationPeriods=1,DatapointsToAlarm=1,Threshold=1,ComparisonOperator='GreaterThanOrEqualToThreshold',TreatMissingData='missing')
   ```

   Replace <STEP_SCALING_POLICY_ARN> with the Amazon Resource Name (ARN) of the scaling policy you created in the previous step.
   <STEP_SCALING_POLICY_ARN> を、前のステップで作成したスケーリングポリシーの Amazon リソース名 (ARN) に置き換えます。
   Notice the "MinInstanceCount": 0 setting in the endpoint configuration, which allows the endpoint to scale down to zero instances.
   エンドポイント構成の "MinInstanceCount": 0 設定に注意してください。これにより、エンドポイントはゼロインスタンスにスケールダウンできます。
   With the scaling policy, CloudWatch alarm, and minimum instances set to zero, your SageMaker inference endpoint will now be able to automatically scale down to zero instances when not in use.
   スケーリングポリシー、CloudWatch アラーム、および最小インスタンスがゼロに設定されていることで、SageMaker 推論エンドポイントは、使用されていないときに自動的にゼロインスタンスにスケールダウンできるようになります。

## 1.6. Test the solution 解決策のテスト

When our SageMaker endpoint doesn’t receive requests for 15 minutes, it will automatically scale down to zero the number of model copies:
私たちのSageMakerエンドポイントが15分間リクエストを受け取らない場合、モデルのコピーの数は自動的にゼロにスケールダウンします。

```
time.sleep(500)whileTrue:desc=sagemaker_client.describe_inference_component(InferenceComponentName=inference_component_name)status=desc["InferenceComponentStatus"]print(status)sys.stdout.flush()ifstatusin["InService","Failed"]:breaktime.sleep(30)desc=sagemaker_client.describe_inference_component(InferenceComponentName=inference_component_name)print(desc)
```

After 10 additional minutes of inactivity, SageMaker automatically stops all underlying instances of the endpoint, eliminating all associated instance costs.
さらに10分間の非アクティブ状態の後、SageMakerはエンドポイントのすべての基盤となるインスタンスを自動的に停止し、関連するインスタンスコストをすべて排除します。

If we try to invoke our endpoint while instances are scaled down to zero, we get a validation error:
インスタンスがゼロにスケールダウンしている間にエンドポイントを呼び出そうとすると、検証エラーが発生します。

An error occurred (ValidationError) when calling the InvokeEndpoint operation: Inference Component has no capacity to process this request. ApplicationAutoScaling may be in-progress (if configured) or try to increase the capacity by invoking UpdateInferenceComponentRuntimeConfig API.
InvokeEndpoint操作を呼び出す際にエラーが発生しました（ValidationError）：推論コンポーネントにはこのリクエストを処理する能力がありません。ApplicationAutoScalingが進行中である可能性があります（設定されている場合）または、UpdateInferenceComponentRuntimeConfig APIを呼び出して容量を増やそうとしてください。

```
sagemaker_client.invoke_endpoint(EndpointName=endpoint_name,InferenceComponentName=inference_component_name,Body=json.dumps({"inputs":"The diamondback terrapin was the first reptile to be","parameters":{"do_sample":True,"max_new_tokens":256,"min_new_tokens":256,"temperature":0.3,"watermark":True,},}),ContentType="application/json",)["Body"].read().decode("utf8")
```

However, after 1 minute, our step scaling policy should start. SageMaker will then start provisioning a new instance and deploy our inference component model copy to handle requests.
しかし、1分後には、私たちのステップスケーリングポリシーが開始されるはずです。SageMakerは新しいインスタンスのプロビジョニングを開始し、リクエストを処理するために推論コンポーネントのモデルコピーをデプロイします。

## 1.7. Schedule scaling down to zero スケジュールのスケーリングをゼロにする

In some scenarios, you might observe consistent weekly traffic patterns: a steady workload Monday through Friday, and no traffic on weekends.
いくつかのシナリオでは、一貫した週次トラフィックパターンを観察することがあります：月曜日から金曜日までの安定した作業負荷と、週末のトラフィックがないことです。
You can optimize costs and performance by configuring scheduled actions that align with these patterns:
これらのパターンに合わせてスケジュールされたアクションを設定することで、コストとパフォーマンスを最適化できます：

- Weekend scale-in (Friday evening)– Configure a scheduled action to reduce the number of model copies to zero.
- 週末のスケールイン（金曜日の夕方）– モデルコピーの数をゼロに減らすスケジュールされたアクションを設定します。
This will instruct SageMaker to scale the number instance behind the endpoint to zero, completely eliminating costs during the weekend period of no usage.
これにより、SageMakerはエンドポイントの背後にあるインスタンスの数をゼロにスケールダウンし、使用されていない週末の期間中のコストを完全に排除します。

- Workweek scale-out (Monday morning)– Set up a complementary scheduled action to restore the required model capacity for the inference component on Monday morning, so your application is ready for weekday operations.
- 平日スケールアウト（月曜日の朝）– 月曜日の朝に推論コンポーネントの必要なモデル容量を復元する補完的なスケジュールされたアクションを設定し、アプリケーションが平日の操作に備えられるようにします。

You can scale your endpoint to zero in two ways.
エンドポイントをゼロにスケールダウンする方法は2つあります。
The first method is to set the number of model copies to zero in your inference component using the UpdateInferenceComponentRuntimeConfig API.
最初の方法は、UpdateInferenceComponentRuntimeConfig APIを使用して推論コンポーネントのモデルコピーの数をゼロに設定することです。
This approach maintains your endpoint configuration while eliminating compute costs during periods of inactivity.
このアプローチは、非アクティブな期間中に計算コストを排除しながら、エンドポイントの構成を維持します。

```
sagemaker_client.update_inference_component_runtime_config(InferenceComponentName=inference_component_name,DesiredRuntimeConfig={'CopyCount':0})
```

Amazon EventBridge Scheduler can automate SageMaker API calls using cron/rate expressions for recurring schedules or one-time invocations.
Amazon EventBridge Schedulerは、定期的なスケジュールや一度きりの呼び出しのためにcron/rate式を使用してSageMaker API呼び出しを自動化できます。
To function, EventBridge Scheduler requires an execution role with appropriate permissions to invoke the target API operations on your behalf.
機能するためには、EventBridge Schedulerは、あなたの代わりにターゲットAPI操作を呼び出すための適切な権限を持つ実行ロールを必要とします。
For more information about how to create this role, see Set up the execution role.
このロールの作成方法の詳細については、「実行ロールの設定」を参照してください。
The specific permissions needed depend on the target API being called.
必要な特定の権限は、呼び出されるターゲットAPIによって異なります。

The following code creates two scheduled actions for the inference component during 2024–2025.
以下のコードは、2024年から2025年の間に推論コンポーネントのための2つのスケジュールされたアクションを作成します。
The first schedule scales in the CopyCount to zero every Friday at 18:00 UTC+1, and the second schedule restores model capacity every Monday at 07:00 UTC+1.
最初のスケジュールは、毎週金曜日の18:00 UTC+1にCopyCountをゼロにスケールインし、2番目のスケジュールは毎週月曜日の07:00 UTC+1にモデル容量を復元します。
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
複数の推論コンポーネントを持つエンドポイントをゼロにスケールダウンするには、すべてのコンポーネントを0に設定するか削除する必要があります。
You can also automate this process by using EventBridge Scheduler to trigger an AWS Lambda function that handles either deletion or zero-setting of all inference components.
また、EventBridge Schedulerを使用して、すべての推論コンポーネントの削除またはゼロ設定を処理するAWS Lambda関数をトリガーすることで、このプロセスを自動化することもできます。

## 1.8. Performance evaluation パフォーマンス評価

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
このような慎重なスケーリングアプローチは、変動するワークロードを持つ環境において、一貫したパフォーマンスとコスト効率を維持するのに役立ちます。

### 1.8.1. Scale up Trials スケールアップ試験

- Target Tracking: Scale Model Copies to Zero (min)– This refers to the time it took target tracking to trigger the alarm and SageMaker to decrease model copies to zero on the instance
- ターゲットトラッキング: モデルコピーをゼロにスケールダウンする時間（分）– これは、ターゲットトラッキングがアラームをトリガーし、SageMakerがインスタンス上のモデルコピーをゼロに減少させるのにかかった時間を指します。

- Scale in Instance Count to Zero (min)– This refers to the time it takes SageMaker to scale the instances down to zero after all inference component model copies are zero
- インスタンス数をゼロにスケールダウンする時間（分）– これは、すべての推論コンポーネントのモデルコピーがゼロになった後、SageMakerがインスタンスをゼロにスケールダウンするのにかかる時間を指します。

- Step Scaling: Scale up Model Copies from Zero (min)– This refers to the time it took step scaling to trigger the alarm and for SageMaker to provision the instances
- ステップスケーリング: ゼロからモデルコピーをスケールアップする時間（分）– これは、ステップスケーリングがアラームをトリガーし、SageMakerがインスタンスをプロビジョニングするのにかかった時間を指します。

- Scale out Instance Count from Zero (min)– This refers to the time it takes for SageMaker to scale out and add inference component model copies
- インスタンス数をゼロからスケールアウトする時間（分）– これは、SageMakerがスケールアウトし、推論コンポーネントのモデルコピーを追加するのにかかる時間を指します。

If you want more customization and faster scaling, consider using step scaling to scale model copies instead of target tracking.
より多くのカスタマイズと迅速なスケーリングを望む場合は、ターゲットトラッキングの代わりにステップスケーリングを使用してモデルコピーをスケールすることを検討してください。

## 1.9. Customers testimonials 顧客の証言

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
「SageMakerエンドポイントのScale to Zero機能は、iFoodの機械学習運用にとって基本的なものとなります。
Over the years, we’ve collaborated closely with the SageMaker team to enhance our inference capabilities.
私たちは、推論能力を向上させるために、SageMakerチームと密接に協力してきました。
This feature represents a significant advancement, as it allows us to improve cost efficiency without compromising the performance and quality of our ML services, given that inference constitutes a substantial part of our infrastructure expenses.”
この機能は重要な進展を示しており、推論が私たちのインフラストラクチャ費用の大部分を占めるため、MLサービスのパフォーマンスと品質を損なうことなくコスト効率を向上させることができます。」
– Daniel Vieira, MLOps Engineer Manager at iFoods
– Daniel Vieira, iFoodsのMLOpsエンジニアマネージャー

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
APOIDEAの製品は、繰り返しの人間の分析タスクを自動化し、広範な財務文書から貴重な財務インサイトを抽出して、業界全体のAI駆動の変革を加速します。
“SageMaker’s Scale to Zero feature is a game changer for our AI financial analysis solution in operations.
「SageMakerのScale to Zero機能は、私たちのAI財務分析ソリューションの運用においてゲームチェンジャーです。
It delivers significant cost savings by scaling down endpoints during quiet periods, while maintaining the flexibility we need for batch inference and model testing.
静かな期間中にエンドポイントを縮小することで大幅なコスト削減を実現し、バッチ推論やモデルテストに必要な柔軟性を維持します。
This capability is transforming how we manage our GenAI workloads and evaluate new models.
この機能は、私たちのGenAIワークロードの管理方法と新しいモデルの評価方法を変革しています。
We’re eager to harness its power to further optimize our deep learning and NLP model deployments.”
私たちは、この機能の力を活用して、深層学習とNLPモデルの展開をさらに最適化することを楽しみにしています。」
– Mickey Yip, VP of Product at APOIDEA Group
– Mickey Yip, APOIDEA Groupの製品担当副社長

Fortiro, based in Melbourne, Australia, is a FinTech company specializing in automated document fraud detection and financial verification for trusted financial institutions.
オーストラリアのメルボルンに本社を置くFortiroは、信頼できる金融機関向けの自動文書詐欺検出と財務検証を専門とするFinTech企業です。
“The new Scale-to-Zero capability in SageMaker is a game-changer for our MLOps and delivers great cost savings.
「SageMakerの新しいScale-to-Zero機能は、私たちのMLOpsにとってゲームチェンジャーであり、大幅なコスト削減を実現します。
Being able to easily scale inference endpoints and GPUs means we can take advantage of a fast, highly responsive environment, without incurring unnecessary costs.
推論エンドポイントとGPUを簡単にスケールできることは、不要なコストをかけることなく、迅速で高い応答性のある環境を活用できることを意味します。
Our R&D teams constantly experiment with new AI-based document fraud detection methods, which involves a lot of testing and repeating.
私たちのR&Dチームは、新しいAIベースの文書詐欺検出方法を常に実験しており、多くのテストと繰り返しが必要です。
This capability empowers us to do this both faster and more efficiently.”
この機能は、私たちがこれをより早く、より効率的に行うことを可能にします。」
– Amir Vahid, Chief Technology Officer at Fortiro
– Amir Vahid, Fortiroの最高技術責任者

These testimonials underscore the anticipation for SageMaker’s Scale to Zero feature.
これらの証言は、SageMakerのScale to Zero機能への期待を強調しています。
As organizations begin to implement this capability, we expect to see innovative applications that balance cost efficiency with performance in machine learning deployments.
組織がこの機能を実装し始めると、コスト効率とパフォーマンスのバランスを取った革新的なアプリケーションが見られることを期待しています。

## 1.10. Conclusion 結論

In this post, we introduced the new scale to zero feature in SageMaker, an innovative capability that enables you to optimize costs by automatically scaling in your inference endpoints when they’re not in use.
本稿では、SageMakerの新しいスケール・トゥ・ゼロ機能を紹介しました。この革新的な機能は、推論エンドポイントが使用されていないときに自動的にスケールダウンすることでコストを最適化することを可能にします。

We guided you through the detailed process of implementing this feature, including configuring endpoints, setting up auto scaling policies, and managing inference components for both automatic and scheduled scaling scenarios.
この機能を実装するための詳細なプロセス、エンドポイントの設定、自動スケーリングポリシーの設定、そして自動およびスケジュールされたスケーリングシナリオのための推論コンポーネントの管理について説明しました。

This cost-saving functionality presents new possibilities for how you can approach your ML operations.
このコスト削減機能は、機械学習（ML）オペレーションへのアプローチに新たな可能性を提供します。

With this feature, you can closely align your compute resource usage with actual needs, potentially reducing costs during periods of low demand.
この機能を使用することで、コンピュートリソースの使用を実際のニーズに密接に合わせることができ、需要が低い期間中のコストを削減する可能性があります。

We encourage you to try this capability and start optimizing your SageMaker inference costs today.
この機能を試し、今日からSageMakerの推論コストを最適化することをお勧めします。

To help you get started quickly, we’ve prepared a comprehensive notebooks containing an end-to-end example of how to configure an endpoint to scale to zero.
迅速に始められるように、エンドポイントをスケール・トゥ・ゼロに設定する方法のエンドツーエンドの例を含む包括的なノートブックを用意しました。

We encourage you to try this capability and start optimizing your SageMaker inference costs today!
この機能を試し、今日からSageMakerの推論コストを最適化することをお勧めします！

### 1.10.1. About the authors 著者について

Marc Karpis an ML Architect with the Amazon SageMaker Service team.
Marc Karpisは、Amazon SageMakerサービスチームのMLアーキテクトです。
He focuses on helping customers design, deploy, and manage ML workloads at scale.
彼は、顧客が大規模なMLワークロードを設計、展開、管理するのを支援することに注力しています。
In his spare time, he enjoys traveling and exploring new places.
余暇には、旅行や新しい場所を探索することを楽しんでいます。

Christian Kamwangalais an AI/ML and Generative AI Specialist Solutions Architect at AWS, based in Paris, France.
Christian Kamwangaは、フランス・パリに拠点を置くAWSのAI/MLおよび生成AIスペシャリストソリューションアーキテクトです。
He helps enterprise customers architect and implement cutting-edge AI solutions using AWS’s comprehensive suite of tools, with a focus on production-ready systems that follow industry best practices.
彼は、業界のベストプラクティスに従った生産準備が整ったシステムに焦点を当て、AWSの包括的なツール群を使用して企業顧客が最先端のAIソリューションを設計し、実装するのを支援しています。
In his spare time, Christian enjoys exploring nature and spending time with family and friends.
余暇には、自然を探索したり、家族や友人と過ごすことを楽しんでいます。

Saurabh Trikandeis a Senior Product Manager for Amazon Bedrock and SageMaker Inference.
Saurabh Trikandeは、Amazon BedrockおよびSageMaker Inferenceのシニアプロダクトマネージャーです。
He is passionate about working with customers and partners, motivated by the goal of democratizing AI.
彼は、AIの民主化を目指して顧客やパートナーと協力することに情熱を注いでいます。
He focuses on core challenges related to deploying complex AI applications, inference with multi-tenant models, cost optimizations, and making the deployment of Generative AI models more accessible.
彼は、複雑なAIアプリケーションの展開、マルチテナントモデルによる推論、コスト最適化、生成AIモデルの展開をよりアクセスしやすくすることに関連する主要な課題に焦点を当てています。
In his spare time, Saurabh enjoys hiking, learning about innovative technologies, following TechCrunch, and spending time with his family.
余暇には、ハイキングをしたり、革新的な技術について学んだり、TechCrunchをフォローしたり、家族と過ごすことを楽しんでいます。

Raghu Rameshais a Senior GenAI/ML Solutions Architect on the Amazon SageMaker Service team.
Raghu Rameshは、Amazon SageMakerサービスチームのシニアGenAI/MLソリューションアーキテクトです。
He focuses on helping customers build, deploy, and migrate ML production workloads to SageMaker at scale.
彼は、顧客が大規模にMLプロダクションワークロードをSageMakerに構築、展開、移行するのを支援することに注力しています。
He specializes in machine learning, AI, and computer vision domains, and holds a master’s degree in computer science from UT Dallas.
彼は、機械学習、AI、コンピュータビジョンの分野を専門としており、UTダラスでコンピュータサイエンスの修士号を取得しています。
In his free time, he enjoys traveling and photography.
自由な時間には、旅行や写真撮影を楽しんでいます。

Melanie Li, PhD, is a Senior Generative AI Specialist Solutions Architect at AWS based in Sydney, Australia, where her focus is on working with customers to build solutions leveraging state-of-the-art AI and machine learning tools.
Melanie Li博士は、オーストラリア・シドニーに拠点を置くAWSのシニア生成AIスペシャリストソリューションアーキテクトであり、最先端のAIおよび機械学習ツールを活用したソリューションを構築するために顧客と協力することに注力しています。
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
余暇には、読書をしたり、長距離ランニングをしたり、家族と新しい場所を探索することを楽しんでいます。

### 1.10.2. Resources リソース

- Getting Started 始めに
- What's New 新着情報

### 1.10.3. Blog Topics ブログトピック

- Amazon Bedrock
- Amazon Comprehend
- Amazon Kendra
- Amazon Lex
- Amazon Polly
- Amazon Q
- Amazon Rekognition
- Amazon SageMaker
- Amazon Textract

### 1.10.4. Follow フォロー

- Twitter
- Facebook
- LinkedIn
- Twitch
- Email Updates (メール更新)

### 1.10.5. Learn About AWS AWSについて学ぶ

- What Is AWS? AWSとは何ですか？
- What Is Cloud Computing? クラウドコンピューティングとは何ですか？
- AWS Accessibility AWSのアクセシビリティ
- AWS Inclusion, Diversity & Equity AWSの包括性、多様性、平等
- What Is DevOps? DevOpsとは何ですか？
- What Is a Container? コンテナとは何ですか？
- What Is a Data Lake? データレイクとは何ですか？
- What is Artificial Intelligence (AI)? 人工知能（AI）とは何ですか？
- What is Generative AI? ジェネレーティブAIとは何ですか？
- What is Machine Learning (ML)? 機械学習（ML）とは何ですか？
- AWS Cloud Security AWSクラウドセキュリティ
- What's New 新着情報
- Blogs ブログ
- Press Releases プレスリリース

### 1.10.6. Resources for AWS AWSのリソース

- Getting Started 始めに
- Training and Certification トレーニングと認証
- AWS Solutions Library AWSソリューションライブラリ
- Architecture Center アーキテクチャセンター
- Product and Technical FAQs 製品および技術に関するFAQ
- Analyst Reports アナリストレポート
- AWS Partners AWSパートナー

### 1.10.7. Developers on AWS AWS上の開発者

- Developer Center 開発者センター
- SDKs & Tools SDKとツール
- .NET on AWS AWS上の.NET
- Python on AWS AWS上のPython
- Java on AWS AWS上のJava
- PHP on AWS AWS上のPHP
- JavaScript on AWS AWS上のJavaScript
