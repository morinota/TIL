## link

- https://neptune.ai/blog/organizing-ml-monorepo-with-pants

# Organizing ML Monorepo With Pants

Have you ever copy-pasted chunks of utility code between projects, resulting in multiple versions of the same code living in different repositories? Or, perhaps, you had to make pull requests to tens of projects after the name of the GCP bucket in which you store your data was updated?

Situations described above arise way too often in ML teams, and their consequences vary from a single developer’s annoyance to the team’s inability to ship their code as needed. Luckily, there’s a remedy.

Let’s dive into the world of monorepos, an architecture widely adopted in major tech companies like Google, and how they can enhance your ML workflows. A monorepo offers a plethora of advantages which, despite some drawbacks, make it a compelling choice for managing complex machine learning ecosystems.

We will briefly debate monorepos’ merits and demerits, examine why it’s an excellent architecture choice for machine learning teams, and peek into how BigTech is using it. Finally, we’ll see how to harness the power of the Pants build system to organize your machine learning monorepo into a robust CI/CD build system.

Strap in as we embark on this journey to streamline your ML project management.

# What is a monorepo?

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/Monorepo.png?resize=1536%2C1536&ssl=1)

A monorepo (short for monolithic repository) is a software development strategy where code for many projects is stored in the same repository. The idea can be as broad as all of the company code written in a variety of programming languages stored together (did somebody say Google?) or as narrow as a couple of Python projects developed by a small team thrown into a single repository.

In this blog post, we focus on repositories storing machine learning code.

# Monorepos vs. polyrepos

Monorepos are in stark contrast to the polyrepos approach, where each individual project or component has its own separate repository. A lot has been said about the advantages and disadvantages of both approaches, and we won’t go down this rabbit hole too deep. Let’s just put the basics on the table.

The monorepo architecture offers the following advantages:

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/Monorepos-vs.-polyrepos-1.png?resize=1536%2C804&ssl=1)

- Single CI/CD pipeline, meaning no hidden deployment knowledge spread across individual contributors to different repositories;
- Atomic commits, given that all projects reside in the same repository, developers can make cross-project changes that span across multiple projects but are merged as a single commit;
- Easy sharing of utilities and templates across projects;Easy unification of coding standards and approaches;
- Better code discoverability.

Naturally, there are no free lunches. We need to pay for the above goodies, and the price comes in the form of:

- Scalability challenges: As the codebase grows, managing a monorepo can become increasingly difficult. At a really large scale, you’ll need powerful tools and servers to handle operations like cloning, pulling, and pushing changes, which can take a significant amount of time and resources.
- Complexity: A monorepo can be more complex to manage, particularly with regard to dependencies and versioning. A change in a shared component could potentially impact many projects, so extra caution is needed to avoid breaking changes.
- Visibility and access control: With everyone working out of the same repository, it can be difficult to control who has access to what. While not a disadvantage as such, it could pose problems of a legal nature in cases where code is subject to a very strict NDA.

The decision as to whether the advantages a monorepo offers are worth paying the price is to be determined by each organization or team individually. However, unless you are operating at a prohibitively large scale or are dealing with top-secret missions, I would argue that – at least when it comes to my area of expertise, the machine learning projects – a monorepo is a good architecture choice in most cases.

Let’s talk about why that is.

# Machine learning with monorepos

There are at least six reasons why monorepos are particularly suitable for machine learning projects.

1. Data pipeline integration
2. Consistency across experiments
3. Simplified model versioning
4. Cross-functional collaboration
5. Atomic changes
6. Unification of coding standards

## Data pipeline integration

Machine learning projects often involve data pipelines that preprocess, transform, and feed data into the model. These pipelines might be tightly integrated with the ML code. Keeping the data pipelines and ML code in the same repo helps maintain this tight integration and streamline the workflow.

## Consistency across experiments

Machine learning development involves a lot of experimentation. Having all experiments in a monorepo ensures consistent environment setups and reduces the risk of discrepancies between different experiments due to varying code or data versions.

## Simplified model versioning

In a monorepo, the code and model versions are in sync because they are checked into the same repository. This makes it easier to manage and trace model versions, which can be especially important in projects where ML reproducibility is critical.

Just take the commit SHA at any given point in time, and it gives the information on the state of all models and services.

## Cross-functional collaboration

Machine learning projects often involve collaboration between data scientists, ML engineers, and software engineers. A monorepo facilitates this cross-functional collaboration by providing a single source of truth for all project-related code and resources.

## Atomic changes

In the context of ML, a model’s performance can depend on various interconnected factors like data preprocessing, feature extraction, model architecture, and post-processing. A monorepo allows for atomic changes – a change to multiple of these components can be committed as one, ensuring that interdependencies are always in sync.

