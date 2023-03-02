## link

- https://arxiv.org/abs/1812.02353

## title

Top-K Off-Policy Correction for a REINFORCE Recommender System

## abstract

Industrial recommender systems deal with extremely large action spaces -- many millions of items to recommend. Moreover, they need to serve billions of users, who are unique at any point in time, making a complex user state space. Luckily, huge quantities of logged implicit feedback (e.g., user clicks, dwell time) are available for learning. Learning from the logged feedback is however subject to biases caused by only observing feedback on recommendations selected by the previous versions of the recommender. In this work, we present a general recipe of addressing such biases in a production top-K recommender system at Youtube, built with a policy-gradient-based algorithm, i.e. REINFORCE. The contributions of the paper are: (1) scaling REINFORCE to a production recommender system with an action space on the orders of millions; (2) applying off-policy correction to address data biases in learning from logged feedback collected from multiple behavior policies; (3) proposing a novel top-K off-policy correction to account for our policy recommending multiple items at a time; (4) showcasing the value of exploration. We demonstrate the efficacy of our approaches through a series of simulations and multiple live experiments on Youtube.

# Introduction

Recommender systems are relied on, throughout industry, to help users sort through huge corpuses of content and discover the small fraction of content they would be interested in. This problem is challenging because of the huge number of items that could be recommended. Furthermore, surfacing the right item to the right user at the right time requires the recommender system to constantly adapt to users’ shifting interest (state) based on their historical interaction with the system [6]. Unfortunately, we observe relatively little data for such a large state and action space, with most users only having been exposed to a small fraction of items and providing explicit feedback to an even smaller fraction. That is, recommender systems receive extremely sparse data for training in general, e.g., the Netflix Prize dataset was only 0.1% dense [5]. As a result, a good amount of research in recommender systems explores different mechanisms for treating this extreme sparsity. Learning from implicit user feedback, such as clicks and dwell-time, as well as filling in unobserved interactions, has been an important step in improving recommenders [19] but the problem remains an open one.

In a mostly separate line of research, reinforcement learning (RL) has recently achieved impressive advances in games [38, 46] as well as robotics [22, 25]. RL in general focuses on building agents that take actions in an environment so as to maximize some notion of long term reward. Here we explore framing recommendation as building RL agents to maximize each user’s long term satisfaction with the system. This offers us new perspectives on recommendation problems as well as opportunities to build on top of the recent RL advancement. However, there are significant challenges to put this perspective into practice.

As introduced above, recommender systems deal with large state and action spaces, and this is particularly exacerbated in industrial settings. The set of items available to recommend is non-stationary and new items are brought into the system constantly, resulting in an ever-growing action space with new items having even sparser feedback. Further, user preferences over these items are shifting all the time, resulting in continuously-evolving user states. Being able to reason through these large number of actions in such a complex environment poses unique challenges in applying existing RL algorithms. Here we share our experience adapting the REINFORCE algorithm [48] to a neural candidate generator (a top-𝐾 recommender system) with extremely large action and state spaces.

In addition to the massive action and state spaces, RL for recommendation is distinct in its limited availability of data. Classic RL applications have overcome data inefficiencies by collecting large quantities of training data with self-play and simulation [38]. In contrast, the complex dynamics of the recommender system has made simulation for generating realistic recommendation data nonviable. As a result, we cannot easily probe for reward in previously unexplored areas of the state and action space, since observing reward requires giving a real recommendation to a real user. Instead, the model relies mostly on data made available from the previous recommendation models (policies), most of which we cannot control or can no longer control. To most effectively utilize logged-feedback from other policies, we take an off-policy learning approach, in which we simultaneously learn a model of the previous policies and incorporate it in correcting the data biases when training our new policy. We also experimentally demonstrate the value in exploratory data.

Finally, most of the research in RL focuses on producing a policy that chooses a single item. Real-world recommenders, on the other hand, typically offer the user multiple recommendations at a time [44]. Therefore, we define a novel top-𝐾 off-policy correction for our top-𝐾 recommender system. We find that while the standard off-policy correction results in a policy that is optimal for top-1 recommendation, this top-𝐾 off-policy correction leads to significant better top-𝐾 recommendations in both simulations and live experiments. Together, we offer the following contributions:

- REINFORCE Recommender: We scale a REINFORCE policygradient-based approach to learn a neural recommendation policy in a extremely large action space.
- Off-Policy Candidate Generation: We apply off-policy correction to learn from logged feedback, collected from an ensemble of prior model policies. We incorporate a learned neural model of the behavior policies to correct data biases.
- Top-𝐾 Off-Policy Correction: We offer a novel top-𝐾 offpolicy correction to account for the fact that our recommender outputs multiple items at a time.
- Benefits in Live Experiments: We demonstrate in live experiments, which was rarely done in existing RL literature, the value of these approaches to improve user long term satisfaction

