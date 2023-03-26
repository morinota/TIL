## links リンク

- https://microservices.io/patterns/microservices.html https://microservices.io/patterns/microservices.html

# Pattern: Microservice Architecture パターン マイクロサービス・アーキテクチャ

## Context コンテクスト

You are developing a business-critical enterprise application
ビジネスクリティカルなエンタープライズアプリケーションを開発している
You need to deliver changes rapidly, frequently and reliably - as measured by the DORA metrics - in order for your business to thrive in today’s volatile, uncertain, complex and ambiguous world
今日の不安定、不確実、複雑、曖昧な世界でビジネスを成功させるためには、DORAメトリクスで測定されるように、迅速、頻繁、かつ信頼性の高い変化を提供することが必要です。
Consequently, your engineering organization is organized into small, loosely coupled, cross-functional teams
その結果、エンジニアリング組織は、小規模で疎結合なクロスファンクショナルチームに編成されます。
Each team delivers software using DevOps practices as defined by the DevOps handbook
各チームは、DevOpsハンドブックで定義されたDevOpsプラクティスを用いてソフトウェアを提供する。
In particular, it practices continuous deployment
特に、継続的なデプロイメントを実践している
The team delivers a stream of small, frequent changes that are tested by an automated deployment pipeline and deployed into production.
このチームは、小規模で頻繁な変更を次々と提供し、自動デプロイメントパイプラインによってテストされ、本番環境にデプロイされます。

A team is responsible for one or more subdomains
チームは1つまたは複数のサブドメインを担当する
A subdomain is an implementable model of a slice of business functionality, a.k.a
サブドメインは、ビジネス機能のスライスを実装可能なモデルであり、以下のようなものである。
business capability
営業力
It consists of business logic, which consists of business entities (a.k.a
ビジネスロジックで構成され、ビジネスエンティティ（a.k.a.
DDD aggregates) that implement business rules, and adapters, which communicate with the outside world
ビジネスルールを実装するDDDアグリゲート）、外部との通信を行うアダプタなど
A Java-based subdomain, for example, consists of classes organized into packages that’s compiled into a JAR file.
例えば、Javaベースのサブドメインは、JARファイルにコンパイルされたパッケージに編成されたクラスで構成されています。

The subdomains implement the application’s behavior, which consists of a set of (system) operations
サブドメインは、アプリケーションの動作を実装するもので、一連の（システム）操作から構成されています。
An operation is invoked in one of three ways: synchronous and asynchronous requests from clients; events published by other applications and services; and the passing of time
操作は、クライアントからの同期および非同期のリクエスト、他のアプリケーションやサービスから公開されるイベント、時間の経過の3つの方法のいずれかで呼び出されます。
It mutates and queries business entities in one or more subdomains.
1つまたは複数のサブドメイン内のビジネスエンティティを変異させ、問い合わせることができます。

## Problem 問題

How to organize the subdomains into one or more deployable/executable components?
サブドメインを1つ以上の展開可能/実行可能なコンポーネントにまとめるには？

## Forces フォース

There are five dark energy forces:
ダークエネルギーの力は5つある：

- Simple components - simple components consisting of few subdomains are easier to understand and maintain than complex components シンプルなコンポーネント - 数個のサブドメインからなるシンプルなコンポーネントは、複雑なコンポーネントよりも理解しやすく、メンテナンスも簡単です。

- Team autonomy - a team needs to be able develop, test and deploy their software independently of other teams チームの自律性 - チームは、他のチームから独立してソフトウェアを開発、テスト、デプロイできる必要があります。

- Fast deployment pipeline - fast feedback and high deployment frequency are essential and are enabled by a fast deployment pipeline, which in turn requires components that are fast to build and test. 高速デプロイメント・パイプライン - 高速フィードバックと高いデプロイメント頻度が不可欠であり、高速デプロイメント・パイプラインによって実現されます。

- Support multiple technology stacks - subdomains are sometimes implemented using a variety of technologies; and developers need to evolve the application’s technology stack, e.g. use current versions of languages and frameworks 複数のテクノロジースタックをサポート - サブドメインは様々なテクノロジーを使って実装される場合があり、開発者はアプリケーションのテクノロジースタックを進化させる必要があります。 最新バージョンの言語やフレームワークを使用する

- Segregate subdomains by their characteristics - e.g. resource requirements to improve scalability, their availability requirements to improve availability, their security requirements to improve security, etc. サブドメインはその特性で分ける - 例 スケーラビリティを向上させるためのリソース要件、可用性を向上させるための可用性要件、セキュリティを向上させるためのセキュリティ要件など。

