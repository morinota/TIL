refs: https://arxiv.org/html/2409.05181v3

# Sliding-Window Thompson Sampling for Non-Stationary Settings
# スライディングウィンドウ・トンプソンサンプリングによる非定常設定

## Abstract 要約

Non-stationary multi-armed bandits(NS-MABs) model sequential decision-making problems in which the expected rewards of a set of actions, a.k.a.arms, evolve over time.
非定常マルチアームバンディット（NS-MAB）は、**アクションのセット（いわゆるアーム）の期待報酬が時間とともに変化する逐次的な意思決定問題**をモデル化します。
In this paper, we fill a gap in the literature by providing a novel analysis of Thompson sampling-inspired (TS) algorithms for NS-MABs that both corrects and generalizes existing work.
本論文では、既存の研究を修正し一般化する非定常マルチアームバンディット（NS-MAB）向けのトンプソンサンプリング（TS）アルゴリズムに関する新しい分析を提供することで、文献のギャップを埋めます。
Specifically, we study the cumulative frequentist regret of two algorithms based on sliding-window TS approaches with different priors, namely Beta-SWTS and $\gamma$-SWGTS.
具体的には、**異なる事前分布を持つスライディングウィンドウTSアプローチに基づく2つのアルゴリズム**、すなわちBeta-SWTSと$\gamma$-SWGTSの累積頻度主義的後悔を研究します。
We derive a unifying regret upper bound for these algorithms that applies to any arbitrary NS-MAB (with either Bernoulli or subgaussian rewards).
これらのアルゴリズムに対して、任意の非定常マルチアームバンディット（ベルヌーイ報酬またはサブガウス報酬のいずれかを持つ）に適用可能な統一的な後悔の上限を導出します。
Our result introduces new indices that capture the inherent sources of complexity in the learning problem.
私たちの結果は、学習問題における固有の複雑さの源を捉える新しい指標を導入します。
Then, we specialize our general result to two of the most common NS-MAB settings: the abruptly changing and the smoothly changing environments, showing that it matches state-of-the-art results.
次に、一般的な結果を最も一般的な2つの非定常マルチアームバンディット設定、すなわち急激に変化する環境と滑らかに変化する環境に特化し、最先端の結果と一致することを示します。
Finally, we evaluate the performance of the analyzed algorithms in simulated environments and compare them with state-of-the-art approaches for NS-MABs.
最後に、分析したアルゴリズムの性能をシミュレーション環境で評価し、非定常マルチアームバンディットに対する最先端のアプローチと比較します。

<!-- ここまで読んだ! -->

## IIntroduction はじめに

A multi-armed bandit [MAB, 32] problem is a sequential game between a learner and an environment. 
マルチアームバンディット（MAB）問題は、学習者と環境の間の逐次ゲームです。
In each round $t$, the learner first chooses an action, often called arm, and the environment then reveals a reward. 
各ラウンド$t$において、学習者はまずアクション（通常はアームと呼ばれる）を選択し、環境はその後報酬を明らかにします。
The goal of the learner is to balance exploration and exploitation, minimizing the expected cumulative regret, 
学習者の目標は、探索と活用のバランスを取り、期待される累積後悔を最小化することです。
defined as the performance difference, expressed in expected rewards, between playing the optimal arm and the learner. 
これは、最適なアームをプレイすることと学習者の間の期待報酬で表されるパフォーマンスの差として定義されます。
These algorithms have traditionally been studied in stationary settings where the environment does not change over time. 
**これらのアルゴリズムは、環境が時間とともに変化しない定常的な設定で伝統的に研究されてきました。**
As a consequence, the optimal arm $i^*$ is constant and does not depend on the round $t$. 
その結果、**最適なアーム $i^*$ は一定**であり、ラウンド$t$には依存しません。(=一番良いアームが時間によって変わらない!:thinking:)
However, many real-world applications, such as online advertising [37, 30], healthcare [35, 16, 18, 27] and dynamic pricing [21, 12], operate in environments that are changing over time. 
しかし、オンライン広告[37, 30]、ヘルスケア[35, 16, 18, 27]、動的価格設定[21, 12]などの**多くの実世界のアプリケーションは、時間とともに変化する環境で動作します**。
These are often referred to as non-stationary MABs (NS-MABs), where the world evolves independently of the actions taken by the learner. 
これらはしばしば**非定常マルチアームバンディット（NS-MAB）**と呼ばれ、**世界は学習者が取ったアクションとは独立して進化**します。("独立"っていうのは、学習者のアクションによる影響とは別で、環境が変化するってことか...!!:thinking:)
As a consequence, the optimal arm $i^*(t)$ is potentially different in every round $t$, making the decision problem more challenging. 
その結果、最適なアーム $i^*(t)$ は各ラウンド $t$ で異なる可能性があり、意思決定問題がより困難になります。
This requires the design of learning algorithms able to adapt to environment modifications. 
これには、**環境の変更に適応できる学習アルゴリズムの設計が必要**です。

<!-- ここまで読んだ! -->

In the past years, the bandit literature focused on the design of algorithms that handle specific classes of NS-MABs characterized by certain regularity conditions. 
過去数年間、バンディット文献は、**特定の規則性条件によって特徴付けられるNS-MAB**の特定のクラスを処理するアルゴリズムの設計に焦点を当ててきました。(Sliding window系手法ってシンプルだけど、やや後発なのか...!!:thinking:)
The piecewise-constant abruptly changing MABs [23, 40, 33, 6, 10, 11] are characterized by expected rewards that remain constant during some rounds and change at unknown rounds, called breakpoints. 
区分定数的に急激に変化するMAB[23, 40, 33, 6, 10, 11]は、いくつかのラウンドで期待報酬が一定であり、未知のラウンドで変化することが特徴です。これらのラウンドはブレークポイントと呼ばれます。
Another form of regularity are the smoothly changing MABs [15, 48] where the expected rewards vary by a limited amount across rounds. 
もう一つの規則性の形態は、期待報酬がラウンド間で限られた量だけ変化する滑らかに変化するMAB[15, 48]です。
Other forms of regularity include the rising [26, 36] and rotting [45] MABs, where the expected rewards can only increase or decrease in time, respectively, and the MABs with bounded variation [10], where the expected reward is constrained to have a finite cumulative variation over the learning horizon. 
他の規則性の形態には、期待報酬が時間とともに増加または減少することしかできない上昇[26, 36]および腐敗[45]MAB、そして期待報酬が学習のホライズンにわたって有限の累積変動を持つように制約される有界変動のMAB[10]が含まれます。
Several algorithmic approaches have been adopted for addressing regret minimization in NS-MABs [e.g., 23, 15, 10, 48]. 
NS-MABにおける後悔最小化に対処するために、いくつかのアルゴリズム的アプローチが採用されています[e.g., 23, 15, 10, 48]。
Among them, Thompson sampling (TS) [47] is one of the most widely used bandit algorithms for its simplicity in implementation and its good empirical performance. 
その中でも、**トンプソンサンプリング（TS）[47]は、実装の簡便さと良好な経験的パフォーマンスのために最も広く使用されているバンディットアルゴリズムの一つ**です。
However, the classical TS algorithm is devised for stationary MABs where they enjoy strong theoretical guarantees [29, 4, 5]. 
**しかし、古典的なTSアルゴリズムは、強力な理論的保証を享受する定常MAB用に設計されています**[29, 4, 5]。
Variations to the classical TS have been proposed to tackle NS-MABs including sliding-window [48] and discounted [39, 38, 17] approaches. 
**古典的なTSのバリエーションが、スライディングウィンドウ[48]や割引[39, 38, 17]アプローチを含むNS-MABに対処するために提案**されています。
These algorithms come often with theoretical guarantees for specific classes of NS-MABs, namely piecewise-constant abruptly changing and smoothly changing. 
これらのアルゴリズムは、しばしば特定のクラスのNS-MAB、すなわち区分定数的に急激に変化するものと滑らかに変化するものに対する理論的保証を伴います。

<!-- ここまで読んだ! -->

### Original Contributions 本論文のオリジナルな貢献

In this paper, differently from what is often done in literature, we provide a unifying analysis of sliding-window TS algorithms that does not rely on the specific form of non-stationarity (namely piecewise-constant abruptly changing and smoothly changing). 
本論文では、文献でしばしば行われることとは異なり、**特定の非定常性の形態（すなわち区分定数的に急激に変化するものと滑らかに変化するもの）に依存しないスライディングウィンドウTSアルゴリズム**の統一的な分析を提供します。
(なるほど、SW-TS系の手法の強みって、非定常性の形態に依存しないってことなのか...!!:thinking:)
Our novel analysis shed lights on the inherent complexity of the regret minimization problem in general NS-MABs and introduces new quantities to characterize quantitatively such a complexity. 
私たちの新しい分析は、一般的なNS-MABにおける後悔最小化問題の固有の複雑さに光を当て、その複雑さを定量的に特徴付ける新しい量を導入します。
Furthermore, we extend and correct the original analysis of Trovò et al. [48]. 
さらに、私たちはTrovòら[48]の元の分析を拡張し、修正します。
In Appendix D, we show that some passages of the analysis by Trovò et al. [48] are incorrect. 
付録Dでは、Trovòら[48]の分析のいくつかの部分が不正確であることを示します。
Finally, we show how the state-of-the-art results for the specific forms of non-stationarity (namely piecewise-constant abruptly changing and smoothly changing) can be retrieved as a particular case of our analysis. 
最後に、特定の非定常性の形態（すなわち区分定数的に急激に変化するものと滑らかに変化するもの）に対する最先端の結果が、私たちの分析の特別なケースとして再取得できる方法を示します。

<!-- ここまで読んだ! -->

The content of the paper is summarized as follows: 
本論文の内容は以下のように要約されます：

- In Section II, we survey the related works on TS algorithms and approaches for regret minimization in NS-MABs. 
  - セクションIIでは、TSアルゴリズムとNS-MABにおける後悔最小化のアプローチに関する関連研究を調査します。
- In Section III, we provide the setting, the assumptions on the reward distributions, and the definition of cumulative regret. 
  - セクションIIIでは、設定、報酬分布に関する仮定、および累積後悔の定義を提供します。
- In Section IV, we describe two TS-inspired algorithms, namely Beta-SWTS and $\gamma$-SWGTS based on a sliding-window approach, exploiting the $\tau$ (being $\tau$ the window size) most recent samples to estimate the expected rewards. 
  - セクションIVでは、スライディングウィンドウアプローチに基づくBeta-SWTSと$\gamma$-SWGTSという2つのTSに触発されたアルゴリズムを説明し、期待報酬を推定するために$\tau$（$\tau$はウィンドウサイズ）の最も最近のサンプルを利用します。

- In the first part of Section V, we introduce new quantities to characterize how complex is to learn with sliding-window algorithms in an NS-MAB with expected rewards evolving with no particular form of non-stationarity. 
  - セクションVの前半では、特定の非定常性の形態を持たない期待報酬が進化するNS-MABにおいて、スライディングウィンドウアルゴリズムで学習することがどれほど複雑であるかを特徴付ける新しい量を導入します。
  In particular, we define two sets, namely the learnable set and the unlearnable set (Definition V.1), to describe in which rounds an algorithm exploiting the most recent samples only is expected to identify the optimal arm. 
  特に、最も最近のサンプルのみを利用するアルゴリズムが最適なアームを特定することが期待されるラウンドを説明するために、学習可能なセットと学習不可能なセット（定義V.1）という2つのセットを定義します。
  Furthermore, we define a new suboptimality gap notion, $\Delta_{\tau}$ (Definition V.2) that will be employed in the analysis. 
  さらに、分析で使用される新しい非最適性ギャップの概念$\Delta_{\tau}$（定義V.2）を定義します。

- In the second part of Section V, we derive novel unifying regret upper bounds of the Beta-SWTS and $\gamma$-SWGTS algorithms described in Section IV, for Bernoulli and subgaussian rewards, respectively. 
  - セクションVの後半では、セクションIVで説明したBeta-SWTSおよび$\gamma$-SWGTSアルゴリズムの新しい統一的な後悔上限を、ベルヌーイおよびサブガウス報酬に対して導出します。
  Our analysis exploits the quantities previously defined to characterize the complexity of the learning problem and makes no assumption on the underlying form of non-stationarity. 
  私たちの分析は、学習問題の複雑さを特徴付けるために以前に定義された量を利用し、基礎となる非定常性の形態に関する仮定を行いません。

- We leverage the results of Section V to derive regret upper bounds for the abruptly changing NS-MABs (Section VI) and the smoothly changing NS-MABs (Section VII). 
  - セクションVの結果を利用して、急激に変化するNS-MAB（セクションVI）および滑らかに変化するNS-MAB（セクションVII）の後悔上限を導出します。
  Moreover, we show how our bounds are comparable with the state-of-the-art ones derived with analyses tailored for the specific form of non-stationarity. 
  さらに、私たちの境界が特定の非定常性の形態に合わせた分析から導出された最先端のものとどのように比較可能であるかを示します。

- In Section VIII, we experimentally compare the performance of the analyzed algorithms with those in the bandit literature that are devised to learn in non-stationary scenarios. 
  - セクションVIIIでは、分析したアルゴリズムのパフォーマンスを、非定常シナリオで学習するために設計されたバンディット文献のアルゴリズムと実験的に比較します。

The proofs of the results presented in the main paper are reported in Appendix A and B. 
本論文で提示された結果の証明は、付録AおよびBに記載されています。

<!-- ここまで読んだ! -->

## IIRelated works II 関連研究

In this section, we survey the main related works about TS and approaches for regret minimization in NS-MABs. 
このセクションでは、TSに関する主な関連研究と、NS-MABにおける後悔最小化のアプローチを調査します。

### II-A Thompson Sampling

TS was introduced in 1933 [47] for allocating experimental effort in online sequential decision-making problems, and its effectiveness has been investigated both empirically [14,44] and theoretically [5,29] only in the last decades. 
TSは1933年に[47]オンライン逐次意思決定問題における実験的努力の配分のために導入され、その効果は過去数十年にわたり、実証的[14,44]および理論的[5,29]に調査されてきました。
The algorithm has found widespread applications in various fields, including online advertising [25,2,3], clinical trials [8], recommendation systems [30] and hyperparameter tuning for machine learning methods [28]. 
**このアルゴリズムは、オンライン広告[25,2,3]、臨床試験[8]、推薦システム[30]、および機械学習手法のハイパーパラメータ調整[28]など、さまざまな分野で広く応用**されています。
TS is optimal in the stationary case, i.e., achieving instance-dependent regret matching the lower bound [31]. 
**TSは定常状態の場合に最適**であり、すなわち、インスタンス依存の後悔が下限[31]に一致することを達成します。
However, it has been shown in multiple cases that in NS-MABs [24,48,34] or in adversarial settings [13] it provides poor performances in terms of regret. 
しかし、**NS-MABs[24,48,34]や敵対的設定[13]においては、後悔の観点から性能が悪いことが複数のケースで示されています**。(non-stationary環境やadversarial環境では、TSはあまり強くないのか...!!:thinking:)

<!-- ここまで読んだ! -->

### II-B 非定常バンディット(Non-Stationary Bandits)

Lately,UCB1andTSalgorithms inspired the development of techniques to face the inherent complexities of NS-MABs[50]. 
最近、UCB1およびTSアルゴリズムは、NS-MABs（非定常マルチアームバンディット）の固有の複雑さに対処するための技術の開発を促しました[50]。
The main idea behind these newly crafted algorithms is to forget past observations, removing samples from the statistics of the arms’ expected reward. 
**これらの新たに作成されたアルゴリズムの主なアイデアは、過去の観測を忘れ、アームの期待報酬の統計からサンプルを除去すること**です。

Two main approaches are present in the bandit literature to forget past observations: passive and active. 
**過去の観測を忘れるためのバンディット文献には、主に2つのアプローチがあります：受動的アプローチと能動的アプローチ**です。

The former iteratively discards the information coming from the far past, making decisions using only the most recent samples coming from the arms selected by the algorithms. 
前者は、遠い過去からの情報を反復的に廃棄し、アルゴリズムによって選択された**アームからの最新のサンプルのみを使用して意思決定を行います。**
Examples of such a family of algorithms are Discounted-TS[39], DUCB[24], which employ a multiplicative discount factor to reduce the impact of samples seen in the past. 
このようなアルゴリズムの例としては、Discounted-TS[39]やDUCB[24]があり、これらは過去に見たサンプルの影響を減少させるために乗法的割引因子を使用します。
It has been shown that these algorithms achieve regret of order $O(\sqrt{\Upsilon_{T}T}\log(T))$ in piecewise-constant abruptly changing environments, where $\Upsilon_{T}$ is the number breakpoint present during the learning horizon $T$. 
これらのアルゴリズムは、区分定数の急激に変化する環境において、$O(\sqrt{\Upsilon_{T}T}\log(T))$の後悔を達成することが示されています。ここで、$\Upsilon_{T}$は学習ホライズン$T$の間に存在するブレークポイントの数です。
Finally, SW-UCB[24] used a sliding-window approach in combination with an upper confidence bound to get a regret of order $O(\sqrt{\Upsilon_{T}T\log(T)})$ in the same setting. 
最後に、SW-UCB[24]は、スライディングウィンドウアプローチを上限信頼区間と組み合わせて使用し、同じ設定で$O(\sqrt{\Upsilon_{T}T\log(T)})$の後悔を得ました。

<!-- ここまで読んだ! -->

Instead, the active approach encompasses the use of change-detection techniques[9] to decide when it is the case to discard old samples. 
一方、能動的アプローチは、古いサンプルを廃棄するタイミングを決定するために変化検出技術[9]を使用します。
This occurs when a sufficiently large change affects the arms’ expected rewards. 
これは、十分に大きな変化がアームの期待報酬に影響を与えるときに発生します。
Among the active approaches to deal with the abruptly changing bandits, we mention CUSUM-UCB[33] and BR-MAB[40]. 
急激に変化するバンディットに対処するための能動的アプローチの中で、CUSUM-UCB[33]とBR-MAB[40]を挙げます。
They achieve a regret of order $O\left(\sqrt{\Upsilon_{T}T\log(\frac{T}{\Upsilon_{T}})}\right)$. 
これらは、$O\left(\sqrt{\Upsilon_{T}T\log(\frac{T}{\Upsilon_{T}})}\right)$の後悔を達成します。
Instead, in the same setting, GLR-klUCB[11], based on the use of KL-UCB as a bandit selection algorithm and a nonparametric change point method, achieve an $O(\sqrt{\Upsilon_{T}T\log(T)})$ regret. 
同じ設定の中で、KL-UCBをバンディット選択アルゴリズムとして使用し、非パラメトリック変化点法に基づくGLR-klUCB[11]は、$O(\sqrt{\Upsilon_{T}T\log(T)})$の後悔を達成します。
Another approach that is worth mentioning is RExp3[10], which builds on Exp3[7], adding scheduled restarts to the original algorithm, and it handles arbitrary evolutions of the expected rewards as long as they are constrained within $[0,1]$ and the learner knows the total variation $V_{T}$ of the expected reward, providing an $O(V_{T}^{\frac{1}{3}}T^{\frac{2}{3}})$ regret. 
言及する価値のある別のアプローチはRExp3[10]で、これはExp3[7]に基づき、元のアルゴリズムにスケジュールされた再起動を追加し、期待報酬の任意の進化を扱います。期待報酬が$[0,1]$に制約され、学習者が期待報酬の総変動$V_{T}$を知っている限り、$O(V_{T}^{\frac{1}{3}}T^{\frac{2}{3}})$の後悔を提供します。
Finally, different approaches to developing TS-like algorithms in NS-MABs resort to de-prioritizing information that more quickly loses usefulness and deriving a bound on the Bayesian regret of the algorithm. 
最後に、NS-MABsにおけるTSのようなアルゴリズムを開発するための異なるアプローチは、より早く有用性を失う情報の優先度を下げ、アルゴリズムのベイズ後悔に対する境界を導出することに依存します。

<!-- ここまで読んだ! 能動的アプローチは実運用のハードル高いかもと思いあまりちゃんと読んでないが -->

