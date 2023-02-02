# Chapter 8. Events and the Message Bus 第8章 イベントとメッセージバス イベントとメッセージバス

So far we’ve spent a lot of time and energy on a simple problem that we could easily have solved with Django.
これまで私たちは、Django で簡単に解決できた単純な問題に、多くの時間とエネルギーを費やしてきました。
You might be asking if the increased testability and expressiveness are really worth all the effort.
テスト容易性と表現力の向上が、本当にすべての努力に見合うものなのかどうか、 疑問に思っているかもしれません。

In practice, though, we find that it’s not the obvious features that make a mess of our codebases: it’s the goop around the edge.
しかし、実際には、コードベースを混乱させるのは、明らかな機能ではなく、その周辺にあるゴミなのです。
It’s reporting, and permissions, and workflows that touch a zillion objects.
レポート、パーミッション、ワークフローなど、多くのオブジェクトに触れているのです。

Our example will be a typical notification requirement: when we can’t allocate an order because we’re out of stock, we should alert the buying team.
この例では、典型的な通知要件として、在庫切れで注文を割り当てられない場合、購買チームに警告する必要があります。
They’ll go and fix the problem by buying more stock, and all will be well.
在庫切れのため注文を割り当てられない場合、購買チームに警告する必要があります。購買チームは在庫を買い足して問題を解決し、すべてがうまくいくでしょう。

For a first version, our product owner says we can just send the alert by email.
最初のバージョンでは、製品オーナーは、電子メールでアラートを送信すればよいと言います。

Let’s see how our architecture holds up when we need to plug in some of the mundane stuff that makes up so much of our systems.
では、私たちのシステムの多くを占める、ありふれたものを接続したときに、このアーキテクチャがどのように耐えられるか見てみましょう。

We’ll start by doing the simplest, most expeditious thing, and talk about why it’s exactly this kind of decision that leads us to the Big Ball of Mud.
まずは、最もシンプルで手軽な方法から始めて、なぜ、このような判断が「泥の大箱」につながってしまうのか、その理由をお話しします。

Then we’ll show how to use the Domain Events pattern to separate side effects from our use cases, and how to use a simple Message Bus pattern for triggering behavior based on those events.
次に、Domain Eventsパターンを使ってユースケースから副作用を分離する方法と、これらのイベントに基づいて動作をトリガーするためのシンプルなMessage Busパターンを使う方法を紹介します。
We’ll show a few options for creating those events and how to pass them to the message bus, and finally we’ll show how the Unit of Work pattern can be modified to connect the two together elegantly, as previewed in Figure 8-1.
これらのイベントを作成するためのいくつかのオプションと、それらをメッセージバスに渡す方法を紹介し、最後に図8-1でプレビューしたように、Unit of Workパターンを修正して、この2つをエレガントに接続する方法を紹介する。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0801.png)

TIP
ヒント

The code for this chapter is in the chapter_08_events_and_message_bus branch on GitHub:
この章のコードは、GitHubのchapter_08_events_and_message_busブランチにあります。

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_08_events_and_message_bus
# or to code along, checkout the previous chapter:
git checkout chapter_07_aggregate
```

## Avoiding Making a Mess ♪混乱を避けるために

So.
だから
Email alerts when we run out of stock.
在庫が無くなった時のメール通知。
When we have new requirements like ones that really have nothing to do with the core domain, it’s all too easy to start dumping these things into our web controllers.
コア・ドメインとは全く関係ないような 新しい要件があると ウェブ・コントローラーにこれらのものを 投入し始めるのはあまりにも簡単です。

### First, Let’s Avoid Making a Mess of Our Web Controllers まず、ウェブコントローラーを混乱させないようにしよう

As a one-off hack, this might be OK:
一回限りのハックとしては、これでOKかもしれません。

Just whack it in the endpoint—what could go wrong?
エンドポイントに叩き込むだけ-何が問題なのか？
(src
(src

```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    line = model.OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )
    try:
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        batchref = services.allocate(line, uow)
    except (model.OutOfStock, services.InvalidSku) as e:
        send_mail(
            'out of stock',
            'stock_admin@made.com',
            f'{line.orderid} - {line.sku}'
        )
        return jsonify({'message': str(e)}), 400

    return jsonify({'batchref': batchref}), 201
