## link

- https://dl.acm.org/doi/pdf/10.1145/3460231.3474236

## title

Values of User Exploration in Recommender Systems

## abstract

Reinforcement Learning (RL) has been sought after to bring next-generation recommender systems to further improve user experience on recommendation platforms. While the exploration-exploitation tradeoff is the foundation of RL research, the value of exploration in (RL-based) recommender systems is less well understood. Exploration, commonly seen as a tool to reduce model uncertainty in regions of sparse user interaction/feedback, is believed to cost user experience in the short term, while the indirect benefit of better model quality arrives at a later time. We focus on another aspect of exploration, which we refer to as user exploration to help discover new user interests, and argue it can improve user experience even in the more imminent term.

We examine the role of user exploration in changing different facets of recommendation quality that more directly impact user experience. To do so, we introduce a series of methods inspired by exploration research in RL to increase user exploration in an RL-based recommender system, and study their effect on the end recommendation quality, more specifically, on accuracy, diversity, novelty and serendipity. We propose a set of metrics to measure (RL based) recommender systems in these four aspects and evaluate the impact of exploration-induced methods against these metrics. In addition to the offline measurements, we conduct live experiments on an industrial recommendation platform serving billions of users to showcase the benefit of user exploration. Moreover, we use conversion of casual users to core users as an indicator of the holistic long-term user experience and study the values of user exploration in helping platforms convert users. Through offline analyses and live experiments, we study the correlation between these four facets of recommendation quality and long term user experience, and connect serendipity to improved long term user experience.

# Introduction

In the era of increasing choices, recommender systems are becoming indispensable in helping users navigate the million or billion pieces of contents available on recommendation platforms. These systems are built to satisfy users’ information needs by anticipating what they would be interested in consuming next. Collaborative filtering [28, 47] and supervised learning based approaches predicting users’ immediate response toward recommendations [12, 65] such as clicks, dwell time, likes, have had enormous successes. Researchers however are becoming increasingly aware of the limitations of such approaches. First, focus on driving short-term engagements such as user clicks fails to account for the long term impact of a recommendation. Second, lack of exploration causes these systems to increasingly concentrate on the known user interests and create satiation effect, i.e., reduced enjoyment of the content.

Reinforcement learning (and bandits) techniques have emerged as appealing alternatives [11, 23, 67, 68] over the years. Compared with supervised learning based approaches, RL offers two advantages: 1) Exploration. (Online) RL algorithms inherently explore regions they are less certain about. This provides a natural mechanism to deviate from the current system behavior, and introduce previously unseen contents to users; 2) Long-term user experience optimization. As the planning horizon of these RL agents extends, the recommender naturally shifts its focus from short-term user engagement toward optimizing the long-term user experience on the platform. We focus our discussion on exploration, though as we show in the analyses it innately connects to the long-term user experience.

The tradeoff between exploration and exploitation is central to the design of RL agents [17, 57]. An agent learns to form a policy to maximize returns in a changing environment by taking actions and receiving reward/feedback from the environment. The agent is incentivized to exploit, repeating actions taken in the past that produced higher rewards, to maximize reward. On the other hand, the agent needs to explore previously unseen actions in order to discover potentially better options. Exploration in RL based recommender systems serves a similar goal, that is to expose users to previously unseen items to discover contents the user is potentially interested in. The benefit of exploration to counter the selection bias of existing systems and generate training data to reduce model uncertainty has been established [11]. Here we focus on another aspect of exploration that we refer to as user exploration, i.e., exploration for discovering something new for the user.

As exploration innately leads to recommending something less pertinent to the known user interests, it is often seen as a cost to user experience, especially in the short term. Here we argue that recommender systems have an inherent need for exploration as users perceive other factors of recommendation quality besides accuracy [5, 66]. We dissect the values of user exploration by examining its role in changing different aspects of recommendation quality that impact the user experience on recommendation platforms. Together, we make the following contributions:

- Methods to Introduce User Exploration: We introduce a collection of methods, inspired by exploration research in RL, to improve user exploration in recommender systems.
- Metrics: We propose a set of metrics measuring the different aspects of recommendation quality, that is accuracy, diversity, novelty and serendipity for RL based recommender systems.
- Offline Analyses: We conduct an extensive set of offline analyses to understand the values of user exploration in changing the four aspects of recommendation quality.
- Live Experiments: We conduct live experiments of the proposed methods on a commercial recommendation platform serving billions of users and millions of items, and showcase the value of user exploration in improving long-term user experience on the platform.
- Serendipity for Long Term User Experience: Through offline analyses and live experiments, we study the correlation between these four aspects of recommendation quality and the long term user experience. Using conversion of casual users to core users as an indicator of the holistic long term user experience, we connect serendipity to improved long term user experience.

