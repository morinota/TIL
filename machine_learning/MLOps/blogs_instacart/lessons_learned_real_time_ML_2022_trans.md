## ref ref

<https://tech.instacart.com/lessons-learned-the-journey-to-real-time-machine-learning-at-instacart-942f3a656af3>
<https://tech.instacart.com/lessons-learned-the-journey-to-real-time-machine-learning-at-instacart-942f3a656af3>

# Lessons Learned: The Journey to Real-Time Machine Learning at Instacart インスタカートにおけるリアルタイム機械学習への旅

Instacart incorporates machine learning extensively to improve the quality of experience for all actors in our “four-sided marketplace” — customers who place orders on Instacart apps to get deliveries in as fast as 30 minutes, shoppers who can go online at anytime to fulfill customer orders, retailers that sell their products and can make updates to their catalog in real time, and the brand partners that participate in auctions on the Instacart Advertising platform to promote their products.
Instacartは、Instacartアプリで注文して最短30分で配達を受ける顧客、いつでもオンラインで顧客の注文に対応できる買い物客、商品を販売してリアルタイムでカタログを更新できる小売業者、Instacart Advertisingプラットフォームでオークションに参加して商品を宣伝するブランド・パートナーなど、「四面市場」のすべての関係者の体験の質を向上させるために、機械学習を広範囲に取り入れている。

![Figure 1: How ML models support shopping journey at Instacart]()

Figure 1 depicts a typical shopping journey at Instacart, powered by hundreds of machine learning models.
図1は、何百もの機械学習モデルによるInstacartの典型的なショッピング・ジャーニーを示している。
All of these actions happen in real time, which means leveraging machine learning in real-time can provide significant value to the business.
**これらのすべてのアクション(ユーザ目線では...!)はリアルタイムで行われるため、リアルタイムで機械学習を活用することはビジネスに大きな価値を提供できる**。
One of the major changes we have gone through is transitioning many of our batch-oriented ML systems into real-time.
私たちが経験した大きな変化のひとつは、**バッチ指向のMLシステムの多くをリアルタイムに移行したこと**です。
In this post, we describe our transition process, review main challenges and decisions, and draw important lessons that could help others learn from our experience.
この投稿では、私たちの移行プロセスを説明し、主な課題と決定を振り返り、他の人々が私たちの経験から学ぶのに役立つ重要な教訓をまとめます。

## History of Batch-Oriented ML Systems バッチ指向MLシステムの歴史

Most machine learning in production is about leveraging signals (features) derived from raw data to predict targeted goals (labels).
生産現場における機械学習のほとんどは、生データから得られたシグナル（特徴）を活用して、目標とするゴール（ラベル）を予測することである。
The quality of features is crucial and the features are largely categorized into two types by freshness:
特徴の品質は重要であり、特徴は鮮度によって大きく2つのタイプに分類される：

- **Batch features**: Features extracted from historical data, often through batch processing.
  - **バッチ特徴： 過去のデータからバッチ処理で抽出された特徴**。
  - These types of features usually change infrequently, such as category or nutrition information of a food product.
  - この種の特徴量は、食品のカテゴリーや栄養情報のように、**通常は頻繁に変更されるものではない**。(ふむふむ確かに...!:thinking_face:)

- **Real-time features**: Features extracted from real-time data, often through stream processing.
  - リアルタイム特徴量： リアルタイムのデータから、ストリーム処理によって抽出された特徴量。
  - These types of features usually change frequently and the changes are essential for model prediction and decision-making.
    - **この種の特徴は通常頻繁に変化し**、その変化はモデルの予測や意思決定に不可欠である。
  - Some examples are real-time item availability, supply (number of online shoppers) and demand (number of orders), and customers real-time shopping sessions.
    - 例えば、リアルタイムの商品在庫状況、供給(オンラインショッピング利用者数)と需要(注文数)、顧客のリアルタイムのショッピングセッションなどである。