We find this combination of approaches valuable for increasing user enjoyment and believe it frames many of the practical challenges going forward for using RL in recommendations.

# Related work

## Reinforcement Learning:

Value-based approaches such as Q-learning, and policy-based ones such as policy gradients constitute classical approaches to solve RL problems [40]. A general comparison of modern RL approaches can be found in [29] with a focus on asynchronous learning which is key to scaling up to large problems. Although value-based methods present many advantages such as seamless off-policy learning, they are known to be prone to instability with function approximation [41]. Often, extensive hyper-parameter tuning is required to achieve stable behavior for these approaches. Despite the practical success of many value-based approaches such as deep Q-learning [30], policy convergence of these algorithms are not well-studied. Policy-based approaches on the other hand, remain rather stable w.r.t. function approximations given a sufficiently small learning rate. We therefore choose to rely on a policy-gradient-based approach, in particular REINFORCE [48], and to adapt this on-policy method to provide reliable policy gradient estimates when training off-policy.

## Neural Recommenders:

Another line of work that is closely related to ours is the growing body of literature on applying deep neural networks to recommender systems [11, 16, 37], in particular using recurrent neural networks to incorporate temporal information and historical events for recommendation [6, 17, 20, 45, 49]. We employed similar network architectures to model the evolving of user states through interactions with the recommender system. As neural architecture design is not the main focus of our work, we refer interested readers to these prior works for more detailed discussions.

## Bandit Problems in recommender systems:

On-line learning methods are also popular to quickly adapt recommendation systems as new user feedback becomes available. Bandit algorithms such as Upper Confidence Bound (UCB) [3] trade off exploration and exploitation in an analytically tractable way that provides strong guarantees on the regret. Different algorithms such as Thomson sampling [9], have been successfully applied to news recommendations and display advertising. Contextual bandits offer a contextaware refinement of the basic on-line learning approaches and tailor the recommendation toward user interests [27]. Agarwal et al. [2] aimed to make contextual bandits tractable and easy to implement. Hybrid methods that rely on matrix factorization and bandits have also been developed to solve cold-start problems in recommender systems [28].

## Propensity Scoring and Reinforcement Learning in Recommender Systems:

The problem of learning off-policy [31, 33, 34] is pervasive in RL and affects policy gradient generally. As a policy evolves so does the distribution under which gradient expectations are computed. Standard approaches in robotics [1, 36] circumvent this issue by constraining policy updates so that they do not change the policy too substantially before new data is collected under an updated policy, which in return provides monotonic improvement guarantees of the RL objective. Such proximal methods are unfortunately not applicable in the recommendations setting where item catalogues and user behaviors change rapidly, and therefore substantial policy changes are required. Meanwhile feedback is slow to collect at scale w.r.t. the large state and action space. As a matter of fact, offline evaluation of a given policy is already a challenge in the recommender system setting. Multiple off-policy estimators leveraging inverse-propensity scores, capped inverse-propensity scores and various variance control measures have been developed [13, 42, 43, 47]. Off-policy evaluation corrects for a similar data skew as off-policy RL and similar methods are applied on both problems. Inverse propensity scoring has also been employed to improve a serving policy at scale in [39]. Joachims et al. [21] learns a model of logged feedback for an unbiased ranking model; we take a similar perspective but use a DNN to model the logged behavior policy required for the off-policy learning. More recently an off-policy approach has been adapted to the more complex problem of slate recommendation [44] where a pseudo-inverse estimator assuming a structural prior on the slate and reward is applied in conjunction with inverse propensity scoring.

# Reinforce Recommender

We begin with describing the setup of our recommender system, and our approach to RL-based recommendation.

For each user, we consider a sequence of user historical interactions with the system, recording the actions taken by the recommender, i.e., videos recommended, as well as user feedback, such as clicks and watch time. Given such a sequence, we predict the next action to take, i.e., videos to recommend, so that user satisfaction metrics, e.g., indicated by clicks or watch time, improve.

We translate this setup into a Markov Decision Process (MDP) (S, A, P, 𝑅, 𝜌0,𝛾) where

- S: a continuous state space describing the user states;
- A: a discrete action space, containing items available for recommendation;
- P : S × A × S → R is the state transition probability;
- 𝑅 : S × A → R is the reward function, where 𝑟(𝑠, 𝑎) is the immediate reward obtained by performing action 𝑎 at user state 𝑠;
- 𝜌0 is the initial state distribution;
- 𝛾 is the discount factor for future rewards.

We seek a policy 𝜋 (𝑎|𝑠) that casts a distribution over the item to recommend 𝑎 ∈ A conditional to the user state 𝑠 ∈ S, so as to maximize the expected cumulative reward obtained by the recommender system,

$$
\tag{0}
$$

