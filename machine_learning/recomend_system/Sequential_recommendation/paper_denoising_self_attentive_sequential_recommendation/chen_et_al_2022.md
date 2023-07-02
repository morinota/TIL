## 0.1. link

- https://dl.acm.org/doi/abs/10.1145/3523227.3546788
- https://arxiv.org/pdf/2212.04120.pdf

## 0.2. title

Denoising Self-Attentive Sequential Recommendation

## 0.3. abstract

Transformer-based sequential recommenders are very powerful for capturing both short-term and long-term sequential item dependencies. This is mainly attributed to their unique self-attention networks to exploit pairwise item-item interactions within the sequence. However, real-world item sequences are often noisy, which is particularly true for implicit feedback. For example, a large portion of clicks do not align well with user preferences, and many products end up with negative reviews or being returned. As such, the current user action only depends on a subset of items, not on the entire sequences. Many existing Transformer-based models use full attention distributions, which inevitably assign certain credits to irrelevant items. This may lead to sub-optimal performance if Transformers are not regularized properly.

Here we propose the Rec-denoiser model for better training of self-attentive recommender systems. In Rec-denoiser, we aim to adaptively prune noisy items that are unrelated to the next item prediction. To achieve this, we simply attach each self-attention layer with a trainable binary mask to prune noisy attentions, resulting in sparse and clean attention distributions. This largely purifies item-item dependencies and provides better model interpretability. In addition, the self-attention network is typically not Lipschitz continuous and is vulnerable to small perturbations. Jacobian regularization is further applied to the Transformer blocks to improve the robustness of Transformers for noisy sequences. Our Rec-denoiser is a general plugin that is compatible to many Transformers. Quantitative results on real-world datasets show that our Rec-denoiser outperforms the state-of-the-art baselines.

# 1. introduction

Sequential recommendation aims to recommend the next item based on a user’s historical actions [20, 35, 39, 44, 47], e.g., to recommend a bluetooth headphone after a user purchases a smart phone. Learning sequential user behaviors is, however, challenging since a user’s choices on items generally depend on both long-term and short-term preferences. Early Markov Chain models [19, 39] have been proposed to capture short-term item transitions by assuming that a user’s next decision is derived from a few preceding actions, while neglecting long-term preferences. To alleviate this limitation, many deep neural networks have been proposed to model the entire users’ sequences and achieve great success, including recurrent neural networks [20, 53] and convolutional neural networks [42, 54, 57].

Recently, Transformers have shown promising results in various tasks, such as machine translation [43]. One key component of Transformers is the self-attention network, which is capable of learning long-range dependencies by computing attention weights between each pair of objects in a sequence. Inspired by the success of Transformers, several self-attentive sequential recommenders have been proposed and achieve the state-of-the-art performance [26, 41, 49, 50]. For example, SASRec [26] is the pioneering framework to adopt self-attention network to learn the importance of items at different positions. BERT4Rec [41] further models the correlations of items from both left-to-right and right-to-left directions. SSE-PT [50] is a personalized Transformer model that provides better interpretability of engagement patterns by introducing user embeddings. LSAN [31] adopts a novel twin-attention sequential framework, which can capture both long-term and short-term user preference signals. Recently, Transformers4Rec [14] performs an empirical analysis with broad experiments of various Transformer architectures for the task of sequential recommendation.

Although encouraging performance has been achieved, the robustness of sequential recommenders is far less studied in the literature. Many real-world item sequences are naturally noisy, containing both true-positive and false-positive interactions [6, 45, 46]. For example, a large portion of clicks do not align well with user preferences, and many products end up with negative reviews or being returned. In addition, there is no any prior knowledge about how a user’s historical actions should be generated in online systems. Therefore, developing robust algorithms to defend noise is of great significance for sequential recommendation.

Clearly, not every item in a sequence is aligned well with user preferences, especially for implicit feedbacks (e.g., clicks, views, etc.) [8]. Unfortunately, the vanilla self-attention network is not Lipschitz continuous1 , and is vulnerable to the quality of input sequences [28]. Recently, in the tasks of language modeling, people found that a large amount of BERT’s attentions focus on less meaningful tokens, like "[SEP]" and ".", which leads to a misleading explanation [11]. It is thus likely to obtain sub-optimal performance if self-attention networks are not well regularized for noisy sequences. We use the following example to further explain above concerns.

Figure 1 illustrates an example of left-to-right sequential recommendation where a user’s sequence contains some noisy or irrelevant items. For example, a father may interchangeably purchase (phone, headphone, laptop) for his son, and (bag, pant) for his daughter, resulting in a sequence: (phone, bag, headphone, pant, laptop). In the setting of sequential recommendation, we intend to infer the next item, e.g., laptop, based on the user’s previous actions, e.g., (phone, bag, headphone, pant). However, the correlations among items are unclear, and intuitively pant and laptop are neither complementary nor compatible to each other, which makes the prediction untrustworthy. A trustworthy model should be able to only capture correlated items while ignoring these irrelevant items within sequences. Existing self-attentive sequential models (e.g., SASRec [26] and BERT4Rec [41]) are insufficient to address noisy items within sequences. The reason is that their full attention distributions are dense and would assign certain credits to all items, including irrelevant items. This causes a lack of focus and makes models less interpretable [10, 58].

