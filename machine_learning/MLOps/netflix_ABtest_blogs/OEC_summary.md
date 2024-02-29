<!-- より良い意思決定がしたいので、ABテストにおけるOEC周りについて調べた -->

n週連続推薦システム系論文読んだシリーズ k 週目の記事になります。
ちなみに k-1 週目は [タイトル](url) でした!

## はじめに:

- 本資料は、netflixさんやXさんのテックブログやpracticeをまとめた論文を参考に自分の理解をまとめたものです:)
  - [NetflixさんのABテストに関するブログ連載](https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8)
  - [X(旧Twitter)さんのABテストのサンプルサイズに関するブログ](https://blog.twitter.com/engineering/en_us/a/2016/power-minimal-detectable-effect-and-bucket-size-estimation-in-ab-tests)
  - [web上でのコントロール実験に関するpracticeをまとめた論文](https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf)
  - 上記の文献ではABテストを経てより良い意思決定のための工夫として様々紹介されています。
- 本資料は、より良い意思決定のために意識すべきことの1つとして、ABテストにおけるOEC(Overall Evaluation Criterion)をはじめとした評価するmetricの選定についてまとめたものです。

# OEC(Overall Evaluation Criterion) とは?
