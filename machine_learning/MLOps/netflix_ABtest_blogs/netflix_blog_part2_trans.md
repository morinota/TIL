## 0.1. link 0.1.リンク

https://netflixtechblog.com/what-is-an-a-b-test-b08cc1b57962
https://netflixtechblog.com/what-is-an-a-b-test-b08cc1b57962

# 1. What is an A/B Test? 1. A/Bテストとは何か？

This is the second post in a multi-part series on how Netflix uses A/B tests to inform decisions and continuously innovate on our products.
この記事は、NetflixがどのようにA/Bテストを使用して意思決定を行い、継続的に製品を革新しているかについての複数回シリーズの2回目です。
See here for Part 1: Decision Making at Netflix.
パート1はこちら ネットフリックスの意思決定
Subsequent posts will go into more details on the statistics of A/B tests, experimentation across Netflix, how Netflix has invested in infrastructure to support and scale experimentation, and the importance of the culture of experimentation within Netflix.
次回の記事では、A/Bテストの統計、Netflix全体での実験、Netflixが実験をサポートし拡張するためのインフラにどのように投資してきたか、Netflix内の実験文化の重要性について、さらに詳しく説明する。

An A/B test is a simple controlled experiment.
A/Bテストは、単純な対照実験である。
Let’s say — this is a hypothetical! — we want to learn if a new product experience that flips all of the boxart upside down in the TV UI is good for our members.
これは仮定の話です！- TVのUIでボックスアートをすべてひっくり返すような新しい製品体験が、メンバーにとって良いものかどうかを知りたい。

To run the experiment, we take a subset of our members, usually a simple random sample, and then use random assignment to evenly split that sample into two groups.
実験を行うには、会員の一部（通常は単純無作為標本）を採取し、無作為割付けを使ってその標本を均等に2つのグループに分ける。
Group “A,” often called the “control group,” continues to receive the base Netflix UI experience, while Group “B,” often called the “treatment group”, receives a different experience, based on a specific hypothesis about improving the member experience (more on those hypotheses below).
対照群」と呼ばれることの多い「グループA」は、ベースとなるネットフリックスのUI体験を受け続けるが、「治療群」と呼ばれることの多い「グループB」は、会員体験の改善に関する特定の仮説に基づいて、異なる体験を受ける（これらの仮説については後述する）。
Here, Group B receives the Upside Down box art.
ここでは、グループBがアップサイドダウンのボックスアートを受け取る。

We wait, and we then compare the values of a variety of metrics from Group A to those from Group B.
そして、AグループとBグループのさまざまな指標の値を比較する。
Some metrics will be specific to the given hypothesis.
メトリクスの中には、与えられた仮説に特化したものもある。
For a UI experiment, we’ll look at engagement with different variants of the new feature.
UIの実験として、新機能のさまざまなバリエーションでのエンゲージメントを調べます。
For an experiment that aims to deliver more relevant results in the search experience, we’ll measure if members are finding more things to watch through search.
検索エクスペリエンスにおいてより関連性の高い結果を提供することを目的とした実験では、会員が検索を通じてより多くの観たいものを見つけているかどうかを測定する。
In other types of experiments, we might focus on more technical metrics, such as the time it takes the app to load, or the quality of video we are able to provide under different network conditions.
他のタイプの実験では、アプリのロードにかかる時間や、異なるネットワーク条件下で提供できるビデオの品質など、より技術的な指標に焦点を当てるかもしれません。

![figure2]()

With many experiments, including the Upside Down box art example, we need to think carefully about what our metrics are telling us.
アップサイドダウンのボックスアートの例も含め、多くの実験では、測定基準が何を物語っているのかを注意深く考える必要がある。

Suppose we look at the click through rate, measuring the fraction of members in each experience that clicked on a title.
各エクスペリエンスにおいて、タイトルをクリックしたメンバーの割合を測定し、クリック率を見るとします。

