## link

https://arxiv.org/pdf/2305.05585.pdf

## title

Improving Implicit Feedback-Based Recommendation through Multi-Behavior Alignment

## abstruct

Recommender systems that learn from implicit feedback often use large volumes of a single type of implicit user feedback, such as clicks, to enhance the prediction of sparse target behavior such as purchases. Using multiple types of implicit user feedback for such target behavior prediction purposes is still an open question. Existing studies that attempted to learn from multiple types of user behavior often fail to: (i) learn universal and accurate user preferences from different behavioral data distributions, and (ii) overcome the noise and bias in observed implicit user feedback. To address the above problems, we propose multi-behavior alignment (MBA), a novel recommendation framework that learns from implicit feedback by using multiple types of behavioral data. We conjecture that multiple types of behavior from the same user (e.g., clicks and purchases) should reflect similar preferences of that user. To this end, we regard the underlying universal user preferences as a latent variable. The variable is inferred by maximizing the likelihood of multiple observed behavioral data distributions and, at the same time, minimizing the Kullback–Leibler divergence (KL-divergence) between user models learned from auxiliary behavior (such as clicks or views) and the target behavior separately. MBA infers universal user preferences from multi-behavior data and performs data denoising to enable effective knowledge transfer. We conduct experiments on three datasets, including a dataset collected from an operational e-commerce platform. Empirical results demonstrate the effectiveness of our proposed method in utilizing multiple types of behavioral data to enhance the prediction of the target behavior.

# Introduction

Recommender systems aim to infer user preferences from observed user-item interactions and recommend items that match those preferences. Many operational recommender systems are trained from implicit user feedback [14, 16]. Recommender systems that learn from implicit user feedback are typically trained on a single type of implicit user behavior, such as clicks. However, in real-world scenarios, multiple types of user behavior are logged when a user interacts with a recommender system. For example, users may click, add to a cart, and purchase items on an e-commerce platform [31]. Simply learning recommenders from a single type of behavioral data such as clicks can lead to a misunderstanding of a user’s real user preferences since the click data is noisy and can easily be corrupted due to bias [5], and thus lead to suboptimal target behavior (e.g., purchases) predictions. Meanwhile, only considering purchase data tends to lead to severe cold-start problems [26, 41, 48] and data sparsity problems [23, 27]. Using multiple types of behavioral data. How can we use multiple types of auxiliary behavioral data (such as clicks) to enhance the prediction of sparse target user behavior (such as purchases) and thereby improve recommendation performance? Some prior work [2, 12] has used multi-task learning to train recommender systems on both target behavior and multiple types of auxiliary behavior. Building on recent advances in graph neural networks, Jin et al. [18] encode target behavior and multiple types of auxiliary behavior into a heterogeneous graph and perform convolution operations on the constructed graph for recommendation. In addition, recent research tries to integrate the micro-behavior of useritem interactions into representation learning in the sequential and session-based recommendation [25, 44, 46]. These publications focus on mining user preferences from user-item interactions, which is different from our task of predicting target behavior from multiple types of user behavior. Limitations of current approaches. Prior work on using multiple types of behavioral data to improve the prediction of the target behavior in a recommendation setting has two main limitations. The first limitation concerns the gap between data distributions of different types of behavior. This gap impacts the learning of universal and effective user preferences. For example, users may have clicked on but not purchased items, resulting in different positive and negative instance distributions across auxiliary and target behaviors. Existing work typically learns separate user preferences for different types of behavior and then combines those preferences to obtain an aggregate user representation. We argue that: (i) user preferences learned separately based on different types of behavior may not consistently lead to the true user preferences, and (ii) multiple types of user behavior should reflect similar user preferences; in other words, there should be an underlying universal set of user preferences under different types of behavior of the same user. The second limitation concerns the presence of noise and bias in auxiliary behavioral data, which impacts knowledge extraction and transfer. A basic assumption of recommendations based on implicit feedback is that observed interactions between users and items reflect positive user preferences, while unobserved interactions are considered negative training instances. However, this assumption seldom holds in reality. A click may be triggered by popularity bias [5], which does not reflect a positive preference. And an unobserved interaction may be attributed to a lack of exposure [6]. Hence, simply incorporating noisy or biased behavioral data may lead to sub-optimal recommendation performance. Motivation. Our assumption is that multiple types of behavior from the same user (e.g., clicks and purchases) should reflect similar preferences of that user. To illustrate this assumption, consider Figure 1, which shows distributions of items that two users (𝑢1 and 𝑢2) interacted with (clicks 𝑐 and purchases 𝑝), in the Beibei and Taobao datasets (described in Section 4.2 below). For both users, the items they clicked or purchased are relatively close. These observations motivate our hypothesis that multiple types of user behavior reflect similar user preferences, which is vital to improve the recommendation performance further. Proposed method. To address the problem of learning from multiple types of auxiliary behavioral data and improve the prediction of the target behavior (and hence recommendation performance), we propose a training framework called multi-behavior alignment (MBA). MBA aligns user preferences learned from different types of behavior. The key assumption behind MBA is that multiple types of behavior from the same user reflect similar underlying user preferences. To address the data distribution limitation mentioned above, we utilize KL-divergence to measure the discrepancy between user models learned from multiple types of auxiliary behavior and target behavior, and then conduct knowledge transfer by minimizing this discrepancy to improve the recommendation performance. For the second limitation mentioned above (concerning noise and bias in behavioral data), MBA regards the underlying universal user preferences as a latent variable. The variable is then inferred by maximizing the likelihood of multiple types of observed behavioral data while minimizing the discrepancy between models trained on different types of behavioral data. In this manner, MBA denoises multiple types of behavioral data and enables more effective knowledge transfer across multiple types of user behavior. To demonstrate the effectiveness of the proposed method, we conduct extensive experiments on two open benchmark datasets and one dataset collected from an operational e-commerce platform. Experimental results show that the proposed MBA framework outperforms related state-of-the-art baselines. Main contributions. Our main contributions are as follows: • We argue that multiple types of auxiliary and target behavior should reflect similar user preferences, and we propose to infer the true user preferences from multiple types of behavioral data. • We propose a learning framework MBA to jointly perform data denoising and knowledge transfer across multiple types of behavioral data to enhance target behavior prediction and hence improve the recommendation performance. • We conduct experiments on three datasets to demonstrate the effectiveness of the MBA method. One of these datasets is collected from an operational e-commerce platform, and includes clicks and purchase behavior data. Experimental results show state-of-the-art recommendation performance of the proposed MBA method.