Here the expectation is taken over the trajectories 𝜏 = (𝑠0, 𝑎0, 𝑠1, · · · ) obtained by acting according to the policy:𝑠0 ∼ 𝜌0, 𝑎𝑡 ∼ 𝜋 (·|𝑠𝑡), 𝑠𝑡+1 ∼ P(·|𝑠𝑡 , 𝑎𝑡). In other words,

$$
\tag{1}
$$

Here 𝑑 𝜋 𝑡 (·) denotes the (discounted) state visitation frequency at time 𝑡 under the policy 𝜋. Different families of methods are available to solve such an RL problems: Q-learning [38], Policy Gradient [26, 36, 48] and black box optimization [15]. Here we focus on a policy-gradient-based approach, i.e., REINFORCE [48].

We assume a function form of the policy 𝜋𝜃 , parametrised by 𝜃 ∈ R 𝑑 . The gradient of the expected cumulative reward with respect to the policy parameters can be derived analytically thanks to the “log-trick”, yielding the following REINFORCE gradient

$$
\tag{2}
$$

Here 𝑅𝑡 (𝑠𝑡 , 𝑎𝑡) = Í|𝜏 | 𝑡 ′=𝑡 𝛾 𝑡 ′−𝑡 𝑟(𝑠𝑡 ′, 𝑎𝑡 ′) is the discounted future reward for action at time 𝑡. The discounting factor 𝛾 is applied to reduce variance in the gradient estimate. In on-line RL, where the policy gradient is computed on trajectories generated by the policy under consideration, the monte carlo estimate of the policy gradient is unbiased.

# Off-Policy Correction

Unlike classical reinforcement learning, our learner does not have real-time interactive control of the recommender due to learning and infrastructure constraints. In other words, we cannot perform online updates to the policy and generate trajectories according to the updated policy immediately. Instead we receive logged feedback of actions chosen by a historical policy (or a mixture of policies), which could have a different distribution over the action space than the policy we are updating.

We focus on addressing the data biases that arise when applying policy gradient methods under this setting. In particular, the fact that we collect data with a periodicity of several hours and compute many policy parameter updates before deploying a new version of the policy in production implies that the set of trajectories we employ to estimate the policy gradient is generated by a different policy. Moreover, we learn from batched feedback collected by other recommenders as well, which follow drastically different policies. A naive policy gradient estimator is no longer unbiased as the gradient in Equation (2) requires sampling trajectories from the updated policy 𝜋𝜃 while the trajectories we collected were drawn from a combination of historical policies 𝛽.

We address the distribution mismatch with importance weighting [31, 33, 34]. Consider a trajectory 𝜏 = (𝑠0, 𝑎0, 𝑠1, · · · ) sampled according to a behavior policy 𝛽, the off-policy-corrected gradient estimator is then:

$$
\tag{3}
$$

where

$$
\tag{3.5}
$$

is the importance weight. This correction produces an unbiased estimator whenever the trajectories are collected with actions sampled according to 𝛽. However, the variance of the estimator can be huge when the difference in 𝜋𝜃 and the behavior policy 𝛽 results in very low or high values of the importance weights.

To reduce the variance of each gradient term, we take the firstorder approximation and ignore the state visitation differences under the two policies as the importance weights of future trajectories, which yields a slightly biased estimator of the policy gradient with lower variance:

$$
\tag{4}
$$

Achiam et al. [1] prove that the impact of this first-order approximation on the total reward of the learned policy is bounded in magnitude by 𝑂 𝐸𝑠∼𝑑 𝛽 [𝐷𝑇𝑉 (𝜋 |𝛽) [𝑠]]) where 𝐷𝑇𝑉 is the total variation between 𝜋 (·|𝑠) and 𝛽 (·|𝑠) and 𝑑 𝛽 is the discounted future state distribution under 𝛽. This estimator trades off the variance of the exact off-policy correction while still correcting for the large bias of a non-corrected policy gradient, which is better suited for on-policy learning.

## Parametrising the polic

We model our belief on the user state at each time 𝑡, which capture both evolving user interests using a 𝑛-dimensional vector, that is, s𝑡 ∈ R 𝑛 . The action taken at each time 𝑡 along the trajectory is embedded using an 𝑚-dimensional vector u𝑎𝑡 ∈ R 𝑚. We model the state transition P : S×A×S with a recurrent neural network [6, 49]

$$
\tag{}
$$

We experimented with a variety of popular RNN cells such as Long Short-Term Memory (LSTM) [18] and Gated Recurrent Units (GRU) [10], and ended up using a simplified cell called Chaos Free RNN (CFN) [24] due to its stability and computational efficiency. The state is updated recursively as

$$
\tag{5}
$$

where z𝑡 , i𝑡 ∈ R 𝑛 are the update and input gate respectively.

Conditioning on a user state s, the policy 𝜋𝜃 (𝑎|s) is then modeled with a simple softmax,

$$
\tag{6}
$$

