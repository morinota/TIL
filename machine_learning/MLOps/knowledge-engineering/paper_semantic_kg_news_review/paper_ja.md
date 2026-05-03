refs: https://dl.acm.org/doi/epdf/10.1145/3543508


# Semantic Knowledge Graphs for the News: A Review ニュースのためのセマンティック知識グラフ：レビュー  
Andreas L. Opdahl, Tareq Al-Moslmi, Duc-Tien Dang-Nguyen, Marc Gallofré Ocaña, Bjørnar Tessem, Csaba Veres  
ACM Computing Surveys, Vol. 55, No. 7, Article 140. December 2022.


## Abstract 要約

ICT platforms for news production, distribution, and consumption must exploit the ever-growing availability of digital data. 
ニュースの制作、配信、消費のためのICTプラットフォームは、ますます増加するデジタルデータの利用可能性を活用しなければなりません。
These data originate from different sources and in different formats; they arrive at different velocities and in different volumes. 
**これらのデータは異なるソースから異なる形式で生成され、異なる速度と異なるボリュームで到着**します。
Semantic knowledge graphs (KGs) is an established technique for integrating such heterogeneous information. 
セマンティック知識グラフ（KG）は、そのような異種情報を統合するための確立された手法です。
It is therefore well-aligned with the needs of news producers and distributors, and it is likely to become increasingly important for the news industry. 
したがって、これはニュースの制作および配信者のニーズに適合しており、ニュース業界にとってますます重要になると考えられます。
This article reviews the research on using semantic knowledge graphs for production, distribution, and consumption of news. 
この記事では、**ニュースの制作、配信、消費におけるセマンティック知識グラフの使用に関する研究**をレビューします。
The purpose is to present an overview of the field; to investigate what it means; and to suggest opportunities and needs for further research and development. 
その目的は、この分野の概要を提示し、それが何を意味するのかを調査し、さらなる研究と開発の機会とニーズを提案することです。

Keywords: News, journalism, news production, news distribution, news consumption, knowledge graphs, ontology, semantic technologies, Linked Data, Linked Open Data, Semantic Web, literature review  
キーワード: ニュース、ジャーナリズム、ニュース制作、ニュース配信、ニュース消費、知識グラフ、オントロジー、セマンティック技術、リンクデータ、リンクオープンデータ、セマンティックウェブ、文献レビュー

<!-- ここまで読んだ! -->


## 1. Introduction はじめに

Journalism relies increasingly on computers and the Internet. 
ジャーナリズムはますますコンピュータとインターネットに依存しています。 
Central drivers are the big and open data sources that have become available on the Web. 
その中心的な要因は、ウェブ上で利用可能になった大規模でオープンなデータソースです。 
For example, researchers have investigated how news events can be extracted from big-data sources such as tweets and other texts and how big and open data can benefit journalistic creativity during the early phases of news production. 
例えば、研究者たちは、ツイートやその他のテキストといったビッグデータソースからニュースイベントをどのように抽出できるか、またビッグデータとオープンデータがニュース制作の初期段階においてジャーナリズムの創造性にどのように寄与できるかを調査しています。 

Semantic knowledge graphs and other semantic technologies offer a way to make big and open data sources more readily available for journalistic and other news-related purposes. 
セマンティック知識グラフやその他のセマンティック技術は、ビッグデータおよびオープンデータソースをジャーナリズムやその他のニュース関連目的により容易に利用できるようにする手段を提供します。 
They offer a standard model and supporting resources for sharing, processing, and storing factual knowledge on both the syntactic and semantic level. 
これらは、構文的および意味的レベルの事実知識を共有、処理、保存するための標準モデルとサポートリソースを提供します。 
Such knowledge graphs thus offer a way to make big, open, and other data sources better integrated and more meaningful. 
したがって、このような知識グラフは、大規模でオープンなデータソースやその他のデータソースをより良く統合し、より意味のあるものにする手段を提供します。 
They make it possible to integrate the highly heterogeneous information available on the Internet and to make it more readily available for journalistic and other news-related purposes. 
これにより、インターネット上で利用可能な非常に異質な情報を統合し、ジャーナリズムやその他のニュース関連目的により容易に利用できるようにします。 

This article will systematically review the research literature on semantic knowledge graphs in the past two decades, from the time when the Semantic Web—an important precursor to semantic knowledge graphs—was first proposed. 
この記事では、セマンティック知識グラフに関する研究文献を過去20年間にわたり体系的にレビューします。これは、セマンティックウェブ（セマンティック知識グラフの重要な前提）が初めて提案された時期から始まります。 
The purpose is to present an overview of the field; to investigate what it means; and to suggest opportunities and needs for further research and development. 
その目的は、この分野の概要を示し、それが何を意味するのかを調査し、さらなる研究と開発の機会とニーズを提案することです。 
We understand both semantic knowledge graphs and the news in a broad sense. 
私たちは、セマンティック知識グラフとニュースの両方を広い意味で理解しています。 
Along with semantic knowledge graphs, we include facilitating semantic technologies such as RDF, OWL, and SPARQL and their uses for semantically Linked (Open) Data and Semantic Web. 
セマンティック知識グラフに加えて、RDF、OWL、SPARQLなどのセマンティック技術を含め、それらのセマンティックにリンクされた（オープン）データおよびセマンティックウェブへの利用を含みます。 
We also include all aspects of production, distribution, and consumption of news. 
また、ニュースの制作、配信、消費のすべての側面も含めます。 
More precise inclusion and exclusion criteria will follow in Section 2. 
より正確な包含および除外基準は、セクション2で示します。 

To the best of our knowledge, no literature review has previously attempted to cover this increasingly important area in depth. 
私たちの知る限り、これまでにこのますます重要な分野を深くカバーしようとした文献レビューはありません。 
Several reviews have been published recently on computational journalism in its various guises, but none of them go deeply into the technology in general nor into semantic knowledge graphs in particular. 
最近、さまざまな形態の計算ジャーナリズムに関するいくつかのレビューが発表されていますが、それらのどれも一般的な技術や特にセマンティック知識グラフに深く踏み込んでいません。 
Also, recent overviews of knowledge graphs do not consider the specific challenges and opportunities for journalism or the news domain. 
また、最近の知識グラフの概要は、ジャーナリズムやニュース分野に特有の課題や機会を考慮していません。 
Among the few papers that discuss the relation between semantic technologies and news, Pellegrini (2012) discusses how Linked Data can be integrated into and add value to news production processes and value chains in a non-disruptive way. 
セマンティック技術とニュースの関係について論じている数少ない論文の中で、Pellegrini（2012）は、リンクデータがニュース制作プロセスやバリューチェーンにどのように統合され、非破壊的に価値を追加できるかを論じています。 
It presents use cases from dynamic semantic publishing at BBC with attention to professional scepticism towards technology-driven innovation. 
これは、技術主導の革新に対する専門的懐疑心に注意を払いながら、BBCの動的セマンティック出版からのユースケースを提示します。 
More recently, Newsroom 3.0 builds on an international field study of three newsrooms—in Brazil, Costa Rica, and the UK—to propose a framework for managing technological and media convergence in newsrooms. 
最近では、Newsroom 3.0がブラジル、コスタリカ、イギリスの3つのニュースルームに関する国際的なフィールドスタディに基づいて、ニュースルームにおける技術的およびメディアの融合を管理するためのフレームワークを提案しています。 
The framework uses semantic technologies to manage news knowledge, attempting to support interdisciplinary teams in their coordination of journalistic activities, cooperative production of content, and communication between professionals and news prosumers. 
このフレームワークは、ニュース知識を管理するためにセマンティック技術を使用し、ジャーナリズム活動の調整、コンテンツの共同制作、専門家とニュースプロシューマー間のコミュニケーションを支援することを試みています。 
Transitions in Journalism discusses how new technologies are constantly challenging well-established journalistic norms and practices, discussing ways in which semantic journalism can exploit semantic technologies for everyday journalism. 
Transitions in Journalismは、新しい技術がどのように確立されたジャーナリズムの規範や慣行に常に挑戦しているかを論じ、セマンティックジャーナリズムが日常のジャーナリズムのためにセマンティック技術をどのように活用できるかを議論しています。 

Compared to these targeted efforts, this article presents the first systematic review of semantic knowledge graphs for news-related purposes in a broad sense. 
これらの特定の取り組みと比較して、この記事はニュース関連目的のためのセマンティック知識グラフに関する初の体系的レビューを広い意味で提示します。 
We ask the following research questions: 
私たちは以下の研究質問を提起します： 
**RQ1**: Which research problems and approaches are most common, and what are the central results? 
**RQ1**: どの研究問題とアプローチが最も一般的であり、中心的な結果は何ですか？ 
For example, the different research contributions may produce different types of results; use different research methods; target different users; focus on different news-related tasks using different input data; use different semantic and other techniques; and address different news domains, languages, and phases of the news life-cycle. 
例えば、異なる研究貢献は異なるタイプの結果を生み出す可能性があり、異なる研究方法を使用し、異なるユーザーを対象とし、異なる入力データを使用して異なるニュース関連タスクに焦点を当て、異なるセマンティックおよびその他の技術を使用し、異なるニュースドメイン、言語、ニュースライフサイクルの段階に対処します。 

**RQ2**: Which research problems and approaches have received less attention, and what types of contributions are rarer? 
**RQ2**: どの研究問題とアプローチがあまり注目されておらず、どのような貢献がより稀ですか？ 
Where are the green fields and other areas where knowledge is limited and further research needed? 
知識が限られている緑のフィールドやその他の領域はどこにあり、さらなる研究が必要ですか？ 

**RQ3**: How is the research evolving? 
**RQ3**: 研究はどのように進化していますか？ 
Different problems, result types, and approaches may be more or less prominent at different times, and each of them may be dealt with differently at different times. 
異なる問題、結果のタイプ、アプローチは、異なる時期においてより目立つ場合もあれば、そうでない場合もあり、それぞれが異なる時期に異なる方法で扱われる可能性があります。 

**RQ4**: Which are the most frequently cited papers and projects, and which papers and projects are citing one another? 
**RQ4**: 最も頻繁に引用される論文やプロジェクトはどれで、どの論文やプロジェクトが互いに引用していますか？ 
For example, how is the research literature organised; which earlier results are cited most by the main papers; and which main papers are most cited in the broader literature? 
例えば、研究文献はどのように整理されているか、主要な論文によって最も引用される以前の結果は何か、そしてどの主要な論文がより広範な文献で最も引用されていますか？ 

To answer these questions, the rest of the article is organised as follows: 
これらの質問に答えるために、この記事の残りの部分は以下のように構成されています： 
Section 2 outlines the literature-review process. 
セクション2では文献レビューのプロセスを概説します。 
Section 3 reviews the main papers. 
セクション3では主要な論文をレビューします。 
Section 4 discusses the main papers, answers the research questions, and offers many paths for further work. 
セクション4では主要な論文を議論し、研究質問に答え、さらなる作業のための多くの道を提供します。 
Section 5 concludes the article. 
セクション5ではこの記事を締めくくります。



## 2. Method 方法

To answer our research questions, we conduct a systematic literature review (SLR). 
私たちは研究質問に答えるために、系統的文献レビュー（SLR）を実施します。

In line with our aim to present an overview of the field, we review the research literature in breadth to cover as many salient research problems, approaches, and potential solutions as possible. 
私たちの目的はこの分野の概要を提示することであり、重要な研究問題、アプローチ、潜在的な解決策をできるだけ多くカバーするために、広範に研究文献をレビューします。

Our review covers research on semantic knowledge graphs for the news understood in a wide sense. 
私たちのレビューは、広義に理解されるニュースのためのセマンティック知識グラフに関する研究をカバーします。

We include papers that use semantic technologies such as RDF, OWL, and SPARQL and practices such as Linked (Open) Data and Semantic Web, but we exclude papers that use graph structures only for computational purposes isolated from the semantically linked Web of Data. 
私たちは、RDF、OWL、SPARQLなどのセマンティック技術や、Linked (Open) DataやSemantic Webなどの実践を使用する論文を含めますが、セマンティックにリンクされたデータのWebから孤立した計算目的のためだけにグラフ構造を使用する論文は除外します。

We also include all aspects of production, distribution, and consumption of news, but we exclude research that uses news corpora only for evaluation purposes. 
私たちはニュースの生産、配信、消費のすべての側面を含めますが、評価目的のためだけにニュースコーパスを使用する研究は除外します。

We search for literature through the five search engines ACM Digital Library, Elsevier ScienceDirect, IEEE Xplore, SpringerLink, and Clarivate Analytics' Web of Science. 
私たちは、ACM Digital Library、Elsevier ScienceDirect、IEEE Xplore、SpringerLink、Clarivate AnalyticsのWeb of Scienceという5つの検索エンジンを通じて文献を検索します。

We also conduct supplementary searches using Google Scholar. 
また、Google Scholarを使用して補足的な検索も行います。

We search using variations of the phrases "knowledge graph," "semantic technology," "linked data," "linked open data," and "semantic web" combined with variations of "news" and "journalism" adapted to each search engine's syntax. 
私たちは、各検索エンジンの構文に適応した「ニュース」や「ジャーナリズム」のバリエーションと組み合わせた「knowledge graph」、「semantic technology」、「linked data」、「linked open data」、「semantic web」というフレーズのバリエーションを使用して検索します。

We select peer-reviewed and archival papers published in esteemed English-language journals or in high-quality conferences and workshops. 
私たちは、権威ある英語の学術誌や高品質の会議およびワークショップで発表された査読済みのアーカイブ論文を選択します。

The search results are screened in three stages, so each selected paper is in the end considered by at least three co-authors. 
検索結果は3段階でスクリーニングされるため、最終的に各選択された論文は少なくとも3人の共著者によって検討されます。

In the first stage, we screen search results based on title, abstract, and keywords. 
第一段階では、タイトル、要約、キーワードに基づいて検索結果をスクリーニングします。

In the second stage, we skim the full papers and also consider the length, type, language, and source of each paper. 
第二段階では、全文をざっと読み、各論文の長さ、タイプ、言語、出所も考慮します。

In the third stage, we analyse the selected papers in detail according to the framework described below. 
第三段階では、以下に説明するフレームワークに従って選択された論文を詳細に分析します。

When several papers describe the same line of work, we select the most recent and comprehensive report. 
複数の論文が同じ作業ラインを説明している場合、私たちは最も最近の包括的な報告を選択します。

In the end, more than 6,000 search results are narrowed down to 80 fully analysed main papers. 
最終的に、6,000以上の検索結果が80の完全に分析された主要論文に絞り込まれます。

Through a pilot study, we establish an analysis framework that we continue to revise and refine as the analysis progresses. 
パイロットスタディを通じて、私たちは分析が進むにつれて継続的に改訂・洗練していく分析フレームワークを確立します。

The 10 top-level themes in the final framework are: 
最終フレームワークの10のトップレベルテーマは次のとおりです：

- **Technical result type**: pipelines/prototypes, industrial platforms, algorithms, ontologies, knowledge graphs. 
- **技術的結果の種類**: パイプライン/プロトタイプ、産業プラットフォーム、アルゴリズム、オントロジー、知識グラフ。

- **Empirical result type**: experiments, case studies, industrial testing, etc. 
- **経験的結果の種類**: 実験、ケーススタディ、産業テストなど。

- **Intended users**: general news users, journalists, archivists, knowledge workers. 
- **対象ユーザー**: 一般ニュースユーザー、ジャーナリスト、アーキビスト、知識労働者。

- **Task**: semantic annotation, event detection, relation extraction, content retrieval/provision/enrichment. 
- **タスク**: セマンティックアノテーション、イベント検出、関係抽出、コンテンツの取得/提供/強化。

- **Input data**: digital news articles, social media messages, multimedia news. 
- **入力データ**: デジタルニュース記事、ソーシャルメディアメッセージ、マルチメディアニュース。

- **News life cycle**: future news, emerging news, breaking news, developing news, already published news. 
- **ニュースライフサイクル**: 未来のニュース、新興ニュース、速報ニュース、発展中のニュース、すでに公開されたニュース。

- **Semantic techniques**: exchange standards, ontologies and vocabularies, semantic data resources, processing and storage techniques. 
- **セマンティック技術**: 交換基準、オントロジーと語彙、セマンティックデータリソース、処理およびストレージ技術。

- **Other techniques**: news standards, NLP, ML, DL. 
- **その他の技術**: ニュース基準、NLP、ML、DL。

- **News domain**: economy/finance, environment, education, etc. 
- **ニュースドメイン**: 経済/金融、環境、教育など。

- **Language and region**: language(s) targeted by the research. 
- **言語と地域**: 研究の対象となる言語。

For example, many main papers address specific groups of intended users. 
例えば、多くの主要論文は特定の対象ユーザーグループに対処しています。

Intended users therefore becomes a top-level theme in our framework, with more specific groups of users, such as journalists, archivists, and fact checkers, as sub-themes. 
したがって、対象ユーザーは私たちのフレームワークのトップレベルテーマとなり、ジャーナリスト、アーキビスト、ファクトチェッカーなどのより具体的なユーザーグループがサブテーマとなります。

We make the detailed paper analyses along with their metadata available as a semantic knowledge graph through a SPARQL endpoint. 
私たちは、詳細な論文分析とそのメタデータをSPARQLエンドポイントを通じてセマンティック知識グラフとして提供します。

To support impact analysis, the metadata includes all incoming and outgoing citations of and by our main papers. 
影響分析をサポートするために、メタデータには私たちの主要論文のすべての受信および送信の引用が含まれています。

The complete graph contains information about 4,238 papers, 9,712 authors, and 699 topics from Semantic Scholar. 
完全なグラフには、4,238の論文、9,712の著者、およびSemantic Scholarからの699のトピックに関する情報が含まれています。



## 3. Review of Main Papers 主要論文のレビュー

This section reviews the 80 main papers according to the themes of the framework.  
このセクションでは、フレームワークのテーマに従って80の主要な論文をレビューします。  
Our review and discussion is based on careful manual reading, analysis, marking, and discussion of the main papers, organised by the evolving themes and sub-themes in our analysis framework.  
私たちのレビューと議論は、進化するテーマとサブテーマに基づいて整理された主要な論文の慎重な手動読解、分析、マーク付け、議論に基づいています。  

### 3.1. Technical Result Types 技術的結果の種類

The main papers present a wide variety of technical research results.  
主要な論文は、さまざまな技術的研究結果を示しています。  
**Pipelines and prototypes**: A clear majority of main papers develop ICT architectures and tools for supporting news-related information processing with semantic knowledge graphs and related techniques.  
**パイプラインとプロトタイプ**: 明らかに大多数の主要な論文は、セマンティック知識グラフや関連技術を用いてニュース関連情報処理を支援するICTアーキテクチャとツールを開発しています。  
Most common are research prototypes and experimental pipelines.  
最も一般的なのは、研究プロトタイプと実験的パイプラインです。  
For example, the Knowledge and Information Management (KIM) platform is an early and much-cited information extraction system that annotates and indexes named entities found in news documents semantically and makes them available for retrieval.  
例えば、Knowledge and Information Management (KIM)プラットフォームは、ニュース文書に見られる固有名詞をセマンティックに注釈付けし、インデックス化して検索可能にする初期の引用の多い情報抽出システムです。  
To allow precise ontology-based retrieval, each identified entity is annotated with both a specific instance in an extensive knowledge base and a class defined in the associated KIM Ontology (KIMO), which defines around 250 classes and 100 attributes and relations.  
正確なオントロジーに基づく検索を可能にするために、各特定されたエンティティには、広範な知識ベース内の特定のインスタンスと、約250のクラスと100の属性および関係を定義する関連するKIMオントロジー（KIMO）で定義されたクラスの両方が注釈付けされています。  
The platform offers a graphical user interface for viewing, browsing and performing complex searches in collections of annotated news articles.  
このプラットフォームは、注釈付きニュース記事のコレクションを表示、閲覧、および複雑な検索を実行するためのグラフィカルユーザーインターフェースを提供します。  
Another early initiative is the News Engine Web Services (NEWS) project, which presents a prototype that automatically annotates published news items in several languages.  
もう一つの初期の取り組みは、News Engine Web Services (NEWS)プロジェクトで、これは複数の言語で公開されたニュース項目を自動的に注釈付けするプロトタイプを提示します。  
The aim is to help news agencies provide fresh, relevant, and high-quality information to their customers.  
その目的は、ニュース機関が顧客に新鮮で関連性が高く、高品質な情報を提供するのを助けることです。  
NEWS uses a dedicated ontology (the NEWS Ontology) to facilitate semantic search, subscription-based services, and news creation through a web-based user interface.  
NEWSは、セマンティック検索、サブスクリプションベースのサービス、およびウェブベースのユーザーインターフェースを通じたニュース作成を促進するために、専用のオントロジー（NEWSオントロジー）を使用します。  
Hermes supplies news-based evidence to decision-makers.  
Hermesは、意思決定者にニュースに基づく証拠を提供します。  
To facilitate semantic retrieval, it automatically identifies topics in news articles and classifies them.  
セマンティック検索を促進するために、ニュース記事内のトピックを自動的に特定し、分類します。  
The topics and classes are defined in an ontology that has been extended with synonyms and hypernyms from WordNet to improve recall.  
トピックとクラスは、リコールを改善するためにWordNetからの同義語と上位語で拡張されたオントロジーで定義されています。  

**Production systems**: Some main papers take one step further and present industrial platforms that have run in news organisations, either experimentally or in production.  
**生産システム**: 一部の主要な論文はさらに一歩進んで、ニュース組織で実験的または本番で稼働している産業プラットフォームを提示します。  
The earliest example is AnnoTerra, a system developed by NASA to enhance earth-science news feeds with content from relevant multimedia data sources.  
最も早い例は、NASAによって開発されたAnnoTerraで、関連するマルチメディアデータソースからのコンテンツで地球科学ニュースフィードを強化します。  
The system matches ontology concepts with keywords found in the news texts to identify data sources and support semantic searches.  
このシステムは、ニューステキストに見られるキーワードとオントロジー概念を一致させてデータソースを特定し、セマンティック検索をサポートします。  
Sánchez-Fernández et al. report industrial experience with NEWS at EFE, a Spanish international news agency.  
Sánchez-Fernándezらは、スペインの国際ニュース機関EFEでのNEWSに関する産業経験を報告しています。  
The most recent example is VLX-Stories, a commercial, multilingual system for event detection and information retrieval from media feeds.  
最も最近の例は、メディアフィードからのイベント検出と情報検索のための商業的な多言語システムであるVLX-Storiesです。  
The system harvests information from online news sites; aggregates them into events; labels them semantically; and represents them in a knowledge graph.  
このシステムは、オンラインニュースサイトから情報を収集し、それをイベントに集約し、セマンティックにラベル付けし、知識グラフで表現します。  
The system is also able to detect emerging entities in online news.  
このシステムは、オンラインニュースにおける新たなエンティティを検出することもできます。  
VLX-Stories is deployed in production in several organisations in several countries.  
VLX-Storiesは、いくつかの国のいくつかの組織で本番環境に展開されています。  
Each month, it detects over 9,000 events from over 4,000 news feeds from seven different countries and in three different languages, extending its knowledge graph with 1,300 new entities as a side result.  
毎月、7つの異なる国から4,000以上のニュースフィードから9,000以上のイベントを検出し、1,300の新しいエンティティを副次的な結果として知識グラフに追加します。  

