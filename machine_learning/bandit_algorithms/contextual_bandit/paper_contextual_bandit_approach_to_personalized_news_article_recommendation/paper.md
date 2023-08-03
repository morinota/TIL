## link

https://elicit.org/search?q=contextual-bandit+approach+to+personalized+news+article+recommendation&token=01H6WSCJKBN9JGVG9CRQNKSJQJ&paper=ec0072bc37f83f1a81459df43289613e04cc61e1&column=title

## title

A contextual-bandit approach to personalized news article recommendation

## Abstract

Personalized web services strive to adapt their services (advertisements, news articles, etc.) to individual users by making use of both content and user information. Despite a few recent advances, this problem remains challenging for at least two reasons. First, web service is featured with dynamically changing pools of content, rendering traditional collaborative filtering methods inapplicable. Second, the scale of most web services of practical interest calls for solutions that are both fast in learning and computation.

In this work, we model personalized recommendation of news articles as a contextual bandit problem, a principled approach in which a learning algorithm sequentially selects articles to serve users based on contextual information about the users and articles, while simultaneously adapting its article-selection strategy based on user-click feedback to maximize total user clicks.

The contributions of this work are three-fold. First, we propose a new, general contextual bandit algorithm that is computationally efficient and well motivated from learning theory. Second, we argue that any bandit algorithm can be reliably evaluated offline using previously recorded random traffic. Finally, using this offline evaluation method, we successfully applied our new algorithm to a Yahoo! Front Page Today Module dataset containing over 33 million events. Results showed a 12.5% click lift compared to a standard context-free bandit algorithm, and the advantage becomes even greater when data gets more scarce.

# 1. INTRODUCTION

This paper addresses the challenge of identifying the most appropriate web-based content at the best time for individual users. Most \* This work was done while R. Schapire visited Yahoo! Labs. April 26-30, 2010 , Raleigh, North Carolina, USA. . service vendors acquire and maintain a large amount of content in their repository, for instance, for filtering news articles [14] or for the display of advertisements [5]. Moreover, the content of such a web-service repository changes dynamically, undergoing frequent insertions and deletions. In such a setting, it is crucial to quickly identify interesting content for users. For instance, a news filter must promptly identify the popularity of breaking news, while also adapting to the fading value of existing, aging news stories.

A version of this paper appears at WWW 2010,
It is generally difficult to model popularity and temporal changes based solely on content information. In practice, we usually explore the unknown by collecting consumers' feedback in real time to evaluate the popularity of new content while monitoring changes in its value [3]. For instance, a small amount of traffic can be designated for such exploration. Based on the users' response (such as clicks) to randomly selected content on this small slice of traffic, the most popular content can be identified and exploited on the remaining traffic. This strategy, with random exploration on an ǫ fraction of the traffic and greedy exploitation on the rest, is known as ǫ-greedy. Advanced exploration approaches such as EXP3 [8] or UCB1 [7] could be applied as well. Intuitively, we need to distribute more traffic to new content to learn its value more quickly, and fewer users to track temporal changes of existing content.

Recently, personalized recommendation has become a desirable feature for websites to improve user satisfaction by tailoring content presentation to suit individual users' needs [10]. Personalization involves a process of gathering and storing user attributes, managing content assets, and, based on an analysis of current and past users' behavior, delivering the individually best content to the present user being served.

Often, both users and content are represented by sets of features. User features may include historical activities at an aggregated level as well as declared demographic information. Content features may contain descriptive information and categories. In this scenario, exploration and exploitation have to be deployed at an individual level since the views of different users on the same content can vary significantly. Since there may be a very large number of possible choices or actions available, it becomes critical to recognize commonalities between content items and to transfer that knowledge across the content pool.

Traditional recommender systems, including collaborative filtering, content-based filtering and hybrid approaches, can provide meaningful recommendations at an individual level by leveraging users' interests as demonstrated by their past activity. Collaborative filtering [25], by recognizing similarities across users based on their consumption history, provides a good recommendation solution to the scenarios where overlap in historical consumption across users is relatively high and the content universe is almost static. Contentbased filtering helps to identify new items which well match an existing user's consumption profile, but the recommended items are always similar to the items previously taken by the user [20]. Hybrid approaches [11] have been developed by combining two or more recommendation techniques; for example, the inability of collaborative filtering to recommend new items is commonly alleviated by combining it with content-based filtering.

However, as noted above, in many web-based scenarios, the content universe undergoes frequent changes, with content popularity changing over time as well. Furthermore, a significant number of visitors are likely to be entirely new with no historical consumption record whatsoever; this is known as a cold-start situation [21]. These issues make traditional recommender-system approaches difficult to apply, as shown by prior empirical studies [12]. It thus becomes indispensable to learn the goodness of match between user interests and content when one or both of them are new. However, acquiring such information can be expensive and may reduce user satisfaction in the short term, raising the question of optimally balancing the two competing goals: maximizing user satisfaction in the long run, and gathering information about goodness of match between user interests and content.

