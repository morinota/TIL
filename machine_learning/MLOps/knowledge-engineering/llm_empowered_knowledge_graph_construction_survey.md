refs: https://arxiv.org/pdf/2510.20345


## LLM-EMPOWERED KNOWLEDGE GRAPH CONSTRUCTION: A SURVEY
## LLMによって強化された知識グラフ構築：調査

**Haonan Bian** Xidian University Xi’an China 23151214251@stu.xidian.edu.cn  
**ハオナン・ビアン** 西安電子科技大学 中国 23151214251@stu.xidian.edu.cn  

#### ABSTRACT  
Knowledge Graphs (KGs) have long served as a fundamental infrastructure for structured knowledge representation and reasoning. 
知識グラフ（KG）は、構造化された知識の表現と推論のための基本的なインフラストラクチャとして長い間機能してきました。

With the advent of Large Language Models (LLMs), the construction of KGs has entered a new paradigm—shifting from rule-based and statistical pipelines to language-driven and generative frameworks. 
大規模言語モデル（LLM）の登場により、KGの構築は新しいパラダイムに入り、ルールベースおよび統計的なパイプラインから、言語駆動型および生成的なフレームワークへと移行しています。

This survey provides a comprehensive overview of recent progress in LLM-empowered knowledge graph construction, systematically analyzing how LLMs reshape the classical three-layered pipeline of ontology engineering, knowledge extraction, and knowledge fusion. 
この調査は、LLMによって強化された知識グラフ構築の最近の進展を包括的に概観し、LLMがどのように従来の三層パイプライン（オントロジー工学、知識抽出、知識融合）を再構築するかを体系的に分析します。

We first revisit traditional KG methodologies to establish conceptual foundations, and then review emerging LLM-driven approaches from two complementary perspectives: schema-based paradigms, which emphasize structure, normalization, and consistency; and schema-free paradigms, which highlight flexibility, adaptability, and open discovery. 
まず、従来のKG手法を再検討し、概念的な基盤を確立した後、構造、正規化、一貫性を強調するスキーマベースのパラダイムと、柔軟性、適応性、オープンな発見を強調するスキーマフリーパラダイムという2つの補完的な視点から新たに出現したLLM駆動のアプローチをレビューします。

Across each stage, we synthesize representative frameworks, analyze their technical mechanisms, and identify their limitations. 
各段階において、代表的なフレームワークを統合し、その技術的メカニズムを分析し、限界を特定します。

Finally, the survey outlines key trends and future research directions, including KG-based reasoning for LLMs, dynamic knowledge memory for agentic systems, and multimodal KG construction. 
最後に、この調査は、LLMのためのKGベースの推論、エージェントシステムのための動的知識メモリ、マルチモーダルKG構築など、主要なトレンドと今後の研究方向を概説します。

Through this systematic review, we aim to clarify the evolving interplay between LLMs and knowledge graphs, bridging symbolic knowledge engineering and neural semantic understanding toward the development of adaptive, explainable, and intelligent knowledge systems. 
この体系的なレビューを通じて、LLMと知識グラフの進化する相互作用を明確にし、適応可能で説明可能な知識システムの開発に向けて、象徴的な知識工学と神経的意味理解をつなぐことを目指します。

#### 1 INTRODUCTION  
Knowledge Graphs (KGs) have long served as a cornerstone for representing, integrating, and reasoning over structured knowledge. 
知識グラフ（KG）は、構造化された知識を表現、統合、推論するための基盤として長い間機能してきました。

They provide a unified semantic foundation that underpins a wide range of intelligent applications, such as semantic search, question answering, and scientific discovery. 
KGは、セマンティック検索、質問応答、科学的発見など、幅広いインテリジェントアプリケーションを支える統一された意味的基盤を提供します。

Conventional KG construction pipelines are typically composed of three major components: **ontology engineering, knowledge extraction, and knowledge fusion. 
従来のKG構築パイプラインは、通常、3つの主要なコンポーネント（オントロジー工学、知識抽出、知識融合）で構成されています。

Despite their success in enabling large-scale knowledge organization, traditional paradigms (e.g., Zhong et al. (2023); Zhao et al. (2024)) continue to face three enduring challenges: 
大規模な知識の組織化を可能にする上での成功にもかかわらず、従来のパラダイム（例：Zhong et al. (2023); Zhao et al. (2024)）は、依然として3つの永続的な課題に直面しています。

(1) Scalability and data sparsity, as rule-based and supervised systems often fail to generalize across domains; 
（1）スケーラビリティとデータの希薄性：ルールベースおよび監視型システムは、しばしばドメインを超えて一般化できないためです。

(2) Expert dependency and rigidity, since schema and ontology design require substantial human intervention and lack adaptability; 
（2）専門家依存と硬直性：スキーマとオントロジーの設計には多大な人間の介入が必要であり、適応性に欠けるためです。

and (3) Pipeline fragmentation, where the disjoint handling of construction stages causes cumulative error propagation. 
（3）パイプラインの断片化：構築段階の分断的な処理が累積的なエラー伝播を引き起こすためです。

These limitations hinder the development of self-evolving, large-scale, and dynamic KGs. 
これらの制限は、自己進化する大規模で動的なKGの開発を妨げています。

The advent of Large Language Models (LLMs) introduces a transformative paradigm for overcoming these bottlenecks. 
大規模言語モデル（LLM）の登場は、これらのボトルネックを克服するための変革的なパラダイムを導入します。

Through large-scale pretraining and emergent generalization capabilities, LLMs enable three key mechanisms: 
大規模な事前学習と新たに現れる一般化能力を通じて、LLMは3つの重要なメカニズムを可能にします。

(1) Generative knowledge modeling, synthesizing structured representations directly from unstructured text; 
（1）生成的知識モデリング：非構造化テキストから直接構造化された表現を合成します。

(2) Semantic unification, integrating heterogeneous knowledge sources through natural language grounding; 
（2）意味的統合：自然言語の基盤を通じて異種の知識源を統合します。

and (3) Instruction-driven orchestration, coordinating complex KG construction workflows via prompt-based interaction. 
（3）指示駆動のオーケストレーション：プロンプトベースのインタラクションを介して複雑なKG構築ワークフローを調整します。

Consequently, LLMs are evolving beyond traditional text-processing tools into cognitive engines that seamlessly bridge natural language and structured knowledge (e.g., Zhu et al. (2024b); Zhang & Soh (2024)).  
その結果、LLMは従来のテキスト処理ツールを超えて、自然言語と構造化された知識をシームレスに結びつける認知エンジンへと進化しています（例：Zhu et al. (2024b); Zhang & Soh (2024)）。

This evolution marks a paradigm shift from rule-driven, pipeline-based systems toward LLM-driven, unified, and adaptive frameworks, where knowledge acquisition, organization, and reasoning emerge as interdependent processes within a generative and self-refining ecosystem (Pan et al., 2024). 
この進化は、ルール駆動型のパイプラインベースのシステムから、LLM駆動型の統一的かつ適応的なフレームワークへのパラダイムシフトを示しており、知識の獲得、組織化、推論が生成的で自己洗練的なエコシステム内で相互依存するプロセスとして現れます（Pan et al., 2024）。

In light of these rapid advances, this paper presents a comprehensive survey of LLM-driven knowledge graph construction. 
これらの急速な進展を踏まえ、本論文ではLLM駆動の知識グラフ構築に関する包括的な調査を提示します。

We systematically review recent research spanning ontology engineering, knowledge extraction, and fusion, analyze emerging methodological paradigms, and highlight open challenges and future directions at the intersection of LLMs and knowledge representation. 
オントロジー工学、知識抽出、融合にわたる最近の研究を体系的にレビューし、新たに出現した方法論的パラダイムを分析し、LLMと知識表現の交差点における未解決の課題と今後の方向性を強調します。

The remainder of this paper is organized as follows: 
本論文の残りの部分は以下のように構成されています。

- Section 2 introduces the foundations of traditional knowledge graph construction, covering ontology engineering, knowledge extraction, and fusion techniques prior to the LLM era. 
- セクション2では、従来の知識グラフ構築の基礎を紹介し、LLM時代以前のオントロジー工学、知識抽出、融合技術をカバーします。

- Section 3 reviews LLM-enhanced ontology construction, encompassing both top-down paradigms (LLMs as ontology assistants) and bottom-up paradigms (KGs for LLMs). 
- セクション3では、LLM強化オントロジー構築をレビューし、トップダウンパラダイム（オントロジーアシスタントとしてのLLM）とボトムアップパラダイム（LLMのためのKG）の両方を含みます。

- Section 4 presents LLM-driven knowledge extraction, comparing schema-based and schema-free methodologies. 
- セクション4では、LLM駆動の知識抽出を提示し、スキーマベースとスキーマフリーの方法論を比較します。

- Section 5 discusses LLM-powered knowledge fusion, focusing on schema-level, instance-level, and hybrid frameworks. 
- セクション5では、LLM駆動の知識融合について議論し、スキーマレベル、インスタンスレベル、ハイブリッドフレームワークに焦点を当てます。

- Section 6 explores future research directions, including KG-based reasoning, dynamic knowledge memory, and multimodal KG construction. 
- セクション6では、KGベースの推論、動的知識メモリ、マルチモーダルKG構築など、今後の研究方向を探ります。

#### 2 PRELIMINARIES  
The construction of Knowledge Graphs (KGs) traditionally follows a three-layered pipeline comprising ontology engineering, knowledge extraction, and knowledge fusion. 
知識グラフ（KG）の構築は、従来、オントロジー工学、知識抽出、知識融合からなる三層のパイプラインに従って行われます。

Prior to the advent of Large Language Models (LLMs), these stages were implemented through rule-based, statistical, and symbolic approaches. 
大規模言語モデル（LLM）の登場以前は、これらの段階はルールベース、統計的、及び象徴的アプローチを通じて実装されていました。

This section briefly reviews these conventional methodologies to establish context for the subsequent discussion on LLM-empowered KG construction. 
このセクションでは、LLMによって強化されたKG構築に関する後続の議論の文脈を確立するために、これらの従来の方法論を簡単にレビューします。

2.1 ONTOLOGY ENGINEERING  
Ontology Engineering (OE) involves the formal specification of domain concepts, relationships, and constraints. 
オントロジー工学（OE）は、ドメインの概念、関係、および制約の正式な仕様を含みます。

In the pre-LLM era, ontologies were primarily manually constructed by domain experts, often supported by semantic web tools such as Protégé and guided by established methodologies including METHONTOLOGY and On-To-Knowledge. 
LLM時代以前、オントロジーは主にドメインの専門家によって手動で構築され、しばしばProtégéなどのセマンティックウェブツールによってサポートされ、METHONTOLOGYやOn-To-Knowledgeなどの確立された方法論に従っていました。

These systematic processes emphasized conceptual rigor and logical consistency but required extensive expert intervention. 
これらの体系的なプロセスは、概念的な厳密さと論理的一貫性を強調しましたが、広範な専門家の介入を必要としました。

As summarized by Zouaq & Nkambou (2010), ontology design during this period was characterized by strong human supervision and limited scalability. 
Zouaq & Nkambou（2010）によって要約されたように、この期間のオントロジー設計は、強い人間の監視と限られたスケーラビリティが特徴でした。

Subsequent semi-automatic approaches—collectively known as ontology learning—sought to derive ontological structures from textual corpora, as reviewed in Asim et al. (2018). 
その後の半自動アプローチ（総称してオントロジー学習と呼ばれる）は、Asim et al.（2018）でレビューされたように、テキストコーパスからオントロジー構造を導出しようとしました。

However, even advanced frameworks such as NeOn struggled with ontology evolution, modular reuse, and dynamic adaptation. 
しかし、NeOnのような高度なフレームワークでさえ、オントロジーの進化、モジュールの再利用、動的適応に苦労しました。

As highlighted by Kotis et al. (2020), traditional OE frameworks offered precision and formal soundness but lacked flexibility and efficiency for large-scale or continuously evolving knowledge domains. 
Kotis et al.（2020）によって強調されたように、従来のOEフレームワークは精度と形式的な健全性を提供しましたが、大規模または継続的に進化する知識ドメインに対する柔軟性と効率に欠けていました。

2.2 KNOWLEDGE EXTRACTION  
Knowledge Extraction (KE) aims to identify entities, relations, and attributes from unstructured or semi-structured data. 
知識抽出（KE）は、非構造化または半構造化データからエンティティ、関係、および属性を特定することを目的としています。

Early approaches relied on handcrafted linguistic rules and pattern matching, which provided interpretability but were brittle and domain-specific. 
初期のアプローチは、手作りの言語ルールとパターンマッチングに依存しており、解釈可能性を提供しましたが、脆弱でドメイン特有でした。

The evolution from symbolic and rule-based systems to statistical and neural methods has been systematically summarized in Pai et al. (2024). 
象徴的およびルールベースのシステムから統計的および神経的手法への進化は、Pai et al.（2024）で体系的に要約されています。

The advent of deep learning architectures, such as BiLSTM-CRF and Transformer-based models, marked a paradigm shift toward data-driven feature learning, as discussed by Yang et al. (2022b). 
BiLSTM-CRFやTransformerベースのモデルなどの深層学習アーキテクチャの登場は、データ駆動型の特徴学習へのパラダイムシフトを示しました（Yang et al.（2022b）による議論）。

Comprehensive analyses such as Detroja et al. (2023) further categorize supervised, weakly supervised, and unsupervised relation extraction paradigms, emphasizing their dependence on annotated data and limited cross-domain generalization.  
Detroja et al.（2023）などの包括的な分析は、監視型、弱監視型、および非監視型の関係抽出パラダイムをさらに分類し、注釈付きデータへの依存と限られたクロスドメイングeneralizationを強調しています。

