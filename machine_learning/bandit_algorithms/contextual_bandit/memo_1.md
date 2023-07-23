## refs

- https://qiita.com/usaito/items/e727dcac7325b50d4d4c#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB

# Contextual Banditとは

context(ユーザ特徴、アイテム特徴、etc.)によって、各arm(選択肢、action、何を推薦するか)の報酬構造が変化する、というアイデア。
具体的には、各armで得られる**報酬に対して仮定した確率分布のパラメータ**を、contextに応じて変化させる。これにより、より効率的に得られる報酬を最大化できるだろう、という想定。

## 仮定

時刻 $t$ における あるarm $a$ からの報酬 $r_{t, a}$ は、既知同一分散 $\sigma^{2}$ を持つ正規分布に従うと仮定する(Linear Stochastic Bandit).
この時、Contextual Banditは以下の様に報酬をモデル化する.

$$
r_{t, a} = \theta^{T}_{a} \mathbf{x}_{t, a} + \epsilon_{t},
\\
\epsilon_{t} \sim^{i.i.d.} Norm(0 | \sigma^2)
\tag{1}
$$

よって、時刻 $t$ におけるarm $a$ からの報酬 $r_{t, a}$ は以下。

$$
r_{t, a} \sim Norm(\theta^{T}_{a} \mathbf{x}_{t, a} | \sigma^2)
$$

おそらく $\theta^{T}_{a} \mathbf{x}_{t, a}$ の部分は、任意の決定論的関数 $f_{\theta}(\mathbf{x}_{t, a})$ に一般化できるのでは??:thinking:
(->じゃあ決定論的な推薦モデルを、確率的な推薦モデルに拡張するのってそこまで困難じゃないかも??:thinking:)

Contextual Banditは報酬の確率分布に関するモデルパラメータを逐次的に推定する(arm選択 -> 報酬を取得 -> パラメータ更新 -> arm選択...を繰り返す??)。
時刻$t$の度に、context情報 $\mathbf{x}_{t, a}$ を用いて各armの報酬の確率分布を推定し、次に選択するarmを選択する。

# 最も基本的なアルゴリズムを3つ紹介

## LinUCB (Linear Model × Upper Confidence Bound Bandit)

Contextual Bandit の草分け的論文。

以下の疑似コードのアルゴリズムで、各time step $t$ にarmを選択しながら、観測される報酬とcontext情報から線形モデルのパラメータ $\hat{\theta_{a}}$ を逐次的に更新していく.

![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F236331%2F1da758cc-d26b-1965-1e13-c40e26409340.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=16718b2f4e384ad9a1f8acc49c1ff38e)

ここで時刻 $t$ における線形パラメータの推定値は以下のように導かれる(最小二乗法??):

$$
\hat{\theta}_{a} = \argmin_{\theta} \sum_{s=1}^{t} (r_{s,a} - \theta_{a}^{T} \mathbf{x}_{s,a})^2
$$

- LinUCBは各時刻 $t$ において、報酬の不偏推定値 $\hat{\theta}_{a}$ に、推定値の標準偏差 $\sqrt{\mathbf{x}_{t, a}^{T} A_{a}^{-1} \mathbf{x}_{t,a}}$ の $\alpha$ 倍を足した値が最も大きくなるarmを選択する.
- $\alpha$ はハイパーパラメータ。大きいほど探索を、小さいほど活用を重視する.

## LinTS (Linear Model × Thompson Sampling Bandit)

- Thompson Sampling Bandit の Contextual Bandit への拡張.
- 各armの報酬のモデル式は LinUCBと同様に線形モデル.
- A_t_a, b_t_aの更新式もLinUCBと同じ。
- $\theta$ の推定方法がベイズっぽい感じ。

## 目的変数がbinaryの場合の報酬モデル式:

$$
\mathbb{P}(r_{t,a} = 1)
= sigmoid(\theta_{a}^T \mathbf{x}_{t,a})
$$

- ただ結局、最適なarmを選ぶ戦略はLinUB等と同じ感じ.
-
