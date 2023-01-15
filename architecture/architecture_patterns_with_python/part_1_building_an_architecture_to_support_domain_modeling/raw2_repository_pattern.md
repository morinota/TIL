# 2. Repository Pattern

It’s time to make good on our promise to use the dependency inversion principle as a way of decoupling our core logic from infrastructural concerns.

We’ll introduce the Repository pattern, a simplifying abstraction over data storage, allowing us to decouple our model layer from the data layer. We’ll present a concrete example of how this simplifying abstraction makes our system more testable by hiding the complexities of the database.

Figure 2-1 shows a little preview of what we’re going to build: a `Repository` object that sits between our domain model and the database.

![Figure 2-1. Before and after the Repository pattern](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0201.png)

The code for this chapter is in the chapter_02_repository branch on GitHub.

## Persisting Our Domain Model

In Chapter 1 we built a simple domain model that can allocate orders to batches of stock. It’s easy for us to write tests against this code because there aren’t any dependencies or infrastructure to set up. If we needed to run a database or an API and create test data, our tests would be harder to write and maintain.

Sadly, at some point we’ll need to put our perfect little model in the hands of users and contend with the real world of spreadsheets and web browsers and race conditions. For the next few chapters we’re going to look at how we can connect our idealized domain model to external state.

We expect to be working in an agile manner, so our priority is to get to a minimum viable product as quickly as possible. In our case, that’s going to be a web API. In a real project, you might dive straight in with some end-to-end tests and start plugging in a web framework, test-driving things outside-in.

But we know that, no matter what, we’re going to need some form of persistent storage, and this is a textbook, so we can allow ourselves a tiny bit more bottom-up development and start to think about storage and databases.

## Some Pseudocode: What Are We Going to Need?

When we build our first API endpoint, we know we’re going to have some code that looks more or less like the following.

What our first API endpoint will look like

```python
@flask.route.gubbins
def allocate_endpoint():
    # extract order line from request
    line = OrderLine(request.params, ...)
    # load all batches from the DB
    batches = ...
    # call our domain service
    allocate(line, batches)
    # then save the allocation back to the database somehow
    return 201
```

- NOTE
  - We’ve used Flask because it’s lightweight, but you don’t need to be a Flask user to understand this book. In fact, we’ll show you how to make your choice of framework a minor detail.

We’ll need a way to retrieve batch info from the database and instantiate our domain model objects from it, and we’ll also need a way of saving them back to the database.

What? Oh, “gubbins” is a British word for “stuff.” You can just ignore that. It’s pseudocode, OK?

## Applying the DIP to Data Access

As mentioned in the introduction, a layered architecture is a common approach to structuring a system that has a UI, some logic, and a database (see Figure 2-2).

![Figure 2-2. Layered architecture
](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0202.png)

Django’s Model-View-Template structure is closely related, as is Model-View-Controller (MVC). In any case, the aim is to keep the layers separate (which is a good thing), and to have each layer depend only on the one below it.

But we want our domain model to have no dependencies whatsoever.1 We don’t want infrastructure concerns bleeding over into our domain model and slowing our unit tests or our ability to make changes.

Instead, as discussed in the introduction, we’ll think of our model as being on the “inside,” and dependencies flowing inward to it; this is what people sometimes call onion architecture (see Figure 2-3).

![Figure 2-3. Onion architecture](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0203.png)

- IS THIS PORTS AND ADAPTERS?
- If you’ve been reading about architectural patterns, you may be asking yourself questions like this:

  - Is this ports and adapters? Or is it hexagonal architecture? Is that the same as onion architecture? What about the clean architecture? What’s a port, and what’s an adapter? Why do you people have so many words for the same thing?

- Although some people like to nitpick over the differences, all these are pretty much names for the same thing, and they all boil down to the dependency inversion principle: high-level modules (the domain) should not depend on low-level ones (the infrastructure).2

- We’ll get into some of the nitty-gritty around “depending on abstractions,” and whether there is a Pythonic equivalent of interfaces, later in the book. See also “What Is a Port and What Is an Adapter, in Python?”.

## Reminder: Our Model

Let’s remind ourselves of our domain model (see Figure 2-4): an allocation is the concept of linking an `OrderLine` to a `Batch`. We’re storing the allocations as a collection on our `Batch` object.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0103.png)

