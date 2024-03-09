## link リンク

- https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions/ https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions/

# Choosing a Sequential Testing Framework — Comparisons and Discussions 逐次テストフレームワークの選択 - 比較と考察

## TL;DR ♪ TL;DR

Sequential tests are the bread and butter for any company conducting online experiments.
Sequential testは、オンライン実験を行う企業にとって糧となるものだ。
The literature on sequential testing has developed quickly over the last 10 years, and it’s not always easy to determine which test is most suitable for the setup of your company — many of these tests are “optimal” in some sense, and most leading A/B testing companies have their own favorite.
逐次テストに関する文献はこの10年で急速に発展し、**どのテストが自社のセットアップに最も適しているか**を判断するのは必ずしも容易ではない。これらのテストの多くはある意味で「最適」であり、A/Bテストのリーディングカンパニーのほとんどが自社のお気に入りを持っている。
Even though the sequential testing literature is blooming, there is surprisingly little advice available (we have only found this blog post) on how to choose between the different sequential tests.
シーケンシャル・テストの文献が花盛りであるにもかかわらず、さまざまなシーケンシャル・テストの中からどのように選べばいいのかについてのアドバイスは驚くほど少ない（私たちはこのブログ記事しか見つけていない）。
With this blog post we aim to share our reasoning around this choice.
このブログでは、この選択にまつわる私たちの理由を紹介する。

Spotify’s Experimentation Platform uses so-called group sequential tests (GSTs).
Spotifyの実験プラットフォームでは、いわゆる**group sequential tests (GSTs)**を使用している。
In this post, we highlight some of the pros and cons of our chosen method using simulation results.
この記事では、シミュレーション結果を用いて、私たちが選んだ方法の長所と短所を紹介する。
We conclude that two main parameters should affect your choice of sequential analysis tool:
結論として、**2つの主要なパラメータがsequential analysis toolの選択に影響を与えるべき**であることを示す。

- If your data infrastructure provides data in batch or streaming.
  データインフラがバッチまたはストリーミングでデータを提供する場合。(SaaSなどのオンラインソフトウェアサービスの場合は基本streamingな気がする...?? まあでも実験したい施策の内容にもよるか...!)

- If you can make reasonable estimates of the maximum sample size an experiment will reach.
  実験が到達する最大サンプル数を合理的に見積もることができる場合。
  (このサンプルサイズって、fixed horizon testにおけるunder-poweredな状況を避ける為の最小サンプルサイズの話かな?? いや、最大サンプルサイズだからまた違う話か...!:thinking_face:)

We show that when you can estimate the maximum sample size that an experiment will reach, GST is the approach that gives you the highest power, regardless of whether your data is streamed or comes in batches.
実験が到達する最大サンプルサイズを見積もることができる場合、データがストリーミングであるかバッチであるかに関係なく、GSTは最も高いパワーを提供するアプローチであることを示す。

## Solid experimentation practices ensure valid risk management 確かな実験の実践が有効なリスク管理を保証する

Experimentation lets us be bold in our ideas.
実験によって、私たちは大胆な発想ができるようになる。
We can iterate faster and try new things to identify what changes resonate with our users.
**私たちは、より速く反復(iterate)し、新しいことを試し、どのような変化がユーザに響くかを特定することができる**。
Spotify takes an evidence-driven approach to the product development cycle by having a scientific mindset in our experimentation practices.
Spotifyは製品開発サイクルにおいて、科学的なマインドセットで実験を行うことで、エビデンスに基づいたアプローチを取っています。
Ultimately, this means limiting the risk of making poor product decisions.
結局のところ、**これは誤ったproduct decisionsをするリスクを抑える**ことを意味する。

From a product decision perspective, the risks we face include shipping changes that don’t have a positive impact on the user experience, or missing out on shipping changes that do, in fact, lead to a better user experience.
product decisionsの観点から見ると、私たちが直面するリスクには、**ユーザ体験にポジティブな影響を与えない変更をリリース**すること、または**実際にはユーザ体験を向上させる変更をリリースすることを見逃すこと**が含まれる。(false positiveとfalse negativeの不確実性の話だ...!!:thinking_face:)
In data science jargon, these mistakes are often called “false positives” and “false negatives.” The frequency at which these mistakes occur in repeated experimentation is the false positive or false negative rate.
データサイエンスの専門用語では、これらのミスはしばしば "偽陽性 "や "偽陰性 "と呼ばれる。繰り返される実験において、これらのミスが発生する頻度が偽陽性率または偽陰性率である。
The intended false positive rate is often referred to as “alpha.” By properly designing the experiment, these rates can be controlled.
意図した(i.e. 許容した?)偽陽性率は、しばしば "alpha"と呼ばれる。適切に実験を設計することで、これらの割合を制御することができる。(これらのリスク(i.e. 不確実性)をなくす事はできないんだよね...!:thinking_face:)
In Spotify’s Experimentation Platform, we’ve gone to great lengths to ensure that our experimenters can have complete trust that these risks will be managed as the experimenter intended.
SpotifyのExperimentation Platformでは、**実験者が意図した通りにこれらのリスクが管理されることを完全に信頼できるようにするため**に、多大な努力を払ってきた。(experimentation platform大事だね～...!:thinking_face:)

## Peeking is a common source of unintended risk inflation 覗き見は、意図せざるリスク・インフレの一般的な原因である。

One of the most common sources of incorrect risk management in experimentation is often referred to as “peeking.” Most standard statistical tests — like z-tests or t-tests — are constructed in a way that limits the risks only if the tests are used after the data collection phase is over.
実験における誤ったリスク管理の最も一般的な原因の一つは、しばしば **"peeking(覗き見)"**と呼ばれる。**ほとんどの標準的な統計的検定（z検定やt検定など）は、データ収集段階が終わった後に使用される場合にのみリスクを制限するように構築されている**。
(z検定は、観測される標本平均の確率分布が、中心極限定理で正規分布に従うと仮定するようなアプローチ。t検定は、t分布に従うと仮定するようなアプローチだっけ:thinking_face:)
Peeking inflates the false positive rate because these nonsequential (standard) tests are applied repeatedly during the data collection phase.
これらのnon-sequntial (standard) テストがデータ収集段階中に繰り返し適用されるのだから、peekingは偽陽性率を増加させる。