# Related Work

Reinforcement Learning for Recommender Systems. Deep reinforcement learning, combining high-capacity function approximators, i.e., deep neural networks, with the mathematical formulations in classic reinforcement learning [57], has achieved enormous success in various domains such as games, robotics and hardware design [18, 33, 36, 52]. It has attracted a lot of attention from the recommeder system research community as well. Shani et al. [51] were among the first to formally formulate recommendation as a Markov decision process (MDP) and experiment with model-based RL approaches for book recommendation. Zheng et al. [70] applied DQN for news recommendation. Dulac-Arnold et al. [14] enabled RL in problem spaces with a large number of discrete actions and showcased its performance on various recommendation tasks with tens of thousands of actions. Liu et al. [34] tested actor-critic approaches on recommendation datasets such as MovieLens, Yahoo Music and Jester. Set recommendation using RL has been studied in [11, 23, 69]. In recent years, we also start seeing success of RL in real-world recommendation applications. Chen et al. [11] scaled a batch RL algorithm, i.e., REINFORCE with off-policy correction to a commercial platform serving billions of users and tens of millions of contents. Hu et al. [22] tested an extension of the deep deterministic policy gradient (DDPG) method for learning to rank on Taobao, a commercial search platform.

Exploration in Reinforcement Learning. The exploration/exploitation dilemma has long been studied in multi-armed bandits and classic reinforcement learning [17, 57]. Exploration methods are concerned with reducing agents’ uncertainty of the environment reward and/or the dynamics. For the stochastic bandits problems, Upper Confidence Bound (UCB) [30] and Thompson Sampling (TS) [4, 10, 59] are among the most well known techniques with both theoretical guarantees and empirical successes. In classic reinforcement learning with tabular settings, count-based exploration techniques quantifying the uncertainty based on the inverse square root of the state-action visit count, can be seen as extension of these techniques to Markov Decision Processes (MDPs). Tang et al. [58] further generalizes counted-based methods to deep RL with highdimensional state spaces. Another camp of methods, commonly referred to as intrinsic motivation [21, 24, 48, 56], encourages the agents to explore regions leading up to surprises. The surprise factor is often measured by the agents’ predictive errors on environment reward or dynamics, or equivalently information gain the agents can acquire by taking an action under the current state. Bellemare et al. [6] unifies count-based exploration and intrinsic motivation through the lens of information gain or learning progress. Our work takes inspiration from these existing works, and re-designs the algorithms to fit more closely with the recommendation setup.

Diversity, Novelty and Serendipity of Recommender Systems. While early recommendation research has focused almost exclusively on improving recommendation accuracy, it has become increasingly recognized that there are other factors of recommendation quality contributing to the overall user experience on the platform. Herlocker et al. [19] in their seminal work of evaluating collaborative filtering based recommender systems defined various metrics to measure recommendation accuracy, coverage, novelty as well as serendipity. Diversity is another important aspect that has been extensively studied [3, 5]. Diversification algorithms are used to increase coverage of the full range of user interests, and to counter the saturation effect of consuming similar contents [72]. Zhou et al. [71] studied the dilemma between accuracy and diversity, and proposed a hybrid approach to balance the two. Novelty [8] is closely related to long tail recommendation [62], measuring the capacity of the recommender systems to make predictions and reach the full inventory of contents available on the platforms. One of the early definitions of serendipity was introduced in [19], which captures the degree to which a recommendation is both relevant and surprising to users. Zhang et al. [66] proposed a hybrid rank-interpolation approach to combine outputs of three LDA algorithms [7] focusing on either accuracy, diversity or serendipity to achieve a balance between these factors in the end recommendations. Oku and Hattori [41] proposed a fusion based technique to mix items users expressed interest on based on item attributes in order to introduce serendipitous contents. Our work measures the effect of exploration on recommendation accuracy, diversity, novelty and serendipity, and connects these factors to long term user experience.

# Background