This metric alone may be a misleading measure of whether this new UI is a success, as members might click on a title in the Upside Down product experience only in order to read it more easily.
この指標だけでは、この新しいUIが成功したかどうかを測るには誤解を招くかもしれない。というのも、会員がアップサイドダウンの製品エクスペリエンスでタイトルをクリックするのは、より読みやすくするためだけかもしれないからだ。

In this case, we might also want to evaluate what fraction of members subsequently navigate away from that title versus proceeding to play it.
この場合、何パーセントの会員が、そのタイトルからナビゲートし、プレイに進むかを評価することもできるだろう。

In all cases, we also look at more general metrics that aim to capture the joy and satisfaction that Netflix is delivering to our members.
すべての場合において、Netflixが会員に提供している喜びや満足度を把握することを目的とした、より一般的な指標も見ています。
These metrics include measures of member engagement with Netflix: are the ideas we are testing helping our members to choose Netflix as their entertainment destination on any given night?
これらの指標には、会員とNetflixとのエンゲージメントに関する指標も含まれる： 私たちがテストしているアイデアは、会員がある夜にNetflixをエンターテイメントの目的地として選ぶのに役立っているか？

There’s a lot of statistics involved as well — how large a difference is considered significant? How many members do we need in a test in order to detect an effect of a given magnitude? How do we most efficiently analyze the data? We’ll cover some of those details in subsequent posts, focussing on the high level intuition.
どの程度の差が有意とみなされるのか？ある大きさの効果を検出するためには、何人の被験者が必要なのか？データを最も効率的に分析するにはどうすればよいのか？このような詳細については、次回以降、ハイレベルな直観に焦点を当てながら、いくつか取り上げることにする。

## 1.1. Holding everything else constant 1.1.他のすべてを一定に保つ

Because we create our control (“A”) and treatment (“B”) groups using random assignment, we can ensure that individuals in the two groups are, on average, balanced on all dimensions that may be meaningful to the test.
無作為割付けを用いて対照群（"A"）と治療群（"B"）を作るので、2つの群に属する個人が、平均して、テストに意味のありそうなすべての次元で均衡していることを保証できる。
Random assignment ensures, for example, that the average length of Netflix membership is not markedly different between the control and treatment groups, nor are content preferences, primary language selections, and so forth.
無作為割当てにより、例えば、ネットフリックスの平均会員期間が対照群と治療群の間で著しく異なることはなく、コンテンツの嗜好や主要言語の選択なども異なることはない。
The only remaining difference between the groups is the new experience we are testing, ensuring our estimate of the impact of the new experience is not biased in any way.
グループ間に残る唯一の違いは、私たちがテストしている新しい経験であり、新しい経験の影響の推定がいかなる偏りもないことを保証する。

To understand how important this is, let’s consider another way we could make decisions: we could roll out the new Upside Down box art experience (discussed above) to all Netflix members, and see if there’s a big change in one of our metrics.
これがいかに重要かを理解するために、私たちが意思決定をする別の方法を考えてみましょう： 新しいUpside Downのボックスアートエクスペリエンス（上述）をNetflixの全会員に展開し、指標のひとつに大きな変化があるかどうかを見てみましょう。
If there’s a positive change, or no evidence of any meaningful change, we’ll keep the new experience; if there’s evidence of a negative change, we’ll roll back to the prior product experience.
ポジティブな変化、あるいは意味のある変化の証拠がなければ、新しい経験を維持し、ネガティブな変化の証拠があれば、以前の製品経験にロールバックする。

Let’s say we did that (again — this is a hypothetical!), and flipped the switch to the Upside Down experience on the 16th day of a month.
仮にそうして（これも仮定の話だ！）、ある月の16日目にアップサイドダウン体験のスイッチを入れたとしよう。
How would you act if we gathered the following data?
次のようなデータを集めたら、あなたはどう行動しますか？

