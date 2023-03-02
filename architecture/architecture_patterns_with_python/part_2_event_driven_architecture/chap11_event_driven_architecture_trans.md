# chapter 11. Event-Driven Architecture: Using Events To Integrate Microservices 第11章 イベント駆動型アーキテクチャ。 イベントを利用してマイクロサービスを統合する

In the preceding chapter, we never actually spoke about how we would receive the “batch quantity changed” events, or indeed, how we might notify the outside world about reallocations.
前章では、"バッチ数量が変更されました"というEventをどのように受け取るか、また、再割り当てをどのように外部に通知するかについて、実際に話をしたことはなかった.

We have a microservice with a web API, but what about other ways of talking to other systems?
ウェブAPIを持つマイクロサービスがありますが、他のシステムと会話する他の方法はどうでしょうか？
How will we know if, say, a shipment is delayed or the quantity is amended?
例えば、出荷が遅れたり、数量が修正された場合、どのようにして知ることができるだろうか？
How will we tell the warehouse system that an order has been allocated and needs to be sent to a customer?
注文が割り当てられ、顧客に送信する必要があることを倉庫システムにどのように伝えるのだろうか？

In this chapter, we’d like to show how the events metaphor can be extended to encompass the way that we handle incoming and outgoing messages from the system.
この章では、events metaphor(隠喩, 比喩) を拡張して、**システムからのメッセージの入出力をどのように処理するか**を紹介したいと思う.
Internally, the core of our application is now a message processor.
内部的には、アプリケーションの中核は message processor になっている.
Let’s follow through on that so it becomes a message processor externally as well.
続いて、外部でも message processor になるようにしよう.
As shown in Figure 11-1, our application will receive events from external sources via an external message bus (we’ll use Redis pub/sub queues as an example) and publish its outputs, in the form of events, back there as well.
図 11-1 に示すように、このアプリケーションは、**external mesage bus経由** (例として Redis pub/sub queue)で 外部ソースからイベントを受け取り、イベントという形でその出力もそこに戻すように発行する.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1101.png)

