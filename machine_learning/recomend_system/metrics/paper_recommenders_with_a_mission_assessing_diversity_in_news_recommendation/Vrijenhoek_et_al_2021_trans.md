## link リンク

- https://dl.acm.org/doi/10.1145/3406522.3446019 https://dl.acm.org/doi/10.1145/3406522.3446019

## title タイトル

Recommenders with a Mission: Assessing Diversity in News Recommendations
使命感を持ったレコメンダー： ニュースレコメンデーションにおける多様性の評価

## abstract アブストラクト

News recommenders help users to find relevant online content and have the potential to fulfill a crucial role in a democratic society, directing the scarce attention of citizens towards the information that is most important to them.
ニュースレコメンダーは、ユーザーが関連するオンラインコンテンツを見つけるのを助け、市民の乏しい注意を最も重要な情報に向けるという、民主主義社会における重要な役割を果たす可能性を持っています。
Simultaneously, recent concerns about so-called filter bubbles, misinformation and selective exposure are symptomatic of the disruptive potential of these digital news recommenders.
同時に、いわゆるフィルターバブル、誤報、選択的露出に関する最近の懸念は、こうしたデジタルニュースレコメンダーの破壊的可能性を示すものである。
Recommender systems can make or break filter bubbles, and as such can be instrumental in creating either a more closed or a more open internet.
レコメンダーシステムは、フィルターバブルを作ることも壊すこともできるため、より閉じたインターネット、より開かれたインターネットのどちらにも貢献することができます。
Current approaches to evaluating recommender systems are often focused on measuring an increase in user clicks and short-term engagement, rather than measuring the user's longer term interest in diverse and important information.
現在のレコメンダーシステムの評価アプローチは、多様で重要な情報に対するユーザーの長期的な興味を測定するのではなく、ユーザーのクリック数の増加や短期的なエンゲージメントを測定することに重点を置くことが多い。

This paper aims to bridge the gap between normative notions of diversity, rooted in democratic theory, and quantitative metrics necessary for evaluating the recommender system.
本稿では、民主主義理論に根ざした多様性の規範的な概念と、レコメンダーシステムの評価に必要な定量的な指標とのギャップを埋めることを目的としています。
We propose a set of metrics grounded in social science interpretations of diversity and suggest ways for practical implementations.
私たちは、社会科学的な多様性の解釈に基づいた一連の指標を提案し、実用化のための方法を提案する。

# Introduction 序章

News recommender algorithms have the potential to fulfill a crucial role in democratic society.
ニュースレコメンダーアルゴリズムは、民主主義社会で重要な役割を果たす可能性がある。
By filtering and sorting information and news, recommenders can help users to overcome maybe the greatest challenge of the online information environment: finding　and selecting relevant online content - content they need to be informed citizens, be on top of relevant developments, and have their say [13].
情報やニュースをフィルタリングして分類することで、レコメンダーは、ユーザーがオンライン情報環境の最大の課題である、関連するオンラインコンテンツ（市民として情報を得、関連する動向を把握し、発言するために必要なコンテンツ）を見つけて選択することを支援することができます [13].
Informed by data on what a user likes to read, what people similar to him or her like to read, what content sells best, etc., recommenders use machine learning and AI techniques to make ever smarter suggestions to their users [12, 29, 30, 50].
レコメンダーは、ユーザーが好んで読むもの、同じような人が好んで読むもの、どのようなコンテンツが最も売れるかなどのデータから情報を得て、機械学習やAI技術を使って、ユーザーに対してよりスマートな提案を行います [12, 29, 30, 50]．
For the news media, algorithmic recommendations offer a way to remain relevant on the global competition for attention, create higher levels of engagement with content, develop ways of informing citizens and offer services that people are actually willing to pay for [4].
ニュースメディアにとって、アルゴリズムによるレコメンデーションは、世界的な注目度競争の中で関連性を保ち、コンテンツへの高いエンゲージメントを生み出し、市民に情報を提供する方法を開発し、人々が実際に喜んでお金を払うようなサービスを提供する方法を提供します [4].
With this comes the power to channel attention and shape individual reading agendas and thus new risks and responsibilities.
このことは、注目を集め、個々の読書の意図を形成する力をもたらし、その結果、新たなリスクと責任をもたらすことになります。
Recommender systems can be pivotal in deciding what kind of news the public does and does not see.
リコメンダーシステムは、一般の人々がどのようなニュースを見るか、見ないかを決定する上で極めて重要な役割を果たします。
Depending on their design, recommenders can either unlock the diversity of online information [19, 37] for their users, or lock them into routines of "more of the same", or in the most extreme case into so-called filter bubbles [42] and information sphericules.
レコメンダーは、そのデザインによって、オンライン情報の多様性 [19, 37] をユーザーに開放することも、「同じことの繰り返し」のルーチンに閉じ込めることも、最も極端なケースでは、いわゆるフィルターバブル [42] や情報スフェリカルへと導くこともできる。

The most frequently used key performance indicators, or KPIs, for optimizing recommender systems, assess and aim to maximize short-term user engagement, such as click-through rate or time spent on a page [23].
レコメンダーシステムの最適化のために最も頻繁に使用される重要業績評価指標（KPI）は、クリックスルー率やページ滞在時間など、短期的なユーザーエンゲージメントを評価し、最大化することを目的としている[23]。
Often, these KPIs are defined by data limitations, and by technological and business demands rather than the societal and democratic mission of the media.
多くの場合、これらのKPIは、データの制限や、メディアの社会的・民主的使命ではなく、技術的・ビジネス的要求によって定義されます。
More recently however a process of re-thinking algorithmic recommender design has begun, in response to concerns from users [49], regulators (e.g., EU HLEG [39]), academics, and news organizations themselves [4, 32].
しかし、最近では、ユーザー[49]、規制当局（EU HLEG [39]など）、学者、そして報道機関自身からの懸念に応えて、アルゴリズムの推奨デザインを再考するプロセスが始まっています[4、32]。
Finding ways to develop new metrics and models of more "diverse" recommendations has developed into a vibrant field of experimentation - in academia as well as in the data science and R&D departments of a growing number of media corporations.
より多様なレコメンデーションのための新しい指標やモデルを開発する方法は、アカデミアだけでなく、増え続けるメディア企業のデータサイエンスや研究開発部門でも、活発に実験が行われています。

But what exactly does diverse mean, and how much diversity is ’enough’? As central as diversity (or pluralism, a notion that is often used interchangeably) is to many debates about the optimal design of news recommenders, as unclear it is what diverse recommender design actually entails [31].
しかし、多様性とは一体何を意味し、どれくらいの多様性が「十分」なのだろうか。多様性（または多元主義、しばしば互換的に使用される概念）がニュース推薦者の最適設計に関する多くの議論の中心であるのと同様に、多様な推薦者設計が実際に何を意味するのかが不明である[31]。
In the growing literature that tries to conceptualise and translate diversity into specific design requirements, a gap between the computer science and the normative literature can be observed.
多様性を概念化し、具体的な設計要件に変換しようとする文献が増加する中、コンピュータサイエンスと規範的な文献の間にギャップが見られるようになりました。
While diversity in the computer science literature is often defined as concrete technical metrics, such as the intra-list distance of recommended items [6, 53] (see also Section 2), diversity in the normative sense is about larger societal concepts: democracy, freedom of expressions, cultural inclusion, mutual respect and tolerance [19].
コンピュータサイエンスの文献における多様性は、推奨項目のリスト内距離のような具体的な技術的指標として定義されることが多いが [6, 53] （セクション2も参照）、規範的意味での多様性は、民主主義、表現の自由、文化の受容、相互尊重、許容といった大きな社会的概念についてである [19]．
There is a mismatch between different theoretical understandings of the construct of diversity, similar to the one observed in Fairness research [22].
多様性の構成要素に関する異なる理論的理解の間には、Fairness研究[22]で観察されたものと同様のミスマッチがある。
For news recommenders to be truly able to unlock the abundance of information online and inform citizens better, it is imperative to find ways to overcome the fundamental differences in approaching diversity.
ニュースレコメンダーが真にネット上の豊富な情報を解き放ち、市民により良い情報を提供できるようになるためには、多様性へのアプローチの根本的な違いを克服する方法を見つけることが不可欠である。
There is a need to reconceptualise this central but also elusive concept in a way that both does justice to the goals and values that diversity must promote, as well as facilitates the translation of diversity into metrics that are concrete enough to inform algorithmic design.
多様性が促進すべき目標や価値を正しく理解し、多様性をアルゴリズム設計に反映させるのに十分な具体的指標に変換することを容易にする方法で、この中心的だが捉えどころのない概念を再認識する必要があるのです。

This paper describes the efforts of a team from computer science, communication science, and media law and policy experts, to bridge this gap between normative and computational approaches towards diversity, and translate diversity, as a normative concept, to a concrete set of metrics that can be used to evaluate and/or compare different news recommender designs.
本論文では、コンピュータサイエンス、コミュニケーションサイエンス、メディア法・政策の専門家からなるチームが、多様性に関する規範的アプローチと計算機的アプローチの間のギャップを埋め、規範的概念としての多様性を、異なるニュース推薦デザインの評価や比較に使用可能な具体的メトリクスセットに変換する取り組みを説明します。

We first conceptualise diversity from a technical point of view (Section 2) and from a social science interpretation, including its role in democratic models (Section 3).
まず、技術的な観点から多様性を概念化し（第2節）、民主主義モデルにおける役割を含む社会科学的解釈から多様性を概念化する（第3節）。
In Section 4 we expand upon the social science notion of diversity, and propose five metrics grounded in Information Retrieval that reflect our normative approach.
第4章では、社会科学的な多様性の概念を拡張し、私たちの規範的なアプローチを反映した情報検索に基づく5つの指標を提案します。
We cover the limitations of the proposed metrics and this approach in Section 5.
セクション5では、提案したメトリクスと本アプローチの限界について取り上げる。
We conclude with detailing our implementation of the metrics and the steps to undertake as a media company when intending to adopt this normative notion of diversity in practice.
最後に、このダイバーシティの規範となる概念を実際に採用しようとする場合、メディア企業としてどのような手順を踏めばよいのか、私たちが実施したメトリクスの詳細を説明します。

# A technical conception of diversity in news recommenders ニュースレコメンダーにおける多様性の技術的概念

