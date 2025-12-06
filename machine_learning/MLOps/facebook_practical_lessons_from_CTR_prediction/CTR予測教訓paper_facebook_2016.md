
refs: /Users/masato.morita/Downloads/paper.pdf


# Practical Lessons from Predicting Clicks on Ads at Facebook  
# Facebookにおける広告クリック予測からの実践的教訓

## Xinran He, Junfeng Pan, Ou Jin, Tianbing Xu, Bo Liu[∗], Tao Xu[∗], Yanxin Shi[∗], Antoine Atallah[∗], Ralf Herbrich[∗], Stuart Bowers, Joaquin Quiñonero Candela  
## Xinran He, Junfeng Pan, Ou Jin, Tianbing Xu, Bo Liu[∗], Tao Xu[∗], Yanxin Shi[∗], Antoine Atallah[∗], Ralf Herbrich[∗], Stuart Bowers, Joaquin Quiñonero Candela  

### Facebook 1601 Willow Road, Menlo Park, CA, United States  
### Facebook 1601 Willow Road, Menlo Park, CA, United States


```md
## {panjunfeng, oujin, joaquinq, sbowers}@fb.com
```  



## ABSTRACT 要約

Online advertising allows advertisers to only bid and pay for measurable user responses, such as clicks on ads. 
オンライン広告は、広告主が広告のクリックなどの測定可能なユーザーの反応に対してのみ入札し、支払うことを可能にします。
As a consequence, click prediction systems are central to most online advertising systems. 
その結果、クリック予測システムはほとんどのオンライン広告システムの中心的な役割を果たします。
With over 750 million daily active users and over 1 million active advertisers, predicting clicks on Facebook ads is a challenging machine learning task. 
日々7億5000万以上のアクティブユーザーと100万人以上のアクティブ広告主を抱えるFacebook広告のクリックを予測することは、挑戦的な機械学習のタスクです。
In this paper we introduce a model which combines decision trees with logistic regression, outperforming either of these methods on its own by over 3%, an improvement with significant impact to the overall system performance. 
本論文では、決定木とロジスティック回帰を組み合わせたモデルを紹介し、これらの手法のいずれか単独よりも3%以上の性能向上を実現し、全体のシステム性能に重要な影響を与える改善を示します。
We then explore how a number of fundamental parameters impact the final prediction performance of our system. 
次に、いくつかの基本的なパラメータが私たちのシステムの最終的な予測性能にどのように影響するかを探ります。
Not surprisingly, the most important thing is to have the right features: those capturing historical information about the user or ad dominate other types of features. 
驚くことではありませんが、最も重要なのは適切な特徴を持つことです：ユーザーや広告に関する歴史的情報を捉える特徴が他のタイプの特徴を支配します。
Once we have the right features and the right model (decisions trees plus logistic regression), other factors play small roles (though even small improvements are important at scale). 
**適切な特徴と適切なモデル（決定木とロジスティック回帰）を持つ**と、他の要因は小さな役割を果たします（ただし、小さな改善でもスケールでは重要です）。
Picking the optimal handling for data freshness, learning rate schema and data sampling improve the model slightly, though much less than adding a high-value feature, or picking the right model to begin with. 
データの新鮮さ、学習率スキーマ、データサンプリングの最適な取り扱いを選択することでモデルはわずかに改善されますが、高価値の特徴を追加することや、最初に適切なモデルを選ぶことに比べると、その改善ははるかに少ないです。

<!-- ここまで読んだ -->

## 1. INTRODUCTION はじめに

Digital advertising is a multi-billion dollar industry and is growing dramatically each year. 
デジタル広告は数十億ドル規模の産業であり、毎年劇的に成長しています。
In most online advertising platforms the allocation of ads is dynamic, tailored to user interests based on their observed feedback. 
ほとんどのオンライン広告プラットフォームでは、広告の配分は動的であり、ユーザの観察されたフィードバックに基づいてユーザの興味に合わせて調整されています。
Machine learning plays a central role in computing the expected utility of a candidate ad to a user, and in this way increases the efficiency of the marketplace. 
機械学習は、候補広告がユーザにとって期待される効用を計算する上で中心的な役割を果たし、この方法で市場の効率を高めます。
The 2007 seminal papers by Varian [11] and by Edelman et al. [4] describe the bid and pay per click auctions pioneered by Google and Yahoo! 
2007年のVarian [11]およびEdelmanら [4]による画期的な論文は、GoogleとYahoo!によって先駆けられた入札およびクリックごとの支払いオークションを説明しています。
That same year Microsoft was also building a sponsored search marketplace based on the same auction model [9]. 
同じ年にMicrosoftも同じオークションモデルに基づいたスポンサー検索マーケットプレイスを構築していました [9]。
The efficiency of an ads auction depends on the accuracy and calibration of click prediction. 
**広告オークションの効率は、クリック予測の精度とキャリブレーションに依存**します。
The click prediction system needs to be robust and adaptive, and capable of learning from massive volumes of data. 
クリック予測システムは堅牢で適応性があり、大量のデータから学習できる必要があります。
The goal of this paper is to share insights derived from experiments performed with these requirements in mind and executed against real world data. 
この論文の目的は、これらの要件を考慮して実施された実験から得られた洞察を共有し、実世界のデータに対して実行されたものです。

In sponsored search advertising, the user query is used to retrieve candidate ads, which explicitly or implicitly are matched to the query. 
スポンサー検索広告では、ユーザのクエリを使用して候補広告を取得し、これらは明示的または暗黙的にクエリにマッチします。
At Facebook, ads are not associated with a query, but instead specify demographic and interest targeting. 
Facebookでは、広告はクエリに関連付けられておらず、代わりに人口統計および興味のターゲティングを指定します。
As a consequence of this, the volume of ads that are eligible to be displayed when a user visits Facebook can be larger than for sponsored search. 
その結果、ユーザがFacebookを訪れたときに表示される資格のある広告の量は、スポンサー検索よりも多くなる可能性があります。

In order tackle a very large number of candidate ads per request, where a request for ads is triggered whenever a user visits Facebook, we would first build a cascade of classifiers of increasing computational cost. 
**ユーザがFacebookを訪れるたびに広告のリクエストがトリガーされる場合、非常に多くの候補広告に対処するために、まず計算コストが増加する分類器のカスケードを構築します。**
In this paper we focus on the last stage click prediction model of a cascade classifier, that is the model that produces predictions for the final set of candidate ads. 
この論文では、カスケード分類器の最終段階のクリック予測モデル、つまり最終的な候補広告のセットに対する予測を生成するモデルに焦点を当てます。

We find that a hybrid model which combines decision trees with logistic regression outperforms either of these methods on their own by over 3%. 
決定木とロジスティック回帰を組み合わせたハイブリッドモデルが、これらのいずれかの手法単独よりも3%以上優れていることがわかりました。
This improvement has significant impact to the overall system performance. 
この改善は、全体のシステム性能に大きな影響を与えます。
A number of fundamental parameters impact the final prediction performance of our system. 
いくつかの基本的なパラメータが、私たちのシステムの最終的な予測性能に影響を与えます。
As expected the most important thing is to have the right features: those capturing historical information about the user or ad dominate other types of features. 
**予想通り、最も重要なことは適切な特徴を持つことです：ユーザや広告に関する歴史的情報を捉える特徴が他のタイプの特徴を支配します。**
Once we have the right features and the right model (decisions trees plus logistic regression), other factors play small roles (though even small improvements are important at scale). 
適切な特徴と適切なモデル（決定木とロジスティック回帰）が揃ったら、他の要因は小さな役割を果たします（ただし、小さな改善でもスケールでは重要です）。
Picking the optimal handling for data freshness, learning rate schema and data sampling improve the model slightly, though much less than adding a high-value feature, or picking the right model to begin with. 
**データの新鮮さ、学習率スキーマ、およびデータサンプリングの最適な処理を選択することでモデルがわずかに改善されますが、高価値の特徴を追加することや、最初に適切なモデルを選ぶことに比べるとはるかに少ない**です。

<!-- ここまで読んだ! -->

We begin with an overview of our experimental setup in Section 2. 
私たちは、セクション2で実験設定の概要から始めます。
In Section 3 we evaluate different probabilistic linear classifiers and diverse online learning algorithms. 
セクション3では、さまざまな確率的線形分類器と多様なオンライン学習アルゴリズムを評価します。
In the context of linear classification we go on to evaluate the impact of feature transforms and data freshness. 
線形分類の文脈において、特徴変換とデータの新鮮さの影響を評価します。
Inspired by the practical lessons learned, particularly around data freshness and online learning, we present a model architecture that incorporates an online learning layer, whilst producing fairly compact models. 
特にデータの新鮮さとオンライン学習に関する実践的な教訓に触発され、オンライン学習レイヤーを組み込んだモデルアーキテクチャを提示し、比較的コンパクトなモデルを生成します。
Section 4 describes a key component required for the online learning layer, the online joiner, an experimental piece of infrastructure that can generate a live stream of real-time training data. 
セクション4では、オンライン学習レイヤーに必要な重要なコンポーネントであるオンラインジョイナー、リアルタイムのトレーニングデータのライブストリームを生成できる実験的なインフラストラクチャについて説明します。

Lastly we present ways to trade accuracy for memory and compute time and to cope with massive amounts of training data. 
最後に、精度とメモリおよび計算時間をトレードオフする方法と、大量のトレーニングデータに対処する方法を提示します。
In Section 5 we describe practical ways to keep memory and latency contained for massive scale applications and in Section 6 we delve into the tradeoff between training data volume and accuracy. 
セクション5では、大規模アプリケーションのためにメモリとレイテンシを抑える実用的な方法を説明し、セクション6ではトレーニングデータのボリュームと精度のトレードオフについて掘り下げます。

