## 0.1. link リンク

- https://arxiv.org/abs/1602.05352 https://arxiv.org/abs/1602.05352

## 0.2. title タイトル

Recommendations as Treatments: Debiasing Learning and Evaluation
トリートメントとしてのレコメンデーション 学習と評価の乖離

## 0.3. abstract アブストラクト

Most data for evaluating and training recommender systems is subject to selection biases, either through self-selection by the users or through the actions of the recommendation system itself.
推薦システムを評価・訓練するためのデータの多くは、ユーザによる自己選択や推薦システム自体の動作によって、選択バイアスがかかっている。
In this paper, we provide a principled approach to handling selection biases, adapting models and estimation techniques from causal inference.
本論文では、選択バイアスを扱うための原理的なアプローチを提供し、因果推論からモデルと推定技術を適応させる。
The approach leads to unbiased performance estimators despite biased data, and to a matrix factorization method that provides substantially improved prediction performance on real-world data.
このアプローチにより、偏ったデータにもかかわらず不偏の性能推定値が得られ、また、実世界のデータにおいて予測性能を大幅に向上させる行列因数分解法が得られる。
We theoretically and empirically characterize the robustness of the approach, finding that it is highly practical and scalable.
本アプローチの堅牢性を理論的・実証的に評価し、高い実用性とスケーラビリティを有することを明らかにしました。

# 1. Introduction 序章

Virtually all data for training recommender systems is subject to selection biases.
レコメンダーシステムの学習用データは、事実上、選択バイアスがかかっている。
For example, in a movie recommendation system users typically watch and rate those movies that they like, and rarely rate movies that they do not like (Pradel et al., 2012).
例えば、映画推薦システムにおいて、ユーザーは通常、自分の好きな映画を観て評価し、自分の嫌いな映画を評価することはほとんどありません（Pradel et al, 2012）。(ユーザ自身の選択行動によるselection bias)
Similarly, when an adplacement system recommends ads, it shows ads that it believes to be of interest to the user, but will less frequently display other ads.
同様に、アドプレースメントシステムが広告を推奨する場合、ユーザが興味を持つと思われる広告を表示しますが、それ以外の広告を表示する頻度は低くなる. (推薦システムの動作によるselection bias)
Having observations be conditioned on the effect we would like to optimize (e.g.the star rating, the probability of a click, etc.) leads to data that is Missing Not At Random (MNAR) (Little & Rubin, 2002).
最適化したい効果（例：星の評価、クリックの確率など）でオブザベーションを条件付けると、**MNAR（Missing Not At Random）**(Little & Rubin, 2002)と呼ばれるデータになります。
This creates a widely-recognized challenge for evaluating recommender systems (Marlin & Zemel, 2009; Myttenaere et al., 2014).
このことは、レコメンダーシステムの評価において広く認識されている課題を生み出しています（Marlin & Zemel, 2009; Myttenaere et al, 2014）。

We develop an approach to evaluate and train recommender systems that remedies selection biases in a principled, practical, and highly effective way.
本論文は、選択バイアスを是正するレコメンダーシステムを、原理的、実用的かつ効果的に評価・訓練するアプローチを開発する。
Viewing recommendation from a causal inference perspective, we argue that exposing a user to an item in a recommendation system is an intervention analogous to exposing a patient to a treatment in a medical study.
**推薦を因果推論の観点から見ると**、推薦システムでユーザにアイテムを見せることは、医学研究において患者に治療法を見せるのと同じような介入(intervention)であると主張する.
In both cases, the goal is to accurately estimate the effect of new interventions (e.g.a new treatment policy or a new set of recommendations) despite incomplete and biased data due to self-selection or experimenterbias.
どちらの場合も、自己選択や実験者のバイアスによる不完全で偏ったデータにもかかわらず、新しい介入（新しい治療方針や新しい勧告のセットなど）の効果を正確に推定することが目的である.
By connecting recommendation to causal inference from experimental and observational data, we derive a principled framework for unbiased evaluation and learning of recommender systems under selection biases.
**推薦と実験・観測データからの因果推論を結びつけること**で、選択バイアス下での推薦システムの公平な評価と学習のための原則的なフレームワークを導き出す。

The main contribution of this paper is four-fold.
本論文の主な貢献は、4つある。
First, we show how estimating the quality of a recommendation system can be approached with propensity-weighting techniques commonly used in causal inference (Imbens & Rubin, 2015), complete-cases analysis (Little & Rubin, 2002), and other problems (Cortes et al., 2008; Bickel et al., 2009; Sugiyama & Kawanabe, 2012).
まず、因果推論（Imbens & Rubin, 2015）、完全事例分析（Little & Rubin, 2002）などの問題でよく使われる**propensity-weighting(傾向性重み付け)技術**を使って、推薦システムの品質を推定する方法を示す（Cortes et al, 2008; Bickel et al, 2009; Sugiyama & Kawanabe, 2012）.
In particular, we derive unbiased estimators for a wide range of performance measures (e.g.MSE, MAE, DCG).
特に、幅広い性能指標（MSE、MAE、DCGなど）に対して不偏推定量を導出することができる.
Second, with these estimators in hand, we propose an Empirical Risk Minimization (ERM) framework for learning recommendation systems under selection bias, for which we derive generalization error bounds.
次に、これらの推定量を用いて、選択バイアス下の推薦システムを学習するための**Empirical Risk Minimization (ERM) フレームワーク**を提案し、そのための一般化誤差の境界を導出する。
Third, we use the ERM framework to derive a matrix factorization method that can account for selection bias while remaining conceptually simple and highly scalable.
第三に、ERMフレームワークを用いて、選択バイアスを考慮しつつ、**概念的にシンプルで拡張性の高い行列分解法**を導出する。
Fourth, we explore methods to estimate propensities in observational settings where selection bias is due to selfselection by the users, and we characterize the robustness of the framework against mis-specified propensities.
第四に、選択バイアスがユーザの自己選択によるものである観察設定において、propensityを推定する方法を探求し、予感の誤特定に対する枠組みの頑健性を特徴付けるものである。

Our conceptual and theoretical contributions are validated in an extensive empirical evaluation.
私たちの概念的・理論的な貢献は、広範な実証評価で検証されています。
For the task of evaluating recommender systems, we show that our performance estimators can be orders-of-magnitude more accurate than standard estimators commonly used in the past (Bell et al., 2007).
レコメンダーシステムを評価するタスクにおいて、我々の性能推定器は、過去に一般的に使用された標準的な推定器よりも数桁高い精度を持つことができることを示す（Bell et al, 2007）.
For the task of learning recommender systems, we show that our new matrix factorization method substantially outperforms methods that ignore selection bias, as well as existing state-of-the-art methods that perform jointlikelihood inference under MNAR data (Hernandez-Lobato ´ et al., 2014).
推薦システムを学習するタスクに対して、我々の新しい行列分解法は、選択バイアスを無視する手法や、MNARデータの下で共同尤度推論を行う既存の最先端手法を大幅に上回ることを示す（Hernandez-Lobato´ et al, 2014）。
This is especially promising given the conceptual simplicity and scalability of our approach compared to joint-likelihood inference.
これは、共同尤度推論と比較して、我々のアプローチが概念的に単純でスケーラブルであることを考えると、特に有望である。
We provide an implemention of our method, as well as a new benchmark dataset, online1 .
本手法の実装と新しいベンチマークデータセットをオンラインで提供します1。

# 2. Related Work 関連作品

## 2.1. 推薦システムとMNAR

Past work that explicitly dealt with the MNAR nature of recommendation data approached the problem as missingdata imputation based on the joint likelihood of the missing data model and the rating model (Marlin et al., 2007; Marlin & Zemel, 2009; Hernandez-Lobato et al.´ , 2014).
推薦データのMNARの性質を明示的に扱った過去の研究は、欠損データモデルと評価モデルの共同尤度に基づく欠損データインピュテーションとして問題にアプローチした（Marlin et al.2007; Marlin & Zemel, 2009; Hernandez-Lobato et al.´ ,2014）．
This has led to sophisticated and highly complex methods.
そのため、洗練された高度に複雑な手法が採用されています。
We take a fundamentally different approach that treats both models separately, making our approach modular and scalable.
私たちは、この**2つのモデル**(欠損データモデルと評価モデル?)を別々に扱うという根本的に異なるアプローチをとり、私たちのアプローチをモジュール化し、拡張可能にしています。
Furthermore, our approach is robust to mis-specification of the rating model, and we characterize how the overall learning process degrades gracefully under a mis-specified missing-data model.
さらに、本アプローチは評価モデルの誤仕様に対して頑健であり、誤仕様の欠測モデルの下で学習プロセス全体がどのように潔く劣化するかを特徴付けることができる。
We empirically compare against the state-of-the-art joint likelihood model (Hernandez-Lobato et al.´ , 2014) in this paper.
本稿では、最先端の**共同尤度モデル（Hernandez-Lobato et al.´ , 2014）**と実証的に比較しています。

