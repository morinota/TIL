## refs:

- https://continuousdelivery.com/foundations/

# Foundations

Continuous delivery rests on three foundations: comprehensive configuration management, continuous integration, and continuous testing.

In this section, you can read an overview of each of these foundations. You’ll also discover how to find out more about each of them, and find answers to some frequently-asked questions.

# Configuration Management

refs: https://continuousdelivery.com/foundations/configuration-management/

Automation plays a vital role in ensuring we can release software repeatably and reliably. One key goal is to take repetitive manual processes like build, deployment, regression testing and infrastructure provisioning, and automate them. In order to achieve this, we need to version control everything required to perform these processes, including source code, test and deployment scripts, infrastructure and application configuration information, and the many libraries and packages we depend upon. We also want to make it straightforward to query the current—and historical—state of our environments.

We have two overriding goals:

Reproducibility: We should be able to provision any environment in a fully automated fashion, and know that any new environment reproduced from the same configuration is identical.
Traceability: We should be able to pick any environment and be able to determine quickly and precisely the versions of every dependency used to create that environment. We also want to to be able to compare previous versions of an environment and see what has changed between them.

These capabilities give us several very important benefits:

Disaster recovery: When something goes wrong with one of our environments, for example a hardware failure or a security breach, we need to be able to reproduce that environment in a deterministic amount of time in order to be able to restore service.
Auditability: In order to demonstrate the integrity of the delivery process, we need to be able to show the path backwards from every deployment to the elements it came from, including their version. Comprehensive configuration management, combined with deployment pipelines, enable this.
Higher quality: The software delivery process is often subject to long delays waiting for development, testing and production environments to be prepared. When this can be done automatically from version control, we can get feedback on the impact of our changes much more rapidly, enabling us to build quality in to our software.
Capacity management: When we want to add more capacity to our environments, the ability to create new reproductions of existing servers is essential. This capability enables the horizontal scaling of modern cloud-based distributed systems.
Response to defects: When we discover a critical defect, or a vulnerability in some component of our system, we want to get a new version of our software released as quickly as possible. Many organizations have an emergency process for this type of change which goes faster by bypassing some of the testing and auditing. This presents an especially serious dilemma in safety-critical systems. Our goal should be to be able to use our normal release process for emergency fixes—which is precisely what continuous delivery enables, on the basis of comprehensive configuration management.
As environments become more complex and heterogeneous, it becomes progressively harder to achieve these goals. Achieving perfect reproducibility and traceability to the last byte for a complex enterprise system is impossible (apart from anything else, every real system has state). Thus a key part of configuration management is working to simplify our architecture, environments and processes to reduce the investment required to achieve the desired benefits.

When working to achieve the benefits, we should always start by defining in measurable terms the goals we want to achieve. This allows us to determine which of the possible paths to reach our goal are likely to be the best, and to change direction or reassess our goals if we discover our approach is going to be too expensive or take too long.

## Resources

My talk on lean configuration management
Kief Morris’ entry on ImmutableServer in Martin Fowler’s bliki is a good place to start, along with Kief’s forthcoming book.
Tom Limoncelli et al’s encyclopedic book The Practice of Cloud System Administration: Designing and Operating Large Distributed Systems, Volume 2
Pedro Canahuati on scaling operations at Facebook.

## FAQ

What tools should I use?

Tool choice is a complex topic, and in many cases (unless you use something wholly unsuitable) tool choice is not the critical factor in success. I recommend doing some research to whittle down a shortlist based on what technologies your team is familiar with, what has the widest level of usage, and what is under active development and support, and then setting a short-term goal and trying to achieve it using each of the tools on your shortlist.

How do containers / the cloud / virtualization technologies affect this topic?

The most important thing is that every new advance makes it easier and cheaper to achieve the benefits described. However in themselves, technologies such as containerization are not a silver bullet. For example, it’s not uncommon to see developers create “snowflake” containers whose contents are hard to audit or reproduce. We still need to apply the discipline of comprehensive use of version control and the deployment pipeline in order to achieve our goals.

