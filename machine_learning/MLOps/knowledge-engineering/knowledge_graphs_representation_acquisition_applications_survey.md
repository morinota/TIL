refs: https://arxiv.org/pdf/2002.00388


## A Survey on Knowledge Graphs: Representation, Acquisition and Applications
#### Shaoxiong Ji, Shirui Pan, Member, IEEE, Erik Cambria, Senior Member, IEEE, Pekka Marttinen, Philip S. Yu, Life Fellow, IEEE  
## 知識グラフに関する調査：表現、取得、応用
#### シャオシオン・ジー、シルイ・パン、IEEE会員、エリック・カンブリア、IEEEシニア会員、ペッカ・マルティネン、フィリップ・S・ユー、IEEEライフフェロー  

**_Abstract—Human knowledge provides a formal understand-_**  
**_要約—人間の知識は世界の正式な理解を提供します。_**  
**ing of the world. Knowledge graphs that represent structural**  
**構造的関係を表す知識グラフは、認知と人間レベルの知能に向けた、ますます人気のある研究方向となっています。**  
**relations between entities have become an increasingly popular**  
**この調査では、知識グラフに関する包括的なレビューを提供し、以下の1) 知識グラフの表現学習、2) 知識の取得と補完、**  
**research direction towards cognition and human-level intelligence.**  
**3) 時間的知識グラフ、4) 知識を意識した応用に関する全体的な研究トピックをまとめ、最近のブレークスルーと将来の研究を促進するための視点を要約します。**  
**In this survey, we provide a comprehensive review of knowledge**  
**私たちは、これらのトピックに関する全体的な分類と新しい分類法を提案します。**  
**graph covering overall research topics about 1) knowledge graph**  
**知識グラフの埋め込みは、表現空間、スコアリング関数、エンコーディングモデル、補助情報の4つの側面から整理されます。**  
**representation learning, 2) knowledge acquisition and completion,**  
**知識の取得、特に知識グラフの補完に関しては、埋め込み手法、パス推論、論理ルール推論をレビューします。**  
**3) temporal knowledge graph, and 4) knowledge-aware appli-**  
**さらに、メタ関係学習、常識推論、時間的知識グラフなどのいくつかの新興トピックを探ります。**  
**cations, and summarize recent breakthroughs and perspective**  
**知識グラフに関する将来の研究を促進するために、さまざまなタスクに関するデータセットとオープンソースライブラリのキュレーションされたコレクションも提供します。**  
**directions to facilitate future research. We propose a full-view**  
**最後に、いくつかの有望な研究方向について徹底的な展望を示します。**  
**categorization and new taxonomies on these topics. Knowledge**  
**_Index_**  
**graph embedding is organized from four aspects of representation**  
**_用語—知識グラフ、表現学習、知識グラフの補完、関係抽出、推論、深層学習。_**  
**space, scoring function, encoding models, and auxiliary infor-**  
**I. INTRODUCTION**  
**mation. For knowledge acquisition, especially knowledge graph**  
**人間の知識を取り入れることは、人工知能（AI）の研究方向の一つです。**  
**completion, embedding methods, path inference, and logical rule**  
**知識の表現と推論は、人間の問題解決に触発され、知的システムが複雑なタスクを解決する能力を得るために知識を表現することです。**  
**reasoning, are reviewed. We further explore several emerging top-**  
**最近、構造化された人間の知識の一形態としての知識グラフは、学界と産業の両方から大きな研究の注目を集めています。**  
**ics, including meta relational learning, commonsense reasoning,**  
**知識グラフは、事実の構造化された表現であり、エンティティ、関係、意味的記述で構成されています。**  
**and temporal knowledge graphs. To facilitate future research**  
**エンティティは実世界のオブジェクトや抽象的な概念であり、関係はエンティティ間の関係を表し、エンティティとその関係の意味的記述には、明確に定義された意味を持つタイプやプロパティが含まれます。**  
**on knowledge graphs, we also provide a curated collection of**  
**プロパティグラフまたは属性グラフは広く使用されており、ノードと関係にはプロパティや属性があります。**  
**datasets and open-source libraries on different tasks. In the**  
**知識グラフという用語は、わずかな違いで知識ベースと同義です。**  
**end, we have a thorough outlook on several promising research**  
**知識グラフは、そのグラフ構造を考慮すると、グラフとして見ることができます。**  
**directions.**  
**形式的な意味論が関与する場合、事実に対する解釈と推論のための知識ベースとして考えることができます。**  
**Knowledge can be expressed in a factual triple in the form of (head, relation, tail) or (subject, predicate, object) under the resource description framework (RDF), for example, (Albert Einstein, WinnerOf, Nobel Prize).**  
**知識ベースと知識グラフの例は図1に示されています。**  
**それは、(アルバート・アインシュタイン, WinnerOf, ノーベル賞)のように、リソース記述フレームワーク（RDF）の下で（ヘッド、関係、テール）または（主語、述語、目的語）の形で事実の三重項として表現できます。**  
**It can also be represented as a directed graph with nodes as entities and edges as relations.**  
**それはまた、ノードをエンティティ、エッジを関係とする有向グラフとして表現することもできます。**  
**For simplicity and following the trend of the research community, this paper uses the terms knowledge graph and knowledge base interchangeably.**  
**簡潔さのために、そして研究コミュニティのトレンドに従って、この論文では知識グラフと知識ベースという用語を互換的に使用します。**  
**(Albert Einstein, BornIn, German Empire)**  
**(アルバート・アインシュタイン, BornIn, ドイツ帝国)**  
**(Albert Einstein, SonOf, Hermann Einstein)**  
**(アルバート・アインシュタイン, SonOf, ヘルマン・アインシュタイン)**  
**(Albert Einstein, GraduateFrom, University of Zurich)**  
**(アルバート・アインシュタイン, GraduateFrom, チューリッヒ大学)**  
**(Albert Einstein, WinnerOf, Nobel Prize in Physics)**  
**(アルバート・アインシュタイン, WinnerOf, ノーベル物理学賞)**  
**(Albert Einstein, ExpertIn, Physics)**  
**(アルバート・アインシュタイン, ExpertIn, 物理学)**  
**(Nobel Prize in Physics, AwardIn, Physics)**  
**(ノーベル物理学賞, AwardIn, 物理学)**  
**(The theory of relativity, TheoryOf, Physics)**  
**(相対性理論, TheoryOf, 物理学)**  
**(Albert Einstein, SupervisedBy, Alfred Kleiner)**  
**(アルバート・アインシュタイン, SupervisedBy, アルフレッド・クレイナー)**  
**(Alfred Kleiner, ProfessorOf, University of Zurich)**  
**(アルフレッド・クレイナー, ProfessorOf, チューリッヒ大学)**  
**(The theory of relativity, ProposedBy, Albert Einstein)**  
**(相対性理論, ProposedBy, アルバート・アインシュタイン)**  
**(Hans Albert Einstein, SonOf, Albert Einstein)**  
**(ハンス・アルバート・アインシュタイン, SonOf, アルバート・アインシュタイン)**  
**(a) Factual triples in knowledge base.**  
**(a) 知識ベースにおける事実の三重項。**  
**(b) Entities and relations in knowledge graph.**  
**(b) 知識グラフにおけるエンティティと関係。**  
**Manuscript received August 09, 2020; revised November xx, 2020; accepted March 30, 2021.**  
**原稿は2020年8月9日に受理され、2020年11月xx日に改訂され、2021年3月30日に受理されました。**  
**This work is supported in part by NSF under grants III1763325, III-1909323, SaTC-1930941, in part by the Agency for Science, Technology and Research (A*STAR) under its AME Programmatic Funding Scheme (Project #A18A2b0046), and in part by the Academy of Finland (grants 336033, 315896), BusinessFinland (grant 884/31/2018), and EU H2020 (grant 101016775).**  
**この研究は、NSFの助成金III1763325、III-1909323、SaTC-1930941、A*STARのAMEプログラム資金スキーム（プロジェクト#A18A2b0046）による支援、フィンランドアカデミー（助成金336033、315896）、BusinessFinland（助成金884/31/2018）、EU H2020（助成金101016775）による支援を受けています。**  
**(Corresponding author: Shirui Pan.)**  
**(対応著者：シルイ・パン)**  
**S. Ji and P. Marttinen are with Aalto University, Finland. E-mail: _{shaoxiong.ji; pekka.marttinen}@aalto.fi_**  
**S. JiとP. Marttinenはフィンランドのアールト大学に所属しています。E-mail: _{shaoxiong.ji; pekka.marttinen}@aalto.fi_**  
**S. Pan is with the Department of Data Science and AI, Faculty of IT, Monash University, Australia. E-mail: shirui.pan@monash.edu**  
**S. Panはオーストラリアのモナシュ大学IT学部データサイエンスおよびAI学科に所属しています。E-mail: shirui.pan@monash.edu**  
**E. Cambria is with Nanyang Technological University, Singapore. Email: cambria@ntu.edu.sg**  
**E. Cambriaはシンガポールの南洋理工大学に所属しています。Email: cambria@ntu.edu.sg**  
**PS Y i ith U i it f Illi i t Chi USA E il @ i d**  
**PS Yはイリノイ大学シカゴ校に所属しています。E-mail: @**  
**Fig. 1: An example of knowledge base and knowledge graph.**  
**図1: 知識ベースと知識グラフの例。**  
**Recent advances in knowledge-graph-based research focus on knowledge representation learning (KRL) or knowledge graph embedding (KGE) by mapping entities and relations into low-dimensional vectors while capturing their semantic meanings [5], [9].**  
**知識グラフに基づく研究の最近の進展は、エンティティと関係を低次元ベクトルにマッピングし、その意味を捉えることによって、知識表現学習（KRL）または知識グラフ埋め込み（KGE）に焦点を当てています。**  
**Specific knowledge acquisition tasks include knowledge graph completion (KGC), triple classification, entity recognition, and relation extraction.**  
**特定の知識取得タスクには、知識グラフの補完（KGC）、三重項分類、エンティティ認識、関係抽出が含まれます。**  
**Knowledge-aware models benefit from the integration of heterogeneous information, rich ontologies and semantics for knowledge representation, and multi-lingual knowledge.**  
**知識を意識したモデルは、知識表現のための異種情報、豊富なオントロジーと意味論、そして多言語知識の統合から恩恵を受けます。**  
**Thus, many real-world applications such as recommendation systems and question answering have been brought about prosperity with the ability of commonsense understanding and reasoning.**  
**そのため、推薦システムや質問応答などの多くの実世界のアプリケーションは、常識的理解と推論の能力によって繁栄をもたらしました。**  
**Some real-world products, for example, Microsoft’s Satori and Google’s Knowledge Graph [3], have shown a strong capacity to provide more efficient services.**  
**例えば、MicrosoftのSatoriやGoogleのKnowledge Graph [3]などのいくつかの実世界の製品は、より効率的なサービスを提供する強力な能力を示しています。**  
**This paper conducts a comprehensive survey of current literature on knowledge graphs which enriches graphs with more**  
**この論文は、知識グラフに関する現在の文献の包括的な調査を行い、グラフをより豊かにします。**  
**context, intelligence, and semantics for knowledge acquisition and knowledge-aware applications. Our main contributions are summarized as follows.**  
**知識取得と知識を意識した応用のための文脈、知性、意味論を提供します。私たちの主な貢献は以下のように要約されます。**  
**_• Comprehensive review. We conduct a comprehensive_**  
**_• 包括的なレビュー。私たちは、知識グラフの起源と知識グラフにおける関係学習の現代技術の包括的なレビューを行います。_**  
**review of the origin of knowledge graph and modern techniques for relational learning on knowledge graphs.**  
**知識グラフの表現学習と推論の主要なニューラルアーキテクチャを紹介し、比較します。**  
**Major neural architectures of knowledge graph representation learning and reasoning are introduced and compared.**  
**さらに、さまざまなドメインにおける多くのアプリケーションの完全な概要を提供します。**  
**Moreover, we provide a complete overview of many applications in different domains.**  
**_• Full-view categorization and new taxonomies. A full-_**  
**_• 全面的な分類と新しい分類法。知識グラフに関する研究の全面的な分類と、詳細な新しい分類法を提示します。_**  
**view categorization of research on knowledge graph, together with fine-grained new taxonomies are presented.**  
**具体的には、高レベルで、KRL、知識取得、時間的知識グラフ、知識を意識した応用の4つの側面における知識グラフに関する研究をレビューします。**  
**Specifically, in the high-level, we review the research on knowledge graphs in four aspects: KRL, knowledge acquisition, temporal knowledge graphs, and knowledge-aware applications.**  
**KRLについては、表現空間、スコアリング関数、エンコーディングモデル、補助情報の4つの視点に細分化された分類法を提案します。**  
**For KRL, we further propose fine-grained taxonomies into four views, including representation space, scoring function, encoding models, and auxiliary information.**  
**知識取得については、KGCを埋め込みベースのランキング、関係パス推論、論理ルール推論、メタ関係学習の下でレビューします。**  
**For knowledge acquisition, KGC is reviewed under embedding-based ranking, relational path reasoning, logical rule reasoning, and meta relational learning;**  
**エンティティ取得タスクは、エンティティ認識、タイプ付け、曖昧さ解消、整合に分けられます。**  
**entity acquisition tasks are divided into entity recognition, typing, disambiguation, and alignment;**  
**関係抽出は、ニューラルパラダイムに従って議論されます。**  
**and relation extraction is discussed according to the neural paradigms.**  
**_• Wide coverage on emerging advances. We provide wide_**  
**_• 新興の進展に関する広範なカバレッジ。新興トピックに関する広範なカバレッジを提供します。_**  
**coverage on emerging topics, including transformer-based knowledge encoding, graph neural network (GNN) based knowledge propagation, reinforcement learning-based path reasoning, and meta relational learning.**  
**_• Summary and outlook on future directions. This survey_**  
**_• 将来の方向性に関する要約と展望。この調査は、各カテゴリの要約を提供し、有望な将来の研究方向を強調します。_**  
**provides a summary of each category and highlights promising future research directions.**  
**The remainder of this survey is organized as follows: first, an overview of knowledge graphs including history, notations, definitions, and categorization is given in Section II; then, we discuss KRL in Section III from four scopes; next, our review goes to tasks of knowledge acquisition and temporal knowledge graphs in Section IV and Section V; downstream applications are introduced in Section VI; finally, we discuss future research directions, together with a conclusion in the end. Other information, including KRL model training and a collection of knowledge graph datasets and open-source implementations, can be found in the appendices.**  
**この調査の残りの部分は次のように構成されています。まず、知識グラフの概要（歴史、表記、定義、分類を含む）を第II節で示し、次に第III節で4つの範囲からKRLについて議論します。次に、私たちのレビューは第IV節と第V節で知識取得と時間的知識グラフのタスクに移り、下流のアプリケーションは第VI節で紹介されます。最後に、将来の研究方向について議論し、結論を述べます。KRLモデルのトレーニングや知識グラフデータセットとオープンソース実装のコレクションを含むその他の情報は、付録にあります。**  



. A brief road map of knowledge base history is illustrated in Fig. 10 in Appendix A.
知識ベースの歴史の簡単なロードマップが付録Aの図10に示されています。

Many general knowledge graph databases and domain-specific knowledge bases have been released to facilitate research.
多くの一般的な知識グラフデータベースやドメイン特化型知識ベースが研究を促進するために公開されています。

We introduce more general and domain-specific knowledge bases in Appendices F-A1 and F-A2.
私たちは、付録F-A1およびF-A2で、より一般的かつドメイン特化型の知識ベースを紹介します。

_B. Definitions and Notations_  
_B. 定義と表記_

Most efforts have been made to give a definition by describing general semantic representation or essential characteristics.
ほとんどの努力は、一般的な意味表現や本質的な特徴を説明することによって定義を与えることに向けられています。

However, there is no such wide-accepted formal definition.
しかし、そのような広く受け入れられた正式な定義は存在しません。

Paulheim [11] defined four criteria for knowledge graphs.
Paulheim [11]は、知識グラフのための4つの基準を定義しました。

Ehrlinger and Woß [12] analyzed several existing definitions and proposed Definition 1, which emphasizes the reasoning engine of knowledge graphs.
EhrlingerとWoß [12]は、いくつかの既存の定義を分析し、知識グラフの推論エンジンを強調する定義1を提案しました。

Wang et al. [5] proposed a definition as a multi-relational graph in Definition 2.
Wangら [5]は、定義2において多関係グラフとしての定義を提案しました。

Following previous literature, we define a knowledge graph as $G = (E, R, F)$ where $E$, $R$, and $F$ are sets of entities, relations and facts, respectively.
先行文献に従い、私たちは知識グラフを$G = (E, R, F)$と定義します。ここで、$E$、$R$、$F$はそれぞれエンティティ、関係、事実の集合です。

A fact is denoted as a triple $(h, r, t)$.
事実は三つ組$(h, r, t)$として表されます。

**Definition 1 (Ehrlinger and Woß [12])** **. A knowledge graph acquires and integrates information into an ontology and applies a reasoner to derive new knowledge.**  
**定義1 (EhrlingerとWoß [12])** **. 知識グラフは情報をオントロジーに取得し統合し、推論機を適用して新しい知識を導出します。**

**Definition 2 (Wang et al. [5]). A knowledge graph is a multi-relational graph composed of entities and relations which are regarded as nodes and different types of edges, respectively.**  
**定義2 (Wangら [5]). 知識グラフは、エンティティと関係から構成される多関係グラフであり、これらはそれぞれノードと異なるタイプのエッジと見なされます。**

Specific notations and their descriptions are listed in Table I.
特定の表記とその説明は表Iに示されています。

Details of several mathematical operations are explained in Appendix B.
いくつかの数学的操作の詳細は付録Bで説明されています。

_C. Categorization of Research on Knowledge Graph_  
_C. 知識グラフに関する研究の分類_

This survey provides a comprehensive literature review on the research of knowledge graphs, namely KRL, knowledge acquisition, and a wide range of downstream knowledge-aware applications, where many recent advanced deep learning techniques are integrated.
この調査は、知識グラフの研究、すなわちKRL、知識獲得、および多くの最近の高度な深層学習技術が統合された幅広い下流の知識対応アプリケーションに関する包括的な文献レビューを提供します。

The overall categorization of the research is illustrated in Fig. 2.
研究の全体的な分類は図2に示されています。

| Notation | Description |  
|---|---|  
| $G$ | A knowledge graph |  
| $F$ | A set of facts |  
| $(h, r, t)$ | A triple of head, relation and tail |  
| $r \in R, e \in E$ | Relation set and entity set |  
| $v \in V$ | Vertex in vertice set |  
| $\xi \in E_G$ | Edge in edge set |  
| $es, eq, et$ | Source/query/current entity |  
| $rq$ | Query relation |  
| $< w_1, \ldots, w_n >$ | Text corpus |  
| $d \cdot ( \cdot )$ | Distance metric in specific space |  
| $fr(h, t)$ | Scoring function |  
| $\sigma( \cdot ), g( \cdot )$ | Non-linear activation function |  
| **Mr** | Mapping matrix |  
| **M** | Tensor |  
| $L$ | Loss function |  
| $R[d]$ | $d$ dimensional real-valued space |  
| $C[d]$ | $d$ dimensional complex space |  
| $H[d]$ | $d$ dimensional hypercomplex space |  
| $T[d]$ | $d$ dimensional torus space |  
| $B[d]_c$ | $d$ dimensional hyperbolic space with curvature $c$ |  
| $N (u, \sigma^2 I)$ | Gaussian distribution |  
| $\langle h, t \rangle$ | Hermitian dot product |  
| $t \otimes r$ | Hamilton product |  
| $h \circ t, h \odot t$ | Hadamard (element-wise) product |  
| $h \star t$ | Circular correlation |  
| concat(), $[h, r]$ | Vectors/matrices concatenation |  
| $\omega$ | Convolutional filters |  
| $*$ | Convolution operator |  

**Knowledge Representation Learning is a critical research issue of knowledge graph which paves the way for many knowledge acquisition tasks and downstream applications.**  
**知識表現学習は、知識グラフの重要な研究課題であり、多くの知識獲得タスクや下流のアプリケーションへの道を開きます。**

We categorize KRL into four aspects of representation space, scoring function, encoding models and auxiliary information, providing a clear workflow for developing a KRL model.
私たちはKRLを表現空間、スコアリング関数、エンコーディングモデル、補助情報の4つの側面に分類し、KRLモデルを開発するための明確なワークフローを提供します。

Specific ingredients include:  
具体的な要素は以下の通りです：

1) representation space in which the relations and entities are represented;  
1) 関係とエンティティが表現される表現空間；

