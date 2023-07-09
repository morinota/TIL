## link リンク

https://www.thedigitalcatbooks.com/pycabook-chapter-05/
https://www.thedigitalcatbooks.com/pycabook-chapter-05/

# Chapter 5 - Error management 第5章 エラー管理

You sent them out there and you didn't even warn them! Why didn't you warn them, Burke?
彼らを送り出したのに、警告もしなかった！なぜ警告しなかったんだ、バーク？

Aliens, 1986
1986年『エイリアン

In every software project, a great part of the code is dedicated to error management, and this code has to be rock solid.
どのソフトウェア・プロジェクトでも、コードの大部分はエラー管理に費やされる。
Error management is a complex topic, and there is always a corner case that we left out, or a condition that we supposed could never fail, while it does.
エラー管理は複雑なトピックであり、私たちが見落としたコーナーケースや、絶対に失敗しないと思っていたのに、失敗してしまう条件が常に存在する。

In a clean architecture, the main process is the creation of use cases and their execution.
クリーンなアーキテクチャでは、主なプロセスはユースケースの作成とその実行である。
This is, therefore, the main source of errors, and the use cases layer is where we have to implement the error management.
したがって、これがエラーの主な原因であり、ユースケース・レイヤーはエラー管理を実装しなければならない場所である。
Errors can obviously come from the domain models layer, but since those models are created by the use cases the errors that are not managed by the models themselves automatically become errors of the use cases.
エラーは明らかにドメインモデルレイヤーから発生する可能性があるが、これらのモデルはユースケースによって作成されるため、モデル自体で管理できないエラーは自動的にユースケースのエラーになる。

## Request and responses リクエストとレスポンス

We can divide the error management code into two different areas.
エラー管理コードを2つの異なる領域に分けることができる。
The first one represents and manages requests, that is, the input data that reaches our use case.
最初のものは、リクエスト、つまりユースケースに届く入力データを表し、管理する。
The second one covers the way we return results from the use case through responses, the output data.
もうひとつは、ユースケースからレスポンス（出力データ）を通じて結果を返す方法である。
These two concepts shouldn't be confused with HTTP requests and responses, even though there are similarities.
これら2つの概念は、類似点はあってもHTTPリクエストとレスポンスと混同してはならない。
We are now considering the way data can be passed to and received from use cases, and how to manage errors.
現在、ユースケースとのデータの受け渡し方法や、エラーの管理方法について検討している。
This has nothing to do with the possible use of this architecture to expose an HTTP API.
これは、HTTP APIを公開するためにこのアーキテクチャを使用する可能性とは何の関係もない。

Request and response objects are an important part of a clean architecture, as they transport call parameters, inputs and results from outside the application into the use cases layer.
リクエスト・オブジェクトとレスポンス・オブジェクトは、アプリケーションの外部からユースケース・レイヤに呼び出しパラメータ、入力、結果を転送するため、クリーンなアーキテクチャの重要な部分である。

More specifically, requests are objects created from incoming API calls, thus they shall deal with things like incorrect values, missing parameters, wrong formats, and so on.
より具体的には、リクエストはAPIコールから生成されるオブジェクトであるため、間違った値や足りないパラメータ、間違ったフォーマットなどに対処しなければならない。
Responses, on the other hand, have to contain the actual results of the API calls, but shall also be able to represent error cases and deliver rich information on what happened.
一方、レスポンスは、APIコールの実際の結果を含まなければならないが、エラー・ケースを表現し、何が起こったかについての豊富な情報を提供することもできなければならない。

The actual implementation of request and response objects is completely free, the clean architecture says nothing about them.
リクエスト・オブジェクトとレスポンス・オブジェクトの実際の実装は完全に自由である。
The decision on how to pack and represent data is up to us.
データをどのように梱包し、表現するかは私たち次第だ。

To start working on possible errors and understand how to manage them, I will expand room_list_use_case to support filters that can be used to select a subset of the Room objects in storage.
起こりうるエラーに着手し、その管理方法を理解するために、room_list_use_caseを拡張して、ストレージ内のルーム・オブジェクトのサブセットを選択するために使用できるフィルタをサポートするようにします。