Let’s see how we might translate this to a relational database.

### The “Normal” ORM Way: Model Depends on ORM

These days, it’s unlikely that your team members are hand-rolling their own SQL queries. Instead, you’re almost certainly using some kind of framework to generate SQL for you based on your model objects.

These frameworks are called object-relational mappers (ORMs) because they exist to bridge the conceptual gap between the world of objects and domain modeling and the world of databases and relational algebra.

The most important thing an ORM gives us is persistence ignorance: the idea that our fancy domain model doesn’t need to know anything about how data is loaded or persisted. This helps keep our domain clean of direct dependencies on particular database technologies.3

But if you follow the typical SQLAlchemy tutorial, you’ll end up with something like this:

SQLAlchemy “declarative” syntax, model depends on ORM (orm.py)

```python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Order(Base):
    id = Column(Integer, primary_key=True)

class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Integer(String(250))
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)

class Allocation(Base):
    ...
```

You don’t need to understand SQLAlchemy to see that our pristine model is now full of dependencies on the ORM and is starting to look ugly as hell besides. Can we really say this model is ignorant of the database? How can it be separate from storage concerns when our model properties are directly coupled to database columns?

- DJANGO’S ORM IS ESSENTIALLY THE SAME, BUT MORE RESTRICTIVE
- If you’re more used to Django, the preceding “declarative” SQLAlchemy snippet translates to something like this:

Django ORM example

```python
class Order(models.Model):
    pass

class OrderLine(models.Model):
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    order = models.ForeignKey(Order)

class Allocation(models.Model):
    ...
```

- The point is the same—our model classes inherit directly from ORM classes, so our model depends on the ORM. We want it to be the other way around.
- Django doesn’t provide an equivalent for SQLAlchemy’s classical mapper, but see Appendix D for examples of how to apply dependency inversion and the Repository pattern to Django.

### Inverting the Dependency: ORM Depends on Model

Well, thankfully, that’s not the only way to use SQLAlchemy. The alternative is to define your schema separately, and to define an explicit mapper for how to convert between the schema and our domain model, what SQLAlchemy calls a classical mapping:

Explicit ORM mapping with SQLAlchemy Table objects (orm.py)

```python
from sqlalchemy.orm import mapper, relationship

import model  1


metadata = MetaData()

order_lines = Table(  2
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

...

def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)  3
```

1. The ORM imports (or “depends on” or “knows about”) the domain model, and not the other way around.
2. We define our database tables and columns by using SQLAlchemy’s abstractions.4
3. When we call the mapper function, SQLAlchemy does its magic to bind our domain model classes to the various tables we’ve defined.

The end result will be that, if we call `start_mappers`, we will be able to easily load and save domain model instances from and to the database. But if we never call that function, our domain model classes stay blissfully unaware of the database.

This gives us all the benefits of SQLAlchemy, including the ability to use `alembic` for migrations, and the ability to transparently query using our domain classes, as we’ll see.

When you’re first trying to build your ORM config, it can be useful to write tests for it, as in the following example:

Testing the ORM directly (throwaway tests) (test_orm.py)

```python
def test_orderline_mapper_can_load_lines(session):  1
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty) VALUES '
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )
    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
```

1. If you haven’t used pytest, the session argument to this test needs explaining. You don’t need to worry about the details of pytest or its fixtures for the purposes of this book, but the short explanation is that you can define common dependencies for your tests as “fixtures,” and pytest will inject them to the tests that need them by looking at their function arguments. In this case, it’s a SQLAlchemy database session.

You probably wouldn’t keep these tests around—as you’ll see shortly, once you’ve taken the step of inverting the dependency of ORM and domain model, it’s only a small additional step to implement another abstraction called the Repository pattern, which will be easier to write tests against and will provide a simple interface for faking out later in tests.

But we’ve already achieved our objective of inverting the traditional dependency: the domain model stays “pure” and free from infrastructure concerns. We could throw away SQLAlchemy and use a different ORM, or a totally different persistence system, and the domain model doesn’t need to change at all.

Depending on what you’re doing in your domain model, and especially if you stray far from the OO paradigm, you may find it increasingly hard to get the ORM to produce the exact behavior you need, and you may need to modify your domain model.5 As so often happens with architectural decisions, you’ll need to consider a trade-off. As the Zen of Python says, “Practicality beats purity!”

