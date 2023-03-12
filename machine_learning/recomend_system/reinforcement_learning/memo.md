## link

- https://yagami12.hatenablog.com/entry/2019/02/22/210608

# 強化学習のモデル化

- Agent: 意思決定と学習（※将来に渡る収益の期待値を最大化するような学習）を行う行動主体.
- 環境(environment): Agent が相互作用を行う対象であり、agent のaction $a$ を反映した上で、agent に対して、state $s$ と、そのstate でのreward $r$ を与える.
  - (推薦システムにおいては、environment = userになる!)
- Agent のaction $a$は、確率分布で表現される 行動方策(policy) $\pi(s, a)$ に基づいて(確定的 or 確率的)選択される.
  - $\pi(s, a)$ : s_t =sならば(=の条件で) $a_t = a$ となる確率を表す.(=つまり条件付き確率.)
- エージェントと環境は、継続的に(i.e. 離散時間 $t=0,1,2,...$ の各々の時間 t おいて)相互作用を行う.

## 報酬に関して: immediate reward(即時報酬) と discounted cumulative reward(割引累積報酬)

強化学習における全てのAgentの目的は、"将来に渡る=Cumulative reward"を最大化する事.

- immediate reward $r$: あるstateにおいてagentがactionを起こした結果、どれくらいの報酬が得られるのか.
- cumularive reward
  - $R_t$ や$G(t)$で表される?
  - 時間tにおける discounted rewardは $R_t = r_{t+1} + \gamma \times r_{t+2} + \gamma^2 r_{t+3} + \cdots$
- discount rate(割引率) $\gamma$:
  - agentのゴールを絞り込む為に設定するハイパーパラメータ.
  - 0 ~ 1の値を取る.
  - $\gamma = 0$ の場合, **agentは直近の報酬(=即時報酬)にしか関心がない...!**
  - $\gamma = 1$ の場合, 各ステップtの報酬(即時報酬)はdiscountされない.
  - $\gamma$ の値が大きい程、agentは遠い将来の報酬をより気にするようになる.
  - $\gamma$ の値が小さい程、agentはより極端なdiscountを行う(=**将来の報酬に対するdiscount...!**)

agentがその意思決定目的とする収益(=cumulative rewardの事)は、**時間経過 $t=0,1,2,..$ での時間経過によって、その値が減衰する**ものとする.

## Agentと環境の相互作用

## マルコフ決定過程(Markov Decision Process, MDP) と One-step Dynamics

- state space $S$: すべてのstateの集合.
- action space $A$: 可能なactionの集合. 
  - state $s$で利用可能なactionの集合を$A(s)$と表す.

environmentの**One-step Dynamics**は、"**environmentが時間ステップ毎にstateやrewardをどのように決めるか**"を意味する.
これは、それぞれ可能な$s', r, s, a$について、 $p(s', r|s, a) = P(S(t+1)=s', R(t+1)=r|S(t)=s, A(t)=a)$ を指定する事で定義できる.
(ようするに**条件付き確率**か!)

MDPは以下のように定義される.

- stateの集合 