2) scoring function for measuring the plausibility of factual triples;  
2) 事実の三つ組の妥当性を測定するためのスコアリング関数；

3) encoding models for representing and learning relational interactions;  
3) 関係の相互作用を表現し学習するためのエンコーディングモデル；

4) auxiliary information to be incorporated into the embedding methods.  
4) 埋め込み手法に組み込む補助情報。

Representation learning includes point-wise space, manifold, complex vector space, Gaussian distribution, and discrete space.
表現学習には、ポイントワイズ空間、マニフォールド、複素ベクトル空間、ガウス分布、および離散空間が含まれます。

Scoring metrics are generally divided into distance-based and similarity matching based scoring functions.
スコアリングメトリックは一般的に距離ベースと類似性マッチングに基づくスコアリング関数に分けられます。

Current research focuses on encoding models, including linear/bilinear models, factorization, and neural networks.
現在の研究は、線形/バイリニアモデル、因子分解、ニューラルネットワークを含むエンコーディングモデルに焦点を当てています。

Auxiliary information considers textual, visual, and type information.
補助情報は、テキスト、視覚、およびタイプ情報を考慮します。

**Knowledge Acquisition tasks are divided into three categories, i.e., KGC, relation extraction, and entity discovery.**  
**知識獲得タスクは、KGC、関係抽出、エンティティ発見の3つのカテゴリに分けられます。**

