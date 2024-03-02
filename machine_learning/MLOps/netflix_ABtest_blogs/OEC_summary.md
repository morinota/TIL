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

カバ本によると、組織を運用するためのmetricsとして以下の3種類に分類する方法が一般的なようです:

- goal metrics
  - 別名 success metrics, 他にも日本語で「真に重要なmetrics」とも呼ばれるらしい。(英語だとなんだろう)
  - 組織が最終的に大切にしている事を反映してる。
    - 組織のミッションを完全に指標に変換する事は困難なので、**goal metricsは組織が成し遂げたい事のproxy(代理)**である可能性がある。
      - -> ミッションのproxyとして、より良いgoal metricsをiterativeに探す必要はある。
    - **組織のミッションとgoal metricsの間の違いや関連性の限界を理解すること**は、ビジネスやプロダクトをより正しい方向に進める上で非常に重要らしい...!
  - **良いgoal metricsは、単一または少数のmetrics集合であり、組織が目指す最終的な成功を最もよく捉えるもの**。
- driver metrics:
  - 別名 signpost metrics, surrogate metrics, proxy metrics, 間接的または予測metrics
  - goal metricsよりも短期的に動く、敏感なmetricsである傾向。
  - 組織の成功そのものよりも、組織を成功に導くためのメンタル因果モデルを反映したもの。(i.e. 成功要因は何かの仮説を反映したもの)
    - (i.e. 「施策や取り組み → 組織の成功」の因果グラフにおける中間因子的なものを反映したmetricsか...!!:thinking:)
    - (**goal metricsとdriver metricsの関係は、Netflixさんのブログにおけるprimary decision metricsとsecondary metricsの関係と似てそう**...!!:thinking:)
  - 良いdriver metricsは、施策や取り組みがgoal metricsを正しい方向に動いているか否かを反映している。
- guardrail metrics:
  - **そもそもの前提条件に違反することを防ぐためのmetrics**。
    - 基本的にgoal metricsとdriver metricsの改善を目指すが、重要な制約に違反せずに成功に向かうためにはguradrail metricsも重要...!!
  - **guardrail metricsは二種類**:
    - ビジネスを守る観点でのguardrail metrics
      - ex. latency, error rate, etc...
    - 実験の信用性や妥当性の観点でのguardrail metrics
      - 均一なサンプルサイズ,
    - (なのでABテストの文脈でguardrail metricsという文言はよく出てくる...!:thinking:)
  - guardrail metricsはgoal merticsやdriver metricsよりも敏感であるケースが多い(i.e. 短期的?)

ちなみに上記の3分類の他にも、以下のような分類方法もあるとのことでした!

- Asset metrics & engagement metrics
- bussiness metrics & operational metrics

### metricsについての議論を行う事の価値

(metricsっていいよね、大事だよねって話...!そもそもmetricsって定量指標の事??:thinking:)

- どのような分類方法を採用するかに依らず、metricsについての議論を行う事は重要。
  - 会社レベル、チームレベル、機能レベル、個人レベルの目標設定に使用できる...!
  - 役員報告からシステムの監視まで、あらゆるものに使用できる...!
- **各チームのmetricsを、組織全体のgoalや戦略の方向性と一致させることが重要**という話:
  - hoge

## 実験のためのmetricsとOEC

## OEC(Overall Evaluation Criterion) とは?