<!-- ここまで読んだ -->

## 2. EXPERIMENTAL SETUP 実験設定

In order to achieve rigorous and controlled experiments, we prepared offline training data by selecting an arbitrary week of the 4th quarter of 2013. 
厳密で制御された実験を実現するために、2013年第4四半期の任意の週を選択してオフラインのトレーニングデータを準備しました。 
In order to maintain the same training and testing data under different conditions, we prepared offline training data which is similar to that observed online. 
異なる条件下で同じトレーニングデータとテストデータを維持するために、オンラインで観察されたものに類似したオフラインのトレーニングデータを準備しました。 
We partition the stored offline data into training and testing and use them to simulate the streaming data for online training and prediction. 
**保存されたオフラインデータをトレーニングとテストに分割し、それを使用してオンラインのトレーニングと予測のためのストリーミングデータをシミュレートします。**
The same training/testing data are used as testbed for all the experiments in the paper. 
同じトレーニング/テストデータが、論文内のすべての実験のテストベッドとして使用されます。

**Evaluation metrics**: Since we are most concerned with the impact of the factors to the machine learning model, we use the accuracy of prediction instead of metrics directly related to profit and revenue. 
**評価指標**：私たちが最も関心を持っているのは機械学習モデルへの要因の影響であるため、利益や収益に直接関連する指標の代わりに予測の精度を使用します。
In this work, we use Normalized Entropy (NE) and calibration as our major evaluation metric. 
本研究では、Normalized Entropy (NE) とキャリブレーションを主要な評価指標として使用します。

_Normalized Entropy or more accurately, Normalized Cross-_ Entropy is equivalent to the average log loss per impression divided by what the average log loss per impression would be if a model predicted the background click through rate (CTR) for every impression. 
_正規化エントロピー、より正確には正規化交差エントロピーは、各インプレッションあたりの平均ログ損失を、モデルがすべてのインプレッションに対して背景のクリック率（CTR）を予測した場合の平均ログ損失で割ったものに相当します。 
In other words, it is the predictive log loss normalized by the entropy of the background CTR. 
言い換えれば、これは背景CTRのエントロピーで正規化された予測ログ損失です。 
The background CTR is the average empirical CTR of the training data set. 
背景CTRは、トレーニングデータセットの平均経験的CTRです。 
It would be perhaps more descriptive to refer to the metric as the Normalized Logarithmic Loss. 
この指標をNormalized Logarithmic Lossと呼ぶ方が、より説明的かもしれません。 
The lower the value is, the better is the prediction made by the model. 
値が低いほど、モデルによる予測が良いことを示します。 
The reason for this normalization is that the closer the background CTR is to either 0 or 1, the easier it is to achieve a better log loss. 
この正規化の理由は、背景CTRが0または1に近いほど、より良いログ損失を達成しやすくなるからです。 
Dividing by the entropy of the background CTR makes the NE insensitive to the background CTR. 
背景CTRのエントロピーで割ることで、NEは背景CTRに対して鈍感になります。 
Assume a given training data set has _N examples with labels yi ∈{−1, +1} and estimated prob-_ ability of click pi where i = 1, 2, ...N . 
与えられたトレーニングデータセットが、ラベル $y_i \in \{-1, +1\}$ を持つ $N$ の例と、推定クリック確率 $p_i$ を持つと仮定します（$i = 1, 2, ...N$）。 
The average empirical CTR as $p$ 
平均経験的CTRを $p$ とすると、 

$$
NE = -\frac{1}{N} \sum_{i=1}^{N} \left( \frac{1 + y_i}{2} \log(p_i) + \frac{1 - y_i}{2} \log(1 - p_i) \right)
$$

is essentially a component in calculating Relative Information Gain (RIG) and RIG = 1 − _NE_  
は、相対情報利得（RIG）を計算するための成分であり、$RIG = 1 - NE$ です。

<!-- ここまで読んだ! -->



_Calibration is the ratio of the average estimated CTR and_ empirical CTR. 
_キャリブレーションは、平均推定CTRと経験的CTRの比率です。 
In other words, it is the ratio of the number of expected clicks to the number of actually observed clicks. 
言い換えれば、期待されるクリック数と実際に観察されたクリック数の比率です。 
Calibration is a very important metric since accurate and well-calibrated prediction of CTR is essential to the success of online bidding and auction. 
キャリブレーションは非常に重要な指標であり、CTRの正確で適切にキャリブレーションされた予測は、オンライン入札およびオークションの成功に不可欠です。 
The less the calibration differs from 1, the better the model is. 
キャリブレーションが1から離れていないほど、モデルは優れています。 
We only report calibration in the experiments where it is non-trivial. 
私たちは、非自明な実験においてのみキャリブレーションを報告します。 

Note that, Area-Under-ROC (AUC) is also a pretty good metric for measuring ranking quality without considering calibration. 
なお、ROC曲線下面積（AUC）もキャリブレーションを考慮せずにランキング品質を測定するための良い指標です。 
In a realistic environment, we expect the prediction to be accurate instead of merely getting the optimal ranking order to avoid potential under-delivery or overdelivery. 
現実的な環境では、潜在的な過少配信や過剰配信を避けるために、単に最適なランキング順を得るのではなく、予測が正確であることを期待します。 
NE measures the goodness of predictions and implicitly reflects calibration. 
NEは予測の良さを測定し、暗黙的にキャリブレーションを反映します。 
For example, if a model overpredicts by 2x and we apply a global multiplier 0.5 to fix the calibration, the corresponding NE will be also improved even though AUC remains the same. 
例えば、モデルが2倍に過大予測し、キャリブレーションを修正するためにグローバル乗数0.5を適用すると、対応するNEも改善されますが、AUCは同じままです。 
See [12] for in-depth study on these metrics. 
これらの指標に関する詳細な研究については[12]を参照してください。

<!-- ここまで読んだ! -->

## 3. PREDICTION MODEL STRUCTURE 予測モデル構造

![]()
Figure 1: Hybrid model structure.
Input features are transformed by means of boosted decision trees. 
The output of each individual tree is treated as a categorical input feature to a sparse linear classifier. 
Boosted decision trees prove to be very powerful feature transforms. 
図1：ハイブリッドモデル構造。 入力特徴は ブーストされた決定木によって変換されます。 各個別の木の出力は、 **スパース線形分類器へのカテゴリカル入力特徴として扱われます**。ブーストされた決定木は非常に強力な特徴変換であることが証明されています。
(ロジスティック回帰モデルの入力は、スパースなバイナリベクトルなのか...!:thinking:)

<!-- ここまで読んだ! -->

In this section we present a hybrid model structure: the concatenation of boosted decision trees and of a probabilistic sparse linear classifier, illustrated in Figure 1. 
このセクションでは、ブーストされた決定木と確率的スパース線形分類器の連結というハイブリッドモデル構造を提示します。これは図1に示されています。
In Section 3.1 we show that decision trees are very powerful input feature transformations, that significantly increase the accuracy of probabilistic linear classifiers. 
セクション3.1では、決定木が非常に強力な入力特徴変換であり、確率的線形分類器の精度を大幅に向上させることを示します。
In Section 3.2 we show how fresher training data leads to more accurate predictions. 
セクション3.2では、新しいトレーニングデータがどのようにより正確な予測につながるかを示します。
This motivates the idea to use an online learning method to train the linear classifier. 
これにより、線形分類器をトレーニングするためにオンライン学習手法を使用するというアイデアが生まれます。
In Section 3.3 we compare a number of online learning variants for two families of probabilistic linear classifiers. 
セクション3.3では、2つのファミリーの確率的線形分類器に対するいくつかのオンライン学習のバリアントを比較します。

<!-- ここまで読んだ! -->

The online learning schemes we evaluate are based on the  Stochastic Gradient Descent (SGD) algorithm [2] applied to_ sparse linear classifiers. 
評価するオンライン学習スキームは、スパース線形分類器に適用される_確率的勾配降下法（SGD）アルゴリズム[2]_に基づいています。
After feature transformation, an ad impression is given in terms of a structured vector $x = (e_{i1}, \ldots, e_{in})$ where $e_i$ is the i-th unit vector and $i_1, \ldots, i_n$ are the values of the n categorical input features. 
特徴変換の後、広告インプレッションは構造化ベクトル $x = (e_{i1}, \ldots, e_{in})$の形で与えられます。ここで、$e_i$ はi番目の単位ベクトルであり、$i_1, \ldots, i_n$ はn個のカテゴリカル入力特徴の値です。(=入力特徴量はn次元のone-hotベクトル?:thinking:)
In the training phase, we also assume that we are given a binary label $y \in \{+1, -1\}$ indicating a click or no-click. 
**トレーニングフェーズでは、クリックまたは非クリックを示すバイナリラベル$y \in \{+1, -1\}$が与えられると仮定**します。(はいはい。binary形式のrewardね...!:thinking:)

Given a labeled ad impression $(x, y)$, let us denote the linear combination of active weights as  
ラベル付き広告インプレッション$(x, y)$が与えられた場合、アクティブウェイトの線形結合を次のように表します。  

$$
s(y, x, w) = y \cdot w^T x = y \sum_{j=1}^{n} w_{j, i_j}
\tag{2}
$$