To address the above issues, one straightforward strategy is to design sparse Transformer architectures that sparsify the connections in the attention layers, which have been actively investigated in language modeling tasks [10, 58]. Several representative models are Star Transformer [18], Sparse Transformer [10], Longformer [2], and BigBird [58]. These sparse attention patterns could mitigate noisy issues and avoid allocating credits to unrelated contents for the query of interest. However, these models largely rely on pre-defined attention schemas, which lacks flexibility and adaptability in practice. Unlike end-to-end training approaches, whether these sparse patterns could generalize well to sequential recommendation remains unknown and is still an open research question.

Fig. 1. An illustrative example of sequential recommendation where a sequence contains noisy or irrelevant items in left-to-right self-attention networks.

Contributions. In this work, we propose to design a denoising strategy, Rec-Denoiser, for better training of selfattentive sequential recommenders. Our idea stems from the recent findings that not all attentions are necessary and simply pruning redundant attentions could further improve the performance [10, 12, 40, 55, 58]. Rather than randomly dropping out attentions, we introduce differentiable masks to drop task-irrelevant attentions in the self-attention layers, which can yield exactly zero attention scores for noisy items. The introduced sparsity in the self-attention layers has several benefits: 1) Irrelevant attentions with parameterized masks can be learned to be dropped in a data-driven way. Taking Figure 1 as an example, our Rec-denoiser would prune the sequence (phone, bag, headphone) for pant, and (phone, bag, headphone, pant) for laptop in the attention maps. Namely, we seek next item prediction explicitly based on a subset of more informative items. 2) Our Rec-Denoiser still takes full advantage of Transformers as it does not change their architectures, but only the attention distributions. As such, Rec-Denoiser is easy to implement and is compatible to any Transformers, making them less complicated as well as improving their interpretability.

In our proposed Rec-Denoiser, there are two major challenges. First, the discreteness of binary masks (i.e., 0 is dropped while 1 is kept) is, however, intractable in the back-propagation. To remedy this issue, we relax the discrete variables with a continuous approximation through probabilistic reparameterization [25]. As such, our differentiable masks can be trained jointly with original Transformers in an end-to-end fashion. In addition, the scaled dot-product attention is not Lipschitz continuous and is thus vulnerable to input perturbations [28]. In this work, Jacobian regularization [21, 24] is further applied to the entire Transformer blocks, to improve the robustness of Transformers for noisy sequences. Experimental results on real-world benchmark datasets demonstrate the effectiveness and robustness of the proposed Rec-Denoiser. In summary, our contributions are:

- We introduce the idea of denoising item sequences for better of training self-attentive sequential recommenders, which greatly reduces the negative impacts of noisy items.
- We present a general Rec-Denoiser framework with differentiable masks that can achieve sparse attentions by dynamically pruning irrelevant information, leading to better model performance.
- We propose an unbiased gradient estimator to optimize the binary masks, and apply Jacobian regularization on the gradients of Transformer blocks to further improve its robustness.
- The experimental results demonstrate significant improvements that Rec-Denoiser brings to self-attentive recommenders (5.05% ∼ 19.55% performance gains), as well as its robustness against input perturbations.

# 2. Related Work

In this section, we briefly review the related work on sequential recommendation and sparse Transformers. We also highlight the differences between the existing efforts and ours.

## 2.1. Sequential Recommendation

Leveraging sequences of user-item interactions is crucial for sequential recommendation. User dynamics can be caught by Markov Chains for inferring the conditional probability of an item based on the previous items [19, 39]. More recently, growing efforts have been dedicated to deploying deep neural networks for sequential recommendation such as recurrent neural networks [20, 53], convolutional neural networks [42, 54, 57], memory networks [9, 22], and graph neural networks [4, 7, 51]. For example, GRU4Rec [20] employs a gated recurrent unit to study temporal behaviors of users. Caser [42] learns sequential patterns by using convolutional filters on local sequences. MANN [9] adopts memory-augmented neural networks to model user historical records. SR-GNN [51] converts session sequences into graphs and uses graph neural networks to capture complex item-item transitions.

Transformer-based models have shown promising potential in sequential recommendation [5, 26, 30, 32, 33, 41, 49, 50], due to their ability of modeling arbitrary dependencies in a sequence. For example, SASRec [26] first adopts self-attention network to learn the importance of items at different positions. In the follow-up studies, several Transformer variants have been designed for different scenarios by adding bidirectional attentions [41], time intervals [30], personalization [50], importance sampling [32], and sequence augmentation [33]. However, very few studies pay attention to the robustness of self-attentive recommender models. Typically, users’ sequences contain lots of irrelevant items since they may subsequently purchase a series of products with different purposes [45]. As such, the current user action only depends on a subset of items, not on the entire sequences. However, the self-attention module is known to be sensitive to noisy sequences [28], which may lead to sub-optimal generalization performance. In this paper, we aim to reap the benefits of Transformers while denoising the noisy item sequences by using learnable masks in an end-to-end fashion.

