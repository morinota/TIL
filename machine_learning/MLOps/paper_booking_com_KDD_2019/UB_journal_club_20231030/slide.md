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

title: 宿泊予約サービスbooking.comの150個の機械学習モデルの開発運用で得た6つの教訓をまとめた論文(KDD2019)を読んだ
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


## どんな論文??

<!-- - 宿泊予サー約ビスbooking.comの150個の機械学習モデルの開発運用で得た6つの教訓をまとめた論文(KDD2019) -->
- Booking.comの何十ものチームによって開発され、世界中の何億人ものユーザに公開され、厳密なRCTによって検証された、機械学習アプリケーションの成功例約150件の分析を行い、そこで得られた**6つの教訓**を発表した論文:(まず機械学習サービスを開発するチームがいくつもある(?)の凄いな...!:thinking:)
  - 教訓1: Inception: Machine Learning as a Swiss Knife for Product Development
  - 教訓2: Modeling: Offline Model Performance Is Just A Health Check
  - 教訓3: Modeling: Before Solving A Problem, Design It
  - 教訓4: Deployment: Time Is Money
  - 教訓5: Monitoring: Unsupervised Red Flag
  - 教訓6: Evaluation: Experiment Design Sophistication Pays Off

## この論文を選んだモチベーション:

- KDD2019で採択された論文で、どうやら各所で話題になったらしい。()
  - (既に知ってる方もいるかも??)(当時、MLと出会う前の土木工学の学生だった私は全く知らず...!)
- 本論文のユニークな点:
  - MLに関する文献のほとんどは、アルゴリズムや数学的な側面に焦点を当ててる。(自分もこっち読むことが多い)
  - 一方で本論文は、商業的な利益が最優先される産業分野において、どのようにしたらMLが有意義な効果をもたらすことができるかに焦点を当ててる。
  - MLエンジニアとして経験が非常に浅い自分は、こういった「MLでいかにビジネスやプロダクト価値の向上に貢献するか」に関する論文も読んで経験不足を補うべきかもと思った...!:thinking:

# 教訓1: Inception: Machine Learning as a Swiss Knife for Product Development

- 機械学習は、プロダクト開発におけるスイスナイフである(=多機能で色んな用途に使える例えらしい...:thinking:)
- プロダクトの様々な機能の開発/改善の為に、機械学習を様々な文脈(specialized/semantic)で活用し、ビジネス価値を提供できたという話。

## 教訓1の概要: semantic model いいなぁ...

- 特定のusecaseに特化した specialized model
- 様々なusecaseで活用可能性がある **semantic model**
  - 理解しやすい概念をモデル化する(ex. 定量化できていないユーザの特徴を、MLでモデル化する、みたいな??:thinking:)
  - ex) 「ユーザが旅行の目的地に対してどの程度flexibleであるか」を定量化するモデルを作り、**プロダクトチーム全体にdestination-flexibilityの概念を与える**ことで、プロダクトの改善に役立てることができた。(MLチーム以外も理解・活用可能な汎用的な特徴量を作る、みたいなイメージかな...めちゃいいね!:thinking:)
  - **開発に携わる全ての人がsemanticモデルの出力に基づいて**、新機能やパーソナライゼーション、説得力のある意思決定などに使用可能性がある。(semanticなモデルいいなぁ...:thinking:)
- (specialized model と semantic modelはたぶん排反ではない:thinking:)

## 教訓1の概要: 各MLプロジェクトはビジネス価値を提供する

:::: {.columns}

::: {.column width="50%"}

- MLベースのプロジェクトがもたらした直接的な影響(図2より)
  - 調査期間内に成功した全プロジェクト(MLベースか否かに依らず)のビジネス指標改善の中央値を、ベースライン(1.0)とする。
  - 各barは、各model familyによる同指標改善(導入直後 or モデル改善時の測定値)の中央値(ベースラインとの相対値)

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

