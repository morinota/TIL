## 0.1. link リンク

- 元論文: [Visualizing Data using t-SNE](https://lvdmaaten.github.io/publications/papers/JMLR_2008.pdf) 元論文 [t-SNEによるデータの可視化](https://lvdmaaten.github.io/publications/papers/JMLR_2008.pdf)

## 0.2. title タイトル

Visualizing Data using t-SNE
t-SNEを使ったデータの可視化

## 0.3. absract absract

We present a new technique called “t-SNE” that visualizes high-dimensional data by giving each datapoint a location in a two or three-dimensional map.
各データポイントに2次元または3次元の地図上の位置を与えることによって、**高次元データを可視化する「t-SNE」と呼ばれる新しい手法**を紹介する。
The technique is a variation of Stochastic Neighbor Embedding (Hinton and Roweis, 2002) that is much easier to optimize, and produces significantly better visualizations by reducing the tendency to crowd points together in the center of the map.
この手法は、確率的近傍埋め込み（Stochastic Neighbor Embedding）（Hinton and Roweis, 2002）のバリエーションであり、最適化がはるかに容易で、マップの中心に点が密集する傾向を抑えることで、大幅に優れた視覚化を実現する。
t-SNE is better than existing techniques at creating a single map that reveals structure at many different scales.
t-SNEは、多くの異なるスケールにおける構造を明らかにする単一のマップを作成する上で、既存の技術よりも優れている。
This is particularly important for high-dimensional data that lie on several different, but related, low-dimensional manifolds, such as images of objects from multiple classes seen from multiple viewpoints.
これは、複数の視点から見た複数のクラスのオブジェクトの画像のような、複数の異なる、しかし関連する低次元多様体上にある高次元データにとって特に重要である。
For visualizing the structure of very large data sets, we show how t-SNE can use random walks on neighborhood graphs to allow the implicit structure of all of the data to influence the way in which a subset of the data is displayed.
非常に大規模なデータセットの構造を可視化するために、t-SNEが近傍グラフ上のランダムウォークをどのように使用できるかを示す。
We illustrate the performance of t-SNE on a wide variety of data sets and compare it with many other non-parametric visualization techniques, including Sammon mapping, Isomap, and Locally Linear Embedding.
様々なデータセットにおけるt-SNEの性能を示し、サモン・マッピング、アイソマップ、局所線形埋め込みを含む他の多くのノンパラメトリック可視化技術と比較する。
The visualizations produced by t-SNE are significantly better than those produced by the other techniques on almost all of the data sets.
**t-SNEによって生成された可視化は、ほとんどすべてのデータセットにおいて、他の手法によって生成された可視化よりも有意に優れている**。

# 1. Introduction はじめに

Visualization of high-dimensional data is an important problem in many different domains, and deals with data of widely varying dimensionality.
高次元データの可視化は様々な領域で重要な問題であり、様々な次元のデータを扱う。
Cell nuclei that are relevant to breast cancer, for example, are described by approximately 30 variables (Street et al., 1993), whereas the pixel intensity vectors used to represent images or the word-count vectors used to represent documents typically have thousands of dimensions.
例えば、乳がんに関連する細胞核は約30の変数で記述される（Street et al, 1993）が、画像を表現するのに使われるピクセル強度ベクトルや文書を表現するのに使われる単語数ベクトルは、通常数千の次元を持つ。
Over the last few decades, a variety of techniques for the visualization of such high-dimensional data have been proposed, many of which are reviewed by de Oliveira and Levkowitz (2003).
ここ数十年の間に、このような**高次元データの可視化のための様々な技術**が提案されており、その多くはde Oliveira and Levkowitz (2003)によってレビューされている。
Important techniques include iconographic displays such as Chernoff faces (Chernoff, 1973), pixel-based techniques (Keim, 2000), and techniques that represent the dimensions in the data as vertices in a graph (Battista et al., 1994).
重要な技法には、チェルノフ・フェイス（Chernoff, 1973）のような図像表示、ピクセル・ベースの技法（Keim, 2000）、データの次元をグラフの頂点として表現する技法（Battista et al, 1994）などがある。
Most of these techniques simply provide tools to display more than two data dimensions, and leave the interpretation of the data to the human observer.
**これらの技術のほとんどは、2次元以上のデータを表示するツールを提供するだけで、データの解釈は人間の観察者に委ねられている。**(三次元以上は解釈むずいよな...!f)
This severely limits the applicability of these techniques to real-word data sets that contain thousands of high-dimensional datapoints.
このため、何千もの高次元データポイントを含む実世界のデータセットには、これらの技術の適用が著しく制限される。(うんうん)

In contrast to the visualization techniques discussed above, dimensionality reduction methods convert the high-dimensional data set X = {x1, x2,..., xn} into two or three-dimensional data Y = {y1, y2,..., yn} that can be displayed in a scatterplot.
上述の可視化技術とは対照的に、**次元削減法は、高次元データセット $X = \{x_1, x_2, ..., x_n\}$ を、散布図に表示できる2次元または3次元データ $Y = \{y_1, y_2, ..., y_n\}$ に変換する**。
In the paper, we refer to the low-dimensional data representation Y as a map, and to the low-dimensional representations yi of individual datapoints as map points.
本稿では、**低次元データ表現 $Y$ をマップ**と呼び、個々のデータポイントの低次元表現 $y_i$ を**マップポイント**と呼ぶ。
The aim of dimensionality reduction is to preserve as much of the significant structure of the high-dimensional data as possible in the low-dimensional map.
**次元削減の目的は、高次元のデータの重要な構造を低次元のマップにできるだけ残す**ことである。
Various techniques for this problem have been proposed that differ in the type of structure they preserve.
この問題に対しては、保存する構造の種類が異なる様々な手法が提案されている。
Traditional dimensionality reduction techniques such as Principal Components Analysis (PCA; Hotelling, 1933) and classical multidimensional scaling (MDS; Torgerson, 1952) are linear techniques that focus on keeping the low-dimensional representations of dissimilar datapoints far apart.
主成分分析(PCA; Hotelling, 1933)や古典的な多次元尺度構成法(MDS; Torgerson, 1952)のような**伝統的な次元削減技法は、異種データポイントの低次元表現を遠ざけることに焦点を当てた線形技法**である。
For high-dimensional data that lies on or near a low-dimensional, non-linear manifold it is usually more important to keep the low-dimensional representations of very similar datapoints close together, which is typically not possible with a linear mapping.
低次元の非線形多様体上または近傍にある高次元データに対しては、非常に類似したデータポイントの低次元表現を近くに保つことが、**通常は線形マッピングでは不可能であるため、非線形マッピング**が必要となる。

A large number of nonlinear dimensionality reduction techniques that aim to preserve the local structure of data have been proposed, many of which are reviewed by Lee and Verleysen (2007).
**データのlocal構造を保持することを目的とした非線形次元削減手法が数多く提案**されており、その多くはLee and Verleysen (2007)によってレビューされている。
In particular, we mention the following seven techniques: (1) Sammon mapping (Sammon, 1969), (2) curvilinear components analysis (CCA; Demartines and Herault, ´ 1997), (3) Stochastic Neighbor Embedding (SNE; Hinton and Roweis, 2002), (4) Isomap (Tenenbaum et al., 2000), (5) Maximum Variance Unfolding (MVU; Weinberger et al., 2004), (6) Locally Linear Embedding (LLE; Roweis and Saul, 2000), and (7) Laplacian Eigenmaps (Belkin and Niyogi, 2002).
特に以下の7つの技法を挙げる： (1) Sammon mapping (Sammon, 1969), (2) curvilinear components analysis (CCA; Demartines and Herault, ´ 1997), (3) Stochastic Neighbor Embedding (SNE; Hinton and Roweis, 2002), (4) Isomap (Tenenbaum et al、 2000）、(5) Maximum Variance Unfolding (MVU; Weinberger et al., 2004)、(6) Locally Linear Embedding (LLE; Roweis and Saul, 2000)、(7) Laplacian Eigenmaps (Belkin and Niyogi, 2002)がある。
Despite the strong performance of these techniques on artificial data sets, they are often not very successful at visualizing real, high-dimensional data.
これらの技術は人工的なデータセットでは高い性能を発揮するものの、実際の高次元データの可視化ではあまり成功しないことが多い。
In particular, most of the techniques are not capable of retaining both the local and the global structure of the data in a single map.
**特に、ほとんどの技術は、データのローカル構造とグローバル構造の両方を単一のマップに保持することができない**。
For instance, a recent study reveals that even a semi-supervised variant of MVU is not capable of separating handwritten digits into their natural clusters (Song et al., 2007).
例えば、最近の研究では、MVUの半教師付き変種でさえ、手書きの数字を自然なクラスターに分離できないことが明らかになった（Song et al, 2007）。

In this paper, we describe a way of converting a high-dimensional data set into a matrix of pairwise similarities and we introduce a new technique, called “t-SNE”, for visualizing the resulting similarity data.
本論文では、高次元データセットをペアごとの類似度行列に変換する方法を説明し、得られた類似度データを可視化するための「t-SNE」と呼ばれる新しい手法を紹介する。
t-SNE is capable of capturing much of the local structure of the high-dimensional data very well, while also revealing global structure such as the presence of clusters at several scales.
**t-SNEは、高次元データの局所的な構造の多くを非常によく捉えることができ、同時にいくつかのスケールにおけるクラスターの存在などの大域的な構造も明らかにすることができる。**
We illustrate the performance of t-SNE by comparing it to the seven dimensionality reduction techniques mentioned above on five data sets from a variety of domains.
我々は、様々なドメインからの5つのデータセット上で、上記の7つの次元削減技術と比較することにより、t-SNEの性能を説明する。
Because of space limitations, most of the (7+1)×5 = 40 maps are presented in the supplemental material, but the maps that we present in the paper are sufficient to demonstrate the superiority of t-SNE.
紙面の都合上、(7+1)×5＝40のマップの大半は補足資料に掲載したが、t-SNEの優位性を示すには、論文で紹介したマップで十分である。

The outline of the paper is as follows.
論文のアウトラインは以下の通り。
In Section 2, we outline SNE as presented by Hinton and Roweis (2002), which forms the basis for t-SNE.
セクション2では、t-SNEの基礎となるHinton and Roweis (2002)によるSNEについて概説する。
In Section 3, we present t-SNE, which has two important differences from SNE.
セクション3では、SNEとの2つの重要な違いを持つt-SNEを紹介する。
In Section 4, we describe the experimental setup and the results of our experiments.
セクション4では、実験セットアップと実験結果について述べる。
Subsequently, Section 5 shows how t-SNE can be modified to visualize realworld data sets that contain many more than 10,000 datapoints.
続いてセクション5では、10,000以上のデータポイントを含む実世界のデータセットを視覚化するために、t-SNEをどのように修正できるかを示す。
The results of our experiments are discussed in more detail in Section 6.
実験結果についてはセクション6で詳しく述べる。
Our conclusions and suggestions for future work are presented in Section 7.
結論と今後の課題についてはセクション7で述べる。

# 2. Stochastic Neighbor Embedding 確率的隣人埋め込み

Stochastic Neighbor Embedding (SNE) starts by converting the high-dimensional Euclidean distances between datapoints into conditional probabilities that represent similarities.
**確率的近傍埋め込み(SNE)は、データポイント間の高次元ユークリッド距離を、類似性を表す条件付き確率に変換する**ことから始まる。
The similarity of datapoint x j to datapoint xi is the conditional probability, p j|i , that xi would pick x j as its neighbor if neighbors were picked in proportion to their probability density under a Gaussian centered at xi .
データポイント $x_j$ のデータポイント $x_i$ への類似性は、$x_i$ を中心とするガウス分布の確率密度に比例して近傍が選択された場合に、$x_i$ が近傍として $x_j$ を選択する条件付き確率 $p_{j|i}$ である。
For nearby datapoints, pj|i is relatively high, whereas for widely separated datapoints, p j|i will be almost infinitesimal (for reasonable values of the variance of the Gaussian, σi).
近くのデータポイントでは、$p_{j|i}$ は比較的高く、離れたデータポイントでは、$p_{j|i}$ はほとんど無限小になる(ガウス分布の分散 $\sigma_i$ の妥当な値に対して)。
Mathematically, the conditional probability pj|i is given by
(ちなみに)数学的には、条件付き確率 $p_{j|i}$ は次式で与えられる。

$$
p_{i|j} = \frac{\exp(-\|x_i - x_j\|^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-\|x_i - x_k\|^2 / 2\sigma_i^2)}
\tag{1}
$$

where σi is the variance of the Gaussian that is centered on datapoint xi .
ここでσi はデータポイントxi を中心とするガウス分布の分散である。
The method for determining the value of σi is presented later in this section.
σiの値を決定する方法は、このセクションで後述する。
Because we are only interested in modeling pairwise similarities, we set the value of pi|i to zero.
ペアワイズの類似性をモデル化することに興味があるため、$p_{i|i}$ の値をゼロに設定する。
For the low-dimensional counterparts yi and y j of the high-dimensional datapoints xi and x j , it is possible to compute a similar conditional probability, which we denote by qj|i .
高次元データポイント$x_i$と$x_j$を**mappingした低次元対応 $y_i$ と$y_j$について、同様の条件付き確率$q_{j|i}$を計算することが可能である**。(うんうん...!)
We set the variance of the Gaussian that is employed in the computation of the conditional probabilities q j|i to √ 1 2 .
条件付き確率 $q_{j|i}$ の計算に使用されるガウス分布の分散を $1 / \sqrt{2}$ に設定する。
Hence, we model the similarity of map point y j to map point yi
したがって、圧縮後の**map point $y_i$ からmap point $y_j$ への類似性**を以下のようにモデル化する。

$$
q_{j|i} = \frac{\exp(-\|y_i - y_j\|^2)}{\sum_{k \neq i} \exp(-\|y_i - y_k\|^2)}
\tag{}
$$

Again, since we are only interested in modeling pairwise similarities, we set qi|i = 0.
再び、ペアワイズの類似性をモデル化することに興味があるため、$q_{i|i}$ の値をゼロに設定する。

If the map points yi and y j correctly model the similarity between the high-dimensional datapoints xi and x j , the conditional probabilities p j|i and qj|i will be equal.
**map point $y_i$ と$y_j$が高次元データポイント $x_i$ と $x_j$ の類似性を正しくモデル化している場合、条件付き確率 $p_{j|i}$ と $q_{j|i}$ は等しくなる。**(うんうん...!これが最適化の方向性か...!)
Motivated by this observation, SNE aims to find a low-dimensional data representation that minimizes the mismatch between pj|i and qj|i .
この観察に基づいて、SNEは、$p_{j|i}$ と $q_{j|i}$ の不一致を最小化する低次元データ表現を見つけることを目指す。
A natural measure of the faithfulness with which q j|i models pj|i is the KullbackLeibler divergence (which is in this case equal to the cross-entropy up to an additive constant).
**「$q_{j|i}$ が $p_{j|i}$ をどの程度忠実にモデル化しているか」の自然な尺度は、カルバック・ライブラー発散**（この場合、加法定数を除いてクロスエントロピーと等しい）である。
SNE minimizes the sum of Kullback-Leibler divergences over all datapoints using a gradient descent method.
SNEは、勾配降下法を用いて、**すべてのデータポイントのカルバック・ライブラー発散の和を最小化**する。
The cost function C is given by
コスト関数Cは次式で与えられる。(=loss function?)

$$
C = \sum_i KL(P_i || Q_i) = \sum_i \sum_j p_{j|i} \log \frac{p_{j|i}}{q_{j|i}}
\tag{2}
$$

in which Pi represents the conditional probability distribution over all other datapoints given datapoint xi , and Qi represents the conditional probability distribution over all other map points given map point yi .
ここで、$P_i$ はデータポイント $x_i$ が与えられたときの他のすべてのデータポイントに対する条件付き確率分布を表し、$Q_i$ はマップポイント $y_i$ が与えられたときの他のすべてのマップポイントに対する条件付き確率分布を表す。
Because the Kullback-Leibler divergence is not symmetric, different types of error in the pairwise distances in the low-dimensional map are not weighted equally.
**カルバック・ライブラー発散に対称性はないので(だよね!JSダイバージェンスはあるよ!)、低次元マップの対距離の異なるタイプの誤差は等しく重み付けされない**。(ここがSNEとt-SNEとの違いかな...??)
In particular, there is a large cost for using widely separated map points to represent nearby datapoints (i.e., for us a small qj|i to model a large pj|i ), but there is only a small cost for using nearby map points to represent widely separated datapoints.
特に、近くのデータポイントを表現するために離れたマップポイントを使用する場合（つまり、大きな $p_{j|i}$ をモデル化するために小さな $q_{j|i}$ を使用する場合）には、大きなコストが発生するが、離れたデータポイントを表現するために近くのマップポイントを使用する場合には、小さなコストしか発生しない。
This small cost comes from wasting some of the probability mass in the relevant Q distributions.
このわずかなコストは、**関連するQ分布の確率質量の一部を無駄にすること**に由来する。
In other words, the SNE cost function focuses on retaining the local structure of the data in the map (for reasonable values of the variance of the Gaussian in the high-dimensional space, σi).
**言い換えれば、SNEコスト関数は、（高次元空間におけるガウスの分散σiの妥当な値に対して）マップ内のデータの局所構造を保持することに重点を置く。** (高次元空間における正規分布の分散はハイパーパラメータか...!)

The remaining parameter to be selected is the variance σi of the Gaussian that is centered over each high-dimensional datapoint, xi .
選択すべき残りのパラメータは、各高次元データポイントxi を中心とするガウスの分散σi である。
It is not likely that there is a single value of σi that is optimal for all datapoints in the data set because the density of the data is likely to vary.
**データの密度は変化する可能性が高いため、データセット内のすべてのデータポイントに最適なσiの値が1つである可能性は低い。**(確かに...! 混雑してるエリアとそうでないエリア)
In dense regions, a smaller value of σi is usually more appropriate than in sparser regions.
密な領域では、通常、$\sigma_i$ の値が小さい方が、疎な領域よりも適している。
Any particular value of σi induces a probability distribution, Pi , over all of the other datapoints.
$\sigma_i$ の特定の値は、他のすべてのデータポイントに対する確率分布 $P_i$ を導く。
This distribution has an entropy which increases as σi increases.
この分布はエントロピー(=ばらつき??)を持ち、σiが増加するにつれて増加する。
SNE performs a binary search for the value of σi that produces a Pi with a fixed perplexity that is specified by the user.3 The perplexity is defined as
SNE は、ユーザーが指定したfixed perplexityを持つ $P_i$ を生成する $\sigma_i$ の値の2分探索を行う。ここで、perplexityは次式で定義される。

$$
Perp(P_i) = 2^{H(P_i)}
\tag{}
$$

where H(Pi) is the Shannon entropy of Pi measured in bits
ここで、H(Pi)はPiのシャノンエントロピー（ビット単位）である。

$$
H(P_i) = -\sum_j p_{j|i} \log_2 p_{j|i}
\tag{}
$$

The perplexity can be interpreted as a smooth measure of the effective number of neighbors.
**perplexityは、有効な近傍の数の滑らかな尺度として解釈することができる。**(smooth measureって"ざっくり"みたいなイメージ??)
The performance of SNE is fairly robust to changes in the perplexity, and typical values are between 5 and 50.
SNEの性能はperplexityの変化に対してかなり頑健であり、典型的な値は5から50の間である。
The minimization of the cost function in Equation 2 is performed using a gradient descent method.
式2のコスト関数の最小化は、勾配降下法を用いて行われる。
The gradient has a surprisingly simple form.
勾配は驚くほど単純な形をしている。

$$
\frac{\partial C}{\partial y_i} = 2 \sum_j (p_{j|i} - q_{j|i} + p_{i|j} - q_{i|j})(y_i - y_j)
\tag{}
$$

Physically, the gradient may be interpreted as the resultant force created by a set of springs between the map point yi and all other map points y j .
物理的には、勾配は、地図点 yi と他のすべての地図点 y j Fとの間のバネの集合によって生じる結果的な力として解釈することができる。(面白い...!)
All springs exert a force along the direction (yi −y j).
すべてのバネは $y_i - y_j$ の方向に力を及ぼす。
The spring between yi and y j repels or attracts the map points depending on whether the distance between the two in the map is too small or too large to represent the similarities between the two high-dimensional datapoints.
$y_i$ と $y_j$ の間のバネは、2つの高次元データポイントの類似性を表現するために、マップ上の距離が小さすぎるか大きすぎるかに応じて、マップポイントを引き離すか引き寄せる。
The force exerted by the spring between yi and y j is proportional to its length, and also proportional to its stiffness, which is the mismatch (p j|i −qj|i + pi| j −qi| j) between the pairwise similarities of the data points and the map points.
$y_i$ と $y_j$ の間のバネが及ぼす力は、**その長さに比例し、また、その硬さに比例する**。ここで、硬さは、データポイントとマップポイントのペアごとの類似性とマップポイントの不一致($p_{j|i} - q_{j|i} + p_{i|j} - q_{i|j}$)である。

The gradient descent is initialized by sampling map points randomly from an isotropic Gaussian with small variance that is centered around the origin.
勾配降下は、原点を中心とした小さな分散を持つ等方性ガウスからランダムにマップ点をサンプリングすることで初期化される。(確率的勾配降下法)
In order to speed up the optimization and to avoid poor local minima, a relatively large momentum term is added to the gradient.
最適化を高速化し、貧弱な局所極小値を避けるために、比較的大きな運動量項を勾配に加える。(これは局所最適解を避ける話か...!)
In other words, the current gradient is added to an exponentially decaying sum of previous gradients in order to determine the changes in the coordinates of the map points at each iteration of the gradient search.
言い換えれば、勾配探索の各反復におけるmap pointの座標の変化を決定するために、現在の勾配は、前の勾配の指数関数的に減衰する和に加えられる。
Mathematically, the gradient update with a momentum term is given by
数学的には、運動量項を持つ勾配更新は次式で与えられる。

$$
Y(t) = Y(t-1) + \eta \frac{\partial C}{\partial Y} + \alpha(t) (Y(t-1) - Y(t-2))
\tag{}
$$

where Y (t) indicates the solution at iteration t, η indicates the learning rate, and α(t) represents the momentum at iteration t.
ここで、$Y(t)$ は反復tでの解を示し、$\eta$ は学習率を示し、$\alpha(t)$ は反復tでの運動量を示す。

In addition, in the early stages of the optimization, Gaussian noise is added to the map points after each iteration.
さらに、最適化の初期段階では、各反復の後にmap pointにガウスノイズが加えられる。
Gradually reducing the variance of this noise performs a type of simulated annealing that helps the optimization to escape from poor local minima in the cost function.
このノイズの分散を徐々に小さくしていくことで、シミュレーテッド・アニーリングの一種が実行され、最適化がコスト関数の貧弱な局所極小値から脱出できるようになる。(最初は探索的に最適解を探していくよ！みたいなイメージ?)
If the variance of the noise changes very slowly at the critical point at which the global structure of the map starts to form, SNE tends to find maps with a better global organization.
マップの大域的な構造が形成され始める臨界点でノイズの分散が非常にゆっくりと変化する場合、SNEはより優れた大域的な構造を持つマップを見つける傾向がある。
Unfortunately, this requires sensible choices of the initial amount of Gaussian noise and the rate at which it decays.
残念なことに、これにはガウスノイズの初期量と減衰速度の適切な選択が必要である。(ハイパーパラメータか...!)
Moreover, these choices interact with the amount of momentum and the step size that are employed in the gradient descent.
さらに、これらの選択は、勾配降下で採用される運動量やステップサイズと相互作用する。
It is therefore common to run the optimization several times on a data set to find appropriate values for the parameters.4 In this respect, SNE is inferior to methods that allow convex optimization and it would be useful to find an optimization method that gives good results without requiring the extra computation time and parameter choices introduced by the simulated annealing.
したがって、パラメータの適切な値を見つけるために、データセット上で最適化を数回実行することは一般的である。
この点で、SNEは凸最適化を許可する方法に劣っており、シミュレーテッド・アニーリングによって導入された余分な計算時間とハイパーパラメータ選択を必要とせずに良い結果を与える最適化方法を見つけることは有用であるだろう。(これがt-SNEか...!)

# 3. t-Distributed Stochastic Neighbor Embedding t分布確率的隣接埋め込み

Section 2 discussed SNE as it was presented by Hinton and Roweis (2002).
セクション2では、Hinton and Roweis (2002)が提示したSNEについて論じた。
Although SNE constructs reasonably good visualizations, it is hampered by a cost function that is difficult to optimize and by a problem we refer to as the “crowding problem”.
**SNEはそれなりに優れたビジュアライゼーションを構築するが、最適化が難しいコスト関数と、われわれが「クラウディング問題」と呼ぶ問題によって妨げられている**。
In this section, we present a new technique called “t-Distributed Stochastic Neighbor Embedding” or “t-SNE” that aims to alleviate these problems.
このセクションでは、**これらの問題を軽減することを目的とした「t-Distributed Stochastic Neighbor Embedding」（t-SNE）と呼ばれる新しい手**法を紹介する。
The cost function used by t-SNE differs from the one used by SNE in two ways: (1) it uses a symmetrized version of the SNE cost function with simpler gradients that was briefly introduced by Cook et al.(2007) and (2) it uses a Student-t distribution rather than a Gaussian to compute the similarity between two points in the low-dimensional space.
t-SNEで使用されるコスト関数は、SNEで使用されるものとは2つの点で異なる：(1)Cookら(2007)によって簡単に紹介された、より単純な勾配を持つSNEコスト関数の対称化バージョンを使用すること、(2)低次元空間における2点間の類似度を計算するために、ガウス分布ではなくスチューデントt分布を使用すること、である。
t-SNE employs a heavy-tailed distribution in the low-dimensional space to alleviate both the crowding problem and the optimization problems of SNE.
t-SNEは、SNEの混雑問題と最適化問題の両方を軽減するために、低次元空間における重尾分布を採用している。
In this section, we first discuss the symmetric version of SNE (Section 3.1).
このセクションでは、まずSNEの対称バージョンについて説明する（セクション3.1）。
Subsequently, we discuss the crowding problem (Section 3.2), and the use of heavy-tailed distributions to address this problem (Section 3.3).
続いて、混雑問題（セクション3.2）と、この問題に対処するための重尾部分布の使用（セクション3.3）について議論する。
We conclude the section by describing our approach to the optimization of the t-SNE cost function (Section 3.4).3.1 Symmetric SNE As an alternative to minimizing the sum of the Kullback-Leibler divergences between the conditional probabilities pj|i and qj|i , it is also possible to minimize a single Kullback-Leibler divergence between a joint probability distribution, P, in the high-dimensional space and a joint probability distribution, Q, in the low-dimensional space:
i and qj

$$
\tag{}
$$

where again, we set pii and qii to zero.
ここでもpiiとqiiをゼロとする。
We refer to this type of SNE as symmetric SNE, because it has the property that pi j = pji and qi j = qji for ∀i, j.
このタイプのSNEは、∀i, jに対してpi j = pji、qi j = qjiという性質を持つため、対称SNEと呼ぶ。
In symmetric SNE, the pairwise similarities in the low-dimensional map qi j are given by
対称SNEでは、低次元写像qi jにおける対の類似度は次式で与えられる。

$$
\tag{3}
$$

The obvious way to define the pairwise similarities in the high-dimensional space pi j is
高次元空間pi jにおける一対の類似性を定義する明白な方法は次の通りである。

$$
\tag{}
$$

but this causes problems when a high-dimensional datapoint xi is an outlier (i.e., all pairwise distances kxi − x jk 2 are large for xi).
しかしこれは、高次元のデータポイントxiが外れ値である場合（すなわち、すべての対距離kxi - x jk 2がxiに対して大きい場合）に問題を引き起こす。
For such an outlier, the values of pi j are extremely small for all j, so the location of its low-dimensional map point yi has very little effect on the cost function.
このような異常値では、pi jの値はすべてのjに対して極めて小さいので、その低次元の地図点yiの位置はコスト関数にほとんど影響しない。
As a result, the position of the map point is not well determined by the positions of the other map points.
その結果、地図点の位置は他の地図点の位置によってうまく決定されない。
We circumvent this problem by defining the joint probabilities pi j in the high-dimensional space to be the symmetrized conditional probabilities, that is, we set pi j = pj|i+pi| j 2n .
i+pi
This ensures that ∑j pi j > 1 2n for all datapoints xi , as a result of which each datapoint xi makes a significant contribution to the cost function.
これにより、すべてのデータポイント xi に対して、∑j pi j > 1 2n が保証され、その結果、各データポイント xi はコスト関数に大きく寄与する。
In the low-dimensional space, symmetric SNE simply uses Equation 3.
低次元空間では、対称SNEは単に式3を使用する。
The main advantage of the symmetric version of SNE is the simpler form of its gradient, which is faster to compute.
対称版SNEの主な利点は、勾配の形が単純で、計算が速いことである。
The gradient of symmetric SNE is fairly similar to that of asymmetric SNE, and is given by
対称SNEの勾配は非対称SNEの勾配とよく似ており、次式で与えられる。

$$
\tag{}
$$

In preliminary experiments, we observed that symmetric SNE seems to produce maps that are just as good as asymmetric SNE, and sometimes even a little better.
予備的な実験では、対称SNEは非対称SNEと同じくらい良いマップを生成し、時には少し良いマップを生成することさえあるようだ。

## 3.1. The Crowding Problem

Consider a set of datapoints that lie on a two-dimensional curved manifold which is approximately linear on a small scale, and which is embedded within a higher-dimensional space.
小さなスケールでほぼ線形であり、高次元空間に埋め込まれた2次元曲線多様体上にあるデータポイントの集合を考える。
It is possible to model the small pairwise distances between datapoints fairly well in a two-dimensional map, which is often illustrated on toy examples such as the “Swiss roll” data set.
データポイント間の小さなペア間距離を2次元マップの中でかなりうまくモデル化することが可能で、これは「スイスロール」データセットのようなおもちゃの例でよく説明される。
Now suppose that the manifold has ten intrinsic dimensions5 and is embedded within a space of much higher dimensionality.
ここで、この多様体が10次元の固有次元5を持ち、もっと高次元の空間に埋め込まれているとしよう。
There are several reasons why the pairwise distances in a two-dimensional map cannot faithfully model distances between points on the ten-dimensional manifold.
二次元マップの対距離では、10次元多様体上の点間距離を忠実にモデル化できない理由はいくつかある。
For instance, in ten dimensions, it is possible to have 11 datapoints that are mutually equidistant and there is no way to model this faithfully in a two-dimensional map.
例えば、10次元の場合、互いに等距離にある11個のデータポイントが存在する可能性があり、これを2次元の地図で忠実にモデル化する方法はない。
A related problem is the very different distribution of pairwise distances in the two spaces.
関連する問題は、2つの空間における対距離の分布が大きく異なることである。
The volume of a sphere centered on datapoint i scales as r m, where r is the radius and m the dimensionality of the sphere.
データポイントiを中心とする球の体積はr mとしてスケールし、rは半径、mは球の次元数である。
So if the datapoints are approximately uniformly distributed in the region around i on the ten-dimensional manifold, and we try to model the distances from i to the other datapoints in the two-dimensional map, we get the following “crowding problem”: the area of the two-dimensional map that is available to accommodate moderately distant datapoints will not be nearly large enough compared with the area available to accommodate nearby datapoints.
そこで、データポイントが10次元多様体上のiの周りの領域にほぼ一様に分布しているとして、iから他のデータポイントまでの距離を2次元マップ上でモデル化しようとすると、次のような「混雑問題」が発生する： ほどよく離れたデータポイントを収容できる二次元マップの領域は、近くのデータポイントを収容できる領域と比べると、ほとんど十分な大きさにならない。
Hence, if we want to model the small distances accurately in the map, most of the points that are at a moderate distance from datapoint i will have to be placed much too far away in the two-dimensional map.
したがって、地図上で小さな距離を正確にモデル化しようとすれば、データポイントiから中程度の距離にある点のほとんどは、二次元地図上ではかなり遠くに配置しなければならない。
In SNE, the spring connecting datapoint i to each of these too-distant map points will thus exert a very small attractive force.
SNEでは、データ点iとこれらの遠すぎる地図点のそれぞれを結ぶバネは、このように非常に小さな吸引力を発揮する。
Although these attractive forces are very small, the very large number of such forces crushes together the points in the center of the map, which prevents gaps from forming between the natural clusters.
これらの引力は非常に小さいが、このような力の数が非常に多いため、マップの中心にある点同士が押しつぶされ、自然のクラスター間に隙間ができるのを防ぐことができる。
Note that the crowding problem is not specific to SNE, but that it also occurs in other local techniques for multidimensional scaling such as Sammon mapping.
クラウディング問題はSNEに特有の問題ではなく、サモン・マッピングのような多次元スケーリングの他の局所的手法でも発生することに注意。
An attempt to address the crowding problem by adding a slight repulsion to all springs was presented by Cook et al.(2007).
すべてのバネにわずかな反発力を加えることで、クラウディング問題に対処する試みがCookら（2007）によって発表された。
The slight repulsion is created by introducing a uniform background model with a small mixing proportion, ρ.
わずかな斥力は、混合割合ρが小さい一様な背景モデルを導入することによって生じる。
So however far apart two map points are, qi j can never fall below 2ρ n(n−1) (because the uniform background distribution is over n(n−1)/2 pairs).
そのため、2つの写像点がどんなに離れていても、qi jが2ρ n(n-1)を下回ることはない（一様な背景分布がn(n-1)/2組に及ぶため）。
As a result, for datapoints that are far apart in the high-dimensional space, qi j will always be larger than pi j , leading to a slight repulsion.
その結果、高次元空間で離れたデータポイントの場合、qi jは常にpi jより大きくなり、わずかな反発が生じる。
This technique is called UNI-SNE and although it usually outperforms standard SNE, the optimization of the UNI-SNE cost function is tedious.
この手法はUNI-SNEと呼ばれ、通常、標準的なSNEよりも優れているが、UNI-SNEのコスト関数の最適化は面倒である。
The best optimization method known is to start by setting the background mixing proportion to zero (i.e., by performing standard SNE).
知られている最良の最適化方法は、バックグラウンドの混合比率をゼロに設定することから始めることである（すなわち、標準的なSNEを実行すること）。
Once the SNE cost function has been optimized using simulated annealing, the background mixing proportion can be increased to allow some gaps to form between natural clusters as shown by Cook et al.(2007).
SNEコスト関数がシミュレーテッドアニーリングを用いて最適化されると、Cookら(2007)が示したように、バックグラウンドの混合比率を高めて、自然のクラスター間にギャップが形成されるようにすることができる。
Optimizing the UNI-SNE cost function directly does not work because two map points that are far apart will get almost all of their qi j from the uniform background.
UNI-SNEコスト関数を直接最適化してもうまくいかないのは、離れた2つの地図点はそのqi jのほとんどすべてを一様な背景から得てしまうからである。
So even if their pi j is large, there will be no attractive force between them, because a small change in their separation will have a vanishingly small proportional effect on qi j .
そのため、たとえπ j が大きくても、両者の間に引力は生じない。なぜなら、両者の距離のわずかな変化は、qi j に及ぼす比例効果が極端に小さいからである。
This means that if two parts of a cluster get separated early on in the optimization, there is no force to pull them back together.3.3 Mismatched Tails can Compensate for Mismatched Dimensionalities Since symmetric SNE is actually matching the joint probabilities of pairs of datapoints in the highdimensional and the low-dimensional spaces rather than their distances, we have a natural way of alleviating the crowding problem that works as follows.
3.3 Mismatched Tails can compensate for Mismatched Dimensionalities 対称SNEは、実際には、高次元空間と低次元空間におけるデータポ イントのペアの結合確率のマッチングであり、それらの距離のマッチング ではないので、混雑問題を緩和する自然な方法がある。
In the high-dimensional space, we convert distances into probabilities using a Gaussian distribution.
高次元空間では、ガウス分布を使って距離を確率に変換する。
In the low-dimensional map, we can use a probability distribution that has much heavier tails than a Gaussian to convert distances into probabilities.
低次元マップでは、距離を確率に変換するために、ガウス分布よりもずっと重いテールを持つ確率分布を使うことができる。
This allows a moderate distance in the high-dimensional space to be faithfully modeled by a much larger distance in the map and, as a result, it eliminates the unwanted attractive forces between map points that represent moderately dissimilar datapoints.
これにより、高次元空間における適度な距離が、マップにおけるはるかに大きな距離によって忠実にモデル化され、その結果、適度に異なるデータポイントを表すマップポイント間の不要な引力が排除される。
In t-SNE, we employ a Student t-distribution with one degree of freedom (which is the same as a Cauchy distribution) as the heavy-tailed distribution in the low-dimensional map.
t-SNEでは、低次元写像の重尾部分布として、自由度1のスチューデントt分布（コーシー分布と同じ）を採用する。
Using this distribution, the joint probabilities qi j are defined as
この分布を用いると、結合確率qi jは次のように定義される。

$$
\tag{4}
$$

We use a Student t-distribution with a single degree of freedom, because it has the particularly nice property that 1+kyi −y jk 2 −1 approaches an inverse square law for large pairwise distances kyi − y jk in the low-dimensional map.
これは、低次元の写像において、1+kyi -y jk 2 -1が大きな対の距離kyi - y jkに対して逆2乗則に近づくという、特に優れた性質を持っているからである。
This makes the map’s representation of joint probabilities (almost) invariant to changes in the scale of the map for map points that are far apart.
これによって、地図上の結合確率の表現は、地図上の点が離れている場合、地図の縮尺の変化に対して（ほぼ）不変となる。
It also means that large clusters of points that are far apart interact in just the same way as individual points, so the optimization operates in the same way at all but the finest scales.
また、離れた点の大きなクラスターも個々の点と同じように相互作用するため、最適化は最も細かいスケール以外ではすべて同じように動作する。
A theoretical justification for our selection of the Student t-distribution is that it is closely related to the Gaussian distribution, as the Student t-distribution is an infinite mixture of Gaussians.
スチューデントt分布を選択する理論的な正当性は、スチューデントt分布がガウシアンの無限混合分布であるように、それがガウシアン分布と密接に関連していることである。
A computationally convenient property is that it is much faster to evaluate the density of a point under a Student t-distribution than under a Gaussian because it does not involve an exponential, even though the Student t-distribution is equivalent to an infinite mixture of Gaussians with different variances.
計算上便利な特性は、スチューデントt分布は、異なる分散を持つガウシアンの無限混合分布と等価であるにもかかわらず、指数関数が含まれないため、ガウシアンよりもスチューデントt分布の下で点の密度を評価する方がはるかに速いということである。
The gradient of the Kullback-Leibler divergence between P and the Student-t based joint probability distribution Q (computed using Equation 4) is derived in Appendix A, and is given by
PとStudent-tに基づく結合確率分布Q（式4を用いて計算）の間のカルバック・ライブラー発散の勾配は、付録Aで導出され、次式で与えられる。

$$
\tag{5}
$$

In Figure 1(a) to 1(c), we show the gradients between two low-dimensional datapoints yi and y j as a function of their pairwise Euclidean distances in the high-dimensional and the low-dimensional space (i.e., as a function of kxi −x jk and kyi −y jk) for the symmetric versions of SNE, UNI-SNE, and t-SNE.
図1(a)～(c)では、SNE、UNI-SNE、t-SNEの対称バージョンについて、2つの低次元データポイントyiとy jの間の勾配を、高次元空間と低次元空間における対のユークリッド距離の関数として（すなわち、kxi -x jkとkyi -y jkの関数として）示している。
In the figures, positive values of the gradient represent an attraction between the lowdimensional datapoints yi and y j , whereas negative values represent a repulsion between the two datapoints.
図では、勾配の正の値は低次元のデータポイント yi と y j の間の引力を表し、負の値は2つのデータポイント間の反発を表す。
From the figures, we observe two main advantages of the t-SNE gradient over the gradients of SNE and UNI-SNE.
図から、SNEやUNI-SNEの勾配に対するt-SNEの勾配の2つの主な利点が観察される。
First, the t-SNE gradient strongly repels dissimilar datapoints that are modeled by a small pairwise distance in the low-dimensional representation.
第一に、t-SNE勾配は、低次元表現において小さな対距離でモデル化される異種データポイントを強く反発する。
SNE has such a repulsion as well, but its effect is minimal compared to the strong attractions elsewhere in the gradient (the largest attraction in our graphical representation of the gradient is approximately 19, whereas the largest repulsion is approximately 1).
SNEにもそのような斥力があるが、勾配内の他の場所にある強い引力と比べると、その影響はごくわずかである（勾配のグラフ表現における最大の引力は約19であるのに対し、最大の斥力は約1である）。
In UNI-SNE, the amount of repulsion between dissimilar datapoints is slightly larger, however, this repulsion is only strong when the pairwise distance between the points in the lowdimensional representation is already large (which is often not the case, since the low-dimensional representation is initialized by sampling from a Gaussian with a very small variance that is centered around the origin).
UNI-SNEでは、非類似のデータポイント間の反発は若干大きくなるが、この反発が強くなるのは、低次元表現におけるポイント間のペアワイズ距離がすでに大きい場合のみである（低次元表現は、原点を中心とする非常に小さな分散を持つガウスからのサンプリングによって初期化されるため、多くの場合そうではない）。
Second, although t-SNE introduces strong repulsions between dissimilar datapoints that are modeled by small pairwise distances, these repulsions do not go to infinity.
第二に、t-SNEは、小さな対距離によってモデル化される異種データポイント間に強い反発を導入するが、これらの反発は無限大にはならない。
In this respect, t-SNE differs from UNI-SNE, in which the strength of the repulsion between very dissimilar datapoints is proportional to their pairwise distance in the low-dimensional map, which may cause dissimilar datapoints to move much too far away from each other.
この点で、t-SNEはUNI-SNEとは異なり、非常に異質なデータポイント間の反発の強さは、低次元マップにおける対の距離に比例するため、異質なデータポイントが互いに大きく離れてしまう可能性がある。
Taken together, t-SNE puts emphasis on (1) modeling dissimilar datapoints by means of large pairwise distances, and (2) modeling similar datapoints by means of small pairwise distances.
t-SNEは、(1)大きな対距離によって非類似のデータポイントをモデル化し、(2)小さな対距離によって類似のデータポイントをモデル化することに重点を置いている。
Moreover, as a result of these characteristics of the t-SNE cost function (and as a result of the approximate scale invariance of the Student t-distribution), the optimization of the t-SNE cost function is much easier than the optimization of the cost functions of SNE and UNI-SNE.
さらに、t-SNEコスト関数のこれらの特徴の結果として（そしてスチューデントt分布の近似的なスケール不変性の結果として）、t-SNEコスト関数の最適化は、SNEやUNI-SNEのコスト関数の最適化よりもはるかに簡単です。
Specifically, t-SNE introduces long-range forces in the low-dimensional map that can pull back together two (clusters of) similar points that get separated early on in the optimization.
具体的には、t-SNEは低次元のマップに長距離の力を導入し、最適化の初期段階で分離してしまった2つの（類似した点の）クラスターを引き戻すことができる。
SNE and UNI-SNE do not have such long-range forces, as a result of which SNE and UNI-SNE need to use simulated annealing to obtain reasonable solutions.
SNEとUNI-SNEはこのような長距離力を持たないため、妥当な解を得るためにはシミュレーテッド・アニーリングを使用する必要がある。
Instead, the long-range forces in t-SNE facilitate the identification of good local optima without resorting to simulated annealing.
その代わりに、t-SNEの長距離力は、シミュレーテッド・アニーリングに頼ることなく、良好な局所最適値の同定を容易にする。

## 3.2. Optimization Methods for t-SNE t-SNEの最適化手法

We start by presenting a relatively simple, gradient descent procedure for optimizing the t-SNE cost function.
まず、t-SNEコスト関数を最適化するための、比較的単純な勾配降下法を紹介する。
This simple procedure uses a momentum term to reduce the number of iterations required and it works best if the momentum term is small until the map points have become moderately well organized.
この単純な手順は、必要な反復回数を減らすために運動量項を使用し、マップポイントが適度に整理されるまで運動量項が小さい場合に最適に機能する。
Pseudocode for this simple algorithm is presented in Algorithm 1.
この単純なアルゴリズムのシュードコードをアルゴリズム1に示す。
The simple algorithm can be sped up using the adaptive learning rate scheme that is described by Jacobs (1988), which gradually increases the learning rate in directions in which the gradient is stable.
この単純なアルゴリズムは、Jacobs (1988)によって説明されている適応学習率スキームを用いて高速化することができ、勾配が安定している方向で学習率を徐々に増加させる。
Although the simple algorithm produces visualizations that are often much better than those produced by other non-parametric dimensionality reduction techniques, the results can be improved further by using either of two tricks.
このシンプルなアルゴリズムは、しばしば他のノンパラメトリック次元削減テクニックによって生成されるものよりもはるかに優れた可視化を生成するが、結果は2つのトリックのいずれかを使用することによってさらに改善することができる。
The first trick, which we call “early compression”, is to force the map points to stay close together at the start of the optimization.
私たちが "early compression "と呼んでいる最初のトリックは、最適化の開始時に地図上の点を強制的に近づけることである。
When the distances between map points are small, it is easy for clusters to move through one another so it is much easier to explore the space of possible global organizations of the data.
地図上のポイント間の距離が小さいと、クラスターが互いに移動しやすくなるため、データのグローバルな組織の可能性を探るのがより簡単になる。
Early compression is implemented by adding an additional L2-penalty to the cost function that is proportional to the sum of square distances of the map points from the origin.
早期圧縮は、原点からの地図点の二乗距離の和に比例するL2-ペナルティをコスト関数に追加することで実装される。
The magnitude of this penalty term and the iteration at which it is removed are set by hand, but the behavior is fairly robust across variations in these two additional optimization parameters.
このペナルティ項の大きさと、それを除去する反復は手作業で設定されるが、この2つの追加最適化パラメータの変動に対して挙動はかなりロバストである。
A less obvious way to improve the optimization, which we call “early exaggeration”, is to multiply all of the pi j’s by, for example, 4, in the initial stages of the optimization.
最適化を改善するあまり明白でない方法は、私たちが「初期誇張」と呼んでいるもので、最適化の初期段階で、すべてのπjを例えば4倍することです。
This means that almost all of the qi j’s, which still add up to 1, are much too small to model their corresponding pi j’s.
つまり、ほとんどすべてのqi jは、それでも足して1になるが、対応するpi jをモデル化するには小さすぎる。
As a result, the optimization is encouraged to focus on modeling the large pi j’s by fairly large qi j’s.
その結果、最適化は、かなり大きなqi jによって大きなpi jをモデル化することに集中することが推奨される。
The effect is that the natural clusters in the data tend to form tight widely separated clusters in the map.
その結果、データ中の自然なクラスターは、地図上では大きく離れた狭いクラスターを形成する傾向がある。
This creates a lot of relatively empty space in the map, which makes it much easier for the clusters to move around relative to one another in order to find a good global organization.
これによって、地図上に比較的空白のスペースが多くでき、クラスターが互いに相対的に移動しやすくなる。
In all the visualizations presented in this paper and in the supporting material, we used exactly the same optimization procedure.
本稿および補足資料で紹介するすべての可視化において、まったく同じ最適化手順を使用した。
We used the early exaggeration method with an exaggeration of 4 for the first 50 iterations (note that early exaggeration is not included in the pseudocode in Algorithm 1).
最初の50回の反復では、誇張度4の早期誇張法を使用した（早期誇張法はアルゴリズム1の擬似コードには含まれていないことに注意）。
The number of gradient descent iterations T was set 1000, and the momentum term was set to α (t) = 0.5 for t < 250 and α (t) = 0.8 for t ≥ 250.
勾配降下の反復回数Tは1000回とし、運動量項はt<250の場合はα(t)=0.5、t≧250の場合はα(t)=0.8とした。
The learning rate η is initially set to 100 and it is updated after every iteration by means of the adaptive learning rate scheme described by Jacobs (1988).
学習率ηは初期値として100に設定され、Jacobs (1988)に記述された適応学習率スキームによって反復毎に更新される。
A Matlab implementation of the resulting algorithm is available at http://ticc.
結果のアルゴリズムのMatlab実装はhttp://ticc。
uvt.nl/˜lvdrmaaten/tsne.
uvt.nl/ 〜lvdrmaaten/tsne.

# 4. Experiments 実験

To evaluate t-SNE, we present experimentsin which t-SNE is compared to seven other non-parametric techniques for dimensionality reduction.
t-SNEを評価するために、t-SNEを他の7つのノンパラメトリック次元削減手法と比較する実験を行う。
Because of space limitations, in the paper, we only compare t-SNE with: (1) Sammon mapping, (2) Isomap, and (3) LLE.
紙面の都合上、本稿ではt-SNEとの比較のみを行う： (1)サモンマッピング、(2)アイソマップ、(3)LLE。
In the supporting material, we also compare t-SNE with: (4) CCA, (5) SNE, (6) MVU, and (7) Laplacian Eigenmaps.
補足資料では、t-SNEも比較している： (4)CCA、(5)SNE、(6)MVU、(7)ラプラシアン固有マップ。
We performed experiments on five data sets that represent a variety of application domains.
様々なアプリケーション・ドメインを代表する5つのデータセットで実験を行った。
Again because of space limitations, we restrict ourselves to three data sets in the paper.
ここでも紙面の都合上、3つのデータセットに限定した。
The results of our experiments on the remaining two data sets are presented in the supplemental material.
残りの2つのデータセットに関する実験結果は、補足資料に掲載されている。
In Section 4.1, the data sets that we employed in our experiments are introduced.
セクション4.1では、実験に使用したデータセットを紹介する。
The setup of the experimentsis presented in Section 4.2.In Section 4.3, we present the results of our experiments.4.1 Data Sets The five data sets we employed in our experiments are: (1) the MNIST data set, (2) the Olivetti faces data set, (3) the COIL-20 data set, (4) the word-features data set, and (5) the Netflix data set.
セクション4.3では、実験結果を示す。4.1 データセット 実験に使用したデータセットは以下の5つである： (1) MNIST データセット、(2) Olivetti faces データセット、(3) COIL-20 データセット、(4) word-features データセット、(5) Netflix データセットである。
We only present results on the first three data sets in this section.
このセクションでは、最初の3つのデータセットについての結果のみを紹介する。
The results on the remaining two data sets are presented in the supporting material.
残りの2つのデータセットに関する結果は、補足資料に記載されている。
The first three data sets are introduced below.
最初の3つのデータセットを以下に紹介する。
The MNIST data set6 contains 60,000 grayscale images of handwritten digits.
MNISTデータセット6には、6万枚の手書き数字のグレースケール画像が含まれている。
For our experiments, we randomly selected 6,000 of the images for computational reasons.
実験では、計算上の理由から6,000枚の画像を無作為に選んだ。
The digit images have 28×28 = 784 pixels (i.e., dimensions).
桁の画像は28×28＝784ピクセル（＝寸法）。
The Olivetti faces data set7 consists of images of 40 individuals with small variations in viewpoint, large variations in expression, and occasional addition of glasses.
オリベッティの顔データセット7は、40人の画像から構成されており、視点が微妙に変化し、表情が大きく変化し、メガネをかけることもある。
The data set consists of 400 images (10 per individual) of size 92×112 = 10,304 pixels, and is labeled according to identity.
データセットは、サイズ92×112＝10,304ピクセルの画像400枚（1人当たり10枚）からなり、同一性に応じてラベル付けされている。
The COIL-20 data set (Nene et al., 1996) contains images of 20 different objects viewed from 72 equally spaced orientations, yielding a total of 1,440 images.
COIL-20データセット（Nene et al, 1996）には、20種類の物体を72の等間隔な方向から見た画像が含まれており、合計1,440枚の画像がある。
The images contain 32×32 = 1,024 pixels.4.2 Experimental Setup In all of our experiments, we start by using PCA to reduce the dimensionality of the data to 30.
4.2 実験セットアップ すべての実験において、まずPCAを使ってデータの次元を30に減らす。
This speeds up the computation of pairwise distances between the datapoints and suppresses some noise without severely distorting the interpoint distances.
これにより、データポイント間のペアワイズ距離の計算が高速化され、ポイント間距離を大きく歪めることなく、ノイズがある程度抑制される。
We then use each of the dimensionality reduction techniques to convert the 30-dimensional representation to a two-dimensional map and we show the resulting map as a scatterplot.
次に、それぞれの次元削減技術を用いて30次元の表現を2次元のマップに変換し、その結果のマップを散布図として示す。
For all of the data sets, there is information about the class of each datapoint, but the class information is only used to select a color and/or symbol for the map points.
すべてのデータセットについて、各データポイントのクラスに関する情報があるが、クラス情報は地図ポイントの色や記号を選択するためにのみ使用される。
The class information is not used to determine the spatial coordinates of the map points.
クラス情報は、地図ポイントの空間座標を決定するためには使用されない。
The coloring thus provides a way of evaluating how well the map preserves the similarities within each class.
このように色付けは、マップが各クラス内の類似性をどの程度保存しているかを評価する方法を提供する。
The cost function parameter settings we employed in our experiments are listed in Table 1.
実験で採用したコスト関数のパラメータ設定を表1に示す。
In the table, Perp represents the perplexity of the conditional probability distribution induced by a Gaussian kernel and k represents the number of nearest neighbors employed in a neighborhood graph.
表中、Perpはガウシアンカーネルによって誘導される条件付き確率分布の当惑度を表し、kは近傍グラフで採用される最近傍の数を表す。
In the experiments with Isomap and LLE, we only visualize datapoints that correspond to vertices in the largest connected component of the neighborhood graph.8 For the Sammon mapping optimization, we performed Newton’s method for 500 iterations.4.3 Results In Figures 2 and 3, we show the results of our experiments with t-SNE, Sammon mapping, Isomap, and LLE on the MNIST data set.
IsomapとLLEの実験では、近傍グラフの最大連結成分に含まれる頂点に対応するデータポイントのみを可視化した8。4.3 結果 図2と図3に、MNISTデータセットに対するt-SNE、Sammon mapping、Isomap、LLEの実験結果を示す。
The results reveal the strong performance of t-SNE compared to the other techniques.
その結果、t-SNEが他の手法に比べて強力な性能を持つことが明らかになった。
In particular, Sammon mapping constructs a “ball” in which only three classes (representing the digits 0, 1, and 7) are somewhat separated from the other classes.
特に、サモンマッピングは、3つのクラス（数字の0、1、7を表す）だけが他のクラスから多少離れている「ボール」を構成する。
Isomap and LLE produce solutions in which there are large overlaps between the digit classes.
IsomapとLLEは、桁クラス間に大きな重複がある解を生成する。
In contrast, tSNE constructs a map in which the separation between the digit classes is almost perfect.
対照的に、tSNEは桁クラス間の分離がほぼ完全な写像を構築する。
Moreover, detailed inspection of the t-SNE map reveals that much of the local structure of the data (such as the orientation of the ones) is captured as well.
さらに、t-SNEマップを詳細に観察すると、データの局所的な構造（ものの向きなど）の多くも捉えられていることがわかる。
This is illustrated in more detail in Section 5 (see Figure 7).
これはセクション5で詳しく説明されている（図7参照）。
The map produced by t-SNE contains some points that are clustered with the wrong class, but most of these points correspond to distorted digits many of which are difficult to identify.
t-SNEによって作成されたマップには、間違ったクラスにクラスタリングされた点がいくつか含まれているが、これらの点のほとんどは、識別が困難な歪んだ数字の多くに対応している。
Figure 4 shows the results of applying t-SNE, Sammon mapping, Isomap, and LLE to the Olivetti faces data set.
図4は、オリベッティの顔データセットにt-SNE、サモンマッピング、アイソマップ、LLEを適用した結果を示している。
Again, Isomap and LLE produce solutions that provide little insight into the class structure of the data.
ここでも、IsomapとLLEは、データのクラス構造をほとんど理解できない解を出す。
The map constructed by Sammon mapping is significantly better, since it models many of the members of each class fairly close together, but none of the classes are clearly separated in the Sammon map.
サモンマッピングで作成されたマップは、各クラスのメンバーの多くをかなり近くにモデル化しているため、かなり優れているが、サモンマップではどのクラスも明確に分離されていない。
In contrast, t-SNE does a much better job of revealing the natural classes in the data.
対照的に、t-SNEはデータ中の自然なクラスを明らかにするのに非常に優れている。
Some individuals have their ten images split into two clusters, usually because a subset of the images have the head facing in a significantly different direction, or because they have a very different expression or glasses.
10枚の画像が2つのクラスターに分かれている人もいるが、これは通常、画像の一部で頭の向きが大きく異なっていたり、表情や眼鏡のかけ方が大きく異なっていたりするためである。
For these individuals, it is not clear that their ten images form a natural class when using Euclidean distance in pixel space.
画素空間のユークリッド距離を使用する場合、これらの人々の10枚の画像が自然なクラスを形成していることは明らかではない。
Figure 5 shows the results of applying t-SNE, Sammon mapping, Isomap, and LLE to the COIL20 data set.
図5は、COIL20データセットにt-SNE、サモンマッピング、アイソマップ、LLEを適用した結果を示している。
For many of the 20 objects, t-SNE accurately represents the one-dimensional manifold of viewpoints as a closed loop.
20のオブジェクトの多くについて、t-SNEは視点の一次元多様体を閉ループとして正確に表現する。
For objects which look similar from the front and the back, t-SNE distorts the loop so that the images of front and back are mapped to nearby points.
t-SNEは、表と裏が似ているオブジェクトに対して、表と裏のイメージが近くの点にマッピングされるようにループを歪める。
For the four types of toy car in the COIL-20 data set (the four aligned “sausages” in the bottom-left of the tSNE map), the four rotation manifolds are aligned by the orientation of the cars to capture the high similarity between different cars at the same orientation.
COIL-20データセットに含まれる4種類のおもちゃの車（tSNEマップの左下にある4つの整列した「ソーセージ」）については、4つの回転多様体が車の向きによって整列され、同じ向きで異なる車の間の高い類似性を捉える。
This prevents t-SNE from keeping the four manifolds clearly separate.
このため、t-SNEは4つのマニホールドを明確に分けることができない。
Figure 5 also reveals that the other three techniques are not nearly as good at cleanly separating the manifolds that correspond to very different objects.
図5はまた、他の3つの技法が、非常に異なるオブジェクトに対応する多様体をきれいに分離することに、ほとんど長けていないことを明らかにしている。
In addition, Isomap and LLE only visualize a small number of classes from the COIL-20 data set, because the data set comprises a large number of widely separated submanifolds that give rise to small connected components in the neighborhood graph.
さらに、IsomapとLLEは、COIL-20データセットから少数のクラスしか可視化しない。これは、データセットが近傍グラフの小さな連結成分を生じさせる多数の広く分離した部分多様体から構成されているためである。

# 5. Applying t-SNE to Large Data Sets 大規模データセットへのt-SNEの適用

Applying t-SNE to Large Data Sets Like many other visualization techniques, t-SNE has a computational and memory complexity that is quadratic in the number of datapoints.
大規模データセットへのt-SNEの適用 他の多くの可視化技術と同様に、t-SNEはデータポイント数の2次関数的な計算量とメモリ複雑度を持つ。
This makes it infeasible to apply the standard version of t-SNE to data sets that contain many more than, say, 10,000 points.
このため、標準版のt-SNEを、例えば10,000点以上の点を含むデータセットに適用することは不可能である。
Obviously, it is possible to pick a random subset of the datapoints and display them using t-SNE, but such an approach fails to make use of the information that the undisplayed datapoints provide about the underlying manifolds.
もちろん、データポイントの無作為な部分集合を選び、t-SNEを使って表示することは可能だが、そのようなアプローチでは、表示されていないデータポイントが提供する基礎となる多様体に関する情報を利用することができない。
Suppose, for example, that A, B, and C are all equidistant in the high-dimensional space.
例えば、A、B、Cがすべて高次元空間で等距離にあるとする。
If there are many undisplayed datapoints between A and B and none between A and C, it is much more likely that A and B are part of the same cluster than A and C.
AとBの間に表示されないデータポイントが多く、AとCの間に表示されないデータポイントがない場合、AとBはAとCよりも同じクラスターの一部である可能性が高い。
This is illustrated in Figure 6.
これを図6に示す。
In this section, we show how t-SNE can be modified to display a random subset of the datapoints (so-called landmark points) in a way that uses information from the entire (possibly very large) data set.
このセクションでは、データ点（いわゆるランドマーク点）のランダムな部分集合を表示するために、t-SNEをどのように修正すればよいかを、データセット全体（おそらく非常に大きい）の情報を使用する方法で示す。
We start by choosing a desired number of neighbors and creating a neighborhood graph for all of the datapoints.
まず、希望する数の近傍を選び、すべてのデータポイントの近傍グラフを作成する。
Although this is computationally intensive, it is only done once.
これは計算量が多いが、一度しか行わない。
Then, for each of the landmark points, we define a random walk starting at that landmark point and terminating as soon as it lands on another landmark point.
次に、それぞれのランドマーク点について、そのランドマーク点から出発し、他のランドマーク点に着地したらすぐに終了するランダムウォークを定義する。
During a random walk, the probability of choosing an edge emanating from node xi to node x j is proportional to e −kxi−x jk 2 .
ランダムウォーク中、ノードxiからノードx jに向かう辺を選ぶ確率はe -kxi-x jk 2に比例する。
We define pj|i to be the fraction of random walks starting at landmark point xi that terminate at landmark point x j .
i to be the fraction of random walks starting at landmark point xi that terminate at landmark point x j .
This has some resemblance to the way Isomap measures pairwise distances between points.
これは、アイソマップがポイント間のペア距離を測定する方法に似ている。
However, as in diffusion maps (Lafon and Lee, 2006; Nadler et al., 2006), rather than looking for the shortest path through the neighborhood graph, the random walk-based affinity measure integrates over all paths through the neighborhood graph.
しかし、拡散マップ（Lafon and Lee, 2006; Nadler et al, 2006）のように、近傍グラフを通る最短経路を探すのではなく、ランダムウォークベースの親和性尺度は、近傍グラフを通るすべての経路を積分する。
As a result, the random walk-based affinity measure is much less sensitive to “short-circuits” (Lee and Verleysen, 2005), in which a single noisy datapoint provides a bridge between two regions of dataspace that should be far apart in the map.
その結果、ランダムウォークベースの親和性測定は、「ショートサーキット」（Lee and Verleysen, 2005）に対する感度が非常に低くなる。
Similar approaches using random walks have also been successfully applied to, for example, semi-supervised learning (Szummer and Jaakkola, 2001; Zhu et al., 2003) and image segmentation (Grady, 2006).
ランダムウォークを用いた同様のアプローチは、例えば半教師付き学習（Szummer and Jaakkola, 2001; Zhu et al.

The most obvious way to compute the random walk-based similarities p j|i is to explicitly perform the random walks on the neighborhood graph, which works very well in practice, given that one can easily perform one million random walks per second.
i is to explicitly perform the random walks on the neighborhood graph, which works very well in practice, given that one can easily perform one million random walks per second.
Alternatively, Grady (2006) presents an analytical solution to compute the pairwise similarities p j|i that involves solving a sparse linear system.
i that involves solving a sparse linear system.
The analytical solution to compute the similarities p j|i is sketched in Appendix B.
i is sketched in Appendix B.
In preliminary experiments, we did not find significant differences between performing the random walks explicitly and the analytical solution.
予備実験では、ランダムウォークを陽解法で実行した場合と解析解で実行した場合の有意差は見られなかった。
In the experiment we present below, we explicitly performed the random walks because this is computationally less expensive.
以下に紹介する実験では、ランダムウォークを明示的に行ったが、これは計算コストが低いからである。
However, for very large data sets in which the landmark points are very sparse, the analytical solution may be more appropriate.
しかし、ランドマーク点が非常にまばらな非常に大規模なデータセットの場合は、解析解の方が適切な場合がある。
Figure 7 shows the results of an experiment, in which we applied the random walk version of t-SNE to 6,000 randomly selected digits from the MNIST data set, using all 60,000 digits to compute the pairwise affinities p j|i .
i .
In the experiment, we used a neighborhood graph that was constructed using a value of k = 20 nearest neighbors.9 The inset of the figure shows the same visualization as a scatterplot in which the colors represent the labels of the digits.
実験では、k＝20の最近接値を用いて作成した近傍グラフを使用した9。図の挿入図は、散布図と同じ視覚化で、色は数字のラベルを表している。
In the t-SNE map, all classes are clearly separated and the “continental” sevens form a small separate cluster.
t-SNEマップでは、すべてのクラスが明確に分離され、"コンチネンタル "セブンは小さな独立したクラスターを形成している。
Moreover, t-SNE reveals the main dimensions of variation within each class, such as the orientation of the ones, fours, sevens, and nines, or the “loopiness” of the twos.
さらに、t-SNEは、1、4、7、9の向きや、2の「ループ性」のような、各クラス内の変動の主な次元を明らかにする。
The strong performance of t-SNE is also reflected in the generalization error of nearest neighbor classifiers that are trained on the low-dimensional representation.
t-SNEの強力な性能は、低次元表現で訓練された最近傍分類器の汎化誤差にも反映されている。
Whereas the generalization error (measured using 10-fold cross validation) of a 1-nearest neighbor classifier trained on the original 784-dimensional datapoints is 5.75%, the generalization error of a 1-nearest neighbor classifier trained on the two-dimensional data representation produced by t-SNE is only 5.13%.
元の784次元のデータポイントに対して訓練された1-最近傍分類器の汎化誤差（10-fold cross validationを用いて測定）が5.75%であるのに対し、t-SNEによって生成された2次元データ表現に対して訓練された1-最近傍分類器の汎化誤差はわずか5.13%である。
The computational requirements of random walk t-SNE are reasonable: it took only one hour of CPU time to construct the map in Figure 7.
ランダムウォークt-SNEの計算要件は合理的である： 図7のマップを作成するのにかかったCPU時間はわずか1時間である。

# 6. Discussion 議論

The results in the previous two sections (and those in the supplemental material) demonstrate the performance of t-SNE on a wide variety of data sets.
前の2つのセクションの結果（および補足資料の結果）は、様々なデータセットにおけるt-SNEの性能を示している。
In this section, we discuss the differences between t-SNE and other non-parametric techniques (Section 6.1), and we also discuss a number of weaknesses and possible improvements of t-SNE (Section 6.2).6.1 Comparison with Related Techniques Classical scaling (Torgerson, 1952), which is closely related to PCA (Mardia et al., 1979; Williams, 2002), finds a linear transformation of the data that minimizes the sum of the squared errors between high-dimensional pairwise distances and their low-dimensional representatives.
本節では、t-SNEと他のノンパラメトリック技法との違いを議論し（セクション6.1）、t-SNEの多くの弱点と可能な改善点についても議論する（セクション6.2）。6.1 関連技法との比較 PCA（Mardia et al, 1979; Williams, 2002）と密接に関連する古典的スケーリング（Torgerson, 1952）は、高次元の対距離とその低次元の代表との間の2乗誤差の和を最小化するデータの線形変換を見つける。
A linear method such as classical scaling is not good at modeling curved manifolds and it focuses on preserving the distances between widely separated datapoints rather than on preserving the distances between nearby datapoints.
古典的なスケーリングのような線形手法は、曲線多様体のモデル化には向いておらず、近接したデータポイント間の距離を保存することよりも、大きく離れたデータポイント間の距離を保存することに重点を置いている。
An important approach that attempts to address the problems of classical scaling is the Sammon mapping (Sammon, 1969) which alters the cost function of classical scaling by dividing the squared error in the representation of each pairwise Euclidean distance by the original Euclidean distance in the high-dimensional space.
古典的スケーリングの問題に対処しようとする重要なアプローチは、サモンマッピング（Sammon, 1969）である。これは、各対ユークリッド距離の表現における二乗誤差を高次元空間における元のユークリッド距離で割ることによって、古典的スケーリングのコスト関数を変更するものである。
The resulting cost function is given by
その結果、コスト関数は次式で与えられる。

$$
\tag{}
$$

where the constant outside of the sum is added in order to simplify the derivation of the gradient.
ここで、和の外側の定数は、勾配の導出を簡単にするために加えられている。
The main weakness of the Sammon cost function is that the importance of retaining small pairwise distances in the map is largely dependent on small differences in these pairwise distances.
サモンのコスト関数の主な弱点は、マップに小さなペアワイズ距離を残すことの重要性が、これらのペアワイズ距離の小さな差に大きく依存することである。
In particular, a small error in the model of two high-dimensional points that are extremely close together results in a large contribution to the cost function.
特に、極めて近接した2つの高次元の点のモデルにおける小さな誤差は、コスト関数に大きな寄与をもたらす。
Since all small pairwise distances constitute the local structure of the data, it seems more appropriate to aim to assign approximately equal importance to all small pairwise distances.
すべての小さな対距離がデータの局所的な構造を構成するので、すべての小さな対距離に対してほぼ等しい重要度を割り当てることを目指すのがより適切であると思われる。
In contrast to Sammon mapping, the Gaussian kernel employed in the high-dimensional space by t-SNE defines a soft border between the local and global structure of the data and for pairs of datapoints that are close together relative to the standard deviation of the Gaussian, the importance of modeling their separations is almost independent of the magnitudes of those separations.
サモンマッピングとは対照的に、t-SNEが高次元空間で採用するガウシアンカーネルは、データのローカル構造とグローバル構造の間のソフトな境界を定義し、ガウシアンの標準偏差に相対的に近いデータポイントのペアについては、それらの分離をモデル化することの重要性は、それらの分離の大きさにほとんど依存しない。
Moreover, t-SNE determines the local neighborhood size for each datapoint separately based on the local density of the data (by forcing each conditional probability distribution Pi to have the same perplexity).
さらに、t-SNEは、データの局所密度に基づいて、各データポイントの局所近傍サイズを個別に決定する（各条件付き確率分布Piが同じpleplexityを持つように強制することによって）。
The strong performance of t-SNE compared to Isomap is partly explained by Isomap’s susceptibility to “short-circuiting”.
t-SNEがIsomapと比較して強力な性能を発揮するのは、Isomapが「短絡」しやすいことが一因である。
Also, Isomap mainly focuses on modeling large geodesic distances rather than small ones.
また、Isomapは、小さな測地線距離よりも大きな測地線距離をモデル化することに主眼を置いている。
The strong performance of t-SNE compared to LLE is mainly due to a basic weakness of LLE: the only thing that prevents all datapoints from collapsing onto a single point is a constraint on the covariance of the low-dimensional representation.
LLEと比較してt-SNEの性能が高いのは、主にLLEの基本的な弱点によるものである： すべてのデータポイントが1点に集約されるのを防ぐ唯一のものは、低次元表現の共分散に対する制約である。
In practice, this constraint is often satisfied by placing most of the map points near the center of the map and using a few widely scattered points to create large covariance (see Figure 3(b) and 4(d)).
実際には、ほとんどの地図点を地図の中心付近に配置し、大きな共分散を作るために広く散らばったいくつかの点を使うことで、この制約を満たすことが多い（図3（b）と図4（d）参照）。
For neighborhood graphs that are almost disconnected, the covariance constraint can also be satisfied by a “curdled” map in which there are a few widely separated, collapsed subsets corresponding to the almost disconnected components.
ほぼ切断された近傍グラフの場合、共分散の制約は、ほぼ切断された構成要素に対応する、いくつかの大きく離れた、折りたたまれた部分集合が存在する "curdled "写像によっても満たすことができる。
Furthermore, neighborhood-graph based techniques (such as Isomap and LLE) are not capable of visualizing data that consists of two or more widely separated submanifolds, because such data does not give rise to a connected neighborhood graph.
さらに、近傍グラフに基づく技術（IsomapやLLEなど）は、2つ以上の大きく離れた部分多様体からなるデータを可視化することはできない。
It is possible to produce a separate map for each connected component, but this loses information about the relative similarities of the separate components.
接続されたコンポーネントごとに別々のマップを作成することは可能だが、これでは別々のコンポーネントの相対的な類似性に関する情報が失われてしまう。
Like Isomap and LLE, the random walk version of t-SNE employs neighborhood graphs, but it does not suffer from short-circuiting problems because the pairwise similarities between the highdimensional datapoints are computed by integrating over all paths through the neighborhood graph.
IsomapやLLEと同様に、ランダムウォーク版のt-SNEは近傍グラフを用いるが、高次元データポイント間の対類似度は近傍グラフを通る全ての経路を積分することで計算されるため、短絡問題に悩まされることはない。
Because of the diffusion-based interpretation of the conditional probabilities underlying the random walk version of t-SNE, it is useful to compare t-SNE to diffusion maps.
t-SNEのランダムウォーク版の基礎となる条件付き確率の拡散に基づく解釈のため、t-SNEと拡散マップを比較することは有用である。
Diffusion maps define a “diffusion distance” on the high-dimensional datapoints that is given by
拡散マップは、高次元データポイント上の "拡散距離 "を定義する。

$$
\tag{}
$$

where p (t) i j represents the probability of a particle traveling from xi to x j in t timesteps through a graph on the data with Gaussian emission probabilities.
ここで、p (t) i j は、ガウス放出確率を持つデータ上のグラフをtタイムステップでxiからx jへ粒子が移動する確率を表す。
The term ψ(xk) (0) is a measure for the local density of the points, and serves a similar purpose to the fixed perplexity Gaussian kernel that is employed in SNE.
ψ(xk)(0)は点の局所密度を表す尺度であり、SNEで採用されている固定難度ガウスカーネルと同様の役割を果たす。
The diffusion map is formed by the principal non-trivial eigenvectors of the Markov matrix of the random walks of length t.
拡散マップは、長さtのランダムウォークのマルコフ行列の主要な非自明な固有ベクトルによって形成される。
It can be shown that when all (n−1) non-trivial eigenvectors are employed, the Euclidean distances in the diffusion map are equal to the diffusion distances in the high-dimensional data representation (Lafon and Lee, 2006).
(n-1)すべての非自明な固有ベクトルが採用されるとき、拡散マップにおけるユークリッド距離は、高次元データ表現における拡散距離と等しいことが示される(Lafon and Lee, 2006)。
Mathematically, diffusion maps minimize
数学的には、拡散マップは最小化する。

$$
\tag{}
$$

As a result, diffusion maps are susceptible to the same problems as classical scaling: they assign much higher importance to modeling the large pairwise diffusion distances than the small ones and as a result, they are not good at retaining the local structure of the data.
その結果、拡散マップは古典的なスケーリングと同じ問題の影響を受けやすい： 拡散マップは、小さな拡散距離よりも大きな拡散距離をモデル化することを非常に重要視し、その結果、データの局所構造を保持することが苦手となる。
Moreover, in contrast to the random walk version of t-SNE, diffusion maps do not have a natural way of selecting the length, t, of the random walks.
さらに、t-SNEのランダムウォーク版とは対照的に、拡散マップにはランダムウォークの長さtを選択する自然な方法がない。
In the supplemental material, we present results that reveal that t-SNE outperforms CCA (Demartines and Herault, ´ 1997), MVU (Weinberger et al., 2004), and Laplacian Eigenmaps (Belkin and Niyogi, 2002) as well.
補足資料では、t-SNEがCCA (Demartines and Herault, ´ 1997)、MVU (Weinberger et al., 2004)、Laplacian Eigenmaps (Belkin and Niyogi, 2002)をも上回ることを明らかにした結果を示す。
For CCA and the closely related CDA (Lee et al., 2000), these results can be partially explained by the hard border λ that these techniques define between local and global structure, as opposed to the soft border of t-SNE.
CCAと密接に関連するCDA (Lee et al., 2000)では、これらの結果は、t-SNEのソフトボーダーとは対照的に、これらの手法がローカル構造とグローバル構造の間に定義するハードボーダーλによって部分的に説明することができる。
Moreover, within the range λ, CCA suffers from the same weakness as Sammon mapping: it assigns extremely high importance to modeling the distance between two datapoints that are extremely close.
さらに、λの範囲内では、CCAはサモン・マッピングと同じ弱点に悩まされる： それは、極めて近い2つのデータポイント間の距離をモデル化することに極めて高い重要性を割り当てることである。
Like t-SNE, MVU (Weinberger et al., 2004) tries to model all of the small separations well but MVU insists on modeling them perfectly (i.e., it treats them as constraints) and a single erroneous constraint may severely affect the performance of MVU.
t-SNEと同様に、MVU (Weinberger et al., 2004)は、すべての小さな分離をうまくモデル化しようとするが、MVUはそれらを完全にモデル化することにこだわり（つまり、それらを制約として扱う）、1つの誤った制約がMVUの性能に重大な影響を与える可能性がある。
This can occur when there is a short-circuit between two parts of a curved manifold that are far apart in the intrinsic manifold coordinates.
これは、固有多様体座標において離れている湾曲多様体の2つの部分の間に短絡がある場合に起こりうる。
Also, MVU makes no attempt to model longer range structure: It simply pulls the map points as far apart as possible subject to the hard constraints so, unlike t-SNE, it cannot be expected to produce sensible large-scale structure in the map.
また、MVUはより長い範囲の構造をモデル化しようとはしない： t-SNEとは異なり、マップに大規模な構造を作り出すことは期待できない。
For Laplacian Eigenmaps, the poor results relative to t-SNE may be explained by the fact that Laplacian Eigenmaps have the same covariance constraint as LLE, and it is easy to cheat on this constraint.6.2 Weaknesses Although we have shown that t-SNE comparesfavorably to other techniquesfor data visualization, tSNE has three potential weaknesses: (1) it is unclear how t-SNE performs on general dimensionality reduction tasks, (2) the relatively local nature of t-SNE makes it sensitive to the curse of the intrinsic dimensionality of the data, and (3) t-SNE is not guaranteed to converge to a global optimum of its cost function.
6.2 弱点 t-SNEがデータ可視化のための他の技法と比較して有利であることを示したが、t-SNEには3つの潜在的な弱点がある： (1)t-SNEが一般的な次元削減タスクでどのように機能するかは不明である。(2)t-SNEは比較的局所的な性質を持っているため、データの固有次元の呪いに敏感である。
Below, we discuss the three weaknesses in more detail.1) Dimensionality reduction for other purposes.
以下では、3つの弱点について詳しく説明する。1）他の目的のための次元削減。
It is not obvious how t-SNE will perform on the more general task of dimensionality reduction (i.e., when the dimensionality of the data is not reduced to two or three, but to d > 3 dimensions).
t-SNEが、より一般的な次元削減タスク（すなわち、データの次元が2次元や3次元に削減されるのではなく、d＞3次元に削減される場合）において、どのように機能するかは明らかではない。
To simplify evaluation issues, this paper only considers the use of t-SNE for data visualization.
評価の問題を単純化するため、本稿ではデータ可視化のためのt-SNEの使用のみを検討する。
The behavior of t-SNE when reducing data to two or three dimensions cannot readily be extrapolated to d > 3 dimensions because of the heavy tails of the Student-t distribution.
データを2次元または3次元に縮小したときのt-SNEの挙動は、Student-t分布の重い尾のため、d > 3次元には容易に外挿できない。
In high-dimensional spaces, the heavy tails comprise a relatively large portion of the probability mass under the Student-t distribution, which might lead to d-dimensional data representations that do not preserve the local structure of the data as well.
高次元空間では、スチューデントt分布の確率質量に占める重いテールの割合が相対的に大きくなるため、データの局所構造を保存しきれないd次元のデータ表現になる可能性がある。
Hence, for tasks in which the dimensionality of the data needs to be reduced to a dimensionality higher than three, Student t-distributions with more than one degree of freedom10 are likely to be more appropriate.2) Curse of intrinsic dimensionality.
したがって、データの次元を3次元以上にする必要があるタスクでは、自由度10が1以上のスチューデントt分布がより適切であると考えられる。
t-SNE reduces the dimensionality of data mainly based on local properties of the data, which makes t-SNE sensitive to the curse of the intrinsic dimensionality of the data (Bengio, 2007).
t-SNEは主にデータの局所的な性質に基づいてデータの次元を削減するため、t-SNEはデータの固有次元の呪いに敏感である（Bengio, 2007）。
In data sets with a high intrinsic dimensionality and an underlying manifold that is highly varying, the local linearity assumption on the manifold that t-SNE implicitly makes (by employing Euclidean distances between near neighbors) may be violated.
固有次元が高く、基礎となる多様体が大きく変化するデータセットでは、t-SNEが暗黙のうちに行う（近傍間のユークリッド距離を用いる）多様体の局所線形性の仮定が破られる可能性がある。
As a result, t-SNE might be less successful if it is applied on data sets with a very high intrinsic dimensionality (for instance, a recent study by Meytlis and Sirovich (2007) estimates the space of images of faces to be constituted of approximately 100 dimensions).
例えば、Meytlis and Sirovich (2007)による最近の研究では、顔の画像空間は約100次元で構成されていると推定されている。
Manifold learners such as Isomap and LLE suffer from exactly the same problems (see, e.g., Bengio, 2007; van der Maaten et al., 2008).
IsomapやLLEのような多様体学習者も、まったく同じ問題を抱えている（例えば、Bengio, 2007; van der Maaten et al.）
A possible way to (partially) address this issue is by performing t-SNE on a data representation obtained from a model that represents the highly varying data manifold efficiently in a number of nonlinear layers such as an autoencoder (Hinton and Salakhutdinov, 2006).
この問題に（部分的に）対処する可能な方法は、オートエンコーダのような多数の非線形層で高度に変化するデータ多様体を効率的に表現するモデルから得られたデータ表現に対してt-SNEを実行することである（Hinton and Salakhutdinov, 2006）。
Such deep-layer architectures can represent complex nonlinear functions in a much simpler way, and as a result, require fewer datapoints to learn an appropriate solution (as is illustrated for a d-bits parity task by Bengio 2007).
このような深層アーキテクチャは、複雑な非線形関数をより単純な方法で表現することができ、その結果、適切な解を学習するために必要なデータポイントが少なくなる（Bengio 2007によるdビットのパリティ・タスクの例）。
Performing t-SNE on a data representation produced by, for example, an autoencoder is likely to improve the quality of the constructed visualizations, because autoencoders can identify highly-varying manifolds better than a local method such as t-SNE.
オートエンコーダは、t-SNEのような局所的な手法よりも、変化の大きい多様体をよりよく識別できるため、例えばオートエンコーダによって生成されたデータ表現に対してt-SNEを実行すると、構築された可視化の品質が向上する可能性が高い。
However, the reader should note that it is by definition impossible to fully represent the structure of intrinsically high-dimensional data in two or three dimensions.3) Non-convexity of the t-SNE cost function.
3）t-SNEコスト関数の非凸性。
A nice property of most state-of-the-art dimensionality reduction techniques (such as classical scaling, Isomap, LLE, and diffusion maps) is the convexity of their cost functions.
最新の次元削減技術（古典的スケーリング、アイソマップ、LLE、拡散マップなど）の優れた特性は、そのコスト関数が凸であることである。
A major weakness of t-SNE is that the cost function is not convex, as a result of which several optimization parameters need to be chosen.
t-SNEの大きな弱点は、コスト関数が凸でないことであり、その結果、いくつかの最適化パラメータを選択する必要がある。
The constructed solutions depend on these choices of optimization parameters and may be different each time t-SNE is run from an initial random configuration of map points.
構築された解は、最適化パラメータの選択に依存し、マップポイントの初期ランダム構成からt-SNEを実行するたびに異なる可能性がある。
We have demonstrated that the same choice of optimization parameters can be used for a variety of different visualization tasks, and we found that the quality of the optima does not vary much from run to run.
我々は、最適化パラメータの同じ選択が様々な異なる可視化タスクに使用できることを実証し、最適化の質は実行ごとにあまり変わらないことを発見した。
Therefore, we think that the weakness of the optimization method is insufficient reason to reject t-SNE in favor of methods that lead to convex optimization problems but produce noticeably worse visualizations.
したがって、最適化手法の弱さは、凸最適化問題を導くが、著しく悪い視覚化をもたらす手法を支持して、t-SNEを拒否する十分な理由にはならないと考える。
A local optimum of a cost function that accurately captures what we want in a visualization is often preferable to the global optimum of a cost function that fails to capture important aspects of what we want.
私たちが視覚化に求めるものを正確にとらえるコスト関数の局所最適は、私たちが求めるものの重要な側面をとらえることができないコスト関数の全体最適よりも望ましいことが多い。
Moreover, the convexity of cost functions can be misleading, because their optimization is often computationally infeasible for large real-world data sets, prompting the use of approximation techniques (de Silva and Tenenbaum, 2003; Weinberger et al., 2007).
さらに、コスト関数の凸性は誤解を招く可能性がある。なぜなら、その最適化は、実世界の大規模なデータセットでは計算不可能であることが多く、近似技法の使用を促しているからである（de Silva and Tenenbaum, 2003; Weinberger et al, 2007）。
Even for LLE and Laplacian Eigenmaps, the optimization is performed using iterative Arnoldi (Arnoldi, 1951) or Jacobi-Davidson (Fokkema et al., 1999) methods, which may fail to find the global optimum due to convergence problems.
LLEやラプラシアン固有マップの場合でも、最適化はArnoldi (Arnoldi, 1951)やJacobi-Davidson (Fokkema et al., 1999)の反復法を用いて行われるが、収束の問題から大域的最適解を見つけられないことがある。