It is a natural choice for relatively small companies to start with batch-oriented ML systems since the progress can be bootstrapped by existing batch-oriented infrastructures.
**比較的小規模な企業がバッチ指向のMLシステムから始めるのは自然な選択である。なぜなら、既存のバッチ指向のインフラストラクチャによって開発を容易に進められるから**だ。(うんうん...!:thinking:)
While some of our logistics systems were using real-time predictions using mostly transactional data and some event-driven feature computation, it was not easy to generate features and was not widely adopted across the company.
私たちの物流システムの中には、主にトランザクションデータと一部のイベント駆動型特徴量計算を使用してリアルタイム予測を行っているものもありましたが、**特徴量を生成することは簡単ではなく、会社全体で広く採用されていませんでした**。
Most other ML systems at Instacart started with batched-oriented systems with two main characteristics: 1) ML models only had access to batch features; 2) these models generated predictions offline in batches and consumed those predictions either offline for analytics, or online using a lookup table.
**Instacartの他のほとんどのMLシステムは、2つの主な特徴を持つバッチ指向システムから始まった**： 1)MLモデルはバッチ特徴量にしかアクセスしなかった； 2)これらのモデルはバッチでオフラインで予測を生成し、その予測をオフラインで分析用に消費するか、ルックアップテーブルを使用してオンラインで消費していた。
(わかる〜...!:thinking_face:)
Machine learning engineers could simply write the model outputs to database tables and applications could read them in production without the need for any complicated infrastructure.
**機械学習エンジニアは、モデルの出力をデータベースのテーブルに書き込むだけで、アプリケーションは複雑なインフラを必要とせずに、本番環境でそれを読み取ることができる**。
However, we experienced several limitations in these batch-oriented ML systems:
しかし、これらのバッチ指向のMLシステムにはいくつかの限界があった:

- 1. Stale Predictions: Precomputed prediction offers an inferior experience in many applications since they only generate stale responses to requests that happened in the past.
  - 陳腐な予測： 事前に計算された予測は、過去に発生したリクエストに対してのみ陳腐な応答を生成するため、多くのアプリケーションで劣った体験を提供する。
  - For example, batch prediction only allowed us to classify historical queries but performed poorly on new queries.
  - 例えば、バッチ予測は過去のクエリーを分類することができたが、新しいクエリーに対してはうまく機能しなかった。

- 2. Inefficient Resource Usage: It is a waste of resources to generate predictions daily for all customers since many customers are not active every day.
  - **非効率的なリソース使用： 多くの顧客は毎日アクティブではないため、すべての顧客の予測を毎日生成するのはリソースの無駄**です。

- 3. Limited Coverage: This system provides limited coverage.
  - 限られた範囲： このシステムは限られた範囲をカバーする。
  - For instance, it’s not possible to cache predictions for all user-item pairs due to large cardinality and we have to truncate the pairs in the long-tail.
  - 例えば、**カーディナリティが大きいため、すべてのユーザーとアイテムのペアの予測をキャッシュすることは不可能であり、ロングテールのペアを切り捨てる必要がある**。

- 4. Response Lag: Models are less responsive to recent changes since real-time features, such as customers’ intents in the current shopping session and real-time product availability, are not accessible to the model.
  - レスポンスの遅れ： 現在のショッピングセッションにおける顧客の意図や、リアルタイムの商品在庫状況などのリアルタイムの機能は、モデルにはアクセスできないため、モデルは最近の変化に対する反応が鈍い。

- 5. Suboptimal: Data freshness impacts the quality of model output.
  - 最適化されていない： **データの鮮度がモデルの出力の品質に影響を与える**。
  - Without the up-to-date signals (such as supply and demand), the fulfillment process can be suboptimal since models do not have access to real-time changes and the lag in decision-making can lead to inefficient resource allocation.
  - 最新のシグナル（需給など）がなければ、モデルはリアルタイムの変化にアクセスできず、意思決定の遅れが非効率的な資源配分につながるため、フルフィルメント・プロセスは最適化されない可能性がある。

(上記の記述は、バッチ特徴量を使ったオンライン推論ならで達成できることと、オンライン特徴量を使ったオンライン推論なら達成できること、の両方がありそう...!:thinking_face:)

As we introduce product innovations in the Instacart app to improve personalization, inspiration, capturing and serving dynamic features in real time becomes essential.
パーソナライゼーションを向上させるためにInstacartアプリに製品イノベーションを導入する際、インスピレーション、リアルタイムでの動的特徴量のキャプチャと提供が不可欠になります。
This requires transitioning most of the ML services at Instacart from batch-oriented to real-time systems.
**そのためには、インスタカートのMLサービスのほとんどをバッチ指向からリアルタイム・システムに移行する必要がある**。
Among other things, we have gone through the following major transitions to enable real-time ML:
とりわけ、リアルタイムMLを実現するために、私たちは以下のような**2つの大きな変遷**を経てきた：