where v𝑎 ∈ R 𝑛 is another embedding for each action 𝑎 in the action space A and 𝑇 is a temperature that is normally set to 1. Using a higher value in 𝑇 produces a smoother policy over the action space. The normalization term in the softmax requires going over all the possible actions, which is in the order of millions in our setting. To speed up the computation, we perform sampled softmax [4] during training. At serving time, we used an efficient nearest neighbor search algorithm to retrieve top actions and approximate the softmax probability using these actions only, as detailed in section 5.

In summary, the parameter 𝜃 of the policy 𝜋𝜃 contains the two action embeddings U ∈ R 𝑚× |A | and V ∈ R 𝑛× |A | as well as the weight matrices U𝑧, U𝑖 ∈ R 𝑛×𝑛 , W𝑢, W𝑖 , W𝑎 ∈ R 𝑛×𝑚 and biases b𝑢, b𝑖 ∈ R 𝑛 in the RNN cell. Figure 1 shows a diagram describing the neural architecture of the main policy 𝜋𝜃 . Given an observed trajectory 𝜏 = (𝑠0, 𝑎0, 𝑠1, · · · ) sampled from a behavior policy 𝛽, the new policy first generates a model of the user state s𝑡+1 by starting with an initial state s0 ∼ 𝜌0 1 and iterating through the recurrent cell as in Equation (5) 2 . Given the user state s𝑡+1 the policy head casts a distribution on the action space through a softmax as in Equation (6). With 𝜋𝜃 (𝑎𝑡+1 |s𝑡+1), we can then produce a policy gradient as in Equation (4) to update the policy.

## Estimating the behavior policy

One difficulty in coming up with the off-policy corrected estimator in Equation (4) is to get the behavior policy 𝛽. Ideally, for each logged feedback of a chosen action we received, we would like to also log the probability of the behavior policy choosing that action. Directly logging the behavior policy is however not feasible in our case as (1) there are multiple agents in our system, many of which we do not have control over, and (2) some agents have a deterministic policy, and setting 𝛽 to 0 or 1 is not the most effective way to utilize these logged feedback.

Instead we take the approach first introduced in [39], and estimate the behavior policy 𝛽, which in our case is a mixture of the policies of the multiple agents in the system, using the logged actions. Given a set of logged feedback D = {(s𝑖 , 𝑎𝑖),𝑖 = 1, · · · , 𝑁}, Strehl et al. [39] estimates ˆ𝛽 (𝑎) independent of user state by aggregate action frequency throughout the corpus. In contrast, we adopt a context-dependent neural estimator. For each state-action pair (𝑠, 𝑎) collected, we estimate the probability ˆ𝛽𝜃 ′ (𝑎|𝑠) that the mixture of behavior policies choosing that action using another softmax, parametrised by 𝜃 ′ . As shown in Figure 1, we re-use the user state 𝑠 generated from the RNN model from the main policy, and model the mixed behavior policy with another softmax layer. To prevent the behavior head from intefering with the user state of the main policy, we block its gradient from flowing back into the RNN. We also experimented with separating the 𝜋𝜃 and 𝛽𝜃 ′ estimators, which incurs computational overhead for computing another state representation but does not results in any metric improvement in offline and live experiments.

Despite a substantial sharing of parameters between the two policy heads 𝜋𝜃 and 𝛽𝜃 ′, there are two noticeable difference between them: (1) While the main policy 𝜋𝜃 is effectively trained using a weighted softmax to take into account of long term reward, the behavior policy head 𝛽𝜃 ′ is trained using only the state-action pairs; (2) While the main policy head 𝜋𝜃 is trained using only items on the trajectory with non-zero reward 3 , the behavior policy 𝛽𝜃 ′ is trained using all of the items on the trajectory to avoid introducing bias in the 𝛽 estimate.

In [39], it is argued that that a behavior policy that is deterministically choosing an action 𝑎 given state 𝑠 at time 𝑡1 and action 𝑏 at time 𝑡2 can be treated as randomizing between action 𝑎 and 𝑏 over the timespan of the logging. Here we could argue the same point, which explains why the behavior policy could be other than 0 or 1 given a deterministic policy. In addition, since we have multiple policies acting simultaneously, if one policy is determinstically choosing action 𝑎 given user state 𝑠, and another one is determinstically choosing action 𝑏, then estimating ˆ𝛽𝜃 ′ in such a way would approximate the expected frequency of action 𝑎 being chosen under the mixture of these behavior policies given user state 𝑠.

## Top-𝐾 Off-Policy Correction

Another challenge in our setting is that our system recommends a page of 𝑘 items to users at a time. As users are going to browse through (the full or partial set of) our recommendations and potentially interact with more than one item, we need to pick a set of relevant items instead of a single one. In other words, we seek a policy Π𝜃 (𝐴|𝑠), here each action 𝐴 is to select a set of 𝑘 items, to maximize the expected cumulative reward,

