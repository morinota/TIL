## 0.1. refs 審判

- https://nexocode.com/blog/posts/lambda-vs-kappa-architecture/ https://nexocode.com/blog/posts/lambda-vs-kappa-architecture/

# 1. Lambda vs. Kappa Architecture. A Guide to Choosing the Right Data Processing Architecture for Your Needs ラムダ対ラムダ カッパ・アーキテクチャー ニーズに合ったデータ処理アーキテクチャの選択ガイド

DOROTA OWCZAREK - DECEMBER 30, 2022 - UPDATED ON APRIL 24, 2023
ドロタ・オウチャレク - 2022年12月30日 - 2023年4月24日更新

In today’s digital age, data is a crucial asset for businesses of all sizes.
今日のデジタル時代において、データはあらゆる規模の企業にとって極めて重要な資産である。
Unsurprisingly, choosing the right data processing architecture is a top priority for many organizations.
当然のことながら、適切なデータ処理アーキテクチャを選択することは、多くの組織にとって最優先事項である。
Two popular options for data processing architectures are Lambda and Kappa.
**データ処理アーキテクチャの一般的な選択肢は、LambdaとKappaである**。
(MLシステムの特徴量作成も、学習も、推論も、data processingの一種と言えそうだよな...!:thinking:)

In this blog post, we’ll dive deeply into the key features and characteristics of these architectures and provide a comparison to help you decide which one is the best fit for your business needs.
このブログポストでは、これらのアーキテクチャの主な特徴や特性について深く掘り下げ、ビジネスニーズに最適なアーキテクチャを決定するのに役立つ比較を提供します。
Whether you’re a data scientist, engineer, or business owner, this guide will provide valuable insights into the pros and cons of each architecture and help you make an informed decision on which one to choose.
あなたがデータサイエンティストであれ、エンジニアであれ、ビジネスオーナーであれ、このガイドは、各アーキテクチャの長所と短所についての貴重な洞察を提供し、どれを選ぶべきかについて十分な情報に基づいた決断を下す助けとなるだろう。

## 1.1. TL;DR ♪ TL;DR

- Data processing architectures like Lambda and Kappa help businesses analyze and extract valuable insights from their data in real-time.
  LambdaやKappaのようなデータ処理アーキテクチャは、企業がリアルタイムでデータを分析し、価値ある洞察を抽出するのに役立つ。
- Lambda architecture uses separate batch and stream processing systems, making it scalable and fault-tolerant but complex to set up and maintain (as it duplicates processing logic).
  **Lambdaアーキテクチャは、別々のバッチ処理とストリーム処理システムを使用**しており、scalableでfault-tolerantだが、セットアップとメンテナンスが複雑である（処理ロジックが重複しているため）。
  - (メモ) **fault-tolerant(フォールトトレラント, 耐障害性?)**とは??
    - tolerant = 「寛容な、耐性がある」みたいな形容詞。toにアクセントが付く感じ! :thinking:
    - エラーや障害が発生しても、正常に機能し続けることができる能力。
    - 「ソフトウェアアーキテクチャの基礎」のアーキテクチャ特性の1つに、似たような概念があったかも...?? つまり、「**Availability(可用性)が高い**」事と同義...?? :thinking:
      - -> chatGPTに聞いた感じでは、**「fault-tolerant なシステム」である事は、「high-available(高可用性な)システム」を実現するための要素の一つっぽい**...! :thinking:
      - Availability(可用性)は、システムがどれだけ長い時間、中断なくサービスを提供できるか、という概念。なので、システムがエラーや障害への耐性を持つ事(i.e. fault-tolerant)はその一部...!:thinking:
- Kappa architecture simplifies the pipeline with a single stream processing system as it treats all data as streams, providing flexibility and ease of maintenance, but requires experience in stream processing and distributed systems.
  **Kappaアーキテクチャは、すべてのデータをストリームとして扱う**ため、単一のストリーム処理システムを使用してパイプラインを簡素化し、柔軟性とメンテナンスの容易さを提供するが、ストリーム処理と分散システムに関する経験が必要である。
- Lambda architecture is well-suited when companies have mixed requirements for stream and batch processing, e.g., for real-time analytics and multiple batch processing tasks or data lakes, while Kappa architecture is ideal for continuous data pipelines, real-time data processing, and IoT systems.
  Lambdaアーキテクチャは、企業がストリーム処理とバッチ処理の混在要件を持っている場合に適してる。例えば、リアルタイム分析や複数のバッチ処理タスクやデータレイクなど。一方、Kappaアーキテクチャは、連続データパイプライン、リアルタイムデータ処理、IoTシステムに最適である。

