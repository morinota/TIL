# 1. Chapter 8. Events and the Message Bus 第8章 イベントとメッセージバス

So far we’ve spent a lot of time and energy on a simple problem that we could easily have solved with Django.
これまで私たちは、Django で簡単に解決できた単純な問題に、多くの時間とエネルギーを費やしてきた.
You might be asking if the increased testability and expressiveness are really worth all the effort.
テスト容易性と表現力の向上が、本当にすべての努力に見合うものなのかどうか、 疑問に思っているかもしれない.

In practice, though, we find that it’s not the obvious features that make a mess of our codebases: it’s the goop around the edge.
しかし、実際には、コードベースを混乱させるのは、明らかな機能ではなく、その周辺にあるゴミなのである.
It’s reporting, and permissions, and workflows that touch a zillion objects.
レポート、パーミッション、ワークフローなど、多くのオブジェクトに触れているのである.

Our example will be a typical notification requirement: when we can’t allocate an order because we’re out of stock, we should alert the buying team.
この例では、典型的な通知要件として、**在庫切れで注文を割り当てられない場合、購買チームに警告する必要がある**.
They’ll go and fix the problem by buying more stock, and all will be well.
購買チームは在庫を買い足して問題を解決し、すべてがうまくいくだろう.

For a first version, our product owner says we can just send the alert by email.
最初のバージョンでは、製品オーナーは、電子メールでアラートを送信すればよいと言う.

Let’s see how our architecture holds up when we need to plug in some of the mundane stuff that makes up so much of our systems.
では、私たちのシステムの多くを占める、ありふれたものを接続したときに、このアーキテクチャがどのように耐えられるか見てみよう.

We’ll start by doing the simplest, most expeditious thing, and talk about why it’s exactly this kind of decision that leads us to the Big Ball of Mud.
まずは、最もシンプルで手軽な方法から始めて、なぜ、このような判断が「泥の大箱」につながってしまうのか、その理由をお話しする.

Then we’ll show how to use the Domain Events pattern to separate side effects from our use cases, and how to use a simple Message Bus pattern for triggering behavior based on those events.
次に、**Domain Events pattern** を使ってユースケースから副作用を分離する方法と、これらの Event に基づいて動作をトリガーするためのシンプルな **Message Bus pattern** を使う方法を紹介する.
We’ll show a few options for creating those events and how to pass them to the message bus, and finally we’ll show how the Unit of Work pattern can be modified to connect the two together elegantly, as previewed in Figure 8-1.
これらの Event を作成するためのいくつかのオプションと、それらを Message Bus に渡す方法を紹介し、最後に図8-1でプレビューしたように、Unit of Work pattern を修正して、この2つをエレガントに接続する方法を紹介する.

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

## 1.1. Avoiding Making a Mess ♪混乱を避けるために

So.
だから
Email alerts when we run out of stock.
在庫が無くなった時のメール通知.
When we have new requirements like ones that really have nothing to do with the core domain, it’s all too easy to start dumping these things into our web controllers.
Core Domainとは全く関係ないような 新しい要件があると Web Controllersにこれらのものを 投入し始めるのはあまりにも簡単である.

### 1.1.1. First, Let’s Avoid Making a Mess of Our Web Controllers まず、ウェブコントローラーを混乱させないようにしよう

As a one-off hack, this might be OK:
一回限りのハックとしては、これでOKかもしれない.

Just whack it in the endpoint—what could go wrong? (src/allocation/entrypoints/flask_app.py)
エンドポイントに叩き込むだけ-何が問題なのか？

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
        ) # メール送信機能をhttpレイヤーに追加してみたが...
        return jsonify({'message': str(e)}), 400

    return jsonify({'batchref': batchref}), 201
```

…but it’s easy to see how we can quickly end up in a mess by patching things up like this.
...しかし、このようにパッチを適用することで、すぐに混乱に陥ることは容易に想像できる.
Sending email isn’t the job of our HTTP layer, and we’d like to be able to unit test this new feature.
**メールの送信はHTTPレイヤーの仕事ではないし、この新しい機能をユニットテストできるようにしたい**のである.

### 1.1.2. And Let’s Not Make a Mess of Our Model Either そして、私たちのモデルも台無しにしないようにしよう.

Assuming we don’t want to put this code into our web controllers, because we want them to be as thin as possible, we may look at putting it right at the source, in the model:
**Web Controller(=HTTP Layer?)はできるだけ薄くしたい**ので、このコードをWeb Controller に入れたくないと仮定すると、このコードをソースであるModelに直接入れる作戦になるかもしれない.

Email-sending code in our model isn’t lovely either (src/allocation/domain/model.py)

```python
    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
            )
            #...
        except StopIteration:
            email.send_mail('stock@made.com', f'Out of stock for {line.sku}') # domain service にsend_mailを追加してみる方法もあんまり...
            raise OutOfStock(f'Out of stock for sku {line.sku}')
