
# An Empirical Evaluation of Thompson Sampling  
**Olivier Chapelle**  
Yahoo! Research  
Santa Clara, CA  
chap@yahoo-inc.com  
**Lihong Li**  
Yahoo! Research  
Santa Clara, CA  
lihong@yahoo-inc.com  

# トンプソンサンプリングの実証評価  
**オリビエ・シャペル**  
Yahoo! Research  
サンタクララ, CA  
chap@yahoo-inc.com  
**リホン・リー**  
Yahoo! Research  
サンタクララ, CA  
lihong@yahoo-inc.com  



## Abstract 要約

Thompson sampling is one of oldest heuristic to address the exploration / exploitation trade-off, but it is surprisingly unpopular in the literature. 
トンプソンサンプリングは、探索と活用のトレードオフに対処するための最も古いヒューリスティックの一つですが、文献では驚くほど人気がありません。
We present here some empirical results using Thompson sampling on simulated and real data, 
ここでは、シミュレーションデータと実データを用いたトンプソンサンプリングのいくつかの実証結果を示します、
and show that it is highly competitive. 
そして、それが非常に競争力があることを示します。
And since this heuristic is very easy to implement, we argue that it should be part of the standard baselines to compare against. 
このヒューリスティックは非常に実装が簡単であるため、比較のための標準的なベースラインの一部であるべきだと主張します。



## 1 Introduction はじめに

Various algorithms have been proposed to solve exploration / exploitation or bandit problems. 
さまざまなアルゴリズムが探索/活用またはバンディット問題を解決するために提案されています。 
One of the most popular is Upper Confidence Bound or UCB [7, 3], for which strong theoretical guarantees on the regret can be proved. 
最も人気のあるアルゴリズムの一つは、Upper Confidence Bound（UCB）[7, 3]であり、これに対しては後悔に関する強力な理論的保証が証明できます。 
Another representative is the Bayes-optimal approach of Gittins [4] that directly maximizes expected cumulative payoffs with respect to a given prior distribution. 
もう一つの代表的なアプローチは、Gittins [4] のベイズ最適アプローチであり、これは与えられた事前分布に対して期待累積報酬を直接最大化します。 
A less known family of algorithms is the so-called probability matching. 
あまり知られていないアルゴリズムの一群は、いわゆる確率マッチングです。 
The idea of this heuristic is old and dates back to [16]. 
このヒューリスティックのアイデアは古く、[16]に遡ります。 
This is the reason why this scheme is also referred to as Thompson_sampling._ 
このため、この手法はThompson_sampling_とも呼ばれます。 

The idea of Thompson sampling is to randomly draw each arm according to its probability of being optimal. 
Thompson samplingのアイデアは、各アームを最適である確率に従ってランダムに引くことです。 
In contrast to a full Bayesian method like Gittins index, one can often implement Thompson sampling efficiently. 
Gittinsインデックスのような完全なベイズ法とは対照的に、Thompson samplingは効率的に実装できることが多いです。 
Recent results using Thompson sampling seem promising [5, 6, 14, 12]. 
Thompson samplingを使用した最近の結果は有望に見えます[5, 6, 14, 12]。 
The reason why it is not very popular might be because of its lack of theoretical analysis. 
それがあまり人気がない理由は、理論的分析が不足しているからかもしれません。 
Only two papers have tried to provide such analysis, but they were only able to prove asymptotic convergence [6, 11]. 
このような分析を提供しようとした論文は2つだけですが、彼らは漸近収束を証明することしかできませんでした[6, 11]。 

In this work, we present some empirical results, first on a simulated problem and then on two real-world ones: display advertisement selection and news article recommendation. 
本研究では、まずシミュレーション問題に関するいくつかの実証結果を示し、次に2つの実世界の問題、すなわちディスプレイ広告の選択とニュース記事の推薦について述べます。 
In all cases, despite its simplicity, Thompson sampling achieves state-of-the-art results, and in some cases significantly outperforms other alternatives like UCB. 
すべてのケースにおいて、その単純さにもかかわらず、Thompson samplingは最先端の結果を達成し、場合によってはUCBのような他の選択肢を大幅に上回ります。 
The findings suggest the necessity to include Thompson sampling as part of the standard baselines to compare against, and to develop finite-time regret bound for this empirically successful algorithm. 
これらの発見は、Thompson samplingを比較のための標準的なベースラインの一部として含める必要性と、この経験的に成功したアルゴリズムの有限時間後悔境界を開発する必要性を示唆しています。



## 2 Algorithm アルゴリズム

The contextual bandit setting is as follows. At each round we have a context x (optional) and a set of actions.  
コンテキストバンディットの設定は次のようになります。各ラウンドで、オプションのコンテキスト $x$ とアクションのセットがあります。

After choosing an action a, we observe a reward r.  
アクション $a$ を選択した後、報酬 $r$ を観察します。

The goal is to find a policy $A \in A$ that selects actions such that the cumulative reward is as large as possible.  
目標は、累積報酬ができるだけ大きくなるようにアクションを選択するポリシー $A \in A$ を見つけることです。

Thompson sampling is best understood in a Bayesian setting as follows.  
トンプソンサンプリングは、ベイズ設定で次のように理解されます。

The set of past observations $D$ is made of triplets $(x_i, a_i, r_i)$ and are modeled using a parametric likelihood function $P(r|a, x, \theta)$ depending on some parameters $\theta$.  
過去の観察のセット $D$ は三つ組 $(x_i, a_i, r_i)$ で構成され、いくつかのパラメータ $\theta$ に依存するパラメトリック尤度関数 $P(r|a, x, \theta)$ を使用してモデル化されます。

Given some prior distribution $P(\theta)$ on these parameters, the posterior distribution of these parameters is given by the Bayes rule, $P(\theta|D) \propto P(r_i|a_i, x_i, \theta)P(\theta)$.  
これらのパラメータに対する事前分布 $P(\theta)$ が与えられると、これらのパラメータの事後分布はベイズの定理により、$P(\theta|D) \propto P(r_i|a_i, x_i, \theta)P(\theta)$ で与えられます。

In the realizable case, the reward is a stochastic function of the action, context and the unknown, true parameter $\theta^{[*]}$.  
実現可能な場合、報酬はアクション、コンテキスト、および未知の真のパラメータ $\theta^{[*]}$ の確率的関数です。

Ideally, we would like to choose the action maximizing the expected reward, $\max_a E(r|a, x, \theta^{[*]})$.  
理想的には、期待報酬を最大化するアクションを選択したいです、$\max_a E(r|a, x, \theta^{[*]})$。

Of course, $\theta^{[*]}$ is unknown.  
もちろん、$\theta^{[*]}$ は未知です。

If we are just interested in maximizing the immediate reward (exploitation), then one should choose the action that maximizes $E(r|a, x) = \int E(r|a, x, \theta)P(\theta|D)d\theta$.  
もし私たちが即時報酬を最大化すること（搾取）にのみ関心があるなら、$E(r|a, x) = \int E(r|a, x, \theta)P(\theta|D)d\theta$ を最大化するアクションを選ぶべきです。

