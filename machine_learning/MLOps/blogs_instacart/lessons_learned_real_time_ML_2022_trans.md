## ref ref

https://tech.instacart.com/lessons-learned-the-journey-to-real-time-machine-learning-at-instacart-942f3a656af3
https://tech.instacart.com/lessons-learned-the-journey-to-real-time-machine-learning-at-instacart-942f3a656af3

# Lessons Learned: The Journey to Real-Time Machine Learning at Instacart インスタカートにおけるリアルタイム機械学習への旅

Instacart incorporates machine learning extensively to improve the quality of experience for all actors in our “four-sided marketplace” — customers who place orders on Instacart apps to get deliveries in as fast as 30 minutes, shoppers who can go online at anytime to fulfill customer orders, retailers that sell their products and can make updates to their catalog in real time, and the brand partners that participate in auctions on the Instacart Advertising platform to promote their products.
Instacartは、Instacartアプリで注文して最短30分で配達を受ける顧客、いつでもオンラインで顧客の注文に対応できる買い物客、商品を販売してリアルタイムでカタログを更新できる小売業者、Instacart Advertisingプラットフォームでオークションに参加して商品を宣伝するブランド・パートナーなど、「四面市場」のすべての関係者の体験の質を向上させるために、機械学習を広範囲に取り入れている。

Figure 1 depicts a typical shopping journey at Instacart, powered by hundreds of machine learning models.
図1は、何百もの機械学習モデルによるInstacartの典型的なショッピング・ジャーニーを示している。
All of these actions happen in real time, which means leveraging machine learning in real-time can provide significant value to the business.
[empty]
One of the major changes we have gone through is transitioning many of our batch-oriented ML systems into real-time.
私たちが経験した大きな変化のひとつは、バッチ指向のMLシステムの多くをリアルタイムに移行したことです。
In this post, we describe our transition process, review main challenges and decisions, and draw important lessons that could help others learn from our experience.
この投稿では、私たちの移籍プロセスについて説明し、主な課題と決断を検証し、他の人々が私たちの経験から学ぶのに役立つ重要な教訓を導き出す。

## History of Batch-Oriented ML Systems バッチ指向MLシステムの歴史

Most machine learning in production is about leveraging signals (features) derived from raw data to predict targeted goals (labels).
生産現場における機械学習のほとんどは、生データから得られたシグナル（特徴）を活用して、目標とするゴール（ラベル）を予測することである。
The quality of features is crucial and the features are largely categorized into two types by freshness:
特徴の質は非常に重要で、特徴は鮮度によって大きく2種類に分類される：

Batch features: Features extracted from historical data, often through batch processing.
バッチ特徴： 過去のデータからバッチ処理で抽出された特徴。
These types of features usually change infrequently, such as category or nutrition information of a food product.
この種の機能は、食品のカテゴリーや栄養情報のように、通常は頻繁に変更されるものではない。

Real-time features: Features extracted from real-time data, often through stream processing.
リアルタイムの特徴： リアルタイムのデータから、ストリーム処理によって抽出された特徴。
These types of features usually change frequently and the changes are essential for model prediction and decision-making.
この種の特徴は通常頻繁に変化し、その変化はモデルの予測や意思決定に不可欠である。
Some examples are real-time item availability, supply (number of online shoppers) and demand (number of orders), and customers real-time shopping sessions.
例えば、リアルタイムの商品在庫状況、供給（オンラインショッピング利用者数）と需要（注文数）、顧客のリアルタイムのショッピングセッションなどである。

