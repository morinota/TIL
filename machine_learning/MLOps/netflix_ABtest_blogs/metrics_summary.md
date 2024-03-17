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
    - (goal metricsやdriver metrics達の多くが、実験のためのmetricsとして適していない場合の話?? その場合は、何らかのproxy metricsを採用する必要があるのか...!:thinking:)
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

# netflixさんのブログにて

- ABテストでは3種類のmetricsを使う事を述べていた:
  - primary decision metrics:
    - 施策のアイデアを、**実験で検証可能な仮説に変換したもの**。
  - secondary metrics:
    - **施策とprimary decision metricsの間の因果関係**を監視するためのmetrics。
      - プロダクトの変更とprimary decision metricsの変化の間の因果関係を明確にし、このcausal chainに沿ったsecondary metricsを監視する。
      - -> secondary metricsの監視により、**primary decision metricsの変化が、我々が仮定した因果関係通りにプロダクトの変更によって発生しているのかどうかの判断根拠を持てる**...!
        - 例えば、primary decision metricsが改善したが、secondary metricsが改善されなかった場合、primary decision metricsの変化はプロダクトの変更によるものではなく偽陽性(false positive)である可能性がある...!
  - guardrail metrics:
    - 新機能による意図しない悪影響などを監視するためのmetrics。
    - ちなみに「guardrail metrics」という用語は、実験の信用性や妥当性を保証するためのmetricsという文脈でも使われる事もあるが、ブログ内では前者の意味合いで紹介されてた!

ex.) NetflixのUIにおける「Top 10リスト」というプロダクト新機能のテストにおける、primary decision metricsとsecondary metricsの例:

- 1. 核となる施策のアイデア = 「各国や地域で人気のある動画を表示する事で、以下の2つの理由でユーザに利益をもたらすのでは??」
  - 理由1: ユーザ同士が共通の体験ができることで、人気のある動画についてのコミュニケーションを通じて互いにつながる事ができる。
  - 理由2: ユーザがどの動画を見るべきかの選択を助ける事ができる(ようは推薦か:thinking:)
- 2. アイデアを実験で検証可能な仮説に変換して、primary decision metricsを選定する:
  - **検証可能な仮説 = 「$X$ を変更すれば、metric $Y$ が改善されるような形で、ユーザ体験が改善されるのでは?」というstatement(文?)**
  - top 10リストの例でアイデアから変換された仮説:「top 10 listの体験をユーザに表示する事で、ユーザ達が視聴すべき動画を見つけるのに役立ち、ユーザのengagementを向上させる事ができる。」
    - (メモ) ちなみに「engagement」ってどんな概念だっけ??
      - 「**ユーザーとプロダクトの間のつながりの強さ**」や「ユーザーがプロダクトにどれだけ関与しているか」を表す概念。
      - このつながりが強ければ強いほど、ユーザーはそのプロダクトを頻繁に使用し、より深いレベルでの活動を行い、プロダクトに対してポジティブな感情を持つ傾向がある。
      - engagementを表す指標には、active users, retention rate(継続率)などがある...!
  - Netflixにおいてユーザのengagementを測定するmetricは「夜間のサービス利用率」。これが**primary decision metrics**になる。(正確にはengagementのproxyというか代理指標か...! retension rateは短期的に測定可能な指標ではないから...!:thinking:)
    - (Netflixの場合、**このmetricが長期的なユーザのretention確率と相関している事**が分析で判明しているらしく、他の多くのABテストでもprimary decision metricsとして使用されているらしいっぽい。)
- 3. 施策とprimary decision metricsの間の因果関係を監視するためのsecondary metricsを選定する:
  - top 10リストの例でのsecondary metrics: 「ユーザがtop 10 listをクリックした回数」
    - プロダクトの変更「top 10 list機能の追加」と、primary decision metrics「夜間のサービス利用率」の間の因果関係を明確にするために、secondary metricsとして「top10リストに掲載された動画の視聴回数」等が監視される。
      - 仮に、top 10 listのユーザ体験が本当に良いものであるならば、top 10 listに掲載された動画の視聴回数が増加した上で、その結果として強いengagementが得られるはず...!
- 4. 新機能による意図しない悪影響などを監視するためのguardrail metricsを選定する:
  - 例えば、新機能がユーザへ混乱や不満を与えている度合いを示す可能性のある「カスタマーサービスへの接触率」など。

# Webのコントロール実験に関するpracticeをまとめた論文でのOECについて

