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

- hogehoge

## outline:

# RADioの活用例を考えた① 推論結果の品質モニタリング

MLOps Maturity Assessmentや Booking.comの論文でも主張されているが、バッチ推論でもオンライン推論でも、推論結果の品質をモニタリングし、異常があれば早期に検知する事は重要。

## 推論結果の品質モニタリング指標としてのRADio

- hoge

# RADioの活用例を考えた② 推薦モデルのオフライン評価

## オフライン評価難しい問題

ニュース推薦の分野では、metadataとしてテキストが使える事と、推薦アイテムであるニュースのlifecycleが短く、新着のcold-start itemを推薦したいusecaseが多い事から、**content-based系の手法**が多く採用されてる。

> However, in general, content-based techniques are considered not to be very accurate in offline experiments when using IR measures like precision and recall [80].
> As we will discuss later, the effectiveness of pure collaborative filtering methods might be overestimated in offline experiments,

しかし、content-based手法はオフライン実験においてprecisionやrecallなど(=要はaccuracy-basedな、教師ラベルに依存するmetrics??:thinking:)では正確に評価しづらく、一方でcollaborative filtering系やmost-popular itemsは過大評価されやすい傾向。
(人気度バイアスとか、Off-Policy Evaluation分野で言うところのlogging policy由来のバイアスとかが原因??:thinking:)
(もちろんunder samplingやOPE推定量等でバイアス除去を試みるアプローチもある。)

## オフライン評価指標としてのRADio

- hoge
