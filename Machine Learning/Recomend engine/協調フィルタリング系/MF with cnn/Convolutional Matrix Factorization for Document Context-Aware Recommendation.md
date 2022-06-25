# 参考

- https://www.m3tech.blog/entry/2018/03/07/122353
- https://github.com/nishiba/convmf

# タイトル

- Convolutional Matrix Factorization for Document Context-Aware Recommendation
- ドキュメントコンテキストを考慮したレコメンデーションの為の畳み込み行列因子分解

# Introduction

## 評価行列のスパース性の上昇

- The exploding growth of the number of users and items in ecommerce services increases the sparseness of user-to-item ratining data. eコマースサービスにおけるユーザ数とアイテム数の爆発的な増加により、ユーザからアイテムへの評価データのスパース性が高まっている。
  - Eventually, this sparsity deteriorates the rating prediction accuracy of traditional collaborative filtering techniこのようなスパース性は， 従来の協調型レコメンデーション手法のレーティング予測精度を低下させる
  - To enhance the accuracy, several recommendation techniques had been proposed that consider not only rating information but also auxil-そこで、評価情報だけでなく、ソーシャルネットワーク、アイテムの説明文書のような**補助的な情報も考慮した推薦手法**が提案されている。

## 補助的な情報も考慮した推薦手法

- 近年、、LDA（Latent Dirichlet Allocation ）やSDAE（Stacked Denoising AutoEncoder）などの**文書モデリング手法**に基づき、レビュー、アブストラクト、シノプスなどの項目記述文書を追加的に利用するアプローチが提案されている。
  - 具体的には，Wangらはトピックモデリング(LDA)と協調検索を確率的 アプローチで組み合わせた協調トピック回帰(CTR)を提案した
  - また、項目 記述文書を分析するために、LDAを協調的手法に統合したCTRのバリエーション が、異なる統合アプローチで提案されている。
  - 最近では、Wangらが SDAEを確率的行列分解（PMF）に統合する協調深層学習（CDL）を提案し[20]、これにより評価予測精度の点でより正確な潜在モデルを生成している

## 既存手法の欠点<bag-of-wordsモデルの前提>

- しかし、既存の統合モデルは、周辺語や語順など**文書の文脈情報を無視した bag-of-wordsモデル**を前提としているため、文書情報を十分に把握することができない。
  - 例えば、ある文書に次の2つの文が与えられているとする。
    - people trust the man.",
    - "people betray his trust finally."
    - LDAやSDAEは文書を識別可能な単語の袋として考えるので、"trust "という単語の出現をそれぞれ識別することはでき ない。
    - つまり、"trust "という単語はほとんど同じ意味に見えますが、**動詞と名詞と いう微妙な構文上の違い**がある。
- このような文書内の微妙な違いも、文書 をより深く理解するための自明な要素であり、さらにそのような理解を深めることで評 価予測精度を向上させることができる。

## CNNの活用

- To address the aforementioned issue, we utilize convolutional neural network (CNN), which is the state-of-the-art machine learning methodology that shows high performance for various domains such as computer vision. CNNは、コンピュータビジョン[13]、自然言語処理[2, 10, 11]、情報検索[4, 21] などの様々な分野で高い性能を示す最先端の機械学習手法であり、CNNを利用することで前述の課題を解決する。
  - CNN effectively captures local features of images or documents through modeling components such as local receptive fields, shared weights, and subsampling. CNNは局所受容体、共有重み、サブサンプリングなどのモデル化要素により、画像や文書の局所的な特徴を効果的に捉えることができる。
  - Thus, the use of CNN facilitates deeper understanding of documents, and generates better latent model than LDA and SDAE do, especially for items that resort to their description documents due to the lack of ratings. したがって、CNNを用いることで、文書のより深い理解が容易になり、**特に評価がないために説明文書に頼る項目(=コールドスタート問題！！)**については、LDAやSDAEよりも優れた潜在モデルを生成することができる。
  - Moreover, CNN is able to take advantage of pre-trained word embedding models such as Glove [18] for deeper understanding of item description documents. さらに、CNNはGlove[18]のような 事前に学習された単語埋め込みモデルを利用することができ、アイテムの説明文書 をより深く理解することができる。
  - Note that LDA and SDAE cannot exploit pre-trained word embedding models because they adopt bag-of-words models. ただし、LDAとSDAEはbag-of-wordsモデルを 採用しているため、事前に学習された単語埋め込みモデルを利用することができない。

## 推薦タスクに向けたCNNの技術的課題

