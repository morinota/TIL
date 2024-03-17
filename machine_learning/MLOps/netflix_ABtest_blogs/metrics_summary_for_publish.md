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
(一応、推薦システムもオンライン実験するじゃん、ということで許してください!:pray:)

## TL;DR

- 本資料は、ABテストでより良い意思決定がしたいので、ABテストの際に監視・評価すべきmetricsやOEC(Overall Evaluation Criterion)に焦点を当てて調査し、自分の理解をまとめたもの!
- **ABテストで監視・評価すべきmetricsは、ざっくり以下の4種類**に分類されるっぽい!
  - 1. 施策が成功したのか、その影響はどうだったのかを判断するための primary metrics (i.e. primary decision metrics)
  - 2. primary metricsの変化が本当に施策による効果か否かを判断するための secondary metrics
    - (用語は様々だが、基本的には施策からprimary metricsへの因果関係の中間因子的なものを反映したmetricsという認識...!:thinking:)
  - 3. ビジネス上の制約を守る為のguardrail metrics
  - 4. 実験の信用性を守る為のguardrail metrics
- 複数のprimary metricsが存在しそれらが競合し得る場合、**組織内で意思決定の整合性を保つ事が難しくなる**。その解決策としてあるのが、**複数のprimary metricsを合成したOEC(Overall Evaluation Criterion)**を導入すること。

## はじめに

- 本資料は、ABテストでより良い意思決定のために意識すべきことの1つとして、**ABテストの際に評価するmetricsやOEC(Overall Evaluation Criterion)**に焦点を当て、自分の理解をまとめたものです。
  - きっかけ: 前回、ABテストでよりよい意思決定をするための必要条件の一つとして、under-poweredなテストを避ける為の設計方法について調査しました。調べていく中で、適切なサンプルサイズ設計のアプローチとか分かったけど、**そもそもサンプルサイズ設計の前に、どのmetricsを監視・評価すべきなのよ!**って迷ったので。