The filters could be, for example, represented by a dictionary that contains attributes of the model Room and the logic to apply to them.
フィルターは、例えば、モデル・ルームの属性とそれに適用するロジックを含む辞書で表現することができます。
Once we accept such a rich structure, we open our use case to all sorts of errors: attributes that do not exist in the model, thresholds of the wrong type, filters that make the storage layer crash, and so on.
一旦このようなリッチな構造を受け入れると、ユースケースはあらゆる種類のエラーにさらされることになる。モデルに存在しない属性、間違ったタイプのしきい値、ストレージレイヤーをクラッシュさせるフィルターなどなど。
All these considerations have to be taken into account by the use case.
これらすべての考慮事項は、ユースケースによって考慮されなければならない。

## Basic structure 基本構造

We can implement structured requests before we expand the use case to accept filters.
フィルタを受け入れるユースケースを拡張する前に、構造化されたリクエストを実装することができる。
We just need a class RoomListRequest that can be initialised without parameters, so let us create the file tests/requests/test_room_list.py and put there a test for this object.
パラメータなしで初期化できるRoomListRequestクラスが必要なので、tests/requests/test_room_list.pyファイルを作成し、このオブジェクトのテストを置きましょう。

While at the moment this request object is basically empty, it will come in handy as soon as we start having parameters for the list use case.
現時点では、このリクエストオブジェクトは基本的に空であるが、リストのユースケースのパラメータを持つようになれば、すぐに便利になるだろう。
The code of the class RoomListRequest is the following
RoomListRequestクラスのコードは以下の通り。

The response object is also very simple since for the moment we just need to return a successful result.
レスポンス・オブジェクトも非常にシンプルで、当面は成功した結果を返せばよいからだ。
Unlike the request, the response is not linked to any particular use case, so the test file can be named tests/test_responses.py
リクエストとは異なり、レスポンスは特定のユースケースにリンクされていないので、テストファイルの名前は tests/test_responses.py になります。

and the actual response object is in the file rentomatic/responses.py
実際のレスポンスオブジェクトはrentomatic/responses.pyにあります。

With these two objects, we just laid the foundations for richer management of input and outputs of the use case, especially in the case of error conditions.
これら2つのオブジェクトによって、ユースケースの入出力をより豊かに管理するための基礎が築かれた。

## Requests and responses in a use case ユースケースにおけるリクエストとレスポンス

Let's implement the request and response objects that we developed into the use case.
ユースケースに開発したリクエストとレスポンスのオブジェクトを実装してみよう。
To do this, we need to change the use case so that it accepts a request and return a response.
そのためには、リクエストを受け取ってレスポンスを返すようにユースケースを変更する必要がある。
The new version of tests/use_cases/test_room_list.py is the following
tests/use_cases/test_room_list.pyの新しいバージョンは以下の通りです。

And the changes in the use case are minimal.
そして、ユースケースの変更は最小限である。
The new version of the file rentomatic/use_cases/room_list.py is the following
rentomatic/use_cases/room_list.pyの新しいバージョンは以下の通りです。

Now we have a standard way to pack input and output values, and the above pattern is valid for every use case we can create.
これで、入力値と出力値をパックする標準的な方法ができ、上記のパターンは、作成できるすべてのユースケースで有効だ。
We are still missing some features, however, because so far requests and responses are not used to perform error management.
というのも、リクエストとレスポンスがエラー管理に使われていないからだ。

## Request validation リクエスト検証

The parameter filters that we want to add to the use case allows the caller to add conditions to narrow the results of the model list operation, using a notation like <attribute>__<operator>.
ユースケースに追加したいパラメータフィルターは、<属性>__<演算子>のような記法を使って、モデルリスト操作の結果を絞り込むための条件を呼び出し側が追加できるようにします。
For example, specifying filters={'price__lt': 100} should return all the results with a price lower than 100.
例えば、filters={'price__lt': 100}と指定すると、100より安い価格の結果がすべて返される。

Since the model Room has many attributes, the number of possible filters is very high.
モデル・ルームには多くの属性があるため、可能なフィルターの数は非常に多くなる。
For simplicity's sake, I will consider the following cases:
簡単のため、以下のケースを考えてみる：