We base our work on the REINFORCE recommender system introduced in [11], in which the authors framed a set recommendation problem as a Markov Decision Process (MDP) (S, A, P, R, ρ0,γ ). Here S is the state space capturing the user interests and context, A is the discrete action space containing items available for recommendation, P : S × A × S → R is the state transition probability, and R : S × A → R is the reward function, with r(s, a) note the immediate reward of action a under state s. ρ0 is the initial state distribution, and γ the discount for future rewards. Let Ht = {(A0, a0,r0), · · · , (At−1, at−1,rt−1)} denote an user’s historical activities on the platform up to time t, where At ′ stands for the set of items recommended to the user at time t ′ , at ′ denotes the item the user interacted with at t ′ (at ′ can be null), and rt ′ captures the user feedback (reward) on at ′ (rt ′ = 0 if the user did not interact with any item in At ′). The history Ht is encoded through a recurrent neural network to capture the latent user state, that is, ust = RNNθ (Ht ). Given the latent user state, a softmax policy over the item corpus A is parameterized as

$$
\tag{1}
$$

which defines a distribution over the item corpus A conditioning on the user state st at time t. Here va stands for the embedding of the item a. The agent then generates a set of recommendation At to user at time t according to the learned softmax policy πθ (·|st ). The policy parameters θ are learned using REINFORCE [60] so as to maximize the expected cumulative reward over the user trajectories,

$$
\tag{2}
$$

where Rt = Ir(st ,at )>0 · ÍT t ′=t γ t ′−t r(st ′, at ′) is the discounted cumulative reward starting from time t.

RL was designed as an online learning paradigm in the first place [57]. Note that the expectation in eq. 2 is taken over the trajectories generated according to the learned policy, and d πθ t (s) is the discounted state visitation probability under πθ [32]. One of the main contribution of [11] is bringing the REINFORCE algorithm to the offline batch learning setup commonly deployed in industrial recommender systems. The authors applied a first-order approximation [2] of importance sampling to address the distribution shift caused by offline training, resulting in a gradient of the following:

$$
\tag{3}
$$

Here β(·|s) denotes the behavior policy, i.e., the action distribution conditioning on state s in the batch collected trajectories. d β t (s) is the discounted state visitation probability under β. This importance weight is further adapted to accommodate the set recommendation setup. We refer interested readers to [11] for more details.

To balance exploration and exploitation, a hybrid approach that returns the top K ′ most probable items, while sampling the rest K −K ′ items according to πθ (Boltzmann exploration [13]), is employed during serving.

# Method

Here we introduce three simple methods inspired by exploration research in RL to increase user exploration in the REINFORCE recommender system during training. That is, to recommend content less pertinent to the known user interests, and to discover new user interests.

## Entropy Regularization

The first method promotes recommending contents less pertinent to the known user interests by encouraging the policy πθ (·|s) to have an output distribution with high entropy [61]. Mnih et al. [38] observed that adding entropy of the policy to the objective function discourages premature convergence to sub-optimal deterministic policies and leads to better performance. Pereyra et al. [46] conducted a systemic study of entropy regularization and found it to improve a wide range of state-of-the-art models.


We add of the entropy to the RL learning objective as defined in eq. 2 during training. That is,

$$
\tag{4}
$$

where the entropy of the conditional distribution πθ (·|s) is defined as H (πθ (·|s)) = − Í a ∈A πθ (a|s) log πθ (a|s). Here α controls the strength of the regularization. The entropy is equivalent to the negative reverse KL divergence of the conditional distribution πθ (·|s) to the uniform distribution. That is, H (πθ (·|s)) = −DK L(πθ (·|s)||U ) + const, where U stands for a uniform distribution across the action space A. As we increase this regularization, it pushes the learned policy to be closer to a uniform distribution, thus promoting exploration.

## Intrinsic Motivation and Reward Shaping

The second method helps discovering new user interests through reward shaping. The reward function r(s, a) as defined in eq. 2, describes the (immediate) value of a recommendation a to a user s. It plays a critical role in deciding the learned policy πθ . Reward shaping, transforming or supplying additional rewards beyond those provided by the MDP, is very effective in guiding the learning of RL agents to produce policies desired by the algorithm designers [1, 27, 40].

Exploration has been extensively studied in RL [6, 42–44, 55], and has been shown to be extremely useful in solving hard tasks, e.g., tasks with sparse reward and/or long horizons, and . These works can be roughly grouped into two categories. One concerns quantifying the uncertainty of the value function of the state-action pairs so the agent can direct its exploration on regions where it is most uncertain. The other uses a qualitative notion of curiosity or intrinsic motivation to encourage the agent to explore its environment and learn skills that might be useful later. Both camps of methods later adds an intrinsic reward r i (s, a), either capturing the uncertainty or curiosity to the extrinsic reward r e (s, a) that is emitted by the environment directly, to help the agent explore the unknown or learn new skills. That is, transforming the reward function to

