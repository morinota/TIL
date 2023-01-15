# Chapter 5. TDD in High Gear and Low Gear 第5章 ハイギアとローギアでのTDD

We’ve introduced the service layer to capture some of the additional orchestration responsibilities we need from a working application.
サービスレイヤーは、アプリケーションに必要なオーケストレーションの責任を果たすために導入されました。
The service layer helps us clearly define our use cases and the workflow for each: what we need to get from our repositories, what pre-checks and current state validation we should do, and what we save at the end.
サービス層は、ユースケースとそれぞれのワークフローを明確に定義するのに役立ちます。リポジトリから取得する必要があるもの、事前チェックと現在の状態の検証を行うべきもの、そして最後に保存するものです。

But currently, many of our unit tests operate at a lower level, acting directly on the model.
しかし現在、多くのユニットテストはより低いレベルで動作し、モデルに対して直接作用しています。
In this chapter we’ll discuss the trade-offs involved in moving those tests up to the service-layer level, and some more general testing guidelines.
この章では、これらのテストをサービスレイヤーに移行する際のトレードオフと、より一般的なテストのガイドラインを説明します。

- HARRY SAYS: SEEING A TEST PYRAMID IN ACTION WAS A LIGHT-BULB MOMENT harry says: テスト用ピラミッドが実際に動いているのを見たときは、とても衝撃的でした。

- Here are a few words from Harry directly: ハリーさんから直接いただいたお言葉をご紹介します。

- I was initially skeptical of all Bob’s architectural patterns, but seeing an actual test pyramid made me a convert. 最初はボブの建築パターンに懐疑的でしたが、実際のテストピラミッドを見て、改心しました。

- Once you implement domain modeling and the service layer, you really actually can get to a stage where unit tests outnumber integration and end-to-end tests by an order of magnitude. Having worked in places where the E2E test build would take hours (“wait ‘til tomorrow,” essentially), I can’t tell you what a difference it makes to be able to run all your tests in minutes or seconds. ドメインモデリングとサービスレイヤーを実装すれば、ユニットテストがインテグレーションテストやエンドツーエンドテストよりも桁違いに多くなる段階に実際に到達することができます。 E2Eテストのビルドに何時間もかかるような場所で働いてきた私にとって、数分から数秒ですべてのテストを実行できるようになることが、どれほど大きな違いであるかは、想像もつかないほどです。

- Read on for some guidelines on how to decide what kinds of tests to write and at which level. The high gear versus low gear way of thinking really changed my testing life. どのような種類のテストを、どのレベルで書くべきかを決定するためのガイドラインについては、こちらをお読みください。 ハイギアとローギアの考え方は、私のテスト人生を大きく変えました。

## How Is Our Test Pyramid Looking? How Is Our Test Pyramid Looking?

Let’s see what this move to using a service layer, with its own service-layer tests, does to our test pyramid:
サービスレイヤーを使用し、サービスレイヤーのテストを使用することで、テストピラミッドがどうなるかを見てみましょう。

Counting types of tests
テストの種類をカウントする

```
$ grep -c test_ test_*.py
tests/unit/test_allocate.py:4
tests/unit/test_batches.py:8
tests/unit/test_services.py:3
tests/integration/test_orm.py:6
tests/integration/test_repository.py:2
tests/e2e/test_api.py:2
```

Not bad!
悪くない！
We have 15 unit tests, 8 integration tests, and just 2 end-to-end tests.
ユニットテストが15個、統合テストが8個、そしてエンドツーエンドテストが2個だけです。
That’s already a healthy-looking test pyramid.
これはすでに健康的なテストピラミッドです。

## Should Domain Layer Tests Move to the Service Layer? ドメイン層のテストはサービス層に移行すべきなのか？

Let’s see what happens if we take this a step further.
これをさらに一歩進めるとどうなるか見てみましょう。
Since we can test our software against the service layer, we don’t really need tests for the domain model anymore.
サービス層に対してソフトウェアをテストできるようになったので、 ドメインモデルに対するテストはもう必要ありません。
Instead, we could rewrite all of the domain-level tests from Chapter 1 in terms of the service layer:
そのかわり、第1章でのドメインレベルのテストをすべてサービス層の観点で書き直すことができます。