For example, imagine that we’re running an experiment on 1,000 users split evenly into a control group and a treatment group.
例えば、1,000人のユーザーをcontrol groupとtreatment groupに均等に分けて実験を行っているとしよう。
We use a z-test to see if there’s a significant difference between the treatment group and the control group in terms of, for example, minutes played on Spotify.
例えば、**Spotifyでの再生時間について、control groupとtreatment groupの間に有意な差があるかどうか**を調べるためにz検定を使用する。
After collecting a new pair of observations from both groups, we apply our test.
両グループから新しいオブザベーション(->ex. 各variantの再生時間の標本平均...!)のペアを収集した後、我々のテストを適用する。
If we don’t find a significant difference, we proceed to collect another pair of observations and repeat the test.
**有意差が見つからなければ、もう1組のオブザベーションを収集し、テストを繰り返す**。(同じサンプルサイズを複数回集めるみたいなイメージ...!:thinking_face:)
With this design, the overall false positive rate is the probability of finding a false positive in any of the tests we conduct.
この設計では、**全体的な偽陽性率(overall false positive rate)は、実施したテストのどれかで偽陽性を見つける確率**である。
After we’ve conducted the first two tests, a false positive can be obtained in the first test or in the second test, given that the first test was negative.
最初の2つのテストを実施した後、最初のテストが否定的であるときに、最初のテストまたは2番目のテストで偽陽性が得られる。(??)
With a z-test constructed to yield a 5% false positive rate if used once, the true false positive rate that the experimenter faces is in fact closer to 10%, since the two tests give us two opportunities to find a significant effect.
1回使用すれば5％の偽陽性率が得られるように構成されたz検定では、2回の検定で有意な効果を見つける機会が2回あるため、実験者が直面する真の偽陽性率は実際には10％近くとなる。(=1 - (0.95)^2 = 0.0975 = 約9.8%か...!:thinking_face:)
The figure below shows how the false positive rate intended to be at 5% grows if we continue as in the previous example: collect a new pair of observations, test for an effect, and if not significant, continue and collect another pair of observations and test again.
下の図は、前の例と同じように続けると、5%になるはずの偽陽性率がどのように大きくなるかを示している： 新しいオブザベーションの組を収集し、効果を検定し、有意でなければ、続けて別のオブザベーションの組を収集し、再度検定する。
The true false positive rate grows quickly, and after repeated tests the experimenter encounters a true false positive rate that severely exceeds the intended 5% rate.
真の偽陽性率は急速に高まり、テストを繰り返すうちに、実験者は意図した5％を大きく超える真の偽陽性率に遭遇する。

![]()
Figure 1: The false positive rate increases when peeking. The solid line describes the true false positive rate encountered by the experimenter when peeking, and the dashed line indicates the desired false positive rate of 1%.
図1：peekingをすると偽陽性率が増加する。実線はpeekingをすると実験者が遭遇する真の偽陽性率を示し、破線は1％の望んだ偽陽性率を示している。(有意水準1%の場合の話か...!)

<!-- ここまで読んだ! -->

## Sequential tests solve the peeking problem シーケンシャルテストはピーキング問題を解決する

While uncontrolled peeking must be avoided, it’s also important to monitor regressions while collecting data for experiments.
**無秩序なpeekingは避けるべきだが、実験のデータを収集する間にregressions(=退行!)を監視することも重要**である。
A main objective of experimentation is to know early on if end users are negatively affected by the experience being tested.
**実験の主な目的は、エンドユーザがテスト中の体験によって悪影響を受けるかどうかを早い段階で知ることである**。(=やっぱりsequential testingの目的はregressionの発見なのか...!:thinking_face:)
To do this, we need a way to control the risk of raising false alarms, as well as the risk of failing to raise the alarm when something is, in fact, affecting the end-user experience negatively.
そのためには、**誤報を出すリスク**、**実際にエンドユーザの体験に悪影響を与えているものを見逃すリスク**を制御する方法が必要である。(sequential testingの2つの不確実性(リスク)...!!:thinking_face:)

To solve the peeking problem, we can leverage a wide class of statistical tests known as sequential tests.
peeking問題を解決するためには、sequential testsとして知られる広範なクラスの統計的テストを活用することができる。
These tests account for the sequential and recurrent nature of testing in different ways, depending on their specific implementations.
これらのテストは、その具体的な実装によって、異なる方法で、テストのsequentialでrecurrentな性質を考慮する。
They all let us repeatedly test the same hypothesis while data is being collected, without inflating the false positive rate.
**いずれも、偽陽性率を高めることなく、データ収集中に同じ仮説を繰り返し検証することができる**。
Different tests come with different requirements — some require us to estimate the total number of observations that the test will include in the end, and some don’t.
**異なるテストには異なる要件があり**、最終的にテストに含まれるオブザベーションの総数を推定する必要があるものもあれば、そうでないものもあります。
Some are better suited when data arrives in batches (for example, once per day), and some when data is available in real time.
データがバッチ(例えば1日1回)で届く場合に適しているものもあれば、データがリアルタイムで入手できる場合に適しているものもある。
In the next section, we provide a short, nonexhaustive overview of the current sequential testing landscape where we focus on tests that are well-known.
次のセクションでは、よく知られているテストに焦点を当て、現在のシーケンシャル・テストの状況について、網羅的ではない短い概観を提供する。
Furthermore, we concentrate on the power of these tests, specifically, the rate of rejecting the null hypothesis that there is no difference in means between treatment and control for some metric of interest, given the alternative hypothesis of a nonzero difference.
さらに、これらのテストの検出力に焦点を当てる。特に、興味のあるメトリックについて、対立仮説がゼロでない差(=これくらいcontrolよりも下がったら早期終了する、という仮定した効果量?:thinking:)であるという場合に、treatmentとcontrolの平均に差がないという帰無仮説を棄却する割合である。

The methods we study are:
私たちが研究している方法とは

- The group sequential test (GST).
  グループ・シーケンシャル・テスト（GST）。
  At Spotify, we use the GST with alpha spending as proposed by Lan and DeMets (1983).
  Spotifyでは、LanとDeMets(1983)が提唱したアルファ支出を伴うGSTを使用している。

- Two versions of always valid inference (AVI):
  **always valid inference (AVI)**の2つのバージョン：
  - The **mixture sequential probability ratio test (mSPRT)**.
    Popularized, used, and extended by Optimizely, Uber, Netflix, and Amplitude, for example.
    例えば、Optimizely、Uber、Netflix、Amplitudeなどが普及、使用、拡張している。
  - The **generalization of always valid inference (GAVI)**, as proposed by Howard et al.(2021).
    Howardら(2021)が提唱した**GAVIの一般化**。
    Used by Eppo, for example.
    例えば、Eppoが使用している。(Eppo=オンライン実験プラットフォームを提供する会社?)
- The **corrected-alpha approach (CAA)**.
  補正アルファ・アプローチ（CAA）。
  Used and proposed by Statsig.
  Statsigが使用・提案。
- A naive approach using Bonferroni corrections as a baseline (benchmark).
  ベースライン（ベンチマーク）としてボンフェローニ補正を用いた素朴なアプローチ。

Below, we briefly go through the tests one by one.
以下、ひとつひとつのテストを簡単に紹介する。
The purpose is not to present the technical or mathematical details but rather to highlight the properties and limitations of each framework.
その目的は、技術的あるいは数学的な詳細を紹介することではなく、むしろ**各フレームワークの特性と限界を強調すること**にある。

<!-- ここまで読んだ! -->

### Group sequential tests グループ・シーケンシャル・テスト

