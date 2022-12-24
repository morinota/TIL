# RankNetの拡張、LambdaRank(2006)

RankNetは、**モデルが出力した確率と真の確率のクロスエントロピー**を最小化することで、ランキングを正確にするアルゴリズムだった。
しかし、場合によってはクロスエントロピー以外の指標を最小化したいケースがある。

例えば、web検索の検索結果などにおいて、**１番目と３番目の記事の順番が逆**になってしまっているのと、**７番目と９番目の記事が逆になってしまっている**のは、どちらが重大な間違いだろうか。
人間視点から見れば、**明らかに前者の方がより大きな間違い**だと言える。

このように、例えば上位N位までの正確性を重視したい場合は、クロスエントロピー以外の損失関数をデザインすることができ、一般的に次のように書ける。

$$
L(
        f(X_{q,1}, y_{q,1}),
        f(X_{q,2}, y_{q,2}),
        \cdots,
        f(X_{q,m_q}, y_{q,m_q})
    )
$$

もしくは、Q個の検索キーワード(or ユーザ)を想定する場合は...

$$
L_0 = \sum_{q}{
    L(
        f(X_{q,1}, y_{q,1}),
        f(X_{q,2}, y_{q,2}),
        \cdots,
        f(X_{q,m_q}, y_{q,m_q})
    )
}
$$

つまり、RankNetはペアワイズ、LambdaRankはリストワイズの損失関数を使用してる！！

ここで問題になるのは、順**位が関係する損失関数は一般的には連続値を取らない**ので、LambdaRankのような微分を用いた最適化ができないということ。

そこで、LambdaRankはRankNetを拡張して最適化を行う！
元のLambdaRankは次の微分を使用して最適化していた。

$$
\frac{\partial C}{\partial \mathbf{w}}
= \sum_{(i, j) \in I}{
  \frac{\partial C_{ij}}{\partial \mathbf{w}}
  } \\
= \sum_{(i, j) \in I}{
  \frac{\partial C_{ij}}{\partial o_{ij}}
  (
    \frac{\partial f_{\mathbf{w}}(X_i)}{\partial \mathbf{w}}
    - \frac{\partial f_{\mathbf{w}}(X_j)}{\partial \mathbf{w}}
  )
  } \tag{3}
$$

LambdaRankではそれを以下のように改変する！

$$
\frac{\partial C'}{\partial \mathbf{w}}
= \sum_{(i, j) \in I}{
  \frac{\partial C_{ij}}{\partial o_{ij}}
  |\Delta_{ij}|
  (
    \frac{\partial f_{\mathbf{w}}(X_i)}{\partial \mathbf{w}}
    - \frac{\partial f_{\mathbf{w}}(X_j)}{\partial \mathbf{w}}
  )
  } \tag{3}
$$

ここで$\Delta_{ij}$は、出力値f(x_i)とf(x_j)の値を逆にした場合のリストワイズ損失関数Lの差:

$$
\Delta_{ij} = L(\{f(x_1), \cdots, f(x_i), \cdots, f(x_j), \cdots, f(x_m)\}, {l_1, \cdots, l_m}) \\
- L(\{f(x_1), \cdots, f(x_j), \cdots, f(x_i), \cdots, f(x_m)\}, {l_1, \cdots, l_m})
$$

これを微分としてgradient descent(勾配降下法)を行うと、LLを小さくできることが知られている。

直感的には、**間違えると大きな損失をうむ $(i,j)$のペアに関する勾配を増やしている**(＝**重み付けしている**！)、と見なす事ができる！

# 参考

- ランキング学習： RankNetからLambdaRank、そしてLambdaMARTへ
  - https://qiita.com/kiita_da_yo/items/8ba552fce5b99cbf85fd
