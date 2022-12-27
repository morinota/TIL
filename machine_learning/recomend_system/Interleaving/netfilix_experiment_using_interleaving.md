## 0.1. link

https://netflixtechblog.com/interleaving-in-online-experiments-at-netflix-a04ee392ec55

## 0.2. title

Innovating Faster on Personalization Algorithms at Netflix Using Interleaving
インターリーブを用いたNetflixのパーソナライゼーションアルゴリズムの高速化

## 0.3. Introduction

The Netflix experience is powered by a family of ranking algorithms, each optimized for a different purpose. For instance, the Top Picks row on the homepage makes recommendations based on a personalized ranking of videos, and the Trending Now row also incorporates recent popularity trends. These algorithms, along with many others, are used together to construct personalized homepages for over 100 million members.
Netflixの体験は、**それぞれが異なる目的のために最適化されたランキングアルゴリズムのファミリー**によって支えられています。例えば、トップページの「Top Picks」列は、パーソナライズされたビデオのランキングに基づいておすすめを表示し、「Trending Now」列には、最近の人気トレンドも組み込まれています。これらのアルゴリズムは、1億人以上の会員のためにパーソナライズされたホームページを構築するために使用されています。

To accelerate the pace of algorithm innovation, we have devised a two-stage online experimentation process.
The first stage is a fast pruning step in which we identify the most promising ranking algorithms from a large initial set of ideas.
The second stage is a traditional A/B test on the pared-down set of algorithms to measure their impact on longer-term member behavior.
In this blog post, we focus on our approach to the first stage: an interleaving technique that unlocks our ability to more precisely measure member preferences.
**アルゴリズム革新のペースを加速**するために、我々は**2段階のオンライン実験プロセス**を考案した。
第一段階は、大規模な初期アイデアセットから最も有望なランキング・アルゴリズムを特定する高速な刈り込みステップです。第2段階は、絞り込んだアルゴリズムに対して従来のA/Bテストを行い、長期的な会員行動への影響を測定します。このブログでは、第1段階のアプローチに焦点を当て、会員の嗜好をより正確に測定する能力を引き出すインターリーブ技術について説明します。

# 1. Faster algorithm innovation with interleaving

Increasing the rate of learning by testing a broad set of ideas quickly is a major driver of algorithm innovation. We have expanded the number of new algorithms that can be tested by introducing an initial pruning stage of online experimentation that satisfies two properties:
幅広いアイデアを迅速にテストすることで学習速度を向上させることは、アルゴリズム革新の主要な推進力である。我々は、**以下の2つの特性を満たすオンライン実験の初期刈り込み段階**を導入することで、テスト可能な新しいアルゴリズムの数を拡大した。

- It is highly sensitive to ranking algorithm quality, i.e., it reliably identifies the best algorithms with considerably smaller sample size compared to traditional A/B testing. **ランキングアルゴリズムの品質に高い感度**を持ち、従来のA/Bテストと比較してかなり少ないサンプル数で確実に最適なアルゴリズムを特定することができます。
- It is predictive of success in the second stage: the metrics measured in the first stage are aligned with our core A/B evaluation metrics. 第2ステージでの成功を予測するものです。第1ステージで測定された指標は、私たちのコアなA/B評価指標と一致しています。

We have achieved the above using an interleaving technique (cf. Chapelle et al.) that dramatically speeds up our experimentation process (see Fig. 2). The first stage finishes in a matter of days, leaving us with a small group of the most promising ranking algorithms. The second stage uses only these select algorithms, which allows us to assign fewer members to the overall experiment and to reduce the total experiment duration compared to a traditional A/B test.
我々は、実験プロセスを劇的にスピードアップするインターリーブ技術（参照：Chapelle et al.）を使用して、上記を達成しました（図2参照）。第一段階は数日で終了し、**最も有望なランキングアルゴリズムの小グループ**を残す。第2段階では、**これらの選択されたアルゴリズムのみ**を使用するため、従来のA/Bテストと比較して、**実験全体のメンバーをより少なく**割り当て、**実験全体の期間を短縮**することができます。

