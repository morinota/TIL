refs: https://www.sciencedirect.com/science/article/pii/S0166361520305558


# A knowledge-graph platform for newsrooms ニュースルームのための知識グラフプラットフォーム  
Arne Berven, Ole A. Christensen, Sindre Moldeklev, Andreas L. Opdahl, Kjetil J. Villanger  
Computers in Industry 123 (2020) 103321


## Abstract 要約

Journalism is challenged by digitalisation and social media, resulting in lower subscription numbers and reduced advertising income. 
**ジャーナリズムはデジタル化とソーシャルメディアによって脅かされており、その結果、購読者数が減少し、広告収入が減少**しています。 
Information and communication techniques (ICT) offer new opportunities. 
情報通信技術（ICT）は新たな機会を提供します。 
Our research group is collaborating with a software developer of news production tools for the international market to explore how social, open, and other data sources can be leveraged for journalistic purposes. 
私たちの研究グループは、国際市場向けのニュース制作ツールのソフトウェア開発者と協力し、社会的、オープン、その他のデータソースをジャーナリズムの目的でどのように活用できるかを探求しています。 
We have developed an architecture and prototype called News Hunter that uses knowledge graphs, natural-language processing (NLP), and machine learning (ML) together to support journalists. 
私たちは、知識グラフ、自然言語処理（NLP）、および機械学習（ML）を組み合わせてジャーナリストを支援する「News Hunter」と呼ばれるアーキテクチャとプロトタイプを開発しました。 
Our focus is on combining existing data sources and computation and storage techniques into a flexible architecture for news journalism. 
私たちの焦点は、既存のデータソースと計算およびストレージ技術を組み合わせて、ニュースジャーナリズムのための柔軟なアーキテクチャを構築することです。 
The paper presents News Hunter along with plans and possibilities for future work. 
この論文では、News Hunterを紹介し、今後の作業の計画と可能性について述べます。

<!-- ここまで読んだ! -->
<!-- ジャーナリズムだから、取材とかニュース記事作成とかの話なのかな?? 記者を支援するためのデータ基盤の論文みたい!! :thinking: -->

- ざっくり:
  - 本論文 = “記者を支援するためのデータ基盤”の論文!  ニュース制作の裏側に「Knowledge Graph基盤」を入れる話。

## 1. Introduction はじめに

Journalism is in crisis, but information and communication technologies (ICT) offer new opportunities. 
ジャーナリズムは危機に瀕していますが、情報通信技術（ICT）は新たな機会を提供します。
Journalists today have access to a wealth of digital information from news aggregators, social media, and open data providers in addition to traditional sources. 
今日のジャーナリストは、従来の情報源に加えて、ニュースアグリゲーター、ソーシャルメディア、オープンデータプロバイダーからの豊富なデジタル情報にアクセスできます。
Computational journalism is "the advanced application of computing, algorithms, and automation to the gathering, evaluation, composition, presentation, and distribution of news." 
計算ジャーナリズムとは、「ニュースの収集、評価、構成、提示、配信におけるコンピューティング、アルゴリズム、および自動化の高度な応用」です。
News platforms, or journalistic knowledge platforms, support computational journalism through integrated content and software components that support all stages of news production, thereby creating "a competitive advantage by enabling scale and reducing marginal costs in the gathering, production, and dissemination of their content". 
ニュースプラットフォーム、またはジャーナリスティックナレッジプラットフォームは、ニュース制作のすべての段階をサポートする統合コンテンツおよびソフトウェアコンポーネントを通じて計算ジャーナリズムを支援し、「収集、制作、配信におけるスケールを可能にし、限界コストを削減することによって競争優位性を生み出します」。

For example, journalistic knowledge platforms can use knowledge graphs and other semantic technologies to automatically harvest, analyse, enrich, organise, and prepare potentially news-related information with increasing semantic precision. 
例えば、ジャーナリスティックナレッジプラットフォームは、ナレッジグラフやその他のセマンティック技術を使用して、潜在的にニュース関連の情報を自動的に収集、分析、強化、整理、準備し、セマンティック精度を高めることができます。
They can also leverage theories and techniques from artificial intelligence and, in particular, from machine learning, and natural-language processing, to classify, label, cluster, detect events, and otherwise process journalistic information in new and meaningful ways. 
また、人工知能、特に機械学習や自然言語処理の理論や技術を活用して、ジャーナリスティック情報を新しく意義のある方法で分類、ラベル付け、クラスタリング、イベント検出、その他の処理を行うことができます。

News Hunter is an architecture and a series of proof-of-concept prototypes that: harvests potentially news-related texts and social-media messages from the net; analyses and represents them semantically in a knowledge graph; classifies, clusters, and labels them; enriches them with background information; and presents them in real time to journalists who are working on related reports or as tips about new events. 
News Hunterは、アーキテクチャと一連の概念実証プロトタイプであり、潜在的にニュース関連のテキストやソーシャルメディアメッセージをネットから収集し、それらをナレッジグラフでセマンティックに分析・表現し、分類、クラスタリング、ラベル付けを行い、背景情報で強化し、関連するレポートに取り組んでいるジャーナリストや新しいイベントに関するヒントとしてリアルタイムで提示します。
For this purpose, News Hunter combines knowledge graphs and other semantic technologies with techniques from artificial intelligence, such as machine learning, and natural-language understanding. 
この目的のために、News Hunterはナレッジグラフやその他のセマンティック技術を、機械学習や自然言語理解などの人工知能の技術と組み合わせています。

News Hunter is being developed in collaboration between a university research group and a software developer of news production tools for the international market. 
News Hunterは、大学の研究グループと国際市場向けのニュース制作ツールのソフトウェア開発者との共同で開発されています。
Our research goal is to understand whether and how topical information and communication techniques (ICTs) can be leveraged to make social, open, and other data sources more readily available for journalistic work. 
私たちの研究目標は、トピック情報および通信技術（ICT）が、社会的、オープン、その他のデータソースをジャーナリズムの作業により利用しやすくするためにどのように活用できるかを理解することです。
Our industrial goal is to develop and evaluate proof-of-concept prototypes of such a journalistic knowledge platform. 
私たちの産業目標は、そのようなジャーナリスティックナレッジプラットフォームの概念実証プロトタイプを開発し、評価することです。
These two goals mutually reinforce one another, because work on the research goal supplies theories and ideas for development, whereas work on the industrial goal returns working prototypes and evaluations of the research. 
これら二つの目標は相互に強化し合います。なぜなら、研究目標に関する作業は開発のための理論やアイデアを提供し、一方で産業目標に関する作業は研究の実働プロトタイプと評価をもたらすからです。

The paper starts with the following research question: how can existing heterogeneous data sources and processing and storage techniques be combined to support news journalism? 
本論文は、次の研究課題から始まります：既存の異種データソースと処理およびストレージ技術をどのように組み合わせてニュースジャーナリズムを支援できるか？
We first review the most similar existing systems described in the literature. 
まず、文献で説明されている最も類似した既存のシステムをレビューします。
We then outline our research and development approach, before we present and evaluate the News Hunter architecture along with its proof-of-concept prototype and components. 
次に、私たちの研究と開発アプローチを概説し、その後、News Hunterのアーキテクチャとその概念実証プロトタイプおよびコンポーネントを提示し、評価します。
We also compare News Hunter with the existing systems and discuss future plans and possibilities. 
また、News Hunterを既存のシステムと比較し、今後の計画や可能性について議論します。



## 2. Background 背景

Neptuno is an early semantic newspaper archive system that aims to give archivists and reporters more expressive ways to describe and annotate news materials and to give reporters and readers better search and browsing capabilities.  
Neptunoは、アーカイビストと報道者にニュース資料を記述し注釈を付けるためのより表現力豊かな方法を提供し、報道者と読者により良い検索およびブラウジング機能を提供することを目的とした初期のセマンティック新聞アーカイブシステムです。

It uses an ontology for classifying archive content along with modules for semantic search, browsing and visualisation of content, but is limited to organising and disseminating already published news.  
それは、アーカイブコンテンツを分類するためのオントロジーと、セマンティック検索、ブラウジング、コンテンツの視覚化のためのモジュールを使用していますが、既に公開されたニュースの整理と配信に制限されています。

News Engine Web Services (NEWS) is another early example of a journalistic knowledge platform, which uses natural-language processing (NLP) techniques in combination with a domain-specific ontology to annotate news reports and photography descriptions precisely in order to streamline news retrieval, production, and dissemination.  
News Engine Web Services (NEWS)は、ジャーナリズム知識プラットフォームの別の初期の例であり、自然言語処理（NLP）技術をドメイン特化型オントロジーと組み合わせて使用し、ニュースレポートや写真の説明に正確に注釈を付けて、ニュースの取得、制作、配信を効率化します。

In contrast to our platform, NEWS is limited to semantic annotation of existing news items.  
私たちのプラットフォームとは対照的に、NEWSは既存のニュースアイテムのセマンティック注釈に制限されています。

It represents metadata as RDFS and uses concepts from SUMO/MILO, but does not build a knowledge graph for detecting and representing news events.  
それはメタデータをRDFSとして表現し、SUMO/MILOの概念を使用していますが、ニュースイベントを検出し表現するための知識グラフを構築していません。

Global Database of Events, Language, and Tone (GDELT) is a project and a live web service that monitors the world's news media in over 100 languages and provides a real-time open data global graph of news items and events that is updated every 15 min.  
Global Database of Events, Language, and Tone (GDELT)は、100以上の言語で世界のニュースメディアを監視し、15分ごとに更新されるニュースアイテムとイベントのリアルタイムオープンデータグローバルグラフを提供するプロジェクトおよびライブウェブサービスです。

GDELT uses newspaper texts and TV and radio news as input, and aims to increasingly analyse social-media sources as well.  
GDELTは、新聞のテキストやテレビおよびラジオのニュースを入力として使用し、ソーシャルメディアのソースもますます分析することを目指しています。

The data are provided in tables that can be transformed into a graph, but not all the data are disambiguated with IRIs that point into the LOD cloud.  
データはグラフに変換可能なテーブルで提供されますが、すべてのデータがLODクラウドを指すIRIで明確化されているわけではありません。

