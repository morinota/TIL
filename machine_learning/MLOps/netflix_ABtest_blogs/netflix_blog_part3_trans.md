## link リンク

https://netflixtechblog.com/interpreting-a-b-test-results-false-positives-and-statistical-significance-c1522d0db27a
https://netflixtechblog.com/interpreting-a-b-test-results-false-positives-and-statistical-significance-c1522d0db27a

# Interpreting A/B test results: false positives and statistical significance A/Bテスト結果の解釈： 偽陽性と統計的有意性

This is the third post in a multi-part series on how Netflix uses A/B tests to inform decisions and continuously innovate on our products.
この記事は、NetflixがどのようにA/Bテストを使用して意思決定を行い、継続的に製品を革新しているかについての複数回シリーズの3回目です。
Need to catch up? Have a look at Part 1 (Decision Making at Netflix) and Part 2 (What is an A/B Test?).
追いつく必要がありますか？パート1（Netflixにおける意思決定）とパート2（A/Bテストとは）をご覧ください。
Subsequent posts will go into more details on experimentation across Netflix, how Netflix has invested in infrastructure to support and scale experimentation, and the importance of the culture of experimentation within Netflix.
次回の記事では、Netflix全体における実験の詳細、Netflixが実験をサポートし拡大するためのインフラにどのように投資してきたか、Netflixにおける実験文化の重要性について説明する。

In Part 2: What is an A/B Test we talked about testing the Top 10 lists on Netflix, and how the primary decision metric for this test was a measure of member satisfaction with Netflix.
パート2： A/Bテストとは何か」では、Netflixのトップ10リストのテストについて、そしてこのテストの主要な決定指標が、Netflixに対する会員の満足度を測るものであったことについてお話しました。
If a test like this shows a statistically significant improvement in the primary decision metric, the feature is a strong candidate for a roll out to all of our members.
このようなテストにより、主要な決定指標において統計的に有意な改善が見られた場合、その機能は全メンバーに展開する有力な候補となります。
But how do we know if we’ve made the right decision, given the results of the test? It’s important to acknowledge that no approach to decision making can entirely eliminate uncertainty and the possibility of making mistakes.
しかし、テストの結果を受けて、正しい決断を下したかどうかをどうやって知ることができるのだろうか？意思決定に対するどんなアプローチも、不確実性や間違いを犯す可能性を完全に排除することはできないことを認めることが重要だ。
Using a framework based on hypothesis generation, A/B testing, and statistical analysis allows us to carefully quantify uncertainties, and understand the probabilities of making different types of mistakes.
仮説生成、A/Bテスト、統計分析に基づくフレームワークを使用することで、不確実性を慎重に定量化し、さまざまなタイプのミスを犯す確率を理解することができる。

There are two types of mistakes we can make in acting on test results.
テスト結果に基づいて行動する際に犯しうる過ちには2種類ある。
A false positive (also called a Type I error) occurs when the data from the test indicates a meaningful difference between the control and treatment experiences, but in truth there is no difference.
偽陽性（タイプIエラーとも呼ばれる）は、テストから得られたデータが、コントロールとトリートメントの経験の間に意味のある違いを示しているが、実際には違いがない場合に起こる。
This scenario is like having a medical test come back as positive for a disease when you are healthy.
このシナリオは、健康なのに医療検査で病気が陽性と出るようなものだ。
The other error we can make in deciding on a test is a false negative (also called a Type II error), which occurs when the data do not indicate a meaningful difference between treatment and control, but in truth there is a difference.
これは、データが処置とコントロールの間に意味のある差を示さないが、本当は差がある場合に起こる。
This scenario is like having a medical test come back negative — when you do indeed have the disease you are being tested for.
このシナリオは、医療検査で陰性と判定されるようなものである。

