<!-- これ読む! -->

# How The New York Times incorporates editorial judgment in algorithms to curate its home page ニューヨーク・タイムズ紙はどのように編集者の判断をアルゴリズムに組み込み、ホームページをキュレーションしているのか？

The Times’ algorithmic recommendations team on responding to reader feedback, newsroom concerns, and technical hurdles.
読者からのフィードバック、ニュースルームの懸念事項、技術的なハードルへの対応について、タイムズ紙のアルゴリズム推薦チーム。

Whether on the web or the app, the home page of The New York Times is a crucial gateway, setting the stage for readers’ experiences and guiding them to the most important news of the day.
ウェブであれアプリであれ、ニューヨーク・タイムズのトップページは、読者の体験の舞台を整え、**その日の最も重要なニュースへと導く、重要なゲートウェイ**である。
The Times publishes over 250 stories daily, far more than the 50 to 60 stories that can be featured on the home page at a given time.
**タイムズ紙は毎日250以上の記事を掲載しており、トップページに掲載される50から60の記事をはるかに上回る**。(自社コンテンツだけなのかな、日経新聞みたいに:thinking:)
Traditionally, editors have manually selected and programmed which stories appear, when and where, multiple times daily.
従来は、編集者が毎日何度も、どの記事を、いつ、どこに掲載するかを手作業で選択し、プログラムしていた。
This manual process presents challenges:
この手作業には課題がある：

- How can we provide readers a relevant, useful, and fresh experience each time they visit the home page?
読者がホームページを訪れるたびに、関連性が高く、有益で、新鮮な体験を提供するにはどうすればいいのか。

- How can we make our editorial curation process more efficient and scalable?
**編集キュレーション・プロセスをより効率的でスケーラブルなものにする**にはどうすればいいか？

- How do we maximize the reach of each story and expose more stories to our readers?
それぞれのストーリーのリーチを最大化し、より多くのストーリーを読者に届けるにはどうすればいいのか？

To address these challenges, the Times has been actively developing and testing editorially driven algorithms to assist in curating home page content.
このような課題に対処するため、タイムズはホームページのコンテンツの**キュレーションを支援する編集者主導のアルゴリズム**を積極的に開発し、テストしてきた。
These algorithms are editorially driven in that a human editor’s judgment or input is incorporated into every aspect of the algorithm — including deciding where on the home page the stories are placed, informing the rankings, and potentially influencing and overriding algorithmic outputs when necessary.
これらのアルゴリズムは、**人間の編集者の判断や入力がアルゴリズムのあらゆる側面に組み込まれているため、編集者主導**と言える。つまり、ストーリーがホームページのどこに配置されるかを決定し、ランキングを通知し、必要に応じてアルゴリズムの出力に影響を与え、上書きすることができる。
From the get-go, we’ve designed algorithmic programming to elevate human curation, not to replace it.
私たちは最初から、**人間のキュレーションに取って代わるのではなく、人間のキュレーションを向上させるためにアルゴリズム・プログラミングを設計**しました。(この考えは大事かも...!:thinking: 両輪の関係というよりは、合体させる感じか...:thinking:)

<!-- ここまで読んだ! -->

## Which parts of the home page are algorithmically programmed? ホームページのどの部分がアルゴリズムでプログラムされていますか？

The Times began using algorithms for content recommendations in 2011 but only recently started applying them to home page modules.
タイムズ紙は2011年にコンテンツの推薦にアルゴリズムを使い始めたが、最近になってホームページのモジュールに適用し始めた。
For years, we only had one algorithmically-powered module, “Smarter Living,” on the home page, and later, “Popular in The Times.” Both were positioned relatively low on the page.
何年もの間、ホームページには「Smarter Living」というアルゴリズムで動くモジュールが1つしかなく、後に「Popular in The Times」が追加された。どちらもページの下部に位置していた。

