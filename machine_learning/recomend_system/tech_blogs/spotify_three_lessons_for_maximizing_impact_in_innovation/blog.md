## link

https://engineering.atspotify.com/2023/08/experimentation-at-spotify-three-lessons-for-maximizing-impact-in-innovation/

# Experimentation at Spotify: Three Lessons for Maximizing Impact in Innovation

As companies mature, it’s easy to believe that the core experience and most user needs have been resolved, and all that’s left to work toward are the marginal benefits, the cherries on top. Cherries on top might add delight and panache, but they rarely cause fundamental shifts in performance and success. And as a business, even a mature one, we’re looking for the innovations that tangibly impact the KPIs we care about.

Because we’re testing things that have a lower chance of causing top-line impact, experimentation as a practice and method can become a questionable task. Why spend time and effort to prepare and run an experiment if the results are inconclusive? It’s an understandable and fair question. At the end of the day, a business needs to prioritize actions that contribute to its objectives. However, it would be the wrong conclusion to think we have to write off experimentation altogether — we can, instead, change our approach to it.

In order to make better use of the experimentation method and achieve more tangible impact for the business in a mature context, we ensure we are following three rather straightforward strategies:

1. Start with the decision that needs to be made.
2. Utilize localization to innovate for homogeneous populations.
3. Break the feature apart into its most critical pieces.

## Starting with the decision that needs to be made

Our quest for information, as humans and as organizations, often stems from the need to make decisions. We search for information about travel destinations and flight options to plan a vacation; companies try to decide whether to acquire organizations by gathering yearly statements and other financial data. And in the case of product development, we need to consider what to build, how to build it, for whom to build it, when it will launch, and ultimately decide whether it might be worth it to build at all.

To make a decision, we don’t necessarily need perfect information — or all the information. We need just enough to feel confident about going one way or another. One can see it as an optimization function between spending as few resources as possible to obtain relevant information versus empowering decision-makers to confidently reject alternatives and choose a path forward. Experimentation can be a rather resource-intensive exercise, requiring months of planning, building, running, and analyzing, and in the end, the results might be inconclusive if the right preparations haven’t been made. It’s easy to overdo experiments by cramming in too many variations or by testing something we already have the answer to. On the other hand, experiments can also be under-done — a consequence of attempting to minimize resource use, which results in a lack of information for making the intended decision.

The key here is to approach experimentation, and research in general, with the questions (a) What decision are we trying to inform? and (b) Why are we not able to make that decision with the information at hand? This helps us identify the appropriate — and least resource-intensive — method for finding the answers. And in a case where experimentation is the right answer, this helps us design the test to be as useful as possible.

## Utilizing localization to innovate for homogeneous populations

Experimentation at Spotify: Three Lessons for Maximizing Impact in Innovation

August 16, 2023
Published by Gabriella Ljunggren, Data Scientist
3 lessons for maximizing impact header image.
As companies mature, it’s easy to believe that the core experience and most user needs have been resolved, and all that’s left to work toward are the marginal benefits, the cherries on top. Cherries on top might add delight and panache, but they rarely cause fundamental shifts in performance and success. And as a business, even a mature one, we’re looking for the innovations that tangibly impact the KPIs we care about.

Because we’re testing things that have a lower chance of causing top-line impact, experimentation as a practice and method can become a questionable task. Why spend time and effort to prepare and run an experiment if the results are inconclusive? It’s an understandable and fair question. At the end of the day, a business needs to prioritize actions that contribute to its objectives. However, it would be the wrong conclusion to think we have to write off experimentation altogether — we can, instead, change our approach to it.

In order to make better use of the experimentation method and achieve more tangible impact for the business in a mature context, we ensure we are following three rather straightforward strategies:

Start with the decision that needs to be made.
Utilize localization to innovate for homogeneous populations.
Break the feature apart into its most critical pieces.
Starting with the decision that needs to be made
Our quest for information, as humans and as organizations, often stems from the need to make decisions. We search for information about travel destinations and flight options to plan a vacation; companies try to decide whether to acquire organizations by gathering yearly statements and other financial data. And in the case of product development, we need to consider what to build, how to build it, for whom to build it, when it will launch, and ultimately decide whether it might be worth it to build at all.

To make a decision, we don’t necessarily need perfect information — or all the information. We need just enough to feel confident about going one way or another. One can see it as an optimization function between spending as few resources as possible to obtain relevant information versus empowering decision-makers to confidently reject alternatives and choose a path forward. Experimentation can be a rather resource-intensive exercise, requiring months of planning, building, running, and analyzing, and in the end, the results might be inconclusive if the right preparations haven’t been made. It’s easy to overdo experiments by cramming in too many variations or by testing something we already have the answer to. On the other hand, experiments can also be under-done — a consequence of attempting to minimize resource use, which results in a lack of information for making the intended decision.