# Continuous Integration

refs: https://continuousdelivery.com/foundations/continuous-integration/

Combining the work of multiple developers is hard. Software systems are complex, and an apparently simple, self-contained change to a single file can easily have unintended consequences which compromise the correctness of the system. As a result, some teams have developers work isolated from each other on their own branches, both to keep trunk / master stable, and to prevent them treading on each other’s toes.

However, over time these branches diverge from each other. While merging a single one of these branches into mainline is not usually troublesome, the work required to integrate multiple long-lived branches into mainline is usually painful, requiring significant amounts of re-work as conflicting assumptions of developers are revealed and must be resolved.

Teams using long-lived branches often require code freezes, or even integration and stabilization phases, as they work to integrate these branches prior to a release. Despite modern tooling, this process is still expensive and unpredictable. On teams larger than a few developers, the integration of multiple branches requires multiple rounds of regression testing and bug fixing to validate that the system will work as expected following these merges. This problem becomes exponentially more severe as team sizes grow, and as branches become more long-lived.

The practice of continuous integration was invented to address these problems. CI (continuous integration) follows the XP (extreme programming) principle that if something is painful, we should do it more often, and bring the pain forward. Thus in CI developers integrate all their work into trunk (also known as mainline or master) on a regular basis (at least daily). A set of automated tests is run both before and after the merge to validate that no regressions are introduced. If these automated tests fail, the team stops what they are doing and someone fixes the problem immediately.

Thus we ensure that the software is always in a working state, and that developer branches do not diverge significantly from trunk. The benefits of continuous integration are very significant—research shows that it leads to higher levels of throughput, more stable systems, and higher quality software. However the practice is still controversial, for two main reasons.

First, it requires developers to break up large features and other changes into smaller, more incremental steps that can be integrated into trunk / master. This is a paradigm shift for developers who are not used to working in this way. It also takes longer to get large features completed. However in general we don’t want to optimize for the speed at which developers can declare their work “dev complete” on a branch. Rather, we want to be able to get changes reviewed, integrated, tested and deployed as fast as possible—and this process is an order of magnitude faster and cheaper when the changes are small and self-contained, and the branches they live on are short-lived. Working in small batches also ensures developers get regular feedback on the impact of their work on the system as a whole—from other developers, testers, customers, and automated performance and security tests—which in turn makes any problems easier to detect, triage, and fix.

Second, continuous integration requires a fast-running set of comprehensive automated unit tests. These tests should be comprehensive enough to give a good level of confidence that the software will work as expected, while also running in a few minutes or less. If the automated unit tests take longer to run, developers will not want to run them frequently, and they will become harder to maintain. Creating maintainable suites of automated unit tests is complex and is best done through test-driven development (TDD), in which developers write failing automated tests before they implement the code that makes the tests pass. TDD has several benefits, the most important of which is that it ensures developers write code that is modular and easy to test, reducing the maintenance cost of the resulting automated test suites. But TDD is still not sufficiently widely practiced.

Despite these barriers, helping software development teams implement continuous integration should be the number one priority for any organization wanting to start the journey to continuous delivery. By creating rapid feedback loops and ensuring developers work in small batches, CI enables teams to build quality into their software, thus reducing the cost of ongoing software development, and increasing both the productivity of teams and the quality of the work they produce.

## Resources

Martin Fowler’s canonical article on Continuous Integration.
My personal favourite introduction, James Shore’s CI on a dollar a day.
Paul Hammant has a series of detailed articles describing how Amazon, Google, Facebook and others practice trunk-based development.
A video in which Google’s John Penix describes how Google practices CI at scale.
Paul Duvall’s book on Continuous Integration.

## FAQ

How do I know if my team is really doing CI?

I have a simple test I use to determine if teams are really practicing CI. 1) are all the engineers pushing their code into trunk / master (not feature branches) on a daily basis? 2) does every commit trigger a run of the unit tests? 3) When the build is broken, is it typically fixed within 10 minutes? If you can answer yes to all three questions, congratulations! You are practicing continuous integration. In my experience, less than 20% of teams that think they are doing CI can actually pass the test. Note that it’s entirely possible to do CI without using a CI tool, and conversely, just because you’re using a CI tool does not mean you are doing CI!

Don’t modern tools such as Git make CI unnecessary?

No. Distributed version control systems are an incredibly powerful tool that I fully endorse (and have been using since 2008). However like all powerful tools, they can be used in a multitude of ways, not all of them good. It’s perfectly possible to practice CI using Git, and indeed recommended for full-time teams. The main scenario where trunk-based development is not appropriate is open-source projects, where most contributors should be working on forks of the codebase rather than on master. There’s more discussion of CI and DVCS in a blog post I wrote on the topic.

Does trunk-based development mean using feature toggles?

No. Feature toggles are a new-fangled term for an old pattern: configuration options. In this context, we use them to hide from users features that are not “ready”, so we can continue to check in on trunk. However feature toggles are only really necessary when practicing continuous deployment, in which we release multiple times a day. For teams releasing every couple of weeks, or less frequently, they are unnecessary. There are, however, two important practices to enable trunk-based development without using feature toggles. First, we should build out our APIs before we create the user interface that relies on them. APIs (including automated tests running against them) can be created and deployed to production “dark” (that is, without anything calling them), enabling us to work on the implementation of a story on trunk. The UI (which should almost always be a thin layer over the API) is written last. Second, we should aim to break down large features into small stories (1-3 days’ work) in a way that they build upon each other iteratively, not incrementally. In this way, we ensure we can continue to release increments of the feature. Only in the cases where an iterative approach is not possible for some reason (and this is less often than you think, given sufficient imagination) do we need to introduce feature toggles.

What about GitHub-style development?

In general, I am fine with GitHub’s “flow” process—provided branches don’t live longer than a day or so. If you’re breaking features down into stories and practicing incremental development (see previous FAQ entry), this is not a problem. I also believe that code review should be done in process—ideally by inviting someone to pair with you (perhaps using screenhero if you’re working on a remote team) when you’re ready to check in, and reviewing the code then and there. Code review is best done continuously, and working in small batches enables this. Nobody enjoys reviewing pages and pages of diff that are the result of several day’s work because it’s impossible to reason about the impact of large changes on the system as a whole.

What tools should I use?

Tool choice is a complex topic, and in many cases (unless you use something wholly unsuitable) tool choice is not the critical factor in success. I recommend doing some research to whittle down a shortlist based on what technologies your team is familiar with, what has the widest level of usage, and what is under active development and support, and then setting a short-term goal and trying to achieve it using each of the tools on your shortlist.

# Continuous Testing

refs: https://continuousdelivery.com/foundations/test-automation/

The key to building quality into our software is making sure we can get fast feedback on the impact of changes. Traditionally, extensive use was made of manual inspection of code changes and manual testing (testers following documentation describing the steps required to test the various functions of the system) in order to demonstrate the correctness of the system. This type of testing was normally done in a phase following “dev complete”. However this strategy have several drawbacks:

Manual regression testing takes a long time and is relatively expensive to perform, creating a bottleneck that prevents us releasing software more frequently, and getting feedback to developers weeks (and sometimes months) after they wrote the code being tested.
Manual tests and inspections are not very reliable, since people are notoriously poor at performing repetitive tasks such as regression testing manually, and it is extremely hard to predict the impact of a set of changes on a complex software system through inspection.
When systems are evolving over time, as is the case in modern software products and services, we have to spend considerable effort updating test documentation to keep it up-to-date.
In order to build quality in to software, we need to adopt a different approach. Our goal is to run many different types of tests—both manual and automated—continually throughout the delivery process. The types of tests we want to run are nicely laid out the quadrant diagram created by Brian Marick, below:

Once we have continuous integration and test automation in place, we create a deployment pipeline (the key pattern in continuous delivery). In the deployment pipeline pattern, every change runs a build that a) creates packages that can be deployed to any environment and b) runs unit tests (and possibly other tasks such as static analysis), giving feedback to developers in the space of a few minutes. Packages that pass this set of tests have more comprehensive automated acceptance tests run against them. Once we have packages that pass all the automated tests, they are available for self-service deplyment to other environments for activities such as exploratory testing, usability testing, and ultimately release. Complex products and services may have sophisticated deployment pipelines; a simple, linear pipeline is shown below:

In the deployment pipeline, every change is effectively a release candidate. The job of the deployment pipeline is to catch known issues. If we can’t detect any known problems, we should feel totally comfortable releasing any packages that have gone through it. If we aren’t, or if we discover defects later, it means we need to improve our pipeline, perhaps adding or updating some tests.

Our goal should be to find problems as soon as possible, and make the lead time from check-in to release as short as possible. Thus we want to parallelize the activities in the deployment pipeline, not have many stages executing in series. There is also a feedback process: if we discover bugs in exploratory testing, we should be looking to improve our automated tests. If we discover a defect in the acceptance tests, we should be looking to improve our unit tests (most of our defects should be discovered through unit testing).

Get started by building a skeleton deployment pipeline—create a single unit test, a single acceptance test, an automated deployment script that stands up an exploratory testing envrionment, and thread them together. Then increase test coverage and extend your deployment pipeline as your product or service evolves.

## Resources

A 1h video in which Badri Janakiraman and I discuss how to create maintainable suites of automated acceptance test

Lisa Crispin and Janet Gregory have two great books on agile testing: Agile Testing and More Agile Testing

Elisabeth Hendrickson has written an excellent book on exploratory testing, Explore It!. I recorded an interview with her where we discuss the role of testers, acceptance test driven development, and the impact of continuous delivery on testing. Watch her awesome 30m talk On the Care and Feeding of Feedback Cycles.

Gojko Adzic’s Specification By Example has a series of interviews with successful teams worldwide and is a good distillation of effective patterns for specifying requirements and tests.

Think that “a few minutes” is optimistic for running automated tests? Read Dan Bodart’s blog post Crazy fast build times

Martin Fowler discusses the Test Pyramid and its evil twin, the ice cream cone on his bliki.

## FAQ

Does continuous delivery mean firing all our testers?

No. Testers have a unique perspective on the system—they understand how users interact with it. I recommend having testers pair alongside developers (in person) to help them create and evolve the suites of automated tests. This way, developers get to understand the testers’ perspective, and testers can start to learn test automation. Testers should also be performing exploratory testing continuously as part of their work. Certainly, testers will have to learn new skills—but that is true of anybody working in our industry.

Should we be automating all of our tests?

No. As shown in the quadrant diagram, there are still important manual activities such as exploratory testing and usability testing (although automation can help with these activities, it can’t replace people). We should be aiming to bring all test activities, including security testing, into the development process and performing them continually from the beginning of the software delivery lifecycle for every product and service we build.

Should I stop and automate all of my manual tests right now?

No. Start by writing a couple of automated tests—the ones that validate the most important functionality in the system. Get those running on every commit. Then the rule is to add new tests to cover new functionality that is added, and functionality that is being changed. Over time, you will evolve a comprehensive suite of automated tests. In general, it’s better to have 20 tests that run quickly and are trusted by the team than 2,000 tests that are flaky and constantly failing and which are ignored by the team.

Who is responsible for the automated tests?

The whole team. In particular, developers should be involved in creating and maintaining the automated tests, and should stop what they are doing and fix them whenever there is a failure. This is essential because it teaches developers how to write testable software. When automated tests are created and maintained by a different group from the developers, there is no force acting on the developers to help them write software that is easy to test. Retrofitting automated tests onto such systems is painful and expensive, and poorly designed software that is hard to test is a major factor contributing to automated test suites that are expensive to maintain.
