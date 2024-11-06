<!-- これ読む! -->

# How The New York Times incorporates editorial judgment in algorithms to curate its home page ニューヨーク・タイムズ紙はどのように編集者の判断をアルゴリズムに組み込み、ホームページをキュレーションしているのか？

The Times’ algorithmic recommendations team on responding to reader feedback, newsroom concerns, and technical hurdles.
読者からのフィードバック、ニュースルームの懸念事項、技術的なハードルへの対応について、タイムズ紙のアルゴリズム推薦チーム。

Whether on the web or the app, the home page of The New York Times is a crucial gateway, setting the stage for readers’ experiences and guiding them to the most important news of the day.
ウェブであれアプリであれ、ニューヨーク・タイムズのトップページは、読者の体験の舞台を整え、その日の最も重要なニュースへと導く、重要なゲートウェイである。
The Times publishes over 250 stories daily, far more than the 50 to 60 stories that can be featured on the home page at a given time.
タイムズ紙は毎日250以上の記事を掲載しており、トップページに掲載される50から60の記事をはるかに上回る。
Traditionally, editors have manually selected and programmed which stories appear, when and where, multiple times daily.
従来は、編集者が毎日何度も、どの記事を、いつ、どこに掲載するかを手作業で選択し、プログラムしていた。
This manual process presents challenges:
この手作業には課題がある：

How can we provide readers a relevant, useful, and fresh experience each time they visit the home page?
読者がホームページを訪れるたびに、関連性が高く、有益で、新鮮な体験を提供するにはどうすればいいのか。

How can we make our editorial curation process more efficient and scalable?
編集キュレーション・プロセスをより効率的でスケーラブルなものにするにはどうすればいいか？

How do we maximize the reach of each story and expose more stories to our readers?
それぞれのストーリーのリーチを最大化し、より多くのストーリーを読者に届けるにはどうすればいいのか？

To address these challenges, the Times has been actively developing and testing editorially driven algorithms to assist in curating home page content.
このような課題に対処するため、タイムズはホームページのコンテンツのキュレーションを支援する編集者主導のアルゴリズムを積極的に開発し、テストしてきた。
These algorithms are editorially driven in that a human editor’s judgment or input is incorporated into every aspect of the algorithm — including deciding where on the home page the stories are placed, informing the rankings, and potentially influencing and overriding algorithmic outputs when necessary.
これらのアルゴリズムは、人間の編集者の判断やインプットがアルゴリズムのあらゆる側面に組み込まれているという点で、編集主導型である。
From the get-go, we’ve designed algorithmic programming to elevate human curation, not to replace it.
私たちは最初から、人間のキュレーションに取って代わるのではなく、人間のキュレーションを向上させるためにアルゴリズム・プログラミングを設計しました。

## Which parts of the home page are algorithmically programmed? ホームページのどの部分がアルゴリズムでプログラムされていますか？

The Times began using algorithms for content recommendations in 2011 but only recently started applying them to home page modules.
タイムズ紙は2011年にコンテンツの推薦にアルゴリズムを使い始めたが、最近になってホームページのモジュールに適用し始めた。
For years, we only had one algorithmically-powered module, “Smarter Living,” on the home page, and later, “Popular in The Times.” Both were positioned relatively low on the page.
何年もの間、トップページにはアルゴリズムを駆使したモジュール 「Smarter Living 」と、後に 「Popular in The Times 」があるだけだった。どちらもページの比較的低い位置にあった。

Three years ago, the formation of a cross-functional team — including newsroom editors, product managers, data scientists, data analysts, and engineers — brought the momentum needed to advance our responsible use of algorithms.
3年前、ニュースルームの編集者、プロダクトマネージャー、データサイエンティスト、データアナリスト、エンジニアを含む部門横断的なチームが結成され、アルゴリズムの責任ある利用を推進するために必要な機運が高まった。
Today, nearly half of the home page is programmed with assistance from algorithms that help promote news, features, and sub-brand content, such as The Athletic and Wirecutter.
今日、トップページの半分近くは、The AthleticやWirecutterなどのニュース、特集、サブブランドのコンテンツを促進するアルゴリズムによる支援でプログラムされている。
Some of these modules, such as the features module located at the top right of the home page on the web version, are in highly visible locations.
これらのモジュールの中には、ウェブ版のホームページの右上にあるfeaturesモジュールのように、非常に目につきやすい場所にあるものもある。
During major news moments, editors can also deploy algorithmic modules to display additional coverage to complement a main module of stories near the top of the page.
また、重大なニュースの際には、編集者はアルゴリズムによるモジュールを導入し、ページ上部付近のストーリーのメインモジュールを補完する追加報道を表示することもできる。
(The topmost news package of Figure 1 is an example of this in action.)
(図1の一番上のニュースパッケージは、これが実際に行われている例である)。