The first one is for expanding existing knowledge graphs, while the other two discover new knowledge (aka relations and entities) from the text.
最初のものは既存の知識グラフを拡張するためのものであり、他の2つはテキストから新しい知識（すなわち関係とエンティティ）を発見します。

KGC falls into the following categories: embedding-based ranking, relation path reasoning, rule-based reasoning, and meta relational learning.
KGCは、埋め込みベースのランキング、関係パス推論、ルールベースの推論、およびメタ関係学習の以下のカテゴリに分類されます。

Entity discovery includes recognition, disambiguation, typing, and alignment.
エンティティ発見には、認識、曖昧さ解消、タイプ付け、および整合が含まれます。

Relation extraction models utilize attention mechanism graph convolutional networks (GCNs), adversarial training, reinforcement learning, deep residual learning, and transfer learning.
関係抽出モデルは、注意メカニズムグラフ畳み込みネットワーク（GCN）、敵対的訓練、強化学習、深層残差学習、および転移学習を利用します。

**Temporal Knowledge Graphs incorporate temporal information for representation learning.**  
**時間的知識グラフは、表現学習のために時間的情報を組み込みます。**

This survey categorizes four research fields, including temporal embedding, entity dynamics, temporal relational dependency, and temporal logical reasoning.
この調査は、時間的埋め込み、エンティティの動態、時間的関係依存性、および時間的論理推論を含む4つの研究分野に分類します。

