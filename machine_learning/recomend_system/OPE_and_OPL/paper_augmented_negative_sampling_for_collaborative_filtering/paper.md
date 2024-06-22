## link

- https://dl.acm.org/doi/pdf/10.1145/3604915.3608811

## title

Augmented Negative Sampling for Collaborative Filtering

## abstract

Negative sampling is essential for implicit-feedback-based collaborative filtering, which is used to constitute negative signals from massive unlabeled data to guide supervised learning. The stateof-the-art idea is to utilize hard negative samples that carry more useful information to form a better decision boundary. To balance efficiency and effectiveness, the vast majority of existing methods follow the two-pass approach, in which the first pass samples a fixed number of unobserved items by a simple static distribution and then the second pass selects the final negative items using a more sophisticated negative sampling strategy. However, selecting negative samples from the original items in a dataset is inherently restricted due to the limited available choices, and thus may not be able to contrast positive samples well. In this paper, we confirm this observation via carefully designed experiments and introduce two major limitations of existing solutions: ambiguous trap and information discrimination. Our response to such limitations is to introduce “augmented” negative samples that may not exist in the original dataset. This direction renders a substantial technical challenge because constructing unconstrained negative samples may introduce excessive noise that eventually distorts the decision boundary. To this end, we introduce a novel generic augmented negative sampling (ANS) paradigm and provide a concrete instantiation. First, we disentangle hard and easy factors of negative items. Next, we generate new candidate negative samples by augmenting only the easy factors in a regulated manner: the direction and magnitude of the augmentation are carefully calibrated. Finally, we design an advanced negative sampling strategy to identify the final augmented negative samples, which considers not only the score function used in existing methods but also a new metric called augmentation gain. Extensive experiments on real-world datasets demonstrate that our method significantly outperforms state-of-the-art baselines. Our code is publicly available at https://github.com/Asa9aoTK/ANS-Recbole.

# Introduction

Collaborative filtering (CF), as an important paradigm of recommender systems, leverages observed user-item interactions to model users’ potential preferences [13, 15, 35]. In real-world scenarios, such interactions are normally in the form of implicit feedback (e.g., clicks or purchases), instead of explicit ratings [34]. Each observed interaction is normally considered a positive sample. As for negative samples, existing methods usually randomly select some uninteracted items. Then a CF model is optimized to give positive samples higher scores than negative ones via, for example, the Bayesian personalized ranking (BPR) loss function [26], where a score function (e.g., inner product) is used to measure the similarity between a user and an item. Recent studies have shown that negative samples have a great impact on model performance [22, 41, 45]. As the state of the art, hard negative sampling strategies whose general idea is to oversample high-score negative items have exhibited promising performance [4, 8, 9, 41, 44]. While selecting a negative item with a high score makes it harder for a model to classify a user, it has the potential to bring more useful information and greater gradients, which are beneficial to model training [4, 25]. Ideally, one would calculate the scores of all uninteracted items to identify the best negative samples. However, its time complexity is prohibitive. To balance efficiency and effectiveness, the two-pass approach has been widely adopted [1, 9, 16, 41, 44]. The first pass samples a fixed number of unobserved items by a static distribution, and the second pass then selects the final negative items with a more sophisticated negative sampling method.

