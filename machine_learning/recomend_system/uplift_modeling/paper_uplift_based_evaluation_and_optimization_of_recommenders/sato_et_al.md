## 0.1. link

[pdf](https://dl.acm.org/doi/pdf/10.1145/3298689.3347018)

## 0.2. title

Uplif-based Evaluation and Optimization of Recommenders

## 0.3. abstruct

Recommender systems aim to increase user actions such as clicks and purchases. Typical evaluations of recommenders regard the purchase of a recommended item as a success. However, the item may have been purchased even without the recommendation. An uplift is defned as an increase in user actions caused by recommendations. Situations with and without a recommendation cannot both be observed for a specifc user-item pair at a given time instance, making uplift-based evaluation and optimization challenging. This paper proposes new evaluation metrics and optimization methods for the uplift in a recommender system. We apply a causal inference framework to estimate the average uplift for the ofine evaluation of recommenders. Our evaluation protocol leverages both purchase and recommendation logs under a currently deployed recommender system, to simulate the cases both with and without recommendations. This enables the ofine evaluation of the uplift for newly generated recommendation lists. For optimization, we need to defne positive and negative samples that are specifc to an uplift-based approach. For this purpose, we deduce four classes of items by observing purchase and recommendation logs. We derive the relative priorities among these four classes in terms of the uplift and use them to construct both pointwise and pairwise sampling methods for uplift optimization. Through dedicated experiments with three public datasets, we demonstrate the efectiveness of our optimization methods in improving the uplift.

# 1. introduction

One of the major goals of recommender systems is to induce positive user interactions, such as clicks and purchases. Because increases in user interactions directly beneft businesses, recommender systems have been utilized in various domains of industry. Recommendations are typically evaluated in terms of purchases1 of recommended items. However, these items may have been purchased even without recommendations. For a certain e-commerce site, more than 75% of the recommended items that were clicked would have been clicked even without the recommendations [42]. We argue that the true success of recommendations is represented by the increase in user actions caused by recommendations. Such an increase afected purely by recommendations is called an uplift. The development of a recommender should focus more on the uplift than the accurate prediction of user purchases. However, evaluating and optimizing the uplift is difcult, owing to its unobservable nature. An item is either recommended or not for a specifc user at a given time instance, so the uplift cannot be directly measured for a given recommendation. This means that there is no ground truth for training and evaluating a model. Previous studies targeting uplift construct purchase prediction models incorporating recommendation efects [2, 40]. The items recommended are ones that have the largest diferences between the predicted purchase probabilities for cases with and without recommendations. Another approach builds two prediction models: one for predictions with recommendations and the other for predictions with no recommendations [3]. All of these methods are based on purchase prediction models optimized for prediction accuracy, even though they target uplift. We expect an improvement in uplift performance by optimizing models directly for the uplift. In this study, we propose new evaluation methods and optimization methods for uplift-based recommendation. First, we show that common accuracy-based evaluation metrics such as precision do not align with the uplift. Then, we derive evaluation protocols to estimate the average uplift for recommendations, based on a potential outcome framework in causal inference [15, 28, 37]. Furthermore, we propose optimization methods for recommenders, to improve the uplift. We apply these methods to a matrix factorization model [14, 32, 35], which is the most common model for recommenders. To verify the efectiveness of the proposed optimization methods, we compare the uplift performance of our methods with baselines, including recent recommenders [3, 40] that target the uplift. We further investigate the characteristics of our uplift-based optimizations and the recommendation outputs.

The contributions of this paper are summarized as follows.

- We propose ofine evaluation metrics for the recommendation uplift (Section 2).
- We present both pointwise and pairwise optimization methods for uplift-based recommendation (Section 3).
- We demonstrate the efectiveness of our optimization methods through comparisons with baselines (Subsection 5.2).
- We clarify the characteristics of the optimization (Subsection 5.3) and the recommendation outputs (Subsection 5.4).

# 2. Uplift-Based Evaluation

## 2.1. Discrepancy between Accuracy and Uplift

## 2.2. Causal Inference Framework

## 2.3. Uplift Estimates for Recommenders

# 3. Uplift-Based Optimization

## 3.1. Classifcation of the Observations

## 3.2. Proposed Sampling Method

# 4. Related Work

## 4.1. Causal Inference for Recommenders

## 4.2. Recommendation Targeting Uplift

# 5. Experiments

## 5.1. Experimental Settings

## 5.2. Performance Comparison (RQ1)

## 5.3. Uplift-based Optimization Properties (RQ2)

## 5.4. Trends of the Recommended Items (RQ3)

# 6. Conclusions
