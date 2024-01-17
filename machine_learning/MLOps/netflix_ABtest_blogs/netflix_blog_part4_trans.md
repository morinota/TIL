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
パート3： 偽陽性と統計的有意性では、検査結果を解釈する際に起こりうる2種類の誤りを定義した： 偽陽性と偽陰性です。
We then used simple thought exercises based on flipping coins to build intuition around false positives and related concepts such as statistical significance, p-values, and confidence intervals.
その後、コインをはじくという簡単な思考練習を行い、偽陽性や、統計的有意性、p値、信頼区間といった関連概念について直感を養った。
In this post, we’ll do the same for false negatives and the related concept of statistical power.
この投稿では、偽陰性と、それに関連する統計的検出力という概念についても同じことをする。

## False negatives and power 偽陰性とパワー

A false negative occurs when the data do not indicate a meaningful difference between treatment and control, but in truth there is a difference.
偽陰性は、データが治療と対照の間に意味のある差を示さないが、実際には差がある場合に起こる。
Continuing on an example from Part 3, a false negative corresponds to labeling the photo of the cat as a “not cat.” False negatives are closely related to the statistical concept of power, which gives the probability of a true positive given the experimental design and a true effect of a specific size.
第3回の例を続けると、偽陰性は猫の写真を "猫ではない "とラベル付けすることに相当する。偽陰性は検出力という統計学的概念と密接な関係があり、これは実験デザインと特定の大きさの真の効果が与えられた場合に、真陽性となる確率を示すものである。
In fact, power is simply one minus the false negative rate.
実際、検出力とは単純に1マイナス偽陰性率である。

Power involves thinking about possible outcomes given a specific assumption about the actual state of the world — similar to how in Part 3 we defined significance by first assuming the null hypothesis is true.
第3回で帰無仮説が真であると仮定して有意性を定義したのと同様である。
To build intuition about power, let’s go back to the same coin example from Part 3, where the goal is to decide if the coin is unfair using an experiment that calculates the fraction of heads in 100 flips.
ここでは、コインを100回ひっくり返して出た目の割合を計算する実験を使って、コインが不公平かどうかを判断することが目的である。
The distribution of outcomes under the null hypothesis that the coin is fair is shown in black in Figure 2.
コインは公平であるという帰無仮説のもとでの結果の分布を図2の黒で示す。
To make the diagram easier to interpret, we’ve smoothed over the tops of the histograms.
図を解釈しやすくするため、ヒストグラムの上部を平滑化した。

What would happen in this experiment if the coin is not fair? To make the thought exercise more specific, let’s work through what happens when we have a coin where heads occurs, on average, 64% of the time (the choice of that peculiar number will become clear later on).
もしコインが公平でなかったら、この実験では何が起こるだろうか？より具体的に考えるために、平均して64％の確率で表が出るコインを使った場合に何が起こるかを考えてみよう（この特異な数字の選択は後で明らかになる）。
Because there is uncertainty or noise in our experiment, we don’t expect to see exactly 64 heads in 100 flips.
実験には不確定要素やノイズがあるため、100回めくって64回正確に頭が出るとは思わない。
But as with the null hypothesis that the coin is fair, we can calculate all the possible outcomes if this specific alternative hypothesis is true.
しかし、「コインは公平である」という帰無仮説と同様に、この特定の対立仮説が真である場合に起こりうるすべての結果を計算することができる。
This distribution is shown with the red curve in Figure 2.
この分布は図2の赤い曲線で示されている。

Visually, power is the fraction of this alternative (red) distribution that lies beyond the critical values under the null hypothesis (the blue lines and black curve; see Part 3).
視覚的には、検出力とは、帰無仮説のもとでの臨界値（青い線と黒い曲線；第3部参照）を超える、この代替（赤）分布の割合のことである。
Here, 80% of the alternative distribution (red) falls to the right of the taller blue line that demarcates the critical value of the upper rejection region.
ここでは、代替分布の80％（赤）が、棄却域上限の臨界値を示す背の高い青い線の右側に位置している。
Assuming that the truth about the coin is that the probability of heads is 64%, then the power of this test is 80%.
コインの真実は、頭の確率が64％であると仮定すると、このテストの検出力は80％である。
To be complete, there is also a negligibly small part of the alternative (red) distribution that falls within the lower rejection region (to the left of the short blue line).
完全を期すため、代替分布（赤）には、（短い青線の左側の）下限棄却領域内に入る無視できるほど小さな部分もある。

