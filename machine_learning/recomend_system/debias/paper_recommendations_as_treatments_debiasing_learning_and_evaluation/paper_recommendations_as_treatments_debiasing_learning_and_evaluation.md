## link

- https://arxiv.org/abs/1602.05352

## title

Recommendations as Treatments: Debiasing Learning and Evaluation

## abstract

Most data for evaluating and training recommender systems is subject to selection biases, either through self-selection by the users or through the actions of the recommendation system itself. In this paper, we provide a principled approach to handling selection biases, adapting models and estimation techniques from causal inference. The approach leads to unbiased performance estimators despite biased data, and to a matrix factorization method that provides substantially improved prediction performance on real-world data. We theoretically and empirically characterize the robustness of the approach, finding that it is highly practical and scalable.

# Introduction

Virtually all data for training recommender systems is subject to selection biases. For example, in a movie recommendation system users typically watch and rate those movies that they like, and rarely rate movies that they do not like (Pradel et al., 2012). Similarly, when an adplacement system recommends ads, it shows ads that it believes to be of interest to the user, but will less frequently display other ads. Having observations be conditioned on the effect we would like to optimize (e.g. the star rating, the probability of a click, etc.) leads to data that is Missing Not At Random (MNAR) (Little & Rubin, 2002). This creates a widely-recognized challenge for evaluating recommender systems (Marlin & Zemel, 2009; Myttenaere et al., 2014).

We develop an approach to evaluate and train recommender systems that remedies selection biases in a principled, practical, and highly effective way. Viewing recommendation from a causal inference perspective, we argue that exposing a user to an item in a recommendation system is an intervention analogous to exposing a patient to a treatment in a medical study. In both cases, the goal is to accurately estimate the effect of new interventions (e.g. a new treatment policy or a new set of recommendations) despite incomplete and biased data due to self-selection or experimenterbias. By connecting recommendation to causal inference from experimental and observational data, we derive a principled framework for unbiased evaluation and learning of recommender systems under selection biases.

The main contribution of this paper is four-fold. First, we show how estimating the quality of a recommendation system can be approached with propensity-weighting techniques commonly used in causal inference (Imbens & Rubin, 2015), complete-cases analysis (Little & Rubin, 2002), and other problems (Cortes et al., 2008; Bickel et al., 2009; Sugiyama & Kawanabe, 2012). In particular, we derive unbiased estimators for a wide range of performance measures (e.g. MSE, MAE, DCG). Second, with these estimators in hand, we propose an Empirical Risk Minimization (ERM) framework for learning recommendation systems under selection bias, for which we derive generalization error bounds. Third, we use the ERM framework to derive a matrix factorization method that can account for selection bias while remaining conceptually simple and highly scalable. Fourth, we explore methods to estimate propensities in observational settings where selection bias is due to selfselection by the users, and we characterize the robustness of the framework against mis-specified propensities.

Our conceptual and theoretical contributions are validated in an extensive empirical evaluation. For the task of evaluating recommender systems, we show that our performance estimators can be orders-of-magnitude more accurate than standard estimators commonly used in the past (Bell et al., 2007). For the task of learning recommender systems, we show that our new matrix factorization method substantially outperforms methods that ignore selection bias, as well as existing state-of-the-art methods that perform jointlikelihood inference under MNAR data (Hernandez-Lobato ´ et al., 2014). This is especially promising given the conceptual simplicity and scalability of our approach compared to joint-likelihood inference. We provide an implemention of our method, as well as a new benchmark dataset, online1 .

# Related Work

Past work that explicitly dealt with the MNAR nature of recommendation data approached the problem as missingdata imputation based on the joint likelihood of the missing data model and the rating model (Marlin et al., 2007; Marlin & Zemel, 2009; Hernandez-Lobato et al. ´ , 2014). This has led to sophisticated and highly complex methods. We take a fundamentally different approach that treats both models separately, making our approach modular and scalable. Furthermore, our approach is robust to mis-specification of the rating model, and we characterize how the overall learning process degrades gracefully under a mis-specified missing-data model. We empirically compare against the state-of-the-art joint likelihood model (Hernandez-Lobato et al. ´ , 2014) in this paper.