**Knowledge-aware Applications include natural language understanding (NLU), question answering, recommendation systems, and miscellaneous real-world tasks, which inject knowledge to improve representation learning.**  
**知識対応アプリケーションには、自然言語理解（NLU）、質問応答、推薦システム、およびさまざまな実世界のタスクが含まれ、知識を注入して表現学習を改善します。**

- Point-wise - Manifold  
- Single-fact QA  
- Complex - Gaussian Representation Space  
- Natural Language Question Answering - Multi-hop  
- Discrete Understanding Reasoning  
- Distance Scoring Function  
- Knowledge Knowledge- Dialogue Systems  
- Semantic Representation Aware Matching- Others  
- Encoding Models Learning Applications  
- Recommender Systems  
- Linear/Bilinear Auxiliary Information Knowledge  
- Others Applications - Question Generation  
- Factorization Graph - Search Engine  
- Neural Nets - Textual - Type - Visual - Medical Applications  
- CNN - Mental Healthcare  
- RNN Knowledge - Zero-shot Image  
- Transformers- GCN Entity Discovery Acquisition Knowledge  
- Temporal Classification- Text Generation- Sentiment Analysis  
- Relation Extraction Graph  
- Recognition Temporal Embedding  
- Typing Knowledge Graph Completion  
- Disambiguation  
- Alignment - Neural Nets Entity Dynamics  
- Attention - Embedding-based Ranking  
- GCN - Path-based Reasoning  
- GAN - Rule-based Reasoning  
- Temporal Relational Dependency  
- RL - Meta Relational Learning  
- Others - Triple Classification  
- Temporal Logical Reasoning  

