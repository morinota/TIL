## link リンク

https://netflixtechblog.com/netflix-a-culture-of-learning-394bc7d0f94c
https://netflixtechblog.com/netflix-a-culture-of-learning-394bc7d0f94c

# Netflix: A Culture of Learning ネットフリックス 学びの文化

This is the last post in an overview series on experimentation at Netflix.
ネットフリックスの実験に関する概要シリーズの最終回である。
Need to catch up? Earlier posts covered the basics of A/B tests (Part 1 and Part 2 ), core statistical concepts (Part 3 and Part 4), how to build confidence in a decision (Part 5), and the the role of Experimentation and A/B testing within the larger Data Science and Engineering organization at Netflix (Part 6).
追いつく必要がありますか？以前の投稿では、A/Bテストの基本（パート1およびパート2）、中核となる統計的概念（パート3およびパート4）、意思決定の信頼性を構築する方法（パート5）、Netflixの大規模なデータサイエンスおよびエンジニアリング組織における実験とA/Bテストの役割（パート6）をカバーしました。

Earlier posts in this series covered the why, what and how of A/B testing, all of which are necessary to reap the benefits of experimentation for product development.
このシリーズの以前の記事では、A/Bテストの理由、内容、方法について説明した。
But without a little magic, these basics are still not enough.
しかし、ちょっとした魔法がなければ、これらの基本はまだ十分ではない。

The secret sauce that turns the raw ingredients of experimentation into supercharged product innovation is culture.
**実験の原材料を超高速の製品革新に変える秘密のソースは、文化**である。
There are never any shortcuts when developing and growing culture, and fostering a culture of experimentation is no exception.
文化を発展させ成長させることに近道はなく、実験文化の育成も例外ではない。
Building leadership buy-in for an approach to learning that emphasizes A/B testing, building trust in the results of tests, and building the technical capabilities to execute experiments at scale all take time — particularly within an organization that’s new to these ideas.
A/Bテストを重視する学習へのアプローチに対するリーダーシップの賛同を得ること、テストの結果に対する信頼を築くこと、実験を大規模に実行するための技術的能力を構築すること、これらすべてに時間がかかる。
But the pay-offs of using experimentation and the virtuous cycle of product development via the scientific method are well worth the effort.
しかし、科学的手法による実験と製品開発の好循環を利用することの見返りは、努力に十分見合うものである。
Our colleagues at Microsoft have shared thoughtful publications on how to Kickstart the Experimentation Flywheel and build a culture of experimentation, while their “Crawl, Walk, Run, Fly” model is a great tool for assessing the maturity of an experimentation practice.
マイクロソフトの同僚たちは、実験フライホイールをキックスタートさせ、実験文化を構築する方法について、思慮深い出版物を共有している。また、彼らの「クロール、ウォーク、ラン、フライ」モデルは、実験プラクティスの成熟度を評価するための素晴らしいツールである。

At Netflix, we’ve been leveraging experimentation and the scientific method for decades, and are fortunate to have a mature experimentation culture.
Netflixでは、実験と科学的手法を何十年も活用しており、幸運にも成熟した実験文化を持っている。
There is broad buy-in across the company, including from the C-Suite, that, whenever possible, results from A/B tests or other causal inference approaches are near-requirements for decision making.
可能な限り、A/Bテストやその他の因果推論アプローチから得られた結果を、意思決定のための必要条件に近いものとすることが、経営幹部を含む全社的な幅広い賛同を得ている。
We’ve also invested in education programs to up-level company-wide understanding of how we use A/B tests as a framework for product development.
また、製品開発のフレームワークとしてA/Bテストをどのように活用しているかについて、全社的な理解を高めるための教育プログラムにも投資してきました。
In fact, most of the material from this blog series has been adapted from our internal Experimentation 101 and 201 classes, which are open to anyone at Netflix.
実際、このブログシリーズのネタのほとんどは、Netflixの誰でも参加できる社内クラス「Experimentation 101」と「201」から転用したものだ。

## Netflix is organized to learn ネットフリックスは学ぶために組織されている

