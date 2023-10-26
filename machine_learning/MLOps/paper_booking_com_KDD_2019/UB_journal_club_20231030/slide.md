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

title: 宿泊予約サービスbooking.comの150個の機械学習モデルの開発運用で得た6つの教訓をまとめた論文(KDD2019)を読んで概要と感想
subtitle: 論文読み会
date: 2023/10/26
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 参考文献:

- 元論文: [150 Successful Machine Learning Models: 6 Lessons Learned at Booking.com](https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf)

## このテーマを選んだ理由

- hogehoge

## どんな論文??

- 宿泊予約サービスbooking.comの150個の機械学習モデルの開発運用で得た6つの教訓をまとめた論文(KDD2019)
- 教訓1は、プロダクト開発において機械学習を色んな用途・文脈で活用できている話。
- 教訓2は、機械学習モデルのオフライン評価指標とオンラインでのビジネス指標との間に相関がなかった話。
- 教訓3は、機械学習で解かせるべき問題設定をよく考え続けよう、という話。
- 教訓4は、レイテンシー大事という話。
- 教訓5は、モデルの推論結果の品質のモニタリングの話。(応答分布分析良いね...!:thinking:)
- 教訓6は、RCTの実験デザイン頑張ってる話。

# 教訓1: Inception: Machine Learning as a Swiss Knife for Product Development

- 機械学習は、プロダクト開発におけるスイスナイフである(=多機能で色んな用途に使える例えらしい...:thinking:)

## 教訓1の感想: spmantic modelいいなぁ...:thinking:

- プロダクトの異なる機能の開発/改善の為に、機械学習を様々な文脈で活用できたという話。
  - 特定のusecaseに特化した specialized model
  - 様々なusecaseで活用可能性がある **semantic model**
    - 理解しやすい概念をモデル化する(定量化できていないユーザの特徴を、MLでモデル化する、みたいな??:thinking:)
    - ex) 「ユーザが旅行の目的地に対してどの程度flexibleであるか」を定量化するモデルを作り、**プロダクトチーム全体にdestination-flexibilityの概念を与える**ことで、プロダクトの改善に役立てることができた。(MLチーム以外も理解・活用可能な汎用的な特徴量を作る、みたいなイメージかな...めちゃいいね!:thinking:)
  - semanticモデルにより、**商品開発に携わる全ての人がモデルの出力に基づいて**、新機能やパーソナライゼーション、説得力のある意思決定などに導入できるようになる。(semanticなモデルいいなぁ...:thinking:)

# 教訓2: Modeling: Offline Model Performance Is Just A Health Check(オフラインでのモデルのパフォーマンスは健康診断に過ぎない)

# 教訓3: Modeling:Before Solving A Problem, Design It (問題を解かせる前に、解かせるべき問題をデザインする)

# 教訓4: Deployment: Time Is Money (時は金なり)

# 教訓5: Monitoring: Unsupervised Red Flag (監視されないレッドフラッグ)

# 教訓6: Evaluation: Experiment Design Sophistication Pays Off (洗練された実験計画が功を奏す)