Also, GDELT's primary focus is on conflicts, not general news, and it represents events as actor1-action-actor2 triplets that are more fine-grained than news events.  
また、GDELTの主な焦点は一般ニュースではなく紛争にあり、ニュースイベントよりも詳細なactor1-action-actor2トリプレットとしてイベントを表現します。

EventRegistry is a live web site that continuously harvests news items from RSS feeds in many languages; uses named-entity recognition and wikification to represent the items as RDF in a knowledge graph; and groups the items according to event (a significant happening reported several times).  
EventRegistryは、さまざまな言語のRSSフィードからニュースアイテムを継続的に収集するライブウェブサイトであり、名前付きエンティティ認識とウィキ化を使用してアイテムを知識グラフ内のRDFとして表現し、イベント（何度も報告された重要な出来事）に基づいてアイテムをグループ化します。

Each group is then categorised according to the DMOZ taxonomy; linked to related information about locations, involved people, and organisations; and used to track events and trending topics in real time.  
各グループはDMOZ分類法に従って分類され、場所、関与した人々、組織に関する関連情報にリンクされ、リアルタイムでイベントやトレンドトピックを追跡するために使用されます。

In contrast to News Hunter, EventRegistry only monitors events that are already reported in RSS streams and, although it uses RDF, linking is limited to Wikipedia articles and DMOZ categories.  
News Hunterとは対照的に、EventRegistryはRSSストリームで既に報告されているイベントのみを監視し、RDFを使用していますが、リンクはWikipediaの記事とDMOZカテゴリに制限されています。

NewsReader analyses web-news texts written in four different languages semantically and enriches them with information from general and linguistic reference knowledge bases in order to build event-centric knowledge graphs (ECKG).  
NewsReaderは、4つの異なる言語で書かれたウェブニューステキストをセマンティックに分析し、一般的および言語的な参照知識ベースからの情報でそれらを豊かにし、イベント中心の知識グラフ（ECKG）を構築します。

ECKGs are defined by an OWL ontology and describe events in terms of what has happened, who was involved, and where and when it took place.  
ECKGはOWLオントロジーによって定義され、何が起こったのか、誰が関与したのか、どこでいつ起こったのかという観点からイベントを説明します。

Like EventRegistry, NewsReader differs from our platform by only considering published news reports.  
EventRegistryと同様に、NewsReaderは公開されたニュースレポートのみを考慮することで私たちのプラットフォームとは異なります。

Reuters' Tracer harvests and analyses tweets in real time to detect new events and trending topics.  
ReutersのTracerは、リアルタイムでツイートを収集および分析し、新しいイベントやトレンドトピックを検出します。

Tracer can thereby detect newsworthy events several minutes before they are reported by news media.  
これにより、Tracerはニュースメディアによって報告される数分前にニュース価値のあるイベントを検出できます。

However, Reuters Tracer does not represent messages and news events semantically in knowledge graphs.  
しかし、Reuters Tracerはメッセージやニュースイベントを知識グラフ内でセマンティックに表現していません。

It is limited to harvesting tweets and thus focusses on fine-grained events.  
それはツイートを収集することに制限されており、したがって詳細なイベントに焦点を当てています。

Scalable Understanding of Multilingual MediA (SUMMA) records, transcribes, and translates multimedia news items in six languages, driven by the need to support data journalism in organisations like BBC and Deutsche Welle (DW).  
Scalable Understanding of Multilingual MediA (SUMMA)は、BBCやDeutsche Welle (DW)のような組織でデータジャーナリズムを支援する必要性に駆動され、6つの言語でマルチメディアニュースアイテムを記録、転写、翻訳します。

It then employs NLP and ML techniques to extract named entities, events, and topics and to summarise emerging news clusters.  
その後、NLPおよびML技術を使用して名前付きエンティティ、イベント、トピックを抽出し、新たに出現するニュースクラスターを要約します。

Like GDELT, SUMMA deals with multimedia news.  
GDELTと同様に、SUMMAはマルチメディアニュースを扱います。

It represents metadata as RDFS and uses labels defined in SUMO/MILO, but does not link externally to the LOD cloud nor build a knowledge graph for detecting and representing news events.  
それはメタデータをRDFSとして表現し、SUMO/MILOで定義されたラベルを使用していますが、LODクラウドに外部リンクを作成せず、ニュースイベントを検出し表現するための知識グラフを構築していません。

Also unlike our platform, it focusses on organising and summarising already reported news, rather than on detecting new events.  
私たちのプラットフォームとは異なり、既に報告されたニュースの整理と要約に焦点を当てており、新しいイベントの検出には焦点を当てていません。

Acquisition de Schémas pour la Reconnaissance et l'Annotation d'Événements Liés (ASRAEL) harvests English and French news texts; annotates them semantically with items and statements from Wikidata; and links them to Wikidata events using IPTC's rNews vocabulary for metadata annotation.  
Acquisition de Schémas pour la Reconnaissance et l'Annotation d'Événements Liés (ASRAEL)は、英語とフランス語のニューステキストを収集し、Wikidataからのアイテムやステートメントでセマンティックに注釈を付け、IPTCのrNews語彙を使用してWikidataイベントにリンクします。

The resulting knowledge graph can be queried using SPARQL.  
結果として得られる知識グラフはSPARQLを使用してクエリできます。

Unlike our platform, the focus is on contextualising and enriching existing news items and ASRAEL can only identify events that have already been represented in Wikidata.  
私たちのプラットフォームとは異なり、ASRAELは既存のニュースアイテムを文脈化し豊かにすることに焦点を当てており、Wikidataに既に表現されているイベントのみを特定できます。

Each existing system demonstrates new information services that can be highly useful for journalists and in newsrooms, but none of them yet combine the full strength of externally linked knowledge graphs and ontologies to harvest both pre-news messages from social media and already published news reports.  
既存の各システムは、ジャーナリストやニュースルームに非常に役立つ新しい情報サービスを示していますが、いずれもまだ外部リンクされた知識グラフとオントロジーの完全な力を組み合わせて、ソーシャルメディアからのプレニュースメッセージと既に公開されたニュースレポートの両方を収集することはできていません。

Dealing with both pre- and post-news information in the same platform would improve support for central tasks, such as identifying which social-media events that are really pre news and following up how unfolding news events spread and perhaps develop further in social media.  
プレニュース情報とポストニュース情報の両方を同じプラットフォームで扱うことは、実際にプレニュースであるソーシャルメディアイベントを特定し、展開中のニュースイベントがどのように広がり、ソーシャルメディアでさらに発展するかを追跡するなどの中心的なタスクへのサポートを改善します。

Also, the literature on existing systems does little to address architecture for journalistic knowledge platforms and, when it is mentioned at all, it is limited to simpler processing pipelines.  
また、既存のシステムに関する文献は、ジャーナリズム知識プラットフォームのアーキテクチャにほとんど触れておらず、言及されている場合でも、より単純な処理パイプラインに制限されています。

In light of this, we sharpen our starting research question as follows: how can pre-and post-news data sources and processing and storage techniques be combined into a flexible architecture for news journalism?  
このような背景を踏まえ、私たちは出発点となる研究課題を次のように明確化します：プレニュースおよびポストニュースデータソースと処理およびストレージ技術をどのように組み合わせて、ニュースジャーナリズムのための柔軟なアーキテクチャを構築できるか？

In the following sections, we will explain how our News Hunter architecture and prototype contribute to filling this gap and to advance research on journalistic knowledge platforms.  
次のセクションでは、私たちのNews Hunterアーキテクチャとプロトタイプがこのギャップを埋め、ジャーナリズム知識プラットフォームに関する研究を進めるのにどのように貢献するかを説明します。