Group sequential tests can be viewed as consecutive applications of traditional tests like the z-test.
**group sequential testsは、z検定などの伝統的なテストの連続的な適用**として見ることができる。
The GST exploits the known correlation structure between intermittent tests to optimally account for the fact that we are testing multiple times.
GSTは、断続的なテスト間の既知の相関構造を利用して、**複数回テストを行っていることを最適に考慮**する。
For detailed introduction see e.g.Kim and Tsiatis (2020) and Jennison and Turnbull (1999).
詳しい紹介は、Kim and Tsiatis (2020)やJennison and Turnbull (1999)などを参照のこと。

#### Pros: 長所:

- Using the alpha-spending approach, alpha can be spent arbitrarily over the times you decide to peek, and you only spend alpha when you peek — if you skip one peek, you can save that unused alpha for later.
  alpha-speadingアプローチを使用すると、peekするタイミングで任意にalphaを使うことができ、peekするときだけalphaを使う。1回のpeekをスキップすると、その未使用のalphaを後で使うことができる。
  Moreover, you don’t have to decide in advance how many tests you run or at what time during the data collection you run them.
  しかも、テストの回数やデータ収集のタイミングを事前に決めておく必要はない。
  If you do not peek at all during the data collection, the test once the data collection phase is over is exactly the traditional z-test.
  データ収集中にまったく覗き見をしなければ、データ収集段階が終わった後のテストは、まさに伝統的なz検定となる。

- Easy to explain due to the relation with z-tests.
  z検定との関係で説明しやすい。

#### Cons: 短所:

- You need to know or be able to estimate the maximum sample size in advance.
  **事前に最大サンプル数を知っておく**か、推定できるようにしておく必要がある。
  If you observe fewer users than expected, the test will be conservative and the true false positive rate will be lower than intended.
  観察されるユーザが予想より少なければ、テストは保守的になり、真の偽陽性率は意図したより低くなります。
  If you keep observing new users after you have reached the expected total amount, the test will have an inflated false positive rate.
  予想総数に達した後も新規ユーザを観察し続けると、テストは偽陽性率が高くなる。

- You need to select an alpha spending function.
  alpha spending functionを選択する必要がある。(ハイパーパラメータ的な?? 連続的に検定する事を考慮し、alphaをどのように補正するか、みたいな関数...??)
  If you always reach the planned sample size, this choice is not critical, but if you undersample and observe too few users, the choice of spending function can affect the power properties substantially.
  常に計画されたサンプルサイズに達する場合、この選択は重要ではないが、サンプル数が少なすぎると、speading functionの選択がパワーの特性に大きく影響する。

- The critical values used in the test need to be obtained by solving integrals numerically.
  試験で使用するcritical valuesは、数値的に積分を解いて得る必要がある。(=null distributionの形が複雑になって、critical valueが解析的に得られないってこと?:thinking_face:)
  This numerical problem becomes more challenging with many intermittent analyses, and it is therefore not feasible to use GST in a streaming fashion, i.e., run more than a few hundred intermittent analyses for one experiment.
  この数値的な問題は、多くの断続的な分析があるとより難しくなり、したがって、GSTをstreaming fashion(方式)で使用すること、つまり、**1つの実験に数百回以上の断続的な分析を実行することは不可能**である。

### Always valid inference (AVI) 法

Always valid inference tests allow for continuous testing during data collection without deciding in advance on a stopping rule or the number of intermittent analyses.
always valid inference testsは、事前に停止ルールや断続的な分析の回数を決めることなく、データ収集中に連続的なテストを行うことを可能にする。
We present both mSPRT and GAVI, but mSPRT is essentially a special case of GAVI, and the pros and cons are the same.
mSPRTとGAVIの両方を紹介しますが、mSPRTは基本的にGAVIの特殊なケースであり、長所と短所は同じです。
For details see e.g.Howard et al.(2021) or Lindon et al.(2022).
詳細はHowardら(2021)やLindonら(2022)を参照のこと。

#### Pros:

- Easy to implement.
  実行するのは簡単だ。
- Allows unlimited sampling and no expected sample size is required in advance.
  無制限のサンプリングが可能で、事前に予想されるサンプルサイズは必要ない。
- Allows arbitrary stopping rules.
  任意の停止ルールを許可する。
- Supports streaming and batch data.
  streamingデータもbatchデータもサポートする。

#### Cons:

- Requires the experimenter to choose parameters of the mixing distribution, i.e., the distribution that describes the effect under the alternative hypothesis.
  mixing distribution(混合分布)、すなわち対立仮説のもとでの効果を記述する分布のパラメータを選択することを実験者に要求する。(分布の分散とかを事前に指定する必要があるってこと...??:thinking_face:)
  This choice affects the statistical properties of the test and is nontrivial.
  この選択は検定の統計的特性に影響し、自明ではない。
  If the approximate expected sample size is known, it can be used to select the parameter, but then the pro of not having to know the sample size is lost.
  おおよその予想されるサンプルサイズがわかっている場合、そのパラメータを選択するために使用できるが、その場合、サンプルサイズを知る必要がないという利点が失われる。
- Harder to understand for folks trained in traditional hypothesis testing.
  伝統的な仮説検証の訓練を受けた人々には理解しにくい。
  It will probably take a while before intro courses in statistics cover these tests.
  統計学の入門コースでこれらのテストが扱われるようになるには、しばらく時間がかかるだろう。
- Has by construction less power when analyzing data in batch compared to streaming.
  構造上、streamingに比べてbatchでデータを分析すると、パワーが低くなる。

<!-- ここまで読んだ! -->

### Bonferroni corrections ボンフェローニ補正

If we have an upper bound for how many intermittent analyses we want to make, we can solve the peeking problem by selecting a conservative approach.
断続的な分析の回数に上限があれば、**conservativeな(保守的な)アプローチ**を選択することで、peeking問題を解決することができる。(保守的な = 有意水準(i.e. 許容する偽陽性率)を小さくする事...??:thinkng:)
We can bound the false positive rate by adjusting for multiple comparisons using Bonferroni corrections, where we use a standard z-test but with alpha divided by the number of intermittent analyses.
Bonferroni補正を用いて複数の比較を調整することで、偽陽性率を制限することができる。ここでは、標準的なz検定を使用するが、**alphaを断続的な分析の回数で割る**。(多重検定を考慮して、有意水準をより小さくするって事か!)
Since the test statistic is highly correlated over repeated testing, the Bonferroni approach is conservative by construction.
検定統計量は繰り返しテストで高度に相関しているため、Bonferroniアプローチは構造上保守的である。

#### Pros:

- Easy to implement and explain.
  実施も説明も簡単だ。

#### Cons:

- You have to decide the maximum number of intermittent analyses in advance.
  断続的な分析の最大回数をあらかじめ決めておく必要がある。
- With many intermittent analyses, the test will become highly conservative with low power as a consequence.
  断続的な分析が多い場合、テストは非常に保守的になり(i.e. acceptable false positive rateが低くなり...!)、結果として検出力が低くなる。

### Corrected-alpha approach 修正アルファ・アプローチ

