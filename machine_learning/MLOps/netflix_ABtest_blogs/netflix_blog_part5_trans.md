## 0.1. link リンク

https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8
https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8

# 1. Building confidence in a decision

決断への自信を深める

This is the fifth post in a multi-part series on how Netflix uses A/B tests to inform decisions and continuously innovate on our products.
この記事は、NetflixがどのようにA/Bテストを使用して意思決定を行い、継続的に製品を革新しているかについて、複数回に分けてご紹介するシリーズの第5回目です。
Need to catch up? Have a look at Part 1 (Decision Making at Netflix), Part 2 (What is an A/B Test?), Part 3 (False positives and statistical significance), and Part 4 (False negatives and power).
追いつく必要がありますか？パート1（Netflixにおける意思決定）、パート2（A/Bテストとは）、パート3（偽陽性と統計的有意性）、パート4（偽陰性と検出力）をご覧ください。
Subsequent posts will go into more details on experimentation across Netflix, how Netflix has invested in infrastructure to support and scale experimentation, and the importance of developing a culture of experimentation within an organization.
次回の記事では、Netflixにおける実験の詳細、Netflixが実験をサポートし拡大するためにどのようにインフラに投資してきたか、組織内で実験文化を発展させることの重要性について述べる。

In Parts 3 (False positives and statistical significance) and 4 (False negatives and power), we discussed the core statistical concepts that underpin A/B tests: false positives, statistical significance and p-values, as well as false negatives and power.
第3部（偽陽性と統計的有意性）と第4部（偽陰性と検出力）では、**A/Bテストを支える中核となる統計的概念について**説明した： 偽陽性、統計的有意性、p値、そして偽陰性と検出力である。
Here, we’ll get to the hard part: how do we use test results to support decision making in a complex business environment?
ここで、難しい話に入ろう： **複雑なビジネス環境における意思決定をサポートするために、テスト結果をどのように利用するか**？

The unpleasant reality about A/B testing is that no test result is a certain reflection of the underlying truth.
A/Bテストに関する不愉快な現実は、どんなテスト結果も根本的な真実を確実に反映するものではないということだ。
As we discussed in previous posts, good practice involves first setting and understanding the false positive rate, and then designing an experiment that is well powered so it is likely to detect true effects of reasonable and meaningful magnitudes.
以前の記事で説明したように、良い実践には、**まず偽陽性率を設定し理解すること**、そして、**妥当で意味のある大きさの真の効果を検出できるよう、十分な検出力を持つ実験を計画すること**が必要である。
These concepts from statistics help us reduce and understand error rates and make good decisions in the face of uncertainty.
統計学のこれらの概念は、私たちがエラー率を減らし、理解し、不確実性に直面して適切な意思決定をするのに役立ちます。
But there is still no way to know whether the result of a specific experiment is a false positive or a false negative.
しかし、特定の実験結果が偽陽性なのか偽陰性なのかを知る方法はまだない。

![figure 1: Figure 1: Inspiration from Voltaire.]()
doubt is not a pleasant condition, but certainty is absurd. ― Voltaire
疑いは快適な状態ではないが、確信は不合理である。 ― ヴォルテール

In using A/B testing to evolve the Netflix member experience, we’ve found it critical to look beyond just the numbers, including the p-value, and to interpret results with strong and sensible judgment to decide if there’s compelling evidence that a new experience is a “win” for our members.
ネットフリックスの会員体験を進化させるためにA/Bテストを活用する際、**p値を含む数字だけにとらわれず**、強く賢明な判断で結果を解釈し、新しい体験が会員にとって「勝利」であるという説得力のある証拠があるかどうかを判断することが重要だとわかりました。
These considerations are aligned with the American Statistical Association’s 2016 Statement on Statistical Significance and P-Values, where the following three direct quotes (bolded) all inform our experimentation practice.
これらの考慮事項は、米国統計協会の「統計的有意性とP値に関する2016年の声明」に沿ったものであり、以下の**3つの直接引用（太字）**はすべて我々の実験実践に役立つものである。