## 2.2. Sparce Transformer

Recently, many lightweight Transformers seek to achieve sparse attention maps since not all attentions carry important information in the self-attention layers [2, 10, 18, 29, 58]. For instance, Reformer [29] computes attentions based on locality-sensitive hashing, leading to lower memory consumption. Star Transformer [18] replaces the fully-connected structure of self-attention with a star-shape topology. Sparse Transformer [10] and Longformer [2] achieve sparsity by using various sparse patterns, such as diagonal sliding windows, dilated sliding windows, local and global sliding windows. BigBird [58] uses random and several fixed patterns to build sparse blocks. It has been shown that these sparse attentions can obtain the state-of-the-art performance and greatly reduce computational complexity. However, many of them rely on fixed attention schemas that lack flexibility and require tremendous engineering efforts.

Another line of work is to use learnable attention distributions [12, 36, 38, 40]. Mostly, they calculate attention weights with variants of sparsemax that replaces the softmax normalization in the self-attention networks. This allows to produce both sparse and bounded attentions, yielding a compact and interpretable set of alignments. Our Rec-denoiser is related to this line of work. Instead of using sparsemax, we design a trainable binary mask for the self-attention network. As a result, our proposed Rec-denoiser can automatically determine which self-attention connections should be deleted or kept in a data-driven way.

# 3. Problem and Background

In this section, we first formulate the problem of sequential recommendation, and then revisit several self-attentive models. We further discuss the limitations of the existing work.

## 3.1. Problem Setup

In sequential recommendation, let $U$ be a set of users, $I$ a set of items, and $S = {S^1, S^2,\cdots, S^{|U|}}$ a set of users' actions.
We user $S^u = (S^u_1, S^u_2, \cdots, S^u_{|S^u|})$ to denote a sequence of items for user $u \in U$ in a chronological order, where $S^u_t \in I$ is the item that user $u$ has interacted with at time $t$, and $|S^u|$ is the length of sequence.

Given the interaction history $S^u$, sequential recommendation seeks to predict the next item $S^u_{S^u+1}$ at time step $|S^u+1|$.
During the training process [26, 41], it will be convenient to regard the model’s input as $(S^u_1, S^u_2, \cdots, S^u_{|S^u - 1|})$ and its expected output is a shifted version of the input sequence: $(S^u_2, S^u_3, \cdots, S^u_{|S^u|})$.

## 3.2. Self-attenvive Recommenders

Owing to the ability of learning long sequences, Transformer architectures [43] have been widely used in sequential recommendation, like **SASRec** [26], BERT4Rec [41], and TiSASRec [30]. Here we briefly introduce the design of SASRec and discuss its limitations.

### 3.2.1. Embedding Layer

Transformer-based recommenders maintain an item embedding table $T \in R^{|I| \times d}$ , where 𝑑 is the size of the embedding. For each sequence $(S^u_1, S^u_2, \cdots, S^u_{|S^u - 1|})$, it can be converted into a fixed-length sequence $(s_1, s_2, \cdots s_n)$, where $n$ is the maximum length (e.g., keeping the most recent 𝑛 items by truncating or padding items). The embedding for $(s_1, s_2, \cdots s_n)$ is denoted as $E \in R^{n \times d}$ , which can be retrieved from the table $T$. To capture the impacts of different positions, one can inject a learnable positional embedding $P \in R^{n \times d}$ into the input embedding as:

$$
\hat{E} = E + P \tag{1}
$$

where $\hat{E} \in R^{n\times d}$ is an order-aware embedding, which can be directly fed to any Transformer-based models.

### 3.2.2. Transformer Block

A Transformer block consists of a self-attention layer and a point-wise feed-forward layer.
**Self-attention Layer**: The key component of Transformer block is the self-attention layer that is highly efficient to uncover sequential dependencies in a sequence [43]. The scaled dot-product attention is a popular attention kernel:

$$
\text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d}}) V
\tag{2}
$$

where $\text{Attention}(Q, K, V) \in R^{n \times d}$ is the output item representations; $Q = \hat{E}W^Q$, $K =\hat{E}W^K$, and $V = \hat{E}W^V$ are the queries, keys and values, respectively; ${W^Q, W^K, W^V} \in R^{d \times d}$ are three projection matrices; and $\sqrt{d}$ is the scale factor to produce a softer attention distribution. In sequential recommendation, one can utilize either left-to-right unidirectional attentions (e.g., SASRec [26] and TiSASRec [30]) or bidirectional attentions (e.g., BERT4Rec [41]) to predict the next item. Moreover, one can apply H attention functions in parallel to enhance expressiveness: $H <- \text{MultiHead}(\hat{E})$ [43].
**Point-wise Feed-forward Layer**: As the self attention layer is built on linear projections, we can endow the nonlinearity by introducing a point-wise feed-forward layers:

$$
F_i = FFN(H_i) = \text{ReLU}(H_i W^{(1)} + b^{(1)})W^{(2)} + b^{(2)}
\tag{3}
$$

where $W^{(*)} \in R^{d \times d}$, $b^{(*)} \in R^d$ are the learnable weights and bias.

In practice, it is usually beneficial to learn hierarchical item dependencies by stacking more Transformer blocks. Also, one can adopt the tricks of residual connection, dropout, and layer normalization for stabilizing and accelerating the training. Here we simply summarize the output of $L$ Transformer blocks as: $F^{(L)} <- \text{Transformer}(\hat{E})$.

### 3.2.3. Learning Objective

After stacked $L$ Transformer blocks, one can predict the next item (given the first $t$ items) based on $F_t^{(L)}$. In this work, we use inner product to predict the relevance of item $i$ as:

$$
r_{i, t} = <F_{t}^{(L)}, T_i>,
$$

where $T_i \in R^d$ is the embedding of item $i$. Recall that the model inputs a sequence $s = (s_1, s_2, \cdots, s_n)$ and its desired output is a shifted version of the same sequence $o = (o_1, o_2, \cdots, o_n)$, we can adopt the binary cross-entropy loss as:

$$
L_{BCE} = - \sum_{S^u \in S} \sum_{t=1}^{n}{[\log{\sigma(r_{o_t, t})} + \log{1 - \sigma (r_{o_t', t})}]} + a \cdot ||\theta||^2_F
\tag{4}
$$

where $\theta$ is the mode parameters, $a$ is the reqularizer to prevent over-fitting, $o'_t \notin S^u$ is a negative sample corresponding to $o_t$, and $\sigma(\cdot)$ is the sigmoid function.
More details can be found in SASRec [26] and BERT4Rec [41].

## 3.3. The Noisy Attentions Problem

Despite the success of SASRec and its variants, we argue that they are insufficient to address the noisy items in sequences. The reason is that the full attention distributions (e.g., Eq. (2)) are dense and would assign certain credits to irrelevant items. This complicates the item-item dependencies, increases the training difficulty, and even degrades the model performance. To address this issue, several attempts have been proposed to manually define sparse attention schemas in language modeling tasks [2, 10, 18, 58]. However, these fixed sparse attentions cannot adapt to the input data [12], leading to sub-optimal performance.

On the other hand, several dropout techniques are specifically designed for Transformers to keep only a small portion of attentions, including LayerDrop [17], DropHead [60], and UniDrop [52]. Nevertheless, these randomly dropout approaches are susceptible to bias: the fact that attentions can be dropped randomly does not mean that the model allows them to be dropped, which may lead to over-aggressive pruning issues. In contrast, we propose a simple yet effective data-driven method to mask out irrelevant attentions by using differentiable masks.

# 4. Rec-Denoiser

In this section, we present our Rec-Denoiser that consists of two parts: differentiable masks for self-attention layers and Jacobian regularization for Transformer blocks.

## 4.1. Differentiable Masks

The self-attention layer is the cornerstone of Transformers to capture long-range dependencies. As shown in Eq. (2), the softmax operator assigns a non-zero weight to every item. However, full attention distributions may not always be advantageous since they may cause irrelevant dependencies, unnecessary computation, and unexpected explanation. We next put forward differentiable masks to address this concern.

### 4.1.1. Learnable Sparse Attentions

Not every item in a sequence is aligned well with user preferences in the same sense that not all attentions are strictly needed in self-attention layers. Therefore, we attach each self-attention layer with a trainable binary mask to prune noisy or task-irrelevant attentions. Formally, for the 𝑙-th self-attention layer in Eq. (2), we introduce a binary matrix $Z^{(l)} \in {0, 1}^{n\times n}$, where $Z^{(l)}_{u,v}$ denotes whether the connection between query $u$ and key $v$ is present. As such, the $l$-th self-attention layer becomes:

$$
A^{(l)} = \text{softmax}(\frac{Q^{(l)} K^{(l)T}}{\sqrt{d}}),
\\
M^{(l)} = A^{(l)} \odot Z^{(l)},
\\
\text{Attention}(Q^{(l)}, K^{(l)}, V^{(l)}) = M^{(l)} V^{(l)},
\tag{5}
$$

where $A^{(l)}$ is the original full attentions, $M^{(l)}$ denotes the sparse attentions, and $\odot$ is the element-wise product. Intuitively, the mask $Z^{(l)}$ (e.g., 1 is kept and 0 is dropped) requires minimal changes to the original self-attention layer. More importantly, they are capable of yielding exactly zero attention scores for irrelevant dependencies, resulting in better interpretability. The idea of differentiable masks is not new. In the language modeling, differentiable masks have been shown to be very powerful to extract short yet sufficient sentences, which achieves better performance [1, 13].

One way to encourage sparsity of $M^{(l)}$ is to explicitly penalize the number of non-zero entries of $Z^{(l)}$, for $1 \leq l \leq L$, by minimizing:

$$
R_M = \sum_{l=1}^{L}||Z^{l}||_{0}
= \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0],
\tag{6}
$$

where $I[c]$ is an indicator that is equal to 1 if the condition $c$ holds and 0 otherwise; and $||\cdot||_{0}$ denotes the $L_0$ norm that is able to drive irrelevant attentions to be exact zeros.

However, there are two challenges for optimizing $Z^{(l)}$: non-differentiability and large variance. $L_0$ is discontinuous and has zero derivatives almost everywhere. Additionally, there are $2^{n^2}$ possible states for the binary mask $Z^{(l)}$ with large variance. Next, we propose an efficient estimator to solve this stochastic binary optimization problem.

### 4.1.2. Efficient Gradient Computation

Since Z (𝑙) is jointly optimized with the original Transformer-based models, we combine Eq. (4) and Eq. (6) into one unified objective:

$$
L(Z, \Theta) = L_{BCE}({A^{(l)} \odot Z^{(l)}}, \Theta) + \beta \cdot \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0]
\tag{7}
$$

where 𝛽 controls the sparsity of masks and we denote Z as Z := {Z (1) , · · · , Z (𝐿) }. We further consider each Z (𝑙) 𝑢,𝑣 is drawn from a Bernoulli distribution parameterized by Π (𝑙) 𝑢,𝑣 such that Z (𝑙) 𝑢,𝑣 ∼ Bern(Π (𝑙) 𝑢,𝑣 ) [34]. As the parameter Π (𝑙) 𝑢,𝑣 is jointly trained with the downstream tasks, a small value of Π (𝑙) 𝑢,𝑣 suggests that the attention A (𝑙) 𝑢,𝑣 is more likely to be irrelevant, and could be removed without side effects. By doing this, Eq. (7) becomes:

$$
\tag{8}
$$

where E(·) is the expectation. The regularization term is now continuous, but the first term L𝐵𝐶𝐸 (Z, Θ) still involves the discrete variables Z (𝑙) . One can address this issue by using existing gradient estimators, such as REINFORCE [48] and Straight Through Estimator [3], etc. These approaches, however, suffer from either biased gradients or high variance. Alternatively, we directly optimize discrete variables using the recently proposed augment-REINFORCEmerge (ARM) [15, 16, 56], which is unbiased and has low variance. In particular, we adopt the reparameterization trick [25], which reparameterizes Π (𝑙) 𝑢,𝑣 ∈ [0, 1] to a deterministic function 𝑔(·) with parameter Φ (𝑙) 𝑢,𝑣 , such that:

$$
\tag{9}
$$

since the deterministic function 𝑔(·) should be bounded within [0, 1], we simply choose the standard sigmoid function as our deterministic function: 𝑔(𝑥) = 1/(1 + 𝑒 −𝑥 ). As such, the second term in Eq. (8) becomes differentiable with the continuous function 𝑔(·). We next present the ARM estimator for computing the gradients of binary variables in the first term of Eq. (8) [15, 16, 56]. According to Theorem 1 in ARM [56], we can compute the gradients for Eq. (8) as:

$$
\tag{10}
$$

where Uni(0, 1) denotes the Uniform distribution within [0, 1], and L𝐵𝐶𝐸 (I[U > 𝑔(−Φ)], Θ) is the cross-entropy loss obtained by setting the binary masks Z (𝑙) to 1 if U (𝑙) > 𝑔(−Φ (𝑙) ) in the forward pass, and 0 otherwise. The same strategy is applied to L𝐵𝐶𝐸 (I[U < 𝑔(Φ)], Θ). Moreover, ARM is an unbiased estimator due to the linearity of expectations. Note that we need to evaluate L𝐵𝐶𝐸 (·) twice to compute gradients in Eq. (10). Given the fact that 𝑢 ∼ Uni(0, 1) implies (1 − 𝑢) ∼ Uni(0, 1), we can replace U with (1 − U) in the indicator function inside L𝐵𝐶𝐸 (I[U > 𝑔(−Φ)], Θ):

$$
\tag{}
$$

To this end, we can further reduce the complexity by considering the variants of ARM – Augment-Reinforce (AR) [56]:

$$
\tag{11}
$$

where only requires one-forward pass. The gradient estimator ∇ 𝐴𝑅 Φ L (Φ, Θ) is still unbiased but may pose higher variance, comparing to ∇ 𝐴𝑅𝑀 Φ L (Φ, Θ). In the experiments, we can trade off the variance of the estimator with complexity.

In the training stage, we update ∇ΦL (Φ, Θ) (either Eq. (10) or Eq. (11)) and ∇ΘL (Φ, Θ) 3 during the back propagation. In the inference stage, we can use the expectation of Z (𝑙) 𝑢,𝑣 ∼ Bern(Π (𝑙) 𝑢,𝑣 ) as the mask in Eq. (5), i.e., E(Z (𝑙) 𝑢,𝑣 ) = Π (𝑙) 𝑢,𝑣 = 𝑔(𝚽 (𝑙) 𝑢,𝑣 ). Nevertheless, this will not yield a sparse attention M(𝑙) since the sigmoid function is smooth unless the hard sigmoid function is used in Eq. (9). Here we simply clip those values 𝑔(𝚽 (𝑙) 𝑢,𝑣 ) ≤ 0.5 to zeros such that a sparse attention matrix is guaranteed and the corresponding noisy attentions are eventually eliminated.

## 4.2. Jacobian Regularization

As recently proved by [28], the standard dot-product self-attention is not Lipschitz continuous and is vulnerable to the quality of input sequences. Let 𝑓 (𝑙) be the 𝑙-th Transformer block (Sec 3.2.2) that contains both a self-attention layer and a point-wise feed-forward layer, and x be the input. We can measure the robustness of the Transformer block using the residual error: 𝑓 (𝑙) (x + 𝝐) − 𝑓 (𝑙) (x), where 𝝐 is a small perturbation vector and the norm of 𝝐 is bounded by a small scalar 𝛿, i.e., ∥𝝐 ∥2 ≤ 𝛿. Following the Taylor expansion, we have:

$$
\tag{}
$$

Let J (𝑙) (x) represent the Jacobian matrix at x where J (𝑙) 𝑖𝑗 = 𝜕 𝑓 (𝑙) 𝑖 (x) 𝜕𝑥𝑗 . Then, we set J (𝑙) 𝑖 (x) = 𝜕 𝑓 (𝑙) 𝑖 (x) 𝜕x to denote the 𝑖-th row of J (𝑙) (x). According to Hölder’s inequality4 , we have:

$$
\tag{}
$$

Above inequality indicates that regularizing the 𝐿2 norm on the Jacobians enforces a Lipschitz constraint at least locally, and the residual error is strictly bounded. Thus, we propose to regularize Jacobians with Frobenius norm for each Transformer block as:

$$
\tag{12}
$$

Importantly, ∥J (𝑙) ∥ 2 𝐹 can be approximated via various Monte-Carlo estimators [23, 37]. In this work, we adopt the classical Hutchinson estimator [23]. For each Jocobian matrix J (𝑙) ∈ R 𝑛×𝑛 , we have:

$$
\tag{}
$$

where 𝜼 ∈ N (0, I𝑛) is the normal distribution vector. We further make use of random projections to compute the norm of Jacobians R𝐽 and its gradient ∇ΘR𝐽 (Θ) [21], which significantly reduces the running time in practice.

## 4.3. Optimization

### 4.3.1. Joint Training

Putting together loss in Eq. (4), Eq. (6), and Eq. (12), the overall objective of Rec-Denoiser is:

$$
\tag{13}
$$

where 𝛽 and 𝛾 are regularizers to control the sparsity and robustness of self-attention networks, respectively. Algorithm 1 summarizes the overall training of Rec-Denoiser with the AR estimator.

Lastly, it is worth mentioning that our Rec-Denoiser is compatible to many Transformer-based sequential recommender models since our differentiable masks and gradient regularizations will not change their main architectures. If we simply set all masks Z (𝑙) to be all-ones matrix and 𝛽 = 𝛾 = 0, our model boils down to their original designs. If we randomly set subset of masks Z (𝑙) to be zeros, it is equivalent to structured Dropout like LayerDrop [17], DropHead [60]. In addition, our Rec-Denoiser can work together with linearized self-attention networks [27, 59] to further reduce the complexity of attentions. We leave this extension in the future.

### 4.3.2. Model Complexity

The complexity of Rec-Denoiser comes from three parts: a basic Transformer, differentiable masks, and Jacobian regularization. The complexity of basic Transformer keeps the same as SASRec [26] or BERT4Rec [41]. The complexity of differentiable masks requires either one-forward pass (e.g., AR with high variance) or two-forward pass (e.g., ARM with low variance) of the model. In sequential recommenders, the number of Transformer blocks is often very small (e.g., 𝐿 = 2 in SASRec [26] and BERT4Rec [41] ). It is thus reasonable to use the ARM estimator without heavy computations. Besides, we compare the performance of AR and ARM estimators in Sec 5.3. Moreover, the random project techniques are surprisingly efficient to compute the norms of Jacobians [21]. As a result, the overall computational complexity remains the same order as the original Transformers during the training. However, during the inference, our attention maps are very sparse, which enables much faster feed-forward computations.

# 5. Experiments

Here we present our empirical results. Our experiments are designed to answer the following research questions:

- RQ1: How effective is the proposed Rec-Denoiser compared to the state-of-the-art sequential recommenders?
- RQ2: How can Rec-Denoiser reduce the negative impacts of noisy items in a sequence?
- RQ3: How do different components (e.g., differentiable masks and Jacobian regularization) affect the overall performance of Rec-Denoiser?

## 5.1. Experimental Setting

### 5.1.1. Dataset

We evaluate our models on five benchmark datasets: Movielens5 , Amazon6 (we choose the three commonly used categories: Beauty, Games, and Movies&TV), and Steam7 [30]. Their statistics are shown in Table 1. Among different datasets, MovieLens is the most dense one while Beauty has the fewest actions per user. We use the same procedure as [26, 30, 39] to perform preprocessing and split data into train/valid/test sets, i.e., the last item of each user’s sequence for testing, the second-to-last for validation, and the remaining items for training.

### 5.1.2. Baselines

Here we include two groups of baselines. The first group includes general sequential methods (Sec 5.2): 1) FPMC [39]: a mixture of matrix factorization and first-order Markov chains model; 2) GRU4Rec [20]: a RNN-based method that models user action sequences; 3) Caser [42]: a CNN-based framework that captures high-order relationships via convolutional operations; 4) SASRec [26]: a Transformer-based method that uses left-to-right selfattention layers; 5) BERT4Rec [41]: an architecture that is similar to SASRec, but using bidirectional self-attention layers; 6) TiSASRec [30]: a time-aware self-attention model that further considers the relative time intervals between any two items; 7) SSE-PT [50]: a framework that introduces personalization into self-attention layers; 8) Rec-Denoiser: our proposed Rec-Denoiser that can choose any self-attentive models as its backbone. The second group contains sparse Transformers (Sec 5.3): 1) Sparse Transformer [10]: it uses a fixed attention pattern, where only specific cells summarize previous locations in the attention layers; 2) 𝛼-entmax sparse attention [12]: it simply replaces softmax with 𝛼-entmax to achieve sparsity. Note that we do not compare with other popular sparse Transformers like Star Transformer [18], Longformer [2], and BigBird [58]. These Transformers are specifically designed for thousands of tokens or longer in the language modeling tasks. We leave their explorations for recommendations in the future. We also do not compare with LayerDrop [17] and DropHead [60] since the number of Transformer blocks and heads are often very small (e.g., 𝐿 = 2 in SARRec) in sequential recommendation. Other sequential architectures like memory networks [9, 22] and graph neural networks [4, 51] have been outperformed by the above baselines, we simply omit these baselines and focus on Transformer-based models. The goal of experiments is to see whether the proposed differentiable mask techniques can reduce the negative impacts of noisy items in the self-attention layers.