```

But that’s even worse!
しかし、それはさらに悪いことだ.
We don’t want our model to have any dependencies on infrastructure concerns like `email.send_mail`.
**私たちのモデルには、`email.send_mail`のようなインフラストラクチャへの依存性を持たせたくない**. (Domain Modelはどれにも依存しないようにしたいんだった...!)

This email-sending thing is unwelcome goop messing up the nice clean flow of our system.
このメール送信の件は、私たちのシステムのきれいな流れを台無しにする歓迎されないgoop(?)である.
What we’d like is to keep our domain model focused on the rule “You can’t allocate more stuff than is actually available.”
私たちが望むのは、**Domain Model を "実際に利用できる以上のものを割り当ててはいけない "というルールに集中させ続けること**である.

The domain model’s job is to know that we’re out of stock, but the responsibility of sending an alert belongs elsewhere.
Domain Modelの仕事は在庫がないことを知ることだが、**アラートを送るresponsibilityは他にある**.
We should be able to turn this feature on or off, or to switch to SMS notifications instead, without needing to change the rules of our domain model.
**Domain Model のルールを変更することなく、この機能をオンにしたりオフにしたり、代わりにSMS通知に切り替えたりすることができるは**ずである...!! (機能追加や変更のしやすさ...!)

### 1.1.3. Or the Service Layer!

The requirement “Try to allocate some stock, and send an email if it fails” is an example of workflow orchestration: it’s a set of steps that the system has to follow to achieve a goal.
"在庫の割り当てを試み、失敗したらメールを送る"という要件は、Workflow Orchestration の一例である：これは、システムが目標を達成するために従わなければならない一連のステップだ.

We’ve written a service layer to manage orchestration for us, but even here the feature feels out of place:
私たちは、Orchestration を管理するための Service layer を書いたが、ここでもこの機能は場違いな感じがする...

And in the service layer, it’s out of place (src/allocation/service_layer/services.py)

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
            email.send_mail('stock@made.com', f'Out of stock for {line.sku}') # Service Layer にsend_mailを追加してみるのも, うーん...
            raise
```

Catching an exception and reraising it?
例外をキャッチして再レイズ？
It could be worse, but it’s definitely making us unhappy.
もっとひどいかもしれませんが、間違いなく私たちを不幸にしている.
Why is it so hard to find a suitable home for this code?
**なぜこのコードに適した家を見つけるのがこんなに難しいのだろうか？**

## 1.2. Single Responsibility Principle 単一責任原則

Really, this is a violation of the single responsibility principle (SRP).1 Our use case is allocation.
本当に、これは**Single Responsibility Principle(SRP, 単一責任原則?)**に違反している. 私たちのユースケースはallocationである.
Our endpoint, service function, and domain methods are all called `allocate`, not `allocate_and_send_mail_if_out_of_stock`.
私たちのエンドポイント、サービス関数、ドメインのメソッドはすべて `allocate` と呼ばれ、`allocate_and_send_mail_if_out_of_stock` と呼ばれることはないのである.

- TIP ヒント
- Rule of thumb: if you can’t describe what your function does without using words like “then” or “and,” you might be violating the SRP. **経験則：もし、"then"や"and"といった言葉を使わずに関数の動作を説明できない場合、SRPに違反している可能性がある**.

One formulation of the SRP is that each class should have only a single reason to change.
Single Responsibility Principleの一つの定式化は、**各クラスが変更する理由はただ一つであるべきだ**ということである.
When we switch from email to SMS, we shouldn’t have to update our `allocate()` function, because that’s clearly a separate responsibility.
電子メールから SMS に切り替えるとき、`allocate()` 関数を更新する必要はない. それは明らかに別のresponsibilityだから.

To solve the problem, we’re going to split the orchestration into separate steps so that the different concerns don’t get tangled up.2 The domain model’s job is to know that we’re out of stock, but the responsibility of sending an alert belongs elsewhere.
この問題を解決するために、Orchestrationを別々のステップに分割し、異なる懸念が絡まないようにする.2
Domain Model の仕事は、在庫切れを知ることですが、アラートを送る責任は別のところに属する.
We should be able to turn this feature on or off, or to switch to SMS notifications instead, without needing to change the rules of our domain model.
(**...なので!**)この機能をオンにしたりオフにしたり、代わりにSMS通知に切り替えることは、Domain Modelのルールを変更する必要なくできるはず.