As a final remark, we point out that differently from CUSUM-UCB, GLR-klUCB and BR-MAB, we are able to characterize the regret for any NS-MAB, as long as the distribution of the rewards is either Bernoulli or subgaussian, and in a more general setting than the piecewise-constant abruptly-changing ones. 
最後に、CUSUM-UCB、GLR-klUCB、BR-MABとは異なり、報酬の分布がベルヌーイまたはサブガウスである限り、任意のNS-MABに対する後悔を特定できることを指摘します。また、区分定数の急激に変化するものよりも一般的な設定であることも強調します。
Furthermore, differently from the analysis of RExp3, we retrieve guarantees on the performance also for expected rewards that are not bounded in $[0,1]$. 
さらに、RExp3の分析とは異なり、$[0,1]$に制約されない期待報酬に対しても性能の保証を得ることができます。
Moreover, we highlight that in the work by Liu et al. [34], the authors evaluate the Bayesian regret while we retrieve frequentist bounds on the performance that are notoriously more informative. 
さらに、Liuらの研究[34]では、著者たちがベイズ後悔を評価しているのに対し、私たちは性能に関する頻度主義的な境界を取得しており、これは著名により情報量が多いです。
In [15], the authors dealt with non-stationary, smoothly-changing bandits, a setting in which the expected rewards evolve for a limited amount between two rounds. 
文献[15]では、著者たちは非定常で滑らかに変化するバンディットに対処しており、これは期待報酬が2ラウンドの間に限られた量で進化する設定です。
They designed SW-KL-UCB they achieve a $O(H(\Delta,T)+\frac{T\log(\tau)}{\Delta^{2}\tau})$ regret, where the order of $H(\Delta,T)$ depends on the bandit instance and $\Delta$ is the minimum non-zero distance of the expected rewards within the learning horizon between the best arm and the suboptimal arms. 
彼らはSW-KL-UCBを設計し、$O(H(\Delta,T)+\frac{T\log(\tau)}{\Delta^{2}\tau})$の後悔を達成しました。ここで、$H(\Delta,T)$のオーダーはバンディットのインスタンスに依存し、$\Delta$は最良アームと最適でないアームの間の学習ホライズン内での期待報酬の最小非ゼロ距離です。
Recently paper [38] analyzed the regret of the $\gamma$-SWGTS algorithm. 
最近の論文[38]では、$\gamma$-SWGTSアルゴリズムの後悔が分析されました。
However, the authors do not face the far more challenging Beta-Binomial case and consider only the piece-wise constant abruptly changing settings. 
しかし、著者たちははるかに困難なベータ-二項分布のケースには対処せず、区分定数の急激に変化する設定のみを考慮しています。
We also remark that [38] cite a preprint version of the present paper [19, https://arxiv.org/abs/2409.05181]. 
また、[38]が本論文のプレプリント版[19, https://arxiv.org/abs/2409.05181]を引用していることも指摘します。

<!-- 雑にここまで読んだ! -->

## III 問題定義


At each round t ∈ ⟦ T ⟧ ,4 where T ∈ ℕ is the learning horizon, the learner selects an arm I t ∈ ⟦ K ⟧ among a finite set of K arms and observes a realization of the reward X I t , t . 
各ラウンド $t \in \llbracket T \rrbracket$ において、$T \in \mathbb{N}$ は学習のホライズンであり、学習者は、有限の $K$ 本のアームの中から $I_t \in \llbracket K \rrbracket$ を選択し、報酬 $X_{I_t,t}$ の実現を観察します。
The reward for each arm i ∈ ⟦ K ⟧ ≔ { 1 , … , K } at round t ∈ ⟦ T ⟧ is modeled by a random variable X i , t described by a distribution unknown to the learner. 
各アーム $i \in \llbracket K \rrbracket \coloneqq \{1,\ldots,K\}$ に対する報酬は、ラウンド $t \in \llbracket T \rrbracket$ において、確率変数 $X_{i,t}$ によってモデル化されます。これは学習者には未知の分布によって記述されます。
We denote by μ i , t ≔ 𝔼 ⁢ [ X i , t ] the corresponding expected reward. 
私たちは、期待報酬を $\mu_{i,t} \coloneqq \mathbb{E}[X_{i,t}]$ と表記します。これが対応する期待報酬です。
We study two types of distributions of the rewards encoded by the following assumptions.
私たちは、以下の仮定によって符号化された**報酬の2種類の分布**を研究します。 

- 定式化メモ:
  - (基本的には、カジノのスロットマシンの例を想定すればOK!:thinking:)
  - ラウンド: $t \in \llbracket T \rrbracket$ (1ラウンド目からTラウンド目まで)
  - アーム: $i \in \llbracket K \rrbracket$ (1本目のアームからK本目のアームまで)
  - 学習者: ラウンドごとにアームを1本選択する
  - 報酬: 各アーム$i$のラウンド$t$での報酬は確率変数 $X_{i,t}$ でモデル化される
    - 期待報酬 (=観測される報酬の期待値): $\mu_{i,t} = \mathbb{E}[X_{i,t}]$
    - 報酬分布は、学習者には未知。各アーム $i$ ごとに ラウンド $t$ ごとに異なる可能性ある(non-stationary setting)

<!-- ここまで読んだ! -->

Assumption III.1 (Bernoulli rewards). 
仮定 III.1 (ベルヌーイ報酬).
For every arm i ∈ ⟦ K ⟧ and round t ∈ ⟦ T ⟧ , the reward X i , t is s.t. X i , t ∼ Be ⁢ ( μ i , t ) , where Be ⁢ ( μ ) denotes a Bernoulli distribution with parameter μ ∈ [ 0 , 1 ] .
全てのアーム $i \in K$ とラウンド $t \in T$ に対して、報酬 $X_{i,t}$ は $X_{i,t} \sim \textit{Be}(\mu_{i,t})$ となります。ここで、$\textit{Be}(\mu)$ はパラメータ $\mu \in [0,1]$ を持つベルヌーイ分布を示します。
(つまり、報酬がbinary(0か1)である場合の設定...!!:thinking:)

<!-- ここまで読んだ! -->

Assumption III.2 (Subgaussian rewards). 
仮定 III.2 (サブガウス報酬).
For every arm i ∈ ⟦ K ⟧ and round t ∈ ⟦ T ⟧ , the reward X i , t is s.t. X i , t ∼ SubG ⁢ ( μ i , t , λ 2 ) , where SubG ⁢ ( μ , λ 2 ) denotes a generic subgaussian distribution with finite mean μ ∈ ℝ and proxy variance λ 2 .5
全てのアーム $i \in K $ とラウンド $t \in T$ に対して、報酬 $X_{i,t}$ は $X_{i,t} \sim \textit{SubG}(\mu_{i,t},\lambda^{2})$ となります。ここで、$\textit{SubG}(\mu,\lambda^{2})$ は有限の平均 $\mu \in \mathbb{R}$ と代理分散 $\lambda^{2}$ を持つ一般的なサブガウス分布を示します。5
(つまり、報酬が連続値を取る場合の設定ってこと...!!普通の正規分布じゃなくて"サブ"ガウス...??:thinking:)

---注釈
A random variable $X$ with expectation $\mu$ is $\lambda^{2}$-subgaussian if for every $s \in \mathbb{R}$ it holds that 
期待値 $\mu$ を持つ確率変数 $X$ は、すべての $s \in \mathbb{R}$ に対して 
$\mathbb{E}[\exp(s(X-\mu))] \leq \exp(s^{2}\lambda^{2}/2)$. 
$\mathbb{E}[\exp(s(X-\mu))] \leq \exp(s^{2}\lambda^{2}/2)$ であるとき、$\lambda^{2}$-サブガウスと呼ばれます。 
---

- サブガウス報酬に関するメモ:
  - サブガウス分布 = 正規分布(ガウス分布)と同じくらい、もしくはそれよりも急速に尾部が減少する分布。
  - 「ある確率変数Xが $\lambda^{2}$-サブガウス分布に従う」ことの定義が、上記の注釈で書かれてる内容。確率分布の分散が一定以下になるよね、という定義...!!:thinking:

<!-- ここまで読んだ! -->

The goal of the learner $\mathfrak{A}$ is to minimize the expected cumulative dynamic frequentist regret $R_{T}(\mathfrak{A})$ over the learning horizon $T$, defined as the cumulative difference between the reward of an oracle that chooses at each time the arm with the largest expected reward at round $t$, defined as $i^{*}(t) \in \mathop{\text{argmax}}_{i \in \llbracket K \rrbracket} \mu_{i,t}$, and expected reward $\mu_{I_{t},t}$ of the arm $I_{t}$ selected by the learner for the round, formally: 
学習者 $\mathfrak{A}$ の目標は、学習ホライズン $T$ にわたる期待累積動的頻度主義的後悔 $R_{T}(\mathfrak{A})$ を最小化することです。これは、各時点でラウンド $t$ における最大の期待報酬を持つアームを選択するオラクルの報酬と、学習者がラウンドのために選択したアーム $I_{t}$ の期待報酬 $\mu_{I_{t},t}$ との累積差として正式に定義されます。$i^{*}(t) \in \mathop{\text{argmax}}_{i \in \llbracket K \rrbracket} \mu_{i,t}$ と定義されます。

$$
R_{T}(A) := \mathbb{E} \left[ \sum_{t=1}^{T} \left( \mu_{i^{*}(t),t} - \mu_{I_{t},t} \right) \right].
\tag{1}
$$

where the expected value is taken w.r.t. the randomness of the rewards and the possible randomness of the algorithm. 
ここで、期待値は、報酬のランダム性(=報酬の確率分布!:thinking:)とアルゴリズムの可能なランダム性(=意思決定方策の確率分布!:thinking:)に関して取られます。
In the following, as is often done in the NS-MABs literature (e.g., [11,33,40,48,24]) we provide results on the expected value of the pull of the arms $\mathbb{E}[N_{i,T}]$, where $N_{i,T}$ is the random variable representing the number of total pulls of the arm $i$ at round $T$ excluding the rounds in which $i$ is optimal, formally defined as $N_{i,T} = \sum_{t=1}^{T} \mathds{1}\{I_{t}=i,\,i\neq i^{*}(t)\}$. 
以下では、NS-MABsの文献（例：[11,33,40,48,24]）でよく行われているように、**アームのプルの期待値 $\mathbb{E}[N_{i,T}]$ に関する結果を提供します。ここで、$N_{i,T}$ は、アーム $i$ の総プル数を表す確率変数**であり、$i$ が最適であるラウンドを除外しています。(iが最適だったラウンドを除外するのはなんでだろ...??累積regretの計算では無意味だから...??:thinking:)
正式には、$N_{i,T} = \sum_{t=1}^{T} \mathds{1}\{I_{t}=i,\,i\neq i^{*}(t)\}$ と定義されます。

<!-- ここまで読んだ! -->

## IVAlgorithms IV アルゴリズム

We analyze twosliding-windowalgorithms, namely theBeta-SWTS, proposed in[48], and theγ𝛾\gammaitalic_γ-SWGTS, introduced byFiandri etal. [20], both inspired by the classical TS algorithm. 
私たちは、**2つのスライディングウィンドウアルゴリズム**、すなわち、[48]で提案された**Beta-SWTS**と、Fiandriらによって導入された**γ-SWGTS**を分析します。どちらも古典的なTSアルゴリズムに触発されています。(GTSのGはガウスの意味??:thinking:)
Similarly to what happens withSW-UCB, they handle the problem posed by the dynamical nature of the expected rewards by exploiting only the subset of the most recent collected rewards, i.e., within a sliding window of sizeτ∈ℕ𝜏ℕ\tau\in\mathbb{N}italic_τ ∈ blackboard_N. 
SW-UCBと同様に、彼らは**期待報酬の動的な性質によって引き起こされる問題を、最近収集された報酬のサブセットのみを利用することで対処**します。すなわち、サイズ $\tau \in \mathbb{N}$ のスライディングウィンドウ内でです。
(うんうん、SW系の手法はわかりやすい...!:thinking:)
This allows us to handle the bias given by the least recent collected rewards, which, in an NS-MAB, may be non-representative of the current expected rewards. 
これにより、NS-MABにおいて、最も最近収集された報酬が現在の期待報酬を代表しない可能性があるため、最も古い収集された報酬によるバイアスを扱うことができます。(??)

<!-- ここまで読んだ! -->

The pseudocode ofBeta-SWTSfor Bernoulli-distributed rewards is presented in Algorithm1, while the pseudocode ofγ𝛾\gammaitalic_γ-SWGTSfor subgaussian rewards is presented in Algorithm2. 
Bernoulli分布の報酬に対するBeta-SWTSの擬似コードはアルゴリズム1に示されており、サブガウス報酬に対するγ-SWGTSの擬似コードはアルゴリズム2に示されています。
They are based on the principle ofconjugate-priorupdates. 
彼らは共役事前更新の原則に基づいています。
The key difference from the classical TS stands in discarding older examples, thanks to the window widthτ𝜏\tauitalic_τ, through a sliding-window mechanism. 
**古典的なTSとの主な違いは、スライディングウィンドウメカニズムを通じて、ウィンドウ幅τによって古い例を捨てること**にあります。(うんうん。SW系アプローとはそうだよね:thinking:)
This way, the prior remains sufficiently spread over time, ensuring ongoing exploration, essential to deal with non-stationarity. 
このようにして、事前分布は時間とともに十分に広がり続け、非定常性に対処するために不可欠な継続的な探索を保証します。

<!-- ここまで読んだ! -->

- 各ラウンド$t \in T $およびアーム $i \in  K$ に対して、パラメータ $\mu_{i,t}$ の事前分布を $\nu_{i,t}$ で示します。
- Beta-SWTSでは、無情報事前分布(uninformative prior)が設定されます。
- すなわち、$\nu_{i,1} := \text{Beta}(1,1)$（行3）であり、ここで$\text{Beta}(\alpha,\beta)$ はパラメータ $\alpha,\beta \geq 0$ を持つベータ分布です。
- ラウンド $t$ におけるアーム $i$ の期待報酬の事後分布は、$\nu_{i,t} := \text{Beta}(S_{i,t,\tau} + 1, N_{i,t,\tau} - S_{i,t,\tau} + 1)$ で与えられます。(うんうん。binary報酬の普通のbanditだ...!:thinking:)
- ここで、$N_{i,t,\tau} := \sum_{s=\max{\{t-\tau,1\}}}^{t-1}\mathds{1}{\{I_{s}=i\}}$は、アーム $i$ が直近の $\min{\{t,\tau\}}$ ラウンドで選択された回数です。
- また、$S_{i,t,\tau} := \sum_{s=\max\{{t-\tau,1}\}}^{t-1}X_{i,s}\mathds{1}{\{I_{s}=i\}}$は、アーム$i$が直近の$\min{\{t,\tau\}}$ラウンドで収集した累積報酬です。
- 各ラウンド $t$ および各アーム $i$ に対して、アルゴリズムは $\theta_{i,t,\tau}$ からランダムサンプルを引きます。これは、いわゆるトンプソンサンプルです（行5）。
- 次に、サンプルの値が最も大きいアームが選択されます（行6）。
- 収集した報酬 $X_{I_{t},t}$ に基づいて、事前分布 $\nu_{i,t+1}$ が更新されます（行10）。(=観測報酬に基づいて信念を更新...!:thinking:)

<!-- ここまで読んだ! -->

- γ-SWGTSアルゴリズムは、いくつかの違いを除いて、Beta-SWTSと同じ原則を共有しています。 
- 特に、すべてのアームが1回プレイされるKラウンドの初期化の後（行3）、各ラウンド$t$において、事前分布は $\nu_{i,t} := \mathcal{N}(\frac{S_{i,t,\tau}}{N_{i,t,\tau}}, \frac{1}{\gamma N_{i,t,\tau}})$ として定義されます。
  - 一次元正規分布...!:thinking:
  - ここで、$\mathcal{N}(\alpha,\beta)$ は平均 $\alpha \in \mathbb{R}$、分散$\beta \geq 0$ のガウス分布です。
  - $S_{i,t,\tau}$ および $N_{i,t,\tau}$ は上記のように定義され(=beta-SWTS)と同じ!)、$\gamma > 0$は後で設定されるハイパーパラメータです。
- 各ラウンド $t$ および各アーム $i$ に対して、アルゴリズムは $\nu_{i,t}$ からランダムサンプル $\theta_{i,t,\tau}$ を引き（行13）、最も大きなトンプソンサンプルを持つアームが選択されます（行14）。
- アームに関する情報がない場合、すなわち$N_{i,t,\tau} = 0$のとき、アームは強制的にプレイされ、事前分布が常に明確に定義されるようになります（行10）。
- 次に、収集した報酬$X_{I_{t},t}$に基づいて、事前分布$\nu_{i,t+1}$が更新されます（行19）。(=プレイについて観測された報酬に基づいて、信念を更新...!:thinking:)

<!-- ここまで読んだ! -->

## VRegret Analysis for the General Non-Stationary Environment 一般非定常環境におけるレグレット分析

In this paper, we investigate NS-MABs in a unifying framework allowing the mean rewards $\mu_{i,t}$ to change arbitrarily over time with no particular regularity, as long as the Assumption III.1 or Assumption III.2 is met. 
本論文では、**期待報酬 $\mu_{i,t}$ が特定の規則性なしに時間とともに任意に変化することを許可する統一的な枠組み**の中で、NS-MABを調査します。これは、仮定 III.1 または仮定 III.2 が満たされる限りです。
Beginning from this general regret analysis, in Sections VI and VII, we particularize it for the cases in which $\mu_{i,t}$ satisfies additional regularity conditions, i.e., abrupt and smoothly changing, respectively. 
この一般的なレグレット分析から始めて、セクション VI と VII では、$\mu_{i,t}$ が追加の規則性条件、すなわち急激に変化する場合と滑らかに変化する場合に特化します。
We start the analysis by introducing a definition to characterize the rounds during which the algorithms can effectively assess the best arm even in the presence of non-stationarity. 
私たちは、非定常性が存在する場合でも、アルゴリズムが効果的に最良のアームを評価できるラウンドを特徴付ける定義を導入することから分析を始めます。

<!-- ここまで読んだ! -->

**Definition V.1** (Unlearnable set $F_{\tau}$ and learnable set $F_{\tau}^{C}$)
**定義 V.1**

For every window size $\tau \in \mathbb{N}$, the unlearnable set $\mathcal{F}_{\tau}$ is defined as any superset of $\mathcal{F}_{\tau}^{\prime}$ defined as: 
すべてのウィンドウサイズ $\tau \in \mathbb{N}$ に対して、学習不可能な集合 $\mathcal{F}_{\tau}$ は、次のように定義される $\mathcal{F}_{\tau}^{\prime}$ の任意の上位集合として定義されます。

$$
F
\tag{2}
$$

and the learnable set $\mathcal{F}_{\tau}^{\complement}$ is defined as $\mathcal{F}_{\tau}^{\complement} \coloneqq \llbracket T \rrbracket \setminus \mathcal{F}_{\tau}$. 
そして、学習可能な集合 $\mathcal{F}_{\tau}^{\complement}$ は、$\mathcal{F}_{\tau}^{\complement} \coloneqq \llbracket T \rrbracket \setminus \mathcal{F}_{\tau}$ と定義されます。

Notice that by definition, for every round $t \in \mathcal{F}_{\tau}^{\complement}$, the following inequality holds true for all $i \neq i^{*}(t)$: 
定義により、すべてのラウンド $t \in \mathcal{F}_{\tau}^{\complement}$ に対して、次の不等式がすべての $i \neq i^{*}(t)$ に対して成り立ちます。

Intuitively, $\mathcal{F}_{\tau}^{\complement}$ collects all the rounds $t \in \llbracket T \rrbracket$ such that the smallest expected reward of the optimal arm $i^{*}(t)$ within the last $\tau$ rounds is larger than the largest expected reward of all other arms in the same interval spanning the length of the sliding window $\tau$. 
直感的には、$\mathcal{F}_{\tau}^{\complement}$ は、最適アーム $i^{*}(t)$ の過去 $\tau$ ラウンド内の最小期待報酬が、同じスライディングウィンドウの長さ $\tau$ にわたる他のすべてのアームの最大期待報酬よりも大きいラウンド $t \in \llbracket T \rrbracket$ を集めます。

This enables the introduction of a general definition for the suboptimality gaps $\Delta_{\tau}$ that encodes how challenging it is to identify the optimal arm relying on the rewards collected in the past $\tau$ rounds only. 
これにより、過去 $\tau$ ラウンドで収集された報酬のみに依存して最適アームを特定することがどれほど困難であるかを符号化する一般的な定義であるサブオプティマリティギャップ $\Delta_{\tau}$ を導入できます。

**Definition V.2**
**定義 V.2**

For every window size $\tau \in \mathbb{N}$, the general suboptimality gap is defined as follows: 
すべてのウィンドウサイズ $\tau \in \mathbb{N}$ に対して、一般的なサブオプティマリティギャップは次のように定義されます。

The suboptimality gap $\Delta_{\tau} > 0$ quantifies a minimum non-zero distance in terms of expected reward between the optimal arm $i^{*}(t)$ and all other arms across all rounds $t \in \mathcal{F}_{\tau}^{\complement}$. 
サブオプティマリティギャップ $\Delta_{\tau} > 0$ は、最適アーム $i^{*}(t)$ とすべての他のアームとの間の期待報酬に関する最小の非ゼロ距離を定量化します。

We are now ready to present the result on the upper bound of the expected number of pulls for the analyzed algorithms. 
これで、分析されたアルゴリズムの期待される引き数の上限に関する結果を提示する準備が整いました。

**Theorem V.1**  
**定理 V.1**

Under Assumption III.1 and $\tau \in \mathbb{N}$, for Beta-SWTS the following holds true for every arm $i \in \llbracket K \rrbracket$: 
仮定 III.1 および $\tau \in \mathbb{N}$ の下で、Beta-SWTS に対して、すべてのアーム $i \in \llbracket K \rrbracket$ に対して次のことが成り立ちます。

**Theorem V.2**  
**定理 V.2**

Under Assumption III.2, $\tau \in \mathbb{N}$, for $\gamma$-SWGTS with $\gamma \leq \min\{\frac{1}{4\lambda^{2}},1\}$ the following holds true for every arm $i \in \llbracket K \rrbracket$: 
仮定 III.2 の下で、$\tau \in \mathbb{N}$ に対して、$\gamma$-SWGTS で $\gamma \leq \min\{\frac{1}{4\lambda^{2}},1\}$ の場合、すべてのアーム $i \in \llbracket K \rrbracket$ に対して次のことが成り立ちます。

These results capture a trade-off in the choice of the window size $\tau$. 
これらの結果は、ウィンドウサイズ $\tau$ の選択におけるトレードオフを捉えています。

Specifically, we observe that, given a window size $\tau$, the regret is decomposed in two contributions, namely: (A) $A$, being the cardinality of the unlearnable set $|\mathcal{F}_{\tau}|$, i.e., a superset of the set of rounds in which no algorithm exploiting only the $\tau$ most recent samples can distinguish consistently the best arm from the suboptimal ones; 
具体的には、ウィンドウサイズ $\tau$ が与えられた場合、レグレットは2つの寄与に分解されることが観察されます。すなわち、(A) $A$ は学習不可能な集合の基数 $|\mathcal{F}_{\tau}|$ であり、これは $\tau$ の最も最近のサンプルのみを利用するアルゴリズムが最良のアームとサブオプティマルなアームを一貫して区別できないラウンドの集合の上位集合です。

(B) $B$, corresponding to the expected number of pulls of the suboptimal arm within the learnable set. 
(B) $B$ は、学習可能な集合内のサブオプティマルアームの期待される引き数に対応します。

We can see that (A) tends to increase with $\tau$ and (B) decreases with $\tau$. 
(A) は $\tau$ とともに増加する傾向があり、(B) は $\tau$ とともに減少することがわかります。

Notice that dealing with subgaussian reward, a term that accounts for the (possibly) greater uncertainty for the realization of the rewards appears, namely $\gamma$. 
サブガウス報酬を扱う際には、報酬の実現に対する（おそらく）より大きな不確実性を考慮する項、すなわち $\gamma$ が現れます。

Similarly, an additional (C) term arises for $\gamma$-SWGTS, taking into account the forced exploration to ensure the posterior distribution is always well defined. 
同様に、$\gamma$-SWGTS に対しては、事後分布が常に明確に定義されることを保証するための強制的な探索を考慮した追加の (C) 項が現れます。

In the next sections, we discuss how these results compare to the ones retrieved in the literature for the most common stationary bandits. 
次のセクションでは、これらの結果が最も一般的な定常バンディットに関する文献で得られた結果とどのように比較されるかを議論します。

Figure 1 provides an example showing how the choice of the window size $\tau$ affects the cardinalities of $\mathcal{F}_{\tau}$ and $\mathcal{F}_{\tau}^{\complement}$. 
図1は、ウィンドウサイズ $\tau$ の選択が $\mathcal{F}_{\tau}$ と $\mathcal{F}_{\tau}^{\complement}$ の基数にどのように影響するかを示す例を提供します。

The figure depicts a setting in which the optimal arm is the same until an abrupt change occurs. 
この図は、最適アームが急激な変化が起こるまで同じである設定を描いています。

This partitions the learning horizon into the intervals $\mathcal{I}_{1}$, $\mathcal{I}_{2}$, and $\mathcal{I}_{3}$. 
これにより、学習の地平線が区間 $\mathcal{I}_{1}$、$\mathcal{I}_{2}$、および $\mathcal{I}_{3}$ に分割されます。

We consider three different values for the window size $\tau_{1} > \tau_{2} > \tau_{3}$. 
ウィンドウサイズに対して、$\tau_{1} > \tau_{2} > \tau_{3}$ の3つの異なる値を考えます。

As the window size increases, the cardinality of $\mathcal{F}_{\tau}^{\complement}$ decreases, as depicted below the figure. 
ウィンドウサイズが増加するにつれて、$\mathcal{F}_{\tau}^{\complement}$ の基数は減少します。これは図の下に示されています。

Indeed, the learnable sets exclude those rounds for which the window overlaps with two different intervals. 
実際、学習可能な集合は、ウィンドウが2つの異なる区間と重なるラウンドを除外します。

Conversely, when we set a small window, e.g., $\tau_{3}$, the set $\mathcal{F}_{\tau_{3}}^{\complement}$ includes more rounds while guaranteeing that a generic algorithm exploiting samples from the window is capable of selecting the best arm consistently. 
逆に、小さなウィンドウ、例えば $\tau_{3}$ を設定すると、集合 $\mathcal{F}_{\tau_{3}}^{\complement}$ はより多くのラウンドを含み、ウィンドウからのサンプルを利用する一般的なアルゴリズムが一貫して最良のアームを選択できることを保証します。

This is due to the fact that, for smaller window size, the algorithms are able to adapt faster to the new form of the expected rewards. 
これは、ウィンドウサイズが小さいほど、アルゴリズムが期待報酬の新しい形により早く適応できるためです。

However, choosing $\tau$ too small, as suggested by term (B) of Theorems V.1 and V.2, can lead to a large number of pulls of the suboptimal arms, proportional to $\widetilde{O}\left(\frac{T}{\tau}\right)$, as the algorithms become too explorative. 
しかし、定理 V.1 および V.2 の項 (B) で示唆されるように、$\tau$ を小さく選びすぎると、アルゴリズムが過度に探索的になるため、サブオプティマルアームの引き数が大きくなり、$O\left(\frac{T}{\tau}\right)$ に比例する可能性があります。

As a final remark, we highlight that we do not ask for any specific regularity for the expected rewards, so the results hold for any arbitrary NS-MAB, e.g., also for the rising restless or the rotting restless bandits. 
最後に、期待報酬に対して特定の規則性を求めないことを強調しますので、結果は任意の NS-MAB に対して成り立ちます。例えば、上昇するレストレスバンディットや腐敗するレストレスバンディットにも適用されます。

Now, we are ready to show the results these theorems imply for the most common NS-MAB, i.e., abruptly changing and smoothly changing ones. 
これで、これらの定理が最も一般的な NS-MAB、すなわち急激に変化するものと滑らかに変化するものに対して示唆する結果を示す準備が整いました。

Figure 1: 
図1：



## VIRegret Analysis for Abruptly Changing Environments

VI Regret Analysis for Abruptly Changing Environments  
突然変化する環境におけるVIの後悔分析

We now consider the piece-wise constant abruptly-changing environment, i.e., those scenarios in which the expected rewards of the arms remain the same during subsets of the learning horizon called phases, and the phase changes at unknown rounds called breakpoints (Figure 2a).  
ここでは、部分的に定数の突然変化する環境、すなわち、アームの期待報酬が学習ホライズンのサブセットであるフェーズの間は同じままで、未知のラウンドであるブレークポイントでフェーズが変化するシナリオを考えます（図2a）。

First, we introduce some quantities used to characterize the regret.  
まず、後悔を特徴づけるために使用されるいくつかの量を導入します。

Second, we express Theorem V.1 and Theorem V.2 in terms of these newly defined quantities, comparing them with those of the state-of-the-art algorithms devised for this setting.  
次に、これらの新たに定義された量を用いて定理V.1および定理V.2を表現し、この設定のために考案された最先端のアルゴリズムのものと比較します。

Finally, we show that our results apply to a far more general class of abruptly-changing NS-MABs where the expected reward is not constrained to remain constant within each phase.  
最後に、私たちの結果が、各フェーズ内で期待報酬が一定であることに制約されない、より一般的な突然変化するNS-MABのクラスに適用されることを示します。

### Definition VI.1

A breakpoint is a round $t \in \llbracket 2,T \rrbracket$ such that there exists $i \in \llbracket K \rrbracket$ for which holds $\mu_{i,t} \neq \mu_{i,t-1}$.  
**定義 VI.1**  
ブレークポイントは、$t \in \llbracket 2,T \rrbracket$ であり、$i \in \llbracket K \rrbracket$ が存在して $\mu_{i,t} \neq \mu_{i,t-1}$ が成り立つラウンドです。

Let us denote with $b_{\psi}$ as the $\psi$-th breakpoint $1 < b_{1} < \ldots < b_{\Upsilon_{T}} < T$, where $\Upsilon_{T} \in \llbracket T \rrbracket$ is the total number of breakpoints over a learning horizon $T$.  
$\psi$-thブレークポイントを $b_{\psi}$ と表記し、$1 < b_{1} < \ldots < b_{\Upsilon_{T}} < T$ とし、ここで $\Upsilon_{T} \in \llbracket T \rrbracket$ は学習ホライズン $T$ におけるブレークポイントの総数です。

The breakpoints partition the learning horizon $\llbracket T \rrbracket$ into phases $\mathcal{F}_{\psi}$ and pseudophases $\mathcal{F}_{\psi,\tau}^{*}$.  
ブレークポイントは学習ホライズン $\llbracket T \rrbracket$ をフェーズ $\mathcal{F}_{\psi}$ と擬似フェーズ $\mathcal{F}_{\psi,\tau}^{*}$ に分割します。

Formally, using the convention that $b_{0} = 1$ and $b_{\Upsilon_{T}+1} = T$:  
形式的には、$b_{0} = 1$ および $b_{\Upsilon_{T}+1} = T$ という規約を用います：

### Definition VI.2

Let $T \in \mathbb{N}$ be the learning horizon and $\psi \in \llbracket \Upsilon_{T}+1 \rrbracket$, we define the $\psi$-th phase as:  
**定義 VI.2**  
$T \in \mathbb{N}$ を学習ホライズンとし、$\psi \in \llbracket \Upsilon_{T}+1 \rrbracket$ とすると、$\psi$-thフェーズを次のように定義します：

It is worth noting that the optimal arm $i^{*}(t)$ is for sure constant within each phase $\psi \in \llbracket \Psi_{T}+1 \rrbracket$, i.e., we can appropriately denote it as $i^{*}_{\psi}$.  
最適アーム $i^{*}(t)$ は、各フェーズ $\psi \in \llbracket \Psi_{T}+1 \rrbracket$ 内で確実に一定であることに注意する価値があります。すなわち、適切に $i^{*}_{\psi}$ と表記できます。

### Definition VI.3

Let $T \in \mathbb{N}$ be the learning horizon, a window size $\tau$, and $\psi \in \llbracket 2,\Upsilon_{T}+1 \rrbracket$, the $\psi$-th pseudophase is defined as:  
**定義 VI.3**  
$T \in \mathbb{N}$ を学習ホライズン、ウィンドウサイズ $\tau$、および $\psi \in \llbracket 2,\Upsilon_{T}+1 \rrbracket$ とすると、$\psi$-th擬似フェーズを次のように定義します：

and $\mathcal{F}_{1,\tau}^{*} = \mathcal{F}_{1}$.  
そして、$\mathcal{F}_{1,\tau}^{*} = \mathcal{F}_{1}$。

When $\tau$ is longer than the phase, the pseudophase is empty, i.e., where $\mathcal{F}_{\psi,\tau}^{*} = \{\}$ for $\tau \geq b_{\psi} - b_{\psi-1}$.  
$\tau$ がフェーズよりも長い場合、擬似フェーズは空になります。すなわち、$\mathcal{F}_{\psi,\tau}^{*} = \{\}$ となります。

Finally, we define $\mathcal{F}_{\tau}^{*} = \bigcup_{\psi=1}^{\Upsilon_{T}+1} \mathcal{F}_{\psi,\tau}^{*}$.  
最後に、$\mathcal{F}_{\tau}^{*} = \bigcup_{\psi=1}^{\Upsilon_{T}+1} \mathcal{F}_{\psi,\tau}^{*}$ と定義します。

The intuition behind the definition of the pseudophase is that if we use an algorithm $\mathfrak{A}$ relying on a sliding window of size $\tau$ during the rounds of the pseudophase $\mathcal{F}_{\psi,\tau}^{*}$, the algorithm $\mathfrak{A}$ uses only on rewards belonging to the single phase $\mathcal{F}_{\psi}$.  
擬似フェーズの定義の背後にある直感は、擬似フェーズ $\mathcal{F}_{\psi,\tau}^{*}$ のラウンド中にサイズ $\tau$ のスライディングウィンドウに依存するアルゴリズム $\mathfrak{A}$ を使用する場合、アルゴリズム $\mathfrak{A}$ は単一のフェーズ $\mathcal{F}_{\psi}$ に属する報酬のみを使用するということです。

We provide a graphical representation of the definitions introduced above in Figure 2a.  
上記の定義のグラフィカルな表現を図2aに示します。

In particular, we have two breakpoints ($\Upsilon_{T}=2$), and three phases $\mathcal{F}_{1}, \mathcal{F}_{2}, \mathcal{F}_{3}$.  
特に、2つのブレークポイント（$\Upsilon_{T}=2$）と3つのフェーズ $\mathcal{F}_{1}, \mathcal{F}_{2}, \mathcal{F}_{3}$ があります。

Given a window size of $\tau$, we have three pseudophases $\mathcal{F}_{1,\tau}^{*}, \mathcal{F}_{2,\tau}^{*}, \mathcal{F}_{3,\tau}^{*}$, where the last two pseudophases start $\tau$ rounds after the start of the corresponding phase.  
ウィンドウサイズ $\tau$ を考えると、3つの擬似フェーズ $\mathcal{F}_{1,\tau}^{*}, \mathcal{F}_{2,\tau}^{*}, \mathcal{F}_{3,\tau}^{*}$ があり、最後の2つの擬似フェーズは対応するフェーズの開始から $\tau$ ラウンド後に始まります。

Let us characterize the sets introduced in Definition VI.1, namely $\mathcal{F}_{\tau}$ and $\mathcal{F}_{\tau}^{\complement}$, using the concepts of phase and pseudophase.  
定義 VI.1 で導入された集合、すなわち $\mathcal{F}_{\tau}$ と $\mathcal{F}_{\tau}^{\complement}$ を、フェーズと擬似フェーズの概念を用いて特徴づけましょう。

We can express $\mathcal{F}_{\tau}$ as the union of the set of rounds of length $\tau$ after every breakpoint, formally:  
$\mathcal{F}_{\tau}$ を、すべてのブレークポイントの後の長さ $\tau$ のラウンドの集合の和として表現できます。形式的には：

Consequently, we have $\mathcal{F}_{\tau}^{\complement} = \mathcal{F}_{\tau}^{*}$.  
したがって、$\mathcal{F}_{\tau}^{\complement} = \mathcal{F}_{\tau}^{*}$ となります。

Therefore, since for any round $t \in \llbracket T \rrbracket$ belonging to a pseudophase, the algorithms using a sliding window of size $\tau$ uses samples coming from a single phase, we have that for any $t \in \mathcal{F}_{\tau}^{*}$:  
したがって、擬似フェーズに属する任意のラウンド $t \in \llbracket T \rrbracket$ に対して、サイズ $\tau$ のスライディングウィンドウを使用するアルゴリズムは単一のフェーズからのサンプルを使用するため、任意の $t \in \mathcal{F}_{\tau}^{*}$ に対して次のようになります：

which corresponds to the learnable set in Definition VI.1.  
これは定義 VI.1 における学習可能な集合に対応します。

The latter inequality follows from the fact that any round $t \in \mathcal{F}_{\tau}^{*}$ belongs to a pseudophase $\mathcal{F}_{\psi,\tau}^{*}$ and, therefore, all the times $t' \in \llbracket t-\tau,t-1 \rrbracket$ belong to a single phase $\mathcal{F}_{\psi}$.  
後者の不等式は、任意のラウンド $t \in \mathcal{F}_{\tau}^{*}$ が擬似フェーズ $\mathcal{F}_{\psi,\tau}^{*}$ に属し、したがって、すべての時刻 $t' \in \llbracket t-\tau,t-1 \rrbracket$ が単一のフェーズ $\mathcal{F}_{\psi}$ に属するという事実に基づいています。

By definition of the general suboptimality gap (Definition V.2), we have:  
一般的なサブオプティマリティギャップの定義（定義 V.2）により、次のようになります：

Notice that the definition of $\Delta_{\tau}$, if $\tau$ is such that no pseudophase is empty, corresponds to the definition of $\Delta$ in the work by [23] in the case of piecewise-constant setting.  
$\Delta_{\tau}$ の定義は、$\tau$ が擬似フェーズが空でない場合に、部分的に定数の設定における [23] の作業の $\Delta$ の定義に対応することに注意してください。

We are now ready to present the results on the upper bounds of the number of plays in the abruptly changing environment.  
突然変化する環境におけるプレイ数の上限に関する結果を提示する準備が整いました。

### Theorem VI.1

Under Assumptions III.1, $\tau \in \mathbb{N}$, for Beta-SWTS the following holds:  
**定理 VI.1**  
仮定 III.1 の下で、$\tau \in \mathbb{N}$ の場合、Beta-SWTS に対して次のことが成り立ちます：

### Theorem VI.2

Under Assumptions III.2, $\tau \in \mathbb{N}$, for $\gamma$-SWGTS with $\gamma \leq \min\{\frac{1}{4\lambda^{2}},1\}$ it holds that:  
**定理 VI.2**  
仮定 III.2 の下で、$\tau \in \mathbb{N}$ の場合、$\gamma$-SWGTS に対して $\gamma \leq \min\{\frac{1}{4\lambda^{2}},1\}$ が成り立ちます：

Let us further analyze the bounds obtained.  
得られた境界をさらに分析しましょう。

Making a direct comparison with Theorem V.1 and V.2 for the general NS-MAB setting, we now appreciate a clearer formulation for the cardinality of the unlearnable set.  
一般的な NS-MAB 設定に対する定理 V.1 および V.2 と直接比較することで、学習不可能な集合の基数に対するより明確な定式化を理解できるようになりました。

In fact, in abruptly changing environments, it is convenient to characterize the unlearnable set as the set of rounds length $\tau$ after every breakpoint.  
実際、突然変化する環境では、学習不可能な集合をすべてのブレークポイントの後の長さ $\tau$ のラウンドの集合として特徴づけることが便利です。

In these $\Upsilon_{T}$ rounds, we cannot guarantee that the algorithms will be able to distinguish the best arm from the suboptimal ones.  
これらの $\Upsilon_{T}$ ラウンドでは、アルゴリズムが最適なアームとサブオプティマルなアームを区別できることを保証できません。

Figure 2a provides an explicit graphical representation of the quantities introduced.  
図2aは、導入された量の明示的なグラフィカル表現を提供します。

In particular, we see that in the first $\tau$ rounds of each phase, the rewards gathered within the window size are not representative of the current expected rewards, as they may include examples from rounds in which the ranking of the arms is different.  
特に、各フェーズの最初の $\tau$ ラウンドでは、ウィンドウサイズ内で収集された報酬が現在の期待報酬を代表するものではなく、アームのランキングが異なるラウンドからの例を含む可能性があることがわかります。

The order for the expected number of pulls of the suboptimal arm within the learnable set matches the state-of-the-art order in $T, \tau$, and $\Delta_{\tau}$ for the expected number of pulls for a sliding window algorithm, even when applied to a stationary bandit [23].  
学習可能な集合内のサブオプティマルアームの期待される引き回しの順序は、スライディングウィンドウアルゴリズムの期待される引き回しのための最先端の順序と一致し、定常バンディット [23] に適用される場合でも同様です。

Since existing algorithms for this setting are devised to handle environments with expected rewards bounded in $[0,1]$, in order to compare the results obtained we only consider the piecewise-constant abruptly-changing environment with Bernoulli rewards.  
この設定の既存のアルゴリズムは、期待報酬が $[0,1]$ に制約される環境を扱うように設計されているため、得られた結果を比較するために、ベルヌーイ報酬を持つ部分的に定数の突然変化する環境のみを考慮します。

Let us assume $\Delta_{\tau}$ constant w.r.t. $T$, as done in the NS-MAB literature and let us choose $\tau \propto T \ln(T)$.  
$\Delta_{\tau}$ が $T$ に対して一定であると仮定し、NS-MAB 文献で行われているように、$\tau \propto T \ln(T)$ を選びましょう。

From Theorem VI.1 and VI.2, we derive the following guarantees on the regret:  
定理 VI.1 および VI.2 から、後悔に関する次の保証を導きます：

that is the same order of the guarantees on the regret of SW-UCB.  
これは SW-UCB の後悔に関する保証と同じ順序です。

Even if GLR-klUCB relies on an active approach to deal with non-stationary bandits, it also retrieves the same order for the bounds on the regret.  
GLR-klUCB が非定常バンディットに対処するためにアクティブなアプローチに依存している場合でも、後悔の境界に対して同じ順序を取得します。

Finally, CUSUM-UCB and BR-MAB can achieve the following upper bound on the regret:  
最後に、CUSUM-UCB と BR-MAB は後悔に関する次の上限を達成できます：

which is better than the previous one only for a $\Upsilon_{T}$ factor in the logarithmic term.  
これは、対数項における $\Upsilon_{T}$ の因子に対してのみ前のものよりも優れています。

The results of Theorem V.1 and Theorem V.2 hold for a way more general setting than the piece-wise constant abruptly-changing NS-MABs.  
定理 V.1 および定理 V.2 の結果は、部分的に定数の突然変化する NS-MAB よりもはるかに一般的な設定に対して成り立ちます。

In Figure 2b, we highlight the rounds belonging to the unlearnable set in yellow and the rounds belonging to the learnable set in green for a setting in which the expected rewards are not constant but the expected reward of the optimal arm never intersects that of the suboptimal ones in every phase.  
図2bでは、期待報酬が一定でないが、最適アームの期待報酬が各フェーズでサブオプティマルなアームのそれと交差しない設定において、学習不可能な集合に属するラウンドを黄色で、学習可能な集合に属するラウンドを緑で強調表示します。

Note that the cardinality of the learnable and unlearnable sets are the same as those of the NS-MAB described by Figure 2a.  
学習可能な集合と学習不可能な集合の基数は、図2aで説明されている NS-MAB のそれと同じであることに注意してください。

Thus, it is not surprising that Theorem VI.1 and Theorem VI.2 hold even for the second setting.  
したがって、定理 VI.1 および定理 VI.2 が第二の設定でも成り立つことは驚くべきことではありません。

This represents a generality of our analysis that, to the best of the authors’ knowledge, is not captured by the existing NS-MAB literature.  
これは、著者の知識の限りでは、既存の NS-MAB 文献では捉えられていない私たちの分析の一般性を表しています。

We refer to the class of NS-MABs as (general) abruptly-changing, which can be formally defined through a notion of general breakpoint.  
私たちは、一般的なブレークポイントの概念を通じて正式に定義できる NS-MAB のクラスを（一般的な）突然変化するものと呼びます。

### Definition VI.4

A set of $\Upsilon_{T}+1$ rounds $1 \equiv b_{0} < b_{1} < \ldots < b_{\Upsilon_{T}} < T \equiv b_{\Upsilon_{T}+1}$ are generalized breakpoints if for every $\psi \in \llbracket \Upsilon_{T}+1 \rrbracket$ it holds that:  
**定義 VI.4**  
$\Upsilon_{T}+1$ ラウンドの集合 $1 \equiv b_{0} < b_{1} < \ldots < b_{\Upsilon_{T}} < T \equiv b_{\Upsilon_{T}+1}$ は、すべての $\psi \in \llbracket \Upsilon_{T}+1 \rrbracket$ に対して次のことが成り立つ場合、一般化されたブレークポイントです：

for every arm $i \in \llbracket K \rrbracket \setminus \{i^{*}(t)\}$.  
すべてのアーム $i \in \llbracket K \rrbracket \setminus \{i^{*}(t)\}$ に対して。

Notice that, similarly to the previous case, by definition, the optimal arm does not change within two breakpoints, i.e., $i^{*}(t) = i^{*}_{\psi}$ for every $t \in \llbracket b_{\psi-1},b_{\psi}-1 \rrbracket$ and interval $\psi \in \llbracket \Upsilon_{T}+1 \rrbracket$.  
前のケースと同様に、定義により、最適アームは2つのブレークポイント内で変化しないことに注意してください。すなわち、$i^{*}(t) = i^{*}_{\psi}$ は、すべての $t \in \llbracket b_{\psi-1},b_{\psi}-1 \rrbracket$ および区間 $\psi \in \llbracket \Upsilon_{T}+1 \rrbracket$ に対して成り立ちます。

The definitions of phases and pseudophases (Definition VI.2 and Definition VI.3) still hold with the new definition of the breakpoint.  
フェーズと擬似フェーズの定義（定義 VI.2 および定義 VI.3）は、新しいブレークポイントの定義でも依然として成り立ちます。

Again, when sampling within an arbitrary pseudophase $\mathcal{F}_{\psi,\tau}^{*}$, since we use only samples belonging to phase $\mathcal{F}_{\psi}$ for which it holds by definition that $\min_{t \in \llbracket b_{\psi-1},b_{\psi}-1 \rrbracket}\{\mu_{i^{*}(t),t}\} > \max_{t \in \llbracket b_{\psi-1},b_{\psi}-1 \rrbracket}\{\mu_{i,t}\}$, also the following holds true for any $t \in \mathcal{F}_{\tau}^{*}$:  
再び、任意の擬似フェーズ $\mathcal{F}_{\psi,\tau}^{*}$ 内でサンプリングする場合、定義により、フェーズ $\mathcal{F}_{\psi}$ に属するサンプルのみを使用するため、次のことが任意の $t \in \mathcal{F}_{\tau}^{*}$ に対して成り立ちます：

which corresponds to the learnable set in Definition V.1.  
これは定義 V.1 における学習可能な集合に対応します。



## VIIRegret Analysis for Smoothly Changing Environments
## VII 滑らかに変化する環境における後悔分析

We now study what can be inferred from Theorems V.1 and V.2 in the smoothly changing environments, i.e., those scenarios in which the expected reward of each arm is allowed to vary only for a limited amount between consecutive rounds. 
ここでは、滑らかに変化する環境における定理 V.1 および V.2 から何が推測できるかを研究します。すなわち、各アームの期待報酬が連続するラウンド間で限られた範囲内でのみ変動するシナリオです。

The regret analysis through breakpoints is unsuitable for an environment in which the expected rewards evolve smoothly. 
ブレークポイントを通じた後悔分析は、期待報酬が滑らかに進化する環境には適していません。

In what follows, we characterize the regret the algorithms suffer in these settings introducing the most common definitions and assumptions used in the smoothly changing environment literature, deriving the implications for the sets introduced in Definition V.1. 
以下では、これらの設定においてアルゴリズムが被る後悔を特徴づけ、滑らかに変化する環境の文献で使用される最も一般的な定義と仮定を導入し、定義 V.1 で導入された集合に対する含意を導き出します。

Finally, we compare our results with the state-of-the-art results for the setting. 
最後に、私たちの結果をこの設定における最先端の結果と比較します。

### V.1 Assumption VII.1
### V.1 仮定 VII.1

The expected reward of the arms is Lipschitz continuous if there exists $\sigma < +\infty$ such that for every round $t, t' \in \llbracket T \rrbracket$ and arm $i \in \llbracket K \rrbracket$ we have:
アームの期待報酬はリプシッツ連続である。もし $\sigma < +\infty$ が存在し、すべてのラウンド $t, t' \in \llbracket T \rrbracket$ およびアーム $i \in \llbracket K \rrbracket$ に対して次が成り立つならば：

$$
\text{(14)}
$$

### Assumption VII.2
### 仮定 VII.2

Let $\Delta' > 2\sigma\tau > 0$ be finite, we define $\mathcal{F}_{\Delta',T}$ as:
$\Delta' > 2\sigma\tau > 0$ を有限とし、$\mathcal{F}_{\Delta',T}$ を次のように定義します：