But in an exploration / exploitation setting, the probability matching heuristic consists in randomly selecting an action $a$ according to its probability of being optimal.  
しかし、探索/搾取の設定では、確率マッチングヒューリスティックは、最適である確率に従ってアクション $a$ をランダムに選択することから成ります。

That is, action $a$ is chosen with probability  
すなわち、アクション $a$ は次の確率で選ばれます。

$$
P(a) \propto E(r|a, x, \theta) = \int \max_{a'} E(r|a', x, \theta) P(\theta|D) d\theta,
$$  
ここで $I$ は指示関数です。積分は明示的に計算する必要はありません：アルゴリズム1で説明されているように、各ラウンドでランダムパラメータ $\theta$ を引くことが十分です。

Note that the integral does not have to be computed explicitly: it suffices to draw a random parameter $\theta$ at each round as explained in Algorithm 1.  
積分は明示的に計算する必要はありません：アルゴリズム1で説明されているように、各ラウンドでランダムパラメータ $\theta$ を引くことが十分です。

Implementation of the algorithm is thus efficient and straightforward in most applications.  
したがって、アルゴリズムの実装はほとんどのアプリケーションで効率的かつ簡単です。

**Algorithm 1 Thompson sampling**  
**アルゴリズム1 トンプソンサンプリング**

$$
D = \emptyset
$$  
**for $t = 1, \ldots, T$ do**  
**$t = 1, \ldots, T$ の間**  

Receive context $x_t$  
コンテキスト $x_t$ を受け取る

Draw $\theta[t]$ according to $P(\theta|D)$  
$P(\theta|D)$ に従って $\theta[t]$ を引く

Select $a_t = \arg \max_a E(r|x_t, a, \theta[t])$  
$a_t = \arg \max_a E(r|x_t, a, \theta[t])$ を選択する

Observe reward $r_t$  
報酬 $r_t$ を観察する

$$
D = D \cup (x_t, a_t, r_t)  
$$  
**end for**  
**終了**

In the standard K-armed Bernoulli bandit, each action corresponds to the choice of an arm.  
標準的なKアームベルヌーイバンディットでは、各アクションはアームの選択に対応します。

The reward of the i-th arm follows a Bernoulli distribution with mean $\theta_i^{[*]}$.  
i番目のアームの報酬は平均 $\theta_i^{[*]}$ のベルヌーイ分布に従います。

It is standard to model the mean reward of each arm using a Beta distribution since it is the conjugate distribution of the binomial distribution.  
各アームの平均報酬をベータ分布を使用してモデル化するのが標準です。なぜなら、それは二項分布の共役分布だからです。

The instantiation of Thompson sampling for the Bernoulli bandit is given in algorithm 2.  
ベルヌーイバンディットに対するトンプソンサンプリングの具体化はアルゴリズム2に示されています。

It is straightforward to adapt the algorithm to the case where different arms use different Beta distributions as their priors.  
異なるアームが異なるベータ分布を事前分布として使用する場合にアルゴリズムを適応させるのは簡単です。

**Algorithm 2 Thompson sampling for the Bernoulli bandit**  
**アルゴリズム2 ベルヌーイバンディットのためのトンプソンサンプリング**

**Require: $\alpha, \beta$ prior parameters of a Beta distribution**  
**必要条件: ベータ分布の事前パラメータ $\alpha, \beta$**

$$
S_i = 0, F_i = 0, \forall i. \text{ {成功と失敗のカウンタ}} 
$$  
**for $t = 1, \ldots, T$ do**  
**$t = 1, \ldots, T$ の間**  

**for $i = 1, \ldots, K$ do**  
**$i = 1, \ldots, K$ の間**  

Draw $\theta_i$ according to Beta($S_i + \alpha, F_i + \beta$).  
ベータ分布 $Beta(S_i + \alpha, F_i + \beta)$ に従って $\theta_i$ を引く。

**end for**  
**終了**

Draw arm $\hat{i} = \arg \max_i \theta_i$ and observe reward $r$  
アーム $\hat{i} = \arg \max_i \theta_i$ を引き、報酬 $r$ を観察する。

**if $r = 1$ then**  
**もし $r = 1$ なら**  

$$
S_{\hat{i}} = S_{\hat{i}} + 1  
$$  
**else**  
**そうでなければ**  

$$
F_{\hat{i}} = F_{\hat{i}} + 1  
$$  
**end if**  
**終了**

**end for**  
**終了**



## 3 Simulations シミュレーション

We present some simulation results with Thompson sampling for the Bernoulli bandit problem and compare them to the UCB algorithm. 
私たちは、Bernoulliバンディット問題に対するThompsonサンプリングのいくつかのシミュレーション結果を示し、UCBアルゴリズムと比較します。 
The reward probability of each of the K arms is modeled by a Beta distribution which is updated after an arm is selected (see algorithm 2). 
各Kアームの報酬確率は、アームが選択された後に更新されるBeta分布でモデル化されています（アルゴリズム2を参照）。 
The initial prior distribution is Beta(1,1).  
初期の事前分布はBeta(1,1)です。 

There are various variants of the UCB algorithm, but they all have in common that the confidence parameter should increase over time. 
UCBアルゴリズムにはさまざまなバリエーションがありますが、すべての共通点は、信頼パラメータが時間とともに増加する必要があることです。 
Specifically, we chose the arm for which the following upper confidence bound [8, page 278] is maximum:  
具体的には、次の上限信頼区間[8, ページ278]が最大となるアームを選択しました：  

$$
2 m[k] \sqrt{\frac{\log(1/\delta)}{m}} + \sqrt{\frac{2 \log(1/\delta)}{m}} \leq k + \sqrt{m}
$$  

where m is the number of times the arm has been selected and k its total reward. 
ここで、mはアームが選択された回数、kはその合計報酬です。 
This is a tight upper confidence bound derived from Chernoff’s bound.  
これは、Chernoffの境界から導出された厳密な上限信頼区間です。 

In this simulation, the best arm has a reward probability of 0.5 and the K - 1 other arms have a probability of 0.5 - ε. 
このシミュレーションでは、最良のアームの報酬確率は0.5で、他のK - 1アームの確率は0.5 - εです。 
In order to speed up the computations, the parameters are only updated after every 100 iterations. 
計算を高速化するために、パラメータは100回の反復ごとにのみ更新されます。 
The regret as a function of T for various settings is plotted in figure 1. 
さまざまな設定に対するTの関数としての後悔が図1にプロットされています。 
An asymptotic lower bound has been established in [7] for the regret of a bandit algorithm:  
バンディットアルゴリズムの後悔に対して、[7]で漸近的下限が確立されています：  

$$
R(T) \geq \sum_{i=1}^{K} p[*] - p_i D(p_i || p[*]) + o(1)
$$  

