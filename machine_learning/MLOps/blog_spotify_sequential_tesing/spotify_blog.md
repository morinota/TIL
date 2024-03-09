## link

- https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions/

# Choosing a Sequential Testing Framework — Comparisons and Discussions

## TL;DR

Sequential tests are the bread and butter for any company conducting online experiments. The literature on sequential testing has developed quickly over the last 10 years, and it’s not always easy to determine which test is most suitable for the setup of your company — many of these tests are “optimal” in some sense, and most leading A/B testing companies have their own favorite. Even though the sequential testing literature is blooming, there is surprisingly little advice available (we have only found this blog post) on how to choose between the different sequential tests. With this blog post we aim to share our reasoning around this choice.

Spotify’s Experimentation Platform uses so-called group sequential tests (GSTs). In this post, we highlight some of the pros and cons of our chosen method using simulation results. We conclude that two main parameters should affect your choice of sequential analysis tool:

If your data infrastructure provides data in batch or streaming.
If you can make reasonable estimates of the maximum sample size an experiment will reach.
We show that when you can estimate the maximum sample size that an experiment will reach, GST is the approach that gives you the highest power, regardless of whether your data is streamed or comes in batches.

## Solid experimentation practices ensure valid risk management

Experimentation lets us be bold in our ideas. We can iterate faster and try new things to identify what changes resonate with our users. Spotify takes an evidence-driven approach to the product development cycle by having a scientific mindset in our experimentation practices. Ultimately, this means limiting the risk of making poor product decisions.

From a product decision perspective, the risks we face include shipping changes that don’t have a positive impact on the user experience, or missing out on shipping changes that do, in fact, lead to a better user experience. In data science jargon, these mistakes are often called “false positives” and “false negatives.” The frequency at which these mistakes occur in repeated experimentation is the false positive or false negative rate. The intended false positive rate is often referred to as “alpha.” By properly designing the experiment, these rates can be controlled. In Spotify’s Experimentation Platform, we’ve gone to great lengths to ensure that our experimenters can have complete trust that these risks will be managed as the experimenter intended.

## Peeking is a common source of unintended risk inflation

One of the most common sources of incorrect risk management in experimentation is often referred to as “peeking.” Most standard statistical tests — like z-tests or t-tests — are constructed in a way that limits the risks only if the tests are used after the data collection phase is over. Peeking inflates the false positive rate because these nonsequential (standard) tests are applied repeatedly during the data collection phase. For example, imagine that we’re running an experiment on 1,000 users split evenly into a control group and a treatment group. We use a z-test to see if there’s a significant difference between the treatment group and the control group in terms of, for example, minutes played on Spotify. After collecting a new pair of observations from both groups, we apply our test. If we don’t find a significant difference, we proceed to collect another pair of observations and repeat the test. With this design, the overall false positive rate is the probability of finding a false positive in any of the tests we conduct. After we’ve conducted the first two tests, a false positive can be obtained in the first test or in the second test, given that the first test was negative. With a z-test constructed to yield a 5% false positive rate if used once, the true false positive rate that the experimenter faces is in fact closer to 10%, since the two tests give us two opportunities to find a significant effect. The figure below shows how the false positive rate intended to be at 5% grows if we continue as in the previous example: collect a new pair of observations, test for an effect, and if not significant, continue and collect another pair of observations and test again. The true false positive rate grows quickly, and after repeated tests the experimenter encounters a true false positive rate that severely exceeds the intended 5% rate.

## Sequential tests solve the peeking problem

While uncontrolled peeking must be avoided, it’s also important to monitor regressions while collecting data for experiments. A main objective of experimentation is to know early on if end users are negatively affected by the experience being tested. To do this, we need a way to control the risk of raising false alarms, as well as the risk of failing to raise the alarm when something is, in fact, affecting the end-user experience negatively.

