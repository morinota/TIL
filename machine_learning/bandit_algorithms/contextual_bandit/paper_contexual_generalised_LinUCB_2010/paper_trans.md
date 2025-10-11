
# Parametric Bandits: The Generalized Linear Case  

## Abstract 要約

We consider structured multi-armed bandit problems based on the Generalized Linear Model (GLM) framework of statistics.
私たちは、一般化線形モデル（GLM）統計フレームワークに基づく構造化されたマルチアームバンディット問題を考察します。
For these bandits, we propose a new algorithm, called GLM-UCB.
これらのバンディットに対して、私たちはGLM-UCBと呼ばれる新しいアルゴリズムを提案します。
We derive finite time, high probability bounds on the regret of the algorithm, extending previous analyses developed for the linear bandits to the non-linear case.
私たちは、このアルゴリズムの後悔に関する有限時間、高確率の境界を導出し、線形バンディットのために開発された以前の分析を非線形ケースに拡張します。
The analysis highlights a key difficulty in generalizing linear bandit algorithms to the non-linear case, which is solved in GLM-UCB by focusing on the reward space rather than on the parameter space.
この分析は、線形バンディットアルゴリズムを非線形ケースに一般化する際の重要な困難を浮き彫りにし、GLM-UCBではパラメータ空間ではなく報酬空間に焦点を当てることでこれを解決します。
Moreover, as the actual effectiveness of current parameterized bandit algorithms is often poor in practice, we provide a tuning method based on asymptotic arguments, which leads to significantly better practical performance.
さらに、現在のパラメータ化されたバンディットアルゴリズムの実際の効果がしばしば不十分であるため、漸近的な議論に基づく調整方法を提供し、これにより実際のパフォーマンスが大幅に向上します。
We present two numerical experiments on real-world data that illustrate the potential of the GLM-UCB approach.
私たちは、GLM-UCBアプローチの可能性を示す実世界データに基づく2つの数値実験を提示します。

**Keywords: multi-armed bandit, parametric bandits, generalized linear models, UCB, regret minimization.**  
**キーワード: マルチアームバンディット、パラメトリックバンディット、一般化線形モデル、UCB、後悔最小化。**

## 1 Introduction はじめに

In the classical K-armed bandit problem, an agent selects at each time step one of the K arms and receives a reward that depends on the chosen action.
古典的なKアームバンディット問題では、エージェントは各時間ステップでK本のアームのうちの1本を選択し、選択したアクションに依存する報酬を受け取ります。
The aim of the agent is to choose the sequence of arms to be played so as to maximize the cumulated reward.
エージェントの目的は、累積報酬を最大化するようにプレイするアームのシーケンスを選択することです。
There is a fundamental trade-off between gathering experimental data about the reward distribution (exploration) and exploiting the arm which seems to be the most promising.
報酬分布に関する実験データを収集すること（探索）と、最も有望に見えるアームを利用することとの間には基本的なトレードオフがあります。

In the basic multi-armed bandit problem, also called the independent bandits problem, the rewards are assumed to be random and distributed independently according to a probability distribution that is specific to each arm –see [1, 2, 3, 4] and references therein.
基本的なマルチアームバンディット問題、または独立バンディット問題では、報酬はランダムであり、各アームに特有の確率分布に従って独立に分布していると仮定されます – [1, 2, 3, 4]およびそこにある参考文献を参照してください。
Recently, structured bandit problems in which the distributions of the rewards pertaining to each arm are connected by a common unknown parameter have received much attention [5, 6, 7, 8, 9].
最近、各アームに関連する報酬の分布が共通の未知のパラメータによって結びつけられた構造化バンディット問題が多くの注目を集めています [5, 6, 7, 8, 9]。
This model is motivated by the many practical applications where the number of arms is large, but the payoffs are interrelated.
このモデルは、アームの数が多いがペイオフが相互に関連している多くの実用的なアプリケーションに基づいています。
Up to know, two different models were studied in the literature along these lines.
これまでのところ、これらの観点から文献で2つの異なるモデルが研究されてきました。
In one model, in each times step, a side-information, or context, is given to the agent first.
1つのモデルでは、各時間ステップで、エージェントに最初にサイド情報またはコンテキストが与えられます。
The payoffs of the arms depend both on this side information and the index of the arm.
アームのペイオフは、このサイド情報とアームのインデックスの両方に依存します。
Thus the optimal arm changes with the context [5, 6, 9].
したがって、最適なアームはコンテキストによって変化します [5, 6, 9]。

In the second, simpler model, that we are also interested in here, there is no side-information, but the agent is given a model that describes the possible relations between the arms’ payoffs.
私たちがここで関心を持っている2つ目の、より単純なモデルでは、サイド情報はありませんが、エージェントにはアームのペイオフ間の可能な関係を説明するモデルが与えられます。
In particular, in “linear bandits” [10, 8, 11, 12], each arm $a \in A$ is associated with some $d$-dimensional vector $m_a \in \mathbb{R}^d$ known to the agent.
特に、「線形バンディット」 [10, 8, 11, 12] では、各アーム $a \in A$ は、エージェントに知られているいくつかの$d$次元ベクトル $m_a \in \mathbb{R}^d$ に関連付けられています。
The expected payoffs of the arms are given by the inner product of their associated vector and some fixed, but initially unknown parameter vector $\theta^*$.
アームの期待ペイオフは、それらの関連付けられたベクトルと、いくつかの固定されたが初めは未知のパラメータベクトル $\theta^*$ の内積によって与えられます。
Thus, the expected payoff of arm $a$ is $m_a^T \theta^*$, which is linear in $\theta^*$.
したがって、アーム $a$ の期待ペイオフは $m_a^T \theta^*$ であり、これは $\theta^*$ に対して線形です。

In this article, we study a richer generalized linear model (GLM) in which the expectation of the reward conditionally to the action $a$ is given by $\mu(m_a^T \theta^*)$, where $\mu$ is a real-valued, non-linear function called the (inverse) link function.
この記事では、アクション $a$ に条件付けられた報酬の期待値が $\mu(m_a^T \theta^*)$ で与えられる、より豊かな一般化線形モデル (GLM) を研究します。ここで、$\mu$ は実数値の非線形関数で、(逆)リンク関数と呼ばれます。
This generalization allows to consider a wider class of problems, and in particular cases where the rewards are counts or binary variables using, respectively, Poisson or logistic regression.
この一般化により、より広いクラスの問題を考慮することができ、特に報酬がカウントまたはバイナリ変数である場合に、ポアソン回帰またはロジスティック回帰をそれぞれ使用することができます。
Obviously, this situation is very common in the fields of marketing, social networking, web-mining (see example of Section 5.2 below) or clinical studies.
明らかに、この状況はマーケティング、ソーシャルネットワーキング、ウェブマイニング（以下のセクション5.2の例を参照）や臨床研究の分野で非常に一般的です。

Our first contribution is an “optimistic” algorithm, termed GLM-UCB, inspired by the Upper Confidence Bound (UCB) approach [2].
私たちの最初の貢献は、Upper Confidence Bound (UCB) アプローチ [2] に触発された「楽観的」アルゴリズムであるGLM-UCBです。
GLM-UCB generalizes the algorithms studied by [10, 8, 12].
GLM-UCBは、[10, 8, 12]で研究されたアルゴリズムを一般化します。
Our next contribution are finite-time bounds on the statistical performance of this algorithm.
次の貢献は、このアルゴリズムの統計的性能に関する有限時間の境界です。
In particular, we show that the performance depends on the dimension of the parameter but not on the number of arms, a result that was previously known in the linear case.
特に、性能はパラメータの次元に依存しますが、アームの数には依存しないことを示します。これは線形の場合に以前から知られていた結果です。
Interestingly, the GLM-UCB approach takes advantage of the particular structure of the parameter estimate of generalized linear models and operates only in the reward space.
興味深いことに、GLM-UCBアプローチは一般化線形モデルのパラメータ推定の特定の構造を利用し、報酬空間内でのみ動作します。
In contrast, the parameter-space confidence region approach adopted by [8, 12] appears to be harder to generalize to non-linear regression models.
対照的に、[8, 12]で採用されたパラメータ空間の信頼領域アプローチは、非線形回帰モデルに一般化するのが難しいようです。