At this point, though, our API endpoint might look something like the following, and we could get it to work just fine:

Using SQLAlchemy directly in our API endpoint

```python
@flask.route.gubbins
def allocate_endpoint():
    session = start_session()

    # extract order line from request
    line = OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )

    # load all batches from the DB
    batches = session.query(Batch).all()

    # call our domain service
    allocate(line, batches)

    # save the allocation back to the database
    session.commit()

    return 201
```

## Introducing the Repository Pattern

The Repository pattern is an abstraction over persistent storage. It hides the boring details of data access by pretending that all of our data is in memory.

If we had infinite memory in our laptops, we’d have no need for clumsy databases. Instead, we could just use our objects whenever we liked. What would that look like?

You have to get your data from somewhere

```python
import all_my_data

def create_a_batch():
    batch = Batch(...)
    all_my_data.batches.add(batch)

def modify_a_batch(batch_id, new_quantity):
    batch = all_my_data.batches.get(batch_id)
    batch.change_initial_quantity(new_quantity)
```

Even though our objects are in memory, we need to put them somewhere so we can find them again. Our in-memory data would let us add new objects, just like a list or a set. Because the objects are in memory, we never need to call a .save() method; we just fetch the object we care about and modify it in memory.

### The Repository in the Abstract

The simplest repository has just two methods: `add()` to put a new item in the repository, and `get()` to return a previously added item.6 We stick rigidly to using these methods for data access in our domain and our service layer. This self-imposed simplicity stops us from coupling our domain model to the database.

Here’s what an abstract base class (ABC) for our repository would look like:

The simplest possible repository (repository.py)

```python
class AbstractRepository(abc.ABC):

    @abc.abstractmethod  1
    def add(self, batch: model.Batch):
        raise NotImplementedError  2

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
```

1. Python tip: `@abc.abstractmethod` is one of the only things that makes ABCs actually “work” in Python. Python will refuse to let you instantiate a class that does not implement all the `abstractmethods` defined in its parent class.7
2. `raise NotImplementedError` is nice, but it’s neither necessary nor sufficient. In fact, your abstract methods can have real behavior that subclasses can call out to, if you really want.

- ABSTRACT BASE CLASSES, DUCK TYPING, AND PROTOCOLS
  - We’re using abstract base classes in this book for didactic reasons: we hope they help explain what the interface of the repository abstraction is.
  - In real life, we’ve sometimes found ourselves deleting ABCs from our production code, because Python makes it too easy to ignore them, and they end up unmaintained and, at worst, misleading. In practice we often just rely on Python’s duck typing to enable abstractions. To a Pythonista, a repository is any object that has `add(thing)` and `get(id)` methods.
  - An alternative to look into is PEP 544 protocols. These give you typing without the possibility of inheritance, which “prefer composition over inheritance” fans will particularly like.

### What Is the Trade-Off?

> You know they say economists know the price of everything and the value of nothing? Well, programmers know the benefits of everything and the trade-offs of nothing. Rich Hickey

Whenever we introduce an architectural pattern in this book, we’ll always ask, “What do we get for this? And what does it cost us?”

Usually, at the very least, we’ll be introducing an extra layer of abstraction, and although we may hope it will reduce complexity overall, it does add complexity locally, and it has a cost in terms of the raw numbers of moving parts and ongoing maintenance.

The Repository pattern is probably one of the easiest choices in the book, though, if you’re already heading down the DDD and dependency inversion route. As far as our code is concerned, we’re really just swapping the SQLAlchemy abstraction (`session.query(Batch)`) for a different one (`batches_repo.get`) that we designed.

We will have to write a few lines of code in our repository class each time we add a new domain object that we want to retrieve, but in return we get a simple abstraction over our storage layer, which we control. The Repository pattern would make it easy to make fundamental changes to the way we store things (see Appendix C), and as we’ll see, it is easy to fake out for unit tests.

In addition, the Repository pattern is so common in the DDD world that, if you do collaborate with programmers who have come to Python from the Java and C# worlds, they’re likely to recognize it. Figure 2-5 illustrates the pattern.

![Figure 2-5. Repository pattern](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0205.png)

