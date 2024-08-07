## 0.1. refs: refs：

- https://dev.to/cassiocappellari/fundamentals-of-rest-api-2nag https://dev.to/cassiocappellari/fundamentals-of-rest-api-2nag

# 1. Fundamentals of REST API REST APIの基礎

## 1.1. Introduction

We live in a modern and ultra-connected world that shares a huge amount of data every second through browsers, servers, softwares and applications.
私たちは、ブラウザ、サーバ、ソフトウェア、アプリケーションを通じて毎秒莫大な量のデータを共有する、現代的で超接続された世界に住んでいる。
For all these systems to communicate with each other, we have a tool that is the key player to integrate all this complexity: the APIs.
これらすべてのシステムが互いに通信するために、この複雑なシステムすべてを統合する重要な役割を果たすツールがある： APIである。

In this article I share my knowledge, experience and studies about this technology, with the goal to provide a basic understanding of the main fundamentals of API, REST and HTTP Protocol.
この記事では、API、REST、HTTPプロトコルの主な基礎についての基本的な理解を提供することを目的として、この技術に関する私の知識、経験、研究を共有する。

## 1.2. API Concept APIコンセプト

API means Application Programming Interface and, like any other interface, allows interactions.
APIとはApplication Programming Interface（アプリケーション・プログラミング・インターフェース）のことで、**他のインターフェースと同様、相互作用を可能にするもの**である。
In the case of an API, it allows interactions between systems by following a set of standards and protocols in order to share features, information and data.
APIの場合、一連の標準とプロトコルに従って、システム間の相互作用を可能にし、機能、情報、データを共有する。
In other words, it provides developers the opportunity to build and design products and services that will communicate with other products and services.
言い換えれば、APIは、開発者が他の製品やサービスと通信する製品やサービスを構築し、設計する機会を提供する。

We can have different architectural styles of APIs and, nowadays, the main one that is a key part of our Internet world it’s called REST, an acronym for REpresentational State Transfer.
**APIにはさまざまなアーキテクチャー・スタイルがあるが、現在、インターネットの世界で重要な役割を担っているのは、RESTと呼ばれるもの**だ。

## 1.3. REST Fundamentals RESTの基礎

REST is an architecture style to develop web services, which uses the HTTP protocol as a communication interface in order to transfer data through HTTP methods.
**RESTはウェブサービスを開発するためのアーキテクチャスタイルで、HTTPプロトコルを通信インターフェースとして使用し、HTTPメソッドを通じてデータを転送する**。
In other words, it allows performing basic data manipulation within an application with efficiency, such as creating, retrieving, updating and deleting information.
言い換えれば、情報の作成、検索、更新、削除など、アプリケーション内での基本的なデータ操作を効率的に行うことができる。

REST was born and created in 2000 by Roy Fielding in his PhD dissertation and, according to him:
RESTは、2000年にロイ・フィールディングが博士論文の中で誕生させたもので、彼によれば次のようなものである：

“The name “Representational State Transfer” is intended to evoke an image of how a well-designed Web application behaves: a network of web pages (a virtual state-machine), where the user progresses through the application by selecting links (state transitions), resulting in the next page (representing the next state of the application) being transferred to the user and rendered for their use.”
「Representational State Transfer（表現的状態遷移）」という名前は、よく設計されたウェブアプリケーションの動作をイメージさせることを意図しています： ウェブページのネットワーク（仮想的な状態マシン）であり、ユーザーはリンク（状態遷移）を選択することでアプリケーションを進行させ、その結果、次のページ（アプリケーションの次の状態を表す）がユーザーに転送され、ユーザーが使用できるようにレンダリングされる。"

So, as Roy Fielding defines, in order to build a well-designed web application, we can use REST principles that help us to develop services that are more scalable, reliable and flexible.
だから、ロイ・フィールディングが定義しているように、よく設計されたウェブアプリケーションを構築するために、**よりスケーラブルで信頼性があり、柔軟性のあるサービスを開発するのに役立つREST原則**を使用することができます。
To achieve this goal, the REST architecture has six constraints and an API that is driven by that can be called RESTful.
この目標を達成するために、**RESTアーキテクチャには6つの制約**があり、それによって駆動されるAPIはRESTfulと呼ぶことができる。
(お、前読んだ「What is REST?」では、RESTfulシステムの特性は2つだったきがする...!:thinking: : 1:クライアントとサーバの関心が分離している, 2:statelessである(=サーバがクライアントの状態を保存しない))