- TIP ヒント
- The code for this chapter is in the chapter_11_external_events branch on GitHub: この章のコードは、GitHubのchapter_11_external_eventsブランチにある.

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_11_external_events
# or to code along, checkout the previous chapter:
git checkout chapter_10_commands
```

## Distributed Ball of Mud, and Thinking in Nouns ♪泥の塊が分布し、名詞で思考する

Before we get into that, let’s talk about the alternatives.
その前に、代替案について説明する.
We regularly talk to engineers who are trying to build out a microservices architecture.
私たちは定期的に、マイクロサービス・アーキテクチャを構築しようとしているエンジニアと話をする.
Often they are migrating from an existing application, and their first instinct is to split their system into nouns.
多くの場合、彼らは既存のアプリケーションから移行してきており、最初の直感は、システムを名詞に分割することである.

What nouns have we introduced so far in our system?
これまで導入したシステムにはどんな名詞があっただろうか.
Well, we have batches of stock, orders, products, and customers.
さて、在庫のBatch、Order、Product、そしてCustomerである.
So a naive attempt at breaking up the system might have looked like Figure 11-2 (notice that we’ve named our system after a noun, Batches, instead of Allocation).
したがって、システムを単純に分割しようとすると、図11-2のようになる.(Allocationではなく、Batchesという名詞の名前をシステムにつけていることに注意してください).

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1102.png)

Each “thing” in our system has an associated service, which exposes an HTTP API.
このシステムの各 "モノ "には、関連するサービスがあり、HTTP APIを公開している.

Let’s work through an example happy-path flow in Figure 11-3: our users visit a website and can choose from products that are in stock.
図11-3のハッピーパスフローの例で作業してみよう. ユーザーがウェブサイトを訪問し、在庫のある商品から選ぶことができる.
When they add an item to their basket, we will reserve some stock for them.
ユーザが商品をカゴに入れたら、在庫を確保する.
When an order is complete, we confirm the reservation, which causes us to send dispatch instructions to the warehouse.
注文が完了すると、予約を確認し、倉庫に発送指示を出す.
Let’s also say, if this is the customer’s third order, we want to update the customer record to flag them as a VIP.
また、今回が3回目の注文の場合、顧客レコードを更新して、VIPとしてフラグを立てたいとする.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1103.png)

We can think of each of these steps as a command in our system: `ReserveStock`, `ConfirmReservation`, `DispatchGoods`, `MakeCustomerVIP`, and so forth.
これらの各ステップは、システム内のコマンドとして考えることができる.`ReserveStock`, `ConfirmReservation`, `DispatchGoods`, `MakeCustomerVIP` などである.

This style of architecture, where we create a microservice per database table and treat our HTTP APIs as CRUD interfaces to anemic models, is the most common initial way for people to approach service-oriented design.
**データベースのテーブルごとにマイクロサービスを作り**、HTTP APIを貧弱なモデルへのCRUDインターフェイスとして扱うこのスタイルは、サービス指向設計に取り組む最初の方法として最も一般的なものである.

This works fine for systems that are very simple, but it can quickly degrade into a distributed ball of mud.
これは、**非常にシンプルなシステムには有効だが、すぐに分散した泥の塊に劣化してしまう**.

To see why, let’s consider another case.
その理由を知るために、別のケースを考えてみよう.
Sometimes, when stock arrives at the warehouse, we discover that items have been water damaged during transit.
在庫が倉庫に到着したとき、輸送中に水濡れしていることが判明することがある.
We can’t sell water-damaged sofas, so we have to throw them away and request more stock from our partners.
水濡れしたソファーは売れないので、廃棄して、パートナーに在庫の追加を依頼しなければなりません.
We also need to update our stock model, and that might mean we need to reallocate a customer’s order.
また、在庫モデルを更新する必要があり、お客様の注文を再配置する必要があるかもしれない.

Where does this logic go?
このロジックはどこに行くのでしょうか？

Well, the Warehouse system knows that the stock has been damaged, so maybe it should own this process, as shown in Figure 11-4.
さて、倉庫システムは在庫が破損したことを知っているので、図11-4に示すように、このプロセスを所有する必要があるかもしれない.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1104.png)

This sort of works too, but now our dependency graph is a mess.
これも一応うまくいくのですが、今度は依存関係のグラフがぐちゃぐちゃになってしまった.
To allocate stock, the Orders service drives the Batches system, which drives Warehouse; but in order to handle problems at the warehouse, our Warehouse system drives Batches, which drives Orders.
しかし、倉庫での問題を処理するために、倉庫システムはBatchesを動かし、それがOrdersを動かすのである.

Multiply this by all the other workflows we need to provide, and you can see how services quickly get tangled up.
これを他のワークフローに当てはめると、いかにサービスが煩雑になるかがわかるはず.

## Error Handling in Distributed Systems 分散システムにおけるエラー処理

“Things break” is a universal law of software engineering.
"**Things break**" はソフトウェア工学の普遍的な法則である.
What happens in our system when one of our requests fails?
リクエストの1つが失敗したとき、私たちのシステムでは何が起こるのでしょうか?
Let’s say that a network error happens right after we take a user’s order for three `MISBEGOTTEN-RUG`, as shown in Figure 11-5.
図11-5に示すように、ユーザーが`MISBEGOTTEN-RUG`を3つ注文した直後に、ネットワークエラーが発生したとしよう.

We have two options here: we can place the order anyway and leave it unallocated, or we can refuse to take the order because the allocation can’t be guaranteed.
ここでは2つの選択肢がある. とにかく注文を出して未配分のままにしておくか、配分が保証できないので注文を受けるのを拒否するか、どちらかである.
The failure state of our batches service has bubbled up and is affecting the reliability of our order service.
バッチサービスの障害状態が湧き上がり、オーダーサービスの信頼性に影響を及ぼしているのである.

When two things have to be changed together, we say that they are coupled.
**2つのものが一緒に変化しなければならない(=双方向の依存関係?一方向も??)**とき、私たちはそれを"**couplingしている**"と言う.
We can think of this failure cascade as a kind of temporal coupling: every part of the system has to work at the same time for any part of it to work.
この故障のカスケードは、一種の **temporal coupling(時間的結合)**と考えることができる. **システムのどの部分が動作するにも、同時に動作する必要がある**である.
As the system gets bigger, there is an exponentially increasing probability that some part is degraded.
システムが大きくなればなるほど、どこかが劣化する確率は指数関数的に高くなる.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1105.png)

- Connascence

  - We’re using the term coupling here, but there’s another way to describe the relationships between our systems. Connascence is a term used by some authors to describe the different types of coupling. ここでは"coupling"という言葉を使っているが、システム間の関係を表現する別の方法がある "**Connascence(コナッセンス)**"は、異なるタイプのcoupling を表現するために一部の著者が使用している用語である.
  - Connascence isn’t bad, but some types of connascence are stronger than others. We want to have strong connascence locally, as when two classes are closely related, but weak connascence at a distance. コナセンスは悪いものではないが、コナセンスには強いタイプもある. 2つのクラスが密接に関連している場合のように、局所的には強いコナッセンスを持ちたいが、離れたところでは弱いコナッセンスを持ちたいのである.
  - In our first example of a distributed ball of mud, we see Connascence of Execution: multiple components need to know the correct order of work for an operation to be successful. 最初の泥の塊の例では、"**Connascence of Execution(実行の連鎖)**"が見られる.i.e. 作業を成功させるためには、複数のコンポーネントが正しい作業順序を知る必要がある.
  - When thinking about error conditions here, we’re talking about Connascence of Timing: multiple things have to happen, one after another, for the operation to work. ここでいうエラーとは、"**Connascence of Timing**"のことで、複数のことが次々に起こらないと動作しないことを指す.
  - When we replace our RPC-style system with events, we replace both of these types of connascence with a weaker type. That’s Connascence of Name: multiple components need to agree only on the name of an event and the names of fields it carries. RPCスタイルのシステムをイベントに置き換えるとき、この2つのタイプの接続をより弱いタイプに置き換える. つまり、"**Connascence of Name**"である. 複数のコンポーネントは、イベントの名前とそれが運ぶフィールドの名前についてだけ合意すればよい. (**なるほど...!これが良い=弱いConnascenceか...!**)
  - We can never completely avoid coupling, except by having our software not talk to any other software. What we want is to avoid inappropriate coupling. Connascence provides a mental model for understanding the strength and type of coupling inherent in different architectural styles. Read all about it at connascence.io. ソフトウェアが他のソフトウェアと会話しないようにすることを除けば、結合を完全に避けることはできない. 私たちが望むのは、**不適切な結合を避けること**である. **Connascenceは、異なるアーキテクチャスタイルに内在するcoupling の強さとタイプを理解するため**のメンタルモデルを提供する. connascence.ioでそのすべてを読むことができる.

## The Alternative: Temporal Decoupling Using Asynchronous Messaging 代替案 非同期メッセージングを用いた時間的デカップリング

How do we get appropriate coupling?
どうすれば適切な coupling が得られるのか.
We’ve already seen part of the answer, which is that we should think in terms of verbs, not nouns.
その答えの一部をすでに見てきた. それは、**名詞(noun)ではなく動詞(verb)で考えるべき**だということだ.
Our domain model is about modeling a business process.
私たちの **Domain Model は、ビジネスプロセスをモデル化するもの**である.
It’s not a static data model about a thing; it’s a model of a verb.
これは、ある物に関する静的なデータモデルではなく、**動詞のモデル**なのである. (例題におけるDomain Modelの本質は、"allocate"という動作??)

So instead of thinking about a system for orders and a system for batches, we think about a system for ordering and a system for allocating, and so on.
だから、発注のシステムとバッチのシステムを考えるのではなく、発注のシステムと配分のシステムを考える、といった具合に.

When we separate things this way, it’s a little easier to see which system should be responsible for what.
このように物事を分けて考えると、どのシステムが何に責任を持つべきかが、少しわかりやすくなる.
When thinking about ordering, really we want to make sure that when we place an order, the order is placed.
注文について考えるとき、私たちが本当にしたいのは、注文をしたときに、その注文が行われるようにする事である.
Everything else can happen later, so long as it happens.
それ以外のことは後回しでいいのである.

- NOTE 注
  - If this sounds familiar, it should! Segregating responsibilities is the same process we went through when designing our aggregates and commands. もしこれが聞き覚えのあるものであれば、その通りである. 責任の分担(Segregating responsibilities)は、Aggregateとcommandを設計するときに行ったのと同じプロセスである.

Like aggregates, microservices should be consistency boundaries.
Aggregateのように、**マイクロサービスもconsistency boundary(一貫性の境界)であるべき**だ.
Between two services, we can accept eventual consistency, and that means we don’t need to rely on synchronous calls.
2つのサービスの間では、最終的な一貫性を受け入れることができ、それは同期呼び出しに依存する必要がないことを意味する.
Each service accepts commands from the outside world and raises events to record the result.
各サービスは外界からのcommandを受け付け、その結果を記録するためにeventを発生させる.
Other services can listen to those events to trigger the next steps in the workflow.
他のサービスは、それらのeventをlistenして、ワークフローの次のステップをトリガーすることができる.

To avoid the Distributed Ball of Mud anti-pattern, instead of temporally coupled HTTP API calls, we want to use asynchronous messaging to integrate our systems.
Distributed Ball of Mud のアンチパターンを避けるために、時間的に結合された HTTP API コールの代わりに、**非同期メッセージング(asynchronous messaging=同期的でなくても受け渡せるmessage?)**を使用してシステムを統合したいと思う.
We want our `BatchQuantityChanged` messages to come in as external messages from upstream systems, and we want our system to publish `Allocated` events for downstream systems to listen to.
`BatchQuantityChanged`メッセージが上流のシステムからexternal messageとして送られてくるようにし、下流のシステムが listen できるように`Allocated` イベントを発行するようにしたいと思う.

Why is this better?
なぜこの方法が良いのでしょうか？
First, because things can fail independently, it’s easier to handle degraded behavior: we can still take orders if the allocation system is having a bad day.
まず、**独立して故障することができる**ので、劣化した動作に対応しやすくなる. 割り当てシステムの調子が悪くても、注文は受けられる.(=常に一緒に動いているような"同期的"な接続ではなく、非同期的な接続関係だから...!)

Second, we’re reducing the strength of coupling between our systems.
第二に、システム間の結合の強さを低減していること.
If we need to change the order of operations or to introduce new steps in the process, we can do that locally.
操作の順序を変えたり、新しいステップを導入したりする必要がある場合、ローカルでそれを行うことができる.

## Using a Redis Pub/Sub Channel for Integration Redis Pubを利用する

Let’s see how it will all work concretely.
では、具体的にどう動くか見てみよう.
We’ll need some way of getting events out of one system and into another, like our message bus, but for services.
メッセージバスのように、**あるシステムから別のシステムへ、しかしサービスのためにイベントを取得する方法**が必要.
This piece of infrastructure is often called a message broker.
このようなインフラは、しばしば **message broker** と呼ばれる.
The role of a message broker is to take messages from publishers and deliver them to subscribers.
message broker の役割は、publisher(=client? 上流のシステム?)からメッセージを受け取り、それをsubscriber(=下流のシステム?)に配信する事である.

At MADE.com, we use Event Store; Kafka or RabbitMQ are valid alternatives.
MADE.comでは、Event Storeを使用している. KafkaやRabbitMQは有効な代替手段である.(??)
A lightweight solution based on Redis pub
Redisパブをベースとした軽量なソリューション

- NOTE 注
  - We’re glossing over the complexity involved in choosing the right messaging platform. Concerns like message ordering, failure handling, and idempotency all need to be thought through. For a few pointers, see “Footguns”. 正しいmessaging platform(=message brokerの事??)の選択には、複雑さがつきまとう. メッセージの順序、障害処理、およびべき等といった懸念事項は、すべて考え抜かれる必要がある. いくつかのポインタについては、"Footguns "を参照してください.

Our new flow will look like Figure 11-6:
新しいフローは図 11-6 のようになる.
Redis provides the `BatchQuantityChanged` event that kicks off the whole process, and our Allocated event is published back out to Redis again at the end.
Redis は全体のプロセスを開始する `BatchQuantityChanged` イベントを提供し、割り当てられたイベントは最後に再び Redis に publish される.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1106.png)

## Test-Driving It All Using an End-to-End Test エンド・ツー・エンド・テストですべてを検証する

Here’s how we might start with an end-to-end test.
ここでは、エンドツーエンドのテストをどのように始めるかについて説明する.
We can use our existing API to create batches, and then we’ll test both inbound and outbound messages:
既存のAPIを使ってバッチを作成し、インバウンドとアウトバウンドの両方のメッセージをテストすることができる.

An end-to-end test for our pub/sub model (tests/e2e/test_external_events.py)

```python
def test_change_batch_quantity_leading_to_reallocation():
    # start with two batches and an order allocated to one of them  1
    orderid, sku = random_orderid(), random_sku()
    earlier_batch, later_batch = random_batchref('old'), random_batchref('newer')
    api_client.post_to_add_batch(earlier_batch, sku, qty=10, eta='2011-01-02') # 2
    api_client.post_to_add_batch(later_batch, sku, qty=10, eta='2011-01-02')
    response = api_client.post_to_allocate(orderid, sku, 10) # 2
    assert response.json()['batchref'] == earlier_batch

    subscription = redis_client.subscribe_to('line_allocated') #3

    # change quantity on allocated batch so it's less than our order  1
    redis_client.publish_message('change_batch_quantity', {  #3
        'batchref': earlier_batch, 'qty': 5
    })

    # wait until we see a message saying the order has been reallocated  1
    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):  4
        with attempt:
            message = subscription.get_message(timeout=1)
            if message:
                messages.append(message)
                print(messages)
            data = json.loads(messages[-1]['data'])
            assert data['orderid'] == orderid
            assert data['batchref'] == later_batch
