refs: https://arxiv.org/pdf/2310.00637


## Knowledge Engineering using Large Language Models
### Bradley P. Allen - University of Amsterdam, Amsterdam, NL
### Lise Stork - Vrije Universiteit Amsterdam, Amsterdam, NL
### Paul Groth - University of Amsterdam, Amsterdam, NL  

## 知識工学と大規模言語モデルの利用
### ブラッドリー・P・アレン - アムステルダム大学、オランダ
### リゼ・ストーク - フリー大学アムステルダム、オランダ
### ポール・グロス - アムステルダム大学、オランダ  

### Abstract

Knowledge engineering is a discipline that focuses on the creation and maintenance of processes that generate and apply knowledge. 
知識工学は、知識を生成し適用するプロセスの創造と維持に焦点を当てた学問です。 
Traditionally, knowledge engineering approaches have focused on knowledge expressed in formal languages. 
従来、知識工学のアプローチは、形式言語で表現された知識に焦点を当ててきました。 
The emergence of large language models and their capabilities to effectively work with natural language, in its broadest sense, raises questions about the foundations and practice of knowledge engineering. 
大規模言語モデルの出現と、自然言語（その最も広い意味で）を効果的に扱う能力は、知識工学の基盤と実践に関する疑問を提起します。 
Here, we outline the potential role of LLMs in knowledge engineering, identifying two central directions: 1) creating hybrid neuro-symbolic knowledge systems; and 2) enabling knowledge engineering in natural language. 
ここでは、**知識工学におけるLLMsの潜在的な役割を概説し、2つの中心的な方向性を特定します：1）ハイブリッド神経シンボリック知識システムの作成；2）自然言語における知識工学の実現。** 
Additionally, we formulate key open research questions to tackle these directions. 
さらに、これらの方向性に取り組むための重要なオープンリサーチクエスチョンを定式化します。  