The key here is to approach experimentation, and research in general, with the questions (a) What decision are we trying to inform? and (b) Why are we not able to make that decision with the information at hand? This helps us identify the appropriate — and least resource-intensive — method for finding the answers. And in a case where experimentation is the right answer, this helps us design the test to be as useful as possible.

Utilizing localization to innovate for homogeneous populations
As a response to the difficulty of moving top-line metrics in a mature org, we often fall back on discussing alternative definitions of success and the tiering of metrics or user behavior changes to arrive at conclusions about a feature’s potential value. But that conversation overlooks another important dimension: the heterogeneous population of users and needs that we’re solving for as a global company.

We recently set out to experiment on new features for the Japanese market. The Japanese market is unique in many ways, and it has evolved to become a cultural epicenter of the world. We started a year ago with foundational market research to better understand consumers and their behaviors in this market. We ended up with a hypothesis for a new feature that we wanted to test and a specific cohort to test it on. We discovered that by quite rigorously limiting the scope and the target audience for the experiment, we were able to achieve positive top-line impact with an experience that, in a global experiment, would have been lost in the vast smorgasbord of features within our app.

The key to why we were able to achieve positive results for the Japanese experience was in part the limiting of the audience, both in terms of the market and the specific cohort of users within that market. A limited cohort of users in a specific market allows us to solve for a targeted user need and build a solution closely adapted to that, instead of shooting widely and blindly. It’s intuitive to think that we have a higher chance of proving a hypothesis right (or technically rejecting the null hypothesis) if that hypothesis has been carefully crafted from real user needs and is to be proven on a verified segment of the market.

Furthermore, the metrics through which we validate the hypothesis will generally vary less when we measure data for a specific, and more homogeneous, sample compared to all users globally. A concrete example of this idea is the difference in IQ distributions between men and women, where the average is the same but the variance is greater among men than among women. So if you experiment on the whole population, you get a larger variance than if you were to only experiment on a subgroup of women. This is important because it means that we can measure smaller changes in the success metric with maintained significance, i.e., increase our chances of concluding impact.

To add to this, the quality of the localization, in terms of, for example, translations, can be higher when keeping the scope focused on a single market, which in turn reduces the risk of usability issues and value being lost in translation. By having a targeted focus, and not building for a generic global user, we can greatly improve our chances of building and testing impactful products.

## Breaking the feature apart into its most critical pieces

When starting new product development projects, we often fall into the trap of wanting to test the whole new experience against a control without it, because we’re expected to motivate investments through impact on business KPIs. We might think that this will save resources, because we can learn early on whether this new product is a worthwhile investment or not. But in practice this approach often ends up being more costly because when testing a complete experience too early, the risk of bugs, usability issues, and small quirks in the user flow is much higher, which can then hinder the realization of high-level impact and lead to the false conclusion that the product is not valuable or the user need is not real. Or we spend time building a complete experience that turns out to be “meh” at best.

It might initially sound counterintuitive to test small changes to maximize impact, but it’s often the case that the more we’re able to isolate individual changes to the product experience, the more useful and interpretable the data coming out of the experiment will be. Not to mention, the requirement of maturity of the product and code for testing is much lower if we are testing an isolated piece of the experience — which means we can do these types of tests earlier and cheaper than with a full-blown product. However, for this approach to be practically and statistically viable, we need to have a thorough understanding of the user needs through UX research so that we can prioritize the most relevant, or risky, aspects of the experience for testing.

We saw a recent example of this when experimenting on new localized features in some markets in Southeast Asia, where a complete experience was launched for a marketing campaign, without having been tested with users beforehand. The hope was that the experience together with the campaign would drive new user acquisitions, but we ended up being unable to prove any such effects. What happened was that the entry point took up too much real estate in the app, causing negative effects on users who were not interested in the new experience. Had we spent time up front, when designing the experiment, we could have isolated the entry point aspect of it, to make sure we learned about that in particular, which could have helped us draw more definitive conclusions about top-line impact.

## Conclusion

All in all, experimentation is a tool to help us find the innovative experiences that move the needle forward and contribute to the business. But to really do that effectively in a maturing product, we need to have a solid understanding of what decisions we’re trying to make, the users, and the needs we’re solving for. By focusing on more homogeneous groups of users, such as those in specific markets, and localizing the product for them, we can find a shortcut to experiments that actually can prove top-line impact.
