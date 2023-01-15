# Chapter 8. Events and the Message Bus

So far we’ve spent a lot of time and energy on a simple problem that we could easily have solved with Django. You might be asking if the increased testability and expressiveness are really worth all the effort.

In practice, though, we find that it’s not the obvious features that make a mess of our codebases: it’s the goop around the edge. It’s reporting, and permissions, and workflows that touch a zillion objects.

Our example will be a typical notification requirement: when we can’t allocate an order because we’re out of stock, we should alert the buying team. They’ll go and fix the problem by buying more stock, and all will be well.

For a first version, our product owner says we can just send the alert by email.

Let’s see how our architecture holds up when we need to plug in some of the mundane stuff that makes up so much of our systems.

We’ll start by doing the simplest, most expeditious thing, and talk about why it’s exactly this kind of decision that leads us to the Big Ball of Mud.

Then we’ll show how to use the Domain Events pattern to separate side effects from our use cases, and how to use a simple Message Bus pattern for triggering behavior based on those events. We’ll show a few options for creating those events and how to pass them to the message bus, and finally we’ll show how the Unit of Work pattern can be modified to connect the two together elegantly, as previewed in Figure 8-1.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0801.png)

TIP
The code for this chapter is in the chapter_08_events_and_message_bus branch on GitHub:

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_08_events_and_message_bus
# or to code along, checkout the previous chapter:
git checkout chapter_07_aggregate
```

## Avoiding Making a Mess

So. Email alerts when we run out of stock. When we have new requirements like ones that really have nothing to do with the core domain, it’s all too easy to start dumping these things into our web controllers.

### First, Let’s Avoid Making a Mess of Our Web Controllers

As a one-off hack, this might be OK:

Just whack it in the endpoint—what could go wrong? (src/allocation/entrypoints/flask_app.py)

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

…but it’s easy to see how we can quickly end up in a mess by patching things up like this. Sending email isn’t the job of our HTTP layer, and we’d like to be able to unit test this new feature.

### And Let’s Not Make a Mess of Our Model Either

Assuming we don’t want to put this code into our web controllers, because we want them to be as thin as possible, we may look at putting it right at the source, in the model:

Email-sending code in our model isn’t lovely either (src/allocation/domain/model.py)

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

But that’s even worse! We don’t want our model to have any dependencies on infrastructure concerns like `email.send_mail`.

This email-sending thing is unwelcome goop messing up the nice clean flow of our system. What we’d like is to keep our domain model focused on the rule “You can’t allocate more stuff than is actually available.”

The domain model’s job is to know that we’re out of stock, but the responsibility of sending an alert belongs elsewhere. We should be able to turn this feature on or off, or to switch to SMS notifications instead, without needing to change the rules of our domain model.

### Or the Service Layer!

The requirement “Try to allocate some stock, and send an email if it fails” is an example of workflow orchestration: it’s a set of steps that the system has to follow to achieve a goal.

We’ve written a service layer to manage orchestration for us, but even here the feature feels out of place:

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
            email.send_mail('stock@made.com', f'Out of stock for {line.sku}')
            raise
```

Catching an exception and reraising it? It could be worse, but it’s definitely making us unhappy. Why is it so hard to find a suitable home for this code?

## Single Responsibility Principle

Really, this is a violation of the single responsibility principle (SRP).1 Our use case is allocation. Our endpoint, service function, and domain methods are all called `allocate`, not `allocate_and_send_mail_if_out_of_stock`.

- TIP
- Rule of thumb: if you can’t describe what your function does without using words like “then” or “and,” you might be violating the SRP.

One formulation of the SRP is that each class should have only a single reason to change. When we switch from email to SMS, we shouldn’t have to update our `allocate()` function, because that’s clearly a separate responsibility.

To solve the problem, we’re going to split the orchestration into separate steps so that the different concerns don’t get tangled up.2 The domain model’s job is to know that we’re out of stock, but the responsibility of sending an alert belongs elsewhere. We should be able to turn this feature on or off, or to switch to SMS notifications instead, without needing to change the rules of our domain model.

We’d also like to keep the service layer free of implementation details. We want to apply the dependency inversion principle to notifications so that our service layer depends on an abstraction, in the same way as we avoid depending on the database by using a unit of work.

## All Aboard the Message Bus!

The patterns we’re going to introduce here are Domain Events and the Message Bus. We can implement them in a few ways, so we’ll show a couple before settling on the one we like most.

### The Model Records Events

First, rather than being concerned about emails, our model will be in charge of recording events—facts about things that have happened. We’ll use a message bus to respond to events and invoke a new operation.

### Events Are Simple Dataclasses

An event is a kind of value object. Events don’t have any behavior, because they’re pure data structures. We always name events in the language of the domain, and we think of them as part of our domain model.

We could store them in model.py, but we may as well keep them in their own file (this might be a good time to consider refactoring out a directory called domain so that we have domain/model.py and domain/events.py):

Event classes (src/allocation/domain/events.py)

```python
from dataclasses import dataclass

class Event:  1
    pass

@dataclass
class OutOfStock(Event):  2
    sku: str

```