As another way to build intuition, consider the real reason that the internet and machine learning exist: to label if images show cats.
直感を養うもうひとつの方法として、インターネットと機械学習が存在する本当の理由を考えてみよう： インターネットや機械学習が存在する本当の理由を考えてみよう。
For a given image, there are two possible decisions (apply the label “cat” or “not cat”), and likewise there are two possible truths (the image either features a cat or it does not).
ある画像に対して、2つの可能な決定（「猫」というラベルを貼るか、「猫ではない」というラベルを貼るか）があり、同様に2つの可能な真実（画像には猫がいるか、いないか）がある。
This leads to a total of four possible outcomes, shown in Figure 1.
その結果、図1に示すように、合計4つの結果が考えられる。
The same is true with A/B tests: we make one of two decisions based on the data (“sufficient evidence to conclude that the Top 10 list affects member satisfaction” or “insufficient evidence”), and there are two possible truths, that we never get to know with complete uncertainty (“Top 10 list truly affects member satisfaction” or “it does not”).
A/Bテストでも同じことが言える： A/Bテストも同じで、データに基づいて2つの判断（「トップ10リストが会員の満足度に影響すると結論づけるのに十分な証拠」または「不十分な証拠」）のいずれかを下し、2つの可能性のある真実（「トップ10リストが本当に会員の満足度に影響する」または「影響しない」）がありますが、完全な不確実性をもって知ることはできません。

The uncomfortable truth about false positives and false negatives is that we can’t make them both go away.
偽陽性と偽陰性についての不快な真実は、私たちはその両方を消し去ることはできないということだ。
In fact, they trade off with one another.
実際、互いにトレードオフの関係にある。
Designing experiments so that the rate of false positives is minuscule necessarily increases the false negative rate, and vice versa.
偽陽性の割合が極小になるように実験をデザインすると、必然的に偽陰性の割合が高くなる。
In practice, we aim to quantify, understand, and control these two sources of error.
実際には、この2つのエラーの原因を定量化し、理解し、コントロールすることを目指している。

In the remainder of this post, we’ll use simple examples to build up intuition around false positives and related statistical concepts; in the next post in this series, we’ll do the same for false negatives.
この記事の残りの部分では、偽陽性と関連する統計的概念について直感を養うために簡単な例を使用します。

## False positives and statistical significance 偽陽性と統計的有意性

With a great hypothesis and a clear understanding of the primary decision metric, it’s time to turn to the statistical aspects of designing an A/B test.
優れた仮説と主要な意思決定指標の明確な理解があれば、A/Bテストを設計するための統計的側面に目を向ける時が来た。
This process generally starts by fixing the acceptable false positive rate.
このプロセスは通常、許容可能な偽陽性率を修正することから始まる。
By convention, this false positive rate is usually set to 5%: for tests where there is not a meaningful difference between treatment and control, we’ll falsely conclude that there is a “statistically significant” difference 5% of the time.
慣例では、この偽陽性率は通常5%に設定される： 治療とコントロールの間に意味のある差がないテストでは、5％の確率で「統計的に有意な」差があると誤って結論づけることになる。
Tests that are conducted with this 5% false positive rate are said to be run at the 5% significance level.
この5％の偽陽性率で実施される検定は、5％の有意水準で実施されるという。

Using the 5% significance level convention can feel uncomfortable.
有意水準5％の慣例を使うと、違和感を覚えることがある。
By following this convention, we are accepting that, in instances when the treatment and control experience are not meaningfully different for our members, we’ll make a mistake 5% of the time.
この慣例に従うことで、メンバーにとって治療と対照の経験に意味のある違いがない場合、我々は5％の確率で間違いを犯すことを受け入れることになる。
We’ll label 5% of the non-cat photos as displaying cats.
猫以外の写真の5％を猫が写っている写真とする。

The false positive rate is closely associated with the “statistical significance” of the observed difference in metric values between the treatment and control groups, which we measure using the p-value.
偽陽性率は、治療群と対照群の間で観測された指標値の差の "統計的有意性 "と密接に関連しており、p値を用いて測定する。
The p-value is the probability of seeing an outcome at least as extreme as our A/B test result, had there truly been no difference between the treatment and control experiences.
p値は、A/Bテストの結果と少なくとも同じ極端な結果が出る確率である。
An intuitive way to understand statistical significance and p-values, which have been confusing students of statistics for over a century (your authors included!), is in terms of simple games of chance where we can calculate and visualize all the relevant probabilities.
統計の有意性とp値を理解する直感的な方法は、1世紀以上にわたって統計学の学生を混乱させてきた（あなたの著者も含めて！）。

