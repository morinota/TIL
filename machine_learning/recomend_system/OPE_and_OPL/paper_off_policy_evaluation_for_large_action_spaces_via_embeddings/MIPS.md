## link

- https://arxiv.org/pdf/2202.06317.pdf

## title

Off-Policy Evaluation for Large Action Spaces via Embeddings

## Abstruct

Off-policy evaluation (OPE) in contextual bandits has seen rapid adoption in real-world systems, since it enables offline evaluation of new policies using only historic log data. Unfortunately, when the number of actions is large, existing OPE estimators – most of which are based on inverse propensity score weighting – degrade severely and can suffer from extreme bias and variance. This foils the use of OPE in many applications from recommender systems to language models. To overcome this issue, we propose a new OPE estimator that leverages marginalized importance weights when action embeddings provide structure in the action space. We characterize the bias, variance, and mean squared error of the proposed estimator and analyze the conditions under which the action embedding provides statistical benefits over conventional estimators. In addition to the theoretical analysis, we find that the empirical performance improvement can be substantial, enabling reliable OPE even when existing estimators collapse due to a large number of actions.

# Introduction

Many intelligent systems (e.g., recommender systems, voice assistants, search engines) interact with the environment through a contextual bandit process where a policy observes a context, takes an action, and obtains a reward. Logs of these interactions provide valuable data for off-policy evaluation (OPE), which aims to accurately evaluate the performance of new policies without ever deploying them in the field. OPE is of great practical relevance, as it helps avoid costly online A/B tests and can also act as subroutines for batch policy learning (Dud´ık et al., 2014; Su et al., 2020a). However, OPE is challenging, since the logs contain only partial-information feedback – specifically the reward of the chosen action, but not the counterfactual rewards of all the other actions a different policy might choose.

When the action space is small, recent advances in the design of OPE estimators have led to a number of reliable methods with good theoretical guarantees (Dud´ık et al., 2014; Swaminathan & Joachims, 2015a; Wang et al., 2017; Farajtabar et al., 2018; Su et al., 2019; 2020a; Metelli et al., 2021). Unfortunately, these estimators can degrade severely when the number of available actions is large. Large action spaces are prevalent in many potential applications of OPE, such as recommender systems where policies have to handle thousands or millions of items (e.g., movies, songs, products). In such a situation, the existing estimators based on inverse propensity score (IPS) weighting (Horvitz & Thompson, 1952) can incur high bias and variance, and as a result, be impractical for OPE. First, a large action space makes it challenging for the logging policy to have common support with the target policies, and IPS is biased under support deficiency (Sachdeva et al., 2020). Second, a large number of actions typically leads to high variance of IPS due to large importance weights. To illustrate, we find in our experiments that the variance and mean squared error of IPS inflate by a factor of over 300 when the number of actions increases from 10 to 5000 given a fixed sample size. While doubly robust (DR) estimators can somewhat reduce the variance by introducing a reward estimator as a control variate (Dud´ık et al., 2014), they do not address the fundamental issues that come with large action spaces.

To overcome the limitations of the existing estimators when the action space is large, we leverage additional information about the actions in the form of action embeddings. There are many cases where we have access to such prior information. For example, movies are characterized by auxiliary information such as genres (e.g., adventure, science fiction, documentary), director, or actors. We should then be able to utilize these supplemental data to infer the value of actions under-explored by the logging policy, potentially achieving much more accurate policy evaluation than the existing estimators. We first provide the conditions under which action embeddings provide another path for unbiased OPE, even with support deficient actions. We then propose the Marginalized IPS (MIPS) estimator, which uses the marginal distribution of action embeddings, rather than actual actions, to define a new type of importance weights. We show that MIPS is unbiased under an alternative condition, which states that the action embeddings should mediate every causal effect of the action on the reward. Moreover, we show that MIPS has a lower variance than IPS, especially when there is a large number of actions, and thus the vanilla importance weights have a high variance. We also characterize the gain in MSE provided by MIPS, which implies an interesting bias-variance trade-off with respect to the quality of the action embeddings. Including many embedding dimensions captures the causal effect better, leading to a smaller bias of MIPS. In contrast, using only a subset of the embedding dimensions reduces the variance more. We thus propose a strategy to intentionally violate the assumption about the action embeddings by discarding less relevant embedding dimensions for achieving a better MSE at the cost of introducing some bias. Comprehensive experiments on synthetic and real-world bandit data verify the theoretical findings, indicating that MIPS can provide an effective bias-variance trade-off in the presence of many actions.

