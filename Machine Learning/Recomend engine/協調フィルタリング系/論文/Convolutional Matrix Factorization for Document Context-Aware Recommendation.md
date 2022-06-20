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

### Output Layer 出力層