```

1. You can read the story of what’s going on in this test from the comments: we want to send an event into the system that causes an order line to be reallocated, and we see that reallocation come out as an event in Redis too. このテストで何が起こっているかは、コメントから読み取ることができる. orderlineを再割り当てするイベントをシステムに送信したいのですが、その再割り当てがRedisでもイベントとして表示されるのがわかる.

2. `api_client` is a little helper that we refactored out to share between our two test types; it wraps our calls to `requests.post`. 2. `api_client` は小さなヘルパーで、2つのテストタイプで共有できるようにリファクタリングしたもので、 `requests.post` への呼び出しをラップしている.

3. `redis_client` is another little test helper, the details of which don’t really matter; its job is to be able to send and receive messages from various Redis channels. We’ll use a channel called `change_batch_quantity` to send in our request to change the quantity for a batch, and we’ll listen to another channel called `line_allocated` to look out for the expected reallocation. `redis_client`はもうひとつの小さなテストヘルパーで、その詳細はあまり重要ではない. このヘルパーの仕事は、さまざまな Redis チャンネルからメッセージを送受信できるようにすることである. ここでは`change_batch_quantity`という名前のチャンネルを使ってバッチの数量を変更するリクエストを送信し、`line_allocated` という名前のチャンネルで再割り当てが行われるのを待つ.

4. Because of the asynchronous nature of the system under test, we need to use the `tenacity` library again to add a retry loop—first, because it may take some time for our new `line_allocated` message to arrive, but also because it won’t be the only message on that channel. まず、新しい `line_allocated` メッセージが到着するまでに時間がかかるかもしれませんし、そのチャンネルにあるのはそのメッセージだけではないからである.

### Redis Is Another Thin Adapter Around Our Message Bus Redisはメッセージバスを囲むもう一つの薄いアダプターである

Our Redis pub
当社のRedisパブ

Simple Redis message listener (src/allocation/entrypoints/redis_eventconsumer.py)

```python
r = redis.Redis(**config.get_redis_host_and_port())