In summary, traditional KE methods established the technical foundation for modern extraction pipelines but remained constrained by data scarcity, weak generalization, and cumulative error propagation—limitations that motivate the LLM-driven paradigms discussed in later sections.  
要約すると、従来のKE手法は現代の抽出パイプラインの技術的基盤を確立しましたが、データの希少性、弱い一般化、累積的なエラー伝播という制約に悩まされており、これらの制限が後のセクションで議論されるLLM駆動のパラダイムを促進しています。

2.3 KNOWLEDGE FUSION  
Knowledge Fusion (KF) focuses on integrating heterogeneous knowledge sources into a coherent and consistent graph by resolving issues of duplication, conflict, and heterogeneity. 
知識融合（KF）は、重複、対立、および異質性の問題を解決することによって、異種の知識源を一貫した整合性のあるグラフに統合することに焦点を当てています。

A central subtask is entity alignment, which determines whether entities from different datasets refer to the same real-world object. 
中心的なサブタスクはエンティティの整合であり、異なるデータセットからのエンティティが同じ現実世界のオブジェクトを指すかどうかを判断します。

Classical approaches relied on lexical and structural similarity measures, as reviewed in Zeng et al. (2021). 
古典的なアプローチは、Zeng et al.（2021）でレビューされたように、語彙的および構造的な類似性測定に依存していました。

The introduction of representation learning enabled embedding-based techniques that align entities within shared vector spaces, improving scalability and automation, as surveyed by Zhu et al. (2024a). 
表現学習の導入により、共有ベクトル空間内でエンティティを整合させる埋め込みベースの技術が可能になり、Zhu et al.（2024a）による調査でスケーラビリティと自動化が向上しました。

Domain-specific applications, such as Yang et al. (2022a), demonstrate multi-feature fusion strategies combining structural, attribute, and relational similarities. 
Yang et al.（2022a）などのドメイン特有のアプリケーションは、構造的、属性的、関係的な類似性を組み合わせたマルチフィーチャー融合戦略を示しています。

Other graph-level models, such as Liu et al. (2022), further integrate semantic cues to enhance alignment robustness. 
Liu et al.（2022）などの他のグラフレベルのモデルは、整合性の堅牢性を高めるために意味的手がかりをさらに統合しています。

Despite these advancements, traditional fusion pipelines continue to struggle with semantic heterogeneity, large-scale integration, and dynamic knowledge updating—challenges that contemporary LLM-based fusion frameworks are increasingly designed to address. 
これらの進展にもかかわらず、従来の融合パイプラインは、意味的異質性、大規模統合、動的知識更新に苦しみ続けており、現代のLLMベースの融合フレームワークがますますこれらの課題に対処するように設計されています。

Figure 1: Taxonomy of LLM for KGC  
図1: KGCのためのLLMの分類

#### 3 LLM-ENHANCED ONTOLOGY CONSTRUCTION  
The integration of Large Language Models (LLMs) has introduced a fundamental paradigm shift in Ontology Engineering (OE) and, by extension, Knowledge Graph (KG) construction. 
大規模言語モデル（LLM）の統合は、オントロジー工学（OE）およびそれに伴う知識グラフ（KG）構築において根本的なパラダイムシフトをもたらしました。

Current research generally follows two complementary directions: a top-down approach, which leverages LLMs as intelligent assistants for formal ontology modeling, and a bottom-up approach, which employs ontology construction to enhance the reasoning and representation capabilities of LLMs themselves. 
現在の研究は一般的に、形式的なオントロジーモデリングのための知的アシスタントとしてLLMを活用するトップダウンアプローチと、LLM自体の推論および表現能力を強化するためにオントロジー構築を利用するボトムアップアプローチの2つの補完的な方向に従っています。

3.1 TOP-DOWN ONTOLOGY CONSTRUCTION: LLMS AS ONTOLOGY ASSISTANTS  
The top-down paradigm extends the traditions of the Semantic Web and Knowledge Engineering, emphasizing ontology development guided by predefined semantic requirements. 
トップダウンパラダイムは、セマンティックウェブと知識工学の伝統を拡張し、事前に定義された意味的要件に基づいてオントロジーの開発を強調します。



. Within this framework, LLMs serve as advanced co-modelers that assist human experts in translating natural language specifications—such as competency questions (CQs), user stories, or domain descriptions—into formal ontologies, typically represented in OWL or related standards. 
この枠組みの中で、LLMsは高度な共同モデルとして機能し、専門家が自然言語の仕様（能力質問（CQ）、ユーザーストーリー、またはドメイン記述など）を形式的なオントロジーに翻訳するのを支援します。これらは通常、OWLまたは関連する標準で表現されます。

This paradigm prioritizes conceptual abstraction, the precise definition of relations, and structured semantic representation to ensure that subsequent knowledge extraction and instance population adhere to well-defined logical constraints.
このパラダイムは、概念的抽象化、関係の正確な定義、および構造化された意味表現を優先し、次の知識抽出とインスタンスの生成が明確に定義された論理的制約に従うことを保証します。

3.1.1 COMPETENCY QUESTION (CQ)-BASED ONTOLOGY CONSTRUCTION
3.1.1 能力質問（CQ）に基づくオントロジー構築

CQ-based methods represent a requirements-driven pathway toward automated ontology modeling.
CQベースの手法は、自動化されたオントロジーモデリングに向けた要求駆動型の経路を表します。

In this setting, LLMs parse CQs or user stories to identify, categorize, and formalize domain-specific concepts, attributes, and relationships.
この設定では、LLMsはCQやユーザーストーリーを解析して、ドメイン特有の概念、属性、および関係を特定、分類、形式化します。

A pioneering framework, Ontogenia (Lippolis et al., 2025a), introduced the use of Metacognitive Prompting for ontology generation, enabling the model to perform self-reflection and structural correction during synthesis.
先駆的なフレームワークであるOntogenia（Lippolis et al., 2025a）は、オントロジー生成のためのメタ認知プロンプティングの使用を導入し、モデルが合成中に自己反省と構造的修正を行えるようにしました。

By incorporating Ontology Design Patterns (ODPs), Ontogenia improves both the consistency and complexity of generated ontologies.
Ontology Design Patterns（ODP）を取り入れることで、Ontogeniaは生成されたオントロジーの一貫性と複雑性の両方を向上させます。

Similarly, the CQbyCQ framework (Saeedizade & Blomqvist, 2024) demonstrated that LLMs can directly translate CQs and user stories into OWL-compliant schemas, effectively automating the transition from requirements to structured ontological models.
同様に、CQbyCQフレームワーク（Saeedizade & Blomqvist, 2024）は、LLMsがCQやユーザーストーリーをOWL準拠のスキーマに直接翻訳できることを示し、要求から構造化されたオントロジーモデルへの移行を効果的に自動化します。

Building on these advances, Lippolis et al. (2025b) proposed two complementary prompting strategies: a “memoryless” approach for modular construction and a reflective iterative method inspired by Ontogenia.
これらの進展を基に、Lippolis et al.（2025b）は、モジュール構築のための「メモリレス」アプローチと、Ontogeniaに触発された反射的反復手法の2つの補完的なプロンプティング戦略を提案しました。

Empirical evaluations revealed that LLMs can autonomously identify classes, object properties, and data properties, while generating corresponding logical axioms with consistency comparable to that of junior human modelers.
実証的評価により、LLMsが自律的にクラス、オブジェクトプロパティ、およびデータプロパティを特定できることが明らかになり、ジュニアの人間モデルと同等の一貫性を持つ論理公理を生成できることが示されました。

Collectively, these studies have led to semi-automated ontology construction pipelines encompassing the entire lifecycle—from CQ formulation and validation to ontology instantiation—with human experts intervening only at critical checkpoints.
これらの研究は、CQの定式化と検証からオントロジーのインスタンス化までの全ライフサイクルを包含する半自動オントロジー構築パイプラインを生み出し、人間の専門家は重要なチェックポイントでのみ介入します。

Through this evolution, LLMs have transitioned from passive analytical tools to active modeling collaborators in ontology design.
この進化を通じて、LLMsは受動的な分析ツールからオントロジー設計における能動的なモデリングコラボレーターへと移行しました。

3.1.2 NATURAL LANGUAGE-BASED ONTOLOGY CONSTRUCTION
3.1.2 自然言語に基づくオントロジー構築

Beyond CQ-driven paradigms, natural language-based ontology construction seeks to induce semantic schemas directly from unstructured or semi-structured text corpora, eliminating the dependency on explicitly formulated questions.
CQ駆動型のパラダイムを超えて、自然言語に基づくオントロジー構築は、明示的に定式化された質問への依存を排除し、非構造化または半構造化されたテキストコーパスから直接意味的スキーマを誘導しようとします。

The goal is to enable LLMs to autonomously uncover conceptual hierarchies and relational patterns from natural language, achieving a direct mapping from textual descriptions to formal logical representations.
目標は、LLMsが自然言語から自律的に概念階層と関係パターンを発見し、テキスト記述から形式的な論理表現への直接的なマッピングを実現することです。

Foundational work in this domain—including Saeedizade & Blomqvist (2024) and Lippolis et al. (2025b)—systematically evaluated GPT-4’s performance and confirmed that its outputs approach the quality of novice human modelers, thereby validating the feasibility of “intelligent ontology assistants.”
この分野の基礎的な研究（Saeedizade & Blomqvist, 2024およびLippolis et al., 2025bを含む）は、GPT-4のパフォーマンスを体系的に評価し、その出力が初心者の人間モデルの品質に近づくことを確認し、「インテリジェントオントロジーアシスタント」の実現可能性を検証しました。

The LLMs4OL framework (Giglou et al., 2023) further verified LLMs’ capacity for concept identification, relation extraction, and semantic pattern induction in general-purpose domains.
LLMs4OLフレームワーク（Giglou et al., 2023）は、一般目的のドメインにおける概念特定、関係抽出、および意味パターン誘導に対するLLMsの能力をさらに検証しました。

Likewise, Mateiu & Groza (2023) demonstrated the use of fine-tuned models to directly translate natural language into OWL axioms within established ontology editors such as Protégé.
同様に、Mateiu & Groza（2023）は、Protégéなどの確立されたオントロジーエディタ内で自然言語をOWL公理に直接翻訳するために微調整されたモデルの使用を示しました。

Recent systems such as NeOn-GPT (Fathallah et al., 2025) and LLMs4Life (Fathallah et al., 2024) have advanced this direction by introducing end-to-end, prompt-driven workflows that integrate ontology reuse and adaptive refinement to construct deep, coherent ontological structures in complex scientific domains (e.g., life sciences).
最近のシステムであるNeOn-GPT（Fathallah et al., 2025）やLLMs4Life（Fathallah et al., 2024）は、オントロジーの再利用と適応的な洗練を統合するエンドツーエンドのプロンプト駆動型ワークフローを導入することで、この方向を進展させ、複雑な科学分野（例：ライフサイエンス）における深く、一貫したオントロジー構造を構築しています。

Meanwhile, lightweight frameworks such as **LKD-KGC (Sun et al., 2025) enable rapid schema induction for open-domain knowledge graphs by** clustering entity types extracted from document summaries.
一方、**LKD-KGC（Sun et al., 2025）などの軽量フレームワークは、文書要約から抽出されたエンティティタイプをクラスタリングすることによって、オープンドメインの知識グラフの迅速なスキーマ誘導を可能にします。**

In summary, top-down research on LLM-assisted ontology construction emphasizes semantic consistency, structural completeness, and human–AI collaboration, marking a significant evolution of traditional knowledge engineering toward more intelligent, language-driven paradigms.
要約すると、LLM支援のオントロジー構築に関するトップダウンの研究は、意味的一貫性、構造的完全性、および人間とAIのコラボレーションを強調しており、よりインテリジェントで言語駆動のパラダイムへの伝統的な知識工学の重要な進化を示しています。

3.2 BOTTOM-UP ONTOLOGY SCHEMA CONSTRUCTION: KGS FOR LLMS
3.2 ボトムアップオントロジースキーマ構築：LLMsのためのKGs

The bottom-up methodology has gained increasing attention as a response to paradigm shifts introduced by the era of Large Language Models (LLMs), particularly within Retrieval-Augmented Generation (RAG) frameworks.
ボトムアップの方法論は、特にRetrieval-Augmented Generation（RAG）フレームワーク内で、Large Language Models（LLMs）の時代によってもたらされたパラダイムシフトへの応答として、ますます注目を集めています。

In this paradigm, the knowledge graph is no longer viewed merely as a static repository of structured knowledge for human interpretation.
このパラダイムでは、知識グラフはもはや人間の解釈のための構造化された知識の静的なリポジトリとしてのみ見られることはありません。

Instead, it serves as a dynamic infrastructure that provides factual grounding and structured memory for LLMs.
代わりに、それはLLMsのための事実に基づく基盤と構造化されたメモリを提供する動的なインフラストラクチャとして機能します。

Consequently, research focus has shifted from manually designing ontological hierarchies to automatically inducing **schemas from unstructured or semi-structured data. This evolution can be delineated through three** interrelated stages of progress.
その結果、研究の焦点は、手動でオントロジー階層を設計することから、非構造化または半構造化データからのスキーマの自動誘導に移行しました。この進化は、3つの相互関連する進展の段階を通じて区別できます。

Early studies such as GraphRAG (Edge et al., 2024) and OntoRAG (Tiwari et al., 2025) established the foundation for data-driven ontology construction.
GraphRAG（Edge et al., 2024）やOntoRAG（Tiwari et al., 2025）などの初期の研究は、データ駆動型オントロジー構築の基盤を確立しました。

These approaches first generate instance-level graphs from raw text via open information extraction, and then abstract ontological concepts and relations through clustering and generalization.
これらのアプローチは、まずオープン情報抽出を介して生のテキストからインスタンスレベルのグラフを生成し、次にクラスタリングと一般化を通じてオントロジーの概念と関係を抽象化します。