As a company, Netflix is organized to emphasize the importance of learning from data, including from A/B tests.
ネットフリックスは企業として、A/Bテストを含め、データから学ぶことの重要性を強調する組織である。
Our Data and Insights organization has teams that partner with all corners of the company to deliver a better experience to our members, from understanding content preferences around the globe to delivering a seamless customer support experience.
データ＆インサイト部門は、世界中のコンテンツ嗜好の把握からシームレスなカスタマー・サポート体験の提供まで、会員により良い体験をお届けするために、社内のあらゆる部署と提携しています。
We use qualitative and quantitative consumer research, analytics, experimentation, predictive modeling, and other tools to develop a deep understanding of our members.
私たちは、質的・量的消費者調査、分析、実験、予測モデリング、その他のツールを駆使して、会員を深く理解しています。
And we own the data pipelines that power everything from executive-oriented dashboards to the personalization systems that help connect each Netflix member with content that will spark joy for them.
そして、経営陣向けのダッシュボードから、ネットフリックスの各会員に喜びをもたらすコンテンツを提供するパーソナライゼーション・システムまで、すべてを支えるデータ・パイプラインを所有しています。
This data-driven mindset is ubiquitous at all levels of the company, and the Data and Insights organization is represented at the highest echelon of Netflix Leadership.
このようなデータ主導の考え方は社内のあらゆる階層に浸透しており、データ＆インサイト部門はネットフリックス・リーダーシップの最上位に位置しています。

As discussed in Part 6, there are experimentation and causal inference focussed data scientists who collaborate with product innovation teams across Netflix.
第6回で説明したように、ネットフリックスの製品イノベーションチームと協力する、実験と因果推論に焦点を当てたデータサイエンティストがいる。
These data scientists design and execute tests to support learning agendas and contribute to decision making.
これらのデータサイエンティストは、学習課題をサポートし、意思決定に貢献するためのテストを設計・実行する。
By diving deep into the details of single test results, looking for patterns across tests, and exploring other data sources, these Netflix data scientists build up domain expertise about aspects of the Netflix experience and become valued partners to product managers and engineering leaders.
1つのテスト結果の詳細に深く入り込み、テスト全体のパターンを探し、他のデータソースを探索することで、Netflixのデータサイエンティストは、Netflixの体験の側面に関する専門知識を蓄積し、プロダクトマネージャーやエンジニアリングリーダーの大切なパートナーになります。
Data scientists help shape the evolution of the Netflix product through opportunity sizing and identifying areas ripe for innovation, and frequently propose hypotheses that are subsequently tested.
データ・サイエンティストは、ビジネスチャンスを見極め、イノベーションが必要な領域を特定することで、ネットフリックスの製品の進化を形作る手助けをし、頻繁に仮説を提案し、その後に検証を行う。

We’ve also invested in a broad and flexible experimentation platform that allows our experimentation program to scale with the ambitions of the company to learn more and better serve Netflix members.
私たちはまた、より多くのことを学び、ネットフリックスの会員により良いサービスを提供するという会社の野心に合わせて実験プログラムを拡張できるよう、広範で柔軟な実験プラットフォームに投資してきました。
Just as the Netflix product itself has evolved over the years, our approach to developing technologies to support experimentation at scale continues to evolve.
ネットフリックスの製品そのものが年々進化しているように、スケールの大きな実験をサポートするテクノロジーを開発するアプローチも進化し続けている。
In fact, we’ve been working to improve experimentation platform solutions at Netflix for more than 20 years — our first investments in tooling to support A/B tests came way back in 2001.
実際、Netflixでは20年以上前から実験プラットフォーム・ソリューションの改善に取り組んでおり、A/Bテストをサポートするツールへの最初の投資は2001年に遡る。

## Learning and experimentation are ubiquitous across Netflix 学習と実験はネットフリックスのいたるところで行われている。