![](https://miro.medium.com/max/720/0*Gw_KOdbFTvBlzQaN.)

Fig. 2: Faster algorithm innovation using interleaving. The world of new algorithms is represented by light bulbs. Among these, there is a winning idea (depicted in red). The interleaving approach allows us to quickly prune down the initial set of ranking algorithms to the most promising candidates, enabling us to conduct experiments a rate much faster than traditional A/B testing to identify winning ideas.
図2：インターリーブによるアルゴリズム革新の高速化。新しいアルゴリズムの数を電球で表現しています(**30種類の推薦モデル**)。この中に、**勝利のアイデア(=要はある一つの素晴らしい推薦モデル)**（赤で描かれている）があります。インターリーブ方式を採用することで、ランキングアルゴリズムの初期セットから最も有望な候補を素早く絞り込み、**従来のA/Bテストよりもはるかに速いスピードで**実験を行い、(30個の推薦モデルから)**勝利のアイデア(赤色のアルゴリズム)を特定**することが可能になります。

# 2. Using a repeated measures design to determine preferences 繰り返し測定のデザインを使って、嗜好を決定する

To develop intuition around the sensitivity gain that interleaving offers, let’s consider an experiment to determine whether Coke or Pepsi is preferred within a population.
インターリーブがもたらす感度の向上について直感的に理解するために、**ある集団の中でコーラとペプシのどちらが好まれるかを判断する実験**を考えてみましょう。

## 2.1. traditional A/B testingのケース

If we use traditional A/B testing, we might randomly split the population into two groups and perform a blind trial.
**従来のA/Bテスト**であれば、**母集団をランダムに2つのグループに分け**、ブラインドテストを行うかもしれません。
One group would be offered only Coke, and the second group would be offered only Pepsi (with neither drink having identifiable labels).
**一方のグループにはコーラだけを、もう一方のグループにはペプシだけを提供**します（どちらの飲み物にも識別できるラベルをつけます）。
At the conclusion of the experiment, we could determine whether there is a preference for Coke or Pepsi by measuring the difference in soda consumption between the two groups, along with the extent of uncertainty in this measurement, which can tell us if there is a statistically significant difference.
実験の終わりに、**2つのグループ間のソーダの消費量の差**と、この**測定における不確実性の程度**を測定することによって、コーラまたはペプシに対する好みがあるかどうかを判断することができます。

While this approach works, there may be opportunities for refining the measurement.
このアプローチは有効ですが、測定をより洗練させる機会もあるかもしれません。

First, there is a major source of measurement uncertainty: the wide variation in soda consumption habits within the population, ranging from those who hardly consume any soda to those who consume copious amounts.
第一に、測定の不確かさの主な原因があります。それは、ソーダをほとんど消費しない人から大量に消費する人まで、**人口内のソーダ消費習慣に大きなばらつきがある**ことです。

Second, heavy soda consumers may represent a small percentage of the population, but they could account for a large percentage of overall soda consumption.
第二に、**ソーダの大量消費者は人口に占める割合は少ない**かもしれませんが、**ソーダの消費量全体では大きな割合を占めている可能性**があります。

Therefore, even a small imbalance in heavy soda consumers between the two groups may have a disproportionate impact on our conclusions.
したがって、**2つのグループ間のヘビーソーダ消費者のバランスが少し崩れただけ**でも、結論に不釣り合いな影響(=Bias!!!)を与える可能性があります。

When running online experiments, consumer internet products often face similar issues related to their most active users, whether it is in measuring a change to a metric like streaming hours at Netflix or perhaps messages sent or photos shared in a social app.
オンライン実験を行う際、消費者向けインターネット製品は、Netflixでのストリーミング時間のような指標の変化や、おそらくソーシャルアプリでのメッセージ送信や写真共有の測定など、その最もアクティブなユーザーに関する同様の問題に直面することがよくあります。

## 2.2. a repeated measures design 反復測定デザイン(=つまりinterleaving...??)

As an alternative to traditional A/B testing, we can use a repeated measures design for measuring preference for Coke or Pepsi.
従来のA/Bテストの代わりに、コーラやペプシに対する嗜好性を測定するために反復測定デザインを使用することができます。
In this approach, the population would not be randomly split.
このアプローチでは、母集団は無作為に分割されません。
Rather, each person would have the option of either Coke or Pepsi (with neither brand having identifiable labels but yet still being visually distinguishable).
むしろ、各人がコーラかペプシのどちらかを選択することになります（どちらのブランドにも識別可能なラベルはありませんが、視覚的に区別することができます）。
At the conclusion of the experiment, we could compare, at the level of a person, the fraction of soda consumption for Coke or Pepsi.
実験終了時に、コーラかペプシか、炭酸飲料の消費割合を一人一人のレベルで比較することができるのです。
In this design, このデザインでは、

- 1. we remove the uncertainty contributed by the wide range in population-level soda-consumption habits, and 1）人口レベルでの**ソーダ消費習慣の幅が広いことによる不確実性**を取り除き、
- 2. by giving every person equal weight, we reduce the possibility that the measurement is materially affected by an imbalance in heavy soda consumers. 2）すべての人に**同じ重みを与える**(...???)ことで、**ソーダの大量消費者の不均衡によって測定が重大な影響を受ける可能性を減らす**ことができます。

# 3. Interleaving at Netflix

At Netflix, we use interleaving in the first stage of experimentation to sensitively determine member preference between two ranking algorithms.
Netflixでは、実験の最初の段階でインターリーブを使って、**2つのランキングアルゴリズム間のユーザの好み**を敏感に判断しています。
The figure below depicts the differences between A/B testing and interleaving.
下図は、A/Bテストとインターリービングの違いを表しています。

In traditional A/B testing, we choose two groups of subscribers: one to be exposed to ranking algorithm A and another to B.
従来のA/Bテストでは、ランキング・アルゴリズムAとBの**2つのグループ**を選びます。

In interleaving, we select **a single set of subscribers** who are exposed to an interleaved ranking generated by blending the rankings of algorithms A and B.
インターリーブでは、**アルゴリズムAとBのランキングをブレンドして生成したインターリーブ・ランキング**に接触する**加入者を1セット選びます**.
This allows us to present choices side-by-side to the user to determine their preference of ranking algorithms.
ユーザーに選択肢を並べて提示することで、ランキング・アルゴリズムの嗜好を判断します。
(**Members are not able to distinguish between which algorithm recommended a particular video.**)
(**会員は、どのアルゴリズムが特定の動画を推奨しているかを区別することができません**)。
We calculate the relative preference for a ranking algorithm by comparing the share of hours viewed, with attribution based on which ranking algorithm recommended the video.
**どのランキングアルゴリズムがその動画を推奨しているかをattribution(=つまりアルゴリズムの持つ属性...?)**とし、視聴時間のシェアを比較することで、ランキングアルゴリズムの**相対的な嗜好性(preference)を算出**しています。

![](https://miro.medium.com/max/720/1*i9VwKzBJewkRsz3oNAfUvQ.webp)

Fig. 3: A/B Testing vs. Interleaving. In traditional A/B testing, the population is split into two groups, one exposed to ranking algorithm A and another to B. Core evaluation metrics like retention and streaming are measured and compared between the two groups. In contrast, interleaving exposes one group of members to a blended ranking of rankers A and B. User preference for a ranking algorithm is determined by comparing the share of viewing hours coming from videos recommended by rankers A or B.
図3：A/Bテストとインターリーブとの比較。従来のA/Bテストでは、**母集団を2つのグループに分け**、一方にはランキング・アルゴリズムAを、もう一方にはランキング・アルゴリズムBを適用し、リテンションやストリーミングなどのコア評価指標を測定して2グループ間で比較する。一方、インターリーブでは、1つのグループにランカーAとBの混合ランキングを公開し、**ランカーAまたはBが推奨する動画からの視聴時間の割合を比較**することで、**ランキングアルゴリズムに対するユーザーの好み(=このユーザはアルゴリズムAとアルゴリズムBのどちらを好むか...?)**を決定します。

## 3.1. position bias(位置バイアス)の存在

When generating an interleaved set of videos from two ranking algorithms A and B for a row on the Netflix homepage, **we have to consider the presence of position bias**: the probability of a member playing a video decreases as we go from left to right.
Netflixのホームページの1列に対して、**2つのランキングアルゴリズムAおよびBから動画のインターリーブセットを生成**するとき、**位置バイアスの存在を考慮する必要**があります。
位置バイアス:Netflixの場合、メンバーがビデオを再生する確率は左から右に行くほど低くなります。

For interleaving to yield valid measurements, we must ensure that at any given position in a row, a video is equally likely to have come from ranking algorithm A or B.
interleavingが**有効な測定値をもたらす**ためには、行の**任意の位置で、動画がランキングアルゴリズムAまたはBから来た"可能性が等しくなるように"(=i.e. 条件がフェアになるように...??)**しなければなりません。

## 3.2. position biasを取り除く為の工夫

To address this, we have been using a variant of team draft interleaving, which mimics the process of how team selection occurs for a friendly sports match.
そこで、スポーツの親善試合で行われるチーム選択のプロセスを模倣した、**チームドラフトのインターリーブという変種**を使用しています。

In this process, two team captains toss a coin to determine who picks first.
この方法では、2人のチームのキャプテンがコインを投げて、どちらが先に指名するかを決めます。
They then alternate picks, with each captain selecting the player who is highest on their preference list and is still available.
そして、それぞれのキャプテンが、自分の希望する選手リストの中で最も高く、まだ指名可能な選手を交互に指名します。
This process continues until team selection is complete.
このプロセスは、チームの選択が完了するまで続けられます。
Applying this analogy to interleaving for Netflix recommendations, the videos represent the available players and ranking algorithms A and B represent the ordered preferences of the two team captains.
このアナロジーを Netflix のレコメンデーションに適用すると、**ビデオは利用可能な選手**、**ランキングアルゴリズム A と B は 2 人のチームキャプテンの好みの順番**を表しています。
We randomly determine which ranking algorithm contributes the first video to the interleaved list.
どちらのランキングアルゴリズムがインターリーブされたリストに最初のビデオを提供するかをランダムに決定します。
The ranking algorithms then alternate, with each algorithm contributing their highest-ranked video that is still available (see Fig. 4).
その後、ランキングアルゴリズムが交互に、各アルゴリズムがまだ利用可能な最高ランクのビデオを提供する（図4参照）。
The member preference for ranking algorithm A or B is determined by measuring which algorithm produced the greater share of hours viewed within the interleaved row, with views attributed to the ranker that contributed the video.
「**ランキング・アルゴリズムAまたはBのユーザの好み**」は、**インターリーブされた列の中で、どちらのアルゴリズムがより多くの視聴時間を生み出したか**を測定することによって決定され、視聴はビデオを提供したランカーに帰着します。

![](https://miro.medium.com/max/720/0*NvBopWcAdHnjzgkr.)

Fig. 4: Interleaving videos from two ranking algorithms using team draft. Ranking algorithms A and B will each have an ordered set of personalized videos. We start with a random coin toss that determines whether ranking algorithm A or B contributes the first video. Each algorithm then takes turns contributing the highest ranked video that is not yet in the interleaved list. Two possible outcomes for the interleaved list are shown depending on which ranker got to select first. We measure user preference by comparing the share of viewing hours attributed to each ranking algorithm.
図4: チームドラフトを用いた2つのランキングアルゴリズムからのビデオのインターリーブ。ランキングアルゴリズムAとBは、それぞれパーソナライズされたビデオの順序付きセットを持っています。まず、ランダムなコイントスにより、ランキング・アルゴリズムAとBのどちらが最初のビデオを提供するかを決定します。その後、各アルゴリズムは**交互**に、**まだインターリーブリストにない最高ランクのビデオ**を投稿する。どちらのランキングアルゴリズムが最初に選択したかによって、インターリーブされたリストの2つの可能な結果が表示されます。**各ランキング・アルゴリズムに帰属する視聴時間のシェアを比較**することで、ユーザの嗜好(=このユーザには、アルゴリズムAとBのどちらを適用するべきか??)を測定する。

# 4. Comparing the sensitivity of interleaving to traditional A/B testing インターリービングの感度を従来のA/Bテストと比較する

## 4.1. 必要なサンプル数に関する実験

The first requirement that we laid out for using interleaving in a two-stage online experimentation process was that it needs to **reliably identify the better ranking algorithm with a considerably smaller sample size**.
2段階のオンライン実験プロセスでインターリービングを使用するための最初の要件は、**かなり少ないサンプルサイズでより良いランキングアルゴリズムを確実に特定**する必要があるということであった。

To evaluate how well interleaving satisfies this requirement, we turned to a case in which two ranking algorithms A and B were of known relative quality: **ranker B is better than ranker A**. We then ran an interleaving experiment in parallel with an A/B test using these 2 rankers.
「Interleavingが本当に↑の要件を満たすかどうか」を評価する為に、2つのランキングアルゴリズムA、Bの相対的品質が既知である場合、つまり**ランカーBがランカーAより優れている場合**に着目し、この2つのランカーを用いたA/Bテストと並行してインターリーブ実験を実施しました。

To compare the sensitivity of interleaving vs. A/B testing, we computed both the interleaving preference and A/B metrics at various sample sizes using **bootstrap subsampling**.
インターリーブとA/Bテストの**感度を比較する**ために、**ブートストラップ・サブサンプリング**を用いて、**さまざまなサンプルサイズにおいてインターリーブの嗜好性とA/Bの指標の両方を計算**しました。

In performing the bootstrap analysis, we either simulated assigning N users to the interleaving cell or N/2 users to each cell of the traditional A/B experiment.
ブートストラップ分析では、インターリービングのセルに**N人**のユーザーを割り当てるか、従来のA/B実験の各セルに**N/2人**のユーザーを割り当てるかのどちらかをシミュレートしました。

If we were to randomly guess which ranker is better, the probability of disagreeing with the true preference would be 50%.
もし、**どのランカーが良いかをランダムに推測すると、真の好みと異なる確率は50%**になる。(まあコイントスだからわかる...!)

When this probability is 5%, we are achieving 95% power to detect the difference in ranker quality.
この確率が5%のとき、ランカー品質の差を検出する検出力が95%に達していることになる。
Therefore, a metric that crosses this threshold with a fewer number of subscribers is the more sensitive one.
したがって、**より少ない購読者数でこの閾値を越える指標**は、より感度の高いものであると言えます。

## 必要なサンプル数に関する実験結果

Figure 5 shows the results from our analysis. We compare the interleaving preference with two metrics typically used in the A/B setting: overall streaming and an algo-specific engagement metric.
図5は、私たちの分析結果を示しています。インターリーブ優先度を、**A/B設定で通常使用される2つのメトリクス**(すなわち全体的なストリーミング(Streaming)とアルゴ固有のエンゲージメントメトリクス(Algo Engagement))と比較しています。
The sensitivity of metrics used to evaluate A/B tests can vary over a wide range.
A/Bテストの評価に使用されるメトリクスの感度は、広い範囲で変化する可能性があります。
We find that interleaving is very sensitive: it requires >100× fewer users than our most sensitive A/B metric to achieve 95% power.
インターリーブが非常に高感度であることは、95%のパワーを達成するために、最も高感度なA/Bメトリックよりも100倍以上少ないユーザーを必要とすることからもわかります。

![](https://miro.medium.com/max/720/0*-J01hMSubMnHdRgV.)

Fig. 5: Sensitivity of interleaving vs. traditional A/B metrics for two rankers of known relative quality. Bootstrap subsampling was used to measure the sensitivity of interleaving compared to traditional engagement metrics. We find that interleaving can require >100× fewer subscribers to correctly determine ranker preference even compared to the most sensitive A/B metric.
図5：相対的な品質が既知の2つのランカーに対するインターリーブの感度と従来のA/Bメトリクス。
ブートストラップサブサンプリングは、従来のエンゲージメントメトリクスと比較してインターリーブの感度を測定するために使用されました。
インターリービングは、最も感度の高い A/B メトリクスと比較しても、ランカーの好みを正しく判断するのに必要な購読者数が 100 倍以上少ないことがわかります。

# 5. Correlation of interleaving metrics with A/B metrics インターリーブ指標とA/B指標の相関性

## InterleavingとA/Bテスト結果の整合性に関する実験

Our second requirement was that the metrics measured in the interleaving stage need to be aligned with our traditional A/B test metrics. We now evaluate whether the interleaving preference is predictive of a ranker’s performance in the subsequent A/B test.
2つ目の要件は、**インターリーブ段階で測定されるメトリクスが、従来のA/Bテストのメトリクスと整合**している必要があることでした。次に、インターリービングの嗜好が、その後のA/Bテストにおけるランカーのパフォーマンスを予測できるかどうかを評価します。

## 結果

The figure below shows the change in the interleaving preference metric versus the change in the A/B metric compared to control.
下図は、インターリーブプリファレンス指標の変化と、A/B指標の変化をコントロールと比較して示したものです。
Each data point represents a ranking algorithm that is evaluated against the production ranker, which serves as control.
各データポイントは、コントロールとして機能するプロダクションランカーに対して評価されたランキングアルゴリズムを表しています。
We find that there is a very strong correlation and alignment between the interleaving metric and our most sensitive A/B evaluation metric, giving us confidence that the interleaving preference is predictive of success in a traditional A/B experiment.
**インターリーブ評価指標と最も感度の高いA/B評価指標との間には非常に強い相関**と整合性があることがわかり、インターリーブ選好が従来のA/B実験における成功を予測するものであることが確信されます。

![](https://miro.medium.com/max/720/0*7zUlANjU7v4CNAMv.)

Fig 6: Correlation of the interleaving measurement with the most sensitive A/B metric. Each point represents measurements for a different ranking algorithm evaluated against the production algorithm. There is a strong correlation between the interleaving preference measurement and our most sensitive A/B metric
図6：インターリーブ測定値と最も感度の高いA/Bメトリックの相関。各ポイントは、生産アルゴリズムに対して評価された、異なるランキングアルゴリズムの測定値を表しています。インターリーブ・プリファレンス測定と最も感度の高いA/Bメトリクスの間には強い相関があります。

# 6. Conclusion

Interleaving is a powerful technique that has enabled us to accelerate ranking algorithm innovation at Netflix.
インターリーブとは、Netflixのランキングアルゴリズムのイノベーションを加速させる強力な技術です。
It allows us to sensitively measure member preference for ranking algorithms and to identify the most promising candidates within days.
この手法により、ランキング・アルゴリズムに対するメンバーの好みを敏感に察知し、最も有望な候補を数日以内に特定することができます。
This has enabled us to quickly test a broad set of new algorithms, and thus increase our rate of learning.
これにより、新しいアルゴリズムの幅広いセットを迅速にテストすることができ、学習率を高めることができました。

While interleaving provides an enormous boost in sensitivity and aligns well with A/B metrics, **it does have limitations**.
インターリーブは感度を大幅に向上させ、A/B評価指標にも合致していますが、**限界もあります**。

- First, implementing an interleaving framework can be fairly involved, which presents challenges from an engineering perspective.まず、**インターリーブ・フレームワークの実装はかなり複雑**で、エンジニアリングの観点からは困難です。
  - The presence of business logic can furthermore interfere, which requires building scalable solutions for consistency checks and automated detection of issues. さらに、ビジネスロジックが存在する場合、一貫性チェックと問題点の自動検出のためのスケーラブルなソリューションの構築が必要になります。
- Second, while interleaving enables quick identification of the best ranking algorithms, **a limitation is that it is a relative measurement of user preference for a ranking algorithm**. 第二に、インターリービングは最適なランキングアルゴリズムを迅速に特定することができますが、ランキングアルゴリズムに対するユーザーの好みを**相対的に測定するものであるという限界**があります。
  - That is, it does not allow us to directly measure changes to metrics such as retention. **つまり、リテンションなどの指標の変化を直接測定**することができない。(i.e. あくまで相対的な値!)

We address **the latter limitatio**n by running an **A/B experiment in a second phase**, where our initial set of ideas has been pruned to the best candidates.
**後者の制限**については、最初のアイデアセットを最適な候補に刈り込んだ**第二段階で、A/B実験を行うことで対処**している。
This gives us the option to power up the experiment by increasing the sample size per cell, which enables us to perform careful measurements of longer-term member behavior.
これにより、**セルあたりのサンプル数を増やして(=つまり第一段階で候補数を大きく削っているから??)実験をパワーアップ**させ、より長期的なメンバーの行動を注意深く測定することが可能になります。
Addressing these challenges and developing better measurements are aspects that we are continuing to explore.
このような課題に取り組み、より優れた測定方法を開発することは、私たちが引き続き探求している点です。

If the work described here sounds exciting to you, please take a look at the jobs page. We are always looking for talented data scientists and researchers to join our team and help innovate on experimentation methods at Netflix. Your work will help shape the product experience for the next 100M members worldwide!
ここに書かれている仕事がエキサイティングに思えるなら、ぜひ求人ページをご覧ください。私たちは常に、才能あるデータサイエンティストや研究者がチームに加わり、Netflixでの実験手法の革新に貢献してくれることを求めています。あなたの仕事は、今後世界中の1億人の会員のための製品体験を形成するのに役立ちます
