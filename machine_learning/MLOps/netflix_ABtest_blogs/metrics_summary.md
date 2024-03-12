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

# 組織を運用するためのmetrics

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

ちなみに上記の3分類の他にも、以下のような分類方法もあるとのことでした!(よくわかってない...:thinking:)

- Asset metrics & engagement metrics
- bussiness metrics & operational metrics

## metricsについての議論を行う事の価値

(metricsっていいよね、大事だよねって話...!そもそもmetricsって定量指標の事??:thinking:)

- どのような分類方法を採用するかに依らず、metricsについての議論を行う事は重要。
  - 会社レベル、チームレベル、機能レベル、個人レベルの目標設定に使用できる...!
  - 役員報告からシステムの監視まで、あらゆるものに使用できる...!
  - 組織が進化し、metricsへの理解が進化するにつれて、時間をかけてmetricsを反復改善していく事も期待される...!
- 会社レベルとチームレベルでのgoal & driver & guardrail metricsの測定:
  - 各チームは異なる種類の貢献をして(ex. 異なるdriver metricを改善して?:thinking:)、会社全体の成功に貢献している可能性が高い。
    - 同じmetricでも、チームによって異なる役割になりうる。(ex. あるチームではlatencyはguardrail metricsだが、別のチームではgoal metrics...!)
- 各チームのmetricsを、組織全体のgoalや戦略の方向性と一致させることが重要。
  - 組織の規模や目的(i.e. 役割?)に応じて各チームが独自のgoal & driver & guardrail merticsを持っているとしても、それら全てが会社全体のgoal & driver & guardrail metricsと整合しているべき...!

## metricsの定式化

- 「metricsの定式化」とは? = 定性的な概念を、具体的で定量化可能な定義にする操作。

以下は、定式化する際の主要な原理をまとめたもの:

- goal metricsの原則:
  - 単純である。
  - 安定している。
- driver metricsの原則:
  - goal metricsと整合している。
  - 操作可能かつ関連性がある。
  - 敏感に反応する。
  - ゲーム化に耐性がある。
- guardrail metricsの原則:
  - hoge

以下は、mertics定式化に役立つテクニックと考慮すべき点:

- hoge
- goal or driver metricsの定式化の際には「品質」を考慮すべきだよ。
- metrics定義に統計モデルを組み込む場合、解釈可能な状態に保ち、継続的に検証し続けるべきだよ。
- ユーザの不満や不幸など、望まないものを正確に測定する方が簡単なケースがあるよ。
- metricsはproxy(代理)なので、常に失敗のリスクがある事を意識すべきだよ。(ex. ゲーム化など?)

## metricsの継続的な評価と検証

- metricsの有効性の評価は、最初の定式化の段階でも、その後の運用の段階でも継続的に行われるべき。
- ex.
  - ゲーム化しちゃってないか?
  - goal metricsとdriver metricsの間の因果関係が整合しているか?(実際、driver metricsが改善したら、goal metricsの改善が促進されるの??って観点。)
  - 同様に、goal metricsとguardrail metricsの間の因果関係も整合しているか?

## metricsの進化

## (Optional) guardrail metricsについて

## (Optional) ゲーム化のしやすさについて

# 実験のためのmetricsとOEC

## ビジネス上のmetricsから実験のためのmetricsを作る

- 前述のように、データ駆動型の組織では goal metrics, driver metrics, guardrail metricsが定義される。
  - これらのmetricsは、必ずしも実験に使用するためのmetricsとして適しているとは限らない。
- 実験の為のmetricsは、以下の条件を満たしているべき:
  - 1. 測定可能性。
    - ex. ECサイトにおいて、商品購入後のユーザ満足度は測定困難。
  - 2. 計算可能性。
    - ABテストの各variantに紐づけて、metricの値を計算可能である必要がある。
  - 3. 分析感度が高く、即時性があること。
    - 施策による変化を瞬時に検出するのに、十分な分析感度を持ってる必要がある。
    - (自分の解釈メモ)
      - 「分析感度が高い」metricsの要素 = 変動性(ばらつき)が小さい?
    - ex.)
      - 「会社の株価」は分析感度が低い。
        - 日常的なプロダクト変更が実験期間中に株価に影響を与えるのはほぼゼロなので...!
      - 「サブスクリプション契約(1年間)の更新率」は即時性が低い。
        - 1年間の実験を行わない限りは、施策が更新率に与える影響を検出するのは困難...!
        - この場合は、更新の意思決定につながる満足度の早期指標となるようなsurrogate metrics(代理指標)を探すと良い...!
      - 分析感度が極端に高いmetricsの例 = 新機能が存在するか(表示されてるか)否かのbinary metric
        - 当たり前だが、非常に敏感に反応する。でもユーザ体験に関する情報が得られないので無意味ではある。
      - ↑の中間的な分析感度を持つmetricsの例 = 新機能のCTR:
        - 感度は高いはず。
        - しかし、ページの他の部分の影響や他の機能との共食い(canibalization)を考慮できず、局所的な影響しか評価できない...!
      - 良いmetricsの例 = ページ全体のCTR、ページ全体のsuccess metricなど。