This “data-to-schema” process transforms empirical knowledge into reusable conceptual structures, illustrating how instance-rich corpora can give rise to ontological blueprints.
この「データからスキーマへの」プロセスは、経験的知識を再利用可能な概念構造に変換し、インスタンスが豊富なコーパスがどのようにオントロジーの青写真を生み出すかを示しています。

Building upon this foundation, the EDC (Extract–Define–Canonicalize) framework (Zhang & Soh, 2024) advanced the pipeline into a three-stage process consisting of open extraction, semantic definition, and schema normalization.
この基盤を基に、EDC（Extract–Define–Canonicalize）フレームワーク（Zhang & Soh, 2024）は、オープン抽出、意味定義、およびスキーマ正規化からなる3段階のプロセスにパイプラインを進展させました。

It enables the alignment of automatically induced schemas with existing ontologies, or the creation of new ones when predefined structures are absent.
これにより、自動的に誘導されたスキーマを既存のオントロジーと整合させることができ、事前に定義された構造が存在しない場合には新しいものを作成することができます。

Extending this adaptability, AdaKGC (Ye et al., 2023) addressed the challenge of dynamic schema evolution, allowing models to incorporate novel relations and entity types without retraining.
この適応性を拡張するために、AdaKGC（Ye et al., 2023）は動的スキーマ進化の課題に対処し、モデルが再訓練なしで新しい関係やエンティティタイプを取り入れることを可能にしました。

Collectively, these advances shift the focus from static schema construction toward continuous schema adaptation within evolving knowledge environments.
これらの進展は、静的スキーマ構築から進化する知識環境内での継続的なスキーマ適応へと焦点を移します。

More recent efforts have transitioned beyond algorithmic prototypes toward deployable knowledge systems.
最近の取り組みは、アルゴリズムのプロトタイプを超えて、展開可能な知識システムへと移行しています。

For example, AutoSchemaKG (Bai et al., 2025) integrates schema-based and schema-free paradigms within a unified architecture, supporting the real-time generation and evolution of enterprise-scale knowledge graphs.
例えば、AutoSchemaKG（Bai et al., 2025）は、スキーマベースとスキーマフリーのパラダイムを統一されたアーキテクチャ内で統合し、企業規模の知識グラフのリアルタイム生成と進化をサポートします。

In this stage, KGs operate as a form of external knowledge _memory for LLMs—prioritizing factual coverage, scalability, and maintainability over purely se-_ mantic completeness.
この段階では、KGはLLMsのための外部知識メモリの一形態として機能し、純粋な意味的完全性よりも事実のカバレッジ、スケーラビリティ、および保守性を優先します。

This transformation marks a pragmatic reorientation of ontology construction, emphasizing its service to LLM reasoning and interpretability in knowledge-intensive applications.
この変革は、オントロジー構築の実用的な再指向を示し、知識集約型アプリケーションにおけるLLMの推論と解釈可能性へのサービスを強調します。

In summary, bottom-up ontology schema construction redefines the interplay between LLMs and knowledge engineering.
要約すると、ボトムアップのオントロジースキーマ構築は、LLMsと知識工学の相互作用を再定義します。

The focus evolves from “LLMs for Ontology Engineering” to “Ontolo**gies and KGs for LLMs”.
焦点は「オントロジー工学のためのLLMs」から「LLMsのためのオントロジーとKGs」へと進化します。

Whereas the top-down trajectory emphasizes semantic modeling, logical consistency, and expert-guided alignment—positioning LLMs as intelligent assistants in ontology design—the bottom-up trajectory prioritizes automatic extraction, schema induction, and dynamic evolution.
トップダウンの軌道が意味的モデリング、論理的一貫性、および専門家による整合性を強調し、LLMsをオントロジー設計のインテリジェントアシスタントとして位置付けるのに対し、ボトムアップの軌道は自動抽出、スキーマ誘導、および動的進化を優先します。

This progression advances toward self-updating, interpretable, and scalable knowledge ecosystems that strengthen the grounding and reasoning capabilities of LLMs.
この進展は、LLMsの基盤と推論能力を強化する自己更新可能で解釈可能、かつスケーラブルな知識エコシステムに向かっています。

#### 4 LLM-DRIVEN KNOWLEDGE EXTRACTION
#### 4 LLM駆動の知識抽出

Through a systematic examination of recent advances, it becomes evident that methodologies for Large Language Model (LLM)-driven knowledge extraction have evolved along two principal paradigms: schema-based extraction, which operates under explicit structural guidance, and **schema-free extraction, which transcends the limitations of predefined templates. The former em-**
最近の進展を体系的に検討することで、Large Language Model（LLM）駆動の知識抽出の方法論が、明示的な構造的ガイダンスの下で機能するスキーマベースの抽出と、**事前に定義されたテンプレートの制限を超えるスキーマフリーの抽出という2つの主要なパラダイムに沿って進化していることが明らかになります。前者は-**

phasizes normalization, structural consistency, and semantic alignment, while the latter prioritizes adaptability, openness, and exploratory discovery.
正規化、構造的一貫性、および意味的整合性を強調する一方で、後者は適応性、オープン性、および探索的発見を優先します。

Together, these paradigms delineate the conceptual landscape of contemporary research in LLM-based knowledge extraction.
これらのパラダイムは、LLMベースの知識抽出における現代の研究の概念的な風景を描き出します。

4.1 SCHEMA-BASED METHODS
4.1 スキーマベースの手法

The central principle of schema-based extraction lies in its reliance on an explicit knowledge schema that provides both structural guidance and semantic constraints for the extraction process.
スキーマベースの抽出の中心的な原則は、抽出プロセスのための構造的ガイダンスと意味的制約の両方を提供する明示的な知識スキーマに依存していることです。

Within this paradigm, the research trajectory demonstrates a clear evolution—from the use of static ontological blueprints toward adaptive and dynamically evolving schema frameworks.
このパラダイム内では、研究の軌道は、静的なオントロジーの青写真の使用から、適応的で動的に進化するスキーマフレームワークへの明確な進化を示しています。

4.1.1 STATIC SCHEMA-DRIVEN EXTRACTION
4.1.1 静的スキーマ駆動の抽出

Early studies in LLM-driven knowledge extraction predominantly employed predefined, static **schemas that rigidly constrained the extraction process. In this paradigm, the ontology functions as** a fixed semantic backbone, directing the LLM to populate the knowledge base under strict structural supervision.
LLM駆動の知識抽出における初期の研究は、主に事前定義された静的な**スキーマを使用して、抽出プロセスを厳格に制約しました。このパラダイムでは、オントロジーは**固定された意味的バックボーンとして機能し、LLMに厳格な構造的監視の下で知識ベースを充填するよう指示します。

The progression of this research line can be broadly characterized by three developmental stages.
この研究の進展は、広く3つの発展段階によって特徴付けられます。

Initial efforts, such as Kommineni et al. (2024), utilized fully predefined ontological structures to ensure precision and interpretability.
Kommineni et al.（2024）などの初期の取り組みは、精度と解釈可能性を確保するために完全に事前定義されたオントロジー構造を利用しました。

In their pipeline, the LLM first generates Competency Questions (CQs) to delineate the knowledge scope, constructs the corresponding ontology (TBox), and subsequently performs ABox population under explicit schema supervision—achieving high consistency but limited flexibility.
彼らのパイプラインでは、LLMはまず能力質問（CQ）を生成して知識の範囲を明確にし、対応するオントロジー（TBox）を構築し、その後、明示的なスキーマ監視の下でABoxの充填を行います。これにより高い一貫性が達成されますが、柔軟性は制限されます。

Similarly, the KARMA framework (Lu & Wang, 2025) adopts a multi-agent architecture, in which each agent executes schema-guided extraction tasks to guarantee accurate entity normalization and relation classification within a fixed ontological boundary.
同様に、KARMAフレームワーク（Lu & Wang, 2025）は、各エージェントがスキーマに基づく抽出タスクを実行して、固定されたオントロジーの境界内で正確なエンティティの正規化と関係の分類を保証するマルチエージェントアーキテクチャを採用しています。

Building on these rigid frameworks, subsequent studies sought to enhance modularity and reusability through staged prompting.
これらの厳格なフレームワークを基に、後続の研究は段階的なプロンプティングを通じてモジュール性と再利用性を向上させることを目指しました。

For instance, Feng et al.
例えば、Feng et al.



. For instance, Feng et al. (2024) proposed a two-step “ontology-grounded extraction” approach: first generating a domain-specific ontology directly from text, and then leveraging it as a directive prompt for RDF triple extraction. 
例えば、Fengら（2024）は、2段階の「オントロジーに基づく抽出」アプローチを提案しました。最初にテキストからドメイン特有のオントロジーを直接生成し、それをRDFトリプル抽出の指示プロンプトとして活用します。

This approach strengthens structural alignment while maintaining partial adaptability. 
このアプローチは、部分的な適応性を維持しながら、構造的整合性を強化します。

More recent developments introduce localized flexibility within otherwise static frameworks. 
最近の進展は、静的なフレームワーク内に局所的な柔軟性を導入します。

**ODKE+ (Khorshidi et al., 2025) proposes ontology snippets—dynamically selected ontology sub-** sets—to construct context-aware prompts tailored to specific entities, thus enabling limited schema adaptation at runtime. 
**ODKE+（Khorshidiら、2025）は、特定のエンティティに合わせたコンテキスト対応プロンプトを構築するために、動的に選択されたオントロジーのサブセットであるオントロジースニペットを提案します。**これにより、実行時に限られたスキーマ適応が可能になります。

Likewise, Bhattarai et al. (2024) utilize the medical ontology UMLS to dynamically generate task-specific prompts for clinical information extraction. 
同様に、Bhattaraiら（2024）は、医療オントロジーであるUMLSを利用して、臨床情報抽出のためのタスク特有のプロンプトを動的に生成します。

Although these methods introduce local adaptability, they remain bounded by pre-existing macro-schemas, representing a transitional phase toward schema dynamism. 
これらの方法は局所的な適応性を導入しますが、既存のマクロスキーマに制約されており、スキーマのダイナミズムへの移行段階を示しています。

In summary, static schema-driven extraction forms the foundational paradigm of LLM-assisted knowledge extraction, emphasizing precision, logical consistency, and interpretability. 
要約すると、静的スキーマ駆動の抽出は、LLM支援の知識抽出の基盤となるパラダイムを形成し、精度、論理的一貫性、解釈可能性を強調します。

However, its dependence on rigid ontological templates restricts scalability and cross-domain generalization. 
しかし、厳格なオントロジーテンプレートへの依存は、スケーラビリティとクロスドメインの一般化を制限します。

The progression from fixed schema control to selective, context-aware schema prompting marks the field’s gradual shift toward more adaptive, data-responsive frameworks. 
固定スキーマ制御から選択的でコンテキスト対応のスキーマプロンプトへの進展は、より適応的でデータ応答型のフレームワークへの分野の徐々の移行を示しています。

4.1.2 DYNAMIC AND ADAPTIVE SCHEMA-BASED EXTRACTION
4.1.2 動的かつ適応的なスキーマベースの抽出

Recent approaches reconceptualize the schema as a dynamic, evolving component of the extraction process rather than a fixed template—a shift from schema guiding extraction to schema co-evolving with it. 
最近のアプローチは、スキーマを固定テンプレートではなく、抽出プロセスの動的で進化するコンポーネントとして再概念化しています。これは、スキーマが抽出を導くのではなく、スキーマがそれと共に共進化するというシフトです。

**AutoSchemaKG (Bai et al., 2025) exemplifies this trend by inducing schemas from large-scale cor-** pora via unsupervised clustering and relation discovery. 
**AutoSchemaKG（Baiら、2025）は、無監督クラスタリングと関係発見を通じて大規模コーパスからスキーマを誘導することで、この傾向を示しています。**

It employs multi-stage prompts tailored to different relation types, enabling the schema to evolve iteratively with extracted content and improving open-domain scalability. 
それは、異なる関係タイプに合わせたマルチステージプロンプトを使用し、スキーマが抽出されたコンテンツと共に反復的に進化し、オープンドメインのスケーラビリティを向上させます。

Building on this idea, AdaKGC (Ye et al., 2023) tackles schema _drift through two mechanisms: the Schema-Enriched Prefix Instruction (SPI) for context-aware_ prompting and the Schema-Constrained Dynamic Decoding (SDD) for schema adaptation without retraining. 
このアイデアを基に、AdaKGC（Yeら、2023）は、スキーマのドリフトに対処するために、コンテキスト対応プロンプトのためのスキーマ強化プレフィックス指示（SPI）と、再訓練なしでのスキーマ適応のためのスキーマ制約動的デコーディング（SDD）の2つのメカニズムを使用します。

Together, these methods enable adaptive schema learning, bridging symbolic structure and data-driven flexibility. 
これらの方法は、シンボリックな構造とデータ駆動の柔軟性をつなぐ適応的スキーマ学習を可能にします。

They lay the groundwork for continual, self-updating knowledge graph construction where extraction and schema evolution progress synergistically. 
これにより、抽出とスキーマの進化が相乗的に進行する継続的で自己更新可能な知識グラフ構築の基盤が築かれます。

4.2 SCHEMA-FREE METHODS
4.2 スキーマフリー手法

In contrast to paradigms that depend on externally defined blueprints, schema-free extraction aims to acquire structured knowledge directly from unstructured text without relying on any predefined ontology or relation schema. 
外部で定義された青写真に依存するパラダイムとは対照的に、スキーマフリー抽出は、あらかじめ定義されたオントロジーや関係スキーマに依存せず、非構造化テキストから直接構造化された知識を取得することを目指します。

The central idea is to leverage Large Language Models (LLMs) as autonomous extractors capable of identifying entities and relations through advanced prompt engineering, instruction tuning, and self-organizing reasoning. 
中心的なアイデアは、LLM（大規模言語モデル）を自律的な抽出器として活用し、高度なプロンプトエンジニアリング、指示調整、自己組織化推論を通じてエンティティと関係を特定できるようにすることです。

