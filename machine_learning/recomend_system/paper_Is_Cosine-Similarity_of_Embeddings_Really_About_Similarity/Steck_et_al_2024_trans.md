## 0.1. link リンク

https://arxiv.org/pdf/2403.05440.pdf
https://arxiv.org/pdf/2403.05440.pdf

## 0.2. title タイトル

Is Cosine-Similarity of Embeddings Really About Similarity?
埋め込みコサイン類似度は本当に類似度なのか？

## 0.3. abstract 抄録

Cosine-similarity is the cosine of the angle between two vectors, or equivalently the dot product between their normalizations.
コサイン類似度は、2つのベクトル間の角度の余弦、または等価的にそれらの正規化間のドット積である。
A popular application is to quantify semantic similarity between high-dimensional objects by applying cosine-similarity to a learned low-dimensional feature embedding.
よく使われるアプリケーションは、学習された低次元の特徴埋め込みに余弦類似度を適用することで、高次元のオブジェクト間の意味的類似性を定量化することである。
This can work better but sometimes also worse than the unnormalized dot-product between embedded vectors in practice.
これは、実際には埋め込みベクトル間の正規化されていないドット積よりもうまくいくこともあるが、悪くなることもある。
To gain insight into this empirical observation, we study embeddings derived from regularized linear models, where closed-form solutions facilitate analytical insights.
この経験的観測を洞察するために、我々は、閉形式解が分析的洞察を容易にする正則化線形モデルに由来する埋め込みを研究する。
We derive analytically how cosine-similarity can yield arbitrary and therefore meaningless ‘similarities.’ For some linear models the similarities are not even unique, while for others they are implicitly controlled by the regularization.
我々は、余弦類似度がどのように恣意的で無意味な「類似度」をもたらすかを解析的に導出する。ある線形モデルでは類似度は一意でさえなく、他のモデルでは正則化によって暗黙のうちに制御される。
We discuss implications beyond linear models: a combination of different regularizations are employed when learning deep models; these have implicit and unintended effects when taking cosinesimilarities of the resulting embeddings, rendering results opaque and possibly arbitrary.
線形モデル以外の意味についても議論する： ディープモデルを学習する際、様々な正則化の組み合わせが採用される。これらの正則化は、結果として得られる埋込みのコサインシミラーを取る際に、暗黙的かつ意図しない効果をもたらし、結果を不透明かつ恣意的なものにする。
Based on these insights, we caution against blindly using cosine-similarity and outline alternatives.
これらの洞察に基づき、我々はコサイン類似度を盲目的に使用することに注意を促し、代替案を概説する。

# 1. Introduction はじめに

Discrete entities are often embedded via a learned mapping to dense real-valued vectors in a variety of domains.
離散エンティティは、多くの場合、さまざまな領域において、学習されたマッピングを介して、密な実数値ベクトルに埋め込まれる。
For instance, words are embedded based on their surrounding context in a large language model (LLM), while recommender systems often learn an embedding of items (and users) based on how they are consumed by users.
例えば、大規模言語モデル（LLM）では、単語はその周囲の文脈に基づいて埋め込まれる。一方、レコメンダーシステムは、アイテム（およびユーザー）がユーザーによってどのように消費されるかに基づいて、アイテム（およびユーザー）の埋め込みを学習することが多い。
The benefits of such embeddings are manifold.
このようなエンベッディングの利点は多岐にわたる。
In particular, they can be used directly as (frozen or fine-tuned) inputs to other models, and/or they can provide a data-driven notion of (semantic) similarity between entities that were previously atomic and discrete.
特に、他のモデルへの（凍結または微調整された）入力として直接使用したり、以前は原子的で離散的であったエンティティ間の（意味的な）類似性のデータ駆動型概念を提供したりすることができる。
While similarity in ’cosine similarity’ refers to the fact that larger values (as opposed to smaller values in distance metrics) indicate closer proximity, it has, however, also become a very popular measure of semantic similarity between the entities of interest, the motivation being that the norm of the learned embedding-vectors is not as important as the directional alignment between the embedding-vectors.
コサイン類似度」の類似度は、（距離メトリクスの小さな値とは対照的に）大きな値がより近い接近を示すという事実を意味するが、しかし、それはまた、学習された埋め込みベクトルのノルムは、埋め込みベクトル間の方向の整列ほど重要ではないという動機から、関心のあるエンティティ間の意味的類似性の非常に一般的な尺度となっている。
While there are countless papers that report the successful use of cosine similarity in practical applications, it was, however, also found to not work as well as other approaches, like the (unnormalized) dot-product between the learned embeddings, e.g., see [3, 4, 8].
コサイン類似度を実用的なアプリケーションで成功裏に使用したことを報告する論文は数え切れないほどあるが、しかし、学習された埋め込み間の（正規化されていない）ドット積のような他のアプローチほどうまく機能しないことも判明している（例えば、[3, 4, 8]を参照）。
In this paper, we try to shed light on these inconsistent empirical observations.
本稿では、こうした一貫性のない経験則に光を当てたい。
We show that cosine similarity of the learned embeddings can in fact yield arbitrary results.
我々は、学習された埋込みの余弦類似度が、実際には任意の結果をもたらすことができることを示す。
We find that the underlying reason is not cosine similarity itself, but the fact that the learned embeddings have a degree of freedom that can render arbitrary cosine-similarities even though their (unnormalized) dot-products are well-defined and unique.
その根本的な理由は、コサイン類似度そのものではなく、学習された埋め込みが、その（正規化されていない）ドット積がよく定義され一意であるにもかかわらず、任意のコサイン類似度をレンダリングできる自由度を持っているという事実にあることがわかった。
To obtain insights that hold more generally, we derive analytical solutions, which is possible for linear Matrix Factorization (MF) models–this is outlined in detail in the next Section.
より一般的な洞察を得るために、線形行列因数分解（MF）モデルで可能な解析解を導く。
In Section 3, we propose possible remedies.
セクション3では、可能な改善策を提案する。
The experiments in Section 4 illustrate our findings derived in this paper.
セクション4の実験は、本稿で得られた知見を説明するものである。

