# chapter 13. Dependency Injection (And Bootstrapping)

Dependency injection (DI) is regarded with suspicion in the Python world. And we’ve managed just fine without it so far in the example code for this book!

In this chapter, we’ll explore some of the pain points in our code that lead us to consider using DI, and we’ll present some options for how to do it, leaving it to you to pick which you think is most Pythonic.

We’ll also add a new component to our architecture called bootstrap.py; it will be in charge of dependency injection, as well as some other initialization stuff that we often need. We’ll explain why this sort of thing is called a composition root in OO languages, and why bootstrap script is just fine for our purposes.

Figure 13-1 shows what our app looks like without a bootstrapper: the entrypoints do a lot of initialization and passing around of our main dependency, the UoW.

---

TIP

If you haven’t already, it’s worth reading Chapter 3 before continuing with this chapter, particularly the discussion of functional versus object-oriented dependency management.

---

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1301.png)

---

TIP
The code for this chapter is in the chapter_13_dependency_injection branch on GitHub:

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_13_dependency_injection
# or to code along, checkout the previous chapter:
git checkout chapter_12_cqrs
```

---

Figure 13-2 shows our bootstrapper taking over those responsibilities.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1302.png)

## Implicit Versus Explicit Dependencies

Depending on your particular brain type, you may have a slight feeling of unease at the back of your mind at this point. Let’s bring it out into the open. We’ve shown you two ways of managing dependencies and testing them.

For our database dependency, we’ve built a careful framework of explicit dependencies and easy options for overriding them in tests. Our main handler functions declare an explicit dependency on the UoW:

Our handlers have an explicit dependency on the UoW (src/allocation/service_layer/handlers.py)

```python
def allocate(
        cmd: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork
):
```

And that makes it easy to swap in a fake UoW in our service-layer tests:

Service-layer tests against a fake UoW: (tests/unit/test_services.py)

```python
    uow = FakeUnitOfWork()
    messagebus.handle([...], uow)
```

The UoW itself declares an explicit dependency on the session factory:

The UoW depends on a session factory (src/allocation/service_layer/unit_of_work.py)

```python
class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
        ...
```

We take advantage of it in our integration tests to be able to sometimes use SQLite instead of Postgres:

Integration tests against a different DB (tests/integration/test_uow.py)

```python
def test_rolls_back_uncommitted_work_by_default(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)  1
```

1. Integration tests swap out the default Postgres session_factory for a SQLite one.

## Aren’t Explicit Dependencies Totally Weird and Java-y?

If you’re used to the way things normally happen in Python, you’ll be thinking all this is a bit weird. The standard way to do things is to declare our dependency implicitly by simply importing it, and then if we ever need to change it for tests, we can monkeypatch, as is Right and True in dynamic languages:

Email sending as a normal import-based dependency (src/allocation/service_layer/handlers.py)

```python
from allocation.adapters import email, redis_eventpublisher  1
...

