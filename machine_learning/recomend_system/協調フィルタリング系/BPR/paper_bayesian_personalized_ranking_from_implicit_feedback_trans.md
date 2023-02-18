## link

- https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf httpsを使用しています。

## titile # titile

BPR:
BPR
Bayesian Personalized Ranking from Implicit Feedback
暗黙のフィードバックによるベイズ型パーソナライズランキング

## abstract アブストラクト

Item recommendation is the task of predicting a personalized ranking on a set of items (e.g. websites, movies, products).
アイテム推薦とは、アイテム（例：ウェブサイト、映画、商品）の集合に対して、パーソナライズされたランキングを予測するタスクである。
In this paper, we investigate the most common scenario with implicit feedback (e.g. clicks, purchases).
本論文では、最も一般的なシナリオである暗黙のフィードバック（例えば、クリック、購入）を調査する。
There are many methods for item recommendation from implicit feedback like matrix factorization (MF) or adaptive knearest-neighbor (kNN).
暗黙のフィードバックからアイテムを推薦する方法として、行列因子法（Matrix Factorization: MF）や適応的最近傍探索法（Adaptive Knearest- Neighbor: kNN）など多くの方法が存在する。
Even though these methods are designed for the item prediction task of personalized ranking, none of them is directly optimized for ranking.
これらの手法はパーソナライズされたランキングのアイテム予測タスクのために設計されているにもかかわらず、ランキングのために直接最適化されているものはない。
In this paper we present a generic optimization criterion BPR-Opt for personalized ranking that is the maximum posterior estimator derived from a Bayesian analysis of the problem.
本論文では、パーソナライズドランキングのための汎用最適化基準BPR-Optを提示する。これは問題のベイズ分析から導かれる最大事後推定値である。
We also provide a generic learning algorithm for optimizing models with respect to BPR-Opt.
また、BPR-Optに関してモデルを最適化するための汎用的な学習アルゴリズムを提供する。
The learning method is based on stochastic gradient descent with bootstrap sampling.
この学習法はブートストラップサンプリングによる確率的勾配降下法に基づいている。
We show how to apply our method to two state-of-the-art recommender models: matrix factorization and adaptive kNN.
我々はこの方法を2つの最新の推薦モデル、行列分解と適応的kNNに適用する方法を示す。
Our experiments indicate that for the task of personalized ranking our optimization method outperforms the standard learning techniques for MF and kNN.
我々の実験は、個人化されたランキングのタスクに対して、我々の最適化手法は、MFとkNNの標準的な学習技術を凌駕することを示している。
The results show the importance of optimizing models for the right criterion.
この結果は、正しい基準でモデルを最適化することの重要性を示している。

# Introduction はじめに

Recommending content is an important task in many information systems.
コンテンツを推薦することは、多くの情報システムにおいて重要なタスクである。
For example online shopping websites like Amazon give each customer personalized recommendations of products that the user might be interested in.
例えば、Amazonのようなオンラインショッピングサイトでは、ユーザーが興味を持ちそうな商品を、それぞれの顧客にパーソナライズして推薦している。
Other examples are video portals like YouTube that recommend movies to customers.
また、YouTubeのような動画ポータルサイトでは、顧客に映画を推薦している。
Personalization is attractive both for content providers, who can increase sales or views, and for customers, who can find interesting content more easily.
パーソナライゼーションは、コンテンツ提供者にとっては売上や視聴回数を増やすことができ、顧客にとっては興味深いコンテンツをより簡単に見つけることができるという点で魅力的である。
In this paper, we focus on item recommendation.
本論文では、項目推薦に注目する。
The task of item recommendation is to create a user-specific ranking for a set of items.
項目推薦の課題は、ある項目の集合に対して、ユーザー固有のランキングを作成することである。
Preferences of users about items are learned from the user’s past interaction with the system – e.g. his buying history, viewing history, etc.
アイテムに関するユーザーの好みは、ユーザーの過去のシステムとのインタラクション（例えば、購入履歴、閲覧履歴など）から学習される。

Recommender systems are an active topic of research.
レコメンダーシステムは活発な研究テーマである。
Most recent work is on scenarios where users provide explicit feedback, e.g. in terms of ratings.
最近の研究のほとんどは、ユーザが評価などの形で明示的にフィードバックを行うシナリオに関するものである。
Nevertheless, in real-world scenarios most feedback is not explicit but implicit.
しかし、実世界のシナリオでは、ほとんどのフィードバックは明示的ではなく、暗黙的である。
Implicit feedback is tracked automatically, like monitoring clicks, view times, purchases, etc.
暗黙的なフィードバックは、クリック数、視聴時間、購入数などを自動的に追跡することができる。
Thus it is much easier to collect, because the user has not to express his taste explicitly.
そのため、ユーザーは自分の好みを明示的に表現する必要がなく、収集が非常に容易である。
In fact implicit feedback is already available in almost any information system – e.g. web servers record any page access in log files.
実際、暗黙のフィードバックは、ほとんどすべての情報システムで利用可能である。例えば、ウェブサーバーはすべてのページアクセスをログファイルに記録する。

In this paper we present a generic method for learning models for personalized ranking.
本論文では、パーソナライズされたランキングのためのモデルを学習するための汎用的な方法を紹介する。
The contributions of this work are:
この研究の貢献は以下の通りである。

- 1. We present the generic optimization criterion BPR-Opt derived from the maximum posterior estimator for optimal personalized ranking. We show the analogies of BPR-Opt to maximization of the area under ROC curve. 1.パーソナライズされた最適なランキングのための最大事後推定量から導かれる汎用最適化基準BPR-Optを提示する。 BPR-OptのROC曲線下面積の最大化へのアナロジーを示す。

- 2. For maximizing BPR-Opt, we propose the generic learning algorithm LearnBPR that is based on stochastic gradient descent with bootstrap sampling of training triples. We show that our algorithm is superior to standard gradient descent techniques for optimizing w.r.t. BPR-Opt. 2.BPR-Optを最大化するために、我々は確率的勾配降下法とブートストラップサンプリングに基づく汎用学習アルゴリズムLearnBPRを提案する。 このアルゴリズムは、BPR-Optの最適化において、標準的な勾配降下法より優れていることを示す。

- 3. We show how to apply LearnBPR to two stateof-the-art recommender model classes. 3.LearnBPRを2つの最先端レコメンダーモデルクラスに適用する方法を示す。

- 4. Our experiments empirically show that for the task of of personalized ranking, learning a model with BPR outperforms other learning methods. 4. 我々の実験では、個人化ランキングのタスクに対して、BPRによるモデルの学習が他の学習方法よりも優れていることが実証的に示された。

# Related Work 関連作品