> “Proper inference requires full reporting and transparency.”
> (適切な推論には完全な報告と透明性が必要)

As discussed in Part 3: (False positives and statistical significance), by convention we run experiments at a 5% false positive rate.
パート3： 偽陽性と統計的有意性）で述べたように、**慣例として我々は5％の偽陽性率で実験を行う**。
In practice, then, if we run twenty experiments (say to evaluate if each of twenty colors of jelly beans are linked to acne) we’d expect at least one significant result — even if, in truth, the null hypothesis is true in each case and there is no actual effect.
実際には、20の実験（例えば、20の色のゼリービーンがにきびに関連しているかどうかを評価するため）を実行すると、少なくとも1つの有意な結果が得られると予想される。たとえ真実であっても、帰無仮説が各ケースで真実であり、実際の効果がないとしても。(20回に1回は偽陽性を検出する想定...!)
This is the Multiple Comparisons Problem, and there are a number of approaches to controlling the overall false positive rate that we’ll not cover here.
これは「多重比較問題」であり、全体的な偽陽性率をコントロールするための多くのアプローチがあるが、ここでは取り上げない。
Of primary importance, though, is to report and track not only results from tests that yield significant results — but also those that do not.
しかし、第一に重要なのは、重要な結果をもたらしたテストだけでなく、そうでないテストの結果も報告し、追跡することである。

![figure 2: All you need to know about false positives, in cartoon form.]()

> “A p-value, or statistical significance, does not measure the size of an effect or the importance of a result.”
> "p値（統計的有意性）は、効果の大きさや結果の重要性を測るものではない"

In Part 4 (False negatives and power), we talked about the importance, in the experimental design phase, of powering A/B tests to have a high probability of detecting reasonable and meaningful metric movements.
パート4（偽陰性と検出力）では、実験デザインの段階で、**妥当で意味のある指標の動きを高い確率で検出できるようにA/Bテストに検出力をつけることの重要性**についてお話しました。
Similar considerations are relevant when interpreting results.
結果を解釈する際にも、同様の考慮が必要である。
Even if results are statistically significant (p-value < 0.05), the estimated metric movements may be so small that they are immaterial to the Netflix member experience, and we are better off investing our innovation efforts in other areas.
結果が統計的に有意 (p値＜0.05) であったとしても、推定された指標の動きは、ネットフリックスの会員体験にとって重要でないほど小さい可能性があり、イノベーションの努力を他の分野に投資した方がよい。(ex. サンプルサイズが大き過ぎたらp値は低くでやすい。-> この状態は、無意味なほど小さい差について、検出力が高くなってる)
Or the costs of scaling out a new feature may be so high relative to the benefits that we could better serve our members by not rolling out the feature and investing those funds in improving different areas of the product experience.
あるいは、新機能をスケールアウトするためのコストが、利点に比して非常に高く、その機能を展開せず、その資金を製品体験の別の分野の改善に投資した方が、会員により良いサービスを提供できるかもしれない。

> “Scientific conclusions and business or policy decisions should not be based only on whether a p-value passes a specific threshold.”
> "科学的な結論やビジネスや政策の決定は、p値が特定の閾値を超えたかどうかだけに基づくべきではありません。"

The remainder of this post gives insights into practices we use at Netflix to arrive at decisions, focusing on how we holistically evaluate evidence from an A/B test.
この記事の残りの部分では、Netflixで意思決定に至るために使っているプラクティスについて、**A/Bテストから得られたエビデンスをどのように総合的に評価するか**に焦点を当てながら、洞察を述べる。

## 1.1. Building a data-driven case データに基づくケースの構築

