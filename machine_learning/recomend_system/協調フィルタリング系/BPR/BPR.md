## 参考

- https://qiita.com/guglilac/items/49bc35bd2631177624ce#implicit-feedback--ranking%E5%AD%A6%E7%BF%92
- レコメンドアルゴリズム(BPR)の導出から実装まで
  - https://techblog.zozo.com/entry/2016/07/01/134825
- [元論文?](https://github.com/zerebom/paper-books/issues/51)
- [論文まとめ](https://www.smartbowwow.com/2019/09/bpr-bayesian-personalized-ranking-from.html)

# implicit feedback + ranking学習という考え

Bayesian Personalized Ranking (BPR)は、**implicit feedbackからランキング学習を行う手法**.

BPR以前にimplicit feedbackからランキング学習を行う手法としては、手元にある履歴のデータは正例のラベルをつけて, **未観測のuser\*itemの組をランダムにサンプリングして負例ラベルをつけ、２値分類問題を解く**という手法があった.
(それこそH&Mでの一般的な解法!=> 負例の付け方に工夫あり!)

学習した後、userごとに未観測のアイテムのリストを渡して一つずつ予測し、予測された正例の確率でソートしてランキングを出力、という流れ.

これはランキング学習の手法の中でもpoint-wiseな手法に分類される.
当然分類器はlog lossなどのlossに対して最適化しているため、ランキングの評価指標とは異なる方向に最適化している.

BPRはこのようなpoint-wiseな手法ではなく、データの組を入力とする**pair-wiseな手法**に分類される.

## BPRのお気持ち

BPRでは(履歴に出てきた(=positive) item A, user B)の組 (履歴にないitem C, user B)の組に関して、「**user Bが item Aを item C よりも 好む**」という仮定を置く.
出てきていない者同士、出てきた者同士はどちらをより好むかはわからないとする.

user Bが item Cを少しは好んでいてまだ買っていない状態だとしても、**item Aよりは好みの度合いが小さい**、みたいなことを表現している.
(i.e. 未観測(u, i)のペアについて、全てnegativeと捉えるのではなく、あくまで順序を予測している?)

## BPRの定式化

BPRは、あるuserがあるitemをどれくらい好むかという**preference scoreを予測するmodelを必要**とする.
**このmodelの部分はどのモデルでもよく**、baselineとしてはよくMatrix Factorizationなどが用いられる.

BPRでは、**正例のitem**と、**サンプリングしてきた未観測item**の二つのitemを受け取り、それぞれuserとのpreference scoreを計算する.

その差をsigmoid関数に通して、どちらのitemがより好まれるかを予測する.

user $u$が item $j$よりもitem $i$を好む確率(=パラメータ$\Theta$ から見ると尤度)を以下のように定義する.

$$
p(i > j; u,\Theta) =
p(i >_{u} j|\Theta)
:= \sigma(\hat{x}_{uij}(\Theta))
= \sigma(\hat{r}_{ui} - \hat{r}_{uj})
$$

(上の確率pは$p(i >_{u} j|\Theta)$のように表記される事もある.不等号に添え字$u$があるのが面白い...! ユーザuにとっては...みたいなイメージ.)

ここで、$\hat{x}_{uij}(\Theta)$は、「itemとuserの組を入力として何らかのスコアを出力するような、パラメータ$\Theta$のモデル」の出力値$\hat{r}_{ui}$と$\hat{r}_{uj}$の差、みたいな感じ.

これを使ってlossを作る.

後は尤度(=多分BPRの実際はMLじゃなくてMAP)が最大になるようにpreference score $p$を予測する部分のパラメータを更新していく、という流れになる.
最適化はSGD(確率的勾配降下法, Stochastic gradient descent)を用いる.

全てのアイテム$i \in I$について、正しいパーソナライズされたランキングを見つけるためのベイズ定式化は、以下の**事後確率を最大化(=MLじゃなくMAPか...!)**することである.
(ここで、$\Theta$は任意のモデルクラス（例えば、行列分解）のパラメータベクトルを表す.)

$$
p(\Theta| >_u) \sim p(>_u | \Theta) p(\Theta)
\\
\because \text{bayesの定理より、左辺は尤度関数 * 事前分布}
$$

ここで、

- $>_u$はユーザuの潜在的なアイテム嗜好度ランキング.
  - 全てのユーザは互いに独立であると仮定する.
  - また、特定のユーザーに対するアイテムの各組（i、j）の順序付けは、他のすべての組の順序付けから独立していると仮定する.

従って、上記のユーザu固有の尤度関数$\sim p(>_u | \Theta)$は、まず単一の確率密度密度の積として書き換えられ、全ユーザについて結合することができる.

$$
\prod_{u \in U} p(>_u | \Theta) = \prod_{(u,i,j) \in D_s} p(i >_u j|\Theta)
$$

これらを用いて損失関数は...

$$
BPR := - \ln \prod_{u \in U} p(\Theta| >_u) \\
= - \ln \prod_{u \in U} p(>_u | \Theta) p(\Theta) \\
= - \ln \prod_{(u,i,j) \in D_s} \sigma(\hat{x}_{uij}(\Theta)) p(\Theta) \\
= - \sum_{(u,i,j) \in D_s} \ln \sigma(\hat{x}_{uij}(\Theta)) + \ln p(\Theta) \\
$$

# BPRの導出から実装まで

要するにBPR(Bayesian Personalized Ranking)は、~~ALSと同じような、行列分解におけるパラメータを求める手法**??? ~~ **ランク学習的な損失関数の種類に近い\*\*気がする...!!

=> ユーザ×アイテムのRating Matrixを行列分解する問題の解法の一つ??

ユーザ$U$ x アイテム$I$の行列の行列分解の問題をBPRで解くことを考える.

## データ

BPRで扱う学習データは以下のように表現される.

$$
D_s := {(u, i, j)|i\in I_u^+ \land j \in I\I_u^+}
$$

($:=$は、"左辺を右辺の式で定義する"という意味)
ここで、

- I: 全てのアイテムの集合.
- $I_u^+$: ユーザ$u$が好む(=評価が正の, positive)アイテムの集合.
- $I \setminus I_u^+$: 集合Iから集合$I_u^+$を除いたものの集合.(=**差集合**)

である.
従って、集合$D_s$から取り出された任意のu,i,jのTriplet $(u,i,j)\in D_s$は、"ユーザuはアイテムjよりもアイテムiを好む"事を意味する.
(=implicitデータにおいて$j$は unlike or didn't knowの筈だが、BPRではそういう仮定を置くという話?)

集合$D_s$のサイズは$U \times I \times I$になる.(おおよそって話...!)
全てのTripletデータ($(u,i,j)\in D_s$)を学習に用いる事は不可能なので、BPRでは学習データを与えられたデータからサンプリングする.

## 定式化

分解後の行列(=行列分解をイメージ)を$W \in R^{U\times k}$, $H\in R^{I\times k}$とする.
「あるユーザuについての全アイテムの嗜好度の順序(大小関係)」を$>_u$で表すとすると、$i >_u j$と表記すれば「ユーザuはアイテムjよりもアイテムiを好む」事を指す.

この場合の尤度関数は以下のように定義される.

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