# Off-Policy Evaluation

We follow the general contextual bandit setup, and an extensive discussion of related work is given in Appendix A. Let x ∈ X ⊆ R dx be a dx-dimensional context vector drawn i.i.d. from an unknown distribution p(x). Given context x, a possibly stochastic policy π(a|x) chooses action a from a finite action space denoted as A. The reward r ∈ [0, rmax] is then sampled from an unknown conditional distribution p(r|x, a). We measure the effectiveness of a policy π through its value

$$
\tag{1}
$$

where q(x, a) := E[r|x, a] denotes the expected reward given context x and action a.

In OPE, we are given logged bandit data collected by a logging policy π0. Specifically, let D := {(xi , ai , ri)} n i=1 be a sample of logged bandit data containing n independent observations drawn from the logging policy as (x, a, r) ∼ p(x)π0(a|x)p(r|x, a). We aim to develop an estimator Vˆ for the value of a target policy π (which is different from π0) using only the logged data in D. The accuracy of Vˆ is quantified by its mean squared error (MSE)

$$
\tag{}
$$

where ED[·] takes the expectation over the logged data and

$$
\tag{}
$$

In the following theoretical analysis, we focus on the IPS estimator, since most advanced OPE estimators are based on IPS weighting (Dud´ık et al., 2014; Wang et al., 2017; Su et al., 2019; 2020a; Metelli et al., 2021). IPS estimates the value of π by re-weighting the observed rewards as follow

$$
\tag{}
$$

where w(x, a) := π(a|x)/π0(a|x) is called the (vanilla) importance weight. This estimator is unbiased (i.e., ED[Vˆ IPS(π; D)] = V (π)) under the following common support assumption.

Assumption 2.1. (Common Support) The logging policy π0 is said to have common support for policy π if π(a|x) > 0 → π0(a|x) > 0 for all a ∈ A and x ∈ X .

The unbiasedness of IPS is desirable, making this simple re-weighting technique so popular. However, IPS can still be highly biased, particularly when the action space is large. Sachdeva et al. (2020) indicate that IPS has the following bias when Assumption 2.1 is not true.

$$
\tag{}
$$

where U0(x, π0) := {a ∈ A | π0(a|x) = 0} is the set of unsupported or deficient actions for context x under π0. Note that U0(x, π0) can be large especially when A is large. This bias is due to the fact that the logged dataset D does not contain any information about the unsupported actions. Another critical issue of IPS is that its variance can be large, which is given as follows (Dud´ık et al., 2014)

$$
\tag{2}
$$

where σ 2 (x, a) := V[r|x, a]. The variance consists of three terms. The first term reflects the randomness in the rewards. The second term represents the variance due to the randomness over the contexts. The final term is the penalty arising from the use of IPS weighting, and it is proportional to the weights and the true expected reward. The variance contributed by the first and third terms can be extremely large when the weights w(x, a) have a wide range, which occurs when π assigns large probabilities to actions that have low probability under π0. The latter can be expected when the action space A is large and the logging policy π0 aims to have universal support (i.e., π0(a|x) > 0 for all a and x). Swaminathan et al. (2017) also point out that the variance of IPS grows linearly with w(x, a), which can be Ω(|A|).

This variance issue can be lessened by incorporating a reward estimator qˆ(x, a) ≈ q(x, a) as a control variate, resulting in the DR estimator (Dud´ık et al., 2014). DR often improves the MSE of IPS due to its variance reduction property. However, DR still suffers when the number of actions is large, and it can experience substantial performance deterioration as we demonstrate in our experiments.

# The Marginalized IPS Estimator