**System architectures**: Whether oriented towards research or industry, another group of papers proposes system architectures.  
**システムアーキテクチャ**: 研究または産業に向けられたものであれ、別のグループの論文はシステムアーキテクチャを提案しています。  
The World News Finder presents an architecture that is representative of many systems that exploit KGs for managing news content.  
World News Finderは、ニュースコンテンツを管理するためにKGを活用する多くのシステムを代表するアーキテクチャを提示します。  
Online news articles in HTML format are parsed and analysed using GATE (General Architecture for Text Engineering) and ANNIE (A Nearly New Information Extraction system) with the support of JAPE (Java Annotations Pattern Engine) rules and ontology gazetteering lists.  
HTML形式のオンラインニュース記事は、GATE（General Architecture for Text Engineering）およびANNIE（A Nearly New Information Extraction system）を使用して解析および分析され、JAPE（Java Annotations Pattern Engine）ルールとオントロジーガゼッタリリストのサポートを受けます。  
A domain ontology is then used in combination with heuristic rules to annotate the analysed news texts semantically.  
次に、ドメインオントロジーがヒューリスティックルールと組み合わせて使用され、分析されたニューステキストにセマンティックに注釈付けされます。  
The annotated news articles are represented in a metadata repository and made available for semantic search through a GUI.  
注釈付きニュース記事はメタデータリポジトリに表現され、GUIを通じてセマンティック検索のために利用可能になります。  

**Algorithms**: Another group of papers focuses on developing algorithms that exploit semantic knowledge graphs and related techniques, usually supported by proof-of-concept prototypes that are also used for evaluation.  
**アルゴリズム**: 別のグループの論文は、セマンティック知識グラフや関連技術を活用するアルゴリズムの開発に焦点を当てており、通常は評価にも使用される概念実証プロトタイプによってサポートされています。  
Inspired by Google's PageRank algorithm, Fernández et al. propose the IdentityRank algorithm for named entity disambiguation in the NEWS project.  
GoogleのPageRankアルゴリズムに触発されて、FernándezらはNEWSプロジェクトにおける固有名詞の曖昧さ解消のためのIdentityRankアルゴリズムを提案します。  
IdentityRank dynamically adjusts its weights for ranking candidate instances based on news trends (the frequency of each instance in a period of time) and semantic coherence (the frequency of the instance in a certain context), and it can be retrained based on user feedback and corrections.  
IdentityRankは、ニューストレンド（一定期間内の各インスタンスの頻度）とセマンティックコヒーレンス（特定のコンテキスト内のインスタンスの頻度）に基づいて候補インスタンスのランキングのための重みを動的に調整し、ユーザーフィードバックや修正に基づいて再訓練することができます。  
Ponza et al. take trending entities in news streams as their starting point and attempt to identify and rank other entities in their context.  
Ponzaらは、ニュースストリーム内のトレンドエンティティを出発点として、他のエンティティをそのコンテキスト内で特定し、ランキングしようとします。  
The purpose is to represent trends more richly and understand them better.  
その目的は、トレンドをより豊かに表現し、よりよく理解することです。  
One unsupervised and one supervised algorithm are compared.  
1つの教師なしアルゴリズムと1つの教師ありアルゴリズムが比較されます。  
The unsupervised approach uses a personalised version of the PageRank algorithm over a graph of trending and contextual entities.  
教師なしアプローチは、トレンドおよびコンテキストエンティティのグラフ上でPageRankアルゴリズムのパーソナライズ版を使用します。  
The edges encode directional similarities between the entities using embeddings from a background knowledge graph.  
エッジは、バックグラウンド知識グラフからの埋め込みを使用して、エンティティ間の方向性の類似性をエンコードします。  
The supervised, and better performing, approach uses a selection of hand-crafted features along with a learning-to-rank (LTR) model, LightGBM.  
教師ありで、より良いパフォーマンスを発揮するアプローチは、手作りの特徴の選択と学習ランキング（LTR）モデルであるLightGBMを使用します。  
The selected features include positions and frequencies of the entities in the input texts, their co-occurrences and popularity, coherence measures based on TagMe and on entity embeddings, and the entities' local importance in the text (or salience).  
選択された特徴には、入力テキスト内のエンティティの位置と頻度、共起と人気、TagMeおよびエンティティ埋め込みに基づくコヒーレンス測定、テキスト内のエンティティの局所的重要性（または顕著性）が含まれます。  
NewsLink processes news articles and natural-language (NL) queries from users in the same way, using standard natural-language processing (NLP) techniques.  
NewsLinkは、標準的な自然言語処理（NLP）技術を使用して、ニュース記事とユーザーからの自然言語（NL）クエリを同様に処理します。  
Co-occurrence between entities in a news article or query is used to divide it into segments, for example, corresponding to sentences.  
ニュース記事やクエリ内のエンティティ間の共起は、それをセグメントに分割するために使用されます。例えば、文に対応するセグメントです。  
The entities in each segment are mapped to an open KG from which a connected sub-graph is extracted to represent the segment.  
各セグメント内のエンティティはオープンKGにマッピングされ、そこからセグメントを表すための接続されたサブグラフが抽出されます。  
The sub-graphs are then merged to represent the articles and queries as KGs that can be compared for similarity to support more robust and explainable query answering.  
サブグラフはその後マージされ、記事とクエリをKGとして表現し、類似性を比較してより堅牢で説明可能なクエリ応答をサポートします。  
Hermes also provides an algorithm for ranking semantic search results.  
Hermesは、セマンティック検索結果のランキングのためのアルゴリズムも提供します。  

**Neural-network architectures**: Rather than proposing algorithms, many recent main papers instead exploit semantic knowledge graphs for news purposes using deep neural-network (NN) architectures.  
**ニューラルネットワークアーキテクチャ**: アルゴリズムを提案するのではなく、多くの最近の主要な論文は、深層ニューラルネットワーク（NN）アーキテクチャを使用してニュース目的のためにセマンティック知識グラフを活用しています。  
These papers, too, are supported by proof-of-concept prototypes, which are usually evaluated using gold-standard datasets and information retrieval (IR) metrics.  
これらの論文も、通常はゴールドスタンダードデータセットと情報検索（IR）メトリクスを使用して評価される概念実証プロトタイプによってサポートされています。  
Heterogeneous graph Embedding framework for Emerging Relation detection (HEER) detects emerging entities and relations from text reports, i.e., new entities and relations in the news that have so far not been included in a knowledge graph.  
新たな関係検出のための異種グラフ埋め込みフレームワーク（HEER）は、テキストレポートから新たなエンティティと関係を検出します。つまり、これまで知識グラフに含まれていなかったニュース内の新しいエンティティと関係です。  
The challenges addressed are that new entities and relations appear at high speed, with little available information at first and without negative examples to learn from.  
取り組まれている課題は、新しいエンティティと関係が高速度で現れ、最初は利用可能な情報がほとんどなく、学習するためのネガティブな例がないことです。  
HEER represents incoming news texts as graphs based on entity co-occurrence and incrementally maintains joint embeddings of the news graphs and an open knowledge graph.  
HEERは、エンティティの共起に基づいて受信ニューステキストをグラフとして表現し、ニュースグラフとオープン知識グラフの共同埋め込みを段階的に維持します。  
The result is positive and unlabelled (PU) entity embeddings that are used to train and maintain a PU classifier that detects emerging relations incrementally.  
その結果は、ポジティブでラベル付けされていない（PU）エンティティ埋め込みであり、これを使用して新たな関係を段階的に検出するPU分類器を訓練および維持します。  

Context-Aware Graph Embedding (CAGE) is an approach for session-based news recommendation.  
Context-Aware Graph Embedding (CAGE)は、セッションベースのニュース推薦のためのアプローチです。  
Entities are extracted from input texts and used to extract a sub-knowledge graph from an open knowledge graph (the paper uses Wikidata).  
エンティティは入力テキストから抽出され、オープン知識グラフ（この論文ではWikidataを使用）からサブ知識グラフを抽出するために使用されます。  
Knowledge-graph embeddings are calculated from the sub-knowledge graph, whereas pre-trained word embeddings and Convolutional Neural Networks (CNNs) are used to derive content embeddings from the corresponding input texts.  
知識グラフの埋め込みはサブ知識グラフから計算され、一方で事前訓練された単語埋め込みと畳み込みニューラルネットワーク（CNN）が対応する入力テキストからコンテンツ埋め込みを導出するために使用されます。  
The knowledge-graph and content embeddings are concatenated and combined with user embeddings and refined further using CNNs.  
知識グラフとコンテンツ埋め込みは連結され、ユーザー埋め込みと組み合わされ、さらにCNNを使用して洗練されます。  
Finally, an Attention Neural Network (ANN) on top of Gated Recurrent Units (GRUs) are used to recommend articles from the resulting embeddings, taking short-term user preferences into account.  
最後に、Gated Recurrent Units (GRUs)の上にあるAttention Neural Network (ANN)が、得られた埋め込みから記事を推薦するために使用され、短期的なユーザーの好みを考慮します。  

Deep Triple Networks (DTN) use a deep-network architecture for topic-specific fake news detection.  
Deep Triple Networks (DTN)は、トピック特化型のフェイクニュース検出のための深層ネットワークアーキテクチャを使用します。  
News texts are analysed in two ways in parallel: The first way is to use word2vec embeddings and self-attention on the raw input text.  
ニューステキストは、2つの方法で並行して分析されます。最初の方法は、生の入力テキストに対してword2vec埋め込みと自己注意を使用することです。  
The second way is to extract triples from the text and analyse them using TransD graph embeddings, attention and a bi-directional LSTM (Long Short-Term Memory).  
2つ目の方法は、テキストからトリプルを抽出し、TransDグラフ埋め込み、注意、双方向LSTM（Long Short-Term Memory）を使用して分析することです。  
A CNN is used to combine the results of the two parallel analyses into a single output vector.  
CNNは、2つの並行分析の結果を単一の出力ベクトルに結合するために使用されます。  
Background knowledge has been infused into the second way by training the TransD graph embeddings, not only on the triples extracted from the input text, but also on related triples from a 4-hop DBpedia extract.  
背景知識は、入力テキストから抽出されたトリプルだけでなく、4ホップDBpedia抽出からの関連トリプルに対してもTransDグラフ埋め込みを訓練することによって、2つ目の方法に注入されています。  
Maximum and average biases from the graph triples are concatenated with the CNN output vector and used to classify news texts as real or fake.  
グラフトリプルからの最大および平均バイアスはCNN出力ベクトルと連結され、ニューステキストを真または偽として分類するために使用されます。  
The intuition behind this and other bias-based approaches to fake news detection is that, if the input text is false, triples learned only from the input text will have smaller bias than triples learned from the same text infused with true (and thus conflicting) real-world knowledge.  
このアプローチや他のバイアスベースのフェイクニュース検出アプローチの背後にある直感は、入力テキストが偽である場合、入力テキストからのみ学習されたトリプルは、真実（したがって矛盾する）現実世界の知識で注入された同じテキストから学習されたトリプルよりも小さいバイアスを持つということです。  

**Ontologies**: Almost half the papers include a general or domain-specific ontology for creating and managing other semantic knowledge graphs.  
**オントロジー**: ほぼ半数の論文は、他のセマンティック知識グラフを作成および管理するための一般的またはドメイン特化型のオントロジーを含んでいます。  
For example, the NEWS project uses OWL to represent the NEWS Ontology, which standardises and interconnects the semantic labels used to annotate and disseminate news content.  
例えば、NEWSプロジェクトはOWLを使用してNEWSオントロジーを表現し、ニュースコンテンツを注釈付けし、普及させるために使用されるセマンティックラベルを標準化し、相互接続します。  
The Semantics-based Pipeline for Economic Event Detection (SPEED) uses a finance ontology represented in OWL to ensure interoperability between and reuse of existing semantic and NLP solutions.  
経済イベント検出のためのセマンティクスベースのパイプライン（SPEED）は、OWLで表現されたファイナンスオントロジーを使用して、既存のセマンティックおよびNLPソリューション間の相互運用性と再利用を確保します。  
Troncy represents the IPTC (International Press Telecommunications Council) News Codes as SKOS concepts in an OWL ontology and discusses its uses for semantic enrichment and search.  
Troncyは、IPTC（国際プレス電気通信評議会）ニュースコードをOWLオントロジー内のSKOS概念として表現し、セマンティックな強化と検索のための使用について議論します。  



. Troncy represents the IPTC (International Press Telecommunications Council) News Codes as SKOS concepts in an OWL ontology and discusses its uses for semantic enrichment and search. 
トロンシーは、IPTC（国際報道通信評議会）ニュースコードをSKOS概念としてOWLオントロジーで表現し、意味的な強化と検索への利用について論じています。

The Evolutionary Event Ontology Knowledge (EEOK) ontology represents how different types of news events tend to unfold over time. 
進化的イベントオントロジー知識（EEOK）オントロジーは、異なるタイプのニュースイベントが時間とともにどのように展開するかを表現します。

The ontology is supported by a pipeline that mines event-evolution patterns from natural-language news texts that report different stages of the same macro event (or storyline). 
このオントロジーは、同じマクロイベント（またはストーリーライン）の異なる段階を報告する自然言語ニューステキストからイベント進化パターンをマイニングするパイプラインによってサポートされています。

The patterns are represented in OWL and used to extract and predict further events in developing storylines more precisely.  
これらのパターンはOWLで表現され、発展中のストーリーラインにおけるさらなるイベントをより正確に抽出し予測するために使用されます。

**Knowledge graphs**: A few papers even present a populated, instance-level semantic knowledge graph or other linked knowledge base as a central result. 
**知識グラフ**: いくつかの論文では、人口が埋められたインスタンスレベルのセマンティック知識グラフや他のリンクされた知識ベースを中心的な結果として提示しています。

For example, K-Pop populates a semantic knowledge graph for enriching news about Korean pop artists. 
例えば、K-Popは韓国のポップアーティストに関するニュースを強化するためのセマンティック知識グラフを構築します。

The purpose is to provide comprehensive profiles for singers and groups, their activities, organisations, and catalogues. 
その目的は、歌手やグループ、彼らの活動、組織、カタログの包括的なプロフィールを提供することです。

As an example application, the resulting entertainment KG is used to power Gnosis, a mobile application for recommending K-Pop news articles. 
例として、得られたエンターテインメントKGは、K-Popニュース記事を推薦するためのモバイルアプリケーションGnosisを支えるために使用されます。

CrimeBase presents a knowledge graph that integrates crime-related information from popular Indian online newspapers. 
CrimeBaseは、人気のあるインドのオンライン新聞から犯罪関連情報を統合した知識グラフを提示します。

The purpose is to help law enforcement agencies analyse and prevent criminal activities by gathering and integrating crime entities from text and images and making them available in machine-readable form. 
その目的は、テキストや画像から犯罪エンティティを収集・統合し、それを機械可読形式で提供することによって、法執行機関が犯罪活動を分析し防止するのを助けることです。

ClaimsKG is a live knowledge graph that represents more than 28,000 fact-checked claims published since 1996, totalling over 6 million triples. 
ClaimsKGは、1996年以降に公開された28,000以上のファクトチェックされた主張を表すライブ知識グラフで、合計600万以上のトリプルを含みます。

It uses a semi-automatic pipeline to harvest fact checks from popular fact-checking websites; annotate them with entities from DBpedia; represent them in RDF according to a semantic data model in RDFS; normalise the validity ratings; and resolve co-references across claims. 
これは、人気のファクトチェックウェブサイトからファクトチェックを収集するための半自動パイプラインを使用し、DBpediaのエンティティで注釈を付け、RDFSのセマンティックデータモデルに従ってRDFで表現し、妥当性評価を正規化し、主張間の共参照を解決します。

Duroyon et al. use hashtags and other metadata associated with tweets and tweeters to build an RDF model of over 900,000 French political tweets, totalling more than 20 million triples that describe facts, statements, and beliefs in time. 
デュロヨンらは、ツイートやツイッター利用者に関連するハッシュタグや他のメタデータを使用して、90万以上のフランスの政治ツイートのRDFモデルを構築し、時間における事実、声明、信念を記述する2000万以上のトリプルを合計します。

The purpose is to trace how actors propagate knowledge—as well as misinformation and hearsay—over time. 
その目的は、時間の経過とともに、アクターが知識をどのように広めるか—誤情報や噂も含めて—を追跡することです。

**Formal models**: A small final group of papers proposes formal models of various types and for different purposes. 
**形式モデル**: 最後の小さなグループの論文は、さまざまなタイプと異なる目的のための形式モデルを提案しています。

For example, Golbeck and Halaschek-Wiener present a formal model for managing inconsistencies that arise when live news streams are represented incrementally using description logic. 
例えば、ゴルベックとハラスチェック＝ウィーナーは、ライブニュースストリームが記述論理を使用して段階的に表現されるときに発生する矛盾を管理するための形式モデルを提示します。

A trust-based algorithm for belief-base revision is presented that takes users' trust in information sources into account when choosing which inconsistent information to discard. 
ユーザーの情報源に対する信頼を考慮して、どの矛盾した情報を破棄するかを選択する際に、信頼に基づく信念ベースの修正アルゴリズムが提示されています。

**Summary**: Our review suggests that the most common types of results are pipelines and prototypes. 
**要約**: 私たちのレビューは、最も一般的な結果のタイプはパイプラインとプロトタイプであることを示唆しています。

In addition, many papers propose ontologies, system architectures, algorithms, and neural-network architectures. 
さらに、多くの論文がオントロジー、システムアーキテクチャ、アルゴリズム、ニューラルネットワークアーキテクチャを提案しています。

A few papers also introduce new knowledge graphs. 
いくつかの論文は新しい知識グラフも紹介しています。

There has been a shift in recent years from research on algorithms and system architectures towards papers that propose deep neural-network architectures. 
近年、アルゴリズムやシステムアーキテクチャに関する研究から、深層ニューラルネットワークアーキテクチャを提案する論文へのシフトが見られます。

A few of those recent papers also mention explainability. 
最近のいくつかの論文では、説明可能性についても言及されています。

### 3.2. Empirical Result Types  
### 3.2. 実証結果のタイプ

A large majority of the papers include an empirical evaluation of their technical proposals.  
大多数の論文は、技術提案の実証評価を含んでいます。

**Experiments**: As shown in the previous section, a majority of papers develop pipelines or prototypes, which are then evaluated empirically.  
**実験**: 前のセクションで示したように、大多数の論文はパイプラインやプロトタイプを開発し、それが実証的に評価されます。

The most common evaluation method is controlled experiments using gold-standard datasets and information retrieval (IR) measures such as precision (P), recall (R), and accuracy (A).  
最も一般的な評価方法は、ゴールドスタンダードデータセットと情報検索（IR）指標（精度（P）、再現率（R）、正確性（A）など）を使用した制御実験です。

For example, KOPRA is a deep-learning approach that uses a Graph Convolutional Network (GCN) for news recommendation.  
例えば、KOPRAはニュース推薦のためにグラフ畳み込みネットワーク（GCN）を使用する深層学習アプローチです。

An initial entity graph (called interest graph) is created for each user from entities mentioned in the news titles and abstracts of that user's short- and long-term click histories.  
初期エンティティグラフ（インタレストグラフと呼ばれる）は、ニュースのタイトルやそのユーザーの短期および長期のクリック履歴に言及されたエンティティから各ユーザーのために作成されます。

A joint knowledge pruning and Recurrent Graph Convolution (RGC) mechanism is then used to augment the entities in the interest graph with related entities from an open KG.  
次に、共同知識プルーニングと再帰的グラフ畳み込み（RGC）メカニズムを使用して、オープンKGからの関連エンティティでインタレストグラフ内のエンティティを増強します。

Finally, entities extracted from candidate news texts are compared with entities in the interest graphs to predict articles a user may find interesting.  
最後に、候補ニューステキストから抽出されたエンティティは、インタレストグラフ内のエンティティと比較され、ユーザーが興味を持つ可能性のある記事を予測します。

The approach is evaluated experimentally with Wikidata as the open KG and using two standard datasets (MIND and Adressa).  
このアプローチは、オープンKGとしてWikidataを使用し、2つの標準データセット（MINDとAdressa）を使用して実験的に評価されます。

RDFLiveNews aims to represent RSS data streams as RDF triples in real time.  
RDFLiveNewsは、RSSデータストリームをリアルタイムでRDFトリプルとして表現することを目指しています。

Candidate triples are extracted from individual RSS items and clustered to suggested output triples.  
候補トリプルは、個々のRSSアイテムから抽出され、提案された出力トリプルにクラスタリングされます。

Components of the approach are evaluated in two ways.  
アプローチのコンポーネントは2つの方法で評価されます。

The first way measures RDFLiveNews' ability to disambiguate alternative URIs for named entities detected in the input items.  
最初の方法は、入力アイテムで検出された名前付きエンティティの代替URIを明確にするRDFLiveNewsの能力を測定します。

Disambiguation results are evaluated against a manually crafted gold standard using precision, recall, and F1 metrics and by comparing them to the outputs of a state-of-art NED tool (AIDA).  
明確化結果は、精度、再現率、F1メトリックを使用して手動で作成されたゴールドスタンダードと比較し、最先端のNEDツール（AIDA）の出力と比較して評価されます。

The second way measures RDFLiveNews' ability to cluster similar triples extracted from different RSS items.  
2つ目の方法は、異なるRSSアイテムから抽出された類似トリプルをクラスタリングするRDFLiveNewsの能力を測定します。

The clusters are evaluated against the manually crafted gold standard using sensitivity (S), positive predictive value (PPV), and their geometric mean.  
クラスタは、感度（S）、陽性的中率（PPV）、およびそれらの幾何平均を使用して手動で作成されたゴールドスタンダードと比較して評価されます。

**Performance evaluation**: A smaller number of experimental papers collect performance measures such as execution times and throughput in addition to or instead of IR measures.  
**パフォーマンス評価**: より少数の実験論文は、IR指標の代わりにまたはそれに加えて、実行時間やスループットなどのパフォーマンス測定を収集します。

For example, the scalability of RDFLiveNews is also measured using run times for different components of the approach on three test corpora.  
例えば、RDFLiveNewsのスケーラビリティは、3つのテストコーパスにおけるアプローチの異なるコンポーネントの実行時間を使用して測定されます。

The results suggest that, with some parallelisation, it is able to handle at least 1,500 parallel RSS feeds.  
結果は、いくつかの並列処理を行うことで、少なくとも1,500の並列RSSフィードを処理できることを示唆しています。

