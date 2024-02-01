## link リンク

https://netflixtechblog.com/experimentation-is-a-major-focus-of-data-science-across-netflix-f67923f8e985
https://netflixtechblog.com/experimentation-is-a-major-focus-of-data-science-across-netflix-f67923f8e985

# Experimentation is a major focus of Data Science across Netflix ネットフリックスのデータサイエンスは、実験に重点を置いている。

Earlier posts in this series covered the basics of A/B tests (Part 1 and Part 2 ), core statistical concepts (Part 3 and Part 4), and how to build confidence in decisions based on A/B test results (Part 5).
このシリーズの以前の記事では、A/Bテストの基本（第1回と第2回）、中核となる統計的概念（第3回と第4回）、A/Bテスト結果に基づく意思決定の信頼性を高める方法（第5回）を取り上げた。
Here we describe the role of Experimentation and A/B testing within the larger Data Science and Engineering organization at Netflix, including how our platform investments support running tests at scale while enabling innovation.
ここでは、Netflixの大規模なデータサイエンスとエンジニアリングの組織におけるエクスペリメンテーションとA/Bテストの役割について説明します。
The subsequent and final post in this series will discuss the importance of the culture of experimentation within Netflix.
このシリーズの最終回となる次回は、ネットフリックスにおける実験文化の重要性について論じる。

Experimentation and causal inference is one of the primary focus areas within Netflix’s Data Science and Engineering organization.
**実験と因果推論は、ネットフリックスのデータサイエンス・エンジニアリング組織における主要な重点分野のひとつである**。
To directly support great decision-making throughout the company, there are a number of data science teams at Netflix that partner directly with Product Managers, engineering teams, and other business units to design, execute, and learn from experiments.
**会社全体の優れた意思決定を直接サポートするために**、ネットフリックスには、プロダクトマネージャー、エンジニアリングチーム、その他のビジネスユニットと直接提携し、実験を設計、実行、そして実験から学ぶデータサイエンスチームが数多くあります。
To enable scale, we’ve built, and continue to invest in, an internal experimentation platform (XP for short).
規模拡大を可能にするため、私たちは社内に実験プラットフォーム（略してXP）を構築し、投資を続けている。
And we intentionally encourage collaboration between the centralized experimentation platform and the data science teams that partner directly with Netflix business units.
また、集中型の実験プラットフォームと、ネットフリックスの事業部門と直接提携するデータサイエンスチームとのコラボレーションを意図的に奨励しています。

Curious to learn more about other Data Science and Engineering functions at Netflix? To learn about Analytics and Viz Engineering, have a look at Analytics at Netflix: Who We Are and What We Do by Molly Jackman & Meghana Reddy and How Our Paths Brought Us to Data and Netflix by Julie Beckley & Chris Pham.
Netflixの他のデータサイエンスとエンジニアリング機能についてもっと知りたいですか？アナリティクスとヴィズ・エンジニアリングについては、Netflixのアナリティクスをご覧ください： Molly Jackman & Meghana Reddy著「Who We Are and What We Do」、Julie Beckley & Chris Pham著「How Our Paths Brought Us to Data and Netflix」をご覧ください。
Curious to learn about what it’s like to be a Data Engineer at Netflix? Hear directly from Samuel Setegne, Dhevi Rajendran, Kevin Wylie, and Pallavi Phadnis in our “Data Engineers of Netflix” interview series.
Netflixのデータエンジニアの仕事について知りたいですか？サミュエル・セテグネ、デビ・ラジェンドラン、ケビン・ワイリー、パラビ・ファドニスのインタビューシリーズ「Netflixのデータエンジニア」をご覧ください。

Experimentation and causal inference data scientists who work directly with Netflix business units develop deep domain understanding and intuition about the business areas where they work.
ネットフリックスの事業部門と直接仕事をする実験と因果推論のデータサイエンティストは、彼らが働く事業領域について深い領域理解と直感を身につける。
Data scientists in these roles apply the scientific method to improve the Netflix experience for current and future members, and are involved in the whole life cycle of experimentation: data exploration and ideation; designing and executing tests; analyzing results to help inform decisions on tests; synthesizing learnings from numerous tests (and other sources) to understand member behavior and identify opportunity areas for innovation.
このような役割を担うデータサイエンティストは、現在および将来の会員のネットフリックス体験を向上させるために科学的手法を適用し、**実験の全ライフサイクルに携わります**： データ探索とアイデアの創出、テストの設計と実行、テストの意思決定に役立つ結果の分析、会員の行動を理解し、イノベーションの機会領域を特定するための多数のテスト（およびその他の情報源）からの学習の統合。
It’s a virtuous, scientifically rigorous cycle of testing specific hypotheses about member behaviors and preferences that are grounded in general principles (deduction), and generalizing learning from experiments to build up our conceptual understanding of our members (induction).
それは、**一般原則に基づいた会員の行動や嗜好に関する具体的な仮説を検証し（演繹）、実験から得た学びを一般化して会員の概念的な理解を深める（帰納）という、科学的に厳密な好循環**である。
In success, this cycle enables us to rapidly innovate on all aspects of the Netflix service, confident that we are delivering more joy to our members as our decisions are backed by empirical evidence.
このサイクルを成功させることで、私たちはネットフリックス・サービスのあらゆる面において、経験則に裏打ちされた決断を下し、より多くの喜びを会員に提供することを確信しながら、迅速にイノベーションを起こすことができる。

Curious to learn more? Have a look at “A Day in the Life of an Experimentation and Causal Inference Scientist @ Netflix” by Stephanie Lane, Wenjing Zheng, and Mihir Tendulkar.
もっと知りたいですか？ステファニー・レーン、鄭文精、ミヒール・テンドゥルカルによる「A Day in the Life of an Experimentation and Causal Inference Scientist @ Netflix」をご覧ください。

