## links

- https://microservices.io/patterns/microservices.html

# Pattern: Microservice Architecture

## Context

You are developing a business-critical enterprise application. You need to deliver changes rapidly, frequently and reliably - as measured by the DORA metrics - in order for your business to thrive in today’s volatile, uncertain, complex and ambiguous world. Consequently, your engineering organization is organized into small, loosely coupled, cross-functional teams. Each team delivers software using DevOps practices as defined by the DevOps handbook. In particular, it practices continuous deployment. The team delivers a stream of small, frequent changes that are tested by an automated deployment pipeline and deployed into production.

A team is responsible for one or more subdomains. A subdomain is an implementable model of a slice of business functionality, a.k.a. business capability. It consists of business logic, which consists of business entities (a.k.a. DDD aggregates) that implement business rules, and adapters, which communicate with the outside world. A Java-based subdomain, for example, consists of classes organized into packages that’s compiled into a JAR file.

The subdomains implement the application’s behavior, which consists of a set of (system) operations. An operation is invoked in one of three ways: synchronous and asynchronous requests from clients; events published by other applications and services; and the passing of time. It mutates and queries business entities in one or more subdomains.

## Problem

How to organize the subdomains into one or more deployable/executable components?

## Forces

There are five dark energy forces:

- Simple components - simple components consisting of few subdomains are easier to understand and maintain than complex components
- Team autonomy - a team needs to be able develop, test and deploy their software independently of other teams
- Fast deployment pipeline - fast feedback and high deployment frequency are essential and are enabled by a fast deployment pipeline, which in turn requires components that are fast to build and test.
- Support multiple technology stacks - subdomains are sometimes implemented using a variety of technologies; and developers need to evolve the application’s technology stack, e.g. use current versions of languages and frameworks
- Segregate subdomains by their characteristics - e.g. resource requirements to improve scalability, their availability requirements to improve availability, their security requirements to improve security, etc.

There are five dark matter forces:

- Simple interactions - an operation that’s local to a component or consists of a few simple interactions between components is easier to understand and troubleshoot than complex interactions
- Efficient interactions - a distributed operation that involves lots of network roundtrips and large data transfers can be too inefficient
- Prefer ACID over BASE - it’s easier to implement an operation as an ACID transaction rather than, for example, eventually consistent sagas
- Minimize runtime coupling - to maximize the availability and reduce the latency of an operation
- Minimize design time coupling - reduce the likelihood of changing services in lockstep, which reduces productivity

## Solution

Design an architecture that structures the application as a set of independently deployable, loosely coupled, components, a.k.a. services. Each service consists of one or more subdomains.

Some operations will be local (implemented by a single service), while others will be distributed across multiple services. A distributed operation is implemented using either synchronously using a protocol such as HTTP/REST or asynchronously using a message broker, such as Apache Kafka.

## Examples

### Fictitious e-commerce application

Let’s imagine that you are building an e-commerce application that takes orders from customers, verifies inventory and available credit, and ships them. The application consists of several components including the StoreFrontUI, which implements the user interface, along with some backend services for checking credit, maintaining inventory and shipping orders. The application consists of a set of services.

### Show me the code

Please see the example applications developed by Chris Richardson. These examples on Github illustrate various aspects of the microservice architecture.

## Resulting context

### Benefits

This solution has a number of benefits:

Simple services - each service consists of a small number of subdomains - possibly just one - and so is easier to understand and maintain
Team autonomy - a team can develop, test and deploy their service independently of other teams
Fast deployment pipeline - each service is fast to test since it’s relatively small, and can be deployed independently
Support multiple technology stacks - different services can use different technology stacks and can be upgraded independently
Segregate subdomains by their characteristics - subdomains can be segregated by their characteristics into separate services in order to improve scalability, availabilty, security etc

### Drawbacks

This solution has a number of (potential) drawbacks:

Some distributed operations might be complex, and difficult to understand and troubleshoot
Some distributed operations might be potentially inefficient
Some operations might need to be implemented using complex, eventually consistent (non-ACID) transaction management since loose coupling requires each service to have its own database.
Some distributed operations might involve tight runtime coupling between services, which reduces their availability.
Risk of tight design-time coupling between services, which requires time consuming lockstep changes

### Issues

There are many issues that you must address.

#### How to design a microservice architecture that avoids the potential drawbacks?

How to design a microservice architecture that avoids the potential drawbacks of complex, inefficient interactions; complex eventually consistent transactions; and tight runtime coupling. Assemblage, is an architecture definition process that uses the dark energy and dark matter forces to group the subdomains in a way that results in good microservice architecture.

#### How to implement distributed operations?

One challenge with using the microservice operation is implementing distributed operations, which span multiple services. This is especially challenging since each service has its own database. The solution is to use the service collaboration patterns:

Saga, which implements a distributed command as a series of local transactions
Command-side replica, which replicas read-only data to the service that implements a command
API composition, which implements a distributed query as a series of local queries
CQRS, which implements a distributed query as a series of local queries
The Saga, Command-side replica and CQRS patterns use asynchronous messaging. Services typically need to use the Transaction Outbox pattern to atomically update persistent business entities and send a message.

## Related patterns

There are many patterns related to the Microservices architecture pattern. The Monolithic architecture is an alternative to the microservice architecture. The other patterns in the Microservice architecture architecture pattern address issues that you will encounter when applying this pattern.

Sservice collaboration patterns:

- Saga, which implements a distributed command as a series of local transactions
- Command-side replica, which replicas read-only data to the service that implements a command
- API composition, which implements a distributed query as a series of local queries
- CQRS, which implements a distributed query as a series of local queries

The Messaging and Remote Procedure Invocation patterns are two different ways that services can communicate.
The Database per Service pattern describes how each service has its own database in order to ensure loose coupling.
The API Gateway pattern defines how clients access the services in a microservice architecture.
The Client-side Discovery and Server-side Discovery patterns are used to route requests for a client to an available service instance in a microservice architecture.
Testing patterns: Service Component Test and Service Integration Contract Test
Circuit Breaker
Access Token
Observability patterns:

- Log aggregation
- Application metrics
- Audit logging
- Distributed tracing
- Exception tracking
- Health check API
- Log deployments and changes

UI patterns:

- Server-side page fragment composition
- Client-side UI composition

The Single Service per Host and Multiple Services per Host patterns are two different deployment strategies.
Cross-cutting concerns patterns: Microservice chassis pattern and Externalized configuration

## Known uses

Most large scale web sites including Netflix, Amazon and eBay have evolved from a monolithic architecture to a microservice architecture.

Netflix, which is a very popular video streaming service that’s responsible for up to 30% of Internet traffic, has a large scale, service-oriented architecture. They handle over a billion calls per day to their video streaming API from over 800 different kinds of devices. Each API call fans out to an average of six calls to backend services.

Amazon.com originally had a two-tier architecture. In order to scale they migrated to a service-oriented architecture consisting of hundreds of backend services. Several applications call these services including the applications that implement the Amazon.com website and the web service API. The Amazon.com website application calls 100-150 services to get the data that used to build a web page.

The auction site ebay.com also evolved from a monolithic architecture to a service-oriented architecture. The application tier consists of multiple independent applications. Each application implements the business logic for a specific function area such as buying or selling. Each application uses X-axis splits and some applications such as search use Z-axis splits. Ebay.com also applies a combination of X-, Y- and Z-style scaling to the database tier.

There are numerous other examples of companies using the microservice architecture.