The above problem is indeed known as a feature-based exploration/exploitation problem. In this paper, we formulate it as a contextual bandit problem, a principled approach in which a learning algorithm sequentially selects articles to serve users based on contextual information of the user and articles, while simultaneously adapting its article-selection strategy based on user-click feedback to maximize total user clicks in the long run. We define a bandit problem and then review some existing approaches in Section 2. Then, we propose a new algorithm, LinUCB, in Section 3 which has a similar regret analysis to the best known algorithms for competing with the best linear predictor, with a lower computational overhead. We also address the problem of offline evaluation in Section 4, showing this is possible for any explore/exploit strategy when interactions are independent and identically distributed (i.i.d.), as might be a reasonable assumption for different users. We then test our new algorithm and several existing algorithms using this offline evaluation strategy in Section 5.

# 2. FORMULATION & RELATED WORK

In this section, we define the K-armed contextual bandit problem formally, and as an example, show how it can model the personalized news article recommendation problem. We then discuss existing methods and their limitations.

## 2.1 A Multi-armed Bandit Formulation

The problem of personalized news article recommendation can be naturally modeled as a multi-armed bandit problem with context information. Following previous work [18], we call it a contextual bandit. 1 Formally, a contextual-bandit algorithm A proceeds in discrete trials t = 1, 2, 3, . . . In trial t:

1. The algorithm observes the current user ut and a set At of arms or actions together with their feature vectors xt,a for a ∈ At. The vector xt,a summarizes information of both the user ut and arm a, and will be referred to as the context. 2. Based on observed payoffs in previous trials, A chooses an arm at ∈ At, and receives payoff rt,a t whose expectation depends on both the user ut and the arm at. 3. The algorithm then improves its arm-selection strategy with the new observation, (xt,a t , at, rt,a t ). It is important to em-phasize here that no feedback (namely, the payoff rt,a) is observed for unchosen arms a = at. The consequence of this fact is discussed in more details in the next subsection. In the process above, the total T -trial payoff of A is defined as T t=1 rt,a t . Similarly, we define the optimal expected T -trial payoff as E T t=1 r t,a _ t , where a _ t is the arm with maximum expected payoff at trial t. Our goal is to design A so that the expected total payoff above is maximized. Equivalently, we may find an algorithm so that its regret with respect to the optimal arm-selection strategy is minimized. Here, the T -trial regret R A (T ) of algorithm A is defined formally by