### 5.1.3. Evaluation metrics

For easy comparison, we adopt two common Top-N metrics, Hit@𝑁 and NDCG@𝑁 (with default value 𝑁 = 10), to evaluate the performance of sequential models [26, 30, 41]. Typically, Hit@𝑁 counts the rates of the ground-truth items among top-𝑁 items, while NDCG@𝑁 considers the position and assigns higher weights to higher positions. Following the work [26, 30], for each user, we randomly sample 100 negative items, and rank these items with the ground-truth item. We calculate Hit@10 and NDCG@10 based on the rankings of these 101 items.

### 5.1.4. Parameter settings

For all baselines, we initialize the hyper-parameters as the ones suggested by their original work. They are then well tuned on the validation set to achieve optimal performance. The final results are conducted on the test set. We search the dimension size of items within {10, 20, 30, 40, 50}. As our Rec-Denoiser is a general plugin, we use the same hyper-parameters as the basic Transformers, e.g., number of Transformer blocks, batch size, learning rate in Adam optimizer, etc. According to Table 1, we set the maximum length of item sequence 𝑛 = 50 for dense datasets MovieLens and Movies&TV, and 𝑛 = 25 for sparse datasets Beauty, Games, and Steam. In addition, we set the number of Transformer blocks 𝐿 = 2, and the number of heads 𝐻 = 2 for self-attentive models. For Rec-Denoiser, two extra regularizers 𝛽 and 𝛾 are both searched within {10−1 , 10−2 , . . . , 10−5 }. We choose ARM estimator due to the shallow structures of self-attentive recommenders.