Related but different from the problem we consider is recommendation from positive feedback alone (Hu et al., 2008; Liang et al., 2016). Related to this setting are also alternative approaches to learning with MNAR data (Steck, 2010; 2011; Lim et al., 2015), which aim to avoid the problem by considering performance measures less affected by selection bias under mild assumptions. Of these works, the approach of Steck (2011) is most closely related to ours, since it defines a recall estimator that uses item popularity as a proxy for propensity. Similar to our work, Steck (2010; 2011) and Hu et al. (2008) also derive weighted matrix factorization methods, but with weighting schemes that are either heuristic or need to be tuned via cross validation. In contrast, our weighted matrix factorization method enjoys rigorous learning guarantees in an ERM framework.

Propensity-based approaches have been widely used in causal inference from observational studies (Imbens & Rubin, 2015), as well as in complete-case analysis for missing data (Little & Rubin, 2002; Seaman & White, 2013) and in survey sampling (Thompson, 2012). However, their use in matrix completion is new to our knowledge. Weighting approaches are also widely used in domain adaptation and covariate shift, where data from one source is used to train for a different problem (e.g., Huang et al., 2006; Bickel et al., 2009; Sugiyama & Kawanabe, 2012). We will draw upon this work, especially the learning theory of weighting approaches in (Cortes et al., 2008; 2010).

# Unbiased Performance Estimation for Recommendation

Consider a toy example adapted from Steck (2010) to illustrate the disastrous effect that selection bias can have on conventional evaluation using a test set of held-out ratings. Denote with u ∈ {1, ..., U} the users and with i ∈ {1, ..., I} the movies. Figure 1 shows the matrix of true ratings Y ∈ U×I for our toy example, where a sub set of users are “horror lovers” who rate all horror movies 5 and all romance movies 1. Similarly, there is a subset of “romance lovers” who rate just the opposite way. However, both groups rate dramas as 3. The binary matrix O ∈ {0, 1} U×I in Figure 1 shows for which movies the users provided their rating to the system, [Ou,i = 1] ⇔ [Yu,i observed]. Our toy example shows a strong correlation between liking and rating a movie, and the matrix P describes the marginal probabilities Pu,i = P(Ou,i = 1) with which each rating is revealed. For this data, consider the following two evaluation tasks.

## Task 1: Estimating Rating Prediction Accuracy

For the first task, we want to evaluate how well a predicted rating matrix Yˆ reflects the true ratings in Y . Standard evaluation measures like Mean Absolute Error (MAE) or Mean Squared Error (MSE) can be written as:

$$
\tag{1}
$$

for an appropriately chosen δu,i(Y, Yˆ ).

$$
\tag{2}
$$

$$
\tag{3}
$$

$$
\tag{4}
$$

Since Y is only partially known, the conventional practice is to estimate R(Yˆ ) using the average over only the observed entries,

$$
\tag{5}
$$

We call this the naive estimator, and its naivety leads to a gross misjudgment for the Yˆ 1 and Yˆ 2 given in Figure 1. Even though Yˆ 1 is clearly better than Yˆ 2 by any reasonable measure of performance, Rˆ naive(Yˆ ) will reliably claim that Yˆ 2 has better MAE than Yˆ 1. This error is due to selection bias, since 1-star ratings are under-represented in the observed data and δu,i(Y, Yˆ ) is correlated with Yu,i. More generally, under selection bias, Rˆ naive(Yˆ ) is not an unbiased estimate of the true performance R(Yˆ ) (Steck, 2013):

$$
\tag{6}
$$

Before we design an improved estimator to replace Rˆ naive(Yˆ ), let’s turn to a related evaluation task.

## Task 2: Estimating Recommendation Quality

