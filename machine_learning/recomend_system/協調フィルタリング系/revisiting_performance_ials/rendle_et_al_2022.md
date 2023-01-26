## link

https://dl.acm.org/doi/fullHtml/10.1145/3523227.3548486

https://www.semanticscholar.org/paper/Revisiting-the-Performance-of-iALS-on-Item-Rendle-Krichene/2cc27e89b6b174eb356dd33d00d70fda65b3f7e6

## title

Revisiting the Performance of iALS on Item Recommendation Benchmarks

## abstruct

Matrix factorization learned by implicit alternating least squares (iALS) is a popular baseline in recommender system research publications. iALS is known to be one of the most computationally efficient and scalable collaborative filtering methods. However, recent studies suggest that its prediction quality is not competitive with the current state of the art, in particular autoencoders and other item-based collaborative filtering methods. In this work, we revisit four well-studied benchmarks where iALS was reported to perform poorly and show that with proper tuning, iALS is highly competitive and outperforms any method on at least half of the comparisons. We hope that these high quality results together with iALS's known scalability spark new interest in applying and further improving this decade old technique.

# introduction

Research in recommender system algorithms is largely driven by results from empirical studies. Newly proposed recommender algorithms are typically compared to established baseline algorithms on a set of recommender tasks. Findings from such studies influence both the direction of future research and the algorithms for practitioners to adopt, hence it is very important to make sure that the experimental results are reliable. Recent work has highlighted issues in recommender system evaluations (e.g., [6, 24]) where newly proposed algorithms often were unable to outperform older baselines hence leading to unreliable claims about the quality of different algorithms.

In this work, we carry out a study of the performance of iALS, a matrix factorization algorithm with quadratic loss, on top-n item recommendation benchmarks. We demonstrate that iALS is able to achieve much better performance than previously reported and is competitive with recently developed and often more complex models. In addition to reinforcing the importance of tuning baseline models, we provide detailed guidance on tuning iALS, which we hope to help unlock the power of this algorithm in practice.

iALS 1 [12] is an algorithm for learning a matrix factorization model for the purpose of top-n item recommendation from implicit feedback. An example for such a recommendation task would be to find the best movies (products, songs,...) for a user given the past movies watched (products bought, songs listened,...) by this user. iALS has been proposed over a decade ago and serves as one of the most commonly used baselines in the recommender system literature. While iALS is regarded as a simple and computationally efficient algorithm, it is typically no longer considered a top performing method with respect to prediction quality (e.g., [9, 17]). In this work, we revisit four well-studied item recommendation benchmarks where poor prediction quality was reported for iALS. The benchmarks that we pick have been proposed and studied by multiple research groups [1, 6, 9, 13, 17] and other researchers have used them for evaluating newly proposed algorithms [14, 18, 25, 26]. The poor iALS results have been established and reproduced by multiple groups [1, 6, 9, 13, 17] including a paper focused on reproducibility [1]. However, contrary to these results, we show that iALS can in fact generate high quality results on exactly the same benchmarks using exactly the same evaluation method. Our iALS numbers outperform not only the previously reported numbers for iALS but outperform the reported quality of any other recommender algorithm on at least half of the evaluation metrics. We attribute this contradiction to the difficulty of evaluating baselines [24], which can be challenging for many reasons, including improper hyper-parameter tuning. In this work, we give a detailed description of the role of the iALS hyperparameters, and how to tune them. We hope that these insights help both researchers and practitioners to obtain better results for this important algorithm in the future. As our experiments show, properly tuning an existing algorithm can have as much quality gain as inventing novel modeling techniques.

Our empirical results also call for rethinking the effectiveness of the quadratic loss for ranking problems. It is striking that iALS achieves competitive or better performance than models learned with ranking losses (LambdaNet, WARP, softmax) which reflect the top-n recommendation task more closely. These observations suggest that further research efforts are needed to deepen our understanding of loss functions for recommender systems.

# Implicit Alternating Least Squares (iALS)

## Item Recommendation from Implicit Feedback