$$
\text{(15)}
$$

There exist $\beta \in [0,1]$ and finite $F < +\infty$, such that $|\mathcal{F}_{\Delta',T}| \leq FT^{\beta}$.
$\beta \in [0,1]$ かつ有限の $F < +\infty$ が存在し、次が成り立つ：

$$
|\mathcal{F}_{\Delta',T}| \leq FT^{\beta}
$$

Notice that Assumption 11 in [15] is a particular case of the above assumption when $\beta = 1$. 
[15] の仮定 11 は、$\beta = 1$ のときに上記の仮定の特別な場合であることに注意してください。

We, instead, follow the line of [48], considering an arbitrary order of $T^{\beta}$.
私たちは、代わりに [48] の考え方に従い、$T^{\beta}$ の任意の順序を考慮します。

In the proof of Theorem VII.1, we show that, under Assumptions VII.1 and VII.2, considering the complement set $\mathcal{F}_{\Delta',T}^{\complement} \coloneqq \llbracket T \rrbracket \setminus \mathcal{F}_{\Delta',T}$, for every round $t \in \mathcal{F}_{\Delta',T}^{\complement}$, it holds that:
定理 VII.1 の証明において、仮定 VII.1 および VII.2 の下で、補集合 $\mathcal{F}_{\Delta',T}^{\complement} \coloneqq \llbracket T \rrbracket \setminus \mathcal{F}_{\Delta',T}$ を考慮すると、すべてのラウンド $t \in \mathcal{F}_{\Delta',T}^{\complement}$ に対して次が成り立つ：

$$
\text{(16)}
$$

This implies that $\mathcal{F}_{\tau} = \mathcal{F}_{\Delta',T}$.
これは、$\mathcal{F}_{\tau} = \mathcal{F}_{\Delta',T}$ であることを意味します。

From this fact, it is easy to prove that also $\Delta_{\tau} = \Delta' - 2\sigma\tau$.
この事実から、$\Delta_{\tau} = \Delta' - 2\sigma\tau$ であることも簡単に証明できます。

We are now ready to present the results on the upper bounds of the number of pulls of suboptimal arms for the smoothly changing environment.
これで、滑らかに変化する環境における非最適アームの引き回数の上限に関する結果を提示する準備が整いました。

### Theorem VII.1
### 定理 VII.1

Under Assumptions III.1, VII.1, and VII.2, $\tau \in \mathbb{N}$, for Beta-SWTS, it holds that:
仮定 III.1, VII.1, および VII.2 の下で、$\tau \in \mathbb{N}$ の場合、Beta-SWTS に対して次が成り立ちます：

$$
\text{(17)}
$$

### Theorem VII.2
### 定理 VII.2

Under Assumptions III.2, VII.1, and VII.2, $\tau \in \mathbb{N}$, for $\gamma$-SWGTS with $\gamma \leq \min\left\{\frac{1}{4\lambda^{2}},1\right\}$, it holds that:
仮定 III.2, VII.1, および VII.2 の下で、$\tau \in \mathbb{N}$ の場合、$\gamma$-SWGTS で $\gamma \leq \min\left\{\frac{1}{4\lambda^{2}},1\right\}$ のとき、次が成り立ちます：

$$
\text{(18)}
$$

Again, we identify the two main contributions, the cardinality of the unlearnable set and the expected number of pulls within the learnable set. 
再び、私たちは二つの主要な寄与、すなわち学習不可能な集合の基数と学習可能な集合内の引き回しの期待数を特定します。

The former can be bounded, under Assumption VII.2, by $FT^{\beta}$.
前者は、仮定 VII.2 の下で $FT^{\beta}$ によって制約されます。

The latter is characterized by a sub-optimality gap $\Delta_{\tau}$ that depends on the smoothness parameter $\sigma$ and on the window size $\tau$, capturing the fact that in the rounds in which the distance between the best arm and the suboptimal ones is lower-bounded by $\Delta'$ (as defined in Assumption VII.2), the smooth evolution allows to identify the optimal arm. 
後者は、滑らかさパラメータ $\sigma$ とウィンドウサイズ $\tau$ に依存する非最適性ギャップ $\Delta_{\tau}$ によって特徴付けられます。これは、最良のアームと非最適なアームとの距離が $\Delta'$（仮定 VII.2 で定義された）によって下限されるラウンドにおいて、滑らかな進化が最適なアームを特定できることを示しています。

We remark that the order of $T, \tau$ and $\Delta_{\tau}$ matches the state-of-the-art results when applied to stationary bandits.
$T, \tau$ および $\Delta_{\tau}$ の順序は、定常バンディットに適用した場合の最先端の結果と一致することを指摘します。

Let us compare the previous results with the state-of-the-art ones in an environment characterized by Bernoulli rewards. 
前述の結果を、ベルヌーイ報酬によって特徴付けられる環境における最先端の結果と比較してみましょう。

The order for the regret is given by:
後悔の順序は次のように与えられます：

$$
\text{(19)}
$$

matching the order of the regret obtained in Theorem D.2 by Combes and Proutiere [15] for SW-KL-UCB.
これは、Combes と Proutiere [15] によって SW-KL-UCB のために得られた定理 D.2 の後悔の順序と一致します。



## VIIIExperiments VIII 実験

We experimentally evaluate our algorithms w.r.t.the state-of-the-art algorithms for NS-MABs. 
私たちは、NS-MABに関する最先端のアルゴリズムに対して、私たちのアルゴリズムを実験的に評価します。

In particular, we considered the following baseline algorithms:Rexp3[10], an NS-MAB algorithm based on variation budget,SW-KL-UCB[22], one of the most effective stationary MAB algorithms,Ser4[6], which considers best arm switches during the process, and sliding-window algorithms that are generally able to deal with non-stationary bandit settings such asSW-UCB[24],SW-KL-UCB[15]. 
特に、以下のベースラインアルゴリズムを考慮しました：Rexp3[10]（変動予算に基づくNS-MABアルゴリズム）、SW-KL-UCB[22]（最も効果的な定常MABアルゴリズムの1つ）、プロセス中に最良のアームの切り替えを考慮するSer4[6]、およびSW-UCB[24]やSW-KL-UCB[15]のような非定常バンディット設定に対処できるスライディングウィンドウアルゴリズムです。

We include an algorithm meant for stationary bandits, i.e.,TS[47], to show the impact of the sliding window approach on the regret in dynamic scenarios. 
定常バンディット用のアルゴリズム、すなわちTS[47]を含めて、動的シナリオにおけるスライディングウィンドウアプローチの影響を示します。

The parameters for all the baseline algorithms have been set as recommended in the corresponding papers (see also AppendixCfor details). 
すべてのベースラインアルゴリズムのパラメータは、対応する論文で推奨されているように設定されています（詳細は付録Cも参照してください）。

For all experiments, we considerK=10𝐾10K=10italic_K = 10arms and set the learning horizon toT=5⋅104𝑇⋅5superscript104T=5\cdot 10^{4}italic_T = 5 ⋅ 10 start_POSTSUPERSCRIPT 4 end_POSTSUPERSCRIPT. 
すべての実験において、$K=10$（アームの数）を考慮し、学習ホライズンを$T=5\cdot 10^{4}$に設定します。

The rewards for a chosen armi𝑖iitalic_iwill be sampled from a Bernoulli distribution whose probability of success at timet𝑡titalic_tis given byμi,tsubscript𝜇𝑖𝑡\mu_{i,t}italic_μ start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPTthat will evolve over rounds as specified in the following. 
選択されたアーム$i$の報酬は、時間$t$における成功確率が$\mu_{i,t}$であるベルヌーイ分布からサンプリングされ、以下に示すようにラウンドごとに進化します。

Since we derived above that the order of cumulative regret for our algorithms is the same as that ofSW-UCB, we set the window sizeτ𝜏\tauitalic_τfor TS-like approaches toτ=4TlnT𝜏4𝑇𝑇\tau=4\sqrt{T\ln{T}}italic_τ = 4 square-root start_ARG italic_T roman_ln italic_T end_ARG, as also prescribed byGarivier and Moulines [23]. 
私たちのアルゴリズムの累積的な後悔のオーダーがSW-UCBと同じであることを上で導出したため、TSのようなアプローチのウィンドウサイズ$\tau$を$\tau=4\sqrt{T\ln{T}}$に設定します。これはGarivierとMoulines[23]によっても規定されています。

Regarding our algorithms, we also provide a sensitivity analysis evaluating the cumulative regret for different choices of the window sizeτ𝜏\tauitalic_τ. 
私たちのアルゴリズムに関して、異なるウィンドウサイズ$\tau$の選択に対する累積的な後悔を評価する感度分析も提供します。

We tested our algorithms assuming to misspecify the order of the sliding window w.r.t.the learning horizonT𝑇Titalic_T, formally, we setα∈{0.2,0.4,0.5,0.6,0.8}𝛼0.20.40.50.60.8\alpha\in\{0.2,0.4,0.5,0.6,0.8\}italic_α ∈ { 0.2 , 0.4 , 0.5 , 0.6 , 0.8 }andτ=Tα𝜏superscript𝑇𝛼\tau=T^{\alpha}italic_τ = italic_T start_POSTSUPERSCRIPT italic_α end_POSTSUPERSCRIPT. 
私たちは、学習ホライズン$T$に対するスライディングウィンドウのオーダーを誤って指定することを仮定してアルゴリズムをテストしました。形式的には、$\alpha \in \{0.2, 0.4, 0.5, 0.6, 0.8\}$とし、$\tau=T^{\alpha}$と設定します。

For the sake of notation, we denote the theoretically-based choice for the parameter, i.e.,τ=4TlnT,𝜏4𝑇𝑇\tau=4\sqrt{T\ln{T}},italic_τ = 4 square-root start_ARG italic_T roman_ln italic_T end_ARG ,asτ=T0.5𝜏superscript𝑇0.5\tau=T^{0.5}italic_τ = italic_T start_POSTSUPERSCRIPT 0.5 end_POSTSUPERSCRIPTin the sensitivity analysis. 
記法のために、パラメータの理論に基づく選択、すなわち$\tau=4\sqrt{T\ln{T}}$を、感度分析において$\tau=T^{0.5}$と表記します。

We denote withαTSsubscript𝛼𝑇𝑆\alpha_{TS}italic_α start_POSTSUBSCRIPT italic_T italic_S end_POSTSUBSCRIPTthe misspecification of the sliding window forBetas-SWTSandαGTSsubscript𝛼𝐺𝑇𝑆\alpha_{GTS}italic_α start_POSTSUBSCRIPT italic_G italic_T italic_S end_POSTSUBSCRIPTthe one forγ𝛾\gammaitalic_γ-SWGTS. 
$\alpha_{TS}$はBetas-SWTSのスライディングウィンドウの誤指定を、$\alpha_{GTS}$は$\gamma$-SWGTSの誤指定を示します。

In the following, the results for the different algorithms𝔄𝔄\mathfrak{A}fraktur_Aare provided in terms of the empirical cumulated regretR^t(𝔄)subscript^𝑅𝑡𝔄\hat{R}_{t}(\mathfrak{A})over^ start_ARG italic_R end_ARG start_POSTSUBSCRIPT italic_t end_POSTSUBSCRIPT ( fraktur_A )averaged over50505050independent runs. 
以下に、異なるアルゴリズム$\mathfrak{A}$に対する結果を、$R_{t}(\mathfrak{A})$（50回の独立した実行の平均）という形で提供します。標準偏差は半透明の領域として示されます。



### VIII-A 突然変化するシナリオ

In this scenario, we perform two experiments. 
このシナリオでは、2つの実験を行います。

First, we test the algorithms in a piecewise-constant, abruptly-changing setting. 
まず、段階的に一定で突然変化する設定でアルゴリズムをテストします。

The evolution of the expected reward over time of the arms is provided in Figure 3a, and the formal definition of the expected reward evolution over phases is provided in Appendix C. 
アームの期待報酬の時間に対する進化は図3aに示されており、フェーズごとの期待報酬の進化の正式な定義は付録Cに記載されています。

In the second experiment, we test the algorithms in a general abruptly-changing scenario, i.e., the expected rewards within each phase evolve arbitrarily between two breakpoints. 
2つ目の実験では、一般的な突然変化するシナリオでアルゴリズムをテストします。つまり、各フェーズ内の期待報酬は2つのブレークポイントの間で任意に進化します。

The evolution of the expected rewards is represented in Figure 4a, and the formal definition of the expected reward evolution over time is provided in Appendix C. 
期待報酬の進化は図4aに示されており、時間に対する期待報酬の進化の正式な定義は付録Cに記載されています。

In both settings the optimal arm is $10$ during the $\mathcal{F}_{1}$ and $\mathcal{F}_{3}$ phases and arm $11$ during the $\mathcal{F}_{2}$ and $\mathcal{F}_{4}$ phases. 
両方の設定において、最適なアームはフェーズ$\mathcal{F}_{1}$および$\mathcal{F}_{3}$の間は$10$であり、フェーズ$\mathcal{F}_{2}$および$\mathcal{F}_{4}$の間はアーム$11$です。



#### Results 結果

The results of the regret of the analyzed algorithms are provided in Figures 3b and 4b. 
分析したアルゴリズムの後悔の結果は、図3bおよび4bに示されています。

Since similar conclusions can be drawn from both experiments, for the sake of presentation, we focus on the description of the former. 
両方の実験から類似の結論が導き出せるため、プレゼンテーションの都合上、前者の説明に焦点を当てます。

The algorithms providing the worst performance overall are Rexp3 and Ser4. 
全体的に最も悪いパフォーマンスを提供するアルゴリズムはRexp3とSer4です。

We believe this can be explained by the way some hyperparameters are set based on theoretical considerations, which should be tuned depending on the specific scenario to provide better performance. 
これは、いくつかのハイパーパラメータが理論的考慮に基づいて設定されているためであり、特定のシナリオに応じて調整する必要があると考えています。

During the first phase $\mathcal{F}_{1}$, the best-performing algorithm is TS, since the setting is comparable to a stationary environment during the phase and it is the only algorithm considering the entire history to take decisions. 
最初のフェーズ$\mathcal{F}_{1}$の間、最も良いパフォーマンスを発揮するアルゴリズムはTSです。なぜなら、この設定はフェーズ中の定常環境に類似しており、全履歴を考慮して意思決定を行う唯一のアルゴリズムだからです。

As soon as we change phase, and consequently, the optimal arm changes, all the algorithms start accumulating regret at an increased rate. 
フェーズを変更すると、最適なアームも変わり、すべてのアルゴリズムは増加した速度で後悔を蓄積し始めます。

In particular, the TS algorithm cannot address this change, and its performance degrades as multiple changes occur. 
特に、TSアルゴリズムはこの変化に対処できず、複数の変化が発生するにつれてそのパフォーマンスが低下します。

Conversely, its sliding window counterpart Beta-SWTS provides the best performances starting from the initial part of phase $\mathcal{F}_{2}$ (t ≈ 12.000), showing that forgetting the past is an effective strategy in such a scenario. 
逆に、そのスライディングウィンドウの対応物であるBeta-SWTSは、フェーズ$\mathcal{F}_{2}$の初期部分（$t \approx 12.000$）から最良のパフォーマンスを提供し、過去を忘れることがこのようなシナリオで効果的な戦略であることを示しています。

By the end of the learning horizon, most of the sliding-window-based approaches are able to outperform the TS algorithm. 
学習のホライズンの終わりまでに、ほとんどのスライディングウィンドウベースのアプローチはTSアルゴリズムを上回ることができます。

The fact that $\gamma$-SWGTS is not the best-performing algorithm in this setting is due to the fact that it is designed for generic subgaussian rewards, while the other ones are specifically crafted for Bernoulli rewards. 
$\gamma$-SWGTSがこの設定で最も良いパフォーマンスを発揮しない理由は、一般的なサブガウス報酬のために設計されているのに対し、他のアルゴリズムはベルヌーイ報酬のために特別に作られているからです。

Therefore, in its design, it needs to introduce more exploration to deal with possibly more complex distribution than the Bernoulli. 
したがって、その設計では、ベルヌーイよりもおそらくより複雑な分布に対処するために、より多くの探索を導入する必要があります。



#### Sensitivity Analysis 感度分析

Let us focus on the sensitivity analysis provided in Figure3cand4c. 
図3cおよび4cに示されている感度分析に焦点を当てましょう。

In both environments, we see that for smaller window sizes, i.e., $\alpha=0.2$, the algorithms become too explorative, leading to a larger regret at the end of the learning horizon. 
両方の環境において、ウィンドウサイズが小さい場合、すなわち、$\alpha=0.2$のとき、アルゴリズムは過度に探索的になり、学習のホライズンの終わりにおいて大きな後悔を引き起こします。

This means that we are too aggressive in discarding samples used for the arms’ reward estimates, preventing the algorithms from converging to an optimum when the environment is not changing, i.e., we are not switching to the following phase. 
これは、アームの報酬推定に使用されるサンプルを捨てることに対して過度に攻撃的であることを意味し、環境が変化していないとき、すなわち次のフェーズに切り替えていないときに、アルゴリズムが最適解に収束するのを妨げます。

As the window size increases, the performance for both algorithms improves, achieving the minimum at the suggested window size (i.e., $\tau=4\sqrt{T\log(T)}$) for Beta-SWTS, while $\gamma$-SWGTS reaches its best performance at $\alpha=0.8$, further highlighting the explorative nature of sampling from a Gaussian distribution in a Bernoulli setting. 
ウィンドウサイズが大きくなるにつれて、両方のアルゴリズムの性能が向上し、Beta-SWTSの場合は提案されたウィンドウサイズ（すなわち、$\tau=4\sqrt{T\log(T)}$）で最小値を達成します。一方、$\gamma$-SWGTSは$\alpha=0.8$で最高の性能に達し、ベルヌーイ設定におけるガウス分布からのサンプリングの探索的性質をさらに強調しています。



### VIII-B スムーズに変化するシナリオ

Smoothly Changing Scenario
スムーズに変化するシナリオ

Similarly to what has been done by Combes and Proutiere [15], we test our algorithms on an instance of a smoothly changing environment, as depicted in Figure 5a. 
CombesとProutiere [15]が行ったように、私たちはFigure 5aに示されているスムーズに変化する環境のインスタンスでアルゴリズムをテストします。

In this setting, the smoothness parameter is set to $\sigma=0.0001$. 
この設定では、スムーズさのパラメータは$\sigma=0.0001$に設定されています。

We report the formal evolution of the expected reward and additional results on other smoothly changing environments with different values for the smoothness parameter $\sigma$ in Appendix C. 
期待報酬の正式な進化と、スムーズさのパラメータ$\sigma$の異なる値を持つ他のスムーズに変化する環境に関する追加結果をAppendix Cで報告します。

Even in this environment, the optimal arm changes over time so that each arm is optimal for at least one round over the selected learning horizon. 
この環境でも、最適なアームは時間とともに変化し、各アームは選択された学習ホライズンの間に少なくとも1ラウンドは最適になります。



#### Results 結果

The cumulative regret is provided in Figure5b. 
累積後悔はFigure5bに示されています。

Among the worst performing algorithms we have Ser4, Rexp3, and SW-KL-UCB. 
最もパフォーマンスが悪いアルゴリズムには、Ser4、Rexp3、およびSW-KL-UCBがあります。

Even in this case, the issue is related to the initialization of the parameters that may play a crucial role in having low regret. 
この場合でも、問題はパラメータの初期化に関連しており、低い後悔を得るために重要な役割を果たす可能性があります。

In this setting Beta-SWTS outperforms all the other algorithms in $t \in [30.000, 50.000]$. 
この設定では、Beta-SWTSが$t \in [30.000, 50.000]$の範囲で他のすべてのアルゴリズムを上回ります。

Indeed, it is particularly effective in dealing with cases in which arms whose expected reward was among the lowest becomes optimal. 
実際、期待報酬が最も低いアームが最適になるケースに対処するのに特に効果的です。

For instance, in $t \in [10.000, 20.000]$, phase in which $a_{10}$ become optimal, the Beta-SWTS is providing the lowest increase rate among the analyzed algorithms. 
例えば、$t \in [10.000, 20.000]$のフェーズでは、$a_{10}$が最適になるとき、Beta-SWTSは分析されたアルゴリズムの中で最も低い増加率を提供しています。

Once more, the classical TS algorithm is outperformed by its sliding-window counterpart in $t \in [30.000, 50.000]$. 
再び、古典的なTSアルゴリズムは、$t \in [30.000, 50.000]$の範囲でそのスライディングウィンドウの対応物に劣っています。

Similarly to what happened in the generalized abruptly changing environments, the performance of $\gamma$-SWGTS displays moderate performance in this setting due to the more general formulation of the algorithm. 
一般化された急激に変化する環境で起こったことと同様に、$\gamma$-SWGTSのパフォーマンスは、この設定ではアルゴリズムのより一般的な定式化のために中程度のパフォーマンスを示します。



#### Sensitivity Analysis 感度分析

The sensitivity analysis is presented in Figure5c. 
感度分析はFigure5cに示されています。

The behavior is similar to what we presented in the abruptly-changing scenario. 
その挙動は、急激に変化するシナリオで示したものと似ています。

More specifically, for small sliding window sizes, the algorithms tend to explore more than is needed. 
より具体的には、小さなスライディングウィンドウサイズの場合、アルゴリズムは必要以上に探索する傾向があります。

Conversely, for larger values of the window size, the performance tends to collapse to almost the same regret curve. 
逆に、ウィンドウサイズの値が大きくなると、性能はほぼ同じ後悔曲線に収束する傾向があります。

However, for $\alpha=1$, i.e., using the classical TS, would provide a significantly large regret, which shows the necessity to introduce at least a limited amount of forgetting in such settings. 
しかし、$\alpha=1$、すなわち古典的なTSを使用すると、非常に大きな後悔が生じるため、そのような設定では少なくとも限られた量の忘却を導入する必要性が示されます。

5c  
TS  
(a)  
(b)  
(c)  
Figure 5:  



## IXConclusions IX 結論

We have characterized the performance of TS-like algorithms designed for NS-MABs, namely Beta-SWTS and $\gamma$-SWGTS, in a general formulation for non-stationary setting, deriving general regret bounds to characterize the learning process in any arbitrary environment, for Bernoulli and subgaussian rewards, respectively. 
私たちは、非定常設定の一般的な定式化において、NS-MABs（非定常マルチアームバンディット）向けに設計されたTSライクなアルゴリズム、具体的にはBeta-SWTSと$\gamma$-SWGTSの性能を特徴づけ、ベルヌーイ報酬およびサブガウス報酬に対して任意の環境における学習プロセスを特徴づける一般的な後悔境界を導出しました。

We have shown how such a general result applies to two of the most common non-stationary settings in the literature, namely the abruptly changing environment and the smoothly changing one, deriving upper bounds on the regret that are in line with the state of the art. 
私たちは、このような一般的な結果が文献における最も一般的な2つの非定常設定、すなわち急激に変化する環境と滑らかに変化する環境にどのように適用されるかを示し、最先端の研究に沿った後悔の上限を導出しました。

Finally, we have performed numerical validations of the proposed algorithms against the baselines that represent the state-of-the-art solutions for learning in dynamic scenarios, showing how the sliding window approach applied to the TS algorithm is a viable solution to deal with Non-Stationary settings. 
最後に、動的シナリオにおける学習の最先端ソリューションを表すベースラインに対して提案したアルゴリズムの数値的検証を行い、TSアルゴリズムに適用されたスライディングウィンドウアプローチが非定常設定に対処するための実行可能な解決策であることを示しました。

Future lines of research include developing specialized TS-like algorithms that take into account the specific nature of the non-stationarity or extending the analysis to non-stationary cases in which the arms reward presents a structure among them, such as linear bandits. 
今後の研究の方向性には、非定常性の特定の性質を考慮した専門的なTSライクなアルゴリズムの開発や、アームの報酬が線形バンディットのようにそれらの間に構造を持つ非定常ケースへの分析の拡張が含まれます。



## References 参考文献

- Abramowitz and Stegun [1968]↑Milton Abramowitz and IreneA Stegun.Handbook of mathematical functions with formulas, graphs, and mathematical tables.US Government printing office, 55, 1968.
- Abramowitz and Stegun [1968]↑ミルトン・アブラモウィッツとアイリーン・A・ステグン。数式、グラフ、数学的表を含む数学関数のハンドブック。アメリカ合衆国政府印刷局、55、1968年。
  
- Agarwal [2013]↑Deepak Agarwal.Computational advertising: the linkedin way.InProceedings of the Conference on Information & Knowledge Management (CIKM), pages 1585–1586, 2013.
- Agarwal [2013]↑ディーパク・アガルワル。計算広告：LinkedInの方法。情報と知識管理に関する会議の議事録（CIKM）、ページ1585–1586、2013年。

- Agarwal etal. [2014]↑Deepak Agarwal, BoLong, Jonathan Traupman, Doris Xin, and Liang Zhang.Laser: A scalable response prediction platform for online advertising.InProceedings of the ACM international conference on Web Search and Data Mining (WSDM), pages 173–182, 2014.
- Agarwal etal. [2014]↑ディーパク・アガルワル、ボ・ロン、ジョナサン・トラウプマン、ドリス・シン、リャン・チャン。レーザー：オンライン広告のためのスケーラブルな応答予測プラットフォーム。ACM国際会議の議事録（WSDM）、ページ173–182、2014年。

- Agrawal and Goyal [2012]↑Shipra Agrawal and Navin Goyal.Analysis of thompson sampling for the multi-armed bandit problem.InProceedings of the Conference on learning theory (COLT), 2012.
- Agrawal and Goyal [2012]↑シプラ・アグラワルとナビン・ゴヤル。マルチアームバンディット問題に対するトンプソンサンプリングの分析。学習理論に関する会議の議事録（COLT）、2012年。

- Agrawal and Goyal [2017]↑Shipra Agrawal and Navin Goyal.Near-optimal regret bounds for thompson sampling.Journal of the ACM (JACM), 64(5):1–24, 2017.
- Agrawal and Goyal [2017]↑シプラ・アグラワルとナビン・ゴヤル。トンプソンサンプリングのためのほぼ最適な後悔境界。ACMジャーナル（JACM）、64(5):1–24、2017年。

- Allesiardo etal. [2017]↑Robin Allesiardo, Raphaël Féraud, and Odalric-Ambrym Maillard.The non-stationary stochastic multi-armed bandit problem.International Journal of Data Science and Analytics, 3(4):267–283, 2017.
- Allesiardo etal. [2017]↑ロビン・アレシアルド、ラファエル・フェロー、オダリック・アンブリム・マイラルド。非定常確率的マルチアームバンディット問題。データサイエンスと分析の国際ジャーナル、3(4):267–283、2017年。

- Auer etal. [2002]↑Peter Auer, Nicolo Cesa-Bianchi, and Paul Fischer.Finite-time analysis of the multiarmed bandit problem.Machine learning, 47:235–256, 2002.
- Auer etal. [2002]↑ピーター・アウアー、ニコロ・チェーザ・ビアンキ、ポール・フィッシャー。マルチアームバンディット問題の有限時間分析。機械学習、47:235–256、2002年。

- Aziz etal. [2021]↑Maryam Aziz, Emilie Kaufmann, and Marie-Karelle Riviere.On multi-armed bandit designs for dose-finding trials.Journal of Machine Learning Research (JMLR), 22(14):1–38, 2021.
- Aziz etal. [2021]↑マリアム・アジズ、エミリー・カウフマン、マリー・カレール・リビエール。用量探索試験のためのマルチアームバンディットデザインについて。機械学習研究ジャーナル（JMLR）、22(14):1–38、2021年。

- Basseville etal. [1993]↑Michele Basseville, IgorV Nikiforov, etal.Detection of abrupt changes: theory and application.Prentice Hall Englewood Cliffs, 104, 1993.
- Basseville etal. [1993]↑ミケーレ・バッセヴィル、イゴール・V・ニキフォロフ、他。急激な変化の検出：理論と応用。プレンティス・ホール、エンゲルウッド・クリフス、104、1993年。

- Besbes etal. [2014]↑Omar Besbes, Yonatan Gur, and Assaf Zeevi.Stochastic multi-armed-bandit problem with non-stationary rewards.Advances in neural information processing systems (NeurIPS), 2014.
- Besbes etal. [2014]↑オマール・ベスベス、ヨナタン・グル、アッサフ・ゼエビ。非定常報酬を持つ確率的マルチアームバンディット問題。神経情報処理システムの進展（NeurIPS）、2014年。

- Besson etal. [2022]↑Lilian Besson, Emilie Kaufmann, Odalric-Ambrym Maillard, and Julien Seznec.Efficient change-point detection for tackling piecewise-stationary bandits.Journal of Mchine Learning Research (JMLR), 23(77):1–40, 2022.
- Besson etal. [2022]↑リリアン・ベッソン、エミリー・カウフマン、オダリック・アンブリム・マイラルド、ジュリアン・セズネック。区分的定常バンディットに対処するための効率的な変化点検出。機械学習研究ジャーナル（JMLR）、23(77):1–40、2022年。

- Bi etal. [2024]↑Wenjie Bi, Bing Wang, and Haiying Liu.Personalized dynamic pricing based on improved thompson sampling.Mathematics, 12(8):1123, 2024.
- Bi etal. [2024]↑ウェンジー・ビ、ビン・ワン、ハイイン・リウ。改良されたトンプソンサンプリングに基づく個別化された動的価格設定。数学、12(8):1123、2024年。

- Cesa-Bianchi and Lugosi [2006]↑Nicolo Cesa-Bianchi and Gábor Lugosi.Prediction, learning, and games.Cambridge university press, 2006.
- Cesa-Bianchi and Lugosi [2006]↑ニコロ・チェーザ・ビアンキとガーボル・ルゴシ。予測、学習、ゲーム。ケンブリッジ大学出版、2006年。

- Chapelle and Li [2011]↑Olivier Chapelle and Lihong Li.An empirical evaluation of thompson sampling.InAdvances in Neural Information Processing Systems (NeurIPS), 2011.
- Chapelle and Li [2011]↑オリビエ・シャペルとリホン・リー。トンプソンサンプリングの実証評価。神経情報処理システムの進展（NeurIPS）、2011年。

- Combes and Proutiere [2014]↑Richard Combes and Alexandre Proutiere.Unimodal bandits: Regret lower bounds and optimal algorithms.InProceedings of the International Conference on Machine Learning (ICML), volume32, pages 521–529, 2014.
- Combes and Proutiere [2014]↑リチャード・コンブとアレクサンドル・プルティエール。単峰バンディット：後悔の下限と最適アルゴリズム。国際機械学習会議の議事録（ICML）、第32巻、ページ521–529、2014年。

- Dasgupta etal. [2024]↑Arpan Dasgupta, Gagan Jain, Arun Suggala, Karthikeyan Shanmugam, Milind Tambe, and Aparna Taneja.Bayesian collaborative bandits with thompson sampling for improved outreach in maternal health program.2024.URLhttps://arxiv.org/abs/2410.21405.
- Dasgupta etal. [2024]↑アルパン・ダスグプタ、ガガン・ジャイン、アラン・サッガラ、カルティケヤン・シャヌムガム、ミリンド・タンベ、アパルナ・タネジャ。母子保健プログラムにおけるアウトリーチを改善するためのトンプソンサンプリングを用いたベイズ的協調バンディット。2024年。URLhttps://arxiv.org/abs/2410.21405。

- deFreitasFonseca etal. [2024]↑Gustavo deFreitasFonseca, LucasCoelho eSilva, and Paulo AndréLima deCastro.Addressing non-stationarity with relaxed f-discounted-sliding-window thompson sampling.In2024 IEEE International Conference on Omni-layer Intelligent Systems (COINS), pages 1–6. IEEE, 2024.
- deFreitasFonseca etal. [2024]↑グスタボ・デ・フレイタス・フォンセカ、ルーカス・コエーリョ・エ・シルバ、パウロ・アンドレ・リマ・デ・カストロ。リラックスしたf割引スライディングウィンドウトンプソンサンプリングによる非定常性への対処。2024年IEEE国際会議オムニレイヤーインテリジェントシステム（COINS）、ページ1–6。IEEE、2024年。

- Dixit etal. [2023]↑KrishnaKant Dixit, Devvret Verma, SureshKumar Muthuvel, KLaxminarayanamma, Mukesh Kumar, and Amit Srivastava.Thompson sampling algorithm for personalized treatment recommendations in healthcare.In2023 International Conference on Artificial Intelligence for Innovations in Healthcare Industries (ICAIIHI), volume1, pages 1–6. IEEE, 2023.
- Dixit etal. [2023]↑クリシュナ・カント・ディクシット、デヴヴレト・ヴェルマ、スレシュ・クマール・ムトゥヴェル、K・ラクシュミナラヤンアマ、ムケシュ・クマール、アミット・スリバスタバ。ヘルスケアにおける個別化された治療推奨のためのトンプソンサンプリングアルゴリズム。2023年人工知能とヘルスケア産業の革新に関する国際会議（ICAIIHI）、第1巻、ページ1–6。IEEE、2023年。

- Fiandri etal. [2024]↑Marco Fiandri, AlbertoMaria Metelli, and Francesco Trovò.Sliding-window thompson sampling for non-stationary settings.2024.URLhttps://arxiv.org/abs/2409.051810.
- Fiandri etal. [2024]↑マルコ・フィアンドリ、アルベルト・マリア・メテッリ、フランチェスコ・トロヴォ。非定常設定のためのスライディングウィンドウトンプソンサンプリング。2024年。URLhttps://arxiv.org/abs/2409.051810。

- Fiandri etal. [2025]↑Marco Fiandri, AlbertoMaria Metelli, and Francesco Trovò.Thompson sampling-like algorithms for stochastic rising bandits, 2025.URLhttps://arxiv.org/abs/2505.12092.
- Fiandri etal. [2025]↑マルコ・フィアンドリ、アルベルト・マリア・メテッリ、フランチェスコ・トロヴォ。確率的上昇バンディットのためのトンプソンサンプリングに似たアルゴリズム、2025年。URLhttps://arxiv.org/abs/2505.12092。

- Ganti etal. [2018]↑Ravi Ganti, Matyas Sustik, Quoc Tran, and Brian Seaman.Thompson sampling for dynamic pricing.2018.URLhttps://arxiv.org/abs/1802.03050.
- Ganti etal. [2018]↑ラビ・ガンティ、マティアス・サスティク、クォック・トラン、ブライアン・シーマン。動的価格設定のためのトンプソンサンプリング。2018年。URLhttps://arxiv.org/abs/1802.03050。

- Garivier and Cappé [2011]↑Aurélien Garivier and Olivier Cappé.The kl-ucb algorithm for bounded stochastic bandits and beyond.InProceedings of the Conference On Learning Theory (COLT), pages 359–376, 2011.
- Garivier and Cappé [2011]↑オーレリアン・ガリビエとオリビエ・カッペ。制約付き確率的バンディットのためのkl-ucbアルゴリズム。学習理論に関する会議の議事録（COLT）、ページ359–376、2011年。

- Garivier and Moulines [2008]↑Aurélien Garivier and Eric Moulines.On upper-confidence bound policies for non-stationary bandit problems.2008.URLhttps://arxiv.org/abs/0805.3415.
- Garivier and Moulines [2008]↑オーレリアン・ガリビエとエリック・ムーリネス。非定常バンディット問題に対する上限信頼区間ポリシーについて。2008年。URLhttps://arxiv.org/abs/0805.3415。

- Garivier and Moulines [2011]↑Aurélien Garivier and Eric Moulines.On upper-confidence bound policies for switching bandit problems.InProceedings of the international conference on Algorithmic Learning Theory (ALT), 2011.
- Garivier and Moulines [2011]↑オーレリアン・ガリビエとエリック・ムーリネス。スイッチングバンディット問題に対する上限信頼区間ポリシーについて。アルゴリズミック学習理論に関する国際会議の議事録（ALT）、2011年。

- Graepel etal. [2010]↑Thore Graepel, JoaquinQuinonero Candela, Thomas Borchert, and Ralf Herbrich.Web-scale bayesian click-through rate prediction for sponsored search advertising in microsoft’s bing search engine.Omnipress, 2010.
- Graepel etal. [2010]↑トーレ・グレペル、ホアキン・キノネロ・カンデラ、トーマス・ボルヒェルト、ラルフ・ヘルブリッヒ。マイクロソフトのBing検索エンジンにおけるスポンサー検索広告のためのウェブスケールベイズ的クリック率予測。オムニプレス、2010年。

- Heidari etal. [2016]↑Hoda Heidari, MichaelJ Kearns, and Aaron Roth.Tight policy regret bounds for improving and decaying bandits.InProceedings of the International Joint Conference on Artificial Intelligence (IJCAI), pages 1562–1570, 2016.
- Heidari etal. [2016]↑ホダ・ヘイダリ、マイケル・J・カーン、アーロン・ロス。改善および減衰バンディットのための厳密なポリシー後悔境界。国際人工知能合同会議（IJCAI）の議事録、ページ1562–1570、2016年。

- Jaiswal etal. [2025]↑Prateek Jaiswal, Esmaeil Keyvanshokooh, and Junyu Cao.Deconfounded warm-start thompson sampling with applications to precision medicine, 2025.URLhttps://arxiv.org/abs/2505.17283.
- Jaiswal etal. [2025]↑プラティーク・ジャイスワル、エスマイル・ケイバンショコフ、ジュンユ・カオ。精密医療への応用を伴うデコンファウンド・ウォームスタート・トンプソンサンプリング、2025年。URLhttps://arxiv.org/abs/2505.17283。

- Kandasamy etal. [2018]↑Kirthevasan Kandasamy, Willie Neiswanger, Jeff Schneider, Barnabas Poczos, and EricP Xing.Neural architecture search with bayesian optimisation and optimal transport.Advances in neural information processing systems (NeurIPS), 2018.
- Kandasamy etal. [2018]↑キルテヴァサン・カンダサミ、ウィリー・ネイスワンガー、ジェフ・シュナイダー、バルナバス・ポコズ、エリック・P・シン。ベイズ最適化と最適輸送を用いたニューラルアーキテクチャ探索。神経情報処理システムの進展（NeurIPS）、2018年。

- Kaufmann etal. [2012]↑Emilie Kaufmann, Nathaniel Korda, and Rémi Munos.Thompson sampling: An asymptotically optimal finite-time analysis.InProceedings of the international conference on Algorithmic Learning Theory (ALT), 2012.
- Kaufmann etal. [2012]↑エミリー・カウフマン、ナサニエル・コルダ、レミ・ムノス。トンプソンサンプリング：漸近的に最適な有限時間分析。アルゴリズミック学習理論に関する国際会議の議事録（ALT）、2012年。

- Kawale etal. [2015]↑Jaya Kawale, HungH Bui, Branislav Kveton, Long Tran-Thanh, and Sanjay Chawla.Efficient thompson sampling for online matrix-factorization recommendation.Advances in neural information processing systems (NeurIPS), 2015.
- Kawale etal. [2015]↑ジャヤ・カワレ、フンH・ブイ、ブラニスラフ・クヴェトン、ロング・トラン・タン、サンジェイ・チャウラ。オンライン行列因子分解推薦のための効率的なトンプソンサンプリング。神経情報処理システムの進展（NeurIPS）、2015年。

- Lai and Robbins [1985]↑TzeLeung Lai and Herbert Robbins.Asymptotically efficient adaptive allocation rules.Advances in applied mathematics, 6(1):4–22, 1985.
- Lai and Robbins [1985]↑ライ・ツェルンとハーバート・ロビンズ。漸近的に効率的な適応的配分ルール。応用数学の進展、6(1):4–22、1985年。

- Lattimore and Szepesvári [2020]↑Tor Lattimore and Csaba Szepesvári.Bandit algorithms.Cambridge University Press, 2020.
- Lattimore and Szepesvári [2020]↑トール・ラッティモアとチャバ・セペシュヴァリ。バンディットアルゴリズム。ケンブリッジ大学出版、2020年。

- Liu etal. [2018]↑Fang Liu, Joohyun Lee, and Ness Shroff.A change-detection based framework for piecewise-stationary multi-armed bandit problem.InProceedings of the Conference on Artificial Intelligence (AAAI), volume32, 2018.
- Liu etal. [2018]↑ファン・リウ、ジョーヒョン・リー、ネス・シュロフ。区分的定常マルチアームバンディット問題のための変化検出に基づくフレームワーク。人工知能に関する会議の議事録（AAAI）、第32巻、2018年。

- Liu etal. [2023]↑Yueyang Liu, Benjamin VanRoy, and Kuang Xu.Nonstationary bandit learning via predictive sampling.International Conference on Artificial Intelligence and Statistics (AISTATS), 2023.
- Liu etal. [2023]↑ユエヤン・リウ、ベンジャミン・バンロイ、クァン・シュー。予測サンプリングによる非定常バンディット学習。人工知能と統計に関する国際会議（AISTATS）、2023年。

- Lu etal. [2021]↑Yangyi Lu, Ziping Xu, and Ambuj Tewari.Bandit algorithms for precision medicine.2021.URLhttps://arxiv.org/abs/2108.04782.
- Lu etal. [2021]↑ヤンイー・ル、ジーピン・シュー、アンブジュ・テワリ。精密医療のためのバンディットアルゴリズム。2021年。URLhttps://arxiv.org/abs/2108.04782。

- Metelli etal. [2022]↑AlbertoMaria Metelli, Francesco Trovò, Matteo Pirola, and Marcello Restelli.Stochastic rising bandits.InProceedings of the International Conference on Machine Learning (ICML), volume 162, pages 15421–15457, 2022.
- Metelli etal. [2022]↑アルベルト・マリア・メテッリ、フランチェスコ・トロヴォ、マッテオ・ピロラ、マルチェロ・レステッリ。確率的上昇バンディット。国際機械学習会議の議事録（ICML）、第162巻、ページ15421–15457、2022年。

- Pandey and Olston [2006]↑Sandeep Pandey and Christopher Olston.Handling advertisements of unknown quality in search advertising.InAdvances in Neural Information Processing Systems (NeurIPS), 2006.
- Pandey and Olston [2006]↑サンディープ・パンデイとクリストファー・オルストン。検索広告における未知の品質の広告の取り扱い。神経情報処理システムの進展（NeurIPS）、2006年。

- Qi etal. [2025]↑Han Qi, Fei Guo, and LiZhu.Thompson sampling for non-stationary bandit problems.Entropy, 27(1):51, 2025.
- Qi etal. [2025]↑ハン・チー、フェイ・グオ、リ・ズー。非定常バンディット問題のためのトンプソンサンプリング。エントロピー、27(1):51、2025年。

- Raj and Kalyani [2017]↑Vishnu Raj and Sheetal Kalyani.Taming non-stationary bandits: A bayesian approach.2017.URLhttps://arxiv.org/abs/1707.09727.
- Raj and Kalyani [2017]↑ヴィシュヌ・ラージとシータル・カリヤニ。非定常バンディットの制御：ベイズ的アプローチ。2017年。URLhttps://arxiv.org/abs/1707.09727。

- Re etal. [2021]↑Gerlando Re, Fabio Chiusano, Francesco Trovò, Diego Carrera, Giacomo Boracchi, and Marcello Restelli.Exploiting history data for nonstationary multi-armed bandit.InProceedings of the European Conference on Machine Learning (ECML), pages 51–66, 2021.
- Re etal. [2021]↑ジェルランド・レ、ファビオ・キウザーノ、フランチェスコ・トロヴォ、ディエゴ・カレラ、ジャコモ・ボラッキ、マルチェロ・レステッリ。非定常マルチアームバンディットのための履歴データの活用。欧州機械学習会議の議事録（ECML）、ページ51–66、2021年。

- Rigollet and Hütter [2023]↑Philippe Rigollet and Jan-Christian Hütter.High-dimensional statistics.2023.URLhttps://arxiv.org/abs/2310.19244.
- Rigollet and Hütter [2023]↑フィリップ・リゴレとヤン・クリスチャン・ヒュッター。高次元統計。2023年。URLhttps://arxiv.org/abs/2310.19244。

- Roch [2024]↑Sebastien Roch.Modern discrete probability: An essential toolkit.Cambridge University Press, 2024.
- Roch [2024]↑セバスチャン・ロッシュ。現代の離散確率：必須ツールキット。ケンブリッジ大学出版、2024年。

- Russo and VanRoy [2016]↑Daniel Russo and Benjamin VanRoy.An information-theoretic analysis of thompson sampling.Journal of Machine Learning Research (JMLR), 17(68):1–30, 2016.
- Russo and VanRoy [2016]↑ダニエル・ルッソとベンジャミン・バンロイ。トンプソンサンプリングの情報理論的分析。機械学習研究ジャーナル（JMLR）、17(68):1–30、2016年。

- Scott [2010]↑Steven Scott.A modern bayesian look at the multi-armed bandit.Applied Stochastic Models in Business and Industry, 26:639 – 658, 11 2010.
- Scott [2010]↑スティーブン・スコット。現代のベイズ的視点から見たマルチアームバンディット。ビジネスと産業における応用確率モデル、26:639 – 658、2010年11月。

- Seznec etal. [2019]↑Julien Seznec, Andrea Locatelli, Alexandra Carpentier, Alessandro Lazaric, and Michal Valko.Rotting bandits are no harder than stochastic ones.InThe International Conference on Artificial Intelligence and Statistics (AISTATS), volume89, pages 2564–2572, 2019.
- Seznec etal. [2019]↑ジュリアン・セズネック、アンドレア・ロカテッリ、アレクサンドラ・カルパンティエ、アレッサンドロ・ラザリック、ミハル・ヴァルコ。腐敗バンディットは確率的バンディットよりも難しくない。人工知能と統計に関する国際会議（AISTATS）、第89巻、ページ2564–2572、2019年。

- Seznec etal. [2020]↑Julien Seznec, Pierre Menard, Alessandro Lazaric, and Michal Valko.A single algorithm for both restless and rested rotting bandits.InProceedings of the International Conference on Artificial Intelligence and Statistics (AISTATS), volume 108, pages 3784–3794, 2020.
- Seznec etal. [2020]↑ジュリアン・セズネック、ピエール・メナル、アレッサンドロ・ラザリック、ミハル・ヴァルコ。落ち着かないバンディットと落ち着いたバンディットの両方に対する単一のアルゴリズム。人工知能と統計に関する国際会議（AISTATS）の議事録、第108巻、ページ3784–3794、2020年。

- Thompson [1933]↑WilliamR. Thompson.On the likelihood that one unknown probability exceeds another in view of the evidence of two samples.Biometrika, 25(3/4):285–294, 1933.
- Thompson [1933]↑ウィリアムR・トンプソン。2つのサンプルの証拠に基づいて、1つの未知の確率が別の確率を超える可能性について。バイオメトリカ、25(3/4):285–294、1933年。

- Trovò etal. [2020]↑Francesco Trovò, Stefano Paladino, Marcello Restelli, and Nicola Gatti.Sliding-window thompson sampling for non-stationary settings.Journal of Artificial Intelligence Research (JAIR), 68:311–364, 2020.
- Trovò etal. [2020]↑フランチェスコ・トロヴォ、ステファノ・パラディーノ、マルチェロ・レステッリ、ニコラ・ガッティ。非定常設定のためのスライディングウィンドウトンプソンサンプリング。人工知能研究ジャーナル（JAIR）、68:311–364、2020年。

- Wang [1993]↑Y.H. Wang.On the number of successes in independent trials.Statistica Sinica, 3(2):295–312, 1993.
- Wang [1993]↑Y.H.ワン。独立試行における成功の数について。統計学シニカ、3(2):295–312、1993年。

- Whittle [1988]↑P.Whittle.Restless bandits: Activity allocation in a changing world.Journal of Applied Probability, 25:287–298, 1988.ISSN 00219002.
- Whittle [1988]↑P・ウィットル。落ち着かないバンディット：変化する世界における活動配分。応用確率ジャーナル、25:287–298、1988年。ISSN 00219002。



## Code Availability コードの入手可能性

All the codes are publicly available at the following link: https://github.com/albertometelli/stochastic-rising-bandits.
すべてのコードは、以下のリンクで公開されています: https://github.com/albertometelli/stochastic-rising-bandits.



## Appendix A 付録 A

We now present two Lemmas that will be useful throughout the analysis.  
ここでは、分析に役立つ2つの補題を示します。

### Definition A.1 定義 A.1

Let $i,i^{\prime} \in \llbracket K \rrbracket$ be two arms, $t \in \llbracket T \rrbracket$ be a round, $\tau \in \llbracket T \rrbracket$ be the window, and $y_{i^{\prime},t} \in (0,1)$ be a threshold, we define:  
$i,i^{\prime} \in \llbracket K \rrbracket$ を2つのアームとし、$t \in \llbracket T \rrbracket$ をラウンド、$\tau \in \llbracket T \rrbracket$ をウィンドウ、$y_{i^{\prime},t} \in (0,1)$ を閾値とすると、次のように定義します：

$$
\mathcal{F}_{t} 
$$  
ここで、$\mathcal{F}_{t}$ は、ラウンド $t$ までにプレイされたアームのシーケンスと観測された報酬によって誘導されるフィルトレーションです。

### Definition A.2 定義 A.2

For each $i \in \llbracket K \rrbracket$, we define the set of rounds $t \in \mathcal{F}_{\tau}^{\complement}$ and $i \neq i^{*}(t)$ as $\mathcal{F}_{i,\tau}^{\complement}$. Formally:  
各 $i \in \llbracket K \rrbracket$ に対して、$t \in \mathcal{F}_{\tau}^{\complement}$ かつ $i \neq i^{*}(t)$ のラウンドの集合を $\mathcal{F}_{i,\tau}^{\complement}$ と定義します。形式的には：

$$
\mathcal{F}_{i,\tau}^{\complement} 
$$  

We propose a slight modification of Lemma 5.1 from [20] and Lemma C.1 from [20], to obtain results that are more suitable to describe the regret in restless setting.  
私たちは、[20] の補題 5.1 と [20] の補題 C.1 のわずかな修正を提案し、落ち着きのない設定における後悔を説明するのにより適した結果を得ます。

### Lemma 1 補題 1

**Beta-SWTS**  
Let $T \in \mathbb{N}$ be the learning horizon, $\tau \in \llbracket T \rrbracket$ the window size, for the Beta-SWTS algorithm it holds for every free parameter $\omega \in \llbracket 0,T \rrbracket$ that:  
$T \in \mathbb{N}$ を学習のホライズンとし、$\tau \in \llbracket T \rrbracket$ をウィンドウサイズとすると、Beta-SWTS アルゴリズムに対して、任意の自由パラメータ $\omega \in \llbracket 0,T \rrbracket$ に対して次のようになります：

The proof will follow the same steps of the proof in [20] with some changes to adapt to the restless setting.  
証明は、落ち着きのない設定に適応するためのいくつかの変更を加えつつ、[20] の証明の同じステップに従います。

We define the event $E_{i}(t) \coloneqq \{\theta_{i,t,\tau} \leq y_{i,t}\}$. Thus, assigning immediate regret equal to one for every round in $\mathcal{F}_{\tau}$ the following holds:  
イベント $E_{i}(t) \coloneqq \{\theta_{i,t,\tau} \leq y_{i,t}\}$ を定義します。したがって、$\mathcal{F}_{\tau}$ のすべてのラウンドに対して即時の後悔を1とすると、次のようになります：

$$
\text{(22)}
$$  

Let us first face term (A):  
まず、項 (A) に取り組みましょう：

$$
\text{(A)}
$$  

Observe that (C) can be bounded by Lemma 8. Thus, the above inequality can be rewritten as:  
(C) は補題 8 によって制約されることに注意してください。したがって、上記の不等式は次のように書き換えることができます：

$$
\text{(A)}
$$  

We now focus on the term (D). Defining $\mathcal{T} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) > \frac{1}{\tau}, N_{i,t,\tau} \geq \omega\}$ assign $\mathcal{T}$ conditional-set.  
次に、項 (D) に焦点を当てます。$\mathcal{T} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) > \frac{1}{\tau}, N_{i,t,\tau} \geq \omega\}$ を定義し、$\mathcal{T}$ 条件付き集合を割り当てます。

$$
\mathcal{T} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) > \frac{1}{\tau}, N_{i,t,\tau} \geq \omega\}
$$  