$$
\tag{}
$$

Here 𝑅𝑡 (𝑠𝑡 , 𝐴𝑡) denotes the cumulative return of the set 𝐴𝑡 at state 𝑠𝑡 . Unfortunately, the action space grows exponentially under this set recommendation formulation [44, 50], which is prohibitively large given the number of items we choose from are in the orders of millions.

To make the problem tractable, we assume that a user will interact with at most one item from the returned set 𝐴. In other words, there will be at most one item with non-zero cumulative reward among 𝐴. We further assume that the expected return of an item is independent of other items chosen in the set 𝐴 4 . With these two assumptions, we can reduce the set problem to

$$
\tag{}
$$

Here 𝑅𝑡 (𝑠𝑡 , 𝑎𝑡) is the cumulative return of the item 𝑎𝑡 the user interacted with, and 𝑎𝑡 ∈ 𝐴𝑡 ∼ Π𝜃 (·|𝑠𝑡) indicates that 𝑎𝑡 was chosen by the set policy. Furthermore, we constrain ourselves to generate the set action 𝐴 by independently sampling each item 𝑎 according to the softmax policy 𝜋𝜃 described in Equation (6) and then de-duplicate. As a result, the probability of an item 𝑎 appearing in the final non-repetitive set 𝐴 is simply 𝛼𝜃 (𝑎|𝑠) = 1 − (1 − 𝜋𝜃 (𝑎|𝑠))𝐾, where 𝐾 is the number of times we sample. 5 .

We can then adapt the REINFORCE algorithm to the set recommendation setting by simply modifying the gradient update in Equation (2) to

$$
\tag{}
$$

Accordingly, we can update the off-policy corrected gradient in Equation (4) by replacing 𝜋𝜃 with 𝛼𝜃 , resulting in the top-𝐾 off-policy correction factor:

$$
\tag{7}
$$

Comparing Equation (7) with Equation (4), the top-𝐾 policy adds an additional multiplier of

$$
\tag{8}
$$

to the original off-policy correction factor of 𝜋 (𝑎 |𝑠) 𝛽 (𝑎 |𝑠) .

Now let us take a closer look at this additional multiplier:

- As 𝜋𝜃 (𝑎|𝑠) → 0, 𝜆𝐾 (𝑠, 𝑎) → 𝐾. The top-𝐾 off-policy correction increases the policy update by a factor of 𝐾 comparing to the standard off-policy correction;
- As 𝜋𝜃 (𝑎|𝑠) → 1, 𝜆𝐾 (𝑠, 𝑎) → 0. This multiplier zeros out the policy update.
- As 𝐾 increases, this multiplier reduces the gradient to zero faster as 𝜋𝜃 (𝑎|𝑠) reaches a reasonable range.

In summary, when the desirable item has a small mass in the softmax policy 𝜋𝜃 (·|𝑠), the top-𝐾 correction more aggressively pushes up its likelihood than the standard correction. Once the softmax policy 𝜋𝜃 (·|𝑠) casts a reasonable mass on the desirable item (to ensure it will be likely to appear in the top-𝐾), the correction then zeros out the gradient and no longer tries to push up its likelihood. This in return allows other items of interest to take up some mass in the softmax policy. As we are going to demonstrate in the simulation as well as live experiment, while the standard off-policy correction converges to a policy that is optimal when choosing a single item, the top-𝐾 correction leads to better top-𝐾 recommendations.

## Variance Reduction Techniques

As detailed at the beginning of this section, we take a first-order approximation to reduce variance in the gradient estimate. Nonetheless, the gradient can still suffer from large variance due to large importance weight of 𝜔(𝑠, 𝑎) = 𝜋 (𝑎 |𝑠) 𝛽 (𝑎 |𝑠) as shown in Equation (4), Similarly for top-𝐾 off-policy correction. Large importance weight could result from (1) large deviation of the new policy 𝜋 (·|𝑠) from the behavior policy, in particular, the new policy explores regions that are less explored by the behavior policy. That is, 𝜋 (𝑎|𝑠) ≫ 𝛽 (𝑎|𝑠) and (2) large variance in the 𝛽 estimate.

We tested several techniques proposed in counterfactual learning and RL literature to control variance in the gradient estimate. Most of these techniques reduce variance at the cost of introducing some bias in the gradient estimate.

### Weight Capping.

The first approach we take is to simply cap the weight [8] as

$$
\tag{9}
$$

Smaller value of 𝑐 reduces variance in the gradient estimate, but introduces larger bias.

### Normalized Importance Sampling (NIS).

Second technique we employed is to introduce a ratio control variate, where we use classical weight normalization [32] defined by:

$$
\tag{}
$$

As E𝛽 [𝜔(𝑠, 𝑎)] = 1, the normalizing constant is equal to 𝑛, the batch size, in expectation. As 𝑛 increases, the effect of NIS is equivalent to tuning down the learning rate.

