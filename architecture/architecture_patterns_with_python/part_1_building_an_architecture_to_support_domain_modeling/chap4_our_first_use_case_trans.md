# Chapter 4. Our First Use Case: Flask API and Service Layer 第4章 私たちの最初のユースケース。 Flask APIとサービスレイヤー

Back to our allocations project!
アロケーションのプロジェクトに戻ろう
Figure 4-1 shows the point we reached at the end of Chapter 2, which covered the Repository pattern.
図4-1は、Repositoryパターンを扱った第2章の終わりで到達した地点です。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0401.png)

In this chapter, we discuss the differences between orchestration logic, business logic, and interfacing code, and we introduce the Service Layer pattern to take care of orchestrating our workflows and defining the use cases of our system.
この章では、オーケストレーションロジック、ビジネスロジック、インターフェイスコードの違いについて説明し、ワークフローのオーケストレーションとシステムのユースケースを定義するためのService Layerパターンを紹介します。

We’ll also discuss testing: by combining the Service Layer with our repository abstraction over the database, we’re able to write fast tests, not just of our domain model but of the entire workflow for a use case.
サービスレイヤーとデータベースを抽象化したリポジトリを組み合わせることで、ドメインモデルだけでなく、ユースケースのワークフロー全体のテストを高速に記述することができます。

Figure 4-2 shows what we’re aiming for: we’re going to add a Flask API that will talk to the service layer, which will serve as the entrypoint to our domain model.
図4-2は、私たちが目指しているものを示しています。サービスレイヤーと対話するFlask APIを追加し、ドメインモデルへのエントリポイントとして機能させるつもりです。
Because our service layer depends on the `AbstractRepository`, we can unit test it by using `FakeRepository` but run our production code using `SqlAlchemyRepository`.
サービスレイヤーは `AbstractRepository` に依存しているので、 `FakeRepository` を使ってユニットテストを行い、 `SqlAlchemyRepository` を使ってプロダクションコードを実行することができます。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0402.png)

In our diagrams, we are using the convention that new components are highlighted with bold text
この図では、新しいコンポーネントは太字でハイライトされるという慣習を使用しています。

TIP
ヒント

The code for this chapter is in the chapter_04_service_layer branch on GitHub:
この章のコードは、GitHubのchapter_04_service_layerブランチにあります。

## Connecting Our Application to the Real World 私たちのアプリケーションを実世界につなげるために

Like any good agile team, we’re hustling to try to get an MVP out and in front of the users to start gathering feedback.
他の優れたアジャイルチームと同様、私たちはMVPを発表し、ユーザーの前でフィードバックを集め始めようと奮闘しているところです。
We have the core of our domain model and the domain service we need to allocate orders, and we have the repository interface for permanent storage.
私たちは、ドメインモデルのコアと、注文を割り当てるために必要なドメインサービス、そして永久保存のためのリポジトリインターフェースを手に入れました。

Let’s plug all the moving parts together as quickly as we can and then refactor toward a cleaner architecture.
すべての可動部品をできるだけ早く接続し、よりクリーンなアーキテクチャに向けてリファクタリングしていきましょう。
Here’s our plan:
これが私たちの計画です。

1. Use Flask to put an API endpoint in front of our `allocate` domain service. Wire up the database session and our repository. Test it with an end-to-end test and some quick-and-dirty SQL to prepare test data. Flaskを使って、APIエンドポイントを `allocate` ドメインサービスの前に配置します。 データベースセッションとリポジトリの配線。 エンドツーエンドテストと、テストデータを準備するためのクイックアンドダーティなSQLでテストします。

2. Refactor out a service layer that can serve as an abstraction to capture the use case and that will sit between Flask and our domain model. Build some service-layer tests and show how they can use `FakeRepository`. ユースケースを抽象化し、Flaskとドメインモデルの間に位置するサービスレイヤーをリファクタリングする。 サービスレイヤーのテストをいくつか作って、それらがどのように `FakeRepository` を使うことができるかを示す。

3. Experiment with different types of parameters for our service layer functions; show that using primitive data types allows the service layer’s clients (our tests and our Flask API) to be decoupled from the model layer. プリミティブなデータ型を使うことで、サービス層のクライアント（テストとFlask API）をモデル層から切り離すことができることを示す。

## A First End-to-End Test 最初のエンド・ツー・エンド・テスト

