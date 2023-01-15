# chapter 11. Event-Driven Architecture: Using Events To Integrate Microservices

In the preceding chapter, we never actually spoke about how we would receive the “batch quantity changed” events, or indeed, how we might notify the outside world about reallocations.

We have a microservice with a web API, but what about other ways of talking to other systems? How will we know if, say, a shipment is delayed or the quantity is amended? How will we tell the warehouse system that an order has been allocated and needs to be sent to a customer?

In this chapter, we’d like to show how the events metaphor can be extended to encompass the way that we handle incoming and outgoing messages from the system. Internally, the core of our application is now a message processor. Let’s follow through on that so it becomes a message processor externally as well. As shown in Figure 11-1, our application will receive events from external sources via an external message bus (we’ll use Redis pub/sub queues as an example) and publish its outputs, in the form of events, back there as well.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1101.png)

- TIP
- The code for this chapter is in the chapter_11_external_events branch on GitHub:

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_11_external_events
# or to code along, checkout the previous chapter:
git checkout chapter_10_commands
```

## Distributed Ball of Mud, and Thinking in Nouns

Before we get into that, let’s talk about the alternatives. We regularly talk to engineers who are trying to build out a microservices architecture. Often they are migrating from an existing application, and their first instinct is to split their system into nouns.

What nouns have we introduced so far in our system? Well, we have batches of stock, orders, products, and customers. So a naive attempt at breaking up the system might have looked like Figure 11-2 (notice that we’ve named our system after a noun, Batches, instead of Allocation).

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1102.png)

Each “thing” in our system has an associated service, which exposes an HTTP API.

Let’s work through an example happy-path flow in Figure 11-3: our users visit a website and can choose from products that are in stock. When they add an item to their basket, we will reserve some stock for them. When an order is complete, we confirm the reservation, which causes us to send dispatch instructions to the warehouse. Let’s also say, if this is the customer’s third order, we want to update the customer record to flag them as a VIP.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1103.png)

We can think of each of these steps as a command in our system: `ReserveStock`, `ConfirmReservation`, `DispatchGoods`, `MakeCustomerVIP`, and so forth.

This style of architecture, where we create a microservice per database table and treat our HTTP APIs as CRUD interfaces to anemic models, is the most common initial way for people to approach service-oriented design.

This works fine for systems that are very simple, but it can quickly degrade into a distributed ball of mud.

To see why, let’s consider another case. Sometimes, when stock arrives at the warehouse, we discover that items have been water damaged during transit. We can’t sell water-damaged sofas, so we have to throw them away and request more stock from our partners. We also need to update our stock model, and that might mean we need to reallocate a customer’s order.

Where does this logic go?

Well, the Warehouse system knows that the stock has been damaged, so maybe it should own this process, as shown in Figure 11-4.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1104.png)

This sort of works too, but now our dependency graph is a mess. To allocate stock, the Orders service drives the Batches system, which drives Warehouse; but in order to handle problems at the warehouse, our Warehouse system drives Batches, which drives Orders.

Multiply this by all the other workflows we need to provide, and you can see how services quickly get tangled up.

## Error Handling in Distributed Systems

“Things break” is a universal law of software engineering. What happens in our system when one of our requests fails? Let’s say that a network error happens right after we take a user’s order for three `MISBEGOTTEN-RUG`, as shown in Figure 11-5.

We have two options here: we can place the order anyway and leave it unallocated, or we can refuse to take the order because the allocation can’t be guaranteed. The failure state of our batches service has bubbled up and is affecting the reliability of our order service.

When two things have to be changed together, we say that they are coupled. We can think of this failure cascade as a kind of temporal coupling: every part of the system has to work at the same time for any part of it to work. As the system gets bigger, there is an exponentially increasing probability that some part is degraded.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1105.png)

- CONNASCENCE
- We’re using the term coupling here, but there’s another way to describe the relationships between our systems. Connascence is a term used by some authors to describe the different types of coupling.
- Connascence isn’t bad, but some types of connascence are stronger than others. We want to have strong connascence locally, as when two classes are closely related, but weak connascence at a distance.
- In our first example of a distributed ball of mud, we see Connascence of Execution: multiple components need to know the correct order of work for an operation to be successful.
- When thinking about error conditions here, we’re talking about Connascence of Timing: multiple things have to happen, one after another, for the operation to work.
- When we replace our RPC-style system with events, we replace both of these types of connascence with a weaker type. That’s Connascence of Name: multiple components need to agree only on the name of an event and the names of fields it carries.
- We can never completely avoid coupling, except by having our software not talk to any other software. What we want is to avoid inappropriate coupling. Connascence provides a mental model for understanding the strength and type of coupling inherent in different architectural styles. Read all about it at connascence.io.

## The Alternative: Temporal Decoupling Using Asynchronous Messaging

How do we get appropriate coupling? We’ve already seen part of the answer, which is that we should think in terms of verbs, not nouns. Our domain model is about modeling a business process. It’s not a static data model about a thing; it’s a model of a verb.

So instead of thinking about a system for orders and a system for batches, we think about a system for ordering and a system for allocating, and so on.

When we separate things this way, it’s a little easier to see which system should be responsible for what. When thinking about ordering, really we want to make sure that when we place an order, the order is placed. Everything else can happen later, so long as it happens.

- NOTE
- If this sounds familiar, it should! Segregating responsibilities is the same process we went through when designing our aggregates and commands.

Like aggregates, microservices should be consistency boundaries. Between two services, we can accept eventual consistency, and that means we don’t need to rely on synchronous calls. Each service accepts commands from the outside world and raises events to record the result. Other services can listen to those events to trigger the next steps in the workflow.

To avoid the Distributed Ball of Mud anti-pattern, instead of temporally coupled HTTP API calls, we want to use asynchronous messaging to integrate our systems. We want our `BatchQuantityChanged` messages to come in as external messages from upstream systems, and we want our system to publish `Allocated` events for downstream systems to listen to.

Why is this better? First, because things can fail independently, it’s easier to handle degraded behavior: we can still take orders if the allocation system is having a bad day.

Second, we’re reducing the strength of coupling between our systems. If we need to change the order of operations or to introduce new steps in the process, we can do that locally.

## Using a Redis Pub/Sub Channel for Integration

Let’s see how it will all work concretely. We’ll need some way of getting events out of one system and into another, like our message bus, but for services. This piece of infrastructure is often called a message broker. The role of a message broker is to take messages from publishers and deliver them to subscribers.

At MADE.com, we use Event Store; Kafka or RabbitMQ are valid alternatives. A lightweight solution based on Redis pub/sub channels can also work just fine, and because Redis is much more generally familiar to people, we thought we’d use it for this book.

- NOTE
- We’re glossing over the complexity involved in choosing the right messaging platform. Concerns like message ordering, failure handling, and idempotency all need to be thought through. For a few pointers, see “Footguns”.

Our new flow will look like Figure 11-6: Redis provides the `BatchQuantityChanged` event that kicks off the whole process, and our Allocated event is published back out to Redis again at the end.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1106.png)

## Test-Driving It All Using an End-to-End Test

Here’s how we might start with an end-to-end test. We can use our existing API to create batches, and then we’ll test both inbound and outbound messages:

An end-to-end test for our pub/sub model (tests/e2e/test_external_events.py)

```python
def test_change_batch_quantity_leading_to_reallocation():
    # start with two batches and an order allocated to one of them  1
    orderid, sku = random_orderid(), random_sku()
    earlier_batch, later_batch = random_batchref('old'), random_batchref('newer')
    api_client.post_to_add_batch(earlier_batch, sku, qty=10, eta='2011-01-02')  2
    api_client.post_to_add_batch(later_batch, sku, qty=10, eta='2011-01-02')
    response = api_client.post_to_allocate(orderid, sku, 10)  2
    assert response.json()['batchref'] == earlier_batch

    subscription = redis_client.subscribe_to('line_allocated')  3

    # change quantity on allocated batch so it's less than our order  1
    redis_client.publish_message('change_batch_quantity', {  3
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

1. You can read the story of what’s going on in this test from the comments: we want to send an event into the system that causes an order line to be reallocated, and we see that reallocation come out as an event in Redis too.

2. `api_client` is a little helper that we refactored out to share between our two test types; it wraps our calls to `requests.post`.

3. `redis_client` is another little test helper, the details of which don’t really matter; its job is to be able to send and receive messages from various Redis channels. We’ll use a channel called `change_batch_quantity` to send in our request to change the quantity for a batch, and we’ll listen to another channel called `line_allocated` to look out for the expected reallocation.

4. Because of the asynchronous nature of the system under test, we need to use the `tenacity` library again to add a retry loop—first, because it may take some time for our new `line_allocated` message to arrive, but also because it won’t be the only message on that channel.

### Redis Is Another Thin Adapter Around Our Message Bus

Our Redis pub/sub listener (we call it an event consumer) is very much like Flask: it translates from the outside world to our events:

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

1. `main()` subscribes us to the `change_batch_quantity` channel on load.

2. Our main job as an entrypoint to the system is to deserialize JSON, convert it to a `Command`, and pass it to the service layer—much as the Flask adapter does.

We also build a new downstream adapter to do the opposite job—converting domain events to public events:

Simple Redis message publisher (src/allocation/adapters/redis_eventpublisher.py)

```python
r = redis.Redis(**config.get_redis_host_and_port())


def publish(channel, event: events.Event):  1
    logging.debug('publishing: channel=%s, event=%s', channel, event)
    r.publish(channel, json.dumps(asdict(event)))
```

1. We take a hardcoded channel here, but you could also store a mapping between event classes/names and the appropriate channel, allowing one or more message types to go to different channels.

### Our New Outgoing Event

Here’s what the `Allocated` event will look like:

New event (src/allocation/domain/events.py)

```python
@dataclass
class Allocated(Event):
    orderid: str
    sku: str
    qty: int
    batchref: str
```

It captures everything we need to know about an allocation: the details of the order line, and which batch it was allocated to.

We add it into our model’s `allocate()` method (having added a test first, naturally):

Product.allocate() emits new event to record what happened (src/allocation/domain/model.py)

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

The message bus grows (src/allocation/service_layer/messagebus.py)

```python
HANDLERS = {
    events.Allocated: [handlers.publish_allocated_event],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
```

Publishing the event uses our helper function from the Redis wrapper:

Publish to Redis (src/allocation/service_layer/handlers.py)

```python
def publish_allocated_event(
        event: events.Allocated, uow: unit_of_work.AbstractUnitOfWork,
):
    redis_eventpublisher.publish('line_allocated', event)
```

## Internal Versus External Events

It’s a good idea to keep the distinction between internal and external events clear. Some events may come from the outside, and some events may get upgraded and published externally, but not all of them will. This is particularly important if you get into event sourcing (very much a topic for another book, though).

- TIP
- Outbound events are one of the places it’s important to apply validation. See Appendix E for some validation philosophy and examples.

- EXERCISE FOR THE READER
- A nice simple one for this chapter: make it so that the main `allocate()` use case can also be invoked by an event on a Redis channel, as well as (or instead of) via the API.
- You will likely want to add a new E2E test and feed through some changes into `redis_eventconsumer.py`.

## Wrap-Up

Events can come from the outside, but they can also be published externally—our `publish` handler converts an event to a message on a Redis channel. We use events to talk to the outside world. This kind of temporal decoupling buys us a lot of flexibility in our application integrations, but as always, it comes at a cost.

> Event notification is nice because it implies a low level of coupling, and is pretty simple to set up. It can become problematic, however, if there really is a logical flow that runs over various event notifications...It can be hard to see such a flow as it’s not explicit in any program text....This can make it hard to debug and modify. --Martin Fowler, “What do you mean by ‘Event-Driven’”

Table 11-1 shows some trade-offs to think about.

Table 11-1. Event-based microservices integration: the trade-offs

- Pros
  - Avoids the distributed big ball of mud.
  - Services are decoupled: it’s easier to change individual services and add new ones
- Cons
  - The overall flows of information are harder to see.
  - Eventual consistency is a new concept to deal with.
  - Message reliability and choices around at-least-once versus at-most-once delivery need thinking through.

More generally, if you’re moving from a model of synchronous messaging to an async one, you also open up a whole host of problems having to do with message reliability and eventual consistency. Read on to “Footguns”.
