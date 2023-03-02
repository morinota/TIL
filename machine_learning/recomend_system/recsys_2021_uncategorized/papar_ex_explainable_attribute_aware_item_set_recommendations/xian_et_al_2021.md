## link

- https://assets.amazon.science/d3/ad/9af131bd49b8a0697c6bd763a1cf/ex3-explainable-attribute-aware-item-set-recommendations.pdf
- https://www.wantedly.com/companies/wantedly/post_articles/350652

## title

EX3 : Explainable Attribute-aware Item-set Recommendations

## abstract

Existing recommender systems in the e-commerce domain primarily focus on generating a set of relevant items as recommendations; however, few existing systems utilize underlying item attributes as a key organizing principle in presenting recommendations to users. Mining important attributes of items from customer perspectives and presenting them along with item sets as recommendations can provide users more explainability and help them make better purchase decision. In this work, we generalize the attribute-aware item-set recommendation problem, and develop a new approach to generate sets of items (recommendations) with corresponding important attributes (explanations) that can best justify why the items are recommended to users. In particular, we propose a system that learns important attributes from historical user behavior to derive item set recommendations, so that an organized view of recommendations and their attribute-driven explanations can help users more easily understand how the recommendations relate to their preferences. Our approach is geared towards real world scenarios: we expect a solution to be scalable to billions of items, and be able to learn item and attribute relevance automatically from user behavior without human annotations. To this end, we propose a multi-step learning-based framework called Extract-Expect-Explain (EX3 ), which is able to adaptively select recommended items and important attributes for users. We experiment on a large-scale real-world benchmark and the results show that our model outperforms state-of-the-art baselines by an 11.35% increase on NDCG with adaptive explainability for item set recommendation.

# Introduction

Recommender systems have been widely deployed in modern e-commerce websites, helping users overcome overwhelming selection issues in large catalogs and contributing large business impact [9, 20, 32]. Many existing recommender systems in industry focus on generating a set of relevant items based on a set of pivot/query items along with metadata such as item attributes. However, few of them utilize the underlying item attributes as a way to explain why the items are recommended to users. Without distinguishing attributes, recommendations can often be overlooked by users who are unfamiliar with the items [23], especially when they have to click into corresponding detail pages to find more in-depth information. In this work, we generalize the attribute-aware item-set recommendation problem [3, 4, 10, 28], which aims to generate exact-𝐾 sets of recommended items along with attribute-driven explanations to help users quickly locate the items of interest according to objective item properties (brand, color, size, etc) and subjective user feedback (ratings). In particular, we propose a method to learn behavior-oriented attribute importance from historical user actions, a technique which can be applied to other use cases beyond explainable recommendations including query rewriting [25] and review summarization [40].

Throughout the paper, we study the explainable attribute-aware item-set recommendation problem by learning an item-to-item-set mapping guided by attribute differences. Formally, given a “pivot” item, our goal is to generate 𝐾 sets of items (recommendations), each of which is associated with an important attribute (explanation) to justify why the items are recommended to users. We aim to not only generate relevant item recommendations, but also provide corresponding explanations based on those important item attributes whose value changes will affect user purchase decision. Unlike existing work [3] that focuses primarily on making understandable substitute recommendations, we attempt to help users broaden their consideration set by presenting them with differentiated options by attribute type. Additionally, different from generating explanations based on user–item and item–attribute interactions [3], we propose to infer important attributes directly from users’ historical behaviors, providing a framework to understand how users reason about recommendations when making decisions. To the best of our knowledge, we are the first to approach the explainable item-set recommendations via behavior-oriented important attribute identification in e-commerce domain.

The main idea in solving this problem is to first learn important attributes based on users’ historical behaviors, and then generate corresponding item recommendations. Note that learning important attributes can benefit many other applications beyond item-set recommendations alone. Modeling behavior-oriented attribute importance from users’ historical actions rather than manual identification is a critical component to conduct explainable recommendations. It saves time-consuming effort in manual labeling and provides a more robust way to model user preference. Once important attributes are derived, we can utilize them to build user profiles, e.g., identifying users’ preferred size, color, flavor, etc, which can be used in generating personalized recommendations. We can also perform brief item summarization based on important attributes, and the proposed method can also be easily extended to involve more contextual information (e.g., users’ sequential actions) to provide customized item summarization [40]. We can further leverage the behavior-driven important attributes to advance query rewriting techniques in the item search domain, by attending to those terms that are closely related to items’ important attributes.