- However, existing CNNs are not suitable for recommendation task, as their objectives are different from the objective of recommendation. しかし、既存のCNNは推薦の目的とは異なるため、推薦タスクには適していな い。
  - Specifically, conventional CNNs mainly solve classifi-cation task that is to predict labels of words, phrases, or documents. 具体的には、**従来のCNNは主に単語、フレーズ、文書などのラベルを予測する分類タスク**を解決する。
  - On the contrary, the objective of recommendation is regarded as a regression task aiming at accurately approximating ratings of users on items. これに対して、**推薦の目的は、アイテムに対するユーザの評価を正確に近似することを目的とした回帰タスク**とみなされている。
  - Thus, the existing CNNs cannot be directly applied to our task of recommendation. したがって、既存のCNNは推薦というタスクに直接適用することはできない。

## 技術的課題への対応

- To handle the technical issue, we propose a document contextaware recommendation model, convolutional matrix factorization (ConvMF), which captures contextual information of item description documents by utilizing convolutional neural network (CNN) and further enhances the rating prediction accuracy. この技術的課題を処理するために、我々は畳み込みニューラルネットワーク（CNN）を利用して項目記述文書の文脈情報を捕捉し、さらに評価予測精度を向上させる文書文脈考慮型推薦モデル、畳み込み行列分解（ConvMF）を提案する。
  - Precisely, ConvMF seamlessly integrates CNN into PMF, which is commonly used for recommendation tasks. 具体的には、ConvMFは推薦タスクによく用いられるPMFにCNNをシームレスに統合したものである。
  - Consequently, the integrated model follows the recommendation objective, and eventually effectively utilizes both collaborative information and contextual information. その結果、統合されたモデルは推薦の目的に従い、最終的に協調情報と文脈情報の両方を効果的に利用することができる。
  - As a result, ConvMF accurately predicts unknown ratings even when the rating data is extremely sparse. その結果、ConvMFは、評価データが極めて疎な場合でも、未知の評価を正確に予測することができる。

## 本研究でしたこと

- To demonstrate the effectiveness of ConvMF, we evaluate ConvMF on three different real-world datasets. ConvMFの有効性を示すために、我々は3つの異なる実世界のデータセットでConvMFを評価した。
  - Our extensive experiments over various sparsenesses of rating datasets demonstrate that ConvMF significantly outperforms the state-of-the-art models.様々なスパースネスを持つ評価データセットに対する広範な実験により、ConvMFが最先端モデルを著しく上回ることを実証する。
  - The superiority of ConvMF verifies that ConvMF generates item latent models that effectively reflect contextual information of item description documents even when the rating data is extremely sparse. ConvMFの優位性は、評価データが極めて疎である場合でも、項目説明文書の文脈情報を効果的に反映した項目潜在モデルを生成することを検証する。
  - We also qualitatively demonstrate that ConvMF indeed captures subtle contextual differences of a word in a document. また、ConvMFが文書中の単語の微妙な文脈の違いを実際に捉えることを定性的に示す。
  - Furthermore, we investigate whether pre-trained word embedding model helps improve the rating prediction accuracy of ConvMF. さらに、事前に学習した単語埋め込みモデルがConvMFの評価予測精度を向上させるかどうかを調査する。
  - Detailed experiment results are also available at http://dm.postech. ac.kr/ConvMF besides our implementation and datasets.詳細な実験結果は、我々の実装とデータセットに加えて、http://dm.postech. ac.kr/ConvMF で公開されている。

## Our contributions

- Our contributions are summarized as follows. 我々の貢献は以下のようにまとめられる。
  - We address limitations of the bag-of-words model based approaches and develop a novel document context-aware recommendation model (ConvMF). 我々はBag-of-Wordsモデルに基づくアプローチの限界に対処し、新しい文書文脈考慮型推薦モデル（ConvMF）を開発する。
  - To exploit both ratings and item description documents, we seamlessly integrate CNN into PMF under probabilistic perspective.評価と項目説明文書の両方を利用するために、我々はCNNを確率的な観点でPMFにシームレスに統合する。
  - We extensively demonstrate the superiority of ConvMF over the state-of-the-art models on three real-world datasets with quantitative and qualitative results. 我々は、3つの実世界データセットにおいて、ConvMFの優位性を定量的・定性的な結果で示す。

## 本論文の構成

- The remainder of the paper is organized as follows. 本論文の残りの部分は以下のように構成される。
  - Section 2 briefly reviews preliminaries on the most representative collaborative filtering technique and CNN. セクション2は最も代表的な協調フィルタリング技術とCNNに関する前置きを簡単にレビューする。
  - Section 3 introduces an overview of ConvMF, explains our CNN architecture of ConvMF, and describes how to optimize ConvMF.
  - セクション3ではConvMFの概要を紹介し，我々のConvMFのCNNアーキテクチャを説明し，ConvMFを最適化する方法を説明する．
  - Section 4 experimentally evaluates ConvMF and discuss the evaluation results. セクション4ではConvMFを実験的に評価し、評価結果について議論する。
  - Section 5 summarizes our contributions and gives future work. セクション 5 では我々の貢献と今後の課題をまとめる。

