# 1. Chapter 9. Going to Town on the Message Bus 第9章 メッセージバスで街に繰り出す

In this chapter, we’ll start to make events more fundamental to the internal structure of our application.
この章では、Eventをアプリケーションの内部構造にとってより基本的なものにすることに着手する.
We’ll move from the current state in Figure 9-1, where events are an optional side effect…
図 9-1 のように、Eventがオプションの副次的なものである状態から、...

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0901.png)

…to the situation in Figure 9-2, where everything goes via the message bus, and our app has been transformed fundamentally into a message processor.
...図9-2のような状況になると、すべてがMessage busを経由するようになり、**アプリは根本的にmessage processer(=入力メッセージを受け取って解析し、適切な処理を行い、必要な出力メッセージを生成するプログラムの事...??)に変化している**.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0902.png)

- TIP ヒント
  The code for this chapter is in the chapter_09_all_messagebus branch on GitHub:
  この章のコードは、GitHub の chapter_09_all_messagebus ブランチにある.

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_09_all_messagebus
# or to code along, checkout the previous chapter:
git checkout chapter_08_events_and_message_bus
```

## 1.1. A New Requirement Leads Us to a New Architecture 新しい要求が新しいアーキテクチャを導く

Rich Hickey talks about situated software, meaning software that runs for extended periods of time, managing a real-world process.
リッチ・ヒッキーは、**現実世界のプロセスを管理し長時間稼働するソフトウェア**である"**situated (状況的) software**" について語る.
Examples include warehouse-management systems, logistics schedulers, and payroll systems.
例えば、倉庫管理システム、物流スケジューラ、給与計算システムなどである.

This software is tricky to write because unexpected things happen all the time in the real world of physical objects and unreliable humans.
このソフトウェアが厄介なのは、物理的なモノと信頼できない人間という現実の世界では、常に予期せぬことが起こるからだ.
For example:
例えば

- During a stock-take, we discover that three `SPRINGY-MATTRESSes` have been water damaged by a leaky roof. 棚卸の際、3台の「SPRINGY-MATTRESS」が屋根の雨漏りにより水濡れしていることが判明した.
- A consignment of `RELIABLE-FORKs` is missing the required documentation and is held in customs for several weeks. Three `RELIABLE-FORKs` subsequently fail safety testing and are destroyed. ある`RELIABLE-FORKs`の荷物が必要な書類を欠いており、数週間税関で留め置かれている. その後、3つの`RELIABLE-FORKs`が安全性テストに不合格となり、廃棄された.
- A global shortage of sequins means we’re unable to manufacture our next batch of `SPARKLY-BOOKCASE`. 世界的なスパンコールの不足により、次のロットの`SPARKLY-BOOKCASE`を製造することができなくなった.

In these types of situations, we learn about the need to change batch quantities when they’re already in the system.
このような場面では、**すでにシステム上にあるバッチ数量を変更する必要性**について学ぶ.
Perhaps someone made a mistake on the number in the manifest, or perhaps some sofas fell off a truck.
おそらく、誰かがマニフェストの番号を間違えたか、あるいはトラックからソファが落ちたのでしょう.
Following a conversation with the business,1 we model the situation as in Figure 9-3.
ビジネスとの会話に続いて、私たちは図9-3のように状況をモデル化します1。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0903.png)

An event we’ll call `BatchQuantityChanged` should lead us to change the quantity on the batch, yes, but also to apply a business rule: if the new quantity drops to less than the total already allocated, we need to deallocate those orders from that batch.
`BatchQuantityChanged` と呼ぶイベントによって、バッチの数量を変更することができますが、ビジネスルールを適用することもできる.
Then each one will require a new allocation, which we can capture as an event called `AllocationRequired`.
新しい数量がすでに割り当てられている合計よりも少ない場合、そのバッチからそれらの注文の割り当てを解除する必要がある. それから、それぞれが新しい割り当てを必要とし、それを `AllocationRequired` というイベントとして捕らえることができる.

Perhaps you’re already anticipating that our internal message bus and events can help implement this requirement.
おそらく、内部Message Bus と Event がこの要件を実装するのに役立つと既に予想されているだろう.
We could define a service called `change_batch_quantity` that knows how to adjust batch quantities and also how to deallocate any excess order lines, and then each deallocation can emit an `AllocationRequired` event that can be forwarded to the existing `allocate` service, in separate transactions.
バッチ数量を調整する方法と、余分な注文行の割り当てを解除する方法を知っている `change_batch_quantity` というサービスを定義して、割り当て解除ごとに `AllocationRequired` イベントを発行して、既存の `allocate` サービスに転送できるように、別々のトランザクションで設定することが可能です。
Once again, our message bus helps us to enforce the single responsibility principle, and it allows us to make choices about transactions and data integrity.
繰り返しになりますが、Message bus は**single responsibility principle(単一責任の原則)**を実施するのに役立ち、トランザクションとデータの整合性について選択することを可能にする.

### 1.1.1. Imagining an Architecture Change: Everything Will Be an Event Handler アーキテクチャの変化を想像してみる。 すべてがイベントハンドラになる

But before we jump in, think about where we’re headed.
しかし、飛び込む前に、どこに向かっているのかを考えてみましょう。
There are two kinds of flows through our system:
私たちのシステムには、2種類の流れがあります。

API calls that are handled by a service-layer function
サービスレイヤの機能で処理されるAPIコール

Internal events (which might be raised as a side effect of a service-layer function) and their handlers (which in turn call service-layer functions)
内部イベント（サービスレイヤー機能の副作用として発生する可能性がある）とそのハンドラ（そのハンドラがサービスレイヤー機能を呼び出す）。

Wouldn’t it be easier if everything was an event handler?
すべてがイベントハンドラであれば、もっと簡単ではないでしょうか？
If we rethink our API calls as capturing events, the service-layer functions can be event handlers too, and we no longer need to make a distinction between internal and external event handlers:
APIコールをイベントの捕捉と捉えれば、サービスレイヤーの関数もイベントハンドラになり、内部と外部のイベントハンドラを区別する必要はなくなる。

- `services.allocate()` could be the handler for an `AllocationRequired` event and could emit `Allocated` events as its output. `services.allocate()` は `AllocationRequired` イベントのハンドラで、その出力として `Allocated` イベントを発生させることができます。

- `services.add_batch()` could be the handler for a `BatchCreated` event.2 `services.add_batch()` は `BatchCreated` イベントのハンドラである可能性があります。

Our new requirement will fit the same pattern:
私たちの新しい要求も、同じパターンに当てはまるでしょう。

- An event called `BatchQuantityChanged` can invoke a handler called `change_batch_quantity()`. BatchQuantityChanged`というイベントは、`change_batch_quantity()` というハンドラを呼び出すことができます。

