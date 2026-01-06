## CHAPTER 9: Streaming and Real-Time Features
## 第9章：ストリーミングとリアルタイムフィーチャー
If you want to implement a scalable real-time ML system that has a feature freshness of just a few seconds, you need streaming feature pipelines. 
数秒のフィーチャーの新鮮さを持つスケーラブルなリアルタイムMLシステムを実装したい場合は、ストリーミングフィーチャーパイプラインが必要です。

A streaming feature pipeline is a stream-processing program that runs 24/7, consuming events from a streaming data source, potentially enriching those events from other data sources, applying data transformations to create features, and writing the output feature data to a feature store. 
ストリーミングフィーチャーパイプラインは、24時間365日稼働するストリーム処理プログラムであり、ストリーミングデータソースからイベントを消費し、他のデータソースからそれらのイベントを豊かにし、データ変換を適用してフィーチャーを作成し、出力フィーチャーデータをフィーチャーストアに書き込みます。

Operationally, streaming pipelines have more in common with microservices than batch pipelines. 
運用上、ストリーミングパイプラインはバッチパイプラインよりもマイクロサービスに共通点が多いです。

If a streaming pipeline breaks, it often needs to be fixed immediately. 
ストリーミングパイプラインが壊れた場合、即座に修正する必要があります。

You don’t have until the next scheduled batch run to fix it. 
次のスケジュールされたバッチ実行まで修正する時間はありません。

Stream processing programs divide (partition) the infinite stream of events into groups of related events that are processed together in windows. 
ストリーム処理プログラムは、無限のイベントストリームを関連するイベントのグループに分割（パーティション）し、ウィンドウ内で一緒に処理します。

A window is a time-bound set of events. 
ウィンドウは、時間に制約のあるイベントのセットです。

For example, a streaming pipeline could create a window that groups credit card transactions by credit card number for the last hour and computes features over those events, such as the number of card transactions in the last hour for each card. 
例えば、ストリーミングパイプラインは、過去1時間のクレジットカード取引をクレジットカード番号でグループ化するウィンドウを作成し、各カードの過去1時間の取引数などのフィーチャーを計算することができます。

In such a case, you would need to consider what to do with late-arriving data after its processing window had closed. 
その場合、処理ウィンドウが閉じた後に遅れて到着したデータに対して何をするかを考慮する必要があります。

For example, what should you do with a credit card transaction that arrived two hours late? 
例えば、2時間遅れて到着したクレジットカード取引にはどう対処すべきでしょうか？

Despite these challenges, streaming feature pipelines are increasingly being used to build real-time ML systems. 
これらの課題にもかかわらず、ストリーミングフィーチャーパイプラインはリアルタイムMLシステムを構築するためにますます使用されています。

They are also becoming more accessible to developers, with stream processing frameworks now supporting SQL and Python, as well as traditional languages such as Java. 
また、ストリーム処理フレームワークは、SQLやPython、従来の言語であるJavaをサポートするようになり、開発者にとってもよりアクセスしやすくなっています。

But stream processing is not always required for real-time features. 
しかし、リアルタイムフィーチャーには常にストリーム処理が必要なわけではありません。

Sometimes fresh features that capture information about the most recent events in the world, such as how many times a user clicked a button in the last 30 seconds, can be computed as ODTs in online inference pipelines using the raw event data. 
時には、ユーザーが過去30秒間にボタンを何回クリックしたかなど、世界の最新のイベントに関する情報をキャプチャする新鮮なフィーチャーは、生のイベントデータを使用してオンライン推論パイプラインでODTsとして計算できます。

We will start by looking at how real-time features are crucial to building interactive AI-enabled systems that can react intelligently to both user inputs and environmental changes in real time. 
リアルタイムフィーチャーが、ユーザー入力と環境の変化の両方に対してインテリジェントに反応できるインタラクティブなAI対応システムを構築するために重要であることを見ていきます。

###### Interactive AI-Enabled Systems Need Real-Time Features
###### インタラクティブなAI対応システムにはリアルタイムフィーチャーが必要
An interactive AI-enabled system adapts its behavior in real time based on context, user actions, and environmental changes. 
インタラクティブなAI対応システムは、コンテキスト、ユーザーの行動、および環境の変化に基づいてリアルタイムでその動作を適応させます。

An interactive AI-enabled system can be built on a classical ML model, a deep learning model, or an LLM. 
インタラクティブなAI対応システムは、古典的なMLモデル、深層学習モデル、またはLLMの上に構築できます。

In Chapter 1, we presented TikTok as an example of an interactive AI-enabled system that uses AI to recommend videos based on recent user actions and context. 
第1章では、最近のユーザーの行動とコンテキストに基づいて動画を推薦するAIを使用したインタラクティブなAI対応システムの例としてTikTokを紹介しました。

ByteDance, the makers of TikTok, built extensive real-time data processing infrastructure to ensure that their AI feels responsive and not laggy. 
TikTokの製作者であるByteDanceは、AIが応答性があり、遅延がないと感じるようにするために、広範なリアルタイムデータ処理インフラを構築しました。

TikTok’s recommender adapts to your nonverbal actions (swipes, likes, searches) within a second or so with the help of both classical ML models and deep learning models. 
TikTokのレコメンダーは、古典的なMLモデルと深層学習モデルの両方の助けを借りて、あなたの非言語的な行動（スワイプ、いいね、検索）に1秒以内に適応します。

Interactive applications can also leverage agents and LLM-powered applications (see Chapter 12) to become real-time AI that’s enabled by extending the agent’s API to include IDs as well as the user prompt. 
インタラクティブなアプリケーションは、エージェントやLLM駆動のアプリケーション（第12章参照）を活用して、エージェントのAPIを拡張してIDやユーザープロンプトを含めることでリアルタイムAIになります。

Applications use many IDs to track users, user actions, clickstreams, and application states (orders, articles, transactions, etc.). 
アプリケーションは、多くのIDを使用してユーザー、ユーザーの行動、クリックストリーム、およびアプリケーションの状態（注文、記事、取引など）を追跡します。

When an application issues a query to an agent or LLM application, it can also include application IDs as part of the context of the query. 
アプリケーションがエージェントまたはLLMアプリケーションにクエリを発行する際、アプリケーションIDをクエリのコンテキストの一部として含めることもできます。

For example, if the user asked, “What happened to the shoes I ordered last week?” the agent would receive that query along with the user ID. 
例えば、ユーザーが「先週注文した靴はどうなりましたか？」と尋ねた場合、エージェントはそのクエリをユーザーIDとともに受け取ります。

The user ID could then be used to retrieve from the feature store all events related to the user for the previous week. 
ユーザーIDは、フィーチャーストアから前の週に関連するすべてのイベントを取得するために使用されます。

Those events could then be passed as context to the system prompt, along with the user query, so that the LLM could synthesize the correct answer that the shoes were shipped yesterday. 
これらのイベントは、ユーザーのクエリとともにシステムプロンプトへのコンテキストとして渡され、LLMが「靴は昨日発送されました」という正しい答えを合成できるようにします。

In effect, we can use the online feature store as the retrieval engine for RAG with agents and LLMs (see Figure 9-1). 
実際、オンラインフィーチャーストアをエージェントとLLMを使用したRAGの取得エンジンとして利用できます（図9-1参照）。

_Figure 9-1. If applications that are powered by LLMs are to appear intelligent to humans, they need to respond to both verbal and nonverbal human actions as well as environmental changes in near real time. This can be achieved by real-time data processing of application and environmental data and making this data available to the LLM using an online feature store._
_Figure 9-1. LLMによって駆動されるアプリケーションが人間に知的に見えるためには、言語的および非言語的な人間の行動と環境の変化の両方に近いリアルタイムで応答する必要があります。これは、アプリケーションと環境データのリアルタイムデータ処理を行い、このデータをオンラインフィーチャーストアを使用してLLMに提供することで実現できます。_

This feature store RAG architecture augments the agent with memory of what has happened in the application, and application IDs are the key that agents use to retrieve the correct memory for the current application context. 
このフィーチャーストアRAGアーキテクチャは、エージェントにアプリケーションで何が起こったかの記憶を追加し、アプリケーションIDはエージェントが現在のアプリケーションコンテキストに対して正しい記憶を取得するために使用するキーです。

For this real-time



agentic architecture to work, it requires low-latency stream processing of application events and the online feature store. 
エージェントアーキテクチャが機能するためには、アプリケーションイベントの低遅延ストリーム処理とオンラインフィーチャーストアが必要です。

In a production system, the application would publish events to an event-streaming platform and a stream-processing application would consume them, transform them, and publish them to the online feature store. 
本番システムでは、アプリケーションがイベントをイベントストリーミングプラットフォームに公開し、ストリーム処理アプリケーションがそれらを消費し、変換し、オンラインフィーチャーストアに公開します。

It is also possible to push the raw events to the online feature store and delay the transformation step to ODTs. 
生のイベントをオンラインフィーチャーストアにプッシュし、変換ステップをODTsに遅延させることも可能です。

In the following sections, we will look at the different parts of this architecture, starting with the event-streaming platform. 
次のセクションでは、このアーキテクチャの異なる部分を見ていきますが、まずはイベントストリーミングプラットフォームから始めます。

###### Event-Streaming Platforms
###### イベントストリーミングプラットフォーム

Streaming data sources provide data as a sequence of events, messages, or records. 
ストリーミングデータソースは、データをイベント、メッセージ、またはレコードのシーケンスとして提供します。

We call the real-time data an event stream. 
リアルタイムデータをイベントストリームと呼びます。

Event streams are ingested and processed incrementally by streaming or batch feature pipelines. 
イベントストリームは、ストリーミングまたはバッチフィーチャーパイプラインによって段階的に取り込まれ、処理されます。

Examples of event streams that are useful for building interactive AI-enabled applications are: 
インタラクティブなAI対応アプリケーションを構築するために役立つイベントストリームの例は以下の通りです：

- CDC or polling from an operational database 
- オペレーショナルデータベースからのCDCまたはポーリング
- Activity logs in applications 
- アプリケーションのアクティビティログ
- Sensors used by applications, such as location, cameras, edge/IoT devices, and Supervisory Control and Data Acquisition (SCADA) sensors in manufacturing systems 
- アプリケーションで使用されるセンサー（位置情報、カメラ、エッジ/IoTデバイス、製造システムの監視制御およびデータ取得（SCADA）センサーなど）
- Application context information (failures in services, resource problems, etc.) 
- アプリケーションコンテキスト情報（サービスの障害、リソースの問題など）
- Third-party data (from a subscription to an API that sends notifications of events) 
- サードパーティデータ（イベントの通知を送信するAPIへのサブスクリプションから）

Event streams from these different data sources are centralized in an event-streaming _platform (or event bus) that acts as a hub, where clients can subscribe to receive real-_ time event streams. 
これらの異なるデータソースからのイベントストリームは、クライアントがリアルタイムイベントストリームを受信するためにサブスクライブできるハブとして機能するイベントストリーミングプラットフォーム（またはイベントバス）に集中化されます。

Event-streaming platforms are scalable data platforms that manage real-time event streams, storing events for a limited period of time (a few days or weeks is typical). 
イベントストリーミングプラットフォームは、リアルタイムイベントストリームを管理するスケーラブルなデータプラットフォームであり、イベントを限られた期間（通常は数日または数週間）保存します。

The events are produced from data sources and later consumed by decoupled clients. 
イベントはデータソースから生成され、後にデカップリングされたクライアントによって消費されます。

Examples of widely used event-streaming platforms are: 
広く使用されているイベントストリーミングプラットフォームの例は以下の通りです：

_Apache Kafka_ 
オープンソースのスケーラブルな分散イベントストリーミングプラットフォーム

_Amazon Kinesis_ 
クラウドネイティブなマネージドイベントストリーミングサービス

_Google Cloud Pub/Sub_ 
クラウドネイティブなイベントストリーミングサービス

Event-streaming platforms are a primary data source for streaming feature pipelines. 
イベントストリーミングプラットフォームは、ストリーミングフィーチャーパイプラインの主要なデータソースです。

Typically, the events contain time-series data, with events containing a timestamp added at the data source. 
通常、イベントには時系列データが含まれており、データソースで追加されたタイムスタンプを含むイベントがあります。

Streaming feature pipelines use event time, not ingestion time, to aggregate events and create features. 
ストリーミングフィーチャーパイプラインは、イベントを集約し、フィーチャーを作成するために、取り込み時間ではなくイベント時間を使用します。

Stream processing programs include a _sink, which is a place where the results of data processing are stored. 
ストリーム処理プログラムには、データ処理の結果が保存される場所であるシンクが含まれます。

Examples of sinks include the event-streaming platforms themselves (building data processing DAGs), lakehouses (event streaming), and feature stores for real-time ML systems. 
シンクの例には、イベントストリーミングプラットフォーム自体（データ処理DAGの構築）、レイクハウス（イベントストリーミング）、およびリアルタイムMLシステムのフィーチャーストアが含まれます。

The next section covers the different architectures for computing real-time features. 
次のセクションでは、リアルタイムフィーチャーを計算するための異なるアーキテクチャについて説明します。

If you just want to get straight to programming streaming feature pipelines, you can safely skip to “Writing Streaming Feature Pipelines” on page 242. 
ストリーミングフィーチャーパイプラインのプログラミングにすぐに取り掛かりたい場合は、242ページの「ストリーミングフィーチャーパイプラインの作成」に安全にスキップできます。

###### Shift Left or Shift Right?
###### シフト左またはシフト右？

Streaming feature pipelines precompute features to provide history and context for online models. 
ストリーミングフィーチャーパイプラインは、オンラインモデルのために履歴とコンテキストを提供するためにフィーチャーを事前計算します。

However, it is also possible to compute real-time features on demand in response to prediction requests from AI-enabled applications or services. 
しかし、AI対応アプリケーションやサービスからの予測リクエストに応じて、リアルタイムフィーチャーをオンデマンドで計算することも可能です。

As an architect, you will have to choose whether you want to shift left feature computation to a feature pipeline or shift right feature computation to compute features at request time. 
アーキテクトとして、フィーチャー計算をフィーチャーパイプラインにシフト左させるか、リクエスト時にフィーチャーを計算するためにシフト右させるかを選択する必要があります。

The term shifting left comes from the practice of moving a phase of the software development process to the left on a timeline when you consider the traditional software development lifecycle, while shifting right moves the phase closer to operations. 
シフト左という用語は、従来のソフトウェア開発ライフサイクルを考慮したときに、ソフトウェア開発プロセスのフェーズをタイムライン上で左に移動させる慣行から来ており、シフト右はフェーズを運用に近づけます。

In terms of feature engineering, shifting left means precomputing features and making them available for retrieval via the feature store. 
フィーチャーエンジニアリングの観点から、シフト左はフィーチャーを事前計算し、フィーチャーストアを介して取得可能にすることを意味します。

Shifting right means computing features in ODTs or MDTs. 
シフト右はODTsまたはMDTsでフィーチャーを計算することを意味します。

Shifting left helps reduce the latency of prediction requests, as retrieving precomputed features from the feature store is often faster than computing the features on demand. 
シフト左は、フィーチャーストアから事前計算されたフィーチャーを取得する方が、オンデマンドでフィーチャーを計算するよりも速いため、予測リクエストのレイテンシを減少させるのに役立ちます。

Shifting right can remove the need for feature pipelines (reducing system complexity) if all fresh features can be computed on demand. 
シフト右は、すべての新鮮なフィーチャーがオンデマンドで計算できる場合、フィーチャーパイプラインの必要性を排除することができ（システムの複雑さを減少させ）、ます。

