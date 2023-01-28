## ref

- [本論文](https://dl.acm.org/doi/fullHtml/10.1145/3523227.3548486#BibPLXBIB0010)
- オリジナルのiALS: [Collaborative Filtering for Implicit Feedback Datasets](http://yifanhu.net/PUB/cf.pdf)
- 損失関数の拡張ver?(unobserved weightについて)[A Generic Coordinate Descent Framework for Learning from Implicit Feedback](https://dl.acm.org/doi/10.1145/3038912.3052694)
- 損失関数の正則化項に関する拡張?[Large-Scale Parallel Collaborative Filtering for the Netflix Prize](https://link.springer.com/chapter/10.1007/978-3-540-68880-8_32)

# Implicit Alternating Least Squares (iALS)について

## Item Recommendation from Implicit Feedback

ユーザ集合Uに対して集合Iからアイテムを推薦する.
学習の為に、正のユーザ*アイテムペア集合$S \subseteq U\times I$(i.e. Sは、任意のU*Iペア集合の部分集合.等号含む.)が与えられる. (=implicit feedback. 場合によっては重みの異なるfeedbackも得られる.)
ex. $(u, i)\in S$: ユーザuが映画iを見た, あるいは顧客uが製品iを買った.

implicit feedbackからの学習の大きな困難は、S内のfeedbackが全てpositiveのみ(i.e. negativeなfeedbackが存在しない). その上で、全ての未観測ペア $U\times I \setminus S$(= **集合U\*Iに対する 集合Sの差集合**)を推定する必要がある事.

implicit ALSでは、Sを用いて、この任意のユーザ\*アイテムのペア(u, i)にスコア $\hat{y}(u,i)$を割り当てるモデルを作る.

## iALS: Model, Loss and Training iALS

### model
iALSは行列分解モデルを用いる.

各ユーザーuはd次元の埋め込みベクトル$w_u$に、各アイテムiはd次元の埋め込みベクトル$h_i$として、特徴づけられる.
ユーザとアイテムのペアの予測スコアは、それらの埋め込みベクトル間の内積.

$$
\hat{y}(u,i) := <w_u, h_i>, W\in \mathbb{R}^{U\times d}, H \in \mathbb{R}^{I \times d} \tag{1}
$$


iALSにおいて学習プロセスで推定されるべきモデルパラメータは、embedding matrix WとH(元論文にはlatent matrixと表記されていた気がする).

### 損失関数

パラメータは3つの要素からなるiALS損失$L(W, H)$を最小化することによって学習される.

$$
L(W,H) &= L_S(W,H) + L_I(W,H) + R(W,H) \tag{2}
$$

(**ALSを用いた行列分解に関する文献**では、これらの成分について若干異なる定義が存在するらしい...)
論文では、 [2]に従って全てのペアをunobserved weightで重み付けする形式(=一律の重み?)を採用.
[29] が提案したように、周波数ベースの正則化を行う.

損失関数(2)の構成要素は以下. (元論文Hu_et_alとは少し損失関数が異なる.元論文では PreferenceとConfidenceという概念があった.)

$$
L_S(W,H) = \sum _{(u,i) \in S} (\hat{y}(u,i) - 1)^2
\tag{3}
$$

第1成分LSは**観測されたペアSに対して**定義され、予測スコアが観測されたラベル（ここでは1）とどの程度異なるかを評価する成分.

$$
L_I(W,H) = \alpha _0\sum _{u \in U} \sum _{i\in I} \hat{y}(u,i)^2
\tag{4}
$$

第二成分LIは**U×Iにおける全てのペアに対して**定義され、予測スコアが0とどれだけ違うかを評価する成分.

$$
R(W,H) = \lambda \left(\sum _{u \in U} \#_u^\nu \, \Vert \mathbf {w}_u\Vert ^2 + \sum _{i \in I}\#_i^\nu \, \Vert \mathbf {h}_i\Vert ^2 \right)
\\
\#_u = |\lbrace i : (u,i) \in S\rbrace |+\alpha _0 |I| \\
\#_i = |\lbrace u : (u,i) \in S\rbrace |+\alpha _0 |U|
\tag{5}
$$

第三成分RはL2正則化であり、埋め込みベクトルのノルムが小さくなるように促す成分. 
νは頻度正則化の強さを制御し、従来のALS正則化ν=0とSGD最適化器が暗黙的に適用する頻度正則化重み付けν=1の間で切り替える.(?? 29を読めばわかる...?)

### 損失関数の3つの成分の関係

個々の(u,i)ペアでは、各成分LS, LI, Rの損失は0になりやすいが、**合同で意味のある目的を形成**する.
この3つの成分のトレードオフは、 **unobserved weight** $\alpha_0$ **regularization weight(正則化項の重み)** $\lambda$によって制御される.
適切なトレードオフを選択することはiALSにとって重要.

### 最適化手法(パラメータ推定法)

iALSの損失は、交互最小二乗法(ALS)のT回のepochによって効率的に最適化される.
各epochの計算量は、当初提案したソルバーでは$O(d^2|S| + d^3(|U|+|I|))$ で、iterative solvers(?)では$O(d|S| + d^2 (|U|+|I|))$ である [2, 10, 20]. 