Three years ago, the formation of a cross-functional team — including newsroom editors, product managers, data scientists, data analysts, and engineers — brought the momentum needed to advance our responsible use of algorithms.
**3年前、ニュースルームの編集者、プロダクトマネージャー、データサイエンティスト、データアナリスト、エンジニアを含む部門横断的なチームが結成され、アルゴリズムの責任ある使用を進めるために必要な勢いをもたらした**。
Today, nearly half of the home page is programmed with assistance from algorithms that help promote news, features, and sub-brand content, such as The Athletic and Wirecutter.
今日、トップページの半分近くは、ニュース、特集、The AthleticやWirecutterなどのサブブランドのコンテンツを促進するのに役立つアルゴリズムの支援を受けてプログラムされている。
Some of these modules, such as the features module located at the top right of the home page on the web version, are in highly visible locations.
これらのモジュールの中には、ウェブ版のホームページの右上にあるfeaturesモジュールのように、非常に目につきやすい場所にあるものもある。
During major news moments, editors can also deploy algorithmic modules to display additional coverage to complement a main module of stories near the top of the page.
また、重大なニュースの際には、編集者がアルゴリズムモジュールを展開して、ページの上部近くにある主要なモジュールのストーリーを補完する追加のカバレッジを表示することもできる。
(The topmost news package of Figure 1 is an example of this in action.)
(図1の一番上のニュースパッケージは、これが実際に行われている例である)。

![]()

## How is editorial judgment incorporated into algorithmic programming? アルゴリズミック・プログラミングに編集者の判断をどのように取り入れるか？

Algorithmic programming comprises three steps: (1) Pooling: Creating a pool of eligible stories for the specific module; (2) Ranking: Sorting stories by a ranking mechanism; and (3) Finishing: Applying editorial guardrails and business rules to ensure the final output of stories meets our standards.
アルゴリズム・プログラミングには3つのステップがある： (1) プーリング： 特定のモジュールのための適格なストーリーのプールを作成すること； (2) ランキング： ストーリーをランキングするメカニズムによってソートすること； (3) 仕上げ： 編集のガードレールとビジネスルールを適用して、ストーリーの最終出力が私たちの基準を満たすようにすること。

To make an algorithmic recommendation, we first need a pool of articles eligible to appear in a given home page module.
アルゴリズムによる推薦を行うには、まず、与えられたホームページ・モジュールに表示される記事のプールが必要である。
A pool can be either manually curated by editors or automatically generated via a query based on rules set by the newsroom.
**プールは、編集者によって手動でキュレーションされるか、ニュースルームが設定したルールに基づいてクエリを使用して自動的に生成される。**　(ふむふむ...!:thinking:)