## 3. Research approach 研究アプローチ  
### 3.1. Collaborators 協力者  
Wolftech Broadcast Solutions is a software company that develops integrated news systems for making live news production simpler and more efficient.  
Wolftech Broadcast Solutionsは、ライブニュース制作をより簡単かつ効率的にするための統合ニュースシステムを開発するソフトウェア会社です。  
Wolftech News is their system for effective news production with current focus on television news.  
Wolftech Newsは、テレビニュースに現在焦点を当てた効果的なニュース制作のためのシステムです。  
It aims to help journalists and other newsroom workers collaborate effectively and efficiently on creating, managing, and publishing media to a variety of platforms.  
このシステムは、ジャーナリストや他のニュースルームのスタッフが、さまざまなプラットフォームにメディアを作成、管理、公開する際に、効果的かつ効率的に協力できるよう支援することを目的としています。  
It supports and improves the workflows in a newsroom by integrating mobile solutions for fieldwork with central systems for news monitoring, resource management, news editing, and multi-platform publishing (on live and internet TV, web, social media, etc.).  
このシステムは、現場作業のためのモバイルソリューションと、ニュース監視、リソース管理、ニュース編集、マルチプラットフォーム出版（ライブおよびインターネットテレビ、ウェブ、ソーシャルメディアなど）のための中央システムを統合することによって、ニュースルームのワークフローをサポートし、改善します。  
The group for Intelligent Information Systems (I2S) at the University of Bergen studies information systems (IS) that employ artificial intelligence (AI) related techniques, such as knowledge graphs, machine learning, and natural-language understanding.  
ベルゲン大学のインテリジェント情報システム（I2S）グループは、知識グラフ、機械学習、自然言語理解などの人工知能（AI）関連技術を用いた情報システム（IS）を研究しています。  
News Hunter is a collaboration between Wolftech and I2S that aims to extend Wolftech News to harvest, organise and leverage social media streams and other big-data sources for journalistic and newsroom purposes, using topical ICTs such as knowledge graphs, machine learning, and natural-language processing.  
News Hunterは、WolftechとI2Sの共同プロジェクトであり、知識グラフ、機械学習、自然言語処理などのトピカルICTを使用して、Wolftech Newsを拡張し、ジャーナリズムやニュースルームの目的のためにソーシャルメディアストリームや他のビッグデータソースを収集、整理、活用することを目指しています。  
### 3.2. Method 方法  
Because our research involves explorative technology development, we have organised and reported it as design science, where the aim is to advance theory and improve practice on journalistic knowledge platforms by incrementally developing and evaluating two research artefacts: an architecture (a high-level structure of system components) and a prototype that instantiates the architecture as a proof-of-concept.  
私たちの研究は探求的な技術開発を含むため、デザインサイエンスとして整理し報告しています。ここでの目的は、ジャーナリズム知識プラットフォームにおける理論を進展させ、実践を改善することです。これを実現するために、アーキテクチャ（システムコンポーネントの高レベル構造）と、アーキテクチャを概念実証として具現化するプロトタイプの2つの研究アーティファクトを段階的に開発し評価しています。  
Following Hevner's three-cycle model of design-science research, we synchronise research and development iterations in continuous dialogue with Wolftech, in order to get feedback on results and ideas for new features.  
Hevnerのデザインサイエンス研究の三サイクルモデルに従い、Wolftechとの継続的な対話の中で研究と開発の反復を同期させ、結果に対するフィードバックや新機能のアイデアを得るようにしています。  
For each iteration, we attempt to define clear goals for both research and development, based on an explicit development process that involve selected tools and technologies and where each step produces well-defined and verifiable results.  
各反復において、選択されたツールと技術を含む明示的な開発プロセスに基づいて、研究と開発の両方に対して明確な目標を定義しようとします。そして、各ステップは明確に定義され、検証可能な結果を生み出します。  
We seek short, XP-like iterations, typically of 1–3 weeks' length, inspired by the minimum viable product (MVP) idea: build the minimum number of features that is required for the platform to work as intended, and then evolve from there.  
私たちは、通常1〜3週間の短いXPスタイルの反復を求めており、これは最小限の実用的製品（MVP）のアイデアに触発されています：プラットフォームが意図した通りに機能するために必要な最小限の機能を構築し、そこから進化させます。  
We align with technologies that Wolftech already use in their development and runtime environments.  
私たちは、Wolftechがすでにその開発および実行環境で使用している技術に合わせています。  
Throughout development, we use proof-of-concept evaluations after each major development iteration (typically every 1–3 weeks) along with component evaluations to gauge the quality of the most central components in our architecture.  
開発全体を通じて、各主要開発反復（通常は1〜3週間ごと）の後に概念実証評価を行い、コンポーネント評価とともに、私たちのアーキテクチャの最も中心的なコンポーネントの品質を測定します。  
Section 5 will present evaluations of central prototype features with human participants.  
第5節では、人間の参加者を用いた中心的なプロトタイプ機能の評価を示します。  
### 3.3. Process プロセス  
The first simple News Hunter prototype harvested posts from Facebook's public API and ran non-English posts through Google's Translate API.  
最初のシンプルなNews Hunterプロトタイプは、Facebookの公開APIから投稿を収集し、非英語の投稿をGoogleのTranslate APIを通じて処理しました。  
The English texts were then analysed using IBM's online Alchemy API (today part of the IBM cloud) to extract metadata about topics, named entities, and sentiments.  
その後、英語のテキストはIBMのオンラインAlchemy API（現在はIBMクラウドの一部）を使用して分析され、トピック、固有名詞、感情に関するメタデータを抽出しました。  
The Alchemy metadata, along with the message itself and additional metadata from Facebook's API (date, title, location, etc.), were then loaded into a graph database (triple store).  
Alchemyメタデータは、メッセージ自体およびFacebookのAPIからの追加メタデータ（日時、タイトル、場所など）とともに、グラフデータベース（トリプルストア）にロードされました。  
The first prototype was written in C# as an ASP.NET application using BrightstarDB (a graph database/triple store for the .NET platform) as triple store.  
最初のプロトタイプは、C#で書かれ、ASP.NETアプリケーションとしてBrightstarDB（.NETプラットフォーム用のグラフデータベース/トリプルストア）をトリプルストアとして使用しました。  
Having demonstrated the viability of our idea, we then started developing a more elaborate and clearly architected, second News Hunter prototype from scratch, which the rest this paper will present and discuss.  
私たちのアイデアの実現可能性を示した後、より洗練され、明確に設計された第二のNews Hunterプロトタイプをゼロから開発し始めました。このプロトタイプについては、今後の部分で紹介し議論します。  



## 4. Architecture アーキテクチャ

Fig. 1 places News Hunter in its usage context, whereas Fig. 2 shows the News Hunter architecture with access and serving relations between its components. 
図1はNews Hunterをその使用コンテキストに配置し、図2はそのコンポーネント間のアクセスと提供関係を示しています。
The prototype reported in this paper implements central functionality of all these components, although a few of them only in rudimentary form. 
本論文で報告されているプロトタイプは、これらのコンポーネントの中心的な機能を実装していますが、そのうちのいくつかは初歩的な形でのみ実装されています。
This section and the next present and discuss the overall architecture and the more developed prototype components in further detail. 
このセクションと次のセクションでは、全体のアーキテクチャと、より発展したプロトタイプコンポーネントについて詳しく説明し、議論します。

### 4.1. Harvesters ハーベスター

The harvesters continuously download potentially news-related information items (articles, messages, posts, tweets...) from relevant sources such as Facebook and Twitter, RSS feeds, and major English-, Norwegian- and Spanish-language news sites. 
ハーベスターは、FacebookやTwitter、RSSフィード、主要な英語、ノルウェー語、スペイン語のニュースサイトなどの関連ソースから、ニュース関連の情報アイテム（記事、メッセージ、投稿、ツイートなど）を継続的にダウンロードします。
The harvesters are implemented as Python scripts that use the Tweepy library to harvest Tweets, the Feedparser library for RSS, and the Newspaper library to harvest news reports. 
ハーベスターは、Tweepyライブラリを使用してツイートを収集し、Feedparserライブラリを使用してRSSを処理し、Newspaperライブラリを使用してニュースレポートを収集するPythonスクリプトとして実装されています。
The pre-processed news items are stored as JSON objects in a source database. 
前処理されたニュースアイテムは、ソースデータベースにJSONオブジェクトとして保存されます。
Defining harvesters as a separate type of component in the architecture makes it easier to add new harvesters to future version of the platform, for example to retrieve information from new information sources or to incorporate external harvesting services and components. 
アーキテクチャ内でハーベスターを別のタイプのコンポーネントとして定義することで、将来のプラットフォームのバージョンに新しいハーベスターを追加しやすくなります。たとえば、新しい情報ソースから情報を取得したり、外部のハーベスティングサービスやコンポーネントを組み込んだりすることができます。
Commercial harvesting components are already becoming available in the form of news aggregators such as datahub.io and newsapi.org. 
商業的なハーベスティングコンポーネントは、すでにdatahub.ioやnewsapi.orgなどのニュースアグリゲーターの形で利用可能になっています。
Running multiple harvester components independently in parallel also makes the platform more resilient to changed or unavailable information sources. 
複数のハーベスターコンポーネントを独立して並行して実行することで、プラットフォームは変更されたり利用できなくなった情報ソースに対してもより耐性を持つようになります。

### 4.2. Source DB ソースDB

The source database stores the original items to make the raw texts available for later retrieval and further analysis. 
ソースデータベースは、元のアイテムを保存し、生のテキストを後で取得およびさらなる分析のために利用可能にします。
The source database is implemented using Elasticsearch with a Python script that inserts harvested item texts and selected metadata. 
ソースデータベースは、Elasticsearchを使用して実装されており、収集したアイテムのテキストと選択されたメタデータを挿入するPythonスクリプトが使用されています。
The source DB also merges duplicates, which is important when multiple harvesters are run in parallel. 
ソースDBは重複をマージすることも行い、これは複数のハーベスターが並行して実行される場合に重要です。
Including a source DB as a component in the architecture makes it possible to re-analyse old news items whenever a lifter has been introduced or improved. 
アーキテクチャにソースDBをコンポーネントとして含めることで、リフターが導入または改善されるたびに古いニュースアイテムを再分析することが可能になります。
It also facilitates graded lifting, where seemingly less important items, for example from social media, can first be lifted coarsely and quickly and then re-analysed more deeply later if they turn out to be important. 
また、グレード付きリフティングを容易にし、たとえばソーシャルメディアからの重要性が低いと思われるアイテムをまず粗く迅速にリフトし、後で重要であることが判明した場合に再分析することができます。
Storing the original texts also makes them available for other NLP techniques should the need arise, and it ensures that a news item remains accessible even if it is later removed by the publisher, for example because of censorship. 
元のテキストを保存することで、必要に応じて他のNLP技術に利用できるようになり、ニュースアイテムが後に出版社によって削除された場合でも（たとえば検閲のために）アクセス可能であることが保証されます。

### 4.3. Translator 翻訳者

When necessary, the translator creates canonical-language translations of news items in the source database. 
必要に応じて、翻訳者はソースデータベース内のニュースアイテムの標準言語翻訳を作成します。
The prototype uses English as canonical language. 
プロトタイプは英語を標準言語として使用しています。
The translator relies on Microsoft's online Translate API, because the standard libraries we have explored do not support small languages like Norwegian. 
翻訳者はMicrosoftのオンラインTranslate APIに依存しています。なぜなら、私たちが調査した標準ライブラリはノルウェー語のような小さな言語をサポートしていないからです。
Including a source translator in the architecture makes it possible to use lifting techniques developed and tuned for richly-resourced languages such as English to lift news items from smaller languages for which NLP pipelines and training materials are less developed or missing completely. 
アーキテクチャにソース翻訳者を含めることで、英語のようなリソースが豊富な言語のために開発され調整されたリフティング技術を使用して、NLPパイプラインやトレーニング資料があまり発展していないか、まったく欠如している小さな言語からニュースアイテムをリフトすることが可能になります。
Storing translations of texts into the same canonical language also simplifies cross-language retrieval. 
同じ標準言語にテキストの翻訳を保存することは、クロスランゲージ検索を簡素化します。

### 4.4. Lifter and analysers リフターと分析者

The lifter runs the harvested (and perhaps translated) news items through an NLP pipeline to represent them semantically as small knowledge graphs, which can be inserted into a graph database (triple store). 
リフターは収集された（おそらく翻訳された）ニュースアイテムをNLPパイプラインに通し、それらを小さな知識グラフとして意味的に表現し、グラフデータベース（トリプルストア）に挿入できるようにします。
The analyser realises the NLP pipeline and invokes sub-components for specific tasks such as sentiment analysis, topic analysis, named-entity (NE) analysis, and classification. 
分析者はNLPパイプラインを実現し、感情分析、トピック分析、固有表現（NE）分析、分類などの特定のタスクのためにサブコンポーネントを呼び出します。
The backbone of the analyser is implemented in C#, with most of the components written in Python. 
分析者のバックボーンはC#で実装されており、ほとんどのコンポーネントはPythonで記述されています。