Typically, generating a recommendation is seen as a reranking problem.
一般に、推薦文の生成は、リランキング問題として捉えられている。
Given a set of candidate items, the goal is to present these items in such a way that the user finds the item he or she is most interested in at the top, followed by the second-most interesting one, and so on.
候補となるアイテムのセットがある場合、ユーザーが最も興味のあるアイテムを一番上に見つけ、次に2番目に興味のあるアイテムが続くように、これらのアイテムを提示することが目標です。
How well this recommendation reflects the actual interest of the user is called the accuracy of the recommendation.
この推薦文がどれだけユーザーの実際の興味を反映しているかを、推薦文の精度と呼びます。
Content-based approaches aim to maximize this accuracy by looking at the type of items that the user has interacted with before and recommend similar ones.
コンテンツベースのアプローチでは、ユーザーが以前に接したアイテムの種類を調べ、類似のものを推薦することで、この精度を最大化することを目指しています。
In the context of news recommendations, one could think of finding topics or overall texts that are similar to what is in the user’s reading history.
ニュースレコメンデーションの文脈では、ユーザーの読書履歴にあるものに近いトピックやテキスト全体を見つけることが考えられる。
On the other hand, in collaborative filtering approaches, the algorithm considers what other users similar to the user in question have liked, and recommends those.
一方、協調フィルタリングアプローチでは、当該ユーザーに類似した他のユーザーがどのようなものを気に入っているかを考慮し、それらを推薦するアルゴリズムが採用されています。
Most state-of-the-art systems are hybrids of these approaches.
最新のシステムの多くは、これらのアプローチのハイブリッドです。
Evaluation of the system can be done in both an online and offline fashion; offline often includes testing the system on a piece of held-out data on its accuracy, whereas online evaluation monitors for increases or decreases of user interactions and clickthrough rates following the issued recommendations [2].
システムの評価は、オンラインとオフラインの両方で行うことができます。オフラインでは、多くの場合、その精度について、保有するデータの一部でシステムをテストします。一方、オンライン評価は、発行された勧告に従ってユーザーのインタラクションとクリックスルー率が増加または減少することを監視します [2] 。
However, this approach by its definition unduly promotes the items similar to what a user has seen before, locking the user in a feedback loop of "more of the same" [35].
しかし、このアプローチは、その定義上、ユーザーが以前に見たものと似たものを不当に宣伝し、ユーザーを「同じものをもっと」というフィードバックループに閉じ込めることになります[35]。
It also introduces a so-called "confounding bias" [7], which happens when an algorithm attempts to model user behavior when the algorithm itself influences that behavior.
また、アルゴリズムがユーザーの行動をモデル化しようとしたときに、アルゴリズム自体がその行動に影響を与える、いわゆる「交絡バイアス」[7]が発生することも指摘されています。
To tackle this in many currently operational systems "beyond-accuracy" metrics diversity, novelty, serendipity and coverage are introduced.
そのため、現在運用されている多くのシステムでは、「精度を超える」指標として、多様性、新規性、セレンディピティ、カバレッジが導入されています。
Diversity reflects how different the items within the recommendation set are from each other.
多様性とは、推薦セット内のアイテムが互いにどれだけ異なるかを反映したものです。
One intuitive usecase can be found in the context of ambiguous search queries.
直感的な使用例としては、あいまいな検索クエリの文脈があります。
A user searching for "orange" should receive results about the color, the fruit, the telecom company, the Dutch royal family, and the river in Namibia, and not just about the one the system thinks he or she is most likely to be interested in.
オレンジ」を検索したユーザーは、色、果物、通信会社、オランダ王室、ナミビアの川に関する結果を受け取るべきで、システムが最も興味を持ちそうだと思うものだけを受け取るべきではありません。
The challenge then lies in how to define this difference or distance.
そして、この違いや距離をどのように定義するかが課題となる。
In the context of news recommendations many different approaches exist, such as using a cosine similarity on a bag of words model or by calculating the distance between the article’s topics [58].
ニュース推薦の文脈では、Bag of wordsモデルのコサイン類似度を使用したり、記事のトピック間の距離を計算するなど、多くの異なるアプローチが存在する[58]。
The concepts of novelty and serendipity are strongly linked.
ノベルティとセレンディピティという概念は強く結びついています。
Novelty reflects the likeliness that the user has never seen this item before, whereas serendipity reflects whether a user was positively surprised by the item in question.
新規性は、ユーザーがそのアイテムを見たことがない可能性を、セレンディピティは、ユーザーがそのアイテムにポジティブな驚きを覚えたかどうかを反映します。
However, an item can be novel without being serendipitous (such as the weather forecast), and an item may also be serendipitous without being novel (such as an item that has been seen a long time ago, but becomes relevant again in light of recent events).
しかし、セレンディピティでなくても新規性のあるもの（天気予報など）もあれば、新規性がなくてもセレンディピティであるもの（ずっと前に見たことがあるが、最近の出来事に照らし合わせて再び関連性が出てきたものなど）もあるのです。
A common approach to improving novelty and serendipity is by unlocking the "long tail" content of the system, while still optimizing for user accuracy.
新規性やセレンディピティを向上させるための一般的なアプローチは、ユーザーの精度を最適化しつつ、システムの「ロングテール」コンテンツを解き放つことです。
The long tail refers to the "lesser known" content in the system, that is less popular and therefore seen by less users.
ロングテールとは、システム内のコンテンツのうち、人気がなく、そのため見るユーザーも少ない、「あまり知られていない」コンテンツのことを指します。
By recommending less popular content the recommender systems increase the chance that an item is actually novel to a user.
レコメンダーシステムは、人気のないコンテンツを推薦することで、そのアイテムがユーザーにとって実際に目新しいものである確率を高めることができます。
Lastly, coverage reflects to what extent all the items available in the system have been recommended to at least a certain number of users.
最後に、カバレッジは、システムで利用可能なすべてのアイテムが、少なくとも一定数のユーザーにどの程度推奨されているかを反映するものです。
This metric is naturally strongly influenced by the novelty of the recommendations, as increasing the visibility of lesser-seen items increases the overall coverage of all items.
この指標は当然ながらレコメンデーションの新規性に強く影響され、あまり見られていないアイテムの可視性を高めることで、全アイテムのカバー率を高めることができる。

# A democrative conception of diversity in news recommenders ニュースレコメンダーにおける多様性の民主主義的概念

What becomes apparent from the overview in Section 2 is that although there are various attempts to conceptualize evaluation metrics beyond accuracy in the computer science literature, these metrics are constructed for the broad field of recommendation systems, and are therefore not only relevant in the context of news, but also for music, movies, web search queries and even online dating.
第2節の概要から明らかになるのは、コンピュータサイエンスの文献では、精度を超えた評価指標を概念化する様々な試みがなされているが、これらの指標は推薦システムという広い分野に対して構築されているため、ニュースという文脈に限らず、音楽、映画、ウェブ検索クエリ、さらにはオンラインデートにも関連するということである。
However, what they win in generalizability, they lose in specificity.
しかし、一般性では勝っていても、特異性では負けています。
They are not grounded in, and do not refer back to the normative understanding of diversity in the media law, fundamental rights law, democratic theory and media studies/communication science literature, as is also demonstrated in Loecherbach et al.[31].
また、Loecherbachら[31]が示すように、メディア法、基本権法、民主主義理論、メディア研究/コミュニケーション科学の文献における多様性の規範的理解に根拠がなく、言及もしない。

Before we define more quantitative metrics to assess diversity in news recommendation, we first offer a conceptualization of diversity.
ニュース推薦における多様性を評価するためのより定量的な指標を定義する前に、まず多様性の概念的な説明を行う。
Following the definition of the Council of Europe, diversity is not a goal in itself, it is a concept with a mission, and it has a pivotal role in promoting the values that define us as a democratic society.
欧州評議会の定義に従えば、多様性はそれ自体が目的ではなく、使命を持った概念であり、民主主義社会として私たちを定義する価値観を促進する上で極めて重要な役割を担っているのです。
These values may differ according to different democratic approaches.
これらの価値観は、民主主義のアプローチの違いによって異なる場合があります。
This article builds on a conceptualisation of diversity in recommendations that has been developed by Helberger [19].
本稿では、Helberger[19]が開発したレコメンデーションにおける多様性の概念に基づき説明する。
Here, Helberger combines the normative understanding of diversity, meaning what should diverse recommendations look like, with more empirical conceptions, meaning what is the impact of diverse exposure on users.
ここでヘルバーガーは、多様なレコメンデーションはどうあるべきかという規範的な理解と、多様な露出がユーザーに与える影響とは何かという、より実証的な概念を組み合わせている。
There are many theories of democracy, but the paper by Helberger focuses on 4 of the most commonly used theories when talking about the democratic role of the media: Liberal, Participatory, Deliberative and Critical theories of democracy (see also [9, 10, 25, 48]).
民主主義には多くの理論があるが、Helbergerの論文では、メディアの民主的役割について語る際に最もよく使われる4つの理論に焦点をあてている： 自由主義、参加主義、熟議主義、批判主義である（[9, 10, 25, 48]も参照）。

It is important to note that no model is inherently better or worse than another.
ここで重要なのは、どのモデルも他のモデルより本質的に優れている、あるいは劣っているということはないということです。
Which model is followed is something that should be decided by the media companies themselves, following their mission and dependent on the role they want to play in a democratic society.
どのモデルに従うかは、メディア企業自身が、その使命に従い、民主主義社会で果たしたい役割に応じて決めるべきことである。

## The Liberal model リベラルモデル

In liberal democratic theory, individual freedom, including fundamental rights such as the right to privacy and freedom of expression, dispersion of power but also personal development and autonomy of citizens stands central.
自由民主主義理論では、プライバシー権や表現の自由などの基本的な権利を含む個人の自由、権力の分散だけでなく、市民の人格形成や自律が中心となっています。
The liberal model is in principal sympathetic to the idea of algorithmic recommendations and considers recommenders as tools to enable citizens to further their autonomy and find relevant content.
リベラルモデルは、基本的にアルゴリズムによるレコメンデーションの考え方に共感し、レコメンダーを市民の自主性を高め、関連するコンテンツを見つけることを可能にするツールとみなしています。
The underlying premise is that citizens know for themselves best what they need in terms of self-fulfillment and exercising their fundamental rights to freedom of expression and freedom to hold opinions, and even if they do not, this is only to a limited extent a problem for democracy.
大前提として、自己実現や表現の自由・意見表明の自由といった基本的権利の行使に必要なことは、市民が自分自身で一番よく知っており、たとえそうでなくても、それは民主主義の問題として限られた範囲に過ぎない。
This is because the normative expectations of what it means to be a good citizen are comparatively low and there is a strict division of tasks, in which "political elites [...] act, whereas citizens react"[48].
それは、「良い市民とは何か」という規範的期待が比較的低く、「政治的エリートが[...]行動し、市民が反応する」という厳しい役割分担が存在するからである[48]。

Under such liberal perspective, diversity would entail a userdriven approach to diversity that reflects citizens interests and preferences not only in terms of content, but also in terms of for example style, language and complexity.
このようなリベラルな視点に立つと、多様性は、コンテンツだけでなく、例えばスタイルや言語、複雑さなど、市民の関心や好みを反映したユーザー主導のアプローチとなる。
The liberal recommender is required to inform citizens about prominent issues, especially during key democratic moments such as election time, but else it is expected to take little distance from personal preferences.
リベラルなレコメンダーは、特に選挙のような民主主義の重要な局面では、市民に目立つ問題を知らせることが求められるが、それ以外では個人の好みとは距離を置くことが期待される。
It is perfectly acceptable for citizens to be consuming primarily cat videos and celebrity news, as long as doing so is an expression of their autonomy.
市民が猫の動画や有名人のニュースを中心に消費していても、それが市民の自律性の表現である限り、全く問題ありません。

Summary.
概要
The liberal model of democracy promotes self-development and autonomous decision making.
自由主義的な民主主義のモデルは、自己啓発と自律的な意思決定を促進します。
As such, a news recommender following a liberal approach should focus on the following criteria:
そのため、リベラルなアプローチによるニュースレコメンダーは、次のような基準を重視する必要があります：

- Facilitating the specialization of a user in an area of his/her choosing ユーザーが選択した分野での専門性を高めること。

