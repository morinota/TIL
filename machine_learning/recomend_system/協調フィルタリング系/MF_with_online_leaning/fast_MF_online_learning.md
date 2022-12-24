## 0.1. link

- https://arxiv.org/abs/1708.05024

## title:

Fast Matrix Factorization for Online Recommendation with Implicit Feedback

## 0.2. Abstract

# 1. Introduction

# 2. Related Work

# 3. Preliminaries 前置き

## 3.1. MF method for Implicit Feedback

まず基本的な表記法をまとめる。

- $R \in \mathbb{R}^{M \times N}$:ユーザとアイテムのInteraction Matrix(Explicitデータの場合はRating Matrix?)
- $M$:the number of users
- $N$:the number of items
- $\mathcal{R}$: the set of user-item pairs whose values are non-zero.
- $u, i$: indices of a user and an item.
- $\mathbf{p}_u$: the user latent vector for $u$
- $\mathcal{R}_{u}$: the set of items that are interacted by $u$.
- $\mathbf{q}_i$: the item latent vector for $u$
- $\mathcal{R}_{i}$: the set of users that are interacted by $i$.
- $P \in \mathbb{R}^{M\times K}$: the latent factor matrix for users.
- $Q \in \mathbb{R}^{N\times K}$: the latent factor matrix for items.

$$
\hat{r}_{ui} = <\mathbf{p}_u, \mathbf{q}_i> = \mathbf{p}_u^T \mathbf{q}_i
\tag{1}
$$

モデルパラメータを推定する為に、Hu et al. (確かこれが前に読んだやつ！)は、Implicitフィードバック行列$R$の各予測に**重み（＝たしか、信頼度Confidenceだっけ...?**）を関連付ける、**weighted regression function**を(目的関数として！！)導入した。

$$
J = \sum_{u=1}^M \sum_{i=1}^N w_{ui}(r_{ui} - \hat{r}_{ui})^2
+ \lambda(\sum_{u=1}^M ||\mathbf{p}_u||^2
+ \sum_{i=1}^N ||\mathbf{q}_i||^2)
\tag{2}
$$

ここで、

- $w_{ui}$: the weight of entry $r_{ui}$. and we use $W=[w_{ui}]_{M\times N}$
- $\lambda$: the strength of regularizationをコントロールするハイパーパラメータ。

ImplicitフィードバックのMFでは、通常、欠落したentriesには$r_{ui}$の値はゼロだが、**$w_{ui}$の重みはゼロでないものが割り当てられ**、どちらも性能にとって重要であることに注意されたい。

## 3.2. Optimization by ALS

交互最小二乗法(ALS)は、MFやグラフ正則化などの回帰モデルを最適化するための一般的なアプローチです[10]。ALSは、1つのパラメータを繰り返し最適化し、他のパラメータは固定することで機能します。**ALSの前提条件は、最適化の部分問題が解析的に解けること**である。ここでは、Huの研究[12]がこの問題をどのように解決しているかを説明する。

まず、user latent vector puに関してJを最小化することは、以下の目的関数$J_u$最小化することと等価である。

$$
J_u = ||W^u (r_u - Q \mathbf{p}_u)||^2 + \lambda ||\mathbf{p}_u||^2
$$

ここで、

- $W^u$は、$N \times N$のDiagonal matrix(対角行列)。
  - つまりその対角要素$W_{ii}^u = w_{ui}$

そして上の$J_u$を最小にするのは、一階微分=0となるところ。

$$
\frac{\partial J_u}{\partial p_u}
= 2 Q^T W^u Q p_u - 2Q^T W^u r_u + 2\lambda p_u = 0 \\
\Rightarrow p_u = (Q^T W^u Q + \lambda I)^{-1} Q^T W^u r_u
\tag{3}
$$

ここで、

- $I$は単位行列(Identity Martix)。

この解析解はリッジ回帰とも呼ばれる。同じ手順に従って、$q_i$の解も得る事ができる。