Statsig proposed a simple adjustment that reduces the false positive inflation rate from peeking.
Statsigは、peekingによる偽陽性のインフレ率を減らすための簡単な調整を提案した。
The approach does not solve the peeking problem in the sense that the false positive rate under peeking is bounded below the target level (alpha) but substantially limits the inflation itself.
このアプローチは、peeking問題を解決するわけではない。つまり、peekingの下での偽陽性率が目標レベル（alpha）よりも低く抑えられるが、インフレ自体は大幅に制限される。

#### Pros:

- Easy to use.
  使いやすい。

#### Cons:

- Does not bound the false positive rate and, therefore, does not solve the peeking problem.
  偽陽性率を制限しないため、peeking問題を解決しない。(??)
- The actual false positive rate depends on the sample size and number of intermittent analyses — which might be hard for experimenters to understand.
  実際の偽陽性率はサンプルサイズと断続的な分析の回数に依存するため、実験者にとって理解しにくいかもしれない。(??)

### How data is delivered affects the choice of test データがどのように配信されるかは、テストの選択に影響する。

Most companies running online experiments have data infrastructure that supports either batch or streaming data (or both).
オンライン実験を実施しているほとんどの企業は、batchデータまたはstreamingデータ（またはその両方）をサポートするデータインフラストラクチャを持っている。(うんうん...!)
In the context of online experimentation, batch data implies that analysis can, at most, be done each time a new batch of data is delivered.
オンライン実験の文脈では、batchデータは、新しいデータのバッチが配信されるたびに分析が行われることを意味する。
At Spotify, most data jobs are run daily, implying one analysis per day during an experiment.
Spotifyでは、ほとんどのデータジョブは毎日実行され、実験中は1日1回の分析を意味する。
As the name indicates, the group sequential test is built for use with batches (groups) of data.
その名が示すように、**グループ・シーケンシャル・テストは、データのbatch (group)と一緒に使用するために構築されている**。
If the number of intermittent analyses adds up to more than a few hundred, the test will no longer be a feasible option due to increasingly complex numerical integrations.
断続的な解析の回数が数百回以上になると、数値積分がますます複雑になるため、この試験はもはや実行可能な選択肢ではなくなる。
Most experiments at Spotify run for a few weeks at most, and our data arrives in batches, which means that the GST is a good fit for our experimentation environment.
**Spotifyのほとんどの実験は、最大でも数週間しか実行されず**、データはバッチで届くため、GSTは我々の実験環境に適している。

Streaming data, on the other hand, allows us to analyze results after each new observation.
一方、streamingデータを使用すると、新しい観測ごとに結果を分析することができる。
In other words, there can be as many analyses as there are observations in the sample.
言い換えると、標本中のオブザベーションの数だけ分析があり得ます。
The AVI family of tests can be computed as soon as a new observation comes in.
AVIファミリーのテストは、新しい観測が入るとすぐに計算することができる。
In fact, to utilize their full potential to find significant results, AVI tests should ideally be used with streaming data.
実際、重要な結果を導き出すためにAVIテストの可能性を最大限に活用するには、ストリーミングデータを使用するのが理想的である。
While streaming data is favorable, they can also handle batch data by simply skipping the intermittent analyses.
ストリーミングデータが好ましい一方で、断続的な分析を単にスキップすることでバッチデータも処理できる。(streamingデータをbatchデータとして扱えるよねって話か...!)
This will, however, inevitably make the AVI tests conservative to some extent, as most of the chances for false positive results are never considered.
しかし、これでは偽陽性の可能性がほとんど考慮されないため、AVI検査がある程度保守的になるのは避けられない。
We come back to this point in the simulation study below.
この点については、後述のシミュレーション・スタディで触れることにする。

<!-- ここまで読んだ! -->

## Evaluating the efficacy of sequential tests by their false positive rates and statistical power

There are two important properties by which we assess the usefulness and effectiveness of the sequential tests:
sequential testsの有用性と効果を評価するための**2つの重要な特性**がある。

- A bounded false positive rate: The first and most important property for a sequential test is that it solves the peeking problem.
  偽陽性率が有限であること： sequential testの最初で最も重要な特性は、peeking問題を解決することである。
  That is, the false positive rate should not be above the intended rate (alpha) even in the presence of peeking.
  **つまりpeekingがあったとしても、偽陽性率は意図した割合(alpha)を超えてはならない**。
  (ここでalphaは、fixed-horizon testを前提としたテスト全体の偽陽性率のことっぽい...!:thinking:)
- High power/sensitivity: The second property is the power or sensitivity for a test, i.e., how often we reject the null hypothesis when it is not true.
  高い検出力/感度： 2つ目の特性は、検定の検出力または感度、すなわち帰無仮説が真でないときにそれを棄却する頻度です。
  As often as possible, we want our test to identify effects when they are there and reject the null hypothesis when it is not true.
  可能な限り多くの場合、テストが効果を識別し、帰無仮説が真でないときにそれを棄却することを望む。(施策に有害な効果がある場合に、それを正しく見つけ出すことができる必要がある...!:thinking:)

We acknowledge that these tests could be evaluated from many additional angles, for example what type of test statistics they can be used together with and what their small-sample properties are.
我々は、これらの検定が、例えば、どのような種類の検定統計量と併用できるのか、また、その小標本特性はどのようなものなのかなど、多くの追加的な角度から評価できることを認める。
In our experience, power and false positive rate are the most important aspects, and thus a good starting point for comparing.
私たちの経験では、検出力と偽陽性率が最も重要な点であり、比較の出発点として適している。

Of the five tests mentioned above, all but the corrected-alpha approach (CAA) fulfill the first criterion of a bounded false positive rate.
**上述した5つのテストのうち、corrected-alpha approach (CAA)を除くすべてのテストは、有限の偽陽性率の基準(=1つ目の基準)を満たしている**。
The CAA test is constructed in such a way that the overall false positive rate is strictly larger than alpha if any peeking is performed during data collection.
CAAテストは、データ収集中にpeekingが行われた場合、全体的な偽陽性率が厳密にalphaよりも大きくなるように構築されている。
The level of inflation depends on how often you peek and how large the total sample size is, as our results below reveal.
インフレの程度は、以下の結果で明らかなように、どれくらいの頻度でpeekingするか、そして総サンプルサイズがどれくらいかに依存する。
Since it doesn’t bound the false positive rate under peeking, we don’t view CAA as a proper sequential test and will leave it out of the power comparison.
**peekingの下で偽陽性率を制限しないため、CAAを適切なsequential testとは見なしておらず**、パワーの比較から除外する。

All other tests by construction bound the false positive rate to alpha or lower if used as intended but differ in power/sensitivity.
**他のすべてのtestは、意図したとおりに使用された場合、偽陽性率はalpha以下に制限される**が、検出力/感度は異なる。
However, these tests are also optimized to have sensitivity for different settings that we discuss further in the next section.
しかし、これらのテストは、次のセクションでさらに議論するさまざまな設定に対して感度を持つように最適化されている。

<!-- ここまで読んだ! -->

## Monte Carlo simulation study モンテカルロ・シミュレーション研究

To build intuition for the important trade-offs when selecting between the sequential tests discussed above, we perform a small Monte Carlo simulation study.
上述した逐次テストを選択する際の重要なトレードオフを直感的に理解するために、小規模なモンテカルロ・シミュレーションを行った。

