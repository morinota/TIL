## link

https://arxiv.org/pdf/2403.05440.pdf

## title

Is Cosine-Similarity of Embeddings Really About Similarity?

## abstract
Cosine-similarity is the cosine of the angle between two vectors, or equivalently the dot product between their normalizations. A popular application is to quantify semantic similarity between high-dimensional objects by applying cosine-similarity to a learned low-dimensional feature embedding. This can work better but sometimes also worse than the unnormalized dot-product between embedded vectors in practice. To gain insight into this empirical observation, we study embeddings derived from regularized linear models, where closed-form solutions facilitate analytical insights. We derive analytically how cosine-similarity can yield arbitrary and therefore meaningless ‘similarities.’ For some linear models the similarities are not even unique, while for others they are implicitly controlled by the regularization. We discuss implications beyond linear models: a combination of different regularizations are employed when learning deep models; these have implicit and unintended effects when taking cosinesimilarities of the resulting embeddings, rendering results opaque and possibly arbitrary. Based on these insights, we caution against blindly using cosine-similarity and outline alternatives.

# Introduction

Discrete entities are often embedded via a learned mapping to dense real-valued vectors in a variety of domains. For instance, words are embedded based on their surrounding context in a large language model (LLM), while recommender systems often learn an embedding of items (and users) based on how they are consumed by users. The benefits of such embeddings are manifold. In particular, they can be used directly as (frozen or fine-tuned) inputs to other models, and/or they can provide a data-driven notion of (semantic) similarity between entities that were previously atomic and discrete. While similarity in ’cosine similarity’ refers to the fact that larger values (as opposed to smaller values in distance metrics) indicate closer proximity, it has, however, also become a very popular measure of semantic similarity between the entities of interest, the motivation being that the norm of the learned embedding-vectors is not as important as the directional alignment between the embedding-vectors. While there are countless papers that report the successful use of cosine similarity in practical applications, it was, however, also found to not work as well as other approaches, like the (unnormalized) dot-product between the learned embeddings, e.g., see [3, 4, 8]. In this paper, we try to shed light on these inconsistent empirical observations. We show that cosine similarity of the learned embeddings can in fact yield arbitrary results. We find that the underlying reason is not cosine similarity itself, but the fact that the learned embeddings have a degree of freedom that can render arbitrary cosine-similarities even though their (unnormalized) dot-products are well-defined and unique. To obtain insights that hold more generally, we derive analytical solutions, which is possible for linear Matrix Factorization (MF) models–this is outlined in detail in the next Section. In Section 3, we propose possible remedies. The experiments in Section 4 illustrate our findings derived in this paper.

# Matrix Factorization Models 

In this paper, we focus on linear models as they allow for closed-form solutions, and hence a theoretical understanding of the limitations of the cosine-similarity metric applied to learned embeddings. We are given a matrix X ∈ R n×p containing n data points and p features (e.g., users and items, respectively, in case of recommender systems). The goal in matrix-factorization (MF) models, or equivalently in linear autoencoders, is to estimate a low-rank matrix AB⊤ ∈ R p×p , where A, B ∈ R p×k with k ≤ p, such that the product XABT is a good approximation of X: 1 X ≈ XAB⊤. When the given X is a user-item matrix, the rows ⃗bi of B are typically referred to as the (k-dimensional) item-embeddings, while the rows of XA, denoted by ⃗xu · A, can be interpreted as the user-embeddings, where the embedding of user u is the sum of the item-embeddings ⃗aj that the user has consumed. Note that this model is defined in terms of the (unnormalized) dot-product between the user and item embeddings (XAB⊤)u,i = ⟨ ⃗xu · A, ⃗bi⟩. Nevertheless, once the embeddings have been learned, it is common practice to also consider their cosine-similarity, between two items cosSim( ⃗bi , ⃗bi ′ ), two users cosSim( ⃗xu · A, ⃗xu′ · A), or a user and an item cosSim( ⃗xu · A, ⃗bi). In the following, we show that this can lead to arbitrary results, and they may not even be unique.

## Training 


