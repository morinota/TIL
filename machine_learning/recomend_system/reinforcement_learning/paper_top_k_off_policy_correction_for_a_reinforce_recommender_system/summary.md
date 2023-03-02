# Top-K Off-Policy Correction for a REINFORCE Recommender System

published date: hogehoge September 2019,
authors: Chen
url(paper): https://arxiv.org/abs/1812.02353
(勉強会発表者: morinota)

---

## どんなもの?

- 推薦システムにおいては、膨大な量のimplicit feedback(ex. ユーザのクリック数、滞在時間など)が学習用に利用できる.
- しかし、ログに記録されたfeedbackからの学習は、現在運用している推薦システムによって選択された推薦アイテムリストに対するfeedback のみ を観測することによって引き起こされるbiasに左右される.
- 本論文では、REINFORCEアルゴリズム[48]を、非常に大きなaction space と state space を持つneural candidate generator(top-K推薦システム)に適応させた経験を紹介する.
  - REINFORCEアルゴリズム[48]:
    - 強化学習の一種であるpolicy勾配法の中で、最も基本的なアプローチ.
    - policy勾配法 = agentのpolicy(行動選択戦略)を直接最適化することで、最適な行動を選択するようにagentを訓練する方法.

## 先行研究と比べて何がすごい？

## 技術や手法の肝は？

### 問題設定

まず、本論文における推薦システムの構成と、RLに基づく推薦のアプローチについて説明する.

**推薦システムとユーザとの過去のInteraction**(=推薦システムがある動画アイテムをオススメして、それに対してユーザがどのようなreactionを示したか!)の **sequence(順序)**を考慮する.
(ex. 各ユーザについて、推薦システムが行ったaction(i.e. 推薦するアイテム)、および、クリックや視聴時間などのuser feedbackを記録したデータ.)

このような一連の動作が与えられると、クリック数や視聴時間などのユーザ満足度の指標を向上させるような、次にとるべきaction(i.e.推薦する動画アイテム)を予測する.

この設定を 以下のようなマルコフ決定過程(Markov Decision Process, MDP)$(S, A, P, R, \rho_0,\gamma)$に置き換える:

- $S$: ユーザーの状態を記述するcontinuous(連続的)なstate space.
- $A$: 推薦可能なアイテムを含む、discrete(離散的)な action space.(i.e. 推薦アイテムの選択肢=候補?)
- $P$: $S \times A \times S \rightarrow \mathbb{R}$ は state transition probability(状態遷移確率).
  - agentのactionを受けてstateが変化する時の**確率分布**.
  - (stateはcontinuous valueだから、たぶん確率密度関数)
  - $p(s', r|s, a) = P(S_{t+1}=s', R_{t+1}=r|S_t=s, A_t=a)$
- $R$: $S \times A \rightarrow \mathbb{R}$ は reward function(報酬関数).
  - ex) $r(s, a)$はユーザのstate $s$においてaction $a$ を行うことによって得られる immediate reward(即時報酬)である.
  - 下の期待累積報酬を最大化する数式を見た感じでは、$R$はcumulative rewardを返すような関数? 一方で小文字$r$はimmediate rewardを返すような関数.
- $\rho_0$: initial state distribution(初期状態分布).
- $\gamma$: 将来の報酬に対するdiscount factor(割引係数).

そして推薦システムが得る**expected cumulative reward(期待累積報酬)を最大化するような**, policy $\pi(a|s)$ を模索する.
policy $\pi(a|s)$は、ユーザのstate $s \in S$を条件づけた上で推薦アイテム $a \in A$ を選択する確率(確率質量)を返すような 確率分布関数.

$$
\max_{\pi} J(\pi) = E_{\tau \sim \pi}[R(\tau)],
\\
\text{where } R(\tau) = \sum_{t=0}^{|\tau|} r(s_t, a_t)
$$

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