- Tailored to a user’s preferences, both in terms of content and in terms of style コンテンツもスタイルも、ユーザーの好みに合わせてカスタマイズできる

## The Participatory model 参加型モデル

An important difference between the liberal and the participatory model of democracy is what it means to be a good citizen.
民主主義のリベラルモデルと参加型モデルの重要な違いは、「良い市民であること」とは何かということです。
Under participatory conceptions, the role of (personal) freedom and autonomy is to further the common good, rather than personal self-development [20].
参加型の概念では、（個人の）自由と自律の役割は、個人の自己開発よりも、むしろ共通善を促進することである[20]。
Citizens cannot afford to be uninterested in politics because they have an active role to play in helping the community to thrive [48].
市民は、地域社会の繁栄に貢献する積極的な役割を担っているのだから、政治に無関心でいるわけにはいかないのだ[48]。
Accordingly, the media, and by extension news recommenders must do more than to give citizens ’what they want’, and instead provide citizens with the information they need to play their role as active and engaged citizens [1, 16, 24, 26], and to further the participatory values, such as inclusiveness, equality, participation, tolerance.
したがって、メディア、ひいてはニュース推薦者は、市民が「欲しいもの」を与えるだけでなく、市民が活動的で関与する市民としての役割を果たすために必要な情報を提供し [1, 16, 24, 26] 、包括性、平等、参加、寛容といった参加型の価値を促進することが必要であると言える。
Participatory recommenders must also proactively address the fear of missing out on important information and depth, and the concerns about being left out.
参加型レコメンダーは、重要な情報や深みを見逃す恐れや、取り残されることへの不安にも積極的に対処する必要があります。
Here the challenge is to make a selection that gives a fair representation of different ideas and opinions in society, while also helping a user to gain a deeper understanding, and feeling engaged, rather than confused.
ここでは、社会のさまざまな考えや意見を公平に表現しながら、ユーザーがより深く理解し、混乱することなく夢中になれるようなセレクションを作ることが課題です。
This also involves that recommenders are able to respond to the different needs of users in which information is being presented.
これは、レコメンダーが、情報が提示されるユーザーのさまざまなニーズに対応できるようにすることにもつながります。
The form of presentation is an aspect that is often neglected in discussions around news recommender diversity, ignoring the fact that different people have different preferences and cognitive abilities to process information.
プレゼンテーションの形態は、ニュースレコメンダーの多様性をめぐる議論において、人によって嗜好や情報を処理する認知能力が異なるという事実を無視して軽視されがちな側面がある。
Accordingly, the media should ’frame politics in a way that mobilizes people’s interests and participation in politics’.
従って、メディアは「人々の関心と政治への参加を動員するような形で政治を組み立てる」べきである。
Strömbäck [48] and Ferree et al.[15] speak of ’empowerment’: to be truly empowering, media content needs to be presented in different forms and styles [8, 15, 57].
Strömbäck［48］とFerreeら［15］は「エンパワーメント」について述べている：真にエンパワーメントするためには、メディアコンテンツは異なる形態やスタイルで提示される必要がある［8、15、57］。
By extension, this means that diversity is not only a matter of the diversity of content, but also of communicative styles.
ひいては、多様性とは、コンテンツの多様性だけでなく、コミュニケーションスタイルの多様性でもあることを意味します。
What would then characterize diversity in a participatory recommender are, on the one hand, active editorial curation in the form of drawing attention to items that citizens ’should know’, taking into account inclusive and proportional representation of main political/ideological viewpoints in society; a focus on political content/news, but also: non-news content that speaks to broader public and, on the other hand, a heterogeneity of styles and tones, possibly also emotional, empathetic, galvanizing, reconciliatory.
参加型レコメンダーの多様性を特徴づけるものは、一方では、社会の主要な政治的／思想的視点の包括的かつ比例的な代表性を考慮しながら、市民が「知るべき」項目に注意を向けるという形で、積極的に編集キュレーションを行うこと、政治コンテンツ／ニュースに焦点を当てつつ、より広い市民に語りかけるニュース以外のコンテンツも扱うこと、他方では、スタイルやトーンの異質さ、おそらく感情、共感、活気、和解も含まれます。

Summary.
概要
The participatory model of democracy aims to enable people to play an active role in society.
参加型民主主義のモデルは、人々が社会で積極的な役割を果たすことができるようにすることを目的としています。
It values the idea of the ‘common good’ over that of the individual.
個人よりも「共通善」という考え方を大切にしています。
Therefore, a participatory recommender should follow the following principles:
したがって、参加型レコメンダーは、以下の原則に従うべきである：

- Different users do not necessarily see the same articles, but they do see the same topics. 異なるユーザーが必ずしも同じ記事を見るとは限りませんが、同じトピックを見ることはあります。

- Article’s complexity is tailored to a user’s preference and capability 記事の複雑さは、ユーザーの好みや能力に合わせて調整される

- Reflects the prevalent voices in society 社会に浸透している声を反映させる

- Empathetic writing style 共感できる文体

## The Deliberative model デリバティブモデル

The participatory and the deliberative models of democracy have much in common (compare Ferree et al.[15]).
民主主義の参加型モデルと熟議型モデルには多くの共通点がある（Ferreeら[15]を参照）。
Also in the deliberative or discursive conceptions of democracy, community and active participation of virtuous citizens stands central.
また、民主主義の熟議的概念や言説的概念では、コミュニティや徳の高い市民の積極的な参加が中心となっています。
One of the major differences is that the deliberative model operates on the premise that ideas and preferences are not a given, but that instead we must focus more on the process of identifying and negotiating and, ultimately, agreeing on different values and issues [15, 25].
大きな違いの一つは、熟議モデルが、アイデアや好みは所与のものではなく、代わりに、異なる価値観や問題点を特定し、交渉し、最終的に合意するプロセスにもっと焦点を当てなければならないという前提で運営されていることです［15、25］。
Political and public will formation is not simply the result of who has the most votes or ’buyers’, but it is the result of a process of public scrutiny and intensive reflection [20].
政治的・公的意志の形成は、単に誰が最も多くの票や「買い手」を持っているかという結果ではなく、国民の監視と集中的な考察のプロセスの結果である [20] 。
This involves a process of actively comparing and engaging with other also contrary and opposing ideas [34].
これには、他の反対意見や対立意見と積極的に比較し、関与するプロセスが含まれます[34]。
The epistemological shift from information to deliberation has important implications for the way the role of news recommenders can be conceptualised.
情報から熟議への認識論の転換は、ニュースレコメンダーの役割を概念化する上で重要な意味を持つ。
Under a deliberative perspective, it is not enough to ’simply’ inform people.
熟議的な観点では、「単に」知らせるだけでは不十分である。
The media need to do more, and has an important role in "promoting and indeed improving the quality of public life - and not merely reporting on and complaining about it" [9].
メディアはより多くのことをする必要があり、「公共生活の質を促進し、実際に向上させる-単に報告したり文句を言ったりするだけではない-」という重要な役割を担っている[9]。
Strömbäck [48] goes even further and demands that the media should also "actively foster political discussions that are characterised by impartiality, rationality, intellectual honesty and equality among the participants".
Strömbäck［48］はさらに踏み込んで、メディアは「公平性、合理性、知的誠実さ、参加者の平等性を特徴とする政治的議論を積極的に促進」することも要求している。
Diversity in the deliberative conception has the important task of confronting the audience with different and challenging viewpoints that they did not consider before, or not in this way [34].
熟議概念における多様性は、聴衆に、以前は考えなかった、あるいはこのように考えなかった、異なる、挑戦的な視点を突きつけるという重要な任務を持つ[34]。
Concretely, this means that a deliberative recommender should include a higher share of articles presenting various perspectives, diversity of emotions, range of different sources; it should strive for equal representation, as well as on recommending items of balanced content, commentary, discussion formats, background information; potentially some prominence for public service media content (as the mission of many public service media includes the creation of a deliberative public sphere), as well as a preference for rational tone, consensus seeking, inviting commentary and reflection.
具体的には、審議型レコメンダーは、さまざまな視点、感情の多様性、さまざまなソースを提示する記事の比率を高め、平等な表現、バランスのとれたコンテンツ、解説、議論形式、背景情報のアイテムを推奨するよう努めるべきであるということである。

Summary.
概要
The focus of the deliberative recommender is on presenting different opinions and values in society, with the goal of coming to a common consensus or agreeing on different values.
審議型レコメンダーは、社会におけるさまざまな意見や価値観を提示し、共通のコンセンサスを得ること、あるいは異なる価値観に合意することを目的としています。

- Focus on topics that are currently at the center of public debate 現在、社会的な議論の中心となっているトピックに焦点を当てる。

- Within those topics, present a plurality of voices and opinions そのテーマの中で、複数の声や意見を提示すること

- Impartial and rational writing style 公平で合理的な文体

## The Critical model クリティカルモデル

A main thrust of criticism of the deliberative model is that it is too much focused on rational choice, on drawing an artificial line between public and private, on overvaluing agreement and disregarding the importance of conflict and disagreement as a form of democratic exercise [26].
熟議モデルに対する批判の主な柱は、合理的な選択に焦点を当てすぎ、公的と私的の間に人工的な線を引き、合意を過大評価し、民主主義の行使の一形態としての対立や不一致の重要性を軽視している、というものである[26]。
The focus on reason and tolerance muffles away the stark, sometimes shrill contrasts and hidden inequalities that are present in society, or even discourage them from developing their identity in the first place.
理性と寛容に焦点を当てることで、社会に存在する厳しい、時には耳障りなコントラストや隠れた不平等を消し去り、あるいは、そもそも自分のアイデンティティを確立することを思いとどまらせてしまうのです。
Accordingly, under more radical or critical perspectives, citizens should look beyond the paint of civil and rational deliberation.
したがって、より急進的な、あるいは批判的な視点に立つと、市民は市民的で合理的な審議のペイントを超えたところに目を向けるべきである。
They should discover and experience the many marginalised voices of those "who are ’outsiders within’ the system"[15], and when doing so critically reflect on reigning elites and their ability to give these voices their rightful place in society.
彼らは「システム内の "アウトサイダー "である人々」[15]の多くの周縁化された声を発見し経験し、そうすることで支配するエリートやこれらの声を社会における正当な位置に与える彼らの能力について批判的に考察するべきである。
Diverse critical recommenders hence do not simply give people what they want.
そのため、多様なクリティカル・レコメンダーは、人々が望むものをただ与えるだけではありません。
Instead, they actively nudge readers to experience otherness, and draw attention to the marginalised, invisible or less powerful ideas and opinions in society.
その代わりに、読者に他者性を体験するよう積極的に働きかけ、社会から疎外された、目に見えない、あるいは力のない考え方や意見に注意を向けさせる。
And again, it is not only the question of what kinds of content are presented but also the how: whereas in the deliberative and also the participatory model, much focus is on a rational, reconciliary and measured tone, critical recommenders would also offer room for alternative forms of presentations: narratives that appeal to the ’normal’ citizen because they tell an everyday life story, emotional and provocative content, even figurative and shrill tones - all with the objective to escape the standard of civility and the language of the stereotypical "middle-aged, educated, blank white man"[56].
審議型や参加型では、理性的、調整的、慎重な表現が重視されるのに対して、批判的な推薦者は、別の表現形式を受け入れる余地も提供する： 日常生活の物語を語ることで「普通の」市民にアピールする物語、感情的で挑発的な内容、比喩的で荒々しいトーンなど、すべて礼節の基準やステレオタイプの「中年の、教育を受けた、無口な白人」の言葉から逃れることを目的とするものである[56]。

