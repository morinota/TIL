## link リンク

https://www.tandfonline.com/doi/full/10.1080/21670811.2019.1623700
https://www.tandfonline.com/doi/full/10.1080/21670811.2019.1623700

## title タイトル

On the Democratic Role of News Recommenders
ニュースレコメンダーの民主的役割について

## abstract 抄録

Are algorithmic news recommenders a threat to the democratic role of the media?
アルゴリズムによるニュース推薦ツールは、メディアの民主的役割を脅かすものなのか？
Or are they an opportunity, and, if so, how would news recommenders need to be designed to advance values and goals that we consider essential in a democratic society?
もしそうだとすれば、民主主義社会で不可欠と考えられる価値や目標を推進するために、ニュース推薦システムはどのように設計される必要があるのだろうか。
These are central questions in the ongoing academic and policy debate about the likely implications of data analytics and machine learning for the democratic role of the media and the shift from traditional mass-media modes of distribution towards more personalised news and platforms
これらは、メディアの民主的役割や、伝統的なマスメディアの配信形態からよりパーソナライズされたニュースやプラットフォームへのシフトに対するデータ分析や機械学習の影響について、現在進行中の学術的・政策的議論における中心的な疑問である。
Building on democratic theory and the growing body of literature about the digital turn in journalism, this article offers a conceptual framework for assessing the threats and opportunities around the democratic role of news recommenders, and develops a typology of different ‘democratic recommenders’.
民主主義理論や、ジャーナリズムにおけるデジタル・ターンに関する文献の増加に基づき、本稿では、**ニュース推薦システムの民主的役割をめぐる脅威と機会を評価するための概念的フレームワーク**を提供し、さまざまな **"democratic recommenders"(=民主的推薦システム??)のtypology**(=分類化や類型化する事??)を展開する。

# Introduction はじめに

Are AI and algorithms a threat to, or an opportunity for, the democratic role of the media? Although it is clear that algorithmic news recommendations will have an important role in shaping the democratic contribution of the press, it is still subject to debate whether this development is for the better or the worse.
AIとアルゴリズムは、メディアの民主的役割にとって脅威なのか、それとも好機なのか？アルゴリズムによるニュース推薦が、報道の民主的貢献を形成する上で重要な役割を果たすことは明らかだが、**この発展が良い方向なのか悪い方向なのかは、まだ議論の余地がある**。
There are those who warn about the potentially negative implications for democracy – filter bubbles, sphericules, polarisation, fragmentation and the general demise of the public sphere (Pariser Citation2011; Sunstein Citation2001).
フィルターバブル、スフェリキュール、分極化、分断化、そして公共圏の一般的な終焉といった、民主主義にとって潜在的にネガティブな影響について警告する人々がいる(Pariser Citation2011; Sunstein Citation2001)。

- (以下は用語の整理)
- Filter Bubbles(フィルターバブル):
  - 概要: インターネット上での情報のフィルタリングにより、ユーザが**自分の既存の信念や興味に合った情報だけにさらされる**現象。
  - 例: ソーシャルメディアや検索エンジンがユーザのクリック履歴や過去の行動に基づいて、そのユーザにとって好意的な情報を優先的に表示する。
- Sphericules(スフェリキュール):
  - 概要: 特定のトピックや意見に焦点を当て、その中で閉じた情報空間が形成される現象。
  - 例: 特定の政治的立場や興味を共有するユーザが、**同じ情報源から同じ種類の情報を受け取り**、他の視点や情報にはあまり触れない状態。
- Polarisation(ポーラリゼーション):
  - 概要: 意見や立場が極端な対立に分かれる現象。
  - 例: 社会的な議論が二極化し、中間の立場が減少することにより、対話が難しくなり、対立が激化する。(Polarisationはフィルターバブル等によって発生するような現象??:thinking:)
- Fragmentation(フラグメンテーション):
  - 概要: 情報や社会が小さな断片に分割される現象。
  - 例: インターネット上の多くの情報源やコミュニティがあり、それぞれが異なる情報や価値観を提供することで、社会が断片化する。
- Demise of the Public Sphere(公共領域の崩壊):
  - 概要: 公共の討論や意思決定における共通の場所やプラットフォームが減少する現象。
  - 例: インターネット上での情報の分断や極端な意見の対立が進むことにより、公共の領域が崩壊し、健全な議論が難しくなる。(これは最悪のシナリオにおける最終的な到達点、みたいな??:thinking:)

Others are concerned about the “black box” character of recommenders and the difficulty of holding algorithms accountable for their public value implications (Diakopoulos and Koliska Citation2017).
また、レコメンダーの「ブラックボックス」的性格や、アルゴリズムが持つ公共的価値への影響について説明責任を果たすことの難しさを懸念する人もいる（Diakopoulos and Koliska Citation2017）。
Yet others emphasise the opportunities that arise for the news media – opportunities to rejuvenate the media, allow more responsiveness to the interests of readers, deploy exciting new business models and find smarter, data-driven ways to engage with their audiences.
しかし、ニュースメディアにとって次のような機会が生まれることを強調する人もいる: メディアの若返り、読者の関心へのさらなる対応、エキサイティングな新しいビジネスモデルの展開、よりスマートでデータに基づいた視聴者との関わり方の発見などである。

In the 2018 Reuters Report, almost three quarters of the editors, CEOs and digital leaders interviewed indicated that they were already experimenting with AI or were planning to do so (or were planning to do more experimenting), and that the particular focus of their initiatives would be, in addition to robo-journalism, algorithmic news recommendations (Newman, Citation2018, 29).
2018年のロイター・レポートでは、インタビューした編集者、最高経営責任者（CEO）、デジタル・リーダーのほぼ4分の3が、AIを使った実験をすでに行っているか、行う予定である(あるいは、さらに実験を行う予定である)と回答しており、特に注力する取り組みとしては、ロボ・ジャーナリズムに加えて、アルゴリズムによるニュース推薦が挙げられている（Newman, Citation2018, 29）。(へぇー:thinking:)
The task of algorithmic news recommenders is to filter the growing abundance of online information.
アルゴリズム・ニュース・レコメンダーの仕事は、**増え続けるオンライン情報をフィルタリングすること**である。(そういう意味では、パーソナライズしなくても、誤情報や、過剰な釣り記事を除外する事も、仕事の一つであると言える。)
Generally, four types of news recommender algorithms can be distinguished, namely algorithms that make personalised recommendations on the basis of metadata (content based), insights into what other users like to read (collaborative filtering), data on their users (knowledge based), or a combination thereof (Karimi, Jannach, Jugovac, 2018).
一般に、**ニュース推薦アルゴリズムには次の4つのタイプがある**: すなわち、メタデータに基づくパーソナライズ推薦(コンテンツベース)、他のユーザが好んで読むものに対する洞察に基づくパーソナライズ推薦(協調フィルタリング)、ユーザに関するデータ(knowledge-based)、またはそれらの組み合わせに基づいてパーソナライズされた推薦を行うアルゴリズムである(Karimi, Jannach, Jugovac, 2018)。

- (メモ)
- knowledge-basedな手法: ユーザ自身が要求を推薦システムに明示的に入力し、適宜要求を修正しながら、最終的に満足のいくアイテムを見つける手法。lifecycleの短いニュース推薦ではあんまり使われてないらしい:thinking:
  - 参考: https://speakerdeck.com/okukenta/recsys-text-intro04_knowledge-based_recommender_system?slide=4
  - knowledge

Another important distinction is that between self-selected recommendations (users determine the selection criteria and feed the system with their own preferences) and preselected recommendations (media determine the selection, based on volunteered or inferred data; Thurman and Schifferes Citation2012).
もう一つの重要な区別は、**self-selected recommendations**(ユーザが選択基準を決定し、自分の好みをシステムに与える)と**preselected recommendations**(メディアが、ボランティアまたは推論されたデータに基づいて、選択を決定するThurman and Schifferes Citation2012)の違いである。
Depending on the media outlet and the metrics that recommendation algorithms are being optimised for, news recommendations can be used to increase time spent, advertising revenues and user satisfaction, but also to actively guide readers and match individual readers with the news it is apt for them to receive.
メディアや推薦アルゴリズムが最適化される指標にもよるが、ニュース推薦を利用することで、滞在時間、広告収入、ユーザ満足度を向上させるだけでなく、読者を積極的に誘導し、個々の読者が受け取るのに適したニュースをマッチングさせることもできる。
The focus of this article is on the latter, and it will be argued that the power to actively guide and shape individuals’ news exposure also brings with it new responsibilities and new very fundamental questions about the role of news recommenders in accomplishing the media’s democratic mission.
本稿の焦点は後者(=preselected recommendations)であり、個人のニュース露出を積極的に誘導し形成する力は、メディアの民主的使命を達成する上でのニュース推薦システムの役割について、新たな責任と非常に根本的な疑問をもたらすものでもあることを論じる。
How diverse or not diverse, and how personally relevant and inclusive should recommendations be?
どの程度多様であるべきか、あるいは多様でないのか、また、どの程度個人的な関連性があり、包括的であるべきか。
How far should the media go in engaging with the audience, and what is the role of other values, such as participation, transparency, deliberation and privacy?
メディアはどこまで視聴者と関わるべきか、また、参加、透明性、熟慮、プライバシーといった他の価値観の役割は何か。
What are the longer term societal implications of personalised information exposure?
パーソナル化された情報露出は、長期的にはどのような社会的影響を及ぼすのだろうか？
And more generally, what are the objectives and values that recommendations should be optimised for?
さらに一般的に言えば、レコメンデーションが最適化されるべき目的と価値とは何か？

In order to be able to answer these questions, we need more insights into the different values at stake and how personalised recommendations can positively or negatively affect the realisation of these values (Helberger, Karppinen, and D’acunto Citation2018; Helberger Citation2011).
これらの問いに答えられるようになるには、問題となっているさまざまな価値観と、パーソナライズ推薦がこれらの価値観の実現にどのようにプラスまたはマイナスの影響を与えるかについて、より深い洞察が必要である（Helberger, Karppinen, and D'acunto Citation2018; Helberger Citation2011）。
The objective of this article is therefore to explore how democratic theory can offer a useful frame for assessing the threats posed by news recommenders to the democratic role of the media, and the opportunities they present.
そこで本稿の目的は、民主主義理論が、ニュース推薦システムがメディアの民主的役割にもたらす脅威と、それらがもたらす機会を評価するために、いかに有用なフレームを提供できるかを探ることである。
In so doing, the article hopes to prepare the ground for a more nuanced discussion of algorithmic recommenders, AI and filter bubbles, and help to explore how news recommenders can contribute to democratic goals and editorial missions.
そうすることで、この記事は、アルゴリズムによる推薦システム、AI、フィルターバブルについてのよりニュアンスに富んだ議論の土台を整え、ニュース推薦システムが民主主義の目標や編集の使命にどのように貢献できるかを探る一助となることを期待している。

# News Recommenders and Democracy – Hopes and Concerns ニュースレコメンダーと民主主義 - 期待と懸念

The media are a central institution in any democratic society (Balkin Citation2018) and they have at least two important roles to play.
メディアは民主主義社会の中心的機関であり（Balkin Citation2018）、少なくとも**2つの重要な役割**を担っている。
One is to inform citizens, to provide them with the information they need to make meaningful political choices and help to hold their democratically elected representatives accountable.
ひとつは、市民に情報を提供し、**有意義な政治的選択をするために必要な情報を提供し、民主的に選ばれた代表者の責任を追及する手助けをすること**である。
Part of this information function is to critically investigate and report about important societal and political matters, and warn citizens about misconduct and problematic situations that require the attention of voters (the “watchdog function” of the media).
この情報機能の一部は、社会的・政治的に重要な事柄を批判的に調査・報道し、有権者の注意を必要とする不祥事や問題状況について市民に警告することである（メディアの「番犬機能」）。
The other is to create a diverse public forum where the different ideas and opinions in a democratic society can be articulated, encountered, debated and weighed.
もうひとつは、民主主義社会におけるさまざまな考えや意見を明確にし、出会い、議論し、評価することができる**多様な公共の場を作ること**である。
As we will see, the relative weight that the different theories of democracy attach to these two roles varies, and in the case of news recommenders the roles can even conflict, which is an important source of concerns about the democratic role of recommenders.
後述するように、民主主義の異なる理論がこの2つの役割に与える相対的な重みはさまざまであり、ニュース推薦システムの場合、この役割が対立することさえある。