To solve the peeking problem, we can leverage a wide class of statistical tests known as sequential tests. These tests account for the sequential and recurrent nature of testing in different ways, depending on their specific implementations. They all let us repeatedly test the same hypothesis while data is being collected, without inflating the false positive rate. Different tests come with different requirements — some require us to estimate the total number of observations that the test will include in the end, and some don’t. Some are better suited when data arrives in batches (for example, once per day), and some when data is available in real time. In the next section, we provide a short, nonexhaustive overview of the current sequential testing landscape where we focus on tests that are well-known. Furthermore, we concentrate on the power of these tests, specifically, the rate of rejecting the null hypothesis that there is no difference in means between treatment and control for some metric of interest, given the alternative hypothesis of a nonzero difference.

The methods we study are:

The group sequential test (GST). At Spotify, we use the GST with alpha spending as proposed by Lan and DeMets (1983).
Two versions of always valid inference (AVI):
The mixture sequential probability ratio test (mSPRT). Popularized, used, and extended by Optimizely, Uber, Netflix, and Amplitude, for example.  
The generalization of always valid inference (GAVI), as proposed by Howard et al. (2021). Used by Eppo, for example.
The corrected-alpha approach (CAA). Used and proposed by Statsig.
A naive approach using Bonferroni corrections as a baseline (benchmark).
Below, we briefly go through the tests one by one. The purpose is not to present the technical or mathematical details but rather to highlight the properties and limitations of each framework.

### Group sequential tests

Group sequential tests can be viewed as consecutive applications of traditional tests like the z-test. The GST exploits the known correlation structure between intermittent tests to optimally account for the fact that we are testing multiple times. For detailed introduction see e.g. Kim and Tsiatis (2020) and Jennison and Turnbull (1999).

Pros:

Using the alpha-spending approach, alpha can be spent arbitrarily over the times you decide to peek, and you only spend alpha when you peek — if you skip one peek, you can save that unused alpha for later. Moreover, you don’t have to decide in advance how many tests you run or at what time during the data collection you run them. If you do not peek at all during the data collection, the test once the data collection phase is over is exactly the traditional z-test.
Easy to explain due to the relation with z-tests.
Cons:

You need to know or be able to estimate the maximum sample size in advance. If you observe fewer users than expected, the test will be conservative and the true false positive rate will be lower than intended. If you keep observing new users after you have reached the expected total amount, the test will have an inflated false positive rate.
You need to select an alpha spending function. If you always reach the planned sample size, this choice is not critical, but if you undersample and observe too few users, the choice of spending function can affect the power properties substantially.
The critical values used in the test need to be obtained by solving integrals numerically. This numerical problem becomes more challenging with many intermittent analyses, and it is therefore not feasible to use GST in a streaming fashion, i.e., run more than a few hundred intermittent analyses for one experiment.

### Always valid inference

Always valid inference tests allow for continuous testing during data collection without deciding in advance on a stopping rule or the number of intermittent analyses. We present both mSPRT and GAVI, but mSPRT is essentially a special case of GAVI, and the pros and cons are the same. For details see e.g. Howard et al. (2021) or Lindon et al. (2022).

Pros:

Easy to implement.
Allows unlimited sampling and no expected sample size is required in advance.
Allows arbitrary stopping rules.
Supports streaming and batch data.
Cons:

Requires the experimenter to choose parameters of the mixing distribution, i.e., the distribution that describes the effect under the alternative hypothesis. This choice affects the statistical properties of the test and is nontrivial. If the approximate expected sample size is known, it can be used to select the parameter, but then the pro of not having to know the sample size is lost.
Harder to understand for folks trained in traditional hypothesis testing. It will probably take a while before intro courses in statistics cover these tests.
Has by construction less power when analyzing data in batch compared to streaming.

### Bonferroni corrections

If we have an upper bound for how many intermittent analyses we want to make, we can solve the peeking problem by selecting a conservative approach. We can bound the false positive rate by adjusting for multiple comparisons using Bonferroni corrections, where we use a standard z-test but with alpha divided by the number of intermittent analyses. Since the test statistic is highly correlated over repeated testing, the Bonferroni approach is conservative by construction.