Summary.
概要
The critical recommender aims to provide a platform to those voices and opinions that would otherwise go unheard.
クリティカルレコメンダーは、普段は聞くことのできない声や意見に、プラットフォームを提供することを目的としています。
From a critical democracy perspective on diversity, recommenders should be optimized on the following principles:
多様性に関する批判的民主主義の観点から、レコメンダーは以下の原則に基づき最適化されるべきです：

- Emphasis on voices from marginalized groups 限界集落からの声の重視

- Emotional writing style エモーショナルな文体

# Diversity metrics 多様性の指標

The democratic models described in Section 3 lead to different conceptualizations of diversity as a value, which again translate into different diversity expectations for recommender systems.
セクション3で説明した民主的なモデルは、価値としての多様性の異なる概念化をもたらし、それがまた推薦システムに対する異なる多様性の期待に変換される。
In this section, we propose five metrics that follow directly from these expectations, grounded in democratic theory and adapted from existing Information Retrieval metrics: Calibration, Fragmentation, Activation, Representation and Alternative Voices.
このセクションでは、民主主義理論に基づき、既存の情報検索メトリクスを応用して、これらの期待から直接的に導かれる5つのメトリクスを提案します： Calibration、Fragmentation、Activation、Representation、Alternative Voicesである。
For each of these metrics, we explain the concept and link to democratic theory.
それぞれの指標について、その概念や民主主義理論との関連性を説明しています。
Furthermore we make a suggestion for operationalization, but note that this work is an initial outline and that much work still needs to be done.
さらに、運用のための提案を行いますが、この作業は初期のアウトラインであり、まだ多くの作業が必要であることに留意してください。
Future work should include more work on the validity of the metrics, for example by following the measurement models specified in Jacobs and Wallach [22].
今後の課題としては、例えばJacobs and Wallach [22]で規定されている測定モデルに従って、測定基準の妥当性についてさらに検討する必要があります。
Lastly we mention a number of the limitations of the currently proposed metrics and their operationalizations.
最後に、現在提案されているメトリクスとその運用の限界について言及します。

Table 1 provides an overview of the different models, metrics and their expected value ranges.
表1は、さまざまなモデル、指標、およびそれらの期待値範囲の概要を示している。
Note that not all metrics are relevant to all models.
なお、すべてのメトリクスがすべてのモデルに関連するわけではありません。

Before explaining the metrics, we define the following variables that are relevant to multiple metrics:
メトリクスを説明する前に、複数のメトリクスに関連する以下の変数を定義します：

- 𝑝: The list of articles the recommender system could make its selection from, also referred to as the ’pool’ 𝑝: 推薦システムが選択することができる記事のリストで、「プール」とも呼ばれます。

- 𝑞: The unordered list of articles in the recommendation set 𝑞: 推薦セットに含まれる記事の順序不同のリスト

- 𝑄: The ordered list of articles in the recommendation set 𝑄: 推薦セットに含まれる記事の順序付きリスト

- 𝑟: The list of articles in a user’s reading history 𝑟: ユーザーの読書履歴にある記事のリスト

## Calibration 

The Calibration metric reflects to what extent the issued recommendations reflect the user’s preferences.
Calibrationは、発行されたレコメンデーションがユーザーの好みをどの程度反映しているかを示す指標です。
A score of 0 indicates a perfect Calibration, whereas a higher score indicates a larger divergence from the user’s preferences.
スコア0は完璧なキャリブレーションを意味し、スコアが高いほどユーザーの好みとの乖離が大きいことを意味します。

### Explanation. 説明があります。

Calibration is a well-known metric in traditional recommender system literature [47].
キャリブレーションは、従来のレコメンダーシステムの文献ではよく知られた指標である[47]。
It is calculated by measuring the difference in distributions of categorical information, such as topics in the news domain or genres in the movie domain, between what is currently recommended to the user and what the user has consumed in the past.
ニュース領域ではトピック、映画領域ではジャンルといったカテゴリー情報の分布において、現在ユーザーに推奨されているものと、過去にユーザーが消費したものとの差を測定することで算出されるものです。
However, we extend our notion of calibration beyond topicality or genre.
しかし、私たちは、キャリブレーションの概念を、話題性やジャンルの枠を超えて拡張しています。
News recommendations can also be tailored to the user in terms of article style and complexity, allowing the reader to receive content that is attuned to their information needs and processing preferences.
また、記事のスタイルや複雑さなど、ユーザーに合わせたニュース推薦が可能で、読者は自分の情報ニーズや処理の好みに合わせたコンテンツを受け取ることができるようになります。
This may be split up within different topics; a user may be an expert in the field of politics but less so in the field of medicine, and may want to receive more complex articles in case of the first, and less in case of the second.
政治には詳しいが、医療にはあまり詳しくないというような場合、前者の場合はより複雑な記事を、後者の場合はより少ない記事を受け取りたいと考えるかもしれません。

### In the context of democratic recommenders. 民主的な推薦者の文脈で。

The Calibration metric is most significant for recommenders following the Liberal and Participatory model.
Calibration」指標は、「Liberal」「Participatory」モデルのレコメンダーにおいて最も重要である。
The aim of the Liberal model is to facilitate user specialization, and assumes that the user eventually knows best what they want to read.
リベラルモデルの目的は、ユーザーの特殊化を促進することであり、最終的にユーザーが読みたいものを最もよく知っていることを前提としています。
In these models, we expect the Calibration scores to be closer to 0.
これらのモデルでは、キャリブレーションのスコアが0に近くなることが予想されます。
On the other hand, the Participatory model favors the common good over the individual.
一方、「参加型」は、個人よりも共通の利益を優先するモデルです。
We therefore expect a higher degree of divergence in Calibration, at least when considered in light of topicality.
したがって、少なくとも話題性を考慮すると、キャリブレーションではより高度な乖離が予想されます。
Both models, but especially the Participatory model, require that the user receives content that is tailored to their needs in terms of article complexity, and in this context we expect a Calibration score that is closer to zero.
どちらのモデルも、特に参加型モデルでは、記事の複雑さという点でユーザーのニーズに合わせたコンテンツを受け取る必要があり、この文脈では、0に近いCalibrationスコアが予想されます。

### Operationalization. オペレーション化。

For the operationalization of a recommender’s Calibration score it is important to have information on not only an article’s topic and complexity, which can potentially be automatically extracted from an article’s body (see for example Feng et al.[14] and Kim and Oh [28]), but also on the user’s preferences regarding this matter.
レコメンダーのキャリブレーションスコアを運用するためには、記事の本文から自動的に抽出できる可能性のある、記事のトピックと複雑さに関する情報だけでなく（例えば、Fengら[14]とKim and Oh [28]を参照）、この問題に関するユーザーの好みに関する情報も重要である。
Note that topicality can be both generic (politics, entertainment, sports, etc) and more specific (climate change, Arsenal).
なお、話題性には一般的なもの（政治、娯楽、スポーツなど）と、より具体的なもの（気候変動、アーセナルなど）がある。
In light of democratic theory more fine-grained information is preferable, but this is not always available.
民主主義の理論に照らせば、よりきめ細かい情報が望ましいのですが、必ずしもそうとは限りません。
Steck [47] uses the Kullback-Leibler divergence between two probability distributions as Calibration metric, as follows:
Steck [47]では、2つの確率分布間のKullback-Leibler divergenceをCalibration metricとして、以下のように使用しています：

$$
$$