## Better Informed Citizens versus Concerns about the Demise of the Public Sphere より良い情報を持つ市民対公共圏の終焉への懸念

Many citizens consider recommenders a good way to get the news and to navigate their way through the growing abundance of information, and in some circumstances they even consider them preferable to journalistically curated choices (Thurman et al.Citation2018).
多くの市民は、推薦システムはニュースを入手し、増え続ける豊富な情報の中から自分の進むべき道をナビゲートしてくれる良い方法だと考えており、状況によっては、ジャーナリスティックにキュレーションされた選択肢(=編集者が選ぶ方法?:thinking:)よりも好ましいとさえ考えている（Thurman et al.Citation2018）。
The ability to filter and customise the information offer enables the media to be more responsive to the concrete information needs of users, and brings journalists one step closer to truly engaging with their audience.
提供する情報をフィルタリングし、カスタマイズする能力によって、メディアはユーザの具体的な情報ニーズにより応えることができるようになり、ジャーナリストは視聴者との真のエンゲージメントに一歩近づくことができる。
In so doing, algorithmic recommendations respond to an old criticism of liberal authors about the media patronising the user (Wentzel Citation2002) and the lack of media responsiveness, which some have even described as “one of the most difficult problems for media regulation” (Gibbons Citation1998).
そうすることで、アルゴリズミック・レコメンデーションは、メディアがユーザーを贔屓にしている（Wentzel Citation2002）というリベラル派の著者の古くからの批判や、メディアの応答性の欠如に応えることになる、
これは、「メディア規制にとって最も困難な問題のひとつ」（Gibbons Citation1998）とさえ言われている。
Usher (2010) predicts that audience tracking will “turn[…] journalism from elitism of writing for itself and back to writing what people are actually looking for.” Hindman goes one step further, arguing it is an obligation for journalists to use audience analytics, for exactly this reason (Hindman 2017).
Usher（2010）は、視聴者追跡によって "ジャーナリズムは自分のために書くというエリート主義から、人々が実際に求めているものを書くことに立ち返るだろう "と予測している。Hindmanはさらに一歩踏み込んで、まさにこの理由から、オーディエンス分析を利用することはジャーナリストの義務であると主張している（Hindman 2017）。
What is more, personalised news recommendations allow the media not only to help users find relevant information, but also to inform them better and more effectively.
さらに、パーソナライズされたニュース推薦によって、メディアはユーザが関連情報を見つけるのを助けるだけでなく、よりよく、より効果的に情報を提供することができる。
‘The audience’ is not homogenous but consists of a diversity of audiences, each with its own preferences, interests and information needs, as well as different levels of education and ways of processing information.
**「視聴者」は均質なものではなく、それぞれが独自の嗜好、関心、情報ニーズを持ち、教育レベルや情報処理の方法も異なる多様な視聴者で構成されている**。
By using AI and algorithms, news recommenders can better accommodate these differences.
AIとアルゴリズムを使うことで、ニュース推薦システムはこうした違いにうまく対応できるようになる。

The ability to serve individual users better and more effectively is also the source of some of the most prominent concerns about the impact of recommenders on democracy.
**レコメンダーが民主主義に与える影響に関する最も顕著な懸念の根源**は、個々のユーザにより良く、より効果的にサービスを提供する能力でもある。
In an environment in which each user gets the news she needs, will there still be a public forum where diverse ideas and opinions can meet? Not only academics but also regulators warn that there is at least “a risk that recommendations are used in a manner that narrows citizens’ exposure to different points of view, by reinforcing their past habits or those of their friends” (OFCOM Citation2012).
各ユーザが必要なニュースを入手する環境において、多様な考えや意見が集まる公共の場は存在するのだろうか？学者だけでなく規制当局も、少なくとも「過去の習慣や友人の習慣を強化することで、**市民がさまざまな視点に触れる機会を狭めるような形で推薦が使われるリスクがある**」と警告している（OFCOM Citation2012）。(まさにフィルターバブル的な話:thinking:)
Lively debates about the extent to which news recommenders enclose users in filter bubbles (Pariser Citation2011) and echo chambers (Sunstein Citation2001) and about a public sphere that gradually dissolves into sphericules (Gitlin Citation1998) are essentially concerns about the tension between a media environment in which algorithms sort people into information profiles and interest bubbles, and the public forum function of the media.
ニュース推薦ツールがどの程度ユーザをフィルター・バブル（Pariser Citation2011）やエコーチェンバー（Sunstein Citation2001）に囲い込むか、また、徐々に球体に溶解していく公共圏（Gitlin Citation1998）について活発に議論されているが、これは本質的に、アルゴリズムが人々を情報プロファイルや関心バブルに選別するメディア環境と、メディアの公共フォーラム機能との間の緊張に関する懸念である。
Concerns about a fragmentation of the media landscape with the effect that people no longer encounter counter-attitudinal or unexpected information and therefore become less tolerant, more polarised or even radical existed before the arrival of news recommenders (Helberger, 2006).
メディア状況の分断化によって、人々が反論的な情報や予期せぬ情報に遭遇しなくなり、その結果、寛容さが失われ、偏向的、あるいは過激になるのではないかという懸念は、ニュースレコメンダーが登場する以前からあった（Helberger, 2006）。
What distinguishes the filter bubble scenario from more general concerns about the ongoing media fragmentation is the relative lack of user agency, particularly in instances of preselected recommendations, and the opacity of the process.
フィルターバブルのシナリオが、現在進行中のメディアの断片化に関するより一般的な懸念と異なるのは、ユーザの主体性が相対的に欠如していること、特にpre-selected recommendationsの例では、そのプロセスが不透明であることだ。
Furthermore, with recommenders, stereotypes and prejudices can be reinforced through perpetual algorithmic feedback loops.
**さらに、レコメンダーを使えば、アルゴリズムによる永続的なフィードバックループを通じて、固定観念や偏見が強化される可能性がある**。
As a consequence, the fault lines between the different groups or fragments in society deepen, and in the worst case become impossible to bridge.
その結果、社会のさまざまなグループや断片の間の断層は深まり、最悪の場合、埋めることが不可能になる。

# Hopes for, and Concerns about, the Future of the Media as a Democratic Institution 民主的制度としてのメディアの将来に対する期待と懸念

At a more structural level, scholars increasingly worry about the implications of AI and algorithms for the sustainable future of the media as an institution.
より構造的なレベルでは、AIやアルゴリズムがメディアという組織の持続可能な未来に与える影響について、学者たちはますます心配するようになっている。
Will the media still be able to independently observe and report what is worth reporting when it is no longer the editor who decides what is newsworthy, having been replaced by algorithms and the quantified interests and preferences of the audience? (Anderson Citation2011).
**何がニュースに値するかを決定するのはもはや編集者ではなく、アルゴリズムと数値化された視聴者の興味や嗜好に取って代わられたとき、メディアはまだ独自に観察し、報道する価値のあるものを報道できるだろうか**?(アンダーソン引用2011)。
Ferrer-Conill and Tandoc (Citation2018, 13) are among those who warn that “[a]vailable metrics then become proxies to … journalistic ideals, especially for overworked journalists.” An important factor in this context is the degree of internal and external commercial pressure (Coddington 2015) from advertisers (Turow Citation2005), and from other sources of “commercial optimalisation” such as search engines, social media platforms and web analytics companies (Newman Citation2018, 31; Belair-Gagnon and Holton Citation2018, 15; see also Lewis and Usher Citation2016).
Ferrer-ConillとTandoc (Citation2018, 13)は、「利用可能な指標は、特に働き過ぎのジャーナリストにとって、...ジャーナリズムの理想に対するプロキシになる」と警告している。この文脈における重要な要因は、広告主（Turow Citation2005）や、検索エンジン、ソーシャルメディア・プラットフォーム、ウェブ分析会社といった「商業的最適化」の他の情報源からの、内外の商業的圧力（Coddington 2015）の程度である（Newman Citation2018, 31; Belair-Gagnon and Holton Citation2018, 15; Lewis and Usher Citation2016も参照）。
The alleged opacity of algorithms (Diakopoulos and Koliska 2017) adds to these concerns, as this opacity can make it more difficult to identify external influences on the media, as well as to hold the media accountable for the way they carry out their democratic task and journalistic mission.
アルゴリズムの不透明性（Diakopoulos and Koliska 2017）が、こうした懸念に拍車をかけている。この不透明性は、メディアに対する外部からの影響を特定することを難しくするだけでなく、メディアがその民主的任務とジャーナリズムの使命を遂行する方法について説明責任を果たすことを難しくしかねないからだ。
Finally, in the digital environment the traditional media find themselves in fierce competition with truly digital natives, such as social media platforms and search engines, some of which have far more data than the traditional media, and far more expertise and experience in the competition for the attention of users (Moore Citation2016).
最後に、デジタル環境において、伝統的メディアは、ソーシャルメディア・プラットフォームや検索エンジンなど、真のデジタル・ネイティブとの激しい競争にさらされている。

At the same time, data and data analytics offer the news media economic and strategic advantages, and could thus very well be a means for them to regain (and hold) both territory and the attention of their readers.
同時に、**データとデータ分析は、ニュースメディアに経済的・戦略的な利点を提供し、その結果、ニュースメディアが領土と読者の注目の両方を取り戻す（保持する）手段となる可能性も大いにある**。
Societal concerns about the lack of transparency and diversity and the danger of filter bubbles in the online environment also provide an opportunity for the traditional media to create a profile for themselves distinct from that of social media platforms that optimise for commercial goals that are very different from the goal of promoting better informed citizens and the public sphere.
透明性と多様性の欠如や、オンライン環境におけるフィルターバブルの危険性についての社会的懸念は、伝統的メディアにとって、より良い情報を持つ市民や公共圏を促進するという目標とはまったく異なる商業的目標に最適化されたソーシャルメディア・プラットフォームとは一線を画す、自らのプロフィールを作成する機会にもなる。(メディア本来の目的を意識する事は、ユニークで魅力的なメディアになる機会でもあるよ！って話??:thinking:)
In addition, the ability to optimise for advertising (Newman Citation2018), paying readers and more efficient internal routines (Zamith Citation2018, 423) can help newsrooms both to make more sense of the media economy in which they operate and to survive in the “battle for audience attention” (Cherubini and Nielsen Citation2016, 9).
さらに、広告（Newman Citation2018）、有料読者、より効率的な社内ルーチン（Zamith Citation2018, 423）に最適化する能力は、ニュースルームが活動するメディア経済をより理解し、「視聴者の注目をめぐる戦い」（Cherubini and Nielsen Citation2016, 9）で生き残るために役立つ。

# Concerns about Surveillance, Manipulation and the Erosion of Intellectual Privacy