No one is interested in getting into a long terminology debate about what counts as an end-to-end (E2E) test versus a functional test versus an acceptance test versus an integration test versus a unit test.
エンドツーエンドテスト、機能テスト、受け入れテスト、統合テスト、単体テストなど、何をテストと呼ぶかについての長い専門用語の議論には誰も興味がないでしょう。
Different projects need different combinations of tests, and we’ve seen perfectly successful projects just split things into “fast tests” and “slow tests.”
プロジェクトによって必要なテストの組み合わせは異なるし、完全に成功したプロジェクトでも、「速いテスト」と「遅いテスト」に分けているのを見たことがある。

For now, we want to write one or maybe two tests that are going to exercise a “real” API endpoint (using HTTP) and talk to a real database.
今のところ、(HTTP を使って) 「本物の」 API エンドポイントを実行し、本物のデータベースと対話するテストを 1 つか 2 つ書きたいと考えています。
Let’s call them end-to-end tests because it’s one of the most self-explanatory names.
最も分かりやすい名前の一つなので、これをエンドツーエンドテストと呼ぶことにしましょう。

The following shows a first cut:
以下はファーストカットの様子です。

A first API test (test_api.py)
最初のAPIテスト(test_api.py)

```python
@pytest.mark.usefixtures('restart_api')
def test_api_returns_allocation(add_stock):
sku, othersku = random_sku(), random_sku('other')  1
earlybatch = random_batchref(1)
laterbatch = random_batchref(2)
otherbatch = random_batchref(3)
add_stock([  2
(laterbatch, sku, 100, '2011-01-02'),
(earlybatch, sku, 100, '2011-01-01'),
(otherbatch, othersku, 100, None),
])
data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}
url = config.get_api_url()  3
r = requests.post(f'{url}/allocate', json=data)
assert r.status_code == 201
assert r.json()['batchref'] == earlybatch
```

1. random_sku(), random_batchref(), and so on are little helper functions that generate randomized characters by using the uuid module. Because we’re running against an actual database now, this is one way to prevent various tests and runs from interfering with each other. random_sku()、random_batchref() などは、uuid モジュールを使ってランダムな文字を生成する小さなヘルパー関数です。 私たちは今、実際のデータベースに対して実行しているので、これは様々なテストや実行が互いに干渉し合うのを防ぐための一つの方法です。

2. add_stock is a helper fixture that just hides away the details of manually inserting rows into the database using SQL. We’ll show a nicer way of doing this later in the chapter. add_stock はヘルパーフィクスチャで、SQL を使って手動でデータベースに行を挿入する詳細を隠しているだけです。 この章の後半で、これを行うより素敵な方法を紹介します。

3. config.py is a module in which we keep configuration information. config.py は、設定情報を保持するモジュールです。

Everyone solves these problems in different ways, but you’re going to need some way of spinning up Flask, possibly in a container, and of talking to a Postgres database.
この問題を解決する方法は人それぞれですが、Flaskを起動し、おそらくはコンテナで、Postgresデータベースと通信する方法が必要でしょう。
If you want to see how we did it, check out Appendix B.
私たちがどのように行ったか見たい場合は、付録Bをチェックしてください。

## The Straightforward Implementation ストレートな実装

Implementing things in the most obvious way, you might get something like this:
最もわかりやすい方法で実装すると、次のようになります。

First cut of Flask app (flask_app.py)
Flaskアプリのファーストカット(flask_app.py)

```python
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
import model
import orm
import repository
orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
session = get_session()
batches = repository.SqlAlchemyRepository(session).list()
line = model.OrderLine(
request.json['orderid'],
request.json['sku'],
request.json['qty'],
)
batchref = model.allocate(line, batches)
return jsonify({'batchref': batchref}), 201
```

So far, so good.
ここまではいいんです。
No need for too much more of your “architecture astronaut” nonsense, Bob and Harry, you may be thinking.
ボブやハリーは、もう「建築宇宙飛行士」なんていう戯言は必要ない、と思っているかもしれませんね。

But hang on a minute—there’s no commit.
しかし、ちょっと待てよ、コミットはしていない。
We’re not actually saving our allocation to the database.
実際にデータベースにアロケーションを保存しているわけではありません。
Now we need a second test, either one that will inspect the database state after (not very black-boxy), or maybe one that checks that we can’t allocate a second line if a first should have already depleted the batch:
今、私たちは2つ目のテストを必要としています。それは、データベースの状態を後で検査するもの（あまりブラックボックス的ではありませんが）か、あるいは、最初の行がすでにバッチを使い果たしている場合に2番目の行を割り当てられないことをチェックするものです。