Say we want to know if a coin is unfair, in the sense that the probability of heads is not 0.5 (or 50%).
コインの表が出る確率が0.5（または50％）ではないという意味で、コインが不公平かどうかを知りたいとする。
It may sound like a simple scenario, but it is directly relevant to many businesses, Netflix included, where the goal is to understand if a new product experience results in a different rate for some binary user activity, from clicking on a UI feature to retaining the Netflix service for another month.
単純なシナリオのように聞こえるかもしれないが、これはネットフリックスを含む多くのビジネスに直接関係するものであり、新しい製品体験が、UI機能のクリックからネットフリックスのサービスをもう1ヶ月継続するまでの二律背反的なユーザー活動において、異なるレートをもたらすかどうかを理解することを目標としている。
So any intuition we can build through simple games with coins maps directly to interpreting A/B tests.
つまり、コインを使った簡単なゲームを通じて構築できる直感は、そのままA/Bテストの解釈につながるのだ。

To decide if the coin is unfair, let’s run the following experiment: we’ll flip the coin 100 times and calculate the fraction of outcomes that are heads.
コインが不公平かどうかを判断するために、次のような実験をしてみよう： コインを100回ひっくり返して、表が出た割合を計算する。
Because of randomness, or “noise,” even if the coin were perfectly fair we wouldn’t expect exactly 50 heads and 50 tails — but how much of a deviation from 50 is “too much”? When do we have sufficient evidence to reject the baseline assertion that the coin is in fact fair? Would you be willing to conclude that the coin is unfair if 60 out of 100 flips were heads? 70? We need a way to align on a decision framework and understand the associated false positive rate.
ランダム性、つまり「ノイズ」のせいで、たとえコインが完全に公平であったとしても、正確に50枚の表と50枚の裏を期待することはできない。コインが実際に公正であるという基本的な主張を否定するのに十分な証拠はいつ得られるのでしょうか？コインを100回ひっくり返して60回が表だったら、そのコインは不公平だと結論づけられますか？70? 判断の枠組みを揃え、関連する偽陽性率を理解する方法が必要だ。

To build intuition, let’s run through a thought exercise.
直感を養うために、思考の練習をしてみよう。
First, we’ll assume the coin is fair — this is our “null hypothesis,” which is always a statement of status quo or equality.
まず、コインは公平であると仮定する。これは「帰無仮説」であり、常に現状維持または平等であることを表明するものである。
We then seek compelling evidence against this null hypothesis from the data.
そして、この帰無仮説に対する有力な証拠をデータから探し出す。
To make a decision on what constitutes compelling evidence, we calculate the probability of every possible outcome, assuming that the null hypothesis is true.
何が有力な証拠となるかを判断するために、帰無仮説が真であると仮定して、あらゆる可能性のある結果の確率を計算する。
For the coin flipping example, that’s the probability of 100 flips yielding zero heads, one head, two heads, and so forth up to 100 heads — assuming that the coin is fair.
コインを裏返す例で言えば、コインを100回裏返したときに、0個の表が出る確率、1個の表が出る確率、2個の表が出る確率......というように、100個の表が出る確率である。
Skipping over the math, each of these possible outcomes and their associated probabilities are shown with the black and blue bars in Figure 3 (ignore the colors for now).
計算を飛ばして、これらの可能性のある各結果とそれに関連する確率を図3の黒と青の棒で示す（今は色は無視する）。

We can then compare this probability distribution of outcomes, calculated under the assumption that the coin is fair, to the data we’ve collected.
そして、コインが公平であるという仮定の下で計算されたこの結果の確率分布を、私たちが収集したデータと比較することができる。
Say we observe that 55% of 100 flips are heads (the solid red line in Figure 3).
100回のフリップのうち55％がヘッドであることを観察したとしよう（図3の赤い実線）。
To quantify if this observation is compelling evidence that the coin is not fair, we count up the probabilities associated with every outcome that is less likely than our observation.
この観察が、コインが公正でないことの有力な証拠であるかどうかを定量化するために、観察よりも可能性の低いすべての結果に関連する確率を数え上げる。
Here, because we’ve made no assumptions about heads or tails being more likely, we sum up the probabilities of 55% or more of the flips coming up heads (the bars to the right of the solid red line) and the probabilities of 55% or more of the flips coming up tails (the bars to the left of the dashed red line).
ここでは、ヘッドとテールのどちらが確率が高いかについては仮定していないので、55％以上がヘッドになる確率（赤い実線の右側の棒グラフ）と55％以上がテールになる確率（赤い破線の左側の棒グラフ）を合計している。