Our second contribution is a tuning method based on asymptotic arguments.
私たちの2つ目の貢献は、漸近的な議論に基づくチューニング方法です。
This contribution addresses the poor empirical performance of the current algorithms that we have observed for small or moderate sample-sizes when these algorithms are tuned based on finite-sample bounds.
この貢献は、これらのアルゴリズムが有限サンプルの境界に基づいて調整されるときに、小さなまたは中程度のサンプルサイズに対して観察された現在のアルゴリズムの乏しい経験的性能に対処します。

The paper is organized as follows.
本論文は以下のように構成されています。
The generalized linear bandit model is presented in Section 2, together with a brief survey of needed statistical results.
一般化線形バンディットモデルはセクション2で提示され、必要な統計結果の簡単な調査が行われます。
Section 3 is devoted to the description of the GLM-UCB algorithm, which is compared to related approaches.
セクション3は、GLM-UCBアルゴリズムの説明に専念し、関連するアプローチと比較されます。
Section 4 presents our regret bounds, as well as a discussion, based on asymptotic arguments, on the optimal tuning of the method.
セクション4では、私たちの後悔の境界と、漸近的な議論に基づく方法の最適なチューニングに関する議論が提示されます。
Section 5 reports the results of two experiments on real data sets.
セクション5では、実データセットに関する2つの実験の結果が報告されます。

## 2 Generalized Linear Bandits, Generalized Linear Models

We consider a structured bandit model with a finite, but possibly very large, number of arms.
私たちは、有限であるが、場合によっては非常に大きな数のアームを持つ構造化バンディットモデルを考えます。

At each time t, the agent chooses an arm At from the set A (we shall denote the cardinality of A by K).
各時刻 $t$ において、エージェントは集合 $A$ からアーム $A_t$ を選択します（$A$ の基数を $K$ と表記します）。

The prior knowledge available to the agent consists of a collection of vectors {ma}a∈A of features which are specific to each arm and a so-called (inverse) link function µ : R → R.
エージェントが利用できる事前知識は、各アームに特有の特徴のベクトルの集合 ${m_a} \forall {a \in A}$ と、いわゆる（逆）リンク関数 $\mu : \mathbb{R} \to \mathbb{R}$ で構成されています。
(m_aはいわゆるcontext...!:thinking:)
(逆リンク関数はスカラーをスカラーに変換するやつ...!:thinking:)

The generalized linear bandit model investigated in this work is based on the assumption that the payoff $R_t$ received at time $t$ is conditionally independent of the past payoffs and choices and it satisfies
本研究で調査された一般化線形バンディットモデルは、**時刻 $t$ に受け取る報酬 $R_t$ が過去の報酬や選択に条件付き独立**であり、次の条件を満たすという仮定に基づいています。

$$
E [ R_t | A_t] = \mu(m_{A_t}^T \theta^*)
$$  

for some unknown parameter vector $\theta^* \in \mathbb{R}^d$.
ここで、未知のパラメータベクトル $\theta^* \in \mathbb{R}^d$ に対して成り立ちます。この枠組みは、[10, 8, 12] によって考慮された線形バンディットモデルを一般化しています。

Just like the linear bandit model builds on linear regression, our model capitalizes on the well-known statistical framework of Generalized Linear Models (GLMs).
線形バンディットモデルが線形回帰に基づいているのと同様に、私たちのモデルは一般化線形モデル（GLM）のよく知られた統計的枠組みを活用しています。

The advantage of this framework is that it allows to address various, specific reward structures widely found in applications.
この枠組みの利点は、アプリケーションで広く見られるさまざまな特定の報酬構造に対処できることです。

For example, when rewards are binary-valued, a suitable choice of $\mu$ is $\mu(x) = \frac{\exp(x)}{1 + \exp(x)}$, leading to the logistic regression model.
たとえば、**報酬が二値の場合、逆リンク関数 $\mu$ の適切な選択は $\mu(x) = \frac{\exp(x)}{1 + \exp(x)}$ であり、ロジスティック回帰モデルにつながります**。(うんうん...!)

For integer valued rewards, the choice $\mu(x) = \exp(x)$ leads to the Poisson regression model.
**整数値の報酬の場合、逆リンク関数の適切な選択は $\mu(x) = \exp(x)$ になり、ポアソン回帰モデルにつながります**。

This can be easily extended to the case of multinomial (or polytomic) logistic regression, which is appropriate to model situations in which the rewards are associated with categorical variables.
これは、**報酬がカテゴリカル変数に関連付けられている状況**をモデル化するのに適している多項ロジスティック回帰の場合に簡単に拡張できます。

To keep this article self-contained, we briefly review the main properties of GLMs [13].
この記事を自己完結型(=ありがたい!)に保つために、GLMの主な特性を簡単にレビューします [13]。

<!-- ここまで読んだ! -->

A univariate probability distribution is said to belong to a canonical exponential family if its density with respect to a reference measure is given by
単変量確率分布は、基準測度に対する密度が次のように与えられる場合、標準指数族に属すると言います。
(統計学の知識っぽい。。。)

$$
p_\beta(r) = \exp (r\beta - b(\beta) + c(r)),
$$  
where $\beta$ is a real parameter, $c(\cdot)$ is a real function and the function $b(\cdot)$ is assumed to be twice continuously differentiable.
ここで、$\beta$ は実数パラメータ、$c(\cdot)$ は実数関数、$b(\cdot)$ は2回連続微分可能であると仮定します。

This family contains the Gaussian and Gamma distributions when the reference measure is the Lebesgue measure and the Poisson and Bernoulli distributions when the reference measure is the counting measure on the integers.
この族は、基準測度がルベーグ測度であるときにガウス分布とガンマ分布を含み、基準測度が整数上のカウント測度であるときにポアソン分布とベルヌーイ分布を含みます。

For a random variable $R$ with density defined in (2), $E(R) = b'(\beta)$ and $Var(R) = b''(\beta)$, where $b'$ and $b''$ denote, respectively, the first and second derivatives of $b$.
式 (2) で定義された密度を持つ確率変数 $R$ に対して、$E(R) = b'(\beta)$ および $Var(R) = b''(\beta)$ であり、ここで $b'$ と $b''$ はそれぞれ $b$ の1階および2階導関数を示します。

In addition, $b''(\beta)$ can also be shown to be equal to the Fisher information matrix for the parameter $\beta$.
さらに、$b''(\beta)$ はパラメータ $\beta$ のフィッシャー情報行列に等しいことも示されます。

The function $b$ is thus strictly convex.
したがって、関数 $b$ は厳密に凸です。

Now, assume that, in addition to the response variable $R$, we have at hand a vector of covariates $X \in \mathbb{R}^d$.
さて、応答変数 $R$ に加えて、共変量のベクトル $X \in \mathbb{R}^d$ を手元に持っていると仮定します。