and $\mathcal{T}^{\prime} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) \leq \frac{1}{\tau}, N_{i,t,\tau} \geq \omega\}$ assign $\mathcal{T}^{\prime}$ conditional-set.  
また、$\mathcal{T}^{\prime} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) \leq \frac{1}{\tau}, N_{i,t,\tau} \geq \omega\}$ を定義し、$\mathcal{T}^{\prime}$ 条件付き集合を割り当てます。

$$
\mathcal{T}^{\prime} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) \leq \frac{1}{\tau}, N_{i,t,\tau} \geq \omega\}
$$  

Now we focus on term (B). We have:  
今、項 (B) に焦点を当てます。次のようになります：

$$
\text{(32)}
$$  

In order to bound (B) we need to bound (E).  
(B) を制約するためには、(E) を制約する必要があります。

Let $i^{\prime} = \operatorname{argmax}_{i \neq i^{*}(t)} \theta_{i,t,\tau}$. Then, we have:  
$i^{\prime} = \operatorname{argmax}_{i \neq i^{*}(t)} \theta_{i,t,\tau}$ とします。すると、次のようになります：

$$
\text{(33)}
$$  

The statement follows by summing all the terms.  
すべての項を合計することによって、命題が成り立ちます。

∎

### Lemma 2 補題 2