- 一般的には、goal metrics & driver metrics & guardrail metricsの中から、上述した4つの特性を満たすmetricsの一部を、実験のためのmetricsとして選択することになる。
- その上で、metricsセットに以下のようなmetrcisを追加する必要があるかも:
  - goal metricsやdriver metricsのsurrogate metrics(i.e. proxy metrics)
    - (goal metricsやdriver metrics達の多くが、実験のためのmetricsとして適していない場合の話??:thinking:)
  - 特定の機能の動きを理解する為の、より詳細なmetrics
    - (たぶんnetflixさんのブログにおけるsecondary metricsのようなもの...!:thinking:)
    - (ex. 新機能によってページ全体のCTRが上がる事を期待したい場合、その新機能自体のlocalなCTRが「より詳細なmetrics」に該当するよね...!:thinking:)
  - 信用性guardrail metricsやデータ品質に関するmetrics
    - (i.e. 実験の信用性や妥当性の観点でのguardrail metrics)
  - 診断とデバッグのためのmetrics
- 典型的な実験スコアカードには、いくつかのprimary metrics(主要なmetrics)と数百から数千のその他のmetricsがある。

## primary metrics(主要なmetrics)を合成してOECを作る。

- 実験のための複数のprimary metricsを選定したら、そこから**1つのmetricを選択するか**、**複数のmetricsを保持するか**、**複数のmetricsを合成して1つのOEC(Overall Evaluation Criterion)を作るか**、を決める必要がある。
- 一部の書籍では、**単一のmetricを選択する事を推奨**している:
  - OMTM(One Metric that Matters, 関心事を1つのmetricsにすること)(Lean Analytics)
  - WIG(Wildly Important Goal)(THe 4 Disciplines of Execution)
- これらは魅力的だが、あまりに単純化されている。
  - 多くのシナリオでは、最適化されているか否かを補足できる**単純な単一のmetricは存在しない**。
  - ex.) ジェット機のパイロットは、高度、速度、燃料残量、気象状況など、複数の指標を同時に監視する必要がある。パイロットが見るダッシュボードに表示するべき単一のmetricは存在しない...!
- 実際には、多くの組織では複数のprimary metricsを検討し、**metrics間のどのようなトレードオフを受け入れるかのメンタルモデル**を持っている。

- トレードオフのメンタルモデルを表す為に、**複数のmetricsを重み付けした合成metricを単一のOECと見なす**事が、より理想的な解決策かもしれない。
  - ex) スポーツの世界ではよくこの合成metricが広く使われてる。バスケの得点は、「3.0 × スリーポイントシュート成功率 + 2.0 × フリースロー成功率 + 2.0 × フィールドゴール成功率」
  - 単一のmetricを作る事ができれば、成功の定義を明確にできる。-> **組織内でトレードオフのメンタルモデルの認識をあわせられる**...! **意思決定に一貫性**をもたらす事ができる...!
  - また、この合成metricによるOEC作成のアプローチが上手く機能すれば、チームは経営陣にエスカレーションする事なく意思決定を行う事ができる。
- Roy(2001)が提案した合成手法:
  - 各metricsを事前に定義された範囲に正規化する。(ex. 0-1の範囲に正規化)
  - それぞれに重みを割り当てる。
  - OECは正規化されたmetricsの重み付け合計になる。
- いきなり重み付けするのは難しいので、カバ本では、意思決定の方針を以下の4つのグループに分類する事を推奨してる:
  - 1. 全てのprimary metricsがflatまたはpositiveで、少なくとも1つのmetricがpositiveである場合は、変更をlaunchする。
  - 2. 全てのprimary metricsがflatまたはnegativeで、少なくとも1つのmetricがnegativeである場合は、変更をrevertする。
  - 3. 全てのprimary metricsがflatの場合は、変更をlaunchせずに、実験の検出力を上げるか、さっさと失敗と見なすか、方向転換するかの検討を行う。
  - 4. いくつかのprimary metricsがpositiveで、いくつかがnegativeである場合は、トレードオフのメンタルモデルに基づいて意思決定を行う。この意思決定が十分に蓄積されたら、primary metricsに重みを割り当てる事ができるようになる可能性がある...!
- primary metricsを一つにできない場合は、primary metricsの数を最小限に絞る事を目指すべき。
  - 経験則から「**実験のprimary metricsの数を5つ以下に絞るべき**」というルールがある。
  - なぜ? -> primary metricsの数が多いほど、primary metricsの少なくともどれか1つでfalse positiveが発生する確率が高くなってしまうから...!
    - primary metricsの数を$n$とすると、false positiveが発生する確率は以下のようになる:
      - $1 - (1 - \alpha)^n$
      - $\alpha$は、acceptable false poritive rate(i.e. 有意水準)
      - 例えば、$\alpha=0.05$の場合、$n=5$でfalse positiveが発生する確率は約23%になる...! 一方でもし $n=10$だと、false positiveが発生する確率は約40%に至る...!
    - ただそもそも、p-valueによる閾値(i.e. 差が有意か否か)に強い意味を持たせすぎるのは非推奨。(p-hackingが起こりやすくなるので...!)
      - (p-hacking = 何度も検定を繰り返し、有意な結果を得るためにデータを選択する行為)

## OEC(Overall Evaluation Criterion) とは?

# 実験におけるランダム化単位と分析単位の話

- ABテストのランダム化単位(＝実験単位？)とmetricの分析単位って基本的に同じじゃないとダメなのかなって思ってたんだけど、**粒度の粗さ的には「ランダム化単位 >= 分析単位」が推奨**みたい。
- ランダム化単位の方が細かくなっちゃうのがダメっぽい。
- ex.
  - ランダム化単位=ユーザ、分析単位=ページのような、ランダム化単位の方が粗いケースでは、ページview数が極端に多い特定の１ユーザが大きく貢献しないようなmetricを選んだり、何かしらブートストラップサンプリング的な事を行ったり少し工夫が必要みたい。