# Related Work

We review prior work on multi-behavior recommendation and on denoising methods for recommendation from implicit feedback.

## Multi-behavior recommendation

Unlike conventional implicit feedback recommendation models [15, 21], which train a recommender on a single type of user behavior (e.g., clicks), multi-behavior recommendation models use multiple types of auxiliary behavior data to enhance the recommendation performance on target behavior [1, 7, 12, 18, 33, 37, 39]. Recent studies use multi-task learning to perform joint optimization on learning auxiliary behavior and target behavior. For example, Gao et al. [12] propose a multi-task learning framework to learn user preferences from multi-behavior data based on a pre-defined relationship between different behavior. Since different behavioral interactions between users and items can form a heterogeneous graph, recent studies also focus on using graph neural network (GNN) to mine the correlations among different types of behavior. For example, Wang et al. [33] uses the auxiliary behavior data to build global item-to-item relations and further improve the recommendation performance of target behavior. Jin et al. [18] propose a graph convolutional network (GCN) based model on capturing the diverse influence of different types of behavior and the various semantics of different types of behavior. Xia et al. [39] incorporate multi-behavior signals through graph-based meta-learning. Chen et al. [1] regard the multi-behavior recommendation task as a multirelationship prediction task and train the recommender with an efficient non-sampling method. Additionally, some studies apply contrastive learning or a variational autoencoder (VAE) to improve the multi-behavior recommender. Xuan et al. [42] propose a knowledge graph enhanced contrastive learning framework to capture multi-behavioral dependencies better and solve the data sparsity problem of the target behavior, and Ma et al. [24] propose a VAEbased model to conduct multi-behavior recommendation. Another related research field is based on micro-behaviors [25, 44, 46], which utilize the micro-operation sequence in the process of user-item interactions to capture user preferences and predict the next item. For example, Yuan et al. [44] focus on “sequential patterns” and “dyadic relational patterns” in micro-behaviors, and then use an extended self-attention network to mine the relationship between micro-behavior and user preferences. This work focuses on mining user preferences from the micro-operation sequence. However, existing studies still neglect the different data distributions across multiple types of user behavior, and thus fail to learn accurate and universal user preferences. Besides, prior work does not consider the noisy signals of user implicit feedback data, resulting in ineffective knowledge extraction and transfers.