- The attribute code supports only __eq, which finds the room with the specific code if it exists 属性コードは__eqのみをサポートし、特定のコードを持つ部屋が存在する場合、それを見つける。

- The attribute price supports __eq, __lt, and __gt 属性priceは__eq、__lt、__gtをサポートしています。

- All other attributes cannot be used in filters 他のすべての属性は、フィルターでは使用できません。

The core idea here is that requests are customised for use cases, so they can contain the logic that validates the arguments used to instantiate them.
ここでの核となる考え方は、リクエストはユースケース用にカスタマイズされ、そのインスタンス化に使われる引数を検証するロジックを含むことができるということである。
The request is valid or invalid before it reaches the use case, so it is not the responsibility of the latter to check that the input values have proper values or a proper format.
リクエストはユースケースに到達する前に有効か無効かが決まるので、入力値が適切な値や適切なフォーマットを持っているかどうかをチェックするのは後者の責任ではない。

This also means that building a request might result in two different objects, a valid one or an invalid one.
これはまた、リクエストをビルドすると、有効なものと無効なものの2つの異なる オブジェクトが生成される可能性があることを意味する。
For this reason, I decided to split the existing class RoomListRequest into RoomListValidRequest and RoomListInvalidRequest, creating a factory function that returns the proper object.
このため、既存のRoomListRequestクラスをRoomListValidRequestとRoomListInvalidRequestに分割し、適切なオブジェクトを返すファクトリー関数を作ることにした。

The first thing to do is to change the existing tests to use the factory.
最初にすべきことは、既存のテストをファクトリーを使用するように変更することである。

Next, I will test that passing the wrong type of object as filters or that using incorrect keys results in an invalid request
次に、フィルターとして間違ったタイプのオブジェクトを渡したり、間違ったキーを使用すると、無効なリクエストになることをテストしてみる。

Last, I will test the supported and unsupported keys
最後に、サポートされているキーとサポートされていないキーをテストする。

Note that I used the decorator pytest.mark.parametrize to run the same test on multiple values.
複数の値に対して同じテストを実行するためにpytest.mark.parametrizeデコレータを使用したことに注意してください。

Following the TDD approach, adding those tests one by one and writing the code that passes them, I come up with the following code
TDDのアプローチに従い、テストをひとつずつ追加し、それをパスするコードを書くと、次のようなコードになる。

The introduction of the factory makes one use case test fails.
ファクトリーの導入により、あるユースケースのテストが失敗する。
The new version of that test is
そのテストの新しいバージョンは

## Responses and failures 反応と失敗

There is a wide range of errors that can happen while the use case code is executed.
ユースケース・コードの実行中に起こりうるエラーは多岐にわたる。
Validation errors, as we just discussed in the previous section, but also business logic errors or errors that come from the repository layer or other external systems that the use case interfaces with.
前のセクションで説明したバリデーションエラーだけでなく、ビジネスロジックエラーや、ユースケースがインターフェースするリポジトリレイヤーやその他の外部システムから発生するエラーもある。
Whatever the error, the use case shall always return an object with a known structure (the response), so we need a new object that provides good support for different types of failures.
どのようなエラーであっても、ユースケースは常に既知の構造を持つオブジェクト（レスポンス）を返す。

As happened for the requests there is no unique way to provide such an object, and the following code is just one of the possible solutions.
リクエストで起こったように、このようなオブジェクトを提供するユニークな方法はない。
First of all, after some necessary imports, I test that responses have a boolean value
まず、必要なインポートを行った後、レスポンスがブール値を持つかどうかをテストする。

Then I test the structure of responses, checking type and value.
そして、レスポンスの構造をテストし、型と値をチェックする。
ResponseFailure objects should also have an attribute message
ResponseFailureオブジェクトは、属性メッセージも持つ必要があります。

The remaining tests are all about ResponseFailure.
残りのテストはすべてResponseFailureに関するものである。
First, a test to check that it can be initialised with an exception
まず、例外が発生しても初期化できることを確認するためのテスト。

Since we want to be able to build a response directly from an invalid request, getting all the errors contained in the latter, we need to test that case
無効なリクエストから直接レスポンスを生成し、後者に含まれるすべてのエラーを取得できるようにしたいので、次のようなケースをテストする必要がある。