## Unification of coding standards

Finally, machine learning teams often include members without a software engineering background. These mathematicians, statisticians, and econometricians are brainy folks with brilliant ideas and the skills to train models that solve business problems. However, writing code that is clean, easy to read, and maintain might not always be their strongest side.

A monorepo helps by automatically checking and enforcing coding standards across all projects, which not only ensures high code quality but also helps the less engineering-inclined team members learn and grow.

# How they do it in industry: famous monorepos

In the software development landscape, some of the largest and most successful companies in the world use monorepos. Here are a few notable examples.

- Google: Google has long been a staunch advocate for the monorepo approach. Their entire codebase, estimated to contain 2 billion lines of code, is contained in a single, massive repository. They even published a paper about it.
- Meta: Meta also employs a monorepo for their vast codebase. They created a version control system called “Mercurial” to handle the size and complexity of their monorepo.
- Twitter: Twitter has been managing their monorepo for a long time using Pants, the build system we will talk about next!

Many other companies such as Microsoft, Uber, Airbnb, and Stripe are using the monorepo approach at least for some parts of their codebases, too.

Enough of the theory! Let’s take a look at how to actually build a machine learning monorepo. Because just throwing what used to be separate repositories into one folder does not do the job.

# How to set up ML monorepo with Python?

Throughout this section, we will base our discussion on a sample machine learning repository I’ve created for this article. It is a simple monorepo holding just one project, or module: a hand-written digits classifier called mnist, after the famous dataset it uses.

All you need to know right now is that in the monorepo’s root there is a directory called mnist, and in it, there is some Python code for training the model, the corresponding unit tests, and a Dockerfile to run training in a container.

We will be using this small example to keep things simple, but in a larger monorepo, mnist would be just one of the many project folders in the repo’s root, each of which will contain source code, tests, dockerfiles, and requirement files at the least.

## Build system: Why do you need one and how to choose it?

### The Why?

Think about all the actions, other than writing code, that the different teams developing different projects within the monorepo take as part of their development workflow. They would run linters against their code to ensure adherence to style standards, run unit tests, build artifacts such as docker containers and Python wheels, push them to external artifact repositories, and deploy them to production.

### Take testing.

You’ve made a change in a utility function you maintain, ran the tests, and all’s green. But how can you be sure your change is not breaking code for other teams that might be importing your utility? You should run their test suite, too, of course.

But to do this, you need to know exactly where the code you changed is being used. As the codebase grows, finding this out manually doesn’t scale well. Of course, as an alternative, you can always execute all the tests, but again: that approach doesn’t scale very well.

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/2.png?resize=1536%2C804&ssl=1)

### Another example, production deployment.

Whether you deploy weekly, daily, or continuously, when the time comes, you would build all the services in the monorepo and push them to production. But hey, do you need to build all of them on each occasion? That could be time-consuming and expensive at scale.

Some projects might not have been updated for weeks. On the other hand, the shared utility code they use might have received updates. How do we decide what to build? Again, it’s all about dependencies. Ideally, we would only build services that have been affected by the recent changes.

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/1.png?resize=1536%2C804&ssl=1)

All of this can be handled with a simple shell script with a small codebase, but as it scales and projects start sharing code, challenges emerge, many of which revolve around dependency management.

### Picking the right system

All of the above is not a problem anymore if you invest in a proper build system. A build system’s primary task is to build code. And it should do so in a clever way: the developer should only need to tell it what to build (“build docker images affected by my latest commit”, or “run only those tests that cover code which uses the method I’ve updated”), but the how should be left for the system to figure out.

There are a couple of great open-source build systems out there. Since most machine learning is done in Python, let’s focus on the ones with the best Python support. The two most popular choices in this regard are Bazel and Pants.

Bazel is an open-source version of Google’s internal build system, Blaze. Pants is also heavily inspired by Blaze and it aims for similar technical design goals as Bazel. An interested reader will find a good comparison of Pants vs. Bazel in this blog post (but keep in mind it comes from the Pants devs). The table at the bottom of monorepo.tools offers yet another comparison.

Both systems are great, and it is not my intention to declare a “better” solution here. That being said, Pants is often described as easier to set up, more approachable, and well-optimized for Python, which makes it a perfect fit for machine learning monorepos.

In my personal experience, the decisive factor that made me go with Pants was its active and helpful community. Whenever you have questions or doubts, just post on the community Slack channel, and a bunch of supportive folks will help you out soon.

## Introducing Pants

Alright, time to get to the meat of it! We will go step by step, introducing different Pants’ functionalities and how to implement them. Again, you can check out the associated sample repo here.

### Setup