Pros:

Easy to implement and explain.
Cons:

You have to decide the maximum number of intermittent analyses in advance.
With many intermittent analyses, the test will become highly conservative with low power as a consequence.

### Corrected-alpha approach

Statsig proposed a simple adjustment that reduces the false positive inflation rate from peeking. The approach does not solve the peeking problem in the sense that the false positive rate under peeking is bounded below the target level (alpha) but substantially limits the inflation itself.

Pros:

Easy to use.
Cons:

Does not bound the false positive rate and, therefore, does not solve the peeking problem.
The actual false positive rate depends on the sample size and number of intermittent analyses — which might be hard for experimenters to understand.

### How data is delivered affects the choice of test

Most companies running online experiments have data infrastructure that supports either batch or streaming data (or both). In the context of online experimentation, batch data implies that analysis can, at most, be done each time a new batch of data is delivered. At Spotify, most data jobs are run daily, implying one analysis per day during an experiment. As the name indicates, the group sequential test is built for use with batches (groups) of data. If the number of intermittent analyses adds up to more than a few hundred, the test will no longer be a feasible option due to increasingly complex numerical integrations. Most experiments at Spotify run for a few weeks at most, and our data arrives in batches, which means that the GST is a good fit for our experimentation environment.

Streaming data, on the other hand, allows us to analyze results after each new observation. In other words, there can be as many analyses as there are observations in the sample. The AVI family of tests can be computed as soon as a new observation comes in. In fact, to utilize their full potential to find significant results, AVI tests should ideally be used with streaming data. While streaming data is favorable, they can also handle batch data by simply skipping the intermittent analyses. This will, however, inevitably make the AVI tests conservative to some extent, as most of the chances for false positive results are never considered. We come back to this point in the simulation study below.

## Evaluating the efficacy of sequential tests by their false positive rates and statistical power

There are two important properties by which we assess the usefulness and effectiveness of the sequential tests:

A bounded false positive rate: The first and most important property for a sequential test is that it solves the peeking problem. That is, the false positive rate should not be above the intended rate (alpha) even in the presence of peeking.
High power/sensitivity: The second property is the power or sensitivity for a test, i.e., how often we reject the null hypothesis when it is not true. As often as possible, we want our test to identify effects when they are there and reject the null hypothesis when it is not true.
We acknowledge that these tests could be evaluated from many additional angles, for example what type of test statistics they can be used together with and what their small-sample properties are. In our experience, power and false positive rate are the most important aspects, and thus a good starting point for comparing.

Of the five tests mentioned above, all but the corrected-alpha approach (CAA) fulfill the first criterion of a bounded false positive rate. The CAA test is constructed in such a way that the overall false positive rate is strictly larger than alpha if any peeking is performed during data collection. The level of inflation depends on how often you peek and how large the total sample size is, as our results below reveal. Since it doesn’t bound the false positive rate under peeking, we don’t view CAA as a proper sequential test and will leave it out of the power comparison.

All other tests by construction bound the false positive rate to alpha or lower if used as intended but differ in power/sensitivity. However, these tests are also optimized to have sensitivity for different settings that we discuss further in the next section.

## Monte Carlo simulation study

To build intuition for the important trade-offs when selecting between the sequential tests discussed above, we perform a small Monte Carlo simulation study.

To keep this post short, some of the details of the setup are left out. Please refer to the replication code for details. All data in the simulation is generated from a normal distribution with mean 1 (+ treatment effect under treatment) and variance 1. The sample size is balanced between treatment and control with 500 observations in each group. We run 100,000 replications for each combination of parameters. We use one-sided tests with the intended false positive rate (alpha) set to 5%. All statistical assumptions of all tests are fulfilled by construction without the need for large samples. For all simulations we vary the number of intermittent analyses. We conduct 14, 28, 42, or 56 evenly spaced analyses, or analyze results in a streaming fashion. The latter corresponds to 500 intermittent analyses in this case. Note that stream is not calculated for the GSTs since this is not plausible for the sample sizes typically handled in online experimentation.