where pi is the reward probability of the i-th arm, p[*] = max pi and D is the Kullback-Leibler divergence. 
ここで、$p_i$はi番目のアームの報酬確率、$p[*]$ = max $p_i$、$D$はKullback-Leiblerダイバージェンスです。 
This lower bound is logarithmic in T with a constant depending on the pi values. 
この下限は、$p_i$の値に依存する定数を持つTに対して対数的です。 
The plots in figure 1 show that the regrets are indeed logarithmic in T (the linear trend on the right hand side) and it turns out that the observed constants (slope of the lines) are close to the optimal constants given by the lower bound (2). 
図1のプロットは、後悔が実際にTに対して対数的であることを示しており（右側の線形トレンド）、観測された定数（線の傾き）が下限（2）によって与えられる最適な定数に近いことがわかります。 
Note that the offset of the red curve is irrelevant because of the o(1) term in the lower bound (2). 
赤い曲線のオフセットは、下限（2）のo(1)項のために無関係であることに注意してください。 
In fact, the red curves were shifted such that they pass through the lower left-hand corner of the plot.  
実際、赤い曲線はプロットの左下隅を通過するようにシフトされました。 

K=10, ε=0.1 K=100, ε=0.1  
900 10000  
Thompson Thompson  
800 UCB UCB  
700 Asymptotic lower bound 8000 Asymptotic lower bound  
600  
6000  
500  
400  
4000  
300  
200 2000  
100  
0102 103 104 105 106 0102 103 104 105 106 107  
T T  
K=10, ε=0.02 4 K=100, ε=0.02  
4000 5 [x 10]  
Thompson Thompson  
3500 UCB UCB  
Asymptotic lower bound 4 Asymptotic lower bound  
3000  
2500 3  
2000  
1500 2  
1000  
1  
500  
0102 103 104 105 106 107 0102 104 106 108  
T T  
Figure 1: Cumulative regret for K 10, 100 and ε 0.02, 0.1 . 
図1：K=10、100およびε=0.02、0.1の累積後悔。 
The plots are averaged over 100 repetitions. 
プロットは100回の繰り返しの平均です。 
The red line is the lower bound (2) shifted such that it goes through the origin.  
赤い線は、原点を通過するようにシフトされた下限（2）です。 

As with any Bayesian algorithm, one can wonder about the robustness of Thompson sampling to prior mismatch. 
他のベイズアルゴリズムと同様に、Thompsonサンプリングの事前不一致に対するロバスト性について疑問を持つことができます。 
The results in figure 1 include already some prior mismatch because the Beta prior with parameters (1,1) has a large variance while the true probabilities were selected to be close to 0.5. 
図1の結果には、パラメータ(1,1)のBeta事前が大きな分散を持つため、すでにいくつかの事前不一致が含まれていますが、真の確率は0.5に近いものとして選択されました。 

Figure 2: Regret of optimistic Thompson sampling [11] in the same setting as the lower left plot of figure 1.  
図2：図1の左下のプロットと同じ設定での楽観的Thompsonサンプリングの後悔[11]。 
We have also done some other simulations (not shown) where there is a mismatch in the prior mean. 
私たちは、事前平均に不一致がある他のシミュレーション（表示されていない）も行いました。 
In particular, when the reward probability of the best arm is 0.1 and the 9 others have a probability of 0.08, Thompson sampling—with the same prior as before—is still better than UCB and is still asymptotically optimal. 
特に、最良のアームの報酬確率が0.1で、他の9つが0.08の確率を持つ場合、Thompsonサンプリングは（以前と同じ事前で）依然としてUCBよりも優れており、漸近的に最適です。 

We can thus conclude that in these simulations, Thompson sampling is asymptotically optimal and achieves a smaller regret than the popular UCB algorithm. 
したがって、これらのシミュレーションでは、Thompsonサンプリングが漸近的に最適であり、人気のあるUCBアルゴリズムよりも小さな後悔を達成することが結論できます。 
It is important to note that for UCB, the confidence bound (1) is tight; we have tried some other confidence bounds, including the one originally proposed in [3], but they resulted in larger regrets. 
UCBに関しては、信頼区間（1）が厳密であることに注意することが重要です。私たちは、[3]で元々提案されたものを含む他の信頼区間を試しましたが、それらはより大きな後悔をもたらしました。 

**Optimistic Thompson sampling**  
**楽観的Thompsonサンプリング**  
The intuition behind UCB and Thompson sampling is that, for the purpose of exploration, it is beneficial to boost the predictions of actions for which we are uncertain. 
UCBとThompsonサンプリングの背後にある直感は、探索の目的のために、不確実なアクションの予測を強化することが有益であるということです。 
But Thompson sampling modifies the predictions in both directions and there is apparently no benefit in decreasing a prediction. 
しかし、Thompsonサンプリングは予測を両方向に修正し、予測を減少させることには明らかに利点がありません。 
This observation led to a recently proposed algorithm called Optimistic Bayesian sampling [11] in which the modified score is never smaller than the mean. 
この観察は、修正されたスコアが平均よりも小さくならない楽観的ベイズサンプリング[11]と呼ばれる最近提案されたアルゴリズムにつながりました。 
More precisely, in algorithm 1, Er(r|xt, a, θ[t]) is replaced by max(Er(r|xt, a, θ[t]), Er,θ|D(r|xt, a, θ)).  
より正確には、アルゴリズム1では、$E_r(r|x_t, a, \theta[t])$が$max(E_r(r|x_t, a, \theta[t]), E_{r,\theta|D(r|x_t, a, \theta)})$に置き換えられます。 

Simulations in [12] showed some gains using this optimistic version of Thompson sampling. 
[12]のシミュレーションでは、この楽観的なバージョンのThompsonサンプリングを使用することでいくつかの利点が示されました。 
We compared in figure 2 the two versions of Thompson sampling in the case K = 10 and ε = 0.02. 
図2では、K=10およびε=0.02の場合の2つのThompsonサンプリングのバージョンを比較しました。 
Optimistic Thompson sampling achieves a slightly better regret, but the gain is marginal. 
楽観的Thompsonサンプリングはわずかに良い後悔を達成しますが、その利点はわずかです。 
A possible explanation is that when the number of arms is large, it is likely that, in standard Thompson sampling, the selected arm has a already a boosted score. 
考えられる説明は、アームの数が多い場合、標準のThompsonサンプリングでは選択されたアームがすでに強化されたスコアを持っている可能性が高いということです。 

**Posterior reshaping**  
**事後再形成**  
Thompson sampling is a heuristic advocating to draw samples from the posterior, but one might consider changing that heuristic to draw samples from a modified distribution. 
Thompsonサンプリングは事後からサンプルを引くことを支持するヒューリスティックですが、そのヒューリスティックを変更して修正された分布からサンプルを引くことを考慮することができます。 
In particular, sharpening the posterior would have the effect of increasing exploitation while widening it would favor exploration. 
特に、事後を鋭くすることは、利用を増加させる効果があり、広げることは探索を優先させることになります。 
In our simulations, the posterior is a Beta distribution with parameters a and b, and we have tried to change it to parameters a/α, b/α. 
私たちのシミュレーションでは、事後はパラメータaとbのBeta分布であり、これをパラメータa/α、b/αに変更しようとしました。 
Doing so does not change the posterior mean, but multiply its variance by a factor close to α[2].  
そうすることで、事後の平均は変わりませんが、その分散はα[2]に近い因子で乗算されます。 