The following proposes a new estimator that circumvents the challenges of IPS for large action spaces. Our approach is to bring additional structure into the estimation problem, providing a path forward despite the minimax optimality of IPS and DR. In particular, IPS and DR achieve the minimax optimal MSE of at most O(n −1 (Eπ0 [w(x, a) 2σ 2 (x, a) + w(x, a) 2 r 2 max])), which means that they are impossible to improve upon in the worst case beyond constant factors (Wang et al., 2017; Swaminathan et al., 2017), unless we bring in additional structure. Our key idea for overcoming the limits of IPS and DR is to assume the existence of action embeddings as prior information. The intuition is that this can help the estimator transfer information between similar actions. More formally, suppose we are given a de-dimensional action embedding e ∈ E ⊆ R de for each action a, where we merely assume that the embedding is drawn i.i.d. from some unknown distribution p(e|x, a). The simplest example is to construct action embeddings using predefined category information (e.g., product category). Then, the embedding distribution is independent of the context and it is deterministic given the action. Our framework is also applicable to the most general case of continuous, stochastic, and context-dependent action embeddings. For example, product prices may be generated by a personalized pricing algorithm running behind the system. In this case, the embedding is continuous, depends on the user context, and can be stochastic if there is some randomness in the pricing algorithm. Using the action embeddings, we now refine the definition of the policy value as:

$$


$$

Note here that q(x, a) = Ep(e|x,a) [q(x, a, e)] where q(x, a, e) := E[r|x, a, e], so the above refinement does not contradict the original definition given in Eq. (1). A logged bandit dataset now contains action embeddings for each observation in D = {(xi , ai , ei , ri)} n i=1, where each tuple is generated by the logging policy as (x, a, e, r) ∼ p(x)π0(a|x)p(e|x, a)p(r|x, a, e). Our strategy is to leverage this additional information for achieving a more accurate OPE for large action spaces. To motivate our approach, we introduce two properties characterizing an action embedding.

Assumption 3.1. (Common Embedding Support) The logging policy π0 is said to have common embedding support for policy π if p(e|x, π) > 0 → p(e|x, π0) > 0 for all e ∈ E and x ∈ X , where p(e|x, π) := P a∈A p(e|x, a)π(a|x) is the marginal distribution over the action embedding space given context x and policy π.

Assumption 3.1 is analogous to Assumption 2.1, but requires only the common support with respect to the action embedding space, which can be substantially more compact than the action space itself. Indeed, Assumption 3.1 is weaker than common support of IPS (Assumption 2.1).1 Next, we characterize the expressiveness of the embedding in the ideal case, but we will relax this assumption later.

Assumption 3.2. (No Direct Effect) Action a has no direct effect on the reward r, i.e., a ⊥ r | x, e. As illustrated in Figure 1, Assumption 3.2 requires that every possible effect of a on r be fully mediated by the observed embedding e. For now, we rely on the validity of Assumption 3.2, as it is convenient for introducing the proposed estimator. However, we later show that it is often beneficial to strategically discard some embedding dimensions and violate the assumption to achieve a better MSE. We start the derivation of our new estimator with the observation that Assumption 3.2 gives us another path to unbiased estimation of the policy value without Assumption 2.1.

Proposition 3.3. Under Assumption 3.2, we have

$$
\tag{}
$$

See Appendix B.1 for the proof. Proposition 3.3 provides another expression of the policy value without explicitly relying on the action variable a. This new expression naturally leads to the following marginalized inverse propensity score (MIPS) estimator, which is our main proposal.

$$
\tag{}
$$

where w(x, e) := p(e|x, π)/p(e|x, π0) is the marginal importance weight defined with respect to the marginal distribution over the action embedding space. To obtain an intuition for the benefits of MIPS, we provide a toy example in Table 1 with X = {x1}, A = {a1, a2, a3}, and E = {e1, e2, e3} (a special case of our formulation with a discrete embedding space). The left table describes the logging and target policies with respect to A and implies that Assumption 2.1 is violated (π0(a1|x1) = 0.0). The middle table describes the conditional distribution of the action embedding e given action a (e.g., probability of a movie a belonging to a genre e). The right table describes the marginal distributions over E, which are calculable from the other two tables. By considering the marginal distribution, Assumption 3.1 is ensured in the right table, even if Assumption 2.1 is not true in the left table. Moreover, the maximum importance weight is smaller for the right table (maxe∈E w(x1, e) < maxa∈A w(x1, a)), which may contribute to a variance reduction of the resulting estimator. Below, we formally analyze the key statistical properties of MIPS and compare them with those of IPS, including the realistic case where Assumption 3.2 is violated.

## Theoretical Analysis

First, the following proposition shows that MIPS is unbiased under assumptions different from those of IPS.

Proposition 3.4. Under Assumptions 3.1 and 3.2, MIPS is unbiased, i.e., ED[VˆMIPS(π; D)] = V (π) for any π. See Appendix B.2 for the proof. Proposition 3.4 states that, even when π0 fails to provide common support over A such that IPS is biased, MIPS can still be unbiased if π0 provides common support over E (Assumption 3.1) and e fully captures the causal effect of a on r (Assumption 3.2).