```

…but it’s easy to see how we can quickly end up in a mess by patching things up like this.
...しかし、このようにパッチを適用することで、すぐに混乱に陥ることは容易に想像できます。
Sending email isn’t the job of our HTTP layer, and we’d like to be able to unit test this new feature.
メールの送信はHTTPレイヤーの仕事ではありませんし、この新しい機能をユニットテストできるようにしたいのです。

### And Let’s Not Make a Mess of Our Model Either そして、私たちのモデルも台無しにしないようにしましょう。

Assuming we don’t want to put this code into our web controllers, because we want them to be as thin as possible, we may look at putting it right at the source, in the model:
ウェブコントローラはできるだけ薄くしたいので、このコードをウェブコントローラに入れたくないと仮定すると、このコードをソースであるモデルに直接入れることになるかもしれません。

Email-sending code in our model isn’t lovely either (src
私たちのモデルのメール送信コードも素敵ではありません (src

```python
    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
            )
            #...
        except StopIteration:
            email.send_mail('stock@made.com', f'Out of stock for {line.sku}')
            raise OutOfStock(f'Out of stock for sku {line.sku}')
```

But that’s even worse!
しかし、それはさらに悪いことです
We don’t want our model to have any dependencies on infrastructure concerns like `email.send_mail`.
私たちのモデルには、`email.send_mail`のようなインフラストラクチャへの依存性を持たせたくありません。

This email-sending thing is unwelcome goop messing up the nice clean flow of our system.
このメール送信の件は、私たちのシステムのきれいな流れを台無しにする歓迎されないグープです。
What we’d like is to keep our domain model focused on the rule “You can’t allocate more stuff than is actually available.”
私たちが望むのは、ドメインモデルを "実際に利用できる以上のものを割り当ててはいけない "というルールに集中させ続けることです。

The domain model’s job is to know that we’re out of stock, but the responsibility of sending an alert belongs elsewhere.
ドメインモデルの仕事は、在庫がないことを知ることですが、アラートを送る責任は他にあります。
We should be able to turn this feature on or off, or to switch to SMS notifications instead, without needing to change the rules of our domain model.
ドメインモデルのルールを変更することなく、この機能をオンにしたりオフにしたり、代わりにSMS通知に切り替えたりすることができるはずです。

### Or the Service Layer! サービス層でもいい!

The requirement “Try to allocate some stock, and send an email if it fails” is an example of workflow orchestration: it’s a set of steps that the system has to follow to achieve a goal.
在庫の割り当てを試み、失敗したらメールを送る」という要件は、ワークフロー・オーケストレーションの一例です：これは、システムが目標を達成するために従わなければならない一連のステップです。

We’ve written a service layer to manage orchestration for us, but even here the feature feels out of place:
私たちは、オーケストレーションを管理するためのサービスレイヤーを書きましたが、ここでもこの機能は場違いな感じがします。

And in the service layer, it’s out of place (src
そして、サービス層では、場違い（src

```python
def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        try:
            batchref = product.allocate(line)
            uow.commit()
            return batchref
        except model.OutOfStock:
            email.send_mail('stock@made.com', f'Out of stock for {line.sku}')
            raise