The performance of KnowledgeSeeker, an ontology-based agent system for recommending Chinese news articles, is measured through execution times on three datasets for a given computer configuration and using the performance of a vanilla TF-IDF-based approach as comparison baseline.  
中国のニュース記事を推薦するためのオントロジーに基づくエージェントシステムであるKnowledgeSeekerのパフォーマンスは、特定のコンピュータ構成に対して3つのデータセットでの実行時間を通じて測定され、バニラTF-IDFベースのアプローチのパフォーマンスを比較ベースラインとして使用します。

The throughput of SPEED is benchmarked on a corpus of 200 news messages extracted from Yahoo!'s business and technology news feeds.  
SPEEDのスループットは、Yahoo!のビジネスおよびテクノロジーニュースフィードから抽出された200のニュースメッセージのコーパスでベンチマークされます。

**Ablation, explainability, and parameter studies**: Many recent papers also include ablation studies, explainability studies, and parameter and sensitivity studies.  
**アブレーション、説明可能性、およびパラメータ研究**: 最近の多くの論文には、アブレーション研究、説明可能性研究、およびパラメータと感度の研究も含まれています。

A common theme is that they all use deep or other machine learning techniques.  
共通のテーマは、すべてが深層または他の機械学習技術を使用していることです。

**Industrial testing**: A few papers present case studies or experience reports from industry.  
**産業テスト**: いくつかの論文は、業界からのケーススタディや経験報告を提示しています。

We have already mentioned the commercial VLX-Stories system.  
私たちはすでに商業用のVLX-Storiesシステムに言及しました。

Mannens et al. extend the news production workflow at VRT (Vlaamse Radio- en Televisieomroep), a national Belgian broadcaster, to support personalised news recommendation and dissemination via RSS feeds.  
マンネンスらは、ベルギーの国営放送局VRT（フラームスラジオ・テレビジョン）のニュース制作ワークフローを拡張し、RSSフィードを介したパーソナライズされたニュース推薦と配信をサポートします。

A semantic version of the IPTC's NewsML-G2 standard is proposed as a unifying (meta-)data model for dynamic distributed news event information.  
IPTCのNewsML-G2標準のセマンティックバージョンが、動的分散ニュースイベント情報の統一（メタ）データモデルとして提案されています。

As a result, RDF/OWL and NewsML-G2 can be used in combination to automatically categorise, link, and enrich news-event metadata.  
その結果、RDF/OWLとNewsML-G2は組み合わせて使用することで、ニュースイベントメタデータを自動的に分類、リンク、および強化することができます。

The system has been hooked into the VRT's workflow engine, facilitating automatic recommendation of developing news stories to individual news users.  
このシステムはVRTのワークフローエンジンに接続され、個々のニュースユーザーに対して発展中のニュースストーリーの自動推薦を促進します。

Tamilin et al. semantically enrich the content of archival news texts.  
タミリンらは、アーカイブニューステキストの内容を意味的に強化します。

The proposed system identifies mentions of named entities along with their contexts; links the contextualised mentions to entities in a knowledge base; and uses the links to retrieve further relevant information from the knowledge base.  
提案されたシステムは、名前付きエンティティの言及とその文脈を特定し、文脈化された言及を知識ベースのエンティティにリンクし、そのリンクを使用して知識ベースからさらに関連情報を取得します。

The system has been deployed and applied to 10 years of archival news in a local Italian newspaper.  
このシステムは、地元のイタリアの新聞の10年間のアーカイブニュースに展開され、適用されています。

And as already mentioned, a prototype of the NEWS system has run experimentally at EFE, alongside their legacy production system, introducing a semi-automatic workflow that lets journalists validate the annotations suggested by the system.  
そしてすでに述べたように、NEWSシステムのプロトタイプは、彼らのレガシー生産システムと並行してEFEで実験的に稼働し、ジャーナリストがシステムによって提案された注釈を検証できる半自動ワークフローを導入しています。

**Case studies and examples**: Other papers present realistic examples based on industrial experience.  
**ケーススタディと例**: 他の論文は、産業経験に基づいた現実的な例を提示しています。

For example, the MediaLoep project discusses how to improve retrieval and increase reuse of previously broadcast multimedia news items at VRT, the national Belgian broadcaster, both as background information and as reusable footage.  
例えば、MediaLoepプロジェクトは、ベルギーの国営放送局VRTで以前に放送されたマルチメディアニュースアイテムの検索を改善し、再利用を増やす方法について論じています。

The paper reports experiences with collecting descriptive metadata from different news production systems; integrating the metadata using a semantic data model; and connecting the data model to other semantic data sets to enable more powerful semantic search.  
この論文は、異なるニュース制作システムからの記述メタデータの収集、セマンティックデータモデルを使用したメタデータの統合、およびデータモデルを他のセマンティックデータセットに接続してより強力なセマンティック検索を可能にする経験を報告しています。

**Proof-of-concept demonstrations and use cases**: Similar types of qualitative evaluations, but with less focus in industrial-scale examples, are proof-of-concept demonstrations and hypothetical use cases.  
**概念実証デモとユースケース**: 同様のタイプの定性的評価ですが、産業規模の例にあまり焦点を当てていないのが概念実証デモと仮想ユースケースです。

**User studies**: A final group of papers presents user studies and usability tests.  
**ユーザー研究**: 最後のグループの論文は、ユーザー研究とユーザビリティテストを提示しています。

Yokoo et al. represent news articles as small knowledge graphs enriched with word similarities from WordNet.  
横尾らは、ニュース記事をWordNetからの単語の類似性で強化された小さな知識グラフとして表現します。

Overlaps between the sub-graphs of new articles and of articles a user has found interesting in the past are used to recommend new articles to the user.  
新しい記事のサブグラフと、ユーザーが過去に興味を持った記事のサブグラフとの重複を使用して、ユーザーに新しい記事を推薦します。

Sub-graphs are compared using Jaccard similarity.  
サブグラフはジャッカール類似度を使用して比較されます。

The approach is evaluated on a collection of Japanese news articles.  
このアプローチは、日本のニュース記事のコレクションで評価されます。

Twenty users were asked to rate suggested articles in terms of relevance and of interest, breaking the latter down into curiosity and serendipity.  
20人のユーザーに、提案された記事の関連性と興味について評価するよう求められ、後者は好奇心と偶然性に分けられました。

**Summary**: Our review shows that experimental evaluation of proposed pipelines/prototypes is the most used research method.  
**要約**: 私たちのレビューは、提案されたパイプライン/プロトタイプの実験的評価が最も使用されている研究方法であることを示しています。

Experiments most often use information retrieval measures, but usability and performance measures are also employed.  
実験は最も頻繁に情報検索指標を使用しますが、ユーザビリティとパフォーマンス指標も使用されます。

In recent years, experiments are increasingly often supplemented by studies of ablation, explainability, and parameter selection.  
近年、実験はアブレーション、説明可能性、およびパラメータ選択の研究によってますます補完されています。

Other used research methods are industrial testing, case studies and examples, proof-of-concept demos, use cases, and user studies.  
他に使用される研究方法には、産業テスト、ケーススタディと例、概念実証デモ、ユースケース、ユーザー研究があります。

### 3.3. Intended Users  
### 3.3. 対象ユーザー

**News users**: More than half the main papers aim to offer news services to the general public.  
**ニュースユーザー**: 主要な論文の半数以上は、一般の人々にニュースサービスを提供することを目指しています。

An early example is Rich News, a system that automatically transcribes and segments radio and TV streams.  
初期の例はRich Newsで、これはラジオとテレビのストリームを自動的に転写し、セグメント化するシステムです。

Key phrases extracted from each segment are used to retrieve web pages that report the same news event.  
各セグメントから抽出されたキーフレーズは、同じニュースイベントを報告するウェブページを取得するために使用されます。



. Key phrases extracted from each segment are used to retrieve web pages that report the same news event. 
各セグメントから抽出されたキーフレーズは、同じニュースイベントを報告するウェブページを取得するために使用されます。

The web pages are annotated semantically using the KIM platform, whose web interface is used to support searching and browsing news stories semantically by topic and playing the corresponding segments of the associated media files.  
ウェブページはKIMプラットフォームを使用して意味的に注釈が付けられ、そのウェブインターフェースは、トピックごとにニュースストーリーを意味的に検索および閲覧し、関連するメディアファイルの対応するセグメントを再生することをサポートします。

**Journalists, newsrooms, and news agencies**: The second largest group of papers aims to support journalists and other professionals in newsrooms and news agencies.  
**ジャーナリスト、ニュースルーム、ニュースエージェンシー**: 第二の大きなグループの論文は、ジャーナリストやニュースルーム、ニュースエージェンシーの他の専門家を支援することを目的としています。

Several projects mentioned already belong to this type, including the NEWS project.  
すでに言及された複数のプロジェクトは、このタイプに属しており、NEWSプロジェクトが含まれます。

The proposals in MediaLoep, EEOK, Ponza et al., and Troncy also target journalists and other news professionals.  
MediaLoep、EEOK、Ponzaら、Troncyの提案もジャーナリストや他のニュース専門家を対象としています。

The ambition of the News Angler project is to enable automatic detection of newsworthy events from a dynamically evolving knowledge graph by representing news angles, such as "proximity," "nepotism," or "fall from grace," formally using Common Logic.  
News Anglerプロジェクトの野望は、「近接」、「縁故主義」、「失脚」などのニュースの角度をCommon Logicを使用して正式に表現することにより、動的に進化する知識グラフからニュース価値のあるイベントを自動的に検出できるようにすることです。

**Knowledge-base maintainers**: Rather than supporting news users directly, some papers support knowledge-base maintainers on a technical level.  
**知識ベースの管理者**: ニュースユーザーを直接支援するのではなく、一部の論文は技術的なレベルで知識ベースの管理者を支援します。

For example, Fernández et al. present a plugin for maintaining the NEWS ontology.  
例えば、FernándezらはNEWSオントロジーを維持するためのプラグインを提示しています。

Aethalides extends the Hermes framework with a pipeline for semantic classification using concepts defined in a domain ontology.  
Aethalidesは、ドメインオントロジーで定義された概念を使用して意味的分類のためのパイプラインを持つHermesフレームワークを拡張します。

**Archivists**: A smaller group of papers targets archivists, who maintain knowledge bases on the content level.  
**アーカイビスト**: より小さなグループの論文は、コンテンツレベルで知識ベースを維持するアーカイビストを対象としています。

For example, Neptuno is an early semantic newspaper archive system that aims to give archivists and reporters richer ways to describe and annotate news materials and to give reporters and news readers better search and browsing capabilities.  
例えば、Neptunoは、アーカイビストや記者にニュース資料を記述し注釈を付けるためのより豊かな方法を提供し、記者やニュース読者により良い検索および閲覧機能を提供することを目的とした初期の意味的新聞アーカイブシステムです。

It uses an ontology for classifying archive content along with modules for semantic search, browsing, and visualisation.  
それは、アーカイブコンテンツを分類するためのオントロジーと、意味的検索、閲覧、視覚化のためのモジュールを使用します。

The purpose of the formal model for belief-base revision is also to maintain knowledge bases by detecting and resolving inconsistencies.  
信念ベースの改訂のための形式モデルの目的は、不整合を検出し解決することによって知識ベースを維持することでもあります。

**Fake-news detectors and fact checkers**: Several recent papers focus on supporting fake-news detectors and fact checkers.  
**フェイクニュース検出器とファクトチェッカー**: 最近のいくつかの論文は、フェイクニュース検出器とファクトチェッカーを支援することに焦点を当てています。

We have already mentioned Deep Triple Networks (DTN).  
私たちはすでにDeep Triple Networks (DTN)について言及しました。

Brașoveanu and Andonie detect fake news through a hybrid approach that assesses sentiments, entities, and facts extracted from news texts.  
BrașoveanuとAndonieは、ニューステキストから抽出された感情、エンティティ、および事実を評価するハイブリッドアプローチを通じてフェイクニュースを検出します。

ClaimsKG, the large knowledge graph of French political tweets, can be used to trace how knowledge—along with misinformation and hearsay—is propagated over time.  
フランスの政治ツイートの大規模な知識グラフであるClaimsKGは、知識がどのように誤情報や噂とともに時間の経過とともに広がるかを追跡するために使用できます。

Several of the recent deep-NN approaches we will present later also target fake-news detection and fact checking.  
後で紹介する最近のいくつかの深層ニューラルネットワークアプローチもフェイクニュース検出とファクトチェックを対象としています。

**Knowledge workers**: A smaller group of papers targets general knowledge workers and information professionals outside the news profession.  
**知識労働者**: より小さなグループの論文は、ニュース専門職の外にいる一般的な知識労働者や情報専門家を対象としています。

For example, KIM aims to improve news browsing and searching for knowledge workers in general.  
例えば、KIMは一般的な知識労働者のためにニュースの閲覧と検索を改善することを目指しています。

Other papers aim to support specific information professions.  
他の論文は特定の情報専門職を支援することを目指しています。

The Automatic Georeferencing Video (AGV) pipeline makes news videos from the RAI archives available for geography education.  
Automatic Georeferencing Video (AGV)パイプラインは、RAIアーカイブからのニュースビデオを地理教育のために利用可能にします。

Audio is extracted from video using ffmpeg and transcribed using Ants.  
音声はffmpegを使用してビデオから抽出され、Antsを使用して文字起こしされます。

Apache OpenNLP is used to extract named entities mentioned in the video segment.  
Apache OpenNLPは、ビデオセグメントで言及された固有名詞を抽出するために使用されます。

Google's Knowledge Graph is used to add representative images and facts about related people and places.  
GoogleのKnowledge Graphは、関連する人々や場所に関する代表的な画像や事実を追加するために使用されます。

The places are in turn used to make the videos and their metadata available through Google Street Map-based user interfaces.  
その場所は、Google Street Mapベースのユーザーインターフェースを通じてビデオとそのメタデータを利用可能にするために使用されます。

The pipeline is tested on a dataset of 10-minute excerpts from 6,600 videos from a thematic RAI newscast (Leonardo TGR).  
このパイプラインは、テーマ別のRAIニュース放送（Leonardo TGR）からの6,600本のビデオの10分間の抜粋のデータセットでテストされています。

AnnoTerra uses ontologies and semantic search to improve NASA's earth-science news feeds, targeting both experts and inexperienced users of earth-science data.  
AnnoTerraは、オントロジーと意味的検索を使用してNASAの地球科学ニュースフィードを改善し、専門家と地球科学データの未経験のユーザーの両方を対象としています。

CrimeBase uses rules to extract entities from text and associated image captions in multimodal crime-related online news.  
CrimeBaseは、マルチモーダルな犯罪関連のオンラインニュースにおけるテキストと関連する画像キャプションからエンティティを抽出するためのルールを使用します。

The extracted entities are correlated using contextual and semantic similarity measures, whereas image entities are correlated using image features.  
抽出されたエンティティは、文脈的および意味的類似性測定を使用して相関付けられ、一方で画像エンティティは画像特徴を使用して相関付けられます。

The resulting knowledge base uses an OWL ontology to integrate crime-related information from popular Indian online newspapers.  
結果として得られた知識ベースは、人気のあるインドのオンライン新聞からの犯罪関連情報を統合するためにOWLオントロジーを使用します。

Other main papers target professionals in domains such as economy and finance, environmental communication, and medicine.  
他の主要な論文は、経済や金融、環境コミュニケーション、医学などの分野の専門家を対象としています。

**Summary**: Our review indicates that the most frequently intended users (or beneficiaries) of the main-paper proposals are general news users and journalists.  
**要約**: 私たちのレビューは、主要な論文の提案の最も頻繁に意図されたユーザー（または受益者）が一般のニュースユーザーとジャーナリストであることを示しています。

Other intended users/beneficiaries are newsrooms, knowledge-base maintainers, archivists, fake-news detectors and fact checkers, and different types of knowledge workers.  
他の意図されたユーザー/受益者は、ニュースルーム、知識ベースの管理者、アーカイビスト、フェイクニュース検出器とファクトチェッカー、さまざまな種類の知識労働者です。

### 3.4. Tasks  
### 3.4. タスク

The main papers target a wide range of news production, dissemination, and consumption activities, such as search, recommendation, categorisation, and event detection.  
主要な論文は、検索、推薦、分類、イベント検出など、ニュースの制作、普及、消費活動の幅広い範囲を対象としています。

**Semantic annotation**: Many of the earliest approaches focus on adding semantic labels to entities and topics mentioned in published news texts.  
**意味的注釈**: 初期のアプローチの多くは、公開されたニューステキストで言及されたエンティティやトピックに意味的ラベルを追加することに焦点を当てています。

We have already introduced KIM, which labels named entities found in news items with links to instances in a knowledge base and to classes defined in the KIM Ontology (KIMO).  
私たちはすでにKIMを紹介しました。これは、ニュース項目で見つかった固有名詞に知識ベースのインスタンスやKIMオントロジー（KIMO）で定義されたクラスへのリンクを付けてラベルを付けます。

We have also introduced NEWS, which annotates news items with named entities linked to external sources such as Wikipedia, ISO country codes, NASDAQ company codes, the CIA World Factbook, and SUMO/MILO.  
私たちはまた、Wikipedia、ISO国コード、NASDAQ会社コード、CIA World Factbook、SUMO/MILOなどの外部ソースにリンクされた固有名詞でニュース項目に注釈を付けるNEWSも紹介しました。

It also categorises the news items by content and represents news metadata using standards and vocabularies such as the Dublin Core (DC) vocabulary, the IPTC's News Codes, the News Industry Text Format (NITF), NewsML, and PRISM—the Publishing Requirements for Industry Standard Metadata.  
それはまた、ニュース項目をコンテンツによって分類し、Dublin Core (DC)語彙、IPTCのニュースコード、ニュース業界テキストフォーマット（NITF）、NewsML、PRISM（業界標準メタデータの出版要件）などの標準と語彙を使用してニュースメタデータを表現します。

**Enrichment**: A smaller group of papers instead focuses on enriching annotated news items with Linked Open Data or information from other semantically labelled sources.  
**エンリッチメント**: より小さなグループの論文は、代わりに注釈付きニュース項目をLinked Open Dataや他の意味的にラベル付けされたソースからの情報で豊かにすることに焦点を当てています。

For example, Antonini et al. extend the life of TV content by integrating heterogeneous data from sources such as broadcast archives, newspapers, blogs, social media, and encyclopedia and by aligning semantic content metadata with the users' evolving interests.  
例えば、Antoniniらは、放送アーカイブ、新聞、ブログ、ソーシャルメディア、百科事典などのソースからの異種データを統合し、ユーザーの進化する興味に合わせて意味的コンテンツメタデータを整合させることによって、TVコンテンツの寿命を延ばします。

AGV annotates TV news programs with geographical entities to make archival video content available through a map-based user interface for educational purposes.  
AGVは、教育目的のために地図ベースのユーザーインターフェースを通じてアーカイブビデオコンテンツを利用可能にするために、地理的エンティティでTVニュースプログラムに注釈を付けます。

In addition to representing the IPTC News Codes using SKOS, Troncy discusses how multimedia news metadata can be augmented using natural-language and multimedia analysis techniques and enriched with Linked Data, such as facts from DBpedia and GeoNames.  
Troncyは、SKOSを使用してIPTCニュースコードを表現することに加えて、マルチメディアニュースメタデータが自然言語およびマルチメディア分析技術を使用してどのように拡張され、DBpediaやGeoNamesからの事実などのLinked Dataで豊かにされるかについて議論します。

Contributions that represent news texts as sub-graphs of open KGs such as Wikidata (e.g., CAGE, KOPRA, and NewsLink) can also be considered enrichment approaches.  
ニューステキストをWikidata（例：CAGE、KOPRA、NewsLink）などのオープンKGのサブグラフとして表現する貢献もエンリッチメントアプローチと見なすことができます。

**Content retrieval**: Other papers use semantic annotations (or "semantic footprints") to support on-demand ("pull") or proactive ("push") dissemination of news content.  
**コンテンツ取得**: 他の論文は、意味的注釈（または「意味的フットプリント」）を使用して、オンデマンド（「プル」）またはプロアクティブ（「プッシュ」）なニュースコンテンツの普及をサポートします。

On the retrieval (on-demand, pull) side, a clear majority of the main papers support tasks such as searching for and otherwise retrieving news items.  
取得（オンデマンド、プル）側では、主要な論文の明らかな多数がニュース項目を検索したり、その他の方法で取得したりするタスクをサポートしています。

Projects such as KIM, NEWS, and Hermes all have content provision as central tasks.  
KIM、NEWS、Hermesなどのプロジェクトは、すべてコンテンツ提供を中心的なタスクとしています。

The Hermes Graphical Query Language (HGQL) makes it simpler for non-expert users to search semantically for content available in the Hermes framework.  
Hermes Graphical Query Language (HGQL)は、非専門家のユーザーがHermesフレームワークで利用可能なコンテンツを意味的に検索するのを簡単にします。

It is based on RDF-GL, a SPARQL-based graphical query language for RDF, and also provides an algorithm for ranking search results.  
これは、RDFのためのSPARQLベースのグラフィカルクエリ言語であるRDF-GLに基づいており、検索結果をランク付けするためのアルゴリズムも提供します。

The World News Finder uses a World News Ontology along with heuristic rules to automatically create metadata files from HTML news documents to support semantic user queries.  
World News Finderは、ヒューリスティックルールとともにWorld News Ontologyを使用して、HTMLニュース文書からメタデータファイルを自動的に作成し、意味的ユーザークエリをサポートします。

The aim of NewsLink is to support more robust as well as explainable query answering.  
NewsLinkの目的は、より堅牢で説明可能なクエリ応答をサポートすることです。

**Content provision**: On the provision (proactive, push) side, another large group of papers focuses on actively propagating news to users.  
**コンテンツ提供**: 提供（プロアクティブ、プッシュ）側では、別の大きなグループの論文がユーザーにニュースを積極的に伝播させることに焦点を当てています。

For example, Joseph and Jiang aim to provide more accurate content-based recommendations.  
例えば、JosephとJiangは、より正確なコンテンツベースの推薦を提供することを目指しています。

They use existing tools for entity discovery and linking to represent news messages as sub-graphs by adding edges from Freebase.  
彼らは、エンティティ発見とリンクのための既存のツールを使用して、Freebaseからのエッジを追加することによってニュースメッセージをサブグラフとして表現します。

A new human-annotated data set (CNREC) for evaluating content-based news recommendation systems is made available and used to evaluate the approach.  
コンテンツベースのニュース推薦システムを評価するための新しい人間注釈付きデータセット（CNREC）が利用可能になり、アプローチの評価に使用されます。

Cantador et al. aim to deal with data sparsity and cold-start issues in news recommender systems.  
Cantadorらは、ニュース推薦システムにおけるデータの希薄性とコールドスタートの問題に対処することを目指しています。

They enrich semantic representations of news items and of users with Linked Data to provide more input to recommendation algorithms.  
彼らは、推薦アルゴリズムにより多くの入力を提供するために、ニュース項目とユーザーの意味的表現をLinked Dataで豊かにします。

