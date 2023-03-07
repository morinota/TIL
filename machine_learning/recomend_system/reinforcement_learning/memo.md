## link

- https://yagami12.hatenablog.com/entry/2019/02/22/210608

# 強化学習のモデル化

- Agent: 意思決定と学習（※将来に渡る収益の期待値を最大化するような学習）を行う行動主体.
- 環境: Agent が相互作用を行う対象であり、agent のaction $a$ を反映した上で、agent に対して、state $s$ と、そのstate でのreward $r$ を与える.
- Agent のaction $a$は、確率分布で表現される 行動方策(policy) $\pi(s, a)$ に基づいて(確定的 or 確率的)選択される.
  - $\pi(s, a)$ : s_t =sならば(=の条件で) $a_t = a$ となる確率を表す.(=つまり条件付き確率.)


## Agentと環境の相互作用

## 環境のマルコフ性


