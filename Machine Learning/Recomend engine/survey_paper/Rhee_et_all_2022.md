## 0.1. link

https://dl.acm.org/doi/abs/10.1145/3523227.3546757
https://dl.acm.org/doi/pdf/10.1145/3523227.3546757?casa_token=3kkYhpFdUDkAAAAA:zipZZnov8a0YaVfYEm7PKzszWsmMqV31imC5L6xAW_jwgKe74UF4d-xifHIa3b5IUr43CBTSuoN2KIXj

## 0.2. title

Countering Popularity Bias by Regularizing Score Differences



## 0.3. abstruct

Recommendation system often suffers from popularity bias. Often the training data inherently exhibits long-tail distribution in item popularity (data bias). Moreover, the recommendation systems could give unfairly higher recommendation scores to popular items even among items a user equally liked, resulting in over-recommendation of popular items (model bias). In this study we propose a novel method to reduce the model bias while maintaining accuracy by directly regularizing the recommendation scores to be equal across items a user preferred. Akin to contrastive learning, we extend the widely used pairwise loss (BPR loss) which maximizes the score differences between preferred and unpreferred items, with a regularization term that minimizes the score differences within preferred and unpreferred items, respectively, thereby achieving both high debias and high accuracy performance with no additional training. To test the effectiveness of the proposed method, we design an experiment using a synthetic dataset which induces model bias with baseline training; we showed applying the proposed method resulted in drastic reduction of model bias while maintaining accuracy. Comprehensive comparison with earlier debias methods showed the proposed method had advantages in terms of computational validity and efficiency. Further empirical experiments utilizing four benchmark datasets and four recommendation models indicated the proposed method showed general improvements over performances of earlier debias methods. We hope that our method could help users enjoy diverse recommendations promoting serendipitous findings. Code available at https://github.com/stillpsy/popbias.

![](https://developers.cyberagent.co.jp/blog/wp-content/uploads/2022/10/popularity_bias_fig1-768x296.jpg)

# 1. Introduction

# 2. Related Work

## 2.1. Popularity Bias

## 2.2. Countering Popularity Bias

## 2.3. Contrastive Learning

# 3. Preliminaries

## 3.1. Implicit Recommendation System and Bayesian Personalized Ranking Loss

## 3.2. Popularity Bias in Model Prediction (Model Bias)

## 3.3. Visual Illustration on Synthetic Data

# 4. Proposed Method

## 4.1. Regularization Term ot Minimize Score Difference

## 4.2. Illustration of the Proposed Method on the Synthetic Data

# 5. Advangtages of the Proposed Method

## 5.1. Performances of Earlier Methods

## 5.2. Comparing the Zerosum Method with the PD Method

## 5.3. Comparing the Zerosum Method with the Pearson Method

# 6. Empirical Experiments

## 6.1. Experimental Settings

## 6.2. Results & Discussion

# 7. Conclusion