### 1.3.1. Client-Server (契約1)

The main principle of the Client-Server web architecture is the Separation of Concerns, which means that the Client that sends the request it’s completely independent from the Server that returns the response.
クライアント・サーバーのウェブアーキテクチャの主要な原則は、関心の分離です。これは、**リクエストを送信するクライアントが、レスポンスを返すサーバと完全に独立していること**を意味します。

### 1.3.2. Stateless ステートレス (契約2)

All the information (state) that is required in a request must be sended by the Client.
**リクエストに必要なすべての情報(state)は、クライアントによって送信されなければならない**。
Therefore, the Server must not store any data during a Client-Server communication, which means that every request is a standalone request.
したがって、サーバはクライアントとサーバの通信中にデータを保存してはならず、**すべてのリクエストは standalone なリクエストである**ということです。

### 1.3.3. Cache (契約3)

Cache is a computational storage structure focused on keeping stored data that is frequently accessed, improving performance and network efficiency.
**キャッシュは、頻繁にアクセスされるデータを保持し、パフォーマンスとネットワーク効率を向上させることに焦点を当てた計算ストレージ構造**です。
Therefore, through caching, it’s possible to reduce or even eliminate the need for the Client to send requests to the Server (who must inform if the request can be cacheable or not).
したがって、キャッシュを通じて、クライアントがサーバにリクエストを送信する必要を減らすか、さらには排除することができます (**サーバはリクエストがキャッシュ可能かどうかを通知する必要があります**)。

(キャッシュされるのは基本的にサーバ側??クライアント側でキャッシュされることもある??:thinking:)

### 1.3.4. Interface Uniform (契約4)

(これって統一された相互作用方法、みたいなイメージ??:thinking:)

Means how Client and Server will share information by defining an interface that must be followed in every request.
クライアントとサーバがどのように情報を共有するかを意味し、すべてのリクエストで従わなければならないインターフェイスを定義する。
In other words, it’s a contract between the Client and the Server that determines the standards for their communication.
言い換えれば、それはクライアントとサーバの間の契約であり、彼らのコミュニケーションのための標準を決定する。

Here, we have four additional constraints that is part of Uniform Interface:
ここでは、**Uniform Interface の一部である4つの追加の制約**があります。

#### 1.3.4.1. Identification of Resources リソースの識別

REST is based on resources, and a resource is an information that can be named.
RESTはリソースに基づいており、**リソースとは名前を付けることができる情報**のことである。
It’s used in a request to identify what the Client wants to access in the Server.
これは、クライアントがサーバの何にアクセスしたいかを識別するための リクエストで使われる。
(path to the resourceをリクエストに含めないといけないんだよね...!:thinking:)

For example, to retrieve a list of products, the resource must be setted in the URL: http://api.example.com/products
例えば、商品のリストを取得するには、URLにリソースを設定しなければならない： `http://api.example.com/products` (base URL + path to the resource...! :thinking:)

#### 1.3.4.2. Manipulation of Resources Through Representation 表現を通じたリソースの操作

(要するに、ヘッダーの `Accept` field を指定しないといけないよってことっぽい...??:thinking:)

The Client must be sure that the request to the Server has enough information to manipulate (create, retrieve, update, delete) the informed resource, which can be represented by multiple formats, such as JSON, XML, HTML etc.
**クライアントは、サーバへのリクエストに、指定されたリソースを操作（作成、取得、更新、削除）するための十分な情報が含まれていることを確認しなければならない**。これは、JSON、XML、HTMLなどの複数の形式で表現することができる。(これって Design by Contract における事前条件みたいな...??)
In other words, the Client can specify the desired representation of a resource in every request to a Server.
言い換えれば、クライアントはサーバへのリクエストのたびに、リソースの望ましい表現を指定することができる。

For example: a Client can specify in a request to retrieve a resource in JSON format.
例えば、クライアントは

#### 1.3.4.3. Self-descriptive Messages 自己紹介メッセージ

A self-descriptive message ensures a uniform interface in the communication by containing all the information that a Client or a Server needs to understand the request and the response just by checking the semantics of the message.
self-descriptive messageは、統一されたインターフェイスを通信に保証する。それは、メッセージの意味論をチェックすることでクライアントやサーバがリクエストとレスポンスを理解するために必要なすべての情報を含むことにより...!