- 「オフラインでのモデル性能の推定値(横軸)」と「RCTで観察されたビジネス指標(縦軸)」に相関がなかった話。
- 前回発表時のイントロで引用してました!: [ABテストする前に機械学習モデルの性能を確度高く評価したいけど、皆どうやってるんだろう?について色々調べている話](https://morinota.quarto.pub/journal_club_20230904/#/%E4%BB%8A%E5%9B%9E%E3%81%AE%E3%83%86%E3%83%BC%E3%83%9E%E3%82%92%E9%81%B8%E3%82%93%E3%81%A0%E7%B5%8C%E7%B7%AF)
- 今回は割愛します!

:::

::: {.column width="60%"}

![](https://i.imgur.com/TZEaYJu.png)
(論文より引用)

:::

::::

# 教訓3: Modeling:Before Solving A Problem, Design It (問題を解かせる前に、解かせるべき問題をデザインする)

- MLでビジネス課題の解決に貢献するための最初のステップは、**機械学習問題を「設定」すること**だった。
  - モデルを改善するのが最も明白な方法だけど、**問題設定そのものを変える事も有効** という話:thinking:
  - 特に主問題を直接最適化できずに代理問題を解くケース(ex. 推薦)や、主問題自体が曖昧なケース(ex. semantic model)では問題設定が重要:thinking:

## 教訓3の概要: iterationで有効な問題設定を探す

- -> 一般的に**最良の問題設定はすぐに思い浮かぶものではなく、実験のiterationの中で問題設定を変えること**が非常に効果的な方法だった。

:::: {.columns}

::: {.column width="50%"}

- Booking.comでの問題設定の変更例:
  - 滞在時間の長さを予測する回帰問題 $\rightarrow$ 多クラス分類問題。
  - clickログに基づくユーザ嗜好予測 $\rightarrow$ レビューテキストに関するNLP問題。
- 図3は観光地推薦のiterationの経緯:
  - barの長さはビジネス指標の改善度合い(機能導入時との相対値)
  - UI変更等も含めつつ、MLの問題設定(図中の`Algo: hogehoge`)を変更しながら機能を改善した。

:::

::: {.column width="50%"}

![(論文より引用)](https://i.imgur.com/neUw25S.png)

:::

::::

# 教訓4: Deployment: Time Is Money (時は金なり)

- レイテンシーが遅いとユーザとビジネス指標に悪影響だった話。

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

- 課題1:Incomplete(不完全な) feedback:
  - 多くの状況では、完全な正解ラベルを観察することはできない。
  - ex.) あるユーザに2つのプッシュ通知A&Bのどちらかを送るかを選択するモデルの場合、タップしたか否かの正解ラベルは、実際に送信した片方のみ観測できる。送信しなかった方の正解ラベルは観測されない。
- 課題2:Delayed(遅れる) feedback:
  - 推論が行われてから何日も、あるいは何週間も経ってから、正解ラベルが観測される場合もある。
  - ex.) あるユーザに2つのプッシュ通知A&Bのどちらかを送るかを選択するモデルの場合、実際にユーザがプッシュ通知を見るのは、推論してから1日後かもしれない。

## 教訓5の概要: Booking.comがどのように課題に対応しているか

- 前述の課題から、precisionやrecallなどの正解ラベルに依存した指標は不適切-> **正解ラベルに依存しない指標**で推論結果の品質を監視したい...!
  - 「モデルの品質について、それがサービスを提供するときに行う推論結果を見るだけで、何が言えるのだろうか?」 -> Booking.comでは**応答分布分析(=Response Distribution Analysis)**を採用。
  - 応答分布図(Response Distribution Chart, RDC, 要はモデル出力のヒストグラムっぽい)に基づいた手法。
  - (**正常なRDCはこうあるべき、という仮定をヒューリスティックに用意しておく必要がありそう**:thinking:)
- -> 経験的に、応答分布分析は、**モデルの欠陥を早期に発見**できる非常に有用なツールだった。

## 教訓5の概要: 応答分布分析の例(2値分類モデル)

:::: {.columns}

::: {.column width="50%"}

- 応答分布図の典型的なパターン:
  - 単峰分布(図7左上) -> 学習時と推論時のデータの分布に大きく違いがある可能性。
  - 極端な高頻度のmodeを持つ分布(図7右上) -> 学習データに想定外の外れ値が含まれてる可能性。

:::

::: {.column width="50%"}

![](https://i.imgur.com/ZcdTVDi.png)

:::

::::

- 平滑ではない非常にnoisyな分布(図7左下)-> 予測が安定しない。モデルがsparce過ぎる可能性。
- 滑らかな二峰性分布(図7右下) -> 2クラスを上手く区別できていそう。(完璧なモデルは0と1に２つのピークがある想定)

このような感じで、推論結果の品質を、推論直後に、**正解ラベルに依存しない指標で**監視している。

# 教訓6: Evaluation: Experiment Design Sophistication Pays Off (洗練された実験デザインが功を奏す)

- RCT(ランダム比較試験)による実験はBooking.comの文化に根付いている。
- MLプロジェクトも同様にRCTを通して実験され、その効果を検出し、改善のiterationに役立てている。
- MLのRCTを行う際、**モデリング(ex. 推論精度??:thinking:)と実装の選択(ex. latencyとか??:thinking:)がビジネス指標に及ぼす因果効果を分離**する為に、実験デザインを工夫してる話。

## 教訓6の概要: Triggered Analysisの適用

- RCTは、ユーザ集合をcontrol群とtreatment群に分け、それぞれ"変化"と"変化なし"に晒される。
- しかし、**必ずしも全ユーザがtreatment可能(treatable)ではない**。(MLモデルの場合、特定の特徴量を必要とすることがある為、よくある)
  - (ex. 旧モデル=ランダムな旅行先推薦、新モデル=パーソナライズされた旅行先推薦のケース。直近1年間の旅行履歴を特徴量に使用するとして、履歴がないユーザは、treatableではない。よって、分析時にはcontrol群とtreatment群両方から除外する、みたいな??:thinking:)
- -> treatableではないユーザは、サンプルにノイズを加え、観察された効果を希釈してしまう -> **Triggered Analysis**の適用

:::: {.columns}

::: {.column width="50%"}

- 両群のtreatableな(or triggeredな)ユーザだけを分析する。(treatment群のtreatableなユーザは実際にtriggerされるので...!:thinking:) (図8参照)

:::

::: {.column width="50%"}

![](https://i.imgur.com/b501FJx.png)

:::

::::



## 教訓6の概要: TriggerがMLモデル出力値に依存するケースの実験デザイン

- ex)「ユーザの目的地の柔軟性」を定量化するMLモデルのRCTのケース。MLモデルが「柔軟性がある」と判定したユーザにのみ、代替の目的地が推薦される。
  - controll群では新モデルの出力が不明であるため、trigger基準(treatableか否か)を条件付けられず図8の設定は適用できない。
- -> 図9のような3群($C, T_1, T_2$)による実験デザインを採用。

:::: {.columns}

::: {.column width="60%"}

- $C$ は旧モデルを適用。
- 2つのtreatment群 $T_1$ と $T_2$ は新モデルを走らせ、Trigger基準(ex. 出力>0.5)をチェックするが、triggerされた $T_1$ のユーザだけが変化にさらされる。
- $T_2$ には新モデルの出力に関係なく、旧モデルが適用される。

:::

::: {.column width="40%"}

![](https://i.imgur.com/UdXXsQ5.png)

:::

::::

- 統計分析は、$T_1$ と $T_2$ の両方からtriggerされた(=新モデルのtrigger基準を満たした)ユーザだけを用いて実施する。

## 教訓6の概要: モデル精度と計算性能の因果効果を分離する実験デザイン

- 前述の3群のRCTデザインは、MLモデルの**推論精度がユーザ体験に与える因果効果を、latency等の影響から切り離す**方法としても役立つ。

:::: {.columns}

::: {.column width="40%"}

- $C$ と $T_1$ の比較: パフォーマンス低下を含む**新機能の全体的な効果** を測定する。(i.e. 推論結果の精度 & latencyを含めて総合的なUX!:thinking:)(positiveな結果だったらこれだけでGOサインを出せる。)

:::

::: {.column width="50%"}

![(論文より引用)](https://i.imgur.com/J4tmi1g.png)

:::

::::

- $C$ と $T_2$ の比較: 推論結果を共有(旧モデル)。新旧モデルでlatencyの違いの影響を測定できる。
- $T_1$ と $T_2$ の比較: 推論時のlatencyを共有。新モデルの露出だけが異なる。新旧モデルの推論結果の精度の違いの効果を測定できる。

# まとめ

- 宿泊予約サービスbooking.comの150個のMLモデルの開発運用で得た6つの教訓をまとめた論文(KDD2019)
- 教訓1は、プロダクト開発においてMLを色んな用途・文脈で活用できている話だった。(特定のusecaseに特化したspecializedなモデル と 様々なusecaseで活用可能性があるsemanticなモデル... semanticなモデル良いね:thinking:)
- 教訓2は、MLモデルのオフライン評価指標とオンラインでのビジネス指標との間に相関がなかった話。
- 教訓3は、ML問題設定をよく考え続けよう、という話。
- 教訓4は、latency大事という話。
- 教訓5は、MLモデルの推論結果の品質のモニタリングの話。(応答分布分析良いね...!:thinking:)
- 教訓6は、MLモデルの効果を確度高く検出する為に、Triggerd AnalysisとRCTの実験デザイン頑張ってる話。