# PRELIMINARY 前置き

## Matrix Factorization

- Traditional collaborative filtering techniques are categorized into two categories [5]: memory-based methods (e.g. nearest neighborhood) [3, 7, 12] and model-based methods (e.g. latent factor model) [12, 20].従来の協調フィルタリング技術は、記憶に基づく手法（最近傍など）[3, 7, 12]とモデルに基づく手法（潜在因子モデルなど）[12, 20]に分類される[5]。
- In general, model-based methods are known to generate more accurate recommendation results [12]. 一般に、モデルベース手法は、より正確な推薦結果を生成することが知られている[12]。
- Thus in this section, we describe MF, which is the most popular model-based method. そこで、本節では、モデルベース手法の中で最もポピュラーなMFについて説明する。

### 理論

- The goal of MF is to find latent models of users and items on a shared latent space in which the strengths of user-item relationships (i.e., rating by a user on an item) are computed by inner products [12]. MFの目的は、ユーザとアイテムの関係（ユーザによるアイテムへの評価）の強さが内積によって計算される共有潜在空間上でユーザとアイテムの潜在モデルを見つけることである[12]。
  - Suppose that we have N users, M items and a user-item rating matrix $R \in \mathbb{R}^{N\times M}$ . ここで、N人のユーザ、M個のアイテム、ユーザとアイテムの評価行列$R \in \mathbb{R}^{N\times M}$があるとする。
  - In MF, the latent models of user i and item j are represented as k-dimensional models, $u_i \in \mathbb{R^k}$ and vj ∈ Rk. MFでは、ユーザ i とアイテム j の潜在モデルを k 次元モデル ui∈Rk, vj∈Rk として表現する。
  - The rating rij of user i on item j is approximated by the inner-product of corresponding latent models of user i and item j (i.e. rij ≈ ˆ rij = uT i vj). ユーザiのアイテムjに対する評価rijは、ユーザiとアイテムjの対応する潜在モデルの内積で近似される（すなわち、rij ≈ ˆ rij = uT i vj）。
  - A general way of training latent models is to minimize a loss function L, which consists of sum-of-squarederror terms between the actual ratings and the predicted ratings and L2 regularized terms that try to avoid the over-fitting problem as follows: 潜在モデルを学習する一般的な方法は、以下のように実際の評価と予測される評価の二乗誤差の項とオーバーフィッティング問題を回避しようとするL2正則化項からなる損失関数Lを最小化することである。

$$
L = \sum_{i}^{N} \sum_{j}^{M}
I_{ij}(r_{ij}-u_{i}^T v_j)^2
+ \lambda_u \sum_i^N ||u_i||^2
+ \lambda_u \sum_j^M ||u_j||^2
$$

where $I_{ij}$ is an indicator function such that it is 1 if user i rated item j and 0 otherwise. ここで、**$I_{ij}$は、ユーザiがアイテムjを評価した場合に1、そうでない場合に0となるような指標関数**である。
(**「評価行列内の観測済みの評価値のみを用いて学習する」事を、関数$I_{ij}$を使うことで数式内で表現してる**！！)

## Convolutional Neural Network

### 構成

- Convolutional neural network (CNN) is a variant of feed-forward neural networks with the following components 畳み込みニューラルネットワーク（CNN）は、フィードフォワードニューラルネットワークの変種であり、以下の構成要素を持つ:
  - 1. convolution layer for generating local features, 局所特徴を生成する畳み込み層
  - 2. pooling (or sub-sampling) layer for representing data as more concise representation by selecting only several representative local features (i.e., features having the highest score via the activation functions) from the previous layer, which is usually a convolution layer. 前層（通常は畳み込み層）から代表局所特徴（活性化関数を介して最高スコアを持つ特徴）だけを複数選択し、より簡潔な表現としてデータを表現するプーリング（またはサブサンプリング）層

### 発展の背景