**2012 ACM Subject Classification Computing methodologies** Natural language processing, Computing methodologies Machine learning, Computing methodologies Philosophical/theoretical foundations of artificial intelligence, Software and its engineering Software development methods  
**2012 ACM主題分類 コンピューティング手法** 自然言語処理、コンピューティング手法 機械学習、コンピューティング手法 人工知能の哲学的/理論的基盤、ソフトウェアとその工学 ソフトウェア開発手法  
**Keywords and Phrases knowledge engineering, large language models**  
**キーワードとフレーズ 知識工学、大規模言語モデル**  
**[Digital Object Identifier 10.1234/0000000.00000000](https://doi.org/10.1234/0000000.00000000)**  
**デジタルオブジェクト識別子 10.1234/0000000.00000000**  
**Received 2023-07-14 Accepted To be completed by Dagstuhl editorial office Published To be completed by Dagstuhl editorial office**  
**受理日 2023-07-14 採択日 ダグシュタール編集部によって完了予定 発行日 ダグシュタール編集部によって完了予定**  

<!-- ここまで読んだ! -->

### 1 Introduction  

Knowledge engineering (KE) is a discipline concerned with the development and maintenance of automated processes that generate and apply knowledge [4, 93]. 
知識工学（KE）は、知識を生成し適用する自動化プロセスの開発と維持に関する学問です[4, 93]。 
Knowledge engineering rose to prominence in the nineteen-seventies, when Edward Feigenbaum and others became convinced that automating knowledge production through the application of research into artificial intelligence required a domain-specific focus [32]. 
知識工学は1970年代に注目を集め、エドワード・フェイゲンバウムらが人工知能に関する研究の応用を通じて知識生産を自動化するには、ドメイン特化型の焦点が必要であると確信しました[32]。 
The period from the mid-nineteen-seventies into the nineteen-eighties saw the knowledge engineering of rule-based expert systems for the purposes of the automation of decision making in business enterprise settings. 
1970年代中頃から1980年代にかけて、ビジネス企業の意思決定の自動化を目的としたルールベースのエキスパートシステムの知識工学が行われました。 
By the early nineteen-nineties, however, it became clear that the expert systems approach, given its dependence on manual knowledge acquisition and rule-based representation of knowledge by highly skilled knowledge engineers, resulted in systems that were expensive to maintain and difficult to adapt to changing requirements or application contexts. 
しかし、**1990年代初頭には、エキスパートシステムアプローチが、高度な知識エンジニアによる手動の知識取得とルールベースの知識表現に依存しているため、維持が高コスト**で、変化する要件やアプリケーションコンテキストに適応するのが難しいシステムを生み出すことが明らかになりました。 
Feigenbaum argued that, to be successful, future knowledge-based systems would need to be scalable, globally distributed, and interoperable [34]. 
フェイゲンバウムは、成功するためには、将来の知識ベースシステムはスケーラブルで、グローバルに分散され、相互運用可能である必要があると主張しました[34]。 

The establishment of the World Wide Web and the emergence of Web architectural principles in the mid-nineteen-nineties provided a means to address these requirements. 
1990年代中頃にワールドワイドウェブが確立され、ウェブのアーキテクチャ原則が出現したことで、これらの要件に対処する手段が提供されました。 
Tim Berners-Lee argued for a "Web of Data" based on linked data principles, standard ontologies, and data sharing protocols that established open standards for knowledge representation and delivery on and across the Web [11]. 
ティム・バーナーズ＝リーは、リンクデータ原則、標準的なオントロジー、およびデータ共有プロトコルに基づく「データのウェブ」を提唱し、ウェブ上での知識表現と配信のためのオープンスタンダードを確立しました[11]。 
The subsequent twenty years witnessed the development of a globally federated open linked data "cloud" [13], the refinement of techniques for ontology engineering [51], and methodologies for the development of knowledge-based systems [86]. 
その後の20年間で、グローバルに連携したオープンリンクデータの「クラウド」[13]の開発、オントロジー工学の技術の洗練[51]、および知識ベースシステムの開発手法[86]が進展しました。 
During the same period, increasing use of machine learning and natural language processing techniques led to new means of knowledge production through the automated extraction of knowledge from natural language documents and structured data sources [26, 68]. 
同じ期間中に、**機械学習と自然言語処理技術の利用が増加し、自然言語文書や構造化データソースからの知識の自動抽出を通じて新しい知識生産手段**が生まれました[26, 68]。 
Internet-based businesses in particular found value in using such technologies to improve access to and discovery of Web content and data [43]. 
特にインターネットベースのビジネスは、これらの技術を使用してウェブコンテンツやデータへのアクセスと発見を改善する価値を見出しました[43]。 
A consensus emerged around the use of knowledge graphs as the main approach to knowledge representation in the practice of knowledge engineering in both commercial and research arenas, providing easier reuse of knowledge across different tasks and a better developer experience for knowledge engineers [45]. 
商業および研究の両分野における知識工学の実践において、知識グラフを知識表現の主要なアプローチとして使用することに関する合意が形成され、異なるタスク間での知識の再利用が容易になり、知識エンジニアにとっての開発者体験が向上しました[45]。 

More recently, the increase in the availability of graphical processing hardware for fast matrix arithmetic, and the exploitation of such hardware to drive concurrent innovations in neural network architectures at heretofore unseen scales [106], has led to a new set of possibilities for the production of knowledge using large language models (LLMs). 
最近では、高速行列演算のためのグラフィカルプロセッシングハードウェアの利用可能性の増加と、そのようなハードウェアを利用して前例のない規模でニューラルネットワークアーキテクチャの同時革新を推進することが、 **大規模言語モデル（LLMs）を使用した知識生産の新たな可能性**をもたらしました[106]。 
LLMs are probabilistic models of natural language, trained on very large corpora of content, principally acquired from the Web. 
**LLMsは自然言語の確率モデルであり、主にウェブから取得された非常に大規模なコーパスで訓練**されています。 
Similiar to previous approaches to language modelling, given a sequence of tokens LLMs predict a probable next sequence of tokens based on a learned probability distribution of such sequences. 
**以前の言語モデリングアプローチと同様に、トークンのシーケンスが与えられると、LLMsはそのシーケンスの学習された確率分布に基づいて、次に来るトークンのシーケンスを予測**します。 
However, presumably due to the vast amount of content processed in learning and the large size and architecture of the neural networks involved, LLMs exhibit remarkable capabilities for natural language processing that far exceed earlier approaches [60]. 
しかし、**学習において処理される膨大な量のコンテンツと、関与するニューラルネットワークの大きさとアーキテクチャのために、LLMsは以前のアプローチをはるかに超える自然言語処理の驚くべき能力を示します**[60]。

<!-- ここまで読んだ! -->

These capabilities include the ability to do zero- or few-shot learning across domains [20], to generalize across tasks, including the ability to perform domain-independent question answering integrating large amounts of world knowledge [77], to generate text passages at human levels of fluency and coherence [28, 96], to deal gracefully with ambiguity and long-range dependencies in natural language [104], and to reduce or even eliminate the need for manual feature engineering [98]. 
これらの能力には、**ドメインを超えたゼロショットまたは少数ショット学習の能力[20]、タスク間の一般化、世界知識の大量統合を含むドメイン非依存の質問応答の実行能力[77]、人間レベルの流暢さと一貫性でテキストを生成する能力[28, 96]、自然言語における曖昧さや長期依存性に優雅に対処する能力[104]、および手動特徴エンジニアリングの必要性を減少または排除する能力[98]**が含まれます。 
LLMs also exhibit the ability to generate and interpret structured and semi-structured information, including programming language code [6, 100], tables [46, 53], and RDF metadata [106, 58, 7]. 
LLMsは、プログラミング言語コード[6, 100]、テーブル[46, 53]、およびRDFメタデータ[106, 58, 7]を含む構造化および半構造化情報を生成および解釈する能力も示します。 
The generalization of language models (termed "foundation models" by some) to other modalities including images and audio have led to similarly significant advances in image understanding [23, 117], image generation [38, 79, 83], speech recognition, and text-to-speech generation [78, 105]. 
言語モデルの一般化（いくつかの人によって「基盤モデル」と呼ばれる）は、画像や音声を含む他のモダリティに対しても行われ、画像理解[23, 117]、画像生成[38, 79, 83]、音声認識、テキストから音声への生成[78, 105]において同様に重要な進展をもたらしました。 
Such capabilities have prompted a significant amount of research and development activity demonstrating potential applications of LLMs [66, 84, 54]. 
このような能力は、LLMsの潜在的な応用を示す多くの研究開発活動を促進しました[66, 84, 54]。 
However, the means of incorporating LLMs into structured, controllable, and repeatable approaches to developing and fielding such applications in production use are only just beginning to be considered in detail [73]. 
しかし、**LLMsを構造化され、制御可能で、再現可能なアプローチに組み込んで、実際の使用においてそのようなアプリケーションを開発および展開する手段は、詳細に検討され始めたばかり**です[73]。 

This paper engages with the question of how LLMs can be effectively employed in the context of knowledge engineering. 
本論文は、**LLMsを知識工学の文脈でどのように効果的に活用できるか**という問題に取り組みます。 
We start by examining the different forms that knowledge can take, both as inputs for constructing knowledge systems and as outputs of such systems. 
私たちは、知識が知識システムを構築するための入力として、またそのようなシステムの出力としてどのような異なる形を取るかを検討することから始めます。 
We argue that the distinction between knowledge expressed in natural language (or other evolved, naturally occurring modalities such as images or video) and knowledge expressed in formal languages (for example, as knowledge graphs or rules), sheds light how LLMs can be brought to bear on the development of knowledge systems. 
私たちは、自然言語（または画像やビデオなどの他の進化した自然発生的モダリティ）で表現された知識と、形式言語（例えば、知識グラフやルールとして）で表現された知識の違いが、LLMsが知識システムの開発にどのように寄与できるかを明らかにすると主張します。 

<!-- ここまで読んだ! -->

Based on this perspective, we then describe two potential paths forward. 
この視点に基づいて、私たちは次に**2つの潜在的な進むべき道**を説明します。 
One approach involves treating LLMs as components within hybrid neuro-symbolic knowledge systems. 
1つのアプローチは、LLMsをハイブリッド神経シンボリック知識システム内のコンポーネントとして扱うことです。 
The other approach treats LLMs and prompt engineering [57] as a standalone approach to knowledge engineering, using natural language as the primary representation of knowledge. 
もう1つのアプローチは、LLMsとプロンプトエンジニアリング[57]を知識工学への独立したアプローチとして扱い、自然言語を知識の主要な表現として使用することです。 
We then enumerate a set of open research problems in the exploration of these paths. 
次に、これらの道を探求する中でのオープンリサーチ問題のセットを列挙します。 
These problems aim to determine the feasibility of and potential approaches to using LLMs with existing KE methodologies, as well as the development of new KE methodologies centered around LLMs and prompt engineering. 
これらの問題は、既存のKE手法とLLMsを使用することの実現可能性と潜在的なアプローチを特定することを目的としており、LLMsとプロンプトエンジニアリングを中心にした新しいKE手法の開発も含まれます。  

<!-- ここまで読んだ! -->

### 2 Forms of knowledge and their engineering 知識の形態とその工学

In the history of the computational investigation of knowledge engineering, knowledge has been often treated primarily as symbolic expressions. 
知識工学の計算的調査の歴史において、知識は主にシンボリック表現として扱われてきました。 
However, as [39] noted, knowledge is actually encoded in a variety of media and forms, most notably in natural language (e.g. English) but also in images, video, or even spreadsheets. 
しかし、[39]が指摘したように、知識は実際にはさまざまなメディアや形態にエンコードされており、特に自然言語（例：英語）だけでなく、画像、ビデオ、さらにはスプレッドシートにも存在します。 
This fact becomes even more apparent when looking at institutional knowledge practices that have developed over centuries, for example, in the sciences or archives [44]. 
この事実は、科学やアーカイブなど、何世紀にもわたって発展してきた制度的知識慣行を見ていると、さらに明らかになります[44]。 
We now illustrate this point by describing the many ways in which knowledge manifests itself in the context of biodiversity informatics. 
ここでは、生物多様性情報学の文脈において知識がどのように現れるかを説明することで、この点を示します。  

<!-- ここまで読んだ! -->

### 2.1 The multimodal richness of knowledge: an example from biodiversity sciences 生物多様性科学における知識のマルチモーダルな豊かさの例

The ultimate goal of biodiversity science is to understand species evolution, variation, and distribution, but finds applications in a variety of other fields such as climate science and policy. 
生物多様性科学の最終的な目標は、種の進化、変異、および分布を理解することであり、気候科学や政策などのさまざまな他の分野にも応用されています。 
At its heart is the collection and observation of organisms, providing evidence for deductions about the natural world [59]. 
その中心には、生物の収集と観察があり、自然界に関する推論の証拠を提供します[59]。 
Such knowledge is inherently multimodal in nature, most commonly appearing in the form of images, physical objects, tree structures and sequences, i.e., molecular data. 
このような**知識は本質的にマルチモーダルであり、最も一般的には画像、物理的オブジェクト、木構造、シーケンス（すなわち分子データ）の形で現れます。** 
Historically, organism sightings have been carefully logged in handwritten field diaries to describe species behaviour and environmental conditions. 
歴史的に、生物の目撃情報は、種の行動や環境条件を記述するために手書きのフィールドダイアリーに慎重に記録されてきました。 
Detailed drawings and later photographs were made to capture colour, organs and other knowledge about an organism’s traits used for identification, which is best conveyed visually but which is challenging to preserve in natural specimens. 
詳細な図面や後の写真は、識別に使用される生物の特性に関する色、器官、およびその他の知識を捉えるために作成され、視覚的に最もよく伝えられますが、自然標本で保存するのは難しいです。
These manuscripts are housed, together with the physical zoological specimens and herbaria which they describe, in museums and collection facilities across the world. 
これらの原稿は、記述されている物理的な動物標本や標本館と共に、世界中の博物館や収集施設に保管されています。
Both the multimodal nature of these knowledge sources as well as their distributed nature hamper knowledge integration and synthesis. 
**これらの知識源の多様なモダリティと分散した性質の両方が、知識の統合と合成を妨げています。**

Metadata describes the specimen’s provenance: where specimens were found, who found them, and provides an attempt at identifying the type of organism (such as the preserved squid specimen shown in Figure 1). 
**メタデータ**は標本の出所を説明します：標本がどこで見つかったか、誰が見つけたか、そして生物の種類を特定しようとする試みを提供します（図1に示されている保存されたイカの標本など）。
Such knowledge is paramount, as it allows researchers to understand resources within the context in which they were produced, enabling researchers to carry out ecological studies such as distribution modeling over time. 
このような知識は非常に重要であり、研究者が資源を生産された文脈の中で理解することを可能にし、時間をかけた分布モデルなどの生態学的研究を行うことを可能にします。

For a systematic comparison of the multitude of resources available, the biodiversity sciences have had a long-standing tradition of developing information standards [67]. 
利用可能な多くのリソースの体系的な比較のために、生物多様性科学は情報標準の開発に長い伝統を持っています[67]。
From Linnaeus’ Systema naturae mid 18th century as well as his formal introduction of zoological nomenclature, taxonomists have started categorizing natural specimens according to tree-like hierarchical structures. 
リンネの『自然の体系』の18世紀中頃から、彼の動物命名法の正式な導入に至るまで、分類学者は自然標本を木のような階層構造に従って分類し始めました。
The process is challenging, given that biologist up until this day do not have a full picture of all living organisms on earth, and incomplete, naturally evolved and fuzzy knowledge is not easily systematized. 
このプロセスは困難であり、今日に至るまで生物学者は地球上のすべての生物の全体像を把握しておらず、不完全で自然に進化した曖昧な知識は簡単には体系化できません。

<!-- ここまで読んだ! -->

The development of digital methods has opened up new pathways for comparison and analysis. 
**デジタル手法の発展は、比較と分析のための新しい道を開きました。**
Gene sequencing technology has lead biologist to the genetic comparison of species, by the calculation of ancestry and construction of evolutionary tree structures in the study of phylogeny [50]. 
遺伝子配列決定技術は、生物学者が系統学の研究において系譜の計算と進化的樹構造の構築を通じて種の遺伝的比較を行うことを可能にしました[50]。
More importantly, digital methods allowed the transfer of analog resources, such as specimen collection scans [14] and metadata, to the digital world. 
さらに重要なことに、デジタル手法は、標本収集スキャン[14]やメタデータなどのアナログリソースをデジタル世界に移行することを可能にしました。
Such techniques have furthered formalisation and thereby interoperability of collected data through the use of Web standards, such as globally unique identifiers for species names [72] as well as shared vocabularies for data integration across collections [10]. 
このような技術は、種名のためのグローバルにユニークな識別子[72]や、コレクション間のデータ統合のための共有語彙[10]などのWeb標準を使用することによって、収集データの形式化と相互運用性を進めました。
The Global Biodiversity Information Facility (GBIF) and their data integration toolkit serves as a great example of such integration efforts [97, 81]. 
グローバル生物多様性情報機関（GBIF）とそのデータ統合ツールキットは、そのような統合努力の優れた例となっています[97, 81]。
Currently, there is a large emphasis on linking up disparate digital resources in the creation of an interconnected network of digital collection objects on the Web, linked up with relevant ecological, environmental and other related data in support of machine actionability (i.e., the ability of computational systems to find, access, interoperate, and reuse data with minimal intervention) for an array of interdisciplinary tasks such as fact-based decision-making and forecasting [41]. 
現在、Web上でのデジタルコレクションオブジェクトの相互接続ネットワークの作成において、異なるデジタルリソースをリンクさせることに大きな重点が置かれており、機械のアクショナビリティ（すなわち、計算システムが最小限の介入でデータを見つけ、アクセスし、相互運用し、再利用する能力）をサポートするために、関連する生態学的、環境的およびその他の関連データとリンクされています。これは、事実に基づく意思決定や予測などのさまざまな学際的タスクに役立ちます[41]。
Using data standards for describing and reasoning over collection data can aid researchers counter unwanted biases via transparency. 
コレクションデータを記述し、推論するためのデータ標準を使用することで、研究者は透明性を通じて望ましくないバイアスに対抗することができます。
However, making data comply with data standards can also lead to oversimplification or reinterpretation [71]. 
**しかし、データをデータ標準に準拠させることは、過度の単純化や再解釈を招く可能性もあります[71]。**

<!-- ここまで読んだ! -->

Machine learning and knowledge engineering strategies can help to (semi-)automatically extract and structure biodiversity knowledge according [102, 91], for instance using state-of-the-art computer vision or natural language processing techniques as well as crowd-sourcing platforms for the annotation of field diaries and other collection objects with formal language [92, 29]. 
**機械学習と知識工学の戦略は、生物多様性の知識を（半）自動的に抽出し、構造化するのに役立ちます[102, 91]**。たとえば、最先端のコンピュータビジョンや自然言語処理技術、さらにはフィールドダイアリーや他の収集物の注釈に正式な言語を使用するためのクラウドソーシングプラットフォームを使用することが含まれます[92, 29]。
Nevertheless, a bottleneck in the digitization of collections and their use for machine actionability is the amount of work and domain expertise required for the formalisation of such knowledge, and the extraction from unstructured texts, images and video’s. 
それにもかかわらず、コレクションのデジタル化と機械のアクショナビリティのための利用におけるボトルネックは、そのような知識の形式化に必要な作業量とドメイン専門知識、そして非構造化されたテキスト、画像、ビデオからの抽出にあります。
Historical resources, i.e. handwritten texts, pose an additional challenge, as they are exceptionally challenging to interpret within the current scientific paradigm [107]. 
歴史的リソース、すなわち手書きのテキストは、現在の科学的パラダイム内で解釈するのが非常に困難であるため、追加の課題をもたらします[107]。

The variety and usefulness of different forms of knowledge both natural and formal and the challenges they pose is not limited to the biodiversity domain as described above. 
**自然的および形式的なさまざまな知識の形態の多様性と有用性、そしてそれらがもたらす課題**は、上記の生物多様性の領域に限られません。
We see the same diversity happening in law [82], medicine [16, 21] and even self-driving vehicles [9]. 
法[82]、医学[16, 21]、さらには自動運転車[9]においても同様の多様性が見られます。
To summarize: 
要約すると、

- domain knowledge is often best represented in a variety of modalities, i.e., images, taxonomies, or free text, each modality with its own data structure and characteristics which should be preserved, and no easy way of integrating, interfacing with or reasoning over multimodal knowledge in a federated way exists;
ドメイン知識はしばしばさまざまなモダリティ、すなわち画像、分類法、または自由なテキストで最もよく表現されます。各モダリティには保存すべき独自のデータ構造と特性があり、連邦的に多モダリティの知識を統合、インターフェース、または推論する簡単な方法は存在しません。

- provenance of data is paramount in understanding knowledge within the context in which it was produced; 
データの出所は、知識が生産された文脈内で理解する上で非常に重要です。

- fuzzy, incomplete, or complex knowledge is not easily systematized; 
曖昧で不完全、または複雑な知識は簡単には体系化できません。

- using data standards for describing and reasoning over collection data can aid researchers counter unwanted biases via transparency; 
コレクションデータを記述し、推論するためのデータ標準を使用することで、研究者は透明性を通じて望ましくないバイアスに対抗することができます。

- making data comply with data standards can lead to oversimplification or reinterpretation; 
データをデータ標準に準拠させることは、過度の単純化や再解釈を招く可能性があります。

- the production of structured domain knowledge, for instance from images or free text, requires domain expertise, and is therefore labour intensive and costly; 
画像や自由なテキストからの構造化されたドメイン知識の生成は、ドメイン専門知識を必要とし、したがって労働集約的でコストがかかります。

- knowledge evolves, and knowledge-based systems are required to deal with updates in their knowledge bases. 
**知識は進化し、知識ベースのシステムはその知識ベースの更新に対処する必要があります。**

<!-- ここまで読んだ! -->

### 2.2 KE as the transformation of knowledge expressed in natural language into knowledge expressed in a formal language KE（知識工学）とは、自然言語で表現された知識を形式言語で表現された知識に変換することです。

(↑のKEの定義は、単純明快で分かりやすいな...!!:thinking:)

This sort of rich and complex array of modalities for the representation of knowledge has traditionally posed a challenge to knowledge engineers [33]. 
このような豊かで複雑な知識の表現のためのモダリティの配列は、伝統的に知識工学者にとっての課題となってきました[33]。
Much of the literature on knowledge engineering methodology has focused on the ways in which knowledge in these naturally-occurring forms can be recast into a structured symbolic representation, e.g., using methods of knowledge elicitation from subject matter experts [88], for instance by the formulation of competency questions for analysing application ontologies [12]. 
知識工学の方法論に関する文献の多くは、これらの自然に発生する形態の知識を構造化された象徴的表現に再構成する方法に焦点を当てています。たとえば、専門家からの知識引き出しの方法[88]を使用し、アプリケーションオントロジーを分析するための能力質問の定式化によってです[12]。
One way to think about this is as the process of expressing knowledge presented in a natural, humanly evolved language in a formally-defined language. 
これを考える一つの方法は、自然で人間が進化させた言語で提示された知識を形式的に定義された言語で表現するプロセスとして捉えることです。
This notion of the transformation of natural language into a formal language as a means of enabling effective reasoning has a deep history rooted in methodologies developed by analytical philosophers of the early twentieth century [24, 69], but dating even further back to Liebniz’s lingua rationalis [35] and the thought of Ramón Lull [37]. 
自然言語を形式言語に変換するというこの概念は、効果的な推論を可能にする手段として、20世紀初頭の分析哲学者によって開発された方法論に深く根ざした歴史を持っています[24, 69]。しかし、リーブニッツの「理性的言語」[35]やラモン・ルルの思想[37]にまで遡ります。
Catarina Dutilh Novaes [69] has argued that formal languages enable reasoning that is less skewed by bias and held beliefs, an effect achieved through de-semantification, i.e., the process of replacing terms in a natural language with symbols that can be manipulated without interpretation using a system of rules of transformation. 
カタリナ・デュティル・ノヴァエス[69]は、形式言語がバイアスや信念によって歪められにくい推論を可能にすると主張しています。この効果は、自然言語の用語を解釈なしに操作できる記号に置き換えるプロセスである「デセマンティフィケーション」を通じて達成されます。
Coupled with sensorimotor manipulation of symbols in a notational system, people can reason in a manner that outstrips their abilities unaided by such a technology. 
記号の記法システムにおけるセンサーモーター操作と組み合わせることで、人々はそのような技術なしでは達成できない方法で推論することができます。

While Dutilh Novaes’ analysis focuses on this idea of formal languages as a cognitive tool used by humans directly, e.g. through the manipulation of a system of notation using paper and pencil, she notes that this manipulation of symbols is the route to the mechanization of reasoning through computation. 
デュティル・ノヴァエスの分析は、紙と鉛筆を使用した記法システムの操作を通じて人間が直接使用する認知ツールとしての形式言語のアイデアに焦点を当てていますが、彼女はこの記号の操作が計算を通じた推論の機械化への道であることを指摘しています。
When externally manifested as a function executed by a machine through either interpretation by an inference engine, or through compilation into a machine-level language, this approach of formalization yields the benefits of reliability, greater speed and efficiency in reasoning. 
**推論エンジンによる解釈や機械レベルの言語へのコンパイルを通じて、外部的に機械によって実行される機能として現れると、この形式化のアプローチは信頼性、より高い速度、そして推論の効率性の利点をもたらします。**
(うんうん。LLMの精度を高めるためのRAGだとしても、自然言語よりも構造化されていた方が、このような利点があるよね、という話...!!:thinking:)

This idea captures precisely the essence of the practice of knowledge engineering: Starting from sources of knowledge expressed in natural language and other modalities of human expression, through the process of formalization [51, 95], knowledge engineers create computational artifacts embodying this knowledge. 
このアイデアは、**知識工学の実践の本質を正確に捉えています：自然言語や他の人間の表現のモダリティで表現された知識の源から始まり、形式化のプロセスを通じて[51, 95]、知識工学者はこの知識を具現化した計算アーティファクトを作成**します。
These computational artifacts then enable us to reason using this knowledge in a predictable, efficient, and repeatable fashion. 
これらの計算アーティファクトは、その後、この知識を予測可能で効率的かつ再現可能な方法で推論することを可能にします。
This is done either by proxy through the action of autonomous agents, or in the context of human-mediated decision-making processes. 
これは、自律エージェントの行動を通じて代理で行われるか、人間が仲介する意思決定プロセスの文脈で行われます。

<!-- ここまで読んだ! -->

### 2.3 LLMs as a general-purpose technology for transforming natural language into formal language
### 2.3 LLM（大規模言語モデル）を自然言語を形式言語に変換するための汎用技術として

Until recently, there have been two ways in which this sort of formalization could be performed: through the manual authoring of symbolic/logical representations, e.g., as in the traditional notion of expert systems [34], or through the use of machine learning and natural language processing to extract such representations automatically from natural language text [61]. 
最近まで、この種の**形式化を行う方法は二つ**ありました：(1)象徴的/論理的表現の手動作成、たとえば伝統的な専門家システムの概念[34]のように、(2)または機械学習と自然言語処理を使用して、そのような表現を自然言語テキストから自動的に抽出する方法[61]です。
But what has become evident with the emergence of LLMs, with their capabilities for language learning and processing, is that they provide a new and powerful type of general purpose tool for mapping between natural language[2] and formal language, as well as other modalities. 
しかし、**言語学習と処理の能力を持つLLMの出現により明らかになったのは、自然言語[2]と形式言語、さらには他のモダリティ間のマッピングのための新しく強力な汎用ツールを提供するということ**です。
LLMs have shown state-of-the-art performance on challenging NLP tasks such as relation extraction [5] or text abstraction/summarization [114], and have been used to translate between other modalities, such as images and text (called vision-language models [119, 77]) in computer vision tasks, or from natural language to code [113, 47], in which a pretrained task-agnostic language model can be zero-shot and few-shot transferred to perform a certain task [20, 52]. 
**LLMは、関係抽出[5]やテキストの抽象化/要約[114]などの難しいNLPタスクで最先端のパフォーマンスを示しており**、コンピュータビジョンタスクにおいて画像とテキスト（ビジョン-ランゲージモデル[119, 77]と呼ばれる）間の翻訳や、自然言語からコード[113, 47]への翻訳に使用されています。この場合、事前学習されたタスクに依存しない言語モデルは、特定のタスクを実行するためにゼロショットおよび少数ショットで転送されることができます[20, 52]。
If one accepts the position that KE can be generally described as the process of transforming knowledge in natural language into knowledge in formal language, then it becomes clear that LLMs provide an advance in our ability to perform knowledge engineering tasks.
もし、**KEは一般に自然言語の知識を形式言語の知識に変換するプロセス**として説明できるという立場を受け入れるならば、**LLMsが知識工学タスクを実行する能力の向上を提供することは明らか**になります。

<!-- ここまで読んだ! -->

### 3 The use of LLMs in the practice of knowledge engineering: two scenarios 知識工学の実践におけるLLMsの使用：二つのシナリオ

Given the above discussion, the natural question that arises is: what might be the utility and impact of the use of LLMs for the transformation of natural language into formal language, when applied in the context of the practice of knowledge engineering?
上記の議論を踏まえると、**自然言語を形式言語に変換するためのLLMsの使用が、知識工学の実践の文脈でどのような有用性と影響を持つのか**という自然な疑問が生じます。

When LLMs emerged as a new technology in the mid-2010s, two views of the relationship between LLMs and knowledge bases (KBs) were put forward.
2010年代中頃にLLMsが新しい技術として登場したとき、LLMsと知識ベース（KBs）との関係について二つの見解が提唱されました。
One was the LLM can be a useful component for various processes that are part of a larger knowledge engineering workflow (i.e. "LMs for KBs" [3]); the other was that that the LLM is a cognitive artifact that can be treated as a knowledge base in and of itself (i.e., "LMs as KBs" [75]).
**一つは、LLMがより大きな知識工学ワークフローの一部であるさまざまなプロセスに役立つコンポーネントであるというもの**であり（すなわち、「KBのためのLMs」[3]）、**もう一つは、LLMがそれ自体が知識ベースとして扱える認知的アーティファクトである**というものでした（すなわち、「KBとしてのLMs」[75]）。
(うんうん、前者はイメージある...! 分類モデルというコンポーネントのハードル下がったみたいな...!:thinking:)
We exploit this dichotomy to formulate a pair of possible future scenarios for the use of LLMs in the practice of KE.
私たちはこの二分法を利用して、**知識工学の実践におけるLLMsの使用に関する二つの将来のシナリオ**を定式化します。
One is to use LLMs as a technology for or tool in support of implementing knowledge tasks that have traditionally been build using older technologies such as rule bases and natural language processing (NLP).
一つは、LLMを、従来はルールベースや自然言語処理（NLP）などの古い技術を使用して構築されてきた知識タスクの実装を支援するための技術またはツールとして使用することです。
Another is to use LLMs to remove the need for knowledge engineers to be fluent in a formal language, i.e., by allowing knowledge for a given knowledge task to be expressed in natural language, and then using prompt engineering as the primary paradigm for the implementation of reasoning and learning.
もう一つは、**LLMを使用して知識エンジニアが形式言語に堪能である必要をなくすこと**です。つまり、特定の知識タスクの知識を自然言語で表現できるようにし、その後、推論と学習の実装のための主要なパラダイムとしてプロンプトエンジニアリングを使用することです。
We now explore each of these scenarios in turn, and consider the open research problems that they raise.
これから、これらのシナリオを順に探求し、それらが提起するオープンな研究課題について考察します。

<!-- ここまで読んだ! -->

### 3.1 LLMs as components or tools used in knowledge engineering 知識工学で使用されるコンポーネントまたはツールとしてのLLMs

(こっちの活用はイメージしやすい!:thinking:)

We illustrate the first scenario through reference to CommonKADS [86], a structured methodology that has been used by knowledge engineers since the early 2000’s.
最初のシナリオを、2000年代初頭から知識エンジニアによって使用されている構造化された方法論であるCommonKADS [86]を参照することで説明します。
CommonKADS is the refinement of an approach to providing a disciplined approach to the development of knowledge systems.
CommonKADSは、知識システムの開発に対する規律あるアプローチを提供するためのアプローチの洗練です。
This approach saw initial development in the nineteen-eighties as a reaction to both the ad-hoc nature of early expert systems development [111] and to the frequency of failures in the deployment of expert systems in an organizational context [34].
このアプローチは、1980年代に初期のエキスパートシステム開発のアドホックな性質[111]と、組織的文脈におけるエキスパートシステムの展開における失敗の頻度[34]に対する反応として初期の開発が行われました。
Stemming from early work on making expert systems development understandable and repeatable [42], CommonKADS is distinguished from methodologies more focused on ontology development (e.g., NeON [94], Kendall and McGuinness’s "Ontology 101" framework [51], and Presutti’s ontology design patterns [76]) in that it provides practical guidance for specification and implementation of knowledge systems components in a broader sense.
エキスパートシステム開発を理解可能かつ再現可能にするための初期の研究[42]に由来し、CommonKADSは、よりオントロジー開発に焦点を当てた方法論（例：NeON [94]、KendallとMcGuinnessの「Ontology 101」フレームワーク[51]、およびPresuttiのオントロジーデザインパターン[76]）とは異なり、より広い意味での知識システムコンポーネントの仕様と実装に関する実用的なガイダンスを提供します。
It attempts to provide a synoptic guide to the full scope of activities involved in the practice of KE, and show how it relates to the activities of the organization in which that engineering is taking place.
それは、**KEの実践に関与する活動の全範囲に対する概観的なガイド**を提供し、その工学が行われている組織の活動との関連を示そうとします。
As such, in the context of this paper we can use it as a framework to explore for what tasks and in what ways LLMs can be used for KE.
したがって、本論文の文脈において、私たちはそれをLLMsがKEにどのようなタスクと方法で使用できるかを探求するためのフレームワークとして使用できます。

Some tasks identified by CommonKADS as part of the KE process may remain largely unchanged by the use of LLMs.
CommonKADSによってKEプロセスの一部として特定されたタスクの中には、LLMsの使用によってほとんど変更されないものもあります。
These include knowledge task identification and project organizational design.
これには、知識タスクの特定やプロジェクトの組織設計が含まれます。
But others can involve the use of LLMs.
しかし、他のタスクはLLMsの使用を含むことができます。
LLMs can assist knowledge engineers and/or knowledge providers in the performance of knowledge engineering tasks.
LLMsは、知識エンジニアや知識提供者が知識工学タスクを実行するのを支援することができます。
They can also be a means for the implementation of modules performing knowledge-intensive tasks.
また、知識集約型タスクを実行するモジュールの実装手段にもなり得ます。
Examples of these uses include the following:
これらの使用例には以下が含まれます：

- **Knowledge acquisition and elicitation** LLMs can be used to support knowledge acquisition and elicitation in a given domain of interest.
**知識獲得と引き出し** LLMは、特定の関心領域における知識獲得と引き出しを支援するために使用できます。
Engineers can create prompts that target specific aspects of the domain, using the responses as a starting point for building the knowledge base.
エンジニアは、ドメインの特定の側面をターゲットにしたプロンプトを作成し、その応答を知識ベースを構築するための出発点として使用できます。
Dialogs between LLMs trained using such prompts and knowledge providers, the subject matter experts, can support the review, validation, and refinement of the acquired knowledge [8].
そのようなプロンプトを使用して訓練されたLLMsと知識提供者（専門家）との対話は、獲得した知識のレビュー、検証、および洗練を支援することができます[8]。

- **Knowledge organization** LLMs can be used to organize the acquired knowledge into a coherent structure using natural language, making it easy to understand and update.
**知識の整理** LLMは、獲得した知識を自然言語を使用して一貫した構造に整理するために使用でき、理解しやすく、更新しやすくします。(これが一番最初に思いつく使用例だな...!!:thinking:)
Prompt engineering can be used to develop a set of prompts that extract formal language using the LLM, e.g., for text to graph generation [40] or vice versa [18, 2].
プロンプトエンジニアリングを使用して、**LLMを使用して形式言語を抽出するためのプロンプトのセット**を開発することができます。例えば、テキストからグラフ生成[40]やその逆[18, 2]のためです。
Moreover, LLMs are used for program synthesis [113, 47], the generation of metadata [56] or for fusing knowledge graphs [118].
さらに、LLMsはプログラム合成[113, 47]、メタデータの生成[56]、または知識グラフの融合[118]に使用されます。

- **Data augmentation** LLMs can be used to generate synthetic training data to aid in testing the knowledge system by evaluating its performance on instances of the specific task [116].
**データ拡張** LLMは、特定のタスクのインスタンスに対するパフォーマンスを評価することによって、知識システムのテストを支援するために**合成トレーニングデータを生成するために使用**できます[116]。

- **Testing and refinement** Feedback from subject matter experts and users can be used to prompt an LLM to refine the natural language knowledge base and improve the system’s accuracy and efficiency through self-correction of prompts and tuning of the LLM model settings as needed to optimize the system’s performance [110].
**テストと洗練** 専門家やユーザーからのフィードバックは、LLMに自然言語知識ベースを洗練させ、プロンプトの自己修正やLLMモデル設定の調整を通じてシステムの精度と効率を向上させるために使用できます[110]。

- **Maintenance** LLMs can be used to monitor new information and trends, and to then propose new prompts integrating those updates into the knowledge base.
**メンテナンス** LLMは、**新しい情報やトレンドを監視し、それらの更新を知識ベースに統合**する新しいプロンプトを提案するために使用できます。

<!-- ここまで読んだ! -->

![Figure 2 Hierarchy of knowledge-intensive task types from CommonKADS ([86], p.125)]()

Consider the CommonKADS knowledge task hierarchy shown in Figure 2.
図2に示されているCommonKADSの知識タスク階層を考えてみましょう。
Synthetic knowledge-intensive tasks, e.g. design or configuration, are amenable to generative approaches [109]; analytic knowledge-intensive tasks can involve LLM components within a hybrid neuro-symbolic knowledge system.
合成知識集約型タスク（例：設計や構成）は生成的アプローチに適しており[109]、分析的知識集約型タスクはハイブリッド神経シンボリック知識システム内でLLMコンポーネントを含むことができます。

<!-- ここまで読んだ! -->

A shortcoming of using CommonKADS for our purposes, however, is that it predates the widespread use of machine learning and statistical natural language processing in KE.
ただし、私たちの目的でCommonKADSを使用することの短所は、KEにおける機械学習と統計的自然言語処理の広範な使用の前に存在していることです。(なるほどCommonKADSっていうのは、before 最新のML&NLPに提案された考え方ってことね...!!:thinking:)
A number of architectural approaches have since been developed that extend the CommonKADS concepts of a knowledge-intensive task type hierarchy and knowledge module templates.
その後、知識集約型タスクタイプ階層と知識モジュールテンプレートのCommonKADSの概念を拡張するいくつかのアーキテクチャアプローチが開発されました。
These include modeling the fine-grained data flows and workflows associated with knowledge systems that combine components that ingest, clean, transform, aggregate and generate data, as well as generate and apply models built using machine learning [103, 19, 27, 31, 101].
これには、データを取り込み、クリーンアップし、変換し、集約し、生成するコンポーネントを組み合わせた知識システムに関連する詳細なデータフローとワークフローのモデリングが含まれ、機械学習を使用して構築されたモデルを生成および適用します[103, 19, 27, 31, 101]。
These architectures are put forward as providing a general framework for composing heterogeneous tools for knowledge representation and inference into a single integrated hybrid neuro-symbolic system.
これらのアーキテクチャは、知識表現と推論のための異種ツールを単一の統合ハイブリッド神経シンボリックシステムに構成するための一般的なフレームワークを提供すると提案されています。
The design pattern notations put forward in recent work [103, 101, 31] treat data, models, and symbolic representations as the inputs and outputs of components composed into a variety of knowledge system design patterns.
最近の研究[103, 101, 31]で提案されたデザインパターンの表記は、データ、モデル、およびシンボリック表現を、さまざまな知識システムデザインパターンに構成されたコンポーネントの入力と出力として扱います。
Generalizing these into natural language and formal language inputs and outputs can provide a simple way to extend these design notations to accommodate both LLMs as well as a richer set of knowledge representations.
これらを自然言語と形式言語の入力および出力に一般化することで、LLMsとより豊かな知識表現の両方に対応するために、これらのデザイン表記を拡張する簡単な方法を提供できます。

<!-- ここまで読んだ! -->

### 3.2 Knowledge engineering as prompt engineering プロンプトエンジニアリングとしての知識工学

Given that LLMs enable knowledge modeling in natural language, it is conceivable that the programming of knowledge modules could take place entirely in natural language.
LLMsが自然言語での知識モデリングを可能にすることを考えると、知識モジュールのプログラミングが完全に自然言語で行われる可能性があります。
Consider that prompt programming is "finding the most appropriate prompt to allow an LLM to solve a task" [57].
**プロンプトプログラミングは「LLMがタスクを解決するために最も適切なプロンプトを見つけること」**であると考えてみてください[57]。
One can through this lens view knowledge engineering as the crafting of dialogues in which a subject matter expert (SME) arrives at a conclusion by considering the preceding context and argumentation [80, 109, 89, 60].
この視点を通じて、知識工学を、専門家（SME）が前の文脈と議論を考慮して結論に達する対話の作成と見なすことができます[80, 109, 89, 60]。
This framing of knowledge engineering as prompt engineering is the second scenario we wish to explore.
知識工学をプロンプトエンジニアリングとして捉えるこの枠組みは、私たちが探求したい第二のシナリオです。
(ん?? シナリオ1とどう違うんだろ?? :thinking:)

<!-- ここまで読んだ! -->

From the perspective of the CommonKADS knowledge-intensive task type hierarchy, this would involve a redefinition of the types and hierarchy to use LLMs and prompt programming design patterns, e.g. as described in [57].
CommonKADSの知識集約型タスクタイプ階層の観点から見ると、これはLLMsとプロンプトプログラミングデザインパターンを使用するためのタイプと階層の再定義を含むことになります。例えば、[57]で説明されているように。
Several aspects of this redefinition could include:
この再定義のいくつかの側面には以下が含まれる可能性があります：

- **Natural language inference** LLMs can be used to build natural language inference engines that use the organized knowledge to perform the specific task by taking input queries and generate output using prompt engineering to guide the LLM towards generating accurate inferences, e.g. using zero- or few-shot chain-of-thought design patterns.
**自然言語推論** LLMは、整理された知識を使用して特定のタスクを実行する自然言語推論エンジンを構築するために使用でき、入力クエリを受け取り、プロンプトエンジニアリングを使用してLLMを正確な推論を生成するように導く出力を生成します。例えば、ゼロショットまたは少数ショットのチェーン・オブ・ソートデザインパターンを使用します。
The benefit here is that the gap between the knowledge engineer, knowledge provider (the subject matter expert) and the user is smaller since a translation to a formal language (the language of the engineer) is no longer required.
ここでの利点は、知識エンジニア、知識提供者（専門家）、およびユーザー間のギャップが小さくなることです。なぜなら、形式言語（エンジニアの言語）への翻訳がもはや必要ないからです。

- **Knowledge-intensive task execution through human/machine dialog** LLMs can be used to a conversational interface that allows users to interact with the knowledge system and receive task-specific support.
**人間/機械対話を通じた知識集約型タスクの実行** LLMは、ユーザーが知識システムと対話し、タスク特有のサポートを受けることを可能にする会話インターフェースに使用できます。

- **Testing and refinement through human/machine dialog** Feedback from subject matter experts and users can be used to prompt an LLM to refine the natural language knowledge base and improve the system’s accuracy and efficiency through self-correction of prompts and tuning of the LLM model settings as needed to optimize the system’s performance.
**人間/機械対話を通じたテストと洗練** 専門家やユーザーからのフィードバックは、LLMに自然言語知識ベースを洗練させ、プロンプトの自己修正やLLMモデル設定の調整を通じてシステムの精度と効率を向上させるために使用できます。

<!-- ここまで読んだ! -->

One possible benefit of this approach would be that the barrier to adoption of knowledge engineering as a practice could be lowered significantly.
**このアプローチの一つの可能な利点は、知識工学を実践として採用する際の障壁が大幅に低下する可能性があること**です。
Knowledge elicitation could be conducted entirely within natural language, meaning that subject matter experts without training in formal knowledge representations could perform these tasks directly.
**知識の引き出しは完全に自然言語内で行うことができるため、形式的な知識表現の訓練を受けていない専門家がこれらのタスクを直接実行できること**を意味します。(おお、まだちゃんと分かってないけど嬉しそう...!!:thinking:)
However, this approach assumes that predictable inference [101] using natural language is satisfactory.
**しかし、このアプローチは、自然言語を使用した予測可能な推論[101]が満足できるものであると仮定**しています。
The propensity of current LLMs to "hallucinate", i.e., to confabulate facts, is an obstacle to the realization of this idea [48].
**現在のLLMsが「幻覚」を起こす傾向、すなわち事実を作り上げることは、このアイデアの実現に対する障害**です[48]。
Multiple efforts have been devoted to the creation of prompt programming patterns that address this issue, ranging from chain-of-thought approaches to retrieval-assisted generation, i.e. the augmentation of LLMs with authoritative document indexes and stores.
この問題に対処するために、思考の連鎖アプローチから、権威ある文書インデックスやストアを用いたLLMの拡張である**retrieval-assisted generation**に至るまで、プロンプトプログラミングパターンの作成に多くの努力が注がれています。(RAGってこの訳し方もするんだ...!! AがAugmentadの印象が強かった...!:thinking:)
Recent work has described ways in which knowledge graphs as a formal language can be integrated with natural language and LLM-based language processing and reasoning to provide knowledge systems architectures that directly address this issue.
最近の研究では、**形式言語としての知識グラフを自然言語およびLLMベースの言語処理と推論に統合する方法**が説明されており、これによりこの問題に直接対処する知識システムアーキテクチャが提供されます。(あ、これはGraph-RAG的なやつの話かな...!!:thinking:)
surveys work in this direction.
この方向性に関する研究を調査しています。

<!-- ここまで読んだ! -->

### 4 Open research questions オープンリサーチクエスチョン

Using the scenarios outlined above, we can identify a number of open research questions to be addressed to realize either or both of these two possible approaches to the use of LLMs in knowledge engineering.
上記のシナリオを使用して、知識工学におけるLLMの使用に関するこれら2つの可能なアプローチのいずれかまたは両方を実現するために対処すべきオープンリサーチクエスチョンを特定できます。
These questions touch on three general areas: the impact of LLMs on the methodologies used to build knowledge systems, on the architectural design of knowledge systems incorporating and/or based on LLMs, and on the evaluation of such systems.
これらの質問は、知識システムを構築するために使用される方法論に対するLLMの影響、LLMを組み込んだまたは基にした知識システムのアーキテクチャ設計、そしてそのようなシステムの評価という3つの一般的な領域に関わります。
For each of these open questions, we provide a link back to the biodiversity scenario discussed in Section 2.1 denoted by a �.
これらのオープンリサーチクエスチョンのそれぞれについて、セクション2.1で議論された生物多様性シナリオへのリンクを提供します。

<!-- ここまで読んだ! -->

### 4.1 Methodology 方法論

#### 4.1.1 How can knowledge engineering methodologies best be adapted to use LLMs? 知識工学の方法論は、LLMを使用するためにどのように最適に適応できるか？

How can we harmoniously meld the considerable body of work on knowledge engineering methodologies with the new capabilities presented by LLMs?
私たちは、知識工学の方法論に関する膨大な研究とLLMが提供する新しい能力をどのように調和させることができるでしょうか？

Schreiber’s conceptualization of knowledge engineering as the construction of different aspect models of human knowledge, as discussed above, offers a framework for further elaboration.
上記で議論したように、Schreiberの知識工学の概念化は、人間の知識の異なる側面モデルの構築として、さらなる詳細化のための枠組みを提供します。
The distinctive characteristics of LLMs, coupled with prompt engineering, present unique challenges and opportunities for building agents within a knowledge system, one that is consistent with the CommonKADS approach.
LLMの特異な特性とプロンプトエンジニアリングは、CommonKADSアプローチと一致する知識システム内でエージェントを構築するための独自の課題と機会を提供します。

While the role definitions within KE methodologies might mostly remain the same, the skills required for knowledge engineers will need morphing to adapt to the LLM environment.
KE方法論内の役割定義はほとんど同じままであるかもしれませんが、**知識エンジニアに必要なスキルはLLM環境に適応するために変化する必要があります。**
This evolution of roles calls for an extensive investigation into what these new skills might look like, and how they can be cultivated.
この役割の進化は、これらの新しいスキルがどのようなものであるか、そしてそれをどのように育成できるかについての広範な調査を必要とします。
Additionally, the adaptability of the various knowledge-intensive task type hierarchies described by CommonKADS and its descendants in the literature on hybrid neuro-symbolic systems to accommodate LLMs is another fertile area for exploration.
さらに、CommonKADSおよびその子孫によって記述されたさまざまな知識集約型タスクタイプ階層のLLMへの適応性は、探求のためのもう一つの肥沃な領域です。

LLM-based applications, likened to synthetic tasks within these knowledge engineering frameworks, raise compelling research questions regarding accuracy and the prevention of hallucinations.
LLMベースのアプリケーションは、これらの知識工学フレームワーク内の合成タスクに似ており、精度と幻覚の防止に関する興味深い研究課題を提起します。
LLM-based applications have a lower bar to reach with respect to notions of accuracy and avoidance of hallucinations, but still must provide useful and reliable guidance to users and practitioners.
LLMベースのアプリケーションは、精度や幻覚の回避に関する概念に対して達成すべきハードルが低いですが、**それでもユーザーや実務者に有用で信頼できるガイダンスを提供する必要**があります。

<!-- ここまで読んだ! -->

Connecting back to the biodiversity domain, answering these questions would provide guidance on the appropriate methodology to adopt when developing a new specimen curation and collection knowledge management system that needs to deal with multimodal assets like handwritten text or images.
生物多様性の領域に戻ると、これらの質問に答えることは、手書きのテキストや画像のようなマルチモーダル資産を扱う必要がある新しい標本キュレーションおよびコレクション知識管理システムを開発する際に採用すべき適切な方法論に関するガイダンスを提供します。

<!-- ここまで読んだ! -->

#### 4.1.2 How do principles of content and data management apply to prompt engineering? コンテンツおよびデータ管理の原則は、プロンプトエンジニアリングにどのように適用されるか？

Applying content and/or data management principles to collections of prompts and prompt templates, integral to work with LLMs, is an area ripe for exploration.
LLMとの作業に不可欠なプロンプトとプロンプトテンプレートのコレクションにコンテンツおよび/またはデータ管理の原則を適用することは、探求に適した領域です。
Properly managing these resources could improve efficiency and guide the development of improved methodologies in knowledge engineering.
これらのリソースを適切に管理することで、効率が向上し、知識工学における改善された方法論の開発を導くことができます。
This calls for a rigorous investigation of current data management practices, their applicability to LLMs, and potential areas of refinement.
これは、現在のデータ管理慣行、そのLLMへの適用可能性、および改善の可能性のある領域についての厳密な調査を必要とします。
Ensuring the reproducibility of LLM engineering from a FAIR data standpoint is a crucial yet complex challenge.
FAIRデータの観点からLLMエンジニアリングの再現性を確保することは、重要でありながら複雑な課題です。
Developing and validating practices and protocols that facilitate easy tracing and reproduction of LLM-based processes and outputs is central to this endeavour.
LLMベースのプロセスと出力の容易な追跡と再現を促進する実践とプロトコルを開発し、検証することは、この取り組みの中心です。
Addressing this challenge will aid researchers in applying LLM engineering in a FAIR way.
この課題に対処することは、研究者がFAIRな方法でLLMエンジニアリングを適用するのを助けるでしょう。
Doing so is critical for biodiversity research and science in general where precision, reproducibility and provenance are key for knowledge discovery and research integrity.
これは、生物多様性研究や一般的な科学にとって重要であり、精度、再現性、出所が知識発見と研究の整合性の鍵となります。

<!-- ここまで読んだ! -->

#### 4.1.3 What are the cognitive norms that govern the conduct of KE? KEの実施を支配する認知規範とは何か？

A crucial area of inquiry involves the identification and understanding of cognitive norms, as described by Menary, that govern the practice of knowledge engineering.
重要な調査領域は、Menaryによって説明された知識工学の実践を支配する認知規範の特定と理解です。
Cognitive norms are established within a human community of practice as a way of governing the acceptable use of "external representational vehicles to complete a cognitive task".
認知規範は、認知タスクを完了するための「外部表現手段の受け入れ可能な使用」を管理する方法として、人間の実践コミュニティ内で確立されます。
As the consumer adoption of LLM technology has progressed, we see a great deal of controversy about when and how it is appropriate to use, e.g. in the context of education or the authoring of research publications.
LLM技術の消費者採用が進むにつれて、教育や研究出版物の著作の文脈において、いつどのように使用するのが適切かについて多くの論争が見られます。
Understanding how these norms shape the use of LLMs in this context is an under-explored field of study.
この文脈におけるLLMの使用を形作るこれらの規範を理解することは、あまり探求されていない研究分野です。
By unravelling the interplay between these cognitive norms and LLM usage, we can gain valuable insights into the dynamics of knowledge engineering practices and possibly foster more effective and responsible uses of LLMs.
これらの認知規範とLLMの使用との相互作用を解明することで、知識工学の実践のダイナミクスに関する貴重な洞察を得ることができ、より効果的で責任あるLLMの使用を促進する可能性があります。
In the biodiversity sciences, this means understanding the cognitive norms specific to the domain, to understand how LLMs can be used in a way that respects the domain’s practices and standards.
生物多様性科学においては、これはその領域に特有の認知規範を理解し、LLMがその領域の慣行や基準を尊重する方法で使用できるかを理解することを意味します。

<!-- ここまで読んだ! -->

#### 4.1.4 How do LLMs impact the labor economics of KE? LLMはKEの労働経済にどのように影響するか？

A related but distinct question pertains to the impact of LLMs on the economic costs associated with knowledge engineering.
関連するが異なる質問は、**知識工学に関連する経済的コストに対するLLMの影響**に関するものです。
The introduction and application of LLMs in this field may significantly alter the economic landscape, either by driving costs down through automation and efficiency or by introducing new costs tied to system development, maintenance, and oversight.
この分野におけるLLMの導入と適用は、コストを自動化と効率によって削減するか、システムの開発、保守、監視に関連する新しいコストを導入することによって、経済的な状況を大きく変える可能性があります。
Thoroughly exploring these economic implications can shed light on the broader effects of integrating LLMs into knowledge engineering.
これらの経済的影響を徹底的に探求することで、LLMを知識工学に統合することのより広範な影響を明らかにすることができます。

The realm of labor economics as it pertains to hybrid or centaur systems is another area ripe for investigation.
ハイブリッドまたはケンタウロスシステムに関連する労働経済の領域は、探求に適した別の領域です。
Understanding how the deployment of these systems influences labor distribution, skill requirements, and job roles could provide valuable input into the planning and implementation of such technologies.
これらのシステムの展開が労働分配、スキル要件、職務にどのように影響するかを理解することは、そのような技術の計画と実施に貴重な情報を提供する可能性があります。
Additionally, it could reveal the potential societal and economic impacts of this technological evolution.
さらに、これはこの技術的進化の潜在的な社会的および経済的影響を明らかにする可能性があります。

Developments for LLM-based KE can help mitigate labour of knowledge experts in the biodiversity sciences, for instance by the development of more efficient KE workflows for the digitization of museum specimens or manuscripts.
LLMベースのKEの発展は、生物多様性科学における知識専門家の労働を軽減するのに役立ち、例えば博物館の標本や原稿のデジタル化のためのより効率的なKEワークフローの開発によって実現されます。

<!-- ここまで読んだ! -->

### 4.2 Architecture アーキテクチャ

#### 4.2.1 How can hybrid neuro-symbolic architectural models incorporate LLMs? ハイブリッド神経シンボリックアーキテクチャモデルは、どのようにLLMを組み込むことができるか？

Design patterns for hybrid neuro-symbolic systems offer a structured approach to comprehend the flow of data within a knowledge system.
ハイブリッド神経シンボリックシステムのデザインパターンは、知識システム内のデータの流れを理解するための構造化されたアプローチを提供します。
Adapting this model to account for the differences between natural and formal language could significantly enhance our ability to trace and manage data within knowledge systems.
このモデルを自然言語と形式言語の違いを考慮して適応させることで、知識システム内のデータを追跡し管理する能力が大幅に向上する可能性があります。
A salient research question emerging from this scenario pertains to the actual process of integrating LLMs into knowledge engineering data processing flows.
このシナリオから浮かび上がる重要な研究課題は、LLMを知識工学のデータ処理フローに統合する実際のプロセスに関するものです。
Understanding the nuances of this process will involve a deep examination of the shifts in methodologies, practices, and the potential re-evaluations of existing knowledge engineering paradigms.
このプロセスのニュアンスを理解することは、方法論、実践の変化、および既存の知識工学パラダイムの再評価の可能性についての深い検討を伴います。
The perspective of KE enabled by LLMs as focused on the transformation of natural language into formal language provides insights that can be used to improve the motivation for hybrid neuro-symbolic systems.
自然言語を形式言語に変換することに焦点を当てたLLMによって可能にされたKEの視点は、ハイブリッド神経シンボリックシステムの動機を改善するために使用できる洞察を提供します。
Addressing these questions would shed light on tasks for which hybridization using LLMs would prove favourable, e.g., image classification of species.
これらの質問に対処することで、LLMを使用したハイブリッド化が有利であるタスク、例えば種の画像分類に関する洞察が得られます。

<!-- ここまで読んだ! -->

### 4.2.2 How can prompt engineering patterns support reasoning in natural language?　プロンプトエンジニアリングパターンは、自然言語での推論をどのようにサポートできるか？

One fundamental question that arises is how prompt engineering patterns can be utilized to facilitate reasoning in natural language.
生じる基本的な質問は、プロンプトエンジニアリングパターンをどのように利用して自然言語での推論を促進できるかということです。
Exploring this topic involves understanding the mechanics of these patterns and their implications on natural language processing capabilities of LLMs.
このトピックを探求することは、これらのパターンのメカニズムとLLMの自然言語処理能力への影響を理解することを含みます。
This line of research could open new possibilities for enhancing the functionality and efficiency of these models.
この研究の方向性は、これらのモデルの機能性と効率を向上させる新しい可能性を開くかもしれません。

A related inquiry concerns the structure, controllability, and repeatability of reasoning facilitated by LLMs.
関連する調査は、LLMによって促進される推論の構造、制御可能性、および再現性に関するものです。
Examining ways to create structured, manageable, and reproducible reasoning processes within these models could significantly advance our capacity to handle complex knowledge engineering tasks and improve the reliability of LLMs.
これらのモデル内で構造化され、管理可能で再現可能な推論プロセスを作成する方法を検討することは、複雑な知識工学タスクを処理する能力を大幅に向上させ、LLMの信頼性を改善する可能性があります。

The interaction of LLMs and approaches to reasoning based on probabilistic formalisms is also an underexplored area of research.
LLMと確率的形式主義に基づく推論アプローチの相互作用も、あまり探求されていない研究領域です。
A particularly evocative effort in this area is that described in which describes the use of LLMs to transform natural language into programs in a probabilistic programming language, which can then be executed to support reasoning in a particular problem domain.
この領域で特に印象的な取り組みは、LLMを使用して自然言語を確率的プログラミング言語のプログラムに変換し、それを実行して特定の問題領域での推論をサポートする方法を説明したものです。
We note that this work provides an excellent example of the knowledge engineering as the transformation of natural language into formal language perspective and of the impact of LLMs in advancing that perspective.
この研究は、自然言語を形式言語に変換するという知識工学の視点と、その視点を進展させる上でのLLMの影響の優れた例を提供することに注意します。
Investigating how to automatically generate and assess other nuanced forms of knowledge within LLMs could lead to a more refined understanding of these models and their capabilities.
LLM内で他の微妙な知識の形式を自動的に生成し評価する方法を調査することは、これらのモデルとその能力に対するより洗練された理解につながる可能性があります。

Given that biodiversity knowledge is often best represented in a variety of modalities each with their own data structures and characteristics, research may explore how LLMs can act as natural language interfaces to such multimodal knowledge bases.
生物多様性の知識は、しばしばそれぞれ独自のデータ構造と特性を持つさまざまなモダリティで最もよく表現されるため、研究はLLMがそのようなマルチモーダル知識ベースへの自然言語インターフェースとして機能する方法を探るかもしれません。

<!-- ここまで読んだ! -->

#### 4.2.3 How can we manage bias, trust and control in LLMs using knowledge graphs? 知識グラフを使用してLLMにおけるバイアス、信頼、制御をどのように管理できますか？

(Graph-RAG的なやつの話かな...!!:thinking:)
Trust, control, and bias in LLMs, especially when these models leverage knowledge graphs, are critical areas to explore.
LLMにおける信頼、制御、バイアス、特にこれらのモデルが知識グラフを活用する場合は、探求すべき重要な領域です。
Understanding how to detect, measure, and mitigate bias, as well as establish trust and exert control in these models, is an essential aspect of ensuring ethical and responsible use of LLMs.
バイアスを検出、測定、軽減する方法、ならびにこれらのモデルにおいて信頼を確立し制御を行使する方法を理解することは、LLMの倫理的かつ責任ある使用を確保するための重要な側面です。
Furthermore, investigating methods to update facts in LLMs serving as knowledge graphs is a crucial area of research.
さらに、知識グラフとして機能するLLM内の事実を更新する方法を調査することは、重要な研究分野です。
Developing strategies for efficient and reliable fact updating could enhance the accuracy and usefulness of these models.
効率的かつ信頼性の高い事実更新のための戦略を開発することは、これらのモデルの精度と有用性を向上させる可能性があります。
Another key question involves understanding how we can add provenance to statements produced by LLMs.
もう一つの重要な質問は、LLMによって生成されたステートメントにどのように出所を追加できるかを理解することです。
This line of research could prove vital in tracking the origin of information within these models, thus enhancing their reliability and usability.
この研究の方向性は、これらのモデル内の情報の出所を追跡する上で重要であり、その結果、信頼性と使いやすさを向上させる可能性があります。
It opens the door to more robust auditing and validation practices in the use of LLMs.
これは、LLMの使用におけるより堅牢な監査および検証の実践への扉を開きます。
Addressing this challenge can help biodiversity researchers detect and mitigate biases, as use of LLMs might further exacerbate knowledge gaps, e.g., groups of individuals omitted from historical narratives in archival collections.
この課題に対処することは、生物多様性研究者がバイアスを検出し軽減するのに役立ちます。LLMの使用は、アーカイブコレクションの歴史的な物語から省かれた個人のグループなど、知識のギャップをさらに悪化させる可能性があります。
Moreover, novel update mechanisms can aid researchers to reliably update facts or changing knowledge structures learned by LLMs, for instance when domain knowledge evolves.
さらに、新しい更新メカニズムは、研究者がLLMによって学習された事実や変化する知識構造を信頼性を持って更新するのを助けることができます。たとえば、ドメイン知識が進化する場合です。

<!-- ここまで読んだ! -->

#### 4.2.4 Is extrinsic explanation sufficient? 外的説明は十分ですか？

A significant area of interest pertains to how we can effectively address the explainability of answers generated using LLMs.
重要な関心のある領域は、**LLMを使用して生成された回答の説明可能性にどのように効果的に対処できるか**に関係しています。
This exploration requires a deep dive into the functioning of LLMs and the mechanisms that govern their responses to prompts.
この探求は、LLMの機能とプロンプトに対する応答を支配するメカニズムを深く掘り下げることを必要とします。
Developing a thorough understanding of these processes can aid in creating transparency and trust in LLMs, as well as fostering their effective use.
これらのプロセスを徹底的に理解することは、LLMにおける透明性と信頼を創出し、その効果的な使用を促進するのに役立ちます。
The need for explanation in LLMs also leads to the question of whether extrinsic explanation is sufficient for the purposes of justifying a knowledge system’s reasoning, as argued in general for the intelligibility of knowledge systems by Cappelen and Devers, or if intrinsic explainability is a necessary requirement.
LLMにおける説明の必要性は、外的説明が知識システムの推論を正当化する目的に対して十分であるか、CappelenとDeversによる知識システムの理解可能性に関する一般的な議論のように、内的説明可能性が必要な要件であるかという疑問につながります。
This question calls for a thoughtful exploration of the value and limitations of both extrinsic and intrinsic explanation methodologies, and their implications for the understanding and usage of LLMs.
この質問は、外的および内的説明手法の価値と限界、ならびにそれらがLLMの理解と使用に与える影響についての慎重な探求を求めています。
An exciting research avenue arises from the work of Tiddi concerning explainability with formal languages.
形式言語による説明可能性に関するTiddiの研究から、興味深い研究の道が生まれます。
The exploration of this topic could reveal significant insights into how we can leverage formal languages to enhance the explainability of LLMs.
このトピックの探求は、形式言語を活用してLLMの説明可能性を向上させる方法に関する重要な洞察を明らかにする可能性があります。
This could pave the way for new methods to increase transparency and intelligibility in these models.
これは、これらのモデルにおける透明性と理解可能性を高める新しい方法への道を開く可能性があります。
In the sciences in general, answering these questions would aid explainability of LLM-generated answers via curated facts, increasing transparency and trust.
一般的に科学において、これらの質問に答えることは、キュレーションされた事実を通じてLLM生成の回答の説明可能性を助け、透明性と信頼を高めることになります。

<!-- ここまで読んだ! -->

### 4.2.5 How can LLMs support the engineering of hybrid human/machine knowledge systems?　LLMはハイブリッド人間/機械知識システムのエンジニアリングをどのようにサポートできますか？

Another topic of interest involves exploring the potential of hybrid systems that combine human cognition with machine capabilities within a dialogical framework.
もう一つの関心のあるトピックは、対話的な枠組みの中で人間の認知と機械の能力を組み合わせたハイブリッドシステムの可能性を探ることです。
As an exciting example of the possibilities for new approaches to human/machine collaboration in this vein, we point to the recent results reported by on the creation of conversational agents that simulate goal-directed human conversation and collaboration on tasks.
この方向性における人間/機械のコラボレーションへの新しいアプローチの可能性の興味深い例として、目標指向の人間の会話とタスクにおけるコラボレーションをシミュレートする会話エージェントの作成に関する最近の結果を指摘します。
One can imagine coupling LLM-based agents with human interlocutors working collaboratively in this manner on specific knowledge-intensive tasks.
LLMベースのエージェントをこのように特定の知識集約的なタスクで協力して作業する人間の対話者と結びつけることを想像できます。
Understanding how to develop these types of systems, and what their implications might be for the practice of knowledge engineering presents a fertile research line.
これらのタイプのシステムをどのように開発するか、そしてそれが知識エンジニアリングの実践にどのような影響を与えるかを理解することは、豊かな研究のラインを提示します。
It requires the careful analysis of human-machine interaction, the study of system design principles, and the investigation of their potential impact.
これは、人間と機械の相互作用の慎重な分析、システム設計原則の研究、およびそれらの潜在的な影響の調査を必要とします。
Research in this avenue can help mitigate the workload of the knowledge expert, for instance in the elicitation of domain knowledge, or crowdsourcing of annotations from unstructured sources such as herbaria or manuscripts.
この分野の研究は、ドメイン知識の引き出しや、標本館や原稿などの非構造的なソースからのアノテーションのクラウドソーシングにおいて、知識専門家の作業負荷を軽減するのに役立ちます。

<!-- ここまで読んだ! -->

### 4.3 Evaluation 評価

#### 4.3.1 How do we evaluate knowledge systems with LLM components? LLMコンポーネントを持つ知識システムをどのように評価しますか？

The first point of interest involves the evaluation of knowledge-based systems, with a focus beyond just logic.
最初の関心のあるポイントは、知識ベースのシステムの評価であり、単なる論理を超えた焦点を持っています。
This area calls for innovative methodologies to assess the system’s capacity to manage and utilize knowledge efficiently, going beyond traditional logical evaluations.
この分野は、従来の論理的評価を超えて、システムが知識を効率的に管理し利用する能力を評価するための革新的な方法論を求めています。
This topic of evaluation naturally extends to the question of how we evaluate ontologies and design patterns within knowledge engineering.
この評価のトピックは、**知識エンジニアリング内のオントロジーやデザインパターンをどのように評価するかという疑問**に自然に拡張されます。
Evaluating these aspects would require a deep dive into the structures and mechanisms underpinning these elements, potentially leading to the development of refined evaluation metrics and methodologies.
これらの側面を評価するには、これらの要素を支える構造とメカニズムを深く掘り下げる必要があり、洗練された評価指標や方法論の開発につながる可能性があります。
Interestingly, the long-standing paradigm of machine learning evaluation, relying on benchmarking against a standard train/test dataset, seems to falter in the era of LLMs.
**興味深いことに、標準のトレイン/テストデータセットに対するベンチマークに依存する機械学習評価の長年のパラダイムは、LLMの時代においては失敗しているようです。** (そうなの??:thinking:)
This presents an intriguing challenge for researchers and engineers alike.
これは、研究者やエンジニアにとって興味深い課題を提示します。
It is quite possible that traditional methods may need to be significantly buttressed by methodologies and supporting tools for the direct human evaluation of knowledge system performance.
従来の方法は、知識システムのパフォーマンスの直接的な人間評価のための方法論や支援ツールによって大幅に強化される必要があるかもしれません。
This has implications concerning the cost and speed of evaluation processes, encouraging the rethink of current approaches to perhaps develop new strategies that balance accuracy, cost-effectiveness, and timeliness.
これは、評価プロセスのコストと速度に関する影響があり、現在のアプローチを再考し、精度、コスト効率、タイムリーさのバランスを取る新しい戦略を開発することを促します。
Reimagining evaluation methodologies in this new context could provide transformative insights into how we can gain confidence in the reliability engineering of knowledge systems that use LLMs.
この新しい文脈で評価方法論を再考することは、LLMを使用する知識システムの信頼性エンジニアリングに自信を持つ方法に関する変革的な洞察を提供する可能性があります。
Developments in this direction may aid biodiversity researchers to get a better understanding of the real-world efficacy of employing knowledge-based systems with LLM components in their institutions.
この方向での進展は、生物多様性研究者が自らの機関でLLMコンポーネントを持つ知識ベースのシステムを使用することの実世界での有効性をよりよく理解するのに役立つかもしれません。
One can think of improving access to collections, knowledge discovery, or accuracy in describing institutional knowledge.
コレクションへのアクセスの改善、知識発見、または機関知識の記述の精度向上を考えることができます。

<!-- ここまで読んだ! -->

### 4.3.2 What is the relationship between evaluation and explainability? 評価と説明可能性の関係は何ですか？

Lastly, there is an inherent dependency of evaluation on effective solutions for explainability within knowledge systems.
最後に、評価は知識システム内の説明可能性に対する効果的な解決策に依存しています。
Understanding this relationship could help in the creation of more comprehensive evaluation models that take into account not only the performance of a system but also its explainability.
この関係を理解することは、システムのパフォーマンスだけでなく、その説明可能性も考慮に入れたより包括的な評価モデルの作成に役立つかもしれません。

### 5 Summary 要約

In this paper, we have advocated for a reconsideration of the practice and methodology of knowledge engineering in light of the emergence of LLMs.
本論文では、LLMの出現を踏まえた知識エンジニアリングの実践と方法論の再考を提唱しました。
We argued that LLMs allow naturally-occurring and humanly-evolved means of conveying knowledge to be brought to bear in the automation of knowledge tasks.
私たちは、LLMが自然に発生し、人間が進化させた知識を伝える手段を知識タスクの自動化に活用できると主張しました。
We described how this can enhance the engineering of hybrid neuro-symbolic knowledge systems, and how this can make knowledge engineering possible by people who do not necessarily have the experience of recasting natural language into formal, structured representation languages.
これがハイブリッド神経シンボリック知識システムのエンジニアリングをどのように強化できるか、そしてこれが自然言語を正式で構造化された表現言語に再構成する経験を持たない人々による知識エンジニアリングを可能にするかを説明しました。
(これが本論文で提唱されてる2つのシナリオだよね! :thinking:)
Both of these possibilities will involve addressing a broad range of open questions, which we have attempted to outline above.
これらの可能性の両方は、私たちが上記で概説しようとした幅広い未解決の質問に対処することを含むでしょう。
Given the rapid pace of the development of this area of research, it is our earnest hope that the coming months and years will yield results shedding light on these questions.
この研究分野の急速な発展を考慮すると、今後数ヶ月および数年でこれらの質問に光を当てる結果が得られることを切に願っています。

<!-- ここまで読んだ! -->
