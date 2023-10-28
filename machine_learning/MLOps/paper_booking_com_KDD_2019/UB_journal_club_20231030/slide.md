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
- 教訓1: Inception: Machine Learning as a Swiss Knife for Product Development (機械学習はプロダクト開発におけるスイスナイフである)
- 教訓2: Modeling: Offline Model Performance Is Just A Health Check(オフラインでのモデルのパフォーマンスは健康診断に過ぎない)
- 教訓3: Modeling:Before Solving A Problem, Design It (問題を解かせる前に、解かせるべき問題をデザインする)
- 教訓4: Deployment: Time Is Money (時は金なり)
- 教訓5: Monitoring: Unsupervised Red Flag (監視されないレッドフラッグ)
- 教訓6: Evaluation: Experiment Design Sophistication Pays Off (洗練された実験計画が功を奏す)

## 本論文の貢献

# 教訓1: Inception: Machine Learning as a Swiss Knife for Product Development

- 機械学習は、プロダクト開発におけるスイスナイフである(=多機能で色んな用途に使える例えらしい...:thinking:)

## 教訓1の概要:

- プロダクトの異なる機能の開発/改善の為に、機械学習を様々な文脈で活用できたという話。
  - 特定のusecaseに特化した specialized model
  - 様々なusecaseで活用可能性がある **semantic model**
    - 理解しやすい概念をモデル化する(定量化できていないユーザの特徴を、MLでモデル化する、みたいな??:thinking:)
    - ex) 「ユーザが旅行の目的地に対してどの程度flexibleであるか」を定量化するモデルを作り、**プロダクトチーム全体にdestination-flexibilityの概念を与える**ことで、プロダクトの改善に役立てることができた。(MLチーム以外も理解・活用可能な汎用的な特徴量を作る、みたいなイメージかな...めちゃいいね!:thinking:)
  - semanticモデルにより、**商品開発に携わる全ての人がモデルの出力に基づいて**、新機能やパーソナライゼーション、説得力のある意思決定などに導入できるようになる。(semanticなモデルいいなぁ...:thinking:)

## 教訓1の概要: MLプロジェクト

:::: {.columns}

::: {.column width="50%"}

- MLベースのプロジェクトがもたらした直接的な影響(図2より)
  - 調査期間内に成功した全プロジェクト(MLベースか否かに依らず)のビジネス指標改善の中央値を、ベースライン(1.0)とする。
  - 各barは、各model familyによる同指標改善の中央値(導入直後 or モデル改善時の測定値)(ベースラインとの相対値)

:::

::: {.column width="50%"}