Test allocations are persisted (test_api.py)
テスト用のアロケーションを永続化した(test_api.py)

```python
@pytest.mark.usefixtures('restart_api')
def test_allocations_are_persisted(add_stock):
sku = random_sku()
batch1, batch2 = random_batchref(1), random_batchref(2)
order1, order2 = random_orderid(1), random_orderid(2)
add_stock([
(batch1, sku, 10, '2011-01-01'),
(batch2, sku, 10, '2011-01-02'),
])
line1 = {'orderid': order1, 'sku': sku, 'qty': 10}
line2 = {'orderid': order2, 'sku': sku, 'qty': 10}
url = config.get_api_url()
# first order uses up all stock in batch 1
r = requests.post(f'{url}/allocate', json=line1)
assert r.status_code == 201
assert r.json()['batchref'] == batch1
# second order should go to batch 2
r = requests.post(f'{url}/allocate', json=line2)
assert r.status_code == 201
assert r.json()['batchref'] == batch2
```

Not quite so lovely, but that will force us to add the commit.
それほど素敵なものではありませんが、その分、コミットを追加せざるを得ません。

## Error Conditions That Require Database Checks データベースチェックが必要なエラー状況

If we keep going like this, though, things are going to get uglier and uglier.
このままでは、どんどん醜態をさらすことになりますが。

Suppose we want to add a bit of error handling.
例えば、ちょっとしたエラー処理を追加したいとします。
What if the domain raises an error, for a SKU that’s out of stock?
もしドメインが在庫切れのSKUに対してエラーを発生させたらどうでしょうか？
Or what about a SKU that doesn’t even exist?
あるいは、存在しないSKUについてはどうでしょうか？
That’s not something the domain even knows about, nor should it.
それはドメインが知っていることでもなければ、知るべきことでもありません。
It’s more of a sanity check that we should implement at the database layer, before we even invoke the domain service.
これは、ドメインサービスを呼び出す前に、データベース層で実装されるべきサニティチェックのようなものです。

Now we’re looking at two more end-to-end tests:
今度は、さらに2つのエンドツーエンドのテストを見てみましょう。

Yet more tests at the E2E layer (test_api.py)
E2Eレイヤーのテストをさらに追加 (test_api.py)

```python
@pytest.mark.usefixtures('restart_api')
def test_400_message_for_out_of_stock(add_stock):  1
sku, smalL_batch, large_order = random_sku(), random_batchref(), random_orderid()
add_stock([
(smalL_batch, sku, 10, '2011-01-01'),
])
data = {'orderid': large_order, 'sku': sku, 'qty': 20}
url = config.get_api_url()
r = requests.post(f'{url}/allocate', json=data)
assert r.status_code == 400
assert r.json()['message'] == f'Out of stock for sku {sku}'
@pytest.mark.usefixtures('restart_api')
def test_400_message_for_invalid_sku():  2
unknown_sku, orderid = random_sku(), random_orderid()
data = {'orderid': orderid, 'sku': unknown_sku, 'qty': 20}
url = config.get_api_url()
r = requests.post(f'{url}/allocate', json=data)
assert r.status_code == 400
assert r.json()['message'] == f'Invalid sku {unknown_sku}'
```

1. In the first test, we’re trying to allocate more units than we have in stock. 最初のテストでは、在庫数より多くのユニットを割り当てようとしています。

2. In the second, the SKU just doesn’t exist (because we never called `add_stock`), so it’s invalid as far as our app is concerned. 2では、SKUが存在しないので（`add_stock`を呼んでいないので）、私たちのアプリに関する限り、無効です。

And sure, we could implement it in the Flask app too:
そして確かに、Flaskアプリにも実装することができました。

Flask app starting to get crufty (flask_app.py)
Flaskアプリがカクカクするようになった (flask_app.py)

```python
def is_valid_sku(sku, batches):
return sku in {b.sku for b in batches}
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
session = get_session()
batches = repository.SqlAlchemyRepository(session).list()
line = model.OrderLine(
request.json['orderid'],
request.json['sku'],
request.json['qty'],
)
if not is_valid_sku(line.sku, batches):
return jsonify({'message': f'Invalid sku {line.sku}'}), 400
try:
batchref = model.allocate(line, batches)
except model.OutOfStock as e:
return jsonify({'message': str(e)}), 400
session.commit()
return jsonify({'batchref': batchref}), 201
```