#### 4.4.1. Sentiment analyser 感情分析者

Sentiment analysis is implemented using the AFINN Python library. 
感情分析はAFINN Pythonライブラリを使用して実装されています。

#### 4.4.2. Topic analyser トピック分析者

Unsupervised topic extraction is implemented using a variety of tools. 
教師なしトピック抽出はさまざまなツールを使用して実装されています。
Microtexts from Twitter and Facebook, are analysed using the RAKE (Rapid Automatic Keyword Extraction) library, written in C#. 
TwitterやFacebookからのマイクロテキストは、C#で書かれたRAKE（Rapid Automatic Keyword Extraction）ライブラリを使用して分析されます。
RSS items are handled using Textacy, a wrapper library for Spacy (see below). 
RSSアイテムは、SpacyのラッパーライブラリであるTextacyを使用して処理されます（下記参照）。
Longer texts are analysed with the Python-implementation of the TextRank library, which also supports automatic topic extraction along with report summarisation. 
長いテキストは、報告要約とともに自動トピック抽出をサポートするTextRankライブラリのPython実装を使用して分析されます。
Longer texts introduce a bias because they generate more keywords, making them appear more prominent than shorter texts when querying by topic. 
長いテキストは、より多くのキーワードを生成するため、トピックでクエリを行う際に短いテキストよりも目立つように見えるため、バイアスを導入します。
The analyser therefore weighs each keyword by its position in the text (because news texts should present its most central themes in the beginning) and number of occurrences, so that infrequent and late-occurring keywords weigh less. 
したがって、分析者は各キーワードの重みをテキスト内の位置（ニューステキストは最も中心的なテーマを最初に提示すべきであるため）と出現回数によって決定し、出現頻度が低く遅れて出現するキーワードの重みを軽くします。

#### 4.4.3. Named-entity (NE) analyser 固有表現（NE）分析者

Part-of-speech (PoS) tagging and named-entity recognition (NER) uses the Python-library Spacy, whereas named-entity linking are done with DBpedia Spotlight. 
品詞（PoS）タグ付けと固有表現認識（NER）はPythonライブラリのSpacyを使用し、固有表現リンクはDBpedia Spotlightで行います。
Written in Scala, Spotlight tags named entities recognised in the text with DBpedia IRIs in order to provide more precise semantics and facilitate data enrichment with linked open data. 
Scalaで書かれたSpotlightは、テキスト内で認識された固有表現にDBpedia IRIをタグ付けし、より正確な意味を提供し、リンクされたオープンデータによるデータの強化を促進します。
Separating the lifter into a separate component makes it available both downstream for lifting harvested news items and upstream for lifting the stories-being written by journalists. 
リフターを別のコンポーネントとして分離することで、収集されたニュースアイテムをリフトするためのダウンストリームと、ジャーナリストによって書かれているストーリーをリフトするためのアップストリームの両方で利用可能になります。
A clearly defined lifting API might also make it easier to incorporate external lifting tools and services seamlessly into the platform, such as those provided by FRED and PIKES. 
明確に定義されたリフティングAPIは、FREDやPIKESが提供するような外部リフティングツールやサービスをプラットフォームにシームレスに組み込むのを容易にするかもしれません。
Furthermore, the lifting component can hide complexity, for example opaquely using different NLP pipelines for different types of news items or using an ensemble of different analysers for the same item, and it makes it easier to add new or improved analysers. 
さらに、リフティングコンポーネントは複雑さを隠すことができ、たとえば異なるタイプのニュースアイテムに対して異なるNLPパイプラインを不透明に使用したり、同じアイテムに対して異なる分析者のアンサンブルを使用したりすることができ、新しいまたは改善された分析者を追加しやすくします。

### 4.5. Graph DB グラフDB

The graph database (or triple store) combines the resulting semantic representations of news items into a persistent, contiguous journalistic knowledge graph, or news graph. 
グラフデータベース（またはトリプルストア）は、ニュースアイテムの結果として得られた意味的表現を永続的で連続的なジャーナリズム知識グラフ、またはニュースグラフに統合します。
It also stores the titles and first paragraphs of each news item in its original language and canonical translation. 
また、各ニュースアイテムのタイトルと最初の段落を元の言語と標準翻訳で保存します。
The graph database is implemented as a BrightstarDB triple store, which is a DBMS specifically for RDF graphs. 
グラフデータベースは、RDFグラフ専用のDBMSであるBrightstarDBトリプルストアとして実装されています。
To upload and query data, we use the Microsoft Entity Framework along with LINQ (Language Integrated Query), a .NET component for C#-native data querying of domain-specific models that automatically translates datatype-specific queries to SPARQL for processing by BrightstarDB. 
データをアップロードおよびクエリするために、Microsoft Entity FrameworkとLINQ（言語統合クエリ）を使用します。これは、ドメイン固有モデルのC#ネイティブデータクエリ用の.NETコンポーネントで、データ型特有のクエリを自動的にSPARQLに変換してBrightstarDBで処理します。
The graph database is a central component in the architecture because it is the output target and input source for several other components. 
グラフデータベースは、他のいくつかのコンポーネントの出力ターゲットおよび入力ソースであるため、アーキテクチャの中心的なコンポーネントです。
Most importantly, it stores the output from the lifter and it provides the information needed by the retriever and thus, indirectly, by the front end in Fig. 2. 
最も重要なのは、リフターからの出力を保存し、リトリーバーが必要とする情報を提供し、したがって、間接的に図2のフロントエンドに情報を提供することです。
In addition, it is continuously monitored by the enricher, event detector and social networker components, which thereby become decoupled from one another and from the other components. 
さらに、エンリッチャー、イベント検出器、ソーシャルネットワーカーコンポーネントによって継続的に監視され、これによりそれぞれが他のコンポーネントから分離されます。
Defining a single interface to the triple store also ensures scalability as the knowledge graph grows, because the data can be split thematically, chronologically, regionally, or otherwise into several more manageable knowledge graphs without changing other components. 
トリプルストアへの単一のインターフェースを定義することは、知識グラフが成長するにつれてスケーラビリティを確保します。なぜなら、データはテーマ別、時間的、地域的、またはその他の方法で、他のコンポーネントを変更することなく、より管理しやすい複数の知識グラフに分割できるからです。

### 4.6. Ontology オントロジー

The ontology describes how lifted news items are represented semantically. 
オントロジーは、リフトされたニュースアイテムがどのように意味的に表現されるかを説明します。
A clearly defined ontology is crucial to support the graph database as the central knowledge repository in the architecture. 
明確に定義されたオントロジーは、アーキテクチャ内の中央知識リポジトリとしてグラフデータベースをサポートするために重要です。
It must therefore define all the classes and properties necessary for representing the output of the lifter, as well as the classes and properties needed by the retriever and thus, indirectly, by the front end. 
したがって、リフターの出力を表現するために必要なすべてのクラスとプロパティ、およびリトリーバーが必要とするクラスとプロパティ（したがって、間接的にフロントエンドが必要とするもの）を定義する必要があります。
As shown in Fig. 3, Items are potentially news-relevant harvested items, with Item Types such as news article, report-in-writing, RSS item, blog post, and microtext (Facebook message or tweet). 
図3に示すように、アイテムは潜在的にニュース関連の収集アイテムであり、アイテムタイプにはニュース記事、執筆中のレポート、RSSアイテム、ブログ投稿、マイクロテキスト（Facebookメッセージまたはツイート）があります。
Descriptors represent the semantic contents of items, with relations to namedEntities, topics, locations, and sentiments that are mentioned or expressed in the text. 
記述子はアイテムの意味的内容を表し、テキスト内で言及または表現されるnamedEntities、トピック、場所、感情との関係を持ちます。
Topics and named entities (such as people, organisations, and places) are EnrichableResources with a unique IRI, meaning that they can easily be enriched with additional triples available in the LOD cloud from sources such as DBpedia. 
トピックと固有表現（人、組織、場所など）は、ユニークなIRIを持つEnrichableResourcesであり、DBpediaなどのソースから利用可能な追加のトリプルで簡単に強化できます。
The ontology has been explicitly defined using the Web Ontology Language (OWL), making the graph database interface more clearly defined and making it easier to enrich the knowledge graph with linked-open data from other ontologies. 
オントロジーはWeb Ontology Language（OWL）を使用して明示的に定義されており、グラフデータベースインターフェースがより明確に定義され、他のオントロジーからのリンクされたオープンデータで知識グラフを強化しやすくなります。
It also facilitates automated reasoning to ensure that the ontology remains consistent. 
また、オントロジーが一貫性を保つことを保証するために自動推論を促進します。
Because the ontology follows good linked-open data practices, such as reusing and interlinking terms from existing ontologies, it can easily be extended with terms from other popular ontologies, for example to represent the source IRIs and creation dates of items, social relations between persons, and semantic relations between topics. 
オントロジーは、既存のオントロジーからの用語の再利用や相互リンクなどの良好なリンクオープンデータの慣行に従っているため、他の人気のあるオントロジーからの用語で簡単に拡張できます。たとえば、アイテムのソースIRIや作成日、人物間の社会的関係、トピック間の意味的関係を表現するために拡張できます。

### 4.7. Classifiers 分類器

The classifiers organise the harvested and lifted news items further, using several NLP and ML pipelines. 
分類器は、収集されたニュースアイテムとリフトされたニュースアイテムをさらに整理し、いくつかのNLPおよびMLパイプラインを使用します。

#### 4.7.1. Single-label classifier 単一ラベル分類器