**-SWGTS**  
Let $T \in \mathbb{N}$ be the learning horizon, $\tau \in \llbracket T \rrbracket$ be the window size, for the $\gamma$-ET-SWGTS algorithm the following holds for every $i \neq i^{*}(t)$ and free parameters $\omega \in \llbracket T \rrbracket$ and $\epsilon > 0$:  
$T \in \mathbb{N}$ を学習のホライズンとし、$\tau \in \llbracket T \rrbracket$ をウィンドウサイズとすると、$\gamma$-ET-SWGTS アルゴリズムに対して、任意の $i \neq i^{*}(t)$ と自由パラメータ $\omega \in \llbracket T \rrbracket$ および $\epsilon > 0$ に対して次のようになります：

We define the event $E_{i}(t) \coloneqq \{\theta_{i,t,\tau} \leq y_{i,t}\}$. Thus, the following holds, assigning "error" equal to one for every round in $\mathcal{F}_{\tau}$:  
イベント $E_{i}(t) \coloneqq \{\theta_{i,t,\tau} \leq y_{i,t}\}$ を定義します。したがって、$\mathcal{F}_{\tau}$ のすべてのラウンドに対して "エラー" を1とすると、次のようになります：

$$
\text{(36)}
$$  

Let us first face term (A):  
まず、項 (A) に取り組みましょう：