We’d also like to keep the service layer free of implementation details.
また、Service Layer は実装(=Domain Model?)の詳細から解放された状態に保ちたいと考えている.
We want to apply the dependency inversion principle to notifications so that our service layer depends on an abstraction, in the same way as we avoid depending on the database by using a unit of work.
私たちは **Depencency Inversion Principle** を notification に適用し、Service Layer が abstractionされたもの(何の?)に依存するようにしたいと思う.

## 1.3. All Aboard the Message Bus! ♪みんなでメッセージバスに乗ろう！

The patterns we’re going to introduce here are Domain Events and the Message Bus.
今回紹介するのは、**Domain Event** と **Message Bus** のパターン.
We can implement them in a few ways, so we’ll show a couple before settling on the one we like most.
これらのパターンはいくつかの方法で実装することができるので、いくつか紹介した後、最も気に入ったものに決定する.

### 1.3.1. The Model Records Events モデルにはイベントが記録される

First, rather than being concerned about emails, our model will be in charge of recording events—facts about things that have happened.
まず、このモデルでは、メールではなく、**Event（起こったこと）**を記録することに専念する.
We’ll use a message bus to respond to events and invoke a new operation.
Message bus を使って、Eventに応答し、新しいオペレーションを呼び出すことにする.

### 1.3.2. Events Are Simple Dataclasses イベントは単純なデータクラス

An event is a kind of value object.
**EventはValue Objectの一種**である.
Events don’t have any behavior, because they’re pure data structures.
**Eventは純粋なデータ構造であるため、動作を持たない**.
We always name events in the language of the domain, and we think of them as part of our domain model.
**Event は常に Domain Language で命名され、Domain Model の一部とみなされる**.

We could store them in model.py, but we may as well keep them in their own file (this might be a good time to consider refactoring out a directory called domain so that we have domain/model.py and domain/events.py):
`model.py`に格納することもできるが、それ自身のファイルに格納する方が良いだろう.（これは、`domain`というディレクトリをリファクタリングして、`domain/model.py`と`domain/events.py`を持つように考える良い機会かもしれない）.

Event classes (src/domain/events.py)

```python
from dataclasses import dataclass

class Event:  # 1. 各Eventの親クラス(Abstractionとは部分的に役割が異なる?)
    pass

@dataclass
class OutOfStock(Event):  # 2.
    sku: str

```

1. Once we have a number of events, we’ll find it useful to have a parent class that can store common attributes. It’s also useful for type hints in our message bus, as you’ll see shortly. **Eventが多数になると、共通の属性を保存できる親クラスがあると便利**だと思う. また、まもなく見るように、**Message Busのタイプヒントにも便利**である.

2. `dataclasses` are great for domain events too. dataclassses はドメインイベントにも最適.

### 1.3.3. The Model Raises Events モデルがイベントを発生させる

When our domain model records a fact that happened, we say it raises an event.
**Domain Model が起こった事実を記録することを、"Eventを発生させる"**と言う.

Here’s what it will look like from the outside; if we ask `Product` to allocate but it can’t, it should raise an event:
外から見るとこんな感じ. もし `Product` にallocateを要求してallocateができなかったら、 Event を発生させる必要がある.

Test our aggregate to raise events (tests/unit/test_product.py)

```python
def test_records_out_of_stock_event_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    product = Product(sku="SMALL-FORK", batches=[batch])
    product.allocate(OrderLine('order1', 'SMALL-FORK', 10))

    allocation = product.allocate(OrderLine('order2', 'SMALL-FORK', 1))
    assert product.events[-1] == events.OutOfStock(sku="SMALL-FORK")  1
    assert allocation is None
```

1. Our aggregate will expose a new attribute called `.events` that will contain a list of facts about what has happened, in the form of `Event` objects. 私たちのAggregateは `.events` という新しい属性を公開する. この属性には、起こったことに関する事実のリストが `Event` オブジェクトの形で格納される.

Here’s what the model looks like on the inside:
モデルの内部はこんな感じ.