To this end, we propose a multi-step framework called Extract-Expect-Explain (EX3 ) to approach the explainable item-set recommendation problem. Our EX3 framework takes as input a pivot/query item and a list of candidate items as well as their catalog features (e.g., title, item type), and adaptively outputs sets of recommended items associated with important attributes as explanations. Specifically, in the first Extract-step, we introduce an attention-based item embedding learning framework, which is scalable to generating embeddings for billions of items, and can be leveraged to refine coarse-grained candidate items for a given pivot item. Then, in the Expect-step, we propose an AttributeDifferentiating Network to learn the expected utility score on the tuples of {query item, candidate item, attribute} to indicate how the difference on attribute values between query item and candidate item affects users’ purchase decision. The goal of this step is to learn attribute importance based on the impact of value changes towards user purchase behavior. For instance, if we observe that value changes of “shoe size” affected more user purchase decisions than color changes, the Expect-step is more likely to predict higher utility score on {query shoe, candidate shoe, size} than {query shoe, candidate shoe, color}. Given the refined candidate items and the estimated utility scores, we propose a bipartite b-Matching-based algorithm in the Explain-step to balance the relevance and behavior-driven attribute importance to deliver the final results for item-set recommendation. Such a multi-step framework design provides the flexibility to serve the explainable attribute-aware item-set recommendation and other relevant applications.

To guarantee the robustness and scalability in real world environment, EX3 is carefully designed to overcome several inherent challenges. (1) The foremost challenge is how to dynamically recommend items and attributes that provide comprehensive information contributed to users’ purchase decision. In this work, we propose to train EX3 with user behavior signals in the distant supervision manner, and leverage attribute value difference and historical purchase signals to capture user-behavior driven important attributes. We believe that the important attributes are those whose value changes will critically affect users’ purchase decision, e.g., size for shoes, roast type for coffee. (2) In real-world environment, we are always facing data challenges, especially on the attribute missing/sparsity issues. To have a robust performance even when attribute coverage is poor, we develop a robust attention mechanism called Random-masking Attention Block in Expect-step to bound the softmax output based on prior attribute coverage information. (3) Scaling EX3 to millions of different items is also challenging. To ensure EX3 to be generalized to multiple item types and large-scale items, we introduce a highly-scalable item embedding framework in Extract-step, design an attribute-driven attention mechanism in Expect-step to directly learn attribute importance from user behavior without human labeling, and propose a constrained bipartite b-Matching algorithm in Explain-step that can be easily parallelized to generate top items and important attributes for explainable item-set recommendation. The contributions of this paper are three-fold.

- We highlight the importance of jointly considering important attributes and relevant items in achieving the optimal user experience in explainable recommendations.
- We propose a novel three-step framework, EX3 , to approach the explainable attribute-aware item-set recommendation problem along with couples of novel components. The whole framework is carefully designed towards large-scale real-world scenario.
- We extensively conduct experiments on the real-world benchmark for item-set recommendations. The results show that EX3 achieves 11.35% better NDCG than state-of-the-art baselines, as well as better explainability in terms of important attribute ranking.

# Preliminary

In this section, we start with the introduction of relevant concepts and formulation of the explainable attribute-aware item-set recommendation problem. Then, we introduce how to approach this problem via distant supervision.

## Problem Formulation.

Let P be the universal set of items and A be the set of all available attributes. We define the attribute value to be a function 𝑣 : P × A ↦→ C𝑑𝑣 that maps an item and an attribute to a sequence of characters, where C denotes a set of predefined characters and 𝑑𝑣 is the maximum length of the sequence.1 An item 𝑝 ∈ P is said to have value 𝑣(𝑝, 𝑎) on attribute 𝑎 ∈ A if 𝑣(𝑝, 𝑎) ≠ ∅. Accordingly, the attribute-value pairs of an item 𝑝 on multiple attributes are defined as 𝐴𝑝 = {(𝑎1, 𝑣1), . . . , (𝑎|𝐴𝑝 | , 𝑣|𝐴𝑝 | ) | 𝑎𝑖 ∈ A, 𝑣𝑖 = 𝑣(𝑝, 𝑎𝑖), 𝑣𝑖 ≠ ∅,𝑖 = 1, . . . , |𝐴𝑝 |}. In addition, we define an explainable group 𝐺𝑎 = (𝑎, 𝑃𝑎) to be a tuple of an attribute 𝑎 ∈ A and a subset of items 𝑃𝑎 ⊂ P and each item in 𝑃𝑎 has non-empty value on attribute 𝑎. The item set 𝑃𝑎 is assumed for recommendation and the attribute 𝑎 is used to generate the explanation. The problem of explainable attribute-aware item-set recommendation can be formalized as follows.

Definition 1 (Problem Definition). Given the pivot item 𝑞 ∈ P with attribute-value pairs 𝐴𝑞, and the number of groups, 𝐾, the goal is to output 𝐾 ordered explainable groups 𝐺𝑎(1) , . . . ,𝐺𝑎(𝐾) such that the user utility (e.g., purchase) of displaying 𝐾 such groups is maximized.

Intuitively, the goal of the problem is to recommend 𝐾 groups of items with attributes such that the likelihood of these recommended items being clicked or purchased is maximized after users compare them with the pivot item and view the displayed attribute-based justifications. In other words, it is required to generate important attributes given different pivot and candidate items so that they are useful to users, e.g., “screen resolution” is relatively more important than “height” for a TV item. Note that the explainable item set recommendation can be considered to be a item-to-item-set recommendation problem in e-commerce shopping scenario, and we assume user context information is not available in this work. The challenges of this problem are threefold.