(なんのこっちゃ...??)

#### 1.3.4.4. HATEOAS (Hypertext As The Engine Of Application State) (アプリケーション状態のエンジンとしてのハイパーテキスト)

HATEOAS means that a response sent from the Server should contain information about what the Client can do in further requests.
**HATEOASとは、サーバから送られるレスポンスが、クライアントが更なるリクエストで何ができるかについての情報を含むべきであること**を意味する。
In other words, the Server indicates what actions the Client can do next.
言い換えれば、**サーバはクライアントが次にどのようなアクションができるかを示す**。
In REST standards, Servers must send only hypermedia (links) to Clients.
**REST標準では、サーバはクライアントにハイパーメディア(links) のみを送信しなければならない**。(ハイパーリンクだけを送信する? 次にそこにアクセスしてくれって示してるってこと??:thinking:)

### 1.3.5. Layered system レイヤーシステム (契約5)

Layered system relates to the fact that there can be more components and subsystems between a Client and a Server.
レイヤードシステムとは、クライアントとサーバーの間により多くのコンポーネントとサブシステムが存在することに関連しています。
In other words, the client can’t assume that it is communicating directly to the Server, and don’t know about the complexity to process the request and return the response.
言い換えれば、**クライアントは、サーバと直接通信しているとは仮定できず、リクエストを処理しレスポンスを返すための複雑さについては知らない**。
(複雑さに関しては、そもそも契約1でサーバとクライアントを分離させてる時点で、満たせる気がする...??:thinking:)

For example: a Client sends a request to a Server, but first it passes by a proxy layer for security check.
例えば クライアントがサーバにリクエストを送信する場合、まずセキュリティチェックのために proxy層を通過する。(なるほど確かに...! Load Balancer とかもそうだよね...!:thinking:)

### 1.3.6. Code On Demand コード・オン・デマンド (契約6)

Code On Demand is the only optional constraint, and means that a Server can send an executable code as a response to the Client.
**コード・オン・デマンドは、唯一のoptionalな制約**であり、**サーバはクライアントに対して実行可能なコードをレスポンスとして送信することができる**ことを意味します。
In other words, it’s what happens when a browser, for example, receives a response from the Server with a HTML tag `<script>` so, when the HTML document is loaded, the script can be executed.
言い換えれば、たとえばブラウザがサーバーからHTMLタグ `<script>` を含むレスポンスを受け取ったときに、HTMLドキュメントがロードされると、スクリプトが実行される。

<!-- ここまで読んだ! RESFfulアプリケーションの6つの制約...! -->

## 1.4. Request Anatomy リクエスト解剖学

Basically, a Client request has 4 main elements that compose all the information that is needed to interact with the Server.
基本的に、クライアントリクエストには4つの主要な要素があり、サーバーとやり取りするために必要なすべての情報を構成します。

### 1.4.1. URL URL

URL means Uniform Resource Locator, which is the address to not just identify a resource, but also to specify how to access it.
URLとはUniform Resource Locator（ユニフォーム・リソース・ロケーター）のことで、リソースを識別するだけでなく、そのリソースへのアクセス方法を指定するためのアドレスである。
In an API, the URL can be named as Base URL, which means that is the base address that will be used in every request.
APIでは、URLはベースURLと名付けることができる。これは、すべてのリクエストで使用されるベースアドレスであることを意味する。

For example: http://api.example.com
例えば http://api.example.com

### 1.4.2. URI URI

URI means Uniform Resource Identifier, which is used in the URL to specify which resource the Client would like to access in a request.
URIとはUniform Resource Identifier(統一資源識別子)のことで、クライアントがリクエストの中でどのリソースにアクセスしたいかを指定するためにURLで使われる。

For example: http://api.example.com/products
例えば http://api.example.com/products

URL: http://api.example.com/
URL http://api.example.com/

URI: /products
URI： /製品

Therefore, every URL is an URI, but not all URIs are URLs.
したがって、すべてのURLはURIであるが、すべてのURIがURLというわけではない。

### 1.4.3. Parameters パラメーター

Parameters are information that can be sended in a request by the Client in order to influence the response by the Server.
パラメータとは、サーバーのレスポンスに影響を与えるために、クライアントがリクエストで送信できる情報のことです。
REST has 4 types of parameters, and its use will depend on the type of action that the request demands.
RESTには4種類のパラメータがあり、その使い方はリクエストが要求するアクションの種類によって異なる。

