## 0.1. link 0.1. リンク

- [pdf](https://arxiv.org/pdf/2107.06630.pdf) pdf](https:

- [この方のブログを見て本論文を見つけた.](https://ayakobaba.hatenablog.com/entry/2021/09/25/190642) [I found this paper through this person's blog. ](https:

## 0.2. title 0.2. タイトル

Online Evaluation Methods for the Causal Effect of Recommendations
レコメンデーションの因果関係に対するオンライン評価手法

## 0.3. abstract 0.3. 抽象的

Evaluating the causal effect of recommendations is an important objective because the causal effect on user interactions can directly leads to an increase in sales and user engagement.
レコメンデーションの因果関係を評価することは、ユーザーとのインタラクションの因果関係が売上やユーザーエンゲージメントの増加に直結するため、重要な目的である。
To select an optimal recommendation model, it is common to conduct A
最適なレコメンデーションモデルを選択するために、一般的にはA

# 1. Introduction 1. はじめに

A recommendation is a treatment that can affect user behavior.
レコメンデーションは、ユーザーの行動に影響を与えることができる治療法である。
An increase in user actions, such as purchases or views, by the recommendation is the treatment effect (also called the causal effect).
レコメンデーションによって、購入や閲覧などのユーザーアクションが増加することが、トリートメント効果（因果効果ともいう）である。
Because this leads to improved sales or user engagement, the causal effect of recommendations is important for businesses.
これは売上やユーザーエンゲージメントの向上につながるため、企業にとってレコメンデーションの因果関係は重要である。
While most recommendation methods aim for accurate predictions of user behaviors, there may be a discrepancy between the accuracy and the causal effect of recommendations [25].
多くの推薦手法は、ユーザーの行動を正確に予測することを目的としているが、推薦の精度と因果効果の間に乖離がある場合がある[25]。
Several recent works have thus proposed recommendation methods to rank items by the causal effect of recommendations [1, 24, 25, 27, 28].
そこで，近年では，推薦の因果関係によって項目をランク付けする推薦手法がいくつか提案されている[1, 24, 25, 27, 28]．

Online experiments are commonly conducted to compare model performance and select the best recommendation model.
モデルの性能を比較し、最適な推薦モデルを選択するために、オンライン実験が一般的に行われている。
However, evaluating the causal effect is not straightforward; we cannot naively compare the outcomes of recommended items because the causal effect is the difference between the potential outcomes with and without the treatment [12, 22].
しかし、因果関係の評価は一筋縄ではいかない。因果関係とは、処理を行った場合と行わなかった場合の潜在的な結果の差であるため、推薦項目の結果を単純に比較することはできない[12, 22]。
A
A

In this paper, we propose efficient online evaluation methods for the causal effect of recommendations based on interleaving.
本論文では、インターリービングに基づく推薦の因果関係の効率的なオンライン評価法を提案する。
Interleaving generates a list from the lists ranked by the two models to be compared [3].
インターリービングは、比較対象となる2つのモデルによってランク付けされたリストからリストを生成する[3]。
Whereas previous interleaving methods only measure the outcomes of items in the intersection of the original and interleaved lists, our proposed methods also measure the outcomes of items in the original lists but not in the interleaved list.
従来のインターリーブ法は、元のリストとインターリーブされたリストの交点にある項目の結果のみを測定するのに対し、我々の提案する方法は、元のリストにあるがインターリーブされたリストにない項目の結果も測定する。
We propose an interleaving method that selects items with equal probability for unbiased evaluation.
我々は、偏りのない評価を行うために、項目を等確率で選択するインターリーブ手法を提案する。
With unequal selection probabilities, the evaluation might be biased due to confounding [8] between recommendation and potential outcomes, leading to inaccurate judgments of the recommendation models.
選択確率が等しくない場合，推薦と潜在的な結果の交絡[8]により評価に偏りが生じ，推薦モデルの判定が不正確になる可能性がある．
We remove the possible bias by properly weighting the outcomes based on the inverse propensity score (IPS) method used in causal inference [16, 21].
我々は，因果推論で用いられる逆性向スコア（IPS）法 [16, 21]に基づいて，アウトカムを適切に重み付けすることで，この可能性のあるバイアスを除去している．
This enables the use of a more general interleaving framework that only requires non-zero probabilities to be selected for any item in the original lists.
これにより、より一般的なインターリーブフレームワークを使用することができ、元のリスト内の任意のアイテムについて選択される非ゼロの確率を必要とするのみである。
As an instance of the framework, we propose a causal balanced interleaving method that balances the number of items chosen from the two compared lists.
この枠組みの一例として、我々は、比較された2つのリストから選択される項目の数を均衡させる因果的均衡インターリーブ法を提案する。
To verify the unbiasedness and efficiency of the proposed interleaving methods, we simulate online experiments to compare ranking models.
提案するインターリーブ法の不偏性と効率性を検証するために、ランキングモデルを比較するオンライン実験のシミュレーションを行う。

The contributions of this paper are summarized as follows.
本論文の貢献は以下のようにまとめられる。

- We propose the first interleaving methods to compare recommendation models in terms of their causal effect. 我々は、レコメンデーションモデルを因果関係の観点から比較するためのインターリーブ手法を初めて提案する。

- We verify the unbiasedness and efficiency of the proposed methods through simulated online experiments 提案手法の不偏性と効率性を模擬オンライン実験により検証する

# 2. Related Work 2. 関連作品

## 2.1. Interleaving Methods 2.1. インターリーブ方法

Interleaving is an online evaluation method for comparing two ranking models by observing user interactions with an interleaved list that is generated from lists ranked by the two models to be compared [3].
インターリーブとは，比較する2つのモデルによってランク付けされたリストから生成されるインターリーブリストに対するユーザのインタラクションを観察することによって，2つのランキングモデルを比較するオンライン評価手法である[3]．
Several interleaving methods have been proposed for evaluating information retrieval systems.
情報検索システムの評価手法として，いくつかのインターリーブ手法が提案されている．
Balanced interleaving [14, 15] generates an interleaved list from two rankings to be compared such that the highest ranks in the interleaved list 𝑘𝐴 and 𝑘𝐵 from the two rankings 𝐴 and 𝐵, respectively, are the same or different by at most one.
Balanced interleaving [14, 15] は、比較する二つのランキングから、二つのランキングᵅと𝑘からそれぞれインターリーブされたリストの最高ランク𝑘𝐵が同じか最大1だけ異なるようにインターリーブリストを生成するものである。
Team draft interleaving [19] alternatively selects items from compared rankings, analogously to selecting teams for a friendly team-sports match.
チームドラフトインターリーブ[19]は、チームスポーツの親善試合のチームを選ぶように、比較したランキングから項目を選択する方法である。
Probabilistic interleaving [9] selects items according to probabilities that depend on the item ranks.
確率的インターリーブ(Probabilistic interleaving) [9] は項目のランクに依存する確率に従って項目を選択する。
Optimized interleaving [18] makes the properties required for interleaving in information retrieval explicit and then generates interleaved lists by solving an optimization problem to fulfill those properties.
最適化インターリーブ[18]は，情報検索におけるインターリーブに必要な特性を明示し，その特性を満たすように最適化問題を解いてインターリーブリストを生成する．
Interleaving methods have been extended to multileaving that compare multiple rankings simultaneously [30, 31].
インターリービングの手法は，複数の順位を同時に比較するマルチリービングに拡張されている[30, 31]．
Multileaving has been also applied to the evaluation of a news recommender system [11].
また，マルチリービングはニュース推薦システムの評価にも適用されている[11]．
The objective of previous interleaving methods is to evaluate how accurately the rankings reflect queries or user preferences, whereas our goal is to evaluate rankings in terms of the causal effect.
従来のインターリーブ法の目的は，ランキングがいかに正確にクエリやユーザの嗜好を反映しているかを評価することであるが，我々の目的は，因果関係の観点からランキングを評価することである．
To the best of our knowledge, at present there are no interleaving methods for causal effects.
我々の知る限り，現在のところ因果関係を考慮したインタリービング手法は存在しない．

## 2.2. Recommendation Methods for the Causal Effect 2.2. 因果関係の推奨方法

Recommendations can affect users’ opinions [5] and induce users’ actions [6, 13].
このように，レコメンデーションはユーザの意見に影響を与え [5]，ユーザの行動を誘発することができる [6, 13]．
However, users’ actions on recommended items could have occurred even without the recommendations [32].
しかし、推薦されたものに対するユーザの行動は、推薦されなく ても発生する可能性がある[32]。
Building recommendation models that target the causal effect is challenging because the ground truth data of causal effects are not observable [10].
このような因果関係を考慮したレコメンデーションモデルを構築することは、因果関係のグランドトゥルースデータが観測できないため、困難である[10]。
One approach is to train prediction models for both recommended and non-recommended outcomes and then to rank the items based on the difference between the two predictions [1, 24].
そのため，推薦された結果と推薦されな かった結果の両方について予測モデルを学習し，2つの予測値の差に基 づいて項目をランク付けする方法がある[1, 24]．
Another approach is to optimize models directly for the causal effect.
もう一つのアプローチは、因果関係に対して直接モデルを最適化することである。
ULRMF and ULBPR [25] are respectively pointwise and pairwise optimization methods that use label transformations and training data samplings designed for causal effect optimization.
ULRMFとULBPR[25]は、それぞれポイントワイズとペアワイズの最適化手法で、ラベル変換と学習データのサンプリングを使用し、因果効果の最適化のために設計されています。
DLCE [27] is an unbiased learning method for the causal effect that uses an IPS-based unbiased learning objective.
DLCE [27]は、IPSに基づく不偏の学習目的を用いた因果効果のための不偏の学習方法である。
There are also neighborhood methods for causal effects [28] that are based on a matching estimator in causal inference.
また、因果推論におけるマッチング推定量に基づく因果効果の近傍法[28]も存在する。
These prior works on causal effects evaluated methods offline and did not discuss protocols for online evaluation.
これらの因果効果に関する先行研究では、手法をオフラインで評価し、オンライン評価のためのプロトコルについては議論されていない。
In this study, we develop online evaluation methods and compare some of the aforementioned recommendation methods in simulated online experiments.
本研究では、オンライン評価手法を開発し、模擬オンライン実験において前述の推薦手法のいくつかを比較する。

Another line of works in the area of causal recommendation aims for debiasing [4].
また，因果関係推薦の分野では，デビアス（debiasing） を目的とした研究も行われている [4]．
Several methods have been proposed to learn users’ true preferences from biased (missing-not-at-random) feedback data [2, 23, 29, 33].1 These methods can be regarded as predicting interactions with recommendations (i.e., $Y_{ui}^T$, defined in the next section).
偏った（missing-not-at-random）フィードバックデータからユーザの真の嗜好を学習する方法がいくつか提案されている[2, 23, 29, 33] 1。これらの方法は、推薦との相互作用（すなわち、次節で定義する $Y_{ui}^T$ ）を予測するものと考えることができる。
Hence, we can evaluate them using previous interleaving methods.
したがって，以前のインターリーブ法を用いてそれらを評価することができる．

# 3. Evaluation Methods for the Causal Effect of Recommendatios 3. レコメンデーションの因果関係の評価方法

## 3.1. Causal Effect of Recommendations 3.1. 推奨事項の因果関係

In this subsection, we define the causal effect of recommendations.
このサブセクションでは、レコメンデーションの因果関係を定義する。
Let $U$ and $I$ be sets of users and items, respectively.
U$と$I$をそれぞれユーザーとアイテムの集合とする。
Let $Y_{ui}
また、$Y_{ui}とする。
\in {0, 1}$ denote the interaction (e.g., purchase or view) of user $u \in U$ with item $i \in I$.
\U$と$I$をそれぞれユーザーとアイテムの集合とし、ユーザー$uとアイテム$iの相互作用（購入や閲覧など）を$Y_{ui}{in {0, 1}$とする。
User interactions may differ depending on whether the item is recommended or not.
ユーザとのインタラクションは、そのアイテムが推奨されるか否かによって異なる場合がある。
We denote the binary indicator for the recommendation (also called the treatment assignment) by $Z_{ui}
ここで、推奨の2値指標を$Z_{ui}とする（処理割り当てともいう）。
\in {0, 1}$.
\in {0, 1}$ とする。
Let $Y_{ui}^T$ and $Y_{ui}^C \in {0, 1}$ be hypothetical user interactions (also called potential outcomes [22]) when item $i$ is recommended to $u$ ($Z_{ui} = 1$) and when it is not recommended ($Z_{ui} = 0$), respectively.
また、$Y_{ui}^T$と$Y_{ui}^C \in {0, 1}$ をそれぞれ$u$にアイテム$i$を推奨した場合（$Z_{ui} = 1$）と推奨しない場合（$Z_{ui} = 0$）の仮想のユーザー相互作用（潜在結果ともいう[22]）であるとする。
The causal effect $\tau_{ui}$ of recommending item $i$ to user $u$ is defined as the difference between the two potential outcomes: $\tau_{ui} = Y_{ui}^T − Y_{ui}^C$, that takes ternary values, $\tau_{ui}
アイテム$i$をユーザ$u$に推奨する因果効果$tau_{ui}$は、2つの潜在的な結果の差として定義される：$tau_{ui} = Y_{ui}^T - Y_{ui}^C$, 3値をとり、$tau_{ui}は、$tau_{ui} = Y_{ui}^C$, 3値をとる
\in {−1, 0, 1}$.
\の3値をとる。
Using potential outcomes, the observed interaction can be expressed as
ポテンシャルアウトカムを用いると、観測された相互作用は次のように表現できる。

$$
Y_{ui} = Z_{ui} Y_{ui}^T +(1 -Z_{ui})Y_{ui}^C
\tag{1}
$$

$Y_{ui} = Y_{ui}^T if $i$ is recommended ($Z_{ui}= 1$) and $Y_{ui} = Y_{ui}^C$ if it is not recommended ($Z_{ui} = 0$).
i$を推奨する場合($Z_{ui}= 1$)は$Y_{ui}=Y_{ui}^T、推奨しない場合($Z_{ui}= 0$)は$Y_{ui}=Y_{ui}^C$とする。
Note that $Y_{ui}^T$ or $Y_{ui}^C$ cannot both be observed at a specific time; hence, $\tau_{ui}$ is not directly observable.
ただし、$Y_{ui}^T$または$Y_{ui}^C$の両方を特定の時間に観測することはできないので、$tau_{ui}$は直接観測できないことに注意。

The recommendation model $A$ generates a recommendation list $L_u^A$ for each user.
推薦モデル$A$は、各ユーザーの推薦リスト$L_u^A$を生成する。
The average causal effect of model $A$ is then defined as
そして、モデル$A$の平均的な因果効果は、以下のように定義される。

$$
\hat{\tau}_A = \frac{1}{n|S_A|} \sum_{u \in S_A} \sum_{i \in L_{u}^A} \tau_{ui}
\tag{2}
$$

In this work, we evaluate models using the above metric.2 That is, when comparing two models, we regard $A$ to superior to $B$ when $\tau_A > \tau_B$.
つまり、2つのモデルを比較するとき、$A$は$B$より$tau_A > \tau_B$ のとき優れているとみなす。

## 3.2. A/B testing for the Causal Effect 3.2. A

For A
For A

$$
\tag{3}
$$

This converges to $\tau_A$ as $
S_A

The typical evaluation metrics for A
の代表的な評価指標は、A

$$
\tag{4}
$$

Because the rightmost term in the final equation does not depend on the model, we can compare $\hat_{\tau_A}$ and $\hat_{\tau_B}$ by comparing $\hat{Y}_A^{total}$ and $\hat{Y}_B^{total}$.
最終式の右端の項はモデルに依存しないので、$hat_{tau_A}$と$hat_{tau_B}$の比較は、$hat{Y}_A^{total}$と$hat{Y}_B^{total}$の比較で可能です。
On the other hand, the average interactions with the recommended lists can be expressed as
一方，推奨リストとの平均的なインタラクションは，以下の式で表すことができる．

$$
\tag{5}
$$

Hence, the evaluation based only on interactions with recommended lists is not valid testing for the causal effect.
したがって、推奨リストとの相互作用に基づく評価だけでは、因果関係の検証としては有効ではない。

Although A
が、A

## 3.3. Interleaving for the Causal Effect 3.3. 因果関係のインターリーブ

In this subsection, we propose interleaving methods for the online evaluation of the causal effects of recommendations.
本節では，推薦の因果関係をオンラインで評価するためのインターリーブ手法を提案する．
Previous interleaving methods only measure outcomes in the interleaved lists: they only include $Y_{ui}^T$ and lack information on $Y_{ui}^C$.
これまでのインターリーブ法は、インターリーブされたリストの結果のみを測定する：それらは$Y_{ui}^T$のみを含み、$Y_{ui}^C$に関する情報を欠いている。
Further, if the item selection for the interleaved list is not randomized controlled, the naive estimate from the observed outcomes might be biased due to the confounding between recommendations and potential outcomes.
さらに，インターリーブされたリストの項目選択がランダム化制御されていない場合，レコメンデーションと潜在的なアウトカムとの交絡により，観測されたアウトカムからのナイーブな推定値にバイアスがかかる可能性がある．
We need to remedy the bias for valid comparison.
有効な比較のためには、この偏りを是正する必要がある。

Here we describe the problem setting of interleaving for the causal effect.
ここでは、因果関係のある効果に対するインターリーブに関する問題設定を説明する。
For each user $u$, we construct the interleaved list $L_u$ from the compared lists $L_u^A$ and $L_u^B$.
各ユーザー$u$について、比較されたリスト$L_u^A$と$L_u^B$からインターリーブされたリスト$L_u$を構築する。
We observe outcomes ${Y_{ui}}$ for all items $i \in I$.
I$の全ての項目$i \in I$について、結果${Y_{ui}}$を観測する。
Note that $Y_{ui} = Y_{ui}^T$ if item $i$ is in the interleaved list ($i \in L_{u}$ or equivalently, $Z_{ui} = 1$) and $Y_{ui} = Y_{ui}^C$ if it is not in the list ($i \in I \setminus L_u$ or equivalently, $Z_{ui}= 0$).
ただし、項目$i$がインターリーブリストにある場合（$i \in L_{u}$ or equivalently, $Z_{ui} = 1$）には$Y_{ui}=Y_{ui}^T$、リストにない場合（$i \in Isetminus L_u$ or equivalently, $Z_{ui}= 0$)には$Y_{ui}^C$であることに注意してください。
We want to compare the average causal effects of lists $L_u^A$ and $L_u^B$:
リスト$L_u^A$と$L_u^B$の平均的な因果効果を比較したい。

$$
\tag{6}
$$

We need to estimate the above values from observed outcomes because we cannot directly observe $\tau_{ui}$.
直接$tau_{ui}$を観測できないので、観測された結果から上記の値を推定する必要があります。

If the items in $L_u^A$ and $L_u^B$ are randomly assigned to the interleaved list independent of the potential outcomes, that is, $(Y_{ui}^T, Y_{ui}^C) \perp Z_{ui}$, the case can be regarded as a randomized controlled trial (RCT) [12, 22].
L_u^A$と$L_u^B$の項目が潜在的な結果とは無関係にインターリーブリストにランダムに割り当てられた場合、つまり$(Y_{ui}^T, Y_{ui}^C) \perp Z_{ui}$ なら、この事例は無作為対照試験（RCT）と見なすことができる [12, 22]．
3 We can then simply estimate $\tau_{L_u^A}$ as the difference in average outcomes for items on and not on the interleaved list:
そして、$tau_{L_u^A}$をインターリーブ・リストにあるものとないものとの平均結果の差として単純に推定することができる。

$$
\tag{7}
$$

One way to realize such a randomized assignment is to select 𝑛 items from $L_u^A \cup L_u^B$ with equal probability: $p = n \setminus
L_u^A \cup L_u^B

The independence requirement heavily restricts the potential design space of interleaving methods. We thus derive estimates that are applicable to more general cases. Denote the probability (also called the propensity) of being included in the interleaved list $L_u$ by $p_{ui} = E[Z_{ui} = 1
X_{ui}]$. We assume that 1) the covariates $X_{ui}$ contain all confounders of $(Y_{ui}^T, Y_{ui}^C)$ and $Z_{ui}$, and 2) the treatment assignment is not deterministic ($0 < p_{ui} < 1$ for $i \in L_u^A \cup L_u^B$).4 Assumption 1 is equivalent to conditional independence: $(Y_{ui}^T,Y_{ui}^C) \perp Z_{ui}

