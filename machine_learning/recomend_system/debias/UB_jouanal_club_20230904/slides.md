---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: ABテストする前に機械学習モデルの性能を確度高く評価したいけど、皆どうやってるんだろう?について色々調べている話
subtitle: 論文読み会
date: 2023/09/04
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 参考文献:

- usaitoさんの資料: [Off-Policy Evaluationの基礎とOpen Bandit Dataset & Pipelineの紹介](https://speakerdeck.com/usaito/off-policy-evaluationfalseji-chu-toopen-bandit-dataset-and-pipelinefalseshao-jie)
- 大規模行動空間におけるOPEの論文: [Off-Policy Evaluation for Large Action Spaces via Embeddings](https://arxiv.org/pdf/2202.06317.pdf)
- 複数のオフラインmetricsからオンライン性能を予測する論文: [Predicting Online Performance of News Recommender Systems Through Richer Evaluation Metrics](https://dl.acm.org/doi/10.1145/2792838.2800184)
- netflixのtechブログ: [Innovating Faster on Personalization Algorithms at Netflix Using Interleaving](https://netflixtechblog.com/interleaving-in-online-experiments-at-netflix-a04ee392ec55)
- naiveだけど有効なオフライン評価方法をしてた contextual bandit の論文: [A contextual-bandit approach to personalized news article recommendation](https://arxiv.org/pdf/1003.0146.pdf)

## 今回のテーマを選んだ経緯

- 推薦や広告配信等の意思決定タスクに機械学習を適用する上で、オフライン評価とオンライン評価の結果の乖離問題がある。
-

## ABテストする前に機械学習モデルの性能を確度高く評価できたらどんな点が嬉しい?

:::: {.columns}

::: {.column width="50%"}

できる場合

- ABテスト前に有効そうな施策を絞り込む事ができ、仮説 -> 施策 -> 検証をより高速に回す事ができる。
- ハイパーパラメータチューニングができる。
- ユーザ体験を悪化させ得る施策を、オンライン環境に出す前に検知する事ができる。

:::

::: {.column width="50%"}

できない場合

- 全ての仮説に対してABテストする必要があり、仮説 -> 施策 -> 検証の速度が下がる。(ABテストの運用コストを下げても、どうしてもオフライン実験するよりは時間がかかる。10倍くらい?)
- 誤った基準でハイパーパラメータチューニングしてしまう可能性。
- ユーザ体験を悪化させ得る施策を、オンライン環境に出す可能性。

:::

::::

## 色々調べたオフライン評価の確度をあげるアプローチ達

- 1. Off-Policy Evaluation手法を用いて過去のログデータからオンライン性能を推定(@ ファッションアイテムの推薦)
- 2. 力技っぽい!: オフライン観測可能なmetricsからオンライン性能を予測する回帰モデルを作る(@ ニュース記事の推薦)
- 3. naiveだけど導入しやすさと効果は高そう: 一定期間のみ、一様ランダムなモデルを本番適用してログデータ収集 (@ ニュース記事の推薦)
- 4. より高速なオンライン評価手法 Interleaving をABテストの前に導入する(@ 動画の推薦)

今日は主にアプローチ1について紹介し、アプローチ2 ~ 4はさらっと紹介程度の予定。

# 調べた方法1. Off-Policy Evaluation 手法を用いて過去のログデータからオンライン性能を推定(@ ファッションアイテムの推薦)

- 自分はusaitoさん & wantedlyさんの勉強会に参加してこのOff-Policy Evaluation(以下、OPE) 分野を知った。
- 今回は概要紹介 & 自分の感想を話すので、更に詳しくはusaitoさんの資料やOPE関連の論文を読むと良さそう!

## Off-Policy Evaluation(OPE)とは?

OPEは新しいpolicyを製品に導入することなく、その性能を正確に評価する事を目的とした方法論。具体的には、稼働中の意思決定システム **logging policy $\pi_{0}$** で得たログを使って、施策 **target policy $\pi$** のオンライン性能を推定したい。

OPE文献で用いられるnotation

- $\mathbf{x} \in X$: contextベクトル(モデルに入力する特徴量...!)
- $a \in A$: 意思決定タスクにおいて選択される行動(action)。基本的には離散変数。$A$ は行動空間。
- $\pi(a|\mathbf{x})$: 意思決定policyが context $\mathbf{x}$ を受け取って行動 $a$ を選択する確率。
- $r \sim p(r|\mathbf{x}, a)$: 選択された行動に基づいて得られる報酬(reward)(ex. click, 購入, 翌週も継続利用してくれる)

強化学習っぽいnotation...!Off-Policy Learningという分野もあるっぽいし、 contextual banditを想定したOPE論文が多い印象...!:thinking:

## OPEが解きたい問題:

まず、任意の**意思決定policyの性能**を以下の様に定義(=要は報酬の期待値!:thinking:):

$$
V(\pi)
:= \mathbb{E}_{p(\mathbf{x})\pi(a|\mathbf{x})p(r|\mathbf{x},a)}[r]
= \mathbb{E}_{p(\mathbf{x})\pi(a|\mathbf{x})}[q(\mathbf{x},a)]
$$

ここで $q(\mathbf{x}, a) := \mathbb{E}[r|\mathbf{x}, a]$ は、あるcontext $\mathbf{x}$ において行動 $a$ を選択した場合の報酬 $r$ の期待値。
(ex. 報酬 $r$ をclickするか否かと定義した場合は、$V(\pi)$ はCTRになる:thinking:)

OPEでは、**$\pi_{0}$ で得られた過去の $n$ 個のログデータ $D := {(\mathbf{x}_i, a_i , r_i)}_{i=1}^{n}$ のみ**を用いて、($\pi_{0}$ とは異なる) **$\pi$ の性能 $V(\pi)$ を高い精度で推定したい**。その為にOPE推定量 $\hat{V}(\pi)$ を開発したい。

そしてOPE推定量の精度は、MSE(平均二乗誤差)によって定量化される:

$$
MSE(\hat{V}(\pi)) = \mathbb{E}_{D} [(V(\pi) - \hat{V}(\pi;D))^2]
$$

## 各OPE推定量を比較する為の視点: biasとvariance

OPE推定量の評価に用いるMSE(平均二乗誤差)は、以下の様に **$(推定量のbias)^2$ と $(推定量のvariance)$ に分解**できる。

$$
MSE(\hat{V}(\pi)) = \mathbb{E}_{D} [(V(\pi) - \hat{V}(\pi;D))^2]
\\
= Bias[\hat{V}(\pi)]^2 + \mathbb{V}_{D}[\hat{V}(\pi;D)]
$$

よって、**各OPE推定量の良し悪しを比較する際はbiasとvarianceに注目すると良い**らしい。
(ex. 推定量Aは biasは小さいがvarianceが大きい。推定量Bはbiasは大きいがvarianceが小さい)

## 代表的な3つのOPE推定量

基本的にこれら3つのOPE推定量が、OPE研究の基礎になっているらしい:

- DM(Direct Method)推定量
- IPS(Inverse Propensity Scoring)推定量
- DR(Doubly Robust)推定量

## 代表的なOPE推定量① DM(Direct Method)

:::: {.columns}

::: {.column width="60%"}

過去の観測データから**事前に報酬期待値 $q(\mathbf{x}, a) := \mathbb{E}[r|\mathbf{x}, a]$ の予測モデル $\hat{q}(\mathbf{x}, a)$ を学習しておき**、それをOPEに用いる。

$$
\hat{V}_{DM}(\pi;D) = \frac{1}{n} \sum_{i=1}^{n} \hat{q}(\mathbf{x}_{i}, \pi(\mathbf{x}_{i});D)
$$

- 特徴: OPEの精度が報酬予測モデル $\hat{q}$ に大きく依存する為、biasは大きい。一方でvarianceは小さい。
- ただそもそも精度の良い報酬予測モデル $\hat{q}$ を作れる時点で、それを使った意思決定policyを運用すれば良いので、OPEとしての実用性は低め。

:::

::: {.column width="40%"}

hoge

:::

::::

## 代表的なOPE推定量② IPS(Inverse Propensity Scoring)

:::: {.columns}

::: {.column width="60%"}

logging policy による**行動の選ばれやすさ(=propensity score) の逆数で観測報酬を重み付け**して、naiveな推定量のbiasを取り除く。

$$
\hat{V}_{IPS}(\pi;D) = \frac{1}{n} \sum_{i=1}^{n} \frac{\mathbb{I}[\pi(\mathbf{x}_{i}) = a_i]}{\pi_{0}(a_i|\mathbf{x}_i)} r_{i}
$$

- biasは小さい(=仮定を満たせば不偏)。
- varianceは大きく、データ $n$ が増える程小さくなっていく。
- 先進的なOPE推定量の多くが、このIPS推定量に基づいている。

:::

::: {.column width="40%"}

hoge

:::

::::

## 代表的なOPE推定量③ DR(Doubly Robust)

:::: {.columns}

::: {.column width="60%"}

DMとIPSを組み合わせた推定量。
DM推定量をベースラインとしつつ、報酬期待値予測モデル $\hat{q}$ の誤差をIPS重み付けで補正している。

$$
\hat{V}_{DR}(\pi;D) = \hat{V}_{DR}(\pi;D)
\\
+ \frac{1}{n} \sum_{i=1}^{n} (r_{i} - \hat{q}(\mathbf{x}_i, a_i)) \frac{\mathbb{I}[\pi(\mathbf{x}_{i}) = a_i]}{\pi_{0}(a_i|\mathbf{x}_i)}
$$

- 特徴: DM推定量の性質によりvarianceを抑えつつ、IPS推定量の性質(=仮定を満たせば不偏)を受けてbiasを小さくしている。

:::

::: {.column width="40%"}

hoge

:::

::::

## 大規模行動空間を持つ意思決定タスクでOPEが難しい問題

## IPS推定量の満たすべき仮定: Common Support Assumption

# 調べた方法2. 力技っぽい!: オフライン観測可能なmetricsからオンライン性能を予測する回帰モデルを作る(@ ニュース記事の推薦)

- hoge

# 調べた方法3. naiveだけど導入しやすさと効果は高そう: 一定期間のみ、一様ランダムなモデルを本番適用してログデータ収集 (@ ニュース記事の推薦)

- hoge

# 調べた方法4. より高速なオンライン評価手法 Interleaving をABテストの前に導入する(@ 動画の推薦)

- hoge
  $$
