## 0.1. link

- https://arxiv.org/abs/1708.05024

## 0.2. Abstract

# 1. Introduction

# 2. Related Work

# 3. Preliminaries

## 3.1. MF method for Implicit Feedback

## 3.2. Optimization by ALS

### 3.2.1. Efficiency Issue with ALS

### 3.2.2. Speed-up with Uniform Weighting

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

- $\hat{r}_{ui}^f = \hat{r}_{ui} - p_{uf} q_{if}$. 言い換えれば、latent factor の一要素 $f$なしの予測値$\hat{r}$

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