- **Real-Time Serving**: From serving precomputed predictions to real-time serving in order to reduce staleness, limited coverage, and resource underutilization.
リアルタイム配信： 事前に計算された予測をリアルタイムに提供することで、陳腐化、カバレッジの制限、リソースの過少利用を削減する。

- **Real-Time Features**: From batch features to real-time features to ensure data freshness, and enable models to respond to up-to-date changes.
リアルタイム特徴量： データの鮮度を確保し、モデルが最新の変更に対応できるようにするために、バッチ特徴量からリアルタイム特徴量への移行。

## Transition 1: From serving precomputed predictions to real-time serving Transition 1： 事前に計算された予測値の提供からリアルタイムの提供へ

![figure3]()

Transitioning to a real-time serving system has been made possible by two products: Feature Store and Online Inference Platform.
**リアルタイム・サービング・システムへの移行は、2つのプロダクトによって可能になった： フィーチャーストアとオンライン推論プラットフォームである**。(feature store出てきた!)
Feature Store is a key-value store for fast feature retrieval and Online Inference Platform is a system that hosts each model as an RPC (Remote Procedure Call) endpoint.
Feature Storeは高速な特徴量検索のためのKey-Valueストアであり、**Online Inference Platformは各モデルをRPC（Remote Procedure Call）エンドポイントとしてホストするシステム**である。

- (memo) RPC (Remote Procedure Call)って?
  - 分散システムにおいて、**ネットワーク上の別のコンピュータ上で実行される手続き(プログラム)を、あたかもローカルコンピュータ上で実行されているかのように呼び出す**ことができる仕組み。
    - 異なるコンピュータ間で手続き(関数やメソッド)を呼び出す、みたいなイメージ??:thinking_face:
  - RESTfulなWeb APIとの違い:
    - RESTfulなWeb APIのエンドポイントはリソース指向。**各endpointは、特定のリソース & リソースに対する操作(ex. GET, POST, PUT, DELETE,etc.)を表現**する。
    - RPCエンドポイントは、手続きやメソッドの呼び出しをリモートで行う事を前提に設計されている。そのため、関数名やメソッド名がそのままリクエストに使用される。**関数呼び出しに近い形式での利用が想定**されてる。

Real-Time Serving improved machine learning applications by integrating new features such as personalization, optimized computation resources by eliminating execution of unused predictions, and increased conversions by optimizing long-tail queries.
Real-Time Servingは、パーソナライゼーションなどの新機能を統合することで機械学習アプリケーションを改善し、**未使用の予測の実行を排除することで計算リソースを最適化**し、ロングテールのクエリを最適化することでコンバージョンを増加させた。
Most importantly, it also provided better customer experience because it incorporated personalized results and improved results for new users/queries.
最も重要なことは、**パーソナライズされた結果を組み込み、新規ユーザやクエリに対する結果を改善することで、より良い顧客体験を提供した事**である。

Even though the transition was a significant win for machine learning applications, introducing real-time serving introduced many technical challenges.
この移行は機械学習アプリケーションにとって大きな勝利であったが、リアルタイム・サービスの導入には多くの技術的な課題が生じた。

<!-- ここまで読んだ! -->

### Challenges of Moving to Real-Time Serving リアルタイム・サービスへの移行の課題

- **Latency**: Latency plays an important role in the user experience; no one likes to wait to see search results loading while shopping.
待ち時間： 待ち時間はユーザー体験において重要な役割を果たす。ショッピング中に検索結果がロードされるのを待つのが好きな人はいない。
A real-time serving system introduces dependencies on feature retrieval, feature engineering, and model prediction and makes it essential that those processes are fast and can be accessed with a tight latency budget.
リアルタイム・サービング・システムでは、特徴検索、特徴エンジニアリング、モデル予測に依存関係が生じ、これらのプロセスが高速で、厳しいレイテンシ・バジェットでアクセスできることが不可欠となる。

- **Availability**: The real-time inference system introduces a failure point that can cause downtime in the backend service.
可用性： **リアルタイム推論システムは、バックエンド・サービスにダウンタイムを引き起こす可能性のある障害点を導入**する。(なるほど、障害点...!:thinking_face:)
Ensuring high availability of the model services necessitates better monitoring, error handling, and deployment practices.
モデル・サービスの高い可用性を確保するには、モニタリング、エラー処理、デプロイメントを改善する必要がある。