Related but different from the problem we consider is recommendation from positive feedback alone (Hu et al., 2008; Liang et al., 2016).
関連しているが、我々が考える問題とは異なるのが、**ポジティブフィードバックのみによる推薦**である（Hu et al, 2008; Liang et al, 2016）.
Related to this setting are also alternative approaches to learning with MNAR data (Steck, 2010; 2011; Lim et al., 2015), which aim to avoid the problem by considering performance measures less affected by selection bias under mild assumptions.
この設定に関連して、MNARデータを用いた学習に対する代替アプローチ（Steck, 2010; 2011; Lim et al, 2015）もあり、穏やかな仮定の下で選択バイアスの影響を受けにくい性能指標を考慮することで問題を回避することを目指しています。
Of these works, the approach of Steck (2011) is most closely related to ours, since it defines a recall estimator that uses item popularity as a proxy for propensity.
これらの研究のうち、Steck (2011)のアプローチは、**アイテムの人気を傾向(propensity)の代理として使用する**recall estimator(推定量)を定義しているため、我々のアプローチと最も密接な関係があります。
Similar to our work, Steck (2010; 2011) and Hu et al.(2008) also derive weighted matrix factorization methods, but with weighting schemes that are either heuristic or need to be tuned via cross validation.
Steck (2010; 2011) や **Hu et al. (2008)(あれ? implicit ALSの元論文...!)**も我々の研究と同様に**重み付け行列分解法**を導出しているが、重み付けのスキームは発見的であるかクロスバリデーションによって調整する必要がある。
In contrast, our weighted matrix factorization method enjoys rigorous learning guarantees in an ERM framework.
これに対し、我々の重み付き行列分解法は、ERMの枠組みで厳密な学習保証を享受することができる.

## 2.2. Propensity-based approach

Propensity-based approaches have been widely used in causal inference from observational studies (Imbens & Rubin, 2015), as well as in complete-case analysis for missing data (Little & Rubin, 2002; Seaman & White, 2013) and in survey sampling (Thompson, 2012).
**傾向ベースアプローチ**は，観察研究からの因果推論（Imbens & Rubin, 2015）や，欠損データに対する完全症例分析（Little & Rubin, 2002; Seaman & White, 2013），調査サンプリング（Thompson, 2012）で広く利用されてきた．
However, their use in matrix completion is new to our knowledge.
しかし、**matrix completionにおけるこれらの使用は、我々の知る限り新しいもの**である。
Weighting approaches are also widely used in domain adaptation and covariate shift, where data from one source is used to train for a different problem (e.g., Huang et al., 2006; Bickel et al., 2009; Sugiyama & Kawanabe, 2012).
重み付けアプローチは、ドメイン適応や共変量シフトにおいても広く用いられており、あるソースからのデータを用いて異なる問題に対する学習を行うことができる（例：Huang et al, 2006; Bickel et al, 2009; Sugiyama & Kawanabe, 2012）.
We will draw upon this work, especially the learning theory of weighting approaches in (Cortes et al., 2008; 2010).
この研究、特に(Cortes et al., 2008; 2010)の重み付けアプローチの学習理論を活用します。

# 3. Unbiased Performance Estimation for Recommendation レコメンデーションのための不偏の性能推定

Consider a toy example adapted from Steck (2010) to illustrate the disastrous effect that selection bias can have on conventional evaluation using a test set of held-out ratings.
Steck(2010)から引用したおもちゃの例で、選択バイアスが従来の評価に与える悲惨な影響について考えてみましょう。
Denote with u ∈ {1, ..., U} the users and with i ∈ {1, ..., I} the movies.
u∈｛1，...，U｝をユーザ、i∈｛1，...，I｝を映画とする.
Figure 1 shows the matrix of true ratings $Y \in \mathbf{R}^{U \times I}$ for our toy example, where a sub set of users are “horror lovers” who rate all horror movies 5 and all romance movies 1.
図1は、"ホラー好き"のユーザのサブセットが、すべてのホラー映画を5、すべてのロマンス映画を1と評価する場合における、真の評価の行列$Y \in \mathbf{R}^{U \times I}$を示したものである。
Similarly, there is a subset of “romance lovers” who rate just the opposite way.
同様に、「ロマンス好き」の中にも、正反対の評価をする人がいます。
However, both groups rate dramas as 3.
しかし、どちらのグループもドラマを3として評価しています。
The binary matrix $O ∈ {0, 1}^{U×I}$ in Figure 1 shows for which movies the users provided their rating to the system, [Ou,i = 1] ⇔ [Yu,i observed].
図1の2値行列$O ∈ {0, 1}^{U×I}$は、ユーザがどの映画の評価をシステムに提供したかを示しており、$[O_{u,i} = 1] ⇔ [Y_{u,i} \text{observed}]$となる。
Our toy example shows a strong correlation between liking and rating a movie, and the matrix P describes the marginal probabilities $P_{u,i} = P(O_{u,i} = 1)$ with which each rating is revealed.
このおもちゃの例では、映画の好き嫌いと評価の間に強い相関があり、行列Pは、各評価が明らかになる周辺確率 $P_{u,i} = P(O_{u,i} = 1)$ を記述しています。
For this data, consider the following two evaluation tasks.
このデータについて、次の2つの評価作業を考えてみる。

## 3.1. Task 1: Estimating Rating Prediction Accuracy タスク1： 視聴率予測精度の見積もり

For the first task, we want to evaluate how well a predicted rating matrix Yˆ reflects the true ratings in Y .
最初のタスクでは，予測された評価行列Yˆが，Yの真の評価をどれだけ反映しているかを評価したい。
Standard evaluation measures like Mean Absolute Error (MAE) or Mean Squared Error (MSE) can be written as:
平均絶対誤差（MAE）や平均二乗誤差（MSE）のような標準的な評価指標は、次のように書くことができます：

$$
R(\hat{Y}) = \frac{1}{U \cdot I} \sum_{u=1}^{U} \sum_{i=1}^{I} \delta_{u,i}(Y, \hat{Y})
\tag{1}
$$

for an appropriately chosen $\delta_{u,i}(Y, \hat{Y})$.
を適切に選択した$\delta_{u,i}(Y, \hat{Y})$の場合。

$$
MAE: \delta_{u,i}(Y, \hat{Y}) = |Y_{u,i} - \hat{Y}_{u,i}|
\tag{2}
$$

$$
MSE: \delta_{u,i}(Y, \hat{Y}) = (Y_{u,i} - \hat{Y}_{u,i})^2

\tag{3}
$$

$$
Accuracy: \delta_{u,i}(Y, \hat{Y}) = \mathbf{1}(Y_{u,i} = \hat{Y}_{u,i})
\tag{4}
$$

Since Y is only partially known, the conventional practice is to estimate R(Yˆ ) using the average over only the observed entries,
$Y$は部分的にしかわからないため、従来は観測されたエントリのみの平均値を用いて$R(\hat{A})$を推定していた、

$$
\hat{R}_{naive}(\hat{Y})
= \frac{1}{|{(u,i):O_{u,i} = 1}|} \sum_{(u,i):O_{u,i}=1} \delta_{u,i}(Y,\hat{Y})
\tag{5}
$$

We call this the naive estimator, and its naivety leads to a gross misjudgment for the Yˆ 1 and Yˆ 2 given in Figure 1.
これを**ナイーブ推定量**と呼びますが、そのナイーブさは、図1で与えられたYˆ1、Yˆ2に対する重大な誤判定を招きます。
Even though Yˆ 1 is clearly better than Yˆ 2 by any reasonable measure of performance, Rˆ naive(Yˆ ) will reliably claim that Yˆ 2 has better MAE than Yˆ 1.
どのような合理的な性能指標でもYˆ 1がYˆ 2より明らかに優れているにもかかわらず、ナイーブ推定量 $\hat{R}_{naive}(\hat{Y})$は、Yˆ 2がYˆ 1よりMAEの観点から優れていると確実に主張することになる.
This error is due to selection bias, since 1-star ratings are under-represented in the observed data and δu,i(Y, Yˆ ) is correlated with Yu,i.
**この誤差は選択バイアスによるもの**で、1つ星の評価は観測データでは過小評価されており、δu,i(Y, Yˆ )はYu,iと相関があるためである.
More generally, under selection bias, Rˆ naive(Yˆ ) is not an unbiased estimate of the true performance R(Yˆ ) (Steck, 2013):
より一般的には、選択バイアスの下では、ナイーブ推定量は、真の性能の不偏推定値ではない（Steck, 2013）：

$$
E_{O}[\hat{R}_{naive}(\hat{Y})] \neq R(\hat{Y})
\tag{6}
$$

Before we design an improved estimator to replace Rˆ naive(Yˆ ), let’s turn to a related evaluation task.
$\hat{R}_{naive}(\hat{Y})$ を置き換える改良型推定器を設計する前に、関連する評価タスクに目を向けよう.

## 3.2. Task 2: Estimating Recommendation Quality タスク2：レコメンデーション品質の見積もり

Instead of evaluating the accuracy of predicted ratings, we may want to more directly evaluate the quality of a particular recommendation.
予測された評価値の精度を評価するのではなく、**より直接的に特定の推薦の質を評価したい場合**がある。
To this effect, let’s redefine Yˆ to now encode recommendations as a binary matrix analogous to O, where [Yˆ u,i = 1] ⇔ [i is recommended to u], limited to a budget of k recommendations per user.
このため、$\hat{Y}$を再定義し、Oに類似した二値行列として**推薦結果を符号化**する。ここで、$[\hat{Y}_{u,i} = 1]$ ⇔ [i が u に推薦される]とし、1ユーザあたりk件の推薦文を予算として限定する.
An example is Yˆ 3 in Figure 1.
例として、図1のYˆ3が挙げられる。
A reasonable way to measure the quality of a recommendation is the Cumulative Gain (CG) that the user derives from the recommended movies, which we define as the average star-rating of the recommended movies in our toy example.(More realistically, Y would contain quality scores derived from indicators like “clicked” and “watched to the end”.)
推薦の質を測る合理的な方法は、**ユーザが推薦された映画から得るCumulative Gain(累積利益, CG)**であり、我々はおもちゃの例で推薦された映画の平均星評価と定義する。(より現実的には、Yには「クリック」「最後まで見た」などの指標から得られる品質スコア クリックした」「最後まで見た」などの指標に基づく品質スコアを含む。)
CG can again be written in the form of Eq.(1) with
CGは、再び式(1)の形で、次のように書くことができます。(真の嗜好$Y_{u,i}$Yがより高いアイテムを推薦しているか否か.)