### Trusted Region Policy Optimization (TRPO).

TRPO [36] prevents the new policy 𝜋 from deviating from the behavior policy by adding a regularization that penalizes the KL divergence of these two policies. It achieves similar effect as the weight capping.

# Exploration

As should be clear by this point, the distribution of training data is important for learning a good policy. Exploration policies to inquire about actions rarely taken by the existing system have been extensively studied. In practice, brute-force exploration, such as 𝜖-greedy, is not viable in a production system like YouTube where this could, and mostly likely would, result in inappropriate recommendations and a bad user experience. For example, Schnabel et al. [35] studied the cost of exploration.

Instead we employ Boltzmann exploration [12] to get the benefit of exploratory data without negatively impacting user experience. We consider using a stochastic policy where recommendations are sampled from 𝜋𝜃 rather than taking the 𝐾 items with the highest probability. This has the challenge of being computationally inefficient because we need to calculate the full softmax, which is prohibitively expensive considering our action space. Rather, we make use of efficient approximate nearest neighbor-based systems to look up the top 𝑀 items in the softmax [14]. We then feed the logits of these 𝑀 items into a smaller softmax to normalize the probabilities and sample from this distribution. By setting 𝑀 ≫ 𝐾 we can still retrieve most of the probability mass, limit the risk of bad recommendations, and enable computationally efficient sampling. In practice, we further balance exploration and exploitation by returning the top 𝐾 ′ most probable items and sample 𝐾 − 𝐾 ′ items from the remaining 𝑀 − 𝐾 ′ items.

# Experimental Results

We showcase the effectiveness of these approaches for addressing data biases in a series of simulated experiments and live experiments in an industrial-scale recommender system.

## Simulation

We start with designing simulation experiments to shed light on the off-policy correction ideas under more controlled settings. To simplify our simulation, we assume the problem is stateless, in other words, the reward 𝑅 is independent of user states, and the action does not alter the user states either. As a result, each action on a trajectory can be independently chosen.

### Off-policy correction.

In the first simulation, we assume there are 10 items, that is A = {𝑎𝑖 ,𝑖 = 1, · · · , 10}. The reward of each one is equal to its index, that is, 𝑟(𝑎𝑖) = 𝑖. When we are choosing a single item, the optimal policy under this setting is to always choose the 10𝑡ℎ item as it gives the most reward, that is,

$$
\tag{}
$$

We parameterize 𝜋𝜃 using a stateless softmax

$$
\tag{}
$$

Given observations sampled from the behavior policy 𝛽, naively applying policy gradient without taking into account of data bias as in Equation (2) would converge to a policy

$$
\tag{}
$$

This has an obvious downside: the more the behavior policy chooses a sub-optimal item, the more the new policy will be biased toward choosing the same item.

Figure 2 compares the policies 𝜋𝜃 , learned without and with off-policy correction using SGD [7], when the behavior policy 𝛽 is skewed to favor items with least reward. As shown in Figure 2 (left), naively applying the policy gradient without accounting for the data biases leads to a sub-optimal policy. In the worst case, if the behavior policy always chooses the action with the lowest reward, we will end up with a policy that is arbitrarily poor and mimicking the behavior policy (i.e., converge to selecting the least rewarded item). On the other hand, applying the off-policy correction allows us to converge to the optimal policy 𝜋 ∗ regardless of how the data is collected, as shown in Figure 2 (right).

### Top-𝐾 off-policy correction.

To understand the difference between the standard off-policy correction and the top-𝐾 off-policy correction proposed, we designed another simulation in which we can recommend multiple items. Again we assume there are 10 items, with 𝑟(𝑎1) = 10, 𝑟(𝑎2) = 9, and the remaining items are of much lower reward 𝑟(𝑎𝑖) = 1, ∀𝑖 = 3, · · · , 10. Here we focus on recommending two items, that is, 𝐾 = 2. The behavior policy 𝛽 follows a uniform distribution, i.e., choosing each item with equal chance.

Given an observation (𝑎𝑖 , 𝑟𝑖) sampled from 𝛽, the standard offpolicy correction has a SGD updates of the following form,

$$
\tag{}
$$

where 𝜂 is the learning rate. SGD keeps increasing the likelihood of the item 𝑎𝑖 proportional to the expected reward under 𝜋𝜃 until 𝜋𝜃 (𝑎𝑖) = 1, under which the gradient goes to 0. The top-𝐾 off-policy correction, on the other hand, has an update of the following form,

$$
\tag{}
$$

