# Epilogue

## What Now?

Phew! We’ve covered a lot of ground in this book, and for most of our audience all of these ideas are new. With that in mind, we can’t hope to make you experts in these techniques. All we can really do is show you the broad-brush ideas, and just enough code for you to go ahead and write something from scratch.

The code we’ve shown in this book isn’t battle-hardened production code: it’s a set of Lego blocks that you can play with to make your first house, spaceship, and skyscraper.

That leaves us with two big tasks. We want to talk about how to start applying these ideas for real in an existing system, and we need to warn you about some of the things we had to skip. We’ve given you a whole new arsenal of ways to shoot yourself in the foot, so we should discuss some basic firearms safety.

## How Do I Get There from Here?

Chances are that a lot of you are thinking something like this:

“OK Bob and Harry, that’s all well and good, and if I ever get hired to work on a green-field new service, I know what to do. But in the meantime, I’m here with my big ball of Django mud, and I don’t see any way to get to your nice, clean, perfect, untainted, simplistic model. Not from here.”

We hear you. Once you’ve already built a big ball of mud, it’s hard to know how to start improving things. Really, we need to tackle things step by step.

First things first: what problem are you trying to solve? Is the software too hard to change? Is the performance unacceptable? Have you got weird, inexplicable bugs?

Having a clear goal in mind will help you to prioritize the work that needs to be done and, importantly, communicate the reasons for doing it to the rest of the team. Businesses tend to have pragmatic approaches to technical debt and refactoring, so long as engineers can make a reasoned argument for fixing things.

---

- TIP

Making complex changes to a system is often an easier sell if you link it to feature work. Perhaps you’re launching a new product or opening your service to new markets? This is the right time to spend engineering resources on fixing the foundations. With a six-month project to deliver, it’s easier to make the argument for three weeks of cleanup work. Bob refers to this as architecture tax.

---

## Separating Entangled Responsibilities

At the beginning of the book, we said that the main characteristic of a big ball of mud is homogeneity: every part of the system looks the same, because we haven’t been clear about the responsibilities of each component. To fix that, we’ll need to start separating out responsibilities and introducing clear boundaries. One of the first things we can do is to start building a service layer (Figure E-1).

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_ep01.png)

This was the system in which Bob first learned how to break apart a ball of mud, and it was a doozy. There was logic everywhere—in the web pages, in manager objects, in helpers, in fat service classes that we’d written to abstract the managers and helpers, and in hairy command objects that we’d written to break apart the services.

If you’re working in a system that’s reached this point, the situation can feel hopeless, but it’s never too late to start weeding an overgrown garden. Eventually, we hired an architect who knew what he was doing, and he helped us get things back under control.

Start by working out the use cases of your system. If you have a user interface, what actions does it perform? If you have a backend processing component, maybe each cron job or Celery job is a single use case. Each of your use cases needs to have an imperative name: Apply Billing Charges, Clean Abandoned Accounts, or Raise Purchase Order, for example.

In our case, most of our use cases were part of the manager classes and had names like Create Workspace or Delete Document Version. Each use case was invoked from a web frontend.

We aim to create a single function or class for each of these supported operations that deals with orchestrating the work to be done. Each use case should do the following:

- Start its own database transaction if needed
- Fetch any required data
- Check any preconditions (see the Ensure pattern in Appendix E)
- Update the domain model
- Persist any changes

Each use case should succeed or fail as an atomic unit. You might need to call one use case from another. That’s OK; just make a note of it, and try to avoid long-running database transactions.

---

- NOTE

One of the biggest problems we had was that manager methods called other manager methods, and data access could happen from the model objects themselves. It was hard to understand what each operation did without going on a treasure hunt across the codebase. Pulling all the logic into a single method, and using a UoW to control our transactions, made the system easier to reason about.

---

---

- CASE STUDY: LAYERING AN OVERGROWN SYSTEM

Many years ago, Bob worked for a software company that had outsourced the first version of its application, an online collaboration platform for sharing and working on files.