- メモ: 線形スコアの定義
  - $s(y, x, w)$ = スコア関数
  - $y$ = ラベル (クリックなら+1, 非クリックなら-1)
  - $x$ = 特徴量ベクトル
  - $w$ = 現在のモデルの重みベクトル
  - 上式の役割: マージン。このスコア関数の値が正で大きいほど「正解ラベルと同じ方向に自信を持って予測してる」ことを意味する。負で小さいほど「誤った方向に自信を持って予測してる」ことを意味する。

where $w$ is automatically controlled by the belief uncertainty $\sigma$. 
ここで $w$ は信念(=ベイズ推定の概念だ!)の不確実性 $\sigma$ によって自動的に制御されます。



In the state of the art Bayesian online learning scheme for
probit regression (BOPR) described in [7] the likelihood and
prior are given by
ベイジアンオンライン学習スキームの最先端である[7]で説明されているプロビット回帰（BOPR）では、尤度関数と事前分布は次のように与えられます。

$$
p(y|x,w) = \Phi(\frac{s(y,x,w)}{\beta})
$$

$$
p(w) = \prod_{k=1}^{N} N(w_k; \mu_{k}, \sigma_{k}^2)
$$

- メモ:
  - 尤度関数(likelihood function)について。
    - 意味: 観測データが与えられたときに、モデルパラメータがそのデータを生成する最もらしさ(尤度)
    - $\Phi$ = 標準正規分布の累積密度関数。ロジスティック回帰がシグモイド関数を使ってスコアを0~1の確率に変換するのに対し、プロビット回帰はこの$\Phi$関数 (これもS字カーブの関数)を使う。
    - $s(y,x,w)$ = 先ほど定義した線形スコア関数。予測の合ってる度合いを表す。
    - $\beta$ = ノイズパラメータ。予測の「曖昧さ」を調整する定数。
    - 直感的な意味: 線形モデルが計算したスコア $s$ が高いほど、、$\Phi(\frac{s}{\beta})$ の値は1に近づき、クリック確率が高いと予測する。
  - (モデルパラメータの)事前分布(prior distribution)について。
    - 意味: モデルの重み $w$ がどのような値を取りうるか、という事前の確率分布(信念)を表す。(実際には確率変数ではないだろうが、たぶんこの辺りの値かなという主観的な分布を表すイメージ...!:thnking:)
    - $N(w_k; \mu_{k}, \sigma_{k}^2)$ = 各重み $w_k$ が、平均 $\mu_k$、分散 $\sigma_k^2$ の正規分布に従うと仮定。
    - $\prod_{k=1}^{N}$ = 全ての重み(回帰係数)がが、「互いに独立に」分布していると仮定してるので、同時確率分布が各重みの確率分布の積で表される。

<!-- ここまで読んだ -->

where Φ(t) is the cumulative density function of standard normal distribution and N(t) is the density function of the standard normal distribution. The online training is achieved through expectation propagation with moment matching. The resulting model consists of the mean and the variance of the approximate posterior distribution of weight vector w. The inference in the BOPR algorithm is to compute p(w|y, x) and project it back to the closest factorizing Gaussian approximation of p(w). Thus, the update algorithm can be solely expressed in terms of update equations for all means and variances of the non-zero components x (see [7]):
ここで $\Phi(t)$ は標準正規分布の累積密度関数であり、$N(t)$ は標準正規分布の密度関数です。オンライン学習は、モーメントマッチングを用いた期待値伝播を通じて達成されます。得られたモデルは、重みベクトル $w$ の近似事後分布の平均と分散で構成されます。BOPRアルゴリズムの推論は、$p(w|y, x)$ を計算し、それを $p(w)$ の最も近い因子化ガウス近似に投影し直すことです。したがって、更新アルゴリズムは、非ゼロ成分 $x$ のすべての平均と分散の更新方程式の観点から以下のように表現できます（[7]を参照）:

$$
\mu_{i_{j}}　<- \mu_{i_{j}} + y \cdot \frac{\sigma_{i_{j}}^2}{\sqrt{\beta^2 + \sum_{j=1}^{n} \sigma_{i_j}^2}} \cdot \frac{N(t)}{\Phi(t)}
$$

In Subsection 3.3 we will present various step-size functions $\eta$ and compare to BOPR. 
サブセクション3.3では、さまざまなステップサイズ関数 $\eta$ を提示し、BOPRと比較します。
Both SGD-based LR and BOPR described above are stream learners as they adapt to training data one

<!-- ここは一旦後回し。線形回帰モデルの学習方法の話なので! -->

## 3.1 Decision tree feature transforms 決定木特徴変換

There are two simple ways to transform the input features of a linear classifier in order to improve its accuracy. 
線形分類器の入力特徴を変換して精度を向上させるための2つの簡単な方法があります。
For continuous features, a simple trick for learning non-linear transformations is to bin the feature and treat the bin index as a categorical feature. 
連続特徴に対して、非線形変換を学習するための簡単なトリックは、特徴をビンに分け、そのビンのインデックスをカテゴリカル特徴として扱うことです。
The linear classifier effectively learns a piece-wise constant non-linear map for the feature. 
線形分類器は、特徴に対して効果的に区分定数の非線形マップを学習します。
It is important to learn useful bin boundaries, and there are many information maximizing ways to do this. 
有用なビンの境界を学習することが重要であり、これを行うための情報を最大化する方法は多くあります。

The second simple but effective transformation consists in building tuple input features. 
2つ目の簡単ですが効果的な変換は、タプル入力特徴を構築することです。
For categorical features, the brute force approach consists in taking the Cartesian product, i.e. in creating a new categorical feature that takes as values all possible values of the original features. 
カテゴリカル特徴に対して、ブルートフォースアプローチは、直積を取ること、すなわち元の特徴のすべての可能な値を値として持つ新しいカテゴリカル特徴を作成することです。
Not all combinations are useful, and those that are not can be pruned out. 
すべての組み合わせが有用であるわけではなく、有用でないものは剪定することができます。
If the input features are continuous, one can do joint binning, using for example a k-d tree. 
入力特徴が連続の場合、例えばk-dツリーを使用して共同ビン分けを行うことができます。

We found that boosted decision trees are a powerful and very convenient way to implement non-linear and tuple transformations of the kind we just described. 
私たちは、**ブーステッド決定木が、先に述べたような非線形およびタプル変換を実装するための強力で非常に便利な方法である**ことを発見しました。
We treat each individual tree as a categorical feature that takes as value the index of the leaf an instance ends up falling in. 
各個別の木を、インスタンスが落ち着く葉のインデックスを値とするカテゴリカル特徴として扱います。
We use 1of-K coding of this type of features. 
このタイプの特徴に1of-Kコーディングを使用します。
For example, consider the boosted tree model in Figure 1 with 2 subtrees, where the first subtree has 3 leafs and the second 2 leafs. 
例えば、図1のブーステッドツリーモデルを考えてみましょう。ここでは、最初のサブツリーに3つの葉があり、2つ目のサブツリーに2つの葉があります。
If an instance ends up in leaf 2 in the first subtree and leaf 1 in second subtree, the overall input to the linear classifier will be the binary vector [0, 1, 0, 1, 0], where the first 3 entries correspond to the leaves of the first subtree and last 2 to those of the second subtree. 
**インスタンスが最初のサブツリーの葉2に、2つ目のサブツリーの葉1に落ち着くと、線形分類器への全体の入力はバイナリベクトル[0, 1, 0, 1, 0]になります**。ここで、最初の3つのエントリは最初のサブツリーの葉に対応し、最後の2つは2つ目のサブツリーの葉に対応します。
The boosted decision trees we use follow the Gradient Boosting Machine (GBM) [5], where the classic L2-TreeBoost algorithm is used. 
私たちが使用するブーステッド決定木は、Gradient Boosting Machine (GBM) [5]に従い、古典的なL2-TreeBoostアルゴリズムが使用されます。
In each learning iteration, a new tree is created to model the residual of previous trees. 
各学習イテレーションで、新しい木が作成され、前の木の残差をモデル化します。
We can understand boosted decision tree based transformation as a supervised feature encoding that converts a real-valued vector into a compact binary-valued vector. 
**ブーステッド決定木に基づく変換は、実数値ベクトルをコンパクトなバイナリ値ベクトルに変換する教師あり特徴エンコーディングとして理解できます。**
A traversal from root node to a leaf node represents a rule on certain features. 
ルートノードから葉ノードへのトラバースは、特定の特徴に関するルールを表します。
Fitting a linear classifier on the binary vector is essentially learning weights for the set of rules. 
バイナリベクトルに線形分類器を適合させることは、本質的にルールのセットに対する重みを学習することです。
Boosted decision trees are trained in a batch manner. 
ブーステッド決定木はバッチ方式で訓練されます。

We carry out experiments to show the effect of including tree features as inputs to the linear model. 
私たちは、線形モデルへの入力として木の特徴を含めることの効果を示す実験を行います。
In this experiment we compare two logistic regression models, one with tree feature transforms and the other with plain (non-transformed) features. 
この実験では、木の特徴変換を含むロジスティック回帰モデルと、通常の（変換されていない）特徴を持つモデルの2つを比較します。
We also use a boosted decision tree model only for comparison. 
比較のために、ブーステッド決定木モデルも使用します。
Table 1 shows the results. 
表1は結果を示しています。