In order to provide additional entry paths into the knowledge graph, NLP and ML techniques are used to classify (label) news items. 
知識グラフへの追加のエントリパスを提供するために、NLPおよびML技術を使用してニュースアイテムを分類（ラベル付け）します。
A single-label classifier is implemented as a pipeline that uses Spacy for part-of-speech (PoS) tagging, stop-word removal, and lemmatisation. 
単一ラベル分類器は、品詞（PoS）タグ付け、ストップワードの削除、レマタイゼーションにSpacyを使用するパイプラインとして実装されています。
scikit-learn is then used to create a term-document matrix and for feature selection, assigning higher weights to potentially important words in a text using TF-IDF. 
次に、scikit-learnを使用して用語-文書行列を作成し、特徴選択を行い、TF-IDFを使用してテキスト内の潜在的に重要な単語に高い重みを割り当てます。
The final classification step uses both a support-vector machine (SVM) implemented using scikit-learn and a multi-layer perceptron (MLP) neural network implemented using Keras. 
最終的な分類ステップでは、scikit-learnを使用して実装されたサポートベクターマシン（SVM）と、Kerasを使用して実装された多層パーセプトロン（MLP）ニューラルネットワークの両方を使用します。
Out of 2225 pre-labelled RSS items from BBC's Insight dataset, 70% were used for training and 30% held out for validation. 
BBCのInsightデータセットからの2225の事前ラベル付けされたRSSアイテムのうち、70%がトレーニングに使用され、30%が検証のために保持されました。



. Out of 2225 pre-labelled RSS items from BBC's Insight dataset, 70% were used for training and 30% held out for validation.  
BBCのInsightデータセットからの2225件の事前ラベル付けされたRSSアイテムのうち、70%がトレーニングに使用され、30%が検証のために保持されました。

#### 4.7.2. Multi-label classifier  
Multi-label classification relaxes the single-label requirement and has the potential to represent news content even more flexibly and precisely, in particular when combined with standard news taxonomies such as the IPTC Media Topics.  
マルチラベル分類は、単一ラベルの要件を緩和し、特にIPTCメディアトピックのような標準的なニュース分類法と組み合わせることで、ニュースコンテンツをさらに柔軟かつ正確に表現する可能性があります。

Multi-label classification is implemented by the same pipeline used for single-label classification.  
マルチラベル分類は、単一ラベル分類に使用されるのと同じパイプラインによって実装されます。

Out of 544,820 pre-labelled news articles from The Guardian's public API, 70% were used for training and 30% held out for validation.  
The Guardianの公開APIからの544,820件の事前ラベル付けされたニュース記事のうち、70%がトレーニングに使用され、30%が検証のために保持されました。

String equivalence supported by WordNet synsets were used to match the Guardian labels to IPTC news codes.  
WordNetのシンセットによってサポートされる文字列の同等性を使用して、GuardianのラベルをIPTCニュースコードに一致させました。

Similarly to the lifter component, a classification component with a clearly defined API makes it easier to incorporate external classification tools and services into the platform.  
リフターコンポーネントと同様に、明確に定義されたAPIを持つ分類コンポーネントは、外部の分類ツールやサービスをプラットフォームに組み込むのを容易にします。

Many primary and secondary news sources already label the news items they provide, sometimes even with semantically disambiguated IRIs.  
多くの一次および二次ニュースソースは、提供するニュースアイテムにラベルを付けており、時には意味的に曖昧さを解消したIRIを使用しています。

Defining single- and multi-label classifiers as sub-components inside the classifier makes it easier to run several alternative components in parallel as part of ensembles, and it makes it easier to add new or improved specific classification components.  
単一およびマルチラベル分類器を分類器内のサブコンポーネントとして定義することで、アンサンブルの一部として複数の代替コンポーネントを並行して実行し、新しいまたは改善された特定の分類コンポーネントを追加するのが容易になります。

### 4.8. Event detection  
The event detector clusters news items according to named entities, topics, and location in order to identify potentially newsworthy events.  
イベント検出器は、名前付きエンティティ、トピック、および場所に基づいてニュースアイテムをクラスタリングし、潜在的にニュース価値のあるイベントを特定します。

Multiple near-simultaneous news items related to the same entity (including places) and/or topic suggests that a potentially newsworthy event is unfolding.  
同じエンティティ（場所を含む）および/またはトピックに関連する複数のほぼ同時のニュースアイテムは、潜在的にニュース価値のあるイベントが進行中であることを示唆しています。

The event detector is implemented by clustering news items represented in the knowledge graph, selecting items from recent days and pre-processing them to calculate TF-IDFs.  
イベント検出器は、知識グラフに表現されたニュースアイテムをクラスタリングし、最近の日付のアイテムを選択してTF-IDFを計算するために前処理することによって実装されます。

Scikit-learn's DBSCAN algorithm is then used for clustering, because it offers scalability and focus on neighbourhood size at the expense of uneven cluster sizes.  
次に、Scikit-learnのDBSCANアルゴリズムがクラスタリングに使用されます。これは、スケーラビリティを提供し、均一でないクラスタサイズの代償として近隣サイズに焦点を当てるからです。

Defining event detection as a separate component type makes it possible to develop specialised event detectors running in parallel for different event types and makes it easier to introduce new detectors without changing other components.  
イベント検出を別のコンポーネントタイプとして定義することで、異なるイベントタイプのために並行して動作する専門のイベント検出器を開発することが可能になり、他のコンポーネントを変更することなく新しい検出器を導入するのが容易になります。

### 4.9. Enricher  
Enrichers augment the knowledge graph by inserting related information from external data sources.  
エンリッチャーは、外部データソースから関連情報を挿入することによって知識グラフを拡張します。

An example enricher component is implemented using pre-written SPARQL queries that use IRIs returned by DBpedia Spotlight to retrieve related background information on demand from the live DBpedia endpoint.  
例として、DBpedia Spotlightから返されたIRIを使用して、ライブDBpediaエンドポイントから関連する背景情報をオンデマンドで取得する事前に書かれたSPARQLクエリを使用してエンリッチャーコンポーネントが実装されています。

Another example enricher is implemented using the Twitter API to retrieve tweets on demand from athletes represented in the knowledge graph.  
別の例として、知識グラフに表現されたアスリートからオンデマンドでツイートを取得するためにTwitter APIを使用してエンリッチャーが実装されています。

The front end can also retrieve additional background information on demand from social, open, and other data sources on the web.  
フロントエンドは、ソーシャル、オープン、その他のウェブ上のデータソースからオンデマンドで追加の背景情報を取得することもできます。

Separating out the enricher as a separate type of component avoids redundancy, because specific enrichment tasks such as adding external LOD data about, for example, athletes is carried out in a single place in the architecture, instead of being replicated across several different components that all somehow deal with athletes.  
エンリッチャーを別のタイプのコンポーネントとして分離することで冗長性を回避します。たとえば、アスリートに関する外部LODデータを追加するような特定のエンリッチメントタスクは、アーキテクチャ内の単一の場所で実行され、アスリートに関連する複数の異なるコンポーネントに複製されることはありません。

Instead of adding different types of information about athletes for different purposes in several different components, possibly creating both factual inconsistencies and terminology conflicts, all athlete information is thereby added in a coordinated manner by a single enricher component that can collaborate with other enrichers, such as a more general person-information enricher.  
異なる目的のために複数の異なるコンポーネントにアスリートに関する異なるタイプの情報を追加する代わりに、事実の不一致や用語の対立を生じさせる可能性があるため、すべてのアスリート情報は、より一般的な人情報エンリッチャーなどの他のエンリッチャーと協力できる単一のエンリッチャーコンポーネントによって調整された方法で追加されます。

These enrichers can work independently of the lifters and other components, continuously scanning the input queues to the knowledge graph for new resources to enrich.  
これらのエンリッチャーは、リフターや他のコンポーネントとは独立して動作し、知識グラフへの新しいリソースをエンリッチするために入力キューを継続的にスキャンします。

### 4.10. Social networking  
The social networker conducts affinity analysis to identify whether people in the knowledge graph are on friendly terms or not, a useful feature for journalists when selecting informants and planning interviews.  
ソーシャルネットワーカーは、知識グラフ内の人々が友好的な関係にあるかどうかを特定するために親和性分析を行います。これは、情報提供者を選択し、インタビューを計画する際にジャーナリストにとって有用な機能です。

Who-knows-who graphs help journalists prepare for interviews outside their usual areas, for example to avoid saying something wrong to the subjects.  
誰が誰を知っているかのグラフは、ジャーナリストが通常の領域外でのインタビューの準備をするのに役立ち、たとえば、被取材者に対して間違ったことを言わないようにします。

News Hunter also supports invitation of interview objects, giving journalists and other newsroom workers a standard form for creating invitations and saving invitations in the knowledge graph so they can be revised and reused in the future.  
News Hunterは、インタビュー対象者の招待もサポートしており、ジャーナリストや他のニュースルームの作業者に招待状を作成するための標準フォームを提供し、招待状を知識グラフに保存して将来修正および再利用できるようにします。

Similarly to the enricher, defining a specific social-networking component in the architecture makes it easier to incorporate existing social and other network analysis tools and services in the platform, and it avoids redundancy because all network analysis are carried out in a single place.  
エンリッチャーと同様に、アーキテクチャ内に特定のソーシャルネットワーキングコンポーネントを定義することで、プラットフォームに既存のソーシャルおよびその他のネットワーク分析ツールやサービスを組み込むのが容易になり、すべてのネットワーク分析が単一の場所で実行されるため冗長性を回避します。

### 4.11. Report editor  
The report editor lets the journalist type in a report which is analysed in real time.  
レポートエディタは、ジャーナリストがレポートを入力し、それがリアルタイムで分析されることを可能にします。

The report editor is implemented as a Froala WYSIWYG-editor plug-in.  
レポートエディタは、Froala WYSIWYGエディタプラグインとして実装されています。

Whenever the journalist pauses writing, the text is sent asynchronously via the lifter to the same NLP pipeline that is used to analyse harvested news items.  
ジャーナリストが執筆を一時停止するたびに、テキストは非同期的にリフターを介して収集されたニュースアイテムを分析するために使用される同じNLPパイプラインに送信されます。

This has several benefits.  
これにはいくつかの利点があります。

The journalist gets instant feedback on the sentiment of their writing and under which category they should save and publish their reports.  
ジャーナリストは、自分の執筆の感情に関する即時のフィードバックを受け取り、レポートを保存および公開すべきカテゴリを知ることができます。