### 3.2.1. Efficiency Issue with ALS

- userとitemのlatent vectorを更新する為に、$K \times K$行列の逆行列の計算が避けられない。
- **行列の反転はExpensiveな処理**であり、通常、時間計算量は$O(K^3)$と仮定される。
- その為、ある１ユーザのuser latent vectorを更新するには、時間$O(K^3 + N K^2)$を要する。
- したがって、全てのモデルパラメータ(user latent matrix & item latent matrix)を一回更新する為に必要な時間計算量(Time Complexity)は、$O((M+N)K^3 + MNK^2)$
- 明らかに、この計算量の多さは、数百万のuserとitem、数十億のInteractionが存在し得る大規模データでこのアルゴリズムを実行する事を非現実的なモノにしている。

### 3.2.2. Speed-up with Uniform Weighting

- Hu et alは、高い計算量を削減する為に、missing entries(=Rating matrixのゼロ要素)に対して一律の重みを適用した。
  - ＝＞すなわち、Rating Matrixの全てのゼロ要素は、同じ重み$w_0$を持つと仮定。

この工夫を使うと、user latent vectorの更新式(式3)の中の$Q^T W^u Q$は以下のように変形できる。

$$
Q^T W^u Q = w_0 Q^T Q + Q^T (W^u - W^0)Q \tag{4}
$$

ここで、

- $W^0$ : 全ての対角要素が$w0$である対角行列(diagonal matrix)

そして$Q^T Q$は、任意の$u$とは独立なので、全てのuser latent vectorを更新する前に事前計算が可能。
$W^u - W^0$が$|R_u|$個の非ゼロ要素しか持たない事を考慮すると、式(4)を$O(|R_u| K^2)$で計算する事が可能。

＝＞したがって、ALSにおける全てのパラメータ一回更新にかかるtime Complexityは、$O((M + N)K^3 + |R|K^2)$に低減される！

それでも、逆行列の計算部分$O((M + N)K^3)$項は、$(M + N)K \geq |R|$の場合に主要なコストとなりうる。(**すなわちlatent vectorの次元数$K$が多くなればなるほど**...!!!**$K^3$だからグングン**！！)
更に、$O|R|K^2$の部分は、$O(|R|K)$の時間しか必要としないSGDに比べてずっと高い。

＝＞**latent vectorの次元数$K$の大きさは、より良い汎化性、ひいてはより良い予測性能につながる為、非常に重要なハイパーパラメータ**である。
そのため、上記の手法によって高速化されたALSを持ってしても、大規模データでの実行はまだ禁止されている。

更に、Uniform weightingの仮定は実際のアプリケーションでは通常無効であり、モデルの予測性能を劣化させる。
＝＞このため、Uniform Weightingに依存しない、効率的なImplicit MF法を設計する事が必要。

## 3.3. Generic Element-wise ALS Learner

これまでのALS解法のBottleneckは、user latent vectorとitem latent vectorの更新の際に発生する逆行列の計算である。

なので、「要素レベル(=ベクトルレベルではなく??)でパラメータを最適化する」のは自然な考え。（＝逆行列の計算が不要だから??）
latent vectorの各要素(＝座標, coordinate)を最適化し、他の座標は固定とする。
これを実現する為に、まず、目的関数である式(2)の微分を求める。

$$
\frac{\partial J}{\partial p_{uf}}
= -2 \sum_{i=1}^N (r_{ui} - \hat{r}_{ui}^f)
+ 2 p_{uf} \sum_{i=1}^N w_{ui} q_{if}^2 + 2 \lambda p_{uf}
$$

ここで、

- $\hat{r}_{ui}^f = \hat{r}_{ui} - p_{uf} q_{if}$. 言い換えれば、latent factor の一要素 (添字$f$)を含めない場合の予測値$\hat{r}$

この微分式=0とすると、$p_{uf}$の解が得られる。

