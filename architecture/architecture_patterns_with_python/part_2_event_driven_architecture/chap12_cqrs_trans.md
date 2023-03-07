# chapter 12 Command-Query Responsibility Segregation (CQRS) 第12章 コマンドクエリ責任分離(CQRS)

In this chapter, we’re going to start with a fairly uncontroversial insight: reads (queries) and writes (commands) are different, so they should be treated differently (or have their responsibilities segregated, if you will).
この章では、**読み込み(query)と書き込み(commands)は異なる**ので、**それぞれを別扱いする(あるいは責任を分離する)べき**であるという、かなり議論の余地のない見解から始めるつもりである.
Then we’re going to push that insight as far as we can.
そして、その考えを可能な限り押し進めようと思う.

If you’re anything like Harry, this will all seem extreme at first, but hopefully we can make the argument that it’s not totally unreasonable.
ハリーのように、最初は極端な話だと思われるかもしれませんが、まったく理不尽な話ではないことを主張できればと思う.

Figure 12-1 shows where we might end up.
図12-1は、その行き着く先を示したものである.

- TIP
- The code for this chapter is in the chapter_12_cqrs branch on GitHub. 本章のコードはGitHubのchapter_12_cqrsブランチにあります。

```python
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_12_cqrs
# or to code along, checkout the previous chapter:
git checkout chapter_11_external_events
```

First, though, why bother?
まず、なぜ悩むのか、だが...

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1201.png)

## Domain Models Are for Writing ドメインモデルは書くためにある

We’ve spent a lot of time in this book talking about how to build software that enforces the rules of our domain.
この本では、ドメインのルールを強制するソフトウェアを構築する方法について、多くの時間を費やしてきました。
These rules, or constraints, will be different for every application, and they make up the interesting core of our systems.
これらのルールや制約は、アプリケーションごとに異なり、私たちのシステムの興味深いコアを構成しています。

In this book, we’ve set explicit constraints like “You can’t allocate more stock than is available,” as well as implicit constraints like “Each order line is allocated to a single batch.”
本書では、"在庫以上の在庫は割り当てられない "といった明示的な制約と、"各注文行は1つのバッチに割り当てる "といった暗黙の制約を設定しました。

We wrote down these rules as unit tests at the beginning of the book:
このルールを冒頭のユニットテストとして書き出しました。