- OEC(Overall Evaluation Criterion)の定義:

  - 実験の目的(objective)を表す定量的な指標。
  - 類似した用語: Outcome, Evaluation metric, Performance metric, Fitness function, etc.
  - 実験に複数の目的がある場合:
    - 単一のmetricを選択する、もしくは複数の目的を表すmetricsを重み付けした単一の合成metricを用意する事が、非常に望ましく、推奨される。
  - 長期目標はOECの一部であるべき:
    - 良いOECは、短期的な目標だけに焦点を当てるべきではない。むしろ、lifetive valueなどの長期的な目標(goal)を予測する要素を含むべき。
      - (OECは、長期的なgoalと整合するような、短期で測定可能なmetricであるべきってことか...!:thinking:)

- 教訓「Agree on the OEC upfront (OECを事前に合意する)」
  - 教訓の中の 「Culture and business」 セクションにて、OEC関連の話も少し出てきてた!
  - まずコントロール実験の強みは、ビジネスの新機能の価値を客観的に測定できること。
    - そしてこの強みは、**実験前に、関係者が実験をどのように評価するかについて合意できている場合に最もよく発揮される**。
    - しかし、**多くのソフトウェアプロダクトの評価ではしばしば競合する複数の目標があるため、この教訓が適用されていない事がある**。
  - OECは、複数の目標を単一のmetricに変換する combined measure になり得る。しかし、いざOECを策定しようとすると、組織は様々な目標の価値を軽量し、それらの相対的な重要性を決定する必要がある。
  - コントロール実験するうえで必ずしも単一のmetricが必要というわけではないが、こうした事前のハードワークは、組織を整え、goalを明確にする事ができる。
    - (難しいけど単一のOECを作っておけると、意思決定しやすくて最高だよねってことか...!:thinking:)

最後に、OECに関する論文内での励まし(?)として、以下の言葉が述べられていました:)

> Coming up with good OECs is hard, but what is the alternative? The key point here is to recognize this limitation, but avoid throwing the baby out with the bathwater.
> 良いOECを考えるのは難しいが、その代わりに何があるだろうか? ここでの重要なポイントは、この限界を認識しながらも、お風呂の水と一緒に赤ん坊を投げ出さないようにすることである。

# the first Practical Online Controlled Experiments Summit(第一回実践的オンラインコントロール実験サミット)の論文でのOEC metricsに関する議論

- 実験のOECはどうあるべきか?
- OECが、ユーザの不満を増大させるものにペナルティを与えるようにするにはどうするのが良いか?
- OECの良し悪しをどのように評価するべきか?
- ユーザのlong-term value(LTV)を推定するモデル(MLモデルや統計モデルの意味!)がある一方で、OEC metricsを作成するうえでそのようなモデルの活用可能性は??
- 施策によってOEC metricsが改善or悪化された場合、その因果関係を最もよく説明するにはどうすればよいか??

セクション4「OEC: Overall Evaluation Criterion Metric」にて。

## OECを設定する事の価値の話:

- オンラインコントロール実験の重要な利点:
  - 新しいアイデアを評価するうえでの意思決定プロレスを合理化し、より客観的なものにできる事!
- オンラインコントロール実験を行わない場合...
  - あるアイデアの賛成派も反対派も、過去の経験や記憶、特定のビジネスレポートやユーザからのフィードバックの解釈だけを頼りに、議論を進めることになる。
  - 最終的にリーダーが、そのアイデアをship(出荷)するか否かの判断を行う。
  - このような意思決定スタイルは、HiPPO(高給取りの意見)に基づいており、多くのcognitive biases(認知バイアス)に影響されやすい。
- OECを設定する事の価値:

  - HiPPOに基づく意思決定スタイルを、アイデア-ユーザの反応の因果効果に基づく、より客観的なdata-drivenの意思決定スタイルに変える事ができる。
  - 論文内では、**プロダクトに関する全ての実験についてOECを設定する事を推奨**している。(全ての実験でOECを統一すべきって意味??:thinking:)

## 実験で監視するmetricsの話:

- **実験で監視される全てのmetricsがOECの一部というわけではなく、実験結果を分析するには様々な種類のmetricsが必要**。

  - 1. 実験結果が信頼できるものかどうかを判断するためのmetrics (ex. サンプル比率とか)
    - (これも文脈によってはguardrail metricsの一種だよね...!:thinking:)
  - 2. 施策が成功したのか、その影響はどうだったのかを判断するためのmetrics (この一連のmetricsがOECを構成する)
    - (文脈的に、**この論文内ではOECは複数のmetricsの合成metricである事を前提としてるっぽい**...!:thinking:)
  - 3. OEC metricsに加えて、テストされている施策の成功を明確に示すものではないが、悪化させたくないguardrail metrics。
  - 4. 実験のmetricsの残りの大部分は、diagnostic, feature, local metricsと呼ばれるもの。
    - これらのmetricsは、OECの動きの原因を理解するために使われる。
    - (あ、じゃあこれらのmetricsが、netflixさんのブログで言うところのsecondary metricsに相当するのか...!:thinking:)

## OECが考慮すべき重要な特性:

- 良いOECを見つけるのは難しい。
- OECが考慮すべき重要な特性:
  - 1. 第一に、優れたOECは、key product indicators(KPIs)の長期的な向上を示すものでなければならない。
  - 2. 第二に、OECはゲーム化しづらく、プロダクトチームの適切な行動にインセンティブを与えるものでなければならない。
  - 3. 第三に、OEC metricsは敏感でなければならない。
  - 4. 第四に、OEC metricsの計算コストは高すぎてはならない。
  - 5. 第五に、OEC metricsはkey product goalsを推進し得る多様なシナリオを考慮できなければならない。

## SearchとDiscoveryの両方を考慮した評価が難しい話:

- セクション4.2.1「Search vs Discovery」にて。
- 検索エンジンにおけるユーザ体験の良し悪しの評価方法は、アカデミアや多くの検索プロダクトにおいて、長い間研究課題になってる。
  - なんで課題になってるの? -> **各ユーザの行動の意図を理解するのが難しいから**! (SearchなのかDiscoveryなのか!:thinking:)
- ユーザ行動の2種類の意図:
  - **Search** = ユーザがgoal-orientedな意図を持ってプロダクトを訪問して、探してるものを素早く見つけたいケース。
  - **Discovery** = ユーザが特定の何かを探してるのではなくて単にトピックを探求してるような、よりbrowsing的なもしくは新しい情報を発見したいという意図を持ってプロダクトを訪問してるケース。
- 検索体験の評価が難しい(i.e. metricsの選定が難しい...!:thinking:)話
  - 意図によって、観測されたユーザ行動の良し悪しの評価が異なる。
    - ex.「要約スニペット付きの記事リンクをclickしなかった」というユーザ行動が観測された場合:
      - ユーザの意図がSearchの場合 -> ユーザが探してる情報を選んで表示してあげる事ができなかった、negativeな経験と判断すべきかもしれない。
      - ユーザの意図がDiscoveryの場合 -> ユーザが要約を読んで記事の概要を理解しそれ以上の情報が必要ないと判断したことを、positiveな経験と判断すべきかもしれない。
  - 2種類の意図(=goal-orientedなSearch, browsing的なDiscovery)が競合し得る。
    - 例えば、ユーザのDiscovery的な意図を満足させられるように検索エンジンを最適化した場合、Search的な意図を持つユーザの体験がイマイチになり得る。
    - (両者はトレードオフになり得るから評価方法が難しいのか...! セッション毎のユーザの意図を予測・分類できたら良い感じに評価できそうだよね、まあそれがなかなか難しいんだろうけどなぁ...!:thinking:)

## 複数のprodact goalsとトレードオフの話:

- セクション4.2.2「Product Goals and Trade-offs」にて。
- 良い OEC metrics というのは、長期的なプロダクトのKPIやgoalの改善を反映しているべき。
- これはまず、プロダクトのgoalが明確である事を前提とした話。でも、これって簡単な話ではない。
  - **プロダクトのgoalを明確にし組織全体で戦略を一致させるには、多くの努力とエネルギーが必要なので**...!
    - この話には、ユーザが誰なのか、どのようにユーザにサービスを提供するのがベストなのかを定義するような決定も含まれる。
    - 更に、組織はプロダクトの収益化戦略も作らなければならない。
    - **プロダクトのgoalが明確でない場合、プロダクト組織の各サブチームは、他のチームや組織全体のgoalと一致しない独自のgoalを設定する可能性がある**。(うんうん、この現象は想像できる...!:thinking:)