$$
\text{(A)}
$$  

Observe that (C) can be bounded by Lemma 8. Thus, the above inequality can be rewritten as:  
(C) は補題 8 によって制約されることに注意してください。したがって、上記の不等式は次のように書き換えることができます：

$$
\text{(A)}
$$  

We now focus on the term (D). Defining $\mathcal{T} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) > \frac{1}{\tau \epsilon_{i}}, N_{i,t,\tau} \geq \omega\}$ assign $\mathcal{T}$ conditional-set.  
次に、項 (D) に焦点を当てます。$\mathcal{T} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) > \frac{1}{\tau \epsilon_{i}}, N_{i,t,\tau} \geq \omega\}$ を定義し、$\mathcal{T}$ 条件付き集合を割り当てます。

$$
\mathcal{T} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) > \frac{1}{\tau \epsilon_{i}}, N_{i,t,\tau} \geq \omega\}
$$  

and $\mathcal{T}^{\prime} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) \leq \frac{1}{\tau \epsilon_{i}}, N_{i,t,\tau} \geq \omega\}$ assign $\mathcal{T}^{\prime}$ conditional-set.  
また、$\mathcal{T}^{\prime} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) \leq \frac{1}{\tau \epsilon_{i}}, N_{i,t,\tau} \geq \omega\}$ を定義し、$\mathcal{T}^{\prime}$ 条件付き集合を割り当てます。

$$
\mathcal{T}^{\prime} := \{t \in \mathcal{F}_{i,\tau}^{\complement} : 1 - \mathbb{P}(\theta_{i,t,\tau} \leq y_{i,t} \mid \mathcal{F}_{t-1}) \leq \frac{1}{\tau \epsilon_{i}}, N_{i,t,\tau} \geq \omega\}
$$  

Term (B) is bounded exactly as in the proof of Lemma 1. The statement follows by summing all the terms.  
項 (B) は補題 1 の証明と同様に制約されます。すべての項を合計することによって、命題が成り立ちます。

∎



## Appendix BProofs 付録B 証明

Appendix B  
付録B  

See V.1  
V.1  

First of all, let us recall Lemma 1:  
まず最初に、補題1を思い出しましょう：  

Let us define the two threshold quantities $x_{i,t}$ and $y_{i,t}$ for $t \in \mathcal{F}_{i,\tau}^{\complement}$ (the time the policy-maker has to choose the arm) as:  
$ t \in \mathcal{F}_{i,\tau}^{\complement} $ のための2つの閾値量 $x_{i,t}$ と $y_{i,t}$ を定義します（政策決定者がアームを選択するための時間）：

$$
\Delta_{i,t,\tau} = \min_{t^{\prime} \in \llbracket t - \tau, t - 1 \rrbracket} \{ \mu_{i^{*}(t), t^{\prime}} \} - \max_{t^{\prime} \in \llbracket t - 1, t - \tau \rrbracket} \{ \mu_{i(t), t^{\prime}} \}
$$  
$$
\Delta_{i,t,\tau} = \min_{t^{\prime} \in \llbracket t - \tau, t - 1 \rrbracket} \{ \mu_{i^{*}(t), t^{\prime}} \} - \max_{t^{\prime} \in \llbracket t - 1, t - \tau \rrbracket} \{ \mu_{i(t), t^{\prime}} \}
$$  

we will always consider in the following analysis the choices:  
以下の分析では、常に次の選択肢を考慮します：  

Notice then that the following quantities will have their minima for those $t \in \mathcal{F}_{\tau}^{\complement}$ such that $\Delta_{i,t,\tau} = \Delta_{\tau}$:  
次に、以下の量は、$\Delta_{i,t,\tau} = \Delta_{\tau}$ となるような $t \in \mathcal{F}_{\tau}^{\complement}$ に対して最小値を持つことに注意してください：  

$$
\Delta_{i,t,\tau} = \Delta_{\tau}
$$  
$$
\Delta_{i,t,\tau} = \Delta_{\tau}
$$  

and independently from the time $t \in \llbracket T \rrbracket$ in which happens, they will always have the same value.  
そして、これが起こる時間 $t \in \llbracket T \rrbracket$ に関係なく、常に同じ値を持ちます。  

We refer to the minimum values the quantities above can get in $t \in \mathcal{F}_{i,\tau}^{\complement}$ as:  
上記の量が $t \in \mathcal{F}_{i,\tau}^{\complement}$ で得られる最小値を次のように呼びます：  

$$
\text{(48)}
$$  
$$
\text{(48)}
$$  

We choose $\omega = \frac{\ln(\tau)}{2(x_{i} - y_{i})^{2}}$ and define $\hat{\mu}_{i,t,\tau} = \frac{S_{i,t,\tau}}{N_{i,t,\tau}}$.  
$\omega = \frac{\ln(\tau)}{2(x_{i} - y_{i})^{2}}$ を選び、$\hat{\mu}_{i,t,\tau} = \frac{S_{i,t,\tau}}{N_{i,t,\tau}}$ を定義します。  

We will consider $\tau \geq e$.  
$\tau \geq e$ を考慮します。  

We first tackle Term $(\mathcal{S}.1)$.  
まず、項 $(\mathcal{S}.1)$ に取り組みます。  



#### Term (𝒮.1𝒮.1\mathcal{S}.1caligraphic_S .1) 

We have: 
私たちは次のことを持っています：

(49) 
(49)

(50) 
(50)

(51) 
(51)

First, we face term(𝒮.1.2)𝒮.1.2(\mathcal{S}.1.2)( caligraphic_S .1.2 ), for each summand in the sum holds the following: 
まず、term(𝒮.1.2)𝒮.1.2(\mathcal{S}.1.2)( caligraphic_S .1.2 )に直面します。和の各項は次のようになります：

(52) 
(52)

(53) 
(53)

(54) 
(54)

(55) 
(55)

(56) 
(56)

where the inequality from Equation (54) to Equation (55) follow from the Chernoff-Hoeffding inequality. 
ここで、式(54)から式(55)への不等式は、チェルノフ・ホフディング不等式に従います。

Summing over all the roundt𝑡titalic_t, we obtain(𝒮.1.2)≤Tτ𝒮.1.2𝑇𝜏(\mathcal{S}.1.2)\leq\frac{T}{\tau}( caligraphic_S .1.2 ) ≤ divide start_ARG italic_T end_ARG start_ARG italic_τ end_ARG 
すべてのroundt𝑡titalic_tを合計すると、(𝒮.1.2)≤Tτ𝒮.1.2𝑇𝜏(\mathcal{S}.1.2)\leq\frac{T}{\tau}( caligraphic_S .1.2 ) ≤ divide start_ARG italic_T end_ARG start_ARG italic_τ end_ARGが得られます。

We now focus on term(𝒮.1.1)𝒮.1.1(\mathcal{S}.1.1)( caligraphic_S .1.1 ). 
次に、term(𝒮.1.1)𝒮.1.1(\mathcal{S}.1.1)( caligraphic_S .1.1 )に焦点を当てます。

We want to assess if it is possible for condition(∗)(*)( ∗ )to happen, in order to do so evaluate the following: 
条件(∗)(*)( ∗ )が発生する可能性があるかどうかを評価したいので、次のことを評価します：

54 
54

55 
55

(57) 
(57)

(58) 
(58)

(59) 
(59)

(60) 
(60)

(61) 
(61)

(62) 
(62)

(63) 
(63)

where for the last inequality, we exploited the Pinsker inequality. 
最後の不等式では、ピンスカー不等式を利用しました。

Equation(59) was derived by exploiting the fact that on the eventxi,t≥μ^i,t,τsubscript𝑥𝑖𝑡subscript^𝜇𝑖𝑡𝜏x_{i,t}\geq\hat{\mu}_{i,t,\tau}italic_x start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPT ≥ over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT 
式(59)は、事象$x_{i,t}\geq\hat{\mu}_{i,t,\tau}$の事実を利用して導出されました。

a sample fromBeta(xi,tNi,t,τ+1,(1−xi,t)Ni,t,τ+1)Betasubscript𝑥𝑖𝑡subscript𝑁𝑖𝑡𝜏11subscript𝑥𝑖𝑡subscript𝑁𝑖𝑡𝜏1\text{Beta}\left(x_{i,t}N_{i,t,\tau}+1,(1-x_{i,t})N_{i,t,\tau}+1\right) 
$\text{Beta}\left(x_{i,t}N_{i,t,\tau}+1,(1-x_{i,t})N_{i,t,\tau}+1\right)$のサンプルは、

is likely to be as large as a sample fromBeta(μ^i,t,τNi,t,τ+1,(1−μ^i,t,τ)Ni,t,τ+1)Betasubscript^𝜇𝑖𝑡𝜏subscript𝑁𝑖𝑡𝜏11subscript^𝜇𝑖𝑡𝜏subscript𝑁𝑖𝑡𝜏1\text{Beta}(\hat{\mu}_{i,t,\tau}N_{i,t,\tau}+1,(1-\hat{\mu}_{i,t,\tau})N_{i,t,\tau}+1) 
$\text{Beta}(\hat{\mu}_{i,t,\tau}N_{i,t,\tau}+1,(1-\hat{\mu}_{i,t,\tau})N_{i,t,\tau}+1)$のサンプルと同じくらい大きくなる可能性があります。

reported formally in Lemma11. 
これは、補題11で正式に報告されています。

Equation (60) follows from Fact4, while Equation61from Lemma10 
式(60)はFact4から導かれ、式(61)は補題10から導かれます。

Therefore, forω=logτ2(yi−xi)2𝜔𝜏2superscriptsubscript𝑦𝑖subscript𝑥𝑖2\omega=\frac{\log{\tau}}{2(y_{i}-x_{i})^{2}}italic_ω = divide start_ARG roman_log italic_τ end_ARG start_ARG 2 ( italic_y start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT - italic_x start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ) start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG 
したがって、$\omega=\frac{\log{\tau}}{2(y_{i}-x_{i})^{2}}$となります。

we have: 
私たちは次のことを得ます：

59 
59

11 
11

60 
60

4 
4

61 
61

10 
10

(64) 
(64)

Then, it follows that condition(∗)(*)( ∗ )is never met, and each summand in(𝒮.1.1)𝒮.1.1(\mathcal{S}.1.1)( caligraphic_S .1.1 )is equal to zero, so(𝒮.1.1)=0𝒮.1.10(\mathcal{S}.1.1)=0( caligraphic_S .1.1 ) = 0. 
したがって、条件(∗)(*)( ∗ )は決して満たされず、(𝒮.1.1)𝒮.1.1(\mathcal{S}.1.1)( caligraphic_S .1.1 )の各項はゼロに等しくなるため、(𝒮.1.1)=0𝒮.1.10(\mathcal{S}.1.1)=0( caligraphic_S .1.1 ) = 0となります。



#### Term (𝒮.2𝒮.2\mathcal{S}.2caligraphic_S .2) 用語 (𝒮.2𝒮.2\mathcal{S}.2caligraphic_S .2)

We can rewrite the term (𝒮.2𝒮.2\mathcal{S}.2caligraphic_S .2) as follows: 
用語 (𝒮.2𝒮.2\mathcal{S}.2caligraphic_S .2) を次のように書き換えることができます：

(65) 
(65)

(66) 
(66)

Exploiting the fact that $\mathbb{E}[XY]=\mathbb{E}[X\mathbb{E}[Y\mid X]]$, we can rewrite both $(\mathcal{S}.2.1)$ and $(\mathcal{S}.2.2)$ as: 
$\mathbb{E}[XY]=\mathbb{E}[X\mathbb{E}[Y\mid X]]$ という事実を利用して、$(\mathcal{S}.2.1)$ と $(\mathcal{S}.2.2)$ の両方を次のように書き換えることができます：

(67) 
(67)

(68) 
(68)

Let us first tackle term $(\mathcal{S}.2.1)$: 
まず、用語 $(\mathcal{S}.2.1)$ に取り組みましょう：

(69) 
(69)

Taking inspiration from peeling-like arguments, let us decompose the event $\mathcal{C}_1$ in $\lceil\log(\tau)\rceil$ sub-events $\mathcal{C}_{1,j}$ for $j\geq 1$ defined as follow: 
剥がしのような議論からインスピレーションを得て、イベント $\mathcal{C}_1$ を $\lceil\log(\tau)\rceil$ の部分イベント $\mathcal{C}_{1,j}$ に分解しましょう。ここで $j\geq 1$ と定義します：

(70) 
(70)

with the convention: 
次のように定義します：

(71) 
(71)

notice that $\lceil\log(\tau)\rceil$ of such sub-events are enough as by definition $N_{i,t,\tau}\leq\tau$ holds. This yields to: 
このような部分イベントの $\lceil\log(\tau)\rceil$ は十分であり、定義により $N_{i,t,\tau}\leq\tau$ が成り立ちます。これにより次のようになります：

(72) 
(72)

Let $\Delta_{i}^{\prime}\coloneqq\mu_{i^{*},\mathcal{F}_{\tau}^{\complement}}-y_{i}$, we can rewrite term $(\mathcal{S}.2.1)$ as: 
$\Delta_{i}^{\prime}\coloneqq\mu_{i^{*},\mathcal{F}_{\tau}^{\complement}}-y_{i}$ とし、用語 $(\mathcal{S}.2.1)$ を次のように書き換えることができます：

(73) 
(73)

(74) 
(74)

notice that, for each $j$, the only summands that will contribute to the sum will be those for which condition $\mathcal{C}_{1,j}$ holds true. Thus, for each $j$, the following will hold: 
各 $j$ に対して、合計に寄与する唯一の項は条件 $\mathcal{C}_{1,j}$ が成り立つものであることに注意してください。したがって、各 $j$ に対して、次のことが成り立ちます：

(75) 
(75)

We are now interested in evaluating $(*)$ for each $j$. For this purpose we rewrite it as: 
次に、各 $j$ に対して $(*)$ を評価することに興味があります。この目的のために、次のように書き換えます：

(76) 
(76)