If the task of the media is to inform citizens and provide a public forum, how much distance between the media and their audiences is actually needed to ensure that the media can fulfill this task? In other words, what is the role of data and privacy, and what are the potential dangers of the media knowing too much about their audience? Because many (though not all) news recommenders will use personal data to optimise their results and better match results with individual users, new concerns about this constant tracking and monitoring accompany the media’s quantitative turn.
メディアの任務が**市民に情報を提供し、公共の場を提供すること**だとすれば、メディアがこの任務を確実に果たすためには、メディアと視聴者の間に実際どれほどの距離が必要なのだろうか？言い換えれば、データとプライバシーの役割とは何か、メディアが視聴者について知りすぎることの潜在的な危険性とは何か。多くの（すべてではないが）ニュースレコメンダーは、その結果を最適化し、個々のユーザーと結果をよりマッチングさせるために個人データを使用するため、この絶え間ない追跡と監視に関する新たな懸念は、メディアの量的転換に伴うものである。
As Richards (Citation2008, 392) explains, a certain measure of intellectual privacy is “critical to the most basic operations of expression, because it gives new ideas the room they need to grow”.
Richards (Citation2008, 392)が説明するように、一定の知的プライバシーは「表現の最も基本的な営みにとって重要である。
The constant surveillance can also affect more directly the democratic role of the media, for example where there may be chilling repercussions for users’ exercise of their free speech rights, or where digital technology is used to manipulate opinions.
例えば、言論の自由を行使するユーザに対して冷ややかな反応があったり、デジタル技術が意見操作に使われたりするような場合だ。
Put differently, protecting the privacy of their users can be a way of protecting the very activity we expect media users, as citizens, to engage in, namely critical and diverse thinking.
別の言い方をすれば、メディア利用者のプライバシーを保護することは、私たちが市民としてメディア利用者に期待する活動、すなわち批判的で多様な思考を保護することにつながる。

As this brief overview shows, the debate about the role of news recommenders in a democratic media landscape has been characterised by varied hopes and concerns, assumptions and anecdotal evidence.
この簡単な概要が示すように、民主的なメディア状況におけるニュース推薦者の役割に関する議論は、さまざまな希望や懸念、仮定や逸話的証拠によって特徴づけられてきた。
Some of these hopes and concerns contradict, others seem unconnected.
これらの希望と懸念は矛盾するものもあれば、つながりがないように見えるものもある。
What is missing is a conceptual framework for assessing the threats and opportunities of news recommenders that helps to critically question some of the assumptions made and, more generally, to understand news recommenders in the broader context of the democratic role of the media.
**欠けているのは、ニュースレコメンダーの脅威と機会を評価するための概念的枠組み**であり、それによって、いくつかの仮定を批判的に問い直し、より一般的には、メディアの民主的役割というより広い文脈でニュースレコメンダーを理解することができる。
This is why the next section takes a step back and, building on theories of democratic media, sets out to develop such a framework.
だからこそ、次の章では一歩引いて、民主的メディアの理論に基づきながら、そのような枠組みを構築していくのである。

# A Conceptual Framework for Assessing the Democratic Role of News Recommenders ニュースレコメンダーの民主的役割を評価するための概念的枠組み

Many excellent scholars have developed theories of democracy and the media – work that has contributed greatly to informing our expectations about the role that the media and informed citizens should play in a democracy (Christians Citation2009; Strömbäck Citation2005; Dahlberg Citation2011; Ferree et al.Citation2002; Curran Citation2015).
多くの優れた学者が民主主義とメディアに関する理論を構築しており、民主主義においてメディアと情報化された市民が果たすべき役割について私たちの期待に大きく寄与している（Christians Citation2009; Strömbäck Citation2005; Dahlberg Citation2011; Ferree et al.Citation2002; Curran Citation2015）。
Their work forms the point of departure for the current investigation.
彼らの研究は、今回の調査の出発点となった。
Given the central role that the media play in a democratic society, democratic theories form a logical normative framework to concretise the societal role of the media, as well as to evaluate their performance.
民主主義社会においてメディアが果たす中心的役割を考えれば、民主主義理論はメディアの社会的役割を具体化し、そのパフォーマンスを評価するための論理的な規範的枠組みを形成する。
This article argues that, by extension, the same must be true for news recommenders, to the extent that news recommenders are a tool for the media to fulfill their roles.
本稿は、ニュースレコメンダーがメディアの役割を果たすためのツールであるという点で、ニュースレコメンダーにも同じことが言えるはずだと主張する。(民主主義社会においてメディアが果たすべき中心的役割 = ニュース推薦が果たすべき役割?)
Since it would be impossible to recount all democratic theories within one article, this article focus on what are arguably the three main and most commonly used theories in academic work on the media (Karppinen Citation2013b): liberal, participatory and deliberative theories.
1つの論文ですべての民主主義理論を回顧することは不可能であるため、本稿では、メディアに関する学術的研究において間違いなく主要かつ最も一般的に用いられている**3つの理論**に焦点を当てる（Karppinen Citation2013b）： 自由主義理論、参加型理論、熟議型理論である。
Carving out the different theoretical approaches behind these theories will allow the development of three different perspectives on the democratic role of recommenders.
これらの理論の背後にある異なる理論的アプローチを明らかにすることで、推薦者の民主的役割に関する3つの異なる視点を発展させることができる。
Although it would undoubtedly be extremely interesting to discuss news recommenders against the background of a far richer and more differentiated approach to democratic theory (such as critical democratic theory, which this article only briefly touches upon), space is limited and the main point that this article wishes to make is that there are multiple ways in which recommenders can contribute to the democratic role of the media, provided they are developed out of a vision of the values that recommenders are used to serve.
民主主義理論に対するはるかに豊かで差別化されたアプローチ（批判的民主主義理論など、本稿ではほんの少し触れるにすぎない）を背景にニュース推薦者を論じることは、間違いなくきわめて興味深いのだが、スペースは限られており、本稿が主張したいのは、推薦者が奉仕するために使われる価値観から発展させるのであれば、推薦者がメディアの民主的役割に貢献できる方法は複数あるということである。
Different democratic theories foreground different values and expectations for news recommenders.
民主主義理論の違いによって、ニュース推薦者に対する価値観や期待は異なる。

# Liberal Models of Democracy 民主主義の自由主義モデル

Within the liberal tradition, further distinctions are made, such as Christians’ pluralist model (Christians Citation2009), which corresponds largely with Strömbäck’s (Citation2005) competitive model of democracy, or Curran’s (Citation2015) rational choice model.
リベラルの伝統の中では、クリスチャンの多元主義モデル（Christians Citation2009）やカランの合理的選択モデル（Curran Citation2015）など、さらなる区別がなされている。
Common to all these perspectives is the idea of a decentralised model of political power, where different groups and ideas compete for influence and ultimately political power in the “market place of ideas” (Napoli Citation1999; see also the critical analysis by Karppinen Citation2013a), and do so unhampered by the state or other institutions.
これらの視点に共通するのは、政治権力の分散モデルという考え方であり、そこではさまざまな集団や思想が「思想の市場」（ナポリ引用1999；カルピネン引用2013aによる批判的分析も参照）において影響力、ひいては政治権力を競い合い、国家やその他の制度に妨げられることなくそうしている。
Central shared values are individual freedom – including fundamental rights such as the right to privacy and freedom of expression – dispersion of power, personal development and autonomy.
共有される価値観の中心は、プライバシーや表現の自由といった基本的権利を含む個人の自由、権力の分散、個人の成長、自律性である。

The challenge for liberal democracy is to eventually aggregate all these different views and ideas into political will in a process that Christians (Citation2009, 97) describes as “constant negotiation”.
リベラル・デモクラシーの課題は、クリスチャン（Citation2009, 97）が「絶え間ない交渉」と表現するプロセスにおいて、最終的にこれらすべての異なる見解や考えを政治的意思に集約することである。
Accordingly, elections are a central democratic moment.
したがって、選挙は民主主義の中心的な瞬間である。
It is at election time that citizens can express their political will, by voting for the party that best represents their interests.
市民が政治的意思を表明できるのは選挙時であり、自分たちの利益を最もよく代表する政党に投票することである。
In the liberal model, democratic participation and being a good citizen therefore largely revolve around the act of voting, as opposed to more participatory or deliberative models where citizens’ active participation in the public discourse is far more central.
リベラルなモデルでは、民主主義への参加と善良な市民であることは、投票という行為を中心に展開され、市民が積極的に公論に参加する参加型や熟議型のモデルとは対照的である。
As Ferree et al.(Citation2002, 290) put it: “Citizens need policy makers who are ultimately accountable to them but they do not need to participate in public discourse on policy issues.
Ferreeら(Citation2002, 290)はこう言っている： 「市民は、自分たちに対して最終的に説明責任を負う政策立案者を必要としているが、政策問題についての公論に参加する必要はない。
Not only do they not need to, but public life is actually better off if they don’t.”
そうする必要がないだけでなく、そうしない方が公共の場はより良いものになる」。

With respect to the information needs of citizens, this means that there is little reason why citizens should not read and watch what they like, as long as in the run-up to elections, they are sufficiently informed to cast their votes (Ferree et al.Citation2002, 291).
市民の情報ニーズに関して言えば、選挙までの間に十分な情報を得て投票する限り、市民が好きなものを読んだり見たりしない理由はほとんどないということだ（Ferree et al.Citation2002, 291）。
There is a strong focus on personal autonomy – the freedom to choose the information one is interested in.
個人的な自主性、つまり自分の興味のある情報を選択する自由を強く重視している。
What does that mean for the information role of the media? If one follows Christians (Citation2009, 100), “[r]ather than trying to inform citizens about issues over which they have no direct and immediate control, journalism serves an administrative democracy by alerting the community to crises … [and providing] detailed accounts of campaign promises and platforms, especially during the months preceding a contested election” (in a similar vein, Strömbäck Citation2005, 335).
メディアの情報的役割とは何を意味するのだろうか。クリスチャン（Citation2009, 100）に従えば、「ジャーナリズムは、市民が直接的かつ直接にコントロールできない問題について市民に情報を提供しようとする以上に、地域社会に危機を知らせ......（中略）......（中略）......（中略）......選挙公約や綱領の詳細な説明を、特に争われる選挙前の数ヶ月間に提供することによって、行政民主主義に貢献している」（同様の意味で、Strömbäck Citation2005, 335）。
This is Zaller’s “burglar alarm” standard, where rather than aspiring to an ideal (and unrealistic) situation in which citizens are broadly informed on all matters relevant to public affairs, the media instead must make them aware of acute problems that merit their immediate attention (Zaller Citation2003).
これはザラーの "防犯ベル "基準であり、市民が公共問題に関連するすべての事柄について広く知らされているという理想的な（そして非現実的な）状況を目指すのではなく、メディアはその代わりに、市民が直ちに注意を払うに値する深刻な問題を認識させなければならない（Zaller Citation2003）。

# Implications for a Liberal Recommender リベラル・レコメンダーへの示唆

From the perspective of liberal democratic traditions, recommenders, then, could potentially have quite literally laiberating role, to the extent that they put the interests and information preferences of users centre stage.
自由民主主義の伝統からすれば、レコメンダーは、利用者の関心と情報の好みを中心に据える限りにおいて、文字どおり、自由を与える役割を果たす可能性がある。
True, the orientation towards the user, and the possible resulting hyper-responsiveness of the press, might result in a situation in which newsrooms select content based on users’ preferences, and not on what the audience ‘ought to know’.
確かに、ユーザーへの志向と、その結果として起こりうる報道機関の超反応性は、ニュースルームが視聴者の「知るべきこと」ではなく、ユーザーの嗜好に基づいてコンテンツを選択するという状況をもたらすかもしれない。
But how worrisome are these concerns under a more liberal perspective on democracy? From the liberal perspective, it is essentially a prerogative of citizens to decide which information they need so they can make well-informed decisions, and they should be able to do so free from external influences.
しかし、民主主義をよりリベラルにとらえた場合、こうした懸念はどの程度憂慮すべきものなのだろうか。リベラルな視点に立てば、十分な情報に基づいた意思決定をするために必要な情報を決めるのは、基本的に市民の特権であり、市民は外部の影響から自由にそれを行うことができるはずである。
And if citizens primarily choose to look at cat videos and celebrity news? Under more liberal conceptions of democracy, that could be perfectly fine as long as doing so is a result of the way they exercise their autonomy and freedom of expression.
もし市民が主に猫の動画や有名人のニュースを見ることを選んだとしたら？民主主義に対するよりリベラルな考え方の下では、そうすることが彼らの自治と表現の自由を行使した結果である限り、それはまったく問題ないだろう。
Or to quote Strömbäck (Citation2005,334): “How people choose to spend their time and their mental energy is up to themselves, as long as they do not violate the basic democratic freedoms and rights.
あるいは、Strömbäck（引用2005,334）の言葉を引用しよう： 「民主主義の基本的な自由と権利を侵害しない限り、人々が自分の時間と精神的エネルギーをどのように使うかは、彼ら自身の自由である。
To demand that people in general spend their lives keeping up with the news, getting informed, and participating in public life, is to demand too much.”
一般の人々に、ニュースについていくこと、情報を得ること、公的な生活に参加することに人生を費やすことを要求するのは、過剰な要求だ」。