$$
CG: \delta_{u,i}(Y, \hat{Y}) = (I/k) \hat{Y} \cdot Y_{u,i}
\tag{7}
$$

However, unless users have watched all movies in Yˆ , we cannot compute CG directly via Eq.(1).
しかし、ユーザーがYˆの全ての映画を視聴していない限り、式(1)を用いて直接CGを計算することはできない. (真の目的関数は計算できない。観測データから近似する他ない...)
Hence, we are faced with the counterfactual question: how well would our users have enjoyed themselves (in terms of CG), if they had followed our recommendations Yˆ instead of watching the movies indicated in O? Note that rankings of recommendations are similar to the set-based recommendation described above, and measures like Discounted Cumulative Gain (DCG), DCG@k, Precision at k (PREC@k), and others (Aslam et al., 2006; Yilmaz et al., 2008) also fit in this setting.
したがって、我々は、**実際に観測された映画(Oで示される)を見ていた(消費した)代わりに、我々の推薦Yˆに従って映画を消費した場合、我々のユーザは（CGの面で）どの程度楽しめただろうか**、という**反実仮想的な問い**に直面することになる? 推薦のランキングは、上述のセットベースの推薦と同様であり、割引累積利益（DCG）、DCG@k、Precision at k（PREC@k）などの尺度（Aslam et al.、2006；Yilmaz et al.、2008）もこの設定に適合することに注意。
For those, let the values of Yˆ in each row define the predicted ranking, then
ちなみに、それらのmetricついて同様、各行のYˆの値を予測される順位とすると

$$
DCG: \delta_{u,i}(Y,\hat{Y}) = (I /\log(rank(\hat{Y}_{u,i}))) \cdot Y_{u,i}
\tag{8}
$$

$$
Precision@k: \delta_{u,i}(Y,\hat{Y}) = (I /k) \cdot Y_{u,i} \cdot \mathbb{1}{rank(\hat{Y}_{u,i}) \leq k}
\tag{9}
$$

One approach, similar in spirit to condensed DCG (Sakai, 2007), is to again use the naive estimator from Eq.(5).
凝縮型DCG（Sakai, 2007）と同様の考え方で、式(5)から再びナイーブな推定量を用いる方法もある。
However, this and similar estimators are generally biased for R(Yˆ ) (Pradel et al., 2012; Steck, 2013).
しかし，この推定量や類似の推定量は，一般にR(Yˆ )に偏りがある（Pradel et al, 2012; Steck, 2013）。(i.e. R(\hat{Y})の普遍推定量ではない)

To get unbiased estimates of recommendation quality despite missing observations, consider the following connection to estimating average treatment effects of a given policy in causal inference, that was already explored in the contextual bandit setting (Li et al., 2011; Dud´ık et al., 2011).
観測値が欠損しているにもかかわらず、推薦の質の不偏推定値を得るには、**因果推論における与えられたpolicyの average treatment effects**の推定に次のような関連性を考慮する。これは、文脈バンディットの設定ですでに探求されていた（Li et al, 2011; Dud´ık et al, 2011）．
If we think of a recommendation as an intervention analogous to treating a patient with a specific drug, in both settings we want to estimate the effect of a new treatment policy (e.g.give drug A to women and drug B to men, or new recommendations Yˆ ).
推薦を特定の薬で患者を治療するような介入と考えるなら、**どちらの設定(task1でもtask2でも)でも**、新しい治療方針（例えば、女性には薬Aを、男性には薬Bを与える、あるいは新しい推薦Yˆ）の効果を推定したい。
The challenge in both cases is that we have only partial knowledge of how much certain patients (users) benefited from certain treatments (movies) (i.e., Yu,i with Ou,i = 1), while the vast majority of potential outcomes in Y is unobserved.
どちらの場合も、**ある患者（ユーザー）がある治療（映画）からどれだけ恩恵を受けたかについては部分的な知識しかなく**（すなわち、$O_{u,i} = 1$の $Y_{u,i}$のみ）、Yにおける潜在的な結果の大部分は未観測であるという課題がある.

## 3.3. Propensity-Scored Performance Estimators プロペンシティ-スコアード・パフォーマンス・エスティメーター

The key to handling selection bias in both of the abovementioned evaluation tasks lies in understanding the process that generates the observation pattern in O.
上記のいずれの評価作業においても、**選択バイアスを処理する鍵は、Oの観察パターンを生成するプロセスを理解すること**にある。
This process is typically called the Assignment Mechanism in causal inference (Imbens & Rubin, 2015) or the Missing Data Mechanism in missing data analysis (Little & Rubin, 2002).
このプロセスは、一般的に**因果推論におけるAssignment Mechanism** (Imbens & Rubin, 2015)、**欠損データ分析におけるMissing Data Mechanism** (Little & Rubin, 2002)と呼ばれている.
We differentiate the following two settings:
以下の2つの設定を区別しています(実環境において、2種類の異なる観察パターン生成プロセスがある。)：

- **Experimental Setting**. In this setting, the assignment mechanism is under the control of the recommendation system. An example is an ad-placement system that controls which ads to show to which user. 実験セッティング。 この設定では、割り当て機構は推薦システムの制御下にある。 例えば、どの広告をどのユーザに見せるかを制御するアドプレースメントシステムがあります。

- **Observational Setting**. In this setting, the users are part of the assignment mechanism that generates O. An example is an online streaming service for movies, where users self-select the movies they watch and rate. オブザベーションセッティング この設定では、ユーザはOを生成する割り当て機構の一部である。 例えば、映画のオンラインストリーミングサービスでは、ユーザが視聴する映画を自分で選んで評価します。

In this paper, we assume that the assignment mechanism is probabilistic, meaning that the marginal probability Pu,i = P(Ou,i = 1) of observing an entry Yu,i is non-zero for all user/item pairs.
本論文では、割り当てメカニズムが確率的であると仮定する。つまり、エントリ$Y_{u,i}$を観察する周辺確率$P_{u,i} = P(O_{u,i} = 1)$は、**すべてのユーザとアイテムのペアに対して非ゼロであると仮定する**.
This ensures that, in principle, every element of Y could be observed, even though any particular O reveals only a small subset.
これにより、特定のOが小さな部分集合しか明らかにしないとしても、原理的にはYのすべての要素を観察することができる.
We refer to Pu,i as the propensity of observing Yu,i.
$P_{u,i}$を「**$Y_{u,i}$ を観察する傾向(propensity)**」と呼ぶことにする.
In the experimental setting, we know the matrix P of all propensities, since we have implemented the assignment mechanism.
experimental setting では、割り当て機構を実装しているので、すべてのpropensitiesの行列Pを知ることができる.
In the observational setting, we will need to estimate P from the observed matrix O.
**observational setting では、観測された行列OからPを推定する必要がある**.
We defer the discussion of propensity estimation to Section 5, and focus on the experimental setting first.
(observational settingの際に必要な) propensity estimation の議論は第5節に譲り、まずはexperimental settingに焦点を当てる。

**IPS Estimator**:
IPS Estimatorです：

The Inverse-Propensity-Scoring (IPS) estimator (Thompson, 2012; Little & Rubin, 2002; Imbens & Rubin, 2015), which applies equally to the task of rating prediction evaluation as to the task of recommendation quality estimation, is defined as,
レコメンド品質推定のタスクと同様にレーティング予測評価のタスクにも適用される**Inverse-Propensity-Scoring (IPS)推定量** (Thompson, 2012; Little & Rubin, 2002; Imbens & Rubin, 2015) は、次のように定義されている、

$$
\hat{R}_{IPS}(\hat{Y}|P) = \frac{1}{U \cdot I} \sum_{(u,i):O_{u,i} = 1} \frac{\delta_{u,i}(Y, \hat{Y})}{P_{u,i}}
\\
= \frac{1}{U \cdot I} \sum_{u} \sum_{i} \frac{\delta_{u,i}(Y, \hat{Y})}{P_{u,i}} \cdot O_{u,i}
\\
\because \text{O_{u,i}はbinary変数なので...!}
\tag{10}
$$

Unlike the naive estimator Rˆ naive(Yˆ ), the IPS estimator is unbiased for any probabilistic assignment mechanism.
ナイーブ推定量$\hat{R(\hat{Y})}_{naive}$ とは異なり、**IPS推定量はどのような確率的割り当て機構に対しても不偏である**.
Note that the IPS estimator only requires the marginal probabilities Pu,i and unbiased-ness is not affected by dependencies within O:
なお、IPS推定器は周辺確率Pu,iのみを必要とし、不偏性はO内の依存性には影響されない：

$$
E_{O}[\hat{R}_{IPS}(\hat{Y}|P)]
= \frac{1}{U\cdot I} \sum_{u} \sum_{i}
E_{O_{u,i}}[\frac{\delta_{u,i}(Y,\hat{Y})}{P_{u,i}} O_{u,i}]
\\
= \frac{1}{U\cdot I} \sum_{u} \sum_{i}
\delta_{u,i}(Y,\hat{Y})
\\
\because \text{定義より...} P_{u,i} = E_{O_{u,i}}[O_{u,i}]
\\
= R(\hat{Y})
\tag{10.5}
$$