Success in these roles requires a broad technical skill set, a self-starter attitude, and a deep curiosity about the domain space.
このような職務で成功するには、幅広い技術的スキルセット、セルフスターターとしての姿勢、領域空間に対する深い好奇心が必要です。
Netflix data scientists are relentless in their pursuit of knowledge from data, and constantly look to go the extra distance and ask one more question.
ネットフリックスのデータ・サイエンティストは、データから知識を得ることに絶え間なく取り組み、**常に一歩踏み込んだ質問**をしている。
“What more can we learn from this test, to inform the next one?”
このテストから更に何を学び、次のテストに役立てることができるだろうか？
“What information can I synthesize from the last year of tests, to inform opportunity sizing for next year’s learning roadmap?”
昨年のテストからどのような情報を総合して、来年の学習ロードマップのオポチュニティ・サイジングに役立てることができるだろうか？
“What other data and intuition can I bring to the problem?”
この問題に、他にどのようなデータや直感をもたらすことができるだろうか？
“Given my own experience with Netflix, where might there be opportunities to test and improve on the current experience?”
私自身のネットフリックスでの経験から、現在の体験をテストし改善する機会はどこにあるだろうか？
We look to our data scientists to push the boundaries on both the design and analysis of experiments: what new approaches or methods may yield valuable insights, given the learning agenda in a particular part of the product?
私たちは、データサイエンティストに、実験の設計と分析の両方の限界を押し広げることを期待しています： 製品の特定の部分における学習課題を考えると、どのような新しいアプローチや方法が貴重な洞察をもたらす可能性があるのか？
These data scientists are also sought after as trusted thought partners by their business partners, as they develop deep domain expertise about our members and the Netflix experience.
これらのデータサイエンティストは、会員とNetflixの体験について深い領域知識を身につけるにつれて、ビジネスパートナーからの信頼できる思考パートナーとしても求められています。

Here are quick summaries of a few of the experimentation areas at Netflix and some of the innovative work that’s come out of each.
ここでは、**Netflixにおけるいくつかの実験分野と、それぞれから生まれた革新的な作品**を簡単にまとめてみた。
This is not an exhaustive list, and we’ve focused on areas where opportunities to learn and deliver a better member experience through experimentation may be less obvious.
これは網羅的なリストではなく、実験を通じて学習し、より良い会員体験を提供する機会が目立たない分野に焦点を絞っている。

## Growth Advertising 成長広告

At Netflix, we want to entertain the world! Our growth team advertises on social media platforms and other websites to share news about upcoming titles and new product features, with the ultimate goal of growing the number of Netflix members worldwide.
Netflixは世界を楽しませたいと考えています！Netflixのグロースチームは、世界中のNetflix会員数を増やすことを最終目標に、ソーシャルメディアプラットフォームやその他のウェブサイトで、近日配信予定のタイトルや新機能に関するニュースを発信しています。
Data Scientists play a vital role in building automated systems that leverage causal inference to decide how we spend our advertising budget.
データサイエンティストは、因果推論を活用して広告予算の使い道を決定する自動システムを構築する上で重要な役割を担っている。

In advertising, the treatments (the ads that we purchase) have a direct monetary cost to Netflix.
広告では、トリートメント（私たちが購入する広告）はネットフリックスにとって直接的な金銭的コストとなる。
As a result, we are risk averse in decision making and actively mitigate the probability of purchasing ads that are not efficiently attracting new members.
その結果、リスク回避的な意思決定を行い、新規会員を効率的に獲得できない広告を購入する確率を積極的に軽減している。
Abiding by this risk aversion is challenging in our domain because experiments generally have low power (see Part 4).
このリスク回避を守ることは、私たちの領域では難しい。というのも、**実験は一般的にパワーが低いから**だ（第4回参照）。(検出力が低い = 偽陰性が高い...!)
For example we rely on difference-in-differences techniques for unbiased comparisons between the potentially different audiences experiencing each advertising treatment, and these approaches effectively reduce the sample size (more details for the very interested reader).
例えば、各広告処理を経験した潜在的に異なるオーディエンス間の不偏比較を行うために、差分差分法に頼っているが、これらのアプローチはサンプルサイズを効果的に縮小する（詳細は興味のある読者に）。
One way to address these power reductions would be to simply run longer experiments — but that would slow down our overall pace of innovation.
このような**検出力の低下に対処する方法の1つは、単に長期間の実験を行うことだが、それでは全体的なイノベーションのペースが遅くなってしまう**。

Here we highlight two related problems for experimentation in this domain and briefly describe how we address them while maintaining a high cadence of experimentation.
ここでは、この領域における実験に関連する2つの問題に焦点を当て、実験の高いケイデンスを維持しながら、どのようにそれらに対処するかを簡単に説明する。

Recall that Part 3 and Part 4 described two types of errors: false positives (or Type-I errors) and false negatives (Type-II errors).
第3部と第4部では、2種類のエラーについて説明した： 偽陽性（またはI型エラー）と偽陰性（II型エラー）である。
Particularly in regimes where experiments are low-powered, two other error types can occur with high probability, so are important to consider when acting upon a statistically significant test result:
特に**実験が低パワーの場合、他の2つのエラーが高い確率で発生する可能性**があり、統計的に有意なテスト結果に基づいて行動する際に考慮することが重要である：
(Type-1とType-2とは異なる2つのエラー??)

- **A Type-S error** occurs when, given that we observe a statistically-significant result, the estimated metric movement has the opposite sign relative to the truth. Type-Sエラーは、**統計的に有意な結果が観測されたにもかかわらず、推定されたメトリックの動きが真実とは逆の符号を持つ場合**に発生する。

- **A Type-M error** occurs when, given that we observe a statistically-significant result, the size of the estimated metric movement is magnified (or exaggerated) relative to the truth. Type-Mエラーは、**統計的に有意な結果が観測されたにもかかわらず、推定されたメトリックの動きの大きさが真実よりも相対的に拡大（または誇張）された場合**に発生する。

If we simply declare statistically significant test results (with positive metric movements) to be winners, a Type-S error would imply that we actually selected the wrong treatment to promote to production, and all our future advertising spend would be producing suboptimal results.
統計的に有意なテスト結果（プラスの指標の動き）を単に勝者と宣言すれば、**Type-Sエラーは、私たちが実際にproductionに促進するために間違ったtreatmentを選択したこと**を意味し、私たちの将来の広告費はすべて、最適とは言えない結果を生み出すことになる。
A Type-M error means that we are over-estimating the impact of the treatment.
**type-Mエラーは、treatmentの影響を過大評価していることを意味**する。
In the short term, a Type-M error means we would overstate our result, and in the long-term it could lead to overestimating our optimal budget level, or even misprioritizing future research tracks.
短期的には、タイプMのエラーは、結果を誇張しすぎることを意味し、長期的には、最適な予算レベルを過大評価することにつながり、将来の研究路線の優先順位を誤る可能性さえある。(長期的には、type-Mエラーも悪影響が大きいのかも。)