It may be that people have already gathered from other sources the information they need to make informed decisions, for example from non-personalised parts of the website or conversations with friends.
例えば、ウェブサイトのパーソナライズされていない部分や友人との会話など、十分な情報に基づいた意思決定を行うために必要な情報を、他の情報源からすでに収集している場合もあります。
It may be that the citizen can actually be trusted to demand the information that she needs to cast an informed vote.
情報に基づいて投票するために必要な情報を要求する市民は、実は信頼できるのかもしれない。
It may also be that newsrooms are not the perfect and uncontested arbiters of what citizens “need to know” (Boczkowski 2013).
また、ニュースルームは、市民が「知る必要があること」（Boczkowski 2013年）についての完璧で議論の余地のない裁定者ではないのかもしれない。
The point is: user-driven content choices do not necessarily have to be undemocratic, and the same is true for news recommenders that provide users with user-driven recommendations.
重要なのは ユーザー主導のコンテンツ選択は必ずしも非民主的である必要はなく、ユーザー主導のレコメンデーションをユーザーに提供するニュースレコメンダーにも同じことが言える。
There is arguably some minimal information that the population should receive, for example information about democratic, economic and social crises.
例えば、民主主義、経済、社会的危機に関する情報など、国民が受け取るべき最低限の情報は間違いなく存在する。
This information, however, does not necessarily need to be provided in the form of recommendations; it could be offered as part of the general website, with the recommender being nothing more than an added service.
しかし、この情報は必ずしもレコメンデーションの形で提供される必要はなく、一般的なウェブサイトの一部として提供され、レコメンデーターは付加的なサービスにすぎない。
One could also argue that recommendations could differ during and outside election times, and that the balance between what people want to know and what they need to know to take informed election decisions could vary.
また、選挙期間中とそれ以外では、推奨される内容が異なる可能性があり、人々が知りたいことと、十分な情報に基づいた選挙の意思決定をするために知る必要があることのバランスが異なる可能性があるとも言える。
What is important is that no opinion should intentionally be excluded (Ferree et al.Citation2002, 293).
重要なのは、いかなる意見も意図的に排除すべきではないということである（Ferree et al.Citation2002, 293）。
Whether or not it is prominently presented, or even ranked high enough to be noticed, will depend on its popularity and the size of the audience that wants to hear that view.
それが目立つように紹介されるかどうか、あるいは注目されるほど上位にランクされるかどうかは、その人気と、その見解を聞きたいと思う観客の規模による。
In other words, there is no obligation to provide equal representation; nor is there a right to an audience (Christians Citation2009; Napoli Citation2011, 108).
言い換えれば、平等な表現を提供する義務はなく、謁見を受ける権利もない（Christians Citation2009; Napoli Citation2011, 108）。
It would be perfectly logical for a recommender to give more prominence to those ideas that have the greatest popularity or dominance within society.
レコメンダーが、社会的な人気や優位性を持つ考え方をより重視するのは、まったく論理的なことだ。