![(論文より引用)](https://i.imgur.com/egM372v.png)

:::

::::

- -> 1つを除いて、各model family の貢献度はベンチマークを上回っている。全model familyの中央値もベースラインより大きい。
- また、MLモデルが新プロジェクトの基礎となるような間接的な影響も社内で観察された(特にsemantic model 関連の話??:thinking:)

# 教訓2: Modeling: Offline Model Performance Is Just A Health Check(オフラインでのモデルのパフォーマンスは健康診断に過ぎない)

## 教訓2の概要と感想

:::: {.columns}

::: {.column width="40%"}

- hogehoge

:::

::: {.column width="60%"}

![](https://i.imgur.com/TZEaYJu.png)
(論文より引用)

:::

::::

# 教訓3: Modeling:Before Solving A Problem, Design It (問題を解かせる前に、解かせるべき問題をデザインする)

## 教訓3の概要:

:::: {.columns}

::: {.column width="50%"}

- MLでビジネス課題の解決に貢献するための最初のステップは、**機械学習問題を「設定」すること**だった。
  - モデルを改善するのが最も明白な方法だけど、**問題設定そのものを変える事も有効** という話:thinking:
- ex) 滞在時間の長さを予測する回帰問題->多クラス分類問題。clickログに基づくユーザ嗜好モデル -> 宿泊客のレビューデータに関するNLP問題

:::

::: {.column width="50%"}

![(論文より引用)](https://i.imgur.com/neUw25S.png)

:::

::::

- 一般的に、**最良の問題設定はすぐに思い浮かぶものではなく、問題設定を変えることが非常に効果的な方法だった**。

# 教訓4: Deployment: Time Is Money (時は金なり)

## 教訓4の概要:レイテンシーが遅いとユーザとビジネスに悪影響だった

:::: {.columns}

::: {.column width="60%"}

- 情報検索・推薦の文脈では、latencyが大きいとユーザ行動に悪影響を与えることがよく知られている[1]。
- 疑似的なlatencyを各ユーザ群に割り当てる多群RCT(結果は図6):
  - ->latencyが約30％増加すると、コンバージョン率が0.5％以上低下する傾向

:::

::: {.column width="40%"}

![](https://i.imgur.com/w5cUyEr.png)

:::

::::

- MLモデルは推論時に多大な計算資源を必要とする(=入力特徴量の前処理も含む)ため、time is money問題は特に関連する。
- Booking.comでの工夫: 推論の分散処理, 事前計算とキャッシュ, sparceなモデルの採用, etc. (sparceモデルの採用に関して、**latencyとモデル性能の影響を切り離してユーザ影響を評価する**為に教訓6のRCTデザインを用いる)

# 教訓5: Monitoring: Unsupervised Red Flag (監視されないレッドフラッグ)

- 推論APIがリクエストを返す時に、その推論の品質をモニタリングすることは重要(推論データの分布の変化や、学習・推論パイプラインへのバグの混入などによって、**エラーやlatency等には現れない推論結果の品質の低下にいち早く気づく**ため...!)
- 推論結果のモニタリングにおける2つの課題と、Booking.comがどのように課題に対応しているかの話。

## 教訓5の概要: 推論結果の品質モニタリングにおける2つの課題

- 課題1:Incomplete(不完全な) feedback
  - 多くの状況では、正解ラベルを観測することはできない。
- 課題2:Delayed(遅れる) feedback
  - 推論が行われてから何日も、あるいは何週間も経ってから、正解ラベルが観測される場合もある。

## 教訓5の概要: Booking.comがどのように課題に対応しているか

- 上記の課題から、**precisionやrecallなどの正解ラベルに依存した指標は不適切**-> 正解ラベルに依存しない指標で推論結果の品質を監視したい...!
  - 「モデルの品質について、それがサービスを提供するときに行う推論結果を見るだけで、何が言えるのだろうか?」 -> Booking.comでは**応答分布分析(=Response Distribution Analysis)**を採用。
  - 応答分布図(Response Distribution Chart, RDC, 要はモデル出力のヒストグラムっぽい)に基づいた手法。(正常なRDCはこうあるべき、という仮定をヒューリスティックに用意しておく必要がありそう?:thinking:)

:::: {.columns}

::: {.column width="50%"}

- hogehoge

:::

::: {.column width="50%"}

![(論文より引用)](https://i.imgur.com/ZcdTVDi.png)

:::

::::

# 教訓6: Evaluation: Experiment Design Sophistication Pays Off (洗練された実験計画が功を奏す)

-

## 教訓6の概要

:::: {.columns}

::: {.column width="40%"}

- hogehoge

:::

::: {.column width="60%"}

![](https://i.imgur.com/b501FJx.png)
![](https://i.imgur.com/UdXXsQ5.png)
![](https://i.imgur.com/J4tmi1g.png)
(いづれも論文より引用)

:::

::::

# まとめ

- 宿泊予約サービスbooking.comの150個の機械学習モデルの開発運用で得た6つの教訓をまとめた論文(KDD2019)
- 教訓1は、プロダクト開発において機械学習を色んな用途・文脈で活用できている話だった。(特定のusecaseに特化した**specializedなモデル** と 様々なusecaseで活用可能性がある**semanticなモデル**... semanticなモデル良いね:thinking:)
- 教訓2は、機械学習モデルのオフライン評価指標とオンラインでのビジネス指標との間に相関がなかった話。
- 教訓3は、機械学習で解かせるべき問題設定をよく考え続けよう、という話。
- 教訓4は、レイテンシー大事という話。
- 教訓5は、モデルの推論結果の品質のモニタリングの話。(応答分布分析良いね...!:thinking:)
- 教訓6は、RCTの実験デザイン頑張ってる話。