As always, we start with a test. This would probably be classified as an integration test, since we’re checking that our code (the repository) is correctly integrated with the database; hence, the tests tend to mix raw SQL with calls and assertions on our own code.

- tip
- Unlike the ORM tests from earlier, these tests are good candidates for staying part of your codebase longer term, particularly if any parts of your domain model mean the object-relational map is nontrivial.

Repository test for saving an object (test_repository.py)

```python
def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)  1
    session.commit()  2

    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'  3
    ))
    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
```

1. `repo.add()` is the method under test here.
2. We keep the `.commit()` outside of the repository and make it the responsibility of the caller. There are pros and cons for this; some of our reasons will become clearer when we get to Chapter 6.
3. We use the raw SQL to verify that the right data has been saved.

The next test involves retrieving batches and allocations, so it’s more complex:

Repository test for retrieving a complex object (test_repository.py)

```python
def insert_order_line(session):
    session.execute(  1
        'INSERT INTO order_lines (orderid, sku, qty)'
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid="order1", sku="GENERIC-SOFA")
    )
    return orderline_id

def insert_batch(session, batch_id):  2
    ...

def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)  3

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference  3
    assert retrieved.sku == expected.sku  4
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {  4
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
```

1. This tests the read side, so the raw SQL is preparing data to be read by the `repo.get()`.
2. We’ll spare you the details of `insert_batch` and `insert_allocation`; the point is to create a couple of batches, and, for the batch we’re interested in, to have one existing order line allocated to it.
3. And that’s what we verify here. The first `assert ==` checks that the types match, and that the reference is the same (because, as you remember, `Batch` is an entity, and we have a custom `eq` for it).
4. So we also explicitly check on its major attributes, including `._allocations`, which is a Python set of `OrderLine` value objects.

Whether or not you painstakingly write tests for every model is a judgment call. Once you have one class tested for create/modify/save, you might be happy to go on and do the others with a minimal round-trip test, or even nothing at all, if they all follow a similar pattern. In our case, the ORM config that sets up the `._allocations` set is a little complex, so it merited a specific test.

You end up with something like this:

A typical repository (repository.py)

```python
class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
```

And now our Flask endpoint might look something like the following:

Using our repository directly in our API endpoint

```python
@flask.route.gubbins
def allocate_endpoint():
    batches = SqlAlchemyRepository.list()
    lines = [
        OrderLine(l['orderid'], l['sku'], l['qty'])
         for l in request.params...
    ]
    allocate(lines, batches)
    session.commit()
    return 201
```

- EXERCISE FOR THE READER
- We bumped into a friend at a DDD conference the other day who said, “I haven’t used an ORM in 10 years.” The Repository pattern and an ORM both act as abstractions in front of raw SQL, so using one behind the other isn’t really necessary. Why not have a go at implementing our repository without using the ORM? You’ll find the code on GitHub.
- We’ve left the repository tests, but figuring out what SQL to write is up to you. Perhaps it’ll be harder than you think; perhaps it’ll be easier. But the nice thing is, the rest of your application just doesn’t care.

## Building a Fake Repository for Tests Is Now Trivial!

Here’s one of the biggest benefits of the Repository pattern:

A simple fake repository using a set (repository.py)

```python
class FakeRepository(AbstractRepository):

    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
```

Because it’s a simple wrapper around a set, all the methods are one-liners.

Using a fake repo in tests is really easy, and we have a simple abstraction that’s easy to use and reason about:

Example usage of fake repository (test_api.py)

```python
fake_repo = FakeRepository([batch1, batch2, batch3])
```

You’ll see this fake in action in the next chapter.

- TIP
- Building fakes for your abstractions is an excellent way to get design feedback: if it’s hard to fake, the abstraction is probably too complicated.

## What Is a Port and What Is an Adapter, in Python?

We don’t want to dwell on the terminology too much here because the main thing we want to focus on is dependency inversion, and the specifics of the technique you use don’t matter too much. Also, we’re aware that different people use slightly different definitions.

Ports and adapters came out of the OO world, and the definition we hold onto is that the port is the interface between our application and whatever it is we wish to abstract away, and the adapter is the implementation behind that interface or abstraction.