To characterize the variability of the IPS estimator, however, we assume that observations are independent given P, which corresponds to a multivariate Bernoulli model where each Ou,i is a biased coin flip with probability Pu,i.
しかし、IPS推定量のばらつきを特徴づけるために、観測値($O$の各要素)は$P$が与えられた時に独立であると仮定する(=条件付き独立?)。これは、多変量ベルヌーイモデルに相当し、**各Ou,iは確率Pu,iで偏ったコインフリップ**となる.
The following proposition (proof in appendix) provides some intuition about how the accuracy of the IPS estimator changes as the propensities become more “non-uniform”.
次の命題（証明は付録）は、**propensities(傾向)が「非一様」になるにつれてIPS推定器の精度がどのように変化するか**について、いくつかの直感を与える.(おまけっぽい内容だから優先度は低そう...!)

Proposition 3.1 (Tail Bound for IPS Estimator).
命題3.1（IPS推定量のテールバウンド）。
Let P be the independent Bernoulli probabilities of observing each entry.
各エントリーを観察する独立したベルヌーイ確率をPとする。
For any given Yˆ and Y , with probability 1 − η, the IPS estimator Rˆ IP S(Yˆ |P) does not deviate from the true R(Yˆ ) by more than:
任意の与えられたYˆとYに対して、確率$1 - η$で、IPS推定量Rˆ IP S(Yˆ |P) は、**真のR(Yˆ )からそれ以上乖離することはない**：

$$
\tag{10.6}
$$

where ρu,i = δu,i(Y,Yˆ ) Pu,i if Pu,i < 1, and ρu,i = 0 otherwise.
ここで、Pu,i＜1の場合はρu,i＝δu,i（Y,Yˆ）Pu,i、それ以外の場合はρu,i＝0である。

To illustrate this bound, consider the case of uniform propensities Pu,i = p.
この境界を説明するために、一様な予言Pu,i = pの場合を考えてみる。
This means that n = p U I elements of Y are revealed in expectation.
これは、Yのn＝p U I個の要素が期待値で明らかになることを意味する。
In this case, the bound is O(1/(p √ UI)).
この場合、境界はO(1/(p √ UI))となる。
If the Pu,i are non-uniform, the bound can be much larger even if the expected number of revealed elements, PPu,i is n.
Pu,iが不均一な場合、明らかにされた要素の期待数PPu,iがnであっても、その境界はより大きくなる可能性がある。
We are paying for the unbiased-ness of IPS in terms of variability, and we will evaluate whether this price is well spent throughout the paper.
IPSのバラツキに対する不偏性という対価を払っているわけですが、この対価がうまく使われているかどうかは、論文を通して評価していきたいと思います。

**SNIPS Estimator**.
SNIPS Estimatorです。
One technique that can reduce variability is the use of control variates (Owen, 2013).
ばらつきを抑える手法として、**制御変量の利用**がある（Owen, 2013）。
Applied to the IPS estimator, we know that EO hP (u,i):Ou,i=1 1 Pu,i i = U · I.
IPS推定量に適用すると、$E_{O}[\sum_{(u,i):O_{u,i}=1} \frac{1}{P_{u,i}}]= U \cdot I$ となることがわかる.(これを使うと、IPS推定量の分散を低減できる...??)
This yields the SelfNormalized Inverse Propensity Scoring (SNIPS) estimator (Trotter & Tukey, 1956; Swaminathan & Joachims, 2015)
これにより、**Self Normalized Inverse Propensity Scoring (SNIPS)** estimator (Trotter & Tukey, 1956; Swaminathan & Joachims, 2015) が得られます。

$$
\hat{R}_{SNIPS}(\hat{Y}|P) = \frac{
    \sum_{(u,i):O_{u,i} = 1} \frac{\delta_{u,i}(Y, \hat{Y})}{P_{u,i}} % 分子=元のIPS推定量の式.
}{
    \sum_{(u,i):O_{u,i}=1} \frac{1}{P_{u,i}} % 制御変量?
}
\tag{11}
$$

The SNIPS estimator often has lower variance than the IPS estimator but has a small bias (Hesterberg, 1995).
SNIPS推定器はIPS推定器よりも分散が小さいことが多いが、小さいバイアスを持っている.（Hesterberg, 1995）。

## 3.4. Empirical Illustration of Estimators 推定量の経験則による説明

To illustrate the effectiveness of the proposed estimators we conducted an experiment on the semi-synthetic ML100K dataset described in Section 6.2.For this dataset, Y is completely known so that we can compute true performance via Eq.(1).
提案する推定量の有効性を示すために、セクション6.2で説明した半合成のML100Kデータセットで実験を行った、 このデータセットでは、Yは完全に既知であるため、式(1)を用いて真の性能を計算することが可能である.
The probability Pu,i of observing a rating Yu,i was chosen to mimic the observed marginal rating distribution in the original ML100K dataset (see Section 6.2) such that, on average, 5% of the Y matrix was revealed.
評価$Y_{u,i}$を観測する確率$P_{u,i}$は，ML100Kデータセット（セクション6.2参照）で観測された周辺評価分布(?)を模倣し，平均してY行列の5％が明らかになる(=観測される)ように選択した．

Table 1 shows the results for estimating rating prediction accuracy via MAE and recommendation quality via DCG@50 for the following five prediction matrices Yˆ i .
表1は，以下の5つの予測行列Yˆ i について，MAEによる視聴率予測精度とDCG@50による推薦品質を推定した結果である。
Let |Y = r| be the number of r-star ratings in Y .
Yに含まれるrつ星の評価の数を｜Y = r｜とする.(explicit feedbackの例なんだなー...)

- REC ONES: The prediction matrix Yˆ is identical to the true rating matrix Y , except that |{(u, i) : Yu,i = 5}| randomly selected true ratings of 1 are flipped to 5. This means half of the predicted fives are true fives, and half are true ones. i) : Yu,i = 5} つまり、予測された5人のうち半分が真の5人であり、半分が真の1人である。

- REC FOURS: Same as REC ONES, but flipping 4-star ratings instead. REC FOURS： REC ONESと同じですが、代わりに4つ星の評価をひっくり返します。

- ROTATE: For each predicted rating Yˆ u,i = Yu,i −1 when Yu,i ≥ 2, and Yˆ u,i = 5 when Yu,i = 1. を回転させる： 各予測レーティングについて、Yu,i≧2のときはYˆ u,i = Yu,i -1、Yu,i = 1のときはYˆ u,i = 5。

- SKEWED: Predictions Yˆ u,i are sampled from N (Yˆ raw u,i |µ = Yu,i, σ = 6−Yu,i 2 ) and clipped to the interval [0, 6]. = Yu,i, σ = 6−Yu,i 2 ) and clipped to the interval [0, 6].

- COARSENED: If the true rating Yu,i ≤ 3, then Yˆ u,i = 3. Otherwise Yˆ u,i = 4. COARSENEDとする： 真の評価 Yu,i ≦ 3 ならば、Yˆ u,i ＝ 3 となる。 それ以外の場合はYˆ u,i = 4となります。

Rankings for DCG@50 were created by sorting items according to Yˆ i for each user.
DCG@50のランキングは、各ユーザーのYˆiに従って項目をソートして作成しました。
In Table 1, we report the average and standard deviation of estimates over 50 samples of O from P.
表1では、PからO(観測)の50サンプルにわたる推定値の平均と標準偏差を報告する。
We see that the mean IPS estimate perfectly matches the true performance for both MAE and DCG as expected.
**IPSの平均推定値は、予想通りMAEとDCGの両方で真の性能に完全に一致する**ことがわかる.
The bias of SNIPS is negligible as well.
SNIPSのバイアスも無視できるほどです。
The naive estimator is severely biased and its estimated MAE incorrectly ranks the prediction matrices Yˆ i (e.g.it ranks the performance of REC ONES higher than REC FOURS).
**ナイーブ推定器は著しく偏り**、その推定MAEは予測行列Yˆiを誤ってランク付けする（例えば、REC ONESの性能をREC FOURSより高くランク付けしてしまう）。
The standard deviation of IPS and SNIPS is substantially smaller than the bias that Naive incurs.
IPSとSNIPSの標準偏差は、Naiveが発生させるバイアスよりもかなり小さいです。
Furthermore, SNIPS manages to reduce the standard deviation of IPS for MAE but not for DCG.
さらに、SNIPSは、MAEではIPSの標準偏差を小さくすることができたが、DCGではできなかった。
We will empirically study these estimators more comprehensively in Section 6.
これらの推定量については、第6節でより包括的に実証的に検討する。

# 4. Propensity-Scored Recommendation Learning 傾向スコア付き推薦学習

We will now use the unbiased estimators from the previous section in an Empirical Risk Minimization (ERM) framework for learning, prove generalization error bounds, and derive a matrix factorization method for rating prediction.
ここでは、前節の不偏推定量を**ERM（Empirical Risk Minimization）**の枠組み(=観測されたデータのみを使って誤差を最小化するように学習する方法だっけ?)で学習に用い、汎化誤差の境界を証明し、rating予測のための行列分解法を導出する。

## 4.1. ERM for Recommendation with Propensities プロペンシティを用いたレコメンデーションのためのERM