- プロダクトのgoalが明確になっても、多くの企業では**関心のある主要なmetricsが複数個になる**事が多い。そして、**複数個の主要なmetricsをどう相対的に評価するかもまた難しい**。
  - ex.) あるプロダクトが、収益とユーザ幸福度に関するgoalをもつ場合:
    - (つまり、goalの達成度合いを評価する為の主要なmetricsが2つ存在する場合か...!:thinking:)
    - ある新機能が、ユーザ幸福度を高めるが収益を減少させるトレードオフが観測されたとすると、どのような場合にこの新機能をリリースするべきか??
    - この意思決定は、リーダーシップによってケースバイケースで実施される事が多い。
    - でもこの意思決定アプローチは、多くの認知バイアスに影響されやすく、また全体的なプロダクト戦略との一貫性を保つ事が難しい...!
  - 例えばBingのプロダクトチームは、このトレードオフを全体的なプロダクト戦略に合わせて、複数の実験で一貫した意思決定プロセスが使用される事を保証する為に、異なるmetricsを重み付ける事を試みている。
    - (**要するに、複数のgoalを合成した単一のOEC metricの作成を試みてるって話か...! それができたら苦労はしねぇ**...!:thinking:)

## OECの良し悪しを評価する方法の話:

- セクション4.2.3「Evaluating Methods」にて。
- OECが広く採用される為には、OEC metricsの変更を評価するプロセスを確立する事が重要。
  - 組織によっては、OECの変更を検討し、それが優れたOECの特性を保持しているか否かを確認する専門のレビューチームが存在することもある。
- OECの評価プロセスを確立する為のアプローチ達:
  - 1. 過去の実験データを使ってOECの性能を評価するアプローチ:
    - (**要するに、OEC metricsのオフライン実験か...!**:thinking:)
    - かつてプロダクトにpositive、negative、neutralな影響を与えたと認識されている、過去の実験データを用意する。
    - 過去の実験データに対して新旧のOECを適用し、そのOECが十分な感度と正しい方向性でプロダクトへの影響を捉えられるかどうかを評価する。
    - このアプローチの導入事例: Microsoft, Yandex
    - このアプローチの難しいポイント: 信頼性の高いlabel (=positive, negative, or neutral) を持つ、スケーラブルな実験データを作成すること。
  - 2. 意図的なプロダクトの劣化実験:
    - (**こっちは要するにOECのオンライン実験か..!**:thinking:)
    - 意図的なプロダクトを劣化させて、OEC metricsがその劣化によるnegativeな影響を十分な感度で検出できるかどうかを評価する。
    - このアプローチの導入事例: Microsoft, Google (ユーザ体験を意図的に遅くする実験が有名らしい...! 確かBooking.comでもlatencyを意図的に遅くする実験を行ってた気がする、OECを評価する目的ではなかったかもしれないけど...!:thinking:)

## metricsにおける機械学習モデルの活用の話:

- セクション4.2.4「Using Machine Learning in Metrics」にて。
- 組織やチームによっては、**機械学習モデルを組み込んでmetricsを作ろうとする事例**もある。
  - ex.1) ユーザ満足度を定量評価できるmetricsを作るために、ユーザ行動のsequenceデータを入力としたMLモデルを使う事例。
  - ex.2) 複数のｍetricsを組み合わせてより感度の高いOEC metricsを作るために、機械学習モデルを使う事例。
  - ex.3) long-term outcome(たぶんLTVとか??:thinking:)を捉える OEC metrics を作るために、MLモデルを使ってproxy metricsを作ろうとする事例。
    - (確かLTV(lifetime value)って、生存分布分析みたいな、lifetime distributionみたいな統計モデルを使って推定するものなんだっけ...!:thinking:)
- 多くのプロダクトチームは、**限られたエリアで慎重に**これらの方法を試している。
  - **すでに低い枝の果実(=簡単に改善できる部分)がほとんど摘み終わっているような成熟したプロダクト領域**で、より一般的に使用されているらしい。(より複雑なモデルで小さな変化を検出する必要があるような領域)
  - それ以外のプロダクト領域では、通常は、OECとしてより単純なmetricsを使用する方が推奨される。
- metricsの作成にMLモデルを活用することによる懸念:
  - 1. 複雑なモデルであるほど、解釈が難しくなりmetricsが変化した理由を理解しづらくなる。
  - 2. 複雑なモデルであるほど、振る舞いがブラックボックス化し、metricsの信頼性が低下する可能性がある。
  - 3. MLモデルを新しいデータで再学習させると、metricsが突然変化する可能性がある。(再学習の判断が難しい?)
  - 4. 簡単にゲーム化される可能性がある。