# 2. Matrix Factorization Models 行列因数分解モデル

In this paper, we focus on linear models as they allow for closed-form solutions, and hence a theoretical understanding of the limitations of the cosine-similarity metric applied to learned embeddings.
本論文では、閉形式解を可能にする線形モデルに焦点を当て、それゆえ、学習された埋め込みに適用される余弦類似度メトリックの限界を理論的に理解する。
We are given a matrix X ∈ R n×p containing n data points and p features (e.g., users and items, respectively, in case of recommender systems).
$n$個のデータ点と$p$個の特徴（例えば、レコメンダーシステムの場合は、それぞれユーザーとアイテム）を含む行列 $X \in \mathbb{R}^{n \times p}$ が与えられているとする。
The goal in matrix-factorization (MF) models, or equivalently in linear autoencoders, is to estimate a low-rank matrix AB⊤ ∈ R p×p , where A, B ∈ R p×k with k ≤ p, such that the product XABT is a good approximation of X: 1 X ≈ XAB⊤.
行列因数分解(MF)モデル、あるいは線形オートエンコーダにおける目標は、低ランク行列 $AB^T \in \mathbb{R}^{p \times p}$ を推定することであり、ここで $A, B \in \mathbb{R}^{p \times k}$ であり、$k \leq p$ であり、$XAB^T$ が $X$ の良い近似であることである: $X \approx XAB^T$。
When the given X is a user-item matrix, the rows ⃗bi of B are typically referred to as the (k-dimensional) item-embeddings, while the rows of XA, denoted by ⃗xu · A, can be interpreted as the user-embeddings, where the embedding of user u is the sum of the item-embeddings ⃗aj that the user has consumed.
与えられた $X$ がuser-item行列の場合、$B$の行 $\vec{b}_{i}$ は通常、(k次元の)アイテム埋め込みと呼ばれる。一方、$XA$の行（$\vec{x}_{u} \cdot A$ で表される）は、ユーザ埋め込みと解釈できる。ここで、ユーザ $u$ の埋め込みは、ユーザが消費したアイテム埋め込み $\vec{a}_{j}$ の合計である。(item embeddingが2種類出てきてない?:thinking:)
(通常のMFのnotationでは、XAを一つの行列として表す事が多い気がする...??:thinking:)

Note that this model is defined in terms of the (unnormalized) dot-product between the user and item embeddings (XAB⊤)u,i = ⟨ ⃗xu · A, ⃗bi⟩.
このモデルは、ユーザとアイテムの埋め込み $(XA B^T)_{u,i} = <\vec{x}_{u} \cdot A, \vec{b}_{i}>$ の（正規化されていない）ドット積として定義されていることに注意してください。(損失関数内でのユーザの嗜好スコアの定義の話...?)
Nevertheless, once the embeddings have been learned, it is common practice to also consider their cosine-similarity, between two items cosSim( ⃗bi , ⃗bi ′ ), two users cosSim( ⃗xu · A, ⃗xu′ · A), or a user and an item cosSim( ⃗xu · A, ⃗bi).
それにもかかわらず、一度埋め込みが学習されると、2つのアイテム間のcosSim( $\vec{b}_{i}, \vec{b}_{i'}$ )、2人のユーザ間のcosSim( $\vec{x}_{u} \cdot A, \vec{x}_{u'} \cdot A$ )、またはユーザとアイテム間のcosSim( $\vec{x}_{u} \cdot A, \vec{b}_{i}$ )のような、**それらのcosine-similarityも考慮するのが一般的である。** (うんうん、なるほど...??)
In the following, we show that this can lead to arbitrary results, and they may not even be unique.
以下では、これが任意の結果を導き、一意でない可能性さえあることを示す。

## 2.1. Training トレーニング