![]()
Table 1: Logistic regression(LR) and boosted decision tree(Trees) make a powerful combination. We evaluate them by their Normalized Entropy (NE) relative to that of the Trees only model.
表1: ロジスティック回帰（LR）とブーステッド決定木（Trees）は強力な組み合わせを作ります。私たちは、それらをTreesのみのモデルに対するNormalized Entropy（NE）で評価します。

<!-- ここまで読んだ! -->

Tree feature transformations help decrease Normalized Entropy by more more than 3.4% relative to the Normalized Entropy of the model with no tree transforms. 
木の特徴変換は、木の変換がないモデルのNormalized Entropyに対して3.4%以上Normalized Entropyを減少させるのに役立ちます。
This is a very significant relative improvement. 
これは非常に重要な相対的改善です。
For reference, a typical feature engineering experiment will shave off a couple of tens of a percent of relative NE. 
参考までに、典型的な特徴エンジニアリング実験では、相対NEを数パーセント削減することが一般的です。
It is interesting to see that the LR and Tree models used in isolation have comparable prediction accuracy (LR is a bit better), but that it is their combination that yield an accuracy leap. 
単独で使用されるLRとTreeモデルは同等の予測精度を持っていることが興味深いです（LRの方が少し良い）が、それらの組み合わせが精度の飛躍をもたらすことです。
The gain in prediction accuracy is significant; for reference, the majority of feature engineering experiments only manage to decrease Normalized Entropy by a fraction of a percentage.
予測精度の向上は顕著です。参考までに、特徴エンジニアリング実験の大部分は、Normalized Entropyをわずかに減少させることしかできません。

<!-- ここまで読んだ! -->

## 3.2 データの新鮮さ

Click prediction systems are often deployed in dynamic environments where the data distribution changes over time. 
クリック予測システムは、データ分布が時間とともに変化する動的な環境でしばしば展開されます。
We study the effect of training data freshness on predictive performance. 
私たちは、トレーニングデータの新鮮さが予測性能に与える影響を研究します。
To do this we train a model on one particular day and test it on consecutive days. 
これを行うために、特定の日にモデルをトレーニングし、連続する日でテストします。
We run these experiments both for a boosted decision tree model, and for a logisitic regression model with tree-transformed input features. 
これらの実験は、ブーストされた決定木モデルと、ツリー変換された入力特徴を持つロジスティック回帰モデルの両方で実施します。

In this experiment we train on one day of data, and evaluate on the six consecutive days and compute the normalized entropy on each. 
この実験では、1日のデータでトレーニングし、6日間の連続した日で評価し、それぞれの正規化エントロピーを計算します。
The results are shown on Figure 2. 
結果は図2に示されています。

Prediction accuracy clearly degrades for both models as the delay between training and test set increases. 
予測精度は、トレーニングセットとテストセットの遅延が増加するにつれて、両方のモデルで明らかに低下します。
For both models it can been seen that NE can be reduced by approximately 1% by going from training weekly to training daily. 
両方のモデルにおいて、週単位のトレーニングから日単位のトレーニングに移行することで、NEを約1%削減できることがわかります。

These findings indicate that it is worth retraining on a daily basis. 
これらの発見は、日々の再トレーニングが価値があることを示しています。
One option would be to have a recurring daily job that retrains the models, possibly in batch. 
**1つの選択肢は、モデルを再トレーニングする定期的な日次ジョブを持つことであり、バッチ処理で行うことも可能**です。
The time needed to retrain boosted decision trees varies, depending on factors such as number of examples for training, number of trees, number of leaves in each tree, cpu, memory, etc. 
ブーストされた決定木を再トレーニングするのに必要な時間は、トレーニングのための例の数、木の数、各木の葉の数、CPU、メモリなどの要因によって異なります。
It may take more than 24 hours to build a boosting model with hundreds of trees from hundreds of millions of instances with a single core cpu. 
単一コアのCPUで数億のインスタンスから数百の木を持つブースティングモデルを構築するには、24時間以上かかることがあります。
In a practical case, the training can be done within a few hours via sufficient concurrency in a multi-core machine with large amount of memory for holding the whole training set. 
実際のケースでは、全トレーニングセットを保持するための大量のメモリを持つマルチコアマシンで十分な同時実行性を利用することで、トレーニングは数時間以内に行うことができます。
In the next section we consider an alternative. 
次のセクションでは、別の選択肢を考慮します。
The boosted decision trees can be trained daily or every couple of days, but the linear classifier can be trained in near real-time by using some flavor of online learning. 
**ブーストされた決定木は日々または数日に1回トレーニングできますが、線形分類器はオンライン学習の一種を使用することでほぼリアルタイムでトレーニングできます**。

<!-- ここまで読んだ! -->

## 3.3 オンライン線形分類器

In order to maximize data freshness, one option is to train the linear classifier online, that is, directly as the labelled ad impressions arrive. 
データの新鮮さを最大化するための一つの選択肢は、線形分類器をオンラインで訓練することです。つまり、ラベル付き広告インプレッションが到着する際に直接訓練します。
In the upcoming Section 4 we descibe a piece of infrastructure that could generate real-time training data. 
次のセクション4では、リアルタイムのトレーニングデータを生成できるインフラストラクチャの一部について説明します。
In this section we evaluate several ways of setting learning rates for SGD-based online learning for logistic regression. 
このセクションでは、ロジスティック回帰のSGDベースのオンライン学習のための学習率を設定するいくつかの方法を評価します。
We then compare the best variant to online learning for the BOPR model. 
その後、最良のバリアントをBOPRモデルのオンライン学習と比較します。

<!-- ここまで読んだ! -->

In terms of (6), we explore the following choices: 
式(6)に関して、以下の選択肢を探ります：

1. Per-coordinate learning rate: The learning rate for feature i at iteration t is set to 
    特徴ごとの学習率：イテレーションtでの特徴iの学習率は次のように設定されます。

$$
\alpha \eta_{t,i} = \frac{\alpha}{\beta + \sum_{j=1}^{t} [\nabla]_{j,i}^2}
$$

α, β are two tunable parameters (proposed in [8])._
（ここで、_α_と_β_は調整可能な2つのパラメータです（[8]で提案されています）。）

2. Per-weight square root learning rate:  重みごとの平方根学習率：

$$
\alpha \eta_{t,i} = \sqrt{n_{t,i}},
$$

where $n_{t,i}$ is the total training instances with feature $i$ till iteration $t.$
ここで、$n_{t,i}$はイテレーション$t$までの特徴$i$を持つトレーニングインスタンスの合計です。

3. Per-weight learning rate: 重みごとの学習率：

$$
\eta_{t,i} = \frac{\alpha}{n_{t,i}}.
$$

4.  Global learning rate: グローバル学習率：

$$
\eta_{t,i} = \frac{\alpha}{\sqrt{t}}.
$$

5. Constant learning rate: 定数学習率：

$$
\eta_{t,i} = \alpha.
$$

- メモ: 学習率のバリエーション
  - パターン1: 重みごとの学習率について
    - 単純に「その特徴量が何回登場したか」に基づいて学習率を調整する方法(Tree系モデルで特徴量作ってるから、multi-hotベクトルなので。
      - 各要素が1回登場するたびに学習率を少しずつ下げていくイメージ...!:thinking:)
    - 結果: 論文内では、一番悪いパフォーマンスを示した。
      - 理由: 学習率が「急激に下がりすぎる(decrease too fast)」ため。まだモデルが十分に学習し切れてない(最適な重みに到達してない)段階でも、登場回数が多いという理由だけで学習率がほぼゼロになり、学習が早期終了してしまう。
  - パターン2: 座標ごとの学習率(per-coordinate learning rate)について
    - 「過去の勾配(誤差の大きさ)の蓄積」に基づいて学習率を決める手法。(AdaGradと呼ばれる手法に相当する)
      - 分母にあるのは、登場回数ではなく、過去の勾配($\nabla$)の2乗和。
      - 予測を大きく外して勾配(修正量)が大きいときは、分母があまり大きくならず、学習率が保たれる。
      - 逆に、勾配が小さく安定してくると、徐々に学習率が下がっていく。
    - 結果: 論文内では、一番良いパフォーマンスを示した。
      - 理由: ベイズ的なアプローチ（BOPR）と同様に、**モデルパラメータの各値の「不確実性」に応じて学習の強さを自動調整できるため。まだ確信が持てない（勾配が大きい）特徴量は強く学習し、確信が持てるようになったら学習を弱めるという理想的な挙動**をしてる。
The first three schemes set learning rates individually per feature. 
最初の3つのスキームは、特徴ごとに個別に学習率を設定します。
The last two use the same rate for all features. 
最後の2つは、すべての特徴に同じレートを使用します。
All the tunable parameters are optimized by grid search (optima detailed in Table 2.) 
すべての調整可能なパラメータはグリッドサーチによって最適化されます（最適値は表2に詳細があります）。

<!-- ここまで読んだ! -->

We lower bound the learning rates by 0.00001 for continuous learning. 
連続学習のために、学習率の下限を0.00001に設定します。
We train and test LR models on same data with the above learning rate schemes. 
上記の学習率スキームを使用して、同じデータでLRモデルを訓練およびテストします。
The experiment results are shown in Figure 3. 
実験結果は図3に示されています。