Despite the significant progress made by hard negative sampling, selecting negative samples from the original items in a dataset is inherently restricted due to the limited available choices. Such original items may not be able to contrast positive samples well. Indeed, we design a set of intuitive experiments to show that existing works suffer from two major drawbacks. (1) Ambiguous trap. Since the vast majority of unobserved items have very low scores (i.e., they are easy negative samples), randomly sampling a small number of candidate negative items in the first pass is difficult to include useful hard negative samples, which, in turn, substantially limits the efficacy of the second pass. (2) Information discrimination. In the second pass, most existing studies overly focus on high-score negative items and largely neglect low-score negative items. We empirically show that such low-score negative items also contain critical, unique information that leads to better model performance. Our response to such drawbacks is to introduce “augmented” negative samples (i.e., synthetic items) that are more similar to positive items while still being negative. While data augmentation techniques have been proposed in other domains [17, 37, 38, 40], it is technically challenging to apply similar ideas to negative sampling for collaborative filtering. This is because all of them fail to carefully regulate and quantify the augmentation needed to approximate positive items while not introducing excessive noise or still being negative. To this end, we present a novel generic augmented negative sampling (ANS) paradigm and then provide a concrete instantiation. Our insight is that it is imperative to understand a negative item’s hardness from a more fine-granular perspective. We propose to disentangle an item’s embedding into hard and easy factors (i.e., a set of dimensions of the embedding vector), where hardness is defined by whether a negative item has similar values to the corresponding user in the given factor. This definition is in line with the definition of hardness in hard negative sampling. Here the key technical challenge originates from the lack of supervision signals. Consequently, we propose two learning tasks that combine contrastive learning (CL) [43] and disentanglement methods [12] to guarantee the credibility of the disentanglement. Since our goal is to create synthetic negative items similar to positive items, we keep the hard factor of a negative item unchanged and focus on augmenting the easy factor by controlling the direction and magnitude of added noise. The augmentation mechanism needs to be carefully designed so that the augmented item will become more similar to the corresponding positive item, but will not cross the decision boundary. Furthermore, we introduce a new metric called augmentation gain to measure the difference between the scores before and after the augmentation. Our sampling strategy is guided by augmentation gain, which gives low-score items with higher augmentation gain a larger probability of being sampled. In this way, we can effectively mitigate information discrimination, leading to better performance. We summarize our main contributions as follows:

- We design a set of intuitive experiments to reveal two notable limitations of existing hard negative sampling methods, namely ambiguous trap and information discrimination.
- To the best of our knowledge, we are the first to propose to generate negative samples from a fine-granular perspective to improve
- implicit CF. In particular, we propose a new direction of generating regulated augmentation to address the unique challenges of CF.
- We propose a general paradigm called augmented negative sampling (ANS) that consists of three steps, including disentanglement, augmentation, and sampling. We also present a concrete implementation of ANS, which is not only performant but also efficient.
- We conduct extensive experiments on five real-world datasets to demonstrate that ANS can achieve significant improvements over representative state-of-the-art negative sampling methods.

# Related Work

## Model-Agnostic Negative Sampling

A common type of negative sampling strategy selects negative samples based on a pre-determined static distribution [6, 36, 39]. Such a strategy is normally efficient since it does not need to be adjusted in the model training process. Random negative sampling (RNS) [5, 26, 35, 40] is a simple and representative model-agnostic sampling strategy, which selects negative samples from unobserved items according to a uniform distribution. However, the uniform distribution is difficult to guarantee the quality of negative samples. Inspired by the word-frequency-based distribution [11] and node-degree-based distribution [23] in other domains, an itempopularity-based distribution [2, 6] has been introduced. Under this distribution, popular items are more likely to be sampled as negative items, which helps to mitigate the widespread popularity bias issue in recommender systems [3]. Although this kind of strategy is generally efficient, the pre-determined distributions are not customized for the underlying models and not adaptively adjusted during the training process. As a result, their performance is often sub-optimal.

## Model-Aware Negative Sampling

These strategies take into consideration some information of the underlying model, denoted by 𝑓 , to guide the sampling process. Given 𝑓 , the probability of sampling an item 𝑖 is defined as 𝑝(𝑖 | 𝑓 ) ∝ 𝑔(𝑓 , e𝑖), where 𝑔(·, ·) is a sampling function, and e𝑖 denotes the embedding of 𝑖. Existing studies focus on choosing different 𝑓 and/or designing a proper 𝑔(·, ·) to achieve better performance. The most representative work is hard negative sampling, which defines 𝑔(·, ·) as a score function. It assigns higher sampling probabilities to the negative items with larger prediction scores [8, 9, 16, 25, 41, 44]. For example, DNS [41] assumes that the high-score items should be more likely to be selected, and thus chooses 𝑔(·, ·) to be the inner product and 𝑓 to be user representations. With the goal of mitigating false negative samples, SRNS [9] further incorporates the information about the last few epochs into 𝑓 and designs 𝑔(·, ·) to give false negative samples lower scores. IRGAN [33] integrates a generative adversarial network into 𝑔(·, ·) to determine the probabilities of negative samples through the min-max game. ReinforcedNS [8] use reinforcement learning into 𝑔(·, ·). With well-designed 𝑓 and 𝑔(·, ·), we can generally achieve better performance. However, selecting suitable negative items need to compute 𝑔(·, ·) for all unobserved items, which is extremely timeconsuming and prohibitively expensive. Take DNS as an example. Calculating the probability of sampling an item is equivalent to performing softmax on all unobserved samples, which is unacceptable in real-world applications [4, 24, 33]. As a result, most model-aware sampling strategies adopt the two-pass approach or its variants. In this case, 𝑔(·, ·) is only applied to a small number of candidates sampled in the first pass. While such two-pass-based negative sampling strategies have been the mainstream methods, they exhibit two notable limitations, namely ambiguous trap and information discrimination, which motivates us to propose an augmented negative sampling paradigm. In the next section, we will explain these limitations via a set of intuitive experiments.