- Even though CNN has been originally developed for computer vision [13], the key idea of CNN has been actively applied to information retrieval and NLP such as search query retrieval [4, 21], sentence modeling and classification [10, 11], and other traditional NLP tasks [2]. CNNはもともとコンピュータビジョンのために開発されたにもかかわらず[13]、CNNのキーアイディアは、検索クエリ検索[4, 21]、文のモデリングと分類[10, 11]などの情報検索とNLP、およびその他の伝統的なNLPタスク[2]に活発に適用されている。
- Although CNN for NLP tasks requires a significant amount of modification on the architecture of CNN, it eventually helps enhance the performance of various NLP tasks.NLPタスクのためのCNNは、CNNのアーキテクチャに多大な修正を加える必要があるが、最終的には様々なNLPタスクの性能向上に貢献する。

### CNNと推薦システムの歴史

- However, CNN has not yet been actively adopted to the field of recommender system. しかし、CNNは推薦システムの分野にはまだ積極的に採用されていない。
  - To the best of our knowledge, van den Oord et al. were first to apply CNN to music recommendation [22], where they analyzed songs in acoustic analysis point of view via CNN, and proposed a model that predicts the ratings based on the item latent model obtained by acoustic CNN. 我々の知る限り、**van den OordらはCNNを音楽推薦に初めて適用**し[22]、CNNによって楽曲を音響分析の観点から解析し、音響CNNによって得られた項目潜在モデルに基づいて評価を予測するモデルを提案している。
- However, their CNN model, designed for acoustic signal processing, is not suitable for processing documents. しかし、音響信号処理のために設計された彼らのCNNモデルは、文書の処理には適していない。
  - Documents and acoustic signals have an inherent difference on the quality of surrounding features. 文書と音響信号では、周辺の特徴量の質に本質的な違いがある。
  - A signal at a certain time is inherently similar to its surrounding signals, i.e., the signals that have slight time difference, while a word at a certain position in the document has a large semantical difference from the surrounding words. ある時刻の信号は周囲の信号、すなわちわずかな時間差のある信号と本質的に類似しているが、文書中のある位置の単語は周囲の単語と大きな意味的差異を持っている。
  - Such difference in the degree of similarity between surrounding features affects the quality of local features, and eventually requires different CNN architectures. このような周辺特徴量の類似度の違いは局所特徴量の品質に影響し、最終的には異なるCNNアーキテクチャを必要とする。
  - Furthermore, the model does not fully reflect the collaborative information. さらに、このモデルは協調情報を十分に反映していない。
  - In particular, the item latent models are mainly determined by the results of audio signal analysis via CNN rather than collaborative information. 特に、項目潜像モデルは、協調情報よりもCNNによる音声信号解析の結果によって主に決定される。
- Thus, the performance of overall recommendation even does not achieve that of weighted matrix factorization (WMF) [9], which is one of the conventional MF-based collaborative filtering techniques dealing with implicit feedback dataset. このため、全体の推薦性能は、**暗黙のフィードバックデータを扱う従来のMFベースの協調フィルタリング手法の一つである重み付き行列分解（WMF）**[9]の性能にさえ及ばない。

# Convolutional Matrix Factorization

In this section, we provide details of the proposed model, convolutional matrix factorization (ConvMF), through three steps:本節では、提案モデルである畳み込み行列分解（ConvMF）の詳細を、3つのステップを通じて説明する。

- 1. We introduce the probabilistic model of ConvMF, and describe the key idea to bridge PMF and CNN in order to utilize both ratings and item description documents. ConvMFの確率モデルを紹介し、評価と項目記述文書の両方を利用するためにPMFとCNNを橋渡しする重要なアイデアを説明する。
- 2)We explain the detailed architecture of our CNN, which generates document latent model by analyzing item description documents.項目記述文書を分析し、文書潜在モデルを生成する我々のCNNの詳細なアーキテクチャを説明する。
- 3)Finally, we describe how to optimize latent variables of ConvMF. 最後に、ConvMFの潜在変数の最適化方法について述べる。

## Probabilistic Model of ConvMF

![](../images/2022-06-19-15-17-08.png)

Figure 1 shows the overview of the probabilistic model for ConvMF, which integrates CNN into PMF. 図1はCNNをPMFに統合したConvMFの確率モデルの概要を示したものである。

Suppose we have N users and M items, and observed ratings are represented by $R\in \mathbb{R}^{N\times M}$ matrix. N人のユーザとM個のアイテムがあり、観測された評価行列は$R\in \mathbb{R}^{N\times M}$行列で表現されるとする。

Then, our goal is to find user and item latent models (U ∈ Rk×N and V ∈ Rk×M ) whose product (U T V ) reconstructs the rating matrix R. そして、その積（$U^T \cdot V$）が評価行列 $R$を再構成するユーザとアイテムの潜在モデル（$U\in \mathbb{R}^{k\times N}$ と $V \in \mathbb{R}^{k\times M}$）を見つけることが目的である。