$$
p_{uf} = \frac{
    \sum_{i=1}^N (r_{ui} - \hat{r}_{ui}^f) w_{ui} q_{if}
}{
    \sum_{i=1}^N w_{ui} q_{if}^2 + \lambda
}
\tag{5}
$$

同様に、item latent factorの解析解も得ることができる。

$$
q_{if} = \frac{
    \sum_{u=1}^M (r_{ui} - \hat{r}_{ui}^f) w_{ui} p_{uf}
}{
    \sum_{u=1}^N w_{ui} p_{uf}^2 + \lambda
}
\tag{6}
$$

他のパラメータを固定した状態で、あるパラメータを最適化するclosed-formな解法が与えられると、アルゴリズムは共同最適(a joint optimum)に達するまで、全てのモデルパラメータに対してそれを繰り返し実行する。
目的関数が非凸である為、勾配が損失する臨界点がlocal minimam(局所最小解)になる事がある。

### 3.3.1. Time Complexity

上述したように、要素レベルでパラメータ最適化を行う事で、サイズの大きい(expensiveな)行列の**逆行列の計算を回避**する事ができる。

＝＞これにより、一回の反復(=MFの全てのパラメータの一回更新)にかかる
Time Complexityは$O(M N K^2)$となり、$O(K^3)$の項を排除することで直接的にALSを高速化できる。

さらに、$\hat{r}_{ui}$を事前計算する事で、$\hat{r}_{ui}^f$を$O(K)$ではなく$O(1)$で計算する事ができる！
＝＞そのため、**一回の反復(=MFの全てのパラメータの一回更新)にかかる
Time Complexityは$O(M N K)$となり**、全てのuser × itemの評価値$\hat{r}_{ui}$を予測するのと同じになる。

# 4. Our Implicit MF Method

我々はまず，**欠損データに対するアイテム指向の重み付けを提案**し，それに続いて，推薦タスクに対して一様な重み付けよりも効果的な，**人気を考慮した重み付け戦略**を提案する．
次に、**目的関数を最適化する高速なeALSアルゴリズム**を開発し、従来のALS[12]や汎用要素別ALS学習器[26]と比較して、学習量を大幅に削減する。
最後に、**リアルタイムオンライン学習のための学習アルゴリズムの調整方法**について述べる。

## 4.1. Item-Oriented Weighting on Missing Data 欠損データに対するアイテム指向の重み付け

- アイテム空間が広い為、ユーザにとってのmissing entriesは、**否定的なフィードバック(negative feedback)と未知のフィードバック(unknown feedback)が混在**している。

  - =>よって、missing entriesに対して重み$w_{ui}$を指定する際、**negative feedbackに高い重みを割り当てる**ことが望まれる。
  - しかし、この２つのケースを区別することは自明だが困難。(=>implicitだから当然！)
  - また、通常、Interaction Matrix(Rating Matrix)$R$は非常に大きく、スパースである為、**各ゼロ要素に個別の重みを格納するのはあまりにも時間がかかりすぎる**！
  - ＝＞よって既存の研究では、**ゼロ要素に対して単純な一様重みを適用**している。しかしこれは実際のApplicationでは最適ではなく、拡張も不可能。

- コンテンツ提供者が**アイテム側のネガティブな情報(ex. どのアイテムがユーザに宣伝されたがInteractionが少ないか？)**にアクセスしやすい事を考慮すると...
  - => **何らかのアイテムの特性に基づいて欠損データを重みづけする**方法が現実的では？？

これを捉える為に、この論文では、**より細かい目的関数**を以下のように考案する。

$$
L =
\sum_{(u,i)\in \mathcal{R}}{w_{ui}(r_{ui} - \hat{r}_{ui})^2}
+ \sum_{u=1}^M \sum_{i \notin \mathcal{R}_u} c_i \hat{r}_{ui}^2
\\
+ \lambda (\sum_{u=1}^M ||p_u||^2 + \sum_{i=1}^N ||q_i||^2)
\tag{7}
$$

ここで、