$$
\tag{5}
$$

where c controls the relative importance of the intrinsic reward w.r.t. the extrinsic reward emitted by the environment.

Schmidhuber [49] formally captures the theory of creativity, fun and curiosity as an intrinsic desire to discover surprising patterns of the environment, and argues that a curiosity-driven agent can learn even in the absence of external reward. Our proposal bears the same principle by rewarding the agent more when it discovers some previously unknown patterns of the environment, that is the user. Let R e t (st , at ) = Ir e (st ,at )>0 · ÍT t ′=t γ t ′−t r e (st ′, at ′) be the discounted cumulation of the extrinsic reward on the stateaction pair (st , at ) observed on the trajectory. We then define the cumulative reward Rt (st , at ) used for the gradient update in eq. 3 as

$$
\tag{6}
$$

Here c > 1 is a constant multiplier.

As explained in Section 3, the agent perceives the environment, that is the user interests and context, through encoding user’s historical activities Ht = {(A0, a0,r0), · · · , (At−1, at−1,rt−1)}. One can imagine a large update (surprise) to the agent’s modeling of the environment if an item at recommended given the state st is 1) drastically different from any of the items the user interacted with in the past; 2) enjoyed by the user, i.e., r e (st , at ) or R e (st , at ) is high. These two conditions, surprise and relevance, align with the serendipity metrics we are going to detail in Section 5.5.

To measure the surprise of at , we define It = {at ′, ∀t ′ < t and rt ′ > 0} as the set of items the user interacted with up to time t. As recommendation items are often associated with various attributes as described in Section 5.1, we use these attributes to measure the similarity (or difference) of a candidate action at towards It . For example, we consider an item at surprising (different) if its topic cluster is different from any of the items in It .

The multiplicative design in eq. 6 naturally accomplishes the second condition, that is, relevance. Comparing with the additive form (eq. 5), the multiplicative design results in: 1) a candidate action at with zero extrinsic reward, i.e., R e t (st , at ) = 0 will NOT receive any additional reward even if being under-surfaced; 2) an action at receiving higher extrinsic reward R e t (st , at ) will be rewarded even more compared with those that are equally surprising but received lower extrinsic reward. This contrasts with the additive form where the extrinsic rewards observed does not influence the intrinsic reward. In other words, the additive design gives a uniform boost to actions based entirely on surprise. The multiplicative design on the other end, favors surprising actions that actually lead to improved user experience, indicated by higher extrinsic reward.

## Actionable Representation for Exploration

The third method reinforces the newly discovered user interest through representation learning. Learning effective representation is critical to improve the sample efficiency of many machine learning algorithms, and RL is no exception. Most prior work on representation learning for RL has focused on generative approaches, learning representations that capture all underlying factors of variation in the observation space in a more disentangled or well-ordered manner. Self-supervised learning [20, 25, 50, 54] to capture the full dynamics of the environment has also attracted a lot of attentions lately. Ghosh et al. [16] instead argue to learn functionally salient representations: representations that are not necessarily complete in terms of capturing all factors of variation in the observation space, but rather aim to capture those factors of variation that are important for decision making – that are "actionable."

The REINFORCE agent introduced in Section 3 describes the environment, i.e., the user, through encoding his/her historical activities Ht . That is, ust = RNNθ (Ht ). When an user interacted with a surprising item at (to the agent) and gave high reward, the user state ust should be updated to capture the new information so the agent can act differently next. That is, to make recommendations according to the newly acquired information about the new interest of the user. To aid the agent in capturing this information in its state, we extend Ht with an additional bit, indicating whether or not an item the user interacts with is surprising and relevant. That is, we expand Ht = {(A0, a0,r0,i0), · · · , (At−1, at−1,rt−1,it−1)}, where it ′ = 1 if 1) the attribute of at (such as topic cluster) is different from that of any items in It ′ (being a surprise) and; 2) rt > 0 (being relevant). Here It ′ is the list of items the user has interacted with up to time t ′ . This feature is then embedded and consumed by the RNN along with other features describing the item at.

# Measurement