Focusing on the user-profiling (or personalisation) side of news recommendation, Hopfgartner and Jose use semantic annotations of news videos to profile users' evolving information needs and interests to recommend the most suitable news stories.  
ニュース推薦のユーザープロファイリング（またはパーソナライズ）側に焦点を当てて、HopfgartnerとJoseはニュースビデオの意味的注釈を使用して、ユーザーの進化する情報ニーズと興味をプロファイルし、最も適切なニュースストーリーを推薦します。

Context-Aware Graph Embedding (CAGE) focuses on providing session-based recommendations, whereas KOPRA aims to take both users' short- and long-term behaviours into account.  
Context-Aware Graph Embedding (CAGE)はセッションベースの推薦を提供することに焦点を当てており、KOPRAはユーザーの短期的および長期的な行動の両方を考慮することを目指しています。

**Event detection**: Several more recent approaches go beyond semantic labelling and enrichment of news content, attempting to extract events or relations (triples, facts) from news items to represent their meaning on a fine-grained level.  
**イベント検出**: 最近のいくつかのアプローチは、ニュースコンテンツの意味的ラベリングとエンリッチメントを超えて、ニュース項目からイベントや関係（トリプル、事実）を抽出し、それらの意味を詳細に表現しようとしています。

NewsReader is a cross-lingual system (or "reading machine") that is designed to ingest high volumes of news articles and represent them as Event-Centric Knowledge Graphs (ECKGs).  
NewsReaderは、高ボリュームのニュース記事を取り込み、イベント中心の知識グラフ（ECKG）として表現するように設計されたクロスリンガルシステム（または「リーディングマシン」）です。

Each graph describes an event, and perhaps how it develops over time, along with the actors and other entities involved in the event.  
各グラフは、イベントを説明し、場合によってはそれが時間の経過とともにどのように発展するか、イベントに関与するアクターや他のエンティティとともに説明します。

The graphs are connected through shared entities and temporal overlaps, and the entities are linked to background information in knowledge bases such as DBpedia.  
グラフは共有エンティティと時間的重複を通じて接続され、エンティティはDBpediaなどの知識ベースの背景情報にリンクされています。

The ASRAEL project maps events described in unstructured news articles to structured event representations in Wikidata, which are used to enrich the representations of the articles.  
ASRAELプロジェクトは、非構造化ニュース記事で説明されたイベントをWikidataの構造化イベント表現にマッピングし、これを使用して記事の表現を豊かにします。

Because Wikidata's event hierarchy is considered too fine-grained for use in search engines, a hierarchical clustering step follows, after which the more coarsely categorised events are made available for querying and navigation through an event-oriented knowledge graph.  
Wikidataのイベント階層は検索エンジンでの使用には細かすぎると考えられているため、階層的クラスタリングステップが続き、その後、より粗く分類されたイベントがクエリとナビゲーションのためにイベント指向の知識グラフを通じて利用可能になります。

To keep the Hermes knowledge base up to date, Schouten et al. represent lexico-semantic patterns and associated actions as rules that are used to semi-automatically detect and semantically describe news events.  
Hermes知識ベースを最新の状態に保つために、Schoutenらは、語彙意味的パターンと関連するアクションをルールとして表現し、これを使用してニュースイベントを半自動的に検出し、意味的に記述します。



. represent lexico-semantic patterns and associated actions as rules that are used to semi-automatically detect and semantically describe news events. 
レキシコ・セマンティックパターンと関連するアクションをルールとして表現し、ニュースイベントを半自動的に検出し、意味的に記述するために使用します。

The approach is implemented in the Hermes News Portal (HNP), a realisation of the Hermes framework that lets news users browse and query for relevant news items. 
このアプローチは、ニュースユーザーが関連するニュースアイテムをブラウズし、クエリを実行できるHermesフレームワークの実現であるHermes News Portal (HNP)に実装されています。

The Evolutionary Event Ontology Knowledge (EEOK) ontology aims to support event detection by suggesting which event types to look for next in a developing storyline. 
進化的イベントオントロジー知識（EEOK）オントロジーは、発展中のストーリーラインで次に探すべきイベントタイプを提案することによって、イベント検出をサポートすることを目的としています。

Kuzey et al. identify and reconcile named events from news articles and represent them in a semantic knowledge graph according to textual contents, entities, and temporal ordering. 
Kuzeyらは、ニュース記事から命名されたイベントを特定し、調整し、テキストの内容、エンティティ、および時間的順序に従ってセマンティックナレッジグラフに表現します。

The commercial tool VLX-Stories also detects events in media feeds.  
商業ツールVLX-Storiesもメディアフィード内のイベントを検出します。

**Relation extraction**: Other papers instead focus on relation extraction, detecting triples (or facts) that can be used to build new or update existing RDF graphs. 
**関係抽出**: 他の論文は、関係抽出に焦点を当て、新しいRDFグラフを構築したり、既存のグラフを更新したりするために使用できるトリプル（または事実）を検出します。

An early proposal for deeper text analysis is SemNews, which extracts textual-meaning representations (TMRs) from RSS news items using the OntoSem tool, which represents each text as a set of facts about: which actions that are described in the text; which agents, locations, and themes each action involves; and any temporal relations between the actions. 
より深いテキスト分析の初期提案はSemNewsであり、これはOntoSemツールを使用してRSSニュースアイテムからテキスト意味表現（TMR）を抽出します。このツールは、各テキストを次のような事実のセットとして表現します: テキストで説明されているアクション、各アクションに関与するエージェント、場所、テーマ、およびアクション間の時間的関係。

The SemNews tool transforms the TMRs into OWL to support semantic searching, browsing, and indexing of RSS news items. 
SemNewsツールは、TMRをOWLに変換して、RSSニュースアイテムのセマンティック検索、ブラウジング、およびインデックス作成をサポートします。

It also powers an experimental web service that provides semantically annotated news items along with news summaries to human users. 
また、セマンティックに注釈付けされたニュースアイテムとニュース要約を人間のユーザーに提供する実験的なウェブサービスを支えています。

BKSport automatically annotates sports news using language-pattern rules in combination with a domain ontology and a knowledge base built on top of the KIM platform. 
BKSportは、KIMプラットフォームの上に構築されたドメインオントロジーとナレッジベースと組み合わせて、言語パターンルールを使用してスポーツニュースに自動的に注釈を付けます。

The tool extracts links and typed entities as well as semantic relations between them. 
このツールは、リンクと型付きエンティティ、およびそれらの間のセマンティック関係を抽出します。

It also uses pronoun recognition to resolve co-references. 
また、代名詞認識を使用して共参照を解決します。

Prasojo et al. represent the sentences in a news item as triples, analysing not only top-level but also subordinate clauses. 
Prasojoらは、ニュースアイテム内の文をトリプルとして表現し、トップレベルだけでなく従属節も分析します。

The triples are run through a pipeline of natural language tools that fuse and prioritise them. 
トリプルは、融合し優先順位を付ける自然言語ツールのパイプラインを通じて処理されます。

Finally, selected triples are used to summarise the underlying event reported in the news item. 
最後に、選択されたトリプルは、ニュースアイテムで報告された基礎となるイベントを要約するために使用されます。

Färber et al. identify novel statements in the news, building on ClausIE and DBpedia to propose a semantic novelty measure that takes individual user-relevance into account. 
Färberらは、ClausIEとDBpediaに基づいてニュース内の新しい声明を特定し、個々のユーザー関連性を考慮に入れたセマンティックな新規性測定を提案します。

**Sub-graph extraction**: An alternative to extracting relations from news texts is to represent texts by sub-graphs extracted from open knowledge graphs. 
**サブグラフ抽出**: ニューステキストから関係を抽出する代替手段は、オープンナレッジグラフから抽出されたサブグラフによってテキストを表現することです。

An early example is Joseph and Jiang, which uses standard techniques to discover and link entities and adds edges from Freebase to represent news messages as sub-graphs to support content-based news recommendation. 
初期の例はJosephとJiangであり、これは標準技術を使用してエンティティを発見しリンクし、Freebaseからエッジを追加してニュースメッセージをサブグラフとして表現し、コンテンツベースのニュース推薦をサポートします。

AnchorKG represents news articles as small anchor graphs, which consist of entities that are prominently mentioned in the news text, along with relations between those entities taken from an open knowledge graph, and along with those entities' k-hop neighbourhoods in the graph. 
AnchorKGは、ニュース記事を小さなアンカーグラフとして表現し、これはニューステキストで顕著に言及されるエンティティと、オープンナレッジグラフから取得したそれらのエンティティ間の関係、およびグラフ内のそれらのエンティティのk-hop近傍で構成されます。

One aim is to improve news recommendation by making real-time knowledge reasoning scalable to large open knowledge graphs. 
1つの目的は、リアルタイムの知識推論を大規模なオープンナレッジグラフにスケーラブルにすることによってニュース推薦を改善することです。

Another aim is to support explainable reasoning about similarity. 
もう1つの目的は、類似性に関する説明可能な推論をサポートすることです。

Reinforcement learning is used to train an anchor-graph extractor jointly with a news recommender, using already recognised and linked named entities as inputs. 
強化学習は、すでに認識されリンクされた命名エンティティを入力として使用し、ニュース推薦者と共同でアンカーグラフ抽出器を訓練するために使用されます。

The approach is evaluated using the MIND dataset and a private dataset extracted from Bing News with Wikidata as reference graph. 
このアプローチは、MINDデータセットとWikidataを参照グラフとして使用してBing Newsから抽出されたプライベートデータセットを使用して評価されます。

CAGE represents news texts as sub-graphs extracted from an open reference knowledge graph to support session-based news recommendation. 
CAGEは、セッションベースのニュース推薦をサポートするために、オープンリファレンスナレッジグラフから抽出されたサブグラフとしてニューステキストを表現します。

KOPRA extracts an entity graph (called interest graph) for each user from seed entities that are mentioned in the news titles and abstracts in the user's short- and long-term click histories. 
KOPRAは、ユーザーの短期および長期のクリック履歴におけるニュースのタイトルと要約に言及されているシードエンティティから、各ユーザーのためにエンティティグラフ（興味グラフと呼ばれる）を抽出します。

NewsLink represents both news articles and user queries as small KGs that can be compared for similarity. 
NewsLinkは、ニュース記事とユーザーのクエリの両方を、小さなKGとして表現し、類似性を比較できるようにします。

**KG updating**: Several recent contributions use deep and other machine-learning techniques to keep evolving knowledge graphs up-to-date by identifying new (emerging, dark) entities and new (or emerging) relations between (the new or existing) entities. 
**KGの更新**: 最近のいくつかの貢献は、深層学習やその他の機械学習技術を使用して、新しい（出現する、暗い）エンティティと（新しいまたは出現する）エンティティ間の新しい関係を特定することによって、進化するナレッジグラフを最新の状態に保ちます。

We have already mentioned HEER. 
私たちはすでにHEERについて言及しました。

PolarisX automatically expands language-independent knowledge graphs in real time with representations of new events reported by news sites and on social media. 
PolarisXは、ニュースサイトやソーシャルメディアで報告された新しいイベントの表現を使用して、リアルタイムで言語に依存しないナレッジグラフを自動的に拡張します。

It uses a relation extraction model based on pre-trained multilingual BERT to detect new relations. 
それは、新しい関係を検出するために、事前に訓練された多言語BERTに基づく関係抽出モデルを使用します。

Challenges addressed are that available reference knowledge graphs have limited size and scope and that existing techniques are not able to deal with neologisms based on human common sense. 
対処される課題は、利用可能な参照ナレッジグラフがサイズと範囲に制限があり、既存の技術が人間の常識に基づく新語に対処できないことです。

Text-Aware MUlti-RElational learning method (TAMURE) also extends a knowledge graph with relations that emerge in the news. 
テキスト対応のマルチ関係学習法（TAMURE）も、ニュースで出現する関係を持つナレッジグラフを拡張します。

It addresses the source heterogeneity of structured knowledge graphs and unstructured news texts by learning joint embeddings of entities, relations, and texts using tensor factorisation implemented in TensorFlow. 
それは、TensorFlowで実装されたテンソル分解を使用して、エンティティ、関係、およびテキストの共同埋め込みを学習することによって、構造化されたナレッジグラフと非構造化ニューステキストのソースの異質性に対処します。

TAMURE is linear in the number of parameters, making it suitable for large-scale KGs and live news streams. 
TAMUREはパラメータの数に対して線形であり、大規模なKGやライブニュースストリームに適しています。

Sagi et al. empirically investigate the prevalence of entities in online news feeds that cannot be identified by DBpedia Spotlight or by Google's Knowledge Graph API. 
Sagiらは、DBpedia SpotlightやGoogleのKnowledge Graph APIによって特定できないオンラインニュースフィード内のエンティティの普及を実証的に調査します。

Out of 13,456 named entities in an RSS sample, 378 were missing from DBpedia, 488 were missing from Google's Knowledge Graph, and 297 were missing from both. 
RSSサンプル内の13,456の命名エンティティのうち、378はDBpediaに欠け、488はGoogleのKnowledge Graphに欠け、297は両方に欠けていました。

**Ontology development**: In various ways, several main papers support ontology development. 
**オントロジー開発**: 様々な方法で、いくつかの主要な論文がオントロジー開発をサポートしています。

Early projects such as KIM and NEWS focus on developing new domain ontologies, whereas KIM integrates existing IPTC standards and vocabularies into the LOD cloud. 
KIMやNEWSのような初期プロジェクトは新しいドメインオントロジーの開発に焦点を当てているのに対し、KIMは既存のIPTC標準と語彙をLODクラウドに統合します。

More recent efforts, such as EEOK, use machine learning techniques to automate ontology creation and maintenance. 
EEOKのような最近の取り組みは、オントロジーの作成と維持を自動化するために機械学習技術を使用します。

**Fake-news detection and fact checking**: Several recent papers focus on the detection of fake news, such as Brașoveanu and Andonie. 
**フェイクニュース検出とファクトチェック**: 最近のいくつかの論文は、BrașoveanuやAndonieのようにフェイクニュースの検出に焦点を当てています。

Another proposal is Pan et al., which uses graph embeddings of news texts to identify fake news. 
別の提案はPanらであり、ニューステキストのグラフ埋め込みを使用してフェイクニュースを特定します。

Müller-Budack et al. present a multimodal approach to quantify whether real-world news texts and their associated images represent the same or connected entities, suggesting that low coherence is a possible indicator of fake news. 
Müller-Budackらは、現実のニューステキストとそれに関連する画像が同じまたは関連するエンティティを表しているかどうかを定量化するためのマルチモーダルアプローチを提示し、低い一貫性がフェイクニュースの可能性のある指標であることを示唆しています。

Groza and Pop lift medical information from non-trusted sources into semantic form using FRED and reasons over the resulting description logic representations using Racer and HermiT. 
GrozaとPopは、FREDを使用して信頼できないソースから医療情報をセマンティック形式に変換し、RacerとHermiTを使用して得られた記述論理表現に基づいて推論します。

Reasoning inconsistencies are taken to indicate potential "medical myths" that are verbalised and presented to human agents along with an explanation of the inconsistency. 
推論の不整合は、潜在的な「医療神話」を示すものとされ、それが言語化され、不整合の説明とともに人間のエージェントに提示されます。

KLG-GAT uses an open knowledge graph to enhance fact checking and verification. 
KLG-GATは、オープンナレッジグラフを使用してファクトチェックと検証を強化します。

Constituency parsing is used to find entity mentions in the claims, which are used to retrieve relevant Wikipedia articles as potential evidence. 
構文解析は、主張内のエンティティの言及を見つけるために使用され、それが関連するWikipedia記事を潜在的な証拠として取得するために使用されます。

A BERT-based sentence retrieval model is then used to select the most relevant evidence for the claim. 
次に、BERTベースの文取得モデルが主張に対して最も関連性の高い証拠を選択するために使用されます。

TagMe is used to link entities in the claims and in the evidence sentences to the Wikidata5M subset of Wikidata and extract triples whose entities are mentioned in the claim and/or evidence. 
TagMeは、主張と証拠文内のエンティティをWikidataのWikidata5Mサブセットにリンクし、主張および/または証拠に言及されているエンティティを持つトリプルを抽出するために使用されます。

The triples are further ranked using a BERT-based learning-to-rank (LTR) model. 
トリプルは、BERTベースの学習ランキング（LTR）モデルを使用してさらにランク付けされます。

High-ranked triples are used to construct a graph of the central claim, its potential evidence sentences, and triples that connect the claim to the evidence sentences. 
高ランクのトリプルは、中央の主張、その潜在的な証拠文、および主張を証拠文に接続するトリプルのグラフを構築するために使用されます。

A two-level multi-head graph attention network is used to propagate information between the claim, evidence, and knowledge (triple) nodes in the graph as input to a claim classification layer. 
二層のマルチヘッドグラフアテンションネットワークが、主張、証拠、およびナレッジ（トリプル）ノード間で情報を伝播させるために使用され、主張分類層への入力となります。

**Content generation**: Targeting news content generation, Tweet2News extracts RDF triples from documentary (headline-like) tweets using the IPTC's rNews vocabulary, organises them into storylines, and enriches them with Linked Open Data to facilitate news generation in addition to retrieval. 
**コンテンツ生成**: ニュースコンテンツ生成をターゲットにしたTweet2Newsは、IPTCのrNews語彙を使用してドキュメンタリー（見出しのような）ツイートからRDFトリプルを抽出し、それらをストーリーラインに整理し、取得に加えてニュース生成を促進するためにLinked Open Dataで豊かにします。

The Pundit algorithm even suggests plausible future events based on descriptions of current events. 
Punditアルゴリズムは、現在のイベントの説明に基づいて、もっともらしい未来のイベントを提案します。

Structured representations of news titles are extracted from a large historical news archive that covers more than 150 years, and a machine-learning algorithm is used to extract causal relations from the structured representations. 
ニュースタイトルの構造化表現は、150年以上にわたる大規模な歴史的ニュースアーカイブから抽出され、構造化表現から因果関係を抽出するために機械学習アルゴリズムが使用されます。

Although the authors do not propose specific journalistic uses of Pundit, their algorithm might be used in newsrooms to anticipate alternative continuations of developing events. 
著者たちはPunditの特定のジャーナリズムの使用を提案していませんが、彼らのアルゴリズムはニュースルームで発展中のイベントの代替的な継続を予測するために使用されるかもしれません。

Jing et al. aim to auto-generate human-quality news image captions based on a corpus of news texts with associated images and captions. 
Jingらは、関連する画像とキャプションを持つニューステキストのコーパスに基づいて、人間品質のニュース画像キャプションを自動生成することを目指しています。

Each news image is represented as a feature vector using a pre-trained CNN, and each corresponding article text is split into sentences containing named entities that are processed further in two ways. 
各ニュース画像は、事前に訓練されたCNNを使用して特徴ベクトルとして表現され、各対応する記事テキストは、命名エンティティを含む文に分割され、さらに2つの方法で処理されます。

One line of analysis enriches the sentences and entities with related information from DBpedia. 
1つの分析ラインは、DBpediaからの関連情報で文とエンティティを豊かにします。

Another line instead replaces the named entities with type placeholders, such as PERSON, NORP, LOC, ORG, and GPE, producing generic sentences that are compressed using dependency parsing and represented as TF-IDF weighted bags-of-words. 
別のラインは、命名エンティティをPERSON、NORP、LOC、ORG、GPEなどの型プレースホルダーに置き換え、依存関係解析を使用して圧縮された一般的な文を生成し、TF-IDF加重のバッグオブワーズとして表現します。

Correlations are then established between the generic-sentence representations and the features of the associated images in the corpus. 
次に、一般的な文の表現とコーパス内の関連画像の特徴との間に相関関係が確立されます。

An LSTM model is trained to generate matching caption templates for images on top of the pre-trained CNN. 
LSTMモデルは、事前に訓練されたCNNの上に画像に対して一致するキャプションテンプレートを生成するために訓練されます。

Finally, the semantically enriched original sentences are used to fill in individual entities for the type placeholders. 
最後に、意味的に豊かにされた元の文が、型プレースホルダーの個々のエンティティを埋めるために使用されます。

The approach is evaluated on two public datasets, Good News (466K examples) and Breaking News (110K examples), that include news images and captions along with article texts. 
このアプローチは、ニュース画像とキャプションを含む記事テキストを持つ2つの公開データセット、Good News（466K例）とBreaking News（110K例）で評価されます。

Prasojo et al. uses the triples that have been extracted, fused, and prioritised from news sentences to generate new sentences that summarise the underlying news events. 
Prasojoらは、ニュース文から抽出され、融合され、優先順位が付けられたトリプルを使用して、基礎となるニュースイベントを要約する新しい文を生成します。

The News Angler project represents news angles to support automatic detection of newsworthy events from a knowledge graph. 
News Anglerプロジェクトは、ナレッジグラフからニュース価値のあるイベントを自動的に検出するためにニュースアングルを表現します。

**Prediction**: Prediction is the focus of a small group of papers that includes Pundit and EEOK. 
**予測**: 予測は、PunditやEEOKを含む小さなグループの論文の焦点です。



**Prediction**: Prediction is the focus of a small group of papers that includes Pundit and EEOK. 
**予測**: 予測は、PunditやEEOKを含む少数の論文の焦点です。

To predict stock prices, EKGStock uses named-entity recognition and relation extraction to represent news about Chinese enterprises as knowledge graphs. 
株価を予測するために、EKGStockは固有表現認識と関係抽出を使用して、中国企業に関するニュースを知識グラフとして表現します。

Embeddings of the enterprise-specific graphs are then used to estimate connectedness between enterprises. 
企業特有のグラフの埋め込みは、企業間の接続性を推定するために使用されます。

Sentiments of news reports that mention an enterprise are then fed into a Gated Recurrent Unit (GRU) model that predicts stock prices, not only for the mentioned enterprise, but also for its semantically related ones. 
企業に言及するニュース報道の感情は、その企業だけでなく、意味的に関連する企業の株価を予測するGated Recurrent Unit (GRU)モデルに入力されます。

Recent predictive approaches include deep-neural network-based recommendation papers, such as DKN, that are trained to predict click-through rates (CTR). 
最近の予測アプローチには、クリック率（CTR）を予測するように訓練された、DKNのような深層ニューラルネットワークに基づく推薦論文が含まれます。

**Other tasks**: In addition to these most frequent uses of knowledge graphs for news, several main papers address semantic similarity. 
**その他のタスク**: ニュースに対する知識グラフの最も一般的な使用法に加えて、いくつかの主要な論文が意味的類似性に取り組んでいます。

For example, Kasper et al. use information extraction techniques to automatically annotate news documents semantically to facilitate cross-lingual retrieval of documents with similar annotations. 
例えば、Kasperらは情報抽出技術を使用して、ニュース文書を自動的に意味的に注釈付けし、類似の注釈を持つ文書のクロスリンガル検索を容易にします。

De Nies et al. cluster semantic representations to detect how news items are derived from one another, using the PROV-O ontology to represent the results semantically. 
De Niesらは意味的表現をクラスタリングして、ニュース項目がどのように相互に派生しているかを検出し、結果を意味的に表現するためにPROV-Oオントロジーを使用します。

