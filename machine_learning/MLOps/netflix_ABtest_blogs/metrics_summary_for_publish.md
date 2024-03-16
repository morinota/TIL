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

title: より良い意思決定がしたいので、under-powered なテストを避けるためのABテスト設計方法を調べた
subtitle: y-tech-ai ワクワク勉強会
date: 2024/02/xx
author: モーリタ
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

<!-- title: 不確実性を含むABテストでより良い意思決定がしたいので、OECとかmetrics周りを調べた! -->

n週連続推薦システム系論文読んだシリーズ 38 週目の記事になります:)
ちなみに37週目は [より良い意思決定がしたいので、under-powered なテストを避けるためのABテスト設計方法を調べた](https://zenn.dev/morinota/articles/ee3503cc818dd0) でした!
(一応、推薦システムもオンライン実験するので!:pray:)

## はじめに

- 本資料は、ABテストでより良い意思決定のために意識すべきことの1つとして、**ABテストの際に評価するmetricsやOEC(Overall Evaluation Criterion)**に焦点を当て、自分の理解をまとめたものです。

  - きっかけ: 前回、ABテストでよりよい意思決定をするための必要条件の一つとして、under-poweredなテストを避ける為の設計方法について調査しました。調べていく中で、適切なサンプルサイズ設計のアプローチとか分かったけど、**そもそもサンプルサイズ設計の前に、どのmetricsを監視・評価すべきなのよ!**って迷ったので。

- ちなみに参考文献は以下です:

  - [NetflixさんのABテストに関するブログ連載](https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8)
  - [X(旧Twitter)さんのABテストのサンプルサイズ設計に関するブログ](https://blog.twitter.com/engineering/en_us/a/2016/power-minimal-detectable-effect-and-bucket-size-estimation-in-ab-tests)
  - [web上でのコントロール実験に関するpracticeをまとめた論文](https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf)
  - [第一回webコントロール実験実線サミットの論文]()
  - [(通称、カバ本?)]()

- もし理解の誤りや気になる点などあれば、カジュアルに絵文字をつけてコメントしていただけると喜びます...!:thinking:

## ABテストでどんなmetricsを監視・評価すればいいのよ??

### metricsってどんな種類があるの??

#### Netflixさんのテックブログでの記述によると...

まずNetflixさんのブログでは、**以下の3種類のmetrics**を使う事を述べていました。

- 1. primary decision metrics
  - **施策のアイデアを実験で検証可能な仮説に変換**して得られたmetrics。
- 2. secondary metrics
  - **施策(ex. プロダクトの変更)とprimary decision metricsの間の因果関係**を監視するためのmetrics。
    - 仮定するcausal chainのイメージはこう！「施策の適用 → secondary metricsが変化するはず! → primary decision」metricsが変化するはず!」
  - -> secondary metricsを監視することで、**primary decision metricsの変化が、我々が仮定した因果関係通りに施策によって発生しているのかどうかの判断根拠を持てる**...!
    - ex.) 期待通りにprimary decision metricsが改善したが、secondary metricsが期待と異なる変化をしている場合、primary decision metricsの変化は施策の効果によるものではなく偽陽性(false positive)である可能性がある。
- 3. guardrail metrics:
  - **施策による意図しない悪影響などを監視する為のmetrics**。
  - ちなみに...
    - 「guardrail metrics」という用語には大きく2種類のmetricsが含まれているようです。
    - 後述する他の参考資料などでは、**実験の信用性や妥当性を保証するためのmetrics**、という文脈でも使用されていました。でも、Netflixさんのブログ内では主に前者の意味合いで紹介されてました!

(ちなみに、ブログ内では「Top 10 list」というプロダクト新機能のABテストを例に、上記の3種のmetricsの設定手順について詳しく説明されていました! 分かりやすくてありがてぇ...!:thinking:)
(ちなみに文脈的に、どの種類のmetricsも必ずしも単一のmetricであるべき、という制約はなさそうでした!:thinking:)

#### カバ本での記述によると...

#### 実践プラクティスサミットの論文での記述によると...

## OEC(Overall Evaluation Criterion)について

### OEC(Overall Evaluation Criterion)ってなんぞや??

## OECの定義:

## おわりに

- 不確実性を含むABテストでより良い意思決定がしたいので、Netflixさんのテックブログや論文達やカバ本などを読んで、OECとかmetrics周りを調べたよ! というお話でした。
- まとめ:
  - hogehoge
  - hogehoge
- 最後まで読んでいただきありがとうございました! もし気になった点や自分の理解に誤ってる点などあれば、ぜひカジュアルに絵文字をつけてコメントいただけるとめちゃめちゃ喜びます:)