where 𝑟(𝑐|𝑢) is the distribution of categorical information 𝑐 across the articles consumed by the user in the past, and 𝑞˜(𝑐|𝑢) is an approximation of 𝑞(𝑐|𝑢) (necessary since KL divergence diverges if 𝑞(𝑐|𝑢) = 0), which is the distribution of the categories c across the current recommendation set.
𝑢) is the distribution of categorical information 𝑐 across the articles consumed by the user in the past, and 𝑞˜(𝑐
As mentioned before, a score of 0 indicates that there is no divergence between the two distributions, meaning they are identical.
前述したように、スコア0は2つの分布の間に乖離がない、つまり同一であることを意味します。
The higher the Calibration score, the larger the divergence.
Calibrationスコアが高いほど、乖離は大きくなります。
As KL divergence can yield very high scores when dividing by numbers close to zero, outliers can greatly influence the average outcome.
KLダイバージェンスは、ゼロに近い数値で割ると非常に高いスコアが得られるため、異常値は平均的な結果に大きく影響します。
Therefore, the aggregate Calibration score is calculated by taking the median of all the Calibration scores for individual users.
そのため、個々のユーザーのCalibrationスコアの中央値を取ることで、Calibrationスコアの総和を算出します。

### Limitations. 制限があります。

This approach is tailored to categorical data, but sometimes our data may be numerical rather than categorical, for example in the case of article complexity.
このアプローチはカテゴリーデータに適していますが、例えば記事の複雑さのように、カテゴリーデータではなく数値データである場合もあります。
In these cases, a simple distance measure may suffice over the more complex KullbackLeibler divergence.
このような場合、より複雑なカルバックライブラー発散よりも、単純な距離測定で十分な場合があります。

## Fragmentation フラグメンテーション

The Fragmentation metric denotes the amount of overlap between news story chains shown to different users.
Fragmentationメトリクスは、異なるユーザーに表示されるニュースストーリーチェーン間の重複の量を示す。
A Fragmentation score of 0 indicates a perfect overlap between users, whereas a score of 1 indicates no overlap at all.
Fragmentationのスコアが0であれば、ユーザー同士が完全に重なっていることを示し、スコアが1であれば、全く重なっていないことを示します。

### Explanation. 説明があります。

News recommender systems create a recommendation by filtering from a large pool of available news items.
ニュースレコメンダーシステムは、利用可能なニュースアイテムの大規模なプールからフィルタリングすることによって推薦を作成します。
By doing so they may stimulate a common public sphere, or create smaller and more specialized ’bubbles’.
そうすることで、共通の公共圏を刺激したり、より小さく、より専門的な「バブル」を作り出したりすることができる。
This may occur both in terms of topics recommended, which is the focus of the Fragmentation metric, and in terms of presented perspectives, which will be later explained in the Representation metric.
これは、Fragmentationの指標で注目される推奨トピックと、Representationの指標で後述する提示された視点の両面で発生する可能性があります。
Fragmentation specifically compares differences in recommended news story chains, or sets of articles describing the same issue or event from different perspectives, writing styles or points in time [38], between users; the smaller the difference, the more aware the users are of the same events and issues in society, and the more we can speak of a joint agenda.
フラグメンテーションとは、具体的には、ユーザー間で推奨されるニュースストーリーチェーン（同じ問題や出来事を異なる視点、書き方、時点から記述した記事の集合）[38]の違いを比較するもので、違いが小さいほど、ユーザーは社会における同じ出来事や問題をより認識しており、共同課題を語ることができるとしています。
When the news story chains shown to the users differ significantly, the public sphere becomes more fragmented, hence the term Fragmentation.
ユーザーに表示されるニュースストーリーの連鎖が大きく異なると、公共圏がより細分化されるため、Fragmentationと呼ばれるようになった。

### In the context of democratic recommenders. 民主的な推薦者の文脈で。

Both the Participatory and Deliberative models favor a common public sphere, and therefore a Fragmentation score that is closer to zero.
参加型と熟議型の両モデルとも、共通の公共圏を好むため、フラグメンテーションのスコアはゼロに近くなります。
The Liberal model on the other hand promotes the specialization of the user in their area of interest, which in turn causes a higher Fragmentation score.
一方、Liberalモデルは、ユーザーの興味ある分野への特化を促進するため、Fragmentationスコアが高くなります。
Finally the Critical model, with its emphasis on drawing attention to power imbalances prevalent in society as a whole, calls for a low Fragmentation score.
最後に、社会全体の力の不均衡に注目することに重点を置く「クリティカル」モデルは、「フラグメンテーション」のスコアを低く設定します。

### Operationalization. オペレーション化。

This metric requires that individual articles can be aggregated into higher-level news story chains over time.
この指標は、個々の記事が時間と共により高いレベルのニュースストーリーチェーンに集約されることを必要とします。
This can be done through manual annotation or automated extraction process.
これは、手動によるアノテーションや自動抽出処理によって行うことができます。
Two unsupervised learning approaches for doing this automatically can be found in Nicholls and Bright [38] and Trilling and van Hoof [51].
これを自動的に行うための教師なし学習のアプローチは、Nicholls and Bright [38]とTrilling and van Hoof [51]にある。
Once the stories are identified, the Fragmentation score can be defined as the aggregate average distance between all sets of recommendations between all users.
ストーリーが特定されると、Fragmentationスコアは、すべてのユーザー間の推奨セット間の平均距離の総和として定義することができる。
Dillahunt et al.[11], which aimed to detect filter bubbles in search engine results, defines this distance with the Kendall Tau Rank Distance (KDT), which measures the number of pairwise disagreements between two lists of ranked items.
検索エンジンの結果におけるフィルターバブルの検出を目的としたDillahuntら[11]は、この距離を、ランク付けされたアイテムの2つのリスト間の対の不一致の数を測定するKendall Tau Rank Distance（KDT）で定義しています。
However, Kendall Tau is not suitable when the two lists can be (largely) disjointed.
しかし、2つのリストが（大きく）ばらばらになる可能性がある場合、Kendall Tauは適さない。
It also penalizes differences at the top of the list equally to those more at the bottom.
また、上位の差は下位の差に等しくペナルティーを与えることになります。
Instead we base our approach on the Rank Biased Overlap used in Webber et al.[54]:
その代わりに、Webberら[54]で使用されているRank Biased Overlapをベースとしたアプローチを採用しています：

$$


$$

where 𝑄1 and 𝑄2 denote two (potentially) infinite ordered lists, or two recommendations issued to users 1 and 2, and 𝑠 a parameter that generates a set of weights with a geometric progression starting at 1 and moving towards 0 that ensures the tail of the recommendation is counted less severely compared to its head.
ここで、ᵄ1と𝑄2は、2つの（潜在的に）無限順序リスト、またはユーザー1と2に発行された2つの勧告を示し、↪Ll_1D460は、勧告の尾部がその頭部と比較してより厳しくカウントされるように、1から始まり0に向かって幾何級数で重みセットを生成するパラメーターです。
Because of this there is a natural cut-off point where the score stabilizes.
そのため、スコアが安定する自然なカットオフポイントが存在するのです。
We iterate over the ranks 𝑑 in the recommendation set, and at each rank we calculate the average overlap 𝐴𝑑 .
推薦セットのランクᑑを繰り返し、各ランクで平均重複度ᑑを計算します。
Because Rank-Biased Overlap yields a score between 0 and 1, with 0 indicating two completely disjoint lists and 1 a perfect overlap, and the score that is expressed is semantically opposite of what we aim to express with the Fragmentation metric, we obtain the Fragmentation score by calculating 1 minus the Rank-Biased Overlap.
Rank-Biased Overlapは0と1の間のスコアで、0は2つのリストが完全に不連続、1は完全に重なることを示し、表現されるスコアはFragmentation指標で表現しようとするものと意味的に逆なので、1マイナスRank-Biased Overlapを計算してFragmentationスコアを求めることにします。
Lastly, the aggregate Fragmentation score is calculated by averaging the Fragmentation score between each user and every other user.
最後に、各ユーザーのFragmentationスコアを他のユーザーと平均して、Aggregate Fragmentation scoreを算出します。

### Limitations. 制限があります。

Since this approach is computationally expensive (every user is compared to every other user, which is 𝑂(𝑛 2 ) complexity), some additional work is needed on its scalability in practice, for example through sampling methods.
このアプローチは計算量が多いため（すべてのユーザーを他のすべてのユーザーと比較するため、ᵄ(𝑛 2 ) の複雑さになる）、サンプリング方法など、実際のスケーラビリティについて追加の作業が必要である。

## Activation アクティベーション

The Activation metric expresses whether the issued recommendations are aimed at inspiring the users to take action.
Activationは、発行されたレコメンデーションが、ユーザーの行動を喚起するものであるかどうかを表す指標です。
A score close to 1 indicates a high amount of activating content, whereas a score close to 0 indicates more neutral content.
スコアが1に近いほど活性化するコンテンツが多く、0に近いほど中立的なコンテンツが多いことを表しています。

### Explanation. 説明があります。

The way in which an article is written may affect the reader in some way.
記事の書き方は、読み手に何らかの影響を与える可能性があります。
An impartial article may foster understanding for different perspectives, whereas an emotional article may activate them to undertake action.
公平な記事であれば、異なる視点への理解を深めることができ、感情的な記事であれば、行動を起こすきっかけとなる。
A lot of work has been done on the effect of emotions and affect on the undertaking of collective group action.
感情や影響が集団行動の引き受けに与える影響については、これまでにも多くの研究がなされてきた。
This holds especially for anger, in combination with a sense of group efficacy [52].
これは、特に怒りについて、集団の有効性の感覚との組み合わせで当てはまる[52]。
But positive emotions play a role too; for example, "joy" elicits the urge to get involved, and "hope" to dream big [17].
しかし、ポジティブな感情も重要な役割を担っています。例えば、「喜び」は巻き込まれたいという衝動を引き出し、「希望」は大きな夢を抱かせるのです[17]。
The link between emotions, affect and activation is described well by Papacharissi [40]: "...for it is affect that provides the intensity with which we experience emotions like pain, joy, and love, and more important, the urgency to act upon those feelings".
感情、情動、活性化の間の関連性は、Papacharissi [40]によってよく説明されている： 「痛み、喜び、愛といった感情を経験する強さ、そしてより重要なのは、その感情に基づいて行動する緊急性を提供するのは情動である」。
The Activation metric aims to capture this by measuring the strength of emotions expressed in an article.
Activation指標は、記事中に表現された感情の強さを測定することで、これを把握することを目的としています。

### In the context of democratic recommenders. 民主的な推薦者の文脈で。

The Activation metric is relevant in three of the four different models.
Activationの指標は、4種類のモデルのうち3種類で関連しています。
The Deliberative model aims for a common consensus and debate, and therefore would give a certain measure of prominence to impartial articles with low Activation scores.
Deliberativeモデルは、共通のコンセンサスと議論を目指すため、Activationスコアが低い公平な記事を一定程度目立たせることになる。
The Participatory model fosters the common good and understanding, and aims to facilitate users in fulfilling their roles as citizens, undertaking action when necessary.
参加型モデルは、共通の利益と理解を促進し、ユーザーが市民としての役割を果たし、必要に応じて行動できるようにすることを目的としています。
This leads to a slightly wider value range; some activating content is desirable, but nothing too extreme.
そのため、数値の幅がやや広くなっています。活性化する成分があることが望ましいのですが、極端なものはありません。
The Critical model however leaves more room for emotional and provocative content to challenge the status quo.
しかし、クリティカルモデルでは、現状を打破するためのエモーショナルで挑発的なコンテンツがより多く存在することになります。
Here high values of Activation should be expected.
ここでは、Activationの高い値が期待される。

### Operationalization. オペレーション化。

The Circumplex Model of Affect [43] describes a dimensional model where all types of emotions are expressed using the terms valence and arousal.
感情のサーカムプレックスモデル[43]は、すべてのタイプの感情が価数と覚醒という用語を使って表現される次元モデルを説明している。
Valence indicates whether the emotion is positive or negative, while arousal refers to the strength of the emotion and to what extent it expresses action.
Valenceは感情がポジティブかネガティブかを示し、Arousalは感情の強さ、行動をどの程度表すかを示す。
Following this, for example, ’excitement’ has a positive valence and arousal, whereas ’bored’ is negative for both.
これに従うと、例えば「興奮」は正の価数と覚醒度を持つのに対し、「退屈」は両者とも負の価数である。
Based on the theory described above a number of "sentiment analysis" tools have been developed, which typically have the goal of identifying whether people have a positive or negative sentiment regarding a certain product or issue.
このような理論に基づき、多くの「感情分析」ツールが開発され、ある製品や問題に対して人々がポジティブな感情を持っているかネガティブな感情を持っているかを特定することを目的としています。
For example, Hutto and Gilbert [21] provides a lexicon-based tool that for each input piece of text outputs a compound score ranging from -1 (very negative) to 1 (very positive).
例えば、Hutto and Gilbert [21]は、各入力テキストに対して、-1（非常にネガティブ）から1（非常にポジティブ）までの複合スコアを出力する、辞書ベースのツールを提供しています。
The absolute values of these scores can be used as an approximation of the arousal and therefore be used to determine the Activation score of a single article.
これらのスコアの絶対値は、覚醒度の近似値として使用できるため、1つの記事のActivationスコアを決定するために使用することができます。
Then, the total Activation score of the recommender system should be calculated two-fold.
そして、レコメンダーシステムのActivationスコアの合計は、2回に分けて計算する必要があります。
The average Activation score of the items recommended to each user provides a baseline score for whether the articles overall tend to be activating or neutral.
各ユーザーに推奨されたアイテムの平均活性化スコアは、記事全体が活性化する傾向にあるのか、中立的な傾向にあるのかの基準スコアとなります。
Next, the issued recommendations are compared to the available pool of data as follows:
次に、発行された提言と利用可能なデータプールを以下のように比較します：

$$
Activation
$$

Here 𝑝 denotes the set of all available articles in the pool, and 𝑞 those in the recommendation.
ここで、ᵅはプールにあるすべての利用可能な記事の集合を示し、↪Ll_1D45E は推薦にあるものを示す。
For both sets we take the mean of the absolute polarity value of each article, which we use as an approximation for Activation.
両セットとも、各記事の極性の絶対値の平均をとり、これをActivationの近似値として使用する。
We subtract the mean from the available pool of articles from the mean of the recommendation set, which maps to a range of [−1, 1].
利用可能な記事のプールから、推薦セットの平均値を引くと、[-1, 1]の範囲にマッピングされるのです。
A value lower than zero indicates that the recommender system shows less activating content than was available in the pool of data, and therefore favors more neutral articles.
ゼロより低い値は、レコメンダーシステムが、データプールで利用可能だったよりも活性化するコンテンツが少なく、より中立的な記事を優先して表示することを示します。
Values higher than zero show the opposite; the recommendation sets contained proportionally more activating content than was available in the pool.
ゼロより高い値は、その逆で、レコメンデーションセットには、プールで利用可能なものより比例して多くの活性化コンテンツが含まれていることを示しています。

### Limitations. 制限があります。

Of principle importance is the impact that the article’s text has on the reader.
原則的に重要なのは、記事の文章が読者に与える影響である。
However, as we have no direct way of measuring this, we hold to the assumption that a strongly emotional article will also cause similarly strong emotions in a reader, which again translates into higher willingness to act.
しかし、これを直接測定する方法がないため、私たちは、強く感情を揺さぶられる記事は、読者にも同様の強い感情を与え、それがまた行動意欲を高めるという仮定を立てています。
It must also be noted that people may respond differently to different emotions (for example, anger may incite either approach (action) or avoidance (inaction) tendencies) [44].
また、人は感情によって反応が異なる（例えば、怒りは接近（行動）傾向と回避（不作為）傾向のどちらかを誘発する）ことに留意しなければならない[44]。
We therefore see this approach as an approximation of the concept of activation, affect and emotion in articles, until such a time when more research in the topic allows us to be more nuanced in our perceptions.
したがって、このアプローチは、論文における活性化、影響、感情の概念の近似値であり、このテーマに関するより多くの研究によって、よりニュアンスのある認識ができるようになるまでの間、このようなアプローチになると考えています。

## Representation 表現

The Representation metric expresses whether the issued recommendations provide a balance of different opinions and perspectives, where one is not unduly more or less represented than others.
代表性」指標は、発行された提言が、異なる意見や視点のバランスを保ち、ある意見が他の意見より不当に多く、あるいは少なくなっていないかどうかを表すものです。
A score close to zero indicates a balance, where the model of democracy that is chosen determines what this balance entails, whereas a higher score indicates larger discrepancies.
ゼロに近いほどバランスが取れていることを示し、そのバランスがどのようなものであるかは、選択された民主主義のモデルによって決定されます。一方、スコアが高いほど矛盾が大きいことを示します。

### Explanation. 説明があります。

Representation is one of the more intuitive interpretations of diversity.
Representationは、より直感的な多様性の解釈の一つです。
Depending on which model of democracy is chosen, news recommendations should contain a plurality of different opinions.
民主主義のどのモデルを選択するかによって、ニュースレコメンデーションには複数の異なる意見が含まれるはずです。
Here we care more about what is being said than who says it, which is the goal of the final metric, Alternative Voices.
ここでは、誰が言っているのかよりも、何が言われているのかが重要であり、それが最後の指標であるAlternative Voicesの目標です。
In order to define what it means to provide a balance of opinions, one needs to refer back to the different models and their goals.
意見のバランスを取るとはどういうことかを定義するためには、さまざまなモデルとその目的を参照する必要があります。

### In the context of democratic recommenders. 民主的な推薦者の文脈で。

The Participatory model aims to be reflective of "the real political world".
参加型モデルは、「現実の政治世界」を反映することを目的としています。
Power relations that are therefore present in society should also be present in the news recommendations, with a larger share in the Representation for the more prevalent opinions.
したがって、社会に存在する力関係は、ニュースレコメンデーションにも存在し、より優勢な意見ほどRepresentationでのシェアが大きくなるはずです。
On the other hand, the Deliberative model aims to provide an equal overview of all opinions without one being more prevalent than the other.
一方、Deliberativeモデルは、一つの意見が他の意見よりも優勢になることなく、すべての意見を平等に俯瞰することを目的としています。
The Critical model has a large focus on shifting power balances, and it does so by giving a platform to underrepresented opinions, thereby promoting an inverse point of view.
クリティカルモデルは、パワーバランスを変えることに大きな重点を置いており、代表的でない意見にプラットフォームを与えることで、逆の視点を促進することでそれを実現しています。
In doing this, the Critical model also strongly considers the characteristics of the opinion holder, specifically whether they are part of a minority group or not, though this is the goal of the last metric, Alternative Voices.
この際、Criticalモデルでは、意見保有者の特性、具体的にはマイノリティグループに属しているかどうかも強く考慮されていますが、これは最後の指標であるAlternative Voicesが目指すところです。

### Operationalization. オペレーション化。

Representation, and Alternative Voices as well, rely strongly on the correct and complete identification of the opinions and opinion holders mentioned in the news.
Representation、そしてAlternative Voicesは、ニュースで言及された意見と意見保有者を正確かつ完全に特定することに強く依存しています。
Though there is research available on the usage of Natural Language patterns to extract opinion data from an article’s text [41], additional work is necessary on its applicability in this context.
記事のテキストから意見データを抽出するための自然言語パターンの使用に関する研究はあるが[41]、この文脈での適用可能性についてはさらなる研究が必要である。
For example, it is of significant importance that not one type of opinion or opinion holder is systematically missed.
例えば、一種類の意見や意見保有者が組織的に見逃されないことが重要である。
Once the quality of the extraction is relatively certain, additional work is also necessary on the placement of opinions relative to each other; for example, which opinions are in favor, against or neutral on a statement, and how are these represented in the recommendations.
例えば、ある意見に対して賛成、反対、中立のどの意見があり、それらをどのように推薦文に反映させるかなど、抽出の質が比較的確かなものであれば、意見の相対的な配置についても追加作業が必要である。
This task is extremely complex, even for humans.
この作業は、人間でも非常に複雑です。
In the meantime approximations can be used, for example by considering (spokespersons of) political parties and their position on the political spectrum.
その際、例えば政党のスポークスパーソンや政治スペクトル上の位置づけを考慮することで、近似値を用いることができる。
This can be done through manual annotations, with hardcoded lists of politicians and their parties, or automatically by for example querying Wikidata for information on persons identified through Named Entity Recognition.
これは、政治家とその政党のリストをハードコードした手作業によるアノテーションや、名前付き固有表現認識によって特定された人物の情報をWikidataに問い合わせるなどして自動的に行うことができる。
To calculate the Representation score, we once again use the Kullback-Leibler Divergence, but this time on the different opinion categories in the recommendations versus the available pool of data:
Representationスコアの算出には、再びKullback-Leibler Divergenceを使用しますが、今回はレコメンデーションと利用可能なデータプールの異なる意見カテゴリについて使用します：

$$
Representation
$$

This calculation is similar to the one in Section 4.1.However, 𝑜 indicates the different opinions in the data; 𝑝(𝑜) represents the proportion of the times this opinion was present in the overall pool of data, whereas 𝑞˜(𝑜 |𝑢) represents the proportion of times user 𝑢 has seen this opinion in their recommendations.
𝑢) represents the proportion of times user 𝑢 has seen this opinion in their recommendations.
A score of 0 means a perfect match between the two, which means that the opinions shown in the recommendations are perfectly representative of those in society.
0点というのは、両者が完全に一致していることを意味し、推薦文に示された意見が社会を完全に代表していることを意味します。
When following the Participatory model reflective point of view we want this value to be as close to zero as possible, as being representative of society is its main goal.
参加型モデルの反射的な視点に従うと、社会を代表することが主な目的であるため、この値はできるだけゼロに近づけたい。
However, when following one of the other models, we have to make some alterations on the distributions expressed by 𝑝.
しかし、他のモデルに従う場合、ᵅで表される分布にいくつかの変更を加えなければならない。
The Critical model’s inverse point of view aims for the recommendations to diverge as much from the power relations in society as possible.
クリティカルモデルの逆視点は、提言が社会の力関係からできるだけ乖離することを目指すものである。
However, since very small differences in distributions can result in a very large KL divergence, simply maximizing the KL divergence is not sufficient.
しかし、非常に小さな分布の違いが非常に大きなKLダイバージェンスをもたらすことがあるため、単にKLダイバージェンスを最大化するだけでは十分ではありません。
Instead, we inverse the distribution of opinions present in 𝑝.
その代わりに、ᑝに存在する意見の分布を逆算する。
Similarly, when choosing the Deliberative model, we want all opinions in the recommendations to be equally represented, and therefore we choose 𝑝 as a uniform distribution of opinions.
同様に、Deliberativeモデルを選択する場合、推薦文に含まれるすべての意見を均等に反映させたいので、意見の均一分布としてŅを選択します。
This way, for each of the different approaches holds that the closer the divergence is to zero, the better the recommendations reflect the desired representation of different opinions.
このように、異なるアプローチのそれぞれについて、ダイバージェンスがゼロに近ければ近いほど、レコメンデーションは異なる意見の望ましい表現を反映していることになります。
For each of the reflective, inverse and equal approaches, the aggregated Representation score is obtained by averaging the Representation score over all recommendations issued to all users.
Reflective、Inverse、Equalの各アプローチにおいて、全ユーザーに発行されたすべての推薦文のRepresentationスコアを平均することで、集約されたRepresentationスコアが得られる。