The most popular model for recommender systems is k-nearest neighbor (kNN) collaborative filtering [2].
レコメンダーシステムで最も人気のあるモデルは k-nearest neighbor (kNN) 協調フィルタリングである [2]．
Traditionally the similarity matrix of kNN is computed by heuristics – e.g. the Pearson correlation – but in recent work [8] the similarity matrix is treated as model parameters and is learned specifically for the task.
伝統的に kNN の類似度行列はヒューリスティックに、例えばピアソン相関によって計算されるが、最近の研究 [8] では類似度行列はモデルパラメータとして扱われ、タスクのために特別に学習される。
Recently, matrix factorization (MF) has become very popular in recommender systems both for implicit and explicit feedback.
最近、推薦システムにおいて、暗黙的・明示的フィードバックのために、行列分解(MF)が非常に一般的になってきた。
In early work [13] singular value decomposition (SVD) has been proposed to learn the feature matrices.
初期の研究[13]では、特徴行列を学習するために特異値分解(SVD)が提案されている。
MF models learned by SVD have shown to be very prone to overfitting.
しかし，SVDによって学習されたMFモデルはオーバーフィットに陥りやすいことが分かっている．
Thus regularized learning methods have been proposed.
そこで，正則化された学習方法が提案されている．
For item prediction Hu et al. [5] and Pan et al. [10] propose a regularized least-square optimization with case weights (WR-MF).
Huら[5]とPanら[10]は項目予測に対して，事例重み付き正則化最小二乗最適化法(WR-MF)を提案している．
The case weights can be used to reduce the impact of negative examples.
事例重みは否定的な事例の影響を軽減するために用いることができる．
Hofmann [4] proposes a probabilistic latent semantic model for item recommendation.
Hofmann [4]は項目推薦のための確率的潜在的意味モデルを提案している．
Schmidt-Thieme [14] converts the problem into a multi-class problem and solves it with a set of binary classifiers.
Schmidt-Thieme [14] はこの問題をマルチクラス問題に変換し，バイナリ分類器のセットで解決している．
Even though all the work on item prediction discussed above is evaluated on personalized ranking datasets, none of these methods directly optimizes its model parameters for ranking.
上記のアイテム予測に関するすべての研究はパーソナライズされたランキングデータセットで評価されているが、これらの方法のいずれもランキングのためにモデルパラメータを直接最適化していない。
Instead they optimize to predict if an item is selected by a user or not.
その代わりに、アイテムがユーザによって選択されるかどうかを予測するために最適化される。
In our work we derive an optimization criterion for personalized ranking that is based on pairs of items (i.e. the user-specific order of two items).
我々の研究では、アイテムのペア（すなわち、2つのアイテムのユーザー固有の順序）に基づくパーソナライズされたランキングのための最適化基準を導出する。
We will show how state-of-the-art models like MF or adaptive kNN can be optimized with respect to this criterion to provide better ranking quality than with usual learning methods.
我々は、MFやadaptive kNNのような最先端のモデルが、この基準に関してどのように最適化され、通常の学習方法よりも優れたランキング品質を提供することができるかを示す。
A detailed discussion of the relationship between our approach and the WRMF approach of Hu et al. [5] and Pan et al. [10] as well as maximum margin matrix factorization [15] can be found in Section 5.
我々のアプローチとHuら[5]やPanら[10]のWRMFアプローチや最大マージン行列分解[15]との関係についてはセクション5で詳しく説明する。
In Section 4.1.1, we will also discuss the relations of our optimization criterion to AUC optimization like in [3].
また、セクション4.1.1では、我々の最適化基準と[3]のようなAUC最適化との関係についても議論する。

In this paper, we focus on offline learning of the model parameters.
この論文では、モデルパラメータのオフライン学習に焦点を当てる。
Extending the learning method to online learning scenarios – e.g. a new user is added and his history increases from 0 to 1, 2, . . . feedback events – has already been studied for MF for the related task of rating prediction [11].
この学習方法をオンライン学習シナリオに拡張すること、例えば、新しいユーザーが追加され、その履歴が0から1、2、...とフィードバックイベントに増加することは、関連タスクである視聴率予測用のMFについて既に研究されている[11]。
The same fold-in strategy can be used for BPR.
同じフォールドイン戦略をBPRに用いることができる。

There is also related work on learning to rank with non-collaborative models.
また、非協力的なモデルを用いた順位付けの学習に関する関連研究もある。
One direction is to model distributions on permutations [7, 6].
一つの方向性は並べ換えに関する分布をモデル化することである[7, 6]。
Burges et al. [1] optimize a neural network model for ranking using gradient descent.
Burgesら[1]は勾配降下法を用いてランキングのためのニューラルネットワークモデルを最適化する。
All these approaches learn only one ranking – i.e. they are non-personalized.
これらのアプローチはすべて一つのランキングしか学習しない、つまり非個人化である。
In contrast to this, our models are collaborative models that learn personalized rankings, i.e. one individual ranking per user.
これに対して，我々のモデルは協調モデルであり，個人化されたランキングを学習する，つまり，**ユーザごとに1つの個人的なランキングを学習**する．
In our evaluation, we show empirically that in typical recommender settings our personalized BPR model outperforms even the theoretical upper bound for non-personalized ranking.
我々の評価では、典型的なレコメンダー設定において、我々のパーソナライズドBPRモデルが非パーソナライズドランキングの理論的上限値さえも上回ることを経験的に示している。

# Personalized Ranking パーソナライズド・ランキング

The task of personalized ranking is to provide a user with a ranked list of items.
パーソナライズド・ランキングのタスクは、ユーザーにアイテムのランク付けされたリストを提供することである。
This is also called item recommendation.
これは、アイテム推薦とも呼ばれます。
An example is an online shop that wants to recommend a personalized ranked list of items that the user might want to buy.
例えば、オンラインショップが、ユーザーが買いたいと思うようなアイテムのパーソナライズされたランク付けされたリストを推薦したい場合である。
In this paper we investigate scenarios where the ranking has to be inferred from the implicit behavior (e.g. purchases in the past) of the user.
この論文では、ユーザーの暗黙の行動（例えば、過去の購入履歴）からランキングを推定しなければならないシナリオを調査している。
Interesting about implicit feedback systems is that only positive observations are available.
暗黙のフィードバックシステムで興味深いのは、肯定的な観測のみが利用可能であることである。
The non-observed user-item pairs – e.g. a user has not bought an item yet – are a mixture of real negative feedback (the user is not interested in buying the item) and missing values (the user might want to buy the item in the future).
観測されないユーザーとアイテムのペア（例えば、ユーザーはまだアイテムを購入していない）は、実際のネガティブフィードバック（ユーザーはアイテムを購入することに興味がない）と欠損値（ユーザーは将来的にアイテムを購入したいかもしれない）の混合物である。

## Formalization 形式化

Let U be the set of all users and I the set of all items.
Uを全ユーザの集合、Iを全アイテムの集合とする。
In our scenario implicit feedback $S \subset U×I$ is available (see left side of Figure 1).
このシナリオでは、暗黙のフィードバック$S \subset U×I$が利用可能である（図1の左側参照）。
Examples for such feedback are purchases in an online shop, views in a video portal or clicks on a website.
このようなフィードバックの例として、オンラインショップでの購入、ビデオポータルでの視聴、ウェブサイトでのクリックがある。
The task of the recommender system is now to provide the user with a personalized total ranking $>_u \subset I^2$ of all items, where $>_u$ has to meet the properties of a total order:
ここで、$>_u$は総順序の特性を満たさなければならない。

