---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    scrollable: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: (RecSys2022 Best Papers)ニュース推薦の民主的役割を考慮した5つの多様性指標RADioの論文を読んで、推論品質の監視とかオフライン評価とかで色々使えないかなーと思いを馳せた話
subtitle: 2023/11/22 推薦システム論文読み会
# date:
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 参考文献:

- 1. メインの論文: [RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf)
- 2. メイン論文の元のやつ: [Recommenders with a Mission: Assessing Diversity in News Recommendations](https://dl.acm.org/doi/10.1145/3406522.3446019)
- 3. (メイン論文の背景にあるやつ!)ニュース推薦の民主的役割のtypologyを提案した論文: [On the Democratic Role of News Recommenders](https://www.tandfonline.com/doi/full/10.1080/21670811.2019.1623700)
- 4. Booking.comの論文: [150 Successful Machine Learning Models: 6 Lessons Learned at Booking.com](https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf)
- 5. News推薦のサーベイ論文: [News Recommender Systems - Survey and Roads Ahead](https://web-ainf.aau.at/pub/jannach/files/Journal_IPM_2018.pdf)
- 6. MLOpsの成熟度を高める為のガイドライン: [MLOps Maturity Assessment](https://mlops.community/mlops-maturity-assessment/)

## どんな論文? 選んだモチベーションは??

- 論文title:[RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf)
- RecSys2022 Best Paper Awards
- 一般的な推薦システムにおける"多様性"は、シンプルに推薦アイテム間の距離指標として表される事が多いが、ニュース推薦における"多様性"を検討する上では、それでは不十分でしょ！(というか、目指すべき点はそれではないでしょ!)って話。
- 本論文の目的は、コンピュータサイエンスにおける"多様性"と、メディアや民主主義の規範的な意味としての"多様性"のギャップを埋めること。
  - 規範的概念としての"多様性"を、異なるニュース推薦モデルの評価や比較に使用可能な5つのmetrics集合 RADio に落とし込む。
- この論文を読んだのは半年前なのですが、推薦モデルの推論品質の監視やオフライン評価に使えないかなーと思いを馳せ始め、皆さんと共有したく選択した。

## 導入: ニュース推薦の精度と多様性の話

> ニュース推薦アルゴリズムの仕事は、増え続けるオンライン情報を**フィルタリング**すること (by文献2)

フィルタリングの方針は、メディアが成したい使命によって異なる。

## 4種のメディアモデルとニュース推薦方針

既存研究では、メディアの民主主義的な使命を以下の**4種類**のメディアモデルとして分類:

- The Liberal(自由主義) model: コンテンツもスタイルも、**ユーザの好みに合わせて**提供する。
  - ユーザが選択した分野での専門性を高める。
- The Participatory(参加主義) model: ユーザが社会で活動するために必要な**共通認識**を、**各ユーザに分かりやすい形で**提供する。
  - ユーザ達が必ずしも同じ記事を見る必要はないが、同じトピック。記事のcomplexity(複雑さ)は、ユーザの好みや能力に合わせて調整。
- The Deliberative (議論主義) model: 現在、**社会的な議論の中心にあるトピック**を選び、**異なる意見や多様な視点**を提供する。
- The Critical(批判主義) model: 普段は届きにくい、**マイノリティなコミュニティの意見や主張**を積極的に提供する。

(各メディアモデルに優劣はなくて、どのモデルに従うかは、メディア企業自身が、そのmissionに従い、民主主義社会で果たしたい役割に応じて決めるべき)

## 5種類のdiversity metrics

4種のメディアモデルによって"目指すべき多様性"の価値と意味合いが異なる。本論文では、**各メディアモデルが推薦システムに期待する性質**から導出した、**5つのdiversity metrics**を提案:

:::: {.columns}

::: {.column width="50%"}

- Calibration: hogehoge
- Fragmentation: hogehoge
- Activation: hogehoge
- Representation:
- Alternative Voices

:::

::: {.column width="50%"}

全metricsに共通する性質:

- distance metric。
- ２つの確率分布間のJS-Divergence。
- 異なる推薦モデル間や異なるmetric間で比較したいので、全て値域が $[0; 1]$。(0に近いほど2つの分布の距離が近い)
- rank付けした推薦に適用したいので、rank情報を持った離散分布に適用可能。(rank-awareな指標)

:::

::::

(論文では、これらの性質を満たす為の導出過程とか考えが丁寧に記述されてた。らrank-awareにする上での重み付け方法の選択とか。)

## 5種類のdiversity metrics ① Calibration

:::: {.columns}

::: {.column width="50%"}

- 「推薦記事がユーザの好みとどの程度合っているか」を反映したもの。
  - 推薦記事リストの分布とユーザの閲読履歴の分布の間の距離を意味する。

$$
Calibration = D_{JS}(P^*(c|H), Q^*(c|R))
\\
% = \sum_{c} Q^*(c|R) f(\frac{P^*(c|H)}{Q^*(c|R)})
\tag{7}
$$

:::

::: {.column width="50%"}

分布のイメージ図、みたいなやつ。

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ は、rankで重み付けされた確率関数である事を意味する。 $H$ は、あるユーザの閲読履歴にある記事集合。$R$ は、推薦記事リスト。$c$ は確率変数。(論文中では、記事categoryや記事のcomplexityを確率変数として提案してたので $c$ にしてるっぽい。)

## 5種類のdiversity metrics ② Fragmentation

:::: {.columns}

::: {.column width="50%"}

- 「共通したトピックの記事を提供できているか」の度合いを反映したもの。
  - 複数ユーザの推薦記事リストの分布間の距離を意味する。(二人のユーザ $u$ と $v$ を比較する)

$$
Fragmentation = D_{JS}(P^*(e|R^{u}), Q^*(e|R^{v}))
% = \sum_{e} Q^*(e|R^v) f(\frac{P^*(e|R^u)}{Q^*(e|R^v)})
\tag{8}
$$

:::

::: {.column width="50%"}

分布のイメージ図、みたいなやつ。

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ は、rankで重み付けされた確率関数である事を意味する。 $R^{u}, R^{v}$ は、ユーザuとvの推薦記事リスト。$e$ は、記事のevent(=記事のトピック的な?)を表す確率変数。

## 5種類のdiversity metrics ③ Activation

:::: {.columns}

::: {.column width="50%"}

- 「肯定的な記事ばかり推薦してしまってないか、逆に否定的な記事ばかり推薦してしまってないか」の度合いを反映したもの。
  - 推薦可能な記事プール $S$ と、推薦記事リスト $R$ のactivation score(=positiveかnegativeか)の分布間の距離を表す。

$$
Activation = D_{JS}(P(k|S), Q^*(k|R))
% = \sum_{k} Q^*(k|R) f(\frac{P(k|S)}{Q^*(k|R)})
\tag{9}
$$

:::

::: {.column width="50%"}

分布のイメージ図、みたいなやつ。

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ は、rankで重み付けされた確率関数である事を意味する。 $k$ は、記事のactivation score(=positiveかnegativeか)を表す確率変数。

なお、記事のactivation scoreは、論文ではテキストのsentiment analysis(感情分析?)等で得る事を想定していた。

## 5種類のdiversity metrics ④ Representation

:::: {.columns}

::: {.column width="50%"}

- 「viewpoint(ex. 政治的トピックや政党の言及など)の多様性」の度合いを反映したもの。
  - 記事プール $S$ と、推薦記事リスト $R$ のviewpoint(離散値を想定) の分布間の距離を表す。

$$
Representation = D_{JS}(P(p|S), Q^*(p|R))
% = \sum_{p} Q^*(p|R) f(\frac{P(p|S)}{Q^*(p|R)})
\tag{10}
$$

:::

::: {.column width="50%"}

分布のイメージ図、みたいなやつ。

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ はrankで重み付けされた確率関数の意味。 $p$ は 記事のviewpointを表す離散変数。

(どうやって記事のメタデータとしてviewpointを作れるだろう...:thinking:)

# NewsPicksにおけるRADioの活用可能性に思いを馳せてみた。

# RADioの活用例を考えた① 推論結果の品質モニタリング

MLOps Maturity Assessmentや Booking.comの論文でも主張されているが、バッチ推論でもオンライン推論でも、推論結果の品質をモニタリングし、異常があれば早期に検知する事は重要。

## 推論結果の品質モニタリング指標としてのRADio

- hoge

# RADioの活用例を考えた② 推薦モデルのオフライン評価

## オフライン評価難しい問題

ニュース推薦の分野では、metadataとしてテキストが使える事と、推薦アイテム=ニュースのlifecycleが短く、新鮮なcold-start itemを推薦したいusecaseが多い事から、**content-based系の手法**(i.e. id-onlyでない手法)が多く採用されてる印象。

> However, in general, content-based techniques are considered not to be very accurate in offline experiments when using IR measures like precision and recall [80].
> As we will discuss later, the effectiveness of pure collaborative filtering methods might be overestimated in offline experiments,

しかし、content-based手法はオフライン実験においてprecisionやrecallなど(=要はaccuracy-basedな、教師ラベルに依存するmetrics??:thinking:)では正確に評価しづらく、一方でid-only手法やmost-popular itemsは過大評価されやすい傾向。
(人気度バイアスとか、Off-Policy Evaluation分野で言うところのlogging policy由来のバイアスとかが原因??:thinking:)

(もちろんunder samplingやOPE推定量等でバイアス除去を試みるアプローチもある。)
(ただ、OPEのIPS推定量に基づくアプローチは、logging policyが探索的なモデルである必要があるので、決定論的な推薦システムでは活用が厳しい...!:thinking:)

## オフライン評価指標としてのRADio

- RADioはいずれも、推薦後の教師ラベルに依存しないmetricsなので、バイアスの影響を受けづらい。(あ、でもユーザのreading historyは、バイアスの影響を受けているか...! under samplingアプローチと組み合わせるのはどうだろう...!:thinking:)
-