Under these assumptions, we can construct an unbiased estimator using IPS weighting [16]:
このような仮定のもと、IPS重み付けを用いて不偏推定量を構築することができる[16]。

$$
\tag{8}
$$

This estimator is unbiased since
この推定量は不偏である。

$$
\tag{9}
$$

We propose a general framework for interleaving as follows.
我々は、以下のようにインターリーブの一般的なフレームワークを提案する。

- (1) Construct interleaved lists ${L_u}$ using an interleaving method that satisfies positivity (Assumption 2). (1) 積極性（仮定2）を満たすインターリーブ方式でインターリーブリスト${L_u}$を構成する。

- (2) Conduct online experiments and obtain outcomes ${Y_{ui}}$. (2) オンライン実験を行い、結果 ${Y_{ui}}$ を得る。

- (3) Estimate $\tau_{L_u^A}$ and $\tau_{L_u^B}$ by Eq. (8) and compare them. (3) $tau_{L_u^A}$ と $tau_{L_u^B}$ を式（8）で推算し、比較せよ。

As an example of a valid interleaving method that satisfies positivity, we propose causal balanced interleaving (CBI), the pseudo-code for which is shown in Algorithm $1$. CBI alternatively selects items from each list to balance the items chosen from each list. The item choice in each round is not deterministic in order to satisfy the positivity required for causal effect estimates. The propensity depends on whether an item is in the intersection, $1(i \in L_u^A \cap L_u^B)$. If an item is included in both lists, it has a greater probability of being chosen. The propensity also depends on the cardinality of the union of the compared lists, $
L_u^A \cup L_u^B

