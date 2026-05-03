refs: https://arxiv.org/pdf/2408.08878v1


## Knowledge Prompting: How Knowledge Engineers Use Large Language Models
## 知識プロンプティング：知識エンジニアが大規模言語モデルをどのように使用するか

### ELISAVET KOUTSIANA[∗], King’s College London, United Kingdom 
### JOHANNA WALKER[∗], King’s College London, United Kingdom 
### MICHELLE NWACHUKWU, King’s College London, United Kingdom 
### ALBERT MEROÑO-PEÑUELA, King’s College London, United Kingdom 
### ELENA SIMPERL[∗], King’s College London, United Kingdom  

Despite many advances in knowledge engineering (KE), challenges remain in areas such as engineering knowledge graphs (KGs) at scale, keeping up with evolving domain knowledge, multilingualism, and multimodality. 
知識工学（KE）における多くの進展にもかかわらず、スケールでの知識グラフ（KG）のエンジニアリング、進化するドメイン知識の把握、多言語性、マルチモーダリティなどの分野では課題が残っています。

Recently, KE has used LLMs to support semi-automatic tasks, but the most effective use of LLMs to support knowledge engineers across the KE activities is still in its infancy. 
最近、KEはLLMsを使用して半自動タスクをサポートしていますが、KE活動全体で知識エンジニアをサポートするためのLLMsの最も効果的な使用はまだ初期段階にあります。

To explore the vision of LLM copilots for KE and change existing KE practices, we conducted a multimethod study during a KE hackathon. 
KEのためのLLMコパイロットのビジョンを探求し、既存のKEプラクティスを変えるために、KEハッカソン中に多方法研究を実施しました。

We investigated participants’ views on the use of LLMs, the challenges they face, the skills they may need to integrate LLMs into their practices, and how they use LLMs responsibly. 
私たちは、参加者がLLMsの使用についての見解、直面している課題、LLMsを自分の実践に統合するために必要なスキル、そしてLLMsを責任を持って使用する方法を調査しました。

We found participants felt LLMs could contribute to improving efficiency when engineering KGs, but presented increased challenges around the already complex issues of evaluating the KE tasks. 
参加者は、LLMsがKGをエンジニアリングする際の効率向上に寄与できると感じましたが、KEタスクの評価に関する既に複雑な問題に対して新たな課題を提示しました。

We discovered prompting to be a useful but undervalued skill for knowledge engineers working with LLMs, and note that natural language processing skills may become more relevant across more roles in KG construction. 
プロンプティングは、LLMsを使用する知識エンジニアにとって有用であるが過小評価されているスキルであることがわかりました。また、自然言語処理スキルはKG構築のより多くの役割でより関連性が高くなる可能性があることに注意しました。

Integrating LLMs into KE tasks needs to be mindful of potential risks and harms related to responsible AI. 
LLMsをKEタスクに統合する際は、責任あるAIに関連する潜在的なリスクや害に留意する必要があります。

Given the limited ethical training, most knowledge engineers receive solutions such as our suggested ‘KG cards’ based on data cards could be a useful guide for KG construction. 
限られた倫理的トレーニングを考慮すると、ほとんどの知識エンジニアが受ける解決策として、私たちが提案するデータカードに基づく「KGカード」がKG構築の有用なガイドとなる可能性があります。

Our findings can support designers of KE AI copilots, KE researchers, and practitioners using advanced AI to develop trustworthy applications, propose new methodologies for KE and operate new technologies responsibly. 
私たちの発見は、KE AIコパイロットの設計者、KE研究者、信頼できるアプリケーションを開発するために高度なAIを使用する実務者をサポートし、KEのための新しい方法論を提案し、新しい技術を責任を持って運用するのに役立ちます。

CCS Concepts: • Computing methodologies → **Ontology engineering; • Human-centered computing →** _Natural language_ interfaces; Ethnographic studies.  
CCS概念：• コンピューティング方法論 → **オントロジーエンジニアリング; • 人間中心のコンピューティング →** _自然言語_ インターフェース; エスノグラフィー研究。

Additional Key Words and Phrases: Knowledge Graph, Knowledge Engineering, Large Language Models, Hackathon, Ethnographic Study, Interviews, Knowledge Engineers Skills, Bias  
追加のキーワードとフレーズ：知識グラフ、知識工学、大規模言語モデル、ハッカソン、エスノグラフィー研究、インタビュー、知識エンジニアのスキル、バイアス  

