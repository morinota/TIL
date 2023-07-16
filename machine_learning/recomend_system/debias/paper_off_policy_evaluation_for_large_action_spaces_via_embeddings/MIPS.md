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