To keep this post short, some of the details of the setup are left out.
この記事を短くするため、セットアップの詳細は一部割愛する。
Please refer to the replication code for details.
詳しくはレプリケーションコードをご覧ください。
All data in the simulation is generated from a normal distribution with mean 1 (+ treatment effect under treatment) and variance 1.
シミュレーションのすべてのデータは、平均1（＋治療下の治療効果）、分散1の正規分布から生成される。
The sample size is balanced between treatment and control with 500 observations in each group.
サンプル・サイズは、各グループで500のオブザベーションがあり、トリートメントとコントロールの間でバランスが取れている。
We run 100,000 replications for each combination of parameters.
各パラメータの組み合わせについて100,000回の反復を行った。
We use one-sided tests with the intended false positive rate (alpha) set to 5%.
偽陽性率（アルファ）を5%に設定した片側検定を使用する。
All statistical assumptions of all tests are fulfilled by construction without the need for large samples.
すべての検定の統計的仮定は、大規模なサンプルを必要とすることなく、構成によって満たされる。
For all simulations we vary the number of intermittent analyses.
すべてのシミュレーションで、断続的な分析の回数を変えた。
We conduct 14, 28, 42, or 56 evenly spaced analyses, or analyze results in a streaming fashion.
14回、28回、42回、56回と等間隔に分析を行うか、ストリーミング方式で結果を分析する。
The latter corresponds to 500 intermittent analyses in this case.
後者はこの場合、500回の断続的な分析に相当する。
Note that stream is not calculated for the GSTs since this is not plausible for the sample sizes typically handled in online experimentation.
オンライン実験で一般的に扱われるサンプルサイズでは妥当ではないため、ストリームはGSTでは計算されないことに注意。

We obtain bounds for the GST using the ldbounds R package, where we vary the expected sample size parameter [n].
ldbounds Rパッケージを用いてGSTの境界を求め、期待されるサンプルサイズのパラメータ[n]を変化させる。
We implement the GAVI test according to Eppo’s documentation, where we vary the numerator of the tuning parameter [rho].
GAVIテストをEppoのドキュメントに従って実施し、チューニングパラメータ[rho]の分子を変化させる。
The version of the mSPRT that we use follows the generalization presented by Lindon et al.(2022).
我々が使用するMSPRTのバージョンは、Lindonら(2022)が提示した一般化に従っている。
We consider only the one-dimensional case and vary the tuning parameter [phi].
一次元の場合のみを考え、チューニングパラメーター[phi]を変化させる。
For CAA, we follow the procedure outlined in Statsig’s documentation.
CAAについては、Statsigの文書に概説されている手順に従う。

We first focus on the false positive rate and then compare power under various settings for the tests that properly bound the false positive rate.
まず偽陽性率に注目し、次に偽陽性率を適切に制限するテストについて、様々な設定下での検出力を比較する。

### False positive rate 偽陽性率

For the empirical false positive rate simulation, we consider the following tests and variants of tests:
経験的な誤検出率のシミュレーションのために、以下のテストとテストのバリエーションを検討する：

GST
GST

We apply the test with (1) a correctly assumed sample size, (2) a 50% underestimated sample size (i.e., we wrongly assumed a too low maximum sample size 500, but the real observed final sample size was 750), and (3) a 50% overestimated sample size (i.e., we assumed a too high sample size 500, but the real sample size was 250).
(1)正しく仮定されたサンプルサイズ、(2)50％過小評価されたサンプルサイズ（すなわち、最大サンプルサイズが500と低すぎることを誤って仮定したが、実際に観察された最終サンプルサイズは750であった）、および(3)50％過大評価されたサンプルサイズ（すなわち、サンプルサイズが500と高すぎることを仮定したが、実際のサンプルサイズは250であった）を用いてテストを適用する。
When we oversample and obtain more observations than expected, we apply the correction to the bounds proposed in Wassmer and Brannath (2016), pages 78–79.
我々がオーバーサンプリングして予想より多くのオブザベーションを得たときは，Wassmer and Brannath (2016)の78-79ページで提案されている境界への補正を適用する．

We use two versions of the so-called power family alpha spending function that are either quadratic or cubic in the information ratio.
我々は、いわゆるパワー・ファミリー・アルファ支出関数の2つのバージョンを使用し、情報比率の2次関数または3次関数を使用する。
See Lan and DeMets (1983).
Lan and DeMets (1983)を参照。

GAVI
GAVI

We set the numerator in the tuning parameter [rho] to the correct expected sample size, and to 50% oversampled or undersampled.
チューニングパラメーター[rho]の分子を、正しい予想サンプルサイズに設定し、50％のオーバーサンプルまたはアンダーサンプルに設定した。

mSPRT
エムエスピーアールティー

We set the tuning parameter [phi] to 1/[tau]2 where [tau] is equal to one of the true effect sizes used in the simulation study (0.1, 0.2, or 0.3).
チューニングパラメーター[phi]を1/[tau]2に設定し、[tau]はシミュレーション研究で使用された真の効果量（0.1、0.2、0.3）のいずれかに等しい。

CAA – no settings.
CAA - 設定なし。

Naive
ナイーブ

The alpha used in the standard z-test is set to 0.05 divided by the number of intermittent analyses.
標準的なz検定で使用されるアルファは、0.05÷断続的分析の回数に設定される。

#### Results 結果

Table 1 displays the empirical false positive results across the 100,000 Monte Carlo replications.
表1は、100,000回のモンテカルロ法による経験的偽陽性結果を示している。
As expected, all tests but the oversampled GST and the CAA tests successfully bound the false positive rate.
予想通り、オーバーサンプリングGSTとCAAテスト以外のすべてのテストは、偽陽性率を抑えることに成功した。
For the GST this is expected since all the false positive rate is fully consumed once the sample reaches the planned sample size, and any test beyond that point will inflate the false positive rate.
GSTの場合、サンプルが計画されたサンプル・サイズに達すると、すべての偽陽性率が完全に消費され、それ以上の検査は偽陽性率を増加させるので、これは予想されることである。
Similarly, the CAA test is using all intended false positive rate on the last analysis point, and all tests run before the full sample is obtained inflate the false positive rate.
同様に、CAAテストは最後の分析ポイントで意図したすべての偽陽性率を使用しており、全サンプルが得られる前に実行されたすべてのテストは偽陽性率を増加させる。

It is worth noting that the always valid tests (GAVI and mSPRT) are conservative when the test is not performed after each new observation.
常に有効な検定（GAVIとMSPRT）は、新たな観察が行われるたびに検定が行われない場合、保守的であることは注目に値する。
Interestingly, the naive approach has similar conservativeness as some of the always valid approaches when 14 intermittent analyses are performed.
興味深いことに、ナイーブアプローチは、14の断続的な分析を行った場合、常に有効ないくつかのアプローチと同様の保守性を持つ。

### Power パワー