But our Flask app is starting to look a bit unwieldy.
しかし、私たちのFlaskアプリは、少し扱いにくくなってきているようです。
And our number of E2E tests is starting to get out of control, and soon we’ll end up with an inverted test pyramid (or “ice-cream cone model,” as Bob likes to call it).
そして、E2Eテストの数は制御不能になりつつあり、やがて逆ピラミッド（ボブが言うところの「アイスクリームコーンモデル」）になってしまうのです。

## Introducing a Service Layer, and Using FakeRepository to Unit Test It サービスレイヤーの導入と FakeRepository を使ったユニットテスト

If we look at what our Flask app is doing, there’s quite a lot of what we might call orchestration—fetching stuff out of our repository, validating our input against database state, handling errors, and committing in the happy path.
Flaskアプリが何をしているかを見てみると、オーケストレーションと呼ばれるものがかなり多く、リポジトリからの取得、データベースの状態に対する入力の検証、エラーの処理、ハッピーパスでのコミットなどがあります。
Most of these things don’t have anything to do with having a web API endpoint (you’d need them if you were building a CLI, for example; see Appendix C), and they’re not really things that need to be tested by end-to-end tests.
これらのほとんどは、Web APIエンドポイントを持つこととは関係なく（例えばCLIを構築している場合は必要でしょう。付録Cを参照）、エンドツーエンドテストでテストする必要があるものでもありません。

It often makes sense to split out a service layer, sometimes called an orchestration layer or a use-case layer.
サービスレイヤー（オーケストレーションレイヤーやユースケースレイヤーと呼ばれることもある）を分割することは、しばしば意味がある。

Do you remember the `FakeRepository` that we prepared in Chapter 3?
第3章で準備した`FakeRepository`を覚えていますか？

Our fake repository, an in-memory collection of batches (test_services.py)
偽のリポジトリ、バッチのインメモリコレクション(test_services.py)

```python
class FakeRepository(repository.AbstractRepository):
def __init__(self, batches):
self._batches = set(batches)
def add(self, batch):
self._batches.add(batch)
def get(self, reference):
return next(b for b in self._batches if b.reference == reference)
def list(self):
return list(self._batches)
```

Here’s where it will come in useful; it lets us test our service layer with nice, fast unit tests:
ここで役に立つのが、サービスレイヤーを素晴らしく高速なユニットテストでテストできるようにすることです。

Unit testing with fakes at the service layer (test_services.py)
サービス層でのフェイクを使ったユニットテスト(test_services.py)

```python
def test_returns_allocation():
line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
batch = model.Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
repo = FakeRepository([batch])  1
result = services.allocate(line, repo, FakeSession())  23
assert result == "b1"
def test_error_for_invalid_sku():
line = model.OrderLine("o1", "NONEXISTENTSKU", 10)
batch = model.Batch("b1", "AREALSKU", 100, eta=None)
repo = FakeRepository([batch])  1
with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
services.allocate(line, repo, FakeSession())  23
```