When the company brought development in-house, it passed through several generations of developers’ hands, and each wave of new developers added more complexity to the code’s structure.

At its heart, the system was an ASP.NET Web Forms application, built with an NHibernate ORM. Users would upload documents into workspaces, where they could invite other workspace members to review, comment on, or modify their work.

Most of the complexity of the application was in the permissions model because each document was contained in a folder, and folders allowed read, write, and edit permissions, much like a Linux filesystem.

Additionally, each workspace belonged to an account, and the account had quotas attached to it via a billing package.

As a result, every read or write operation against a document had to load an enormous number of objects from the database in order to test permissions and quotas. Creating a new workspace involved hundreds of database queries as we set up the permissions structure, invited users, and set up sample content.

Some of the code for operations was in web handlers that ran when a user clicked a button or submitted a form; some of it was in manager objects that held code for orchestrating work; and some of it was in the domain model. Model objects would make database calls or copy files on disk, and the test coverage was abysmal.

To fix the problem, we first introduced a service layer so that all of the code for creating a document or workspace was in one place and could be understood. This involved pulling data access code out of the domain model and into command handlers. Likewise, we pulled orchestration code out of the managers and the web handlers and pushed it into handlers.

The resulting command handlers were long and messy, but we’d made a start at introducing order to the chaos.

---

- TIP

It’s fine if you have duplication in the use-case functions. We’re not trying to write perfect code; we’re just trying to extract some meaningful layers. It’s better to duplicate some code in a few places than to have use-case functions calling one another in a long chain.

---

This is a good opportunity to pull any data-access or orchestration code out of the domain model and into the use cases. We should also try to pull I/O concerns (e.g., sending email, writing files) out of the domain model and up into the use-case functions. We apply the techniques from Chapter 3 on abstractions to keep our handlers unit testable even when they’re performing I/O.

These use-case functions will mostly be about logging, data access, and error handling. Once you’ve done this step, you’ll have a grasp of what your program actually does, and a way to make sure each operation has a clearly defined start and finish. We’ll have taken a step toward building a pure domain model.

Read Working Effectively with Legacy Code by Michael C. Feathers (Prentice Hall) for guidance on getting legacy code under test and starting separating responsibilities.

## Identifying Aggregates and Bounded Contexts

Part of the problem with the codebase in our case study was that the object graph was highly connected. Each account had many workspaces, and each workspace had many members, all of whom had their own accounts. Each workspace contained many documents, which had many versions.

You can’t express the full horror of the thing in a class diagram. For one thing, there wasn’t really a single account related to a user. Instead, there was a bizarre rule requiring you to enumerate all of the accounts associated to the user via the workspaces and take the one with the earliest creation date.

Every object in the system was part of an inheritance hierarchy that included `SecureObject` and `Version`. This inheritance hierarchy was mirrored directly in the database schema, so that every query had to join across 10 different tables and look at a discriminator column just to tell what kind of objects you were working with.

The codebase made it easy to “dot” your way through these objects like so:

```python
user.account.workspaces[0].documents.versions[1].owner.account.settings[0];
```

Building a system this way with Django ORM or SQLAlchemy is easy but is to be avoided. Although it’s convenient, it makes it very hard to reason about performance because each property might trigger a lookup to the database.

---

- TIP

Aggregates are a consistency boundary. In general, each use case should update a single aggregate at a time. One handler fetches one aggregate from a repository, modifies its state, and raises any events that happen as a result. If you need data from another part of the system, it’s totally fine to use a read model, but avoid updating multiple aggregates in a single transaction. When we choose to separate code into different aggregates, we’re explicitly choosing to make them eventually consistent with one another.

---

A bunch of operations required us to loop over objects this way—for example:

```python
# Lock a user's workspaces for nonpayment

def lock_account(user):
    for workspace in user.account.workspaces:
        workspace.archive()
```

Or even recurse over collections of folders and documents:

```python
def lock_documents_in_folder(folder):

    for doc in folder.documents:
         doc.archive()

     for child in folder.children:
         lock_documents_in_folder(child)
```