# Limitations of the Two-pass approach

In this section, we first formulate the problem of implicit CF and then explain ambiguous trap and information discrimination via intuitive experiments. We consider the Last.fm and Amazon-Baby datasets in experiments. A comprehensive description of the data is provided in Section 5.

## Implicit CF

We denote the set of historical interactions by O + = {(𝑢,𝑖+ ) | 𝑢 ∈ U,𝑖+ ∈ I}, where U and I are the set of users and the set of items, respectively. The most common implicit CF paradigm is to learn user and item representations (e𝑢 and e𝑖 ) from the historical interactions and then predict the scores of unobserved items to recommend the top-K items. The BPR loss function is widely used to optimize the model:

$$
\tag{1}
$$

where 𝜎(·) is the sigmoid function, and 𝑠(·, ·) is a score function (e.g., the inner product) that measures the similarity between the user and item representations. Here 𝑖 − is a negative sample selected by a sampling strategy. Our goal is to design a negative sampling strategy that is generic to different CF models. Following previous studies [4, 26, 33], without loss of generality, we consider matrix factorization with Bayesian personalized ranking (MF-BPR) [26] as the basic CF model to illustrate ANS.

## Ambiguous Trap

We choose DNS [41], which is the most representative hard negative sampling method, to train an MF-BPR model on the Last.fm dataset and calculate the scores of unobserved user-item pairs in different training periods. Figure 1(a), 1(b), 1(c) demonstrates the frequency distributions of the scores at different epochs. The lowest 80% of the scores are emphasized by the pink shade. We can observe that as training progresses, more and more scores are concentrated in the low-score region, meaning that the vast majority of unobserved items are easy negative samples. Recall that the first pass samples a fixed number of negative items by a uniform distribution. Randomly sampling a small number of negative items in the first pass is difficult to include useful hard negative samples, which, in turn, substantially limits the efficacy of the second pass. We call this phenomenon ambiguous trap.

To further demonstrate the existence of ambiguous trap, in Figure 1(d), we plot the min-max normalizing maximum and minimum scores of the sampled negative items in the first pass on the Last.fm dataset. It can be seen that the difference between the maximum score and the minimum score is consistently small, suggesting that randomly sampling a small number of negative items makes the hardness of the negative samples obtained from DNS far from ideal. Note that a straightforward attempt to mitigate ambiguous trap is to substantially increase the sample size in the first pass. However, it is inevitably at the cost of substantial time and space overhead [4]. Inspired by contrastive learning [17, 37, 40], we propose to augment the sampled negative items to increase their hardness.

## Information Discrimination

In the second pass, most existing studies overly focus on high-score negative items and largely neglect low-score negative items, which also contain critical, unique information to improve model performance. Overemphasizing high-score items as negative samples may result in worse model performance. Several studies [4, 27] have made efforts to assign lower sampling probabilities to low-score items using algorithms like softmax and its derivatives. However, selecting those significantly lower-score items in comparison to others, remains a challenge. We call this behavior information discrimination. To verify the existence of information discrimination, we introduce a new measure named Pairwise Exclusive-hit Ratio (PER) [18] to CF, which is used to compare the difference between the information learned by two different methods. More specifically, PER(𝑥, 𝑦) quantifies the information captured by the method 𝑥 but not by 𝑦 via

$$
\tag{2}
$$

where H𝑥 denotes the set of test interactions correctly predicted by the method 𝑥. Next, we choose two representative negative sampling methods, RNS [8] and DNS [41] to train MF-BPR models and calculate the PER between them. Recall that DNS is more likely to select high-score negative items while RNS uniformly randomly selects negative items irrespective of their scores. The obtained results are depicted in Figure 2 (excluding HNS data for the current analysis). We can observe that: (1) the DNS strategy can indeed learn more information, confirming the benefits of leveraging hard negative samples to form a tighter decision boundary. (2) The values of PER(RNS, DNS) on two datasets (0.2 and 0.33) indicate that even the simple RNS strategy can still learn rich information that is not learned by DNS. In other words, the easy negative items overlooked by DNS are still valuable for CF. Such an information discrimination problem inspires us to understand a negative item’s hardness from a more fine-granular perspective in order to extract more useful information.