Netflix has a unique internal culture that reinforces the use of experimentation and the scientific method as a means to deliver more joy to all of our current and future members.
ネットフリックスには、現在そして未来のすべての会員にさらなる喜びを提供する手段として、実験と科学的手法の活用を強化するユニークな社内文化があります。
As a company, we aim to be curious, and to truly and honestly understand our members around the world, and how we can better entertain them.
会社として、私たちは好奇心旺盛であること、そして世界中の会員を本当に誠実に理解すること、そしてどうすれば彼らをより良く楽しませることができるかを目指している。
We are also open minded, knowing that great ideas can come from unlikely sources.
また、私たちはオープンマインドであり、素晴らしいアイデアは思いもよらないところから生まれるものだと知っている。
There’s no better way to learn and make great decisions than to confirm or falsify ideas and hypotheses using the power of rigorous testing.
学習し、優れた決断を下すには、厳格なテストの力を使ってアイデアや仮説を確認したり、偽証したりすることに勝る方法はない。
Openly and candidly sharing test results allows everyone at Netflix to develop intuition about our members and ideas for how we can deliver an ever better experience to them — and then the virtuous cycle starts again.
テスト結果をオープンに、率直に共有することで、ネットフリックスの全員がメンバーに関する直感を養い、どうすればより良い体験を提供できるかを考え、そしてまた好循環が始まる。

In fact, Netflix has so many tests running on the product at any given time that a member may be simultaneously allocated to several tests.
実際、ネットフリックスは常時多くのテストを実施しており、1人のメンバーが複数のテストに同時に割り振られることもある。
There is not one Netflix product: at any given time, we are testing out a large number of product variants, always seeking to learn more about how we can deliver more joy to our current members and attract new members.
ネットフリックスの商品はひとつではありません： Netflixは、常に多くの製品バリエーションをテストし、現在の会員により多くの喜びを提供し、新しい会員を惹きつけるにはどうすればよいかを常に追求しています。
Some tests, such as the Top 10 list, are easy for users to notice, while others, such as changes to the personalization and search systems or how Netflix encodes and delivers streaming video, are less obvious.
トップ10リストのようにユーザーが気づきやすいテストもあれば、パーソナライズや検索システムの変更、Netflixがストリーミングビデオをエンコードして配信する方法の変更など、あまり目立たないものもある。

At Netflix, we are not afraid to test boldly, and to challenge fundamental or long-held assumptions.
Netflixでは、大胆なテストを恐れず、基本的な前提や長年の前提に挑戦します。
The Top 10 list is a great example of both: it’s a large and noticeable change that surfaces a new type of evidence on the Netflix product.
トップ10リストはその両方の好例である： それは、ネットフリックスの製品に関する新しいタイプの証拠を表面化させる、大規模かつ顕著な変更である。
Large tests like this can open up whole new areas for innovation, and are actively socialized and debated within the company (see below).
このような大規模なテストは、革新のためのまったく新しい分野を切り開く可能性があり、社内で活発に社会化され、議論される（下記参照）。
On the other end of the spectrum, we also run tests on much smaller scales in order to optimize every aspect of the product.
その一方で、製品のあらゆる面を最適化するために、もっと小規模なテストも行っている。
A great example is the testing we do to find just the right text copy for every aspect of the product.
その好例が、製品のあらゆる側面に適切なテキストコピーを見つけるために行うテストだ。
By the numbers, we run far more of these smaller and less noticeable tests, and we invest in end-to-end infrastructure that simplifies their execution, allowing product teams to rapidly go from hypothesis to test to roll out of the winning experience.
そして、その実行を簡素化するエンド・ツー・エンドのインフラに投資し、製品チームが仮説からテスト、勝利体験のロールアウトまでを迅速に行えるようにしている。
As an example, the Shakespeare project provides an end-to-end solution for rapid text copy testing that integrates with the centralized Netflix experimentation platform.
一例として、シェイクスピア・プロジェクトは、集中型のネットフリックス実験プラットフォームと統合した、迅速なテキスト・コピー・テストのためのエンド・ツー・エンドのソリューションを提供している。
More generally, we are always on the lookout for new areas that can benefit from experimentation, or areas where additional methodology or tooling can produce new or faster learnings.
より一般的に言えば、私たちは常に、実験から利益を得ることができる新しい分野や、追加的な方法論やツールによって新たな、あるいはより迅速な学びを生み出すことができる分野に目を光らせている。

## Debating tests and the importance of humility ディベートテストと謙虚さの重要性

