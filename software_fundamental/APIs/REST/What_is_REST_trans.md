## refs: refs：

- https://roadmap.sh/backend https://roadmap.sh/backend

- [What is REST?](https://www.codecademy.com/article/what-is-rest)

# What is REST? RESTとは何か？

Learn about the REST (Representational State Transfer) paradigm and how rest architecture streamlines communication between web components.
**REST (Representational State Transfer) パラダイム**と、RESTアーキテクチャがどのようにウェブコンポーネント間の通信を合理化するかについて学びます。

## REpresentational State Transfer

REST, or REpresentational State Transfer, is an architectural style for providing standards between computer systems on the web, making it easier for systems to communicate with each other.
REST (REpresentational State Transfer) は、**ウェブ上のコンピュータ・システム間で標準を提供するためのアーキテクチャ・スタイル**であり、システム間の通信を容易にする。
REST-compliant systems, often called RESTful systems, are characterized by how they are stateless and separate the concerns of client and server.
RESTに準拠したシステムは、しばしば**RESTfulシステム**と呼ばれ、**ステートレスであることと、クライアントとサーバの関心事を分離していることが特徴**である。(ほうほう)
We will go into what these terms mean and why they are beneficial characteristics for services on the Web.
これらの用語が何を意味するのか、そして**なぜウェブ上のサービスにとって有益な特性なのか**について説明する。
Pay close attention: If you’re looking for a career in tech, you may be asked to define rest during an interview.
注意してください：テック業界でキャリアを探している場合、面接でRESTを定義するよう求められるかもしれません。

### Separation of Client and Server クライアントとサーバの分離

In the REST architectural style, the implementation of the client and the implementation of the server can be done independently without each knowing about the other.
RESTアーキテクチャ・スタイルでは、**クライアントの実装とサーバの実装を互いに知らなくても独立して行うことができる**。(いいね...!:thinking:)
This means that the code on the client side can be changed at any time without affecting the operation of the server, and the code on the server side can be changed without affecting the operation of the client.
つまり、クライアント側のコードを変更してもサーバの動作に影響を与えず、サーバ側のコードを変更してもクライアントの動作に影響を与えない。

As long as each side knows what format of messages to send to the other, they can be kept modular and separate.
**お互いが相手に送るメッセージのフォーマットを知っている限り**、モジュール化され、分離された状態を保つことができる。(うんうん...!じゃあSagemakerのbatch jobもRESTfulなシステムと言えるのかな？:thinking:)
Separating the user interface concerns from the data storage concerns, we improve the flexibility of the interface across platforms and improve scalability by simplifying the server components.
ユーザインターフェースの関心事をデータストレージの関心事から分離することで、インターフェースの柔軟性を向上させ、プラットフォーム間でのインターフェースを改善し、サーバコンポーネントを単純化することでスケーラビリティを向上させる。
Additionally, the separation allows each component the ability to evolve independently.
さらに、分離することによって、各コンポーネントが独立して進化することができる。
(クライアントとサーバを分割することって当たり前のような気がするけど、これがRESTfulなシステムの性質の1つなんだ...!:thinking:)

By using a REST interface, different clients hit the same REST endpoints, perform the same actions, and receive the same responses.
RESTインターフェースを使うことで、異なるクライアントが同じRESTエンドポイントにアクセスし、同じアクションを実行し、同じ応答を受け取る。

### Statelessness ステートレス

Systems that follow the REST paradigm are stateless, meaning that the server does not need to know anything about what state the client is in and vice versa.
RESTパラダイムに従うシステムはステートレスである。**つまり、サーバはクライアントがどの状態にあるかを知る必要がなく、その逆も同様**である。(じゃあSagemakerのbatch jobの実行は、ステートレスとは言えないかも...? jobの実行が完了してからS3上の成果物を見に行かなきゃいけないし...!そういうことではない??:thinking:)
In this way, both the server and the client can understand any message received, even without seeing previous messages.
こうすることで、サーバもクライアントも、以前のメッセージを見なくても、受け取ったメッセージを理解することができる。(あ、「状態を知る必要がない」とは、前回のやりとりを覚えてる必要がない、みたいなこと??:thinking:)
This constraint of statelessness is enforced through the use of resources, rather than commands.
このステートレスという制約は、コマンドではなく、リソースの使用によって強制される。
Resources are the nouns of the Web - they describe any object, document, or thing that you may need to store or send to other services.
リソースはウェブの名詞であり、保存したり他のサービスに送信したりする必要のあるあらゆるオブジェクト、文書、物を表す。

- メモ:
  - statelessnessは、「**サーバがクライアントの状態(state)を保存しない**」という原則。
  - -> 各リクエストが独立しており、その実行に必要な全ての情報を含んでいる必要がある。(あ、じゃあSagemaker の batch jobもstatelessだ...!:thinking:)

Because REST systems interact through standard operations on resources, they do not rely on the implementation of interfaces.
RESTシステムは、リソースに対する標準的な操作を通じて相互作用するため、インターフェースの実装に依存しない。

These constraints help RESTful applications achieve reliability, quick performance, and scalability, as components that can be managed, updated, and reused without affecting the system as a whole, even during operation of the system.
これらの制約により、RESTfulアプリケーションは、システムの運用中であっても、システム全体に影響を与えることなく、管理、更新、再利用が可能なコンポーネントとして、信頼性、迅速なパフォーマンス、およびスケーラビリティを達成することができます。
(ここでの「制約」は2つの性質のこと?? 1. サーバとクライアントの関心の分離、2. ステートレス??:thinking:)

Now, we’ll explore how the communication between the client and server actually happens when we are implementing a RESTful interface.
では、RESTfulインターフェイスを実装する場合、**クライアントとサーバ間の通信が実際にどのように行われるのか**を探ってみよう。

## Communication between Client and Server クライアントとサーバ間の通信

In the REST architecture, clients send requests to retrieve or modify resources, and servers send responses to these requests.
RESTアーキテクチャでは、クライアントはリソースを取得または変更するリクエストを送信し、サーバーはこれらのリクエストに対するレスポンスを送信する。
Let’s take a look at the standard ways to make requests and send responses.
リクエストとレスポンスの標準的な送信方法を見てみよう。

### Making Requests リクエスト

REST requires that a client make a request to the server in order to retrieve or modify data on the server.
RESTでは、サーバ上のデータを取得または変更するために、クライアントがサーバーにリクエストを行う必要がある。
A request generally consists of:
リクエストは一般的に以下の内容で構成される：

- an HTTP verb, which defines what kind of operation to perform
  どのような操作を実行するかを定義する **HTTP verb(動詞)** (HTTP methodって言われるやつかな...! GETとか)

- a header, which allows the client to pass along information about the request
  クライアントがリクエストに関する情報を渡すことを可能にする、**ヘッダー**

- a path to a resource リソースへのパス
  - (これはリソースの場所を特定するURLの一部)
  - endpoint = サーバ上の特定のリソースやデータにアクセスするための具体的なアドレス。
    - **RESTfulシステムにおけるendpoint = base URL + path to a resource**
    - ex. endpoint = `https://api.example.com` + `/users/123`
- an optional message body containing data データを含むオプションの **message body**

#### HTTP Verbs HTTP 動詞

There are 4 basic HTTP verbs we use in requests to interact with resources in a REST system:
RESTシステムでリソースとやりとりするリクエストには、**4つの基本的なHTTP動詞**がある:

- GET — retrieve a specific resource (by id) or a collection of resources
  GET - 特定のリソース（idによる）またはリソースのコレクションを取得します。

- POST — create a new resource
  POST - 新しいリソースを作成する

- PUT — update a specific resource (by id)
  PUT - 特定のリソースを（idで）更新する。

- DELETE — remove a specific resource by id
  DELETE - 特定のリソースをidで削除する。

You can learn more about these HTTP verbs in the following Codecademy article:
これらのHTTP動詞については、以下のCodecademyの記事で詳しく学ぶことができる：

What is CRUD?
CRUDとは？

#### Headers and Accept parameters ヘッダーとAcceptパラメーター

In the header of the request, the client sends the type of content that it is able to receive from the server.
リクエストのヘッダーで、クライアントはサーバから受信できるコンテンツのタイプを送信する。(へぇー！)
This is called the Accept field, and it ensures that the server does not send data that cannot be understood or processed by the client.
これは**Accept フィールド**と呼ばれ、**クライアントが理解できない、あるいは処理できないデータをサーバが送信しないようにする**。
The options for types of content are MIME Types (or Multipurpose Internet Mail Extensions), which you can read more about in the MDN Web Docs.
コンテンツのタイプのオプションは MIME タイプ（またはMultipurpose Internet Mail Extensions）で、MDN Web Docsで詳細を読むことができます。

MIME Types, used to specify the content types in the Accept field, consist of a type and a subtype.
MIMEタイプは、 `Accept` フィールドでコンテントタイプを指定するために使われ、`type` と `subtype` で構成される。
They are separated by a slash (/).
これらはスラッシュ（/）で区切られる。

For example, a text file containing HTML would be specified with the type text/html.
例えば、HTMLを含むテキスト・ファイルは `text/html` タイプで指定される。
If this text file contained CSS instead, it would be specified as text/css.
このテキスト・ファイルにCSSが含まれている場合は、text/cssと指定する。
A generic text file would be denoted as text/plain.
一般的なテキストファイルはtext/plainと表記される。
This default value, text/plain, is not a catch-all, however.
しかし、このデフォルト値であるtext/plainは万能ではない。
If a client is expecting text/css and receives text/plain, it will not be able to recognize the content.
クライアントがtext/cssを期待してtext/plainを受け取った場合、コンテンツを認識することができません。

Other types and commonly used subtypes:
その他のタイプとよく使われるサブタイプ：

image — `image/png`, image/jpeg, image/gif
image - image/png、image/jpeg、image/gif

audio — audio/wav, audio/mpeg
オーディオ - オーディオ/WAV、オーディオ/MPEG

video — video/mp4, video/ogg
ビデオ - ビデオ/MP4、ビデオ/OGG

application — application/json, application/pdf, application/xml, application/octet-stream
アプリケーション - application/json、application/pdf、application/xml、application/octet-stream

For example, a client accessing a resource with id 23 in an articles resource on a server might send a GET request like this:
例えば、クライアントがサーバ上の記事リソースにあるid 23のリソースにアクセスする場合、次のようなGETリクエストを送るかもしれない:

```shell
GET /articles/23 # HTTP verb と path of the resource
Accept: text/html, application/xhtml # Accept field
```

The Accept header field in this case is saying that the client will accept the content in text/html or application/xhtml.
この場合のAcceptヘッダーフィールドは、クライアントがtext/htmlまたは application/xhtmlのコンテンツを受け入れることを述べている。
(うんうん...!)

#### Paths パス

Requests must contain a path to a resource that the operation should be performed on.
**リクエストには、操作を実行するリソースへのパスを含めなければならない**。
In RESTful APIs, paths should be designed to help the client know what is going on.
RESTfulなAPIでは、Pathはクライアントが「何が起こっているのか」を知るのに役立つように設計されるべきです。

Conventionally, the first part of the path should be the plural form of the resource.
**通常、パスの最初の部分はリソースの複数形であるべき**です。(なるほどたしかに:thinking:)
This keeps nested paths simple to read and easy to understand.
これにより、ネストされたパスはシンプルに読みやすく、理解しやすくなる。
(ex. `fashionboutique.com/customers/223/orders/12`)

A path like fashionboutique.com/customers/223/orders/12 is clear in what it points to, even if you’ve never seen this specific path before, because it is hierarchical and descriptive.
`fashionboutique.com/customers/223/orders/12` のようなパスは、階層的で説明的であるため、たとえあなたがこの特定のパスを見たことがなかったとしても、何を指しているのかが明確です。(確かにわかりやすい...! base URLも含まれてるな...!:thinking:)
We can see that we are accessing the order with id 12 for the customer with id 223.
ID223の顧客のID12の注文にアクセスしていることがわかります。

Paths should contain the information necessary to locate a resource with the degree of specificity needed.
**パスは、リソースを見つけるために必要な情報を、必要な程度に具体的に含むべき**である。
When referring to a list or collection of resources, it is not always necessary to add an id.
リソースのリストやコレクションを参照する場合、必ずしもidを追加する必要はない。
For example, a POST request to the fashionboutique.com/customers path would not need an extra identifier, as the server will generate an id for the new object.
例えば、 `fashionboutique.com/customers` パスへのPOSTリクエストは、サーバーが新しいオブジェクトのidを生成するので、余分な識別子を必要としません。

If we are trying to access a single resource, we would need to append an id to the path.
**単一のリソースにアクセスしようとする場合、パスに id を付加する必要がある**。
For example: GET fashionboutique.com/customers/:id — retrieves the item in the customers resource with the id specified.
例えば `GET fashionboutique.com/customers/:id` - 指定された `id` を持つ `customers` リソースのアイテムを取得します。
DELETE fashionboutique.com/customers/:id — deletes the item in the customers resource with the id specified.
`DELETE fashionboutique.com/customers/:id` - `customers` リソース内の指定された `id` のアイテムを削除します。

<!-- ここまで読んだ! -->

### Sending Responses 回答の送信

#### Content Types field

In cases where the server is sending a data payload to the client, the server must include a content-type in the header of the response.
サーバがクライアントに data payload を送信する場合、**サーバはレスポンスのヘッダに `content-type` を含めなければならない**。
(リクエストのヘッダには `Accept` field を含めなきゃいけなくて、レスポンスのヘッダには `content-type` を含めなきゃいけないのか...!:thinking:)
This content-type header field alerts the client to the type of data it is sending in the response body.
この `content-type` ヘッダーフィールドは、レスポンスボディで送信しているデータのタイプをクライアントに通知する。
These content types are MIME Types, just as they are in the accept field of the request header.
これらのコンテントタイプは、リクエストヘッダのacceptフィールドに あるのと同じように、MIMEタイプである。(MIME Typesは表記方法の話??:thinking:)
The content-type that the server sends back in the response should be one of the options that the client specified in the accept field of the request.
**サーバがレスポンスで送り返すcontent-typeは、クライアントがリクエストのacceptフィールドで指定したオプションの一つでなければならない**。(うんうん...!:thinking:)

For example, when a client is accessing a resource with id 23 in an articles resource with this GET Request:
例えば、クライアントがこのGETリクエストでarticlesリソース内のid 23のリソースにアクセスしている場合：

```shell
GET /articles/23 HTTP/1.1 # HTTP verb と path of the resource と HTTP version?
Accept: text/html, application/xhtml # Accept field
```

The server might send back the content with the response header:
サーバは、レスポンスヘッダで以下のようにコンテンツを送り返すかもしれない：

```shell
HTTP/1.1 200 (OK) # HTTP version と ステータスコード
Content-Type: text/html # Content-Type field
```

This would signify that the content requested is being returned in the response body with a content-type of text/html, which the client said it would be able to accept.
これは、リクエストされたコンテンツが`text/html`の`content-type`でレスポンスボディに返されていることを示しており、クライアントが受け入れることができると述べている。

<!-- ここまで読んだ! -->

#### Response Codes レスポンス・コード

Responses from the server contain status codes to alert the client to information about the success of the operation.
サーバーからの応答には、操作の成功に関する情報をクライアントに警告するためのステータスコードが含まれている。
As a developer, you do not need to know every status code (there are many of them), but you should know the most common ones and how they are used:
開発者として、すべてのステータスコードを知る必要はありませんが（多くのステータスコードがあります）、最も一般的なものと、それらがどのように使用されるかを知っておくべきです：

For each HTTP verb, there are expected status codes a server should return upon success:
各HTTP動詞には、成功時にサーバーが返すべき期待ステータスコードがある：

GET — return 200 (OK)
GET - 200 (OK)を返す

POST — return 201 (CREATED)
POST - 201（CREATED）を返す。

PUT — return 200 (OK)
PUT - 200（OK）を返す。

DELETE — return 204 (NO CONTENT) If the operation fails, return the most specific status code possible corresponding to the problem that was encountered.
DELETE - return 204 (NO CONTENT) 操作に失敗した場合は、発生した問題に対応する、可能な限り具体的なステータスコードを返します。

#### Examples of Requests and Responses リクエストとレスポンスの例

Let’s say we have an application that allows you to view, create, edit, and delete customers and orders for a small clothing store hosted at fashionboutique.com.
fashionboutique.comでホストされている小さな洋服店の顧客や注文を表示、作成、編集、削除できるアプリケーションがあるとします。
We could create an HTTP API that allows a client to perform these functions:
クライアントがこれらの機能を実行できるようなHTTP APIを作ることができる：

If we wanted to view all customers, the request would look like this:
すべての顧客を表示したい場合、リクエストは次のようになる：

GET http://fashionboutique.com/customers
http://fashionboutique.com/customers

Accept: application/json
受け付ける： application/json

A possible response header would look like:
可能なレスポンス・ヘッダは次のようになる：

Status Code: 200 (OK)
ステータスコード 200 (OK)

Content-type: application/json
コンテンツタイプ application/json

followed by the customers data requested in application/json format.
の後に、application/json形式で要求された顧客データが続く。

Create a new customer by posting the data:
データを投稿して新しい顧客を作成する：

```shell
POST http://fashionboutique.com/customers
Body:
{
  “customer”: {
    “name” = “Scylla Buss”,
    “email” = “scylla.buss@codecademy.org”
  }
}
```

The server then generates an id for that object and returns it back to the client, with a header like:
そして、サーバーはそのオブジェクトのidを生成し、以下のようなヘッダーをつけてクライアントに返す：

```
201 (CREATED)
Content-type: application/json
To view a single customer we GET it by specifying that customer’s id:

GET http://fashionboutique.com/customers/123
Accept: application/json
```

A possible response header would look like:
可能なレスポンス・ヘッダは次のようになる：

```
Status Code: 200 (OK)
Content-type: application/json
```

followed by the data for the customer resource with id 23 in application/json format.
の後に、id 23の顧客リソースのデータがapplication/json形式で続きます。

We can update that customer by PUT ting the new data:
新しいデータをPUTすることで、その顧客を更新することができる：

```
PUT http://fashionboutique.com/customers/123
Body:
{
  “customer”: {
    “name” = “Scylla Buss”,
    “email” = “scyllabuss1@codecademy.com”
  }
}
```

A possible response header would have Status Code: 200 (OK), to notify the client that the item with id 123 has been modified.
可能なレスポンスヘッダは Status Code： 200 (OK) で、id 123 のアイテムが変更されたことをクライアントに通知します。

We can also DELETE that customer by specifying its id:
また、idを指定してその顧客をDELETEすることもできる：

```
DELETE http://fashionboutique.com/customers/123
```

The response would have a header containing Status Code: 204 (NO CONTENT), notifying the client that the item with id 123 has been deleted, and nothing in the body.
レスポンスには、Status Code： 204 (NO CONTENT) を含むヘッダを持ち、id 123 のアイテムが削除されたことをクライアントに通知します。

## Practice with REST RESTの練習

Let’s imagine we are building a photo-collection site.
写真集サイトを作るとしよう。
We want to make an API to keep track of users, venues, and photos of those venues.
ユーザー、会場、会場の写真を記録するAPIを作りたい。
This site has an index.html and a style.css.
このサイトにはindex.htmlとstyle.cssがあります。
Each user has a username and a password.
各ユーザーはユーザー名とパスワードを持っている。
Each photo has a venue and an owner (i.e.the user who took the picture).
それぞれの写真には撮影地とオーナー（撮影したユーザー）が設定されている。
Each venue has a name and street address.
各会場には名前と住所がある。
Can you design a REST system that would accommodate:
それに対応するRESTシステムを設計できるか：

storing users, photos, and venues
ユーザー、写真、会場の保存

accessing venues and accessing certain photos of a certain venue
会場へのアクセス、特定の会場の特定の写真へのアクセス

Start by writing out:
書き出すことから始めよう：

what kinds of requests we would want to make
どのようなリクエストをしたいのか

what responses the server should return
サーバーが返すべき応答

what the content-type of each response should be
各レスポンスのコンテントタイプはどうあるべきか

## Possible Solution - Models 解決策 - モデル

```shell
{
  “user”: {
    "id": <Integer>,
    “username”: <String>,
    “password”:  <String>
  }
}
{
  “photo”: {
    "id": <Integer>,
    “venue_id”: <Integer>,
    “author_id”: <Integer>
  }
}
{
  “venue”: {
    "id": <Integer>,
    “name”: <String>,
    “address”: <String>
  }
}
```

## Possible Solution - Requests/Responses 解決策 - リクエスト/レスポンス

### GET Requests GETリクエスト

```
Request- GET /index.html Accept: text/html Response- 200 (OK) Content-type: text/html

Request- GET /style.css Accept: text/css Response- 200 (OK) Content-type: text/css

Request- GET /venues Accept:application/json Response- 200 (OK) Content-type: application/json

Request- GET /venues/:id Accept: application/json Response- 200 (OK) Content-type: application/json

Request- GET /venues/:id/photos/:id Accept: application/json Response- 200 (OK) Content-type: image/png
```

### POST Requests POSTリクエスト

```
Request- POST /users Response- 201 (CREATED) Content-type: application/json

Request- POST /venues Response- 201 (CREATED) Content-type: application/json

Request- POST /venues/:id/photos Response- 201 (CREATED) Content-type: application/json
```

### PUT Requests PUTリクエスト

```
Request- PUT /users/:id Response- 200 (OK)

Request- PUT /venues/:id Response- 200 (OK)

Request- PUT /venues/:id/photos/:id Response- 200 (OK)
```

### DELETE Requests DELETEリクエスト

```shell
Request- DELETE /venues/:id Response- 204 (NO CONTENT)

Request- DELETE /venues/:id/photos/:id Response- 204 (NO CONTENT)
```