![]()

## How is editorial judgment incorporated into algorithmic programming? アルゴリズミック・プログラミングに編集者の判断をどのように取り入れるか？

Algorithmic programming comprises three steps: (1) Pooling: Creating a pool of eligible stories for the specific module; (2) Ranking: Sorting stories by a ranking mechanism; and (3) Finishing: Applying editorial guardrails and business rules to ensure the final output of stories meets our standards.
アルゴリズム・プログラミングには3つのステップがある： (1) プーリング： (2) ランキング： (3)仕上げ： 編集のガードレールとビジネス・ルールを適用し、ストーリーの最終アウトプットが当社の基準を満たすようにする。
Editorial judgment is incorporated into all of these steps, in different ways.
編集者の判断は、さまざまな方法で、これらすべてのステップに組み込まれている。

To make an algorithmic recommendation, we first need a pool of articles eligible to appear in a given home page module.
アルゴリズムによる推薦を行うには、まず、与えられたホームページ・モジュールに表示される記事のプールが必要である。
A pool can be either manually curated by editors or automatically generated via a query based on rules set by the newsroom.
プールは、編集者が手動でキュレーションすることも、ニュースルームが設定したルールに基づいてクエリを介して自動的に生成することもできる。

A pool typically includes more stories than the number of slots available in the module, so we need a mechanism to rank them to determine which ones to show first and in what order.
プールには通常、モジュールで利用可能なスロットの数よりも多くのストーリーが含まれるので、どのストーリーを最初に、どの順番で表示するかを決定するために、それらをランク付けするメカニズムが必要です。
While there are various ways to rank stories, the algorithm we frequently use on the home page is a contextual bandit, a reinforcement learning method (see our previous blog post for more information).
ストーリーのランク付けにはさまざまな方法があるが、トップページで頻繁に使用しているアルゴリズムは、強化学習法のひとつであるコンテクスチュアル・バンディットである（詳しくは以前のブログ記事を参照）。
In its simplest form, a bandit recommends the same set of engaging articles to all users; the “contextual” version uses additional reader information (e.g., reading history or geographical location) to adjust the recommendations and make the experience more relevant for each reader.
最も単純な形では、バンディットはすべてのユーザーに同じ魅力的な記事セットを推薦する。「コンテクスチュアル 」バージョンは、読者の追加情報（例えば、読書履歴や地理的な場所）を使用して推薦を調整し、各読者にとってより適切なエクスペリエンスにする。
For an example of the geo-personalized bandit, see here.
地理的にパーソナライズされた盗賊の例については、こちらをご覧ください。

To prioritize mission-driven and significant stories, we use several approaches to quantify editorial importance.
ミッション重視の重要なストーリーに優先順位をつけるため、編集の重要性を定量化するいくつかのアプローチを用いている。
One approach is having editors assign a rank to each story in the pool, with more recent and newsworthy stories generally considered more important.
一つの方法は、編集者が各記事にランクをつけることである。
Another method infers a story’s importance based on its past promotion on the homepage, where stories that remain in prominent positions for longer are rated as more important.
もう一つの方法は、トップページでの過去のプロモーションに基づいてストーリーの重要性を推測するもので、目立つ位置に長くとどまっているストーリーほど重要性が高いと評価される。
Regardless of the approach, editorial importance can be combined with the bandit to ensure that editorial judgment is incorporated into the ranking process, thus prioritizing stories deemed important by the newsroom.
どのようなアプローチにせよ、編集上の重要度をバンディットと組み合わせることで、編集上の判断がランキングプロセスに組み込まれ、ニュースルームが重要だと判断した記事に優先順位をつけることができる。

