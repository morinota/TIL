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

title: (RecSys2022 Best Papers)メディアモデルを考慮したニュース推薦の5つの多様性指標群の論文を読んで、活用可能性に思いを馳せた話
subtitle: 2023/11/22 推薦システム論文読み会
# date:
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 最初に自己紹介

:::: {.columns}

::: {.column width="70%"}

- 発表者: モーリタ (twitter @moritama7431)
- 所属: 株式会社ユーザベース NewsPicks インターン
- Qiita: https://qiita.com/morinota
- github: https://github.com/morinotaK

:::
::: {.column width="30%"}

![](https://pbs.twimg.com/profile_images/1539885839173709824/3RqtaSyu_400x400.jpg){fig-align="center" width=150}

:::
::::

- 博士課程への入学時期に偶然Kaggleをきっかけに推薦システム分野と出会い、趣味で論文読んで実装してブログに上げてた。「推薦システムを趣味ではなく仕事として関わりたい」と思い、NewsPicksさんに機会をもらって休学してインターン中。([インターン1年の振り返りブログ書きましたー!](https://tech.uzabase.com/entry/2023/10/06/150603))
- 興味ある事:
  - 推薦システム周り(より確度の高いオフライン評価とか。最近はNetflixの推薦モデル統合のブログをきっかけに、multi-taskな推薦モデルとか。)
  - MLシステムの設計・開発・運用改善(最近MLOps勉強会を経て、MLOps Maturity AssessmentとかRecSysOpsとかFTP Pipelinesとか気になって調べ中。今の業務もこちらの重みが強い印象なので...!)

## 参考文献:

- 1. メインの論文: [RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf)
- 2. メイン論文の元のやつ: [Recommenders with a Mission: Assessing Diversity in News Recommendations](https://dl.acm.org/doi/10.1145/3406522.3446019)
- 3. (メイン論文の背景にあるやつ!)ニュース推薦の民主的役割のtypologyを提案した論文: [On the Democratic Role of News Recommenders](https://www.tandfonline.com/doi/full/10.1080/21670811.2019.1623700)
- 4. Booking.comの論文: [150 Successful Machine Learning Models: 6 Lessons Learned at Booking.com](https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf)
- 5. News推薦のサーベイ論文: [News Recommender Systems - Survey and Roads Ahead](https://web-ainf.aau.at/pub/jannach/files/Journal_IPM_2018.pdf)
- 6. MLOpsの成熟度を高める為のガイドライン: [MLOps Maturity Assessment](https://mlops.community/mlops-maturity-assessment/)

## どんな論文? 選んだモチベーションは??

- 論文title:[RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf)
- RecSys2022 Best Paper Awards
- 一般的な推薦システムにおける"多様性"は、シンプルに推薦アイテム間の距離指標として表される事が多いが、ニュース推薦における"多様性"を検討する上では、それでは不十分でしょ！(というか、目指すべき点はそれではないでしょ!)って話。
- 本論文の目的は、コンピュータサイエンスにおける"多様性"と、メディアや民主主義の規範的な意味としての"多様性"のギャップを埋めること。
  - 規範的概念としての"多様性"を、異なるニュース推薦モデルの評価や比較に使用可能な5つのmetrics集合 RADio に落とし込む。
- この論文を読んだのは半年前なのですが、推薦モデルの推論品質の監視やオフライン評価に使えないかなーと思いを馳せ始め、皆さんと共有したく選択した。

# 論文の概要紹介

## 導入: ニュース推薦の精度と多様性の話

- 推薦結果の"精度"のみを考慮した推薦システムは、ユーザが以前に見たものと似たものを不当に宣伝し、ユーザを"more of the same"のフィードバックループに閉じ込め得る。そのため**beyond-accuracy指標**として"多様性"の研究が進んでいる。
- 多様性指標として一般的なのは、intra-list-diversity(ILD)(=推薦アイテムリスト間の非類似度)
  - 様々な分野で活用可能だが、民主主義社会におけるメディアの役割を果たす為の"diverseなニュース推薦システム"のニュアンスを完全には表現できない。
- そもそもニュース推薦アルゴリズムの仕事は、増え続けるオンライン情報を**フィルタリング**すること
  - その**フィルタリングの方針は、各メディアの役割によって異なる**。

## 4種のメディアモデルとニュース推薦方針

既存研究では、メディアの民主主義的な使命を以下の**4種類**のメディアモデルとして分類:

- The Liberal(自由主義) model: コンテンツもスタイルも、**ユーザの好みに合わせて**提供する。
  - ユーザが選択した分野での専門性を高める。
- The Participatory(参加主義) model: ユーザが社会で活動するために必要な**共通認識**を、**各ユーザに分かりやすい形で**提供する。
  - ユーザ達が必ずしも同じ記事を見る必要はないが、同じトピック。記事のcomplexity(複雑さ)は、ユーザの好みや能力に合わせて調整。
- The Deliberative (議論主義) model: 現在、**社会的な議論の中心にあるトピック**を選び、**異なる意見や多様な視点**を提供する。
- The Critical(批判主義) model: 普段は届きにくい、**マイノリティなコミュニティの意見や主張**を積極的に提供する。

(各メディアモデルに優劣はなくて、どのモデルに従うかは、メディア企業自身が、そのmissionに従い、民主主義社会で果たしたい役割に応じて決めるべき)

## 5種類のdiversity metrics: RADio

前述した4種のメディアモデルによって"目指すべき多様性"の価値と意味合いが異なる。本論文では、**各メディアモデルが推薦システムに期待する性質**から導出した、**5つのdiversity metrics RADio**を提案:

:::: {.columns}

::: {.column width="50%"}

- Calibration
- Fragmentation
- Activation
- Representation
- Alternative Voices

(論文では、これらの性質を満たす為の導出過程とか考えが丁寧に記述されてた。JS-Divergenceを選ぶ理由とか、rank-awareにする上での重み付け方法の選択とか。)

:::

::: {.column width="50%"}

全metricsに共通する性質:

- distance metric(同一性, 対称性, 三角形の不等式)。
- ２つの離散分布間のJS-Divergence。
- 異なる推薦モデル間や異なるmetric間で比較したいので、全て値域が $[0; 1]$。(0に近いほど2つの分布の距離が近い)
- rank情報を持った離散分布に適用可能。(rank-awareな指標)

:::

::::

## 5種類のdiversity metrics: RADio

RADio = Rank-Aware Divergence metrics (ioは??:thinking:)

![](https://imgur.com/c2eTjvh)

## 5種類のdiversity metrics ① Calibration

:::: {.columns}

::: {.column width="60%"}

- 「推薦記事がユーザの好みとどの程度合っているか」を反映したもの。
  - 推薦記事リストの分布とユーザの閲読履歴の分布の間の距離を意味する。

$$
Calibration = D_{JS}(P^*(c|H), Q^*(c|R))
\\
% = \sum_{c} Q^*(c|R) f(\frac{P^*(c|H)}{Q^*(c|R)})\
$$

:::

::: {.column width="40%"}

![](https://imgur.com/9SOsgiH)

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ は、rankで重み付けされた確率関数である事を意味する。 $H$ は、あるユーザの閲読履歴にある記事集合。$R$ は、推薦記事リスト。$c$ は確率変数。(論文中では、記事categoryや記事のcomplexityを確率変数として提案してたので $c$ にしてるっぽい?)

## 5種類のdiversity metrics ② Fragmentation

:::: {.columns}

::: {.column width="60%"}

- 「共通したトピックの記事を提供できているか」の度合いを反映したもの。
  - 複数ユーザの推薦記事リストの分布間の距離を意味する。(二人のユーザ $u$ と $v$ を比較する)

$$
Fragmentation = D_{JS}(P^*(e|R^{u}), Q^*(e|R^{v}))
% = \sum_{e} Q^*(e|R^v) f(\frac{P^*(e|R^u)}{Q^*(e|R^v)})
$$

:::

::: {.column width="40%"}

![](https://imgur.com/83x6nBJ){width=50%}

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ は、rankで重み付けされた確率関数である事を意味する。 $R^{u}, R^{v}$ は、ユーザuとvの推薦記事リスト。$e$ は、記事のevent(=記事のトピック的な?)を表す確率変数。

## 5種類のdiversity metrics ③ Activation

:::: {.columns}

::: {.column width="60%"}

- 「肯定的な記事ばかり推薦してしまってないか、逆に否定的な記事ばかり推薦してしまってないか」の度合いを反映したもの。
  - 推薦可能な記事プール $S$ と、推薦記事リスト $R$ のactivation score(=positiveかnegativeか)の分布間の距離を表す。

$$
Activation = D_{JS}(P(k|S), Q^*(k|R))
% = \sum_{k} Q^*(k|R) f(\frac{P(k|S)}{Q^*(k|R)})
$$

:::

::: {.column width="40%"}

![](https://imgur.com/68SdgQp){width=50%}

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ は、rankで重み付けされた確率関数である事を意味する。 $k$ は、記事のactivation score(=positiveかnegativeか)を表す確率変数。(論文ではテキストのsentiment analysisで得る事を想定)

## 5種類のdiversity metrics ④ Representation

:::: {.columns}

::: {.column width="60%"}

- 「視点(ex. 政治的トピックや政党の言及など)の多様性」の度合いを反映したもの。
  - 記事プール $S$ と、推薦記事リスト $R$ のviewpoint(離散値を想定) の分布間の距離を表す。

$$
Representation = D_{JS}(P(p|S), Q^*(p|R))
% = \sum_{p} Q^*(p|R) f(\frac{P(p|S)}{Q^*(p|R)})
$$

:::

::: {.column width="40%"}

![](https://imgur.com/H8tORYn){width=50%}

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ はrankで重み付けされた確率関数の意味。 $p$ は 記事のviewpointを表す離散変数。
(記事のメタデータをNLPパイプラインに通してviewpointを作る)

## 5種類のdiversity metrics ⑤ Alternative Voices

:::: {.columns}

::: {.column width="60%"}

- 「意見の声の持ち主(Minority/Majority)の多様性」を反映したもの。(Representationは意見の中身の多様性)
  - Minority/Majorityの例: 非白人/白人, 非男性/男性, etc.
  - 記事プール $S$ と、推薦記事リスト $R$ のviewpointの持ち主の分布間の距離を表す。

$$
AlternativeVoices = D_{JS}(P(m|S), Q^*(m|R))
% = \sum_{m} Q^*(m|R) f(\frac{P(m|S)}{Q^*(m|R)})
$$

:::

::: {.column width="40%"}

![](https://imgur.com/6UO7s2Z){width=50%}

:::
::::

ここで、$P$ と $Q$ は異なる2つの離散確率関数。添字 $*$ はrankで重み付けされた確率関数の意味。 $m \in \{Minority, Majority\}$ は離散変数。

## メディアモデルとRADioの関係

<!-- メディアモデルとmetricsの対応表 -->

![](https://imgur.com/RZ46Wz5){fig-align="center" width=600}

- 異なるアルゴリズムのRADioの各値を比較する事で、開発者はどの手法が各メディアが求める機能に適しているか、定量評価できる。
  - ex) 自由主義モデルはユーザの好みに合わせた情報を提供したい -> 低いCalibrationと高いFragmentation
  - ex) 参加主義モデルは社会で必要な共通認識を各ユーザに分かりやすい形で提供したい -> 高いCalibration(complexity)と低いFragmentation
- 今後の課題:
  - RADioに関連する多くの特徴量の抽出が難しい事(ここはLLMの普及で難易度低下?:thinking:)
  - post-hocな評価ではなく、損失関数として活用可能なmetrics

# ここからはRADioの活用可能性に思いを馳せてみた話

## 推論結果の品質モニタリング

- MLOps Maturity Assessmentの項目4や Booking.comの論文の教訓5でも主張されているが、バッチ推論でもオンライン推論でも推論結果の品質をモニタリングすることは重要
  - (データの分布の変化や、学習・推論パイプラインへのバグの混入などによって、**エラーやlatency等には現れない推論結果の品質の低下にいち早く気づきたい**…!)
- 推薦システムの場合は Incomplete(不完全な) feedbackとDelayed(遅延) feedbackの問題があるので、precisionやrecallなどの正解ラベルに依存した指標は不適切-> **正解ラベルに依存しない指標**で推論結果の品質を監視したい…! -> Booking.comの論文では、応答分布分析を採用してた。
- **RADioはいずれも正解ラベルに依存しない指標なので活用可能では??**(というかRADioは推薦結果の分布を他の分布と比較して評価してるので、応答分布分析と言えるのかも):thinking:
  - 特に自由主義モデルや参加主義モデルのusecaseでは、Calibration(topic)が使いやすそう(ex. 金融の記事を良く読むユーザに金融の記事をたくさん推薦できているか):thinking:

## 推薦モデルのオフライン評価

- ニュース推薦の分野では、metadataとしてテキストが使える事と、ニュースのlifecycleが短く新鮮なcold-start itemを推薦したいusecaseが多い事から、**content-based系の手法**(i.e. id-onlyでない手法)が多く採用されてる。
- しかし、content-based手法はオフライン実験においてprecisionやrecallなどでは正確に評価しづらく、**一方でid-only手法やmost-popular itemsは過大評価されやすい傾向**がある。(参考文献5より)
  - 人気度バイアスとか、Off-Policy Evaluation分野で言うところのlogging policy由来のバイアスとかが原因??:thinking:
  - もちろんunder samplingやOPE推定量による重み付けにより、バイアス除去を試みるアプローチもあるよね:thinking: ただ、OPEのIPS推定量に基づくアプローチはlogging policyが探索的なモデルである必要があるので、決定論的な推薦システムでは活用が難しそう...!:thinking:
- RADioはいずれも正解ラベルに依存しない指標なので、**少なくともid-only手法が過大評価されがち問題は解消できたりしないかな**? :thinking:
  - (あ、でもユーザの閲読履歴は、人気度やlogging policy由来のバイアスの影響を受けているか...! under sampling的なアプローチと組み合わせるのはどうだろう...!:thinking:)

## まとめ:

- ニュース推薦の民主的役割を考慮した5つの多様性指標RADioを提案する論文を読んだ:
  - hoge
- 推論品質の監視とかオフライン評価とかで色々使えないかなーと思いを馳せた:
  - 推薦結果の品質のモニタリング
  - ニュース推薦モデルのオフライン評価

## 参考文献:

- 1. メインの論文: [RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations](https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf)
- 2. メイン論文の元のやつ: [Recommenders with a Mission: Assessing Diversity in News Recommendations](https://dl.acm.org/doi/10.1145/3406522.3446019)
- 3. (メイン論文の背景にあるやつ!)ニュース推薦の民主的役割のtypologyを提案した論文: [On the Democratic Role of News Recommenders](https://www.tandfonline.com/doi/full/10.1080/21670811.2019.1623700)
- 4. Booking.comの論文: [150 Successful Machine Learning Models: 6 Lessons Learned at Booking.com](https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf)
- 5. News推薦のサーベイ論文: [News Recommender Systems - Survey and Roads Ahead](https://web-ainf.aau.at/pub/jannach/files/Journal_IPM_2018.pdf)
- 6. MLOpsの成熟度を高める為のガイドライン: [MLOps Maturity Assessment](https://mlops.community/mlops-maturity-assessment/)