These operations killed performance, but fixing them meant giving up our single object graph. Instead, we began to identify aggregates and to break the direct links between objects.

---

- NOTE

We talked about the infamous SELECT N+1 problem in Chapter 12, and how we might choose to use different techniques when reading data for queries versus reading data for commands.

---

Mostly we did this by replacing direct references with identifiers.

Before aggregates:

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_ep02.png)

After modeling with aggregates:

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_ep03.png)

---

- TIP

Bidirectional links are often a sign that your aggregates aren’t right. In our original code, a `Document` knew about its containing `Folder`, and the `Folder` had a collection of `Documents`. This makes it easy to traverse the object graph but stops us from thinking properly about the consistency boundaries we need. We break apart aggregates by using references instead. In the new model, a `Document` had reference to its `parent_folder` but had no way to directly access the `Folder`.

---

If we needed to read data, we avoided writing complex loops and transforms and tried to replace them with straight SQL. For example, one of our screens was a tree view of folders and documents.

This screen was incredibly heavy on the database, because it relied on nested for loops that triggered a lazy-loaded ORM.

---

- TIP

We use this same technique in Chapter 11, where we replace a nested loop over ORM objects with a simple SQL query. It’s the first step in a CQRS approach.

---

After a lot of head-scratching, we replaced the ORM code with a big, ugly stored procedure. The code looked horrible, but it was much faster and helped to break the links between `Folder` and `Document`.

When we needed to write data, we changed a single aggregate at a time, and we introduced a message bus to handle events. For example, in the new model, when we locked an account, we could first query for all the affected workspaces via `SELECT id FROM workspace WHERE account_id = ?`.

We could then raise a new command for each workspace:

```python
for workspace_id in workspaces:
    bus.handle(LockWorkspace(workspace_id))
```

## An Event-Driven Approach to Go to Microservices via Strangler Pattern

The Strangler Fig pattern involves creating a new system around the edges of an old system, while keeping it running. Bits of old functionality are gradually intercepted and replaced, until the old system is left doing nothing at all and can be switched off.

When building the availability service, we used a technique called event interception to move functionality from one place to another. This is a three-step process:

Raise events to represent the changes happening in a system you want to replace.

Build a second system that consumes those events and uses them to build its own domain model.

Replace the older system with the new.

We used event interception to move from Figure E-2…

![Figure E-2. Before: strong, bidirectional coupling based on XML-RPC](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_ep04.png)

to Figure E-3.

![Figure E-3. After: loose coupling with asynchronous events (you can find a high-resolution version of this diagram at cosmicpython.com)](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_ep05.png)

Practically, this was a several month-long project. Our first step was to write a domain model that could represent batches, shipments, and products. We used TDD to build a toy system that could answer a single question: “If I want N units of HAZARDOUS_RUG, how long will they take to be delivered?”

---

- TIP

When deploying an event-driven system, start with a “walking skeleton.” Deploying a system that just logs its input forces us to tackle all the infrastructural questions and start working in production.

---

- CASE STUDY: CARVING OUT A MICROSERVICE TO REPLACE A DOMAIN

MADE.com started out with two monoliths: one for the frontend ecommerce application, and one for the backend fulfillment system.

The two systems communicated through XML-RPC. Periodically, the backend system would wake up and query the frontend system to find out about new orders. When it had imported all the new orders, it would send RPC commands to update the stock levels.

Over time this synchronization process became slower and slower until, one Christmas, it took longer than 24 hours to import a single day’s orders. Bob was hired to break the system into a set of event-driven services.

First, we identified that the slowest part of the process was calculating and synchronizing the available stock. What we needed was a system that could listen to external events and keep a running total of how much stock was available.

We exposed that information via an API, so that the user’s browser could ask how much stock was available for each product and how long it would take to deliver to their address.

Whenever a product ran out of stock completely, we would raise a new event that the ecommerce platform could use to take a product off sale. Because we didn’t know how much load we would need to handle, we wrote the system with a CQRS pattern. Whenever the amount of stock changed, we would update a Redis database with a cached view model. Our Flask API queried these view models instead of running the complex domain model.