In probabilistic point of view, the conditional distribution over observed ratings is given by ... 確率的な観点からは、観測評価に関する条件付き分布(=**すなわち尤度関数！！**)は次式で与えられる。

$$
p(R|U, V, \sigma^2)
= \prod_{i}^{N} \prod_{j}^{M}
 N(r_{ij}|u_i^T v_j, \sigma^2)^{I_{ij}}
$$

ここで、

- N (x|μ, σ2) is the probability density function of the Gaussian normal distribution with mean μ and variance σ2,
  - $N (x|μ, σ2)$は平均 μ、分散 σ2 の一次元ガウス正規分布の確率密度関数、
- and $I_{ij}$ is an indicator function as mentioned in Section 2.1.
  - $I_{ij}$は 2.1 節で述べたように、「Ratingが観測されていれば1, 未観測であれば0を返す」指標関数である。

As a generative model for user latent models, we place conventional priori, a zero-mean spherical Gaussian prior on user latent models with variance σ2 U.
ユーザ特徴行列(各列ベクトルがユーザ特徴ベクトル)のPriori(事前分布)として、Spherical Gaussian priorを選ぶ。(要するに$U_i$間は独立、各$U_i$はD次元正規分布に従って生成されると仮定！)
以下の式を見ればわかる！

$$
p(U|\sigma^2_U) = \prod_{i}^{N} N(u_i|\mathbf{0}, \sigma_U^2 I)
$$

However, unlike the probabilistic model for item latent models in conventional PMF, we assume that an item latent model is generated from three variables: しかし、**従来のPMF(確率的行列分解)におけるアイテム特徴行列の確率モデルとは異なり**、今回のアイテム特徴行列は以下の３変数から生成される：

- 1） internal weights W in our CNN1 我々のCNN1における内部重みW、
- 2）Xj representing the document of item j項目jの文書を表すXj、
- 3）epsilon variable as Gaussian noise ガウス雑音としてのε変数

$$
v_j = cnn(W, X_j) + \epsilon_j \\
\epsilon_j \sim N(\mathbf{0}, \sigma^2_V I)
$$

For each weight wk in W , we place zero-mean spherical Gaussian prior, the most commonly used prior.また、Wの各重み$w_k$に対して、最も一般的に用いられるゼロ平均の球形ガウス事前分布（=>つまり平均ベクトル0の多次元の正規分布!）を設定する。

$$
p(W|\sigma^2_W) = \prod_k N(w_k|0, \sigma_W^2) \\
(各w_kは独立だった！なので同時分布は一次元正規分布の積)
$$

Accordingly, the conditional distribution over item latent models is given by...したがって、アイテム特徴行列に対する条件付き分布は次式で与えられる。

$$
p(V|W, X, \sigma^2_V) = \prod_j^{M}
N(\mathbf{\mu} = v_j|cnn(W,X_j), \Omega = \sigma_V^2I)
$$

ここで、

- X is the set of description documents of items. Xはアイテムの記述文書の集合
  - =>つまり、X_jはアイテムjの特徴量！
- CNNモデルから得られるDocument latent vactor($cnn(W,X_j)$)はガウス分布の平均として用いられている。
  - it plays an **important role as a bridge between CNN and PMF** that helps to fully analyze both description **documents** and **ratings**.**CNNとPMFの橋渡し**として、**説明文書**(すなわち、アイテムが持つ特徴量、コンテキスト)と**評価**(Explicit or Implicit feedback)の両方を完全に分析するために重要な役割を果たす。
- アイテムのガウスノイズ($\epsilon_j \sim N(\mathbf{0}, \sigma^2_V I)$)はガウス分布の分散として用いられる。

## CNN Architecture of ConvMF

The objective of our CNN architecture is to generate document latent vectors from documents of items, which are used to compose the item latent models with epsilon variables. 本CNNアーキテクチャの目的は、相手うの文書からdocument latent vectors(文書潜在ベクトル)を生成し、それを用いてイプシロン変数でitem latent models(アイテム特徴行列)を構成することである。

Figure 2 shows our CNN architecture that consists of four layers; 1) embedding layer, 2) convolution layer, 3) pooling layer, and 4) output layer.図2は我々のCNNアーキテクチャを示し、1）埋め込み層、2）畳み込み層、3）プーリング層、4）出力層の4層から構成されている。

![](../images/2022-06-19-19-58-28.png)

### Embedding Layer 埋め込み層

- 埋め込み層は、**生のDocumentを、次の畳み込み層のために、文書を表す密な数値行列に変換**する。
- 具体的には、Documentを$l$個の単語の列と見なし、**文書中の単語のベクトルを連結して行列として表現**する。
- 単語ベクトルはランダムに初期化されるか、Glove[18]のような事前に学習された単語埋め込みモデルで初期化される。
- この単語ベクトルは、さらに最適化処理によって学習される。
- そして、文書行列$D \in \mathbb{R}^{p\timesl}$は次のようになる。

