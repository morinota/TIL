
# Feature Store Architecture and How to Build One 特徴ストアのアーキテクチャとその構築方法

Learn about the Feature Store Architecture and dive deep into advanced concepts and best practices for building a feature store.
フィーチャーストアのアーキテクチャについて学び、フィーチャーストアを構築するための高度な概念とベストプラクティスに深く掘り下げます。

As machine learning becomes increasingly integral to business operations, the role of ML Platform Teams is gaining prominence. 
機械学習がビジネスオペレーションにますます不可欠なものとなるにつれて、MLプラットフォームチームの役割が重要性を増しています。
These teams are tasked with developing or selecting the essential tools that enable machine learning to move beyond experimentation into real-world applications. 
これらのチームは、機械学習が実験を超えて実世界のアプリケーションに移行するために必要なツールを開発または選定する任務を担っています。
One such indispensable tool is a feature store. 
そのような不可欠なツールの一つが特徴ストアです。
If you find yourself grappling with the complexities of data pipelines for your ML models, a feature store could be the solution you're looking for. 
もしあなたがMLモデルのデータパイプラインの複雑さに悩んでいるなら、特徴ストアがあなたが探している解決策かもしれません。
In this article, we aim to provide a comprehensive guide to understanding and implementing a feature store, layer by layer. 
この記事では、特徴ストアを理解し、層ごとに実装するための包括的なガイドを提供することを目指します。
Our goal is to help you make an informed decision on whether a feature store aligns with your needs. 
私たちの目標は、特徴ストアがあなたのニーズに合っているかどうかについて、情報に基づいた意思決定を行う手助けをすることです。

<!-- ここまで読んだ -->


## Feature Store Architecture? Why Before How フィーチャーストアアーキテクチャ？ howの前にwhy

Let's get real for a moment. 
少し現実を見てみましょう。
You're not building a feature store for the fun of it; you're building it because you have real challenges that need real solutions. 
**あなたは楽しみのためにフィーチャーストアを構築しているのではありません。実際の課題があり、それに対する実際の解決策が必要だから**です。
So, what's driving you to consider a feature store in the first place? 
では、そもそもフィーチャーストアを検討する理由は何でしょうか？
Here are some of the most compelling reasons we've heard: 
ここに、私たちが聞いた中で最も説得力のある理由をいくつか挙げます。

Real-Time Feature Serving - Your machine learning models require features with low latency and the ability to scale. 
**リアルタイムフィーチャーサービング** - あなたの機械学習モデルは、低遅延でスケーラブルなフィーチャーを必要とします。
This isn't just a nice-to-have; it's essential for operational efficiency. 
これは単なる「あれば良い」ものではなく、運用効率にとって不可欠です。

Standardization - You're tired of the Wild West approach to feature pipelines. 
**標準化** - あなたはフィーチャーパイプラインの無法地帯的なアプローチに疲れています。
You want a standardized way to build, store, and manage features for all your ML projects. 
すべての機械学習プロジェクトに対して、フィーチャーを構築、保存、管理するための標準化された方法を求めています。

Unified Data Pipelines - The days of maintaining separate pipelines for training and serving are over. 
統一データパイプライン - トレーニングとサービングのために別々のパイプラインを維持する時代は終わりました。(これは学習と推論でそれぞれ特徴量を作る処理が実装されてる、みたいな意味合いだよね...! :thinking:)
You're looking for a unified approach to reduce training/serving skew and make your life easier. 
トレーニングとサービングの偏りを減らし、生活を楽にするための統一されたアプローチを探しています。

Feature Reusability and Efficiency - A centralized feature store not only makes it easier to share features across projects but also enhances discoverability, accuracy, and cost-efficiency. 
**フィーチャーの再利用性と効率** - 中央集権的なフィーチャーストアは、プロジェクト間でフィーチャーを共有しやすくするだけでなく、発見性、正確性、コスト効率を向上させます。
By having a single source of truth for your features, you avoid redundant calculations and inconsistent usage in models. 
フィーチャーの単一の真実の源を持つことで、冗長な計算やモデル内での不一致な使用を避けることができます。

If any of these resonate with you, you're in the right place. 
**これらのいずれかに共感するなら、あなたは正しい場所にいます。**
A feature store addresses these challenges head-on, providing a structured, scalable way to manage your features, from ingestion to serving. 
フィーチャーストアはこれらの課題に直接対処し、取り込みからサービングまでフィーチャーを管理するための構造化されたスケーラブルな方法を提供します。
And the best part? 
そして、最も良い点は？
It's not a one-size-fits-all solution; it's a framework that can be tailored to meet your specific needs and constraints. 
**これは一律の解決策ではなく、あなたの特定のニーズと制約に合わせて調整できるフレームワーク**です。
So, what's driving you to consider building a feature store in the first place? 
では、そもそもフィーチャーストアを構築することを検討する理由は何でしょうか？

<!-- ここまで読んだ -->

## Feature Store vs. Data Store vs. ETL Pipelines: Understanding the Nuances 特徴ストアとデータストアとETLパイプライン：ニュアンスを理解する

As you navigate the landscape of data management for machine learning, you'll encounter several key components, each with its own set of capabilities and limitations. 
機械学習のためのデータ管理の領域を進むと、各々が独自の機能と制限を持ついくつかの重要なコンポーネントに出会うことになります。
While feature stores are the stars of this guide, it's crucial to understand how they differ from traditional data stores and ETL (Extract, Transform, Load) pipelines. 
このガイドの主役は特徴ストアですが、従来のデータストアやETL（Extract, Transform, Load）パイプラインとの違いを理解することが重要です。
This will not only help you make informed decisions but also enable you to integrate these components seamlessly. 
これにより、情報に基づいた意思決定ができるだけでなく、これらのコンポーネントをシームレスに統合することも可能になります。

### The Role of a Feature Store 特徴ストアの役割