## 5.2. Overall Performance(RQ1)

Table 2 presents the overall recommendation performance of all methods on the five datasets. Our proposed Recdenoisers consistently obtain the best performance for all datasets. Additionally, we have the following observations:

- The self-attentive sequential models (e.g., SASRec, BERT4Rec, TiSASRec, and SSE-PT) generally outperform FPMC, GRU4Rec, and Caser with a large margin, verifying that the self-attention networks have good ability of capture long-range item dependencies for the task of sequential recommendation.
- Comparing the original SASRec and its variants BERT4Rec, TiSASRec and SSE-PT, we find that the self-attentive models can gets benefit from incorporating additional information such as bi-directional attentions, time intervals, and user personalization. Such auxiliary information is important to interpret the dynamic behaviors of users.
- The relative improvements of Rec-denoisers over their backbones are significant for all cases. For example, SASRec+Denoiser has on average 8.04% improvement with respect to Hit@10 and over 12.42% improvements with respect to NDCG@10. Analogously, BERT4Rec+Denoiser outperforms the vanilla BERT4Rec by average 7.47% in Hit@10 and 11.64% in NDCG@10. We also conduct the significant test between Rec-denoisers and their backbones, where all 𝑝-values< 1𝑒 −6 , showing that the improvements of Rec-denoisers are statistically significant in all cases.

