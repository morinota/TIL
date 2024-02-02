## link リンク

https://blog.twitter.com/engineering/en_us/a/2016/power-minimal-detectable-effect-and-bucket-size-estimation-in-ab-tests
https://blog.twitter.com/engineering/en_us/a/2016/power-minimal-detectable-effect-and-bucket-size-estimation-in-ab-tests

# Power, minimal detectable effect, and bucket size estimation in A/B tests A/Bテストにおける検出力、最小検出効果、バケットサイズの推定

Bucket size estimation for A/B experiments
A/B実験のバケットサイズ推定

In previous posts, we discussed how to detect potentially biased experiments, and explored the implications of using multiple control groups.
以前の投稿では、偏りの可能性のある実験を検出する方法について述べ、**複数の対照群を用いることの意味**を探った。
This post describes how Twitter’s A/B testing framework, DDG, addresses one of the most common questions we hear from experimenters, product managers, and engineers: how many users do we need to sample in order to run an informative experiment?
この投稿では、TwitterのA/BテストフレームワークであるDDGが、実験担当者、プロダクトマネージャー、エンジニアからよく聞かれる質問の1つにどのように対応しているかについて説明します: **有益な実験を行うには、何人のユーザをサンプリングする必要がありますか？**

From a statistical standpoint, the larger the buckets, the better.
統計的な観点から言えば、バケツは大きければ大きいほどいい。
If all we cared about was how reliably and quickly we could observe a change, we would run all tests at a 50/50 split, which is not always advisable.
どれだけ確実に、どれだけ早く変化を観察できるかだけを重視するなら、すべてのテストを半々で実施することになるが、これは必ずしも望ましいことではない。
New features have risk, and we want to limit risk exposure.
新機能にはリスクが伴う。
Also, if experimental treatments change as we iterate on designs and approaches, we might confuse a lot of users.
また、デザインやアプローチを繰り返すうちに実験的な治療が変化すると、多くのユーザを混乱させる可能性がある。

Additionally, if all experiments ran at a 50/50 split, our users could wind up in multiple experiments simultaneously, making it difficult to reason what anyone should be experiencing at any given time.
さらに、**すべての実験が半々の割合で行われた場合、ユーザは同時に複数の実験に参加することになり、どの時点で誰が何を経験すべきかを推論することが難しくなる**。(なるほど...!)
Thus, if 1% of the traffic is sufficient to measure effect of changes, we would prefer to use only 1%.
したがって、**変化の影響を測定するのに1％のトラフィックで十分であれば、1％のみを使用する方が望ましい**。
However, if we pick too small a bucket, we might not be able to observe a real change, which will affect our decision-making and/or slow down iteration while we re-run the experiment with larger buckets.
しかし、あまりに小さなバケツを選ぶと、実際の変化を観察することができないかもしれない。

To address this problem, we created a special tool to provide guidance for experimenters on sizing their experiment appropriately, and to alert them when experiments are likely to be underpowered.
この問題に対処するため、私たちは特別なツールを作成し、**実験者に実験の適切なサイジング**に関するガイダンスを提供し、実験がpower(検出力)不足になりそうな場合に警告を発するようにした。

## Prior art

先行技術

There are many different experiment sizing and power calculation tools available online.
ネット上には、さまざまな実験サイズや検出力の計算ツールがある。
They tend to either explicitly ask the experimenter the sample mean and standard deviation (in addition to overall population size) or they address “click through rate” (CTR) or “conversion” — binary-valued metrics (either 1 or 0) for which variance is easy to calculate given the ratio of 1s to 0s.
それらは、実験者にサンプル平均と標準偏差（全体の人口サイズに加えて）を明示的に尋ねるか、あるいは「クリックスルー率」（CTR）や「コンバージョン」を扱う傾向がある。これらは、バイナリ値（1または0）の指標であり、1と0の比率(=二項分布におけるパラメータ pのこと...!)が与えられれば分散を簡単に計算できる。(=二項分布の分散は $p(1-p)$ だっけ? とにかくpから導出できる)

None of these were straightforward to incorporate into our experiment creation workflow, for two reasons:
これらのいずれも、2つの理由から、私たちの実験作成ワークフローに簡単に組み込むことはできなかった。