As a result, we could answer the question “How much stock is available?” in 2 to 3 milliseconds, and now the API frequently handles hundreds of requests a second for sustained periods.

If this all sounds a little familiar, well, now you know where our example app came from!

---

Once we had a working domain model, we switched to building out some infrastructural pieces. Our first production deployment was a tiny system that could receive a `batch_created` event and log its JSON representation. This is the “Hello World” of event-driven architecture. It forced us to deploy a message bus, hook up a producer and consumer, build a deployment pipeline, and write a simple message handler.

Given a deployment pipeline, the infrastructure we needed, and a basic domain model, we were off. A couple months later, we were in production and serving real customers.

## Convincing Your Stakeholders to Try Something New

If you’re thinking about carving a new system out of a big ball of mud, you’re probably suffering problems with reliability, performance, maintainability, or all three simultaneously. Deep, intractable problems call for drastic measures!

We recommend domain modeling as a first step. In many overgrown systems, the engineers, product owners, and customers no longer speak the same language. Business stakeholders speak about the system in abstract, process-focused terms, while developers are forced to speak about the system as it physically exists in its wild and chaotic state.

---

- CASE STUDY: THE USER MODEL

We mentioned earlier that the account and user model in our first system were bound together by a “bizarre rule.” This is a perfect example of how engineering and business stakeholders can drift apart.

In this system, accounts parented workspaces, and users were members of workspaces. Workspaces were the fundamental unit for applying permissions and quotas. If a user joined a workspace and didn’t already have an account, we would associate them with the account that owned that workspace.

This was messy and ad hoc, but it worked fine until the day a product owner asked for a new feature:

> When a user joins a company, we want to add them to some default workspaces for the company, like the HR workspace or the Company Announcements workspace.

We had to explain to them that there was no such thing as a company, and there was no sense in which a user joined an account. Moreover, a “company” might have many accounts owned by different users, and a new user might be invited to any one of them.

Years of adding hacks and work-arounds to a broken model caught up with us, and we had to rewrite the entire user management function as a brand-new system.

---

Figuring out how to model your domain is a complex task that’s the subject of many decent books in its own right. We like to use interactive techniques like event storming and CRC modeling, because humans are good at collaborating through play. Event modeling is another technique that brings engineers and product owners together to understand a system in terms of commands, queries, and events.

---

- TIP

Check out www.eventmodeling.org and www.eventstorming.org for some great guides to visual modeling of systems with events.

---

The goal is to be able to talk about the system by using the same ubiquitous language, so that you can agree on where the complexity lies.

We’ve found a lot of value in treating domain problems as TDD kata. For example, the first code we wrote for the availability service was the batch and order line model. You can treat this as a lunchtime workshop, or as a spike at the beginning of a project. Once you can demonstrate the value of modeling, it’s easier to make the argument for structuring the project to optimize for modeling.

---

- CASE STUDY: DAVID SEDDON ON TAKING SMALL STEPS

Hi, I’m David, one of the tech reviewers on this book. I’ve worked on several complex Django monoliths, and so I’ve known the pain that Bob and Harry have made all sorts of grand promises about soothing.

When I was first exposed to the patterns described here, I was rather excited. I had successfully used some of the techniques already on smaller projects, but here was a blueprint for much larger, database-backed systems like the one I work on in my day job. So I started trying to figure out how I could implement that blueprint at my current organization.

I chose to tackle a problem area of the codebase that had always bothered me. I began by implementing it as a use case. But I found myself running into unexpected questions. There were things that I hadn’t considered while reading that now made it difficult to see what to do. Was it a problem if my use case interacted with two different aggregates? Could one use case call another? And how was it going to exist within a system that followed different architectural principles without resulting in a horrible mess?