One practical way to evaluate the evidence in support of a decision is to think in terms of constructing a legal case in favor of the new product experience:
決定を支持する証拠を評価する実際的な方法のひとつは、新商品体験に有利な法的事例を構築するという観点から考えることである:
is there enough evidence to “convict” and conclude, beyond that 5% reasonable doubt, that there is a true effect that benefits our members?
5％の合理的な疑いを超えて、会員に利益をもたらす真の効果があると結論づけるために、十分な証拠があるか？
To help build that case, here are some helpful questions that we ask ourselves in interpreting test results:
そのケースを構築するのに役立つために、**テスト結果を解釈する際に自問するいくつかの質問**を紹介する。

### 1.1.1. Do the results align with the hypothesis?結果は仮説と一致しているか？

If the hypothesis was about optimizing compute resources for back-end infrastructure, and results showed a major and statistically significant increase in user satisfaction, we’d be skeptical.
仮説がバックエンドインフラストラクチャのコンピューティングリソースの最適化についてであり、結果がユーザ満足度の大幅な統計的に有意な増加を示していた場合、私たちは懐疑的になるだろう。
The result may be a false positive — or, more than likely, the result of a bug or error in the execution of the experiment (Twyman’s Law).
その結果は偽陽性かもしれないし、実験実行中のバグやエラーの結果かもしれない(ツイマンの法則)。
Sometimes surprising results are correct, but more often than not they are either the result of implementation errors or false positives, motivating us to dig deep into the data to identify root causes.
意外な結果が正しいこともあるが、多くの場合、実装ミスか偽陽性の結果であり、根本原因を特定するためにデータを深く掘り下げる動機となる。

### 1.1.2. Does the metric story hang together? メトリクスストーリーはまとまっているか？

In Part 2 (What is an A/B Test?), we talked about the importance of describing the causal mechanism through which a change made to the product impacts both secondary metrics and the primary decision metric specified for the test.
パート2（A/Bテストとは何か）では、製品に加えられた変更が、secondary metricsとテストで指定されたprimary decision metricの両方にどのように影響を与えるかという**因果関係のメカニズムを記述することの重要性**について説明しました。
In evaluating test results, it’s important to look at changes in these secondary metrics, which are often specific to a particular experiment, to assess if any changes in the primary metric follow the hypothesized causal chain.
テスト結果を評価する際には、このような**secondary metricsの変化を見ることが重要**であり、これらはしばしば特定の実験に特有のものであり、**primary metricの変化が仮説に基づいた因果関係の連鎖に従っているかどうかを評価することが重要**である。
With the Top 10 experiment, for example, we’d check if inclusion in the Top 10 list increases title-level engagement, and if members are finding more of the titles they watch from the home page versus other areas of the product.
例えば、「トップ10」の実験では、「トップ10」リストへの掲載がタイトルレベルのエンゲージメントを高めるかどうか、また、会員が視聴するタイトルをトップページから探す場合と他のエリアから探す場合を比較します。
Increased engagement with the Top 10 titles and more plays coming from the home page would help build our confidence that it is in fact the Top 10 list that is increasing overall member satisfaction.
トップ10タイトルへのengagementの増加と、ホームページからの再生数の増加は、実際にはトップ10リストが全体的な会員満足度を高めていることを確信するのに役立つだろう。
In contrast, if our primary member satisfaction metric was up in the Top 10 treatment group, but analysis of these secondary metrics showed no increase in engagement with titles included in the Top 10 list, we’d be skeptical.
対照的に、主要な会員満足度指標がトップ10の治療群で上昇していたとしても、これらのsecondary metricsの分析で、トップ10リストに含まれるタイトルへのエンゲージメントが増加していないことがわかれば、私たちは懐疑的になるだろう。
Maybe the Top 10 list isn’t a great experience for our members, and its presence drives more members off the home page, increasing engagement with the Netflix search experience — which is so amazing that the result is an increase in overall satisfaction.
もしかしたら、トップ10リストは会員にとって素晴らしい体験ではないかもしれない。その存在によって、より多くの会員がホームページから離れ、ネットフリックスの検索体験へのエンゲージメントが高まる。
Or maybe it’s a false positive.
あるいは偽陽性かもしれない。
In any case, movements in secondary metrics can cast sufficient doubt that, despite movement in the primary decision metric, we are unable to confidently conclude that the treatment is activating the hypothesized causal mechanism.
いずれにせよ、secondary metricsの動きは、primary decision metricの動きにもかかわらず、treatmentが仮説に基づいた因果関係のメカニズムを活性化していると確信できないほど十分な疑いを投げかけることができる。