A key factor affecting the utility of cosine-similarity metric is the regularization employed when learning the embeddings in A, B, as outlined in the following.
cosine-similarity メトリックの有用性に影響を与える重要な要因は、以下に概説するように、A, Bの埋め込みを学習する際に採用される正則化である。
Consider the following two, commonly used, regularization schemes (which both have closed-form solutions, see Sections 2.2 and 2.3:
よく使われる次の2つの正則化スキームを考えてみましょう（どちらも閉形式の解がある、セクション2.2と2.3を参照）。
(L1正則化とL2正則化の話...???)

$$
\min_{A,B} ||X − XAB^T||^2_F + \lambda ||AB^T||^2_F \tag{1}
$$

$$
\min_{A,B} ||X − XAB^T||^2_F + \lambda (||XA||^2_F + ||B||^2_F) \tag{2}
$$

(両方ともL2正則化を含むMFの損失関数の話...???)
The two training objectives obviously differ in their L2-norm regularization:
この2つの学習目的は、明らかにL2ノルム正則化において異なる:

In the first objective, ||AB⊤||2 F applies to their product.
第1の目的関数では、$||AB^T||^2_F$ がそれらの積に適用される。
In linear models, this kind of L2-norm regularization can be shown to be equivalent to learning with denoising, i.e., drop-out in the input layer, e.g., see [6].
線形モデルでは、この種のL2ノルム正則化は、ノイズ除去、**つまり入力層のドロップアウトで学習することと同等**であることが示されている（例えば、[6]を参照）。
Moreover, the resulting prediction accuracy on held-out test-data was experimentally found to be superior to the one of the second objective [2].
さらに、hold-outテストデータでの予測精度は、実験的に第2の目的関数よりも優れていることが実験的に見つかっている[2]。
Not only in MF models, but also in deep learning it is often observed that denoising or drop-out (this objective) leads to better results on held-out test-data than weight decay (second objective) does.
MFモデルだけでなく、ディープラーニングでも、ノイズ除去やドロップアウト（この目的）がウェイト減衰(第2の目的関数) よりもhold-outテストデータでより良い結果をもたらすことがしばしば観察される。(ノイズへのover fittingを避ける効果があるのかな...!)

The second objective is equivalent to the usual matrix factorization objective minW ||X − P Q⊤||2 F + λ(||P||2 F + ||Q||2 F ), where X is factorized as P Q⊤, and P = XA and Q = B.
|X − P Q⊤
第2の目的関数は、通常のMatrix factorization目的関数 $min_{W} ||X − PQ^T||^2_F + \lambda (||P||^2_F + ||Q||^2_F)$ と同等であり、ここで $X$ は $PQ^T$ として因数分解され、$P = XA$ および $Q = B$ である。(うんうん、これが一般的なMFのnotationな気がする...!)
This equivalence is outlined, e.g., in [2].
この等価性は、例えば[2]に概説されている。
Here, the key is that each matrix P and Q is regularized separately, similar to weight decay in deep learning.
ここで重要なのは、ディープラーニングにおけるweight decay(重み減衰?)と同様に、**各行列PとQが別々に正則化されていること**である。

If Aˆ and Bˆ are solutions to either objective, it is well known that then also ARˆ and BRˆ with an arbitrary rotation matrix R ∈ R k×k , are solutions as well.
$\hat{A}$ と $\hat{B}$ がどちらかの目的関数の解(=closed-formな解)である場合、任意の回転行列 $R \in \mathbb{R}^{k \times k}$ を用いた $\hat{A}R$ と $\hat{B}R$ もまた解であることはよく知られている。(そうなのか...!)
(rotation matrix = ベクトルや行列を特定の軸周りに回転させる行列っぽい)
While cosine similarity is invariant under such rotations R, one of the key insights in this paper is that the first (but not the second) objective is also invariant to rescalings of the columns of A and B (i.e., the different latent dimensions of the embeddings): if AˆBˆ⊤ is a solution of the first objective, so is ADD ˆ −1Bˆ⊤ where D ∈ R k×k is an arbitrary diagonal matrix.
cosine類似度はこのようなrotation matrix $R$ に対して不変である一方で、本稿の主要な洞察の一つは、**第1の目的関数がAとBの列 (i.e. 埋め込みの異なる潜在次元) のスケーリングにも不変であること**である: 第1の目的関数の解が $\hat{A}\hat{B}^T$ である場合、任意の対角行列 $D \in \mathbb{R}^{k \times k}$ を用いた $\hat{A}D D^{-1}\hat{B}^T$ もまた解である。(なるほど...??)
We can hence define a new solution (as a function of D) as follows:
したがって、新しい解を ($D$ の関数として) 以下のように定義することができる:

$$
\hat{A}^{(D)} :=  \hat{A}D
\\
\hat{B}^{(D)} :=  \hat{B}D^{-1}
\tag{3}
$$

In turn, this diagonal matrix D affects the normalization of the learned user and item embeddings (i.e., rows):
この対角行列 $D$ は、**学習されたユーザとアイテムの埋め込み（つまり、行）の正規化に影響を与える**。

$$
(X \hat{A}^{(D)})_{(normalized)} = \Omega_{A} X \hat{A}^{(D)} = \Omega_{A} X \hat{A}D
\\
\hat{B}^{(D)}_{(normalized)} = \Omega_{B} \hat{B}^{(D)} = \Omega_{B} \hat{B}D^{-1}
\tag{4}
$$

where ΩA and ΩB are appropriate diagonal matrices to normalize each learned embedding (row) to unit Euclidean norm.
ここで $\Omega_{A}$ と $\Omega_{B}$ は、それぞれの学習された埋め込み（行）をユニットユークリッドノルムに**正規化するための適切な対角行列**である。(各要素を定数倍するためのdiagonal matrix)
Note that in general the matrices do not commute, and hence a different choice for D cannot (exactly) be compensated by the normalizing matrices ΩA and ΩB.
一般に、これらの行列は可換ではないため、異なる $D$ の選択は正規化行列 $\Omega_{A}$ と $\Omega_{B}$ によって（正確に）補償されることはないことに注意してください。
(??)
As they depend on D, we make this explicit by ΩA(D) and ΩB(D).
これらは $D$ に依存するため、我々はこれを $\Omega_{A}(D)$ と $\Omega_{B}(D)$ で明示的に示す。(正規化するためには、もともとのベクトルのノルムに依存するからそりゃそう...!)
Hence, also the cosine similarities of the embeddings depend on this arbitrary matrix D.
したがって、埋め込みのcosine類似度もこの**任意の行列 $D$ に依存**する。
As one may consider the cosine-similarity between two items, two users, or a user and an item, the three combinations read
2つのアイテム、2人のユーザ、またはユーザとアイテムの間のcosine類似度を考えることができるため、3つの組み合わせは以下のようになる。

item-item:

$$
cosSim(\hat{B}^{(D)}, \hat{B}^{(D)}) = \Omega_{B}(D) \cdot \hat{B} \cdot D^{-2} \cdot \hat{B}^{T} \cdot \Omega_{B}(D)
$$

user-user:

$$
cosSim(X\hat{A}^{(D)}, X\hat{A}^{(D)}) = \Omega_{A}(D) \cdot X \cdot \hat{A} \cdot D^2 \cdot (X \cdot \hat{A})^{T} \cdot \Omega_{A}(D)
$$

user-item:

$$
cosSim(X\hat{A}^{(D)}, \hat{B}^{(D)}) = \Omega_{A}(D) \cdot X \hat{A} \cdot \hat{B}^{T} \cdot \Omega_{B}(D)
$$

It is apparent that the cosine-similarity in all three combinations depends on the arbitrary diagonal matrix D: while they all indirectly depend on D due to its effect on the normalizing matrices ΩA(D) and ΩB(D), note that the (particularly popular) item-item cosine-similarity (first line) in addition depends directly on D (and so does the user-user cosine-similarity, see second item).
**これら3つの組み合わせのcosine類似度が、任意の対角行列 $D$ に依存していることは明らか**である: それらはすべて、正規化(用の対角)行列 $\Omega_{A}(D)$ と $\Omega_{B}(D)$ に対する $D$ の影響によって間接的に $D$ に依存しているが、**（特に人気のある）item-itemのcosine類似度（最初の行）は、直接的に $D$ に依存していることに注意**してください(user-userのcosine類似度も同様、2番目の行を参照)。

<!-- ここまで読んだ! -->

## 2.2. Details on First Objective (Eq. 1) 第1目標（式1）の詳細

The closed-form solution of the training objective in Eq.1 was derived in [2] and reads Aˆ (1)Bˆ⊤ (1) = Vk · dMat(..., 1 1+λ/σ2 i , ...)k · V ⊤ k , where X =: UΣV ⊤ is the singular value decomposition (SVD) of the given data matrix X, where Σ = dMat(..., σi , ...) denotes the diagonal matrix of singular values, while U, V contain the left and right singular vectors, respectively.
式1の学習目的関数のclosed-formな解は[2]で導出され、$\hat{A}_{(1)}\hat{B}_{(1)}^T = V_k \cdot dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...)_{k} \cdot V_k^T$ となる。ここで、$X =: U \Sigma V^T$ は与えられたデータ行列 $X$ の特異値分解(SVD)であり、$\Sigma = dMat(..., \sigma_i, ...)$ は特異値のdiagonal matrix(対角行列)を示し、$U, V$ はそれぞれ左特異ベクトルと右特異ベクトルを含む。
(なるほど、dMatって、diagonal matrix=対角行列を示すnotationなのか...!:thinking:)
Regarding the k largest eigenvalues σi , we denote the truncated matrices of rank k as Uk, Vk and (...)k.
$k$個の最大固有値 $\sigma_i$ に関して、ランク$k$のtruncateされた(切り捨てられた)行列をそれぞれ $U_k, V_k$ と $(...)_k$ と表す。
We may define...
以下のように定義することができる...