The evolution of this paradigm unfolds along two major trajectories: structured generative extraction and open information extraction. 
このパラダイムの進化は、構造化生成抽出とオープン情報抽出の2つの主要な軌道に沿って展開します。

4.2.1 STRUCTURED GENERATIVE EXTRACTION
4.2.1 構造化生成抽出

The first trajectory, structured generative extraction, focuses on prompting LLMs to construct an _implicit or on-the-fly schema during generation. 
最初の軌道である構造化生成抽出は、LLMに生成中に暗黙的またはその場でスキーマを構築するよう促すことに焦点を当てています。

Although no external ontology is provided, struc-_ tured reasoning patterns and generative templates guide the model toward consistent and coherent knowledge generation.  
外部のオントロジーは提供されていませんが、構造的推論パターンと生成テンプレートがモデルを一貫した整合性のある知識生成へと導きます。

Early studies, such as Nie et al. (2024), integrated the extraction process with Chain-of-Thought **(CoT) prompting, encouraging stepwise reasoning for entity and relation identification.** 
Nieら（2024）などの初期の研究は、抽出プロセスをChain-of-Thought（CoT）プロンプトと統合し、エンティティと関係の特定のための段階的推論を促しました。

This approach demonstrated that explicit schemas can be effectively replaced by reasoning-driven organization. 
このアプローチは、明示的なスキーマが推論駆動の組織によって効果的に置き換えられることを示しました。

Building on this insight, AutoRE (Xue et al., 2024) introduced an RHF (Relation–Head–Facts) pipeline via instruction fine-tuning, enabling the model to internalize relational regularities and improve coherence and scalability across documents. 
この洞察を基に、AutoRE（Xueら、2024）は、指示微調整を通じてRHF（Relation–Head–Facts）パイプラインを導入し、モデルが関係の規則性を内在化し、文書全体での整合性とスケーラビリティを向上させることを可能にしました。

Subsequent works further enhanced schema-free extraction by incorporating retrieval and interactivity. 
その後の研究は、情報検索とインタラクティビティを組み込むことで、スキーマフリー抽出をさらに強化しました。

For instance, Papaluca et al. (2024) proposed a Retrieval-Augmented prompting framework that dynamically enriches the context window with semantically related exemplars, thereby improving factual precision. 
例えば、Papalucaら（2024）は、文脈ウィンドウを意味的に関連する例で動的に豊かにするRetrieval-Augmentedプロンプトフレームワークを提案し、事実の精度を向上させました。

In parallel, ChatIE (Wei et al., 2024) reformulated extraction as a multi**turn dialogue process, wherein the model iteratively refines entity and relation candidates through** chained question answering. 
同時に、ChatIE（Weiら、2024）は、抽出をマルチターン対話プロセスとして再定義し、モデルが連鎖的な質問応答を通じてエンティティと関係の候補を反復的に洗練させるようにしました。

Similarly, KGGEN (Mo et al., 2025) decomposed extraction into two sequential LLM invocations—first detecting entities, then generating relations—to reduce cognitive load and mitigate error propagation. 
同様に、KGGEN（Moら、2025）は、抽出を2つの連続したLLM呼び出しに分解しました。最初にエンティティを検出し、次に関係を生成することで、認知負荷を軽減し、エラーの伝播を緩和します。

Collectively, these studies reveal that even without explicit schemas, LLMs can internalize latent relational structures through guided reasoning, modular prompting, and interactive refinement—laying the groundwork for open-ended and self-organizing knowledge generation. 
これらの研究は、明示的なスキーマがなくても、LLMがガイド付き推論、モジュールプロンプト、インタラクティブな洗練を通じて潜在的な関係構造を内在化できることを示しており、オープンエンドで自己組織化された知識生成の基盤を築いています。

4.2.2 OPEN INFORMATION EXTRACTION (OIE)
4.2.2 オープン情報抽出（OIE）

**Open Information Extraction (OIE) extends structured generative methods toward schema-free** extraction, aiming to discover all possible entity–relation–object triples from text without relying on predefined types. 
**オープン情報抽出（OIE）は、構造化生成手法をスキーマフリー抽出に拡張し、あらかじめ定義されたタイプに依存せず、テキストからすべての可能なエンティティ–関係–オブジェクトトリプルを発見することを目指します。**

The EDC framework (Zhang & Soh, 2024) exemplifies this paradigm: its Extract stage uses few-shot prompting to generate comprehensive natural-language triples, producing a raw open knowledge graph that later undergoes definition and canonicalization. 
EDCフレームワーク（Zhang & Soh、2024）はこのパラダイムの例です。そのExtractステージは、少数ショットプロンプトを使用して包括的な自然言語トリプルを生成し、後に定義と標準化を経る生のオープン知識グラフを生成します。

OIE prioritizes coverage and discovery over structural regularity. 
OIEは、構造的な規則性よりもカバレッジと発見を優先します。

When combined with schema induction or canonicalization, it bridges unstructured text and emergent ontological organization—completing the continuum from schema-free to schema-generative knowledge construction. 
スキーマ誘導や標準化と組み合わせることで、非構造化テキストと新たに出現するオントロジーの組織をつなぎ、スキーマフリーからスキーマ生成知識構築への連続体を完成させます。

#### 5 LLM-POWERED KNOWLEDGE FUSION
#### 5 LLM駆動の知識融合

An examination of recent advances and pioneering studies indicates that methodologies leveraging Large Language Models (LLMs) for knowledge fusion predominantly address challenges at two fundamental levels: (1) constructing a unified and normalized knowledge skeleton at the schema **layer, and (2) integrating and aligning the specific knowledge flesh at the instance layer.** 
最近の進展と先駆的な研究の検討は、知識融合のために大規模言語モデル（LLM）を活用する方法論が主に2つの基本的なレベルでの課題に対処していることを示しています：（1）スキーマ層での統一された正規化された知識スケルトンの構築、（2）インスタンス層での特定の知識の統合と整合。

According to this distinction, existing approaches can be categorized into three major classes: schema-level **fusion, instance-level fusion, and hybrid frameworks that integrate both.** 
この区別に従って、既存のアプローチは、スキーマレベルの融合、インスタンスレベルの融合、そして両方を統合するハイブリッドフレームワークの3つの主要なクラスに分類できます。

5.1 SCHEMA-LEVEL FUSION
5.1 スキーマレベルの融合

Schema-level fusion unifies the structural backbone of knowledge graphs—concepts, entity types, relations, and attributes—into a coherent and semantically consistent schema. 
スキーマレベルの融合は、知識グラフの構造的バックボーンである概念、エンティティタイプ、関係、属性を一貫性のある意味的に整合したスキーマに統合します。

By aligning heterogeneous elements, it ensures that all knowledge adheres to a unified conceptual specification. 
異種要素を整合させることで、すべての知識が統一された概念仕様に従うことを保証します。

Research in this area has evolved through three major phases. 
この分野の研究は、3つの主要なフェーズを経て進化してきました。

**(1) Ontology-driven consistency. Early work relied on explicit ontologies as global constraints.** 
**（1）オントロジー駆動の整合性。初期の研究は、明示的なオントロジーをグローバルな制約として依存していました。**

For instance, Kommineni et al. (2024) enforced alignment between extracted triples and predefined ontological definitions, achieving high semantic consistency but limited flexibility across domains. 
例えば、Kommineniら（2024）は、抽出されたトリプルとあらかじめ定義されたオントロジー定義との整合性を強制し、高い意味的一貫性を達成しましたが、ドメイン間の柔軟性は限られていました。

**(2) Data-driven unification. To overcome this rigidity, LKD-KGC (Sun et al., 2025) introduced** adaptive, embedding-based schema integration. 
**（2）データ駆動の統合。この硬直性を克服するために、LKD-KGC（Sunら、2025）は、**適応型の埋め込みベースのスキーマ統合を導入しました。

It automatically extracts and merges equivalent entity types via vector clustering and LLM-based deduplication, allowing schema alignment to emerge dynamically from data. 
それは、ベクトルクラスタリングとLLMベースの重複排除を通じて同等のエンティティタイプを自動的に抽出し、マージし、スキーマの整合性がデータから動的に生じることを可能にします。

**(3) LLM-enabled canonicalization. Recent approaches such as EDC (Zhang & Soh, 2024) extend** fusion toward semantic canonicalization. 
**（3）LLM駆動の標準化。最近のアプローチであるEDC（Zhang & Soh、2024）は、**融合を意味的標準化に拡張します。

By prompting LLMs to generate natural language definitions of schema components and comparing them via vector similarity, this method supports both self-alignment and cross-schema mapping with greater automation and semantic precision.  
LLMにスキーマコンポーネントの自然言語定義を生成させ、ベクトル類似性を通じて比較することで、この方法は自己整合とクロススキーママッピングの両方をより自動化され、意味的精度を高めてサポートします。

In summary, schema-level fusion has progressed from ontology-driven to data-driven to LLM**enabled paradigms—marking a shift from rigid rule-based alignment toward flexible, semantics-** oriented fusion mediated by LLM reasoning. 
要約すると、スキーマレベルの融合は、オントロジー駆動からデータ駆動、LLM駆動のパラダイムへと進展しており、LLMの推論によって媒介された柔軟で意味的な融合への移行を示しています。

5.2 INSTANCE-LEVEL FUSION
5.2 インスタンスレベルの融合

Instance-level fusion integrates concrete knowledge instances by addressing entity alignment, dis**ambiguation, deduplication, and conflict resolution. 
インスタンスレベルの融合は、エンティティの整合、曖昧さの解消、重複排除、そして対立解決に取り組むことで具体的な知識インスタンスを統合します。

Its goal is to reconcile heterogeneous or** redundant entities to maintain a coherent and semantically precise knowledge graph. 
その目標は、異種または冗長なエンティティを調整し、一貫性があり意味的に正確な知識グラフを維持することです。

Recent work reflects a clear evolution—from heuristic clustering to structured, reasoning-based frameworks. 
最近の研究は、ヒューリスティッククラスタリングから構造化された推論ベースのフレームワークへの明確な進化を反映しています。

Early studies such as KGGEN (Mo et al., 2025) employed iterative LLM-guided clustering to merge equivalent entities and relations beyond surface matching. 
KGGEN（Moら、2025）などの初期の研究は、表面的なマッチングを超えて同等のエンティティと関係をマージするために、反復的なLLMガイドクラスタリングを使用しました。

The framework performs progressive triple extraction followed by semantic grouping, revealing the potential of LLMs to aggregate semantically related entities through implicit reasoning rather than explicit rules. 
このフレームワークは、進行的なトリプル抽出を行い、その後に意味的グルーピングを行い、LLMが明示的なルールではなく暗黙の推論を通じて意味的に関連するエンティティを集約する可能性を明らかにします。

Later, _LLM-Align (Chen et al., 2024) and EntGPT (Ding et al., 2025) reframed alignment as a contextual_ _reasoning task, using multi-step prompting to enhance semantic discrimination. 
その後、LLM-Align（Chenら、2024）とEntGPT（Dingら、2025）は、整合を文脈的な推論タスクとして再定義し、マルチステッププロンプトを使用して意味的な識別を強化しました。

LLM-Align treats_ alignment as a constrained multiple-choice problem, while EntGPT introduces a two-phase refinement pipeline that first generates candidate entities and then applies targeted reasoning for final selection, significantly improving alignment precision. 
LLM-Alignは整合を制約付きの選択問題として扱い、EntGPTは最初に候補エンティティを生成し、その後にターゲット推論を適用して最終選択を行う2段階の洗練パイプラインを導入し、整合精度を大幅に向上させます。

More recent efforts incorporate structural and retrieval cues—e.g., Pons et al. (2025) leverage RAG-based fusion to exploit class–subclass hierarchies and entity descriptions for zero-shot disambiguation. 
最近の取り組みは、構造的および情報検索の手がかりを組み込んでいます。例えば、Ponsら（2025）は、RAGベースの融合を活用してクラス–サブクラスの階層とエンティティの説明を利用し、ゼロショットの曖昧さの解消を行います。

This integration of graph topology enables more robust reasoning about unseen or ambiguous entities. 
このグラフトポロジーの統合により、見えないまたは曖昧なエンティティに関するより堅牢な推論が可能になります。

Efficiency has also improved through hierarchical designs such as COMEM (Wang et al., 2024), which combines lightweight filtering with fine-grained reasoning. 
効率性は、軽量フィルタリングと細かい推論を組み合わせたCOMEM（Wangら、2024）などの階層的設計を通じて向上しました。



. Efficiency has also improved through hierarchical designs such as COMEM (Wang et al., 2024), which combines lightweight filtering with fine-grained reasoning. 
効率は、軽量フィルタリングと細かい推論を組み合わせたCOMEM（Wang et al., 2024）などの階層的設計を通じて向上しました。

By cascading smaller and larger LLMs in a multi-stage pipeline, it achieves substantial efficiency gains while maintaining high semantic accuracy in large-scale fusion tasks. 
小規模および大規模なLLMをマルチステージパイプラインで連鎖させることにより、大規模な融合タスクにおいて高い意味的精度を維持しながら、かなりの効率向上を達成します。

Overall, LLMs have evolved from simple matchers to adaptive reasoning agents that integrate contextual, structural, and retrieved signals for scalable, self-correcting fusion—paving the way toward autonomous knowledge graph construction. 
全体として、LLMは単純なマッチャーから、スケーラブルで自己修正可能な融合のために文脈的、構造的、取得された信号を統合する適応型推論エージェントへと進化しており、自律的な知識グラフ構築への道を開いています。

5.3 COMPREHENSIVE AND HYBRID FRAMEWORKS
5.3 包括的およびハイブリッドフレームワーク

