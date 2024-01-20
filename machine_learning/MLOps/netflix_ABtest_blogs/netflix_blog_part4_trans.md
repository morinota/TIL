## link リンク

https://netflixtechblog.com/interpreting-a-b-test-results-false-negatives-and-power-6943995cf3a8
https://netflixtechblog.com/interpreting-a-b-test-results-false-negatives-and-power-6943995cf3a8

# Interpreting A/B test results: false negatives and power A/Bテスト結果の解釈： 偽陰性と検出力

This is the fourth post in a multi-part series on how Netflix uses A/B tests to inform decisions and continuously innovate on our products.
この記事は、NetflixがどのようにA/Bテストを使用して意思決定を行い、継続的に製品を革新しているかについて、複数回に分けてご紹介するシリーズの4回目です。
Need to catch up? Have a look at Part 1 (Decision Making at Netflix), Part 2 (What is an A/B Test?), Part 3 (False positives and statistical significance).
追いつく必要がありますか？パート1（Netflixにおける意思決定）、パート2（A/Bテストとは）、パート3（偽陽性と統計的有意性）をご覧ください。
Subsequent posts will go into more details on experimentation across Netflix, how Netflix has invested in infrastructure to support and scale experimentation, and the importance of the culture of experimentation within Netflix.
この後の記事では、Netflix全体における実験、Netflixが実験をサポートし拡大するためのインフラへの投資方法、Netflixにおける実験文化の重要性について、さらに詳しく説明する予定だ。

In Part 3: False positives and statistical significance, we defined the two types of mistakes that can occur when interpreting test results: false positives and false negatives.
パート3： false positives and statistical significanceでは、テスト結果を解釈する際に発生しうる2種類の間違い、すなわちfalse positivesとfalse negativesを定義した。
We then used simple thought exercises based on flipping coins to build intuition around false positives and related concepts such as statistical significance, p-values, and confidence intervals.
その後、コインをはじくという簡単な思考練習を行い、false positivesと統計的有意性、p値、confidence intervalsなどの関連概念について直感を養った。
In this post, we’ll do the same for false negatives and the related concept of statistical power.
この投稿では、false negativesとstatistical powerという関連概念についても同様に行う。

## False negatives and power 偽陰性とパワー

A false negative occurs when the data do not indicate a meaningful difference between treatment and control, but in truth there is a difference.
false negativeとは、(観測された)データが処理とコントロールの間に意味のある差を示していないが、実際には差がある場合のことである。
Continuing on an example from Part 3, a false negative corresponds to labeling the photo of the cat as a “not cat.”
第3回の例を続けると、偽陰性は猫の写真を "猫ではない "とラベル付けすることに相当する。
False negatives are closely related to the statistical concept of power, which gives the probability of a true positive given the experimental design and a true effect of a specific size.
**false negativesは、実験設計と特定のサイズの真の効果が与えられたときのtrue positiveの確率を与える、統計的概念であるpowerと密接に関連している**。
In fact, power is simply one minus the false negative rate.
実際、powerは単に1からfalse negative rate(=これは許容するfalse negative rateの値?)を引いたものである。

Power involves thinking about possible outcomes given a specific assumption about the actual state of the world — similar to how in Part 3 we defined significance by first assuming the null hypothesis is true.
**powerは、実際の世界の状態についての特定の仮定が与えられたときの可能な結果について考えることを含む**。これは、第3部にて、まず帰無仮説が真であると仮定することで有意性を定義したものと同様。
To build intuition about power, let’s go back to the same coin example from Part 3, where the goal is to decide if the coin is unfair using an experiment that calculates the fraction of heads in 100 flips.
powerについての直感を養うために、第3部の同じコインの例に戻ってみよう。ここでは、**100回の反転で表が出る割合を計算する実験を使って、コインが不公平であるかどうかを判断することが目的**である。(うんうん。ここで100回はサンプルサイズに該当するのかな...!)
The distribution of outcomes under the null hypothesis that the coin is fair is shown in black in Figure 2.
コインは公平であるという帰無仮説のもとでの結果の分布を図2の黒で示す。(= null distribution!)
To make the diagram easier to interpret, we’ve smoothed over the tops of the histograms.
図を解釈しやすくするため、ヒストグラムの上部を平滑化した。

![figure2]()