It is a natural choice for relatively small companies to start with batch-oriented ML systems since the progress can be bootstrapped by existing batch-oriented infrastructures.
比較的小規模な企業がバッチ指向のMLシステムから始めるのは自然な選択である。なぜなら、既存のバッチ指向のインフラによって進歩をブートストラップできるからである。
While some of our logistics systems were using real-time predictions using mostly transactional data and some event-driven feature computation, it was not easy to generate features and was not widely adopted across the company.
私たちの物流システムの中には、主にトランザクション・データとイベント・ドリブンの特徴量計算を使ったリアルタイム予測を使っているものもありましたが、特徴量を生成するのは簡単ではなく、全社的に広く採用されるには至っていませんでした。
Most other ML systems at Instacart started with batched-oriented systems with two main characteristics: 1) ML models only had access to batch features; 2) these models generated predictions offline in batches and consumed those predictions either offline for analytics, or online using a lookup table.
Instacartの他のほとんどのMLシステムは、2つの主な特徴を持つバッチ指向システムから始まった： 1)MLモデルはバッチの特徴にしかアクセスできなかった。2)これらのモデルはオフラインでバッチで予測を生成し、分析のためにオフラインで、またはルックアップテーブルを使用してオンラインでそれらの予測を消費した。
Machine learning engineers could simply write the model outputs to database tables and applications could read them in production without the need for any complicated infrastructure.
機械学習エンジニアは、モデルの出力をデータベースのテーブルに書き込むだけで、アプリケーションは複雑なインフラを必要とせずに、本番環境でそれを読み取ることができる。
However, we experienced several limitations in these batch-oriented ML systems:
しかし、これらのバッチ指向のMLシステムにはいくつかの限界があった：

Stale Predictions: Precomputed prediction offers an inferior experience in many applications since they only generate stale responses to requests that happened in the past.
陳腐な予測： 事前に計算された予測は、過去に起こったリクエストに対する古いレスポンスを生成するだけなので、多くのアプリケーションで劣った経験を提供する。
For example, batch prediction only allowed us to classify historical queries but performed poorly on new queries.
例えば、バッチ予測は過去のクエリーを分類することができたが、新しいクエリーに対してはうまく機能しなかった。

Inefficient Resource Usage: It is a waste of resources to generate predictions daily for all customers since many customers are not active every day.
非効率的なリソース使用： 多くの顧客は毎日アクティブではないため、すべての顧客の予測を毎日生成するのはリソースの無駄です。

Limited Coverage: This system provides limited coverage.
限られた範囲： このシステムは限られた範囲をカバーする。
For instance, it’s not possible to cache predictions for all user-item pairs due to large cardinality and we have to truncate the pairs in the long-tail.
例えば、カーディナリティが大きいため、すべてのユーザーとアイテムのペアの予測をキャッシュすることは不可能であり、ロングテールのペアを切り捨てる必要がある。

Response Lag: Models are less responsive to recent changes since real-time features, such as customers’ intents in the current shopping session and real-time product availability, are not accessible to the model.
レスポンスの遅れ： 現在のショッピングセッションにおける顧客の意図や、リアルタイムの商品在庫状況などのリアルタイムの機能は、モデルにはアクセスできないため、モデルは最近の変化に対する反応が鈍い。

Suboptimal: Data freshness impacts the quality of model output.
最適ではない： データの鮮度がモデル出力の品質に影響する。
Without the up-to-date signals (such as supply and demand), the fulfillment process can be suboptimal since models do not have access to real-time changes and the lag in decision-making can lead to inefficient resource allocation.
最新のシグナル（需給など）がなければ、モデルはリアルタイムの変化にアクセスできず、意思決定の遅れが非効率的な資源配分につながるため、フルフィルメント・プロセスは最適化されない可能性がある。

As we introduce product innovations in the Instacart app to improve personalization, inspiration, capturing and serving dynamic features in real time becomes essential.
パーソナライゼーションを向上させるためにInstacartアプリに製品イノベーションを導入する際、インスピレーション、リアルタイムでの動的機能のキャプチャと提供が不可欠になります。
This requires transitioning most of the ML services at Instacart from batch-oriented to real-time systems.
そのためには、インスタカートのMLサービスのほとんどをバッチ指向からリアルタイム・システムに移行する必要がある。
Among other things, we have gone through the following major transitions to enable real-time ML:
とりわけ、リアルタイムMLを実現するために、私たちは以下のような大きな変遷を経てきた：