Now Python doesn’t have interfaces per se, so although it’s usually easy to identify an adapter, defining the port can be harder. If you’re using an abstract base class, that’s the port. If not, the port is just the duck type that your adapters conform to and that your core application expects—the function and method names in use, and their argument names and types.

Concretely, in this chapter, `AbstractRepository` is the port, and `SqlAlchemyRepository` and `FakeRepository` are the adapters.

## Wrap-Up

Bearing the Rich Hickey quote in mind, in each chapter we summarize the costs and benefits of each architectural pattern we introduce. We want to be clear that we’re not saying every single application needs to be built this way; only sometimes does the complexity of the app and domain make it worth investing the time and effort in adding these extra layers of indirection.

With that in mind, Table 2-1 shows some of the pros and cons of the Repository pattern and our persistence-ignorant model.

Table 2-1. Repository pattern and persistence ignorance: the trade-offs

- Pros
- We have a simple interface between persistent storage and our domain model.
- It’s easy to make a fake version of the repository for unit testing, or to swap out different storage solutions, because we’ve fully decoupled the model from infrastructure concerns.
- Writing the domain model before thinking about persistence helps us focus on the business problem at hand. If we ever want to radically change our approach, we can do that in our model, without needing to worry about foreign keys or migrations until later.
- Our database schema is really simple because we have complete control over how we map our objects to tables.
- Cons
- An ORM already buys you some decoupling. Changing foreign keys might be hard, but it should be pretty easy to swap between MySQL and Postgres if you ever need to.
- Maintaining ORM mappings by hand requires extra work and extra code.
- Any extra layer of indirection always increases maintenance costs and adds a “WTF factor” for Python programmers who’ve never seen the Repository pattern before.

Figure 2-6 shows the basic thesis: yes, for simple cases, a decoupled domain model is harder work than a simple ORM/ActiveRecord pattern.8

- TIP
- If your app is just a simple CRUD (create-read-update-delete) wrapper around a database, then you don’t need a domain model or a repository.

But the more complex the domain, the more an investment in freeing yourself from infrastructure concerns will pay off in terms of the ease of making changes.

![Figure 2-6. Domain model trade-offs as a diagram](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0206.png)

Our example code isn’t complex enough to give more than a hint of what the right-hand side of the graph looks like, but the hints are there. Imagine, for example, if we decide one day that we want to change allocations to live on the `OrderLine` instead of on the `Batch` object: if we were using Django, say, we’d have to define and think through the database migration before we could run any tests. As it is, because our model is just plain old Python objects, we can change a `set()` to being a new attribute, without needing to think about the database until later.

- REPOSITORY PATTERN RECAP
- Apply dependency inversion to your ORM
  - Our domain model should be free of infrastructure concerns, so your ORM should import your model, and not the other way around.
- The Repository pattern is a simple abstraction around permanent storage
  - The repository gives you the illusion of a collection of in-memory objects. It makes it easy to create a FakeRepository for testing and to swap fundamental details of your infrastructure without disrupting your core application. See Appendix C for an example.

You’ll be wondering, how do we instantiate these repositories, fake or real? What will our Flask app actually look like? You’ll find out in the next exciting installment, the Service Layer pattern.

But first, a brief digression.

- 1 I suppose we mean “no stateful dependencies.” Depending on a helper library is fine; depending on an ORM or a web framework is not.
- 2 Mark Seemann has an excellent blog post on the topic.
- 3 In this sense, using an ORM is already an example of the DIP. Instead of depending on hardcoded SQL, we depend on an abstraction, the ORM. But that’s not enough for us—not in this book!
- 4 Even in projects where we don’t use an ORM, we often use SQLAlchemy alongside Alembic to declaratively create schemas in Python and to manage migrations, connections, and sessions.
- 5 Shout-out to the amazingly helpful SQLAlchemy maintainers, and to Mike Bayer in particular.
- 6 You may be thinking, “What about list or delete or update?” However, in an ideal world, we modify our model objects one at a time, and delete is usually handled as a soft-delete—i.e., batch.cancel(). Finally, update is taken care of by the Unit of Work pattern, as you’ll see in Chapter 6.
- 7 To really reap the benefits of ABCs (such as they may be), be running helpers like pylint and mypy.
- 8 Diagram inspired by a post called “Global Complexity, Local Simplicity” by Rob Vens.