Pants is installable with pip. In this tutorial, we will use the most recent stable version as of this writing, 2.15.1.

```
pip install pantsbuild.pants==2.15.1
```

Pants is configurable through a global master config file named pants.toml. In it, we can configure Pants’ own behavior as well as the settings of downstream tools it relies on, such as pytest or mypy.

Let’s start with a bare minimum pants.toml:

```
[GLOBAL]
pants_version = "2.15.1"
backend_packages = [
    "pants.backend.python",
]

[source]
root_patterns = ["/"]

[python]
interpreter_constraints = ["==3.9.*"]
```

In the global section, we define the Pants version and the backend packages we need. These packages are Pants’ engines that support different features. For starters, we only include the Python backend.

In the source section, we set the source to the repository’s root. Since version 2.15, to make sure this is picked up, we also need to add an empty BUILD_ROOT file at the repository’s root.

Finally, in the Python section, we choose the Python version to use. Pants will browse our system in search of a version that matches the conditions specified here, so make sure you have this version installed.

That’s a start! Next, let’s take a look at any build system’s heart: the BUILD files.

### Build files

Build files are configuration files used to define targets (what to build) and their dependencies (what they need to work) in a declarative way.

You can have multiple build files at different levels of the directory tree. The more there are, the more granular the control over dependency management. In fact, Google has a build file in virtually every directory in their repo.

In our example, we will use three build files:

- mnist/BUILD – in the project directory, this build file will define the python requirements for the project and the docker container to build;
- mnist/src/BUILD – in the source code directory, this build file will define python sources, that is, files to be covered by python-specific checks;
- mnist/tests/BUILD – in the tests directory, this build file will define which files to run with Pytest and what dependencies are needed for these tests to run.

Let’s take a look at the mnist/src/BUILD:

```
python_sources(
    name="python",
    resolve="mnist",
    sources=["**/*.py"],
)
```

At the same time, mnist/BUILD looks like this:

```
python_requirements(
    name="reqs",
    source="requirements.txt",
    resolve="mnist",
)
```

The two entries in the build files are referred to as targets. First, we have a Python sources target, which we aptly call python, although the name could be anything. We define our Python sources as all .py files in the directory. This is relative to the build file’s location, that is: even if we had Python files outside of the mnist/src directory, these sources only capture the contents of the mnist/src folder. There is also a resolve filed; we will talk about it in a moment.

Next, we have the Python requirements target. It tells Pants where to find the requirements needed to execute our Python code (again, relative to the build file’s location, which is in the mnist project’s root in this case).

This is all we need to get started. To make sure the build file definition is correct, let’s run:

```
pants tailor --check update-build-files --check ::
```

As expected, we get: “No required changes to BUILD files found.” as the output. Good!

Let’s spend a bit more time on this command. In a nutshell, a bare pants tailor can automatically create build files. However, it sometimes tends to add too many for one’s needs, which is why I tend to add them manually, followed by the command above that checks their correctness.

The double semicolon at the end is a Pants notation that tells it to run the command over the entire monorepo. Alternatively, we could have replaced it with mnist: to run only against the mnist module.

### Dependencies and lockfiles

To do efficient dependency management, pants relies on lockfiles. Lockfiles record the specific versions and sources of all dependencies used by each project. This includes both direct and transitive dependencies.

By capturing this information, lockfiles ensure that the same versions of dependencies are used consistently across different environments and builds. In other words, they serve as a snapshot of the dependency graph, ensuring reproducibility and consistency across builds.

To generate a lockfile for our mnist module, we need the following addition to pants.toml:

```
[python]
interpreter_constraints = ["==3.9.*"]
enable_resolves = true
default_resolve = "mnist"

[python.resolves]
mnist = "mnist/mnist.lock"
```

We enable the resolves (Pants term for lockfiles’ environments) and define one for mnist passing a file path. We also choose it as the default one. This is the resolve we have passed to Python sources and Python requirements target before: this is how they know what dependencies are needed. We can now run:

to get:

This has created a file at mnist/mnist.lock. This file should be checked with git if you intend to use Pants for your remote CI/CD. And naturally, it needs to be updated every time you update the requirements.txt file.

With more projects in the monorepo, you would rather generate the lockfiles selectively for the project that needs it, e.g. pants generate-lockfiles mnist: .

That’s it for the setup! Now let’s use Pants to do something useful for us.

### Unifying code style with Pants

Pants natively supports a number of Python linters and code formatting tools such as Black, yapf, Docformatter, Autoflake, Flake8, isort, Pyupgrade, or Bandit. They are all used in the same way; in our example, let’s implement Black and Docformatter.

To do so, we add appropriate two backends to pants.toml:
