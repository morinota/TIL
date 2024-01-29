## link

https://booking.ai/how-good-are-your-ml-best-practices-fd7722262437

# How good are your ML best practices?

## Introduction

In Software engineering, best practices serve as an important part of the discussion on how to develop good quality software, which can be easily maintained, scaled, extended, and tested. Why do we mention maintenance, scalability, extendability or testing? These are only a few of the possible attributes you might wish to consider when defining quality for your particular software product. There are many more, and they heavily depend on your use case. Machine Learning Systems pose their own specific challenges, that is why we developed a Quality Model for machine learning.

Having defined the quality model and attributes of interest, we can start thinking about what best practices we can apply, to cover these attributes. The list of possible best practices one might apply is extensive, and there are many resources available such as [3], [4], [5]. These lists can seem overwhelming, and in reality not all of them can be always applied to the fullest extent. It usually is required to prioritise one over the other, and there has been little discussion on how to perform such prioritisation. Additionally a single practice can contribute to many attributes, so how can we choose the right combination of best practices to cover the attributes we need to fulfil.

For example, if you had to choose only 5 of best practices from [3], which would you choose and why, given your constraints and requirements? To answer this question, we propose a framework to prioritise best practices.

## The elements of the prioritisation framework

The goal of applying best practices is to improve the quality of your ML system. But how do we define quality?

The standard approach to define quality in software is the use of Quality Models. “A quality model provides the framework towards a definition of quality” [1]. It is the set of characteristics and the relationships between them that provides the basis for specifying quality requirements and evaluation [2]. There does not exist a Quality Model for Machine Learning Systems, that’s why we introduced our own.

Once the Quality Model is defined and we understand what attributes (sub-characteristics in our model) of software we need to cover, we need a set of best practices which we can apply. Adopting a best practice can bring us closer to solving a particular sub-characteristic, or it can completely solve it — it depends on the best practice and the extent to which it has been implemented. For example, writing complete documentation with all the important assumptions made during the development of an ML system can fully solve Understandability but can also improve Repeatability since documentation makes it easier to repeat the lifecycle of a given ML system

The extent of implementation and the number of best practices we can afford to implement depends on the designated effort budget and desired quality coverage, something that varies a lot between projects.

We built a list of best practices from external resources such as [3], [4], [5] and surveyed our Machine Learning community and conducted interviews with practitioners, to find out which best practices are used in our company.

## Quality Model meets Best Practices

Once the Quality Model has been built and the list of best practices has been established, the missing link is the relationship between each quality model sub-characteristic and the individual best practices. To give an example, if we remove all redundant features from our Machine Learning System , do we solve the Accuracy of the system? Does testability improve? Does our system scale better, or is it easier to Monitor? To answer these questions, we need a mapping from a (sub-characteristic, best practice) pair to a number that represents how much the sub-characteristic benefits from the best-practice. We decided to use a scale of 0–4, where 0 means that a particular sub-characteristic has no relevance to a given best practice, and 4 means that a particular sub-characteristic is covered (meaning that is completely addressed) by a given best practice. We assume the scores are additive. If a sub-characteristic is covered, i.e. we apply best practices whose contributions sum up to 4, we assume more work on this particular sub-characteristic is not necessary.

## Score elicitation

To obtain the scores for the (sub-characteristic, best practice) pairs , we organised a training for experienced machine learning practitioners (machine learning scientists, and engineers) on the quality model and best practices to make sure both are well understood and then asked them for scores for each possible (sub-characteristic, best practice) pair. To verify that these scores are consistent, we computed inter-annotator agreement, which proved a good agreement between the practitioners (see section 4.3 Inter-annotator Agreement in our paper). The final relationship of a (sub-characteristic, best practice) is computed using a statistic of the collected scores such as mean or median.

## Which practices should I choose?

Having obtained the relationship between a quality model and best practices, we can solve the problem of which practices should I select, given a budget expressed in the number of practices and a subset of quality sub-characteristics (we might be interested in not solving all of them, e.g. a proof of concept system might not care about scalability).

​​The objective of our optimization problem is to choose a subset of practices that maximizes the coverage of the quality model under a budget constraint.

## Optimisation algorithms

To solve the optimization problem of finding the set of practices that maximises the quality coverage we consider 2 algorithms: a) brute force and b) greedy. The brute force algorithm very quickly leads to a combinatorial explosion of the search space even for a small number of practices and budget, hence in practice we use the greedy algorithm for which we found that rarely yields sub-optimal results and is much faster. You can find the exact algorithms in our paper.

## Applications

Ok, we have a framework that we can use to score and prioritize best practices. But what can we do with it? Below we provide three applications of the framework which helped us get a better understanding of ML best practices.

### #1: Analyzing sets of best practices

An application of our framework is to analyze sets of best practices. Given a set of practices, we can score each practice against each quality sub-characteristic and then visualize the total contributions of the sub-characteristics to assess which sub-characteristics receive a lot of attention and which are underrepresented.

We do this exercise for the internal set of 41 practices that we apply at Booking.com and we can see the results in the figure below. In the figure we marked the threshold k=24 contribution points which we used for indicating if a sub-characteristic is covered (for more details refer to the Section 4.2 of the paper).

From the figure we see that while most of the sub-characteristics are covered, there are a few which are not, such as standards-compliance, scalability or discoverability. This insight helped us identify gaps in our set of practices and helped us create new ones that can address those gaps. We also got our first learning:

Learning #1: We can identify gaps in sets of practices, by analyzing their coverage on each quality sub-characteristic.

Some examples of practices that we created are:

To address the gap in Vulnerability, we created an ML security inspection process and we created a practice called “Request an ML system security inspection”.

To address the gap in Responsiveness, we created the practice: “Latency and throughput requirements are defined”, which means that the model builder should be aware of latency and throughput requirements when developing.

To address the gap in Discoverability, we created the practice: “Register the ML system in an accessible registry” and we made sure that all the systems are being registered and visible.

We also did this exercise using 3 open source sets of practices ([3], [4], [5]) and we found that while each set in isolation covers only a subset of the sub-characteristics, when combined, they complement each other! You can find the details in our paper.

### #2: Assessing how many practices are enough

The second exercise we did is to find how many practices are needed in order to maximize the quality coverage. To do this, we combined the 3 open source with the internal set of practices (after removing those that overlap) and we ended up with 101 practices in total. We then find the top N practices from the combined set using our greedy algorithm, for N increasing from 1 to 101, and compute the coverage percentage for each N, which we plot in the figure below.

We find that by applying 5 practices, we already cover 40% of the sub-characteristics, 10 practices cover 70% and 24 are needed to cover 96% which is the maximum (we do not reach 100% because discoverability is never fully covered even if we combine all the sets). This means that by using 24 practices, we achieve a similar result in terms of quality as with 101 practices! This is because many practices overlap in terms of the quality attributes they contribute to, which leads us to our second learning:

Learning #2: When applying the right set of practices, we can achieve a significant reduction in the effort of adoption!

#3: Identifying the best of the best practices
Since we can identify how many practices are enough to maximize the quality coverage, we can also find which are actually those practices. To do this, we run the greedy algorithm using as budget 24 practices, and we find that the ones the set which maximizes coverage is the following:

Versioning for Data, Model, Configurations and Scripts [5]
Continuously Monitor the Behaviour of Deployed Models [5]
Unifying and automating ML workflow [4]
Remove redundant features [3]
Continuously Measure Model Quality and Performance [5]
All input feature code is tested [3]
Automate Model Deployment [5]
Use of Containarized Environment [6]
Unified Environment for all Lifecycle Steps [6]
Enable Shadow Deployment [5]
The ML system outperforms a simple baseline [3]
Have Your Application Audited [5]
Monitor model staleness [3]
Use A Collaborative Development Platform [5]
Explain Results and Decisions to Users [5]
The ML system has a clear owner [6]
Assign an Owner to Each Feature and Document its Rationale [5]
Computing performance has not regressed [3]
Communicate, Align, and Collaborate With Others [5]
Perform Risk Assessments [5]
Peer Review Training Scripts [5]
Establish Responsible AI Values [5]
Write documentation about the ML system [6]
Write Modular and Reusable Code [6]
Using this set we can narrow down which practices we should prioritize pushing forward in our organization in order to ensure holistic quality coverage and avoid the adoption of practices aiming at the same goals. We should note though that to create this optimal set, we considered equal importance for each sub-characteristic and the same adoption effort per practice, so we advise careful adoption of this set with consideration of your organization’s needs. For example, if safety is top priority, practices focusing on robustness should be prioritized. This takes us to our last learning:

Learning #3: The optimal set of practices for an organization is possible to be specified, however it depends on the exact organization’s needs.

## Conclusion

Adopting practices at random or based on their popularity is sub-optimal since each practice targets different quality sub-characteristics and in many cases they overlap. Due to this, we implemented a framework to analyze and prioritize machine learning practices and we used it to identify gaps in the practices we have adopted at Booking.com. We also found that even though there is a proliferation of machine learning best practices, only a few are needed to achieve high coverage of all quality aspects.

If you want to learn more, you can read our full paper at and you can also use the code of the framework in our Github page. We are always more than happy to discuss any thoughts or feedback on the framework, so don’t hesitate to reach out.
