## 0.1. link

- https://arxiv.org/abs/1708.05024

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

モデルパラメータを推定する為に、Hu et al. は、Implicitフィードバック行列$R$の各予測に**信頼度Confidence**を関連付ける、weighted regression functionを(目的関数として！！)導入した。

$$
J = \sum_{u=1}^M \sum_{i=1}^N w_{ui}(r_{ui} - \hat{r}_{ui})^2
+ \lambda(\sum_{u=1}^M ||\mathbf{p}_u||^2
+ \sum_{i=1}^N ||\mathbf{q}_i||^2)
\tag{2}
$$

ここで、
- $w_{ui}$: the weight of entry $r_{ui}$. and we use $W=[w_{ui}]_{M\times N}$
- $\lambda$: the strength of regularizationをコントロールする。

ImplicitフィードバックのMFでは、通常、欠落したentriesにはruiの値はゼロだが、**wuiの重みはゼロでないものが割り当てられ**、どちらも性能にとって重要であることに注意されたい。


## 3.2. Optimization by ALS

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

＝＞latent vectorの次元数$K$の大きさは、より良い汎化性、ひいてはより良い予測性能につながる為、非常に重要なハイパーパラメータである。
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

### 4.1.1. Popularity-aware Weighting Strategy 人気を考慮した重み付け戦略

### 4.1.2. Relationship to Negative Sampling

## 4.2. Fast eALS Learning Algorithm 高速なeALSアルゴリズム

### 4.2.1. Discussion

#### 4.2.1.1. Time Complexity

#### 4.2.1.2. Computing the Objective Function

#### 4.2.1.3. Parallel Learning

## 4.3. Online Update

### 4.3.1. Incremental Updating

### 4.3.2. Weight of New Interactions

### 4.3.3. Time Complexity

# 5. Experiments

## 5.1. Experimental Settings

## 5.2. Offline Protocol

## 5.3. Online Protocol

# 6. Conclusion and Future Work
