## link

https://netflixtechblog.com/what-is-an-a-b-test-b08cc1b57962

# What is an A/B Test?

This is the second post in a multi-part series on how Netflix uses A/B tests to inform decisions and continuously innovate on our products. See here for Part 1: Decision Making at Netflix. Subsequent posts will go into more details on the statistics of A/B tests, experimentation across Netflix, how Netflix has invested in infrastructure to support and scale experimentation, and the importance of the culture of experimentation within Netflix.
これは、NetflixがA/Bテストをどのように使用して意思決定を行い、製品を継続的に革新しているかについてのマルチパートシリーズの2番目の投稿です。第1部：Netflixの意思決定を参照してください。後続の投稿では、A/Bテストの統計、Netflix全体での実験、Netflixが実験をサポートおよびスケーリングするためにインフラストラクチャに投資した方法、およびNetflix内の実験の文化の重要性について詳しく説明します。

An A/B test is a simple controlled experiment. Let’s say — this is a hypothetical! — we want to learn if a new product experience that flips all of the boxart upside down in the TV UI is good for our members.
ABテストは、単純なコントロールされた実験です。仮に、これは仮想的なものです！ —私たちは、TV UIのすべてのボックスアートを逆さまにする新しい製品体験が私たちのメンバーにとって良いかどうかを学びたいとします。

To run the experiment, we take a subset of our members, usually a simple random sample, and then use random assignment to evenly split that sample into two groups. Group “A,” often called the “control group,” continues to receive the base Netflix UI experience, while Group “B,” often called the “treatment group”, receives a different experience, based on a specific hypothesis about improving the member experience (more on those hypotheses below). Here, Group B receives the Upside Down box art.
実験を実行するには、通常は単純な無作為抽出で、メンバーのサブセットを取得し、そのサンプルを2つのグループに均等に分割するためにランダム割り当てを使用します。グループ「A」は、通常「コントロールグループ」と呼ばれ、「ベースのNetflix UI体験」を引き続き受け取ります。一方、グループ「B」は、通常「治療グループ」と呼ばれ、メンバー体験を改善するという特定の仮説に基づいて、異なる体験を受け取ります（以下でそれらの仮説について詳しく説明します）。ここでは、グループBは逆さまのボックスアートを受け取ります。

We wait, and we then compare the values of a variety of metrics from Group A to those from Group B. Some metrics will be specific to the given hypothesis. For a UI experiment, we’ll look at engagement with different variants of the new feature. For an experiment that aims to deliver more relevant results in the search experience, we’ll measure if members are finding more things to watch through search. In other types of experiments, we might focus on more technical metrics, such as the time it takes the app to load, or the quality of video we are able to provide under different network conditions.
待って、次にグループAとグループBのさまざまなメトリックの値を比較します。**一部のメトリックは、特定の仮説に固有のものになります**。 UI実験の場合、新しい機能のさまざまなバリアントとのエンゲージメントを調べます。検索体験でより関連性の高い結果を提供することを目的とした実験の場合、メンバーが検索を介して見るものを見つけているかどうかを測定します。他のタイプの実験では、アプリの読み込みにかかる時間や、さまざまなネットワーク条件下で提供できるビデオの品質など、より技術的なメトリックに焦点を当てることがあります。

With many experiments, including the Upside Down box art example, we need to think carefully about what our metrics are telling us. Suppose we look at the click through rate, measuring the fraction of members in each experience that clicked on a title. This metric alone may be a misleading measure of whether this new UI is a success, as members might click on a title in the Upside Down product experience only in order to read it more easily. In this case, we might also want to evaluate what fraction of members subsequently navigate away from that title versus proceeding to play it.
逆さまのボックスアートの例を含む多くの実験では、**メトリックが何を示しているかを慎重に考える必要があります**。クリックスルー率を見てみましょう。各体験でタイトルをクリックしたメンバーの割合を測定します。このメトリックだけでは、この新しいUIが成功かどうかを判断するのに誤解を招く可能性があります。メンバーは、逆さまの製品体験でタイトルをクリックするだけで、より簡単に読むためにタイトルをクリックする可能性があります。この場合、そのタイトルから後にどのくらいのメンバーがナビゲートを離れ、再生するかどうかの割合も評価したいと思うかもしれません。