Real-Time Serving: From serving precomputed predictions to real-time serving in order to reduce staleness, limited coverage, and resource underutilization.
リアルタイム配信： 事前に計算された予測をリアルタイムに提供することで、陳腐化、カバレッジの制限、リソースの過少利用を削減する。

Real-Time Features: From batch features to real-time features to ensure data freshness, and enable models to respond to up-to-date changes.
リアルタイム機能： バッチ機能からリアルタイム機能まで、データの鮮度を確保し、モデルが最新の変化に対応できるようにします。

## Transition 1: From serving precomputed predictions to real-time serving Transition 1： 事前に計算された予測値の提供からリアルタイムの提供へ

Transitioning to a real-time serving system has been made possible by two products: Feature Store and Online Inference Platform.
リアルタイム・サービング・システムへの移行は、2つの製品によって可能になった： フィーチャーストアとオンライン推論プラットフォームである。
Feature Store is a key-value store for fast feature retrieval and Online Inference Platform is a system that hosts each model as an RPC (Remote Procedure Call) endpoint.
Feature Storeは高速な特徴検索のためのKey-Valueストアであり、Online Inference Platformは各モデルをRPC（Remote Procedure Call）エンドポイントとしてホストするシステムである。
Real-Time Serving improved machine learning applications by integrating new features such as personalization, optimized computation resources by eliminating execution of unused predictions, and increased conversions by optimizing long-tail queries.
Real-Time Servingは、パーソナライゼーションなどの新機能を統合することで機械学習アプリケーションを改善し、未使用の予測の実行を排除することで計算リソースを最適化し、ロングテールのクエリを最適化することでコンバージョンを増加させた。
Most importantly, it also provided better customer experience because it incorporated personalized results and improved results for new users/queries.
最も重要なことは、パーソナライズされた結果が組み込まれ、新規ユーザーやクエリに対する結果が改善されたため、より良い顧客体験が提供されたことだ。

Even though the transition was a significant win for machine learning applications, introducing real-time serving introduced many technical challenges.
この移行は機械学習アプリケーションにとって大きな勝利だったとはいえ、リアルタイム・サービングの導入には多くの技術的課題があった。

## Challenges of Moving to Real-Time Serving リアルタイム・サービスへの移行の課題

Latency: Latency plays an important role in the user experience; no one likes to wait to see search results loading while shopping.
待ち時間： 待ち時間はユーザー体験において重要な役割を果たす。ショッピング中に検索結果がロードされるのを待つのが好きな人はいない。
A real-time serving system introduces dependencies on feature retrieval, feature engineering, and model prediction and makes it essential that those processes are fast and can be accessed with a tight latency budget.
リアルタイム・サービング・システムでは、特徴検索、特徴エンジニアリング、モデル予測に依存関係が生じ、これらのプロセスが高速で、厳しいレイテンシ・バジェットでアクセスできることが不可欠となる。

Availability: The real-time inference system introduces a failure point that can cause downtime in the backend service.
可用性： リアルタイム推論システムは、バックエンド・サービスにダウンタイムを引き起こす可能性のある障害点を導入する。
Ensuring high availability of the model services necessitates better monitoring, error handling, and deployment practices.
モデル・サービスの高い可用性を確保するには、モニタリング、エラー処理、デプロイメントを改善する必要がある。

Steep Learning Curve: The system involves understanding many new components and processes.
急な学習曲線： このシステムは、多くの新しいコンポーネントやプロセスを理解する必要がある。
It was mainly challenging for machine learning engineers because it changed the development process and introduced many new tools.
開発プロセスが変わり、多くの新しいツールが導入されたため、主に機械学習エンジニアにとってチャレンジングなものだった。