$$
\hat{A}_{(1)} = \hat{B}_{(1)} := V_k \cdot dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...)_{k}^{1/2}
\tag{5}
$$

The arbitrariness of cosine-similarity becomes especially striking here when we consider the special case of a full-rank MF model, i.e., when k = p.
コサイン類似度の恣意性(arbitrariness)は、フルランクMFモデルの特別な場合、すなわち$k=p$の場合に特に顕著になる。(i.e. full-rankな行列 = 線形方程式に一意の解が存在する。rank忘れた...!:thinking:)
This is illustrated by the following two cases:
これは以下の2つのケースで説明できる：

(以下、ケース1つ目)

if we choose D = dMat(..., 1 1+λ/σ2 i , ...) 1 2 , then we have Aˆ (D) (1) = Aˆ (1) · D = V · dMat(..., 1 1+λ/σ2 i , ...) and Bˆ (D) (1) = Bˆ (1) · D−1 = V .
$D = dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...)^{1/2}$ とすると、$A_{(D)}^{(1)} = A_{(1)} \cdot D = V \cdot dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...)$ および $B_{(D)}^{(1)} = B_{(1)} \cdot D^{-1} = V$ となる。
Given that the fullrank matrix of singular vectors V is already normalized (regarding both columns and rows), the normalization ΩB = I hence equals the identity matrix I.
fullrankな特異ベクトル行列 $V$ はすでに正規化されている（列と行の両方について）事を考慮すると、したがって正規化行列 $\Omega_{B} = I$ は単位行列 $I$ と等しい。
We thus obtain regarding the item-item cosine-similarities:
こうして、item-itemのcosine類似度について得られる：

$$
cosSim(\hat{B}_{(D)}^{(1)}, \hat{B}_{(D)}^{(1)}) = VV^T = I
$$

which is quite a bizarre result, as it says that the cosine-similarity between any pair of (different) item-embeddings is zero, i.e., an item is only similar to itself, but not to any other item!
これは非常に奇妙な結果である。これは、**任意のペアの（異なる）アイテム埋め込み間のcosine類似度がゼロであることを示しており**、つまり、アイテムは自分自身にしか類似しておらず、他のアイテムには類似していないということである！

Another remarkable result is obtained for the user-item cosine-similarity:
ユーザーとアイテムのcosine類似度についても興味深い結果が得られる：