Netflix has mature operating mechanisms to debate, make, and socialize product decisions.
ネットフリックスには、商品決定を議論し、決定し、社会化するための成熟した運営メカニズムがある。
Netflix does not make decisions by committee or by seeking consensus.
ネットフリックスは、委員会やコンセンサスを求めて意思決定を行うことはない。
Instead, for every significant decision there is a single “Informed Captain” who is ultimately responsible for making a judgment call after digesting relevant data and input from colleagues (including dissenting perspectives).
その代わり、重要な決断を下す際には、関連データと同僚からの意見（反対意見も含む）を咀嚼した上で、最終的な判断を下す責任を負う "インフォームド・キャプテン "が一人いる。
Wherever possible, A/B test results or causal inference studies are an expected input to this decision making process.
可能な限り、A/Bテストの結果や因果推論研究は、この意思決定プロセスへのインプットとして期待される。

In fact, not only are test results expected for product decisions — it’s expected that decisions on investment areas for innovation and testing, test plans for major innovations, and results of major tests are all summarized in memos, socialized broadly, and actively debated.
実際、製品の決定にはテスト結果が期待されるだけでなく、技術革新とテストのための投資分野の決定、主要な技術革新のテスト計画、主要なテストの結果がすべてメモにまとめられ、広く社会化され、活発に議論されることが期待されている。
The forums where these debates take place are broadly accessible, ensuring a diverse set of viewpoints provide feedback on test designs and results, and weigh in on decisions.
このような討論が行われる場は広くアクセス可能であり、多様な視点からの試験設計や結果についてのフィードバックや、決定事項についての意見交換が行われる。
Invites for these forums are open to anyone who is interested, and the price of admission is reading the memo.
このようなフォーラムへの招待は、興味のある人なら誰でも可能で、入場料はメモを読むことだ。
Despite strong executive attendance, there’s a notable lack of hierarchy in these forums, as we all seek to be led by the data.
エグゼクティブの出席が多いにもかかわらず、このようなフォーラムには上下関係がない。

Netflix data scientists are active and valued participants in these forums.
ネットフリックスのデータサイエンティストは、こうしたフォーラムに積極的に参加し、高く評価されている。
Data scientists are expected to speak for the data, both what can and what cannot be concluded from experimental results, the pros and cons of different experimental designs, and so forth.
データサイエンティストは、実験結果から何が結論づけられ、何が結論づけられないか、異なる実験デザインの長所と短所など、データを代弁することが期待されている。
Although they are not informed captains on product decisions, data scientists, as interpreters of the data, are active contributors to key product decisions.
データ・サイエンティストは、製品の意思決定におけるキャプテンではないが、データの解釈者として、製品の重要な意思決定に積極的に貢献する。

Product evolution via experimentation can be a humbling experience.
実験による製品の進化は、屈辱的な経験かもしれない。
At Netflix, we have experts in every discipline required to develop and evolve the Netflix service (product managers, UI/UX designers, data scientists, engineers of all types, experts in recommendation systems and streaming video optimization — the list goes on), who are constantly coming up with novel hypotheses for how to improve Netflix.
Netflixには、Netflixサービスの開発・進化に必要なあらゆる分野の専門家（プロダクトマネージャー、UI/UXデザイナー、データサイエンティスト、あらゆるタイプのエンジニア、レコメンドシステムやストリーミングビデオ最適化の専門家など、数え上げればきりがない）がおり、Netflixを改善するための斬新な仮説を常に打ち出している。
But only a small percentage of our ideas turn out to be winners in A/B tests.
しかし、A/Bテストで勝者となるのは、私たちのアイデアのごく一部にすぎない。
That’s right: despite our broad expertise, our members let us know, through their actions in A/B tests, that most of our ideas do not improve the service.
その通りです： 私たちの幅広い専門知識にもかかわらず、会員たちはA/Bテストでの行動を通じて、私たちのアイデアのほとんどがサービスを改善しないことを私たちに教えてくれました。
We build and test hundreds of product variants each year, but only a small percentage end up in production and rolled out to the more than 200 million Netflix members around the world.
私たちは毎年、何百もの製品バリエーションを構築し、テストしていますが、最終的に製品化され、世界中の2億人以上のNetflix会員に展開されるのはごく一部です。

