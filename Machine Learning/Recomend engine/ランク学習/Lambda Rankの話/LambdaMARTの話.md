# LambdaMART

LambdaRankは勾配の計算方法を与えるものなので、微分可能なモデルならどのモデルにも適用することができます。LambdaRankをGradient Boostingに適用したものを、LambdaMARTというようです。

# 損失関数の勾配計算

$f(X_i)$に関する損失関数の勾配は、以下の様に計算できる。

$$
\frac{\partial C'}{\partial f(X_i)}
= \sum_{(i,j)\in I}{
  \frac{\partial C'}{\partial o_{ij}}
  |\Delta_{i,j}|
}
- \sum_{(j,i)\in I}{
  \frac{\partial C'}{\partial o_{ij}}
  |\Delta_{i,j}|
}\\

= \left( \sum_{(i,j)\in I} - \sum_{(j,i)\in I} \right)
\frac{\partial C'}{\partial o_{ij}}|\Delta_{i,j}|\\

= \left( \sum_{(i,j)\in I} - \sum_{(j,i)\in I} \right)
\frac{-|\Delta_{ij}|}{1 + \exp(f(X_i) - f(X_j))}
$$

これを用いて、Gradient Boosting を実行する事ができる。

# 参考

- ランキング学習： RankNetからLambdaRank、そしてLambdaMARTへ
  - https://qiita.com/kiita_da_yo/items/8ba552fce5b99cbf85fd