For the power comparison, we drop the methods that do not bound the false positive rate to make power comparisons valid.
検出力の比較では、検出力の比較を有効にするために、偽陽性率を制限しない方法は除外する。
For the methods that successfully bound the false positive rate and thus solve the peeking problem, we now turn our attention to the power.
偽陽性率を抑制し、ピーキング問題を解決することに成功した方法について、次にパワーに注目する。
That is, each test’s ability to detect an effect when it exists.
つまり、効果が存在する場合にそれを検出する各検査の能力である。
To do this, we now also add a true effect equal to 0.0, 0.1, 0.2, 0.3, or 0.4 standard deviations of the outcome.
そのために、結果の0.0、0.1、0.2、0.3、0.4標準偏差に等しい真の効果も加える。
This implies that for the zero effect, the observed power corresponds to the empirical false positive rate.
これは、効果がゼロの場合、観測された検出力が経験的偽陽性率に相当することを意味する。

### Results 結果

Table 2 displays the empirical power results for a given treatment effect of 0.2 standard deviations.
表2は、治療効果が0.2標準偏差である場合の経験的検出力の結果を示している。
This effect size was chosen as no method has power 1 or 0 for this effect size, which makes the difference between the methods clearer.
この効果量を選んだのは、どの方法もこの効果量に対して検出力1または0を示さないためであり、これによって方法間の差が明確になる。

The results show that the GST is in most cases superior to all other methods in terms of power, even when the expected sample size is overestimated.
その結果、**予想される標本サイズが過大に見積もられている場合でも、ほとんどの場合、検出力の点でGSTが他のすべての方法よりも優れていることが示された**。
The exception is when the GST uses an alpha spending function that spends very little alpha in combination with an overestimated sample size.
例外は、GSTが、過大評価されたサンプルサイズと組み合わせて、アルファをほとんど使わないアルファ支出関数を使用している場合である。
This is natural since the phase of the data collection during which most of the alpha is planned to be spent never comes.
アルファの大半が費やされるはずのデータ収集の段階が来ないのだから、これは当然のことである。
In this situation, GST has power comparable to the always valid tests, but systematically lower power than the best performing always valid test variants.
このような状況では、GSTは常に有効な検査と同等の検出力を持つが、常に有効な検査の中で最も成績のよいバリエーションよりも系統的に検出力が低い。

The number of intermittent analyses only has a minor impact on the power of the GST.
**断続的な分析回数は、GSTのパワーにわずかな影響しか与えない。**
As expected, the always valid tests GAVI and mSPRT have lower power, the fewer intermittent analyses we perform.
予想通り、常に有効なテストであるGAVIとMSPRTは、断続的な分析が少ないほど検出力が低くなる。
Even though the differences are not very large, it is worth noting that the naive approach (Bonferroni) with 14 intermittent analyses has higher power than all considered variants of the always valid tests with that few analyses.
その差はそれほど大きくないとはいえ、14回の断続的分析による素朴なアプローチ（Bonferroni）の方が、その数回の分析による常に有効な検定のすべての検討された変形よりも検出力が高いことは注目に値する。
The mSPRT power is relatively stable across different choices of its tuning parameter, and we see the same for GAVI.
MSPRTのパワーは、チューニング・パラメーターの選択によって比較的安定している。

Figure 2 presents the full power curves for a subset of the settings.
図2は、セッティングの一部についてのフルパワー曲線である。
Most variations perform equally well, with the major exceptions for all effect sizes considered being GST, and Bonferroni correction with stream data.
ほとんどのバリエーションは同じようにうまくいき、GSTとストリームデータでのボンフェローニ補正は、検討したすべての効果量の主な例外であった。
Bonferroni correction with 14 or 56 intermittent analyses performs surprisingly well but expectedly overcompensates when conducting 500 analyses.
14回または56回の断続的な分析でのボンフェローニ補正は驚くほどうまくいくが、500回の分析では予想通り過剰補正となる。

## What can we learn from the results? 我々はこの結果から何を学ぶことができるのか？

In summary, we find that the group sequential test is systematically better or comparable to always valid approaches.
まとめると、**group sequential testは、常に有効なアプローチと比べて、系統的に優れているか同等である**ことがわかった。
Since we analyze data arriving in batches at Spotify, the group sequential test’s inability to handle streaming data is no practical limitation; in fact, it means that we’re able to evaluate the data more efficiently since we don’t need to analyze results continuously as data arrives.
Spotifyでは、到着したデータを一括して分析しているため、グループ逐次テストがストリーミングデータを扱えないことは、実用上の制限ではない。
A surprising result is that when the number of analyses carried out is kept low, applying Bonferroni corrections to standard z-tests is as effective as relying on always valid approaches.
驚くべき結果は、実施した分析数が少ない場合、標準的なz検定にボンフェローニ補正を適用することは、常に有効なアプローチに頼るのと同じくらい効果的であるということである。
This result suggests that depending on the situation, always valid tests may be too general and conservative.
この結果は、状況によっては、常に有効なテストが一般的で保守的すぎる可能性を示唆している。

While our simulation study is simple and transparent, the results may not generalize to other situations.
我々のシミュレーション研究はシンプルで透明性が高いが、結果は他の状況に一般化されるとは限らない。
Our setup mimics a real-life situation in which there is an upper limit on the number of observations or on the runtime of the experiment.
我々のセットアップは、オブザベーションの数や実験の実行時間に上限があるような現実の状況を模倣している。
In some cases, the experimenter may want to leave the experiment on indefinitely, so the always valid tests would be more attractive.
場合によっては、実験者は無期限に実験を続けたいかもしれないので、常に有効なテストの方が魅力的だろう。
In the simulation, we have also assumed that the variance is known.
シミュレーションでは、分散が既知であることも仮定した。
In practice, it is not, and estimating the variance could cause further changes to the results.
実際にはそうではなく、分散を推定することで結果がさらに変わる可能性がある。
Similarly, we generated data from a normal distribution in the simulation study, and each of the tests could be differently affected if the data instead were, for example, heavily skewed.
同様に、シミュレーション研究では正規分布からデータを作成したが、例えばデータが大きく歪んでいた場合、それぞれのテストは異なる影響を受ける可能性がある。

