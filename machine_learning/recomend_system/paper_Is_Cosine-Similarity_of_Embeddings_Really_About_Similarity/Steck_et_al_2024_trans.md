## link リンク

https://arxiv.org/pdf/2403.05440.pdf
https://arxiv.org/pdf/2403.05440.pdf

## title タイトル

Is Cosine-Similarity of Embeddings Really About Similarity?
埋め込みコサイン類似度は本当に類似度なのか？

## abstract 抄録

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

# Introduction はじめに

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

# Matrix Factorization Models 行列因数分解モデル

In this paper, we focus on linear models as they allow for closed-form solutions, and hence a theoretical understanding of the limitations of the cosine-similarity metric applied to learned embeddings.
本論文では、閉形式解を可能にする線形モデルに焦点を当て、それゆえ、学習された埋め込みに適用される余弦類似度メトリックの限界を理論的に理解する。
We are given a matrix X ∈ R n×p containing n data points and p features (e.g., users and items, respectively, in case of recommender systems).
n個のデータ点とp個の特徴（例えば、レコメンダー・システムの場合、それぞれユーザーとアイテム）を含む行列X∈R n×pが与えられる。
The goal in matrix-factorization (MF) models, or equivalently in linear autoencoders, is to estimate a low-rank matrix AB⊤ ∈ R p×p , where A, B ∈ R p×k with k ≤ p, such that the product XABT is a good approximation of X: 1 X ≈ XAB⊤.
行列因数分解(MF)モデル、あるいは線形オートエンコーダにおける目標は、低ランク行列ABA4⊤∈R p×p（A, B∈R p×k、k≦p）、積XABTがXの良い近似となるような行列を推定することである： 1 X ≈ XAB⊤。
When the given X is a user-item matrix, the rows ⃗bi of B are typically referred to as the (k-dimensional) item-embeddings, while the rows of XA, denoted by ⃗xu · A, can be interpreted as the user-embeddings, where the embedding of user u is the sum of the item-embeddings ⃗aj that the user has consumed.
与えられたXがユーザーアイテム行列であるとき、Bの行⃗biは一般的に（k次元）アイテム埋め込みと呼ばれ、一方、⃗xu - Aで示されるXAの行はユーザー埋め込みと解釈される。
Note that this model is defined in terms of the (unnormalized) dot-product between the user and item embeddings (XAB⊤)u,i = ⟨ ⃗xu · A, ⃗bi⟩.
このモデルは、ユーザーとアイテムの埋め込み（XAB⊤）u,i = ⟨xu - A, ⃗bi⟩の間の（正規化されていない）ドット積で定義されていることに注意。
Nevertheless, once the embeddings have been learned, it is common practice to also consider their cosine-similarity, between two items cosSim( ⃗bi , ⃗bi ′ ), two users cosSim( ⃗xu · A, ⃗xu′ · A), or a user and an item cosSim( ⃗xu · A, ⃗bi).
埋め込みが学習されると、2つのアイテムcosSim( ⃗ ⃗ ′ )、2つのユーザーcosSim( ⃗ ⃗ - A, ⃗ ⃗ - A)、またはユーザーとアイテムのcosSim( ⃗ ⃗ - A, ⃗ ⃗ ⃗ ⃗ )の間の余弦類似性も考慮するのが一般的です。
In the following, we show that this can lead to arbitrary results, and they may not even be unique.
以下では、これが任意の結果を導き、一意でない可能性さえあることを示す。

## Training トレーニング