- $c_i$: usersによって見逃されたアイテム$i$が、真にnegativeな評価なのかを表すConfidence(確信度).
  - コンテンツの実務者からのドメイン知識を符号化(encode)する為の手段として機能する事ができる。
- 右辺第一項は非ゼロ要素、第二項はゼロ要素のentitiesの２乗誤差を表している。＝＞**通常の目的関数をより分割(細かく)している**！
  - 非ゼロ要素の重み(Confidence?)は$u, i$のペア毎にユニークな値。
  - ゼロ要素の重みは$i$に対してのみユニークな値。

続いて以下で、ドメインに依存しない$c_i$を決定する戦略を提示する。

### 4.1.1. Popularity-aware Weighting Strategy 人気を考慮した重み付け戦略

- 多くのWeb2.0システムの既存のビジュアルインターフェース(=GUI？)では、人気のあるアイテムがレコメンデーションで表示される。
  - ＝＞他の全ての要因が同じであれば、人気のあるアイテムは一般的にユーザに知られている可能性が高い。
  - ＝＞従って、**人気のあるアイテムに関するentitiesの欠損(＝Interaction Matrixのゼロ要素)は、ユーザにとって本当に無関心である可能性が高い**と考えるのは合理的。
  - この効果を考慮し、アイテムの人気度に基づいて、Confidence $c_i$をparametrizeする。

$$
c_i = c_0
\frac{f_{i}^{\alpha}}{\sum_{j=1}^N f_{j}^{\alpha}}
\tag{8}
$$

ここで、

- $f_{i}$:Implicit Feedbackにおける**頻度** $\frac{|\mathcal{R}_i|}{\sum_{j=1}^N |\mathcal{R}_j|}$ によって与えられる、アイテム$i$の人気度。
- $c_0$:全てのゼロ要素の重み(Confidence)を決定する。ハイパーパラメータ？
- $\alpha$:不人気アイテムに対する人気アイテムの有意性(Significance level)を制御する。
  - ハイパーパラメータ?
  - $\alpha > 1$の時、人気アイテムの重みが促進されて、不人気アイテムに対する差が強化される。
  - $0 < \alpha < 1$の時、人気アイテムの重みが抑制されて平滑化効果がある。
  - 経験的には、$\alpha=0.5$が良い結果をもたらす？
  - なお、**$\alpha=0$とすると**、$w_0 = \frac{c_0}{N}$となり、**ゼロ要素に対する一様な重み付け**となる。

### 4.1.2. Relationship to Negative Sampling

- 提案するPopularity-aware weighting strategyは、RendleのBPR学習におけるPopularity-based oversampling[24]と直観的に同じであり、**基本的に人気のあるものを高い確率で否定的なフィードバックとしてサンプリングする**もの。
  - ＝＞要するに、**重み付けするのと、データをオーバーサンプリングする事は意味合いは同じ！って事**。Unbalancedなクラス分類問題と似てる感じ？？
- 本研究で提案する**eALS学習器は、各モデルパラメータを厳密に最適化**することにより、これらの学習問題を回避している。

## 4.2. Fast eALS Learning Algorithm 高速なeALSアルゴリズム

重み付きのゼロ要素によってもたらされる膨大な繰り返し計算を避ける事で、学習を高速化できる。
以下に$p_{uf}$の導出過程を詳述する。$q_{if}$の導出過程も同様。