- **Steep Learning Curve**: The system involves understanding many new components and processes.
急な学習曲線(=エンジニアにとっての学習負荷、みたいな...!:thinking:)： このシステムは、多くの新しいコンポーネントやプロセスを理解する必要がある。
It was mainly challenging for machine learning engineers because it changed the development process and introduced many new tools.
**開発プロセスが変わり、多くの新しいツールが導入されたため、主に機械学習エンジニアにとってチャレンジングなものだった**。

<!-- ここまで読んだ! -->

### Key Decisions 重要な決定

- **Unified Interface**: Developing a unified interface, Griffin, enabled us to integrate best practices such as unit tests, integration tests, and canary deployments.
統一インターフェース： 統一インターフェースGriffinを開発することで、ユニットテスト、統合テスト、カナリアデプロイメントなどのベストプラクティスを統合することができた。
It also reduced the learning curve for machine learning engineers by providing standard workflow templates, and tools for fast troubleshooting.
また、**標準的なワークフローテンプレートや、迅速なトラブルシューティングのためのツールを提供することで、機械学習エンジニアの学習曲線を短縮した**。
Additionally, creating a single entrypoint to our system allowed us to standardize monitoring, observability, and other processes required for reliability.
さらに、**システムへのエントリーポイントをひとつにした**ことで、モニタリングや観測可能性など、信頼性に必要なプロセスを標準化することができた。

- Generalized Service Format: We chose an RPC framework that was widely used at Instacart for inter-service communications.
一般化されたサービス・フォーマット： **Instacartでサービス間通信に広く使われているRPCフレームワークを選択**した。
Reusing existing tools allowed us to quickly develop a production-grade platform and support communication between multiple languages such as Ruby, Scala, Python, and Go.
既存のツールを再利用することで、プロダクショングレードのプラットフォームを迅速に開発し、Ruby、Scala、Python、Goなどの複数の言語間の通信をサポートすることができた。
Furthermore, it allowed machine learning engineers to share knowledge between groups and grow faster with collaboration.
さらに、機械学習エンジニアがグループ間で知識を共有し、協力して成長することができるようになった。

<!-- ここまで読んだ! -->

## Transition 2: From batch features to real-time features Transition 2： バッチ特徴量からリアルタイム特徴量へ

![figure4]()

The transition to real-time serving has improved the user experience by eliminating the staleness and limited coverage of the precomputed predictions.
**real-timeサービングへの移行により、事前計算された予測の陳腐さとカバレッジの制限がなくなり、ユーザ体験が向上した**。
However, all predictions are still based on batch features.
**しかし、すべての予測は依然としてバッチ特徴量に基づいている**。
The best experience in a shopping journey requires both batch features and real-time features.
**ショッピング・ジャーニーにおける最高の体験には、バッチ特徴量とリアルタイム特徴量の両方が必要**だ。(うんうん...!:thinking_face:)

To enable real-time features, we developed a real-time processing pipeline with streaming technologies as shown in Figure 4.
リアルタイム機能を実現するために、図4に示すような**ストリーミング技術を用いたリアルタイム処理パイプライン**を開発した。
The pipeline listens to raw events stored in Kafka published by services, transforms them into desired features using Flink, and sinks them into Feature Store for on-demand access.
パイプラインは、サービスによって公開されたKafkaに保存された生のイベントをリッスンし、Flinkを使用してそれらを望ましい特徴量に変換し、Feature Storeに同期してオンデマンドでアクセスできるようにする。
Although streaming is a relatively mature technology, there are still quite a few challenges we faced in the transition.
ストリーミングは比較的成熟した技術ですが、移行にあたって直面した課題はまだたくさんあります。

### Challenges 課題

#### Siloed streaming technologies in different organizations: 組織ごとにサイロ化されたストリーミング技術

The need for stream processing at different teams vary from simple notifications to analytics.
Therefore, each organization had adopted the tools that fit its respective needs and we ended up with three different streaming tools.
**単純な通知から分析まで、チームによってストリーム処理の必要性は異なる。そのため、各組織はそれぞれのニーズに合ったツールを採用し、結局、3つの異なるストリーミング・ツールが存在することになった。** (なるほど...! 非常に納得感のある言語化...!:thinking_face:)
This works fine locally within each organization, but it is challenging for machine learning since it requires events built across different organizations.
これは各組織(チームと言ってもいい?)内では問題なく機能するが、**機械学習にとっては異なる組織間で構築されたイベントが必要であるため、課題となる**。