Rewriting a domain test at the service layer (tests
サービス層でドメインテストを書き換える（テスト

```python
# domain-layer test:
def test_prefers_current_stock_batches_to_shipments():
in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
line = OrderLine("oref", "RETRO-CLOCK", 10)
allocate(line, [in_stock_batch, shipment_batch])
assert in_stock_batch.available_quantity == 90
assert shipment_batch.available_quantity == 100
# service-layer test:
def test_prefers_warehouse_batches_to_shipments():
in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
repo = FakeRepository([in_stock_batch, shipment_batch])
session = FakeSession()
line = OrderLine('oref', "RETRO-CLOCK", 10)
services.allocate(line, repo, session)
assert in_stock_batch.available_quantity == 90
assert shipment_batch.available_quantity == 100
```

Why would we want to do that?
なぜ、そんなことをしたいのだろう？

Tests are supposed to help us change our system fearlessly, but often we see teams writing too many tests against their domain model.
しかし、しばしば、ドメインモデルに対してあまりにも多くのテストを書いているチームを見かけます。
This causes problems when they come to change their codebase and find that they need to update tens or even hundreds of unit tests.
これは、コードベースを変更する際に、数十から数百のユニットテストを更新する必要があることに気づいたときに、問題を引き起こします。

This makes sense if you stop to think about the purpose of automated tests.
これは、自動テストの目的について考えるのを止めれば、理にかなっています。
We use tests to enforce that a property of the system doesn’t change while we’re working.
私たちは、作業中にシステムのプロパティが変更されないようにするためにテストを使用します。
We use tests to check that the API continues to return 200, that the database session continues to commit, and that orders are still being allocated.
API が 200 を返し続けること、データベースセッションがコミットし続けること、そして注文がまだ割り当てられていることを確認するためにテストを使用します。

If we accidentally change one of those behaviors, our tests will break.
もしこれらの動作のいずれかを誤って変更してしまうと、テストは失敗してしまいます。
The flip side, though, is that if we want to change the design of our code, any tests relying directly on that code will also fail.
逆に言えば、もしコードの設計を変えたいのなら、そのコードに直接依存しているテストも失敗してしまうということです。

As we get further into the book, you’ll see how the service layer forms an API for our system that we can drive in multiple ways.
この本をさらに読み進めると、サービスレイヤーがどのようにシステムのためのAPIを形成し、複数の方法で駆動できるかがわかります。
Testing against this API reduces the amount of code that we need to change when we refactor our domain model.
この API に対してテストを行うことで、ドメインモデルをリファクタリングする際に変更する必要があるコードの量を減らすことができます。
If we restrict ourselves to testing only against the service layer, we won’t have any tests that directly interact with “private” methods or attributes on our model objects, which leaves us freer to refactor them.
サービス層に対するテストに限定すると、モデルオブジェクトの "private" なメソッドや属性と直接やりとりするテストがなくなるので、 その分リファクタリングがしやすくなります。

- TIP ヒント

- Every line of code that we put in a test is like a blob of glue, holding the system in a particular shape. The more low-level tests we have, the harder it will be to change things. テストに入れるコードの一行一行は、接着剤の塊のようなもので、システムを特定の形に保持するものです。 低レベルのテストが多ければ多いほど、物事を変更するのは難しくなります。

## On Deciding What Kind of Tests to Write どのようなテストを書くべきかを決めるにあたって

You might be asking yourself, “Should I rewrite all my unit tests, then?
あなたは、「では、ユニットテストを全部書き直した方がいいのか？
Is it wrong to write tests against the domain model?”
ドメインモデルに対してテストを書くのは間違っているのでしょうか?" といった疑問を持つかもしれません。
To answer those questions, it’s important to understand the trade-off between coupling and design feedback (see Figure 5-1).
これらの質問に答えるには、結合と設計のフィードバックのトレードオフを理解することが重要です（図5-1参照）。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0501.png)

Extreme programming (XP) exhorts us to “listen to the code.”
エクストリームプログラミング（XP）では、"コードに耳を傾ける "ことを勧めています。
When we’re writing tests, we might find that the code is hard to use or notice a code smell.
テストを書いているとき、コードが使いにくいと感じたり、コードの匂いに気づいたりすることがあります。
This is a trigger for us to refactor, and to reconsider our design.
これは、リファクタリングや設計を見直すきっかけになります。