Figure 3 shows the average and distribution of regret for different values of α. 
図3は、異なるαの値に対する平均と後悔の分布を示しています。 
Values of α smaller than 1 decrease the amount of exploration and often result in lower regret. 
1未満のαの値は探索の量を減少させ、しばしば低い後悔をもたらします。 
But the price to pay is a higher variance: in some runs, the regret is very large. 
しかし、代償として高い分散が生じます：いくつかの実行では、後悔が非常に大きくなります。 
The average regret is asymptotically not as good as with α = 1, but tends to be better in the non-asymptotic regime. 
平均的な後悔は、α=1のときほど良くはありませんが、非漸近的な領域ではより良くなる傾向があります。 

**Impact of delay**  
**遅延の影響**  
In a real world system, the feedback is typically not processed immediately because of various runtime constraints. 
実世界のシステムでは、フィードバックは通常、さまざまな実行時の制約のために即座に処理されません。 
Instead it usually arrives in batches over a certain period of time. 
代わりに、通常は一定の期間にわたってバッチで到着します。 
We now try to quantify the impact of this delay by doing some simulations that mimic the problem of news articles recommendation [9] that will be described in section 5.  
私たちは、セクション5で説明されるニュース記事の推薦の問題[9]を模倣するいくつかのシミュレーションを行うことで、この遅延の影響を定量化しようとしています。 

Figure 3: Thompson sampling where the parameters of the Beta posterior distribution have been divided by α. 
図3：Beta事後分布のパラメータがαで割られたThompsonサンプリング。 
The setting is the same as in the lower left plot of figure 1 (1000 repetitions). 
設定は図1の左下のプロットと同じです（1000回の繰り返し）。 
Left: average regret as a function of T. 
左：Tの関数としての平均後悔。 
Right: distribution of the regret at T = 10[7]. 
右：$T = 10^7$における後悔の分布。 
Since the outliers can take extreme values, those above 6000 are compressed at the top of the figure.  
外れ値が極端な値を取る可能性があるため、6000を超えるものは図の上部で圧縮されています。 

Table 1: Influence of the delay: regret when the feedback is provided every δ steps.  
表1：遅延の影響：フィードバックが毎δステップで提供されるときの後悔。  

| δ   | 1      | 3      | 10     | 32     | 100    | 316    | 1000   |
|-----|--------|--------|--------|--------|--------|--------|--------|
| UCB | 24,145 | 24,695 | 25,662 | 28,148 | 37,141 | 77,687 | 226,220|
| TS  | 9,105  | 9,199  | 9,049  | 9,451  | 11,550 | 21,594 | 59,256 |
| Ratio| 2.65   | 2.68   | 2.84   | 2.98   | 3.22   | 3.60   | 3.82   |

We consider a dynamic set of 10 items. 
私たちは10アイテムの動的セットを考えます。 
At a given time, with probability 10^{-3} one of the item retires and is replaced by a new one. 
ある時点で、確率$10^{-3}$でアイテムの1つが退役し、新しいものに置き換えられます。 
The true reward probability of a given item is drawn according to a Beta(4,4) distribution. 
特定のアイテムの真の報酬確率はBeta(4,4)分布に従って引かれます。 
The feedback is received only every δ time units. 
フィードバックはδ時間単位でのみ受信されます。 
Table 1 shows the average regret (over 100 repetitions) of Thompson sampling and UCB at T = 10^{6}. 
表1は、$T = 10^6$におけるThompsonサンプリングとUCBの平均後悔（100回の繰り返しの平均）を示しています。 
An interesting quantity in this simulation is the relative regret of UCB and Thompson sampling. 
このシミュレーションでの興味深い量は、UCBとThompsonサンプリングの相対的な後悔です。 
It appears that Thompson sampling is more robust than UCB when the delay is long. 
遅延が長い場合、ThompsonサンプリングはUCBよりもロバストであるようです。 
Thompson sampling alleviates the influence of delayed feedback by randomizing over actions; on the other hand, UCB is deterministic and suffers a larger regret in case of a sub-optimal choice. 
Thompsonサンプリングはアクションをランダム化することで遅延フィードバックの影響を軽減します。一方、UCBは決定論的であり、最適でない選択をした場合により大きな後悔を被ります。



## 4 Display Advertising ディスプレイ広告

We now consider an online advertising application. 
ここでは、オンライン広告アプリケーションを考えます。

Given a user visiting a publisher page, the problem is to select the best advertisement for that user. 
出版社のページを訪れるユーザがいる場合、そのユーザに最適な広告を選択することが問題です。

A key element in this matching problem is the click-through rate (CTR) estimation: what is the probability that a given ad will be clicked given some context (user, page visited)? 
このマッチング問題の重要な要素は、クリック率（CTR）の推定です。特定の広告がクリックされる確率は、あるコンテキスト（ユーザ、訪問したページ）に基づいてどのように決まるのでしょうか？

Indeed, in a cost-per-click (CPC) campaign, the advertiser only pays when his ad gets clicked. 
実際、クリック課金（CPC）キャンペーンでは、広告主は広告がクリックされたときのみ支払います。

This is the reason why it is important to select ads with high CTRs. 
そのため、CTRが高い広告を選択することが重要です。

There is of course a fundamental exploration / exploitation dilemma here: in order to learn the CTR of an ad, it needs to be displayed, leading to a potential loss of short-term revenue. 
もちろん、ここには基本的な探索/活用のジレンマがあります。広告のCTRを学習するためには、その広告を表示する必要があり、短期的な収益の損失を引き起こす可能性があります。

More details on display advertising and the data used for modeling can be found in [1].  
ディスプレイ広告とモデル化に使用されるデータの詳細については、[1]を参照してください。

In this paper, we consider standard regularized logistic regression for predicting CTR. 
本論文では、CTRを予測するために標準的な正則化ロジスティック回帰を考慮します。

There are several features representing the user, page, ad, as well as conjunctions of these features. 
ユーザ、ページ、広告を表すいくつかの特徴があり、これらの特徴の組み合わせも含まれます。

Some of the features include identifiers of the ad, advertiser, publisher and visited page. 
これらの特徴の中には、広告、広告主、出版社、訪問したページの識別子が含まれています。

These features are hashed [17] and each training sample ends up being represented as sparse binary vector of dimension 2[24].  
これらの特徴はハッシュ化され、各トレーニングサンプルは次元2のスパースバイナリベクトルとして表現されます。

In our model, the posterior distribution on the weights is approximated by a Gaussian distribution with diagonal covariance matrix. 
私たちのモデルでは、重みの事後分布は対角共分散行列を持つガウス分布で近似されます。

As in the Laplace approximation, the mean of this distribution is the mode of the posterior and the inverse variance of each weight is given by the curvature. 
ラプラス近似と同様に、この分布の平均は事後のモードであり、各重みの逆分散は曲率によって与えられます。

The use of this convenient approximation of the posterior is twofold. 
この便利な事後分布の近似の使用は二重の目的があります。

It first serves as a prior on the weights to update the model when a new batch of training data becomes available, as described in algorithm 3. 
まず、新しいトレーニングデータのバッチが利用可能になったときにモデルを更新するための重みの事前分布として機能します（アルゴリズム3で説明されています）。