where the expected value $\mathbb{E}_{N_{j}^{\prime},\ \underline{\mu}_{i^{*}(t)}}[\cdot]$ is taken over all the values of $N_{j-1}<N_{j}^{\prime}\leq N_{j}$ and over all different histories $\underline{\mu}_{i^{*}(t)}$ that yield to $N_{j}^{\prime}$ trials, with $\underline{\mu}_{i^{*}(t)}$ being the set of the $N_{j}^{\prime}$ probabilities of success of every trial of the best arm that make $\mathcal{C}_{1,j}$ true. 
期待値 $\mathbb{E}_{N_{j}^{\prime},\ \underline{\mu}_{i^{*}(t)}}[\cdot]$ は、$N_{j-1}<N_{j}^{\prime}\leq N_{j}$ のすべての値と、$\mathcal{C}_{1,j}$ を真にする最良のアームのすべての試行の成功確率の $N_{j}^{\prime}$ の集合である $\underline{\mu}_{i^{*}(t)}$ のすべての異なる履歴にわたって取られます。

(77) 
(77)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(78) 
(78)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(79) 
(79)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(80) 
(80)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(81) 
(81)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(82) 
(82)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(83) 
(83)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(84) 
(84)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(85) 
(85)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(86) 
(86)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(87) 
(87)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(88) 
(88)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(89) 
(89)

In order to bound these terms, we remember that $p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$. 
これらの項を制約するために、$p_{i^{*}(t),t,\tau}^{i}=\mathbb{P}(Beta(S_{i^{*}(t),t,\tau}+1,F_{i^{*}(t),t,\tau}+1)>y_{i,t}|\mathcal{F}_{t-1})=F^{B}_{N_{j}^{\prime}+1,y_{i,t}}(S_{i^{*}(t),t,\tau})$ を思い出します。

(90) 
(90)

The inequality from Equation (88) to Equation (89) follows again from Lemma 8, while the last inequality is derived by the fact that by definition $N_{j}/N_{j-1}=e$. 
式 (88) から式 (89) への不等式は再び補題 8 から導かれ、最後の不等式は定義により $N_{j}/N_{j-1}=e$ であることから導かれます。

(91) 
(91)

We tackle now term $(\mathcal{S}.2.2)$, making the same consideration that we have done from Equation (75), we infer that the only terms that will contribute to the summands are those for which condition $\mathcal{C}_{2}$ holds true, formally: 
次に、用語 $(\mathcal{S}.2.2)$ に取り組み、式 (75) で行ったのと同じ考察を行うと、合計に寄与する唯一の項は条件 $\mathcal{C}_{2}$ が成り立つものであることがわかります。形式的には：

(92) 
(92)

Again, by using Lemma 9 we can bound term $(*)$ with the bounds provided in Lemma 4 for the stationary bandit with expected reward for the best arm equal to $\mu_{i^{*}}^{\prime}$, defined as above. 
再び、補題 9 を使用することで、最良のアームの期待報酬が上記のように定義された $\mu_{i^{*}}^{\prime}$ に等しい定常バンディットのための補題 4 で提供された制約を用いて、項 $(*)$ を制約することができます。

(93) 
(93)

where, from Equation (94) to Equation (95) we used the Pinsker’s Inequality, namely: $D_{i,t}\geq 2\Delta_{i}^{\prime\prime 2}$. 
ここで、式 (94) から式 (95) への不等式はピンスカーの不等式を使用しました。すなわち、$D_{i,t}\geq 2\Delta_{i}^{\prime\prime 2}$ です。

(94) 
(94)

Then, summing over all rounds we get $(\mathcal{S}.2.2)\leq\frac{T}{\tau}$. 
次に、すべてのラウンドを合計すると、$(\mathcal{S}.2.2)\leq\frac{T}{\tau}$ となります。

(95) 
(95)

The result of the statement follows by summing all the terms, remembering that by definition $\Delta_{i}^{\prime}=\frac{\Delta_{\tau}}{3}$. 
この結果は、すべての項を合計することによって得られ、定義により $\Delta_{i}^{\prime}=\frac{\Delta_{\tau}}{3}$ であることを思い出します。

(96) 
(96)

∎ 
∎

See V.2 
V.2 を参照してください

We recall Lemma 2: 
補題 2 を思い出します：

(97) 
(97)

Let us define $x_{i,t}$ and $y_{i,t}$ for $t\in\mathcal{F}_{i,\tau}^{\complement}$ as: 
$ t\in\mathcal{F}_{i,\tau}^{\complement}$ のとき、$x_{i,t}$ と $y_{i,t}$ を次のように定義します：

(98) 
(98)

with $\Delta_{i,t,\tau}=\min_{t^{\prime}\in\llbracket t-\tau,t-1\rrbracket}\{\mu_{i^{*}(t),t^{\prime}}\}-\max_{t^{\prime}\in\llbracket t-\tau,t-1\rrbracket}\{\mu_{i(t),t^{\prime}}\}$. 
$\Delta_{i,t,\tau}=\min_{t^{\prime}\in\llbracket t-\tau,t-1\rrbracket}\{\mu_{i^{*}(t),t^{\prime}}\}-\max_{t^{\prime}\in\llbracket t-\tau,t-1\rrbracket}\{\mu_{i(t),t^{\prime}}\}$ です。

(99) 
(99)

Notice then that the following quantities will have their minima for those $t\in\mathcal{F}_{i,\tau}^{\complement}$ such that $\Delta_{i,t,\tau}=\Delta_{\tau}$. 
したがって、次の量は、$\Delta_{i,t,\tau}=\Delta_{\tau}$ となる $t\in\mathcal{F}_{i,\tau}^{\complement}$ に対して最小値を持つことに注意してください。

(100) 
(100)

and independently from the time $t\in\llbracket T\rrbracket$ in which happens, they will always have the same value. 
そして、発生する時間 $t\in\llbracket T\rrbracket$ に依存せず、常に同じ値を持ちます。

(101) 
(101)

We refer to the minimum values the quantities above can get in $t\in\mathcal{F}_{\tau}^{\complement}$ as: 
上記の量が $t\in\mathcal{F}_{\tau}^{\complement}$ で得られる最小値を次のように呼びます：

(102) 
(102)

We choose $\omega=\frac{288\log(\tau\Delta_{\tau}^{2}+e^{6})}{\gamma\Delta_{\tau}^{2}}$, $\epsilon_{i}=\Delta_{\tau}^{2}$, $\tau\geq e$ and $\hat{\mu}_{i,t,\tau}=\frac{S_{i,t,\tau}}{N_{i,t,\tau}}$. 
$\omega=\frac{288\log(\tau\Delta_{\tau}^{2}+e^{6})}{\gamma\Delta_{\tau}^{2}}$、$\epsilon_{i}=\Delta_{\tau}^{2}$、$\tau\geq e$ および $\hat{\mu}_{i,t,\tau}=\frac{S_{i,t,\tau}}{N_{i,t,\tau}}$ を選びます。

(103) 
(103)



#### Term (𝒮.1𝒮.1\mathcal{S}.1caligraphic_S .1) 用語 (𝒮.1)

Decomposing the term in two contributions, we obtain:
項を二つの寄与に分解すると、次のようになります：

(100)  
(100)

(101)  
(101)

(102)  
(102)

We first tackle term(𝒮.1.2)𝒮.1.2(\mathcal{S}.1.2)( caligraphic_S .1.2 ), considering each summand we get:
まず、項(𝒮.1.2)𝒮.1.2(\mathcal{S}.1.2)( caligraphic_S .1.2 )に取り組み、各和項を考慮すると、次のようになります：

(103)  
(103)

(104)  
(104)

(105)  
(105)

(106)  
(106)

(107)  
(107)

Where the inequality from Equation (104) to Equation (105) follows from the Chernoff bounds for subgaussian random variables, reported formally in Lemma7.
式(104)から式(105)への不等式は、レマ7で正式に報告されたサブガウス過程の確率変数に対するチェルノフ境界に基づいています。

Facing term(𝒮.2.1)𝒮.2.1(\mathcal{S}.2.1)( caligraphic_S .2.1 ), we want to evaluate if ever condition(∗)(*)( ∗ )is met.
項(𝒮.2.1)𝒮.2.1(\mathcal{S}.2.1)( caligraphic_S .2.1 )に直面し、条件(∗)(*)( ∗ )が満たされるかどうかを評価したいと思います。

In order to do so let us consider:
そのために、次のことを考えましょう：

(108)  
(108)

where the inequality in Equation (108) follows from Lemma11.
式(108)の不等式は、レマ11に基づいています。

Using Lemma6:
レマ6を使用すると：

(109)  
(109)

(110)  
(110)

which is smaller than $ \frac{1}{\tau\Delta_{\tau}^{2}} $ because $ \omega \geq \frac{2\ln\left(\tau\Delta_{\tau}^{2}\right)}{\gamma\left(y_{i}-x_{i}\right)^{2}} $.
これは $ \frac{1}{\tau\Delta_{\tau}^{2}} $ より小さく、$ \omega \geq \frac{2\ln\left(\tau\Delta_{\tau}^{2}\right)}{\gamma\left(y_{i}-x_{i}\right)^{2}} $ です。

Substituting, we get:
代入すると、次のようになります：

(111)  
(111)

So that condition(∗)(*)( ∗ )is never met and $ \mathcal{S}.1.1=0 $.
したがって、条件(∗)(*)( ∗ )は決して満たされず、$ \mathcal{S}.1.1=0 $ となります。



#### Term (𝒮.2𝒮.2\mathcal{S}.2caligraphic_S .2)
We decompose it as:
(112)
項(𝒮.2.1)𝒮.2.1(\mathcal{S}.2.1)( caligraphic_S .2.1 )を考えます。私たちは、Beta-TSの証明で行ったように、形式的に項を書き直します。
(112)
Let us face term(𝒮.2.1)𝒮.2.1(\mathcal{S}.2.1)( caligraphic_S .2.1 ). We rewrite the term, similarly to what we have done for the Beta-TS proof, formally:
Beta-TS
(113)
Let us evaluate what happens when 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 holds true, i.e., those cases in which the summands within the summation in Equation (112) are different from zero.
(113)
𝒞1𝒞1\mathcal{C}1caligraphic_C 1 が真であるとき、すなわち式(112)の合計内の項がゼロでない場合に何が起こるかを評価します。
We will show that whenever condition 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 holds true (∗)(*)( ∗ ) is bounded by a constant.
私たちは、条件 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 が真であるとき、(∗)(*)( ∗ ) が定数で制約されることを示します。
We will show that for any realization of the number of pulls within a time window τ𝜏\tauitalic_τ such that condition 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 holds true (i.e. number of pulls j𝑗jitalic_j of the optimal arm within the time window less than ω𝜔\omegaitalic_ω) the expected value of G_j G_{j}italic_G start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT is bounded by a constant for all j𝑗jitalic_j defined as earlier.
私たちは、条件 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 が真であるような時間ウィンドウ τ𝜏\tauitalic_τ 内の引きの数の任意の実現に対して、最適なアームの引きの数 j𝑗jitalic_j が ω𝜔\omegaitalic_ω より少ない場合、すべての j𝑗jitalic_j に対して G_j G_{j}italic_G start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT の期待値が定数で制約されることを示します。
Let Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT denote a 𝒩(μ^i∗(t),j,1/γ_j) 𝒩subscript^𝜇superscript𝑖𝑡𝑗1𝛾𝑗\mathcal{N}\left({\hat{\mu}}_{i^{*}(t),j},\frac{1}{\gamma j}\right)caligraphic_N ( over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT , divide start_ARG 1 end_ARG start_ARG italic_γ italic_j end_ARG ) distributed Gaussian random variable, where μ^i∗(t),j subscript^𝜇superscript𝑖𝑡𝑗{\hat{\mu}}_{i^{*}(t),j} over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT is the sample mean of the optimal arm’s rewards played j𝑗jitalic_j times within a time window τ𝜏\tauitalic_τ at time t∈ℱi,τ∁𝑡 superscriptsubscriptℱ𝑖𝜏complement t∈\mathcal{F}_{i,\tau}^{\complement}italic_t ∈ caligraphic_F start_POSTSUBSCRIPT italic_i , italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT.
Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT を 𝒩(μ^i∗(t),j,1/γ_j) 𝒩subscript^𝜇superscript𝑖𝑡𝑗1𝛾𝑗\mathcal{N}\left({\hat{\mu}}_{i^{*}(t),j},\frac{1}{\gamma j}\right)caligraphic_N ( over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT , divide start_ARG 1 end_ARG start_ARG italic_γ italic_j end_ARG ) で分布するガウスランダム変数とし、μ^i∗(t),j subscript^𝜇superscript𝑖𝑡𝑗{\hat{\mu}}_{i^{*}(t),j} over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT を時間ウィンドウ τ𝜏\tauitalic_τ 内で j𝑗jitalic_j 回プレイされた最適アームの報酬のサンプル平均とします。
Let G_j G_{j}italic_G start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT be the geometric random variable denoting the number of consecutive independent trials until and including the trial where a sample of Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT becomes greater than y_{i,t} y_{i,t}italic_y start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPT.
G_j G_{j}italic_G start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT を、Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT のサンプルが y_{i,t} y_{i,t}italic_y start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPT より大きくなるまでの連続した独立試行の回数を示す幾何学的ランダム変数とします。
Consider now an arbitrary realization where the best arm has been played j𝑗jitalic_j times and with sample expected rewards 𝔼[μ^i∗(t),j] 𝔼delimited-[]subscript^𝜇superscript𝑖𝑡𝑗\mathbb{E}[{\hat{\mu}}_{i^{*}(t),j}] blackboard_E [ over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT ], respecting condition 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 then observe that p_{i^{*}(t),t,\tau} = \operatorname{Pr}\left(\Theta_{j}>y_{i,t}\mid\mathbb{F}_{\tau_{j}}\right) italic_p start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_t , italic_τ end_POSTSUBSCRIPT = roman_Pr ( roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT > italic_y start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPT ∣ blackboard_F start_POSTSUBSCRIPT italic_τ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT end_POSTSUBSCRIPT ) and:
Consider now an arbitrary realization where the best arm has been played j𝑗jitalic_j times and with sample expected rewards 𝔼[μ^i∗(t),j] 𝔼delimited-[]subscript^𝜇superscript𝑖𝑡𝑗\mathbb{E}[{\hat{\mu}}_{i^{*}(t),j}] blackboard_E [ over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT ], respecting condition 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 then observe that p_{i^{*}(t),t,\tau} = \operatorname{Pr}\left(\Theta_{j}>y_{i,t}\mid\mathbb{F}_{\tau_{j}}\right) italic_p start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUBSCRIPT ( italic_t ) , italic_t , italic_τ end_POSTSUBSCRIPT = roman_Pr ( roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT > italic_y start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPT ∣ blackboard_F start_POSTSUBSCRIPT italic_τ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT end_POSTSUBSCRIPT ) and:
112
(114)
where by 𝔼_{j\mid\mathcal{C}1}[\cdot] blackboard_E start_POSTSUBSCRIPT italic_j ∣ caligraphic_C 1 end_POSTSUBSCRIPT [ ⋅ ] we denote the expected value taken over every j𝑗jitalic_j (and every possible 𝔼[μ^i∗(t),j] 𝔼delimited-[]subscript^𝜇superscript𝑖𝑡𝑗\mathbb{E}[{\hat{\mu}}_{i^{*}(t),j}] blackboard_E [ over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT ] compatible with j𝑗jitalic_j pulls) respecting condition 𝒞1𝒞1\mathcal{C}1caligraphic_C 1.
ここで、𝔼_{j\mid\mathcal{C}1}[\cdot] blackboard_E start_POSTSUBSCRIPT italic_j ∣ caligraphic_C 1 end_POSTSUBSCRIPT [ ⋅ ] は、すべての j𝑗jitalic_j (および j𝑗jitalic_j 引きに対応するすべての可能な 𝔼[μ^i∗(t),j] 𝔼delimited-[]subscript^𝜇superscript𝑖𝑡𝑗\mathbb{E}[{\hat{\mu}}_{i^{*}(t),j}] blackboard_E [ over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT ] を含む) に対して、条件 𝒞1𝒞1\mathcal{C}1caligraphic_C 1 を尊重して期待値を示します。
Consider any integer r≥1 𝑟1r\geq 1 italic_r ≥ 1. Let z=lnr 𝑧𝑟 z=\sqrt{\ln r} italic_z = square-root start_ARG roman_ln italic_r end_ARG and let random variable MAX_r denote the maximum of r 𝑟ritalic_r independent samples of Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT.
任意の整数 r≥1 𝑟1r\geq 1 italic_r ≥ 1 を考えます。z=lnr 𝑧𝑟 z=\sqrt{\ln r} italic_z = square-root start_ARG roman_ln italic_r end_ARG とし、ランダム変数 MAX_r を Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT の r 𝑟ritalic_r 独立サンプルの最大値とします。
We abbreviate μ^i∗(t),j subscript^𝜇superscript𝑖𝑡𝑗{\hat{\mu}}_{i^{*}(t),j} over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT to μ^i∗ subscript^𝜇superscript𝑖{\hat{\mu}}_{i^{*}} over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT end_POSTSUBSCRIPT and we will abbreviate min_{t^{\prime}\in\llbracket t-\tau,t-1\rrbracket}\{\mu_{i^{*}(t),t^{\prime}}\} roman_min start_POSTSUBSCRIPT italic_t start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ∈ ⟦ italic_t - italic_τ , italic_t - 1 ⟧ end_POSTSUBSCRIPT { italic_μ start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_t start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT end_POSTSUBSCRIPT } as μ_{i^{*}} italic_μ start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUBSCRIPT in the following.
私たちは μ^i∗(t),j subscript^𝜇superscript𝑖𝑡𝑗{\hat{\mu}}_{i^{*}(t),j} over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_j end_POSTSUBSCRIPT を μ^i∗ subscript^𝜇superscript𝑖{\hat{\mu}}_{i^{*}} over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT end_POSTSUBSCRIPT と略し、次に min_{t^{\prime}\in\llbracket t-\tau,t-1\rrbracket}\{\mu_{i^{*}(t),t^{\prime}}\} roman_min start_POSTSUBSCRIPT italic_t start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ∈ ⟦ italic_t - italic_τ , italic_t - 1 ⟧ end_POSTSUBSCRIPT { italic_μ start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) , italic_t start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT end_POSTSUBSCRIPT } を μ_{i^{*}} italic_μ start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUBSCRIPT と略します。
Then for any integer r≥1 𝑟1r\geq 1 italic_r ≥ 1:
(138)
(139)
(140)
(141)
where we used that y_{i,t} = μ_{i^{*}} - \frac{\Delta_{i,t,\tau}}{3} italic_y start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPT = italic_μ start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUBSCRIPT - divide start_ARG roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT end_ARG start_ARG 3 end_ARG.
その後、任意の整数 r≥1 𝑟1r\geq 1 italic_r ≥ 1 に対して:
(138)
(139)
(140)
(141)
ここで、y_{i,t} = μ_{i^{*}} - \frac{\Delta_{i,t,\tau}}{3} italic_y start_POSTSUBSCRIPT italic_i , italic_t end_POSTSUBSCRIPT = italic_μ start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUBSCRIPT - divide start_ARG roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT end_ARG start_ARG 3 end_ARG を使用しました。
Now, since j≥ω=288\ln(τΔτ^2+e^6) \gamma Δτ^2 ≥ 288\ln(τΔ_{i,t,\tau}^2+e^6) \gamma(Δ_{i,t,\tau})^2 𝑗𝜔288𝜏superscriptsubscriptΔ𝜏^2superscript𝑒^6𝛾superscriptsubscriptΔ𝜏^2 j\geq\omega=\frac{288\ln\left(\tau\Delta_{\tau}^{2}+e^{6}\right)}{\gamma\Delta_{\tau}^{2}}\geq\frac{288\ln\left(\tau\Delta_{i,t,\tau}^{2}+e^{6}\right)}{\gamma(\Delta_{i,t,\tau})^{2}} italic_j ≥ italic_ω = divide start_ARG 288 roman_ln ( italic_τ roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT + italic_e start_POSTSUPERSCRIPT 6 end_POSTSUPERSCRIPT ) end_ARG start_ARG italic_γ roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG ≥ divide start_ARG 288 roman_ln ( italic_τ roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT + italic_e start_POSTSUPERSCRIPT 6 end_POSTSUPERSCRIPT ) end_ARG start_ARG italic_γ ( roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT ) start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG for t∈ℱτ 𝑡subscriptℱ𝜏 t∈\mathcal{F}_{\tau} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT, as Δ_{i,t,\tau} ≥ Δ_{\tau} roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT ≥ roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT, we have that:
Now, since j≥ω=288\ln(τΔτ^2+e^6) \gamma Δτ^2 ≥ 288\ln(τΔ_{i,t,\tau}^2+e^6) \gamma(Δ_{i,t,\tau})^2 𝑗𝜔288𝜏superscriptsubscriptΔ𝜏^2superscript𝑒^6𝛾superscriptsubscriptΔ𝜏^2 j\geq\omega=\frac{288\ln\left(\tau\Delta_{\tau}^{2}+e^{6}\right)}{\gamma\Delta_{\tau}^{2}}\geq\frac{288\ln\left(\tau\Delta_{i,t,\tau}^{2}+e^{6}\right)}{\gamma(\Delta_{i,t,\tau})^{2}} italic_j ≥ italic_ω = divide start_ARG 288 roman_ln ( italic_τ roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT + italic_e start_POSTSUPERSCRIPT 6 end_POSTSUPERSCRIPT ) end_ARG start_ARG italic_γ roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG ≥ divide start_ARG 288 roman_ln ( italic_τ roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT + italic_e start_POSTSUPERSCRIPT 6 end_POSTSUPERSCRIPT ) end_ARG start_ARG italic_γ ( roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT ) start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG for t∈ℱτ 𝑡subscriptℱ𝜏 t∈\mathcal{F}_{\tau} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT, as Δ_{i,t,\tau} ≥ Δ_{\tau} roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT ≥ roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT, we have that:
(142)
Therefore, for r≤(τΔ_{i,t,\tau}^2+e^6)^2 𝑟superscriptsubscriptΔ𝑖𝑡𝜏2superscript𝑒^62r\leq\left(\tau\Delta_{i,t,\tau}^{2}+e^{6}\right)^{2} italic_r ≤ ( italic_τ roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT + italic_e start_POSTSUPERSCRIPT 6 end_POSTSUPERSCRIPT ) start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT:
(143)
Then, since Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT is 𝒩(μ^i∗,j,1/γ_j) 𝒩subscript^𝜇superscript𝑖𝑗1𝛾𝑗\mathcal{N}\left({\hat{\mu}}_{i^{*},j},\frac{1}{\gamma j}\right) caligraphic_N ( over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT , italic_j end_POSTSUBSCRIPT , divide start_ARG 1 end_ARG start_ARG italic_γ italic_j end_ARG ) distributed random variable, using the upper bound in Lemma 6, we obtain for any instantiation F_{τ_j} of history 𝔽_{τ_j} \mathbb{F}_{\tau_{j}} blackboard_F start_POSTSUBSCRIPT italic_τ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT end_POSTSUBSCRIPT,
(144)
Then, since Θ_j \Theta_{j}roman_Θ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT is 𝒩(μ^i∗,j,1/γ_j) 𝒩subscript^𝜇superscript𝑖𝑗1𝛾𝑗\mathcal{N}\left({\hat{\mu}}_{i^{*},j},\frac{1}{\gamma j}\right) caligraphic_N ( over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT , italic_j end_POSTSUBSCRIPT , divide start_ARG 1 end_ARG start_ARG italic_γ italic_j end_ARG ) distributed random variable, using the upper bound in Lemma 6, we obtain for any instantiation F_{τ_j} of history 𝔽_{τ_j} \mathbb{F}_{\tau_{j}} blackboard_F start_POSTSUBSCRIPT italic_τ start_POSTSUBSCRIPT italic_j end_POSTSUBSCRIPT end_POSTSUBSCRIPT,
(144)
being j≥ω 𝑗𝜔 j\geq\omega italic_j ≥ italic_ω. This implies:
(145)
また、任意の t 𝑡 t italic_t について条件 𝒞2𝒞2\mathcal{C}2caligraphic_C 2 が真である場合、j≥ω 𝑗𝜔 j\geq\omega italic_j ≥ italic_ω となり、7 を使用すると次のようになります。
(146)
(147)
where the last inequality of Equation (146) follows from the fact that:
(148)
(149)
(150)
where the last inequality follows as by definition, we will always have that μ_{i^{*}} - \mathbb{E}[{\hat{\mu}}_{i^{*}}] \leq 0 italic_μ start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUBSCRIPT - blackboard_E [ over^ start_ARG italic_μ end_ARG start_POSTSUBSCRIPT italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ] ≤ 0.
(151)
Let T'=(τΔ_{i,t,\tau}^2+e^6)^2 𝑇^{\prime}=\left(\tau\Delta_{i,t,\tau}^{2}+e^{6}\right)^{2} italic_T start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT = ( italic_τ roman_Δ start_POSTSUBSCRIPT italic_i , italic_t , italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT + italic_e start_POSTSUPERSCRIPT 6 end_POSTSUPERSCRIPT ) start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT.
(151)
したがって、1≤r≤T' 1 𝑟superscriptsubscript𝑇′ 1\leq r\leq T^{\prime} 1 ≤ italic_r ≤ italic_T start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
(152)
When r≥T'≥e^{12} 𝑟superscript𝑇′superscript𝑒^{12} r\geq T^{\prime}\geq e^{12} italic_r ≥ italic_T start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ≥ italic_e start_POSTSUPERSCRIPT 12 end_POSTSUPERSCRIPT, we obtain:
(153)
すべての境界を組み合わせると、私たちは j 𝑗 jitalic_j に依存しない境界を導出しました:
(154)
(155)
(156)
(157)
So that:
(158)
The statement follows by summing all the terms.
この主張は、すべての項を合計することによって導かれます。
∎
See VI.1
VI.1
The proof follows by defining ℱτ subscript ℱ𝜏 \mathcal{F}_{\tau} caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT as the set of times of length τ𝜏\tau italic_τ after every breakpoint, and noticing that by definition of the general abruptly changing setting, we have for any t∈ℱτ∁ 𝑡 subscript ℱ𝜏 complement t∈\mathcal{F}_{\tau}^{\complement} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT, as we have demonstrated in the main paper, that:
∎
See VI.2
VI.2
The proof, yet again, follows by defining ℱτ subscript ℱ𝜏 \mathcal{F}_{\tau} caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT as the set of times of length τ𝜏\tau italic_τ after every breakpoint, and noticing that by definition of the general abruptly changing setting we have for any t∈ℱτ∁ 𝑡 subscript ℱ𝜏 complement t∈\mathcal{F}_{\tau}^{\complement} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT, as we have demonstrated in the main paper, that:
∎
See VII.1
VII.1
To derive the bound, we will assign "error" equal to one for every t∈ℱΔ′,T 𝑡 subscript ℱ superscript Δ′ 𝑇 t∈\mathcal{F}_{\Delta^{\prime},T} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT , italic_T end_POSTSUBSCRIPT and we will study what happens in ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT.
境界を導出するために、私たちは t∈ℱΔ′,T 𝑡 subscript ℱ superscript Δ′ 𝑇 t∈\mathcal{F}_{\Delta^{\prime},T} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT のすべてに対して "error" を1に設定します。そして、ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT で何が起こるかを調べます。
Notice that by definition of ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT we will have that ∀i≠i∗(t) for-all 𝑖 superscript 𝑖 𝑡 ∀ i\neq i^{*}(t) ∀ italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ):
ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT の定義により、∀i≠i∗(t) for-all 𝑖 superscript 𝑖 𝑡 ∀ i\neq i^{*}(t) ∀ italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) が成り立ちます。
Using the Lipschitz assumption we can infer that for i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ):
リプシッツ仮定を使用すると、i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) に対して推測できます。
and, similarly, by making use of the Lipscithz assumption, we obtain, for i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ):
同様に、リプシッツ仮定を使用することで、i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) に対して得られます。
Substituting we obtain:
置き換えることで得られます:
so that due to the introduced assumptions, we have:
導入された仮定により、次のようになります:
Notice that is the assumption for the general theorem, so we will have that ℱΔ′,T∁ = ℱτ∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement superscriptsubscript ℱ𝜏 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement}=\mathcal{F}_{\tau}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT = caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT, this yields to the desired result noticing that by definition Δτ=Δ′−2στ subscript Δ𝜏 superscript Δ′ 2 𝜎 𝜏 \Delta_{\tau}=\Delta^{\prime}-2\sigma\tau roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT = roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT - 2 italic_σ italic_τ.
注意すべきは、これは一般定理の仮定であるため、ℱΔ′,T∁=ℱτ∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement superscriptsubscript ℱ𝜏 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement}=\mathcal{F}_{\tau}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT = caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT となり、定義により Δτ=Δ′−2στ subscript Δ𝜏 superscript Δ′ 2 𝜎 𝜏 \Delta_{\tau}=\Delta^{\prime}-2\sigma\tau roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT = roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT - 2 italic_σ italic_τ となります。
∎
See VII.2
VII.2
In order to derive the bound we will assign "error" equal to one for every t∈ℱΔ′,T 𝑡 subscript ℱ superscript Δ′ 𝑇 t∈\mathcal{F}_{\Delta^{\prime},T} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT and we will study what happens in ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT, i.e. the set of times t∈⟦T⟧ t∈\llbracket T\rrbracket italic_t ∈ ⟦ italic_T ⟧ such that t∉ℱΔ′,T 𝑡 subscript ℱ superscript Δ′ 𝑇 t\notin\mathcal{F}_{\Delta^{\prime},T} italic_t ∉ caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT.
境界を導出するために、私たちは t∈ℱΔ′,T 𝑡 subscript ℱ superscript Δ′ 𝑇 t∈\mathcal{F}_{\Delta^{\prime},T} italic_t ∈ caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT のすべてに対して "error" を1に設定します。そして、ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT で何が起こるかを調べます。すなわち、t∈⟦T⟧ t∈\llbracket T\rrbracket italic_t ∈ ⟦ italic_T ⟧ で t∉ℱΔ′,T 𝑡 subscript ℱ superscript Δ′ 𝑇 t\notin\mathcal{F}_{\Delta^{\prime},T} italic_t ∉ caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT となる時間の集合です。
Notice that by definition of ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT we will have that ∀i≠i∗(t) for-all 𝑖 superscript 𝑖 𝑡 ∀ i\neq i^{*}(t) ∀ italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ):
ℱΔ′,T∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT の定義により、∀i≠i∗(t) for-all 𝑖 superscript 𝑖 𝑡 ∀ i\neq i^{*}(t) ∀ italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) が成り立ちます。
Using the Lipschitz assumption, we can infer that for i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ):
リプシッツ仮定を使用すると、i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) に対して推測できます。
and, similarly, by making use of the Lipschitz assumption, we obtain, for i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ):
同様に、リプシッツ仮定を使用することで、i≠i∗(t) 𝑖 superscript 𝑖 𝑡 i\neq i^{*}(t) italic_i ≠ italic_i start_POSTSUPERSCRIPT ∗ end_POSTSUPERSCRIPT ( italic_t ) に対して得られます。
Substituting we obtain:
置き換えることで得られます:
so that due to the introduced assumptions, we have:
導入された仮定により、次のようになります:
Notice that is the assumption for the general theorem, so we will have that ℱΔ′,T∁ = ℱτ∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement superscriptsubscript ℱ𝜏 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement}=\mathcal{F}_{\tau}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT = caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT, this yields to the desired result noticing that by definition Δτ=Δ′−2στ subscript Δ𝜏 superscript Δ′ 2 𝜎 𝜏 \Delta_{\tau}=\Delta^{\prime}-2\sigma\tau roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT = roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT - 2 italic_σ italic_τ.
注意すべきは、これは一般定理の仮定であるため、ℱΔ′,T∁=ℱτ∁ superscriptsubscript ℱ superscriptsubscript Δ′ 𝑇 complement superscriptsubscript ℱ𝜏 complement \mathcal{F}_{\Delta^{\prime},T}^{\complement}=\mathcal{F}_{\tau}^{\complement} caligraphic_F start_POSTSUBSCRIPT roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUBSCRIPT , italic_T end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT = caligraphic_F start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ∁ end_POSTSUPERSCRIPT となり、定義により Δτ=Δ′−2στ subscript Δ𝜏 superscript Δ′ 2 𝜎 𝜏 \Delta_{\tau}=\Delta^{\prime}-2\sigma\tau roman_Δ start_POSTSUBSCRIPT italic_τ end_POSTSUBSCRIPT = roman_Δ start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT - 2 italic_σ italic_τ.
∎