## Recommendation denoising

Existing recommender systems are usually trained with implicit feedback since it is much easier to collect than explicit ratings [28]. Recently, some research [17, 32, 36] has pointed out that implicit feedback can easily be corrupted by different factors, such as various kinds of bias [5] or users’ mistaken clicks. Therefore, there have been efforts aimed at alleviating the noisy problem of implicit recommendation. These efforts include sample selection methods [8– 11, 36, 43], re-weighting methods [3, 30, 32, 32, 35], methods using additional information [19, 22, 45], and methods designing specific denoising architectures [4, 13, 38, 40]. Sample selection methods aim to design more effective samplers for model training. For example, Gantner et al. [11] consider popular but un-interacted items as items that are highly likely to be negative ones, while Ding et al. [8] consider clicked but not purchased items as likely to be negative samples. Re-weighting methods typically identify noisy samples as instances with higher loss values and then assign lower weights to them. For example, Wang et al. [32] discard the large-loss samples with a dynamic threshold in each iteration. Wang et al. [35] utilize the differences between model predictions as the denoising signals. Additional information such as dwell time [19], gaze pattern [45] and auxiliary item features [22] can also be used to denoise implicit feedback. Methods designing specific denoising architectures improve the robustness of recommender systems by designing special modules. Wu et al. [38] use self-supervised learning on user-item interaction graphs to improve the robustness of graph-based recommendation models. Gao et al. [13] utilize the self-labeled memorized data as denoising signals to improve the robustness of recommendation models. Unlike the work listed above, which does not consider multiple types of user behavior, in this work, we focus on extracting underlying user preferences from (potentially) corrupted multi-behavior data and then conducting knowledge transfer to improve the recommendation performance.

# Method

In this section, we detail our proposed MBA framework for multibehavior recommendation. We first introduce notations and the problem formulation in Section 3.1. After that, we describe how to perform multi-behavior alignment on noisy implicit feedback in Section 3.2. Finally, training details are given in Section 3.3.

## Notation and problem formulation

We write 𝑢 ∈ U and 𝑖 ∈ I for a user and an item, where U and I indicate the user set and the item set, respectively. Without loss of generality, we regard click behavior as the auxiliary behavior and purchase behavior as the target behavior. We write R𝑓 ∈ R |U |× |I| for the observed purchase behavior data. Specifically, each item 𝑟 𝑓 𝑢,𝑖 ∈ R𝑓 is set to 1 if there is a purchase behavior between user 𝑢 and item 𝑖; otherwise 𝑟 𝑓 𝑢,𝑖 is set as 0. Similarly, we denote R𝑔 ∈ R |U |× |I | as the observed click behavior data, where each 𝑟 𝑔 𝑢,𝑖 ∈ R𝑔 is set as 1 if there is a click behavior between user 𝑢 and item 𝑖; otherwise 𝑟 𝑔 𝑢,𝑖 = 0. We use 𝑃 (R𝑓 ) and 𝑃 (R𝑔) to denote the user preference distribution learned from R𝑓 and R𝑔, respectively. We assume that there is an underlying latent true user preference matrix R𝑡 with 𝑟 𝑡 𝑢,𝑖 ∈ R𝑡 as the true preference of user 𝑢 over item 𝑖. The probabilistic distribution of R𝑡 is denoted as 𝑃 (R𝑡). Both the data observation of R𝑓 and R𝑔 is motivated by the latent universal true user preference distribution 𝑃 (R𝑡) plus different kinds of noises or biases. Formally, we assume that 𝑃 (R𝑡) follows a Bernoulli distribution and can be approximated by a target recommender model 𝑡𝜃 with 𝜃 as the parameters:

$$
\tag{1}
$$

Since the true user preferences 𝑟 𝑡 𝑢,𝑖 are intractable, we need to introduce the learning signals from the observed 𝑟 𝑓 𝑢,𝑖 and 𝑟 𝑔 𝑢,𝑖 to infer 𝑟 𝑡 𝑢,𝑖. As a result, we introduce the following models to depict the correlations between the observed user implicit feedback (i.e., 𝑟 𝑓 𝑢,𝑖 and 𝑟 𝑔 𝑢,𝑖 ) and the latent true user preferences 𝑟 𝑡 𝑢,𝑖:

$$
\tag{2}
$$

where ℎ 𝑓 𝜙 (𝑢,𝑖) and ℎ 𝑓 𝜑 (𝑢,𝑖) are parameterized by 𝜙 and 𝜑 in the observed purchase behavior data, respectively, while ℎ 𝑔 𝜙′ (𝑢,𝑖) and ℎ 𝑔 𝜑′ (𝑢,𝑖) are parameterized by 𝜙 ′ and 𝜑 ′ in the observed click behavior data respectively. The target of our task is formulated as follows: given the observed multi-behavior user implicit feedback, i.e., R𝑓 and R𝑔, we aim to train the latent true user preference model 𝑡𝜃 , and then use 𝑡𝜃 to improve the prediction performance on target behavior. More precisely, during model inference, we introduce both 𝑃 (Rf ) and 𝑃 (Rt) to perform the target behavior recommendation and use a hyperparameter 𝛽 to balance the 𝑃 (Rt) and 𝑃 (Rf ), which is formulated as:

$$
\tag{3}
$$

We select items with the highest score as the target behavior recommendation results.

## Multi-behavior alignment on noisy data

The key motivation for MBA is that multiple types of user behavior should reflect similar user preferences. Hence, Eq. 4 is expected to be achieved with the convergence of the training models:

$$
\tag{4}
$$

Therefore, 𝑃 (R𝑓 ) and 𝑃 (R𝑡) should have a relatively small KLdivergence, which is formulated as follows:

$$
\tag{5}
$$

Similarly, we also have the KL-divergence between 𝑃 (R𝑔) and 𝑃 (R𝑡):

$$
\tag{6}
$$

However, naively minimizing the above KL-divergence is not feasible since it overlooks the data distribution gaps and correlations between multiple types of behavior. To address this issue, we use Bayes’ theorem to rewrite 𝑃 (R𝑡) as follows:

$$
\tag{7}
$$

By substituting the right part of Eq. 7 into Eq. 5 and rearranging erms, we obtain the following equation:

$$
\tag{8}
$$

Since 𝐾𝐿[𝑃 (R𝑓 ) ∥𝑃 (R𝑡 | R𝑔)] ≥ 0, the left side of Eq. 8 is an approximate lower bound of the logarithm log 𝑃 (R𝑔). The bound is satisfied if, and only if, 𝑃 (R𝑓 ) perfectly recovers 𝑃 (R𝑡 | R𝑔), which means 𝑃 (R𝑓 ) trained on the observed target behavior can perfectly approximates the true user preference distribution captured from the auxiliary behavior data. The above condition is in line with the main motivation of the MBA, i.e., different behavior data should reflect similar user preferences. We see that the left side of Eq. 8 is based on the expectation over 𝑃 (R𝑓 ), which means that we are trying to train 𝑃 (R𝑓 ) with the given corrupted auxiliary behavior data R𝑔 (i.e., the term 𝐸𝑃 (R𝑓 ) [log 𝑃 (R𝑔 | R𝑡)]) and then to transmit the information from 𝑃 (R𝑓 ) to 𝑃 (R𝑡) via the term 𝐾𝐿[𝑃 (R𝑓 ) ∥𝑃 (R𝑡)]. Such a learning process is ineffective for learning the true user preference distribution 𝑃 (R𝑡) and the target recommender model 𝑡𝜃 . To overcome the above issue, according to Eq. 4, when the training process has converged, the preference distributions 𝑃 (R𝑓 ) and 𝑃 (R𝑡) would be close to each other. As a result, we can change the expectation over 𝑃 (R𝑓 ) to the expectation over 𝑃 (R𝑡) to learn 𝑃 (R𝑡) more effectively. So we modify the left side of Eq. 8 as

$$
\tag{9}
$$

Similarly, if we substitute the middle part of Eq. 7 into Eq. 6 and perform similar derivations, we can obtain:

$$
\tag{10}
$$

The left side of Eq. 10 is an approximate lower bound of log 𝑃 (R𝑓 ). The bound is satisfied only if 𝑃 (R𝑔) perfectly recovers 𝑃 (R𝑡 | R𝑓 ), which means 𝑃 (R𝑔) trained on the observed auxiliary behaviors can perfectly approximate the true user preference distribution captured from the target behavior data. Such condition further verifies the soundness of MBA, i.e., multiple types of user behavior are motivated by similar underlying user preferences. Combining the left side of both Eq. 9 and Eq. 10 we obtain the loss function as:

$$
\tag{11}
$$

We can see that the loss function aims to maximize the likelihood of data observation (i.e., 𝑃 (R𝑔 | R𝑡) and 𝑃 (R𝑓 | R𝑡)) and minimize the KL-divergence between distributions learned from different user behavior data. The learning process of MBA serves as a filter to simultaneously denoise multiple types of user behavior and conduct beneficial knowledge transfers to infer the true user preferences to enhance the prediction of the target behavior.

## Training details

As described in Section 3.1, we learn the user preference distributions 𝑃 (R𝑓 ) and 𝑃 (R𝑔) from R𝑓 and R𝑔, respectively. In order to enhance the learning stability, we pre-train 𝑃 (R𝑓 ) and 𝑃 (R𝑔) in R𝑓 and R𝑔, respectively. We use the same model structures of our target recommender 𝑡𝜃 as the pre-training model. As the training converges, the KL-divergence will gradually approach 0. In order to enhance the role of the KL-divergence in conveying information, we set a hyperparameter 𝛼 to enhance the effectiveness of the KL-divergence. Then we obtain the following training loss function:

$$
\tag{12}
$$

### Expectation derivation.

As described in Section 3.1, both R𝑓 and R𝑔 contain various kinds of noise and bias. In order to infer the latent true user preferences from the corrupted multi-behavior data, we use ℎ 𝑓 𝜙 (𝑢,𝑖) and ℎ 𝑓 𝜑 (𝑢,𝑖) to capture the correlations between the true user preferences and the observed purchase data. Similarly, ℎ 𝑔 𝜙′ (𝑢,𝑖) and ℎ 𝑔 𝜑′ (𝑢,𝑖) are used to capture the correlations between the true user preferences and the observed click data, as shown in Eq. 2. Specifically, we expand 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑔 | R𝑡)] as:

$$
\tag{13}
$$

Similarly, the term 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑓 | R𝑡)] can be expanded as:

$$
\tag{14}
$$

By aligning and denoising the observed target behavior and auxiliary behavior data simultaneously, the target recommender 𝑡𝜃 is trained to learn the universal true user preference distribution.

### Alternative model training.

In the learning stage, we find that directly training 𝑡𝜃 with Eq. 12–Eq. 14 does not yield satisfactory results, which is caused by the simultaneous update of five models (i.e., ℎ 𝑔 𝜙′ , ℎ 𝑔 𝜑′ , ℎ 𝑓 𝜙 , ℎ 𝑓 𝜑 and 𝑡𝜃 ) in such an optimization process. These five models may interfere with each other and prevent 𝑡𝜃 from learning well. To address this problem, we set two alternative training steps to train the involved models iteratively. In the first training step, we assume that a user tends to not click or purchase items that the user dislikes. That is to say, given 𝑟 𝑡 𝑢,𝑖 = 0 we have 𝑟 𝑓 𝑢,𝑖 ≈ 0 and 𝑟 𝑔 𝑢,𝑖 ≈ 0, so we have ℎ 𝑓 𝜙 ≈ 0 and ℎ 𝑔 𝜙′ ≈ 0 according to Eq. 2. Thus in this step, only the models ℎ 𝑓 𝜑 , ℎ 𝑔 𝜑′ and 𝑡𝜃 are trained. Then Eq. 13 can be reformulated as:

$$
\tag{15}
$$

where

$$
\tag{}
$$

Meanwhile, Eq. 14 can be reformulated as:

$$
\tag{16}
$$

where

$$
\tag{}
$$

Here, we denote 𝐶1 as a large positive hyperparameter to replace − logℎ 𝑔 𝜙′ (𝑢,𝑖) and − logℎ 𝑓 𝜙 (𝑢,𝑖). In the second training step, we assume that a user tends to click and purchase the items that the user likes. That is to say, given 𝑟 𝑡 𝑢,𝑖 = 1 we have 𝑟 𝑓 𝑢,𝑖 ≈ 1 and 𝑟 𝑔 𝑢,𝑖 ≈ 1, so we have ℎ 𝑓 𝜑 ≈ 1 and ℎ 𝑔 𝜑′ ≈ 1 according to Eq. 2. Thus in this step, only the models ℎ 𝑓 𝜙 , ℎ 𝑔 𝜙′ and 𝑡𝜃 will be updated. Then Eq. 13 can be reformulated as:

$$
\tag{17}
$$

where

$$
\tag{}
$$

Eq. 14 can be reformulated as:

$$
\tag{18}
$$

where

$$
\tag{}
$$

𝐶2 is a large positive hyperparameter to replace − log(1−ℎ 𝑔 𝜑′ (𝑢,𝑖)) and − log(1 − ℎ 𝑓 𝜑 (𝑢,𝑖)).

### Training procedure.

In order to facilitate the description of sampling and training process, we divide 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑔 | R𝑡)] and 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑓 | R𝑡)] into four parts (see Eq. 15 to Eq. 18), namely click positive loss (𝐿𝐶𝑃 and 𝐿 ′ 𝐶𝑃 ), click negative loss (𝐿𝐶𝑁 and 𝐿 ′ 𝐶𝑁 ), purchase positive loss (𝐿𝑃𝑃 and 𝐿 ′ 𝑃𝑃 ), and purchase negative loss (𝐿𝑃𝑁 and 𝐿 ′ 𝑃𝑁 ). Each sample in the training set can be categorized into one of three situations: (i) clicked and purchased, (ii) clicked but not purchased, and (iii) not clicked and not purchased. The three situations involve different terms in 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑔 | R𝑡)] and 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑓 | R𝑡)]. In situation (i), each sample involves the 𝐿𝐶𝑃 and 𝐿𝑃𝑃 (or 𝐿 ′ 𝐶𝑃 and 𝐿 ′ 𝑃𝑃 in the alternative training step). In situation (ii), each sample involves the 𝐿𝐶𝑃 and 𝐿𝑃𝑁 (or 𝐿 ′ 𝐶𝑃 and 𝐿 ′ 𝑃𝑁 in the alternative training step). In situation (iii), each sample involves the 𝐿𝐶𝑁 and 𝐿𝑃𝑁 (or 𝐿 ′ 𝐶𝑁 and 𝐿 ′ 𝑃𝑁 in the alternative training step). We then train MBA according to the observed multiple types of user behavior data in situations (i) and (ii), and use the samples in situation (iii) as our negative samples. Details of the training process for MBA are provided in Algorithm 1.

# Experimental settings

## Experimental questions

Our experiments are conducted to answer the following research questions: (RQ1) How do the proposed methods perform compared with state-of-the-art recommendation baselines on different datasets? (RQ2) How do the proposed methods perform compared with other denoising frameworks? (RQ3) Can MBA help to learn universal user preferences from users’ multiple types of behavior? (RQ4) How do the components and the hyperparameter settings affect the recommendation performance of MBA?

## Datasets

To evaluate the effectiveness of our method, we conduct a series of experiments on three real-world benchmark datasets, including Beibei1 [12], Taobao2 [47], and MBD (multi-behavior dataset), a dataset we collected from an operational e-commerce platform. The details are as follows: (i) The Beibei dataset is an open dataset collected from Beibei, the largest infant product e-commerce platform in China, which includes three types of behavior, click, add-to-cart and purchase. This work uses two kinds of behavioral data, clicks and purchases. (ii) The Taobao dataset is an open dataset collected from Taobao, the largest e-commerce platform in China, which includes three types of behavior, click, add to cart and purchase. In this work, we use clicks and purchases of this dataset. (iii) The MBD dataset is collected from an operational e-commerce platform, and includes two types of behavior, click and purchase. For each dataset, we ensure that users have interactions on both types of behavior, and we set click data as auxiliary behavior data and purchase data as target behavior data. Table 1 shows the statistics of our datasets

## Evaluation protocols

We divide the datasets into training and test sets with a ratio of 4:1. We adopt two widely used metrics Recall@𝑘 and NDCG@𝑘. Recall@𝑘 represents the coverage of true positive items that appear in the final top-𝑘 ranked list. NDCG@𝑘 measures the ranking quality of the final recommended items. In our experiments, we use the setting of 𝑘 = 10, 20. For our method and the baselines, the reported results are the average values over all users. For every result, we conduct the experiments three times and report the average values.

## Baselines