- How to automatically identify important attributes without supervision and aggregate relevant items into the corresponding groups for recommendation?
- How to make the model robust to the data issues including missing attributes and noisy and arbitrary values?
- How to effectively reduce the search space of seeking similar items for item set recommendation and make the model scalable to large real-world dataset?

## Distant Supervision.

In order to capture the comparable relationship among various items, we consider three common user behavior signals to construct datasets to provide distant supervision [11, 20, 30]: co-purchase (Bcp), co-view (Bcv) and purchase-after-view (Bpv) between items, where Bcp, Bcv, Bpv ⊆ P × P denote how items are co-purchased, co-viewed and view-then-purchased together. From the above definition, one can notice that Bpv offers an opportunity to simulate users’ shopping behaviors. When users view an item and then purchase another one in a short period of time (e.g., within the same session), it is reasonable to assume that users are making comparison between relevant items. Through empirical analysis on Amazon Mechanical Turk (MTurk), we observe that item pairs within Bpv have more than 80% similarities, which verifies our assumption that users are comparing similar items before purchase. In order to further improve the relevance from raw behavior signals to build up distant supervision with high quality, by further combing Bcp and Bcv, we conduct several annotation experiments via MTurk and observe that B = Bcv ∩ Bpv − Bcp, which contains items pairs in both Bcv and Bpv but not in Bcp, gives us the best relevance signals and mimics users’ shopping actions on Bpv. Throughout the paper, we will use this way to construct datasets for model learning and offline evaluation on multiple item categories.

# Proposed Method

In this section, we first formulate an optimization-based method for the explainable attribute-aware item-set recommendation problem and pose several potential issues of this solution in industrial scenario. Then, we propose a novel learning-based framework called Extract-Expect-Explain (EX3 ) as a feasible and scalable alternative. 

An Optimization-based Method. 
Suppose we have a utility function 𝑢(𝑞, 𝑝, 𝑎) that estimates how likely users will click (or purchase) a recommended item 𝑝 ∈ P after comparing it with the pivot item 𝑞 ∈ P on attribute 𝑎 ∈ A, i.e., 𝑢 : P × P × A ↦→ [0, 1]. We can formulate an optimization problem for explainable item set recommendation as follows. Given a pivot item 𝑞, 𝑚 candidate items {𝑝1, . . . , 𝑝𝑚} ⊆ P and 𝑛 attributes {𝑎1, . . . , 𝑎𝑛} ⊆ A, we aim to find an assignment 𝑋 ∈ {0, 1} 𝑚×𝑛 that maximizes the overall utilities subject to some constraints:

$$
\tag{1}
$$

where 𝑋𝑖𝑗 = 1 means the item 𝑝𝑖 is assigned to the explainable group 𝐺𝑎𝑗 with attribute 𝑎𝑗 , and otherwise 𝑋𝑖𝑗 = 0. The group capacity constraint restricts the max number of items assigned in each group with an upperbound 𝐷grp ∈ N, while the item diversity constraint limits the occurrence of each item in overall recommendations with upperbound 𝐷div ∈ N. The problem defined in Eq. 1 can be deemed as the weighted bipartite b-matching problem [22], which can be solved by modern LP solvers. Once the 𝑛 sets of item assignments are derived from 𝑋, we can easily select top-𝐾 groups with any heuristic method based on group-level utility, e.g., the average of all item-attribute utilities in the group. 

However, there are two major issues with this method. First, the optimization in Eq. 1 cannot be efficiently solved when 𝑚 is very large and let alone take all items in P as input. Second, the utility 𝑢(𝑞, 𝑝, 𝑎) is not directly available from distant user behavior signal (e.g. view-then-purchase) because users will not explicitly express which attributes are important to them to compare the items. Meanwhile, attribute frequency is also not a good indicator for 𝑢(𝑞, 𝑝, 𝑎) due to the common data issue of large amount of missing attribute values. 

To this end, we propose a learning based multi-step framework called Extract-Expect-Explain (EX3 ). As illustrated in Fig. 1, the first Extract step aims to reduce the search space of candidate items by learning item embeddings with distant supervision and approximating coarse-grained item similarity. Next, the Expect step aims to estimate the utility function 𝑢(𝑞, 𝑝, 𝑎) by decomposing it into two parts: fine-grained item relevance and attribute importance. The last Explain step leverages the outputs from two previous steps to solve the optimization problem and derive the 𝐾 explainable groups for item set recommendations.

## Extract-Step

In this step, we aim to learn an item encoder 𝜙 : P ↦→ R 𝑑𝑝 that maps each item in P to 𝑑𝑝 -dimensional space such that the items with relationships in B are closer in the latent space. The latent item vectors generated by 𝜙 can be subsequently used as pretrained item embeddings in downstream steps and extracting coarse-grained similar candidates with respect to pivot items.