This is the mythical p-value: the probability of seeing a result as extreme as our observation, if the null hypothesis were true.
これが神話上のp値である： 帰無仮説が真であった場合に、観察結果と同じような極端な結果が出る確率。
In our case, the null hypothesis is that the coin is fair, the observation is 55% heads in 100 flips, and the p-value is about 0.32.
この場合、帰無仮説は「コインは公平である」、観測値は100回ひっくり返して55％が表、p値は約0.32である。
The interpretation is as follows: were we to repeat, many times, the experiment of flipping a coin 100 times and calculating the fraction of heads, with a fair coin (the null hypothesis is true), in 32% of those experiments the outcome would feature at least 55% heads or at least 55% tails (results at least as unlikely as our actual observation).
解釈は以下の通りである： 公正なコイン（帰無仮説が真）を使って、コインを100回ひっくり返して表が出た割合を計算する実験を何度も繰り返した場合、そのうちの32％の結果で、少なくとも55％の表か少なくとも55％の裏が出たことになる（実際の観察結果と同じくらいあり得ない結果）。

How do we use the p-value to decide if there is statistically significant evidence that the coin is unfair — or that our new product experience is an improvement on the status quo? It comes back to that 5% false positive rate that we agreed to accept at the beginning: we conclude that there is a statistically significant effect if the p-value is less than 0.05.
コインが不公平であるという統計的に有意な証拠があるかどうか、あるいは私たちの新しい製品体験が現状より改善されているかどうかを判断するのに、p値をどのように使えばいいのだろうか？それは、最初に受け入れることに同意した5％の偽陽性率に戻る： p値が0.05より小さければ、統計的に有意な効果があると結論づける。
This formalizes the intuition that we should reject the null hypothesis that the coin is fair if our result is sufficiently unlikely to occur under the assumption of a fair coin.
これは、公正なコインを仮定した場合、その結果が十分に起こりにくいのであれば、コインは公正であるという帰無仮説を棄却すべきであるという直観を形式化したものである。
In the example of observing 55 heads in 100 coin flips, we calculated a p-value of 0.32.
コインを100回ひっくり返して55個の頭を観察した例では、p値は0.32と計算された。
Because the p-value is larger than the 0.05 significance level, we conclude that there is not statistically significant evidence that the coin is unfair.
p値は有意水準0.05より大きいので、コインが不公平であるという統計的に有意な証拠はないと結論づけられる。

There are two conclusions that we can make from an experiment or A/B test: we either conclude there is an effect (“the coin is unfair”, “the Top 10 feature increases member satisfaction”) or we conclude that there is insufficient evidence to conclude there is an effect (“cannot conclude the coin is unfair,” “cannot conclude that the Top 10 row increases member satisfaction”).
実験やA/Bテストから得られる結論は2つある： すなわち、効果があると結論づけるか（「コインは不公平である」、「トップ10の機能はメンバーの満足度を高める」）、効果があると結論づけるには証拠が不十分であると結論づけるか（「コインは不公平であると結論づけることはできない」、「トップ10の行はメンバーの満足度を高めると結論づけることはできない」）。
It’s a lot like a jury trial, where the two possible outcomes are “guilty” or “not guilty” — and “not guilty” is very different from “innocent.” Likewise, this (frequentist) approach to A/B testing does not allow us to make the conclusion that there is no effect — we never conclude the coin is fair, or that the new product feature has no impact on our members.
これは陪審裁判のようなもので、起こりうる結果は "有罪 "か "無罪 "の2つであり、"無罪 "は "無実 "とは全く異なる。同様に、A/Bテストに対するこの（頻度論的な）アプローチでは、「効果がない」という結論を出すことはできない。コインは公平であるとか、新商品の機能は会員に何の影響も与えないと結論づけることはない。
We just conclude we’ve not collected enough evidence to reject the null assumption that there is no difference.
差がないという帰無仮説を棄却するのに十分な証拠を集めていないと結論づけるだけだ。
In the coin example above, we observed 55% heads in 100 flips, and concluded we had insufficient evidence to label the coin as unfair.
上のコインの例では、100回ひっくり返して55％の表が出た。
Critically, we did not conclude that the coin was fair — after all, if we gathered more evidence, say by flipping that same coin 1000 times, we might find sufficiently compelling evidence to reject the null hypothesis of fairness.
もっと証拠を集めれば、たとえば同じコインを1000回ひっくり返せば、公正であるという帰無仮説を棄却する十分説得力のある証拠が見つかるかもしれない。

