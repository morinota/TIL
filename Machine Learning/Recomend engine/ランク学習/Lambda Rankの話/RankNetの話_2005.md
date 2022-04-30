# ランキング学習における問題設定

ランキング学習のアルゴリズムは、優れた順番を生成してくれるパラメータ$\mathbf{w}$を得ることが目的となる。

# RankNet(2005)

データ $X_i$ とデータ $X_j$ の順序を比べる時、$o_{ij}=f(X_i)−f(X_j)$が$0$より大きいならば、「iがjより順位が高い確率」がその逆よりも高い、ということになります。

RankNetでは、その確率が$o_{ij}$にのみ依存すると仮定し、次のようにモデリングする。

$$
P_{ij} = sigmoid(o_{ij}) = \frac{1}{1 + \exp(-o_{ij})} \tag{1}
$$

ここでP\_{ij}は、"**iがjより順位が高い確率**"を示す。

真の確率(質量関数。今回の場合は(1, 0)か(0, 1))を$\bar{P}_{ij}$とし、推定値$P_{ij}$(ex. (0.8, 0.2))に対する、交差エントロピー誤差(Cross-entropy Loss)を計算すると、

$$
C_{\bar{P}_{ij}, P_{ij}}
= - \sum_{x}{\bar{P}_{ij}(x) \cdot \log{P_{ij}(x)}} \\
= - \bar{P}_{ij} \cdot \log{P_{ij}} - (1 - \bar{P}_{ij}) \cdot \log{(1 - P_{ij})} \\
$$

式(1)を代入して...

$$
C_{\bar{P}_{ij}, P_{ij}}
= - \bar{P}_{ij} \cdot \log{sigmoid(o_{ij})}
- (1 - \bar{P}_{ij}) \cdot \log{(1 - sigmoid(o_{ij}))} \\

\because シグモイド関数を代入して... \\

= - \bar{P}_{ij} \cdot \log{\frac{1}{1 + \exp(-o_{ij})}}
- (1 - \bar{P}_{ij}) \cdot \log{\frac{\exp(-o_{ij})}{1 + \exp(-o_{ij})}}\\

\because 分子と分母に \exp(o_{ij})をかけて...\\

= - \bar{P}_{ij} \cdot \log{\frac{\exp(o_{ij})}{1 + \exp(o_{ij})}}
- (1 - \bar{P}_{ij}) \cdot \log{\frac{1}{1 + \exp(o_{ij})}}\\

\because logの中身を展開して...\\

= - \bar{P}_{ij} \cdot \{o_{ij} - \log(1+\exp(o_{ij}))\}
- (1 - \bar{P}_{ij}) \cdot  \{0 - \log (1 + \exp(o_{ij}) )\} \\

= \bar{P}_{ij} \cdot \{- o_{ij} + \log(1+\exp(o_{ij}))\}
+ (1 - \bar{P}_{ij}) \cdot \{\log(1+\exp(o_{ij}))\} \\

= - o_{ij} \bar{P}_{ij} + \log(1 + \exp(o_{ij})) \tag{2}
$$

となる。ここで、任意のiとjに対して、真の確率(質量関数, "**iがjより順位が高い確率**")は、

$$
P_ij =
\begin{cases}
  1 & (x_iの方が順位が高い) \\
  0 & (x_jの方が順位が高い) \\
  \frac{1}{2} & 順位が同じ
\end{cases}
$$

の3通りの値を取り得る。これらを式(2)に代入すると、任意のiとjに対する交差エントロピー誤差の値は、

$$
C_ij =
\begin{cases}
  - o_{ij} + \log(1 + \exp(o_{ij})) = \log(\exp(-o_{ij})+1) & (x_iの方が順位が高い) \\
  \log(1 + \exp(o_{ij})) & (x_jの方が順位が高い) \\
  \log(\frac{1}{2} \exp(o_{ij}) - \frac{1}{2} \exp(o_{ij})) & (順位が同じ)
\end{cases}
$$

と表される。

データが$I = \{ (i,j)|x_iとx_jを比べるとx_iの方が順位が高い \}$の形で与えられる場合、最小化したい損失関数は以下のようになる。

$$
C = \sum_{(i, j) \in I}{C_ij}
$$

この損失関数Cについて、モデルパラメータwの微分を求める事ができれば、Gradient Descent(勾配降下法)を利用して、Cを最小化するwを計算する事ができる。

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

これをバカ正直に計算すれば、$(i, j) \in I$の数に比例した回数だけ、
$\frac{\partial f_{\mathbf{w}}(X_i)}{\partial \mathbf{w}}$
を計算する事になる。

もしモデルfにニューラルネットワークを使用する場合、Back Propagation等のコストの掛かる計算になってしまう。

そこで、式3を以下のように書き直す。

$$
\frac{\partial C}{\partial \mathbf{w}}
= \sum_{(i, j) \in I}{
  \frac{\partial C_{ij}}{\partial o_{ij}}
  (
    \frac{\partial f_{\mathbf{w}}(X_i)}{\partial \mathbf{w}}
    - \frac{\partial f_{\mathbf{w}}(X_j)}{\partial \mathbf{w}}
  )
  } \\

= \sum_{i}{\lambda _{i} \frac{\partial f_{\mathbf{w}}(X_i)}{\partial \mathbf{w}}
}
$$

上式におけるλは以下で定義される。

$$
\lambda_i = \sum_{j:(i, j) \in I}{
  \frac{\partial C_{ij}}{\partial o_{ij}}
}
- \sum_{j:(j, i) \in I}{
  \frac{\partial C_{ij}}{\partial o_{ij}}
}
$$

ここで、sumが(i, j)に関する和から、iに関する和になっている事に注目。この形式にする事によって、モデルの微分の計算はデータ数分で済むことが明らかになっている。

# RankNetの拡張、LambdaRank(2006)



# 参考

- ランキング学習： RankNetからLambdaRank、そしてLambdaMARTへ
  - https://qiita.com/kiita_da_yo/items/8ba552fce5b99cbf85fd