Empirical Risk Minimization underlies many successful learning algorithms like SVMs (Cortes & Vapnik, 1995), Boosting (Schapire, 1990), and Deep Networks (Bengio, 2009).
経験的リスク最小化は、SVM (Cortes & Vapnik, 1995), Boosting (Schapire, 1990), Deep Networks (Bengio, 2009) など多くの成功した学習アルゴリズムの基礎となっている.
Weighted ERM approaches have been effective for cost-sensitive classification, domain adaptation and covariate shift (Zadrozny et al., 2003; Bickel et al., 2009; Sugiyama & Kawanabe, 2012).
**重み付けERMアプローチ**は、コスト重視の分類、ドメイン適応、共変量シフトに有効である（Zadrozny et al, 2003; Bickel et al, 2009; Sugiyama & Kawanabe, 2012）。
We adapt ERM to our setting by realizing that Eq.(1) corresponds to an expected loss (i.e.risk) over the data generating process P(O|P).
式(1)がデータ生成過程(=傾向スコアで条件付けられた、観測データOの確率分布)P(O|P)に対する期待損失（＝リスク）に相当することを理解することで、ERMを我々の設定に適応する.
Given a sample from P(O|P), we can think of the IPS estimator from Eq.(10) as the Empirical Risk Rˆ(Yˆ ) that estimates R(Yˆ ) for any Yˆ .
P(O|P)からのサンプルが与えられたとき、式(10)のIPS推定量は、任意のYˆに対してR(Yˆ )を推定するEmpirical Risk Rˆ(Yˆ )と考えることができます。

Definition 4.1 (Propensity-Scored ERM for Recommendation).
定義 4.1 (Propensity-Scored ERM for Recommendation)。
Given training observations O from Y with marginal propensities P, given a hypothesis space H of predictions Yˆ , and given a loss function δu,i(Y, Yˆ ), ERM selects the Yˆ ∈ H that optimizes:
$Y$ から周辺傾向確率 $P$ を持つ学習観測 $O$ が与えられ、予測 $\hat{Y}$ の仮説空間 $H$ が与えられ、損失関数 $\delta_{u,i}(Y, \hat{Y})$ が与えられると、ERMは最適化する $\hat{Y} \in H$ を選択する：

$$
\hat{Y}^{ERM} = \argmin_{\hat{Y} \in H} (\hat{R}_{IPS}(\hat{Y}|P))
\tag{12}
$$

Using the SNIPS estimator does not change the argmax.
SNIPS推定器を使ってもargmaxは変わりません。
To illustrate the validity of the propensity-scored ERM approach, we state the following generalization error bound (proof in appendix) similar to Cortes et al.(2010).
傾向スコア付きERMアプローチの有効性を示すために、Cortes et al(2010)と同様に、以下の一般化誤差境界を述べる（証明は付録）。
We consider only finite H for the sake of conciseness.
ここでは簡潔にするため、有限のHのみを考える。

Theorem 4.2 (Propensity-Scored ERM Generalization Error Bound).
定理4.2（傾向スコア付きERMの一般化誤差の境界）。
For any finite hypothesis space of predictions H = {Yˆ 1, ..., Yˆ |H|} and loss 0 ≤ δu,i(Y, Yˆ ) ≤ ∆, the true risk R(Yˆ ) of the empirical risk minimizer Yˆ ERM from H using the IPS estimator, given training observations O from Y with independent Bernoulli propensities P, is bounded with probability 1 − η by:
任意の有限の予測仮説空間 $H＝{\hat{Y}_1, ..., \hat{Y}_{|H|}}$ と損失0≦δu,i（Y, Yˆ ）≦△ に対して、独立したベルヌーイ予言Pを持つYからの訓練観測Oが与えられたとき、IPS推定器を用いたHからの経験的リスク最小化器Yˆ ERMの真のリスクR（Yˆ ）が確率1 - ηで次によって境界されます：

$$
\tag{13}
$$

## 4.2. Propensity-Scored Matrix Factorization 傾向スコア化行列因子法

We now use propensity-scored ERM to derive a matrix factorization method for the problem of rating prediction.
次に、傾向スコア付きERMを用いて、格付け予測の問題に対する行列分解法を導出する.
Assume a standard rank-d-restricted and L2-regularized matrix factorization model Yˆ u,i = v T u wi+au+bi+c with user, item, and global offsets as our hypothesis space H.
仮説空間Hとして、ユーザ、アイテム、グローバルオフセットを持つ標準的なランクd制限・L2正則化行列分解モデル $\hat{Y}_{u,i} = v^T_{u} w_{i} + a_{u} + b_{i} + c$ を仮定する.
Under this model, propensity-scored ERM leads to the following training objective:
このモデルの下では、傾向スコア付きERMは次のようなトレーニング目的を導く：

$$
\argmin_{V,W,A}[\sum_{O_{u,i}=1} \frac{\delta_{u,i}(Y, V^TW+A)}{P_{u,i}} + \lambda(|V|^2_F + |W|^2_F)]
\tag{14}
$$

where A encodes the offset terms and Yˆ ERM = V T W+A.
ここで、Aはオフセット項(定数項、bais項)を符号化し、 $\hat{Y}^{ERM} = V^TW + A$ である.
Except for the propensities Pu,i that act like weights for each loss term, the training objective is identical to the standard incomplete matrix factorization objective (Koren, 2008; Steck, 2010; Hu et al., 2008) with MSE (using Eq.(3)) or MAE (using Eq.(2)).
各損失項の重みのように働く傾向 $P_{u,i}$ を除いて、学習目的は、MSE（式（3）を使用）またはMAE（式（2）を使用）による**標準的な不完全行列分解の目的関数（Koren、2008；Steck、2010；Hu et al、2008）と同一**である.
So, we can readily draw upon existing optimization algorithms (i.e., Gemulla et al., 2011; Yu et al., 2012) that can efficiently solve the training problem at scale.
そのため、スケールアップしたトレーニング問題を効率的に解決できる既存の最適化アルゴリズム（Gemulla et al.
For the experiments reported in this paper, we use Limited-memory BFGS (Byrd et al., 1995).
本稿で報告する実験では、Limited-memory BFGS (Byrd et al., 1995)を使用した。
Our implementation is available online3 .
私たちの実装はオンラインで公開されています3 。

Conventional incomplete matrix factorization is a special case of Eq.(14) for MCAR (Missing Completely At Random) data, i.e., all propensities Pu,i are equal.
従来の不完全行列分解は、MCAR（Missing Completely At Random）データに対する式（14）の特殊な場合、すなわち、**すべての傾向 P\_{u,i} が等しい場合**である。
Solving this training objective for other δu,i(Y, Yˆ ) that are nondifferentiable is more challenging, but possible avenues exist (Joachims, 2005; Chapelle & Wu, 2010).
非微分である他の $\delta_{u,i}(Y, \hat{Y})$ に対してこの訓練目的を解くことはより困難であるが、可能な道は存在する（Joachims, 2005; Chapelle & Wu, 2010.）
Finally, note that other recommendation methods (e.g., Weimer et al., 2007; Lin, 2007) can in principle be adapted to propensity scoring as well.
最後に、**他の推薦法（例えばWeimer et al., 2007; Lin, 2007）も原理的には傾向性スコアリングに適応できること**に留意してください。

# 5. Propensity Estimation for Observational Data 観察データに対する傾向推定法

We now turn to the Observational Setting where propensities need to be estimated.
次に、**propensities の推定が必要なObservational Setting**に移ります。
One might be worried that we need to perfectly reconstruct all propensities for effective learning.
効果的な学習のために、すべての性質を完璧に再構築する必要があるのではないかと心配されるかもしれません。
However, as we will show, we merely need estimated propensities that are “better” than the naive assumption of observations being revealed uniformly, i.e., P = |{(u, i) : Ou,i = 1}|/ (U · I) for all users and items.
しかし、これから示すように、我々は、**観測結果が一様に明らかになるという素朴(naive)な仮定よりも「良い」推定されたpropensitiesを必要としているだけ**である。(i.e. 全てのユーザとアイテムについて $P = |{(u, i) : O_{u,i} = 1}|/ (U \cdot I)$)
The following characterizes “better” propensities in terms of the bias they induce and their effect on the variability of the learning process.
以下では、「より良い」propensities について、それが誘発するバイアスと、学習プロセスの変動に対する効果の観点から特徴付ける。

Lemma(補足) 5.1 (Bias of IPS Estimator under Inaccurate Propensities).
レンマ5.1（**不正確なPropensities の下でのIPS推定器のバイアス**）。
Let P be the marginal probabilities of observing an entry of the rating matrix Y , and let Pˆ be the estimated propensities such that Pˆ u,i > 0 for all u, i.
評価行列Yのエントリを観測する周辺確率をPとし、すべてのu, iに対して$\hat{P}_{u,i} > 0$となるようなpropensity推定量を$\hat{P}$とする.
The bias of the IPS estimator Eq.(10) using Pˆ is
Pˆを用いたIPS推定量式(10)のバイアスは、以下の通り。

$$
bias(\hat{R}_{IPS}(\hat{Y}|\hat{P})) = \sum_{u,i} \frac{\delta_{u,i}(Y, \hat{Y})}{UI} [1 - \frac{P_{u,i}}{\hat{P}_{u,i}}]
\tag{15}
$$

In addition to bias, the following generalization error bound (proof in appendix) characterizes the overall impact of the estimated propensities on the learning process.
バイアスに加えて、以下の一般化誤差境界（証明は付録）は、推定された傾向が学習過程に与える全体的な影響を特徴づける.