The model raises a domain event (src

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

1. Here’s our new .events attribute in use. 新しい.events属性が使用されている様子.

2. Rather than invoking some email-sending code directly, we record those events at the place they occur, using only the language of the domain. allocateできなかった際に、**メール送信のコードを直接呼び出すのではなく、それらのイベントが発生した場所で、ドメインの言語のみを使用して記録する**.

3. We’re also going to stop raising an exception for the out-of-stock case. The event will do the job the exception was doing. また、在庫切れの場合にExceptionを発生させることもやめようと思う. **Exceptionがやっていた仕事を、Eventがやってくれるようになる**.

- NOTE 注
- We’re actually addressing a code smell we had until now, which is that we were using exceptions for control flow. In general, if you’re implementing domain events, don’t raise exceptions to describe the same domain concept. As you’ll see later when we handle events in the Unit of Work pattern, it’s confusing to have to reason about events and exceptions together. 実は今まであったコードの臭い、つまり制御フローに例外を使っていたことに対処しているのだ. **一般に、Domain Eventを実装する場合、同じドメインコンセプトを表現するためにExceptionを発生させないようにしよう**. 後でUnit of Work patternで Event を処理するときにわかるが、**EventとException を一緒に理由づけしなければならなくなると混乱してしまう**.

### 1.3.4. The Message Bus Maps Events to Handlers メッセージバスはイベントをハンドラにマッピングする

A message bus basically says, “When I see this event, I should invoke the following handler function.”
**Message Bus は、基本的に "このEventを見たら、次のhandler関数を呼び出すように "というもの**だ.
In other words, it’s a simple publish-subscribe system.
言い換えれば、単純な publish-subscribe(?)システムである.
Handlers are subscribed to receive events, which we publish to the bus.
handlerはEventを受信するためにSubscribe(?)され、それを Bus に Publish する.(??)
It sounds harder than it is, and we usually implement it with a dict:
実際より難しそうに聞こえるので、**通常はdictで実装する**.

Simple message bus (src/allocation/service_layer/messagebus.py)

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
- Note that the message bus as implemented doesn’t give us concurrency because only one handler will run at a time. Our objective isn’t to support parallel threads but to separate tasks conceptually, and to keep each UoW as small as possible. This helps us to understand the codebase because the “recipe” for how to run each use case is written in a single place. See the following sidebar. Message Busの実装では、一度に一つのhandlerしか実行されないため、同時並行性(concurrency)が得られないことに注意せよ. 私たちの目的は、並列スレッドをサポートすることではなく、**タスクを概念的に分離し、各UoWをできるだけ小さくすること**である. これは、各ユースケースを実行する方法の「レシピ」が一箇所に書かれているため、コードベースを理解するのに役立つ. 次のサイドバーを参照してください.

- IS THIS LIKE CELERY? これはセロリのようなものだろうか?
- Celery is a popular tool in the Python world for deferring self-contained chunks of work to an asynchronous task queue. The message bus we’re presenting here is very different, so the short answer to the above question is no; our message bus has more in common with a Node.js app, a UI event loop, or an actor framework. Celeryは、Pythonの世界では、**自己完結した仕事の塊を非同期タスクキューに先送りするためのツール**として人気がある. このMessage Bus は、Node.jsのアプリやUIのイベントループ、あるいはアクターフレームワークと共通点が多い.(?)
- If you do have a requirement for moving work off the main thread, you can still use our event-based metaphors, but we suggest you use external events for that. There’s more discussion in Table 11-1, but essentially, if you implement a way of persisting events to a centralized store, you can subscribe other containers or other microservices to them. Then that same concept of using events to separate responsibilities across units of work within a single process/service can be extended across multiple processes—which may be different containers within the same service, or totally different microservices. メインスレッドから作業を移す要件がある場合、イベントベースのメタファーをまだ使用できますが、その場合は外部イベントを使用することをお勧めする.(?) 表11-1に詳しい説明がありますが、基本的には、Eventを集中型ストアに永続化する方法を実装すれば、他のコンテナや他のマイクロサービスをそれにサブスクライブすることができる. 次に、Eventを使用して、単一のプロセス内の作業単位間で責任を分離するという同じコンセプトがある.
- If you follow us in this approach, your API for distributing tasks is your event classes—or a JSON representation of them. This allows you a lot of flexibility in who you distribute tasks to; they need not necessarily be Python services. Celery’s API for distributing tasks is essentially “function name plus arguments,” which is more restrictive, and Python-only. このアプローチに従えば、タスクを配布するためのAPIはEventクラスか、そのJSON表現になる. これにより、タスクを配布する相手がPythonのサービスである必要はなく、非常に柔軟に対応することができる. Celeryのタスク配信APIは、基本的に「関数名＋引数」であり、より制約が多く、Python専用となる.

## 1.4. Option 1: The Service Layer Takes Events from the Model and Puts Them on the Message Bus Option 1: サービス層はモデルからイベントを受け取り、メッセージバスに載せる

Our domain model raises events, and our message bus will call the right handlers whenever an event happens.
**Domain Model は Event を発生させ、Message Bus は Event が発生するたびに適切な handler を呼び出す**.
Now all we need is to connect the two.
あとは、この2つをつなげるだけ.
We need something to catch events from the model and pass them to the message bus—the publishing step.
**modelからのEvent をキャッチし、Message Bus に渡すもの**が必要. これがPublishingのステップ.

The simplest way to do this is by adding some code into our service layer:
これを実現する最も簡単な方法は、Service Layer にいくつかのコードを追加すること.

The service layer with an explicit message bus (src/allocation/service_layer/services.py)

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
            messagebus.handle(product.events) # 2. message busがeventを受け取りhandlerを呼び出す.
```

1. We keep the try/finally from our ugly earlier implementation (we haven’t gotten rid of all exceptions yet, just OutOfStock). 以前の醜い実装から try/finally を残している（まだすべてのExceptionを取り除いたわけではない、OutOfStock だけである）.

2. But now, instead of depending directly on an email infrastructure, the service layer is just in charge of passing events from the model up to the message bus. しかし今度は、メールインフラに直接依存するのではなく、**Service layer は Model から Message Bus にイベントを渡すことだけ**を担当するようになった.

That already avoids some of the ugliness that we had in our naive implementation, and we have several systems that work like this one, in which the service layer explicitly collects events from aggregates and passes them to the message bus.
このように、**Service Layer が明示的に Aggregate からイベントを収集し、Message Bus に渡すような仕組みのシステム**もいくつかある.

## 1.5. Option 2: The Service Layer Raises Its Own Events Option 2: サービス層は独自のイベントを発生させる

Another variant on this that we’ve used is to have the service layer in charge of creating and raising events directly, rather than having them raised by the domain model:
また、Domain Model からEventを発生させるのではなく、**Service Layer が直接 Event の作成と発生を担当する**のも、このバリエーション.

Service layer calls messagebus.handle directly (src/allocation/service_layer/services.py)

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

1. As before, we commit even if we fail to allocate because the code is simpler this way and it’s easier to reason about: we always commit unless something goes wrong. Committing when we haven’t changed anything is safe and keeps the code uncluttered. この方がコードがシンプルになり、理屈もつけやすいから. 何か問題が起きない限り、常にコミットする. 何も変更していないときにコミットすることは、安全であり、コードをすっきりさせることができる.(??)

Again, we have applications in production that implement the pattern in this way.
繰り返しになる、このパターンを実装したアプリケーションは実稼働している.
What works for you will depend on the particular trade-offs you face, but we’d like to show you what we think is the most elegant solution, in which we put the unit of work in charge of collecting and raising events.
何がうまくいくかは、あなたが直面する特定のトレードオフに依存しますが、私たちが最もエレガントだと思う解決策をお見せしたいと思う. それは、**Unit of Work に Event の収集と発生を担当させる**というものである.

## 1.6. Option 3: The UoW Publishes Events to the Message Bus オプション 3: UoW がイベントをメッセージバスに発行する

The UoW already has a `try` UoWはすでに`try`を搭載している.

The UoW meets the message bus (src/allocation/service_layer/unit_of_work.py)

```python
class AbstractUnitOfWork(abc.ABC):
    ...

    def commit(self):
        self._commit() #1. subclassesから privateメソッドを呼ぶように修正.
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

1. We’ll change our commit method to require a private .\_commit() method from subclasses. サブクラスから private .\_commit() メソッドを要求するようにコミットメソッドを変更する.

2. After committing, we run through all the objects that our repository has seen and pass their events to the message bus. コミットした後、リポジトリが見たすべてのオブジェクト(=Aggregate?)を実行し、そのEventをメッセージバスに渡す.

3. That relies on the repository keeping track of aggregates that have been loaded using a new attribute, .seen, as you’ll see in the next listing. これは、次のリストで見るように、新しい属性である .seen を使って読み込まれた Aggregate をリポジトリが追跡していることに依存する.

- NOTE 注
- Are you wondering what happens if one of the handlers fails? We’ll discuss error handling in detail in Chapter 10. handlerのひとつが失敗したらどうなるのか、気になりませんか？ エラー処理については、第10章で詳しく説明する.

Repository tracks aggregates that pass through it (src/allocation/adapters/repository.py)
Repositoryは、それを通過したAggregateを追跡する(=記録を残す?)

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

1. For the UoW to be able to publish new events, it needs to be able to ask the repository for which `Product` objects have been used during this session. We use a `set` called `.seen` to store them. That means our implementations need to call `super().__init__()`. UoW が新しいEventを発行できるようにするには、このセッションでどの `Product` オブジェクトが使用されたかをRepositoryに問い合わせることができるようにする必要がある. 私たちは、それらを保存するために `.seen` という `set` を使用する. つまり、私たちの実装では `super().__init__()` を呼び出す必要がある.

2. The parent `add()` method adds things to `.seen`, and now requires subclasses to implement `._add()`. 親クラスの `add()` メソッドは `.seen` に物を追加しますが、サブクラスには `._add()` の実装が必要になった. (=これはサブクラス毎にaddの為の処理方法が異なる為??)

3. Similarly, `.get()` delegates to a `._get()` function, to be implemented by subclasses, in order to capture objects seen. 同様に、`.get()` は、見たオブジェクトを捕捉するために、サブクラスが実装する `._get()` 関数に委譲する. (=これも同様に、サブクラス毎にgetの為の処理方法が異なる為??)

- NOTE 注
- The use of `._underscorey()` methods and subclassing is definitely not the only way you could implement these patterns. Have a go at the Exercise for the Reader in this chapter and experiment with some alternatives. **`._underscorey()` メソッド(i.e. privateメソッド)の使用とサブクラス化は、これらのパターンを実装するための唯一の方法**であることは間違いない. この章の「読者のための練習問題」を読んで、いくつかの選択肢を試してみてください.

After the UoW and repository collaborate in this way to automatically keep track of live objects and process their events, the service layer can be totally free of event-handling concerns:
UoWとRepositoryがこのように連携して、生きているオブジェクト(=Aggregate?)を自動的に追跡し、そのEventを処理した後、Service LayerはEvent処理に関する懸念から完全に解放されることになる.

Service layer is clean again (src/allocation/service_layer/services.py)

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
また、Service Layer のフェイクを変更し、適切な場所で `super()` を呼び出すようにしたり、アンダースコアのメソッドを実装することを忘れないようにしなければなりませんが、変更は最小限にとどめられる.

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

- Are you finding all those `._add()` and `._commit()` methods “super-gross,” in the words of our beloved tech reviewer Hynek? Does it “make you want to beat Harry around the head with a plushie snake”? Hey, our code listings are only meant to be examples, not the perfect solution! Why not go see if you can do better? 私たちの愛する技術評論家ハイネックの言葉を借りれば、`._add()` と `._commit()` のすべてのメソッドが「超キモい」と感じていませんか？ ヘビのぬいぐるみでハリーの頭をぶん殴りたくなる」のでしょうか？ **私たちのコードリストはあくまでも例であって、完璧な解決策ではありません**よ. もっといい方法がないか、試してみませんか？

One composition over inheritance way to go would be to implement a wrapper class:
継承を超えたコンポジションの1つの方法として、**Wrappter classを実装すること(?)**が考えられます。

A wrapper adds functionality and then delegates (src/adapters/repository.py)
wrapperは機能を追加した後、 **delegate(=委任,委託, 移譲 = オブジェクトの振る舞いを別のオブジェクトに肩代わりしてもらう事)**する.

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

1. By wrapping the repository, we can call the actual `.add()` and `.get()` methods, avoiding weird underscorey methods. RepositoryをWrapすることで、実際の `.add()` と `.get()` メソッドを呼び出すことができ、変なアンダースコアを使ったメソッドを回避することができる.(??) (`TrackingRepository`がWrapper class??)

- See if you can apply a similar pattern to our UoW class in order to get rid of those Java-y `_commit()` methods too. You can find the code on GitHub. 同じようなパターンをUoWクラスに適用して、Java的な `_commit()` メソッドを取り除くことができるかどうか見てみよう. このコードはGitHubで見ることができる.

- Switching all the ABCs to `typing.Protocol` is a good way to force yourself to avoid using inheritance. Let us know if you come up with something nice! ABCを全て`typing.Protocol`に切り替えることで、無理やり**継承(inheritance)**を使わないようにすることができる. 何かいい方法が思いついたら、ぜひ教えてください.

You might be starting to worry that maintaining these fakes is going to be a maintenance burden.
このようなフェイクを維持するのはメンテナンスの負担になるのではと心配になってきたのではないだろうか.
There’s no doubt that it is work, but in our experience it’s not a lot of work.
作業であることは間違いありませんが、私たちの経験では、それほど大変な作業ではない.
Once your project is up and running, the interface for your repository and UoW abstractions really don’t change much.
一度プロジェクトが立ち上がれば、RepositoryとUoWの抽象化のためのインターフェイスは本当にあまり変わらない.
And if you’re using ABCs, they’ll help remind you when things get out of sync.
また、ABCを使用している場合は、同期がとれなくなったときに、ABCが教えてくれる.

## 1.7. Wrap-Up まとめ

Domain events give us a way to handle workflows in our system.
Domain Event は、システムでワークフローを処理するための方法.
We often find, listening to our domain experts, that they express requirements in a causal or temporal way
専門家(Domain Expert)の話を聞いていると、要件が因果関係や時間的な関係で表現されていることがよくある.
—for example, “When we try to allocate stock but there’s none available, then we should send an email to the buying team.”
例えば、「在庫を割り当てようとしたときに、在庫がない場合は、購買チームにメールを送る」というようにだ.

The magic words “When X, then Y” often tell us about an event that we can make concrete in our system.
**"When X, then Y"という魔法の言葉**は、しばしば、私たちのシステムで具体化できるEventについて教えてくれる.
Treating events as first-class things in our model helps us make our code more testable and observable, and it helps isolate concerns.
**Eventを第一級のものとしてモデル化することは、コードをよりテストしやすく、観察しやすくし、懸念を分離するのに役立つ**.

And Table 8-1 shows the trade-offs as we see them.
そして、表8-1は、私たちが考えるトレードオフを示したものである.

Table 8-1.
表8-1.
Domain events: the trade-offs
ドメインイベント：トレードオフ

- Pros 長所

  - A message bus gives us a nice way to separate responsibilities when we have to take multiple actions in response to a request. Message Bus は、リクエストに応答して複数の(種類の)アクションを取らなければならないときに、Responsibilityを分離するための良い方法を提供する.
  - Event handlers are nicely decoupled from the “core” application logic, making it easy to change their implementation later. Event Handler は、「コア」アプリケーションロジックからうまく切り離されているため、後から実装を変更することも容易.
  - Domain events are a great way to model the real world, and we can use them as part of our business language when modeling with stakeholders. Domein Event は実世界をモデル化する優れた方法であり、ステークホルダーとモデル化する際に、business language(=domain language?)の一部として使用することができる.

- Cons 短所

  - The message bus is an additional thing to wrap your head around; the implementation in which the unit of work raises events for us is neat but also magic. It’s not obvious when we call `commit` that we’re also going to go and send email to people. Message Bus はさらに頭を悩ませるもの. Unit of Work が私たちのためにEventを発生させるという実装はきちんとしたものだが、魔法でもある. `commit`を呼び出すときに、人々にメールを送信することは明らかではない.
  - What’s more, that hidden event-handling code executes synchronously, meaning your service-layer function doesn’t finish until all the handlers for any events are finished. That could cause unexpected performance problems in your web endpoints (adding asynchronous processing is possible but makes things even more confusing). さらに、その隠されたEvent処理コードは同期的に実行される. つまり、**Service Layer の関数は、すべてのEvent のhandlerが終了するまで終了しない**. これは、ウェブエンドポイントに予期せぬパフォーマンスの問題を引き起こす可能性がある（非同期処理を追加することは可能ですが、事態をさらに混乱させる）.
  - More generally, event-driven workflows can be confusing because after things are split across a chain of multiple handlers, there is no single place in the system where you can understand how a request will be fulfilled. より一般的には、Event駆動型のワークフローは、複数のhandlerの連鎖によって物事が分割された後、リクエストがどのように実現されるかを理解できる単一の場所がシステム内に存在しないため(??)、混乱することがある.
  - You also open yourself up to the possibility of circular dependencies between your event handlers, and infinite loops. また、Event Handler 間の循環的な依存関係や、無限ループの可能性も出てくる.(これはわかる...!)

Events are useful for more than just sending email, though.
しかし、Eventは電子メールを送る以外にも便利.
In Chapter 7 we spent a lot of time convincing you that you should define aggregates, or boundaries where we guarantee consistency.
第7章では、**Aggregate**、つまり**一貫性を保証する境界を定義する必要がある**ことを納得させるために多くの時間を費やした.
People often ask, “What should I do if I need to change multiple aggregates as part of a request?”
リクエストの一部として複数のAggregateを変更する必要がある場合、どうすればよいのでしょうか?" という質問がよくある.
Now we have the tools we need to answer that question.
今、私たちはその質問に答えるために必要なツールを持っている.

If we have two things that can be transactionally isolated (e.g., an order and a product), then we can make them eventually consistent by using events.
トランザクション的に分離できる2つのもの(例えば、order と product)があれば、Eventを使うことで、最終的に整合性を持たせることができる.(??次の文を読んだらなんとなくわかる...!)
When an order is canceled, we should find the products that were allocated to it and remove the allocations.
**注文(=order)がキャンセルされたら、それに割り当てられていた商品(=Product)を探し出し、割り当てを削除する必要がある.**

### 1.7.1. DOMAIN EVENTS AND THE MESSAGE BUS RECAP ドメインイベントとメッセージバスの再録

- Events can help with the single responsibility principle **EventはSingle Responsibility Principleに役立つ**.
  - Code gets tangled up when we mix multiple concerns in one place. Events can help us to keep things tidy by separating primary use cases from secondary ones. We also use events for communicating between aggregates so that we don’t need to run long-running transactions that lock against multiple tables. 複数の関心事が混在していると、コードがこんがらがってしまう. **Eventは、一次的なユースケースと二次的なユースケースを分離することで、物事を整理整頓するのに役立っている.** また、Aggregate 間の通信にもEventを利用し、複数のテーブルに対してロックするような長時間トランザクションを実行する必要がないようにしている.
- A message bus routes messages to handlers Message Busは、メッセージ(=Eventが発生した旨の?)をhandlerに転送する.
  - You can think of a message bus as a dict that maps from events to their consumers. It doesn’t “know” anything about the meaning of events; it’s just a piece of dumb infrastructure for getting messages around the system. Message Bus は、**Event からその消費者(=handler)にマップするdictと考えることができる**. **Message Bus自体はEventの意味について何も知らない**. それは、システム上でメッセージをやり取りするためのダムなインフラの一部に過ぎない.
- Option 1: Service layer raises events and passes them to message bus オプション1：**Service LayerがEventを発生させ、message Busに渡す**.
  - The simplest way to start using events in your system is to raise them from handlers by calling `bus.handle(some_new_event)` after you commit your unit of work. システムでEventを使い始める最も簡単な方法は、作業単位をcommitした後に `bus.handle(some_new_event)` を呼び出して、handlerからイベントを発生させること.
- Option 2: Domain model raises events, service layer passes them to message bus オプション2：**Domain Modelがイベントを発生させ、Service Layerがそれをメッセージバスに渡す.**
  - The logic about when to raise an event really should live with the model, so we can improve our system’s design and testability by raising events from the domain model. It’s easy for our handlers to collect events off the model objects after `commit` and pass them to the bus. いつイベントを発生させるかについてのロジックは、本当にモデルとともにあるべき. したがって、ドメインモデルからイベントを発生させることによって、システムの設計とテスト容易性を改善することができる. ハンドラは `commit` の後にモデルオブジェクトからイベントを収集し、バスに渡すのは簡単.
- Option 3: UoW collects events from aggregates and passes them to message bus オプション3：UoWはAggregateからイベントを収集し、メッセージバスに渡す.
  - Adding `bus.handle(aggregate.events)` to every handler is annoying, so we can tidy up by making our unit of work responsible for raising events that were raised by loaded objects. This is the most complex design and might rely on ORM magic, but it’s clean and easy to use once it’s set up. すべてのハンドラに `bus.handle(aggregate.events)` を追加するのは面倒なので、ロードされたオブジェクトによって発生したイベントの発生を担当するUnit of Workを作ることで片付けられる. これは最も複雑な設計で、ORMマジックに依存するかもしれませんが、一度セットアップすればクリーンで使いやすいもの.

In Chapter 9, we’ll look at this idea in more detail as we build a more complex workflow with our new message bus.
第9章では、新しいMessage Busを使ってより複雑なワークフローを構築しながら、このアイデアをより詳細に見ていく.

1. This principle is the S in [SOLID](https://oreil.ly/AIdSD). この原理は、[SOLID](https:
2. Our tech reviewer Ed Jung likes to say that the move from imperative to event-based flow control changes what used to be orchestration into choreography. 技術評論家のEd Jungは、命令型からイベントベースのフロー制御への移行により、**これまでorchestrationだったものが、choreographyに変わった**と言うのが好き.(??)

- [orchestration と choreography: マイクロサービスアーキテクチャの話](https://ts0818.hatenablog.com/entry/2019/10/06/152518)
