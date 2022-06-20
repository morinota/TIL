# 参考

- https://qiita.com/guglilac/items/49bc35bd2631177624ce#implicit-feedback--ranking%E5%AD%A6%E7%BF%92
- レコメンドアルゴリズム(BPR)の導出から実装まで
  - https://techblog.zozo.com/entry/2016/07/01/134825

# implicit feedback + ranking学習

Bayesian Personalized Ranking (BPR)は、
implicit feedbackからランキング学習を行う手法。

BPR以前にimplicit feedbackからランキング学習を行う手法としては、**手元にある履歴のデータは正例のラベルをつけて、ログにないuserとitemの組をランダムにサンプリングして負例ラベルをつけ、２値分類問題を解く**という手法があった。
(それこそH&Mでの一般的な解法!=> 負例の付け方に工夫あり)

学習した後、userごとに未観測のアイテムのリストを渡して一つずつ予測し、予測された正例の確率でソートしてランキングを出力、という流れ。

これはランキング学習の手法の中でもpoint-wiseな手法に分類される。
当然分類器はlog lossなどのlossに対して最適化しているため、ランキングの評価指標とは異なる方向に最適化している。

# Bayesian Personalized Ranking (BPR) [Rendle+, UAI2009]

BPRはこのようなpoint-wiseな手法ではなく、データの組を入力とするpair-wiseな手法に分類される。
先に述べた手法とは異なり、ランキングの指標(AUC)に対して最適化するようなlossを提案している。

BPRは、あるuserがあるitemをどれくらい好むかという**preference scoreを予測するmodelを必要**とする。
このmodelの部分はどのモデルでもよく、**baselineとしてはよくMatrix Factorizationなどが用いられる**。

BPRでは、**正例のitem**と、**サンプリングしてきた未観測item**の二つのitemを受け取り、それぞれpreference scoreを計算する。

その差をsigmoid関数に通して、どちらのitemがより好まれるかを予測する。

**user $u$が item $j$よりもitem $j$を好む確率**を

$$
p(i > j; u,\Theta) = \sigma(\hat{r}_{ui} - \hat{r}_{uj})
$$

のように計算する。

後は尤度が最大になるようにpreference scoreを予測する部分のパラメータを更新していく、という流れになる。最適化はSGD(確率的勾配降下法, Stochastic gradient descent)を用いる。

このlossはAUCの近似になっているので、よりランキング指標に特化した最適化が行われるよ、という気持ちが現れているわけである。

# BPRの導出から実装まで

要するに**BPR(Bayesian Personalized Ranking)は、ALSと同じような、行列分解におけるパラメータを求める手法**???

=> ユーザ×アイテムのRating Matrixを行列分解する問題の解法の一つ??

ユーザ$U$ x アイテム$I$の行列の行列分解の問題をBPRで解くことを考えます。
## データ

BPRで扱う学習データは以下のように表現する

$$
D_s := 
{(u, i, j)|i\in I_u^+ \land j \in I\I_u^+}
$$

ここで、
- Iは全てのアイテムの集合、
- $I_u^+$はユーザ$u$が好む(評価が正の)アイテムの集合、
- $I\I_u^+$はIから$I_u^+$を除いたものの集合

である。
したがって、$(u,i,j)\in D_s$の意味は、「ユーザuはアイテムjよりアイテムiを好む」となる。

$D_s$のサイズは$U \times I \times I$になる。全てのデータを学習に用いる事は不可能なので、BPRでは学習データを与えられたデータからサンプリングする。

```python
# sample a user
u = np.random.randint(userCount)
itemList = trainMatrix.getrowview(u).rows[0]
if len(itemList) == 0:
    continue

# sample a positive item
i = random.choice(itemList)

# sample a negative item
j = np.random.randint(itemCount)
while trainMatrix[u, j] != 0:
    j = np.random.randint(itemCount)
```

## 定式化
分解後の行列を$W \in R^{U\times k}$, $H\in R^{I\times k}$とする。
「あるユーザuについての全アイテムの嗜好度の順序(大小関係)」を$>_u$で表すとすると、$i >_u j$と表記すれば「ユーザuはアイテムjよりもアイテムiを好む」事を指す。

この場合の尤度関数は以下のように定義される。

$$
\prod_{u\in U}{p(>_u | W, H)} 
:= \prod_{(u,i,j)\in D_s}{p(i >_u j |W, H)}
$$

ここで、
$$
p(i >_u j |W, H) = \sigma(W_u H_i^T - W_u H_j^T), \\
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

である。また、W, Hの事前分布をEを単位行列として

$$
W ~ N(0, \lambda_W E) \\
H ~ N(0, \lambda_H E)
$$

で定義すると、事後確率最大化(MAP)の式は以下で与えられる。

$$
L := \ln p(W, H|>_u) \\
= \ln p(>_u|W, H)p(W)p(H) \\
= \ln p(>_u|W, H) + \ln p(W) + \ln p(H) \\
= \ln \prod_{(u,i,j)\in D_s}{p(i >_u j |W, H)} + \ln p(W) + \ln p(H) \\
= \ln \prod_{(u,i,j)\in D_s}{\sigma(W_u H_i^T - W_u H_j^T)} + \ln p(W) + \ln p(H) \\
= \sum_{(u,i,j)\in D_s}{\ln \sigma(W_u H_i^T - W_u H_j^T)} - \lambda_W||W||^2 - \lambda_H ||H||^2
$$

この式を最大化するW,Hを求めることがBPRの目的となる。
第1項で好きなアイテムに関する予測値とそうでないアイテムに関する予測値の差を大きくするように学習する。
第2項、第3項は正則化項として機能する(=>事前分布の項がL2(?)正則化項として機能してる?!)
