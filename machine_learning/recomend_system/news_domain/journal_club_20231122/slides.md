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

title: (RecSys2022 Best Papers)ニュース推薦の民主的役割を考慮した5つの多様性指標RADioの論文を読んで、推論品質モニタリングとかオフライン評価とかで色々使えないかなーと思った話
subtitle: 2023/11/22 推薦システム論文読み会
# date:
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 参考文献:

- メインの論文: [RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf)
- (メイン論文の背景にあるやつ!)ニュース推薦の民主的役割のtypologyを提案した論文: [On the Democratic Role of News Recommenders](https://www.tandfonline.com/doi/full/10.1080/21670811.2019.1623700)
- Booking.comの論文: [150 Successful Machine Learning Models: 6 Lessons Learned at Booking.com](https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf)
- News推薦のサーベイ論文: [hoge]()
- MLOpsの成熟度を高める為のガイドライン: [MLOps Maturity Assessment]()

## どんな論文? 選んだモチベーションは??

- 論文title:[RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf)
- RecSys2022 Best Paper Awards
- ニュース推薦やメディアの民主的役割を考慮した5つの多様性指標群を用いた推薦システムの評価フレームワーク RADio を提案する論文。
  - 「〇〇を目的としたメディアを目指す場合、☓☓と△△のdiversity metricのスコアが高い推薦システムを選ぶと良い」みたいなdiversity metricsの使い方, モデルの選び方を提案する論文(とざっくり解釈してます...!:thinking:).
- 多様性の指標として，よりニュース推薦の分野に特化した指標を提案していた。
- この論文を読んだのは半年前なのですが、推論結果の品質モニタリングやオフライン評価に使えないかなと考え始め、皆さんに共有したく選択した。

## 背景: メディアの役割を意識した推薦システムの概念モデル

既存研究では、メディアの民主主義的な役割を考慮して以下の4種類に分類:

- The Liberal model(自由主義モデル): ユーザの好みに合わせて、トピックや文章のスタイルを選ぶ推薦システム。
- The Participatory model(参加型モデル): ユーザがコミュニティで活動するために必要な共通認識をわかりやすい形で提供する推薦システム。
- The Deliberative model(審議型モデル): 現在注目が集まっているトピックに対して異なる意見やさまざまな視点を与える推薦システム
- The Critical model(批判モデル): マイノリティなコミュニティの声を強調させる推薦システム。

## 5つの多様性指標の共通点

- 順位付けされた推薦記事リストに対して適用可能。
- rank-awareなmetrics。
- value rangeは0~1。
- JS-Divergenceの形式をしており、2つの分布間の距離を測る。

## 5つの多様性指標

:::: {.columns}

::: {.column width="50%"}

- 5種類の多様性指標:
- Calibration
- Fragmentation
- Activation
- Representation
- Alternative Voices

:::

::: {.column width="50%"}

- hoge

:::

::::

# RADioの活用例を考えた① 推論結果の品質モニタリング

MLOps Maturity Assessmentや Booking.comの論文でも主張されているが、バッチ推論でもオンライン推論でも、推論結果の品質をモニタリングし、異常があれば早期に検知する事は重要。

## 推論結果の品質モニタリング指標としてのRADio

- hoge

# RADioの活用例を考えた② 推薦モデルのオフライン評価

## オフライン評価難しい問題

ニュース推薦の分野では、metadataとしてテキストが使える事と、推薦アイテムであるニュースのlifecycleが短く、新鮮なcold-start itemを推薦したいusecaseが多い事から、**content-based系の手法**が多く採用されてる。

> However, in general, content-based techniques are considered not to be very accurate in offline experiments when using IR measures like precision and recall [80].
> As we will discuss later, the effectiveness of pure collaborative filtering methods might be overestimated in offline experiments,

しかし、content-based手法はオフライン実験においてprecisionやrecallなど(=要はaccuracy-basedな、教師ラベルに依存するmetrics??:thinking:)では正確に評価しづらく、一方でcollaborative filtering系やmost-popular itemsは過大評価されやすい傾向。
(人気度バイアスとか、Off-Policy Evaluation分野で言うところのlogging policy由来のバイアスとかが原因??:thinking:)

(もちろんunder samplingやOPE推定量等でバイアス除去を試みるアプローチもある。)
(ただ、OPEのIPS推定量に基づくアプローチは、logging policyが探索的なモデルである必要があるので、決定論的な推薦システムでは活用が厳しい...!:thinking:)

## オフライン評価指標としてのRADio

- RADioはいずれも、推薦後の教師ラベルに依存しないmetricsなので、バイアスの影響を受けづらい。(あ、でもユーザのreading historyは、バイアスの影響を受けているか...! under samplingアプローチと組み合わせるのはどうだろう...!:thinking:)
-