1. **Non-binary metrics**: Many metrics we track are not ones that can be described in terms of CTR.
   バイナリではないメトリクス： 私たちが追跡している多くの指標は、CTRで説明できるものではありません。
   For example “proportion of people who ‘like’ a Tweet” is a binary metric, a user either hits the ‘like’ button at some point, or she does not.
   例えば、「あるツイートに『いいね！』を押した人の割合」は、ユーザがある時点で『いいね！』ボタンを押すか、押さないかのbinary metricである。
   “Average number of Tweets people ‘like’” is a non-binary metric.
   「人々が "いいね！"したツイートの平均数」は、non-binary metricである。
   A user can like many Tweets.
   ユーザーは多くのツイートに「いいね！」を押すことができる。
   Variance of such metrics can’t be calculated directly from the metric value, and isn’t something an experimenter is likely to have at hand.
   このようなmetricsの分散は、メトリック値から直接計算することはできず、実験者が手元に取得している可能性は低い。

2. Targeted Experiments: When observing an experiment, a naive estimate of variance of a metric would be calculating the metric across the full population, and recording the observed variance.
   ターゲットを絞った実験: 実験を観察するとき、素朴にmetricの分散を推定すると、全人口にわたってmetricを計算し、観測された分散を記録することになる。
   However, as described in an earlier post, Twitter experiments use “trigger analysis” — only subsets of users who trigger specific features are included in an experiment.
   しかし、以前の記事で説明したように、ツイッターの実験では「**トリガー分析**」が使われる。つまり、**特定の機能をトリガーしたユーザのサブセットだけが実験に含まれる**。(ex. プッシュ通知開封後の導線改善のABテストの場合、triggerはプッシュ通知を開封すること)
   These sub-populations frequently have different values for important metrics than does the overall Twitter population (this is intuitive: people who tap the “New Tweet” icon are a-priori more likely to send a Tweet than those who do not!).
   **このような小集団は、重要なmetricsについて、Twitter全体の人口とは異なる値を持つことが多い** (これは直感的である：「新しいツイート」アイコンをタップする人は、ツイートしない人よりもツイートする可能性が高い！)。
   Since an experimenter can instrument the code to trigger an experiment at practically any place in the app, pre-calculating variances for each metric at each possible trigger point is unrealistic.
   実験者は、アプリの実質的にどの場所でも実験をトリガーするようにコードを計装化することができるので、可能性のあるトリガーポイントごとに各metricの分散を事前に計算することは現実的ではない。

## A quick review of statistical power 統計的検出力の簡単な復習

Let’s first define a few terms.
まず、いくつかの用語を定義しよう。

Null hypothesis is the hypothesis that the treatment has no effect.
帰無仮説とは、treatmentに効果がないという仮説のことである。
An A/B test seeks to measures a statistic for control and treatment, and calculates the probability that the difference would be as extreme as the observed difference under the null hypothesis.
A/B検定は、controlとtreatmentの統計量を測定し、帰無仮説の下で、観測された差くらい極端な差が生じる確率を計算する。
(p値が確率なのか割合なのかは、そんなに重要じゃない気がしてきた。「**観測された差が、帰無仮説の元でどれくらい起こりうることなのかの度合い**」を表してる。それが 20回のうちx回おこるような割合でもいいし、x/20みたいな確率としてでもいい気がする...!)

This probability is called the p-value.
この確率はp値と呼ばれる。
We reject the null hypothesis if p-value is very low.
p値が非常に小さい場合は帰無仮説を棄却する。
The conventional threshold for rejecting the null hypothesis is 5%.
帰無仮説を棄却するための従来の閾値は5％である。

Power is the probability that an experiment will flag a real change as statistically significant.
検出力とは、実験が実際の変化を統計的に有意であると判定する確率のことである。
The convention is to require 80% power.
慣例では80％の検出力が必要とされる。
Power depends on magnitude of the change, and variance among samples.
検出力は、変化(effect size, 効果量)の大きさとサンプル間の分散に依存する。