# 4. Experiments 4. 実験

## 4.1. Experimental Setup 4.1. 実験セットアップ

We experimented with the following online evaluation methods.6
以下のようなオンライン評価方法を実験した6。

- AB-total: A/B testing evaluated by the total user interactions, as expressed in Eq. (4). AB-合計：A

- AB-list: A/B testing evaluated by user interactions only with items on the recommended list, as in Eq. (5). AB-リスト A

- EPI-RCT: Interleaving to select items from $L_u^A \cup L_u^B$ with equal probability and evaluation using Eq. (7). EPI-RCT：$L_u^A \cup L_u^B$から等確率で項目を選択するインターリーブと式(7)による評価。

- CBI-RCT: Interleaving by Algorithm 1 and evaluation using Eq. (7), that is, no bias correction by IPS. CBI-RCT: Algorithm 1 でインターリーブし、式(7)で評価、つまり IPS によるバイアス補正なし。

- CBI-IPS: Interleaving by Algorithm 1 and evaluation using Eq. (8). CBI-IPS。 アルゴリズム1によるインターリーブと式(8)による評価。

Through the experiments, we aim to answer the following research questions:
実験を通して、我々は以下の研究課題に答えることを目的とする。
RQ1) Which method produces valid (unbiased) estimates of the true differences in average causal effects (4.2.1)?, and RQ2) Are the proposed interleaving methods more efficient (do they require fewer experimental users) than AB testing (4.2.2)?
RQ1）どの方法が平均的な因果効果の真の差の有効な（不偏の）推定値を生み出すか（4.2.1），RQ2）提案するインターリーブ法はABテストよりも効率が良いか（実験ユーザの数が少なくても良いか）（4.2.2），RQ3）どの方法が平均的な因果効果の真の差の有効な（不偏の）推定値を生み出すか，RQ4）。
We first prepared semisynthetic datasets that contain both potential outcomes $Y_{ui}^T$ and $Y_{ui}^C$ for all user-item pairs.
まず、全てのユーザー項目ペアについて、潜在的な結果$Y_{ui}^T$と$Y_{ui}^C$の両方を含む半合成データセットを用意しました。
Because we observe $Y_{ui} = Y_{ui}^T$ if $Z_{ui} = 1$ and $Y_{ui}= Y_{ui}^C$ if $Z_{ui}=0$, both potential outcomes are necessary to simulate user outcomes under various ranking models and online evaluation methods.
Z_{ui}=1$なら$Y_{ui}^T$、$Z_{ui}=0$なら$Y_{ui}=Y_{ui}^C$と観測されるので、様々なランキングモデルやオンライン評価法でのユーザ成果をシミュレーションするためには、両方の潜在的な成果が必要である。
Following the procedure described in [28], we generated two datasets: one is based on the Dunnhumby dataset,7 and the other is based on the MovieLens-1M (ML-1M) dataset [7].8 The detail and rationale of ML one are described in Section 5.1 of [28] and that of DH one are described in 5.1.1 of [27].
1つはDunnhumbyデータセット7，もう1つはMovieLens-1M (ML-1M) データセット[7]に基づくものである8．
Each dataset is comprised of independently generated training and testing data.
各データセットは独立に生成されたトレーニングデータとテストデータから構成される．
The testing data were used to simulate online evaluation, and the training data were used to train the following models:9 the causality-aware user-based neighborhood methods (CUBN) with outcome similarity (-O) and treatment similarity (-T) [28], the uplift-based pointwise and pairwise learning methods (ULRMF and ULBPR) [25], the Bayesian personalized ranking method (BPR) [20], and the user-based neighborhood method (UBN) [17].
テストデータはオンライン評価のシミュレーションに使用し，学習データは以下のモデルの学習に使用した：9 結果類似度（-O）と治療類似度（-T）による因果関係を考慮したユーザベース近傍法（CUBN） [28]，隆起に基づくポイントワイズ及びペアワイズ学習法（ULRMF と ULBPR）[25]， ベイズパーソナライズドランキング法（BPR） [20] 及びユーザベース近傍法 (UBN) [17]．
We compared two models among CUBN-T, ULRMF, BPR on the Dunnhumby data and two models among CUBN-O, ULBPR, UBN on the ML-1M data.10 The average causal effect $\bar{\tau_{L_u^{model}}}$ and the average treated outcomes $\bar{Y_{L_u^{model}}^T}$ of the trained models are listed in Table 1.
学習したモデルの平均因果効果 $bar{tau_{L_u^{model}}$ と平均処理結果 $bar{Y_{L_u^{model}}^T}$ を表1に示す．
The superior models in terms of the average causal effect do not necessarily have higher average treated outcomes.
平均因果効果の点で優れたモデルは、必ずしも平均治療成績が高いとは限らない。
That is, we may mistakenly select a poor model in terms of the causal effect if we only evaluate the outcomes of the recommended items.
つまり、推奨項目の結果のみを評価すると、因果効果の点で劣るモデルを誤って選択してしまう可能性がある。

Table 1.
表1.
Averages of causal effect and potential outcomes under treatment with recommendation lists of size 𝑛 = 10.
サイズ𝑛 = 10の推薦リストを用いた治療下での因果効果と潜在的成果の平均値。

Our protocol for simulating online experiments is the following.
オンライン実験のシミュレーションのプロトコルは以下の通りである。
First, we randomly select a subset of users and generate lists $L_u^A, L_u^B$ using compared models.
まず、ユーザの部分集合をランダムに選択し、比較したモデルを用いてリスト$L_u^A, L_u^B$を生成する。
For the A
に対して、A

## 4.2. Results and Discussion 4.2. 結果および考察

### 4.2.1. Validity of the evaluation methods 4.2.1. 評価手法の妥当性

We evaluated the validity of the online evaluation methods using random subsets of 1,000 users.
1,000 人のユーザーからなるランダムサブセットを用いて，オンライン評価手法の妥当性を評価した．
The means and standard deviations of the estimated differences are shown in Table 2.
推定された差の平均値と標準偏差を表2に示す。
The means obtained by EPI-RCT and CBI-IPS are close to the true differences.
EPI-RCTとCBI-IPSの平均値は真の差に近い値であった。
The means obtained by AB-total are also close to the true value for Dunnhumby but deviate slightly for ML-1M.
AB-totalで得られた平均値もDunnhumbyでは真の値に近いが、ML-1Mでは若干乖離している。
The AB-list often yields estimates that differ substantially from the true values but are similar to the differences in treated outcomes, $\bar{Y^T_{L_u^{model}}}$, as shown in Table 1.
AB-listでは、表1に示すように、真の値とは大きく異なるが、治療成績の差$¥bar{Y^T_{L_u^{model}}$に近い推定値を得ることが多い。
This is expected because the AB-list evaluates $Y_{ui}^T$, not $\tau_{ui}$, as expressed in Eq. (5).
これは、式（5）で表されるように、AB-listは$Y_{ui}^T$を評価するのであって、$tau_{ui}$を評価するのではないため、予想されることである。
Further, the CBI-RCT estimates also deviate from the true differences in most cases.11 This is due to the bias induced by the uneven probability of recommendation in interleaving.
さらに、CBI-RCTの推定値もほとんどの場合、真の差から乖離している11。これは、インターリーブにおける推奨確率の不均一性によって引き起こされるバイアスのためである。
Conversely, CBI-IPS successfully removes the bias and produces estimates centered around the true values.
逆に、CBI-IPSはこのバイアスをうまく除去し、真の値を中心とした推定値を得ることができる。

Table 2.
表2.
Estimated differences between the causal effects of the compared models (mean ± standard deviations for 10,000 simulated runs).
比較したモデルの因果効果の差の推定値（10,000回のシミュレーション実行の平均値±標準偏差）。
The results highlighted in bold indicate that the true values are within the 95% confidence intervals of the mean estimates
太字で表示された結果は、真の値が平均推定値の95%信頼区間内にあることを示す

### 4.2.2. Efficiency of the interleaving methods. 4.2.2. インターリーブ手法の効率性

We compared the efficiency of AB-total, EPI-RCT, and CBI-IPS, all of which were shown to be valid in the previous section.
前節で有効性が示されたAB-total, EPI-RCT, CBI-IPSの効率性を比較した．
We simulated user subsets of various sizes in {10, 14, 20, 30, 50, 70, 100, 140, 200, 300, 500, 700, 1000, 1400, 2000} and evaluated the ratio of false judgments (when the sign of the estimated difference is the opposite of the truth).
10, 14, 20, 30, 50, 70, 100, 140, 200, 300, 500, 700, 1000, 1400, 2000}の様々なサイズのユーザサブセットを模擬し，誤判定の割合（推定差分の符号が真と反対の場合）を評価した．
Figure 1 shows the ratio of false judgments according to the number of users.
図1は、ユーザ数に応じた誤判定率の推移を示したものである。
As the number of users increases, the false ratios of CBI-IPS and EPI-RCT decrease more rapidly than that of AB-total does.
CBI-IPSとEPI-RCTの誤判定比率は，利用者数の増加とともに，AB-totalの誤判定比率よりも急速に減少することがわかる．
For the Dunnhumby dataset, AB-total requires around 30 times more users than CBI-IPS and EPI-RCT to achieve the same false ratio.
Dunnhumbyデータセットでは，AB-totalはCBI-IPSとEPI-RCTと同じ誤判定率を達成するために約30倍のユーザ数を必要とする．
For the ML-1M dataset, AB-total did not reach the same false ratio in the experimental range of subset sizes.
ML-1Mデータセットでは，AB-totalは実験範囲の部分集合サイズにおいて，同じ誤答率に達しなかった．
These results demonstrate the superior efficiency of the proposed interleaving methods.
これらの結果は、提案するインターリーブ手法の優れた効率性を示している。
Furthermore, CBI-IPS tends to be slightly more efficient than EPI-RCT, as expected from the smaller standard deviations shown in Table 2.
さらに、表2に示す標準偏差の小ささから予想されるように、CBI-IPSはEPI-RCTよりもわずかに効率が良い傾向がある。
This is probably because the number of items selected from the compared lists is balanced in this interleaving method.
これは、このインターリーブ手法では、比較したリストから選択される項目の数がバランスされているためと考えられる。

Fig. 1.
図1.
Dependence on the number of users.
ユーザー数への依存性

# Conclusions 結論

In this paper, we proposed the first interleaving methods for comparing recommender models in terms of causal effects.
本論文では，レコメンダーモデルを因果関係の観点から比較するためのインターリーブ手法を初めて提案した．
To realize unbiased model comparisons, our methods either select items with equal probabilities or weight the outcomes using IPS.
本手法では、モデルの比較を偏りなく行うために、項目を等確率で選択するか、IPSを用いて結果に重み付けを行う。
We simulated online experiments and verified that our interleaving methods and an A
我々はオンライン実験のシミュレーションを行い、我々のインターリーブ手法とA