In all cases, we also look at more general metrics that aim to capture the joy and satisfaction that Netflix is delivering to our members. These metrics include measures of member engagement with Netflix: are the ideas we are testing helping our members to choose Netflix as their entertainment destination on any given night?
すべての場合において、Netflixがメンバーに提供している喜びと満足を捉えることを目的とした**一般的なメトリック**も調べます。これらのメトリックには、Netflixへのメンバーのエンゲージメントの測定が含まれます。テストしているアイデアは、メンバーが任意の夜にエンターテインメントの目的地としてNetflixを選択するのを助けていますか？

There’s a lot of statistics involved as well — how large a difference is considered significant? How many members do we need in a test in order to detect an effect of a given magnitude? How do we most efficiently analyze the data? We’ll cover some of those details in subsequent posts, focussing on the high level intuition.
統計にもたくさんの統計があります。どのくらいの差が有意と見なされますか？与えられた大きさの効果を検出するために、テストに何人のメンバーが必要ですか？データを最も効率的に分析するにはどうすればよいですか？私たちは、高レベルの直感に焦点を当てて、後続の投稿でそれらの詳細のいくつかをカバーします。

## Holding everything else constant

Because we create our control (“A”) and treatment (“B”) groups using random assignment, we can ensure that individuals in the two groups are, on average, balanced on all dimensions that may be meaningful to the test. Random assignment ensures, for example, that the average length of Netflix membership is not markedly different between the control and treatment groups, nor are content preferences, primary language selections, and so forth. The only remaining difference between the groups is the new experience we are testing, ensuring our estimate of the impact of the new experience is not biased in any way.
ランダム割り当てを使用してコントロール（「A」）と治療（「B」）グループを作成するため、2つのグループの個人がテストに意味のあるすべての次元で平均的にバランスしていることを保証できます。ランダム割り当てにより、例えば、Netflixの会員資格の平均期間がコントロールグループと治療グループの間で著しく異なることはなく、コンテンツの嗜好、主要な言語の選択なども同様です。**グループ間の唯一の残りの違いは、テストしている新しい体験であり、新しい体験の影響の推定値がどのようなバイアスもないことを保証します**。

To understand how important this is, let’s consider another way we could make decisions: we could roll out the new Upside Down box art experience (discussed above) to all Netflix members, and see if there’s a big change in one of our metrics. If there’s a positive change, or no evidence of any meaningful change, we’ll keep the new experience; if there’s evidence of a negative change, we’ll roll back to the prior product experience.
これがどれほど重要かを理解するために、別の方法で意思決定を行うことを考えてみましょう。新しい逆さまのボックスアート体験（上記で説明した）をすべてのNetflixメンバーに展開し、メトリックの1つに大きな変化があるかどうかを確認します。ポジティブな変化があるか、または意味のある変化の証拠がない場合は、新しい体験を維持します。負の変化の証拠がある場合は、以前の製品体験に戻します。

Let’s say we did that (again — this is a hypothetical!), and flipped the switch to the Upside Down experience on the 16th day of a month. How would you act if we gathered the following data?
これを行ったとしましょう（再び、これは仮想的なものです！）そして、月の16日に逆さまの体験にスイッチを切り替えました。次のデータを収集した場合、どのように行動しますか？

The data look good: we release a new product experience and member engagement goes way up! But if you had these data, plus the knowledge that Product B flips all the box art in the UI upside down, how confident would you be that the new product experience really is good for our members?
データは良さそうです：新しい製品体験をリリースすると、メンバーのエンゲージメントが大幅に向上します！しかし、これらのデータと、製品BがUIのすべてのボックスアートを逆さまにすることを知っている場合、新しい製品体験が本当にメンバーにとって良いかどうかにどれほど自信がありますか？

Do we really know that the new product experience is what caused the increase in engagement? What other explanations are possible?
新しい製品体験がエンゲージメントの増加の原因であることを本当に知っていますか？他にどんな説明が可能ですか？