What happened to that oh-so-promising blueprint? Did I actually understand the ideas well enough to put them into practice? Was it even suitable for my application? Even if it was, would any of my colleagues agree to such a major change? Were these just nice ideas for me to fantasize about while I got on with real life?

It took me a while to realize that I could start small. I didn’t need to be a purist or to get it right the first time: I could experiment, finding what worked for me.

And so that’s what I’ve done. I’ve been able to apply some of the ideas in a few places. I’ve built new features whose business logic can be tested without the database or mocks. And as a team, we’ve introduced a service layer to help define the jobs the system does.

If you start trying to apply these patterns in your work, you may go through similar feelings to begin with. When the nice theory of a book meets the reality of your codebase, it can be demoralizing.

My advice is to focus on a specific problem and ask yourself how you can put the relevant ideas to use, perhaps in an initially limited and imperfect fashion. You may discover, as I did, that the first problem you pick might be a bit too difficult; if so, move on to something else. Don’t try to boil the ocean, and don’t be too afraid of making mistakes. It will be a learning experience, and you can be confident that you’re moving roughly in a direction that others have found useful.

So, if you’re feeling the pain too, give these ideas a try. Don’t feel you need permission to rearchitect everything. Just look for somewhere small to start. And above all, do it to solve a specific problem. If you’re successful in solving it, you’ll know you got something right—and others will too.

---

## Questions Our Tech Reviewers Asked That We Couldn’t Work into Prose

Here are some questions we heard during drafting that we couldn’t find a good place to address elsewhere in the book:

> Do I need to do all of this at once? Can I just do a bit at a time?

No, you can absolutely adopt these techniques bit by bit. If you have an existing system, we recommend building a service layer to try to keep orchestration in one place. Once you have that, it’s much easier to push logic into the model and push edge concerns like validation or error handling to the entrypoints.

It’s worth having a service layer even if you still have a big, messy Django ORM because it’s a way to start understanding the boundaries of operations.

> Extracting use cases will break a lot of my existing code; it’s too tangled

Just copy and paste. It’s OK to cause more duplication in the short term. Think of this as a multistep process. Your code is in a bad state now, so copy and paste it to a new place and then make that new code clean and tidy.

Once you’ve done that, you can replace uses of the old code with calls to your new code and finally delete the mess. Fixing large codebases is a messy and painful process. Don’t expect things to get instantly better, and don’t worry if some bits of your application stay messy.

> Do I need to do CQRS? That sounds weird. Can’t I just use repositories?

Of course you can! The techniques we’re presenting in this book are intended to make your life easier. They’re not some kind of ascetic discipline with which to punish yourself.

In our first case-study system, we had a lot of View Builder objects that used repositories to fetch data and then performed some transformations to return dumb read models. The advantage is that when you hit a performance problem, it’s easy to rewrite a view builder to use custom queries or raw SQL.

> How should use cases interact across a larger system? Is it a problem for one to call another?

This might be an interim step. Again, in the first case study, we had handlers that would need to invoke other handlers. This gets really messy, though, and it’s much better to move to using a message bus to separate these concerns.

Generally, your system will have a single message bus implementation and a bunch of subdomains that center on a particular aggregate or set of aggregates. When your use case has finished, it can raise an event, and a handler elsewhere can run.

> Is it a code smell for a use case to use multiple repositories/aggregates, and if so, why?

An aggregate is a consistency boundary, so if your use case needs to update two aggregates atomically (within the same transaction), then your consistency boundary is wrong, strictly speaking. Ideally you should think about moving to a new aggregate that wraps up all the things you want to change at the same time.

If you’re actually updating only one aggregate and using the other(s) for read-only access, then that’s fine, although you could consider building a read/view model to get you that data instead—it makes things cleaner if each use case has only one aggregate.

If you do need to modify two aggregates, but the two operations don’t have to be in the same transaction/UoW, then consider splitting the work out into two different handlers and using a domain event to carry information between the two. You can read more in these papers on aggregate design by Vaughn Vernon.

> What if I have a read-only but business-logic-heavy system?