$$
cosSim(X\hat{A}_{(D)}^{(1)}, \hat{B}_{(D)}^{(1)}) = \Omega_{A} \cdot X \cdot V \cdot dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...) \cdot V^T
\\
= \Omega_{A} \cdot X \cdot \hat{A}_{(1)} \cdot \hat{B}_{(1)}^T
$$

as the only difference to the (unnormalized) dot-product is due to the matrix ΩA, which normalizes the rows—hence, when we consider the ranking of the items for a given user based on the predicted scores, cosine-similarity and (unnormalized) dot-product result in exactly the same ranking of the items as the row-normalization is only an irrelevant constant in this case.
（正規化されていない）ドット積との唯一の違いは、行を正規化する行列 $\Omega_{A}$ によるものである。なので、予測されたスコアに基づいて特定のユーザのアイテムのランキングを考えると、cosine類似度と（正規化されていない）ドット積は、この場合には無関係な定数であるため、アイテムのランキングがまったく同じになる。

(以下、ケース2つ目)

if we choose D = dMat(..., 1 1+λ/σ2 i , ...) − 1 2 , then we have analogously to the previous case: Bˆ (D) (1) = V · dMat(..., 1 1+λ/σ2 i , ...), and Aˆ (D) (1) = V is orthonormal.
$D = dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...)^{-1/2}$ とすると、前のケースと同様に、$B_{(D)}^{(1)} = V \cdot dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...)$ および $A_{(D)}^{(1)} = V$ となる。
We now obtain regarding the user-user cosine-similarities:
次に、user-userのcosine類似度について得られる：

$$
cosSim(X\hat{A}_{(D)}^{(1)}, X\hat{A}_{(D)}^{(1)}) = \Omega_{A} \cdot X \cdot X^T \cdot \Omega_{A}
$$

i.e., now the user-similarities are simply based on the raw data-matrix X, i.e., without any smoothing due to the learned embeddings.
つまり、user-similarityは今や生データ行列 $X$ に基づいており、学習された埋め込みによるスムージングはない。
Concerning the user-item cosine-similarities, we now obtain
user-itemの余弦類似度に関しては、次のようになる。

$$
cosSim(X\hat{A}_{(D)}^{(1)}, \hat{B}_{(D)}^{(1)}) = \Omega_{A} \cdot X \cdot \hat{A}_{(1)} \cdot \hat{B}_{(1)}^T \cdot \Omega_{B}
$$

i.e., now ΩB normalizes the rows of B, which we did not have in the previous choice of D.
すなわち、$\Omega_{B}$ はBの行を正規化する。これは、前のDの選択肢ではなかった。
Similarly, the item-item cosine-similarities
同様に、item-itemのcosine類似度は

$$
cosSim(\hat{B}_{(D)}^{(1)}, \hat{B}_{(D)}^{(1)}) = \Omega_{B} \cdot V \cdot dMat(..., \frac{1}{1+\lambda/\sigma^2_i}, ...)^2 \cdot V^T \cdot \Omega_{B}
$$

are very different from the bizarre result we obtained in the previous choice of D.
は、以前のDの選択で得られた奇妙な結果とは大きく異なる。

Overall, these two cases show that different choices for D result in different cosine-similarities, even though the learned model Aˆ (D) (1) Bˆ (D)⊤ (1) = Aˆ (1)Bˆ⊤ (1) is invariant to D.
全体として、**これらの2つのケースは、学習されたモデル $\hat{A}_{(D)}^{(1)}\hat{B}_{(D)}^{(1)T} = \hat{A}_{(1)}\hat{B}_{(1)}^T$ が $D$ に依らず不変であるにもかかわらず、異なる $D$ の選択が異なるcosine類似度をもたらすことを示している**。(なるほど...!それが言いたかった事なのか...!)
In other words, the results of cosine-similarity are arbitray and not unique for this model.
言い換えれば、cosine類似度の結果はこのモデルに対して任意であり、一意ではない。

<!-- ここまで読んだ! -->

## 2.3. Details on Second Objective (Eq. 2) 第2目標（式2）の詳細

The solution of the training objective in Eq.2 was derived in [7] and reads
式2の訓練目的の解は[7]で導かれ、以下のようになる。(これもclosed-formな解か...!:thinking:)

$$
\hat{A}^{(2)} = V_{k} \cdot dMat(...,\sqrt{frac{1}{\sigma_i} \cdot (1 - \frac{\lambda}{\sigma_i})_+}, ...)_{k}
\\
\hat{B}^{(2)} = V_{k} \cdot dMat(...,\sqrt{\sigma_i \cdot (1 - \frac{\lambda}{\sigma_i})_+}, ...)_{k}
$$

where (y)+ = max(0, y), and again X =: UΣV ⊤ is the SVD of the training data X, and Σ = dMat(..., σi , ...).
ここで、$(y)_+ = max(0, y)$ であり、再び $X =: U \Sigma V^T$ は訓練データ $X$ のSVDであり、$\Sigma = dMat(..., \sigma_i, ...)$ である。(SVDって3つの行列に分解するんだっけか...!:thinking:)
Note that, if we use the usual notation of MF where P = XA and Q = B, we obtain Pˆ = XAˆ (2) = Uk · dMat(..., q σi · (1 − λ σi )+, ...)k,
通常のMFの表記法を使用すると、$P = XA$ および $Q = B$ の場合、$\hat{P} = X\hat{A}^{(2)} = U_k \cdot dMat(..., \sqrt{\sigma_i \cdot (1 - \frac{\lambda}{\sigma_i})_+}, ...)_{k}$ となる。
where we can see that here the diagonal matrix dMat(..., q σi · (1 − λ σi )+, ...)k is the same for the user-embeddings and the item-embeddings in Eq.6,
ここで、diagonal metrix $dMat(..., \sqrt{\sigma_i \cdot (1 - \frac{\lambda}{\sigma_i})_+}, ...)$ が式6のユーザ埋め込みとアイテム埋め込みに対して同じであることがわかる。
as expected due to the symmetry in the L2-norm regularization ||P||2 F + ||Q||2 F in the training objective in Eq.2.
これは、式2のtraining objectiveのL2ノルム正則化 $||P||^2_F + ||Q||^2_F$ の対称性によるものである。