Figure 9-2 shows how shift-left feature computation is performed in feature pipelines, while shift-right feature computation is performed in online inference pipelines using ODTs or MDTs. 
図9-2は、フィーチャーパイプラインでシフト左フィーチャー計算がどのように行われるかを示しており、シフト右フィーチャー計算はODTsまたはMDTsを使用したオンライン推論パイプラインで行われます。

_Figure 9-2. Shifting left involves precomputing features in feature pipelines, while shifting_ _right involves computing features on demand in response to prediction requests._ 
_図9-2. シフト左はフィーチャーパイプラインでフィーチャーを事前計算することを含み、シフト右は予測リクエストに応じてフィーチャーをオンデマンドで計算することを含みます。_

Typically, application requirements help decide whether to precompute features or create features on demand. 
通常、アプリケーションの要件がフィーチャーを事前計算するか、オンデマンドで作成するかを決定するのに役立ちます。

Reasons to shift left feature computation include: 
フィーチャー計算をシフト左させる理由には以下が含まれます：

- The application requires very low-latency predictions (for example, it has a P99 10 ms latency requirement, where 99% of predictions are received in less than 10 ms). 
- アプリケーションは非常に低遅延の予測を必要とします（例えば、P99 10 msのレイテンシ要件があり、99%の予測が10 ms未満で受信されます）。

- The overall computational burden is reduced by precomputing features in a performant streaming engine compared with ODTs or MDTs. 
- ODTsやMDTsと比較して、パフォーマンスの良いストリーミングエンジンでフィーチャーを事前計算することにより、全体的な計算負担が軽減されます。

Reasons to shift right feature computation include: 
フィーチャー計算をシフト右させる理由には以下が含まれます：

- Latency-insensitive prediction requests, so features can be computed on demand to avoid wasting CPU cycles to precompute features that are not used 
- レイテンシに敏感でない予測リクエストがあるため、使用されないフィーチャーを事前計算するためにCPUサイクルを無駄にしないように、フィーチャーをオンデマンドで計算できます。

- Avoiding the infrastructural burden of running a streaming feature pipeline 
- ストリーミングフィーチャーパイプラインを実行するためのインフラストラクチャの負担を回避します。

Table 9-1 shows some real-time ML use cases that favor precomputed features and other use cases that favor computing features on demand. 
表9-1は、事前計算されたフィーチャーを好むリアルタイムMLのユースケースと、オンデマンドでフィーチャーを計算することを好む他のユースケースを示しています。

_Table 9-1. Use cases that tend to favor either shift left or shift right for feature computation_ 
_表9-1. フィーチャー計算においてシフト左またはシフト右を好む傾向のあるユースケース_

**Use case** **Precompute features or compute on demand?** 
**ユースケース** **フィーチャーを事前計算するか、オンデマンドで計算するか？**

Fraud _Shift left. This requires real-time decisions with low latency. Precomputing features ensures that the_ inference pipeline can quickly retrieve these features, minimizing the need for costly, real-time computation. 
詐欺 _シフト左。これは低遅延でリアルタイムの意思決定を必要とします。フィーチャーを事前計算することで、推論パイプラインはこれらのフィーチャーを迅速に取得でき、コストのかかるリアルタイム計算の必要性を最小限に抑えます。

Personalized recommendations _Shift left. Recommendations need to be served with low latency. Precomputing user preferences,_ product similarity scores, and historical behavior allows the system to respond quickly without complex, real-time computation. However, lightweight real-time updates (e.g., incorporating recent clicks or views) may complement this. 
パーソナライズされた推奨 _シフト左。推奨は低遅延で提供される必要があります。ユーザーの好み、製品の類似スコア、過去の行動を事前計算することで、システムは複雑なリアルタイム計算なしで迅速に応答できます。ただし、軽量なリアルタイム更新（例：最近のクリックやビューを組み込むこと）はこれを補完する可能性があります。

Dynamic pricing _Shift right. Pricing often depends on rapidly changing factors like supply, demand, competitor pricing,_ and external events. These variables may need to be retrieved using third-party APIs at runtime, requiring ODTs. 
動的価格設定 _シフト右。価格はしばしば供給、需要、競合他社の価格、外部イベントなどの急速に変化する要因に依存します。これらの変数は、ランタイムでサードパーティAPIを使用して取得する必要があり、ODTsを必要とします。

Chatbots with browser-session context _Shift right. The chatbot must consider dynamic, session-specific context (e.g., a user’s most recent_ query, the ongoing conversation context) in its predictions. This makes precomputing less effective since the system primarily relies on immediate conversational context for feature computation. 
ブラウザセッションコンテキストを持つチャットボット _シフト右。チャットボットは、予測において動的でセッション固有のコンテキスト（例：ユーザーの最近のクエリ、進行中の会話コンテキスト）を考慮する必要があります。これにより、システムはフィーチャー計算のために即時の会話コンテキストに主に依存するため、事前計算が効果的でなくなります。

Predictive maintenance _Shift left. Maintenance predictions are typically based on historical telemetry data, precomputed_ failure likelihoods, and trends. A shift-left approach enables efficient analysis of device health and reduces the computational burden during predictions by precomputing features like moving averages and anomaly scores. 
予測保守 _シフト左。保守予測は通常、過去のテレメトリデータ、事前計算された故障の可能性、およびトレンドに基づいています。シフト左アプローチは、デバイスの健康状態の効率的な分析を可能にし、移動平均や異常スコアなどのフィーチャーを事前計算することで、予測中の計算負担を軽減します。

PII removal _Shift left and right. According to the data minimization principle, you should remove PII as early as_ possible in the pipeline to reduce the risk of exposing sensitive information throughout the data processing lifecycle. You still may have to check for PII at request time, necessitating ODTs. 
PIIの削除 _シフト左および右。データ最小化の原則に従い、データ処理ライフサイクル全体で機密情報が露出するリスクを減らすために、パイプライン内でできるだけ早くPIIを削除する必要があります。リクエスト時にPIIを確認する必要がある場合もあり、ODTsを必要とします。

As always in computing, choices imply trade-offs. 
コンピューティングにおいては常に、選択にはトレードオフが伴います。

Shifting left may incur too much operational overhead and require new skills with stream processing, while shifting right could add too much latency and cost to your predictions. 
シフト左は過剰な運用オーバーヘッドを引き起こし、ストリーム処理に新しいスキルを必要とする可能性がありますが、シフト右は予測に過剰なレイテンシとコストを追加する可能性があります。

In addition, some types of ODTs, such as aggregations, may require specific support from your online feature store to be computed efficiently. 
さらに、集約などの一部のODTのタイプは、効率的に計算されるためにオンラインフィーチャーストアからの特定のサポートを必要とする場合があります。

###### Shift-Right Architectures
###### シフト右アーキテクチャ

Figure 9-3 shows an on-demand feature computation architecture, in which there is no streaming feature pipeline and real-time features are computed by ODTs that push down aggregation computations to the online feature store. 
図9-3は、ストリーミングフィーチャーパイプラインがなく、リアルタイムフィーチャーがODTsによって計算され、集約計算がオンラインフィーチャーストアにプッシュダウンされるオンデマンドフィーチャー計算アーキテクチャを示しています。

_Figure 9-3. Shift-right architectures can use fresh features by applications writing their_ _events directly to the feature store._ 
_図9-3. シフト右アーキテクチャは、アプリケーションが自らのイベントを直接フィーチャーストアに書き込むことによって新鮮なフィーチャーを使用できます。_

In this architecture, the AI-enabled application or service streams raw events created by it directly to the feature store (via a Kafka or a REST API). 
このアーキテクチャでは、AI対応アプリケーションまたはサービスが自ら生成した生のイベントを直接フィーチャーストアにストリーミングします（KafkaまたはREST APIを介して）。

The events get stored as rows in online feature groups and asynchronously materialized to the offline feature store (lakehouse tables). 
イベントはオンラインフィーチャーグループの行として保存され、非同期的にオフラインフィーチャーストア（レイクハウステーブル）に具現化されます。

The types of different data transformations that can be performed in ODT functions include: 
ODT関数で実行できるさまざまなデータ変換のタイプには以下が含まれます：

_Stateless transformations_ Computed using only request parameters 
_ステートレス変換_ リクエストパラメータのみを使用して計算されます

_Stateful transformations_ Computed using a combination of request parameters and precomputed features read from the feature store 
_ステートフル変換_ リクエストパラメータとフィーチャーストアから読み取った事前計算されたフィーチャーの組み合わせを使用して計算されます

_Stateful transformations with raw events_ Where you read records from the online feature store as a DataFrame and then perform transformations on the DataFrame 
_生のイベントを使用したステートフル変換_ オンラインフィーチャーストアからレコードをDataFrameとして読み取り、その後DataFrameに対して変換を実行します

_Stateful transformations with SQL_ Where transformations are executed in the online feature store directly as SQL expressions, returning transformed data as a DataFrame; for example, pushdown aggregations, as shown in Figure 9-3 
_SQLを使用したステートフル変換_ 変換がオンラインフィーチャーストアで直接SQL式として実行され、変換されたデータがDataFrameとして返されます。例えば、図9-3に示すようにプッシュダウン集約があります。



ODTs that can execute stateless transformations and precomputed transformations were introduced in Chapter 7 as Python UDFs and Pandas UDFs. 
ステートレス変換と事前計算された変換を実行できるODTは、第7章でPython UDFおよびPandas UDFとして紹介されました。

Stateful transformations with raw events are more compute intensive and may place high load on the online inference pipeline, network, and feature store. 
生のイベントを用いたステートフル変換は、計算集約的であり、オンライン推論パイプライン、ネットワーク、およびフィーチャーストアに高い負荷をかける可能性があります。

Figure 9-4 shows a shift-right architecture in which aggregations can be either performed with DataFrames in an ODT on the raw records or pushed down to the online feature store that executes them as SQL. 
図9-4は、集約がODT内のDataFrameを使用して生のレコードで実行されるか、SQLとして実行するオンラインフィーチャーストアにプッシュダウンされるシフトライトアーキテクチャを示しています。

_Figure 9-4. Shift-right architecture that filters and transforms events in a streaming feature pipeline before they are written to the online feature store. ODTs compute aggregations from the events either locally with DataFrames or using a pushdown aggregation SQL command._  
_図9-4. オンラインフィーチャーストアに書き込まれる前に、ストリーミングフィーチャーパイプラインでイベントをフィルタリングおよび変換するシフトライトアーキテクチャ。ODTsは、イベントから集約をローカルでDataFramesを使用して計算するか、プッシュダウン集約SQLコマンドを使用します。_

In general, the ODT reading the raw records and processing them with DataFrames will have much higher latency and computation overhead than if the aggregations were pushed down to the online feature store and executed as SQL. 
一般的に、生のレコードを読み取り、DataFramesで処理するODTは、集約がオンラインフィーチャーストアにプッシュダウンされてSQLとして実行される場合よりも、はるかに高いレイテンシと計算オーバーヘッドを持ちます。

We have already looked at how ODTs prevent offline-online skew, but how do ondemand SQL transformations prevent skew when the same SQL should be executed in a feature pipeline on historical data? 
私たちはすでにODTがオフラインとオンラインのスキューを防ぐ方法を見てきましたが、同じSQLが履歴データのフィーチャーパイプラインで実行されるべきとき、オンデマンドSQL変換はどのようにスキューを防ぐのでしょうか？

They can do this if the system provides language-level API calls that create the SQL that is ultimately executed. 
システムが最終的に実行されるSQLを生成する言語レベルのAPI呼び出しを提供する場合、これを実現できます。

For example, in Hopsworks, a Postgres-compliant SQL dialect is supported in both RonSQL (SQL run against RonDB REST server) and Spark SQL/DuckDB. 
例えば、Hopsworksでは、Postgres準拠のSQL方言がRonSQL（RonDB RESTサーバーに対して実行されるSQL）とSpark SQL/DuckDBの両方でサポートされています。

One caveat for on-demand SQL is that the online feature store must support a SQL API. 
オンデマンドSQLの一つの注意点は、オンラインフィーチャーストアがSQL APIをサポートしている必要があることです。

For example, not all online feature stores support pushdown aggregations, as many online feature stores are key-value stores without support for SQL. 
例えば、すべてのオンラインフィーチャーストアがプッシュダウン集約をサポートしているわけではなく、多くのオンラインフィーチャーストアはSQLをサポートしていないキー-バリューストアです。

An additional requirement for your online feature store is that it should support a TTL for rows. 
オンラインフィーチャーストアに対する追加の要件は、行に対するTTLをサポートする必要があることです。

The TTL can be specified at either the table level or the row level. 
TTLは、テーブルレベルまたは行レベルのいずれかで指定できます。

The reason a TTL is required is that online feature groups typically only store the latest feature values for entities. 
TTLが必要な理由は、オンラインフィーチャーグループが通常、エンティティの最新のフィーチャー値のみを保存するためです。

