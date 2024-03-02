<!-- より良い意思決定がしたいので、ABテストにおけるOEC周りについて調べた -->

n週連続推薦システム系論文読んだシリーズ k 週目の記事になります。
ちなみに k-1 週目は [タイトル](url) でした!

## はじめに:

- 本資料は、netflixさんやXさんのテックブログやpracticeをまとめた論文を参考に自分の理解をまとめたものです:)
  - [NetflixさんのABテストに関するブログ連載](https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8)
  - [X(旧Twitter)さんのABテストのサンプルサイズに関するブログ](https://blog.twitter.com/engineering/en_us/a/2016/power-minimal-detectable-effect-and-bucket-size-estimation-in-ab-tests)
  - [web上でのコントロール実験に関するpracticeをまとめた論文](https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf)
  - [hogehoge](https://www.researchgate.net/publication/333136404_Top_Challenges_from_the_first_Practical_Online_Controlled_Experiments_Summit)
  - [hogehoge(通称カバ本)]()
  - 上記の文献ではABテストを経てより良い意思決定のための工夫として様々紹介されています。
- 本資料は、より良い意思決定のために意識すべきことの1つとして、ABテストにおけるOEC(Overall Evaluation Criterion)をはじめとした評価するmetricの選定についてまとめたものです。

# metricsに関する様々な概念:

元々本記事の執筆を試みた際は、ABテストの分析に使用すべきmetricsやOEC(Overall Evaluation Criterion)について調査しまとめる予定でした。
しかし調査を進めるうちに、metricsに関する様々な概念があり、OECのことを理解・解釈するためには、それらの概念についてもざっくり把握しておく必要があると感じました!

## 組織を運用するためのmetrics

カバ本によると、組織を運用するためのmetricsの一般的な分類方法として以下のようなものがあるようです:

- goal metrics
- driver metrics
- guardrail metrics

ちなみに、他の分類方法もあるとのことでした:

- hoge

## 実験のためのmetricsとOEC

## OEC(Overall Evaluation Criterion) とは?