Instead of evaluating the accuracy of predicted ratings, we may want to more directly evaluate the quality of a particular recommendation. To this effect, let’s redefine Yˆ to now encode recommendations as a binary matrix analogous to O, where [Yˆ u,i = 1] ⇔ [i is recommended to u], limited to a budget of k recommendations per user. An example is Yˆ 3 in Figure 1. A reasonable way to measure the quality of a recommendation is the Cumulative Gain (CG) that the user derives from the recommended movies, which we define as the average star-rating of the recommended movies in our toy example2 . CG can again be written in the form of Eq. (1) with

$$
\tag{7}
$$

However, unless users have watched all movies in Yˆ , we cannot compute CG directly via Eq. (1). Hence, we are faced with the counterfactual question: how well would our users have enjoyed themselves (in terms of CG), if they had followed our recommendations Yˆ instead of watching the movies indicated in O? Note that rankings of recommendations are similar to the set-based recommendation described above, and measures like Discounted Cumulative Gain (DCG), DCG@k, Precision at k (PREC@k), and others (Aslam et al., 2006; Yilmaz et al., 2008) also fit in this setting. For those, let the values of Yˆ in each row define the predicted ranking, then

$$
\tag{8}
$$

$$
\tag{9}
$$

One approach, similar in spirit to condensed DCG (Sakai, 2007), is to again use the naive estimator from Eq. (5). However, this and similar estimators are generally biased for R(Yˆ ) (Pradel et al., 2012; Steck, 2013).

To get unbiased estimates of recommendation quality despite missing observations, consider the following connection to estimating average treatment effects of a given policy in causal inference, that was already explored in the contextual bandit setting (Li et al., 2011; Dud´ık et al., 2011). If we think of a recommendation as an intervention analogous to treating a patient with a specific drug, in both settings we want to estimate the effect of a new treatment policy (e.g. give drug A to women and drug B to men, or new recommendations Yˆ ). The challenge in both cases is that we have only partial knowledge of how much certain patients (users) benefited from certain treatments (movies) (i.e., Yu,i with Ou,i = 1), while the vast majority of potential outcomes in Y is unobserved.

## Propensity-Scored Performance Estimators

The key to handling selection bias in both of the abovementioned evaluation tasks lies in understanding the process that generates the observation pattern in O. This process is typically called the Assignment Mechanism in causal inference (Imbens & Rubin, 2015) or the Missing Data Mechanism in missing data analysis (Little & Rubin, 2002). We differentiate the following two settings:

- Experimental Setting. In this setting, the assignment mechanism is under the control of the recommendation system. An example is an ad-placement system that controls which ads to show to which user.
- Observational Setting. In this setting, the users are part of the assignment mechanism that generates O. An example is an online streaming service for movies, where users self-select the movies they watch and rate.

In this paper, we assume that the assignment mechanism is probabilistic, meaning that the marginal probability Pu,i = P(Ou,i = 1) of observing an entry Yu,i is non-zero for all user/item pairs. This ensures that, in principle, every element of Y could be observed, even though any particular O reveals only a small subset. We refer to Pu,i as the propensity of observing Yu,i. In the experimental setting, we know the matrix P of all propensities, since we have implemented the assignment mechanism. In the observational setting, we will need to estimate P from the observed matrix O. We defer the discussion of propensity estimation to Section 5, and focus on the experimental setting first.

IPS Estimator:
The Inverse-Propensity-Scoring (IPS) estimator (Thompson, 2012; Little & Rubin, 2002; Imbens & Rubin, 2015), which applies equally to the task of rating prediction evaluation as to the task of recommendation quality estimation, is defined as,

$$
\tag{10}
$$

Unlike the naive estimator Rˆ naive(Yˆ ), the IPS estimator is unbiased for any probabilistic assignment mechanism. Note that the IPS estimator only requires the marginal probabilities Pu,i and unbiased-ness is not affected by dependencies within O:

$$
\tag{10.5}
$$

To characterize the variability of the IPS estimator, however, we assume that observations are independent given P, which corresponds to a multivariate Bernoulli model where each Ou,i is a biased coin flip with probability Pu,i. The following proposition (proof in appendix) provides some intuition about how the accuracy of the IPS estimator changes as the propensities become more “non-uniform”.