True effect is the actual difference of mean between the buckets that would have been observed if we had infinitely large sample sizes.
**真の効果(True effect)**とは、サンプルサイズが無限に大きかった場合に観察されたであろう、バケツ間の平均値の実際の差のことである。(=controlの確率分布とtreatmentの確率分布の期待値の差:thinking:)
It’s a fixed but unknown parameter, which we are trying to infer.
それは**固定されているが未知のパラメータであり、我々はそれを推測しようとしている**。
The difference we compute from the samples is called the observed effect and is an estimate of the true effect.
サンプルから計算された差は、**observed effect(観測された効果)**と呼ばれ、true effectの推定値である。
Given sample size and sample variance, we can calculate the smallest real effect size which we would be able to detect at 80% power.
標本サイズと標本分散が与えられれば、80％の検出力で検出できる最小の実際のeffect sizeを計算することができる。
This value is called the minimal detectable effect with 80% power, or 0.8 MDE.
この値は、検出力80％の**minimal detectable effect(検出可能な最小効果)**、すなわち0.8 MDEと呼ばれる。

The graph below — which applies to a one-sided two sample t-test — helps us visualize all this.
以下のグラフは、片側2標本のt検定に適用されるもので、これを視覚化するのに役立つ。
The two bell-shaped curves represent the sampling distribution of the standardized mean difference, under the null hypothesis (red) and the alternative (green) respectively.
2つの釣鐘型の曲線は、それぞれ帰無仮説（赤）と対立仮説（緑）の下でのstandardized mean difference(=treatment平均 - control平均を標準化した確率変数...!)のサンプリング分布を表している。

![]()

The umber-colored area illustrates false positives — the 5% chance of getting a measurement under the null hypothesis that is so far from the mean that we call it statistically significant.
灰色で示した部分は false positive を示している。つまり、**帰無仮説の下で(=が正しい場合に)、平均から遠い測定値を統計的に有意と呼んでしまう5％の確率**である。
The green area illustrates the 80% of time we call statistical significance under the alternative.
緑色の領域は、対立仮説の下で(=が正しい場合に)、統計的に有意と呼ぶ80％の確率を示している。
Note there’s a lot of red and green to the left of the MDE
MDEの左側には、たくさんの赤と緑があることに注意しよう。
— it is possible to observe a statistically significant change that is less than “minimal detectable effect” under the conventional cutoff values of 0.05 p-value and 0.8 MDE
従来のcutoff値である0.05 p値と0.8 MDEの条件下では、minimal detectable effectよりも小さい統計的に有意な変化を観測することが可能である
(you can’t observe it as often as 4 out of 5 times, but you can still happen to observe it).
(5回中4回の頻度では観測することはできないが、観測する可能性はある)(それはそう、MDE 0.8よりも小さい効果だから...!:thinking:)

We can represent false positive rate and power (of a two-sided test) in the following way:
(両側検定の)false positive rateとpowerは、次のように表すことができる。

$$
\text{False Positive Rate} = \mathbb{P}(||\frac{\bar{X} - \bar{Y}}{SD(\bar{X} - \bar{Y})}|| > C | \mu_{1} = \mu_{2})
$$

$$
\text{Power} = \mathbb{P}(|\frac{\bar{X} - \bar{Y}}{SD(\bar{X} - \bar{Y})}| > C | \mu_{1} \neq \mu_{2})
$$

As experimenters, we want to increase our power and decrease the false positive rate.
実験者としては、**検出力を高め、偽陽性率を下げたい**。
Low statistical power means we can miss a positive change and dismiss an experiment that would have made a difference.
統計的検出力が低いということは、肯定的な変化を見逃し、違いがあったであろう実験を却下する可能性があるということだ。
It also means we can miss a negative change, and pass through as harmless an experiment that in fact hurts our metrics.
また、ネガティブな変化を見逃し、無害な実験と見せかけて、実際には指標に悪影響を及ぼすこともある。

Ensuring we can get sufficient power is a critical step in experiment design.
**十分な検出力を確保すること**は、実験計画における重要なステップである。

## Sizing an experiment 実験のサイジング