And it is also the distribution used in Thompson sampling.  
また、これはトンプソンサンプリングで使用される分布でもあります。

**Algorithm 3 Regularized logistic regression with batch updates**  
**アルゴリズム3 バッチ更新を伴う正則化ロジスティック回帰**  
**Require: Regularization parameter λ > 0.**  
**必要条件: 正則化パラメータ λ > 0.**  
_mi = 0, qi = λ. {Each weight wi has an independent prior N_ (mi, qi[−][1])}  
_mi = 0, qi = λ. {各重み wi は独立した事前分布 N_ (mi, qi[−][1]) を持つ}  
**for t = 1, . . ., T do**  
**t = 1, . . ., T の間ループする**  
Get a new batch of training data (xj, yj), j = 1, . . ., n.  
新しいトレーニングデータ (xj, yj) を取得する。 j = 1, . . ., n.  
1 � �  
Find w as the minimizer of: 2 _qi(wi −_ _mi)[2]_ + log(1 + exp(−yjw[⊤]xj)).  
次の式の最小化問題を解いて w を求める: 2 _qi(wi −_ _mi)[2]_ + log(1 + exp(−yjw[⊤]xj)).  
_i=1_ _j=1_  
_mi = wi_  
_mi = wi_  
_qi = qi +_ _x[2]ij[p][j][(1][ −]_ _[p][j][)][, p][j]_ [= (1 + exp(][−][w][⊤][x][j][))][−][1][ {][Laplace approximation][}]  
_qi = qi +_ _x[2]ij[p][j][(1][ −]_ _[p][j][)][, p][j]_ [= (1 + exp(][−][w][⊤][x][j][))][−][1][ {][ラプラス近似][}]  
_j=1_  
**end for**  
**終了**  
Evaluating an explore / exploit policy is difficult because we typically do not know the reward of an action that was not chosen.  
探索/活用ポリシーを評価することは難しいです。なぜなら、通常、選択されなかったアクションの報酬がわからないからです。

A possible solution, as we shall see in section 5, is to use a replayer in which previous, randomized exploration data can be used to produce an unbiased offline estimator of the new policy [10].  
可能な解決策は、セクション5で見るように、以前のランダム化された探索データを使用して新しいポリシーのバイアスのないオフライン推定器を生成するリプレイヤーを使用することです [10]。

Unfortunately, their approach cannot be used in our case here because it reduces the effective data size substantially when the number of arms K is large, yielding too high variance in the evaluation results.  
残念ながら、彼らのアプローチは、アームの数 K が大きいときに有効なデータサイズを大幅に減少させ、評価結果において過度の分散をもたらすため、ここでは使用できません。

[15] studies another promising approach using the idea of importance weighting, but the method applies only when the policy is static, which is not the case for online bandit algorithms that constantly adapt to its history.  
[15] は重要度重み付けのアイデアを使用した別の有望なアプローチを研究していますが、この方法はポリシーが静的な場合にのみ適用され、歴史に常に適応するオンラインバンディットアルゴリズムには当てはまりません。

For the sake of simplicity, therefore, we considered in this section a simulated environment.  
そのため、単純さのために、このセクションではシミュレーション環境を考慮しました。

More precisely, the context and the ads are real, but the clicks are simulated using a weight vector w[∗].  
より正確には、コンテキストと広告は実際のものであるが、クリックは重みベクトル $w^{*}$ を使用してシミュレートされています。

This weight vector could have been chosen arbitrarily, but it was in fact a perturbed version of some weight vector learned from real clicks.  
この重みベクトルは任意に選ばれる可能性がありましたが、実際には実際のクリックから学習された重みベクトルの摂動版でした。

The input feature vectors x are thus as in the real world setting, but the clicks are artificially generated with probability $P(y = 1 | x) = (1 + \exp(-w^{*⊤}x))^{-1}$.  
したがって、入力特徴ベクトル $x$ は実世界の設定と同様ですが、クリックは確率 $P(y = 1 | x) = (1 + \exp(-w^{*⊤}x))^{-1}$ で人工的に生成されます。

About 13,000 contexts, representing a small random subset of the total traffic, are presented every hour to the policy which has to choose an ad among a set of eligible ads.  
約13,000のコンテキストが、全トラフィックの小さなランダムサブセットを表し、毎時ポリシーに提示され、ポリシーは適格な広告のセットから広告を選択する必要があります。

The number of eligible ads for each context depends on numerous constraints set by the advertiser and the publisher.  
各コンテキストに対する適格な広告の数は、広告主と出版社によって設定された多数の制約に依存します。

It varies between 5,910 and 1 with a mean of 1,364 and a median of 514 (over a set of 66,373 ads).  
その数は5,910から1の間で変動し、平均1,364、中央値514（66,373の広告のセットに対して）です。

Note that in this experiment, the number of eligible ads is smaller than what we would observe in live traffic because we restricted the set of advertisers.  
この実験では、広告主のセットを制限したため、適格な広告の数はライブトラフィックで観察される数よりも少ないことに注意してください。

The model is updated every hour as described in algorithm 3.  
モデルは、アルゴリズム3で説明されているように、毎時更新されます。

A feature vector is constructed for every (context, ad) pair and the policy decides which ad to show.  
各 (コンテキスト, 広告) ペアに対して特徴ベクトルが構築され、ポリシーはどの広告を表示するかを決定します。

A click for that ad is then generated with probability $(1 + \exp(-w^{*⊤}x))^{-1}$.  
その広告のクリックは、確率 $(1 + \exp(-w^{*⊤}x))^{-1}$ で生成されます。

This labeled training sample is then used at the end of the hour to update the model.  
このラベル付きトレーニングサンプルは、時間の終わりにモデルを更新するために使用されます。

The total number of clicks received during this one hour period is the reward.  
この1時間の間に受け取ったクリックの総数が報酬となります。

But in order to eliminate unnecessary variance in the estimation, we instead computed the expectation of that number since the click probabilities are known.  
しかし、推定における不必要な分散を排除するために、クリック確率が知られているため、その数の期待値を計算しました。

Several explore / exploit strategies are compared; they only differ in the way the ads are selected; all the rest, including the model updates, is identical as described in algorithm 3.  
いくつかの探索/活用戦略が比較されます。これらは広告の選択方法のみが異なり、モデルの更新を含むその他はアルゴリズム3で説明されているように同一です。

These strategies are:  
これらの戦略は次のとおりです：

**Thompson sampling This is algorithm 1 where each weight is drawn independently according to its Gaussian posterior approximation N (mi, qi[−][1]) (see algorithm 3).**  
**トンプソンサンプリング これはアルゴリズム1であり、各重みはそのガウス事後近似 N (mi, qi[−][1]) に従って独立に引かれます（アルゴリズム3を参照）。**

As in section 3, we also consider a variant in which the standard deviations qi[−][1][/][2] are first multiplied by a factor _α_ 0.25, 0.5.  
セクション3と同様に、標準偏差 $q_{i}^{-1/2}$ が最初に係数 $\alpha$ 0.25, 0.5 で乗算されるバリアントも考慮します。

This favors exploitation over exploration.  
これは探索よりも活用を優先します。