def main():
    orm.start_mappers()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('change_batch_quantity')  1

    for m in pubsub.listen():
        handle_change_batch_quantity(m)


def handle_change_batch_quantity(m):
    logging.debug('handling %s', m)
    data = json.loads(m['data'])  2
    cmd = commands.ChangeBatchQuantity(ref=data['batchref'], qty=data['qty'])  2
    messagebus.handle(cmd, uow=unit_of_work.SqlAlchemyUnitOfWork())
```

1. `main()` subscribes us to the `change_batch_quantity` channel on load. 1. `main()` はロード時に `change_batch_quantity` チャンネルにサブスクライブする.

2. Our main job as an entrypoint to the system is to deserialize JSON, convert it to a `Command`, and pass it to the service layer—much as the Flask adapter does. **システムのentrypointとしての我々の主な仕事**は、**JSON をデシリアライズして `Command` に変換**し、Flask アダプタが行うのと同じように Service Layer に渡すことである.

We also build a new downstream adapter to do the opposite job—converting domain events to public events:
また、Domain event(?)を public event(?)に変換する、逆の作業を行うダウンストリームアダプタも新たに構築します。

Simple Redis message publisher (src/allocation/adapters/redis_eventpublisher.py)

```python
r = redis.Redis(**config.get_redis_host_and_port())


