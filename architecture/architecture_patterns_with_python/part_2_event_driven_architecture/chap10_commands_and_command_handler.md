# Chapter 10. Commands and Command Handler

In the previous chapter, we talked about using events as a way of representing the inputs to our system, and we turned our application into a message-processing machine.

To achieve that, we converted all our use-case functions to event handlers. When the API receives a POST to create a new batch, it builds a new BatchCreated event and handles it as if it were an internal event. This might feel counterintuitive. After all, the batch hasn’t been created yet; that’s why we called the API. We’re going to fix that conceptual wart by introducing commands and showing how they can be handled by the same message bus but with slightly different rules.

===================

TIP

The code for this chapter is in the chapter_10_commands branch on GitHub:

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_10_commands
# or to code along, checkout the previous chapter:
git checkout chapter_09_all_messagebus
```

## Commands and Events

Like events, commands are a type of message—instructions sent by one part of a system to another. We usually represent commands with dumb data structures and can handle them in much the same way as events.

The differences between commands and events, though, are important.

Commands are sent by one actor to another specific actor with the expectation that a particular thing will happen as a result. When we post a form to an API handler, we are sending a command. We name commands with imperative mood verb phrases like “allocate stock” or “delay shipment.”

Commands capture intent. They express our wish for the system to do something. As a result, when they fail, the sender needs to receive error information.

Events are broadcast by an actor to all interested listeners. When we publish `BatchQuantityChanged`, we don’t know who’s going to pick it up. We name events with past-tense verb phrases like “order allocated to stock” or “shipment delayed.”

We often use events to spread the knowledge about successful commands.

Events capture facts about things that happened in the past. Since we don’t know who’s handling an event, senders should not care whether the receivers succeeded or failed. Table 10-1 recaps the differences.

Table 10-1. Events versus commands

|                | Event              | Command         |
| -------------- | ------------------ | --------------- |
| Named          | Past tense         | Imperative mood |
|                |                    |                 |
| Error handling | Fail independently | Fail noisily    |
|                |                    |                 |
| Sent to        | All listeners      | One recipient   |

What kinds of commands do we have in our system right now?

Pulling out some commands (src/allocation/domain/commands.py)

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

1. `commands.Allocate` will replace `events.AllocationRequired`.

2. `commands.CreateBatch` will replace `events.BatchCreated`.

3. `commands.ChangeBatchQuantity` will replace `events.BatchQuantityChanged`.

## Differences in Exception Handling

Just changing the names and verbs is all very well, but that won’t change the behavior of our system. We want to treat events and commands similarly, but not exactly the same. Let’s see how our message bus changes:

Dispatch events and commands differently (src/allocation/service_layer/messagebus.py)

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

1. It still has a main `handle()` entrypoint that takes a `message`, which may be a command or an event.

2. We dispatch events and commands to two different helper functions, shown next.

Here’s how we handle events:

Events cannot interrupt the flow (src/allocation/service_layer/messagebus.py)

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

1. Events go to a dispatcher that can delegate to multiple handlers per event.

2. It catches and logs errors but doesn’t let them interrupt message processing.

And here’s how we do commands:

Commands reraise exceptions (src/allocation/service_layer/messagebus.py)

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

1. The command dispatcher expects just one handler per command.

2. If any errors are raised, they fail fast and will bubble up.

3. `return result` is only temporary; as mentioned in “A Temporary Ugly Hack: The Message Bus Has to Return Results”, it’s a temporary hack to allow the message bus to return the batch reference for the API to use. We’ll fix this in Chapter 12.

We also change the single `HANDLERS` dict into different ones for commands and events. Commands can have only one handler, according to our convention:

New handlers dicts (src/allocation/service_layer/messagebus.py)

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

## Discussion: Events, Commands, and Error Handling

Many developers get uncomfortable at this point and ask, “What happens when an event fails to process? How am I supposed to make sure the system is in a consistent state?” If we manage to process half of the events during `messagebus.handle` before an out-of-memory error kills our process, how do we mitigate problems caused by the lost messages?

Let’s start with the worst case: we fail to handle an event, and the system is left in an inconsistent state. What kind of error would cause this? Often in our systems we can end up in an inconsistent state when only half an operation is completed.

For example, we could allocate three units of `DESIRABLE_BEANBAG` to a customer’s order but somehow fail to reduce the amount of remaining stock. This would cause an inconsistent state: the three units of stock are both allocated and available, depending on how you look at it. Later, we might allocate those same beanbags to another customer, causing a headache for customer support.

In our allocation service, though, we’ve already taken steps to prevent that happening. We’ve carefully identified aggregates that act as consistency boundaries, and we’ve introduced a UoW that manages the atomic success or failure of an update to an aggregate.

For example, when we allocate stock to an order, our consistency boundary is the `Product` aggregate. This means that we can’t accidentally overallocate: either a particular order line is allocated to the product, or it is not—there’s no room for inconsistent states.

By definition, we don’t require two aggregates to be immediately consistent, so if we fail to process an event and update only a single aggregate, our system can still be made eventually consistent. We shouldn’t violate any constraints of the system.

With this example in mind, we can better understand the reason for splitting messages into commands and events. When a user wants to make the system do something, we represent their request as a command. That command should modify a single aggregate and either succeed or fail in totality. Any other bookkeeping, cleanup, and notification we need to do can happen via an event. We don’t require the event handlers to succeed in order for the command to be successful.

Let’s look at another example (from a different, imaginary projet) to see why not.

Imagine we are building an ecommerce website that sells expensive luxury goods. Our marketing department wants to reward customers for repeat visits. We will flag customers as VIPs after they make their third purchase, and this will entitle them to priority treatment and special offers. Our acceptance criteria for this story reads as follows:

```
Given a customer with two orders in their history,
When the customer places a third order,
Then they should be flagged as a VIP.