- And the new `AllocationRequired` events that it may raise can be passed on to `services.allocate()` too, so there is no conceptual difference between a brand-new allocation coming from the API and a reallocation that’s internally triggered by a deallocation. そして、新たに発生する可能性のある `AllocationRequired` イベントも `services.allocate()` に渡すことができます。したがって、API から来る新しい割り当てと、割り当て解除によって内部的に引き起こされる再割り当ての間に、概念的な違いはありません。

All sound like a bit much?
全部はちょっと無理かな？
Let’s work toward it all gradually.
少しずつ進めていきましょう。
We’ll follow the Preparatory Refactoring workflow, aka “Make the change easy; then make the easy change”:
私たちは、準備的リファクタリングのワークフロー、別名「変更を簡単にし、次に簡単な変更をする」ことに従います。

1. We refactor our service layer into event handlers. We can get used to the idea of events being the way we describe inputs to the system. In particular, the existing `services.allocate()` function will become the handler for an event called `AllocationRequired`. サービスレイヤーをイベントハンドラにリファクタリングする。 システムに対する入力を記述する方法がイベントであるという考え方に慣れることができます。 特に、既存の `services.allocate()` 関数は、 `AllocationRequired` というイベントのハンドラになります。

2. We build an end-to-end test that puts `BatchQuantityChanged` events into the system and looks for `Allocated` events coming out. BatchQuantityChanged` イベントをシステムに投入し、`Allocated` イベントが出てくるかどうかを調べるエンドツーエンドテストを構築します。

3. Our implementation will conceptually be very simple: a new handler for `BatchQuantityChanged` events, whose implementation will emit `AllocationRequired` events, which in turn will be handled by the exact same handler for allocations that the API uses. BatchQuantityChanged`イベント用の新しいハンドラで、その実装は`AllocationRequired` イベントを発行し、順番に API が使うのと全く同じ割り当て用のハンドラによって処理されます。

Along the way, we’ll make a small tweak to the message bus and UoW, moving the responsibility for putting new events on the message bus into the message bus itself.
その過程で、メッセージバスとUoWに小さな手を加え、メッセージバスに新しいイベントを置く責任をメッセージバス自体に移すことにします。

## 1.2. Refactoring Service Functions to Message Handlers サービスファンクションからメッセージハンドラへのリファクタリング

We start by defining the two events that capture our current API inputs—`AllocationRequired` and `BatchCreated`:
まず、現在の API 入力を取得するための 2 つのイベント、`AllocationRequired` と `BatchCreated` を定義します。