Comprehensive and hybrid frameworks unify schema-level and instance-level fusion within a single, end-to-end workflow, moving beyond traditional modular pipelines toward integrated, prompt-driven architectures. 
包括的およびハイブリッドフレームワークは、スキーマレベルとインスタンスレベルの融合を単一のエンドツーエンドのワークフロー内で統合し、従来のモジュラー・パイプラインを超えて統合されたプロンプト駆動のアーキテクチャへと移行します。

The KARMA framework (Lu & Wang, 2025) exemplifies a multi-agent design where specialized agents collaboratively handle schema alignment, conflict resolution, and quality evaluation, achieving scalability and global consistency. 
KARMAフレームワーク（Lu & Wang, 2025）は、専門のエージェントが共同でスキーマの整合、対立の解決、品質評価を行い、スケーラビリティとグローバルな一貫性を達成するマルチエージェント設計の例です。

Building on this, ODKE+ (Khorshidi et al., 2025) employs an ontology-guided workflow coupling schema supervision with instance-level corroboration for improved semantic fidelity. 
これを基に、ODKE+（Khorshidi et al., 2025）は、スキーマの監視とインスタンスレベルの確認を結びつけたオントロジー指向のワークフローを採用し、意味的忠実性を向上させます。

More recently, Graphusion (Yang et al., 2024) introduces a unified, prompt-based paradigm that performs all fusion subtasks—alignment, consolidation, and inference—within a single generative cycle. 
最近では、Graphusion（Yang et al., 2024）が、すべての融合サブタスク（整合、統合、推論）を単一の生成サイクル内で実行する統一されたプロンプトベースのパラダイムを導入しました。

Together, these frameworks signal a shift toward integrated, adaptive, and generative fusion systems, marking a crucial step toward autonomous, self-evolving knowledge graphs capable of continuous construction and reasoning in LLM-driven ecosystems. 
これらのフレームワークは、統合された適応型および生成型の融合システムへの移行を示しており、LLM駆動のエコシステムにおける継続的な構築と推論が可能な自律的で自己進化する知識グラフへの重要なステップを示しています。

#### 6 FUTURE APPLICATIONS
#### 6 将来の応用

Research at the intersection of Large Language Models (LLMs) and Knowledge Graphs (KGs) is progressively advancing toward deeper intelligent interaction and greater autonomy in knowledge representation and reasoning. 
大規模言語モデル（LLM）と知識グラフ（KG）の交差点における研究は、知識の表現と推論におけるより深い知的相互作用とより大きな自律性に向けて進展しています。

In light of these developments, several promising directions are emerging for future exploration.  
これらの進展を受けて、将来の探求に向けたいくつかの有望な方向性が浮上しています。

6.1 KNOWLEDGE GRAPH-BASED REASONING FOR LLMS
6.1 LLMのための知識グラフに基づく推論

Future work is expected to further integrate structured KGs into the reasoning mechanisms of LLMs, enhancing their logical consistency, causal inference, and interpretability. 
今後の研究では、構造化されたKGをLLMの推論メカニズムにさらに統合し、論理的一貫性、因果推論、解釈可能性を向上させることが期待されています。

This research direction signifies not only an improvement in reasoning capabilities but also a conceptual transition from _knowledge construction to knowledge-driven reasoning. 
この研究の方向性は、推論能力の向上だけでなく、_知識構築から知識駆動の推論への概念的な移行を示しています。

High-quality, well-structured KGs will provide the foundation for explainable and verifiable model inference. 
高品質でよく構造化されたKGは、説明可能で検証可能なモデル推論の基盤を提供します。

Existing studies such as KG_based Random-Walk Reasoning (Kim et al., 2024) and KG-RAR (Wu et al., 2025) have demonstrated the potential of this paradigm. 
KG_based Random-Walk Reasoning（Kim et al., 2024）やKG-RAR（Wu et al., 2025）などの既存の研究は、このパラダイムの可能性を示しています。

A crucial complementary challenge, however, lies in how enhanced reasoning abilities can in turn support more robust and automated KG construction—forming a self-improving, virtuous cycle between knowledge building and reasoning. 
しかし、重要な補完的な課題は、強化された推論能力がどのようにしてより堅牢で自動化されたKG構築を支援できるかにあり、知識構築と推論の間に自己改善の好循環を形成することです。

6.2 DYNAMIC KNOWLEDGE MEMORY FOR AGENTIC SYSTEMS
6.2 エージェントシステムのための動的知識メモリ

Achieving autonomy in LLM-powered agents requires overcoming the limits of finite context windows through persistent, structured memory. 
LLM駆動のエージェントにおける自律性を達成するには、持続的で構造化されたメモリを通じて有限のコンテキストウィンドウの限界を克服する必要があります。

Recent architectures envision the knowledge graph **(KG) as a dynamic memory substrate, evolving continuously with agent interactions rather than** storing static histories. 
最近のアーキテクチャは、知識グラフ**（KG）を動的メモリ基盤として想定し、静的な履歴を保存するのではなく、エージェントの相互作用とともに継続的に進化します。**

Frameworks such as A-MEM (Xu et al., 2025) model memory as interconnected “notes” enriched with contextual metadata, enabling continual reorganization and growth. 
A-MEM（Xu et al., 2025）などのフレームワークは、メモリを文脈メタデータで強化された相互接続された「ノート」としてモデル化し、継続的な再編成と成長を可能にします。

Similarly, Zep (Rasmussen et al., 2025) employs a temporal knowledge graph (TKG) to manage fact validity and support time-aware reasoning and updates. 
同様に、Zep（Rasmussen et al., 2025）は、事実の妥当性を管理し、時間を意識した推論と更新をサポートするために時間的知識グラフ（TKG）を使用します。

These advances highlight dynamic KGs as long-term, interpretable memory systems that enable continuous learning, multi-agent collaboration, and self-reflective reasoning. 
これらの進展は、動的KGを長期的で解釈可能なメモリシステムとして強調し、継続的な学習、マルチエージェントのコラボレーション、自己反省的な推論を可能にします。

Future work will focus on improving scalability, temporal coherence, and multimodal integration for fully autonomous, knowledge-grounded agents. 
今後の研究は、完全に自律的で知識に基づくエージェントのために、スケーラビリティ、時間的一貫性、マルチモーダル統合の改善に焦点を当てます。

6.3 MULTIMODAL KNOWLEDGE GRAPH CONSTRUCTION
6.3 マルチモーダル知識グラフ構築

Multimodal Knowledge Graph (MMKG) construction aims to integrate heterogeneous modalities—such as text, images, audio, and video—into unified, structured representations that enable richer reasoning and cross-modal alignment. 
マルチモーダル知識グラフ（MMKG）構築は、テキスト、画像、音声、動画などの異種モダリティを統合し、より豊かな推論とクロスモーダル整合を可能にする統一された構造化表現を目指します。

Representative work includes VaLiK (Vision-alignto-Language integrated KG) (Liu et al., 2025), which cascades pretrained Vision-Language Models (VLMs) to translate visual features into textual form, followed by a cross-modal verification module to filter noise and assemble MMKGs. 
代表的な研究には、視覚特徴をテキスト形式に変換するために事前学習された視覚言語モデル（VLM）を連鎖させ、ノイズをフィルタリングしてMMKGを構築するためのクロスモーダル検証モジュールを持つVaLiK（Vision-alignto-Language integrated KG）（Liu et al., 2025）が含まれます。

This process achieves entity–image linkage without manual annotation. 
このプロセスは、手動アノテーションなしでエンティティと画像のリンクを実現します。

Beyond structure, representation learning methods such as KG-MRI (Lu et al., 2024) employ multimodal embeddings with contrastive objectives to align heterogeneous modalities into coherent semantic spaces. 
構造を超えて、KG-MRI（Lu et al., 2024）などの表現学習手法は、対照的な目的を持つマルチモーダル埋め込みを使用して、異種モダリティを一貫した意味空間に整合させます。

Key challenges remain in modality heterogeneity, alignment noise, scalability, and robustness under missing or imbalanced modalities. 
モダリティの異質性、整合ノイズ、スケーラビリティ、欠落または不均衡なモダリティに対する堅牢性に関する重要な課題が残っています。

As LLMs and VLMs continue to co-evolve, MMKGs will become a cornerstone for bridging perceptual input and symbolic reasoning across modalities. 
LLMとVLMが共進化し続ける中で、MMKGはモダリティ間の知覚入力と象徴的推論をつなぐ基盤となるでしょう。

6.4 NEW ROLES FOR KGS IN LLM APPLICATIONS: BEYOND RAG
6.4 LLMアプリケーションにおけるKGの新しい役割：RAGを超えて

Beyond their use as retrieval backbones in RAG systems, Knowledge Graphs (KGs) are increasingly envisioned as a cognitive middle layer bridging raw input and LLM reasoning. 
RAGシステムにおける検索バックボーンとしての使用を超えて、知識グラフ（KG）は、生の入力とLLMの推論をつなぐ認知的中間層としてますます想定されています。

In this paradigm, KGs provide a structured scaffold for querying, planning, and decision-making, enabling more interpretable and grounded generation. 
このパラダイムにおいて、KGはクエリ、計画、意思決定のための構造化された足場を提供し、より解釈可能で基盤のある生成を可能にします。

Recent studies illustrate this shift. 
最近の研究はこのシフトを示しています。

CogER (Bing et al., 2023) formulates recommendation as cognition-aware KG reasoning, integrating intuitive and pathbased inference for explainability. 
CogER（Bing et al., 2023）は、推薦を認知を意識したKG推論として定式化し、説明可能性のために直感的かつ経路ベースの推論を統合しています。

In the biomedical domain, PKG-LLM (Sarabadani et al., 2025) employs domain KGs for knowledge augmentation and predictive modeling in mental health diagnostics. 
バイオメディカル領域では、PKG-LLM（Sarabadani et al., 2025）が、知識の拡張とメンタルヘルス診断における予測モデリングのためにドメインKGを使用しています。

Together, these approaches treat the KG as an interactive reasoning substrate, promising more robust and explainable generation in domains such as science, code, and healthcare. 
これらのアプローチは、KGをインタラクティブな推論基盤として扱い、科学、コード、ヘルスケアなどの分野でより堅牢で説明可能な生成を約束します。

#### 7 CONCLUSION
#### 7 結論

This survey presents a comprehensive overview of how Large Language Models (LLMs) are transforming Knowledge Graph (KG) construction across ontology engineering, knowledge extraction, and knowledge fusion. 
この調査は、大規模言語モデル（LLM）がオントロジー工学、知識抽出、知識融合における知識グラフ（KG）構築をどのように変革しているかの包括的な概要を示しています。

LLMs shift the paradigm from rule-based and modular pipelines toward unified, adaptive, and generative frameworks. 
LLMは、ルールベースおよびモジュラー・パイプラインから統一された適応型および生成型フレームワークへのパラダイムをシフトさせます。

Across these stages, three trends emerge: (1) the evolution from static schemas to dynamic induction, (2) the integration of pipeline modularity into _generative unification, and (3) the transition from symbolic rigidity to semantic adaptability. 
これらの段階を通じて、次の3つのトレンドが浮上します：（1）静的スキーマから動的誘導への進化、（2）パイプラインのモジュール性を_生成的統合に統合すること、（3）象徴的な硬直性から意味的適応性への移行です。

Together, these shifts redefine KGs as living, cognitive infrastructures that blend language understanding with structured reasoning. 
これらのシフトは、KGを言語理解と構造化された推論を融合させた生きた認知インフラストラクチャとして再定義します。

Despite remarkable progress, challenges remain in scalability, reliability, and continual adaptation. 
顕著な進展があったにもかかわらず、スケーラビリティ、信頼性、継続的な適応に関する課題が残っています。

Future advances in prompt design, multimodal integration, and _knowledge-grounded reasoning will be key to realizing autonomous and explainable knowledge-_ **centric AI systems.**
今後のプロンプト設計、マルチモーダル統合、_知識に基づく推論の進展が、自律的で説明可能な知識中心のAIシステムを実現するための鍵となるでしょう。

#### REFERENCES
#### 参考文献

Muhammad Nabeel Asim, Muhammad Wasim, Muhammad Usman Ghani Khan, Waqar Mahmood, and Hafiza Mahnoor Abbasi. A survey of ontology learning techniques and applications. 
Muhammad Nabeel Asim、Muhammad Wasim、Muhammad Usman Ghani Khan、Waqar Mahmood、およびHafiza Mahnoor Abbasi。オントロジー学習技術と応用に関する調査。  
_Database, 2018:bay101, 2018._  
_データベース、2018:bay101、2018。_