$$
\forall i, j \in I: i \neq j => i >_u j \lor j >_u i \tag{totality}
$$

$$
\forall i, j \in I:  i >_u j \land j >_u i =>i=j \tag{antisymmetry}
$$

$$
\forall i, j, k \in I:  i >_u j \land j >_u k => i >_u k \tag{transitivity}


$$

- $\forall$=任意の、全ての $\forall$=arbitrary, all

- $\lor$ = 論理和(or), "または" $\lor$ = logical OR, "or"

- $\land$ = 論理積(and), "かつ" $\land$ = logical product(and), "and"

- $\subset$ = 部分集合. subset$ = 部分集合。

For convenience we also define:
また、便宜上、以下のように定義する。

$$
I_u^+ := {i \in I : (u,i) \in S}
\\
U_i^+ := {u \in U : (u,i) \in S}
$$

## Analysis of the problem setting 問題設定の分析

As we have indicated before, in implicit feedback systems only positive classes are observed.
前にも述べたように、暗黙のフィードバックシステムでは、正のクラスのみが観測される。
The remaining data is a mixture of actually negative and missing values.
残りのデータは、実際には負の値や欠損値が混在している。
The most common approach for coping with the missing value problem is to ignore all of them but then typical machine learning models are unable to learn anything, because they cannot distinguish between the two levels anymore.
欠損値問題に対処する最も一般的なアプローチは、欠損値をすべて無視することであるが、そうすると典型的な機械学習モデルは、2つのレベルを区別できなくなり、何も学習できなくなる。

The usual approach for item recommenders is to predict a personalized score ˆxui for an item that reflects the preference of the user for the item.
アイテム推薦器の通常のアプローチは、アイテムに対するユーザの好みを反映したパーソナライズドスコアˆxuiを予測することである。
Then the items are ranked by sorting them according to that score.
そして、そのスコアに従ってアイテムをソートすることでランク付けを行う。
Machine learning approaches for item recommenders [5, 10] typically create the training data from S by giving pairs $(u, i) \in S$ a positive class label and all other combinations in $(U × I) \setminus S$ a negative one (see Figure 1).
アイテム推薦器の機械学習アプローチ[5, 10]では、S$に含まれるペア$(u, i) \に正のクラスラベルを、$(U × I) \setminus S$に含まれる他の組み合わせに負のクラスラベルを与えてSから学習データを作成することが一般的である（図1参照）。
Then a model is fitted to this data.
そして、このデータに対してモデルを当てはめる。
That means the model is optimized to predict the value 1 for elements in S and 0 for the rest.
つまり、Sに含まれる要素は値1、それ以外は値0と予測するようにモデルを最適化する。
The problem with this approach is that all elements the model should rank in the future ($(U × I) \setminus S$) are presented to the learning algorithm as negative feedback during training.
この方法の問題点は、学習時にモデルが将来順位をつけるべき要素（$(U × I) \setminus S$）がすべて負のフィードバックとして学習アルゴリズムに提示されてしまうことである。
That means a model with enough expressiveness (that can fit the training data exactly) cannot rank at all as it predicts only 0s.
つまり、十分な表現力を持つ（学習データにぴったりとフィットする）モデルは、0ばかりを予測してしまうため、全く順位がつけられないということです。
The only reason why such machine learning methods can predict rankings are strategies to prevent overfitting, like regularization.
このような機械学習法が順位を予測できるのは、正則化のようなオーバーフィッティングを防ぐための戦略だけである。

We use a different approach by using item pairs as training data and optimize for correctly ranking item pairs instead of scoring single items as this better represents the problem than just replacing missing values with negative ones.
我々は、学習データとして項目ペアを使用し、単項目のスコアではなく、項目ペアを正しくランク付けすることで最適化するアプローチをとっている。これは、単に欠損値を負の値で置き換えるよりも問題をよく表している。
From S we try to reconstruct for each user parts of $>_u$.
Sから各ユーザーの$>_u$の部分を再構築することを試みる。
If an item i has been viewed by user u – i.e. $(u, i) \in S$ – then we assume that the user prefers this item over all other non-observed items.
もしあるアイテムiがユーザuによって閲覧されたことがあれば（すなわち$(u, i) \in S$）、そのユーザは他のすべての非観測アイテムよりもこのアイテムを好むと仮定する。
E.g. in Figure 2 user $u_1$ has viewed item $i_2$ but not item $i_1$, so we assume that this user prefers item $i_2$ over $i_1$: $i_2 >_u i_1$.
例えば、図2において、ユーザ $u_1$ はアイテム $i_2$ を見たが、アイテム $i_1$ は見ていないので、このユーザはアイテム $i_2$ を $i_1$ より好むと仮定する： $i_2 >_u i_1$.
For items that have both been seen by a user, we cannot infer any preference.
両方とも見たことのある項目については、好みを推論することはできない。
The same is true for two items that a user has not seen yet (e.g. item $i_1$ and $i_4$ for user $u_1$).
ユーザがまだ見ていない2つの項目についても同様である（例：ユーザ $u_1$ の項目 $i_1$ と $i_4$ ）。
To formalize this we create training data $D_s :
これを定式化するために、学習データ $D_s :
U × I × I$ by:
U × I × I$ によって作成する。

$$
D_s := {(u,i,j)|i \in I_u^+ \land j \in I\setminus I_u^+}
$$

The semantics of $(u, i, j) \in D_s$ is that user u is assumed to prefer i over j. As $>_u$ is antisymmetric, the negative cases are regarded implicitly.
(u, i, j) \in D_s$ の意味論は、ユーザ u は j よりも i を好むと仮定することである。

Our approach has two advantages:
私たちのアプローチには、2つの利点があります。

- 1. Our training data consists of both positive and negative pairs and missing values. The missing values between two non-observed items are exactly the item pairs that have to be ranked in the future. That means from a pairwise point of view the training data D_s and the test data is disjoint. 1.我々の学習データは正負両方のペアと欠損値からなる。 2つの非観測項目間の欠損値は、まさに将来順位付けされなければならない項目ペアである。 つまり、ペアワイズの観点からは、学習データD_sとテストデータは不連続であることを意味します。

- 2.  The training data is created for the actual objective of ranking, i.e. the observed subset $D_s$ of $>_u$ is used as training data. 2.実際の目的であるランキングのための学習データを作成する。すなわち、$>_u$の観測部分集合$D_s$を学習データとして使用する。

# Bayesian Personalized Ranking (BPR) ベイズパーソナライズドランキング（BPR）