We obtain bounds for the GST using the ldbounds R package, where we vary the expected sample size parameter [n]. We implement the GAVI test according to Eppo’s documentation, where we vary the numerator of the tuning parameter [rho]. The version of the mSPRT that we use follows the generalization presented by Lindon et al. (2022). We consider only the one-dimensional case and vary the tuning parameter [phi]. For CAA, we follow the procedure outlined in Statsig’s documentation.

We first focus on the false positive rate and then compare power under various settings for the tests that properly bound the false positive rate.

### False positive rate

For the empirical false positive rate simulation, we consider the following tests and variants of tests:

GST
We apply the test with (1) a correctly assumed sample size, (2) a 50% underestimated sample size (i.e., we wrongly assumed a too low maximum sample size 500, but the real observed final sample size was 750), and (3) a 50% overestimated sample size (i.e., we assumed a too high sample size 500, but the real sample size was 250). When we oversample and obtain more observations than expected, we apply the correction to the bounds proposed in Wassmer and Brannath (2016), pages 78–79.
We use two versions of the so-called power family alpha spending function that are either quadratic or cubic in the information ratio. See Lan and DeMets (1983).
GAVI
We set the numerator in the tuning parameter [rho] to the correct expected sample size, and to 50% oversampled or undersampled.
mSPRT
We set the tuning parameter [phi] to 1/[tau]2 where [tau] is equal to one of the true effect sizes used in the simulation study (0.1, 0.2, or 0.3).
CAA – no settings.
Naive
The alpha used in the standard z-test is set to 0.05 divided by the number of intermittent analyses.

#### Results

Table 1 displays the empirical false positive results across the 100,000 Monte Carlo replications. As expected, all tests but the oversampled GST and the CAA tests successfully bound the false positive rate. For the GST this is expected since all the false positive rate is fully consumed once the sample reaches the planned sample size, and any test beyond that point will inflate the false positive rate. Similarly, the CAA test is using all intended false positive rate on the last analysis point, and all tests run before the full sample is obtained inflate the false positive rate.

It is worth noting that the always valid tests (GAVI and mSPRT) are conservative when the test is not performed after each new observation. Interestingly, the naive approach has similar conservativeness as some of the always valid approaches when 14 intermittent analyses are performed.

### Power

For the power comparison, we drop the methods that do not bound the false positive rate to make power comparisons valid. For the methods that successfully bound the false positive rate and thus solve the peeking problem, we now turn our attention to the power. That is, each test’s ability to detect an effect when it exists. To do this, we now also add a true effect equal to 0.0, 0.1, 0.2, 0.3, or 0.4 standard deviations of the outcome. This implies that for the zero effect, the observed power corresponds to the empirical false positive rate.

### Results

Table 2 displays the empirical power results for a given treatment effect of 0.2 standard deviations. This effect size was chosen as no method has power 1 or 0 for this effect size, which makes the difference between the methods clearer.

The results show that the GST is in most cases superior to all other methods in terms of power, even when the expected sample size is overestimated. The exception is when the GST uses an alpha spending function that spends very little alpha in combination with an overestimated sample size. This is natural since the phase of the data collection during which most of the alpha is planned to be spent never comes. In this situation, GST has power comparable to the always valid tests, but systematically lower power than the best performing always valid test variants.

The number of intermittent analyses only has a minor impact on the power of the GST. As expected, the always valid tests GAVI and mSPRT have lower power, the fewer intermittent analyses we perform. Even though the differences are not very large, it is worth noting that the naive approach (Bonferroni) with 14 intermittent analyses has higher power than all considered variants of the always valid tests with that few analyses. The mSPRT power is relatively stable across different choices of its tuning parameter, and we see the same for GAVI.