### Limitations. 制限があります。

Kullback-Leibler divergence treats each category as being independent, and does not account for opinions and standpoints that may be more or less similar to other categories.
カルバック・ライブラーダイバージェンスは、各カテゴリーを独立したものとして扱い、他のカテゴリーと多かれ少なかれ類似している意見や立場は考慮しない。

## Alternative Voices オルタナティブ・ヴォイス

The Alternative Voices metric measures the relative presence of people from a minority or marginalised group.
オルタナティブ・ヴォイスの指標は、少数派または周縁化されたグループの人々の相対的な存在感を測定するものです。
A higher score indicates a proportionally larger presence.
スコアが高いほど、存在感が比例して大きくなることを示します。

### Explanation. 説明があります。

Where Representation is largely focused on the explicit content of a perspective (the what), Alternative Voices is more concerned with the person holding it (the who), and specifically whether this person or organisation is one of a minority or an otherwise marginalised group that is more likely to be underrepresented in the mainstream media.
Representationが視点の明確な内容（What）に主眼を置いているのに対し、Alternative Voicesは、その視点を持つ人物（Who）に関心があり、特にその人物や組織が、主流メディアで十分に表現されない可能性の高い少数派や疎外されたグループの一人であるかどうかを重視しています。
What exactly entails a minority is rather vaguely defined.
具体的に何をもってマイノリティとするかは、かなり曖昧な定義になっています。
Article 1 from the 1992 United Nations Minorities Declaration refers to minorities “a non-dominant group of individuals who share certain national, ethnic, religious or linguistic characteristics which are different from those of the majority population", though there is no internationally agreed-upon definition.
1992年の国連マイノリティ宣言の第1条では、マイノリティを「多数派とは異なる特定の国家、民族、宗教、言語的特徴を共有する個人の非支配的集団」と規定しているが、国際的に合意された定義はない。
In practice, this interpretation is often extended with gender identity, disability and sexual orientation.
実際には、この解釈は、性自認、障害、性的指向と拡張されることが多い。
A major challenge of the Alternative Voices metric lies in the actual identification of a minority voice.
オルタナティブボイスの指標の大きな課題は、マイノリティボイスを実際に特定することにある。
Though there are a number of studies that aim to detect certain characteristics of minorities from textual data, such as predicting a person’s ethnicity and gender based on their first and last name [46], there are no approaches that 1) model all minority characteristics or 2) perform well consistently.
テキストデータからマイノリティの特定の特性を検出することを目的とした研究は数多くありますが、例えば、姓と名からその人の民族性と性別を予測する[46]など、1）すべてのマイノリティ特性をモデル化する、2）一貫して良い結果を出す、というアプローチは存在しないのです。
This process needs significant additional and most importantly multidisciplinary research, with a large focus on ensuring that doing this type of analysis does not lead to unintended stereotyping, exclusion or misrepresentation.
このプロセスでは、この種の分析を行うことが意図しないステレオタイプ化、排除、誤った表現につながらないようにすることに大きな焦点を当てた、大幅な追加研究、最も重要な学際的研究が必要です。
For example, Keyes [27] shows that current studies typically treat gender classification as a purely binary problem, thereby systematically leaving out and wrongly classifying transgender people.
例えば、Keyes [27]は、現在の研究が一般的に性別分類を純粋な二項対立の問題として扱っており、それによってトランスジェンダーの人々を体系的に除外し、間違って分類していることを示しています。
Similarly, Hanna et al.[18] argue that race and ethnicity are strongly social constructs that should not be treated as objective differences between groups.
同様に、Hannaら[18]は、人種や民族は強く社会的な構成要素であり、集団間の客観的な差異として扱うべきものではないと主張している。
This topic, typically referred to as (algorithmic) Fairness, is an active research field that aims to counter bias and discrimination in data-driven computer systems.
このテーマは、一般的に「（アルゴリズムによる）公平性」と呼ばれ、データ駆動型のコンピュータシステムにおける偏見や差別に対抗することを目的とした活発な研究分野である。
One thing is for certain: any recommender system that actively promotes one type of voice over another should make very explicit on what criteria and following which methods it does this.
ある音声を他の音声よりも積極的に推奨するレコメンダーシステムは、どのような基準で、どのような方法でそれを行うかを明確にする必要があります。
Following this both the identification and the way its algorithms use this information must be fully transparent and auditable.
その上で、識別とそのアルゴリズムが情報を使用する方法について、完全に透明で監査可能でなければなりません。
However, for the remainder of this section we will assume that we do have a proper way of identifying people from a minority group, either through manual annotation or automatic extraction.
しかし、このセクションの残りの部分では、手動アノテーションまたは自動抽出によって、少数派の人々を識別する適切な方法があることを仮定することにします。