Specifically, each item 𝑝 ∈ P is initialized with either a one-hot vector or a raw feature vector extracted from metadata such as item title and category. Then, it is fed to the item encoder 𝜙, which is modeled as a multilayer perceptron (MLP) with non-linear activation function. In order to capture relatedness among items, we assume that each item is similar to its related items in B and is distinguishable from other unrelated items. As illustrated in Fig. 1(a), let 𝑁𝑝 = {𝑝𝑖 | (𝑝, 𝑝𝑖) ∈ B} be the related items for an item 𝑝 ∈ P. We define a metric function 𝑓 (𝑝, 𝑁𝑝 ) to measure the distance between the item and its related items:

$$
\tag{2}
$$

where 𝜆 is the base distance to distinguish 𝑝 and 𝑁𝑝 , and ℎ(·) denotes an aggregation function over item set 𝑁𝑝 , which encodes 𝑁𝑝 into the same 𝑑𝑝 -dimensional space as 𝜙 (𝑝). In this work, we define ℎ(·) to be a weighted sum over item embeddings via dot-product attention:

$$
\tag{3}
$$

We assign a positive label 𝑦 + = 1 for each pair of (𝑝, 𝑁𝑝 ). For non-trivial learning to distinguish item relatedness, for each item 𝑝, we also randomly sample |𝑁𝑝 | items from Bpv as negative samples denoted by 𝑁 − 𝑝 with assigned label 𝑦 − = −1. Therefore, the encoder 𝜙 can be trained by minimizing a hinge loss with the following objective function:

$$
\tag{4}
$$

where 𝜖 is the margin distance. 

Once the item encoder 𝜙 is trained, for each pivot item 𝑞 ∈ P, we can retrieve a set of 𝑚 (|𝑁𝑝 | ≪ 𝑚 ≪ |P |) coarse-grained related items as its candidate set 𝐶𝑞, i.e., 𝐶𝑞 = {𝑝𝑖 |rank (𝑓 (𝑞, {𝑞})) = 𝑖, 𝑝𝑖 ∈ P \ {𝑞},𝑖 ∈ [𝑚]}.


##  Expect-Step

The goal of this step is to learn the utility function 𝑢(𝑞, 𝑝, 𝑎) to estimate how likely a candidate item 𝑝 will be clicked or purchased by users after being compared with pivot item 𝑞 on attribute 𝑎. For simplicity of modeling, we assume that the utility function can be decomposed into two parts:

$$
\tag{5}
$$

where 𝑔 : [0, 1] × [0, 1] ↦→ [0, 1] is a binary operation. The first term 𝑢rel(𝑞, 𝑝) reveals the fine-grained item relevance, or equivalently, the likelihood of item 𝑝 being clicked by users after compared with pivot 𝑞 (no matter which attributes are considered). The second term 𝑢att(𝑎|𝑞, 𝑝) indicates the importance of displaying attribute 𝑎 to users when they compare items 𝑞 and 𝑝. It is natural to learn these two functions if well-curated datasets are available. However, practically, even though the item relevance can be simulated from distant user behavior signals, e.g., Bpv view-then-purchased, the groundtruth of important attributes still remain unknown. This is because users will not explicitly express the usefulness of item attributes when they do online shopping, which leads to the challenge of how to infer the attribute importance without supervision. In addition, the data issue of missing attributes and noisy values is quite common since it costs much time and effort to manually align all the attributes of items. That is to say each item may contain arbitrary number of attributes and their values may contain arbitrary content and data types. 

To overcome the issues, we propose a novel neural model named Attribute Differentiating Network (ADN) to jointly approximate 𝑢rel and 𝑢att. Formally, it takes as input a pivot item𝑞 and a candidate item 𝑝 along with the corresponding attribute-value pairs 𝐴𝑞, 𝐴𝑝 (e.g., 𝐴𝑞 = {(𝑎1, 𝑣(𝑞, 𝑎1)), . . . , (𝑎𝑛, 𝑣(𝑞, 𝑎𝑛))}), and simultaneously outputs an item relevance score 𝑌ˆ 𝑝 ∈ [0, 1] and attribute importance scores 𝑦ˆ𝑝,𝑗 ∈ [0, 1] for attribute 𝑎𝑗 (𝑗 = 1, . . . , 𝑛). 

### Network Overview. 

As illustrated in Fig. 2, ADN consists of three components: a value-difference module to capture the difference levels of attribute values of two items, an attention-based attribute scorer to implicitly predict the attribute contribution, and a relevance predictor that estimates the fine-grained relevance of two items. Specifically, two input items are first respectively vectorized by the encoder 𝜙 from the Extract step. The derived item embeddings are then mapped into low-dimensional space via linear transformation, i.e. x𝑞𝑝 = 𝑊𝑝 [𝜙 (𝑞);𝜙 (𝑝)], where [;] denotes the concatenation and 𝑊𝑝 is the learnable parameters. Then, each attribute-value tuple (𝑎𝑗 , 𝑣(𝑞, 𝑎𝑗), 𝑣(𝑝, 𝑎𝑗)) is encoded by the value-difference module into a vector denoted by x𝑣𝑗 . All these vectors x𝑣1 , . . . , x𝑣𝑛 together with x𝑞𝑝 will be further fed to the attention-based attribute scorer to produce attribute importance scores 𝑦ˆ𝑝,1, . . . ,𝑦ˆ𝑝,𝑛 as well as an aggregated vector z𝑣 about value-difference information on all attributes. The relevance predictor finally yields 𝑌ˆ 𝑝 based on the joint of x𝑞𝑝 and z𝑣 . 