def send_out_of_stock_notification(
        event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork,
):
    email.send(  2
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
```

1. Hardcoded import

2. Calls specific email sender directly

Why pollute our application code with unnecessary arguments just for the sake of our tests? `mock.patch` makes monkeypatching nice and easy:

mock dot patch, thank you Michael Foord (tests/unit/test_handlers.py)

```python
    with mock.patch("allocation.adapters.email.send") as mock_send_mail:
        ...
```

The trouble is that we’ve made it look easy because our toy example doesn’t send real email (`email.send_mail` just does a `print`), but in real life, you’d end up having to call `mock.patch` for every single test that might cause an out-of-stock notification. If you’ve worked on codebases with lots of mocks used to prevent unwanted side effects, you’ll know how annoying that mocky boilerplate gets.

And you’ll know that mocks tightly couple us to the implementation. By choosing to monkeypatch `email.send_mail`, we are tied to doing `import email`, and if we ever want to do `from email import send_mail`, a trivial refactor, we’d have to change all our mocks.

So it’s a trade-off. Yes, declaring explicit dependencies is unnecessary, strictly speaking, and using them would make our application code marginally more complex. But in return, we’d get tests that are easier to write and manage.

On top of that, declaring an explicit dependency is an example of the dependency inversion principle—rather than having an (implicit) dependency on a specific detail, we have an (explicit) dependency on an abstraction:

> Explicit is better than implicit. ---The Zen of Python

The explicit dependency is more abstract (src/allocation/service_layer/handlers.py)

```python
def send_out_of_stock_notification(
        event: events.OutOfStock, send_mail: Callable,
):
    send_mail(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
```

But if we do change to declaring all these dependencies explicitly, who will inject them, and how? So far, we’ve really been dealing with only passing the UoW around: our tests use `FakeUnitOfWork`, while Flask and Redis eventconsumer entrypoints use the real UoW, and the message bus passes them onto our command handlers. If we add real and fake email classes, who will create them and pass them on?

That’s extra (duplicated) cruft for Flask, Redis, and our tests. Moreover, putting all the responsibility for passing dependencies to the right handler onto the message bus feels like a violation of the SRP.

Instead, we’ll reach for a pattern called Composition Root (a bootstrap script to you and me),1 and we’ll do a bit of “manual DI” (dependency injection without a framework). See Figure 13-3.2

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1303.png)

## Preparing Handlers: Manual DI with Closures and Partials

One way to turn a function with dependencies into one that’s ready to be called later with those dependencies already injected is to use closures or partial functions to compose the function with its dependencies:

Examples of DI using closures or partial functions

```python
# existing allocate function, with abstract uow dependency
def allocate(
        cmd: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork
):
    line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
    with uow:
        ...

# bootstrap script prepares actual UoW

def bootstrap(..):
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    # prepare a version of the allocate fn with UoW dependency captured in a closure
    allocate_composed = lambda cmd: allocate(cmd, uow)

    # or, equivalently (this gets you a nicer stack trace)
    def allocate_composed(cmd):
        return allocate(cmd, uow)

    # alternatively with a partial
    import functools
    allocate_composed = functools.partial(allocate, uow=uow)  1

# later at runtime, we can call the partial function, and it will have
# the UoW already bound
allocate_composed(cmd)
```

1. The difference between closures (lambdas or named functions) and `functools.partial` is that the former use late binding of variables, which can be a source of confusion if any of the dependencies are mutable.

Here’s the same pattern again for the `send_out_of_stock_notification()` handler, which has different dependencies:

Another closure and partial functions example

```python
def send_out_of_stock_notification(
        event: events.OutOfStock, send_mail: Callable,
):
    send_mail(
        'stock@made.com',
        ...


# prepare a version of the send_out_of_stock_notification with dependencies
sosn_composed  = lambda event: send_out_of_stock_notification(event, email.send_mail)

...
# later, at runtime:
sosn_composed(event)  # will have email.send_mail already injected in
```

## An Alternative Using Classes

Closures and partial functions will feel familiar to people who’ve done a bit of functional programming. Here’s an alternative using classes, which may appeal to others. It requires rewriting all our handler functions as classes, though:

DI using classes

```python
# we replace the old `def allocate(cmd, uow)` with:

class AllocateHandler:

    def __init__(self, uow: unit_of_work.AbstractUnitOfWork):  2
        self.uow = uow

    def __call__(self, cmd: commands.Allocate):  1
        line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
        with self.uow:
            # rest of handler method as before
            ...

# bootstrap script prepares actual UoW
uow = unit_of_work.SqlAlchemyUnitOfWork()

# then prepares a version of the allocate fn with dependencies already injected
allocate = AllocateHandler(uow)

...
# later at runtime, we can call the handler instance, and it will have
# the UoW already injected
allocate(cmd)
```

1. The class is designed to produce a callable function, so it has a `call` method.

2. But we use the `init` to declare the dependencies it requires. This sort of thing will feel familiar if you’ve ever made class-based descriptors, or a class-based context manager that takes arguments.

Use whichever you and your team feel more comfortable with.

## A Bootstrap Script

We want our bootstrap script to do the following:

1. Declare default dependencies but allow us to override them
2. Do the “init” stuff that we need to get our app started
3. Inject all the dependencies into our handlers
4. Give us back the core object for our app, the message bus

Here’s a first cut:

A bootstrap function (src/allocation/bootstrap.py)

```python
def bootstrap(
    start_orm: bool = True,  1
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),  2
    send_mail: Callable = email.send,
    publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:

    if start_orm:
        orm.start_mappers()  1

    dependencies = {'uow': uow, 'send_mail': send_mail, 'publish': publish}
    injected_event_handlers = {  3
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {  3
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(  4
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )
```

1. `orm.start_mappers()` is our example of initialization work that needs to be done once at the beginning of an app. We also see things like setting up the `logging` module.

2. We can use the argument defaults to define what the normal/production defaults are. It’s nice to have them in a single place, but sometimes dependencies have some side effects at construction time, in which case you might prefer to default them to `None` instead.

3. We build up our injected versions of the handler mappings by using a function called `inject_dependencies()`, which we’ll show next.

4. We return a configured message bus ready for use.

Here’s how we inject dependencies into a handler function by inspecting it:

DI by inspecting function signatures (src/allocation/bootstrap.py)

```python
def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters  1
    deps = {
        name: dependency
        for name, dependency in dependencies.items()  2
        if name in params
    }
    return lambda message: handler(message, **deps)  3
```

1. We inspect our command/event handler’s arguments.

2. We match them by name to our dependencies.

3. We inject them as kwargs to produce a partial.

---

- EVEN-MORE-MANUAL DI WITH LESS MAGIC

If you’re finding the preceding `inspect` code a little harder to grok, this even simpler version may appeal to you.

Harry wrote the code for `inject_dependencies()` as a first cut of how to do “manual” dependency injection, and when he saw it, Bob accused him of overengineering and writing his own DI framework.

It honestly didn’t even occur to Harry that you could do it any more plainly, but you can, like this:

Manually creating partial functions inline (src/allocation/bootstrap.py)

```python
    injected_event_handlers = {
        events.Allocated: [
            lambda e: handlers.publish_allocated_event(e, publish),
            lambda e: handlers.add_allocation_to_read_model(e, uow),
        ],
        events.Deallocated: [
            lambda e: handlers.remove_allocation_from_read_model(e, uow),
            lambda e: handlers.reallocate(e, uow),
        ],
        events.OutOfStock: [
            lambda e: handlers.send_out_of_stock_notification(e, send_mail)
        ]
    }
    injected_command_handlers = {
        commands.Allocate: lambda c: handlers.allocate(c, uow),
        commands.CreateBatch: \
            lambda c: handlers.add_batch(c, uow),
        commands.ChangeBatchQuantity: \
            lambda c: handlers.change_batch_quantity(c, uow),
    }
```

Harry says he couldn’t even imagine writing out that many lines of code and having to look up that many function arguments manually. This is a perfectly viable solution, though, since it’s only one line of code or so per handler you add, and thus not a massive maintenance burden even if you have dozens of handlers.

Our app is structured in such a way that we always want to do dependency injection in only one place, the handler functions, so this super-manual solution and Harry’s `inspect()`-based one will both work fine.

If you find yourself wanting to do DI in more things and at different times, or if you ever get into dependency chains (in which your dependencies have their own dependencies, and so on), you may get some mileage out of a “real” DI framework.

At MADE, we’ve used Inject in a few places, and it’s fine, although it makes Pylint unhappy. You might also check out Punq, as written by Bob himself, or the DRY-Python crew’s dependencies.

---

## Message Bus Is Given Handlers at Runtime

Our message bus will no longer be static; it needs to have the already-injected handlers given to it. So we turn it from being a module into a configurable class:

MessageBus as a class (src/allocation/service_layer/messagebus.py)

```python
class MessageBus:  1

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],  2
        command_handlers: Dict[Type[commands.Command], Callable],  2
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):  3
        self.queue = [message]  4
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f'{message} was not an Event or Command')
```

1. The message bus becomes a class…

2. …which is given its already-dependency-injected handlers.

3. The main `handle()` function is substantially the same, with just a few attributes and methods moved onto `self`.

4. Using `self.queue` like this is not thread-safe, which might be a problem if you’re using threads, because the bus instance is global in the Flask app context as we’ve written it. Just something to watch out for.

What else changes in the bus?

Event and command handler logic stays the same (src/allocation/service_layer/messagebus.py)

```python
    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:  1
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                handler(event)  2
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue


    def handle_command(self, command: commands.Command):
        logger.debug('handling command %s', command)
        try:
            handler = self.command_handlers[type(command)]  1
            handler(command)  2
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise
```

1. `handle_event` and `handle_command` are substantially the same, but instead of indexing into a static `EVENT_HANDLERS` or `COMMAND_HANDLERS` dict, they use the versions on `self`.

2. Instead of passing a UoW into the handler, we expect the handlers to already have all their dependencies, so all they need is a single argument, the specific event or command.

## Using Bootstrap in Our Entrypoints

In our application’s entrypoints, we now just call `bootstrap.bootstrap()` and get a message bus that’s ready to go, rather than configuring a UoW and the rest of it:

Flask calls bootstrap (src/allocation/entrypoints/flask_app.py)

```python
-from allocation import views
+from allocation import bootstrap, views

 app = Flask(__name__)
-orm.start_mappers()  1
+bus = bootstrap.bootstrap()


 @app.route("/add_batch", methods=['POST'])
@@ -19,8 +16,7 @@ def add_batch():
     cmd = commands.CreateBatch(
         request.json['ref'], request.json['sku'], request.json['qty'], eta,
     )
-    uow = unit_of_work.SqlAlchemyUnitOfWork()  2
-    messagebus.handle(cmd, uow)
+    bus.handle(cmd)  3
     return 'OK', 201
```

1. We no longer need to call `start_orm()`; the bootstrap script’s initialization stages will do that.

2. We no longer need to explicitly build a particular type of UoW; the bootstrap script defaults take care of it.

3. And our message bus is now a specific instance rather than the global module.3

## Initializing DI in Our Tests

In tests, we can use `bootstrap.bootstrap()` with overridden defaults to get a custom message bus. Here’s an example in an integration test:

Overriding bootstrap defaults (tests/integration/test_views.py)

```python
@pytest.fixture
def sqlite_bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,  1
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),  2
        send_mail=lambda *args: None,  3
        publish=lambda *args: None,  3
    )
    yield bus
    clear_mappers()