A key factor affecting the utility of cosine-similarity metric is the regularization employed when learning the embeddings in A, B, as outlined in the following. Consider the following two, commonly used, regularization schemes (which both have closed-form solutions, see Sections 2.2 and 2.3:

$$
$$

The two training objectives obviously differ in their L2-norm regularization: • In the first objective, ||AB⊤||2 F applies to their product. In linear models, this kind of L2-norm regularization can be shown to be equivalent to learning with denoising, i.e., drop-out in the input layer, e.g., see [6]. Moreover, the resulting prediction accuracy on held-out test-data was experimentally found to be superior to the one of the second objective [2]. Not only in MF models, but also in deep learning it is often observed that denoising or drop-out (this objective) leads to better results on held-out test-data than weight decay (second objective) does. • The second objective is equivalent to the usual matrix factorization objective minW ||X − P Q⊤||2 F + λ(||P||2 F + ||Q||2 F ), where X is factorized as P Q⊤, and P = XA and Q = B. This equivalence is outlined, e.g., in [2]. Here, the key is that each matrix P and Q is regularized separately, similar to weight decay in deep learning. If Aˆ and Bˆ are solutions to either objective, it is well known that then also ARˆ and BRˆ with an arbitrary rotation matrix R ∈ R k×k , are solutions as well. While cosine similarity is invariant under such rotations R, one of the key insights in this paper is that the first (but not the second) objective is also invariant to rescalings of the columns of A and B (i.e., the different latent dimensions of the embeddings): if AˆBˆ⊤ is a solution of the first objective, so is ADD ˆ −1Bˆ⊤ where D ∈ R k×k is an arbitrary diagonal matrix. We can hence define a new solution (as a function of D) as follows:

$$

$$

In turn, this diagonal matrix D affects the normalization of the learned user and item embeddings (i.e., rows):

$$

$$

where ΩA and ΩB are appropriate diagonal matrices to normalize each learned embedding (row) to unit Euclidean norm. Note that in general the matrices do not commute, and hence a different choice for D cannot (exactly) be compensated by the normalizing matrices ΩA and ΩB. As they depend on D, we make this explicit by ΩA(D) and ΩB(D). Hence, also the cosine similarities of the embeddings depend on this arbitrary matrix D. As one may consider the cosine-similarity between two items, two users, or a user and an item, the three combinations read

$$

$$

It is apparent that the cosine-similarity in all three combinations depends on the arbitrary diagonal matrix D: while they all indirectly depend on D due to its effect on the normalizing matrices ΩA(D) and ΩB(D), note that the (particularly popular) item-item cosine-similarity (first line) in addition depends directly on D (and so does the user-user cosine-similarity, see second item).

## Details on First Objective (Eq. 1) 

The closed-form solution of the training objective in Eq. 1 was derived in [2] and reads Aˆ (1)Bˆ⊤ (1) = Vk · dMat(..., 1 1+λ/σ2 i , ...)k · V ⊤ k , where X =: UΣV ⊤ is the singular value decomposition (SVD) of the given data matrix X, where Σ = dMat(..., σi , ...) denotes the diagonal matrix of singular values, while U, V contain the left and right singular vectors, respectively. Regarding the k largest eigenvalues σi , we denote the truncated matrices of rank k as Uk, Vk and (...)k. We may define2

$$

$$

The arbitrariness of cosine-similarity becomes especially striking here when we consider the special case of a full-rank MF model, i.e., when k = p. This is illustrated by the following two cases: • if we choose D = dMat(..., 1 1+λ/σ2 i , ...) 1 2 , then we have Aˆ (D) (1) = Aˆ (1) · D = V · dMat(..., 1 1+λ/σ2 i , ...) and Bˆ (D) (1) = Bˆ (1) · D−1 = V . Given that the fullrank matrix of singular vectors V is already normalized (regarding both columns and rows), the normalization ΩB = I hence equals the identity matrix I. We thus obtain regarding the item-item cosine-similarities:

$$

$$

which is quite a bizarre result, as it says that the cosine-similarity between any pair of (different) item-embeddings is zero, i.e., an item is only similar to itself, but not to any other item! Another remarkable result is obtained for the user-item cosine-similarity:

$$

$$

as the only difference to the (unnormalized) dot-product is due to the matrix ΩA, which normalizes the rows—hence, when we consider the ranking of the items for a given user based on the predicted scores, cosine-similarity and (unnormalized) dot-product result in exactly the same ranking of the items as the row-normalization is only an irrelevant constant in this case.

if we choose D = dMat(..., 1 1+λ/σ2 i , ...) − 1 2 , then we have analogously to the previous case: Bˆ (D) (1) = V · dMat(..., 1 1+λ/σ2 i , ...), and Aˆ (D) (1) = V is orthonormal. We now obtain regarding the user-user cosine-similarities:

$$

$$

i.e., now the user-similarities are simply based on the raw data-matrix X, i.e., without any smoothing due to the learned embeddings. Concerning the user-item cosine-similarities, we now obtain

$$

$$

i.e., now ΩB normalizes the rows of B, which we did not have in the previous choice of D. Similarly, the item-item cosine-similarities

$$

$$

are very different from the bizarre result we obtained in the previous choice of D.


Overall, these two cases show that different choices for D result in different cosine-similarities, even though the learned model Aˆ (D) (1) Bˆ (D)⊤ (1) = Aˆ (1)Bˆ⊤ (1) is invariant to D. In other words, the results of cosine-similarity are arbitray and not unique for this model.

## Details on Second Objective (Eq. 2) 

The solution of the training objective in Eq. 2 was derived in [7] and reads

$$

$$

where (y)+ = max(0, y), and again X =: UΣV ⊤ is the SVD of the training data X, and Σ = dMat(..., σi , ...). Note that, if we use the usual notation of MF where P = XA and Q = B, we obtain Pˆ = XAˆ (2) = Uk · dMat(..., q σi · (1 − λ σi )+, ...)k, where we can see that here the diagonal matrix dMat(..., q σi · (1 − λ σi )+, ...)k is the same for the user-embeddings and the item-embeddings in Eq. 6, as expected due to the symmetry in the L2-norm regularization ||P||2 F + ||Q||2 F in the training objective in Eq. 2. The key difference to the first training objective (see Eq. 1) is that here the L2-norm regularization ||P||2 F + ||Q||2 F is applied to each matrix individually, so that this solution is unique (up to irrelevant rotations, as mentioned above), i.e., in this case there is no way to introduce an arbitrary diagonal matrix D into the solution of the second objective. Hence, the cosine-similarity applied to the learned embeddings of this MF variant yields unique results. While this solution is unique, it remains an open question if this unique diagonal matrix dMat(..., q σi · (1 − λ σi )+, ...)k regarding the user and item embeddings yields the best possible semantic similarities in practice. If we believe, however, that this regularization makes the cosine-similarity useful concerning semantic similarity, we could compare the forms of the diagonal matrices in both variants, i.e., comparing Eq. 6 with Eq. 5 suggests that the arbitrary diagonal matrix D in the first variant (see section above) analogously may be chosen as D = dMat(..., p 1/σi , ...)k.

![]()

Figure 1: Illustration of the large variability of item-item cosine similarities cosSim(B, B) on the same data due to different modeling choices. Left: groundtruth clusters (items are sorted by cluster assignment, and within each cluster by descending baseline popularity). After training w.r.t. Eq. 1, which allows for arbitrary re-scaling of the singular vectors in Vk, the center three plots show three particular choices of re-scaling, as indicated above each plot. Right: based on (unique) B obtained when training w.r.t. Eq. 2.

# Remedies and Alternatives to Cosine-Similarity 

As we showed analytically above, when a model is trained w.r.t. the dotproduct, its effect on cosine-similarity can be opaque and sometimes not even unique. One solution obviously is to train the model w.r.t. to cosine similarity, which layer normalization [1] may facilitate. Another approach is to avoid the embedding space, which caused the problems outlined above in the first place, and project it back into the original space, where the cosine-similarity can then be applied. For instance, using the models above, and given the raw data X, one may view XAˆBˆ⊤ as its smoothed version, and the rows of XAˆBˆ⊤ as the users’ embeddings in the original space, where cosine-similarity may then be applied. Apart from that, it is also important to note that, in cosine-similarity, normalization is applied only after the embeddings have been learned. This can noticeably reduce the resulting (semantic) similarities compared to applying some normalization, or reduction of popularity-bias, before or during learning. This can be done in several ways. For instance, a default approach in statistics is to standardize the data X (so that each column has zero mean and unit variance). Common approaches in deep learning include the use of negative sampling or inverse propensity scaling (IPS) as to account for the different item popularities (and user activity-levels). For instance, in word2vec [5], a matrix factorization model was trained by sampling negatives with a probability proportional to their frequency (popularity) in the training data taken to the power of β = 3/4, which resulted in impressive word-similarities at that time.


# Experiments

While we discussed the full-rank model above, as it was amenable to analytical insights, we now illustrate these findings experimentally for low-rank embeddings. We are not aware of a good metric for semantic similarity, which motivated us to conduct experiments on simulated data, so that the ground-truth semantic similarites are known. To this end, we simulated data where items are grouped into clusters, and users interact with items based on their cluster preferences. We then examined to what extent cosine similarities applied to learned embeddings can recover the item cluster structure. In detail, we generated interactions between n = 20, 000 users and p = 1, 000 items that were randomly assigned to C = 5 clusters with probabilities pc for c = 1, ..., C. Then we sampled the powerlaw-exponent for each cluster c, βc ∼ Unif(β (item) min , β(item) max ) where we chose β (item) min = 0.25 and β (item) max = 1.5, and then assigned a baseline popularity to each item i according to the powerlaw pi = PowerLaw(βc). Then we generated the items that each user u had interacted with: first, we randomly sampled user-cluster preferences puc, and then computed the user-item probabilities: pui = puci P pi i puci pi . We sampled the number of items for this user, ku ∼ PowerLaw(β (user)), where we used β (user) = 0.5, and then sampled ku items (without replacement) using probabilities pui. We then learned the matrices A, B according to Eq. 1 and also Eq. 2 (with λ = 10, 000 and λ = 100, respectively) from the simulated data. We used a low-rank constraint k = 50 ≪ p = 1, 000 to complement the analytical results for the full-rank case above. Fig. 1 shows the ”true” item-item-similarities as defined by the item clusters on the left hand side, while the remaining four plots show the item-item cosine similarities obtained for the following four scenarios: after training w.r.t. Eq. 1, which allows for arbitrary re-scaling of the singular vectors in Vk (as outlined in Section 2.2), the center three cosine-similarities are obtained for three choices of re-scaling. The last plot in this row is obtained from training w.r.t. Eq. 2, which results in a unique solution for the cosine-similarities. Again, the main purpose here is to illustrate how vastly different the resulting cosine-similarities can be even for reasonable choices of re-scaling when training w.r.t. Eq. 1 (note that we did not use any extreme choice for the re-scaling here, like anti-correlated with the singular values, even though this would also be permitted), and also for the unique solution when training w.r.t. Eq. 2.

# Conclusions

It is common practice to use cosine-similarity between learned user and/or item embeddings as a measure of semantic similarity between these entities. We study cosine similarities in the context of linear matrix factorization models, which allow for analytical derivations, and show that cosine similarities are heavily dependent on the method and regularization technique, and in some cases can be rendered even meaningless. Our analytical derivations are complemented experimentally by qualitatively examining the output of these models applied simulated data where we have ground truth item-item similarity. Based on these insights, we caution against blindly using cosine-similarity, and proposed a couple of approaches to mitigate this issue. While this short paper is limited to linear models that allow for insights based on analytical derivations, we expect cosine-similarity of the learned embeddings in deep models to be plagued by similar problems, if not larger ones, as a combination of various regularization methods is typically applied there, and different layers in the model may be subject to different regularization—which implicitly determines a particular scaling (analogous to matrix D above) of the different latent dimensions in the learned embeddings in each layer of the deep model, and hence its effect on the resulting cosine similarities may become even more opaque there.