To demonstrate the effectiveness of our method, we compare MBA with several state-of-the-art methods. The methods used for comparison include single-behavior models, multi-behavior models, and recommendation denoising methods. The single-behavior models that we consider are: (i) MF-BPR [28], which uses bayesian personalized ranking (BPR) loss to optimize matrix factorization. (ii) NGCF [34], which encodes collaborative signals into the embedding process through multiple graph convolutional layers and models higher-order connectivity in user-item graphs. (iii) LightGCN [15], which simplifies graph convolution by removing the matrix transformation and non-linear activation. We use the BPR loss to optimize LightGCN. The multi-behavior models that we consider are: (i) MB-GCN [18], which constructs a multi-behavior heterogeneous graph and uses GCN to perform behavior-aware embedding propagation. (ii) MB- GMN [39], which incorporates multi-behavior pattern modeling with the meta-learning paradigm. (iii) CML [37], which uses a new multi-behavior contrastive learning paradigm to capture the transferable user-item relationships from multi-behavior data. To verify that the proposed method improves performance by denoising implicit feedback, we also introduce the following denoising frameworks: (i) WBPR [11], which is a re-sampling-based method which considers popular, but un-interacted items are highly likely to be negative. (ii) T-CE [32], which is a re-weighting based method which discards the large-loss samples with a dynamic threshold in each iteration. (iii) DeCA [35], which is a newly proposed denoising method that utilizes the agreement predictions on clean examples across different models and minimizes the KL-divergence between the real user preference parameterized by two recommendation models. (iv) SGDL [13], which is a new denoising paradigm that utilizes self-labeled memorized data as denoising signals to improve the robustness of recommendation models.

## Implementation details

We implement our method with PyTorch.3 Without special mention, we set MF as our base model 𝑡𝜃 since MF is still one of the best models for capturing user preferences for recommendations [29]. The model is optimized by Adam [20] optimizer with a learning rate of 0.001, where the batch size is set as 2048. The embedding size is set to 32. The hyperparameters 𝛼, 𝐶1 and 𝐶2 are search from { 1, 10, 100, 1000 }. 𝛽 is search from { 0.7, 0.8, 1 }. To avoid over-fitting, 𝐿2 normalization is searched in { 10−6 , 10−5 , . . . , 1 }. Each training step is formed by one interacted example, and one randomly sampled negative example for efficient computation. We use Recall@20 on the test set for early stopping if the value does not increase after 20 epochs. For the hyperparameters of all recommendation baselines, we use the values suggested by the original papers with carefully finetuning on the three datasets. For all graph-based methods, the number of graph-based message propagation layers is fixed at 3.

# Experimental Results

## Performance comparison (RQ1)

To answer RQ1, we conduct experiments on the Beibei, Taobao and MBD datasets. The performance comparisons are reported in Table 2. From the table, we have the following observations. First, the proposed MBA method achieves the best performance and consistently outperforms all baselines across all datasets. For instance, the average improvement of MBA over the strongest baseline is approximately 6.3% on the Beibei dataset, 6.6% on the Taobao dataset and 1.5% on the MBD dataset. These improvements demonstrate the effectiveness of MBA. We contribute the significant performance improvement to the following two reasons: (i) we align the user preferences based on two types of two behavior, transferring useful information from the auxiliary behavior data to enhance the performance of the target behavior predictions; (ii) noisy interactions are reduced through preference alignment, which helps to improve the learning of the latent universal true user preferences. Second, except CML the multi-behavior models outperform the single-behavior models by a large margin. This reflects the fact that adding auxiliary behavior information can improve the recommendation performance of the target behavior. We conjecture that CML cannot achieve satisfactory performance because it incorporates the knowledge contained in auxiliary behavior through contrastive meta-learning, which introduces more noisy signals. Furthermore, we compare MBA with the best single-behavior model (NGCF on the Beibei and MBD datasets, LightGCN on the Taobao dataset), and see that MBA achieves an average improvement of 12.4% on the Beibei dataset, 26.8% on the Taobao dataset and 15.3% on the MBD dataset. To conclude, the proposed MBA approach consistently and significantly outperforms related single-behavior and multi-behavior recommendation baselines on the purchase prediction task.

## Denoising (RQ2)