There is one big lever we can use to get desired power: the bucket size.
望みの検出力を得るために使える大きなレバー(=ようはハイパーパラメータ?)がひとつある： バケツの大きさだ。
We want to allocate enough traffic that we can detect the effect, but not so much that we’re practically shipping the feature.
効果を検出できるだけのトラフィックを割り当てたいが、実際にはその機能を出荷しているようなものではない。
To figure out how large our bucket sizes need to be, let’s take another look at the power formula.
バケツの大きさを決めるために、検出力の式をもう一度見てみよう。
Assuming a false positive rate of 5% and a two-tailed test, we see that power can be represented by:
偽陽性率5%、両側検定と仮定すると、検出力は次式で表される：

$$
\text{Power} = \mathbb{P}(Z > 1.96 - \frac{|\mu_{1} - \mu_{2}|}{\sqrt{\sigma_{1}^{2}/n + \sigma_{2}^{2}/m}}) + \mathbb{P}(Z < -1.96 + \frac{|\mu_{1} - \mu_{2}|}{\sqrt{\sigma_{1}^{2}/n + \sigma_{2}^{2}/m}})
$$

Here, Z is the distribution of the standardized mean difference.
ここで、Zはstandardized mean differenceの分布である。(1.96は平均0 & 分散1 の標準正規分布の $1 - cdf(0.025)$ の値だっけ...?? :thinking:) (1.96から何かしら減算してるのは、標準正規分布を平行移動させたいから...!)
The difference of mus is the true effect size, and sigmas represent the standard deviation of the metrics in control and treatment buckets, respectively.
$\mu$ の差はtrue effect size(真の効果量)であり、$\sigma$ はそれぞれcontrolとtreatmentのバケツのmetricsの標準偏差を表している。
Sizes of each bucket are represented by n and m.
各バケットのサイズはnとmで表される。
Finally, 1.96 is the C from above when we set false positive rate to 5% (the curious can find derivation in any statistics textbook).
最後に、1.96は、偽陽性率を5％に設定した場合の前述式のCである（興味のある人は、統計の教科書で導出を見つけることができる）。(これはだから、平均0 & 分散1 の標準正規分布の $1 - cdf(0.025)$ の値だよね...!)

Given this equation, we can make a few assertions on how to increase power:
**この方程式を前提にすれば、検出力を向上させる方法についていくつか主張することができる**:

- The larger the true effect size, the larger the power.
  true effect sizeが大きければ大きいほど、検出力も大きくなる。
- The smaller the variance, the smaller the sigma, the larger the power.
  分散が小さければ小さいほど、シグマが小さければ小さいほど、検出力は大きくなる。
- The larger the sample size, the larger the power.
  サンプルサイズが大きければ大きいほど、検出力も大きくなる。

If we use the convention of requiring power to be at least 80%, and make the simplifying assumptions that we have equal bucket sizes (n = m) and that the sigmas are the same, we can derive a nice formula for sample size n, as a function of true effect size and variance (via Kohavi et al [1]).
検出力が少なくとも80％必要であるという慣例を用い、**バケットサイズが等しく($n = m$)、$\sigma$ が同じであるという単純化した仮定**を行うと、**true effect sizeと分散の関数**として、サンプルサイズ $n$ の素敵な式を導くことができる。(Kohavi et al [1]による)

$$
n = 15.7 \times (\frac{\sigma}{\Delta})^{2}
$$

With this simplified formula in place, we need to get a handle on delta and sigma — the true effect size and standard deviation, respectively.
この簡略化された公式をもとに、$\Delta$ と $\sigma$ 、つまり、**true effect sizeと標準偏差を把握する必要がある**。
(ここで標準偏差は、controlとtreatmentのバケツのmetricsの標準偏差の平均値を指している。標準偏差が同じという仮定)
(検定したいmetricがbinary metricの場合は、true effect sizeさえ把握すれば、標準偏差は 導出できるんだっけ...?? :thinking:)

## Bucket size estimation tool

バケットサイズ推定ツール

Since we can’t rely on collecting metric variance or standard deviation for the specific sampled populations directly from the experimenters, we created a tool that can make suggestions based on basic data the experimenter can get more easily.
私たちは、実験者から直接、特定のサンプリングされた母集団の計量分散や標準偏差を収集することに頼ることができないので、**実験者がより簡単に入手できる基本的なデータに基づいて提案を行うことができるツール**を作成しました。