Other journalists in the same organisation that are working on similar new items can be identified to foster collaboration and avoid duplicate work.  
同じ組織内で類似のニュースアイテムに取り組んでいる他のジャーナリストを特定することで、コラボレーションを促進し、重複作業を避けることができます。

And the knowledge graph can be queried for relevant background information to present to the journalist.  
また、知識グラフに対してジャーナリストに提示するための関連する背景情報を照会することができます。

The latter is implemented using simple algorithms based on semantic distance, so that the relevance of a harvested new item is proportional to the number of related topics and named entities, weighted by the strength of each relation.  
後者は、意味的距離に基づく単純なアルゴリズムを使用して実装されており、収集されたニュースアイテムの関連性は、関連するトピックと名前付きエンティティの数に比例し、各関係の強さによって重み付けされます。

Exact word-sense match is the strongest, followed by synonyms, hyper-/hyponyms, and then other semantic relations.  
正確な語義の一致が最も強く、次に同義語、上位語/下位語、そして他の意味的関係が続きます。

Defining the report editor as a distinct component with a clearly defined API is important because most news organisations will already have report editing tools in place, which should fit as seamlessly as possible into the News Hunter platform.  
レポートエディタを明確に定義されたAPIを持つ独立したコンポーネントとして定義することは重要です。なぜなら、ほとんどのニュース組織はすでにレポート編集ツールを持っており、それがNews Hunterプラットフォームにできるだけシームレスに統合されるべきだからです。

### 4.12. Front end  
The front end embeds the report editor in a working environment.  
フロントエンドは、作業環境にレポートエディタを埋め込みます。

It receives the result of semantically analysing the report-in-writing and invokes the retriever component to present similar news items and other relevant background information to the journalist.  
フロントエンドは、執筆中のレポートの意味的分析の結果を受け取り、リトリーバーコンポーネントを呼び出して、ジャーナリストに類似のニュースアイテムやその他の関連背景情報を提示します。

The report editor is implemented as an interactive HTML page as shown in Fig. 4, developed using AngularJS, HTML and CSS, Sketch, and Marvel.  
レポートエディタは、図4に示すように、AngularJS、HTML、CSS、Sketch、Marvelを使用して開発されたインタラクティブなHTMLページとして実装されています。

The user can click on the identified topics and named entities to retrieve summaries of related news items.  
ユーザーは、特定されたトピックや名前付きエンティティをクリックして、関連するニュースアイテムの要約を取得できます。

The front end also displays the most recent item cluster detected in the knowledge graph.  
フロントエンドは、知識グラフで検出された最も最近のアイテムクラスタも表示します。

The News Hunter prototype thus provides a full application stack, from the web-based GUI down to the web interfaces and persistent data storage.  
このように、News Hunterプロトタイプは、ウェブベースのGUIからウェブインターフェースおよび永続的なデータストレージまでの完全なアプリケーションスタックを提供します。

Isolating the front end as a separate component inside a well-defined API is beneficial in the same way as the report-editor component.  
フロントエンドを明確に定義されたAPI内の独立したコンポーネントとして分離することは、レポートエディタコンポーネントと同様に有益です。

Many news organisations already have newsroom tools in place with which the News Hunter front end should integrate as seamlessly as possible.  
多くのニュース組織はすでにニュースルームツールを持っており、News Hunterのフロントエンドはできるだけシームレスに統合されるべきです。

### 4.13. Microservice framework  
The microservice framework leverages REST endpoints in order to: decouple the architecture, make it more flexible, and facilitate APIs written in different languages.  
マイクロサービスフレームワークは、アーキテクチャを分離し、より柔軟にし、異なる言語で書かれたAPIを容易にするためにRESTエンドポイントを活用します。

The microservices are implemented using Flask, a framework written in and for Python, but also usable from C#.  
マイクロサービスはFlaskを使用して実装されており、FlaskはPython用に書かれたフレームワークですが、C#からも使用可能です。

A message-exchange component is an essential part of a distributed architecture such as News Hunter, and Flask is a natural light-weight starting point for a prototype.  
メッセージ交換コンポーネントは、News Hunterのような分散アーキテクチャの重要な部分であり、Flaskはプロトタイプのための自然な軽量スタートポイントです。

Using a standardised message-exchange framework makes the component interfaces clearer and prepares for introducing a more comprehensive, big-data ready message-exchange framework such as Kafka in future versions of the prototype.  
標準化されたメッセージ交換フレームワークを使用することで、コンポーネントインターフェースが明確になり、将来のプロトタイプのバージョンでKafkaのようなより包括的でビッグデータ対応のメッセージ交換フレームワークを導入する準備が整います。



## 5. Evaluation 評価

This section reviews the results of our final evaluation of the central News Hunter features with human participants.  
このセクションでは、人間の参加者を対象とした中央のNews Hunter機能の最終評価の結果をレビューします。  
In addition to the evaluations presented here, we conducted functional tests and standard performance evaluations at the end of each development iteration.  
ここで示す評価に加えて、各開発イテレーションの終了時に機能テストと標準的なパフォーマンス評価を実施しました。  

### 5.1. Procedure 手順

Six subjects participated in the final evaluation: two with background as journalists and four with background as software developers.  
最終評価には6人の被験者が参加しました：ジャーナリストとしてのバックグラウンドを持つ2人と、ソフトウェア開発者としてのバックグラウンドを持つ4人です。  
They all had experience with newsroom systems through the development of Wolftech News system, but they had not participated in developing News Hunter.  
彼らは全員、Wolftech Newsシステムの開発を通じてニュースルームシステムの経験がありましたが、News Hunterの開発には参加していませんでした。  
Their experience with the News system was beneficial because they thus understood the users' needs and were able to assess the prototype in its intended context as a component of News.  
ニュースシステムに関する彼らの経験は有益であり、ユーザーのニーズを理解し、Newsのコンポーネントとしてのプロトタイプをその意図された文脈で評価することができました。  
Our evaluation focused on identifying the relatively most and least useful News Hunter features in order to identify important paths for further work.  
私たちの評価は、相対的に最も有用なNews Hunterの機能と最も有用でない機能を特定し、さらなる作業のための重要な道筋を特定することに焦点を当てました。  
Importantly, we did not attempt to compare News Hunter to existing platforms, when the participants' connection to Wolftech might have biased their responses.  
重要なことに、参加者がWolftechに関連しているために彼らの反応が偏る可能性があるため、News Hunterを既存のプラットフォームと比較しようとはしませんでした。  

We first introduced the purpose of the evaluation briefly and demonstrated the prototype.  
まず、評価の目的を簡単に紹介し、プロトタイプをデモしました。  
The participants were then presented with three English-language news reports, each 350–400 words long, from different domains: the Reuters article "Trump gives nod to Republican tax-credit proposal on Obamacare" (389 words), the BBC article "UKIP burka ban policy 'misguided' says party's MEP" (491 words), and the CNN article "Paul Pogba: Is he worth $120 million?" (449 words).  
その後、参加者には異なるドメインからの3つの英語のニュースレポート（各350〜400語）が提示されました：Reutersの記事「Trump gives nod to Republican tax-credit proposal on Obamacare」（389語）、BBCの記事「UKIP burka ban policy 'misguided' says party's MEP」（491語）、CNNの記事「Paul Pogba: Is he worth $120 million?」（449語）です。  
The participants were instructed to read the news reports and explore the following six features of News Hunter in order: inspecting published news reports through the front end; displaying named entities for reports-in-writing; displaying topics for reports-in-writing; generating summaries of longer reports; retrieving clusters of recent reports ("top stories"); and retrieving reports related to the report-in-writing.  
参加者には、ニュースレポートを読み、次の6つのNews Hunterの機能を順番に探索するよう指示されました：フロントエンドを通じて公開されたニュースレポートを検査すること；執筆中のレポートのための固有名詞を表示すること；執筆中のレポートのためのトピックを表示すること；長いレポートの要約を生成すること；最近のレポートのクラスター（「トップストーリー」）を取得すること；および執筆中のレポートに関連するレポートを取得することです。  
For each feature, we asked three questions: what is useful about this feature?, what is missing from or is problematic with this feature?, and is the feature useful overall?  
各機能について、私たちは3つの質問をしました：この機能のどこが有用ですか？この機能には何が欠けているか、または問題がありますか？この機能は全体として有用ですか？  
In general, the respondents were positive to all the features, but they also pointed to many areas of improvement, which we now turn to discuss.  
一般的に、回答者はすべての機能に対して肯定的でしたが、改善の余地が多くあることも指摘しました。これについて今から議論します。  

### 5.2. Inspecting published news reports 公開されたニュースレポートの検査

All participants considered this feature useful for getting an overview of existing news.  
すべての参加者は、この機能が既存のニュースの概要を把握するのに有用であると考えました。  
They suggested several possible improvements: an option to skip the inspect menu to go straight to the report text; a flag indicating when a report has been updated; access to the report's update history; more prominent display of report texts compared to entities and keywords; and displaying the most relevant named entities as a word cloud.  
彼らは、検査メニューをスキップしてレポートテキストに直接移動するオプション、レポートが更新されたときに示すフラグ、レポートの更新履歴へのアクセス、エンティティやキーワードに比べてレポートテキストをより目立たせること、そして最も関連性の高い固有名詞をワードクラウドとして表示することなど、いくつかの改善案を提案しました。  

### 5.3. Displaying named entities 固有名詞の表示