A key factor affecting the utility of cosine-similarity metric is the regularization employed when learning the embeddings in A, B, as outlined in the following.
cosine-similarity メトリックの有用性に影響を与える重要な要因は、以下に概説するように、A, Bの埋め込みを学習する際に採用される正則化である。
Consider the following two, commonly used, regularization schemes (which both have closed-form solutions, see Sections 2.2 and 2.3:
よく使われる次の2つの正則化スキームを考えてみよう（どちらも閉形式解を持つ、セクション2.2と2.3参照）：

$$
$$

The two training objectives obviously differ in their L2-norm regularization: • In the first objective, ||AB⊤||2 F applies to their product.
この2つの訓練目的は、L2ノルムの正則化において明らかに異なる： - 最初の目的では 
In linear models, this kind of L2-norm regularization can be shown to be equivalent to learning with denoising, i.e., drop-out in the input layer, e.g., see [6].
線形モデルでは、このようなL2-norm正則化は、ノイズ除去を伴う学習、つまり入力層でのドロップアウトと等価であることが示される。
Moreover, the resulting prediction accuracy on held-out test-data was experimentally found to be superior to the one of the second objective [2].
さらに、保留されたテストデータに対する予測精度は、実験的に第2の目的[2]のものよりも優れていることが判明した。
Not only in MF models, but also in deep learning it is often observed that denoising or drop-out (this objective) leads to better results on held-out test-data than weight decay (second objective) does.
MFモデルだけでなく、ディープラーニングにおいても、ノイズ除去やドロップアウト（この目的）は、ウェイト減衰（第2の目的）よりも、保持されたテストデータでより良い結果をもたらすことがよく観察される。
• The second objective is equivalent to the usual matrix factorization objective minW ||X − P Q⊤||2 F + λ(||P||2 F + ||Q||2 F ), where X is factorized as P Q⊤, and P = XA and Q = B.
|X − P Q⊤
This equivalence is outlined, e.g., in [2].
この等価性は、例えば[2]に概説されている。
Here, the key is that each matrix P and Q is regularized separately, similar to weight decay in deep learning.
ここで重要なのは、ディープラーニングにおけるウェイト減衰と同様に、各行列PとQが別々に正則化されることだ。
If Aˆ and Bˆ are solutions to either objective, it is well known that then also ARˆ and BRˆ with an arbitrary rotation matrix R ∈ R k×k , are solutions as well.
AˆとBˆがいずれかの目的に対する解であるならば、任意の回転行列R∈R k×kを持つARˆとBRˆも解であることはよく知られている。
While cosine similarity is invariant under such rotations R, one of the key insights in this paper is that the first (but not the second) objective is also invariant to rescalings of the columns of A and B (i.e., the different latent dimensions of the embeddings): if AˆBˆ⊤ is a solution of the first objective, so is ADD ˆ −1Bˆ⊤ where D ∈ R k×k is an arbitrary diagonal matrix.
コサイン類似度はこのような回転Rに対して不変であるが、本論文の重要な洞察の1つは、第一の目的（第二の目的ではない）は、AとBの列の再スケーリング（すなわち、埋込みの異なる潜在次元）に対しても不変であるということである： もしAˆBˆ⊤が第1の目的の解であれば、ADD ˆ -1B ˆ⊤も同様であり、ここでD∈R k×k は任意の対角行列である。
We can hence define a new solution (as a function of D) as follows:
したがって、新しい解を（Dの関数として）次のように定義することができる：

$$

$$

In turn, this diagonal matrix D affects the normalization of the learned user and item embeddings (i.e., rows):
この対角行列Dは、学習されたユーザーとアイテムの埋め込み（つまり行）の正規化に影響する：

$$

$$

where ΩA and ΩB are appropriate diagonal matrices to normalize each learned embedding (row) to unit Euclidean norm.
ここでΩAとΩBは、学習された各埋め込み（行）を単位ユークリッドノルムに正規化するための適切な対角行列である。
Note that in general the matrices do not commute, and hence a different choice for D cannot (exactly) be compensated by the normalizing matrices ΩA and ΩB.
一般に行列は通分しないので、Dに異なる選択をしたとしても、正規化行列ΩAとΩBによって（正確に）補正することはできない。
As they depend on D, we make this explicit by ΩA(D) and ΩB(D).
これらはDに依存するので、ΩA(D)とΩB(D)で明示する。
Hence, also the cosine similarities of the embeddings depend on this arbitrary matrix D.
したがって、埋込みの余弦類似度もこの任意の行列Dに依存する。
As one may consider the cosine-similarity between two items, two users, or a user and an item, the three combinations read
2つのアイテム、2人のユーザー、またはユーザーとアイテムの間の余弦類似度を考えると、3つの組み合わせは以下のようになる。

$$

$$

It is apparent that the cosine-similarity in all three combinations depends on the arbitrary diagonal matrix D: while they all indirectly depend on D due to its effect on the normalizing matrices ΩA(D) and ΩB(D), note that the (particularly popular) item-item cosine-similarity (first line) in addition depends directly on D (and so does the user-user cosine-similarity, see second item).
3つの組み合わせの余弦類似度は、すべて任意の対角行列Dに依存することが明らかである： これらはすべて正規化行列ΩA(D)とΩB(D)への影響により間接的にDに依存するが、（特によく使われる）項目-項目の余弦類似度（1行目）はさらにDに直接依存することに注意（ユーザー-ユーザーの余弦類似度も同様、2番目の項目を参照）。

## Details on First Objective (Eq. 1) 第1目標（式1）の詳細

The closed-form solution of the training objective in Eq.1 was derived in [2] and reads Aˆ (1)Bˆ⊤ (1) = Vk · dMat(..., 1 1+λ/σ2 i , ...)k · V ⊤ k , where X =: UΣV ⊤ is the singular value decomposition (SVD) of the given data matrix X, where Σ = dMat(..., σi , ...) denotes the diagonal matrix of singular values, while U, V contain the left and right singular vectors, respectively.
式1の学習目的の閉形式解は[2]で導かれ、 Aˆ (1)Bˆ⊤ (1) = Vk - dMat(..., 1 1+λ/σ2 i , ...)k - V ⊤ k 、ここでX =： ここで Σ = dMat(..., σi , ...) は特異値の対角行列を表し， U, V はそれぞれ左特異ベクトルと右特異ベクトルを含む．
Regarding the k largest eigenvalues σi , we denote the truncated matrices of rank k as Uk, Vk and (...)k.
k個の最大固有値σi について、ランクkの切り捨て行列をUk, Vk, (...)kとする。
We may define2
を定義することができる。

$$

$$

The arbitrariness of cosine-similarity becomes especially striking here when we consider the special case of a full-rank MF model, i.e., when k = p.
コサイン類似度の恣意性は、フルランクMFモデルの特別な場合、すなわちk=pの場合を考えると、特に顕著になる。
This is illustrated by the following two cases: • if we choose D = dMat(..., 1 1+λ/σ2 i , ...) 1 2 , then we have Aˆ (D) (1) = Aˆ (1) · D = V · dMat(..., 1 1+λ/σ2 i , ...) and Bˆ (D) (1) = Bˆ (1) · D−1 = V .
これは以下の2つのケースで説明できる： - D = dMat(..., 1 1+λ/σ2 i , ...) 1 2 とすると、Aˆ (D) (1) = Aˆ (1) - D = V - dMat(..., 1 1+λ/σ2 i , ...) となり、Bˆ (D) (1) = Bˆ (1) - D-1 = V となる。
Given that the fullrank matrix of singular vectors V is already normalized (regarding both columns and rows), the normalization ΩB = I hence equals the identity matrix I.
特異ベクトルVのフルランク行列が（列と行の両方に関して）すでに正規化されていることを考えると、正規化ΩB = Iは、したがって恒等行列Iに等しい。
We thus obtain regarding the item-item cosine-similarities:
こうして、項目間の余弦類似度が得られる：

$$

$$

which is quite a bizarre result, as it says that the cosine-similarity between any pair of (different) item-embeddings is zero, i.e., an item is only similar to itself, but not to any other item! Another remarkable result is obtained for the user-item cosine-similarity:
これは非常に奇妙な結果である。というのも、（異なる）アイテム包含の任意のペア間の余弦類似度はゼロであり、つまり、アイテムはそれ自身にのみ類似しているが、他のアイテムには類似していないからである！もう一つの驚くべき結果は、ユーザー-アイテムの余弦類似度について得られる：

$$

$$

as the only difference to the (unnormalized) dot-product is due to the matrix ΩA, which normalizes the rows—hence, when we consider the ranking of the items for a given user based on the predicted scores, cosine-similarity and (unnormalized) dot-product result in exactly the same ranking of the items as the row-normalization is only an irrelevant constant in this case.
(正規化されていない)ドット積との唯一の違いは、行を正規化する行列ΩAによるものである。したがって、予測されたスコアに基づいて、与えられたユーザーに対するアイテムのランキングを考えるとき、余弦類似度と(正規化されていない)ドット積は、行の正規化がこの場合に無関係な定数にすぎないように、アイテムの全く同じランキングになる。

if we choose D = dMat(..., 1 1+λ/σ2 i , ...) − 1 2 , then we have analogously to the previous case: Bˆ (D) (1) = V · dMat(..., 1 1+λ/σ2 i , ...), and Aˆ (D) (1) = V is orthonormal.
D = dMat(..., 1 1+λ/σ2 i , ...) - 1 2 とすると、前のケースと同様に Bˆ (D) (1) = V - dMat(..., 1 1+λ/σ2 i , ...) であり、Aˆ (D) (1) = V は正規直交である。
We now obtain regarding the user-user cosine-similarities:
次に、ユーザーとユーザーの余弦類似度について求める：

$$

$$

i.e., now the user-similarities are simply based on the raw data-matrix X, i.e., without any smoothing due to the learned embeddings.
つまり、ユーザー・シミラリティは、学習された埋め込みによる平滑化なしで、生のデータ行列Xに基づくだけである。
Concerning the user-item cosine-similarities, we now obtain
ユーザーとアイテムの余弦類似度に関しては、次のようになる。

$$

$$

i.e., now ΩB normalizes the rows of B, which we did not have in the previous choice of D.
すなわち、ΩBはBの行を正規化する。
Similarly, the item-item cosine-similarities
同様に、項目間の余弦類似度

$$

$$

are very different from the bizarre result we obtained in the previous choice of D.
は、以前のDの選択で得られた奇妙な結果とは大きく異なる。

Overall, these two cases show that different choices for D result in different cosine-similarities, even though the learned model Aˆ (D) (1) Bˆ (D)⊤ (1) = Aˆ (1)Bˆ⊤ (1) is invariant to D.
全体として、これらの2つのケースは、学習モデルAˆ (D) (1) Bˆ (D)↪Sm_22A4 (1) = Aˆ (1)Bˆ⊤ (1)がDに対して不変であるにもかかわらず、Dの選択が異なると余弦類似度が異なることを示している。
In other words, the results of cosine-similarity are arbitray and not unique for this model.
言い換えれば、余弦類似度の結果は恣意的なものであり、このモデルに固有のものではない。

## Details on Second Objective (Eq. 2) 第2目標（式2）の詳細

The solution of the training objective in Eq.2 was derived in [7] and reads
式2の訓練目的の解は[7]で導かれ、以下のようになる。

$$

$$

where (y)+ = max(0, y), and again X =: UΣV ⊤ is the SVD of the training data X, and Σ = dMat(..., σi , ...).
ここで、(y)+ = max(0, y)、またX =： UΣV ⊤は学習データXのSVDであり、Σ = dMat(..., σi , ...)である。
Note that, if we use the usual notation of MF where P = XA and Q = B, we obtain Pˆ = XAˆ (2) = Uk · dMat(..., q σi · (1 − λ σi )+, ...)k, where we can see that here the diagonal matrix dMat(..., q σi · (1 − λ σi )+, ...)k is the same for the user-embeddings and the item-embeddings in Eq.6, as expected due to the symmetry in the L2-norm regularization ||P||2 F + ||Q||2 F in the training objective in Eq.2.The key difference to the first training objective (see Eq.1) is that here the L2-norm regularization ||P||2 F + ||Q||2 F is applied to each matrix individually, so that this solution is unique (up to irrelevant rotations, as mentioned above), i.e., in this case there is no way to introduce an arbitrary diagonal matrix D into the solution of the second objective.
|P
Hence, the cosine-similarity applied to the learned embeddings of this MF variant yields unique results.
したがって、このMF変種の学習済み埋め込みにコサイン類似度を適用すると、ユニークな結果が得られる。
While this solution is unique, it remains an open question if this unique diagonal matrix dMat(..., q σi · (1 − λ σi )+, ...)k regarding the user and item embeddings yields the best possible semantic similarities in practice.
この解はユニークであるが、ユーザーとアイテムの埋め込みに関するこのユニークな対角行列dMat(..., q σi - (1 - λ σi )+, ...)kが、実際に可能な限り最良の意味的類似性をもたらすかどうかは未解決のままである。
If we believe, however, that this regularization makes the cosine-similarity useful concerning semantic similarity, we could compare the forms of the diagonal matrices in both variants, i.e., comparing Eq.6 with Eq.5 suggests that the arbitrary diagonal matrix D in the first variant (see section above) analogously may be chosen as D = dMat(..., p 1/σi , ...)k.
しかしながら、この正則化がコサイン類似度を意味的類似度に関して有用にすると考えるならば、両変形における対角行列の形式を比較することができる。すなわち、式.6と式.5を比較すると、最初の変形における任意の対角行列D（上のセクションを参照）は、類推的にD = dMat(..., p 1/σi , ...)kとして選択されることが示唆される。

![]()

Figure 1: Illustration of the large variability of item-item cosine similarities cosSim(B, B) on the same data due to different modeling choices.
図1： 図1: モデル選択の違いによる、同じデータ上での項目-項目余弦類似度cosSim(B, B)の大きなばらつきの説明。
Left: groundtruth clusters (items are sorted by cluster assignment, and within each cluster by descending baseline popularity).
左： groundtruthクラスタ（アイテムは、クラスタの割り当てによって、各クラスタ内でベースライン人気の降順でソートされている）。
After training w.r.t.
トレーニング後
Eq.1, which allows for arbitrary re-scaling of the singular vectors in Vk, the center three plots show three particular choices of re-scaling, as indicated above each plot.
式.1では、Vkの特異ベクトルを任意に再スケーリングすることができますが、中央の3つのプロットは、各プロットの上に示されているように、再スケーリングの3つの特定の選択を示しています。
Right: based on (unique) B obtained when training w.r.t.
右： 訓練時に得られた（ユニークな）Bに基づく。
Eq.2.
式2。

# Remedies and Alternatives to Cosine-Similarity コサイン類似度の救済策と代替案

As we showed analytically above, when a model is trained w.r.t.
上で解析的に示したように、モデルがw.r.t.で学習された場合、次のようになる。
the dotproduct, its effect on cosine-similarity can be opaque and sometimes not even unique.
ドットプロダクションがコサイン類似度に与える影響は不透明で、一意でないことさえある。
One solution obviously is to train the model w.r.t.
一つの解決策は、明らかにモデルを訓練することである。
to cosine similarity, which layer normalization [1] may facilitate.
レイヤーの正規化 [1]が容易になるかもしれない。
Another approach is to avoid the embedding space, which caused the problems outlined above in the first place, and project it back into the original space, where the cosine-similarity can then be applied.
もう一つのアプローチは、そもそも上記の問題を引き起こした埋め込み空間を避け、元の空間に投影し直し、そこで余弦類似度を適用することである。
For instance, using the models above, and given the raw data X, one may view XAˆBˆ⊤ as its smoothed version, and the rows of XAˆBˆ⊤ as the users’ embeddings in the original space, where cosine-similarity may then be applied.
例えば、上記のモデルを使用し、生データXが与えられた場合、XAˆBˆ⊤を平滑化したものと見なし、XAˆBˆ⊤の行を元の空間におけるユーザーの埋め込みと見なし、そこで余弦類似度を適用することができる。
Apart from that, it is also important to note that, in cosine-similarity, normalization is applied only after the embeddings have been learned.
それとは別に、cosine-similarityでは、埋め込みが学習された後にのみ正規化が適用されることも重要である。
This can noticeably reduce the resulting (semantic) similarities compared to applying some normalization, or reduction of popularity-bias, before or during learning.
これは、学習前や学習中に何らかの正規化を施したり、人気バイアスを軽減したりするのに比べて、結果として得られる（意味的な）類似性を著しく低下させる可能性がある。
This can be done in several ways.
これにはいくつかの方法がある。
For instance, a default approach in statistics is to standardize the data X (so that each column has zero mean and unit variance).
例えば、統計学におけるデフォルトのアプローチは、データXを標準化することである（各列がゼロ平均と単位分散を持つように）。
Common approaches in deep learning include the use of negative sampling or inverse propensity scaling (IPS) as to account for the different item popularities (and user activity-levels).
ディープラーニングにおける一般的なアプローチには、異なるアイテムの人気度（およびユーザーのアクティビティレベル）を考慮するためのネガティブサンプリングや逆傾向スケーリング（IPS）の使用が含まれる。
For instance, in word2vec [5], a matrix factorization model was trained by sampling negatives with a probability proportional to their frequency (popularity) in the training data taken to the power of β = 3/4, which resulted in impressive word-similarities at that time.
例えば、word2vec [5]では、β = 3/4乗の学習データにおける頻度（人気度）に比例した確率で否定語をサンプリングすることで、行列因数分解モデルを学習した。

# Experiments 実験

While we discussed the full-rank model above, as it was amenable to analytical insights, we now illustrate these findings experimentally for low-rank embeddings.
フルランクモデルについては、分析的な洞察が可能であったため、上記で説明したが、ここでは、低ランクの埋め込みについて実験的にこれらの知見を説明する。
We are not aware of a good metric for semantic similarity, which motivated us to conduct experiments on simulated data, so that the ground-truth semantic similarites are known.
我々は、意味的類似性のための良い指標を知らないので、真実の意味的類似性を知るために、模擬データで実験を行う動機となった。
To this end, we simulated data where items are grouped into clusters, and users interact with items based on their cluster preferences.
この目的のために、アイテムがクラスタにグループ化され、ユーザーがクラスタの嗜好に基づいてアイテムと相互作用するデータをシミュレートした。
We then examined to what extent cosine similarities applied to learned embeddings can recover the item cluster structure.
次に、学習された埋め込みにコサイン類似度を適用することで、どの程度項目クラスター構造を復元できるかを調べた。
In detail, we generated interactions between n = 20, 000 users and p = 1, 000 items that were randomly assigned to C = 5 clusters with probabilities pc for c = 1, ..., C.
詳細には、c = 1, ..., Cの確率pcでC = 5クラスタにランダムに割り当てられたn = 20, 000ユーザーとp = 1, 000アイテムの間の相互作用を生成した。
Then we sampled the powerlaw-exponent for each cluster c, βc ∼ Unif(β (item) min , β(item) max ) where we chose β (item) min = 0.25 and β (item) max = 1.5, and then assigned a baseline popularity to each item i according to the powerlaw pi = PowerLaw(βc).
次に、各クラスタcのパワーロー指数βc ∼ Unif(β (item) min , β (item) max ) をサンプリングし、β (item) min = 0.25 と β (item) max = 1.5 を選び、パワーローpi = PowerLaw(βc)に従って各アイテムiにベースライン人気を割り当てた。
Then we generated the items that each user u had interacted with: first, we randomly sampled user-cluster preferences puc, and then computed the user-item probabilities: pui = puci P pi i puci pi .
次に、各ユーザーuが相互作用したアイテムを生成した： まず、ユーザー・クラスタの嗜好pucをランダムにサンプリングし、ユーザー・アイテムの確率を計算した： pui = puci P pi i puci pi .
We sampled the number of items for this user, ku ∼ PowerLaw(β (user)), where we used β (user) = 0.5, and then sampled ku items (without replacement) using probabilities pui.
このユーザーのアイテム数ku ∼ PowerLaw(β (user))をサンプリングし、ここではβ (user) = 0.5とし、確率puiを用いてku個のアイテムを（置換なしで）サンプリングした。
We then learned the matrices A, B according to Eq.1 and also Eq.2 (with λ = 10, 000 and λ = 100, respectively) from the simulated data.
次に、模擬データから式1および式2（それぞれλ=10,000、λ=100）に従って行列A、Bを学習した。
We used a low-rank constraint k = 50 ≪ p = 1, 000 to complement the analytical results for the full-rank case above.
上記のフルランクの場合の解析結果を補完するために、低ランクの制約k = 50 ≪ p = 1,000≫を使用した。
Fig.1 shows the ”true” item-item-similarities as defined by the item clusters on the left hand side, while the remaining four plots show the item-item cosine similarities obtained for the following four scenarios: after training w.r.t.
Fig.1は左側に項目クラスタによって定義された「真の」項目間類似度を示し、残りの4つのプロットは以下の4つのシナリオで得られた項目間余弦類似度を示す： 訓練後w.r.t.
Eq.1, which allows for arbitrary re-scaling of the singular vectors in Vk (as outlined in Section 2.2), the center three cosine-similarities are obtained for three choices of re-scaling.
式.1は、（セクション2.2で概説したように）Vkの特異ベクトルを任意に再スケーリングできるようにするもので、再スケーリングの3つの選択に対して、中心3つの余弦類似度が得られる。
The last plot in this row is obtained from training w.r.t.
この行の最後のプロットは、r.t.トレーニングから得られたものである。
Eq.2, which results in a unique solution for the cosine-similarities.
式.2により、余弦類似度に対する一意解が得られる。
Again, the main purpose here is to illustrate how vastly different the resulting cosine-similarities can be even for reasonable choices of re-scaling when training w.r.t.
繰り返しになるが、ここでの主な目的は、訓練時のリ・スケーリングを合理的に選択した場合でも、結果として得られる余弦類似度がいかに大きく異なるかを説明することである。
Eq.1 (note that we did not use any extreme choice for the re-scaling here, like anti-correlated with the singular values, even though this would also be permitted), and also for the unique solution when training w.r.t.
Eq.1（ここでは、特異値と反相関するような極端な再スケーリングは行っていない。
Eq.2.
式2。

# Conclusions 結論

It is common practice to use cosine-similarity between learned user and/or item embeddings as a measure of semantic similarity between these entities.
これらのエンティティ間の意味的類似性の尺度として、学習されたユーザおよび/またはアイテムの埋め込み間の余弦類似度を使用することが一般的である。
We study cosine similarities in the context of linear matrix factorization models, which allow for analytical derivations, and show that cosine similarities are heavily dependent on the method and regularization technique, and in some cases can be rendered even meaningless.
我々は、解析的な導出が可能な線形行列分解モデルの文脈で余弦類似度を研究し、余弦類似度は手法と正則化手法に大きく依存し、場合によっては無意味にさえなり得ることを示す。
Our analytical derivations are complemented experimentally by qualitatively examining the output of these models applied simulated data where we have ground truth item-item similarity.
私たちの分析的な導出は、これらのモデルの出力を、グランドトゥルースの項目-項目の類似性を持つシミュレーションデータに適用して定性的に調べることにより、実験的に補完される。
Based on these insights, we caution against blindly using cosine-similarity, and proposed a couple of approaches to mitigate this issue.
これらの洞察に基づき、我々はコサイン類似度を盲目的に使用することに注意し、この問題を軽減するためのいくつかのアプローチを提案した。
While this short paper is limited to linear models that allow for insights based on analytical derivations, we expect cosine-similarity of the learned embeddings in deep models to be plagued by similar problems, if not larger ones, as a combination of various regularization methods is typically applied there, and different layers in the model may be subject to different regularization—which implicitly determines a particular scaling (analogous to matrix D above) of the different latent dimensions in the learned embeddings in each layer of the deep model, and hence its effect on the resulting cosine similarities may become even more opaque there.
この短い論文は、解析的導出に基づく洞察を可能にする線形モデルに限定されているが、様々な正則化手法の組み合わせが一般的に適用されるため、ディープモデルにおける学習された埋め込み値の余弦類似性は、より大きな問題ではないにせよ、同様の問題に悩まされることが予想される、 これは、ディープモデルの各層で学習された埋め込みにおける異なる潜在次元の特定のスケーリング（上記の行列Dに類似）を暗黙のうちに決定するものであり、それゆえ、結果として得られる余弦類似度に対するその影響は、そこでさらに不透明となる可能性がある。