An important special case of the general contextual bandit problem is the well-known K-armed bandit in which (i) the arm set At remains unchanged and contains K arms for all t, and (ii) the user ut (or equivalently, the context

is the same for all t. Since both the arm set and contexts are constant at every trial, they make no difference to a bandit algorithm, and so we will also refer to this type of bandit as a context-free bandit.

In the context of article recommendation, we may view articles in the pool as arms. When a presented article is clicked, a payoff of 1 is incurred; otherwise, the payoff is 0. With this definition of payoff, the expected payoff of an article is precisely its clickthrough rate (CTR), and choosing an article with maximum CTR is equivalent to maximizing the expected number of clicks from users, which in turn is the same as maximizing the total expected payoff in our bandit formulation.

Furthermore, in web services we often have access to user information which can be used to infer a user's interest and to choose news articles that are probably most interesting to her. For example, it is much more likely for a male teenager to be interested in an article about iPod products rather than retirement plans. Therefore, we may "summarize" users and articles by a set of informative features that describe them compactly. By doing so, a bandit algorithm can generalize CTR information from one article/user to another, and learn to choose good articles more quickly, especially for new users and articles.

## 2.2 Existing Bandit Algorithms

The fundamental challenge in bandit problems is the need for balancing exploration and exploitation. To minimize the regret in Eq. ( 1), an algorithm A exploits its past experience to select the arm that appears best. On the other hand, this seemingly optimal arm may in fact be suboptimal, due to imprecision in A's knowledge. In order to avoid this undesired situation, A has to explore by actually choosing seemingly suboptimal arms so as to gather more information about them (c.f., step 3 in the bandit process defined in the previous subsection). Exploration can increase short-term regret since some suboptimal arms may be chosen. However, obtaining information about the arms' average payoffs (i.e., exploration) can refine A's estimate of the arms' payoffs and in turn reduce long-term regret. Clearly, neither a purely exploring nor a purely exploiting algorithm works best in general, and a good tradeoff is needed.

The context-free K-armed bandit problem has been studied by statisticians for a long time [9,24,26]. One of the simplest and most straightforward algorithms is ǫ-greedy. In each trial t, this algorithm first estimates the average payoff μt,a of each arm a. Then, with probability 1 − ǫ, it chooses the greedy arm (i.e., the arm with highest payoff estimate); with probability ǫ, it chooses a random arm. In the limit, each arm will be tried infinitely often, and so the payoff estimate μt,a converges to the true value µa with probability 1. Furthermore, by decaying ǫ appropriately (e.g., [24]), the per-step regret, R A (T )/T , converges to 0 with probability 1.

In contrast to the unguided exploration strategy adopted by ǫgreedy, another class of algorithms generally known as upper confidence bound algorithms [4,7,17] use a smarter way to balance exploration and exploitation. Specifically, in trial t, these algorithms estimate both the mean payoff μt,a of each arm a as well as a corresponding confidence interval ct,a, so that |μt,a − µa| < ct,a holds with high probability. They then select the arm that achieves a highest upper confidence bound (UCB for short): at = arg maxa (μt,a + ct,a). With appropriately defined confidence intervals, it can be shown that such algorithms have a small total Ttrial regret that is only logarithmic in the total number of trials T , which turns out to be optimal [17].

While context-free K-armed bandits are extensively studied and well understood, the more general contextual bandit problem has remained challenging. The EXP4 algorithm [8] uses the exponential weighting technique to achieve an Õ( √ T ) regret, 2 but the computational complexity may be exponential in the number of features. Another general contextual bandit algorithm is the epochgreedy algorithm [18] that is similar to ǫ-greedy with shrinking ǫ. This algorithm is computationally efficient given an oracle optimizer but has the weaker regret guarantee of Õ(T 2/3 ).

Algorithms with stronger regret guarantees may be designed under various modeling assumptions about the bandit. Assuming the expected payoff of an arm is linear in its features, Auer [6] describes the LinRel algorithm that is essentially a UCB-type approach and shows that one of its variants has a regret of Õ( √ T ), a significant improvement over earlier algorithms [1].

Finally, we note that there exist another class of bandit algorithms based on Bayes rule, such as Gittins index methods [15]. With appropriately defined prior distributions, Bayesian approaches may have good performance. These methods require extensive offline engineering to obtain good prior models, and are often computationally prohibitive without coupling with approximation techniques [2].

# 3. ALGORITHM

Given asymptotic optimality and the strong regret bound of UCB methods for context-free bandit algorithms, it is tempting to devise similar algorithms for contextual bandit problems. Given some parametric form of payoff function, a number of methods exist to estimate from data the confidence interval of the parameters with which we can compute a UCB of the estimated arm payoff. Such an approach, however, is expensive in general.

In this work, we show that a confidence interval can be computed efficiently in closed form when the payoff model is linear, and call this algorithm LinUCB. For convenience of exposition, we first describe the simpler form for disjoint linear models, and then consider the general case of hybrid models in Section 3.2. We note LinUCB is a generic contextual bandit algorithms which applies to applications other than personalized news article recommendation.

## 3.1 LinUCB with Disjoint Linear Models

Using the notation of Section 2.1, we assume the expected payoff of an arm a is linear in its d-dimensional feature xt,a with some unknown coefficient vector θ θ θ \* a ; namely, for all t,

This model is called disjoint since the parameters are not shared 2 Note Õ(•) is the same as O(•) but suppresses logarithmic factors.

among different arms. Let Da be a design matrix of dimension m × d at trial t, whose rows correspond to m training inputs (e.g., m contexts that are observed previously for article a), and ba ∈ R m be the corresponding response vector (e.g., the corresponding m click/no-click user feedback). Applying ridge regression to the training data (Da, ca) gives an estimate of the coefficients:

where I d is the d × d identity matrix. When components in ca are independent conditioned on corresponding rows in Da, it can be shown [27] that, with probability at least 1 − δ,

for any δ > 0 and xt,a ∈ R d , where α = 1 + ln(2/δ)/2 is a constant. In other words, the inequality above gives a reasonably tight UCB for the expected payoff of arm a, from which a UCBtype arm-selection strategy can be derived: at each trial t, choose

where

The confidence interval in Eq. ( 4) may be motivated and derived from other principles. For instance, ridge regression can also be interpreted as a Bayesian point estimate, where the posterior distribution of the coefficient vector, denoted as p(θ θ θa), is Gaussian with mean θ θ θa and covariance A −1 a . Given the current model, the predictive variance of the expected payoff x ⊤ t,a θ θ θ \* a is evaluated as x ⊤ t,a A −1 a xt,a, and then x ⊤ t,a A −1 a xt,a becomes the standard deviation. Furthermore, in information theory [19], the differential entropy of p(θ θ θa) is defined as − 1 2 ln((2π) d det Aa). The entropy of p(θ θ θa) when updated by the inclusion of the new point xt,a then becomes − 1 2 ln((2π) d det (Aa + xt,ax ⊤ t,a )). The entropy reduction in the model posterior is 1 2 ln(1 + x ⊤ t,a A −1 a xt,a). This quantity is often used to evaluate model improvement contributed from xt,a. Therefore, the criterion for arm selection in Eq. ( 5) can also be regarded as an additive trade-off between the payoff estimate and model uncertainty reduction.

Algorithm 1 gives a detailed description of the entire LinUCB algorithm, whose only input parameter is α. Note the value of α given in Eq. ( 4) may be conservatively large in some applications, and so optimizing this parameter may result in higher total payoffs in practice. Like all UCB methods, LinUCB always chooses the arm with highest UCB (as in Eq. ( 5)).

This algorithm has a few nice properties. First, its computational complexity is linear in the number of arms and at most cubic in the number of features. To decrease computation further, we may update Aa t in every step (which takes O(d 2 ) time), but compute and cache Qa

(for all a) periodically instead of in realtime. Second, the algorithm works well for a dynamic arm set, and remains efficient as long as the size of At is not too large. This case is true in many applications. In news article recommendation, for instance, editors add/remove articles to/from a pool and the pool size remains essentially constant. Third, although it is not the focus of the present paper, we can adapt the analysis from [6] to show the following: if the arm set At is fixed and contains K arms, then the confidence interval (i.e., the right-hand side of Eq. ( 4)) decreases fast enough with more and more data, and then prove the strong regret bound of Õ( √ KdT ), matching the state-of-the-art result [6] for bandits satisfying Eq. ( 2). These theoretical results indicate fundamental soundness and efficiency of the algorithm.

Algorithm 1 LinUCB with disjoint linear models. 0: Inputs: α ∈ R+ 1: for t = 1, 2, 3, . . . , T do 2:

Observe features of all arms a ∈ At: xt,a ∈ R d 3:

for all a ∈ At do 4:

if a is new then 5:

Aa ← I d (d-dimensional identity matrix) 6:

ba ← 0 d×1 (d-dimensional zero vector) 7:

end for 11:

Choose arm at = arg maxa∈A t pt,a with ties broken arbitrarily, and observe a real-valued payoff rt 12:

13: ba t ← ba t + rtxt,a t 14: end for Finally, we note that, under the assumption that input features xt,a were drawn i.i.d. from a normal distribution (in addition to the modeling assumption in Eq. ( 2)), Pavlidis et al. [22] came up with a similar algorithm that uses a least-squares solution θ θ θa instead of our ridge-regression solution ( θ θ θa in Eq. ( 3)) to compute the UCB. However, our approach (and theoretical analysis) is more general and remains valid even when input features are nonstationary. More importantly, we will discuss in the next section how to extend the basic Algorithm 1 to a much more interesting case not covered by Pavlidis et al.

3.2 LinUCB with Hybrid Linear Models
Algorithm 1 (or the similar algorithm in [22]) computes the inverse of the matrix, D ⊤ a Da + I d (or D ⊤ a Da), where Da is again the design matrix with rows corresponding to features in the training data. These matrices of all arms have fixed dimension d × d, and can be updated efficiently and incrementally. Moreover, their inverses can be computed easily as the parameters in Algorithm 1 are disjoint: the solution θ θ θa in Eq. ( 3) is not affected by training data of other arms, and so can be computed separately. We now consider the more interesting case with hybrid models.

In many applications including ours, it is helpful to use features that are shared by all arms, in addition to the arm-specific ones. For example, in news article recommendation, a user may prefer only articles about politics for which this provides a mechanism. Hence, it is helpful to have features that have both shared and non-shared components. Formally, we adopt the following hybrid model by adding another linear term to the right-hand side of Eq. ( 2):

where zt,a ∈ R k is the feature of the current user/article combination, and β β β _ is an unknown coefficient vector common to all arms. This model is hybrid in the sense that some of the coefficients β β β _ are shared by all arms, while others θ θ θ \* a are not. For hybrid models, we can no longer use Algorithm 1 as the confidence intervals of various arms are not independent due to the shared features. Fortunately, there is an efficient way to compute an UCB along the same line of reasoning as in the previous section. The derivation relies heavily on block matrix inversion techniques. Due to space limitation, we only give the pseudocode in Algorithm 2 (where lines 5 and 12 compute the ridge-regression solution of the coefficients, and line 13 computes the confidence interval), and leave detailed derivations to a full paper. Here, we Algorithm 2 LinUCB with hybrid linear models. 0: Inputs: α ∈ R+ 1: A0 ← I k (k-dimensional identity matrix) 2: b0 ← 0 k (k-dimensional zero vector) 3: for t = 1, 2, 3, . . . , T do 4:

Observe features of all arms a ∈ At: (zt,a, xt,a) ∈ R k+d 5:

for all a ∈ At do 7:

if a is new then 8:

Aa ← I d (d-dimensional identity matrix) 9:

Ba ← 0 d×k (d-by-k zero matrix) 10:

ba ← 0 d×1 (d-dimensional zero vector) 11:

at ba t 24: end for only point out the important fact that the algorithm is computationally efficient since the building blocks in the algorithm (A0, b0, Aa, Ba, and ba) all have fixed dimensions and can be updated incrementally. Furthermore, quantities associated with arms not existing in At no longer get involved in the computation. Finally, we can also compute and cache the inverses (A −1 0 and A −1 a ) periodically instead of at the end of each trial to reduce the per-trial computational complexity to O(d 2 + k 2 ).

# 4. EVALUATION METHODOLOGY

Compared to machine learning in the more standard supervised setting, evaluation of methods in a contextual bandit setting is frustratingly difficult. Our goal here is to measure the performance of a bandit algorithm π, that is, a rule for selecting an arm at each time step based on the preceding interactions (such as the algorithms described above). Because of the interactive nature of the problem, it would seem that the only way to do this is to actually run the algorithm on "live" data. However, in practice, this approach is likely to be infeasible due to the serious logistical challenges that it presents. Rather, we may only have offline data available that was collected at a previous time using an entirely different logging policy. Because payoffs are only observed for the arms chosen by the logging policy, which are likely to often differ from those chosen by the algorithm π being evaluated, it is not at all clear how to evaluate π based only on such logged data. This evaluation problem may be viewed as a special case of the so-called "off-policy evaluation problem" in reinforcement learning (see, c.f., [23]).

One solution is to build a simulator to model the bandit process from the logged data, and then evaluate π with the simulator. However, the modeling step will introduce bias in the simulator and so make it hard to justify the reliability of this simulator-based evalu-ation approach. In contrast, we propose an approach that is simple to implement, grounded on logged data, and unbiased.

In this section, we describe a provably reliable technique for carrying out such an evaluation, assuming that the individual events are i.i.d., and that the logging policy that was used to gather the logged data chose each arm at each time step uniformly at random. Although we omit the details, this latter assumption can be weakened considerably so that any randomized logging policy is allowed and our solution can be modified accordingly using rejection sampling, but at the cost of decreased efficiency in using data.

More precisely, we suppose that there is some unknown distribution D from which tuples are drawn i.i.d. of the form (x1, ..., xK, r1, . . . , rK), each consisting of observed feature vectors and hidden payoffs for all arms. We also posit access to a large sequence of logged events resulting from the interaction of the logging policy with the world. Each such event consists of the context vectors x1, ..., xK , a selected arm a and the resulting observed payoff ra. Crucially, only the payoff ra is observed for the single arm a that was chosen uniformly at random. For simplicity of presentation, we take this sequence of logged events to be an infinitely long stream; however, we also give explicit bounds on the actual finite number of events required by our evaluation method.

Our goal is to use this data to evaluate a bandit algorithm π. Formally, π is a (possibly randomized) mapping for selecting the arm at at time t based on the history ht−1 of t−1 preceding events, together with the current context vectors xt1, ..., xtK.

Our proposed policy evaluator is shown in Algorithm 3. The method takes as input a policy π and a desired number of "good" events T on which to base the evaluation. We then step through the stream of logged events one by one. If, given the current history ht−1, it happens that the policy π chooses the same arm a as the one that was selected by the logging policy, then the event is retained, that is, added to the history, and the total payoff Rt updated. Otherwise, if the policy π selects a different arm from the one that was taken by the logging policy, then the event is entirely ignored, and the algorithm proceeds to the next event without any other change in its state.

Note that, because the logging policy chooses each arm uniformly at random, each event is retained by this algorithm with probability exactly 1/K, independent of everything else. This means that the events which are retained have the same distribution as if they were selected by D. As a result, we can prove that two processes are equivalent: the first is evaluating the policy against T real-world events from D, and the second is evaluating the policy using the policy evaluator on a stream of logged events. THEOREM 1. For all distributions D of contexts, all policies π, all T , and all sequences of events hT ,

where S is a stream of events drawn i.i.d. from a uniform random logging policy and D. Furthermore, the expected number of events obtained from the stream to gather a history hT of length T is KT .

This theorem says that every history hT has the identical probability in the real world as in the policy evaluator. Many statistics of these histories, such as the average payoff RT /T returned by Algorithm 3, are therefore unbiased estimates of the value of the algorithm π. Further, the theorem states that KT logged events are required, in expectation, to retain a sample of size T .

PROOF. The proof is by induction on t = 1, . . . , T starting with a base case of the empty history which has probability 1 when t = 0 Algorithm 3 Policy_Evaluator. 0: Inputs: T > 0; policy π; stream of events Rt ← Rt−1 + ra 9: end for 10: Output: RT /T under both methods of evaluation. In the inductive case, assume that we have for all t − 1:

and want to prove the same statement for any history ht. Since the data is i.i.d. and any randomization in the policy is independent of randomization in the world, we need only prove that conditioned on the history ht−1 the distribution over the t-th event is the same for each process. In other words, we must show:

Since the arm a is chosen uniformly at random in the logging policy, the probability that the policy evaluator exits the inner loop is identical for any policy, any history, any features, and any arm, implying this happens for the last event with the probability of the last event, PrD(xt,1, ..., xt,K, rt,a). Similarly, since the policy π's distribution over arms is independent conditioned on the history ht−1 and features (xt,1, ..., xt,K ), the probability of arm a is just Pr π(h t−1 ) (a|xt,1, ..., xt,K ). Finally, since each event from the stream is retained with probability exactly 1/K, the expected number required to retain T events is exactly KT .

# 5. EXPERIMENTS

In this section, we verify the capacity of the proposed LinUCB algorithm on a real-world application using the offline evaluation method of Section 4. We start with an introduction of the problem setting in Yahoo! Today-Module, and then describe the user/item attributes we used in experiments. Finally, we define performance metrics and report experimental results with comparison to a few standard (contextual) bandit algorithms.

## 5.1 Yahoo! Today Module

The Today Module is the most prominent panel on the Yahoo! Front Page, which is also one of the most visited pages on the Internet; see a snapshot in Figure 1 . The default "Featured" tab in the Today Module highlights one of four high-quality articles, mainly news, while the four articles are selected from an hourly-refreshed article pool curated by human editors. As illustrated in Figure 1 , there are four articles at footer positions, indexed by F1-F4. Each article is represented by a small picture and a title. One of the four articles is highlighted at the story position, which is featured by a large picture, a title and a short summary along with related links. By default, the article at F1 is highlighted at the story position. A user can click on the highlighted article at the story position to read more details if she is interested in the article. The event is recorded as a story click. To draw visitors' attention, we would like to rank available articles according to individual interests, and highlight the most attractive article for each visitor at the story position.

## 5.2 Experiment Setup

This subsection gives a detailed description of our experimental setup, including data collection, feature construction, performance evaluation, and competing algorithms.

### 5.2.1 Data Collection

We collected events from a random bucket in May 2009. Users were randomly selected to the bucket with a certain probability per visiting view. 3 In this bucket, articles were randomly selected from the article pool to serve users. To avoid exposure bias at footer positions, we only focused on users' interactions with F1 articles at the story position. Each user interaction event consists of three components: (i) the random article chosen to serve the user, (ii) user/article information, and (iii) whether the user clicks on the article at the story position. Section 4 shows these random events can be used to reliably evaluate a bandit algorithm's expected payoff.

There were about 4.7 million events in the random bucket on May 01. We used this day's events (called "tuning data") for model validation to decide the optimal parameter for each competing bandit algorithm. Then we ran these algorithms with tuned parameters on a one-week event set (called "evaluation data") in the random bucket from May 03-09, which contained about 36 million events.

### 5.2.2 Feature Construction

We now describe the user/article features constructed for our experiments. Two sets of features for the disjoint and hybrid models, respectively, were used to test the two forms of LinUCB in Section 3 and to verify our conjecture that hybrid models can improve learning speed.

We start with raw user features that were selected by "support". The support of a feature is the fraction of users having that feature. To reduce noise in the data, we only selected features with high support. Specifically, we used a feature when its support is at least 0.1. Then, each user was originally represented by a raw feature vector of over 1000 categorical components, which include: (i) demographic information: gender (2 classes) and age discretized into 10 segments; (ii) geographic features: about 200 metropolitan locations worldwide and U.S. states; and (iii) behavioral categories: about 1000 binary categories that summarize the user's consumption history within Yahoo! properties. Other than these features, no other information was used to identify a user.

Similarly, each article was represented by a raw feature vector of about 100 categorical features constructed in the same way. These features include: (i) URL categories: tens of classes inferred from the URL of the article resource; and (ii) editor categories: tens of topics tagged by human editors to summarize the article content.

We followed a previous procedure [12] to encode categorical user/article features as binary vectors and then normalize each feature vector to unit length. We also augmented each feature vector with a constant feature of value 1. Now each article and user was represented by a feature vector of 83 and 1193 entries, respectively.

To further reduce dimensionality and capture nonlinearity in these raw features, we carried out conjoint analysis based on random exploration data collected in September 2008. Following a previous approach to dimensionality reduction [13], we projected user features onto article categories and then clustered users with similar preferences into groups. More specifically:

• We first used logistic regression (LR) to fit a bilinear model for click probability given raw user/article features so that φ φ φ ⊤ u Wφ φ φa approximated the probability that the user u clicks on article a, where φ φ φu and φ φ φa were the corresponding feature vectors, and W was a weight matrix optimized by LR.

• Raw user features were then projected onto an induced space by computing ψ ψ ψu

Here, the i th component in ψ ψ ψu for user u may be interpreted as the degree to which the user likes the i th category of articles. K-means was applied to group users in the induced ψ ψ ψu space into 5 clusters.

• The final user feature was a six-vector: five entries corresponded to membership of that user in these 5 clusters (computed with a Gaussian kernel and then normalized so that they sum up to unity), and the sixth was a constant feature 1. At trial t, each article a has a separate six-dimensional feature xt,a that is exactly the six-dimensional feature constructed as above for user ut. Since these article features do not overlap, they are for disjoint linear models defined in Section 3.

For each article a, we performed the same dimensionality reduction to obtain a six-dimensional article feature (including a constant 1 feature). Its outer product with a user feature gave 6 × 6 = 36 features, denoted zt,a ∈ R 36 , that corresponded to the shared features in Eq. ( 6), and thus (zt,a, xt,a) could be used in the hybrid linear model. Note the features zt,a contains user-article interaction information, while xt,a contains user information only.

Here, we intentionally used five users (and articles) groups, which has been shown to be representative in segmentation analysis [13]. Another reason for using a relatively small feature space is that, in online services, storing and retrieving large amounts of user/article information will be too expensive to be practical.

5.3 Compared Algorithms
The algorithms empirically evaluated in our experiments can be categorized into three groups: I. Algorithms that make no use of features. These correspond to the context-free K-armed bandit algorithms that ignore all contexts (i.e., user/article information).

• random: A random policy always chooses one of the candidate articles from the pool with equal probability. This algorithm requires no parameters and does not "learn" over time. • ǫ-greedy: As described in Section 2.2, it estimates each article's CTR; then it chooses a random article with probability ǫ, and chooses the article of the highest CTR estimate with probability 1 − ǫ. The only parameter of this policy is ǫ. • ucb: As described in Section 2.2, this policy estimates each article's CTR as well as a confidence interval of the estimate, and always chooses the article with the highest UCB. Specifically, following UCB1 [7], we computed an article a's confidence interval by ct,a = α √ nt,a , where nt,a is the number of times a was chosen prior to trial t, and α > 0 is a parameter.

• omniscient: Such a policy achieves the best empirical context-free CTR from hindsight. It first computes each article's empirical CTR from logged events, and then always chooses the article with highest empircal CTR when it is evaluated using the same logged events. This algorithm requires no parameters and does not "learn" over time. II. Algorithms with "warm start"-an intermediate step towards personalized services. The idea is to provide an offline-estimated user-specific adjustment on articles' context-free CTRs over the whole traffic. The offset serves as an initialization on CTR estimate for new content, a.k.a."warm start". We re-trained the bilinear logistic regression model studied in [12] on Sept 2008 random traffic data, using features zt,a constructed above. The selection criterion then becomes the sum of the context-free CTR estimate and a bilinear term for a user-specific CTR adjustment. In training, CTR was estimated using the context-free ǫ-greedy with ǫ = 1.

• ǫ-greedy (warm): This algorithm is the same as ǫ-greedy except it adds the user-specific CTR correction to the article's context-free CTR estimate. • ucb (warm): This algorithm is the same as the previous one but replaces ǫ-greedy with ucb. III. Algorithms that learn user-specific CTRs online.

• ǫ-greedy (seg): Each user is assigned to the closest user cluster among the five constructed in Section 5.2.2, and so all users are partitioned into five groups (a.k.a. user segments), in each of which a separate copy of ǫ-greedy was run.

• ucb (seg): This algorithm is similar to ǫ-greedy (seg) except it ran a copy of ucb in each of the five user segments. • ǫ-greedy (disjoint): This is ǫ-greedy with disjoint models, and may be viewed as a close variant of epoch-greedy [18]. • linucb (disjoint): This is Algorithm 1 with disjoint models.

• ǫ-greedy (hybrid): This is ǫ-greedy with hybrid models, and may be viewed as a close variant of epoch-greedy. • linucb (hybrid): This is Algorithm 2 with hybrid models.

5.4 Performance Metric
An algorithm's CTR is defined as the ratio of the number of clicks it receives and the number of steps it is run. We used all algorithms' CTRs on the random logged events for performance comparison. To protect business-sensitive information, we report an algorithm's relative CTR, which is the algorithm's CTR divided by the random policy's. Therefore, we will not report a random policy's relative CTR as it is always 1 by definition. For convenience, we will use the term "CTR" from now on instead of "relative CTR".

For each algorithm, we are interested in two CTRs motivated by our application, which may be useful for other similar applications. When deploying the methods to Yahoo!'s front page, one reasonable way is to randomly split all traffic to this page into two buckets [3]. The first, called "learning bucket", usually consists of a small fraction of traffic on which various bandit algorithms are run to learn/estimate article CTRs. The other, called "deployment bucket", is where Yahoo! Front Page greedily serves users using CTR estimates obained from the learning bucket. Note that "learning" and "deployment" are interleaved in this problem, and so in every view falling into the deployment bucket, the article with the highest current (user-specific) CTR estimate is chosen; this estimate may change later if the learning bucket gets more data. CTRs in both buckets were estimated with Algorithm 3. Since the deployment bucket is often larger than the learning bucket, CTR in the deployment bucket is more important. However, a higher CTR in the learning bucket suggests a faster learning rate (or equivalently, smaller regret) for a bandit algorithm. Therefore, we chose to report algorithm CTRs in both buckets.

### 5.5.1 Results for Tuning Data

Each of the competing algorithms (except random and omniscient) in Section 5.3 requires a single parameter: ǫ for ǫ-greedy algorithms and α for UCB ones. We used tuning data to optimize these parameters. Figure 2 shows how the CTR of each algorithm changes with respective parameters. All results were obtained by a single run, but given the size of our dataset and the unbiasedness result in Theorem 1, the reported numbers are statistically reliable.

First, as seen from Figure 2 , the CTR curves in the learning buckets often possess the inverted U-shape. When the parameter (ǫ or α) is too small, there was insufficient exploration, the algorithms failed to identify good articles, and had a smaller number of clicks. On the other hand, when the parameter is too large, the algorithms appeared to and thus wasted some of the opportunities to increase the number of clicks. Based on these plots on tuning data, we chose appropriate parameters for each algorithm and ran it once on the evaluation data in the next subsection.

Second, it can be concluded from the plots that warm-start information is indeed helpful for finding a better match between user interest and article content, compared to the no-feature versions of ǫ-greedy and UCB. Specifically, both ǫ-greedy (warm) and ucb (warm) were able to beat omniscient, the highest CTRs achievable by context-free policies in hindsight. However, performance of the two algorithms using warm-start information is not as stable as algorithms that learn the weights online. Since the offline model for "warm start" was trained with article CTRs estimated on all random traffic [12], ǫ-greedy (warm) gets more stable performance in the deployment bucket when ǫ is close to 1. The warm start part also helps ucb (warm) in the learning bucket by selecting more attractive articles to users from scratch, but did not help ucb (warm) in determining the best online for deployment. Since ucb relies on the a confidence interval for exploration, it is hard to correct the initialization bias introduced by "warm start". In contrast, all online-learning algorithms were able to consistently beat the omniscient policy. Therefore, we did not try the warm-start algorithms on the evaluation data.

Third, ǫ-greedy algorithms (on the left of Figure 2 ) achieved similar CTR as upper confidence bound ones (on the right of Figure 2 ) in the deployment bucket when appropriate parameters were used. Thus, both types of algorithms appeared to learn comparable policies. However, they seemed to have lower CTR in the learning bucket, which is consistent with the empirical findings of contextfree algorithms [2] in real bucket tests.

Finally, to compare algorithms when data are sparse, we repeated the same parameter tuning process for each algorithm with fewer data, at the level of 30%, 20%, 10%, 5%, and 1%. Note that we still used all data to evaluate an algorithm's CTR as done in Algorithm 3, but then only a fraction of available data were randomly chosen to be used by the algorithm to improve its policy.

### 5.5.2 Results for Evaluation Data

With parameters optimized on the tuning data (c.f., Figure 2 ), we ran the algorithms on the evaluation data and summarized the CTRs in Table 1 . The table also reports the CTR lift compared to the baseline of ǫ-greedy. The CTR of omniscient was 1.615, and so a significantly larger CTR of an algorithm indicates its effective use of user/article features for personalization. Recall that the reported CTRs were normalized by the random policy's CTR. We examine the results more closely in the following subsections.

On the Use of Features.
We first investigate whether it helps to use features in article recommendation. It is clear from Table 1 that, by considering user features, both ǫ-greedy (seg/disjoint/hybrid) and UCB methods (ucb (seg) and linucb (disjoint/hybrid)) were able to achieve a CTR lift of around 10%, compared to the baseline ǫ-greedy.

To better visualize the effect of features, Figure 3 shows how an article's CTR (when chosen by an algorithm) was lifted compared to its base CTR (namely, the context-free CTR). 4 Here, an article's base CTR measures how interesting it is to a random user, and was estimated from logged events. Therefore, a high ratio of the lifted and base CTRs of an article is a strong indicator that an algorithm does recommend this article to potentially interested users. the other three plots show clear benefits by considering personalized recommendation. In an extreme case (Figure 3 (c)), one of the article's CTR was lifted from 1.31 to 3.03-a 132% improvement. Furthermore, it is consistent with our previous results on tuning data that, compared to ǫ-greedy algorithms, UCB methods achieved higher CTRs in the deployment bucket, and the advantage was even greater in the learning bucket. As mentioned in Section 2.2, ǫgreedy approaches are unguided because they choose articles uniformly at random for exploration. In contrast, exploration in upper confidence bound methods are effectively guided by confidence intervals-a measure of uncertainty in an algorithm's CTR estimate. Our experimental results imply the effectiveness of upper confidence bound methods and we believe they have similar benefits in many other applications as well.

On the Size of Data.
One of the challenges in personalized web services is the scale of the applications. In our problem, for example, a small pool of news articles were hand-picked by human editors. But if we wish to allow more choices or use automated article selection methods to determine the article pool, the number of articles can be too large even for the high volume of Yahoo! traffic. Therefore, it becomes critical for an algorithm to quickly identify a good match between user interests and article contents when data are sparse. In our experiments, we artificially reduced data size (to the levels of 30%, 20%, 10%, 5%, and 1%, respectively) to mimic the situation where we have a large article pool but a fixed volume of traffic.

To better visualize the comparison results, we use bar graphs in Figure 4 to plot all algorithms' CTRs with various data sparsity levels. A few observations are in order. First, at all data sparsity levels, features were still useful. At the level of 1%, for instance, we observed a 10.3% improvement of linucb (hybrid)'s CTR in the deployment bucket (1.493) over ucb's (1.354).

Second, UCB methods consistently outperformed ǫ-greedy ones in the deployment bucket. 5 The advantage over ǫ-greedy was even more apparent when data size was smaller.

Third, compared to ucb (seg) and linucb (disjoint), linucb (hybrid) showed significant benefits when data size was small. Recall that in hybrid models, some features are shared by all articles, making it possible for CTR information of one article to be "transferred" to others. This advantage is particularly useful when the article pool is large. In contrast, in disjoint models, feedback of one article may not be utilized by other articles; the same is true for ucb (seg). Figure 4 (a) shows transfer learning is indeed helpful when data are sparse.

Comparing ucb (seg) and linucb (disjoint).

From Figure 4 (a), it can be seen that ucb (seg) and linucb (disjoint) had similar performance. We believe it was no coincidence. Recall that features in our disjoint model are actually normalized membership measures of a user in the five clusters described in Section 5.2.2. Hence, these features may be viewed as a "soft" version of the user assignment process adopted by ucb (seg).

Figure 5 plots the histogram of a user's relative membership measure to the closest cluster, namely, the largest component of the user's five, non-constant features. It is clear that most users were quite close to one of the five cluster centers: the maximum membership of about 85% users were higher than 0.5, and about 40% of them were higher than 0.8. Therefore, many of these features have a highly dominating component, making the feature vector similar to the "hard" version of user group assignment.

We believe that adding more features with diverse components, such as those found by principal component analysis, would be necessary to further distinguish linucb (disjoint) from ucb (seg).

# 6. CONCLUSIONS

This paper takes a contextual-bandit approach to personalized web-based services such as news article recommendation. We proposed a simple and reliable method for evaluating bandit algorithms directly from logged events, so that the often problematic simulator-building step could be avoided. Based on real Yahoo! Front Page traffic, we found that upper confidence bound methods generally outperform the simpler yet unguided ǫ-greedy methods. Furthermore, our new algorithm LinUCB shows advantages when data are sparse, suggesting its effectiveness to personalized web services when the number of contents in the pool is large.

In the future, we plan to investigate bandit approaches to other similar web-based serviced such as online advertising, and compare our algorithms to related methods such as Banditron [16]. A second direction is to extend the bandit formulation and algorithms in which an "arm" may refer to a complex object rather than an item (like an article). An example is ranking, where an arm corresponds to a permutation of retrieved webpages. Finally, user interests change over time, and so it is interesting to consider temporal information in bandit algorithms.

acknowledgement
We thank Deepak Agarwal, Bee-Chung Chen, Daniel Hsu, and Kishore Papineni for many helpful discussions, István Szita and Tom Walsh for clarifying their algorithm, and Taylor Xi and the anonymous reviewers for suggestions that improved the presentation of the paper.