The key insight is that while in theory, an experiment can be instrumented anywhere in the app, many product teams at Twitter tend to instrument experiments in relatively few decision points.
重要な洞察は、理論的にはアプリのどこにでも実験を組み込むことができるが、Twitterの多くのプロダクトチームは、比較的少数の意思決定ポイントで実験を組み込む傾向があるということだ。
Stable products also tend to reuse their custom metrics between experiments.
安定した製品は、実験間でカスタムメトリクスを再利用する傾向もある。
In these cases, we have a rich set of experiment records and historical data that we can use to estimate the sigmas for an upcoming but similar experiment.
このような場合、**私たちは豊富な実験記録と過去のデータセットを持っており、それを使って今後行われる類似の実験のシグマを推定することができる**。(この話はnetflixのABテストの記事にもあったな...!)
Our tool simply asks the experimenter to provide an ID of a similar experiment from the past, and loads up observed statistics from that experiment for all metrics the experiment tracked.
我々のツールは、**実験者に過去の類似実験のIDを提供するよう求めるだけで、実験が追跡したすべてのメトリクスについて、その実験から観測された統計量をロードする**。(いいね...!)
The experimenter can now choose any of the previously tracked metrics, specify how much of a lift they expect to see with new changes, and get accurate estimates on the amount of traffic they need to allocate to reliably observe the expected change.
実験者は、これまで追跡していたメトリクスのいずれかを選択し、新たな変更によってどの程度の上昇が期待できるかを指定し(=**期待するeffect sizeは指定するのか**...!:thinking:)、期待される変化を確実に観察するために割り当てる必要があるトラフィック量について、正確な見積もりを得ることができる。

In cases where no prior experiments have been instrumented in the same location, or when brand new metrics are necessary, an experiment can be started in “dry-run” mode, just bucketing into control.
同じ場所での先行実験がない場合、あるいは全く新しい測定基準が必要な場合、実験は **"dry-run"モードで開始**され、単にcontrolにバケット分けされる。(=標準偏差を推定するために、controlのみの実験を行うのか...!:thinking:)
The regular experiment pipeline will collect all the statistics necessary for buckets to be estimated.
通常の実験パイプラインは、バケットを推定するために必要なすべての統計情報を収集する。

## Calling attention to underpowered metrics 力不足の指標に注意を喚起

Sometimes the bucket estimation tool isn’t enough.
バケツ見積もりツールでは不十分なこともある。
Experimenters may discover that their experiment targets an audience with different behavior from the audience of the experiment they provided for bucket size estimation.
実験者は、実験の対象となる観客が、バケツサイズの推定に提供した実験の観客とは異なる行動をすることを発見するかもしれない。
They may also want to assess impact on metrics that were not taken into account when using the bucket estimation tool.
また、バケット見積もりツールを使用する際に考慮されなかった指標への影響を評価したい場合もある。
In such cases, it’s possible that a given metric has insufficient power to make a strong claim regarding experiment results.
このような場合、実験結果について強く主張するには、あるmetricに十分な検出力がない可能性がある。
We call attention to metrics for which no significant effect is detected, and the minimal detectable effect is large.
私たちは、**有意な効果が検出されず、minimal detectable effectが大きいメトリクスに注意を喚起する**。

<!-- ここまで読んだ! -->

Consider a hypothetical experiment that attempts to improve the “Who To Follow” suggestion algorithm.
Who To Follow "サジェスト・アルゴリズムの改善を試みる仮想実験を考えてみよう。
Let’s imagine that historical experiments of this sort tend to produce a gain of 1% more follows.
この種の歴史的な実験では、1％増の利得が得られる傾向があると想像してみよう。(これが期待するeffect sizeかな??)
In the current experiment, we measure a 1.5% observed effect but it isn’t statistically significant.
今回の実験では、1.5％の効果が観測されたが、統計的には有意ではなかった。
We also calculate that based on the current sample size, MDE is 5%.
また、現在のサンプル数から計算すると、MDEは5％となる。 (0.8 MDEが5%)