### Value-Difference Module. 

As shown in Fig. 2(b), we represent each attribute 𝑎𝑗 as a one-hot vector and then embed it into 𝑑𝑎-dimensional space via linear transformation, i.e., a𝑗 = 𝑊𝑎𝑎𝑗 , with learnable parameters 𝑊𝑎. Since the value 𝑣(𝑝, 𝑎𝑗) of item 𝑝 and attribute 𝑎𝑗 can be of arbitrary type, inspired by character-level CNN, we treat it as a sequence of characters and each character is embedded into a 𝑑𝑐 -dimensional vector via linear transformation with parameters 𝑊𝑐 . Suppose the length of character sequence is at most 𝑛𝑐 . We can represent the value 𝑣(𝑝, 𝑎𝑗) as a matrix v𝑝 𝑗 ∈ R 𝑛𝑐×𝑑𝑐 . Then, we adopt convolutional layers to encode the character sequence as follows:

$$
\tag{6}
$$

where conv(·) denotes the 1D convolution layer and maxpool(·) is the 1D max pooling layer. The output x𝑖𝑗 ∈ R 𝑑𝑐 is the latent representation of arbitrary value 𝑣𝑖𝑗 . To capture value difference on attribute 𝑎𝑗 between items 𝑞, 𝑝, we further encode the attribute vector a𝑗 and the value vectors x𝑞𝑗 and x𝑝 𝑗 via an MLP:

$$
\tag{7}
$$

where x𝑣𝑗 is supposed to encode the value-difference information between values 𝑣(𝑞, 𝑎𝑗) and 𝑣(𝑝, 𝑎𝑗) on attribute 𝑎𝑗 .

### Attention-based Attribute Scorer. 

Since our goal is to detect important attributes with respect to the pair of items, we further entangle each value-difference vector x𝑣𝑗 of attribute 𝑎𝑗 conditioned on item vector x𝑞𝑝 as follows:

$$
\tag{8}
$$

where another MLP𝑝 is employed to generate the item-conditioned value-difference vector w𝑝 𝑗 .

Natually, we can use attention mechanism to aggregate 𝑛 item-conditioned attribute vectors w𝑝1, . . . , w𝑝𝑛 for better representation and automatic detection of important attributes. However, directly applying existing attention mechanism here will encounter several issues. First, the learned attention weights may have bias on frequent attributes. That is higher weights may not necessarily indicate attribute importance, but only because they are easily to acquire and hence occur frequently in datasets. Second, attribute cardinality varies from items to items due to the issue of missing attribute values, so model performance is not supposed to only rely on a single attribute, i.e. distributing large weight on one attribute. To this end, we propose the Random-masking Attention Block (RAB) to alleviate the issues. Specifically, given item vector x𝑞𝑝 and 𝑛 item-conditioned value-difference vectors w𝑝1, . . . , w𝑝𝑛, the RAB block is defined as follows.

$$
\tag{9}
$$

$$
\tag{10}
$$

$$
\tag{11}
$$

where 𝜂𝑗 is a random mask that has value 𝛾 with probability 𝑓 𝑟𝑒𝑞𝑗 (frequency of attribute 𝑎𝑗 ) in training and value 1 otherwise. It is used to alleviate the influence by imbalanced attribute frequencies. 𝜏𝑗 is known as the temperature in softmax and is set as (1 + 𝑓 𝑟𝑒𝑞𝑗) by default, which is used to shrink the attention on the attribute assigned with large weight. The RAB block can be regarded as a variant of the scaled dot-product attention by incorporating randomness of attribute frequencies and item-conditioned information. The attention weights {𝑦ˆ𝑝,𝑗 }𝑗 ∈ [𝑛] are used to approximate attribute importance 𝑢att(𝑎𝑗 |𝑞, 𝑝). The output z𝑣 encodes the aggregated information contributed by all attributes.

### Relevance Predictor. 

We adopt a linear classifier model to predict the relevance of two items based on the item vector as well as encoded attribute-value vector:

$$
\tag{12}
$$

We treat the problem as a binary classification with the objective function defined as follows:

$$
\tag{13}
$$
Note that pairwise ranking loss can also easily be extended here and the choice of a better ranking loss function is beyond the scope of this paper.