Let's write the classes that make the tests pass
テストをパスさせるクラスを書こう。

Through the method _format_message() we enable the class to accept both string messages and Python exceptions, which is very handy when dealing with external libraries that can raise exceptions we do not know or do not want to manage.
メソッド _format_message() を通して、このクラスが文字列メッセージと Python の例外の両方を受け取れるようにしています。

The error types contained in the class ResponseTypes are very similar to HTTP errors, and this will be useful later when we will return responses from the web framework.
ResponseTypesクラスに含まれるエラー・タイプはHTTPエラーに非常によく似ており、後でウェブ・フレームワークからレスポンスを返すときに役立つ。
PARAMETERS_ERROR signals that something was wrong in the input parameters passed by the request.
PARAMETERS_ERRORは、リクエストから渡された入力パラメータに何か問題があったことを知らせる。
RESOURCE_ERROR signals that the process ended correctly, but the requested resource is not available, for example when reading a specific value from a data storage.
RESOURCE_ERRORは、プロセスは正しく終了したが、要求されたリソースが利用できないことを知らせる。
Last, SYSTEM_ERROR signals that something went wrong with the process itself, and will be used mostly to signal an exception in the Python code.
最後に、SYSTEM_ERRORは、プロセス自体に何か問題が発生したことを知らせるもので、主にPythonのコードで例外を知らせるために使われる。

## Error management in a use case ユースケースにおけるエラー管理

Our implementation of requests and responses is finally complete, so we can now implement the last version of our use case.
リクエストとレスポンスの実装がようやく完了したので、ユースケースの最後のバージョンを実装することができる。
The function room_list_use_case is still missing a proper validation of the incoming request, and is not returning a suitable response in case something went wrong.
room_list_use_case関数は、入力されたリクエストの適切な検証をまだ行っておらず、何か問題が発生した場合に適切なレスポンスを返さない。

The test test_room_list_without_parameters must match the new API, so I added filters=None to assert_called_with
テストtest_room_list_without_parametersは新しいAPIにマッチしなければならないので、assert_called_withにfilters=Noneを追加した。

There are three new tests that we can add to check the behaviour of the use case when filters is not None.
filtersがNoneでない場合のユースケースの動作をチェックするために追加できる新しいテストが3つある。
The first one checks that the value of the key filters in the dictionary used to create the request is actually used when calling the repository.
最初のものは、リクエストを作成するために使われた辞書のキーフィルターの値が、リポジトリを呼び出すときに実際に使われることをチェックします。
These last two tests check the behaviour of the use case when the repository raises an exception or when the request is badly formatted.
最後の2つのテストは、リポジトリが例外を発生させたときや、リクエストが不正なフォーマットだったときのユースケースの振る舞いをチェックします。

Now change the use case to contain the new use case implementation that makes all the tests pass
すべてのテストをパスさせる新しいユースケースの実装を含むように、ユースケースを変更する。

As you can see, the first thing that the use case does is to check if the request is valid.
ご覧のように、このユースケースが最初に行うことは、リクエストが有効かどうかをチェックすることである。
Otherwise, it returns a ResponseFailure built with the same request object.
そうでなければ、同じリクエストオブジェクトで構築されたResponseFailureを返す。
Then the actual business logic is implemented, calling the repository and returning a successful response.
その後、実際のビジネスロジックが実装され、リポジトリを呼び出し、成功したレスポンスを返す。
If something goes wrong in this phase the exception is caught and returned as an aptly formatted ResponseFailure.
このフェーズで何か問題が発生すると、例外がキャッチされ、適切な形式のResponseFailureとして返される。

## Integrating external systems 外部システムとの統合

I want to point out a big problem represented by mocks.
モックに代表される大きな問題を指摘したい。