To reduce the impact of these errors, we take a Bayesian approach to experimentation in growth advertising.
**こうした誤差の影響を減らすため、成長広告ではベイズ的なアプローチで実験を行う**。
We’ve run many tests in this area and use the distribution of metric movements from past tests as an additional input to the analysis.
私たちはこの分野で多くのテストを実施しており、**過去のテストから得られたメトリクスの動きの分布を分析への追加インプットとして使用**している。(事前分布的な役割...??)
Intuitively (and mathematically) this approach results in estimated metric movements that are smaller in magnitude and that feature narrower confidence intervals (Part 3).
直感的に（そして数学的に）、このアプローチは、推定されたメトリックの動きがより小さく、信頼区間が狭くなる（第3回参照）。
Combined, these two effects reduce the risk of Type-S and Type-M errors.
この2つの効果を組み合わせることで、S型エラーやM型エラーのリスクを減らすことができる。

As the benefits from ending suboptimal treatments early can be substantial, we would also like to be able to make informed, statistically-valid decisions to end experiments as quickly as possible.This is an active research area for the team, and we’ve investigated Group Sequential Testing and Bayesian Inference as methods to allow for optimal stopping (see below for more on both of those).
**最適でないtreatmentを早期に終了することで得られる利点は大きいため、できるだけ早く実験を終了するための情報に基づいた統計的に妥当な意思決定を行うこともできるようにしたい**。これはチームの活発な研究分野であり、最適な停止を可能にするための方法として、**Group Sequential Testing**と**Bayesian Inference**を調査してきた（以下でそれぞれについて詳しく説明する）。
The latter, when combined with decision theoretic concepts like expected loss (or risk) minimization, can be used to formally evaluate the impact of different decisions — including the decision to end the experiment early.
後者は、期待損失（またはリスク）最小化のような意思決定理論的概念と組み合わせることで、さまざまな意思決定（実験を早期に終了する意思決定を含む）の影響を正式に評価するために使用することができる。

## Payments ペイメント

The payments team believes that the methods of payment (credit card, direct debit, mobile carrier billing, etc) that a future or current member has access to should never be a barrier to signing up for Netflix, or the reason that a member leaves Netflix.
ペイメントチームは、将来または現在の会員が利用できる支払い方法（クレジットカード、口座振替、携帯キャリア課金など）が、Netflixに登録する際の障壁や、会員がNetflixを退会する理由になってはならないと考えています。(課金システムチーム、みたいなことかな??)
There are numerous touchpoints between a member and the payments team: we establish relationships between Netflix and new members, maintain those relationships with renewals, and (sadly!) see the end of those relationships when members elect to cancel.
会員とペイメントチームとの間には多くの接点があります: **ネットフリックスと新規会員との関係を構築し、その関係を更新で維持し、そして（悲しいことですが！）会員が解約を選択すると、その関係は終わりを迎えます**。

We innovate on methods of payment, authentication experiences, text copy and UI designs on the Netflix product, and any other place that we may smooth the payment experience for members.
私たちは、支払い方法、認証体験、Netflix製品上のテキストコピーやUIデザイン、その他会員の支払い体験をスムーズにするあらゆる場所について革新的な取り組みを行っています。
In all of these areas, we seek to improve the quality and velocity of our decision-making, guided by the testing principles laid out in this series.
これらすべての分野において、**私たちはこのシリーズで示したテストの原則に導かれながら、意思決定の質と速度の向上を目指している**。

Decision quality doesn’t just mean telling people, “Ship it!” when the p-value (see Part 3) drops below 0.05.
**意思決定の質とは、p値（第3回参照）が0.05を下回ったときに「出荷しろ！」と言うことだけを意味しない**。
It starts with having a good hypothesis and a clear decision framework — especially one that judiciously balances between long-term objectives and getting a read in a pragmatic timeframe.
それは、**優れた仮説と明確な決断の枠組みを持つことから始まる**。特に、長期的な目標と現実的な時間枠で読み取ることのバランスを慎重にとるものである。
We don’t have unlimited traffic or time, so sometimes we have to make hard choices.
交通量も時間も無制限ではないので、時には厳しい選択を迫られることもある。
Are there metrics that can yield a signal faster? What’s the tradeoff of using those? What’s the expected loss of calling this test, versus the opportunity cost of running something else? These are fun problems to tackle, and we are always looking to improve.
**より早くシグナルを得られる指標はあるのか？それを使うことのトレードオフは？このテストを実施することによる期待損失と、他のテストを実施することによる機会費用とは？これらは取り組むのが楽しい問題であり、私たちは常に改善を求めている**。

We also actively invest in increasing decision velocity, often in close partnership with the Experimentation Platform team.
私たちはまた、しばしば実験プラットフォーム・チームと緊密に連携しながら、意思決定の速度を高めるために積極的に投資しています。
Over the past year, we’ve piloted models and workflows for three approaches to faster experimentation: Group Sequential Testing (GST), Gaussian Bayesian Inference, and Adaptive Testing.
この1年間、我々は、**より迅速な実験を行うための3つのアプローチのモデルとワークフローを試験的に導入してきた**： **Group Sequential Testing (GST)**、**Gaussian Bayesian Inference**、**Adaptive Testing**である。
Any one of these techniques would enhance our experiment throughput on their own; together, they promise to alter the trajectory of payments experimentation velocity at Netflix.
これらのテクニックのうち、どれか1つだけでも実験のスループットは向上するだろう。

## Partnerships パートナーシップ