1. Once we have a number of events, we’ll find it useful to have a parent class that can store common attributes. It’s also useful for type hints in our message bus, as you’ll see shortly.

2. `dataclasses` are great for domain events too.

### The Model Raises Events

When our domain model records a fact that happened, we say it raises an event.

Here’s what it will look like from the outside; if we ask `Product` to allocate but it can’t, it should raise an event:

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

1. Our aggregate will expose a new attribute called `.events` that will contain a list of facts about what has happened, in the form of `Event` objects.

Here’s what the model looks like on the inside:

The model raises a domain event (src/allocation/domain/model.py)

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

1. Here’s our new .events attribute in use.

2. Rather than invoking some email-sending code directly, we record those events at the place they occur, using only the language of the domain.

3. We’re also going to stop raising an exception for the out-of-stock case. The event will do the job the exception was doing.

- NOTE
- We’re actually addressing a code smell we had until now, which is that we were using exceptions for control flow. In general, if you’re implementing domain events, don’t raise exceptions to describe the same domain concept. As you’ll see later when we handle events in the Unit of Work pattern, it’s confusing to have to reason about events and exceptions together.

### The Message Bus Maps Events to Handlers

A message bus basically says, “When I see this event, I should invoke the following handler function.” In other words, it’s a simple publish-subscribe system. Handlers are subscribed to receive events, which we publish to the bus. It sounds harder than it is, and we usually implement it with a dict:

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

- NOTE
- Note that the message bus as implemented doesn’t give us concurrency because only one handler will run at a time. Our objective isn’t to support parallel threads but to separate tasks conceptually, and to keep each UoW as small as possible. This helps us to understand the codebase because the “recipe” for how to run each use case is written in a single place. See the following sidebar.

- IS THIS LIKE CELERY?
- Celery is a popular tool in the Python world for deferring self-contained chunks of work to an asynchronous task queue. The message bus we’re presenting here is very different, so the short answer to the above question is no; our message bus has more in common with a Node.js app, a UI event loop, or an actor framework.
- If you do have a requirement for moving work off the main thread, you can still use our event-based metaphors, but we suggest you use external events for that. There’s more discussion in Table 11-1, but essentially, if you implement a way of persisting events to a centralized store, you can subscribe other containers or other microservices to them. Then that same concept of using events to separate responsibilities across units of work within a single process/service can be extended across multiple processes—which may be different containers within the same service, or totally different microservices.
- If you follow us in this approach, your API for distributing tasks is your event classes—or a JSON representation of them. This allows you a lot of flexibility in who you distribute tasks to; they need not necessarily be Python services. Celery’s API for distributing tasks is essentially “function name plus arguments,” which is more restrictive, and Python-only.

## Option 1: The Service Layer Takes Events from the Model and Puts Them on the Message Bus

Our domain model raises events, and our message bus will call the right handlers whenever an event happens. Now all we need is to connect the two. We need something to catch events from the model and pass them to the message bus—the publishing step.

The simplest way to do this is by adding some code into our service layer:

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
            messagebus.handle(product.events)  2