Personalization has been the cornerstone of modern recommender systems. It aims to produce targeted and accurate recommendations based on user historical activities. Overly focusing on the accuracy aspect of recommendation, however, runs the risk of exposing users only to a concentrated set of contents. This could attract user attention in the near term, but likely hurt user experience in the long run. There has been a growing body of work examining factors other than accuracy in shaping user’s perception of recommendation quality [9, 19, 35, 66, 72, 72]. In particular, aspects such as diversity, novelty and serendipity of recommendations have been studied. Here we design metrics to measure these four aspects for a RL based recommender system. Some of the metrics measure directly on the learned policy πθ , and thus apply only to systems producing a distribution over the content vocabulary. Others measure on the recommendation set A πθ generated by acting according to πθ (taking most probable items) 1 , which are generic for any types of recommender systems 2 . These metrics bear similarity to many prior works in quantifying the four factors of recommendation quality [5, 8, 15, 19, 26, 29, 66].

## Attributes

We first introduce two item attributes that are used to define both the surprise factor in eq (6) as well as the metrics:

Topic cluster. A topic cluster for each item is produced by: 1) taking the item co-occurrence matrix, where entry (i, j) counts the number of times item i and j were interacted by the same user consecutively; 2) performing matrix factorization to generate one embedding for each item; 3) using k-means to cluster the learned embeddings into 10K clusters; 4) assigning the nearest cluster to each item.

Content provider. Content provider is another attribute of interest as: 1) we observed consistency between contents produced by the same provider, e.g., a food blogger often writes about specific cuisines; 2) we are interested in understanding the importance of content-provider diversity/novelty [37, 64] in influencing long term user experience.

## Accuracy

Arguably the most important property of a recommender is to be able to retrieve contents the user is interested in consuming. We compute the mean average precision at K = 50 (mAP@50) [63] on the recommended set A πθ to measure the accuracy, that is the average precision of identifying an item the user is interested in consuming among A πθ .

## Diversity

Diversity measures the number of distinct faucets the recommendation set contains. Many measurements of set diversity have been proposed [39, 45, 53]. Among them, the average dissimilarity of all pairs of items in the set is a popular choice.

$$
\tag{7}
$$

We define the similarity between two items i and j both on topic level and on content provider level. That is, Sim(i, j) = 1 if i and j belongs to the same topic cluster, and 0 otherwise. Similarly for content provider.

## Novelty

The two terms of novelty and serendipity have been used interchangeably in the literature. In this work, we use novelty to focus on the global popularity-based measurements and serendipity to capture the unexpectedness/surprise of the recommendation to a specific user. That is, novelty concerns the recommender system’s capacity to suggest something a user is unlikely to know about already or discover by themselves. Zhou et al. [71] first introduced the notion of self-information of a recommended item, which measures the unexpectedness of a recommended item relative to its global popularity.

$$
\tag{8}
$$

Herep(a) measures the chance a random user would have consumed item a. By definition, a globally "under-explored" item (tail content) will have higher self-information. With the definition of item-level self-information, we can then measure novelty of the learned policy πθ as

$$
\tag{9}
$$

A learned policy πθ that casts more mass on items with higher selfinformation, being able to recommend "under-explored" items, is deemed more novel. We can define the novelty metrics for attributes similarly by looking at the self-information of the attribute instead, e.g., popularity of the content provider.

## Serendipity

Serendipity captures the unexpectedness/surprise of a recommendation to a specific user. It measures the capability of the recommender system to recommend relevant contents outside of the user’s normal interests. There are two important factors in play here: 1) unexpectedness/surprise: as a counter example, a recommendation of John Lenon to listeners of The Beatles will not constitutes a surprising recommendation; 2) relevance: the surprising contents should be of interest to the user. In other words, serendipity measure the ability of the recommender to discover previously unknown (to the recommender) interests of the user.


We define the serendipity value of a recommendation at w.r.t. a user with interaction history of It as

$$
\tag{10}
$$

Again we can define the content-provider level serendipity value similarly. With the serendipity value of an item defined, we can then quantify the serendipity of the recommendation set Sπθ as

$$
\tag{11}
$$

## Long Term User Experience

Past work has suggested connections between these recommendation qualities toward long term user experience, either through surveys or interviews [5, 66]. We use user returning to the platform, and user moving from a low-activity bucket to a highly-active one on the platform as the holistic measurement of improved long term user experience, and establish the connection between these measurements and long term user experience.

# Offline Analysis

We conducted an extensive set of offline experiments comparing the exploration strategies introduced in Section 4. Specifically, we built these exploration approaches onto the baseline REINFORCE recommender described in Section 3. We evaluate them by computing the set of metrics defined in Section 5 and compare the metric movements between different hyper-parameter settings and different exploration methods.