## ​​Rejection Regions and Confidence Intervals 

There are two other concepts in A/B testing that are closely related to p-values: the rejection region for a test, and the confidence interval for an observation.
A/Bテストには、p値に密接に関係する他の2つの概念がある： 検定の棄却域とオブザベーションの信頼区間である．
We cover them both in this section, building on the coin example from above.
このセクションでは、上記のコインの例を基に、この2つを取り上げる。

Rejection Regions.
拒絶領域。
Another way to build a decision rule for a test is in terms of what’s called a “rejection region” — the set of values for which we’d conclude that the coin is unfair.
テストの判定ルールを作るもう一つの方法は、「棄却領域」と呼ばれるもの、つまりコインが不公平であると結論づける値の集合という観点である。
To calculate the rejection region, we once more assume the null hypothesis is true (the coin is fair), and then define the rejection region as the set of least likely outcomes with probabilities that sum to no more than 0.05.
棄却域を計算するには、もう一度帰無仮説が真（コインは公平）であると仮定し、確率の合計が0.05以下になる可能性が最も低い結果の集合を棄却域と定義する。
The rejection region consists of the outcomes that are the most extreme, provided the null hypothesis is correct — the outcomes where the evidence against the null hypothesis is strongest.
棄却域は、帰無仮説が正しい場合に最も極端な結果、つまり帰無仮説に対する証拠が最も強い結果で構成される。
If an observation falls in the rejection region, we conclude that there is statistically significant evidence that the coin is not fair, and “reject” the null.
もし観察値が棄却域に入れば、コインは公平ではないという統計的に有意な証拠があると結論づけ、帰無値を「棄却」する。
In the case of the simple coin experiment, the rejection region corresponds to observing fewer than 40% or more than 60% heads (shown with blue shaded bars in Figure 3).
単純なコイン実験の場合、棄却領域は、40％未満または60％以上のヘッドを観察した場合に相当する（図3の青い網掛けバーで示す）。
We call the boundaries of the rejection region, here 40% and 60% heads, the critical values of the test.
棄却領域の境界、ここでは40％ヘッドと60％ヘッドをテストの臨界値と呼ぶ。

There is an equivalence between the rejection region and the p-value, and both lead to the same decision: the p-value is less than 0.05 if and only if the observation lies in the rejection region.
棄却域とp値の間には等価性があり、両方とも同じ決定を導く： オブザベーションが棄却域にある場合のみ，p-値は0.05より小さい．