In this section we derive a generic method for solving the personalized ranking task. It consists of the general optimization criterion for personalized ranking, BPR-Opt, which will be derived by a Bayesian analysis of the problem using the likelihood function for $p(i >_u j
\Theta)$ and the prior probability for the model parameter $p(\Theta)$. We show the analogies to the ranking statistic AUC (area under the ROC curve). For learning models with respect to BPR-Opt, we propose the algorithm LearnBPR. Finally, we show how BPROpt and LearnBPR can be applied to two state-ofthe-art recommender algorithms, matrix factorization and adaptive kNN. Optimized with BPR these models are able to generate better rankings than with the usual training methods.

## BPR Optimization Criterion BPR最適化基準

The Bayesian formulation of finding the correct personalized ranking for all items $i \in I$ is to maximize the following posterior probability where $\Theta$ represents the parameter vector of an arbitrary model class (e.g. matrix factorization).
すべての項目$i \in I$に対して正しい個人化ランキングを求めるベイズ定式化は、以下の事後確率を最大化することである。ここで、$Theta$は任意のモデルクラス（例えば、行列分解）のパラメータベクトルを表す。

$$
p(\Theta|>_u) \propto p(>_u|\Theta) p(\Theta)
$$

- $\propto$: 比例. 比例。

Here, $>_u$ is the desired but latent preference structure for user u. All users are presumed to act independently of each other. We also assume the ordering of each pair of items (i, j) for a specific user is independent of the ordering of every other pair. Hence, the above user-specific likelihood function $p(>_u
\Theta)$ can first be rewritten as a product of single densities and second be combined for all users $u \in U$.

$$
\prod_{u \in U} p(>_u | \Theta) = \prod_{(u,i,j) \in U \times I \times I} p(i >_u j|\Theta)^{\epsilon((u,i,j)\in D_s)} \cdot (1 - p(i >_u j|\Theta))^{\epsilon((u,i,j)\in D_s)}
$$

where $\epsilon$ is the indicator function:
ここで、$epsilon$は指標関数である。

$$
\epsilon(b) := 1 \text{ if b is true} \text{ else } 0
$$

Due to the totality and antisymmetry of a sound pairwise ordering scheme the above formula can be simplified to:
健全なペアワイズオーダー方式の全体性と反対称性により、上記の式は次のように簡略化されます。

$$
\prod_{u \in U} p(>_u | \Theta) = \prod_{(u,i,j) \in D_s} p(i >_u j|\Theta)
$$

So far it is generally not guaranteed to get a personalized total order.
これまでのところ、一般に個人的なトータルオーダーを得ることは保証されていない。
In order to establish this, the already mentioned sound properties (totality, antisymmetry and transitivity) need to be fulfilled.
これを成立させるためには、すでに述べた音響特性（全体性、非対称性、推移性）を満たす必要がある。
To do so, we define the individual probability that a user really prefers item i to item j as:
そのために、あるユーザーがアイテムjよりもアイテムiを本当に好む個別確率を次のように定義する。

$$
p(i >_u j|\Theta) := \sigma(\hat{x}_{uij}(\Theta))
$$

where $\sigma$ is the logistic sigmoid:
ここで、$sigma$はロジスティック・シグモイドである。

$$
\sigma(x) := \frac{1}{1 + e^{-x}}
$$

Here $\hat{x}_{uij}(\Theta)$ is an arbitrary real-valued function of the model parameter vector Θ which captures the special relationship between user u, item i and item j. In other words, our generic framework delegates the task of modeling the relationship between u, i and j to an underlying model class like matrix factorization or adaptive kNN, which are in charge of estimating $\hat{x}_{uij}(\Theta)$.
ここで、$hat{x}_{uij}( \Theta)$ は、ユーザu、アイテムi、アイテムjの特別な関係を捉えるモデルパラメータベクトルΘの任意の実数値関数である。言い換えれば、我々の汎用フレームワークは、u、i、j間の関係のモデル化タスクを行列分解や適応的kNNなどの基礎モデルクラスに委ね、それらのクラスは$hat{x}_{uij}( \Theta)$ を推定する責任を有する。
Hence, it becomes feasible to statistically model a personalized total order $>_u$.
したがって、個人化された全順序$>_u$を統計的にモデル化することが可能になる。
For convenience, in the following we will skip the argument $\Theta$ from $\hat{x}_{uij}$.
以下、便宜上、$hat{x}_{uij}$から引数$Theta$を省略する。

So far, we have only discussed the likelihood function.
これまで、尤度関数についてのみ述べてきた。
In order to complete the Bayesian modeling approach of the personalized ranking task, we introduce a general prior density $p(\Theta)$ which is a normal distribution with zero mean and variance-covariance matrix $\Sigma_{\Theta}$.
パーソナライズドランキングタスクのベイズモデリング手法を完成させるために、平均が0で分散共分散行列が$Sigma_{Theta}$の正規分布である一般的な事前密度$p（ \theta）$ を導入する。

$$
p(\Theta) \sim N(0, \Sigma_{\Theta})
$$

In the following, to reduce the number of unknown hyperparameters we set $\Sigma_{\Theta} = \lambda_{\Theta} I$.
以下では、未知のハイパーパラメータの数を減らすために、$Sigma_{Theta} = \lambda_{Theta} I$とします。
Now we can formulate the maximum posterior estimator to derive our generic optimization criterion for personalized ranking BPR-Opt.
ここで、最大事後推定量を定式化し、個人化ランキングの汎用最適化基準BPR-Optを導出することができます。

$$
BPR-O_{PT}:= \ln \prod_{u \in U} p(\Theta| >_u) \\
= \ln \prod_{u \in U} p(>_u | \Theta) p(\Theta) \\
= \ln \prod_{(u,i,j) \in D_s} \sigma(\hat{x}_{uij}(\Theta)) p(\Theta) \\
= \sum_{(u,i,j) \in D_s} \ln \sigma(\hat{x}_{uij}(\Theta)) + \ln p(\Theta) \\
= \sum_{(u,i,j) \in D_s} \ln \sigma(\hat{x}_{uij}(\Theta)) -  \lambda_{\Theta}||\Theta||^2 \\


$$

where $\lambda_{\Theta}$ are model specific regularization parameters.
ここで、$lambda_{Theta}$はモデル固有の正則化パラメータである。

### Analogies to AUC optimization AUC最適化へのアナロジー

With this formulation of the Bayesian Personalized Ranking (BPR) scheme, it is now easy to grasp the analogy between BPR and AUC.
このようにBayesian Personalized Ranking (BPR) スキームを定式化すると、BPRとAUCの類似性を容易に把握することができるようになる。
The AUC per user is usually defined as:
ユーザーごとのAUCは通常次のように定義される。

$$
\text{AUC}(u) := \frac{1}{|I_u^+||I \setminus I_u^+|} \sum_{i \in I_u^+} \sum_{j \in |I \setminus I_u^+|} \epsilon(\hat{x}_{uij} > 0)
$$

Hence the average AUC is:
したがって、平均的なAUCは

$$
\text{AUC} := \frac{1}{|U|} \sum_{u \in U} \text{AUC}(u)
$$

With our notation of $D_s$ this can be written as:
D_s$の表記で、これは次のように書くことができる。

$$
\text{AUC}(u):= \sum_{(u,i,j) \in D_S} z_u \epsilon(\hat{x}_{uij} > 0)
\tag{1}
$$