## Key Decisions 

Unified Interface: Developing a unified interface, Griffin, enabled us to integrate best practices such as unit tests, integration tests, and canary deployments.
統一インターフェース： 統一インターフェースGriffinを開発することで、ユニットテスト、統合テスト、カナリアデプロイメントなどのベストプラクティスを統合することができた。
It also reduced the learning curve for machine learning engineers by providing standard workflow templates, and tools for fast troubleshooting.
また、標準的なワークフローテンプレートや、迅速なトラブルシューティングのためのツールを提供することで、機械学習エンジニアの学習曲線を短縮した。
Additionally, creating a single entrypoint to our system allowed us to standardize monitoring, observability, and other processes required for reliability.
さらに、システムへのエントリーポイントをひとつにしたことで、モニタリングや観測可能性など、信頼性に必要なプロセスを標準化することができた。

Generalized Service Format: We chose an RPC framework that was widely used at Instacart for inter-service communications.
一般化されたサービス・フォーマット： Instacartでサービス間通信に広く使われているRPCフレームワークを選択した。
Reusing existing tools allowed us to quickly develop a production-grade platform and support communication between multiple languages such as Ruby, Scala, Python, and Go.
既存のツールを再利用することで、プロダクション・グレードのプラットフォームを迅速に開発し、Ruby、Scala、Python、Goといった複数の言語間のコミュニケーションをサポートすることができた。
Furthermore, it allowed machine learning engineers to share knowledge between groups and grow faster with collaboration.
さらに、機械学習エンジニアがグループ間で知識を共有し、コラボレーションによってより速く成長できるようになった。

## Transition 2: From batch features to real-time features Transition 2： バッチ機能からリアルタイム機能へ

The transition to real-time serving has improved the user experience by eliminating the staleness and limited coverage of the precomputed predictions.
リアルタイム配信への移行は、事前に計算された予測の陳腐さと限られたカバレッジを排除することで、ユーザーエクスペリエンスを向上させた。
However, all predictions are still based on batch features.
しかし、すべての予測は依然としてバッチ特徴に基づいている。
The best experience in a shopping journey requires both batch features and real-time features.
ショッピング・ジャーニーにおける最高の体験には、バッチ機能とリアルタイム機能の両方が必要だ。
To enable real-time features, we developed a real-time processing pipeline with streaming technologies as shown in Figure 4.
リアルタイム機能を実現するために、図4に示すようなストリーミング技術を用いたリアルタイム処理パイプラインを開発した。
The pipeline listens to raw events stored in Kafka published by services, transforms them into desired features using Flink, and sinks them into Feature Store for on-demand access.
パイプラインは、サービスによって公開されたKafkaに保存された生のイベントをリスンし、Flinkを使ってそれらを必要な機能に変換し、オンデマンドアクセスのためにFeature Storeにシンクする。
Although streaming is a relatively mature technology, there are still quite a few challenges we faced in the transition.
ストリーミングは比較的成熟した技術ですが、移行にあたって直面した課題はまだたくさんあります。

### Challenges 課題

Siloed streaming technologies in different organizations: The need for stream processing at different teams vary from simple notifications to analytics.
組織ごとにサイロ化されたストリーミング技術： 単純な通知から分析まで、チームによってストリーム処理の必要性は異なる。
Therefore, each organization had adopted the tools that fit its respective needs and we ended up with three different streaming tools.
そのため、各組織はそれぞれのニーズに合ったツールを採用し、結局、3つの異なるストリーミング・ツールが存在することになった。
This works fine locally within each organization, but it is challenging for machine learning since it requires events built across different organizations.
これは各組織内では問題なく機能するが、機械学習では異なる組織間で構築されたイベントが必要となるため、難しい。