Proposition 3.1 (Tail Bound for IPS Estimator). Let P be the independent Bernoulli probabilities of observing each entry. For any given Yˆ and Y , with probability 1 − η, the IPS estimator Rˆ IP S(Yˆ |P) does not deviate from the true R(Yˆ ) by more than:

$$
\tag{10.6}
$$

where ρu,i = δu,i(Y,Yˆ ) Pu,i if Pu,i < 1, and ρu,i = 0 otherwise.

To illustrate this bound, consider the case of uniform propensities Pu,i = p. This means that n = p U I elements of Y are revealed in expectation. In this case, the bound is O(1/(p √ UI)). If the Pu,i are non-uniform, the bound can be much larger even if the expected number of revealed elements, PPu,i is n. We are paying for the unbiased-ness of IPS in terms of variability, and we will evaluate whether this price is well spent throughout the paper.

SNIPS Estimator. One technique that can reduce variability is the use of control variates (Owen, 2013). Applied to the IPS estimator, we know that EO hP (u,i):Ou,i=1 1 Pu,i i = U · I. This yields the SelfNormalized Inverse Propensity Scoring (SNIPS) estimator (Trotter & Tukey, 1956; Swaminathan & Joachims, 2015)

$$
\tag{11}
$$

The SNIPS estimator often has lower variance than the IPS estimator but has a small bias (Hesterberg, 1995).

## Empirical Illustration of Estimators

To illustrate the effectiveness of the proposed estimators we conducted an experiment on the semi-synthetic ML100K dataset described in Section 6.2. For this dataset, Y is completely known so that we can compute true performance via Eq. (1). The probability Pu,i of observing a rating Yu,i was chosen to mimic the observed marginal rating distribution in the original ML100K dataset (see Section 6.2) such that, on average, 5% of the Y matrix was revealed.

Table 1 shows the results for estimating rating prediction accuracy via MAE and recommendation quality via DCG@50 for the following five prediction matrices Yˆ i . Let |Y = r| be the number of r-star ratings in Y .

- REC ONES: The prediction matrix Yˆ is identical to the true rating matrix Y , except that |{(u, i) : Yu,i = 5}| randomly selected true ratings of 1 are flipped to 5. This means half of the predicted fives are true fives, and half are true ones.
- REC FOURS: Same as REC ONES, but flipping 4-star ratings instead.
- ROTATE: For each predicted rating Yˆ u,i = Yu,i −1 when Yu,i ≥ 2, and Yˆ u,i = 5 when Yu,i = 1.
- SKEWED: Predictions Yˆ u,i are sampled from N (Yˆ raw u,i |µ = Yu,i, σ = 6−Yu,i 2 ) and clipped to the interval [0, 6].
- COARSENED: If the true rating Yu,i ≤ 3, then Yˆ u,i = 3. Otherwise Yˆ u,i = 4.

Rankings for DCG@50 were created by sorting items according to Yˆ i for each user. In Table 1, we report the average and standard deviation of estimates over 50 samples of O from P. We see that the mean IPS estimate perfectly matches the true performance for both MAE and DCG as expected. The bias of SNIPS is negligible as well. The naive estimator is severely biased and its estimated MAE incorrectly ranks the prediction matrices Yˆ i (e.g. it ranks the performance of REC ONES higher than REC FOURS). The standard deviation of IPS and SNIPS is substantially smaller than the bias that Naive incurs. Furthermore, SNIPS manages to reduce the standard deviation of IPS for MAE but not for DCG. We will empirically study these estimators more comprehensively in Section 6.

# Propensity-Scored Recommendation Learning

We will now use the unbiased estimators from the previous section in an Empirical Risk Minimization (ERM) framework for learning, prove generalization error bounds, and derive a matrix factorization method for rating prediction.

## ERM for Recommendation with Propensities

