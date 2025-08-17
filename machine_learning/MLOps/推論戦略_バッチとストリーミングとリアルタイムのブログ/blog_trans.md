refs: https://www.infracloud.io/blogs/exploring-ai-model-inference/

# Exploring AI Model Inference: Servers, Frameworks, and Optimization Strategies AIモデル推論の探求：サーバー、フレームワーク、および最適化戦略

Over the past two years, we’ve witnessed the rise of Large Language Models (LLM) and Multimodal models distributed as Software as a Service (SaaS) applications like ChatGPT, Claude, Sora, among others. 
過去2年間で、私たちはChatGPT、Claude、SoraなどのSoftware as a Service（SaaS）アプリケーションとして配布される大規模言語モデル（LLM）やマルチモーダルモデルの台頭を目の当たりにしました。 
These SaaS applications demonstrate the tangible benefits AI models offer in an accessible format. 
これらのSaaSアプリケーションは、AIモデルが提供する具体的な利点をアクセスしやすい形式で示しています。
However, integrating AI into your business poses challenges when relying on such SaaS applications, primarily due to the lack of control over data storage. 
しかし、このようなSaaSアプリケーションに依存してAIをビジネスに統合することは、主にデータストレージに対する制御の欠如のために課題をもたらします。 
Plus, you might need to fine-tune them with your proprietary data to make it more contextual. 
さらに、より文脈に即したものにするために、独自のデータで微調整する必要があるかもしれません。 
This entire process of developing/fine-tuning the models and then deploying them in production is quite complex and this is where MLOps as a practice comes in. 
**モデルの開発/微調整を行い、それを本番環境にデプロイするというこの全プロセスは非常に複雑であり、ここでMLOpsという実践が登場**します。 
Now, one critical part of the MLOps process is Inference, i.e., when models are deployed in production so they can be used to solve business problems. 
さて、**MLOpsプロセスの重要な部分の一つは推論（Inference）**であり、これはモデルが本番環境にデプロイされ、ビジネス上の問題を解決するために使用されるときのことを指します。 

Inference refers to using a trained machine learning model to make predictions or decisions based on new input data. 
**推論とは、新しい入力データに基づいて予測や決定を行うために訓練された機械学習モデルを使用すること**を指します。 
It is a crucial part of the machine learning workflow, as it allows the model to be utilized in real-world applications to perform tasks such as image recognition, natural language processing, recommendation systems, and many others. 
これは機械学習ワークフローの重要な部分であり、モデルが画像認識、自然言語処理、推薦システムなどのタスクを実行するために実世界のアプリケーションで利用されることを可能にします。 

In this blog post, we aim to underscore the crucial decisions that must be taken into account when considering deploying a model on your infrastructure. 
このブログ記事では、**モデルをあなたのインフラストラクチャにデプロイする際に考慮すべき重要な決定事項**を強調することを目的としています。 
We’ll delve into topics such as exploring various deployment options for trained models, identifying optimizations to minimize infrastructure needs for hosting the models, and evaluating inference servers and frameworks to streamline operational aspects of deploying models in production. 
私たちは、訓練されたモデルの**さまざまなデプロイメントオプションの探求**、モデルをホスティングするためのインフラストラクチャのニーズを最小限に抑えるための最適化の特定、そしてモデルを本番環境にデプロイする際の運用面を効率化するための推論サーバーとフレームワークの評価などのトピックに深く掘り下げます。 
Making informed decisions in these areas empowers you to effectively select the optimal path or approach for managing model deployment in production. 
これらの分野で情報に基づいた決定を下すことは、モデルの本番環境へのデプロイ管理において最適な道筋やアプローチを効果的に選択する力を与えます。 

<!-- ここまで読んだ! -->

## Model serving modes モデル提供モード

Typically, models integrate into AI enabled applications or products – accepting input and producing predictions as output. 
通常、モデルはAI対応のアプリケーションや製品に統合され、入力を受け取り、出力として予測を生成します。
Depending on the specific use case or product design, there are generally three model serving options available: 
特定のユースケースや製品設計に応じて、**一般的に利用可能なモデル提供オプションは3つ**あります:
(お! バッチとリアルタイムの2つじゃないパターンだ! 嬉しいね...!:thinking:)

<!-- ここまで読んだ! -->

### Online serving オンラインサービング