### 1.1.3. Is there additional supporting or refuting evidence, such as consistent patterns across similar variants of an experience?

ある経験の類似したバリエーションに一貫したパターンがあるなど、追加的な裏付けや反証はあるか？

It’s common to test a number of variants of an idea within a single experiment.
**一つの実験において、アイデアのいくつかのvariantをテストすることは一般的**である。(2つとか3つとか)
For example, with something like the Top 10 experience, we may test a number of design variants and a number of different ways to position the Top 10 row on the homepage.
例えば、トップ10エクスペリエンスのようなものでは、デザインのバリエーションや、トップ10の行をホームページに配置するさまざまな方法をテストすることがある。
If the Top 10 experience is great for Netflix members, we’d expect to see similar gains in both primary and secondary metrics across many of these variants.
Netflixの会員にとってTop10の体験が素晴らしいものであれば、これらのvariantの多くで一次指標と二次指標の両方で同様の向上が見られると予想される。
Some designs may be better than others, but seeing broadly consistent results across the variants helps build that case in favor of the Top 10 experience.
いくつかのデザインは他のデザインよりも優れているかもしれないが、**バリエーション全体にわたって広く一貫した結果を見ること**は、トップ10の経験を支持するケースを構築するのに役立つ。
If, on the other hand, we test 20 design and positioning variants and only one yields a significant movement in the primary decision metric, we’d be much more skeptical.
一方、20のデザインとポジショニングのバリエーションをテストして、primary decision metricで有意な動きを示すのは1つだけであれば、私たちはより懐疑的になるだろう。(本当に施策が有効なら、20個のうちの1つだけでなく、複数のバリエーションで段階的な変化が見られるはず)
After all, with that 5% false positive rate, we expect on average one significant result from random chance alone.
結局のところ、5％の偽陽性率があれば、無作為の偶然だけで平均して1つの有意な結果が得られると予想される。

### 1.1.4. Do results repeat? 結果は繰り返されるか？

Finally, the surest way to build confidence in a result is to see if results repeat in a follow-up test.
最後に、結果に自信を持つための最も確実な方法は、フォローアップテストで結果が繰り返されるかどうかを確認することである。
If results of an initial A/B test are suggestive but not conclusive, we’ll often run a follow-up test that hones in on the hypothesis based on learnings generated from the first test.
**最初のA/Bテストの結果が示唆的ではあっても決定的でない場合、私たちはしばしば、最初のテストから得られた学習に基づいて仮説に磨きをかけるフォローアップテストを実施**します。
With something like the Top 10 test, for example, we might observe that certain design and row positioning choices generally lead to positive metric movements, some of which are statistically significant.
例えば、トップ10テストのようなものであれば、ある種のデザインや列の配置を選択することで、一般的にポジティブな指標の動きにつながり、そのうちのいくつかは統計的に有意であることが観察されるかもしれない。
We’d then refine these most promising design and positioning variants, and run a new test.
そして、**最も有望なデザインとポジショニングのバリエーションを改良し、新たなテストを実施する**。
With fewer experiences to test, we can also increase the allocation size to gain more power.
テストする経験が少なければ、**より大きなpowerを得るために割り当てサイズを大きくすることもできる**。
Another strategy, useful when the product changes are large, is to gradually roll out the winning treatment experience to the entire user or member based to confirm benefits seen in the A/B test, and to ensure there are no unexpected deleterious impacts.
製品の変更が大規模な場合に有効なもう一つの戦略は、A/Bテストで見られた利点を確認し、予期せぬ悪影響がないことを確認するために、勝利したtreatment experienceをユーザ全体またはメンバー全体に徐々に展開することである。(割合を徐々に増やしていくやつ。でも今回の動機は、示唆はあるが確信が持てないからか...!)
In this case, instead of rolling out the new experience to all users at once, we slowly ramp up the fraction of members receiving the new experience, and observe differences with respect to those still receiving the old experience.
この場合、新しいエクスペリエンスをすべてのユーザに一度に展開するのではなく、新しいエクスペリエンスを受けるメンバーの割合を徐々に増やし、古いエクスペリエンスをまだ受けているメンバーとの違いを観察する。