```

Catching an exception and reraising it?
例外をキャッチして再レイズ？
It could be worse, but it’s definitely making us unhappy.
もっとひどいかもしれませんが、間違いなく私たちを不幸にしています。
Why is it so hard to find a suitable home for this code?
なぜこのコードに適した家を見つけるのがこんなに難しいのでしょうか？

## Single Responsibility Principle 単一責任原則

Really, this is a violation of the single responsibility principle (SRP).1 Our use case is allocation.
本当に、これは単一責任原則(SRP)に違反しています。1 私たちのユースケースはアロケーションです。
Our endpoint, service function, and domain methods are all called `allocate`, not `allocate_and_send_mail_if_out_of_stock`.
私たちのエンドポイント、サービス関数、ドメインのメソッドはすべて `allocate` と呼ばれ、`allocate_and_send_mail_if_out_of_stock` と呼ばれることはないのです。

- TIP ヒント

- Rule of thumb: if you can’t describe what your function does without using words like “then” or “and,” you might be violating the SRP. 経験則：もし、「then」や「and」といった言葉を使わずに関数の動作を説明できない場合、SRPに違反している可能性があります。

One formulation of the SRP is that each class should have only a single reason to change.
SRPの一つの定式化は、各クラスが変更する理由はただ一つであるべきだということです。
When we switch from email to SMS, we shouldn’t have to update our `allocate()` function, because that’s clearly a separate responsibility.
電子メールから SMS に切り替えるとき、`allocate()` 関数を更新する必要はありません。

To solve the problem, we’re going to split the orchestration into separate steps so that the different concerns don’t get tangled up.2 The domain model’s job is to know that we’re out of stock, but the responsibility of sending an alert belongs elsewhere.
この問題を解決するために、オーケストレーションを別々のステップに分割し、異なる懸念が絡まないようにします。2 ドメインモデルの仕事は、在庫切れを知ることですが、アラートを送る責任は別のところに属します。
We should be able to turn this feature on or off, or to switch to SMS notifications instead, without needing to change the rules of our domain model.
ドメインモデルの仕事は、在庫切れを知ることですが、アラートを送る責任は他にあります。この機能をオンにしたりオフにしたり、代わりにSMS通知に切り替えることは、ドメインモデルのルールを変更する必要なくできるはずです。

We’d also like to keep the service layer free of implementation details.
また、サービス層は実装の詳細から解放された状態に保ちたいと考えています。
We want to apply the dependency inversion principle to notifications so that our service layer depends on an abstraction, in the same way as we avoid depending on the database by using a unit of work.
私たちは依存関係の逆転原理をnotificationに適用し、サービス層が抽象化されたものに依存するようにしたいと思います。

## All Aboard the Message Bus! ♪みんなでメッセージバスに乗ろう！

The patterns we’re going to introduce here are Domain Events and the Message Bus.
今回紹介するのは、ドメインイベントとメッセージバスのパターンです。
We can implement them in a few ways, so we’ll show a couple before settling on the one we like most.
これらのパターンはいくつかの方法で実装することができるので、いくつか紹介した後、最も気に入ったものに決定します。

### The Model Records Events モデルにはイベントが記録される

First, rather than being concerned about emails, our model will be in charge of recording events—facts about things that have happened.
まず、このモデルでは、メールではなく、イベント（起こったこと）を記録することに専念します。
We’ll use a message bus to respond to events and invoke a new operation.
メッセージバスを使って、イベントに応答し、新しいオペレーションを呼び出すことにします。

### Events Are Simple Dataclasses イベントは単純なデータクラス

An event is a kind of value object.
イベントは値オブジェクトの一種です。
Events don’t have any behavior, because they’re pure data structures.
イベントは純粋なデータ構造であるため、動作を持ちません。
We always name events in the language of the domain, and we think of them as part of our domain model.
イベントは常にドメイン言語で命名され、ドメインモデルの一部とみなされます。

We could store them in model.py, but we may as well keep them in their own file (this might be a good time to consider refactoring out a directory called domain so that we have domain
model.pyに格納することもできますが、独自のファイルに格納する方が良いでしょう（これは、domainというディレクトリをリファクタリングすることを検討する良い機会かもしれませんので、 domain

Event classes (src
イベントクラス（src

```python
from dataclasses import dataclass

class Event:  1
    pass

@dataclass
class OutOfStock(Event):  2
    sku: str

```

1. Once we have a number of events, we’ll find it useful to have a parent class that can store common attributes. It’s also useful for type hints in our message bus, as you’ll see shortly. イベントが多数になると、共通の属性を保存できる親クラスがあると便利だと思います。 また、まもなく見るように、メッセージバスのタイプヒントにも便利です。

2. `dataclasses` are great for domain events too. データクラス`はドメインイベントにも最適です。

### The Model Raises Events モデルがイベントを発生させる

When our domain model records a fact that happened, we say it raises an event.
ドメインモデルが、起こった事実を記録することを、イベントを発生させると言う。

Here’s what it will look like from the outside; if we ask `Product` to allocate but it can’t, it should raise an event:
外から見るとこんな感じです。もし `Product` に割り当てを要求して割り当てができなかったら、イベントを発生させる必要があります。

