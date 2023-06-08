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

title: hogehogeな論文を読んだ
subtitle: n週連続推薦システム系論文読んだシリーズ 17週目
# date: 2023/06/02
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 論文の基本情報

- title: Recommendations as Treatments: Debiasing Learning and Evaluation
- published date: hogehoge September 2022,
- authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
- url(paper): [https://arxiv.org/abs/1602.05352](https://arxiv.org/abs/1602.05352)

## ざっくり論文概要

# Introduction

## 推薦システムにおける選択バイアスとMNARデータ

## 本論文の目的

## MNARデータの扱いに関する既存研究

## Propensity-based アプローチに関して

V

# 推薦システムの為のunbiasedな性能推定

# MNARデータが従来の学習・検証に与える影響

## 映画の例の説明1

映画の例で、選択バイアスが従来の評価に与える悲惨な影響について考えてみる.
$u \in {1，...，U}$をユーザidx、$i \in {1，...，I}$ を映画idxとする.

![](https://d3i71xaburhd42.cloudfront.net/e108e3925e5abf9423ec95fd634a3a9417fcc3eb/2-Figure1-1.png){fig-align="center"}

- 図1 左上の$Y$は、"ホラー好き"ユーザ集合は全てのホラー映画を5点、全てのロマンス映画を1点と評価する様な**真の評価行列** $Y \in \mathbf{R}^{U \times I}$ ("ロマンス好き"ユーザ集合は逆)

## 映画の例の説明2

![](https://d3i71xaburhd42.cloudfront.net/e108e3925e5abf9423ec95fd634a3a9417fcc3eb/2-Figure1-1.png){fig-align="center"}

- 図1 右上のbinary行列 $O \in  \{0, 1\}^{U \times I}$ は実際に評価が観測された{u,i}ペア. $[O_{u,i} = 1] ⇔ [Y_{u,i} \text{observed}]$ を意味する. ($O$はobservationの意味)

## 映画の例の説明3

![](https://d3i71xaburhd42.cloudfront.net/e108e3925e5abf9423ec95fd634a3a9417fcc3eb/2-Figure1-1.png){fig-align="center"}

- 図1 中央上の行列 $P$は、各{u,i}の評価が実際に観測される確率 $P_{u,i} = P(O_{u,i} = 1)$ を意味する. この映画の例では、**映画ジャンルの好き嫌いと評価値の観測されやすさに強い相関**がある。

## 映画の例の説明4

![](https://d3i71xaburhd42.cloudfront.net/e108e3925e5abf9423ec95fd634a3a9417fcc3eb/2-Figure1-1.png){fig-align="center"}

このデータについて、以下の二つのタスクの評価を考えてみる.

- タスク1: 評価値の予測精度の推定
- タスク2: 推薦の精度の推定

## タスク1: 評価値の予測精度の推定

![](https://d3i71xaburhd42.cloudfront.net/e108e3925e5abf9423ec95fd634a3a9417fcc3eb/2-Figure1-1.png){fig-align="center"}

- 図1の左下 $\hat{Y}_1$ と中央下 $\hat{Y}_2$は、ある推薦モデル1と2によって予測された評価行列を表す。

タスク1では，これらの予測された評価行列 $\hat{Y}$が，真の評価行列$Y$をどれだけ反映(予測)できたかを推定(評価)したい...!

## タスク1: 評価値の予測精度の推定

標準的なaccuracy metricの場合、次のように書くことができる.

$$
R(\hat{Y}) = \frac{1}{U \cdot I} \sum_{u=1}^{U} \sum_{i=1}^{I} \delta_{u,i}(Y, \hat{Y})
\tag{1}
$$

ここで、$\delta_{u,i}(Y, \hat{Y})$ は真の値と予測値の差を表し、具体的な $\delta()$ 関数は採用するmetricによって異なる.

しかし実環境では真の評価行列$Y$は一部の要素しか観測されない為、従来は以下の様に、**観測済みエントリ{u,i}のみを用いて**$R(\hat{Y})$を推定する.

$$
\hat{R}_{naive}(\hat{Y})
= \frac{1}{|{(u,i):O_{u,i} = 1}|} \sum_{(u,i):O_{u,i}=1} \delta_{u,i}(Y,\hat{Y})
\tag{5}
$$

これを、誤差関数 $R(\hat{Y})$ の**naive推定量**と呼ぶ. このnaiveさが、図1の$\hat{Y}_1$、$\hat{Y}_2$に対する重大な誤判定を招いてしまう.

## タスク1: 評価値の予測精度の推定

![](https://d3i71xaburhd42.cloudfront.net/e108e3925e5abf9423ec95fd634a3a9417fcc3eb/2-Figure1-1.png){fig-align="center"}

図1の例を見ると、$\hat{Y}_1$ の方が $\hat{Y}_2$ よりも予測精度が優れているはず.
しかしnaive推定量$\hat{R}_{naive}(\hat{Y})$は、$\hat{Y}_2$の方が予測誤差が小さいと判断してしまう...
これは**選択バイアスによるもの**であり、1点の評価は観測されにくい為、誤差関数のnaive推定量では過小評価される。
より一般的に言えば、選択バイアス(MNARデータ)下では、**naive推定量は真の誤差関数の不偏推定量ではない**(Steck, 2013). すなわち：

$$
E_{O}[\hat{R}_{naive}(\hat{Y})] \neq R(\hat{Y})
\tag{6}
$$

## タスク2: 推薦の精度の推定

![](https://d3i71xaburhd42.cloudfront.net/e108e3925e5abf9423ec95fd634a3a9417fcc3eb/2-Figure1-1.png){fig-align="center"}

タスク2では、予測評価値の精度ではなく、より直感的に**推薦するか否か**の意思決定の精度を評価する.
この為に$\hat{Y}$を再定義し、図1 右下の $\hat{Y}_3$ では、$O$ に類似したbinary行列として推薦結果を符号化している. ここで、$[\hat{Y}_{u,i} = 1]$ ⇔ [i が u に推薦される]とし、1ユーザあたりk件のみ推薦する.

## タスク2: 推薦の精度の推定

推薦の精度を評価するmetricsとして一般的なのは、ユーザが推薦された映画から得るCumulative Gain(累積利益, CG). 図1の例では、推薦映画リストの平均評価として定義する.
以下の $delta()$ を用いて、再び式(1)の誤差関数を定義する事ができる.

$$
CG: \delta_{u,i}(Y, \hat{Y}) = (I/k) \hat{Y} \cdot Y_{u,i}
\tag{7}
$$

- しかし、ユーザが$\hat{Y}$の全ての映画を視聴していない限り、式(1)を用いて直接CGを計算することはできない. (真の目的関数は計算できない。観測データから近似する他ない...)
- 従って、実際に観測された映画を見ていた(消費した)代わりに、推薦$\hat{Y}$に従って映画を消費した場合、ユーザは(CGの面で)どの程度楽しめただろうか、という**反実仮想的な問い**に直面する.
- CGの様に推薦結果を集合を見なすmetricだけでなく、割引累積利益(DCG)、DCG@k、Precision at k(PREC@k)などのranking metricsも同様の設定が当てはまる.

タスク1と同様に式(5)のnaive推定量を用いる方法もあるが、タスク2においてもnaive推定量は$R(\hat{Y})$の不偏推定量ではない.

# 推薦システムの誤差関数の推定量をどのように不偏にする??

## 因果推論のアプローチを使ってみようという話

$Y$の観測値が欠損している状況で推薦システムの性能の不偏推定値を得る為に、本論文では、因果推論の**average treatment effects**の推定方法を活用するアプローチを採用する.

推薦タスクを、ある薬で患者を治療するような介入(intervention)と同様に考えると、新しい治療方針(ex. 女性には薬Aを、男性には薬Bを与える = 新しい推薦結果$\hat{Y}$) の効果を推定したい.

どちらの場合も、**ある患者(i.e. ユーザ)がある治療(i.e. 映画)からどれだけ恩恵を受けたかについては部分的な知識しかなく**(すなわち、$O_{u,i} = 1$の $Y_{u,i}$のみ...!)、$Y$における潜在的な結果の大部分は未観測である、という課題がある.

## 選択バイアスを処理する鍵

## 2種類の観察パターン生成プロセス

## Propensity Score(傾向スコア)を使って推定量を調整する

## IPS Estimator

## 