The power of a test corresponds to a specific, postulated effect size.
検定の検出力は、特定の仮定された効果量に対応する。
In our example, the test has 80% power to detect that a coin is unfair, if that unfair coin in truth has a probability of heads equal to 64%.
この例では、不公平なコインの表が出る確率が64%である場合、そのコインは不公平であることを検出する80%の検出力があります。
The interpretation is as follows: if the coin has probability of heads equal to 64%, and we repeatedly run the experiment of flipping 100 times and making a decision at the 5% significance level, then we will correctly reject the null hypothesis that the coin is fair in about 4 out of every 5 experiments.
解釈は次のようになる： コインの表が出る確率が64％で、100回めくって有意水準5％で判定するという実験を繰り返すと、5回に4回くらいは「コインは公平である」という帰無仮説を正しく棄却できる。
And 20% of those repeated experiments will result in a false negative: we’ll not reject the null hypothesis that the coin is fair, even though it is unfair.
そして、繰り返される実験の20％は偽陰性となる： コインが不公平であっても、そのコインが公平であるという帰無仮説は棄却されない。

## Ways to increase power パワーを上げる方法

In designing an A/B test, we first fix the significance level (the convention is 5%: if there is no difference between treatment and control, we’ll see false positives 5% of the time), and then design the experiment to control false negatives.
A/Bテストの設計では、まず有意水準を決め（慣例は5％： 処理とコントロールの間に差がなければ、5％の確率で偽陽性を見ることになる）、そして偽陰性をコントロールするように実験をデザインする。
There are three primary levers we can pull to increase power and reduce the probability of false negatives:
パワーを高め、偽陰性の確率を減らすために、私たちが引くことのできる主なレバーが3つある：

1. Effect size. Simply put, the larger the effect size — the difference in metric values between Groups A and B — the higher the probability that we’ll be able to correctly detect that difference. To build intuition, think about running an experiment to determine if a coin is unfair, where the data we collect is the fraction of heads in 100 flips. Now think of two scenarios. In the first scenario, the true probability of heads is 55%, and in the second it is 75%. Intuitively (and mathematically!) it is more likely that our experiment identifies the coin as unfair in the second scenario. The true probability of heads is further from the null value of 50%, so it’s more likely that an experiment will produce an outcome that falls in the rejection region. In the product development context, we can increase the expected magnitude of metric movements by being bold vs incremental with the hypotheses we test. Another strategy to increase effect sizes is to test in new areas of the product, where there may be room for larger improvements in member satisfaction. That said, one of the joys of learning through experimentation is the element of surprise: at times, seemingly small changes can have a major impact on top-line metrics. 効果の大きさ。 簡単に言えば、効果量（A群とB群間の指標値の差）が大きければ大きいほど、その差を正しく検出できる確率が高くなるということだ。 直感を養うために、コインが不公平かどうかを判断する実験を行うことを考えてみよう。 ここで2つのシナリオを考えてみよう。 最初のシナリオでは、ヘッドが出る確率は55％、2番目のシナリオでは75％である。 直感的に（そして数学的に！）、私たちの実験では、2番目のシナリオでコインを不公平と識別する可能性が高い。 ヘッドの真の確率は、ヌル値である50％からさらに離れているので、実験が棄却域に入る結果をもたらす可能性が高くなる。 製品開発の文脈では、検証する仮説を大胆なものから漸進的なものにすることで、期待される指標の動きの大きさを増大させることができる。 効果サイズを大きくするもう一つの戦略は、会員満足度により大きな改善の余地があるかもしれない、製品の新しい分野でテストを行うことである。 とはいえ、実験を通じて学ぶ楽しみのひとつは、驚きの要素である： 一見小さな変化が、トップラインの指標に大きな影響を与えることがある。

2. Sample size. The more units in the experiment, the higher the power and the easier it is to correctly identify smaller effects. To build intuition, think again about running an experiment to determine if a coin is unfair, where the data we collect is the fraction of heads in a fixed number of flips and the true probability of heads is 64%. Consider two scenarios: in the first, we flip the coin 20 times, and in the second, we flip the coin 100 times. Intuitively (and mathematically!), it is more likely that our experiment identifies the coin as unfair in the second scenario. With more data, the result from the experiment is going to be closer to the true rate of 64% heads, while the outcomes under the assumption of a fair coin concentrate around 0.50, causing the rejection region to encroach on the 50% value. These effects combine, so that with more data there is a greater probability that the result from the experiment with the unfair coin will fall in that rejection region, resulting in a true positive. In the product development context, we can increase the power by allocating more members (or other units) to the test or by reducing the number of test groups, though there is a tradeoff between the sample size in each test and the number of non-overlapping tests that can be run at the same time. サンプルサイズ。 実験単位が多ければ多いほど検出力が高くなり、より小さな効果を正しく識別しやすくなる。 直感を養うために、コインが不公平かどうかを判断する実験を行うことをもう一度考えてみよう。ここで収集するデータは、一定回数の反転で表が出た割合であり、表が出る真の確率は64％である。 二つのシナリオを考えてみよう： 1つ目はコインを20回裏返す場合、2つ目はコインを100回裏返す場合である。 直感的に（そして数学的に！）、私たちの実験では、2番目のシナリオでコインを不公平と識別する可能性が高い。 より多くのデータがあれば、実験結果は64％のヘッドという真の確率に近づくだろう。一方、公平なコインを仮定した場合の結果は0.50前後に集中し、棄却領域が50％の値に近づいていく。 これらの効果が組み合わさり、データが多ければ多いほど、不公平なコインを使った実験の結果がその棄却領域に入る確率が高くなり、結果として真陽性となる。 製品開発の文脈では、より多くのメンバー（または他のユニット）をテストに割り当てるか、テストグループの数を減らすことで検出力を高めることができますが、各テストにおけるサンプルサイズと同時に実行できる重複しないテストの数との間にはトレードオフがあります。