View models can have complex logic in them. In this book, we’ve encouraged you to separate your read and write models because they have different consistency and throughput requirements. Mostly, we can use simpler logic for reads, but that’s not always true. In particular, permissions and authorization models can add a lot of complexity to our read side.

We’ve written systems in which the view models needed extensive unit tests. In those systems, we split a view builder from a view fetcher, as in Figure E-4.

![Figure E-4. A view builder and view fetcher (you can find a high-resolution version of this diagram at cosmicpython.com)](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_ep06.png)

- This makes it easy to test the view builder by giving it mocked data (e.g., a list of dicts). “Fancy CQRS” with event handlers is really a way of running our complex view logic whenever we write so that we can avoid running it when we read.

> Do I need to build microservices to do this stuff?

Egads, no! These techniques predate microservices by a decade or so. Aggregates, domain events, and dependency inversion are ways to control complexity in large systems. It just so happens that when you’ve built a set of use cases and a model for a business process, moving it to its own service is relatively easy, but that’s not a requirement.

> I’m using Django. Can I still do this?

We have an entire appendix just for you: Appendix D!

## Footguns

OK, so we’ve given you a whole bunch of new toys to play with. Here’s the fine print. Harry and Bob do not recommend that you copy and paste our code into a production system and rebuild your automated trading platform on Redis pub/sub. For reasons of brevity and simplicity, we’ve hand-waved a lot of tricky subjects. Here’s a list of things we think you should know before trying this for real.

> Reliable messaging is hard

Redis pub/sub is not reliable and shouldn’t be used as a general-purpose messaging tool. We picked it because it’s familiar and easy to run. At MADE, we run Event Store as our messaging tool, but we’ve had experience with RabbitMQ and Amazon EventBridge.

Tyler Treat has some excellent blog posts on his site bravenewgeek.com; you should read at least read “You Cannot Have Exactly-Once Delivery” and “What You Want Is What You Don’t: Understanding Trade-Offs in Distributed Messaging”.

> We explicitly choose small, focused transactions that can fail independently

In Chapter 8, we update our process so that deallocating an order line and reallocating the line happen in two separate units of work. You will need monitoring to know when these transactions fail, and tooling to replay events. Some of this is made easier by using a transaction log as your message broker (e.g., Kafka or EventStore). You might also look at the Outbox pattern.

> We don’t discuss idempotency

We haven’t given any real thought to what happens when handlers are retried. In practice you will want to make handlers idempotent so that calling them repeatedly with the same message will not make repeated changes to state. This is a key technique for building reliability, because it enables us to safely retry events when they fail.

There’s a lot of good material on idempotent message handling, try starting with “How to Ensure Idempotency in an Eventual Consistent DDD/CQRS Application” and “(Un)Reliability in Messaging”.

> Your events will need to change their schema over time

You’ll need to find some way of documenting your events and sharing schema with consumers. We like using JSON schema and markdown because it’s simple but there is other prior art. Greg Young wrote an entire book on managing event-driven systems over time: Versioning in an Event Sourced System (Leanpub).

## More Required Reading

A few more books we’d like to recommend to help you on your way:

- Clean Architectures in Python by Leonardo Giordani (Leanpub), which came out in 2019, is one of the few previous books on application architecture in Python.

- Enterprise Integration Patterns by Gregor Hohpe and Bobby Woolf (Addison-Wesley Professional) is a pretty good start for messaging patterns.

- Monolith to Microservices by Sam Newman (O’Reilly), and Newman’s first book, Building Microservices (O’Reilly). The Strangler Fig pattern is mentioned as a favorite, along with many others. These are good to check out if you’re thinking of moving to microservices, and they’re also good on integration patterns and the considerations of async messaging-based integration.

## Wrap-Up

Phew! That’s a lot of warnings and reading suggestions; we hope we haven’t scared you off completely. Our goal with this book is to give you just enough knowledge and intuition for you to start building some of this for yourself. We would love to hear how you get on and what problems you’re facing with the techniques in your own systems, so why not get in touch with us over at www.cosmicpython.com?