Empirical Risk Minimization underlies many successful learning algorithms like SVMs (Cortes & Vapnik, 1995), Boosting (Schapire, 1990), and Deep Networks (Bengio, 2009). Weighted ERM approaches have been effective for cost-sensitive classification, domain adaptation and covariate shift (Zadrozny et al., 2003; Bickel et al., 2009; Sugiyama & Kawanabe, 2012). We adapt ERM to our setting by realizing that Eq. (1) corresponds to an expected loss (i.e. risk) over the data generating process P(O|P). Given a sample from P(O|P), we can think of the IPS estimator from Eq. (10) as the Empirical Risk Rˆ(Yˆ ) that estimates R(Yˆ ) for any Yˆ .

Definition 4.1 (Propensity-Scored ERM for Recommendation). Given training observations O from Y with marginal propensities P, given a hypothesis space H of predictions Yˆ , and given a loss function δu,i(Y, Yˆ ), ERM selects the Yˆ ∈ H that optimizes:

$$
\tag{12}
$$

Using the SNIPS estimator does not change the argmax. To illustrate the validity of the propensity-scored ERM approach, we state the following generalization error bound (proof in appendix) similar to Cortes et al. (2010). We consider only finite H for the sake of conciseness.

Theorem 4.2 (Propensity-Scored ERM Generalization Error Bound). For any finite hypothesis space of predictions H = {Yˆ 1, ..., Yˆ |H|} and loss 0 ≤ δu,i(Y, Yˆ ) ≤ ∆, the true risk R(Yˆ ) of the empirical risk minimizer Yˆ ERM from H using the IPS estimator, given training observations O from Y with independent Bernoulli propensities P, is bounded with probability 1 − η by:

$$
\tag{13}
$$

## Propensity-Scored Matrix Factorization

We now use propensity-scored ERM to derive a matrix factorization method for the problem of rating prediction. Assume a standard rank-d-restricted and L2-regularized matrix factorization model Yˆ u,i = v T u wi+au+bi+c with user, item, and global offsets as our hypothesis space H. Under this model, propensity-scored ERM leads to the following training objective:

$$
\tag{14}
$$

where A encodes the offset terms and Yˆ ERM = V T W+A. Except for the propensities Pu,i that act like weights for each loss term, the training objective is identical to the standard incomplete matrix factorization objective (Koren, 2008; Steck, 2010; Hu et al., 2008) with MSE (using Eq. (3)) or MAE (using Eq. (2)). So, we can readily draw upon existing optimization algorithms (i.e., Gemulla et al., 2011; Yu et al., 2012) that can efficiently solve the training problem at scale. For the experiments reported in this paper, we use Limited-memory BFGS (Byrd et al., 1995). Our implementation is available online3 .

Conventional incomplete matrix factorization is a special case of Eq. (14) for MCAR (Missing Completely At Random) data, i.e., all propensities Pu,i are equal. Solving this training objective for other δu,i(Y, Yˆ ) that are nondifferentiable is more challenging, but possible avenues exist (Joachims, 2005; Chapelle & Wu, 2010). Finally, note that other recommendation methods (e.g., Weimer et al., 2007; Lin, 2007) can in principle be adapted to propensity scoring as well.

# Propensity Estimation for Observational Data

We now turn to the Observational Setting where propensities need to be estimated. One might be worried that we need to perfectly reconstruct all propensities for effective learning. However, as we will show, we merely need estimated propensities that are “better” than the naive assumption of observations being revealed uniformly, i.e., P = |{(u, i) : Ou,i = 1}|/ (U · I) for all users and items. The following characterizes “better” propensities in terms of the bias they induce and their effect on the variability of the learning process.

Lemma 5.1 (Bias of IPS Estimator under Inaccurate Propensities). Let P be the marginal probabilities of observing an entry of the rating matrix Y , and let Pˆ be the estimated propensities such that Pˆ u,i > 0 for all u, i. The bias of the IPS estimator Eq. (10) using Pˆ is

$$
\tag{15}
$$

In addition to bias, the following generalization error bound (proof in appendix) characterizes the overall impact of the estimated propensities on the learning process.