These improvements of our proposed models are mainly attributed to the following reasons: 1) Rec-denoisers inherit full advantages of the self-attention networks as in SASRec, BERT4Rec, TiSASRec, and SSE-PT; 2) Through differentiable masks, irrelevant item-item dependencies are removed, which could largely reduce the negative impacts of noisy data; 3) Jacobian regularization enforces the smoothness of gradients, limiting quick changes of the output against input perturbations. In general, smoothness improves the generalization of sequential recommendation. Overall, the experimental results demonstrate the superiority of our Rec-Denoisers.

## 5.3. Robustness to Noises(RQ2)

As discussed before, the observed item sequences often contain some noisy items that are uncorrelated to each other. Generally, the performance of self-attention networks is sensitive to noisy input. Here we analyze how robust our training strategy is for noisy sequences. To achieve this, we follow the strategy [35] that corrupts the training data by randomly replacing a portion of the observed items in the training set with uniformly sampled items that are not in the validation or test set. We range the ratio of the corrupted training data from 0% to 25%. We only report the results of SASRec and SASRec-Denoiser in terms of Hit@10. The performance of other self-attentive models is the same and omitted here due to page limitations. In addition, we compare with two recent sparse Transformers: Sparse Transformer [10] and 𝛼-entmax sparse attention [12]. All the simulated experiments are repeated five times and the average results are shown in Figure 2. Clearly, the performance of all models degrades with the increasing noise ratio. We observe that our Rec-denoiser (use either ARM or AR estimators) consistently outperforms 𝛼-entmax and Sparse Transformer under different ratios of noise on all datasets. 𝛼-entmax heavily relies on one trainable parameter 𝛼 to filter out the noise, which may be over tuned during the training, while Sparse Transformer adopts a fixed attention pattern, which may lead to uncertain results, especially for short item sequences like Beauty and Games. In contrast, our differentaible masks have much more flexibility to adapt to noisy sequences. The Jacobian regularization further encourages the smoothness of our gradients, leading to better generalization. From the results, the AR estimator performs better than 𝛼-entmax but worse than ARM. This result is expected since ARM has much low variance. In summary, both ARM and AR estimators are able to reduce the negative impacts of noisy sequences, which could improve the robustness of self-attentive models.