Fig. 2: Categorization of research on knowledge graphs.  
図2: 知識グラフに関する研究の分類。

_D. Related Surveys_  
_D. 関連する調査_

Previous survey papers on knowledge graphs mainly focus on statistical relational learning [4], knowledge graph refinement [11], Chinese knowledge graph construction [13], knowledge reasoning [14], KGE [5] or KRL [9].
知識グラフに関する以前の調査論文は、主に統計的関係学習 [4]、知識グラフの洗練 [11]、中国の知識グラフ構築 [13]、知識推論 [14]、KGE [5] または KRL [9] に焦点を当てています。

The latter two surveys are more related to our work.
後者の2つの調査は、私たちの研究により関連しています。

Lin et al. [9] presented KRL in a linear manner, with a concentration on quantitative analysis.
Linら [9]は、KRLを線形的に提示し、定量分析に重点を置きました。

Wang et al. [5] categorized KRL according to scoring functions and specifically focused on the type of information utilized in KRL.
Wangら [5]は、スコアリング関数に基づいてKRLを分類し、特にKRLで利用される情報のタイプに焦点を当てました。

It provides a general view of current research only from the perspective of scoring metrics.
それは、スコアリングメトリックの観点からのみ、現在の研究の一般的な見解を提供します。

Our survey goes deeper to the flow of KRL and provides a full-scaled view from four-folds, including representation space, scoring function, encoding models, and auxiliary information.
私たちの調査はKRLの流れをより深く掘り下げ、表現空間、スコアリング関数、エンコーディングモデル、補助情報を含む4つの側面からの全体的な見解を提供します。

Besides, our paper provides a comprehensive review of knowledge acquisition and knowledge-aware applications with several emerging topics such as knowledge-graph-based reasoning and few-shot learning discussed.
さらに、私たちの論文は、知識グラフに基づく推論や少数ショット学習などのいくつかの新たなトピックを議論しながら、知識獲得と知識対応アプリケーションの包括的なレビューを提供します。

III. KNOWLEDGE REPRESENTATION LEARNING  
III. 知識表現学習

KRL is also known as KGE, multi-relation learning, and statistical relational learning in the literature.
KRLは、文献においてKGE、マルチリレーション学習、統計的関係学習としても知られています。

This section reviews recent advances on distributed representation learning with rich semantic information of entities and relations form four scopes including representation space (representing entities and relations, Sec. III-A), scoring function (measuring the plausibility of facts, Sec. III-B), encoding models (modeling the semantic interaction of facts, Sec. III-C), and auxiliary information (utilizing external information, Sec. III-D).
このセクションでは、エンティティと関係の豊富な意味情報を持つ分散表現学習の最近の進展を、表現空間（エンティティと関係を表現する、セクションIII-A）、スコアリング関数（事実の妥当性を測定する、セクションIII-B）、エンコーディングモデル（事実の意味的相互作用をモデル化する、セクションIII-C）、および補助情報（外部情報を利用する、セクションIII-D）の4つの範囲にわたってレビューします。

We further provide a summary in Sec. III-E.
さらに、セクションIII-Eで要約を提供します。

The training strategies for KRL models are reviewed in Appendix D.
KRLモデルのトレーニング戦略は付録Dでレビューされています。

| Col1 | Recommender Systems |  
|---|---|  
| Others Applications | |  