# Methodology

Driven by the aforementioned limitations, we propose a novel generic augmented negative sampling (ANS) paradigm, which consists of three major steps: disentanglement, augmentation, and sampling. The disentanglement step learns an item’s hard and easy factors; the augmentation step adds regulated noise to the easy factor so as to increase the item’s hardness; the sampling strategy selects the final negative samples based on a new metric we propose. The workflow of ANS is illustrated in Figure 3. Note that these steps can be implemented by different methods and thus the overall paradigm is generic. We present a possible instantiation in the following sections.

## Disentanglement

To understand a negative item’s hardness from a more fine-granular perspective, we propose to disentangle its embedding into hard and easy factors (i.e., a set of dimensions of the embedding vector), where hardness is defined by whether a negative item has similar values to the corresponding user in the given factor. Similarly, we follow the two-pass approach to first randomly sample 𝑀 (𝑀 ≪ |I|) items from the unobserved items to form a candidate negative set E. We design a gating module to identify which dimensions of a negative item e𝑛 ∈ R 𝑑 in E are hard with respect to user e𝑢 ∈ R 𝑑 via

$$
\tag{3}
$$

where 𝑔𝑎𝑡𝑒ℎ𝑎𝑟𝑑 ∈ R 𝑑 gives the weights of different dimensions. The sigmoid function 𝜎(·) maps the values to (0, 1). W𝑖𝑡𝑒𝑚 ∈ R 𝑑×𝑑 and W𝑢𝑠𝑒𝑟 ∈ R 𝑑×𝑑 are linear transformations used to ensure that the user and item embeddings are in the common latent space [22]. ⊙ is the element-wise product, which measures the similarity between e𝑖 and e𝑢 in each dimension [35]. After obtaining the weights 𝑔𝑎𝑡𝑒ℎ𝑎𝑟𝑑 , we adopt the element-wise product to extract the hard factor e ℎ𝑎𝑟𝑑 𝑛 . The easy factor e 𝑒𝑎𝑠𝑦 𝑛 is then calculated via element-wise subtraction [12].

$$
\tag{4}
$$

Due to the lack of ground truth for hard and easy factors, it is inherently difficult to guarantee the credibility of the disentanglement. Inspired by its superiority in unsupervised scenarios [19, 43], we propose to adopt contrastive learning to guide the disentanglement. By definition, the hard factor of a negative item should be more similar to the user, while the easy factor should be the opposite. Therefore, given a score function 𝑠(·, ·) to calculate the similarity between a pair, we design a contrastive loss L𝑐 as

$$
\tag{5}
$$

However, optimizing only L𝑐 may lead to a trivial solution: including all dimensions as the hard factor. Therefore, we introduce another loss with the auxiliary information from positive items. We adopt a similar operation with the same weights 𝑔𝑎𝑡𝑒ℎ𝑎𝑟𝑑 to obtain the corresponding positive item factor e ′ 𝑝 and e ′′ 𝑝 :

$$
\tag{6}
$$

This is particularly important as e 𝑒𝑎𝑠𝑦 𝑛 may emphasize the first 48 dimensions while e ℎ𝑎𝑟𝑑 𝑛 may emphasize the last 14. In order to ensure coherence in subsequent operations, it is imperative to maintain the correspondence of dimensions. For ease of understanding, reader can directly regard them as positive samples. Intuitively, e ℎ𝑎𝑟𝑑 𝑛 should be more similar to positive since it is difficult for users to discern it as a negative sample (both have a high similarity to the user). However, this signal is not entirely reliable, as it may not accurately reflect a user’s level of interest. Therefore, instead of relying on a stringent constraint like Equation 5, we introduce another disentanglement loss L𝑑 as

$$
\tag{7}
$$

where the Euclidean distance is used to measure the similarity between e ′ 𝑝 and e ℎ𝑎𝑟𝑑 𝑛 while the score function is used to measure the similarity between e 𝑒𝑎𝑠𝑦 𝑝 and e ′′ 𝑛 . This is because we want to leverage only reliable hardness while we can be more lenient with the easy part.