**LinUCB This is an extension of the UCB algorithm to the parametric case [9].**  
**LinUCB これはUCBアルゴリズムのパラメトリックケースへの拡張です [9]。**

It selects the ad based on mean and standard deviation.  
これは平均と標準偏差に基づいて広告を選択します。

It also has a factor α to control the exploration / exploitation trade-off.  
また、探索/活用のトレードオフを制御するための係数 $\alpha$ もあります。

More precisely, LinUCB selects the ad for which  
より正確には、LinUCBは次の条件を満たす広告を選択します：

$$
\sum_{i=1}^{d} m_i x_i + \alpha \sum_{i=1}^{d} q_i^{-1} x_i^2 \text{ is maximum.}
$$  
$$
\sum_{i=1}^{d} m_i x_i + \alpha \sum_{i=1}^{d} q_i^{-1} x_i^2 \text{ が最大です。}
$$  

**Exploit-only Select the ad with the highest mean.**  
**活用のみ 平均が最も高い広告を選択します。**

**Random Select the ad uniformly at random.**  
**ランダム 適当に広告を選択します。**

Table 2: CTR regrets on the display advertising data.  
表2: ディスプレイ広告データにおけるCTRの後悔。  
Method TS LinUCB _ε-greedy_ Exploit Random  
手法 TS LinUCB _ε-greedy_ 活用 ランダム  
Parameter 0.25 0.5 1 0.5 1 2 0.005 0.01 0.02  
パラメータ 0.25 0.5 1 0.5 1 2 0.005 0.01 0.02  
Regret (%) 4.45 3.72 3.81 4.99 4.22 4.14 5.05 4.98 5.22 5.00 31.95  
後悔 (%) 4.45 3.72 3.81 4.99 4.22 4.14 5.05 4.98 5.22 5.00 31.95  

0.1  
Thompson  
0.09 LinUCB  
Exploit  
0.08  
0.07  
0.06  
0.05  
0.04  
0.03  
0.02  
0.01  
0  
0 10 20 30 40 50 60 70 80 90  
時間  
Figure 4: CTR regret over the 4 days test period for 3 algorithms: Thompson sampling with α = 0.5, LinUCB with α = 2, Exploit-only.  
図4: 3つのアルゴリズムに対する4日間のテスト期間におけるCTRの後悔: $\alpha = 0.5$ のトンプソンサンプリング、$\alpha = 2$ のLinUCB、活用のみ。

The regret in the first hour is large, around 0.3, because the algorithms predict randomly (no initial model provided).  
最初の1時間の後悔は大きく、約0.3です。これは、アルゴリズムがランダムに予測するため（初期モデルが提供されていないため）です。

_ε-greedy Mix between exploitation and random: with ε probability, select a random ad; otherwise, select the one with the highest mean.  
_ε-greedy 活用とランダムの混合: 確率 ε でランダムな広告を選択し、そうでなければ平均が最も高い広告を選択します。

**Results** A preliminary result is about the quality of the variance prediction.  
**結果** 予備的な結果は、分散予測の質に関するものです。

The diagonal Gaussian approximation of the posterior does not seem to harm the variance predictions.  
事後の対角ガウス近似は、分散予測に悪影響を及ぼさないようです。

In particular, they are very well calibrated: when constructing a 95% confidence interval for CTR, the true CTR is in this interval 95.1% of the time.  
特に、非常によくキャリブレーションされています: CTRの95%信頼区間を構築する際、真のCTRはこの区間に95.1%の確率で存在します。

The regrets of the different explore / exploit strategies can be found in table 2.  
異なる探索/活用戦略の後悔は表2に示されています。

Thompson sampling achieves the best regret and interestingly the modified version with α = 0.5 gives slightly better results than the standard version (α = 1).  
トンプソンサンプリングは最良の後悔を達成し、興味深いことに、$\alpha = 0.5$ の修正バージョンは標準バージョン（$\alpha = 1$）よりもわずかに良い結果を示します。

This confirms the results of the previous section (figure 3) where α < 1 yielded better regrets in the non-asymptotic regime.  
これは、$\alpha < 1$ が非漸近領域でより良い後悔をもたらすことを示した前のセクション（図3）の結果を確認します。

Exploit-only does pretty well, at least compared to random selection.  
活用のみはかなり良好で、少なくともランダム選択と比較してそうです。

This seems at first a bit surprising given that the system has no prior knowledge about the CTRs.  
これは、システムがCTRに関する事前知識を持っていないことを考えると、最初は少し驚くべきことのようです。

A possible explanation is that the change in context induces some exploration, as noted in [13].  
可能な説明は、コンテキストの変化がいくつかの探索を引き起こすということです（[13]で指摘されています）。

Also, the fact that exploit-only is so much better than random might explain why ε-greedy does not beat it: whenever this strategy chooses a random action, it suffers a large regret in average which is not compensated by its exploration benefit.  
また、活用のみがランダムよりもはるかに優れているという事実は、なぜε-greedyがそれを上回らないのかを説明するかもしれません。この戦略がランダムなアクションを選択するたびに、平均して大きな後悔を被り、その探索の利益で補償されることはありません。

Finally figure 4 shows the regret of three algorithms across time.  
最後に、図4は時間にわたる3つのアルゴリズムの後悔を示しています。

As expected, the regret has a decreasing trend over time.  
予想通り、後悔は時間とともに減少する傾向があります。



## 5 News Article Recommendation ニュース記事推薦

In this section, we consider another application of Thompson sampling in personalized news article recommendation on Yahoo! front page [2, 9].  
このセクションでは、Yahoo! フロントページにおけるパーソナライズされたニュース記事推薦におけるトンプソンサンプリングの別の応用を考察します [2, 9]。

Each time a user visits the portal, a news article out of a small pool of hand-picked candidates is recommended.  
ユーザがポータルを訪れるたびに、厳選された候補の小さなプールからニュース記事が推薦されます。

The candidate pool is dynamic: old articles may retire and new articles may be added in.  
候補プールは動的であり、古い記事は退役し、新しい記事が追加されることがあります。

The average size of the pool is around 20.  
プールの平均サイズは約20です。

The goal is to choose the most interesting article to users, or formally, maximize the total number of clicks on the recommended articles.  
目標は、ユーザにとって最も興味深い記事を選ぶことであり、正式には推薦された記事のクリック数を最大化することです。

In this case, we treat articles as arms, and define the payoff to be 1 if the article is clicked on and 0 otherwise.  
この場合、記事をアームとして扱い、記事がクリックされた場合のペイオフを1、そうでない場合を0と定義します。

Therefore, the average per-trial payoff of a policy is its overall CTR.  
したがって、ポリシーの平均試行あたりのペイオフは、その全体のCTR（クリック率）です。

Each user was associated with a binary raw feature vector of over 1000 dimension, which indicates information of the user like age, gender, geographical location, behavioral targeting, etc.  
各ユーザは、年齢、性別、地理的位置、行動ターゲティングなどのユーザ情報を示す1000次元以上のバイナリ生特徴ベクトルに関連付けられました。

These features are typically sparse, so using them directly makes learning more difficult and is computationally expensive.  
これらの特徴は通常スパースであるため、直接使用すると学習が難しくなり、計算コストが高くなります。