where 𝜆𝐾 (𝑎𝑖) is the multiplier as defined in section 4.3. When 𝜋𝜃 (𝑎𝑖) is small, 𝜆𝐾 (𝑎𝑖) ≈ 𝐾, and SGD increases the likelihood of the item 𝑎𝑖 more aggressively. As 𝜋𝜃 (𝑎𝑖) reaches to a large enough value, 𝜆𝐾 (𝑎𝑖) goes to 0. As a result, SGD will no longer force to increase the likelihood of this item even when 𝜋𝜃 (𝑎𝑖) is still less than 1. This in return allows the second-best item to take up some mass in the learned policy.

Figure 3 shows the policies 𝜋𝜃 learned with the standard (left) and top-𝐾 off-policy correction (right). We can see that with the standard off-policy correction, although the learned policy is calibrated [23] in the sense that it still maintains the ordering of items w.r.t. their expected reward, it converges to a policy that cast almost its entire mass on the top-1 item, that is 𝜋 (𝑎1) ≈ 1.0. As a result, the learned policy loses track of the difference between a slightly sub-optimal item (𝑎2 in this example) and the rest. The top-𝐾 correction, on the other hand, converges to a policy that has a significant mass on the second optimal item, while maintaining the order of optimality between items. As a result, we are able to recommend to users two high-reward items and aggregate more reward overall.

## Live Experiments

While simulated experiments are valuable to understand new methods, the goal of any recommender systems is ultimately to improve real user experience. We therefore conduct a series of A/B experiments running in a live system to measure the benefits of these approaches.

We evaluate these methods on a production RNN candidate generation model in use at YouTube, similar to the setup described in [6, 11]. The model is one of many candidate generators that produce recommendations, which are scored and ranked by a separate ranking model before being shown to users on the YouTube Homepage or the side panel on the video watch page. As described above, the model is trained following the REINFORCE algorithm. The immediate reward 𝑟 is designed to reflect different user activities; videos that are recommended but not clicked receive zero reward. The long term reward 𝑅 is aggregated over a time horizon of 4–10 hours. In each experiment both the control and the test model use the same reward function. Experiments are run for multiple days, during which the model is trained continuously with new events being used as training data with a lag under 24 hours. While we look at various online metrics with the recommender system during live experiments, we are going to focus our discussion on the amount of time user spent watching videos, referred to as ViewTime.

The experiments presented here describe multiple sequential improvements to the production system. Unfortunately, in such a setting, the latest recommender system provides the training data for the next experiment, and as a result, once the production system incorporates a new approach, subsequent experiments cannot be compared to the earlier system. Therefore, each of the following experiments should be taken as the analysis for each component individually, and we state in each section what was the previous recommender system from which the new approach receives data.

### Exploration.

We begin with understanding the value of exploratory data in improving model quality. In particular, we would like to measure if serving a stochastic policy, under which we sample from the softmax model as described in Section 5, results in better recommendations than serving a deterministic policy where the model always recommends the 𝐾 items with the highest probability according to the softmax.

We conducted a first set of experiments to understand the impact of serving a stochastic policy vs. a deterministic one while keeping the training process unchanged. In the experiment, the control population is served with a deterministic policy, while a small slice of test traffic is served with the stochastic policy as described in Section 5. Both policies are based on the same softmax model trained as in Equation (??). To control the amount of randomness in the stochastic policy at serving, we varied the temperature used in Equation (6). A lower 𝑇 reduces the stochastic policy to a deterministic one, while a higher 𝑇 leads to a random policy that recommends any item with equal chance. With 𝑇 set to 1, we observed no statistically significant change in ViewTime during the experiment, which suggests the amount of randomness introduced from sampling does not hurt the user experience directly.

However, this experimental setup does not account for the benefit of having exploratory data available during training. One of the main biases in learning from logged data is that the model does not observe feedback of actions not chosen by the previous recommendation policy, and exploratory data alleviates this problem. We conducted a followup experiment where we introduce the exploratory data into training. To do that, we split users on the platform into three buckets: 90%, 5%, 5%. The first two buckets are served with a deterministic policy based on a deterministic model and the last bucket of users is served with a stochastic policy based on a model trained with exploratory data. The deterministic model is trained using only data acquired in the first two buckets, while the stochastic model is trained on data from the first and third buckets. As a result, these two models receive the same amount of training data, but the stochastic model is more likely to observe the outcomes of some rarer state, action pairs because of exploration.

Following this experimental procedure, we observe a statistically significant increase in ViewTime by 0.07% in the test population. While the improvement is not large, it comes from a relatively small amount of exploration data (only 5% of users experience the stochastic policy). We expect higher gain now that the stochastic policy has been fully launched.

### Off-Policy Correction.

Following the use of a stochastic policy, we tested incorporating off-policy correction during training. Here, we follow a more traditional A/B testing setup 6 where we train two models, both using the full traffic. The control model is trained following Equation (??), only weighting examples by the reward. The test model follows the structure in Figure 1, where the model learns both a serving policy 𝜋𝜃 as well as the behavior policy 𝛽𝜃 ′. The serving policy is trained with the off-policy correction described in Equation (4) where each example is weighted not only by the reward but also the importance weight 𝜋𝜃 𝛽𝜃 ′ for addressing data bias.