Our basic domain tests (tests
私たちの基本的なドメインテスト（テスト

```python
def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18

...

def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False
```

To apply these rules properly, we needed to ensure that operations were consistent, and so we introduced patterns like Unit of Work and Aggregate that help us commit small chunks of work.
これらのルールを適切に適用するためには、操作の一貫性を確保する必要があるため、Unit of WorkやAggregateといった、小さな作業の塊をコミットするのに役立つパターンを導入しました。

To communicate changes between those small chunks, we introduced the Domain Events pattern so we can write rules like “When stock is damaged or lost, adjust the available quantity on the batch, and reallocate orders if necessary.”
その小さな塊の間で変更を伝えるために、Domain Eventsパターンを導入しました。"在庫が破損したり紛失したりしたら、バッチの使用可能量を調整し、必要に応じて注文を再割り当てする "というようなルールを書くことができます。

All of this complexity exists so we can enforce rules when we change the state of our system.
このような複雑なものはすべて、システムの状態を変更するときにルールを強制できるように存在します。
We’ve built a flexible set of tools for writing data.
私たちは、データを書き込むための柔軟なツール群を構築しました。

What about reads, though?
読書はどうなんでしょう？

## Most Users Aren’t Going to Buy Your Furniture ほとんどのユーザーはあなたの家具を買おうとはしない

At MADE.com, we have a system very like the allocation service.
MADE.comでは、このアロケーションサービスのようなシステムを導入しています。
In a busy day, we might process one hundred orders in an hour, and we have a big gnarly system for allocating stock to those orders.
忙しい日は1時間に100件の注文を処理することもありますが、その注文に在庫を割り振るための大きなニッチなシステムを持っているのです。

In that same busy day, though, we might have one hundred product views per second.
しかし、同じ忙しい日でも、1秒間に100回の商品閲覧がある場合もあります。
Each time somebody visits a product page, or a product listing page, we need to figure out whether the product is still in stock and how long it will take us to deliver it.
商品ページや商品一覧ページにアクセスするたびに、その商品の在庫があるかどうか、納品までにかかる時間はどのくらいか、などを確認する必要があります。

The domain is the same—we’re concerned with batches of stock, and their arrival date, and the amount that’s still available—but the access pattern is very different.
ドメインは同じで、在庫のバッチとその到着日、そしてまだ利用可能な量に関心がありますが、アクセスパターンは大きく異なります。
For example, our customers won’t notice if the query is a few seconds out of date, but if our allocate service is inconsistent, we’ll make a mess of their orders.
例えば、クエリが数秒古くても顧客は気づきませんが、アロケートサービスに一貫性がないと、顧客の注文を台無しにすることになります。
We can take advantage of this difference by making our reads eventually consistent in order to make them perform better.
この違いを利用して、読み込みを最終的に一貫性のあるものにすることで、より良いパフォーマンスを実現することができます。

---
---

- IS READ CONSISTENCY TRULY ATTAINABLE? は本当に達成できるのでしょうか？

This idea of trading consistency against performance makes a lot of developers nervous at first, so let’s talk quickly about that.
このように一貫性を性能と引き換えにするという考え方は、多くの開発者を最初は不安にさせるので、それについて手短にお話ししましょう。

Let’s imagine that our “Get Available Stock” query is 30 seconds out of date when Bob visits the page for `ASYMMETRICAL-DRESSER`.
ボブが`ASYMMETRICAL-DRESSER`のページにアクセスしたとき、我々の「利用可能な在庫を取得」クエリが30秒古くなっていたとしよう。
Meanwhile, though, Harry has already bought the last item.
しかしその間に、ハリーはすでに最後の商品を買ってしまっている。
When we try to allocate Bob’s order, we’ll get a failure, and we’ll need to either cancel his order or buy more stock and delay his delivery.
ボブの注文を割り当てようとすると失敗してしまい、彼の注文をキャンセルするか、在庫を買い足して彼の配送を遅らせる必要があります。

People who’ve worked only with relational data stores get really nervous about this problem, but it’s worth considering two other scenarios to gain some perspective.
リレーショナル・データ・ストアだけを扱ってきた人は、この問題にとても神経質になりますが、視点を変えるために、他の2つのシナリオを考えてみる価値があります。

First, let’s imagine that Bob and Harry both visit the page at the same time.
まず、ボブさんとハリーさんが同時にこのページを訪れたとします。
Harry goes off to make coffee, and by the time he returns, Bob has already bought the last dresser.
ハリーがコーヒーを入れに行き、戻ってきたときには、ボブはすでに最後のドレッサーを買ってしまっている。
When Harry places his order, we send it to the allocation service, and because there’s not enough stock, we have to refund his payment or buy more stock and delay his delivery.
ハリーが注文すると、それを配車サービスに送るのですが、在庫が足りないので、支払いを返金するか、在庫を買い足して納品を遅らせる必要があります。

As soon as we render the product page, the data is already stale.
商品ページをレンダリングした時点で、データはすでに古くなっているのです。
This insight is key to understanding why reads can be safely inconsistent: we’ll always need to check the current state of our system when we come to allocate, because all distributed systems are inconsistent.
この洞察は、なぜ読み込みが安全に一貫性を欠くことができるのかを理解するための鍵です。すべての分散システムは一貫性を欠くので、割り当てに来るときには常にシステムの現在の状態を確認する必要があります。
As soon as you have a web server and two customers, you have the potential for stale data.
ウェブサーバーと2人の顧客がいる時点で、データが古くなる可能性があるのです。

OK, let’s assume we solve that problem somehow: we magically build a totally consistent web application where nobody ever sees stale data.
では、この問題を解決するために、魔法のように完全に一貫したウェブアプリケーションを構築し、誰も古いデータを見ることがないと仮定しましょう。
This time Harry gets to the page first and buys his dresser.
今度はハリーが先にページにアクセスし、ドレッサーを購入しました。

Unfortunately for him, when the warehouse staff tries to dispatch his furniture, it falls off the forklift and smashes into a zillion pieces.
ところが、倉庫のスタッフが家具を運び出そうとしたところ、フォークリフトから落ちて粉々に砕けてしまったのです。
Now what?
さて、どうする？

The only options are to either call Harry and refund his order or buy more stock and delay delivery.
ハリーに電話して注文を返金するか、在庫を買い足して納期を遅らせるかのどちらかしか選択肢がない。

No matter what we do, we’re always going to find that our software systems are inconsistent with reality, and so we’ll always need business processes to cope with these edge cases.
どんなことをしても、ソフトウェア・システムが現実と矛盾していることはあります。
It’s OK to trade performance for consistency on the read side, because stale data is essentially unavoidable.
古いデータは基本的に避けられないので、読み込み側では性能と一貫性を交換しても問題ありません。

---
---

We can think of these requirements as forming two halves of a system: the read side and the write side, shown in Table 12-1.
これらの要件は、表12-1に示すように、システムのリードサイドとライトサイドの2つのハーフを形成していると考えることができます。

For the write side, our fancy domain architectural patterns help us to evolve our system over time, but the complexity we’ve built so far doesn’t buy anything for reading data.
書き込み側では、派手なドメインアーキテクチャパターンが、時間をかけてシステムを進化させるのに役立ちますが、これまで構築してきた複雑さは、データを読み込むためには何も買えません。
The service layer, the unit of work, and the clever domain model are just bloat.
サービス層、作業単位、巧妙なドメインモデルなどは、単なる肥大化です。

Table 12-1.
表12-1.
Read versus write
読み出しと書き込みの比較















## Post/Redirect/Get and CQS ポスト

If you do web development, you’re probably familiar with the Post
Web制作をされている方ならご存知だと思いますが、Post

This approach fixes the problems that arise when users refresh the results page in their browser or try to bookmark a results page.
この方法は、ユーザーがブラウザで結果ページを更新したり、結果ページをブックマークしようとしたときに発生する問題を解決するものです。
In the case of a refresh, it can lead to our users double-submitting data and thus buying two sofas when they needed only one.
更新の場合、ユーザーがデータを二重に送信してしまい、1つしか必要ないソファを2つ購入してしまう可能性があります。
In the case of a bookmark, our hapless customers will end up with a broken page when they try to GET a POST endpoint.
ブックマークの場合は、POSTエンドポイントをGETしようとすると、ページが壊れてしまいます。

Both these problems happen because we’re returning data in response to a write operation.
いずれも、書き込み操作に対応してデータを返しているために起こる問題です。
Post
投稿

This technique is a simple example of command-query separation (CQS).
このテクニックは、コマンド・クエリ分離（CQS）の簡単な例です。
In CQS we follow one simple rule: functions should either modify state or answer questions, but never both.
CQSでは、関数は状態を変更するか、質問に答えるかのどちらかでなければならず、両方を行うことはない、というシンプルなルールに従います。
This makes software easier to reason about: we should always be able to ask, “Are the lights on?” without flicking the light switch.
つまり、関数は状態を変更するか、質問に答えるかのどちらかであるべきで、両方を行うことはできないということです。

---
---

- NOTE ノート

When building APIs, we can apply the same design technique by returning a 201 Created, or a 202 Accepted, with a Location header containing the URI of our new resources.
APIを構築する場合、新しいリソースのURIを含むLocationヘッダとともに、201 Createdまたは202 Acceptedを返すことで、同じ設計手法を適用することができます。
What’s important here isn’t the status code we use but the logical separation of work into a write phase and a query phase.
ここで重要なのは、使用するステータスコードではなく、作業を書き込みフェーズと問い合わせフェーズに論理的に分離することです。

---
---

As you’ll see, we can use the CQS principle to make our systems faster and more scalable, but first, let’s fix the CQS violation in our existing code.
これからわかるように、私たちはCQSの原則を利用してシステムをより速く、よりスケーラブルにすることができるのですが、まずは既存のコードにあるCQS違反を修正しましょう。
Ages ago, we introduced an `allocate` endpoint that takes an order and calls our service layer to allocate some stock.
何年も前に、私たちは `allocate` エンドポイントを導入しました。このエンドポイントは注文を受け、サービスレイヤーを呼び出して在庫を確保します。
At the end of the call, we return a 200 OK and the batch ID.
呼び出しの最後には、200 OKとバッチIDが返されます。
That’s led to some ugly design flaws so that we can get the data we need.
これは、必要なデータを取得できるようにするために、いくつかの醜い設計上の欠陥につながりました。
Let’s change it to return a simple OK message and instead provide a new read-only endpoint to retrieve allocation state:
単純なOKメッセージを返すように変更し、代わりに割り当て状態を取得するための新しい読み取り専用エンドポイントを提供することにしましょう。

API test does a GET after the POST (tests
APIテストでは、POSTの後にGETを行う（テスト

```python
@pytest.mark.usefixtures('postgres_db')
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_202_and_batch_is_allocated():
    orderid = random_orderid()
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    api_client.post_to_add_batch(laterbatch, sku, 100, '2011-01-02')
    api_client.post_to_add_batch(earlybatch, sku, 100, '2011-01-01')
    api_client.post_to_add_batch(otherbatch, othersku, 100, None)

    r = api_client.post_to_allocate(orderid, sku, qty=3)
    assert r.status_code == 202

    r = api_client.get_allocation(orderid)
    assert r.ok
    assert r.json() == [
        {'sku': sku, 'batchref': earlybatch},
    ]


@pytest.mark.usefixtures('postgres_db')
@pytest.mark.usefixtures('restart_api')
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, orderid = random_sku(), random_orderid()
    r = api_client.post_to_allocate(
        orderid, unknown_sku, qty=20, expect_success=False,
    )
    assert r.status_code == 400
    assert r.json()['message'] == f'Invalid sku {unknown_sku}'

    r = api_client.get_allocation(orderid)
    assert r.status_code == 404
```

OK, what might the Flask app look like?
さて、Flaskのアプリはどのようなものでしょうか？

Endpoint for viewing allocations (src
アロケーションを閲覧するためのエンドポイント（src

```python
from allocation import views
...

@app.route("/allocations/<orderid>", methods=['GET'])
def allocations_view_endpoint(orderid):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = views.allocations(orderid, uow)  1
    if not result:
        return 'not found', 404
    return jsonify(result), 200
```

1. All right, a views.py, fair enough; we can keep read-only stuff in there, and it’ll be a real views.py, not like Django’s, something that knows how to build read-only views of our data… よし、views.pyだ、十分だ。読み取り専用のものを入れておけば、Djangoのものとは違う、本物のviews.pyになる。

## Hold On to Your Lunch, Folks Hold on to Your Lunch, Folks

Hmm, so we can probably just add a list method to our existing repository object:
うーん、じゃあ、既存のリポジトリオブジェクトにlistメソッドを追加すればいいんじゃない？

Views do…raw SQL?
ビューが...生SQLを？
(src
(src

```python
from allocation.service_layer import unit_of_work

def allocations(orderid: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = list(uow.session.execute(
            'SELECT ol.sku, b.reference'
            ' FROM allocations AS a'
            ' JOIN batches AS b ON a.batch_id = b.id'
            ' JOIN order_lines AS ol ON a.orderline_id = ol.id'
            ' WHERE ol.orderid = :orderid',
            dict(orderid=orderid)
        ))
    return [{'sku': sku, 'batchref': batchref} for sku, batchref in results]
```

Excuse me?
失礼ですが、「？
Raw SQL?
生SQLですか？

If you’re anything like Harry encountering this pattern for the first time, you’ll be wondering what on earth Bob has been smoking.
このパターンに初めて遭遇したハリーのような人は、ボブはいったい何を吸っていたのだろうと思うことでしょう。
We’re hand-rolling our own SQL now, and converting database rows directly to dicts?
私たちは今、独自のSQLを手作業で作成し、データベースの行を直接ディクテに変換しているのですか？
After all the effort we put into building a nice domain model?
せっかく素敵なドメインモデルを構築したのに？
And what about the Repository pattern?
リポジトリパターンはどうなんだ？
Isn’t that meant to be our abstraction around the database?
あれはデータベースを抽象化するためのものではないのか？
Why don’t we reuse that?
なぜそれを再利用しないのか？

Well, let’s explore that seemingly simpler alternative first, and see what it looks like in practice.
では、まずその一見シンプルな選択肢を探ってみて、実際にどのようなものなのかを見てみましょう。

We’ll still keep our view in a separate views.py module; enforcing a clear distinction between reads and writes in your application is still a good idea.
アプリケーションで読み取りと書き込みを明確に区別することは、やはり良いアイデアです。
We apply command-query separation, and it’s easy to see which code modifies state (the event handlers) and which code just retrieves read-only state (the views).
コマンドとクエリの分離を適用し、どのコードが状態を変更し（イベントハンドラ）、どのコードが読み取り専用の状態（ビュー）を取得するだけかを簡単に確認することができます。

---
---

- TIP ティップ

Splitting out your read-only views from your state-modifying command and event handlers is probably a good idea, even if you don’t want to go to full-blown CQRS.
本格的なCQRSにしなくても、読み取り専用のビューと、状態を変更するコマンドやイベントハンドラを分離することは、おそらく良いアイデアだと思います。

---
---

## Testing CQRS Views CQRSビューのテスト

Before we get into exploring various options, let’s talk about testing.
様々な選択肢を検討する前に、テストについて説明しましょう。
Whichever approaches you decide to go for, you’re probably going to need at least one integration test.
どのようなアプローチを取るにしても、少なくとも1回は統合テストが必要でしょう。
Something like this:
次のようなものです。

An integration test for a view (tests
ビューの統合テスト（テスト

```python
def test_allocations_view(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    messagebus.handle(commands.CreateBatch('sku1batch', 'sku1', 50, None), uow)  1
    messagebus.handle(commands.CreateBatch('sku2batch', 'sku2', 50, today), uow)
    messagebus.handle(commands.Allocate('order1', 'sku1', 20), uow)
    messagebus.handle(commands.Allocate('order1', 'sku2', 20), uow)
    # add a spurious batch and order to make sure we're getting the right ones
    messagebus.handle(commands.CreateBatch('sku1batch-later', 'sku1', 50, today), uow)
    messagebus.handle(commands.Allocate('otherorder', 'sku1', 30), uow)
    messagebus.handle(commands.Allocate('otherorder', 'sku2', 10), uow)

    assert views.allocations('order1', uow) == [
        {'sku': 'sku1', 'batchref': 'sku1batch'},
        {'sku': 'sku2', 'batchref': 'sku2batch'},
    ]
```

1. We do the setup for the integration test by using the public entrypoint to our application, the message bus. That keeps our tests decoupled from any implementation/infrastructure details about how things get stored. 統合テストのセットアップは、アプリケーションのパブリックなエントリポイントであるメッセージバスを使用して行います。 これにより、テストはどのような実装からも切り離された状態になります。

## “Obvious” Alternative 1: Using the Existing Repository 「明白な」代替案1：既存のリポジトリを使う

How about adding a helper method to our `products` repository?
私たちの `products` リポジトリにヘルパーメソッドを追加するのはどうでしょうか。

A simple view that uses the repository (src
リポジトリを利用したシンプルなビュー（src

```python
from allocation import unit_of_work

def allocations(orderid: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        products = uow.products.for_order(orderid=orderid)  1
        batches = [b for p in products for b in p.batches]  2
        return [
            {'sku': b.sku, 'batchref': b.reference}
            for b in batches
            if orderid in b.orderids  3
        ]
```

1. Our repository returns Product objects, and we need to find all the products for the SKUs in a given order, so we’ll build a new helper method called .for_order() on the repository. 私たちのリポジトリはProductオブジェクトを返し、与えられた注文のSKUのすべての製品を見つける必要があるので、リポジトリに.for_order()という新しいヘルパーメソッドを構築することにします。

2. Now we have products but we actually want batch references, so we get all the possible batches with a list comprehension. これで商品が揃いましたが、実際にはバッチ参照が必要なので、リスト内包で可能なバッチをすべて取得します。

3. We filter again to get just the batches for our specific order. That, in turn, relies on our Batch objects being able to tell us which order IDs it has allocated. 特定の注文に対応するバッチだけを取得するために、再度フィルターをかけます。 これは、バッチオブジェクトがどの注文IDを割り当てたかを教えてくれることに依存します。

We implement that last using a `.orderid` property:
最後に`.orderid`プロパティを使用して実装します。

An arguably unnecessary property on our model (src
私たちのモデルには、間違いなく不要なプロパティ（src

```python
class Batch:
    ...

    @property
    def orderids(self):
        return {l.orderid for l in self._allocations}
```

You can start to see that reusing our existing repository and domain model classes is not as straightforward as you might have assumed.
既存のリポジトリとドメインモデルのクラスを再利用することは、想定していたほど簡単ではないことがおわかりいただけると思います。
We’ve had to add new helper methods to both, and we’re doing a bunch of looping and filtering in Python, which is work that would be done much more efficiently by the database.
両者に新しいヘルパーメソッドを追加する必要があり、Pythonでループやフィルタリングをたくさん行っていますが、これはデータベースで行う方がはるかに効率的な作業です。

So yes, on the plus side we’re reusing our existing abstractions, but on the downside, it all feels quite clunky.
つまり、プラス面では、既存の抽象的な機能を再利用していることになりますが、マイナス面では、非常に不便に感じられます。

## Your Domain Model Is Not Optimized for Read Operations Your Domain Model Is Not Optimized for Read Operations（ドメインモデルが読み取り操作に最適化されていない

What we’re seeing here are the effects of having a domain model that is designed primarily for write operations, while our requirements for reads are often conceptually quite different.
これは、ドメインモデルが主に書き込み操作のために設計されているのに対して、読み出しに関する要件は概念的にまったく異なることが多いということの影響である。

This is the chin-stroking-architect’s justification for CQRS.
これは、CQRSを正当化するための顎関節症アーキテクトの主張です。
As we’ve said before, a domain model is not a data model—we’re trying to capture the way the business works: workflow, rules around state changes, messages exchanged; concerns about how the system reacts to external events and user input.
ワークフロー、状態変化に関するルール、メッセージのやり取り、外部イベントやユーザー入力に対するシステムの反応に関する懸念など、ビジネスが機能する方法を把握しようとしているのです。
Most of this stuff is totally irrelevant for read-only operations.
ワークフロー、状態変化に関するルール、交換されるメッセージ、外部イベントやユーザー入力に対するシステムの反応に関する懸念などです。これらのほとんどは、読み取り専用の操作には全く関係ありません。

---
---

- TIP ティップ

This justification for CQRS is related to the justification for the Domain Model pattern.
このCQRSの正当性は、Domain Modelパターンの正当性と関連しています。
If you’re building a simple CRUD app, reads and writes are going to be closely related, so you don’t need a domain model or CQRS.
単純なCRUDアプリを作る場合、読み込みと書き込みは密接に関係しているので、ドメインモデルもCQRSも必要ありません。
But the more complex your domain, the more likely you are to need both.
しかし、ドメインが複雑になればなるほど、その両方が必要になる可能性が高くなります。

---
---

To make a facile point, your domain classes will have multiple methods for modifying state, and you won’t need any of them for read-only operations.
手前味噌ですが、ドメインクラスには状態を変更するための複数のメソッドがあり、読み取り専用の操作にはそのどれもが必要ないはずです。

As the complexity of your domain model grows, you will find yourself making more and more choices about how to structure that model, which make it more and more awkward to use for read operations.
ドメインモデルが複雑になると、そのモデルの構造についてますます多くの選択をすることになり、読み取り操作に使うにはますます不便になります。

## “Obvious” Alternative 2: Using the ORM 「明白な」選択肢2：ORMを使う

You may be thinking, OK, if our repository is clunky, and working with `Products` is clunky, then I can at least use my ORM and work with `Batches`.
リポジトリが不便で `Products` を扱うのも不便なら、せめて ORM を使って `Batches` を扱えるようにしよう、とお考えかもしれませんね。
That’s what it’s for!
そのためのものなのです。

A simple view that uses the ORM (src
ORMを使用したシンプルなビュー（src

```python
from allocation import unit_of_work, model

def allocations(orderid: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        batches = uow.session.query(model.Batch).join(
            model.OrderLine, model.Batch._allocations
        ).filter(
            model.OrderLine.orderid == orderid
        )
        return [
            {'sku': b.sku, 'batchref': b.batchref}
            for b in batches
        ]
```

But is that actually any easier to write or understand than the raw SQL version from the code example in “Hold On to Your Lunch, Folks”?
しかし、それは "Hold On to Your Lunch, Folks" のコード例にある生の SQL バージョンよりも書きやすく、理解しやすいのでしょうか？
It may not look too bad up there, but we can tell you it took several attempts, and plenty of digging through the SQLAlchemy docs.
しかし、SQLAlchemyのドキュメントを何度も読み、何度も試行錯誤を繰り返した結果、このようになりました。
SQL is just SQL.
SQLはあくまでSQLです。

But the ORM can also expose us to performance problems.
しかし、ORMはパフォーマンスの問題にさらされることもあります。

## SELECT N+1 and Other Performance Considerations SELECT N+1 とその他のパフォーマンスに関する考察

The so-called SELECT N+1 problem is a common performance problem with ORMs: when retrieving a list of objects, your ORM will often perform an initial query to, say, get all the IDs of the objects it needs, and then issue individual queries for each object to retrieve their attributes.
いわゆるSELECT N+1問題は、ORMでよく見られるパフォーマンス問題です。オブジェクトのリストを取得する場合、ORMは最初のクエリーを実行して必要なオブジェクトのIDをすべて取得し、次に各オブジェクトに対して個別のクエリーを発行してその属性を取得することがよくあります。
This is especially likely if there are any foreign-key relationships on your objects.
これは、オブジェクトに外部キーのリレーションシップがある場合に特に起こりがちです。

---
---

- NOTE ノート

In all fairness, we should say that SQLAlchemy is quite good at avoiding the SELECT N+1 problem.
公平に見て、SQLAlchemy は SELECT N+1 の問題を避けるのに非常に優れていると言うべきでしょう。
It doesn’t display it in the preceding example, and you can request eager loading explicitly to avoid it when dealing with joined objects.
先の例では表示されませんし、結合したオブジェクトを扱うときには、それを避けるために明示的にイーガーローディングを要求することができます。

---
---

Beyond `SELECT N+1`, you may have other reasons for wanting to decouple the way you persist state changes from the way that you retrieve current state.
SELECT N+1` 以外にも、状態の変化を持続させる方法と現在の状態を取得する方法を切り離したい理由があるかもしれません。
A set of fully normalized relational tables is a good way to make sure that write operations never cause data corruption.
完全に正規化されたリレーショナルテーブルのセットは、書き込み操作によってデータが破損することがないようにするための良い方法である。
But retrieving data using lots of joins can be slow.
しかし、多くの結合を使用してデータを取得すると、時間がかかることがあります。
It’s common in such cases to add some denormalized views, build read replicas, or even add caching layers.
このような場合、非正規化ビューを追加したり、リードレプリカを構築したり、あるいはキャッシュ層を追加するのが一般的です。

## Time to Completely Jump the Shark Time to Completely Jump the Shark（シャークを完全に飛び越える時

On that note: have we convinced you that our raw SQL version isn’t so weird as it first seemed?
その点、私たちのRaw SQLバージョンは、最初に感じたほど奇妙なものではないということを納得していただけたでしょうか。
Perhaps we were exaggerating for effect?
もしかしたら、私たちは効果的に誇張していたのかもしれません。
Just you wait.
待っててください。

So, reasonable or not, that hardcoded SQL query is pretty ugly, right?
合理的であろうとなかろうと、ハードコードされたSQLクエリはかなり不格好ですよね？
What if we made it nicer…
もし、それをもっと素敵なものにしたらどうでしょう？

A much nicer query (src
もっと素敵なクエリ（src

```python
def allocations(orderid: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = list(uow.session.execute(
            'SELECT sku, batchref FROM allocations_view WHERE orderid = :orderid',
            dict(orderid=orderid)
        ))
        ...
```

…by keeping a totally separate, denormalized data store for our view model?
...ビューモデルのために、非正規化されたデータストアを完全に分離しておくことで、？

Hee hee hee, no foreign keys, just strings, YOLO (src
へーきへーき、外部キーもなく文字列だけ、YOLO (src

```python
allocations_view = Table(
    'allocations_view', metadata,
    Column('orderid', String(255)),
    Column('sku', String(255)),
    Column('batchref', String(255)),
)
```

OK, nicer-looking SQL queries wouldn’t be a justification for anything really, but building a denormalized copy of your data that’s optimized for read operations isn’t uncommon, once you’ve reached the limits of what you can do with indexes.
しかし、インデックスでできることの限界に達したら、読み取り操作に最適化されたデータの非正規化コピーを構築することは珍しいことではありません。

Even with well-tuned indexes, a relational database uses a lot of CPU to perform joins.
うまく調整されたインデックスを使用しても、リレーショナルデータベースは結合を実行するために多くのCPUを使用します。
The fastest queries will always be `SELECT * from mytable WHERE key = :value`.
最速のクエリは常に `SELECT * from mytable WHERE key = :value` となります。

More than raw speed, though, this approach buys us scale.
しかし、このアプローチでは、スピードよりもスケールの方が重要です。
When we’re writing data to a relational database, we need to make sure that we get a lock over the rows we’re changing so we don’t run into consistency problems.
リレーショナルデータベースにデータを書き込む場合、一貫性の問題が発生しないように、変更する行を確実にロックする必要があります。

If multiple clients are changing data at the same time, we’ll have weird race conditions.
複数のクライアントが同時にデータを変更すると、奇妙なレースコンディションが発生します。
When we’re reading data, though, there’s no limit to the number of clients that can concurrently execute.
しかし、データを読み込む場合は、同時実行できるクライアントの数に制限はありません。
For this reason, read-only stores can be horizontally scaled out.
このため、読み取り専用ストアは水平方向にスケールアウトすることが可能です。

---
---

- TIP ティップ

Because read replicas can be inconsistent, there’s no limit to how many we can have.
リードレプリカは一貫性がないので、いくつあっても困らない。
If you’re struggling to scale a system with a complex data store, ask whether you could build a simpler read model.
複雑なデータストアを持つシステムの拡張に苦労している場合は、よりシンプルな読み取りモデルを構築できないかどうか尋ねてみてください。

---
---

Keeping the read model up to date is the challenge!
読み取りモデルを常に最新の状態に保つことが課題です
Database views (materialized or otherwise) and triggers are a common solution, but that limits you to your database.
データベースのビュー（マテリアライズド、その他）やトリガーは一般的な解決策ですが、これではデータベースに制限されてしまいます。
We’d like to show you how to reuse our event-driven architecture instead.
代わりにイベント駆動型アーキテクチャを再利用する方法を紹介したいと思います。

### Updating a Read Model Table Using an Event Handler イベントハンドラを使用した読み取りモデルテーブルの更新

We add a second handler to the `Allocated` event:
Allocated`イベントに2つ目のハンドラを追加する。

Allocated event gets a new handler (src
割り当てられたイベントは、新しいハンドラーを取得します（src

```python
EVENT_HANDLERS = {
    events.Allocated: [
        handlers.publish_allocated_event,
        handlers.add_allocation_to_read_model
    ],
```

Here’s what our update-view-model code looks like:
update-view-modelのコードはこんな感じです。

Update on allocation (src
アロケーションの更新（src

```python
def add_allocation_to_read_model(
        event: events.Allocated, uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            'INSERT INTO allocations_view (orderid, sku, batchref)'
            ' VALUES (:orderid, :sku, :batchref)',
            dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref)
        )
        uow.commit()
```

Believe it or not, that will pretty much work!
信じられないかもしれませんが、これはかなりうまくいきますよ。
And it will work against the exact same integration tests as the rest of our options.
しかも、他の選択肢と全く同じ統合テストに対して動作します。

OK, you’ll also need to handle `Deallocated`:
OK、`Deallocated`の処理も必要です。

A second listener for read model updates
モデルの更新を読み取るための2番目のリスナー

```python
events.Deallocated: [
    handlers.remove_allocation_from_read_model,
    handlers.reallocate
],

...

def remove_allocation_from_read_model(
        event: events.Deallocated, uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            'DELETE FROM allocations_view '
            ' WHERE orderid = :orderid AND sku = :sku',
```

Figure 12-2 shows the flow across the two requests.
図12-2に、2つのリクエストにまたがるフローを示します。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1202.png)

In Figure 12-2, you can see two transactions in the POST
図12-2では、POSTの2つのトランザクションが表示されています。

---
---

- REBUILDING FROM SCRATCH 一からやり直し

“What happens when it breaks?” should be the first question we ask as engineers.
"壊れたらどうするのか？"というのは、エンジニアとして最初に問うべきことです。

How do we deal with a view model that hasn’t been updated because of a bug or temporary outage?
バグや一時的な停止でビューモデルが更新されていない場合、どのように対処すればいいのでしょうか。
Well, this is just another case where events and commands can fail independently.
まあ、これはイベントとコマンドが独立して失敗する可能性がある別のケースなんだけどね。

If we never updated the view model, and the `ASYMMETRICAL-DRESSER` was forever in stock, that would be annoying for customers, but the `allocate` service would still fail, and we’d take action to fix the problem.
ビューモデルを更新せず、`ASYMMETRICAL-DRESSER`がいつまでも在庫切れだった場合、顧客にとっては迷惑な話ですが、それでも`allocate`サービスは失敗し、問題を解決するための行動を取ることになります。

Rebuilding a view model is easy, though.
ビューモデルの再構築は簡単ですが。
Since we’re using a service layer to update our view model, we can write a tool that does the following:
ビューモデルの更新にサービスレイヤーを使っているので、以下のようなツールを書けばいいのです。

Queries the current state of the write side to work out what’s currently allocated
書き込み側の現在の状態を照会して、現在割り当てられているものを調べる

Calls the `add_allocate_to_read_model` handler for each allocated item
割り当てられたアイテムごとに `add_allocate_to_read_model` ハンドラを呼び出す。

We can use this technique to create entirely new read models from historical data.
この技術を使えば、過去のデータから全く新しい読み取りモデルを作ることができる。

---
---

## Changing Our Read Model Implementation Is Easy 読み上げモデルの実装変更は簡単です

Let’s see the flexibility that our event-driven model buys us in action, by seeing what happens if we ever decide we want to implement a read model by using a totally separate storage engine, Redis.
イベントドリブンモデルがもたらす柔軟性を、実際に見てみましょう。

Just watch:
見ているだけでいい。

Handlers update a Redis read model (src
ハンドラはRedisのリードモデル（src）を更新します。

```python
def add_allocation_to_read_model(event: events.Allocated, _):
    redis_eventpublisher.update_readmodel(event.orderid, event.sku, event.batchref)

def remove_allocation_from_read_model(event: events.Deallocated, _):
    redis_eventpublisher.update_readmodel(event.orderid, event.sku, None)
```

The helpers in our Redis module are one-liners:
Redisモジュールのヘルパーはワンライナーです。

Redis read model read and update (src
Redisリードモデルの読み込みと更新（src

```python
def update_readmodel(orderid, sku, batchref):
    r.hset(orderid, sku, batchref)


def get_readmodel(orderid):
    return r.hgetall(orderid)
```

(Maybe the name redis_eventpublisher.py is a misnomer now, but you get the idea.)
(今となってはredis_eventpublisher.pyという名前は語弊があるかもしれませんが、お分かりいただけると思います)。

And the view itself changes very slightly to adapt to its new backend:
そして、新しいバックエンドに適応するために、ビュー自体もごくわずかに変化します。

View adapted to Redis (src
Redisに適応したビュー（src

```python
def allocations(orderid):
    batches = redis_eventpublisher.get_readmodel(orderid)
    return [
        {'batchref': b.decode(), 'sku': s.decode()}
        for s, b in batches.items()
    ]
```

And the exact same integration tests that we had before still pass, because they are written at a level of abstraction that’s decoupled from the implementation: setup puts messages on the message bus, and the assertions are against our view.
なぜなら、実装から切り離された抽象的なレベルで書かれているからです。セットアップはメッセージバスにメッセージを置き、アサーションは我々のビューに対して行われます。

---
---

- TIP ティップ

Event handlers are a great way to manage updates to a read model, if you decide you need one.
イベントハンドラは、読み取りモデルの更新を管理するのに最適な方法です（必要だと判断した場合）。
They also make it easy to change the implementation of that read model at a later date.
また、後日、その読み取りモデルの実装を変更することも容易になります。

---
---

---
---

- EXERCISE FOR THE READER どくたんぎょう

Implement another view, this time to show the allocation for a single order line.
別のビューを実装し、今度は1つの注文行の割り当てを表示します。

Here the trade-offs between using hardcoded SQL versus going via a repository should be much more blurry.
ハードコードされたSQLを使うか、リポジトリを経由するかというトレードオフは、より曖昧になるはずです。
Try a few versions (maybe including going to Redis), and see which you prefer.
いくつかのバージョン（Redisへの移行も含む）を試してみて、どちらがいいかを考えてみてください。

---
---

## Wrap-Up ラップアップ

Table 12-2 proposes some pros and cons for each of our options.
表12-2は、それぞれの選択肢について、いくつかの長所と短所を提案している。

As it happens, the allocation service at MADE.com does use “full-blown” CQRS, with a read model stored in Redis, and even a second layer of cache provided by Varnish.
実際、MADE.comのアロケーションサービスでは、Redisに保存されたリードモデルや、Varnishによる2層目のキャッシュなど、「本格的な」CQRSを使用しています。
But its use cases are quite a bit different from what we’ve shown here.
しかし、そのユースケースは今回紹介したものとはかなり異なっています。
For the kind of allocation service we’re building, it seems unlikely that you’d need to use a separate read model and event handlers for updating it.
私たちが構築しているような割り当てサービスでは、別の読み取りモデルとそれを更新するためのイベントハンドラを使用する必要はなさそうです。

But as your domain model becomes richer and more complex, a simplified read model become ever more compelling.
しかし、ドメインモデルがリッチで複雑になるにつれ、簡略化された読み取りモデルがますます説得力を持つようになります。

Table 12-2.
表12-2.
Trade-offs of various view model options
様々なビューモデルオプションのトレードオフ



















Often, your read operations will be acting on the same conceptual objects as your write model, so using the ORM, adding some read methods to your repositories, and using domain model classes for your read operations is just fine.
多くの場合、読み取り操作は書き込みモデルと同じ概念オブジェクトに対して行われるため、ORMを使用し、いくつかの読み取りメソッドをリポジトリに追加し、読み取り操作にドメインモデルクラスを使用することがちょうどよいのです。

In our book example, the read operations act on quite different conceptual entities to our domain model.
この本の例では、読み取り操作は、ドメインモデルとはまったく異なる概念的なエンティティに作用します。
The allocation service thinks in terms of `Batches` for a single SKU, but users care about allocations for a whole order, with multiple SKUs, so using the ORM ends up being a little awkward.
割り当てサービスは1つのSKUに対して`バッチ`という単位で考えますが、ユーザーは複数のSKUを含む注文全体に対する割り当てを気にするので、ORMを使うのは少し厄介なことに終わります。
We’d be quite tempted to go with the raw-SQL view we showed right at the beginning of the chapter.
この章の冒頭で紹介した生のSQLビューを使いたくなりますね。

On that note, let’s sally forth into our final chapter.
それでは、最終章に突入です。