Theorem 5.2 (Propensity-Scored ERM Generalization Error Bound under Inaccurate Propensities).
定理5.2（不正確な予感の下での傾向スコア付きERM汎化誤差の境界）。
For any finite hypothesis space of predictions H = {Yˆ 1, ..., Yˆ |H|}, the transductive prediction error of the empirical risk minimizer Yˆ ERM, using the IPS estimator with estimated propensities Pˆ (Pˆ u,i > 0) and given training observations O from Y with independent Bernoulli propensities P, is bounded by:
予測値H＝｛Yˆ 1, ..., Yˆ |H｝の任意の有限仮説空間に対して、推定傾向 Pˆ（Pˆ u,i > 0）を有するIPS推定器を用い、独立ベルヌーイ予兆Pを有するYからの訓練観測値Oが与えられた場合の経験的リスク最小化器Yˆ ERMの伝達予測誤差は、次式で境界付けられる：

$$
R(\hat{Y}^{ERM}) \leq \hat{R}_{IPS}(\hat{Y}^{ERM}|\hat{P}) + \frac{\Delta}{UI}\sum_{u,i} |1 - \frac{P_{u,i}}{\hat{P}_{u,i}}|
\\
+ \frac{\Delta}{UI} \sqrt{\frac{log(2|H| / \nu)}{2}} \sqrt{\sum_{u,i}\frac{1}{\hat{P}_{u,i}^2}}
\tag{16}
$$

The bound shows a bias-variance trade-off that does not occur in conventional ERM.
このバウンドは、従来のERMでは生じなかったバイアスとバリアンスのトレードオフを示すものである。(biasを小さくしようとするとbarianceが大きくなる?)
In particular, the bound suggests that it may be beneficial to overestimate small propensities, if this reduces the variability more than it increases the bias.
特に、この境界は、バイアスを増加させるよりも変動を減少させる方が、小さな予感を過大評価することが有益であることを示唆する。

## 5.1. Propensity Estimation Models. プロペンシティ・エスティメーション・モデル

Recall that our goal is to estimate the probabilities Pu,i with which ratings for user u and item i will be observed.
**我々の目的は、ユーザーuとアイテムiの評価が観測される確率Pu,iを推定すること**であることを思い出してください。
In general, the propensities
一般に、propensities は

$$
P_{u,i} = P(O_{u,i} = 1| X, X^{hid}, Y)
\tag{17}
$$

can depend on some observable features X (e.g., the predicted rating displayed to the user), unobservable features Xhid (e.g., whether the item was recommended by a friend), and the ratings Y .
は、観測可能な特徴X（例えば、ユーザに表示される予測評価）、観測不可能な特徴$X^{hid}$（例えば、アイテムが友人によって推薦されたかどうか）、および評価$Y$に依存している可能性がある。
It is reasonable to assume that Ou,i is independent of the new predictions Yˆ (and therefore independent of δu,i(Y, Yˆ )) once the observable features are taken into account.
観測可能な特徴が考慮されれば、$O_{u,i}$は新しい予測値$\hat{Y}$に依存しない（したがって、δu,i（Y, Yˆ ）にも依存しない）と考えるのが妥当である。(??)
The following outlines two simple propensity estimation methods, but there is a wide range of other techniques available (e.g., McCaffrey et al., 2004) that can cater to domain-specific needs.
以下では**2つの簡単な傾向推定法**を概説するが、ドメイン固有のニーズに対応できる他の技法も幅広く存在する（例：McCaffrey et al, 2004）。

### 5.1.1. Propensity Estimation via Naive Bayes. ナイーブベイズによる傾向推定を行う。

The first approach estimates $P(O_{u,i}|X, Xhid, Y)$ by assuming that dependencies between covariates X, Xhid and other ratings are negligible.
最初のアプローチは、**共変量 X、Xhidと他の評価Yとの間の依存関係が無視できると仮定**(=> i.e.)して、$P(O_{u,i}|X, Xhid, Y)$を推定する。(要するにMCARなデータ?とは違うか...!)
Eq.(17) then reduces to P(Ou,i|Yu,i) similar to Marlin & Zemel (2009).
式(17)は、Marlin & Zemel (2009)と同様に、$P(O_{u,i}|Y_{u,i})$に還元されます。
We can treat Yu,i as observed, since we only need the propensities for observed entries to compute IPS and SNIPS.
IPSとSNIPSの計算には、**観測されたエントリ{u,i}の傾向スコアのみが必要**なので、**(全ての!)Yu,iは観測されたものとして扱うことができる**.
This yields the Naive Bayes propensity estimator:
これにより、ナイーブベイズの傾向推定器が得られる：

$$
P(O_{u,i} = 1|Y_{u,i} = r) = \frac{P(Y=r|O=1)P(O=1)}{P(Y=r)}
\tag{18}
$$

We dropped the subscripts to reflect that parameters are tied across all u and i.
パラメータがすべてのuとiで結ばれていることを反映するために、添え字を削除した。(i.e. MNARデータにおいて、全ての{u,i}ペアで$P(Y=r|O=1)$も$P(O=1)$も等しいはずだから...??)
Maximum likelihood estimates for P(Y = r | O = 1) and P(O = 1) can be obtained by counting observed ratings in MNAR data.
$P(Y=r｜O=1)$とP(O=1)の最尤推定値は、**MNARデータで観測された評価を数えることで得ることができる**.(シンプルに割り算で推定できる?)
However, to estimate P(Y = r), we need a small sample of MCAR data.
しかし、P(Y = r)を推定するためには、MCARデータの少量サンプルが必要です。

### 5.1.2. Propensity Estimation via Logistic Regression ロジスティック回帰による傾向推定

The second propensity estimation approach we explore (which does not require a sample of MCAR data) is based on logistic regression and is commonly used in causal inference (Rosenbaum, 2002).
私たちが探求する**2つ目の傾向推定アプローチ（MCARデータのサンプルを必要としない）は、ロジスティック回帰に基づくもの**で、**因果推論によく使われる**ものです。
It also starts from Eq.(17), but aims to find model parameters φ such that O becomes independent of unobserved Xhid and Y , i.e., P(Ou,i|X, Xhid, Y ) = P(Ou,i|X, φ).
これも式(17)から出発するが、**Oが未観測のXhidとYに依存しなくなるようなモデルパラメータφ**、すなわち $P(O_{u,i}|X, X_{hid}, Y) = P(O_{u,i}|X, φ)$ を見つけることを目的としている.
The main modeling assumption is that there exists a φ = (w, β, γ) such that $P_{u,i} = \sigma(w^T X_{u,i} + \beta_{i} + \gamma_{u})$.
主なモデリングの仮定は、$P_{u,i} = \sigma(w^T X_{u,i} + \beta_{i} + \gamma_{u})$ となるようなφ = (w, β, γ) が存在することである.
Here, Xu,i is a vector encoding all observable information about a user-item pair (e.g., user demographics, whether an item was promoted, etc.), and σ(·) is the sigmoid function.
ここで、$X_{u,i}$は、ユーザとアイテムのペアに関するすべての観測可能な情報(例えば、ユーザーのデモグラフィック、アイテムがプロモーションされたかどうかなど)を符号化したベクトルで、$\sigma()$はシグモイド関数です。
βi and γu are peritem and per-user offsets.
$\beta_{i}$、$\gamma_{u}$は、アイテム単位、ユーザ単位のオフセットである.

# 6. Empirical Evaluation 実証的評価

We conduct semi-synthetic experiments to explore the empirical performance and robustness of the proposed methods in both the experimental and the observational setting.
半合成実験を行い、experimental setting と observational setting の両方で提案手法の経験的性能とロバスト性を探る.
Furthermore, we compare against the state-of-theart joint-likelihood method for MNAR data (Hernandez- ´ Lobato et al., 2014) on real-world datasets.
さらに、実世界のデータセットにおいて、**MNAR(Missing Not At Random)データに対する最先端の共同尤度法**（Hernandez- ´ Lobato et al, 2014）と比較しました.

## 6.1. Experiment Setup 実験セットアップ

In all experiments, we perform model selection for the regularization parameter λ and/or the rank of the factorization $d$ via cross-validation as follows.
すべての実験において、正則化パラメータ**λ**および/または因数分解のランク**d**のモデル選択を、以下のようにクロスバリデーションで行う.(２つのハイパーパラメータを最適化する問題っぽい.)
We randomly split the observed MNAR ratings into k folds (k = 4 in all experiments), training on k − 1 and evaluating on the remaining one using the IPS estimator.
観測されたMNAR評価をランダムにk個のフォールド（すべての実験でk = 4）に分割し、k - 1で訓練し、残りの1つでIPS推定量を用いて評価した. (あ、foldってk分割交差検証の1ブロックの事だったのかな.)
Reflecting this additional split requires scaling the propensities in the training folds by k−1 k and those in the validation fold by 1 k .
この追加分割を反映させるためには，訓練フォールドのpropensitiesをk-1/k倍，検証フォールドのpropensitiesを1/k倍で**スケーリング**する必要があります.
The parameters with the best validation set performance are then used to retrain on all MNAR data.
その後、**検証セットのパフォーマンスが最も良いパラメータを使用して、すべてのMNARデータで再トレーニングを行い**ます。
We finally report performance on the MCAR test set for the real-world datasets, or using Eq.(1) for our semi-synthetic dataset.
最後に、実世界のデータセットについてはMCAR(Missing Completely At Random)テストセット、半合成データセットについては式(1)を用いた性能を報告します。

## 6.2. How does sampling bias severity affect evaluation? サンプリングバイアスの厳しさは評価にどう影響するのか？