From the above result, SGD with per-coordinate learning rate achieves the best prediction accuracy, with a NE almost 5% lower than when using per weight learning rate, which performs worst. 
上記の結果から、特徴ごとの学習率を用いたSGDが最も優れた予測精度を達成し、重みごとの学習率を使用した場合よりもNEがほぼ5％低くなります。これは最も悪いパフォーマンスを示します。
This result is in line with the conclusion in [8]. 
この結果は[8]の結論と一致しています。
SGD with per-weight square root and constant learning rate achieves similar and slightly worse NE. 
重みごとの平方根および定数学習率を用いたSGDは、類似したNEを達成しますが、わずかに悪化します。
The other two schemes are significant worse than the previous versions. 
他の2つのスキームは、前のバージョンよりも著しく悪化しています。
The global learning rate fails mainly due to the imbalance of number of training instance on each features. 
グローバル学習率は、各特徴のトレーニングインスタンスの数の不均衡が主な原因で失敗します。
Since each training instance may consist of different features, some popular features receive much more training instances than others. 
各トレーニングインスタンスは異なる特徴で構成される可能性があるため、人気のある特徴は他の特徴よりもはるかに多くのトレーニングインスタンスを受け取ります。
Under the global learning rate scheme, the learning rate for the features with fewer instances decreases too fast, and prevents convergence to the optimum weight. 
グローバル学習率スキームの下では、インスタンスが少ない特徴の学習率が急速に減少し、最適な重みへの収束を妨げます。

Although the per-weight learning rates scheme addresses this problem, it still fails because it decreases the learning rate for all features too fast. 
重みごとの学習率スキームはこの問題に対処しますが、すべての特徴の学習率を急速に減少させるため、依然として失敗します。

Training terminates too early where the model converges to a sub-optimal point. 
トレーニングは早すぎる段階で終了し、モデルがサブ最適点に収束します。

This explains why this scheme has the worst performance among all the choices. 
これが、このスキームがすべての選択肢の中で最も悪いパフォーマンスを示す理由です。

It is interesting to note that the BOPR update equation (3) for the mean is most similar to per-coordinate learning rate version of SGD for LR. 
BOPRの平均に対する更新方程式（3）が、LRの特徴ごとの学習率バージョンのSGDに最も類似していることは興味深いです。

The effective learning rate for BOPR is specific to each coordinate, and depends on the posterior variance of the weight associated to each individual coordinate, as well as the “surprise” of label given what the model would have predicted [7]. 
BOPRの効果的な学習率は各座標に特有であり、各個別の座標に関連する重みの事後分散や、モデルが予測した内容に基づくラベルの「驚き」に依存します[7]。

We carry out an experiment to compare the prediction performance of LR trained with per-coordinate SGD and BOPR. 
私たちは、特徴ごとのSGDで訓練されたLRとBOPRの予測性能を比較する実験を行います。

We train both LR and BOPR models on the same training data and evaluate the prediction performance on the next day. 
同じトレーニングデータでLRとBOPRモデルの両方を訓練し、翌日の予測性能を評価します。

The result is shown in Table 3. 
結果は表3に示されています。

**Table 3: Per-coordinate online LR versus BOPR**
**表3: 特徴ごとのオンラインLR対BOPR**

|Model Type|NE (relative to LR)|
|---|---|
|LR|100% (reference)|
|BOPR|99.82%|

Perhaps as one would expect, given the qualitative similarity of the update equations, BOPR and LR trained with SGD with per-coordinate learning rate have very similar prediction performance in terms of both NE and also calibration (not shown in the table). 
更新方程式の定性的な類似性を考慮すると予想通りかもしれませんが、BOPRと特徴ごとの学習率でSGDで訓練されたLRは、NEとキャリブレーションの両方において非常に類似した予測性能を持っています（表には示されていません）。

One advantages of LR over BOPR is that the model size is half, given that there is only a weight associated to each sparse feature value, rather than a mean and a variance. 
LRのBOPRに対する一つの利点は、各スパース特徴値に関連付けられた重みのみがあるため、モデルサイズが半分であることです。

Depending on the implementation, the smaller model size may lead to better cache locality and thus faster cache lookup. 
実装によっては、より小さなモデルサイズがキャッシュの局所性を向上させ、結果としてキャッシュの検索が速くなる可能性があります。

In terms of computational expense at prediction time, the LR model only requires one inner product over the feature vector and the weight vector, while BOPR models needs two inner products for both variance vector and mean vector with the feature vector. 
予測時の計算コストに関して、LRモデルは特徴ベクトルと重みベクトルの間で1つの内積のみを必要としますが、BOPRモデルは特徴ベクトルとの間で分散ベクトルと平均ベクトルの両方に対して2つの内積を必要とします。

One important advantage of BOPR over LR is that being a Bayesian formulation, it provides a full predictive distribution over the probability of click. 
BOPRのLRに対する重要な利点の一つは、ベイズの定式化であるため、クリックの確率に対する完全な予測分布を提供することです。

This can be used to compute percentiles of the predictive distribution, which can be used for explore/exploit learning schemes [3]. 
これは予測分布のパーセンタイルを計算するために使用でき、探索/活用学習スキーム[3]に利用できます。



## 4. ONLINE DATA JOINER

The previous section established that fresher training data results in increased prediction accuracy. 
前のセクションでは、新しいトレーニングデータが予測精度の向上につながることを示しました。

It also presented a simple model architecture where the linear classifier layer is trained online. 
また、線形分類器層がオンラインでトレーニングされるシンプルなモデルアーキテクチャを提示しました。

This section introduces an experimental system that generates real-time training data used to train the linear classifier via online learning. 
このセクションでは、オンライン学習を通じて線形分類器をトレーニングするために使用されるリアルタイムトレーニングデータを生成する実験システムを紹介します。

We will refer to this system as the “online joiner” since the critical operation it does is to join labels (click/no-click) to training inputs (ad impressions) in an online manner. 
このシステムを「オンラインジョイナー」と呼びます。なぜなら、重要な操作は、ラベル（クリック/非クリック）をトレーニング入力（広告インプレッション）にオンラインで結合するからです。

Similar infrastructure is used for stream learning for example in the Google Advertising System [1]. 
同様のインフラは、例えばGoogle広告システム[1]におけるストリーム学習にも使用されています。

The online joiner outputs a real-time training data stream to an infrastructure called Scribe [10]. 
オンラインジョイナーは、Scribe [10]と呼ばれるインフラにリアルタイムトレーニングデータストリームを出力します。

While the positive labels (clicks) are well defined, there is no such thing as a “no click” button the user can press. 
ポジティブラベル（クリック）は明確に定義されていますが、ユーザーが押すことのできる「非クリック」ボタンは存在しません。

For this reason, an impression is considered to have a negative no click label if the user did not click the ad after a fixed, and sufficiently long period of time after seeing the ad. 
このため、ユーザーが広告を見た後、固定された十分に長い時間内に広告をクリックしなかった場合、そのインプレッションはネガティブな非クリックラベルを持つと見なされます。

The length of the waiting time window needs to be tuned carefully. 
待機時間ウィンドウの長さは慎重に調整する必要があります。

Using too long a waiting window delays the real-time training data and increases the memory allocated to buffering impressions while waiting for the click signal. 
待機ウィンドウが長すぎると、リアルタイムトレーニングデータが遅延し、クリック信号を待っている間にインプレッションをバッファリングするために割り当てられるメモリが増加します。

A too short time window causes some of the clicks to be lost, since the corresponding impression may have been flushed out and labeled as non-clicked. 
時間ウィンドウが短すぎると、対応するインプレッションがフラッシュアウトされ、非クリックとしてラベル付けされる可能性があるため、一部のクリックが失われることになります。

This negatively affects “click coverage,” the fraction of all clicks successfully joined to impressions. 
これは「クリックカバレッジ」に悪影響を及ぼし、すべてのクリックの中でインプレッションに成功裏に結合された割合を低下させます。

As a result, the online joiner system must strike a balance between recency and click coverage. 
その結果、オンラインジョイナーシステムは新鮮さとクリックカバレッジのバランスを取る必要があります。

Not having full click coverage means that the real-time training set will be biased: the empirical CTR that is somewhat lower than the ground truth. 
完全なクリックカバレッジがないことは、リアルタイムトレーニングセットがバイアスを持つことを意味します。すなわち、実際のCTRが真実よりもやや低くなります。

This is because a fraction of the impressions labeled non-clicked would have been labeled as clicked if the waiting time had been long enough. 
これは、非クリックとしてラベル付けされたインプレッションの一部が、待機時間が十分に長ければクリックとしてラベル付けされていたであろうからです。

In practice however, we found that it is easy to reduce this bias to decimal points of a percentage with waiting window sizes that result in manageable memory requirements. 
しかし、実際には、管理可能なメモリ要件を満たす待機ウィンドウサイズでこのバイアスを小数点以下のパーセンテージに減少させることが容易であることがわかりました。

In addition, this small bias can be measured and corrected for. 
さらに、この小さなバイアスは測定され、修正することができます。

More study on the window size and efficiency can be found at [6]. 
ウィンドウサイズと効率に関するさらなる研究は[6]にあります。

The online joiner is designed to perform a distributed stream-to-stream join on ad impressions and ad clicks utilizing a request ID as the primary component of the join predicate. 
オンラインジョイナーは、リクエストIDを結合述語の主要なコンポーネントとして利用し、広告インプレッションと広告クリックの分散ストリーム間結合を実行するように設計されています。

A request ID is generated every time a user performs an action on Facebook that triggers a refresh of the content they are exposed to. 
リクエストIDは、ユーザーがFacebook上でコンテンツのリフレッシュを引き起こすアクションを実行するたびに生成されます。

A schematic data and model flow for the online joiner consequent online learning is shown in Figure 4. 
オンラインジョイナーによるオンライン学習のためのデータとモデルの流れの概略は図4に示されています。

