## 0.1. link

[pdf](https://dl.acm.org/doi/pdf/10.1145/3298689.3347018)

## 0.2. title

Uplift-based Evaluation and Optimization of Recommenders

## 0.3. abstruct

Recommender systems aim to increase user actions such as clicks and purchases.
Typical evaluations of recommenders regard the purchase of a recommended item as a success. However, the item may have been purchased even without the recommendation.
An uplift is defned as an increase in user actions caused by recommendations.
Situations with and without a recommendation cannot both be observed for a specifc user-item pair at a given time instance, making uplift-based evaluation and optimization challenging.
レコメンダーシステムは、クリックや購入といったユーザーのアクションを増やすことを目的としている.
一般的なレコメンダー評価では、推薦された商品を購入することが成功であるとされる.
しかし、レコメンドがなくても購入された可能性がある。レコメンドによるユーザーアクションの増加をアップリフトと定義している.
しかし，ある時点のあるユーザとアイテムのペアに対して，推薦がある場合とない場合の両方の状況を観測することは不可能であり，アップリフトに基づく評価と最適化は困難である．

This paper proposes new evaluation metrics and optimization methods for the uplift in a recommender system.
本論文では、推薦システムにおけるアップリフトの新しい評価指標と最適化手法を提案する.
We apply a causal inference framework to estimate the average uplift for the ofine evaluation of recommenders.
我々は因果推論の枠組みを適用し，レコメンダーシステムを評価するための平均的な高揚度を推定する．
Our evaluation protocol leverages both purchase and recommendation logs under a currently deployed recommender system, to simulate the cases both with and without recommendations.
本論文では，レコメンダーシステムにおける購買履歴と推薦履歴の両方を用いて，推薦がある場合とない場合のシミュレーションを行う．
This enables the ofine evaluation of the uplift for newly generated recommendation lists.
これにより，新たに生成された推薦リストの高揚度を正当に評価することができる．
For optimization, we need to defne positive and negative samples that are specifc to an uplift-based approach.
最適化のためには、アップリフトベースアプローチに特化したポジティブサンプルとネガティブサンプルを定義する必要がある.
For this purpose, we deduce four classes of items by observing purchase and recommendation logs.
そのために、購買履歴と推薦履歴から4つの分類を導き出す.
We derive the relative priorities among these four classes in terms of the uplift and use them to construct both pointwise and pairwise sampling methods for uplift optimization.
そして，これら4つのクラス間の相対的な優先順位を高揚度の観点から導き出し，それを用いて高揚度最適化のためのポイントワイズサンプリングとペアワイズサンプリングの手法を構築する．
Through dedicated experiments with three public datasets, we demonstrate the efectiveness of our optimization methods in improving the uplift.
また，3つの公共データセットを用いた実験により，我々の最適化手法がアップリフトの改善に有効であることを実証する．

# 1. introduction

One of the major goals of recommender systems is to induce positive user interactions, such as clicks and purchases. Because increases in user interactions directly beneft businesses, recommender systems have been utilized in various domains of industry. Recommendations are typically evaluated in terms of purchases1 of recommended items. However, these items may have been purchased even without recommendations. For a certain e-commerce site, more than 75% of the recommended items that were clicked would have been clicked even without the recommendations [42]. We argue that the true success of recommendations is represented by the increase in user actions caused by recommendations. Such an increase afected purely by recommendations is called an uplift. The development of a recommender should focus more on the uplift than the accurate prediction of user purchases. However, evaluating and optimizing the uplift is difcult, owing to its unobservable nature. An item is either recommended or not for a specifc user at a given time instance, so the uplift cannot be directly measured for a given recommendation. This means that there is no ground truth for training and evaluating a model. Previous studies targeting uplift construct purchase prediction models incorporating recommendation efects [2, 40]. The items recommended are ones that have the largest diferences between the predicted purchase probabilities for cases with and without recommendations. Another approach builds two prediction models: one for predictions with recommendations and the other for predictions with no recommendations [3]. All of these methods are based on purchase prediction models optimized for prediction accuracy, even though they target uplift. We expect an improvement in uplift performance by optimizing models directly for the uplift. In this study, we propose new evaluation methods and optimization methods for uplift-based recommendation. First, we show that common accuracy-based evaluation metrics such as precision do not align with the uplift. Then, we derive evaluation protocols to estimate the average uplift for recommendations, based on a potential outcome framework in causal inference [15, 28, 37]. Furthermore, we propose optimization methods for recommenders, to improve the uplift. We apply these methods to a matrix factorization model [14, 32, 35], which is the most common model for recommenders. To verify the efectiveness of the proposed optimization methods, we compare the uplift performance of our methods with baselines, including recent recommenders [3, 40] that target the uplift. We further investigate the characteristics of our uplift-based optimizations and the recommendation outputs.
レコメンダーシステムの主要な目的の一つは、クリックや購入といったポジティブなユーザーインタラクションを誘発することである.
ユーザーとのインタラクションが増えることは、ビジネスに直結するため、レコメンダーシステムは様々な産業領域で活用されている.
レコメンデーションは、通常、推奨された商品の購入1という形で評価される.
しかし、**レコメンドされなくても購入されている可能性**がある.
ある EC サイトでは，クリックされたレコメンド商品の 75% 以上はレコメンドがなくてもクリックされていたであろうという結果が出ている[42]．
レコメンデーションの真の成功は，レコメンデーションによっ て引き起こされるユーザの行動の増加によって表されると我々は主張する．
このように、レコメンデーションによって純粋に影響される増加を **Uplift** と呼ぶ.
レコメンダーの開発では、ユーザの購買行動を正確に予測することよりも、アップリフトに重点を置くべきである.
しかし、**アップリフトの評価と最適化は、その観測不可能な性質により困難**である.
あるアイテムはある時点で特定のユーザに推薦されるか否かであり、推薦されたアイテムに対するUpliftを直接測定することはできない.
つまり、**モデルを学習・評価するための ground truth が存在しない**のである.
このため，レコメンデーションの効果を利用した購買予測モデルを構築する．
レコメンデーションがある場合とない場合の予測購入確率の差 が最も大きいものを推奨品目とする．
また，レコメンデーションがある場合の予測モデルと，レコメンデーションがない場合の予測モデルの2つを構築するアプローチもある[3]．
これらの方法はすべて、アップリフトを対象としているにもかかわらず、予測精度に最適化された購入予測モデルに基づいている.
**モデルを直接 Uplift に基づき最適化することで，Uplift性能の向上が期待される**．

本研究では，アップリフトに基づく推薦のための新たな評価手法と最適化手法を提案する．
まず，**精度などの一般的な精度ベースの評価指標はアップリフトと整合していないことを示す**．
そして，因果推論[15, 28, 37]における潜在的な結果の枠組みに基づき，レコメンデーションの平均的なアップリフトを推定する評価プロトコルを導出する．さらに、レコメンダーの最適化手法を提案し、アップリフトを向上させる。これらの手法を、レコメンダーの最も一般的なモデルである行列分解モデル[14, 32, 35]に適用する。提案する最適化手法の有効性を検証するため，提案手法のアップリフト性能を，アップリフトを目標とした最近のレコメンダー[3, 40]を含むベースラインと比較する．さらに，提案するアップリフトに基づく最適化手法と推薦出力の特徴について検討する．

The contributions of this paper are summarized as follows.

- We propose ofine evaluation metrics for the recommendation uplift (Section 2).
- We present both pointwise and pairwise optimization methods for uplift-based recommendation (Section 3).
- We demonstrate the efectiveness of our optimization methods through comparisons with baselines (Subsection 5.2).
- We clarify the characteristics of the optimization (Subsection 5.3) and the recommendation outputs (Subsection 5.4).

# 2. Uplift-Based Evaluation

Recommenders are typically evaluated in terms of recommendation accuracy. A recommender is considered to be better than others if a larger number of its recommended items are purchased. We refer to this evaluation approach as **accuracy-based evaluation**. Precision, which is a commonly utilized accuracy metric for recommenders, is defned as the number of purchases divided by the number of recommendations. However, items may have been bought even without recommendations if the user was already aware of and had a preference for those items. Thus, we aim to evaluate recommenders in terms of the uplift they achieve.
レコメンダーは通常、推薦精度の観点から評価される。レコメンダーは、推薦した商品がより多く購入されれば、他のレコメンダーより優れているとみなされる。この評価手法を精度評価と呼ぶ。レコメンダーの精度の指標としてよく使われる「精度」は、「購入数÷推奨数」で定義される。しかし、推薦がなくても、ユーザーがその商品を認知し、嗜好していれば、購入される可能性がある。このように、リコメンダーは「高揚度」という観点で評価されることを目指します。

## 2.1. Discrepancy between Accuracy and Uplift

In this subsection, we demonstrate that accuracy metrics such as precision are unsuitable for the goal of increasing user purchases.
To describe two cases with and without a recommendation, we adopt the concept of potential outcome from causal inference [15, 28, 37]. Let $Y^T \in {0, 1}$ be the potential outcome with a recommendation (treatment condition) and $Y^C \in {0, 1}$ be the potential outcome without a recommendation (control condition)2. $Y^T= 1$ and $Y^C= 1$ indicate that an item3 will be purchased when recommended and not recommended, respectively. The uplift $\tau$ of an item for a given user4 is $Y^T - Y^C$ . Considering the two possible actions of a user in the two given scenarios, there are four item classes for the user:
このサブセクションでは，精度のような正確さの指標は， ユーザーの購買意欲を高めるという目的には適さないことを 示している．推薦がある場合とない場合の2つのケースを説明するた めに，因果推論[15, 28, 37]の潜在的な結果の概念を採用す る．Y^T=1$, $Y^C=1$ は，それぞれ推奨されたときとされな いときにアイテム3 が購入されることを示す．あるユーザ4に対する商品の高揚度$Y^T - Y^C$ は、$Y^T - Y^C$ である。与えられた2つのシナリオにおけるユーザの2つの行動を考慮すると、ユーザにとって4つのアイテムクラスが存在することになる。

- True Uplift (TU). $Y^T= 1$ and $Y^C = 0$, hence $\tau = 1$. The item will be purchased if recommended, but will not be purchased if not recommended.
- False Uplift (FU). $Y^T= Y^C = 1$, hence $\tau= 0$. The item will be purchased regardless of whether it is recommended.
- True Drop (TD). $Y^T= 0$ and $Y^C = 1$, hence $\tau = −1$. The item will be purchased if it is not recommended, but will not be purchased if it is recommended.
- False Drop (FD). $Y^T = Y^C = 0$, hence $\tau= 0$. The item will not be purchased regardless of whether it is recommended.

To intuitively illustrate the diference between the uplift and accuracy in an ofine evaluation setting, we consider four lists of ten recommendations, as shown in Fig. 1. We assume that we have an offline dataset, which includes both purchase logs and recommendation logs for a currently deployed recommender. Note that TU items are only purchased if recommended, and TD items are only purchased if not recommended. Purchases of other FU and FD items do not depend on recommendations. The total uplift that would have been obtained if all the ten items were recommended in the past is shown in Table 1. We also list precision under two settings: one with all items on the list, and the other with only the items recommended in the logs. The former is a common setting for the ofine evaluations of recommenders [9]. The latter is a setting employed in the previous work [7, 25] to estimate the online performance of a recommender. The former precision value and total uplift exhibit opposite trends for these samples. This means that the best model for achieving a higher uplift cannot be selected based on this former precision. Excluding items without recommendations does not resolve this issue. The latter precision value, calculated using only the recommended items (items with solid boundaries in Fig. 1), exhibits the same value for all lists, and is still unable to select the best model.

As demonstrated by the above illustration, accuracy-based evaluation is not suitable for evaluating the uplift caused by recommenders. We need to employ an evaluation metric designed for uplift-based evaluation. However, we cannot directly calculate the total uplift, because we only observe either $Y^T$ or $Y^C$ for a user-item pair at a given time. To overcome this difculty, we apply a causal inference framework to estimate the average treatment efect.

## 2.2. Causal Inference Framework

In this subsection, we introduce the causal inference framework [15, 28, 37], which we apply to the uplift-based evaluation of recommenders in the next subsection. The treatment efect τ for a subject is defned as the diference between the potential outcomes with and without treatment: $\tau \equiv Y^T - Y^C$ .
Note that $\tau$ is not directly measurable, because each subject is either treated or not, and either $Y^T$ or $Y^C$ is observed. However, we can estimate the average treatment efect (ATE), which is expressed as $E[\tau] = E[Y^T] − E[Y^C]$.
このサブセクションでは、因果推論フレームワーク [15, 28, 37] を紹介し、次のサブセクションでレコメンダーのアップリフトベース評価に適用する。ある被験者の治療効果τは、治療の有無による潜在的な結果の差とし て定義される： $tau \equiv Y^T - Y^C$ 。
ただし、被験者が治療を受けるか受けないか、$Y^T$か$Y^C$のどちらかが観測されるため、$Θtau$は直接測定できないことに注意。しかし、平均治療効果（ATE）を推定することができ、これは $E[\tau] = E[Y^T] - E[Y^C]$ で表される。

Let $Z \in {0, 1}$ be the binary indicator for the treatment, with $Z = 1$ and $Z = 0$ indicating that the subject does and does not receive treatment, respectively.
The covariates associated with the subject are denoted by $X$, e.g., demographic and past records of the subject before treatment assignment. Consider $N$ subjects, indexed by $n$. We use $S^T$ and $S^C$ to denote the sets of subjects who do and do not receive treatment, respectively. Naively, the ATE can be estimated as the diference between the average outcomes of the two sets;
ここで、$Zは治療の二値指標とし、$Z = 1$は治療を受けたことを、$Z = 0$は治療を受けなかったことをそれぞれ示すものとする。被験者に関連する共変量は$X$で表し、例えば、治療割り当て前の被験者の人口統計学的記録と過去の記録である。n$を指標とし、$N$人の被験者を考える。ここで、$S^T$と$S^C$を、それぞれ治療を受ける被験者と受けない被験者の集合を表すのに用いる。直観的には、ATEは2つの集合の平均結果の差として推定できる。

$$
\hat{\tau} = \frac{1}{|S_T|} \sum_{n \in S_T} Y_n^T - \frac{1}{|S_C|} \sum_{n \in S_C} Y_n^C
\tag{1}
$$

If treatment is randomly assigned to subjects independent of the potential outcomes, i.e., $(Y^T ,Y^C)⊥Z$, then $\hat{\tau}$ converges to the ATE almost surely when $N \rightarrow \infty$ (see the proof of [31, Theorem 9.2]).

Because the independence condition $(Y^T,Y^C)⊥Z$ is a strong assumption, we instead consider conditional independence $(Y^T, Y^C) ⊥Z|X$, which means that the covariates X contain all confounders of $(Y^T,Y^C)$ and $Z$ [28]. Under the conditional independence, the inverse propensity scoring (IPS) estimator,

$$
\hat{\tau}_{IPS} = \frac{1}{N} \sum_{n \in S_T} \frac{Y_n^T}{e(X_n)} - \frac{1}{N} \sum_{n \in S_C} \frac{Y_n^C}{1 - e(X_n)}
\tag{2}
$$

is known to be an unbiased estimator of the ATE. Here, $e(X_n) = p(Z_n = 1|X_n)$ is the probability of treatment assignment conditioned on the covariates X, which is called the propensity score [36]. However, the IPS is prone to sufer from high variance of estimates, because a small propensity score leads to a large weight on an outcome for a certain subject. To remedy this, self-normalized inverse propensity scoring (SNIPS) has been proposed[45]. This adjusts the estimates by the sum of the inverse propensity scores:

$$
\hat{\tau}_{SNIPS} = \frac{
    \sum_{n\in S_T} \frac{Y_n^T}{e(X_n)}
}{
    \sum_{n\in S_T} \frac{1}{e(X_n)}
}
- \frac{
    \sum_{n\in S_C} \frac{Y_n^C}{e(X_n)}
}{
    \sum_{n\in S_C} \frac{1}{e(X_n)}
}
\tag{3}
$$

Under the independence condition $(Y^T,Y^C )⊥Z|X$, the estimator $\hat{\tau}_{SNIPS}$ converges to the ATE almost surely when $N \rightarrow \infty$.

## 2.3. Uplift Estimates for Recommenders

In this subsection, we design evaluation protocols for the uplift caused by recommendation, based on the causal inference framework described in the previous subsection. The goal is to evaluate the uplift performance of a new recommender model M. We assume that we have an offline dataset comprising purchase and recommendation logs under a currently deployed model D. For the uplift evaluation of recommenders, a treatment Z is a recommendation by D, and $Y^T_{ui} = 1$ means that a user u purchases an item i when it is recommended. Let R be a binary variable such that $R = 1$ if M recommends the item. We want to evaluate $E[\tau] = E[Y^T − Y^C|R = 1]$. Let defne $p = E[Y^T|R = 1]$ and $p = E[Y^C|R = 1]$, purchase probabilities of items selected by M with and without an actual recommendation by D, respectively. The uplift can then be interpreted as the increase in purchase probability caused by the recommendaC tion: $p^T − p^C$.
本節では，前節で述べた因果推論の枠組みをもとに，レコメンデーションによるアップリフトの評価プロトコルを設計する．目標は新しいレコメンダーモデルMのアップリフト性能を評価することである。現在導入されているモデルDの下での購入と推薦ログからなるアインデータセットがあるとする。レコメンダーのアップリフト評価では、処理ZはDによる推薦であり、$Y^T_{ui} = 1$はユーザーuが商品iを推薦されたときに購入することを意味する。Rは、Mがアイテムを推奨した場合に$R = 1$となるような2値変数とする。E[\tau] = E[Y^T - Y^C|R = 1]$を評価したい。ここで、$p = E[Y^T|R = 1]$、$p = E[Y^C|R = 1]$を、Dによる実際の推薦がある場合とない場合のMが選んだアイテムの購入確率と定義する。そして、アップリフトは、レコメンデーションによる購買確率の上昇分、$p^T - p^C$と解釈できる。

Let $L^M_u$ be a recommendation list for user u, generated by the u new model M that we want to evaluate. In the recommendation logs, we have a list, $L^D_u$ of actually recommended items for the user u by the deployed model D. We assume that some items in $L^M_u$ are included in $L_u^D$, and some are not. We write $L^{M\capD}_u$ for items in both $L^M_u$ and $L^D_u$, and $L^{M\D}_u$ for items in $L^M_u$ but not in $L^D_u$. $L^{M\cap D}_u$ and $L^{M\D}_u$ can be regarded as the treatment set $S_T$ and control set $S_C$, respectively. Therefore, Eq. (1) becomes,

$$
\hat{\tau}_{L_u^M} = \frac{1}{|L^{M \cap D}_u|}
\sum_{i \in L^{M \cap D}_u} Y_{ui}^T
- \frac{1}{|L^{M \setminus D}_u|} \sum_{L^{M \setminus D}_u} Y_{ui}^C
\tag{4}
$$

The left and right terms are the purchase probabilities of items in $L_u^M$ if recommended and if not recommended, respectively.
左項と右項はそれぞれ、$L_u^M$のアイテムを推薦した場合と推薦しなかった場合の購入確率である.

We evaluated recommendation lists of Fig. 1 using this metric. The results are shown in the bottom row of Table 1. This metric aligns well with the total uplift, indicating that the proposed metric is appropriate for evaluating recommenders in terms of the uplift. We can also derive the SNIPS estimate of the uplift from Eq. (3):

この指標を用いて、図1の推薦リストを評価した。その結果を表1の最下段に示す。この指標は総上昇量とよく一致しており，提案した指標は上昇量という観点でレコメンダーの評価を行うのに適していることがわかる．また、式(3)からSNIPSによる高揚度の推定値を導き出すことができる。

$$
(\hat{\tau}_{L_u^M})_{SNIPS} = \frac{
    \sum_{i \in L_u^{M \cap D}} \frac{Y_{ui}^T}{e(X_{ui})}
}{
    \sum_{i \in L_u^{M \cap D}} \frac{1}{e(X_{ui})}
}
- \frac{
    \sum_{i \in L^{M \setminus D}_u} \frac{Y_{ui}^C}{1 - e(X_{ui})}
}{
    \sum_{i \in L^{M \setminus D}_u} \frac{1}{1 - e(X_{ui})}
}
\tag{5}
$$

For recommenders, Xui can be past records of purchase and recommendation, user demographics, and item contents.

As an evaluation metric of the model M, we take the average over all users U for both estimators:

$$
\bar{\tau} = \frac{1}{|U|} \sum_{u \in U} \hat{\tau}_{L_u^M}
\\
\bar{\tau}_{SNIPS} = \frac{1}{|U|} \sum_{u \in U} (\hat{\tau}_{L_u^M})_{SNIPS}
\tag{6}
$$

In this study, we employ these metrics for the ofine evaluation of uplift performance. We refer to τ¯ as Uplift@N and τ¯ SNIPS as UpliftSNIPS@N, where $N = |L_u^M|$ is the size of the recommendation. u Using the protocol described in this subsection, the uplift performance of a new model M is evaluated ofine using the purchase and recommendation logs under a currently deployed model D.

If the purchase probability without recommendation is negligible, e.g., in case of ad clicks, the right terms of Eq. (4) and (5) disappear. The equations then become similar to the previous counterfactual ofine evaluation [7, 25]. Our evaluation is an extension which considers the possibility of purchase without recommendation.

The uplift estimate by Eq. (4) depends on the assumption that potential outcomes of items in LM do not relate to logged recommendations by D. The uplift estimate by Eq. (5) depends on the assumption that covariates X used for estimating the propensity include enough information to resolve dependency between $(Y^T,Y^C)$ and Z. Though it is difcult to guarantee these assumptions, in practice, we can be confdent in the evaluation if the results of model comparison are consistent for both Uplift@N and UpliftSNIPS@N.

# 3. Uplift-Based Optimization

Of the four item classes TU, FU, TD, and TD, defned in Subsection 2.1, only TU items can lead to uplift when recommended. However, identifcation of these four classes requires observation of both YT and YC , which is not feasible by nature. This implies that we do not have an observable ground truth against which to train models. In this section, we propose uplift optimization methods to overcome the above problem.

## 3.1. Classifcation of the Observations

In Subsection 2.1, we categorized items into four hidden classes based on the combinations of potential outcomes. We now categorize items into observable classes from purchase and recommendation logs, while aligning them with the hidden classes. In the observed dataset, for a given user and time instance, an item is either recommended (R) or not (NR); and either purchased (P) or not (NP). This provides the following observable classes (also summarized in Table 2):

- An item is recommended and purchased (R-P). Possible hidden classes of the observed item are TU or FU.
- An item is recommended and NOT purchased (R-NP). Possible hidden classes of the observed item are FD or TD.
- An item is NOT recommended and purchased (NR-P). Possible hidden classes of the observed item are FU or TD.
- An item is NOT recommended and NOT purchased (NR-NP). Possible hidden classes of the observed item are TU or FD.

We defne $C_{class}$ as the set of items in $class \in {R-P, R-NP, NR-P, NR-NP}$ for a particular user, u ∈ U . We also defne I+ and I− as the set of positive and negative items for that user.
In traditional accuracy-based optimizations [14, 32, 35], I+ u ∼ CR−P ∪ CN R−P (purchased items) and I− ∼ CR−N P ∪ CN R−N P (non-purchased u items). We argue that this sampling method is not optimal for uplift and redefne the positive and negative samples. Since TU items result in an uplift, we consider classes that include TU items as positive. Thus, (CR−P ∪CN R−N P ) should be a reasonable choice for positive item sampling. Following the same reasoning, sinceCR−N P and CN R−P do not include TU items, Iu − ∼ (CR−N P ∪ CN R−P ).

However, using these positive samples has some problems. Most purchase logs are extremely sparse (NP is large) and most recommenders limit the recommendations to a small number (NR is large). This means that the cardinality of CN R−N P is much larger than that of the other classes and is close to the total number of items. Owing to a consumer’s limited purchasing power, we assume that the number of TU items is much smaller than the total number of items. Hence, the probability of the items in CN R−N P belonging to TU should be low:

$$
p(i \in TU | i \in C_{NR-NP}) = \frac{|TU \cap C_{NR-NP}|}{|C_{NR-NP}|}
\\
\approx \frac{|TU \cap C_{NR-NP}|}{|I|} < \frac{|TU|}{|I|} << 1
$$

On the contrary, considering the fact that recommenders generally improve sales substantially [1], we assume that the possibility of the items in CR−P belonging to TU is not relatively low. Hence,

$$
P(i \in TU | i \in C_{R-P}) > P(i \in TU | i \in C_{NR-NP})
$$

Because of the above, we cannot considerCN R−N P to be completely positive. Thus, we propose a parameter α, which is the probability of items from set CN R−N P being sampled as positive. We discuss this further in the following subsection.

## 3.2. Proposed Sampling Method

# 4. Related Work

## 4.1. Causal Inference for Recommenders

## 4.2. Recommendation Targeting Uplift

# 5. Experiments

## 5.1. Experimental Settings

## 5.2. Performance Comparison (RQ1)

## 5.3. Uplift-based Optimization Properties (RQ2)

## 5.4. Trends of the Recommended Items (RQ3)

# 6. Conclusions