Confidence Intervals.
信頼区間。
So far, we’ve approached building a decision rule by first starting with the null hypothesis, which is always a statement of no change or equivalence (“the coin is fair” or “the product innovation does not impact member satisfaction”).
これまでは、まず帰無仮説（「コインは公平である」または「製品の革新は会員の満足度に影響を与えない」）から始めることで、決定ルールの構築に取り組んできた。
We then define possible outcomes under this null hypothesis and compare our observation to that distribution.
次に、この帰無仮説のもとで起こりうる結果を定義し、我々の観測結果をその分布と比較する。
To understand confidence intervals, it helps to flip the problem around to focus on the observation.
信頼区間を理解するためには、問題を反転させて観察に焦点を当てることが役立つ。
We then go through a thought exercise: given the observation, what values of the null hypothesis would lead to a decision not to reject, assuming we specify a 5% false positive rate? For our coin flipping example, the observation is 55% heads in 100 flips and we do not reject the null of a fair coin.
次に思考練習をする： 観察結果が与えられたとき、5%の偽陽性率を仮定して、帰無仮説はどのような値なら棄却しないことになるでしょうか？コインを裏返す例では、観察結果は100回ひっくり返して55%が表で、公正なコインという帰無仮説は棄却されません。
Nor would we reject the null hypothesis that the probability of heads was 47.5%, 50%, or 60%.
また、ヘッドの確率が47.5％、50％、60％であるという帰無仮説を棄却することもない。
There’s a whole range of values for which we would not reject the null, from about 45% to 65% probability of heads (Figure 4).
帰無値が棄却されない値には、約45％から65％の確率で頭が出るまでの全範囲がある（図4）。

This range of values is a confidence interval: the set of values under the null hypothesis that would not result in a rejection, given the data from the test.
この値の範囲が信頼区間である： 帰無仮説の下で、検定から得られたデータがあれば、棄却とならない値の集合。
Because we’ve mapped out the interval using tests at the 5% significance level, we’ve created a 95% confidence interval.
有意水準5％の検定を使って区間をマッピングしたので、95％の信頼区間ができた。
The interpretation is that, under repeated experiments, the confidence intervals will cover the true value (here, the actual probability of heads) 95% of the time.
実験を繰り返せば、信頼区間は95％の確率で真の値（ここでは実際のヘッドの確率）をカバーするという解釈である。

There is an equivalence between the confidence interval and the p-value, and both lead to the same decision: the 95% confidence interval does not cover the null value if and only if the p-value is less than 0.05, and in both cases we reject the null hypothesis of no effect.
信頼区間とp値には等価性があり、どちらも同じ決定を導く： 95%信頼区間が帰無値をカバーしないのは、p値が0.05より小さい場合だけであり、どちらの場合も効果なしという帰無仮説を棄却する。

## Summary 要約

Using a series of thought exercises based on flipping coins, we’ve built up intuition about false positives, statistical significance and p-values, rejection regions, confidence intervals, and the two decisions we can make based on test data.
コインをはじくことに基づいた一連の思考訓練を使って、偽陽性、統計的有意性、p値、棄却域、信頼区間、テストデータに基づいて下すことのできる2つの判断について直感を積み上げてきた。
These core concepts and intuition map directly to comparing treatment and control experiences in an A/B test.
これらの核となる概念と直観は、A/Bテストにおけるトリートメントとコントロールの経験の比較に直接マッピングされる。
We define a “null hypothesis” of no difference: the “B” experience does not alter affect member satisfaction.
差がないという「帰無仮説」を定義する： B "の経験は、メンバーの満足度に影響を与えない。
We then play the same thought experiment: what are the possible outcomes and their associated probabilities for the difference in metric values between the treatment and control groups, assuming there is no difference in member satisfaction? We can then compare the observation from the experiment to this distribution, just like with the coin example, calculate a p-value and make a conclusion about the test.
次に、同じ思考実験を行う： 会員の満足度に差がないと仮定した場合、治療群と対照群の間の指標値の差について、起こりうる結果とそれに関連する確率は何であろうか？そして、コインの例と同じように、実験から得られたオブザベーションをこの分布と比較し、p値を計算し、検定に関する結論を出します。
And just like with the coin example, we can define rejection regions and calculate confidence intervals.
そして、コインの例と同じように、棄却域を定義し、信頼区間を計算することができる。

But false positives are only of the two mistakes we can make when acting on test results.
しかし、偽陽性は、検査結果に基づいて行動する際に犯しうる2つの過ちのうちの1つでしかない。
In the next post in this series, we’ll cover the other type of mistake, false negatives, and the closely related concept of statistical power.
このシリーズの次の記事では、もう一つのタイプの誤りである偽陰性と、それに密接に関連する統計的検出力という概念について取り上げる。
Follow the Netflix Tech Blog to stay up to date.
最新情報はNetflix Tech Blogをフォローしてください。
Part 4 is now available.
パート4が公開された。