**ACM Reference Format:**  
**ACM参照フォーマット：**  
Elisavet Koutsiana, Johanna Walker, Michelle Nwachukwu, Albert Meroño-Peñuela, and Elena Simperl. 2024. Knowledge Prompting:  
Elisavet Koutsiana, Johanna Walker, Michelle Nwachukwu, Albert Meroño-Peñuela, および Elena Simperl. 2024. 知識プロンプティング：  
[How Knowledge Engineers Use Large Language Models. 1, 1 (August 2024), 25 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn](https://doi.org/10.1145/nnnnnnn.nnnnnnn)  
知識エンジニアが大規模言語モデルをどのように使用するか。 1, 1 (2024年8月)、25ページ。 https://doi.org/10.1145/nnnnnnn.nnnnnnn



## 1 INTRODUCTION イントロダクション

Knowledge engineering (KE) is the process of capturing, structuring, representing and maintaining knowledge in a machine-readable way [84]. 
知識工学（KE）は、知識を機械可読な方法でキャプチャ、構造化、表現、維持するプロセスです[84]。 
The outcome of this process often takes the form of a knowledge graph (KG) [38]. 
このプロセスの結果は、しばしば知識グラフ（KG）の形を取ります[38]。 
Despite the remarkable evolution of the field, some challenges remain. 
この分野の著しい進化にもかかわらず、いくつかの課題が残っています。 
In particular, that of working at scale across all tasks, from extracting structured knowledge from large collections of domain information to keeping up with how domain knowledge evolves, to supporting multiple languages and modalities to assessing quality. 
特に、構造化された知識を大規模なドメイン情報のコレクションから抽出し、ドメイン知識の進化に追いつき、複数の言語やモダリティをサポートし、品質を評価するというすべてのタスクでスケールで作業することが課題です。 
The solution to scaling lies in automation, for which large language models (LLMs) hold great promise [73, 78]. 
スケーリングの解決策は自動化にあり、大規模言語モデル（LLMs）が大きな可能性を秘めています[73, 78]。 

LLMs have changed the way we work in many fields, including KE. 
LLMsは、KEを含む多くの分野で私たちの働き方を変えました。 
Knowledge engineers have been using natural language processing (NLP) methods and tools to semi-automate tasks like information extraction. 
知識エンジニアは、情報抽出のようなタスクを半自動化するために自然言語処理（NLP）手法やツールを使用してきました。 
However, we don’t know how LLMs affect or could affect those practices. 
しかし、LLMsがこれらの実践にどのように影響を与えるか、または与える可能性があるかはわかりません。 
To explore the changes in KE practices, we studied the interaction of researchers with LLMs to solve KE tasks. 
KEの実践における変化を探るために、私たちは研究者とLLMsとの相互作用を研究し、KEタスクを解決しました。 
For this purpose, the idea of a hackathon emerged during the Dagstuhl Seminar on “Knowledge Graphs and their Role in the Knowledge Engineering of the 21st Century” held in September 2022.[1] 
この目的のために、2022年9月に開催された「知識グラフと21世紀の知識工学におけるその役割」に関するダグシュタールセミナー中にハッカソンのアイデアが浮上しました。[1] 
We invited researchers and practitioners from the AI and KE fields to a four-day hackathon to investigate LLMs’ automation support for KE tasks. 
私たちは、AIおよびKE分野の研究者と実務者を招待し、KEタスクに対するLLMsの自動化サポートを調査するための4日間のハッカソンを開催しました。[2] 

Our study explored what challenges knowledge engineers face, the skills they may need to have, and what safety testing means in this concept. 
私たちの研究は、知識エンジニアが直面する課題、必要とされるスキル、そしてこの概念における安全性テストの意味を探求しました。 
Our investigation included an ethnographic study during the hackathon, followed by a set of semi-structured interviews after the event and a review of the documentary output of the hackathon. 
私たちの調査には、ハッカソン中の民族誌的研究、イベント後の一連の半構造化インタビュー、ハッカソンのドキュメンタリー出力のレビューが含まれました。 
Our research questions are: 
私たちの研究質問は次のとおりです：

(1) What are the main challenges experienced by knowledge engineers when using LLMs for KE tasks? 
(1) LLMsをKEタスクに使用する際に知識エンジニアが直面する主な課題は何ですか？ 

(2) How do knowledge engineers evaluate LLMs’ output for their practices? 
(2) 知識エンジニアは、彼らの実践に対してLLMsの出力をどのように評価しますか？ 

(3) What skills does a knowledge engineer need to incorporate LLMs into their practice? 
(3) 知識エンジニアは、LLMsを彼らの実践に組み込むためにどのようなスキルが必要ですか？ 

(4) How aware are knowledge engineers of using LLMs responsibly? 
(4) 知識エンジニアは、LLMsを責任を持って使用することにどの程度気づいていますか？ 

(5) What factors may affect knowledge engineers’ trust and uptake of the LLM technology? 
(5) どのような要因が知識エンジニアのLLM技術への信頼と受け入れに影響を与える可能性がありますか？ 

Our contributions are threefold: 
私たちの貢献は三つの側面があります：

we present one of the first user studies on the interaction of knowledge engineers with LLMs 
私たちは、知識エンジニアとLLMsとの相互作用に関する最初のユーザースタディの一つを提示します。 

we identify key areas of strength and challenge for KE with LLMs 
私たちは、LLMsを用いたKEの強みと課題の重要な領域を特定します。 

we propose data cards for KGs. 
私たちは、KGsのためのデータカードを提案します。 

Our findings: 
私たちの発見：

give direction to designers of KE AI copilots to create responsible applications 
KE AIコパイロットのデザイナーに責任あるアプリケーションを作成するための方向性を提供します。 

guide KE researchers and practitioners developing new methodologies 
新しい方法論を開発するKE研究者と実務者を指導します。 

advise practitioners wishing to use advanced AI technologies responsibly. 
高度なAI技術を責任を持って使用したい実務者に助言します。 



## 2 BACKGROUND AND RELATED WORK 背景と関連研究

In this section, we describe the background and related work for KE, automation in KE, and responsible AI.  
このセクションでは、知識工学（KE）、KEにおける自動化、および責任あるAIに関する背景と関連研究を説明します。

**2.1** **Knowledge engineering 知識工学**  
KGs represent real-world entities and their relations [38].  
KG（知識グラフ）は、現実世界のエンティティとその関係を表現します[38]。  
The graph structure offers efficient data management, availability of data in different modalities, use of machine learning and crowdsourcing techniques, and lowers cost.  
グラフ構造は、効率的なデータ管理、異なるモダリティでのデータの可用性、機械学習やクラウドソーシング技術の利用を提供し、コストを削減します。  
KGs can be built from numerous sources and often use a schema, an ontology or rules for representation [38].  
KGは多数のソースから構築でき、しばしばスキーマ、オントロジー、または表現のためのルールを使用します[38]。  
KG construction activities workflow depends on the actors involved, the represented domain, the construction tools, and the available data source [38].  
KGの構築活動のワークフローは、関与するアクター、表現されるドメイン、構築ツール、および利用可能なデータソースに依存します[38]。  
Key actors generally include domain experts, specialising in the intricacies of the topic under consideration.  
主要なアクターには、一般的に、検討中のトピックの複雑さに特化したドメイン専門家が含まれます。  
Knowledge engineers elicit insights from these experts to create a conceptual domain model, and in turn, ontology engineers represent this knowledge in a suitable machine language [83].  
知識エンジニアは、これらの専門家から洞察を引き出し、概念的なドメインモデルを作成し、その後、オントロジーエンジニアがこの知識を適切な機械言語で表現します[83]。  
KGs can be built and enriched manually using human collaboration (e.g., enterprise employees or crowdsourcing platforms) [36, 93], and automatically (e.g., NLP) [59, 60] to extract knowledge from text, markup, and structured sources.  
KGは、人間の協力（例：企業の従業員やクラウドソーシングプラットフォーム）を使用して手動で構築および強化することができ[36, 93]、自動的に（例：NLP）テキスト、マークアップ、および構造化されたソースから知識を抽出することもできます[59, 60]。  
Ontologies are often used to structure human knowledge.  
オントロジーは、人間の知識を構造化するためにしばしば使用されます。  
Ontology requirements outline what the ontology should be able to do, what knowledge it should contain, and who will be using it [74].  
オントロジーの要件は、オントロジーが何をできるべきか、どのような知識を含むべきか、誰がそれを使用するかを概説します[74]。  
One of the ways to determine the scope of the ontology is to set a list of questions that a KG based on the ontology should be able to answer known as competency questions [74].  
オントロジーの範囲を決定する方法の一つは、オントロジーに基づくKGが答えることができるべき質問のリストを設定することです。これを能力質問（competency questions）と呼びます[74]。  
Following this, conceptualisation techniques help identify and structure the knowledge represented in the ontology, implementation techniques involve selecting the appropriate ontology language and tools to build the ontology, and finally, evaluation techniques assess the ontology’s accuracy, usability, and compliance with requirements [53, 83].  
これに続いて、概念化技術はオントロジーに表現された知識を特定し構造化するのを助け、実装技術はオントロジーを構築するための適切なオントロジー言語とツールを選択し、最後に評価技術はオントロジーの正確性、使いやすさ、および要件への適合性を評価します[53, 83]。  
Quality assessment is the evaluation of the KG on a number of dimensions [38].  
品質評価は、KGをいくつかの次元で評価することです[38]。  
KGs must be evaluated on their syntactic and semantic accuracy, and their timeliness [25, 28, 47, 59].  
KGは、その構文的および意味的正確性、ならびにタイムリーさに基づいて評価されなければなりません[25, 28, 47, 59]。  
Coverage is the KG value of completeness and representativeness (assessing the level of bias of the existing knowledge in the KG, whether this is inherent in the data, the schema or the reasoning) [19, 42, 48, 59].  
カバレッジは、KGの完全性と代表性の価値です（KG内の既存の知識のバイアスのレベルを評価し、これがデータ、スキーマ、または推論に内在するかどうかを判断します）[19, 42, 48, 59]。  
Coherency refers to consistency - whether the KG is free of contradiction and consistent with the domain it represents - and validity [9, 87].  
一貫性は、矛盾がなく、表現するドメインと一貫しているかどうかを指します - そして妥当性[9, 87]。  
Succinctness refers to the KG’s conciseness and understandability (by humans) [39, 48].  
簡潔さは、KGの簡潔さと理解しやすさ（人間による）を指します[39, 48]。  
The above categories can be assessed type using validation tools [28] such as: human evaluation; measuring precision and recall against gold standards or other sources; or comparing known statistical distributions with those of the KG [19, 25, 59].  
上記のカテゴリは、検証ツール[28]を使用して評価することができます。例えば：人間による評価、ゴールドスタンダードや他のソースに対する精度と再現率の測定、またはKGの既知の統計分布と比較することです[19, 25, 59]。  
While not complicated, these assessments can involve a considerable amount of effort.  
複雑ではありませんが、これらの評価にはかなりの労力がかかる場合があります。  
A standard practice to ensure quality and to correct errors is to use rules and constraints that the KG needs to follow [38].  
品質を確保し、エラーを修正するための標準的な手法は、KGが従う必要のあるルールと制約を使用することです[38]。  
Domain experts are the most suitable specialists for creating these rules, however this is an expensive, manual process.  
ドメイン専門家は、これらのルールを作成するための最も適した専門家ですが、これは高価で手動のプロセスです。  
Previous studies argued that knowledge engineers, besides technical skills, require good communication, conceptual ability, patience, organisational skills and knowledge in diverse areas [61, 68].  
以前の研究では、知識エンジニアは、技術的スキルに加えて、良好なコミュニケーション、概念的能力、忍耐、組織スキル、および多様な分野の知識を必要とすると主張しています[61, 68]。  
In a collaborative ontology engineering scenario, each member can play several roles, depending on the types of contributions and the technology used [83].  
共同オントロジーエンジニアリングのシナリオでは、各メンバーは、貢献の種類や使用される技術に応じて、いくつかの役割を果たすことができます[83]。  
To merge the gap in communication between domain experts and knowledge engineers, ontology engineering research actively involves domain experts in ontology development with the use of technologies such as controlled natural language, semantic wikis, intelligent user interfaces and social commuting [22].  
ドメイン専門家と知識エンジニアの間のコミュニケーションのギャップを埋めるために、オントロジーエンジニアリング研究は、制御された自然言語、セマンティックウィキ、インテリジェントユーザーインターフェース、ソーシャルコミュニケーションなどの技術を使用して、オントロジー開発にドメイン専門家を積極的に関与させています[22]。  
However, all this is disrupted by the advent of LLMs.  
しかし、これらすべてはLLMの出現によって混乱しています。  
Today, people and AI agents collaborate to engineer a KG, changing how knowledge engineers work.  
今日、人々とAIエージェントはKGを構築するために協力し、知識エンジニアの働き方を変えています。

**2.2** **Automation in knowledge engineering 知識工学における自動化**  
Automation has long held promise for KE tasks.  
自動化は、KEタスクに対して長い間期待されてきました。  
Various automatic processes are utilised for KE tasks, including knowledge extraction, refinement, and enrichment [86].  
知識抽出、洗練、強化など、さまざまな自動プロセスがKEタスクに利用されています[86]。  
Knowledge extraction from structured and unstructured sources [73] requires manual and automated approaches.  
構造化されたソースと非構造化されたソースからの知識抽出[73]には、手動および自動アプローチが必要です。  
The automated approach can include a number of machine learning techniques: named-entity recognition (NER) to identify name entities in a text, which are words like people, organisations, and locations [95];  
自動化されたアプローチには、いくつかの機械学習技術が含まれる場合があります：テキスト内の名前エンティティを特定するための固有表現認識（NER）、これは人々、組織、場所などの単語です[95]；  
entity linking to link associated entities in a KG with mentions of entities in text [49];  
エンティティリンクは、KG内の関連エンティティをテキスト内のエンティティの言及とリンクします[49]；  
and relation extraction to identify the relation between entities in a text [14].  
関係抽出は、テキスト内のエンティティ間の関係を特定します[14]。  
However, automated approaches demand costly and time-consuming techniques with human-annotated datasets for the supervised machine-learning training, and human evaluation for the unsupervised pre-trained models.  
しかし、自動化されたアプローチは、監視された機械学習トレーニングのための人間が注釈を付けたデータセットや、非監視の事前トレーニングモデルのための人間評価を必要とする高コストで時間のかかる技術を要求します。  
Furthermore, automated knowledge extraction still presents low accuracy, which can lead to low quality KGs [78, 91].  
さらに、自動化された知識抽出は依然として低い精度を示し、これが低品質のKGにつながる可能性があります[78, 91]。  
KG refinement refers to techniques for KG completion and correction [55, 58].  
KGの洗練は、KGの完成と修正のための技術を指します[55, 58]。  
For KG completion, the aim is to add missing knowledge to the graph, which is an ongoing process.  
KGの完成の目的は、グラフに欠落している知識を追加することであり、これは継続的なプロセスです。  
In this case, KG embedding models are used as a technique to represent information from a KG in a way that computers can understand and work with [18].  
この場合、KG埋め込みモデルは、KGからの情報をコンピュータが理解し、操作できる方法で表現するための技術として使用されます[18]。  
This is the process of turning complex things like entities and relationships in the KG into a simpler format, like numerical vectors.  
これは、KG内のエンティティや関係のような複雑なものを、数値ベクトルのようなより単純な形式に変換するプロセスです。  
KG embeddings are used for link prediction [11], entity resolution [44], relation classification [98] etc.  
KG埋め込みは、リンク予測[11]、エンティティ解決[44]、関係分類[98]などに使用されます。  
In addition, in KG completion, it may be valuable to incorporate cross-lingual entities, as well as different modalities such as images, videos, audio haptics etc.  
さらに、KGの完成においては、クロスリンガルエンティティや、画像、動画、音声触覚などの異なるモダリティを組み込むことが価値があります。  
This is essential for machines to be able to capture the real world in terms of language or human expression through means other than symbolic [16].  
これは、機械が言語や人間の表現を象徴的な手段以外で捉えることができるために不可欠です[16]。  
Multilingualism is challenging to capture since there are limited non-English language datasets, entity extraction models must be retrained for each language, and translation systems are not always accurate [78].  
多言語性を捉えることは困難であり、非英語のデータセットが限られているため、エンティティ抽出モデルは各言語ごとに再トレーニングする必要があり、翻訳システムは常に正確であるとは限りません[78]。  
For multimodality, there are many attempts to describe the different types of knowledge.  
マルチモダリティに関しては、さまざまな種類の知識を説明する試みが多数あります。  
Some knowledge can only be accurately represented in its native modality, for example, musical chords [20].  
一部の知識は、そのネイティブモダリティでのみ正確に表現できます。例えば、音楽の和音です[20]。  
Additionally, while humans are good at providing textual input, some tasks require output in other modes, such as haptics [67].  
さらに、人間はテキスト入力を提供するのが得意ですが、一部のタスクでは触覚などの他のモードでの出力が必要です[67]。  
The extensive availability of images of the web means that visuals are the most often used media in KGs [16].  
ウェブ上の画像の広範な可用性は、視覚がKGで最も頻繁に使用されるメディアであることを意味します[16]。  
However, finding and integrating other multimodal information can be challenging.  
しかし、他のマルチモーダル情報を見つけて統合することは困難です。  
There are limited examples of multimodal datasets, making it difficult to find data and ensure that the different modalities refer to the same entity [16].  
マルチモーダルデータセットの例は限られており、データを見つけて異なるモダリティが同じエンティティを指すことを保証するのが難しくなります[16]。  
These issues are compounded in specific verticals.  
これらの問題は特定の分野で複雑化します。  
Knowledge extraction for domains such as heritage remains complicated and time-consuming [15, 20, 89].  
遺産などのドメインにおける知識抽出は、依然として複雑で時間がかかります[15, 20, 89]。  
In contrast, for KG correction, the aim is to correct existing entities and relations.  
対照的に、KGの修正の目的は、既存のエンティティと関係を修正することです。  
This task can use automatic techniques such as logical inference based on the rules between already existing relations to create and correct new entities and relations.  
このタスクでは、既存の関係間のルールに基づく論理的推論などの自動技術を使用して、新しいエンティティと関係を作成および修正できます。  
Machine learning techniques can also be utilised for this task such as statistical relational learning, building embedding-based link predictors and node classifiers [86].  
このタスクには、統計的関係学習、埋め込みベースのリンク予測器やノード分類器の構築などの機械学習技術も利用できます[86]。  
KG enrichment can incorporate ontology refinement and alignment to improve a given KG.  
KGの強化は、与えられたKGを改善するためにオントロジーの洗練と整合を組み込むことができます。  
In refinement, the aim is to improve text inconsistencies and add meta information like descriptions to entities [58].  
洗練においては、テキストの不整合を改善し、エンティティに説明のようなメタ情報を追加することが目的です[58]。  
In addition, for alignment, LLMs have been used to identify and match entities between KGs, for example, using lexical matching [101].  
さらに、整合のために、LLMがKG間のエンティティを特定し、マッチングするために使用されています。例えば、語彙マッチングを使用します[101]。  
In both cases, developing sufficient and reliable tools can be challenging.  
いずれの場合も、十分で信頼できるツールを開発することは困難です。  
Traditional methods and techniques require revision and modification to serve knowledge engineers in the production of trustworthy and beneficial KGs.  
従来の方法と技術は、信頼できる有益なKGの生成において知識エンジニアに役立つように改訂と修正が必要です。  
Opportunities for automation have grown considerably with the advent of generative AI.  
生成AIの出現により、自動化の機会は大幅に増加しました。  
Pre-trained LLMs like BERT and GPT model families use transformer architecture to achieve state-of-the-art performance for numerous natural language tasks [63].  
BERTやGPTモデルファミリーのような事前トレーニングされたLLMは、トランスフォーマーアーキテクチャを使用して、数多くの自然言語タスクで最先端のパフォーマンスを達成します[63]。  
Two very common processes of LLMs are fine-tuning and prompting [40].  
LLMの非常に一般的な2つのプロセスは、ファインチューニングとプロンプティングです[40]。  
For fine-tuning, a pre-trained model is further trained on a specific task or dataset to improve its knowledge of a particular task or domain.  
ファインチューニングでは、事前トレーニングされたモデルが特定のタスクやデータセットでさらにトレーニングされ、特定のタスクやドメインに関する知識を向上させます。  
For prompting, a natural language text is given as input to enable the model to perform specific tasks [5].  
プロンプティングでは、自然言語のテキストが入力として与えられ、モデルが特定のタスクを実行できるようにします[5]。  
Prompting in a sufficient way to improve models’ outputs requires a number of techniques and rules, introducing the field of prompt engineering [90].  
モデルの出力を改善するために十分な方法でプロンプティングを行うには、いくつかの技術とルールが必要であり、これがプロンプトエンジニアリングの分野を導入します[90]。  
For prompting, the input to LLM instructions are classified as zero-shot and few-shot prompts, where shot means an example [90].  
プロンプティングでは、LLMの指示への入力はゼロショットとフューショットプロンプトに分類されます。ここで、ショットは例を意味します[90]。  
Zero-shot prompts are used in situations where it is not necessary to train the LLM, i.e. no specific examples are provided for the task at hand.  
ゼロショットプロンプトは、LLMをトレーニングする必要がない状況、つまり、現在のタスクに対して特定の例が提供されない場合に使用されます。  
This relies on the LLM’s ability to follow instructions and generate the desired output.  
これは、LLMが指示に従い、望ましい出力を生成する能力に依存します。  
In contrast, in few-shot prompts, the LLM is guided on a task by providing a small set of one or more examples [90].  
対照的に、フューショットプロンプトでは、LLMは1つ以上の例の小さなセットを提供することによってタスクに導かれます[90]。  
The advent of LLMs revealed two perspectives for KE; KGs can be used to enhance LLMs, and LLMs capabilities can be used to assist on KE tasks [2].  
LLMの出現は、KEに対する2つの視点を明らかにしました。KGはLLMを強化するために使用でき、LLMの能力はKEタスクを支援するために使用できます[2]。  
This study considers the second task.  
この研究は、第二のタスクを考慮します。

**2.3** **Responsible AI 責任あるAI**  
Introducing the use of LLMs to KE requires a close understanding of how to use such AI responsibly.  
KEにLLMの使用を導入するには、そのようなAIを責任を持って使用する方法を深く理解する必要があります。



. Responsible AI has many underlying principles and themes that ensure the safe deployment of AI systems [62]. 
責任あるAIには、AIシステムの安全な展開を確保するための多くの基本原則とテーマがあります[62]。

Safety in AI is a principle of AI ethics, one that focuses on preventing harm, specifically harm towards human well-being [50]. 
AIにおける安全性はAI倫理の原則であり、特に人間の幸福に対する害を防ぐことに焦点を当てています[50]。

AI safety can be used to describe harms in multiple ways. 
AIの安全性は、さまざまな方法で害を説明するために使用できます。

For example, there is the existential safety risk of the fast development of AI without regulation [13], and there is the safe development of current AI systems where AI systems deployed currently hold safety risks and may undermine our trust in them [82]. 
例えば、規制なしにAIが急速に発展することによる存在的な安全リスク[13]があり、現在展開されているAIシステムには安全リスクがあり、それが私たちの信頼を損なう可能性があるという安全な開発があります[82]。 

In this study we are interested in the latter. 
本研究では後者に興味があります。

Safety in AI intersects and is reliant on a number of AI ethical themes [50, 52]: 
AIにおける安全性は、いくつかのAI倫理テーマと交差し、依存しています[50, 52]：

Transparency/explainability - being transparent about why a certain decision is made and the capability to explain this appropriately for specific stakeholders. 
透明性/説明可能性 - 特定の意思決定がなぜ行われたのかを透明にし、特定の利害関係者に対して適切に説明する能力。

Privacy - ensuring data privacy through the data processing and use lifecycle of AI systems 
プライバシー - AIシステムのデータ処理と使用ライフサイクルを通じてデータプライバシーを確保すること。

Accountability - ensuring the proper function of AI and compliance with regulation frameworks. 
説明責任 - AIの適切な機能と規制フレームワークへの準拠を確保すること。

Fairness/bias - acting to reduce the likelihood that an algorithm or data systematically produces bias results due to assumptions that are made [75] leading to unfair outcomes of AI systems that discriminate against certain demographic sub-groups. 
公平性/バイアス - アルゴリズムやデータが行われた仮定により体系的にバイアス結果を生じる可能性を減らすために行動すること[75]。これは、特定の人口統計サブグループに対して差別的なAIシステムの不公平な結果につながります。

LLMs are a black-box models, it is not always possible to understand how outputs come about thus transparency can be very difficult and it is hard to explain their results. 
LLMはブラックボックスモデルであり、出力がどのように生成されるかを理解することは常に可能ではないため、透明性が非常に難しく、結果を説明することが困難です。

This is further complicated by a lack of transparency over data training sets, which also increases the risk of the inclusion of personal data. 
これは、データトレーニングセットに関する透明性の欠如によってさらに複雑になり、個人データの含有リスクも高まります。

As generative AI can reproduce data that is present in the training data, it is hard to ensure privacy as it cannot be guaranteed that this data does not appear in outputs. 
生成AIはトレーニングデータに存在するデータを再現できるため、このデータが出力に現れないことを保証できないため、プライバシーを確保することは困難です。

LLMs have been shown to be biased, which can lead to unfair outcomes. 
LLMはバイアスがあることが示されており、これが不公平な結果をもたらす可能性があります。

Lack of clarity on data and training processes also means accountability is difficult to establish. 
データとトレーニングプロセスに関する明確さの欠如は、説明責任を確立することが難しいことも意味します。

Transparency, explainability, and bias are all elements that need considering for any automated KG process; however, they may be exacerbated with the use of LLMs. 
透明性、説明可能性、バイアスは、任意の自動化されたKGプロセスにおいて考慮すべき要素ですが、LLMの使用によって悪化する可能性があります。

Previous studies on the use of LLMs show that they lack sufficient accuracy and credibility to be used without human supervision, particularly regarding the lack of provenance and propensity to hallucinate [45]. 
LLMの使用に関する以前の研究は、特に出所の欠如と幻覚の傾向に関して、LLMが人間の監視なしで使用するには十分な精度と信頼性を欠いていることを示しています[45]。

Provenance and accuracy are particularly important to KG as a trusted knowledge source, as exemplified by Wikidata. 
出所と精度は、信頼できる知識源としてのKGにとって特に重要であり、Wikidataがその例です。

These flag the need for transparency and explainability. 
これらは、透明性と説明可能性の必要性を示しています。

Due to the complexity of models, transparency and explainability have been previously explored through documentation for the models or the datasets used to train the models. 
モデルの複雑さのため、透明性と説明可能性は、モデルやモデルをトレーニングするために使用されるデータセットの文書を通じて以前に探求されてきました。

Mitchell et al. [65] suggested a framework called Model Cards to encourage transparent model reporting. 
Mitchellら[65]は、透明なモデル報告を促進するためのModel Cardsというフレームワークを提案しました。

The framework includes a list of metadata like model details, intended use, factors, demographics, performance, evaluation data, training data, supplementary analysis and ethical considerations. 
このフレームワークには、モデルの詳細、意図された使用、要因、人口統計、パフォーマンス、評価データ、トレーニングデータ、補足分析、倫理的考慮事項などのメタデータのリストが含まれています。

Similarly, Pushkarna et al. [81] introduced a framework called Data Cards for purposeful documentation of datasets as an attempt to offer clear documentation of datasets to produce better explained models. 
同様に、Pushkarnaら[81]は、より明確なデータセットの文書を提供し、より良い説明されたモデルを生成するための目的を持ったデータセットの文書化のためのData Cardsというフレームワークを導入しました。

The framework suggests a structured list of summaries related to datasets’ metadata such as explanations, rationales, provenance, representation, usage, and fairness. 
このフレームワークは、説明、根拠、出所、表現、使用、公平性など、データセットのメタデータに関連する要約の構造化されたリストを提案しています。

In terms of bias this may occur in KG using either manual or automatic ways for completion [92]. 
バイアスに関しては、KGの完成に手動または自動の方法を使用することで発生する可能性があります[92]。

There are also wide ranges of bias, including gender, representatives, and selectivity, which may become encoded into KGs via a number of automated processes. 
性別、代表性、選択性を含むさまざまなバイアスがあり、これらは多くの自動化プロセスを通じてKGにエンコードされる可能性があります。

For example, an issue found in information extraction (IE) is the biased statistical dependencies between entities and classes, which is known as spurious correlation [29, 70]. 
例えば、情報抽出（IE）で見つかる問題は、エンティティとクラス間のバイアスのある統計的依存関係であり、これは虚偽の相関として知られています[29, 70]。

Models heavily rely on this type of correlation between the output labels and surface features which effects the performances generalisation. 
モデルは、出力ラベルと表面特徴間のこの種の相関に大きく依存しており、パフォーマンスの一般化に影響を与えます。

This is due to unbalanced data distributions where entities appear to be casually related but are not. 
これは、エンティティが偶然に関連しているように見えるが、実際にはそうではない不均衡なデータ分布によるものです。

Causal inference is a method that has been used to tackle this specific issue by replacing the target entities [96, 97, 100]. 
因果推論は、ターゲットエンティティを置き換えることによってこの特定の問題に対処するために使用されている方法です[96, 97, 100]。

Counterfactual Manuscript submitted to ACM  
-----
6 Elisavet Koutsiana, Johanna Walker, Michelle Nwachukwu, Albert Meroño-Peñuela, and Elena Simperl
IE (CFIE) [70] extends this method by considering structural information which has been shown to be an important consideration for IE tasks as non-local interactions can be captured [46, 103]. 
反事実情報抽出（CFIE）[70]は、構造情報を考慮することによってこの方法を拡張し、非局所的相互作用を捉えることができるため、IEタスクにとって重要な考慮事項であることが示されています[46, 103]。

NER has been shown to have bias. 
NERにはバイアスがあることが示されています。

There is named regularity bias in which the models’ ability to use contextualised information when predicting the type of entity is ambiguous [29]. 
モデルがエンティティのタイプを予測する際に文脈情報を使用する能力が曖昧であるという名付けられた規則性バイアスがあります[29]。

A study that specifically looked at the biases that dictionary definitions have on the outcomes of the NER method [102]. 
辞書の定義がNER手法の結果に与えるバイアスを特に調査した研究があります[102]。

NER has also been shown to be better at identifying names from specific demographic groups [64, 77]. 
NERは特定の人口統計グループから名前を特定するのが得意であることも示されています[64, 77]。

Demographic biases in KGs have the potential to be caused by neural network-based relation extractions and NER systems excluding protective variables when extracting and processing knowledge [77]. 
KGにおける人口統計バイアスは、知識を抽出および処理する際に保護変数を除外する神経ネットワークベースの関係抽出およびNERシステムによって引き起こされる可能性があります[77]。

A method where this bias has been addressed is by including information from crowdsourced contributors such as background and information seeking process used to research a certain conclusion, tracking potential biases in collected data [21]. 
このバイアスに対処する方法は、特定の結論を研究するために使用される背景や情報探索プロセスなど、クラウドソースの寄稿者からの情報を含め、収集されたデータの潜在的なバイアスを追跡することです[21]。

Semantic role labelling (SRL) is a technique which returns predicate-argument structures for input sentences. 
意味役割ラベリング（SRL）は、入力文に対して述語-引数構造を返す技術です。

This technique has been shown to have demographic bias, such as gender and race bias [104]. 
この技術は、性別や人種のバイアスなどの人口統計バイアスを持つことが示されています[104]。

This technique has also been shown to have commonsense bias where this technique is unable to take into account basic knowledge considered to be commonsense [56]. 
この技術は、常識と見なされる基本的な知識を考慮できない常識バイアスを持つことも示されています[56]。

The fact that LLMs are known for generating stereotypes or discriminating data is that they use automated KE deserves particular attention [69]. 
LLMがステレオタイプや差別的データを生成することで知られている事実は、彼らが自動化された知識抽出を使用しているため、特に注意を要します[69]。

Further, removal of bias is a difficult task as humans are prone to bias of many types [51, 54]. 
さらに、バイアスの除去は困難な作業であり、人間は多くの種類のバイアスに陥りやすいためです[51, 54]。



## 3 METHODOLOGY 方法論

During August 2023 we organised a four-day research hackathon for knowledge engineers and AI researchers to investigate KE with prompt engineering.[3] 
2023年8月に、知識エンジニアとAI研究者のための4日間の研究ハッカソンを開催し、プロンプトエンジニアリングを用いたKEを調査しました。[3] 
The hackathon format offered a tool to explore emerging practices as KE processes and approaches are disrupted by generative AI. 
このハッカソンの形式は、生成AIによってKEプロセスとアプローチが混乱する中で、新たな実践を探求する手段を提供しました。 
This hackathon idea emerged from discussions at the Dagstuhl Seminar on “Knowledge Graphs and their Role in the Knowledge Engineering of the 21st Century” held in September 2022. 
このハッカソンのアイデアは、2022年9月に開催された「知識グラフと21世紀の知識工学におけるその役割」に関するダグシュタールセミナーでの議論から生まれました。 
The project topics (see Table 1) were defined in a community process with 30 experts [33]. 
プロジェクトのトピック（表1を参照）は、30人の専門家とのコミュニティプロセスで定義されました。[33] 
The hackathon hosted 39 participants from 15 different institutes and various environments from academia and industry, with 31 PhD students, 2 postdocs, 1 lecturers, 2 professors, and 3 industry members. 
ハッカソンには、15の異なる機関から39人の参加者が集まり、31人の博士課程学生、2人のポスドク、1人の講師、2人の教授、3人の業界メンバーが参加しました。 
The hackathon attendees were selected based on their background and experience with KE. 
ハッカソンの参加者は、KEに関する背景と経験に基づいて選ばれました。 
They were selected from European research labs that have a strong profile in either publishing in KE venues, or in offering well-used KE industry products. 
彼らは、KE関連の出版物を持つか、広く使用されているKE業界製品を提供している強力なプロファイルを持つ欧州の研究所から選ばれました。 
During the hackathon, participants split into 7 groups of 5 to 7 members, based on their prior experience in KE. 
ハッカソン中、参加者はKEにおける以前の経験に基づいて5〜7人の7つのグループに分かれました。 
Each group investigated one of the topics presented in Table 1. 
各グループは、表1に示されたトピックの1つを調査しました。 
Participants received high level descriptions of the projects but were free to choose which tools, methodologies, domains, and LLM techniques they focused on. 
参加者はプロジェクトの高レベルの説明を受けましたが、どのツール、方法論、ドメイン、LLM技術に焦点を当てるかは自由に選択できました。 

**3.1** **Data Collection and Preparation データ収集と準備**

Data was collected using three approaches to ensure rich data. 
データは、豊富なデータを確保するために3つのアプローチを使用して収集されました。 
The complete list of datasets can be seen in Table 2. 
データセットの完全なリストは表2に示されています。 
_1. Ethnographic observation. Two researchers performed an ethnographic observation study, using the ‘observer as participant’ technique for ethnographic research [24]. 
_1. エスノグラフィック観察。2人の研究者がエスノグラフィック研究のために「参加者としての観察者」技術を使用してエスノグラフィック観察研究を行いました。[24] 
The observer as participant role moves the observer into the study environment and closer to the activity of interest. 
参加者としての観察者の役割は、観察者を研究環境に移動させ、関心のある活動に近づけます。 
The participants are aware of the observer, but the observer is not engaging with the participants and does not ask or interact with anyone. 
参加者は観察者の存在を認識していますが、観察者は参加者と関わらず、誰にも質問したり対話したりしません。 
The researchers observed the various groups and kept detailed notes of the 7 groups’ interactions and decisions. 
研究者はさまざまなグループを観察し、7つのグループの相互作用と決定の詳細なノートを保持しました。 
3urlhttps://king-s-knowledge-graph-lab.github.io/knowledge-prompting-hackathon/ 
3urlhttps://king-s-knowledge-graph-lab.github.io/knowledge-prompting-hackathon/ 
Manuscript submitted to ACM  
-----
Knowledge Prompting: How Knowledge Engineers Use Large Language Models 7
_2. Documents collected from the hackathon. Research output in the form of reports and documentation from the hackathon was collected. 
_2. ハッカソンから収集された文書。ハッカソンからの報告書や文書の形で研究成果が収集されました。 
Hackathon groups produced reports regarding their experience answering specific questions and slide presentations with their strategies and results. 
ハッカソンのグループは、特定の質問に答える経験に関する報告書と、戦略と結果を示すスライドプレゼンテーションを作成しました。 
This resulted in 7 ppts and reports. 
これにより、7つのpptと報告書が作成されました。 
These two data collection activities were conducted contemporaneously with the Hackathon. 
これらの2つのデータ収集活動は、ハッカソンと同時に行われました。 
_3. Semi-structured interviews. After the hackathon, we contacted 14 participants who had volunteered to participate in follow-up interviews to talk about their opinions and experiences interacting with LLMs for KE tasks. 
_3. 半構造化インタビュー。ハッカソン後、KEタスクのためにLLMsと対話する経験や意見について話すために、フォローアップインタビューに参加することを希望した14人の参加者に連絡しました。 
Interviewees had backgrounds in KG construction, KG explainability, ontologies, and machine learning, as well as biology and bioinformatics, data management, FAIR data [23], and digital humanities. 
インタビュー対象者は、KG構築、KGの説明可能性、オントロジー、機械学習、さらには生物学とバイオインフォマティクス、データ管理、FAIRデータ[23]、デジタル人文学のバックグラウンドを持っていました。 
We conducted these interviews virtually between 17 8 2023 and 6 9 2023 using Microsoft Teams.[4] 
これらのインタビューは、2023年8月17日から2023年9月6日まで、Microsoft Teamsを使用して仮想的に実施しました。[4] 
The interview guide can be found in Appendix A. 
インタビューガイドは付録Aにあります。 
/ / / / 
We used Otter.ai [5] to transcribe the interview recordings. 
インタビューの録音を文字起こしするために、Otter.ai [5]を使用しました。 
This and the written data sources were then uploaded into NVIVO [6]. 
これと書面データソースは、その後NVIVO [6]にアップロードされました。 

**3.2** **Data Analysis データ分析**

To address our research questions, we conducted thematic analysis across all the data. 
研究質問に対処するために、すべてのデータにわたってテーマ分析を実施しました。 
We first used an inductive method to search for key themes from the interview topic guide (see Appendix A). 
最初に、インタビューのトピックガイド（付録Aを参照）から主要なテーマを探すために帰納的手法を使用しました。 
Table 3 shows the main themes identified. 
表3には、特定された主要なテーマが示されています。 
We then used a deductive method. 
次に、演繹的手法を使用しました。 
We read the data corpus again for grounded themes that emerged in the data. 
データに現れた基盤となるテーマを見つけるために、データコーパスを再度読みました。 
The final codebook is shown in Appendix B. 
最終的なコードブックは付録Bに示されています。 

[4https://www.microsoft.com/en-gb/microsoft-teams/group-chat-software](https://www.microsoft.com/en-gb/microsoft-teams/group-chat-software) 
[5https://otter.ai/](https://otter.ai/) 
[6https://help-nv.qsrinternational.com/20/win/Content/about-nvivo/about-nvivo.htm](https://help-nv.qsrinternational.com/20/win/Content/about-nvivo/about-nvivo.htm) 

Table 1. Description of hackathon topics with associated tools and methodologies. 
**表1. ハッカソンのトピックの説明と関連するツールおよび方法論。** 
Appendix C Table 7 includes descriptions and references for tools and methodologies included in this table. 
付録Cの表7には、この表に含まれるツールと方法論の説明と参照が含まれています。 

**Hackathon topic ハッカソンのトピック** **KE Tools/Methodologies KEツール/方法論** **LLM Tools/Methodologies LLMツール/方法論** 
Determine if LLMs can extract knowledge structures, including inference rules, to go with Triples investigation 知識構造を抽出できるかどうかを判断する、推論ルールを含む、トリプル調査に伴う ChatGPT, Few-shot prompt facts for KG construction 
Create a framework providing tools for collaborative human-AI ontology engineering 人間とAIの共同オントロジーエンジニアリングのためのツールを提供するフレームワークを作成 Competency Questions, eXtreme ChatGPT, Multiple prompting techniques 
Determine how KE tasks can be supported from LLMs KEタスクがLLMsからどのようにサポートされるかを判断する NeOn methodology, Competency Questions, HermiT Reasoner, OOPS PaLM, Llama, ChatGPT, Few-shot prompt 
Determine if LLMs perform reasoning tasks completely in natural language LLMが自然言語で完全に推論タスクを実行できるかどうかを判断する Triples investigation ChatGPT, Multiple prompting techniques 
Determine if LLMs can perform ontology alignment (i.e. identify and match entities between ontologies) LLMがオントロジーアライメントを実行できるかどうかを判断する（すなわち、オントロジー間のエンティティを特定し、マッチングする） OAEI ChatGPT, Zero-shot prompt 
Determine if multimodal LLMs can be used towards the construction of multimodal KGs マルチモーダルLLMがマルチモーダルKGの構築に使用できるかどうかを判断する Investigate triples mPLUG-Owl, InstructBLIP, Text only prompt (no text + image) 
Determine if we can perform ontology refinement (i.e. techniques for KG completion and correction) using LLMs LLMを使用してオントロジーの洗練（すなわち、KGの完成と修正のための技術）を実行できるかどうかを判断する OntoClean ChatGPT, Llama, Claud, Few-shot prompt 

Table 2. Number of documents and descriptions for each category of documents in the dataset. 
**表2. データセット内の各カテゴリの文書の数と説明。** 

**Selected method 選択された方法** **# documents 文書数** 
Ethnographic study エスノグラフィック研究 2 set of observation notes from two of the authors 2セットの観察ノート（2人の著者から） 
Hackathon reports ハッカソン報告書 7 reports from the Hackathon groups ハッカソングループからの7つの報告書 
Hackathon presentations ハッカソンプレゼンテーション 7 slide presentations from the Hackathon groups ハッカソングループからの7つのスライドプレゼンテーション 
Interviews インタビュー 14 semi-structured interviews with Hackathon participants ハッカソン参加者との14の半構造化インタビュー 

-----
8 Elisavet Koutsiana, Johanna Walker, Michelle Nwachukwu, Albert Meroño-Peñuela, and Elena Simperl 
Table 3. Themes identified through the inductive analysis. 
**表3. 帰納的分析を通じて特定されたテーマ。** 

**Themes テーマ** **Description 説明** 
Background experience 参加者のハッカソン前の経験 
Evaluation 評価の問題とLLM出力に対する提案 
Skills 参加者が持っている、またはLLMと対話するために習得する必要があるスキルと資質 
Challenges 参加者がKEタスクのためにLLMを使用する際に直面する課題 
Bias AI安全性テストに関する参加者の意見 
LLM interaction opinions LLMをKEタスクに使用することに関する参加者の意見 

This analysis was performed by two researchers, who first read the interview topic guide and together identified the key themes. 
この分析は2人の研究者によって行われ、彼らは最初にインタビューのトピックガイドを読み、一緒に主要なテーマを特定しました。 
Then they read the data corpus for the ground themes. 
次に、彼らは基盤となるテーマのためにデータコーパスを読みました。 
Following this, the two researchers, advised by another senior researcher, discussed and confirmed the codebook presented in Appendix B. 
その後、2人の研究者は、別の上級研究者の助言を受けて、付録Bに示されたコードブックについて議論し、確認しました。 

**3.3** **Ethics 倫理**

The ethnographic study was approved by Authors’ institution’s Ethical Advisory Committee via the Full Application Form. 
エスノグラフィック研究は、著者の所属機関の倫理諮問委員会によって、完全な申請書を通じて承認されました。 
Informed electronic (using Microsoft Forms[7] and storing in CSV) consent was given by the participants. 
参加者からは、情報に基づいた電子的（Microsoft Forms[7]を使用し、CSVに保存）同意が得られました。 
Thirty out of the 39 hackathon participants consented to the ethnographic study. 
39人のハッカソン参加者のうち30人がエスノグラフィック研究に同意しました。 
Participants who did not consent were not observed. 
同意しなかった参加者は観察されませんでした。 
No personal information was collected in the analysis. 
分析において個人情報は収集されませんでした。 
The documentary data were collected as an output of the hackathon. 
文書データはハッカソンの成果物として収集されました。 
The interview study was approved by Authors’ institution’s Ethical Advisory Committee via the Minimal Risk Procedure. 
インタビュー研究は、著者の所属機関の倫理諮問委員会によって、最小リスク手続きにより承認されました。 
Informed verbal (audio recordings and chat transcripts) consent was given by the participants. 
参加者からは、情報に基づいた口頭（音声録音とチャットのトランスクリプト）同意が得られました。 
No personal information was used in the analysis. 
分析において個人情報は使用されませんでした。 



## 4 RESULTS 結果

**4.1** **What are the main challenges experienced by knowledge engineers when using LLMs for knowledge engineering tasks?**
**知識エンジニアが知識工学タスクにLLMを使用する際に直面する主な課題は何ですか？**
Testing the use of LLMs for KE tasks was been challenging for all participants. 
KEタスクにLLMを使用することは、すべての参加者にとって困難でした。 
Our observations during the hackathon revealed that the main concerns were identifying appropriate dataset to use, prompting LLMs efficiently, and evaluating the LLM outputs. 
ハッカソン中の観察から、主な懸念は、使用する適切なデータセットの特定、LLMを効率的に促すこと、LLMの出力を評価することでした。 
We asked interviewees which of these they considered important. 
私たちはインタビュー対象者に、これらの中でどれが重要だと考えるかを尋ねました。 

**Dataset. Interviewees (1), (14), (12) emphasised the importance of datasets as a starting point, and groups used prompting as a means to create a dataset (Observer 1).**
**データセット。インタビュー対象者（1）、（14）、（12）は、データセットの重要性を出発点として強調し、グループはデータセットを作成する手段としてプロンプトを使用しました（オブザーバー1）。**
Without a dataset, they felt they could not continue with prompting and evaluation (14). 
データセットがなければ、彼らはプロンプトと評価を続けることができないと感じました（14）。 
“There are many codes online...to interact with language models that wasn’t any problem at all. 
「オンラインには多くのコードがあります...言語モデルと対話することは全く問題ではありませんでした。 
And the evaluation given that you know, you possess a ground truth,...was not too difficult. 
そして、あなたが知っているように、真実の基準を持っている場合の評価は...それほど難しくありませんでした。 
So, the most challenging case work for us was finding a dataset” (8). 
したがって、私たちにとって最も困難な作業はデータセットを見つけることでした」（8）。 
Finding a dataset was challenging for specific group tasks mainly because of the time pressure (14) and fast planning (1) needed to find and set domain knowledge for the task. 
特定のグループタスクにおいてデータセットを見つけることは、主に時間的プレッシャー（14）とタスクのためのドメイン知識を見つけて設定するために必要な迅速な計画（1）のために困難でした。 
On the other hand, an interviewee noted that LLMs should support establishing datasets. 
一方、インタビュー対象者は、LLMがデータセットの確立をサポートすべきだと指摘しました。 
“The dataset is not what concerns me because if anything, I’m pretty impressed with what large language models potentially could do in terms of extracting, like I was saying, concepts, relationships, maybe even constraints or parameters or universal restrictions or existential restrictions, from unstructured data” (13). 
「データセットは私が気にすることではありません。なぜなら、もし何かあれば、私は大規模言語モデルが非構造化データから概念、関係、場合によっては制約やパラメータ、普遍的制限、存在的制限を抽出する可能性に非常に感銘を受けているからです」（13）。 

|Themes|Description| 
|---|---| 
|Background experience|The participants’ experience prior to the hackathon| 
|Evaluation|Evaluation issues and suggestion for LLM outputs| 
|Skills|The skills and qualities participants have or need to gain to interact with LLMs| 
|Challenges|Challenges that participants face while using LLMs for KE tasks| 
|Bias|Participants opinions related to AI safety testing| 
|LLM interaction opinions|Participants opinion about the use of LLMs for KE tasks|  

-----

Knowledge Prompting: How Knowledge Engineers Use Large Language Models 9
**Prompting. An interviewee believed prompting is challenging due to some knowledge engineers’ lack of NLP training and experience, “I think prompting templates we’re going to be, generally more difficult for Semantic Web people, because we are not necessarily natural language processing people” (1).**
**プロンプト。インタビュー対象者は、プロンプトが一部の知識エンジニアのNLPトレーニングと経験の不足により困難であると考えました。「プロンプトテンプレートは、一般的にセマンティックウェブの人々にとってより難しいと思います。なぜなら、私たちは必ずしも自然言語処理の専門家ではないからです」（1）。**
This was also emphasised in the skills that a knowledge engineer needs to work efficiently with LLMs. 
これは、知識エンジニアがLLMと効率的に作業するために必要なスキルでも強調されました。 
Furthermore, many participants noted the time-consuming phase of iteratively testing prompts to receive desirable outcomes (3), (Observer 1). 
さらに、多くの参加者は、望ましい結果を得るためにプロンプトを反復的にテストする時間のかかる段階に言及しました（3）、（オブザーバー1）。 
Some suggested the usefulness of possible “templates for prompting” (Observer 1), (Observer 2), (3), (13). 
いくつかの参加者は、「プロンプト用のテンプレート」の有用性を提案しました（オブザーバー1）、（オブザーバー2）、（3）、（13）。 
In addition, “once we settled on a specific prompt, we said okay, it seems like it works good enough, the most tricky part of it was to make the language model consistent in its responses” (3). 
さらに、「特定のプロンプトに決まったら、うまく機能しているように見えると言いましたが、最も厄介な部分は、言語モデルの応答を一貫性のあるものにすることでした」（3）。 
This was particularly problematic when the process was automated with thousands of prompting iterations. 
これは、プロセスが数千回のプロンプト反復で自動化されたときに特に問題でした。 
Furthermore, syntactical errors also break the scripts and prevent automation (3). 
さらに、構文エラーもスクリプトを壊し、自動化を妨げます（3）。 
In contrast, an interviewee pointed out that prompting engineering is “less scientific” and models “with billions of parameters are not controllable,..., resulting in an output that you cannot reproduce one hour later, two days later. So, this might be a problem” (9). 
対照的に、インタビュー対象者は、プロンプトエンジニアリングは「科学的でない」と指摘し、モデルは「数十億のパラメータを持ち、制御できないため、1時間後、2日後に再現できない出力を生成します。したがって、これは問題かもしれません」（9）。 

**Evaluation. Participants believed that evaluation is challenging mostly due to the lack of benchmarks for specific KE activities, which depends on manual intervention, “so there are papers doing auto prompting...I’m a little biased towards evaluation simply because in my tasks evaluation pretty much boils down to a manual evaluation, there’s no other way to do it...it’s not that we have solved the dataset problem, but we can synthesise some datasets, or we can you know, create them artificially somehow. Evaluation still remains a challenge because. it has to be done manually” (5).**
**評価。参加者は、評価が特定のKE活動のベンチマークの欠如に主に起因して困難であると考えました。これは手動の介入に依存します。「自動プロンプトを行っている論文もあります...私は評価に対して少し偏見があります。なぜなら、私のタスクでは評価はほぼ手動評価に帰着するからです。他に方法はありません...データセットの問題を解決したわけではありませんが、いくつかのデータセットを合成することができますし、人工的に作成することもできます。評価は依然として手動で行う必要があるため、課題として残ります」（5）。**
In the case of using a specific controlled dataset for KG construction, the accuracy and coverage of the KG can be automatically evaluated (2), (10). 
KG構築のために特定の制御されたデータセットを使用する場合、KGの精度とカバレッジは自動的に評価できます（2）、（10）。 
However, in tasks such as designing competency questions or an ontology, there is not always a gold standard to compare with, and manual work from an expert is needed to evaluate the output. 
しかし、能力質問やオントロジーの設計などのタスクでは、常に比較するためのゴールドスタンダードがあるわけではなく、出力を評価するためには専門家の手動作業が必要です。 
Nevertheless, exploring the use of holistic LLM benchmarks such as HELM [8] was suggested (5). 
それでも、HELM [8]のような全体的なLLMベンチマークの使用を探ることが提案されました（5）。 

**4.2** **How do knowledge engineers evaluate LLMs’ output for their practices?**
**4.2** **知識エンジニアは自らの実践のためにLLMの出力をどのように評価しますか？**
We further asked interviewees whether current evaluation techniques for KE tasks could be used to evaluate LLM outputs. 
私たちはさらに、KEタスクのための現在の評価技術がLLMの出力を評価するために使用できるかどうかをインタビュー対象者に尋ねました。 
Most respondents believed that evaluation mainly depends on the task, but highlighted that current evaluation metrics are not sufficient for many KE activities. 
ほとんどの回答者は、評価は主にタスクに依存すると考えましたが、現在の評価指標が多くのKE活動には不十分であることを強調しました。 
Following this, we asked them what a new benchmark or metric would look like. 
その後、私たちは新しいベンチマークや指標がどのようなものになるかを尋ねました。 

**Current evaluation techniques. Some interviewees consider that for specific tasks, like using a controlled dataset (13),(14) and designing ontologies with simple taxonomies (12), evaluation metrics like F1 score, precision and recall (8), and comparison with gold standards are sufficient metrics for evaluation.**
**現在の評価技術。いくつかのインタビュー対象者は、特定のタスク、例えば制御されたデータセットを使用すること（13）、（14）や単純な分類法を用いたオントロジーの設計（12）において、F1スコア、精度、再現率（8）やゴールドスタンダードとの比較のような評価指標が評価に十分であると考えています。**
However, others felt that regarding KE task evaluation, “it’s not [only] a problem that concerns only interaction with large language models, it’s a broader problem that needs to be solved” (9). 
しかし、他の人々は、KEタスクの評価に関して「それは[単に]大規模言語モデルとの相互作用に関する問題ではなく、解決すべきより広い問題です」（9）と感じました。 
Many KE tasks, like ontology semantic and reasoning errors, require human evaluation (1), (5) because “there is no automatic way [to assess]...how well the ontology represents the domain knowledge” (11), and this is important because “if it’s mistaking...in relations which creates the hierarchy...[that] is much more important than making a mistake on some data.” (2) 
オントロジーの意味論や推論エラーのような多くのKEタスクは、人間の評価を必要とします（1）、（5）。なぜなら「オントロジーがドメイン知識をどれだけよく表現しているかを評価する自動的な方法はないからです」（11）。これは重要です。なぜなら「もしそれが関係において間違っている場合、それが階層を作成することは...データのいくつかの間違いを犯すことよりもはるかに重要です」（2）。 
In addition, others highlighted the need to evaluate the additional knowledge i.e., the extra knowledge produced by LLMs (10) and the knowledge is missing from KGs (4),(6),(14). 
さらに、他の人々は、追加の知識、つまりLLMによって生成された追加の知識（10）やKGから欠落している知識（4）、（6）、（14）を評価する必要性を強調しました。 
An interviewee (10) highlighted the extra knowledge produced by LLMs based on their training, for example, when we asked the LLMs to create triples from an expression like “X was born in Y”, we expected “X-is a-person”, “Y-is a-country”, and “X-birthplace-Y, but we also may get “Y-part of-European Union”. 
インタビュー対象者（10）は、LLMがトレーニングに基づいて生成する追加の知識を強調しました。例えば、「XはYで生まれた」という表現からトリプルを作成するようにLLMに依頼したとき、私たちは「X-is a-person」、「Y-is a-country」、「X-birthplace-Y」を期待しましたが、「Y-part of-European Union」を得ることもあります。 
These outputs include knowledge that may be needed to complete a KG, but it requires evaluation. 
これらの出力にはKGを完成させるために必要な知識が含まれていますが、評価が必要です。 
In addition, a way to evaluate the knowledge missed in the LLMs’ outputs is needed. 
さらに、LLMの出力で見逃された知識を評価する方法が必要です。 
An interviewee pointed out that, 
インタビュー対象者は次のように指摘しました。 
“by using these classical evaluation metrics...[we check] what is inside the [input] text and [we miss] what is not in the text” (4). 
「これらの古典的な評価指標を使用することによって...[私たちは] [入力] テキストの中に何があるかを確認し、[テキストにないもの]を見逃しています」（4）。 

Finally, interviewees emphasised the difficulty in processing LLMs output mainly because LLMs return “strings” (10) of text and we lack a way to evaluate the “generative text” (7). 
最後に、インタビュー対象者は、LLMが「文字列」（10）のテキストを返すため、LLMの出力を処理することの難しさを強調しました。また、「生成テキスト」を評価する方法が不足しています（7）。 
It is common in KE tasks to use a specific format like JSON or the expression of an ontology. 
KEタスクでは、JSONのような特定の形式やオントロジーの表現を使用することが一般的です。 
Even in the cases where participants asked the LLM to give output in these particular formats, they faced difficulties because, “the generated string contains inconsistencies, you really need to parse it and get what you want from the string itself, and then you need to convert it into a list, whatever you need” (10). 
参加者がLLMにこれらの特定の形式で出力を提供するように依頼した場合でも、「生成された文字列には不整合が含まれており、本当にそれを解析して、文字列自体から必要なものを取得し、それをリストに変換する必要があります」（10）。 
Complicating this is the fact that, LLM outputs are not all the same type (4), for example, a KG includes dates, values, images, URLs etc. 
これを複雑にするのは、LLMの出力がすべて同じタイプではないという事実です（4）。例えば、KGには日付、値、画像、URLなどが含まれます。 
It is not possible to have a united way to evaluate the different types. 
異なるタイプを評価するための統一された方法を持つことは不可能です。 
Furthermore, another factor in output evaluation is the similarity of the results (4). 
さらに、出力評価における別の要因は、結果の類似性です（4）。 
Current evaluation techniques work on a match, not similarity, meaning they do not manage variations well, and LLMs are prone to inconsistency. 
現在の評価技術は一致に基づいて機能し、類似性ではなく、つまり、変動をうまく管理できず、LLMは不整合に陥りやすいです。 

**New evaluation techniques. Most of the interviewees noted that current evaluation techniques are not sufficient and suggested possible alternatives.**
**新しい評価技術。ほとんどのインタビュー対象者は、現在の評価技術が不十分であると指摘し、可能な代替案を提案しました。**
Some focused on the ontology design (2), (5), suggesting the development of a set of ontologies to be used as gold standards (observer 1). 
いくつかはオントロジー設計（2）、（5）に焦点を当て、ゴールドスタンダードとして使用されるオントロジーのセットの開発を提案しました（オブザーバー1）。 
Others suggested the creation of toolkits (1) for LLMs to review ontology errors similar to existing ontology toolkits, like OntoClean [35] and Oops [79]. 
他の人々は、OntoClean [35]やOops [79]のような既存のオントロジーツールキットに類似したオントロジーエラーをレビューするためのLLM用ツールキットの作成を提案しました（1）。 
However, they acknowledged that this cannot be applied to large-scale KG like Wikidata, and manual work will still be required. 
しかし、彼らはこれがWikidataのような大規模KGには適用できず、手動作業が依然として必要であることを認めました。 
Humans could be more efficient in evaluation if they have the information which prompt is related to the results (Observer 1). 
人間は、どのプロンプトが結果に関連しているかの情報を持っていれば、評価においてより効率的である可能性があります（オブザーバー1）。 
Another suggestion was to test the consistency of data and semantics in a real scenario, “for a company using this data and querying this data, and the simplicity of querying this data, and also the performances of these knowledge graphs in queries per second. 
別の提案は、データと意味論の一貫性を実際のシナリオでテストすることでした。「このデータを使用し、このデータをクエリする会社のために、データをクエリする簡単さ、そしてクエリごとの知識グラフのパフォーマンスも含まれます。 
And also the errors and the consistency of the data that is created,...making sure that the semantics of the data stored in the knowledge graph is consistent and reliable” (9). 
作成されたデータのエラーと一貫性も含まれます...知識グラフに保存されたデータの意味論が一貫して信頼できることを確認することです」（9）。 

In addition, some interviewees were more specific, suggesting the use of techniques used in other fields, like fact checking (10), adversarial algorithms (13), and self-play from reinforcement learning (12). 
さらに、いくつかのインタビュー対象者は、ファクトチェック（10）、敵対的アルゴリズム（13）、強化学習からの自己対戦（12）など、他の分野で使用される技術の利用を提案しました。 
An interviewee suggested using fact-checking techniques to establish that the extra knowledge received is correct and can be used for the KG construction (10). 
インタビュー対象者は、受け取った追加の知識が正しいことを確認し、KG構築に使用できることを確立するためにファクトチェック技術を使用することを提案しました（10）。 
Another interviewee was fascinated by the concept of adversarial algorithms, a technique used to test machine learning by misguiding a model with malicious input. 
別のインタビュー対象者は、悪意のある入力でモデルを誤導することによって機械学習をテストするために使用される技術である敵対的アルゴリズムの概念に魅了されました。 
They suggested using this technique to test LLM results (13). 
彼らはこの技術を使用してLLMの結果をテストすることを提案しました（13）。 
In addition, another suggested the use of self-play technique, a reinforcement learning technique for improving agents’ performance by playing “against themselves". 
さらに、別の提案は、エージェントのパフォーマンスを向上させるために「自分自身と対戦する」自己対戦技術の使用でした。 



In addition, another suggested the use of self-play technique, a reinforcement learning technique for improving agents’ performance by playing “against themselves". 
さらに、別の提案者は、エージェントのパフォーマンスを「自分自身と対戦する」ことで向上させる強化学習技術である自己対戦技術の使用を提案しました。

They suggested to “let the model come up with, a whole host of answers, then compare them between each other [and]...get a more refined answer”, but this will require “more time and computing” (12).
彼らは「モデルに多くの回答を考えさせ、それらを互いに比較させて、より洗練された回答を得る」ことを提案しましたが、これは「より多くの時間と計算」を必要とするでしょう（12）。

Two interviewees (3), (6) commented that we should see LLMs as assistants making the processes in KE smoother and faster because, “we know that as humans, we are lazy to wrote down some stuff like the competency question, so, if [you have a suggestion of] competency question you decide [faster], actually, which one you want to use” (6) and the same can apply every step of the way.
2人のインタビュー対象者（3）、（6）は、LLMsをKEのプロセスをよりスムーズかつ迅速にするアシスタントとして見るべきだとコメントしました。なぜなら、「私たちは人間として、能力質問のようなものを書き留めるのが面倒だと知っているので、もし[能力質問の提案があれば]、実際にどれを使用するかを[より早く]決定できるからです」（6）。これはすべてのステップに当てはまります。

They suggested that evaluation should focus on human satisfaction, “so the language model should probably optimise not really the performances, but the satisfaction of the user at least dealing with that” (3).
彼らは、評価は人間の満足度に焦点を当てるべきだと提案しました。「したがって、言語モデルはおそらくパフォーマンスではなく、少なくともそれに関わるユーザーの満足度を最適化すべきです」（3）。

One interviewee suggested that a more “open-minded” approach is needed in order to advance the field of evaluation.
1人のインタビュー対象者は、評価の分野を進展させるためには、より「オープンマインドな」アプローチが必要だと提案しました。

If metrics are, “novel, it takes longer to review. If it’s a straightforward paper with a slight modification in the method and a new row, it’s easier to evaluate the merit of the work. 
もしメトリクスが「新しいものであれば、レビューに時間がかかります。方法にわずかな修正と新しい行がある単純な論文であれば、作品の価値を評価するのが容易です。

That’s not necessarily the way to go. So there’s a lot of work to be done in evaluation” (5).
それが必ずしも進むべき道ではありません。したがって、評価には多くの作業が必要です」（5）。

**4.3 What skills does a knowledge engineer need to incorporate LLMs into their practice?**
**4.3 LLMを実践に取り入れるために知識エンジニアが必要とするスキルは何ですか？**

**Skills possessed and of use. As it is all collaborative practices, communication within teams was pointed out as an important skill in multi-disciplinary groups such as those at the hackathon (4), (5).**
**持っているスキルと役立つスキル。すべてが協力的な実践であるため、ハッカソン（4）、（5）などの多分野グループにおいて、チーム内のコミュニケーションが重要なスキルとして指摘されました。**

To keep the project moving, the ability to explain and listen to ideas for an efficient workflow are required (4).
プロジェクトを進めるためには、効率的なワークフローのためにアイデアを説明し、聞く能力が必要です（4）。

One interviewee talked about the risk of getting lost in the implementation details, stating, “I kind of knew how to steer people in a direction that would eventually be useful for the final goals” (5).
1人のインタビュー対象者は、実装の詳細に迷うリスクについて話し、「最終的な目標に役立つ方向に人々を導く方法をなんとなく知っていました」と述べました（5）。

Having skill in building ontologies was found to be useful in adding context to the prompts (10), (6).
オントロジーを構築するスキルが、プロンプトにコンテキストを追加するのに役立つことがわかりました（10）、（6）。

For example, using the knowledge structure of a dataset, such as Wikidata (6), and information on how to form triples (10):
例えば、Wikidata（6）のようなデータセットの知識構造や、トリプルを形成する方法に関する情報を使用することです（10）：

“adding...context...as part of the prompt actually helped with the result” (6).
「プロンプトの一部としてコンテキストを追加することが、実際に結果に役立ちました」（6）。

In contrast, one interviewee found that the added context did not make a difference so despite having this skill, they did not consider it important (3).
対照的に、1人のインタビュー対象者は、追加されたコンテキストが違いを生まなかったため、このスキルを持っていても重要だとは考えませんでした（3）。

Building ontologies was also found to be useful in defining the overall goals for the task (5), (9):
オントロジーを構築することは、タスクの全体的な目標を定義するのにも役立つことがわかりました（5）、（9）：

“I could contextualise the tasks defined by the hackathon. 
「私はハッカソンで定義されたタスクを文脈化することができました。

And also, from a more practical point of view, I knew before starting coding, how the final output would have looked like” (9).
また、より実践的な観点から、コーディングを始める前に最終的な出力がどのように見えるかを知っていました」（9）。

Having prompting skills and understanding how prompts can be composed and revised to achieve a desired outcome was found to be important (10), (12), (8):
プロンプトスキルを持ち、プロンプトがどのように構成され、修正されて望ましい結果を達成できるかを理解することが重要であることがわかりました（10）、（12）、（8）：

“I think I have a good understanding of the prompt components. 
「私はプロンプトの構成要素をよく理解していると思います。

So, in a prompt, first you should assign a role, a persona to the language models, and then short task description is really useful.
したがって、プロンプトでは、まず言語モデルに役割やペルソナを割り当て、その後に短いタスクの説明が非常に役立ちます。

And these models shine when you give a few examples in context learning” (10).
そして、これらのモデルは、コンテキスト学習でいくつかの例を与えるときに輝きます」（10）。

In turn, these participants were able to streamline their approach and prompt more efficiently due to their understanding of the different components of prompts.
その結果、これらの参加者はプロンプトの異なる要素を理解することで、アプローチを合理化し、より効率的にプロンプトを作成できるようになりました。

Even just limited experience was found to be useful for forming prompts with one interviewee describing their skill as “not scientific” but found this helped in “understanding how these models respond to small changes” (12).
限られた経験でもプロンプトを形成するのに役立つことがわかり、1人のインタビュー対象者は自分のスキルを「科学的ではない」と表現しましたが、これが「これらのモデルが小さな変化にどのように反応するかを理解するのに役立った」と述べました（12）。

Interviewees acknowledged that rules are needed to prompt efficiently.
インタビュー対象者は、効率的にプロンプトを作成するためにはルールが必要であることを認めました。

There is a sweet spot in how much information is given to LLMs in order to get a desirable output, with too much information being as problematic as too little.
望ましい出力を得るためにLLMsに与える情報量には適切なバランスがあり、情報が多すぎることは少なすぎることと同様に問題です。

Coding was the main technical skill that many interviewees mentioned as being important (2), (3), (8), (9).
コーディングは、多くのインタビュー対象者が重要であると述べた主要な技術スキルでした（2）、（3）、（8）、（9）。

It was found to be useful in interacting with the LLM through the respective API (Application Programming Interface) and not the interface, which was important in querying large batches of prompts.
これは、各API（アプリケーションプログラミングインターフェース）を介してLLMと対話するのに役立ち、インターフェースではなく、大量のプロンプトをクエリする際に重要でした。

Along with this, knowledge in using repositories of models like Hugging Face[8] and Pytorch[9] was also noted as useful by an interviewee (2).
これに加えて、Hugging Face[8]やPytorch[9]のようなモデルのリポジトリを使用する知識も、1人のインタビュー対象者によって役立つと指摘されました（2）。

A useful skill was in version control systems like Git[10] to be able to clone, test and debug projects efficiently (2).
効率的にプロジェクトをクローン、テスト、デバッグできるようにするためのGit[10]のようなバージョン管理システムのスキルが役立ちました（2）。

Some interviewees also mentioned how their coding skill helped them with datasets, such as, scraping websites for datasets (3) and “[building] a dataset” (4).
一部のインタビュー対象者は、コーディングスキルがデータセットにどのように役立ったか、例えば、データセットのためにウェブサイトをスクレイピングすること（3）や「[データセットを]構築すること」（4）を挙げました。

Developing a scientific framework was found for one interviewee to help define the task’s workflow, describing it as “defining objective, defining hypotheses, defining an evaluation strategy, designing so an experiment” (7).
科学的なフレームワークを開発することが、1人のインタビュー対象者にとってタスクのワークフローを定義するのに役立つことがわかり、「目的を定義し、仮説を定義し、評価戦略を定義し、実験を設計する」と説明しました（7）。

**Skills gap. Many of the interviewees who lacked the skill in ontology design and engineering stated its importance (2), (12), (13) specifically for the evaluation of the outputs of the LLM (1), (7).**
**スキルギャップ。オントロジー設計とエンジニアリングのスキルが不足している多くのインタビュー対象者は、その重要性を述べました（2）、（12）、（13）。特にLLMの出力の評価において（1）、（7）。**

They felt that without this, it is difficult to know what a desired output would look like.
彼らは、これがなければ望ましい出力がどのようなものであるかを知るのが難しいと感じました。

For those who did not have prior prompting experience, there were two main distinctions on how they viewed this skill.
以前にプロンプトの経験がなかった人々にとって、このスキルをどのように見ているかには2つの主な違いがありました。

The first way was that some interviewees did not see prompting as a skill and felt that it was too simple of a task with multiple participants, restricting it to a trial-and-error exercise, not acknowledging the possibility to go beyond this.
最初の見方は、一部のインタビュー対象者がプロンプトをスキルとは見なさず、複数の参加者がいるためにあまりにも単純なタスクであると感じ、試行錯誤の演習に制限し、これを超える可能性を認めなかったことです。

They deemed prompting as requiring no expertise where KE and machine learning were categorised as more skillful (7), (13).
彼らは、KEや機械学習がよりスキルのあるものとして分類されるのに対し、プロンプトには専門知識が必要ないと見なしました（7）、（13）。

One interviewee who described themselves as being familiar with LLMs did not deem prompting as a specialist skill in the KE process as they believed any developer could do it (11).
LLMに精通していると自称する1人のインタビュー対象者は、プロンプトをKEプロセスにおける専門的なスキルとは見なさず、誰でも開発者ができると信じていました（11）。

On the other hand some interviewees were interested in gaining more experience to go beyond trial-and-error (4), (3), (1), (14).
一方で、一部のインタビュー対象者は、試行錯誤を超えるためにより多くの経験を得ることに興味を持っていました（4）、（3）、（1）、（14）。

One interviewee acknowledged that prompting can be an intricate process.
1人のインタビュー対象者は、プロンプトが複雑なプロセスであることを認めました。

Some interviewees felt that time for experimentation with large language models is important to build an understanding of prompting and this familiarity with LLMs can improve performance (5).
一部のインタビュー対象者は、大規模言語モデルでの実験のための時間がプロンプトの理解を深めるために重要であり、このLLMへの親しみがパフォーマンスを向上させる可能性があると感じました（5）。

This can also allow for quicker execution of prompting to streamline the workflow, one interviewee noting, “I’m pretty sure that a lot of tricks or tips that I don’t know about” (6).
これにより、ワークフローを合理化するためにプロンプトの実行を迅速化できる可能性があり、1人のインタビュー対象者は「私が知らない多くのトリックやヒントがあると確信しています」と述べました（6）。

Various technical skills were mentioned by several interviewees all of which were specific to running LLMs more efficiently.
さまざまな技術スキルが複数のインタビュー対象者によって言及され、すべてがLLMをより効率的に実行するために特化していました。

For example, one interviewee mentioned learning to use computer clusters to fine-tune LLMs (10), which needs experience and very high computational requirements.
例えば、1人のインタビュー対象者は、LLMを微調整するためにコンピュータクラスターを使用することを学んだと述べました（10）。これは経験と非常に高い計算要件を必要とします。

Another interviewee mentioned using LLaMA and Hugging Face for the use of APIs with different models as an important skill (12).
別のインタビュー対象者は、異なるモデルのAPIを使用するためにLLaMAとHugging Faceを使用することが重要なスキルであると述べました（12）。

There was also an interviewee who felt they needed an enhancement of their coding skills and hardware skills, such as using GPU (9).
また、コーディングスキルやハードウェアスキル、例えばGPUを使用するスキルの向上が必要だと感じているインタビュー対象者もいました（9）。

**4.4 How aware are knowledge engineers of bias as an LLM/KG safety issue?**
**4.4 知識エンジニアは、LLM/KGの安全性の問題としてのバイアスについてどれほど認識していますか？**

Our question on responsible AI was initially framed in terms of “safety”, offering the respondents the opportunity to engage with any aspect of AI safety they felt relevant.
私たちの責任あるAIに関する質問は、最初は「安全性」という観点から構成され、回答者が関連性を感じるAIの安全性の任意の側面に関与する機会を提供しました。

However, although two respondents raised data security (1) and insufficient data (13) as safety concerns, the majority were not clear on what concerns they might be considering.
しかし、2人の回答者がデータセキュリティ（1）や不十分なデータ（13）を安全性の懸念として挙げたものの、大多数は彼らが考慮している懸念が何であるか明確ではありませんでした。

In these cases, we suggested they focus on bias as most people are familiar with this concept.
このような場合、私たちは彼らにバイアスに焦点を当てるよう提案しました。ほとんどの人がこの概念に精通しているからです。

However, this familiarity may also breed contempt.
しかし、この親しみは軽視を生む可能性もあります。

The authors of this paper observed, “when asked about harms, they said it wasn’t discussed – assumes humans are biased anyway so there will be bias anyway, to me sounds like implying that there is no need to consider bias” (Observer 2).
この論文の著者は、「害について尋ねられたとき、彼らはそれが議論されていないと言った - 人間はどうせバイアスがあると仮定しているので、どうせバイアスがあるというのは、バイアスを考慮する必要がないことを暗示しているように聞こえます」と観察者2は述べました。

One respondent noted that they felt it would be “interesting and helpful” to apply safety testing to LLMs and so far had read papers on it (9).
1人の回答者は、LLMに安全性テストを適用することが「興味深く、役立つ」と感じており、これまでにそれに関する論文を読んでいると述べました（9）。

When asked to consider bias, interviewees made comments such as that they had only fleetingly interacted with the issues.
バイアスについて考慮するよう求められたとき、インタビュー対象者は、問題に一時的にしか関与していないといったコメントをしました。

“I’m familiar with the terms, but I haven’t worked on it directly” (10).
「私はその用語に精通していますが、直接取り組んだことはありません」（10）。

They described themselves as have experienced limited exposure (2), possessing a lack of knowledge (12) and interpreting safety as a risk to researchers rather than other publics (14).
彼らは、自分たちが限られた経験を持っている（2）、知識が不足している（12）、安全性を他の公衆ではなく研究者へのリスクとして解釈していると述べました（14）。

One respondent had previously worked as an engineer on a bias detection algorithm but felt this was purely a “theoretical thing”.
1人の回答者は、以前にバイアス検出アルゴリズムのエンジニアとして働いていましたが、これは純粋に「理論的なこと」だと感じていました。

One reason for this lack of engagement appeared to be the perception of safety was seen as a siloed activity rather than integrated with engineering: “that’s not my field” (4).
この関与の欠如の一因は、安全性がエンジニアリングと統合されるのではなく、孤立した活動として見られていることのようです。「それは私の分野ではありません」（4）。

This was not necessarily due to a lack of interest, but perhaps also to a lack of opportunity: that participants had been interested in safety work but “haven’t been able to get to it” (5).
これは必ずしも興味の欠如によるものではなく、機会の欠如によるものかもしれません。参加者は安全性の作業に興味を持っていましたが、「それに取り組むことができなかった」と述べました（5）。

The many variants of bias mean that this is a number of problems not one (6).
バイアスの多くの変種は、これは1つの問題ではなく、いくつかの問題であることを意味します（6）。

There was some awareness that understanding the type of bias is key to addressing it (4).
バイアスの種類を理解することがそれに対処するための鍵であるという認識がありました（4）。

In terms of specific types of bias, a few interviewees had awareness of what these might be, such as provenance (13), selectivity (5), and gender (6).
特定のバイアスの種類に関しては、いくつかのインタビュー対象者がそれらが何であるかを認識していました。例えば、出所（13）、選択性（5）、および性別（6）です。



. In terms of specific types of bias, a few interviewees had awareness of what these might be, such as provenance (13), selectivity (5), and gender (6). 
特定のバイアスの種類に関して、数人のインタビュー対象者は、出所（provenance）（13）、選択性（selectivity）（5）、および性別（gender）（6）など、これらが何であるかを認識していました。

These had also been brought up with one group in the hackathon, with the observer noting, “organiser [told the group] – make sure you don’t bias against gender, race, geographical concepts – If competency questions are biased then ontology is biased” (Observer 2). 
これらはハッカソンのあるグループでも取り上げられ、観察者は「主催者が[グループに]言った – 性別、人種、地理的概念に対してバイアスをかけないように – もし能力に関する質問がバイアスを持っているなら、オントロジーもバイアスを持っている」と指摘しました（Observer 2）。

It is difficult to tell, therefore, whether this knowledge was something the interviewees had applied to previous work, or gained in the relatively recent past of the hackathon. 
したがって、この知識がインタビュー対象者が以前の仕事に適用したものであるのか、ハッカソンの比較的最近の過去に得たものであるのかを判断するのは難しいです。

Correspondingly, there was variation in awareness of bias mitigation: “[I have] no idea how many safety checking solutions have already been provided” (1); “I have some doubts on how these testings are carried out” (9). 
それに応じて、バイアス緩和に対する認識にはばらつきがありました：「[私は]すでに提供されている安全チェックソリューションがいくつあるのか全くわからない」（1）; 「これらのテストがどのように実施されているのかについていくつかの疑問があります」（9）。

One interviewee felt that bias mitigation was more important in commercial products than in the lab (12). 
あるインタビュー対象者は、バイアス緩和が研究室よりも商業製品においてより重要であると感じていました（12）。

There was awareness that addressing bias may change relationships in a KG (4). 
バイアスに対処することがKG（知識グラフ）内の関係を変える可能性があることについての認識がありました（4）。

Particular issues related to LLMs were noted, for instance, ”there are so many confounding issues in the training of an LLM that even if you address bias in a prompt you can’t see the resources it is using to make a decision” (6). 
LLM（大規模言語モデル）に関連する特定の問題が指摘されました。たとえば、「LLMのトレーニングには多くの混乱する問題があるため、プロンプトでバイアスに対処しても、意思決定に使用しているリソースを見ることができません」（6）。

This respondent suggested that there could be ways to mitigate this by mapping the results of repeated prompting. 
この回答者は、繰り返しプロンプトを行った結果をマッピングすることで、これを緩和する方法があるかもしれないと提案しました。

One noted that harm can arise from use, even in a well-tested model. 
ある人は、十分にテストされたモデルであっても、使用から害が生じる可能性があると指摘しました。

“So even though [LLMs] pass [bias] tests, I think there’s still risk if you prompt them in a hateful or discriminative way” (10). 
「だから、[LLMs]が[バイアス]テストに合格しても、憎悪的または差別的な方法でプロンプトを与えると、リスクがあると思います」（10）。

One interviewee suggested that, given the difficulties of mitigating bias, we should at a minimum ”put an array [of] practices in place to monitor what’s coming out [and] how unbiased, how ethical, it is” (5). 
あるインタビュー対象者は、バイアスを緩和することの難しさを考慮して、少なくとも「出てくるものを監視するための一連の実践を整備し、どれだけバイアスがなく、どれだけ倫理的であるかを確認すべきだ」と提案しました（5）。

The idea of ’co-creating’ bias mitigation with users was suggested, with one interviewee suggesting not only reviewing the model for bias before use but also asking users for feedback on perceived bias as they used it (7) and another suggesting that, ”either we fix the data, or maybe we fix the tools somehow that [users] can detect this bias and root it out during their working” (5). 
ユーザーと共にバイアス緩和を「共創」するというアイデアが提案され、あるインタビュー対象者は、使用前にモデルのバイアスをレビューするだけでなく、使用中に認識されたバイアスについてユーザーにフィードバックを求めることを提案しました（7）。別のインタビュー対象者は、「データを修正するか、あるいは[ユーザー]がこのバイアスを検出し、作業中に根絶できるようにツールを修正するかのいずれかです」と提案しました（5）。

Respondents concerns about difficulties with addressing bias included a lack of knowledge of LLM training data and processes (13), a fear that tests for bias would be ineffective (9), and concern that tests alone are insufficient if appropriate action is not subsequently taken (10). 
バイアスに対処することの難しさに関する回答者の懸念には、LLMのトレーニングデータとプロセスに関する知識の欠如（13）、バイアステストが効果的でないのではないかという恐れ（9）、および適切な行動がその後に取られない場合、テストだけでは不十分であるという懸念（10）が含まれていました。

There was also concern about a lack of consensus around safety issues (13) and a feeling that other problems in the model (e.g. accuracy) may be more pressing (2). 
安全問題に関する合意の欠如（13）や、モデル内の他の問題（例：精度）がより差し迫ったものであるという感覚についても懸念がありました（2）。

Some interviewees felt there might be a tension between attempting to reduce bias and model efficacy (2), (12) 
一部のインタビュー対象者は、バイアスを減少させようとすることとモデルの有効性との間に緊張があるかもしれないと感じました（2）、（12）。

”There are evidences that if you debias a language model, it usually downgrades in performance” (8). 
「言語モデルのバイアスを取り除くと、通常はパフォーマンスが低下するという証拠があります」（8）。

Whereas most respondents felt bias was found in data, a few perceived bias might also lie in both the LLM (7) and KGs, specifically in the semantics (9). 
ほとんどの回答者はバイアスがデータに存在すると感じていましたが、一部はバイアスがLLM（7）やKG（知識グラフ）にも存在する可能性があると認識しており、特に意味論において（9）。

One respondent felt that safety was not a concern in KGs (14). 
ある回答者は、KGにおいて安全性は懸念事項ではないと感じていました（14）。

**4.5 What factors may affect knowledge engineers’ trust and uptake of the LLM technology?** 
**4.5 知識エンジニアのLLM技術に対する信頼と受け入れに影響を与える要因は何か？**

Interviewees have varied opinions on the use of LLMs to their practices. 
インタビュー対象者は、LLMの使用に関してさまざまな意見を持っています。

Some find their use promising, and others are more sceptic. 
一部はその使用を有望だと考え、他の人はより懐疑的です。

**Promising. Interviewees believe that LLMs cannot replace humans (3), but they can support KE activities. Using** 
**有望な点。インタビュー対象者は、LLMが人間を置き換えることはできない（3）が、KE活動をサポートできると信じています。使用することで**

LLMs we can reduce time spent on tasks (11), (hackathon report), improve communication between experts in different disciplines (hackathon report), perform tasks even without extended experience (12), for example, in ontology design, and incorporate NLP pipelines in our practices without the need to develop them from the beginning (7). 
LLMを使用することで、タスクにかかる時間を短縮でき（11）、異なる分野の専門家間のコミュニケーションを改善し（ハッカソン報告）、拡張経験がなくてもタスクを実行でき（12）、たとえばオントロジー設計において、最初から開発する必要なくNLPパイプラインを私たちの実践に組み込むことができます（7）。

However, “we need to use them carefully by providing human oversight, [or] human in the loop, or our pipelines need to add options [where] human can intervene... to avoid passing those errors produced by large language models to the downstream tasks” (1). 
しかし、「私たちは人間の監視を提供することによって、注意深く使用する必要があります。[または]人間をループに入れるか、私たちのパイプラインは[人間が介入できる]オプションを追加する必要があります...大規模言語モデルによって生成されたエラーを下流のタスクに渡さないようにするために」（1）。

In this vein, interviewees pointed out that LLMs could improve KE practices (9),(7), (13). 
この観点から、インタビュー対象者はLLMがKEの実践を改善できると指摘しました（9）、（7）、（13）。

However, their use is task-specific and interviewees raised concerns that effective prompting requires experience and there are reproducibility concerns (hackathon report). 
しかし、彼らの使用はタスク特有であり、インタビュー対象者は効果的なプロンプトには経験が必要であり、再現性の懸念があると指摘しました（ハッカソン報告）。

As well as assisting with processes, there was a suggestion for the incorporation of LLMs to improve existing KE tools (9) or to create new and advanced tools to support KE (13). 
プロセスを支援するだけでなく、既存のKEツールを改善するためにLLMを組み込むこと（9）や、KEをサポートするための新しい高度なツールを作成すること（13）が提案されました。

**Sceptic. Some interviewees were found to be more sceptical about the use of LLMs for KE tasks. They felt that LLMs** 
**懐疑的な点。一部のインタビュー対象者は、KEタスクにおけるLLMの使用についてより懐疑的であることがわかりました。彼らはLLMが**

by training are not up-to-date with the latest knowledge and that hallucination is very common (1). 
トレーニングによって最新の知識に追いついておらず、幻覚が非常に一般的であると感じていました（1）。

Moreover, LLMs respond with a prediction of what they think is the answer without giving information about how “confident” they are in the answer (13). 
さらに、LLMは自分が考える答えの予測で応答し、「どれだけ自信があるか」についての情報を提供しません（13）。

In reverse, trusted KGs already support AI with trusted knowledge and can also support LLMs (1). 
逆に、信頼できるKGはすでに信頼できる知識でAIをサポートしており、LLMもサポートできます（1）。

Other interviewees highlighted that LLMs cannot perform all KE activities (11), and the lack of evaluation techniques (6) lead some of the participants to find no value in their use. 
他のインタビュー対象者は、LLMがすべてのKE活動を実行できない（11）ことや、評価技術の欠如（6）が一部の参加者にLLMの使用に価値を見出させない原因となったことを強調しました。

An interviewee expressed, “ Yes, it can help you to quickly get some data just for testing purposes, for example. 
あるインタビュー対象者は、「はい、例えばテスト目的のためにデータを迅速に取得するのに役立ちます。

But for production, I don’t think that I will use it...since I never know which part of it is actually correct” (6). 
しかし、実際の運用では、私はそれを使用するとは思いません...なぜなら、実際にどの部分が正しいのか全くわからないからです」（6）。

During the hackathon, participants felt that LLMs can perform some tasks or simple examples, but in complex scenarios, the output cannot be controlled (i.e. evaluation). 
ハッカソン中、参加者はLLMがいくつかのタスクや単純な例を実行できると感じましたが、複雑なシナリオでは出力を制御できない（すなわち評価）と感じました。

An interviewee expressed that integrating KGs and LLMs was not required as LLMs would entirely replace KGs. 
あるインタビュー対象者は、LLMがKGを完全に置き換えるため、KGとLLMを統合する必要はないと表現しました。



## 5 DISCUSSION 議論

In this section we consider some of the key issues that arose from our results. 
このセクションでは、私たちの結果から生じた重要な問題のいくつかを考察します。 
The hackathon consisted of 7 explorations of how LLMS can be used to support KE. 
ハッカソンは、LLMSがKEをサポートする方法についての7つの探求から成り立っていました。 
Presenting the results of each of these explorations in detail is outside the scope of this paper, but there are some key overarching issues for their use that we present here. 
これらの探求の結果を詳細に示すことは本論文の範囲外ですが、ここではその使用に関するいくつかの重要な全体的な問題を提示します。 
We then explore in some detail issues around skills, in particular prompting and bias detection and mitigation. 
次に、スキルに関する問題、特にプロンプト作成とバイアスの検出および軽減について詳しく探ります。 
Finally, we highlight the importance of transparency and explainability in KGs and we introduce the concept of “KG cards”. 
最後に、KGにおける透明性と説明可能性の重要性を強調し、「KGカード」という概念を紹介します。 

**5.1** **Issues in using large language models for knowledge engineering** 
**5.1** **知識工学における大規模言語モデルの使用に関する問題**

A fundamental conflict occurs in the use of LLMs in KG work because of the ambiguity in the output of generative AIs. 
生成AIの出力の曖昧さのため、KG作業におけるLLMの使用には根本的な対立があります。 
This ambiguity lies mostly in the inherent irreproducibility of results garnered using generative AI. 
この曖昧さは、主に生成AIを使用して得られた結果の本質的な再現不可能性にあります。 
This means that contributions made by LLMs, such as the creation of relations or the similarity between terms, are based on statistical probability rather than consistent fact. 
これは、LLMによって行われる関係の作成や用語間の類似性などの貢献が、一貫した事実ではなく統計的確率に基づいていることを意味します。 
This lack of consistency is also problematic for scientific methods. 
この一貫性の欠如は、科学的方法にとっても問題です。 
This is consistent with previous studies arguing that knowledge extraction remains challenging despite the growing field of NLP [2, 73]. 
これは、NLPの成長する分野にもかかわらず、知識抽出が依然として困難であると主張する以前の研究と一致しています[2, 73]。 
However, one notable use of the LLMs for KE is to potentially create a structured dataset from a variety of unstructured data i.e. for data integration purposes. 
しかし、KEにおけるLLMの注目すべき使用法の1つは、さまざまな非構造化データから構造化データセットを作成する可能性があることです。つまり、データ統合の目的です。 
Other research [94] has found that given a prompt that includes the term “dataset”, in the absence of a dataset, ChatGPT may attempt to “curate” a dataset like an approximation from unstructured data. 
他の研究[94]では、「データセット」という用語を含むプロンプトが与えられた場合、データセットが存在しないときに、ChatGPTが非構造化データからの近似としてデータセットを「キュレーション」しようとする可能性があることがわかりました。 
Therefore, this application seems highly plausible for KE and, particularly, knowledge extraction in a structured format which is familiar to existing practices. 
したがって、このアプリケーションはKE、特に既存の慣行に馴染みのある構造化形式での知識抽出にとって非常に妥当であるようです。 
Following the usual actions of cleaning and transforming, the dataset can be used for KG construction. 
通常のクリーニングと変換の手順に従って、データセットはKG構築に使用できます。 
Yet, the accuracy of LLM results remains an issue. 
しかし、LLMの結果の正確性は依然として問題です。 

Following the knowledge extraction difficulties, another particular area of concern was evaluation. 
知識抽出の困難に続いて、もう1つの特に懸念される領域は評価でした。 
Attempting to evaluate LLM support for KE tasks would simply exacerbate existing evaluation challenges, which were many. 
KEタスクに対するLLMのサポートを評価しようとすることは、既存の評価課題を単に悪化させるだけです。 
These include evaluating accuracy (i.e., syntactic and semantic) and coherency (i.e. consistency and validity), emphasising that we may assess accuracy automatically, but most of the time, coherency requires manual interventions. 
これには、正確性（すなわち、構文的および意味的）や一貫性（すなわち、一貫性と妥当性）の評価が含まれます。正確性は自動的に評価できるかもしれませんが、ほとんどの場合、一貫性には手動の介入が必要です。 
Furthermore, concerns about coverage (i.e. completeness and representativeness) and succinctness (i.e. conciseness and understandability) are also relevant to input as well as output, and should be included as a consideration. 
さらに、カバレッジ（すなわち、完全性と代表性）や簡潔さ（すなわち、簡潔さと理解可能性）に関する懸念も、入力と出力の両方に関連しており、考慮に含めるべきです。 
This is a similar problem to that experienced in crowd-sourced KGs such as Wikidata [1], where variations in the input (such as background and skill of contributors) also demands evaluation as much as the output. 
これは、Wikidata [1]のようなクラウドソーシングされたKGで経験されるのと同様の問題であり、入力の変動（寄稿者の背景やスキルなど）も出力と同様に評価を要求します。 

Regarding the evaluation of LLM outputs, one interesting suggestion was made related to using adversarial algorithms. 
LLM出力の評価に関して、敵対的アルゴリズムを使用することに関連する興味深い提案がなされました。 
“Would something or a product like that stand the scrutiny of an adversarial network, who is trying to maybe test or break the new information derived by the existing system. 
「そのようなものや製品は、既存のシステムから得られた新しい情報をテストまたは破壊しようとする敵対的ネットワークの精査に耐えるでしょうか。 
So can there be a counter point counter punch that tries to break it, and if it cannot be broken or falsified?” 
それを破壊しようとする反論が存在するのでしょうか、そしてそれが破壊または偽造できない場合はどうでしょうか？」 
Recently, an adversarial attack on BARD [32] asking to repeat one iteratively one word eventually got the LLM to reveal gigabites of its training data, demonstrating the usefulness of such processes in testing systems [71]. 
最近、BARD [32]に対する敵対的攻撃が行われ、1つの単語を反復して繰り返すように求めた結果、LLMがトレーニングデータのギガバイトを明らかにすることになり、システムのテストにおけるそのようなプロセスの有用性を示しました[71]。 

Another proposed aspect of evaluation was human satisfaction. 
評価のもう1つの提案された側面は、人間の満足度でした。 
Other research has shown that the natural language element of LLMs, often read by humans as possessed of emotion, can make people feel that the process of using the LLM was successful even if the end result was not [94]. 
他の研究では、LLMの自然言語要素がしばしば人間に感情を持っていると読まれることが、人々にLLMの使用プロセスが成功したと感じさせることができることが示されていますが、最終結果がそうでない場合でも[94]。 
This could be potentially problematic for KE tasks, which requires logic over feelings. 
これは、感情よりも論理を必要とするKEタスクにとって潜在的に問題となる可能性があります。 
A comparable, well-researched situation is that of emotion in financial markets, which can move prices up or down based on public mood rather than underlying economic fundamentals. 
類似の、よく研究された状況は、金融市場における感情の状況であり、これは基礎的な経済的ファンダメンタルズではなく、公共の気分に基づいて価格を上下させることができます。 

**5.2** **Key skills - prompting** 
**5.2** **重要なスキル - プロンプト作成**

Prompting was a fascinating area of discussion. 
プロンプト作成は興味深い議論の領域でした。 
Although many interviewees spoke of how they found previous skills useful in developing effective prompts (and equally, that it was very possible to use ineffective prompts by accident), 
多くのインタビュー対象者は、効果的なプロンプトを開発する際に以前のスキルがどのように役立ったか（同様に、効果的でないプロンプトを誤って使用することが非常に可能であること）について話しましたが、 
some interviewees also felt that prompting skills were not important. 
一部のインタビュー対象者は、プロンプト作成スキルは重要ではないと感じていました。 
This conflict in opinions may be explained by the different tasks and the experience levels of interviewees in KE and in research. 
この意見の対立は、KEや研究におけるインタビュー対象者の異なるタスクや経験レベルによって説明できるかもしれません。 
However, ultimately, prompting was utilised for all the different KE tasks. 
しかし、最終的には、プロンプト作成はすべての異なるKEタスクに利用されました。 
This flags a new era and requirement for a new skill set in the field of KE. 
これは、KEの分野における新しいスキルセットの新しい時代と要件を示しています。 
This suggests that the creation of templates (using a method such as that suggested in [57]) for the KE tasks could benefit the field towards KG construction and fill in gaps in prompting skill level. 
これは、KEタスクのためのテンプレートの作成（[57]で提案された方法を使用するなど）がKG構築に向けて分野に利益をもたらし、プロンプト作成スキルレベルのギャップを埋める可能性があることを示唆しています。 
This has parallels in the introduction of crowd-sourcing to KG construction around a decade ago. 
これは、約10年前にKG構築にクラウドソーシングを導入したことに類似しています。 
Using crowdsourcing means for large-scale KG construction was a successful innovation supporting many intelligent applications today. 
大規模なKG構築のためにクラウドソーシング手段を使用することは、今日の多くのインテリジェントなアプリケーションをサポートする成功した革新でした。 
Additionally, incorporating a prompt engineer in the process, the “knowledge prompting engineer” could also bridge the skill gaps and enhance performance. 
さらに、プロセスにプロンプトエンジニアを組み込むことで、「知識プロンプトエンジニア」がスキルのギャップを埋め、パフォーマンスを向上させることができるでしょう。 

**5.3** **Key skills - bias** 
**5.3** **重要なスキル - バイアス**

There was a distinct lack of engagement with the processes of bias mitigation. 
バイアス軽減のプロセスへの関与が明らかに不足していました。 
This tended to arise from limited exposure to techniques or theories for identifying bias in the model. 
これは、モデル内のバイアスを特定するための技術や理論への限られた露出から生じる傾向がありました。 
While sometimes this was due to a lack of opportunity for KEs to do this, in other cases, it was because of a lack of interest. 
時には、これがKEにとってこれを行う機会の欠如によるものであった一方で、他の場合には、関心の欠如によるものでした。 
It is difficult to argue that the identification and eradication of bias should be left to a specific set of experts, rather than integrating core safety facets into the training of those responsible for building AI. 
バイアスの特定と排除は、AIを構築する責任のある人々のトレーニングにコアの安全面を統合するのではなく、特定の専門家に任せるべきだと主張するのは難しいです。 
Given the variety of safety and ethical aspects and potential harms in AI, it may be that space for “ethical deliberation” in the KG construction process is more valuable than simply providing, for instance, a list of biases for engineers to look out for [31]. 
AIにおけるさまざまな安全および倫理的側面と潜在的な危害を考慮すると、KG構築プロセスにおける「倫理的熟考」のためのスペースは、たとえばエンジニアが注意すべきバイアスのリストを提供することよりも価値があるかもしれません[31]。 

Our results illustrated a data-centric approach to bias in KGs, suggesting that the source of bias was more likely to be the data than the graph model itself. 
私たちの結果は、KGにおけるバイアスに対するデータ中心のアプローチを示し、バイアスの源はグラフモデル自体よりもデータである可能性が高いことを示唆しています。 
However, a few recognised that KG/Ontology/LLM is also important and the data may well be secondary. 
しかし、KG/オントロジー/LLMも重要であり、データは二次的である可能性があると認識している人もいました。 
Including LLMs in the construction of KGs may complicate these sources of bias further and require enhanced awareness [41]. 
KGの構築にLLMを含めることは、これらのバイアスの源をさらに複雑にし、意識の向上を必要とするかもしれません[41]。 

The integration of LLMs into the KE processes may additionally create further potential for harm, such as when, intentionally or unintentionally, the LLM can be manipulated to overcome privacy (as shown in the BARD example above [71]). 
LLMをKEプロセスに統合することは、意図的または非意図的に、LLMがプライバシーを克服するように操作される場合など、さらなる危害の可能性を生むかもしれません（上記のBARDの例に示されているように[71]）。 
This suggests an integrated review of the possible sources of harms introduced to KG when LLMs are utilised would be valuable. 
これは、LLMが利用される際にKGに導入される可能性のある危害の源を統合的にレビューすることが価値があることを示唆しています。 

**5.4** **KG cards to reduce harms** 
**5.4** **危害を減らすためのKGカード**

One way to implement this review of harms would be to develop KG data cards [65, 81], a set of detailed descriptions for transparency and explainability to ensure we produce and use trustworthy KGs. 
この危害のレビューを実施する1つの方法は、KGデータカード[65, 81]を開発することであり、信頼できるKGを生成し使用するための透明性と説明可能性のための詳細な説明のセットです。 
Considering the data cards model [81], a set of similar content themes could be used to guide researchers working on KG construction to supplement their datasets, in this case, KGs, with explanations related to provenance, coverage etc. 
データカードモデル[81]を考慮すると、同様のコンテンツテーマのセットを使用して、KG構築に取り組む研究者をガイドし、データセット、ここではKGに、出所、カバレッジなどに関連する説明を補足することができます。 
Given the lack of training in ethics and, therefore, the need for greater guidance in this area, KG cards can support extensive documentation and guide researchers in order to avoid common safety issues and mistakes. 
倫理に関するトレーニングの欠如と、それゆえにこの分野でのより大きなガイダンスの必要性を考慮すると、KGカードは広範な文書化をサポートし、一般的な安全問題や誤りを避けるために研究者をガイドすることができます。 

Data cards include a list of 31 content themes related to publishers, funding, licence, versions, features, sources, motivation, applications, limitations, cleaning, labelling, descriptive statistics, fairness, and term/domain definitions [81]. 
データカードには、出版社、資金、ライセンス、バージョン、機能、ソース、動機、アプリケーション、制限、クリーニング、ラベリング、記述統計、公平性、および用語/ドメイン定義に関連する31のコンテンツテーマのリストが含まれています[81]。 
Inspired by these themes in Figure 1, we suggest a list of “KG cards” with main themes provenance, construction, knowledge, completeness, safety and licensing. 
図1のこれらのテーマに触発されて、私たちは「KGカード」のリストを提案し、主要なテーマとして出所、構築、知識、完全性、安全性、ライセンスを挙げます。 
With provenance, we suggest tests similar to Holistic Evaluation of Language Models (HELM) [8] for language model transparency and data cards [81] descriptions for dataset explainability. 
出所に関しては、言語モデルの透明性のためのHolistic Evaluation of Language Models (HELM) [8]に類似したテストを提案し、データセットの説明可能性のためのデータカード[81]の説明を提案します。 
For construction, we propose details related to the structure of the graph for transparency in data processing, and for knowledge, we seek to describe the domain, the different languages, and the range of knowledge included (e.g. the list of UK prime ministers up to 2023). 
構築に関しては、データ処理の透明性のためのグラフの構造に関連する詳細を提案し、知識に関しては、ドメイン、異なる言語、および含まれる知識の範囲（例：2023年までの英国首相のリスト）を説明することを目指します。 
Heist et al. [37] presented an overview and comparison of publicly available KGs. 
Heistら[37]は、公開されているKGの概要と比較を示しました。 
Using his recommendations, for the completeness card, we suggest providing details similar to network analysis. 
彼の推奨を使用して、完全性カードのために、ネットワーク分析に類似した詳細を提供することを提案します。 
These are information about the number of nodes, relations, and average linkage, as well as about class hierarchy. 
これには、ノードの数、関係、平均リンク、およびクラス階層に関する情報が含まれます。 
This can offer an understanding for the KG coverage and potentially can support the next card about safety tests. 
これにより、KGのカバレッジを理解し、次の安全テストに関するカードをサポートする可能性があります。 

While data cards describe provenance in detail, there is a lack of focus on aspects of safety, particularly bias. 
データカードは出所を詳細に説明していますが、安全性、特にバイアスの側面に対する焦点が不足しています。 
“Fairness” as a concept is vague, culturally dependent and difficult to operationalise [23, 66]. 
「公平性」という概念は曖昧で、文化に依存し、実行可能にするのが難しいです[23, 66]。 
For KG cards, we suggest a set of safety checks related to data, the application of the KG, KG relations, fairness and explainability. 
KGカードに関しては、データ、KGの適用、KGの関係、公平性、および説明可能性に関連する一連の安全チェックを提案します。 
With this we aim to provide explanations and support for bias and ethics. 
これにより、バイアスと倫理に関する説明とサポートを提供することを目指します。 
Finally, licensing for the data used to build the graph and for the result graph can support its reuse. 
最後に、グラフを構築するために使用されるデータと結果グラフのライセンスは、その再利用をサポートできます。 



. With this we aim to provide explanations and support for bias and ethics.
これにより、私たちはバイアスと倫理に関する説明とサポートを提供することを目指しています。

Finally, licensing for the data used to build the graph and for the result graph can support its reuse.
最後に、グラフを構築するために使用されるデータと結果グラフのライセンスは、その再利用をサポートすることができます。

Fig. 1. Six suggested KG cards with related details.
図1. 関連する詳細を持つ6つの提案されたKGカード。

Using well-structured cards for transparency and explainability motivated others with the Hugging Face platform, inspired by model cards [65], to create a template called dataset cards for its shared datasets.[11]
透明性と説明可能性のために適切に構成されたカードを使用することは、Hugging Faceプラットフォームの他の人々に影響を与え、モデルカード[65]に触発されて、共有データセットのためのdataset cardsというテンプレートを作成させました。[11]

The attempts from essential platforms in the field of AI, like Hugging Face, to create frameworks for explainable datasets show the importance of data provenance and process in the AI era.
AI分野の重要なプラットフォーム、例えばHugging Faceが説明可能なデータセットのためのフレームワークを作成しようとする試みは、AI時代におけるデータの出所とプロセスの重要性を示しています。

Table 4 shows an alignment between Hugging Face’s dataset cards and our suggested KG cards.
表4は、Hugging Faceのデータセットカードと私たちの提案したKGカードとの整合性を示しています。

Most cards match different needs and directions depending on the product (i.r. dataset or KG); however, we suggest incorporating state-of-the-art metrics and emphasising the importance of ethical issues.
ほとんどのカードは、製品（すなわちデータセットまたはKG）に応じて異なるニーズと方向性に一致します。しかし、私たちは最先端の指標を取り入れ、倫理的問題の重要性を強調することを提案します。

In addition, Hugging Face has also adapted the set of model cards for transparency and detailed documentation of their models.[12]
さらに、Hugging Faceは、彼らのモデルの透明性と詳細な文書化のためにモデルカードのセットを適応させました。[12]

We suggest a similar tactic for the explainability of the KG embedding model in the KE field.
私たちは、KE分野におけるKG埋め込みモデルの説明可能性のために、同様の戦術を提案します。

The set of model cards [65] can be used to support documentation with a metadata template and enhance model transparency.
モデルカードのセット[65]は、メタデータテンプレートを使用して文書化をサポートし、モデルの透明性を高めるために使用できます。

Table 5 presents the list of model cards with descriptions and one example of the KG embedding model TransE.
表5は、説明とKG埋め込みモデルTransEの1つの例を含むモデルカードのリストを示しています。

TransE, which stands for Translating Embeddings for Modeling Multi-relational Data, is a state-of-the-art method for creating KG embeddings.
TransEは、複数関係データのモデリングのための埋め込みの翻訳を意味し、KG埋め込みを作成するための最先端の方法です。

Building upon the origin TransE model, more popular models have been created, like TransR (rotating) and TransF (folding) [18].
元のTransEモデルを基にして、TransR（回転）やTransF（折りたたみ）[18]のようなより人気のあるモデルが作成されました。

The TransE example in the table shows that KG embedding model studies offer detailed documentation for model training and evaluation, but the lack of demographic details and ethical considerations flag the need, similar to datasets, to adapt specialised instructions for model documentation in the field of KE.
表のTransEの例は、KG埋め込みモデルの研究がモデルのトレーニングと評価のための詳細な文書を提供していることを示していますが、人口統計の詳細や倫理的考慮が欠けているため、データセットと同様に、KE分野におけるモデル文書化のための専門的な指示を適応させる必要性が浮き彫りになっています。



## 6 CONCLUSION 結論

LLMs herald the emergence of a new era for many fields. 
LLMは多くの分野に新しい時代の到来を告げています。 
It is inevitable that they will change KE in many ways. 
彼らが知識工学（KE）を多くの方法で変えることは避けられません。 
In what direction this will lead us is not clear. 
これが私たちをどの方向に導くのかは明確ではありません。 
The hype around conversational generative AI is such that may one day render KGs obsolete. 
会話型生成AIに関する過剰な期待は、いつの日か知識グラフ（KG）を時代遅れにするかもしれません。 
Currently the volatility and unreliability of generative AI means that KGs will continue to be a trusted source, 
現在、生成AIの不安定性と信頼性の欠如により、KGは引き続き信頼できる情報源であり続けるでしょうが、 
although it is impossible to tell if this will still be true if LLMs become more reliable in the future. 
将来的にLLMがより信頼性を持つようになった場合、これが依然として真実であるかどうかは不明です。 
Today, however, the added efficiency in terms of addressing volume based tasks is of great potential for use alongside more traditional methods. 
しかし、今日では、ボリュームベースのタスクに対処するための効率の向上は、より伝統的な方法と併用するための大きな可能性を秘めています。 
In terms of adoption of new ways of creating KGs this recent development is somewhat analogous to the introduction of crowd sourcing to KE; 
KGを作成する新しい方法の採用に関して、この最近の発展はKEへのクラウドソーシングの導入にやや類似しています； 
an innovation that has subsequently proved of immense value. 
これは、その後、非常に大きな価値を持つことが証明された革新です。 
However, it is crucial that those working in the field are appropriately skilled and supported to work with LLMs in an effective, productive and safe fashion. 
しかし、この分野で働く人々が、LLMを効果的かつ生産的、安全に扱うために適切なスキルを持ち、サポートされることが重要です。 
As well as training, this implies the need for documentation to accompany LLM-assisted KGs such as prompt templates and KG cards. 
トレーニングに加えて、これはプロンプトテンプレートやKGカードなど、LLM支援のKGに付随する文書の必要性を示唆しています。 

**6.1** **Limitations 制限事項**

Participants were selected from European research labs that have a strong profile in either publishing in KE venues, 
参加者は、KEの場での出版に強いプロファイルを持つヨーロッパの研究所から選ばれました。 
or in offering well-used KE industry products. 
または、よく使用されるKE業界製品を提供している研究所からです。 
Given the number of participants not all KE tasks were investigated, 
参加者の数を考慮すると、すべてのKEタスクが調査されたわけではなく、 
the experiments were relatively small scale and groups worked for only three days on the tasks. 
実験は比較的小規模で、グループはタスクに対してわずか3日間しか作業しませんでした。 
Furthermore, most interviewees were different-level PhD students, 
さらに、ほとんどのインタビュー対象者は異なるレベルの博士課程の学生であり、 
missing the opinion of researchers with more than 10 years of experience in the field. 
この分野で10年以上の経験を持つ研究者の意見が欠けていました。 

**6.2** **Contributions and Future Work 貢献と今後の研究**

This is one of the first attempts to understand the interaction between knowledge engineers and LLMs. 
これは、知識エンジニアとLLMの相互作用を理解するための最初の試みの一つです。 
We have identified and presented key areas of strength and challenge for KE working with LLMs, 
私たちは、LLMを使用するKEの強みと課題の重要な領域を特定し、提示しました。 
and we have built on the suggestion of implementing data cards for KGs and propose extending these to more comprehensively address safety within KGs developed with LLMs. 
KGのためのデータカードを実装する提案に基づき、LLMで開発されたKG内の安全性をより包括的に扱うためにこれを拡張することを提案します。 
Future work may look at how LLMs can support less expert users in developing KGs, 
今後の研究では、LLMがどのように専門知識の少ないユーザーをKGの開発で支援できるかを検討するかもしれません。 
as this has been a key use of LLMs in other fields such as coding, report writing, etc. 
これは、コーディングやレポート作成などの他の分野でのLLMの重要な使用法であったからです。 
In particular, a more detailed study on practical methods for identifying and mitigating against bias in LLM-assisted KGs is required, 
特に、LLM支援のKGにおけるバイアスを特定し、軽減するための実用的な方法に関するより詳細な研究が必要です、 
across the entire development pipeline. 
開発パイプライン全体にわたって。 

**6.3** **Acknowledgements 謝辞**

This paper is produced as part of the MuseIT project which has been co-funded by the EU under the Grant Agreement number 101061441. 
この論文は、EUの助成契約番号101061441の下で共同資金提供されたMuseITプロジェクトの一部として作成されました。 
The authors would like to thank all the participants in the 2023 Knowledge Prompting Hackathon at King’s College London. 
著者は、ロンドンのキングスカレッジで開催された2023年のKnowledge Prompting Hackathonのすべての参加者に感謝の意を表します。 

**REFERENCES 参考文献**

[1] David Abián, F Guerra, J Martínez-Romanos, and Raquel Trillo-Lado. 2017. Wikidata and DBpedia: a comparative study. In Semanitic Keyword-based _Search on Structured Data Sources. Springer, 142–154._  
[2] Bradley P Allen, Lise Stork, and Paul Groth. 2023. Knowledge Engineering using Large Language Models. arXiv preprint arXiv:2310.00637 (2023).  
[3] Rohan Anil, Andrew M Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin, Alexandre Passos, Siamak Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng Chen, et al. 2023. Palm 2 technical report. arXiv preprint arXiv:2305.10403 (2023).  
[[4] Anthropic. 2024. Introducing Claude. https://www.anthropic.com/news/introducing-claude. Accessed: April 9, 2024.](https://www.anthropic.com/news/introducing-claude)  
[5] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2023. Prompting is programming: A query language for large language models. Proceedings _of the ACM on Programming Languages 7, PLDI (2023), 1946–1969._  
[6] Eva Blomqvist, Karl Hammar, and Valentina Presutti. 2016. Engineering Ontologies with Patterns-The eXtreme Design Methodology. Ontology _Engineering with Ontology Design Patterns 25 (2016), 23–50._  
[7] Kurt Bollacker, Colin Evans, Praveen Paritosh, Tim Sturge, and Jamie Taylor. 2008. Freebase: a collaboratively created graph database for structuring human knowledge. In Proceedings of the 2008 ACM SIGMOD international conference on Management of data. 1247–1250.  
[8] Rishi Bommasani, Percy Liang, and Tony Lee. 2023. Holistic Evaluation of Language Models. Annals of the New York Academy of Sciences (2023).  
[9] Piero A Bonatti, Aidan Hogan, Axel Polleres, and Luigi Sauro. 2011. Robust and scalable linked data reasoning incorporating provenance and trust annotations. Journal of Web Semantics 9, 2 (2011), 165–201.  
[10] Antoine Bordes, Xavier Glorot, Jason Weston, and Yoshua Bengio. 2014. A semantic matching energy function for learning with multi-relational data: Application to word-sense disambiguation. Machine learning 94 (2014), 233–259.  
[11] Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko. 2013. Translating embeddings for modeling multi-relational data. Advances in neural information processing systems 26 (2013).  
[12] Antoine Bordes, Jason Weston, Ronan Collobert, and Yoshua Bengio. 2011. Learning structured embeddings of knowledge bases. In Proceedings of _the AAAI conference on artificial intelligence, Vol. 25. 301–306._  
[13] Benjamin S Bucknall and Shiri Dori-Hacohen. 2022. Current and near-term AI as a potential existential risk factor. In Proceedings of the 2022 _AAAI/ACM Conference on AI, Ethics, and Society. 119–129._  
[14] Pere-Lluís Huguet Cabot and Roberto Navigli. 2021. REBEL: Relation extraction by end-to-end language generation. In Findings of the Association _for Computational Linguistics: EMNLP 2021. 2370–2381._  
[15] Zongsheng Cao, Qianqian Xu, Zhiyong Yang, Yuan He, Xiaochun Cao, and Qingming Huang. 2022. Otkge: Multi-modal knowledge graph embeddings via optimal transport. Advances in Neural Information Processing Systems 35 (2022), 39090–39102.  
[16] Yong Chen, Xinkai Ge, Shengli Yang, Linmei Hu, Jie Li, and Jinwen Zhang. 2023. A Survey on Multimodal Knowledge Graphs: Construction, Completion and Applications  



. 2023. A Survey on Multimodal Knowledge Graphs: Construction, Completion and Applications. Mathematics 11, 8 (2023), 1815.
2023年。マルチモーダル知識グラフに関する調査：構築、補完、及び応用。数学 11, 8 (2023), 1815。

[17] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale N Fung, and Steven Hoi. 2024.
[17] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale N Fung, および Steven Hoi. 2024年。

Instructblip: Towards general-purpose vision-language models with instruction tuning. Advances in Neural Information Processing Systems 36 (2024).
Instructblip: 指示調整を用いた汎用ビジョン・ランゲージモデルに向けて。神経情報処理システムの進展 36 (2024)。

[18] Yuanfei Dai, Shiping Wang, Neal N Xiong, and Wenzhong Guo. 2020. A survey on knowledge graph embedding: Approaches, applications and benchmarks. Electronics 9, 5 (2020), 750.
[18] Yuanfei Dai, Shiping Wang, Neal N Xiong, および Wenzhong Guo. 2020年。知識グラフ埋め込みに関する調査：アプローチ、応用、およびベンチマーク。エレクトロニクス 9, 5 (2020), 750。

[19] Fariz Darari, Werner Nutt, Giuseppe Pirrò, and Simon Razniewski. 2018. Completeness management for RDF data sources. ACM Transactions on _the Web (TWEB) 12, 3 (2018), 1–53._
[19] Fariz Darari, Werner Nutt, Giuseppe Pirrò, および Simon Razniewski. 2018年。RDFデータソースの完全性管理。ACM Transactions on _the Web (TWEB) 12, 3 (2018), 1–53。_

[20] Jacopo de Berardinis, Albert Meroño-Peñuela, Andrea Poltronieri, and Valentina Presutti. 2023. Choco: a chord corpus and a data transformation workflow for musical harmony knowledge graphs. Scientific Data 10, 1 (2023), 641.
[20] Jacopo de Berardinis, Albert Meroño-Peñuela, Andrea Poltronieri, および Valentina Presutti. 2023年。Choco：音楽的ハーモニー知識グラフのためのコードコーパスとデータ変換ワークフロー。科学データ 10, 1 (2023), 641。

[21] Gianluca Demartini. 2019. Implicit bias in crowdsourced knowledge graphs. In Companion Proceedings of The 2019 World Wide Web Conference. 624–630.
[21] Gianluca Demartini. 2019年。クラウドソーシングされた知識グラフにおける暗黙のバイアス。2019年ワールドワイドウェブ会議の補助論文集において。624–630。

[22] Ronald Denaux, Catherine Dolbear, Glen Hart, Vania Dimitrova, and Anthony G Cohn. 2011. Supporting domain experts to construct conceptual ontologies: A holistic approach. Journal of Web semantics 9, 2 (2011), 113–127.
[22] Ronald Denaux, Catherine Dolbear, Glen Hart, Vania Dimitrova, および Anthony G Cohn. 2011年。ドメイン専門家が概念オントロジーを構築するのを支援する：ホリスティックアプローチ。ウェブセマンティクスジャーナル 9, 2 (2011), 113–127。

[[23] Leigh Dodds. 2020. FAIR, fairer, fairest? https://blog.ldodds.com/2020/07/30/fair-fairer-fairest/](https://blog.ldodds.com/2020/07/30/fair-fairer-fairest/)
[[23] Leigh Dodds. 2020年。FAIR、より公正、最も公正？ https://blog.ldodds.com/2020/07/30/fair-fairer-fairest/](https://blog.ldodds.com/2020/07/30/fair-fairer-fairest/)

[[24] emerald publishing limited. 2023. Ethnography techniques. https://www.emeraldgrouppublishing.com/how-to/observation/use-ethnographic-](https://www.emeraldgrouppublishing.com/how-to/observation/use-ethnographic-methods-participant-observation,) [methods-participant-observation, Accessed on January, 2024.](https://www.emeraldgrouppublishing.com/how-to/observation/use-ethnographic-methods-participant-observation,)
[[24] エメラルド出版有限会社. 2023年。民族誌技術。https://www.emeraldgrouppublishing.com/how-to/observation/use-ethnographic-](https://www.emeraldgrouppublishing.com/how-to/observation/use-ethnographic-methods-participant-observation,) [methods-participant-observation、2024年1月にアクセス。](https://www.emeraldgrouppublishing.com/how-to/observation/use-ethnographic-methods-participant-observation,)

[25] Diego Esteves, Anisa Rula, Aniketh Janardhan Reddy, and Jens Lehmann. 2018. Toward veracity assessment in RDF knowledge bases: an exploratory analysis. Journal of Data and Information Quality (JDIQ) 9, 3 (2018), 1–26.
[25] Diego Esteves, Anisa Rula, Aniketh Janardhan Reddy, および Jens Lehmann. 2018年。RDF知識ベースにおける真実性評価に向けて：探索的分析。データと情報の質に関するジャーナル (JDIQ) 9, 3 (2018), 1–26。

Manuscript submitted to ACM  
原稿はACMに提出されました。

-----
20 Elisavet Koutsiana, Johanna Walker, Michelle Nwachukwu, Albert Meroño-Peñuela, and Elena Simperl
20 Elisavet Koutsiana, Johanna Walker, Michelle Nwachukwu, Albert Meroño-Peñuela, および Elena Simperl

[26] Jérôme Euzenat, Christian Meilicke, Heiner Stuckenschmidt, Pavel Shvaiko, and Cássia Trojahn. 2011. Ontology alignment evaluation initiative: six years of experience. Journal on data semantics XV (2011), 158–192.
[26] Jérôme Euzenat, Christian Meilicke, Heiner Stuckenschmidt, Pavel Shvaiko, および Cássia Trojahn. 2011年。オントロジー整合評価イニシアティブ：6年間の経験。データセマンティクスに関するジャーナル XV (2011), 158–192。

[27] Christiane Fellbaum. 2010. WordNet. In Theory and applications of ontology: computer applications. Springer, 231–243.
[27] Christiane Fellbaum. 2010年。WordNet。オントロジーの理論と応用：コンピュータアプリケーションにおいて。スプリンガー、231–243。

[28] Christian Fürber and Martin Hepp. 2011. Swiqa–a semantic web information quality assessment framework. (2011).
[28] Christian Fürber および Martin Hepp. 2011年。Swiqa–セマンティックウェブ情報品質評価フレームワーク。(2011)。

[29] Abbas Ghaddar, Philippe Langlais, Ahmad Rashid, and Mehdi Rezagholizadeh. 2021. Context-aware adversarial training for name regularity bias in named entity recognition. Transactions of the Association for Computational Linguistics 9 (2021), 586–604.
[29] Abbas Ghaddar, Philippe Langlais, Ahmad Rashid, および Mehdi Rezagholizadeh. 2021年。名前付きエンティティ認識における名前の規則性バイアスに対するコンテキスト対応の敵対的トレーニング。計算言語学協会の取引 9 (2021), 586–604。

[30] Birte Glimm, Ian Horrocks, Boris Motik, Giorgos Stoilos, and Zhe Wang. 2014. HermiT: an OWL 2 reasoner. Journal of automated reasoning 53 (2014), 245–269.
[30] Birte Glimm, Ian Horrocks, Boris Motik, Giorgos Stoilos, および Zhe Wang. 2014年。HermiT：OWL 2推論機。自動推論のジャーナル 53 (2014), 245–269。

[31] Jan Gogoll, Niina Zuber, Severin Kacianka, Timo Greger, Alexander Pretschner, and Julian Nida-Rümelin. 2021. Ethics in the software development process: from codes of conduct to ethical deliberation. Philosophy & Technology (2021), 1–24.
[31] Jan Gogoll, Niina Zuber, Severin Kacianka, Timo Greger, Alexander Pretschner, および Julian Nida-Rümelin. 2021年。ソフトウェア開発プロセスにおける倫理：行動規範から倫理的熟考へ。哲学と技術 (2021), 1–24。

[[32] Google. 2024. Bard main page. https://bard.google.com/chat Accessed on January, 2024.](https://bard.google.com/chat)
[[32] Google. 2024年。Bardメインページ。https://bard.google.com/chat 2024年1月にアクセス。](https://bard.google.com/chat)

[33] Paul Groth, Elena Simperl, Marieke van Erp, and Denny Vrandečić. 2023. Knowledge Graphs and their Role in the Knowledge Engineering of the 21st Century (Dagstuhl Seminar 22372). In Dagstuhl Reports, Vol. 12. Schloss Dagstuhl-Leibniz-Zentrum für Informatik.
[33] Paul Groth, Elena Simperl, Marieke van Erp, および Denny Vrandečić. 2023年。知識グラフと21世紀の知識工学におけるその役割（ダグシュタールセミナー22372）。ダグシュタールレポートにおいて、Vol. 12。シュロス・ダグシュタール-ライプニッツ情報学センター。

[34] Nicola Guarino and Christopher Welty. 2002. Evaluating ontological decisions with OntoClean. Commun. ACM 45, 2 (2002), 61–65.
[34] Nicola Guarino および Christopher Welty. 2002年。OntoCleanを用いたオントロジーの決定の評価。Commun. ACM 45, 2 (2002), 61–65。

[35] Nicola Guarino and Christopher A Welty. 2009. An overview of OntoClean. Handbook on ontologies (2009), 201–220.
[35] Nicola Guarino および Christopher A Welty. 2009年。OntoCleanの概要。オントロジーに関するハンドブック (2009), 201–220。

[[36] Qi He, Bee-Chung Chen, and Deepak Agarwal. [n. d.]. Building the LinkiedIn Knowledge Graph. https://engineering.linkedin.com/blog/2016/10/](https://engineering.linkedin.com/blog/2016/10/building-the-linkedin-knowledge-graph) [building-the-linkedin-knowledge-graph Accessed: November 2023.](https://engineering.linkedin.com/blog/2016/10/building-the-linkedin-knowledge-graph)
[[36] Qi He, Bee-Chung Chen, および Deepak Agarwal. [n. d.]. LinkedIn知識グラフの構築。https://engineering.linkedin.com/blog/2016/10/](https://engineering.linkedin.com/blog/2016/10/building-the-linkedin-knowledge-graph) [building-the-linkedin-knowledge-graph 2023年11月にアクセス。](https://engineering.linkedin.com/blog/2016/10/building-the-linkedin-knowledge-graph)

[37] Nicolas Heist, Sven Hertling, Daniel Ringler, and Heiko Paulheim. 2020. Knowledge Graphs on the Web-An Overview. Knowledge Graphs for _eXplainable Artificial Intelligence (2020), 3–22._
[37] Nicolas Heist, Sven Hertling, Daniel Ringler, および Heiko Paulheim. 2020年。ウェブ上の知識グラフ - 概要。_説明可能な人工知能のための知識グラフ (2020), 3–22。_

[38] Aidan Hogan, Eva Blomqvist, Michael Cochez, Claudia d’Amato, Gerard de Melo, Claudio Gutierrez, Sabrina Kirrane, José Emilio Labra Gayo, Roberto Navigli, Sebastian Neumaier, et al. 2022. Knowledge graphs. (2022).
[38] Aidan Hogan, Eva Blomqvist, Michael Cochez, Claudia d’Amato, Gerard de Melo, Claudio Gutierrez, Sabrina Kirrane, José Emilio Labra Gayo, Roberto Navigli, Sebastian Neumaier, らによる。2022年。知識グラフ。(2022)。

[39] Aidan Hogan, Jürgen Umbrich, Andreas Harth, Richard Cyganiak, Axel Polleres, and Stefan Decker. 2012. An empirical survey of linked data conformance. Journal of Web Semantics 14 (2012), 14–44.
[39] Aidan Hogan, Jürgen Umbrich, Andreas Harth, Richard Cyganiak, Axel Polleres, および Stefan Decker. 2012年。リンクデータの適合性に関する実証的調査。ウェブセマンティクスジャーナル 14 (2012), 14–44。

[40] Linmei Hu, Zeyi Liu, Ziwang Zhao, Lei Hou, Liqiang Nie, and Juanzi Li. 2023. A survey of knowledge enhanced pre-trained language models. IEEE _Transactions on Knowledge and Data Engineering (2023)._
[40] Linmei Hu, Zeyi Liu, Ziwang Zhao, Lei Hou, Liqiang Nie, および Juanzi Li. 2023年。知識強化された事前学習言語モデルに関する調査。IEEE _知識とデータ工学の取引 (2023)。_

[41] Dong Huang, Qingwen Bu, Jie Zhang, Xiaofei Xie, Junjie Chen, and Heming Cui. 2023. Bias assessment and mitigation in llm-based code generation. _arXiv preprint arXiv:2309.14345 (2023)._
[41] Dong Huang, Qingwen Bu, Jie Zhang, Xiaofei Xie, Junjie Chen, および Heming Cui. 2023年。LLMベースのコード生成におけるバイアス評価と軽減。_arXivプレプリント arXiv:2309.14345 (2023)。_

[42] Krzysztof Janowicz, Bo Yan, Blake Regalia, Rui Zhu, and Gengchen Mai. 2018. Debiasing Knowledge Graphs: Why Female Presidents are not like Female Popes.. In ISWC (P&D/Industry/BlueSky).
[42] Krzysztof Janowicz, Bo Yan, Blake Regalia, Rui Zhu, および Gengchen Mai. 2018年。知識グラフのデバイアス：なぜ女性の大統領は女性の教皇のようではないのか。ISWCにおいて (P&D/Industry/BlueSky)。

[43] Rodolphe Jenatton, Nicolas Roux, Antoine Bordes, and Guillaume R Obozinski. 2012. A latent factor model for highly multi-relational data. _Advances in neural information processing systems 25 (2012)._
[43] Rodolphe Jenatton, Nicolas Roux, Antoine Bordes, および Guillaume R Obozinski. 2012年。高度に多関係データのための潜在因子モデル。_神経情報処理システムの進展 25 (2012)。_

[44] Guoliang Ji, Kang Liu, Shizhu He, and Jun Zhao. 2016. Knowledge graph completion with adaptive sparse transfer matrix. In Proceedings of the _AAAI conference on artificial intelligence, Vol. 30._
[44] Guoliang Ji, Kang Liu, Shizhu He, および Jun Zhao. 2016年。適応的スパース転送行列を用いた知識グラフの補完。_人工知能に関するAAAI会議の議事録において、Vol. 30。_

[45] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of hallucination in natural language generation. Comput. Surveys 55, 12 (2023), 1–38.
[45] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, および Pascale Fung. 2023年。自然言語生成における幻覚に関する調査。コンピュータサーベイ 55, 12 (2023), 1–38。

[46] Zhanming Jie and Wei Lu. 2019. Dependency-Guided LSTM-CRF for Named Entity Recognition. In Proceedings of the 2019 Conference on Empirical _Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP). 3862–3872._
[46] Zhanming Jie および Wei Lu. 2019年。名前付きエンティティ認識のための依存ガイド付きLSTM-CRF。2019年の経験的自然言語処理に関する会議および第9回国際共同自然言語処理会議 (EMNLP-IJCNLP) の議事録において。3862–3872。_

[47] Tobias Käfer, Ahmed Abdelrahman, Jürgen Umbrich, Patrick O’Byrne, and Aidan Hogan. 2013. Observing linked data dynamics. In The Semantic _Web: Semantics and Big Data: 10th International Conference, ESWC 2013, Montpellier, France, May 26-30, 2013. Proceedings 10. Springer, 213–227._
[47] Tobias Käfer, Ahmed Abdelrahman, Jürgen Umbrich, Patrick O’Byrne, および Aidan Hogan. 2013年。リンクデータの動態を観察する。セマンティック _ウェブ：セマンティクスとビッグデータ：第10回国際会議、ESWC 2013、フランス・モンペリエ、2013年5月26-30日。議事録 10。スプリンガー、213–227。_

[48] Lucie-Aimée Kaffee, Alessandro Piscopo, Pavlos Vougiouklis, Elena Simperl, Leslie Carr, and Lydia Pintscher. 2017. A glimpse into Babel: an analysis of multilinguality in Wikidata. In Proceedings of the 13th International Symposium on Open Collaboration. 1–5.
[48] Lucie-Aimée Kaffee, Alessandro Piscopo, Pavlos Vougiouklis, Elena Simperl, Leslie Carr, および Lydia Pintscher. 2017年。バベルの一瞥：Wikidataにおける多言語性の分析。第13回国際オープンコラボレーションシンポジウムの議事録において。1–5。

[49] Nikhil Kandpal, Haikang Deng, Adam Roberts, Eric Wallace, and Colin Raffel. 2023. Large language models struggle to learn long-tail knowledge. In International Conference on Machine Learning. PMLR, 15696–15707.
[49] Nikhil Kandpal, Haikang Deng, Adam Roberts, Eric Wallace, および Colin Raffel. 2023年。大規模言語モデルはロングテール知識を学ぶのに苦労する。国際機械学習会議において。PMLR, 15696–15707。

[50] Emre Kazim and Adriano Soares Koshiyama. 2021. A high-level overview of AI ethics. Patterns 2, 9 (2021).
[50] Emre Kazim および Adriano Soares Koshiyama. 2021年。AI倫理の高レベルの概要。パターン 2, 9 (2021)。

[51] Daphna Keidar, Mian Zhong, Ce Zhang, Yash Raj Shrestha, and Bibek Paudel. 2021. Towards automatic bias detection in knowledge graphs. arXiv _preprint arXiv:2109.10697 (2021)._
[51] Daphna Keidar, Mian Zhong, Ce Zhang, Yash Raj Shrestha, および Bibek Paudel. 2021年。知識グラフにおける自動バイアス検出に向けて。arXiv _プレプリント arXiv:2109.10697 (2021)。_

[52] Arif Ali Khan, Sher Badshah, Peng Liang, Muhammad Waseem, Bilal Khan, Aakash Ahmad, Mahdi Fahmideh, Mahmood Niazi, and Muhammad Azeem Akbar. 2022. Ethics of AI: A systematic literature review of principles and challenges. In Proceedings of the 26th International Conference _on Evaluation and Assessment in Software Engineering. 383–392._
[52] Arif Ali Khan, Sher Badshah, Peng Liang, Muhammad Waseem, Bilal Khan, Aakash Ahmad, Mahdi Fahmideh, Mahmood Niazi, および Muhammad Azeem Akbar. 2022年。AIの倫理：原則と課題に関する体系的文献レビュー。第26回国際ソフトウェア工学評価と評価に関する会議の議事録において。383–392。_

[53] Konstantinos I Kotis, George A Vouros, and Dimitris Spiliotopoulos. 2020. Ontology engineering methodologies for the evolution of living and reused ontologies: status, trends, findings and recommendations. The Knowledge Engineering Review 35 (2020).
[53] Konstantinos I Kotis, George A Vouros, および Dimitris Spiliotopoulos. 2020年。生きたオントロジーと再利用されたオントロジーの進化のためのオントロジー工学の方法論：状況、傾向、発見、および推奨。知識工学レビュー 35 (2020)。

[54] Angelie Kraft and Ricardo Usbeck. 2022. The Lifecycle of" Facts": A Survey of Social Bias in Knowledge Graphs. arXiv preprint arXiv:2210.03353 (2022).
[54] Angelie Kraft および Ricardo Usbeck. 2022年。「事実」のライフサイクル：知識グラフにおける社会的バイアスの調査。arXivプレプリント arXiv:2210.03353 (2022)。

[55] Abhijeet Kumar, Abhishek Pandey, Rohit Gadia, and Mridul Mishra. 2020. Building knowledge graph using pre-trained language model for learning entity-aware relationships. In 2020 IEEE International Conference on Computing, Power and Communication Technologies (GUCON). IEEE, 310–315.
[55] Abhijeet Kumar, Abhishek Pandey, Rohit Gadia, および Mridul Mishra. 2020年。エンティティ認識関係を学ぶための事前学習言語モデルを使用した知識グラフの構築。2020年IEEE国際会議における計算、電力、通信技術 (GUCON)。IEEE, 310–315。

Manuscript submitted to ACM  
原稿はACMに提出されました。

-----
Knowledge Prompting: How Knowledge Engineers Use Large Language Models 21
知識プロンプティング：知識エンジニアが大規模言語モデルをどのように使用するか 21

[56] Heather Lent and Anders Søgaard. 2021. Common sense bias in semantic role labeling. In Proceedings of the seventh workshop on noisy user-generated _text (w-nut 2021). 114–119._
[56] Heather Lent および Anders Søgaard. 2021年。セマンティックロールラベリングにおける常識バイアス。第7回ノイジーなユーザー生成テキストに関するワークショップの議事録において (w-nut 2021)。114–119。_

[57] Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi, and Graham Neubig. 2023. Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing. Comput. Surveys 55, 9 (2023), 1–35.
[57] Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi, および Graham Neubig. 2023年。事前学習、プロンプト、予測：自然言語処理におけるプロンプト手法の体系的調査。コンピュータサーベイ 55, 9 (2023), 1–35。

[58] Yifan Liu, Bin Shang, Chenxin Wang, and Yinliang Zhao. 2023. Knowledge Graph Completion with Information Adaptation and Refinement. In _International Conference on Advanced Data Mining and Applications. Springer, 16–31._
[58] Yifan Liu, Bin Shang, Chenxin Wang, および Yinliang Zhao. 2023年。情報適応と洗練を用いた知識グラフの補完。_先進データマイニングと応用に関する国際会議において。スプリンガー、16–31。_

[59] Jose L Martinez-Rodriguez, Aidan Hogan, and Ivan Lopez-Arevalo. 2020. Information extraction meets the semantic web: a survey. Semantic Web 11, 2 (2020), 255–335.
[59] Jose L Martinez-Rodriguez, Aidan Hogan, および Ivan Lopez-Arevalo. 2020年。情報抽出とセマンティックウェブの出会い：調査。セマンティックウェブ 11, 2 (2020), 255–335。

[60] Diana Maynard, Kalina Bontcheva, and Isabelle Augenstein. 2017. Natural language processing for the semantic web. Springer.
[60] Diana Maynard, Kalina Bontcheva, および Isabelle Augenstein. 2017年。セマンティックウェブのための自然言語処理。スプリンガー。

[61] Karen L McGraw and Karen Harbison-Briggs. 1989. Knowledge acquisition: Principles and guidelines. Prentice-Hall, Inc.
[61] Karen L McGraw および Karen Harbison-Briggs. 1989年。知識獲得：原則とガイドライン。プレンティスホール社。

[62] Patrick Mikalef, Kieran Conboy, Jenny Eriksson Lundström, and Aleš Popovič. 2022
[62] Patrick Mikalef, Kieran Conboy, Jenny Eriksson Lundström, および Aleš Popovič. 2022年。



. 1989. Knowledge acquisition: Principles and guidelines. Prentice-Hall, Inc.
1989年。知識獲得：原則とガイドライン。プレンティスホール社。

[62] Patrick Mikalef, Kieran Conboy, Jenny Eriksson Lundström, and Aleš Popovič. 2022. Thinking responsibly about responsible AI and ‘the dark side’of AI., 257–268 pages.
[62] パトリック・ミカレフ、キアラン・コンボイ、ジェニー・エリクソン・ルンドストローム、アレシュ・ポポビッチ。2022年。責任あるAIとAIの「ダークサイド」について責任を持って考える。257–268ページ。

[63] Bonan Min, Hayley Ross, Elior Sulem, Amir Pouran Ben Veyseh, Thien Huu Nguyen, Oscar Sainz, Eneko Agirre, Ilana Heintz, and Dan Roth. 2023.
Recent advances in natural language processing via large pre-trained language models: A survey. Comput. Surveys 56, 2 (2023), 1–40.
[63] ボナン・ミン、ヘイリー・ロス、エリオール・スレム、アミール・プーラン・ベン・ヴェイセ、ティエン・フー・グエン、オスカー・サインズ、エネコ・アギレ、イラナ・ハインツ、ダン・ロス。2023年。
大規模事前学習言語モデルを用いた自然言語処理の最近の進展：調査。コンピュータサーベイ 56, 2 (2023), 1–40。

[64] Shubhanshu Mishra, Sijun He, and Luca Belli. 2020. Assessing demographic bias in named entity recognition. arXiv preprint arXiv:2008.03415 (2020).
[64] シュバンシュ・ミシュラ、シジュン・ハ、ルカ・ベッリ。2020年。名前付きエンティティ認識における人口統計的バイアスの評価。arXivプレプリント arXiv:2008.03415 (2020)。

[65] Margaret Mitchell, Simone Wu, Andrew Zaldivar, Parker Barnes, Lucy Vasserman, Ben Hutchinson, Elena Spitzer, Inioluwa Deborah Raji, and Timnit Gebru. 2019. Model cards for model reporting. In Proceedings of the conference on fairness, accountability, and transparency. 220–229.
[65] マーガレット・ミッチェル、シモーヌ・ウー、アンドリュー・ザルディバル、パーカー・バーンズ、ルーシー・ヴァッサーマン、ベン・ハッチンソン、エレナ・スピッツァー、イニオルワ・デボラ・ラジ、ティムニット・ゲブル。2019年。モデル報告のためのモデルカード。公正性、説明責任、透明性に関する会議の議事録において。220–229。

[66] Luke Munn. 2023. The uselessness of AI ethics. AI and Ethics 3, 3 (2023), 869–877.
[66] ルーク・マン。2023年。AI倫理の無用性。AIと倫理 3, 3 (2023), 869–877。

[[67] MuseIT. 2023. Multisensory, User-centred, Shared cultural Experiences through Interactive Technologies. https://www.muse-it.eu/post/look-](https://www.muse-it.eu/post/look-back-at-haptics-for-inclusion-symposium,) [back-at-haptics-for-inclusion-symposium, Accessed on January, 2024.](https://www.muse-it.eu/post/look-back-at-haptics-for-inclusion-symposium,)
[[67] MuseIT. 2023年。インタラクティブ技術を通じた多感覚のユーザー中心の共有文化体験。https://www.muse-it.eu/post/look-](https://www.muse-it.eu/post/look-back-at-haptics-for-inclusion-symposium,) [haptics-for-inclusion-symposiumを振り返る、2024年1月にアクセス。](https://www.muse-it.eu/post/look-back-at-haptics-for-inclusion-symposium,)

[68] Peter P Mykytyn Jr, Kathleen Mykytyn, and MK Raja. 1994. Knowledge acquisition skills and traits: a self-assessment of knowledge engineers.
_Information & Management 26, 2 (1994), 95–104._
[68] ピーター・P・ミキティン・ジュニア、キャスリーン・ミキティン、MK・ラジャ。1994年。知識獲得スキルと特性：知識エンジニアの自己評価。
_情報と管理 26, 2 (1994), 95–104。_

[69] Moin Nadeem, Anna Bethke, and Siva Reddy. 2021. StereoSet: Measuring stereotypical bias in pretrained language models. In Proceedings of the _59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing_ _(Volume 1: Long Papers). 5356–5371._
[69] モイン・ナディーム、アンナ・ベスケ、シバ・レディ。2021年。StereoSet：事前学習言語モデルにおけるステレオタイプバイアスの測定。_計算言語学会第59回年次総会および第11回国際共同自然言語処理会議_の議事録において_(ボリューム1：長論文)。5356–5371。

[70] Guoshun Nan, Jiaqi Zeng, Rui Qiao, Zhijiang Guo, and Wei Lu. 2021. Uncovering Main Causalities for Long-tailed Information Extraction. In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing. 9683–9695._
[70] グオシュン・ナン、ジャーキ・ゼン、ルイ・チャオ、ジージアン・グオ、ウェイ・ルー。2021年。ロングテール情報抽出の主要因果関係を明らかにする。_2021年自然言語処理における経験的手法に関する会議の議事録において。9683–9695。

[71] Milad Nasr, Nicholas Carlini, Jonathan Hayase, Matthew Jagielski, A Feder Cooper, Daphne Ippolito, Christopher A Choquette-Choo, Eric Wallace, Florian Tramèr, and Katherine Lee. 2023. Scalable extraction of training data from (production) language models. arXiv preprint arXiv:2311.17035 (2023).
[71] ミラド・ナスル、ニコラス・カーニ、ジョナサン・ハヤセ、マシュー・ジャギエルスキー、A・フェダー・クーパー、ダフネ・イッポリト、クリストファー・A・ショケット・チュー、エリック・ウォレス、フローリアン・トラメール、キャサリン・リー。2023年。(生産)言語モデルからのトレーニングデータのスケーラブルな抽出。arXivプレプリント arXiv:2311.17035 (2023)。

[72] Maximilian Nickel, Volker Tresp, Hans-Peter Kriegel, et al. 2011. A three-way model for collective learning on multi-relational data.. In Icml, Vol. 11. 3104482–3104584.
[72] マキシミリアン・ニッケル、フォルカー・トレスプ、ハンス・ペーター・クリーゲル、他。2011年。多関係データにおける集合学習のための三者モデル。Icmlにおいて、ボリューム11。3104482–3104584。

[73] Natasha Noy, Yuqing Gao, Anshu Jain, Anant Narayanan, Alan Patterson, and Jamie Taylor. 2019. Industry-scale Knowledge Graphs: Lessons and Challenges: Five diverse technology companies show how it’s done. Queue 17, 2 (2019), 48–75.
[73] ナターシャ・ノイ、ユーチン・ガオ、アンシュ・ジャイン、アナント・ナラヤナン、アラン・パターソン、ジェイミー・テイラー。2019年。業界規模の知識グラフ：教訓と課題：5つの多様なテクノロジー企業がその方法を示す。キュー 17, 2 (2019), 48–75。

[74] Natalya F Noy, Deborah L McGuinness, et al. 2001. Ontology development 101: A guide to creating your first ontology.
[74] ナタリヤ・F・ノイ、デボラ・L・マクギネス、他。2001年。オントロジー開発101：最初のオントロジーを作成するためのガイド。

[75] Eirini Ntoutsi, Pavlos Fafalios, Ujwal Gadiraju, Vasileios Iosifidis, Wolfgang Nejdl, Maria-Esther Vidal, Salvatore Ruggieri, Franco Turini, Symeon Papadopoulos, Emmanouil Krasanakis, et al. 2020. Bias in data-driven artificial intelligence systems—An introductory survey. Wiley Interdisciplinary _Reviews: Data Mining and Knowledge Discovery 10, 3 (2020), e1356._
[75] エイリニ・ントゥーツィ、パブロス・ファファリオス、ウジュワル・ガディラジュ、ヴァシレイオス・イオシフィディス、ヴォルフガング・ネイジル、マリア・エステル・ビダル、サルバトーレ・ルッジェーリ、フランコ・トゥリーニ、シメオン・パパドプロス、エマノイラ・クラサナキス、他。2020年。データ駆動型人工知能システムにおけるバイアス—入門調査。ワイリー学際的_レビュー：データマイニングと知識発見 10, 3 (2020), e1356。

[[76] OpenAI. 2024. ChatGPT. https://openai.com/chatgpt Accessed: April 9, 2024.](https://openai.com/chatgpt)
[[76] OpenAI. 2024年。ChatGPT。https://openai.com/chatgpt アクセス日：2024年4月9日。](https://openai.com/chatgpt)

[77] Evangelos Paparidis and Konstantinos Kotis. 2021. Towards engineering fair ontologies: Unbiasing a surveillance ontology. In 2021 IEEE International _Conference on Progress in Informatics and Computing (PIC). IEEE, 226–231._
[77] エヴァンゲロス・パパリディス、コンスタンティノス・コティス。2021年。公正なオントロジーの工学に向けて：監視オントロジーのバイアスを取り除く。2021年IEEE国際_情報学と計算の進展に関する会議(PIC)において。IEEE、226–231。

[78] Ciyuan Peng, Feng Xia, Mehdi Naseriparsa, and Francesco Osborne. 2023. Knowledge graphs: Opportunities and challenges. Artificial Intelligence _Review (2023), 1–32._
[78] シーユアン・ペン、フェン・シャ、メフディ・ナセリパルサ、フランチェスコ・オズボーン。2023年。知識グラフ：機会と課題。人工知能_レビュー (2023), 1–32。

[79] María Poveda-Villalón, Asunción Gómez-Pérez, and Mari Carmen Suárez-Figueroa. 2014. Oops!(ontology pitfall scanner!): An on-line tool for ontology evaluation. International Journal on Semantic Web and Information Systems (IJSWIS) 10, 2 (2014), 7–34.
[79] マリア・ポベダ・ビジャロン、アスンシオン・ゴメス・ペレス、マリ・カルメン・スアレス・フィゲロア。2014年。Oops!(オントロジー落とし穴スキャナー！)：オントロジー評価のためのオンラインツール。国際セマンティックウェブと情報システムジャーナル (IJSWIS) 10, 2 (2014), 7–34。

[80] María Poveda-Villalón, Mari Carmen Suárez-Figueroa, and Asunción Gómez-Pérez. 2012. Validating ontologies with oops!. In Knowledge Engineering _and Knowledge Management: 18th International Conference, EKAW 2012, Galway City, Ireland, October 8-12, 2012. Proceedings 18. Springer, 267–281._
[80] マリア・ポベダ・ビジャロン、マリ・カルメン・スアレス・フィゲロア、アスンシオン・ゴメス・ペレス。2012年。Oops!を用いたオントロジーの検証。知識工学_と知識管理：第18回国際会議、EKAW 2012、アイルランド・ゴールウェイ市、2012年10月8-12日。議事録18。スプリンガー、267–281。

[81] Mahima Pushkarna, Andrew Zaldivar, and Oddur Kjartansson. 2022. Data cards: Purposeful and transparent dataset documentation for responsible ai. In Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency. 1776–1826.
[81] マヒマ・プシュカルナ、アンドリュー・ザルディバル、オッダル・キヤルタンス。2022年。データカード：責任あるAIのための目的を持った透明なデータセット文書。2022年ACM公正性、説明責任、透明性に関する会議の議事録において。1776–1826。

[82] Ben Shneiderman. 2020. Human-centered artificial intelligence: Reliable, safe & trustworthy. International Journal of Human–Computer Interaction 36, 6 (2020), 495–504.
[82] ベン・シュナイダーマン。2020年。人間中心の人工知能：信頼性、安全性、信頼性。国際人間–コンピュータ相互作用ジャーナル 36, 6 (2020), 495–504。

[83] Elena Simperl and Markus Luczak-Rösch. 2014. Collaborative ontology engineering: a survey. The Knowledge Engineering Review 29, 1 (2014), 101–131.
[83] エレナ・シンペル、マルクス・ルツァック＝ロッシュ。2014年。共同オントロジー工学：調査。知識工学レビュー 29, 1 (2014), 101–131。

[84] Rudi Studer, V Richard Benjamins, and Dieter Fensel. 1998. Knowledge engineering: Principles and methods. Data & knowledge engineering 25, 1-2 (1998), 161–197.
[84] ルディ・スタウダー、V・リチャード・ベンジャミンズ、ディーター・フェンセル。1998年。知識工学：原則と方法。データと知識工学 25, 1-2 (1998), 161–197。

Manuscript submitted to ACM  
原稿はACMに提出されました。

-----
22 Elisavet Koutsiana, Johanna Walker, Michelle Nwachukwu, Albert Meroño-Peñuela, and Elena Simperl
22 エリサベト・クーツィアナ、ジョハンナ・ウォーカー、ミシェル・ヌワチュク、アルバート・メローニョ・ペニュエラ、エレナ・シンペル

[85] Mari Carmen Suárez-Figueroa, Asunción Gómez-Pérez, and Mariano Fernández-López. 2011. The NeOn methodology for ontology engineering. In _Ontology engineering in a networked world. Springer, 9–34._
[85] マリ・カルメン・スアレス・フィゲロア、アスンシオン・ゴメス・ペレス、マリアーノ・フェルナンデス・ロペス。2011年。ネットワーク化された世界におけるオントロジー工学のためのNeOnメソッド。_ネットワーク化された世界におけるオントロジー工学。スプリンガー、9–34。

[86] Gyte Tamašauskait˙ e and Paul Groth. 2023. Defining a knowledge graph development process through a systematic review.˙ _ACM Transactions on_ _Software Engineering and Methodology 32, 1 (2023), 1–40._
[86] ギテ・タマシャウスカイテ、ポール・グロス。2023年。体系的レビューを通じた知識グラフ開発プロセスの定義。_ACMソフトウェア工学と方法論に関するトランザクション 32, 1 (2023), 1–40。

[87] Katherine Thornton, Harold Solbrig, Gregory S Stupp, Jose Emilio Labra Gayo, Daniel Mietchen, Eric Prud’Hommeaux, and Andra Waagmeester.
2019. Using shape expressions (ShEx) to share RDF data models and to guide curation with rigorous validation. In The Semantic Web: 16th _International Conference, ESWC 2019, Portorož, Slovenia, June 2–6, 2019, Proceedings 16. Springer, 606–620._
[87] キャサリン・ソーントン、ハロルド・ソルブリッグ、グレゴリー・S・スタップ、ホセ・エミリオ・ラブラ・ガヨ、ダニエル・ミエトヒェン、エリック・プルドゥモノー、アンドラ・ワーグミースター。
2019年。形状表現（ShEx）を使用してRDFデータモデルを共有し、厳密な検証でキュレーションをガイドする。セマンティックウェブ：第16回_国際会議、ESWC 2019、ポルトロズ、スロベニア、2019年6月2–6日、議事録16。スプリンガー、606–620。

[88] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288 (2023).
[88] ヒューゴ・トゥーヴロン、ルイ・マルタン、ケビン・ストーン、ピーター・アルバート、アムジャド・アルマヘイリ、ヤスミン・ババエイ、ニコライ・バシュリコフ、ソウミヤ・バトラ、プラジュワル・バルガバ、シュルティ・ボサレ、他。2023年。Llama 2：オープンファンデーションとファインチューニングされたチャットモデル。arXivプレプリント arXiv:2307.09288 (2023)。

[89] Marieke van Erp, William Tullett, Vincent Christlein, Thibault Ehrhart, Ali Hürriyetoğlu, Inger Leemans, Pasquale Lisena, Stefano Menini, Daniel Schwabe, Sara Tonelli, et al. 2023. More than the Name of the Rose: How to Make Computers Read, See, and Organize Smells. The American _Historical Review 128, 1 (2023), 335–369._
[89] マリーケ・ファン・エルプ、ウィリアム・タレット、ヴィンセント・クリストライン、ティボー・エールハルト、アリ・フリリェトグル、インガー・レーマンス、パスクワーレ・リセナ、ステファノ・メニーニ、ダニエル・シュワーベ、サラ・トネッリ、他。2023年。バラの名前以上のもの：コンピュータに匂いを読み、見て、整理させる方法。アメリカ_歴史レビュー 128, 1 (2023), 335–369。

[90] Juan David Velásquez-Henao, Carlos Jaime Franco-Cardona, and Lorena Cadavid-Higuita. 2023. Prompt Engineering: a methodology for optimizing interactions with AI-Language Models in the field of engineering. Dyna 90, 230 (2023), 9–17.
[90] フアン・ダビッド・ベラスケス・ヘナオ、カルロス・ハイメ・フランコ・カルドナ、ロレナ・カダビッド・ヒギータ。2023年。プロンプトエンジニアリング：工学分野におけるAI言語モデルとのインタラクションを最適化するための方法論。ダイナ 90, 230 (2023), 9–17。

[91] Blerta Veseli, Sneha Singhania, Simon Razniewski, and Gerhard Weikum. 2023. Evaluating Language Models for Knowledge Base Completion. In _European Semantic Web Conference. Springer, 227–243._
[91] ブレルタ・ヴェセリ、スネハ・シンガニア、サイモン・ラズニエフスキ、ゲルハルト・ヴァイカム。2023年。知識ベースの補完のための言語モデルの評価。_欧州セマンティックウェブ会議において。スプリンガー、227–243。

[92] Michael Matthias Voit and Heiko Paulheim. 2021. Bias in Knowledge Graphs–an Empirical Study with Movie Recommendation and Different Language Editions of DBpedia. arXiv preprint arXiv:2105.00674 (2021).
[92] ミヒャエル・マティアス・ボイト、ハイコ・パウルハイム。2021年。知識グラフにおけるバイアス–映画推薦とDBpediaの異なる言語版を用いた実証研究。arXivプレプリント arXiv:2105.00674 (2021)。

[93] Denny Vrandečić and Markus Krötzsch. 2014. Wikidata: A Free Collaborative Knowledge Base. Commun. ACM 57, 10 (2014), 78–85.
[93] デニー・ヴランデチッチ、マルクス・クローエツシュ。2014年。ウィキデータ：無料の共同知識ベース。ACMコミュニケーション 57, 10 (2014), 78–85。

[94] Johanna Walker, Elisavet Koutsiana, Joe Massey, Gefion Theurmer, and Elena Simperl. 2023. Prompting Datasets: Data Discovery with Conversational Agents. arXiv preprint arXiv:2312.09947 (2023).
[94] ジョハンナ・ウォーカー、エリサベト・クーツィアナ、ジョー・マッセイ、ゲフィオン・テウルマー、エレナ・シンペル。2023年。プロンプトデータセット：会話型エージェントによるデータ発見。arXivプレプリント arXiv:2312.09947 (2023)。

[95] Shuhe Wang, Xiaofei Sun, Xiaoya Li, Rongbin Ouyang, Fei Wu, Tianwei Zhang, Jiwei Li, and Guoyin Wang. 2023. Gpt-ner: Named entity recognition via large language models. arXiv preprint arXiv:2304.10428 (2023).
[95] シュヘ・ワン、シャオフェイ・サン、シャオヤ・リ、ロンビン・オウヤン、フェイ・ウー、ティエンウェイ・ジャン、ジウェイ・リ、グオイン・ワン。2023年。Gpt-ner：大規模言語モデルによる名前付きエンティティ認識。arXivプレプリント arXiv:2304.10428 (2023)。

[96] Zhao Wang and Aron Culotta. 2020. Identifying Spurious Correlations for Robust Text Classification. In Findings of the Association for Computational _Linguistics: EMNLP 2020. 3431–3440._
[96] ザオ・ワン、アロン・カリオッタ。2020年。堅牢なテキスト分類のための虚偽の相関関係の特定。_計算言語学会の発表：EMNLP 2020において。3431–3440。

[97] Zhao Wang and Aron Culotta. 2021. Robustness to spurious correlations in text classification via automatically generated counterfactuals. In _Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 35. 14024–14031._
[97] ザオ・ワン、アロン・カリオッタ。2021年。自動生成された反実仮想を通じたテキスト分類における虚偽の相関関係に対する堅牢性。_人工知能に関するAAAI会議の議事録において、ボリューム35。14024–14031。

[98] Jason Weston, Antoine Bordes, Oksana Yakhnenko, and Nicolas Usunier. 2013. Connecting Language and Knowledge Bases with Embedding Models for Relation Extraction. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing. 1366–1371.
[98] ジェイソン・ウェストン、アントワーヌ・ボルデス、オクサナ・ヤフネンコ、ニコラス・ウスニエ。2013年。関係抽出のための埋め込みモデルを用いた言語と知識ベースの接続。2013年自然言語処理における経験的手法に関する会議の議事録において。1366–1371。

[99] Qinghao Ye, Haiyang Xu, Guohai Xu, Jiabo Ye, Ming Yan, Yiyang Zhou, Junyang Wang, Anwen Hu, Pengcheng Shi, Yaya Shi, et al. 2023. mplug-owl: Modularization empowers large language models with multimodality. arXiv preprint arXiv:2304.14178 (2023).
[99] チンハオ・イエ、ハイヤン・シュー、グオハイ・シュー、ジアボ・イエ、ミン・ヤン、イーヤン・ジョウ、ジュンヤン・ワン、アンウェン・フー、ペンチョン・シー、ヤヤ・シー、他。2023年。mplug-owl：モジュール化が大規模言語モデルに多様性を与える。arXivプレプリント arXiv:2304.14178 (2023)。

[100] Xiangji Zeng, Yunliang Li, Yuchen Zhai, and Yin Zhang. 2020. Counterfactual generator: A weakly-supervised method for named entity recognition.
In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP). 7270–7280.
[100] シャンジ・ゼン、ユンリャン・リー、ユーチェン・ジャイ、イン・ジャン。2020年。反実仮想生成器：名前付きエンティティ認識のための弱教師あり手法。
2020年自然言語処理における経験的手法に関する会議の議事録において。7270–7280。

[101] Rui Zhang, Yixin Su, Bayu Distiawan Trisedya, Xiaoyan Zhao, Min Yang, Hong Cheng, and Jianzhong Qi. 2023. AutoAlign: Fully Automatic and Effective Knowledge Graph Alignment enabled by Large Language Models. IEEE Transactions on Knowledge and Data Engineering (2023).
[101] ルイ・ジャン、イーシン・スー、バユ・ディスティアワン・トリセダ、シャオヤン・ジャオ、ミン・ヤン、ホン・チェン、ジアンジョン・チー。2023年。AutoAlign：大規模言語モデルによって可能にされた完全自動かつ効果的な知識グラフの整合。IEEE知識とデータ工学トランザクション (2023)。

[102] Wenkai Zhang, Hongyu Lin, Xianpei Han, and Le Sun. 2021. De-biasing Distantly Supervised Named Entity Recognition via Causal Intervention.
In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural _Language Processing (Volume 1: Long Papers). 4803–4813.
[102] ウェンカイ・ジャン、ホンユ・リン、シアンペイ・ハン、レ・スン。2021年。因果介入を通じた遠隔監視された名前付きエンティティ認識のバイアス除去。
計算言語学会第59回年次総会および第11回国際共同自然言語処理会議の議事録において_(ボリューム1：長論文)。4803–4813。

[103] Yuhao Zhang, Peng Qi, and Christopher D Manning. 2018. Graph Convolution over Pruned Dependency Trees Improves Relation Extraction. In _Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing
[103] ユーハオ・ジャン、ペン・チー、クリストファー・D・マニング。2018年。剪定された依存木上のグラフ畳み込みが関係抽出を改善する。_2018年自然言語処理における経験的手法に関する会議の議事録において。



. 2018. Graph Convolution over Pruned Dependency Trees Improves Relation Extraction. In _Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. 2205–2215._
2018年。剪定された依存木に対するグラフ畳み込みが関係抽出を改善する。_2018年自然言語処理に関する実証的方法会議の議事録において。2205–2215。_

[104] Jieyu Zhao, Tianlu Wang, Mark Yatskar, Vicente Ordonez, and Kai-Wei Chang. 2017. Men also like shopping: Reducing gender bias amplification using corpus-level constraints. arXiv preprint arXiv:1707.09457 (2017).
[104] Jieyu Zhao, Tianlu Wang, Mark Yatskar, Vicente Ordonez、Kai-Wei Chang。2017年。男性も買い物が好き：コーパスレベルの制約を使用して性別バイアスの増幅を減少させる。arXivプレプリントarXiv:1707.09457（2017年）。

**A** **APPENDIX: A**
**A** **付録：A**

_Consent. Consent text (to read to interviewees):_
_同意。インタビュー対象者に読むための同意文：_

With this research, we aim to investigate how knowledge engineers and practitioners use LLMs to develop and maintain KGs, ontologies, and knowledge bases. 
この研究では、知識エンジニアや実務者がLLMsを使用してKGs、オントロジー、および知識ベースを開発および維持する方法を調査することを目指しています。

We will not collect any personal data. 
私たちは、個人データを収集しません。

The responses to the questions are fully anonymous. 
質問への回答は完全に匿名です。

The collected data will be shared with Otter AI, an automated transcription service hosted on an AWS server in the US. 
収集されたデータは、米国のAWSサーバーでホストされている自動転写サービスであるOtter AIと共有されます。

Your data will be processed under the terms of UK data protection law (including the UK General Data Protection Regulation (UK GDPR) and the Data Protection Act 2018). 
あなたのデータは、英国のデータ保護法（英国一般データ保護規則（UK GDPR）および2018年データ保護法を含む）の条件に従って処理されます。

Transcripts will be kept until the publication of the research. 
トランスクリプトは、研究の出版まで保持されます。

If you consent to participate in this study, please say loud and clear “Yes I consent”.
この研究に参加することに同意する場合は、「はい、同意します」と大きな声で言ってください。

Manuscript submitted to ACM  
原稿はACMに提出されました。

-----
Knowledge Prompting: How Knowledge Engineers Use Large Language Models 23
_Introduction. Give a bit of an intro of what are the main topics of the questions (e.g., your experience during Hackathon, challenges, skills, automation, evaluation, responsible AI). In the end we will ask you about anything important you want to mention, and you will have time to add comments. Mention that there is no wrong answer._
知識の促進：知識エンジニアが大規模言語モデルをどのように使用するか 23
_序論。質問の主なトピック（例：ハッカソン中の経験、課題、スキル、自動化、評価、責任あるAI）について簡単に紹介してください。最後に、あなたが言及したい重要なことについて尋ねますので、コメントを追加する時間があります。間違った答えはないことを伝えてください。_

_Questions._
_質問。_

(1) What is your experience with KE and building KGs/ontologies?
(1) KEおよびKGs/オントロジーの構築に関するあなたの経験は何ですか？

(2) How did you find the process of interacting with LLMS to solve KE tasks?
(2) KEタスクを解決するためにLLMSと対話するプロセスはどのように感じましたか？

(3) We found that during the Hackathon it was challenging for the groups to (i) find a dataset for testing their pipelines, (ii) find the right prompt questions for the LLMs, and (iii) evaluate the quality of each step toward building an ontology. Which one do you think is the most important?
(3) ハッカソン中、グループが（i）パイプラインをテストするためのデータセットを見つけること、（ii）LLMsに対する適切なプロンプト質問を見つけること、（iii）オントロジーを構築するための各ステップの質を評価することが難しかったことがわかりました。どれが最も重要だと思いますか？

(4) What do you think were the most important skills you have to complete the tasks during the Hackathon?
(4) ハッカソン中にタスクを完了するために最も重要なスキルは何だと思いますか？

(a) Do you feel you had those skills, or do you need to gain experience to complete several tasks?
(a) あなたはそのスキルを持っていると感じますか、それともいくつかのタスクを完了するために経験を積む必要がありますか？

(5) Was there any automated process in the project you worked on during the Hackathon?
(5) ハッカソン中に取り組んだプロジェクトに自動化されたプロセスはありましたか？

(a) What was the purpose of this automation?
(a) この自動化の目的は何でしたか？

(6) Currently, to evaluate ontologies and KG constructions, we use metrics like precision and recall against gold standards, or human evaluation (semantic metric). Do you think this is enough?
(6) 現在、オントロジーとKG構築を評価するために、ゴールドスタンダードに対する精度や再現率などの指標、または人間の評価（意味的指標）を使用しています。これで十分だと思いますか？

(a) What they would look like new benchmarks and metrics?
(a) 新しいベンチマークや指標はどのようなものになると思いますか？

(7) Have you previously used safety testing for responsible AI? Safety testing can be Bias testing against discrimination, Ethical considerations, risk assessment, test for long-term effects.
(7) 責任あるAIのために安全性テストを以前に使用したことがありますか？安全性テストには、差別に対するバイアステスト、倫理的考慮、リスク評価、長期的影響のテストが含まれます。

(a) Do you think this can be used in the LLMs KE scenarios or we need to develop specific solutions?
(a) これはLLMsのKEシナリオで使用できると思いますか、それとも特定のソリューションを開発する必要がありますか？

(8) Do you think there is anything else important for us to know related to LLMs and KE?
(8) LLMsとKEに関連して、私たちが知っておくべき他に重要なことはありますか？

Manuscript submitted to ACM  
原稿はACMに提出されました。

-----
Knowledge Prompting: How Knowledge Engineers Use Large Language Models 25
知識の促進：知識エンジニアが大規模言語モデルをどのように使用するか 25

**B** **APPENDIX: B**
**B** **付録：B**

Table 6. Codebook created by applying inductive and deductive thematic analysis.
表6. 帰納的および演繹的テーマ分析を適用して作成されたコードブック。

**First level code** **Second level code** **Third level code**
**第一レベルコード** **第二レベルコード** **第三レベルコード**

Background Experience
背景 経験

KG construction KG explainability Machine Learning Ontologies Multidisciplinary background
KG構築 KGの説明可能性 機械学習 オントロジー 学際的背景

Bias
バイアス

Bias as risk Bias mitigation awareness Difficulty of assessing bias Limited awareness Other safety issues Removing bias Types of bias
リスクとしてのバイアス バイアス軽減の認識 バイアス評価の難しさ 限られた認識 その他の安全問題 バイアスの除去 バイアスの種類

Challenges
課題

Dataset Evaluation
データセット 評価

KE tasks still demand manual evaluation Lack in KE evaluation techniques
KEタスクは依然として手動評価を必要とする KE評価技術の不足

Prompting
プロンプト

Evaluation
評価

Current evaluation techniques
現在の評価技術

Evaluate the new knowledge produced by LLMs KE evaluation techniques are not sufficient LLMs output is hard to process
LLMsによって生成された新しい知識を評価する KE評価技術は不十分 LLMsの出力は処理が難しい

New evaluation techniques
新しい評価技術

LLM use opinions
LLMの使用意見

Promising
有望

LLMs can support humans LLMs could improve KE tools
LLMsは人間をサポートできる LLMsはKEツールを改善できる

Skeptic
懐疑的

LLMs are not trusted LLMs cannot perform all KE tasks and still need humans in the loop
LLMsは信頼されていない LLMsはすべてのKEタスクを実行できず、依然として人間の介入が必要である

Skills
スキル

Skills had and helped
持っていたスキルと助けたスキル

Communication Knowledge or ontology engineering LLM Technical skills
コミュニケーション 知識またはオントロジーエンジニアリング LLM 技術スキル

Skills need to have
持つべきスキル

LLM Ontology design or ontology engineering Technical skills
LLM オントロジー設計またはオントロジーエンジニアリング 技術スキル

Manuscript submitted to ACM  
原稿はACMに提出されました。

|First level code|Second level code|Third level code|
|---|---|---|
|Background Experience|KG construction KG explainability Machine Learning Ontologies Multidisciplinary background|| 
|Bias|Bias as risk Bias mitigation awareness Difficulty of assessing bias Limited awareness Other safety issues Removing bias Types of bias|| 
|Challenges|Dataset Evaluation Prompting|KE tasks still demand manual evaluation Lack in KE evaluation techniques| 
|Evaluation|Current evaluation techniques New evaluation techniques|Evaluate the new knowledge produced by LLMs KE evaluation techniques are not sufficient LLMs output is hard to process| 
|LLM use opinions|Promising Skeptic|LLMs can support humans LLMs could improve KE tools LLMs are not trusted LLMs cannot perform all KE tasks and still need humans in the loop| 
|Skills|Skills had and helped Skills need to have|Communication Knowledge or ontology engineering LLM Technical skills LLM Ontology design or ontology engineering Technical skills|  

-----
Knowledge Prompting: How Knowledge Engineers Use Large Language Models 25
知識の促進：知識エンジニアが大規模言語モデルをどのように使用するか 25

**C** **APPENDIX: C**
**C** **付録：C**

Table 7. KE and LLM tools and methodologies with description and references.
表7. KEおよびLLMツールと方法論の説明と参考文献。

**Tools/Methodologies** **Description** **Reference**
**ツール/方法論** **説明** **参考文献**

**KE** eXtremeDesign methodology A framework for pattern based ontology design [6]
**KE** eXtremeDesign方法論 パターンベースのオントロジー設計のためのフレームワーク [6]

NeOn methodology A scenario-based methodology that supports the collaborative and dynamic aspects of ontology development, including in distributed environments
NeOn方法論 分散環境を含むオントロジー開発の協力的かつ動的な側面をサポートするシナリオベースの方法論

HermiT Reasoner A reasoner for ontologies that, given an OWL file, can determine if the ontology consistent, identify subsumption relationships between classes, and more
HermiT推論機 OWLファイルが与えられた場合にオントロジーが一貫しているかどうかを判断し、クラス間の包含関係を特定することができるオントロジー用の推論機

OOPS A web-based tool, independent of the ontology development environment, used for detecting modelling errors
OOPS オントロジー開発環境に依存しないウェブベースのツールで、モデリングエラーを検出するために使用される

OAEI Aims at comparing ontology matching systems on precisely defined test cases which can be based on ontologies of different levels of complexity and use different evaluation modalities
OAEI 明確に定義されたテストケースに基づいてオントロジー照合システムを比較することを目的としており、異なるレベルの複雑さのオントロジーに基づくことができ、異なる評価モダリティを使用する

OntoClean A methodology for validating the ontological adequacy of taxonomic relationships based on formal, domain-independent properties of classes
OntoClean クラスの形式的かつドメインに依存しない特性に基づいて、分類関係のオントロジーの適切性を検証するための方法論

**LLMs** ChatGPT A language model developed by OpenAI [76]
**LLMs** ChatGPT OpenAIによって開発された言語モデル [76]

PaLM A transformer-based model developed by Google [3]
PaLM Googleによって開発されたトランスフォーマーベースのモデル [3]

Llama A family of transformer-based autoregressive causal language models developed by Meta
Llama Metaによって開発されたトランスフォーマーベースの自己回帰因果言語モデルのファミリー

mPLUG-Owl A multimodal model that integrates images, text, and other information for comprehension and to generate responses
mPLUG-Owl 理解のために画像、テキスト、およびその他の情報を統合し、応答を生成するマルチモーダルモデル

InstructBLIP A vision-language model leveraging instruction tuning to achieve state-of-the-art performance
InstructBLIP 最先端のパフォーマンスを達成するために指示調整を活用するビジョン・ランゲージモデル

Claude A language model developed by Anthropic with use cases such as summarisation, Q&A, and coding
Claude 要約、Q&A、コーディングなどのユースケースを持つAnthropicによって開発された言語モデル

Manuscript submitted to ACM  
原稿はACMに提出されました。

|Tools/Methodologies|Description|Reference|
|---|---|---|
|KE||| 
|eXtremeDesign methodology|A framework for pattern based ontology design|[6]| 
|NeOn methodology|A scenario-based methodology that supports the collaborative and dynamic aspects of ontology development, including in distributed environments|[85]| 
|HermiT Reasoner|A reasoner for ontologies that, given an OWL file, can determine if the ontology consistent, identify subsumption relationships between classes, and more|[30]| 
|OOPS|A web-based tool, independent of the ontology development environment, used for detecting modelling errors|[80]| 
|OAEI|Aims at comparing ontology matching systems on precisely defined test cases which can be based on ontologies of different levels of complexity and use different evaluation modalities|[26]| 
|OntoClean|A methodology for validating the ontological adequacy of taxonomic relationships based on formal, domain-independent properties of classes|[34]| 
|LLMs||| 
|ChatGPT|A language model developed by OpenAI|[76]| 
|PaLM|A transformer-based model developed by Google|[3]| 
|Llama|A family of transformer-based autoregressive causal language models developed by Meta|[88]| 
|mPLUG-Owl|A multimodal model that integrates images, text, and other information for comprehension and to generate responses|[99]| 
|InstructBLIP|A vision-language model leveraging instruction tuning to achieve state-of-the-art performance|[17]| 
|Claude|A language model developed by Anthropic with use cases such as summarisation, Q&A, and coding|[4]|  