Once the model is trained, we can obtain the relevance score 𝑢rel(𝑞, 𝑝) ≈ 𝑌ˆ 𝑝 that implies whether candidate item 𝑝 is relevant to query item 𝑞, and the attribute importance score 𝑢att(𝑎𝑗 |𝑞, 𝑝) ≈ 𝑦ˆ𝑝,𝑗 (𝑗 = 1, . . . , 𝑛) indicating how important each attribute 𝑎𝑗 is to users when they compare items 𝑞 and 𝑝. We adopt a simple binary operation 𝑔(𝑢rel(𝑞, 𝑝), 𝑢att(𝑎𝑗 |𝑞, 𝑝)) ≈ 𝑌ˆ 𝑝 · 𝑦ˆ𝑝,𝑗 to estimate the utility value 𝑢(𝑞, 𝑝, 𝑎𝑗).

## Explain-Step 

In this step, the goal is to present 𝐾 explainable groups 𝐺𝑎(1) , . . . ,𝐺𝑎(𝐾) such that the whole utility is maximized. The complete inference algorithm is described in Alg. 1. Specifically, it first extracts a small subset of similar candidate items 𝐶𝑞 with respect to the pivot item 𝑞. For each pair of 𝑞 and 𝑝𝑖 ∈ C𝑞, it computes the relevance score of two items as well as the importance scores of attributes. Then, the LP problem defined in Eq. 1 is solved to obtain the assignments of candidate items on attribute-based groups. For each group, the algorithm takes the score from the most significant item as the heuristic score for group-level ranking. Finally, the top 𝐾 groups are generated as the recommendation with attribute-based explanations. Note that we adopt template-based generation approach to generate the natural language explanation based on attributes, which is not the focus in this paper.

## Implementation Detail 

In the Extract-step, the raw features of each item consist in n-gram features extracted from items’ titles, key words and categories. The feature extractor 𝜙 consists of 3 fully-connected layers of sizes 1024, 1024, 128 with ReLU [24] as nonlinear activation function. Margin parameters 𝜆 = 1.0 and 𝜖 = 1.0. The model is trained with Adam optimizer with learning rate 0.001 and batch size 128. 

In the Expect-step, the network parameters are as follows. 𝑊𝑝 ∈ R 256×64 , 𝑊𝑎 ∈ R |A |×64. We restrict maximum character sequence length to 𝑛𝑐 = 200 and the value of characters ranges from 0 – 255. The character embedding size 𝑑𝑐 = 64 with 𝑊𝑐 = R 255×64. Each convolution layer contains 64 filters is 64 and kernels of size 3. The multilayer perceptron MLP𝑣 consists of two fully-connected layers of sizes 172, 64 with ReLU as activation. The MLP𝑝 has two fully-connected layers of sizes 256, 64. In attention, 𝑊𝑞,𝑊𝑘 ,𝑊𝑣 ∈ R 64×64 and MLP𝑜 contains two fully-connected layers of sizes 64, 64. Masking value 𝜂 is set to 0.3 and the attribute frequency freq𝑗 is estimated from the training set. The linear predictor layer 𝑊𝑦 ∈ R 128×1 . The Expect model is trained with Adam optimizer with learning rate of 5 × 10−4 , weight decay 10−5 in total 20 epochs. All deep neural model are implemented in PyTorch and deployed based on Spark. 

In the Explain-step, we set both 𝐷grp and 𝐷att to be 5 by default. Candidate set size |𝐶𝑞 | = 30, |A| = 19 and 𝐾 = 5. The LP problem is solved by PuLP library2 .

# Experiments

In this section, we comprehensively evaluate the performance of the proposed method EX3 in terms of both recommendation and attribute ranking on a real-world benchmark.

## Experimental Setup

### Dataset. 

We take experiments on a real-world industrial dataset collected from Amazon.com including 7 subcategories: Battery, Coffee, Incontinence Protector, Laundry Detergent, Shampoo, Toilet Paper and Vitamin. Following distant supervision manner mentioned in Section 2, each subset can be regarded as an individual benchmark. To enable fast experiments, we randomly sample products from each product category and select their corresponding attributes to construct the datasets. The statistics of these datasets are summarized in Table 1. Similar metadata can also be found in [20, 21]. Due to the large-scale product pool, we generate candidate products for each query product via the proposed Extract-Step, which leads to around 30 similar candidate products per query. Our model and all the baselines are trained and evaluated based on the extracted candidates. We randomly split the dataset into training set (80%), validation set (10%) and test set (10%).

### Baselines & Metrics. 

We compare our method with following baselines. 

- Relevance is the method that computes item similarity based on item embeddings learned in Extract step. 
- BPR [26] is the Bayesian personalized ranking method for making recommendations, which is modified to item-to-item prediction in this work. 
- ACCM [27] is a CF-based and CB-based recommendation approach that leverages attribute to enrich the representation of items. We adapt this method to our item-to-item recommendation. 
- A2CF [3] is the state-of-the-art attribute-based recommendation model that outputs substitutes for pivot items. 
- EX3 is our approach proposed in Expect step. 

For fair comparison, we generate the a candidate set of 30 items for each pivot from the Extract step. All the baselines are evaluated based on the candidate set and also leverage the pretrained item embeddings as input if necessary. 

We adopt NDCG@10, Recall@10, Precision@10 as the metrics to evaluate the top-N recommendation performance.
 
## Top-N Recommendation Performance (Expect-Step)