There are five dark matter forces:
ダークマターフォースは5つある：

- Simple interactions - an operation that’s local to a component or consists of a few simple interactions between components is easier to understand and troubleshoot than complex interactions 単純な相互作用 - コンポーネントに局所的な操作、またはコンポーネント間のいくつかの単純な相互作用で構成される操作は、複雑な相互作用よりも理解しやすく、トラブルシューティングも簡単です。

- Efficient interactions - a distributed operation that involves lots of network roundtrips and large data transfers can be too inefficient 効率的なインタラクション - ネットワークのラウンドトリップや大きなデータ転送を多く含む分散操作は、あまりにも非効率的な場合があります。

- Prefer ACID over BASE - it’s easier to implement an operation as an ACID transaction rather than, for example, eventually consistent sagas BASEよりもACIDを優先する - 例えば、最終的に一貫性のあるサーガよりも、ACIDトランザクションとしてオペレーションを実装する方が簡単だ

- Minimize runtime coupling - to maximize the availability and reduce the latency of an operation ランタイムカップリングの最小化 - オペレーションの可用性を最大化し、レイテンシーを低減させる

- Minimize design time coupling - reduce the likelihood of changing services in lockstep, which reduces productivity 設計時間の結合を最小限に抑える - ロックステップでサービスを変更する可能性を減らし、生産性を低下させる。

## Solution 解決策

Design an architecture that structures the application as a set of independently deployable, loosely coupled, components, a.k.a
アプリケーションを、独立した展開が可能な疎結合のコンポーネントの集合として構成するアーキテクチャを設計する。
services
あっせん
Each service consists of one or more subdomains.
各サービスは、1つまたは複数のサブドメインで構成されています。

Some operations will be local (implemented by a single service), while others will be distributed across multiple services
あるオペレーションはローカル（1つのサービスが実施する）であり、あるオペレーションは複数のサービスに分散される
A distributed operation is implemented using either synchronously using a protocol such as HTTP/REST or asynchronously using a message broker, such as Apache Kafka.
分散操作は、HTTP/RESTなどのプロトコルを使った同期操作と、Apache Kafkaなどのメッセージブローカーを使った非同期操作のどちらかで実現します。

## Examples 例

### Fictitious e-commerce application 架空の電子商取引アプリケーション

Let’s imagine that you are building an e-commerce application that takes orders from customers, verifies inventory and available credit, and ships them
顧客からの注文を受け、在庫と利用可能なクレジットを確認し、発送するeコマース・アプリケーションを構築しているとします。
The application consists of several components including the StoreFrontUI, which implements the user interface, along with some backend services for checking credit, maintaining inventory and shipping orders
アプリケーションは、ユーザーインターフェイスを実装するStoreFrontUIを含むいくつかのコンポーネントと、信用調査、在庫管理、注文の発送などのバックエンドサービスから構成されています。
The application consists of a set of services.
アプリケーションは、一連のサービスから構成されています。

### Show me the code コードを表示する

Please see the example applications developed by Chris Richardson
Chris Richardsonが開発したアプリケーションの例をご覧ください。
These examples on Github illustrate various aspects of the microservice architecture.
Githubにあるこれらの例は、マイクロサービス・アーキテクチャの様々な側面を示しています。

## Resulting context 結果のコンテキスト

### Benefits 福利厚生

This solution has a number of benefits:
このソリューションには、さまざまなメリットがあります：

Simple services - each service consists of a small number of subdomains - possibly just one - and so is easier to understand and maintain
シンプルなサービス - 各サービスは少数のサブドメイン（場合によっては1つ）で構成されるため、理解しやすく保守しやすい

Team autonomy - a team can develop, test and deploy their service independently of other teams
チームの自律性 - チームは他のチームから独立してサービスの開発、テスト、デプロイを行うことができます。

Fast deployment pipeline - each service is fast to test since it’s relatively small, and can be deployed independently
高速なデプロイメント・パイプライン - 各サービスは比較的小さいため、テストが速く、独立してデプロイすることができる

Support multiple technology stacks - different services can use different technology stacks and can be upgraded independently
複数のテクノロジースタックをサポート - 異なるサービスは異なるテクノロジースタックを使用することができ、独立してアップグレードすることができます。

Segregate subdomains by their characteristics - subdomains can be segregated by their characteristics into separate services in order to improve scalability, availabilty, security etc
サブドメインの特性による分離 - スケーラビリティ、可用性、セキュリティなどを向上させるために、サブドメインはその特性によって別々のサービスに分離することができます。