BatchCreated and AllocationRequired events (src
BatchCreated および AllocationRequired イベント（src

```python
@dataclass
class BatchCreated(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

...

@dataclass
class AllocationRequired(Event):
    orderid: str
    sku: str
    qty: int
```

Then we rename services.py to handlers.py; we add the existing message handler for `send_out_of_stock_notification`; and most importantly, we change all the handlers so that they have the same inputs, an event and a UoW:
そして、services.py を handlers.py にリネームします。既存の `send_out_of_stock_notification` のメッセージハンドラを追加します。最も重要なのは、すべてのハンドラが同じ入力、イベントと UoW を持つように変更することです。

Handlers and services are the same thing (src
ハンドラとサービスは同じものです（src

```python
def add_batch(
        event: events.BatchCreated, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku=event.sku)
        ...


def allocate(
        event: events.AllocationRequired, uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(event.orderid, event.sku, event.qty)
    ...


def send_out_of_stock_notification(
        event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork,
):
    email.send(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
```

The change might be clearer as a diff:
差分として変化が明確になるかもしれません。

Changing from services to handlers (src
サービスからハンドラへの変更（src

```python
 def add_batch(
-        ref: str, sku: str, qty: int, eta: Optional[date],
-        uow: unit_of_work.AbstractUnitOfWork
+        event: events.BatchCreated, uow: unit_of_work.AbstractUnitOfWork
 ):
     with uow:
-        product = uow.products.get(sku=sku)
+        product = uow.products.get(sku=event.sku)
     ...


 def allocate(
-        orderid: str, sku: str, qty: int,
-        uow: unit_of_work.AbstractUnitOfWork
+        event: events.AllocationRequired, uow: unit_of_work.AbstractUnitOfWork
 ) -> str:
-    line = OrderLine(orderid, sku, qty)
+    line = OrderLine(event.orderid, event.sku, event.qty)
     ...

+
+def send_out_of_stock_notification(
+        event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork,
+):
+    email.send(
     ...
```

Along the way, we’ve made our service-layer’s API more structured and more consistent.
その過程で、私たちはサービスレイヤーのAPIをより構造化し、より一貫性のあるものにしました。
It was a scattering of primitives, and now it uses well-defined objects (see the following sidebar).
以前はプリミティブが散在していましたが、今ではきちんと定義されたオブジェクトを使っています（次のサイドバーを参照）。

- FROM DOMAIN OBJECTS, VIA PRIMITIVE OBSESSION, TO EVENTS AS AN INTERFACE ドメインオブジェクトから、プリミティブオブセッションを経て、インターフェースとしてのイベントへ

- Some of you may remember “Fully Decoupling the Service-Layer Tests from the Domain”, in which we changed our service-layer API from being in terms of domain objects to primitives. And now we’re moving back, but to different objects? What gives? サービスレイヤーのテストをドメインから完全に切り離す "を覚えている人もいるだろう。その中で、私たちはサービスレイヤーのAPIをドメインオブジェクトからプリミティブに変更した。 そして今、私たちはまた別のオブジェクトに戻ろうとしている？ どうしたんだ？

- In OO circles, people talk about primitive obsession as an anti-pattern: avoid primitives in public APIs, and instead wrap them with custom value classes, they would say. In the Python world, a lot of people would be quite skeptical of that as a rule of thumb. When mindlessly applied, it’s certainly a recipe for unnecessary complexity. So that’s not what we’re doing per se. OOサークルでは、プリミティブへのこだわりはアンチパターンとして語られます。パブリックAPIではプリミティブを避け、代わりにカスタム値クラスでラップする、と。 Pythonの世界では、多くの人がその経験則に懐疑的でしょう。 無頓着に適用すると、確かに不必要に複雑化することになります。 ですから、私たちがやっていることは、それ自体ではありません。

- The move from domain objects to primitives bought us a nice bit of decoupling: our client code was no longer coupled directly to the domain, so the service layer could present an API that stays the same even if we decide to make changes to our model, and vice versa. ドメインオブジェクトからプリミティブへの移行は、素晴らしいデカップリングをもたらしました。クライアントコードはもはやドメインに直接結合されていないので、サービス層は、私たちがモデルを変更することにしても変わらないAPIを提示できますし、逆もまた然りです。

- So have we gone backward? Well, our core domain model objects are still free to vary, but instead we’ve coupled the external world to our event classes. They’re part of the domain too, but the hope is that they vary less often, so they’re a sensible artifact to couple on. では、後戻りしたのでしょうか？ さて、コア・ドメイン・モデルのオブジェクトはまだ自由に変化しますが、その代わりに、外部世界をイベント・クラスに結合しています。 イベントクラスもドメインの一部ですが、イベントクラスはあまり頻繁に変化しないので、カップリングするには理にかなった成果物であると期待されています。

- And what have we bought ourselves? Now, when invoking a use case in our application, we no longer need to remember a particular combination of primitives, but just a single event class that represents the input to our application. That’s conceptually quite nice. On top of that, as you’ll see in Appendix E, those event classes can be a nice place to do some input validation. そして、私たちは何を買ったのでしょうか？ これで、アプリケーションでユースケースを呼び出すときに、プリミティブの特定の組み合わせを覚える必要はなくなり、アプリケーションへの入力を表すイベントクラスを1つだけ覚えることができるようになりました。 これは概念的には非常に素晴らしいことです。 その上、付録Eで見るように、これらのイベントクラスは入力の検証を行うのに格好の場所となり得ます。

### 1.2.1. The Message Bus Now Collects Events from the UoW メッセージバスがUoWからイベントを収集するようになりました。

Our event handlers now need a UoW.
イベントハンドラには UoW が必要です。
In addition, as our message bus becomes more central to our application, it makes sense to put it explicitly in charge of collecting and processing new events.
さらに、メッセージバスがアプリケーションの中心になるにつれて、新しいイベントの収集と処理を明示的に担当させることは理にかなっています。
There was a bit of a circular dependency between the UoW and message bus until now, so this will make it one-way:
これまでUoWとメッセージバスの間には、ちょっとした循環型依存関係がありましたので、これで一方通行になります。

Handle takes a UoW and manages a queue (src
ハンドルはUoWを受け取り、キューを管理する（src

```python
def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):  1
    queue = [event]  2
    while queue:
        event = queue.pop(0)  3
        for handler in HANDLERS[type(event)]:  3
            handler(event, uow=uow)  4
            queue.extend(uow.collect_new_events())  5
```

1. The message bus now gets passed the UoW each time it starts up. メッセージバスが起動するたびにUoWに渡されるようになった。

2. When we begin handling our first event, we start a queue. 最初のイベントの処理を開始するとき、キューを開始します。

3. We pop events from the front of the queue and invoke their handlers (the HANDLERS dict hasn’t changed; it still maps event types to handler functions). イベントをキューの先頭からポップし、そのハンドラを呼び出します（HANDLERSディクショ ンは変更されていません；イベントの種類をハンドラ関数にマッピングしています）。

4. The message bus passes the UoW down to each handler. メッセージバスは、UoWを各ハンドラに受け渡す。

5. After each handler finishes, we collect any new events that have been generated and add them to the queue. 各ハンドラの終了後、新たに発生したイベントを収集し、キューに追加する。

In unit_of_work.py, `publish_events()` becomes a less active method, `collect_new_events()`:
unit_of_work.py では、`publish_events()` は、あまり活発でないメソッド `collect_new_events()` になりました。

UoW no longer puts events directly on the bus (src
UoWはイベントを直接バスに乗せなくなった（src

```python
-from . import messagebus  1
-


 class AbstractUnitOfWork(abc.ABC):
@@ -23,13 +21,11 @@ class AbstractUnitOfWork(abc.ABC):

     def commit(self):
         self._commit()
-        self.publish_events()  2

-    def publish_events(self):
+    def collect_new_events(self):
         for product in self.products.seen:
             while product.events:
-                event = product.events.pop(0)
-                messagebus.handle(event)
+                yield product.events.pop(0)  3
```

1. The `unit_of_work` module now no longer depends on `messagebus`. unit_of_work`モジュールは、もはや`messagebus` に依存しません。

2. We no longer `publish_events` automatically on commit. The message bus is keeping track of the event queue instead. コミット時に自動的に `publish_events` を発行しなくなりました。 代わりにメッセージバスがイベントキューを追跡しています。

3. And the UoW no longer actively puts events on the message bus; it just makes them available. また、UoWはもはや積極的にイベントをメッセージバスに載せることはなく、ただ利用できるようにするだけである。

### 1.2.2. Our Tests Are All Written in Terms of Events Too 私たちのテストもすべて事象で書かれている

Our tests now operate by creating events and putting them on the message bus, rather than invoking service-layer functions directly:
テストは、サービス層の関数を直接呼び出すのではなく、イベントを生成してメッセージバスに乗せることで動作するようになりました。

Handler tests use events (tests
ハンドラテストはイベントを使用する（テスト

```python
class TestAddBatch:

     def test_for_new_product(self):
         uow = FakeUnitOfWork()
-        services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
+        messagebus.handle(
+            events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow
+        )
         assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
         assert uow.committed

...

 class TestAllocate:

     def test_returns_allocation(self):
         uow = FakeUnitOfWork()
-        services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
-        result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
+        messagebus.handle(
+            events.BatchCreated("batch1", "COMPLICATED-LAMP", 100, None), uow
+        )
+        result = messagebus.handle(
+            events.AllocationRequired("o1", "COMPLICATED-LAMP", 10), uow
+        )
         assert result == "batch1"
```

### 1.2.3. A Temporary Ugly Hack: The Message Bus Has to Return Results メッセージバスが結果を返さなければならないという一時的な醜いハック

Our API and our service layer currently want to know the allocated batch reference when they invoke our `allocate()` handler.
API とサービス層は現在、`allocate()` ハンドラを呼び出したときに、割り当てられたバッチリファレンスを知りたがっています。
This means we need to put in a temporary hack on our message bus to let it return events:
これは、イベントを返すようにするために、メッセージバスを一時的にハックする必要があることを意味します。

Message bus returns results (src
メッセージバスが返す結果（src

```python
 def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):
+    results = []
     queue = [event]
     while queue:
         event = queue.pop(0)
         for handler in HANDLERS[type(event)]:
-            handler(event, uow=uow)
+            results.append(handler(event, uow=uow))
             queue.extend(uow.collect_new_events())
+    return results
```

It’s because we’re mixing the read and write responsibilities in our system.
それは、システムの中で読み取りと書き込みの責任を混同しているからです。
We’ll come back to fix this wart in Chapter 12.
第12章では、このイボイボを直すために戻ってくることにします。

### 1.2.4. Modifying Our API to Work with Events イベントと連動するようにAPIを変更する

Flask changing to message bus as a diff (src
Flaskがメッセージバスに変更されたことを差分として（src

```python
 @app.route("/allocate", methods=['POST'])
 def allocate_endpoint():
     try:
-        batchref = services.allocate(
-            request.json['orderid'],  1
-            request.json['sku'],
-            request.json['qty'],
-            unit_of_work.SqlAlchemyUnitOfWork(),
+        event = events.AllocationRequired(  2
+            request.json['orderid'], request.json['sku'], request.json['qty'],
         )
+        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())  3
+        batchref = results.pop(0)
     except InvalidSku as e:
```

1. Instead of calling the service layer with a bunch of primitives extracted from the request JSON… リクエストJSONから抽出したプリミティブの束でサービスレイヤーを呼び出すのではなく、...

2. We instantiate an event. イベントをインスタンス化する。

3. Then we pass it to the message bus. そして、メッセージバスに渡します。

And we should be back to a fully functional application, but one that’s now fully event-driven:
そして、完全に機能するアプリケーションに戻るはずですが、完全にイベントドリブンになったアプリケーションです。

- What used to be service-layer functions are now event handlers. これまでサービスレイヤーの機能であったものが、イベントハンドラになっている。

- That makes them the same as the functions we invoke for handling internal events raised by our domain model. つまり、ドメインモデルから発生する内部イベントを処理するために呼び出す関数と同じになります。

- We use events as our data structure for capturing inputs to the system, as well as for handing off of internal work packages. システムへの入力や、内部のワークパッケージの受け渡しを行うためのデータ構造として、イベントを使用しています。

- The entire app is now best described as a message processor, or an event processor if you prefer. We’ll talk about the distinction in the next chapter. このアプリは、メッセージ・プロセッサー、またはイベント・プロセッサーと呼ぶのが適切でしょう。 この区別については、次の章で説明します。

## 1.3. Implementing Our New Requirement 新要件の実装

We’re done with our refactoring phase.
リファクタリングの段階は終了です。
Let’s see if we really have “made the change easy.”
本当に「変更を簡単に」できたかどうか見てみましょう。
Let’s implement our new requirement, shown in Figure 9-4: we’ll receive as our inputs some new `BatchQuantityChanged` events and pass them to a handler, which in turn might emit some `AllocationRequired` events, and those in turn will go back to our existing handler for reallocation.
図 9-4 に示すように、新しい要件を実装してみましょう。新しい `BatchQuantityChanged` イベントを入力として受け取り、それをハンドラに渡します。ハンドラは次に `AllocationRequired` イベントを発行し、それが既存のハンドラに戻って再割り当てを行います。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0904.png)

- WARNING 警告

- When you split things out like this across two units of work, you now have two database transactions, so you are opening yourself up to integrity issues: something could happen that means the first transaction completes but the second one does not. You’ll need to think about whether this is acceptable, and whether you need to notice when it happens and do something about it. See “Footguns” for more discussion. このように物事を2つの作業単位に分割すると、2つのデータベーストランザクションが発生するため、整合性の問題に直面する可能性があります。 このような事態を許容できるかどうか、また、このような事態が発生したときに気づいて何か対処する必要があるかどうかを考える必要があります。 より詳細な議論は「フットガン」を参照してください。

### 1.3.1. Our New Event 私たちの新しいイベント

The event that tells us a batch quantity has changed is simple; it just needs a batch reference and a new quantity:
バッチ数量が変更されたことを伝えるイベントはシンプルで、バッチ参照と新しい数量が必要なだけです。

New event (src
新規イベント（src

```python
@dataclass
class BatchQuantityChanged(Event):
    ref: str
    qty: int
```

## 1.4. Test-Driving a New Handler 新しいハンドラをテストドライブする

Following the lessons learned in Chapter 4, we can operate in “high gear” and write our unit tests at the highest possible level of abstraction, in terms of events.
第4章での教訓を生かし、ユニットテストを「ハイギア」で動作させ、イベントの観点から可能な限り高い抽象度で書くことができます。
Here’s what they might look like:
以下のような感じです。

Handler tests for change_batch_quantity (tests
change_batch_quantity のハンドラテスト (tests)

```python
class TestChangeBatchQuantity:

    def test_changes_available_quantity(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            events.BatchCreated("batch1", "ADORABLE-SETTEE", 100, None), uow
        )
        [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
        assert batch.available_quantity == 100  1

        messagebus.handle(events.BatchQuantityChanged("batch1", 50), uow)

        assert batch.available_quantity == 50  1


    def test_reallocates_if_necessary(self):
        uow = FakeUnitOfWork()
        event_history = [
            events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
            events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50, date.today()),
            events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
            events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20),
        ]
        for e in event_history:
            messagebus.handle(e, uow)
        [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
        assert batch1.available_quantity == 10
        assert batch2.available_quantity == 50

        messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow)

        # order1 or order2 will be deallocated, so we'll have 25 - 20
        assert batch1.available_quantity == 5  2
        # and 20 will be reallocated to the next batch
        assert batch2.available_quantity == 30  2
```

1. The simple case would be trivially easy to implement; we just modify a quantity. 単純なケースでは、量を変更するだけなので、実装は些細に簡単です。

2. But if we try to change the quantity to less than has been allocated, we’ll need to deallocate at least one order, and we expect to reallocate it to a new batch. しかし、数量を割り当て済みより少なく変更しようとすると、少なくとも1つの注文の割り当てを解除する必要があり、新しいバッチに再割り当てされることが予想されます。

### 1.4.1. Implementation 実装

Our new handler is very simple:
新しいハンドラはとてもシンプルです。

Handler delegates to model layer (src
ハンドラはモデル層に委譲する（src

```python
def change_batch_quantity(
        event: events.BatchQuantityChanged, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get_by_batchref(batchref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
        uow.commit()
```

We realize we’ll need a new query type on our repository:
私たちは、リポジトリに新しいクエリータイプが必要であることを理解しています。

A new query type on our repository (src
私たちのリポジトリにある新しいクエリタイプ（src

```python
class AbstractRepository(abc.ABC):
    ...

    def get(self, sku) -> model.Product:
        ...

    def get_by_batchref(self, batchref) -> model.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref) -> model.Product:
        raise NotImplementedError
    ...

class SqlAlchemyRepository(AbstractRepository):
    ...

    def _get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()

    def _get_by_batchref(self, batchref):
        return self.session.query(model.Product).join(model.Batch).filter(
            orm.batches.c.reference == batchref,
        ).first()
```

And on our `FakeRepository` too:
そして、私たちの `FakeRepository` にも。

Updating the fake repo too (tests
フェイクレポも更新（テスト

```python
class FakeRepository(repository.AbstractRepository):
    ...

    def _get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def _get_by_batchref(self, batchref):
        return next((
            p for p in self._products for b in p.batches
            if b.reference == batchref
        ), None)
```

- NOTE 注

- We’re adding a query to our repository to make this use case easier to implement. So long as our query is returning a single aggregate, we’re not bending any rules. If you find yourself writing complex queries on your repositories, you might want to consider a different design. Methods like `get_most_popular_products` or `find_products_by_order_id` in particular would definitely trigger our spidey sense. Chapter 11 and the epilogue have some tips on managing complex queries. このユースケースを簡単に実装するために、リポジトリにクエリを追加しています。 このクエリが単一の集約を返す限り、何のルールも曲げることはありません。 もしリポジトリに複雑なクエリを書いているのであれば、別の設計を検討したほうがよいでしょう。 特に `get_most_popular_products` や `find_products_by_order_id` のようなメソッドは、間違いなく我々のスパイダーセンスを刺激することでしょう。 11章とエピローグでは、複雑なクエリを管理するためのいくつかのヒントを紹介します。

### 1.4.2. A New Method on the Domain Model ドメインモデルに関する新手法

We add the new method to the model, which does the quantity change and deallocation(s) inline and publishes a new event.
新しいメソッドをモデルに追加し、量の変更と割り当て解除をインラインで行い、新しいイベントを発行します。
We also modify the existing allocate function to publish an event:
また、既存のallocate関数を修正して、イベントを発行するようにします。

Our model evolves to capture the new requirement (src
私たちのモデルは、新しい要件を満たすように進化しています（src

```python
class Product:
    ...

    def change_batch_quantity(self, ref: str, qty: int):
        batch = next(b for b in self.batches if b.reference == ref)
        batch._purchased_quantity = qty
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            self.events.append(
                events.AllocationRequired(line.orderid, line.sku, line.qty)
            )
...

class Batch:
    ...

    def deallocate_one(self) -> OrderLine:
        return self._allocations.pop()
```

We wire up our new handler:
新しいハンドラーを配線する。

The message bus grows (src
メッセージバスが成長する（src

```python
HANDLERS = {
    events.BatchCreated: [handlers.add_batch],
    events.BatchQuantityChanged: [handlers.change_batch_quantity],
    events.AllocationRequired: [handlers.allocate],
    events.OutOfStock: [handlers.send_out_of_stock_notification],

}  # type: Dict[Type[events.Event], List[Callable]]
```

And our new requirement is fully implemented.
そして、私たちの新しい要件は完全に実行されます。

## 1.5. Optionally: Unit Testing Event Handlers in Isolation with a Fake Message Bus Optionally: 偽のメッセージバスでイベントハンドラを分離してユニットテストする

Our main test for the reallocation workflow is edge-to-edge (see the example code in “Test-Driving a New Handler”).
私たちの再割り当てワークフローのメインテストは edge-to-edge です (「新しいハンドラのテスト駆動」のサンプルコードを参照してください)。
It uses the real message bus, and it tests the whole flow, where the `BatchQuantityChanged` event handler triggers deallocation, and emits new `AllocationRequired` events, which in turn are handled by their own handlers.
これは実際のメッセージバスを使用しており、`BatchQuantityChanged` イベントハンドラが割り当て解除のトリガーとなり、新しい `AllocationRequired` イベントを発生させ、そのイベントがそれぞれのハンドラによって処理されるというフロー全体をテストしています。
One test covers a chain of multiple events and handlers.
一つのテストが複数のイベントとハンドラの連鎖をカバーします。

Depending on the complexity of your chain of events, you may decide that you want to test some handlers in isolation from one another.
イベントの連鎖の複雑さによっては、いくつかのハンドラを分離してテストしたいと思うかもしれません。
You can do this using a “fake” message bus.
これは、"偽の "メッセージバスを使って行うことができます。

In our case, we actually intervene by modifying the `publish_events()` method on `FakeUnitOfWork` and decoupling it from the real message bus, instead making it record what events it sees:
この例では、`FakeUnitOfWork` の `publish_events()` メソッドを修正して、実際のメッセージバスから切り離し、代わりに見たイベントを記録するようにすることで、実際に介入しています。

Fake message bus implemented in UoW (tests
UoWに実装された偽メッセージバス（テスト

```python
class FakeUnitOfWorkWithFakeMessageBus(FakeUnitOfWork):

    def __init__(self):
        super().__init__()
        self.events_published = []  # type: List[events.Event]

    def publish_events(self):
        for product in self.products.seen:
            while product.events:
                self.events_published.append(product.events.pop(0))
```

Now when we invoke `messagebus.handle()` using the `FakeUnitOfWorkWithFakeMessageBus`, it runs only the handler for that event.
これで、`FakeUnitOfWorkWithFakeMessageBus` を使って `messagebus.handle()` を呼び出すと、そのイベントのハンドラーだけが実行されるようになりました。
So we can write a more isolated unit test: instead of checking all the side effects, we just check that `BatchQuantityChanged` leads to `AllocationRequired` if the quantity drops below the total already allocated:
つまり、すべての副作用をチェックするのではなく、`BatchQuantityChanged` が、量がすでに割り当てられている合計よりも少なくなった場合に `AllocationRequired` につながることだけをチェックすればいいのです。

Testing reallocation in isolation (tests
再割り当てを単独でテストする（テスト

```python
def test_reallocates_if_necessary_isolated():
    uow = FakeUnitOfWorkWithFakeMessageBus()

    # test setup as before
    event_history = [
        events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
        events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50, date.today()),
        events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
        events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20),
    ]
    for e in event_history:
        messagebus.handle(e, uow)
    [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
    assert batch1.available_quantity == 10
    assert batch2.available_quantity == 50

    messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow)

    # assert on new events emitted rather than downstream side-effects
    [reallocation_event] = uow.events_published
    assert isinstance(reallocation_event, events.AllocationRequired)
    assert reallocation_event.orderid in {'order1', 'order2'}
    assert reallocation_event.sku == 'INDIFFERENT-TABLE'
```

Whether you want to do this or not depends on the complexity of your chain of events.
これを行うかどうかは、イベントの連鎖の複雑さによって決まります。
We say, start out with edge-to-edge testing, and resort to this only if necessary.
私たちは、まずエッジ・トゥ・エッジテストから始め、必要な場合にのみエッジ・トゥ・エッジテストに頼ればいいと言っています。

# 2. =========================================

- EXERCISE FOR THE READER 読書運動

A great way to force yourself to really understand some code is to refactor it.
あるコードを本当に理解することを自分に強制する素晴らしい方法は、それをリファクタリングすることです。
In the discussion of testing handlers in isolation, we used something called `FakeUnitOfWorkWithFakeMessageBus`, which is unnecessarily complicated and violates the SRP.
ハンドラを分離してテストするという議論では、`FakeUnitOfWorkWithFakeMessageBus`というものを使いましたが、これは不必要に複雑でSRPに違反しています。

If we change the message bus to being a class,3 then building a FakeMessageBus is more straightforward:
メッセージバスをクラスとすれば3、FakeMessageBusの構築はより簡単になる。

An abstract message bus and its real and fake versions
抽象的なメッセージバスとその実機・偽機

```python
class AbstractMessageBus:
    HANDLERS: Dict[Type[events.Event], List[Callable]]

    def handle(self, event: events.Event):
        for handler in self.HANDLERS[type(event)]:
            handler(event)


class MessageBus(AbstractMessageBus):
    HANDLERS = {
        events.OutOfStock: [send_out_of_stock_notification],

    }


class FakeMessageBus(messagebus.AbstractMessageBus):
    def __init__(self):
        self.events_published = []  # type: List[events.Event]
        self.handlers = {
            events.OutOfStock: [lambda e: self.events_published.append(e)]
        }
```

So jump into the code on GitHub and see if you can get a class-based version working, and then write a version of `test_reallocates_if_necessary_isolated()` from earlier.
そこで、GitHub にあるコードに飛び込んで、クラスベースのバージョンが動作するかどうかを確認し、先ほどの `test_reallocates_if_necessary_isolated()` のバージョンを書いてみてください。

We use a class-based message bus in Chapter 13, if you need more inspiration.
第13章では、クラスベースのメッセージバスを使用しています。

# 3. ========================================================

## 3.1. Wrap-Up まとめ

Let’s look back at what we’ve achieved, and think about why we did it.
私たちが達成したことを振り返り、なぜそれをしたのかを考えてみましょう。

### 3.1.1. What Have We Achieved? 私たちは何を達成したのでしょうか？

Events are simple dataclasses that define the data structures for inputs and internal messages within our system.
イベントは、システム内の入力と内部メッセージのデータ構造を定義するシンプルなデータクラスである。
This is quite powerful from a DDD standpoint, since events often translate really well into business language (look up event storming if you haven’t already).
イベントはしばしばビジネス言語にうまく変換されるため、これはDDDの観点から非常に強力です（まだの方はイベントストーミングを調べてみてください）。

Handlers are the way we react to events.
ハンドラは、イベントに反応する方法です。
They can call down to our model or call out to external services.
ハンドラは私たちのモデルを呼び出したり、外部サービスを呼び出したりすることができます。
We can define multiple handlers for a single event if we want to.
必要であれば、1つのイベントに対して複数のハンドラを定義することができます。
Handlers can also raise other events.
ハンドラは、他のイベントを発生させることもできる。
This allows us to be very granular about what a handler does and really stick to the SRP.
これにより、ハンドラが何をするかについて非常に細かく設定することができ、SRPに本当に忠実であることができます。

### 3.1.2. Why Have We Achieved? なぜ、私たちは成功したのか？

Our ongoing objective with these architectural patterns is to try to have the complexity of our application grow more slowly than its size.
これらのアーキテクチャパターンを使用する目的は、アプリケーションの複雑さがそのサイズよりも緩やかに成長するようにすることです。
When we go all in on the message bus, as always we pay a price in terms of architectural complexity (see Table 9-1), but we buy ourselves a pattern that can handle almost arbitrarily complex requirements without needing any further conceptual or architectural change to the way we do things.
メッセージバスに全力を注ぐと、いつものようにアーキテクチャーの複雑さという代償を払うことになりますが（表9-1参照）、それ以上の概念的あるいはアーキテクチャーの変更を必要とせずに、ほとんど任意の複雑な要求を処理できるパターンを手に入れることができるのです。

Here we’ve added quite a complicated use case (change quantity, deallocate, start new transaction, reallocate, publish external notification), but architecturally, there’s been no cost in terms of complexity.
ここでは、かなり複雑なユースケース（量の変更、割り当て解除、新しいトランザクションの開始、再割り当て、外部通知の発行）を追加しましたが、アーキテクチャ的には、複雑さの点ではコストはかかっていません。
We’ve added new events, new handlers, and a new external adapter (for email), all of which are existing categories of things in our architecture that we understand and know how to reason about, and that are easy to explain to newcomers.
新しいイベント、新しいハンドラ、そして新しい外部アダプタ（メール用）を追加しましたが、これらはすべて、私たちが理解し、推論する方法を知っているアーキテクチャの既存のカテゴリであり、新規参入者に簡単に説明することができます。
Our moving parts each have one job, they’re connected to each other in well-defined ways, and there are no unexpected side effects.
私たちの可動部品はそれぞれ1つの仕事を持ち、明確に定義された方法で互いに接続されており、予期せぬ副作用はありません。

Table 9-1.
表9-1.
Whole app is a message bus: the trade-offs
アプリ全体がメッセージバス：トレードオフの関係

- Pros 長所

- Handlers and services are the same thing, so that’s simpler. ハンドラとサービスは同じものだから、その方がシンプルでいい。

- We have a nice data structure for inputs to the system. システムへの入力のための素敵なデータ構造があります。

- Cons 短所

- A message bus is still a slightly unpredictable way of doing things from a web point of view. You don’t know in advance when things are going to end. メッセージバスは、Webの観点から見ると、やはり少し予測不可能な方法です。 いつ終わるのか、事前にわからないのです。

- There will be duplication of fields and structure between model objects and events, which will have a maintenance cost. Adding a field to one usually means adding a field to at least one of the others. モデルオブジェクトとイベントの間で、フィールドや構造の重複が発生し、メンテナンスコストがかかります。 通常、1つのフィールドを追加することは、他のフィールドの少なくとも1つにフィールドを追加することを意味します。

Now, you may be wondering, where are those `BatchQuantityChanged` events going to come from?
さて、この `BatchQuantityChanged` イベントはどこから来るのだろうかと疑問に思うかもしれません。
The answer is revealed in a couple chapters’ time.
その答えは、数章後に明らかになります。
But first, let’s talk about events versus commands.
しかしその前に、イベントとコマンドの違いについて説明しましょう。

1. Event-based modeling is so popular that a practice called event storming has been developed for facilitating event-based requirements gathering and domain model elaboration. イベントベースモデリングは、イベントベースの要求収集やドメインモデルの推敲を容易にするために、イベントストーミングと呼ばれるプラクティスが開発されるほど普及している。

2. If you’ve done a bit of reading about event-driven architectures, you may be thinking, “Some of these events sound more like commands!” Bear with us! We’re trying to introduce one concept at a time. In the next chapter, we’ll introduce the distinction between commands and events. イベント駆動型アーキテクチャについて少し読んだことがある人は、"これらのイベントのいくつかは、むしろコマンドのように聞こえる！"と思うかもしれません。 我慢してください。 一度にひとつの概念を紹介するつもりです。 次の章では、コマンドとイベントの区別について説明します。

3. The “simple” implementation in this chapter essentially uses the messagebus.py module itself to implement the Singleton Pattern. この章の「シンプルな」実装は、基本的にmessagebus.pyモジュールそのものを使ってSingletonパターンを実装しています。