$$
D = [
\begin{array}{cc}
   & | & | & | & \\
  \cdots & w_{i-1} & w_{i} & w_{i+1} & \cdots \\
   & | & | & | & \\
\end{array}
]
$$

ここで

- $l$は文書の長さ(単語の数), l is the length of the document
- $p$は各単語ベクトル$w_i$の埋め込み次元の大きさである。p is the size of embedding dimension for each word wi.

### Convolution Layer 畳み込み層

- The convolution layer extracts contextual features. 畳み込み層は文脈の特徴を抽出する。
- As we’ve discussed in Section 2.2, documents are inherently different from signal processing or computer vision in the nature of contextual information. 2.2 節で述べたように、**ドキュメントは、信号処理やコンピュータビジョンとは本質的に異なる文脈情報**を持っている。
  - Thus, we use the convolution architecture in [2, 11] to analyze documents properly. そこで、[2, 11]の畳み込みアーキテクチャを用いて、文書を適切に解析する。
- **畳み込み層によって抽出される文脈特徴 ** $c_i^j \in \mathbb{R}$ は、j 番目の共有重み $W_{c}^j \in \mathbb{R}^{p\times ws}$ によって抽出される。その**Window size $ws$ は周囲の単語数を決定**する。

$$
c_i^j = f(W_c^j * D_{(:, i:(i+ws -1))} + b_c^j) \tag{1}
$$

ここで、

- $*$は畳み込み演算子(Convolution operator)
- $b_c^j$は$W_c^j$のバイアス。
- $f$は非線形活性化関数(non-linear activation function)多分Reluとか！
  - シグモイド、tanh、rectified linear unit (ReLU)などの非線形活性化関数のうち、最適化の収束が遅く、局所最小値が悪くなる可能性のあるvanish gradientの問題を避けるためにReLUを用いる（あたってた！）
- なお、**ここでの$i$は、ユーザを意味するのではなく、Dを畳み込む事で生成される「Contextual feature vector」の要素数を表すindex！ jはアイテムjでOK！(ではなかった！共有重みの添字だった！)**

そして、$W_j^c$を持つDocument jの文脈特徴ベクトル(Contextual feature vector)$c^{j}\in \mathbb{R}^{l-ws +1}$が以下の式(2)によって構成される。

$$
c_j = [ c_1^j, c_2^j, \cdots, c_i^j, \cdots, c_{l-ws+1}^j]
$$

しかし、1つの共有重みShared Weightは、1種類の文脈特徴を捉える。
そこで、**複数の共有重みを用いて複数種類の文脈特徴を捉える**ことで、$W_c$の数$n_c$と同数の文脈特徴ベクトルを生成することが可能となる。
（すなわち、$W_c^j where j = 1,2, \cdots, n_c$

### Pooling Layer プーリング層

The pooling layer **extracts representative features from the convolution layer**, and also deals with variable lengths of documents via **pooling operation that constructs a fixed-length feature vector**. プーリング層は、**畳み込み層から代表的な特徴を抽出**し、**固定長の特徴ベクトルを構築するプーリング操作**によって、文書の可変長に対処する。

After the convolution layer, a document is represented as nc contextual feature vectors, where each contextual feature vector has variable length (i.e., l − ws + 1 contextual feature). 畳み込み層の出力後、ドキュメントは$n_c$ 個の文脈的特徴ベクトルとして表現され，**各文脈特徴ベクトルは可変長**である（すなわち、$l - ws + 1$ 個の文脈特徴）
(つまり$l$がドキュメントの長さ(=単語数)なので、各アイテムによって文脈特徴的特徴ベクトルの長さ(=次元数)が異なる！って事??)

However, such representation imposes two problems: しかし、このような表現では問題が２つある。

- 1）there are too many contextual features ci, where most contextual features might not help enhance the performance,文脈特徴量$c_i$が多すぎて、ほとんどの文脈特徴量が性能向上に寄与しない可能性がある
- 2） the length of contextual feature vectors varies, which makes it difficult to construct the following layers. 文脈特徴ベクトルの長さが変化し、後続の層の構築が困難になる、という問題がある。

Therefore, we utilize max-pooling, which reduces the representation of a document into a nc fixed-length vector by extracting only the maximum contextual feature from each contextual feature vector as follows.そこで、以下のように、pooling層を使って各文脈特徴ベクトルから**最大の文脈特徴のみを抽出**し、**文書の表現を$n_c$個の固定長ベクトルに縮小するmax-pooling**を利用する。
(シンプルに、可変長の各ベクトルから、要素の値が大きいもののみを残すって事か！)