まず第一に、3.3「Generic Element-wise ALS Learner」で導出した$p_{uf}$の更新式(式(5))を、観測データ部分を「非ゼロ要素＋ゼロ要素」に分離して書き直す(式(5'))：

$$
p_{uf} =
\frac{\sum_{i=1}^N (r_{ui}-\hat{r}_{ui}^f) w_{ui}q_{if}}
{\sum_{i=1}^N w_{ui}q_{if}^2 + \lambda} \\
= \frac{
    \sum_{i\in \mathcal{R}_u}(r_{ui}-\hat{r}_{ui}^f) w_{ui}q_{if}
    - \sum_{i \notin \mathcal{R}_u} \hat{r}_{ui}^f c_i q_{if}
}{
\sum_{i \in \mathcal{R}_u} w_{ui}q_{if}^2
+ \sum_{i \notin \mathcal{R}_u} w_{ui}q_{if}^2
+ \lambda
}
\tag{5'}
$$

(**右辺分子の第二項の符号マイナスは、任意の$i \notin \mathcal{R}_u$)において$r_{ui}=0$だから**！！結局は$\sum$を分割しただけ！！）

上式を見ると、明らかに、計算上のボトルネックは欠損データに対する和の部分にあり、これは負の空間全体をトラバースする必要がある。

- トラバース：
  - 直訳：横切る。横断する。
  - 登山にて、**尾根道やピークを避ける為**に、山の斜面を登らずに山腹・斜面を横断すること。
  - ＝＞計算量を減らす為に工夫が必要！って事？？？

まず、分子に注目する。

$$
\sum_{i \notin \mathcal{R}_u} \hat{r}_{ui}^f c_i q_{if}

= \sum_{i}^N c_i q_{if} \sum_{k \neq f}p_{uk}q_{ik}
- \sum_{i \in \mathcal{R}_u}\hat{r}_{ui}^f c_i q_{if}
\\
= \sum_{k \neq f}p_{uk} \sum_{i}^N c_i q_{if} q_{ik}
- \sum_{i \in \mathcal{R}_u}\hat{r}_{ui}^f c_i q_{if}
\tag{9}
$$

この式変形により、主要な計算である「全アイテムについて反復する$\sum_{i}^N c_i q_{if} q_{ik}\sum_{i}^N c_i q_{if} q_{ik}$」は、ユーザ$u$に依存しない事が分かる。
＝＞これをメモ化することで、異なるユーザーの潜在的要因を更新する際の不必要な計算の繰り返しを無くし、大幅な高速化を達成することができる。

$S^q$キャッシュを、$S^q = \sum_{i}^N c_i q_i q_i^T$と定義し事前に計算する事で、全てのユーザiに対してuser latent vector $u_i$(or factor $u_{if}$)を更新する際に使用できる。
すると、式(9)は次のように評価できる：

$$
\sum_{i \notin \mathcal{R}_u} \hat{r}_{ui}^f c_i q_{if}
= \sum_{k \neq f}p_{uk} s_{fk}^q
- \sum_{i \in \mathcal{R}_u}\hat{r}_{ui}^f c_i q_{if}
\tag{10}
$$

これは、時間計算量$O(K + |\mathcal{R}_u|)$で実行できる。

同様に、分母(denominator)の計算を高速化する為に$S^q$キャッシュを適用できる。

$$
\sum_{i \notin \mathcal{R}_u} c_{i} q_{if}^2
= \sum_{i=1}^N c_i q_{if}^2 - \sum_{i \in \mathcal{R}_u} c_i q_{if}^2
\\
= s_{ff}^q - \sum_{i \in \mathcal{R}_u} c_i q_{if}^2
\tag{11}
$$

上記のメモ化(事前計算)戦略をまとめると、$S^q$キャッシュを使用した$p_{uf}$の更新式は以下のようになる。

$$
p_{uf} =
\frac{
    \sum_{i\in \mathcal{R}_u}(r_{ui}-\hat{r}_{ui}^f) w_{ui}q_{if}
    - \sum_{i \notin \mathcal{R}_u} \hat{r}_{ui}^f c_i q_{if}
}{
\sum_{i \in \mathcal{R}_u} w_{ui}q_{if}^2
+ \sum_{i \notin \mathcal{R}_u} w_{ui}q_{if}^2
+ \lambda
} \\
\because \text{式10と11を代入して...}
\\
= \frac{
    \sum_{i\in \mathcal{R}_u}(r_{ui}-\hat{r}_{ui}^f) w_{ui}q_{if}
    - (\sum_{k \neq f}p_{uk} s_{fk}^q
- \sum_{i \in \mathcal{R}_u}\hat{r}_{ui}^f c_i q_{if})
}{
\sum_{i \in \mathcal{R}_u} w_{ui}q_{if}^2
+ (s_{ff}^q - \sum_{i \in \mathcal{R}_u} c_i q_{if}^2)
+ \lambda
}
\\
= \frac{
    \sum_{i\in \mathcal{R}_u}
    [w_{ui}r_{ui} - (w_{ui}- c_{i})\hat{r}_{ui}^f]q_{if}
    - \sum_{k \neq f}p_{uk} s_{fk}^q
}{
\sum_{i \in \mathcal{R}_u} (w_{ui} - c_i)q_{if}^2
+ s_{ff}^q
+ \lambda
}
\tag{12}
$$

同様に、$S^p$キャッシュを定義して、$q_{if}$の更新式を改良する事ができる。

$$
q_{if} = \frac{
    \sum_{u\in \mathcal{R}_i}[w_{ui}r_{ui}-(w_{ui}-c_i)\hat{r}_{ui}^f]p_{uf} - c_i \sum_{k\neq f} q_{ik} s^p_{kf}
}{
    \sum_{u \in \mathcal{R}_i}(w_{ui}-c_i)p_{uf}^2 + c_i s^p_{ff} + \lambda
}
\tag{13}
$$

ここで、

- $s^p_{kf}$：$S^p$キャッシュの$(k, f)$要素。ここで、$S^p = P^T P \in R^{K \times K}$で定義されている。

アルゴリズム1は、我々の**element-wise ALS learner（eALS, 要素別ALS学習器）のaccelerated algorithm(高速化アルゴリズム)**をまとめたものである。収束(=ALSの終了)のためには、訓練集合の目的関数の値を監視するか、ホールドアウトした検証データで予測性能を確認することができる。

![](../images/2022-07-30-19-32-34.png)

### 4.2.1. Discussion

#### 4.2.1.1. Time Complexity

- eALSアルゴリズム(アルゴリズム1)において、ある一つのuser latent factor $p_{uf}$のTime Complexityは$O(K + |\mathcal{R}_u|)$
- ＝＞よって、1 iteration分のeALSのTime Complexityは、$O((M+N)K^2 + |\mathcal{R}|K)$
- table 1に Implicit feedbackの為の他のMFアルゴリズムのTime Complexityをまとめた。
  - ![](../images/2022-08-06-16-45-55.png)

※ちょっとこの部分の導出チェックしてみる

- ある一ユーザのuser latent vectorのTime Complexityは...
  - $K \times O(K + |\mathcal{R}_u|) = O(K(K + |\mathcal{R}_u|))$
- user latent matrix(=全ユーザのuser latent vector)のTime Complexityは...（各ユーザuの$|\mathcal{R}_u|$は異なるので...）
  - $\sum_{u=1}^M O(K(K + |\mathcal{R}_u|)) = O(MK^2 + K \sum_{u=1}^M |\mathcal{R}_u|)$
  - $= O(MK^2 + K |\mathcal{R}|)$
- 上と同様に考えると、item latent matrix(= 全アイテムのitem latent vector)のTime Complexityは...
  - $\sum_{i=1}^N O(K(K + |\mathcal{R}_i|)) = O(NK^2 + K \sum_{i=1}^N |\mathcal{R}_i|)$
  - $= O(NK^2 + K |\mathcal{R}|)$
- 従って、eALS 1 iteration分のTime Complexityは...
  - $O(MK^2 + K |\mathcal{R}|) + O(NK^2 + K |\mathcal{R}|)$
  - $= O((M + N) K^2 + 2 \times K|\mathcal{R}|) = O((M + N) K^2 + K|\mathcal{R}|)$
  - 確か$O$記法において、定数倍は無視できるので！

他MF手法とのTime Complexity比較：

- bector-wise ALSと比較すると、本論文のelement-wise ALSはK倍高速である事がわかる。
- 更に、eALSはRCDと同じ時間計算量であり、もう一つの最新の解決策であるi-SVDよりも高速である。
- RCDに関して：
  - 全データに基づくMFの為の最新の学習機。
  - ランダムに選ばれたlatent vectorに対して勾配降下ステップ(gradient descent step)を実行する。
  - 適切な学習率をハイパーパラメータとして指定する必要がある。
  - eALSのRCDに対する大きな利点：
    - 各パラメータ更新における厳密な最適化により、学習率の必要性を回避できることであり、間違いなくRCDよりも効果的で使い勝手が良い！＝＞要するにハイパーパラメータとして指定する必要がない！
- 最も効率的なアルゴリズムはBPR
  - サンプリングされた部分的な欠損データに対してのみSGD学習器を適用するもの。
  - ＝＞つまり、全てのInteractionのデータを使用しないから早い？？

#### 4.2.1.2. Computing the Objective Function

eALSにおける目的関数(式(7))の再掲：

$$
L =
\sum_{(u,i)\in \mathcal{R}}{w_{ui}(r_{ui} - \hat{r}_{ui})^2}
+ \sum_{u=1}^M \sum_{i \notin \mathcal{R}_u} c_i \hat{r}_{ui}^2
\\
+ \lambda (\sum_{u=1}^M ||p_u||^2 + \sum_{i=1}^N ||q_i||^2)
\tag{7}
$$

目的関数の値を評価する事は、Iteration（反復計算）のConvergence（収束）を確認し、また実装の正しさを検証する為に重要である。

- 直接計算すると、$O(M N K)$の時間がかかり、rating matrix(Interaction matrix)$R$の完全な推定が必要。
- 幸いな事に、Item-oriented weighting(アイテム指向の重み付け)を用いれば、同様に$R$の疎密を利用して高速化する事ができる。

これを実現する為に、大きなコスト(Time Complexity)の原因である欠損データ部分の損失を再計算する：

$$
\sum_{u=1}^M \sum_{i \notin \mathcal{R}_u} c_i \hat{r}_{ui}^2
= \sum_{u=1}^M p_{u}^T S^q p_u
- \sum_{u, i \in \mathcal{R}} c_i \hat{r}_{ui}^2
\tag{14}
$$

パラメータ更新式の高速化の処理でキャッシュしていた$S^q$と、予測キャッシュ$\hat{r}_{ui}$を再利用する事で、直接計算するよりもはるかに早い$O(|\mathcal{R} + M K^2|)$のTime Complexityで目的関数を計算できる！

#### 4.2.1.3. Parallel Learning

eALSのIterationは簡単に並列化できるらしい！

- 第一に、$S$キャッシュの計算
  - (アルゴリズム1における４行目と１２行目)
  - ＝＞標準的な行列の計算
- 第二に、異なるユーザのuser latent vectorの更新：
  - (５~11行目)
  - 更新式中の共有するパラメータは...
    - 互いに独立(?)(i.e. $\hat{r}_{ui}$)
    - もしくは、変化しない(i.e. $S^q$)
  - ＝＞ユーザ毎の更新処理を分離しても、厳密な並列解が得られる！
  - ＝＞つまり、異なるworkers(=CPUとか？)に、分離されたユーザ集合のモデルパラメータを更新させる事ができる！
- 第三に、異なるアイテムのitem latent vectorの更新：
  - user latent vectorと同様に、並列計算できる。

これは、commonly-used SGD learner(一般に用いられるSGD学習器=**確率的勾配降下法, stochastic gradient descent**。訓練インスタンスが与えられた時にモデルのパラメータを更新する確率的手法)に対する、eALSのAdvantageである。

- SGDでは、異なる勾配ステップが互いに影響しあう可能性があり、異なるユーザ・アイテムのパラメータ更新を分離する正確な方法は存在しないらしい...。
  - 並列化によって生じる可能性のある損失を抑制するための高度な戦略が必要となる[7]
- 我々の提案するeALSは、座標降下法により最適化を行い、各ステップで専用のパラメータを更新することで、近似的な損失なしに恥ずかしいほど並列化されたアルゴリズムを実現する。
- 座標降下 vs 勾配降下??「座標降下」ってなんだっけ?
  - 座標降下＝＞目的関数を一つの変数(パラメータ)ずつ最適化する事？＝要するにALSとか？
  - それに対して、勾配降下＝＞各変数(パラメータ)毎に目的関数に対する勾配を求めて、一斉に最適化する事？

## 4.3. Online Update

- 実際には、レコメンダーモデルはオフラインで過去のデータから学習された後、**オンラインで使用され、ユーザに最適なサービスを提供するために適応**する必要がある。
- ここでは、新しいユーザとアイテムのインタラクションが与えられると、モデルのパラメータをリフレッシュするオンライン学習シナリオを考える。

### 4.3.1. Incremental Updating

- $\hat{P}$と$\hat{Q}$をオフライン学習で学習したモデルパラメータ(user latent matrix と item latent matrix)とし、$(u, i)$をstream inされた新しいInteractionを表すとする。
- 新しいInteractionを考慮してモデルパラメータを近似する為に、**$p_u$と$q_i$についてのみ最適化ステップを実行**する。
  - この時、新しいInteractionはglobalな観点からは$\hat{P}$と$\hat{Q}$をあまり変化させないが、$u$と$i$についてはlocalな特徴を大きく変化させることが前提である。
  - 特に、uが新規ユーザの場合、局所更新を実行する事で$p_u$を$q_i$に近づける（＝**ベクトル間の類似度を高める**!）事ができ、**latent factor model の期待値に合致する(?)**新アイテムの場合も同様！
    - $p_u$と$q_i$のベクトル間の類似度が高い程、その内積=評価値の推定値$\hat{r}_{ui}=p_u^T q_i$は大きな値になる！

以下のアルゴリズム2はeALSの漸進的な学習戦略をまとめたものである。
停止基準については、我々の経験則によれば、通常1回の繰り返しで十分な結果が得られる。
さらに、latent vectorsを更新した後、それに応じてSキャッシュを更新する必要があることに留意することが重要である。

![](../images/2022-08-06-16-08-51.png)

### 4.3.2. Weight of New Interactions 新規Interactionの重み付け

- Online 学習において、新しいInteractionはユーザの短期的な興味(Interest)をより反映したものとなる。
- ＝＞Offline学習で使用される過去のInteractionに比べ、**新しいInteractionのデータはユーザの将来の行動を予測する為に高いWeightを割り当てるべき**である。
- ＝＞そこで、各新規Interactionに重み$w_{new}$を設定し(上のアルゴリズム2の4行目)、調整可能(Tunable)なHyper Parameterとする。
  - 後述の５．３節では、このハイパラの設定がOnline学習の性能にどのような影響を与えるかについて検討する。

### 4.3.3. Time Complexity

- 新規Interaction$(u,i)$に対する逐次更新(Incremental Update)は、Time Complexity $O(K^2 + (|\mathcal{R}_u| + |\mathcal{R}_i|)\times K)$で実行可能。
  - このコストは、$u$と$i$のそれぞれの観測されたInteractionの数（$|R_u| と|R_i|$）に依存する。
  - 一方で、「Interactionの総数（$|\mathcal{R}|$）、ユーザ数$M$、アイテム数$N$には依存しない！」
- この**局所的(localized)なTime Complexity**は、**data dependencies(データ依存性??)**を扱う複雑なSoftware stackを避ける事ができる為、Online learing alogrithmのIndustrial useでのDeployment(展開、適用、採用？)に適している。

# 5. Experiments

## 5.1. Experimental Settings

## 5.2. Offline Protocol

## 5.3. Online Protocol

# 6. Conclusion and Future Work