The key difference to the first training objective (see Eq.1) is that here the L2-norm regularization ||P||2 F + ||Q||2 F is applied to each matrix individually, so that this solution is unique (up to irrelevant rotations, as mentioned above), i.e., in this case there is no way to introduce an arbitrary diagonal matrix D into the solution of the second objective.
式1のtraining objectiveとの主な違いは、**ここではL2ノルム正則化 $||P||^2_F + ||Q||^2_F$ がそれぞれの行列に適用されているため、この解が一意である**（上述のように無関係な回転を除いて）ことである。**つまり、この場合、第2の目的関数の解に任意の対角行列 $D$ を導入する方法はない。**（なるほど...? 目的関数2を使う場合はDが任意じゃなくなるのか...!:thinking:)
Hence, the cosine-similarity applied to the learned embeddings of this MF variant yields unique results.
**したがって、このMF variantの学習された埋め込みに適用されるcosine類似度は、一意の結果をもたらす**。(ふむふむ...!)

While this solution is unique, it remains an open question if this unique diagonal matrix dMat(..., q σi · (1 − λ σi )+, ...)k regarding the user and item embeddings yields the best possible semantic similarities in practice.
**この解はユニークであるが、ユーザとアイテムの埋め込みに関するこのユニークな対角行列 $dMat(..., \sqrt{\sigma_i \cdot (1 - \frac{\lambda}{\sigma_i})_+}, ...)$ が実際に最適な意味的類似度をもたらすかどうかは未解決の問題である**。(なるほど...:thinking:)
If we believe, however, that this regularization makes the cosine-similarity useful concerning semantic similarity, we could compare the forms of the diagonal matrices in both variants, i.e., comparing Eq.6 with Eq.5 suggests that the arbitrary diagonal matrix D in the first variant (see section above) analogously may be chosen as D = dMat(..., p 1/σi , ...)k.
しかしながら、この正則化がcosine類似度を意味的類似度に有用にすると信じるならば、両方のvariantの対角行列の形を比較することができる。つまり、式6と式5を比較すると、上記のセクションで述べた第1のvariantの任意の対角行列 $D$ は $D = dMat(..., \frac{p}{\sigma_i}, ...)$ と同様に選択されるかもしれない。(??)

<!-- ここまで読んだ! -->

# 3. Remedies and Alternatives to Cosine-Similarity コサイン類似度の救済策と代替案

As we showed analytically above, when a model is trained w.r.t. the dotproduct, its effect on cosine-similarity can be opaque and sometimes not even unique.
上記で分析的に示したように、**モデルがドットプロダクトに関して訓練された場合、そのcosine類似度に対する影響は不透明であり、時には一意でさえないことがある**。
One solution obviously is to train the model w.r.t. to cosine similarity, which layer normalization [1] may facilitate.
**明らかな解決策の1つは、cosine類似度に関してモデルを訓練することであり、これにはlayer normalization [1]が役立つかもしれない**。(dot-productじゃなくて、ってことね...!:thinking:)
Another approach is to avoid the embedding space, which caused the problems outlined above in the first place, and project it back into the original space, where the cosine-similarity can then be applied.
もう一つのアプローチは、最初に上で概説した問題を引き起こした埋め込み空間を避け、それを元の空間に戻し、そこでcosine類似度を適用することである。
For instance, using the models above, and given the raw data X, one may view XAˆBˆ⊤ as its smoothed version, and the rows of XAˆBˆ⊤ as the users’ embeddings in the original space, where cosine-similarity may then be applied.
例えば、上記のモデルを使用し、生データXが与えられた場合、$X\hat{A}\hat{B}^T$をそのスムージングされたバージョンと見なし、**$X\hat{A}\hat{B}^T$の行を元の空間のユーザの埋め込みとして見なし、そこでcosine類似度を適用することができる**。
(smoothed version = たぶんsparceな離散値の行列を、denceで滑らかな連続値の行列に変換したversionってことっぽい...?:thinking:)

Apart from that, it is also important to note that, in cosine-similarity, normalization is applied only after the embeddings have been learned.
それとは別に、cosine-similarityでは、埋め込みが学習された後に正規化が適用されることも重要である。(実務上でそういうケースが多いってことかな?)
This can noticeably reduce the resulting (semantic) similarities compared to applying some normalization, or reduction of popularity-bias, before or during learning.
**これ(学習後に正規化すること)は、学習前や学習中に正規化や人気バイアスの削減を適用することと比較して、結果として得られる（意味的な）類似性を著しく減少させる可能性がある**。
This can be done in several ways.
これにはいくつかの方法がある。
For instance, a default approach in statistics is to standardize the data X (so that each column has zero mean and unit variance).
例えば、統計学におけるデフォルトのアプローチは、**データXを標準化**することである（各列がゼロ平均と単位分散を持つように）。(=これはbefore learningの話か)
Common approaches in deep learning include the use of negative sampling or inverse propensity scaling (IPS) as to account for the different item popularities (and user activity-levels).
**ディープラーニングにおける一般的なアプローチには、 異なるアイテムの人気度（およびユーザの活動レベル）を考慮するためのネガティブサンプリングや逆傾向スケーリング（IPS）の使用が含まれる。**(IPSは逆傾向スコア重み付けのことだよね!) (前者はbefore learningの話で、後者はduring learningの話か。まあ後者もdefore learningっぽく適用できるかもだけど:thinking:)
For instance, in word2vec [5], a matrix factorization model was trained by sampling negatives with a probability proportional to their frequency (popularity) in the training data taken to the power of β = 3/4, which resulted in impressive word-similarities at that time.
例えば、word2vec [5]では、$\beta = 3/4$ 乗の訓練データの頻度(人気度)に比例した確率でネガティブサンプリングを行う事で、行列因子分解モデルが訓練され、その結果、当時印象的な単語の類似性が得られた。
(word2vecって行列因子分解モデルの一種なのか...!?:thinking:)