3. The variability of the metric in the underlying population. The more homogenous the metric within the population we are testing on, the easier it is to correctly identify true effects. The intuition for this one is a bit trickier, and our simple coin examples finally break down. Say at Netflix that we run a test that aims to reduce some measure of latency, such as the delay between a member pressing play and video playback commencing. Given the variety of devices and internet connections that people use to access Netflix, there is a lot of natural variability in this metric across our users. As a result, if the test treatment results in a small reduction in the latency metric, it’s hard to successfully identify — the “noise” from the variability across members overwhelms the small signal. In contrast, if we ran the test on a set of members that used similar devices with similar web connections, then the small signal is easier to identify — there is less noise that might drown out the signal. We spend a lot of time at Netflix building statistical analysis models that exploit this intuition, and increase power by effectively lowering the variability; see here for a technical description of our approach. 基礎となる集団における指標の変動性。 母集団内の測定基準が均一であればあるほど、真の効果を正しく同定しやすくなる。 この直感は少し厄介で、単純なコインの例は最終的に破綻する。 例えば、会員が再生ボタンを押してからビデオ再生が始まるまでの遅延などです。 人々がNetflixにアクセスするために使用するデバイスやインターネット接続が多様であることを考えると、この指標にはユーザー間で多くの自然なばらつきがあります。 その結果、もし試験的な治療によって待ち時間の指標がわずかに減少したとしても、それをうまく特定することは難しい。メンバー間のばらつきによる「ノイズ」が、小さなシグナルを圧倒してしまうのだ。 対照的に、同じようなデバイスを使い、同じようなウェブ接続をしているメンバーでテストを行った場合、小さなシグナルを特定するのは容易である。 ネットフリックスでは、この直感を利用した統計解析モデルの構築に多くの時間を費やしており、効果的にばらつきを小さくすることでパワーを高めている。

## Powering for reasonable and meaningful effects 合理的で意味のある効果を生み出すためのパワー

Power and the false negative rate are functions of a postulated effect size.
検出力と偽陰性率は、想定される効果量の関数である。
Much like how the 5% false positive rate is a widely-accepted convention, the rule of thumb with power is to aim for 80% power for a reasonable and meaningful effect size (we’ll get to each of those below).
5％の偽陽性率が広く受け入れられている慣例であるのと同様に、検出力に関する経験則は、妥当で意味のある効果量に対して80％の検出力を目指すことである（以下、それぞれについて説明する）。
That is, we postulate an effect size and then design the experiment, primarily through setting the sample size, such that, if the true impact of the treatment experience is as we’ve postulated, the test will correctly identify that there is an effect 80% of the time.
つまり、効果量を仮定し、主にサンプルサイズを設定することで、治療経験の真の影響が仮定した通りであれば、テストは80％の確率で効果があると正しく識別できるように実験をデザインする。
And 20% of the time the result from the test will be a false negative: in truth, there is an effect, but our observation from the test does not lie in the rejection region and we fail to conclude that there is an effect.
そして20％は偽陰性である： 本当は効果があるのだが、テストによる観察結果が棄却域にないため、効果があると結論づけられないのである。
That’s why the examples above used a 64% probability of heads: an experiment with 100 flips then has 80% power.
そのため、上記の例ではヘッドの確率を64％としている： 100回の実験では、80％の検出力がある。

What constitutes a reasonable effect size can be tricky, as tests can surprise us.
何をもって妥当な効果量とするかは、テストが私たちを驚かせることもあるので、難しいところである。
But a mix of domain knowledge and common sense can generally provide solid estimates.
しかし、領域に関する知識と常識を組み合わせることで、一般的に確かな見積もりを出すことができる。
In an area where testing has a long history, such as optimizing the recommendation systems that help Netflix members choose content that’s great for them, we have a solid idea about the effect sizes that our tests tend to produce (be they positive or negative).
ネットフリックスの会員が自分に最適なコンテンツを選べるようにするレコメンデーションシステムの最適化など、テストに長い歴史がある分野では、私たちはテストが（ポジティブであれネガティブであれ）生み出しがちな効果量について確かな考えを持っている。
Given an understanding of past effect sizes, as well as the analysis strategy, we can set the sample size to ensure the test has 80% power for a reasonable metric movement.
過去の効果量と分析戦略を理解すれば、妥当な指標移動に対して検定が80％の検出力を持つようにサンプルサイズを設定することができる。