1. `FakeRepository` holds the `Batch` objects that will be used by our test. FakeRepository` は、テストで使用する `Batch` オブジェクトを保持します。

2. Our services module (services.py) will define an `allocate()` service-layer function. It will sit between our `allocate_endpoint()` function in the API layer and the `allocate()` domain service function from our domain model.1 servicesモジュール(services.py)は、サービス層の関数である `allocate()`を定義します。 これは、APIレイヤーの `allocate_endpoint()` 関数と、ドメインモデルの `allocate()` ドメインサービス関数の間に位置します1。

3. We also need a `FakeSession` to fake out the database session, as shown in the following code snippet. また、以下のコードに示すように、データベースセッションを偽装するために `FakeSession` が必要です。

A fake database session (test_services.py)
偽のデータベースセッション(test_services.py)

```python
class FakeSession():
committed = False
def commit(self):
self.committed = True
```

This fake session is only a temporary solution.
この偽セッションは一時的な解決策に過ぎません。
We’ll get rid of it and make things even nicer soon, in Chapter 6.
第6章では、すぐにこれを取り除いて、もっとすっきりしたものにします。
But in the meantime the fake `.commit()` lets us migrate a third test from the E2E layer:
しかし、それまでの間、偽の `.commit()` によって、E2E レイヤーから 3 番目のテストをマイグレートすることができます。

A second test at the service layer (test_services.py)
サービス層での2つ目のテスト(test_services.py)

```python
def test_commits():
line = model.OrderLine('o1', 'OMINOUS-MIRROR', 10)
batch = model.Batch('b1', 'OMINOUS-MIRROR', 100, eta=None)
repo = FakeRepository([batch])
session = FakeSession()
services.allocate(line, repo, session)
assert session.committed is True
```

### A Typical Service Function 典型的なサービス機能

We’ll write a service function that looks something like this:
次のようなサービス関数を書いてみます。

Basic allocation service (services.py)
基本割り当てサービス(services.py)

```python
class InvalidSku(Exception):
pass
def is_valid_sku(sku, batches):
return sku in {b.sku for b in batches}
def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
batches = repo.list()  1
if not is_valid_sku(line.sku, batches):  2
raise InvalidSku(f'Invalid sku {line.sku}')
batchref = model.allocate(line, batches)  3
session.commit()  4
return batchref
```

Typical service-layer functions have similar steps:
一般的なサービスレイヤの機能も同様のステップを踏みます。

1. We fetch some objects from the repository. リポジトリからいくつかのオブジェクトを取得する。

2. We make some checks or assertions about the request against the current state of the world. 世界の現在の状態に対して、リクエストに関するいくつかのチェックやアサーションを行う。

3. We call a domain service. ドメインサービスと呼ぶ。

4. If all is well, we save/update any state we’ve changed. 問題がなければ、保存する

That last step is a little unsatisfactory at the moment, as our service layer is tightly coupled to our database layer.
この最後のステップは、現時点では少し不満です。サービス層はデータベース層と密接に結合しているからです。
We’ll improve that in Chapter 6 with the Unit of Work pattern.
第6章では、Unit of Workパターンを使ってこれを改善します。

- DEPEND ON ABSTRACTIONS ちゅうしゅつにたよる

- Notice one more thing about our service-layer function: もうひとつ、サービスレイヤの機能にも注目してください。

- `def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:` `def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:`.

- It depends on a repository. We’ve chosen to make the dependency explicit, and we’ve used the type hint to say that we depend on AbstractRepository. This means it’ll work both when the tests give it a FakeRepository and when the Flask app gives it a SqlAlchemyRepository. リポジトリに依存しています。 依存関係を明示することにし、型ヒントを使用して AbstractRepository に依存していることを示しました。 これは、テストがFakeRepositoryを与えても、FlaskアプリがSqlAlchemyRepositoryを与えても動作することを意味します。

- If you remember “The Dependency Inversion Principle”, this is what we mean when we say we should “depend on abstractions.” Our high-level module, the service layer, depends on the repository abstraction. And the details of the implementation for our specific choice of persistent storage also depend on that same abstraction. See Figures 4-3 and 4-4. "依存関係逆転の原則 "を覚えていれば、"抽象に依存する "というのはこのことです。 私たちの上位モジュールであるサービス層は、リポジトリの抽象概念に依存しています。 そして、私たちが選んだ永続的ストレージの実装の詳細もまた、同じ抽象概念に依存しています。 図4-3と図4-4を参照してください。

- See also in Appendix C a worked example of swapping out the details of which persistent storage system to use while leaving the abstractions intact. また、付録Cでは、抽象化を維持したまま、どの永続的ストレージシステムを使用するかの詳細を入れ替えた例も紹介しています。

But the essentials of the service layer are there, and our Flask app now looks a lot cleaner:
しかし、サービスレイヤーの本質はそこにあり、私たちのFlaskアプリはずいぶんすっきりしたものになりました。

Flask app delegating to service layer (flask_app.py)
サービスレイヤーに委ねるFlaskアプリ(flask_app.py)

```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
session = get_session()  1
repo = repository.SqlAlchemyRepository(session)  1
line = model.OrderLine(
request.json['orderid'],  2
request.json['sku'],  2
request.json['qty'],  2
)
try:
batchref = services.allocate(line, repo, session)  2
except (model.OutOfStock, services.InvalidSku) as e:
return jsonify({'message': str(e)}), 400  3
return jsonify({'batchref': batchref}), 201  3
```

1. We instantiate a database session and some repository objects. データベースセッションといくつかのリポジトリオブジェクトをインスタンス化します。

2. We extract the user’s commands from the web request and pass them to a domain service. Webリクエストからユーザのコマンドを抽出し、ドメインサービスに渡す。

3. We return some JSON responses with the appropriate status codes. 適切なステータスコードを持ついくつかのJSONレスポンスを返します。

The responsibilities of the Flask app are just standard web stuff: per-request session management, parsing information out of POST parameters, response status codes, and JSON.
Flaskアプリの責務は、リクエストごとのセッション管理、POSTパラメータからの情報解析、レスポンスステータスコード、JSONなど、標準的なWebのものだけです。
All the orchestration logic is in the use case
すべてのオーケストレーションロジックはユースケースにあります。

Finally, we can confidently strip down our E2E tests to just two, one for the happy path and one for the unhappy path:
最後に、E2Eテストは、ハッピーパスとアンハッピーパスの2つだけに絞り込むことができます。

E2E tests only happy and unhappy paths (test_api.py)
E2Eはハッピーパスとアンハッピーパスのみをテストする(test_api.py)

```python
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_201_and_allocated_batch(add_stock):
sku, othersku = random_sku(), random_sku('other')
earlybatch = random_batchref(1)
laterbatch = random_batchref(2)
otherbatch = random_batchref(3)
add_stock([
(laterbatch, sku, 100, '2011-01-02'),
(earlybatch, sku, 100, '2011-01-01'),
(otherbatch, othersku, 100, None),
])
data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}
url = config.get_api_url()
r = requests.post(f'{url}/allocate', json=data)
assert r.status_code == 201
assert r.json()['batchref'] == earlybatch
@pytest.mark.usefixtures('restart_api')
def test_unhappy_path_returns_400_and_error_message():
unknown_sku, orderid = random_sku(), random_orderid()
data = {'orderid': orderid, 'sku': unknown_sku, 'qty': 20}
url = config.get_api_url()
r = requests.post(f'{url}/allocate', json=data)
assert r.status_code == 400
assert r.json()['message'] == f'Invalid sku {unknown_sku}'
```

We’ve successfully split our tests into two broad categories: tests about web stuff, which we implement end to end; and tests about orchestration stuff, which we can test against the service layer in memory.
私たちは、テストを大きく2つに分けることに成功しました。Webに関するテストは、エンドツーエンドで実装し、オーケストレーションに関するテストは、メモリ上のサービス層に対してテストすることができます。

- EXERCISE FOR THE READER 読書運動

- Now that we have an allocate service, why not build out a service for `deallocate`? We’ve added an E2E test and a few stub service-layer tests for you to get started on GitHub. allocate サービスができたので、`deallocate` のサービスも作ってみませんか？ E2EテストとサービスレイヤーのスタブテストをGitHubに追加しましたので、早速始めてみましょう。

- If that’s not enough, continue into the E2E tests and flask_app.py, and refactor the Flask adapter to be more RESTful. Notice how doing so doesn’t require any change to our service layer or domain layer! それでも不十分な場合は、E2Eテストとflask_app.pyに進み、FlaskアダプタをよりRESTfulにリファクタリングしましょう。 そうすることで、サービス層やドメイン層を変更する必要がないことに注意してください。

- TIP ヒント

- If you decide you want to build a read-only endpoint for retrieving allocation info, just do “the simplest thing that can possibly work,” which is `repo.get()` right in the Flask handler. We’ll talk more about reads versus writes in Chapter 12. もしアロケーション情報を取得するための読み取り専用のエンドポイントを作りたいと思ったら、Flask ハンドラ内で `repo.get()` という「最もシンプルに動作するもの」を実行すればいいのです。 読み込みと書き込みの違いについては、12章で詳しく説明します。

## Why Is Everything Called a Service? なぜ何でもかんでもサービスと呼ばれるのか？

Some of you are probably scratching your heads at this point trying to figure out exactly what the difference is between a domain service and a service layer.
この時点で、ドメインサービスとサービスレイヤーの違いを正確に理解しようと頭を悩ませている方もいらっしゃることでしょう。

We’re sorry—we didn’t choose the names, or we’d have much cooler and friendlier ways to talk about this stuff.
申し訳ありません。私たちが名前を選んだわけではありませんし、もっとクールで友好的な話し方があるはずです。

We’re using two things called a service in this chapter.
この章では、サービスと呼ばれるものを2つ使用します。
The first is an application service (our service layer).
ひとつはアプリケーションサービス (私たちのサービス層) です。
Its job is to handle requests from the outside world and to orchestrate an operation.
その仕事は、外界からのリクエストを処理し、オペレーションをオーケストレーションすることです。
What we mean is that the service layer drives the application by following a bunch of simple steps:
どういうことかというと、サービス層は単純なステップの束に従うことで、アプリケーションを駆動させるということです。

- Get some data from the database データベースからデータを取得する

- Update the domain model ドメインモデルの更新

- Persist any changes 変更を持続させる

This is the kind of boring work that has to happen for every operation in your system, and keeping it separate from business logic helps to keep things tidy.
このような退屈な作業は、システム内のすべてのオペレーションで発生するため、ビジネスロジックと分けて考えることで、整理整頓がしやすくなります。



## Putting Things in Folders to See Where It All Belongs モノをフォルダに分類して、どこに何があるのかを確認する

As our application gets bigger, we’ll need to keep tidying our directory structure.
アプリケーションが大きくなるにつれて、ディレクトリ構造を整理していく必要があります。
The layout of our project gives us useful hints about what kinds of object we’ll find in each file.
プロジェクトのレイアウトは、各ファイルにどのような種類のオブジェクトがあるのかについての有用なヒントを与えてくれます。

Here’s one way we could organize things:
ここで、ひとつの整理をします。

Some subfolders
一部のサブフォルダ

```
.
├── config.py
├── domain  1
│   ├── __init__.py
│   └── model.py
├── service_layer  2
│   ├── __init__.py
│   └── services.py
├── adapters  3
│   ├── __init__.py
│   ├── orm.py
│   └── repository.py
├── entrypoints  4
│   ├── __init__.py
│   └── flask_app.py
└── tests
├── __init__.py
├── conftest.py
├── unit
│   ├── test_allocate.py
│   ├── test_batches.py
│   └── test_services.py
├── integration
│   ├── test_orm.py
│   └── test_repository.py
└── e2e
└── test_api.py
```

1. Let’s have a folder for our domain model. Currently that’s just one file, but for a more complex application, you might have one file per class; you might have helper parent classes for Entity, ValueObject, and Aggregate, and you might add an exceptions.py for domain-layer exceptions and, as you’ll see in Part II, commands.py and events.py. 

2. We’ll distinguish the service layer. Currently that’s just one file called services.py for our service-layer functions. You could add service-layer exceptions here, and as you’ll see in Chapter 5, we’ll add unit_of_work.py. サービスレイヤーを区別することにします。 現状では、サービス層の関数のためのservices.pyという1つのファイルだけです。 ここにサービス層の例外を追加することもできますし、第5章で説明するように、unit_of_work.pyを追加します。

3. Adapters is a nod to the ports and adapters terminology. This will fill up with any other abstractions around external I/O (e.g., a redis_client.py). Strictly speaking, you would call these secondary adapters or driven adapters, or sometimes inward-facing adapters. Adapters は、ポートやアダプタの用語にちなんだものです。 これは、外部Iの周りの他の抽象化されたもので埋め尽くされます。

4. Entrypoints are the places we drive our application from. In the official ports and adapters terminology, these are adapters too, and are referred to as primary, driving, or outward-facing adapters. エントリーポイントとは、アプリケーションを駆動するための場所です。 公式のポートやアダプタの用語では、これらもアダプタであり、プライマリ、ドライビング、または外向きのアダプタと呼ばれています。

What about ports?
ポートについてはどうでしょうか。
As you may remember, they are the abstract interfaces that the adapters implement.
覚えているかもしれませんが、これはアダプタが実装する抽象的なインターフェイスです。
We tend to keep them in the same file as the adapters that implement them.
ポートについては、それを実装したアダプタと同じファイルに保存することが多いです。

## Wrap-Up まとめ

Adding the service layer has really bought us quite a lot:
サービスレイヤーを追加することで、本当に多くのものを得ることができました。

- Our Flask API endpoints become very thin and easy to write: their only responsibility is doing “web stuff,” such as parsing JSON and producing the right HTTP codes for happy or unhappy cases. FlaskのAPIエンドポイントは、JSONをパースしたり、ハッピーなケースやアンハッピーなケースに適切なHTTPコードを生成したりといった「Web的なこと」をするだけで、非常に薄く、簡単に書くことができるようになります。

- We’ve defined a clear API for our domain, a set of use cases or entrypoints that can be used by any adapter without needing to know anything about our domain model classes—whether that’s an API, a CLI (see Appendix C), or the tests! They’re an adapter for our domain too. ドメインモデル・クラスについて何も知らなくても、 どんなアダプタでも使えるユースケースやエントリポイントのセットです。 それが API であれ CLI (付録 C 参照) であれ、あるいはテストであれ! API や CLI (付録 C 参照)、そしてテストもそうです！これらは、私たちのドメインのためのアダプタでもあるのです。

- We can write tests in “high gear” by using the service layer, leaving us free to refactor the domain model in any way we see fit. As long as we can still deliver the same use cases, we can experiment with new designs without needing to rewrite a load of tests. 

- And our test pyramid is looking good—the bulk of our tests are fast unit tests, with just the bare minimum of E2E and integration tests. テストの大部分は高速なユニットテストであり、E2Eテストと統合テストは必要最低限にとどめています。

### The DIP in Action DIPの動作



When we run the tests, Figure 4-4 shows how we implement the abstract dependencies by using `FakeRepository` (the adapter).
テストを実行すると、図 4-4 に示すように、`FakeRepository` (アダプター) を使って抽象的な依存関係を実装していることがわかります。

And when we actually run our app, we swap in the “real” dependency shown in Figure 4-5.
そして、実際にアプリを実行すると、図4-5に示すような「本当の」依存関係に入れ替わります。

![fig 4-4](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0404.png)

![fig 4-5](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0405.png)

Wonderful.
素晴らしい。

Let’s pause for Table 4-1, in which we consider the pros and cons of having a service layer at all.
表4-1では、サービスレイヤーを持つことの是非を考えてみよう。

Table 4-1.
表4-1.
Service layer: the trade-offs
サービス層：トレードオフ

- Pros 長所

- We have a single place to capture all the use cases for our application. 私たちは、アプリケーションのすべてのユースケースを把握する場所を一カ所に集約しています。

- We’ve placed our clever domain logic behind an API, which leaves us free to refactor. 私たちは、巧妙なドメインロジックをAPIの後ろに配置し、自由にリファクタリングできるようにしています。

- We have cleanly separated “stuff that talks HTTP” from “stuff that talks allocation.” "HTTPを話すもの "と "アロケーションを話すもの "をきれいに分離しました。

- When combined with the Repository pattern and `FakeRepository`, we have a nice way of writing tests at a higher level than the domain layer; we can test more of our workflow without needing to use integration tests (read on to Chapter 5 for more elaboration on this). Repositoryパターンと `FakeRepository` を組み合わせると、ドメインレイヤーよりも高いレベルでテストを記述することができるようになります。

- Cons 短所

- If your app is purely a web app, your controllers/view functions can be the single place to capture all the use cases. アプリが純粋なWebアプリの場合、コントローラ

- It’s yet another layer of abstraction. 

- Putting too much logic into the service layer can lead to the Anemic Domain anti-pattern. It’s better to introduce this layer after you spot orchestration logic creeping into your controllers. サービスレイヤーに多くのロジックを入れると、貧弱なドメインというアンチパターンを引き起こす可能性がある。 このレイヤーは、オーケストレーションのロジックがコントローラに忍び込んでいるのを確認してから導入するのがよいでしょう。

- You can get a lot of the benefits that come from having rich domain models by simply pushing logic out of your controllers and down to the model layer, without needing to add an extra layer in between (aka “fat models, thin controllers”). リッチなドメインモデルを持つことで得られる多くの利点は、コントローラからモデル層へとロジックを押し出すだけで、その間に余分な層を追加する必要がありません（別名、「太いモデル、細いコントローラ」）。

But there are still some bits of awkwardness to tidy up:
しかし、まだ片付けなければならないぎこちなさが残っています。

- The service layer is still tightly coupled to the domain, because its API is expressed in terms of OrderLine objects. In Chapter 5, we’ll fix that and talk about the way that the service layer enables more productive TDD. サービスレイヤーは、APIがOrderLineオブジェクトで表現されるため、ドメインとまだ緊密に結合しています。 第5章では、この点を修正し、サービスレイヤーがより生産的なTDDを可能にする方法について説明します。

- The service layer is tightly coupled to a session object. In Chapter 6, we’ll introduce one more pattern that works closely with the Repository and Service Layer patterns, the Unit of Work pattern, and everything will be absolutely lovely. You’ll see! サービスレイヤーはセッションオブジェクトと緊密に結合しています。 第6章では、リポジトリとサービスレイヤーのパターンと密接に連携するもう一つのパターン、Unit of Workパターンを紹介します。そうすれば、すべてが絶対に素敵になります。 見てください!

1. Service-layer services and domain services do have confusingly similar names. We tackle this topic later in “Why Is Everything Called a Service?”. サービスレイヤーサービスとドメインサービスは、紛らわしいほど似たような名前を持っています。 この話題については、後ほど「なぜすべてがサービスと呼ばれるのか」で取り上げます。