The iALS algorithm targets the problem of learning an item recommender that is trained from implicit feedback [21]. In this problem setting, items from a set I should be recommended to users u ∈ U. For learning such a recommender, a set of positive user-item pairs S⊆U × I is given. For example, a pair (u, i) ∈ S could express that user u watched movie i, or customer u bought product i. A major difficulty of learning from implicit feedback is that the pairs in S are typically positive only and need to be contrasted with all the unobserved pairs (U × I)∖S. For example, the movies that haven't been watched by a user or the products that haven't been bought by a customer need to be considered when learning the preferences of a user. A recommender algorithm uses S to learn a scoring function $\hat{y} ; U \times I -> \mathbb{R}$ that assigns a score $\hat{y}(u,i)$ to each user-item pair (u, i). A common application of the scoring function is to return a ranked list of recommended items for a user u, e.g., sorting all items by $\hat{y}(u,i)$ and recommending the k highest ranked ones to the user.

## iALS: Model, Loss and Training

iALS uses the matrix factorization model for scoring a user-item pair. Each user u is embedded into a d dimensional embedding vector Math 4 and every item i into a an embedding vector $w_u \in \mathbb{R}^d$. The predicted score of a user-item pair is the dot product between their embedding vectors: Its scoring function is

$$
\hat{y}(u,i) := <w_u, h_i>, W\in \mathbb{R}^{U\times d}, H \in \mathbb{R}^{I \times d} \tag{1}
$$

The model parameters of matrix factorization are the embedding matrices W and H. These model parameters are learned by minimizing the iALS loss, L( W, H), which consists of three components:

$$
\begin{align} L(W,H) &= L_S(W,H) + L_I(W,H) + R(W,H) \end{align} \tag*{2}
$$

There exist slightly different definitions for these components in the literature on matrix factorization with ALS. We use the formalization that weights all pairs by an unobserved weight [ 2] and allow for frequency-based regularizer as suggested by [ 29] for ALS algorithms for rating prediction. The components are defined as:

$$
\begin{align} L_S(W,H) &= \sum _{(u,i) \in S} (\hat{y}(u,i) - 1)^2 \end{align}
\tag*{3}
$$

$$
\begin{align} L_I(W,H) &= \alpha _0\sum _{u \in U} \sum _{i\in I} \hat{y}(u,i)^2 \end{align}
\tag*{4}
$$