### In the context of democratic recommenders. 民主的な推薦者の文脈で。

The Alternative Voices metric is naturally most significant in the Critical model, which aims to provide a platform to voices that would otherwise go unheard, and therefore has a large focus on the opinions and perspectives from minority groups.
オルタナティブ・ヴォイス」の指標は、当然ながら、「クリティカル」モデルにおいて最も大きな意味を持ちます。「クリティカル」モデルは、通常では聞くことのできない声にプラットフォームを提供することを目的としているため、少数派の意見・見解に大きな焦点が当てられています。
To a lesser extent, the same holds for the Participatory and Deliberative models, where the first aims to foster tolerance and empathy, and the second that they should be equally represented.
程度の差こそあれ、「参加型」と「熟議型」についても同様で、前者は寛容と共感を育むことを目的とし、後者は平等に代表されるべきであるとするものです。

### Operationalization. オペレーション化。

The discussion around Fairness in machine learning systems has lead, among others, to a number of definitions of the concept.
機械学習システムにおける「公平性」をめぐる議論では、さまざまな定義がなされている。
For the operationalization of Alternative Voices we adapt Equation 10 of Burke et al.[5] for our purposes:
Alternative Voicesの運用については、Burkeら[5]の式10を本目的のために適用した：

$$
AlternativeVoices
$$

Here 𝑞 + denotes the number of mentions of people belonging to a protected group in the recommendations, whereas 𝑝 + denotes the number of mentions of people belonging to a protected group in all the available articles.
ここで、ᑞはレコメンデーションにおける保護団体に属する人々の言及数を示し、一方、ᑝ +は利用可能なすべての記事における保護団体に属する人々の言及数を示している。
𝑞 − and 𝑝 − denote similar mentions, but for people belonging to the unprotected group.
ᵅ - とᵅ - は、同様の言及を示しますが、保護されていないグループに属する人々についてです。
Though the example given in Burke et al.[5] describes the equation being used to identify whether loans from protected and unprotected regions appear equally often, it is also directly applicable to our notion of Alternative Voices; however, rather than counting regions being recommended, we count the number of times that people from minority (protected) versus majority (unprotected) groups are being mentioned in the news.
Burkeら[5]の例では、保護された地域からの融資と保護されていない地域からの融資が同じ頻度で登場するかどうかを識別するために使用する方程式を説明しているが、これは我々のAlternative Voicesの概念にもそのまま適用できる。ただし、推奨される地域を数えるのではなく、少数派（保護された）グループと多数派（保護されていない）グループの人々がニュース内で言及する回数を数えることになる。
This function maps to 1 when there is a complete balance between people from the protected and the unprotected groups.
この機能は、保護されたグループと保護されていないグループの人々の間のバランスが完全にとれている場合に1にマッピングされます。
When the value is larger than 1 more people from unprotected groups appear in the recommendation set, whereas lower than 1 means they appear less.
値が1より大きいと、無防備なグループの人々が推薦セットに多く登場し、1より小さいと登場しないことを意味します。
Again, the aggregate score consists of the average Alternative Voices score over all recommendations issued to all users.
ここでも、集計スコアは、全ユーザーに発行されたすべての推薦文の平均的なAlternative Voicesスコアで構成されています。

### Limitations. 制限があります。

A major caveat of this approach is that it assumes that the mere mentioning of minority people is enough to serve the goals of the Alternative Voices metric.
このアプローチの大きな注意点は、マイノリティの人々について言及するだけで、オルタナティヴ・ヴォイスの指標の目的を果たすのに十分であると仮定していることです。
This disregards the fact that these people may be mentioned but from another person’s perspective, or in a negative light.
これは、これらの人々が言及されていても、別の人の視点から、あるいは否定的な意味で言及されている可能性があることを軽視しています。
Further research should focus on not only identifying a person from a minority group, but also whether they are mentioned as an active or passive agent.
マイノリティグループの人物を特定するだけでなく、その人物が能動的な存在として言及されているのか、受動的な存在として言及されているのかについても、さらなる研究が必要です。

# General limitations 一般的な制限

Though all of the metrics described in Section 4 already mention the limitations of that metric specifically, this section describes a number of the limitations of this method as a whole.
セクション4で説明されたすべてのメトリックは、すでに具体的にそのメトリックの限界に言及していますが、このセクションでは、全体としてこのメソッドのいくつかの限界について説明します。

## Ordering ご注文はこちら

Of the currently specified metrics, only Fragmentation takes the ordering of the items in the recommendation into account.
現在規定されているメトリクスのうち、Fragmentationのみ推薦文の項目の順序を考慮しています。
However, the top result in a recommendation is of significantly more importance than the result in place 10.
しかし、レコメンデーションの上位の結果は、10位の結果よりも重要度が格段に高いのです。
In future work, the other metrics should be extended in such a way that they reflect this.
今後、他の指標もこれを反映するように拡張していく必要があります。

## Formalism Trap フォーマリズムの罠

Many of the concepts described here are susceptible to the Formalism Trap described in [45], which is defined as the "[f]ailure to account for the full meaning of social concepts [...], which can be procedural, contextual and contestable, and cannot be resolved through mathematical formalisms".
ここで説明した概念の多くは、[45]で説明した「形式主義の罠」の影響を受けやすく、「手続き的、文脈的、論争的であり、数学的形式主義では解決できない社会概念の完全な意味を説明することができない」と定義されている。
Though our approach aims to model concepts founded in social science and democratic theories, they are merely approximations and to a large extent simplifications of very complex and nuanced concepts that have been contested and debated in the social sciences and humanities for decades.
私たちのアプローチは、社会科学や民主主義の理論に基づく概念をモデル化することを目的としていますが、それらは、何十年にもわたって社会科学や人文科学で議論されてきた非常に複雑で微妙な概念の近似値に過ぎず、かなりの程度単純化されています。
To claim our approach comes close to covering these subtleties would be presumptuous - however, we do believe it is necessary to provide a starting point in the modeling of concepts that have so far largely been neglected or oversimplified in the evaluation of news recommendations.
しかし、これまでニュース推薦の評価で軽視されたり、単純化されたりしてきた概念のモデル化の出発点を提供することは必要だと考えています。
The pitfalls of this trap should be mitigated by always providing full transparency on how these concepts are implemented, on what kind of data they are based, and most importantly on how they should (and should not) be interpreted.
このような落とし穴は、これらの概念がどのように実装されているか、どのようなデータに基づいているか、そして最も重要なことは、これらの概念をどのように解釈すべきか（そして解釈すべきでないか）についての完全な透明性を常に提供することによって軽減されるべきです。

## Bias in the dataset データセットの偏り

The metrics presented in Section 4 typically rely on measuring a difference between the set of recommended items and the full set of articles that were available, the reading history of the user in question or among users.
セクション4で紹介したメトリクスは、通常、推奨アイテムのセットと利用可能だった記事のフルセット、当該ユーザーの読書履歴、またはユーザー間の差分を測定することに依存している。
What it does not do is account for inherent bias in the overall dataset, though the possibility of exposure diversity depends on the availability of content in the pool.
データセット全体に内在する偏りを考慮することはできませんが、露出の多様性の可能性は、プール内のコンテンツの利用可能性に依存します。
If the quality and diversity of the pool is low, recommenders have insufficient options to provide good recommendations.
プールの質と多様性が低ければ、推薦者は良い推薦をするための十分な選択肢を持つことができません。
That means exposure diversity ultimately is dependent on external diversity.
つまり、エクスポージャーの多様性は、最終的には外部の多様性に依存するということです。
Detecting such a bias in the dataset rather than in the produced recommendations and undertaking steps to remedy this needs additional work.
このようなバイアスを、作成されたレコメンデーションではなく、データセットから検出し、これを改善するための措置を講じることは、さらなる作業が必要です。

## Nudging for more diverse news consumption より多様なニュース消費のためのナッジング

The metrics discussed here do not reflect on the process of getting users to actually consume more diverse content.
ここで取り上げた指標は、ユーザーがより多様なコンテンツを実際に消費するようになるまでの過程を反映したものではありません。
Different users may have different ’tolerance’ for diversity, depending on the topic and even on things such as the time of day.
ユーザーによって、話題や時間帯によって、多様性に対する「許容度」が異なる場合があります。
Whether or not news recommenders can successfully motivate users to consume more diverse can also depend on the (user-friendly) design of the recommender and the way the recommendations are presented [33].
ニュースレコメンダーがユーザーの多様な消費をうまく動機づけることができるかどうかは，レコメンダーの（ユーザーフレンドリーな）デザインやレコメンデーションの提示方法にも依存することがある[33]。
Designing for more diverse news consumption also gives rise to a different discussion: is it ethical to nudge news consumption, even if it is for a commendable goal such as "more diversity" or "countering filter bubbles", and where do we draw the line between offering more diverse recommendations and manipulating the reader? The complexity and breadth of this topic are out of scope for this paper, but should be considered in future work.
より多様なニュース消費をデザインすることは、また別の議論を生む。たとえそれが「より多様な」あるいは「フィルターバブルに対抗する」といった称賛に値する目標のためであっても、ニュース消費をナッジすることは倫理的なのか、より多様な推薦をすることと読者を操作することの線引きはどこにあるのか。このトピックの複雑さと広さは本稿の範囲外であるが、今後の研究において考慮されるべきであろう。