A feature store is more than just a specialized repository for machine learning features; it's an integral part of the ML ecosystem that manages the entire lifecycle of feature engineering. 
特徴ストアは、機械学習の特徴のための専門的なリポジトリ以上のものであり、特徴エンジニアリングの全ライフサイクルを管理するMLエコシステムの不可欠な部分です。
While we will delve into its architecture in the following sections, it's important to understand that a feature store is not merely a data storage solution. 
次のセクションではそのアーキテクチャについて詳しく掘り下げますが、特徴ストアは単なるデータストレージソリューションではないことを理解することが重要です。
It provides a comprehensive framework for feature creation, versioning, and serving in both real-time and batch modes. 
特徴ストアは、リアルタイムおよびバッチモードの両方での特徴の作成、バージョン管理、提供のための包括的なフレームワークを提供します。
To gain a deeper understanding of what features are and why they are crucial in machine learning, you can read our article on What is a Feature Store. 
特徴とは何か、そしてそれが機械学習においてなぜ重要であるかをより深く理解するために、私たちの記事「[What is a Feature Store](https://www.qwak.com/post/what-is-a-feature-store-in-ml)」を読むことができます。

<!-- ここまで読んだ -->

### Traditional Data Stores 従来のデータストア

In contrast, traditional data stores like databases or data lakes are more general-purpose. 
**対照的に、データベースやデータレイクのような従来のデータストアは、より一般的な目的に使用されます**。
They are excellent for storing raw or processed data but lack the specialized capabilities for feature engineering and serving that feature stores offer. 
これらは、生データや処理済みデータの保存には優れていますが、フィーチャーストアが提供するフィーチャーエンジニアリングやサービングのための専門的な機能が欠けています。
For instance, they don't inherently support versioning of features or real-time serving with low latency. 
**例えば、従来のデータストアは、フィーチャーのバージョン管理や低遅延でのリアルタイムサービングを本質的にサポートしていません**。
While you could build these capabilities on top of a traditional data store, it would require significant engineering effort, something that's already taken care of in a feature store. 
従来のデータストアの上にこれらの機能を構築することは可能ですが、それにはかなりのエンジニアリングの努力が必要であり、これはフィーチャーストアですでに対処されています。

### ETL Pipelines

ETL pipelines, on the other hand, are the workhorses of data transformation. 
一方で、ETLパイプラインはデータ変換の作業馬です。
They are responsible for extracting data from various sources, transforming it into a usable format, and loading it into a data store. 
彼らは、さまざまなソースからデータを抽出し、それを使用可能な形式に変換し、データストアにロードする責任があります。
While ETL pipelines are essential for data preparation, they are not designed to manage the complexities of feature engineering for machine learning. 
ETLパイプラインはデータ準備に不可欠ですが、機械学習のための特徴エンジニアリングの複雑さを管理するようには設計されていません。
They are more like a one-way street, taking data from point A to point B, without the nuanced management and serving capabilities that feature stores offer. 
彼らは、特徴ストアが提供する微妙な管理や提供機能なしに、データをポイントAからポイントBに移動させる一方通行の通りのようなものです。

### The Interplay 相互作用

Understanding the distinctions doesn't mean choosing one over the others; it's about leveraging each for what it does best. 
区別を理解することは、他のものを選ぶことを意味するのではなく、それぞれの得意な部分を活用することです。
You could use ETL pipelines to prepare your raw data and load it into a traditional data store for initial storage. 
ETLパイプラインを使用して、生データを準備し、初期ストレージのために従来のデータストアにロードすることができます。
From there, the feature store can take over, ingesting this data, transforming it into valuable features, and serving them to your machine learning models. 
そこから、フィーチャーストアがデータを取り込み、それを価値のある特徴に変換し、機械学習モデルに提供する役割を果たします。
In this way, each component—ETL pipelines, traditional data stores, and feature stores—can play a harmonious role in your data ecosystem. 
このように、各コンポーネント（ETLパイプライン、従来のデータストア、フィーチャーストア）は、データエコシステムの中で調和のとれた役割を果たすことができます。
(データの流れとしては、従来のデータストア -> 特徴量パイプライン -> 特徴量ストア、ってイメージ:thinking:)

In the section that follows, we'll take a comprehensive look at the architectural components that make a feature store more than just a data repository. 
次のセクションでは、フィーチャーストアを単なるデータリポジトリ以上のものにするアーキテクチャコンポーネントを包括的に見ていきます。
We'll explore how it serves as a robust framework for feature engineering, management, and real-time serving, all while ensuring scalability and reliability. 
それが、フィーチャーエンジニアリング、管理、リアルタイム提供のための堅牢なフレームワークとして機能し、スケーラビリティと信頼性を確保する方法を探ります。

<!-- ここまで読んだ -->

## Feature Store Architecture: A Practical Guide for Building Your Own
フィーチャーストアアーキテクチャ：自分自身のための実用的なガイド

Before we roll up our sleeves and get our hands dirty with the nuts and bolts of a feature store, let's take a step back. 
フィーチャーストアの詳細に取り組む前に、一歩引いて考えてみましょう。
Imagine you're looking at a blueprint; it's easier to build a house when you know where each room goes, right? 
設計図を見ていると想像してみてください。各部屋の位置がわかっていると、家を建てるのが簡単ですよね？
The same logic applies here. 
ここでも同じ論理が適用されます。
A feature store design is essentially divided into three core layers, each with its own set of components and responsibilities: 
**フィーチャーストアの設計は本質的に3つのコアレイヤー**に分かれており、それぞれに独自のコンポーネントと責任があります：

### Data Infrastructure Layer データインフラストラクチャ層

Think of this as your foundation. 
これはあなたの基盤と考えてください。
It's where raw data is ingested, processed, and stored. 
生データが取り込まれ、処理され、保存される場所です。
This layer is the bedrock upon which everything else is built. 
この層は、他のすべてが構築される基盤です。
Key components include Batch and Stream Processing Engines, as well as Offline and Online Stores. 
主要なコンポーネントには、バッチおよびストリーム処理エンジン、ならびにオフラインおよびオンラインストアが含まれます。
(正直「バッチおよびストリーム処理エンジン」については、多くのfeature storeサービスでは含まれてないイメージ。特徴量生成パイプラインは、基本的にはfeature storeの外にあるイメージ...!:thinking:)

### Serving Layer サービングレイヤー

This is your front door, the gateway through which processed features are made accessible to applications and services. 
これはあなたのフロントドアであり、処理された特徴がアプリケーションやサービスにアクセス可能にするためのゲートウェイです。
It's optimized for speed and designed for scale. 
これは速度の最適化とスケールのために設計されています。
Here, you'll find RESTful APIs or gRPC services that serve your features. 
ここでは、あなたの特徴を提供するRESTful APIやgRPCサービスが見つかります。

<!-- ここまで読んだ! -->

### Application Layer アプリケーション層

Lastly, consider this your control room. 
最後に、これをあなたのコントロールルームと考えてください。
It's the orchestrator that ensures all other layers and components are working in harmony. 
これは、他のすべての層とコンポーネントが調和して機能することを保証するオーケストレーターです。
From job orchestration to feature tracking and system health monitoring, this layer keeps the ship sailing smoothly. 
ジョブのオーケストレーションから機能の追跡、システムの健康監視に至るまで、この層は船をスムーズに航行させます。

Understanding this Feature Store architecture is crucial because it informs every decision you'll make, from the tools you choose to the workflows you establish. 
このFeature Storeアーキテクチャを理解することは重要です。なぜなら、それはあなたが選ぶツールから確立するワークフローまで、あなたが下すすべての決定に影響を与えるからです。
So, keep this blueprint in mind as we delve deeper into each layer and its components. 
したがって、各層とそのコンポーネントにさらに深く掘り下げる際には、この設計図を心に留めておいてください。
Trust us, it'll make the journey ahead a lot less daunting. 
私たちを信じてください。そうすれば、これからの旅がずっと楽になるでしょう。

<!-- ここまで読んだ -->

## The Data Infrastructure Layer: Where It All Begins データインフラストラクチャ層：すべての始まり

The Data Infrastructure Layer is the backbone of your feature store. 
データインフラストラクチャ層は、あなたのフィーチャーストアの背骨です。

It's responsible for the initial stages of your data pipeline, including data ingestion, processing, and storage. 
この層は、データの取り込み、処理、保存を含むデータパイプラインの初期段階を担当しています。

This layer sets the stage for the more specialized operations that follow, making it crucial for the scalability and reliability of your entire system. 
この層は、その後のより専門的な操作のための基盤を整え、システム全体のスケーラビリティと信頼性にとって重要です。



## Batch Processing Engine バッチ処理エンジン

The batch processing engine serves as the computational hub where raw data is transformed into features. 
バッチ処理エンジンは、生データが特徴に変換される計算の中心として機能します。
It's designed to handle large datasets that don't require real-time processing and prepares them for storage in the offline feature store.
これは、リアルタイム処理を必要としない大規模データセットを処理するように設計されており、オフラインフィーチャーストアへの保存のためにそれらを準備します。



### Considerations 考慮事項

- Data Consistency - Consistency is key for maintaining the integrity of machine learning models. 
- データの一貫性 - 一貫性は、機械学習モデルの整合性を維持するための鍵です。 
Ensure that features generated are consistent across different runs.
生成された特徴が異なる実行間で一貫していることを確認してください。

- Versioning - Keep track of different versions of features. 
- バージョニング - 異なるバージョンの特徴を追跡します。 
If a feature is updated or deprecated, this should be captured.
特徴が更新または廃止された場合は、これを記録する必要があります。

- Concurrency - Plan for multiple batch jobs running simultaneously to ensure they don't conflict with each other in the feature store.
- 同時実行 - 複数のバッチジョブが同時に実行されるように計画し、特徴ストア内で互いに競合しないようにします。



### Relevance to SDK Concepts SDK概念との関連性

- Data Sources - The engine is where raw data from various SDK-defined sources like SQL databases, flat files, or external APIs is ingested. 
- データソース - エンジンは、SQLデータベース、フラットファイル、または外部APIなど、さまざまなSDK定義のソースから生データを取り込む場所です。 
Consider the latency and throughput requirements of these data sources when designing your SDK.
SDKを設計する際には、これらのデータソースのレイテンシとスループットの要件を考慮してください。

- Feature Transformations - The engine executes SDK-defined transformations. 
- 特徴変換 - エンジンはSDK定義の変換を実行します。 
Depending on the type of machine learning model, different transformations may be more suitable. 
機械学習モデルの種類によって、異なる変換がより適切である場合があります。 
For example, for classification models, you might consider label encoding, while for regression models, polynomial features could be useful.
例えば、分類モデルの場合はラベルエンコーディングを考慮するかもしれませんが、回帰モデルの場合は多項式特徴が有用である可能性があります。



### Best Practices 最良の実践

- Batch Sizing - Choose batch sizes that optimize both computational speed and system load. 
- バッチサイズ - 計算速度とシステム負荷の両方を最適化するバッチサイズを選択します。 
For time-series data, you might opt for daily or hourly batches.
時系列データの場合、日次または時間単位のバッチを選択することができます。

- Feature Validation - Implement checks to ensure that computed features meet quality and consistency standards, akin to a quality check before a dish leaves the kitchen.
- 特徴の検証 - 計算された特徴が品質と一貫性の基準を満たしていることを確認するためのチェックを実装します。これは、料理がキッチンを出る前の品質チェックに似ています。

- Dependency Management - Manage the order in which features are computed, especially if one feature depends on another, similar to the steps in a recipe.
- 依存関係の管理 - 特徴が計算される順序を管理します。特に、ある特徴が別の特徴に依存している場合は、レシピの手順に似ています。



### Highlighted Option 強調されたオプション

- Apache Spark - Spark offers a distributed computing environment that's highly scalable and fault-tolerant. 
- Apache Spark - Sparkは、高度にスケーラブルでフォールトトレラントな分散コンピューティング環境を提供します。
It supports a wide range of data sources and formats, making it versatile for various feature engineering tasks. 
さまざまなデータソースとフォーマットをサポートしており、さまざまな特徴量エンジニアリングタスクに対して柔軟性があります。
Its native support for machine learning libraries also makes it a robust choice for feature computation and storage in a feature store. 
機械学習ライブラリへのネイティブサポートにより、特徴量計算と特徴量ストアでのストレージにおいても堅牢な選択肢となります。



## Stream Processing Engine ストリーム処理エンジン

The Stream Processing Engine is like the "fast-food counter" of your data infrastructure, designed to handle real-time data processing needs. 
ストリーム処理エンジンは、データインフラストラクチャの「ファーストフードカウンター」のようなもので、リアルタイムデータ処理のニーズに対応するように設計されています。

It processes data as it arrives, making it ideal for applications that require real-time analytics and monitoring.
データが到着する際に処理を行い、リアルタイム分析や監視を必要とするアプリケーションに最適です。



### Considerations 考慮事項

- Latency - Unlike batch processing, latency is a critical factor here. 
- レイテンシ - バッチ処理とは異なり、レイテンシはここで重要な要素です。
The system should be capable of processing data with minimal delay.
システムは、最小限の遅延でデータを処理できる必要があります。

- Scalability - As data streams can be highly variable, the system should be able to scale up or down quickly.
- スケーラビリティ - データストリームは非常に変動する可能性があるため、システムは迅速にスケールアップまたはスケールダウンできる必要があります。

- Data Integrity and Fixes - Mistakes happen, and sometimes incorrect data gets streamed. 
- データの整合性と修正 - ミスは起こり得るものであり、時には不正確なデータがストリーミングされることがあります。
Your engine should not only handle out-of-order or late-arriving data but also be capable of correcting these errors either in real-time or through subsequent batch recalculations.
あなたのエンジンは、順序が乱れたデータや遅れて到着したデータを処理するだけでなく、リアルタイムでまたはその後のバッチ再計算を通じてこれらのエラーを修正できる必要があります。



### Relevance to SDK Concepts SDK概念との関連性

- Data Sources - This engine typically deals with real-time data sources defined in the SDK, such as Kafka streams, IoT sensors, or real-time APIs.
- データソース - このエンジンは通常、SDKで定義されたリアルタイムデータソース（例：Kafkaストリーム、IoTセンサー、リアルタイムAPI）を扱います。

- Feature Transformations - Stream-specific transformations like windowed aggregates or real-time anomaly detection can be executed here. 
- 特徴変換 - ウィンドウ集約やリアルタイム異常検出のようなストリーム特有の変換がここで実行できます。

- For instance, if you're working on a fraud detection system, real-time transformations could flag unusual transaction patterns.
- 例えば、詐欺検出システムに取り組んでいる場合、リアルタイム変換は異常な取引パターンをフラグ付けすることができます。



### Best Practices 最良の実践

- State Management - Keep track of the state of data streams, especially if your features require data from multiple streams or have temporal dependencies.
- 状態管理 - データストリームの状態を追跡し、特に特徴が複数のストリームからのデータを必要とする場合や時間的依存関係がある場合に注意してください。

- Fault Tolerance - Implement mechanisms to recover from failures, ensuring that no data is lost and processing can resume smoothly.
- フォールトトレランス - 障害から回復するためのメカニズムを実装し、データが失われず、処理がスムーズに再開できるようにします。

- Adaptive Scaling - Rather than imposing rate limits, focus on building a system that scales according to the demands of the incoming data streams.
- アダプティブスケーリング - レート制限を課すのではなく、受信データストリームの要求に応じてスケールするシステムを構築することに焦点を当てます。



### Highlighted Option 強調されたオプション

- Apache Spark Structured Streaming - We recommend Apache Spark Structured Streaming for its fault-tolerance, ease of use, and native integration with the Spark SQL engine. 
- Apache Spark Structured Streamingは、その耐障害性、使いやすさ、およびSpark SQLエンジンとのネイティブ統合のために推奨します。
It allows for complex event-time-based window operations and supports various sources and sinks, making it versatile for real-time analytics and feature computation in a feature store. 
これは、複雑なイベント時間ベースのウィンドウ操作を可能にし、さまざまなソースとシンクをサポートするため、リアルタイム分析やフィーチャーストアでのフィーチャー計算において多用途です。
Its compatibility with the broader Spark ecosystem and DataFrame API makes it a robust choice for both batch and real-time data processing. 
より広範なSparkエコシステムおよびDataFrame APIとの互換性により、バッチ処理とリアルタイムデータ処理の両方において堅牢な選択肢となります。
The mature ecosystem, extensive community, and commercial support further solidify its standing as a go-to option for structured streaming tasks. 
成熟したエコシステム、広範なコミュニティ、および商業サポートは、構造化ストリーミングタスクのための選択肢としての地位をさらに強固にします。



## Offline Store オフラインストア

The Offline Store acts as your "data warehouse," a secure and organized place where feature data is stored after being processed by the batch or stream engines. 
オフラインストアは「データウェアハウス」として機能し、バッチまたはストリームエンジンによって処理された後の特徴データが保存される、安全で整理された場所です。
It's designed to handle large volumes of data and is optimized for batch analytics.
大量のデータを処理できるように設計されており、バッチ分析に最適化されています。



### Considerations 考慮事項

- Data Retention - Decide how long the data should be stored, considering both storage costs and data utility.
- データ保持 - ストレージコストとデータの有用性の両方を考慮して、データをどのくらいの期間保存するかを決定します。

- Accessibility - Ensure that the data is easily accessible for batch analytics but also secure.
- アクセシビリティ - データがバッチ分析のために簡単にアクセスできるようにしつつ、安全であることを確認します。

- Data Schema - Maintain a consistent schema to ensure that the data is easily interpretable and usable.
- データスキーマ - データが簡単に解釈可能で使用可能であることを保証するために、一貫したスキーマを維持します。



### Relevance to SDK Concepts SDK概念との関連

- Feature Sets - Feature sets are groups of features that share a common concept or relation. 
- フィーチャーセット - フィーチャーセットは、共通の概念や関係を持つフィーチャーのグループです。 

They are defined in the SDK and stored here. 
これらはSDKで定義され、ここに保存されます。 

These could range from simple numerical features to more complex types like pre-processed text or images. 
これらは、単純な数値フィーチャーから、前処理されたテキストや画像のようなより複雑なタイプまでさまざまです。 

For example, if you're building a recommendation engine, your feature set might include user behavior metrics like click-through rates, time spent on page, and purchase history. 
例えば、推薦エンジンを構築している場合、フィーチャーセットにはクリック率、ページ滞在時間、購入履歴などのユーザー行動指標が含まれるかもしれません。 

These features are related because they all contribute to understanding user preferences. 
これらのフィーチャーは、すべてユーザーの好みを理解するのに寄与するため、関連しています。 

- Feature Retrieval - This is your go-to for batch retrieval of features, often used for training machine learning models. 
- フィーチャーリトリーバル - これは、フィーチャーのバッチ取得のためのもので、機械学習モデルのトレーニングによく使用されます。 

Time-travel support is a part of this, allowing you to query features as they appeared at a specific point in time, which is useful for debugging or auditing. 
タイムトラベルサポートはその一部であり、特定の時点でのフィーチャーの状態をクエリできるようにし、デバッグや監査に役立ちます。



### Best Practices 最良の実践

- ACID Transactions - Implement ACID (Atomicity, Consistency, Isolation, Durability) transactions to ensure data integrity.
- ACIDトランザクション - データの整合性を確保するために、ACID（原子性、一貫性、隔離性、耐久性）トランザクションを実装します。
- Indexing - Use indexing to speed up data retrieval, especially for large datasets.
- インデクシング - 特に大規模データセットに対して、データの取得を高速化するためにインデクシングを使用します。
- Data Validation - Before storing, validate the data to ensure it meets the quality and consistency requirements.
- データ検証 - 保存する前に、データが品質と一貫性の要件を満たしていることを確認するために検証します。



### Highlighted Option 強調されたオプション

- S3 with Delta or Iceberg files - Think of this as your high-security, climate-controlled warehouse. 
- DeltaまたはIcebergファイルを使用したS3 - これは、高セキュリティで気候制御された倉庫のようなものです。
These file formats offer ACID transactions, scalable metadata handling, and unify streaming and batch data processing, making them a robust choice for an offline store.
これらのファイル形式は、ACIDトランザクション、スケーラブルなメタデータ処理を提供し、ストリーミングとバッチデータ処理を統合するため、オフラインストアにとって堅牢な選択肢となります。



## Online Store オンラインストア

The Online Store is akin to your "retail shop," designed for low-latency access to feature data. 
オンラインストアは、あなたの「小売店」に似ており、特徴データへの低遅延アクセスのために設計されています。
It's optimized for quick reads and is the go-to place for real-time applications.
これは迅速な読み取りのために最適化されており、リアルタイムアプリケーションのための主要な場所です。



### Considerations 考慮事項

- Latency - Low-latency is crucial here; data should be retrievable in milliseconds.
- レイテンシ - 低レイテンシはここで重要です。データはミリ秒単位で取得可能であるべきです。
- High Availability - The store should be highly available to meet the demands of real-time applications.
- 高可用性 - ストレージはリアルタイムアプリケーションの要求を満たすために高可用性であるべきです。
- Scalability - As the number of features or the request rate grows, the system should scale seamlessly.
- スケーラビリティ - 機能の数やリクエストレートが増加するにつれて、システムはシームレスにスケールするべきです。



### Relevance to SDK Concepts SDK概念との関連性

- Feature Retrieval - This is the primary source for real-time feature retrieval, often for serving machine learning models in production.
- 特徴取得 - これは、リアルタイムの特徴取得の主要なソースであり、しばしば生産環境で機械学習モデルを提供するために使用されます。

- On-Demand Feature Computation - If the SDK supports it, some lightweight feature computation can also be done here in real-time.
- オンデマンド特徴計算 - SDKがそれをサポートしている場合、ここで軽量な特徴計算もリアルタイムで行うことができます。



### Best Practices 最良の実践

- Data Partitioning - Use partitioning strategies to distribute data across multiple servers for better performance.
- データパーティショニング - 複数のサーバーにデータを分散させるためのパーティショニング戦略を使用して、パフォーマンスを向上させます。

- Caching - Implement caching mechanisms to speed up frequent data retrievals.
- キャッシング - 頻繁なデータ取得を高速化するためにキャッシングメカニズムを実装します。

- Consistency - It's crucial to maintain data consistency between the online and offline stores. This is especially important if both stores are updated simultaneously. Transactional integrity and recoverability are key here. 
- 一貫性 - オンラインストアとオフラインストア間でデータの一貫性を維持することが重要です。これは、両方のストアが同時に更新される場合に特に重要です。トランザクションの整合性と回復可能性がここでは重要です。

For instance, if data is successfully written to the offline store but fails to write to the online store, you'll need a robust mechanism to handle such discrepancies and recover gracefully.
例えば、データがオフラインストアに正常に書き込まれたが、オンラインストアへの書き込みに失敗した場合、そのような不一致を処理し、優雅に回復するための堅牢なメカニズムが必要です。



### Highlighted Option 強調されたオプション

- Redis Caching - Redis is an open-source, in-memory data structure store that provides ultra-fast read and write operations. 
- Redisはオープンソースのインメモリデータ構造ストアで、超高速の読み取りおよび書き込み操作を提供します。
Its low-latency and high-throughput capabilities make it an excellent choice for serving features in real-time machine learning applications. 
その低遅延および高スループットの能力は、リアルタイム機械学習アプリケーションで機能を提供するための優れた選択肢となります。
With various data structures and atomic operations, Redis offers the flexibility to design efficient feature stores tailored to specific needs. 
さまざまなデータ構造と原子的操作を備えたRedisは、特定のニーズに合わせた効率的なフィーチャーストアを設計する柔軟性を提供します。



## The Serving Layer: API-Driven Feature Access サービングレイヤー：API駆動のフィーチャーアクセス

The Serving Layer is your "customer service desk," the interface where external applications and services request and receive feature data. 
サービングレイヤーは「カスタマーサービスデスク」であり、外部アプリケーションやサービスがフィーチャーデータを要求し受け取るインターフェースです。

It's optimized for high availability and low latency, ensuring that features can be served quickly and reliably.
これは高い可用性と低遅延のために最適化されており、フィーチャーが迅速かつ信頼性高く提供されることを保証します。



### Considerations 考慮事項

- API Design - The APIs should be designed for ease of use, with clear documentation and versioning.  
- API設計 - APIは使いやすさを考慮して設計されるべきであり、明確なドキュメントとバージョン管理が必要です。

- Load Balancing - Distribute incoming requests across multiple servers to ensure high availability and low latency.  
- 負荷分散 - 高可用性と低遅延を確保するために、受信リクエストを複数のサーバーに分散させるべきです。

- Security - Implement authentication and authorization mechanisms to control access to feature data.  
- セキュリティ - 機能データへのアクセスを制御するために、認証および認可メカニズムを実装するべきです。



### Relevance to SDK Concepts SDK概念との関連

- Feature Retrieval - This layer is responsible for serving features to external applications, usually through RESTful APIs or gRPC services defined in the SDK.
- 特徴取得 - このレイヤーは、通常SDKで定義されたRESTful APIまたはgRPCサービスを通じて、外部アプリケーションに特徴を提供する責任があります。

- On-the-Fly Computations - In addition to serving precomputed features, this layer can also perform lightweight computations in real-time as per the SDK's capabilities. 
- 即時計算 - このレイヤーは、事前に計算された特徴を提供するだけでなく、SDKの機能に応じてリアルタイムで軽量な計算を行うこともできます。

For example, if you're serving features for a recommendation engine, you might need to calculate the "popularity score" of an item based on real-time user interactions. 
例えば、推薦エンジンのために特徴を提供している場合、リアルタイムのユーザーインタラクションに基づいてアイテムの「人気スコア」を計算する必要があるかもしれません。

This score could be computed on-the-fly at the Serving Layer before being sent to the application.
このスコアは、アプリケーションに送信される前に、サービングレイヤーで即時に計算される可能性があります。



### Best Practices 最良の実践

- Rate Limiting - Implement rate limiting to prevent abuse and ensure fair usage.  
- レート制限 - 悪用を防ぎ、公平な使用を確保するためにレート制限を実装します。

- Monitoring - Keep track of API usage, errors, and latency for ongoing optimization.  
- モニタリング - APIの使用状況、エラー、およびレイテンシを追跡し、継続的な最適化を行います。

- Caching - Use caching mechanisms to speed up frequent data retrievals, much like a well-organized customer service desk that quickly retrieves common forms or information for customers.  
- キャッシング - よく整理されたカスタマーサービスデスクが顧客のために一般的なフォームや情報を迅速に取得するように、頻繁なデータ取得を加速するためにキャッシングメカニズムを使用します。



### Highlighted Option 強調されたオプション

- Kubernetes - For a robust Serving Layer, we recommend a Kubernetes Cluster with the managed service provider of your choice. 
- Kubernetes - 堅牢なサービングレイヤーのために、選択したマネージドサービスプロバイダーと共にKubernetesクラスターを推奨します。
Complement this with Prometheus for real-time monitoring of system metrics and Kafka for effective rate limiting. 
これにPrometheusを追加してシステムメトリクスのリアルタイム監視を行い、効果的なレート制限のためにKafkaを使用します。
When you have a high volume of incoming requests, these services can queue them up and feed them to the serving layer at a controlled rate. 
高いボリュームの着信リクエストがある場合、これらのサービスはリクエストをキューに入れ、制御されたレートでサービングレイヤーに供給することができます。
This helps in preventing the system from being overwhelmed and ensures that resources are used optimally. 
これにより、システムが圧倒されるのを防ぎ、リソースが最適に使用されることが保証されます。
Rate limiting is especially important to prevent abuse and ensure fair usage of resources. 
レート制限は、悪用を防ぎ、リソースの公平な使用を確保するために特に重要です。



## The Application Layer: The Control Tower アプリケーション層：コントロールタワー

The Application Layer serves as the orchestrator for your feature store. 
アプリケーション層は、あなたのフィーチャーストアのオーケストレーターとして機能します。

It manages the data pipelines, keeps track of features and their metadata, and monitors the system's health. 
この層は、データパイプラインを管理し、フィーチャーとそのメタデータを追跡し、システムの健康状態を監視します。

This layer ensures that all components of your feature store work in harmony, making it key for the system's overall performance and reliability. 
この層は、フィーチャーストアのすべてのコンポーネントが調和して機能することを保証し、システム全体のパフォーマンスと信頼性にとって重要です。



## Job Orchestrator ジョブオーケストレーター

The Job Orchestrator is the "conductor of the orchestra," coordinating various components to work in harmony. 
ジョブオーケストレーターは「オーケストラの指揮者」であり、さまざまなコンポーネントが調和して動作するように調整します。
It orchestrates your data pipelines, ensuring that tasks are executed in the correct sequence and managing dependencies between them.
それはあなたのデータパイプラインをオーケストレーションし、タスクが正しい順序で実行されることを保証し、それらの間の依存関係を管理します。



### Considerations 考慮事項

- Workflow Design - Define clear Directed Acyclic Graphs (DAGs) or workflows that outline the sequence and dependencies of tasks.
- ワークフローデザイン - タスクの順序と依存関係を概説する明確な有向非巡回グラフ（DAG）またはワークフローを定義します。



### Relevance to SDK Concepts SDK概念との関連

- Feature Sets - The orchestrator triggers the computation and storage of feature sets defined in the SDK.
- フィーチャーセット - オーケストレーターは、SDKで定義されたフィーチャーセットの計算と保存をトリガーします。



### Best Practices 最良の実践

- Idempotency - Design tasks to be idempotent, meaning they can be safely retried without side effects, akin to a conductor who can restart a musical piece without causing confusion.
  - 冪等性 - タスクを冪等に設計し、つまり副作用なしに安全に再試行できるようにします。これは、指揮者が混乱を引き起こすことなく音楽の作品を再開できることに似ています。

- Integrated Monitoring and Logging - Incorporate monitoring dashboards and job logs into the feature store UI for rapid debugging without compromising access. This allows for a centralized view of job performance and issues, facilitating quicker resolution. Monitoring could include tracking the 'freshness' of data, latency, and error rates. For example, if you're ingesting real-time stock prices, you might set an alert if data hasn't been updated in the last 5 minutes.
  - 統合モニタリングとロギング - モニタリングダッシュボードとジョブログをフィーチャーストアのUIに組み込んで、アクセスを損なうことなく迅速なデバッグを可能にします。これにより、ジョブのパフォーマンスと問題の中央集約的なビューが提供され、迅速な解決が促進されます。モニタリングには、データの「新鮮さ」、レイテンシ、エラーレートの追跡が含まれる場合があります。たとえば、リアルタイムの株価を取り込んでいる場合、データが最後の5分間更新されていない場合にアラートを設定することができます。

- Data Validation and Alerting - While it's challenging to ensure the absolute correctness of computed data, implementing data validation checks and alerting mechanisms can help. For instance, if an ETL job is supposed to aggregate sales data, a sudden 50% drop in sales might trigger an alert for manual review.
  - データ検証とアラート - 計算されたデータの絶対的な正確性を保証することは難しいですが、データ検証チェックとアラートメカニズムを実装することで助けることができます。たとえば、ETLジョブが売上データを集約することになっている場合、売上が突然50%減少すると、手動レビューのためのアラートがトリガーされる可能性があります。



### Highlighted Option 強調されたオプション

- Airflow - Airflow is an open-source platform designed to programmatically author, schedule, and monitor workflows. 
- Airflowは、プログラム的にワークフローを作成、スケジュール、および監視するために設計されたオープンソースのプラットフォームです。
Its rich set of features and extensibility make it a robust choice for orchestrating complex data pipelines, including those in MLOps. 
その豊富な機能セットと拡張性により、MLOpsを含む複雑なデータパイプラインをオーケストレーションするための堅牢な選択肢となります。
With native support for defining task dependencies and scheduling, Airflow provides a comprehensive solution for workflow management. 
タスクの依存関係とスケジューリングを定義するためのネイティブサポートを備えたAirflowは、ワークフロー管理のための包括的なソリューションを提供します。
It also offers integration points for monitoring and alerting through tools like Prometheus and Grafana, or alerting services like PagerDuty. 
また、PrometheusやGrafanaなどのツールや、PagerDutyのようなアラートサービスを通じて、監視およびアラートのための統合ポイントも提供しています。



## Feature Registry (Metadata Store) 特徴レジストリ（メタデータストア）

The Feature Registry serves as the "library catalog" of your feature store, maintaining metadata about each feature, its lineage, and other attributes. 
特徴レジストリは、フィーチャーストアの「図書館カタログ」として機能し、各特徴のメタデータ、その系譜、およびその他の属性を維持します。
It's the backbone that supports CRUD operations for metadata and offers feature lineage tracking.
これは、メタデータのCRUD操作をサポートし、特徴の系譜追跡を提供するバックボーンです。



### Considerations 考慮事項

- Metadata Schema - Define a clear schema for metadata, including feature names, types, and lineage information.
- メタデータスキーマ - 特徴名、タイプ、および系譜情報を含むメタデータの明確なスキーマを定義します。

- Searchability - Ensure that features can be easily searched and retrieved based on their metadata.
- 検索可能性 - 特徴がそのメタデータに基づいて簡単に検索および取得できるようにします。

- Versioning - Implement versioning for features to track changes over time.
- バージョニング - 特徴のバージョニングを実装して、時間の経過に伴う変更を追跡します。



### Relevance to SDK Concepts SDK概念との関連

- Feature Sets - Metadata about feature sets defined in the SDK is stored here. 
- Feature Sets - SDKで定義されたフィーチャセットに関するメタデータがここに保存されています。
This includes details like feature types, default values, and data sources.
これには、フィーチャタイプ、デフォルト値、データソースなどの詳細が含まれます。



### Best Practices 最良の実践

- Data Lineage - Maintain a record of the lineage of each feature, showing its journey from source to serving. 
  - データの系譜 - 各特徴量の系譜の記録を維持し、ソースから提供までの旅を示します。これは、書籍をリストするだけでなく、その起源や図書館に到着するまでの経緯を示す図書館のカタログに似ています。

- Access Control - Implement fine-grained access control to restrict who can view or modify feature metadata. 
  - アクセス制御 - 特徴量のメタデータを表示または変更できる人を制限するために、細かいアクセス制御を実装します。

- Audit Trails - Keep logs of who accessed or modified features, similar to a library's borrowing history. 
  - 監査証跡 - 誰が特徴量にアクセスまたは変更したかのログを保持します。これは、図書館の貸出履歴に似ています。



### Highlighted Option 強調されたオプション

- PostgreSQL with Feast - This relational database offers robust capabilities for storing metadata. 
- PostgreSQL with Feast - このリレーショナルデータベースは、メタデータを保存するための堅牢な機能を提供します。
When used in conjunction with Feast, a feature store framework, you get additional benefits like feature lineage tracking and easy integration with data pipelines.
Feastというフィーチャーストアフレームワークと組み合わせて使用することで、フィーチャーの系譜追跡やデータパイプラインとの簡単な統合などの追加の利点が得られます。



## The Control Plane コントロールプレーン

The Control Plane is the "air traffic control tower" of your feature store, overseeing all operations and ensuring they run smoothly. 
コントロールプレーンは、あなたのフィーチャーストアの「航空交通管制塔」であり、すべての操作を監視し、スムーズに実行されることを保証します。

It serves as the UI for data drift monitoring, access controls, and other management features.
それは、データドリフトの監視、アクセス制御、およびその他の管理機能のためのUIとして機能します。



### Best Practices 最良の実践

- Data Drift and Skew Monitoring - Implement algorithms to detect data drift and skew, which are crucial for maintaining the integrity of machine learning models.
- データドリフトとスキューの監視 - 機械学習モデルの整合性を維持するために重要なデータドリフトとスキューを検出するアルゴリズムを実装します。

- Alerting - Set up alerting mechanisms for critical events or anomalies, with integrations such as Slack Webhooks, Opsgenie, etc.
- アラート - Slack WebhooksやOpsgenieなどの統合を用いて、重要なイベントや異常に対するアラート機構を設定します。

- Audit Logs - Maintain logs for all operations, providing a clear history of changes and access, much like an air traffic control log.
- 監査ログ - すべての操作のログを保持し、変更とアクセスの明確な履歴を提供します。これは、航空交通管制ログのようなものです。



### Highlighted Option 強調されたオプション

- Serving Layer’s Kubernetes - Given that we recommend Kubernetes for the Serving Layer, it makes sense to use the same cluster for the Control Plane as well. 
- Serving LayerのKubernetes - Serving LayerにKubernetesを推奨していることを考えると、Control Planeにも同じクラスターを使用することは理にかなっています。
This offers a cohesive, scalable, and cost-effective management experience, and simplifies the architecture by reducing the number of services you need to manage.
これにより、一貫性があり、スケーラブルでコスト効果の高い管理体験が提供され、管理する必要のあるサービスの数を減らすことでアーキテクチャが簡素化されます。



## Wrapping Up まとめ

Building a feature store is not for the faint of heart; it's a complex endeavor that requires a deep understanding of both your data and the tools at your disposal. 
フィーチャーストアを構築することは簡単ではなく、データと利用可能なツールの両方を深く理解する必要がある複雑な作業です。しかし、良いニュースがあります：あなたは一人で進む必要はありません。 
From managed services to open-source projects, there are resources out there to help you on how to build a feature store. 
マネージドサービスからオープンソースプロジェクトまで、フィーチャーストアを構築するためのリソースが存在します。The key is to start with a solid foundation, and that begins with understanding the feature store architecture. 
重要なのは、しっかりとした基盤から始めることであり、それはフィーチャーストアのアーキテクチャを理解することから始まります。We've walked you through the Data Infrastructure, Serving, and Application Layers, demystifying the components that make them up. 
私たちは、データインフラストラクチャ、サービング、アプリケーションレイヤーを通じて、構成要素を明らかにしてきました。Remember, a feature store is more than just a sum of its parts; it's an ecosystem. 
フィーチャーストアは単なる部品の合計以上のものであり、それはエコシステムです。そして、どんなエコシステムでも、バランスが重要です。 

So as you embark on this journey, keep your eyes on the horizon but your feet firmly on the ground. 
この旅に出るときは、地平線に目を向けつつ、足はしっかりと地面に置いておいてください。After all, the future of machine learning is not just about algorithms; it's about features—how you store them, manage them, and serve them. 
結局のところ、機械学習の未来は単にアルゴリズムのことではなく、フィーチャー—それをどのように保存し、管理し、提供するかに関するものです。And that's a future worth building for. 
そして、それは構築する価値のある未来です。



## Say goodbye to complex AI & ML 複雑なAIとMLにさようなら

Chat with us to see the platform live and discover how we can help simplify your journey deploying AI in production. 
私たちとチャットして、プラットフォームをライブで確認し、AIを本番環境に展開する際の旅をどのように簡素化できるかを発見してください。



## Related posts 関連投稿  
### Building Robust Feature Engineering Pipelines: From Experimentation to Production
堅牢な特徴エンジニアリングパイプラインの構築：実験から生産へ



### Simplifying Machine Learning with the Qwak Feature Store 機械学習をQwakフィーチャーストアで簡素化する



### Uncovering the Power of Real-Time Feature Engineering in Machine Learning 機械学習におけるリアルタイム特徴エンジニアリングの力を明らかにする



## Get started with JFrog ML today. JFrog MLを今すぐ始めましょう。

Access JFrog ML to see how the best ML engineering and data science teams deploy models in production. 
JFrog MLにアクセスして、最高のMLエンジニアリングおよびデータサイエンスチームがどのようにモデルを本番環境にデプロイしているかを確認してください。
Say goodbye to complex MLOps and start delivering today. 
複雑なMLOpsにさようならを告げ、今日から提供を始めましょう。

Your AIPlatform. Built to Scale. 
あなたのAIプラットフォーム。スケールに対応しています。

© 2024 JFrog ML. All rights reserved. 
© 2024 JFrog ML. 全著作権所有。

Terms & Conditions 
利用規約

Privacy Notice 
プライバシー通知

Cookie Notice 
クッキー通知

Announcements Nav link 
お知らせナビリンク

Tab Link 
タブリンク

[Attributes by Finsweet] Disable scrolling 
[Finsweetによる属性] スクロールを無効にする

Include JS Cookie library 
JSクッキーライブラリを含める



## Privacy Preference Center プライバシー設定センター

Your Opt Out Preference Signal is Honored
あなたのオプトアウトの選好信号は尊重されます。

- Your Privacy
- あなたのプライバシー
- Strictly Necessary Cookies
- 厳密に必要なクッキー
- Performance Cookies
- パフォーマンスクッキー
- Functional Cookies
- 機能的クッキー
- Targeting Cookies
- ターゲティングクッキー



### Your Privacy あなたのプライバシー



### Strictly Necessary Cookies 厳密に必要なクッキー



### Performance Cookies パフォーマンスクッキー



### Functional Cookies 機能的クッキー



### Targeting Cookies ターゲティングクッキー
#### Your Privacy あなたのプライバシー
JFrog and our partners use cookies and other tracking technologies to gather information about you and how you interact with our websites and services. 
JFrogと私たちのパートナーは、あなたに関する情報や、私たちのウェブサイトやサービスとのインタラクションを把握するために、クッキーやその他のトラッキング技術を使用します。
As set forth in the table below, we use this information for a variety of purposes, such as for analytics, to optimize the performance of our website, to improve effectiveness of our advertising, and to remember your preferences. 
以下の表に示すように、私たちはこの情報をさまざまな目的で使用します。例えば、分析、ウェブサイトのパフォーマンスの最適化、広告の効果の向上、そしてあなたの好みを記憶するためです。
You can disable certain types of cookies using the Privacy Preference Center toggles below. 
以下のプライバシープリファレンスセンターのトグルを使用して、特定の種類のクッキーを無効にすることができます。
For more information, including which cookies/tracking technologies belong to the below categories, see our Privacy Notice and Cookie Policy. 
詳細情報、特に以下のカテゴリに属するクッキー/トラッキング技術については、私たちのプライバシー通知およびクッキーポリシーをご覧ください。

#### Strictly Necessary Cookies 厳密に必要なクッキー
These are technologies that the digital services need in order to function, and that enable you to move around and use the digital services. 
これらは、デジタルサービスが機能するために必要な技術であり、あなたがデジタルサービスを移動し、使用することを可能にします。
Without these essential technologies, the digital services will not perform as smoothly for you as we would like them to, and we may not be able to provide the digital services or certain features you request. 
これらの必須技術がなければ、デジタルサービスは私たちが望むようにスムーズに機能せず、デジタルサービスやあなたがリクエストする特定の機能を提供できない場合があります。
Examples of where these cookies are used include: to determine when you are signed in; to determine when your account has been inactive; and for other troubleshooting and security purposes. 
これらのクッキーが使用される例には、サインインしているかどうかの判断、アカウントが非アクティブであるかどうかの判断、その他のトラブルシューティングやセキュリティ目的が含まれます。

#### Performance Cookies パフォーマンスクッキー
These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. 
これらのクッキーは、訪問数やトラフィックソースをカウントすることを可能にし、私たちのサイトのパフォーマンスを測定し、改善することができます。
They help us to know which pages are the most and least popular and see how visitors move around the site. 
これにより、どのページが最も人気があり、どのページが最も人気がないかを知り、訪問者がサイト内をどのように移動するかを把握できます。
Although analytics technologies allow us to gather specific information about the pages that you visit and whether you have visited our digital services multiple times, we cannot use them to find out details such as your name or address. 
分析技術により、あなたが訪問したページや、私たちのデジタルサービスを複数回訪問したかどうかに関する特定の情報を収集することはできますが、あなたの名前や住所などの詳細を知るためには使用できません。
For more information about Google Analytics, please refer to "How Google Uses Information From Sites or Apps that Use Our Services," which can be found at www.google.com/policies/privacy/partners/, or any other URL Google may provide from time to time. 
Google Analyticsに関する詳細情報については、「Googleが私たちのサービスを使用するサイトやアプリからの情報をどのように使用するか」を参照してください。これはwww.google.com/policies/privacy/partners/で見つけることができるか、Googleが随時提供する他のURLを参照してください。

#### Functional Cookies 機能的クッキー
These are technologies that help enhance performance and functionality. 
これらは、パフォーマンスと機能を向上させるのに役立つ技術です。
For example, functionality cookies can be used to remember a user's region or remember language preferences and pages and products you have viewed in order to enhance and personalize your experience when you visit our digital services. 
例えば、機能的クッキーは、ユーザーの地域を記憶したり、言語の好みや、あなたが閲覧したページや製品を記憶するために使用され、私たちのデジタルサービスを訪問した際の体験を向上させ、パーソナライズすることができます。

#### Targeting Cookies ターゲティングクッキー
We use marketing technologies, including cookies and other conversion tracking tools, to improve the effectiveness of our online marketing efforts (such as personalized advertisements placed on other digital properties you may visit). 
私たちは、マーケティング技術、クッキーやその他のコンバージョントラッキングツールを使用して、オンラインマーケティング活動の効果を向上させます（例えば、あなたが訪れる可能性のある他のデジタルプロパティに配置されたパーソナライズされた広告など）。



### Cookie List クッキーリスト

Consent
同意

Leg.Interest
法的利益

checkbox label
チェックボックスラベル

label
ラベル

checkbox label
チェックボックスラベル

label
ラベル

checkbox label
チェックボックスラベル

label
ラベル

checkbox label
チェックボックスラベル

label
ラベル