$$
\begin{align} R(W,H) &= \lambda \left(\sum _{u \in U} \#_u^\nu \, \Vert \mathbf {w}_u\Vert ^2 + \sum _{i \in I}\#_i^\nu \, \Vert \mathbf {h}_i\Vert ^2 \right) \end{align}
\tag*{5}
$$

where

$$
\begin{align*} \#_u = |\lbrace i : (u,i) \in S\rbrace |+\alpha _0 |I|, \quad \#_i = |\lbrace u : (u,i) \in S\rbrace |+\alpha _0 |U|. \end{align*}
$$

The first component LS is defined over the observed pairs S and measures how much the predicted score differs from the observed label, here 1. The second component LI is defined over all pairs in U × I and measures how much the predicted score differs from 0. The third component R is an L2 regularizer that encourages small norms of the embedding vectors. In the regularizer, each embedding is weighted by the frequency it appears in LS and LI. ν controls the strength of the frequency regularizer and can switch between traditional ALS regularization ν = 0 and the frequency regularization weighting ν = 1 that an SGD optimizer would apply implicitly.

Individually, it is easy to get a loss of 0 for each component LS, LI, R, however, jointly they form a meaningful objective. The trade-off between the three components is controlled by the unobserved weight α0 and the regularization weight λ. Choosing the proper trade-off is crucial for iALS and is explained in detail in Section A.2.

The iALS loss can be optimized efficiently by T epochs of alternating least squares, where the computational complexity of each epoch is in $O(d^2|S| + d^3(|U|+|I|))$ for the originally proposed solver [12], or in $O(d|S| + d^2 (|U|+|I|))$ for iterative solvers [2, 10, 20].

# Evaluation

We revisit the performance of iALS on four well-studied benchmarks proposed by other authors. Two of them are item recommendation tasks and two are sampled item recommendation tasks. We use exactly the same evaluation protocol (i.e., same splits, metrics) as in the referenced papers. Table 1 summarizes the benchmarks and the selected iALS hyperparameters. For all quality results, we repeated the experiment 10 times and report the mean. Our source code is available at https://github.com/google-research/google-research/tree/master/ials/.

## Item Recommendation

Table 1: Benchmarks (dataset and evaluation protocol) used in our experiments. Our iALS hyperparameters were tuned on holdout sets. All of the experiments share ν = 1 and σ\* = 0.1. For ML1M and Pinterest, we set a maximum dimension of d = 192 for a fair comparison to the results from [9, 22].

In their work about variational autoencoders, Liang et al. [17] have established a set of benchmarks for item recommendation that have been followed by other authors [14, 18, 25, 26] since then. The benchmarks include results for iALS that were produced in [13, 17]. We reinvestigate the results on the Movielens 20M (ML20M) and Million Song Data (MSD) benchmarks. We shortly recap the overall evaluation procedure and refer to [17] and their code2 for details: The evaluation protocol removes all interactions from 10,000 users (ML20M) and 50,000 users (MSD) from the training set and puts them into a holdout set. At evaluation time, the recommender is given 80% of the interactions of each of the holdout users and is asked to generate recommendations for each user. Each ranked list of recommended items is compared to the remaining 20% of the withheld interactions, then ranking metrics are computed. The benchmark provides two versions of the holdout data: one for validation and one for testing. We use the validation set for hyperparameter tuning and report results for the testing set in Table 2. The evaluation setup is geared towards algorithms that make recommendations based on a set of items, like autoencoders or item-based CF, because the evaluation users are not available during training time. Matrix factorization with iALS summarizes the user information in a user embedding which is usually learned at training time – this is not possible for the evaluation users in this protocol. We follow the evaluation protocol strictly and do not train on any part of the evaluation users. Instead, at evaluation time, we create the user embedding using its closed form least squares expression. As discussed in [15], matrix factorization can be seen as an item-based CF method where the history embedding (=user embedding) is generated at inference time through the closed form projection. Note that when using a block solver [23], the user embedding does not have a closed form expression; instead, we perform updates for each block and repeat this 8 times.

Table 2: Quality results on the ML20M and MSD benchmark sorted by Recall@20 scores.

### 3.1.1 Quality.

Table 2 summarizes the benchmark results. The table highlights the previously reported numbers for iALS and our numbers. Previously, matrix factorization with iALS was found to perform poorly with a considerable gap to the state of the art. Both Mult-VAE [17] and the follow-up work RecVAE [25], H+Vamp (Gated) [14], RaCT [18] and EASE [26] outperform the previously reported iALS results on both datasets. However, we obtain considerably better results for iALS matrix factorization than the previously reported iALS numbers. On the MSD dataset only one method, EASE, outperforms our iALS results. On the ML20M dataset, iALS has comparable performance to Mult-VAE. No method consistently outperforms our iALS results over both datasets and all measures, but iALS consistently outperforms CDAE, Mult-DAE, SLIM, WARP. For the remaining methods, iALS is tied with 3 wins out of 6 comparisons. It is interesting to note that most high quality results in Table 2 have been obtained by the inventors of the corresponding methods which indicates that knowledge about an algorithm is useful for obtaining good results and that automated hyperparameter search alone might not be sufficient.

![](https://dl.acm.org/cms/attachment/50001494-5d72-429e-8e5c-455c715845cb/recsys22-140-fig1.jpg)
Figure 1: Our iALS benchmark results with a varying embedding dimension, d. For comparison, the plots contain also the previous iALS results from [17], EASE [26] and Mult-VAE [17]. The capacity for EASE, Mult-VAE and prev. iALS is not varied in the plot and the numbers represent the best values reported in previous work (see Section 3.1.2 for details).

### 3.1.2 Model Capacity

Embedding Dimension. The ML20M and MSD benchmarks focus mainly on quality and Table 2 reported the best quality without considering model size and capacity. Now, we discuss the trade-off between quality and model capacity of iALS and compare it to EASE and Mult-VAE as well as the previously reported iALS numbers from [17]. We measure model capacity by the number of parameters that a model reserves for each item. For iALS and Mult-VAE the item parameters are item embeddings and for EASE the parameters are in the item-to-item weight matrix. Mult-VAE has two item embeddings: one for the input items and one for the output items. Mult-VAE has additional parameters in the hidden units but the number of parameters in these units is small, so we ignore their size in the comparison of this section. During training, iALS also requires space for user embeddings, however at prediction time, embeddings of test users are computed on the fly from item embeddings.

Figure 1 breaks down the performance of iALS by embedding dimension and also includes the best results previously reported for iALS, EASE and Mult-VAE. We report the following variations:

- iALS (our results)3: We explore embedding dimensions of d ∈ {64, 128, 256, 512, 1024, 2048} for ML20M and d ∈ {128, 256, 512, 1024, 2048, 4096, 8192} for MSD.
- Mult-VAE: We use the results from [17] that were generated with 600 dimensional item embeddings for input and output embeddings, so in total Mult-VAE has 1200 free parameters per item.
- EASE: This is a dense model with |I|2 model parameters, where each item has |I| many free parameters. That means for ML20M, the EASE model has 20,108 model parameters per item and for MSD it has 41,140 model parameters per item, which is over an order of magnitude more parameters than Mult-VAE.
- iALS (previous results): These results are from [17] and use item embeddings of d ≤ 200.

Table 3: Quality results on the Movielens 1M and Pinterest benchmarks [9] sorted by HR@10 on ML1M. The previously reported numbers for iALS (and its eALS variation), and our iALS numbers are in bold. The best number is underlined.

The plots in Figure 1 show that all well performing models on this benchmark have a large capacity. For iALS, the gain of large embedding dimensions slowly levels off around d = 1024 (for ML20M) and d = 8192 (for MSD). When looking at smaller iALS dimensions, d = 1024 outperforms Mult-VAE on the MSD dataset, and a dimension of d = 512 outperforms EASE on ML20M. The MSD benchmark is interesting because the best performing methods, EASE and iALS (d = 8192) are much simpler than the advanced autoencoder methods that perform the best on ML20M. However, both EASE and iALS (d = 8192) have a very large model capacity in the item representation. That might indicate that the MSD dataset has structure that is different from ML20M, for example it might have a very high rank.

When comparing our iALS results to the previously reported iALS results [17], we can see that on ML20M, they outperform the previous results substantially, even with a smaller embedding dimension. This shows the importance of well-tuned hyperparameters. On MSD, our results are in line with the previous iALS results for a comparable embedding dimension. However, increasing the embedding dimension results in large improvements. Choosing a comparable capacity as VAE, it outperforms the previously reported iALS quality substantially.

To summarize, the trade-off between quality and model size of iALS is competitive with the state of the art Mult-VAE and EASE models.

### 3.1.3 Runtime.

Finally, the comparison so far ignored runtime. One training epoch of a multithreaded (single-machine) C++ implementation of iALS (using the block solver from [23]) took about 1 minute for d = 2048 on ML20M and 40 minutes for d = 8192 on MSD. And for smaller dimensions: 30 seconds for d = 1024 on ML20M and 1 minute 30 seconds for d = 1024 on MSD. While we ran the experiments for 16 epochs, i.e., the total runtime is 16 times higher, the results are almost converged much earlier. For example for MSD and d = 8192 the quality results after four epochs are Recall@20=0.305, Recall@50=0.412, NDCG@100=0.363. It is up to the application if it is worth spending more resources to train longer.

## Sampled Item Recommendation

We also investigate the performance of iALS on the sampled item recommendation benchmarks from [9] which have been used in multiple publications, including [1, 6, 17, 22]. The benchmark contains two datasets, Pinterest [7] and an implicit version of Movielens 1M (ML1M) [8]. The evaluation protocol removes one item from each user's history and holds it out for evaluation. At evaluation time, the recommender is asked to rank a set of 101 items, where 100 of them are random items and one is the holdout item. The evaluation metrics measure at which position the recommender places the withheld items. As discussed in [16], this evaluation task is less focused on the top items than the measured metrics indicate. We follow the same procedure as in [22] for hyperparameter tuning by holding out data from training for tuning purposes.

Table 3 summarizes the results. The original comparison in [9] reports results for eALS [10] which is a coordinate descent solver for iALS. Follow up work [6] provided results for iALS which have been reproduced in [1]. The previously reported performance of eALS and iALS is poor and not competitive on both measures and both datasets. However, with well tuned hyperparameters, we could achieve a high quality on all metrics with iALS. The results are very close to the ones for a well tuned SGD optimized matrix factorization [22] – which is expected as both are matrix factorization models with a comparable loss. The well-tuned iALS is better than NCF on three metrics and tied on one. It is also better than Mult-DAE [17] on three metrics and worse on one. Furthermore it outperforms EASE [26] and SLIM [19] on all metrics. Note that we limited the embedding dimension for iALS to d = 192 to be comparable to the previously obtained results for NCF and SGD matrix factorization. We also produced results for smaller dimensions and d = 64 without further hyperparameter tuning works reasonably well: for ML1M HR@10=0.722 and NDCG@10=0.445 and for Pinterest HR@10=0.892, NDCG@10=0.573.

# CONCLUSION

This work reinvestigated matrix factorization with the iALS algorithm and discussed techniques to obtain high quality models. On four well-studied item recommendation benchmarks, where iALS was reported to perform poorly, we found that it can actually achieve very competitive results when the hyperparameters are well tuned. In particular, none of the recently proposed methods consistently outperforms iALS. On the contrary, iALS outperforms any method on at least half of the metrics and datasets: iALS improves over a neural autoencoder in 6 out of 10 comparisons and over EASE in 7 out of 10.

These benchmarks focus on prediction quality but ignore other aspects such as training time, scalability to large item catalogs or serving of recommendations. iALS is known to excel in these dimensions: (i) It is a second order method with convergence in a few epochs. (ii) It uses the Gramian trick that solves the issue of |U| · |I| negative pairs. (iii) It is trivially parallelizable as it solves |I| independent problems. (iv) It learns an embedding for each item making the model size linear in the number of items. (v) It uses a dot product model that allows for efficient querying of the top-n scoring items for a user.

iALS also has some challenges: (i) Its loss is less aligned with ranking metrics but surprisingly, it achieves high ranking metrics on benchmarks, on par with models that optimize ranking losses such as lambdarank and softmax. Also EASE and SLIM that share the quadratic loss with iALS do not suffer from the quadratic loss on these benchmarks. (ii) In its simplest form discussed in this paper, iALS learns a matrix factorization model, making it less flexible for richer problems with extra features. However, iALS has been extended for more complex models as well [2, 11, 21]. (iii) Finally, matrix factorization requires recomputing the user embedding whenever a user provides new feedback. Bag of item models like SLIM, EASE or autoencoders do not require retraining but can just make inference using the modified input. Nevertheless, the user embedding of iALS has a closed form expression and this can be seen as the inference step of iALS. Instead of passing the history through an encoder, in iALS a different computation (the solve step) is performed.

We hope that the encouraging benchmark results for iALS spark new interest in this old technique. Other models, such as autoencoders or SLIM, benefited from a growing interest in item-based collaborative filtering that resulted in improved versions such as Mult-VAE, RecVAE or EASE. The basic iALS model might have similar potential for improvements. Besides academia, iALS should be considered as a strong option for practical applications. iALS has very appealing properties in terms of runtime, scalability and low top-n querying costs, and as this study argues, it also performs well on benchmarks in terms of quality.

Finally, this paper is another example for the difficulty of tuning machine learning models [24]. Converging to reliable numbers is a process that takes time and needs a community effort. Over the long term, shared benchmarks like the ones established in the VAE paper [17] and adopted by other researchers [14, 18, 25, 26] are a way to make progress towards reliable numbers. Until then, it should be understood that both the benchmark results that we achieve with iALS and the ones from the other methods might be further improved in the future.

# Hyperparameter Search for iALS

In this section, we give guidelines on how to choose hyperparameter values for iALS. The six hyperparameters4 of iALS are summarized in Table 4.

As our experiments in Section 3 indicate, good hyperparameter values are crucial for obtaining a high quality model. To obtain good hyperparameter values, it is important to focus the search on the important hyperparameters and spent only little time on the unimportant ones. Any reduction of the search space is very important when dealing with exponential complexity. In this section, we will describe the meaning of the iALS hyperparameters in detail. A detailed understanding of the hyperparameters will allow us to eliminate most hyperparameters from a time consuming grid-search and focus on the important regularization value λ and unobserved weight α0.

## Metrics

While exploring hyperparameters, it is useful to look at several metrics. Obviously, measuring the validation metric (e.g., Recall or NDCG on a holdout set) is useful and will drive the overall exploration. However, the validation metrics are often only loosely connected with the training process and might not reveal why a particular hyperparameter choice does not work. To spot some issues with learning related hyperparameters, we found it useful to plot the training loss L and its components LS, LI, R as well. These training losses can reveal if the hyperparameters are in the wrong region and can be useful in the beginning of the hyperparameter search.

Table 4: Hyperparameters of iALS.

![](https://d3i71xaburhd42.cloudfront.net/2cc27e89b6b174eb356dd33d00d70fda65b3f7e6/6-Table1-1.png)


## Hyperparameters

The metrics help to guide the hyperparameter search. It is important to understand the hyperparameters and reduce the search space early and then focus on the important hyperparameters. We also don't recommend tuning a large set of hyperparameters jointly but to explore them iteratively.

Number of Training Iterations. It is advisable to measure the metrics during training after each iteration. This removes the number of iterations T from the search space – provided that T is large enough. A too large value of T is not a concern with respect to quality, but only with respect to runtime. iALS converges usually within a few iterations and a reasonable initial choice could be 16 iterations. Depending on the observed convergence curve, this value can be increased or decreased later. For speeding up exploration, we also found it useful to use a smaller value during initial exploration of the hyperparameter space, and then increase it for the final search. For example, using 8 instead of 16 iterations during a broad search will cut the runtime in half.

Standard Deviation for Initialization. Usually, the standard deviation for iALS is easy to set and we haven't observed much sensitivity within a broad range. Instead of setting the hyperparameter σ, it helps to rescale it by the embedding dimension

$$
\sigma = \frac{1}{\sqrt{d}} \sigma^*
\tag*{6}
$$

where σ * is a small constant, such as 0.1. This makes the initialization less sensitive to large changes in the embedding dimension. The intuition is that this keeps the variance of a random dot product constant, i.e., the variance of predictions at initialization is independent of d.

We only observe some sensitivity if the value for the standard deviation is chosen orders of magnitude too small or too large. In this case, it takes a few extra steps for iALS to readjust the norms of the user and item embeddings. This can be spotted easily by plotting L, LS, LI and R where LS will not drop immediately.
Embedding Dimension. The embedding dimension controls the capacity of the model. From our experience, a common reason for suboptimal results with iALS is that the embedding dimension is chosen too small. We usually observe that, with proper regularization, the larger the embedding dimension the better the quality. For example, for the Movielens 20M dataset, we found that 2000 dimensions provide the best results. It may seem that a 2000 dimensional embedding is too expressive for a dataset that has 73 ratings per user on average. And even worse it might lead to overfitting. However, empirically, larger dimensions are better and L2 regularization is very effective at preventing overfitting. Moreover, other successful models such as VAE are also trained with large embedding dimensions and full rank models such as EASE are also effective. The effectiveness of large embedding dimensions for matrix factorization is also well studied in the rating prediction literature [15, 20, 29].

![](https://dl.acm.org/cms/attachment/4e7097e6-fce8-4b0e-9f90-26605004a8c2/recsys22-140-fig2.jpg)

Figure 2: When using frequency-scaled regularization, ν, good regularization values λ are in different regions for different choices of ν (left). A shifted regularization scale λ* brings good values on the same scale as a reference scale ν*. The middle plot shows scaling to the reference ν* = 0, the right to the reference ν* = 1.

Computational resources are an important factor when choosing the embedding dimension. A good strategy is to first get a rough estimate of good hyperparameter values using a mid-sized embedding dimension, such as d = 128, and then to perform a more refined search using larger embedding dimensions, e.g., doubling the dimension during each refinement of the other hyperparameters until the improvement plateaus. This way, the first pass is sufficiently fast and more time can be spent for the detailed search of the most important parameters: unobserved weight and regularization.

### Unobserved Weight and Regularization.

Both unobserved weight α0 and the regularization λ are crucial for iALS 5 and it is important to choose them carefully. It is advisable to search the unobserved weight together with the regularization because both of them control the trade-off between the three loss components, LS, LI and R. Intuitively, we know that for item recommendation we need both LS and LI – otherwise the solution degenerates to always predicting 1 (if α0 = 0) or always predicting 0 (if α0 → ∞). So, the observed error values of LS and LI shouldn't differ by several orders of magnitude. Similarly, with large embedding dimensions, we need some regularization, so again the values of R, LS and LI should have comparable orders of magnitude.

The scale of regularization values depends on ν (Eq. (5)) which sets the strength of frequency regularization – see Figure 2 left side for an example. Without frequency regularization, ν = 0, good regularization values are typically larger than 1, for frequency regularization ν = 1, good regularization values are usually smaller than 1. This is because the regularization value λ is scaled by (I(u) + α0|I|)ν for each user and by (U(i) + α0|U|)ν for each item. So, if ν is increased and λ is kept constant, then the regularization effect gets stronger. Having two parameters that interact in this way can be complicated during hyperparameter search because whenever ν is changed, the region of good values for λ changes. Instead it can help to normalize the regularization values to a reference scale and search over the normalized parameter λ* with

$$
\begin{align} \lambda &= \lambda ^* \frac{\sum _{i \in I} (|U(i)| + \alpha _0 |U|)^{\nu ^*} + \sum _{u \in U} (|I(u)| + \alpha _0 |I|)^{\nu ^*}}{\sum _{i \in I} (|U(i)| + \alpha _0 |U|)^{\nu } + \sum _{u \in U} (|I(u)| + \alpha _0 |I|)^{\nu }}, \end{align}
$$

where ν * is the reference scale. For example, if we want the regularization values for all ν to be in the same region as ν = 0, we would choose ν * = 0. See Figure  2 middle, where good regularization values λ * are in the same region for ν = 1 as for ν = 0. The right plot in Figure  2 shows a case where ν * = 1 is chosen as the reference and good regularization values for ν = 0 are shifted to the region of the frequency regularized version ν = 1. Which reference ν * to pick depends on the practitioner and the application. For example, if there is a comparison to SGD algorithms, choosing the reference as ν * = 1 might be useful. Or if a practitioner is more familiar with common ALS algorithms, ν * = 0 might be better. Note that the discussed rescaling of λ does not introduce any new hyperparameters and is for convenience only. Also ν * is an arbitrary choice of a reference, it does not need any tuning and (unlike ν) has no effects on the solution; it just simplifies the hyperparameter search for regularization values, λ. Unless stated otherwise, in the following we discuss λ * with a reference point of ν * = 1.

After the relationship of the parameters has been described, we want to give some practical advice on the search. When setting the unobserved weight one should consider the degree of matrix sparseness. It is advised that the overall magnitude of the unobserved loss term (LI(W, H) eq. (4)) does not dominate that of the observed loss term (LS(W, H) eq. (3)). Thus, usually, the unobserved weight is smaller than 1.0 and is decreasing for sparser matrices6. A good starting point is an exponential grid, for example α0 ∈ {1, 0.3, 0.1, 0.03, 0.01, 0.003}. For the regularization, a good starting point is λ* ∈ {0.1, 0.03, 0.01, 0.003, 0.001, 0.0003}. The regularization becomes especially important for larger embedding dimensions. If the hyperparameter search is performed on too small an embedding dimension, the regularization value found on the small dimension might not be a good one for larger dimensions. A large enough dimension (e.g., d = 128) can be used to get a rough estimate on which area a finer search with a higher dimension should focus on. The suggested parameters are a starting point and need to be refined based on the results.

Some additional notes:

- The training errors L for different hyperparameter settings are not comparable and should not be used for selecting a model.
- Plotting curves for validation quality vs. log unobserved weight and validation quality vs. log regularization can help to get an idea which parts can be abandoned and where to refine. In general, we would expect to see some  ∪ -shaped curve (for error) or  ∩ -shaped curve (for quality) for the parameters – if not, then the boundaries of the search may need to be expanded (see Figure 2 for an example). Also the change in quality between two neighboring hyperparameter values shouldn't be too abrupt, otherwise more exploration is needed.
- It also helps not to refine exclusively around the best results, but to look at the overall behavior of the curves to get a better understanding of how hyperparameters interact on a particular data set.
- Measuring the noise in the validation metrics (i.e., if the same experiment is repeated twice, how much do the numbers differ) is also useful to avoid reading too much into a single experiment.
- At some point, large embedding dimensions should be considered. Doubling the embedding dimensions until no improvement is observed is a good strategy. If no improvement is observed, a refined search of regularization and unobserved weight might be needed. Then one can double the embedding dimension again.

Frequency Scaled Regularization. In the experiments of Section 3, frequency scaled regularization was useful and ν = 1 worked the best. Interestingly, it becomes more important with larger embedding dimensions. For example, even though the quality plateaued with ν = 0, with ν = 1 further increasing the embedding dimension gave additional improvements.

# References

https://dl.acm.org/doi/fullHtml/10.1145/3523227.3548486#:~:text=gave%20additional%20improvements.-,REFERENCES,-Vito%C2%A0Walter%20Anelli