#### Event consistency and quality イベントの一貫性と質

Events have been mostly consumed/managed by local teams for their specific needs.
イベントは、そのほとんどがローカルチームによって、それぞれのニーズに合わせて消費／管理されてきた。
This brings two challenges when consolidating events to generate real-time features: 1) it is not clear what events are available; and 2) event quality is not guaranteed.
このため、イベントを統合してリアルタイム特徴量を生成する場合、2つの課題が生じる： 1）どのようなイベントが利用可能であるかが明確でない、2）イベントの品質が保証されていない。

#### Complex pipeline with new development process 新しい開発プロセスを伴う複雑なパイプライン

As shown in Figure 4, the real-time features pipeline introduces a new tech stack.
図4に示すように、**リアルタイム特徴量パイプラインは新しい技術スタックを導入している**。
It starts from raw events published by services, goes through stream processing and Feature Store, and responds to user requests in real-time.
**サービスによって公開された生のイベントから始まり(pub/subモデルだ...!:thinking_face:)、ストリーム処理とフィーチャーストアを経て、ユーザのリクエストにリアルタイムで応答する**。

The challenges with this are twofold.s
これには2つの課題がある。
On the one hand, real-time features (streaming in general) are not common knowledge for machine learning engineers and data scientists.
**まず一方、リアルタイム特徴量（一般的にストリーミング）は、機械学習エンジニアやデータサイエンティストにとっては一般的な知識ではない**。(うんうん...!:thinking_face:)
On the other hand, it is more involved to set up a development environment for streaming processing.
もう一方、ストリーミング処理の開発環境を設定するのはより複雑である。
The fact that data streaming technologies work best in JVM (Java and Scala) with suboptimal support in Python also makes the learning curve steeper.
データ・ストリーミング技術はJVM（JavaとScala）で最も効果的に動作するが、Pythonではサポートが最適でないという事実も、学習曲線を急峻にしている。

### Key Decisions 重要な決定事項

#### Centralized event storage イベントの一元管理

Given the challenging situation that there exist multiple streaming backends in different organizations, we chose Kafka as a centralized storage to put all raw events together so that we can derive ML features from them in consistent format.
異なる組織に複数のストリーミングバックエンドが存在するという困難な状況を考慮して、**すべての生のイベントを一元的に保存するためにKafkaを中央ストレージとして選択し、一貫したフォーマットでML特徴量を導出する**ことができるようにした。