The data look good: we release a new product experience and member engagement goes way up! But if you had these data, plus the knowledge that Product B flips all the box art in the UI upside down, how confident would you be that the new product experience really is good for our members?
データは良好だ： 新しい製品体験をリリースすると、メンバーのエンゲージメントが大幅に向上する！しかし、これらのデータに加え、製品BがUIのボックスアートをすべてひっくり返してしまうという知識があったとしたら、その新しい製品体験が本当にメンバーにとって良いものであると、あなたは確信できるだろうか？

Do we really know that the new product experience is what caused the increase in engagement? What other explanations are possible?
新商品の体験がエンゲージメントを高めたと本当に言えるのだろうか？他にどんな説明が可能だろうか？

What if you also knew that Netflix released a hit title, like a new season of Stranger Things or Bridgerton, or a hit movie like Army of the Dead, on the same day as the (hypothetical) roll out of the new Upside Down product experience? Now we have more than one possible explanation for the increase in engagement: it could be the new product experience, it could be the hit title that’s all over social media, it could be both.
ストレンジャー・シングス』や『ブリッジマン』の新シーズン、あるいは『アーミー・オブ・ザ・デッド』のようなヒット映画が、（仮に）アップサイドダウンの新しい製品体験の展開と同じ日に、ネットフリックスからリリースされたとしたらどうだろう？さて、エンゲージメントの増加については、複数の可能性が考えられる： 新しい製品体験のせいかもしれないし、ソーシャルメディアで話題のヒットタイトルのせいかもしれないし、その両方かもしれない。
Or it could be something else entirely.
あるいは、まったく別のものかもしれない。
The key point is that we don’t know if the new product experience caused the increase in engagement.
重要なのは、新しい製品体験がエンゲージメントの増加を引き起こしたかどうかはわからないということだ。

What if instead we’d run an A/B test with the Upside Down box art product experience, with one group of members receiving the current product (“A”) and another group the Upside Down product (“B”) over the entire month, and gathered the following data:
その代わりに、アップサイドダウンのボックスアートの商品体験でA/Bテストを実施し、あるグループのメンバーには現在の商品（「A」）を、別のグループにはアップサイドダウンの商品（「B」）を1カ月間提供し、次のようなデータを集めたとしたらどうだろう：

In this case, we are led to a different conclusion: the Upside Down product results in generally lower engagement (not surprisingly!), and both groups see an increase in engagement concurrent with the launch of the big title.
この場合、我々は異なる結論に導かれる： アップサイドダウン製品では、エンゲージメントが概して低く（驚くには値しない！）、両グループともビッグタイトルの発売と同時にエンゲージメントが増加する。

A/B tests let us make causal statements.We’ve introduced the Upside Down product experience to Group B only, and because we’ve randomly assigned members to groups A and B, everything else is held constant between the two groups.
A/Bテストでは、因果関係を明らかにすることができる。グループBのみにアップサイドダウンの製品体験を導入し、グループAとBにメンバーをランダムに割り当てたので、他のすべては2つのグループ間で一定に保たれる。
We can therefore conclude with high probability (more on the details next time) that the Upside Down product caused the reduction in engagement.
したがって、（詳細は次回に譲るが）高い確率で、アップサイドダウン製品がエンゲージメントの低下を引き起こしたと結論づけることができる。

This hypothetical example is extreme, but the broad lesson is that there is always something we won’t be able to control.
この仮定の例は極端だが、大まかな教訓は、コントロールできないことが常にあるということだ。
If we roll out an experience to everyone and simply measure a metric before and after the change, there can be relevant differences between the two time periods that prevent us from making a causal conclusion.
ある経験を全員に展開し、その変化の前後で単純に指標を測定した場合、2つの期間の間に関連する差異が生じ、因果関係の結論を出すことができなくなる可能性がある。
Maybe it’s a new title that takes off.
もしかしたら、新しいタイトルが軌道に乗るかもしれない。
Maybe it’s a new product partnership that unlocks Netflix for more users to enjoy.
もしかしたら、Netflixをより多くのユーザーに楽しんでもらうための新しい製品提携かもしれない。
There’s always something we won’t know about.
常に私たちが知らないことがある。
Running A/B tests, where possible, allows us to substantiate causality and confidently make changes to the product knowing that our members have voted for them with their actions.
可能な限りA/Bテストを実施することで、私たちは因果関係を立証することができ、会員がその行動で投票してくれたことを知っているため、自信を持って製品に変更を加えることができる。