Once we have a ranked list of stories, we make final adjustments based on predetermined rules developed with our newsroom partners before stories are shown to readers.
ランク付けされた記事リストが出来上がると、読者に記事を見せる前に、ニュースルームのパートナーとともに作成した所定のルールに基づいて最終調整を行う。
One such intervention we developed is a “pinning” function that allows editors to override the algorithm and pin important stories at the top.
私たちが開発したそのような介入のひとつが、編集者がアルゴリズムを上書きして重要な記事をトップに固定できる「ピン留め」機能である。
Other important examples are our “already-read” and “already-seen” filters, which deprioritize stories that the user has already read or seen a certain number of times (Figure 2).
その他の重要な例として、「既読」と「既視」フィルターがあります。これは、ユーザーが既に読んだり、一定回数見たストーリーを優先順位から除外するものです（図2）。
This finishing step ensures that editorial judgment shapes the final output and that we maintain a dynamic and fresh user experience.
この仕上げのステップによって、編集者の判断が最終的なアウトプットを形成し、ダイナミックで新鮮なユーザー体験を維持することができる。

## How do we set up an algorithmically powered module on the home page? ホームページにアルゴリズムで動くモジュールを設置するには？

The process begins with clearly defining editorial intentions, standards, and boundaries as well as reader goals, and then designing algorithms appropriately.
そのプロセスは、編集の意図、基準、境界線、読者の目標を明確に定義し、適切なアルゴリズムを設計することから始まる。
To illustrate the process, consider the above-mentioned features module (Figure 1): Content in this module is among the most widely read on the home page.
このプロセスを説明するために、前述のfeaturesモジュールを考えてみよう（図1）： このモジュールのコンテンツは、ホームページで最も広く読まれている。
The goal of algorithmic programming for this module is to increase engagement by presenting readers with freshly published features and columns and also to ensure that the most relevant and engaging stories are subsequently displayed.
このモジュールのアルゴリズム・プログラミングの目標は、読者に掲載されたばかりの特集やコラムを提示することでエンゲージメントを高め、また、最も関連性が高く魅力的なストーリーがその後に表示されるようにすることである。

After several rounds of experimentation and extensive collaboration with editors, we realized that more features had to be built to achieve the intended reader experience and for the newsroom to be comfortable with integrating algorithms into their process for programming the home page.
数回にわたる実験と編集者との広範なコラボレーションの結果、私たちは、意図した読者体験を実現し、ニュースルームがホームページをプログラムするプロセスにアルゴリズムを統合することに納得するためには、さらに多くの機能を構築する必要があることに気づいた。
Together, we built and launched the following features, which are cornerstones in accelerating the use of algorithmic programming on the home page:
これらは、ホームページでのアルゴリズム・プログラミングの使用を加速させる基礎となるものです：