But when you want to perform online aggregations, the raw historical event data should be stored there (including features with older `event_times). 
しかし、オンライン集約を実行したい場合、古い`event_times`を含む生の履歴イベントデータはそこに保存されるべきです。

If your feature pipeline now writes raw data to the online feature store (instead of updating feature values for entities), your online feature data could keep growing, and eventually your online store could run out of free storage space. 
もしあなたのフィーチャーパイプラインが現在、エンティティのフィーチャー値を更新するのではなく、生データをオンラインフィーチャーストアに書き込む場合、オンラインフィーチャーデータは増え続け、最終的にオンラインストアが空きストレージスペースを使い果たす可能性があります。

The easiest way to limit the growth in online storage is to specify that rows in an online feature group have a TTL. 
オンラインストレージの成長を制限する最も簡単な方法は、オンラインフィーチャーグループの行にTTLがあることを指定することです。

That way, rows are “garbage collected” after the TTL, continually freeing up storage space. 
そのようにして、行はTTLの後に「ガーベジコレクト」され、ストレージスペースが継続的に解放されます。

The TTL for a row expires when: 
行のTTLは次の条件で期限切れになります：

_current_time > (event_time + TTL)_ 
_current_time > (event_time + TTL)_

where TTL is defined on either a per-row or a per-table basis. 
ここで、TTLは行ごとまたはテーブルごとに定義されます。

Per-table TTL means that all rows in the table are given the same TTL when created. 
テーブルごとのTTLは、テーブル内のすべての行が作成時に同じTTLを与えられることを意味します。

Hopsworks supports both per-table and per-row TTLs (via its online store, RonDB). 
Hopsworksは、テーブルごとのTTLと行ごとのTTLの両方をサポートしています（オンラインストアRonDBを介して）。

After a row has been created (or updated), current time advances, and eventually the TTL for the row expires, whereupon it is scheduled for automatic removal. 
行が作成（または更新）された後、現在の時間が進み、最終的にその行のTTLが期限切れになり、自動削除のためにスケジュールされます。

One problem that can arise here, however, is that writes and deletions can get out of sync due to delays or failures in feature pipelines. 
しかし、ここで発生する可能性のある一つの問題は、書き込みと削除がフィーチャーパイプラインの遅延や失敗により同期が取れなくなることです。

As deletions always happen at the TTL interval, delays in writes can mean data becomes unavailable for some entities. 
削除は常にTTLの間隔で行われるため、書き込みの遅延は、一部のエンティティに対してデータが利用できなくなることを意味します。

[Uber described this problem in a talk at the Feature Store Summit 2024. In the case of a](https://oreil.ly/NMVsk) delayed write, you should also delay deletes. 
[Uberは、2024年のFeature Store Summitでこの問題について説明しました。遅延書き込みの場合、削除も遅延させるべきです。]

While Uber could not do this due to a lack of support for retroactively updating the TTL of already-written rows in Cassandra, Hopsworks’ database, RonDB, provides a purge window where expired rows are only deleted after the purge window has passed. 
Uberは、Cassandraで既に書き込まれた行のTTLを遡って更新するサポートがないため、これを行うことができませんでしたが、HopsworksのデータベースRonDBは、期限切れの行がパージウィンドウが経過した後にのみ削除されるパージウィンドウを提供します。

You can enable reading rows whose TTL has expired, but before the purge window has passed. 
TTLが期限切れになった行の読み取りを有効にできますが、パージウィンドウが経過する前に行います。

You can also temporarily extend the purge window if the delays are significant. 
遅延が大きい場合は、一時的にパージウィンドウを延長することもできます。

###### Shift-Left Architectures
Now we move on to the topic of the rest of this chapter—precomputing feature data in streaming feature pipelines. 
###### シフトレフトアーキテクチャ
さて、私たちはこの章の残りのトピック、ストリーミングフィーチャーパイプラインにおけるフィーチャーデータの事前計算に移ります。

We start by introducing the original (and now legacy) hybrid approach to building streaming feature pipelines as two separate pipelines: online feature engineering in a stream processing layer and offline feature creation in a batch pipeline. 
まず、ストリーミングフィーチャーパイプラインを構築するための元の（そして現在はレガシーの）ハイブリッドアプローチを、ストリーム処理層でのオンラインフィーチャーエンジニアリングとバッチパイプラインでのオフラインフィーチャー作成という2つの別々のパイプラインとして紹介します。

Then, we move on to the modern streaming-native architecture, where the same stream processing program is used for both online and offline feature engineering. 
次に、オンラインとオフラインのフィーチャーエンジニアリングの両方に同じストリーム処理プログラムが使用される現代のストリーミングネイティブアーキテクチャに移ります。

###### Hybrid streaming-batch architecture
The _hybrid streaming-batch architecture is a design in which you have two separate_ processing layers: a stream-processing pipeline for real-time feature engineering and a batch-processing pipeline for historical feature data creation (backfilling). 
###### ハイブリッドストリーミングバッチアーキテクチャ
_ハイブリッドストリーミングバッチアーキテクチャは、リアルタイムフィーチャーエンジニアリングのためのストリーム処理パイプラインと、履歴フィーチャーデータ作成（バックフィリング）のためのバッチ処理パイプラインという2つの別々の処理層を持つ設計です。_

Klarna presented its version of this architecture at AWS re:Invent 2024 (see Figure 9-5). 
Klarnaは、AWS re:Invent 2024でこのアーキテクチャのバージョンを発表しました（図9-5を参照）。

_Figure 9-5. A hybrid streaming-batch architecture is one where you backfill with batch feature pipelines, but real-time data processing is a streaming feature pipeline. © Tony_ _[Liu and Dragan Coric: “AWS re:Invent 2024—Klarna: Accelerating credit decisioning](https://oreil.ly/zL0Mk)_ _[with real-time data processing”.](https://oreil.ly/zL0Mk)_  
_図9-5. ハイブリッドストリーミングバッチアーキテクチャは、バッチフィーチャーパイプラインでバックフィルを行いますが、リアルタイムデータ処理はストリーミングフィーチャーパイプラインです。© Tony_ _[LiuとDragan Coric: “AWS re:Invent 2024—Klarna: リアルタイムデータ処理による信用決定の加速](https://oreil.ly/zL0Mk)。”_

In this system, Klarna prevents offline-online skew by writing the transformation logic once in a shared library that is used in both batch pipelines and streamprocessing pipelines. 
このシステムでは、Klarnaは、バッチパイプラインとストリーム処理パイプラインの両方で使用される共有ライブラリに変換ロジックを一度書くことで、オフラインとオンラインのスキューを防ぎます。

Given that both streaming and batch programs need to be written in languages that can use the same shared feature computation libraries, they use a custom stream-processing framework. 
ストリーミングプログラムとバッチプログラムの両方が、同じ共有フィーチャー計算ライブラリを使用できる言語で書かれる必要があるため、彼らはカスタムストリーム処理フレームワークを使用します。

In general, you should avoid this architecture as it requires custom infrastructure and complex logic in libraries to enable them to be correctly run by both streaming and batch pipelines. 
一般的に、このアーキテクチャはカスタムインフラストラクチャとライブラリ内の複雑なロジックを必要とするため、避けるべきです。

Instead, we will favor a _streaming-native architecture, in which a single stream-processing pipeline can process both real-time data and backfill feature data for training. 
代わりに、リアルタイムデータとトレーニング用のバックフィルフィーチャーデータの両方を処理できる単一のストリーム処理パイプラインを持つ_ストリーミングネイティブアーキテクチャ_を支持します。

In the stream-processing community, the hybrid streaming-batch architecture is called a _Lambda architecture, while a streaming-native architecture is called a Kappa architecture. 
ストリーム処理コミュニティでは、ハイブリッドストリーミングバッチアーキテクチャは_ラムダアーキテクチャ_と呼ばれ、ストリーミングネイティブアーキテクチャは_カッパアーキテクチャ_と呼ばれます。

Knowing this terminology may help you communicate with a data engineer, but the terms _hybrid streaming-batch architecture and_ _streaming-native_ _architecture are easier to explain. 
この用語を知っておくことでデータエンジニアとのコミュニケーションが助けられるかもしれませんが、_ハイブリッドストリーミングバッチアーキテクチャ_と_ストリーミングネイティブアーキテクチャ_という用語の方が説明しやすいです。

###### Streaming-native architecture
The streaming-native architecture uses the streaming feature pipeline to process both real-time event streams and historical data (see Figure 9-6). 
###### ストリーミングネイティブアーキテクチャ
ストリーミングネイティブアーキテクチャは、ストリーミングフィーチャーパイプラインを使用してリアルタイムイベントストリームと履歴データの両方を処理します（図9-6を参照）。

_Figure 9-6. A streaming-native architecture has a streaming feature pipeline that runs in either real-time mode (processing event streams from an event-streaming platform) or backfill mode (processing historical events from a batch data source, such as a lakehouse table). The feature pipeline outputs its feature data to a feature store. Stream-processing engines manage state in a local state store and support failure recovery through checkpointing to a remote store._  
_図9-6. ストリーミングネイティブアーキテクチャは、リアルタイムモード（イベントストリーミングプラットフォームからのイベントストリームを処理）またはバックフィルモード（湖ハウステーブルなどのバッチデータソースからの履歴イベントを処理）で実行されるストリーミングフィーチャーパイプラインを持っています。フィーチャーパイプラインは、そのフィーチャーデータをフィーチャーストアに出力します。ストリーム処理エンジンは、ローカルステートストアで状態を管理し、リモートストアへのチェックポイントを通じて障害回復をサポートします。_

To remove the need for a batch layer that processes historical data, the streaming feature pipeline needs to be able to be run against both streaming and batch data sources and in different modes of operation, depending on whether it processes real-time data or historical data. 
履歴データを処理するバッチレイヤーの必要性を取り除くために、ストリーミングフィーチャーパイプラインは、リアルタイムデータを処理するか履歴データを処理するかに応じて、ストリーミングデータソースとバッチデータソースの両方に対して実行でき、異なる動作モードで実行できる必要があります。

The most common operational modes for a streaming feature pipeline are: 
ストリーミングフィーチャーパイプラインの最も一般的な運用モードは次のとおりです：

_Real-time mode_ The streaming pipeline processes live event streams continuously, sourcing data from an event-streaming platform or other streaming data source. 
_リアルタイムモード_ ストリーミングパイプラインは、イベントストリーミングプラットフォームや他のストリーミングデータソースからデータを取得し、ライブイベントストリームを継続的に処理します。

The streaming engine runs 24/7 and should be highly available, automatically recovering from partial or complete failures. 
ストリーミングエンジンは24時間365日稼働し、高い可用性を持ち、部分的または完全な障害から自動的に回復する必要があります。

_Stream replay_ This mode replays historical events through the streaming pipeline, simulating real-time processing. 
_ストリームリプレイ_ このモードは、ストリーミングパイプラインを通じて履歴イベントをリプレイし、リアルタイム処理をシミュレートします。

The replayed data can originate from a streaming data source (such as the event-streaming platform) or batch data source, and it is processed in the same order and timing as the original stream. 
リプレイされたデータは、ストリーミングデータソース（イベントストリーミングプラットフォームなど）またはバッチデータソースから発生する可能性があり、元のストリームと同じ順序とタイミングで処理されます。

The pipeline exits once the replay is complete. 
パイプラインはリプレイが完了すると終了します。



_Backfilling_ 
このモードは、データのギャップに対処するか、通常はS3互換のオブジェクトストア上のレイクハウステーブルからバッチデータを処理します。 
This mode addresses gaps in data or processes historical data from a batch data source, typically a lakehouse table on an S3-compatible object store. 

After completing the backfilling process, the streaming pipeline exits. 
バックフィリングプロセスが完了すると、ストリーミングパイプラインは終了します。

_Stream reprocessing_ 
このモードでは、ストリームを再実行することによって、すでに処理されたデータに更新されたロジックが適用されます。 
_Stream reprocessing_ In this mode, updated logic is applied to already processed data by re-executing the stream. 

The data source is often the original event-streaming platform but could also be the event-sourced data in a batch data source. 
データソースは、元のイベントストリーミングプラットフォームであることが多いですが、バッチデータソース内のイベントソースデータである可能性もあります。 

Stream reprocessing is often done to create new versions of feature groups (with different implementations of features). 
ストリームの再処理は、しばしば異なる機能の実装を持つフィーチャーグループの新しいバージョンを作成するために行われます。 

The streaming pipeline may either continue running 24/7 or exit if the reprocessing is a onetime task. 
ストリーミングパイプラインは、24時間365日稼働し続けるか、再処理が一度限りのタスクであれば終了します。 

Many organizations store a full copy of the event stream in a process called _event_ _sourcing. 
多くの組織は、_event sourcing_と呼ばれるプロセスでイベントストリームの完全なコピーを保存します。 

This involves copying the event stream to cheaper long-term storage in an object store. 
これは、イベントストリームをオブジェクトストアの安価な長期ストレージにコピーすることを含みます。 

Event sourcing is often needed as event-streaming platforms are not long-term data stores. 
イベントソーシングは、イベントストリーミングプラットフォームが長期データストアではないため、しばしば必要とされます。 

They retain data for a relatively short period of time. 
これらは、比較的短期間データを保持します。 

For example, Apache Kafka stores data for only seven days by default. 
例えば、Apache Kafkaはデフォルトでデータをわずか7日間しか保存しません。 

But with event sourcing, a lakehouse table on an S3-compatible object store can be used as a data source for a streaming feature pipeline to replay, backfill, or reprocess a historical event stream. 
しかし、イベントソーシングを使用することで、S3互換のオブジェクトストア上のレイクハウステーブルを、ストリーミングフィーチャーパイプラインのデータソースとして使用し、過去のイベントストリームを再生、バックフィル、または再処理することができます。 

Without event sourcing, you will often lose the ability to replay, backfill, or reprocess historical event streams when the data has been purged from the eventstreaming platform. 
イベントソーシングがないと、データがイベントストリーミングプラットフォームから削除されたときに、過去のイベントストリームを再生、バックフィル、または再処理する能力を失うことがよくあります。 

The main difference between streaming programs and batch programs is that streaming programs can perform both stateless and stateful data transformations. 
ストリーミングプログラムとバッチプログラムの主な違いは、ストリーミングプログラムが無状態および有状態のデータ変換の両方を実行できることです。 

Batch programs perform only stateless data transformations. 
バッチプログラムは無状態のデータ変換のみを実行します。 

In our credit card fraud system, we use stateful data transformations to create stateful features. 
私たちのクレジットカード詐欺システムでは、有状態のデータ変換を使用して有状態の特徴を作成します。 

For example, aggregation features such as counts and sums of credit card transactions over different periods of time require historical data to be computed. 
例えば、異なる期間にわたるクレジットカード取引のカウントや合計などの集約機能は、計算のために過去のデータを必要とします。 

Stateful data transformation is one of the reasons why some developers consider stream processing to be a challenging development environment. 
有状態のデータ変換は、いくつかの開発者がストリーム処理を挑戦的な開発環境と見なす理由の一つです。 

Another source of complexity for developers is the set of data processing guarantees provided by event sources and streaming engines: 
開発者にとってのもう一つの複雑さの源は、イベントソースとストリーミングエンジンによって提供されるデータ処理の保証のセットです：

_Exactly-once_ 
各イベントは一度だけ処理され、重複や欠落がないことを保証します。 
_Exactly-once_ Each event is processed once and only once, ensuring no duplicates or misses. 

_At-least-once_ 
イベントは1回以上処理され、データ損失はないが、重複イベントを許可します。 
_At-least-once_ Events are processed one or more times, ensuring no data loss but allowing duplicate events. 

_At-most-once_ 
イベントは1回だけ処理されるか、まったく処理されないかで、低遅延を優先しますが、データ損失のリスクがあります。 
_At-most-once_ Events are processed once or not at all, prioritizing low latency but risking data loss. 

Although some stream-processing engines support exactly-once semantics, by default they mostly provide at-least-once semantics. 
いくつかのストリーム処理エンジンはexactly-onceセマンティクスをサポートしていますが、デフォルトでは主にat-least-onceセマンティクスを提供します。 

The challenge with at-least-once semantics is that, through no fault of your own, your feature pipeline could introduce duplicate data. 
at-least-onceセマンティクスの課題は、あなたの過失ではなく、フィーチャーパイプラインが重複データを導入する可能性があることです。 

Luckily, however, we will not have to concern ourselves with duplicate data, as we will use the Hopsworks feature store as a sink. 
しかし幸運なことに、私たちはHopsworksフィーチャーストアをシンクとして使用するため、重複データについて心配する必要はありません。 

It upgrades at-least-once data processing into exactly-once by: 
これは、at-least-onceデータ処理をexactly-onceにアップグレードします：

- Turning duplicate events into idempotent updates for the online store (RonDB) 
- オンラインストア（RonDB）用の冪等更新に重複イベントを変換します。 

- Removing duplicate events for the offline store (Apache Hudi) 
- オフラインストア（Apache Hudi）用の重複イベントを削除します。 

This means you do not have to write extra code to deduplicate data in your streaming pipelines with Hopsworks. 
これは、Hopsworksを使用してストリーミングパイプライン内のデータを重複排除するために追加のコードを書く必要がないことを意味します。 

If you are using a feature store that does not provide exactly-once processing guarantees, you will need to manually deduplicate data or handle duplicate data in your training and inference pipelines. 
exactly-once処理の保証を提供しないフィーチャーストアを使用している場合は、手動でデータを重複排除するか、トレーニングおよび推論パイプラインで重複データを処理する必要があります。 

###### Backpressure 
ストリーミングフィーチャーパイプラインによって生成される負荷は、日中や季節によって異なることがよくあります。 
###### Backpressure 
The load created by streaming feature pipelines often varies throughout the day or season. 

You should provision your stream-processing system so that it can handle the expected write load. 
予想される書き込み負荷を処理できるように、ストリーム処理システムをプロビジョニングする必要があります。 

Many stream-processing frameworks can handle unexpected peaks in event traffic through backpressure. 
多くのストリーム処理フレームワークは、バックプレッシャーを通じてイベントトラフィックの予期しないピークを処理できます。 

Backpressure is a flow control mechanism in stream processing that matches the rate of data production at the source with the rate of data consumption at the sink. 
バックプレッシャーは、ストリーム処理におけるフロー制御メカニズムで、ソースでのデータ生成率とシンクでのデータ消費率を一致させます。 

For example, when a streaming-feature pipeline in Apache Flink detects that it is processing data slower than it is receiving it, it signals upstream components to slow down or temporarily pause data flow. 
例えば、Apache Flinkのストリーミングフィーチャーパイプラインが、受信するよりもデータを処理する速度が遅いことを検出した場合、上流のコンポーネントにデータフローを遅くするか、一時的に停止するように信号を送ります。 

Apache Kafka, in turn, can throttle producers, allowing the system to handle load gracefully without dropping data. 
一方、Apache Kafkaはプロデューサーを制限できるため、システムはデータを失うことなく負荷を優雅に処理できます。 

###### Writing Streaming Feature Pipelines 
第6章では、バッチフィーチャーパイプラインがデータフロー_グラフとして構成されている方法を紹介しました。 
###### Writing Streaming Feature Pipelines 
In Chapter 6, we introduced how batch feature pipelines are structured as a dataflow _graph, with data sources as inputs, DataFrames as nodes, feature functions as edges,_ and feature groups as sinks. 

What we call the DAG of feature functions is, in fact, a dataflow program. 
私たちがフィーチャー関数のDAGと呼ぶものは、実際にはデータフロープログラムです。 

A _dataflow program models computation as a directed graph,_ where data flows between operations, enabling parallel and incremental processing. 
_データフロープログラムは、計算を有向グラフとしてモデル化し、データが操作間で流れることで、並列かつ増分処理を可能にします。 

Similarly, a streaming-feature pipeline is a dataflow program that starts with one or more event streams as input. 
同様に、ストリーミングフィーチャーパイプラインは、1つ以上のイベントストリームを入力として開始するデータフロープログラムです。 

The nodes are operators (that perform the data transformations), the edges represent data dependencies, and the feature groups are the sinks. 
ノードはデータ変換を実行するオペレーターであり、エッジはデータ依存関係を表し、フィーチャーグループはシンクです。 

While batch ETL programs work with DataFrames, stream-processing programs work with datastreams. 
バッチETLプログラムはDataFramesで動作するのに対し、ストリーム処理プログラムはデータストリームで動作します。 

A datastream represents a continuous, unbounded sequence of data records (an event stream) that are generated over time. 
データストリームは、時間の経過とともに生成される連続的で無限のデータレコードのシーケンス（イベントストリーム）を表します。 

A comparison of datastreams and DataFrames is shown in Table 9-2. 
データストリームとDataFramesの比較は、表9-2に示されています。 

_Table 9-2. Comparison of datastreams and DataFrames_ 
表9-2. データストリームとDataFramesの比較 

**Datastream** **DataFrame** 
**データストリーム** **データフレーム** 

Nature Continuous, unbounded flow of schematized data 
性質 スキーマ化されたデータの連続的で無限のフロー 

Static, finite collection of schematized data 
静的で有限のスキーマ化されたデータのコレクション 

Processing (Near) real-time processing producing fresh feature data 
処理 （ほぼ）リアルタイム処理による新鮮なフィーチャーデータの生成 

Batch processing with high latency feature data 
高遅延のフィーチャーデータによるバッチ処理 

Windowing Requires windows to segment data 
ウィンドウ化 データをセグメント化するためにウィンドウが必要 

Operates on the entire dataset 
全体のデータセットで操作 

State Stateful or stateless data processing 
状態 有状態または無状態のデータ処理 

Stateless data processing 
無状態のデータ処理 

Examples Financial transactions and clickstreams 
例 金融取引とクリックストリーム 

Database tables 
データベーステーブル 

Both datastreams and DataFrames have schemas. 
データストリームとDataFramesの両方にはスキーマがあります。 

Operations on datastreams are typically stateful and time-sensitive (with low latency). 
データストリームに対する操作は、通常、有状態で時間に敏感（低遅延）です。 

Windows convert the infinite stream into a bounded set of events that are processed together. 
ウィンドウは無限のストリームを、共に処理される有限のイベントセットに変換します。 

Datastreams also enable easy incremental computation. 
データストリームは、簡単な増分計算も可能にします。 

In contrast, DataFrames represent a static, bounded collection of data (a table) and are processed in batches. 
対照的に、DataFramesは静的で有限のデータコレクション（テーブル）を表し、バッチで処理されます。 

###### Dataflow Programming 
データストリームを使用したデータフロープログラミングでは、オペレーターがその入力（データソースまたは他のオペレーター）からデータを消費し、データに対して計算を行い、出力（他のオペレーターまたは1つ以上のデータシンク）にデータを生成します。 
###### Dataflow Programming 
In dataflow programming with datastreams, operators consume data from their inputs (either data sources or other operators), perform computations on the data, and produce data to their output (either other operators or one or more data sinks). 

Operators without input edges are called data sources and operators without output edges are called _data sinks. 
入力エッジのないオペレーターはデータソースと呼ばれ、出力エッジのないオペレーターは_data sinks_と呼ばれます。 

A dataflow graph must have at least one data source and one data sink. 
データフローグラフには、少なくとも1つのデータソースと1つのデータシンクが必要です。 

A streaming feature pipeline has one or more data sources and one or more feature groups as data sinks. 
ストリーミングフィーチャーパイプラインには、1つ以上のデータソースと1つ以上のフィーチャーグループがデータシンクとしてあります。 

Operators can accept multiple input streams and produce multiple output streams. 
オペレーターは複数の入力ストリームを受け入れ、複数の出力ストリームを生成できます。 

They can also split a single input stream into multiple output streams for parallel processing. 
また、単一の入力ストリームを複数の出力ストリームに分割して並列処理を行うこともできます。 

For example, if you have a lot of data to process, you can split the stream by the event’s primary key, so that the events can be processed in parallel on different CPUs or servers, helping your system scale to process more data in parallel. 
例えば、処理するデータが大量にある場合、イベントの主キーでストリームを分割することで、イベントを異なるCPUやサーバーで並列に処理できるようにし、システムがより多くのデータを並列に処理できるようにします。 

You can also merge multiple input streams into a single output stream with a join transformation. 
また、複数の入力ストリームを結合変換を使用して単一の出力ストリームにマージすることもできます。 

To boost throughput and minimize latency, different operators (or pipeline stages) can run in parallel, a concept known as task parallelism. 
スループットを向上させ、遅延を最小限に抑えるために、異なるオペレーター（またはパイプラインステージ）が並列に実行できる、タスク並列性として知られる概念があります。 

Data exchange between operators can occur through several mechanisms: 
オペレーター間のデータ交換は、いくつかのメカニズムを通じて行われることがあります：

_Forward data exchange_ 
データは、分配やルーティングを変更することなく、次の下流オペレーターに直接渡されます。 
_Forward data exchange_ Data is passed directly to the next downstream operator without altering distribution or routing. 

_Broadcast data exchange_ 
同じデータのコピーがすべての下流オペレーターに送信され、設定やルックアップテーブルのような共有データを分配するのに便利です。 
_Broadcast data exchange_ A copy of the same data is sent to all downstream operators, which is useful for distributing shared data like configuration or lookup tables. 

_Key-based data exchange_ 
データはキーによってルーティングされ、同じキーを持つレコードが同じオペレーターによって処理されることを保証し、並列の有状態操作（例：集約、結合）を可能にします。 
_Key-based data exchange_ Data is routed by key, ensuring records with the same key are processed by the same operator, enabling parallel stateful operations (e.g., aggregations, joins). 

_Random data exchange_ 
データはオペレーター間でランダムに分配され、無状態操作の負荷を均等に分配しますが、データのローカリティは保持されません。 
_Random data exchange_ Data is randomly distributed across operators, balancing load for stateless operations but without preserving data locality. 

Now that we have introduced the main abstractions in dataflow programming for stream processing, we will look at data transformations in operators. 
ストリーム処理のためのデータフロープログラミングにおける主要な抽象概念を紹介したので、オペレーターにおけるデータ変換を見ていきます。 

###### Stateless and Stateful Data Transformations 
_Stateless data processing does not maintain any internal state, and stateless data transformations do not depend on any event in the past. 
_無状態のデータ処理は内部状態を保持せず、無状態のデータ変換は過去のイベントに依存しません。 

As such, stateless data transformations are easily parallelized, as events can be processed independently and in any order. 
そのため、無状態のデータ変換は容易に並列化でき、イベントは独立して任意の順序で処理できます。 

In the event of failure, stateless data transformations can be safely rerun, assuming idempotent and/or atomic updates to output feature stores. 
障害が発生した場合、無状態のデータ変換は安全に再実行でき、出力フィーチャーストアへの冪等および/または原子的な更新が前提となります。 

Out-of-order data is when events arrive for processing in an order that’s different from their event-time order (for example, due to network delays, disconnected operation, and so on). 
順序外データとは、イベントがそのイベント時間の順序とは異なる順序で処理のために到着することです（例えば、ネットワーク遅延や切断された操作などによる）。 

Out-of-order data must be handled in stream-processing pipelines, as it is considered part of normal operation, not an exceptional condition. 
順序外データは、ストリーム処理パイプラインで処理される必要があります。これは、通常の操作の一部と見なされ、例外的な条件ではありません。 

Stream processing supports stateful data transformations that enable the efficient implementation of data transformations for ML features such as: 
ストリーム処理は、有効なデータ変換を可能にする有状態のデータ変換をサポートしています。これにより、ML機能のデータ変換が効率的に実装されます：

_Rolling aggregations_ 
これを使用して、時間の経過に伴うトレンドをキャプチャできます（例えば、過去1時間/日/週のクレジットカード支出）。 
_Rolling aggregations_ You can use these over a period of time to capture trends in time-series data (such as credit card spend in the last hour/day/week). 

_Session-based features_ 
これには、ユーザーセッションのクリック数や期間が含まれます。 
_Session-based features_ These include the number of clicks or duration for a user session.



_Lag features_ These capture the value of a variable at a previous time step (such as yesterday’s air quality).
_Lag features_（ラグ特徴量）これらは、前の時間ステップ（例えば、昨日の空気質）の変数の値をキャプチャします。

_Cumulative sums and counts_ These include capturing customer lifetime value through the amount spent by a customer.
_Cumulative sums and counts_（累積和とカウント）これらは、顧客が支出した金額を通じて顧客の生涯価値をキャプチャすることを含みます。

_Time since last event_ This includes when and where a credit card was most recently used, and it helps identify geographic fraud attacks.
_Time since last event_（最後のイベントからの時間）これには、クレジットカードが最近使用された時期と場所が含まれ、地理的な詐欺攻撃を特定するのに役立ちます。

_Windowed aggregations_ These provide insights into recent spikes or drops in activity (such as anomalous fraud activity in a geographic area).
_Windowed aggregations_（ウィンドウ集約）これらは、最近の活動の急増や急減に関する洞察を提供します（例えば、特定の地域における異常な詐欺活動など）。

_Stateful joins_ You can use these, for example, to join incoming credit card transactions with a stream of metadata about credit cards that’s read from a lakehouse table.
_Stateful joins_（状態を持つ結合）これらは、例えば、到着するクレジットカード取引を、レイクハウステーブルから読み取ったクレジットカードに関するメタデータのストリームと結合するために使用できます。

_Stateful data processing maintains state about previously processed events. The state_ can be updated when processing new events, and the state can be used to parameter‐ ize data transformations.
_状態を持つデータ処理は、以前に処理されたイベントに関する状態を維持します。_その状態は、新しいイベントを処理する際に更新でき、データ変換をパラメータ化するために使用できます。

For these reasons, parallelizing stateful data transformations is more challenging than parallelizing stateless data transformations.
これらの理由から、状態を持つデータ変換を並列化することは、状態を持たないデータ変換を並列化することよりも難しいです。

State needs to be partitioned correctly and reliably recovered in the case of failures.
状態は正しくパーティション分けされ、障害が発生した場合には信頼性を持って回復される必要があります。

There are an increasing number of stream-processing frameworks that can be used to implement stateless and stateful data transformations.
状態を持たないデータ変換と状態を持つデータ変換を実装するために使用できるストリーム処理フレームワークの数が増加しています。

Here, we introduce the most popular open source stream-processing frameworks that support a number of different programming languages:
ここでは、さまざまなプログラミング言語をサポートする最も人気のあるオープンソースのストリーム処理フレームワークを紹介します。

_Apache Flink_ This supports many built-in stateful and stateless data transformation operations as well as (high-performance) user-defined functions in Java using a DataStream API or a Table API in SQL.
_Apache Flink_（アパッチ・フリンク）これは、多くの組み込みの状態を持つおよび状態を持たないデータ変換操作をサポートし、JavaのDataStream APIまたはSQLのTable APIを使用して（高性能の）ユーザー定義関数をサポートします。

_Quix and Pathway_ These are single-host stream-processing engines with Python APIs. They support stateful and stateless data transformations using built-in operators (Pathway has a Rust engine for high performance).
_QuixとPathway_（クイックスとパスウェイ）これらは、Python APIを持つシングルホストのストリーム処理エンジンです。これらは、組み込みのオペレーターを使用して状態を持つおよび状態を持たないデータ変換をサポートします（Pathwayは高性能のためのRustエンジンを持っています）。

_RisingWave_ This is a distributed stream-processing engine built in Rust that supports built-in stateful and stateless data transformation operators in both SQL and Python. It also includes its own row-oriented store, so you can query the streaming state directly with SQL.
_RisingWave_（ライジングウェーブ）これは、Rustで構築された分散ストリーム処理エンジンで、SQLとPythonの両方で組み込みの状態を持つおよび状態を持たないデータ変換オペレーターをサポートします。また、独自の行指向ストアも含まれているため、ストリーミング状態を直接SQLでクエリできます。

_Apache Spark Structured Streaming_ This supports many built-in stateful and stateless data transformation operators using the high-performance Java/Scala engine, as well as lower-performance user-defined functions in Python.
_Apache Spark Structured Streaming_（アパッチ・スパーク・ストラクチャード・ストリーミング）これは、高性能のJava/Scalaエンジンを使用して多くの組み込みの状態を持つおよび状態を持たないデータ変換オペレーターをサポートし、Pythonでの低性能のユーザー定義関数もサポートします。

_[Feldera](https://oreil.ly/Lg2jA)_ This is an open source stream-processing engine built in Rust that supports builtin stateful and stateless data transformation operators in SQL, with support for high-performance incremental computations. User-defined functions can be implemented in Rust.
_[Feldera](https://oreil.ly/Lg2jA)_[（フェルデラ）これは、SQLで組み込みの状態を持つおよび状態を持たないデータ変換オペレーターをサポートするRustで構築されたオープンソースのストリーム処理エンジンで、高性能の増分計算をサポートします。ユーザー定義関数はRustで実装できます。

We will look now in more detail at two of these streaming engines: Apache Flink is the most widely used and capability-rich distributed stream processing engine, and Feldera is a developer-friendly streaming engine in SQL with support for incremental views.
これから、これらのストリーミングエンジンのうち2つをより詳細に見ていきます：Apache Flinkは最も広く使用されている機能豊富な分散ストリーム処理エンジンであり、Felderaは増分ビューをサポートするSQLの開発者に優しいストリーミングエンジンです。

Apache Flink combines functional programming with streaming APIs in Java as well as a Table API in SQL, while Feldera emphasizes declarative SQL.
Apache Flinkは、JavaのストリーミングAPIとTable APIを組み合わせた関数型プログラミングを行い、Felderaは宣言的SQLを強調します。

Both Flink and Feldera process data as it arrives in a continuous event-driven manner, unlike frameworks that rely on microbatching (such as Apache Spark).
FlinkとFelderaの両方は、Apache Sparkのようなマイクロバッチ処理に依存するフレームワークとは異なり、データが到着する際に連続的なイベント駆動型の方法でデータを処理します。

Per-event processing enables subsecond feature freshness in real-time ML systems, while microbatching increases feature freshness to tens of seconds or more.
イベントごとの処理は、リアルタイムのMLシステムにおいてサブ秒の特徴の新鮮さを可能にし、マイクロバッチ処理は特徴の新鮮さを数十秒以上に増加させます。

Apache Flink is distributed and can be scaled out on a cluster (up to thousands of nodes), while Feldera is currently a single-host engine (although it can still scale on modern hardware to process >1M events per second for many streaming workloads).
Apache Flinkは分散型であり、クラスター上でスケールアウト可能（最大数千ノードまで）ですが、Felderaは現在シングルホストエンジンです（ただし、現代のハードウェア上で1秒あたり100万件以上のイベントを処理するためにスケールすることは可能です）。

###### Apache Flink
Flink’s DataStream API supports data transformation operators on an event stream, including:
###### Apache Flink（アパッチ・フリンク）
FlinkのDataStream APIは、イベントストリーム上のデータ変換オペレーターをサポートしており、以下を含みます：

_map_ This applies a function to each event in the stream: 
_map_（マップ）これは、ストリーム内の各イベントに関数を適用します：
```     
stream.map(evt -> evt.value * 2)
```

_filter_ This removes events that do not match a condition: 
_filter_（フィルター）これは、条件に一致しないイベントを削除します：
```     
stream.filter(evt -> evt.value > 10)
```

_keyBy_ This partitions the stream based on a key, so that events can be processed in parallel by many workers. It returns a KeyedStream: 
_keyBy_（キーによる分割）これは、キーに基づいてストリームをパーティション分けし、イベントを多くのワーカーによって並列処理できるようにします。これはKeyedStreamを返します：
```     
stream.keyBy(evt -> evt.pk)
```

_reduce_ This performs incremental aggregation on a KeyedStream, combining events with the same key using a user-defined associative function:
_reduce_（リデュース）これは、KeyedStream上で増分集約を行い、同じキーを持つイベントをユーザー定義の結合関数を使用して結合します：
```     
stream.keyBy(evt -> evt.pk)        
.reduce((a, b) -> a + b);
```

_window_ On a KeyedStream, this groups elements into finite sets based on time or count for aggregation: 
_window_（ウィンドウ）KeyedStream上で、これは集約のために時間またはカウントに基づいて要素を有限のセットにグループ化します：
```     
stream.keyBy(evt ->evt.pk)        
.window(TumblingEventTimeWindows.of(Time.seconds(10)))
```

If you implement custom UDFs in Java, the functions should be Java serializable so that they can be shipped to workers.
JavaでカスタムUDFを実装する場合、関数はJavaシリアライズ可能である必要があり、ワーカーに送信できるようにする必要があります。

For Apache Flink’s Table SQL API, queries are optimized and translated into native Flink jobs.
Apache FlinkのTable SQL APIの場合、クエリは最適化され、ネイティブFlinkジョブに変換されます。

Apache Flink also provides a Complex Event Processing (CEP) library that can be used to specify patterns as finite-state machines that match specific event sequences.
Apache Flinkは、特定のイベントシーケンスに一致する有限状態機械としてパターンを指定するために使用できる複雑なイベント処理（CEP）ライブラリも提供しています。

For example, in our credit card fraud system, we could implement rules such as “Block a credit card that has been used more than 10 times in the last 5 minutes”:
例えば、私たちのクレジットカード詐欺システムでは、「過去5分間に10回以上使用されたクレジットカードをブロックする」といったルールを実装できます：
```   
Pattern<Transaction, ?> fraudPattern =    
Pattern.<Transaction>begin("chainAttack")     
.where(evt -> evt.amount > 50) // Only transactions > 50 dollars     
.timesOrMore(10) // 10 or more times     
.within(Time.minutes(5)); // Within 5 minutes   

PatternStream<Transaction> patternStream =    
CEP.pattern(transactions, fraudPattern);   

DataStream<String> alerts = patternStream     
.select((PatternSelectFunction<Transaction, String>) pattern -> {       
Transaction first = pattern.get("largeTx").get(0);       
return "Fraud detected on card: " + first.cardId;     
});
```

###### Feldera
###### Feldera（フェルデラ）
Feldera provides a SQL API that supports a variety of data transformation operators on an event stream (represented internally as a table of records):
Felderaは、イベントストリーム上のさまざまなデータ変換オペレーターをサポートするSQL APIを提供します（内部的にはレコードのテーブルとして表現されます）：

_Map_ This is implemented via the SELECT clause, applying expressions directly to each record: 
_Map_（マップ）これはSELECT句を介して実装され、各レコードに直接式を適用します：
```     
SELECT value * 2 AS transformed_value FROM stream
```

_Filter_ This is implemented as a `WHERE clause, removing records that do not match a` condition: 
_Filter_（フィルター）これは`WHERE句`として実装され、条件に一致しないレコードを削除します：
```     
SELECT * FROM stream WHERE value > 10
```

_Reduce_ This is analogous to Flink’s reduce operator, and it’s implemented by writing a UDF in SQL or Rust and applying it as an associative function with GROUP BY: 
_Reduce_（リデュース）これはFlinkのリデュースオペレーターに類似しており、SQLまたはRustでUDFを書いて、GROUP BYで結合関数として適用することによって実装されます：
```     
SELECT MY_UDF(value) AS reduced_value FROM stream GROUP BY key
```

_Partition_ 
```   
PARTITION BY logically partitions the stream by key, enabling parallel processing 
```
_Partition_（パーティション） 
```   
PARTITION BYは論理的にストリームをキーでパーティション分けし、並列処理を可能にします 
```

across available CPUs. It’s often used before window or aggregation functions: 
利用可能なCPUにわたって。これは、ウィンドウまたは集約関数の前に使用されることがよくあります：
```     
SELECT key, value FROM stream PARTITION BY key
```

_Windowing_ Feldera provides custom SQL extensions to define windows directly within queries: 
_Windowing_（ウィンドウ処理）Felderaは、クエリ内でウィンドウを直接定義するためのカスタムSQL拡張を提供します：
```     
SELECT key, COUNT(*) AS count       
FROM stream WINDOW TUMBLING (10 SECONDS) GROUP BY key
```

One important consideration when writing streaming programs with Feldera is that long-running windows can accumulate state indefinitely.
Felderaでストリーミングプログラムを書く際の重要な考慮事項は、長時間実行されるウィンドウが状態を無限に蓄積する可能性があることです。

To prevent unbounded state growth (and potential out-of-memory errors), you can define state expiration policies using `RETAIN.
無限の状態成長（および潜在的なメモリ不足エラー）を防ぐために、`RETAIN`を使用して状態の有効期限ポリシーを定義できます。

For example, the following query creates a 10-second tumbling window and specifies that each window’s state is discarded 1 hour after it closes:
例えば、次のクエリは10秒のタムブリングウィンドウを作成し、各ウィンドウの状態が閉じた1時間後に破棄されることを指定します：
```   
SELECT key, COUNT(*) AS count FROM stream WINDOW TUMBLING (10 SECONDS)     
RETAIN 1 HOUR GROUP BY key;
```

###### Benchmarking
###### ベンチマーキング
There is a trade-off between latency and throughput in streaming systems.
ストリーミングシステムには、レイテンシとスループットの間にトレードオフがあります。

You want to process events both with low latency and at high throughput.
イベントを低レイテンシで高スループットで処理したいです。

However, if you push throughput beyond a certain threshold, processing latency will rise.
ただし、スループットを特定の閾値を超えて押し上げると、処理レイテンシが上昇します。

Most streaming feature pipelines should publish an SLO for the 95th or 99th percentile latency.
ほとんどのストリーミングフィーチャーパイプラインは、95パーセンタイルまたは99パーセンタイルのレイテンシに対するSLOを公開する必要があります。

When the system is overloaded and throughput keeps increasing, latency will eventually exceed this SLO.
システムが過負荷になり、スループットが増加し続けると、レイテンシは最終的にこのSLOを超えることになります。

You should benchmark to find out the latency and throughput scalability limits of your streaming feature pipelines.
ストリーミングフィーチャーパイプラインのレイテンシとスループットのスケーラビリティの限界を見つけるためにベンチマークを行うべきです。

###### Windowed Aggregations
###### ウィンドウ集約
Windows define start and end boundaries over an event stream, enabling you to compute functions, such as aggregations, over the data within the window.
ウィンドウはイベントストリームの開始と終了の境界を定義し、ウィンドウ内のデータに対して集約などの関数を計算できるようにします。

For feature engineering, _windowed aggregations help capture temporal patterns or trends,_ adding predictive power to real-time ML systems such as fraud detection, recommendation engines, and predictive maintenance applications.
フィーチャーエンジニアリングにおいて、_ウィンドウ集約は時間的なパターンやトレンドをキャプチャするのに役立ち、_詐欺検出、推薦エンジン、予測保守アプリケーションなどのリアルタイムMLシステムに予測力を追加します。

Figure 9-7 shows a generic
図9-7は一般的なものを示しています。



streaming architecture that computes windowed aggregations over an input event stream and writes computed features to a feature group.
ストリーミングアーキテクチャは、入力イベントストリームに対してウィンドウ集約を計算し、計算された特徴をフィーチャーグループに書き込みます。

_Figure 9-7. Windowed aggregations require an assigner function that maps events to windows, policies for creating and destroying windows, a bucket in the window for storing events, a trigger condition and evaluation function for computing aggregates over events in a bucket, and a sink for the computed aggregations (a feature group)._
_Figure 9-7. ウィンドウ集約には、イベントをウィンドウにマッピングするアサイナ関数、ウィンドウを作成および破棄するためのポリシー、イベントを格納するためのウィンドウ内のバケット、バケット内のイベントに対して集約を計算するためのトリガ条件および評価関数、計算された集約のためのシンク（フィーチャーグループ）が必要です。_

The main components involved in computing windowed aggregations are:
ウィンドウ集約を計算する際に関与する主なコンポーネントは次のとおりです。

_Unbounded event stream_ This is the incoming events from one or more streaming data sources.
_無限イベントストリーム_ これは、1つ以上のストリーミングデータソースからの受信イベントです。

_Window assigner_ The window assigner extracts timestamps from events and then maps events to one or more windows. 
_ウィンドウアサイナ_ ウィンドウアサイナは、イベントからタイムスタンプを抽出し、イベントを1つ以上のウィンドウにマッピングします。

For example, in a 10-minute time window aggregation, a temporal condition checks events in the event stream to see whether their `event_time` falls within the window’s 10-minute boundaries. 
例えば、10分間の時間ウィンドウ集約では、時間条件がイベントストリーム内のイベントをチェックし、それらの`event_time`がウィンドウの10分間の境界内にあるかどうかを確認します。

If the event meets this condition, it is assigned to the window.
イベントがこの条件を満たす場合、それはウィンドウに割り当てられます。

_Window type, state retention policy, and watermark_ These define when a window is created and/or destroyed.
_ウィンドウタイプ、状態保持ポリシー、およびウォーターマーク_ これらは、ウィンドウが作成される時期および/または破棄される時期を定義します。

_Trigger condition_ This specifies when to evaluate the window. 
_トリガ条件_ これは、ウィンドウを評価するタイミングを指定します。

The trigger condition depends on the window type. 
トリガ条件はウィンドウタイプに依存します。

Some windows emit results only at the end of the window, while others emit for every new event.  
一部のウィンドウはウィンドウの終了時にのみ結果を出力しますが、他のウィンドウは新しいイベントごとに出力します。

_Evaluation functions_ These are typically aggregation functions, such as count, sum, and max, and they are computed over the window’s events.
_評価関数_ これらは通常、カウント、合計、最大値などの集約関数であり、ウィンドウ内のイベントに対して計算されます。

_Sink_ The sinks are the destination feature group(s) in the feature store for the computed feature value(s).
_シンク_ シンクは、計算された特徴値のためのフィーチャーストア内の宛先フィーチャーグループです。

Different stream-processing engines support different window types. 
異なるストリーム処理エンジンは異なるウィンドウタイプをサポートします。

For example, Apache Flink supports session windows and global windows (see Figure 9-8).
例えば、Apache Flinkはセッションウィンドウとグローバルウィンドウをサポートしています（図9-8を参照）。

_Figure 9-8. Session and global window aggregations. New session windows are created when new sessions are started or after a period of inactivity for an existing session. Global windows never close while the streaming program runs._
_Figure 9-8. セッションおよびグローバルウィンドウ集約。新しいセッションが開始されると、新しいセッションウィンドウが作成されるか、既存のセッションの非アクティブ期間の後に作成されます。グローバルウィンドウは、ストリーミングプログラムが実行されている間は決して閉じません。_

The session window is useful in computing features of user sessions in entertainment and retail applications—such as activity and engagement levels per session. 
セッションウィンドウは、エンターテインメントや小売アプリケーションにおけるユーザーセッションの特徴を計算するのに役立ちます—例えば、セッションごとの活動やエンゲージメントレベルなどです。

Each event typically contains a session ID (or one is inferred from activity/inactivity gaps).
各イベントには通常、セッションIDが含まれています（または、活動/非活動のギャップから推測されます）。

The window assigner maps events to their session window. 
ウィンドウアサイナは、イベントをそのセッションウィンドウにマッピングします。

A session window starts when a session begins and closes after a period of inactivity. 
セッションウィンドウは、セッションが開始されるときに始まり、非アクティブ期間の後に閉じます。

The number of session windows usually matches the number of active sessions, though a window may persist briefly after inactivity before closing. 
セッションウィンドウの数は通常、アクティブなセッションの数と一致しますが、ウィンドウは閉じる前に非アクティブの後に短時間持続することがあります。

When the session ends (a trigger condition), aggregated features are computed and written to the feature store.  
セッションが終了すると（トリガ条件）、集約された特徴が計算され、フィーチャーストアに書き込まれます。

The global window is useful for computing global features, such as trending products in an ecommerce website. 
グローバルウィンドウは、eコマースウェブサイトでのトレンド商品など、グローバルな特徴を計算するのに役立ちます。

Its window assigner places all relevant events (e.g., purchases, page views) into a single global window spanning the entire streaming job runtime. 
そのウィンドウアサイナは、すべての関連イベント（例：購入、ページビュー）をストリーミングジョブの実行時間全体にわたる単一のグローバルウィンドウに配置します。

The window is created when the streaming job starts and closes when it ends.
ウィンドウは、ストリーミングジョブが開始されるときに作成され、終了するときに閉じます。

Aggregations are typically emitted at regular intervals (e.g., hourly, daily).
集約は通常、定期的な間隔（例：毎時、毎日）で出力されます。

Although global and session windows are useful, there are other far more popular types of windows for computing aggregated features for ML—the rolling aggregation and the time window.
グローバルウィンドウとセッションウィンドウは便利ですが、MLのための集約された特徴を計算するための他のはるかに人気のあるウィンドウタイプがあります—ローリング集約と時間ウィンドウです。

###### Rolling Aggregations
###### ローリング集約

Rolling aggregations create the freshest aggregated features in streaming feature pipelines.
ローリング集約は、ストリーミングフィーチャーパイプラインで最新の集約特徴を作成します。

They are a form of windowed aggregation, but without distinct, fixed windows.
それらはウィンドウ集約の一形態ですが、明確で固定されたウィンドウはありません。

Instead, they compute over a continuously moving time interval. 
代わりに、継続的に移動する時間間隔で計算します。

We’ll still call this interval a “window,” since it behaves like a bounded collection of temporally related events.
この間隔を「ウィンドウ」と呼び続けます。なぜなら、それは時間的に関連するイベントの制約されたコレクションのように振る舞うからです。

A window assigner extracts each event’s event_time and maps it to one or more rolling windows. 
ウィンドウアサイナは、各イベントの`event_time`を抽出し、それを1つ以上のローリングウィンドウにマッピングします。

For example, if there are two rolling windows, one for the previous minute and one for the previous hour:
例えば、前の1分間のための1つのローリングウィンドウと、前の1時間のための1つのローリングウィンドウがある場合：

- An event that is 10 seconds old is added to both windows.
- 10秒前のイベントは両方のウィンドウに追加されます。

- An event that is 70 seconds old is added only to the hour window.
- 70秒前のイベントは、1時間のウィンドウにのみ追加されます。

- Late-arriving events are ignored by both windows but should be handled separately for historical processing.
- 遅れて到着したイベントは両方のウィンドウで無視されますが、履歴処理のために別途処理する必要があります。

Rolling aggregations are evaluated immediately when a new event arrives, giving the lowest possible latency. 
ローリング集約は、新しいイベントが到着するとすぐに評価され、可能な限り低いレイテンシを提供します。

Each arrival triggers a new aggregated value, making rolling aggregations row size–preserving transformations. 
各到着は新しい集約値をトリガし、ローリング集約を行のサイズを保持する変換にします。

The implication is that they are memory-intensive transformations.
その結果、これらはメモリ集約的な変換であることを意味します。

Most streaming engines provide built-in aggregation functions (min, `max`, `mean`, `median`, sum, standard deviation, percentile) to compute rolling aggregations. 
ほとんどのストリーミングエンジンは、ローリング集約を計算するための組み込み集約関数（min、`max`、`mean`、`median`、sum、標準偏差、パーセンタイル）を提供します。

In Figure 9-9, we compute the sum aggregation on the amount column over the last hour, where the event_time column is used to select the rows for the last hour.
図9-9では、`amount`列の合計集約を過去1時間にわたって計算します。ここで、`event_time`列は過去1時間の行を選択するために使用されます。

_Figure 9-9. This rolling aggregation computes the sum of the amount spent in the previous 60 minutes for a given credit card. Every time a new event arrives, the sum is recomputed and immediately updated in the feature store. Events outside the last 60 minutes are ignored._
_Figure 9-9. このローリング集約は、特定のクレジットカードに対して過去60分間に費やされた金額の合計を計算します。新しいイベントが到着するたびに、合計が再計算され、フィーチャーストアに即座に更新されます。過去60分を超えるイベントは無視されます。_

In stream processing, rolling aggregations have traditionally been seen as too computationally expensive for large-scale workloads, since each new event triggers a recomputation over all events in the window. 
ストリーム処理において、ローリング集約は、各新しいイベントがウィンドウ内のすべてのイベントに対して再計算をトリガするため、大規模なワークロードに対して計算コストが高すぎると伝統的に見なされてきました。

The introduction of incremental views (covered later in this chapter) reduces this complexity from linear time (relative to window size) to constant time. 
増分ビューの導入（この章の後半で説明します）は、この複雑さを線形時間（ウィンドウサイズに対して）から定数時間に減少させます。

If your stream-processing engine does not support incremental views, you should probably use time window aggregations, as they are far less computationally intensive.
ストリーム処理エンジンが増分ビューをサポートしていない場合は、時間ウィンドウ集約を使用することをお勧めします。なぜなら、それらははるかに計算負荷が少ないからです。

###### Time Window Aggregations
###### 時間ウィンドウ集約

A _time window is a set of temporally related, often contiguous, events. 
_時間ウィンドウ_ は、時間的に関連する、しばしば連続したイベントの集合です。

Time-windowed aggregations summarize data over a fixed duration:
時間ウィンドウ集約は、固定された期間にわたってデータを要約します：

_Window length_ The time between a window’s start and end
_ウィンドウの長さ_ ウィンドウの開始と終了の間の時間

_Window size_ The number of events in the window’s bucket
_ウィンドウのサイズ_ ウィンドウのバケット内のイベントの数

_Window assigner_ Maps events to windows based on whether the event’s event_time falls between the window’s start and end times
_ウィンドウアサイナ_ イベントの`event_time`がウィンドウの開始時刻と終了時刻の間にあるかどうかに基づいて、イベントをウィンドウにマッピングします。

Unlike rolling aggregations, many time windows can be open simultaneously for different (possibly overlapping) intervals. 
ローリング集約とは異なり、多くの時間ウィンドウは異なる（重複する可能性のある）間隔で同時に開くことができます。

As time advances, windows are continually created and closed, allocating and freeing resources, respectively.
時間が進むにつれて、ウィンドウは継続的に作成され、閉じられ、リソースがそれぞれ割り当てられたり解放されたりします。

The two most common types of windowed aggregations (shown in Figure 9-10) are:
ウィンドウ集約の最も一般的な2つのタイプ（図9-10に示されています）は次のとおりです：

_Tumbling windows_ A window that has a fixed size and does not overlap. Events will be assigned to exactly one window.
_タンブリングウィンドウ_ 固定サイズで重複しないウィンドウです。イベントは正確に1つのウィンドウに割り当てられます。

_Hopping (or sliding) windows_ A window that advances by a fixed interval called the hop size (or slide length) and can overlap with previous windows:
_ホッピング（またはスライディング）ウィンドウ_ ホップサイズ（またはスライド長）と呼ばれる固定間隔で進むウィンドウで、前のウィンドウと重複することがあります：

- Each hop triggers the window’s evaluation function, producing an output even if no events have changed.
- 各ホップはウィンドウの評価関数をトリガし、イベントが変更されていなくても出力を生成します。

- If the hop size is smaller than the window length, the window can be evaluated more frequently and the same event can be assigned to multiple windows.
- ホップサイズがウィンドウの長さより小さい場合、ウィンドウはより頻繁に評価され、同じイベントが複数のウィンドウに割り当てられることがあります。

- In Apache Flink, each hop will create a new window, and this means events are duplicated across windows. 
- Apache Flinkでは、各ホップが新しいウィンドウを作成し、これによりイベントがウィンドウ間で重複します。

If the hop size is much smaller than the window length, data duplication can become excessive and hurt pipeline scalability.
ホップサイズがウィンドウの長さよりもはるかに小さい場合、データの重複が過剰になり、パイプラインのスケーラビリティに悪影響を及ぼす可能性があります。

_Figure 9-10. Tumbling windows do not overlap, while hopping windows can overlap if the hop size is smaller than the window length. Tumbling windows are only evaluated (and, therefore, only output results) after the end of their time window, while hopping windows are evaluated at fixed intervals (the hop size)._
_Figure 9-10. タンブリングウィンドウは重複せず、ホッピングウィンドウはホップサイズがウィンドウの長さより小さい場合に重複することがあります。タンブリングウィンドウは、その時間ウィンドウの終了後にのみ評価され（したがって、結果を出力するのはその後のみ）、ホッピングウィンドウは固定間隔（ホップサイズ）で評価されます。_

Time windows need to be closed at some point to free up their resources (memory).
時間ウィンドウは、リソース（メモリ）を解放するために、いつかは閉じる必要があります。

A window’s state retention policy defines how long the bucket containing the events will be kept until it is closed.
ウィンドウの状態保持ポリシーは、イベントを含むバケットが閉じられるまでの保持期間を定義します。

You can keep time windows open (to accept events with a timestamp between the start and end of the window) for longer by defining a watermark on the window. 
ウィンドウにウォーターマークを定義することで、時間ウィンドウを長く開いたままにすることができます（ウィンドウの開始と終了の間にタイムスタンプを持つイベントを受け入れるため）。

A watermark is an upper bound on how late an event’s timestamp can be for it to be assigned to the time window. 
ウォーターマークは、イベントのタイムスタンプが時間ウィンドウに割り当てられるためにどれだけ遅れることができるかの上限です。

After the watermark has passed, the window is triggered and is closed by the streaming engine.
ウォーターマークが過ぎると、ウィンドウがトリガされ、ストリーミングエンジンによって閉じられます。

For example, if I am computing a one-hour time window aggregation for credit card transactions:
例えば、クレジットカード取引の1時間の時間ウィンドウ集約を計算している場合：

- With a three-hour watermark, an event arriving two hours late will still be assigned to the correct window.
- 3時間のウォーターマークを持つ場合、2時間遅れて到着したイベントは、正しいウィンドウに割り当てられます。

- With a one-hour watermark, that same event would be marked late and excluded.
- 1時間のウォーターマークを持つ場合、その同じイベントは遅れているとマークされ、除外されます。



When choosing a watermark duration, you should either:
水印の期間を選択する際には、次のいずれかを行うべきです：
- Be confident that no delayed events will arrive after the upper bound.
- 上限を超えた遅延イベントが到着しないと確信すること。
- Accept that late events arriving after the bound will be ignored.
- 上限を超えた遅延イベントが到着した場合、それらが無視されることを受け入れること。

Watermarks are a challenging concept to reason about. 
水印は考慮するのが難しい概念です。
They also make real-time ML systems less real-time by increasing evaluation delay for window aggregations (see Figure 9-11).
また、ウィンドウ集約の評価遅延を増加させることにより、リアルタイムMLシステムをリアルタイムでなくします（図9-11を参照）。

_Figure 9-11. Tumbling and hopping windows have different evaluation delays. The eval‐_ _uation delay can be extended by adding a watermark that accepts late events before the_ _watermark’s upper bound but produces less fresh features. Rolling aggregations have no_ _evaluation delay._
_図9-11. タンブリングウィンドウとホッピングウィンドウは異なる評価遅延を持ちます。評価遅延は、遅延イベントを水印の上限前に受け入れる水印を追加することで延長できますが、より新鮮な特徴を生成することは少なくなります。ロール集約には評価遅延がありません。_

On the other hand, watermarks enable applications and services that can be occasion‐ ally disconnected, due to network or device issues, to still provide real-time data for our ML system.
一方で、水印はネットワークやデバイスの問題により時折切断される可能性のあるアプリケーションやサービスが、私たちのMLシステムにリアルタイムデータを提供できるようにします。
For example, some credit card terminals can be used while discon‐ nected from the internet (for example, on an airplane), and when they come back online, they send their credit card transactions for processing.
例えば、いくつかのクレジットカード端末はインターネットから切断されている間（例えば、飛行機の中で）使用でき、オンラインに戻ると、処理のためにクレジットカード取引を送信します。
The late-arriving events may still be useful for predicting future credit card fraud if they are added to longer time windows, such as one-day time windows.
遅れて到着するイベントは、1日などの長い時間ウィンドウに追加される場合、将来のクレジットカード詐欺を予測するのに役立つ可能性があります。

We also may still want to save the late event to compute historical features from it, so that it can be transformed into historical feature data for training new models.
また、遅延イベントを保存して、そこから歴史的特徴を計算し、新しいモデルのトレーニング用の歴史的特徴データに変換したい場合もあります。
That is, the event should still make its way to the offline feature store, even if it is not used to compute any features in the online store:
つまり、そのイベントはオンラインストアで特徴を計算するために使用されなくても、オフラインフィーチャーストアに送られるべきです：
- In Apache Flink, you can use side outputs to process late-arriving events without disrupting the main processing flow.
- Apache Flinkでは、サイド出力を使用して、メイン処理フローを中断することなく遅延到着イベントを処理できます。
- In Hopsworks, your streaming application can handle late events by updating the Kafka event’s header to set a “late” property to true.
- Hopsworksでは、ストリーミングアプリケーションがKafkaイベントのヘッダーを更新して「遅延」プロパティをtrueに設定することで、遅延イベントを処理できます。
On ingestion, Hopsworks then only writes “late” events to the offline store, not the online store.
取り込み時に、Hopsworksは「遅延」イベントをオフラインストアにのみ書き込み、オンラインストアには書き込みません。

If you have a streaming-native architecture, you should not drop late events if you need them to later create training data or for RAG.
ストリーミングネイティブアーキテクチャを持っている場合、後でトレーニングデータやRAGを作成するために必要な遅延イベントをドロップすべきではありません。
There are two solutions to this problem.
この問題には2つの解決策があります。
One is to store all the raw events with event sourcing.
1つは、イベントソーシングを使用してすべての生イベントを保存することです。
Then, when you create feature data from historical data, you can run the same streaming feature pipeline against the event-sourced data.
その後、歴史的データから特徴データを作成する際に、イベントソースデータに対して同じストリーミングフィーチャーパイプラインを実行できます。
The other solution is to have your streaming feature pipeline compute the features on the late data but only write it to the offline store.
もう1つの解決策は、ストリーミングフィーチャーパイプラインが遅延データの特徴を計算し、オフラインストアにのみ書き込むことです。
If you do not want to miss any data, no matter how late it is, you should go with event sourcing.
データを見逃したくない場合は、遅延の有無にかかわらず、イベントソーシングを選択すべきです。

###### Choosing the Best Window Type for Aggregations
###### 集約のための最適なウィンドウタイプの選択

Table 9-3 provides a comparison of tumbling windows, hopping windows, and roll‐ ing aggregations.
表9-3は、タンブリングウィンドウ、ホッピングウィンドウ、およびロール集約の比較を提供します。

_Table 9-3. A comparison of tumbling windows, hopping windows, and rolling aggregations_
_表9-3. タンブリングウィンドウ、ホッピングウィンドウ、およびロール集約の比較_

**Tumbling windows** **Hopping windows** **Rolling aggregations**
**タンブリングウィンドウ** **ホッピングウィンドウ** **ロール集約**

Number of output rows
出力行数

Compute overhead
計算オーバーヘッド

Memory overhead
メモリオーバーヘッド

Row-size reducing. The window’s events are reduced to a single aggregated result.
行サイズを削減します。ウィンドウのイベントは単一の集約結果に減少します。

Low. No overlapping windows. Medium/High.
低。重複ウィンドウなし。中/高。
Overlapping windows.
重複ウィンドウ。

Row-size reducing. The result is aggregated over many events, producing fewer rows than the input.
行サイズを削減します。結果は多くのイベントにわたって集約され、入力よりも少ない行を生成します。
Medium/High. Scales inversely with hop size.
中/高。ホップサイズに反比例してスケールします。

Row-size preserving. The result is recomputed for every input event.
行サイズを保持します。結果はすべての入力イベントに対して再計算されます。
One output per event.
イベントごとに1つの出力。

Low with incremental views. High without.
インクリメンタルビューでは低。なしでは高。

Low. One aggregation computed per window.
低。ウィンドウごとに1つの集約が計算されます。

Low/Medium. No overlapping windows.
低/中。重複ウィンドウなし。

Tumbling windows work well for long, slowly changing time windows with large data volumes that could include late data.
タンブリングウィンドウは、遅延データを含む可能性のある大規模データボリュームを持つ長くゆっくりと変化する時間ウィンドウに適しています。
For example, a one-week tumbling aggregation can be “upgraded” to a hopping window with a one-day hop size to produce fresher outputs.
例えば、1週間のタンブリング集約は、1日ホップサイズのホッピングウィンドウに「アップグレード」されて、より新鮮な出力を生成できます。

In general, you should use rolling aggregations, if feasible.
一般的に、可能であればロール集約を使用すべきです。
They deliver the freshest features without the need for watermarks or evaluation delays.
それらは、水印や評価遅延なしで最も新鮮な特徴を提供します。
They can scale if:
スケールすることができます：
- Your online feature store supports the write rate and storage capacity needed.
- あなたのオンラインフィーチャーストアが必要な書き込みレートとストレージ容量をサポートしている場合。
- Your streaming engine supports incremental views.
- あなたのストリーミングエンジンがインクリメンタルビューをサポートしている場合。

###### Rolling Aggregations with Incremental Views
###### インクリメンタルビューを持つロール集約

Rolling aggregations can be implemented in Apache Flink with OVER aggregates that compute an aggregated value for every input row over a range of ordered rows.
ロール集約は、Apache FlinkでOVER集約を使用して、順序付けられた行の範囲にわたって各入力行の集約値を計算することで実装できます。

However, even though Apache Flink’s OVER aggregates can be partitioned over many workers, they do not scale well with increasing window size and increasing event throughput, as every new event triggers the recalculation of the aggregation function and its computational cost is proportional to the window size (see Figure 9-12).
しかし、Apache FlinkのOVER集約は多くのワーカーに分割できるにもかかわらず、ウィンドウサイズの増加とイベントスループットの増加に対してうまくスケールしません。なぜなら、すべての新しいイベントが集約関数の再計算を引き起こし、その計算コストはウィンドウサイズに比例するからです（図9-12を参照）。

_Figure 9-12. Without incremental views, rolling aggregations recompute the aggregation_ _over all N events. Computing for each new event costs O(N). With incremental views, it_ _is O(1) as the new event is processed with incremental state. Incremental views make_ _per-event rolling aggregations computationally feasible for ML systems._
_図9-12. インクリメンタルビューがない場合、ロール集約はすべてのNイベントにわたって集約を再計算します。各新しいイベントの計算コストはO(N)です。インクリメンタルビューを使用すると、新しいイベントはインクリメンタル状態で処理されるため、O(1)になります。インクリメンタルビューは、MLシステムにとってイベントごとのロール集約を計算可能にします。_

Incremental views solve the scalability challenge by avoiding full recomputation of aggregations when a new event arrives.
インクリメンタルビューは、新しいイベントが到着したときに集約の完全な再計算を回避することで、スケーラビリティの課題を解決します。
Instead, they reuse the previously computed value and apply only the changes introduced by new or removed events.
代わりに、以前に計算された値を再利用し、新しいイベントや削除されたイベントによって導入された変更のみを適用します。
As a result, the work performed is proportional to the input/output changes, not the window size.
その結果、実行される作業はウィンドウサイズではなく、入力/出力の変更に比例します。

[Feldera supports incremental view maintenance through its streaming engine DBSP](https://oreil.ly/SQqTW) [(DataBase inspired by Signal Processing). DBSP implements incremental views using](https://oreil.ly/SQqTW) Z-sets, a generalization of relational sets that track not only which elements are present but also how their counts change over time.
[Felderaは、ストリーミングエンジンDBSPを通じてインクリメンタルビューのメンテナンスをサポートしています](https://oreil.ly/SQqTW) [(信号処理に触発されたデータベース)。DBSPは、Z-setsを使用してインクリメンタルビューを実装します。Z-setsは、どの要素が存在するかだけでなく、それらのカウントが時間とともにどのように変化するかを追跡する関係セットの一般化です。_
In a traditional relational set, an element either exists (count = 1) or does not exist (count = 0).
従来の関係セットでは、要素は存在する（カウント=1）か存在しない（カウント=0）かのいずれかです。
In a Z-set, each ele‐ ment has an integer count that can be positive, zero, or negative:
Z-setでは、各要素は正、ゼロ、または負の整数カウントを持ちます：
- Positive counts represent insertions (adding events).
- 正のカウントは挿入（イベントの追加）を表します。
- Negative counts represent deletions (removing events).
- 負のカウントは削除（イベントの削除）を表します。

This allows Z-sets to represent deltas, the net change between two states, without storing the full state at each step.
これにより、Z-setsはデルタ、すなわち2つの状態間の純変化を表現でき、各ステップで完全な状態を保存する必要がなくなります。



For example, if the previous state had {apple: 5} and the new state has {apple: 3}, the delta is {apple: –2}. 
例えば、前の状態が {apple: 5} で新しい状態が {apple: 3} の場合、デルタは {apple: -2} です。

DBSP applies this delta to the existing state to update results efficiently. 
DBSPはこのデルタを既存の状態に適用して、結果を効率的に更新します。

Because DBSP runs on a single server, it can assume linear time and that each state has exactly one predecessor. 
DBSPは単一のサーバー上で動作するため、線形時間を仮定でき、各状態には正確に1つの前の状態があると考えられます。

This simplifies stream processing logic for developers while keeping aggregation updates fast and scalable. 
これにより、開発者にとってストリーム処理のロジックが簡素化され、集約の更新が迅速かつスケーラブルに保たれます。

Now, we will look at how to implement a rolling aggregation in Feldera. 
ここでは、Felderaでローリング集約を実装する方法を見ていきます。

The general process for deciding how to implement any kind of windowed aggregation is as follows: 
ウィンドウ集約の実装方法を決定するための一般的なプロセスは次のとおりです。

1. Choose the aggregation (sum, count, etc.) with the highest predictive power for your model. 
1. モデルに対して最も予測力の高い集約（合計、カウントなど）を選択します。

Choose the key to group by (optional): define the group over which the aggregation applies, such as credit card number or merchant ID. 
グループ化するキーを選択します（オプション）：集約が適用されるグループを定義します。例えば、クレジットカード番号や商人IDなどです。

2. Select the window size and window type: a rolling aggregation or time window. 
2. ウィンドウサイズとウィンドウタイプを選択します：ローリング集約または時間ウィンドウです。

If you chose a time window, pick the type from tumbling, hopping, or other. 
時間ウィンドウを選択した場合は、タムブリング、ホッピング、またはその他のタイプを選択します。

3. Handle missing data: decide how to treat windows with no data (for example, fill with zeros or NaNs). 
3. 欠損データを処理します：データがないウィンドウをどのように扱うかを決定します（例えば、ゼロまたはNaNで埋めるなど）。

###### Credit Card Fraud Streaming Features
###### クレジットカード詐欺ストリーミング機能

In our credit card fraud system, we are interested in aggregations over credit card transactions, so we group the transactions by cc_num before we compute the aggregations. 
私たちのクレジットカード詐欺システムでは、クレジットカード取引の集約に関心があるため、集約を計算する前に取引をcc_numでグループ化します。

We will use rolling aggregations of transaction sums and counts, as anomalous values of both of these features are predictive of credit card fraud. 
取引の合計とカウントのローリング集約を使用します。これらの特徴の異常値はクレジットカード詐欺の予測に役立ちます。

We will implement the rolling aggregations with incremental views, as they produce the precomputed freshest features and will introduce minimal latency to the online inference pipeline, thus helping our system meet its low-latency requirements. 
私たちは、ローリング集約をインクリメンタルビューで実装します。これにより、事前計算された最新の特徴が生成され、オンライン推論パイプラインに最小限のレイテンシを導入し、システムが低レイテンシ要件を満たすのに役立ちます。

Here, we show SQL in Feldera to compute rolling aggregations over credit card transactions with different time intervals (10 minutes, 1 hour, 1 day, 1 week) and two different aggregations (sum and count): 
ここでは、Felderaでクレジットカード取引に対して異なる時間間隔（10分、1時間、1日、1週間）と2つの異なる集約（合計とカウント）を使用してローリング集約を計算するSQLを示します。

```  
CREATE TABLE credit_card_transactions (     
    t_id BIGINT,     
    ts TIMESTAMP,     
    cc_num VARCHAR,     
    merchant_id VARCHAR,     
    amount DOUBLE,     
    ip_addr VARCHAR,     
    card_present BOOLEAN   
) WITH (     
    'connectors' = '[{transaction_source_config}]'   
);
```

Create a transaction table that represents the event stream. 
イベントストリームを表す取引テーブルを作成します。

We use a Feldera input connector to Apache Kafka to provide the transaction event stream. 
取引イベントストリームを提供するために、Felderaの入力コネクタをApache Kafkaに使用します。

Create a materialized view with our original transaction events enriched with our rolling aggregations. 
元の取引イベントにローリング集約を加えたマテリアライズドビューを作成します。

The `SELECT statement decides what columns are included in your output. 
`SELECT`文は、出力に含まれる列を決定します。

The materialized view contains all the transaction columns and additional columns containing the rolling aggregations—the sum and count for 10-minute, 1-hour, 1-day, and 7-day windows. 
マテリアライズドビューには、すべての取引列と、10分、1時間、1日、7日ウィンドウの合計とカウントを含む追加の列が含まれています。

Note that COUNT ignores NULL values, while COALESCE replaces NULL values with 0.  
COUNTはNULL値を無視し、COALESCEはNULL値を0に置き換えることに注意してください。

For our rolling aggregation columns, we define different window lengths: 
私たちのローリング集約列では、異なるウィンドウの長さを定義します：

```  
10_minute, 1_hour, 1_day, and 7_day. 
10分、1時間、1日、7日です。

Each window includes parameters for (1) the column to group the rows by cc_num, (2) the event_time column, and (3) the window (interval) length that includes the current row. 
各ウィンドウには、(1) 行をcc_numでグループ化する列、(2) event_time列、(3) 現在の行を含むウィンドウ（間隔）長が含まれます。

###### Tiled Time Window Aggregations
###### タイル時間ウィンドウ集約

[Airbnb’s Chronon framework provides an alternative solution to reduce the computa‐](https://oreil.ly/yGiTs) tional overhead of computing rolling aggregations called tiled time window aggrega‐ _tions. 
[AirbnbのChrononフレームワークは、タイル時間ウィンドウ集約と呼ばれるローリング集約の計算にかかる計算オーバーヘッドを削減するための代替ソリューションを提供します。]

Tiles partition a window of length N into M tiles, where M<<N, and compose aggregations using both the tiles with unaligned events at the start and end of the interval. 
タイルは長さNのウィンドウをMタイルに分割し（M<<N）、ウィンドウの開始と終了で整列していないイベントを持つタイルを使用して集約を構成します。

For example, say you want to compose a precise 240-hour aggregation from 24-hour tiles (computed daily) at 12:00 p.m. 
例えば、12:00 p.m.に24時間タイル（毎日計算された）から正確な240時間の集約を構成したいとします。

You will not have yet computed a tile for the current day’s events (from 12:00 a.m. to 12:00 p.m.), and you won’t have a tile for the events from 12:00 p.m. of the last day in the interval (the tile for that day contains events not included in the interval). 
その日のイベント（12:00 a.m.から12:00 p.m.まで）のタイルはまだ計算されておらず、ウィンドウ内の前日の12:00 p.m.のイベントのタイルもありません（その日のタイルにはウィンドウに含まれないイベントが含まれています）。

Tiled aggregations are computed by composing the precomputed tiles with on-demand aggregations over the unaligned events at the start and end of the interval. 
タイル集約は、事前計算されたタイルとウィンドウの開始と終了で整列していないイベントに対するオンデマンド集約を組み合わせることによって計算されます。

Tiled aggregation combines shifting left (precomputed tiles) with shifting right (on-demand aggregations). 
タイル集約は、左にシフト（事前計算されたタイル）することと、右にシフト（オンデマンド集約）することを組み合わせます。

In contrast, incremental views shift left the entire aggregation computation, reducing the latency for aggregated features for real-time ML systems. 
対照的に、インクリメンタルビューは全体の集約計算を左にシフトし、リアルタイムMLシステムの集約機能のレイテンシを減少させます。

###### ASOF Joins and Composition of Transformations
###### ASOF結合と変換の構成

Often you need to enrich event streams by joining event data with historical data from other data sources. 
イベントストリームを他のデータソースからの履歴データと結合して強化する必要があります。

For example, we might want to add to transaction events the status of the credit card that performed the transaction (active, blocked, Lost/ Stolen). 
例えば、取引イベントに取引を行ったクレジットカードのステータス（アクティブ、ブロック、紛失/盗難）を追加したいとします。

We also want to enrich the transaction events with the account_id and bank_id for the card that performed the transaction. 
また、取引を行ったカードのaccount_idとbank_idで取引イベントを強化したいと考えています。

In both of these examples, we join events in our event stream against time-series data from our data warehouse, and, for this, we will need to perform ASOF JOINs. 
これらの例の両方で、イベントストリーム内のイベントをデータウェアハウスの時系列データと結合する必要があり、そのためにASOF JOINを実行する必要があります。

An ASOF JOIN is required because the streaming feature pipeline should be able to be run in either real-time mode or backfill mode. 
ASOF JOINが必要なのは、ストリーミング機能パイプラインがリアルタイムモードまたはバックフィルモードのいずれかで実行できる必要があるからです。

In real-time mode, a given credit card might be “blocked,” while in backfill, at some point in time, it is “active.” 
リアルタイムモードでは、特定のクレジットカードが「ブロック」されている可能性がありますが、バックフィルでは、ある時点で「アクティブ」である可能性があります。

The join needs to enrich the transaction with the correct card status at the point in time of the transaction. 
結合は、取引の時点で正しいカードのステータスで取引を強化する必要があります。

We can also compose data transformations, such as defining an aggregation or filter using derived data. 
また、派生データを使用して集約やフィルタを定義するなど、データ変換を構成することもできます。

Composable transformations let us build layered systems, reuse tested code, and follow the DRY principle. 
合成可能な変換により、レイヤー化されたシステムを構築し、テスト済みのコードを再利用し、DRY原則に従うことができます。



In the next code snippet, we define a new invalid_card transformation as a materi‐ alized view that filters for transactions from cards not marked as `active in` ``` card_details. 
次のコードスニペットでは、`card_details`で「アクティブ」とマークされていないカードからのトランザクションをフィルタリングする新しいinvalid_card変換をマテリアライズドビューとして定義します。

This transformation uses an ASOF JOIN, and the data transformation is a filter (not an aggregation): 
この変換はASOF JOINを使用し、データ変換はフィルタ（集約ではない）です：

```  
CREATE TABLE card_details (     
    cc_num VARCHAR NOT NULL,     
    cc_expiry_date TIMESTAMP,     
    account_id VARCHAR NOT NULL,     
    bank_id VARCHAR NOT NULL,     
    issue_date TIMESTAMP,     
    card_type VARCHAR,     
    status VARCHAR,     
    last_modified TIMESTAMP   
) WITH (     
    'connectors' = '[{card_details_source_config}]'   
);   

CREATE MATERIALIZED VIEW invalid_card_transaction AS   
SELECT     
    t.cc_num,     
    t.ts AS event_time,     
    (cd.status != 'active') AS invalid_card   
FROM credit_card_transactions AS t   
LEFT ASOF JOIN card_details AS cd     
    MATCH_CONDITION (t.ts >= cd.last_modified)     
    ON t.cc_num = cd.cc_num   
``` 
```  
この変換はASOF JOINを使用し、データ変換はフィルタ（集約ではない）です：

CREATE TABLE card_details (     
    cc_num VARCHAR NOT NULL,     
    cc_expiry_date TIMESTAMP,     
    account_id VARCHAR NOT NULL,     
    bank_id VARCHAR NOT NULL,     
    issue_date TIMESTAMP,     
    card_type VARCHAR,     
    status VARCHAR,     
    last_modified TIMESTAMP   
) WITH (     
    'connectors' = '[{card_details_source_config}]'   
);   

CREATE MATERIALIZED VIEW invalid_card_transaction AS   
SELECT     
    t.cc_num,     
    t.ts AS event_time,     
    (cd.status != 'active') AS invalid_card   
FROM credit_card_transactions AS t   
LEFT ASOF JOIN card_details AS cd     
    MATCH_CONDITION (t.ts >= cd.last_modified)     
    ON t.cc_num = cd.cc_num   
``` 

Feldera includes support for `LEFT ASOF JOIN operations for point-in-time correct` joins (see Chapter 4). 
Felderaは「時点で正しい」結合のための`LEFT ASOF JOIN操作`をサポートしています（第4章を参照）。

You can also compose data transformations using nested views. 
ネストされたビューを使用してデータ変換を構成することもできます。

In the following code snippet, we define a materialized view that is computed from the `invalid_card_transaction view. 
次のコードスニペットでは、`invalid_card_transaction`ビューから計算されるマテリアライズドビューを定義します。

This derived feature counts the number of transactions that arrive from invalid cards in a one-day rolling aggregation: 
この派生機能は、無効なカードから到着するトランザクションの数を1日間のローリング集約でカウントします：

```  
CREATE MATERIALIZED VIEW invalid_card_transaction_count AS   
SELECT     
    cc_num,     
    SUM(CASE WHEN invalid_card THEN 1 ELSE 0 END)       
    OVER window_1_day AS invalid_1day   
FROM     
    invalid_card_transaction   
WINDOW     
    window_1_day AS (   
        PARTITION BY cc_num   
        ORDER BY event_time RANGE BETWEEN      
        INTERVAL '1' DAY PRECEDING AND CURRENT ROW     
    ); 
```  
```  
この派生機能は、無効なカードから到着するトランザクションの数を1日間のローリング集約でカウントします：

CREATE MATERIALIZED VIEW invalid_card_transaction_count AS   
SELECT     
    cc_num,     
    SUM(CASE WHEN invalid_card THEN 1 ELSE 0 END)       
    OVER window_1_day AS invalid_1day   
FROM     
    invalid_card_transaction   
WINDOW     
    window_1_day AS (   
        PARTITION BY cc_num   
        ORDER BY event_time RANGE BETWEEN      
        INTERVAL '1' DAY PRECEDING AND CURRENT ROW     
    ); 
``` 

These data transformations show you how to join and enrich the transaction events and compose transformations. 
これらのデータ変換は、トランザクションイベントを結合して強化し、変換を構成する方法を示しています。

Let’s look now at how we add joined features to the ``` cc_trans_aggs_fg feature group and define lagged features as transformations in ``` Feldera. 
次に、`cc_trans_aggs_fg`フィーチャーグループに結合された特徴を追加し、`Feldera`で遅延特徴を変換として定義する方法を見てみましょう。

###### Lagged Features and Feature Pipelines in Feldera
###### Felderaにおける遅延特徴とフィーチャーパイプライン

In the previous section, we presented the streaming data transformations that create the rolling aggregation features for the cc_trans_aggs_fg in Feldera. 
前のセクションでは、Felderaの`cc_trans_aggs_fg`のためのローリング集約機能を作成するストリーミングデータ変換を紹介しました。

We also need to add the following features for cc_trans_aggs_fg: 
また、`cc_trans_aggs_fg`に以下の特徴を追加する必要があります：

- account_id
- bank_id
- prev_ts_transaction
- prev_ip_transaction
- prev_card_present

We will add the account_id and bank_id features through a join transformation with ``` card_details. 
`card_details`との結合変換を通じて、account_idとbank_idの特徴を追加します。

Feldera provides a LAG operator that we can use to efficiently compute ``` lagged features as a stateful data transformation. 
Felderaは、状態を持つデータ変換として効率的に`lagged features`を計算するために使用できるLAG演算子を提供します。

First, we will create two intermediate materialized views, `cc_trans_card and` `lagged_trans, and then join them together` to produce the final features for our feature group, cc_trans_aggs_fg: 
まず、2つの中間マテリアライズドビュー`cc_trans_card`と`lagged_trans`を作成し、それらを結合してフィーチャーグループ`cc_trans_aggs_fg`の最終的な特徴を生成します：

```  
def build_last_tr_sql(transaction_src_config: str, fs_sink_config: str) -> str:     
    return f"""   
    --Point-in-time correct join of rolling_aggregates view with card_details table   
    CREATE MATERIALIZED VIEW cc_trans_card AS   
    SELECT     
        ra.*,     
        cd.account_id,     
        cd.bank_id   
    FROM rolling_aggregates AS ra   
    LEFT ASOF JOIN card_details AS cd     
        MATCH_CONDITION (ra.event_time >= cd.last_modified)     
        ON ra.cc_num = cd.cc_num   
    ;   
    -- Compute lagged features for transactions   
    CREATE LOCAL VIEW lagged_trans AS   
    SELECT     
        ctc.*,     
        LAG(event_time) OVER      
        (PARTITION BY cc_num ORDER BY event_time ASC) AS prev_ts_transaction,     
        LAG(ip_addr) OVER      
        (PARTITION BY cc_num ORDER BY event_time ASC) AS prev_ip_transaction,
```  
```  
最初に、2つの中間マテリアライズドビュー`cc_trans_card`と`lagged_trans`を作成し、それらを結合してフィーチャーグループ`cc_trans_aggs_fg`の最終的な特徴を生成します：

def build_last_tr_sql(transaction_src_config: str, fs_sink_config: str) -> str:     
    return f"""   
    --Point-in-time correct join of rolling_aggregates view with card_details table   
    CREATE MATERIALIZED VIEW cc_trans_card AS   
    SELECT     
        ra.*,     
        cd.account_id,     
        cd.bank_id   
    FROM rolling_aggregates AS ra   
    LEFT ASOF JOIN card_details AS cd     
        MATCH_CONDITION (ra.event_time >= cd.last_modified)     
        ON ra.cc_num = cd.cc_num   
    ;   
    -- Compute lagged features for transactions   
    CREATE LOCAL VIEW lagged_trans AS   
    SELECT     
        ctc.*,     
        LAG(event_time) OVER      
        (PARTITION BY cc_num ORDER BY event_time ASC) AS prev_ts_transaction,     
        LAG(ip_addr) OVER      
        (PARTITION BY cc_num ORDER BY event_time ASC) AS prev_ip_transaction,
``` 

```     
    LAG(card_present) OVER      (PARTITION BY cc_num ORDER BY event_time ASC) AS prev_card_present   
    FROM cc_trans_card AS ctc;   
    -- Write the final features to the feature group sink   
    CREATE VIEW cc_trans_aggs_fg   
    WITH (     
        'connectors' = '[{fs_sink_config}]'   
    )   
    AS     
    SELECT       
        cc_num,       
        event_time,       
        account_id,       
        bank_id,       
        sum_10min,       
        count_10min,       
        sum_1hour,       
        count_1hour,       
        sum_1day,       
        count_1day,       
        sum_7day,       
        count_7day,       
        prev_ts_transaction,       
        prev_ip_transaction,       
        prev_card_present     
    FROM lagged_trans;   
    """ 
```  
```     
    LAG(card_present) OVER      (PARTITION BY cc_num ORDER BY event_time ASC) AS prev_card_present   
    FROM cc_trans_card AS ctc;   
    -- Write the final features to the feature group sink   
    CREATE VIEW cc_trans_aggs_fg   
    WITH (     
        'connectors' = '[{fs_sink_config}]'   
    )   
    AS     
    SELECT       
        cc_num,       
        event_time,       
        account_id,       
        bank_id,       
        sum_10min,       
        count_10min,       
        sum_1hour,       
        count_1hour,       
        sum_1day,       
        count_1day,       
        sum_7day,       
        count_7day,       
        prev_ts_transaction,       
        prev_ip_transaction,       
        prev_card_present     
    FROM lagged_trans;   
    """ 
``` 

Select all columns explicitly instead of lagged_trans to prevent schema breaking changes if new columns are added to lagged_trans. 
新しい列が`lagged_trans`に追加された場合のスキーマ破損の変更を防ぐために、`lagged_trans`の代わりにすべての列を明示的に選択します。

We want these Feldera transformations to read from the transaction data source (an Apache Kafka topic) and to write to Hopsworks feature groups as a sink. 
これらのFeldera変換がトランザクションデータソース（Apache Kafkaトピック）から読み取り、Hopsworksフィーチャーグループに書き込むようにしたいと考えています。

For this, you need to define the input data sources and plug them together to run a Feldera pipeline, as follows: 
そのためには、入力データソースを定義し、それらを接続してFelderaパイプラインを実行する必要があります：

```  
transaction_src_config = # Apache Kafka Topic   
card_details_src_config = # card_details table in data mart   
fs_sink_config = # Hopsworks Feature Group output   
last_tr_sql = build_last_tr_sql(transaction_src_config, fs_sink_config)   
last_tr_pipeline = PipelineBuilder(client, name = \     
    "hopsworks_delta_kafka_last_tr", sql = last_tr_sql).create_or_replace()   
last_tr_pipeline.start() 
```  
```  
そのためには、入力データソースを定義し、それらを接続してFelderaパイプラインを実行する必要があります：

transaction_src_config = # Apache Kafka Topic   
card_details_src_config = # card_details table in data mart   
fs_sink_config = # Hopsworks Feature Group output   
last_tr_sql = build_last_tr_sql(transaction_src_config, fs_sink_config)   
last_tr_pipeline = PipelineBuilder(client, name = \     
    "hopsworks_delta_kafka_last_tr", sql = last_tr_sql).create_or_replace()   
last_tr_pipeline.start() 
``` 

The output of streaming feature pipelines are rows written to feature groups. 
ストリーミングフィーチャーパイプラインの出力は、フィーチャーグループに書き込まれる行です。

The feature groups should already exist before they are written to. 
フィーチャーグループは、書き込まれる前にすでに存在している必要があります。

You typically don’t create the feature groups in the streaming feature pipeline program. 
通常、ストリーミングフィーチャーパイプラインプログラム内でフィーチャーグループを作成することはありません。

Instead, it’s best practice to pre-create the feature groups in a separate program (or notebook) where you also explicitly define the schema for the feature groups, as shown in the following code: 
代わりに、フィーチャーグループのスキーマを明示的に定義する別のプログラム（またはノートブック）でフィーチャーグループを事前に作成することがベストプラクティスです。以下のコードに示すように：

```  
from hsfs.feature import Feature   
features = [     
    Feature(name="cc_num", type="string", online_type="varchar(16)"),     
    Feature(name="account_id", type="string"),     
    Feature(name="bank_id", type="string"),     
    Feature(name="event_time", type="TIMESTAMP"),     
    …   
]   
fg = fs.create_feature_group(name="cc_trans_aggs_fg",                  
    features=features,                  
    …)   
fg.save(features) 
```  
```  
フィーチャーグループのスキーマを明示的に定義する別のプログラム（またはノートブック）でフィーチャーグループを事前に作成することがベストプラクティスです。以下のコードに示すように：

from hsfs.feature import Feature   
features = [     
    Feature(name="cc_num", type="string", online_type="varchar(16)"),     
    Feature(name="account_id", type="string"),     
    Feature(name="bank_id", type="string"),     
    Feature(name="event_time", type="TIMESTAMP"),     
    …   
]   
fg = fs.create_feature_group(name="cc_trans_aggs_fg",                  
    features=features,                  
    …)   
fg.save(features) 
``` 

###### Summary and Exercises
###### まとめと演習

Streaming feature pipelines and ODTs enable real-time ML systems to react at human interactive timescales to nonverbal actions in applications or services. 
ストリーミングフィーチャーパイプラインとODTは、リアルタイムのMLシステムがアプリケーションやサービスにおける非言語的なアクションに対して人間のインタラクティブな時間スケールで反応できるようにします。

In this chapter, we showed how the computation of real-time features can be shifted right, by storing raw event data in the online feature store and then computing features on demand, by either computing them directly in online inference pipelines or pushing down SQL queries to the online feature store. 
この章では、リアルタイム機能の計算を右にシフトする方法を示しました。これは、生のイベントデータをオンラインフィーチャーストアに保存し、オンライン推論パイプラインで直接計算するか、SQLクエリをオンラインフィーチャーストアにプッシュダウンすることによって、オンデマンドで機能を計算することによって実現されます。

Most of the chapter, however, was concerned with shifting left real-time feature computation by precomputing features in streaming pipelines. 
しかし、章のほとんどは、ストリーミングパイプラインで機能を事前計算することによってリアルタイム機能計算を左にシフトすることに関心がありました。

We introduced the basic concepts in building streaming applications, including windowed aggregations and different types of windows. 
ウィンドウ集約やさまざまなタイプのウィンドウを含むストリーミングアプリケーションの構築における基本概念を紹介しました。

We introduced two different stream-processing engines for building streaming feature pipelines, Apache Flink and Feldera. 
ストリーミングフィーチャーパイプラインを構築するための2つの異なるストリーム処理エンジン、Apache FlinkとFelderaを紹介しました。

We also introduced different types of windows for aggregations, and we showed how incremental view maintenance enables scalable, fresh features for rolling aggregations. 
集約のためのさまざまなタイプのウィンドウも紹介し、インクリメンタルビューのメンテナンスがローリング集約のためのスケーラブルで新鮮な機能を可能にする方法を示しました。

We concluded with example SQL programs in Feldera that compute real-time features for our credit card fraud detection system. 
クレジットカード詐欺検出システムのためのリアルタイム機能を計算するFelderaの例SQLプログラムで締めくくりました。

Do the following exercises to help you learn how to design and write streaming feature pipelines: 
ストリーミングフィーチャーパイプラインを設計し、記述する方法を学ぶために、次の演習を行ってください：

- Write a function that transforms the `ip_addr in a transaction into a` _location_ feature. 
- トランザクション内の`ip_addr`を`_location_`フィーチャーに変換する関数を書いてください。

- Compute new features for a new location feature group, composed from the previously computed location feature. 
- 以前に計算されたロケーションフィーチャーから構成される新しいロケーションフィーチャーグループのための新しいフィーチャーを計算してください。

For example, compute a count of transaction activity in a time window, grouped by location. 
例えば、ロケーションごとにグループ化された時間ウィンドウ内のトランザクションアクティビティのカウントを計算してください。

- Write a custom data validation rule in Feldera and write any bad records to a sink feature group containing bad transaction data. 
- Felderaでカスタムデータ検証ルールを書き、悪いトランザクションデータを含むシンクフィーチャーグループに悪いレコードを書き込んでください。

- Add a merchant spend (count) feature over the last 5 minutes, 1 hour, 24 hours, and 7 days.  
- 過去5分、1時間、24時間、7日間のマーチャント支出（カウント）フィーチャーを追加してください。  