Having multiple estimators that enable unbiased OPE under different assumptions is in itself desirable, as we can choose the appropriate estimator depending on the data generating process. However, it is also helpful to understand how violations of the assumptions influence the bias of the resulting estimator. In particular, for MIPS, it is difficult to verify whether Assumption 3.2 is true in practice. The following theorem characterizes the bias of MIPS. Theorem 3.5. (Bias of MIPS) If Assumption 3.1 is true, but Assumption 3.2 is violated, MIPS has the following bias.

$$
\tag{}
$$

where a, b ∈ A. See Appendix B.3 for the proof. Theorem 3.5 suggests that three factors contribute to the bias of MIPS when Assumption 3.2 is violated. The first factor is the predictivity of the action embeddings with respect to the actual actions. When action a is predictable given context x and embedding e, π0(a|x, e) is close to zero or one (deterministic), meaning that π0(a|x, e)π0(b|x, e) is close to zero. This suggests that even if Assumption 3.2 is violated, action embeddings that identify the actions well still enable a nearly unbiased estimation of MIPS. The second factor is the amount of direct effect of the action on the reward, which is quantified by q(x, a, e) − q(x, b, e). When the direct effect of a on r is small, q(x, a, e) − q(x, b, e) also becomes small and so is the bias of MIPS. In an ideal situation where Assumption 3.2 is satisfied, we have q(x, a, e) = q(x, b, e) = q(x, e), thus MIPS is unbiased, which is consistent with Proposition 3.4. Note that the first two factors suggest that, to reduce the bias, the action embeddings should be informative so that they are either predictive of the actions or mediate a large amount of the causal effect. The final factor is the similarity between logging and target policies quantified by w(x, a) − w(x, b). When Assumption 3.2 is satisfied, MIPS is unbiased for any target policy, however, Theorem 3.5 suggests that if the assumption is not true, MIPS produces a larger bias for target policies dissimilar from the logging policy.2

Next, we analyze the variance of MIPS, which we show is never worse than that of IPS and can be substantially lower. Theorem 3.6. (Variance Reduction of MIPS) Under Assumptions 2.1, 3.1, and 3.2, we have

$$
\tag{}
$$

which is non-negative. Note that the variance reduction is also lower bounded by zero even when Assumption 3.2 is not true. See Appendix B.4 for the proof. There are two factors that affect the amount of variance reduction. The first factor is the second moment of the reward with respect to p(r|x, e). This term becomes large when, for example, the reward is noisy even after conditioning on the action embedding e. The second factor is the variance of w(x, a) with respect to the conditional distribution π0(a|x, e), which becomes large when (i) w(x, a) has a wide range or (ii) there remain large variations in a even after conditioning on action embedding e so that π0(a|x, e) remains stochastic. Therefore, MIPS becomes increasingly favorable compared to IPS for larger action spaces where the variance of w(x, a) becomes larger. Moreover, to obtain a large variance reduction, the action embedding should ideally not be unnecessarily predictive of the actions. Finally, the next theorem describes the gain in MSE we can obtain from MIPS when Assumption 3.2 is violated.

Theorem 3.7. (MSE Gain of MIPS) Under Assumptions 2.1 and 3.1, we have

$$
\tag{}
$$

See Appendix B.5 for the proof. Note that IPS can have some bias when Assumption 2.1 is not true, possibly producing a greater MSE gain for MIPS

## Data-Driven Embedding Selection

The analysis in the previous section implies a clear biasvariance trade-off with respect to the quality of the action embeddings. Specifically, Theorem 3.5 suggests that the action embeddings should be as informative as possible to reduce the bias when Assumption 3.2 is violated. On the other hand, Theorem 3.6 suggests that the action embeddings should be as coarse as possible to gain a greater variance reduction. Theorem 3.7 summarizes the bias-variance trade-off in terms of MSE. A possible criticism to MIPS is Assumption 3.2, as it is hard to verify whether this assumption is satisfied using only the observed logged data. However, the above discussion about the bias-variance trade-off implies that it might be effective to strategically violate Assumption 3.2 by discarding some embedding dimensions. This action embedding selection can lead to a large variance reduction at the cost of introducing some bias, possibly improving the MSE of MIPS. To implement the action embedding selection, we can adapt the estimator selection method called SLOPE proposed in Su et al. (2020b) and Tucker & Lee (2021). SLOPE is based on Lepski’s principle for bandwidth selection in nonparametric statistics (Lepski & Spokoiny, 1997) and is used to tune the hyperparameters of OPE estimators. A benefit of SLOPE is that it avoids estimating the bias of the estimator, which is as difficult as OPE. Appendix C describes how to apply SLOPE to the action embedding selection in our setup, and Section 4 evaluates its benefit empirically.