What would happen in this experiment if the coin is not fair? To make the thought exercise more specific, let’s work through what happens when we have a coin where heads occurs, on average, 64% of the time (the choice of that peculiar number will become clear later on).
**もしコインが公平でなかったら、この実験では何が起こるだろうか?**より具体的に考えるために、**平均して64％の確率で表が出るコインを使った場合に何が起こるかを考えてみよう**(**この特異な数字の選択は後で明らかになる**)。
Because there is uncertainty or noise in our experiment, we don’t expect to see exactly 64 heads in 100 flips.
実験には不確定要素やノイズがあるため、100回めくって64回正確に頭が出るとは思わない。
But as with the null hypothesis that the coin is fair, we can calculate all the possible outcomes if this specific alternative hypothesis is true.
しかし、「コインは公平である」という帰無仮説と同様に、この特定の対立仮説が真である場合に起こりうるすべての結果を計算することができる。
This distribution is shown with the red curve in Figure 2.
この分布は図2の赤い曲線で示されている。(=これはalternative distributionっていうのかな??)

Visually, power is the fraction of this alternative (red) distribution that lies beyond the critical values under the null hypothesis (the blue lines and black curve; see Part 3).
視覚的には、**powerは、帰無仮説(青い線と黒い曲線; Part 3を参照)のcritial value(=rejection regionの境界値)を超えるalternative distribution(赤い曲線)の割合**である。
Here, 80% of the alternative distribution (red) falls to the right of the taller blue line that demarcates the critical value of the upper rejection region.
**ここでは、alternative distribution(赤い曲線)の80％が、upper rejection regionの境界値を示す高い青い線の右側にある**。(うんうん...!)
Assuming that the truth about the coin is that the probability of heads is 64%, then the power of this test is 80%.
コインの真実は、表の確率が64％であると仮定すると、このテストのpower は80％である。(なるほど...!alternative distributionを仮定した上じゃないと、powerは計算できないのか...!)
To be complete, there is also a negligibly small part of the alternative (red) distribution that falls within the lower rejection region (to the left of the short blue line).
完全であるためには(i.e. power=100%であるためには???)、alternative distribution(赤い曲線)のほんのわずかな部分が、lower rejection region(短い青い線の左側)に含まれている。

The power of a test corresponds to a specific, postulated effect size.
テストのpowerは、**特定の仮定されたeffect sizeに対応する**。(i.e. 依存する...!)
In our example, the test has 80% power to detect that a coin is unfair, if that unfair coin in truth has a probability of heads equal to 64%.
この例では、不公平なコインの表が出る確率が64%(=ABテストにおける想定するeffect size?)である場合、そのコインは不公平であることを検出する80%の検出力があります。
The interpretation is as follows: if the coin has probability of heads equal to 64%, and we repeatedly run the experiment of flipping 100 times and making a decision at the 5% significance level, then we will correctly reject the null hypothesis that the coin is fair in about 4 out of every 5 experiments.
解釈は次のようになる： コインの表が出る確率が64％ (=effect size?)で、100回(=sample size?)めくって5％のsignificance level (=false positive rateの許容する値) で判断する実験を繰り返し行うと、5回の実験のうち約4回で、コインが公平であるという帰無仮説を正しくrejectすることができる。
And 20% of those repeated experiments will result in a false negative: we’ll not reject the null hypothesis that the coin is fair, even though it is unfair.
そして、繰り返される実験のうちの20％はfalse negativeとなり、コインが不公平であるにもかかわらず、コインが公平であるという帰無仮説をrejectすることはない。

## Ways to increase power パワーを上げる方法

In designing an A/B test, we first fix the significance level (the convention is 5%: if there is no difference between treatment and control, we’ll see false positives 5% of the time), and then design the experiment to control false negatives.
A/Bテストの設計では、まず significance level(慣例では5％：処理とコントロールの間に差がない場合、5％の確率でfalse positivesが発生する)(=許容するfalse positiveの値...!)を固定し、その後、false negatives(=許容するfalse negativeの値)を制御するために実験を設計する。
There are three primary levers we can pull to increase power and reduce the probability of false negatives:
**powerを高め、false negativeの確率を減らすために、私たちが引くことのできる主なレバー(=実験のハイパーパラメータ?)が3つ**ある:

### Effect size.