The initial data stream is generated when a user visits Facebook and a request is made to the ranker for candidate ads. 
初期データストリームは、ユーザーがFacebookを訪れ、候補広告のためにランカーにリクエストが行われたときに生成されます。

The ads are passed back to the user’s device and in parallel each ad and the associated features used in ranking that impression are added to the impression stream. 
広告はユーザーのデバイスに返され、並行して各広告とそのインプレッションのランキングに使用される関連機能がインプレッションストリームに追加されます。

If the user chooses to click the ad, that click will be added to the click stream. 
ユーザーが広告をクリックすることを選択した場合、そのクリックはクリックストリームに追加されます。

To achieve the stream-to-stream join the system utilizes a HashQueue consisting of a First-InFirst-Out queue as a buffer window and a hash map for fast random access to label impressions. 
ストリーム間結合を実現するために、システムはバッファウィンドウとしてのFIFOキューと、ラベルインプレッションへの高速ランダムアクセスのためのハッシュマップで構成されるHashQueueを利用します。

A HashQueue typically has three kinds of operations on key-value pairs: enqueue, dequeue and lookup. 
HashQueueは通常、キー-バリューペアに対して3種類の操作を持ちます：enqueue、dequeue、およびlookupです。

For example, to enqueue an item, we add the item to the front of a queue and create a key in the hash map with value pointing to the item of the queue. 
例えば、アイテムをenqueueするには、アイテムをキューの前に追加し、ハッシュマップにそのアイテムを指す値を持つキーを作成します。

Only after the full join window has expired will the labelled impression be emitted to the training stream. 
完全な結合ウィンドウが期限切れになった後にのみ、ラベル付けされたインプレッションがトレーニングストリームに出力されます。

If no click was joined, it will be emitted as a negatively labeled example. 
クリックが結合されなかった場合、それはネガティブラベルの例として出力されます。

In this experimental setup the trainer learns continuously from the training stream and publishes new models periodically to the Ranker. 
この実験設定では、トレーナーはトレーニングストリームから継続的に学習し、新しいモデルを定期的にランカーに公開します。

This ultimately forms a tight closed loop for the machine learning models where changes in feature distribution or model performance can be captured, learned on, and rectified in short succession. 
これにより、特徴分布やモデル性能の変化を短期間で捉え、学習し、修正できる機械学習モデルの厳密なクローズドループが形成されます。

One important consideration when experimenting with a real-time training data generating system is the need to build protection mechanisms against anomalies that could corrupt the online learning system. 
リアルタイムトレーニングデータ生成システムを実験する際の重要な考慮事項の一つは、オンライン学習システムを損なう可能性のある異常に対する保護メカニズムを構築する必要があることです。

Let us give a simple example. 
簡単な例を挙げましょう。

If the click stream becomes stale because of some data infrastructure issue, the online joiner will produce training data that has a very small or even zero empirical CTR. 
データインフラストラクチャの問題によりクリックストリームが古くなると、オンラインジョイナーは非常に小さいか、ゼロの実際のCTRを持つトレーニングデータを生成します。

As a consequence of this the real-time trainer will begin to incorrectly predict very low, or close to zero probabilities of click. 
この結果、リアルタイムトレーナーは非常に低い、またはゼロに近いクリックの確率を誤って予測し始めます。

The expected value of an ad will naturally depend on the estimated probability of click, and one consequence of incorrectly predicting very low CTR is that the system may show a reduced number of ad impressions. 
広告の期待値は自然にクリックの推定確率に依存し、非常に低いCTRを誤って予測することの一つの結果は、システムが広告インプレッションの数を減少させる可能性があることです。

Anomaly detection mechanisms can help here. 
異常検出メカニズムがここで役立ちます。

For example, one can automatically disconnect the online trainer from the online joiner if the real-time training data distribution changes abruptly. 
例えば、リアルタイムトレーニングデータの分布が急激に変化した場合、オンライントレーナーをオンラインジョイナーから自動的に切断することができます。



## 5. メモリとレイテンシの制御 5.1 ブースティングツリーの数

The more trees in the model the longer the time required to make a prediction. 
モデルにツリーが多いほど、予測に必要な時間が長くなります。
In this part, we study the effect of the number of boosted trees on estimation accuracy. 
この部分では、ブースティングツリーの数が推定精度に与える影響を調査します。

We vary the number of trees from 1 to 2,000 and train the models on one full day of data, and test the prediction performance on the next day. 
ツリーの数を1から2,000まで変化させ、1日のデータでモデルを訓練し、次の日に予測性能をテストします。
We constrain that no more than 12 leaves in each tree. 
各ツリーに12葉を超えないように制約を設けます。
Similar to previous experiments, we use normalized entropy as an evaluation metric. 
前回の実験と同様に、評価指標として正規化エントロピーを使用します。

The experimental results are shown in Figure 5. 
実験結果は図5に示されています。
Normalized entropy decreases as we increase the number of boosted trees. 
ブースティングツリーの数を増やすにつれて、正規化エントロピーは減少します。

However, the gain from adding trees yields diminishing return. 
しかし、ツリーを追加することによる利得は減少していきます。
Almost all NE improvement comes from the first 500 trees. 
正規化エントロピーの改善のほとんどは最初の500本のツリーから得られます。
The last 1,000 trees decrease NE by less than 0.1%. 
残りの1,000本のツリーは、正規化エントロピーを0.1%未満しか減少させません。

Moreover, we see that the normalized entropy for submodel 2 begins to regress after 1,000 trees. 
さらに、サブモデル2の正規化エントロピーは1,000本のツリーを超えると後退し始めます。
The reason for this phenomenon is overfitting. 
この現象の理由は過学習です。
Since the training data for submodel 2 is 4x smaller than that in submodel 0 and 1. 
サブモデル2の訓練データはサブモデル0および1のデータの4倍小さいためです。



## 5.2 特徴の重要性のブースティング

Feature count is another model characteristic that can influence trade-offs between estimation accuracy and computation performance. 
特徴の数は、推定精度と計算性能のトレードオフに影響を与える別のモデルの特性です。 

To better understand the effect of feature count we first apply a feature importance to each feature. 
特徴の数の影響をよりよく理解するために、まず各特徴に対して特徴の重要性を適用します。

In order to measure the importance of a feature we use the statistic Boosting Feature Importance, which aims to capture the cumulative loss reduction attributable to a feature. 
特徴の重要性を測定するために、私たちはBoosting Feature Importanceという統計量を使用します。これは、特徴に起因する累積損失の削減を捉えることを目的としています。

In each tree node construction, a best feature is selected and split to maximize the squared error reduction. 
各ツリーノードの構築において、最良の特徴が選択され、二乗誤差の削減を最大化するように分割されます。

Since a feature can be used in multiple trees, the (Boosting Feature Importance) for each feature is determined by summing the total reduction for a specific feature across all trees. 
特徴は複数の木で使用できるため、各特徴の（Boosting Feature Importance）は、すべての木にわたる特定の特徴の総削減を合計することによって決定されます。

Typically, a small number of features contributes the majority of explanatory power while the remaining features have only a marginal contribution. 
通常、少数の特徴が大部分の説明力に寄与し、残りの特徴はわずかな寄与しか持ちません。

We see this same pattern when plotting the number of features versus their cumulative feature importance in Figure 6. 
図6において、特徴の数とその累積特徴重要性をプロットすると、この同じパターンが見られます。

**Figure 6: Boosting feature importance. X-axis corresponds to number of features. We draw feature importance in log scale on the left-hand side primary y-axis, while the cumulative feature importance is shown with the right-hand side secondary y-axis.**  
**図6: ブースティング特徴の重要性。X軸は特徴の数に対応します。左側の主Y軸には対数スケールで特徴の重要性を描き、右側の副Y軸には累積特徴の重要性を示します。**

From the above result, we can see that the top 10 features are responsible for about half of the total feature importance, while the last 300 features contribute less than 1% feature importance. 
上記の結果から、上位10の特徴が総特徴重要性の約半分を占めているのに対し、最後の300の特徴は1%未満の特徴重要性に寄与していることがわかります。

Based on this finding, we further experiment with only keeping the top 10, 20, 50, 100 and 200 features, and evaluate how the performance is effected. 
この発見に基づいて、上位10、20、50、100、200の特徴のみを保持する実験をさらに行い、パフォーマンスにどのように影響するかを評価します。

The result of the experiment is shown in Figure 7. 
実験の結果は図7に示されています。

From the figure, we can see that the normalized entropy has similar diminishing return property as we include more features. 
図から、正規化エントロピーがより多くの特徴を含めるにつれて、類似の収益逓減特性を持つことがわかります。

In the following, we will do some study on the usefulness of historical and contextual features. 
次に、歴史的および文脈的特徴の有用性についていくつかの研究を行います。

Due to the data sensitivity in nature and the company policy, we are not able to reveal the detail on the actual features we use. 
データの性質上の敏感さと会社の方針により、私たちが使用する実際の特徴の詳細を明らかにすることはできません。

Some example contextual features can be local time of day, day of week, etc. 
いくつかの例として、文脈的特徴には、日中のローカル時間、曜日などがあります。

Historical features can be the cumulative number of clicks on an ad, etc. 
歴史的特徴には、広告の累積クリック数などがあります。



## 5.3 歴史的特徴

The features used in the Boosting model can be categorized into two types: contextual features and historical features.  
Boostingモデルで使用される特徴は、文脈特徴と歴史的特徴の2種類に分類できます。