## Augmentation

Next, we propose an augmentation module to create synthetic negative items which are more similar to the corresponding positive items. After the disentanglement step, we have obtained the hard and easy factors of a negative item, where the hard factor contains more useful information for model training. Therefore, our goal is to augment the easy factor to improve model performance. However, existing augmentation techniques fail to carefully regulate and quantify the augmentation needed to approximate positive items while still being negative. To this end, we propose to regulate the augmentation from two different aspects: Direction: Intuitively, the direction of the augmentation on a negative item should be towards the corresponding positive item. Therefore, we first calculate the difference e𝑑𝑖 𝑓 between the factor of the positive item e ′′ 𝑝 and the easy factor of the negative item e 𝑒𝑎𝑠𝑦 𝑛 :

$$
\tag{8}
$$

A first attempt is to directly make e𝑑𝑖 𝑓 as the direction of the augmentation. This design is less desirable because (1) it introduces too much positive information, which may turn the augmented negative item into positive. (2) It contains too much prior information (i.e., the easy factor is identical to that of the positive item), which can lead to the model collapse problem [28, 29]. Inspired by [40], we carefully smooth the direction of augmentation by extracting the quadrant information e𝑑𝑖𝑟 of e𝑑𝑖 𝑓 with the sign function 𝑠𝑔𝑛(·):

$$
\tag{9}
$$

The direction e𝑑𝑖𝑟 ∈ R 𝑑 effectively compresses the embedding augmentation space into a quadrant space, which provides essential direction information without having the aforementioned issues. Magnitude: Magnitude determines the strength of augmentation. Several studies [14] have shown that when the perturbation to the embedding is overly large, it will dramatically change its original semantics. Therefore, we need to carefully calibrate the magnitude of the augmentation. We design a two-step approach to generate a regulated magnitude Δ ∈ R 𝑑 . We first consider the distribution of Δ. As Δ is a noise embedding, we adopt a uniform distribution on the interval [0, 0.1]. The uniform distribution introduces a certain amount of randomness, which is beneficial to improve the robustness of the model. Second, we restrict Δ to be smaller than a margin. Instead of using a static scalar [22], we dynamically set the margin by calculating the similarity between the hard factors of the negative and corresponding positive items. The intuition is that a higher similarity between the hard factors suggests that the negative item already contains much useful information, and thus we should augment it with a smaller magnitude. Finally, the regulated magnitude Δ is calculated via

$$
\tag{10}
$$

where the element-wise product ⊙ is used to calculate the similarity between e ℎ𝑎𝑟𝑑 𝑛 and e ′ 𝑝 . The transformation matrix W ∈ R 1×𝑑 is used to map the similarity vector to a scalar. The sigmoid function 𝜎(·) helps remove the sign information to avoid interfering with the learned direction e𝑑𝑖𝑟. After carefully determining the direction and magnitude, we can generate the augmented version e 𝑎𝑢𝑔 𝑛 of the negative item e𝑛 as follows

$$
\tag{11}
$$

With our design, the augmented negative item becomes more similar to the corresponding positive item without causing huge changes of the semantics, and can remain negative. We apply the above operation to every item in the candidate negative set E and obtain the augmented negative set E 𝑎𝑢𝑔 .

## Sampling

After obtaining the augmented candidate negative set E 𝑎𝑢𝑔, we need to devise a sampling strategy to select the best negative item from E 𝑎𝑢𝑔 to facilitate model training. Existing hard negative sampling methods select the negative item with the highest score, where the score is calculated by the score function 𝑠(·, ·) with the user and negative item embeddings as input. However, as explained before, negative items with relatively low scores will be seldom selected, which leads to the information discrimination issue. Although the augmentation can already alleviate information discrimination to a certain extent, we further design a more flexible and effective sampling strategy by introducing a new metric named augmentation gain. Augmentation gain measures the score difference before and after the augmentation. Formally, the score 𝑠𝑐𝑜𝑟𝑒 and the augmentation gain 𝑠𝑐𝑜𝑟𝑒𝑎𝑢𝑔 are calculated as:

$$
\tag{12}
$$