We want all of our members to enjoy a high quality experience whenever and however they access Netflix.
Netflixの会員の皆様には、いつでも、どのような方法でも、高品質の体験を楽しんでいただきたいと考えています。
Our partnerships teams work to ensure that the Netflix app and our latest technologies are integrated on a wide variety of consumer products, and that Netflix is easy to discover and use on all of these devices.
私たちのパートナーシップチームは、Netflixアプリと私たちの最新テクノロジーが様々な消費者向け製品に統合され、Netflixがこれらすべてのデバイスで簡単に発見され、利用できるように取り組んでいます。
We also partner with mobile and PayTV operators to create bundled offerings to bring the value of Netflix to more future members.
また、携帯電話会社やPayTV事業者と提携し、Netflixの価値をより多くの未来の会員に提供するためのバンドルサービスを提供しています。

In the partnerships space, many experiences that we want to understand, such as partner-driven marketing campaigns, are not amenable to the A/B testing framework that has been the focus of this series.
パートナーシップの分野では、パートナー主導のマーケティング・キャンペーンなど、**理解したい経験の多くが、この連載で焦点をあててきたA/Bテストの枠組みには適さない**。
Sometimes, users self-select into the experience, or the new experience is rolled out to a large cluster of users all at once.
時には、ユーザが自らそのエクスペリエンスを選択することもあれば、新しいエクスペリエンスが大規模なユーザ集団に一斉に展開されることもある。
This lack of randomization precludes the straightforward causal conclusions that follow from A/B tests.
**この無作為化の欠如は、A/Bテストから導かれる直接的な因果関係の結論を妨げる**。
In these cases, we use quasi experimentation and observational causal inference techniques to infer the causal impact of the experience we are studying.
このような場合、疑似実験や観察的因果推論の手法を用いて、研究対象の経験の因果的影響を推測する。
A key aspect of a data scientist’s role in these analyses is to educate stakeholders on the caveats that come with these studies, while still providing rigorous evaluation and actionable insights, and providing structure to some otherwise ambiguous problems.
このような分析におけるデータサイエンティストの重要な役割は、これらの研究に伴う**注意点について利害関係者を教育すること**であり、同時に厳密な評価と実用的な洞察を提供し、曖昧な問題に構造を与えることである。
Here are some of the challenges and opportunities in these analyses:
これらの分析における課題と機会をいくつか挙げてみよう：

- **Treatment selection confounding**.
  治療選択の交絡。
  When users self-select into the treatment or control experience (versus the random assignment discussed in Part 2), the probability that a user ends up in each experience may depend on their usage habits with Netflix.
  第2回で議論したランダム割り当てに対して）ユーザーが自己選択でトリートメントまたはコントロールのエクスペリエンスに入る場合、ユーザーがそれぞれのエクスペリエンスに入る確率は、Netflixの利用習慣に依存する可能性がある。
  These baseline metrics are also naturally correlated with outcome metrics, such as member satisfaction, and therefore confound the effect of the observed treatment on our outcome metrics.
  これらのベースライン指標は、当然、会員の満足度などのアウトカム指標とも相関しており、したがって、観察された治療のアウトカム指標への影響を混乱させる。
  The problem is exacerbated when the treatment choice or treatment uptake varies with time, which can lead to time varying confounding.
  この問題は、治療法の選択または治療の実施が時間とともに変化する場合に悪化する。
  To deal with these cases, we use methods such as inverse propensity scores, doubly robust estimators, difference-in-difference, or instrumental variables to extract actionable causal insights, with longitudinal analyses to account for the time dependence.
  このようなケースに対処するために、私たちは逆傾向スコア、二重ロバスト推定量、差分推定量、道具変数などの手法を用いて、時間依存性を考慮した縦断的分析を行い、実用的な因果関係の洞察を抽出する。

- **Synthetic controls and structural models**.
  合成コントロールと構造モデル。
  Adjusting for confounding requires having pre-treatment covariates at the same level of aggregation as the response variable.
  交絡を調整するには、治療前の共変量が応答変数と同じ集計レベルにあることが必要である。
  However, sometimes we do not have access to that information at the level of individual Netflix members.
  しかし、ネットフリックスのメンバー個人レベルでは、その情報にアクセスできないこともある。
  In such cases, we analyze aggregate level data using synthetic controls and structural models.
  このような場合、合成コントロールと構造モデルを用いて、集計レベルのデータを分析する。

- **Sensitivity analysis**.
  感度分析。
  In the absence of true A/B testing, our analyses rely on using the available data to adjust away spurious correlations between the treatment and the outcome metrics.
  真のA/Bテストがない場合、我々の分析は、利用可能なデータを使用して、治療と結果指標の間のスプリアス相関を調整することに依存する。
  But how well we can do so depends on whether the available data is sufficient to account for all such correlations.
  しかし、それがどの程度可能かは、利用可能なデータがそのような相関関係をすべて説明するのに十分かどうかにかかっている。
  To understand the validity of our causal claims, we perform sensitivity analyses to evaluate the robustness of our findings.
  我々の因果関係の主張の妥当性を理解するために、感度分析を行い、調査結果の頑健性を評価した。
  (特定のパラメータを変動させて、metricsの動的な変動を見る、みたいな?? ただしABテストではない。)

## Messaging メッセージ

At Netflix, we are always looking for ways to help our members choose content that’s great for them.
Netflixでは、会員の皆様に最適なコンテンツを選んでいただくための方法を常に模索しています。
We do this on the Netflix product through the personalized experience we provide to every member.
ネットフリックスでは、すべての会員にパーソナライズされた体験を提供しています。
But what about other ways we can help keep members informed about new or relevant content, so they’ve something great in mind when it’s time to relax at the end of a long day?
しかし、新しいコンテンツや関連するコンテンツを会員に知らせ、長い一日の終わりにくつろぐときに、会員が何か素晴らしいものを思い浮かべられるよう、私たちが支援できる他の方法はどうだろうか？

