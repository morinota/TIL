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

title: 推薦システムにおけるMNARデータを使った学習 & 検証において、因果推論の傾向スコアを用いて誤差関数を調整する事でbiasに対処する論文を読んだ
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
- published date: 17 Feb 2016,
- authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
- url(paper): [https://arxiv.org/abs/1602.05352](https://arxiv.org/abs/1602.05352)

## ざっくり論文概要

- 本論文は、推薦システムにおける**MNAR(Missing Not at Random)データ**を使った**学習 & 評価(検証)**において、因果推論の傾向スコアを用いて誤差関数を調整する事でbiasに対処しよう！という話だった.
- MNARデータに対する"学習のみ"や、"評価のみ"に焦点を当てた論文も多いが、本論文は両方に焦点を当てて汎用的なアプローチの提案を試みている印象.
- MNARデータを使ってそのままモデル性能(誤差関数)を推定しようとすると、真のモデル性能の値に対してbiasが発生してしまう. (不偏推定量でなくなってしまう.)
- そこで因果推論分野の**propensity score(傾向スコア)**を用いて、モデル性能の推定量を調整して、真のモデル性能の不偏推定量を作ろう...!!という話.
- ↑で作ったモデル性能の不偏推定量をモデル性能の評価(検証)や学習時の目的関数に使う事で、MNARデータにおいても**良い感じの推薦モデルを作れる・選べる**ようになるぞ...!という話.

# Introduction

## 推薦システムにおける選択バイアスとMNARデータ

- 推薦システムの学習用データ・検証用データは、実環境において多くの場合、**選択バイアス**がかかっている.
  - ex.1) 映画推薦システムにおいて、ユーザは自分の好きな映画を観て評価し、自分の嫌いな映画を評価する事はほぼない. ->**ユーザ自身の選択行動による選択バイアス**
  - ex.2) 広告配信システムにおいて、ユーザが興味を持ちそうな広告を表示するが、それ以外の広告を表示する頻度は低くなる. -> **推薦システムの動作による選択バイアス**
- 様々な選択バイアスに伴い開発者が得られるのは、観測/未観測の傾向が偏ったデータ = **MNAR(Missing Not At Random)**と呼ばれるデータになる.(Little & Rubin, 2002)

## 本論文の目的 & アプローチの概要

- 本論文の目的は、**選択バイアスによるMNARデータの元で**、原理的、実用的かつ効果的に推薦システムを評価(検証)・学習できるアプローチを開発する事.
- **推薦を因果推論の観点から見る**と、推薦システムでユーザにアイテムを見せることは、医学研究において患者に治療法を見せるのと同じような介入(intervention)である.
- **推薦と実験・観測データに対する因果推論を結びつけること**で、選択バイアス下での推薦システムの公平な評価と学習のための原則的なフレームワークを導き出す.

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

- 図1の左下 $\hat{Y}_1$ と中央下 $\hat{Y}_2$ は、ある推薦モデル1と2によって予測された評価行列を表す。

タスク1では，これらの予測された評価行列 $\hat{Y}$が，真の評価行列$Y$をどれだけ反映(予測)できたかを推定(評価)したい...!

## タスク1: 評価値の予測精度の推定

標準的な予測誤差の場合、次のように書くことができる. (**学習の場合は損失関数**として、**検証の場合は評価指標**として使用するイメージ...!)

$$
R(\hat{Y}) = \frac{1}{U \cdot I} \sum_{u=1}^{U} \sum_{i=1}^{I} \delta_{u,i}(Y, \hat{Y})
\tag{1}
$$

ここで、$\delta_{u,i}(Y, \hat{Y})$ は真の値 $Y$ と予測値 $\hat{Y}$ の差を表し、具体的な $\delta()$ 関数は採用するmetricによって異なる. 例えば hogehoge と fugafugaの場合は以下.

$$
\delta_{u,i}(Y, \hat{Y}) = hogehoge()
\\
\delta_{u,i}(Y, \hat{Y}) = fugafuga()
\\
\delta_{u,i}(Y, \hat{Y}) = piyopiyo()
$$

## タスク1: 評価値の予測精度の推定

しかし実環境では真の評価行列$Y$は一部の要素しか観測されない為、従来は以下の様に、**観測済みエントリ{u,i}のみを用いて** 予測誤差 $R(\hat{Y})$ を推定する.

$$
\hat{R}_{naive}(\hat{Y})
= \frac{1}{|{(u,i):O_{u,i} = 1}|} \sum_{(u,i):O_{u,i}=1} \delta_{u,i}(Y,\hat{Y})
\tag{5}
$$

ここで、$O_{u,i}$ は... を表すbinary確率変数とする.

$$
O(u,i)
$$

式(5)を、予測誤差 $R(\hat{Y})$ の**naive推定量**と呼ぶ. 実はこのnaiveさが、図1の $\hat{Y}_1$、$\hat{Y}_2$ に対する重大な誤判定を招いてしまう.

## naive推定量のbiasを確認する.

予測誤差 $R(\hat{Y})$ のnaive推定量の期待値を導出して、biasの発生を確認します!

$$
E_{O}[\hat{R}_{naive}(\hat{Y})] = E_{O}[\frac{1}{|{(u,i):O_{u,i} = 1}|} \sum_{(u,i):O_{u,i}=1} \delta_{u,i}(Y,\hat{Y})]
\\
= E_{O}[\frac{1}{|{(u,i):O_{u,i} = 1}|} \sum_{(u,i)} O_{u,i} \cdot \delta_{u,i}(Y,\hat{Y})]
\\
\because O_{u,i} \text{は観測されたか否かを表すbinary変数}
\\
= \frac{1}{|{(u,i):O_{u,i} = 1}|} \sum_{(u,i)} E_{O}[O_{u,i}] \cdot \delta_{u,i}(Y,\hat{Y})
$$

## naive推定量のbiasを確認する.

$$
E_{O}[\hat{R}_{naive}(\hat{Y})] = \frac{1}{|{(u,i):O_{u,i} = 1}|} \sum_{(u,i)} E_{O}[O_{u,i}] \cdot \delta_{u,i}(Y,\hat{Y})
$$

この導出結果から、naive推定量の期待値 $E_{O}[\hat{R}_{naive}(\hat{Y})]$ は、**ある特殊ケースを除いて、真の予測誤差 $R(\hat{Y})$ に比例しない**事が分かりました...!

特殊ケース: **全ての観測ペア(u,i)の観測されやすさ(観測確率)が一様なケース**. すなわち...!

$$
E_{O}[O_{u,i}] = const \in (0, 1] , \forall {(u,i):O_{u,i} = 1}
$$

$E_{O}[O_{u,i}]$ が全てのユーザ・アイテムペアで一様(1つの定数を取る)という条件はかなり強く、実環境ではなかなか 

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

##