## 1.2. It all starts with an idea

An A/B test starts with an idea — some change we can make to the UI, the personalization systems that help members find content, the signup flow for new members, or any other part of the Netflix experience that we believe will produce a positive result for our members.
A/Bテストは、UI、会員がコンテンツを見つけやすくするパーソナライゼーションシステム、新規会員登録フロー、その他ネットフリックス体験のあらゆる部分に加えることができる変更で、会員にとって良い結果をもたらすと思われるアイデアから始まります。
Some ideas we test are incremental innovations, like ways to improve the text copy that appears in the Netflix product; some are more ambitious, like the test that led to “Top 10” lists that Netflix now shows in the UI.
私たちがテストするアイデアの中には、Netflixの製品に表示されるテキストコピーを改善する方法のような、段階的なイノベーションもあれば、Netflixが現在UIで表示している「トップ10」リストにつながったテストのような、より野心的なものもある。

As with all innovations that are rolled out to Netflix members around the globe, Top 10 started as an idea that was turned into a testable hypothesis.
世界中のNetflix会員に展開されるすべてのイノベーションと同様、Top 10も最初はアイデアから始まり、検証可能な仮説に変わった。
Here, the core idea was that surfacing titles that are popular in each country would benefit our members in two ways.
ここで、核となるアイデアは、それぞれの国で人気のあるタイトルを表に出すことで、2つの点で会員に利益をもたらすというものだった。
First, by surfacing what’s popular we can help members have shared experiences and connect with one another through conversations about popular titles.
まず、人気のあるタイトルを表に出すことで、会員が共通の体験を持ち、人気のあるタイトルについての会話を通じて互いにつながることができる。
Second, we can help members choose some great content to watch by fulfilling the intrinsic human desire to be part of a shared conversation.
第二に、共有された会話の一部であることという人間の本能的な欲求を満たすことで、会員が見る素晴らしいコンテンツを選ぶのを手伝うことができる。

We next turn this idea into a testable hypothesis, a statement of the form “If we make change X, it will improve the member experience in a way that makes metric Y improve.”
次に、このアイデアを検証可能な仮説、つまり、"Xを変更すれば、指標Yが改善されるような形で、メンバーのエクスペリエンスが改善される "という形のステートメントに変える。
With the Top 10 example, the hypothesis read: “Showing members the Top 10 experience will help them find something to watch, increasing member joy and satisfaction.”
トップ10の例では、仮説は次のようになった：「トップ10の体験を会員に表示することで、彼らが見るものを見つけるのを手伝い、会員の喜びと満足度を高める」。
The primary decision metric for this test (and many others) is a measure of member engagement with Netflix:
このテスト（および他の多くのテスト）の主要な意思決定指標は、Netflixとの会員のエンゲージメントを測定するものである：
are the ideas we are testing helping our members to choose Netflix as their entertainment destination on any given night?
私たちがテストしているアイデアは、会員がある夜にNetflixをエンターテイメントの目的地として選ぶのに役立っているか？
Our research shows that this metric (details omitted) is correlated, in the long term, with the probability that members will retain their subscriptions.
私たちの調査によると、この指標（詳細は省略）は、長期的には、会員がサブスクリプションを維持する確率と相関している。
Other areas of the business in which we run tests, such as the signup page experience or server side infrastructure, make use of different primary decision metrics, though the principle is the same: what can we measure, during the test, that is aligned with delivering more value in the long-term to our members?
サインアップページのエクスペリエンスやサーバーサイドのインフラストラクチャーなど、テストを実施する他の事業分野では、異なる主要な判断基準を使用していますが、原則は同じです： テスト中に何を測定すれば、長期的に会員により多くの価値を提供できるのか？