We only get that feedback, though, when we’re working closely with the target code.
しかし、そのようなフィードバックが得られるのは、ターゲットコードと密接に連携しているときだけです。
A test for the HTTP API tells us nothing about the fine-grained design of our objects, because it sits at a much higher level of abstraction.
HTTP API のテストは、私たちのオブジェクトの詳細な設計について何も教えてくれません。なぜなら、それははるかに高い抽象度のところにあるからです。

On the other hand, we can rewrite our entire application and, so long as we don’t change the URLs or request formats, our HTTP tests will continue to pass.
一方、アプリケーション全体を書き換えても、URL やリクエストのフォーマットを変更しない限り、HTTP テストは合格し続けることができます。
This gives us confidence that large-scale changes, like changing the database schema, haven’t broken our code.
これは、データベースのスキーマを変更するような大規模な変更でも、コードが壊れないという確信を与えてくれます。

At the other end of the spectrum, the tests we wrote in Chapter 1 helped us to flesh out our understanding of the objects we need.
もう一方では、第1章で書いたテストが、必要なオブジェクトの理解を深めるのに役立った。
The tests guided us to a design that makes sense and reads in the domain language.
テストは、私たちを理にかなった設計に導き、ドメイン言語で読めるようにします。
When our tests read in the domain language, we feel comfortable that our code matches our intuition about the problem we’re trying to solve.
テストがドメイン言語で読めるようになると、私たちは自分のコードが、解決しようとしている問題についての直感と一致していることに安心感を覚えます。

Because the tests are written in the domain language, they act as living documentation for our model.
テストはドメイン言語で書かれているため、私たちのモデルの生きたドキュメントとして機能します。
A new team member can read these tests to quickly understand how the system works and how the core concepts interrelate.
新しいチームメンバーは、これらのテストを読むことで、システムがどのように動作し、コアコンセプトがどのように関連しているのかを素早く理解することができます。

We often “sketch” new behaviors by writing tests at this level to see how the code might look.
私たちはしばしば、このレベルでテストを書いて新しい動作を「スケッチ」し、 コードがどのように見えるかを確認します。
When we want to improve the design of the code, though, we will need to replace or delete these tests, because they are tightly coupled to a particular implementation.
しかし、コードの設計を改善する際には、これらのテストを置き換えたり削除したりする必要があります。

## High and Low Gear 

Most of the time, when we are adding a new feature or fixing a bug, we don’t need to make extensive changes to the domain model.
多くの場合、新しい機能を追加したり、バグを修正したりするときには、ドメインモデルに大きな変更を加える必要はありません。
In these cases, we prefer to write tests against services because of the lower coupling and higher coverage.
このような場合、サービスに対してテストを書く方が、結合度が低く、カバレッジが高いので、好ましいと言えます。

For example, when writing an `add_stock` function or a `cancel_order` feature, we can work more quickly and with less coupling by writing tests against the service layer.
例えば、`add_stock`関数や`cancel_order`機能を書くとき、サービス層に対してテストを書くことで、より速く、より少ない結合で作業することができます。

When starting a new project or when hitting a particularly gnarly problem, we will drop back down to writing tests against the domain model so we get better feedback and executable documentation of our intent.
新しいプロジェクトを始めるときや、特に厄介な問題にぶつかったときは、ドメインモデルに対してテストを書くところまで落とし、より良いフィードバックと実行可能な意図を示す文書を得ることができるようにします。

The metaphor we use is that of shifting gears.
私たちは、ギアチェンジに例えています。
When starting a journey, the bicycle needs to be in a low gear so that it can overcome inertia.
旅立ちのとき、自転車は慣性を克服するために低いギアで走る必要があります。
Once we’re off and running, we can go faster and more efficiently by changing into a high gear; but if we suddenly encounter a steep hill or are forced to slow down by a hazard, we again drop down to a low gear until we can pick up speed again.
しかし、急な坂道や障害物によって減速を余儀なくされた場合は、再び低速のギアを入れて、スピードを取り戻します。

## Fully Decoupling the Service-Layer Tests from the Domain サービスレイヤーのテストをドメインから完全に切り離す