When a customer first becomes a VIP
Then we should send them an email to congratulate them
```

Using the techniques we’ve already discussed in this book, we decide that we want to build a new `History` aggregate that records orders and can raise domain events when rules are met. We will structure the code like this:

VIP customer (example code for a different project)

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

1. The `History` aggregate captures the rules indicating when a customer becomes a VIP. This puts us in a good place to handle changes when the rules become more complex in the future.

2. Our first handler creates an order for the customer and raises a domain event `OrderCreated`.

3. Our second handler updates the `History` object to record that an order was created.

4. Finally, we send an email to the customer when they become a VIP.

Using this code, we can gain some intuition about error handling in an event-driven system.

In our current implementation, we raise events about an aggregate after we persist our state to the database. What if we raised those events before we persisted, and committed all our changes at the same time? That way, we could be sure that all the work was complete. Wouldn’t that be safer?

What happens, though, if the email server is slightly overloaded? If all the work has to complete at the same time, a busy email server can stop us from taking money for orders.

What happens if there is a bug in the implementation of the `History` aggregate? Should we fail to take your money just because we can’t recognize you as a VIP?

By separating out these concerns, we have made it possible for things to fail in isolation, which improves the overall reliability of the system. The only part of this code that has to complete is the command handler that creates an order. This is the only part that a customer cares about, and it’s the part that our business stakeholders should prioritize.

Notice how we’ve deliberately aligned our transactional boundaries to the start and end of the business processes. The names that we use in the code match the jargon used by our business stakeholders, and the handlers we’ve written match the steps of our natural language acceptance criteria. This concordance of names and structure helps us to reason about our systems as they grow larger and more complex.

## Recovering from Errors Synchronously

Hopefully we’ve convinced you that it’s OK for events to fail independently from the commands that raised them. What should we do, then, to make sure we can recover from errors when they inevitably occur?

The first thing we need is to know when an error has occurred, and for that we usually rely on logs.

Let’s look again at the `handle_event` method from our message bus:

Current handle function (src/allocation/service_layer/messagebus.py)

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

When we handle a message in our system, the first thing we do is write a log line to record what we’re about to do. For our `CustomerBecameVIP` use case, the logs might read as follows:

```
Handling event CustomerBecameVIP(customer_id=12345)
with handler <function congratulate_vip_customer at 0x10ebc9a60>
```

Because we’ve chosen to use dataclasses for our message types, we get a neatly printed summary of the incoming data that we can copy and paste into a Python shell to re-create the object.

When an error occurs, we can use the logged data to either reproduce the problem in a unit test or replay the message into the system.

Manual replay works well for cases where we need to fix a bug before we can re-process an event, but our systems will always experience some background level of transient failure. This includes things like network hiccups, table deadlocks, and brief downtime caused by deployments.

For most of those cases, we can recover elegantly by trying again. As the proverb says, “If at first you don’t succeed, retry the operation with an exponentially increasing back-off period.”

Handle with retry (src/allocation/service_layer/messagebus.py)

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

1. Tenacity is a Python library that implements common patterns for retrying.

2. Here we configure our message bus to retry operations up to three times, with an exponentially increasing wait between attempts.

Retrying operations that might fail is probably the single best way to improve the resilience of our software. Again, the Unit of Work and Command Handler patterns mean that each attempt starts from a consistent state and won’t leave things half-finished.

- WARNING
- At some point, regardless of `tenacity`, we’ll have to give up trying to process the message. Building reliable systems with distributed messages is hard, and we have to skim over some tricky bits. There are pointers to more reference materials in the epilogue.

## Wrap-Up

In this book we decided to introduce the concept of events before the concept of commands, but other guides often do it the other way around. Making explicit the requests that our system can respond to by giving them a name and their own data structure is quite a fundamental thing to do. You’ll sometimes see people use the name Command Handler pattern to describe what we’re doing with Events, Commands, and Message Bus.

Table 10-2 discusses some of the things you should think about before you jump on board.

- Pros
  - Treating commands and events differently helps us understand which things have to succeed and which things we can tidy up later.
  - `CreateBatch` is definitely a less confusing name than `BatchCreated`. We are being explicit about the intent of our users, and explicit is better than implicit, right?
- Cons
  - The semantic differences between commands and events can be subtle. Expect bikeshedding arguments over the differences.
  - We’re expressly inviting failure. We know that sometimes things will break, and we’re choosing to handle that by making the failures smaller and more isolated. This can make the system harder to reason about and requires better monitoring.

In Chapter 11 we’ll talk about using events as an integration pattern.