- Businesses should consider their specific data processing needs and choose an architecture that aligns with their goals and requirements.
  企業は、特定のデータ処理ニーズを検討し、目標と要件に沿ったアーキテクチャを選択すべきである。

- If you’re considering implementing a modern data processing architecture, nexocode’s data engineers can help you make the right choice and ensure a seamless transition.
  もし、モダンなデータ処理アーキテクチャを導入することを検討しているなら、nexocodeのデータエンジニアが正しい選択をサポートし、シームレスな移行を確保します。

## 1.2. Data Processing Architectures データ処理アーキテクチャ

Data processing architectures are systems designed to efficiently handle the ingestion, processing, and storage of large amounts of data.
**データ処理アーキテクチャ**は、大量のデータの取り込み、処理、保存を効率的に処理するために設計されたシステムである。(MLシステムの場合は、「処理」に含まれそう? 全部かな。)
These architectures play a crucial role in modern businesses.
これらのアーキテクチャは、現代のビジネスにおいて重要な役割を果たしている。
They allow organizations to analyze and extract valuable insights from their data, which can be used to improve decision-making, optimize operations, and drive growth.
これにより、組織はデータから価値ある洞察を分析し抽出することができ、意思決定の改善、業務の最適化、成長の推進に活用できる。

There are several different types of data processing architectures, each with its own set of characteristics and capabilities.
データ処理アーキテクチャには、それぞれ異なる特性と機能を持ついくつかの異なるタイプがある。
Some famous examples include Lambda and Kappa architectures, which are designed to handle different types of data processing workloads like batch processing or real-time data processing and have their own unique strengths and weaknesses.
**有名な例としては、LambdaアーキテクチャとKappaアーキテクチャがあり**、バッチ処理やリアルタイムデータ処理などの異なるタイプのデータ処理ワークロードを処理するように設計されており、それぞれ独自の強みと弱みを持っている。
It’s essential for businesses to carefully consider their specific data processing needs and choose an architecture that aligns with their goals and requirements.
企業にとっては、自社の特定のデータ処理ニーズを慎重に検討し、目標と要件に沿ったアーキテクチャを選択することが重要である。(うんうん...!)

## 1.3. Lambda Architecture ラムダ・アーキテクチャ

### 1.3.1. Key Features and Characteristics of Lambda Architecture ラムダ・アーキテクチャの主な特徴と特徴

Lambda architecture is a data processing architecture that aims to provide a scalable, fault-tolerant, and flexible system for processing large amounts of data.
ラムダ・アーキテクチャは、大量のデータを処理するための**scalableでfault-tolerant(耐障害性)、flexibleな(柔軟な)システム**を提供することを目的としたデータ処理アーキテクチャである。
It was developed by Nathan Marz in 2011 as a solution to the challenges of processing data in real time at scale.
**2011年にネイサン・マーズによって開発されたもの**で、データをリアルタイムで大規模に処理するという課題に対するソリューションである。
(結構最近だ...!:thinking:)

The critical feature of Lambda architecture is that it uses two separate data processing systems to handle different types of data processing workloads.
**ラムダ・アーキテクチャの重要な特徴は、異なるタイプのデータ処理ワークロードを処理するために、2つの異なるデータ処理システムを使用すること**である。(??)
The first system is a batch processing system, which processes data in large batches and stores the results in a centralized data store, such as a data warehouse or a distributed file system.
第1のシステムはbatch処理システムで、大量のデータをバッチ処理し、その結果をデータウェアハウスや分散ファイルシステムなどの**集中型(centralized)データストアに保存する**。
The second system is a stream processing system, which processes data in real-time as it arrives and stores the results in a distributed data store.
第2のシステムはstream処理システムで、データが到着するとリアルタイムでデータを処理し、その結果を**分散(distributed)データストアに保存する**。