### Drawbacks 欠点

This solution has a number of (potential) drawbacks:
このソリューションには、いくつかの（潜在的な）欠点があります：

Some distributed operations might be complex, and difficult to understand and troubleshoot
分散された操作の中には、複雑で理解やトラブルシューティングが困難なものもあるかもしれません。

Some distributed operations might be potentially inefficient
一部の分散処理では、非効率になる可能性がある

Some operations might need to be implemented using complex, eventually consistent (non-ACID) transaction management since loose coupling requires each service to have its own database.
疎結合では各サービスが独自のデータベースを持つ必要があるため、一部のオペレーションは複雑で最終的に一貫性のある（非ACID）トランザクション管理を使用して実装する必要があるかもしれません。

Some distributed operations might involve tight runtime coupling between services, which reduces their availability.
分散処理の中には、サービス間の実行時結合が強く、可用性が低下するものがあります。

Risk of tight design-time coupling between services, which requires time consuming lockstep changes
サービス間の設計時の結合が強固で、ロックステップの変更に時間がかかるというリスク

### Issues 課題

There are many issues that you must address.
取り組まなければならない課題はたくさんあります。

#### How to design a microservice architecture that avoids the potential drawbacks? 潜在的な欠点を回避するマイクロサービス・アーキテクチャの設計方法とは？

How to design a microservice architecture that avoids the potential drawbacks of complex, inefficient interactions; complex eventually consistent transactions; and tight runtime coupling
複雑で非効率なインタラクション、複雑で一貫性のないトランザクション、厳しいランタイムカップリングといった潜在的な欠点を回避するマイクロサービス・アーキテクチャを設計する方法
Assemblage, is an architecture definition process that uses the dark energy and dark matter forces to group the subdomains in a way that results in good microservice architecture.
Assemblage、は、ダークエネルギーとダークマターの力を使って、良いマイクロサービス・アーキテクチャになるようにサブドメインをグループ化するアーキテクチャ定義プロセスである。

#### How to implement distributed operations? 分散運用をどう実現するか？

One challenge with using the microservice operation is implementing distributed operations, which span multiple services
マイクロサービス運用を利用する際の課題として、複数のサービスにまたがる分散運用の実装がある
This is especially challenging since each service has its own database
特に、各サービスが独自のデータベースを持つため、難易度が高くなります
The solution is to use the service collaboration patterns:
解決策としては、サービス連携パターンを利用することです：

Saga, which implements a distributed command as a series of local transactions
分散コマンドを一連のローカルトランザクションとして実装する「Saga」。

Command-side replica, which replicas read-only data to the service that implements a command
コマンドを実装したサービスに対して、読み取り専用のデータを複製する「コマンドサイドレプリカ

API composition, which implements a distributed query as a series of local queries
分散クエリを一連のローカルクエリとして実装するAPIコンポジション。

CQRS, which implements a distributed query as a series of local queries
分散クエリを一連のローカルクエリとして実装するCQRS

The Saga, Command-side replica and CQRS patterns use asynchronous messaging
Saga、Command-side replica、CQRSの各パターンは、非同期メッセージングを使用します。
Services typically need to use the Transaction Outbox pattern to atomically update persistent business entities and send a message.
サービスは通常、Transaction Outboxパターンを使用して、永続的なビジネスエンティティをアトミックに更新し、メッセージを送信する必要があります。

## Related patterns 関連パターン

There are many patterns related to the Microservices architecture pattern
Microservicesアーキテクチャパターンに関連するパターンはたくさんあります
The Monolithic architecture is an alternative to the microservice architecture
モノリシック・アーキテクチャは、マイクロサービス・アーキテクチャの代替となるものです
The other patterns in the Microservice architecture architecture pattern address issues that you will encounter when applying this pattern.
マイクロサービス・アーキテクチャのアーキテクチャ・パターンの他のパターンは、このパターンを適用する際に遭遇する問題を扱っています。

Sservice collaboration patterns:
Sserviceのコラボレーションパターン：

- Saga, which implements a distributed command as a series of local transactions 分散コマンドを一連のローカルトランザクションとして実装する「Saga」。

- Command-side replica, which replicas read-only data to the service that implements a command コマンドを実装したサービスに対して、読み取り専用のデータを複製する「コマンドサイドレプリカ

- API composition, which implements a distributed query as a series of local queries 分散クエリを一連のローカルクエリとして実装する「APIコンポジション

- CQRS, which implements a distributed query as a series of local queries 分散クエリを一連のローカルクエリとして実装するCQRS