## Estimating the Marginal Importance Weights

When using MIPS, we might have to estimate w(x, e) depending on how the embeddings are given. A simple approach to this is to utilize the following transformation

$$
\tag{3}
$$

Eq. (3) implies that we need an estimate of π0(a|x, e), which we compute by regressing a on (x, e). We can then estimate w(x, e) as wˆ(x, e) = Eπˆ0(a|x,e) [w(x, a)]. 3 This procedure is easy to implement and tractable, even when the embedding space is high-dimensional and continuous. Note that, even if there are some deficient actions, we can directly estimate w(x, e) by solving density ratio estimation as binary classification as done in Sondhi et al. (2020).

# Empirical Evaluation

We first evaluate MIPS on synthetic data to identify the situations where it enables a more accurate OPE. Second, we validate real-world applicability on data from an online fashion store. Our experiments are conducted using the OpenBanditPipeline (OBP)4 , an open-source software for OPE provided by Saito et al. (2020). Our experiment implementation is available at https://github.com/usaito/icml2022-mips

## Synthetic Data

For the first set of experiments, we create synthetic data to be able to compare the estimates to the ground-truth value of the target policies. To create the data, we sample 10- dimensional context vectors x from the standard normal distribution. We also sample de-dimensional categorical action embedding e ∈ E from the following conditional distribution given action a.

$$
\tag{4}
$$

which is independent of the context x in the synthetic experiment. {αa,ek } is a set of parameters sampled independently from the standard normal distribution. Each dimension of E has a cardinality of 10, i.e., Ek = {1, 2, . . . , 10}. We then synthesize the expected reward as

$$
\tag{5}
$$

where M, θx, and θe are parameter matrices or vectors to define the expected reward. These parameters are sampled from a uniform distribution with range [−1, 1]. xek is a context vector corresponding to the k-th dimension of the action embedding, which is unobserved to the estimators. ηk specifies the importance of the k-th dimension of the action embedding, which is sampled from Dirichlet distribution so that Pde k=1 ηk = 1. Note that if we observe all dimensions of E, then q(x, e) = q(x, a, e). On the other hand, q(x, e) 6= q(x, a, e), if there are some missing dimensions, which means that Assumption 3.2 is violated. We synthesize the logging policy π0 by applying the softmax function to q(x, a) = Ep(e|a) [q(x, e)] a

$$
\tag{6}
$$

where β is a parameter that controls the optimality and entropy of the logging policy. A large positive value of β leads to a near-deterministic and well-performing logging policy, while lower values make the logging policy increasingly worse. In the main text, we use β = −1, and additional results for other values of β can be found in Appendix D.2. In contrast, the target policy π is defined a

$$
\tag{}
$$

where the noise  ∈ [0, 1] controls the quality of π. In the main text, we set  = 0.05, which produces a near-optimal and near-deterministic target policy. We share additional results for other values of  in Appendix D.2. To summarize, we first sample context x and define the expected reward q(x, e) as in Eq. (5). We then sample discrete action a from π0 based on Eq. (6). Given action a, we sample categorical action embedding e based on Eq. (4). Finally, we sample the reward from a normal distribution with mean q(x, e) and standard deviation σ = 2.5. Iterating this procedure n times generates logged data D with n independent copies of (x, a, e, r).

### BASELINES

We compare our estimator with Direct Method (DM), IPS, and DR.5 We use the Random Forest (Breiman, 2001) implemented in scikit-learn (Pedregosa et al., 2011) along with 2-fold cross-fitting (Newey & Robins, 2018) to obtain qˆ(x, e) for DR and DM. We use the Logistic Regression of scikit-learn to estimate πˆ0(a|x, e) for MIPS. We also report the results of MIPS with the true importance weights as “MIPS (true)”. MIPS (true) provides the best performance we could achieve by improving the procedure for estimating the importance weights of MIPS