The second consideration, both in this experimental design phase and in deciding where to invest efforts, is to determine what constitutes a meaningful impact to the primary metrics used to decide the test.
この実験計画の段階でも、また労力を投下する場所を決定する上でも、2番目に考慮すべきことは、テストを決定するために使用される主要な測定基準に対して、何が意味のある影響を構成するかを決定することである。
What is meaningful will depend on the impact area of the experiment (member satisfaction, playback latency, technical performance of back end systems, etc.), and potentially the effort or costs associated with the new product experience.
何が有意義かは、実験の影響範囲（会員の満足度、再生レイテンシー、バックエンドシステムの技術的パフォーマンスなど）や、潜在的には新商品体験に関連する労力やコストによって異なる。
As a hypothetical, say that, for effect sizes smaller than a 0.1% change in the primary metric, the cost of supporting the new product feature outweighs the benefits.
仮定の話として、主要指標の0.1％の変化より小さい効果量では、新製品の機能をサポートするコストが利益を上回るとする。
In this case, there’s little point in powering a test to detect a 0.01% change in the metric, as successfully identifying an effect of that size won’t result in a meaningful change in decisions.
この場合、指標の0.01％の変化を検出するためにテストにパワーをかける意味はほとんどない。なぜなら、そのサイズの効果をうまく特定しても、意思決定に意味のある変化をもたらすことはないからだ。
Likewise, if the effect sizes seen in tests in a given innovation area are consistently immaterial to the user experience or the business, that’s a sign that experimentation resources can be more efficiently deployed elsewhere.
同様に、あるイノベーション分野のテストで見られる効果の大きさが、一貫してユーザーエクスペリエンスやビジネスにとって重要でない場合、それは実験リソースをより効率的に他の場所に配置できる兆候である。

## Summary 要約

Parts 3 and 4 of this series have focussed on defining and building intuition around the core concepts used to analyze test results: false positives and negatives, statistical significance, p-values, and power.
このシリーズの第3回と第4回は、テスト結果の分析に使われる中核概念の定義と直感の構築に焦点をあててきた： 偽陽性と陰性、統計的有意性、p値、検出力。

An uncomfortable truth about experimentation is that we can’t simultaneously minimize both false positives and false negatives.
実験に関する不快な真実は、偽陽性と偽陰性の両方を同時に最小限に抑えることはできないということだ。
In fact, false positives and negatives trade off with one another.
実際、偽陽性と偽陰性は互いにトレードオフの関係にある。
If we used a more stringent false positive rate, such as 0.01%, we’d reduce the number of false positives for tests where there is no difference between A and B — but we’d also reduce the power of the test, increasing the rate of false negatives, for those tests where there is a meaningful difference.
0.01％など、より厳格な偽陽性率を用いれば、AとBの間に差がない検査での偽陽性の数は減るだろうが、有意差がある検査では偽陰性の割合が増え、検出力が低下する。
Using a 5% false positive rate and targeting 80% power are well-established conventions that balance between limiting false discovery and enabling true discovery.
5％の偽陽性率を使用し、80％の検出力を目標とすることは、偽の発見を制限することと真の発見を可能にすることの間でバランスをとる、確立された慣例である。
However, in instances where a false positive (or false negative) poses a larger risk, researchers may deviate from these rules of thumb to minimize one type of uncertainty over another.
しかし、偽陽性（または偽陰性）がより大きなリスクとなる場合、研究者はこれらの経験則から逸脱して、ある種の不確実性を他のものよりも最小化することがある。

Our goal is not to eliminate uncertainty, but to understand and quantify the uncertainty in order to make sound decisions.
私たちの目標は不確実性を排除することではなく、健全な意思決定を行うために不確実性を理解し、定量化することである。
In many cases, results from A/B tests require nuanced interpretation, and in fact the test result itself is only one input into a business decision.
多くの場合、A/Bテストの結果には微妙な解釈が必要であり、実際、テスト結果自体はビジネス上の意思決定のための1つのインプットに過ぎない。
In the next post, we’ll cover how to build confidence in a decision using test results.
次回は、テスト結果を使って決断に自信をつける方法を取り上げる。
Follow the Netflix Tech Blog to stay up to date.
最新情報はNetflix Tech Blogをフォローしてください。