- This resembles a REST API endpoint, where input is provided to the model via the endpoint, and immediate predictions are returned as output. 
これは、入力がエンドポイントを介してモデルに提供され、即座に予測が出力として返されるREST APIエンドポイントに似ています。 
- It operates synchronously. 
これは同期的に動作します。
- This is a slightly costly approach as it requires you to handle multiple user requests in parallel. 
これは、複数のユーザリクエストを並行して処理する必要があるため、ややコストがかかるアプローチです。
- Inference servers usually run multiple copies of the model across the available GPU or AI GPU cloud to handle this. 
推論サーバは通常、これを処理するために利用可能なGPUまたはAI GPUクラウド全体でモデルの複数のコピーを実行します。
- From an infrastructure standpoint, you will need the options to scale in or scale out based on the surge or decline in user requests. 
インフラの観点から、ユーザリクエストの急増または減少に基づいてスケールインまたはスケールアウトするオプションが必要です。

![](https://www.infracloud.io/assets/img/blog/exploring-ai-model-inference/online-serving.webp)

### Streaming Serving ストリーミングサービング

Some application architectures follow asynchronous design principles. 
いくつかのアプリケーションアーキテクチャは、非同期設計原則に従います。 
Here, services rely on a shared message bus (such as Kafka or SQS) to receive signals for processing new data. 
ここでは、サービスは新しいデータの処理のために信号を受信するために、共有メッセージバス（KafkaやSQSなど）に依存します。 
In streaming deployment, the model can receive input data from the message bus and deliver predictions either back to the message bus or to storage servers. 
ストリーミングデプロイメントでは、モデルはメッセージバスから入力データを受け取り、予測をメッセージバスに戻すか、ストレージサーバーに送信することができます。

This is a slightly flexible model of deployment, as in asynchronous systems, you do not have any hard coupling between the systems. 
これは、非同期システムでは、システム間に厳密な結合がないため、やや柔軟なデプロイメントモデルです。 
You can leverage different model options here and have parallel consumers to validate the performance. 
ここでは、さまざまなモデルオプションを活用し、パラレルコンシューマーを持ってパフォーマンスを検証することができます。

The scaling principle remains same as the other options. 
スケーリングの原則は、他のオプションと同じです。

![](https://www.infracloud.io/assets/img/blog/exploring-ai-model-inference/streaming-serving.webp)

### Batch serving バッチサービング

With this option, a model is deployed as part of a batch pipeline. 
このオプションでは、モデルはバッチパイプラインの一部として展開されます。 

Input datasets are prepared beforehand, and the model generates predictions, storing them in a storage server for later use by the product in enabling specific features. 
入力データセットは事前に準備され、モデルは予測を生成し、それをストレージサーバーに保存して、製品が特定の機能を有効にするために後で使用します。

This is more predictive model of deployment and you can manage the infra upfront based on the scale estimates. 
これはより予測的なデプロイメントモデルであり、スケールの見積もりに基づいてインフラを事前に管理できます。

Instead of predicting for every request, the model predicts on a batch of data in one request. 
すべてのリクエストに対して予測するのではなく、モデルは1つのリクエストでデータのバッチに対して予測を行います。

![](https://www.infracloud.io/assets/img/blog/exploring-ai-model-inference/batch-serving.webp)

(3種類のサービングモードの利点・欠点を列挙した表も書かれてた!)

<!-- ここまで読んだ! -->

## Inference servers 推論サーバー

An inference server works by receiving input data, typically in the form of requests from clients, which can include queries, images, text, or other forms of data. 
推論サーバーは、通常、クライアントからのリクエストの形で入力データを受け取り、クエリ、画像、テキスト、またはその他のデータ形式を含むことができます。
It then processes this data through trained machine learning models or algorithms to generate predictions, classifications, or other outputs. 
その後、訓練された機械学習モデルやアルゴリズムを通じてこのデータを処理し、予測、分類、またはその他の出力を生成します。

When used in a production environment, it needs to be highly scalable to process large volumes of user requests with low latency and should optimize model execution for speed, memory usage, and energy efficiency. 
本番環境で使用される場合、高いスケーラビリティが求められ、大量のユーザリクエストを低遅延で処理できる必要があり、速度、メモリ使用量、エネルギー効率のためにモデル実行を最適化する必要があります。
Apart from performance metrics, teams usually spend quite a bit of time on operational aspects i.e. managing the model deployments and enabling customizations like adding business logic or preprocessing steps into the inference pipeline. 
パフォーマンス指標とは別に、チームは通常、モデルのデプロイ管理やビジネスロジックの追加、推論パイプラインへの前処理ステップの組み込みなど、運用面にかなりの時間を費やします。

The landscape of AI hardware is rapidly evolving, with much of the optimization in inference relying on effectively harnessing new hardware accelerators for GPU networking, storage access, and more. 
AIハードウェアの状況は急速に進化しており、推論の最適化の多くは、GPUネットワーキング、ストレージアクセスなどの新しいハードウェアアクセラレーターを効果的に活用することに依存しています。
As a result, a plethora of inference servers are currently available, with many new ones emerging. 
その結果、現在利用可能な推論サーバーは多数あり、多くの新しいものが登場しています。
In this discussion, we categorize the existing offerings into two broad categories and explore the value they provide. 
この議論では、既存の提供物を2つの大きなカテゴリに分類し、それらが提供する価値を探ります。

- Native ML/DL servers
- ネイティブML/DLサーバー
- Specialized inference servers
- 専門的な推論サーバー

<!-- ここまで読んだ! -->

### What are native ML/DL servers? ネイティブML/DLサーバーとは？

To build a Machine Learning (ML) / Deep Learning (DL) model, we usually use AI frameworks/libraries like PyTorch, TensorFlow, etc. 
機械学習（ML）/深層学習（DL）モデルを構築するために、通常はPyTorchやTensorFlowなどのAIフレームワーク/ライブラリを使用します。 
This category includes inference servers built by the same frameworks to serve the trained models like TorchServe for PyTorch, TensorServing for Tensorflow models, etc. 
このカテゴリには、PyTorch用のTorchServeやTensorFlowモデル用のTensorServingなど、同じフレームワークによって構築された推論サーバーが含まれます。 
Their sole purpose is to serve the models trained using the same framework. 
それらの唯一の目的は、同じフレームワークを使用して訓練されたモデルを提供することです。 
They provide most of the required capabilities like batch inferencing, optimization support, and service endpoints. 
それらは、バッチ推論、最適化サポート、サービスエンドポイントなど、必要な機能のほとんどを提供します。

Advantages of native ML/DL servers: ネイティブML/DLサーバーの利点：
- Broad hardware support (CPUs, GPUs, TPUs) 
- 幅広いハードウェアサポート（CPU、GPU、TPU）
- Can be used for both training and inference 
- 訓練と推論の両方に使用可能
- Seamless integration with the native ML/DL frameworks 
- ネイティブML/DLフレームワークとのシームレスな統合
- Large ecosystem and community support 
- 大規模なエコシステムとコミュニティサポート

Disadvantages of native ML/DL servers: ネイティブML/DLサーバーの欠点：
- Not optimized specifically for inference workloads 
- 推論ワークロードに特化して最適化されていない
- May have higher latency and lower throughput compared to specialized servers 
- 専門のサーバーと比較して、レイテンシが高く、スループットが低い可能性がある
- Can be more resource-intensive and costly for inference workloads 
- 推論ワークロードに対して、よりリソースを消費し、コストがかかる可能性がある
- May require more manual effort for optimizations and deployment management 
- 最適化やデプロイ管理に対して、より多くの手動作業が必要になる可能性がある

### What are specialized inference servers? 専門的推論サーバとは？

Specialized inference servers are purpose-built inference servers to provide the best optimization possible. 
専門的推論サーバは、最適な最適化を提供するために特別に設計された推論サーバです。
On the hardware side, we have certain inference servers from all the major GPU vendors, i.e. Nvidia, Intel, and AMD. 
ハードウェアの面では、Nvidia、Intel、AMDなどの主要なGPUベンダーからの特定の推論サーバがあります。
They have their inference engine or frameworks that use kernel drivers, libraries, and compilers to provide the best optimization possible. 
彼らは、カーネルドライバ、ライブラリ、およびコンパイラを使用して最適な最適化を提供する推論エンジンまたはフレームワークを持っています。
They use different compilers and optimization techniques to reduce the latency and memory consumption. 
彼らは、レイテンシとメモリ消費を削減するために、異なるコンパイラと最適化技術を使用します。
Some of the popular inference servers from known vendors include: 
知られているベンダーからの人気のある推論サーバには以下が含まれます：

- Nvidia Triton  
  Optimized for Nvidia GPUs, provides high-performance inference for deep learning models, supports models from various frameworks, and enables easy deployment and management of inference workloads.  
  Nvidia Tritonは、Nvidia GPUに最適化されており、深層学習モデルの高性能推論を提供し、さまざまなフレームワークからのモデルをサポートし、推論ワークロードの簡単なデプロイと管理を可能にします。

- Intel OpenVino  
  Enables optimized inference across Intel hardware (CPUs, GPUs, VPUs), supports models from various frameworks, and provides tools for optimizing and deploying deep learning models on Intel architecture.  
  Intel OpenVinoは、Intelハードウェア（CPU、GPU、VPU）全体で最適化された推論を可能にし、さまざまなフレームワークからのモデルをサポートし、Intelアーキテクチャ上で深層学習モデルを最適化およびデプロイするためのツールを提供します。

- AMD ROCm  
  Optimized for AMD GPUs and other AMD accelerators, provides optimized deep learning inference performance on AMD hardware, supports models from various frameworks, and integrates with the ROCm software stack.  
  AMD ROCmは、AMD GPUおよび他のAMDアクセラレータに最適化されており、AMDハードウェア上で最適化された深層学習推論性能を提供し、さまざまなフレームワークからのモデルをサポートし、ROCmソフトウェアスタックと統合します。

Certain large and complex AI models, particularly large language models (LLMs), require specialized inference servers for several reasons:  
特定の大規模で複雑なAIモデル、特に大規模言語モデル（LLM）は、いくつかの理由から専門的推論サーバを必要とします：

- LLMs have a massive number of parameters, often in the billions, which translates to high computational and memory requirements during inference.  
  LLMは、数十億に及ぶ膨大な数のパラメータを持ち、推論中に高い計算およびメモリ要件を意味します。

- Inference needs to be performed quickly, with low latency, to support real-time applications like chatbots, text generation, and question-answering.  
  推論は迅速に、低レイテンシで実行する必要があり、チャットボット、テキスト生成、質問応答などのリアルタイムアプリケーションをサポートします。

- Deploying LLMs at scale requires high throughput and efficient resource utilization to serve numerous concurrent requests cost-effectively.  
  LLMを大規模に展開するには、高いスループットと効率的なリソース利用が必要であり、多数の同時リクエストにコスト効率よく対応します。

- General-purpose ML/DL inference servers may need to be optimized for the specific computational patterns and memory access patterns of LLMs, leading to suboptimal performance and efficiency.  
  一般的なML/DL推論サーバは、LLMの特定の計算パターンやメモリアクセスパターンに最適化する必要があり、最適でない性能や効率につながる可能性があります。

Following are some of the inference servers that are for serving LLMs specifically:  
以下は、LLMを特に提供するための推論サーバのいくつかです：

- vLLM  
- OpenLLM  
- TGI - Text Generation Inference  

Advantages of specialized inference servers:  
専門的推論サーバの利点：

- Optimized specifically for efficient inference workloads  
  効率的な推論ワークロードのために特に最適化されています。

- Lower latency and higher throughput for inference  
  推論のための低レイテンシと高スループット。

- Often more cost-effective for inference deployments  
  推論のデプロイメントにおいて、しばしばよりコスト効果的です。

- Leverage hardware-specific optimizations (e.g., Tensor Cores, INT8 support)  
  ハードウェア特有の最適化（例：Tensor Cores、INT8サポート）を活用します。

- Simplified deployment and management of inference workflows  
  推論ワークフローのデプロイと管理が簡素化されます。

- Often provide advanced features for inference workflows (e.g., batching, ensembling, model analytics)  
  推論ワークフローのための高度な機能（例：バッチ処理、アンサンブル、モデル分析）を提供することがよくあります。

- Can leverage optimized libraries and kernels for specific hardware (e.g., CUDA, ROCm)  
  特定のハードウェア（例：CUDA、ROCm）向けに最適化されたライブラリやカーネルを活用できます。

Disadvantages of specialized inference servers:  
専門的推論サーバの欠点：

- May have limited hardware support (e.g., only Nvidia GPUs, Intel CPUs/GPUs)  
  限定的なハードウェアサポート（例：Nvidia GPU、Intel CPU/GPUのみ）を持つ場合があります。

- Smaller ecosystem and community compared to native ML/DL frameworks  
  ネイティブのML/DLフレームワークと比較して、エコシステムとコミュニティが小さいです。

- May require additional tooling or integration efforts for model conversion/optimization  
  モデルの変換/最適化のために追加のツールや統合作業が必要な場合があります。

- Limited support for training workloads (inference-only)  
  トレーニングワークロードのサポートが限られている（推論専用）。

- May have limited support for custom models or architectures outside the main frameworks  
  メインフレームワークの外にあるカスタムモデルやアーキテクチャのサポートが限られている場合があります。

- Potential vendor lock-in or dependency on specific hardware/software stacks  
  ベンダーロックインや特定のハードウェア/ソフトウェアスタックへの依存の可能性があります。

<!-- ここはあまり現時点で興味なかったのでラフに読み飛ばした! -->

## MLOps frameworks with model serving モデル提供を伴うMLOpsフレームワーク

Serving a model constitutes just one facet of the overall product lifecycle. 
モデルの提供は、全体の製品ライフサイクルの一側面に過ぎません。
There are numerous operational tasks involved, including deployment planning, managing different model versions, efficient traffic routing, dynamic scaling based on workload, implementing security measures, and setting up gateways for effective tenant-based routing. 
これには、デプロイメント計画、異なるモデルバージョンの管理、効率的なトラフィックルーティング、ワークロードに基づく動的スケーリング、セキュリティ対策の実施、効果的なテナントベースのルーティングのためのゲートウェイの設定など、多くの運用タスクが含まれます。

Aside from operational considerations, there are both preparatory and follow-up tasks related to model serving, such as ensuring model availability in registries, integrating with evaluation frameworks, publishing model metadata, and designing workflows for preprocessing and post-processing data inputs and outputs. 
運用上の考慮事項に加えて、モデル提供に関連する準備作業やフォローアップ作業もあり、これにはレジストリでのモデルの可用性の確保、評価フレームワークとの統合、モデルメタデータの公開、データ入力および出力の前処理と後処理のためのワークフローの設計が含まれます。

Your operational team may already be utilizing orchestrators like Kubernetes for serving microservices, and they may prefer to handle model serving similarly. 
あなたの運用チームは、マイクロサービスの提供にKubernetesのようなオーケストレーターをすでに利用しているかもしれず、モデル提供も同様に扱うことを好むかもしれません。
They might also have established cost optimization practices, such as utilizing spot instances or scaling clusters during non-peak hours. 
彼らは、**スポットインスタンスの利用やピーク時間外のクラスターのスケーリングなど**、コスト最適化の実践を確立しているかもしれません。

MLOps frameworks-based solutions address all the phases of model development and deployment and also provide sufficient flexibility to the teams to plug whatever they already have in place. 
MLOpsフレームワークに基づくソリューションは、モデルの開発とデプロイメントのすべてのフェーズに対応し、チームがすでに持っているものを組み込むための十分な柔軟性を提供します。
They provide options to streamline work during model development, such as offering services to provision notebooks for data scientists and integrating with storage solutions to enhance efficiency for data engineers. 
これらは、データサイエンティストのためのノートブックを提供するサービスや、データエンジニアの効率を向上させるためのストレージソリューションとの統合など、モデル開発中の作業を効率化するためのオプションを提供します。
Furthermore, they facilitate integration with ML/DL frameworks, enabling model training on clusters as well. 
さらに、これらはML/DLフレームワークとの統合を促進し、クラスター上でのモデルトレーニングを可能にします。

- MLFlow
- MLRun
- Kubeflow
- Seldon
- KServe
- BentoML
- RayServe

In summary, these MLOps solutions offer comprehensive end-to-end support for developing, deploying, and operating the model in production. 
要約すると、これらのMLOpsソリューションは、モデルの開発、デプロイメント、および運用に対して包括的なエンドツーエンドのサポートを提供します。
If your team is sizable and aims to establish a robust process or practice for effective management right from the start, opting for one of these solutions is highly recommended. 
もしあなたのチームが大規模で、最初から効果的な管理のための堅牢なプロセスやプラクティスを確立することを目指しているのであれば、これらのソリューションのいずれかを選択することを強くお勧めします。
Moreover, they offer customization and integration options that extend beyond the confines of supported tools, allowing you the flexibility to incorporate specific tools tailored to your needs. 
さらに、これらはサポートされているツールの範囲を超えたカスタマイズおよび統合オプションを提供し、あなたのニーズに合わせた特定のツールを組み込む柔軟性を与えます。

<!-- ここまで読んだ! -->

## Inference pipelines 推論パイプライン

As the usage of AI models is becoming more common, we are seeing production inference pipelines becoming more complex. 
AIモデルの使用が一般的になるにつれて、プロダクション推論パイプラインがより複雑になってきています。 
For instance, there are certain tasks like text processing for which you might end up using multiple models to generate the final output. 
例えば、最終的な出力を生成するために複数のモデルを使用することになるテキスト処理のような特定のタスクがあります。 
You might start with a classification model, and based on the result, you pass input data to another model to process it appropriately. 
分類モデルから始め、その結果に基づいて入力データを別のモデルに渡して適切に処理します。 
This requires designing a flow of activities that sometimes even includes processing the output from one stage to prepare it for the next stage. 
これは、時にはある段階の出力を処理して次の段階の準備をすることを含む活動の流れを設計することを必要とします。 

Most of the MLOps frameworks covered above support designing the inference pipelines natively. 
上記で説明したほとんどのMLOpsフレームワークは、推論パイプラインの設計をネイティブにサポートしています。 
They use the capabilities of orchestrators like Kubernetes to schedule and execute the different stages effectively. 
これらは、Kubernetesのようなオーケストレーターの機能を使用して、さまざまな段階を効果的にスケジュールし、実行します。 
Using these frameworks also allows you to use different inference servers that are purpose-built for a specific set of work. 
これらのフレームワークを使用することで、特定の作業セットに特化した異なる推論サーバーを使用することも可能です。 

There are also advanced ML Inference design patterns based on these concepts, like Ensembles and Cascaded Inferences. 
また、これらの概念に基づいた高度なML推論設計パターンもあり、アンサンブルやカスケード推論などがあります。 

#### Ensembles アンサンブル

An ensemble inference pipeline is a type of inference workflow that combines the predictions or outputs of multiple machine learning models to produce a final result. 
アンサンブル推論パイプラインは、複数の機械学習モデルの予測または出力を組み合わせて最終結果を生成する推論ワークフローの一種です。 
They serve as a machine learning strategy that integrates multiple models, referred to as base estimators, during the prediction phase. 
これは、予測フェーズにおいて、ベース推定器と呼ばれる複数のモデルを統合する機械学習戦略として機能します。 
By adopting ensemble models, one can address the technical complexities associated with constructing a singular estimator. 
アンサンブルモデルを採用することで、単一の推定器を構築する際に関連する技術的な複雑さに対処できます。 
This approach involves sending the same input data to an ensemble of models and then combining or aggregating the predictions from all the models to derive the final, most accurate prediction. 
このアプローチでは、同じ入力データをモデルのアンサンブルに送信し、すべてのモデルからの予測を結合または集約して最終的で最も正確な予測を導き出します。 

To understand how an ensemble inference pipeline can be used in the real world consider the following example scenario for credit risk assessment. 
アンサンブル推論パイプラインが実世界でどのように使用されるかを理解するために、信用リスク評価のための以下の例を考えてみましょう。 
Banks could use an ensemble pipeline consisting of a machine learning model for predicting credit scores, a rule-based system for identifying potentially fraudulent applications, and a deep learning model for analyzing unstructured data like applicant social media activity. 
銀行は、信用スコアを予測するための機械学習モデル、潜在的に不正な申請を特定するためのルールベースのシステム、申請者のソーシャルメディア活動のような非構造化データを分析するための深層学習モデルで構成されるアンサンブルパイプラインを使用できます。 
The outputs from these models would be aggregated to arrive at a final credit risk assessment for loan approval decisions. 
これらのモデルからの出力は集約され、ローン承認の決定のための最終的な信用リスク評価に至ります。

#### Cascaded inferences カスケード推論

The cascaded inference pattern involves a sequential arrangement where the output of one model serves as the input for another, forming a cascading pattern. 
カスケード推論パターンは、1つのモデルの出力が別のモデルの入力として機能する順次配置を含み、カスケードパターンを形成します。 
This technique proves valuable in mitigating model biases or addressing incomplete data scenarios by leveraging an additional predictor to compensate for these shortcomings. 
この技術は、追加の予測子を活用してこれらの欠点を補うことで、モデルのバイアスを軽減したり、不完全なデータシナリオに対処したりするのに役立ちます。

Imagine a scenario where a primary model exhibits a certain bias or struggles with incomplete data, potentially leading to inaccurate predictions. 
主要なモデルが特定のバイアスを示したり、不完全なデータに苦しんだりするシナリオを想像してみてください。これは、潜在的に不正確な予測につながる可能性があります。 
In such cases, employing the Cascaded Inference pattern allows for the integration of a secondary model. 
そのような場合、カスケード推論パターンを採用することで、二次モデルの統合が可能になります。 
This secondary model utilizes the output of the primary model as its input, thereby refining the predictions further or compensating for the limitations of the primary model. 
この二次モデルは、主要モデルの出力を入力として利用し、予測をさらに洗練させたり、主要モデルの制限を補ったりします。 
By cascading models in this manner, the overall predictive accuracy can be improved, leading to more reliable outcomes, especially in situations where individual models may falter due to inherent biases or data limitations. 
このようにモデルをカスケードさせることで、全体の予測精度が向上し、特に個々のモデルが固有のバイアスやデータの制限により失敗する可能性がある状況で、より信頼性の高い結果を得ることができます。 

In real-world, a cascaded inference pipeline for a credit card fraud detection system could involve a machine learning model that analyzes transaction patterns to identify potentially fraudulent activities. 
実世界では、クレジットカード不正検出システムのためのカスケード推論パイプラインは、取引パターンを分析して潜在的に不正な活動を特定する機械学習モデルを含むことができます。 
Suspicious transactions are then passed to a deeper neural network model that examines associated data like customer profiles and purchase details. 
疑わしい取引は、その後、顧客プロファイルや購入詳細などの関連データを調査するより深いニューラルネットワークモデルに渡されます。 
Finally, a rule-based system applies specific policies and regulations to make the ultimate fraud determination. 
最後に、ルールベースのシステムが特定のポリシーと規制を適用して最終的な不正判定を行います。 



## Model optimization for inference モデル最適化による推論

Deploying large AI models can be challenging due to their substantial computational, storage, and memory demands, as well as the need to ensure low-latency response times. 
大規模なAIモデルの展開は、その膨大な計算、ストレージ、メモリの要求に加え、低遅延の応答時間を確保する必要があるため、困難です。

A key optimization strategy is model compression, which involves techniques that reduce the model’s size. 
重要な最適化戦略はモデル圧縮であり、これはモデルのサイズを削減する技術を含みます。

Smaller models can be loaded faster, leading to lower latency, and they require fewer resources for computation, storage, and memory. 
小さなモデルはより速くロードできるため、遅延が低くなり、計算、ストレージ、メモリのリソースも少なくて済みます。

By compressing the model, deployment becomes more easy and efficient, enabling quicker inference while minimizing resource requirements. 
モデルを圧縮することで、展開がより簡単かつ効率的になり、リソース要件を最小限に抑えながら迅速な推論が可能になります。

Compressing a model’s size is beneficial for optimizing deployment, but the challenge lies in achieving effective size reduction while preserving good model performance. 
モデルのサイズを圧縮することは展開の最適化に有益ですが、良好なモデル性能を維持しながら効果的なサイズ削減を達成することが課題です。

Consequently, there is often a trade-off to balance between maintaining the model’s accuracy, adhering to computational resource constraints, and meeting latency requirements. 
そのため、モデルの精度を維持し、計算リソースの制約に従い、遅延要件を満たす間でバランスを取るトレードオフがしばしば存在します。

Here, we talk about three techniques aimed at reducing model size:- 
ここでは、モデルサイズを削減することを目的とした3つの技術について説明します：-

- Quantization 
- Quantization（量子化）

- Pruning 
- Pruning（プルーニング）

- Distillation 
- Distillation（蒸留）



### Quantization 量子化

Quantization minimizes the memory necessary for loading and training a model by decreasing the precision of its weights. 
量子化は、モデルの重みの精度を下げることによって、モデルの読み込みとトレーニングに必要なメモリを最小限に抑えます。

It involves converting model parameters from 32-bit to 16-bit, 8-bit, or 4-bit precision. 
これは、モデルパラメータを32ビットから16ビット、8ビット、または4ビットの精度に変換することを含みます。

By quantizing the model weights from 32-bit full-precision to 16-bit or 8-bit precision, you can substantially reduce the memory requirement of a model with one billion parameters to only 2 GB, cutting it by 50%, or even down to just 1 GB, a 75% reduction, for loading. 
32ビットのフル精度から16ビットまたは8ビットの精度にモデルの重みを量子化することにより、10億のパラメータを持つモデルのメモリ要件をわずか2GBに大幅に削減でき、50%の削減が可能です。また、1GBまで削減することもでき、これは75%の削減に相当します。

However, as this optimization is achieved by moving to lower precise data types there will be loss of precision. 
ただし、この最適化は低精度のデータ型に移行することによって達成されるため、精度の損失が生じます。

So, it is always best to benchmark the results of quantization based on your use case. 
したがって、量子化の結果を使用ケースに基づいてベンチマークすることが常に最良です。

In most cases, a drop in prediction accuracy by 1-2% is a good trade-off to achieve low inference time and a reduction in infrastructure cost. 
ほとんどの場合、予測精度が1-2%低下することは、低い推論時間とインフラコストの削減を達成するための良いトレードオフです。

Quantization is broadly classified into two categories based on when you are applying it i.e post or pre-training. 
量子化は、適用するタイミングに基づいて大きく2つのカテゴリに分類されます。すなわち、トレーニング後またはトレーニング前です。

Post training quantization (PTQ) 
トレーニング後の量子化（PTQ）

Post training quantization (PTQ) is a quantization technique that involves applying the quantization process to a trained model after it has finished training. 
トレーニング後の量子化（PTQ）は、トレーニングが完了した後にトレーニング済みモデルに量子化プロセスを適用する量子化技術です。

This method entails converting the model’s weights and activations from high precision, like FP32, to lower precision, such as INT8. 
この方法は、モデルの重みと活性化を高精度（FP32など）から低精度（INT8など）に変換することを伴います。

While PTQ is relatively simple and easy to implement, it does not consider the effects of quantization during the training phase. 
PTQは比較的簡単で実装しやすいですが、トレーニングフェーズ中の量子化の影響を考慮していません。

Most of the inference servers support applying the PTQ to the trained models. 
ほとんどの推論サーバーは、トレーニング済みモデルにPTQを適用することをサポートしています。

Vendor specific frameworks provide supported libraries to enable it. 
ベンダー特有のフレームワークは、それを可能にするサポートライブラリを提供します。

Quantization aware training (QAT) 
量子化認識トレーニング（QAT）

Quantization-aware training (QAT) is an approach that considers the effects of quantization throughout the training process. 
量子化認識トレーニング（QAT）は、トレーニングプロセス全体で量子化の影響を考慮するアプローチです。

During QAT, the model is trained using operations that simulate quantization, enabling it to adapt and perform effectively in a quantized representation. 
QAT中、モデルは量子化をシミュレートする操作を使用してトレーニングされ、量子化された表現で効果的に適応し、パフォーマンスを発揮できるようになります。

This method enhances accuracy by ensuring the model learns to accommodate quantization nuances, resulting in superior performance compared to post-training quantization. 
この方法は、モデルが量子化のニュアンスに適応することを学ぶことを保証することによって精度を向上させ、トレーニング後の量子化と比較して優れたパフォーマンスをもたらします。



### Pruning プルーニング

Pruning endeavors to remove model weights that do not substantially contribute to the model’s overall performance. 
プルーニングは、モデルの全体的な性能に大きく寄与しないモデルの重みを削除することを目指します。

By discarding these weights, the model’s size for inference is reduced, consequently diminishing the necessary compute resources. 
これらの重みを捨てることで、推論のためのモデルのサイズが縮小され、必要な計算リソースが減少します。

Pruning targets model weights that are either zero or extremely close to zero. 
プルーニングは、ゼロまたはゼロに非常に近いモデルの重みを対象とします。

There are post-training techniques, known as one-shot pruning methods, capable of eliminating weights without the need for retraining. 
再訓練を必要とせずに重みを排除できる、one-shot pruning（ワンショットプルーニング）法として知られるポストトレーニング技術があります。

However, one-shot pruning often presents a computational challenge, particularly for large models containing billions of parameters. 
しかし、one-shot pruningは、特に数十億のパラメータを含む大規模モデルに対して計算上の課題を提示することがよくあります。

A post-training pruning technique, known as SparseGPT, seeks to address the difficulties associated with one-shot pruning for large language models. 
SparseGPTとして知られるポストトレーニングプルーニング技術は、大規模言語モデルに対するone-shot pruningに関連する困難を解決しようとしています。

Designed specifically for language-based generative foundational models, SparseGPT introduces an algorithm capable of conducting sparse regression on a significant scale. 
言語ベースの生成的基盤モデル専用に設計されたSparseGPTは、大規模なスパース回帰を実行できるアルゴリズムを導入します。

Theoretically, pruning diminishes the size of the language model (LLM), thereby reducing computational requirements and model latency. 
理論的には、プルーニングは言語モデル（LLM）のサイズを縮小し、それによって計算要件とモデルのレイテンシを減少させます。



### Distillation 蒸留

Distillation is a method aimed at diminishing the size of a model, consequently cutting down on computations and enhancing model inference performance. 
蒸留は、モデルのサイズを縮小し、計算を削減し、モデルの推論性能を向上させることを目的とした手法です。

It employs statistical techniques to train a compact student model based on a more extensive teacher model. 
これは、より大規模な教師モデルに基づいてコンパクトな学生モデルを訓練するために統計的手法を使用します。

The outcome is a student model that preserves a significant portion of the teacher’s model accuracy while employing fewer parameters. 
その結果、学生モデルは、より少ないパラメータを使用しながら、教師モデルの精度の重要な部分を保持します。

Once trained, the student model is utilized for inference tasks. 
一度訓練されると、学生モデルは推論タスクに利用されます。

Due to its reduced size, the student model demands less hardware, resulting in reduced costs per inference request. 
そのサイズが小さいため、学生モデルはより少ないハードウェアを必要とし、推論リクエストごとのコストが削減されます。



## Conclusion 結論

Inference servers serve as the backbone of AI applications, acting as the vital link between the trained AI model and real-world applications. 
推論サーバーはAIアプリケーションの基盤として機能し、訓練されたAIモデルと実世界のアプリケーションとの重要なリンクを担っています。このブログ投稿は、AIモデル推論サーバー、フレームワーク、および最適化戦略の概要を提供しようとしました。

This blog post tried to provide an overview of AI model inference servers, frameworks, and optimization strategies. 
モデルをインフラストラクチャにデプロイする際に考慮すべきさまざまなデプロイメントオプションと考慮事項を理解することが重要です。

It is essential to understand the various deployment options and considerations when considering deploying a model in your infrastructure. 
ここで取り上げたリストは網羅的ではありませんが、次のスタックを選択する際に論理的になるようにオプションをカテゴリに分けるよう努めました。

Although the list covered here is not exhaustive we tried to group options into categories so that it becomes logical to choose your next stack. 
この投稿が有益で魅力的であったことを願っています。

I hope you found this post informative and engaging. 
このような投稿をもっと読みたい方は、私たちの週刊ニュースレターに登録してください。

For more posts like this one, subscribe to our weekly newsletter. 
この投稿についてのあなたの考えを聞きたいので、LinkedInで会話を始めてください:)

I’d love to hear your thoughts on this post, so do start a conversation on LinkedIn:) 



## References 参考文献
- A friendly introduction to machine learning compilers and optimizers
- Generative AI on AWS
- Implementing MLOps in the Enterprise