Supporting visualisation, the Visualizing Relations Between Objects (VRBO) framework uses semantic and statistical methods to identify temporal patterns between entities mentioned in economic news. 
可視化をサポートするために、Visualizing Relations Between Objects (VRBO)フレームワークは、経済ニュースに言及されたエンティティ間の時間的パターンを特定するために、意味的および統計的手法を使用します。

It uses the patterns to create and visualise news alerts that can be formalised and used to manage equity portfolios. 
このパターンを使用して、形式化され、株式ポートフォリオを管理するために使用できるニュースアラートを作成および可視化します。

Neptuno uses visualisation on the ontology level to show and publish how knowledge-base concepts are organised. 
Neptunoは、オントロジーレベルでの可視化を使用して、知識ベースの概念がどのように整理されているかを示し、公開します。

Archiving and general information organisation is a central task of Neptuno and several other main papers. 
アーカイブと一般的な情報の整理は、Neptunoおよびいくつかの他の主要な論文の中心的なタスクです。

Interoperability and data integration is the focus in MediaLoep. 
相互運用性とデータ統合は、MediaLoepの焦点です。

Focusing on multimedia and other metadata, García et al. also has interoperability as a central task, along with contributions such as Antonini et al., SPEED, NewsArticles, and AnnoTerra. 
マルチメディアやその他のメタデータに焦点を当てて、GarcíaらもAntoniniら、SPEED、NewsArticles、AnnoTerraなどの貢献とともに、相互運用性を中心的なタスクとしています。

**Summary**: Our review shows that the research on semantic knowledge graphs for the news support a broad variety of tasks, such as semantic annotation, enrichment, content retrieval and provision, event detection, relation and sub-graph extraction, KG updating, ontology development, fake-news detection and fact checking, content generation, and prediction. 
**要約**: 私たちのレビューは、ニュースのための意味的知識グラフに関する研究が、意味的注釈、強化、コンテンツの取得と提供、イベント検出、関係およびサブグラフの抽出、KGの更新、オントロジーの開発、フェイクニュースの検出とファクトチェック、コンテンツ生成、予測など、幅広いタスクをサポートしていることを示しています。

The past few years have seen a rapidly growing interest in KGs for fake-news identification. 
過去数年で、フェイクニュースの識別のためのKGに対する関心が急速に高まっています。

Support for factual journalism is a related area that is growing. 
事実に基づくジャーナリズムのサポートは、成長している関連分野です。

Automatic news detection is another emerging area that is becoming increasingly important. 
自動ニュース検出は、ますます重要になっている別の新興分野です。

### 3.5. Input Data  
### 3.5. 入力データ  

The proposed approaches rely on a variety of sources and types of primary input data. 
提案されたアプローチは、さまざまなソースとタイプの主要な入力データに依存しています。

Note that this section discusses the data used as input by the solutions proposed or discussed in each main paper, and not the data used for evaluation. 
このセクションでは、各主要論文で提案または議論されたソリューションによって入力として使用されるデータについて説明し、評価に使用されるデータについては言及していません。

**News articles**: The most common input data are textual news articles in digital form. 
**ニュース記事**: 最も一般的な入力データは、デジタル形式のテキストニュース記事です。

For example, Mukherjee et al. read template-based HTML pages and exploit semantic regularities in the templates to automatically annotate HTML elements with semantic labels according to their DOM paths. 
例えば、MukherjeeらはテンプレートベースのHTMLページを読み込み、テンプレート内の意味的規則性を利用して、DOMパスに従ってHTML要素に意味的ラベルを自動的に注釈付けします。

Online news articles are also used as examples and for evaluation. 
オンラインニュース記事も例として使用され、評価に利用されます。

**RSS and other news feeds**: Other main papers take their inputs via RSS feeds or other news feeds. 
**RSSおよびその他のニュースフィード**: 他の主要な論文は、RSSフィードやその他のニュースフィードを介して入力を取得します。

The Ontology-based Personalised Web-Feed Platform (OPWFP) inputs RSS news streams and uses an ontology to provide more precisely customised web feeds. 
Ontology-based Personalised Web-Feed Platform (OPWFP)は、RSSニュースストリームを入力し、オントロジーを使用してより正確にカスタマイズされたウェブフィードを提供します。

User profiles are expressed using the semantic Composite Capability/Preference Profiles (CC/PP) and FOAF vocabularies along with a domain ontology. 
ユーザープロファイルは、意味的なComposite Capability/Preference Profiles (CC/PP)およびFOAF語彙とともに、ドメインオントロジーを使用して表現されます。

The three vocabularies and ontologies are used in combination to select appropriate search topics for the RSS search engine. 
これらの3つの語彙とオントロジーは、RSS検索エンジンの適切な検索トピックを選択するために組み合わせて使用されます。

**Social media and the Web**: Several main papers use social media and other web resources as input, such as Twitter, Wikinews, Wikipedia, and regular HTML-based web sites. 
**ソーシャルメディアとウェブ**: いくつかの主要な論文は、Twitter、Wikinews、Wikipedia、通常のHTMLベースのウェブサイトなど、ソーシャルメディアやその他のウェブリソースを入力として使用します。

To support personalised news recommendation and dissemination, the extension of VRT's news workflow uses OpenID and OAuth for identification and authentication. 
パーソナライズされたニュース推薦と普及をサポートするために、VRTのニュースワークフローの拡張は、識別と認証のためにOpenIDとOAuthを使用します。

In this way, the system can compile user profiles based on data from multiple social-media accounts, using ontologies such as FOAF and SIOC to interoperate user data. 
このようにして、システムは複数のソーシャルメディアアカウントからのデータに基づいてユーザープロファイルをコンパイルでき、FOAFやSIOCなどのオントロジーを使用してユーザーデータを相互運用します。

Focusing on geo-hashtagged tweets, Location Tagging News Feed (LTNF) is a semantics-based system that extracts geographical hashtags from social media and uses a geographical domain ontology to establish relations between the hashtags and the messages they occur in. 
地理的ハッシュタグ付きツイートに焦点を当てたLocation Tagging News Feed (LTNF)は、ソーシャルメディアから地理的ハッシュタグを抽出し、地理的ドメインオントロジーを使用してハッシュタグとそれが発生するメッセージとの関係を確立する意味ベースのシステムです。

Wikipedia is also used as a direct source of input in a few papers. 
Wikipediaは、いくつかの論文で直接の入力ソースとしても使用されます。

**Multimedia news**: Several papers use multimedia data as input. 
**マルチメディアニュース**: いくつかの論文は、入力としてマルチメディアデータを使用します。

Jing et al. analyses news texts in combination with associated images to suggest human-level image captions. 
Jingらは、関連する画像と組み合わせたニューステキストを分析して、人間レベルの画像キャプションを提案します。

To extend the lifetime of TV news, the AGV pipeline makes news videos from the RAI archives available for geography education. 
テレビニュースの寿命を延ばすために、AGVパイプラインはRAIアーカイブからのニュースビデオを地理教育のために利用可能にします。

**News metadata**: Focusing on multimedia metadata, García et al. inputs metadata embedded in formats such as MPEG-7 for content description and MPEG-21 for delivery and consumption. 
**ニュースメタデータ**: マルチメディアメタデータに焦点を当てて、Garcíaらはコンテンツ記述のためのMPEG-7や配信と消費のためのMPEG-21などの形式に埋め込まれたメタデータを入力します。

The approach uses semantic mappings from XML Schema to OWL and from XML to RDF to integrate administrative multimedia metadata in newspaper organisations. 
このアプローチは、XMLスキーマからOWLへの意味的マッピングと、XMLからRDFへのマッピングを使用して、新聞組織内の管理マルチメディアメタデータを統合します。

As already explained, MediaLoep also integrates descriptive multimedia news metadata from news production systems semantically. 
すでに説明したように、MediaLoepはニュース制作システムからの記述的マルチメディアニュースメタデータも意味的に統合します。

**Knowledge graphs**: Many papers use existing knowledge graphs as inputs. 
**知識グラフ**: 多くの論文は、既存の知識グラフを入力として使用します。

The number has risen in the past few years due to the appearance of deep-NN architectures that infuse triples from open KGs to enhance learning from news texts. 
数は、オープンKGからのトリプルを注入してニューステキストからの学習を強化する深層NNアーキテクチャの出現により、過去数年で増加しました。

Indeed, almost all the recent deep learning papers exploit open KGs in this way. 
実際、最近のほとんどすべての深層学習論文は、このようにオープンKGを利用しています。

**User histories**: A smaller group of deep-NN papers inputs user histories, for example, in the form of click logs, to train recommenders. 
**ユーザーヒストリー**: より小規模な深層NN論文のグループは、ユーザーヒストリーを入力として使用し、例えばクリックログの形で、レコメンダーを訓練します。

**Summary**: Our review shows that the research on semantic knowledge graphs for the news exploits a broad range of input sources. 
**要約**: 私たちのレビューは、ニュースのための意味的知識グラフに関する研究が幅広い入力ソースを活用していることを示しています。

Textual news articles in digital form is the most important source. 
デジタル形式のテキストニュース記事が最も重要なソースです。

Other frequently used types of input data are RSS and other news feeds, social media and the Web, multimedia news, news metadata, knowledge graphs, and user histories. 
他に頻繁に使用される入力データのタイプには、RSSおよびその他のニュースフィード、ソーシャルメディアとウェブ、マルチメディアニュース、ニュースメタデータ、知識グラフ、ユーザーヒストリーがあります。

Multimedia, including TV news, were popular in first years of the study period and have seen a rebound in the deep-learning era. 
マルチメディア、特にテレビニュースは、研究期間の最初の数年間に人気があり、深層学習時代に再び注目を集めています。

RSS and other news feeds were popular for many years, but have recently been overtaken by social media, including Twitter. 
RSSおよびその他のニュースフィードは長年人気がありましたが、最近ではTwitterを含むソーシャルメディアに取って代わられています。

In recent years, KGs are being used increasingly often to infuse world knowledge into deep NNs for news analysis. 
近年、KGはニュース分析のために深層NNに世界の知識を注入するためにますます頻繁に使用されています。

User histories have also been used in recent recommendation papers. 
ユーザーヒストリーも最近の推薦論文で使用されています。

### 3.6. News Life Cycle  
### 3.6. ニュースライフサイクル  

The main papers also target different phases of the news life cycle. 
主要な論文は、ニュースライフサイクルの異なるフェーズをターゲットにしています。

The largest group of papers focuses on organising and managing already published news. 
最も大きなグループの論文は、すでに公開されたニュースの整理と管理に焦点を当てています。

For example, Neptuno extends the life of published news by annotating reports with keywords and IPTC codes, thereby relating past news reports to current ones that share the same keywords or code. 
例えば、Neptunoは、レポートにキーワードとIPTCコードを注釈付けすることで、公開されたニュースの寿命を延ばし、過去のニュースレポートを同じキーワードやコードを共有する現在のものに関連付けます。

It thus re-contextualises old news in light of more recent events. 
これにより、最近の出来事を考慮して古いニュースを再文脈化します。

The MediaLoep data model supports managing information generated by news production and publishing processes. 
MediaLoepデータモデルは、ニュース制作および出版プロセスによって生成された情報の管理をサポートします。

AGV makes archival news videos available for geography education. 
AGVは、地理教育のためにアーカイブニュースビデオを利用可能にします。

Focus in recent years has shifted from focusing on already published news to also targeting earlier phases of the news life cycle. 
近年の焦点は、すでに公開されたニュースに焦点を当てることから、ニュースライフサイクルの早い段階にもターゲットを移しています。

As already mentioned, the Pundit algorithm predicts likely future news events based on short textual descriptions of current events. 
すでに述べたように、Punditアルゴリズムは、現在のイベントの短いテキスト記述に基づいて、将来のニュースイベントを予測します。

A small group of mostly Twitter-based papers deals with detecting emerging news, or potentially newsworthy events or situations that are not yet reported as news but that may be circulating in social media or elsewhere. 
主にTwitterに基づく少数のグループの論文は、出現するニュースや、まだニュースとして報告されていないがソーシャルメディアや他の場所で流通している可能性のあるニュース価値のあるイベントや状況を検出することに取り組んでいます。

For example, Tweet2News identifies emerging news from documentary (or headline-like) tweets and lifts them into RDF graphs, which are then enriched with triples from the LOD cloud and arranged into storylines to generate news reports in real time. 
例えば、Tweet2Newsはドキュメンタリー（または見出しのような）ツイートから出現するニュースを特定し、それをRDFグラフに持ち上げ、LODクラウドからのトリプルで強化し、ストーリーラインに配置してリアルタイムでニュースレポートを生成します。

Focusing on breaking news, the Semantics-based Pipeline for Economic Event Detection (SPEED) uses a domain ontology to detect and annotate economic events. 
速報ニュースに焦点を当てたSemantics-based Pipeline for Economic Event Detection (SPEED)は、ドメインオントロジーを使用して経済イベントを検出し、注釈を付けます。

The approach combines ontology-based word and event-phrase gazetteers; a word-phrase look-up component; a word-sense disambiguator; and an event detector that recognises event-patterns described in a domain ontology. 
このアプローチは、オントロジーに基づく単語およびイベントフレーズのガゼッター、単語フレーズのルックアップコンポーネント、単語意味の曖昧性解消器、およびドメインオントロジーで記述されたイベントパターンを認識するイベント検出器を組み合わせています。

The Evolutionary Event Ontology Knowledge (EEOK) ontology represents the typical evolution of developing news stories as patterns. 
Evolutionary Event Ontology Knowledge (EEOK)オントロジーは、発展するニュースストーリーの典型的な進化をパターンとして表現します。

It can thereby be used to predict the most likely next events in a developing story and to train dedicated detectors for different event types and phases (such as "investigation," "arrest," "court hearing") in a complex storyline ("fire outbreak"). 
これにより、発展するストーリーの中で最も可能性の高い次のイベントを予測し、複雑なストーリーライン（「火災発生」）における異なるイベントタイプやフェーズ（「調査」、「逮捕」、「裁判」など）のための専用検出器を訓練することができます。

RDFLiveNews also follows developing news by combining statistical and other machine-learning techniques to represent news events as knowledge graphs in real time by extracting RDF triples from RSS data streams. 
RDFLiveNewsは、統計的およびその他の機械学習技術を組み合わせて、RSSデータストリームからRDFトリプルを抽出することにより、ニュースイベントをリアルタイムで知識グラフとして表現することで、発展するニュースを追跡します。

**Summary**: Our review shows that all the different phases of the news-life cycle are covered by the research, from predicting future news, through detecting and monitoring emerging, breaking, and developing news, to managing and exploiting already published news. 
**要約**: 私たちのレビューは、未来のニュースを予測することから、出現するニュース、速報ニュース、発展するニュースを検出および監視すること、そしてすでに公開されたニュースを管理および活用することまで、ニュースライフサイクルのすべての異なるフェーズが研究によってカバーされていることを示しています。

Many main papers attempt to cover several of these life-cycle phases. 
多くの主要な論文は、これらのライフサイクルフェーズのいくつかをカバーしようとしています。

### 3.7. Semantic Techniques and Tools  
### 3.7. 意味的技術とツール  

The main papers use a broad variety of semantic techniques and tools. 
主要な論文は、幅広い意味的技術とツールを使用しています。

We separate them into exchange formats, ontologies and vocabularies, information resources, and processing and storage techniques. 
それらを交換フォーマット、オントロジーと語彙、情報リソース、処理およびストレージ技術に分けます。

**Semantic exchange formats**: By semantic exchange formats, we mean standards for exchanging and storing semantic data. 
**意味的交換フォーマット**: 意味的交換フォーマットとは、意味データを交換および保存するための標準を指します。

RDF, OWL, and SPARQL are most common. 
RDF、OWL、およびSPARQLが最も一般的です。

More than half of the papers use RDF to manage information. 
半数以上の論文が情報管理にRDFを使用しています。

The earliest example is Neptuno, which uses RDF to represent the IPTC's hierarchical subject reference system. 
最も古い例はNeptunoで、IPTCの階層的な主題参照システムを表現するためにRDFを使用しています。

More than a third of the main papers use OWL for ontology representation. 
主要な論文の3分の1以上がオントロジー表現にOWLを使用しています。



. The earliest example is Neptuno, which uses RDF to represent the IPTC's hierarchical subject reference system. 
最も古い例はNeptunoであり、これはRDFを使用してIPTCの階層的な主題参照システムを表現しています。

More than a third of the main papers use OWL for ontology representation. 
主要な論文の3分の1以上が、オントロジー表現にOWLを使用しています。

For example, the MediaLoep data model is represented in OWL (using the SKOS vocabulary), and its concepts are linked to standard knowledge bases such as DBpedia and GeoNames. 
例えば、MediaLoepデータモデルはOWL（SKOS語彙を使用）で表現され、その概念はDBpediaやGeoNamesなどの標準知識ベースにリンクされています。

And we have already mentioned the NEWS Ontology, which is represented in OWL-DL, the description logic subset of OWL. 
また、私たちはすでに、OWLの記述論理のサブセットであるOWL-DLで表現されたNEWS Ontologyについて言及しました。

SPARQL is also common. 
SPARQLも一般的です。

It is central in the Hermes project and in the News Articles Platform. 
それはHermesプロジェクトやNews Articles Platformの中心的な役割を果たしています。

RDFS is also widely used, including in the NEWS project. 
RDFSも広く使用されており、NEWSプロジェクトにも含まれています。

**Ontologies and vocabularies**: By ontologies and vocabularies, we mean formal terminologies for semantic information exchange. 
**オントロジーと語彙**: オントロジーと語彙とは、セマンティック情報交換のための正式な用語を指します。

Dublin Core (DC) and Friend of a Friend (FOAF) are the most used general vocabularies, starting already with KIM, whose ontology is designed to be aligned with them both. 
Dublin Core (DC)とFriend of a Friend (FOAF)は最も使用される一般的な語彙であり、KIMから始まり、そのオントロジーは両者と整合するように設計されています。

The NEWS project also uses DC, whereas FOAF plays a prominent role in a few approaches that deal with personalisation, in particular in a social context. 
NEWSプロジェクトもDCを使用しており、FOAFは特に社会的文脈におけるパーソナライズに関するいくつかのアプローチで重要な役割を果たしています。

Another much-used ontology is the Simple Knowledge Organization System (SKOS). 
もう一つのよく使用されるオントロジーはSimple Knowledge Organization System (SKOS)です。

It is used by the NEWS Ontology to align and interoperate concepts from different annotation standards, including the IPTC News Codes. 
これはNEWS Ontologyによって、IPTC News Codesを含む異なるアノテーション標準からの概念を整合させ、相互運用するために使用されます。

It is also used for personalised multimedia recommendation in Hopfgartner and Jose, and for integrating news-production metadata in MediaLoep. 
また、HopfgartnerとJoseのパーソナライズされたマルチメディア推薦や、MediaLoepにおけるニュース制作メタデータの統合にも使用されます。

The OWL-representation of IPTC's News Codes by Troncy links to Dublin Core and SKOS concepts to increase precision and facilitate content enrichment. 
TroncyによるIPTCのNews CodesのOWL表現は、精度を高め、コンテンツの強化を促進するためにDublin CoreおよびSKOSの概念にリンクしています。

The Simple Event Model (SEM) and OWL Time are used in the NewsReader and News Angler projects. 
Simple Event Model (SEM)とOWL Timeは、NewsReaderおよびNews Anglerプロジェクトで使用されています。

SUMO/MILO is used in the NEWS project. 
SUMO/MILOはNEWSプロジェクトで使用されています。

SUMO and ESO are used in NewsReader. 
SUMOとESOはNewsReaderで使用されています。

Other general ontologies include schema.org, used to contextualise the ClaimsKG, and KIM's PROTON ontology. 
他の一般的なオントロジーには、ClaimsKGを文脈化するために使用されるschema.orgや、KIMのPROTONオントロジーが含まれます。

The Provenance Data Model (PROV-DM) is used to discover high-level provenance using semantic similarity. 
Provenance Data Model (PROV-DM)は、セマンティック類似性を使用して高レベルの出所を発見するために使用されます。

Although several other papers mention provenance, too, they do not explicitly refer to or use PROV-DM, nor its OWL formulation, PROV-O. 
他のいくつかの論文も出所について言及していますが、PROV-DMやそのOWLの定式化であるPROV-Oを明示的に参照したり使用したりしていません。

However, the NewsReader project uses the Grounded Representation and Source Perspective (GRaSP) framework, which has at least been designed to be compatible with PROV-DM. 
しかし、NewsReaderプロジェクトはGrounded Representation and Source Perspective (GRaSP)フレームワークを使用しており、これは少なくともPROV-DMと互換性があるように設計されています。

On the news side, the rNews vocabulary is used for semantic mark-up of web news resources in several papers. 
ニュースの側では、rNews語彙がいくつかの論文でウェブニュースリソースのセマンティックマークアップに使用されています。

Whereas most of the papers in this review rely on the older versions of rNews, the ASRAEL project uses its newer schema.org-based rNews vocabulary. 
このレビューのほとんどの論文は古いバージョンのrNewsに依存していますが、ASRAELプロジェクトは新しいschema.orgベースのrNews語彙を使用しています。

The Internationalization Tag Set (ITS) is also used in a few papers, for example, to unify claims in ClaimsKG. 
Internationalization Tag Set (ITS)もいくつかの論文で使用されており、例えばClaimsKGの主張を統一するために使用されています。

The IPTC's General Architecture Framework (GAF) is used in NewsReader. 
IPTCのGeneral Architecture Framework (GAF)はNewsReaderで使用されています。

On the natural-language side, several proposals use the RDF/OWL-based NLP Interchange Format (NIF) to exchange semantic data between NLP components. 
自然言語の側では、いくつかの提案がRDF/OWLベースのNLP Interchange Format (NIF)を使用してNLPコンポーネント間でセマンティックデータを交換しています。

In addition, more than a third of the papers propose their own domain ontologies. 
さらに、3分の1以上の論文が独自のドメインオントロジーを提案しています。

**Semantic information resources**: By semantic information resources, we mean open knowledge graphs, or openly available semantic datasets expressed as triples. 
**セマンティック情報リソース**: セマンティック情報リソースとは、オープンな知識グラフ、またはトリプルとして表現されたオープンに利用可能なセマンティックデータセットを指します。

Semantic encyclopedias are most frequently used. 
セマンティック百科事典が最も頻繁に使用されます。

More than a quarter of the main papers somehow exploit DBpedia. 
主要な論文の4分の1以上が何らかの形でDBpediaを活用しています。

It is, for example, used by NewsReader for semantic linking and enrichment. 
例えば、NewsReaderはセマンティックリンクと強化のためにDBpediaを使用しています。

Wikidata is an alternative that is used in several recent approaches. 
Wikidataは、最近のいくつかのアプローチで使用される代替手段です。

It is used by ASRAEL and VLX-Stories to support semantic labelling, enrichment, and search, and it used to detect fake news in Brașoveanu and Andonie. 
ASRAELやVLX-Storiesは、セマンティックラベリング、強化、検索をサポートするためにWikidataを使用しており、BrașoveanuとAndonieではフェイクニュースを検出するために使用されました。