Messaging, including emails and push notifications, is one of the key ways we keep our members in the loop.
**Eメールやプッシュ通知を含むメッセージングは、会員に常に最新情報を提供する重要な方法のひとつ**です。
The messaging team at Netflix strives to provide members with joy beyond the time when they are actively watching content.
Netflixのメッセージング・チームは、会員がコンテンツを積極的に視聴している時間以外にも喜びを提供するよう努めている。
What’s new or coming soon on Netflix? What’s the perfect piece of content that we can tell you about so you can plan “date time movie night” on the go? As a messaging team, we are also mindful of all the digital distractions in our members’ lives, so we work tirelessly to send just the right information to the right members at the right time.
Netflixの新作や近日配信予定の作品は？外出先で "映画デート "を計画するのに最適なコンテンツは？メッセージング・チームとして、私たちはまた、メンバーの生活の中にあるデジタルな注意散漫に気を配り、**適切な情報を適切なタイミングで適切なメンバーに送るために**、たゆまぬ努力を続けています。

Data scientists in this space work closely with product managers and engineers to develop messaging solutions that maximize long term satisfaction for our members.
この分野のデータ・サイエンティストは、プロダクト・マネージャーやエンジニアと緊密に連携し、会員の長期的な満足度を最大化するメッセージング・ソリューションを開発しています。
For example, we are constantly working to deliver a better, more personalized messaging experience to our members.
例えば、私たちはより良い、よりパーソナライズされたメッセージング体験を会員に提供するために常に取り組んでいます。
Each day, we predict how each candidate message would meet a members’ needs, given historical data, and the output informs what, if any, message they will receive.
毎日、**過去のデータをもとに、候補となる各メッセージがどのように会員のニーズを満たすかを予測し、その結果に基づいて、会員が受け取るメッセージの内容を決定**する。
And to ensure that innovations on our personalized messaging approach result in a better experience for our members, we use A/B testing to learn and confirm our hypotheses.
また、パーソナライズされたメッセージング・アプローチの革新が会員にとってより良い体験となるよう、私たちはA/Bテストを用いて仮説を学び、確認しています。

An exciting aspect of working as a data scientist on messaging at Netflix is that we are actively building and using sophisticated learning models to help us better serve our members.
ネットフリックスでメッセージングに関するデータサイエンティストとして働くことのエキサイティングな点は、会員により良いサービスを提供するために、洗練された学習モデルを積極的に構築し、活用していることです。
These models, based on the idea of bandits, continuously balance learning more about member messaging preferences with applying those learnings to deliver more satisfaction to our members.
**banditsの考え方に基づくこれらのモデル**は、会員のメッセージング嗜好についてより深く学ぶことと、その学びを会員により多くの満足を提供するために応用することのバランスを継続的に取っている。
It’s like a continuous A/B test with new treatments deployed all the time.
それは常に新しいtreatmentが導入される、**継続的なA/Bテストのようなもの**だ。
This framework allows us to conduct many exciting and challenging analyses without having to deploy new A/B tests every time.
このフレームワークにより、毎回新しいA/Bテストを展開することなく、多くのエキサイティングでチャレンジングな分析を実施することができる。

## Evidence Selection エビデンスの選択

When a member opens the Netflix application, our goal is to help them choose a title that is a great fit for them.
会員がNetflixのアプリケーションを開いたとき、私たちの目標は、その人にぴったりのタイトルを選んでもらうことです。
One way we do this is through constantly improving the recommendation systems that produce a personalized home page experience for each of our members.
その方法のひとつが、各メンバーにパーソナライズされたホームページ体験を提供するレコメンデーション・システムを常に改善することです。
And beyond title recommendations, we strive to select and present artwork, imagery and other visual “evidence” that is likewise personalized, and helps each member understand why a particular title is a great choice for them — particularly if the title is new to the service or unfamiliar to that member.
また、タイトルを推薦するだけでなく、アートワークや画像、その他の視覚的な "evidence"を選び、提示することで、同様にパーソナライズされ、各会員が特定のタイトルを選ぶ理由を理解できるように努めています。

Creative excellence and continuous improvements to evidence selection systems are both crucial in achieving this goal.
この目標を達成するためには、創造的な卓越性と、エビデンス選定システムの継続的な改善が不可欠である。
Data scientists working in the space of evidence selection use online experiments and offline analysis to provide robust causal insights to power product decisions in both the creation of evidence assets, such as the images that appear on the Netflix homepage, and the development of models that pair members with evidence.
ネットフリックスのホームページに掲載される画像のようなエビデンス資産の作成と、会員とエビデンスをペアリングするモデルの開発の両方において、エビデンス選択の領域で働くデータサイエンティストは、**オンライン実験とオフライン分析を使用して、製品の意思決定を後押しする強固な因果関係の洞察を提供している**。

Sitting at the intersection of content creation and product development, data scientists in this space face some unique challenges:
コンテンツ制作と製品開発の交差点に位置するこの分野のデータサイエンティストは、いくつかのユニークな課題に直面している：

### Predicting evidence performance. エビデンスのパフォーマンスを予測する

Say we are developing a new way to generate a piece of evidence, such as a trailer.
例えば、予告編のような証拠を生成する新しい方法を開発しているとしよう。
Ideally, we’d like to have some sense of the positive outcomes of the new evidence type prior to making a potentially large investment that will take time to pay off.
理想を言えば、投資回収に時間がかかるような大きな投資をする前に、新しいエビデンスタイプのポジティブな成果をある程度把握しておきたい。
Data scientists help inform investment decisions like these by developing causally valid predictive models.
データサイエンティストは、因果関係の妥当な予測モデルを開発することで、このような投資の意思決定を支援する。

### Matching members with the best evidence. 最良のエビデンスでメンバーをマッチングする。

High quality and properly selected evidence is key to a great Netflix experience for all of our members.
高品質で適切に選択された証拠品は、すべての会員にとって素晴らしいネットフリックス体験の鍵です。
While we test and learn about what types of evidence are most effective, and how to match members to the best evidence, we also work to minimize the potential downsides by investing in efficient approaches to A/B tests that allow us to rapidly stop suboptimal treatment experiences.
私たちは、どのような種類のエビデンスが最も効果的なのか、また、どのように会員を最良のエビデンスに適合させるのかをテストし、学ぶ一方で、最適とは言えない治療体験を迅速に中止させることができるA/Bテストの効率的なアプローチに投資することで、潜在的なマイナス面を最小限に抑える取り組みも行っている。

### Providing timely causal feedback on evidence development.