Based on past experience, we know that if there is a true effect, it’s unlikely to be above 5%.
**過去の経験から、もし本当の効果があったとしても、5％を超えることはまずないことがわかっている**。
With the MDE we measured, it’s unlikely we would call a “real” 1.5% change statistically significant.
私たちが測定したMDEでは、"実質的な "1.5％の変化を統計的に有意と呼ぶことはまずないだろう。
In fact, the graph below demonstrates that only 30% of experiments of this size would detect a 1.5% change as statistically significant.
実際、下のグラフは、この規模の実験では、**1.5％の変化を統計的に有意であると検出できるのはわずか30％であること**を示している。
Considering the high MDE, instead of concluding that the proposed improvement has no effect, it’s better to increase the sample size and re-run the experiment with higher power.
MDEが高いこと(=minimum detectable effectのサイズが期待するeffect sizeよりも大きすぎていること...!:thinking:)を考慮すると、提案された改善が効果がないと結論付けるのではなく、サンプルサイズを増やして、より高い検出力で再実行する方が良い。
![]()

The Twitter experimentation framework, DDG, provides visual feedback to experimenters by coloring statistically significant positive changes green, and statistically significant negative changes red.
Twitterの実験フレームワークであるDDGは、統計的に有意な正の変化を緑色に、統計的に有意な負の変化を赤色に着色することで、**実験者に視覚的なフィードバックを提供**する。
We color likely-underpowered metrics a shade of yellow.
私たちは、**検出力不足の可能性のあるメトリクスを黄色に着色**する。
The intensity of the color is used to call experimenters’ attention to the actual p-values when we see statistical significance, and to potential power problems when we do not.
色の濃さは、統計的有意性が見られる場合は実際のp値に、そうでない場合は潜在的な検出力の問題に、実験者の注意を喚起するために使われる。
The intensity of red and green colors depends on the p-value (the more intense, the lower the p-value).
赤と緑の色の濃さはp値に依存する（濃ければ濃いほどp値は低い）。
The intensity of the yellow depends on the MDE (the more intense, the higher the MDE).
黄色の濃さはMDEに依存する（濃ければ濃いほどMDEが高い）。

Summary
概要

Providing the right amount of traffic is critical for successful experimentation.
実験を成功させるには、適切な量のトラフィックを提供することが重要である。
Too little traffic, and the experimenter does not have enough information to make a decision.
トラフィックが少なすぎると、実験者は判断を下すのに十分な情報を得られない。
Too much traffic, and you expose a lot of users to a treatment that might not fully ship.
トラフィックが多すぎると、多くのユーザーを十分に出荷されないかもしれない治療にさらすことになる。
Power analysis is a critical tool for determining how much traffic is required.
パワー分析は、どれだけのトラフィックが必要かを判断するための重要なツールである。
DDG uses data collected from past experiments to guide experimenters in selecting optimal bucket sizes.
DDGは、実験者が最適なバケツサイズを選択する際の指針として、過去の実験から収集したデータを使用している。
Furthermore, DDG provides visual feedback to help experimenters detect whether their experiments are underpowered, allowing them to rerun with larger sample sizes if needed.
さらにDDGは、実験者が実験が検出力不足であるかどうかを検出するのに役立つ視覚的なフィードバックを提供し、必要に応じてより大きなサンプルサイズで再実行できるようにする。
If your A/B testing tool does not have similar capabilities, there’s a decent chance you are missing “real” changes due to being underpowered — both good changes that improve your product, and bad effects that are affecting you negatively.
もしあなたのA/Bテストツールが同じような機能を持っていないなら、力不足のために「本当の」変化を見逃している可能性が高い。
Call your data scientist today, and ask them about power analysis.
今すぐデータサイエンティストに電話して、パワー分析について聞いてみよう。

Acknowledgements
謝辞

Robert Chang and Dmitriy Ryaboy co-authored this blog post.
ロバート・チャンとドミトリー・リャボイの共著。

[1] R.
[1] R.
Kohavi, R.
コハヴィ、R
Longbotham, D.
ロングボッサム、D.
Sommerfield, and R.
ソマーフィールド、R.
M.
M.
Henne.
ヘンだ。
Controlled experiments on the web: Survey and practical guide.
ウェブ上での対照実験： 調査と実践ガイド。
Data Mining and Knowledge Discovery, 18, no.1:140–181, July 2008.
データマイニングと知識発見, 18, no.1:140-181, July 2008.

$$
$$