What if you also knew that Netflix released a hit title, like a new season of Stranger Things or Bridgerton, or a hit movie like Army of the Dead, on the same day as the (hypothetical) roll out of the new Upside Down product experience? Now we have more than one possible explanation for the increase in engagement: it could be the new product experience, it could be the hit title that’s all over social media, it could be both. Or it could be something else entirely. The key point is that we don’t know if the new product experience caused the increase in engagement.
Netflixが同じ日に（仮想的な）新しい逆さまの製品体験をリリースしたのと同じ日に、ストレンジャーシングスやブリジャートンの新シーズン、またはアーミーオブザデッドのようなヒット映画などのヒットタイトルをリリースしたことも知っているとします。これで、エンゲージメントの増加についての説明が1つ以上あります。新しい製品体験かもしれません。ソーシャルメディアで話題のヒットタイトルかもしれません。両方かもしれません。または、完全に別のものかもしれません。重要なポイントは、新しい製品体験がエンゲージメントの増加の原因であるかどうかわからないことです。

What if instead we’d run an A/B test with the Upside Down box art product experience, with one group of members receiving the current product (“A”) and another group the Upside Down product (“B”) over the entire month, and gathered the following data:
代わりに、逆さまのボックスアート製品体験を使用してA/Bテストを実行し、1つのグループのメンバーに現在の製品（「A」）を、もう1つのグループに逆さまの製品（「B」）を1か月間受け取り、次のデータを収集した場合はどうでしょうか。

In this case, we are led to a different conclusion: the Upside Down product results in generally lower engagement (not surprisingly!), and both groups see an increase in engagement concurrent with the launch of the big title.
この場合、私たちは異なる結論に導かれます。逆さまの製品は一般的にエンゲージメントが低下します（驚くべきことではありません！）、両グループともに大きなタイトルの発売と同時にエンゲージメントが増加します。

A/B tests let us make causal statements. We’ve introduced the Upside Down product experience to Group B only, and because we’ve randomly assigned members to groups A and B, everything else is held constant between the two groups. We can therefore conclude with high probability (more on the details next time) that the Upside Down product caused the reduction in engagement.
A/Bテストを使用すると、因果関係のある声明を行うことができます。逆さまの製品体験をグループBのみに導入し、メンバーをグループAとBにランダムに割り当てたため、2つのグループ間では他のすべてが一定に保たれます。したがって、逆さまの製品がエンゲージメントの低下の原因であることを高い確率で結論付けることができます（次回の詳細については後述）。

This hypothetical example is extreme, but the broad lesson is that there is always something we won’t be able to control. If we roll out an experience to everyone and simply measure a metric before and after the change, there can be relevant differences between the two time periods that prevent us from making a causal conclusion. Maybe it’s a new title that takes off. Maybe it’s a new product partnership that unlocks Netflix for more users to enjoy. There’s always something we won’t know about. Running A/B tests, where possible, allows us to substantiate causality and confidently make changes to the product knowing that our members have voted for them with their actions.
この仮想的な例は極端ですが、広い教訓は、**常に制御できないことがあるということです。経験をすべての人に展開し、変更前と変更後にメトリックを単純に測定すると、因果関係の結論を出すことができない2つの期間の間に関連する違いがある可能性があります**(うんうん...。因果効果の検出を保証できるか否かの話...)。それは飛び立つ新しいタイトルかもしれません。それは、より多くのユーザーがNetflixを楽しむためにNetflixを解除する新しい製品パートナーシップかもしれません。私たちが知らないことは常にあります。可能な限りA/Bテストを実行すると、因果関係を裏付けることができ、メンバーが行動でそれらを投票したことを知って、製品に変更を自信を持って行うことができます。

## It all starts with an idea