Along with the primary decision metric for a test, we also consider a number of secondary metrics and how they will be impacted by the product feature we are testing.
テストの主要な決定指標とともに、私たちは多くのsecondary metrics（二次的な指標）を考慮し、テストしているプロダクト機能によってそれらの指標がどのように影響を受けるかを考えます。
The goal here is to articulate the causal chain, from how user behavior will change in response to the new product experience to the change in our primary decision metric.
ここでの目標は、ユーザーの行動が新しい製品体験に反応してどのように変化し、主要な意思決定指標がどのように変化するかという因果の連鎖を明確にすることです。

Articulating the causal chain between the product change and changes in the primary decision metric, and monitoring secondary metrics along this chain, helps us build confidence that any movement in our primary metric is the result of the causal chain we are hypothesizing, and not the result of some unintended consequence of the new feature (or a false positive — much more on that in later posts!).
プロダクトの変更とprimary decision metricの変化の間の因果関係を明確にし、この連鎖に沿ってsecondary metricsを監視することで、私たちは、主要な指標の変化が私たちが仮説を立てている因果連鎖の結果であることを確信することができます。新機能の意図しない結果（または偽陽性）の結果ではない（これについては後の投稿で詳しく説明します）。
For the Top 10 test, engagement is our primary decision metric — but we also look at metrics such as title-level viewing of those titles that appear in the Top 10 list, the fraction of viewing that originates from that row vs other parts of the UI, and so forth.
トップ10テストでは、エンゲージメントがprimary decision metricである。しかし、トップ10リストに掲載されたタイトルのタイトルレベルの視聴、その行からの視聴の割合とUIの他の部分からの視聴の割合など、その他の指標も見ています。
If the Top 10 experience really is good for our members in accord with the hypothesis, we’d expect the treatment group to show an increase in viewing of titles that appear in the Top 10 list, and for generally strong engagement from that row.
仮に、トップ10の体験が本当に会員にとって良いものであるならば、トップ10リストに掲載されたタイトルの視聴が増加し、その列から一般的に強いエンゲージメントが得られると予想される。

Finally, because not all of the ideas we test are winners with our members (and sometimes new features have bugs!) we also look at metrics that act as “guardrails.” Our goal is to limit any downside consequences and to ensure that the new product experience does not have unintended impacts on the member experience.
最後に、私たちがテストするアイデアのすべてが会員に支持されるとは限らないため（そして新機能にバグがあることもあります！）、私たちは "ガードレール "として機能する指標にも注目します。私たちの目標は、あらゆるマイナス面を制限し、新製品の体験が会員の体験に意図しない影響を及ぼさないようにすることです。
For example, we might compare customer service contacts for the control and treatment groups, to check that the new feature is not increasing the contact rate, which may indicate member confusion or dissatisfaction.
例えば、新機能が会員の混乱や不満を示す可能性のある接触率を増加させていないことを確認するために、対照群と処置群のカスタマーサービスへの接触を比較するかもしれない。

## 1.3. Summary 1.3.Summary

This post has focused on building intuition: the basics of an A/B test, why it’s important to run an A/B test versus rolling out a feature and looking at metrics pre- and post- making a change, and how we turn an idea into a testable hypothesis.
この投稿では、直観を構築することに焦点を当ててきました： A/Bテストの基本、なぜA/Bテストを実施することが重要なのか、機能を展開することと変更前後のメトリクスを見ること、そしてアイデアを検証可能な仮説に変える方法です。
Next time, we’ll jump into the basic statistical concepts that we use when comparing metrics from the treatment and control experiences.
次回は、治療体験と対照体験の測定基準を比較する際に使用する、基本的な統計的概念に飛び込むことにしよう。
Follow the Netflix Tech Blog to stay up to date.
最新情報はNetflix Tech Blogをフォローしてください。
Part 3 is already available.
パート3はすでに公開されている。