![Real-time stream processing and batch processing in Lambda Architecture](https://nexocode.com/images/real-time-and-batch-processing-with-flink.webp)
ラムダ・アーキテクチャにおけるリアルタイム・ストリーム処理とバッチ処理

In Lambda architecture, the four main layers work together to process and store large volumes of data.
ラムダ・アーキテクチャーでは、**4つの主要レイヤー**が連携して大量のデータを処理・保存する。
Here’s a brief overview of how each layer functions:
各レイヤーの機能を簡単に説明しよう：

#### 1.3.1.1. Data Ingestion Layer データ取り込みレイヤー

This layer collects and stores raw data from various sources, such as log files, sensors, message queues, and APIs.
このレイヤーは、ログファイル、センサー、メッセージキュー、APIなど、**さまざまなソースから生データを収集・保存する**。
The data is typically ingested in real time and fed to the batch layer and speed layer simultaneously.
**データは通常リアルタイムで取り込まれ、batchレイヤーとspeedレイヤーに同時に供給**される。

#### 1.3.1.2. Batch Layer (Batch processing) バッチレイヤー（バッチ処理）

The batch processing layer is responsible for processing historical data in large batches and storing the results in a centralized data store, such as a data warehouse or a distributed file system.
バッチ処理レイヤーは、過去のデータを大量にバッチ処理し、その結果をデータウェアハウスや分散ファイルシステムなどの集中型データストアに保存する役割を担っている。
This layer typically uses a batch processing framework, such as Hadoop or Spark, to process the data.
このレイヤーは通常、HadoopやSparkなどの**バッチ処理フレームワークを使用してデータを処理する**。
The batch layer is designed to handle large volumes of data and provide a complete view of all data.
batchレイヤーは、大量のデータを処理し、すべてのデータの完全なviewを提供するように設計されている。
(viewとは? = データを集約、加工、計算した結果のことっぽい? 成果物??:thinking:)

#### 1.3.1.3. Speed Layer (Real-Time Data Processing) スピードレイヤー（リアルタイムデータ処理）

The speed layer is responsible for processing real-time data as it arrives and storing the results in a distributed data store, such as a message queue or a NoSQL database.
スピード・レイヤーは、リアルタイムで送られてくるデータを処理し、その**結果をメッセージ・キューやNoSQLデータベースなどの分散データ・ストアに格納**する。
This layer typically uses a stream processing framework, such as Apache Flink or Apache Storm, to process data streams.
このレイヤーは通常、Apache FlinkやApache Stormなどの**ストリーム処理フレームワークを使用してデータストリームを処理する**。
The stream processing layer is designed to handle high-volume data streams and provide up-to-date views of the data.
ストリーム処理レイヤーは、大量のデータストリームを処理し、データの最新viewを提供するように設計されている。

#### 1.3.1.4. Serving Layer サービング・レイヤー

The serving layer is a component of Lambda architecture that is responsible for serving query results to users in real time.
サービング・レイヤーはラムダ・アーキテクチャのコンポーネントで、**クエリ結果をリアルタイムでユーザに提供する役割**を担う。
It is typically implemented as a layer on top of the batch and stream processing layers.
これは通常、batch処理レイヤーとstream処理レイヤーの上にレイヤーとして実装される。(ここで「上のレイヤーとして実装される」というのは、処理の下流側、みたいな意味合いっぽい。データ処理の流れにおいて、serving層はbatch層とspeed層に依存している、という状況っぽい...!:thinking:)
It is accessed through a query layer, which allows users to query the data using a query language, such as SQL or Apache Hive’s HiveQL.
クエリ・レイヤーを介してアクセスされ、SQLやApache HiveのHiveQLなどのクエリ言語を使用してデータにクエリを実行できる。

The serving layer is designed to provide fast and reliable access to query results, regardless of whether the data is being accessed from the batch or stream processing layers.
servicing層は、データがbatch処理レイヤーやstream処理レイヤーからアクセスされているかどうかに関係なく、クエリ結果への高速で信頼性の高いアクセスを提供するように設計されている。
It typically uses a distributed data store, such as a NoSQL database or a distributed cache, to store the query results and serve them to users in real time.
通常、NoSQLデータベースや分散キャッシュなどの分散データストアを使用してクエリ結果を保存し、リアルタイムでユーザーに提供する。

The serving layer is an essential component of Lambda architecture, as it allows users to access the data in a seamless and consistent manner, regardless of the underlying data processing architecture.
**サービング・レイヤーは、Lambdaアーキテクチャの重要なコンポーネントであり、基礎となるデータ処理アーキテクチャに関係なく、ユーザがデータにシームレスかつ一貫した方法でアクセスできるようにする**。
It also plays a crucial role in supporting real-time applications, such as dashboards and analytics, which require fast access to up-to-date data.
また、ダッシュボードやアナリティクスなど、最新のデータに素早くアクセスする必要があるリアルタイム・アプリケーションをサポートする上でも重要な役割を果たしている。

### 1.3.2. Pros and Cons of Using Lambda Architecture ラムダ・アーキテクチャの長所と短所

Here are some advantages of Lambda architecture:
ラムダ・アーキテクチャーの利点は以下の通りだ：

- **Scalability**: Lambda architecture is designed to handle large volumes of data and scale horizontally to meet the needs of the business.
  スケーラビリティ： ラムダ・アーキテクチャは、大量のデータを処理し、ビジネスのニーズに合わせて水平方向に拡張できるように設計されている。

- **Fault-tolerance**: Lambda architecture is designed to be fault-tolerant, with multiple layers and systems working together to ensure that data is processed and stored reliably.
  耐障害性： ラムダ・アーキテクチャはfault-tolerantであり、複数のレイヤーとシステムが連携して、データが信頼性を持って処理・保存されるように設計されている。

- **Flexibility**: Lambda architecture is flexible and can handle a wide range of data processing workloads, from historical batch processing to streaming architecture.
  柔軟性： ラムダ・アーキテクチャは柔軟性が高く、過去のバッチ処理からストリーミング・アーキテクチャまで、幅広いデータ処理ワークロードに対応できる。

While Lambda architecture offers a lot of advantages, it also has some significant drawbacks that businesses need to consider before deciding whether it is the right fit for their needs.
ラムダ・アーキテクチャには多くの利点がある一方、いくつかの重大な欠点もあるため、企業は自社のニーズに適しているかどうかを判断する前に考慮する必要がある。
Here are some disadvantages of using the Lambda architecture system:
ラムダ・アーキテクチャー・システムを使うデメリットをいくつか挙げてみよう：

- **Complexity**: Lambda architecture is a complex system that uses multiple layers and systems to process and store data.
  複雑さ： **ラムダ・アーキテクチャは、データの処理と保存に複数のレイヤーとシステムを使用する複雑なシステム**である。
  It can be challenging to set up and maintain, especially for businesses that are not familiar with distributed systems and data processing frameworks.
  特に分散システムやデータ処理フレームワークに慣れていない企業にとっては、セットアップやメンテナンスが難しい場合もある。
  Although its layers are designed for different pipelines, the underlining logic has duplicated parts causing unnecessary coding overhead for programmers.
  レイヤー達は異なるパイプラインのために設計されているが、その基本的なロジックには重複部分があり、プログラマにとって不要なコーディングのオーバーヘッドを引き起こす。

- **Errors and data discrepancies**: With doubled implementations of different workflows (although following the same logic, implementation matters), you may run into a problem of different results from batch and stream processing engines.
  エラーとデータの不一致： 異なるワークフローを二重に実装した場合（同じロジックに従うとはいえ、実装は重要である）、バッチ処理エンジンとストリーム処理エンジンの結果が異なるという問題に遭遇する可能性がある。
  Hard to find, hard to debug.
  見つけにくく、デバッグしにくい。

- **Architecture lock-in**: It may be super hard to reorganize or migrate existing data stored in the Lambda architecture.
  アーキテクチャのロックイン： ラムダ・アーキテクチャーに保存されている既存のデータを再編成したり移行したりするのは、非常に難しいかもしれない。

<!-- ここまで読んだ! -->

### 1.3.3. Use Cases for Lambda Architecture ラムダ・アーキテクチャの使用例

Lambda architecture is a data processing architecture that is well-suited for a wide range of data processing workloads.
Lambdaアーキテクチャは、幅広いデータ処理ワークロードに適しているデータ処理アーキテクチャである。
It is particularly useful for handling large volumes of data and providing low-latency query results, making it well-suited for real-time analytics applications, such as dashboards and reporting.
**特に大量のデータを処理し、低遅延のクエリ結果を提供するのに役立ち、ダッシュボードやレポートなどのリアルタイム分析アプリケーションに適している**。
Lambda architecture is also useful for batch processing tasks, such as data cleansing, transformation, and aggregation, and stream processing tasks, such as event processing, machine learning models, anomaly detection, and fraud detection.
Lambdaアーキテクチャは、データのクレンジング、変換、集約などのバッチ処理タスクや、イベント処理、機械学習モデル、異常検出、詐欺検出などのストリーム処理タスクにも役立つ。
In addition, Lambda architecture is often used to build data lakes, which are centralized repositories that store structured and unstructured data at rest, and is well-suited for handling the high-volume data streams generated by IoT devices.
さらに、Lambdaアーキテクチャは、構造化データと非構造化データを静的に保存する中央リポジトリであるデータレイクを構築するためによく使用され、IoTデバイスによって生成される大量のデータストリームを処理するのに適している。

<!-- ここまで読んだ! -->

## 1.4. Kappa Architecture カッパ・アーキテクチャー

### 1.4.1. Key Features and Characteristics of Kappa Architecture Kappaアーキテクチャの主な特長と特徴

Kappa architecture is a data processing architecture that is designed to provide a scalable, fault-tolerant, and flexible system for processing large amounts of data in real time.
Kappaアーキテクチャは、大量のデータをリアルタイムで処理するためのscalableでfault-tolerant、flexibleなシステムを提供するように設計されたデータ処理アーキテクチャである。(ここだけ見ると、Lambdaアーキテクチャとアーキテクチャ特性が似てるように感じる...!:thinking:)
It was developed as an alternative to Lambda architecture, which, as mentioned above, uses two separate data processing systems to handle different types of data processing workloads.
これは**Lambdaアーキテクチャの代替として開発されたもの**で、Lambdaアーキテクチャは異なるタイプのデータ処理ワークロードを処理するために2つの別々のデータ処理システムを使用している。
(なるほど...! 代替ならばアーキテクチャ特性が似てるのは納得か)

In contrast to Lambda, Kappa architecture uses a single data processing system to handle both batch processing and stream processing workloads, as it treats everything as streams.
**Lambdaとは対照的に、Kappaアーキテクチャは、すべてをストリームとして扱うため**、単一のデータ処理システムでバッチ処理とストリーム処理の両方のワークロードを処理する。
This allows it to provide a more streamlined and simplified data processing pipeline while still providing fast and reliable access to query results.
これにより、**よりスムーズで簡素化されたデータ処理パイプラインを提供**しつつ、クエリ結果への高速で信頼性の高いアクセスを提供できる。

#### 1.4.1.1. Speed Layer (Stream Layer) スピード・レイヤー（ストリーム・レイヤー）

In Kappa architecture, there is only one main layer: the stream processing layer.
Kappaアーキテクチャでは、**主要なレイヤーは1つだけ**である： stream処理レイヤー。
This layer is responsible for collecting, processing, and storing live streaming data.
**このレイヤーは、ライブ・ストリーミング・データの収集、処理、保存を担当する**。
You can think of it as an evolution of the Lambda approach with the batch processing system removed.
**Lambdaアプローチの進化形であり、バッチ処理システムが削除されたものと考えることができる**。
It is typically implemented using a stream processing engine, such as Apache Flink, Apache Storm, Apache Kinesis, Apache Kafka, (or many other stream processing frameworks) and is designed to handle high-volume data streams and provide fast and reliable access to query results.
これは通常、Apache Flink、Apache Storm、Apache Kinesis、Apache Kafkaなどのストリーム処理エンジンを使用して実装され、大量のデータストリームを処理し、クエリ結果への高速で信頼性の高いアクセスを提供するように設計されている。

The stream processing layer in Kappa architecture is divided into two main components: the ingestion component and the processing component.
Kappaアーキテクチャーのstream処理レイヤーは、**2つの主要なコンポーネント**に分かれている：**ingestionコンポーネントとprocessingコンポーネント**。

- **Ingestion component**: This component is responsible for collecting incoming data and storing raw data from various sources, such as log files, sensors, and APIs.
  インジェスト・コンポーネント： このコンポーネントは、ログファイル、センサー、APIなど、**さまざまなソースから受信データを収集し、生データを保存する役割**を担う。
  The data is typically ingested in real-time and stored in a distributed data store, such as a message queue or a NoSQL database.
  **データは通常リアルタイムで取り込まれ、メッセージキューやNoSQLデータベースなどの分散データストアに保存される**。

- **Processing component**: This component is responsible for processing the data as it arrives and storing the results in a distributed data store.
  処理コンポーネント： このコンポーネントは、**到着したデータを処理し、その結果を分散データストアに保存する役割**を担う。
  It is typically implemented using a stream processing engine, such as Apache Flink or Apache Storm, and is designed to handle high-volume data streams and provide fast and reliable access to query results.
  通常、Apache FlinkやApache Stormなどのストリーム処理エンジンを使用して実装され、大量のデータストリームを処理し、クエリ結果への高速で信頼性の高いアクセスを提供するように設計されている。
  In Kappa architecture, there is no separate serving layer.
  Kappaアーキテクチャでは、独立したサービングレイヤーは存在しない。
  Instead, the stream processing layer is responsible for serving query results to users in real time.
  その代わり、stream処理レイヤーがリアルタイムでユーザにクエリ結果を提供する役割を担っている。

The stream processing platforms in Kappa architecture are designed to be fault-tolerant and scalable, with each component providing a specific function in the real time data processing pipeline.
Kappaアーキテクチャーのストリーム処理プラットフォームは、fault-tolerantでscalableであり、各コンポーネントがリアルタイムデータ処理パイプラインで特定の機能を提供するように設計されている。

![Continuous stream processing - stream processing tools run operations on streaming data to enable real time analytics](https://nexocode.com/images/stream-processing-app.webp)
連続ストリーム処理 - ストリーム処理ツールがストリーミングデータ上で操作を実行してリアルタイムアナリティクスを可能にする

### 1.4.2. Pros and Cons of Using Kappa Architecture Kappaアーキテクチャーの長所と短所

Here are some advantages of using of Kappa architecture:
Kappaアーキテクチャーを使用する利点は以下の通りである：

- **Simplicity and streamlined pipeline**: Kappa architecture uses a single data processing system to handle both batch processing and stream processing workloads, which makes it simpler to set up and maintain compared to Lambda architecture.
  **シンプルさと合理化されたパイプライン**： Kappaアーキテクチャは、単一のデータ処理システムでバッチ処理とストリーム処理の両方のワークロードを処理するため、Lambdaアーキテクチャに比べて**セットアップと保守が簡単**である。
  This can make it easier to manage and optimize the data processing pipeline by reducing the coding overhead.
  これにより、コーディングのオーバーヘッドを削減することで、データ処理パイプラインを管理し、最適化することが容易になる。
- Enables high-throughput big data processing of historical data: Although it may feel that it is not designed for these set of problems, Kappa architecture can support these use cases with grace, enabling reprocessing directly from our stream processing job.
  **過去のデータを高スループットでビッグデータ処理できる**: Kappaアーキテクチャは、このような問題のために設計されていないように感じるかもしれないが、ストリーム処理ジョブから直接再処理を可能にすることで、これらのユースケースを優雅にサポートすることができる。(??)
- Ease of migrations and reorganizations: As there is only stream processing pipeline, you can perform migrations and reorganizations with new data streams created from the canonical data store.
  **移行や再編成が容易**： ストリーム処理パイプラインしかないため、正規データストアから作成された新しいデータストリームを使用して移行や再編成を実行できます。
- Tiered storage: Tiered storage is a method of storing data in different storage tiers, based on the access patterns and performance requirements of the data.
  **階層型ストレージ**： 階層型ストレージとは、**データのアクセスパターンとパフォーマンス要件に基づいて、異なるストレージ階層にデータを格納する方法**である。
  The idea behind tiered storage is to optimize storage costs and performance by storing different types of data on the most appropriate storage tier.
  階層型ストレージの背景にある考え方は、**異なるタイプのデータを最適なストレージ階層に格納することで、ストレージコストとパフォーマンスを最適化すること**である。(うんうん...!:thinking:)
  In Kappa architecture, tiered storage is not a core concept.
  Kappaアーキテクチャでは、階層型ストレージは中核概念ではない。
  However, it is possible to use tiered storage in conjunction with Kappa architecture, as a way to optimize storage costs and performance.
  しかし、ストレージコストとパフォーマンスを最適化する方法として、Kappaアーキテクチャと組み合わせて階層型ストレージを使用することは可能である。(Kappaアーキテクチャを階層型ストレージと組み合わせて使用する話っぽい...!:thinking:)
  For example, businesses may choose to store historical data in a lower-cost fault tolerant distributed storage tier, such as object storage, while storing real-time data in a more performant storage tier, such as a distributed cache or a NoSQL database.
  **例えば、企業は過去のデータをオブジェクトストレージのような低コストのフォールトトレラントな分散ストレージ層に保存する一方で、リアルタイムのデータを分散キャッシュやNoSQLデータベースのようなパフォーマンスの高いストレージ層に保存することを選択することができる**。
  Tiered storage Kappa architecture makes it a cost-efficient and elastic data processing technique without the need for a traditional data lake.
  **階層型ストレージのKappaアーキテクチャは、従来のデータレイクを必要とせず、コスト効率が高く、elastic(弾力的)なデータ処理手法となる**。

When it comes to disadvantages of Kappa architecture, we can mention the following aspects:
Kappaアーキテクチャーの欠点といえば、次のような点が挙げられる：

- Complexity: While Kappa architecture is simpler than Lambda, it can still be complex to set up and maintain, especially for businesses that are not familiar with stream processing frameworks (review common challenges in stream processing).
  複雑さ： KappaのアーキテクチャはLambdaよりもシンプルだが、特にストリーム処理フレームワークに慣れていない企業にとっては、セットアップやメンテナンスが複雑になる可能性がある（[ストリーム処理における一般的な課題](https://nexocode.com/blog/posts/data-stream-processing-challenges/)を参照）。

- Costly infrastructure with scalability issues (when not set properly): Storing big data in an event streaming platform can be costly.
  スケーラビリティの問題を抱えた、コストのかかるインフラ（適切に設定されていない場合）： イベント・ストリーミング・プラットフォームにビッグデータを保存するのはコストがかかる。
  To make it more cost-efficient you may want to use data lake approach from your cloud provider (like AWS S3 or GCP Google Cloud Storage).
  **より費用対効果を高めるには、クラウドプロバイダーのデータレイク・アプローチ（AWS S3やGCP Google Cloud Storageなど）を利用するとよい**だろう。
  Another common approach for big data architecture is building a “streaming data lake” with Apache Kafka as a streaming layer and object storage to enable long-term data storage.
  ビッグデータアーキテクチャのもう一つの一般的なアプローチは、ストリーミングレイヤーとしてApache Kafkaを使用し、長期的なデータ保存を可能にするオブジェクトストレージを使用して「ストリーミングデータレイク」を構築することである。(??)

<!-- ここまで読んだ! -->

### 1.4.3. Use Cases for Kappa Architecture Kappaアーキテクチャの使用例

Kappa architecture is a data processing architecture that is designed to provide a flexible, fault-tolerant, and scalable architecture for processing large amounts of data in real-time.
Kappaアーキテクチャは、大量のデータをリアルタイムで処理するための、柔軟性、耐障害性、拡張性を備えたデータ処理アーキテクチャである。
It is well-suited for a wide range of data processing workloads, including continuous data pipelines, real time data processing, machine learning models and real-time data analytics, IoT systems, and many other use cases with a single technology stack.
継続的なデータパイプライン、リアルタイムデータ処理、機械学習モデルやリアルタイムデータ分析、IoTシステム、その他多くのユースケースを含む幅広いデータ処理ワークロードに適しており、単一のテクノロジースタックで利用できる。

## 1.5. Comparison of Lambda and Kappa Architectures ラムダ・アーキテクチャとカッパ・アーキテクチャの比較

Both architectures are designed to provide scalable, fault-tolerant, and low latency systems for processing data, but they differ in terms of their underlying design and approach to data processing.
どちらのアーキテクチャも、データ処理のためのスケーラブルでフォールト・トレラントな低レイテンシー・システムを提供するように設計されているが、その基本設計とデータ処理へのアプローチの点で異なっている。

### 1.5.1. Data Processing Systems データ処理システム

Lambda architecture uses two separate data processing systems to handle different types of data processing workloads: a batch processing system and a stream processing system.
ラムダ・アーキテクチャは、異なるタイプのデータ処理ワークロードを処理するために、2つの独立したデータ処理システムを使用する： バッチ処理システムとストリーム処理システムだ。
In Kappa architecture, on the other hand, a single stream processing engine acts (stream layer) to handle complete data processing.
一方、Kappaアーキテクチャでは、1つのストリーム処理エンジンが完全なデータ処理を行う（ストリームレイヤー）。
In Lambda, programmers need to learn and maintain two processing frameworks and support any daily code changes in a doubled way.
ラムダでは、プログラマーは2つの処理フレームワークを学び、維持し、日々のコード変更を二重にサポートする必要がある。
This separation (when not implemented in the same way) may cause different results in stream vs.
この分離は（同じように実装されていない場合）、ストリーム対ストリームで異なる結果を引き起こす可能性がある。
batch processing, which may cause further business issues.
バッチ処理は、さらなるビジネス上の問題を引き起こす可能性がある。
Kappa Architecture uses the same code for processing data in real time, eliminating the need for additional effort to maintain separate codebases for batch and stream processing.
Kappaアーキテクチャーは、リアルタイムでデータを処理するために同じコードを使用するので、バッチ処理とストリーム処理のために別々のコードベースを維持するための新たな労力を必要としない。
This makes it a more efficient and error-proof solution.
そのため、より効率的でミスのないソリューションとなっている。

### 1.5.2. Data Storage データストレージ

Lambda architecture has a separate long-term data storage layer, which is used to store historical data and perform complex aggregations.
ラムダ・アーキテクチャには、過去のデータを保存し、複雑な集計を実行するために使用される、別の長期データ保存レイヤーがある。
Kappa architecture does not have a separate long-term data storage layer, and all data is processed and stored by the stream processing system.
Kappaアーキテクチャは、独立した長期データ保存層を持たず、すべてのデータはストリーム処理システムで処理され保存される。

### 1.5.3. Complexity 複雑さ

Lambda architecture is generally more complex to set up and maintain compared to Kappa architecture, as it requires two separate data processing systems and ongoing maintenance to ensure that the batch and stream processing systems are working correctly and efficiently.
一般的に、ラムダ・アーキテクチャは、カッパ・アーキテクチャに比べてセットアップとメンテナンスが複雑である。2つの独立したデータ処理システムが必要であり、バッチ処理システムとストリーム処理システムが正しく効率的に動作するように継続的なメンテナンスが必要だからだ。
Kappa architecture is generally simpler, as it uses a single data processing system to handle all data processing workloads.
Kappaアーキテクチャは、すべてのデータ処理ワークロードを処理するために単一のデータ処理システムを使用するため、一般的に単純である。
On the other hand, Kappa, requires a mindset switch to think about all data as streams an it requires lots of experience in stream processing and distributed systems.
一方、Kappaは、すべてのデータをストリームとして考えるという発想の転換が必要で、ストリーム処理と分散システムに関する多くの経験を必要とする。

If you’re looking for more insights on building data-intensive applications head over to a classic position from Martin Kleppman, Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems, or check our take on this book with key insights highlighted by our colleague, Piotr Kubowicz in his article - Future According to Designing Data-Intensive Applications.
データ集約型アプリケーションの構築に関するより多くの洞察をお探しなら、マーティン・クレップマンの古典的な立場である「Designing Data-Intensive Applications（データ集約型アプリケーションの設計）」をご覧いただきたい： また、私たちの同僚であるPiotr Kubowiczの記事 - データ集約型アプリケーションの設計による未来 - の中で、重要な洞察が強調されています。

## 1.6. The Importance of Choosing the Right Data Processing Architecture for a Business ビジネスに適したデータ処理アーキテクチャを選択することの重要性

The choice of data processing architecture is a critical one for businesses, as it impacts the scalability, performance, and flexibility of the data processing pipeline.
データ処理アーキテクチャの選択は、データ処理パイプラインのスケーラビリティ、パフォーマンス、柔軟性に影響するため、企業にとって非常に重要です。
It is important for businesses to choose a big data architecture that meets their specific needs and to carefully consider the pros and cons of each option before making a decision.
企業にとって重要なのは、特定のニーズを満たすビッグデータアーキテクチャを選択し、決定を下す前に各オプションの長所と短所を慎重に検討することである。
Generally, if you’re building a system that needs real-time data access, start with Kappa.
一般的に、リアルタイムのデータアクセスが必要なシステムを構築する場合は、Kappaから始める。
And as you learn, you’ll be able to master streams in a way that supports all your workflows.
そして、学ぶにつれて、すべてのワークフローをサポートする方法でストリームをマスターできるようになります。

If you are a business owner or data engineer who wants to develop data systems at scale, nexocode’s data engineering experts can help.
データシステムを大規模に開発したいとお考えのビジネスオーナーやデータエンジニアの皆様、nexocodeのデータエンジニアリングエキスパートがお手伝いします。
Our team has extensive experience in building and optimizing modern data processing pipelines and can help you deploy big data architecture that will benefit your business.
当社のチームは、最新のデータ処理パイプラインの構築と最適化において豊富な経験を有しており、お客様のビジネスに利益をもたらすビッグデータアーキテクチャの導入を支援します。
If you want to know more about streaming data architecture read our article here.
ストリーミング・データ・アーキテクチャについてもっと知りたい方は、こちらの記事をお読みください。
Contact us today to learn more about our services and how we can help you develop a data processing architecture that meets your needs and requirements.
私たちのサービスの詳細と、お客様のニーズと要件を満たすデータ処理アーキテクチャの開発をお手伝いする方法については、今すぐお問い合わせください。