There is also increasing uptake of Google's KG, which is used by VLX-Stories to detect emerging entities, in Sagi et al. to separate emerging from already-known entities, and by AGV to provide additional information about entities extracted from educational TV programs. 
また、VLX-Storiesが新たに出現するエンティティを検出するために使用し、Sagiらが新たに出現するエンティティと既知のエンティティを区別するために使用し、AGVが教育テレビ番組から抽出されたエンティティに関する追加情報を提供するために使用するGoogleのKGの利用が増加しています。

Although it has been seeded into Google's knowledge graph and is no longer maintained, Freebase is still being used for external linking in K-Pop, for content-based recommendation in Joseph and Jiang, for evaluation of TAMURE, and for enriching government data in Sarmiento Suárez and Jiménez-Guarín. 
FreebaseはGoogleの知識グラフに組み込まれ、もはやメンテナンスされていませんが、K-Popの外部リンク、JosephとJiangのコンテンツベースの推薦、TAMUREの評価、Sarmiento SuárezとJiménez-Guarínの政府データの強化にまだ使用されています。

GeoNames is used as the reference graph for geographical information in many papers. 
GeoNamesは多くの論文で地理情報の参照グラフとして使用されています。

With the availability of large one-stop KGs like these, fewer papers than before rely on the LOD cloud in general. 
このような大規模なワンストップKGの利用可能性により、以前よりも一般的にLODクラウドに依存する論文は減少しています。

An exception is Hopfgartner and Jose, which exploits the LOD cloud to identify news stories that match users' interests. 
例外として、HopfgartnerとJoseはLODクラウドを利用してユーザーの興味に合ったニュースストーリーを特定しています。

Beyond general semantic encyclopedias and other LOD resources, YAGO2 and its integration of WordNet event classes is used by Kuzey et al. to classify named news events. 
一般的なセマンティック百科事典や他のLODリソースを超えて、YAGO2とそのWordNetイベントクラスの統合は、Kuzeyらによって命名されたニュースイベントを分類するために使用されています。

The initial version of YAGO is used by Pundit to build a world entity graph for mining causal relationship between news events, and in Wang et al. to infuse world knowledge into a Knowledge-driven Multimodal Graph Convolutional Network (KMGCN) for fake news detection. 
YAGOの初期バージョンは、Punditによってニュースイベント間の因果関係をマイニングするための世界エンティティグラフを構築するために使用され、Wangらによってフェイクニュース検出のためにKnowledge-driven Multimodal Graph Convolutional Network (KMGCN)に世界知識を注入するために使用されています。

Common-sense knowledge from the Cyc project is used, too, for example, to augment reasoning over semantic representations mined from financial news texts and to predict future events. 
Cycプロジェクトからの常識知識も使用されており、例えば、金融ニューステキストからマイニングされたセマンティック表現に対する推論を強化し、将来のイベントを予測するために使用されています。

PolarisX uses ConceptNet 5.5 as a development case and for evaluating its approach to automatically expand knowledge graphs with new news events. 
PolarisXは、開発ケースとしてConceptNet 5.5を使用し、新しいニュースイベントで知識グラフを自動的に拡張するアプローチを評価しています。

ConceptNet is also used by Pundit. 
ConceptNetはPunditでも使用されています。

Several of the general semantic information resources, such as DBpedia, ConceptNet, Cyc, Wikidata, and YAGO, come with their own resource-specific ontologies and vocabularies in addition to the ones mentioned in the previous section. 
DBpedia、ConceptNet、Cyc、Wikidata、YAGOなどの一般的なセマンティック情報リソースのいくつかは、前のセクションで言及されたものに加えて、それぞれのリソース固有のオントロジーと語彙を持っています。

On the natural language side, WordNet is not natively semantic, but it is used in a third of the main papers—more than any of the natively semantic resources—including Hermes, NewsReader, and SPEED—although only a single paper explicitly mentions WordNet's RDF version. 
自然言語の側では、WordNetは本来セマンティックではありませんが、主要な論文の3分の1で使用されており（Hermes、NewsReader、SPEEDを含む）、本来セマンティックなリソースの中で最も多く使用されていますが、WordNetのRDFバージョンに言及している論文は1本だけです。

**Semantic processing techniques**: By semantic processing technique, we mean programming techniques and tools used to create and exploit semantic information resources. 
**セマンティック処理技術**: セマンティック処理技術とは、セマンティック情報リソースを作成し、活用するために使用されるプログラミング技術とツールを指します。

Entity linking is the most frequently used technique by far. 
エンティティリンクは、これまでで最も頻繁に使用される技術です。

The most used entity linkers are DBpedia Spotlight, Thomson-Reuters' OpenCalais, and TagMe. 
最も使用されるエンティティリンクは、DBpedia Spotlight、Thomson-ReutersのOpenCalais、TagMeです。

Beyond entity linking, seven papers employ logical reasoning. 
エンティティリンクを超えて、7つの論文が論理的推論を採用しています。

Description logic and OWL-DL is used for trust-based resolution of inconsistent KBs in Golbeck and Halaschek-Wiener and for managing the NEWS Ontology. 
記述論理とOWL-DLは、GolbeckとHalaschek-Wienerにおける不整合なKBの信頼に基づく解決や、NEWS Ontologyの管理に使用されています。

Other papers mention general ontology-enabled reasoning without OWL-DL. 
他の論文は、OWL-DLなしの一般的なオントロジー対応の推論について言及しています。

For example, OPWFP and Novalija and Mladenić, which uses Cyc to answer questions about business news. 
例えば、OPWFPやNovalijaとMladenićは、ビジネスニュースに関する質問に答えるためにCycを使用しています。

Rule-based inference is also used. 
ルールベースの推論も使用されています。

The most common programming API for semantic data processing is Apache's Java-based Jena framework, used in 12 main papers. 
セマンティックデータ処理のための最も一般的なプログラミングAPIは、ApacheのJavaベースのJenaフレームワークであり、12の主要な論文で使用されています。

Only 4 papers mention Python's RDFlib, most of them from recent years. 
PythonのRDFlibに言及しているのは4つの論文だけであり、そのほとんどは最近のものです。

Protégé is used in 4 papers, for example, for ontology development in Neptuno and in the NEWS project. 
Protégéは4つの論文で使用されており、例えばNeptunoやNEWSプロジェクトでのオントロジー開発に使用されています。

**Semantic storage techniques**: Although almost all the main papers mention ontologies or knowledge graphs, few of them discuss storage and none of them focus primarily on the storage side. 
**セマンティックストレージ技術**: ほとんどすべての主要な論文がオントロジーや知識グラフに言及していますが、その中でストレージについて議論しているものは少なく、ストレージ側に主に焦点を当てているものはありません。

The two most frequently used triple stores are RDF4J (formerly Sesame) used by four papers and OpenLink Virtuoso also used by four papers. 
最も頻繁に使用されるトリプルストアは、4つの論文で使用されているRDF4J（以前のSesame）と、4つの論文でも使用されているOpenLink Virtuosoです。

AllegroGraph is employed in two papers. 
AllegroGraphは2つの論文で使用されています。

Used by NewsReader, the KnowledgeStore is designed to store large collections of documents and link them to RDF triples that are extracted from the documents or collected from the LOD cloud. 
NewsReaderで使用されるKnowledgeStoreは、大規模な文書コレクションを保存し、それらを文書から抽出されたRDFトリプルやLODクラウドから収集されたものにリンクするように設計されています。

It uses a big-data ready file system (Hadoop Distributed File System, HDFS) and databases (Apache HBase and Virtuoso) to store unstructured (e.g., news articles) and structured information (e.g., RDF triples) together. 
それは、非構造化情報（例：ニュース記事）と構造化情報（例：RDFトリプル）を一緒に保存するために、ビッグデータ対応のファイルシステム（Hadoop Distributed File System, HDFS）とデータベース（Apache HBaseおよびVirtuoso）を使用しています。

**Summary**: Our review demonstrates that the research on KG for news exploits a broad variety of available semantic resources, techniques, and tools. 
**要約**: 私たちのレビューは、ニュースのためのKGに関する研究が利用可能なセマンティックリソース、技術、ツールの幅広いバラエティを活用していることを示しています。

The research on KGs for news differs from the mainstream research on KGs mainly in its stronger focus on language (e.g., the ITS and NIF vocabularies), on events (e.g., the SEM ontology), and, of course, on news (the rNews vocabulary). 
ニュースのためのKGに関する研究は、主流のKG研究とは主に言語（例：ITSおよびNIF語彙）、イベント（例：SEMオントロジー）、そしてもちろんニュース（rNews語彙）に対するより強い焦点において異なります。

The border between semantic and non-semantic computing techniques is not always sharp. 
セマンティックコンピューティング技術と非セマンティックコンピューティング技術の境界は常に明確ではありません。

For example, although WordNet is not natively semantic, it is available as RDF and is used as a semantic information resource in many proposals. 
例えば、WordNetは本来セマンティックではありませんが、RDFとして利用可能であり、多くの提案でセマンティック情報リソースとして使用されています。

A recent trend is that Wikidata is becoming more popular compared to DBpedia. 
最近の傾向は、WikidataがDBpediaと比較してより人気が高まっていることです。

### 3.8. Other Techniques and Tools  
### 3.8. その他の技術とツール  

Most main papers use semantic knowledge graphs in combination with other techniques and tools. 
ほとんどの主要な論文は、他の技術やツールと組み合わせてセマンティック知識グラフを使用しています。

Similar to the previous section, we separate them into exchange formats, information resources, and processing and storage techniques. 
前のセクションと同様に、これらを交換フォーマット、情報リソース、処理およびストレージ技術に分けます。

The research on semantic knowledge graphs for the news is technologically diverse. 
ニュースのためのセマンティック知識グラフに関する研究は、技術的に多様です。

We find examples of research that exploit most of the popular news-related standards and most of the popular techniques for NLP, machine learning, deep learning, and computing in general. 
私たちは、人気のあるニュース関連の標準や、NLP、機械学習、深層学習、一般的なコンピューティングのための人気のある技術のほとんどを活用する研究の例を見つけます。

On the news side, the IPTC family of standards and resources is central. 
ニュースの側では、IPTCの標準とリソースのファミリーが中心的です。

On the NLP side, entity extraction, NL pre-processing, co-reference resolution, morphological analysis, and semantic-role labelling are common, whereas GATE, Lucene, spaCy, JAPE, and StanfordNER are the most used tools. 
NLPの側では、エンティティ抽出、NL前処理、コア参照解決、形態素解析、セマンティックロールラベリングが一般的であり、GATE、Lucene、spaCy、JAPE、StanfordNERが最も使用されるツールです。

On the ML side, the past decade has seen more and more proposals that exploit machine-learning techniques, as illustrated by three early examples from 2012: 
MLの側では、過去10年間で機械学習技術を活用する提案が増えてきており、2012年の3つの初期の例で示されています。

De Nies et al. uses greedy clustering to automatically detect provenance relations between news articles. 
De Niesらは、貪欲なクラスタリングを使用してニュース記事間の出所関係を自動的に検出します。

The Hermes framework uses a pattern-language and rule-based approach to learn ontology instances and event relations from text, combining lexico-semantic patterns with semantic information. 
Hermesフレームワークは、パターン言語とルールベースのアプローチを使用してテキストからオントロジーインスタンスとイベント関係を学習し、語彙的セマンティックパターンとセマンティック情報を組み合わせています。

It is used to analyse financial and political news articles, splitting its corpus of news articles into a training and a test set. 
これは、金融および政治ニュース記事を分析するために使用され、ニュース記事のコーパスをトレーニングセットとテストセットに分割します。

Pundit mines text patterns from news headlines to predict potential future events based on textual descriptions of current events. 
Punditは、ニュースの見出しからテキストパターンをマイニングして、現在のイベントのテキスト記述に基づいて潜在的な未来のイベントを予測します。

It uses machine learning to automatically induce a causality function based on examples of causality pairs mined from a large collection of archival news headlines. 
それは、アーカイブされたニュース見出しの大規模なコレクションからマイニングされた因果ペアの例に基づいて、因果関係の関数を自動的に導出するために機械学習を使用します。



. It uses machine learning to automatically induce a causality function based on examples of causality pairs mined from a large collection of archival news headlines. 
これは、アーカイブされたニュースヘッドラインの大規模コレクションから抽出された因果ペアの例に基づいて、因果関数を自動的に導出するために機械学習を使用します。

Whereas these early approaches rely on hand-crafted rules and dedicated learning algorithms, more recent proposals use standard machine-learning techniques for word, graph, and entity embeddings, such as TransE, TransR, TransD, and word2vec.  
これらの初期のアプローチは手作りのルールと専用の学習アルゴリズムに依存しているのに対し、最近の提案は、TransE、TransR、TransD、word2vecなどの単語、グラフ、エンティティの埋め込みに標準的な機械学習技術を使用しています。

On the DL side, there has been a sharp rise since 2019 in deep learning approaches. 
DLの側では、2019年以降、深層学習アプローチが急増しています。

PolarisX uses pre-trained multilingual BERT model to detect new relations, with the aim of updating its underlying knowledge graph in real time. 
PolarisXは、事前に学習された多言語BERTモデルを使用して新しい関係を検出し、リアルタイムでその基盤となる知識グラフを更新することを目指しています。

TAMURE uses tensor factorisation implemented in TensorFlow to learn joint embedding representations of entities and relation types. 
TAMUREは、TensorFlowで実装されたテンソル分解を使用して、エンティティと関係タイプの共同埋め込み表現を学習します。

Focusing on click-through rate (CTR) prediction in online news sites, DKN uses a Convolutional Neural Network with separate channels for words and entities and an attention module to dynamically aggregate user histories. 
オンラインニュースサイトにおけるクリック率（CTR）予測に焦点を当てたDKNは、単語とエンティティのための別々のチャネルを持つ畳み込みニューラルネットワークと、ユーザ履歴を動的に集約するための注意モジュールを使用します。

Gao et al. propose a deep neural network model that employs multiple self-attention modules for words, entities, and users for news recommendation. 
Gaoらは、ニュース推薦のために単語、エンティティ、ユーザのための複数の自己注意モジュールを採用した深層ニューラルネットワークモデルを提案しています。

Pan et al. propose the B-TransE model to detect fake news based on content. 
Panらは、コンテンツに基づいてフェイクニュースを検出するためのB-TransEモデルを提案しています。

The most used deep learning techniques and tools are CNN, GRU, GCN, LSTM, BERT, and attention.  
最も使用されている深層学習技術とツールは、CNN、GRU、GCN、LSTM、BERT、および注意です。

The focus on news standards is strongest in the first part of the study period, up to around 2014, when many approaches incorporate existing news standards into the emerging LOD cloud. 
ニュース基準への焦点は、研究期間の最初の部分、すなわち2014年頃までが最も強く、多くのアプローチが既存のニュース基準を新たに出現するLODクラウドに組み込んでいます。

The second part, from around 2015, sees a shift towards machine learning approaches, first focusing on NLP and embedding techniques and, since around 2019, on deep learning.  
第二部は、2015年頃から機械学習アプローチへのシフトを見せ、最初はNLPと埋め込み技術に焦点を当て、2019年頃からは深層学習に移行しています。

### 3.9. News Domain ニュースドメイン

Most of the main papers do not focus on a particular news domain, except as examples or for evaluation. 
主要な論文のほとんどは、特定のニュースドメインに焦点を当てておらず、例や評価のためにのみ言及されています。

Among the domain-specific papers, economy/finance is most common. 
ドメイン特化型の論文の中で、経済/金融が最も一般的です。

For example, Lupiani-Ruiz et al. presents a semantic search engine for financial news that uses an automatically populated knowledge graph that is kept up to date with semantically annotated financial news items, and we have already mentioned the SPEED pipeline for economic event detection and annotation in real time.  
例えば、Lupiani-Ruizらは、意味的に注釈された金融ニュースアイテムで最新の状態に保たれる自動的に生成された知識グラフを使用する金融ニュースのためのセマンティック検索エンジンを提示しており、リアルタイムでの経済イベント検出と注釈のためのSPEEDパイプラインについてもすでに言及しました。

Politics is the theme of over 900,000 French tweets collected to trace propagation of knowledge, misinformation, and hearsay. 
政治は、知識、誤情報、噂の伝播を追跡するために収集された90万以上のフランス語のツイートのテーマです。

Sarmiento Suárez and Jiménez-Guarín use named entity linking to contextualise open government data, making them available in online news portals alongside related news items that match each user's interests. 
Sarmiento SuárezとJiménez-Guarínは、オープン政府データを文脈化するために固有名詞リンクを使用し、各ユーザの興味に合った関連ニュースアイテムとともにオンラインニュースポータルで利用可能にします。

In the sports news domain, Nguyen et al. propose a recommender system based on BKSport that combines semantic and content-based similarity measures to suggest relevant news items. 
スポーツニュースドメインでは、NguyenらがBKSportに基づく推薦システムを提案しており、意味的およびコンテンツベースの類似度測定を組み合わせて関連ニュースアイテムを提案します。

Other domains targeted by multiple papers include science, business, health, and the stock market.  
他の複数の論文が対象とするドメインには、科学、ビジネス、健康、株式市場が含まれます。

Targeting entertainment news, K-Pop builds on an entertainer ontology to compile a semantic knowledge graph that represents the profiles and activities of Korean pop artists. 
エンターテインメントニュースを対象としたK-Popは、エンターテイナーのオントロジーに基づいて、韓国のポップアーティストのプロフィールと活動を表すセマンティック知識グラフを編纂します。

The artists' profiles in the graph are based on information from Wikipedia and enriched with content from DBpedia, Freebase, LinkedMDB, and MusicBrainz. 
グラフ内のアーティストのプロフィールはWikipediaの情報に基づいており、DBpedia、Freebase、LinkedMDB、MusicBrainzからのコンテンツで強化されています。

They are also linked to other sources that represent not only the artist, but also their activities, business, albums, and schedules. 
彼らはまた、アーティストだけでなく、彼らの活動、ビジネス、アルバム、スケジュールを表す他のソースにもリンクされています。

The graph and ontology are used in the Gnosis app to enhance K-Pop entertainment news with information about artists retrieved from the knowledge graph.  
このグラフとオントロジーは、Gnosisアプリで使用され、知識グラフから取得したアーティストに関する情報でK-Popエンターテインメントニュースを強化します。

WebLyzard identifies topics and entities in news about the environment and uses visualisations to present lexical, geo-spatial, and other contextual information to gain overview of perceptions of and reactions to environmental threats and options. 
WebLyzardは、環境に関するニュースのトピックとエンティティを特定し、視覚化を使用して語彙、地理空間、およびその他の文脈情報を提示し、環境の脅威と選択肢に対する認識と反応の概要を把握します。

AGV targets education, in particular in science and technology. 
AGVは教育、特に科学と技術を対象としています。

Other domains include medicine, crime, and earth science.  
他のドメインには、医学、犯罪、地球科学が含まれます。

**Summary**: Our review suggests that semantic knowledge graphs and related semantic techniques are useful in a broad range of news domains. 
**要約**: 私たちのレビューは、セマンティック知識グラフと関連するセマンティック技術が広範なニュースドメインで有用であることを示唆しています。

Most investigated so far are economy and finance. 
これまでに最も調査されたのは経済と金融です。

There is little domain-specificity in the research so far: Most architectures and techniques proposed for one news domain appear readily transferable to others. 
これまでの研究にはドメイン特異性がほとんどなく、あるニュースドメインのために提案されたほとんどのアーキテクチャと技術は他のドメインに容易に移転可能であるようです。

The higher interest in the financial and business domains may result from economic opportunities combined with the availability of both quantitative and qualitative data streams in real time.  
金融およびビジネスドメインへの関心が高いのは、経済的機会とリアルタイムでの定量的および定性的データストリームの利用可能性が組み合わさった結果かもしれません。

### 3.10. Language 言語

The most frequently covered languages beside English are Italian and Spanish, but neither is supported by more than 10 papers. 
英語以外で最も頻繁に取り上げられる言語はイタリア語とスペイン語ですが、どちらも10本以上の論文でサポートされていません。

Support for French and German in the main papers appear only in combination with English. 
主要な論文におけるフランス語とドイツ語のサポートは、英語と組み合わせてのみ見られます。

Many papers deal with a combination of several languages, such as English, Italian, and Spanish in the NEWS project, and a few recent approaches explicitly aim to be multi-lingual (or language-agnostic). 
多くの論文は、NEWSプロジェクトにおける英語、イタリア語、スペイン語のように、いくつかの言語の組み合わせを扱っており、最近のいくつかのアプローチは明示的に多言語（または言語に依存しない）を目指しています。

For example, NewsReader mentions Dutch, Italian, and Spanish in addition to English, whereas PolarisX aims to cover Chinese, Japanese, and Korean.  
例えば、NewsReaderは英語に加えてオランダ語、イタリア語、スペイン語に言及しているのに対し、PolarisXは中国語、日本語、韓国語をカバーすることを目指しています。

**Summary**: Our review suggests that English is the best supported language by far but, of course, this may be because we use English language as an inclusion criterion. 
**要約**: 私たちのレビューは、英語が圧倒的に最もサポートされている言語であることを示唆していますが、もちろんこれは英語を含入基準として使用しているためかもしれません。

Additional papers addressing other major languages, such as Chinese, French, German, Hindi, and Spanish, may instead be written and published in their own languages. 
中国語、フランス語、ドイツ語、ヒンディー語、スペイン語などの他の主要言語に関する追加の論文は、代わりにそれぞれの言語で書かれ、発表される可能性があります。

The other most frequently supported languages are Spanish, Italian, French, Chinese, Dutch, German, and Japanese, with many of the Chinese and Japanese papers published in recent years. 
他に最も頻繁にサポートされている言語はスペイン語、イタリア語、フランス語、中国語、オランダ語、ドイツ語、日本語であり、多くの中国語および日本語の論文は最近発表されています。

Many approaches also support more than one language, exploiting the inherent language-neutrality of ontologies and knowledge graphs. 
多くのアプローチは、オントロジーと知識グラフの本質的な言語中立性を利用して、複数の言語をサポートしています。

There is a growing interest in offering multi-language and language-agnostic solutions.  
多言語および言語に依存しないソリューションを提供することへの関心が高まっています。

### 3.11. Important Papers 重要な論文

Our main papers reference 1,842 earlier papers and are themselves cited 2,381 times according to Semantic Scholar. 
私たちの主要な論文は1,842本の以前の論文を参照しており、Semantic Scholarによると自らは2,381回引用されています。

The most cited of our main papers is the one about KIM (2004), with the much more recent DKN paper (2018) second. 
私たちの主要な論文の中で最も引用されているのはKIM（2004）に関するもので、次に最近のDKN論文（2018）が続きます。

The paper about Pundit (2012) is also frequently cited. 
Pundit（2012）に関する論文も頻繁に引用されています。