Figure 2 presents the full power curves for a subset of the settings. Most variations perform equally well, with the major exceptions for all effect sizes considered being GST, and Bonferroni correction with stream data. Bonferroni correction with 14 or 56 intermittent analyses performs surprisingly well but expectedly overcompensates when conducting 500 analyses.

## What can we learn from the results?

In summary, we find that the group sequential test is systematically better or comparable to always valid approaches. Since we analyze data arriving in batches at Spotify, the group sequential test’s inability to handle streaming data is no practical limitation; in fact, it means that we’re able to evaluate the data more efficiently since we don’t need to analyze results continuously as data arrives. A surprising result is that when the number of analyses carried out is kept low, applying Bonferroni corrections to standard z-tests is as effective as relying on always valid approaches. This result suggests that depending on the situation, always valid tests may be too general and conservative.

While our simulation study is simple and transparent, the results may not generalize to other situations. Our setup mimics a real-life situation in which there is an upper limit on the number of observations or on the runtime of the experiment. In some cases, the experimenter may want to leave the experiment on indefinitely, so the always valid tests would be more attractive. In the simulation, we have also assumed that the variance is known. In practice, it is not, and estimating the variance could cause further changes to the results. Similarly, we generated data from a normal distribution in the simulation study, and each of the tests could be differently affected if the data instead were, for example, heavily skewed.

The always valid approaches require tuning parameters to be set just as the group sequential test requires an expected sample size. For GAVI, we’ve used parameterizations expressing these in terms of expected sample sizes and effect sizes. A major difference between the expected sample size for the group sequential test and the tuning parameters for the always valid approaches is that the latter are guaranteed to never exceed the desired false positive rate no matter what value is selected. The only potential price one has to pay is in terms of power: a suboptimal value could lead to low power. For the group sequential test, a too low expected sample size in relation to what is actually observed means that the test has an inflated false positive rate. While we don’t explore this topic further in this blog post, it’s worth emphasizing that a correctly bounded false positive rate is guaranteed with always valid inference. Sometimes this guarantee might be more valuable than the reduction in power that follows. For example, if estimation of the expected sample size is difficult and often wrong, an always valid test is preferable to the group sequential test.

In the next section, we look more closely at the behavior of the always valid test when the expected sample size isn’t known at all.

## When you can’t estimate the expected sample size

The simulations indicate that GSTs are often preferable from a power perspective if the expected sample size is known or can be estimated. But what about when the expected sample size is not known and can’t be estimated? This could be the case, for example, when there is no historical data for the type of experiments that are being run. In this section, we look more closely at the properties of AVI in this case.

We could see from the simulations that the number of intermittent analyses is much less important than the ability to estimate the expected sample size (GST), or select the mixing parameter (mSPRT, GAVI). The two always valid test variants considered here are comparable in power, so we focus on the GAVI. The expected sample size is parameterized, which makes reasoning easier.

When using GAVI, it’s safer to underestimate the sample size for the mixing parameter than to overestimate (Howard et al. 2021), to optimize power. At the same time, if you have accurate information about the sample size it’s better to use GST. This means that one of the most appealing situations to use GAVI is when you don’t have accurate information about the sample size you’ll reach and you therefore underestimate the sample size as a strategy to have a valid test with reasonable power properties. This begs the question, how well does GAVI perform under largely underestimated sample sizes?

In the simulation below we let the test be optimized for n=10 (note that since the variance is known this does not affect properties of the tests) whereas the actual sample size is 500, implying an underestimation of the order of 50 times. This might seem like an extreme setting, but to put that in perspective, Eppo is currently using n=10,000 as the GAVI setting for all their sequential tests (Eppo 2023). That is, the simulation corresponds to someone running a test with 500,000 users with Eppo’s current setting, which is plausible.

Table 3 displays the empirical power over 100,000 Monte Carlo simulations. To benchmark, we also include the GST with correctly estimated n and a quadratic alpha spending function, which was the test that performed best in the comparison simulation (Table 2). The power loss from a 50x underestimation of n is around 15% as compared to GAVI with the correct n, and around 30% as compared to GST with the correct n. The fact that the power is up to 30% lower indicates the importance of being able to estimate the sample size well to obtain high power in sequential testing.