### RESULTS

The following reports and discusses the MSE, squared bias, and variance of the estimators computed over 100 different sets of logged data replicated with different seeds.

#### How does MIPS perform with varying numbers of actions?

First, we evaluate the estimators’ performance when we vary the number of actions from 10 to 5000. The sample size is fixed at n = 10000. Figure 2 shows how the number of actions affects the estimators’ MSE (both on linear- and log-scale). We observe that MIPS provides substantial improvements over IPS and DR particularly for larger action sets. More specifically, when |A| = 10, MSE(VˆIPS) MSE(VˆMIPS) = 1.38, while MSE(VˆIPS) MSE(VˆMIPS) = 12.38 for |A| = 5000, indicating a significant performance improvement of MIPS for larger action spaces as suggested in Theorem 3.6. MIPS is also consistently better than DM, which suffers from high bias. The figure also shows that MIPS (true) is even better than MIPS in large action sets, mostly due to the reduced bias when using the true marginal importance weights. This observation implies that there is room for further improvement in how to estimate the marginal importance weights.

#### How does MIPS perform with varying sample sizes?

Next, we compare the estimators under varying numbers of samples (n ∈ {800, 1600, 3200, 6400, 12800, 25600}). The number of actions is fixed at |A| = 1000. Figure 3 reports how the estimators’ MSE changes with the size of logged bandit data. We can see that MIPS is appealing in particular for small sample sizes where it outperforms IPS and DR by a larger margin than in large sample regimes ( MSE(VˆIPS) MSE(VˆMIPS) = 9.10 when n = 800, while MSE(VˆIPS) MSE(VˆMIPS) = 4.87 when n = 25600). With the growing sample size, MIPS, IPS, and DR improve their MSE as their variance decreases. In contrast, the accuracy of DM does not change across different sample sizes, but it performs better than IPS and DR because they converge very slowly in the presence of many actions. In contrast, MIPS is better than DM except for n = 800, as the bias of MIPS is much smaller than that of DM. Moreover, MIPS becomes increasingly better than DM with the growing sample size, as the variance of MIPS decreases while DM remains highly biased.

#### How does MIPS perform with varying numbers of deficient actions?

We also compare the estimators under varying numbers of deficient actions (|U0| ∈ {0, 100, 300, 500, 700, 900}) with a fixed action set (|A| = 1000). Figure 4 shows how the number of deficient actions affects the estimators’ MSE, squared bias, and variance. The results suggest that MIPS (true) is robust and not affected by the existence of deficient actions. In addition, MIPS is mostly better than DM, IPS, and DR even when there are many deficient actions. However, we also observe that the gap between MIPS and MIPS (true) increases for large numbers of deficient actions due to the bias in estimating the marginal importance weights. Note that the MSE of IPS and DR decreases with increasing number of deficient actions, because their variance becomes smaller with a smaller number of supported actions, even though their bias increases as suggested by Sachdeva et al. (2020).

#### How does MIPS perform when Assumption 3.2 is violated?

Here, we evaluate the accuracy of MIPS when Assumption 3.2 is violated. To adjust the amount of violation, we modify the action embedding space and reduce the cardinality of each dimension of E to 2 (i.e., Ek = {0, 1}), while we increase the number of dimensions to 20 (de = 20). This leads to |E| = 220 = 1, 048, 576, and we can now drop some dimensions to increase violation. In particular, when we observe all dimensions of E, Assumption 3.2 is perfectly satisfied. However, when we withhold {0, 2, 4, . . . , 18} embedding dimensions, the assumption becomes increasingly invalid. When many dimensions are missing, the bias of MIPS is expected to increase as suggested in Theorem 3.5, potentially leading to a worse MSE. Figure 5 shows how the MSE, squared bias, and variance of the estimators change with varying numbers of unobserved embedding dimensions. Somewhat surprisingly, we observe that MIPS and MIPS (true) perform better when there are some missing dimensions, even if it leads to the violated assumption. Specifically, the MSE of MIPS and MIPS (true) is minimized when there are 4 and 8 missing dimensions (out of 20), respectively. This phenomenon is due to the reduced variance. The third column of Figure 5 implies that the variance of MIPS and MIPS (true) decreases substantially with an increasing number of unobserved dimensions, while the bias increases with the violated assumption as expected. These observations suggest that MIPS can be highly effective despite the violated assumption.