First, we evaluate how different observation models impact the accuracy of performance estimates.
まず、observationモデルの違いが性能推定精度にどのような影響を与えるかを評価します。
We compare the Naive estimator of Eq.(5) for MSE, MAE and DCG with their propensity-weighted analogues, IPS using Eq.(10) and SNIPS using Eq.(11) respectively.
式(5)のナイーブ推定器を、MSE、MAE、DCG(精度指標)について、それぞれ式(10)を用いたIPS、式(11)を用いたSNIPSのような傾向性重み付けをしたものと比較する。
Since this experiment requires experimental control of sampling bias, we created a semi-synthetic dataset and observation model.
この実験ではサンプリングバイアスを実験的に制御する必要があるため、半合成データセットと観測モデルを作成しました。

ML100K Dataset.
ML100K Dataset。

The ML100K dataset4 provides 100K MNAR ratings for 1683 movies by 944 users.
ML100Kデータセット4は、944人のユーザーによる1683本の映画に対する100KのMNAR(Missing Not At Random)レーティングを提供します。
To allow ground-truth evaluation against a fully known rating matrix, we complete these partial ratings using standard matrix factorization.
完全に既知の評価行列に対する真実の評価を可能にするため、標準的な行列分解を用いてこれらの部分評価を完成させます。
The completed matrix, however, give unrealistically high ratings to almost all movies.
しかし、完成したマトリックスでは、ほとんどすべての映画に非現実的な高評価を与えている。
We therefore adjust ratings for the final Y to match a more realistic rating distribution [p1, p2, p3, p4, p5] for ratings 1 to 5 as given in Marlin & Zemel (2009) as follows: we assign the bottom p1 fraction of the entries by value in the completed matrix a rating of 1, and the next p2 fraction of entries by value a rating of 2, and so on.
そこで、Marlin & Zemel (2009)で示された、より現実的なレーティング1〜5の分布 [p1, p2, p3, p4, p5] に合うように、最終Yのレーティングを調整します。完成マトリックスの値による項目のうち、一番下のp1の割合を1、次のp2の割合を2、といったようにレーティングに割り当てます。
Hyper-parameters (rank d and L2 regularization λ) were chosen by using a 90-10 train-test split of the 100K ratings, and maximizing the 0/1 accuracy of the completed matrix on the test set.
ハイパーパラメータ（ランクdとL2正則化λ）は、10万件の評価を90対10で訓練-テスト分割し、テストセットで完成した行列の0/1精度を最大化することで選択した。

ML100K Observation Model.
ML100K観察モデル。