### 1.4.4. Body Params ボディ・パラメータ

The Body, like the name says, it’s the body of the request which contains all the data that the Server needs to successfully process the request.
Bodyは、その名の通りリクエストのボディで、サーバーがリクエストを正常に処理するために必要なすべてのデータを含んでいます。
Therefore, it’s only used in requests that must send information, such as create or update.
そのため、createやupdateなど、情報を送信しなければならないリクエストでのみ使用される。

Example of a request body in JSON format:
JSON形式のリクエストボディの例：

```json
{
    “name”: “Laptop”,
    “price”: 1000
    “available”: true
}
```

### 1.4.5. Route Params ルート・パラメータ

Route params are parameters inserted in the URL with the information to identify a specific resource in order to take an action, such as: retrieve, edit, update or delete.
Route paramsは、次のようなアクションを実行するために、特定のリソースを識別するための情報をURLに挿入するパラメータです： 取得、編集、更新、削除などです。

For example: http://api.example.com/products/1
例えば http://api.example.com/products/1

In this given example, the route param with value 1 identifies the resource that will be manipulated in the request.
この例では、値1を持つルートパラメータは、リクエストで操作されるリソー スを特定する。

### 1.4.6. Query Params クエリ・パラム

Query params are also parameters inserted in the URL, but with the main difference that it’s use cases are related to filter and search information about a resource, or even paginate and ordinate the results.
クエリパラメータもURLに挿入されるパラメータですが、主な違いは、リソースに関する情報のフィルタリングや検索、あるいは結果のページ分割や整列に使用されることです。

For example:
例えば、こうだ：

http://api.example.com/products?name=laptop&available=true
http://api.example.com/products?name=laptop&available=true

In this given example, the Client communicates to the Server that the request is to retrieve products with name equals laptop, and available equals true.
この例では、Clientは、nameがlaptopでavailableがtrueに等しい製品を検索することをServerに伝える。

### 1.4.7. Headers ヘッダー

Headers allows sending extra information in a request, such as authentication tokens and content types.
ヘッダは、認証トークンやコンテントタイプのような追加情報をリクエストに送ることができます。

For example:
例えば、こうだ：

```
Authorization: Bearer token
Accept: application/json
```

In this given example, the Client is sending extra data informing not just it's credentials to access a resource, but also a desired response format.
この例では、クライアントはリソースにアクセスするためのクレデンシャルだけでなく、 希望する応答フォーマットも知らせる追加データを送信している。

## 1.5. HTTP PROTOCOL httpプロトコル

Alright, now that we have a basic understanding of REST fundamentals and it’s constraints, let’s talk about the communication standard that rules the Internet world by defining the interaction patterns between Clients and Servers: the HTTP Protocol (HyperText Transfer Protocol).
さて、RESTの基礎と制約を理解したところで、クライアントとサーバー間の相互作用パターンを定義することで、インターネットの世界を支配している通信標準について話そう： HTTPプロトコル（HyperText Transfer Protocol）です。

The HTTP Protocol determines not just the methods that are allowed in a REST API, which means the action types that the Client can demand in a request, but also the status codes that the Server returns as a response in order to have a good communication flow.
HTTPプロトコルは、REST APIで許可されるメソッド、つまりクライアントがリクエストで要求できるアクションタイプだけでなく、サーバーが良好な通信フローを持つためにレスポンスとして返すステータスコードも決定する。

### 1.5.1. HTTP Methods HTTP メソッド

There are 5 main methods that a Client can use in a request in order to manipulate an API resource, which are related with the 5 basic data manipulation types in a database, such: Create, Retrieve, Update and Delete.
クライアントがAPIリソースを操作するためにリクエストで使用できる主なメソッドは5つあり、これはデータベースにおける5つの基本的なデータ操作タイプと関連している： Create、Retrieve、Update、Deleteです。

4.1.1 GET
4.1.1 GET

This method is used to retrieve data from a Server by indicating the resource in the URL.
このメソッドは、URLにリソースを指定してサーバーからデータを取得するために使用される。
For example, to request a list of products of an API, the Client might send:
例えば、あるAPIの製品リストを要求する場合、クライアントは次のように送信する：

GET http://api.example.com/products
http://api.example.com/products

4.1.2 POST
4.1.2 POST