def publish(channel, event: events.Event):  1
    logging.debug('publishing: channel=%s, event=%s', channel, event)
    r.publish(channel, json.dumps(asdict(event)))
```

1. We take a hardcoded channel here, but you could also store a mapping between event classes/names and the appropriate channel, allowing one or more message types to go to different channels. ここではハードコードされたチャンネルを使用していますが、イベントクラス間のマッピングを保存することもできる.(??)

### Our New Outgoing Event 新発売のイベント

Here’s what the `Allocated` event will look like:
以下は、`Allocated`イベントの様子.

New event (src
新規イベント（src

```python
@dataclass
class Allocated(Event):
    orderid: str
    sku: str
    qty: int
    batchref: str
```

It captures everything we need to know about an allocation: the details of the order line, and which batch it was allocated to.
これは、オーダーラインの詳細や、どのバッチに割り当てられたかなど、割り当てに関する必要な情報をすべて把握することができる.

We add it into our model’s `allocate()` method (having added a test first, naturally):
これをモデルの `allocate()` メソッドに追加する. (当然ながら、最初にテストを追加している).

Product.allocate() emits new event to record what happened (src/allocation/domain/model.py)
`Product.allocate()` は、何が起こったかを記録するために新しいイベントを発行します (src)

```python
class Product:
    ...
    def allocate(self, line: OrderLine) -> str:
        ...

            batch.allocate(line)
            self.version_number += 1
            self.events.append(events.Allocated(
                orderid=line.orderid, sku=line.sku, qty=line.qty,
                batchref=batch.reference,
            ))
            return batch.reference