エビデンス開発の因果関係をタイムリーにフィードバックする。
Insights from data, including from A/B tests, are used extensively to fuel the creation of better artwork, trailers, and other types of evidence.
A/Bテストを含むデータからの洞察は、より良いアートワーク、予告編、その他のタイプの証拠を作成するために幅広く利用されている。
In addition to A/B tests, we work on developing experimental design and analysis frameworks that provide fine-grained causal inference and can keep up with the scale of our learning agenda.
A/Bテストに加えて、私たちは、きめ細かい因果推論を提供し、私たちの学習課題の規模に対応できる実験デザインと分析のフレームワークの開発に取り組んでいます。
We use contextual bandits that minimize regret in matching members to evidence, and through a collaboration with our Algorithms Engineering team, we’ve built the ability to log counterfactuals: what would a different selection policy have recommended? These data provide us with a platform to run rich offline experiments and derive causal inferences that meet our challenges and answer questions that may be slow to answer with A/B tests.
また、アルゴリズム・エンジニアリング・チームとのコラボレーションにより、反事実を記録する機能を構築しました： 別の選択方針であれば、どのような選択を推奨しただろうか？これらのデータは、リッチなオフライン実験を実行し、我々の課題を満たし、A/Bテストでは回答が遅いかもしれない質問に答える因果推論を導き出すためのプラットフォームを提供してくれる。

## Streaming ストリーミング

Now that you’ve signed up for Netflix and found something exciting to watch, what happens when you press play? Behind the scenes, Netflix infrastructure has already kicked into gear, finding the fastest way to deliver your chosen content with great audio and video quality.
Netflixに登録し、何かエキサイティングなコンテンツを見つけたら、再生ボタンを押すとどうなるのだろう？舞台裏では、Netflixのインフラがすでにギアを始動させ、選んだコンテンツを素晴らしい音質と映像品質で配信する最速の方法を見つけ出している。

The numerous engineering teams involved in delivering high quality audio and video use A/B tests to improve the experience we deliver to our members around the world.
高品質のオーディオとビデオの配信に携わる数多くのエンジニアリング・チームは、A/Bテストを駆使して、世界中のメンバーに提供する体験を向上させています。
Innovation areas include the Netflix app itself (across thousands of types of devices), encoding algorithms, and ways to optimize the placement of content on our global Open Connect distribution network.
革新的な分野には、Netflixアプリ自体（何千種類ものデバイスに対応）、エンコーディングアルゴリズム、グローバルなオープンコネクト配信ネットワークにおけるコンテンツの配置を最適化する方法などがあります。

Data science roles in this business area emphasize experimentation at scale and support for autonomous experimentation for engineering teams: how do we enable these teams to efficiently and confidently execute, analyze, and make decisions based on A/B tests? We’ll touch upon four ways that partnerships between data science and engineering teams have benefited this space.
このビジネスエリアにおけるデータサイエンスの役割は、規模に応じた実験と、エンジニアリングチームによる自律的な実験のサポートに重点を置いています： このようなチームがA/Bテストを効率的かつ自信を持って実行、分析、意思決定できるようにするにはどうすればよいのでしょうか？データサイエンスチームとエンジニアリングチームの連携がこの分野にもたらした4つのメリットについて紹介する。

Automation.
オートメーション。
As streaming experiments are numerous (thousands per year) and tend to be short lived, we’ve invested in workflow automations.
**ストリーミング実験は数が多く（年間数千件）、短命になりがちなので、ワークフローの自動化に投資してきた**。
For example, we piggyback on Netflix’s amazing tools for safe deployment of the Netflix client by integrating the experimentation platform’s API directly with Spinnaker deployment pipelines.
例えば、実験プラットフォームのAPIをSpinnakerのデプロイパイプラインに直接統合することで、Netflixクライアントを安全にデプロイするためのNetflixの素晴らしいツールにおんぶにだっこです。
This allows engineers to set up, allocate, and analyze the effects of changes they’ve made using a single configuration file.
これにより、エンジニアは、単一の設定ファイルを使用して、設定、割り当て、および行った変更の影響を分析することができます。
Taking this model even further, users can even ‘automate the automation’ by running multiple rounds of an experiment to perform sequential optimizations.
このモデルをさらに発展させれば、ユーザーは、実験の複数のラウンドを実行して連続的な最適化を実行することで、「自動化を自動化」することもできる。

Beyond average treatment effects.
平均的な治療効果を超える。
As many important streaming video and audio metrics are not well approximated by a normal distribution, we’ve found it critical to look beyond average treatment effects.
多くの重要なストリーミング・ビデオやオーディオの指標は正規分布でうまく近似できないため、平均的な治療効果以上のものを調べることが重要であることがわかりました。
To surmount these challenges, we partnered with the experimentation platform to develop and integrate high-performance bootstrap methods for compressed data, making it fast to estimate distributions and quantile treatment effects for even the most pathological metrics.
これらの課題を克服するために、我々は実験プラットフォームと提携し、圧縮データ用の高性能ブートストラップ法を開発・統合し、最も病的な測定基準でさえも、分布と分位治療効果を迅速に推定できるようにした。
Visualizing quantiles leads to novel insights about treatment effects, and these plots, now produced as part of our automated reporting, are often used to directly support high-level product decisions.
分位を可視化することで、治療効果に関する新たな洞察が得られ、現在では自動化された報告の一部として作成されるこれらのプロットは、高レベルの製品決定を直接サポートするためにしばしば使用される。

Alternatives to A/B testing.
A/Bテストに代わるもの
The Open Connect engineering team faces numerous measurement challenges.
オープンコネクトのエンジニアリングチームは、数多くの測定上の課題に直面している。
Congestion can cause interactions between treatment and control groups; in other cases we are unable to randomize due to the nature of our traffic steering algorithms.
混雑は、治療群と対照群の間に相互作用を引き起こす可能性がある。また、トラフィック・ステアリング・アルゴリズムの性質上、無作為化できない場合もある。
To address these and other challenges, we are investing heavily in quasi-experimentation methods.
こうした課題やその他の課題に対処するため、私たちは準実験的な手法に多大な投資を行っている。
We use Metaflow to pair existing infrastructure for metric definitions and data collection from our Experimentation Platform with custom analysis methods that are based on a difference-in-difference approach.
私たちはMetaflowを使って、Experimentation Platformのメトリクス定義とデータ収集のための既存のインフラと、差分アプローチに基づくカスタム分析手法をペアにしています。
This workflow has allowed us to quickly deploy self-service tools to measure changes that cannot be measured with traditional A/B testing.
このワークフローにより、従来のA/Bテストでは測定できなかった変化を測定するためのセルフサービスツールを迅速に導入できるようになった。
Additionally, our modular approach has made it easy to scale quasi-experiments across Open Connect use cases, allowing us to swap out data sources or analysis methods depending on each team’s individual needs.
さらに、当社のモジュラー・アプローチにより、オープンコネクトのユースケース全体で準実験を簡単にスケールアップできるようになりました。