- ちなみに参考文献は以下です:
  - [NetflixさんのABテストに関するブログ連載](https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8)
  - [X(旧Twitter)さんのABテストのサンプルサイズ設計に関するブログ](https://blog.twitter.com/engineering/en_us/a/2016/power-minimal-detectable-effect-and-bucket-size-estimation-in-ab-tests)
  - [web上でのコントロール実験に関するpracticeをまとめた論文](https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf)
  - [第一回webコントロール実験実線サミットの論文]()
  - [(通称、カバ本?)]()
- もし理解の誤りや気になる点や情報共有したいことなどあれば、カジュアルに絵文字をつけてコメントしていただけると喜びます...!:thinking:

## ABテストでどんなmetricsを監視・評価すればいいのよ??

この点に関しては、3つの文献に色々記載があった為、それぞれの文脈に合わせてまとめてみています。
先に結論から述べると、ABテストで監視・評価すべきmetricsは、ざっくり以下の4種類に分類されるっぽいです!

- 1. 施策が成功したのか、その影響はどうだったのかを判断するための primary metrics (i.e. primary decision metrics)
- 2. primary metricsの変化が本当に施策による効果か否かを判断するための secondary metrics
  - (用語は様々だが、基本的には施策からprimary metricsへの因果関係の中間因子的なものを反映したmetricsという認識...!:thinking:)
- 3. ビジネス上の制約を守る為のguardrail metrics
- 4. 実験の信用性を守る為のguardrail metrics

### Netflixさんのテックブログでの記述によると...

まずNetflixさんのブログでは、**以下の3種類のmetrics**をABテスト内で監視・評価すること事を述べていました。

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

### カバ本での記述によると...

続いて、カバ本では、**まず組織を運用する為のmetricsが存在する前提**で、それらを基に、ABテストに適した性質を満たすような実験用metricsを作成する事を推奨していました。

組織を運用する為のmetricsとして、**以下の3種類のmetrics**が挙げられていました。
(ちなみに、metricsの分類方法はいくつかあるようですが、この分類方法が最も一般的なようです)

- 1. goal metrics:
  - 他の呼び方: success metrics, etc.
  - 組織が成し遂げたいgoalや組織のミッションを反映したmetrics。
- 2. driver metrics:
  - 他の呼び方: signpost metrics, surrogate metrics, proxy metrics, etc.
  - 組織のgoalの達成そのものよりも、goalの達成のための成功要因は何かの仮説を反映したmetrics。
    - (なので、**goal metricsとdriver metricsの関係性**は、Netflixさんのブログにおけるprimary decision metricsとsecondary metricsの関係性と近くて、たぶん「施策や取り組み → 組織の成功」の**因果グラフにおける中間因子的なものを反映したmetrics**か...!!...!:thinking:)
- 3. guardrail metrics:
  - そもそもの制約や前提条件に違反することを防ぐためのmetrics。
  - カバ本では、「guardrail metrics」には**大きく2種類が含まれる**と述べられていました。
    - 3.1 ビジネス上の制約を保証する観点でのguardrail metrics:
      - ex. latency, error rate, etc.
    - 3.2 実験の信用性や妥当性を保証する観点でのguardrail metrics:
      - ex. variant間のサンプルサイズ比率, 期待する効果量に対する検出力, etc.
    - (そのうち前者が、組織を運用する為のmetricsの文脈に合致するはず...!:thinking:)

ちなみに、上記の3種類の組織を運用する為のmetricsに関して、カバ本では他にも以下のような話が丁寧に記述されていました! ありがてぇ～(詳しくはカバ本の6章や7章辺りへ...!)

- metricsについての議論を継続的に行う事の価値の話。
  - (ビジネスの理解を深めながらmetricsをiterativeに改善していきてぇ～:thinking:)
- 各チームのgoal & driver & guardrail merticsが、組織全体のgoal & driver & guardrail merticsの方向性と整合している事が重要という話。
- metricsの定式化のtipsに関する話。
  - (定性的な概念を、いかに定量的なmetricsに落とし込むかの話)
  - goal & driver & guardrail merticsがそれぞれ満たすべき性質・原則を含めて色々紹介されてた!

そしてカバ本では、上述した**ビジネス上のgoal & driver & guardrail merticsを基に、ABテストに適した性質を満たすような実験用metricsを作成する**事を述べているんでした。

**実験用metricsが満たすべき性質は以下の4つ**です。

- 1. 測定可能性:
  - 実験用metricsは、定量的に測定可能である必要がある。
  - (ex. 「商品購入後のユーザ満足度」は直接的には測定困難)
- 2. 計算可能性:
  - 実験用metricsは、ABテストの各variantに紐づけて計算可能である必要がある。
- 3. 感度の高さ:
  - 実験用metricsは、施策の期待する効果を検出するのに十分な感度を持っている必要がある。
    - (例えば**metricsの変動性(分散)**の話とか...!めっちゃばらつきが大きいmetricだと施策の効果を検出できないし...!:thinking:)
    - (ex. 「会社の株価」は、日常的なプロダクト変更や施策に対して感度が低い。)
- 4. 即時性の高さ:
  - 実験用metricsは、**施策の期待する効果を実験期間内に検出できる**必要がある。
    - (ex. 「サブスクリプション契約(1年間)の更新率」は即時性が低い)
      - 1年間の長期的な実験を行わない限りは、施策が更新率に与える影響を検出するのは困難...!
      - この場合は、**契約更新の意思決定につながる満足度の早期指標となるようなproxy的なmetricsを探すと良い**...!

そして一般的には、以下のようなmetricsを実験用metricsとして採用するようです。

- 1. ビジネス上のgoal & driver & guardrail merticsの中から、実験用metricsの満たすべき4つの性質を全て満たすもの。
  - (基本的にはgoal metricsは、性質満たさ無さそう...!:thinking:)
- 2. (必要に応じて) goal metricsやdriver metricsのproxy的なmetrics。
  - (goal metricsやdriver metrics達の多くが、実験のためのmetricsとして適していない場合の話かな?? その場合は、何らかのproxy metricsを定義する必要があるのか...!:thinking:)
- 3. (必要に応じて) 特定の機能の動きを理解するための、より詳細なlocalなmetrics.
  - (ex. 特定の機能のユーザ行動を理解するためのmetrics)
- 4. 実験の信用性や妥当性を保証するためのguardrail metrics.

(1番目と2番目のmetricsが、Netflixさんブログにおけるprimary decision metricsの概念にあたりそう。3番目がsecondary metricsで、4番目がguardrail metricsに該当しそう...!:thinking:)

カバ本によると、典型的な実験スコアカードには、いくつかのprimary metrics(主要なmetrics)と数百から数千のその他のmetricsがある、とのこと。そんなに多いのか...!!:thinking:

### 実践プラクティスサミットの論文での記述によると...

この論文内では、以下の大きく4種類のmetricsが挙げられていました。

- 1. 実験結果が信頼できるものかどうかを判断するためのmetrics。
  - (ex. サンプル比率とか!)
  - (「信用性guardrail metrics」と呼ばれてたりするやつ!:thinking:)
- 2. 施策が成功したのか、その影響はどうだったのかを判断するためのmetrics。この一連のprimary metricsがOECを構成する。
  - (ちなみに、OEC(Overall Evaluation Criterion)というのは、実験の目的(objective)を表す定量的な指標の意味で、次セクションにて理解をまとめます...!)
  - (文脈的に、**この論文内ではOECは複数のprimary metricsの合成metricである事を前提としてるっぽい**...!:thinking:)
- 3. テストされている施策の成功を明確に示すものではないが、悪化させたくないguardrail metrics。
- 4. 実験のmetricsの残りの大部分は、diagnostic, feature, local metricsと呼ばれるもの。
  - これらのmetricsは、OEC(i.e. primary metricsを合成したもの!)の動きの原因を理解するために使われる。

### まとめると...

改めてですが、以上の3つの参考資料によると、ABテストで監視・評価すべきmetricsは、ざっくり以下の4種類に分類されるっぽいです!

- 1. 施策が成功したのか、その影響はどうだったのかを判断するための primary metrics (i.e. primary decision metrics)
- 2. primary metricsの変化が本当に施策による効果か否かを判断するための secondary metrics
  - (用語は様々だが、基本的には施策からprimary metricsへの因果関係の中間因子的なものを反映したmetricsという認識...!:thinking:)
- 3. ビジネス上の制約を守る為のguardrail metrics
- 4. 実験の信用性を守る為のguardrail metrics

## OEC(Overall Evaluation Criterion)について

前セクションにて、どんなmetricsを準備してABテストを行うべきか雰囲気を掴む事ができました!

そしてこのセクションでは、複数のprimary metricsが存在しそれらが競合し得る場合、**組織内で意思決定の整合性を保つ事が難しくなる**問題がある、と。
その解決策として推奨される、**複数のprimary metricsを合成したOEC(Overall Evaluation Criterion)**について理解をまとめます。

### Webのコントロール実験に関するpracticeをまとめた論文での記述によると...

### the first Practical Online Controlled Experiments Summit(第一回実践的オンラインコントロール実験サミット)の論文での記述によると...

### カバ本での記述によると...

## おわりに

- 不確実性を含むABテストでより良い意思決定がしたいので、Netflixさんのテックブログや論文達やカバ本などを読んで、監視すべきmetrics周りとかOECについて調べたよ! というお話でした。
- 最後まで読んでいただきありがとうございました! もし気になった点や自分の理解に誤ってる点などあれば、ぜひカジュアルに絵文字をつけてコメントいただけるとめちゃめちゃ喜びます:)