The Messaging and Remote Procedure Invocation patterns are two different ways that services can communicate.
MessagingパターンとRemote Procedure Invocationパターンは、サービスが通信するための2つの異なる方法です。

The Database per Service pattern describes how each service has its own database in order to ensure loose coupling.
Database per Serviceパターンは、疎結合を確保するために、各サービスが独自のデータベースを持つことを説明しています。

The API Gateway pattern defines how clients access the services in a microservice architecture.
API Gatewayパターンは、クライアントがマイクロサービス・アーキテクチャのサービスにアクセスする方法を定義しています。

The Client-side Discovery and Server-side Discovery patterns are used to route requests for a client to an available service instance in a microservice architecture.
Client-side DiscoveryとServer-side Discoveryパターンは、マイクロサービス・アーキテクチャにおいて、クライアントのリクエストを利用可能なサービス・インスタンスにルーティングするために使用されます。

Testing patterns: Service Component Test and Service Integration Contract Test
テストのパターン サービスコンポーネントテスト、サービス統合契約テスト

Circuit Breaker
サーキットブレーカー

Access Token
アクセストークン

Observability patterns:
観察可能なパターン：

- Log aggregation ログ集計

- Application metrics アプリケーションメトリクス

- Audit logging 監査ロギング

- Distributed tracing 分散型トレース

- Exception tracking 例外処理

- Health check API ヘルスチェックAPI

- Log deployments and changes デプロイメントと変更のログ

UI patterns:
UIパターンです：

- Server-side page fragment composition サーバーサイドのページフラグメントの合成

- Client-side UI composition クライアントサイドのUIコンポジション

The Single Service per Host and Multiple Services per Host patterns are two different deployment strategies.
Single Service per HostとMultiple Services per Hostのパターンは、2つの異なる展開戦略です。

Cross-cutting concerns patterns: Microservice chassis pattern and Externalized configuration
横断的な悩みパターン マイクロサービスシャーシパターン、外部化構成

## Known uses 既知の用途

Most large scale web sites including Netflix, Amazon and eBay have evolved from a monolithic architecture to a microservice architecture.
Netflix、Amazon、eBayをはじめとする大規模なWebサイトの多くは、モノリシックなアーキテクチャからマイクロサービス・アーキテクチャへと進化しています。

Netflix, which is a very popular video streaming service that’s responsible for up to 30% of Internet traffic, has a large scale, service-oriented architecture
インターネットトラフィックの最大30％を占める大人気の動画配信サービスであるNetflixは、大規模なサービス指向アーキテクチャを採用しています。
They handle over a billion calls per day to their video streaming API from over 800 different kinds of devices
800種類以上のデバイスから1日10億回以上のビデオストリーミングAPIへの呼び出しを処理しています。
Each API call fans out to an average of six calls to backend services.
1回のAPI呼び出しで、平均6回のバックエンドサービスへの呼び出しが発生します。

Amazon.com originally had a two-tier architecture
Amazon.comはもともと2層のアーキテクチャを持っていた
In order to scale they migrated to a service-oriented architecture consisting of hundreds of backend services
規模を拡大するために、数百のバックエンド・サービスからなるサービス指向アーキテクチャに移行しました。
Several applications call these services including the applications that implement the Amazon.com website and the web service API
Amazon.comのウェブサイトやウェブサービスAPIを実装するアプリケーションを含む、いくつかのアプリケーションがこれらのサービスを呼び出します。
The Amazon.com website application calls 100-150 services to get the data that used to build a web page.
Amazon.comのWebサイトアプリケーションは、Webページを構築するために使用するデータを取得するために100〜150のサービスを呼び出します。

The auction site ebay.com also evolved from a monolithic architecture to a service-oriented architecture
オークションサイトのebay.comも、モノリシックなアーキテクチャからサービス指向のアーキテクチャに進化している
The application tier consists of multiple independent applications
アプリケーション層は、複数の独立したアプリケーションで構成されています
Each application implements the business logic for a specific function area such as buying or selling
各アプリケーションは、売買などの特定の機能領域のビジネスロジックを実装しています。
Each application uses X-axis splits and some applications such as search use Z-axis splits
各アプリケーションはX軸分割を使用し、検索など一部のアプリケーションはZ軸分割を使用する
Ebay.com also applies a combination of X-, Y- and Z-style scaling to the database tier.
また、Ebay.comでは、データベース層にX、Y、Zスタイルのスケーリングを組み合わせて適用しています。

There are numerous other examples of companies using the microservice architecture.
その他にも、マイクロサービス・アーキテクチャを採用した企業の例は数多くあります。