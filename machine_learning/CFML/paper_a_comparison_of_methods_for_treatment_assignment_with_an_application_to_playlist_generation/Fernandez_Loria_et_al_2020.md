## link

- https://arxiv.org/abs/2004.11532

## title

A Comparison of Methods for Treatment Assignment with an Application to Playlist Generation

[Submitted on 24 Apr 2020 (v1), last revised 30 Apr 2022 (this version, v5)]

## Abstract

This study presents a systematic comparison of methods for individual treatment assignment, a general problem that arises in many applications and has received significant attention from economists, computer scientists, and social scientists. We group the various methods proposed in the literature into three general classes of algorithms (or metalearners): learning models to predict outcomes (the O-learner), learning models to predict causal effects (the E-learner), and learning models to predict optimal treatment assignments (the A-learner). We compare the metalearners in terms of (1) their level of generality and (2) the objective function they use to learn models from data; we then discuss the implications that these characteristics have for modeling and decision making. Notably, we demonstrate analytically and empirically that optimizing for the prediction of outcomes or causal effects is not the same as optimizing for treatment assignments, suggesting that in general the A-learner should lead to better treatment assignments than the other metalearners. We demonstrate the practical implications of our findings in the context of choosing, for each user, the best algorithm for playlist generation in order to optimize engagement. This is the first comparison of the three different metalearners on a real-world application at scale (based on more than half a billion individual treatment assignments). In addition to supporting our analytical findings, the results show how large A/B tests can provide substantial value for learning treatment assignment policies, rather than simply choosing the variant that performs best on average.
