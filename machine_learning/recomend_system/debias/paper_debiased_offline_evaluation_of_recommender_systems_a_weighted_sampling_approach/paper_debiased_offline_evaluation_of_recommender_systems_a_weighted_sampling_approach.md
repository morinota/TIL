## link

- https://dl.acm.org/doi/10.1145/3341105.3375759

## title

Debiased offline evaluation of recommender systems: a weighted-sampling approach

## abstract

Offline evaluation of recommender systems mostly relies on historical data, which is often biased by many confounders. In such data, user-item interactions are Missing Not At Random (MNAR). Measures of recommender system performance on MNAR test data are unlikely to be reliable indicators of real-world performance unless something is done to mitigate the bias. One way that researchers try to obtain less biased offline evaluation is by designing new supposedly unbiased performance estimators for use on MNAR test data. We investigate an alternative solution, a sampling approach. The general idea is to use a sampling strategy on MNAR data to generate an intervened test set with less bias --- one in which interactions are Missing At Random (MAR) or, at least, one that is more MAR-like. An example of this is SKEW, a sampling strategy that aims to adjust for the confounding effect that an item's popularity has on its likelihood of being observed.

In this paper, we propose a novel formulation for the sampling approach. We compare our solution to SKEW and to two baselines which perform a random intervention on MNAR data (and hence are equivalent to no intervention in practice). We empirically validate for the first time the effectiveness of SKEW and we show our approach to be a better estimator of the performance one would obtain on (unbiased) MAR test data. Our strategy benefits from high generality properties (e.g. it can also be employed for training a recommender) and low overheads (e.g. it does not require any learning).