<!-- ここまで読んだ! -->

# 4. Experiments 実験

While we discussed the full-rank model above, as it was amenable to analytical insights, we now illustrate these findings experimentally for low-rank embeddings.
フルランクモデルについては、分析的な洞察が可能であったため、上記で説明したが、ここでは、低ランクの埋め込みについて実験的にこれらの知見を説明する。
We are not aware of a good metric for semantic similarity, which motivated us to conduct experiments on simulated data, so that the ground-truth semantic similarites are known.
我々は、意味的類似性のための良い指標を知らないので、ground-truthの意味的類似性がわかっている模擬データで実験を行うことに動機づけられた。(ふむふむ...!)
To this end, we simulated data where items are grouped into clusters, and users interact with items based on their cluster preferences.
この目的のために、アイテムがクラスタにグループ化され、ユーザーがクラスタの嗜好に基づいてアイテムと相互作用するデータをシミュレートした。(clusterは、アイテムのカテゴリとかに基づいてるのかな...??)
We then examined to what extent cosine similarities applied to learned embeddings can recover the item cluster structure.
次に、学習された埋め込みに適用されたcosine類似度が、**アイテムのクラスタ構造をどの程度回復できるか**を調べた。

(以下は疑似データの作り方! 自分で作る時に参考になりそう...!:thinking:)
In detail, we generated interactions between n = 20, 000 users and p = 1, 000 items that were randomly assigned to C = 5 clusters with probabilities pc for c = 1, ..., C.
詳細には、$n=20,000$人のユーザーと$p=1,000$個のアイテムのinteractionsを生成し、それらを$c=1, ..., C$ の確率 $p_{c}$ で**ランダムに** $C=5$ つのクラスタに割り当てた。(ふむふむ...!)
Then we sampled the powerlaw-exponent for each cluster c, βc ∼ Unif(β (item) min , β(item) max ) where we chose β (item) min = 0.25 and β (item) max = 1.5, and then assigned a baseline popularity to each item i according to the powerlaw pi = PowerLaw(βc).
次に、各クラスタ $c \in \{1, ..., C\}$ に対してpowerlaw指数 $\beta_c \sim Unif(\beta_{item}^{min}, \beta_{item}^{max})$ をサンプリングした($\beta_{item}^{min} = 0.25$ および $\beta_{item}^{max} = 1.5$)。 その後、powerlaw $p_{i} = PowerLaw(\beta_c)$ に従って各アイテム $i$ にベースライン人気度を割り当てた。
(要は、まず一様分布に従って各クラスターに0.25 ~ 1.5のパラメータを割り当てて、そのパラメータを指定したPowerLawに従ってアイテムにベースライン人気度を割り当てたってことっぽい...??)
(PowerLawって何...?確率分布の一種??:thinking:)
Then we generated the items that each user u had interacted with: first, we randomly sampled user-cluster preferences puc, and then computed the user-item probabilities: pui = puci P pi i puci pi .
次に、各ユーザ $u$ が相互作用したアイテムを生成した：まず、user-clusterの嗜好 $p_{uc}$ をランダムにサンプリングし、次にuser-itemの確率を計算した：$p_{ui} = \frac{p_{uc} p_{i}}{\sum_{i} p_{uc} p_{i}}$。
We sampled the number of items for this user, ku ∼ PowerLaw(β (user)), where we used β (user) = 0.5, and then sampled ku items (without replacement) using probabilities pui.
このユーザのアイテムの数 $k_{u}$ をサンプリングし、$k_{u} \sim PowerLaw(\beta_{user})$ を使用し、その後、確率 $p_{ui}$ を使用して $k_{u}$ 個のアイテムをサンプリングした(置換なし)。ここで、$\beta_{user} = 0.5$ を使用した。

(ここから学習)
We then learned the matrices A, B according to Eq.1 and also Eq.2 (with λ = 10, 000 and λ = 100, respectively) from the simulated data.
次に、模擬データから式1および式2（それぞれ $\lambda = 10,000$ および $\lambda = 100$）に従って行列A、Bを学習した。(L2正則化項のハイパーパラメータ)
We used a low-rank constraint k = 50 ≪ p = 1, 000 to complement the analytical results for the full-rank case above.
上記のフルランクの場合の解析結果を補完するために、低ランクの制約 $k = 50 \ll p = 1,000$ を使用した。(kって、ほぼベクトルの次元数ってことでいいのかな?:thinking:)