The low win rate in our experimentation program is both humbling and empowering.
私たちの実験プログラムにおける勝率の低さは、謙虚であると同時に力を与えてくれる。
It’s hard to maintain a big ego when anyone at the company can look at the data and see all the big ideas and investments that have ultimately not panned out.
会社の誰もがデータを見ることができ、最終的にうまくいかなかった大きなアイデアや投資を見ることができるとき、大きなエゴを維持するのは難しい。
But nothing proves the value of decision making through experimentation like seeing ideas that all the experts were bullish on voted down by member actions in A/B tests — and seeing a minor tweak to a sign up flow turn out to be a massive revenue generator.
しかし、専門家の誰もが強気だったアイデアが、A/Bテストで会員の行動によって否決されるのを見ること、そして、登録フローにほんの少し手を加えただけで、大規模な収益を生み出すことが判明するのを見ることほど、実験による意思決定の価値を証明するものはない。

At Netflix, we do not view tests that do not produce winning experience as “failures.” When our members vote down new product experiences with their actions, we still learn a lot about their preferences, what works (and does not work!) for different member cohorts, and where there may, or may not be, opportunities for innovation.
ネットフリックスでは、勝利体験が得られなかったテストを "失敗 "とは見なさない。メンバーの行動によって新しい製品体験が否決されたとしても、私たちはメンバーの嗜好や、異なるメンバー層にとって何が効果的か（そして効果的でないか！）、イノベーションの機会がどこにありそうで、あるいはなさそうであるかについて多くを学ぶことができます。
Combining learnings from tests in a given innovation area, such as the Mobile UI experience, helps us paint a more complete picture of the types of experiences that do and do not resonate with our members, leading to new hypotheses, new tests, and, ultimately, a more joyful experience for our members.
モバイルUIエクスペリエンスなど、特定のイノベーション領域におけるテストから学んだことを組み合わせることで、会員に響くエクスペリエンスと響かないエクスペリエンスのタイプについて、より完全なイメージを描くことができ、新たな仮説、新たなテスト、そして最終的には会員にとってより楽しいエクスペリエンスにつながります。
And as our member base continues to grow globally, and as consumer preferences and expectations continue to evolve, we also revisit ideas that were unsuccessful when originally tested.
また、会員数が世界的に増え続け、消費者の嗜好や期待が進化し続けるなか、当初テストしたときには失敗したアイデアも再検討している。
Sometimes there are signals from the original analysis that suggest now is a better time for that idea, or that it will provide value to some of our newer member cohorts.
時には、当初の分析から、そのアイデアは今がより良い時期であると示唆するシグナルがあったり、新しいメンバー・コーホートの一部に価値をもたらすと示唆するシグナルがあったりする。

Because Netflix tests all ideas, and because most ideas are not winners, our culture of experimentation democratizes ideation.
Netflixはすべてのアイデアをテストし、ほとんどのアイデアは勝者にならないため、私たちの実験文化はアイデアの民主化を実現する。
Product managers are always hungry for ideas, and are open to innovative suggestions coming from anyone in the company, regardless of seniority or expertise.
プロダクトマネージャーは常にアイデアに飢えており、年功序列や専門知識に関係なく、社内の誰からの革新的な提案にもオープンである。
After all, we’ll test anything before rolling it out to the member base, and even the experts have low success rates! We’ve seen time and time again at Netflix that product suggestions large and small that arise from engineers, data scientists, even our executives, can result in unexpected wins.
結局のところ、私たちはメンバーに展開する前に何でもテストしますし、専門家でさえ成功率は低いのです！ネットフリックスでは、エンジニアやデータサイエンティスト、さらには経営幹部から生まれる大小さまざまな製品提案が、思いもよらない勝利をもたらすことがあることを、何度も何度も目の当たりにしてきました。

A culture of experimentation allows more voices to contribute to ideation, and far, far more voices to help inform decision making.
実験的な文化があれば、より多くの声がアイデアに貢献し、はるかに多くの声が意思決定に反映される。
It’s a way to get the best ideas from everyone working on the product, and to ensure that the innovations that are rolled out are vetted and approved by members.
これは、製品に携わる全員から最高のアイデアを得るための方法であり、展開される革新的技術がメンバーによって吟味され、承認されることを保証するための方法である。