## Dataset

We conducted 3 runs of experiments for each comparison and report the mean and standard deviation of the metrics. For each experiment run, we extracted close to a billion user trajectories from a commercial recommendation platform. Each trajectory HT = {(st ,At , at ,rt ) : t = 0, . . . ,T }, as described in Section 3, contains user historical events on the platform. The lengths of trajectories between users can vary depending on their activity level. We keep at most 500 historical pages with at least one positive user interaction (nonzero rt ) for each user. Among the collected trajectories, we hold out 1% for evaluation. We restrict our action space (item corpus) to the most popular 10 million items in the past 48 hours on the platform. Our goal is to build a recommender agent that can choose among the 10 million corpus the next set of items for users to consume so as to maximize the cumulative long-term reward.

## Entropy Regularization

The most straightforward knob to tune up and down the exploration strength for entropy regularization is the regularization coefficient α as defined in eq. 4. We compare the baseline method, a REINFORCE agent maximizing only the expected return as defined in eq. 2, with added entropy regularization with α in [0.1, 0.5, 1.0, 10.0]. 

As shown in Table 1, entropy regularization is an extremely efficient method to introduce diversity and novelty to the system, at the cost of reduced accuracy. When the regularization strength is large, it also significantly drops the system’s capability to introduce serendipitous contents to users because of the loss of relevance. For example, a regularization strength of α = 1.0 drops the topic serendipity value by −21.6% (0.037 → 0.029).

## Intrinsic Motivation

One of the obvious hyper-parameters to adjust the exploration strength for the intrinsic motivation approach is to tune the boosting factor c defined in eq. 6. Here we study the impact of the more interesting variants. 

First, on which attribute to use to define surprise. We experimented with defining surprise by topic cluster (denoted as "topic" in Table 2) and content provider (denoted as "provider" in Table 2). Second, on the length of the user historical events used to define surprise. As explained in [66], users’ perception of surprise of contents can drift over time. Contents that the user interacted in the past, but has not been served and interacted for a long time, can be deemed surprising when being resurfaced again. We experimented with having It contain all the items the user interacted with in the past one day, one week and one year (denoted as d = 1, d = 7 and d = 365 respectively in Table 2). 

Table 2 summarizes the comparison between different variants of the intrinsic motivation proposal. Similar to entropy regularization, all variants improve on diversity at the cost of lower accuracy. This method does not change the novelty metrics significantly, neither on the item level nor content provider level. We thus conclude that tail contents are not necessarily more serendipitous (relevant and surprising) than popular ones. We do see a significant improvement in the serendipity metrics, even though the overall accuracy of these methods turn out unfavorable comparing with the baseline. As an example, the variant which uses topic cluster and a historical window size of 7 days, improves the serendipity level by +18.9% (0.037 → 0.044) even though the overall accuracy measured by mAP@50 was dropped by −13.7% (0.070 → 0.063). Attributes. Offline analyses showed both definitions of surprise based on topic cluster and content provider are equally effective in optimizing different angles of serendipity. That is topic cluster definition improves offline topic serendipity metrics by +18.9% from 0.037 to 0.044, and content provider definition improves content provider serendipity for +11.5% from 0.078 to 0.087. We however do see very different performance in user metrics in live experiments as shown in Section 7.1 below, suggesting one angle (topic serendipity) is more important than the other (content provider serendipity) in optimizing the overall user experience. 

Window sizes. As we extend the historical window used to define surprise, i.e., having It contain longer user history, the definition of surprise becomes stricter. An item is less likely to be surprising/different when comparing with a longer history than a shorter one. As a result the percentage of state-action pairs receiving the extra multiplier of c > 1 is reduced. In the datasets, the percentage is reduced from 36% → 19% → 12% when the window size is extended from 1 → 7 → 365 days. The intrinsic motivation boost is applied to a smaller and smaller set of state-action pairs. The relative change on diversity related metrics is marginal between these variants. The variant with window size of d = 7 scored the highest on the topic serendipity metric, which is defined using a window size of one year.

## Actionable Representation