We still have direct dependencies on the domain in our service-layer tests, because we use domain objects to set up our test data and to invoke our service-layer functions.
サービスレイヤーのテストでは、ドメインに直接依存しています。なぜなら、ドメインオブジェクトを使ってテストデータをセットアップし、サービスレイヤーの関数を呼び出すからです。

To have a service layer that’s fully decoupled from the domain, we need to rewrite its API to work in terms of primitives.
ドメインから完全に切り離されたサービス層を作るには、そのAPIをプリミティブで動作するように書き換える必要があります。

Our service layer currently takes an `OrderLine` domain object:
サービス層は現在、 `OrderLine` ドメインオブジェクトを受け取っている。

Before: allocate takes a domain object (service_layer
Before: allocate はドメインオブジェクト（service_layer）を取る。

```python
def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
```

How would it look if its parameters were all primitive types?
もし、パラメータがすべてプリミティブ型だったら、どのように見えるでしょうか？

After: allocate takes strings and ints (service_layer
後: 文字列とint型（サービスレイヤー）を確保する。

```python
def allocate(
orderid: str, sku: str, qty: int, repo: AbstractRepository, session
) -> str:
```

We rewrite the tests in those terms as well:
テストもそのような観点で書き換えています。

Tests now use primitives in function call (tests
関数呼び出しでプリミティブを使用するようになった（tests

```python
def test_returns_allocation():
batch = model.Batch("batch1", "COMPLICATED-LAMP", 100, eta=None)
repo = FakeRepository([batch])
result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, FakeSession())
assert result == "batch1"
```

But our tests still depend on the domain, because we still manually instantiate `Batch` objects.
しかし、私たちのテストはまだドメインに依存しています。なぜなら、私たちはまだ `Batch` オブジェクトを手作業でインスタンス化しているからです。
So, if one day we decide to massively refactor how our `Batch` model works, we’ll have to change a bunch of tests.
もし、ある日 `Batch` モデルの動作方法を大幅にリファクタリングすることになったら、たくさんのテストを変更しなければならなくなります。

### Mitigation: Keep All Domain Dependencies in Fixture Functions 軽減策 すべてのドメイン依存をフィクスチャ関数に保持する

We could at least abstract that out to a helper function or a fixture in our tests.
少なくとも、ヘルパー関数やテストのフィクスチャに抽象化することができます。
Here’s one way you could do that, adding a factory function on FakeRepository:
ここでは、FakeRepositoryにファクトリー関数を追加することでそれを実現する方法を紹介します。

Factory functions for fixtures are one possibility (tests
フィクスチャのファクトリー機能は、一つの可能性です（テスト

```python
class FakeRepository(set):
@staticmethod
def for_batch(ref, sku, qty, eta=None):
return FakeRepository([
model.Batch(ref, sku, qty, eta),
])
...
def test_returns_allocation():
repo = FakeRepository.for_batch("batch1", "COMPLICATED-LAMP", 100, eta=None)
result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, FakeSession())
assert result == "batch1"
```

At least that would move all of our tests’ dependencies on the domain into one place.
少なくとも、ドメインに依存しているテストのすべてを1つの場所に移動させることができます。

### Adding a Missing Service 欠落しているサービスの追加

We could go one step further, though.
しかし、もう一歩踏み込むことができる。
If we had a service to add stock, we could use that and make our service-layer tests fully expressed in terms of the service layer’s official use cases, removing all dependencies on the domain:
もし、在庫を追加するサービスがあれば、それを使って、サービスレイヤーのテストを、サービスレイヤーの公式ユースケースの観点から完全に表現し、ドメインへの依存をすべて取り除くことができるだろう。

Test for new add_batch service (tests
新サービス「add_batch」のテスト（テスト

```python
def test_add_batch():
repo, session = FakeRepository([]), FakeSession()
services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, repo, session)
assert repo.get("b1") is not None
assert session.committed
```

- TIP ヒント

- In general, if you find yourself needing to do domain-layer stuff directly in your service-layer tests, it may be an indication that your service layer is incomplete. 一般的に、もしあなたがサービス層のテストでドメイン層のものを直接行う必要があると感じるなら、それはあなたのサービス層が不完全であることを示しているのかもしれません。

And the implementation is just two lines:
しかも、実装はたった2行。

A new service for add_batch (service_layer
add_batch の新サービス(service_layer)

```python
def add_batch(
ref: str, sku: str, qty: int, eta: Optional[date],
repo: AbstractRepository, session,
):
repo.add(model.Batch(ref, sku, qty, eta))
session.commit()
def allocate(
orderid: str, sku: str, qty: int, repo: AbstractRepository, session
) -> str:
...
```

- NOTE 注

- Should you write a new service just because it would help remove dependencies from your tests? Probably not. But in this case, we almost definitely would need an add_batch service one day anyway. テストから依存性を取り除くのに役立つからと言って、新しいサービスを書くべきでしょうか？ おそらくそうではないでしょう。 しかし、この場合はいずれにせよ add_batch サービスが必要になることは間違いありません。

That now allows us to rewrite all of our service-layer tests purely in terms of the services themselves, using only primitives, and without any dependencies on the model:
これで、サービス層のテストを、純粋にサービスそのものの観点で、プリミティブだけを使い、モデルに一切依存せずに書き直すことができるようになりました。

Services tests now use only services (tests
サービステストがサービスのみを使用するようになった（テスト

```python
def test_allocate_returns_allocation():
repo, session = FakeRepository([]), FakeSession()
services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, repo, session)
result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, session)
assert result == "batch1"
def test_allocate_errors_for_invalid_sku():
repo, session = FakeRepository([]), FakeSession()
services.add_batch("b1", "AREALSKU", 100, None, repo, session)
with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
services.allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())
```

This is a really nice place to be in.
これは本当にいいところです。
Our service-layer tests depend on only the service layer itself, leaving us completely free to refactor the model as we see fit.
サービスレイヤーのテストはサービスレイヤー自体にのみ依存し、私たちは自由にモデルをリファクタリングすることができます。

## Carrying the Improvement Through to the E2E Tests 改良を E2E テストに持ち込む

In the same way that adding `add_batch` helped decouple our service-layer tests from the model, adding an API endpoint to add a batch would remove the need for the ugly `add_stock` fixture, and our E2E tests could be free of those hardcoded SQL queries and the direct dependency on the database.
add_batch` を追加することでサービスレイヤーのテストをモデルから切り離すことができたのと同じように、バッチを追加する API エンドポイントを追加すれば、醜い `add_stock` フィクスチャが不要になり、E2E テストからハードコードされた SQL クエリとデータベースへの直接依存が無くなります。

Thanks to our service function, adding the endpoint is easy, with just a little JSON wrangling and a single function call required:
サービス関数のおかげで、エンドポイントの追加は簡単で、ほんの少しのJSONの操作と1回の関数呼び出しが必要なだけです。

API for adding a batch (entrypoints
一括で追加するためのAPI（エントリポイント

```python
@app.route("/add_batch", methods=['POST'])
def add_batch():
session = get_session()
repo = repository.SqlAlchemyRepository(session)
eta = request.json['eta']
if eta is not None:
eta = datetime.fromisoformat(eta).date()
services.add_batch(
request.json['ref'], request.json['sku'], request.json['qty'], eta,
repo, session
)
return 'OK', 201
```

- NOTE 注

- Are you thinking to yourself, POST to /add_batch? That’s not very RESTful! You’re quite right. We’re being happily sloppy, but if you’d like to make it all more RESTy, maybe a POST to /batches, then knock yourself out! Because Flask is a thin adapter, it’ll be easy. See the next sidebar. 自分に言い聞かせているのか、POST to

And our hardcoded SQL queries from conftest.py get replaced with some API calls, meaning the API tests have no dependencies other than the API, which is also nice:
そして、conftest.pyからハードコードされたSQLクエリは、いくつかのAPIコールで置き換えられます。つまり、APIテストはAPI以外の依存性を持たないので、これもまた良いことです。

API tests can now add their own batches (tests
APIテストが独自のバッチを追加できるようになりました（テスト

```python
def post_to_add_batch(ref, sku, qty, eta):
url = config.get_api_url()
r = requests.post(
f'{url}/add_batch',
json={'ref': ref, 'sku': sku, 'qty': qty, 'eta': eta}
)
assert r.status_code == 201
@pytest.mark.usefixtures('postgres_db')
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_201_and_allocated_batch():
sku, othersku = random_sku(), random_sku('other')
earlybatch = random_batchref(1)
laterbatch = random_batchref(2)
otherbatch = random_batchref(3)
post_to_add_batch(laterbatch, sku, 100, '2011-01-02')
post_to_add_batch(earlybatch, sku, 100, '2011-01-01')
post_to_add_batch(otherbatch, othersku, 100, None)
data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}
url = config.get_api_url()
r = requests.post(f'{url}/allocate', json=data)
assert r.status_code == 201
assert r.json()['batchref'] == earlybatch
```

## Wrap-Up まとめ

Once you have a service layer in place, you really can move the majority of your test coverage to unit tests and develop a healthy test pyramid.
サービスレイヤーが出来上がると、テストカバレッジの大部分をユニットテストに移行し、健全なテストピラミッドを構築することができます。

- RECAP: RULES OF THUMB FOR DIFFERENT TYPES OF TEST まとめ：テストタイプ別の経験則

- Aim for one end-to-end test per feature 1機能につき1回のエンドツーエンドテストを目標とする

- This might be written against an HTTP API, for example. The objective is to demonstrate that the feature works, and that all the moving parts are glued together correctly. 例えば、HTTPのAPIに対して書かれるかもしれません。 目的は、その機能が動作すること、そしてすべての可動部品が正しく組み合わされていることを実証することです。

- Write the bulk of your tests against the service layer サービス層に対してテストの大部分を記述する

- These edge-to-edge tests offer a good trade-off between coverage, runtime, and efficiency. Each test tends to cover one code path of a feature and use fakes for I/O. This is the place to exhaustively cover all the edge cases and the ins and outs of your business logic.1 これらのエッジ・トゥ・エッジテストは、カバレッジ、ランタイム、効率の間の良いトレードオフを提供します。 各テストは、ある機能の 1 つのコードパスをカバーし、そのコードパスに対して I

- Maintain a small core of tests written against your domain model ドメインモデルに対して記述されたテストの小さなコアを維持する。

- These tests have highly focused coverage and are more brittle, but they have the highest feedback. Don’t be afraid to delete these tests if the functionality is later covered by tests at the service layer. これらのテストはカバレッジが非常に狭く、より脆いものですが、最高のフィードバックが得られます。 もしその機能がサービスレイヤのテストによってカバーされるなら、 これらのテストを削除することを恐れないでください。

- Error handling counts as a feature エラー処理も機能としてカウント

- Ideally, your application will be structured such that all errors that bubble up to your entrypoints (e.g., Flask) are handled in the same way. This means you need to test only the happy path for each feature, and to reserve one end-to-end test for all unhappy paths (and many unhappy path unit tests, of course). 理想を言えば、あなたのアプリケーションは、エントリポイント (例えば Flask) に上がってくるすべてのエラーが同じように処理されるような構造になっていることでしょう。 これは、各機能のハッピーパスだけをテストし、すべてのアンハッピーパスのために1つのエンドツーエンドテストを予約する必要があることを意味します（そしてもちろん、多くのアンハッピーパスのユニットテストも）。

A few things will help along the way:
その過程で、いくつかのことが役に立ちます。

- Express your service layer in terms of primitives rather than domain objects. サービス層をドメインオブジェクトではなく、プリミティブで表現する。

- In an ideal world, you’ll have all the services you need to be able to test entirely against the service layer, rather than hacking state via repositories or the database. This pays off in your end-to-end tests as well. 理想的な世界では、リポジトリやデータベースを介して状態をハックするのではなく、サービス層に対して完全にテストを行うことができるように、必要なすべてのサービスが用意されていることでしょう。 これは、エンドツーエンドのテストでも同じように効果があります。

Onto the next chapter!
次の章へ!

1. A valid concern about writing tests at a higher level is that it can lead to combinatorial explosion for more complex use cases. In these cases, dropping down to lower-level unit tests of the various collaborating domain objects can be useful. But see also Chapter 8 and “Optionally: Unit Testing Event Handlers in Isolation with a Fake Message Bus”. より高いレベルでテストを書くことの有効な懸念は、より複雑なユースケースにおいて組合せ爆発につながる可能性があることです。 このような場合は、さまざまなドメインオブジェクトを連携させた低レベルのユニットテストに落とし込むと便利です。 しかし、第8章と「オプション」も参照してください。 偽のメッセージバスを使ったイベントハンドラの単体テスト" も参照してください。