## Broader institutional context 広い制度的背景

Efforts to develop more diverse and inclusive news recommendation metrics and models do not, on their own, mean that users will receive more diverse recommendations; that requires a combination of editorial judgement, the availability of internal workflows that translate this judgement into technology design, the room to implement alternative diversity metrics in third party software (which again depends on the degree of professional autonomy and negotiating power between the media and software providers), and users who engage with the algorithm when presented with a particular recommendation.
より多様で包括的なニュース推薦の指標やモデルを開発する努力は、それだけでユーザーがより多様な推薦を受けることを意味しません。そのためには、編集者の判断、その判断を技術設計に反映させる内部ワークフローの利用、第三者のソフトウェアに別の多様性指標を実装する余地（これもメディアとソフトウェアプロバイダー間の専門家の自律性と交渉力の程度に依存します）、特定の推薦を提示されたときにアルゴリズムと関わるユーザーとの組み合わせが必要となります。
The design approach must thus additionally consider how values are re-negotiated between stakeholders (e.g.editors, data scientists, regulators, external technology providers), how values are embedded in organizational practices of a news room, and how professional users, citizens, and society create control mechanisms and governance frameworks to realize public values, such as diversity.
そのため、編集者、データサイエンティスト、規制当局、外部技術提供者などのステークホルダー間でどのように価値が再交渉されるのか、ニュースルームの組織的実践にどのように価値が埋め込まれるのか、プロフェッショナルユーザー、市民、社会が多様性などの公共価値を実現するための制御メカニズムやガバナンスの枠組みをどのように作るのか、などをデザインアプローチとして追加的に考慮する必要がある。

## Inherent limits to value by design approaches バリュー・バイ・デザイン・アプローチに内在する限界

Finally, it is important to be mindful of another lesson from the general diversity by design debate, namely that there are also certain limits to value sensitive design, in our case the extent to which diversity as a normative concept can be operationalized in concrete recommender design.
つまり、価値観に配慮したデザインには一定の限界があり、この場合、規範的な概念としての多様性を具体的なレコメンダーデザインでどの程度運用できるかが重要である。
This can have to do with the sheer difficulty of translating certain aspects of diversity, but also with the trade-offs between values that optimizing for exposure diversity can involve.
これは、多様性のある側面を翻訳することが非常に困難であることに加えて、エクスポージャーの多様性を最適化することが価値間のトレードオフを伴うことが関係しています。
Examples of this are commercial constraints and the need to optimize for profit rather than for diversity, but also the limited effectiveness of recommenders in actually steering user choices.
その例として、商業的な制約や、多様性よりも利益のために最適化する必要性が挙げられますが、実際にユーザーの選択を誘導するレコメンダーの効果も限定的です。

# Implementation インプリメンテーション

We are working on the implementation of the concepts and metrics discussed here in an open source tool1 .
ここで取り上げた概念や指標を、オープンソースのツールに実装する作業を行っています1。
The goal of this tool is to implement the metrics described in this paper as evaluation metrics for recommender design, and in doing so enable media companies to evaluate the performance of their own recommendations against those of several baseline recommendations.
本ツールの目的は、本稿で紹介した評価指標をレコメンダーデザインの評価指標として実装することで、メディア企業が自社のレコメンデーションのパフォーマンスを複数のベースラインのレコメンデーションと比較して評価できるようにすることです。

## Approach アプローチ

By making comparisons between the different recommender approaches, media companies should be able to draw conclusions about which recommender strategy fits their editorial mission best.
メディア企業は、さまざまなレコメンダーアプローチを比較検討することで、どのレコメンダー戦略が自社の編集ミッションに最も適しているかという結論を導き出すことができるはずです。
By also comparing the performance of these algorithms to very simple recommendation approaches, such as a random recommender, the media company can also draw conclusions about where the recommender simply reflects the available data, and where it significantly influences the type of data that is shown.
また、これらのアルゴリズムのパフォーマンスを、ランダムレコメンダーなどの非常にシンプルなレコメンデーションアプローチと比較することで、メディア企業は、レコメンダーが利用可能なデータを単に反映する場合と、表示されるデータの種類に大きく影響する場合の結論を導くことができます。
By making these visualizations as intuitive as possible, they should facilitate the discussion between data science teams, editors and upper management around this topic.
これらのビジュアライゼーションをできるだけ直感的に理解できるようにすることで、このトピックに関するデータサイエンスチーム、エディター、上層部の議論を促進することができるはずです。
To make this approach reusable and broadly applicable, it should be implemented and tested on both a benchmark set such as [55] and in a real-life setting.
このアプローチを再利用可能で広く適用できるようにするには、[55]のようなベンチマークセットと現実の設定の両方で実装しテストする必要があります。
We are in contact with multiple media companies, to inform them about the different models of democracy, facilitate the discussion around this subject, and stimulate and test the implementation of our tool.
私たちは、複数のメディア企業と連絡を取り、民主主義のさまざまなモデルについて伝え、このテーマに関する議論を促進し、私たちのツールの実装を刺激し、テストしています。
Simultaneously this topic is continuously being discussed with experts from many different disciplines, as happened for example during a Dagstuhl Workshop[3].
同時にこのテーマは、例えばDagstuhlワークショップ[3]で起こったように、多くの異なる分野の専門家と継続的に議論されています。

## Guidelines for adoption 採用に関するガイドライン

The ultimate goal of this paper is to propose notions that could be incorporated in recommender system design.
本稿の最終目標は、レコメンダーシステムの設計に組み込むことができる概念を提案することである。
In our vision, media companies could approach this in the following steps:
私たちのビジョンでは、メディア企業は次のようなステップでアプローチできると考えています：

- (1) Determine which model of democracy to follow Following the different models described in Section 3, the media company in question should decide which model of democracy the recommender system should reflect. This is something that should be decided in active discussion with the editorial team, and directly in line with the media company’s mission. (1) どの民主主義のモデルに従うか決定する 3節で説明したさまざまなモデルに従って、当該メディア企業は、レコメンダーシステムがどの民主主義のモデルを反映すべきかを決定すべきである。 これは、編集部と積極的に議論して決めるべきことで、メディア企業のミッションに直結することです。

- (2) Identify the corresponding metrics Use Table 1 to determine which metrics are relevant, and what the expected value range for each metric is. For example, when choosing to follow the Deliberative model, the recommender system should optimize for a low Fragmentation, low Activation and equal Representation. Similarly, for the Critical model, it should optimize for high Activation, inverse Representation and high Alternative Voices. (2) 対応するメトリクスの特定 表1を使って、どのメトリクスの関連性があるのか、各メトリクスの期待値範囲はどのくらいなのかを確認します。 例えば、Deliberativeモデルを選択した場合、レコメンダーシステムは、Fragmentationが低く、Activationが低く、Representationが等しくなるように最適化する必要があります。 同様に、Criticalモデルの場合は、高いActivation、逆Representation、高いAlternative Voicesに最適化する必要があります。

- (3) Implement into recommender design Here it is of key importance to determine the relative importance of each metric, and how to make a trade-off between recommender accuracy and normative diversity. For example, Mehrotra et al. [36] details a number of approaches to combining Relevance and Fairness in Spotify’s music recommendation algorithm, and this approach can also be applied in the trade-off between accuracy and the metrics relevant for the chosen model. (3) 推薦者設計への導入 ここでは、各メトリクスの相対的な重要性を判断し、推薦者の精度と規範的多様性のトレードオフをいかに行うかが重要である。 例えば、Mehrotraら[36]は、Spotifyの音楽推薦アルゴリズムにおけるRelevanceとFairnessを組み合わせるための多くのアプローチを詳述しており、このアプローチは、精度と選択したモデルに関連するメトリクスとの間のトレードオフにおいても適用することができる。

We do not consider these metrics to be the final "truth" in the identification of diversity in news recommendations.
これらの指標は、ニュースレコメンデーションにおける多様性の識別における最終的な「真実」であるとは考えていません。
The metrics and their operationalizations should serve as inspiration and a starting point for discussion, not as restrictions or set requirements for "good" recommender design.
メトリックスとその運用は、インスピレーションと議論の出発点として役立つべきものであり、「良い」レコメンダーデザインの制限や要件として設定するものではない。

# Discussion ディスカッション

In this paper we have translated normative notions of diversity into five metrics.
本稿では、多様性に関する規範的な概念を5つの指標に置き換えた。
Each of the metrics proposed here is relevant in the context of democratic news recommenders, and combined they form a picture that aims to be expressive of the nuances in the different models.
ここで提案する各メトリクスは、民主的なニュースレコメンダーの文脈に関連しており、それらを組み合わせることで、異なるモデルのニュアンスを表現することを目指した画像を形成する。
However there is still a lot of work to be done, both in terms of technical feasibility and in undertaking steps to make diversity of central importance for recommender system development.
しかし、技術的な実現可能性という点でも、推薦システム開発において多様性を重要視するためのステップという点でも、まだやるべきことはたくさんあります。

At the basis of our work is that we believe diversity is not a single absolute, but rather an aggregate value with many aspects and a mission in society.
私たちの活動の根底にあるのは、ダイバーシティは単一の絶対的なものではなく、さまざまな側面を持つ総体的な価値であり、社会におけるミッションであると考えることです。
In fact, we argue that what constitutes ’good’ diversity in a recommender system is largely dependent on its goal, which type of content it aims to promote, and which model of the normative framework of democracy it aims to follow.
実際、推薦システムにおいて何が「良い」多様性を構成するかは、その目的、どのようなコンテンツの促進を目指すか、民主主義の規範的枠組みのどのモデルに従うことを目指すかに大きく依存すると、我々は主張する。
As none of these models is inherently better or worse than the others, we believe that a media company should take a normative stance and evaluate their recommender systems accordingly.
どのモデルも本質的に他より優れているわけでもなく、劣っているわけでもないので、メディア企業は規範的なスタンスでレコメンダーシステムを評価するべきだと考えています。

Different fields and disciplines may have very different notions of the same concept, and navigating these differences is a process of constant negotiation and compromise, but also of expectation management.
同じコンセプトでも、分野や領域が異なれば、その考え方も大きく異なります。この違いを乗り越えるには、常に交渉と妥協の連続であり、期待値の管理も必要です。
Abstract concepts such as diversity may never be fully captured by the hard numbers that recommender system practitioners are used to.
多様性のような抽象的な概念は、レコメンダーシステムの実務者が慣れ親しんでいるハードな数字で完全に捉えることはできないかもしれません。
As recommendation algorithms take on an ever more central role in society, the necessity to bridge this gap and make such concepts more concrete also arises.
推薦アルゴリズムが社会の中心的な役割を担うようになった今、このギャップを埋め、その概念をより具体化する必要性が生じているのです。
Social sciences, humanities and computer science will need to meet in the middle between abstract and concrete, and work together to create ethical and interpretable technologies.
社会科学、人文科学、コンピュータサイエンスは、抽象と具体の中間で出会い、倫理的で解釈可能なテクノロジーを共に創造していく必要があるでしょう。
This work is not a final conclusion on how diversity can be measured in news recommendations, but rather a first step in forming the bridge between the normative notion of diversity and its practical implementation.
本研究は、ニュースレコメンデーションにおける多様性の測定方法に関する最終結論ではなく、多様性の規範的な概念とその実践的な実装との間の橋渡しを形成する最初のステップである。