This method is used to create a new resource in the Server by indicating it in the URL and sending the resource data in the request body.
このメソッドは、URLでリソースを示し、リクエストボディでリソースデータを送信することによって、サーバーに新しいリソースを作成するために使用されます。

For example:
例えば、こうだ：

POST http://api.example.com/products
POST http://api.example.com/products

Request body in JSON format:
JSON形式のリクエストボディ：

```json
{
    “name”: “Laptop II”,
    “price”: 1000
    “available”: true
}
```

In this given example, a new product will be created in the database with this provided information.
この例では、提供された情報を使ってデータベースに新しい商品が作成される。

4.1.3 PUT
4.1.3 PUT

This method is used to update a resource data in the Server by identifying it in the URL, and sending the information that will be updated in the request body.
このメソッドは、URLでリソースデータを特定し、リクエストボディで更新される情報を送信することで、サーバー内のリソースデータを更新するために使用されます。

PUT http://api.example.com/products/1
PUT http://api.example.com/products/1

Request body in JSON format:
JSON形式のリクエストボディ：

```json
{
    “name”: “Laptop”,
    “price”: 5000,
    “available”: false
}
```

In this given example, the product with ID 1 will be updated.
この例では、ID 1の製品が更新される。

4.1.4 PATCH
4.1.4 パッチ

This method is also used to update a resource data in the Server by identifying it in the URL, but with the main difference of updating just a specific information.
このメソッドも、URLでリソースデータを特定し、サーバー内のリソースデータを更新するために使用されますが、特定の情報のみを更新するという大きな違いがあります。

PATCH http://api.example.com/products/1
パッチ http://api.example.com/products/1

Request body in JSON format:
JSON形式のリクエストボディ：

```json
{
    “available”: true
}
```

In this given example, just the available property of the product with ID 1 will be updated.
この例では、ID 1の商品のavailableプロパティだけが更新されます。

4.1.5 DELETE
4.1.5 DELETE

This method is used to delete a resource in the Server by identifying it in the URL.
このメソッドは、URLでリソースを特定することにより、サーバー内のリソースを削除するために使用されます。

For example:
例えば、こうだ：

DELETE http://api.example.com/products/1
DELETE http://api.example.com/products/1

In this given example, the product with ID 1 will be deleted.
この例では、ID 1の製品が削除される。

### 1.5.2. HTTP Status Code HTTP ステータスコード

The HTTP Status Codes are codes returned by the Server in order to indicate the type of response in a Client’s request, facilitating the understanding just by its group and number.
HTTPステータスコードは、クライアントのリクエストのレスポンスの種類を示すためにサーバーから返されるコードで、そのグループと番号だけで理解が容易になります。

The most commonly used groups and numbers of status code are:
最もよく使われるステータスコードのグループと番号は以下の通りである：

4.2.1 Group 2
4.2.1 グループ2

Status group that indicates a successful request.
リクエストが成功したことを示すステータスグループ。

4.2.2 Group 3
4.2.2 グループ3

Status group that indicates redirect responses, which are used to inform the Client that the Server needed to perform a redirect to a new URL.
サーバーが新しいURLへのリダイレクトを実行する必要があることをクライアントに通知するために使用される、リダイレクト応答を示すステータスグループ。

4.2.3 Group 4
4.2.3 グループ4

Status group that indicates an error in the Client side, which means that the request was incorrectly builded.
クライアント側のエラーを示すステータスグループで、 リクエストのビルドに誤りがあったことを意味する。

4.2.4 Group 5
4.2.4 第5グループ

Status group that indicates an error in the Server side, which means that the request was sent correctly by the Client, but an error occurred while processing it.
サーバー側のエラーを示すステータスグループ。これは、リクエストはクライアントから正しく送信されたが、処理中にエラーが発生したことを意味する。

## 1.6. Conclusion 結論

I hope that this article helped you to have a basic theoretical approach about REST fundamentals, which is an essential knowledge to every programmer that develops web services.
この記事が、ウェブサービスを開発するすべてのプログラマーにとって不可欠な知識であるRESTの基礎について、基本的な理論的アプローチを持つ助けになったことを願っている。

And, now that you have this core understanding, I invite you to read my other article that provides the basic concepts of an incredible technology for building REST APIs just by clicking on the link below.
そして、この核心的な理解を得たところで、REST APIを構築するための素晴らしいテクノロジーの基本概念を提供する私の別の記事を読んでいただきたい。

```

```