Table 3 reports on a performance comparison with existing denoising frameworks on the Beibei, Taobao and MBD datasets. The results demonstrate that MBA can provide more robust recommendations and improve overall performance than competing approaches. Most of the denoising baselines do not obtain satisfactory results, even after carefully tuning their hyperparameters. Only WBPR can outperform normal training in some cases. However, MBA consistently outperforms normal training and other denoising frameworks. We think the reasons for this are as follows: (i) In MBA, we use the alignment between multi-behavior data as the denoising signal and then transmit information from the multi-behavior distribution to the latent universal true user preference distribution. This learning process facilitates knowledge transfer across multiple types of user behavior and filters out noisy signals. (ii) In the original papers of the compared denoising baselines, testing is conducted based on explicit user-item ratings. However, our method does not use any explicit information like ratings, only implicit interaction data is considered. To further explore the generalization capability of MBA, we also adopt LightGCN as our base model (i.e., using LightGCN as𝑡𝜃 ). The results are also shown in Table 3. We see that MBA is still more effective than the baseline methods. We find that LightGCN-based MBA does not perform as well as MF-based MBA on the Beibei and Taobao datasets. We think the possible reasons are as follows: (i) LightGCN is more complex than MF, making MBA more difficult to train; (ii) LightGCN may be more sensitive to noisy signals due to the aggregation of neighbourhoods, resulting in a decline in the MBA performance compared to using MF as the base model. To conclude, the proposed MBA can generate more accurate recommendation compared with existing denoising frameworks.

## User preferences visualization (RQ3)

To answer RQ3, we visualize the distribution of users’ interacted items. We select two users in the Beibei, Taobao and MBD datasets and draw their behavior distributions using the parameters obtained from an MF model trained on the purchase behavior data and the parameters obtained from MBA, respectively. Figure 2 visualizes the results. From the figure, we observe that for one user, the clicked items and purchased items distributions of MBA stay much closer than that of MF. The observation indicates that MBA can successfully align multiple types of user behavior and infer universal and accurate user preferences. Besides, we see that different users in MBA have more obvious separations than users in MF, which implies that MBA provides more personalized user-specific recommendation than MF.

## Model investigation (RQ4)

5.4.1 Ablation study. Regarding RQ4, we conduct an ablation study (see Table 4) on the following two settings: (i) MBA-KL: we remove KL-divergence when training MBA; and (ii) MBA-PT: we co-train the 𝑃 (R𝑓 ) and 𝑃 (R𝑔) in MBA instead of pre-training. The results show that both parts (KL-divergence and pre-trained models) are essential to MBA because removing either will lead to a performance decrease. Without KL-divergence, we see the performance drops substantially in terms of all metrics. Hence, the KL-divergence helps align the user preferences learned from different behaviors, thus improving the recommendation performance. Without pre-trained models, the results drop dramatically, especially in the Taobao dataset, which indicates that it is hard to cotrain 𝑃 (R𝑓 ) and 𝑃 (R𝑔) with MBA. Using a pre-trained model can reduce MBA’s complexity and provide prior knowledge so that it can more effectively extract the user’s real preferences from the different types of behavior distributions. 5.4.2 Hyperparameter study. Next, we conduct experiments to examine the effect of different parameter settings on MBA. Figure 3 shows the effect of 𝛼, which is used to control the weight of the KL-divergence in conveying information. On the Beibei dataset, the performance of MBA is affected when the 𝛼 is greater than or equal to 100. Thus, when dominated by KL-divergence, MBA’s performance will be close to that of the pre-trained models. On the Taobao and MBD datasets, when 𝛼 is greater than or equal to 100, MBA will gradually converge, with a relatively balanced state between the KL-divergence and the expectation term. Under this setting, MBA achieves the best performance.

# Conclusion

In this work, we have focused on the task of multi-behavior recommendation. We conjectured that multiple types of behavior from the same user reflect similar underlying user preferences. To tackle the challenges of the gap between data distributions of different types of behavior and the challenge of behavioral data being noisy and biased, we proposed a learning framework, namely multi-behavior alignment (MBA), which can infer universal user preferences from multiple types of observed behavioral data, while performing data denoising to achieve beneficial knowledge transfer. Extensive experiments conducted on three real-world datasets showed the effectiveness of the proposed method. Our method proves the value of mining the universal user preferences from multi-behavior data for the implicit feedback-based recommendation. However, a limitation of MBA is that it can only align between two types of behavioral data. As to our future work, we aim to perform alignment on more types of user behavior. In addition, we plan to develop ways of conducting more effective and efficient model training.