## Appendix CExperimental details 付録C 実験の詳細

Appendix C 付録C



### Parameters パラメータ

The choices of the parameters of the algorithms we compared R-less/ed-UCB with are the following:
私たちが比較したR-less/ed-UCBアルゴリズムのパラメータの選択は以下の通りです。

R-less/ed-UCB
R-less/ed-UCB
- • Rexp3: $\gamma=\min\left\{1,\sqrt{\frac{K\log{K}}{(e-1)\Delta_{T}}}\right\}$, $\Delta_{T}=\lceil(K\log{K})^{1/3}(T/V_{T})^{2/3}\rceil$ as recommended by Besbes et al. [10];
- • Rexp3: $\gamma=\min\left\{1,\sqrt{\frac{K\log{K}}{(e-1)\Delta_{T}}}\right\}$（$\gamma=\min\{1,\sqrt{\frac{K\log{K}}{(e-1)\Delta_{T}}}\}$）、$\Delta_{T}=\lceil(K\log{K})^{1/3}(T/V_{T})^{2/3}\rceil$（$\Delta_{T}=\lceil(K\log{K})^{1/3}(T/V_{T})^{2/3}\rceil$）は、Besbes et al. [10]によって推奨されています。

- • KL-UCB: $c=3$ as required by the theoretical results on the regret provided by Garivier and Cappé [22];
- • KL-UCB: $c=3$（$c=3$）は、GarivierとCappé [22]によって提供された後悔に関する理論的結果に基づいています。

- • Ser4: according to what suggested by Allesiardo et al. [6] we selected $\delta=1/T$, $\epsilon=\frac{1}{KT}$, and $\phi=\sqrt{\frac{N}{TK\log({KT})}}$;
- • Ser4: Allesiardo et al. [6]の提案に従い、$\delta=1/T$（$\delta=1/T$）、$\epsilon=\frac{1}{KT}$（$\epsilon=\frac{1}{KT}$）、および$\phi=\sqrt{\frac{N}{TK\log({KT})}}$（$\phi=\sqrt{\frac{N}{TK\log({KT})}}$）を選択しました。

- • SW-UCB: as suggested by Garivier and Moulines [23] we selected the sliding-window $\tau=4\sqrt{T\log{T}}$ and the constant $\xi=0.6$;
- • SW-UCB: GarivierとMoulines [23]の提案に従い、スライディングウィンドウ$\tau=4\sqrt{T\log{T}}$（$\tau=4\sqrt{T\log{T}}$）と定数$\xi=0.6$（$\xi=0.6$）を選択しました。

- • SW-KL-UCB as suggested by Garivier and Moulines [24] we selected the sliding-window $\tau=\sigma^{-4/5}$;
- • SW-KL-UCB: GarivierとMoulines [24]の提案に従い、スライディングウィンドウ$\tau=\sigma^{-4/5}$（$\tau=\sigma^{-4/5}$）を選択しました。



### Equations for the Abruptly Changing Environment 環境が急激に変化するための方程式

(159)  
(159)

(160)  
(160)



### Equations for the Smoothly Changing Environment 滑らかに変化する環境のための方程式

(161)
(161)



### Smoothly Changing Experiment for $\sigma=0.001$

The environment is illustrated in Figure 6a. 
環境は図6aに示されています。

The cumulative regret is depicted in Figure 6b, 
累積後悔は図6bに示されています。

while the sensitivity analysis is represented in Figure 6c. 
感度分析は図6cに示されています。

6a  
6b  
6c  
(a)  
(b)  
(c)  

Figure 6:  
図6：



## Appendix D Trovò et al. [48] の論文からの誤り

Appendix D  
この付録では、Trovò et al. [48] で見つかった技術的な誤りを報告します。  
In this appendix, we report the technical error found in Trovò et al. [48].

Rewriting Equation (18) to Equation (21) from [48]:  
[48] の式 (18) から式 (21) への書き換え:

$$
(162)
$$

$$
(163)
$$

$$
(164)
$$

$$
(165)
$$

Notice that the term $\sum_{t\in\mathcal{F}_{\phi}^{\prime}}\mathbb{E}\left[\mathds{1}\left\{T_{i_{\phi}^{*},t,\tau}\leq\bar{n}_{A}\right\}\right]$ is bounded using Lemma 8, implying that the event $\mathds{1}\{\cdot\}$ is:  
項 $\sum_{t\in\mathcal{F}_{\phi}^{\prime}}\mathbb{E}\left[\mathds{1}\left\{T_{i_{\phi}^{*},t,\tau}\leq\bar{n}_{A}\right\}\right]$ は補題 8 を用いて有界であることに注意してください。これは、事象 $\mathds{1}\{\cdot\}$ が次のように示されることを意味します:

$$
(166)
$$

However, the separation of the event used by the author (following the line of proof [29]) in Equation (12) to Equation (16) in [48]:  
しかし、著者が使用した事象の分離（証明 [29] に従う）において、式 (12) から式 (16) への [48]:

$$
(167)
$$

$$
(168)
$$

$$
(169)
$$

$$
(170)
$$

$$
(171)
$$

is such that the event $\{\cdot\}$ is given by:  
このように、事象 $\{\cdot\}$ は次のように与えられます:

$$
(172)
$$

thus making the derived inequality incorrect.  
これにより、導出された不等式が不正確になります。

The same error is done also in the following equations (Equation 70 to Equation 72 in [48]):  
同様の誤りが次の式（[48] の式 70 から式 72）にもあります:

$$
(173)
$$

$$
(174)
$$

$$
(175)
$$

where notice that yet again $\sum_{t\in\mathcal{F}_{\Delta^{C},N}}\mathbb{P}\left(T_{i_{t}^{*},t,\tau}\leq\bar{n}_{A}\right)$ has been wrongly bounded by $\bar{n}_{A}\lceil\frac{N}{\tau}\rceil$.  
ここで再び、$\sum_{t\in\mathcal{F}_{\Delta^{C},N}}\mathbb{P}\left(T_{i_{t}^{*},t,\tau}\leq\bar{n}_{A}\right)$ が誤って $\bar{n}_{A}\lceil\frac{N}{\tau}\rceil$ によって有界化されていることに注意してください。



## Appendix E 補足レマ

In this appendix, we report some results that already exist in the bandit literature and have been used to demonstrate our results.
この付録では、バンディット文献に既に存在するいくつかの結果を報告し、私たちの結果を示すために使用されました。

### Lemma 3

Let $X_1,\ldots,X_n$ be independent Bernoulli random variables with $\mathbb{E}[X_i]=p_i$, consider the random variable $X=\frac{1}{n}\sum_{i=1}^{n}X_{i}$, with $\mu=\mathbb{E}[X]$.
$X_1,\ldots,X_n$ を独立したベルヌーイ確率変数とし、$\mathbb{E}[X_i]=p_i$ とします。ランダム変数 $X=\frac{1}{n}\sum_{i=1}^{n}X_{i}$ を考え、$\mu=\mathbb{E}[X]$ とします。

For any $0<\lambda<1-\mu$ we have:
任意の $0<\lambda<1-\mu$ に対して、次が成り立ちます：

### Lemma 4

For all positive integers $\alpha,\beta\in\mathbb{N}$, the following equality holds:
すべての正の整数 $\alpha,\beta\in\mathbb{N}$ に対して、次の等式が成り立ちます：

$$
F_{\alpha,\beta}^{beta}(y)
$$
where $F_{\alpha+\beta-1,y}^{B}(\alpha-1)$ is the cumulative distribution function of a binomial variable with $\alpha+\beta-1$ trials having each probability $y$.
ここで、$F_{\alpha+\beta-1,y}^{B}(\alpha-1)$ は、各確率が $y$ である $\alpha+\beta-1$ 回の試行を持つ二項変数の累積分布関数です。

### Lemma 5

Let $Z$ be a Gaussian random variable with mean $\mu$ and standard deviation $\sigma$, then:
$Z$ を平均 $\mu$ と標準偏差 $\sigma$ のガウスランダム変数とします。次が成り立ちます：

$$
(177)
$$

### Lemma 6

Let $Z$ be a Gaussian r.v. with mean $m$ and standard deviation $\sigma$, then:
$Z$ を平均 $m$ と標準偏差 $\sigma$ のガウスランダム変数とします。次が成り立ちます：

$$
(178)
$$

### Lemma 7

Let $X_1,\ldots,X_n$ be independent random variables such that $X_{i}\sim Subg(\sigma^{2})$, then for any $a\in\mathbb{R}^{n}$, we have:
$X_1,\ldots,X_n$ を独立したランダム変数とし、$X_{i}\sim Subg(\sigma^{2})$ とします。任意の $a\in\mathbb{R}^{n}$ に対して、次が成り立ちます：

$$
(179)
$$
and
$$
(180)
$$

Of special interest is the case where $a_i=1/n$ for all $i$ we get that the average $\bar{X}=\frac{1}{n}\sum_{i=1}^{n}X_{i}$ satisfies:
特に興味深いのは、すべての $i$ に対して $a_i=1/n$ の場合であり、平均 $\bar{X}=\frac{1}{n}\sum_{i=1}^{n}X_{i}$ が次を満たします：

### Lemma 8

Let $A\subset\mathbb{N}$, and $\tau\in\mathbb{N}$ fixed. Define $a(n)=\sum_{t=n-\tau}^{n-1}\mathds{1}\{t\in A\}$. Then for all $T\in\mathbb{N}$ and $s\in\mathbb{N}$ we have the inequality:
$A\subset\mathbb{N}$ とし、$\tau\in\mathbb{N}$ を固定します。$a(n)=\sum_{t=n-\tau}^{n-1}\mathds{1}\{t\in A\}$ を定義します。すべての $T\in\mathbb{N}$ および $s\in\mathbb{N}$ に対して、次の不等式が成り立ちます：

$$
(181)
$$

### Lemma 9

Let $j\in\mathbb{N}$, $PB(\underline{\mu}_{i^{*}(t)}(j))$ be a Poisson-Binomial distribution with parameters $\underline{\mu}_{i^{*}(t)}(j)=(\mu_{i^{*}(t),1},\dots,\mu_{i^{*}(t),j})$, and $Bin(j,x)$ be a binomial distribution of $j$ trials and probability of success $0\leq x\leq 1$. Then, it holds that:
$j\in\mathbb{N}$ とし、$PB(\underline{\mu}_{i^{*}(t)}(j))$ をパラメータ $\underline{\mu}_{i^{*}(t)}(j)=(\mu_{i^{*}(t),1},\dots,\mu_{i^{*}(t),j})$ のポアソン-二項分布とし、$Bin(j,x)$ を $j$ 回の試行と成功確率 $0\leq x\leq 1$ の二項分布とします。次が成り立ちます：

### Lemma 10

Let $F_{n,p}^{B}$ be the CDF of a $Bin(n,p)$ distributed random variable, then holds for $m\leq n$ and $q\leq p$:
$F_{n,p}^{B}$ を $Bin(n,p)$ 分布の累積分布関数とします。次が成り立ちます $m\leq n$ および $q\leq p$ の場合：

$$
(182)
$$
for all $x$.
すべての $x$ に対して。

### Lemma 11

(i) A $\mathcal{N}(m,\sigma^{2})$ distributed r.v. is stochastically dominated by $\mathcal{N}(m',\sigma^{2})$ if $m' \geq m$.
(i) $\mathcal{N}(m,\sigma^{2})$ 分布のランダム変数は、$m' \geq m$ の場合に $\mathcal{N}(m',\sigma^{2})$ によって確率的に支配されます。

(ii) A $Beta(\alpha,\beta)$ random variable is stochastically dominated by $Beta(\alpha',\beta')$ if $\alpha' \geq \alpha$ and $\beta' \leq \beta$.
(ii) $Beta(\alpha,\beta)$ ランダム変数は、$\alpha' \geq \alpha$ および $\beta' \leq \beta$ の場合に $Beta(\alpha',\beta')$ によって確率的に支配されます。



##### Report Github Issue GitHubの問題報告

LATE
LATE

A
A

E
E

xml
xml



## Instructions for reporting errors エラー報告の手順

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. 
私たちは論文のHTMLバージョンを改善し続けており、あなたのフィードバックはアクセシビリティとモバイルサポートの向上に役立ちます。 
To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:
HTMLのエラーを報告するには、以下に示すいずれかの方法を選択してください。

- Click the "Report Issue" button.
- "Report Issue"ボタンをクリックしてください。
- Open a report feedback form via keyboard, use "Ctrl + ?".
- キーボードを使用して報告フィードバックフォームを開くには、「Ctrl + ?」を使用してください。
- Make a text selection and click the "Report Issue for Selection" button near your cursor.
- テキストを選択し、カーソルの近くにある「Report Issue for Selection」ボタンをクリックしてください。
- You can use Alt+Y to toggle on and Alt+Shift+Y to toggle off accessible reporting links at each section.
- 各セクションでアクセシブルな報告リンクをオンにするにはAlt+Yを、オフにするにはAlt+Shift+Yを使用できます。

Our team has already identified the following issues. 
私たちのチームはすでに以下の問題を特定しています。 
We appreciate your time reviewing and reporting rendering errors we may not have found yet. 
私たちは、まだ見つけていない可能性のあるレンダリングエラーをレビューし報告するためにあなたが費やす時間に感謝します。 
Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. 
あなたの努力は、すべての読者のためにHTMLバージョンを改善するのに役立ちます。なぜなら、障害は研究へのアクセスの障壁であってはならないからです。 
Thank you for your continued support in championing open access for all.
すべての人にオープンアクセスを推進するためのあなたの継続的なサポートに感謝します。

Have a free development cycle? Help support accessibility at arXiv! 
開発サイクルに余裕がありますか？arXivでのアクセシビリティをサポートしてください！ 
Our collaborators at LaTeXML maintain a list of packages that need conversion, and welcome developer contributions.
私たちの協力者であるLaTeXMLは、変換が必要なパッケージのリストを維持しており、開発者の貢献を歓迎しています。