Exposure boosting: While pinning is an effective tool for increasing the exposure of important stories, it is also a rather blunt one: a pinned story is shown to all readers until unpinned by an editor.
露出を高める： ピン留めは重要なストーリーの露出を増やす効果的なツールだが、かなり鈍感なものでもある： 編集者がピン留めを解除するまで、ピン留めされたストーリーはすべての読者に表示される。
To meet a desire by home page editors for a “softer” and more dynamic solution, we developed an “exposure boosting” capability.
よりソフトでダイナミックなソリューションを求めるホームページ編集者の要望に応えるため、私たちは「露出ブースト」機能を開発しました。
While a “boosted” story also initially appears at the top of the module, it gradually moves down the slots over time — at a rate predetermined by editors — until it becomes subject to the algorithm’s bandit again.
ブースト」されたストーリーも、最初はモジュールの一番上に表示されるが、時間の経過とともに、編集者によってあらかじめ決められた割合で、再びアルゴリズムの盗賊の対象となるまで、徐々にスロットの下に移動していく。
(Figure 3: Exposure Boosting).
(図3： Exposure Boosting）。

Smart refreshing: Another way to increase the exposure of our stories while ensuring that readers are presented with fresh content is by removing articles that the user has seen several times but has not clicked on — this assumes that the reader is not interested in the story displayed and the algorithm instead shows the next story on the list.
スマートリフレッシュ： 読者に新鮮なコンテンツを確実に提供しながら、ストーリーの露出を増やすもう一つの方法は、ユーザーが何度も見たがクリックしなかった記事を削除することである。これは、読者が表示されたストーリーに興味がないと仮定し、代わりにアルゴリズムがリストの次のストーリーを表示する。
When an article is shown to a user, whether they click on it or not, it’s called an impression.
記事がユーザーに表示されたとき、それをクリックするかどうかにかかわらず、それはインプレッションと呼ばれる。
This rather rudimentary logic has its drawbacks: Frequent visitors might experience recommendations refreshing too often, causing a disorienting “slot machine” effect.
この初歩的なロジックには欠点もある： 頻繁に訪問する人は、推薦文が頻繁に更新され、「スロットマシーン」のような幻惑的な効果を経験するかもしれない。
They could also quickly exhaust all recommendations, resulting in a static module.
また、すぐにすべての推薦を使い果たし、静的なモジュールになってしまう可能性もある。
At the same time, infrequent users, who don’t reach the impression limit, might see the same stories on distant subsequent visits, leading to a home page that would feel stale.
同時に、インプレッションの上限に達しない利用頻度の低いユーザーは、次回以降の訪問で同じストーリーを目にする可能性があり、トップページが陳腐に感じられることになる。

These potential issues were especially of concern for high-traffic modules like the features module.
こうした潜在的な問題は、featuresモジュールのようなトラフィックの多いモジュールで特に懸念された。
To address them, we developed a capability called “smart refreshing.” This feature creates a more stable experience for frequent visitors by only increasing the impression counter if a certain amount of time has passed since the last impression.
そこで、私たちは 「スマート・リフレッシュ 」と呼ばれる機能を開発しました。この機能は、最後のインプレッションから一定時間が経過した場合のみインプレッション・カウンターを増加させることで、頻繁に訪れる訪問者により安定した体験を提供します。
Effectively, impressions occurring less than that amount of time are collapsed into a single impression.
事実上、その時間未満に発生したインプレッションは、1つのインプレッションにまとめられる。
For infrequent visitors, smart refreshing limits staleness by automatically refreshing recommendations after a set period since their first impression, even if the impression limit was not reached.
インプレッションの制限に達していなくても、最初のインプレッションから一定期間が経過すると、自動的にレコメンデーションが更新されます。
Home page editors decide on the interval between impressions and the maximum duration a story remains after its initial view based on editorial judgment and A/B testing.
トップページの編集者は、編集者の判断とA/Bテストに基づいて、インプレッションの間隔と、最初の表示後に記事が残る最長時間を決定します。

Exposure minimums: In response to concerns from editors that some stories risk not getting enough exposure under purely algorithmic programming, we developed exposure minimums.
露出の最低ライン アルゴリズミック・プログラミングだけでは十分な露出が得られないストーリーがあるのではないかという編集者の懸念に応え、露出の下限を設定しました。
This capability gives the newsroom the reassurance that all stories (particularly less popular ones) receive a minimum number of impressions on the home page before the algorithm takes over their programming.
この機能により、ニュースルームは、アルゴリズムが番組編成を引き継ぐ前に、すべての記事（特に人気のない記事）がトップページで最低限のインプレッション数を獲得しているという安心感を得ることができる。
This guarantee helps set editorial expectations for story exposure and has enabled the rollout of algorithms on prominent sections of the home page, such as the Features Module.
この保証は、記事露出に対する編集部の期待値を設定するのに役立ち、特集モジュールなどのホームページの目立つセクションにアルゴリズムを展開することを可能にした。
Typically, higher minimum values increase story exposure but can interfere with algorithm optimization, reducing overall engagement.
一般的に、最小値が高いほどストーリーの露出は増えるが、アルゴリズムの最適化に支障をきたし、全体的なエンゲージメントが低下する可能性がある。
To find the right balance between exposure and engagement, the exposure minimum is determined in collaboration with our newsroom partners and through A/B testing.
露出とエンゲージメントの適切なバランスを見つけるため、ニュースルームのパートナーと協力し、A/Bテストを通じて露出の最小値を決定する。

Algo visibility tools: One blocker we encountered while trying to scale algorithmic programming was the lack of visibility for editors regarding reader experience and story performance.
アルゴリズム可視化ツール： アルゴリズム・プログラミングの規模を拡大しようとしたときに、私たちが遭遇した障害のひとつは、読者の体験やストーリーのパフォーマンスに関する編集者の可視性の欠如でした。
One of the biggest challenges was feedback from the newsroom that editors and reporters couldn’t tell if their stories would appear in an algorithmic module on the home page.
最大の課題のひとつは、編集者や記者が自分の記事がトップページのアルゴリズムモジュールに表示されるかどうかわからないというニュースルームからのフィードバックだった。
With the “already-read” filter in place, their stories, which they would have read, wouldn’t show up on the home page.
既読」フィルターが設定されていると、彼らが読んだはずのストーリーはトップページに表示されない。

To address this, our product designer, engineers and data scientists partnered with home page editors to conceptualize and build a browser extension that allows editors to track all the algorithmic modules on the home page, preview different A/B testing variants, and review all the stories that have been selected and eligible for promotion for each module.
この問題に対処するため、当社のプロダクトデザイナー、エンジニア、データサイエンティストはホームページ編集者と協力し、編集者がホームページ上のすべてのアルゴリズムモジュールを追跡し、さまざまなA/Bテストバリアントをプレビューし、各モジュールのプロモーション対象として選択されたすべてのストーリーを確認できるブラウザ拡張機能を構想・構築しました。
Our engineers also built a tool that sends automated alerts to editors about changes in algorithmic programming, including new stories added to the pool and any headline or summary updates.
私たちのエンジニアはまた、アルゴリズム・プログラミングの変更について、編集者に自動アラートを送信するツールも構築しました。このツールには、プールに追加された新しいストーリーや、見出しや要約の更新などが含まれます。
Additionally, the data science team developed a dashboard to provide near-real-time analytics for stories that were algorithmically programmed.
さらに、データサイエンスチームは、アルゴリズムでプログラムされたストーリーをほぼリアルタイムで分析できるダッシュボードを開発した。

After rigorously testing each of these new features and getting editors familiar with these tools and concepts, we permanently implemented algorithmic programming for the features module in the spring of 2024.
これらの新機能の一つひとつを厳密にテストし、編集者がこれらのツールや概念に慣れるようにした後、2024年の春に機能モジュールのアルゴリズム・プログラミングを恒久的に実装した。
This approach not only streamlined the editorial workflow (daily updates to the module were reduced by a third), it also gave stories that had a longer shelf life more time on the home page, lifting overall engagement.
このアプローチにより、編集ワークフローが合理化されただけでなく（モジュールへの毎日の更新が3分の1に減った）、保存期間の長いストーリーがトップページに掲載される時間が長くなり、全体的なエンゲージメントが高まった。
Our product colleagues were delighted that powering the features module with an algorithm also helped increase engagement with our sub-brands such as Wirecutter and Cooking.
当社の製品担当者は、機能モジュールをアルゴリズムで強化することで、WirecutterやCookingといった当社のサブブランドのエンゲージメントを高めることができたと喜んでいます。

## Taking algorithmic programming further — breaking news and more アルゴリズミック・プログラミングをさらに進化させる - ニュース速報他

The strong foundation we built by incorporating editorial thinking into our algorithms, coupled with the trust we cultivated, led to more demand from the newsroom for more algorithmic programming tools.
編集的思考をアルゴリズムに取り入れることで築いた強固な基盤は、私たちが培った信頼と相まって、より多くのアルゴリズム・プログラミング・ツールを求めるニュースルームからの要求につながりました。
Today, editors are also using a tailored set of algorithmic modules to power a secondary set of stories for a topic or news event.
今日、編集者はまた、トピックやニュースイベントに関する二次的なストーリーを提供するために、カスタマイズされたアルゴリズムモジュールを使用している。
These modules are completely self-service for editors, and have been particularly useful during major news events, when the volume of coverage produced often exceeds the amount of real estate on the home page.
これらのモジュールは編集者のための完全なセルフサービスであり、制作された報道の量がホームページの領域を超えることが多い大きなニュースの際に特に役立っている。

Currently, algorithmic programming recommends stories within individual modules on the home page.
現在、アルゴリズム・プログラミングは、ホームページの個々のモジュール内のストーリーを推奨している。
Next, we want to explore and test reordering modules based on a mix of editorial importance, engagement, and personalization signals.
次に、編集の重要性、エンゲージメント、パーソナライゼーションのシグナルをミックスしたものに基づいて、モジュールの並べ替えを検討し、テストしたい。
We believe this approach can further improve a reader’s experience and amplify our journalism.
私たちは、このアプローチが読者の体験をさらに向上させ、ジャーナリズムを増幅させると信じている。

Zhen Yang is a data scientist on the algorithmic recommendations team at The New York Times.
ニューヨーク・タイムズのアルゴリズム・レコメンデーション・チームのデータサイエンティスト。
Celia Eddy, Alex Saez, Derrick Ho, and Christopher Wiggins contributed to this post.
Celia Eddy、Alex Saez、Derrick Ho、Christopher Wigginsが寄稿した。
This article originally appeared on NYT Open and is © 2024 The New York Times Company.
この記事はNYTオープンに掲載されたもので、© 2024 The New York Times Companyの著作です。