$$
d_f = [max(c^1), max(c^2), \cdots, max(c^j), \cdts, max(c^{n_c})]
$$

ここで、

- $c^j$はj番目の共有重みW j cによって抽出された長さl-ws+1の文脈的な特徴ベクトル(?)

### Output Layer 出力層

Generally, at output layer, high-level features obtained from the previous layer should be converted for a specific task. 一般に、出力層では、**前の層で得られた高次の素性 を、特定のタスクのために変換**する必要がある。

Thus, we project df on a k-dimensional space of user and item latent models for our recommendation task, which finally produces a document latent vector by using conventional nonlinear projection:そこで、推薦タスクのために、ユーザ潜在モデルと項目潜在モデルの$k$次元空間に$d_f$を射影し、最終的に従来の非線形射影を用いて文書潜在ベクトルを生成する:

$$
s = \tanh (W_{f2} {\tanh(W_{f1}d_f + d_{f1})} + b_{f_2}) \tag{3}
$$

ここで、

- $W_{f_1}\in \mathbb{R}^{f \times n_c}$と$W_{f_2}\in \mathbb{R}^{k \times f}$は、projection matrices。＝＞全結合層の重み？？
- $b_{f_1}\in \mathbb{R}^f$と$b_{f_1}\in \mathbb{R}^k$はbias vector for $W_{f1}$と$W_{f2}$
- $s \in \mathbb{R}^k$
- 忘れてるかもしれないけど、kは潜在ベクトルの数！！(ユーザ特徴ベクトル、アイテム特徴ベクトルの縦の長さ！)

Eventually, through the above processes, our CNN architecture becomes **a function that takes a raw document as input, and returns latent vectors of each documents as output**:最終的に、上記のプロセスを経て、我々のCNNアーキテクチャは、**生の文書を入力とし、各文書の潜在的なベクトルを出力として返す**関数となる。
つまりこう！

$$
s_j = cnn(W, X_j) \tag{4}
$$

ここで、

- $W$ denotes all the weight and bias variables to prevent clutter. Wは乱雑さを防ぐための**全ての重み変数とバイアス変数**を示す。(つまり推定されるパラメータ)
- $X_j$はアイテムjのDocument。
- $s_j$はアイテムjのDocument潜在ベクトル。

# Optimization Methodology

To optimize the variables such as **user latent models, item latent models, weight and bias variables of CNN**, we use maximum a posteriori (MAP) estimation as follows. **ユーザ潜在モデル、アイテム潜在モデル、CNNの重み&バイアスなどのパラメータ**を最適化するために、以下のように事後分布最大化推定（**MAP推定**）を行う。

$$
\max_{U, V, W} p(U, V, W|R, X, \sigma^2, \sigma_U^2, \sigma_V^2, \sigma_W^2) \\
= \max_{U, V, W}[尤度関数 \times 事前分布] \\
= \max_{U, V, W}[
  p(R|U, V, \sigma^2)
  \cdot p(U|\sigma_U^2)
  \cdot p(V|W, X, \sigma_V^2)
  \cdot p(W|\sigma_W^2)
  ]
  \tag{5}
$$

By taking negative logarithm on Eqn.(5), it is reformulated as follows.式(5)を負対数化(=対数とってマイナスを掛ける！)して、いい感じに変形する($\sigma^2$で割る!)と、以下のようになる。

$$
L(U,V,W) = \frac{1}{2} \sum_{i}^N \sum_{j}^M I_{ij}(r_{ij} - u_{i}^T v_j)^2 \\
  + \frac{\lambda_U}{2} \sum_{i}^N||u_i||^2 \\
  + \frac{\lambda_V}{2} \sum_{j}^M ||v_j - cnn(W,X_j)||^2 \\
  + \frac{\lambda_W}{2} \sum_{k}^{|W_k|}||w_k||^2
\tag{6}

\\
(
\lambda_U = \frac{\sigma^2}{\sigma_U^2},
\lambda_V = \frac{\sigma^2}{\sigma_V^2},
\lambda_W = \frac{\sigma}{\sigma_W^2}
)
$$

We adopt coordinate descent, which iteratively optimizes a latent variable while fixing the remaining variables. そこで、残 りの変数を固定したまま潜在変数を反復して最適化する座標降下を採用 する。(要するにAlternating Least Square??)