Jiaxin Bai, Wei Fan, Qi Hu, Qing Zong, Chunyang Li, Hong Ting Tsang, Hongyu Luo, Yauwai Yim, Haoyu Huang, Xiao Zhou, Feng Qin, Tianshi Zheng, Xi Peng, Xin Yao, Huiwen Yang, Leijie Wu, Yi Ji, Gong Zhang, Renhai Chen, and Yangqiu Song. AutoSchemaKG: Autonomous Knowledge Graph Construction through Dynamic Schema Induction from Web-Scale Corpora. 
Jiaxin Bai、Wei Fan、Qi Hu、Qing Zong、Chunyang Li、Hong Ting Tsang、Hongyu Luo、Yauwai Yim、Haoyu Huang、Xiao Zhou、Feng Qin、Tianshi Zheng、Xi Peng、Xin Yao、Huiwen Yang、Leijie Wu、Yi Ji、Gong Zhang、Renhai Chen、およびYangqiu Song。AutoSchemaKG：Webスケールコーパスからの動的スキーマ誘導による自律的知識グラフ構築。  
_[arXiv preprint arXiv:2505.23628, aug 2025. doi: 10.48550/arXiv.2505.23628. URL http:](http://arxiv.org/abs/2505.23628)_  
_[arXivプレプリントarXiv:2505.23628、2025年8月。doi: 10.48550/arXiv.2505.23628。URL http:](http://arxiv.org/abs/2505.23628)_

Kriti Bhattarai, Inez Y. Oh, Zachary B. Abrams, and Albert M. Lai. Document-level Clinical Entity and Relation extraction via Knowledge Base-Guided Generation. 
Kriti Bhattarai、Inez Y. Oh、Zachary B. Abrams、およびAlbert M. Lai。知識ベースガイド生成による文書レベルの臨床エンティティと関係の抽出。  
In Proceedings of the 23rd _Workshop on Biomedical Natural Language Processing, pp. 318–327, Bangkok, Thailand, 2024._  
_第23回バイオメディカル自然言語処理ワークショップの議事録、pp. 318–327、タイ、バンコク、2024年。_

[Association for Computational Linguistics. doi: 10.18653/v1/2024.bionlp-1.24. URL https:](https://aclanthology.org/2024.bionlp-1.24)  
[計算言語学協会。doi: 10.18653/v1/2024.bionlp-1.24。URL https:](https://aclanthology.org/2024.bionlp-1.24)

Qingyu Bing, Qiannan Zhu, and Zhicheng Dou. Cognition-aware Knowledge Graph Reasoning for Explainable Recommendation. 
Qingyu Bing、Qiannan Zhu、およびZhicheng Dou。説明可能な推薦のための認知を意識した知識グラフ推論。  
In Proceedings of the Sixteenth ACM International Conference on _Web Search and Data Mining, pp. 402–410, Singapore, Singapore, feb 2023. ACM. doi: 10.1145/_  
[3539597.3570391. URL https://dl.acm.org/doi/10.1145/3539597.3570391.](https://dl.acm.org/doi/10.1145/3539597.3570391)

Xuan Chen, Tong Lu, and Zhichun Wang. LLM-Align: Utilizing Large Language Models for Entity Alignment in Knowledge Graphs. 
Xuan Chen、Tong Lu、およびZhichun Wang。LLM-Align：知識グラフにおけるエンティティ整合のための大規模言語モデルの活用。  
arXiv preprint arXiv:2412.04690, dec 2024. doi: 10.48550/  
[arXiv.2412.04690. URL http://arxiv.org/abs/2412.04690.](http://arxiv.org/abs/2412.04690)

Kartik Detroja, CK Bhensdadia, and Brijesh S Bhatt. A survey on relation extraction. 
Kartik Detroja、CK Bhensdadia、およびBrijesh S Bhatt。関係抽出に関する調査。  
Intelligent _Systems with Applications, 19:200244, 2023._  
_応用に関するインテリジェントシステム、19:200244、2023。_

Yifan Ding, Amrit Poudel, Qingkai Zeng, Tim Weninger, Balaji Veeramani, and Sanmitra Bhattacharya. EntGPT: Entity Linking with Generative Large Language Models. 
Yifan Ding、Amrit Poudel、Qingkai Zeng、Tim Weninger、Balaji Veeramani、およびSanmitra Bhattacharya。EntGPT：生成的な大規模言語モデルによるエンティティリンク。  
_arXiv preprint_ _[arXiv:2402.06738, may 2025. doi: 10.48550/arXiv.2402.06738. URL http://arxiv.org/](http://arxiv.org/abs/2402.06738)_  
_[arXivプレプリントarXiv:2402.06738、2025年5月。doi: 10.48550/arXiv.2402.06738。URL http://arxiv.org/](http://arxiv.org/abs/2402.06738)_

Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, and Jonathan Larson. From Local to Global: A Graph RAG Approach to Query-Focused Summarization. 
Darren Edge、Ha Trinh、Newman Cheng、Joshua Bradley、Alex Chao、Apurva Mody、Steven Truitt、およびJonathan Larson。ローカルからグローバルへ：クエリ焦点の要約に対するグラフRAGアプローチ。  
arXiv preprint arXiv:2404.16130, apr 2024. doi: 10.48550/arXiv.2404.16130. URL [http://arxiv.org/abs/2404.16130.](http://arxiv.org/abs/2404.16130)

Nadeen Fathallah, Steffen Staab, and Alsayed Algergawy. LLMs4Life: Large Language Models for Ontology Learning in Life Sciences. 
Nadeen Fathallah、Steffen Staab、およびAlsayed Algergawy。LLMs4Life：ライフサイエンスにおけるオントロジー学習のための大規模言語モデル。  
arXiv preprint arXiv:2412.02035, dec 2024. doi: 10.48550/  



. LLMs4Life: Large Language Models for Ontology Learning in Life Sciences. arXiv preprint arXiv:2412.02035, dec 2024. doi: 10.48550/ [arXiv.2412.02035. URL http://arxiv.org/abs/2412.02035.](http://arxiv.org/abs/2412.02035)
. LLMs4Life: 生命科学におけるオントロジー学習のための大規模言語モデル。arXivプレプリント arXiv:2412.02035、2024年12月。doi: 10.48550/ [arXiv.2412.02035。URL http://arxiv.org/abs/2412.02035。](http://arxiv.org/abs/2412.02035)

Nadeen Fathallah, Arunav Das, Stefano De Giorgis, Andrea Poltronieri, Peter Haase, and Liubov Kovriguina. NeOn-GPT: A Large Language Model-Powered Pipeline for Ontology Learning.
ナディーン・ファタラ、アルナヴ・ダス、ステファノ・デ・ジョルジス、アンドレア・ポルトロニエリ、ピーター・ハーゼ、リュボフ・コブリギナ。NeOn-GPT: オントロジー学習のための大規模言語モデル駆動のパイプライン。

In Albert Mero˜no Pe˜nuela, Oscar Corcho, Paul Groth, Elena Simperl, Valentina Tamma, Andrea Giovanni Nuzzolese, Maria Poveda-Villal´on, Marta Sabou, Valentina Presutti, Irene Celino, Artem Revenko, Joe Raad, Bruno Sartini, and Pasquale Lisena (eds.), The Semantic Web: ESWC _2024 Satellite Events, volume 15344, pp. 36–50. Springer Nature Switzerland, Cham, 2025._ doi: 10.1007/978-3-031-78952-6 4. [URL https://link.springer.com/10.1007/](https://link.springer.com/10.1007/978-3-031-78952-6_4) [978-3-031-78952-6_4.](https://link.springer.com/10.1007/978-3-031-78952-6_4)  
アルバート・メローノ・ペヌエラ、オスカー・コルチョ、ポール・グロース、エレナ・シンペルル、バレンティーナ・タマ、アンドレア・ジョバンニ・ヌッツォレゼ、マリア・ポベダ・ビジャロン、マルタ・サブ、バレンティーナ・プレスッティ、アイリーン・セリーノ、アルテム・レヴェンコ、ジョー・ラード、ブルーノ・サルティーニ、パスカーレ・リセナ（編）、セマンティックウェブ: ESWC _2024 サテライトイベント、ボリューム 15344、pp. 36–50。スプリンガー・ネイチャー・スイス、シャム、2025年。_ doi: 10.1007/978-3-031-78952-6 4。[URL https://link.springer.com/10.1007/](https://link.springer.com/10.1007/978-3-031-78952-6_4) [978-3-031-78952-6_4。](https://link.springer.com/10.1007/978-3-031-78952-6_4)

Xiaohan Feng, Xixin Wu, and Helen Meng. Ontology-grounded Automatic Knowledge Graph Construction by LLM under Wikidata schema. arXiv preprint arXiv:2412.20942, dec 2024. doi: [10.48550/arXiv.2412.20942. URL http://arxiv.org/abs/2412.20942.](http://arxiv.org/abs/2412.20942)
シャオハン・フェン、シーシン・ウー、ヘレン・メン。Wikidataスキーマに基づくLLMによるオントロジーに基づく自動知識グラフ構築。arXivプレプリント arXiv:2412.20942、2024年12月。doi: [10.48550/arXiv.2412.20942。URL http://arxiv.org/abs/2412.20942。](http://arxiv.org/abs/2412.20942)

Hamed Babaei Giglou, Jennifer D’Souza, and S¨oren Auer. LLMs4OL: Large Language Models for Ontology Learning. arXiv preprint arXiv:2307.16648, aug 2023. doi: 10.48550/arXiv.2307. [16648. URL http://arxiv.org/abs/2307.16648.](http://arxiv.org/abs/2307.16648)
ハメド・ババエイ・ギグル、ジェニファー・D・ソウザ、ソーレン・アウアー。LLMs4OL: オントロジー学習のための大規模言語モデル。arXivプレプリント arXiv:2307.16648、2023年8月。doi: 10.48550/arXiv.2307. [16648。URL http://arxiv.org/abs/2307.16648。](http://arxiv.org/abs/2307.16648)

Samira Khorshidi, Azadeh Nikfarjam, Suprita Shankar, Yisi Sang, Yash Govind, Hyun Jang, Ali Kasgari, Alexis McClimans, Mohamed Soliman, Vishnu Konda, Ahmed Fakhry, and Xiaoguang Qi. ODKE+: Ontology-Guided Open-Domain Knowledge Extraction with LLMs. arXiv preprint _[arXiv:2509.04696, sep 2025. doi: 10.48550/arXiv.2509.04696. URL http://arxiv.org/](http://arxiv.org/abs/2509.04696)_ [abs/2509.04696.](http://arxiv.org/abs/2509.04696)
サミラ・コルシディ、アザデ・ニクファルジャム、スプリタ・シャンカール、イシ・サン、ヤシュ・ゴビンド、ヒョン・ジャン、アリ・カスガリ、アレクシス・マククリマンズ、モハメド・ソリマン、ヴィシュヌ・コンダ、アフメド・ファクリー、シャオグアン・チー。ODKE+: LLMによるオントロジー指導のオープンドメイン知識抽出。arXivプレプリント _[arXiv:2509.04696、2025年9月。doi: 10.48550/arXiv.2509.04696。URL http://arxiv.org/](http://arxiv.org/abs/2509.04696)_ [abs/2509.04696。](http://arxiv.org/abs/2509.04696)

Yejin Kim, Eojin Kang, Juae Kim, and H. Howie Huang. Causal Reasoning in Large Language Models: A Knowledge Graph Approach. arXiv preprint arXiv:2410.11588, oct 2024. doi: 10. [48550/arXiv.2410.11588. URL http://arxiv.org/abs/2410.11588.](http://arxiv.org/abs/2410.11588)
イェジン・キム、エオジン・カン、ジュエ・キム、H・ハウイー・ファン。大規模言語モデルにおける因果推論: 知識グラフアプローチ。arXivプレプリント arXiv:2410.11588、2024年10月。doi: 10. [48550/arXiv.2410.11588。URL http://arxiv.org/abs/2410.11588。](http://arxiv.org/abs/2410.11588)

Vamsi Krishna Kommineni, Birgitta K¨onig-Ries, and Sheeba Samuel. Towards the automation of knowledge graph construction using large language models. Journal Name, 2024.
ヴァムシ・クリシュナ・コミネニ、ビルギッタ・ケーニッヒ＝リース、シーバ・サミュエル。大規模言語モデルを使用した知識グラフ構築の自動化に向けて。ジャーナル名、2024年。

Konstantinos I. Kotis, George A. Vouros, and Dimitris Spiliotopoulos. Ontology engineering methodologies for the evolution of living and reused ontologies: status, trends, findings and recommendations. _The Knowledge Engineering Review, 35:e4, 2020._ doi: 10.1017/ S0269888920000065.
コンスタンティノス・I・コティス、ジョージ・A・ヴーロス、ディミトリス・スピリオトポウロス。生きたオントロジーと再利用されたオントロジーの進化のためのオントロジー工学の方法論: 状況、傾向、発見と推奨。_知識工学レビュー、35:e4、2020年。_ doi: 10.1017/ S0269888920000065。

Anna Sofia Lippolis, Miguel Ceriani, Sara Zuppiroli, and Andrea Giovanni Nuzzolese. Ontogenia: Ontology Generation with Metacognitive Prompting in Large Language Models. In Albert Mero˜no Pe˜nuela, Oscar Corcho, Paul Groth, Elena Simperl, Valentina Tamma, Andrea Giovanni Nuzzolese, Maria Poveda-Villal´on, Marta Sabou, Valentina Presutti, Irene Celino, Artem Revenko, Joe Raad, Bruno Sartini, and Pasquale Lisena (eds.), The Semantic Web: ESWC _2024 Satellite Events, volume 15344, pp. 259–265. Springer Nature Switzerland, Cham, 2025a._ [doi: 10.1007/978-3-031-78952-6 38. URL https://link.springer.com/10.1007/](https://link.springer.com/10.1007/978-3-031-78952-6_38) [978-3-031-78952-6_38.](https://link.springer.com/10.1007/978-3-031-78952-6_38)
アンナ・ソフィア・リッポリス、ミゲル・セリアーニ、サラ・ズッピロリ、アンドレア・ジョバンニ・ヌッツォレゼ。Ontogenia: 大規模言語モデルにおけるメタ認知的プロンプティングを用いたオントロジー生成。アルバート・メローノ・ペヌエラ、オスカー・コルチョ、ポール・グロース、エレナ・シンペルル、バレンティーナ・タマ、アンドレア・ジョバンニ・ヌッツォレゼ、マリア・ポベダ・ビジャロン、マルタ・サブ、バレンティーナ・プレスッティ、アイリーン・セリーノ、アルテム・レヴェンコ、ジョー・ラード、ブルーノ・サルティーニ、パスカーレ・リセナ（編）、セマンティックウェブ: ESWC _2024 サテライトイベント、ボリューム 15344、pp. 259–265。スプリンガー・ネイチャー・スイス、シャム、2025年。_ [doi: 10.1007/978-3-031-78952-6 38。URL https://link.springer.com/10.1007/](https://link.springer.com/10.1007/978-3-031-78952-6_38) [978-3-031-78952-6_38。](https://link.springer.com/10.1007/978-3-031-78952-6_38)

Anna Sofia Lippolis, Mohammad Javad Saeedizade, Robin Keskis¨arkk¨a, Sara Zuppiroli, Miguel Ceriani, Aldo Gangemi, Eva Blomqvist, and Andrea Giovanni Nuzzolese. Ontology Generation using Large Language Models. arXiv preprint arXiv:2503.05388, mar 2025b. doi: 10.48550/ [arXiv.2503.05388. URL http://arxiv.org/abs/2503.05388.](http://arxiv.org/abs/2503.05388)
アンナ・ソフィア・リッポリス、モハマド・ジャヴァド・サイーディザーデ、ロビン・ケスキサルッカ、サラ・ズッピロリ、ミゲル・セリアーニ、アルド・ガンジェミ、エヴァ・ブロムクヴィスト、アンドレア・ジョバンニ・ヌッツォレゼ。大規模言語モデルを用いたオントロジー生成。arXivプレプリント arXiv:2503.05388、2025年3月。doi: 10.48550/ [arXiv.2503.05388。URL http://arxiv.org/abs/2503.05388。](http://arxiv.org/abs/2503.05388)

Junming Liu, Siyuan Meng, Yanting Gao, Song Mao, Pinlong Cai, Guohang Yan, Yirong Chen, Zilin Bian, Ding Wang, and Botian Shi. Aligning Vision to Language: Annotation-Free Multimodal Knowledge Graph Construction for Enhanced LLMs Reasoning. _arXiv preprint_ _[arXiv:2503.12972, jul 2025. doi: 10.48550/arXiv.2503.12972. URL http://arxiv.org/](http://arxiv.org/abs/2503.12972)_ [abs/2503.12972.](http://arxiv.org/abs/2503.12972)
ジュンミン・リウ、シーユアン・メン、ヤンティン・ガオ、ソン・マオ、ピンロン・ツァイ、グオハン・ヤン、イーロン・チェン、ズリン・ビアン、ディン・ワン、ボティアン・シー。視覚と言語の整合: 強化されたLLMs推論のための注釈なしのマルチモーダル知識グラフ構築。_arXivプレプリント_ _[arXiv:2503.12972、2025年7月。doi: 10.48550/arXiv.2503.12972。URL http://arxiv.org/](http://arxiv.org/abs/2503.12972)_ [abs/2503.12972。](http://arxiv.org/abs/2503.12972)

Shuang Liu, Man Xu, Yufeng Qin, and Niko Lukaˇc. Knowledge graph alignment network with node-level strong fusion. Applied Sciences, 12(19), 2022. doi: 10.3390/app12199434. URL [https://www.mdpi.com/2076-3417/12/19/9434.](https://www.mdpi.com/2076-3417/12/19/9434)
シュアン・リウ、マン・シュー、ユーフェン・チン、ニコ・ルカチ。ノードレベルの強い融合を持つ知識グラフ整合ネットワーク。応用科学、12(19)、2022年。doi: 10.3390/app12199434。URL [https://www.mdpi.com/2076-3417/12/19/9434。](https://www.mdpi.com/2076-3417/12/19/9434)

Yuxing Lu and Jinzhuo Wang. KARMA: Leveraging Multi-Agent LLMs for Automated Knowledge Graph Enrichment. arXiv preprint arXiv:2502.06472, feb 2025. doi: 10.48550/arXiv.2502.06472. [URL http://arxiv.org/abs/2502.06472.](http://arxiv.org/abs/2502.06472)
ユシン・ルー、ジンジュオ・ワン。KARMA: 自動知識グラフ強化のためのマルチエージェントLLMsの活用。arXivプレプリント arXiv:2502.06472、2025年2月。doi: 10.48550/arXiv.2502.06472。 [URL http://arxiv.org/abs/2502.06472。](http://arxiv.org/abs/2502.06472)

Yuxing Lu, Weichen Zhao, Nan Sun, and Jinzhuo Wang. Enhancing multimodal knowledge graph representation learning through triple contrastive learning. In Kate Larson (ed.), Proceedings of _the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI-24, pp. 5963–_ 5971. International Joint Conferences on Artificial Intelligence Organization, aug 2024. doi: [10.24963/ijcai.2024/659. URL https://doi.org/10.24963/ijcai.2024/659. Main](https://doi.org/10.24963/ijcai.2024/659) Track.  
ユシン・ルー、ウェイチェン・ジャオ、ナン・サン、ジンジュオ・ワン。トリプルコントラスト学習を通じたマルチモーダル知識グラフ表現学習の強化。ケイト・ラーソン（編）、_第33回国際共同人工知能会議、IJCAI-24の議事録、pp. 5963–5971。国際共同人工知能会議機構、2024年8月。doi: [10.24963/ijcai.2024/659。URL https://doi.org/10.24963/ijcai.2024/659。メイン](https://doi.org/10.24963/ijcai.2024/659) トラック。

Patricia Mateiu and Adrian Groza. Ontology engineering with Large Language Models. arXiv _[preprint arXiv:2307.16699, jul 2023. doi: 10.48550/arXiv.2307.16699. URL http://arxiv.](http://arxiv.org/abs/2307.16699)_ [org/abs/2307.16699.](http://arxiv.org/abs/2307.16699)
パトリシア・マテイウ、アドリアン・グロザ。大規模言語モデルを用いたオントロジー工学。arXiv _[プレプリント arXiv:2307.16699、2023年7月。doi: 10.48550/arXiv.2307.16699。URL http://arxiv.](http://arxiv.org/abs/2307.16699)_ [org/abs/2307.16699。](http://arxiv.org/abs/2307.16699)

Belinda Mo, Kyssen Yu, Joshua Kazdan, Proud Mpala, Lisa Yu, Chris Cundy, Charilaos Kanatsoulis, and Sanmi Koyejo. KGGen: Extracting Knowledge Graphs from Plain Text with Language Models. arXiv preprint arXiv:2502.09956, feb 2025. doi: 10.48550/arXiv.2502.09956. [URL http://arxiv.org/abs/2502.09956.](http://arxiv.org/abs/2502.09956)
ベリンダ・モ、キッセン・ユー、ジョシュア・カズダン、プラウド・ムパラ、リサ・ユー、クリス・カンディ、チャリラオス・カナツオリス、サンミ・コイエジョ。KGGen: 言語モデルを用いた平文からの知識グラフの抽出。arXivプレプリント arXiv:2502.09956、2025年2月。doi: 10.48550/arXiv.2502.09956。 [URL http://arxiv.org/abs/2502.09956。](http://arxiv.org/abs/2502.09956)

Jixuan Nie, Xia Hou, Wenfeng Song, Xuan Wang, Xinyu Zhang, Xingliang Jin, Shuozhe Zhang, and Jiaqi Shi. Knowledge graph efficient construction: Embedding chain-of-thought into llms. _Proceedings of the VLDB Endowment. ISSN, 2150:8097, 2024._
ジクシャン・ニエ、シャ・ホウ、ウェンフェン・ソン、シュアン・ワン、シンユ・チャン、シンリャン・ジン、シュオジェ・チャン、ジャーキ・シー。知識グラフの効率的な構築: LLMにおける思考の連鎖の埋め込み。_VLDBエンダウメントの議事録。ISSN、2150:8097、2024年。_

Liu Pai, Wenyang Gao, Wenjie Dong, Lin Ai, Ziwei Gong, Songfang Huang, Li Zongsheng, Ehsan Hoque, Julia Hirschberg, and Yue Zhang. A survey on open information extraction from rule-based model to large language model. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (eds.), Findings of the Association for Computational Linguistics: EMNLP _2024, pp. 9586–9608, Miami, Florida, USA, 2024. Association for Computational Linguistics._ [doi: 10.18653/v1/2024.findings-emnlp.560. URL https://aclanthology.org/2024.](https://aclanthology.org/2024.findings-emnlp.560/) [findings-emnlp.560/.](https://aclanthology.org/2024.findings-emnlp.560/)
リウ・パイ、ウェンヤン・ガオ、ウェンジー・ドン、リン・アイ、ズイウェイ・ゴン、ソンファン・ファン、リ・ゾンシェン、エフサン・ホーク、ジュリア・ヒルシュバーグ、ユエ・ジャン。ルールベースモデルから大規模言語モデルへのオープン情報抽出に関する調査。ヤーセル・アル・オナイザン、モヒット・バンサル、ユン・ナン・チェン（編）、計算言語学会の発見: EMNLP _2024、pp. 9586–9608、マイアミ、フロリダ、アメリカ、2024年。計算言語学会。_ [doi: 10.18653/v1/2024.findings-emnlp.560。URL https://aclanthology.org/2024。](https://aclanthology.org/2024.findings-emnlp.560/) [findings-emnlp.560。](https://aclanthology.org/2024.findings-emnlp.560/)

Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and Xindong Wu. Unifying large language models and knowledge graphs: A roadmap. IEEE Transactions on Knowledge and Data _Engineering, 36(7):3580–3599, 2024._
シルイ・パン、リンハオ・ルオ、ユーフェイ・ワン、チェン・チェン、ジアプ・ワン、シンドン・ウー。大規模言語モデルと知識グラフの統合: ロードマップ。IEEEトランザクションズ・オン・ナレッジ・アンド・データ _エンジニアリング、36(7):3580–3599、2024年。_

Andrea Papaluca, Daniel Krefl, Sergio Rodr´ıguez M´endez, Artem Lensky, and Hanna Suominen. Zero- and Few-Shots Knowledge Graph Triplet Extraction with Large Language Models. In _Proceedings of the 1st Workshop on Knowledge Graphs and Large Language Models (KaLLM_ _2024), pp. 12–23, Bangkok, Thailand, 2024. Association for Computational Linguistics. doi:_ [10.18653/v1/2024.kallm-1.2. URL https://aclanthology.org/2024.kallm-1.2.](https://aclanthology.org/2024.kallm-1.2)
アンドレア・パパルカ、ダニエル・クレフル、セルヒオ・ロドリゲス・メンデス、アルテム・レンスキー、ハンナ・スオミネン。大規模言語モデルを用いたゼロショットおよび少数ショットの知識グラフ三重抽出。_知識グラフと大規模言語モデルに関する第1回ワークショップの議事録 (KaLLM_ _2024)、pp. 12–23、バンコク、タイ、2024年。計算言語学会。doi:_ [10.18653/v1/2024.kallm-1.2。URL https://aclanthology.org/2024.kallm-1.2。](https://aclanthology.org/2024.kallm-1.2)

Gerard Pons, Besim Bilalli, and Anna Queralt. Knowledge Graphs for Enhancing Large Language Models in Entity Disambiguation. arXiv preprint arXiv:2505.02737, pp. 162–179, 2025. doi: [10.1007/978-3-031-77844-5 9. URL http://arxiv.org/abs/2505.02737.](http://arxiv.org/abs/2505.02737)
ジェラード・ポンズ、ベシム・ビラリ、アンナ・クエラルト。エンティティの曖昧さ解消における大規模言語モデルを強化するための知識グラフ。arXivプレプリント arXiv:2505.02737、pp. 162–179、2025年。doi: [10.1007/978-3-031-77844-5 9。URL http://arxiv.org/abs/2505.02737。](http://arxiv.org/abs/2505.02737)

Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: A Temporal Knowledge Graph Architecture for Agent Memory. arXiv preprint arXiv:2501.13956, [jan 2025. doi: 10.48550/arXiv.2501.13956. URL http://arxiv.org/abs/2501.13956.](http://arxiv.org/abs/2501.13956)
プレストン・ラスムッセン、パブロ・パリイチュク、トラビス・ボーヴェ、ジャック・ライアン、ダニエル・チャレフ。Zep: エージェントメモリのための時間的知識グラフアーキテクチャ。arXivプレプリント arXiv:2501.13956、[2025年1月。doi: 10.48550/arXiv.2501.13956。URL http://arxiv.org/abs/2501.13956。](http://arxiv.org/abs/2501.13956)

Mohammad Javad Saeedizade and Eva Blomqvist. Navigating Ontology Development with Large Language Models. In Albert Mero˜no Pe˜nuela, Anastasia Dimou, Rapha¨el Troncy, Olaf Hartig, Maribel Acosta, Mehwish Alam, Heiko Paulheim, and Pasquale Lisena (eds.), _The Semantic Web, volume 14664, pp. 143–161. Springer Nature Switzerland, Cham, 2024._ doi: 10.1007/978-3-031-60626-7 8. [URL https://link.springer.com/10.1007/](https://link.springer.com/10.1007/978-3-031-60626-7_8) [978-3-031-60626-7_8.](https://link.springer.com/10.1007/978-3-031-60626-7_8)
モハマド・ジャヴァド・サイーディザーデ、エヴァ・ブロムクヴィスト。大規模言語モデルを用いたオントロジー開発のナビゲーション。アルバート・メローノ・ペヌエラ、アナスタシア・ディムー、ラファエル・トロンシー、オラフ・ハルティグ、マリベル・アコスタ、メフウィシュ・アラム、ハイコ・ポールハイム、パスカーレ・リセナ（編）、_セマンティックウェブ、ボリューム 14664、pp. 143–161。スプリンガー・ネイチャー・スイス、シャム、2024年。_ doi: 10.1007/978-3-031-60626-7 8。 [URL https://link.springer.com/10.1007/](https://link.springer.com/10.1007/978-3-031-60626-7_8) [978-3-031-60626-7_8。](https://link.springer.com/10.1007/978-3-031-60626-7_8)

Ali Sarabadani, Hadis Taherinia, Niloufar Ghadiri, Ehsan Karimi Shahmarvandi, and Ramin Mousa. PKG-LLM: A Framework for Predicting GAD and MDD Using Knowledge Graphs and Large Language Models in Cognitive Neuroscience. _Preprints, feb 2025._ doi: 10. 20944/preprints202502.0982.v1. [URL https://www.preprints.org/manuscript/](https://www.preprints.org/manuscript/202502.0982/v1) [202502.0982/v1.](https://www.preprints.org/manuscript/202502.0982/v1)
アリ・サラバダニ、ハディス・タヘリニア、ニルーファル・ガディリ、エフサン・カリミ・シャフマルヴァンディ、ラミン・ムーサ。PKG-LLM: 認知神経科学における知識グラフと大規模言語モデルを用いたGADおよびMDDの予測のためのフレームワーク。_プレプリント、2025年2月。_ doi: 10. 20944/preprints202502.0982.v1。 [URL https://www.preprints.org/manuscript/](https://www.preprints.org/manuscript/202502.0982/v1) [202502.0982/v1。](https://www.preprints.org/manuscript/202502.0982/v1)

Jiaqi Sun, Shiyou Qian, Zhangchi Han, Wei Li, Zelin Qian, Dingyu Yang, Jian Cao, and Guangtao Xue. LKD-KGC: Domain-Specific KG Construction via LLM-driven Knowledge Dependency Parsing. arXiv preprint arXiv:2505.24163, may 2025. doi: 10.48550/arXiv.2505.24163. URL [http://arxiv.org/abs/2505.24163.](http://arxiv.org/abs/2505.24163)
ジャーキ・スン、シーヨウ・チエン、ザンチ・ハン、ウェイ・リー、ゼリン・チエン、ディンユ・ヤン、ジアン・カオ、グアンタオ・シュー。LKD-KGC: LLM駆動の知識依存解析によるドメイン特化型KG構築。arXivプレプリント arXiv:2505.24163、2025年5月。doi: 10.48550/arXiv.2505.24163。URL [http://arxiv.org/abs/2505.24163。](http://arxiv.org/abs/2505.24163)

Yash Tiwari, Owais Ahmad Lone, and Mayukha Pal. OntoRAG: Enhancing Question-Answering through Automated Ontology Derivation from Unstructured Knowledge Bases. arXiv preprint _[arXiv:2506.00664, may 2025. doi: 10.48550/arXiv.2506.00664. URL http://arxiv.org/](http://arxiv.org/abs/2506.00664)_ [abs/2506.00664.](http://arxiv.org/abs/2506.00664)  
ヤシュ・ティワリ、オワイス・アフマド・ローン、マユカ・パル。OntoRAG: 非構造化知識ベースからの自動オントロジー導出を通じた質問応答の強化。arXivプレプリント _[arXiv:2506.00664、2025年5月。doi: 10.48550/arXiv.2506.00664。URL http://arxiv.org/](http://arxiv.org/abs/2506.00664)_ [abs/2506.00664。](http://arxiv.org/abs/2506.00664)

Tianshu Wang, Xiaoyang Chen, Hongyu Lin, Xuanang Chen, Xianpei Han, Hao Wang, Zhenyu Zeng, and Le Sun. Match, compare, or select? an investigation of large language models for entity matching
ティアンシュ・ワン、シャオヤン・チェン、ホンユ・リン、シュアンアン・チェン、シャンペイ・ハン、ハオ・ワン、ジェンユ・ゼン、レ・スン。マッチ、比較、または選択? エンティティマッチングのための大規模言語モデルの調査



. Match, compare, or select? an investigation of large language models for entity matching. 
. 一致、比較、または選択？エンティティマッチングのための大規模言語モデルの調査。

arXiv preprint arXiv:2405.16884, 2024. 
arXivプレプリント arXiv:2405.16884、2024年。

Xiang Wei, Xingyu Cui, Ning Cheng, Xiaobin Wang, Xin Zhang, Shen Huang, Pengjun Xie, Jinan Xu, Yufeng Chen, Meishan Zhang, Yong Jiang, and Wenjuan Han. 
Xiang Wei、Xingyu Cui、Ning Cheng、Xiaobin Wang、Xin Zhang、Shen Huang、Pengjun Xie、Jinan Xu、Yufeng Chen、Meishan Zhang、Yong Jiang、Wenjuan Han。

ChatIE: Zero-Shot Information Extraction via Chatting with ChatGPT. 
ChatIE: ChatGPTとのチャットによるゼロショット情報抽出。

arXiv preprint arXiv:2302.10205, may 2024. 
arXivプレプリント arXiv:2302.10205、2024年5月。

doi: 10.48550/arXiv.2302.10205. 
doi: 10.48550/arXiv.2302.10205。

URL http://arxiv.org/abs/2302.10205. 
URL http://arxiv.org/abs/2302.10205。

Wenjie Wu, Yongcheng Jing, Yingjie Wang, Wenbin Hu, and Dacheng Tao. 
Wenjie Wu、Yongcheng Jing、Yingjie Wang、Wenbin Hu、Dacheng Tao。

Graph-Augmented Reasoning: Evolving Step-by-Step Knowledge Graph Retrieval for LLM Reasoning. 
グラフ拡張推論：LLM推論のための段階的知識グラフ取得の進化。

arXiv preprint arXiv:2503.01642, mar 2025. 
arXivプレプリント arXiv:2503.01642、2025年3月。

doi: 10.48550/arXiv.2503.01642. 
doi: 10.48550/arXiv.2503.01642。

URL http://arxiv.org/abs/2503.01642. 
URL http://arxiv.org/abs/2503.01642。

Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. 
Wujiang Xu、Zujie Liang、Kai Mei、Hang Gao、Juntao Tan、Yongfeng Zhang。

A-MEM: Agentic Memory for LLM Agents. 
A-MEM：LLMエージェントのためのエージェンティックメモリ。

arXiv preprint arXiv:2502.12110, oct 2025. 
arXivプレプリント arXiv:2502.12110、2025年10月。

doi: 10.48550/arXiv.2502.12110. 
doi: 10.48550/arXiv.2502.12110。

URL http://arxiv.org/abs/2502.12110. 
URL http://arxiv.org/abs/2502.12110。

Lilong Xue, Dan Zhang, Yuxiao Dong, and Jie Tang. 
Lilong Xue、Dan Zhang、Yuxiao Dong、Jie Tang。

AutoRE: Document-Level Relation Extraction with Large Language Models. 
AutoRE：大規模言語モデルを用いた文書レベルの関係抽出。

In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations), pp. 211–220, Bangkok, Thailand, 2024. 
第62回計算言語学会年次総会（第3巻：システムデモ）の議事録において、ページ211–220、タイ・バンコク、2024年。

Association for Computational Linguistics. 
計算言語学会。

doi: 10.18653/v1/2024.acl-demos.20. 
doi: 10.18653/v1/2024.acl-demos.20。

URL https://aclanthology.org/2024.acl-demos.20. 
URL https://aclanthology.org/2024.acl-demos.20。

Linyao Yang, Chen Lv, Xiao Wang, Ji Qiao, Weiping Ding, Jun Zhang, and Fei-Yue Wang. 
Linyao Yang、Chen Lv、Xiao Wang、Ji Qiao、Weiping Ding、Jun Zhang、Fei-Yue Wang。

Collective entity alignment for knowledge fusion of power grid dispatching knowledge graphs. 
電力網の配信知識グラフの知識融合のための集合的エンティティアラインメント。

IEEE/CAA Journal of Automatica Sinica, 9(11):1990–2004, 2022a. 
IEEE/CAA自動化シニカジャーナル、9(11):1990–2004、2022年。

doi: 10.1109/JAS.2022.105947. 
doi: 10.1109/JAS.2022.105947。

Rui Yang, Boming Yang, Sixun Ouyang, Tianwei She, Aosong Feng, Yuang Jiang, Freddy Lecue, Jinghui Lu, and Irene Li. 
Rui Yang、Boming Yang、Sixun Ouyang、Tianwei She、Aosong Feng、Yuang Jiang、Freddy Lecue、Jinghui Lu、Irene Li。

Graphusion: Leveraging Large Language Models for Scientific Knowledge Graph Fusion and Construction in NLP Education. 
Graphusion：NLP教育における科学的知識グラフの融合と構築のための大規模言語モデルの活用。

arXiv preprint arXiv:2407.10794, jul 2024. 
arXivプレプリント arXiv:2407.10794、2024年7月。

doi: 10.48550/arXiv.2407.10794. 
doi: 10.48550/arXiv.2407.10794。

URL http://arxiv.org/abs/2407.10794. 
URL http://arxiv.org/abs/2407.10794。

Yang Yang, Zhilei Wu, Yuexiang Yang, Shuangshuang Lian, Fengjie Guo, and Zhiwei Wang. 
Yang Yang、Zhilei Wu、Yuexiang Yang、Shuangshuang Lian、Fengjie Guo、Zhiwei Wang。

A survey of information extraction based on deep learning. 
深層学習に基づく情報抽出の調査。

Applied Sciences, 12(19):9691, 2022b. 
応用科学、12(19):9691、2022年。

Hongbin Ye, Honghao Gui, Xin Xu, Xi Chen, Huajun Chen, and Ningyu Zhang. 
Hongbin Ye、Honghao Gui、Xin Xu、Xi Chen、Huajun Chen、Ningyu Zhang。

Schema-adaptable Knowledge Graph Construction. 
スキーマ適応型知識グラフ構築。

arXiv preprint arXiv:2305.08703, nov 2023. 
arXivプレプリント arXiv:2305.08703、2023年11月。

doi: 10.48550/arXiv.2305.08703. 
doi: 10.48550/arXiv.2305.08703。

URL http://arxiv.org/abs/2305.08703. 
URL http://arxiv.org/abs/2305.08703。

Kaisheng Zeng, Chengjiang Li, Lei Hou, Juanzi Li, and Ling Feng. 
Kaisheng Zeng、Chengjiang Li、Lei Hou、Juanzi Li、Ling Feng。

A comprehensive survey of entity alignment for knowledge graphs. 
知識グラフのためのエンティティアラインメントに関する包括的調査。

AI Open, 2:1–13, 2021. 
AIオープン、2:1–13、2021年。

doi: https://doi.org/10.1016/j.aiopen.2021.02.002. 
doi: https://doi.org/10.1016/j.aiopen.2021.02.002。

URL https://www.sciencedirect.com/science/article/pii/S2666651021000036. 
URL https://www.sciencedirect.com/science/article/pii/S2666651021000036。

Bowen Zhang and Harold Soh. 
Bowen Zhang、Harold Soh。

Extract, Define, Canonicalize: An LLM-based Framework for Knowledge Graph Construction. 
抽出、定義、標準化：知識グラフ構築のためのLLMベースのフレームワーク。

In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 9820–9836, Miami, Florida, USA, 2024. 
2024年自然言語処理における経験的手法に関する会議の議事録において、ページ9820–9836、アメリカ・フロリダ州マイアミ、2024年。

Association for Computational Linguistics. 
計算言語学会。

doi: 10.18653/v1/2024.emnlp-main.548. 
doi: 10.18653/v1/2024.emnlp-main.548。

URL https://aclanthology.org/2024.emnlp-main.548. 
URL https://aclanthology.org/2024.emnlp-main.548。

Zhigang Zhao, Xiong Luo, Maojian Chen, and Ling Ma. 
Zhigang Zhao、Xiong Luo、Maojian Chen、Ling Ma。

A survey of knowledge graph construction using machine learning. 
機械学習を用いた知識グラフ構築の調査。

CMES-Computer Modeling in Engineering & Sciences, 139(1), 2024. 
CMES-工学および科学におけるコンピュータモデリング、139(1)、2024年。

Lingfeng Zhong, Jia Wu, Qian Li, Hao Peng, and Xindong Wu. 
Lingfeng Zhong、Jia Wu、Qian Li、Hao Peng、Xindong Wu。

A comprehensive survey on automatic knowledge graph construction. 
自動知識グラフ構築に関する包括的調査。

ACM Computing Surveys, 56(4):1–62, 2023. 
ACMコンピューティングサーベイ、56(4):1–62、2023年。

Beibei Zhu, Ruolin Wang, Junyi Wang, Fei Shao, and Kerun Wang. 
Beibei Zhu、Ruolin Wang、Junyi Wang、Fei Shao、Kerun Wang。

A survey: knowledge graph entity alignment research based on graph embedding. 
調査：グラフ埋め込みに基づく知識グラフエンティティアラインメント研究。

Artificial Intelligence Review, 57(9):229, 2024a. 
人工知能レビュー、57(9):229、2024年。

Yuqi Zhu, Xiaohan Wang, Jing Chen, Shuofei Qiao, Yixin Ou, Yunzhi Yao, Shumin Deng, Huajun Chen, and Ningyu Zhang. 
Yuqi Zhu、Xiaohan Wang、Jing Chen、Shuofei Qiao、Yixin Ou、Yunzhi Yao、Shumin Deng、Huajun Chen、Ningyu Zhang。

Llms for knowledge graph construction and reasoning: Recent capabilities and future opportunities. 
知識グラフ構築と推論のためのLLM：最近の能力と将来の機会。

World Wide Web, 27(5):58, 2024b. 
ワールドワイドウェブ、27(5):58、2024年。

Amal Zouaq and Roger Nkambou. 
Amal Zouaq、Roger Nkambou。

A Survey of Domain Ontology Engineering: Methods and Tools. 
ドメインオントロジーエンジニアリングの調査：方法とツール。

In Roger Nkambou, Jacqueline Bourdeau, and Riichiro Mizoguchi (eds.), Advances in Intelligent Tutoring Systems, volume 308, pp. 103–119. 
Roger Nkambou、Jacqueline Bourdeau、Riichiro Mizoguchi（編）による、インテリジェントチュータリングシステムの進展、ボリューム308、ページ103–119。

Springer Berlin Heidelberg, Berlin, Heidelberg, 2010. 
スプリンガー・ベルリン・ハイデルベルク、ベルリン、ハイデルベルク、2010年。

doi: 10.1007/978-3-642-14363-2 6. 
doi: 10.1007/978-3-642-14363-2 6。

URL http://link.springer.com/10.1007/978-3-642-14363-2_6. 
URL http://link.springer.com/10.1007/978-3-642-14363-2_6。