A better product for our members and an internal culture that is humble and values ideas and evidence: experimentation is a win-win proposition for Netflix.
会員にとってより良い製品、そして謙虚でアイデアと証拠を大切にする社内文化： 実験は、NetflixにとってWin-Winの提案です。

## Emerging research areas 新たな研究分野

Although Netflix has been running experiments for decades, we’ve only scratched the surface relative to what we want to learn and the capabilities we need to build to support those learning ambitions.
Netflixは何十年も実験を続けているが、私たちが何を学びたいのか、そしてそのような学習意欲をサポートするために構築する必要がある能力については、まだ表面しか見ていない。
There are open challenges and opportunities across experimentation and causal inference at Netflix: exploring and implementing new methodologies that allow us to learn faster and better; developing software solutions that support research; evolving our internal experimentation platform to better serve a growing user community and ever increasing size and throughput of experiments.
ネットフリックスには、実験と因果推論に関するオープンな課題と機会がある： より速く、より良い学習を可能にする新しい方法論の探求と導入、研究をサポートするソフトウェアソリューションの開発、ユーザーコミュニティの拡大と実験の規模とスループットの増加により良いサービスを提供するための社内実験プラットフォームの進化。
And there’s a continuous focus on evolving and growing our experimentation culture through internal events and education programs, as well as external contributions.
また、社内のイベントや教育プログラム、社外への貢献を通じて、実験文化を進化させ、成長させることに継続的に焦点を当てている。
Here are a few themes that are on our radar:
私たちが注目しているテーマをいくつか紹介しよう：

### Increasing velocity: beyond fixed time horizon experimentation. 速度の増加： 固定時間地平線の実験を超える。

This series has focused on fixed time horizon tests: sample sizes, the proportion of traffic allocated to each treatment experience, and the test duration are all fixed in advance.
このシリーズでは、固定時間地平テストに焦点を当ててきた： サンプルサイズ、各処置経験に割り当てられるトラフィックの割合、およびテスト期間はすべて事前に固定されている。
In principle, the data are examined only once, at the conclusion of the test.
原則として、データの検査はテストの終了時に一度だけ行われる。
This ensures that the false positive rate (see Part 3) is not increased by peeking at the data numerous times.
これにより、何度もデータを覗き見することによって偽陽性率（第3回参照）が高まることがない。
In practice, we’d like to be able to call tests early, or to adapt how incoming traffic is allocated as we learn incrementally about which treatments are successful and which are not, in a way that preserves the statistical properties described earlier in this series.
実際には、早い段階でテストを呼び出したり、どの治療が成功し、どの治療が失敗したかを段階的に学びながら、このシリーズで前述した統計的特性を維持する方法で、受信トラフィックの割り当て方法を適応させたりできるようにしたい。
To enable these benefits, Netflix is investing in sequential experimentation that permits for valid decision making at any time, versus waiting until a fixed time has passed.
このようなメリットを実現するため、ネットフリックスは、一定の時間が経過するまで待つのではなく、いつでも有効な意思決定ができるよう、逐次的な実験に投資している。
These methods are already being used to ensure safe deployment of Netflix client applications.
これらの方法は、ネットフリックスのクライアントアプリケーションを安全に配備するためにすでに使われている。
We are also investing in support for experimental designs that adaptively allocate traffic throughout the test towards promising treatments.
私たちはまた、有望な治療法に向けて、試験を通じてトラフィックを適応的に割り当てる実験デザインのサポートにも投資している。
The goal of both these efforts is the same: more rapid identification of experiences that benefit members.
この2つの取り組みの目標は同じである： 会員にとって有益な経験をより迅速に特定することである。

### Scaling support for quasi experimentation and causal inference. 準実験と因果推論のスケーリングサポート。