def test_allocations_view(sqlite_bus):
    sqlite_bus.handle(commands.CreateBatch('sku1batch', 'sku1', 50, None))
    sqlite_bus.handle(commands.CreateBatch('sku2batch', 'sku2', 50, date.today()))
    ...
    assert views.allocations('order1', sqlite_bus.uow) == [
        {'sku': 'sku1', 'batchref': 'sku1batch'},
        {'sku': 'sku2', 'batchref': 'sku2batch'},
    ]
```

1. We do still want to start the ORM…

2. …because we’re going to use a real UoW, albeit with an in-memory database.

3. But we don’t need to send email or publish, so we make those noops.

In our unit tests, in contrast, we can reuse our `FakeUnitOfWork`:

Bootstrap in unit test (tests/unit/test_handlers.py)

```python
def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False,  1
        uow=FakeUnitOfWork(),  2
        send_mail=lambda *args: None,  3
        publish=lambda *args: None,  3
    )
```

1. No need to start the ORM…

2. …because the fake UoW doesn’t use one.

3. We want to fake out our email and Redis adapters too.

So that gets rid of a little duplication, and we’ve moved a bunch of setup and sensible defaults into a single place.

---

EXERCISE FOR THE READER 1

Change all the handlers to being classes as per the DI using classes example, and amend the bootstrapper’s DI code as appropriate. This will let you know whether you prefer the functional approach or the class-based approach when it comes to your own projects.

---

## Building an Adapter “Properly”: A Worked Example

To really get a feel for how it all works, let’s work through an example of how you might “properly” build an adapter and do dependency injection for it.

At the moment, we have two types of dependencies:

Two types of dependencies (src/allocation/service_layer/messagebus.py)

```python
    uow: unit_of_work.AbstractUnitOfWork,  1
    send_mail: Callable,  2
    publish: Callable,  2    uow: unit_of_work.AbstractUnitOfWork,  1
    send_mail: Callable,  2
    publish: Callable,  2