# 7. Conclusion 結論

The paper presents a new technique for the visualization of similarity data that is capable of retaining the local structure of the data while also revealing some important global structure (such as clusters at multiple scales).
本論文では、データの局所的な構造を保持しつつ、重要な大域的構造（複数のスケールにおけるクラスターなど）を明らかにすることができる、類似性データの可視化のための新しい手法を紹介する。
Both the computational and the memory complexity of t-SNE are O(n 2 ), but we present a landmark approach that makes it possible to successfully visualize large real-world data sets with limited computational demands.
t-SNEの計算量と記憶量はともにO(n 2 )であるが、限られた計算量で実世界の大規模なデータセットの可視化に成功した画期的なアプローチを紹介する。
Our experiments on a variety of data sets show that t-SNE outperforms existing state-of-the-art techniques for visualizing a variety of real-world data sets.
様々なデータセットでの実験から、t-SNEは実世界の様々なデータセットの可視化において、既存の最先端技術を凌駕することが示された。
Matlab implementations of both the normal and the random walk version of t-SNE are available for download at http://ticc.uvt.nl/˜lvdrmaaten/tsne.
正規版とランダムウォーク版のt-SNEのMatlab実装は、http://ticc.uvt.nl/〜lvdrmaaten/tsneからダウンロードできる。
In future work we plan to investigate the optimization of the number of degrees of freedom of the Student-t distribution used in t-SNE.
今後の研究では、t-SNEで使用されるStudent-t分布の自由度数の最適化について調査する予定である。
This may be helpful for dimensionality reduction when the low-dimensional representation has many dimensions.
これは、低次元表現が多次元である場合に、次元削減のために役に立つかもしれない。
We will also investigate the extension of t-SNE to models in which each high-dimensional datapoint is modeled by several low-dimensional map points as in Cook et al.(2007).
また、Cookら(2007)のように、各高次元データポイントが複数の低次元マップポイントによってモデル化されるモデルへのt-SNEの拡張についても検討する。
Also, we aim to develop a parametric version of t-SNE that allows for generalization to held-out test data by using the t-SNE objective function to train a multilayer neural network that provides an explicit mapping to the low-dimensional space.
また、低次元空間への明示的なマッピングを提供する多層ニューラルネットワークを訓練するためにt-SNE目的関数を使用することにより、保持されたテストデータへの汎化を可能にするt-SNEのパラメトリックバージョンの開発も目指している。