Netflix has learned an enormous amount, and dramatically improved almost every aspect of the product, using the classic online A/B tests, or randomized controlled trials, that have been the focus of this series.
ネットフリックスは、本連載の焦点である古典的なオンラインA/Bテスト（無作為化比較試験）を用いて、膨大な量を学び、製品のほとんどすべての側面を劇的に改善した。
But not every business question is amenable to A/B testing, whether due to an inability to randomize at the individual level, or due to factors, such as spillover effects, that may violate key assumptions for valid causal inference.
しかし、個人レベルでの無作為化が不可能であったり、有効な因果関係を推論するための重要な仮定に反するような波及効果などの要因があったりするため、すべてのビジネス上の疑問がA/Bテストに適しているわけではない。
In these instances, we often rely on the rigorous evaluation of quasi-experiments, where units are not assigned to a treatment or control condition by a random process.
このような場合、多くの場合、準実験の厳密な評価に頼ることになるが、そこでは、無作為なプロセスによって治療条件や対照条件にユニットが割り当てられていない。
But the term “quasi-experimentation” itself covers a broad category of experimental design and methodological approaches that differ between the myriad academic backgrounds represented by the Netflix data science community.
しかし、「準実験」という言葉自体が、ネットフリックス・データサイエンス・コミュニティに代表される無数の学術的背景の間で異なる実験デザインと方法論的アプローチの幅広いカテゴリーをカバーしている。
How can we synthesize best practices across domains and scale our approach to enable more colleagues to leverage quasi-experimentation?
より多くの同僚が準実験を活用できるようにするためには、どのようにすれば領域横断的なベストプラクティスを統合し、アプローチの規模を拡大できるのだろうか？

Our early successes in this space have been driven by investments in knowledge sharing across business verticals, education, and enablement via tooling.
この分野での私たちの初期の成功は、事業部門を超えた知識の共有、教育、ツールによる能力開発への投資によってもたらされた。
Because quasi-experiment use cases span many domains at Netflix, identifying common patterns has been a powerful driver in developing shared libraries that scientists can use to evaluate individual quasi-experiments.
準実験のユースケースはネットフリックスの多くのドメインにまたがっているため、科学者が個々の準実験を評価するために使用できる共有ライブラリを開発する上で、共通のパターンを特定することが強力な推進力となっている。
And to support our continued scale, we’ve built internal tooling that coalesces data retrieval, design evaluation, analysis, and reproducible reporting, all with the goal to enable our scientists.
また、継続的な規模拡大をサポートするため、データ検索、デザイン評価、分析、再現可能な報告を統合する社内ツールを構築し、これらすべてを科学者たちが行えるようにすることを目標としている。

We expect our investments in research, tooling, and education for quasi-experiments to grow over time.
準実験のための研究、ツール、教育への投資は、時間の経過とともに拡大していくものと期待している。
In success, we will enable both scientists and their cross functional partners to learn more about how to deliver more joy to current and future Netflix members.
成功することで、科学者とそのクロスファンクショナル・パートナーの双方が、現在および将来のネットフリックス会員により多くの喜びを提供する方法について、より多くを学ぶことができるようになる。

### Experimentation Platform as a Product. 製品としての実験プラットフォーム。

We treat the Netflix Experimentation Platform as an internal product, complete with its own product manager and innovation roadmap.
私たちは、Netflix Experimentation Platformを、独自のプロダクトマネージャーとイノベーションロードマップを備えた社内製品として扱っています。
We aim to provide an end-to-end paved path for configuring, allocating, monitoring, reporting, storing and analyzing A/B tests, focusing on experimentation use cases that are optimized for simplicity and testing velocity.
私たちは、A/Bテストの設定、割り当て、監視、レポート、保存、分析のためのエンド・ツー・エンドの舗装パスを提供することを目指しており、シンプルさとテストの速度に最適化された実験のユースケースに焦点を当てています。
Our goal is to make experimentation a simple and integrated part of the product lifecycle, with little effort required on the part of engineers, data scientists, or PMs to create, analyze, and act on tests, with automation available wherever the test owner wants it.
エンジニア、データサイエンティスト、PMがテストを作成、分析、実行するのに必要な労力はほとんどなく、テストオーナーが望むところであればどこでも自動化を利用できる。