One can find lower dimension feature subspace by, say, following previous practice [9].  
以前の実践に従って、低次元の特徴サブスペースを見つけることができます [9]。

Here, we adopted the simpler principal component analysis (PCA), which did not appear to affect the bandit algorithms much in our experience.  
ここでは、より簡単な主成分分析（PCA）を採用しましたが、私たちの経験ではバンディットアルゴリズムに大きな影響を与えないようでした。

In particular, we performed a PCA and projected the raw user feature onto the first 20 principal components.  
特に、PCAを実行し、生のユーザ特徴を最初の20の主成分に射影しました。

Finally, a constant feature 1 is appended, so that the final user feature contains 21 components.  
最後に、定数特徴1を追加し、最終的なユーザ特徴は21の成分を含むようにしました。

The constant feature serves as the bias term in the CTR model described next.  
この定数特徴は、次に説明するCTRモデルのバイアス項として機能します。

We use logistic regression, as in Algorithm 3, to model article CTRs: given a user feature vector **x ∈ℜ[21], the probability of click on an article a is (1 + exp(−x[⊤]wa))[−][1]** for some weight vector **wa ∈ℜ[21]** to be learned.  
私たちは、アルゴリズム3のようにロジスティック回帰を使用して記事のCTRをモデル化します：ユーザ特徴ベクトル **x ∈ℜ[21]** が与えられたとき、記事aがクリックされる確率は、学習される重みベクトル **wa ∈ℜ[21]** に対して **(1 + exp(−x[⊤]wa))[−][1]** です。

The same parameter algorithm and exploration heuristics are applied as in the previous section.  
前のセクションと同様に、同じパラメータアルゴリズムと探索ヒューリスティクスが適用されます。

Note that we have a different weight vector for each article, which is affordable as the numbers of articles and features are both small.  
各記事に対して異なる重みベクトルがあることに注意してください。これは、記事と特徴の数がどちらも少ないため、実行可能です。

Furthermore, given the size of data, we have not found article features to be helpful.  
さらに、データのサイズを考慮すると、記事の特徴が役立つとは考えられませんでした。

Indeed, it is shown in our previous work [9, Figure 5] that article features are helpful in this domain only when data are highly sparse.  
実際、私たちの以前の研究 [9, 図5] では、データが非常にスパースな場合にのみ、記事の特徴がこの領域で役立つことが示されています。

Given the small size of candidate pool, we adopt the unbiased offline evaluation method of [10] to compare various bandit algorithms.  
候補プールの小さなサイズを考慮して、私たちはさまざまなバンディットアルゴリズムを比較するために [10] のバイアスのないオフライン評価方法を採用します。

In particular, we collected randomized serving events for a random fraction of user visits; in other words, these random users were recommended an article chosen uniformly from the candidate pool.  
特に、ユーザ訪問のランダムな割合に対してランダム化された提供イベントを収集しました。言い換えれば、これらのランダムユーザには候補プールから均等に選ばれた記事が推薦されました。

From 7 days in June 2009, over 34M randomized serving events were obtained.  
2009年6月の7日間で、3400万件以上のランダム化された提供イベントが得られました。

As in section 3, we varied the update delay to study how various algorithms degrade.  
セクション3と同様に、さまざまなアルゴリズムがどのように劣化するかを研究するために、更新遅延を変化させました。

Three values were tried: 10, 30, and 60 minutes.  
試した値は3つあり、10分、30分、60分です。

Figure 5 summarizes the overall CTRs of four families of algorithm together with the exploit-only baseline.  
図5は、4つのアルゴリズムファミリーの全体的なCTRを、エクスプロイトのみのベースラインとともに要約しています。

As in the previous section, (optimistic) Thompson sampling appears competitive across all delays.  
前のセクションと同様に、（楽観的な）トンプソンサンプリングはすべての遅延において競争力があるようです。

While the deterministic UCB works well with short delay, its performance drops significantly as the delay increases.  
決定論的UCBは短い遅延ではうまく機能しますが、遅延が増加するにつれてその性能は大幅に低下します。

In contrast, randomized algorithms are more robust to delay, and when there is a one-hour delay, (optimistic) Thompson sampling is significant better than others (given the size of our data).  
対照的に、ランダム化アルゴリズムは遅延に対してより堅牢であり、1時間の遅延がある場合、（楽観的な）トンプソンサンプリングは他のアルゴリズムよりも大幅に優れています（データのサイズを考慮すると）。

|TS 0.5 TS 1 OTS 0.5 OTS 1 UCB 1 UCB 2 UCB 5 EG 0.05 EG 0.1 Exploit|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|Col25|Col26|Col27|Col28|Col29|Col30|Col31|Col32|Col33|Col34|Col35|Col36|Col37|Col38|Col39|Col40|Col41|Col42|Col43|Col44|Col45|Col46|Col47|TS 0.5 TS 1 OTS 0.5 OTS 1 UCB 1 UCB 2 UCB 5 EG 0.05 EG 0.1 Exploit|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||
|re t u|5: p|d|N at|or e|m d|a el|1 li a|0 ze ys|d :|{|C 1|T 0,|R 3|s 0|of var, 60 }|io m|u i|s n|a ut|lg es|o .|3 ri T|0 th h|m e|De n|la o o|y ( n rm|mi th a|n) e li|news zatio|a n|rt is|i|cl w|e it|re h|6 c re|0 o s|m p|m ec|e t|n to|d|at a|ion data with dif random baseline|||



## 6 Conclusion 結論

The extensive experimental evaluation carried out in this paper reveals that Thompson sampling is a very effective heuristic for addressing the exploration / exploitation trade-off.  
本論文で実施された広範な実験評価は、トンプソンサンプリングが探索と活用のトレードオフに対処するための非常に効果的なヒューリスティックであることを明らかにしています。 

In its simplest form, it does not have any parameter to tune, but our results show that tweaking the posterior to reduce exploration can be beneficial.  
その最も単純な形では、調整すべきパラメータはありませんが、私たちの結果は、探索を減らすために事後分布を調整することが有益である可能性があることを示しています。 

In any case, Thompson sampling is very easy to implement and should thus be considered as a standard baseline.  
いずれにせよ、トンプソンサンプリングは非常に実装が簡単であり、標準的なベースラインとして考慮されるべきです。 

Also, since it is a randomized algorithm, it is robust in the case of delayed feedback.  
また、これはランダム化アルゴリズムであるため、遅延フィードバックの場合でも堅牢です。 

Future work includes of course, a theoretical analysis of its finite-time regret.  
今後の研究には、もちろん、その有限時間の後悔の理論的分析が含まれます。 

The benefit of this analysis would be twofold.  
この分析の利点は二つあります。 

First, it would hopefully contribute to make Thompson sampling as popular as other algorithms for which regret bounds exist.  
第一に、トンプソンサンプリングが後悔の境界が存在する他のアルゴリズムと同じくらい人気になることに貢献することを期待しています。 

Second, it could provide guidance on tweaking the posterior in order to achieve a smaller regret.  
第二に、より小さな後悔を達成するために事後分布を調整するための指針を提供することができるでしょう。 