After weighting against the expected number of citations of a paper from the same year, the top five most cited main papers are:  
同年の論文の期待される引用数に対して重み付けを行った後、最も引用された主要な論文のトップ5は次のとおりです。

1. DKN: Deep knowledge-aware network for news recommendation (2018)
2. Semantic annotation, indexing, and retrieval (KIM, 2004)
3. Learning causality for news events prediction (Pundit, 2012)
4. Building event-centric knowledge graphs from news (NewsReader, 2016)
5. Content-based fake news detection using knowledge graphs (Pan et al., 2018)  

The papers most frequently referenced by our main papers are seminal works on the Semantic Web, on WordNet, on TransE, GATE, and word2vec. 
私たちの主要な論文で最も頻繁に参照されている論文は、セマンティックウェブ、WordNet、TransE、GATE、word2vecに関する重要な研究です。

Other frequently referenced papers include DBpedia, Freebase, TransR, GloVe, and YAGO, confirming the importance of LOD resources and embedding models for the research on semantic KGs for news.  
他に頻繁に参照される論文にはDBpedia、Freebase、TransR、GloVe、YAGOが含まれ、ニュースのためのセマンティックKGに関する研究におけるLODリソースと埋め込みモデルの重要性が確認されています。

**Summary**: No paper yet stands out as seminal for the research area. 
**要約**: まだこの研究分野の重要な論文は存在しません。

With the exception of the KIM project, none of the main papers or projects are frequently cited by other main papers, suggesting that research on semantic KGs has not yet matured into a clearly defined research area that is recognised by the larger research community.  
KIMプロジェクトを除いて、主要な論文やプロジェクトは他の主要な論文によって頻繁に引用されておらず、セマンティックKGに関する研究はまだ大きな研究コミュニティに認識される明確に定義された研究分野に成熟していないことを示唆しています。

### 3.12. Frequent Authors and Projects 頻繁な著者とプロジェクト

The most frequent main-paper authors are F. Frasincar (7 papers), F. Hogenboom (5 papers), and groups around D. Deursen / E. Mannens / R. Walle (3 papers each), and N. García / L. Sánchez (3 papers each).  
最も頻繁に主要な論文を執筆している著者はF. Frasincar（7本）、F. Hogenboom（5本）、D. Deursen / E. Mannens / R. Walle（各3本）、N. García / L. Sánchez（各3本）です。

Repeated co-authorship among the frequent authors occurs exclusively within a small number of research projects (or persistent collaborations), such as NEWS, Hermes, and NewsReader.  
頻繁な著者間の繰り返しの共著は、NEWS、Hermes、NewsReaderなどの少数の研究プロジェクト（または持続的なコラボレーション）内でのみ発生します。

Hermes and NewsReader are the most frequently cited projects, but there are very few citations to these and to the other projects/collaborations from other main papers.  
HermesとNewsReaderは最も頻繁に引用されるプロジェクトですが、これらや他のプロジェクト/コラボレーションへの引用は非常に少ないです。

Indeed, none of the main papers from the seven listed projects and collaborations are citing one another. 
実際、リストされた7つのプロジェクトやコラボレーションからの主要な論文は互いに引用していません。

Only 43 references in total are from one main paper to another.  
合計で43件の参照のみが、1つの主要な論文から別の論文に向けられています。

**Summary**: The analysis underpins that the research on semantic KGs has not yet matured into a distinct research area. 
**要約**: この分析は、セマンティックKGに関する研究がまだ明確な研究分野に成熟していないことを裏付けています。

The research is carried out mostly by independently working researchers and groups, although the NewsReader project has involved several institutions located in different countries. 
この研究は主に独立して活動する研究者やグループによって行われていますが、NewsReaderプロジェクトには異なる国に位置するいくつかの機関が関与しています。

There is so far little collaboration and accumulation of knowledge in the area, although the early KIM proposal has been used in later research.  
この分野ではこれまでのところコラボレーションや知識の蓄積はほとんどありませんが、初期のKIM提案は後の研究で使用されています。

### 3.13. Evolution over Time 時間の経過に伴う進化

The research on semantic knowledge graphs for news can be divided into four eras that broadly follow the evolution of knowledge graphs and related technologies in general: the Semantic Web (–2009), Linked Open Data (LOD, 2010–2014), knowledge graphs (KGs, 2015–2018), and deep learning (DL, 2019–) eras.  
ニュースのためのセマンティック知識グラフに関する研究は、一般的に知識グラフと関連技術の進化に沿った4つの時代に分けることができます: セマンティックウェブ（–2009）、リンクドオープンデータ（LOD、2010–2014）、知識グラフ（KG、2015–2018）、および深層学習（DL、2019–）の時代です。

The first era (until around 2009) is inspired by the Semantic-Web idea and early ontology work. 
最初の時代（2009年頃まで）は、セマンティックウェブのアイデアと初期のオントロジー作業に触発されています。

Almost all the main papers from this era mention the Semantic Web or Semantic-Web technologies prominently in their introductions. 
この時代のほとんどすべての主要な論文は、導入部でセマンティックウェブまたはセマンティックウェブ技術に言及しています。

They combine basic natural-language processing with central Semantic-Web ideas such as semantic annotation, domain ontologies, and semantic search applied to the news domain. 
彼らは、基本的な自然言語処理を、ニュースドメインに適用された意味的注釈、ドメインオントロジー、セマンティック検索などの中心的なセマンティックウェブのアイデアと組み合わせています。

Many of the papers bring existing news and multimedia publishing standards into the Semantic-Web world, and the IPTC Media Topics are therefore important. 
多くの論文は、既存のニュースおよびマルチメディア出版基準をセマンティックウェブの世界に持ち込み、したがってIPTCメディアトピックは重要です。

Central semantic techniques are RDF, RDFS, OWL, and SPARQL, and important tasks are archiving and browsing. 
中心的なセマンティック技術はRDF、RDFS、OWL、SPARQLであり、重要なタスクはアーカイブとブラウジングです。

There is also an early interest in multimedia.  
また、マルチメディアに対する初期の関心もあります。

The main papers in second era (2010–2014, but starting with Troncy already in 2008) trails the emergence of the LOD cloud, which many of the papers use to motivate their contributions. 
第二の時代（2010–2014年、ただしTroncyは2008年に始まる）における主要な論文は、LODクラウドの出現に続いており、多くの論文がその貢献を動機付けるために使用しています。

Contextualisation and other types of semantic enrichment of news texts is central, aiming to support more precise search and recommendation. 
ニューステキストの文脈化やその他のタイプのセマンティック強化が中心であり、より正確な検索と推薦をサポートすることを目指しています。

Although some papers use Wikipedia and DBpedia for enrichment, the most used information resource is WordNet.  
いくつかの論文は強化のためにWikipediaやDBpediaを使用していますが、最も使用される情報リソースはWordNetです。



. Although some papers use Wikipedia and DBpedia for enrichment, the most used information resource is WordNet. 
いくつかの論文はWikipediaやDBpediaを強化のために使用していますが、最も使用される情報リソースはWordNetです。

To link news texts precisely to existing semantic resources, more advanced pre-processing of news texts is used along with techniques such as morphological analysis and vector spaces. 
ニューステキストを既存のセマンティックリソースに正確にリンクさせるために、形態素解析やベクトル空間などの技術とともに、ニューステキストのより高度な前処理が使用されます。

GATE is a much-used NLP tool in this era, as is OpenCalais for entity linking and Jena for managing RDF data.  
この時代において、GATEは非常に多く使用されるNLPツールであり、OpenCalaisはエンティティリンクのために、JenaはRDFデータの管理のために使用されます。

The third era (2015–2018), reflects Google's adoption of the term "Knowledge Graphs" in 2012 and the growing importance of machine learning. 
第三の時代（2015–2018）は、2012年にGoogleが「Knowledge Graphs」という用語を採用したことと、機械学習の重要性の高まりを反映しています。

One of the first main papers to mention knowledge graphs is Antonini et al. already in 2013, but most of the main papers are published starting in 2015. 
知識グラフに言及した最初の主要な論文の一つは、2013年のAntonini et al.ですが、主要な論文のほとんどは2015年から発表されています。

The research increasingly considers knowledge graphs independently of semantic standards such as RDF and OWL, and uses machine learning and related techniques to analyse news texts more deeply, for example, extracting events and facts (relations). 
研究は、RDFやOWLなどのセマンティックスタンダードから独立して知識グラフを考慮するようになり、機械学習や関連技術を使用してニューステキストをより深く分析し、例えば、イベントや事実（関係）を抽出します。

DBpedia and entity linking become more frequently used, along with word and graph embeddings. 
DBpediaやエンティティリンクは、単語やグラフの埋め込みとともに、より頻繁に使用されるようになります。

On the NLP side, co-reference resolution and dependency parsing become more important, along with StanfordNER.  
NLPの側面では、共参照解決や依存構文解析が重要になり、StanfordNERとともに使用されます。

Since around 2019, a fourth and final era starts to emerge. 
2019年頃から、第四の最終的な時代が現れ始めます。

Typical approaches analyse news articles using deep neural network (NN) architectures that combine text- and graph-embedding approaches and that infuse triples from open KGs into graph representations of news texts. 
典型的なアプローチは、テキストとグラフの埋め込みアプローチを組み合わせた深層ニューラルネットワーク（NN）アーキテクチャを使用してニュース記事を分析し、オープンKGからのトリプルをニューステキストのグラフ表現に注入します。

Central emerging tasks are fact checking, fake-news detection, and click-through rate (CTR) prediction. 
中心的な新たなタスクは、ファクトチェック、フェイクニュース検出、クリック率（CTR）予測です。

Deep-learning techniques such as CNN, LSTM, and attention become important, and spaCy is used for NLP. 
CNN、LSTM、アテンションなどの深層学習技術が重要になり、NLPにはspaCyが使用されます。

On the back of deep image-analysis techniques, multimedia data also makes a return. 
深層画像分析技術の進展に伴い、マルチメディアデータも再び注目されるようになります。



## 4. Discussion 議論

Based on the analysis, this section will discuss each main theme in our analysis framework. 
分析に基づいて、このセクションでは私たちの分析フレームワークの各主要テーマについて議論します。

We will then answer the four research questions posed in the Introduction and discuss the limitations of our article.  
次に、序論で提示された4つの研究質問に答え、私たちの記事の限界について議論します。

### 4.1. Conceptual Framework 概念フレームワーク

The conceptual framework that results from populating our analysis framework with the most frequently used sub-themes from the analysis shows which areas and aspects of semantic knowledge graphs for news that have so far been most explored in the literature.  
私たちの分析フレームワークに分析から最も頻繁に使用されるサブテーマを埋め込むことで得られる概念フレームワークは、ニュースのためのセマンティック知識グラフに関して、これまで文献で最も探求されてきた領域と側面を示しています。

It can be used both as an overview of the research area, as grounds for further theory building, and as a guide for further research.  
これは、研究領域の概要、さらなる理論構築の根拠、そしてさらなる研究のガイドとして使用できます。

The earliest versions of our framework also contained geographical region as a top-level theme, alongside news domain and language, but very few of our main papers were specific to a region, and never exclusively so.  
私たちのフレームワークの初期バージョンには、ニュースドメインや言語と並んで地理的地域がトップレベルのテーマとして含まれていましたが、私たちの主要な論文の中で特定の地域に特化したものは非常に少なく、決して独占的ではありませんでした。

For example, although the contextualisation of open government data in Sarmiento Suárez and Jiménez-Guarín focuses on Colombian politics, the proposed solution is straightforwardly adaptable to other regions.  
例えば、Sarmiento SuárezとJiménez-Guarínによるオープンガバメントデータの文脈化はコロンビアの政治に焦点を当てていますが、提案された解決策は他の地域にも簡単に適応可能です。

### 4.2. Implications for Practice 実践への示唆

For each main theme, this section suggests implications for practice, before the next section proposes paths for further research.  
各主要テーマについて、このセクションでは実践への示唆を提案し、次のセクションではさらなる研究の道筋を提案します。

**Technical result types**: There are already many tools and techniques available that are sufficiently developed to be tested in industrial workflows.  
**技術的結果の種類**: すでに産業ワークフローでテストするのに十分に開発された多くのツールや技術があります。

Commercial tools such as VLX-Stories and ViewerPro are also starting to emerge.  
VLX-StoriesやViewerProなどの商業ツールも登場し始めています。

But most research proposals are either research pipelines/prototypes or standalone components that require considerable effort to integrate into existing workflows before they can become productive.  
しかし、ほとんどの研究提案は、研究パイプライン/プロトタイプまたはスタンドアロンコンポーネントであり、生産的になる前に既存のワークフローに統合するためにかなりの努力を必要とします。

Pilot projects that match high-benefit tasks with low-risk technologies and tools are therefore essential to successfully introduce semantic KGs in newsrooms.  
したがって、高利益のタスクと低リスクの技術やツールを組み合わせたパイロットプロジェクトは、ニュースルームにセマンティックKGを成功裏に導入するために不可欠です。

**Empirical result types**: Although there are examples of tools and techniques that have been deployed in real news production workflows, they are the exception rather than the rule.  
**実証的結果の種類**: 実際のニュース制作ワークフローで展開されたツールや技術の例はありますが、それは例外であり、一般的ではありません。

This poses a double challenge for newsrooms that want to use KGs for news: It is usually not known how robust the proposed techniques and tools are in practice, and it is usually not known how well they fit actual industrial needs.  
これは、ニュースのためにKGを使用したいニュースルームにとって二重の課題を提示します: 提案された技術やツールが実際にどれほど堅牢であるかは通常知られておらず、実際の産業ニーズにどれほど適合するかも通常知られていません。

Introducing KGs into newsrooms must therefore focus on continuous evaluation both of the technology itself and of its consequences, opening possibilities for collaboration between industry (which wants its projects evaluated) and researchers (who want access to industrial cases and data).  
したがって、ニュースルームにKGを導入するには、技術自体とその結果の両方の継続的な評価に焦点を当てる必要があり、産業（プロジェクトの評価を望む）と研究者（産業ケースやデータへのアクセスを望む）との間の協力の可能性を開きます。

**Intended users**: The most mature solutions support journalists through tools and techniques for searching, archiving, and content recommendation.  
**対象ユーザー**: 最も成熟したソリューションは、検索、アーカイブ、およびコンテンツ推薦のためのツールや技術を通じてジャーナリストを支援します。

The general news user is supported by proposals for news recommendation and to some extent searching.  
一般のニュースユーザーは、ニュース推薦やある程度の検索に関する提案によって支援されています。

**Tasks**: The most mature research proposals target long-researched tasks such as semantic annotation, searching, and recommendation, both for content retrieval (pull) and provision (push).  
**タスク**: 最も成熟した研究提案は、セマンティックアノテーション、検索、および推薦など、長年研究されてきたタスクを対象としています。これは、コンテンツの取得（プル）と提供（プッシュ）の両方に該当します。

In particular, annotation of news texts with links to mentioned entities and concepts is already used in practice and will become even more useful as the underlying language models continue to improve.  
特に、言及されたエンティティや概念へのリンクを持つニューステキストのアノテーションはすでに実践で使用されており、基盤となる言語モデルが改善されるにつれてさらに有用になるでしょう。

Semantic searching and browsing are also well-understood areas.  
セマンティック検索やブラウジングもよく理解されている分野です。

Semantic enrichment with information from open KGs and other sources is a maturing area that builds on a long line of research, but suffers from the danger of creating information overload.  
オープンKGや他のソースからの情報によるセマンティックエンリッチメントは、長い研究の系譜に基づく成熟した分野ですが、情報過多を引き起こす危険性に悩まされています。

Rising areas that are becoming available for pilot projects are automatic news detection and automatic provision of background information.  
パイロットプロジェクトに利用可能になりつつある新たな分野は、自動ニュース検出と自動的な背景情報の提供です。

**Input data**: The most mature tools and techniques are text-based.  
**入力データ**: 最も成熟したツールと技術はテキストベースです。

When multimedia is supported, it is often done indirectly by first converting speech to text or by using image captions only.  
マルチメディアがサポートされる場合、それはしばしば音声をテキストに変換するか、画像キャプションのみを使用することによって間接的に行われます。

Newer approaches that exploit native audio and image analysis techniques in combination with semantic KGs may soon become ready for industrial trials.  
セマンティックKGと組み合わせたネイティブオーディオおよび画像分析技術を活用する新しいアプローチは、すぐに産業試験の準備が整うかもしれません。

Many newsrooms already have experience with robots that exploit input data from sensors, the Internet of Things (IoT), and open APIs.  
多くのニュースルームは、センサー、IoT（モノのインターネット）、およびオープンAPIからの入力データを活用するロボットの経験をすでに持っています。

This creates opportunities to explore new uses of semantic KGs that augment existing robot-journalism tools and techniques.  
これにより、既存のロボットジャーナリズムツールや技術を拡張するセマンティックKGの新しい使用法を探求する機会が生まれます。

Much of the research that exploits social media is based on Twitter.  
ソーシャルメディアを活用する研究の多くはTwitterに基づいています。

This poses a challenge, because Twitter use is dwindling in some parts of the world, sometimes with traffic moving to more closed platforms, such as Instagram, Snapchat, Telegram, TikTok, WhatsApp, and so on.  
これは課題を提示します。なぜなら、Twitterの使用は世界の一部で減少しており、時にはトラフィックがInstagram、Snapchat、Telegram、TikTok、WhatsAppなどのより閉じたプラットフォームに移動しているからです。

In response, news organisations could attempt to host more social reader interactions inside their own distribution platforms, where they retain access to the user-generated content.  
これに応じて、ニュース組織は、ユーザー生成コンテンツへのアクセスを保持する自社の配信プラットフォーム内で、より多くのソーシャルリーダーインタラクションをホストしようとするかもしれません。

Semantic KGs offer opportunities through their support for personalisation, recommendation, and networking.  
セマンティックKGは、パーソナライズ、推薦、ネットワーキングのサポートを通じて機会を提供します。

**News life cycle**: Low-risk starting points for industrial trials are the mature research areas based on already-published news, such as archive management, recommendation, and semantically enriched search.  
**ニュースライフサイクル**: 産業試験の低リスクの出発点は、アーカイブ管理、推薦、セマンティックに強化された検索など、すでに公開されたニュースに基づく成熟した研究分野です。

Automated detection of emerging news events and live monitoring of breaking news situations are higher-risk areas that also offer high potential rewards.  
新たなニュースイベントの自動検出や、速報ニュース状況のライブモニタリングは、高リスクでありながら高い潜在的報酬を提供する分野です。

**Semantic techniques**: Because they tend to rely on standard semantic techniques, many of the proposed techniques can be run in the cloud, for example, in Amazon's Neptune-centric KG ecosystem and supported by other Amazon Web Services for NLP and ML/DL.  
**セマンティック技術**: 標準的なセマンティック技術に依存する傾向があるため、提案された多くの技術はクラウドで実行でき、例えば、AmazonのNeptune中心のKGエコシステムや、NLPおよびML/DLのための他のAmazon Web Servicesによってサポートされています。

Cloud infrastructures give newsrooms a way to explore advanced computation- and storage-intensive KG-based solutions without investing heavily upfront in new infrastructure.  
クラウドインフラストラクチャは、ニュースルームに新しいインフラストラクチャに多額の初期投資をせずに、計算およびストレージ集約型のKGベースのソリューションを探求する方法を提供します。

**Other techniques**: The demonstrated ability of KG-based approaches to work alongside a wide variety of other computing techniques and tools suggests that newsrooms that want to exploit semantic KGs should build on what they already have in place, using KG-based techniques to augment existing services and capabilities.  
**その他の技術**: KGベースのアプローチがさまざまな他の計算技術やツールと連携して機能する能力が示されていることは、セマンティックKGを活用したいニュースルームが、既存のサービスや能力を拡張するためにKGベースの技術を使用して、すでに持っているものを基に構築すべきであることを示唆しています。

For example, KGs are well suited to integrate diverse information sources through exchange standards such as RDF and SPARQL and ontologies expressed in RDFS and OWL.  
例えば、KGは、RDFやSPARQLなどの交換標準や、RDFSやOWLで表現されたオントロジーを通じて多様な情報源を統合するのに適しています。

One possibility is therefore to introduce them in newsrooms as part of ML and DL initiatives that need input data from multiple and diverse sources, whether internal or external.  
したがって、1つの可能性は、内部または外部の多様なソースからの入力データを必要とするMLおよびDLイニシアチブの一部として、ニュースルームにKGを導入することです。

Semantic analysis of natural language texts, audio, images, and video is rapidly becoming available as increasingly powerful commodity services.  
自然言語テキスト、オーディオ、画像、ビデオのセマンティック分析は、ますます強力なコモディティサービスとして急速に利用可能になっています。

KGs in newsrooms could be positioned to enrich and exploit the outputs of such services, acting as a hub that can represent and integrate the results of ML- and DL-driven analysis tools and prepare the data for journalists and others.  
ニュースルームにおけるKGは、そのようなサービスの出力を豊かにし、活用するために位置付けられ、MLおよびDL駆動の分析ツールの結果を表現し統合し、ジャーナリストや他の人々のためにデータを準備するハブとして機能することができます。

**News domain**: For newsrooms that want to exploit KGs, the most mature domains are business and finance.  
**ニュースドメイン**: KGを活用したいニュースルームにとって、最も成熟したドメインはビジネスとファイナンスです。

For example, ViewerPro, an industrial tool for ontology-based semantic analysis and annotation of news texts, has been applied to gain effective access to relevant finance news.  
例えば、ニューステキストのオントロジーに基づくセマンティック分析とアノテーションのための産業ツールであるViewerProは、関連する金融ニュースへの効果的なアクセスを得るために適用されています。

The proposed tools and techniques are often transferable across domains and purposes.  
提案されたツールや技術は、しばしばドメインや目的を超えて移転可能です。

Good candidates for industrial uptake are domains that are characterised by data streams that are reliable and high-quality, but insufficiently structured for currently available tools, e.g., for robot journalism.  
産業での採用に適した良い候補は、信頼性が高く高品質なデータストリームを特徴とするドメインですが、現在利用可能なツールには十分に構造化されていないものです。例えば、ロボットジャーナリズムのためのものです。

Using KG-techniques to expand the reach and capabilities of existing journalistic robots may be a path to reap quick benefits from KGs on top of existing infrastructures.  
KG技術を使用して既存のジャーナリズムロボットのリーチと能力を拡大することは、既存のインフラストラクチャの上にKGから迅速な利益を得るための道かもしれません。

**Language**: Given the focus on English in the research on semantic KG for the news and on NLP in general, international news is a natural starting point for newsrooms in non-English speaking countries that want to explore KG-based solutions.  
**言語**: ニュースのためのセマンティックKGに関する研究や一般的なNLPにおける英語への焦点を考えると、国際ニュースはKGベースのソリューションを探求したい非英語圏のニュースルームにとって自然な出発点です。