```

The handler for `ChangeBatchQuantity` already exists, so all we need to add is a handler that publishes the outgoing event:
`ChangeBatchQuantity` のhandlerはすでに存在しているので、追加する必要があるのはoutgoingするeventをpublishするhandlerだけである.

The message bus grows (src/allocation/service_layer/messagebus.py)

```python
HANDLERS = {
    events.Allocated: [handlers.publish_allocated_event],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
```

Publishing the event uses our helper function from the Redis wrapper:
eventの発行には、Redis wrapperのhelper functionが使用される.

Publish to Redis (src/allocation/service_layer/handlers.py)

```python
def publish_allocated_event(
        event: events.Allocated, uow: unit_of_work.AbstractUnitOfWork,
):
    redis_eventpublisher.publish('line_allocated', event)
```

## Internal Versus External Events. Internal Events と External Events

It’s a good idea to keep the distinction between internal and external events clear.
**Internal EventとExternal Eventの区別**を明確にしておくとよいだろう.
Some events may come from the outside, and some events may get upgraded and published externally, but not all of them will.
あるEventは外部からやってくるかもしれないし、あるイベントはアップグレードされて外部でpublishedされるかもしれないが、すべてがそうなるわけではない.
This is particularly important if you get into event sourcing (very much a topic for another book, though).
これは、**event sourcing**(=Eventをどこから受け取るかの話??)に取り掛かる場合、特に重要である.

- TIP ヒント

  - Outbound events are one of the places it’s important to apply validation. See Appendix E for some validation philosophy and examples. Outbound events(?)は、バリデーションを適用することが重要な場所の一つである. 検証の考え方や例については、付録Eを参照されたい.

- EXERCISE FOR THE READER 読書運動
- A nice simple one for this chapter: make it so that the main `allocate()` use case can also be invoked by an event on a Redis channel, as well as (or instead of) via the API. この章ではシンプルなものを紹介します。メインの `allocate()` usecase(=ユースケースはpublicメソッド的な意味合い?)を、**API経由だけでなく、Redisチャネルのイベントでも呼び出せるよう**にしたい (あるいはAPI経由の代わりに).
- You will likely want to add a new E2E test and feed through some changes into `redis_eventconsumer.py`. 新しいE2Eテストを追加して、いくつかの変更を `redis_eventconsumer.py` に反映させたいと思うことだろう.

## Wrap-Up まとめ

Events can come from the outside, but they can also be published externally—our `publish` handler converts an event to a message on a Redis channel.
**イベントは外部からやってくるものですが、外部へ公開(publish)することもできる**(まだあんまり意味をわかってない..., GUIにレスポンスを返す的なイメージだろうか...? ).`publish`ハンドラはイベントをRedisチャンネル上のメッセージに変換する.
We use events to talk to the outside world.
私たちは**eventを利用して外の世界と会話**(=Connascence of Nameだっけ...!!)している.
This kind of temporal decoupling buys us a lot of flexibility in our application integrations, but as always, it comes at a cost.
このような**temporal decoupling**(?)は、アプリケーションの統合に多くの柔軟性をもたらしますが、いつものように、それにはコストがかかる.

> Event notification is nice because it implies a low level of coupling, and is pretty simple to set up.
> **Event notificationは、低レベルの結合を意味し(=(=Connascence of Nameだから?)**、セットアップが非常に簡単であるため、素晴らしいものである.
> It can become problematic, however, if there really is a logical flow that runs over various event notifications...It can be hard to see such a flow as it’s not explicit in any program text....This can make it hard to debug and modify.
> しかし、様々なイベント通知の上に流れる論理的な流れが本当にある場合、問題になることがある...プログラムのテキストに明示されていないので、そのような流れを見るのは難しい...これは、デバッグや修正を困難にすることがある。
> --Martin Fowler, “What do you mean by ‘Event-Driven’”

Table 11-1 shows some trade-offs to think about.
表11-1に、考えるべきトレードオフをいくつか示す.

Table 11-1.
表11-1.
Event-based microservices integration: the trade-offs
イベントベースのマイクロサービス統合：トレードオフの関係

- Pros 長所
- Avoids the distributed big ball of mud. 配布された大きな泥の玉を避けることができる.
- Services are decoupled: it’s easier to change individual services and add new ones **サービスのdecoupling**：個々のサービスの変更や新しいサービスの追加が容易になる.
- Cons 短所
  - The overall flows of information are harder to see. 全体的な情報の流れは見えにくくなっている.(サービス間ではNameのみを使って会話するから??)
  - Eventual consistency is a new concept to deal with. 最終的な整合性(Eventual consistency)は、新しい概念として扱われる.
  - Message reliability and choices around at-least-once versus at-most-once delivery need thinking through. メッセージの信頼性や、at-least-onceとat-most-onceの選択について、よく考える必要がある.

More generally, if you’re moving from a model of synchronous messaging to an async one, you also open up a whole host of problems having to do with message reliability and eventual consistency.
より一般的には、**synchronous(同期的な) messagingのモデルからasync(非同期的な) messagingに移行する**(i.e. サービス同士をより疎な結合にする? その為に Connasance of Name の状態にする?)場合、メッセージの信頼性と最終的な一貫性(eventual consistency)に関連する問題のホスト全体を開くことにもなる.
Read on to “Footguns”.
フットガンズ」までお読みください。