Theorem 5.2 (Propensity-Scored ERM Generalization Error Bound under Inaccurate Propensities). For any finite hypothesis space of predictions H = {Yˆ 1, ..., Yˆ |H|}, the transductive prediction error of the empirical risk minimizer Yˆ ERM, using the IPS estimator with estimated propensities Pˆ (Pˆ u,i > 0) and given training observations O from Y with independent Bernoulli propensities P, is bounded by:

$$
\tag{16}
$$

The bound shows a bias-variance trade-off that does not occur in conventional ERM. In particular, the bound suggests that it may be beneficial to overestimate small propensities, if this reduces the variability more than it increases the bias.

## Propensity Estimation Models.

Recall that our goal is to estimate the probabilities Pu,i with which ratings for user u and item i will be observed. In general, the propensities

$$
\tag{17}
$$

can depend on some observable features X (e.g., the predicted rating displayed to the user), unobservable features Xhid (e.g., whether the item was recommended by a friend), and the ratings Y . It is reasonable to assume that Ou,i is independent of the new predictions Yˆ (and therefore independent of δu,i(Y, Yˆ )) once the observable features are taken into account. The following outlines two simple propensity estimation methods, but there is a wide range of other techniques available (e.g., McCaffrey et al., 2004) that can cater to domain-specific needs.

### Propensity Estimation via Naive Bayes.

The first approach estimates P(Ou,i|X, Xhid, Y ) by assuming that dependencies between covariates X, Xhid and other ratings are negligible. Eq. (17) then reduces to P(Ou,i|Yu,i) similar to Marlin & Zemel (2009). We can treat Yu,i as observed, since we only need the propensities for observed entries to compute IPS and SNIPS. This yields the Naive Bayes propensity estimator:

$$
\tag{18}
$$

We dropped the subscripts to reflect that parameters are tied across all u and i. Maximum likelihood estimates for P(Y = r | O = 1) and P(O = 1) can be obtained by counting observed ratings in MNAR data. However, to estimate P(Y = r), we need a small sample of MCAR data.

### Propensity Estimation via Logistic Regression

The second propensity estimation approach we explore (which does not require a sample of MCAR data) is based on logistic regression and is commonly used in causal inference (Rosenbaum, 2002). It also starts from Eq. (17), but aims to find model parameters φ such that O becomes independent of unobserved Xhid and Y , i.e., P(Ou,i|X, Xhid, Y ) = P(Ou,i|X, φ). The main modeling assumption is that there exists a φ = (w, β, γ) such that Pu,i = σ w T Xu,i + βi + γu  . Here, Xu,i is a vector encoding all observable information about a user-item pair (e.g., user demographics, whether an item was promoted, etc.), and σ(·) is the sigmoid function. βi and γu are peritem and per-user offsets.

# Empirical Evaluation

We conduct semi-synthetic experiments to explore the empirical performance and robustness of the proposed methods in both the experimental and the observational setting. Furthermore, we compare against the state-of-theart joint-likelihood method for MNAR data (Hernandez- ´ Lobato et al., 2014) on real-world datasets.

## Experiment Setup

In all experiments, we perform model selection for the regularization parameter λ and/or the rank of the factorization d via cross-validation as follows. We randomly split the observed MNAR ratings into k folds (k = 4 in all experiments), training on k − 1 and evaluating on the remaining one using the IPS estimator. Reflecting this additional split requires scaling the propensities in the training folds by k−1 k and those in the validation fold by 1 k . The parameters with the best validation set performance are then used to retrain on all MNAR data. We finally report performance on the MCAR test set for the real-world datasets, or using Eq. (1) for our semi-synthetic dataset.

## How does sampling bias severity affect evaluation?

First, we evaluate how different observation models impact the accuracy of performance estimates. We compare the Naive estimator of Eq. (5) for MSE, MAE and DCG with their propensity-weighted analogues, IPS using Eq. (10) and SNIPS using Eq. (11) respectively. Since this experiment requires experimental control of sampling bias, we created a semi-synthetic dataset and observation model.