Event consistency and quality: Events have been mostly consumed/managed by local teams for their specific needs.
イベントの一貫性と質： イベントは、そのほとんどがローカルチームによって、それぞれのニーズに合わせて消費／管理されてきた。
This brings two challenges when consolidating events to generate real-time features: 1) it is not clear what events are available; and 2) event quality is not guaranteed.
このため、イベントを統合してリアルタイム機能を生成する場合、2つの課題が生じる： 1）どのようなイベントが利用可能であるかが明確でない、2）イベントの品質が保証されていない。

Complex pipeline with new development process: As shown in Figure 4, the real-time features pipeline introduces a new tech stack.
新しい開発プロセスを伴う複雑なパイプライン 図4に示すように、リアルタイム機能パイプラインは新しい技術スタックを導入している。
It starts from raw events published by services, goes through stream processing and Feature Store, and responds to user requests in real-time.
サービスによって公開された生のイベントから始まり、ストリーム処理とフィーチャーストアを経て、ユーザーのリクエストにリアルタイムで応答する。
The challenges with this are twofold.
これには2つの課題がある。
On the one hand, real-time features (streaming in general) are not common knowledge for machine learning engineers and data scientists.
一方で、リアルタイム機能（ストリーミング全般）は、機械学習エンジニアやデータサイエンティストにとって一般的な知識ではない。
On the other hand, it is more involved to set up a development environment for streaming processing.
一方、ストリーミング処理のための開発環境を構築するのは、より手間がかかる。
The fact that data streaming technologies work best in JVM (Java and Scala) with suboptimal support in Python also makes the learning curve steeper.
データ・ストリーミング技術はJVM（JavaとScala）で最もうまく機能し、Pythonでは最適なサポートが得られないという事実も、学習曲線をより険しいものにしている。

### Key Decisions 重要な決定事項

Centralized event storage: Given the challenging situation that there exist multiple streaming backends in different organizations, we chose Kafka as a centralized storage to put all raw events together so that we can derive ML features from them in consistent format.
イベントの一元管理： 異なる組織に複数のストリーミング・バックエンドが存在するという困難な状況を考慮し、我々は、すべての生イベントをまとめて、一貫したフォーマットでMLの特徴を導き出せるようにするための集中ストレージとしてKafkaを選択した。
This introduces some extra latency to the pipeline (usually within a few 100ms) and uses some more resources, but the benefits outweigh these shortcomings.
これは、パイプラインに余分なレイテンシーをもたらし（通常は数100ms以内）、より多くのリソースを使用するが、利点はこれらの欠点を上回る。
First, centralized storage scales quickly and avoids building multiple interfaces between real-time ML systems and different streaming tools.
第一に、一元化されたストレージは素早くスケールし、リアルタイムMLシステムと異なるストリーミングツールとの間に複数のインターフェースを構築する必要がない。
Second, this does not impact the existing event usage pattern, and centralized event storage makes it easy to integrate schema validation and data quality checks to improve the events quality.
第二に、これは既存のイベント使用パターンに影響を与えず、一元化されたイベント・ストレージにより、スキーマ検証やデータ品質チェックを統合してイベントの品質を向上させることが容易になる。

Separate event storage and computation: We also made the choice to have separate event storage and event computation.
イベントの保存と計算を分離 また、イベントの保存と計算を別々にすることも選択した。
On the one hand, this modularizes the system by following the design principle of separation of concerns and adopts the best tools for the work.
一方では、関心事の分離という設計原則に従ってシステムをモジュール化し、作業に最適なツールを採用する。
On the other hand, it provides a ground truth reference for all events in a single, durable storage with consistent format and configurable retention period.
その一方で、一貫したフォーマットと設定可能な保存期間を持つ、耐久性のある単一のストレージに、すべてのイベントのグランドトゥルースのリファレンスを提供する。
This makes data audit and compliance review easier, and supports event replay within the retention period when needed.
これにより、データ監査とコンプライアンス・レビューが容易になり、必要に応じて保存期間内のイベント再生をサポートする。