#### How does data-driven embedding selection perform combined with MIPS?

The previous section showed that there is a potential to improve the accuracy of MIPS by selecting a subset of dimensions for estimating the marginal importance weights. We now evaluate whether we can effectively address this embedding selection problem. Figure 6 compares the MSE, squared bias, and variance of MIPS and MIPS with SLOPE (MIPS w/ SLOPE) using the same embedding space as in the previous section. Note that we vary the sample size n and fix |A| = 1000. The results suggest that the data-driven embedding selection provides a substantial improvement in MSE for small sample sizes. As shown in the second and third columns in Figure 6, the embedding selection significantly reduces the variance at the cost of introducing some bias by strategically violating the assumption, which results in a better MSE.

#### Other benefits of MIPS.

MIPS has additional benefits over the conventional estimators. In fact, in addition to the case with many actions, IPS is also vulnerable when logging and target policies differ substantially and the reward is noisy (see Eq. (2)). Appendix D.2 empirically investigates the additional benefits of MIPS with varying logging/target policies and varying noise levels with a fixed action set. We observe that MIPS is substantially more robust to the changes in policies and added noise than IPS or DR, which provides further arguments for the applicability of MIPS.

## Real-World Data

To assess the real-world applicability of MIPS, we now evaluate MIPS on real-world bandit data. In particular, we use the Open Bandit Dataset (OBD)6 (Saito et al., 2020), a publicly available logged bandit dataset collected on a large-scale fashion e-commerce platform. We use 100,000 observations that are randomly sub-sampled from the “ALL” campaign of OBD. The dataset contains user contexts x, fashion items to recommend as action a ∈ A where |A| = 240, and resulting clicks as reward r ∈ {0, 1}. OBD also includes 4-dimensional action embedding vectors such as hierarchical category information about the fashion items. The dataset consists of two sets of logged bandit data collected by two different policies (uniform random and Thompson sampling) during an A/B test of these policies. We regard uniform random and Thompson sampling as logging and target policies, respectively, to perform an evaluation of OPE estimators. Appendix D.3 describes the detailed experimental procedure to evaluate the accuracy of the estimators on real-world bandit data.

#### Results.

We evaluate MIPS (w/o SLOPE) and MIPS (w/ SLOPE) in comparison to DM, IPS, DR, Switch-DR, More Robust DR (Farajtabar et al., 2018), DRos, and DR-λ. We apply SLOPE to tune the built-in hyperparameters of SwitchDR, DRos, and DR-λ. Figure 7 compares the estimators by drawing the cumulative distribution function (CDF) of their squared errors estimated with 150 different bootstrapped samples of the logged data. Note that the squared errors are normalized by that of IPS. We find that MIPS (w/ SLOPE) outperforms IPS in about 80% of the simulation runs, while other estimators, including MIPS (w/o SLOPE), work similarly to IPS. This result demonstrates the real-world applicability of our estimator as well as the importance of implementing action embedding selection in practice. We report qualitatively similar results for other sample sizes (from 10,000 to 500,000) in Appendix D.3.

# Conclusion and Future Work

We explored the problem of OPE for large action spaces. In this setting, existing estimators based on IPS suffer from impractical variance, which limits their applicability. This problem is highly relevant for practical applications, as many real decision making problems such as recommender systems have to deal with a large number of discrete actions. To achieve an accurate OPE for large action spaces, we propose the MIPS estimator, which builds on the marginal importance weights computed with action embeddings. We characterize the important statistical properties of the proposed estimator and discuss when it is superior to the conventional ones. Extensive experiments demonstrate that MIPS provides a significant gain in MSE when the vanilla importance weights become large due to large action spaces, substantially outperforming IPS and related estimators.

Our work raises several interesting research questions. For example, this work assumes the existence of some predefined action embeddings and analyzes the resulting statistical properties of MIPS. Even though we discussed how to choose which embedding dimensions to use for OPE (Section 3.2), it would be intriguing to develop a more principled method to optimize or learn (possibly continuous) action embeddings from the logged data for further improving MIPS. Developing a method for accurately estimating the marginal importance weight would also be crucial to fill the gap between MIPS and MIPS (true) observed in our experiments. It would also be interesting to explore off-policy learning using action embeddings and possible applications of marginal importance weighting to other estimators that depend on the vanilla importance weight such as DR.
