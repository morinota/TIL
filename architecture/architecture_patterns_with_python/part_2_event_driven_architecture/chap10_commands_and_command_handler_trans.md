# Chapter 10. Commands and Command Handler 第10章 コマンドとコマンドハンドラ

In the previous chapter, we talked about using events as a way of representing the inputs to our system, and we turned our application into a message-processing machine.
前章では、システムへの入力を表現する方法としてEventを使用し、**アプリケーションをメッセージ処理マシン(message-processing machine)に変身させる**という話をした.

To achieve that, we converted all our use-case functions to event handlers.
これを実現するために、すべてのユースケース関数(=Service layer function?)をEvent Handlerに変換した.
When the API receives a POST to create a new batch, it builds a new BatchCreated event and handles it as if it were an internal event.
APIが新しいBatchを作成するためのPOSTを受け取ると、新しいBatchCreatedイベントを構築し、それを internal event のように処理する.
This might feel counterintuitive.
これは直感に反していると感じるかもしれない.
After all, the batch hasn’t been created yet; that’s why we called the API.
結局のところ、バッチはまだ作成されておらず、それがAPIを呼び出した理由である.
We’re going to fix that conceptual wart by introducing commands and showing how they can be handled by the same message bus but with slightly different rules.
私たちは、commandsを導入し、それらが同じメッセージバスによってどのように処理されるかを示すことによって、その概念のイボを修正するつもりですが、わずかに異なるルールを持っています

# ===================

TIP
ヒント

The code for this chapter is in the chapter_10_commands branch on GitHub:
この章のコードは、GitHubのchapter_10_commandsブランチにあります。

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_10_commands
# or to code along, checkout the previous chapter:
git checkout chapter_09_all_messagebus
```

## Commands and Events コマンドとイベント

Like events, commands are a type of message—instructions sent by one part of a system to another.
イベントと同様に、コマンドもメッセージの一種であり、システムのある部分から別の部分に送られる命令である。
We usually represent commands with dumb data structures and can handle them in much the same way as events.
通常、コマンドはダムデータ構造で表現され、イベントとほぼ同じように扱うことができる。

The differences between commands and events, though, are important.
しかし、コマンドとイベントの違いは重要です。

Commands are sent by one actor to another specific actor with the expectation that a particular thing will happen as a result.
コマンドは、あるアクターが別の特定のアクターに、その結果として特定のことが起こることを期待して送信するものである。
When we post a form to an API handler, we are sending a command.
APIハンドラにフォームを送信するとき、私たちはコマンドを送信していることになる。
We name commands with imperative mood verb phrases like “allocate stock” or “delay shipment.”
コマンドの名前は、"allocate stock" や "delay shipment" といった命令形の動詞句で表される。

Commands capture intent.
コマンドは意図を把握するものです。
They express our wish for the system to do something.
システムに何かをしてほしいという意思を表現しているのです。
As a result, when they fail, the sender needs to receive error information.
そのため、失敗した場合には、エラー情報を受け取る必要があります。

Events are broadcast by an actor to all interested listeners.
イベントは、アクターによって興味のあるリスナー全てにブロードキャストされます。
When we publish `BatchQuantityChanged`, we don’t know who’s going to pick it up.
私たちが `BatchQuantityChanged` を公開するとき、誰がそれをピックアップするのかわかりません。
We name events with past-tense verb phrases like “order allocated to stock” or “shipment delayed.”
イベントには "order allocated to stock" や "shipment delayed" のような過去形の動詞句で名前を付けます。

We often use events to spread the knowledge about successful commands.
私たちは、成功したコマンドの知識を広めるために、イベントをよく利用します。

Events capture facts about things that happened in the past.
イベントは、過去に起こった事柄に関する事実を捕捉します。
Since we don’t know who’s handling an event, senders should not care whether the receivers succeeded or failed.
誰がイベントを処理しているかは分からないので、送信者は受信者が成功したか失敗したかを気にするべきではありません。
Table 10-1 recaps the differences.
表10-1に違いをまとめました。

Table 10-1.
表10-1.
Events versus commands
イベントとコマンドの比較

What kinds of commands do we have in our system right now?
今、私たちのシステムにはどのようなコマンドがあるのでしょうか。

Pulling out some commands (src
いくつかのコマンドを抜き出す (src

```python
class Command:
    pass