where $z_u$ is the normalizing constant:
ここで、$z_u$は正規化定数である。

$$
z_u = \frac{1}{|U| |I_u^+||I \setminus I_u^+|}
$$

The analogy between (1) and BPR-Opt is obvious.
(1)とBPR-Optの類似性は明白である。
Besides the normalizing constant $z_u$ they only differ in the loss function.
正規化定数$z_u$の他には、損失関数が異なるだけである。
The AUC uses the non-differentiable loss $\epsilon(x > 0)$ which is identical to the Heaviside function:
AUCはHeaviside関数と同じ非微分損失$epsilon(x > 0)$を用いる。

$$
\epsilon(x > 0) = H(x) := 1 \text{ x>0,} \text{else } 0
$$

Instead we use the differentiable loss ln $\sigma(x)$.
その代わりに、微分可能な損失 ln $sigma(x)$ を使用する。
It is common practice to replace the non-differentiable Heaviside function when optimizing for AUC [3].
AUCを最適化する際に、微分不可能なHeaviside関数を置き換えるのは一般的な方法である[3]。
Often the choice of the substitution is heuristic and a similarly shaped function like $\sigma$ is used (see figure 3).
多くの場合、置き換えの選択はヒューリスティックであり、$sigma$のような類似した形状の関数を用いる（図3参照）。
In this paper, we have derived the alternative substitution ln $\sigma(x)$ that is motivated by the MLE.
本論文では、MLEを動機とする代替代入ln $Θsigma(x)$を導出した。

## BPR Learning Algorithm BPR 学習アルゴリズム

In the last section we have derived an optimization criterion for personalized ranking.
前節では、パーソナライズされたランキングのための最適化基準を導きました。
As the criterion is differentiable, gradient descent based algorithms are an obvious choice for maximization.
この基準は微分可能であるため、勾配降下法に基づくアルゴリズムが最大化のための明らかな選択となります。
But as we will see, standard gradient descent is not the right choice for our problem.
しかし、これから見るように、標準的な勾配降下法は我々の問題にとって正しい選択とは言えない。
To solve this issue we propose LearnBPR, a stochastic gradient-descent algorithm based on bootstrap sampling of training triples (see figure 4).
この問題を解決するために、我々は学習用トリプルのブートストラップサンプリングに基づく確率的勾配降下アルゴリズムであるLearnBPRを提案する（図4参照）。

First of all the gradient of BPR-Opt with respect to the model parameters is:
まず、モデルパラメータに対するBPR-Optの勾配は

$$
\frac{\partial BPR-O_{PT}}{\partial \Theta}
= \sum_{(u,i,j) \in D_S} \frac{\partial}{\partial \Theta} \ln \sigma(\hat{x}_{uij})
- \lambda_{\Theta} \frac{\partial}{\partial \Theta} ||\Theta||^2
\\
\propto
\sum_{(u,i,j) \in D_S} \frac{-e^{-\hat{x}_{uij}}}{1 + e^{-\hat{x}_{uij}}} \frac{\partial}{\partial \Theta} \hat{x}_{uij}
- \lambda_{\Theta} \Theta
$$

The two most common algorithms for gradient descent are either full or stochastic gradient descent.
勾配降下法には、完全勾配法と確率的勾配法の2種類があり、完全勾配法が最も一般的である。
In the first case, in each step the full gradient over all training data is computed and then the model parameters are updated with the learning rate $\alpha$:
最初のケースでは、各ステップですべての学習データに対する完全勾配を計算し、学習率 $alpha$ でモデルパラメータを更新する。

$$
\Theta \leftarrow \Theta - \alpha \frac{\partial BPR-O_{PT}}{\partial \Theta}
$$