```

1. We keep the try/finally from our ugly earlier implementation (we haven’t gotten rid of all exceptions yet, just OutOfStock).

2. But now, instead of depending directly on an email infrastructure, the service layer is just in charge of passing events from the model up to the message bus.

That already avoids some of the ugliness that we had in our naive implementation, and we have several systems that work like this one, in which the service layer explicitly collects events from aggregates and passes them to the message bus.

## Option 2: The Service Layer Raises Its Own Events

Another variant on this that we’ve used is to have the service layer in charge of creating and raising events directly, rather than having them raised by the domain model:

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

1. As before, we commit even if we fail to allocate because the code is simpler this way and it’s easier to reason about: we always commit unless something goes wrong. Committing when we haven’t changed anything is safe and keeps the code uncluttered.

Again, we have applications in production that implement the pattern in this way. What works for you will depend on the particular trade-offs you face, but we’d like to show you what we think is the most elegant solution, in which we put the unit of work in charge of collecting and raising events.

## Option 3: The UoW Publishes Events to the Message Bus

The UoW already has a `try/finally`, and it knows about all the aggregates currently in play because it provides access to the repository. So it’s a good place to spot events and pass them to the message bus:

The UoW meets the message bus (src/allocation/service_layer/unit_of_work.py)

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

1. We’ll change our commit method to require a private .\_commit() method from subclasses.

2. After committing, we run through all the objects that our repository has seen and pass their events to the message bus.

3. That relies on the repository keeping track of aggregates that have been loaded using a new attribute, .seen, as you’ll see in the next listing.

- NOTE
- Are you wondering what happens if one of the handlers fails? We’ll discuss error handling in detail in Chapter 10.

Repository tracks aggregates that pass through it (src/allocation/adapters/repository.py)

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

1. For the UoW to be able to publish new events, it needs to be able to ask the repository for which `Product` objects have been used during this session. We use a `set` called `.seen` to store them. That means our implementations need to call `super().__init__()`.

2. The parent `add()` method adds things to `.seen`, and now requires subclasses to implement `._add()`.

3. Similarly, `.get()` delegates to a `._get()` function, to be implemented by subclasses, in order to capture objects seen.

- NOTE
- The use of `._underscorey()` methods and subclassing is definitely not the only way you could implement these patterns. Have a go at the Exercise for the Reader in this chapter and experiment with some alternatives.

After the UoW and repository collaborate in this way to automatically keep track of live objects and process their events, the service layer can be totally free of event-handling concerns:

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

Service-layer fakes need tweaking (tests/unit/test_services.py)

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

- EXERCISE FOR THE READER
- Are you finding all those `._add()` and `._commit()` methods “super-gross,” in the words of our beloved tech reviewer Hynek? Does it “make you want to beat Harry around the head with a plushie snake”? Hey, our code listings are only meant to be examples, not the perfect solution! Why not go see if you can do better?

One composition over inheritance way to go would be to implement a wrapper class:

A wrapper adds functionality and then delegates (src/adapters/repository.py)

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

1. By wrapping the repository, we can call the actual `.add()` and `.get()` methods, avoiding weird underscorey methods.

- See if you can apply a similar pattern to our UoW class in order to get rid of those Java-y `_commit()` methods too. You can find the code on GitHub.

- Switching all the ABCs to `typing.Protocol` is a good way to force yourself to avoid using inheritance. Let us know if you come up with something nice!

You might be starting to worry that maintaining these fakes is going to be a maintenance burden. There’s no doubt that it is work, but in our experience it’s not a lot of work. Once your project is up and running, the interface for your repository and UoW abstractions really don’t change much. And if you’re using ABCs, they’ll help remind you when things get out of sync.

## Wrap-Up

Domain events give us a way to handle workflows in our system. We often find, listening to our domain experts, that they express requirements in a causal or temporal way—for example, “When we try to allocate stock but there’s none available, then we should send an email to the buying team.”

The magic words “When X, then Y” often tell us about an event that we can make concrete in our system. Treating events as first-class things in our model helps us make our code more testable and observable, and it helps isolate concerns.

And Table 8-1 shows the trade-offs as we see them.

Table 8-1. Domain events: the trade-offs

- Pros
  - A message bus gives us a nice way to separate responsibilities when we have to take multiple actions in response to a request.
  - Event handlers are nicely decoupled from the “core” application logic, making it easy to change their implementation later.
  - Domain events are a great way to model the real world, and we can use them as part of our business language when modeling with stakeholders.
- Cons
  - The message bus is an additional thing to wrap your head around; the implementation in which the unit of work raises events for us is neat but also magic. It’s not obvious when we call `commit` that we’re also going to go and send email to people.
  - What’s more, that hidden event-handling code executes synchronously, meaning your service-layer function doesn’t finish until all the handlers for any events are finished. That could cause unexpected performance problems in your web endpoints (adding asynchronous processing is possible but makes things even more confusing).
  - More generally, event-driven workflows can be confusing because after things are split across a chain of multiple handlers, there is no single place in the system where you can understand how a request will be fulfilled.
  - You also open yourself up to the possibility of circular dependencies between your event handlers, and infinite loops.

Events are useful for more than just sending email, though. In Chapter 7 we spent a lot of time convincing you that you should define aggregates, or boundaries where we guarantee consistency. People often ask, “What should I do if I need to change multiple aggregates as part of a request?” Now we have the tools we need to answer that question.

If we have two things that can be transactionally isolated (e.g., an order and a product), then we can make them eventually consistent by using events. When an order is canceled, we should find the products that were allocated to it and remove the allocations.

- DOMAIN EVENTS AND THE MESSAGE BUS RECAP
- Events can help with the single responsibility principle
- Code gets tangled up when we mix multiple concerns in one place. Events can help us to keep things tidy by separating primary use cases from secondary ones. We also use events for communicating between aggregates so that we don’t need to run long-running transactions that lock against multiple tables.

- A message bus routes messages to handlers
- You can think of a message bus as a dict that maps from events to their consumers. It doesn’t “know” anything about the meaning of events; it’s just a piece of dumb infrastructure for getting messages around the system.

- Option 1: Service layer raises events and passes them to message bus
- The simplest way to start using events in your system is to raise them from handlers by calling `bus.handle(some_new_event)` after you commit your unit of work.

- Option 2: Domain model raises events, service layer passes them to message bus
- The logic about when to raise an event really should live with the model, so we can improve our system’s design and testability by raising events from the domain model. It’s easy for our handlers to collect events off the model objects after `commit` and pass them to the bus.

- Option 3: UoW collects events from aggregates and passes them to message bus
- Adding `bus.handle(aggregate.events)` to every handler is annoying, so we can tidy up by making our unit of work responsible for raising events that were raised by loaded objects. This is the most complex design and might rely on ORM magic, but it’s clean and easy to use once it’s set up.

In Chapter 9, we’ll look at this idea in more detail as we build a more complex workflow with our new message bus.

1. This principle is the S in [SOLID](https://oreil.ly/AIdSD).

2. Our tech reviewer Ed Jung likes to say that the move from imperative to event-based flow control changes what used to be orchestration into choreography.