The always valid approaches require tuning parameters to be set just as the group sequential test requires an expected sample size.
常に有効なアプローチは、群逐次検定が期待されるサンプルサイズを必要とするように、チューニングパラメータを設定する必要がある。
For GAVI, we’ve used parameterizations expressing these in terms of expected sample sizes and effect sizes.
GAVIでは、予想されるサンプルサイズとエフェクトサイズという観点から、これらを表現するパラメータ化を用いている。
A major difference between the expected sample size for the group sequential test and the tuning parameters for the always valid approaches is that the latter are guaranteed to never exceed the desired false positive rate no matter what value is selected.
群逐次検定の期待されるサンプルサイズと、常に有効なアプローチのチューニングパラメータの大きな違いは、後者がどのような値を選択しても、望ましい偽陽性率を超えないことが保証されていることである。
The only potential price one has to pay is in terms of power: a suboptimal value could lead to low power.
支払うべき唯一の代償は、パワーという点である： 最適でない値は低電力につながる可能性がある。
For the group sequential test, a too low expected sample size in relation to what is actually observed means that the test has an inflated false positive rate.
群逐次検定では、実際に観察されるものに対して期待される標本サイズが低すぎるということは、その検定が偽陽性率を高くしていることを意味する。
While we don’t explore this topic further in this blog post, it’s worth emphasizing that a correctly bounded false positive rate is guaranteed with always valid inference.
このブログ記事でこのトピックをこれ以上掘り下げることはしないが、常に有効な推論を行うことで、正しく境界が設定された偽陽性率が保証されることは強調しておく価値がある。
Sometimes this guarantee might be more valuable than the reduction in power that follows.
時にはこの保証は、その後の戦力ダウンよりも価値があるかもしれない。
For example, if estimation of the expected sample size is difficult and often wrong, an always valid test is preferable to the group sequential test.
たとえば、期待される標本サイズの推定が困難で、しばしば間違っている場合は、群順次検定よりも常時有効な検定のほうが望ましい。

In the next section, we look more closely at the behavior of the always valid test when the expected sample size isn’t known at all.
次のセクションでは、期待される標本サイズがまったくわかっていないときの常に有効な検定の振る舞いをより詳しく見ます。

## When you can’t estimate the expected sample size 期待されるサンプルサイズを推定できない場合

The simulations indicate that GSTs are often preferable from a power perspective if the expected sample size is known or can be estimated.
このシミュレーションは、予想されるサンプルサイズが既知か推定できる場合、検出力の観点からGSTが望ましいことが多いことを示している。
But what about when the expected sample size is not known and can’t be estimated? This could be the case, for example, when there is no historical data for the type of experiments that are being run.
しかし、予想されるサンプルサイズが不明で推定できない場合はどうだろうか。例えば、実行しようとしている種類の実験について過去のデータがない場合などである。
In this section, we look more closely at the properties of AVI in this case.
このセクションでは、この場合のAVIの特性をより詳しく見ていく。

We could see from the simulations that the number of intermittent analyses is much less important than the ability to estimate the expected sample size (GST), or select the mixing parameter (mSPRT, GAVI).
シミュレーションから、断続的な分析の回数は、期待されるサンプルサイズの推定能力（GST）や混合パラメータの選択能力（MSPRT、GAVI）よりもはるかに重要でないことがわかった。
The two always valid test variants considered here are comparable in power, so we focus on the GAVI.
ここで検討した2つの常時有効なテスト変種は、検出力において同等であるため、GAVIに焦点を当てる。
The expected sample size is parameterized, which makes reasoning easier.
期待されるサンプル・サイズがパラメータ化されているので、推論が容易になる。

When using GAVI, it’s safer to underestimate the sample size for the mixing parameter than to overestimate (Howard et al.2021), to optimize power.
GAVIを使用する場合、検出力を最適化するために、混合パラメータのサンプルサイズを過大評価するよりも過小評価する方が安全である（Howard et al.2021）。
At the same time, if you have accurate information about the sample size it’s better to use GST.
同時に、サンプルサイズに関する正確な情報があれば、GSTを使う方が良い。
This means that one of the most appealing situations to use GAVI is when you don’t have accurate information about the sample size you’ll reach and you therefore underestimate the sample size as a strategy to have a valid test with reasonable power properties.
つまり、GAVIを使用する最も魅力的な状況の1つは、到達する標本サイズに関する正確な情報を持っておらず、したがって妥当な検出力特性を持つ有効な検定を行うための戦略として標本サイズを過小評価する場合である。
This begs the question, how well does GAVI perform under largely underestimated sample sizes?
このことは、GAVIが、ほとんど過小評価されたサンプル数のもとで、どの程度の実績を上げているのかという疑問を抱かせる。

In the simulation below we let the test be optimized for n=10 (note that since the variance is known this does not affect properties of the tests) whereas the actual sample size is 500, implying an underestimation of the order of 50 times.
下のシミュレーションでは、実際の標本サイズが500であるのに対して、検定をn=10（分散は既知なので、これは検定の特性には影響しないことに注意）に最適化させ、50倍のオーダーの過小評価を意味する。
This might seem like an extreme setting, but to put that in perspective, Eppo is currently using n=10,000 as the GAVI setting for all their sequential tests (Eppo 2023).
これは極端な設定と思われるかもしれないが、それを考慮すると、Eppoは現在、すべての逐次試験でGAVIの設定としてn=10,000を使用している（Eppo 2023）。
That is, the simulation corresponds to someone running a test with 500,000 users with Eppo’s current setting, which is plausible.
つまり、このシミュレーションは、誰かがエッポーの現在の設定で50万人のユーザーによるテストを実行したことに相当する。

Table 3 displays the empirical power over 100,000 Monte Carlo simulations.
表3は、100,000回のモンテカルロ・シミュレーションにおける経験的検出力を示している。
To benchmark, we also include the GST with correctly estimated n and a quadratic alpha spending function, which was the test that performed best in the comparison simulation (Table 2).
ベンチマークとして、正しく推定されたnと2次アルファ支出関数を用いたGSTも含めた（表2）。
The power loss from a 50x underestimation of n is around 15% as compared to GAVI with the correct n, and around 30% as compared to GST with the correct n.
nを50倍過小評価した場合の損失は、正しいnを用いたGAVIと比較して約15％、正しいnを用いたGSTと比較して約30％である。
The fact that the power is up to 30% lower indicates the importance of being able to estimate the sample size well to obtain high power in sequential testing.
検出力が最大30％低いという事実は、逐次検定で高い検出力を得るためには、サンプルサイズをうまく見積もることが重要であることを示している。

Given that the GAVI test allows for infinitely large samples, it’s quite remarkable it doesn’t lose more power when underestimating the sample size this severely.
GAVIテストが無限に大きなサンプルを許容することを考えると、サンプルサイズをこれほどひどく過小評価しても検出力が低下しないのは驚くべきことである。
However, it’s worth noting that for up to 56 preplanned intermittent analyses, the Bonferroni approach still outperforms the GAVI in terms of power.
しかし、あらかじめ計画された断続的な分析を56回まで行った場合、検出力という点では、ボンフェローニ法が依然としてGAVI法を上回っていることは注目に値する。

## Our recommendations for selecting a sequential test

Always valid inference is a sequential testing framework that works under very few restrictions.
常に有効な推論は、非常に少ない制約のもとで機能する逐次テストのフレームワークである。
For experimenters that are new to sequential testing and mostly want an early detection system with reliably bounded false positive rates, AVI is the framework to choose.
逐次テストに慣れていない実験者や、確実に偽陽性率を抑えた早期検出システムを望む実験者にとって、AVIは選択すべきフレームワークである。
For more sophisticated experimenters that are chasing power/smaller experiments using, for example, variance reduction, it should be used more carefully.
より洗練された実験者が、例えば分散削減などを用いてパワーを追い求めたり、小規模な実験を行ったりする場合には、より慎重に使用すべきである。
It’s not unlikely that you will lose as much power as standard variance reduction techniques will bring you.
標準的な分散削減技術がもたらすのと同じだけのパワーを失う可能性は低くない。
If you have historical data (which using a variance reduction approach like that suggested by Deng et al.(2013) typically implies), group sequential tests will typically give you substantially higher power.
過去のデータがある場合（Deng et al(2013)が提案しているような分散削減アプローチを用いることが一般的である）、群逐次検定は通常、かなり高い検出力を与える。