The sampling module we propose considers both 𝑠𝑐𝑜𝑟𝑒 and 𝑠𝑐𝑜𝑟𝑒𝑎𝑢𝑔 to select the suitable negative item e 𝑓 𝑖𝑛𝑎𝑙 𝑛 from the augmented candidate negative set E 𝑎𝑢𝑔. To explicitly balance the contributions between 𝑠𝑐𝑜𝑟𝑒 and 𝑠𝑐𝑜𝑟𝑒𝑎𝑢𝑔, we introduce a trade-off parameter 𝜖. The final augmented negative item e 𝑓 𝑖𝑛𝑎𝑙 𝑛 is chosen via

$$
\tag{13}
$$

## Discussion

It is worth noting that most existing negative sampling methods can be considered as a special case of ANS. For example, DNS [41] can be obtained by removing the disentanglement and augmentation steps. MixGCF [16] can be obtained by removing the disentanglement step and replacing the regulated augmentation with unconstrained augmentation based on graph structure information and positive item information. SRNS [9] can be obtained by removing the augmentation step and considering variance in the sampling strategy step.

## Model Optimization

Finally, we adopt the proposed ANS method as the negative sampling strategy and take into consideration also the recommendation loss L to optimize the parameters Θ of an implicit CF model (e.g., MF-BPR).

$$
\tag{14}
$$

where 𝜆 is a hyper-parameter controlling the strength of 𝐿2 regularization, and 𝛾 is another hyper-parameter used to adjust the impact of the contrastive loss and the disentanglement loss. Observably, our negative sampling strategy paradigm can be seamlessly incorporated into mainstream models without the need for substantial modifications.

# Experiment

In this section, we conduct comprehensive experiments to answer the following key research questions: • RQ1: How does ANS perform compared to the baselines and integrating ANS into different mainstream CF models perform compared with the original ones? • RQ2: How accurate is the disentanglement step in the absence of ground truth? • RQ3: Can ANS alleviate ambiguous trap and information discrimination? • RQ4: How do different steps affect ANS’s performance? • RQ5: How do different hyper-parameter settings (i.e., 𝛾, 𝜖, and 𝑀) affect ANS’s performance? • RQ6: How does ANS perform in efficiency?

## Experimental Setup

### Datasets.

We consider five public benchmark datasets in the experiments: Amazon-Baby, Amazon-Beauty, Yelp2018, Gowalla, and Last.fm. In order to comprehensively showcase the efficacy of the proposed methodology, we have partitioned the dataset into two distinct categories for processing. For the datasets Amazonbaby, Amazon-Beauty, and Last.fm, the training set is constructed by including only the interactions that occurred on or before a specified timestamp, similar to the approach used in the state-of-theart method DENS [21]. After reserving the remaining interactions for the test set, a validation set is created by randomly sampling 10% of the interactions from the training set. The adoption of this strategy, as suggested by previous works [4, 22, 32], provides the benefit of preventing data leakage. For Yelp and Gowalla, we have followed the conventional practice of utilizing an 80% training set, 10% test set, and 10% validation set. These datasets have different statistical properties, which can reliably validate the performance of a model [7]. Table 1 summarizes the statistics of the datasets.

### 2 Baseline Algorithms.

To demonstrate the effectiveness of the proposed ANS method, we compare it with several representative state-of-the-art negative sampling methods. • RNS [26]: Random negative sampling (RNS) adopts a uniform distribution to sample unobserved items. • DNS [41]: Dynamic negative sampling (DNS) adaptively selects items with the highest score as the negative samples. • SRNS [9]: SRNS introduces variance to avoid the false negative item problem based on DNS. • MixGCF [16]: MixGCF injects information from positive and graph to synthesizes harder negative samples. • DENS [21]: DENS disentangles relevant and irrelevant factors of items and designs a factor-aware sampling strategy. To further validate the effectiveness of our proposed methodology, we have integrated it with a diverse set of representative models. • NGCF [35]: NGCF employs a message-passing scheme to effectively leverage the high-order information. • LightGCN [13]: LightGCN adopts a simplified approach by eliminating the non-linear transformation and instead utilizing a sum-based pooling module to enhance its performance. • SGL [37]: SGL incorporates contrastive learning. The objective is to enhance the agreement between various views of the same node, while minimizing the agreement between views of different nodes.

### Implementation Details.