```

1. The UoW has an abstract base class. This is the heavyweight option for declaring and managing your external dependency. We’d use this for the case when the dependency is relatively complex.

2. Our email sender and pub/sub publisher are defined as functions. This works just fine for simple dependencies.

Here are some of the things we find ourselves injecting at work:

- An S3 filesystem client
- A key/value store client
- A `requests` session object

Most of these will have more-complex APIs that you can’t capture as a single function: read and write, GET and POST, and so on.

Even though it’s simple, let’s use `send_mail` as an example to talk through how you might define a more complex dependency.

### Define the Abstract and Concrete Implementations

We’ll imagine a more generic notifications API. Could be email, could be SMS, could be Slack posts one day.

An ABC and a concrete implementation (src/allocation/adapters/notifications.py)

```python
class AbstractNotifications(abc.ABC):

    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError

...

class EmailNotifications(AbstractNotifications):

    def __init__(self, smtp_host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server = smtplib.SMTP(smtp_host, port=port)
        self.server.noop()

    def send(self, destination, message):
        msg = f'Subject: allocation service notification\n{message}'
        self.server.sendmail(
            from_addr='allocations@example.com',
            to_addrs=[destination],
            msg=msg
        )
```

We change the dependency in the bootstrap script:

Notifications in message bus (src/allocation/bootstrap.py)

```python
 def bootstrap(
     start_orm: bool = True,
     uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
-    send_mail: Callable = email.send,
+    notifications: AbstractNotifications = EmailNotifications(),
     publish: Callable = redis_eventpublisher.publish,
 ) -> messagebus.MessageBus:
```

### Make a Fake Version for Your Tests

We work through and define a fake version for unit testing:

Fake notifications (tests/unit/test_handlers.py)

```python
class FakeNotifications(notifications.AbstractNotifications):

    def __init__(self):
        self.sent = defaultdict(list)  # type: Dict[str, List[str]]

    def send(self, destination, message):
        self.sent[destination].append(message)
...
```

And we use it in our tests:

Tests change slightly (tests/unit/test_handlers.py)

```python
    def test_sends_email_on_out_of_stock_error(self):
        fake_notifs = FakeNotifications()
        bus = bootstrap.bootstrap(
            start_orm=False,
            uow=FakeUnitOfWork(),
            notifications=fake_notifs,
            publish=lambda *args: None,
        )
        bus.handle(commands.CreateBatch("b1", "POPULAR-CURTAINS", 9, None))
        bus.handle(commands.Allocate("o1", "POPULAR-CURTAINS", 10))
        assert fake_notifs.sent['stock@made.com'] == [
            f"Out of stock for POPULAR-CURTAINS",
        ]
```

### Figure Out How to Integration Test the Real Thing

Now we test the real thing, usually with an end-to-end or integration test. We’ve used MailHog as a real-ish email server for our Docker dev environment:

Docker-compose config with real fake email server (docker-compose.yml)

```yaml
version: "3"

services:

  redis_pubsub:
    build:
      context: .
      dockerfile: Dockerfile
    image: allocation-image
    ...

  api:
    image: allocation-image
    ...

  postgres:
    image: postgres:9.6
    ...

  redis:
    image: redis:alpine
    ...

  mailhog:
    image: mailhog/mailhog
    ports:
      - "11025:1025"
      - "18025:8025"
```

In our integration tests, we use the real `EmailNotifications` class, talking to the MailHog server in the Docker cluster:

Integration test for email (tests/integration/test_email.py)

```python
@pytest.fixture
def bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
        notifications=notifications.EmailNotifications(),  1
        publish=lambda *args: None,
    )
    yield bus
    clear_mappers()