Given that the GAVI test allows for infinitely large samples, it’s quite remarkable it doesn’t lose more power when underestimating the sample size this severely. However, it’s worth noting that for up to 56 preplanned intermittent analyses, the Bonferroni approach still outperforms the GAVI in terms of power.

## Our recommendations for selecting a sequential test

Always valid inference is a sequential testing framework that works under very few restrictions. For experimenters that are new to sequential testing and mostly want an early detection system with reliably bounded false positive rates, AVI is the framework to choose. For more sophisticated experimenters that are chasing power/smaller experiments using, for example, variance reduction, it should be used more carefully. It’s not unlikely that you will lose as much power as standard variance reduction techniques will bring you. If you have historical data (which using a variance reduction approach like that suggested by Deng et al. (2013) typically implies), group sequential tests will typically give you substantially higher power.

In any situation where it is not possible to estimate the sample size accurately, the AVI family of tests is a good choice for sequential testing if data is streamed. If the data cannot be streamed, Bonferroni is also a good alternative, although it requires a prespecified max number of intermittent analyses.
If the sample size can be estimated accurately, but the experimenter wants the option to keep the experiment running longer (larger n) AVI is still a good choice, but with a few caveats. By using AVI when the sample size is estimable, the experimenter is losing power as compared to GST. This means that while additional power can be gained from running the experiment longer than the estimated n first observations, it needs to make up for that loss before actually gaining power as compared to all possible tests that can be used in this situation.
If data is available in stream and early detection of large regressions is the main concern, AVI is a good choice. Neither GST or Bonferroni can handle streaming data, and if the regressions are large, power is not an issue. For small regressions, it might be worth waiting for the first batch and using GST to have higher power for smaller sample sizes to detect the deterioration early.  
If the sample size can be estimated accurately, and there is no need to be able to overrun, GST is a good choice. This holds whether you can analyze in a streaming fashion or in batches. Early detection of regressions can be achieved by running many intermittent analyses early in the experiment. If the expected sample size is underestimated on purpose to avoid oversampling, the alpha spending function should not be too conservative in the early phases of data collection.
A common misunderstanding of GST is that the number of intermittent analyses and their timing during data collection needs to be predetermined. This is not the case, see for example Jennison and Turnbull (2000). In fact, you can do as many or as few intermittent analyses as you want, whenever you want during the data collection — and you only pay for the peeking you make — which means you do not decrease power more than necessary.  
Note on variance reduction: All of the tests presented in this post can also be combined with variance reduction to improve the precision of the experiFments. The most popular variance reduction technique based on linear regression can be implemented in a two-step fashion, and it is therefore possible to perform residualization before any of the methods above. There are formal write-ups about how to perform variance reduction via regression without violating the respective framework for both Always Valid Inference (Lindon et al., 2022), and Group Sequential Tests (Jennison and Turnbull, 2000).

This means that the relative comparisons between the methods in this post apply also under the most common type of variance reduction.

## Summary

Spotify’s Experimentation Platform uses group sequential tests because this test was originally designed for medical studies where data arrived in batches — much like the data infrastructure that currently powers our experimentation platform. For streaming data, the group sequential test is not a viable option unless the data is analyzed in batches. Our simulation study shows that even with access to streaming data, the probability that we will identify an effect, when one exists, is higher when the streaming data is analyzed in batches with the group sequential test than in a streaming fashion using any of the other two tests.

Regardless of the specific sequential test chosen, it is critical to use one. A key aspect of the experimentation platform offered to developers at Spotify is that we help them to continuously monitor experiments and detect any adverse effects promptly, without compromising the statistical validity of the experiments. This would not be possible without a sequential test.

Acknowledgement: the authors thanks Mattias Frånberg, Erik Stenberg, and Lizzie Eardley for feedback and suggestions for this blog post.