Support for custom metrics and dimensions.
カスタムメトリクスとディメンションをサポート。
Last, we’ve developed a (relatively) frictionless path that allows all experimenters (not just data scientists) to create custom metrics and dimensions in a snap when they are needed.
最後に、（データ・サイエンティストだけでなく）すべての実験者が、必要なときにすぐにカスタム測定基準やディメンションを作成できるように、（比較的）摩擦の少ない経路を開発しました。
Anything that can be logged can be quickly passed to the experimentation platform, analyzed, and visualized alongside the long-lived quality of experience metrics that we consider for all tests in this domain.
ログに記録できるものはすべて、実験プラットフォームに素早く渡し、分析し、この領域のすべてのテストについて考慮する長期的な体験品質メトリクスと一緒に可視化することができる。
This allows our engineers to use paved paths to ask and answer more precise questions, so they can spend less time head-scratching and more time testing out exciting ideas.
これにより、エンジニアは舗装された経路を使ってより的確な質問と回答ができるようになり、頭を悩ませる時間を減らしてエキサイティングなアイデアを試す時間を増やすことができる。

## Scaling experimentation and investing in infrastructure 実験の拡大とインフラへの投資

To support the scale and complexity of the experimentation program at Netflix, we’ve invested in building out our own experimentation platform (referred to as “XP” internally).
ネットフリックスの実験プログラムの規模と複雑さをサポートするため、私たちは独自の実験プラットフォーム（社内では「XP」と呼ばれている）の構築に投資してきた。
Our XP provides robust and automated (or semi automated) solutions for the full lifecycle of experiments, from experience management through to analysis, and meets the data scale produced by a high throughput of large tests.
当社のXPは、経験管理から分析に至るまで、実験の全ライフサイクルに堅牢で自動化された（または半自動化された）ソリューションを提供し、大規模テストの高スループットによって生成されるデータ規模に対応します。

XP provides a framework that allows engineering teams to define sets of test treatment experiences in their code, and then use these to configure an experiment.
XPは、エンジニアリング・チームがコードにテスト処理経験のセットを定義し、それを使って実験を構成することを可能にするフレームワークを提供する。
The platform then randomly selects members (or other units we might experiment on, like playback sessions) to assign to experiments, before randomly assigning them to an experience within each experiment (control or one of the treatment experiences).
その後、プラットフォームは、実験に割り当てるメンバー（または再生セッションのような、実験に割り当てる可能性のある他のユニット）をランダムに選択し、各実験内の経験（コントロールまたは治療経験の1つ）にランダムに割り当てる。
Calls by Netflix services to XP then ensure that the correct experiences are delivered, based on which tests a member is part of, and which variants within those tests.
ネットフリックスのサービスからXPへの呼び出しは、メンバーがどのテストに参加しているか、またそのテスト内のどのバリアントに属しているかに基づいて、正しいエクスペリエンスが配信されるようにする。
Our data engineering systems collect these test metadata, and then join them with our core data sets: logs on how members and non members interact with the service, logs that track technical metrics on streaming video delivery, and so forth.
私たちのデータエンジニアリングシステムは、これらのテスト用メタデータを収集し、コアデータセットと結合します： 会員と非会員がどのようにサービスを利用するかに関するログ、ストリーミング・ビデオ配信に関する技術的指標を追跡するログなどです。
These data then flow through automated analysis pipelines and are reported in ABlaze, the front end for reporting and configuring experiments at Netflix.
これらのデータは、自動化された分析パイプラインを経て、Netflixでの実験の報告や設定のためのフロントエンドであるABlazeで報告される。
Aligned with Netflix culture, results from tests are broadly accessible to everyone in the company, not limited to data scientists and decision makers.
ネットフリックスの文化に沿い、テスト結果はデータサイエンティストや意思決定者に限らず、社内の誰もが広くアクセスできる。

The Netflix XP balances execution of the current experimentation program with a focus on future-looking innovation.
ネットフリックスのXPは、現在の実験プログラムの実行と、将来を見据えたイノベーションへの注力のバランスをとっている。
It’s a virtuous flywheel, as XP aims to take whatever is pushing the boundaries of our experimentation program this year and turn it into next year’s one-click solution.
XPは、今年の実験プログラムの限界に挑戦しているものは何でも、来年のワンクリック・ソリューションに変えることを目指しているのだから。
That may involve developing new solutions for allocating members (or other units) to experiments, new ways of tracking conflicts between tests, or new ways of designing, analyzing, and making decisions based on experiments.
そのためには、実験にメンバー（または他のユニット）を割り当てるための新しいソリューションや、実験間の競合を追跡する新しい方法、あるいは実験に基づく設計、分析、意思決定の新しい方法を開発する必要があるかもしれない。
For example, XP partners closely with engineering teams on feature flagging and experience delivery.
例えば、XPはエンジニアリング・チームと緊密に連携し、機能フラグ立てやエクスペリエンス・デリバリーを行う。
In success, these efforts provide a seamless experience for Netflix developers that fully integrates experimentation into the software development lifecycle.
これらの取り組みが成功すれば、ネットフリックスの開発者にシームレスなエクスペリエンスを提供し、ソフトウェア開発ライフサイクルに実験を完全に統合することができる。