Test our aggregate to raise events (tests
イベントを発生させるためのアグリゲートをテストする (tests

```python
def test_records_out_of_stock_event_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    product = Product(sku="SMALL-FORK", batches=[batch])
    product.allocate(OrderLine('order1', 'SMALL-FORK', 10))

    allocation = product.allocate(OrderLine('order2', 'SMALL-FORK', 1))
    assert product.events[-1] == events.OutOfStock(sku="SMALL-FORK")  1
    assert allocation is None
```

1. Our aggregate will expose a new attribute called `.events` that will contain a list of facts about what has happened, in the form of `Event` objects. 私たちのアグリゲートは `.events` という新しい属性を公開します。この属性には、起こったことに関する事実のリストが `Event` オブジェクトの形で格納されます。

Here’s what the model looks like on the inside:
モデルの内部はこんな感じです。

The model raises a domain event (src
モデルはドメインイベントを発生させる（src

```python
class Product:

    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number
        self.events = []  # type: List[events.Event]  1

    def allocate(self, line: OrderLine) -> str:
        try:
            #...
        except StopIteration:
            self.events.append(events.OutOfStock(line.sku))  2
            # raise OutOfStock(f'Out of stock for sku {line.sku}')  3
            return None
```

1. Here’s our new .events attribute in use. 新しい.events属性が使用されている様子です。

2. Rather than invoking some email-sending code directly, we record those events at the place they occur, using only the language of the domain. メール送信のコードを直接呼び出すのではなく、それらのイベントが発生した場所で、ドメインの言語のみを使用して記録します。

3. We’re also going to stop raising an exception for the out-of-stock case. The event will do the job the exception was doing. また、在庫切れの場合に例外を発生させることもやめようと思います。 例外がやっていた仕事を、イベントがやってくれるようになります。

- NOTE 注

- We’re actually addressing a code smell we had until now, which is that we were using exceptions for control flow. In general, if you’re implementing domain events, don’t raise exceptions to describe the same domain concept. As you’ll see later when we handle events in the Unit of Work pattern, it’s confusing to have to reason about events and exceptions together. 実は今まであったコードの臭い、つまり制御フローに例外を使っていたことに対処しているのです。 一般に、ドメインイベントを実装する場合、同じドメインコンセプトを表現するために例外を発生させないようにしましょう。 後でUnit of Workパターンでイベントを処理するときにわかりますが、イベントと例外を一緒に理由づけしなければならないのは混乱します。

### The Message Bus Maps Events to Handlers メッセージバスはイベントをハンドラにマッピングする

A message bus basically says, “When I see this event, I should invoke the following handler function.”
メッセージバスは、基本的に "このイベントを見たら、次のハンドラ関数を呼び出すように "というものだ。
In other words, it’s a simple publish-subscribe system.
言い換えれば、単純なパブリッシュ・サブスクライブシステムです。
Handlers are subscribed to receive events, which we publish to the bus.
ハンドラはイベントを受信するためにサブスクライブされ、それをバスにパブリッシュする。
It sounds harder than it is, and we usually implement it with a dict:
実際より難しそうに聞こえるので、通常はdictで実装する。

Simple message bus (src
シンプルなメッセージバス（src

```python
def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_out_of_stock_notification(event: events.OutOfStock):
    email.send_mail(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )


HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification],

}  # type: Dict[Type[events.Event], List[Callable]]
```

- NOTE 注

- Note that the message bus as implemented doesn’t give us concurrency because only one handler will run at a time. Our objective isn’t to support parallel threads but to separate tasks conceptually, and to keep each UoW as small as possible. This helps us to understand the codebase because the “recipe” for how to run each use case is written in a single place. See the following sidebar. メッセージバスの実装では、一度に一つのハンドラしか実行されないため、同時並行性が得られないことに注意してください。 私たちの目的は、並列スレッドをサポートすることではなく、タスクを概念的に分離し、各UoWをできるだけ小さくすることです。 これは、各ユースケースを実行する方法の「レシピ」が一箇所に書かれているため、コードベースを理解するのに役立つのです。 次のサイドバーを参照してください。

- IS THIS LIKE CELERY? は、セロリのようなものでしょうか？

- Celery is a popular tool in the Python world for deferring self-contained chunks of work to an asynchronous task queue. The message bus we’re presenting here is very different, so the short answer to the above question is no; our message bus has more in common with a Node.js app, a UI event loop, or an actor framework. Celeryは、Pythonの世界では、自己完結した仕事の塊を非同期タスクキューに先送りするためのツールとして人気があります。 このメッセージバスは、Node.jsのアプリやUIのイベントループ、あるいはアクターフレームワークと共通点が多いのです。

- If you do have a requirement for moving work off the main thread, you can still use our event-based metaphors, but we suggest you use external events for that. There’s more discussion in Table 11-1, but essentially, if you implement a way of persisting events to a centralized store, you can subscribe other containers or other microservices to them. Then that same concept of using events to separate responsibilities across units of work within a single process/service can be extended across multiple processes—which may be different containers within the same service, or totally different microservices. メインスレッドから作業を移す要件がある場合、イベントベースのメタファーをまだ使用できますが、その場合は外部イベントを使用することをお勧めします。 表11-1に詳しい説明がありますが、基本的には、イベントを集中型ストアに永続化する方法を実装すれば、他のコンテナや他のマイクロサービスをそれにサブスクライブすることができます。 次に、イベントを使用して、単一のプロセス内の作業単位間で責任を分離するという同じコンセプトがあります。

- If you follow us in this approach, your API for distributing tasks is your event classes—or a JSON representation of them. This allows you a lot of flexibility in who you distribute tasks to; they need not necessarily be Python services. Celery’s API for distributing tasks is essentially “function name plus arguments,” which is more restrictive, and Python-only. このアプローチに従えば、タスクを配布するためのAPIはイベントクラスか、そのJSON表現になります。 これにより、タスクを配布する相手がPythonのサービスである必要はなく、非常に柔軟に対応することができます。 Celeryのタスク配信APIは、基本的に「関数名＋引数」であり、より制約が多く、Python専用となります。

## Option 1: The Service Layer Takes Events from the Model and Puts Them on the Message Bus Option 1: サービス層はモデルからイベントを受け取り、メッセージバスに載せる

Our domain model raises events, and our message bus will call the right handlers whenever an event happens.
ドメインモデルはイベントを発生させ、メッセージバスはイベントが発生するたびに適切なハンドラを呼び出します。
Now all we need is to connect the two.
あとは、この2つをつなげるだけです。
We need something to catch events from the model and pass them to the message bus—the publishing step.
モデルからのイベントをキャッチし、メッセージバスに渡すものが必要です。これがパブリッシングのステップです。

The simplest way to do this is by adding some code into our service layer:
これを実現する最も簡単な方法は、サービスレイヤーにいくつかのコードを追加することです。

The service layer with an explicit message bus (src
明示的なメッセージバスを持つサービス層（src

```python
from . import messagebus
...

def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        try:  1
            batchref = product.allocate(line)
            uow.commit()
            return batchref
        finally:  1
            messagebus.handle(product.events)  2
```

1. We keep the try/finally from our ugly earlier implementation (we haven’t gotten rid of all exceptions yet, just OutOfStock). 私たちは、トライを続ける

2. But now, instead of depending directly on an email infrastructure, the service layer is just in charge of passing events from the model up to the message bus. しかし今度は、メールインフラに直接依存するのではなく、サービス層はモデルからメッセージバスにイベントを渡すことだけを担当するようになりました。

That already avoids some of the ugliness that we had in our naive implementation, and we have several systems that work like this one, in which the service layer explicitly collects events from aggregates and passes them to the message bus.
このように、サービス層が明示的にアグリゲートからイベントを収集し、メッセージバスに渡すような仕組みのシステムもいくつかあります。

## Option 2: The Service Layer Raises Its Own Events Option 2: サービス層は独自のイベントを発生させる

Another variant on this that we’ve used is to have the service layer in charge of creating and raising events directly, rather than having them raised by the domain model:
また、ドメインモデルからイベントを発生させるのではなく、サービスレイヤーが直接イベントの作成と発生を担当するのも、このバリエーションになります。

Service layer calls messagebus.handle directly (src
サービス層はmessagebus.handleを直接呼び出す（src

```python
def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit() 1

        if batchref is None:
            messagebus.handle(events.OutOfStock(line.sku))
        return batchref
```

1. As before, we commit even if we fail to allocate because the code is simpler this way and it’s easier to reason about: we always commit unless something goes wrong. Committing when we haven’t changed anything is safe and keeps the code uncluttered. この方がコードがシンプルになり、理屈もつけやすいからです。何か問題が起きない限り、常にコミットします。 何も変更していないときにコミットすることは、安全であり、コードをすっきりさせることができます。

Again, we have applications in production that implement the pattern in this way.
繰り返しになりますが、このパターンを実装したアプリケーションは実稼働しています。
What works for you will depend on the particular trade-offs you face, but we’d like to show you what we think is the most elegant solution, in which we put the unit of work in charge of collecting and raising events.
何がうまくいくかは、あなたが直面する特定のトレードオフに依存しますが、私たちが最もエレガントだと思う解決策をお見せしたいと思います。それは、作業単位にイベントの収集と発生を担当させるというものです。

## Option 3: The UoW Publishes Events to the Message Bus オプション 3: UoW がイベントをメッセージバスに発行する

The UoW already has a `try
UoWはすでに`try'を搭載しています。

The UoW meets the message bus (src
UoWがメッセージバスに出会い（src

```python
class AbstractUnitOfWork(abc.ABC):
    ...

    def commit(self):
        self._commit()  1
        self.publish_events()  2

    def publish_events(self):  2
        for product in self.products.seen:  3
            while product.events:
                event = product.events.pop(0)
                messagebus.handle(event)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

...

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    ...

    def _commit(self):  1
        self.session.commit()
```

1. We’ll change our commit method to require a private .\_commit() method from subclasses. サブクラスから private .\_commit() メソッドを要求するようにコミットメソッドを変更します。

2. After committing, we run through all the objects that our repository has seen and pass their events to the message bus. コミットした後、リポジトリが見たすべてのオブジェクトを実行し、そのイベントをメッセージバスに渡します。

3. That relies on the repository keeping track of aggregates that have been loaded using a new attribute, .seen, as you’ll see in the next listing. これは、次のリストで見るように、新しい属性である .seen を使って読み込まれたアグリゲートをリポジトリが追跡していることに依存します。

- NOTE 注

- Are you wondering what happens if one of the handlers fails? We’ll discuss error handling in detail in Chapter 10. ハンドラのひとつが失敗したらどうなるのか、気になりませんか？ エラー処理については、第10章で詳しく説明します。

Repository tracks aggregates that pass through it (src
リポジトリは、それを通過したアグリゲート（src）を追跡します。

```python
class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[model.Product]  1

    def add(self, product: model.Product):  2
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:  3
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product):  2
        raise NotImplementedError

    @abc.abstractmethod  3
    def _get(self, sku) -> model.Product:
        raise NotImplementedError



class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):  2
        self.session.add(product)

    def _get(self, sku):  3
        return self.session.query(model.Product).filter_by(sku=sku).first()
```

1. For the UoW to be able to publish new events, it needs to be able to ask the repository for which `Product` objects have been used during this session. We use a `set` called `.seen` to store them. That means our implementations need to call `super().__init__()`. UoW が新しいイベントを発行できるようにするには、このセッションでどの `Product` オブジェクトが使用されたかをリポジトリに問い合わせることができるようにする必要があります。 私たちは、それらを保存するために `.seen` という `set` を使用します。 つまり、私たちの実装では `super().__init__()` を呼び出す必要があるのです。

2. The parent `add()` method adds things to `.seen`, and now requires subclasses to implement `._add()`. 親クラスの `add()` メソッドは `.seen` に物を追加しますが、サブクラスには `._add()` の実装が必要になりました。

3. Similarly, `.get()` delegates to a `._get()` function, to be implemented by subclasses, in order to capture objects seen. 同様に、`.get()` は、見たオブジェクトを捕捉するために、サブクラスが実装する `._get()` 関数に委譲します。

- NOTE 注

- The use of `._underscorey()` methods and subclassing is definitely not the only way you could implement these patterns. Have a go at the Exercise for the Reader in this chapter and experiment with some alternatives. ._underscorey()` メソッドの使用とサブクラス化は、これらのパターンを実装するための唯一の方法であることは間違いありません。 この章の「読者のための練習問題」を読んで、いくつかの選択肢を試してみてください。

After the UoW and repository collaborate in this way to automatically keep track of live objects and process their events, the service layer can be totally free of event-handling concerns:
UoWとリポジトリがこのように連携して、生きているオブジェクトを自動的に追跡し、そのイベントを処理した後、サービス層はイベント処理に関する懸念から完全に解放されることになる。

Service layer is clean again (src
サービス層は再びきれいになった (src

```python
def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit()
        return batchref
```

We do also have to remember to change the fakes in the service layer and make them call `super()` in the right places, and to implement underscorey methods, but the changes are minimal:
また、サービスレイヤーのフェイクを変更し、適切な場所で `super()` を呼び出すようにしたり、アンダースコアのメソッドを実装することを忘れないようにしなければなりませんが、変更は最小限にとどめられます。

Service-layer fakes need tweaking (tests
サービスレイヤーのフェイクは微調整が必要（テスト

```python
class FakeRepository(repository.AbstractRepository):

    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product):
        self._products.add(product)

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

...

class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    ...

    def _commit(self):
        self.committed = True
```

- EXERCISE FOR THE READER 読書運動

- Are you finding all those `._add()` and `._commit()` methods “super-gross,” in the words of our beloved tech reviewer Hynek? Does it “make you want to beat Harry around the head with a plushie snake”? Hey, our code listings are only meant to be examples, not the perfect solution! Why not go see if you can do better? 私たちの愛する技術評論家ハイネックの言葉を借りれば、`._add()` と `._commit()` のすべてのメソッドが「超キモい」と感じていませんか？ ヘビのぬいぐるみでハリーの頭をぶん殴りたくなる」のでしょうか？ 私たちのコードリストはあくまでも例であって、完璧な解決策ではありませんよ。 もっといい方法がないか、試してみませんか？

One composition over inheritance way to go would be to implement a wrapper class:
継承を超えたコンポジションの1つの方法として、ラッパークラスを実装することが考えられます。

A wrapper adds functionality and then delegates (src
ラッパーは機能を追加し、その後デリゲート（src

```python
class TrackingRepository:
    seen: Set[model.Product]

    def __init__(self, repo: AbstractRepository):
        self.seen = set()  # type: Set[model.Product]
        self._repo = repo

    def add(self, product: model.Product):  1
        self._repo.add(product)  1
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._repo.get(sku)
        if product:
            self.seen.add(product)
        return product
```

1. By wrapping the repository, we can call the actual `.add()` and `.get()` methods, avoiding weird underscorey methods. リポジトリをラップすることで、実際の `.add()` と `.get()` メソッドを呼び出すことができ、変なアンダースコアを使ったメソッドを回避することができます。

- See if you can apply a similar pattern to our UoW class in order to get rid of those Java-y `_commit()` methods too. You can find the code on GitHub. 同じようなパターンをUoWクラスに適用して、Java的な `_commit()` メソッドを取り除くことができるかどうか見てみましょう。 このコードはGitHubで見ることができます。

- Switching all the ABCs to `typing.Protocol` is a good way to force yourself to avoid using inheritance. Let us know if you come up with something nice! ABCを全て`typing.Protocol`に切り替えることで、無理やり継承を使わないようにすることができます。 何かいい方法が思いついたら、ぜひ教えてください。

You might be starting to worry that maintaining these fakes is going to be a maintenance burden.
このようなフェイクを維持するのはメンテナンスの負担になるのではと心配になってきたのではないでしょうか。
There’s no doubt that it is work, but in our experience it’s not a lot of work.
作業であることは間違いありませんが、私たちの経験では、それほど大変な作業ではありません。
Once your project is up and running, the interface for your repository and UoW abstractions really don’t change much.
一度プロジェクトが立ち上がれば、リポジトリとUoWの抽象化のためのインターフェイスは本当にあまり変わりません。
And if you’re using ABCs, they’ll help remind you when things get out of sync.
また、ABCを使用している場合は、同期がとれなくなったときに、ABCが教えてくれます。

## Wrap-Up まとめ

Domain events give us a way to handle workflows in our system.
ドメインイベントは、システムでワークフローを処理するための方法です。
We often find, listening to our domain experts, that they express requirements in a causal or temporal way—for example, “When we try to allocate stock but there’s none available, then we should send an email to the buying team.”
例えば、「在庫を割り当てようとしたときに、在庫がない場合は、購買チームにメールを送る」というようにです。

The magic words “When X, then Y” often tell us about an event that we can make concrete in our system.
When X, then Y "という魔法の言葉は、しばしば、私たちのシステムで具体化できるイベントについて教えてくれます。
Treating events as first-class things in our model helps us make our code more testable and observable, and it helps isolate concerns.
イベントを第一級のものとしてモデル化することは、コードをよりテストしやすく、観察しやすくし、懸念を分離するのに役立ちます。

And Table 8-1 shows the trade-offs as we see them.
そして、表8-1は、私たちが考えるトレードオフを示したものである。

Table 8-1.
表8-1.
Domain events: the trade-offs
ドメインイベント：トレードオフ

- Pros 長所

- A message bus gives us a nice way to separate responsibilities when we have to take multiple actions in response to a request. メッセージバスは、リクエストに応答して複数のアクションを取らなければならないときに、責任を分離するための良い方法を提供します。

- Event handlers are nicely decoupled from the “core” application logic, making it easy to change their implementation later. イベントハンドラは、「コア」アプリケーションロジックからうまく切り離されているため、後から実装を変更することも容易です。

- Domain events are a great way to model the real world, and we can use them as part of our business language when modeling with stakeholders. ドメインイベントは実世界をモデル化する優れた方法であり、ステークホルダーとモデル化する際に、ビジネス言語の一部として使用することができるのです。

- Cons 短所

- The message bus is an additional thing to wrap your head around; the implementation in which the unit of work raises events for us is neat but also magic. It’s not obvious when we call `commit` that we’re also going to go and send email to people. メッセージバスはさらに頭を悩ませるものです。作業単位が私たちのためにイベントを発生させるという実装は、きちんとしたものですが、魔法でもあります。 コミット(commit`)を呼び出すときに、人々にメールを送信することは明らかではありません。

- What’s more, that hidden event-handling code executes synchronously, meaning your service-layer function doesn’t finish until all the handlers for any events are finished. That could cause unexpected performance problems in your web endpoints (adding asynchronous processing is possible but makes things even more confusing). さらに、その隠されたイベント処理コードは同期的に実行されます。つまり、サービスレイヤーの関数は、すべてのイベントのハンドラが終了するまで終了しません。 これは、ウェブエンドポイントに予期せぬパフォーマンスの問題を引き起こす可能性があります（非同期処理を追加することは可能ですが、事態をさらに混乱させます）。

- More generally, event-driven workflows can be confusing because after things are split across a chain of multiple handlers, there is no single place in the system where you can understand how a request will be fulfilled. より一般的には、イベント駆動型のワークフローは、複数のハンドラの連鎖によって物事が分割された後、リクエストがどのように実現されるかを理解できる単一の場所がシステム内に存在しないため、混乱することがあります。

- You also open yourself up to the possibility of circular dependencies between your event handlers, and infinite loops. また、イベントハンドラ間の循環的な依存関係や、無限ループの可能性も出てきます。

Events are useful for more than just sending email, though.
しかし、イベントは電子メールを送る以外にも便利です。
In Chapter 7 we spent a lot of time convincing you that you should define aggregates, or boundaries where we guarantee consistency.
第7章では、アグリゲート、つまり一貫性を保証する境界を定義する必要があることを納得させるために多くの時間を費やしました。
People often ask, “What should I do if I need to change multiple aggregates as part of a request?”
リクエストの一部として複数のアグリゲートを変更する必要がある場合、どうすればよいのでしょうか?" という質問がよくあります。
Now we have the tools we need to answer that question.
今、私たちはその質問に答えるために必要なツールを持っています。

If we have two things that can be transactionally isolated (e.g., an order and a product), then we can make them eventually consistent by using events.
トランザクション的に分離できる2つのもの(例えば、注文と商品)があれば、イベントを使うことで、最終的に整合性を持たせることができる。
When an order is canceled, we should find the products that were allocated to it and remove the allocations.
注文がキャンセルされたら、それに割り当てられていた商品を探し出し、割り当てを削除する必要があります。

- DOMAIN EVENTS AND THE MESSAGE BUS RECAP ドメインイベントとメッセージバスの再録

- Events can help with the single responsibility principle イベントは単一責任原則に役立つ

- Code gets tangled up when we mix multiple concerns in one place. Events can help us to keep things tidy by separating primary use cases from secondary ones. We also use events for communicating between aggregates so that we don’t need to run long-running transactions that lock against multiple tables. 複数の関心事が混在していると、コードがこんがらがってしまいます。 イベントは、一次的なユースケースと二次的なユースケースを分離することで、物事を整理整頓するのに役立っています。 また、アグリゲート間の通信にもイベントを利用し、複数のテーブルに対してロックするような長時間トランザクションを実行する必要がないようにしています。

- A message bus routes messages to handlers メッセージバスは、メッセージをハンドラに転送する

- You can think of a message bus as a dict that maps from events to their consumers. It doesn’t “know” anything about the meaning of events; it’s just a piece of dumb infrastructure for getting messages around the system. メッセージバスは、イベントからその消費者にマップするディクテと考えることができます。 メッセージバスはイベントの意味について何も「知らない」のです。それは、システム上でメッセージをやり取りするためのダムなインフラの一部に過ぎません。

- Option 1: Service layer raises events and passes them to message bus オプション1：サービス層がイベントを発生させ、メッセージバスに渡す。

- The simplest way to start using events in your system is to raise them from handlers by calling `bus.handle(some_new_event)` after you commit your unit of work. システムでイベントを使い始める最も簡単な方法は、作業単位をコミットした後に `bus.handle(some_new_event)` を呼び出して、ハンドラからイベントを発生させることです。

- Option 2: Domain model raises events, service layer passes them to message bus オプション2：ドメインモデルがイベントを発生させ、サービス層がそれをメッセージバスに渡す。

- The logic about when to raise an event really should live with the model, so we can improve our system’s design and testability by raising events from the domain model. It’s easy for our handlers to collect events off the model objects after `commit` and pass them to the bus. いつイベントを発生させるかについてのロジックは、本当にモデルとともにあるべきです。したがって、ドメインモデルからイベントを発生させることによって、システムの設計とテスト容易性を改善することができます。 ハンドラは `commit` の後にモデルオブジェクトからイベントを収集し、バスに渡すのは簡単です。

- Option 3: UoW collects events from aggregates and passes them to message bus オプション3：UoWはアグリゲートからイベントを収集し、メッセージバスに渡す

- Adding `bus.handle(aggregate.events)` to every handler is annoying, so we can tidy up by making our unit of work responsible for raising events that were raised by loaded objects. This is the most complex design and might rely on ORM magic, but it’s clean and easy to use once it’s set up. すべてのハンドラに `bus.handle(aggregate.events)` を追加するのは面倒なので、ロードされたオブジェクトによって発生したイベントの発生を担当する作業単位を作ることで片付けられます。 これは最も複雑な設計で、ORMマジックに依存するかもしれませんが、一度セットアップすればクリーンで使いやすいものです。

In Chapter 9, we’ll look at this idea in more detail as we build a more complex workflow with our new message bus.
第9章では、新しいメッセージバスを使ってより複雑なワークフローを構築しながら、このアイデアをより詳細に見ていきます。

1. This principle is the S in [SOLID](https://oreil.ly/AIdSD). この原理は、[SOLID](https:

2. Our tech reviewer Ed Jung likes to say that the move from imperative to event-based flow control changes what used to be orchestration into choreography. 技術評論家のEd Jungは、命令型からイベントベースのフロー制御への移行により、これまでオーケストレーションだったものが、コレオグラフィーに変わったと言うのが好きです。