In this experiment, we first evaluate the recommendation performance output by the Expect step, which produces the same results as traditional recommendations. Specifically, given a pivot item, both our method and all other baselines outputs top 10 recommendations from 30 candidates generated by Extract step. The goal of this experiment is to verify if our model can output more relevant items than others. 

The results are reported in Table 2. We observe that our model EX3 consistently outperforms all baselines across all datasets on all metrics. For instance, our model achieves NDCG of 0.8177, Recall of 0.9667 and Precision of 0.1953, which are higher than the results produced by the best baseline A2CF by a large margin. It is interesting to see that our model shows significant improvements on the item ranking performance, resulting at least 11.35% improvement in NDCG in Overall dataset and 10.36%–56.06% improvements across 7 subdomains. In addition, we notice that for datasets Coffee and Incontinence Protector, the recommendation performance of all models are better than the overall (average) performance. For example, our model achieves NDCG of 0.8716 and 0.8660 respectively, which are higher than Overall NDCG of 0.8177. Other models share similar trends. This indicates that the cases in these two datasets are easier to learn to capture user behavior.

##  Model Robustness to Missing Attributes

We further show our model is robust to missing attributes in inference data with the proposed masking attention. Specifically, we randomly drop 10%, 20%, 30%, 40% and 50% attributes in the test set and evaluate the top-N recommendation performance of our model with and without the proposed attention mechanism. All other settings remain the same. As shown in Fig. 3, our model w/ the technique (red curve) is consistently better than the baseline (blue curve) under different attribute dropping ratios in both NDCG and precision. In addition, we notice that the performance decrease of our model is slower than that of baseline, as the slope of the curve is smaller. This results imply that the proposed model is robust to the missing attributes during inference, which is essential in real-world scenarios.

## Attribute Ranking Performance (Explain-Step) 

### Effectiveness of Attribute Ranking. 

In this experiment, we evaluate the performance of the proposed Explain-Step in identifying important attributes. We specifically consider following three baselines. 

- Random is a simple grouping algorithm by randomly assigning items into attribute-based groups as long as the corresponding value exists. Then the groups are ordered in the way same as Alg. 1 (line 13–14). 
- Greedy is an iterative algorithm by always picking the pair of item and attribute with larger utility value 
- EX3 is our proposed method of the Explain-Step. 

Note that all compared methods differ in the grouping ways but take the same utility function as input, which is generated by the Expect-step for fair comparison. To quantify the attribute ranking performance, we randomly sample around 1000 cases and ask human evaluators to manually score each attribute in a 5-point scale given a pivot item and a set of candidate items. Then we can calculate the average and the normalized score of the predicted important attributes by each model. The results are reported in Table 3. 

We observe that our method EX3 gives the better performance in important attribute ranking compared with two baselines. One interesting fact is that the Greedy algorithm is actually an approximation algorithm for the optimization problem Eq. 1, which interprets that its performance is slightly worse than ours.

### Adaptive attribute ranking. 

In addition, we show that for the same pivot item, our model will rank attributes differently if the candidates are different. We showcase an example in Table 4 to demonstrate this characteristics of our model. Given a shampoo product with ID “B000YG1INI” as pivot item 3 , whose attributes are listed in the second column, we feed two sets of candidate items to our model that is able to generate two different attribute rankings as shown in the upper and lower parts of the table. It is interesting to see that the model is able to rank attributes based on value differences and diversity. Take “brand” attribute as example. In the first case (upper table), “brand” is ranked in the second place and considered as a relatively important attributes when users compare different shampoo products. In contrast, in the second case (lower table), “brand” is ranked lower because all the candidates have the same brand “Desert Essence” and it is less informative for users to enhance their shopping experience.

## Ablation Study 

We first show the recommendation performance under different masking ratios (𝜂) in the proposed attention mechanism. Specifically, we adopt different values of 𝜂 to train the model of Expect step, e.g. 𝜂 = 0, 0.1, . . . , 0.9, 1.0. Note that 𝜂 = 0 means the attribute is completely dropped while 𝜂 = 1 means there is no attribute dropping. We report the top-N recommendation performance under various 𝜂’s in Fig. 4 (a, b). We observe that the masking ratios influence on ranking performance (NDCG) and the model achieves the best performance when 𝜂 = 0.3. For precision, we find that the performance does not vary a lot, but still show similar trends as the NDCG, i.e. 𝜂 = 0.4 leads to the relatively better performance. 

Next, we evaluate the influence of different values of temperatures (𝜏) in the attention mechanism. Specifically, we experiment with two ways of imposing temperatures over softmax function. The first one relies on the predefined attribute frequencies, i.e. 𝜏 = (1 + 𝑓 𝑟𝑒𝑞𝑖) 𝑛 with 𝑛 = 1, 2. The other one uses the fixed value of 𝜏 = 1, 1.5, 2, 10. All other training settings remain the same. The results of top N recommendation are reported in Fig. 4 (c, d). We can see that the default choice of 𝜏 = 1 + 𝑓 𝑟𝑒𝑞𝑖 leads to the best performance in both NDCG and precision. Besides, note that when 𝜏 = 1, it is equivalent to the original softmax function. Our model with the default 𝜏 shows superior performance over such setup, which indicates the effectiveness of the proposed attention mechanism.