## 1.2. Connections with decision theory 意思決定理論との関連

In practice, each person has a different framework for interpreting the results of a test and making a decision.
実際には、各個人は、テストの結果を解釈し、意思決定をするための異なる枠組みを持っている。
Beyond the data, each individual brings, often implicitly, prior information based on their previous experiences with similar A/B tests, as well as a loss or utility function based on their assessment of the potential benefits and consequences of their decision.
データを超えて、各個人は、しばしば暗黙的に、類似のA/Bテストに基づく以前の経験に基づく事前情報を持ち、また、自分の意思決定の潜在的な利益と結果の評価に基づく損失または効用関数を持っている。
There are ways to formalize these human judgements about estimated risks and benefits using [decision theory](https://en.wikipedia.org/wiki/Expected_utility_hypothesis), including [Bayesian decision theory](https://en.wikipedia.org/wiki/Bayes_estimator).
ベイズ決定理論などの決定理論を用いて、推定されるリスクと便益に関する人間の判断を形式化する方法がある。(これはベイジアンABテストの話??)
These approaches involve formally estimating the utility of making correct or incorrect decisions (e.g., the cost of rolling out a code change that doesn’t improve the member experience).
これらのアプローチでは、正しい決定または誤った決定（例えば、会員体験を改善しないコード変更を展開するコスト）を行うことの効用を正式に見積もることが含まれる。
If, at the end of the experiment, we can also estimate the probability of making each type of mistake for each treatment group, we can make a decision that maximizes the expected utility for our members.
実験終了時に、各treatment群で各typeの間違い(=type 1とtype 2のerrorの話か...!)をする確率を推定することができれば、会員の期待効用を最大化する意思決定をすることができる。

Decision theory couples statistical results with decision-making and is therefore a compelling alternative to p-value-based approaches to decision making.
**意思決定理論は統計的結果と意思決定を結びつけるもの**であり、したがって、**意思決定に対するp値ベースのアプローチに代わる説得力のあるもの**である。
However, decision-theoretic approaches can be difficult to generalize across a broad range of experiment applications, due to the nuances of specifying utility functions.
しかし、意思決定理論的なアプローチは、効用関数を特定する際の微妙なニュアンスのため、広範な実験アプリケーションにわたって一般化することが難しい場合がある。
Although imperfect, the [frequentist](https://en.wikipedia.org/wiki/Frequentist_inference) approach to hypothesis testing that we’ve outlined in this series, with its focus on p-values and statistical significance, is a broadly and readily applicable framework for interpreting test results.
不完全ではあるが、このシリーズで概説した仮説検定に対する頻度論的アプローチは、p値と統計的有意性に焦点を当てたものであり、検定結果を解釈するための広範かつ容易に適用できる枠組みである。
(頻度論的なアプローチは、不完全だけど汎用的で適用しやすいのか...!)

Another challenge in interpreting A/B test results is rationalizing through the movements of multiple metrics (primary decision metric and secondary metrics).
**A/Bテストの結果を解釈する際のもう一つの課題は、複数の指標(primary decision metricとsecondary metrics)の動きを合理化すること**である。
A key challenge is that the metrics themselves are often not independent (i.e.metrics may generally move in the same direction, or in opposite directions).
重要な課題は、**metrics自体がしばしば独立していないこと**である（つまり、複数のmetricsは一般的に同じ方向に動いたり、逆方向に動いたりする）。
Here again, more advanced concepts from statistical inference and decision theory are applicable, and at Netflix we are engaged in research to bring more quantitative approaches to this multimetric interpretation problem.
ここでもまた、統計的推論や決定理論からのより高度な概念が適用可能であり、ネットフリックスでは、このmulti-metric解釈問題により多くの定量的アプローチをもたらすための研究に取り組んでいる。
Our approach is to include in the analysis information about historical metric movements using Bayesian inference — more to follow!
私たちのアプローチは、**ベイズ推論を用いて過去の指標の動きに関する情報を分析に含めること**である！

Finally, it’s worth noting that different types of experiments warrant different levels of human judgment in the decision making process.
最後に、実験の種類によって、意思決定プロセスにおける人間の判断のレベルが異なることは注目に値する。
For example, Netflix employs a [form of A/B testing](https://netflixtechblog.com/safe-updates-of-client-applications-at-netflix-1d01c71a930c) to ensure safe deployment of new software versions into production.
例えば、ネットフリックスは、新バージョンのソフトウェアを本番環境に安全に導入するために、A/Bテストの一種を採用している。
Prior to releasing the new version to all members, we first set up a small A/B test, with some members receiving the previous code version and some the new, to ensure there are no bugs or unexpected consequences that degrade the member experience or the performance of our infrastructure.
全メンバーに新バージョンをリリースする前に、まず小規模なA/Bテストを実施し、一部のメンバーには旧バージョンを、一部のメンバーには新バージョンを提供し、メンバーの経験やインフラのパフォーマンスを低下させるようなバグや予期せぬ影響がないことを確認しました。
For this use case, the goal is to automate the deployment process and, using frameworks like regret minimization, the test-based decision making as well.
このユースケースの場合、目標はデプロイプロセスを自動化することであり、後悔最小化のようなフレームワークを使って、テストベースの意思決定も自動化することである。
In success, we save our developers time by automatically passing the new build or flagging metric degradations to the developer.
成功すれば、新しいビルドやメトリクス・デグレードのフラグを自動的に開発者に渡すことで、開発者の時間を節約できる。

## 1.3. Summary

Here we’ve described how to build the case for a product innovation through careful analysis of the experimental data, and noted that different types of tests warrant differing levels of human input to the decision process.
ここでは、実験データの入念な分析を通じて製品革新のケースを構築する方法を説明し、テストの種類によって、意思決定プロセスにおける人間の入力レベルが異なることを指摘した。

Decision making under uncertainty, including acting on results from A/B tests, is difficult, and the tools we’ve described in this series of posts can be hard to apply correctly.
A/Bテストの結果に基づく行動を含め、不確実性の下での意思決定は難しく、この連載で紹介したツールを正しく適用するのは難しい。
But these tools, including the p-value, have withstood the test of time, as reinforced in 2021 by the American Statistical Association president’s task force statement on statistical significance and replicability:
しかし、これらのツール、p値を含むこれらのツールは、統計的有意性と再現性に関する米国統計協会会長のタスクフォース声明によって2021年に強化されたように、時代の試練に耐えてきた。
“the use of p-values and significance testing, properly applied and interpreted, are important tools that should not be abandoned.
[they] increase the rigor of the conclusions drawn from data.”
「p値と有意性検定の使用は、適切に適用され解釈される限り、放棄されるべきではない重要なツールである。[それらは]データから導かれる結論の厳密さを高める。」

The notion of publicly sharing and debating results of key product tests is ingrained in the Experimentation Culture at Netflix, which we’ll discuss in the last installment of this series.
**重要な製品テストの結果を公に共有し、議論するという考え方**は、このシリーズの最終回で説明するネットフリックスの実験文化に根付いている。
But up next, we’ll talk about the different areas of experimentation across Netflix, and the different roles that focus on experimentation.
しかし次は、Netflix全体における実験のさまざまな分野と、実験に重点を置くさまざまな役割についてお話しします。
Follow the Netflix Tech Blog to stay up to date.
最新情報はNetflix Tech Blogをフォローしてください。