We used the prototype to extract named entities and types for each report and select entities with background information available in DBpedia.  
私たちはプロトタイプを使用して、各レポートの固有名詞とそのタイプを抽出し、DBpediaで利用可能な背景情報を持つエンティティを選択しました。  
Most of the participants agreed that associating named entities with reports was useful, in particular for retrieving background information without having to leave the tool to search the web, and that the named entities provided helpful context for understanding a report.  
参加者のほとんどは、固有名詞をレポートに関連付けることが有用であると同意しました。特に、ツールを離れてウェブを検索することなく背景情報を取得できる点や、固有名詞がレポートを理解するための有益な文脈を提供する点が評価されました。  
They found that the term "Named Entities" in the user interface was confusing and suggested that entities should instead be organised according to type, such as "Person", "Organisation", "Place", or even more specifically as "Football player".  
彼らは、ユーザーインターフェースの「Named Entities」という用語が混乱を招くと感じ、エンティティは「Person」、「Organisation」、「Place」などのタイプに基づいて整理されるべきだと提案しました。さらに具体的には「Football player」とすることも考えられます。  
However, a few named entities present in the reports were not found by the tool, and the participants had issues with a few of the suggestions.  
しかし、レポートに存在するいくつかの固有名詞はツールによって見つけられず、参加者は提案のいくつかに問題を抱えていました。  
The respondents found between 73% and 89% of the entities appropriate for each report, having smaller or larger issues with 11%–27% of them.  
回答者は、各レポートに対して73%から89%のエンティティが適切であると考え、11%から27%のエンティティに対して小さな問題または大きな問題を抱えていました。  
For example, for the BBC article ("burka ban"), "Commonwealth" and "EU" had been typed as countries and the wrong election was linked.  
例えば、BBCの記事（「burka ban」）では、「Commonwealth」と「EU」が国としてタイプされ、間違った選挙がリンクされていました。  
The respondents also noted that the named-entity feature could benefit from more filtering options; from triangulating information from multiple sources; and from using verifiable sources.  
回答者はまた、固有名詞機能がより多くのフィルタリングオプション、複数のソースからの情報の三角測量、検証可能なソースの使用から利益を得る可能性があると指摘しました。  
Filtering could be done, for example, by entity relevance, by type (people, organisations, places...), and by map.  
フィルタリングは、例えばエンティティの関連性、タイプ（人、組織、場所など）、および地図によって行うことができます。  

### 5.4. Displaying topics トピックの表示

We also used the prototype to extract topics for the three reports.  
私たちはプロトタイプを使用して、3つのレポートのトピックを抽出しました。  
TextRank tended to describe topics using single keywords or shorter 2–4 word phrases, whereas RAKE suggested many longer topic phrases of 4–9 words.  
TextRankはトピックを単一のキーワードや短い2〜4語のフレーズで説明する傾向がありましたが、RAKEは4〜9語の長いトピックフレーズを多く提案しました。  
Before showing these auto-generated topics to the participants, we asked them to suggest their own suitable topics for each report.  
これらの自動生成されたトピックを参加者に示す前に、各レポートに対して彼ら自身の適切なトピックを提案するように求めました。  
We then let them assess the two topic lists from TextRank and RAKE.  
その後、TextRankとRAKEからの2つのトピックリストを評価してもらいました。  
Most participants preferred the shorter topics generated by TextRank, which were more similar to their own suggestions.  
ほとんどの参加者は、TextRankによって生成された短いトピックを好みました。これらは彼ら自身の提案により似ていました。  
But the RAKE topics were sometimes preferred, and it was pointed out that the two topic-labelling styles were useful each in their own way.  
しかし、RAKEのトピックが好まれることもあり、2つのトピックラベリングスタイルはそれぞれ独自の方法で有用であると指摘されました。  
Most participants agreed that the topics were useful for finding related content and for saving as metadata.  
ほとんどの参加者は、トピックが関連コンテンツを見つけるのに有用であり、メタデータとして保存するのに役立つと同意しました。  
The topic labels also offered a quick and easy way to find out what a report is about.  
トピックラベルは、レポートが何についてであるかを素早く簡単に知る方法も提供しました。  
Both journalists found the feature to be useful overall, but the domain experts were divided.  
両方のジャーナリストはこの機能が全体的に有用であると考えましたが、ドメインの専門家は意見が分かれました。  
They pointed out that the quality of the keywords still needed improvement, e.g., through tuning and word-sense disambiguation.  
彼らは、キーワードの質がまだ改善の余地があることを指摘しました。例えば、チューニングや語義の曖昧さの解消を通じてです。  
It should also be possible to remove bad keyword suggestions from a report.  
レポートから不適切なキーワード提案を削除することも可能であるべきです。  
In addition to keywords used in the text, higher-level topics could also be suggested.  
テキストで使用されるキーワードに加えて、より高次のトピックも提案される可能性があります。  
Although our research aim is to validate the overall News Hunter architecture, and not to optimise individual components through extensive tuning, we compared the TextRank topics quantitatively with the set of user-suggested topics.  
私たちの研究の目的は、全体的なNews Hunterアーキテクチャを検証することであり、個々のコンポーネントを広範にチューニングして最適化することではありませんが、TextRankトピックをユーザー提案トピックのセットと定量的に比較しました。  
F1 scores were low (0.4–0.5), with better recall (0.55–0.75) than precision (0.3–0.4) but, of course, these measures cannot be compared to evaluations that use established and validated gold standards.  
F1スコアは低く（0.4〜0.5）、リコール（0.55〜0.75）が精度（0.3〜0.4）よりも良好でしたが、もちろん、これらの指標は確立された検証済みのゴールドスタンダードを使用した評価と比較することはできません。  
Nevertheless, the evaluation results suggest that keyword extraction with TextRank needs improvement or at least tuning to become useful for journalistic work.  
それでも、評価結果は、TextRankによるキーワード抽出が改善または少なくともチューニングが必要であり、ジャーナリズムの作業に有用になるべきであることを示唆しています。  
We did not compare the RAKE topics quantitatively in the same way, because the longer topic phrases could not be meaningfully compared with the participants' mostly single-keyword topics.  
RAKEトピックを同じ方法で定量的に比較しなかったのは、長いトピックフレーズが参加者のほとんどが単一のキーワードトピックと意味的に比較できなかったからです。  

### 5.5. Report summaries レポートの要約

Two of the domain experts said the summaries were an effective way of gaining a quick overview of a report.  
2人のドメイン専門家は、要約がレポートの迅速な概要を得るための効果的な方法であると言いました。  
One of the journalists added that the summaries could be published already while the main report was being written.  
1人のジャーナリストは、要約はメインレポートが書かれている間にすでに公開できると付け加えました。  
However, the quality of the summaries generated by the prototype needed improvement, and several of the respondents were therefore negative to the presented version of this feature.  
しかし、プロトタイプによって生成された要約の質は改善が必要であり、したがって、いくつかの回答者はこの機能の提示されたバージョンに否定的でした。  

### 5.6. Top stories トップストーリー

The top-story feature shows clusters of recent reports that have been detected as reporting the same event.  
トップストーリー機能は、同じイベントを報告していると検出された最近のレポートのクラスターを表示します。  
The respondents found this useful for identifying multiple reports about the same event and for identifying unfolding events that need to be covered.  
回答者は、同じイベントに関する複数のレポートを特定し、報道が必要な進行中のイベントを特定するのに有用であると考えました。  
However, only named entities and keywords that apply to all the reports in a group should be displayed, and the numbers of named entities and keywords should be restricted.  
ただし、グループ内のすべてのレポートに適用される固有名詞とキーワードのみが表示されるべきであり、固有名詞とキーワードの数は制限されるべきです。  
Respondents also wanted categories and a slider to limit the time frame.  
回答者はまた、カテゴリと時間枠を制限するためのスライダーを求めました。  
Ability to search through groups, control which sources to include, and explain group membership criteria were also called for.  
グループ内を検索する能力、含めるソースを制御する能力、およびグループメンバーシップの基準を説明する能力も求められました。  
Two participants saw it as problematic to make the top-story feature too prominent, because it might drown less prominent but nevertheless important events.  
2人の参加者は、トップストーリー機能をあまりにも目立たせることが問題であると考えました。なぜなら、それが目立たないがそれでも重要なイベントを埋もれさせる可能性があるからです。  

### 5.7. Related reports 関連レポート

All the respondents appreciated the possibility to retrieve related previous news articles.  
すべての回答者は、関連する以前のニュース記事を取得する可能性を評価しました。  
One of them pointed out that the usefulness of this feature would increase with better word-sense disambiguation.  
そのうちの1人は、この機能の有用性はより良い語義の曖昧さの解消によって向上すると指摘しました。  
Some respondents would like more metadata about the previous reports, such as their date and source.  
いくつかの回答者は、以前のレポートに関する日付やソースなどのメタデータがもっと欲しいと考えました。  
Another suggested feature was being able to see if other journalists were working on similar or related reports.  
別の提案された機能は、他のジャーナリストが類似または関連するレポートに取り組んでいるかどうかを見ることができることでした。  

### 5.8. Report editor レポートエディタ

The respondents found the automatic identification of named entities and keywords in the text useful, because they could be used both as metadata and for retrieving relevant background information.  
回答者は、テキスト内の固有名詞とキーワードの自動識別が有用であると考えました。なぜなら、それらはメタデータとしても、関連する背景情報を取得するためにも使用できるからです。  
In-editor access to related news reports was also considered beneficial.  
エディタ内から関連ニュースレポートにアクセスできることも有益であると考えられました。  
The respondents missed the ability to remove unwanted named entities and keywords.  
回答者は、不要な固有名詞やキーワードを削除する能力が欠けていると感じました。  

### 5.9. Classification 分類

We also used the prototype to categorise the three reports.  
私たちはプロトタイプを使用して、3つのレポートを分類しました。  
The participants agreed that the suggested categories were correct, but too general.  
参加者は、提案されたカテゴリが正しいと同意しましたが、あまりにも一般的であると考えました。  
More precise and descriptive ones would be needed to make them useful in practice.  
実際に有用にするためには、より正確で説明的なものが必要です。  
To evaluate single-label classification more precisely, we had held out 30% of the pre-labelled RSS items from BBC's Insight dataset used for training to be used for evaluation.  
単一ラベル分類をより正確に評価するために、トレーニングに使用されたBBCのInsightデータセットから事前ラベル付けされたRSSアイテムの30%を保持し、評価に使用しました。  
Both classifiers were tuned to reach an overall F1 score of 0.89.  
両方の分類器は、全体のF1スコア0.89に達するように調整されました。  
On the nine news categories used for evaluation, they both performed excellently for sports (F1 = 0.98...0.99) but less well for education (F1 = 0.68...0.69), most likely because the training set contained fewer education articles.  
評価に使用された9つのニュースカテゴリでは、両方ともスポーツ（F1 = 0.98...0.99）に対して優れたパフォーマンスを発揮しましたが、教育（F1 = 0.68...0.69）に対してはあまり良くありませんでした。これは、トレーニングセットに教育記事が少なかったためです。  
To evaluate multi-label classification, we had also held out 30% of the pre-labelled news articles from The Guardian used for training to be used for evaluation.  
マルチラベル分類を評価するために、トレーニングに使用されたThe Guardianから事前ラベル付けされたニュース記事の30%も保持し、評価に使用しました。  
String equivalence and WordNet synsets were used to match The Guardian's labels to IPTC news codes before inspecting the matches manually.  
文字列の同等性とWordNetのシンセットを使用して、The GuardianのラベルをIPTCニュースコードに一致させ、その後手動で一致を確認しました。  
The F1 scores were 0.84 for the Scikit-learn SVM and 0.72 for the Keras MLP.  
F1スコアは、Scikit-learn SVMで0.84、Keras MLPで0.72でした。  