ML100K Dataset.
The ML100K dataset4 provides 100K MNAR ratings for 1683 movies by 944 users. To allow ground-truth evaluation against a fully known rating matrix, we complete these partial ratings using standard matrix factorization. The completed matrix, however, give unrealistically high ratings to almost all movies. We therefore adjust ratings for the final Y to match a more realistic rating distribution [p1, p2, p3, p4, p5] for ratings 1 to 5 as given in Marlin & Zemel (2009) as follows: we assign the bottom p1 fraction of the entries by value in the completed matrix a rating of 1, and the next p2 fraction of entries by value a rating of 2, and so on. Hyper-parameters (rank d and L2 regularization λ) were chosen by using a 90-10 train-test split of the 100K ratings, and maximizing the 0/1 accuracy of the completed matrix on the test set.

ML100K Observation Model.
If the underlying rating is 4 or 5, the propensity for observing the rating is equal to k. For ratings r < 4, the corresponding propensity is kα4−r . For each α, k is set so that the expected number of ratings we observe is 5% of the entire matrix. By varying α > 0, we vary the MNAR effect: α = 1 is missing uniformly at random (MCAR), while α → 0 only reveals 4 and 5 rated items. Note that α = 0.25 gives a marginal distribution of observed ratings that reasonably matches the observed MNAR rating marginals on ML100K ([0.06, 0.11, 0.27, 0.35, 0.21] in the real data vs. [0.06, 0.10, 0.25, 0.42, 0.17] in our model).

Results.
Table 1, described in Section 3.4, shows the estimated MAE and DCG@50 when α = 0.25. Next, we vary the severity of the sampling bias by changing α ∈ (0, 1]. Figure 2 reports how accurately (in terms of root mean squared estimation error (RMSE)) each estimator predicts the true MSE and DCG respectively. These results are for the Experimental Setting where propensities are known. They are averages over the five prediction matrices Yˆ i given in Section 3.4 and across 50 trials. Shaded regions indicate a 95% confidence interval.

Over most of the range of α, in particular for the realistic value of α = 0.25, the IPS and SNIPS estimators are orders-of-magnitude more accurate than the Naive estimator. Even for severely low choices of α, the gain due to bias reduction of IPS and SNIPS still outweighs the added variability compared to Naive. When α = 1 (MCAR), SNIPS is algebraically equivalent to Naive, while IPS pays a small penalty due to increased variability from propensity weighting. For MSE, SNIPS consistently reduces estimation error over IPS while both are tied for DCG.

## How does sampling bias severity affect learning?

Now we explore whether these gains in risk estimation accuracy translate into improved learning via ERM, again in the Experimental Setting. Using the same semi-synthetic ML100K dataset and observation model as above, we compare our matrix factorization MF-IPS with the traditional unweighted matrix factorization MF-Naive. Both methods use the same factorization model with separate λ selected via cross-validation and d = 20. The results are plotted in Figure 3 (left), where shaded regions indicate 95% confidence intervals over 30 trials. The propensity-weighted matrix factorization MF-IPS consistently outperforms conventional matrix factorization in terms of MSE. We also conducted experiments for MAE, with similar results.

## How robust is evaluation and learning to inaccurately learned propensities?

We now switch from the Experimental Setting to the Observational Setting, where propensities need to be estimated. To explore robustness to propensity estimates of varying accuracy, we use the ML100K data and observation model with α = 0.25. To generate increasingly bad propensity estimates, we use the Naive Bayes model from Section 5.1, but vary the size of the MCAR sample for estimating the marginal ratings P(Y = r) via the Laplace estimator.

Figure 4 shows how the quality of the propensity estimates impacts evaluation using the same setup as in Section 6.2. Under no condition do the IPS and SNIPS estimator perform worse than Naive. Interestingly, IPS-NB with estimated propensities can perform even better than IPS-KNOWN with known propensities, as can be seen for MSE. This is a known effect, partly because the estimated propensities can provide an effect akin to stratification (Hirano et al., 2003; Wooldridge, 2007).