A pool typically includes more stories than the number of slots available in the module, so we need a mechanism to rank them to determine which ones to show first and in what order.
**プールには通常、モジュールで利用可能なスロットの数よりも多くのストーリーが含まれるので、どのストーリーを最初に、どの順番で表示するかを決定するために、それらをランク付けするメカニズムが必要**です。
While there are various ways to rank stories, the algorithm we frequently use on the home page is a contextual bandit, a reinforcement learning method (see our previous blog post for more information).
**ストーリーのランク付けにはさまざまな方法があるが、トップページで頻繁に使用しているアルゴリズムは、強化学習法のひとつであるコンテクスチュアル・バンディット**である（詳しくは[以前のブログ記事](https://open.nytimes.com/how-the-new-york-times-is-experimenting-with-recommendation-algorithms-562f78624d26)を参照）。
In its simplest form, a bandit recommends the same set of engaging articles to all users; the “contextual” version uses additional reader information (e.g., reading history or geographical location) to adjust the recommendations and make the experience more relevant for each reader.
最も単純な形では、バンディットはすべてのユーザーに同じセットの魅力的な記事を推薦する。「コンテクスチュアル」バージョンは、追加の読者情報（たとえば、閲覧履歴や地理的位置）を使用して推薦を調整し、各読者にとってより関連性のある体験を提供する。
For an example of the geo-personalized bandit, see here.
地理的にパーソナライズされた盗賊の例については、[こちら](https://open.nytimes.com/how-the-new-york-times-is-experimenting-with-recommendation-algorithms-562f78624d26)をご覧ください。

To prioritize mission-driven and significant stories, we use several approaches to quantify editorial importance.
mission-driven (??) で重要なストーリーに優先順位をつけるために、編集上の重要性を定量化するためにいくつかのアプローチを使用しています。
One approach is having editors assign a rank to each story in the pool, with more recent and newsworthy stories generally considered more important.
**ひとつのアプローチは、編集者がプール内の各ストーリーにランクを割り当てること**で、一般的には最近のものやニュース価値の高いものがより重要とされる。
Another method infers a story’s importance based on its past promotion on the homepage, where stories that remain in prominent positions for longer are rated as more important.
**もう一つの方法は、トップページでの過去のプロモーションに基づいてストーリーの重要性を推測するもの**で、より長く目立つ位置にあるストーリーほど重要と評価される。
Regardless of the approach, editorial importance can be combined with the bandit to ensure that editorial judgment is incorporated into the ranking process, thus prioritizing stories deemed important by the newsroom.
どのようなアプローチにせよ、編集上の重要度をバンディットと組み合わせることで、**編集者の判断がランキングプロセスに組み込まれ**、ニュースルームが重要と判断したストーリーが優先されるようになる。

Once we have a ranked list of stories, we make final adjustments based on predetermined rules developed with our newsroom partners before stories are shown to readers.
ランク付けされた記事リストが出来上がると、**読者に記事を見せる前に、ニュースルームのパートナーとともに作成した所定のルールに基づいて最終調整**を行う。
One such intervention we developed is a “pinning” function that allows editors to override the algorithm and pin important stories at the top.
私たちが開発したそのような介入のひとつが、**編集者がアルゴリズムを上書きして重要な記事をトップに固定できる「ピン留め」機能**である。
Other important examples are our “already-read” and “already-seen” filters, which deprioritize stories that the user has already read or seen a certain number of times (Figure 2).
その他の重要な例として、**「既読(already-read)」と「既に見た(already-seen)」のフィルターがあり、ユーザーが既に何度か読んだり見たりしたストーリーを優先度を下げる**（図2）。
This finishing step ensures that editorial judgment shapes the final output and that we maintain a dynamic and fresh user experience.
この仕上げのステップによって、**編集者の判断が最終的なアウトプットを形成**(ex. この出面はパーソナライズを強めに効かせよう、この出面は新しい記事を多く使おう, とか??:thinking:)し、ダイナミックで新鮮なユーザ体験を維持することができる。

<!-- ここまで読んだ! -->

## How do we set up an algorithmically powered module on the home page? ホームページにアルゴリズムで動くモジュールを設置するには？

The process begins with clearly defining editorial intentions, standards, and boundaries as well as reader goals, and then designing algorithms appropriately.
**そのプロセスは、編集の意図、基準、境界線、読者の目標を明確に定義**し、適切なアルゴリズムを設計することから始まる。(要件定義、みたいなことだろうか??:thinking:)
To illustrate the process, consider the above-mentioned features module (Figure 1): Content in this module is among the most widely read on the home page.
このプロセスを説明するために、前述のfeaturesモジュールを考えてみよう（図1）： このモジュールのコンテンツは、トップページで最も多く読まれているものの一つである。
The goal of algorithmic programming for this module is to increase engagement by presenting readers with freshly published features and columns and also to ensure that the most relevant and engaging stories are subsequently displayed.
このモジュールのアルゴリズム・プログラミングの目的は、読者に新しく公開された特集やコラムを提示することでエンゲージメントを高めることであり、その後に最も関連性の高く魅力的なストーリーが表示されるようにすることである。
(モジュール毎に、どのようなアルゴリズムが理想的かを定義する、みたいな??:thinking:)

After several rounds of experimentation and extensive collaboration with editors, we realized that more features had to be built to achieve the intended reader experience and for the newsroom to be comfortable with integrating algorithms into their process for programming the home page.
数回にわたる実験と編集者との幅広い協力の結果、意図された読者体験を実現し、ニュースルームがトップページのプログラムにアルゴリズムを統合することに慣れるために、さらに多くの機能を構築する必要があることがわかりました。
Together, we built and launched the following features, which are cornerstones in accelerating the use of algorithmic programming on the home page:
以下の機能たちを一緒に構築し、リリースしました。これらは、ホームページでのアルゴリズム・プログラミングの利用を加速するための基盤となっています。

### Exposure boosting 露出?のBoosting

(ピン留め機能に、減衰機能を追加した感じかな??:thinking:)

While pinning is an effective tool for increasing the exposure of important stories, it is also a rather blunt one: a pinned story is shown to all readers until unpinned by an editor
ピン留めは重要なストーリーの露出を増やすための効果的なツールであるが、かなり鈍いツールでもある：ピン留めされたストーリーは、編集者によってピン留めが解除されるまで、すべての読者に表示される。
To meet a desire by home page editors for a “softer” and more dynamic solution, we developed an “exposure boosting” capability.
よりソフトでダイナミックなソリューションを求めるトップページの編集者の要望に応えるために、**「露出ブースティング」機能**を開発しました。
While a “boosted” story also initially appears at the top of the module, it gradually moves down the slots over time — at a rate predetermined by editors — until it becomes subject to the algorithm’s bandit again.
「ブーストされた」ストーリーも最初はモジュールのトップに表示されますが、時間の経過とともに、編集者が事前に決定した速度でスロットを下に移動し、再びアルゴリズムのバンディットの対象になります。
(Figure 3: Exposure Boosting).
(図3： Exposure Boosting）。

### Smart refreshing スマートリフレッシュ

(これは、既読記事を消す機能の話っぽい??:thinking:)

Another way to increase the exposure of our stories while ensuring that readers are presented with fresh content is by removing articles that the user has seen several times but has not clicked on — this assumes that the reader is not interested in the story displayed and the algorithm instead shows the next story on the list.
読者に新鮮なコンテンツを確実に提供しながら、ストーリーの露出を増やすもう一つの方法は、**ユーザーが何度か見たがクリックしなかった記事を削除すること**です。これは、**読者が表示されているストーリーに興味を持っていないと仮定し、代わりにアルゴリズムがリストの次のストーリーを表示する**というものです。
When an article is shown to a user, whether they click on it or not, it’s called an impression.
記事がユーザに表示されたとき、それをクリックするかどうかにかかわらず、それはインプレッションと呼ばれる。
This rather rudimentary logic has its drawbacks: Frequent visitors might experience recommendations refreshing too often, causing a disorienting “slot machine” effect.
この初歩的なロジックには欠点があります： **頻繁に訪れるユーザは、推奨が頻繁に更新されるため、「スロットマシン」の効果が生じ、混乱する可能性があります**。(それはそう...!:thinking:)
They could also quickly exhaust all recommendations, resulting in a static module.
また、**すぐにすべての推薦を使い果たし、静的なモジュールになってしまう可能性**もある。
At the same time, infrequent users, who don’t reach the impression limit, might see the same stories on distant subsequent visits, leading to a home page that would feel stale.
同時に、インプレッションの上限に達しない頻度の低いユーザは、後の訪問で同じストーリーを見る可能性があり、古く感じるホームページになる可能性があります。(あ、これは同じ記事かつユーザにk回impが発生したら下げる、というルールにしてるからか:thinking:)

These potential issues were especially of concern for high-traffic modules like the features module.
こうした潜在的な問題は、**featuresモジュールのようなトラフィックの多いモジュールで特に懸念**された。(スロットマシン的なことが起こりやすいもんね...!:thinking:)
To address them, we developed a capability called “smart refreshing.” This feature creates a more stable experience for frequent visitors by only increasing the impression counter if a certain amount of time has passed since the last impression.
これらの問題に対処するために、「スマートリフレッシュ」という機能を開発しました。この機能は、**最後のインプレッションから一定の時間が経過した場合にのみ、インプレッションカウンタを増やすことで、頻繁に訪れるユーザにより安定した体験を提供**します。
Effectively, impressions occurring less than that amount of time are collapsed into a single impression.
事実上、その一定時間よりも短い間隔で発生したインプレッションは、1つのインプレッションにまとめられます。(うんうん、わかりやすい:thinking:)
For infrequent visitors, smart refreshing limits staleness by automatically refreshing recommendations after a set period since their first impression, even if the impression limit was not reached.
頻度の低い訪問者に対しては、**最初のインプレッションから一定の期間が経過した後に、推薦を自動的に更新することで、古さを防ぎます。たとえインプレッションの上限に達していなくても**です。(ただ推薦結果を作り直すだけじゃなくて、前回impした記事は出さない、みたいな工夫をたぶんしてるんだよね...!:thinking:)
Home page editors decide on the interval between impressions and the maximum duration a story remains after its initial view based on editorial judgment and A/B testing.
トップページの編集者は、**編集上の判断とA/Bテストに基づいて、インプレッション間の間隔と、初回の閲覧後にストーリーが残る最大期間を決定**します。(=閾値の最適化の話!!:thinking:)

![]()

<!-- ここまで読んだ! -->

### Exposure minimums 露出の最低値

(コンテンツクリエイターのために、最小限の露出を保証する機能っぽい!:thinking:)

In response to concerns from editors that some stories risk not getting enough exposure under purely algorithmic programming, we developed exposure minimums
**アルゴリズミック・プログラミングだけでは十分な露出が得られないストーリーがあるのではないかという編集者の懸念**に応え、露出の下限を設定しました。
This capability gives the newsroom the reassurance that all stories (particularly less popular ones) receive a minimum number of impressions on the home page before the algorithm takes over their programming.
この機能により、ニュースルームは、**アルゴリズムがプログラムを引き継ぐ(=rankingのプロセス??:thinking:)前に、すべてのストーリー（特に人気のないもの）がホームページで最低限のインプレッションを受けることを保証**されます。
This guarantee helps set editorial expectations for story exposure and has enabled the rollout of algorithms on prominent sections of the home page, such as the Features Module.
**この保証は、記事露出に対する編集部の期待値を設定するのに役立ち、featuresモジュールなどのトップページの目立つセクションでアルゴリズムを展開することを可能にしました**。(コンテンツクリエイターと合意を得ること、大事だ...!:thinking:)
Typically, higher minimum values increase story exposure but can interfere with algorithm optimization, reducing overall engagement.
一般的に、最小値が高いほどストーリーの露出が増えますが、アルゴリズムの最適化に干渉し、全体的なエンゲージメントを減少させる可能性があります。
To find the right balance between exposure and engagement, the exposure minimum is determined in collaboration with our newsroom partners and through A/B testing.
**露出とエンゲージメントの間の適切なバランスを見つけるために、露出の最小値は、ニュースルームのパートナーとの協力とA/Bテストを通じて決定されます**。(閾値の最適化の話!!:thinking:)

### Algo visibility tools アルゴリズム可視化ツール

(編集者がアルゴリズムの振る舞いを見えるようにする機能っぽい! 結局これもExposure minimumsと同じく、コンテンツクリエイターと合意を得るために重要そうだよなぁ...!:thinking:)

One blocker we encountered while trying to scale algorithmic programming was the lack of visibility for editors regarding reader experience and story performance.
**アルゴリズム・プログラミングの規模を拡大しようとしたときに、私たちが遭遇した障害のひとつは、読者の体験やストーリーのパフォーマンスに関する編集者の可視性の欠如**でした。
One of the biggest challenges was feedback from the newsroom that editors and reporters couldn’t tell if their stories would appear in an algorithmic module on the home page.
最大の課題のひとつは、**編集者や記者が自分のストーリーがトップページのアルゴリズムモジュールに表示されるかどうかを知ることができない**というニュースルームからのフィードバックでした。
With the “already-read” filter in place, their stories, which they would have read, wouldn’t show up on the home page.
「既読」フィルターがあるため、彼らが読んだであろうストーリーは、彼らのホームページに表示されません。

To address this, our product designer, engineers and data scientists partnered with home page editors to conceptualize and build a browser extension that allows editors to track all the algorithmic modules on the home page, preview different A/B testing variants, and review all the stories that have been selected and eligible for promotion for each module.
この問題に対処するため、当社のプロダクトデザイナー、エンジニア、データサイエンティストはホームページ編集者と協力し、**編集者がホームページ上のすべてのアルゴリズムモジュールを追跡し、さまざまなA/Bテストバリアントをプレビューし、各モジュールのプロモーション対象として選択されたすべてのストーリーを確認できるブラウザ拡張機能**を構想・構築しました。
Our engineers also built a tool that sends automated alerts to editors about changes in algorithmic programming, including new stories added to the pool and any headline or summary updates.
エンジニアたちは、**アルゴリズム・プログラミングの変更に関する編集者への自動アラートを送信するツール**も構築しました。これには、プールに追加された新しいストーリーや見出しや要約の更新が含まれます。
Additionally, the data science team developed a dashboard to provide near-real-time analytics for stories that were algorithmically programmed.
さらに、データサイエンスチームは、**アルゴリズムでプログラムされたストーリーに対するほぼリアルタイムの分析を提供するダッシュボード**を開発しました。

<!-- 以下は上述の機能たちの総括っぽい内容 -->

After rigorously testing each of these new features and getting editors familiar with these tools and concepts, we permanently implemented algorithmic programming for the features module in the spring of 2024.
これらの新機能のそれぞれを厳密にテストし、編集者にこれらのツールとコンセプトを習熟させた後、**2024年春にfeaturesモジュールのアルゴリズム・プログラミングを永続的に実装**しました。(あ、それでも最近なのか...!:thinking:)
This approach not only streamlined the editorial workflow (daily updates to the module were reduced by a third), it also gave stories that had a longer shelf life more time on the home page, lifting overall engagement.
このアプローチにより、**編集ワークフローが合理化され（モジュールへの日次更新が3分の1に削減されました）**、**より長い寿命を持つストーリーがホームページでより多くの時間を過ごし、全体的なエンゲージメントが向上**しました。
Our product colleagues were delighted that powering the features module with an algorithm also helped increase engagement with our sub-brands such as Wirecutter and Cooking.
当社のプロダクト担当者は、**アルゴリズムを使用してfeaturesモジュールを強化することで、WirecutterやCookingなどのサブブランドとのエンゲージメントが向上**したことに喜んでいました。

<!-- ここまで読んだ! -->

## Taking algorithmic programming further — breaking news and more アルゴリズミック・プログラミングをさらに進化させる - ニュース速報他

The strong foundation we built by incorporating editorial thinking into our algorithms, coupled with the trust we cultivated, led to more demand from the newsroom for more algorithmic programming tools.
編集的思考をアルゴリズムに取り入れ、築いた強固な基盤と、培った信頼が、ニュースルームからより多くのアルゴリズム・プログラミングツールの需要を引き起こしました。
Today, editors are also using a tailored set of algorithmic modules to power a secondary set of stories for a topic or news event.
今日、編集者はまた、トピックやニュースイベントに関する二次的なストーリーを提供するために、カスタマイズされたアルゴリズムモジュールを使用している。
These modules are completely self-service for editors, and have been particularly useful during major news events, when the volume of coverage produced often exceeds the amount of real estate on the home page.
これらのモジュールは、編集者にとって完全なセルフサービスであり、特に重大なニュースイベントの際には、生成されるカバレッジの量がしばしばホームページ上のリアルエステートを超えるため、特に有用です。
(編集者が完全にselfで出面を作るモジュールってこと?? 例えば「話題をまとめよみ」みたいな??:thinking:)

Currently, algorithmic programming recommends stories within individual modules on the home page.
現在、アルゴリズム・プログラミングは、ホームページの個々のモジュール内のストーリーを推薦しています。(=これって多分、編集者に対して出面に載せるべき記事を推薦してる、ってことだよね??:thinking:)
Next, we want to explore and test reordering modules based on a mix of editorial importance, engagement, and personalization signals.
次に、編集上の重要性、エンゲージメント、パーソナライゼーションのシグナルのミックスに基づいてモ**ジュールの並べ替え**を探求し、テストしたいと考えています。
We believe this approach can further improve a reader’s experience and amplify our journalism.
私たちは、このアプローチが読者の体験をさらに向上させ、ジャーナリズムを増幅させると信じている。

<!-- ここまで読んだ! -->

Zhen Yang is a data scientist on the algorithmic recommendations team at The New York Times.
ニューヨーク・タイムズのアルゴリズム・レコメンデーション・チームのデータサイエンティスト。
Celia Eddy, Alex Saez, Derrick Ho, and Christopher Wiggins contributed to this post.
Celia Eddy、Alex Saez、Derrick Ho、Christopher Wigginsが寄稿した。
This article originally appeared on NYT Open and is © 2024 The New York Times Company.
この記事はNYTオープンに掲載されたもので、© 2024 The New York Times Companyの著作です。

<!-- ここまで読んだ! -->