During experiments, we observed the learned policy (test) starts to deviate from the behavior policy (control) that is used to acquire the traffic. Figure 4 plots a CDF of videos selected by our nominator in control and experiment according to the rank of videos in control population (rank 1 is the most nominated video by the control model, and the rightmost is least nominated). We see that instead of mimicking the model (shown in blue) used for data collection, the test model (shown in green) favors videos that are less explored by the control model. We observed that the proportion of nominations coming from videos outside of the top ranks is increased by nearly a factor of three in experiment. This aligns with what we observed in the simulation shown in Figure 2. While ignoring the bias in the data collection process creates a “rich get richer“ phenomenon, whereby a video is nominated in the learned policy simply because it was heavily nominated in the behavior policy, incorporating the off-policy correction reduces this effect.

Interestingly, in live experiment, we did not observe a statistically significant change in ViewTime between control and test population. However, we saw an increase in the number of videos viewed by 0.53%, which was statistically significant, suggesting that users are indeed getting more enjoyment.

### Top-𝐾 Off-Policy.

We now focus on understanding if the top-𝐾 off-policy learning improves the user experience over the standard off-policy approach. In this case, we launched an equivalently structured model now trained with the top-𝐾 off-policy corrected gradient update given in Equation (7) and compared its performance to the previous off-policy model, described in Section 6.2.2. In this experiment, we use 𝐾 = 16 and capping 𝑐 = 𝑒 3 in Equation (9); we will explore these hyperparameters in more detail below.

As described in Section 4.3 and demonstrated in the simulation in Section 6.1.2, while the standard off-policy correction we tested before leads to a policy that is overly-focused on getting the top-1 item correct, the top-𝐾 off-policy correction converges to a smoother policy under which there is a non-zero mass on the other items of interest to users as well. This in turn leads to better top-𝐾 recommendation. Given that we can recommend multiple items, the top-𝐾 off-policy correction leads us to present a better fullpage experience to users than the standard off-policy correction. In particular, we find that the amount of ViewTime increased by 0.85% in the test traffic, with the number of videos viewed slightly decreasing by 0.16%.

### Understanding Hyperparameters.

Last, we perform a direct comparison of how different hyperparameter choices affect the top-𝐾 off-policy correction, and in turn the user experience on the platform. We perform these tests after the top-𝐾 off-policy correction became the production model.

#### Number of actions.

We first explore the choice of 𝐾 in the top-𝐾 off-policy correction. We train three structurally identical models, using 𝐾 ∈ {1, 2, 16, 32}; The control (production) model is the top-𝐾 off-policy model with 𝐾 = 16. We plot the results during a 5-day experiment in Figure 5. As explained in Section 4.3, with 𝐾 = 1, the top-𝐾 off-policy correction reduces to the standard off-policy correction. A drop of 0.66% ViewTime was observed for 𝐾 = 1 compared with the baseline with 𝐾 = 16. This further confirms the gain we observed shifting from the standard off-policy correction to the top-𝐾 off-policy correction. Setting 𝐾 = 2 still performs worse than the production model, but the gap is reduced to 0.35%. 𝐾 = 32 achieves similar performance as the baseline. We conducted follow up experiment which showed mildly positive gain in ViewTime (+0.15% statistically significant) when 𝐾 = 8.

#### Capping.

Here we consider the effect of the variance reduction techniques on the final quality of the learned recommender. Among the techniques discussed in Section 4.4, weight capping brings the biggest gain online in initial experiments. We did not observe further metric improvements from normalized importance sampling, or TRPO [36]. We conducted a regression test to study the impact of weight capping. We compare a model trained using cap 𝑐 = 𝑒 3 (as in production model) in Equation (9) with one trained using 𝑐 = 𝑒 5 . As we lift the restriction on the importance weight, the learned policy 𝜋𝜃 could potentially overfit to a few logged actions that accidentally receives high reward. Swaminathan and Joachims [43] described a similar effect of propensity overfitting. During live experiment, we observe a significant drop of 0.52% in ViewTime when the cap on importance weight was lifted.

# Conclusion

In this paper we have laid out a practical implementation of a policy gradient-based top-𝐾 recommender system in use at YouTube. We scale up REINFORCE to an action space in the orders of millions and have it stably running in a live production system. To realize the full benefits of such an approach, we have demonstrated how to address biases in logged data through incorporating a learned logging policy and a novel top-𝐾 off-policy correction. We conducted extensive analysis and live experiments to measure empirically the importance of accounting for and addressing these underlying biases. We believe these are important steps in making reinforcement learning practically impactful for recommendation and will provide a solid foundation for researchers and practitioners to explore new directions of applying RL to recommender systems.