Form cross-functional working groups early: Since real-time features (or real-time ML initiatives in general) are a highly cross-functional effort, early on in the process, we formed a working group among different teams with experts in product/business development, streaming technologies, and ML development.
早期に部門横断的なワーキンググループを結成 リアルタイム機能（またはリアルタイムMLイニシアチブ全般）は、非常に機能横断的な取り組みであるため、プロセスの初期段階で、製品/ビジネス開発、ストリーミング技術、ML開発の専門家を擁するさまざまなチームからなるワーキンググループを結成した。
This group is critical for us to discuss and reach decisions that address our existing challenges in enabling real-time ML.
このグループは、リアルタイムMLを実現する上での既存の課題を解決するための議論や決定を下すために不可欠な存在だ。
It also helps us to debate and evaluate early use cases for real-time ML.
また、リアルタイムMLの初期のユースケースを議論し、評価するのにも役立つ。
For instance, thanks to the collective views of the working group, we prioritize the real-time item availability as the first use case since it is not only an essential model by itself, but also provides fundamental item availability scores that improve item found rate and customer experience, increases ETA prediction accuracy, and improves many services that require up-to-date item availability information.
例えば、ワーキンググループの総意により、我々は、リアルタイムの商品在庫状況を最初のユースケースとして優先しました。なぜなら、それ自体が不可欠なモデルであるだけでなく、商品発見率と顧客体験を向上させる基本的な商品在庫状況スコアを提供し、ETA予測精度を高め、最新の商品在庫状況情報を必要とする多くのサービスを改善するからです。
The success of this fundamental use case has enabled rapid adoption of real-time ML thereafter.
この基本的なユースケースの成功が、その後のリアルタイムMLの急速な普及を可能にした。

## Retrospection ♪回顧

With two critical transitions and other improvements, we have created an ML platform with real-time serving and real-time features as illustrated in Figure 5.
この2つの重要な変遷とその他の改善により、図5に示すように、リアルタイム・サービングとリアルタイム機能を備えたMLプラットフォームが完成した。
The platform transforms the shopping journey to be more dynamic and efficient, with better personalization and optimized fulfillment.
このプラットフォームは、より良いパーソナライゼーションと最適化されたフルフィルメントによって、ショッピング・ジャーニーをよりダイナミックで効率的なものに変える。
Here are some highlights of the applications launched on the platform:
以下は、このプラットフォームで発表されたアプリケーションのハイライトである：

Real-time item availability updates item availability scores in seconds from a couple of hours.
リアルタイムの商品在庫状況は、数時間から数秒で商品在庫状況のスコアを更新します。
This directly improves item found rate, reduces bad orders, and ultimately increases customer satisfaction.
これは、商品の発見率を直接改善し、不良注文を減らし、最終的に顧客満足度を高める。

Session-based recommendation and personalization models make predictions within the shopping session in real-time.
セッションベースのレコメンデーションとパーソナライゼーションモデルは、リアルタイムでショッピングセッション内の予測を行う。
For instance, by removing items that wouldn’t be of interest to the customer based on their choices in the recent session, we have already made the Instacart storefront more fresh and dynamic with real-time user impression data.
例えば、最近のセッションでの顧客の選択に基づいて、顧客が興味を示さないような商品を削除することで、Instacartのストアフロントをリアルタイムのユーザーの印象データによって、より新鮮でダイナミックなものにしています。

Fraud detection algorithms catch suspicious behaviors in real time and make it possible to prevent fraudulent activities before a loss occurs.
不正検知アルゴリズムは、疑わしい行動をリアルタイムでキャッチし、損失が発生する前に不正行為を防止することを可能にする。
This alone directly reduces millions of fraud-related costs annually.
これだけで、年間数百万ドルの不正関連コストを直接削減できる。