An A/B test starts with an idea — some change we can make to the UI, the personalization systems that help members find content, the signup flow for new members, or any other part of the Netflix experience that we believe will produce a positive result for our members. Some ideas we test are incremental innovations, like ways to improve the text copy that appears in the Netflix product; some are more ambitious, like the test that led to “Top 10” lists that Netflix now shows in the UI.
A/Bテストはアイデアから始まります。メンバーがコンテンツを見つけるのを助けるUI、パーソナライゼーションシステム、新しいメンバーのサインアップフロー、またはメンバーにとってポジティブな結果を生み出すと信じているNetflix体験のその他の部分のいずれかに変更できるものです。テストするアイデアの一部は、Netflix製品に表示されるテキストコピーを改善する方法などの増分のイノベーションです。一部は、Netflixが現在UIに表示している「トップ10」リストにつながったテストのように、より野心的なものです。

As with all innovations that are rolled out to Netflix members around the globe, Top 10 started as an idea that was turned into a testable hypothesis. Here, the core idea was that surfacing titles that are popular in each country would benefit our members in two ways. First, by surfacing what’s popular we can help members have shared experiences and connect with one another through conversations about popular titles. Second, we can help members choose some great content to watch by fulfilling the intrinsic human desire to be part of a shared conversation.
世界中のNetflixメンバーに展開されるすべてのイノベーションと同様に、「トップ10」は、テスト可能な仮説に変えられたアイデアとして始まりました。ここでは、コアアイデアは、各国で人気のあるタイトルを浮上させることで、メンバーに2つの方法で利益をもたらすということでした。まず、人気のあるものを浮上させることで、メンバーが共有の経験を持ち、人気のあるタイトルについての会話を通じてお互いにつながるのを助けることができます。第二に、共有の会話の一部であるという内在的な人間の欲求を満たすことにより、メンバーが視聴する素晴らしいコンテンツを選択するのを助けることができます。

We next turn this idea into a testable hypothesis, a statement of the form “If we make change X, it will improve the member experience in a way that makes metric Y improve.” With the Top 10 example, the hypothesis read: “Showing members the Top 10 experience will help them find something to watch, increasing member joy and satisfaction.” The primary decision metric for this test (and many others) is a measure of member engagement with Netflix: are the ideas we are testing helping our members to choose Netflix as their entertainment destination on any given night? Our research shows that this metric (details omitted) is correlated, in the long term, with the probability that members will retain their subscriptions. Other areas of the business in which we run tests, such as the signup page experience or server side infrastructure, make use of different primary decision metrics, though the principle is the same: what can we measure, during the test, that is aligned with delivering more value in the long-term to our members?


Along with the primary decision metric for a test, we also consider a number of secondary metrics and how they will be impacted by the product feature we are testing. The goal here is to articulate the causal chain, from how user behavior will change in response to the new product experience to the change in our primary decision metric.

Articulating the causal chain between the product change and changes in the primary decision metric, and monitoring secondary metrics along this chain, helps us build confidence that any movement in our primary metric is the result of the causal chain we are hypothesizing, and not the result of some unintended consequence of the new feature (or a false positive — much more on that in later posts!). For the Top 10 test, engagement is our primary decision metric — but we also look at metrics such as title-level viewing of those titles that appear in the Top 10 list, the fraction of viewing that originates from that row vs other parts of the UI, and so forth. If the Top 10 experience really is good for our members in accord with the hypothesis, we’d expect the treatment group to show an increase in viewing of titles that appear in the Top 10 list, and for generally strong engagement from that row.

Finally, because not all of the ideas we test are winners with our members (and sometimes new features have bugs!) we also look at metrics that act as “guardrails.” Our goal is to limit any downside consequences and to ensure that the new product experience does not have unintended impacts on the member experience. For example, we might compare customer service contacts for the control and treatment groups, to check that the new feature is not increasing the contact rate, which may indicate member confusion or dissatisfaction.

## Summary

This post has focused on building intuition: the basics of an A/B test, why it’s important to run an A/B test versus rolling out a feature and looking at metrics pre- and post- making a change, and how we turn an idea into a testable hypothesis. Next time, we’ll jump into the basic statistical concepts that we use when comparing metrics from the treatment and control experiences. Follow the Netflix Tech Blog to stay up to date. Part 3 is already available.