However, if the platform’s default paths don’t work for a specific use case, experimenters can leverage our democratized contribution model, or reuse pieces of the platform, to build out their own solutions.
しかし、プラットフォームのデフォルト・パスが特定のユースケースで機能しない場合、実験者は民主化された貢献モデルを活用したり、プラットフォームの一部を再利用したりして、独自のソリューションを構築することができる。
As experimenters innovate on the boundaries of what’s possible in measurement methodology, experimental design, and automation, the Experimentation Platform team partners to commoditize these innovations and make them available to the broader organization.
実験者は、測定方法論、実験デザイン、自動化において可能なことの境界を革新しており、Experimentation Platformチームは、これらの革新的技術を商品化し、より広範な組織で利用できるようにするためにパートナーを組んでいる。

Three core principles guide product development for our experimentation platform:
私たちの実験プラットフォームの製品開発には、3つの基本原則があります：

Complexities and nuances of testing such as allocations and methodologies should, typically, be abstracted away from the process of running a single test, with emphasis instead placed on opinionated defaults that are sensible for a set of use cases or testing areas.
一般的に、割り当てや方法論といったテストの複雑さや微妙なニュアンスは、1つのテストを実行するプロセスから抽象化されるべきであり、その代わりに、一連のユースケースやテスト領域にとって賢明な意見に基づくデフォルトに重点を置くべきである。

Manual intervention at specific steps in the test execution should, typically, be optional, with emphasis instead on test owners being able to invest their attention where they feel it adds value and leave other areas to automation.
テスト実行の特定のステップにおける手作業による介入は、通常、任意であるべきで、その代わりに、テストオーナーが付加価値を感じられるところに注意を注ぎ、他の領域は自動化に任せることができることに重点を置く。

Designing, executing, reporting, deciding, and learning are all different phases of the experiment lifecycle that have differing needs and users, and each stage benefits from purpose built tooling for each use.
実験の設計、実行、報告、決定、学習はすべて、実験ライフサイクルの異なる段階であり、ニーズもユーザーも異なる。

## Conclusion 結論

Netflix has a strong culture of experimentation, and results from A/B tests, or other applications of the scientific method, are generally expected to inform decisions about how to improve our product and deliver more joy to members.
Netflixには実験を重視する文化があり、A/Bテストやその他の科学的手法の応用から得られた結果は、一般的に、製品を改善し、会員により多くの喜びを提供する方法についての意思決定に反映されることが期待されています。
To support the current and future scale of experimentation required by the growing Netflix member base and the increasing complexity of our business, Netflix has invested in culture, people, infrastructure, and internal education to make A/B testing broadly accessible across the company.
Netflixの会員数の増加とビジネスの複雑化に伴い、現在および将来的に必要とされる実験規模をサポートするため、Netflixは文化、人材、インフラ、社内教育に投資し、A/Bテストを全社的に広く利用できるようにしました。

And we are continuing to evolve our culture of learning and experimentation to deliver more joy to Netflix members around the world.
そして、世界中のNetflix会員にさらなる喜びをお届けするために、学習と実験の文化を進化させ続けています。
As our member base and business grows, smaller differences between treatment and control experiences become materially important.
会員数が増え、ビジネスが成長するにつれて、治療と対照の体験の差が小さくなっていく。
That’s also true for subsets of the population: with a growing member base, we can become more targeted and look to deliver positive experiences to cohorts of users, defined by geographical region, device type, etc.
それは人口のサブセットにも当てはまります： 会員数が増えれば、よりターゲットを絞り、地域やデバイスの種類などによって定義されたユーザー群にポジティブな体験を提供することができる。
As our business grows and expands, we are looking for new places that could benefit from experimentation, ways to run more experiments and learn more with each, and ways to accelerate our experimentation program while making experimentation accessible to more of our colleagues.
私たちのビジネスが成長し拡大するにつれて、私たちは実験から利益を得ることができる新しい場所、より多くの実験を実行し、それぞれの実験からより多くを学ぶ方法、そして実験をより多くの同僚が利用できるようにしながら私たちの実験プログラムを加速させる方法を探しています。

But the biggest opportunity is to deliver more joy to our members through the virtuous cycle of experimentation.
しかし、最大のチャンスは、実験の好循環を通じて会員にさらなる喜びを提供することだ。

Interested in learning more? Explore our research site.
もっと知りたいですか？研究サイトをご覧ください。

Interested in joining us? Explore our open roles.
ご興味がおありですか？募集職種をご覧ください。