- (memo) Kafkaについて
  - Apache Kafkaは、ストリーミングデータをリアルタイムで取り込んで処理するために最適化された分散データストア。
    - 参考: [Apache Kafkaとは？](https://www.ibm.com/cloud/learn/apache-kafka)
  - Kafkaは、キューイングとパブリッシュ/サブスクライブという 2 つのメッセージングモデルを組み合わせて、大量のデータをリアルタイムで処理するためのプラットフォームを提供する。

This introduces some extra latency to the pipeline (usually within a few 100ms) and uses some more resources, but the benefits outweigh these shortcomings.
これは、**パイプラインに余分なレイテンシーをもたらし（通常は数100ms以内）、より多くのリソースを使用するが、利点はこれらの欠点を上回る**。
First, centralized storage scales quickly and avoids building multiple interfaces between real-time ML systems and different streaming tools.
第一に、一元化されたストレージは素早くスケールし、**リアルタイムMLシステムと異なるストリーミングツールとの間に複数のインターフェースを構築する必要がない**。(ここで"リアルタイムMLシステム"の入り口は、多分feature storeのこと:thinking_face:)
Second, this does not impact the existing event usage pattern, and centralized event storage makes it easy to integrate schema validation and data quality checks to improve the events quality.
第二に、 既存のイベント使用パターンに影響を与えず、**一元化されたイベントストレージは、スキーマ検証とデータ品質チェックを統合**し、イベントの品質を向上させるために簡単に行うことができる。

#### Separate event storage and computation イベントの保存と計算を分離

We also made the choice to have separate event storage and event computation.
また、イベントの保存と計算を別々にすることも選択した。
On the one hand, this modularizes the system by following the design principle of separation of concerns and adopts the best tools for the work.
一方で、**関心の分離の設計原則に従い、システムをモジュール化し、各作業に最適なツールを採用**する。
On the other hand, it provides a ground truth reference for all events in a single, durable storage with consistent format and configurable retention period.
もう一方で、一貫したフォーマットと設定可能な保持期間を持つ単一の耐久性のあるストレージにすべてのイベントの基本的な参照を提供する。
This makes data audit and compliance review easier, and supports event replay within the retention period when needed.
これにより、データ監査とコンプライアンス・レビューが容易になり、必要に応じて保持期間内でのイベントの再生をサポートする。

#### Form cross-functional working groups early: 早期に機能横断的なワーキンググループを結成

Since real-time features (or real-time ML initiatives in general) are a highly cross-functional effort, early on in the process, we formed a working group among different teams with experts in product/business development, streaming technologies, and ML development.
**リアルタイム特徴量（または一般的にリアルタイムMLイニシアチブ）は、非常に機能横断的な取り組みである**ため、**プロダクト／ビジネス開発、ストリーミング技術、ML開発の専門家を含む異なるチーム間でワーキンググループを早期に結成**した。(これはめっちゃ大事かも...! 自分一人で全てをやろうとするのではなく...!:thinking_face:)
This group is critical for us to discuss and reach decisions that address our existing challenges in enabling real-time ML.
このグループは、リアルタイムMLを実現する上での既存の課題を解決するための議論や決定を下すために不可欠な存在だ。

It also helps us to debate and evaluate early use cases for real-time ML.
また、**リアルタイムMLの初期のユースケースを議論し、評価するのにも役立つ**。(?)
For instance, thanks to the collective views of the working group, we prioritize the real-time item availability as the first use case since it is not only an essential model by itself, but also provides fundamental item availability scores that improve item found rate and customer experience, increases ETA prediction accuracy, and improves many services that require up-to-date item availability information.
例えば、ワーキンググループの総意により、我々は、リアルタイムの商品在庫状況を最初のユースケースとして優先しました。なぜなら、それ自体が不可欠なモデルであるだけでなく、商品発見率と顧客体験を向上させる基本的な商品在庫状況スコアを提供し、ETA予測精度を高め、**最新の商品在庫状況情報を必要とする多くのサービスを改善するから**です。(**つまり、そのusecaseが、最もいろんなサービスで利用できるusecaseだったから...?? 開発の順番を考える上で、この考え方は大事かも**...!:thinking_face:)
The success of this fundamental use case has enabled rapid adoption of real-time ML thereafter.
この基本的なユースケースの成功が、その後のリアルタイムMLの急速な普及を可能にした。

<!-- ここまで読んだ! -->

## Retrospection ♪回顧

![figure5]()

With two critical transitions and other improvements, we have created an ML platform with real-time serving and real-time features as illustrated in Figure 5.
この2つの重要な変遷とその他の改善により、図5に示すように、リアルタイム・サービングとリアルタイム特徴量を備えたMLプラットフォームを作成しました。
The platform transforms the shopping journey to be more dynamic and efficient, with better personalization and optimized fulfillment.
このプラットフォームは、より良いパーソナライゼーションと最適化されたfulfillment(=満足)を備え、ショッピングジャーニー (=ショッピングのユーザ体験??)をよりダイナミックで効率的なものに変えています。
Here are some highlights of the applications launched on the platform:
以下は、このプラットフォームで発表されたアプリケーションのハイライトである：

- Real-time item availability updates item availability scores in seconds from a couple of hours.
リアルタイムの商品在庫状況は、数時間から数秒で商品在庫状況のスコアを更新します。
This directly improves item found rate, reduces bad orders, and ultimately increases customer satisfaction.
これは、商品の発見率を直接改善し、不良注文を減らし、最終的に顧客満足度を高める。

- Session-based recommendation and personalization models make predictions within the shopping session in real-time.
**セッションベースの**レコメンデーションとパーソナライゼーションモデルは、リアルタイムでショッピングセッション内の予測を行う。
For instance, by removing items that wouldn’t be of interest to the customer based on their choices in the recent session, we have already made the Instacart storefront more fresh and dynamic with real-time user impression data.
例えば、最近のセッションでの顧客の選択に基づいて、顧客が興味を示さないような商品を削除することで、Instacartのストアフロントをリアルタイムのユーザーの印象データによって、より新鮮でダイナミックなものにしています。

- Fraud detection algorithms catch suspicious behaviors in real time and make it possible to prevent fraudulent activities before a loss occurs.
不正検知アルゴリズムは、疑わしい行動をリアルタイムでキャッチし、損失が発生する前に不正行為を防止することを可能にする。
This alone directly reduces millions of fraud-related costs annually.
これだけで、年間数百万ドルの不正関連コストを直接削減できる。

Overall, the real-time ML platform flows terabytes of event data per day, generates features with latency in the order of seconds contrast to hours before, and serves hundreds of models in real time.
全体として、リアルタイムMLプラットフォームは、1日あたりテラバイト単位のイベントデータを流し、数時間前と比較して数秒のレイテンシで特徴量を生成し、数百のモデルをリアルタイムで提供しています。
The platform resolves the limitations of batch-oriented systems to help related ML applications go real time, and also unleashes ML applications to make more business impact.
**このプラットフォームは、バッチ指向のシステムの制限を解決し、関連するMLアプリケーションのリアルタイム化を支援するとともに、MLアプリケーションを解放して、より多くのビジネスインパクトをもたらす。**
Over the last year, the platform has enabled considerable GTV (gross transaction value) growth in a series of A/B experiments.
**昨年、このプラットフォームは、一連のA/B実験においてGTV（総取引額）の大幅な伸びを実現した**。

<!-- ここまで読んだ! -->

## Lessons Learned Lessons Learned

### Infrastructure plays a critical role in real-time ML: リアルタイムMLではインフラが重要な役割を果たす

Transitioning into a real-time system required a major investment in infrastructure tools and processes in order to achieve better observability, efficient computation, high availability, and reliable deployment.
リアルタイム・システムに移行するためには、より優れた観測可能性、効率的な計算、高可用性、信頼性の高い配備を実現するために、インフラストラクチャー・ツールやプロセスに大きな投資が必要だった。
We used many tools and processes for real-time serving and real-time features which allowed us to productionize the platform quickly and show an impact at Instacart.
私たちは、リアルタイム配信とリアルタイム特徴量のために多くのツールとプロセスを使用し、プラットフォームを迅速にプロダクション化し、Instacartでの影響を示すことができた。
Using a unified interface that allows a diverse set of tools was essential in our success.
**多様なツールを許容する統一インターフェースを使用することが、私たちの成功に不可欠だった**。

### Make incremental progress 少しずつ前進する

Going from a batch-oriented ML system to real-time ML platform is a big step.
バッチ指向のMLシステムからリアルタイムMLプラットフォームへの移行は大きな一歩だ。
To make it more manageable, we carried out the transition in two distinct phases as detailed above.
より管理しやすくするため、私たちは上記のように**2段階に分けて移行を行った**。
We also identified at least one impactful use case to start with for each transition.
また、各トランジションについて、少なくとも1つのインパクトのあるユースケースを特定した。
As a result, in each transition phase, we have a clear goal and the incremental impact can be easily measured.
その結果、各移行段階において明確な目標が設定され、段階的なインパクトを簡単に測定できるようになった。
This not only enabled a more gradual platform update but also reduced the learning curve for machine learning engineers who adopted the platform.
これにより、より緩やかなプラットフォームのアップデートが可能になっただけでなく、このプラットフォームを採用した機械学習エンジニアの学習曲線も短縮された。

### Generalized and specialized solutions 一般的なソリューションと専門的なソリューション

(この教訓はまだよくわかってない...!:thinking_face:)

We adopted a generalized solution that helped us cover the majority of the cases with excellent support.
私たちは汎用的なソリューションを採用し、優れたサポートで大半のケースをカバーすることができた。
To accelerate the development, we then started building more specialized products such as an Embedding Platform to focus on more targeted circumstances and reduce the support requests.
開発を加速するために、より専門的なプロダクトを構築し始め、よりターゲットとなる状況に焦点を当て、サポートリクエストを減らした。例えば、Embedding Platformなど。
This balance between generalization and specialization improves the productivity for those specialized use cases, and achieves high reliability in the overall system.
この一般化と専門化のバランスは、特定のユースケースにおける生産性を向上させ、全体的なシステムの信頼性を高める。

### Grow infrastructures with products プロダクトとともにインフラストラクチャを成長させる

Machine learning engineers who adopted our platform during early development played a significant role in improving the quality by providing feedback and in growing the adoption by marketing the platform to other product teams at Instacart.
開発初期に私たちのプラットフォームを採用した機械学習エンジニアは、フィードバックを提供することで品質を向上させ、Instacartの他の製品チームにプラットフォームをマーケティングすることで採用を促進するという重要な役割を果たした。

<!-- ここまで読んだ! -->