Simply put, the larger the effect size — the difference in metric values between Groups A and B — the higher the probability that we’ll be able to correctly detect that difference.
単純に言えば、効果量が大きければ大きいほど、AグループとBグループの間の指標値の差が大きくなり、その差を正しく検出できる確率が高くなる。
To build intuition, think about running an experiment to determine if a coin is unfair, where the data we collect is the fraction of heads in 100 flips.
感覚を深めるために、コインが不公平かどうかを判断する実験を行うことを考えてみよう。ここで収集するデータは、100回の反転で表が出た割合である。
Now think of two scenarios. In the first scenario, the true probability of heads is 55%, and in the second it is 75%.
ここで、2つのシナリオを考えてみよう。1つ目のシナリオでは、表が出る真の確率は55％であり、2つ目のシナリオでは75％である。(2種類のeffect sizeか)
Intuitively (and mathematically!) it is more likely that our experiment identifies the coin as unfair in the second scenario.
直感的に（そして数学的に！）、2番目のシナリオでは、コインを不公平と識別する可能性が高い。
The true probability of heads is further from the null value of 50%, so it’s more likely that an experiment will produce an outcome that falls in the rejection region.
表が出る真の確率は、50％という帰無仮説からさらに離れているため、実験結果がrejection regionに入る可能性が高くなる。
In the product development context, we can increase the expected magnitude of metric movements by being bold vs incremental with the hypotheses we test.
プロダクト開発の文脈では、テストする仮説に対して大胆になることで、指標の移動の予想される大きさを増やすことができる。
Another strategy to increase effect sizes is to test in new areas of the product, where there may be room for larger improvements in member satisfaction.
効果量を増やすための別の戦略は、ユーザの満足度をより大きく向上させる余地があるproductの新しい領域でテストすることである。
That said, one of the joys of learning through experimentation is the element of surprise: at times, seemingly small changes can have a major impact on top-line metrics.
とはいえ、実験を通じて学ぶことの喜びの一つは、驚きの要素である。時には、小さな変化でもトップラインの指標(=重要なビジネス指標のこと??)に大きな影響を与えることがある。

### Sample size.

The more units in the experiment, the higher the power and the easier it is to correctly identify smaller effects.
実験の単位が多ければ多いほど、power が高くなり、より小さな効果を正しく識別しやすくなる。
To build intuition, think again about running an experiment to determine if a coin is unfair, where the data we collect is the fraction of heads in a fixed number of flips and the true probability of heads is 64%.
感覚を深めるために、コインが不公平かどうかを判断する実験を行うことをもう一度考えてみよう。ここで収集するデータは、一定回数の反転で表が出た割合であり、表が出る真の確率は64％(=effect size)である。
Consider two scenarios: in the first, we flip the coin 20 times, and in the second, we flip the coin 100 times.
二つのシナリオを考えてみよう： 1つ目はコインを20回裏返す場合、2つ目はコインを100回裏返す場合である。
Intuitively (and mathematically!), it is more likely that our experiment identifies the coin as unfair in the second scenario.
感覚的に（そして数学的に！）、2番目のシナリオでは、コインを不公平と識別する可能性が高い。
With more data, the result from the experiment is going to be closer to the true rate of 64% heads, while the outcomes under the assumption of a fair coin concentrate around 0.50, causing the rejection region to encroach on the 50% value.
より多くのデータがあれば、実験結果は64％の表という真の確率に近づくだろう。一方、公平なコインを仮定した場合の結果は0.50前後に集中し、rejection regionが50％の値に近づいていく。
(?? rejectin regionはsample sizeに影響をうけるんだっけ? p-valueがsignificance levelより低いか否か = rejection regionに入るか否か = confidence intervalがnull値を含まないか否か、これらは等価だから、影響を受けるのかな...? 母分散は不変だけど、標本分散はsample sizeに依存する、みたいな話かな??)
These effects combine, so that with more data there is a greater probability that the result from the experiment with the unfair coin will fall in that rejection region, resulting in a true positive.
これらの効果が組み合わさり、より多くのデータがあれば、不公平なコインを使った実験の結果がそのrejection regionに入る確率が高くなり、結果としてtrue positiveとなる。
In the product development context, we can increase the power by allocating more members (or other units) to the test or by reducing the number of test groups, though there is a tradeoff between the sample size in each test and the number of non-overlapping tests that can be run at the same time.
プロダクト開発の文脈では、テストに割り当てるユーザ(または他の単位、sessionなど)を増やすか、テストグループ(i.e. variant)の数を減らすことで、powerを高めることができる。ただし、各テストのサンプルサイズと、同時に実行できる重複しないテストの数との間にはトレードオフがある。

### The variability of the metric in the underlying population. 基礎となる集団における指標の変動性

(分布の母分散的な? ばらつきが小さいか否か、みたいな)