The value of contextual features depends exclusively on current information regarding the context in which an ad is to be shown, such as the device used by the users or the current page that the user is on.  
文脈特徴の値は、ユーザが使用しているデバイスやユーザが現在いるページなど、広告が表示される文脈に関する現在の情報のみに依存します。

On the contrary, the historical features depend on previous interaction for the ad or user, for example the click through rate of the ad in last week, or the average click through rate of the user.  
対照的に、歴史的特徴は広告やユーザの以前のインタラクションに依存します。例えば、先週の広告のクリック率やユーザの平均クリック率などです。

**Figure 7: Results for Boosting model with top features. We draw calibration on the left-hand side primary y-axis, while the normalized entropy is shown with the right-hand side secondary y-axis.**  
**図7: トップ特徴を用いたBoostingモデルの結果。左側の主y軸にキャリブレーションを描き、右側の副y軸には正規化エントロピーが示されています。**

In this part, we study how the performance of the system depends on the two types of features.  
この部分では、システムのパフォーマンスが2種類の特徴にどのように依存するかを調査します。

Firstly we check the relative importance of the two types of features.  
まず、2種類の特徴の相対的重要性を確認します。

We do so by sorting all features by importance, then calculate the percentage of historical features in first k-important features.  
すべての特徴を重要性でソートし、最初のk個の重要な特徴における歴史的特徴の割合を計算します。

The result is shown in Figure 8.  
その結果は図8に示されています。

From the result, we can see that historical features provide considerably more explanatory power than contextual features.  
結果から、歴史的特徴が文脈特徴よりもかなり多くの説明力を提供することがわかります。

The top 10 features ordered by importance are all historical features.  
重要性で並べた上位10の特徴はすべて歴史的特徴です。

Among the top 20 features, there are only 2 contextual features despite historical feature occupying roughly 75% of the features in this dataset.  
上位20の特徴の中で、歴史的特徴がこのデータセットの約75%を占めているにもかかわらず、文脈特徴はわずか2つしかありません。

To better understand the comparative value of the features from each type in aggregate we train two Boosting models with only contextual features and only historical features, then compare the two models with the complete model with all features.  
各タイプの特徴の比較価値をよりよく理解するために、文脈特徴のみと歴史的特徴のみを用いた2つのBoostingモデルを訓練し、次にすべての特徴を含む完全モデルと2つのモデルを比較します。

The result is shown in Table 4.  
その結果は表4に示されています。

From the table, we can again verify that in aggregate historical features play a larger role than contextual features.  
表から、歴史的特徴が文脈特徴よりも全体として大きな役割を果たすことを再確認できます。

-----
**Table 4: Boosting model with different types of features**  
**表4: 異なるタイプの特徴を用いたBoostingモデル**

Type of features NE (relative to Contextual)  
特徴のタイプ NE（文脈に対して）

All 95.65%  
すべて 95.65%

Historical 96.32%  
歴史的 96.32%

Contextual 100% (reference)  
文脈 100%（基準）

Without only contextual features, we measure 4.5% loss in prediction accuracy.  
文脈特徴のみを除くと、予測精度が4.5%低下します。

On the contrary, without contextual features, we suffer less than 1% loss in prediction accuracy.  
対照的に、文脈特徴を除くと、予測精度の低下は1%未満です。

It should be noticed that contextual features are very important to handle the cold start problem.  
文脈特徴はコールドスタート問題を扱うために非常に重要であることに注意すべきです。

For new users and ads, contextual features are indispensable for a reasonable click through rate prediction.  
新しいユーザや広告にとって、文脈特徴は合理的なクリック率予測に不可欠です。

In next step, we evaluate the trained models with only historical features or contextual features on the consecutive weeks to test the feature dependency on data freshness.  
次のステップでは、連続した週にわたって歴史的特徴または文脈特徴のみを用いた訓練モデルを評価し、データの新鮮さに対する特徴の依存性をテストします。

The result is shown in Figure 9.  
その結果は図9に示されています。

**Figure 9: Results for data freshness for different type of features. X-axis is the evaluation date while y-axis is the normalized entropy.**  
**図9: 異なるタイプの特徴に対するデータの新鮮さの結果。X軸は評価日、Y軸は正規化エントロピーです。**

From the figure, we can see that the model with contextual features relies more heavily on data freshness than historical features.  
図から、文脈特徴を持つモデルが歴史的特徴よりもデータの新鮮さにより依存していることがわかります。

It is in line with our intuition, since historical features describe long-time accumulated user behaviour, which is much more stable than contextual features.  
これは私たちの直感に合致しており、歴史的特徴は長期間にわたって蓄積されたユーザの行動を記述するため、文脈特徴よりもはるかに安定しています。



## 6. 大規模なトレーニングデータへの対処

A full day of Facebook ads impression data can contain a huge amount of instances. 
1日のFacebook広告インプレッションデータは、膨大な数のインスタンスを含む可能性があります。

Note that we are not able to reveal the actual number as it is confidential. 
実際の数は機密情報であるため、明らかにすることはできません。

But a small fraction of a day’s worth of data can have many hundreds of millions of instances. 
しかし、1日のデータのごく一部でも、数億のインスタンスを持つことがあります。

A common technique used to control the cost of training is reducing the volume of training data. 
トレーニングコストを抑えるために一般的に使用される手法は、トレーニングデータの量を減らすことです。

In this section we evaluate two techniques for down sampling data, uniform subsampling and negative down sampling. 
このセクションでは、データのダウンサンプリングのための2つの手法、均一サブサンプリングとネガティブダウンサンプリングを評価します。

In each case we train a set of boosted tree models with 600 trees and evaluate these using both calibration and normalized entropy. 
各ケースで、600本の木を持つブーステッドツリーモデルのセットをトレーニングし、キャリブレーションと正規化エントロピーの両方を使用して評価します。



## 6.1 Uniform subsampling 一様サブサンプリング

Uniform subsampling of training rows is a tempting approach for reducing data volume because it is both easy to implement and the resulting model can be used without modification on both the subsampled training data and non-subsampled test data. 
トレーニング行の一様サブサンプリングは、データ量を削減するための魅力的なアプローチです。なぜなら、実装が簡単であり、得られたモデルはサブサンプリングされたトレーニングデータと非サブサンプリングのテストデータの両方で修正なしに使用できるからです。
In this part, we evaluate a set of roughly exponentially increasing subsampling rates. 
この部分では、ほぼ指数関数的に増加するサブサンプリング率のセットを評価します。
For each rate we train a boosted tree model sampled at that rate from the base dataset. 
各サンプリング率に対して、その率でベースデータセットからサンプリングされたブーステッドツリーモデルをトレーニングします。
We vary the subsampling rate in {0.001, 0.01, 0.1, 0.5, 1}. 
サブサンプリング率は{0.001, 0.01, 0.1, 0.5, 1}の範囲で変化させます。
The result for data volume is shown in Figure 10. 
データ量の結果は図10に示されています。
It is in **Figure 10: Experiment result for data volume. The** **X-axis corresponds to number of training instances.** **We draw calibration on the left-hand side primary** **y-axis, while the normalized entropy is shown with** **the right-hand side secondary y-axis.**
これは**図10: データ量に関する実験結果。X軸はトレーニングインスタンスの数に対応します。** **左側の主y軸にはキャリブレーションを描き、右側の副y軸には正規化エントロピーが示されています。**
line with our intuition that more data leads to better performance. 
これは、より多くのデータがより良いパフォーマンスにつながるという私たちの直感に沿った結果です。
Moreover, the data volume demonstrates diminishing return in terms of prediction accuracy. 
さらに、データ量は予測精度に関して収穫逓減を示しています。
By using only 10% of the data, the normalized entropy is only a 1% reduction in performance relative to the entire training data set. 
データの10%のみを使用することで、正規化エントロピーは全体のトレーニングデータセットに対してパフォーマンスがわずか1%減少するだけです。
The calibration at this sampling rate shows no performance reduction. 
このサンプリング率でのキャリブレーションは、パフォーマンスの低下を示しません。



## 6.2 Negative down sampling ネガティブダウンサンプリング

Class imbalance has been studied by many researchers and has been shown to have significant impact on the performance of the learned model. 
クラスの不均衡は多くの研究者によって研究されており、学習したモデルの性能に大きな影響を与えることが示されています。
In this part, we investigate the use of negative down sampling to solve the class imbalance problem. 
この部分では、クラスの不均衡問題を解決するためにネガティブダウンサンプリングの使用を調査します。
We empirically experiment with different negative down sampling rate to test the prediction accuracy of the learned model. 
異なるネガティブダウンサンプリングレートで実験を行い、学習したモデルの予測精度をテストします。
We vary the rate in {0.1, 0.01, 0.001, 0.0001}. 
レートは{0.1, 0.01, 0.001, 0.0001}の範囲で変化させます。
The experiment result is shown in Figure 11. 
実験結果は図11に示されています。
From the result, we can see that the negative down sampling rate has significant effect on the performance of the trained model. 
結果から、ネガティブダウンサンプリングレートが訓練されたモデルの性能に大きな影響を与えることがわかります。
The best performance is achieved with negative down sampling rate set to 0.025. 
最良の性能は、ネガティブダウンサンプリングレートを0.025に設定したときに達成されます。



## 6.3 モデルの再キャリブレーション