### 5.10. Event detection イベント検出

To evaluate event detection, we analysed 1292 news reports harvested by our prototype from a variety of newspapers.  
イベント検出を評価するために、私たちはプロトタイプによってさまざまな新聞から収集された1292のニュースレポートを分析しました。  
We compared the resulting clusters with the top stories listed in Google News.  
私たちは、得られたクラスターをGoogle Newsにリストされたトップストーリーと比較しました。  
Two out of the six identified clusters were deemed correct after manual inspection, and the four remaining ones were also among the top events in Google News.  
6つの特定されたクラスターのうち2つは手動検査の後に正しいと見なされ、残りの4つもGoogle Newsのトップイベントの中にありました。  



## 6. Discussion 議論  
### 6.1. Research question 研究課題  
The paper has presented an architecture for and a prototype of a journalistic knowledge platform.  
本論文では、ジャーナリスティックな知識プラットフォームのアーキテクチャとプロトタイプを提示しました。  
The platform is able to harvest data from both pre-news and post-news data sources, exemplified by Twitter, RSS, and online newspapers.  
このプラットフォームは、Twitter、RSS、オンライン新聞などの事前ニュースおよび事後ニュースデータソースからデータを収集することができます。  
It combines the full strength of externally linked knowledge graphs and ontologies with topical AI techniques for natural-language processing and machine learning.  
外部リンクされた知識グラフとオントロジーの完全な強みを、自然言語処理および機械学習のトピカルAI技術と組み合わせています。  
It has been designed to be able evolve and grow, using decoupled components and subcomponents that exchange information and services through a microservice framework and a central knowledge graph.  
それは、マイクロサービスフレームワークと中央知識グラフを通じて情報とサービスを交換する分離されたコンポーネントとサブコンポーネントを使用して進化し成長できるように設計されています。  
The evaluation with domain experts suggest that they found the platform potentially useful.  
ドメイン専門家との評価は、彼らがこのプラットフォームを潜在的に有用であると考えたことを示唆しています。  
The paper thereby answers our research question positively.  
したがって、本論文は私たちの研究課題に対して肯定的に回答しています。  

### 6.2. Design goals 設計目標  
The News Hunter architecture and prototype satisfy central design goals we have established in collaboration with our industrial partner.  
News Hunterのアーキテクチャとプロトタイプは、私たちが産業パートナーと協力して確立した中心的な設計目標を満たしています。  
It makes state-of-the-art techniques for semantic analysis of natural-language texts and for managing and enriching knowledge graphs available to journalists embedded in their newsroom environment.  
自然言語テキストの意味解析および知識グラフの管理と強化のための最先端技術を、ニュースルーム環境に埋め込まれたジャーナリストに提供します。  
It is designed to support live harvesting of potentially news-relevant items from the net and for real-time analysis of these items and of news reports that journalists are working on.  
ネットからの潜在的にニュース関連のアイテムのライブ収集と、ジャーナリストが作業しているこれらのアイテムおよびニュース報告のリアルタイム分析をサポートするように設計されています。  
It offers both push and pull provision of information to journalists, although the latter is currently more developed.  
ジャーナリストに対して情報のプッシュとプルの両方を提供しますが、後者は現在より発展しています。  
It accepts multi-language input through the use of translators, and it is language neutral through its use of language-agnostic IRIs to represent entities and concepts that can have multiple language-tagged labels to describe their names.  
翻訳者を使用して多言語入力を受け入れ、複数の言語タグ付きラベルで名前を説明できるエンティティと概念を表すために言語に依存しないIRIを使用することで、言語中立です。  

### 6.3. Novelty 新規性  
The background section has presented the most similar existing systems described in the literature, showing that each one demonstrates information services that are potentially highly useful for journalists and newsrooms.  
背景セクションでは、文献で説明されている最も類似した既存のシステムを提示し、それぞれがジャーナリストやニュースルームにとって非常に有用である可能性のある情報サービスを示していることを示しています。  
However, only NewsReader uses the full strength of externally linked knowledge graphs defined by an OWL ontology, and only Reuters Tracer harvests social media in order to detect events that are not yet reported in the news.  
しかし、NewsReaderのみがOWLオントロジーによって定義された外部リンクされた知識グラフの完全な強みを利用し、Reuters Tracerのみがソーシャルメディアを収集して、まだニュースで報告されていないイベントを検出します。  
The other systems focus on textual and other news reports that have already been published and do not fully leverage knowledge graphs, ontologies, and linked open data.  
他のシステムは、すでに公開されたテキストおよびその他のニュース報告に焦点を当てており、知識グラフ、オントロジー、およびリンクされたオープンデータを十分に活用していません。  
Hence, News Hunter stands out by leveraging both pre-news (such and Twitter and Facebook) and post-news (such as RSS and web news) information sources in combination with a central knowledge graph.  
したがって、News Hunterは、中央知識グラフと組み合わせて、事前ニュース（TwitterやFacebookなど）および事後ニュース（RSSやウェブニュースなど）の情報源の両方を活用することで際立っています。  
It is unique in combining the following features: It targets journalists and newsrooms specifically.  
以下の機能を組み合わせる点でユニークです：特にジャーナリストとニュースルームを対象としています。  
It uses knowledge graphs centrally to integrate, organise, and analyse information for journalistic and newsroom use.  
ジャーナリスティックおよびニュースルームの使用のために情報を統合、整理、分析するために知識グラフを中心に使用します。  
It harvests, lifts, and ingests news items from multiple sources, both pre-news and post-news.  
事前ニュースと事後ニュースの両方から複数のソースからニュースアイテムを収集、抽出、取り込むことができます。  
And it enriches the knowledge graph with facts taken from the linked open data (LOD) cloud.  
さらに、リンクされたオープンデータ（LOD）クラウドから取得した事実で知識グラフを強化します。  
To the best of our knowledge, News Hunter is the only platform that combines all these features.  
私たちの知る限り、News Hunterはこれらすべての機能を組み合わせた唯一のプラットフォームです。  
Yet, the most important novelty of the present paper may be that it, for the first time, frames architecture for journalistic knowledge platforms as a research issue.  
しかし、本論文の最も重要な新規性は、ジャーナリスティックな知識プラットフォームのアーキテクチャを研究課題として初めて位置づけたことかもしれません。  
The literature on existing systems either does not address architecture at all or it presents processing pipelines without discussing architecture in further depth.  
既存のシステムに関する文献は、アーキテクチャに全く触れないか、アーキテクチャについてさらに深く議論することなく処理パイプラインを提示しています。  
Hence, we plan to investigate architecture for journalistic knowledge platforms more in depth in our further work.  
したがって、今後の研究でジャーナリスティックな知識プラットフォームのアーキテクチャをより深く調査する予定です。



## 7. Conclusion and further work 結論と今後の研究

The paper has shown how pre-and post-news data sources and processing and storage techniques can be combined into a flexible architecture for news journalism. 
本論文では、ニュースジャーナリズムのために、事前および事後のニュースデータソースと処理・ストレージ技術をどのように組み合わせて柔軟なアーキテクチャを構築できるかを示しました。
It thereby answers our initial research question positively. 
これにより、私たちの初期の研究質問に対して肯定的な回答を提供しています。
The evaluation results are encouraging, and we plan to continue to evolve our architecture and prototype in several directions. 
評価結果は励みとなるものであり、私たちはアーキテクチャとプロトタイプをいくつかの方向に進化させ続ける計画です。
We are currently redesigning and reimplementing the prototype into a parallelised big-data ready platform built on top of state-of-art technologies such as Apache Kafka, Blazegraph, Cassandra, Terraform and Ansible. 
現在、私たちはプロトタイプを再設計し、Apache Kafka、Blazegraph、Cassandra、Terraform、Ansibleなどの最先端技術の上に構築された並列化されたビッグデータ対応プラットフォームに再実装しています。
We are also extending and improving the precision of semantic lifting by leveraging recent embedding- and deep-learning based analysis techniques. 
また、最近の埋め込みおよび深層学習に基づく分析技術を活用して、セマンティックリフティングの精度を拡張し改善しています。
We expect that our component-based architecture will make it easy to integrate such new lifting and analysis components into the new News Hunter. 
私たちは、コンポーネントベースのアーキテクチャが、新しいリフティングおよび分析コンポーネントを新しいNews Hunterに統合するのを容易にすることを期待しています。
Furthermore, we are building a larger-scale journalistic knowledge graph and news-item collection for further testing and research. 
さらに、私たちはさらなるテストと研究のために、大規模なジャーナリズム知識グラフとニュースアイテムコレクションを構築しています。
We are currently exploring these possibilities in the ongoing News Angler project, which aims to provide journalists with unexpected angles on and surprising background information about newsworthy events as they unfold. 
現在、私たちは進行中のNews Anglerプロジェクトでこれらの可能性を探求しており、このプロジェクトは、ニュース価値のある出来事が展開される中で、ジャーナリストに予期しない視点や驚くべき背景情報を提供することを目的としています。
Longer-term research challenges include taking into account journalists' and other newsroom workers' preferences and work styles and moving from pure text to non-textual information types, acknowledging that audio and video are also important news sources. 
長期的な研究課題には、ジャーナリストや他のニュースルームの作業者の好みや作業スタイルを考慮に入れ、純粋なテキストから非テキスト情報タイプに移行することが含まれます。音声や映像も重要なニュースソースであることを認識しています。