The canonical GLM associated to (2) postulates that $p_\theta(r|x) = p_{x^T \theta}(r)$, where $\theta \in \mathbb{R}^d$ is a vector of parameter.
式 (2) に関連する標準GLMは、$p_\theta(r|x) = p_{x^T \theta}(r)$ と仮定します。ここで、$\theta \in \mathbb{R}^d$ はパラメータのベクトルです。

Denote by $\mu = b'$ the so-called inverse link function.
$\mu = b'$ をいわゆる逆リンク関数と呼びます。

From the properties of $b$, we know that $\mu$ is continuously differentiable, strictly increasing, and thus one-to-one.
$b$ の特性から、$\mu$ は連続的に微分可能であり、厳密に増加し、したがって一対一であることがわかります。

The maximum likelihood estimator $\hat{\theta}_t$, based on observations $(R_1, X_1), \ldots, (R_{t-1}, X_{t-1})$, is defined as the maximizer of the function
観測 $(R_1, X_1), \ldots, (R_{t-1}, X_{t-1})$ に基づく最尤推定量 $\hat{\theta}_t$ は、次の関数の最大化として定義されます。

$$
\sum_{k=1}^{t-1} \log p_\theta(R_k|X_k) =
\sum_{k=1}^{t-1} \left( R_k X_k^T \theta - b(X_k^T \theta) + c(R_k) \right)
$$  
a strictly concave function in $\theta$.
これは、$\theta$ に関して厳密に凹な関数です。

Upon differentiating, we obtain that $\hat{\theta}_t$ is the unique solution of the following estimating equation
微分すると、$\hat{\theta}_t$ は次の推定方程式の唯一の解であることがわかります。

$$
\sum_{k=1}^{t-1} (R_k - \mu(X_k^T \theta)) X_k = 0
$$  
where we have used the fact that $\mu = b'$.
ここで、$\mu = b'$ という事実を使用しました。

In practice, the solution of (3) may be found efficiently using, for instance, Newton’s algorithm.
実際には、(3) の解は、たとえばニュートン法を使用して効率的に見つけることができます。

A semi-parametric version of the above model is obtained by assuming only that $E_\theta[R|X] = \mu(X^T \theta)$ without (much) further assumptions on the conditional distribution of $R$ given $X$.
上記のモデルの半パラメトリックバージョンは、$E_\theta[R|X] = \mu(X^T \theta)$ であることのみを仮定し、$X$ が与えられたときの $R$ の条件付き分布に関して（あまり）さらなる仮定を置かないことによって得られます。

In this case, the estimator obtained by solving (3) is referred to as the maximum quasi-likelihood estimator.
この場合、(3) を解くことによって得られる推定量は、最大準尤推定量と呼ばれます。

It is a remarkable fact that this estimator is consistent under very general assumptions as long as the design matrix $\sum_{k=1}^{t-1} X_k X_k^T$ tends to infinity.
この推定量は、設計行列 $\sum_{k=1}^{t-1} X_k X_k^T$ が無限大に近づく限り、非常に一般的な仮定の下で一貫性があるというのは注目すべき事実です。

As we will see, this matrix also plays a crucial role in the algorithm that we propose for bandit optimization in the generalized linear bandit model.
私たちが見るように、この行列は一般化線形バンディットモデルにおけるバンディット最適化のために提案するアルゴリズムにおいても重要な役割を果たします。

## 3 The GLM-UCB Algorithm GLM-UCBアルゴリズム