Negative downsampling can speed up training and improve model performance. 
ネガティブダウンサンプリングは、トレーニングを加速し、モデルのパフォーマンスを向上させることができます。 
Note that, if a model is trained in a data set with negative downsampling, it also calibrates the prediction in the downsampling space. 
注意すべきは、ネガティブダウンサンプリングを用いてデータセットでトレーニングされたモデルは、ダウンサンプリング空間での予測もキャリブレーションするということです。 
For example, if the average CTR before sampling is 0.1% and we do a 0.01 negative downsampling, the empirical CTR will become roughly 10%. 
例えば、サンプリング前の平均CTRが0.1%で、0.01のネガティブダウンサンプリングを行うと、経験的CTRはおおよそ10%になります。 
We need to re-calibrate the model for live traffic experiment and get back to the 0.1% prediction with $q = p + \frac{(1 - p)p}{w}$ 
私たちは、ライブトラフィック実験のためにモデルを再キャリブレーションし、$q = p + \frac{(1 - p)p}{w}$を用いて0.1%の予測に戻す必要があります。 
where p is the prediction in downsampling space and w the negative downsampling rate. 
ここで、$p$はダウンサンプリング空間での予測、$w$はネガティブダウンサンプリング率です。



## 7. DISCUSSION 議論

We have presented some practical lessons from experimenting with Facebook ads data. 
私たちは、Facebook広告データを使った実験から得られた実践的な教訓をいくつか提示しました。 
This has inspired a promising hybrid model architecture for click prediction.
これにより、クリック予測のための有望なハイブリッドモデルアーキテクチャが生まれました。

_• Data freshness matters. It is worth retraining at least_ daily. 
_• データの新鮮さは重要です。少なくとも毎日再訓練する価値があります。_ 
In this paper we have gone further and discussed various online learning schemes. 
本論文ではさらに進んで、さまざまなオンライン学習スキームについて議論しました。 
We also presented infrastructure that allows generating real-time training data.
また、リアルタイムのトレーニングデータを生成するためのインフラストラクチャも提示しました。

_• Transforming real-valued input features with boosted_ decision trees significantly increases the prediction accuracy of probabilistic linear classifiers. 
_• ブーストされた決定木を用いて実数値の入力特徴を変換することは、確率的線形分類器の予測精度を大幅に向上させます。_ 
This motivates a hybrid model architecture that concatenates boosted decision trees and a sparse linear classifier.
これにより、ブーストされた決定木とスパース線形分類器を連結するハイブリッドモデルアーキテクチャが動機づけられます。

_• Best online learning method: LR with per-coordinate_ learning rate, which ends up being comparable in performance with BOPR, and performs better than all other LR SGD schemes under study. 
_• 最良のオンライン学習方法：座標ごとの学習率を持つLRで、これはBOPRと性能が同等であり、研究対象の他のすべてのLR SGDスキームよりも優れた性能を発揮します。_ 
(Table 4, Fig 12)
（表4、図12）

We have described tricks to keep memory and latency contained in massive scale machine learning applications.
私たちは、大規模な機械学習アプリケーションにおいてメモリとレイテンシを抑えるためのトリックを説明しました。

_• We have presented the tradeoff between the number of_ boosted decision trees and accuracy. 
_• ブーストされた決定木の数と精度のトレードオフを提示しました。_ 
It is advantageous to keep the number of trees small to keep computation and memory contained.
計算とメモリを抑えるためには、木の数を少なく保つことが有利です。

_• Boosted decision trees give a convenient way of doing_ feature selection by means of feature importance. 
_• ブーストされた決定木は、特徴の重要性を用いて特徴選択を行う便利な方法を提供します。_ 
One can aggressively reduce the number of active features whilst only moderately hurting prediction accuracy.
アクティブな特徴の数を積極的に減らすことができ、予測精度に対しては中程度の影響しか与えません。

_• We have analyzed the effect of using historical fea-_ tures in combination with context features. 
_• 歴史的特徴をコンテキスト特徴と組み合わせて使用する効果を分析しました。_ 
For ads and users with history, these features provide superior predictive performance than context features.
広告や履歴のあるユーザーにとって、これらの特徴はコンテキスト特徴よりも優れた予測性能を提供します。

Finally, we have discussed ways of subsampling the training data, both uniformly but also more interestingly in a biased way where only the negative examples are subsampled.
最後に、トレーニングデータを均等にサンプリングする方法と、より興味深く、負の例のみをサンプリングするバイアスのかかった方法について議論しました。



## 8. REFERENCES 参考文献

[1] R. Ananthanarayanan, V. Basker, S. Das, A. Gupta, H. Jiang, T. Qiu, A. Reznichenko, D. Ryabkov, M. Singh, and S. Venkataraman. Photon: Fault-tolerant and scalable joining of continuous data streams. In SIGMOD, 2013.  
[1] R. Ananthanarayanan, V. Basker, S. Das, A. Gupta, H. Jiang, T. Qiu, A. Reznichenko, D. Ryabkov, M. Singh、および S. Venkataraman. Photon: 障害耐性がありスケーラブルな連続データストリームの結合. SIGMODにおいて, 2013年.

[2] L. Bottou. Online algorithms and stochastic approximations. In D. Saad, editor, Online Learning _and Neural Networks. Cambridge University Press,_ Cambridge, UK, 1998. revised, oct 2012.  
[2] L. Bottou. オンラインアルゴリズムと確率的近似. D. Saad編, Online Learning _and Neural Networks. Cambridge University Press,_ ケンブリッジ, 英国, 1998年. 改訂版, 2012年10月.

[3] O. Chapelle and L. Li. An empirical evaluation of thompson sampling. In Advances in Neural _Information Processing Systems, volume 24, 2012._  
[3] O. Chapelle と L. Li. トンプソンサンプリングの実証評価. Advances in Neural _Information Processing Systems, 第24巻, 2012年._

[4] B. Edelman, M. Ostrovsky, and M. Schwarz. Internet advertising and the generalized second price auction: Selling billions of dollars worth of keywords. In _American Economic Review, volume 97, pages_ 242–259, 2007.  
[4] B. Edelman, M. Ostrovsky, および M. Schwarz. インターネット広告と一般化されたセカンドプライスオークション: 数十億ドル相当のキーワードの販売. _American Economic Review, 第97巻, ページ_ 242–259, 2007年.

[5] J. H. Friedman. Greedy function approximation: A gradient boosting machine. Annals of Statistics, 29:1189–1232, 1999.  
[5] J. H. Friedman. 貪欲な関数近似: 勾配ブースティングマシン. Annals of Statistics, 29:1189–1232, 1999年.

[6] L. Golab and M. T. Ozsu. Processing sliding window[¨] multi-joins in continuous queries over data streams. In _VLDB, pages 500–511, 2003._  
[6] L. Golab と M. T. Ozsu. データストリーム上の連続クエリにおけるスライディングウィンドウ[¨]マルチジョインの処理. _VLDB, ページ 500–511, 2003年._

[7] T. Graepel, J. Qui˜nonero Candela, T. Borchert, and R. Herbrich. Web-scale bayesian click-through rate prediction for sponsored search advertising in Microsoft’s Bing search engine. In ICML, pages 13–20, 2010.  
[7] T. Graepel, J. Qui˜nonero Candela, T. Borchert, および R. Herbrich. MicrosoftのBing検索エンジンにおけるスポンサー検索広告のためのウェブスケールベイズ的クリック率予測. ICMLにおいて, ページ 13–20, 2010年.

[8] H. B. McMahan, G. Holt, D. Sculley, M. Young, D. Ebner, J. Grady, L. Nie, T. Phillips, E. Davydov, D. Golovin, S. Chikkerur, D. Liu, M. Wattenberg, A. M. Hrafnkelsson, T. Boulos, and J. Kubica. Ad click prediction: a view from the trenches. In KDD, 2013.  
[8] H. B. McMahan, G. Holt, D. Sculley, M. Young, D. Ebner, J. Grady, L. Nie, T. Phillips, E. Davydov, D. Golovin, S. Chikkerur, D. Liu, M. Wattenberg, A. M. Hrafnkelsson, T. Boulos, および J. Kubica. 広告クリック予測: 現場からの視点. KDDにおいて, 2013年.

[9] M. Richardson, E. Dominowska, and R. Ragno. Predicting clicks: Estimating the click-through rate for new ads. In WWW, pages 521–530, 2007.  
[9] M. Richardson, E. Dominowska, および R. Ragno. クリック予測: 新しい広告のクリック率の推定. WWWにおいて, ページ 521–530, 2007年.

[10] A. Thusoo, S. Antony, N. Jain, R. Murthy, Z. Shao, D. Borthakur, J. Sarma, and H. Liu. Data warehousing and analytics infrastructure at facebook. In SIGMOD, pages 1013–1020, 2010.  
[10] A. Thusoo, S. Antony, N. Jain, R. Murthy, Z. Shao, D. Borthakur, J. Sarma, および H. Liu. Facebookにおけるデータウェアハウジングと分析インフラストラクチャ. SIGMODにおいて, ページ 1013–1020, 2010年.

[11] H. R. Varian. Position auctions. In International _Journal of Industrial Organization, volume 25, pages_ 1163–1178, 2007.  
[11] H. R. Varian. ポジションオークション. International _Journal of Industrial Organization, 第25巻, ページ_ 1163–1178, 2007年.

[12] J. Yi, Y. Chen, J. Li, S. Sett, and T. W. Yan. Predictive model performance: Offline and online evaluations. In KDD, pages 1294–1302, 2013.  
[12] J. Yi, Y. Chen, J. Li, S. Sett, および T. W. Yan. 予測モデルの性能: オフラインおよびオンライン評価. KDDにおいて, ページ 1294–1302, 2013年.  