The more homogenous the metric within the population we are testing on, the easier it is to correctly identify true effects. The intuition for this one is a bit trickier, and our simple coin examples finally break down.
集団内の指標が均一であればあるほど、真の効果を正しく同定しやすくなる。 この直感は少し厄介で、単純なコインの例は最終的に破綻する。(確かにコインの例では、期待値が同じだけど、ばらつきが大きい小さい、みたいな想像はつきづらいかも...??)
Say at Netflix that we run a test that aims to reduce some measure of latency, such as the delay between a member pressing play and video playback commencing.
ネットフリックスでは、再生ボタンを押してからビデオ再生が始まるまでの遅延などの、**latencyの測定を減らすことを目的としたテスト**を実行するとしよう。
Given the variety of devices and internet connections that people use to access Netflix, there is a lot of natural variability in this metric across our users.
ネットフリックスにアクセスするために人々が使用するデバイスやインターネット接続が多様であることを考えると、**この指標にはユーザ間で多くの自然なばらつきがある**。(確かに、latencyはアプリ由来とユーザ由来の2つの要因があるからか...!)
As a result, if the test treatment results in a small reduction in the latency metric, it’s hard to successfully identify — the “noise” from the variability across members overwhelms the small signal.
その結果、もし試験的なtreatmentによってlatencyの指標がわずかに減少したとしても、それをうまく特定することは難しい。**ユーザ間のばらつきによる「ノイズ」が、小さなシグナルを圧倒してしまうのだ**。
In contrast, if we ran the test on a set of members that used similar devices with similar web connections, then the small signal is easier to identify — there is less noise that might drown out the signal.
対象的に、同じデバイスと同じweb接続を使用するユーザのセットでテストを実行した場合、小さなシグナルを特定するのは簡単である。つまり、**シグナルをかき消す可能性のあるノイズが少ない**のだ。
We spend a lot of time at Netflix building statistical analysis models that exploit this intuition, and increase power by effectively lowering the variability; see here for a technical description of our approach.
ネットフリックスでは、この直感を利用してpowerを高め、ばらつきを効果的に低下させる統計分析モデルを構築するために多くの時間を費やしている。アプローチの技術的な説明は[こちら](https://arxiv.org/pdf/1910.01305.pdf)を参照。

## Powering for reasonable and meaningful effects 合理的で意味のある効果を生み出すためのパワー

Power and the false negative rate are functions of a postulated effect size.
**powerとfalse negative rate(=テストでのfalse negative のリスク)は、仮定された効果量の関数である**。
Much like how the 5% false positive rate is a widely-accepted convention, the rule of thumb with power is to aim for 80% power for a reasonable and meaningful effect size (we’ll get to each of those below).
5％のfalse positive rateが広く受け入れられているのと同様に、**powerの経験則は、合理的(reasonable)で意味のある(meaningful)効果量に対して80％のpowerを目指すこと**である(以下でそれぞれについて説明する)。
That is, we postulate an effect size and then design the experiment, primarily through setting the sample size, such that, if the true impact of the treatment experience is as we’ve postulated, the test will correctly identify that there is an effect 80% of the time.
つまり、**効果量を仮定し、主にsample sizeを設定することで、もしtreatment experienceの真の影響が仮定したものと同じであれば、テストは80％の確率で効果を正しく特定することができる**。
And 20% of the time the result from the test will be a false negative: in truth, there is an effect, but our observation from the test does not lie in the rejection region and we fail to conclude that there is an effect.
そして20％はfalse negativeとなり、実際には効果があるが、テストの結果はrejection regionになく、効果があると結論付けることができない。
That’s why the examples above used a 64% probability of heads: an experiment with 100 flips then has 80% power.
そのため、上記の例では表の確率を64％としている： 100回の実験では、80％の検出力がある。

What constitutes a reasonable effect size can be tricky, as tests can surprise us.
**何をもって妥当な効果量とするかは、テストが私たちを驚かせることもあるので、難しいところ**である。
But a mix of domain knowledge and common sense can generally provide solid estimates.
しかし、ドメイン知識と常識を組み合わせることで、一般的に確かな見積もりを出すことができる。
In an area where testing has a long history, such as optimizing the recommendation systems that help Netflix members choose content that’s great for them, we have a solid idea about the effect sizes that our tests tend to produce (be they positive or negative).
netflixのユーザが自分にとって最適なコンテンツを選択するのを助ける推薦システムを最適化するなど、**テストの歴史が長い分野では、テストが生み出す効果量(正のものも負のものも)について、確かな見積もりができる**。(CTRがこれくらい上がるはず、とか??)
Given an understanding of past effect sizes, as well as the analysis strategy, we can set the sample size to ensure the test has 80% power for a reasonable metric movement.
過去の効果量と分析戦略を理解すれば、妥当な指標移動に対して検定が80％のpowerを持つように、sample sizeを設定することができる。

The second consideration, both in this experimental design phase and in deciding where to invest efforts, is to determine what constitutes a meaningful impact to the primary metrics used to decide the test.
この実験設計フェーズと、どこに努力を投資するかを決定する際の**第二の考慮事項は、テストを決定するために使用されるprimary metricsに対する意味のある(meaningfulな)影響を決定すること**である。(ex. 新施策によってCTRを1%改善することによる利益が、新施策の開発・運用コストよりも上回っているか、みたいな??)
What is meaningful will depend on the impact area of the experiment (member satisfaction, playback latency, technical performance of back end systems, etc.), and potentially the effort or costs associated with the new product experience.
何が有意義かは、実験の影響範囲（会員の満足度、再生レイテンシー、バックエンドシステムの技術的パフォーマンスなど）や、潜在的には新商品体験に関連する労力やコストによって異なる。
As a hypothetical, say that, for effect sizes smaller than a 0.1% change in the primary metric, the cost of supporting the new product feature outweighs the benefits.
仮定の話として、primary metricsの0.1%よりも小さいeffect sizeによる利益よりも、新しい product featureをサポートするコストが上回るとしよう。
In this case, there’s little point in powering a test to detect a 0.01% change in the metric, as successfully identifying an effect of that size won’t result in a meaningful change in decisions.
この場合、指標の0.01％の変化を検出するためにテストにpowerを与えることにはあまり意味がない。なぜなら、**そのようなサイズの効果を正しく特定しても、意思決定に意味のある(meaningfulな)変化は生じないから**である。
Likewise, if the effect sizes seen in tests in a given innovation area are consistently immaterial to the user experience or the business, that’s a sign that experimentation resources can be more efficiently deployed elsewhere.
同様に、**あるイノベーション分野のテストで見られる効果の大きさが、一貫してユーザエクスペリエンスやビジネスにとって重要でない場合、それは実験リソースをより効率的に他の場所に配置できる兆候**である。

## Summary 要約

Parts 3 and 4 of this series have focussed on defining and building intuition around the core concepts used to analyze test results: false positives and negatives, statistical significance, p-values, and power.
このシリーズの第3回と第4回は、テスト結果の分析に使われる中核概念の定義と直感の構築に焦点をあててきた： false positivesとfalse negatives、statistical significance、p-values(=これらは許容するfalse positive rateの値に依存)、power(=許容するfalse negative rateの値に依存)。

An uncomfortable truth about experimentation is that we can’t simultaneously minimize both false positives and false negatives.
実験に関する不快な真実は、偽陽性と偽陰性の両方を同時に最小限に抑えることはできないということだ。
In fact, false positives and negatives trade off with one another.
実際、**偽陽性と偽陰性は互いにトレードオフの関係**にある。
If we used a more stringent false positive rate, such as 0.01%, we’d reduce the number of false positives for tests where there is no difference between A and B — but we’d also reduce the power of the test, increasing the rate of false negatives, for those tests where there is a meaningful difference.
0.01％など、より厳格なfalse positive rateを使用すると、AとBの間に差がないテストのfalse positiveの数を減らすことができるが、AとBの間に意味のある差があるテストのfalse negativeの割合を増やし、テストのpowerを低下させることにもなる。
Using a 5% false positive rate and targeting 80% power are well-established conventions that balance between limiting false discovery and enabling true discovery.
**5％のfalse positive rateと80％のpowerを目標とすることは、false discoveryを制限し、true discoveryを可能にするというバランスをとることができる、確立された慣習である**。
However, in instances where a false positive (or false negative) poses a larger risk, researchers may deviate from these rules of thumb to minimize one type of uncertainty over another.
しかし、**false positive(またはfalse negative)がより大きなリスクをもたらす場合**、研究者は、**ある種の不確実性を他の不確実性よりも最小限に抑えるために、これらの経験則から逸脱する場合がある**。(ex. type I errorの方がtype II errorよりも大きなリスクをもたらす場合、みたいな??)

Our goal is not to eliminate uncertainty, but to understand and quantify the uncertainty in order to make sound decisions.
**私たちの目標は不確実性を排除することではなく、健全な意思決定を行うために不確実性を理解し、定量化することである**。
In many cases, results from A/B tests require nuanced interpretation, and in fact the test result itself is only one input into a business decision.
多くの場合、A/Bテストの結果には微妙な解釈が必要であり、**実際、テスト結果自体はビジネス上の意思決定のための1つのインプットに過ぎない**。
In the next post, we’ll cover how to build confidence in a decision using test results.
次回は、テスト結果を使って決断に自信をつける方法を取り上げる。
Follow the Netflix Tech Blog to stay up to date.
最新情報はNetflix Tech Blogをフォローしてください。