Overall, the real-time ML platform flows terabytes of event data per day, generates features with latency in the order of seconds contrast to hours before, and serves hundreds of models in real time.
全体として、リアルタイムMLプラットフォームは、1日あたりテラバイトのイベントデータを流し、数時間前とは対照的に数秒のオーダーのレイテンシーで特徴を生成し、リアルタイムで数百のモデルを提供する。
The platform resolves the limitations of batch-oriented systems to help related ML applications go real time, and also unleashes ML applications to make more business impact.
このプラットフォームは、バッチ指向のシステムの制限を解決し、関連するMLアプリケーションのリアルタイム化を支援するとともに、MLアプリケーションを解放して、より多くのビジネスインパクトをもたらす。
Over the last year, the platform has enabled considerable GTV (gross transaction value) growth in a series of A/B experiments.
昨年、このプラットフォームは、一連のA/B実験においてGTV（総取引額）の大幅な伸びを実現した。

## Lessons Learned Lessons Learned

Infrastructure plays a critical role in real-time ML
リアルタイムMLではインフラが重要な役割を果たす

Transitioning into a real-time system required a major investment in infrastructure tools and processes in order to achieve better observability, efficient computation, high availability, and reliable deployment.
リアルタイム・システムに移行するためには、より優れた観測可能性、効率的な計算、高可用性、信頼性の高い配備を実現するために、インフラストラクチャー・ツールやプロセスに大きな投資が必要だった。
We used many tools and processes for real-time serving and real-time features which allowed us to productionize the platform quickly and show an impact at Instacart.
私たちは、リアルタイム配信とリアルタイム機能のために多くのツールとプロセスを使用し、プラットフォームを迅速に本番化し、Instacartでインパクトを示すことができました。
Using a unified interface that allows a diverse set of tools was essential in our success.
多様なツールが使える統一されたインターフェイスを使うことは、私たちの成功に不可欠だった。

Make incremental progress
少しずつ前進する

Going from a batch-oriented ML system to real-time ML platform is a big step.
バッチ指向のMLシステムからリアルタイムMLプラットフォームへの移行は大きな一歩だ。
To make it more manageable, we carried out the transition in two distinct phases as detailed above.
より管理しやすくするため、私たちは上記のように2段階に分けて移行を行った。
We also identified at least one impactful use case to start with for each transition.
また、各トランジションについて、少なくとも1つのインパクトのあるユースケースを特定した。
As a result, in each transition phase, we have a clear goal and the incremental impact can be easily measured.
その結果、各移行段階において明確な目標が設定され、段階的なインパクトを簡単に測定できるようになった。
This not only enabled a more gradual platform update but also reduced the learning curve for machine learning engineers who adopted the platform.
これにより、より緩やかなプラットフォームのアップデートが可能になっただけでなく、このプラットフォームを採用した機械学習エンジニアの学習曲線も短縮された。

Generalized and specialized solutions
一般的なソリューションと専門的なソリューション

We adopted a generalized solution that helped us cover the majority of the cases with excellent support.
私たちは汎用的なソリューションを採用し、優れたサポートで大半のケースをカバーすることができた。
To accelerate the development, we then started building more specialized products such as an Embedding Platform to focus on more targeted circumstances and reduce the support requests.
開発を加速させるために、私たちはより専門的な製品、たとえばエンベッディング・プラットフォームを作り始めました。
This balance between generalization and specialization improves the productivity for those specialized use cases, and achieves high reliability in the overall system.
この一般化と専門化のバランスは、専門化されたユースケースの生産性を向上させ、システム全体の高い信頼性を実現する。

Grow infrastructures with products
製品でインフラを成長させる

Machine learning engineers who adopted our platform during early development played a significant role in improving the quality by providing feedback and in growing the adoption by marketing the platform to other product teams at Instacart.
開発初期に私たちのプラットフォームを採用した機械学習エンジニアは、フィードバックを提供することで品質を向上させ、Instacartの他の製品チームにプラットフォームを売り込むことで採用を拡大する上で重要な役割を果たしました。