Similar to previous studies [4, 26, 33], we consider MF-BPR [26] as the basic CF model. For a fair comparison, the size of embeddings is fixed to 64, and the embeddings are initialized with Xavier [10] for all methods. We use Adam [20] to optimize the parameters with a default learning rate of 0.001 and a default mini-batch size of 2048. The 𝐿2 regularization coefficient 𝜆 is set to 10−4 . The size of the candidate negative item set 𝑀 is tested in the range of {2, 4, 8, 16, 32}. The weight 𝛾 of the contrastive and disentanglement losses and 𝜖 of the augmentation gain are both searched in the range of [0, 1]. In order to guarantee the replicability, our approach is implemented by the RecBole v1.1.1 framework [42]. We conducted statistical tests to evaluate the significance of our experimental results.

## RQ1: Overall Performance Comparison

Table 2 shows the results of training MF-BPR with different negative sampling methods. Additionally, the performance of ANS under different models is presented in Table 3. Due to space limitations, we are unable to present the results of other models using various negative sampling strategies. Nonetheless, it is worth noting that the experimental results obtained were similar with Table 2. We can make the following key observations:

• ANS yields the best performance on almost all datasets. In particular, its highest improvements over the strongest baselines are 29.74%, 23.76%, and 31.06% in terms of 𝐻𝑖𝑡 𝑅𝑎𝑡𝑖𝑜@15, 𝑅𝑒𝑐𝑎𝑙𝑙@15, and 𝑁𝐷𝐶𝐺@15 in Beauty, respectively. This demonstrates that ANS is capable of generating more informative negative samples. • The ANS’s remarkable adaptability is a noteworthy feature that allows for its seamless integration into various models. The results presented in Table 3 demonstrate that the incorporation of PAN into the base models leads to improvements across all datasets. • The model-aware methods always outperform the model-agnostic methods (RNS). In general, model-agnostic methods are difficult to guarantee the quality of negative samples. Leveraging various information from the underlying model is indeed a promising research direction. • Despite its simplicity, DNS is a strong baseline. This fact justifies our motivation of studying the hardness from a more fine granularity.

## RQ2: Disentanglement Performance

To verify the disentanglement performance, we spot-check a user and use the T-SNE algorithm [30] to map the disentangled factors into a two-dimensional space. The results are shown in Figure 4(a). We can observe that e ℎ𝑎𝑟𝑑 𝑛 and e ′ 𝑝 are clustered together, confirming that they are indeed similar. In contrast, e 𝑒𝑎𝑠𝑦 𝑛 and e ′′ 𝑝 are more scattered, indicating that they do not carry similar information, which is consistent with our previous analysis. The hard factors should contain most of the useful information of negative items, and thus if we use only hard factors, instead of the entire original item, to train a model, we should achieve similar performance. We validate it by two experiments. First, we plot the curves of 𝑅𝑒𝑐𝑎𝑙𝑙@20 in Figure 4(b). HNS is a variant of RNS, which uses our disentanglement step to extract the hard factors of items and then uses only hard factors to train the model. It can be observed that the performance of HNS is comparable to that of RNS. The two curves are similar, confirming that the hard factors indeed capture the most useful information of negative items. Second, we revisit Figure 2 in Section 3.3. It can be seen that PER(RNS, HNS) is small, which means that HNS captures most of information learned in RNS. In summary, our disentanglement step can effectively disentangle a negative sample into hard and easy factors, which lays a solid foundation for the subsequent steps in ANS.

## RQ3: Ambiguous Trap and Information Discrimination

### Ambiguous Trap.

Demonstrating how ANS can mitigate the ambiguous trap is a challenging task. A first attempt is to show the augmentation gain of the augmented negative samples. However, this idea is flawed because larger augmentation gain cannot always guarantee better performance (e.g., larger augmentation gain can be achieved by introducing a large number of false positive items). Therefore, we choose to analyze the curves of 𝑅𝑒𝑐𝑎𝑙𝑙@20 to show how ANS can mitigate the ambiguous trap, which is shown in Figure 5. Generally, the steeper the curve is, the more information the model can learn in this epoch from negative samples. We can observe that DNS outperforms RNS because its 𝑅𝑒𝑐𝑎𝑙𝑙@20 is always higher than that of RNS and the curve is steeper than that of RNS. It again confirms that hard negative sampling is an effective sampling strategy. In contrast, the curve of ANS exhibits distinct patterns. At the beginning (from epoch 0 to epoch 30), 𝑅𝑒𝑐𝑎𝑙𝑙@20 is low because ANS needs extra efforts to learn how to disentangle and augment negative samples. As the training process progresses (from epoch 30 to epoch 95), ANS demonstrates a greater average gradient. This proves that ANS can generate harder synthetic negative samples, which can largely mitigate the ambiguous trap issue.