In general this approach leads to a descent in the ‘correct’ direction, but convergence is slow. As we have $O(
S

The other popular approach is stochastic gradient descent.
もう1つは確率的勾配降下法（stochastic gradient descent）です。
In this case for each triple $(u, i, j) \in D_S$ an update is performed.
この場合、D_S$の各トリプル$(u, i, j) については、更新が行われる。

$$
\Theta \leftarrow \Theta - \alpha (\sum_{(u,i,j) \in D_S} \frac{e^{-\hat{x}_{uij}}}{1 + e^{-\hat{x}_{uij}}} \frac{\partial}{\partial \Theta} \hat{x}_{uij}
+ \lambda_{\Theta} \Theta)
$$

In general this is a good approach for our skew problem but the order in which the training pairs are traversed is crucial.
一般に、これは我々のスキュー問題に対して良いアプローチですが、学習ペアを走査する順序が重要です。
A typical approach that traverses the data item-wise or user-wise will lead to poor convergence as there are so many consecutive updates on the same user-item pair – i.e. for one user-item pair (u, i) there are many j with $(u, i, j) \in D_S$.
つまり、1つのユーザー項目ペア（u, i）に対して、$(u, i, j) \in D_S$を持つ多くのjが存在するのです。

To solve this issue we suggest to use a stochastic gradient descent algorithm that chooses the triples randomly (uniformly distributed).
この問題を解決するために、トリプルをランダムに（一様に）選択する確率的勾配降下アルゴリズムを使用することを提案する。
With this approach the chances to pick the same user-item combination in consecutive update steps is small.
このアプローチでは、連続した更新ステップで同じユーザー項目の組み合わせを選択する可能性は小さい。
We suggest to use a bootstrap sampling approach with replacement because stopping can be performed at any step.
また、任意のステップで停止が可能であるため、置換を伴うブートストラップ・サンプリング・アプローチを使用することを提案する。
Abandoning the idea of full cycles through the data is especially useful in our case as the number of examples is very large and for convergence often a fraction of a full cycle is sufficient.
データの全サイクルの考えを放棄することは、例数が非常に多く、収束のために全サイクルの数分の一で十分であるため、我々のケースでは特に有用である。
We choose the number of single steps in our evaluation linearly depending on the number of observed positive feedback S.
我々の評価では、観測された正帰還Sの数に応じて、シングルステップの数を線形に選択する。

Figure 5 shows a comparison1 of a typical userwise stochastic gradient descent to our approach LearnBPR with bootstrapping.
図5は、典型的なユーザワイズ確率的勾配降下法と我々のアプローチLearnBPR with bootstrappingの比較1である。
The model is BPRMF with 16 dimensions.
モデルは16次元のBPRMFです。
As you can see LearnBPR converges much faster than user-wise gradient descent.
見ての通り、LearnBPRはユーザーワイズ勾配降下法よりはるかに速く収束する.

## Learning models with BPR BPRによるモデルの学習

In the following we describe two state-of-the-art model classes for item recommendation and how we can learn them with our proposed BPR methods.
以下では、項目推薦のための2つの最新モデルクラスと、それらを我々の提案するBPR手法でどのように学習するかを述べる。
We have chosen the two diverse model classes of matrix factorization [5, 12] and learned k-nearest-neighbor [8].
我々は、行列分解[5, 12]と学習型k-nearest-neighbor[8]という2つの多様なモデルクラスを選択した。
Both classes try to model the hidden preferences of a user on an item.
両クラスとも、あるアイテムに対するユーザの隠れた嗜好をモデル化しようとするものである。
Their prediction is a real number ˆxul per user-item-pair (u, l).
これらの予測はユーザ-アイテムペア(u, l)毎の実数ˆxulである。

Because in our optimization we have triples $(u, i, j) \in DS$, we first decompose the estimator $\hat{x}_{uij}$ and define it as:
今回の最適化では、DS$においてトリプル$(u, i, j) \in DS$があるので、まず、推定量$inthat{x}\_{uij}$を分解して次のように定義します。

$$
\hat{x}_{uij} := \hat{x}_{ui} - \hat{x}_{uj}
$$

Now we can apply any standard collaborative filtering model that predicts $\hat{x}_{ul}$.
これで、$hat{x}_{ul}$を予測する任意の標準的な協調フィルタリングモデルを適用することができます。

It is important to note that even though we use the same models as in other work, we optimize them against another criterion.
重要なのは、他の研究と同じモデルを使用しているにもかかわらず、別の基準に対して最適化を行っていることである。
This will lead to a better ranking because our criterion is optimal for the ranking task.
これは、我々の基準がランキング・タスクに最適であるため、より良いランキングにつながる。
Our criterion does not try to regress a single predictor $\hat{x}_{ul}$ to a single number but instead tries to classify the difference of two predictions $\hat{x}_{ui} - \hat{x}_{uj}$.
我々の基準は、単一の予測値$hat{x}_{ul}$を単一の数値に回帰させようとせず、代わりに2つの予測値$hat{x}_{ui} - \hat{x}_{uj}$ の差を分類しようとするものである。

### Matrix Factorization 行列の因数分解

The problem of predicting $\hat{x}_{ui}$ can be seen as the task of estimating a matrix $X : U × I$. With matrix factorization the target matrix X is approximated by the matrix product of two low-rank matrices $W :
U

$$
\hat{X} := W H^t
$$

where k is the dimensionality
ここで、k は次元数である

$$
\hat{x}_{ui} = w_u \cdot h_i = \sum_{f=1}^k w_{uf} \cdot h_{if}
$$

Besides the dot product in general any kernel can be used like in [11].
ドットプロダクトの他に[11]のように一般的なカーネルを使用することができる。
The model parameters for matrix factorization are $\Theta= (W, H)$.
行列分解におけるモデルパラメータは$Theta= (W, H)$である。
The model parameters can also be seen as latent variables, modeling the nonobserved taste of a user and the non-observed properties of an item.
モデルパラメータは潜在変数とみなすこともでき、ユーザの非観測嗜好やアイテムの非観測特性をモデル化することができる。

In general the best approximation of $\hat{X}$ to X with respect to least-square is achieved by the singular value decomposition (SVD).
一般に、最小二乗に関するXへの$hat{X}$の最良の近似は特異値分解(SVD)によって達成される。
For machine learning tasks, it is known that SVD overfits and therefore many other matrix factorization methods have been proposed, including regularized least square optimization, non-negative factorization, maximum margin factorization, etc.
しかし，機械学習においては，SVDはオーバーフィットすることが知られており，正則化最小二乗最適化，非負値化，最大マージン化など，多くの行列分解法が提案されている．

For the task of ranking, i.e. estimating whether a user prefers one item over another, a better approach is to optimize against the BPR-Opt criterion.
ランキングのタスク、すなわちユーザーがあるアイテムを他のアイテムより好むかどうかを推定するためには、BPR-Opt基準に対して最適化することがより良いアプローチである。
This can be achieved by using our proposed algorithm LearnBPR.
これは我々の提案するアルゴリズムLearnBPRを使用することで達成できる。
As stated before for optimizing with LearnBPR, only the gradient of $\hat{x}_{uij}$ with respect to every model parameter $\theta$ has to be known.
LearnBPRで最適化するために、前述したように、全てのモデルパラメータ$thetta$に関する$hat{x}_{uij}$の勾配のみが分かっている必要があります。
For the matrix factorization model the derivatives are:
行列分解モデルの場合、導関数は以下の通りです。

$$
\frac{\partial}{\partial \theta} \hat{x}_{uij} =
$$

Furthermore, we use three regularization constants: one $\lambda_W$ for the user features W; for the item features H we have two regularization constants, $\lambda_{H^+}$ that is used for positive updates on $h_{if}$, and $\lambda_{H^-}$ for negative updates on $h_{jf}$.
また、正則化定数は3つあり、ユーザ特徴Wには$¥lambda_W$、アイテム特徴Hには$¥lambda_{H^+}$と$¥lambda_{H^-}$の正則化定数を使用し、$h_{if}$の更新に使用される。

### Adaptive k-Nearest-Neighbor 適応型k-Nearest-Neighbor(KNN)

Nearest-neighbor methods are very popular in collaborative filtering.
協調フィルタリングでは、ニアレストネイバ法が非常によく使われている。
They rely on a similarity measure between either items (item-based) or users (user-based).
これらはアイテム（アイテムベース）またはユーザー（ユーザーベース）間の類似度測定に依存します。
In the following we describe item-based methods as they usually provide better results, but user-based methods work analogously.
以下では、通常より良い結果をもたらすアイテムベースの手法を説明するが、ユーザーベースの手法も同様に機能する。
The idea is that the prediction for a user u and an item i depends on the similarity of i to all other items the user has seen in the past – i.e. $I^+_u $.
このアイデアは、ユーザーuとアイテムiの予測は、そのユーザーが過去に見た他のすべてのアイテムとのiの類似性に依存するというものです - すなわち、$I^+\_u $。
Often only the k most similar items of $I^+_u$ are regarded – the k-nearest neighbors.
多くの場合、$I^+_u$の最も類似したk個のアイテム、つまりk-最近傍だけが考慮される。
If the similarities between items are chosen carefully, one can also compare to all items in $I_u^+$.
アイテム間の類似度を慎重に選べば、$I_u^+$の全アイテムと比較することも可能である。
For item prediction the model of item-based k-nearest-neighbor is:
アイテム予測の場合、アイテムベースの k-最近傍のモデルは次のようになる。

$$
\hat{x}_{ui} = \sum_{l \in I_u^+ \land l \neq i} c_{il}
$$

where $C:I×I$ is the symmetric item-correlation
ここで、$C:I×I$は対称的な項目相関である

The common approach for choosing C is by applying a heuristic similarity measure, e.g. cosine vector similarity:
Cを選択する一般的な方法は、コサインベクトル類似度などのヒューリスティックな類似度指標を適用することである。

$$
c_{ij}^{\text{cosine}} := \frac{|U_i^+ \cap U_j^+|}{\sqrt{|U_i^+| \cdot |U_j^+|}}
$$

A better strategy is to adapt the similarity measure C to the problem by learning it.
より良い戦略は、類似性尺度Cを学習することにより、問題に適応させることである。
This can be either done by using C directly as model parameters or if the number of items is too large, one can learn a factorization $HH^t$ of C with $H:I×k$.
これはCをモデルパラメータとして直接使用するか、項目数が多すぎる場合はCの$HH^t$を$H:I×k$で因数分解して学習することができる。
In the following and also in our evaluation we use the first approach of learning C directly without factorizing it.
以下では、また我々の評価では、Cを因数分解せずに直接学習する最初のアプローチを用いる。

Again for optimizing the kNN model for ranking, we apply the BPR optimization criterion and use the LearnBPR algorithm.
kNNモデルのランキング最適化のために、再びBPR最適化基準を適用し、LearnBPRアルゴリズムを使用する。
For applying the algorithm, the gradient of $\hat{x}_{uij}$ with respect to the model parameters C is:
このアルゴリズムを適用するために、モデルパラメータCに関する$Θhat{x}_{uij}$の勾配は。

$$
\frac{\partial}{\partial \theta} \hat{x}_{uij} =
$$

We have two regularization constants, $\lambda_+$ for updates on $c_{il}$, and $\lambda_-$ for updates on $c_{jl}$.
正則化定数は、$c_{il}$の更新に対して$¥lambda_+$、$c_{jl}$の更新に対して$¥lambda_-$の2種類を用意しました。

# Relations to other methods 他のメソッドとの関係

We discuss the relations of our proposed methods for ranking to two further item prediction models.
さらに2つの項目予測モデルに対する我々の提案するランキング手法の関係について議論する。

## Weighted Regularized Matrix Factorization (WR-MF) 重み付き正規化行列因子法(WR-MF)

Both Pan et al. [10] and Hu et al. [5] have presented a matrix factorization method for item prediction from implicit feedback. Thus the model class is the same as we described in Section 4.3.1, i.e. $\hat{X} := W H^T$ with the matrices $W :
U

$$
\sum_{u \in U} \sum_{i \in I} c_{ui}(<w_u, h_i> - 1)^2 + \lambda |W|^2_f + \lambda |H|^2_f
$$

where $c_{ui}$ are not model parameters but apriori given weights for each tuple $(u, i)$.
ここで、$c_{ui}$はモデルパラメータではなく、各タプル$(u, i)$に対して事前に与えられた重みである。
Hu et al. have additional data to estimate $c_{ui}$ for positive feedback and they set $c_{ui} = 1$ for the rest.
Huらは正のフィードバックに対して$c_{ui}$を推定するための追加データ(=元論文では ハイパーパラメータaとrating r*uiを使ってc_uiを算出してる.)を持っており、それ以外(negative feedback)は$c*{ui} = 1$とすることを提案している。
Pan et al. suggest to set $c_{ui} = 1$ for positive feedback and choose lower constants for the rest.
Panらはpositive feedbackに対して$c_{ui} = 1$とし、それ以外は低い定数を選択することを提案している.

First of all, it is obvious that this optimization is on instance level (one item) instead of pair level (two items) as BPR.
まず、この最適化はBPRのようなペアレベル（2項目）ではなく、インスタンスレベル（1項目）であることは明らか.
Apart from this, their optimization is a leastsquare which is known to correspond to the MLE for normally distributed random variables.
また、その最適化は最小二乗であり、正規分布の確率変数に対するMLEに相当することが知られている.
However, the task of item prediction is actually not a regression (quantitative), but a classification (qualitative) one, so the logistic optimization is more appropriate.
しかし、項目予測は回帰（定量的）ではなく、分類（定性的）であるため、ロジスティック最適化がより適切である。

A strong point of WR-MF is that it can be learned in $O(iter (
S

## Maximum Margin Matrix Factorization (MMMF) 最大マージン行列因子法 (MMMF)

Weimer et al. [15] use the maximum margin matrix factorization method (MMMF) for ordinal ranking.
Weimerら[15]は序数ランキングに最大マージン行列分解法（MMMF）を用いている。
Their MMMF is designed for scenarios with explicit feedback in terms of ratings.
彼らのMMMFは評価という明示的なフィードバックがあるシナリオのために設計されている。
Even though their ranking MMMF is not intended for implicit feedback datasets, one could apply it in our scenario by giving all non-observed items the ‘rating’ 0 and the observed ones a 1 (see Figure 1).
彼らのランキングMMMFは暗黙のフィードバックデータセットを意図していないにもかかわらず、すべての非観測項目に「評価」0を与え、観測項目に1を与えることで我々のシナリオに適用することができる(図1参照).
With these modifications their optimization criterion to be minimized would be quite similar to BPR applied for matrix factorization:
これらの修正により、最小化される最適化基準は、行列分解に適用されるBPRと非常に類似したものになるであろう.

$$
\sum_{(u,i,j) \in D_S} \max(0, 1- <w_u, h_i-h_j>) + \lambda_w |W|^2_f + \lambda_h |H|^2_f
$$

One difference is that the error functions differ – our hinge loss is smooth and motivated by the MLE.
1つの違いは、誤差関数が異なることで、我々のヒンジ損失は滑らかであり、MLEによって動機づけられている。
Additionally, our BPR-Opt criterion is generic and can be applied to several models, whereas their method is specific for MF.
さらに、**我々のBPR-Opt基準は汎用的であり、いくつかのモデルに適用できるのに対し、彼らの方法はMFに特化している**.

Besides this, their learning method for MMMF differs from our generic approach LearnBPR. Their learning method is designed to work with sparse explicit data, i.e. they assume that there are many missing values and thus they assume to have much less pairs than in an implicit setting. But when their learning method is applied to implicit feedback datasets, the data has to be densified like described above and the number of training pairs $D_S$ is in $O(
S

# Evaluation 評価

In our evaluation we compare learning with BPR to other learning approaches. We have chosen the two popular model classes of matrix factorization (MF) and k-nearest-neighbor (kNN). MF models are known to outperform [12] many other models including the Bayesian models URP [9] and PLSA [4] for the related task of collaborative rating prediction. In our evaluation, the matrix factorization models are learned by three different methods, i.e. SVD-MF, WR-MF [5, 10] and our BPR-MF. For kNN, we compare cosine vector similarity (Cosine-kNN) to a model that has been optimized using our BPR method (BPR-kNN). Additionally, we report results for the baseline mostpopular, that weights each item user-independent, e.g. : $\hat{x}^{most-pop}\_{ui} :=
U^+\_i

## Datasets データセット

We use two datasets of two different applications. The Rossmann dataset is from an online shop. It contains the buying history of 10, 000 users on 4000 items. In total 426, 612 purchases are recorded. The task is to predict a personalized list of the items the user wants to buy next. The second dataset is the DVD rental dataset of Netflix. This dataset contains the rating behavior of users, where a user provides explicit ratings 1 to 5 stars for some movies. As we want to solve an implicit feedback task, we removed the rating scores from the dataset. Now the task is to predict if a user is likely to rate a movie. Again we are interested in a personalized ranked list starting with the movie that is most likely to be rated. For Netflix we have created a subsample of 10, 000 users, 5000 items containing 565, 738 rating actions. We draw the subsample such that every user has at least 10 items (∀u ∈ U :
I + u

## Evaluation Methodology 評価方法

We use the leave one out evaluation scheme, where we remove for each user randomly one action (one useritem pair) from his history, i.e. we remove one entry from I + u per user u. This results in a disjoint train set Strain and test set Stest.
ここでは，各ユーザの履歴からランダムに1つのアクション（1つのユーザアイテムのペア）を削除する，すなわち，ユーザuごとにI + uから1つのエントリを削除する，leave one out評価スキームを用いる．
The models are then learned on Strain and their predicted personalized ranking is evaluated on the test set Stest by the average AUC statistic:
そして、モデルはStrain上で学習され、予測されたパーソナライズされたランキングはテストセットStest上で平均AUC統計量によって評価される。

$$
AUC = \tag{2}
$$

where the evaluation pairs per user u are:
ここで、ユーザuごとの評価ペアは

$$
E(u) :=
$$

A higher value of the AUC indicates a better quality.
AUCの値が高いほど、品質が良いことを示す。
The trivial AUC of a random guess method is 0.5 and the best achievable quality is 1.
ランダムな推測法の些細なAUCは0.5であり、達成可能な最高の品質は1である。

We repeated all experiments 10 times by drawing new train
新しい列車を抽出して、すべての実験を10回繰り返しました。

## Results and Discussion 結果と考察

Figure 6 shows the AUC quality of all models on the two datasets.
図 6 は、2 つのデータセットにおける全モデルの AUC 品質を示しています。
First of all, you can see that the two BPR optimized methods outperform all other methods in prediction quality.
まず、BPRで最適化された2つの手法は、予測品質において他のすべての手法を上回っていることがわかります。
Comparing the same models among each other one can see the importance of the optimization method.
同じモデル同士を比較すると、最適化手法の重要性がわかる。
For example all MF methods (SVD-MF, WR-MF and BPR-MF) share exactly the same model, but their prediction quality differs a lot.
例えば、すべてのMF手法（SVD-MF、WR-MF、BPR-MF）は全く同じモデルを共有していますが、その予測品質は大きく異なっています。
Even though SVD-MF is known to yield the best fit on the training data with respect to element-wise least square, it is a poor prediction method for machine learning tasks as it results in overfitting.
SVD-MFは、要素ごとの最小二乗法に関しては学習データに最もフィットすることが知られていますが、オーバーフィッティングになるため、機械学習タスクの予測手法としては不向きである.
This can be seen as the quality of SVD-MF decreases with an increasing number of dimensions.
これは、SVD-MFの品質が次元数の増加とともに低下することからもわかる。
WR-MF is a more successful learning method for the task of ranking.
WR-MFはランキングのタスクではより成功した学習方法である。
Due to regularization its performance does not drop but steadily rises with an increasing number of dimensions.
正則化により、WR-MFの性能は次元数の増加とともに低下することなく、着実に向上する。
But BPR-MF outperforms WR-MF clearly for the task of ranking on both datasets.
しかし、BPR-MFは両データセットにおいて、ランキングのタスクで明らかにWR-MFを上回る性能を示す。
For example on Netflix a MF model with 8 dimensions optimized by BPR-MF achieves comparable quality as a MF model with 128 dimensions optimized by WR-MF.
例えばNetflixでは、BPR-MFで最適化された8次元のMFモデルは、WR-MFで最適化された128次元のMFモデルと同等の品質を達成する。

To summarize, our results show the importance of optimizing model parameters to the right criterion.
要約すると、我々の結果はモデルパラメータを正しい基準で最適化することの重要性を示している.
The empirical results indicate that our BPR-Opt criterion learned by LearnBPR outperforms the other stateof-the-art methods for personalized ranking from implicit feedback.
実証結果は、LearnBPRによって学習された我々のBPR-Opt基準は、暗黙のフィードバックから個人化されたランキングのための他の最先端手法を凌駕していることを示している.
The results are justified by the analysis of the problem (section 3.2) and by the theoretical derivation of BPR-Opt from the MLE.
この結果は、問題の分析（3.2節）とMLEからのBPR-Optの理論的導出によって正当化される。

## Non-personalized ranking ノンパーソナライズドランキング

Finally, we compare the AUC quality of our personalized ranking methods to the best possible nonpersonalized ranking method.
最後に、パーソナライズド・ランキング手法のAUC品質を、可能な限り最良の非パーソナライズド・ランキング手法と比較する。
In contrast to our personalized ranking methods, a non-personalized ranking method creates the same ranking > for all users.
パーソナライズド・ランキング手法とは対照的に，**非パーソナライズド・ランキング手法はすべてのユーザに対して同じランキング$>$**を作成する．
We compute the theoretical upper-bound $np_{max}$ for any non-personalized ranking method by optimizing the ranking > on the test set $S_{test}$ 2 .
テストセット$S_{test}$ 2上でランキングを最適化し，非パーソナライズドランキング手法の理論上界$np_{max}$を計算した．
Figure 6 shows that even simple personalized methods like CosinekNN outperform the upper-bound $np_{max}$ — and thus also all non-personalized methods — largely.
図6より，CosinekNNのような単純なパーソナライズド手法でも，上界$np_{max}$，ひいてはすべての非パーソナライズド手法を大きく上回ることがわかる．

# Conclusion 結論

In this paper we have presented a generic optimization criterion and learning algorithm for personalized ranking.
本論文では、パーソナライズド・ランキングのための汎用的な最適化基準と学習アルゴリズムを提示した。
The optimization criterion BPR-Opt is the maximum posterior estimator that is derived from a Bayesian analysis of the problem.
最適化基準BPR-Optは、問題のベイズ分析から導かれる最大事後推定量である。
For learning models with respect to BPR-Opt we have presented the generic learning algorithm LearnBPR that is based on stochastic gradient descent with bootstrap sampling.
BPR-Optに関するモデルを学習するために、我々はブートストラップサンプリングを用いた確率的勾配降下に基づく汎用学習アルゴリズムLearnBPRを提示した。
We have demonstrated how this generic method can be applied to the two state-of-the-art recommender models of matrix factorization and adaptive kNN.
この汎用的な手法は、行列分解と適応的kNNの2つの最新推薦モデルに適用できることを実証した。
In our evaluation we show empirically that for the task of personalized ranking, models learned by BPR outperform the same models that are optimized with respect to other criteria.
我々の評価では、個人化されたランキングのタスクに対して、BPRによって学習されたモデルは、他の基準に関して最適化された同じモデルよりも優れていることを経験的に示している。
Our results show that the prediction quality does not only depend on the model but also largely on the optimization criterion.
この結果は、予測品質がモデルだけでなく、最適化基準にも大きく依存することを示している。
Both our theoretical and empirical results indicate that the BPR optimization method is the right choice for the important task of personalized ranking.
我々の理論的、実証的結果は、BPR最適化手法がパーソナライズドランキングという重要なタスクに適した選択であることを示している.