## Online Simulation and Experiments 

In this experiment, we evaluate the overall performance of the group-form explainable item set recommendation. Before serving the proposed method to real users, we generate a batch of explainable item set recommendations in an offline mode and leverage human annotators to help us evaluate the recommendation quality. For each of 7 product categories, we sample top 50 most popular pivot products from our recommendation dataset and ask the annotators to evaluate whether the attribute-based explainable recommendations can help users make better purchase decision. Note that the evaluation metric contains two-fold interactive measurement on both product relevance and attribute importance, as the ranked important attribute list should depend on what products are recommended to users. Through human evaluation, we obtain over 80% acceptance rate on high-quality item set recommendations with over 86% accuracy on comparable product recommendation performance, which is 2x higher than using raw Bpv data for recommendation. We also conduct online A/B testing through real user traffic on a large-scale e-commerce website, and the results show significant increase of conversion (+0.080%) and revenue (+0.105%) in online A/B experiments.

# Related Work

In this section, we discuss the related work regarding explainable recommendation and item relationship mining. 

## Explainable Recommendation. 

In the era of e-commerce, recommender systems have been widely used to provide users with relevant item suggestions. Most of existing methods are based on collaborative filtering [16], matrix factorization [17] and neural recommendation model [34]. Recently, to further improve user experience of recommender systems [18], great research efforts have been promoted to explainable recommendation problems [6, 7, 35]. One common way to generate explanation for recommendation is to leverage knowledge graphs [5, 15, 31, 33, 39]. For example, Xian et al. [32] propose to leverage reinforcement learning on knowledge graph to provide behavior-based explanation for product recommendations, while Zhao et al. [37] also employs reinforcement learning but propose a different demonstration-based knowledge graph reasoning framework for explainable recommendation. Besides knowledge graph, sentiment/opinion based explainable recommendation is also a popular research topic [2, 8]. Zhang et al. [36] integrate sentiment analysis into factorization model to improve explainable recommendation performance. Wang et al. [29] develop a multi-task learning solution for explainable recommendation, where two learning tasks on user preference modeling for recommendation and opinionated content modeling for explanation are joint learning via a shared tensor factorization framework. There are also research work around attribute-based explainable recommendation. Hou et al. [14] extract visual attributes from product images to conduct explainable fashion recommendation. Chen et al. [3] propose to leverage both user and item attributes to generate interpretable recommendations. Most of existing work focuses on explainable user-item recommendation problems but lack of the discussion on explainable item-to-item-set recommendation tasks, which is also important for e-commerce platforms. Moreover, explainable item-to-item-set recommendation problem is a harder case in explainable recommendation. Unlike explainable user-item recommendation problem where users and items do not always share same properties and thus allow more tolerance on generating explanations, in explainable item-to-item-set scenario, (1) we need to explicitly and rigorously provide reasonable attribute-based explanations between items since they always share same properties, e.g., display size for all TVs, and (2) the item set recommendations should balance both relevance and diversity on multiple item attributes.

## Item Relationship Mining. 

As our work is around item-to-item-set recommendation, we will also discuss existing work on item relationship mining. Identifying relationships among items is a fundamental component of many realworld recommender systems [20, 30]. Linden et al. [19] designs an item-to-item collaborative filtering to generate similar item recommendation for Amazon.com. Zhang et al. [38] discuss the impact of substitute and complement relationship between items on recommendations. Similar efforts [1, 12] have been put to target at explicitly modeling relationship between items for recommendations. Representative examples include Sceptre [20], which proposes a topic modeling method to infer networks of products, and PMSC [30], which incorporates path constraints in item pairwise relational modeling. He et al. [13] design a framework to use visual features to identify compatibility relationship between clothes and jewelry. These methods seek to distinguish substitutes, complements and compatibilities, but fail to provide any clear explanation on why these items are substitutable and comparable.

# Conclusion

In this work, we study the important problem of explainable attribute-aware item-set recommendation. We propose a multi-step learning-based framework called Extract-Expect-Explain (EX3 ) to approach the problem by first extracting coarse-grained candidate sets of items with respect to the pivot to reduce the search space of similar items (Extract-step), followed by a joint prediction of pairwise item relevance and attribute importance (Expect-step), which are subsequently fed to a constrained optimization solver to generate the group-form recommendations with explanations (Explain-step). The experiments are conducted on a real-world large-scale dataset and the results demonstrate that our proposed model achieves over 10% higher NDCG than state-of-the-art baselines in the explainable recommendation domain. Moreover, our proposed method can adaptively generate attribute-based explanations for various products, and the resulting explainable item-set recommendations are also shown to be effective in large-scale online experiments. There are several promising areas that we consider for future work, such as leveraging the learnt important attributes for query rewriting and product categorization.