For analyzing experiments, we’ve built the Netflix XP to be both democratized and modular.
実験を分析するために、私たちはNetflix XPを民主化され、モジュール化されるように構築した。
By democratized, we mean that data scientists (and other users) can directly contribute metrics, causal inference methods for analyzing tests, and visualizations.
民主化とは、データサイエンティスト（およびその他のユーザー）が、メトリクス、テストを分析するための因果推論手法、可視化などを直接提供できることを意味する。
Using these three modules, experimenters can compose flexible reports, tailored to their tests, that flow through to both our frontend UI and a notebook environment that supports ad hoc and exploratory analysis.
これら3つのモジュールを使用することで、実験者はテストに合わせた柔軟なレポートを作成することができ、フロントエンドのUIと、アドホック分析や探索的分析をサポートするノートブック環境の両方に流すことができる。

This model supports rapid prototyping and innovation as we abstract away engineering concerns so that data scientists can contribute code directly to our production experimentation platform — without having to become software engineers themselves.
このモデルは、データ・サイエンティストがソフトウェア・エンジニアになることなく、本番の実験プラットフォームに直接コードを提供できるように、エンジニアリングの懸念を抽象化することで、迅速なプロトタイピングとイノベーションをサポートします。
To ensure that platform capabilities are able to support the required scale (number and size of tests) as analysis methods become more complex and computationally intensive, we’ve invested in developing expertise in performant and robust Computational Causal Inference software for test analysis.
分析手法が複雑化し、計算量が多くなるにつれて、プラットフォーム機能が必要な規模（テストの数と規模）をサポートできるようにするため、当社は、テスト分析用のパフォーマンスと堅牢性を備えた計算原因推論ソフトウェアの専門知識の開発に投資してきました。

It takes a village to build an experimentation platform: software engineers to build and maintain the backend engineering infrastructure; UI engineers to build out the ABlaze front end that is used to manage and analyze experiments; data scientists with expertise in causal inference and numerical computing to develop, implement, scale, and socialize cutting edge methodologies; user experience designers who ensure our products are accessible to our stakeholders; and product managers who keep the platform itself innovating in the right direction.
実験プラットフォームの構築には村が必要である： バックエンドのエンジニアリング・インフラを構築し維持するソフトウェア・エンジニア、実験の管理と分析に使用されるABlazeのフロントエンドを構築するUIエンジニア、最先端の方法論を開発し、実装し、拡張し、社会化するための因果推論と数値計算の専門知識を持つデータ・サイエンティスト、私たちの製品がステークホルダーにとって利用しやすいものであることを保証するユーザー・エクスペリエンス・デザイナー、そしてプラットフォーム自体を正しい方向に革新し続けるプロダクト・マネージャーです。
It’s an incredibly multidisciplinary endeavor, and positions on XP provide opportunities to develop broad skill sets that span disciplines.
XPは非常に学際的な取り組みであり、XPのポジションは分野を超えた幅広いスキルを身につける機会を提供する。
Because experimentation is so pervasive at Netflix, those working on XP are exposed to challenges, and get to collaborate with colleagues, from all corners of Netflix.
ネットフリックスでは実験が非常に浸透しているため、XPに携わる者は、ネットフリックスのあらゆる場所にいる同僚と協力し、課題に取り組むことができる。
It’s a great way to learn broadly about ‘how Netflix works’ from a variety of perspectives.
Netflixの仕組み』を様々な角度から幅広く学ぶことができる。

## Summary 要約

At Netflix, we’ve invested in data science teams that use A/B tests, other experimentation paradigms, and the scientific method more broadly, to support continuous innovation on our product offerings for current and future members.
Netflixでは、A/Bテストやその他の実験パラダイム、より広範な科学的手法を活用する**データサイエンスチームに投資**し、現在および将来の会員向けに提供する製品の継続的なイノベーションをサポートしています。
In tandem, we’ve invested in building out an internal experimentation platform (XP) that supports the scale and complexity of our experimentation and learning program.
それと並行して、私たちは実験と学習プログラムの規模と複雑さをサポートする**社内実験プラットフォーム（XP）の構築に投資**してきました。

In practice, the dividing line between these two investments is blurred and we encourage collaboration between XP and business-oriented data scientists, including through internal events like A/B Experimentation Workshops and Causal Inference Summits.
実際には、この2つの投資の境界線は曖昧であり、A/B実験ワークショップや因果推論サミットなどの社内イベントを通じて、XPとビジネス志向のデータサイエンティストとのコラボレーションを奨励している。
To ensure that experimentation capabilities at Netflix evolve to meet the on-the-ground needs of experimentation practitioners, we are intentional in ensuring that the development of new measurement and experiment management capabilities, and new software systems to both enable and scale research, is a collaborative partnership between XP and experimentation practitioners.
ネットフリックスの実験能力が、実験実務者の現場のニーズを満たすように進化することを確実にするため、私たちは、新しい測定・実験管理能力、および研究を可能にし、規模を拡大するための新しいソフトウェアシステムの開発が、XPと実験実務者の協力的パートナーシップであることを意図しています。
In addition, our intentionally collaborative approach provides great opportunities for folks to lead and contribute to high-impact projects that deliver new capabilities, spanning engineering, measurement, and internal product development.
さらに、意図的に協力的なアプローチをとっているため、エンジニアリング、測定、社内製品開発など、新たな能力を提供するインパクトの大きいプロジェクトをリードし、貢献する絶好の機会を提供しています。
And because of the strategic value Netflix places on experimentation, these collaborative efforts receive broad visibility, including from our executives.
また、ネットフリックスは実験に戦略的価値を置いているため、このような協力的な取り組みは、経営陣を含め、広く認知されている。

So far, this series has covered the why, what and how of A/B testing, all of which are necessary to reap the benefits of an experimentation-based approach to product development.
これまでこのシリーズでは、A/Bテストの「なぜ」「何を」「どのように」行うかを取り上げてきた。これらはすべて、製品開発における実験ベースのアプローチのメリットを享受するために必要なものである。
But without a little magic, these basics are still not enough.
しかし、ちょっとした魔法がなければ、これらの基本はまだ十分ではない。
That magic will be the focus of the next and final post (now available) in this series: the learning and experimentation culture that pervades Netflix.
その魔法は、このシリーズの次回最終回（現在公開中）の焦点となる： Netflixに浸透している学習と実験の文化。
Follow the Netflix Tech Blog to stay up to date.
最新情報はNetflix Tech Blogをフォローしてください。