## 5.4. Study of Rec-Denoiser(RQ3)

We further investigate the parameter sensitivity of Rec-Denoiser. For the number of blocks 𝐿 and the number of heads 𝐻, we find that self-attentive models typically benefit from small values (e.g., 𝐻, 𝐿 ≤ 4), which is similar to [31, 41]. In this section, we mainly study the following hyper-parameters: 1) the maximum length 𝑛, 2) the regularizers 𝛽 and 𝛾 to control the sparsity and smoothness. Here we only study the SASRec and SASRec-Denoiser due to page limitations.

Fig. 3. Effect of maximum length 𝑛 on ranking performance (Hit@10).

Fig. 4. Effect of regularizers 𝛽 and 𝛾 on ranking performance (Hit@10).

### 5.4.1. Maximum Length $n$

Figure 3 shows the Hit@10 for maximum length 𝑛 from 20 to 80 while keeping other optimal hyper-parameters unchanged. We only test on the densest and sparsest datasets: MovieLeans and Beauty. Intuitively, the larger sequence we have, the larger probability that the sequence contains noisy items. FWe observed that our SASRec-Denoiser improves the performance dramatically with longer sequences. This demonstrates that our design is more suitable for longer inputs, without worrying about the quality of sequences.

### 5.4.2. The regularizers $\beta$ and $\gamma$

There are two major regularization parameters 𝛽 and 𝛾 for sparsity and gradient smoothness, respectively. Figure 4 shows the performance by changing one parameter while fixing the other as 0.01. As can be seen, our performance is relatively stable with respect to different settings. In the experiments, the best performance can be achieved at 𝛽 = 0.01 and 𝛾 = 0.001 for the MovieLens dataset.

# 6. Conclusion and Fture Work

In this work, we propose Rec-Denoiser to adaptively eliminate the negative impacts of the noisy items for self-attentive recommender systems. The proposed Rec-Denoiser employs differentiable masks for the self-attention layers, which can dynamically prune irrelevant information. To further tackle the vulnerability of self-attention networks to small perturbations, Jacobian regularization is applied to the Transformer blocks to improve the robustness. Our experimental results on multiple real-world sequential recommendation tasks illustrate the effectiveness of our design.

Our proposed Rec-Denoiser framework (e.g., differentiable masks and Jacobian regularization) can be easily applied to any Transformer-based models in many tasks besides sequential recommendation. In the future, we will continue to demonstrate the contributions of our design in many real-world applications.