If the underlying rating is 4 or 5, the propensity for observing the rating is equal to k.
基礎となる評価が4または5であれば、その評価を観察する propensity はkに等しい.
For ratings r < 4, the corresponding propensity is kα4−r .
rating r < 4 の場合、対応する propensity は $k \alpha^{4-r}$ です.
For each α, k is set so that the expected number of ratings we observe is 5% of the entire matrix.
各 $\alpha$ について、観察する評価の期待数が行列全体の5％となるようにkを設定する.
By varying α > 0, we vary the MNAR effect: α = 1 is missing uniformly at random (MCAR), while α → 0 only reveals 4 and 5 rated items.
α＞0を変化させることで、MNAR効果を変化させている。α＝1は一様にランダムに欠落した状態（MCAR）、α→0は4と5の評価項目のみを明らかにする。
Note that α = 0.25 gives a marginal distribution of observed ratings that reasonably matches the observed MNAR rating marginals on ML100K ([0.06, 0.11, 0.27, 0.35, 0.21] in the real data vs.
なお、α=0.25は、ML100Kで観測されたMNARの評価マージン（実データでは[0.06, 0.11, 0.27, 0.35, 0.21] vs. ML100K）と適度に一致する評価マージン分布を与える.
[0.06, 0.10, 0.25, 0.42, 0.17] in our model).
[我々のモデルでは［0.06, 0.10, 0.25, 0.42, 0.17］）。

Results.
結果が出ました。

![](https://camo.qiitausercontent.com/762bf0e8c16917dec2cf1992fc2c9c9e61791624/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f39383535356361352d396637612d633465342d666266662d3531363531653231393536332e706e67)

Table 1, described in Section 3.4, shows the estimated MAE and DCG@50 when α = 0.25.
3.4節で説明した表1は、α=0.25のときのMAEとDCG@50の推定値である。
Next, we vary the severity of the sampling bias by changing α ∈ (0, 1].
次に、**α∈(0, 1)を変化させることで、サンプリングバイアスの深刻度を変化させます**。($\alpha$は人工データ生成のバイアスをコントロールする実験用のパラメータか...!!)
Figure 2 reports how accurately (in terms of root mean squared estimation error (RMSE)) each estimator predicts the true MSE and DCG respectively.
図2は、各推定器が真のMSEとDCGをそれぞれどの程度正確に（二乗平均平方根推定誤差（RMSE）で）予測したかを報告している。
These results are for the Experimental Setting where propensities are known.
**この結果は、propensities がわかっているExperimental Setting での結果**です。
They are averages over the five prediction matrices Yˆ i given in Section 3.4 and across 50 trials.
これらは、3.4節で示した5つの予測行列Yˆiの平均値であり、50回の試行にわたる平均値である.
Shaded regions indicate a 95% confidence interval.
斜線部は95％信頼区間を示す。

![](https://camo.qiitausercontent.com/e1e3490d7c9d39dc058b5e07bb11686e38684f36/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f38373061353636352d633538632d306532612d643031642d6339663537353265646334332e706e67)

Over most of the range of α, in particular for the realistic value of α = 0.25, the IPS and SNIPS estimators are orders-of-magnitude more accurate than the Naive estimator.
αのほとんどの範囲において、特に現実的な値であるα=0.25では、**IPSとSNIPSの推定値はNaive推定値よりも桁違いに高い精度を示しています**。
Even for severely low choices of α, the gain due to bias reduction of IPS and SNIPS still outweighs the added variability compared to Naive.
αを極端に小さくした場合でも(バイアスがほとんどない場合でも)、IPSとSNIPSのバイアス低減による利得は、Naiveと比較して追加された変動を上回った。
When α = 1 (MCAR), SNIPS is algebraically equivalent to Naive, while IPS pays a small penalty due to increased variability from propensity weighting.
α=1（MCAR）の場合、SNIPSは代数的にNaiveと同等であるが、IPSは傾向重み付けによる変動が大きくなるため、小さなペナルティを支払う。
For MSE, SNIPS consistently reduces estimation error over IPS while both are tied for DCG.
MSEについては、SNIPSはIPSよりも一貫して推定誤差を低減しているが、DCGについては両者が同点である。

## 6.3. How does sampling bias severity affect learning? サンプリングバイアスの厳しさは学習にどう影響するのか？

![](https://camo.qiitausercontent.com/a0297beaca6d40d6a737d171be3c849b91b9e101/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32636334646664632d346464612d623964642d626235662d6231313562663637363435352e706e67)

Now we explore whether these gains in risk estimation accuracy translate into improved learning via ERM, again in the Experimental Setting.
次に、このようなリスク(=誤差関数の事?)推定精度の向上が、**ERMによる学習効果の向上につながるかどうか**を、再びExperimental Setting で検証してみる。
Using the same semi-synthetic ML100K dataset and observation model as above, we compare our matrix factorization MF-IPS with the traditional unweighted matrix factorization MF-Naive.
上記と同じ半合成ML100Kデータセットと観測モデルを用いて、我々の**行列分解MF-IPSと従来の重み付けなし行列分解MF-Naiveを比較**します。
Both methods use the same factorization model with separate λ selected via cross-validation and d = 20.
両手法とも、クロスバリデーションによって選択された別々のλと、d = 20を持つ同じ因数分解モデルを使用する。
The results are plotted in Figure 3 (left), where shaded regions indicate 95% confidence intervals over 30 trials.
結果は図3（左）にプロットされており、斜線部分は30回の試行における95％信頼区間を示しています。
The propensity-weighted matrix factorization MF-IPS consistently outperforms conventional matrix factorization in terms of MSE.
傾向性重み付け行列分解MF-IPSは、MSEの点で、従来の行列分解を常に上回る。
We also conducted experiments for MAE, with similar results.
また、MAEについても実験を行いましたが、同様の結果が得られました。

## 6.4. How robust is evaluation and learning to inaccurately learned propensities?

We now switch from the Experimental Setting to the Observational Setting, where propensities need to be estimated.
ここで、Experimental Settingから Observational Setting に切り替える. この場合、propensities を推定する必要がある.
To explore robustness to propensity estimates of varying accuracy, we use the ML100K data and observation model with α = 0.25.
様々な精度の propensity 推定に対する頑健性を調べるために、ML100Kデータとα=0.25の観測モデルを使用した.
To generate increasingly bad propensity estimates, we use the Naive Bayes model from Section 5.1, but vary the size of the MCAR sample for estimating the marginal ratings P(Y = r) via the Laplace estimator.
ますます悪い propensity 推定値を生成するために，5.1節のナイーブベイズモデルを使用するが，ラプラス推定量による限界視聴率P（Y = r）を推定するためのMCARサンプルの大きさを変える.

Figure 4 shows how the quality of the propensity estimates impacts evaluation using the same setup as in Section 6.2.Under no condition do the IPS and SNIPS estimator perform worse than Naive.
図4は、6.2節と同じ設定を用いて、propensity 推定の品質が評価にどのような影響を与えるかを示したものである。
Interestingly, IPS-NB with estimated propensities can perform even better than IPS-KNOWN with known propensities, as can be seen for MSE.
興味深いことに、propensities 推定したIPS-NBは、MSEでわかるように、予感がわかっているIPS-KNOWNよりもさらに優れた性能を発揮することができます。
This is a known effect, partly because the estimated propensities can provide an effect akin to stratification (Hirano et al., 2003; Wooldridge, 2007).
これは、**推定された propensities が層別化のような効果をもたらす**こともあり、知られている効果である（Hirano et al, 2003; Wooldridge, 2007）。

Figure 3 (right) shows how learning performance is affected by inaccurate propensities using the same setup as in Section 6.3.We compare the MSE prediction error of MFIPS-NB with estimated propensities to that of MF-Naive and MF-IPS with known propensities.
図3（右）は、6.3節と同じ設定で、propensities が不正確な場合に学習性能にどのような影響があるかを示している。propensities を推定したMFIPS-NBのMSE予測誤差を、propensities が分かっているMF-NaiveとMF-IPSと比較している。
The shaded area shows the 95% confidence interval over 30 trials.
網掛け部分は、30回の試行における95％信頼区間を示しています。
Again, we see that MF-IPS-NB outperforms MF-Naive even for severely degraded propensity estimates, demonstrating the robustness of the approach.
ここでも、MF-IPS-NBは、著しく劣化した(MCARの観測データ数が少ない為...!)propensities推定値に対してもMF-Naiveを上回り、アプローチの頑健性を実証していることがわかる。

## 6.5. Performance on Real-World Data 実世界のデータにおける性能

Our final experiment studies performance on real-world datasets.
最後の実験では、実世界のデータセットにおけるパフォーマンスを調査します.(ついにオンライン実験)
We use the following two datasets, which both have a separate test set where users were asked to rate a uniformly drawn sample of items.
以下の2つのデータセットを使用する。これらはどちらも、ユーザに一様に描かれたアイテムのサンプルを評価するよう求められた別のテストセットを持っている。

### Yahoo! R3 Dataset.

Yahoo! R3 Datasetを使用しています。
This dataset5 (Marlin & Zemel, 2009) contains user-song ratings.
このデータセット5 (Marlin & Zemel, 2009) は、ユーザーによる楽曲の評価を含んでいる。
The MNAR training set provides over 300K ratings for songs that were selfselected by 15400 users.
MNARのトレーニングセットは、15400人のユーザーによって自選された楽曲に対する30万件以上の評価を提供しています。(学習データはMNARなデータ)
The test set contains ratings by a subset of 5400 users who were asked to rate 10 randomly chosen songs.
テストセットは、ランダムに選ばれた10曲を評価するよう求められた5400人のユーザーのサブセットによる評価を含んでいます。(即ち、テストデータは完全なMCARデータ)
For this data, we estimate propensities via Naive Bayes.
このデータに対して、ナイーブベイズでpropensitiesを推定しています。
As a MCAR sample for eliciting the marginal rating distribution, we set aside 5% of the test set and only report results on the remaining 95% of the test set.
marginal rating distribution(周辺評価分布?)を引き出すためのMCARサンプルとして、テストセットの5%を確保し、残りの95%のテストセットについてのみ結果を報告します。(現実世界でこの5%をどうやって確保したら良いんだろう...)

### Coat Shopping Dataset.

コートショッピングのデータセット。
We collected a new dataset6 simulating MNAR data of customers shopping for a coat in an online store.
オンラインストアでコートを購入する顧客のMNARデータをシミュレートした新しいデータセット6を収集しました。
The training data was generated by giving Amazon Mechanical Turkers a simple web-shop interface with facets and paging.
学習データは、Amazon Mechanical Turkersにファセットとページングを備えたシンプルなウェブショップのインターフェイスを与えることで作成した。
They were asked to find the coat in the store that they wanted to buy the most.
店内で一番買いたいコートを探してもらうというものでした。
Afterwards, they had to rate 24 of the coats they explored (self-selected) and 16 randomly picked ones on a five-point scale.
その後、自分が探検したコート（自選）24点とランダムに選んだコート16点を5点満点で評価することになりました。
The dataset contains ratings from 290 Turkers on an inventory of 300 items.
データセットには、300のアイテムに対する290人のトルコ人の評価が含まれています。
The self-selected ratings are the training set and the uniformly selected ratings are the test set.
自己選択した評価をトレーニングセット、一律に選択した評価をテストセットとする。
We learn propensities via logistic regression based on user covariates (gender, age group, location, and fashion-awareness) and item covariates (gender, coat type, color, and was it promoted).
ユーザーの共変量（性別、年齢層、場所、ファッション意識）とアイテムの共変量（性別、コートの種類、色、昇進したか）に基づき、ロジスティック回帰でpropensitiesを学習します。
A standard regularized logistic regression (Pedregosa et al., 2011) was trained using all pairs of user and item covariates as features and cross-validated to optimize log-likelihood of the self-selected observations.
標準的な正則化ロジスティック回帰（Pedregosa et al, 2011）は、ユーザーとアイテムの共変量のすべてのペアを特徴として使用して訓練し、自己選択した観測の対数尤度(ハイパーパラメータだっけ?)を最適化するためにクロスバリデーションを行いました。

### Results.

![](https://camo.qiitausercontent.com/37bd3505292d250c39b84dd3d246171271029c6f/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f65623231363364642d633531342d383136352d373666352d3235333830626234326564362e706e67)

結果が出ました。
Table 2 shows that our propensity-scored matrix factorization MF-IPS with learnt propensities substantially and significantly outperforms the conventional matrix factorization approach, as well as the Bayesian imputation models from (Hernandez-Lobato et al.´ , 2014), abbreviated as HL-MNAR and HL-MAR (paired t-test, p < 0.001 for all).
表2より，学習させた傾向スコアを用いた行列分解MF-IPSは，従来の行列分解アプローチや，HL-MNARやHL-MARと略される（Hernandez-Lobato et al.´ , 2014）のベイズインピュテーションモデルを大幅に上回った（paired t-test, p < 0.001 for all）．
This holds for both MAE and MSE.
これは、MAEとMSEの両方で成立します。
Furthermore, the performance of MF-IPS beats the best published results for Yahoo in terms of MSE (1.115) and is close in terms of MAE (0.770) (the CTP-v model of (Marlin & Zemel, 2009) as reported in the supplementary material of Hernandez- ´ Lobato et al.(2014)).
さらに、MF-IPSの性能は、MSE（1.115）の点でYahooの最高の公表結果を上回り、MAE（0.770）の点で近い（Hernandez- ´ Lobato et al（2014）の補足資料で報告されている（Marlin & Zemel, 2009）CTP-v model）となっています。
For MF-IPS and MF-Naive all hyperparameters (i.e., λ ∈ {10−6 , ..., 1} and d ∈ {5, 10, 20, 40}) were chosen by cross-validation.
MF-IPSとMF-Naiveについては、すべてのハイパーパラメータ（すなわち、λ∈{10-6 , ..., 1}とd∈{5, 10, 20, 40}）をクロスバリデーションによって選択した。
For the HL baselines, we explored d ∈ {5, 10, 20, 40} using software provided by the authors7 and report the best performance on the test set for efficiency reasons.
HLベースラインについては，著者らから提供されたソフトウェアを用いてd∈{5, 10, 20, 40}を探索し，効率化のためにテストセットで最高の性能を報告した．
Note that our performance numbers for HL on Yahoo closely match the values reported in (Hernandez-Lobato et al.´ , 2014).
なお、YahooでのHLのパフォーマンス数値は、(Hernandez-Lobato et al.´ , 2014)の報告値とほぼ一致しています。

Compared to the complex generative HL models, we conclude that our discriminative MF-IPS performs robustly and efficiently on real-world data.
**複雑な生成HLモデルと比較して、我々の識別MF-IPSは実世界のデータにおいて頑健かつ効率的な性能を発揮すると結論付けている。**
We conjecture that this strength is a result of not requiring any generative assumptions about the validity of the rating model.
この強みは、レーティングモデルの妥当性に関する生成的な仮定を必要としない結果であると推測しています。
Furthermore, note that there are several promising directions for further improving performance, like propensity clipping (Strehl et al., 2010), doubly-robust estimation (Dud´ık et al., 2011), and the use of improved methods for propensity estimation (McCaffrey et al., 2004).
さらに、propensity クリッピング（Strehl et al., 2010）、ダブルロバスト推定（Dud´ık et al., 2011）、**propensity推定のための改良された手法**の使用（McCaffrey et al., 2004）など、**さらなる性能向上のための有望な方向性がいくつか存在する**ことに留意してください。

# 7. Conclusions 結論

We proposed an effective and robust approach to handle selection bias in the evaluation and training of recommender systems based on propensity scoring.
**傾向スコアリングに基づく推薦システムの評価・学習**において、選択バイアスを効果的かつ頑健に扱うアプローチを提案した。
The approach is a discriminative alternative to existing joint-likelihood methods which are generative.
このアプローチは、生成的である既存の合同尤度法に代わる識別的な方法である。
It therefore inherits many of the advantages (e.g., efficiency, predictive performance, no need for latent variables, fewer modeling assumptions) of discriminative methods.
そのため、識別法の利点（効率性、予測性能、潜在変数が不要、モデル化の仮定が少ないなど）を多く受け継いでいます。
The modularity of the approach— separating the estimation of the assignment model from the rating model—also makes it very practical.
また、割り当てモデルの推定と評価モデルの推定を分離したモジュール方式を採用しているため、非常に実用的です。
In particular, any conditional probability estimation method can be plugged in as the propensity estimator, and we conjecture that many existing rating models can be retrofit with propensity weighting without sacrificing scalability.
特に、どのような条件付き確率推定法(=任意のXからP(y|X)を推定するモデル?)でもprobability推定器として差し込むことができ、既存の多くのレーティングモデルが拡張性を犠牲にすることなく傾向重み付けを後付けできることが推測されます。