(ここから実験結果)
Fig.1 shows the ”true” item-item-similarities as defined by the item clusters on the left hand side, while the remaining four plots show the item-item cosine similarities obtained for the following four scenarios: after training w.r.t. Eq.1, which allows for arbitrary re-scaling of the singular vectors in Vk (as outlined in Section 2.2), the center three cosine-similarities are obtained for three choices of re-scaling.
図1は、**左側にアイテムクラスタによって定義された「真の」アイテム-アイテムの類似性**を示している。残りの4つのプロットは、**次の4つのシナリオで得られたアイテム-アイテムのcosine類似度**を示している：Eq.1に対して訓練した後、Vkの特異ベクトルの任意の再スケーリングを許可する（セクション2.2で概説されているように）、中央の3つのcosine類似度は3つの再スケーリングの選択肢に対して得られている。
The last plot in this row is obtained from training w.r.t.Eq.2, which results in a unique solution for the cosine-similarities.
この行の最後のプロットは、cosine類似度に対して一意の解をもたらすEq.2に対して訓練したものである。

Again, the main purpose here is to illustrate how vastly different the resulting cosine-similarities can be even for reasonable choices of re-scaling when training w.r.t. Eq.1 (note that we did not use any extreme choice for the re-scaling here, like anti-correlated with the singular values, even though this would also be permitted), and also for the unique solution when training w.r.t.Eq.2.
再び、ここでの主な目的は、**Eq.1に対して訓練する際の合理的なre-scalingの選択に対しても、得られるcosine類似度がどれほど異なるかを示すことである**（ここでは、特異値と反相関するような極端な選択肢を使用していないが、これも許可されていることに注意してください）、そしてEq.2に対して訓練する際の一意の解に対しても。
(re-scalingの選択は、たぶんdiagnoal matrix Dの選択肢のこと...!:thinking:)

![]()

Figure 1: Illustration of the large variability of item-item cosine similarities cosSim(B, B) on the same data due to different modeling choices.
図1： 図1: モデル選択の違いによる、同じデータ上でのitem-itemのcosine類似度cosSim(B, B)の大きな変動のイラスト。
Left: groundtruth clusters (items are sorted by cluster assignment, and within each cluster by descending baseline popularity).
左： groundtruthクラスタ（アイテムは、クラスタの割り当てによって、各クラスタ内でベースライン人気の降順でソートされている）。
After training w.r.t. Eq.1, which allows for arbitrary re-scaling of the singular vectors in Vk, the center three plots show three particular choices of re-scaling, as indicated above each plot.
Eq.1(=学習目的関数ver.1!)に対して訓練した後、Vkの特異ベクトルの任意の再スケーリングを許可するため、中央の3つのプロットは、それぞれのプロットの上に示されているように、3つの特定の再スケーリングの選択を示している。
Right: based on (unique) B obtained when training w.r.t. Eq.2.
右： Eq.2(=学習目的関数ver.2!)に対して訓練した際に得られた（一意の）Bに基づいている。
(Bはアイテム埋め込み行列)

- (メモ)w.r.t.って??
  - = with respect to = ～に関して、～に対して。
  - 技術文書などでよく出てくる。ある変数や条件、状況などを前提として、その条件下での議論を行うときに使う。

# 5. Conclusions 結論

It is common practice to use cosine-similarity between learned user and/or item embeddings as a measure of semantic similarity between these entities.
学習されたユーザおよび/またはアイテムの埋め込み間のcosine類似度を、これらのエンティティ間の意味的類似性の尺度として使用することは一般的な実践である。
We study cosine similarities in the context of linear matrix factorization models, which allow for analytical derivations, and show that cosine similarities are heavily dependent on the method and regularization technique, and in some cases can be rendered even meaningless.
我々は、closed-formな解の導出が可能な線形行列因子分解モデルの文脈でcosine類似度を研究し、cosine類似度が手法や正則化技術に大きく依存し、場合によっては意味をなさなくなることを示した。
Our analytical derivations are complemented experimentally by qualitatively examining the output of these models applied simulated data where we have ground truth item-item similarity.
私たちの分析的な導出は、これらのモデルの出力を、ground truthのitem-item類似性を持つ模擬データに適用して質的に調べることで実験的に補完されている。
Based on these insights, we caution against blindly using cosine-similarity, and proposed a couple of approaches to mitigate this issue.
**これらの洞察に基づき、我々はコサイン類似度を盲目的に使用することに注意し、この問題を軽減するためのいくつかのアプローチを提案した**。
While this short paper is limited to linear models that allow for insights based on analytical derivations, we expect cosine-similarity of the learned embeddings in deep models to be plagued by similar problems, if not larger ones, as a combination of various regularization methods is typically applied there, and different layers in the model may be subject to different regularization—which implicitly determines a particular scaling (analogous to matrix D above) of the different latent dimensions in the learned embeddings in each layer of the deep model, and hence its effect on the resulting cosine similarities may become even more opaque there.
この短い論文は、解析的な導出に基づく洞察を可能にする線形モデルに限定されているが、**我々は、深層モデルの学習された埋め込みのcosine類似度が、そこで通常適用されるさまざまな正則化手法の組み合わせによって、同じ問題もしくはそれ以上の問題に悩まされることを予想している**。
そして、モデルの異なる層が異なる正則化の対象になる可能性があり、それが深層モデルの各層の学習された埋め込みの異なる潜在次元の特定のscaling（上記の行列 $D$ に類似）を暗黙的に決定し、その結果のcosine類似度に対するその効果がさらに不透明になる可能性があるからである。
(deepなモデルでそれを検証するには、解析的な導出ができないから、それこそ後半の疑似データなどを用いて実験的に検証するしかなさそう...?:thinking:)

<!-- ここまで読んだ! -->