```md
. The relational interaction between head and tail h[T][ �]Mt is captured as a tensor denoted as **M[�] ∈** R[d][×][d][×][k]. 
ヘッドとテールの関係的相互作用 h[T][ �]Mt は、**M[�] ∈** R[d][×][d][×][k] として示されるテンソルとして捉えられます。

Instead of using the Cartesian coordinate system, HAKE [19] captures semantic hierarchies by mapping entities into the polar coordinate system, i.e., entity embeddings em ∈ R[d] and ep ∈ [0, 2π)[d] in the modulus and phase part, respectively. 
デカルト座標系を使用する代わりに、HAKE [19] はエンティティを極座標系にマッピングすることによって意味的階層を捉えます。すなわち、エンティティ埋め込み em ∈ R[d] と位相部分の ep ∈ [0, 2π)[d] です。

Many other translational models such as TransH [20] also use similar representation space, while semantic matching models use plain vector space (e.g., HolE [21]) and relational projection matrix (e.g., ANALOGY [22]). 
TransH [20] のような他の多くの翻訳モデルも同様の表現空間を使用しますが、意味的マッチングモデルは単純なベクトル空間（例：HolE [21]）や関係投影行列（例：ANALOGY [22]）を使用します。

Principles of these translational and semantic matching models are introduced in Section III-B1 and III-B2, respectively. 
これらの翻訳および意味的マッチングモデルの原則は、それぞれセクション III-B1 および III-B2 で紹介されています。

_2) Complex Vector Space: Instead of using a real-valued_ space, entities and relations are represented in a complex space, where h, t, r ∈ C[d]. 
_2) 複素ベクトル空間：実数値空間を使用する代わりに、エンティティと関係は複素空間で表現され、ここで h, t, r ∈ C[d] です。

Take head entity as an example, **h has a real part Re(h) and an imaginary part Im(h), i.e.,** **h = Re(h)+i Im(h). 
ヘッドエンティティを例に取ると、**h は実部 Re(h) と虚部 Im(h) を持ち、すなわち、** **h = Re(h)+i Im(h) です。

ComplEx [23] firstly introduces complex** vector space shown in Fig. 3b which can capture both symmetric and antisymmetric relations. 
ComplEx [23] は、対称関係と反対称関係の両方を捉えることができる複素ベクトル空間を最初に紹介します（図 3b に示されています）。

Hermitian dot product is used to do composition for relation, head and the conjugate of tail. 
エルミート内積は、関係、ヘッド、およびテールの共役の合成に使用されます。

Inspired by Euler’s identity e[iθ] = cos θ + i sin θ, RotatE [24] proposes a rotational model taking relation as a rotation from head entity to tail entity in complex space as t = h **r where** _◦_ _◦_ denotes the element-wise Hadmard product. 
オイラーの恒等式 e[iθ] = cos θ + i sin θ に触発されて、RotatE [24] は、複素空間におけるヘッドエンティティからテールエンティティへの回転として関係を回転と見なす回転モデルを提案します。ここで t = h **r** であり、_◦_ _◦_ は要素ごとのハダマード積を示します。

QuatE [25] extends the complex-valued space into hypercomplex h, t, r ∈ H[d] by a quaternion Q = a + bi + cj + dk with three imaginary components, where the quaternion inner product, i.e., the Hamilton product h **r, is used as compositional operator for** _⊗_ head entity and relation. 
QuatE [25] は、三つの虚部を持つ四元数 Q = a + bi + cj + dk によって、複素数空間を超複素数空間 h, t, r ∈ H[d] に拡張します。ここで、四元数内積、すなわちハミルトン積 h **r** は、ヘッドエンティティと関係の合成演算子として使用されます。

With the introduction of the rotational Hadmard product in complex space, RotatE [24] can also capture inversion and composition patterns as well as symmetry and antisymmetry. 
複素空間における回転ハダマード積の導入により、RotatE [24] は反転と合成パターン、ならびに対称性と反対称性を捉えることができます。

QuatE [25] uses Hamilton product to capture latent inter-dependencies within the four-dimensional space of entities and relations and gains a more expressive rotational capability than RotatE. 
QuatE [25] はハミルトン積を使用して、エンティティと関係の四次元空間内の潜在的な相互依存関係を捉え、RotatE よりも表現力豊かな回転能力を得ます。

_3) Gaussian Distribution: Inspired by Gaussian word em-_ bedding, the density-based embedding model KG2E [26] introduces Gaussian distribution to deal with the (un)certainties of entities and relations. 
_3) ガウス分布：ガウス語埋め込みに触発されて、密度ベースの埋め込みモデル KG2E [26] は、エンティティと関係の（不）確実性に対処するためにガウス分布を導入します。

The authors embedded entities and relations into multi-dimensional Gaussian distribution _H ∼_ _N (µh, Σh) and T ∼N (µt, Σt). 
著者は、エンティティと関係を多次元ガウス分布 _H ∼_ _N (µh, Σh) および T ∼N (µt, Σt) に埋め込みました。

The mean vector u indicates_ entities and relations’ position, and the covariance matrix **Σ models their (un)certainties. 
平均ベクトル u はエンティティと関係の位置を示し、共分散行列 **Σ はそれらの（不）確実性をモデル化します。

Following the translational** principle, the probability distribution of entity transformation _H −T is denoted as Pe ∼N (µh −_ **_µt, Σh + Σt). 
翻訳原則に従い、エンティティ変換 _H −T の確率分布は Pe ∼N (µh −_ **_µt, Σh + Σt) と示されます。

Similarly,_** TransG [27] represents entities with Gaussian distributions, while it draws a mixture of Gaussian distribution for relation embedding, where the m-th component translation vector of relation r is denoted as ur,m = **t −** **h** _∼_ _N_ �ut − **uh,** �σh[2] [+][ σ]t[2]� **E�.** 
同様に、TransG [27] はエンティティをガウス分布で表現し、関係埋め込みのためにガウス分布の混合を描きます。ここで、関係 r の m 番目の成分翻訳ベクトルは ur,m = **t −** **h** _∼_ _N_ �ut − **uh,** �σh[2] [+][ σ]t[2]� **E�.** と示されます。

_4) Manifold and Group: This section reviews knowledge_ representation in manifold space, Lie group, and dihedral group. 
_4) 多様体と群：このセクションでは、多様体空間、リー群、および二面体群における知識表現をレビューします。

A manifold is a topological space, which could be defined as a set of points with neighborhoods by the set theory. 
多様体は、集合論によって近傍を持つ点の集合として定義できる位相空間です。

The group is algebraic structures defined in abstract algebra. 
群は、抽象代数で定義された代数構造です。

Previous point-wise modeling is an ill-posed algebraic system where the number of scoring equations is far more than the number of entities and relations. 
以前の点ごとのモデリングは、スコアリング方程式の数がエンティティと関係の数を大幅に上回る不適切な代数システムです。

Moreover, embeddings are restricted in an overstrict geometric form even in some methods with subspace projection. 
さらに、埋め込みは、サブスペース投影を使用するいくつかの方法においても、過度に厳しい幾何学的形式に制限されています。

To tackle these issues, ManifoldE [28] extends point-wise embedding into manifold-based embedding. 
これらの問題に対処するために、ManifoldE [28] は点ごとの埋め込みを多様体ベースの埋め込みに拡張します。

The authors introduced two settings of manifold-based embedding, i.e., Sphere and Hyperplane. 
著者は、多様体ベースの埋め込みの二つの設定、すなわち、球面と超平面を導入しました。

An example of a sphere is shown in Fig. 3d. 
球面の例は図 3d に示されています。

For the sphere setting, Reproducing Kernel Hilbert Space is used to represent the manifold function. 
球面設定では、再生核ヒルベルト空間が多様体関数を表現するために使用されます。

Another “hyperplane” setting is introduced to enhance the model with intersected embeddings. 
別の「超平面」設定が、交差埋め込みを持つモデルを強化するために導入されます。

ManifoldE [28] relaxes the real-valued point-wise space into manifold space with a more expressive representation from the geometric perspective. 
ManifoldE [28] は、幾何学的視点からより表現力豊かな表現を持つ多様体空間に実数値点ごとの空間を緩和します。

When the manifold function and relation-specific manifold parameter are set to zero, the manifold collapses into a point. 
多様体関数と関係特有の多様体パラメータがゼロに設定されると、多様体は点に崩壊します。

Hyperbolic space, a multidimensional Riemannian manifold with a constant negative curvature −c (c > 0) : B[d,c] = �x ∈ R[d] : ∥x∥[2] _<_ [1]c �, is drawing attention for its capacity of 
双曲空間は、定数負曲率 −c (c > 0) を持つ多次元リーマン多様体であり、B[d,c] = �x ∈ R[d] : ∥x∥[2] _<_ [1]c � です。階層情報を捉える能力に注目されています。

capturing hierarchical information. 
階層情報を捉える能力に注目されています。

MuRP [29] represents the multi-relational knowledge graph in Poincare ball of hyperbolic´ space B[d]c [=] �x ∈ R[d] : c∥x∥[2] _< 1�. 
MuRP [29] は、双曲空間 B[d]c のポアンカレ球における多関係知識グラフを表現します [=] �x ∈ R[d] : c∥x∥[2] _< 1�。

While it fails to capture_ logical patterns and suffers from constant curvature. 
しかし、論理パターンを捉えることができず、定数曲率に悩まされます。

Chami et al. [30] leverages expressive hyperbolic isometries and learns a relation-specific absolute curvature cr in the hyperbolic space. 
Chami ら [30] は、表現力豊かな双曲線等長写像を利用し、双曲空間における関係特有の絶対曲率 cr を学習します。

TorusE [15] solves the regularization problem of TransE via embedding in an n-dimensional torus space which is a compact Lie group. 
TorusE [15] は、n 次元トーラス空間に埋め込むことによって TransE の正則化問題を解決します。これはコンパクトなリー群です。

With the projection from vector space into torus space defined as π : R[n] _→_ _T_ _[n], x �→_ [x], entities and relations are denoted as [h], [r], [t] ∈ T[n]. 
ベクトル空間からトーラス空間への射影は、π : R[n] _→_ _T_ _[n], x �→_ [x] と定義され、エンティティと関係は [h], [r], [t] ∈ T[n] として示されます。

Similar to TransE, it also learns embeddings following the relational translation in torus space, i.e., [h] + [r] [t]. 
TransE と同様に、トーラス空間における関係翻訳に従って埋め込みを学習します。すなわち、[h] + [r] [t] です。

Recently, DihEdral [31] _≈_ proposes a dihedral symmetry group preserving a 2-dimensional polygon. 
最近、DihEdral [31] _≈_ は、2次元多角形を保持する二面体対称群を提案しました。

It utilizes a finite non-Abelian group to preserve the relational properties of symmetry/skew-symmetry, inversion, and composition effectively with the rotation and reflection properties in the dihedral group. 
それは、二面体群における回転および反射特性を用いて、対称性/反対称性、反転、および合成の関係的特性を効果的に保持するために、有限非アーベル群を利用します。

-----
0  
0.4  
0.2  
_−02_ 2  
**r 2 R[d]**  
**Mr 2 R[d][⇥][d]**  
Im(u)  
**u 2 C[d]** **a 2 R[d]** **b 2 R[d]**  
**u = a + bi**  
**Mcr 2 R[d][⇥][d][⇥][k]**  
Re(u)  
(b) Complex vector space.  
2−2 _−_  
(c) Gaussian distribution.  
_P_ (x1, x2)  
0.3  
0.2  
0.1  
0  
(d) Manifold space.  
0  
(a) Point-wise space.  
_B. Scoring Function_  
Fig. 3: An illustration of knowledge representation in different spaces.  
スコアリング関数は、事実の妥当性を測定するために使用され、エネルギーベースの学習フレームワークではエネルギー関数とも呼ばれます。エネルギーベースの学習は、エネルギー関数 Eθ(x) (θ によってパラメータ化され、x を入力として取る) を学習し、正のサンプルが負のサンプルよりも高いスコアを持つことを確実にすることを目的としています。この論文では、スコアリング関数の用語が統一のために採用されています。

There are two typical types of scoring functions, i.e., distance-based (Fig. 4a) and similarity-based (Fig. 4b) functions, to measure the plausibility of a fact. 
事実の妥当性を測定するために、二つの典型的なスコアリング関数のタイプ、すなわち、距離ベース（図 4a）と類似性ベース（図 4b）関数があります。

Distance-based scoring function measures the plausibility of facts by calculating the distance between entities, where addictive translation with relations as h + **r** **t is widely used.** 
距離ベースのスコアリング関数は、エンティティ間の距離を計算することによって事実の妥当性を測定します。ここで、関係を h + **r** **t** として加算的に翻訳することが広く使用されています。

_≈_ Semantic similarity based scoring measures the plausibility of facts by semantic matching. 
_≈_ 意味的類似性に基づくスコアリングは、意味的マッチングによって事実の妥当性を測定します。

It usually adopts a multiplicative formulation, i.e., h[⊤]Mr ≈ **t[⊤], to transform head entity near** the tail in the representation space. 
通常、乗法的な定式化を採用し、すなわち h[⊤]Mr ≈ **t[⊤] として、表現空間内でヘッドエンティティをテールに近づけます。**

_fr(h, r)_  
of h + **r should be close to the embedding of t with the scoring** function is defined under L1 or L2 constraints as  
h + **r** の _fr(h, r)_ は、スコアリング関数が L1 または L2 制約の下で定義されるとき、t の埋め込みに近い必要があります。

_fr(h, t) = ∥h + r −_ **t∥L1/L2** _._ (2)  
_fr(h, t) = ∥h + r −_ **t∥L1/L2** _._ (2)  

Since that, many variants and extensions of TransE have been proposed. 
そのため、TransE の多くの変種と拡張が提案されています。

For example, TransH [20] projects entities and relations into a hyperplane, TransR [17] introduces separate projection spaces for entities and relations, and TransD [33] constructs dynamic mapping matrices Mrh = rph[⊤]p [+][ I][ and] **Mrt = rpt[⊤]p** [+] **[I][ by the projection vectors][ h][p][,][ t][p][,][ r][p]** _[∈]_ [R][n][. 
例えば、TransH [20] はエンティティと関係を超平面に投影し、TransR [17] はエンティティと関係のための別々の投影空間を導入し、TransD [33] は動的マッピング行列 Mrh = rph[⊤]p [+][ I][ および] **Mrt = rpt[⊤]p** [+] **[I][ を投影ベクトル][ h][p][,][ t][p][,][ r][p]** _[∈]_ [R][n][ を構築します。

By replacing Euclidean distance, TransA [34] uses Mahalanobis distance to enable more adaptive metric learning. 
ユークリッド距離を置き換えることによって、TransA [34] はマハラノビス距離を使用して、より適応的なメトリック学習を可能にします。

Previous methods used additive score functions, TransF [35] relaxes the strict translation and uses dot product as fr(h, t) = (h + r)[⊤]t. 
以前の方法は加算スコア関数を使用していましたが、TransF [35] は厳密な翻訳を緩和し、ドット積を fr(h, t) = (h + r)[⊤]t として使用します。

To balance the constraints on head and tail, a flexible translation scoring function is further proposed. 
ヘッドとテールの制約のバランスを取るために、柔軟な翻訳スコアリング関数がさらに提案されています。

Recently, ITransF [36] enables hidden concepts discovery and statistical strength transferring by learning associations between relations and concepts via sparse attention vectors, with scoring function defined as  
最近、ITransF [36] は、スパースアテンションベクトルを介して関係と概念の関連を学習することによって、隠れた概念の発見と統計的強度の転送を可能にします。スコアリング関数は次のように定義されます。

_fr(h, t) =_ ���αHr _[·][ D][ ·][ h][ +][ r][ −]_ **_[α]r[T]_** _[·][ D][ ·][ t]���ℓ_ _[,]_ (3)  
_fr(h, t) =_ ���αHr _[·][ D][ ·][ h][ +][ r][ −]_ **_[α]r[T]_** _[·][ D][ ·][ t]���ℓ_ _[,]_ (3)  

**r** distance  
**h**  
**t**  
(a) Translational distancebased scoring of TransE.  
**h** **t**  
(b) Semantic similarity-based scoring of DistMult.  
|f (h, r) r r|Col2|Col3|Col4|Col5|  
|---|---|---|---|---|  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | | | |  
| | | |


. KG2E uses two scoring methods, i.e, asymmetric KL-divergence and symmetric expected likelihood. 
KG2Eは、非対称KLダイバージェンスと対称期待尤度という2つのスコアリング手法を使用します。

While the scoring function of ManifoldE is defined as
ManifoldEのスコアリング関数は次のように定義されます。

$$
_fr(h, t) = M(h, r, t) - D_r^2,
$$  
$$
\text{(5)}
$$  
where M is the manifold function, and Dr is a relation-specific manifold parameter. 
ここで、Mは多様体関数であり、$D_r$は関係特有の多様体パラメータです。