A necessary precondition is, of course, that a recommendation does realise users’ autonomy and right to receive information (Eskens, Helberger, and Möller 2017).
もちろん、必要な前提条件は、推薦がユーザーの自律性と情報を受け取る権利を実現することである（Eskens, Helberger, and Möller 2017）。
While it is true that recommenders can potentially make the media more responsive to the information needs of, and demands from, citizens, recommendation technologies can also ignore or misinterpret signals from users (Ekstrand and Willemsen Citation2016).
確かにレコメンダーは、市民の情報ニーズや要求にメディアがより敏感に反応できるようになる可能性があるが、レコメンデーション技術は、ユーザーからのシグナルを無視したり、誤解したりする可能性もある（Ekstrand and Willemsen Citation2016）。
Much will depend on the quality and the sophistication of the analytics and metrics, and the extent to which they are truly able to uncover people’s news needs and interests (Hindman 2017, 189).
その多くは、アナリティクスと測定基準の質と洗練度、そしてそれらが人々のニュースのニーズと関心を真に掘り起こすことができるかどうかにかかっている（Hindman 2017, 189）。
If algorithms are used to nudge or influence citizens against their will (Calo Citation2014) or in an attempt to manipulate their political choices, then they pose a danger to liberal democracies.
もしアルゴリズムが、市民の意思に反して（Calo Citation2014）、あるいは市民の政治的選択を操作しようとして、市民を誘導したり影響を与えたりするために使われるなら、自由民主主義国家に危険をもたらすことになる。
From a liberal perspective, then, perhaps the more important point of attention regarding the potential democratic role of recommenders is their editorial independence from external parties, such as advertisers, political parties or marketing divisions.
リベラルな観点からすれば、レコメンダーの潜在的な民主的役割に関してより重要な注目点は、広告主や政党、マーケティング部門といった外部の関係者からの編集上の独立性だろう。
Another important point of attention under the liberal model would be the extent to which the control over algorithmic recommenders and, perhaps even more importantly, the datasets needed to fuel them, could lead to the creation of new concentrations of market or opinion power, for example in the form of social media platforms.
リベラルなモデルのもとで注目されるもうひとつの重要な点は、アルゴリズムによるレコメンデーターや、おそらくさらに重要なこととして、レコメンデーターに燃料を供給するために必要なデータセットのコントロールが、例えばソーシャルメディアプラットフォームのような形で、市場やオピニオンパワーの新たな集中を生み出す可能性がどの程度あるかということである。
From the perspective of liberal democracy, and its strong focus on the dispersion of power (compare (Karppinen Citation2013a, 31: dispersion of power as “the basis of liberal democracy”; Edwin Baker Citation1998), this is a serious threat to democracy.
リベラル・デモクラシーの観点、および権力の分散に強く焦点を当てている観点（比較（Karppinen Citation2013a, 31： エドウィン・ベイカー引用1998年）、これは民主主義にとって深刻な脅威である。
From the perspective of public policy, herein lie two tasks, namely to prevent data-driven concentrations of opinion power and to ensure that recommenders do indeed reflect the free and autonomous choices of citizens, rather than becoming tools for manipulating public opinion and tinkering with citizens’ minds.
すなわち、データ主導によるオピニオンパワーの集中を防ぐことと、レコメンダーが世論を操作したり市民の心をいじったりする道具になるのではなく、市民の自由で自律的な選択を本当に反映するようにすることである。

A more liberal perspective on democracy would also suggest a more organic and more “interest-driven” approach to diversity.
民主主義に対するよりリベラルな視点は、多様性に対するより有機的で、より「利益誘導的」なアプローチも示唆するだろう。
So far, diversity has mostly been discussed in terms of what the audience ‘needs to know’.
これまでのところ、ダイバーシティは観客が『知る必要があること』という観点で語られることがほとんどだった。
With a more liberal recommender, it would be perfectly acceptable to speak of information that the heterogeneous citizenry “wants to know.” Therefore, a well-designed, diverse recommender would also incorporate a certain element of flexibility, allowing citizens to customise the recommendations to better reflect their interests and preferences, even if not all users will make use of that opportunity, a decision that would be fine as long as it constituted an expression of their autonomy (Harambam et al.Citation2018).
よりリベラルなレコメンダーでは、異質な市民が "知りたい "と思う情報といってもまったく問題ないだろう。したがって、よく設計された多様なレコメンダーには、ある種の柔軟性も盛り込まれ、市民が自分の興味や嗜好をよりよく反映するようにレコメンダーをカスタマイズできるようになる。たとえすべてのユーザーがその機会を利用しないとしても、その決定が市民の自律性の表現である限りは構わないだろう（Harambam et al.Citation2018）。
In fact, preselected choices, particularly when they do not allow citizens to understand why they have received particular recommendations, or do not provide them with the means to influence the settings, are suspicious from a liberal theory point of view.
実際、事前に選択された選択肢、特に市民が特定の推薦を受けた理由を理解できなかったり、設定に影響を与える手段を提供しなかったりする場合は、自由主義理論の観点から見て疑わしい。
One could even go a step further and argue that a liberal recommender would do more than just inform people.
さらに一歩進んで、リベラルなレコメンダーは単に情報を提供するだけではないと主張することもできる。
It would also allow people to have a say regarding the proper balance between their right to information and personal development, and other rights, such as the right to privacy.
また、情報提供や自己啓発の権利と、プライバシーの権利など他の権利との適切なバランスについて、人々が発言することも可能になるだろう。
Seeing that algorithmic news recommendations operate through the collection of large amounts of data, offering users a choice between receiving relevant information and reading anonymously, or perhaps using recommenders that personalise on the basis of meta-data rather than on the basis of users’ inferred interests, would fit perfectly well in the liberal tradition of putting individual rights and freedoms centre stage.
アルゴリズムによるニュースレコメンデーションが大量のデータ収集を通じて機能していることを見れば、ユーザーに関連情報を受け取るか、匿名で読むかの選択肢を提供することも、あるいは、ユーザーが推測した興味に基づいてではなく、メタデータに基づいてパーソナライズするレコメンダーを使用することも、個人の権利と自由を中心に据えるリベラルの伝統に完全に適合するだろう。
This is not to say that the rights to privacy and data protection are less relevant under the other democratic perspectives, but it is under the liberal perspective that a strong argument can be made that the right to privacy, personal autonomy and freedom of expression can outweigh other interests, such as displaying particular “public interest content” more prominently, or nudging users to consume more diverse or more “valuable” information and engage more with the perspectives of others.
プライバシーやデータ保護に対する権利が、他の民主主義的な観点のもとではあまり関係がないとは言わないが、リベラルな観点のもとでこそ、プライバシーや個人の自律、表現の自由に対する権利が、特定の「公益的なコンテンツ」をより目立つように表示したり、利用者がより多様で「価値のある」情報を消費し、他者の視点にもっと関与するように誘導したりするなど、他の利益よりも優先されうるということを強く主張できるのである。

How about concerns over filter bubbles? Interestingly, from a more liberal perspective one could argue that a situation in which users are recommended exactly the information that they request or find interesting could help them to deepen their knowledge and expertise, and thereby enable them to play their role in the democratic process even better and more efficiently.
フィルターバブルに対する懸念はどうだろうか？興味深いことに、よりリベラルな観点からは、ユーザーが要求する、あるいは興味深いと思う情報を的確に推薦される状況は、ユーザーの知識や専門性を深めるのに役立ち、それによって民主主義プロセスにおける役割をより良く、より効率的に果たすことを可能にする、と主張することができる。
Much depends on the conception of what an ‘ideal’ citizen is – an information omnivore, an “expert citizen” or an “everyday maker?” (compare Li and Marsh Citation2008).
理想的な」市民とは何か、つまり情報の雑食者、「専門家市民」、それとも「日常的な作り手」なのか、という概念に大きく左右される。(Li and Marsh Citation2008を参照）。
Particularly interesting here is the role of experts in more liberal models of democracy.
ここで特に興味深いのは、よりリベラルな民主主義モデルにおける専門家の役割である。
As Ferree et al.(Citation2002, 292) explain, the relatively low normative expectations of what it means to be a good citizen are counterbalanced by a prominent role for experts “in defining the issues before they reach the stage at which decisions need to be reached.” In other words, under more liberal democratic models recommenders that feed the focused information needs of expert citizens could fulfill an important role in a democratic society.
Ferree et al.(Citation2002, 292)が説明するように、良い市民であることの意味に対する規範的期待が比較的低いことは、「意思決定が必要な段階に達する前に問題を定義する」という専門家の重要な役割によって相殺されている。言い換えれば、よりリベラルな民主主義モデルのもとでは、専門家である市民の集中的な情報ニーズに応えるレコメンダーが、民主主義社会において重要な役割を果たす可能性がある。
In such a situation, filter bubbles become “expertise bubbles” and have an important role in helping expert citizens to become even more expert.
このような状況では、フィルターの泡は「専門知識の泡」となり、専門家である市民がさらに専門家になるのを助ける重要な役割を果たす。
We could possibly also see the development of two, or even more, types of recommenders: “general interest recommenders” – which serve people’s diverse information needs and preferences – and more “expert” recommenders, which help to make the experts more expert.
また、2種類、あるいはそれ以上のレコメンダーが開発される可能性もある： 人々の多様な情報ニーズや嗜好に応える「一般的な」レコメンダーと、専門家をより専門的にするための、より「専門的な」レコメンダーである。
Indeed, from the perspective of dispersion of power, pluralism in the future could extend not only to a diversity of media sources and content, but also to a diversity of recommenders for a diversity of user needs.
実際、権力の分散という観点からすれば、将来の多元主義は、メディア・ソースやコンテンツの多様性だけでなく、多様なユーザー・ニーズに対するレコメンダーの多様性にも及ぶ可能性がある。

# Participatory Models of Democracy 民主主義の参加型モデル

In contrast to the libertarian focus on autonomy, user agency and dispersion of power, the central focus of more civic (Christians Citation2009, 101), respectively participatory (Strömbäck Citation2005) or republican models of democracy is on a shared civic culture and commitment to citizenship (Christians Citation2009, 102).
自治、利用者の主体性、権力の分散を重視するリバタリアンとは対照的に、より市民的な（Christians Citation2009, 101）、それぞれ参加型（Strömbäck Citation2005）、あるいは共和制的な民主主義モデルの中心的な焦点は、市民文化の共有とシティズンシップへのコミットメントにある（Christians Citation2009, 102）。
And unlike in the more liberal model discussed in the previous section, in the more participatory understanding of democracy, the active participation of citizens is key and the central mechanism for political will formation.
また、前節で述べたよりリベラルなモデルとは異なり、より参加型の民主主義の理解においては、市民の積極的な参加が鍵となり、政治的意思形成の中心的なメカニズムとなる。
Only if all citizens are (at least in theory, and ideally in practice) able to actively participate, have their say or even exercise political functions, can we speak of a true participatory democracy.
すべての市民が（少なくとも理論上は、そして理想的には実際には）積極的に参加し、発言し、あるいは政治的機能を行使することができてはじめて、真の参加型民主主義を語ることができる。
Accordingly, the values that proponents of more participatory models of democracy bring to the fore are very different from those emphasised by proponents of the liberal model: inclusiveness instead of representativeness; equality and tolerance instead of proportionality; and community, active participation and civic virtue instead of self-development, autonomy and ultimate freedom.
したがって、より参加型の民主主義モデルの支持者が前面に押し出す価値観は、自由主義モデルの支持者が強調する価値観とは大きく異なる： 代表性の代わりに包摂性、比例性の代わりに平等と寛容、自己開発、自律性、究極の自由の代わりに共同体、積極的参加、市民の美徳である。

In the discussion about the democratic role of recommenders, two ideas are particularly relevant: one is that societal interest trumps individual self-interest, and the other, which is closely related, is that there are high normative expectations of what it means to be a good citizen.
推薦者の民主的役割に関する議論では、2つの考え方が特に関連する： ひとつは、社会の利益が個人の自己利益に勝るということであり、もうひとつは、密接に関連しているが、善良な市民であることの意味について高い規範的期待があるということである。
Central to advancing welfare is not the sum of individual actions (or preferences), but active collaboration, engagement and subordination to the common good (Etzioni Citation1996).
福祉を向上させる中心は、個人の行動（あるいは嗜好）の総和ではなく、積極的な協力、関与、共通善への従属である（Etzioni Citation1996）。
This ideal of more or less direct self-government cannot be achieved without a certain moral attitude of the citizen or “homo politicus” (Held Citation2006, 29).
この多かれ少なかれ直接的な自治の理想は、市民のある種の道徳的態度、すなわち "ホモ・ポリティカス"（Held Citation2006, 29）なしには達成できない。
This is a citizen who cannot afford to be uninterested in politics and who understands that political participation is “a necessary aspect of the good life” (Held Citation2006, 35) or at least absolutely necessary to secure one’s own liberty and that of the community.
政治に無関心ではいられない市民であり、政治参加は「善き人生の必要な側面」（Held Citation2006, 35）であり、少なくとも自分自身と共同体の自由を確保するためには絶対に必要なものだと理解している。

It is clear that with the more active political role of the citizen, the information needs of the citizen change.
市民の政治的役割がより積極的になるにつれ、市民の情報ニーズが変化することは明らかである。
Instead of having a basic knowledge of political institutions and political alternatives, the active, informed citizen needs to have a far deeper knowledge of not only the political system, but also the different issues on the political agenda – even more so to the extent that she is interested in playing an active part in the making of politics.
積極的な情報通の市民は、政治制度や政治的選択肢に関する基本的な知識を持つ代わりに、政治システムだけでなく、政治課題に関するさまざまな問題についても、はるかに深い知識を持つ必要がある。
Accordingly, the media have an important task in satisfying citizens’ demands for in-depth information - documentaries about social issues, background information and more general information about the political climate (compare Strömbäck Citation2005, 339).
したがって、メディアは、社会問題に関するドキュメンタリー、背景情報、政治情勢に関するより一般的な情報など、詳細な情報を求める市民の要求を満たすという重要な任務を担っている（Strömbäck Citation2005, 339を参照）。
Arguably, and in stark contrast to the liberal model, the role of the media, and here in particular the public service media, shifts from merely informing to actively educating and coaching the active citizen.
リベラルなモデルとは対照的に、メディア、とりわけ公共メディアの役割は、単に情報を提供することから、積極的な市民を積極的に教育し指導することへと移行する。
Tandoc and Thomas (Citation2015, 244) characterise this position well: “If journalism is to help bring about the common good, it must provide the public with more than just what the public wants.”
Tandoc and Thomas (Citation2015, 244)はこの立場をよく表している： 「ジャーナリズムが公益をもたらす手助けをするのであれば、大衆が望む以上のものを提供しなければならない。

Here, also, the expectations with regard to diversity are greater; there is a different and potentially more demanding idea of what constitutes a diverse information offer.
ここでも、多様性への期待はより大きく、多様な情報提供とは何かについて、異なる、そして潜在的により厳しい考え方がある。
Diversity is less about presenting alternatives and accommodating the heterogeneous interests of a heterogeneous citizenry.
多様性とは、代替案を提示したり、異質な市民の異質な関心に対応したりすることではない。
Diversity must represent “all significant interests in society” (Curran Citation2015), including political parties, political, economic and civil society interest groups, religious groups, professional organisations, and so on.
多様性は、政党、政治、経済、市民社会の利益団体、宗教団体、専門家組織など、「社会におけるすべての重要な利益」を代表するものでなければならない（Curran Citation2015）。
A diverse media offer speaks to the different groups in society and inspires them to take an active part in society.
多様なメディアの提供は、社会のさまざまなグループに語りかけ、彼らが社会で積極的な役割を果たすよう促す。
Inclusiveness is critical (Edwin Baker Citation1998, 334; Balkin Citation2018), as is visibility.
包括性は重要であり（Edwin Baker Citation1998, 334; Balkin Citation2018）、可視性も重要である。
Only when citizens are aware of the different perspectives, interests and concerns in a society and are able to tolerate and even further them, is political participation deserving of the name.
市民が社会におけるさまざまな視点、関心、懸念を認識し、それらを容認し、さらに推し進めることができてはじめて、政治参加はその名に値するものとなる。
For the media in the digital environment, this creates an extra challenge: to order and present content in such a way that it reflects the diversity of ideas and opinions.
デジタル環境におけるメディアにとって、これは新たな挑戦となる： それは、多様な考えや意見を反映するようにコンテンツを整え、提示することである。
This necessitates not only a process of inclusion but also a process of exclusion.
そのためには、包摂のプロセスだけでなく、排除のプロセスも必要となる。
In other words, the information task of the media includes making responsible selections, and also making conscious decisions about what not to show because the attention span of people is limited and screen space is scarce.
言い換えれば、メディアの情報タスクには、責任ある選択をすることと、人々の注意力には限りがあり、スクリーンスペースも限られているため、何を見せるべきでないかを意識的に決定することが含まれる。
Or, in the words of Meiklejohn (Meiklejohn Citation1948), 19): “What is essential is not that everyone shall speak.
あるいは、マイクルジョン（Meiklejohn Citation1948）の言葉を借りれば、19）： 「肝心なのは、全員が発言することではない。
But that everything worth saying shall be said.” It becomes clear that news recommenders, as ultimate selection tools, can have a very important democratic role to play in a participatory democracy.
しかし、言う価値のあることはすべて言わなければならない" 究極の選択ツールとしてのニュース推薦者が、参加型民主主義において非常に重要な民主的役割を果たしうることは明らかである。

Please note that, so far, participation has been discussed primarily with reference to the public as a whole.
なお、これまでのところ、参加については主に一般市民全体について論じてきた。
Participation as a democratic value can also require consideration of those who are typically excluded from participation, such as marginalised groups or minorities.
民主主義の価値としての参加は、周縁化された集団やマイノリティなど、一般的に参加から排除される人々への配慮も必要となりうる。
This is particularly the case under more critical theories of democracy that require citizens to discover and experience the many marginalised voices in public and private life.
これは特に、より批判的な民主主義理論のもとでは、市民が公的・私的生活において周縁化された多くの声を発見し、経験することを求めるケースである。
Arguably, this could even mean privileging marginalised voices so they “can offer the ‘double vision’ of those who are ‘outsiders within’ the system” (Ferree et al, Citation2002, 307).
これは、周縁化された人々の声を特権化することで、「システム内の "部外者 "である人々の "二重の視野 "を提供できる」（Ferree et al, Citation2002, 307）ことを意味する。

# Implications for a Participatory Diverse Recommender 参加型多様性レコメンダーへの示唆

The particular challenge and opportunity for the participatory recommender will be to make a selection that gives a fair and inclusive representation of different ideas and opinions in society, while also helping a user to gain a deeper understanding and to feel engaged, rather than confused, by the abundance of information out there.
参加型レコメンダーにとっての特別な挑戦であり機会であるのは、社会におけるさまざまな考えや意見を公平かつ包括的に代表するような選択をすることであり、同時に、ユーザーがより深い理解を得て、世の中に溢れる情報に惑わされることなく、むしろ積極的に関与していると感じられるようにすることである。
Instead of simply giving people what they want (at this particular moment), a participatory recommender will be committed to a far more principled understanding of “participatory diversity.” It must proactively address the fear of missing out on important information and depth, as well as concerns about being left out.
参加型レコメンダーは、単に（今この瞬間に）人々が望むものを提供するのではなく、"参加型の多様性 "をはるかに原理的に理解することに力を注ぐだろう。それは、重要な情報や深みを見逃すことへの恐れや、取り残されることへの懸念に積極的に対処しなければならない。
The participatory recommender is not simply a smarter means to increase user satisfaction and better serve readers: it becomes an important element of active curation of the digital news offer.
参加型レコメンダーは、単にユーザーの満足度を高め、読者によりよいサービスを提供するためのスマートな手段ではない： デジタル・ニュースの積極的なキュレーションの重要な要素となる。

Arguably, even though the main thematic focus of the participatory recommendations will be on political content/news, non-political content must also be fairly represented, so as to enable ordinary people to reflect on daily-life challenges and issues and how they can be approached.
おそらく、参加型勧告の主なテーマが政治的な内容やニュースに絞られるとしても、一般の人々が日常生活の課題や問題、そしてそれらにどのようにアプローチできるかについて考えることができるように、政治的な内容以外のものも公平に扱われなければならない。
For the same reason, in-depth discussions, background content and commentary will also become more important.
同じ理由で、綿密な議論、背景となるコンテンツ、解説もより重要になるだろう。
Alternatively, a news medium might decide to leave the task of presenting a diverse selection of content to the front pages, and instead use recommendation technology to recommend further reading, in-depth information on similar topics and historical items about the same topic from the archive.
あるいは、あるニュース媒体は、多様なコンテンツの選択をフロントページに任せ、その代わりにレコメンデーション・テクノロジーを使って、さらに読むべき本や、似たようなトピックに関する詳細な情報、同じトピックに関する歴史的なアイテムをアーカイブから推薦することにするかもしれない。
Overall, the performance of a diverse recommender that seeks to promote active involvement in politics will be measured by its success in addressing and mobilising all groups in society.
全体として、政治への積極的な参加を促進しようとする多様なレコメンダーのパフォーマンスは、社会のあらゆる集団に働きかけ、動員することに成功したかどうかで測られる。

More attention is also required concerning the form in which the news is delivered.
ニュースがどのような形で伝えられるかについても、より注意が必要である。
Because the ultimate goal is participation, recommendations should seek to galvanize.
最終的な目標は参加であるため、提言は活気を与えることを目指すべきである。
The media “should frame politics in a way that mobilizes people’s interests and participation in politics” (Strömbäck Citation2005, 340).
メディアは「人々の関心と政治への参加を動員するような形で、政治を枠組みづけるべきである」（Strömbäck Citation2005, 340）。
To be truly empowering, media content therefore needs to be presented in a diversity of formats and communication styles (Ferree et al.Citation2002, 298; Christians Citation2009, 102; Zaller Citation2003, 122).
真に力を与えるためには、メディア・コンテンツは多様なフォーマットとコミュニケーション・スタイルで提示される必要がある（Ferree et al.Citation2002, 298; Christians Citation2009, 102; Zaller Citation2003, 122）。
Where the mission is to stimulate active participation, more engaging, emphatic, emotional, critical and even activist tones should be used.
積極的な参加を促すことが使命である場合、より魅力的で、強調的で、感情的で、批判的で、さらには活動家的なトーンを使うべきである。
And where the objective is fostering tolerance, the general tone may be more reconciliatory, non-threatening, non-sensationalist, rational, and compassionate.
また、寛容の育成を目的とする場合、一般的なトーンは和解的、非脅迫的、非感覚主義的、理性的、思いやりのあるものになるかもしれない。

But the participatory recommender is potentially more than a tool to inform.
しかし、参加型レコメンダーは、情報を提供するツール以上の可能性を秘めている。
Taking seriously the idea of the role of the news media in engaging and galvanizing the readership, participatory recommenders can have an important role in actively coaching and engaging users.
読者を惹きつけ、活気づけるというニュースメディアの役割を真剣に考えれば、参加型レコメンダーは、ユーザーを積極的に指導し、惹きつけるという重要な役割を持つことができる。
If a user spends a large amount of screen time on celebrity news or sports, a recommender could nudge her to also try some political news.
ユーザーが有名人のニュースやスポーツに多くの時間を費やしている場合、レコメンダーは政治ニュースも見るように促すことができる。
If a user prefers to sit in her own left/right/centrist bubble, a responsible participatory recommender could recommend content from a different perspective.
もしユーザーが自分の左／右／中心主義的なバブルの中に座ることを好むなら、責任ある参加型レコメンダーは異なる視点からコンテンツを推薦することができる。
Preselected recommenders, in particular, offer clear opportunities in that context.
特に、事前に選ばれた推薦者は、そのような状況において明確な機会を提供する。
And seen from the perspective of more critical democratic theories, recommenders could be turned into even more powerful instruments to draw our scarce attention to the marginalised, invisible or less powerful ideas and opinions in societies with the objective of escaping the muffling standard of civility and the language of the stereotypical “middle-aged, educated, blank white man” (Young Citation1996, 123–124).
そして、より批判的な民主主義理論の観点から見れば、推薦者は、社会から疎外された、目に見えない、あるいは力の弱い考えや意見に私たちの乏しい注意を向けさせるための、より強力な道具となりうる。

Clearly, actively nudging users also invokes tricky ethical questions about the fine line between information, education, and manipulation (Spahn Citation2012), as well as the media’s responsibility to “pop” filter bubbles.
明らかに、積極的にユーザーを誘導することは、情報、教育、操作の間の微妙な境界線（Spahn Citation2012）、そしてフィルターの泡を「弾く」メディアの責任に関する、やっかいな倫理的問題をも呼び起こす。
Filter bubbles, in the sense of filtering decisions that include like-minded and exclude different-minded content, can be a real concern for a participatory democracy.
フィルター・バブルとは、同じような考えを持つコンテンツは含まれ、異なる考えを持つコンテンツは排除されるという意味で、参加型民主主義にとって現実的な懸念となりうる。
A worrisome outcome from the participatory democracy perspective is a situation in which certain people will never become aware of particular ideas and opinions in society, with the filters “ghettoizing citizens into bundles based on narrow preferences and predilections rather than drawing them into a community” (Tandoc and Thomas Citation2015, 247).
参加型民主主義の観点から懸念されるのは、特定の人々が社会における特定の考えや意見に気づくことがない状況であり、フィルターによって「市民がコミュニティに引き込まれるのではなく、狭い嗜好や選好に基づく束にゲトー化される」（Tandoc and Thomas Citation2015, 247）ことである。
Having said that, in certain circumstances filter bubbles can also be conductive to the values of a participatory democracy (and even more so under certain critical theories of democracy).
とはいえ、特定の状況下では、フィルターバブルは参加型民主主義の価値観に資することもある（民主主義のある種の批判的理論下ではなおさらである）。
Filter bubbles could be a very good thing to the extent that they act as incubators of constructive speech, allowing the more marginalised voices in society to join forces and pluck up the courage to speak out (compare Ferree et al.Citation2002, 309).
フィルター・バブルは、建設的な言論のインキュベーターとして機能し、社会から疎外された人々が力を合わせ、勇気を出して発言することを可能にするという点では、非常に良いことかもしれない（Ferree et al.Citation2002, 309を参照）。
This involves a challenge for the media, academics and policymakers to establish clear guidance on how a diverse recommender design can actually help to promote a vibrant, inclusive and diverse media landscape, as well as include and galvanize disengaged or uninterested segments of the population.
このことは、メディア、学者、政策立案者にとって、多様なレコメンダー・デザインが、活気に満ちた、包括的で多様なメディア状況を促進し、また、無関心層や無関心層を取り込み、活気づけるのに実際にどのように役立つのかについて、明確な指針を確立することが課題であることを意味している。
The combination of news recommendations and social media functions could offer interesting perspectives, as long as the media, platforms and policymakers succeed in controlling undesirable side effects, such as hate speech, the spread of misinformation and the abuse of digital technology to polarise and radicalize.
メディア、プラットフォーム、政策立案者が、ヘイトスピーチ、誤報の拡散、デジタル技術の悪用による偏向や過激化など、望ましくない副作用の抑制に成功する限り、ニュース推奨機能とソーシャルメディア機能の組み合わせは、興味深い視点を提供する可能性がある。

In a situation where algorithmic selection decisions are driven more by editorial logic than by individual citizens’ information needs, and the societal function of the media comes more to the fore, the ability of society to hold the media accountable for algorithmic selection decisions becomes more important.
アルゴリズミックな選択決定が、個々の市民の情報ニーズよりも編集の論理によって行われ、メディアの社会的機能がより前面に出てくる状況では、社会がアルゴリズミックな選択決定についてメディアに説明責任を果たさせる能力がより重要になる。
Much of the criticism levelled at algorithmic news recommendations is centred on their opacity and ‘black box’ character (Diakopoulos and Koliska Citation2017).
アルゴリズムによるニュース推薦に対する批判の多くは、その不透明さと「ブラックボックス」的な性格に集中している（Diakopoulos and Koliska Citation2017）。
This lack of transparency and the consequent inability of the community to hold the media accountable can be particularly problematic from the participatory democracy perspective, where “freedom of the press exists to serve the interests of the community, not the interests of journalists and their manager.
このような透明性の欠如と、その結果、コミュニティがメディアに責任を負わせることができないことは、「報道の自由は、ジャーナリストやそのマネージャーの利益ではなく、コミュニティの利益に奉仕するために存在する」という参加型民主主義の観点からは、特に問題となりうる。
The community, rather than market forces or even the newsroom itself, needs to be the final arbiter of journalism’s quality and value” (Christians Citation2009, 104).
ジャーナリズムの質と価値を最終的に決定するのは、市場原理やニュースルームそのものではなく、コミュニティである必要がある」（Christians Citation2009, 104）。
Transparency about the editorial logic behind recommendations and why citizens are being shown certain content and not other content becomes not only a matter of compliance with data protection laws’ requirement of explainability, or a way to enhance personal agency, but also a matter of central democratic interest: transparency in this sense makes it possible for the community to hold the media accountable and to judge the value of recommendations.
推薦の背後にある編集ロジックや、なぜ市民が特定のコンテンツを見せられ、他のコンテンツを見せられないのかについての透明性は、説明可能性というデータ保護法の要件を遵守する問題や、個人の主体性を高める方法というだけでなく、民主主義の中心的な関心事となる： この意味での透明性は、コミュニティがメディアに説明責任を負わせ、推薦の価値を判断することを可能にする。

# Deliberative (or Discursive) Models of Democracy 民主主義の熟議モデル

The participative and the deliberative models of democracy share a focus on community, the placing of societal interest above individual self-interest, and the importance of active, interested citizens.
民主主義の参加型モデルと熟議型モデルは、共同体に焦点を当て、個人の自己利益よりも社会の利益を優先し、積極的で関心のある市民を重要視するという点で共通している。
One of the major differences, however, is that the deliberative model operates on the premise that ideas and preferences are not a given, and that we must focus more on the process of identifying, negotiating and, ultimately, agreeing on different values and issues (Ferree et al.Citation2002, 300; Held Citation2006, 233).
しかし、大きな違いの一つは、熟議モデルは、考えや選好は所与のものではなく、異なる価値観や問題点を特定し、交渉し、最終的に合意するプロセスに重点を置かなければならないという前提で運営されていることである（Ferree et al.Citation2002, 300; Held Citation2006, 233）。
This involves a process of actively comparing ideas, and engaging with ideas that may be contrary to our own (Manin Citation1987).
これには、積極的に考えを比較し、自分の考えとは相反する考えにも関与するプロセスが含まれる（Manin Citation1987）。
Or as Timothy Garton Ash (Garton Ash Citation2016, 212) has put it so succinctly: “I cannot fully express myself – that is, my self – unless I identify my differences with others.” Doing so requires a sphere of mutual shared values and equality: “The dynamics of deliberative democracy are characterised by the norms of equality and symmetry; everyone is to have an equal chance of participation” (Dahlgren Citation2006).
あるいは、ティモシー・ガートン・アッシュ（Garton Ash Citation2016, 212）が簡潔にこう言っている： 「他者との差異を認識しない限り、私は自分自身、つまり自己を完全に表現することはできない。そのためには、相互に価値観を共有し、平等な領域が必要である： 「熟議民主主義のダイナミクスは、平等と対称性の規範によって特徴づけられる。
With regard to the role of the media, the deliberative conception of democracy thus places particular emphasis on the media’s public forum function.
メディアの役割に関して、民主主義の熟議概念は、メディアのパブリック・フォーラム機能を特に重視している。
In addition to fostering critical values such as deliberation, critical and rational reflection, equal chances to participate, tolerance and open-mindedness, creating a public forum and optimal conditions for engagement becomes a value in itself.
熟慮、批判的で理性的な考察、平等な参加の機会、寛容さ、オープンマインドといった批判的な価値観を育むことに加え、公共の場と参加に最適な条件を作り出すこと自体が価値となる。

Under a deliberative perspective, it is thus not enough to “simply” inform people.
熟慮の視点に立てば、人々に「単に」情報を提供するだけでは不十分なのである。
The media should provide “an arena for everyone with strong arguments and direct its attention to those who can contribute to a furthering of the discussion” (Strömbäck Citation2005, 341).
メディアは、「強い主張を持つすべての人に場を提供し、議論の促進に貢献できる人に注意を向ける」（Strömbäck Citation2005, 341）べきである。
Not only is this an invitation for the media to actively guide users’ attention; it suggests the media also have a duty to proactively confront the audience with different and challenging viewpoints that they have not considered before, or not in this way: “Deliberation requires not only multiple but conflicting points of view because conflict of some sort is the essence of politics” (Manin Citation1987, 352).
これは、メディアがユーザーの関心を積極的に誘導するよう促しているだけでなく、メディアには、視聴者がこれまで考えたことのないような、あるいはこのような形では考えたことのないような、異なる視点や挑戦的な視点を積極的に視聴者に突きつける義務があることを示唆している： 「熟議には複数の視点だけでなく、対立する視点も必要である。ある種の対立が政治の本質だからである」（Manin Citation1987, 352）。
Here, diversity becomes instrumental in challenging users to compare and modify their opinions and broaden their horizons.
ここで、多様性は、ユーザーが自分の意見を比較し、修正し、視野を広げることに挑戦する上で重要な役割を果たす。
What is more, exposure to diverse information is essential as a means of fostering a certain open mindedness and tolerance, or what Ferree et al.(Citation2002, 303) call “readiness for dialogue.” Only if people are actually interested in, and curious about, the positions of others, or are motivated to research different perspectives on a particular subject, are they ready to engage in critical reflections with themselves and deliberations with others.
さらに、多様な情報に触れることは、ある種のオープンマインドや寛容さ、あるいはFerreeら（Citation2002, 303）が言うところの "対話の準備 "を育む手段として不可欠である。人々が実際に他者の立場に興味を持ち、好奇心を抱いたり、特定のテーマについて異なる視点を研究する意欲を持ったりして初めて、自分自身と批判的な考察を行い、他者と熟慮する準備が整うのである。
Interestingly, diversity in this reading acquires an almost personalised component: in the deliberative tradition the recommendation that is truly diverse is that which can challenge a particular individual; that is, recommendations that exposes her to ideas and opinions she has not previously been exposed to and challenges her established beliefs.
興味深いことに、この読みにおける多様性は、ほとんど個人的な要素を含んでいる： 審議の伝統において、真に多様な勧告とは、特定の個人に挑戦することができるものである。つまり、その人がこれまで触れたことのない考えや意見に触れ、その人が確立している信念に挑戦するような勧告である。
But as users cannot deliberate upon all ideas and opinions (Manin Citation1987, 356), some element of purposeful filtering is necessary, particularly under the deliberative perspective.
しかし、利用者はすべてのアイデアや意見を熟慮することはできないので（Manin Citation1987, 356）、特に熟慮的な観点の下では、何らかの意図的なフィルタリングが必要である。

# Implications for a Deliberative Recommender 熟慮型レコメンダーへの示唆

It is under the deliberative conception of democracy that algorithmic recommendations can present the greatest opportunities to the democratic process, as well as the most profound threats.
民主主義の熟議的概念のもとで、アルゴリズムによる勧告は民主的プロセスに最大の機会をもたらすと同時に、最も深刻な脅威となりうる。
Not surprisingly, the main critics of algorithmic filtering come from this tradition and warn about polarisation, fragmentation and filter bubbles.
当然のことながら、アルゴリズムによるフィルタリングの主な批判者はこの伝統に由来し、偏光、断片化、フィルターバブルについて警告している。
This is because under the deliberative tradition in particular, the ability to inform people in a more targeted, personally effective way clearly clashes with the second, public forum function of the media.
というのも、特に熟議の伝統の下では、より的を絞った、個人的に効果的な方法で人々に情報を提供する能力は、メディアの第二の機能であるパブリック・フォーラムと明らかに衝突するからである。
Using recommendations to limit people to information that they find agreeable and that appeals to their own interests, excluding voices that challenge, and depriving them of a comprehensive overview of the different ideas and opinions that exist in a society, is in direct conflict with the deliberative ideal.
推薦状を使って、人々が同意し、自分の利益にアピールする情報に限定し、異議を唱える声を排除し、社会に存在するさまざまな考えや意見の包括的な概観を奪うことは、熟議の理想と真っ向から対立する。

But recommendations could also be used in a completely different way: precisely because they are data-driven, recommenders can also take each individual’s different ideas, beliefs and opinions and use them as points of departure, suggesting alternative viewpoints that the individual has not yet thought of.
しかし、レコメンデーションはまったく別の使い方もできる： レコメンダーはデータ駆動型であるからこそ、各個人のさまざまな考えや信念、意見を取り入れ、それを出発点として、その人がまだ考えたことのない別の視点を提案することもできる。
Interestingly, personalisation could become a critical feature of a deliberative recommender, as it allows particular individuals to be challenged and exposed to ideas and opinions that they would not have come across on their own.
興味深いことに、パーソナライゼーションは熟議型レコメンダーの重要な特徴になりうる。
Thus, news recommenders’ democratic role may be not only to inform users but to educate them and nudge them to broaden their horizons and make them practised in tolerance.
したがって、ニュース推薦者の民主的な役割は、利用者に情報を提供するだけでなく、利用者を教育し、視野を広げ、寛容さを身につけさせることなのかもしれない。
Recommenders could expose the reader to extra, in-depth background material.
レコメンダーは、読者にさらに深い背景資料を提供することができる。
They could present different perspectives alongside each other, and also make the user aware of what her current place is in the ideological spectrum.
異なる視点を並べて提示することで、イデオロギー的なスペクトルの中で自分が今どのような位置にいるのかをユーザーに認識させることもできる。
They could become an important instrument for fostering critical reflection and open-mindedness.
批判的な考察とオープンマインドを育むための重要な手段となるだろう。

This means that the path to realising the opportunities offered by algorithmic recommendations and the path to countering the threats they pose are actually one and the same: diversity-sensitive design.
つまり、アルゴリズミック・レコメンデーションがもたらす機会を実現する道と、それがもたらす脅威に対抗する道は、実は同じものなのだ： 多様性に配慮したデザイン
Recommenders can be designed using relatively simple metrics such as clicks and likes, or what content friends liked, but there is no reason why recommendations cannot employ more sophisticated metrics.
レコメンダーは、クリック数や「いいね！」数、あるいは友人がどのコンテンツを気に入ったかといった比較的単純な指標を使って設計することができるが、レコメンデーションがより洗練された指標を採用できない理由はない。
The real challenge for academics, policymakers, editors, journalists and the developers of recommender algorithms is to jointly conceptualise diversity in terms of metrics that deliberative algorithms can be optimised for.
学者、政策立案者、編集者、ジャーナリスト、そしてレコメンダー・アルゴリズムの開発者にとっての真の挑戦は、審議的アルゴリズムが最適化できる指標という観点から、多様性を共同で概念化することである。
The overall goal must be to ensure that citizens remain exposed to a diversity of information, and to counter the undemocratic effects of recommendation that make a significant impact on public opinion formation in a way that is counter-productive to a general “readiness for dialogue” in parts of the population.
全体的な目標は、市民が多様な情報に接し続けられるようにすること、そして、国民の一部における一般的な「対話の準備」に逆行するような形で、世論形成に大きな影響を与える勧告の非民主的な影響に対抗することでなければならない。

Specifically, in recommendations where the focus is more on fostering tolerance and open-mindedness, the ratio of content featuring different cultures and different ethnic, national and linguistic groups, or representatives thereof, will be more relevant, as will presenting content in different languages and giving prominence to content that describes shared experiences (“challenging diversity”).
具体的には、寛容さとオープンマインドを育むことに重点が置かれる勧告では、異なる文化や異なる民族、国家、言語グループ、またはそれらの代表者を取り上げたコンテンツの比率がより適切となり、異なる言語でのコンテンツの提示や、共有された経験（「多様性への挑戦」）を描写するコンテンツの重要性が増す。
And while under the representative liberal model it would probably be acceptable if the recommender presented a proportionally larger share of content that conforms to the ideas and opinions of political majorities, what is key under the deliberative model is not proportionality, but equality.
また、代表的リベラルモデルでは、推薦者が政治的マジョリティの考えや意見に合致したコンテンツを比例して多く提示することはおそらく受け入れられるだろうが、熟議モデルで重要なのは比例ではなく平等である。

A deliberative recommender will be successful if it can contribute to mutual understanding, foster open-mindedness and help people to look beyond their own narrow-minded horizons.
熟議型レコメンダーは、相互理解に貢献し、オープンマインドを育み、人々が自分たちの視野の狭さを乗り越えるのを助けることができれば、成功する。
One can also imagine that a deliberative recommender will strive to present a greater amount of balanced content, commentary, discussion formats and background information, as well as articles that present various perspectives and a diversity of emotions, from a range of different sources and tailored to the background, level of expertise and interests of the user.
また、熟慮型レコメンダーは、より多くのバランスの取れたコンテンツ、解説、討論形式、背景情報、また、様々なソースから、様々な視点や多様な感情を提示する記事を、ユーザーの背景、専門知識レベル、興味に合わせて提示するよう努力することも想像できる。
Such a deliberative recommender could give particular visibility to public service media content, at least to the extent that the public service media in a particular country has the function of fuelling and facilitating the public discourse.
このような熟慮型レコメンダーは、少なくとも特定の国の公共メディアが公共の言論を煽り、促進する機能を持つ限りにおいて、公共メディアのコンテンツに特別な可視性を与えることができるだろう。
It could also offer additional social features for users to comment, engage, agree/disagree and debate.1 Finally, serendipity could play a far larger role here as well, to the extent that serendipitous encounters can promote open-mindedness and mental flexibility (Schoenbach Citation2007).
最後に、セレンディピティがここでもはるかに大きな役割を果たす可能性がある。セレンディピティ的な出会いが、オープンマインドと精神的柔軟性を促進する可能性があるからだ（Schoenbach Citation2007）。

To stimulate reflection and informed debate, not only the content but also the tone and style of the information provided must promote active discourse, as tone and style are “at the heart of the discursive tradition” (Ferree et al.Citation2002, 301).
内省と情報に基づく議論を刺激するためには、提供される情報の内容だけでなく、口調やスタイルも活発な言説を促進するものでなければならない。
The focus will be on styles of communication that are impartial rather than polarising, and rational rather than emotional, and informative styles will be favoured over provocative ones that grab the user’s attention and force her to focus on one particular viewpoint.
また、ユーザーの注意を引いて特定の視点に集中させるような挑発的なスタイルよりも、情報提供的なスタイルが好まれる。

Finally, transparency about the logic behind including or excluding views and opinions plays an almost fundamental role in this type of recommender.
最後に、このタイプのレコメンダーでは、意見や感想を含めるか除外するかのロジックに関する透明性が、ほぼ基本的な役割を果たす。
More than in any other democratic conception of recommendations, it is important that people are aware of the “editorial analytical” choices (compare Cherubini and Nielsen Citation2016, 21) so that they do not assume they are receiving a comprehensive overview of the relevant ideas and opinions when they are not.
他の民主的なレコメンデーションの概念以上に重要なのは、人々が「編集者による分析的な」選択（Cherubini and Nielsen Citation2016, 21を参照）を認識し、関連するアイデアや意見の包括的な概要を受け取っていないと思い込まないようにすることである。

# Four Types of Democratic Recommenders 民主的推薦者の4つのタイプ

So far three distinct types of algorithmic recommenders have been identified, and a fourth hinted at: the liberal, participatory, critical and deliberative recommender.
これまでのところ、アルゴリズムによるレコメンダーには3つのタイプがあり、4つ目のタイプがあることが示唆されている： 自由主義的、参加型、批判的、熟慮型レコメンダーである。
Their main characteristics are summarized in the Table 1.
主な特徴を表1にまとめた。

It can be argued that the first wave of recommenders corresponded with the liberal model of democracy.
推薦者の最初の波は、民主主義の自由主義モデルに対応するものだったと言える。
Liberal recommenders can be found on social media platforms or in early news personalization projects.
リベラルなレコメンダーは、ソーシャルメディア・プラットフォームや初期のニュース・パーソナライゼーション・プロジェクトで見かけることができる。
Liberal recommenders offer users personally relevant information.
リベラル・レコメンダーは、ユーザーに個人的に関連した情報を提供する。
Often criticized for supposedly narrowing users’ views, from the perspective of liberal democracy, liberal recommenders serve perfectly legitimate goals.
リベラル・レコメンダーは、しばしばユーザーの視野を狭めると批判されるが、リベラル・デモクラシーの観点からすれば、至極まっとうな目的を果たしている。
A necessary pre-condition is that users still have the choice to gather information about politics from alternative sources and that their privacy and personal autonomy are respected.
必要な前提条件は、利用者が別の情報源から政治に関する情報を収集する選択肢を持ち、プライバシーと個人の自主性が尊重されることである。

The strong focus on user-driven recommendations may not sit easily with the editorial ambitions of some of the quality media that envision a more active role in society.
ユーザー主導のレコメンデーションへの強いこだわりは、社会により積極的な役割を果たすことを想定している一部の優良メディアの編集的野心とは相容れないかもしれない。
These news outlets may prefer a more engaging, participatory recommender.
こうした報道機関は、より魅力的で参加型のレコメンダーを好むかもしれない。
Participatory recommenders will strive to map the diversity of ideas and opinions in society, and use the affordances of digital technology to respond to differences in information needs, styles and communication preferences.
参加型レコメンダーは、社会におけるアイデアや意見の多様性をマッピングし、情報のニーズやスタイル、コミュニケーションの嗜好の違いに対応するためにデジタル技術の余裕を活用するよう努める。

Conforming to more deliberative conceptions of democracy, deliberative recommenders would need to do more – they would also need to find ways to re-create common spaces in an increasingly fragmented media environment.
より熟議的な民主主義の概念に従えば、熟議的な推薦者はもっと多くのことをする必要がある。
Exposing users to information that they may not have looked for, deliberative recommenders are tools for educating users to remain open to new or different voices in society.
ユーザーが探していなかったような情報に触れることができる熟慮型レコメンダーは、社会の新しい声や異なる声にオープンであり続けるようユーザーを教育するツールである。
It is unlikely that the deliberative recommender can be found on social media platforms or in some of the commercial media, but this type of recommender could be a viable option for public service media.
ソーシャル・メディア・プラットフォームや一部の商業メディアで審議型レコメンダーが見られる可能性は低いが、この種のレコメンダーは公共サービス・メディアにとって有効な選択肢となりうる。

Finally, the article has briefly touched upon more critical recommender types, recommenders that nudge people to encounter and acknowledge minority opinions, push readers out of the comfort zone of established opinions and engage the more marginalized voices in society.
最後に、より批判的なレコメンダーのタイプ、つまり、少数派の意見に出会い、それを認めるよう人々を後押しし、読者を既成の意見のコンフォートゾーンから押し出し、社会のより周縁化された声に関与させるレコメンダーについて簡単に触れた。
As unlikely as it is that such a type of recommender would develop under normal market conditions, critical recommenders could turn into interesting tools for NGOs, civil rights groups but also the public service media.
通常の市場環境では、このようなタイプのレコメンダーが開発される可能性は低いが、批判的なレコメンダーは、NGOや公民権団体、さらには公共サービスメディアにとって興味深いツールになるかもしれない。

Concluding Remarks
結びの言葉

News recommenders can both pose threats to, and offer real opportunities for the democratic role of the media.
ニュース推薦者は、メディアの民主的役割に脅威をもたらすと同時に、真の機会を提供することもできる。
This is why it is so important to implement the technology with a profound understanding of the democratic values algorithmic recommendations can serve.
だからこそ、アルゴリズムによるレコメンデーションが果たしうる民主主義的価値について深く理解した上で、テクノロジーを導入することが非常に重要なのである。
Too often news recommenders are developed as part of an R&D project, or with purely commercial objectives in mind.
ニュースレコメンダーは、研究開発プロジェクトの一環として、あるいは純粋に商業的な目的を念頭に置いて開発されることがあまりに多い。
Inspired by democratic theories of the media, this article has developed a framework for theorizing about the democratic potential of algorithmic recommenders, and identified three types of democratic recommenders (and hinted at a fourth one).
メディアの民主主義理論に触発され、本稿はアルゴリズムによるレコメンダーの民主的な可能性を理論化する枠組みを構築し、民主的なレコメンダーの3つのタイプを特定した（そして4つ目のタイプも示唆した）。
Different democratic theories place different values on, and have different expectations concerning, the role of the media and making citizens central.
民主主義の理論が異なれば、メディアの役割や市民を中心に据えることに関する価値観や期待も異なる。
Sometimes these expectations can conflict.
時にはこれらの期待が衝突することもある。
Whereas under more liberal perspectives that emphasise privacy, autonomy and self-development, recommenders that make recommendations based on users’ interests function well and have a clear democratic role, the same recommender would be assessed very poorly under more participatory conceptions that place societal interest above individual self-interest Similarly, a participatory recommender that succeeds in informing and galvanizing different users through personalised information could still be a concern under a more deliberative model that prefers a reconciliatory, balanced tone to contributions that inspire and engage.
プライバシー、自律性、自己啓発を重視するリベラルな考え方のもとでは、ユーザーの利益に基づいて推薦を行うレコメンダーはうまく機能し、明確な民主的役割を果たすが、個人の自己利益よりも社会の利益を重視する参加型の考え方のもとでは、同じレコメンダーでも評価は非常に低くなる。 同様に、パーソナライズされた情報によってさまざまなユーザーに情報を提供し、活力を与えることに成功した参加型レコメンダーも、刺激的で興味をそそるような貢献よりも、和解的でバランスの取れた論調を好む、より熟慮的なモデルのもとでは、やはり懸念される可能性がある。
In other words, there is no gold standard when it comes to democratic recommenders and the offering of diverse recommendations.
言い換えれば、民主的な推薦者と多様な推薦の提供に関しては、ゴールドスタンダードは存在しない。
This is why there is a typology of recommenders and different avenues the media can take to use the technology in the pursuit of their democratic mission.
だからこそ、推薦者の類型が存在し、メディアが民主的使命の追求のためにテクノロジーを利用できるさまざまな道があるのだ。

Another important insight derived from this analysis is that the potential anti-democratic effects, such as filter bubbles and restricted diversity, cannot be studied in isolation, but need to be considered in relation to the values at stake.
この分析から導き出されるもうひとつの重要な洞察は、フィルターバブルや多様性の制限といった潜在的な反民主的効果は、単独で研究することはできず、危機に瀕している価値との関連で考える必要があるということだ。
So instead of simply asking whether, as a result of algorithmic filtering, users are exposed to a limited media diet, we need to look at the context and the values one cares about.
だから、アルゴリズムによるフィルタリングの結果、ユーザーが限られたメディアにしか接することができなくなったかどうかを単純に問うのではなく、その背景や価値観に目を向ける必要がある。
Depending on the values and the surrounding conditions, selective exposure may even be instrumental in the better functioning of the media and citizens.
価値観や周囲の状況によっては、選択的な露出がメディアと市民のより良い機能のために役立つことさえある。
Also, as this article has shown depending on the democratic theory one follows, diversity in recommendations can take very different forms, from more “interest-driven” liberal conceptions of diversity, to more galvanizing forms of “participatory diversity,” to more inclusive forms of “challenging diversity.”
また、本稿が示したように、民主主義理論に従うかどうかによって、提言における多様性は、より "利益誘導型 "のリベラルな多様性の概念から、より活気あふれる "参加型多様性 "の概念、より包括的な "挑戦型多様性 "の概念まで、まったく異なる形をとりうる。

The more a democratic theory focuses on furthering societal goals rather than individual self-development, the stronger the arguments are to move away from simple, short-term metrics such as clicks towards more sophisticated metrics and responsible, editorial mission-driven design.
民主主義理論が、個人の自己開発よりも社会的目標の推進に焦点を当てれば当てるほど、クリック数のような単純で短期的な指標から、より洗練された指標や責任ある編集的使命に基づいたデザインへと移行する論拠が強くなる。
Clearly, there is a challenge here for the media as well as for policymakers to engage in more active consideration of how recommenders could further the editorial mission.
メディアにとっても、政策立案者にとっても、推薦者がどのように編集の使命を果たせるかについて、より積極的に検討することが課題であることは明らかだ。
In addition, the stronger the societal interest in well-informed citizens, the less responsiveness to the interests of users alone is considered a good thing, and the more recommenders could become an indispensable tool for the media to alert, inform or even educate readers and push them out of their intellectual comfort zones.
さらに、情報通の市民に対する社会の関心が強ければ強いほど、ユーザーの関心だけに応えることが良いことだとは考えられなくなり、レコメンダーはメディアにとって、読者に注意を促し、情報を提供し、あるいは教育し、読者を知的コンフォートゾーンから押し出すための不可欠なツールになりうる。
Alternatively, the more focus there is on individual freedoms and self-development, the more recommenders become a tool in the hands of the user, and should, first and foremost, offer the user agency with regard to her choices.
あるいは、個人の自由と自己啓発に焦点を当てれば当てるほど、レコメンダーはユーザーの手中にある道具となり、何よりもまず、ユーザーの選択に主体性を与えるべきである。

The analysis also has interesting implications for the role of users: theories that expect less active citizenship in political matters can still have high expectations regarding citizens’ management of their own information diet, and recommendations can be an important tool in that.
この分析は、利用者の役割についても興味深い示唆を与えている： 政治的な問題に対してあまり積極的でない市民を期待する理論は、それでもなお、市民が自分自身の情報食生活を管理することに大きな期待を寄せることができ、推薦状はそのための重要なツールとなりうる。
Self-selection recommenders are the preferred option in more liberal models, as opposed to more participatory or deliberative models where preselected recommenders offer more opportunities to present readers with information they “ought to read” (and where nudging them to read such information is actually a good thing).
よりリベラルなモデルでは、自己選択型のレコメンダーが好まれる。対照的に、より参加型や熟議型のモデルでは、事前に選択されたレコメンダーが、読者に「読むべき」情報を提示する機会をより多く提供する（そして、そのような情報を読むように読者をうながすことは、実際には良いことである）。
Where societal interest in well-informed, active and open-minded citizens is the dominant interest, individual interests such as privacy, autonomy and accuracy must be balanced against the opportunities that data and AI offer for better informing and even educating citizens.
十分な情報を得た、活動的で開放的な市民という社会的関心が支配的な関心である場合、プライバシー、自律性、正確性といった個人の関心と、データとAIが提供する、市民により良い情報を提供し、さらには教育する機会とのバランスを取らなければならない。
Algorithmic news recommendations in themselves are neither good nor bad for democracy.
アルゴリズムがニュースを推薦すること自体は、民主主義にとって良いことでも悪いことでもない。
It is the way the media use the technology that creates threats, or opportunities.
脅威や機会を生み出すのは、メディアの技術の使い方なのだ。