In this set of experiments, we compare four setups: 1) baseline: the baseline REINFORCE algorithm; 2) repre. alone: the baseline REINFORCE with the actionable representation, i.e., the additional bit indicating if the item at is serendipitous at state st according to user historical interactions It ; 3) intrinsic alone: the baseline REINFORCE with intrinsic motivation for reward shaping; 4) repre. + intrinsic: the baseline REINFORCE adding both the intrinsic motivation and the actionable representation. As shown in Table 3, adding the indicator alone (row 2) and adding the indicator along with the intrinsic motivation (row 4) resulted in very different metrics. Adding the indicator alone without the reward shaping performs very similarly to the baseline method, suggesting the representation is more useful when combined with the reward shaping. We see +24.3% improvement in the serendipity value comparing (row 4) to (row 1) (0.037 → 0.046), and +4.5% improvement comparing to (row 3) (0.044 → 0.046). This suggests that the added representation is indeed helpful for decision making when the intrinsic motivation is rewarding serendipitous actions, i.e. actions that discover previously unknown user interests.

To gain more insight into how the agent utilizes the additional bit indicating whether or not a historical event is surprising when provided, we compare the learning of the baseline REINFORCE algorithm with intrinsic motivation alone (shown in orange in Figure 1) vs the one combined with both the intrinsic motivation and the actionable representation (shown in cyan in Figure 1). The RNN [31] Chen et al. [11] used to encode the user history Ht has an important gate named input gate. This gate controls how much the RNN is updating its hidden state to take into account a new input (event). We take the activation values of the input gates across the user trajectory, and separate the values in two groups: the ones on historical events that are considered surprising and relevant (shown in Figure 1 left), and the ones on historical events that are not (shown in Figure 1 right). Comparing the left and right figures, we can see that by adding this additional information, the RNN is able to differentiate better between historical events that are serendipitous and those that are not. At the end of training, the mean activation for events that are surprising and relevant (left) is at 0.1765 (+1.4% higher) for intrinsic motivation + actionable representation compared with 0.1741 for intrinsic motivation alone. The mean activation for events that are NOT serendipitous (right) is at 0.1409 (−11.2% lower) for intrinsic motivation + actionable representation compared with 0.1586 for intrinsic motivation alone. This suggests that relying on the reward alone, RNN can still recognize the difference between these two groups of events and perform slightly larger update when the historical event is considered surprising. Adding the feature helps RNN differentiate the two groups better.

# Live Experiments and Long Term User Experience

We conduct a series of live A/B tests on a industrial recommendation platform serving billions of users to evaluate the impact of the proposed exploration approaches. The control serves the base REINFORCE agent as described in Section 3. The agent selects hundreds of candidates from a corpus of 10 million. The returned candidates A πθ , along with others, are ranked by a separate ranking system before showing to the users. We ran three separate experiments: 1) Entropy regularization: serving the REINFORCE agent with entropy regularization as explained in Section 4.1; 2) Intrinsic motivation: serving the REINFORCE agent with intrinsic motivation to discover new user interest (using topic cluster attributes with a history window of 7 days and a serendipity boost c = 4) as explained in Section 4.2; 3) Intrinsic Motivation + Actionable Representation: serving the REINFORCE agent with both the intrinsic motivation and the actionable representation as introduced in Section 4.3. We compare 1) and 2) to the baseline REINFORCE system as described in Section 3 as control to measure the effect of entropy regularization and intrinsic motivation respectively, and 3) to 2) as control to measure the additional value of introducing the actionable representation on top of intrinsic motivation. We first summarize the live experiment results of these experiments in Section 7.1, and later measure several aspects of long term user experience in Section 7.2. In the end, we establish the connection between exploration and different aspects of recommendation quality toward improving long term user experience.

## Results

Figure 3 summarizes the performances of these exploration approaches on the top-line metric capturing user overall enjoyment of the platform. As shown in Figure 3a (α = 0.1 in red, and α = 0.5 in blue), although entropy regularization increases diversity and novelty in both offline and live experiments, it does not lead to significant improvement on the user enjoyment. In other words, increased diversity or novelty alone does not necessarily lead to better user experience. When we increase the regularization strength to α = 0.5, we see slightly worse live metrics.