For newsrooms in English and other major-language countries, KG-powered cross-lingual and language-agnostic services can be used to simplify searching, accessing, and analysing minor-language resources, offering a low-effort/high-reward path to introducing semantic KGs.  
英語および他の主要言語国のニュースルームでは、KGを活用したクロスリンガルおよび言語に依存しないサービスを使用して、マイナー言語リソースの検索、アクセス、および分析を簡素化することができ、セマンティックKGを導入するための低コスト/高リターンの道を提供します。

### 4.3. Implications for Research 研究への示唆

Based on our analysis of main papers, this section proposes paths for further research.  
主要な論文の分析に基づいて、このセクションではさらなる研究の道筋を提案します。

**Technical result types**: More industrial-grade prototypes and platforms are needed in response to the call for industrial testing.  
**技術的結果の種類**: 産業試験の要請に応じて、より産業グレードのプロトタイプやプラットフォームが必要です。

Much of the current research, such as the exploration of deep learning and other AI areas for news purposes, is technology-driven and needs to be balanced by investigations of the needs of journalists, newsrooms, news users, and other stakeholders.  
現在の研究の多くは、ニュース目的のための深層学習や他のAI分野の探求など、技術主導であり、ジャーナリスト、ニュースルーム、ニュースユーザー、その他の利害関係者のニーズの調査によってバランスを取る必要があります。

**Empirical result types**: To better understand industrial needs, challenges, opportunities, and experiences, empirical studies are called for, using the full battery of research approaches, including case- and action-research, interview- and survey-based research, and ethnographic studies of newsrooms.  
**実証的結果の種類**: 産業のニーズ、課題、機会、経験をよりよく理解するために、ケース研究やアクションリサーチ、インタビューや調査に基づく研究、ニュースルームの民族誌的研究を含む、あらゆる研究アプローチを使用した実証研究が求められています。

Research on semantic knowledge graphs for the news might benefit from the growing and complementary body of literature on augmented, computational, and digital journalism, which focuses on the needs of newsrooms and journalists, but goes less into detail about the facilitating technologies, whether semantic or not.  
ニュースのためのセマンティック知識グラフに関する研究は、ニュースルームやジャーナリストのニーズに焦点を当てた拡張、計算、デジタルジャーナリズムに関する成長しつつある補完的な文献から利益を得るかもしれませんが、セマンティックであるかどうかにかかわらず、促進技術の詳細にはあまり触れていません。

Indeed, the research on semantic KGs for the news hardly mentions the literature on augmented/digital/data journalism which, vice versa, does not go into the specifics of KGs.  
実際、ニュースのためのセマンティックKGに関する研究は、拡張/デジタル/データジャーナリズムに関する文献にはほとんど言及しておらず、逆にKGの具体的な内容には触れていません。

Most papers that propose new techniques or tools offer at least some empirical evaluation of their own proposals.  
新しい技術やツールを提案するほとんどの論文は、自らの提案の少なくとも一部の実証評価を提供しています。

Experimental evaluations using gold-standard datasets and information-retrieval measures are becoming increasingly common, but there is no convergence yet towards particular gold-standard datasets and measures, which makes it hard to compare proposals and assess overall progress.  
ゴールドスタンダードデータセットや情報検索指標を使用した実験的評価はますます一般的になっていますが、特定のゴールドスタンダードデータセットや指標への収束はまだなく、提案を比較し全体的な進捗を評価することが難しくなっています。

This is an important methodological challenge for further research.  
これはさらなる研究にとって重要な方法論的課題です。

We also find no papers that focus on evaluating tools or techniques proposed by others.  
他の人が提案したツールや技術の評価に焦点を当てた論文も見当たりません。

Also, the papers that develop pipelines and prototypes are seldom explicit about the design research method they have followed.  
また、パイプラインやプロトタイプを開発する論文は、彼らが従ったデザイン研究方法について明示的であることはほとんどありません。



. Also, the papers that develop pipelines and prototypes are seldom explicit about the design research method they have followed.  
また、パイプラインやプロトタイプを開発する論文は、従ったデザイン研究方法について明示的であることはほとんどありません。  

**Intended users**: We found no papers discussing semantic knowledge graphs and related techniques for citizen journalism, for example, investigating social semantic journalism.  
**対象ユーザー**: 市民ジャーナリズムに関するセマンティック知識グラフや関連技術について議論している論文は見つかりませんでした。たとえば、社会的セマンティックジャーナリズムを調査することです。  
Local journalism is also not a current focus, and we found few papers that explicitly mention newsrooms or consider the social and organisational sides of news production and journalism.  
地域ジャーナリズムも現在の焦点ではなく、ニュースルームを明示的に言及したり、ニュース制作やジャーナリズムの社会的および組織的側面を考慮した論文はほとんど見つかりませんでした。  
There is also no mentioning of robot journalism in the main papers.  
主要な論文にはロボットジャーナリズムについての言及もありません。  

**Tasks**: More research is needed in areas that are critical for representing news content on a deeper level, beyond semantic annotation with named entities, concepts, and topics.  
**タスク**: 名前付きエンティティ、概念、トピックによるセマンティックアノテーションを超えて、ニュースコンテンツをより深いレベルで表現するために重要な分野でのさらなる研究が必要です。  
Central evolving areas are event detection, relation extraction, and KG updating, in particular identification and semantic analysis of dark entities and relations.  
中心的な進化分野は、イベント検出、関係抽出、KGの更新であり、特にダークエンティティと関係の特定およびセマンティック分析です。  

There is little research on the quality of data behind semantic KGs for news.  
ニュースのためのセマンティックKGの背後にあるデータの質に関する研究はほとんどありません。  
Aspects of semantic data quality, such as privacy, provenance, ownership, and terms of use, need more attention.  
プライバシー、出所、所有権、利用規約などのセマンティックデータの質に関する側面には、より多くの注意が必要です。  
Few research proposals target or undertake multimedia analysis natively (i.e., without going through text) and specifically for news.  
ニュースのために、マルチメディア分析をネイティブに（すなわち、テキストを介さずに）対象とする研究提案はほとんどありません。  

**Input data**: The research on social media tends to focus on short texts, which are hard to analyse, because they provide less context and use abbreviations, neologisms, and hashtags.  
**入力データ**: ソーシャルメディアに関する研究は、短いテキストに焦点を当てる傾向があり、文脈が少なく、略語、新語、ハッシュタグを使用するため、分析が難しいです。  
More context can be provided by integrating newer techniques that also analyse the audio, image, and video content in social messages.  
ソーシャルメッセージの音声、画像、動画コンテンツを分析する新しい技術を統合することで、より多くの文脈を提供できます。  
Some research approaches harvest citizen-provided data from social media, but there are no investigations of how to use semantic techniques and tools participatively for citizen journalism.  
市民が提供したデータをソーシャルメディアから収集する研究アプローチもありますが、市民ジャーナリズムのためにセマンティック技術やツールを参加型で使用する方法についての調査はありません。  
There is little research on KGs for news that exploits data from sensors and from the IoT in general, and there is little use of open web APIs outside a few domains (such as business/finance).  
センサーやIoTからのデータを活用するニュースのためのKGに関する研究はほとんどなく、特定のドメイン（ビジネス/金融など）以外でオープンウェブAPIの使用もほとんどありません。  
We have already mentioned the ensuing possibility of combining semantic KGs with robot-journalism tools and techniques.  
私たちはすでに、セマンティックKGとロボットジャーナリズムのツールや技術を組み合わせる可能性について言及しました。  
GDELT is another untapped resource, although data quality and ownership is an issue.  
GDELTは別の未開発のリソースですが、データの質と所有権が問題です。  
Research is needed on how its data quality can be corroborated and improved.  
そのデータの質をどのように確認し、改善できるかについての研究が必要です。  
Also, the low-level events in GDELT data streams need to be aggregated into news-level events.  
また、GDELTデータストリームの低レベルのイベントは、ニュースレベルのイベントに集約する必要があります。  

**News life cycle**: Relatively little research targets detecting emerging news events, monitoring breaking news situations, and following developing stories.  
**ニュースライフサイクル**: 新たに発生するニュースイベントの検出、速報ニュースの状況の監視、発展するストーリーの追跡を対象とした研究は比較的少ないです。  
Event detection and tracking as well as detecting emerging entities and relations are important research challenges.  
イベントの検出と追跡、ならびに新たに出現するエンティティや関係の検出は重要な研究課題です。  

**Semantic techniques**: Most of the research uses existing news corpora or harvests news articles on-demand.  
**セマンティック技術**: ほとんどの研究は既存のニュースコーパスを使用するか、オンデマンドでニュース記事を収集します。  
There is less focus on building and curating journalistic knowledge graphs over time.  
時間をかけてジャーナリスティックな知識グラフを構築し、キュレーションすることに対する関心は少ないです。  
Due to the high volume, velocity, and variety of news-related information, semantic news KGs are a potential driver and test bed for real-time and big-data semantic KGs.  
ニュース関連情報の高いボリューム、速度、バラエティのため、セマンティックニュースKGはリアルタイムおよびビッグデータセマンティックKGの潜在的な推進力およびテストベッドです。  
More research is therefore needed on combining KGs with state-of-the-art techniques for real-time processing and big data.  
したがって、KGをリアルタイム処理およびビッグデータの最先端技術と組み合わせるためのさらなる研究が必要です。  
Yet, none of the main papers have primary focus on the design of semantic data architectures/infrastructures for newsrooms, for example, using big-data infrastructures, data lakes, web-service orchestrations, and so on.  
しかし、主要な論文のいずれも、ニュースルームのためのセマンティックデータアーキテクチャ/インフラストラクチャの設計に主に焦点を当てていません。たとえば、ビッグデータインフラストラクチャ、データレイク、ウェブサービスのオーケストレーションなどを使用しています。  
The most big-data-ready research proposal is NewsReader, through its connection with the big-data ready KnowledgeStore repository.  
最もビッグデータに対応した研究提案は、ビッグデータ対応のKnowledgeStoreリポジトリとの接続を通じてのNewsReaderです。  
The News Hunter platform developed in the News Angler project is also built on top of a big-data ready infrastructure.  
News Anglerプロジェクトで開発されたNews Hunterプラットフォームも、ビッグデータ対応のインフラストラクチャの上に構築されています。  
In addition to supporting processing of big data in real time, these architectures and infrastructures must be forward-engineered to accommodate the increasing availability of high-quality, high-performance commodity cloud-services for NLP, ML, and DL that can be exploited by news organisations.  
ビッグデータのリアルタイム処理をサポートするだけでなく、これらのアーキテクチャとインフラストラクチャは、ニュース組織が活用できる高品質で高性能なコモディティクラウドサービス（NLP、ML、DL用）の利用可能性の増加に対応するように前方設計される必要があります。  

**Other techniques**: On the research side, few approaches to semantic KGs for news exploit recent advances in image understanding and speech recognition.  
**その他の技術**: 研究の側面では、ニュースのためのセマンティックKGに対するアプローチは、画像理解や音声認識の最近の進展を活用しているものはほとんどありません。  
There is a potential for cross-modal solutions that increase precision and recall by combining analyses of text, audio, images and, eventually, video.  
テキスト、音声、画像、そして最終的には動画の分析を組み合わせることで、精度と再現率を向上させるクロスモーダルソリューションの可能性があります。  
These solutions need to be integrated with semantic KGs, and their application should focus on areas where KGs bring additional benefits, such as infusing world and common-sense knowledge into existing analyses.  
これらのソリューションはセマンティックKGと統合する必要があり、その適用はKGが追加の利点をもたらす領域、たとえば、既存の分析に世界的および常識的な知識を注入することに焦点を当てるべきです。  
Also, few approaches so far exploit big-data and real-time computing.  
また、これまでのところ、ビッグデータやリアルタイムコンピューティングを活用するアプローチはほとんどありません。  
Although some proposals express real-time ambitions, they are seldom evaluated on real-volume and -velocity data streams and, when they are (e.g., RDFLiveNews and SPEED), they do not approach web-scale performance.  
いくつかの提案はリアルタイムの野心を表明していますが、実際のボリュームと速度のデータストリームで評価されることはほとんどなく、評価される場合（例：RDFLiveNewsやSPEED）でも、ウェブスケールのパフォーマンスには達していません。  
Although the proposed research pipelines may not be optimised for speed, performance-evaluation results suggest that more efficient algorithms are needed, for example, running on staged and parallel architectures.  
提案された研究パイプラインは速度の最適化がされていないかもしれませんが、パフォーマンス評価の結果は、より効率的なアルゴリズムが必要であることを示唆しています。たとえば、段階的および並列アーキテクチャで実行することです。  
High-performance technologies for massively distributed news knowledge graphs are also called for, for example, exploiting big-graph databases such as Pregel and Giraph.  
大規模に分散されたニュース知識グラフのための高性能技術も求められており、たとえば、PregelやGiraphのようなビッググラフデータベースを活用することです。  

**News domain**: Whereas practical applications of KGs may be driven by economical (for economy/finance) and popular (e.g., for sports) interests, there is ample opportunity on the research side for adapting and tuning existing approaches to new and unexplored domains that have high societal value.  
**ニュースドメイン**: KGの実用的な応用は経済（経済/金融）や人気（スポーツなど）の関心によって推進されるかもしれませんが、社会的価値の高い新しい未開拓のドメインに既存のアプローチを適応させ、調整するための研究の側面には十分な機会があります。  
One largely unexplored domain is corruption and political nepotism, along the lines suggested in the literature.  
文献で示唆されているように、腐敗や政治的縁故主義は、ほとんど探求されていないドメインの一つです。  
Misinformation is another area of great importance, and in the domain of crises and social unrest, the GDELT data streams may offer opportunities.  
誤情報はもう一つの重要な領域であり、危機や社会的不安のドメインにおいて、GDELTデータストリームは機会を提供するかもしれません。  

**Language**: Research is needed to make semantic KGs for news available for smaller languages.  
**言語**: ニュースのためのセマンティックKGを小さな言語で利用可能にするための研究が必要です。  
There is so far little uptake of cross-language models like multi-lingual BERT and little research on exploiting dedicated language models for smaller languages for news purposes.  
これまでのところ、マルチリンガルBERTのようなクロスランゲージモデルの採用は少なく、ニュース目的のために小さな言語用の専用言語モデルを活用する研究もほとんどありません。  

### 4.4. Research Questions  
### 4.4. 研究課題  

We are now ready to answer the four research questions we posed in the Introduction.  
私たちは、序論で提起した4つの研究課題に答える準備が整いました。  

**RQ1**: Which research problems and approaches are most common, and what are the central results?  
**RQ1**: 最も一般的な研究課題とアプローチは何であり、中心的な結果は何ですか？  
The review shows that research on semantic knowledge graphs for news is highly diverse and in constant flux as the enabling technologies evolve.  
レビューは、ニュースのためのセマンティック知識グラフに関する研究が非常に多様であり、支援技術が進化するにつれて常に変化していることを示しています。  
A frequent type of paper is one that develops new tools and techniques for representing news semantically to disseminate news content more effectively.  
頻繁に見られるタイプの論文は、ニュースコンテンツをより効果的に普及させるためにニュースをセマンティックに表現する新しいツールや技術を開発するものです。  
In response to the increasing societal importance of information quality and misinformation, there is currently a rapidly growing interest in fake-news detection and fact checking.  
情報の質と誤情報の社会的重要性が高まる中、現在、フェイクニュース検出やファクトチェックに対する関心が急速に高まっています。  
The tools and techniques are typically developed as pipelines or prototypes and evaluated using experiments, examples or use cases.  
ツールや技術は通常、パイプラインやプロトタイプとして開発され、実験、例、またはユースケースを使用して評価されます。  
The experimental methods used are maturing.  
使用される実験方法は成熟しています。  

**RQ2**: Which research problems and approaches have received less attention, and what types of contributions are rarer?  
**RQ2**: どの研究課題とアプローチがあまり注目されておらず、どのような貢献がより少ないですか？  
Our discussion identifies many under-researched areas.  
私たちの議論は、多くの未研究の領域を特定しています。  
The review shows that there are very few industrial case studies.  
レビューは、産業ケーススタディが非常に少ないことを示しています。  
In our literature searches, we have found few surveys and reviews.  
私たちの文献検索では、調査やレビューがほとんど見つかりませんでした。  
There is also little research on issues such as privacy, ownership, terms of use, and provenance, although a few papers mention the latter.  
プライバシー、所有権、利用規約、出所などの問題に関する研究もほとんどありませんが、いくつかの論文が後者に言及しています。  
Only a few papers focus on evaluating their results in real-time and big-data settings and, when they do, the results are often in need of improvement.  
リアルタイムおよびビッグデータの設定で結果を評価することに焦点を当てた論文はごくわずかで、評価される場合でも、結果はしばしば改善が必要です。  
Other green-field areas include: exploiting location data and data from the Internet of Things, supporting social and citizen journalism, using semantic knowledge graphs to identify new newsworthy events as in Reuters Tracer, and using semantic knowledge graphs to construct narratives and generate news content.  
他の未開拓の分野には、位置データやIoTからのデータを活用すること、社会的および市民ジャーナリズムを支援すること、Reuters Tracerのようにセマンティック知識グラフを使用して新しいニュース価値のあるイベントを特定すること、セマンティック知識グラフを使用して物語を構築し、ニュースコンテンツを生成することが含まれます。  

Although the results suggest that semantic knowledge graphs can indeed support better organisation, management, retrieval, and dissemination of news content, there is still a potential for much larger uptake in industry.  
結果は、セマンティック知識グラフがニュースコンテンツのより良い組織、管理、検索、普及をサポートできることを示唆していますが、業界でのより大きな採用の可能性はまだあります。  
Empirical studies are needed to explain why.  
その理由を説明するためには、実証的な研究が必要です。  
One possible explanation is that there is a mismatch between what the current tools and algorithms offer and what the industry needs.  
一つの可能な説明は、現在のツールやアルゴリズムが提供するものと、業界が必要とするものとの間にミスマッチがあることです。  
Another possible explanation is that the solutions themselves are immature, for example, that existing analysis techniques are not sufficiently precise or that the often crowd-sourced reference and training data used are perceived as less trustworthy.  
別の可能な説明は、ソリューション自体が未成熟であることです。たとえば、既存の分析技術が十分に正確でないか、しばしばクラウドソーシングされた参照データやトレーニングデータが信頼性が低いと見なされていることです。  

**RQ3**: How is the research evolving?  
**RQ3**: 研究はどのように進化していますか？  
Our analysis shows that the research broadly follows the development of the supporting technologies used.  
私たちの分析は、研究が使用される支援技術の発展に広く従っていることを示しています。  
We identify four eras in the evolution of KGs for news, characterised by (1) applying early Semantic-Web ideas to the news domain, (2) exploiting the Linked Open Data (LOD) cloud for news purposes, (3) semantic knowledge graphs and machine learning and, most recently, (4) deep-learning approaches based on semantic knowledge graphs.  
ニュースのためのKGの進化には、(1) 初期のセマンティックウェブのアイデアをニュースドメインに適用すること、(2) ニュース目的のためにリンクドオープンデータ（LOD）クラウドを活用すること、(3) セマンティック知識グラフと機械学習、そして最近では、(4) セマンティック知識グラフに基づく深層学習アプローチの4つの時代があることを特定します。  

**RQ4**: Which are the most frequently cited papers and projects, and which papers and projects are citing one another?  
**RQ4**: 最も頻繁に引用される論文やプロジェクトはどれで、どの論文やプロジェクトが互いに引用していますか？  
The most cited papers are the ones about DKN and KIM.  
最も引用されている論文は、DKNとKIMに関するものです。  
Many recent papers that use deep-learning techniques for fake-news detection or recommendation are already much cited.  
フェイクニュース検出や推薦のために深層学習技術を使用する最近の多くの論文は、すでに多く引用されています。  
Among the central projects, main papers related to the Hermes, NewsReader, and NEWS projects have been most cited.  
中心的なプロジェクトの中で、Hermes、NewsReader、NEWSプロジェクトに関連する主要な論文が最も引用されています。  
Another much-referenced group of papers centres around what we have called the "MediaLoep" collaboration.  
もう一つの多く引用される論文のグループは、私たちが「MediaLoep」コラボレーションと呼んでいるものに中心を置いています。  
The citation analysis shows that the main paper from the Neptuno project and the effort to make IPTC's news architecture semantic also are important.  
引用分析は、Neptunoプロジェクトの主要な論文と、IPTCのニュースアーキテクチャをセマンティックにする努力も重要であることを示しています。  

### 4.5. Limitations  
### 4.5. 制限事項  

The most central limitation of our literature review is its scope.  
私たちの文献レビューの最も中心的な制限は、その範囲です。  
We only consider papers that use semantic knowledge graphs or related semantic techniques for news-related purposes, excluding papers that attempt to solve similar problems using other knowledge representation techniques or targeting other domains.  
私たちは、ニュース関連の目的のためにセマンティック知識グラフや関連するセマンティック技術を使用する論文のみを考慮し、他の知識表現技術を使用して類似の問題を解決しようとする論文や、他のドメインを対象とする論文は除外します。  
There is also a growing body of research on representing texts in general as semantic knowledge graphs, proposing techniques and tools that could also be used to analyse news.  
一般的にテキストをセマンティック知識グラフとして表現する研究も増えており、ニュースを分析するために使用できる技術やツールを提案しています。  



. There is also a growing body of research on representing texts in general as semantic knowledge graphs, proposing techniques and tools that could also be used to analyse news. 
一般的にテキストを意味的知識グラフとして表現する研究が増えており、ニュースを分析するために使用できる技術やツールが提案されています。

There is another growing body of research on supporting news with knowledge graphs that are not semantically linked, i.e., with knowledge graphs whose nodes and edges do not link into the LOD cloud.
意味的にリンクされていない知識グラフ、すなわちノードとエッジがLODクラウドにリンクしていない知識グラフを用いてニュースを支援する研究も増えています。



## 5. Conclusion 結論

We have reported a systematic literature review of research on how semantic knowledge graphs can be used to facilitate all aspects of production, dissemination, and consumption of news. 
私たちは、セマンティック知識グラフがニュースの生産、普及、消費のすべての側面を促進するためにどのように使用できるかに関する研究の体系的な文献レビューを報告しました。 
Starting with more than 6,000 papers, we identified 80 main papers that we analysed in depth according to an analysis framework that we kept refining as analysis progressed. 
6,000以上の論文から始めて、私たちは80の主要な論文を特定し、分析が進むにつれて洗練させていった分析フレームワークに従って深く分析しました。 
As a result, we have been able answer research questions about past, current, and emerging research areas and trends, and Section 4.3 has offered many paths for further work. 
その結果、過去、現在、そして新たに出現する研究分野やトレンドに関する研究質問に答えることができ、セクション4.3ではさらなる研究のための多くの道筋を提供しました。 
We hope the results of our study will be useful for practitioners and researchers who are interested specifically in semantic knowledge graphs for news or more generally in computational journalism or in semantic knowledge graphs. 
私たちの研究の結果が、ニュースのためのセマンティック知識グラフや、より一般的には計算ジャーナリズムやセマンティック知識グラフに特に関心のある実務者や研究者にとって有用であることを願っています。