Specifically, Eqn.(6) becomes a quadratic function with respect to U (or V ) while temporarily assuming W and V (or U ) to be constant.具体的には、W と V（または U）を一時的に一定とし、式（6）は U（または V）に関して二次関数となる。 Then, the optimal solution of U (or V ) can be analytically computed in a closed form by simply differentiating the optimization function L with respect to ui (or vj) as follows.そして、U （またはV ）の最適解は、最適化関数L をui （またはvj ）に関して以下のように微分するだけで、**閉形式(closed-form, 要するに解析的に解ける式？)で解析的に計算**することができる。

$$
u_i \leftarrow (VI_i V^T + \lambda_U I_K)^{-1}VR_i \tag{7}
$$

$$
v_j \leftarrow (U I_j U^T + \lambda_V I_K)^{-1}(UR_j + \lambda_V \cdot cnn(W, X_j)) \tag{8}
$$

(ここは通常のALSによるMFと同じ印象を受けるなぁ...)

where

- ユーザiについて
  - $I_i$ は$I_{ij} , (j=1, \cdots, M)$を対角要素とする対角行列。
  - $R_i$ はユーザiについて$(r_{ij})_{j=1}^M$とするベクトル。
    - つまり、ユーザiの各アイテムjに対する評価値が入ったベクトル!
- アイテムjについて
  - $I_j$と$R_j$の定義は、$I_i$と$R_i$のものと同様。
  - 式(8)はアイテム潜在ベクトル$v_j$を生成する際のCNNのDocument潜在ベクトル$s_j = cnn(W, X_j)$の効果を示している。
  - $\lambda_V$はバランシングパラメータ(要は重み付け平均みたいな?, 意味合いとしては正則化項のハイパラでしょ?)になる。

However, W cannot be optimized by an analytic solution as we do for U and V because W is closely related to the features in CNN architecture such as max-pooling layers and non-linear activation functions. しかし、Wは最大プール層や非線形活性化関数などCNNアーキテクチャの特徴と密接に関係しているため、UやVのように**解析的な解法で最適化することはできない**。

Nonetheless, we observe that L can be interpreted as a squared error function with L2 regularized terms as follows when U and V are temporarily constant.それでも、**UとVが一時的に一定であるとき**、Lは以下のように**L2正則化項を持つ二乗誤差関数**として解釈できることがわかる。
(つまり式(6)をUとVが定数と仮定した時Ver.)

$$
\varepsilon(W) = \frac{\lambda_V}{2} \sum_{j}^M ||v_j - cnn(W,X_j)||^2 \\
+ \frac{\lambda_W}{2} \sum_{k}^{|W_k|}||w_k||^2 + constant
\tag{9}
$$

To optimize W , we use back propagation algorithm. (Recall that W is the weights and biases of each layer.)W を最適化するために、**バックプロパゲーションアルゴリズムを使用**する。(Wは各層の重みとバイアスであることを想起してほしい)。

(=>つまり、式(9)を目的関数としたNNの勾配降下法か！)

The overall optimization process (U, V and W are alternatively updated) is repeated until convergence.
**全体の最適化処理（U, V, Wは交互に更新される）は収束するまで繰り返される**。
With optimized U , V , and W , finally we can predict unknown ratings of users on items:
最適化されたU、V、Wにより、最終的にアイテムに対するユーザの未知の評価を予測することができる。

$$
r_{ij} \approx E[r_{ij}|u_i^T v_j, \sigma^2] \\
= u_i^T v_j = u_i^T \cdot (cnn(W, X_j) + \epsilon_j)
$$

$v_j = cnn(W, X_j) + \epsilon_j$だったことを思い出してほしい...!

## Time Complexity Analysis 時間複雑性解析

For each epoch, all user and item latent models are updated in O(k2nR + k3N + k3M ), where nR is the number of observed ratings. Note that document latent vectors are computed while updating W .
各エポックにおいて、全てのユーザとアイテムの潜在モデルを$O(k^2n_R + k^3N + k^3M )$で更新する（ここで$n_R$は観測された評価の数)

Time complexity for updating W is dominated by the computation of convolution layer, and thus all weight and bias variables of CNN are updated in O(nc · p · l · M ).
Wの更新にかかる時間は畳み込み層の計算に支配されるため，CNNのすべての重み変数とバイアス変数の更新は$O(n_c \cdot  p \cdot l \cdot M)$で行われる．


As a result, the total time complexity per epoch is O(k2nR +k3N +k3M +nc ·p·l·M ), and this optimization process scales linearly with the size of given data.
その結果、エポックあたりの総時間は $O(k^2n_R +k^3N +k^3M +n_c \cdot p\cdot l\cdot M)$となり、この最適化処理は与えられたデータのサイズに比例してスケールする。