Figure 3 (right) shows how learning performance is affected by inaccurate propensities using the same setup as in Section 6.3. We compare the MSE prediction error of MFIPS-NB with estimated propensities to that of MF-Naive and MF-IPS with known propensities. The shaded area shows the 95% confidence interval over 30 trials. Again, we see that MF-IPS-NB outperforms MF-Naive even for severely degraded propensity estimates, demonstrating the robustness of the approach.

## Performance on Real-World Data

Our final experiment studies performance on real-world datasets. We use the following two datasets, which both have a separate test set where users were asked to rate a uniformly drawn sample of items.

Yahoo! R3 Dataset. This dataset5 (Marlin & Zemel, 2009) contains user-song ratings. The MNAR training set provides over 300K ratings for songs that were selfselected by 15400 users. The test set contains ratings by a subset of 5400 users who were asked to rate 10 randomly chosen songs. For this data, we estimate propensities via Naive Bayes. As a MCAR sample for eliciting the marginal rating distribution, we set aside 5% of the test set and only report results on the remaining 95% of the test set.

Coat Shopping Dataset. We collected a new dataset6 simulating MNAR data of customers shopping for a coat in an online store. The training data was generated by giving Amazon Mechanical Turkers a simple web-shop interface with facets and paging. They were asked to find the coat in the store that they wanted to buy the most. Afterwards, they had to rate 24 of the coats they explored (self-selected) and 16 randomly picked ones on a five-point scale. The dataset contains ratings from 290 Turkers on an inventory of 300 items. The self-selected ratings are the training set and the uniformly selected ratings are the test set. We learn propensities via logistic regression based on user covariates (gender, age group, location, and fashion-awareness) and item covariates (gender, coat type, color, and was it promoted). A standard regularized logistic regression (Pedregosa et al., 2011) was trained using all pairs of user and item covariates as features and cross-validated to optimize log-likelihood of the self-selected observations.

Results. Table 2 shows that our propensity-scored matrix factorization MF-IPS with learnt propensities substantially and significantly outperforms the conventional matrix factorization approach, as well as the Bayesian imputation models from (Hernandez-Lobato et al. ´ , 2014), abbreviated as HL-MNAR and HL-MAR (paired t-test, p < 0.001 for all). This holds for both MAE and MSE. Furthermore, the performance of MF-IPS beats the best published results for Yahoo in terms of MSE (1.115) and is close in terms of MAE (0.770) (the CTP-v model of (Marlin & Zemel, 2009) as reported in the supplementary material of Hernandez- ´ Lobato et al. (2014)). For MF-IPS and MF-Naive all hyperparameters (i.e., λ ∈ {10−6 , ..., 1} and d ∈ {5, 10, 20, 40}) were chosen by cross-validation. For the HL baselines, we explored d ∈ {5, 10, 20, 40} using software provided by the authors7 and report the best performance on the test set for efficiency reasons. Note that our performance numbers for HL on Yahoo closely match the values reported in (Hernandez-Lobato et al. ´ , 2014).

Compared to the complex generative HL models, we conclude that our discriminative MF-IPS performs robustly and efficiently on real-world data. We conjecture that this strength is a result of not requiring any generative assumptions about the validity of the rating model. Furthermore, note that there are several promising directions for further improving performance, like propensity clipping (Strehl et al., 2010), doubly-robust estimation (Dud´ık et al., 2011), and the use of improved methods for propensity estimation (McCaffrey et al., 2004).

# Conclusions

We proposed an effective and robust approach to handle selection bias in the evaluation and training of recommender systems based on propensity scoring. The approach is a discriminative alternative to existing joint-likelihood methods which are generative. It therefore inherits many of the advantages (e.g., efficiency, predictive performance, no need for latent variables, fewer modeling assumptions) of discriminative methods. The modularity of the approach— separating the estimation of the assignment model from the rating model—also makes it very practical. In particular, any conditional probability estimation method can be plugged in as the propensity estimator, and we conjecture that many existing rating models can be retrofit with propensity weighting without sacrificing scalability.
