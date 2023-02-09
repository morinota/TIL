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

Recommenders are typically evaluated in terms of recommendation accuracy. A recommender is considered to be better than others if a larger number of its recommended items are purchased. We refer to this evaluation approach as accuracy-based evaluation. Precision, which is a commonly utilized accuracy metric for recommenders, is defned as the number of purchases divided by the number of recommendations. However, items may have been bought even without recommendations if the user was already aware of and had a preference for those items. Thus, we aim to evaluate recommenders in terms of the uplift they achieve.

## 2.1. Discrepancy between Accuracy and Uplift

In this subsection, we demonstrate that accuracy metrics such as precision are unsuitable for the goal of increasing user purchases. To describe two cases with and without a recommendation, we adopt the concept of potential outcome from causal inference [15, 28, 37]. Let $Y^T \in {0, 1}$ be the potential outcome with a recommendation (treatment condition) and $Y^C \in {0, 1}$ be the potential outcome without a recommendation (control condition)2. $Y^T= 1$ and $Y^C= 1$ indicate that an item3 will be purchased when recommended and not recommended, respectively. The uplift $\tau$ of an item for a given user4 is $Y^T - Y^C$ . Considering the two possible actions of a user in the two given scenarios, there are four item classes for the user:

- True Uplift (TU). $Y^T= 1$ and $Y^C = 0$, hence $\tau = 1$. The item will be purchased if recommended, but will not be purchased if not recommended.
- False Uplift (FU). $Y^T= Y^C = 1$, hence $\tau= 0$. The item will be purchased regardless of whether it is recommended.
- True Drop (TD). $Y^T= 0$ and $Y^C = 1$, hence $\tau = −1$. The item will be purchased if it is not recommended, but will not be purchased if it is recommended.
- False Drop (FD). $Y^T = Y^C = 0$, hence $\tau= 0$. The item will not be purchased regardless of whether it is recommended.

To intuitively illustrate the diference between the uplift and accuracy in an ofine evaluation setting, we consider four lists of ten recommendations, as shown in Fig. 1. We assume that we have an ofine dataset, which includes both purchase logs and recommendation logs for a currently deployed recommender. Note that TU items are only purchased if recommended, and TD items are only purchased if not recommended. Purchases of other FU and FD items do not depend on recommendations. The total uplift that would have been obtained if all the ten items were recommended in the past is shown in Table 1. We also list precision under two settings: one with all items on the list, and the other with only the items recommended in the logs. The former is a common setting for the ofine evaluations of recommenders [9]. The latter is a setting employed in the previous work [7, 25] to estimate the online performance of a recommender. The former precision value and total uplift exhibit opposite trends for these samples. This means that the best model for achieving a higher uplift cannot be selected based on this former precision. Excluding items without recommendations does not resolve this issue. The latter precision value, calculated using only the recommended items (items with solid boundaries in Fig. 1), exhibits the same value for all lists, and is still unable to select the best model.

As demonstrated by the above illustration, accuracy-based evaluation is not suitable for evaluating the uplift caused by recommenders. We need to employ an evaluation metric designed for uplift-based evaluation. However, we cannot directly calculate the total uplift, because we only observe either $Y^T$ or $Y^C$ for a user-item pair at a given time. To overcome this difculty, we apply a causal inference framework to estimate the average treatment efect.

## 2.2. Causal Inference Framework

In this subsection, we introduce the causal inference framework [15, 28, 37], which we apply to the uplift-based evaluation of recommenders in the next subsection. The treatment efect τ for a subject is defned as the diference between the potential outcomes with and without treatment: $\tau \equiv Y^T - Y^C$ . Note that $\tau$ is not directly measurable, because each subject is either treated or not, and either $Y^T$ or $Y^C$ is observed. However, we can estimate the average treatment efect (ATE), which is expressed as $E[\tau] = E[Y^T] − E[Y^C]$. 

Let $Z \in {0, 1}$ be the binary indicator for the treatment, with $Z = 1$ and $Z = 0$ indicating that the subject does and does not receive treatment, respectively. The covariates associated with the subject are denoted by $X$, e.g., demographic and past records of the subject before treatment assignment. Consider $N$ subjects, indexed by $n$. We use $S^T$ and $S^C$ to denote the sets of subjects who do and do not receive treatment, respectively. Naively, the ATE can be estimated as the diference between the average outcomes of the two sets;

$$
\tag{1}
$$

If treatment is randomly assigned to subjects independent of the potential outcomes, i.e., (YT ,YC )⊥Z, then τˆ converges to the ATE almost surely when N → ∞ (see the proof of [31, Theorem 9.2]). Because the independence condition (YT ,YC )⊥Z is a strong assumption, we instead consider conditional independence (YT , YC ) ⊥Z |X, which means that the covariates X contain all confounders of (YT ,YC ) and Z [28]. Under the conditional independence, the inverse propensity scoring (IPS) estimator,

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