@dataclass
class Allocate(Command):  1
    orderid: str
    sku: str
    qty: int

@dataclass
class CreateBatch(Command):  2
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

@dataclass
class ChangeBatchQuantity(Command):  3
    ref: str
    qty: int
```

1. `commands.Allocate` will replace `events.AllocationRequired`. 1. `commands.Allocate` が `events.AllocationRequired` に置き換わります。

2. `commands.CreateBatch` will replace `events.BatchCreated`. 2. `commands.CreateBatch` は `events.BatchCreated` を置き換えます。

3. `commands.ChangeBatchQuantity` will replace `events.BatchQuantityChanged`. 3. `commands.ChangeBatchQuantity` は `events.BatchQuantityChanged` を置き換えます。

## Differences in Exception Handling 例外が発生した場合の処理の違い

Just changing the names and verbs is all very well, but that won’t change the behavior of our system.
名前と動詞を変えるだけでは、システムの動作は変わりません。
We want to treat events and commands similarly, but not exactly the same.
イベントとコマンドを同じように扱いたいのですが、全く同じにはできません。
Let’s see how our message bus changes:
メッセージ・バスがどのように変化するか見てみましょう。

Dispatch events and commands differently (src
イベントとコマンドのディスパッチが異なる（src

```python
Message = Union[commands.Command, events.Event]


def handle(message: Message, uow: unit_of_work.AbstractUnitOfWork):  1
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(message, queue, uow)  2
        elif isinstance(message, commands.Command):
            cmd_result = handle_command(message, queue, uow)  2
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')
    return results