## References 参考文献

[1] D. Agarwal, R. Agrawal, R. Khanna, and N. Kota. Estimating rates of rare events with multiple hierarchies through scalable log-linear models. In Proceedings of the 16th ACM SIGKDD _international conference on Knowledge discovery and data mining, pages 213–222, 2010._  
D. Agarwal, R. Agrawal, R. Khanna, および N. Kota. 複数の階層を持つ稀なイベントの発生率をスケーラブルな対数線形モデルを用いて推定する。第16回ACM SIGKDD国際会議「知識発見とデータマイニング」の論文集、ページ213–222、2010年。

[2] Deepak Agarwal, Bee-Chung Chen, Pradheep Elango, Nitin Motgi, Seung-Taek Park, Raghu Ramakrishnan, Scott Roy, and Joe Zachariah. Online models for content optimization. In _Advances in Neural Information Processing Systems 21, pages 17–24, 2008._  
Deepak Agarwal, Bee-Chung Chen, Pradheep Elango, Nitin Motgi, Seung-Taek Park, Raghu Ramakrishnan, Scott Roy, および Joe Zachariah. コンテンツ最適化のためのオンラインモデル。_神経情報処理システムの進展 21、ページ17–24、2008年。_

[3] P. Auer, N. Cesa-Bianchi, and P. Fischer. Finite-time analysis of the multiarmed bandit problem. Machine learning, 47(2):235–256, 2002.  
P. Auer, N. Cesa-Bianchi, および P. Fischer. マルチアームバンディット問題の有限時間分析。機械学習、47(2):235–256、2002年。

[4] John C. Gittins. Multi-armed Bandit Allocation Indices. Wiley Interscience Series in Systems and Optimization. John Wiley & Sons Inc, 1989.  
John C. Gittins. マルチアームバンディット割当インデックス。Wiley Interscienceシリーズ システムと最適化。ジョン・ワイリー・アンド・サンズ社、1989年。

[5] Thore Graepel, Joaquin Quinonero Candela, Thomas Borchert, and Ralf Herbrich. Web-scale Bayesian click-through rate prediction for sponsored search advertising in Microsoft’s Bing search engine. In Proceedings of the Twenty-Seventh International Conference on Machine _Learning (ICML-10), pages 13–20, 2010._  
Thore Graepel, Joaquin Quinonero Candela, Thomas Borchert, および Ralf Herbrich. MicrosoftのBing検索エンジンにおけるスポンサー検索広告のためのウェブ規模のベイズ的クリック率予測。第27回国際機械学習会議（ICML-10）の論文集、ページ13–20、2010年。

[6] O.-C. Granmo. Solving two-armed bernoulli bandit problems using a bayesian learning automaton. International Journal of Intelligent Computing and Cybernetics, 3(2):207–234, 2010.  
O.-C. Granmo. ベイズ学習オートマトンを用いた二腕ベルヌーイバンディット問題の解決。国際知能計算とサイバネティクスジャーナル、3(2):207–234、2010年。

[7] T.L. Lai and H. Robbins. Asymptotically efficient adaptive allocation rules. _Advances in_ _applied mathematics, 6:4–22, 1985._  
T.L. Lai および H. Robbins. 漸近的に効率的な適応割当ルール。_応用数学の進展、6:4–22、1985年。_

[8] J. Langford. Tutorial on practical prediction theory for classification. Journal of Machine _Learning Research, 6(1):273–306, 2005._  
J. Langford. 分類のための実用的予測理論に関するチュートリアル。機械学習研究ジャーナル、6(1):273–306、2005年。

[9] L. Li, W. Chu, J. Langford, and R. E. Schapire. A contextual-bandit approach to personalized news article recommendation. In Proceedings of the 19th international conference on World _wide web, pages 661–670, 2010._  
L. Li, W. Chu, J. Langford, および R. E. Schapire. パーソナライズされたニュース記事推薦のためのコンテキストバンディットアプローチ。第19回国際会議「ワールドワイドウェブ」の論文集、ページ661–670、2010年。

[10] L. Li, W. Chu, J. Langford, and X. Wang. Unbiased offline evaluation of contextual-banditbased news article recommendation algorithms. In Proceedings of the fourth ACM interna_tional conference on Web search and data mining, pages 297–306, 2011._  
L. Li, W. Chu, J. Langford, および X. Wang. コンテキストバンディットベースのニュース記事推薦アルゴリズムのバイアスのないオフライン評価。第4回ACM国際会議「ウェブ検索とデータマイニング」の論文集、ページ297–306、2011年。

[11] Benedict C. May, Nathan Korda, Anthony Lee, and David S. Leslie. Optimistic Bayesian sampling in contextual-bandit problems. Technical Report 11:01, Statistics Group, Department of Mathematics, University of Bristol, 2011. Submitted to the Annals of Applied Probability.  
Benedict C. May, Nathan Korda, Anthony Lee, および David S. Leslie. コンテキストバンディット問題における楽観的ベイズサンプリング。技術報告11:01、統計グループ、ブリストル大学数学科、2011年。応用確率論の年報に提出。

[12] Benedict C. May and David S. Leslie. Simulation studies in optimistic Bayesian sampling in contextual-bandit problems. Technical Report 11:02, Statistics Group, Department of Mathematics, University of Bristol, 2011.  
Benedict C. May および David S. Leslie. コンテキストバンディット問題における楽観的ベイズサンプリングのシミュレーション研究。技術報告11:02、統計グループ、ブリストル大学数学科、2011年。

[13] J. Sarkar. One-armed bandit problems with covariates. The Annals of Statistics, 19(4):1978–2002, 1991.  
J. Sarkar. 共変量を持つ一腕バンディット問題。統計の年報、19(4):1978–2002、1991年。

[14] S. Scott. A modern bayesian look at the multi-armed bandit. Applied Stochastic Models in _Business and Industry, 26:639–658, 2010._  
S. Scott. マルチアームバンディットに対する現代的なベイズ的視点。ビジネスと産業における応用確率モデル、26:639–658、2010年。

[15] Alexander L. Strehl, John Langford, Lihong Li, and Sham M. Kakade. Learning from logged implicit exploration data. In Advances in Neural Information Processing Systems 23 (NIPS_10), pages 2217–2225, 2011._  
Alexander L. Strehl, John Langford, Lihong Li, および Sham M. Kakade. ログされた暗黙の探索データからの学習。神経情報処理システムの進展 23 (NIPS_10)、ページ2217–2225、2011年。

[16] William R. Thompson. On the likelihood that one unknown probability exceeds another in view of the evidence of two samples. Biometrika, 25(3–4):285–294, 1933.  
William R. Thompson. 二つのサンプルの証拠に基づいて、一つの未知の確率が他の確率を超える可能性について。バイオメトリカ、25(3–4):285–294、1933年。

[17] K. Weinberger, A. Dasgupta, J. Attenberg, J. Langford, and A. Smola. Feature hashing for large scale multitask learning. In ICML, 2009.  
K. Weinberger, A. Dasgupta, J. Attenberg, J. Langford, および A. Smola. 大規模マルチタスク学習のための特徴ハッシング。ICML、2009年。