According to (1), the agent receives, upon playing arm a, a random reward whose expected value is
(1)に従って、エージェントはアームaをプレイすると、期待値が
$$
\mu(m'_{a}[\theta^*])
$$
のランダム報酬を受け取ります。ここで、$\theta^* \in \Theta$ は未知のパラメータです。パラメータセット $\Theta$ は、$R^d$ の任意の閉集合です。期待報酬が最大のアームは最適と呼ばれます。エージェントの目的は、受け取る報酬を最大化するために、迅速に最適なアームを見つけることです。貪欲な行動
$$
\text{argmax}_{a \in A} \mu(m'_{a}[\hat{\theta}_t])
$$
は、最適なアームの選択を保証するために十分に探索しない不安定なアルゴリズムにつながる可能性があります。この問題は「楽観的アプローチ」に頼ることで対処できます。線形の場合において[8, 12]で説明されているように、楽観的アルゴリズムは、時刻$t$においてアームを選択することから成ります。  
$$
A_t = \text{argmax}_{a} \max_{\theta} E_{\theta}[R_t | A_t = a] \quad \text{s.t.} \quad \|\theta - \hat{\theta}_t\|_{M_t} \leq \rho(t),
$$
ここで、$\rho$ は適切な「ゆっくり増加する」関数です。  
$$
M_t = \sum_{k=1}^{t-1} m_{A_k} m'_{A_k}
$$  

は、最初の$t - 1$タイムステップに対応する設計行列であり、$\|v\|_M = v'Mv$は、正定値行列$M$によって誘導される行列ノルムを示します。$\|\theta - \hat{\theta}_t\|_{M_t} \leq \rho(t)$の領域は、推定されたパラメータ$\hat{\theta}_t$の周りの信頼楕円体です。このアプローチを線形リンク関数のケースを超えて一般化することは困難に思えます。特に、GLMでは、関連する信頼領域は単純な楕円体よりもパラメータ空間でより複雑な幾何学を持つ可能性があります。その結果、この種の楽観的アルゴリズムの利点は疑わしいようです。[3]  
ここで、以降の文脈においてlogは自然対数を示します。  
最大化することに注意してください。$\mu(m_a[\theta])$を凸信頼領域の上で最大化することは、$\mu(m_a[\theta])$を同じ領域で最大化することと同等です。したがって、計算上、このアプローチは線形の場合と同じくらい難しくはありません。  

別のアプローチは、各アームの期待報酬の上限信頼区間を直接決定し、次に  
$$
E_{\hat{\theta}_t}[R_t | A_t = a] + \rho(t) \|m_a\|_{M_{t-1}}
$$  
を最大化するアクション$a$を選択することです。線形の場合、2つのアプローチは同じ解に至ります[12]。興味深いことに、非線形バンディットの場合、2番目のアプローチがより適切に見えます。  
このセクションの残りでは、(1)で定義されたGLMバンディットモデルにこの2番目のアプローチを適用します。  
(3)に従って、GLMにおけるパラメータの最大準最尤推定量は、推定方程式の唯一の解です。  
$$
\sum_{k=1}^{t-1} \left( R_k - \mu(m'_{A_k}[\hat{\theta}_t]) \right) m_{A_k} = 0,
$$  
ここで、$A_1, \ldots, A_{t-1}$はこれまでにプレイされたアームを示し、$R_1, \ldots, R_{t-1}$は対応する報酬です。  
$g_t(\theta) = \sum_{k=1}^{t-1} \mu(m'_{A_k}[\theta]) m_{A_k}$を、推定されたパラメータ$\hat{\theta}_t$が$g_t(\hat{\theta}_t) = \sum_{k=1}^{t-1} R_k m_{A_k}$を満たすような可逆関数とします。したがって、$\hat{\theta}_t$が許容可能なパラメータの集合$\Theta$の外にある可能性があるため、  
$$
\hat{\theta}_t = g_t(\theta) - \frac{\sum_{k=1}^{t-1} R_k m_{A_k}}{M_{t-1}}
$$  

を用いて$\theta_{\tilde{t}}$を得ます。  

$$
\theta_{\tilde{t}} = \text{argmin}_{\theta \in \Theta} \left( g_t(\theta) - g_t(\hat{\theta}_t) \right)
$$  

において、$\theta_{\tilde{t}}$を求めます。  
$\hat{\theta}_t \in \Theta$（これは簡単に確認でき、私たちが扱った例では常に成り立ちました）であれば、$\theta_{\tilde{t}} = \hat{\theta}_t$とすることができます。これは重要です。なぜなら、$\theta_{\tilde{t}}$を計算することは非自明であり、この単純なチェックによってこの計算を省略できるからです。提案されたアルゴリズムGLM-UCBは次のようになります。  

**Algorithm 1 GLM-UCB** **アルゴリズム 1 GLM-UCB**  
1: Input: $\{m_a\}_{a \in A}$  
1: 入力: $\{m_a\}_{a \in A}$  
2: Play actions $a_1, \ldots, a_d$, receive $R_1, \ldots, R_d$.  
2: アクション$a_1, \ldots, a_d$をプレイし、$R_1, \ldots, R_d$を受け取ります。  
3: for $t > d$ do  
3: $t > d$のとき、  
4: Estimate $\hat{\theta}_t$ according to (6)  
4: (6)に従って$\hat{\theta}_t$を推定します。  
5: **if** $\hat{\theta}_t \in \Theta$ let $\theta_{\tilde{t}} = \hat{\theta}_t$ else compute $\theta_{\tilde{t}}$ according to (7)  
5: **もし** $\hat{\theta}_t \in \Theta$ ならば $\theta_{\tilde{t}} = \hat{\theta}_t$ とし、そうでなければ (7) に従って $\theta_{\tilde{t}}$ を計算します。  
6: Play the action $A_t = \text{argmax}_a \left( \mu(m'_{a}[\theta_{\tilde{t}}]) + \rho(t) \|m_a\|_{M_{t-1}} \right)$, receive $R_t$  
6: アクション $A_t = \text{argmax}_a \left( \mu(m'_{a}[\theta_{\tilde{t}}]) + \rho(t) \|m_a\|_{M_{t-1}} \right)$ をプレイし、$R_t$を受け取ります。  
7: end for  
7: 終了  
At time $t$, for each arm $a$, an upper bound $\mu(m'_{a}[\theta_{\tilde{t}}]) + \beta_t[a]$ is computed, where the “exploration bonus” $\beta_t[a] = \rho(t) \|m_a\|_{M_{t-1}}$ is the product of two terms.  
時刻$t$において、各アーム$a$に対して、上限$\mu(m'_{a}[\theta_{\tilde{t}}]) + \beta_t[a]$が計算されます。ここで、「探索ボーナス」$\beta_t[a] = \rho(t) \|m_a\|_{M_{t-1}}$は2つの項の積です。  
The quantity $\rho(t)$ is a slowly increasing function; we prove in Section 4 that $\rho(t)$ can be set to guarantee high-probability bounds on the expected regret (for the actual form used, see (8)).  
量$\rho(t)$はゆっくり増加する関数です。私たちはセクション4で、$\rho(t)$を設定することで期待される後悔の高確率境界を保証できることを証明します（実際に使用される形式については(8)を参照）。  
Note that the leading term of $\beta_t[a]$ is $\|m_a\|_{M_{t-1}}$ which decreases to zero as $t$ increases.  
$\beta_t[a]$の主な項は$\|m_a\|_{M_{t-1}}$であり、これは$t$が増加するにつれてゼロに減少します。  
As we are mostly interested in the case when the number of arms $K$ is much larger than the dimension $d$, the algorithm is simply initialized by playing actions $a_1, \ldots, a_d$ such that the vectors $m_{a_1}, \ldots, m_{a_d}$ form a basis of $M = \text{span}(m_a, a \in A)$.  
私たちは、アームの数$K$が次元$d$よりもはるかに大きい場合に主に興味があるため、アルゴリズムは単にアクション$a_1, \ldots, a_d$をプレイして、ベクトル$m_{a_1}, \ldots, m_{a_d}$が$M = \text{span}(m_a, a \in A)$の基底を形成するように初期化されます。  
Without loss of generality, here and in what follows we assume that the dimension of $M$ is equal to $d$.  
一般性を失うことなく、ここおよび以下では、$M$の次元が$d$に等しいと仮定します。  
Then, by playing $a_1, \ldots, a_d$ in the first $d$ steps the agent ensures that $M_t$ is invertible for all $t$.  
したがって、最初の$d$ステップで$a_1, \ldots, a_d$をプレイすることにより、エージェントはすべての$t$に対して$M_t$が可逆であることを保証します。  
An alternative strategy would be to initialize $M_0 = \lambda_0 I$, where $I$ is the $d \times d$ identify matrix.  
別の戦略は、$M_0 = \lambda_0 I$で初期化することであり、ここで$I$は$d \times d$の単位行列です。  

### 3.1 Discussion

The purpose of this section is to discuss some properties of Algorithm 1, and in particular the interpretation of the role played by $\|m_a\|_{M_{t-1}}$.
このセクションの目的は、アルゴリズム1のいくつかの特性を議論し、特に$\|m_a\|_{M_{t-1}}$が果たす役割の解釈を行うことです。  
**Generalizing UCB** The standard UCB algorithm for $K$ arms [2] can be seen as a special case of GLM-UCB where the vectors of covariates associated with the arms form an orthogonal system and $\mu(x) = x$.  
**UCBの一般化** $K$アームの標準UCBアルゴリズム[2]は、アームに関連する共変量のベクトルが直交系を形成し、$\mu(x) = x$である場合のGLM-UCBの特別なケースと見なすことができます。  
Indeed, take $d = K$, $A = \{1, \ldots, K\}$, define the vectors $\{m_a\}_{a \in A}$ as the canonical basis $\{e_a\}_{a \in A}$ of $R^d$, and take $\theta \in R^d$ the vector whose component $\theta_a$ is the expected reward for arm $a$.  
実際、$d = K$、$A = \{1, \ldots, K\}$とし、ベクトル$\{m_a\}_{a \in A}$を$R^d$の標準基底$\{e_a\}_{a \in A}$として定義し、$\theta \in R^d$をアーム$a$の期待報酬の成分$\theta_a$を持つベクトルとします。  

Then, $M_t$ is a diagonal matrix whose $a$-th diagonal element is the number $N_t(a)$ of times the $a$-th arm has been played up to time $t$.  
すると、$M_t$は対角行列であり、その$a$番目の対角要素は、時刻$t$までに$a$番目のアームがプレイされた回数$N_t(a)$です。  
Therefore, the exploration bonus in GLM-UCB is given by  
したがって、GLM-UCBにおける探索ボーナスは  
$$
\beta_t[a] = \rho(t) / \sqrt{N_t(a)}.
$$  
また、最大準最尤推定量$\hat{\theta}_t$は、すべての$a \in A$に対して$R_t[a] = \hat{\theta}_t(a)$を満たします。ここで、$R_t[a] = \frac{1}{N_t(a)} \sum_{k=1}^{N_t(a)} R_k$は、アーム$a$をプレイしている間に受け取った報酬の経験的平均です。アルゴリズム1は、よく知られたUCBアルゴリズムに還元されます。この場合、期待される累積後悔は、報酬の範囲が1で制約されていると仮定して、ゆっくり変化する関数$\rho$を$\rho(t) = \sqrt{2 \log(t)}$に設定することで制御できることが知られています[2]。  
**Generalizing linear bandits** Obviously, setting $\mu(x) = x$, we obtain a linear bandit model.  
**線形バンディットの一般化** **明らかに、$\mu(x) = x$と設定することで、線形バンディットモデルを得ます**。(GLBにおいて、逆リンク関数が恒等関数の場合、線形バンディットモデルになる...!:thinking:)  
In this case, assuming that $\Theta = R^d$, the algorithm will reduce to those described in the papers [8, 12].  
この場合、$\Theta = R^d$と仮定すると、アルゴリズムは文献[8, 12]で説明されているものに還元されます。  
In particular, the maximum quasi-likelihood estimator becomes the least-squares estimator and as noted earlier, the algorithm behaves identically to one which chooses the parameter optimistically within the confidence ellipsoid $\{\theta : \|\theta - \hat{\theta}_t\|_{M_t} \leq \rho(t)\}$.  
特に、最大準最尤推定量は最小二乗推定量となり、前述のように、アルゴリズムは信頼楕円体$\{\theta : \|\theta - \hat{\theta}_t\|_{M_t} \leq \rho(t)\}$内で楽観的にパラメータを選択するものと同様に振る舞います。  

**Dependence in the Number of Arms** In contrast to an algorithm such as UCB, Algorithm 1 does not need that all arms be played even once.  
**アームの数に依存すること** UCBのようなアルゴリズムとは対照的に、アルゴリズム1はすべてのアームが少なくとも一度はプレイされる必要はありません。  
To understand this phenomenon, observe that,  
この現象を理解するために、次のことに注意してください。  

$$
M_{t+1} = M_t + m_{A_t} m'_{A_t} \quad \text{and} \quad \|m_a\|^2_{M_{t-1}} = \|m_a\|^2_{M_{t-1}} - \frac{m'_{a} M_{t-1}^{-1} m_{A_t}}{(1 + \|m_{A_t}\|^2_{M_{t-1}})}
$$  

for any arm $a$.  
任意のアーム$a$に対して。  
Thus the exploration bonus $\beta_{t}[a] + 1$ decreases for all arms, except those which are exactly orthogonal to $m_{A_t}$ (in the $M_{t-1}$ metric).  
したがって、探索ボーナス$\beta_{t}[a] + 1$は、$m_{A_t}$に対して正確に直交するアームを除いて、すべてのアームに対して減少します。  
The decrease is most significant for arms that are colinear to $m_{A_t}$.  
この減少は、$m_{A_t}$に共線的なアームに対して最も顕著です。  
This explains why the regret bounds obtained in Theorems 1 and 2 below depend on $d$ but not on $K$.  
これが、以下の定理1および2で得られる後悔の境界が$d$には依存するが$K$には依存しない理由です。  

## 4 理論的分析

In this section we first give our finite sample regret bounds and then show how the algorithm can be tuned based on asymptotic arguments.  
このセクションでは、まず有限サンプルの後悔境界を示し、次に漸近的な議論に基づいてアルゴリズムを調整する方法を示します。

**4.1** **後悔境界**  
To quantify the performance of the GLM-UCB algorithm, we consider the cumulated (pseudo) regret defined as the expected difference between the optimal reward obtained by always playing an optimal arm and the reward received following the algorithm:  
GLM-UCBアルゴリズムの性能を定量化するために、最適なアームを常にプレイすることによって得られる最適な報酬と、アルゴリズムに従って受け取る報酬との期待される差として定義される累積（擬似）後悔を考えます：

$$
\text{Regret}_T = \sum_{t=1}^{T} \left[ \mu(m' a^* [\theta^*]) - \mu(m' A_t [\theta^*]) \right]  
$$

For the sake of the analysis, in this section we shall assume that the following assumptions hold:  
分析のために、このセクションでは以下の仮定が成り立つと仮定します：

**Assumption 1.** The link function $\mu : \mathbb{R} \to \mathbb{R}$ is continuously differentiable, Lipschitz with constant $k_\mu$ and such that $c_\mu = \inf_{\theta \in \Theta, a \in A} \dot{\mu}(m' a[\theta]) > 0$.  
**仮定 1.** リンク関数 $\mu : \mathbb{R} \to \mathbb{R}$ は連続的に微分可能で、定数 $k_\mu$ に対してリプシッツ連続であり、$c_\mu = \inf_{\theta \in \Theta, a \in A} \dot{\mu}(m' a[\theta]) > 0$ です。

For the logistic function $k_\mu = 1/4$, while the value of $c_\mu$ depends on $\sup_{\theta \in \Theta, a \in A} m' a[\theta]$.  
ロジスティック関数の場合、$k_\mu = 1/4$ であり、$c_\mu$ の値は $\sup_{\theta \in \Theta, a \in A} m' a[\theta]$ に依存します。

**Assumption 2.** The norm of covariates in $\{m_a : a \in A\}$ is bounded: there exists $c_m < \infty$ such that for all $a \in A$, $\|m_a\|_2 \leq c_m$.  
**仮定 2.** $\{m_a : a \in A\}$ の共変量のノルムは有界です：すべての $a \in A$ に対して、$\|m_a\|_2 \leq c_m < \infty$ となるような $c_m$ が存在します。

Finally, we make the following assumption on the rewards:  
最後に、報酬に関して以下の仮定をします：

**Assumption 3.** There exists $R_{\max} > 0$ such that for any $t \geq 1$, $0 \leq R_t \leq R_{\max}$ holds a.s. Let $\epsilon_t = R_t - \mu(m' A_t [\theta^*])$. For all $t \geq 1$, it holds that $E[\epsilon_t | m A_t, \epsilon_{t-1}, \ldots, \epsilon_1] = 0$ a.s.  
**仮定 3.** 任意の $t \geq 1$ に対して、$0 \leq R_t \leq R_{\max}$ がほぼ確実に成り立つような $R_{\max} > 0$ が存在します。$\epsilon_t = R_t - \mu(m' A_t [\theta^*])$ とします。すべての $t \geq 1$ に対して、$E[\epsilon_t | m A_t, \epsilon_{t-1}, \ldots, \epsilon_1] = 0$ がほぼ確実に成り立ちます。

As for the standard UCB algorithm, the regret can be analyzed in terms of the difference between the expected reward received playing an optimal arm and that of the best sub-optimal arm:  
標準のUCBアルゴリズムに関しては、後悔は最適なアームをプレイして得られる期待報酬と、最良の準最適アームの期待報酬との差として分析できます：

$$
\Delta(\theta^*) = \min_{a^*} \left[ \mu(m' a[\theta^*]) - \mu(m' a^* [\theta^*]) \right]  
$$

Theorem 1 establishes a high probability bound on the regret underlying using GLM-UCB with $\rho(t) = \frac{2 k_\mu R_{\max}}{c_\mu} \sqrt{2d \log(t) \log\left(\frac{2dT}{\delta}\right)}$,  
定理1は、$\rho(t) = \frac{2 k_\mu R_{\max}}{c_\mu} \sqrt{2d \log(t) \log\left(\frac{2dT}{\delta}\right)}$ を用いたGLM-UCBの後悔に対する高確率境界を確立します。

$$
\text{Regret}_T \leq (d + 1) R_{\max} + \Delta(C d \theta^2) \log\left(2 s T\right) \geq 1 - \delta  
$$

where $T$ is the fixed time horizon, $\kappa = \sqrt{3 + 2 \log(1 + \frac{2c_m}{\lambda_0})$ and $\lambda_0$ denotes the smallest eigenvalue of $\sum_{i=1}^{d} m_a[i] m_a'[i]$, which by our previous assumption is positive.  
ここで、$T$ は固定された時間のホライズンであり、$\kappa = \sqrt{3 + 2 \log(1 + \frac{2c_m}{\lambda_0})$ で、$\lambda_0$ は $\sum_{i=1}^{d} m_a[i] m_a'[i]$ の最小固有値を示し、これは前の仮定により正です。

**Theorem 1 (Problem Dependent Upper Bound).** Let $s = \max(1, \frac{c_m}{\lambda_0})$. Then, under Assumptions 1–3, for all $T \geq 1$, the regret satisfies:  
**定理 1（問題依存上限）。** $s = \max(1, \frac{c_m}{\lambda_0})$ とします。仮定 1–3 の下で、すべての $T \geq 1$ に対して、後悔は次のように満たされます：

$$
P\left(\text{Regret}_T \leq (d + 1) R_{\max} + \Delta(C d \theta^2) \log\left(2 s T\right)\right) \geq 1 - \delta  
$$

with $C = 32 \kappa^2 R c_m^2 k_\mu^2$.  
ここで、$C = 32 \kappa^2 R c_m^2 k_\mu^2$ です。

Note that the above regret bound depends on the true value of $\theta^*$ through $\Delta(\theta^*)$. The following theorem provides an upper-bound of the regret independently of the $\theta^*$.  
上記の後悔境界は、$\Delta(\theta^*)$ を通じて $\theta^*$ の真の値に依存します。次の定理は、$\theta^*$ に依存しない後悔の上限を提供します。

**Theorem 2 (Problem Independent Upper Bound).** Let $s = \max(1, \frac{c_m}{\lambda_0})$. Then, under Assumptions 1–3, for all $T \geq 1$, the regret satisfies  
**定理 2（問題非依存上限）。** $s = \max(1, \frac{c_m}{\lambda_0})$ とします。仮定 1–3 の下で、すべての $T \geq 1$ に対して、後悔は次のように満たされます：

$$
P\left(\text{Regret}_T \leq (d + 1) R_{\max} + C d \log(s T)\right) \geq 1 - \delta  
$$

with $C = 8 R_{\max} c_\mu k_\mu \kappa$.  
ここで、$C = 8 R_{\max} c_\mu k_\mu \kappa$ です。

The proofs of Theorems 1–2 can be found in the supplementary material. The main idea is to use the explicit form of the estimator given by (6) to show that  
定理1–2の証明は補足資料にあります。主なアイデアは、(6) によって与えられる推定量の明示的な形を使用して、次のことを示すことです：

$$
\left\| \mu(m' A_t [\theta^*]) - \mu(m' A_t [\hat{\theta}_t]) \right\| \leq k_{c_\mu} \mu \|m_{A_t}\| M_{t-1} \left\| m_{A_k} \epsilon_k \right\| M_{t-1}  
$$

Bounding the last term on the right-hand side is then carried out following the lines of [12].  
右辺の最後の項の上限は、[12] の手法に従って行われます。

**4.2** **漸近的上限信頼区間**  
Preliminary experiments carried out using the value of $\rho(t)$ defined equation (8), including the case where $\mu$ is the identity function –i.e., using the algorithm described by [8, 12], revealed poor performance for moderate sample sizes.  
式 (8) で定義された $\rho(t)$ の値を使用した予備実験、特に $\mu$ が恒等関数である場合（すなわち、[8, 12] で説明されたアルゴリズムを使用）では、中程度のサンプルサイズでの性能が悪いことが明らかになりました。

A look into the proof of the regret bound easily explains this observation as the mathematical involvement of the arguments is such that some approximations seem unavoidable, in particular several applications of the Cauchy-Schwarz inequality, leading to pessimistic confidence bounds.  
後悔境界の証明を見れば、この観察が簡単に説明されます。というのも、議論の数学的な関与は、いくつかの近似が避けられないように思われ、特にコーシー・シュワルツの不等式のいくつかの適用があり、悲観的な信頼区間につながるからです。

We provide here some asymptotic arguments that suggest to choose significantly smaller exploration bonuses, which will in turn be validated by the numerical experiments presented in Section 5.  
ここでは、かなり小さな探索ボーナスを選択することを示唆するいくつかの漸近的な議論を提供します。これは、セクション5で提示される数値実験によって検証されます。

Consider the canonical GLM associated with an inverse link function $\mu$ and assume that the vectors of covariates $X$ are drawn independently under a fixed distribution.  
逆リンク関数 $\mu$ に関連する標準的なGLMを考え、共変量のベクトル $X$ が固定分布の下で独立に引かれると仮定します。

This random design model would for instance describe the situation when the arms are drawn randomly from a fixed distribution.  
このランダムデザインモデルは、アームが固定分布からランダムに引かれる状況を説明します。

Standard statistical arguments show that the Fisher information matrix pertaining to this model is given by $J = E[\dot{\mu}(X' \theta^*) XX']$ and that the maximum likelihood estimate $\hat{\theta}_t$ is such that  
標準的な統計的議論は、このモデルに関連するフィッシャー情報行列が $J = E[\dot{\mu}(X' \theta^*) XX']$ であり、最尤推定量 $\hat{\theta}_t$ が次のようになることを示します：

$$
\sqrt{t-1} (\hat{\theta}_t - \theta^*) \xrightarrow{d} N(0, J^{-1})  
$$

where $\xrightarrow{d}$ stands for convergence in distribution. Moreover, $\sqrt{t-1} M_t \xrightarrow{d} \Sigma$ where $\Sigma = E[XX']$.  
ここで、$\xrightarrow{d}$ は分布収束を示します。さらに、$\sqrt{t-1} M_t \xrightarrow{d} \Sigma$ であり、$\Sigma = E[XX']$ です。

Hence, using the delta-method and Slutsky’s lemma  
したがって、デルタ法とスルツキーの補題を使用すると、

$$
\|m_a\|_{M_t^{-1}} \left[\mu(m' a' [\hat{\theta}_t]) - \mu(m' a [\theta^*])\right] \xrightarrow{d} N(0, \dot{\mu}(m' a [\theta^*]) \|m' a\|^{-2} J^{-1})  
$$

The right-hand variance is smaller than $k_\mu/c_\mu$ as $J \succeq c_\mu \Sigma$.  
右辺の分散は $J \succeq c_\mu \Sigma$ であるため、$k_\mu/c_\mu$ よりも小さくなります。

Hence, for any sampling distribution such that $J$ and $\Sigma$ are positive definite and sufficiently large $t$ and small $\delta$,  
したがって、$J$ と $\Sigma$ が正定値であり、十分に大きな $t$ と小さな $\delta$ を持つ任意のサンプリング分布に対して、

$$
P\left(\|m_a\|_{M_t^{-1}} \left[\mu(m' a' [\hat{\theta}_t]) - \mu(m' a [\theta^*])\right] > \frac{2k_\mu}{c_\mu} \log\left(\frac{1}{\delta}\right)\right)  
$$

is asymptotically bounded by $\delta$.  
は漸近的に $\delta$ によって制約されます。

Based on the above asymptotic argument, we postulate that using $\rho(t) = \frac{2k_\mu}{c_\mu} \log(t)$, i.e., inflating the exploration bonus by a factor of $\sqrt{k_\mu/c_\mu}$ compared to the usual UCB setting, is sufficient.  
上記の漸近的議論に基づいて、$\rho(t) = \frac{2k_\mu}{c_\mu} \log(t)$ を使用すること、すなわち通常のUCB設定と比較して探索ボーナスを $\sqrt{k_\mu/c_\mu}$ 倍にすることが十分であると仮定します。

This is the setting used in the simulations below.  
これは、以下のシミュレーションで使用される設定です。

## 5 Experiments 実験

To the best of our knowledge, there is currently no public benchmark available to test bandit methods on real world data.
私たちの知る限り、現在、実世界のデータに対してバンディット手法をテストするための公開ベンチマークは存在しません。
On simulated data, the proposed method unsurprisingly outperforms its competitors when the data is indeed simulated from a well-specified generalized linear model.
シミュレーションデータにおいて、提案された手法は、データが適切に指定された一般化線形モデルからシミュレーションされた場合、競合他社を驚くことなく上回ります。
In order to evaluate the potential of the method in more challenging scenarios, we thus carried out two experiments using real world datasets.
したがって、より困難なシナリオにおける手法の可能性を評価するために、実世界のデータセットを使用して2つの実験を実施しました。

-----  
**5.1** **Forest Cover Type Data 森林被覆タイプデータ**  
In this first experiment, we test the performance of the proposed method on a toy problem using the “Forest Cover Type dataset” from the UCI repository.
この最初の実験では、UCIリポジトリからの「森林被覆タイプデータセット」を使用して、提案された手法の性能をおもちゃの問題でテストします。
The dataset (centered and normalized with constant covariate added, resulting in 11-dimensional vectors, ignoring all categorical variables) has been partitioned into K = 32 clusters using unsupervised k-means.
データセット（定数共変量を追加して中心化および正規化され、11次元ベクトルとなり、すべてのカテゴリ変数を無視）は、教師なしk-meansを使用してK = 32クラスタに分割されました。
The values of the response variable for the data points assigned to each cluster are viewed as the outcomes of an arm while the centroid of the cluster is taken as the 11-dimensional vector of covariates characteristic of the arm.
各クラスタに割り当てられたデータポイントの応答変数の値は、アームの結果として見なされ、クラスタの重心はアームの特性を持つ11次元の共変量ベクトルとして取られます。
To cast the problem into the logistic regression framework, each response variable is binarized by associating the first class (“Spruce/Fir”) to a response R = 1 and all other six classes to R = 0.
この問題をロジスティック回帰の枠組みに変換するために、各応答変数は最初のクラス（「スプルース/ファー」）を応答R = 1に、他の6つのクラスをR = 0に関連付けることによって二値化されます。
The proportions of responses equal to 1 in each cluster (or, in other word, the expected reward associated with each arm) ranges from 0.354 to 0.992, while the proportion on the complete set of 581,012 data points is equal to 0.367.
各クラスタにおける応答が1である割合（または、言い換えれば、各アームに関連する期待報酬）は0.354から0.992の範囲であり、581,012のデータポイント全体の割合は0.367です。
In effect, we try to locate as fast as possible the cluster that contains the maximal proportion of trees from a given species.
実際、私たちは特定の種の木の最大割合を含むクラスタをできるだけ早く特定しようとします。
We are faced with a 32-arm problem in a 11-dimensional space with binary rewards.
私たちは、11次元空間における32アームの問題に直面しています。
Obviously, the logistic regression model is not satisfied, although we do expect some regularity with respect to the position of the cluster’s centroid as the logistic regression trained on all data reaches a 0.293 misclassification rate.
明らかに、ロジスティック回帰モデルは満たされていませんが、すべてのデータで訓練されたロジスティック回帰が0.293の誤分類率に達するため、クラスタの重心の位置に関しては何らかの規則性を期待しています。

2000  
UCB  
GLM−UCB  
1500  
ε−greedy  
1000  
500  
0  
0 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000  
t  
6000 GLM−UCB  
UCB  
4000  
2000  
0  
2 4 6 8 10 12 14 16 18  
arm a  
Figure 1: Top: Regret of the UCB, GLM-UCB and the ǫ-greedy algorithms.
図1: 上部: UCB、GLM-UCB、およびǫ-greedyアルゴリズムの後悔。
Bottom: Frequencies of the 20 best arms draws using the UCB and GLM-UCB.
下部: UCBおよびGLM-UCBを使用した20の最良アームの引きの頻度。

We compare the performance of three algorithms.
私たちは3つのアルゴリズムの性能を比較します。
First, the GLM-UCB algorithm, with parameters tuned as indicated in Section 4.2.
まず、セクション4.2で示されたようにパラメータを調整したGLM-UCBアルゴリズムです。
Second, the standard UCB algorithm that ignores the covariates.
次に、共変量を無視する標準UCBアルゴリズムです。
Third, an ǫ-greedy algorithm that performs logistic regression and plays the best estimated action, $A_t = \arg\max_a \mu(m'_{a}[\theta][\hat{t}])$, with probability $1 - \epsilon$ (with $\epsilon = 0.1$).
第三に、ロジスティック回帰を実行し、最良の推定アクションをプレイするǫ-greedyアルゴリズムです。
We observe in the top graph of Figure 1 that the GLM-UCB algorithm achieves the smallest average regret by a large margin.
図1の上部グラフで、GLM-UCBアルゴリズムが大きな差で最小の平均後悔を達成していることがわかります。
When the parameter is well estimated, the greedy algorithm may find the best arm in little time and then leads to small regrets.
パラメータが適切に推定されると、貪欲アルゴリズムは短時間で最良のアームを見つけ、その後小さな後悔につながる可能性があります。
However, the exploration/exploitation tradeoff is not correctly handled by the ǫ-greedy approach causing a large variability in the regret.
しかし、探索/活用のトレードオフはǫ-greedyアプローチによって適切に処理されず、後悔に大きな変動を引き起こします。
The lower plot of Figure 1 shows the number of times each of the 20 best arms have been played by the UCB and GLM-UCB algorithms.
図1の下部プロットは、UCBおよびGLM-UCBアルゴリズムによってプレイされた20の最良アームの回数を示しています。
The arms are sorted in decreasing order of expected reward.
アームは期待報酬の降順にソートされています。
It can be observed that GML-UCB only plays a small subset of all possible arms, concentrating on the bests.
GML-UCBはすべての可能なアームの小さなサブセットのみをプレイし、最良のアームに集中していることが観察できます。
This behavior is made possible by the predictive power of the covariates: by sharing information between arms, it is possible to obtain sufficiently accurate predictions of the expected rewards of all actions, even for those that have never (or rarely) been played.
この動作は共変量の予測力によって可能になります: アーム間で情報を共有することにより、すべてのアクションの期待報酬の十分に正確な予測を得ることが可能です。

|Col1|GLM−UCB UCB|Col3|GLM−UCB UCB|
|---|---|---|---|
|||||  

-----  
**5.2** **Internet Advertisement Data インターネット広告データ**  
In this experiment, we used a large record of the activity of internet users provided by a major ISP.
この実験では、大手ISPが提供するインターネットユーザーの活動の大規模な記録を使用しました。
The original dataset logs the visits to a set of 1222 pages over a six days period corresponding to about $5.10^8$ page visits.
元のデータセットは、約$5.10^8$ページ訪問に相当する6日間の期間にわたる1222ページの訪問を記録しています。
The dataset also contains a record of the users clicks on the ads that were presented on these pages.
データセットには、これらのページに表示された広告に対するユーザーのクリックの記録も含まれています。
We worked with a subset of 208 ads and $3.10^5$ users.
私たちは208の広告と$3.10^5$のユーザーのサブセットで作業しました。
The pages (ads) were partitioned in 10 (respectively, 8) categories using Latent Dirichlet Allocation [15] applied to their respective textual content (in the case of ads, the textual content was that of the page pointed to by the ad’s link).
ページ（広告）は、それぞれのテキストコンテンツに適用された潜在ディリクレ配分法[15]を使用して10（それぞれ8）カテゴリに分割されました（広告の場合、テキストコンテンツは広告のリンクが指すページのものでした）。
This second experiment is much more challenging, as the predictive power of the sole textual information turns out to be quite limited (for instance, Poisson regression trained on the entire data does not even correctly identify the best arm).
この2番目の実験は、単独のテキスト情報の予測力が非常に限られているため、はるかに困難です（たとえば、全データで訓練されたポアソン回帰は最良のアームを正しく特定することすらできません）。

The action space is composed of the 80 pairs of pages and ads categories: when a pair is chosen, it is presented to a group of 50 users, randomly selected from the database, and the reward is the number of recorded clicks.
アクション空間は、ページと広告カテゴリの80ペアで構成されています: ペアが選択されると、データベースからランダムに選択された50人のユーザーのグループに提示され、報酬は記録されたクリックの数です。
As the average reward is typically equal to 0.15, we use a logarithmic link function corresponding to Poisson regression.
平均報酬が通常0.15に等しいため、ポアソン回帰に対応する対数リンク関数を使用します。
The vector of covariates for each pair is of dimension 19: it is composed of an intercept followed by the concatenation of two vectors of dimension 10 and 8 representing, respectively, the categories of the pages and the ads.
各ペアの共変量ベクトルは次元19で構成されています: それは、ページと広告のカテゴリをそれぞれ表す次元10と8の2つのベクトルの連結に続く切片で構成されています。
In this problem, the covariate vectors do not span the entire space; to address this issue, it is sufficient to consider the pseudo-inverse of $M_t$ instead of the inverse.
この問題では、共変量ベクトルは全空間をスパンしません; この問題に対処するためには、逆行列の代わりに$M_t$の擬似逆行列を考慮するだけで十分です。

On this data, we compared the GLM-UCB algorithm with the two alternatives described in Section 5.1.
このデータに対して、私たちはGLM-UCBアルゴリズムをセクション5.1で説明した2つの代替手段と比較しました。
Figure 2 shows that GLM-UCB once again outperforms its competitors, even though the margin over UCB is now less remarkable.
図2は、GLM-UCBが再び競合他社を上回っていることを示していますが、UCBに対するマージンは現在それほど顕著ではありません。
Given the rather limited predictive power of the covariates in this example, this is an encouraging illustration of the potential of techniques which use vectors of covariates in real-life applications.
この例における共変量の予測力がかなり限られていることを考えると、これは実際のアプリケーションで共変量ベクトルを使用する技術の可能性を示す励みとなる例です。

3000  
UCB  
GLM−UCB  
2000 ε−greedy  
1000  
0  
0 1000 2000 3000 4000 5000  
t  
Figure 2: Comparison of the regret of the UCB, GLM-UCB and the ǫ-greedy (ǫ = 0.1) algorithm on the advertisement dataset.
図2: 広告データセットにおけるUCB、GLM-UCB、およびǫ-greedy（ǫ = 0.1）アルゴリズムの後悔の比較。

## 6 Conclusions 結論

We have introduced an approach that generalizes the linear regression model studied by [10, 8, 12].
私たちは、[10, 8, 12]で研究された線形回帰モデルを一般化するアプローチを導入しました。
As in the original UCB algorithm, the proposed GLM-UCB method operates directly in the reward space.
元のUCBアルゴリズムと同様に、提案されたGLM-UCBメソッドは報酬空間で直接動作します。
We discussed how to tune the parameters of the algorithm to avoid exaggerated optimism, which would slow down learning.
私たちは、学習を遅くする誇張された楽観主義を避けるために、アルゴリズムのパラメータを調整する方法について議論しました。
In the numerical simulations, the proposed algorithm was shown to be competitive and sufficiently robust to tackle real-world problems.
数値シミュレーションでは、提案されたアルゴリズムが競争力があり、実世界の問題に対処するのに十分な堅牢性を持つことが示されました。
An interesting open problem (already challenging in the linear case) consists in tightening the theoretical results obtained so far in order to bridge the gap between the existing (pessimistic) confidence bounds and those suggested by the asymptotic arguments presented in Section 4.2, which have been shown to perform satisfactorily in practice.
興味深い未解決の問題（線形の場合ですでに難しい）は、これまで得られた理論的結果を強化し、既存の（悲観的な）信頼区間と、実際に満足のいく性能を示しているセクション4.2で提示された漸近的な議論によって示唆された信頼区間とのギャップを埋めることです。

**Acknowledgments**  
**謝辞**  
This work was supported in part by AICML, AITF, NSERC, PASCAL2 under n[o]216886, the DARPA GALE project under n[o]HR0011-08-C-0110 and Orange Labs under contract n[o]289365.
この研究は、AICML、AITF、NSERC、PASCAL2のn[o]216886、DARPA GALEプロジェクトのn[o]HR0011-08-C-0110、Orange Labsの契約n[o]289365の一部によって支援されました。

-----  
**References**  
**参考文献**  
[1] T.L. Lai and H. Robbins. Asymptotically efficient adaptive allocation rules. Advances in _Applied Mathematics, 6(1):4–22, 1985._  
[2] P. Auer, N. Cesa-Bianchi, and P. Fischer. Finite-time analysis of the multiarmed bandit problem. Machine Learning, 47(2):235–256, 2002.  
[3] N. Cesa-Bianchi and G. Lugosi. Prediction, learning, and games. Cambridge Univ Pr, 2006.  
[4] J. Audibert, R. Munos, and Cs. Szepesv´ari. Tuning bandit algorithms in stochastic environments. Lecture Notes in Computer Science, 4754:150, 2007.  
[5] C.C. Wang, S.R. Kulkarni, and H.V. Poor. Bandit problems with side observations. IEEE _Transactions on Automatic Control, 50(3):338–355, 2005._  
[6] J. Langford and T. Zhang. The epoch-greedy algorithm for multi-armed bandits with side information. Advances in Neural Information Processing Systems, pages 817–824, 2008.  
[7] S. Pandey, D. Chakrabarti, and D. Agarwal. Multi-armed bandit problems with dependent arms. International Conference on Machine learning, pages 721–728, 2007.  
[8] V. Dani, T.P. Hayes, and S.M. Kakade. Stochastic linear optimization under bandit feedback. _Conference on Learning Theory, 2008._  
[9] S.M. Kakade, S. Shalev-Shwartz, and A. Tewari. Efficient bandit algorithms for online multiclass prediction. In Proceedings of the 25th International Conference on Machine _learning, pages 440–447. ACM, 2008._  
[10] P. Auer. Using confidence bounds for exploitation-exploration trade-offs. Journal of Machine _Learning Research, 3:397–422, 2002._  
[11] Y. Abbasi-Yadkori, A. Antos, and Cs. Szepesv´ari. Forced-exploration based algorithms for playing in stochastic linear bandits. In COLT Workshop on On-line Learning with Limited _Feedback, 2009._  
[12] P. Rusmevichientong and J.N. Tsitsiklis. Linearly parameterized bandits. Mathematics of _Operations Research, 35(2):395–411, 2010._  
[13] P. McCullagh and J. A. Nelder. Generalized Linear Models. Chapman and Hall, 1989.  
[14] K. Chen, I. Hu, and Z. Ying. Strong consistency of maximum quasi-likelihood estimators in generalized linear models with fixed and adaptive designs. _Annals of Statistics,_ 27(4):1155–1163, 1999.  
[15] David M. Blei, Andrew Y. Ng, and Michael I. Jordan. Latent Dirichlet allocation. Advances _in Neural Information Processing Systems, 14:601–608, 2002._  
[16] V.H. De La Pena, M.J. Klass, and T.L. Lai. Self-normalized processes: exponential inequalities, moment bounds and iterated logarithm laws. Annals of Probability, 32(3):1902–1933, 2004.  
[17] P. Rusmevichientong and J.N. Tsitsiklis. Linearly parameterized bandits. Arxiv preprint arXiv:0812.3465v2, 2008.  

```