Comparing with entropy regularization (Figure 3a), intrinsic motivation (Figure 3b) and its combination with actionable representation (Figure 3c), not only significantly improve on the top-line metric, but also exhibit a strong learning effect over the course of the experiments 4 . We compare the offline measurement on accuracy, diversity, novelty and serendipity between entropy regularization with α = 0.5 (Table 1 row 3) and intrinsic motivation (Table 3 row 3) and its combination with actionable representation (Table 3 row 4) and make the following observations: 1) the entropy regularization method with α = 0.5 achieves very similar diversity metrics comparing to intrinsic motivation or its combination with actionable representation. All three methods reach a topic diversity around 0.86, and content provider diversity around 0.93; 2) The entropy regularization method achieved slightly higher novelty metric, both in item level and content provider level; 3) The metrics that entropy regularization loses is on accuracy and serendipity. 4) Intrinsic motivation method and its combination with actionable representation have favorable improvement on serendipity comparing with the baseline REINFORCE algorithm even though their accuracy numbers are worse. In conclusion, intrinsic motivation and its combination with actionable representation compare favorably to the baseline REINFORCE and entropy regularization only in the serendipity metrics offline. In live experiments, the intrinsic motivation and its combination with actionable representation were shown to significantly improve over the baseline REINFORCE and entropy regularization, as shown in Figure 3 (middle and right). Combining the offline and live experiment observations, we hypothesize that serendipity is an important faucet of recommendation quality that leads to improved long term user experience. We also conducted another group of live experiments defining surprise for optimization using content provider rather than topic. The experiment turns out neutral on the top-line metric, which suggest topic serendipity is more connected with long term user experience than content provider.

Another top-line metric that we keep track of is the number of days users returning to the platform. For both the intrinsic motivation and actionable representation treatment, we observed significant improvement on this metric as well, suggesting users are encouraged to return to the platform due to better recommendation quality. Figure 2 shows the improvement of user returning in the actionable representation experiment, comparing with the base REINFORCE with intrinsic motivation as control, suggesting that aiding the representation learning with the serendipity information further improves the learned policy, leading to better overall user experience.

## Long Term User Experience

Learning Effect of Intrinsic Motivation. To better understand the effect of intrinsic motivation and reward shaping in the long term, we examine the temporal trend of the live metrics in addition to the aggregated metrics reported above. For the 6-week experiment on intrinsic motivation, we look at week-over-week metrics by aggregating user activities within each week. Specifically, we track the number of unique topic clusters the user has interacted with over every week, as well as the entropy of those topic clusters. Suppose the user has interacted with Ni items from topic cluster i, then the entropy of his/her history is computed as − Í i pˆi loд(pˆi), where pˆi = Ni / Í i Ni is the proportion of items interacted with that are from topic cluster i.

Figure 4 shows the comparison between control and treatment, where the treatment group has a boosting multiplier of 4 for unknown user interests as in Eq. (6). Compared with users in the control group which does not have the reward shaping, users in the treatment group have consistently interacted with more topic clusters (Fig 4a) and generated a higher entropy over cluster distributions (Fig 4c) over the whole experiment period. More interestingly, the amount of improvements over control is increasing over time (Fig 4b and 4d). This suggests a learning effect over time from exploration, which enables users to continuously find and engage with new topics.

User Activity Levels. Users who come to the recommendation platform are heterogeneous in terms of activity levels. Some users visit the platform occasionally, while others visit the platform more regularly and consistently. The long-term goal of a recommendation platform is to not only satisfy the user’s need in the current session, but ideally to see them return to the recommendation platform more often in the future.

We would like to see if adding exploration in the recommendation has any effect on moving user activity levels. We define four user activity levels in terms of how many days they are active on the platform in a 2-week period, which is shown in Fig 5a. For example, a user being casual means that he/she has been active for 1 to 4 days in the last 14 days. Users can become more active or less active depending their experience on the platform as well as exogenous factors not control by recommendation. Suppose the goal of a recommendation platform is moving causal users to become core users. An intuitive way to measure the conversion is by counting the number of users who start off casual, and end up core. This can be realized with a user activity level transition matrix, which measures the movement between different user activity levels.

We examine user activity level before the experiment start date and at the end of the experiment for every treatment group to compute the transition matrix, and compare with control. Figure 5b shows the percentage difference of the transition matrices between the actionable representation treatment group and control. We see that there is a significant increase in casual-to-core conversion rate. This suggests that a successful exploration strategy can result in a desired user movement as less active users are becoming more engaged on the platform.

# Conclusion

We present a systemic study to understand the values of exploration in recommender systems beyond reducing model uncertainty. We examine different user exploration strategies in affecting the four facets of recommendation quality, i.e., accuracy, diversity, novelty and serendipity, that contribute directly to user experience on the platform. We showcase exploration strategies that oriented toward discovering unknown user interests in positively influencing user experience on recommendation platforms. Using conversion of casual users to core users as an indicator of the holistic long term user experience, we connects serendipity to improved long term user experience. We believe these are important first steps in understanding and improving exploration and serendipity in (RL based) recommender systems, and providing foundation for future effort in this direction.