### Information Discrimination.

As for the information discrimination problem, we have shown that the disentanglement step can effectively extract the useful information from low-score items. However, we have not shown that ANS can select more low-score negative items in the training process. To this end, we analyze the percentages of overlapping negative samples between ANS and DNS. The results are presented in Table 4. Recall that DNS always chooses the negative items with the highest scores as the hard negative samples. A less than 50% overlapping indicates that ANS does sample more low-score negative items before the augmentation and effectively alleviates the information discrimination problem.

## RQ4: Ablation Study

We analyze the effectiveness of different components in our model, and evaluate the performance of the following variants of our model: (1) ANS without disentanglement (ANS w/o dis). (2) ANS without augmentation gain (ANS w/o gain). (3) ANS without regulated direction (ANS w/o dir). (4) ANS without regulated magnitude (ANS w/o mag). It is noteworthy to state that the complete elimination of the augmentation step is not taken into consideration due to its equivalence to DNS. The results are presented in Table 5. We can observe that all components we propose can positively contribute to model performance. In particular, the results show that unconstrained augmentation (e.g., ANS w/o mag) cannot achieve meaningful performance. This fact confirms that the existing unconstrained augmentation techniques cannot be directly applied to CF.

## RQ5: Hyper-Parameter Sensitivity

### Impact of 𝛾.

We present the effect of the weight of the contrastive loss and disentanglement loss, 𝛾, in Figure 6. As the value of 𝛾 increases, we can first observe notable performance improvements, which proves that both loss functions are beneficial for the CF model. It is interesting to observe that once 𝛾 becomes larger than a threshold, the performance drops sharply. This observation is expected because in this case the CF model considers the disentanglement as the primary task and ignores the recommendation task. Nevertheless, ANS can achieve reasonable performance under a relatively wide range of 𝛾 values.

### Impact of 𝜖.

Recall that 𝜖 is the parameter to balance the importance between the score and the augmentation gain in the sampling step. Figure 7(a) presents the results of different 𝜖 values. A small 𝜖 value overlooks the importance of the augmentation gain and only achieves sub-optimal performance; a large 𝜖 value may favor an item with a lower score (but a larger score difference), which will reduce the gradient and hurt model performance. But still, ANS can obtain good performance under a relatively wide range of 𝜖 values.

### Impact of 𝑀.

𝑀 denotes the size of candidate negative set E. The present study illustrates the impact of 𝑀 on performance, as depicted in Figure 8. It is evident that an increase in 𝑀 leads to more negative samples, we can get harder negative samples by augmentation, thereby resulting in a performance improvement. Nevertheless, it is noteworthy that excessively large values of 𝑀 can considerably impede the efficiency of the models, and degrade performance due to noise (e.g., false negative samples).

## RQ6: Efficiency Analysis

Following the previous work [22, 31], we also examine the efficiency of different negative sampling methods in Table 6. We report the average running time (in seconds) per epoch and the total number of epochs needed before reaching convergence. All three methods are relatively efficient. There is no wonder that RNS is the most efficient method as it is a model-agnostic strategy. Compared to DNS, our proposed ANS method requires more running time. However, considering the huge performance improvement ANS brings, the additional running time is well justified.

# Conclusion

Motivated by ambiguous trap and information discrimination, from which the state-of-the-art negative sampling methods suffer, for the first time, we proposed to introduce synthetic negative samples from a fine-granular perspective to improve implicit CF. We put forward a novel generic augmented negative sampling (ANS) paradigm, along with a concrete implementation. The paradigm consists of three major steps. The disentanglement step disentangles negative items into hard and easy factors in the absence of supervision signals. The augmentation step generates synthetic negative items using carefully calibrated noise. The sampling step makes use of a new metric called augmentation gain to effectively alleviate information discrimination. Comprehensive experiments demonstrate that ANS can significantly improve model performance and represents an exciting new research direction. In our future work, we intend to explore the efficacy of augmented negative samples in tackling various issues such as fairness and popularity bias. Additionally, we will actively investigate the effectiveness of employing augmented negative sampling in online experiments.