```

1. It still has a main `handle()` entrypoint that takes a `message`, which may be a command or an event. メインとなる `handle()` エントリポイントを持ち、コマンドやイベントのような `message` を受け取ります。

2. We dispatch events and commands to two different helper functions, shown next. イベントとコマンドは、次に示す2種類のヘルパー関数にディスパッチします。

Here’s how we handle events:
ここでは、イベントの取り扱いについて説明します。

Events cannot interrupt the flow (src
イベントはフローを中断できない（src

```python
def handle_event(
    event: events.Event,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):
    for handler in EVENT_HANDLERS[type(event)]:  1
        try:
            logger.debug('handling event %s with handler %s', event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling event %s', event)
            continue  2
```

1. Events go to a dispatcher that can delegate to multiple handlers per event. イベントは、イベントごとに複数のハンドラに委譲することができるディスパッチャに送られます。

2. It catches and logs errors but doesn’t let them interrupt message processing. エラーを捕捉して記録するが、エラーによってメッセージの処理が中断されることはない。

And here’s how we do commands:
そして、コマンドのやり方はこうです。

Commands reraise exceptions (src
コマンド reraise exceptions (src)

```python
def handle_command(
    command: commands.Command,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):
    logger.debug('handling command %s', command)
    try:
        handler = COMMAND_HANDLERS[type(command)]  1
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result  3
    except Exception:
        logger.exception('Exception handling command %s', command)
        raise  2
```

1. The command dispatcher expects just one handler per command. コマンドディスパッチャは、1つのコマンドにつき1つのハンドラを想定しています。

2. If any errors are raised, they fail fast and will bubble up. 何かエラーが発生した場合、高速で失敗し、泡となる。

3. `return result` is only temporary; as mentioned in “A Temporary Ugly Hack: The Message Bus Has to Return Results”, it’s a temporary hack to allow the message bus to return the batch reference for the API to use. We’ll fix this in Chapter 12. `return result` は一時的なものです。「一時的な醜いハック：メッセージバスは結果を返さなければならない」で述べたように、メッセージバスがAPIが使用するためのバッチリファレンスを返せるようにするための一時的なハックなのです。 これは第12章で修正する予定です。

We also change the single `HANDLERS` dict into different ones for commands and events.
また、単一の `HANDLERS` ディクショナリを、コマンドとイベントのための異なるディクショナリに変更します。
Commands can have only one handler, according to our convention:
コマンドは、私たちの慣習に従って、1つのハンドラしか持つことができません。

New handlers dicts (src
新規ハンドラ dicts (src)

```python
EVENT_HANDLERS = {
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.Allocate: handlers.allocate,
    commands.CreateBatch: handlers.add_batch,
    commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]
```

## Discussion: Events, Commands, and Error Handling ディスカッション イベント、コマンド、エラー処理

Many developers get uncomfortable at this point and ask, “What happens when an event fails to process?
多くの開発者はこの時点で不安になり、「イベントの処理に失敗したらどうするんだ？
How am I supposed to make sure the system is in a consistent state?”
イベントの処理に失敗したときはどうするんだ?
If we manage to process half of the events during `messagebus.handle` before an out-of-memory error kills our process, how do we mitigate problems caused by the lost messages?
もし、メモリ不足のエラーでプロセスが停止する前に `messagebus.handle` でイベントの半分を処理できたとして、失われたメッセージによって引き起こされる問題をどのように軽減するのでしょうか？

Let’s start with the worst case: we fail to handle an event, and the system is left in an inconsistent state.
まずは最悪のケースから。イベント処理に失敗し、システムに矛盾が生じたままになってしまうのです。
What kind of error would cause this?
どのようなエラーが発生したら、このような状態になるのでしょうか？
Often in our systems we can end up in an inconsistent state when only half an operation is completed.
私たちのシステムでは、しばしば操作の半分しか完了していないのに、矛盾した状態になってしまうことがあります。

For example, we could allocate three units of `DESIRABLE_BEANBAG` to a customer’s order but somehow fail to reduce the amount of remaining stock.
例えば、`DESIRABLE_BEANBAG` を顧客の注文に3個割り当てたのに、なぜか残りの在庫を減らせなかったとします。
This would cause an inconsistent state: the three units of stock are both allocated and available, depending on how you look at it.
これは矛盾した状態を引き起こします。3つの在庫は、見方によっては、割り当てられたものでもあり、利用可能なものでもあるのです。
Later, we might allocate those same beanbags to another customer, causing a headache for customer support.
後で、同じ豆袋を別の顧客に割り当てて、カスタマーサポートの頭痛の種になるかもしれません。

In our allocation service, though, we’ve already taken steps to prevent that happening.
しかし、私たちのアロケーション・サービスでは、そのようなことが起こらないようにするための措置をすでに講じています。
We’ve carefully identified aggregates that act as consistency boundaries, and we’ve introduced a UoW that manages the atomic success or failure of an update to an aggregate.
一貫性の境界として機能するアグリゲートを慎重に特定し、アグリゲートへの更新のアトミックな成功または失敗を管理するUoWを導入しているのです。

For example, when we allocate stock to an order, our consistency boundary is the `Product` aggregate.
たとえば、注文に在庫を割り当てる場合、一貫性の境界は `Product` という集合体です。
This means that we can’t accidentally overallocate: either a particular order line is allocated to the product, or it is not—there’s no room for inconsistent states.
つまり、誤って過剰に在庫を割り当てることはできません。特定の注文行が製品に割り当てられるか、そうでないかのどちらかです。

By definition, we don’t require two aggregates to be immediately consistent, so if we fail to process an event and update only a single aggregate, our system can still be made eventually consistent.
定義によると、2つの集約がすぐに一致する必要はありません。したがって、イベントの処理に失敗し、1つの集約だけを更新した場合でも、システムは最終的に一致するようにすることができます。
We shouldn’t violate any constraints of the system.
システムの制約に違反してはいけません。

With this example in mind, we can better understand the reason for splitting messages into commands and events.
この例を念頭に置くと、メッセージをコマンドとイベントに分割する理由がよく理解できます。
When a user wants to make the system do something, we represent their request as a command.
ユーザーがシステムに何かをさせたいとき、その要求をコマンドとして表現します。
That command should modify a single aggregate and either succeed or fail in totality.
そのコマンドは1つのアグリゲートを変更し、全体として成功するか失敗するかのどちらかであるべきです。
Any other bookkeeping, cleanup, and notification we need to do can happen via an event.
その他、必要な帳簿や後始末、通知などはすべてイベントを介して行われます。
We don’t require the event handlers to succeed in order for the command to be successful.
コマンドを成功させるために、イベントハンドラが成功する必要はありません。

Let’s look at another example (from a different, imaginary projet) to see why not.
なぜそうならないか、別の例（別の架空のプロジェクト）を見てみましょう。

Imagine we are building an ecommerce website that sells expensive luxury goods.
高価な高級品を販売するeコマースサイトを構築しているとします。
Our marketing department wants to reward customers for repeat visits.
マーケティング部門は、顧客の再来訪に報いるために、報酬を与えたいと考えています。
We will flag customers as VIPs after they make their third purchase, and this will entitle them to priority treatment and special offers.
3回目の購入があった顧客をVIPとしてフラグを立て、優先的な扱いと特別なオファーを受ける権利を与えることにします。
Our acceptance criteria for this story reads as follows:
この話の受け入れ基準は、次のようになります。

```
Given a customer with two orders in their history,
When the customer places a third order,
Then they should be flagged as a VIP.

When a customer first becomes a VIP
Then we should send them an email to congratulate them
```

Using the techniques we’ve already discussed in this book, we decide that we want to build a new `History` aggregate that records orders and can raise domain events when rules are met.
この本ですでに説明したテクニックを使って、注文を記録し、ルールが満たされたときにドメインイベントを発生させることができる新しい `History` 集約を構築することにします。
We will structure the code like this:
コードはこのように構成します。

VIP customer (example code for a different project)
VIPのお客様（別プロジェクトでのコード例）

```python
class History:  # Aggregate

    def __init__(self, customer_id: int):
        self.orders = set() # Set[HistoryEntry]
        self.customer_id = customer_id

    def record_order(self, order_id: str, order_amount: int): 1
        entry = HistoryEntry(order_id, order_amount)

        if entry in self.orders:
            return

        self.orders.add(entry)

        if len(self.orders) == 3:
            self.events.append(
                CustomerBecameVIP(self.customer_id)
            )


def create_order_from_basket(uow, cmd: CreateOrder): 2
    with uow:
        order = Order.from_basket(cmd.customer_id, cmd.basket_items)
        uow.orders.add(order)
        uow.commit() # raises OrderCreated


def update_customer_history(uow, event: OrderCreated): 3
    with uow:
        history = uow.order_history.get(event.customer_id)
        history.record_order(event.order_id, event.order_amount)
        uow.commit() # raises CustomerBecameVIP


def congratulate_vip_customer(uow, event: CustomerBecameVip): 4
    with uow:
        customer = uow.customers.get(event.customer_id)
        email.send(
            customer.email_address,
            f'Congratulations {customer.first_name}!'
        )
```

1. The `History` aggregate captures the rules indicating when a customer becomes a VIP. This puts us in a good place to handle changes when the rules become more complex in the future. 履歴`集計は、顧客がいつVIPになるかを示すルールをキャプチャします。 これにより、将来的にルールがより複雑になった場合に、変更を処理するのに適した状態になります。

2. Our first handler creates an order for the customer and raises a domain event `OrderCreated`. 最初のハンドラは、顧客の注文を作成し、ドメインイベント `OrderCreated` を発生させます。

3. Our second handler updates the `History` object to record that an order was created. 2番目のハンドラは `History` オブジェクトを更新して、注文が作成されたことを記録します。

4. Finally, we send an email to the customer when they become a VIP. 最後に、お客様がVIPになられた際に、メールを送信します。

Using this code, we can gain some intuition about error handling in an event-driven system.
このコードを使って、イベント駆動型システムにおけるエラー処理について、いくつかの直感を得ることができます。

In our current implementation, we raise events about an aggregate after we persist our state to the database.
現在の実装では、状態をデータベースに永続化した後に、アグリゲートに関するイベントを発生させています。
What if we raised those events before we persisted, and committed all our changes at the same time?
もし、永続化する前にイベントを発生させ、すべての変更を同時にコミットしたらどうでしょうか？
That way, we could be sure that all the work was complete.
そうすれば、すべての作業が完了したことを確認することができます。
Wouldn’t that be safer?
その方が安全ではないでしょうか？

What happens, though, if the email server is slightly overloaded?
しかし、メールサーバーが少しでも過負荷になるとどうなるのでしょうか？
If all the work has to complete at the same time, a busy email server can stop us from taking money for orders.
すべての作業を同時に完了させなければならない場合、メールサーバーが混雑すると、注文のためのお金を取ることができなくなることがあります。

What happens if there is a bug in the implementation of the `History` aggregate?
履歴`集計の実装にバグがあった場合、どうなりますか？
Should we fail to take your money just because we can’t recognize you as a VIP?
あなたをVIPと認識できないからといって、お金を受け取れないようにしなければならないのでしょうか？

By separating out these concerns, we have made it possible for things to fail in isolation, which improves the overall reliability of the system.
これらの懸念事項を分離することで、物事が単独で失敗することを可能にし、システム全体の信頼性を向上させているのです。
The only part of this code that has to complete is the command handler that creates an order.
このコードの中で唯一完了しなければならないのは、注文を作成するコマンドハンドラです。
This is the only part that a customer cares about, and it’s the part that our business stakeholders should prioritize.
これはお客様が気にする唯一の部分であり、ビジネス・ステークホルダーが優先すべき部分です。

Notice how we’ve deliberately aligned our transactional boundaries to the start and end of the business processes.
トランザクションの境界を、ビジネスプロセスの開始と終了に意図的に合わせていることに注目してください。
The names that we use in the code match the jargon used by our business stakeholders, and the handlers we’ve written match the steps of our natural language acceptance criteria.
コードで使用する名前は、ビジネス関係者が使用する専門用語と一致し、記述したハンドラは自然言語の受け入れ基準のステップと一致しています。
This concordance of names and structure helps us to reason about our systems as they grow larger and more complex.
このように名前と構造を一致させることで、システムが大きく複雑になった場合でも、推論がしやすくなります。

## Recovering from Errors Synchronously エラーを同期的に回復する

Hopefully we’ve convinced you that it’s OK for events to fail independently from the commands that raised them.
ここまでで、イベントが発生したコマンドとは無関係に失敗しても構わないということがお分かりいただけたと思います。
What should we do, then, to make sure we can recover from errors when they inevitably occur?
では、どうしても発生するエラーから回復するためには、どうすればよいのでしょうか？

The first thing we need is to know when an error has occurred, and for that we usually rely on logs.
まず必要なのは、いつエラーが発生したかを知ることであり、そのためには通常、ログに頼ることになる。

Let’s look again at the `handle_event` method from our message bus:
メッセージバスの `handle_event` メソッドをもう一度見てみましょう。

Current handle function (src
現在のハンドル機能（src

```python
def handle_event(
    event: events.Event,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug('handling event %s with handler %s', event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling event %s', event)
            continue
```

When we handle a message in our system, the first thing we do is write a log line to record what we’re about to do.
私たちのシステムでメッセージを処理するとき、最初にすることは、これからすることを記録するためにログ行を書くことです。
For our `CustomerBecameVIP` use case, the logs might read as follows:
私たちの `CustomerBecameVIP` のユースケースの場合、ログは次のようになります。

```
Handling event CustomerBecameVIP(customer_id=12345)
with handler <function congratulate_vip_customer at 0x10ebc9a60>
```

Because we’ve chosen to use dataclasses for our message types, we get a neatly printed summary of the incoming data that we can copy and paste into a Python shell to re-create the object.
メッセージタイプにデータクラスを使用することにしたので、受信データの要約がきちんと印刷され、Pythonシェルにコピー＆ペーストしてオブジェクトを再作成することができます。

When an error occurs, we can use the logged data to either reproduce the problem in a unit test or replay the message into the system.
エラーが発生した場合、ログに記録されたデータを使って、ユニットテストで問題を再現したり、システムにメッセージを再生したりすることができます。

Manual replay works well for cases where we need to fix a bug before we can re-process an event, but our systems will always experience some background level of transient failure.
手動再生は、イベントを再処理する前にバグを修正する必要がある場合に有効ですが、システムには常にバックグラウンドで一定レベルの一時的な障害が発生します。
This includes things like network hiccups, table deadlocks, and brief downtime caused by deployments.
これには、ネットワーク障害、テーブルのデッドロック、デプロイメントによる短時間のダウンタイムなどが含まれます。

For most of those cases, we can recover elegantly by trying again.
ほとんどの場合、再試行することでエレガントに回復することができます。
As the proverb says, “If at first you don’t succeed, retry the operation with an exponentially increasing back-off period.”
ことわざにもあるように、"最初に成功しなければ、指数関数的に増加するバックオフ期間を使って操作をやり直せ "ということです。

Handle with retry (src
リトライ付きハンドル (src)

```python
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential 1

...

def handle_event(
    event: events.Event,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork
):

    for handler in EVENT_HANDLERS[type(event)]:
        try:
            for attempt in Retrying(  2
                stop=stop_after_attempt(3),
                wait=wait_exponential()
            ):

                with attempt:
                    logger.debug('handling event %s with handler %s', event, handler)
                    handler(event, uow=uow)
                    queue.extend(uow.collect_new_events())
        except RetryError as retry_failure:
            logger.error(
                'Failed to handle event %s times, giving up!,
                retry_failure.last_attempt.attempt_number
            )
            continue
```

1. Tenacity is a Python library that implements common patterns for retrying. Tenacity は再試行のための一般的なパターンを実装した Python ライブラリです。

2. Here we configure our message bus to retry operations up to three times, with an exponentially increasing wait between attempts. ここでは、メッセージバスが最大3回まで操作を再試行し、試行間隔が指数関数的に長くなるように設定しています。

Retrying operations that might fail is probably the single best way to improve the resilience of our software.
失敗するかもしれない操作を再試行することは、おそらくソフトウェアの耐障害性を向上させる唯一最良の方法です。
Again, the Unit of Work and Command Handler patterns mean that each attempt starts from a consistent state and won’t leave things half-finished.
繰り返しになりますが、Unit of Work と Command Handler のパターンは、各試行が一貫した状態から始まり、物事を中途半端な状態で終わらせないことを意味します。

- WARNING 警告

- At some point, regardless of `tenacity`, we’ll have to give up trying to process the message. Building reliable systems with distributed messages is hard, and we have to skim over some tricky bits. There are pointers to more reference materials in the epilogue. ある時点で、「粘り強さ」に関係なく、メッセージを処理することをあきらめなければならなくなるのです。 分散メッセージで信頼性の高いシステムを構築することは難しく、いくつかの厄介な部分には目をつぶらなければならない。 エピローグには、より多くの参考資料へのポインタがあります。

## Wrap-Up まとめ

In this book we decided to introduce the concept of events before the concept of commands, but other guides often do it the other way around.
この本では、コマンドの概念の前にイベントの概念を導入することにしましたが、他のガイドではしばしばその逆になっています。
Making explicit the requests that our system can respond to by giving them a name and their own data structure is quite a fundamental thing to do.
システムが応答できるリクエストに名前と独自のデータ構造を与えて明示することは、非常に基本的なことです。
You’ll sometimes see people use the name Command Handler pattern to describe what we’re doing with Events, Commands, and Message Bus.
イベント、コマンド、メッセージバスでやっていることを説明するのに、コマンドハンドラーパターンという名前を使う人を時々見かけますが、これはそのためです。

Table 10-2 discusses some of the things you should think about before you jump on board.
表10-2は、飛びつく前に考えるべきことを述べている。

- Pros 長所

- Treating commands and events differently helps us understand which things have to succeed and which things we can tidy up later. コマンドとイベントを区別して扱うことで、どれが成功しなければならないか、どれが後で片づけられるかを理解することができます。

- `CreateBatch` is definitely a less confusing name than `BatchCreated`. We are being explicit about the intent of our users, and explicit is better than implicit, right? CreateBatch`は`BatchCreated` よりも紛らわしくない名前であることは間違いありません。 私たちはユーザーの意図に対して明示的であり、暗黙的であるよりも明示的である方が良いのではないでしょうか?

- Cons 短所

- The semantic differences between commands and events can be subtle. Expect bikeshedding arguments over the differences. コマンドとイベントの意味上の違いは、微妙な場合があります。 その違いをめぐっての激しい論争が予想されます。

- We’re expressly inviting failure. We know that sometimes things will break, and we’re choosing to handle that by making the failures smaller and more isolated. This can make the system harder to reason about and requires better monitoring. 私たちは、明示的に失敗を誘い込んでいるのです。 時には物事が壊れることを承知で、失敗をより小さく、より孤立したものにすることで対処することにしているのです。 そのため、システムを推論するのが難しくなり、より良い監視が必要になります。

In Chapter 11 we’ll talk about using events as an integration pattern.
第11章では、統合パターンとしてのイベントの利用について説明します。