As we are testing objects using mocks for external systems, like the repository, no tests fail at the moment, but trying to run the Flask development server will certainly return an error.
リポジトリのような外部システムのモックを使ってオブジェクトをテストしているので、今のところテストが失敗することはありませんが、Flask開発サーバーを実行しようとすると確実にエラーが返されます。
As a matter of fact, neither the repository nor the HTTP server are in sync with the new API, but this cannot be shown by unit tests if they are properly written.
実のところ、リポジトリもHTTPサーバーも新しいAPIと同期していないが、ユニットテストが適切に書かれていれば、それを示すことはできない。
This is the reason why we need integration tests, since external systems that rely on a certain version of the API are running only at that point, and this can raise issues that were masked by mocks.
あるバージョンのAPIに依存している外部システムは、その時点でしか動作していないため、モックによって隠されていた問題が発生する可能性があるからだ。

For this simple project, my integration test is represented by the Flask development server, which at this point crashes.
この単純なプロジェクトでは、私の統合テストはFlaskの開発サーバーに代表される。
If you run FLASK_CONFIG="development" flask run and open http://127.0.0.1:5000/rooms with your browser you will get and Internal Server Error, and on the command line this exception
FLASK_CONFIG="development" flask run を実行し、ブラウザで http://127.0.0.1:5000/rooms を開くと Internal Server Error が発生し、コマンドラインでは次のような例外が発生します。

The same error is returned by the CLI interface.
CLIインターフェイスでも同じエラーが返される。
After the introduction of requests and responses we didn't change the REST endpoint, which is one of the connections between the external world and the use case.
リクエストとレスポンスの導入後も、外部とユースケースをつなぐRESTエンドポイントは変えなかった。
Given that the API of the use case changed, we need to change the code of the endpoints that call the use case.
ユースケースのAPIが変更されたので、ユースケースを呼び出すエンドポイントのコードを変更する必要がある。

## The HTTP server HTTP サーバー

As we can see from the exception above the use case is called with the wrong parameters in the REST endpoint.
上の例外からわかるように、このユースケースはRESTエンドポイントの間違ったパラメータで呼び出されている。
The new version of the test is
新バージョンのテストは

The function test_get was already present but has been changed to reflect the use of requests and responses.
test_get関数はすでに存在していたが、リクエストとレスポンスの使用を反映させるために変更された。
The first change is that the use case in the mock has to return a proper response
最初の変更は、モックのユースケースが適切なレスポンスを返さなければならないということだ。

and the second is the assertion on the call of the use case.
そして2つ目は、ユースケースの呼び出しに関するアサーションである。
It should be called with a properly formatted request, but since we can't compare requests, we need a way to look into the call arguments.
しかし、リクエストを比較することはできないので、呼び出しの引数を調べる方法が必要である。
This can be done with
これは

as the use case should receive a request with empty filters as an argument.
というユースケースは、引数として空のフィルタを持つリクエストを受け取るはずである。

The function test_get_with_filters performs the same operation but passing a query string to the URL /rooms, which requires a different assertion
関数test_get_with_filtersは同じ処理を行うが、URL /roomsにクエリー文字列を渡す。

Both the tests pass with a new version of the endpoint room_list
どちらのテストも、新しいバージョンのエンドポイントroom_listでパスする。

Please note that I'm using a variable named request_object here to avoid clashing with the fixture request provided by pytest-flask.
pytest-flaskが提供するフィクスチャリクエストとの衝突を避けるために、ここではrequest_objectという変数を使っていることに注意してください。
While request contains the HTTP request sent to the web framework by the browser, request_object is the request we send to the use case.
requestがブラウザからウェブ・フレームワークに送られるHTTPリクエストを含むのに対して、request_objectはユースケースに送るリクエストです。

## The repository リポジトリ

If we run the Flask development webserver now and try to access the endpoint /rooms, we will get a nice response that says
今、Flaskの開発用Webサーバーを起動して、エンドポイント/roomsにアクセスしようとすると、次のようなレスポンスが返ってきます。

and if you look at the HTTP response[1] you can see an HTTP 500 error, which is exactly the mapping of our SystemError use case error, which in turn signals a Python exception, which is in the message part of the error.
HTTPレスポンス[1]を見ると、HTTP 500エラーが表示されています。これはSystemErrorユースケースエラーに対応するもので、Pythonの例外を知らせるものです。