In any situation where it is not possible to estimate the sample size accurately, the AVI family of tests is a good choice for sequential testing if data is streamed.
サンプルサイズを正確に見積もることが不可能な状況では、データがストリーム配信されている場合、AVIファミリーのテストはシーケンシャルなテストに適しています。
If the data cannot be streamed, Bonferroni is also a good alternative, although it requires a prespecified max number of intermittent analyses.
データをストリーミングできない場合は、ボンフェローニも良い選択肢であるが、あらかじめ指定された最大断続分析回数が必要である。

If the sample size can be estimated accurately, but the experimenter wants the option to keep the experiment running longer (larger n) AVI is still a good choice, but with a few caveats.
サンプルサイズは正確に推定できるが、実験を長く続けたい（nを大きくしたい）場合、AVIは良い選択であるが、いくつかの注意点がある。
By using AVI when the sample size is estimable, the experimenter is losing power as compared to GST.
標本サイズが推定可能な場合にAVIを用いると、GSTに比べて検出力が低下する。
This means that while additional power can be gained from running the experiment longer than the estimated n first observations, it needs to make up for that loss before actually gaining power as compared to all possible tests that can be used in this situation.
これは、推定されたn回の最初のオブザベーションよりも長く実験を行うことによって、さらなる検出力を得ることができるが、この状況で使用できるすべての可能なテストと比較して、実際に検出力を得る前に、その損失を補う必要があることを意味する。

If data is available in stream and early detection of large regressions is the main concern, AVI is a good choice.
データがストリームで入手可能で、大きな回帰の早期発見が主な関心事であれば、AVIは良い選択である。
Neither GST or Bonferroni can handle streaming data, and if the regressions are large, power is not an issue.
GSTもボンフェローニもストリーミング・データを扱えないし、回帰が大きければ検出力は問題にならない。
For small regressions, it might be worth waiting for the first batch and using GST to have higher power for smaller sample sizes to detect the deterioration early.
小規模な回帰の場合、最初のバッチを待ち、GSTを使用する価値があるかもしれない。

If the sample size can be estimated accurately, and there is no need to be able to overrun, GST is a good choice.
サンプルサイズを正確に見積もることができ、オーバーランする必要がなければ、GSTは良い選択である。
This holds whether you can analyze in a streaming fashion or in batches.
これは、ストリーミングで分析する場合でも、バッチで分析する場合でも同じである。
Early detection of regressions can be achieved by running many intermittent analyses early in the experiment.
リグレッションの早期発見は、実験の初期に多くの断続的分析を実行することで達成できる。
If the expected sample size is underestimated on purpose to avoid oversampling, the alpha spending function should not be too conservative in the early phases of data collection.
オーバーサンプリングを避けるために、予想されるサンプルサイズが意図的に過小評価されている場合、アルファ支出関数はデータ収集の初期段階ではあまり保守的であってはならない。

A common misunderstanding of GST is that the number of intermittent analyses and their timing during data collection needs to be predetermined.
GSTについてよくある誤解は、データ収集中の断続的分析の回数とそのタイミングをあらかじめ決めておく必要があるというものである。
This is not the case, see for example Jennison and Turnbull (2000).
例えば、Jennison and Turnbull (2000)を参照されたい。
In fact, you can do as many or as few intermittent analyses as you want, whenever you want during the data collection — and you only pay for the peeking you make — which means you do not decrease power more than necessary.
実際、データ収集中、好きなときに好きなだけ断続的な分析を行うことができる。

Note on variance reduction: All of the tests presented in this post can also be combined with variance reduction to improve the precision of the experiFments.
分散削減に関するメモ： この投稿で紹介したすべてのテストは、分散削減と組み合わせて実験の精度を向上させることもできる。
The most popular variance reduction technique based on linear regression can be implemented in a two-step fashion, and it is therefore possible to perform residualization before any of the methods above.
線形回帰に基づく最も一般的な分散削減技法は、2つのステップで実装することができ、したがって、上記の方法のどれよりも前に残差化を実行することが可能です。
There are formal write-ups about how to perform variance reduction via regression without violating the respective framework for both Always Valid Inference (Lindon et al., 2022), and Group Sequential Tests (Jennison and Turnbull, 2000).
Always Valid Inference (Lindon et al., 2022)とGroup Sequential Tests (Jennison and Turnbull, 2000)の両方で、それぞれの枠組みを破ることなく、回帰によって分散削減を行う方法についての正式な記述があります。

This means that the relative comparisons between the methods in this post apply also under the most common type of variance reduction.
つまり、この投稿の手法間の相対的な比較は、最も一般的なタイプの分散削減の下でも当てはまるということです。

## Summary 要約

Spotify’s Experimentation Platform uses group sequential tests because this test was originally designed for medical studies where data arrived in batches — much like the data infrastructure that currently powers our experimentation platform.
Spotifyの実験プラットフォームは、group sequential testsを使用している。このテストはもともとデータがバッチで到着する医学研究向けに設計されたものであり、現在の実験プラットフォームの基盤となっているデータインフラストラクチャと非常によく似ている。
For streaming data, the group sequential test is not a viable option unless the data is analyzed in batches.
ストリーミング・データの場合、データをバッチで分析しない限り、グループ・シーケンシャル・テストは実行可能なオプションではない。
Our simulation study shows that even with access to streaming data, the probability that we will identify an effect, when one exists, is higher when the streaming data is analyzed in batches with the group sequential test than in a streaming fashion using any of the other two tests.
我々のシミュレーション研究によれば、ストリーミング・データにアクセスできる場合でも、効果が存在する場合にその効果を特定できる確率は、他の2つのテストのいずれかを用いて**ストリーミング方式で分析するよりも、group sequential testを用いてストリーミングデータをバッチで分析する方が高い**。

Regardless of the specific sequential test chosen, it is critical to use one.
具体的なsequential testが選ばれたとしても、それを使用することが重要である。
A key aspect of the experimentation platform offered to developers at Spotify is that we help them to continuously monitor experiments and detect any adverse effects promptly, without compromising the statistical validity of the experiments.
Spotifyの開発者に提供されている実験プラットフォームの重要な側面の1つは、統計的な妥当性を損なうことなく、**実験を継続的に監視し、迅速に悪影響を検出することを支援すること**である。
This would not be possible without a sequential test.
これはsequential testなしでは不可能である。

Acknowledgement: the authors thanks Mattias Frånberg, Erik Stenberg, and Lizzie Eardley for feedback and suggestions for this blog post.
謝辞 このブログ記事に対するフィードバックと提案をしてくれたMattias Frånberg、Erik Stenberg、Lizzie Eardleyに感謝する。