def get_email_from_mailhog(sku):  2
    host, port = map(config.get_email_host_and_port().get, ['host', 'http_port'])
    all_emails = requests.get(f'http://{host}:{port}/api/v2/messages').json()
    return next(m for m in all_emails['items'] if sku in str(m))


def test_out_of_stock_email(bus):
    sku = random_sku()
    bus.handle(commands.CreateBatch('batch1', sku, 9, None))  3
    bus.handle(commands.Allocate('order1', sku, 10))
    email = get_email_from_mailhog(sku)
    assert email['Raw']['From'] == 'allocations@example.com'  4
    assert email['Raw']['To'] == ['stock@made.com']
    assert f'Out of stock for {sku}' in email['Raw']['Data']
```

1. We use our bootstrapper to build a message bus that talks to the real notifications class.

2. We figure out how to fetch emails from our “real” email server.

3. We use the bus to do our test setup.

4. Against all the odds, this actually worked, pretty much at the first go!

And that’s it really.

---

EXERCISE FOR THE READER 2

You could do two things for practice regarding adapters:

1. Try swapping out our notifications from email to SMS notifications using Twilio, for example, or Slack notifications. Can you find a good equivalent to MailHog for integration testing?

2. In a similar way to what we did moving from `send_mail` to a `Notifications` class, try refactoring our `redis_eventpublisher` that is currently just a `Callable` to some sort of more formal adapter/base class/protocol.

---

## Wrap-Up

Once you have more than one adapter, you’ll start to feel a lot of pain from passing dependencies around manually, unless you do some kind of dependency injection.

Setting up dependency injection is just one of many typical setup/initialization activities that you need to do just once when starting your app. Putting this all together into a bootstrap script is often a good idea.

The bootstrap script is also good as a place to provide sensible default configuration for your adapters, and as a single place to override those adapters with fakes for your tests.

A dependency injection framework can be useful if you find yourself needing to do DI at multiple levels—if you have chained dependencies of components that all need DI, for example.

This chapter also presented a worked example of changing an implicit/simple dependency into a “proper” adapter, factoring out an ABC, defining its real and fake implementations, and thinking through integration testing.

---

- DI AND BOOTSTRAP RECAP

In summary:

1. Define your API using an ABC.

2. Implement the real thing.

3. Build a fake and use it for unit/service-layer/handler tests.

4. Find a less fake version you can put into your Docker environment.

5. Test the less fake “real” thing.

6. Profit!

---

These were the last patterns we wanted to cover, which brings us to the end of Part II. In the epilogue, we’ll try to give you some pointers for applying these techniques in the Real WorldTM.

1. Because Python is not a “pure” OO language, Python developers aren’t necessarily used to the concept of needing to compose a set of objects into a working application. We just pick our entrypoint and run code from top to bottom.

2. Mark Seemann calls this Pure DI or sometimes Vanilla DI.

3. However, it’s still a global in the `flask_app` module scope, if that makes sense. This may cause problems if you ever find yourself wanting to test your Flask app in-process by using the Flask Test Client instead of using Docker as we do. It’s worth researching Flask app factories if you get into this.