This error comes from the repository, which has not been migrated to the new API.
このエラーは、新しいAPIに移行されていないリポジトリから発生します。
We need then to change the method list of the class MemRepo to accept the parameter filters and to act accordingly.
そこで、MemRepoクラスのメソッド・リストを変更して、パラメーター・フィルターを受け入れ、それに従って動作するようにする必要がある。
Pay attention to this point.
この点に注意してほしい。
The filters might have been considered part of the business logic and implemented in the use case itself, but we decided to leverage what the storage system can do, so we moved filtering in that external system.
フィルターはビジネス・ロジックの一部とみなされ、ユースケース自体に実装されていたかもしれないが、私たちはストレージ・システムができることを活用することに決めた。
This is a reasonable choice as databases can usually perform filtering and ordering very well.
データベースは通常、フィルタリングと順序付けを非常にうまく実行できるので、これは合理的な選択である。
Even though the in-memory storage we are currently using is not a database, we are preparing to use a real external storage.
現在使っているインメモリ・ストレージはデータベースではないが、本当の外部ストレージを使う準備をしている。

The new version of repository tests is
リポジトリテストの新バージョンは

As you can see, I added many tests.
ご覧の通り、多くのテストを追加した。
One test for each of the four accepted filters (code__eq, price__eq, price__lt, price__gt, see rentomatic/requests/room_list.py), and one final test that tries two different filters at the same time.
4つのフィルタ（code__eq、price__eq、price__lt、price__gt、rentomatic/requests/room_list.pyを参照）それぞれに対して1つのテストと、2つの異なるフィルタを同時に試す最後のテストがあります。

Again, keep in mind that this is the API exposed by the storage, not the one exposed by the use case.
繰り返しになるが、これはストレージが公開するAPIであって、ユースケースが公開するAPIではないことに留意してほしい。
The fact that the two match is a design decision, but your mileage may vary.
この2つが一致するのはデザイン上の決定事項だが、あなたの感覚は異なるかもしれない。

The new version of the repository is
リポジトリの新しいバージョンは

At this point, you can start the Flask development webserver with FLASK_CONFIG="development" flask run, and get the list of all your rooms at http://localhost:5000/rooms.
この時点で、FLASK_CONFIG="development" flask runでFlaskの開発用Webサーバーを起動し、http://localhost:5000/rooms、すべての部屋のリストを取得することができます。
You can also use filters in the URL, like http://localhost:5000/rooms?filter_code__eq=f853578c-fc0f-4e65-81b8-566c5dffa35a which returns the room with the given code or http://localhost:5000/rooms?filter_price__lt=50 which returns all the rooms with a price less than 50.
http://localhost:5000/rooms?filter_code__eq=f853578c-fc0f-4e65-81b8-566c5dffa35a、指定されたコードを持つ部屋を返す、またはhttp://localhost:5000/rooms?filter_price__lt=50、50未満の価格のすべての部屋を返すように、URLでフィルタを使用することもできます。

## The CLI CLI

At this point fixing the CLI is extremely simple, as we just need to imitate what we did for the HTTP server, only without considering the filters as they were not part of the command line tool.
この時点でCLIを修正するのは非常に簡単で、HTTPサーバーに対して行ったことを真似すればよい。

We now have a very robust system to manage input validation and error conditions, and it is generic enough to be used with any possible use case.
私たちは今、入力検証とエラー条件を管理するための非常に堅牢なシステムを手に入れた。
Obviously, we are free to add new types of errors to increase the granularity with which we manage failures, but the present version already covers everything that can happen inside a use case.
もちろん、失敗を管理する粒度を上げるために新しいタイプのエラーを追加することは自由だが、現在のバージョンはすでにユースケース内で起こりうるすべてのことをカバーしている。

In the next chapter, we will have a look at repositories based on real database engines, showing how to test external systems with integration tests, using PostgreSQL as a database.
次の章では、PostgreSQLをデータベースとして使用し、統合テストで外部システムをテストする方法を紹介しながら、実際のデータベースエンジンに基づいたリポジトリを見ていきます。
In a later chapter I will show how the clean architecture allows us to switch very easily between different external systems, moving the system to MongoDB.
後の章では、このクリーンなアーキテクチャのおかげで、システムをMongoDBに移行し、異なる外部システム間で非常に簡単に切り替えられることを紹介する。