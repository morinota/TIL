## 0.1. link 0.1. リンク

- [pdf](https://arxiv.org/ftp/arxiv/papers/1804/1804.11192.pdf) pdf](https:

## 0.2. abstract 0.2. 抽象的

Explainable recommendation attempts to develop models that generate not only high-quality recommendations but also intuitive explanations.
説明可能なレコメンデーションは、高品質のレコメンデーションだけでなく、直感的な説明も生成するモデルを開発することを試みる.
The explanations may either be post-hoc or directly come from an **explainable model** (also called interpretable or transparent model in some contexts).
説明可能な推薦とは、**説明可能なモデル**（文脈によっては解釈可能なモデル、透明なモデルとも呼ばれる）から直接的に得られる説明か、ポストホックな説明かのどちらかである.
Explainable recommendation tries to address the problem of why: by providing explanations to users or system designers, it helps humans to understand why certain items are recommended by the algorithm, where the human can either be users or system designers.
説明可能な推薦とは、なぜという問題を解決しようとするもので、ユーザーやシステム設計者に説明を提供することで、**アルゴリズムによってあるアイテムが推薦される理由を人間が理解できるようにするもの**である（人間はユーザーでもシステム設計者でもよい）.
Explainable recommendation helps to improve the transparency, persuasiveness, effectiveness, trustworthiness, and satisfaction of recommendation systems.
説明可能な推薦とは、推薦システムの透明性、説得力、有効性、信頼性、満足度を向上させるのに有効である。
It also facilitates system designers for better system debugging.
また、システム設計者がより良いシステムのデバッグを行うことも容易にする。
In recent years, a large number of explainable recommendation approaches – especially model-based methods – have been proposed and applied in real-world systems.
近年、説明可能な推薦手法、特にモデルベース手法が数多く提案され、実世界のシステムに適用されている。
In this survey, we provide a comprehensive review for the explainable recommendation research.
本調査では、説明可能な推薦手法の研究を包括的にレビューする。
We first highlight the position of explainable recommendation in recommender system research by categorizing recommendation problems into the 5W, i.e., what, when, who, where, and why.
まず、推薦問題を5W（what, when, who, where, why）に分類し、推薦システム研究における説明可能な推薦の位置づけを明らかにする.
We then conduct a comprehensive survey of explainable recommendation on three perspectives:
次に、説明可能な推薦について、3つの観点から包括的に調査する.

1. We provide a chronological research timeline of explainable recommendation, including user study approaches in the early years and more recent model-based approaches.
   1）説明可能なレコメンデーションに関する研究年表を作成し、初期のユーザー研究的アプローチから最近のモデルベースアプローチまで、説明可能なレコメンデーションの研究年表を作成する。
2. We provide a two-dimensional taxonomy to classify existing explainable recommendation research: one dimension is the information source (or display style) of the explanations, and the other dimension is the algorithmic mechanism to generate explainable recommendations.
   2）既存の説明可能なレコメンデーション研究を、説明の情報源（あるいは表示スタイル）と説明可能なレコメンデーション生成のアルゴリズム機構という2次元の分類で紹介する。
3. We summarize how explainable recommendation applies to different recommendation tasks, such as product recommendation, social recommendation, and POI recommendation. 商品推薦、社会的推薦、POI推薦などの異なる推薦タスクに対して、説明可能な推薦がどのように適用されるかを要約している。

We also devote a section to discuss the explanation perspectives in broader IR and AI.
また、より広範なIRやAIにおける説明の視点について議論するセクションを設ける。

# 1. Introduction 1. はじめに

## 1.1. Explainable Recommendation 1.1. 説明可能なレコメンデーション

Explainable recommendation refers to personalized recommendation algorithms that address the problem of why – they not only provide users or system designers with recommendation results, but also explanations to clarify why such items are recommended.
説明可能な推薦とは、ユーザーやシステム設計者に推薦結果を提供するだけでなく、なぜそのような項目が推薦されたのかを明確にするための説明を提供する、「なぜ」の問題を解決した個人化推薦アルゴリズムのことである.
In this way, it helps to improve the transparency, persuasiveness, effectiveness, trustworthiness, and user satisfaction of the recommendation systems.
これにより、推薦システムの透明性、説得力、有効性、信頼性、ユーザー満足度を向上させることができる.
It also facilitates system designers to diagnose, debug, and refine the recommendation algorithm.
また、システム設計者が推薦アルゴリズムを診断し、デバッグし、改良することも容易になる.

To highlight the position of explainable recommendation in the recommender system research area, we classify personalized recommendation with a broad conceptual taxonomy.
推薦システム研究領域における説明可能な推薦の位置づけを明らかにするために、我々は個人化推薦を広い概念分類で分類している.
Specifically, personalized recommendation research can be classified into the 5W problems – when, where, who, what, and why, corresponding to time-aware recommendation (when), location-based recommendation (where), social recommendation (who), application-aware recommendation (what), and explainable recommendation (why), where explainable recommendation aims to answer why-type questions in recommender systems.
具体的には、**個人向け推薦の研究は、いつ、どこで、誰が、何を、なぜという5W問題に分類される**.これは、時間考慮型推薦（いつ）、位置情報推薦（どこで）、ソーシャル推薦（誰が）、アプリケーション考慮型推薦（何が）、そして説明可能な推薦（なぜ）に対応し、提案システムにおけるなぜ型の質問に答えることを目的としたものである.

Explainable recommendation models can either be model-intrinsic or model-agnostic (Lipton, 2018; Molnar, 2019).
説明可能なレコメンデーションモデルには、**モデル内在型(model-intrinsic)**と**モデル不可知論型(model-agnostic)**がある（Lipton, 2018; Molnar, 2019）.
The model-intrinsic approach develops interpretable models, whose decision mechanism is transparent, and thus, we can naturally provide explanations for the model decisions (Zhang et al., 2014a).
モデル内在的アプローチは、解釈可能なモデルを開発し、その決定メカニズムは透明であり、したがって、モデルの決定に対して自然に説明を提供することができる（Zhang et al.）.
The model-agnostic approach (Wang et al., 2018d), or sometimes called the post-hoc explanation approach (Peake and Wang, 2018), allows the decision mechanism to be a blackbox.
モデル不可知論的アプローチ（Wang et al., 2018d）、あるいは**post-hoc explanationアプローチ**（Peake and Wang, 2018）と呼ばれることもあるが、意思決定機構をブラックボックスとすることが可能である.
Instead, it develops an explanation model to generate explanations after a decision has been made.
その代わり、**意思決定後に説明を生成するためのexplanationモデル**を開発する.
The philosophy of these two approaches is deeply rooted in our understanding of human cognitive psychology – sometimes we make decisions by careful, rational reasoning and we can explain why we make certain decisions; other times we make decisions first and then find explanations for the decisions to support or justify ourselves (Lipton, 2018; Miller, 2019).
この2つのアプローチの思想は、人間の認知心理学の理解に深く根ざしている--私たちは慎重かつ合理的な推論によって意思決定を行い、ある決定を行う理由を説明できることもあれば、**まず意思決定を行ってから、その決定に対する説明を見つけて自分自身を支持または正当化する**こともある（Lipton，2018； Miller，2019 ）.

The scope of explainable recommendation not only includes developing transparent machine learning, information retrieval, or data mining models.
説明可能なレコメンデーションは、機械学習、情報検索、データマイニングなどの透明性の高いモデルの開発だけでなく、ユーザーやシステム設計者に効果的なレコメンデーションや説明の方法を提供することも含まれる.
It also includes developing effective methods to deliver the recommendations or explanations to users or system designers, because explainable recommendations naturally involve humans in the loop.
また、説明可能な推薦には当然ながら人間が関与するため、ユーザーやシステム設計者に推薦や説明を提供する効果的な手法の開発も含まれる.
Significant research efforts in user behavior analysis and humancomputer interaction community aim to understand how users interact with explanations.
ユーザー行動解析やヒューマンコンピュータインタラクションの分野では、ユーザーが説明とどのように関わるかを理解するために、重要な研究活動が行われている.

With this section, we will introduce not only the explainable recommendation problem, but also a big picture of the recommender system research area.
この章では、説明可能な推薦問題だけでなく、推薦システム研究領域の全体像についても紹介する.
It will help readers to understand what is unique about the explainable recommendation problem, what is the position of explainable recommendation in the research area, and why explainable recommendation is important to the area.
説明可能な推薦問題とは何か、説明可能な推薦の研究領域における位置づけは何か、説明可能な推薦がなぜこの領域で重要なのかを読者に理解してもらうためである.

## 1.2. A Historical Overview 1.2. 歴史的な概要

In this section, we will provide a historical overview of the explainable recommendation research.
このセクションでは、説明可能な推薦の研究の歴史的な概要を説明する.
Though the term explainable recommendation was formally introduced in recent years (Zhang et al., 2014a), the basic concept, however, dates back to some of the earliest works in personalized recommendation research.
Explainable Recommendation という用語は近年正式に導入されましたが（Zhang et al., 2014a）、**しかし、その基本概念はパーソナライズド・レコメンデーション研究の最も初期の研究までさかのぼる**.
For example, Schafer et al. (1999) noted that recommendations could be explained by other items that the user is familiar with, such as this product you are looking at is similar to these other products you liked before, which leads to the fundamental idea of item-based collaborative filtering (CF); Herlocker et al. (2000) studied how to explain CF algorithms in MovieLens based on user surveys; and Sinha and Swearingen (2002) highlighted the role of transparency in recommender systems.
例えば、Schaferら（1999）は、「あなたが見ているこの商品は、あなたが以前気に入ったこれらの他の商品と似ている」など、**ユーザがよく知っている他のアイテムによって推薦が説明できることに注目**し、アイテムベースの協調フィルタリング（CF）の基本的な考え方につながり、Herlockerら（2000）はユーザ調査に基づいてMovieLensにおけるCFアルゴリズムの説明方法を研究し、Sinha and Swearingen（2002）は推薦システムにおける透明性の役割に注目した.
Besides, even before explainable recommendation has attracted serious research attention, the industry has been using manual or semi-automatic explanations in practical systems, such as the people also viewed explanation in e-commerce systems (Tintarev and Masthoff, 2007a).
また、説明可能な推薦が本格的に研究される以前から、業界では、電子商取引システムにおける人々も見る説明（Tintarev and Masthoff, 2007a）のように、手動または半自動の説明を実用的なシステムで使用してきた.

To help the readers understand the “pre-history” research of recommendation explanation and how explainable recommendation emerged as an essential research task in the recent years, we provide a historical overview of the research line in this section.
推薦説明の「前史」研究と、近年、説明可能な推薦が必須の研究課題として浮上した経緯を理解するために、本節では、研究ラインの歴史的概観を示す.

Early approaches to personalized recommender systems mostly focused on content-based or collaborative filtering (CF)-based recommendation (Ricci et al., 2011).
パーソナライズド・レコメンダーシステムの初期のアプローチは、コンテンツベースまたは協調フィルタリング（CF）ベースのレコメンダーに焦点を当てたものであった（Ricci et al.）
Content-based recommender systems model user and item profiles with various available content information, such as the price, color, brand of the goods in e-commerce, or the genre, director, duration of the movies in review systems (Balabanović and Shoham, 1997; Pazzani and Billsus, 2007).
コンテンツベースレコメンダーは，電子商取引における商品の価格，色，ブランド，レビューシステムにおける映画のジャンル，監督，時間など，**様々な利用可能なコンテンツ情報を用いて，ユーザとアイテムのプロファイルをモデル化**する(Balabanović and Shoham, 1997; Pazzani and Billsus, 2007).
Because the item contents are easily understandable to users, it was usually intuitive to explain to users why an item is recommended.
アイテムの内容はユーザにとって理解しやすいため，なぜそのアイテムが推薦されるのかをユーザに説明することは，通常，直感的に理解できるものであった．
For example, one straightforward way is to let users know the content features he
例えば，「なぜそのアイテムが推薦されるのか」をユーザに説明することは，直感的な方法の一つである．

However, collecting content information in different application domains is time-consuming.
しかし、異なるアプリケーション領域でコンテンツ情報を収集するのは時間がかかる.
Collaborative filtering (CF)-based approaches (Ekstrand et al., 2011), on the other hand, attempt to avoid this difficulty by leveraging the wisdom of crowds.
一方、協調フィルタリング（CF）ベースのアプローチ（Ekstrand et al.2011）は、群衆の知恵を活用することによって、この困難を回避しようとするものである.
One of the earliest CF algorithms is User-based CF for the GroupLens news recommendation system (Resnick et al., 1994).
初期の CF アルゴリズムのひとつに、GroupLens **ニュース推薦システム(!?)**のためのユーザベース CF がある（Resnick et al.）
User-based CF represents each user as a vector of ratings, and predicts the user’s missing rating on a news message based on the weighted average of other users’ ratings on the message.
ユーザベースCFは、各ユーザを評価のベクトルとして表現し、あるニュースメッセージに対する他のユーザの評価の加重平均に基づいて、そのユーザの欠落している評価を予測する。
Symmetrically, Sarwar et al. (2001) introduced the Item-based CF method, and Linden et al. (2003) further described its application in Amazon product recommendation system.
これと対称的に、Sarwarら（2001）はアイテムベースCFを紹介し、Lindenら（2003）はさらにそのAmazon商品推薦システムへの応用を述べている。
Item-based CF takes each item as a vector of ratings, and predicts the missing rating based on the weighted average of ratings from similar items.
アイテムベースCFは、各アイテムを評価のベクトルとみなし、類似アイテムの評価の加重平均に基づいて欠落している評価を予測する。

Though the rating prediction mechanism would be relatively difficult to understand for average users, user- and item-based CF are somewhat explainable due to the philosophy of their algorithm design.
評価予測の仕組みは、一般ユーザには比較的理解しにくいものですが、ユーザベースCFとアイテムベースCFは、そのアルゴリズム設計の思想から、ある程度説明可能です。
For example, the items recommended by user-based CF can be explained as “users that are similar to you loved this item”, while item-based CF can be explained as “the item is similar to your previously loved items”.
例えば、ユーザーベースCFで推薦されるアイテムは、「あなたと似たユーザーがこのアイテムを愛用していた」と説明でき、アイテムベースCFは、「そのアイテムは、あなたが以前愛用していたアイテムに似ている」と説明できるのである。
However, although the idea of CF has achieved significant improvement in recommendation accuracy, it is less intuitive to explain compared with content-based algorithms.
しかし、CFの考え方は、推薦精度の大幅な向上を達成したものの、コンテンツベースのアルゴリズムと比較して、直感的に説明しにくいという欠点がある。
Research pioneers in very early stages also noticed the importance of the problem (Herlocker and Konstan, 2000; Herlocker et al., 2000; Sinha and Swearingen, 2002).
ごく初期の段階の研究パイオニアもこの問題の重要性に気づいていた（Herlocker and Konstan, 2000; Herlocker et al.）

The idea of CF achieved further success when integrated with Latent Factor Models (LFM) introduced by Koren (2008) in the late 2000s.
CFの考え方は、2000年代後半にKoren (2008)によって導入されたLatent Factor Models (LFM)と統合されたときに、さらなる成功を収めた。
Among the many LFMs, Matrix Factorization (MF) and its variants were especially successful in rating prediction tasks (Koren et al., 2009).
多くのLFMの中で、Matrix Factorization (MF)とその変種は、格付け予測タスクで特に成功を収めた(Koren et al., 2009)。
Latent factor models have been leading the research and application of recommender systems for many years.
潜在因子モデルは長年にわたり推薦システムの研究・応用をリードしてきた。
However, though successful in recommendation performance, the “latent factors” in LFMs do not possess intuitive meanings, which makes it difficult to understand why an item got good predictions or why it got recommended out of other candidates.
しかし，推薦性能では成功しているものの，LFMにおける「潜在因子」は直感的な意味を持っていないため，ある項目がなぜ良い予測を得たのか，なぜ他の候補の中から推薦されたのかを理解することは難しい．
This lack of model explainability also makes it challenging to provide intuitive explanations to users, since it is hardly acceptable to tell users that we recommend an item only because it gets higher prediction scores by the model.
また、このようなモデルの説明可能性の欠如は、ユーザーに対して直感的な説明を行うことを困難にしている。なぜなら、モデルによって予測スコアが高くなったからと言って、ある項目を推薦するということは、ユーザーにとって受け入れがたいことだからである。

To make recommendation models better understandable, researchers have gradually turned to Explainable Recommendation Systems, where the recommendation algorithm not only outputs a recommendation list, but also explanations for the recommendations by working in an explainable way.
推薦モデルをより理解しやすくするために、研究者は徐々に、推薦アルゴリズムが推薦リストを出力するだけでなく、説明可能な方法で動作することによって推薦に対する説明も行う、説明可能な推薦システムに目を向けてきた。
For example, Zhang et al. (2014a) defined the explainable recommendation problem, and proposed an Explicit Factor Model (EFM) by aligning the latent dimensions with explicit features for explainable recommendation.
例えば、Zhangら（2014a）は説明可能な推薦問題を定義し、説明可能な推薦のために潜在的次元と明示的特徴を整合させることにより、明示的因子モデル（EFM）を提案した。
More approaches were also proposed to address the explainability problem, which we will introduce in detail in the survey.
また、説明可能性問題を解決するために、より多くのアプローチが提案されたが、これらはサーベイで詳しく紹介する。
It is worthwhile noting that deep learning (DL) models for personalized recommendation have emerged in recent years.
近年、個人化推薦のための深層学習（DL）モデルが出現していることは注目に値する。
We acknowledge that whether DL models truly improve the recommendation performance is controversial (Dacrema et al., 2019), but this problem is out of the scope of this survey.
DLモデルが本当に推薦性能を向上させるかどうかは議論のあるところであるが（Dacrema et al., 2019）、この問題は本サーベイの範囲外であることを認めたい。
In this survey, we will focus on the problem that the black-box nature of deep models brings difficulty in model explainability.
本サーベイでは、ディープモデルのブラックボックス的性質がモデルの説明可能性に困難をもたらすという問題に焦点を当てます。
We will review the research efforts on explainable recommendation over deep models.
深層モデル上の説明可能な推薦に関する研究努力をレビューする。

In a broader sense, the explainability of AI systems was already a core discussion in the 1980s era of “old” or logical AI research, when knowledge-based systems predicted (or diagnosed) well but could not explain why.
広い意味で、AIシステムの説明可能性は、1980年代の「古い」あるいは論理的なAI研究の時代には、知識ベースのシステムがうまく予測（あるいは診断）してもその理由を説明できない場合に、すでに中心的な議論となっていた。
For example, the work of Clancy showed that being able to explain predictions requires far more knowledge than just making correct predictions (Clancey, 1982).
例えば、クランシーの研究は、予測を説明できるようになるには、単に正しい予測をするよりもはるかに多くの知識が必要であることを示した（クランシー、1982年）。
The recent boom in big data and computational power have brought AI performance to a new level, but researchers in the broader AI community have again realized the importance of Explainable AI in recent years (Gunning, 2017), which aims to address a wide range of AI explainability problems in deep learning, computer vision, autonomous driving systems, and natural language processing tasks.
近年のビッグデータと計算能力のブームにより、AIの性能は新たなレベルに達しているが、広範なAIコミュニティの研究者は近年、深層学習、コンピュータビジョン、自律走行システム、自然言語処理タスクにおける幅広いAI説明可能性問題の解決を目指す「説明可能AI」の重要性に改めて気付いている（Gunning, 2017）。
As an essential branch of AI research, this also highlights the importance of the IR
また、AI研究の本質的な一分野として、このことはIRの重要性を浮き彫りにしている。

## 1.3. Classification of the Methods 1.3. 手法の分類

In this survey, we provide a classification taxonomy of existing explainable recommendation methods, which can help readers to understand the state-of-the-art of explainable recommendation research.
本調査では、既存の説明可能な推薦手法の分類法を提供し、読者が説明可能な推薦研究の最先端を理解する一助とする。
Specifically, we classify existing explainable recommendation research with two orthogonal dimensions:
具体的には、既存の説明可能な推薦手法の研究を2つの直交する次元で分類する。

1. The information source or display style of the explanations (e.g., textual sentence explanation, or visual explanation), which represents the human-computer interaction (HCI) perspective of explainable recommendation research, and 2) the model to generate such explanations, which represents the machine learning (ML) perspective of explainable recommendation research.
   1）説明の情報源や表示方法（例：文章による説明、視覚的な説明）、2）説明を生成するモデル、これは説明可能な推薦手法の機械学習（ML）の視点である。
   Potential explainable models include the nearest-neighbor, matrix factorization, topic modeling, graph models, deep learning, knowledge reasoning, association rule mining, and others.
   説明可能なモデルとしては、最近傍モデル、行列分解、トピックモデリング、グラフモデル、深層学習、知識推論、アソシエーションルールマイニングなどが考えられる。

With this taxonomy, each combination of the two dimensions refers to a particular sub-direction of explainable recommendation research.
この分類法では、2つの次元のそれぞれの組み合わせが、説明可能なレコメンデーション研究の特定のサブディレクションを指す。
We should note that there could exist conceptual differences between “how explanations are presented (display style)” and “the type of information used for explanations (information source)”.
ただし、「説明の見せ方（表示スタイル）」と「説明のための情報の種類（情報源）」には概念的な差異が存在する可能性がある。
In the context of explainable recommendation, however, these two principles are closely related to each other because the type of information usually determines how the explanations can be displayed.
しかし、説明可能な推薦の文脈では、情報の種類によって説明の表示方法が決まることが多いため、この2つの原則は互いに密接に関連している。
As a result, we merge these two principles into a single classification dimension.
その結果、この2つの原則を1つの分類次元に統合する。
Note that among the possibly many classification taxonomies, this is just one that we think would be appropriate to organize the research on explainable recommendation, because it considers both HCI and ML perspectives of explainable recommendation research.
この分類は、説明可能な推薦の研究において、HCIとMLの両方の視点を考慮したものであり、説明可能な推薦に関する研究を整理するのに適切なものであると考えられる。

Table 1.1 shows how representative explainable recommendation research is classified into different categories.
表 1.1 は、代表的な説明可能推薦の研究がどのように分類されるかを示している。
For example, the Explicit Factor Model (EFM) for explainable recommendation (Zhang et al., 2014a) developed a matrix factorization method for explainable recommendation, which provides an explanation sentence for the recommended item.
例えば、説明可能な推薦のための明示的因子モデル（EFM）（Zhang et al., 2014a）は、推薦項目の説明文を提供する説明可能な推薦のための行列因数分解法を開発したものである。
As a result, it falls into the category of “matrix factorization with textual explanation”.
その結果、「テキストによる説明を伴う行列因子分解」の範疇に入る。
The Interpretable Convolutional Neural Network approach (Seo et al., 2017), on the other hand, develops a deep convolutional neural network model and displays item features to users as explanations, which falls into the category of “deep learning with user
一方、Interpretable Convolutional Neural Network approach (Seo et al., 2017) は、深い畳み込みニューラルネットワークモデルを開発し、アイテム特徴を説明としてユーザーに表示するもので、「ユーザーによる深い学習」のカテゴリに該当する。

## 1.4. Explainability and Effectiveness 1.4. 説明のしやすさと有効性

Explainability and effectiveness could sometimes be conflicting goals in model design that we have to trade-off (Ricci et al., 2011), i.e., we can either choose a simple model for better explainability, or choose a complex model for better accuracy while sacrificing the explainability.
すなわち，説明性を高めるために単純なモデルを選ぶか，説明性を犠牲にして精度を高めるために複雑なモデルを選ぶか，ということである．
While recent evidence also suggests that these two goals may not necessarily conflict with each other when designing recommendation models (Bilgic et al., 2004; Zhang et al., 2014a).
しかし，最近の証拠によれば，推薦モデルを設計する際に，この2つの目標は必ずしも相反しない可能性があることも示唆されている（Bilgic et al.2004; Zhang et al.2014a）．
For example, state-ofthe-art techniques – such as the deep representation learning approaches – can help us to design recommendation models that are both effective and explainable.
例えば、深層表現学習アプローチなどの最先端技術は、効果的かつ説明可能なレコメンデーションモデルを設計するのに役立つと考えられます。
Developing explainable deep models is also an attractive direction in the broader AI community, leading to progress not only in explainable recommendation research, but also in fundamental explainable machine learning problems.
また、説明可能なディープモデルの開発は、より広いAIコミュニティにおいても魅力的な方向性であり、説明可能なレコメンデーション研究のみならず、説明可能な機械学習の基本問題においても進展が期待できる。

When introducing each explainable recommendation model in the following sections, we will also discuss the relationship between explainability and effectiveness in personalized recommendations.
以下、各説明可能なレコメンデーションモデルを紹介する際に、説明可能性とパーソナライズドレコメンデーションにおける有効性の関係についても言及する。

## 1.5. Explainability and Interpretability 1.5. 説明可能性と解釈可能性

Explainability and interpretability are closely related concepts in the literature.
説明可能性と解釈可能性は、文献上では密接に関連した概念である。
In general, interpretability is one of the approaches to achieve explainability.
一般に、解釈可能性は説明可能性を実現するためのアプローチの1つである。
More specifically, Explainable AI (XAI) aims to develop models that can explain their (or other model’s) decisions for system designers or normal users.
より具体的には、説明可能なAI（XAI）は、システム設計者や一般ユーザーに対して、自分（または他のモデル）の判断を説明できるモデルを開発することを目的としている。
To achieve the goal, the model can be either interpretable or non-interpretable.
この目標を達成するために、モデルには解釈可能なものと解釈不可能なものがある。
For example, interpretable models (such as interpretable machine learning) try to develop models whose decision mechanism is locally or globally transparent, and in this way, the model outputs are usually naturally explainable.
例えば、解釈可能なモデル（解釈可能な機械学習など）は、その決定メカニズムが局所的または大域的に透明なモデルを開発しようとするものであり、このようにすれば、モデルの出力は通常自然に説明可能である。
Prominent examples of interpretable models include many linear models such as linear regression and tree-based models such as decision trees.
解釈可能なモデルの代表例としては、線形回帰などの線形モデルや決定木などの木型モデルがある。
Meanwhile, interpretability is not the only way to achieve explainability, e.g., some models can reveal their internal decision mechanism for explanation purpose with complex explanation techniques, such as neural attention mechanisms, natural language explanations, and many post-hoc explanation models, which are widely used in information retrieval, natural language processing, computer vision, graph analysis, and many other tasks.
一方、解釈可能性は説明可能性を達成する唯一の方法ではない、例えば、いくつかのモデルは、情報検索、自然言語処理、コンピュータビジョン、グラフ解析、および他の多くのタスクで広く使用されている神経注意メカニズム、自然言語説明、および多くのポストホック説明モデルなどの複雑な説明技術で説明目的のために内部決定メカニズムを明らかにすることができます。
Researchers and practitioners may design and select appropriate explanation methods to achieve explainable AI for different tasks.
研究者や実務者は、異なるタスクに対して説明可能なAIを実現するために、適切な説明手法を設計し、選択することができる。

## 1.6. How to Read the Survey 1.6. アンケートの読み方

Potential readers of the survey include both researchers and practitioners interested in explainable recommendation systems.
本調査の読者には、説明可能な推薦システムに関心のある研究者と実務家の両方が含まれる。
Readers are encouraged to prepare with basic understandings of recommender systems, such as content-based recommendation (Pazzani and Billsus, 2007), collaborative filtering (Ekstrand et al., 2011), and evaluation of recommender systems (Shani and Gunawardana, 2011).
読者は、コンテンツベース・レコメンデーション (Pazzani and Billsus, 2007) や協調フィルタリング (Ekstrand et al., 2011) 、推薦システムの評価 (Shani and Gunawardana, 2011) など推薦システムの基礎知識を準備することが推奨される。
It is also beneficial to read other related surveys such as explanations in recommender systems from a user study perspective (Tintarev and Masthoff, 2007a), interpretable machine learning (Lipton, 2018; Molnar, 2019), as well as explainable AI in general (Gunning, 2017; Samek et al., 2017).
また、ユーザー調査の観点からの推薦システムにおける説明（Tintarev and Masthoff, 2007a）、解釈可能な機械学習（Lipton, 2018; Molnar, 2019）、さらには説明可能なAI一般（Gunning, 2017; Samek et al.）

The following part of the survey will be organized as follows.
以下、本調査の一部は以下のように構成される。
In Section 2 we will review explainable recommendation from a userinteraction perspective.
第 2 章では、ユーザインタラクションの観点から説明可能なレコメンデーションについて概説す る。
Specifically, we will discuss different information sources that can facilitate explainable recommendation, and different display styles of recommendation explanation, which are closely related with the corresponding information source.
具体的には、説明可能な推薦を促進する様々な情報源と、対応する情報源と密接に関連する推薦説明の様々な表示スタイルについて述べる。
Section 3 will focus on a machine learning perspective of explainable recommendation, which will introduce different types of models for explainable recommendation.
第3章では、説明可能なリコメンデーションに関する機械学習の視点に焦点を当て、説明可能なリコメンデーションのための様々なタイプのモデルを導入する。
Section 4 will introduce evaluation protocols for explainable recommendation, while Section 5 introduces how explainable recommendation methods are used in different real-world recommender system applications.
第4節では、説明可能な推薦の評価プロトコルを紹介し、第5節では、説明可能な推薦手法が実際の推薦システムでどのように利用されているかを紹介する。
In Section 6 we will summarize the survey with several important open problems and future directions of explainable recommendation research.
セクション6では、説明可能な推薦の研究におけるいくつかの重要な未解決問題や将来の方向性について調査を総括する。

# 2. Information Source for Explanations 2. 説明のための情報源

In the previous section, we adopted a two-dimensional taxonomy to classify existing explainable recommendation research.
前節では、既存の説明可能なレコメンデーション研究を分類するために、2次元のタクソノミーを採用した。
In this section, we focus on the first dimension, i.e., the information source (or display style) of recommendation explanations.
本節では、第一の次元、すなわち、推薦説明の情報源（あるいは表示スタイル）に注目する。
The second dimension (models
第二の次元（モデル

An explanation is a piece of information displayed to users, explaining why a particular item is recommended.
説明とは、特定のアイテムが推奨される理由を説明する、ユーザーに表示される情報の一部である。
Recommendation explanations can be generated from different information sources and be presented in different display styles (Tintarev and Masthoff, 2015), e.g., a relevant user or item, a radar chart, a sentence, an image, or a set of reasoning rules.
レコメンデーションの説明は、異なる情報源から生成され、異なる表示スタイルで提示されることができる（Tintarev and Masthoff, 2015）。例えば、関連するユーザーやアイテム、レーダーチャート、文章、画像、または推論ルールのセットなどである。
Besides, there could exist many different explanations for the same recommendation.
その上、同じ推薦文に対して多くの異なる説明が存在する可能性がある。

For example, Zhang et al. (2014a) generated (personalized) textual sentences as explanations to help users understand each recommendation; Wu and Ester (2015), Zhang (2015), and Al-Taie and Kadry (2014) provided topical word clouds to highlight the key features of a recommended item; Chen et al.
例えば、Zhangら（2014a）は、ユーザーが各レコメンドを理解するための説明として（パーソナライズされた）テキスト文を生成し、Wu and Ester（2015）、Zhang（2015）、Al-Taie and Kadry（2014）は、推奨アイテムの主要な特徴を強調するためのトピカルワードクラウドを、Chenら（2014a）は、レコメンドを説明するテキストを生成し、Chenら（2015a）は、推奨アイテムの主要な特徴を強調するテキストを提供した。
(2019b) proposed visually explainable recommendations, where certain regions of a product image are highlighted as the visual explanations; Sharma and Cosley (2013) and Quijano-Sanchez et al. (2017) generated a list of social friends who also liked the recommended product as social explanations.
(2019b) は、商品画像の特定の領域を視覚的説明として強調する視覚的に説明可能なレコメンデーションを提案し、Sharma and Cosley (2013) と Quijano-Sanchez et al. (2017) は、推奨商品を同じく好きなソーシャルフレンドのリストを社会的説明として生成しました。
In early research stages, Herlocker et al. (2000), Bilgic and Mooney (2005), and Tintarev and Masthoff (2007b) and McSherry (2005) adopted statistical histograms or pie charts as explanations to help users understand the rating distribution and the pros
初期の研究段階では、Herlockerら（2000）、Bilgic and Mooney（2005）、Tintarev and Masthoff（2007b）、McSherry（2005）が、統計的ヒストグラムや円グラフを説明に採用して、ユーザーが評価分布や長所を理解できるようにしました。

In this section, we provide a summary of the different types of recommendation explanations to help readers understand what an explanation can look like in real-world settings.
この章では、読者が実世界でどのような説明が可能かを理解するために、様々なタイプの推薦説明の要約を提供する。
We also categorize the related work according to different explanation styles.
また、説明のスタイル別に関連する研究を分類する。
More specifically, the following subsections present an overview of several frequently seen explanations in existing systems.
具体的には、以下のサブセクションで、既存のシステムで頻繁に見られるいくつかの説明の概要を紹介する。

## 2.1. Relevant User or Item Explanation 2.1. 該当するユーザーまたは項目の説明

We start from the very early stages of recommendation explanation research.
我々は推薦説明の研究の非常に初期の段階からスタートする。
In this section, we introduce explainable recommendation based on user- and item-based collaborative filtering (Cleger-Tamayo et al., 2012; Resnick et al., 1994; Sarwar et al., 2001; Zanker and Ninaus, 2010) – two fundamental methods for personalized recommendation.
ここでは、個人向け推薦の基本的な手法であるユーザーベース協調フィルタリングとアイテムベース協調フィルタリング（Cleger-Tamayo et al.2012; Resnick et al.1994; Sarwar et al.2001; Zanker and Ninaus, 2010）に基づく説明可能推薦について紹介する。
Extensions of the two basic methods will also be introduced in this section.
本節では、この2つの基本的な手法の拡張版についても紹介する。

User-based and item-based explanations are usually provided based on users’ implicit or explicit feedback.
ユーザベースおよびアイテムベースの説明は、通常、ユーザの暗黙的または明示的なフィードバックに基づいて行われる。
In user-based collaborative filtering (Resnick et al., 1994), we first find a set of similar users (i.e., neighbors) for the target user.
ユーザーベースの協調フィルタリング（Resnick et al., 1994）では、まずターゲットユーザーの類似ユーザー（すなわち、近隣ユーザー）の集合を見つける。
Once the algorithm recommends an item to the target user, the explanation is that the user is similar to a group of “neighborhood” users, and these neighborhood users made good ratings on the recommended item.
アルゴリズムがターゲットユーザにアイテムを推薦すると、そのユーザは「近隣」ユーザのグループに類似しており、これらの近隣ユーザは推薦されたアイテムに対して良い評価を行ったと説明される。
For example, Herlocker et al. (2000) compared the effectiveness of different display styles for explanations in user-based collaborative filtering.
例えば、Herlockerら（2000）は、ユーザベースの協調フィルタリングにおける説明文の表示スタイルの違いによる効果を比較した。
In this research, explanations can be displayed as an aggregated histogram of the neighbors’ ratings, or be displayed as the detailed ratings of the neighbors, as shown in Figure 2.2.
この研究では、図2.2に示すように、説明は近隣ユーザーの評価を集約したヒストグラムとして表示することも、近隣ユーザーの詳細な評価として表示することも可能である。
Recent model-based explainable recommendation approaches can generate more personalized and meticulously designed explanations than this, but this research illustrated the basic ideas of providing explanations in recommender systems.
最近のモデルベース説明型推薦アプローチでは、これよりもパーソナライズされたきめ細かい説明を生成できるが、本研究は推薦システムにおける説明提供の基本的な考え方を示したものである。

In item-based collaborative filtering (Sarwar et al., 2001), explanations can be provided by telling the user that the recommended item is similar to some other items the user liked before, as shown in the left panel of Figure 2.3, where several highly rated movies by the user (4 or 5 stars) are shown as explanations.
アイテムベースの協調フィルタリング（Sarwar et al.2001）では、図2.3の左図のように、ユーザが高く評価した映画（4つか5つ星）をいくつか説明として表示し、推奨アイテムがユーザが以前気に入った他のアイテムと似ていると伝えることで説明を提供することができる。
More intuitively, as in Figure 2.1, for the recommended item (i.e., the camera lens), a relevant-user explanation tells Bob that similar users William and Fred also bought this item, while a relevant-item explanation persuades Bob to buy the lens by showing the camera he already bought before.
より直感的には、図2.1のように、おすすめ商品（カメラレンズ）に対しては、関連ユーザー説明で、類似ユーザーのウィリアムやフレッドもこの商品を買っていることを伝え、関連アイテム説明で、ボブが以前すでに買ったカメラを示すことでレンズを買うよう説得しているのです。

To study how explanations help in recommender systems, Tintarev (2007) developed a prototype system to study the effect of different types of explanations, especially the relevant-user and relevant-item explanations.
Tintarev (2007) は、推薦システムにおいて説明がどのように役立つかを研究するために、異なるタイプの説明、特に関連ユーザ説明と関連項目説明の効果を研究するためのプロトタイプシステムを開発した。
In particular, the author proposed seven benefits of providing recommendation explanations, including transparency, scrutability, trustworthiness, effectiveness, persuasiveness, efficiency, and satisfaction.
特に、推薦文の説明には、透明性、精査性、信頼性、有効性、説得性、効率性、満足度の7つの利点があることを提案した。
Based on their user study, the author showed that providing appropriate explanations can indeed benefit the recommender system over these seven perspectives.
著者は、ユーザー調査に基づき、適切な説明を行うことで、これら7つの観点で実際に推薦システムに利益をもたらすことができることを示した。

Usually, relevant-item explanations are more intuitive for users to understand because users are familiar with the items they interacted before.
通常、関連項目の説明は、ユーザが以前に対話した項目に慣れているため、ユーザにとってより直感的に理解しやすい。
As a result, these items can serve as credible explanations for users.
その結果、これらの項目は、ユーザーにとって信頼できる説明として機能することができます。
Relevant-user explanations, however, could be less convincing because the target user may know nothing about other “similar” users at all, which may decrease the trustworthiness of the explanations (Herlocker et al., 2000).
しかし、関連するユーザーの説明は、ターゲットユーザーは他の「類似した」ユーザーについて全く知らないかもしれないので、説明の信頼性を低下させる可能性がある（Herlocker et al.）
Besides, disclosing other users’ information may also cause privacy problems in commercial systems.
その上、他のユーザの情報を開示することは、商用システムにおいてプライバシーの問題を引き起こす可能性もある。
This problem drives relevant-user explanation into a new direction, which leverages social friend information to provide social explanations (Ren et al., 2017; Tsai and Brusilovsky, 2018).
この問題は、関連するユーザー説明を、社会的な友人情報を活用して社会的な説明を提供するという新しい方向に向かわせる（Ren et al., 2017; Tsai and Brusilovsky, 2018）。
For example, we can show a user with her friends’ public interest as explanations for our social recommendations.
例えば、社会的推薦の説明として、彼女の友人の公共的関心を持つユーザーを表示することができる。
In the following, we will review this research direction in the social explanation section (Section 2.6).
以下、社会的説明の項でこの研究の方向性を確認する（2.6 節）。

## 2.2. Feature-based Explanation 2.2. 特徴に基づく説明

The feature-based explanation is closely related to content-based recommendation methods.
特徴量に基づく説明は、内容量に基づく推薦手法と密接な関係がある。
In content-based recommendation, the system provides recommendations by matching the user profile with the content features of candidate items (Cramer et al., 2008; Ferwerda et al., 2012; Pazzani and Billsus, 2007).
コンテンツベースド・レコメンデーションでは、ユーザプロファイルと候補アイテムのコンテンツ特徴をマッチングさせることで推薦を行う（Cramer et al., 2008; Ferwerda et al., 2012; Pazzani and Billsus, 2007）。
Content-based recommendations are usually intuitive to explain based on the features.
コンテンツに基づく推薦では、通常、特徴に基づいて直感的に説明することができる。

Depending on the application scenario, content-based recommendations can be generated from different item features.
アプリケーションのシナリオに応じて、コンテンツベースのレコメンデーションは、異なるアイテムの特徴から生成することができる。
For example, movie recommendations can be generated based on movie genres, actors, or directors; while book recommendations can be provided based on book types, price, or authors.
例えば、映画の推薦文は、映画のジャンル、俳優、監督に基づいて生成され、本の推薦文は、本の種類、価格、著者に基づいて提供されることが可能である。
A conventional paradigm for feature-based explanation is to show users with the features that match the user’s profile.
特徴に基づく説明の従来のパラダイムは、ユーザーのプロファイルにマッチする特徴を持つユーザーを表示することである。

Vig et al. (2009) adopted movie tags as features to generate recommendations and explanations, as shown in Figure 2.4.
Vig et al. (2009)は、図 2.4 に示すように、映画のタグを特徴量として採用し、推薦と説明を生成している。
To explain the recommended movie, the system displays the movie features and tells the user why each feature is relevant to her.
推薦された映画を説明するために、システムは映画の特徴を表示し、各特徴がなぜ自分に関係するのかをユーザに伝える。
The authors also designed a user study and showed that providing feature-based explanations can help to improve the effectiveness of recommendations.
また、著者らはユーザー調査を設計し、特徴に基づく説明を行うことで推薦の効果を高めることができることを示した。
Furthermore, Ferwerda et al. (2012) conducted a user study, and the results supported the idea that explanations are highly correlated with user trust and satisfaction in the recommendations.
さらに，Ferwerda et al. (2012)は，ユーザ調査を行い，説明がユーザの推薦に対する信頼や満足度と高い相関があることを支持する結果を得た．

Content features can be displayed in many different explanation styles.
コンテンツの特徴は、さまざまな説明スタイルで表示することができます。
For example, Hou et al. (2018) used radar charts to explain why an item is recommended and why others are not.
例えば、Houら（2018）は、あるアイテムが推奨される理由と他のアイテムが推奨されない理由をレーダーチャートで説明しました。
As shown in Figure 2.5, a recommendation is explained in that most of its aspects satisfy the preference of the target user.
図 2.5 に示すように、レコメンデーションは、そのほとんどの側面が対象ユーザーの好みを満たしていることを説明するものである。

User demographic information describes the content features of users, and the demographic features can also be used to generate feature-based explanations.
ユーザーのデモグラフィック情報は、ユーザーのコンテンツ特徴を記述し、デモグラフィック特徴は、特徴ベースの説明を生成するためにも使用することができる。
Demographic-based recommendation (Pazzani, 1999) is one of the earliest approaches to personalized recommendation systems.
デモグラフィックベースの推薦（Pazzani, 1999）は、パーソナライズされた推薦システムに対する最も初期のアプローチの一つである。
Recently, researchers have also integrated demographic methods into social media to provide product recommendations in social environments (Zhao et al., 2014, 2016).
最近では、研究者は人口統計学的手法をソーシャルメディアに統合し、社会環境における商品推薦を提供することも行っています（Zhao et al.）

The demographic-based approach makes recommendations based on user demographic features such as age, gender, and residence location.
人口統計学に基づくアプローチは、年齢、性別、居住地などのユーザーの人口統計学的特徴に基づいて推薦を行うものである。
Intuitively, an item recommended based on demographic information can be explained by the demographic feature(s) that triggered the recommendation, e.g., by telling the user that “80% of customers in your age bought this product”.
直感的には、デモグラフィック情報に基づいて推薦されたアイテムは、推薦のきっかけとなったデモグラフィック特徴（複数可）、例えば「あなたの年代の顧客の80%がこの商品を購入した」とユーザーに伝えることで説明できる。
Zhao et al. (2014) represented products and users in the same demographic feature space, and used the weights of the features learned by a ranking function to explain the results; Zhao et al. (2016) further explored demographic information in social media environment for product recommendation with feature-based explanations.
Zhaoら（2014）は、商品とユーザーを同じデモグラフィック特徴空間で表現し、ランキング関数で学習した特徴の重みを使って説明した。Zhaoら（2016）はさらに、ソーシャルメディア環境におけるデモグラフィック情報を特徴ベースの説明で商品推奨に利用することを検討した。

## 2.3. Opinion-based Explanation 2.3. 意見に基づく説明

More and more user-generated contents have been accumulating on the Web, such as e-commerce reviews and social media posts, which help users to express their opinion on certain items or aspects.
eコマースのレビューやソーシャルメディアの投稿など、ユーザーが特定のアイテムや側面について意見を表明するのに役立つ、ユーザー生成コンテンツがウェブ上にますます蓄積されてきています。
Researchers have shown that such information is quite beneficial in user profiling and recommendation (McAuley and Leskovec, 2013; Zheng et al., 2017).
研究者たちは、このような情報がユーザーのプロファイリングや推薦にかなり有益であることを示しています（McAuley and Leskovec, 2013; Zheng et al.）
Besides, it helps to generate finer-grained and more reliable explanations, which benefit users to make more informed decisions (Li et al., 2017; Zhang et al., 2014a).
その上、それはより細かい、より信頼性の高い説明を生成するのに役立ち、ユーザーがより多くの情報に基づいた意思決定を行うのに役立ちます（Liら、2017;Zhangら、2014a）。
With this motivation, many models have been proposed to explain recommendations based on user-generated texts.
このような動機から、ユーザーが作成したテキストに基づくレコメンデーションを説明するためのモデルが数多く提案されている。

Methods in this direction can be broadly classified into aspect-level and sentence-level approaches, according to how the explanations are displayed.
この方向の手法は、説明文の表示方法によって、アスペクトレベルのアプローチと文レベルのアプローチに大別される。
See Figure 2.1 for example, where aspect-level models present item aspects (such as color, quality) and their scores as explanations, while the sentence-level models directly present an explanation sentence to users about why the camera lens is recommended.
例えば図2.1を見ると、アスペクトレベルのモデルは項目の側面（色や品質など）とそのスコアを説明として提示し、センテンスレベルのモデルはそのカメラレンズがなぜおすすめなのかという説明文を直接ユーザに対して提示するものである。
We will focus on aspect-level explanation in this subsection, while sentence-level explanations will be introduced in the following subsection together with other natural language generation-based explanation models.
本節ではアスペクトレベルの説明に焦点を当て、文レベルの説明は他の自然言語生成に基づく説明モデルとともに次の節で紹介する。

The aspect-level explanation is similar to feature-based explanation, except that aspects are usually not directly available in an item or user profile.
アスペクトレベルの説明は特徴ベースの説明と似ているが、アスペクトは通常アイテムやユーザープロファイルで直接利用できない点が異なる。
Instead, they are extracted or learned as part of the recommendation model from – e.g., the reviews – and the aspects can be paired up with consumer opinions to express a clear sentiment on the aspect.
その代わり、それらは推薦モデルの一部として-例えば、レビュー-から抽出されるか、学習される。そして、アスペクトは消費者の意見と対になって、そのアスペクトに対する明確な感情を表現することができる。

Researchers in the sentiment analysis community have explored both data mining and machine learning techniques for aspect-level sentiment analysis, which aims to extract aspect-sentiment pairs from text.
感情分析コミュニティの研究者は、テキストからアスペクトと感情のペアを抽出することを目的としたアスペクトレベル感情分析のためのデータマイニングと機械学習技術の両方を模索してきました。
For example, Hu and Liu (2004) proposed a frequent feature mining approach to aspect-level sentiment analysis, and Lu et al. (2011) proposed an optimization approach to construct context-aware sentiment lexicons automatically.
例えば、Hu and Liu (2004) はアスペクトレベル感情分析のための頻出特徴マイニングアプローチを提案し、Lu et al. (2011) は文脈を考慮した感情語彙を自動的に構築する最適化アプローチを提案しました。
A comprehensive review on sentiment analysis and opinion mining is summarized in Liu (2012).
また、Liu (2012)では、センチメント分析とオピニオンマイニングに関する包括的なレビューが要約されている。
Based on these research efforts, Zhang et al. (2014b) developed a phrase-level sentiment analysis toolkit named Sentires1 to extract “aspect–opinion–sentiment” triplets from reviews of a product domain.
これらの研究成果に基づいて、Zhangら（2014b）は、製品ドメインのレビューから「アスペクト-意見-センチメント」のトリプルを抽出するSentires1というフレーズレベルのセンチメント分析ツールキットを開発しました。
For example, given large-scale user reviews about mobile phones, the toolkit can extract triplets such as “noise–high–negative”, “screen–clear–positive”, and “battery_life– long–positive”.
例えば、携帯電話に関する大規模なユーザーレビューが与えられた場合、このツールキットは「noise-high-negative」、「screen-clear-positive」、「battery_life-long-positive」といったトリプレットを抽出することができる。
The toolkit can also detect the contextual sentiment of the opinion words under different aspect words.
また、このツールキットは、異なるアスペクト語の下にある意見語の文脈上のセンチメントを検出することができる。
For example, though “noise” paired with “high” usually represents a negative sentiment, when “quality” is paired with “high”, however, it instead shows a positive sentiment.
例えば、"noise "と "high "の組み合わせは通常ネガティブな感情を表すが、"quality "と "high "の組み合わせでは、ポジティブな感情を表すようになる。

Based on the dictionary of aspect–opinion–sentiment triplets constructed by the program, it can further detect which triplets are contained in a review sentence.
さらに、このプログラムによって構築されたアスペクト・意見・感情の三段論法の辞書に基づいて、レビュー文にどの三段論法が含まれるかを検出することができる。
Based on this toolkit, researchers developed different models for explainable recommendation.
このツールキットに基づき、研究者は説明可能な推薦のための様々なモデルを開発した。
For example, Zhang et al. (2014a) proposed an explicit factor model for explainable recommendation, which presents aspect-opinion word clouds as explanations, such as “bathroom–clean”, to highlight the performance of the recommended item on certain aspects.
例えば、Zhangら（2014a）は、説明可能な推薦のための明示的な要因モデルを提案し、「bathroom-clean」のような説明としてアスペクト-オピニオンワードクラウドを提示し、ある側面に関する推薦項目の性能を強調する。
Wu and Ester (2015) developed a topic modeling approach for explainable hotel recommendations on TripAdvisor, which generates topical word cloud explanations on three hotel features (Location, Service, and Room), as shown in Figure 2.6.
Wu and Ester（2015）は、TripAdvisorにおける説明可能なホテル推薦のためのトピックモデリングアプローチを開発し、図2.6に示すように、3つのホテルの特徴（Location, Service, Room）に関するトピックワードクラウド説明を生成している。
The word size in the word cloud is proportional to the sentiment opinion of the aspect.
ワードクラウド内の単語の大きさは、アスペクトのセンチメント意見に比例する。
Ren et al. (2017) proposed a social collaborative viewpoint regression (sCVR) model for predicting item ratings based on user opinions and social relations, which provides viewpoints as explanations, where a viewpoint refers to a topic with a specific sentiment label.
Renら（2017）は、ユーザーの意見と社会的関係に基づいてアイテムの評価を予測するための社会的協調視点回帰（sCVR）モデルを提案し、説明として視点を提供し、視点は特定のセンチメントラベルを持つトピックを参照します。
Combined with trusted user relations, it helps users to understand their friends’ opinion about a particular item.
信頼できるユーザー関係と組み合わせることで、ユーザーが特定のアイテムに関する友人の意見を理解するのに役立つ。
Wang et al. (2018b) developed a multi-task learning solution for explainable recommendation, where two companion learning tasks of user preference modeling for recommendation and opinionated content modeling for explanation are integrated via a joint tensor factorization framework.
Wangら（2018b）は、説明可能な推薦のためのマルチタスク学習ソリューションを開発し、推薦のためのユーザー嗜好モデリングと説明のための意見付きコンテンツモデリングの2つのコンパニオン学習タスクがジョイントテンソル因子分解のフレームワークを介して統合されています。
We will introduce more about the model details in the explainable recommendation model section (Section 3).
モデルの詳細については、説明可能な推薦モデルのセクション（セクション3）で紹介する。

## 2.4. Sentence Explanation 2.4. 文の説明

Sentence-level approach provides explanation sentences to users.
文レベルでのアプローチは、ユーザーに説明文を提供するものである。
This approach can be further classified into template-based approach and generation-based approach.
このアプローチはさらに、テンプレートベースのアプローチとジェネレーションベースのアプローチに分類される。

Template-based approach first defines some explanation sentence templates, and then fills the templates with different words to personalize them for different users.
テンプレートベースのアプローチは、まずいくつかの説明文のテンプレートを定義し、そのテンプレートに異なる単語を埋め込んで、異なるユーザー向けにパーソナライズするものである。
For example, Zhang et al. (2014a) constructed explanations by telling the user that You might be interested in feature, on which this product performs well.
例えば、Zhangら(2014a)は、「あなたは、この製品がよく機能する特徴に興味があるかもしれません」とユーザーに伝えることで、説明を構築した。
In this template, the feature will be selected based on personalization algorithms to construct a personalized explanation, as shown in Figure 2.7.
このテンプレートでは、図2.7に示すように、パーソナライズアルゴリズムに基づいてfeatureが選択され、パーソナライズされた説明が構築されることになる。
Based on the templates, the model can also provide “dis-recommendations” to let the user know why an item is not a good fit, by telling the user You might be interested in feature, on which this product performs poorly.
また、テンプレートに基づき、ある商品がなぜ良くないのかをユーザーに知らせるために、You might be interested in feature, on which this product performs poorを伝える「ディスレコメンデーション」を提供することもできる。
Based on user studies, it shows that providing both recommendation and dis-recommendation explanations improve the persuasiveness and conversion rate of recommender systems.
ユーザー調査に基づき、推薦と非推薦の両方の説明を提供することで、レコメンダーシステムの説得力とコンバージョン率が向上することが示されている。

Wang et al. (2018b) provided template-based explanations based on both feature and opinion words, for example, an explanation for Yelp restaurant recommendation could be Its decor is [neat] [good] [nice].
Wangら（2018b）は、特徴語と意見語の両方に基づくテンプレートベースの説明を提供し、例えば、Yelpレストランの推薦に対する説明は、Its decor is [neat] [good] [nice]となる。
Its sandwich is [grilled] [cajun] [vegan].
そのサンドイッチは[グリル][ケイジャン][ヴィーガン]である。
Its sauce is [good] [green] [sweet], where words in brackets are opinion words selected by the model to describe the corresponding item feature.
ここで、括弧内の単語は、対応する項目の特徴を説明するためにモデルによって選択された意見の単語である。

Tao et al. (2019a) further integrated regression trees to guide the learning of latent factor models, and used the learnt tree structure to explain the recommendations.
Taoら（2019a）はさらに、潜在因子モデルの学習を導くために回帰木を統合し、学習した木構造を使ってレコメンドを説明した。
They added predefined modifiers in front of the selected features to construct template-based explanations, such as We recommend this item to you because its [good
彼らは、選択された特徴の前にあらかじめ定義された修飾語を追加して、テンプレートベースの説明を構築しました。 私たちはこのアイテムをあなたにお勧めします、なぜならその[良い]からです。

Gao et al. (2019) proposed an explainable deep multi-view learning framework to model multi-level features for explanation.
Gaoら（2019）は、説明のために多階層の特徴をモデル化する説明可能な深層多視点学習フレームワークを提案した。
They also adopted feature-based templates to provide explanations, and the features are organized in an industry-level hierarchy named Microsoft Concept Graph.
また、彼らは説明を提供するために特徴ベースのテンプレートを採用し、特徴はMicrosoft Concept Graphという産業レベルの階層で整理されている。
The model improves accuracy and explainability simultaneously, and is capable of providing highly usable explanations in commercial systems.
このモデルは、精度と説明可能性を同時に向上させ、商用システムにおいてユーザビリティの高い説明を提供することが可能である。
Technical details of the above models will be introduced in the explainable recommendation model section.
上記のモデルの技術的な詳細については、説明可能な推薦モデルの項で紹介する。

Based on natural language generation techniques, we can also generate explanation sentences directly without using templates.
自然言語生成技術に基づけば、テンプレートを使わずに直接説明文を生成することもできる。
For example, Costa et al. (2018) generated explanation sentences based on long-short term memory (LSTM).
例えば、Costaら（2018）は、LSTM（long-short term memory）に基づいて説明文を生成した。
By training over large-scale user reviews, the model can generate reasonable review sentences as explanations, as shown in Figure 2.8.
大規模なユーザーレビューに対して学習を行うことで、図2.8に示すように、説明文として妥当なレビュー文を生成できるモデルである。
Inspired by how people explain word-of-mouth recommendations, Chang et al. (2016) proposed a process to combine crowdsourcing and computation to generate personalized natural language explanations.
人々が口コミの推薦文をどのように説明するかに触発され、Changら（2016）はクラウドソーシングと計算を組み合わせてパーソナライズされた自然言語による説明を生成するプロセスを提案した。
The authors also evaluated the generated explanations in terms of efficiency, effectiveness, trust, and satisfaction.
また、著者らは、生成された説明を効率、有効性、信頼、満足度の観点から評価した。
Li et al. (2017) leveraged gated recurrent units (GRU) to generate tips for a recommended restaurant in Yelp.
Liら(2017)は、Yelpのおすすめレストランのヒントを生成するためにゲーテッドリカレントユニット(GRU)を活用した。
According to the predicted ratings, the model can control the sentiment attitude of the generated tips, which help users understand the key features of the recommended items.
予測された評価に従って、モデルは生成されたヒントのセンチメント態度を制御することができ、ユーザーは推奨されたアイテムの主要な特徴を理解するのに役立つ。
Lu et al. (2018b) proposed a multi-task recommendation model, which jointly learns to perform rating prediction and recommendation explanation.
Luら(2018b)は、評価予測と推薦説明を行うために共同学習するマルチタスク推薦モデルを提案した。
The explanation module employs an adversarial sequence to sequence learning technique to encode, generate, and discriminate the user and item reviews.
説明モジュールは、ユーザーとアイテムのレビューを符号化し、生成し、識別するために、敵対的シーケンスからシーケンスへの学習技法を採用している。
Once trained, the generator can be used to generate explanation sentences.
一度学習した生成器は、説明文の生成に利用できる。

A lot of explanation generation approaches rely on user reviews as the training corpus to train an explanation generation model.
多くの説明生成アプローチは、説明生成モデルを学習するための学習コーパスとして、ユーザレビューに依存している。
However, user reviews are noisy, because not all of the sentences in a review are explanations or justifications of the users’ decision-making process.
しかし、ユーザーレビューは、レビュー内のすべての文がユーザーの意思決定プロセスの説明や正当化であるとは限らないため、ノイズが多い。
Motivated by this problem, Chen et al. (2019a) proposed a hierarchical sequence-to-sequence model (HSS) for personalized explanation generation, which includes an auto-denoising mechanism that selects sentences containing item features for model training.
この問題に動機づけられ、Chenら（2019a）は、パーソナライズされた説明生成のための階層的配列間モデル（HSS）を提案し、これはモデル学習のために項目特徴を含む文を選択する自動デノイズ機構を含んでいる。
Ni et al. (2019) introduced new datasets and methods to address this recommendation justification task.
Niら（2019）は、この推薦正当化タスクに対応するための新しいデータセットと方法を紹介した。
In terms of data, the authors proposed an extractive approach to identify review segments that justify users’ intentions.
データの面では、著者らはユーザーの意図を正当化するレビューセグメントを特定する抽出的なアプローチを提案した。
In terms of generation, the authors proposed a reference-based Seq2Seq model with aspect-planning to generate explanations covering different aspects.
生成の面では、著者らは、異なる側面をカバーする説明を生成するために、アスペクトプランニングを用いた参照ベースのSeq2Seqモデルを提案した。
The authors also proposed an aspect-conditional masked language model to generate diverse justifications based on templates extracted from justification histories.
また、正当化履歴から抽出したテンプレートに基づき、多様な正当化を生成するアスペクト条件付きマスク言語モデルを提案した。

## 2.5. Visual Explanation 2.5. 視覚的な説明

To leverage the intuition of visual images, researchers have tried to utilize item images for explainable recommendation.
視覚的なイメージの直感を活用するために、研究者は説明可能な推薦にアイテム画像を活用することを試みている。
In Figure 2.1, for example, to explain to Bob that the lens is recommended because of its collar appearance, the system highlights the image region corresponding to the necklet of the lens.
例えば、図2.1では、ボブに対して、このレンズは襟が見えるのでおすすめだと説明するために、レンズの襟に相当する画像領域をハイライト表示している。

Lin et al. (2019) studied the explainable outfit recommendation problem, for example, given a top, how to recommend a list of bottoms (e.g., trousers or skirts) that best match the top from a candidate collection, and meanwhile generate explanations for each recommendation.
Linら（2019）は、説明可能な服装推薦問題を研究し、例えば、トップスが与えられたとき、候補コレクションからトップスに最もマッチするボトムス（ズボンやスカートなど）のリストを推薦し、一方で各推薦に対する説明を生成する方法を提案した。
Technically, this work proposed a convolutional neural network with a mutual attention mechanism to extract visual features of the outfits, and the visual features are fed into a neural prediction network to predict the rating scores for the recommendations.
技術的には、服装の視覚的特徴を抽出するために相互注意機構を備えた畳み込みニューラルネットワークを提案し、その視覚的特徴をニューラル予測ネットワークに与えて推薦文の評価点を予測します。
During the prediction procedure, the attention mechanism will learn the importance of different image regions, which tell us which regions of the image are taking effect when generating the recommendations, as shown in Figure 2.9(a).
予測手順の間、注意メカニズムは異なる画像領域の重要性を学習し、図2.9（a）に示すように、推薦文を生成する際に画像のどの領域が効果を発揮しているかを教えてくれるようになる。

Chen et al. (2019b) proposed visually explainable recommendation based on personalized region-of-interest highlights, as shown in Figure 2.10.
Chenら（2019b）は、図2.10に示すように、パーソナライズされた関心領域のハイライトに基づく視覚的に説明可能な推薦を提案した。
The basic idea is that different regions of the product image may attract different users.
基本的な考え方は、商品画像の異なる領域が異なるユーザーを惹きつける可能性があるということである。
As shown by the example in Figure 2.9(b), even for the same shirt, some users may care about the collar design while others may pay attention to the pocket.
図2.9（b）の例で示すように、同じシャツでも、襟のデザインを気にするユーザーもいれば、ポケットに注目するユーザーもいるだろう。
As a result, the authors adopted a neural attention mechanism integrated with both image and review information to learn the importance of each region of an image.
そこで筆者らは、画像とレビューの両方の情報を統合したニューラル・アテンション機構を採用し、画像の各領域の重要度を学習することにした。
The important image regions are highlighted in a personalized way as visual explanations for users.
重要な画像領域は、ユーザーへの視覚的説明としてパーソナライズされた方法で強調される。

In general, the research on visually explainable recommendation is still at its initial stage.
一般に、視覚的に説明可能な推薦に関する研究は、まだ初期段階にある。
With the continuous advancement of deep image processing techniques, we expect that images will be better integrated into recommender systems for both better performance and explainability.
今後、深層画像処理技術の進歩に伴い、推薦システムの性能向上と説明可能性の向上のために、画像の活用が進むと考えられる。

## 2.6. Social Explanation 2.6. 社会的説明

As discussed in the previous subsections, a problem of relevant-user explanations is trustworthiness and privacy concerns, because the target user may have no idea about other users who have “similar interests”.
前節で述べたように、関連ユーザ説明の問題点は、対象ユーザが「類似の興味」を持つ他のユーザを知らない可能性があるため、信頼性とプライバシーへの配慮である。
Usually, it will be more acceptable if we tell the user that his
通常、ユーザに「自分の

Papadimitriou et al. (2012) studied human-style, item-style, featurestyle, and hybrid-style explanations in social recommender systems; they also studied geo-social explanations to combine geographical data with social data.
Papadimitriouら（2012）は、社会的推薦システムにおける人間型、項目型、特徴型、ハイブリッド型の説明を研究し、地理データと社会データを結合するジオソーシャル型説明も研究している。
For example, Facebook provides friends in common as explanations when recommending a new friend to a user (see Figure 2.11(b)).
例えば、Facebookでは、ユーザに新しい友達を推薦する際に、共通の友達を説明として提供する（図2.11(b)参照）。
Sharma and Cosley (2013) studied the effects of social explanations in music recommendation by providing the target user with the number of friends that liked the recommended item (see Figure 2.11(b)).
Sharma and Cosley（2013）は、音楽推薦において、推薦されたアイテムに「いいね」を押した友達の数を対象ユーザに提供し、社会的説明の効果を研究した（図2.11（b）参照）。
The authors found that explanations influence the likelihood of users checking out the recommended artists, but there is little correlation between the likelihood and the actual rating for the artist.
著者らは、説明はユーザが推奨されたアーティストをチェックする可能性に影響を与えるが、その可能性と実際のアーティストに対する評価との間にはほとんど相関がないことを発見した。
Chaney et al. (2015) presented social Poisson factorization, a Bayesian model that incorporates a user’s preference with her friends’ latent influence, which provides explainable serendipity to users, i.e., pleasant surprise due to novelty.
Chaneyら（2015）は、ユーザーの嗜好に友人の潜在的影響力を組み込んだベイズモデルであるソーシャルポアソン因数分解を提示し、ユーザーに説明可能なセレンディピティ、すなわち新規性による嬉しい驚きを提供する。

Except for friend recommendation, social explanations also take effect in other social network scenarios.
友人推薦を除き、社会的説明は他のソーシャルネットワークシナリオでも効果を発揮する。
For example, Park et al. (2018) proposed a unified graph structure to exploit both rating and social information to generate explainable product recommendations.
例えば、Parkら（2018）は、説明可能な製品推薦を生成するために、評価と社会的情報の両方を活用する統一グラフ構造を提案しました。
In this framework, a recommendation can be explained based on the target user’s friends who have similar preferences, as shown in Figure 2.12.
このフレームワークでは、図2.12に示すように、嗜好が似ているターゲットユーザーの友人に基づいてレコメンデーションを説明することができる。
Quijano-Sanchez et al. (2017) introduced a social explanation system applied to group recommendation, which significantly increased the likelihood of the user acceptance, the user satisfaction, and the system efficiency to help users make decisions.
Quijano-Sanchezら(2017)は，グループ推薦に適用した社会的説明システムを導入し，ユーザの意思決定を支援するために，ユーザの受容可能性，ユーザの満足度，システムの効率性を大幅に向上させた。
Wang et al. (2014) generates social explanations such as “A and B also like the item”.
Wang ら（2014）は、「A と B もそのアイテムが好きだ」といった社会的説明を生成する。
They proposed to find an optimal set of users as the most persuasive social explanation.
彼らは、最も説得力のある社会的説明として、最適なユーザー集合を見つけることを提案した。
Specifically, a two-phase ranking algorithm is proposed, where the first phase predicts the persuasiveness score of a single candidate user, and the second phrase predicts the persuasiveness score of a set of users based on the predicted persuasiveness of the individual users, by taking the marginal net utility of persuasiveness, credibility of the explanation and reading cost into consideration.
具体的には，説得力の限界純効用，説明の信頼性，読書コストを考慮し，第1フレーズで候補となる単一のユーザの説得力スコアを予測し，第2フレーズで個々のユーザの予測説得力を基にユーザ集合の説得力スコアを予測するという2段階のランキングアルゴリズムが提案された．

## 2.7. Summary 2.7. 概要

In this section, we introduced several styles of recommendation explanations, including:
本節では、推薦説明のスタイルとして、以下のようなものを紹介した。

1. Explanations based on relevant users or items, which present nearest-neighbor users or items as an explanation.
1. 関連するユーザやアイテムに基づく説明：最近傍のユーザやアイテムを説明として提示する。
   They are closely related to the critical idea behind user-based or item-based collaborative filtering methods.
   これは、ユーザベース協調フィルタリングやアイテムベース協調フィルタリングの背後にある重要な考えと密接に関連している。
1. Feature-based explanation, which provides users with the item features that match the target user’s interest profile.
1. 特徴に基づく説明。ターゲットユーザーの興味プロファイルに合致するアイテムの特徴をユーザーに提示する。
   This approach is closely related to content-based recommendation methods.
   この手法は、コンテンツベースの推薦手法と密接な関係がある。
1. Opinion-based explanation, which aggregates users’ collective opinions in user generated contents as explanations.
1. 意見ベース説明：ユーザが作成したコンテンツにユーザの意見を集約し、説明として提供する。
1. Textual sentence explanation, which provides the target users with explanation sentences.
1. テキスト文による説明：ターゲットユーザに説明文を提供する。
   The sentence could be constructed based on pre-defined templates or directly generated based on natural language generation models.
   説明文は、あらかじめ用意されたテンプレートに基づき構成される場合と、自然言語生成モデルに基づき直接生成される場合がある。
1. Visual explanations, which provide users with image-based explanations.
   5）視覚的説明：画像による説明をユーザに提供する。
   The visual explanation could be a whole image or a region-of-interest highlight in the image.
   視覚的説明には、画像全体、または画像中の関心領域のハイライトが使用される。
1. Social explanations, which provide explanations based on the target user’s social relations.
1. 社会的説明：対象ユーザーの社会的関係性に基づいた説明を行う。
   They help to improve user trust in recommendations and explanations.
   推薦や説明に対するユーザーの信頼度を向上させることができる。

It should be noted that while 1 to 3 are usually bonded with certain types of recommendation algorithms, 4 to 6 focus more on how the explanations are shown to users, which are not necessarily generated by one particular type of algorithm.
1〜3がある種の推薦アルゴリズムと結びつくことが多いのに対して、4〜6はユーザーへの説明の見せ方に重点が置かれており、必ずしもある種のアルゴリズムによって生成されているわけではないことに注意が必要である。
In the following section, we will introduce more details of different explainable recommendation models.
以下では、説明可能なレコメンデーションモデルについて詳しく紹介する。

# 3. Explainable Recommendation Models 3. 説明可能なレコメンデーションモデル

In the previous section, we have seen different types of explanations in recommender systems.
前節では、レコメンダーシステムにおけるさまざまなタイプの説明文を見てきた。
Our next step is to describe how such explanations can be generated.
次のステップでは、そのような説明をどのように生成できるかを説明する。

Explainable recommendation research can consider the explainability of either the recommendation methods or the recommendation results.
説明可能なレコメンデーションとは、レコメンデーション手法の説明可能性とレコメンデーション結果の説明可能性のどちらかを考慮する研究である。
When considering the explainability of methods, explainable recommendation aims to devise interpretable models for increased transparency, and such models usually directly lead to the explainability of results.
手法の説明可能性を考える場合、説明可能な推薦とは、透明性を高めるために解釈可能なモデルを考案することを目的とし、そのようなモデルは通常、結果の説明可能性に直接つながる。
In this section, many of the factorization-based, topic modeling, graphbased, deep learning, knowledge-based, and rule mining approaches adopt this research philosophy – they aim to design intrinsic explainable models and understand how the recommendation process works.
本節では、因子分解ベース、トピックモデリング、グラフベース、深層学習、知識ベース、ルールマイニングなどのアプローチの多くがこの研究理念を採用している。彼らは、本質的に説明可能なモデルを設計し、推薦プロセスがどのように機能するかを理解することを目的としている。

Another philosophy for explainable recommendation research is that we only focus on the explainability of the recommendation results.
説明可能な推薦研究のもう一つの理念は、推薦結果の説明可能性だけに注目することである。
In this way, we treat the recommendation model as a blackbox, and develop separate models to explain the recommendation results produced by this blackbox.
このように、推薦モデルをブラックボックスとして扱い、このブラックボックスが生成する推薦結果を説明するためのモデルを別途開発する。
In this section, the post-hoc
本節では、ポストホック

In the following, we first provide a very brief overview of machine learning for general recommender systems, so as to provide readers with necessary background knowledge.
以下では、まず一般的な推薦システムのための機械学習について、必要な背景知識を読者に提供するために、非常に簡単な概要を説明する。
Then we provide a comprehensive survey on explainable recommendation models.
次に、説明可能な推薦モデルに関する包括的なサーベイを提供する。

## 3.1. Overview of Machine Learning for Recommendation 3.1. レコメンデーションのための機械学習の概要

Recent research on model-based explainable recommendation is closely related to machine learning for recommender systems.
モデルベース説明可能推薦に関する最近の研究は、推薦システムのための機械学習と密接な関係がある。
We first provide a brief overview of machine learning for personalized recommendations in this section.
本節ではまず、パーソナライズド・レコメンデーションのための機械学習について簡単に説明する。
One of the classical ML models for recommendation is Latent Factor Model (LFM), based on Matrix Factorization (MF).
推薦のための古典的なMLモデルのひとつに、行列因子分解（Matrix Factorization, MF）に基づく潜在因子モデル（Latent Factor Model, LFM）がある。
It learns latent factors to predict the missing ratings in a user-item rating matrix.
LFMは潜在的な因子を学習することで、ユーザとアイテムの評価行列に欠落している評価を予測する。
Representative matrix factorization methods include Singular Value Decomposition (SVD) (Koren, 2008; Koren et al., 2009; Srebro and Jaakkola, 2003), Non-negative Matrix Factorization (NMF) (Lee and Seung, 1999, 2001), Max-Margin Matrix Factorization (MMMF) (Rennie and Srebro, 2005; Srebro et al.,
代表的な行列因子分解の手法としては、Singular Value Decomposition (SVD) (Koren, 2008; Koren et al., 2009; Srebro and Jaakkola, 2003), Non-negative Matrix Factorization (NMF) (Lee and Seung, 1999, 2001), Max-Margin Matrix Factorization (MMMF) (Rennie and Srebro, 2005; Srebro et al,
2005), Probabilistic Matrix Factorization (PMF) (Mnih and Salakhutdinov, 2008; Salakhutdinov and Mnih, 2008), and Localized Matrix Factorization (LMF) (Zhang et al., 2013a,b).
2005）、確率的行列因子法（PMF）（Mnih and Salakhutdinov, 2008; Salakhutdinov and Mnih, 2008）、局所的行列因子法（LMF）（Zhang et al, 2013a、b）などがあります。
Matrix factorization methods are also commonly referred to as point-wise prediction, and they are frequently used to predict user explicit feedbacks, such as numerical ratings in e-commerce or movie review websites.
行列分解法は、一般にポイントワイズ予測とも呼ばれ、電子商取引や映画のレビューサイトにおける数値評価など、ユーザーの明示的なフィードバックを予測するために頻繁に使用されています。

Pair-wise learning to rank is frequently used to learn the correct item rankings based on implicit feedback.
暗黙のフィードバックに基づいて正しい項目順位を学習するために、順位付けのためのペアワイズ学習が頻繁に利用されている。
For example, Rendle et al. (2009) proposed Bayesian Personalized Ranking (BPR) to learn the relative ranking of the purchased items (positive item) against unpurchased items (negative items).
例えば、Rendleら（2009）は、未購入アイテム（ネガティブアイテム）に対する購入アイテム（ポジティブアイテム）の相対ランキングを学習するBayesian Personalized Ranking (BPR) を提案した。
Rendle and Schmidt-Thieme (2010) further extended the idea to tensor factorization to model pairwise interactions.
Rendle and Schmidt-Thieme(2010)はさらに、このアイデアをテンソル分解に拡張し、ペアワイズ相互作用をモデル化した。
Except for pair-wise learning to rank, Shi et al. (2010) adopted list-wise learning to rank for collaborative filtering.
Shiら(2010)は協調フィルタリングにおいて、ペア単位の順位付け学習を除き、リスト単位の順位付け学習を採用している。

Deep learning and representation learning also gained much attention in recommendation research.
推薦研究においても、深層学習や表現学習が注目されている。
For example, Cheng et al. (2016) proposed Wide and Deep Network, which combines shallow regression and multiple layer neural network for recommender systems.
例えば、Chengら(2016)は、レコメンダーシステム向けに浅い回帰と多層ニューラルネットワークを組み合わせたWide and Deep Networkを提案した。
Deep Neural Network is also applied in real-world commercial systems such as the YouTube recommender system (Covington et al., 2016).
Deep Neural Networkは、YouTubeレコメンダーシステム（Covington et al.、2016）など、実際の商用システムにも適用されています。
Besides, researchers also explored various deep architectures and information modalities for recommendation, such as convolutional neural networks over text (Zheng et al., 2017) or images (Chen et al., 2019b), recurrent neural networks over user behavior sequence (Hidasi et al., 2016), auto-encoders (Wu et al., 2016), and memory networks (Chen et al., 2018c).
そのほか、研究者は、テキスト（Zheng et al., 2017）や画像（Chen et al., 2019b）上の畳み込みニューラルネットワーク、ユーザー行動シーケンス（Hidasi et al., 2016）上の再帰神経ネットワーク、オートエンコーダー（Wu et al., 2016）、メモリネットワーク（Chen et al., 2018c）など、推薦のための様々な深いアーキテクチャや情報様式を探求しています。

Though many publications are generated in this direction due to the recent popularity of deep learning, we acknowledge that it is controversial whether neural models really make progress in recommender system research (Dacrema et al., 2019).
最近のディープラーニングの普及により、この方向で多くの論文が生み出されているが、ニューラルネットワークモデルが本当にレコメンダーシステム研究を進展させるかどうかは議論の余地があることを認める（Dacrema et al.）
Deep models work when sufficient data is available for training, such as side information or knowledge graphs in some research datasets or in the industry environment (Zhang et al., 2019).
ディープモデルは、いくつかの研究データセットや産業環境における側面情報や知識グラフなど、学習に十分なデータが利用できる場合に機能します（Zhang et al.）
Nevertheless, recommendation performance is not a key focus of this survey.
とはいえ、推薦性能は本調査の重要な焦点ではありません。
Instead, we will focus on the explainability perspective of deep models.
その代わり、ディープモデルの説明可能性の観点に注目する。
A lot of deep models have been developed for explainable recommendation, which we will introduce in the following subsections.
説明可能な推薦のために多くのディープモデルが開発されているが、以下のサブセクションで紹介する。

## 3.2. Factorization Models for Explainable Recommendation 3.2. 説明可能なレコメンデーションのための因数分解モデル

In this section, we introduce how matrix
この項では、行列のしくみについて紹介します。

A lot of explainable recommendation models have been proposed based on matrix factorization methods.
これまで、行列分解法に基づく説明可能な推薦モデルが多く提案されてきた。
One common problem of matrix factorization methods – or more generally, latent factor models – is that the user
行列分解法（より一般的には潜在因子モデル）に共通する問題点として，ユーザ

To solve the problem, Zhang et al. (2014a) proposed Explicit Factor Models (EFM).
この問題を解決するために、Zhang ら (2014a) は Explicit Factor Models (EFM) を提案した。
The basic idea is to recommend products that perform well on the user’s favorite features, as shown in Figure 3.1.
基本的な考え方は、図 3.1 に示すように、ユーザーの好きな特徴でパフォーマンスの高い製品を推薦することである。
Specifically, the proposed approach extracts explicit product features from user reviews, and then aligns each latent dimension of matrix factorization with an explicit feature, so that the factorization and prediction procedures are trackable to provide explicit explanations.
具体的には、提案アプローチは、ユーザーレビューから明示的な製品特徴を抽出し、行列分解の各潜在次元を明示的な特徴に整合させ、因子分解と予測手順を追跡可能にして明示的な説明を提供する。
The proposed approach can provide personalized recommendation explanations based on the explicit features, e.g., “The product is recommended because you are interested in a particular feature, and this product performs well on the feature”.
提案手法は、明示的特徴量に基づいて、例えば、「あなたがある特定の特徴に興味があり、この製品はその特徴に対して性能が良いので、この製品を推薦します」というような、パーソナライズされた推薦説明を提供することができる。
The model can even provide dis-recommendations by telling the user that “The product does not perform very well on a feature that you care about”, which helps to improve the trustworthiness of recommendation systems.
また、「この商品はあなたが気にしている特徴ではあまり性能が良くない」とユーザに伝えることで、推薦システムの信頼性向上に役立つ非推薦を提供することも可能なモデルである。
Because user preferences on item features are dynamic and may change over time, Zhang et al. (2015b) extended the idea by modeling the user’s favorite features dynamically on daily resolution.
アイテムの特徴に関するユーザーの好みは動的であり、時間とともに変化する可能性があるため、Zhangら（2015b）は、ユーザーの好きな特徴を日次解像度で動的にモデル化することでアイデアを拡張しました。

Chen et al. (2016) further extended the EFM model to tensor factorization.
Chen ら（2016）は、EFM モデルをさらにテンソル因子分解に拡張した。
In particular, the authors extracted product features from textual reviews and constructed the user-item-feature cube.
特に、著者らはテキストレビューから商品特徴を抽出し、ユーザー-アイテム-特徴キューブを構築した。
Based on this cube, the authors conducted pair-wise learning to rank to predict user preferences on features and items, which helps to provide personalized recommendations.
このキューブに基づいて、著者らは特徴やアイテムに関するユーザーの嗜好を予測するためにランク付けするペアワイズ学習を実施し、パーソナライズされたレコメンデーションを提供するのに役立てた。
The model was further extended to consider multiple product categories simultaneously, which helps to alleviate the data sparsity problem, as shown in Figure 3.2(a).
さらに、図3.2(a)に示すように、複数の商品カテゴリを同時に考慮するようにモデルを拡張し、データの疎密問題を緩和するのに役立てた。

Wang et al. (2018b) further generalized MF-based explainable recommendation by multi-task learning over tensors.
Wangら（2018b）は、テンソル上のマルチタスク学習によって、MFベースの説明可能な推薦をさらに一般化した。
In particular, two companion learning tasks “user preference modeling for recommendation” and “opinionated content modeling for explanation” are integrated via a joint tensor factorization framework, as shown in Figure 3.2(b).
特に、図3.2(b)に示すように、2つのコンパニオン学習タスク「推薦のためのユーザー嗜好モデリング」と「説明のための意見付きコンテンツモデリング」が共同テンソル因子化フレームワークを介して統合されています。
The algorithm predicts not only a user’s preference over a list of items (i.e., recommendations), but also how the user would appreciate a particular item at the feature level (i.e., opinionated textual explanation).
このアルゴリズムでは、ユーザーの嗜好をリストアップする（推薦）だけでなく、ユーザーが特定のアイテムをどのように評価するかも特徴レベルで予測する（意見付きテキストによる説明）。

User preference distribution over the features could be different on different items, while the above methods assume each user has a global feature preference distribution.
特徴に対するユーザーの選好分布はアイテムによって異なる可能性があるが、上記の方法は各ユーザーがグローバルな特徴選好分布を持っていると仮定している。
As an improvement, Chen et al. (2018b) propose an Attention-driven Factor Model (AFM), which learns and tunes the user attention distribution over features on different items.
改善策として、Chenら（2018b）は、異なるアイテム上の特徴に対するユーザーの注目分布を学習し、チューニングするAttention-driven Factor Model（AFM）を提案している。
Meanwhile, users’ attention distributions can also serve as explanations for recommendations.
一方、ユーザーの注目分布は、レコメンデーションの説明としても機能する。

To analyze the relationship between inputs (user history) and outputs (recommendations) in latent factor models, Cheng et al. (2019a) adopted influence analysis in LFMs towards explainable recommendation.
潜在因子モデルにおけるインプット（ユーザー履歴）とアウトプット（レコメンド）の関係を分析するために、Chengら（2019a）は説明可能なレコメンドに向けてLFMsに影響力分析を採用した。
In particular, the authors incorporate interpretability into LFMs by tracing each prediction back to the model’s training data, and further provide intuitive neighbor-style explanations for the predictions.
特に、著者らは、各予測をモデルの学習データに遡ることでLFMsに解釈可能性を取り入れ、さらに予測に対して直感的なネイバー形式の説明を行っています。
We will provide more details of this work in the following section specifically devoted to model-agnostic and post-hoc explainable recommendation.
この研究の詳細については、モデル不可知論的でポストホックな説明可能レコメンデーションに特化した次のセクションで説明します。
The features extracted from reviews can also be recommended to users as explanations.
レビューから抽出された特徴は、説明としてユーザーに推薦することも可能である。
Bauman et al. (2017) proposed the Sentiment Utility Logistic Model (SULM), which extracts features (i.e., aspects) and user sentiments on these features.
Baumanら（2017）は、特徴（＝アスペクト）とその特徴に対するユーザーの感情を抽出するSentiment Utility Logistic Model（SULM）を提案した。

The features and sentiments are integrated into a matrix factorization model to regress the unknown ratings, which are finally used to generate recommendations.
特徴量とセンチメントを行列因子分解モデルに統合して未知の評価を回帰し、最終的に推薦文の生成に用いる。
The proposed method provides not only item recommendations, but also feature recommendations for each items as explanations.
提案手法は、アイテム推薦だけでなく、各アイテムの特徴推薦を説明として提供する。
For example, the method can recommend restaurants together with the most important aspects that the users can select, such as the time to go to a restaurant (e.g., lunch or dinner), and dishes to order (e.g., seafood).
例えば、本手法では、レストランに行く時間帯（ランチやディナーなど）や注文する料理（シーフードなど）など、ユーザーが選択できる最も重要な点とともに、レストランを推薦することができる。
Qiu et al. (2016) and Hou et al. (2018) also investigated aspect-based latent factor models for recommendation by integrating ratings and reviews.
Qiuら（2016）とHouら（2018）も、評価とレビューを統合して推薦するためのアスペクトベースの潜在要因モデルを研究している。

Latent factor models can also be integrated with other structured data for better recommendation and explainability, such as tree structures or graph structures.
潜在因子モデルは、木構造やグラフ構造など、より良い推薦や説明可能性のために他の構造化データと統合することも可能である。
Tao et al. (2019a) proposed to tame latent factor models for explainability with factorization trees.
Taoら（2019a）は、説明可能性のために潜在因子モデルを因数分解ツリーで飼い慣らすことを提案した。
The authors integrate regression trees to guide the learning of latent factor models for recommendation, and use the learned tree structure to explain the resulting latent factors.
著者らは、推薦のための潜在因子モデルの学習を誘導するために回帰木を統合し、学習された木構造を用いて、得られた潜在因子を説明する。
In particular, the authors build regression trees on users and items with user-generated reviews, and associate a latent profile to each node on the trees to represent users and items.
特に、著者らは、ユーザが作成したレビューを持つユーザとアイテムについて回帰木を構築し、木上の各ノードに潜在プロファイルを関連付けて、ユーザとアイテムを表現する。
With the growth of the regression tree, the latent factors are refined under the regularization imposed by the tree structure.
回帰木の成長とともに、潜在的な要因は木構造によって課される正則化の下で洗練されていく。
As a result, we can track the creation of latent profiles by looking into the path of each factor on regression trees, which thus serves as an explanation for the resulting recommendations.
その結果、回帰木における各因子の経路を調べることで、潜在プロファイルの生成を追跡することができ、結果としてレコメンデーションを説明することができる。

Researchers also investigated model-based approaches to generate relevant-user or relevant-item explanations, which provide explainable recommendations solely based on the user-item rating matrix (see Figure 3.3).
研究者たちは、関連ユーザーまたは関連アイテムの説明を生成するモデルベースのアプローチも研究し、ユーザー・アイテム評価行列（図3.3参照）にのみ基づいて説明可能な推薦を提供するものである。
Specifically, Abdollahi and Nasraoui (2016, 2017) described Explainable Matrix Factorization (EMF) for explainable recommendation.
具体的には、Abdollahi and Nasraoui (2016, 2017) は、説明可能な推薦のための説明可能な行列因子分解 (EMF) について述べている。
This model generates relevant-user explanations, where a recommended item is explained as many users similar to you purchased this item.
このモデルは、推薦されたアイテムが自分と似た多くのユーザーがこのアイテムを購入したと説明される、関連するユーザーの説明を生成するものである。
To achieve this goal, the authors added an explainability regularizer into the objective function of matrix factorization.
この目標を達成するために、著者らは、行列分解法の目的関数に説明可能性正則化を追加した。
The explainability regularizer forces the user latent vector and item latent vector to be close to each other if a lot of the user’s neighbors also purchased the item.
説明可能性正則化とは、ユーザーの潜在ベクトルとアイテムの潜在ベクトルを、ユーザーの近隣にいる多くのユーザーがそのアイテムを購入した場合に、互いに近づくように強制するものである。
In this way, the model naturally selects those commonly purchased items from a user’s neighbors as recommendations, and meanwhile maintains high rating prediction accuracy.
このようにして、このモデルは、ユーザーの近隣住民からよく購入されるアイテムを推薦として自然に選択し、一方で高い評価予測精度を維持する。
Liu et al. (2019) extended the idea by considering the fact that ratings in the user-item interaction matrix are missing not at random.
Liuら（2019）は、ユーザーとアイテムの相互作用行列の評価がランダムではなく欠落しているという事実を考慮し、このアイデアを拡張した。
The authors proposed an explainable probabilistic factorization model, which employs an influence mechanism to evaluate the importance of the users’ historical data, so that the most related users and items can be selected to explain each predicted rating.
著者らは説明可能な確率的因数分解モデルを提案し、ユーザーの履歴データの重要性を評価するために影響メカニズムを採用し、予測された各評価を説明するために最も関連するユーザーとアイテムを選択できるようにした。
Based on the learned influence scores, five representative user
学習された影響度スコアに基づき、5人の代表的なユーザ

## 3.3. Topic Modeling for Explainable Recommendation 3.3. 説明可能なレコメンデーションのためのトピックモデリング

Based on available text information – especially the widely available textual reviews in e-commerce – topic modeling approach has also been widely adopted for explanations in recommender systems.
利用可能なテキスト情報、特にeコマースで広く利用されているテキストレビューに基づいて、トピックモデリングのアプローチも推薦システムにおける説明のために広く採用されてきた。
In these approaches, users can usually be provided with intuitive explanations in the form of topical word clouds (McAuley and Leskovec, 2013; Wu and Ester, 2015; Zhao et al., 2015).
これらのアプローチでは、通常、ユーザーはトピックワードクラウドの形で直感的な説明を提供することができる（McAuley and Leskovec, 2013; Wu and Ester, 2015; Zhao et al, 2015）。
In this section, we review the related work that can be categorized into this approach.
このセクションでは、このアプローチに分類される関連研究をレビューする。

McAuley and Leskovec (2013) proposed to understand the hidden factors in latent factor models based on the hidden topics learned from reviews.
McAuley and Leskovec (2013) は，レビューから学習した隠れたトピックに基づいて，潜在因子モデルにおける隠れた因子を理解することを提案した．
The authors proposed the Hidden Factor and Topic (HFT) model, which bridges latent factor models and Latent Dirichlet Allocation (LDA).
著者らは、潜在因子モデルとLDA（Latent Dirichlet Allocation）の橋渡しをするHFT（Hidden Factor and Topic）モデルを提案した。
It links each dimension of the latent vector with a dimension of the LDA topic distribution vector.
これは、潜在的なベクトルの各次元とLDAトピック分布ベクトルの次元をリンクさせるものである。
By considering reviews, the method improves rating prediction accuracy.
レビューを考慮することで、本手法は評価予測精度を向上させる。
Besides, by projecting each user’s latent vector into the latent topic space in LDA, it helps to understand why a user made a particular rating on a target item.
その上、各ユーザの潜在ベクトルをLDAの潜在トピック空間に射影することで、ユーザが対象アイテムに対して特定の評価を行った理由を理解することができるようになる。
For example, we can detect the most significant topics that a user likes.
例えば、あるユーザが好む最も重要なトピックを検出することができる。

Following this idea, Tan et al. (2016) proposed to model item recommendability and user preference in a unified semantic space, as shown in Figure 3.4(a).
この考えに従い，Tan ら（2016）は，図 3.4（a）に示すように，アイテムの推奨度とユーザの嗜好を統一的な意味空間でモデル化することを提案した．
In this model, each item is embedded as a topical recommendability distribution vector.
このモデルでは、各アイテムはトピカルな推奨度分布ベクトルとして埋め込まれている。
Similarly, each user is embedded in the same topical recommendability space based on his
同様に，各ユーザは，自分の推薦度に基づいて，同じトピック推薦度空間に埋め込まれる．

More generally, researchers also investigated other probabilistic graphic models beyond LDA for explainable recommendations.
より一般的には、研究者は説明可能な推薦のための LDA 以外の確率的なグラフィックモデルも研究している。
Wu and Ester (2015) studied the personalized sentiment estimation problem on item aspects.
Wu and Ester (2015) は、アイテムのアスペクトに関するパーソナライズされたセンチメント推定問題を研究した。
In particular, the authors proposed the FLAME model (Factorized Latent Aspect ModEl), which combines the advantages of collaborative filtering and aspect-based opinion mining.
特に、著者らは協調フィルタリングとアスペクトベースの意見マイニングの利点を組み合わせたFLAMEモデル(Factorized Latent Aspect ModEl)を提案した。
It learns each user’s personalized preferences on different item aspects based on her reviews, as shown in Figure 3.5(a).
このモデルは、図3.5（a）に示すように、各ユーザのレビューに基づいて、異なるアイテムのアスペクトに対する各ユーザの個人的な嗜好を学習する。
Based on this, it predicts the user’s aspect ratings on new items through collective intelligence.
これに基づいて、集合知により新しいアイテムに対するユーザのアスペクト評価を予測する。
The proposed method showed improved performance on hotel recommendations on TripAdvisor.
提案手法は、TripAdvisor上のホテル推薦において、性能の向上を示した。
Further, for each hotel recommendation, it can provide a word cloud of the hotel aspects as an explanation, as shown in Figure 3.5(b), where the size of each aspect is proportional to the sentiment of the aspect.
さらに、各ホテルの推薦に対して、図3.5(b)に示すように、ホテルのアスペクトのワードクラウドを説明として提供することができ、各アスペクトの大きさは、そのアスペクトのセンチメントに比例しています。

Zhao et al. (2015) designed a probabilistic graphical model to integrate sentiment, aspect, and region information in a unified framework for improved recommendation performance and explainability in pointof-interest (POI) recommendation.
Zhaoら（2015）は、pointof-interest（POI）推薦における推薦性能と説明可能性を向上させるために、センチメント、アスペクト、地域情報を統一フレームワークで統合する確率的グラフィカルモデルを設計している。
The explanations are determined by each user’s topical-aspect preference, which is similar to the topical clusters in McAuley and Leskovec (2013), but the difference is that the model can provide sentiment of each cluster for explanation purposes.
説明は各ユーザーのトピカル・アスペクトの好みによって決定され，これはMcAuley and Leskovec (2013) のトピカルクラスターと同様であるが，違いは，このモデルが説明のために各クラスターのセンチメントを提供できる点である．

Ren et al. (2017) leveraged topic modeling for social explainable recommendations.
Ren ら（2017）は、トピックモデリングを活用して、ソーシャル説明可能なレコメンデーションを実現した。
Specifically, the authors proposed social-collaborative viewpoint regression (sCVR).
具体的には、著者らは社会協調的視点回帰（sCVR）を提案した。
A “viewpoint” is defined as a tuple of concept, topic, and sentiment label from both user reviews and trusted social relations, as shown in Figure 3.4(b), and the viewpoints are used as explanations.
図3.4(b)に示すように、「視点」はユーザーレビューと信頼できる社会関係の両方からの概念、トピック、センチメントラベルのタプルとして定義され、視点は説明として使用される。
The authors proposed a probabilistic graphical model based on the viewpoints to improve prediction accuracy.
著者らは、予測精度を向上させるために、視点に基づく確率的グラフィカルモデルを提案した。
Similar to the previous work, explanations are generated based on the user’s favorite topics embedded in the viewpoints.
また，従来と同様に，ビューポイントに埋め込まれたユーザの好きなトピックをもとに説明を生成する．

## 3.4. Graph-based Models for Explainable Recommendation 3.4. 説明可能なレコメンデーションのためのグラフベースのモデル

Many user-user or user-item relationships can be represented as graphs, especially in social network scenarios.
ユーザとユーザ、あるいはユーザとアイテムの関係の多くは、特にソーシャルネットワークのシナリオにおいて、グラフとして表現することができる。
In this section, we introduce how explainable recommendations can be generated based on graph learning approaches such as graph-based propagation and clustering.
ここでは、グラフベースの伝播やクラスタリングなどのグラフ学習アプローチに基づいて、説明可能なレコメンデーションがどのように生成できるかを紹介する。
He et al. (2015) introduced a tripartite graph structure to model the user-item-aspect ternary relations for top-N recommendation, as shown in Figure 3.6, where an aspect is an item feature extracted from user reviews.
Heら（2015）は、図3.6に示すように、トップN推薦のためのユーザ-アイテム-アスペクトの三項関係をモデル化するために三分割グラフ構造を導入し、アスペクトはユーザレビューから抽出したアイテム特徴であるとした。
The authors proposed TriRank, a generic algorithm for ranking the vertices in the tripartite graph, which applies smoothness and fitting constraints for node ranking and personalized recommendation.
著者らは、三分割グラフの頂点をランク付けする汎用アルゴリズムであるTriRankを提案し、ノードのランク付けと個人別推薦のために滑らかさと適合制約を適用している。
In this survey, explanations are attributed to the top-ranked aspects that match the target user and the recommended item.
本調査では，ターゲットユーザと推薦アイテムにマッチする上位のアスペクトに説明を帰着させる．

Without using external information such as aspects, Heckel et al. (2017) conducted over-lapping co-clustering based on user-item bipartite graph for explainable recommendation.
アスペクトなどの外部情報を用いずに，Heckelら（2017）は説明可能な推薦のために，ユーザ・アイテム二部グラフに基づくオーバーラッピング・コクラスタリングを実施した．
In each co-cluster, the users have similar interests, and the items have similar properties, as shown in Figure 3.7.
各コクラスタでは，図 3.7 に示すように，ユーザは類似の関心を持っており，アイテムは類似の性質を持っている．
Explanations are generated based on users’ collaborative information, for example, in the form of “Item A is recommended to Client X with confidence α, because Client X has purchased Item B, C, and D, while clients with similar purchase history (such as Clients Y and Z) also bought Item A”.
説明文はユーザの協調情報に基づいて生成される。例えば、「顧客Xは商品B、C、Dを購入しており、同様の購入履歴を持つ顧客（顧客Y、Zなど）も商品Aを購入しているので、顧客Xには商品Aが信頼度αで推奨される」という形である。
If a user-item pair falls into multiple co-clusters, we can thus generate multiple user-based and item-based explanations from each of the co-cluster.
このように、ユーザーとアイテムのペアが複数のクラスタに該当する場合、それぞれのクラスタから複数のユーザーベース説明とアイテムベース説明を生成することができる。

Wang et al. (2018c) proposed a tree-enhanced embedding model for explainable recommendation to combine the generalization ability of embedding-based models and the explainability of tree-based models.
Wangら（2018c）は、埋め込み型モデルの汎化能力とツリー型モデルの説明可能性を両立させるため、説明可能な推薦のためのツリー拡張埋め込み型モデルを提案した。
In this model, the authors first employed a tree-based model to learn explicit decision rules.
このモデルでは、著者らはまずツリーベースモデルを採用し、明示的な決定ルールを学習した。
The decision rules are based on cross features extracted from side information.
この判断ルールは、サイド情報から抽出された交差特徴量に基づいている。
Then, the authors designed an embedding model that incorporates explicit cross features, and generalize to unseen user or item cross features based on collaborative learning.
次に、協調学習に基づいて、明示的な交差特徴を取り込み、未見のユーザやアイテムの交差特徴に汎化する埋め込みモデルを設計した。
To generate explanations, an attention network is used to detect the most significant decision rules during the recommendation process.
説明文を生成するために、推薦プロセスにおいて最も重要な決定規則を検出するために、アテンションネットワークを用いる。

Graph-based explainable recommendation is also frequently used in social recommendation scenarios, because social network is naturally a graph structure.
また、ソーシャルネットワークは当然グラフ構造であるため、グラフベースの説明可能な推薦がソーシャル推薦の場面で頻繁に利用される。
For example, the UniWalk algorithm (Park et al., 2018) introduced in Section 2 is a graph-based explainable recommendation algorithm.
例えば、セクション2で紹介したUniWalkアルゴリズム(Park et al., 2018)は、グラフベースの説明可能な推薦アルゴリズムである。
It exploits both ratings and the social network to generate explainable product recommendations.
これは、評価とソーシャルネットワークの両方を利用して、説明可能な商品推薦を生成する。
In this algorithm, a recommendation can be explained based on the target user’s friends who have similar preferences on the graph.
このアルゴリズムでは、グラフ上で同様の嗜好を持つターゲットユーザーの友人に基づいて、推薦を説明することができる。

## 3.5. Deep Learning for Explainable Recommendation 3.5. 説明可能なレコメンデーションのためのディープラーニング

Recently, researchers have leveraged deep learning and representation learning for explainable recommendations.
最近、研究者は説明可能な推薦のために深層学習と表現学習を活用している。
The deep explainable recommendation models cover a wide range of deep learning techniques, including CNN (Seo et al., 2017; Tang and Wang, 2018), RNN
深層説明可能な推薦モデルは、CNN (Seo et al., 2017; Tang and Wang, 2018), RNNなどの深層学習技術を幅広くカバーしている。

Seo et al. (2017) proposed to model user preferences and item properties using convolutional neural networks (CNNs) upon review text.
Seo ら（2017）は、レビューテキストに畳み込みニューラルネットワーク（CNN）を用いて、ユーザーの嗜好とアイテムの特性をモデル化することを提案した。
It leans dual local and global attentions for explanation purposes, as shown in Figure 3.8.
図 3.8 に示すように、説明のためにローカルとグローバルの二重のアテンションに傾ける。
When predicting the user-item rating, the model selectively chooses review words with different attention weights.
ユーザーアイテムの評価を予測する際、このモデルは異なる注目の重みを持つレビュー単語を選択的に選択する。
Based on the learned attention weights, the model can show which part of the review is more important for the output.
学習された注意の重みに基づいて、モデルはレビューのどの部分が出力にとってより重要であるかを示すことができる。
Besides, the model can highlight the important words in the review as explanations to help users understand the recommendations.
さらに、モデルはレビューの中の重要な単語を説明として強調し、ユーザーが推奨事項を理解するのを助けることができる。

Similarly, Wu et al. (2019) combined the user-item interaction and review information in a unified framework.
同様に、Wu ら（2019）は、ユーザーとアイテムの相互作用とレビュー情報を統一的なフレームワークで組み合わせた。
The user reviews are attentively summarized as content features, which are further integrated with the user and item embeddings to predict the final ratings.
ユーザーレビューは内容特徴として丁寧にまとめられ、さらにユーザーとアイテムのエンベッディングと統合され、最終的な評価を予測する。
Lu et al. (2018a) presented a deep learning recommendation model that co-learns user and item information from ratings and reviews.
Luら（2018a）は、評価とレビューからユーザーとアイテム情報を共学習する深層学習推薦モデルを発表した。
It jointly optimizes a matrix factorization component (over ratings) and an attention-based GRU network (over reviews), so that features learned from ratings and reviews are aligned with each other.
それは、評価とレビューから学習された特徴が互いに整列するように、行列分解コンポーネント（評価以上）と注意ベースのGRUネットワーク（レビュー以上）を共同で最適化するものである。
Lu et al. (2018b) further added a review discriminator based on adversarial sequence to sequence learning into the joint optimization framework, so that the generator can generate reviews for a user-recommendation pair as natural language explanation.
Luら（2018b）はさらに、敵対的シーケンスに基づくレビュー識別器をシーケンス学習に追加し、生成器がユーザーと推薦のペアに対するレビューを自然言語の説明として生成できるようにした。
In both (Wu et al., 2019) and (Lu et al., 2018a), the attention weights over review words are leveraged to explain the recommendations.
(Wu et al., 2019) と (Lu et al., 2018a) の両方において、レビュー単語上の注目重みが推奨事項を説明するために活用される。

Gao et al. (2019) developed a Deep Explicit Attentive Multi-view Learning Model (DEAML) for explainable recommendation, which aims to mitigate the trade-off between accuracy and explainability by developing explainable deep models.
Gaoら（2019）は、説明可能なディープモデルを開発することにより、精度と説明可能性のトレードオフを緩和することを目的とした、説明可能な推薦のためのDEAML（Deep Explicit Attentive Multi-view Learning Model）を開発しました。
The basic idea is to build an initial network based on an explainable deep hierarchy (e.g., the Microsoft Concept Graph), and improve the model accuracy by optimizing key variables in the hierarchy (e.g., node importance and relevance).
基本的な考え方は、説明可能な深層階層（例えば、マイクロソフトのコンセプトグラフ）に基づいて初期ネットワークを構築し、階層内の主要変数（例えば、ノードの重要度と関連性）を最適化することによって、モデルの精度を向上させることである。
The model outputs feature-level explanations similar to Zhang et al. (2014a), but the features are attentively retrieved from an explicit feature hierarchy.
このモデルは、Zhangら（2014a）と同様に特徴レベルの説明を出力するが、特徴は明示的な特徴階層から注意深く取得される。
The model is capable of modeling multi-level explicit features from noisy and sparse data, and shows highly usable explanations in industry-level applications.
このモデルは、ノイズの多い疎なデータから多階層の明示的な特徴をモデル化することができ、産業レベルのアプリケーションにおいてユーザビリティの高い説明を示している。
Instead of using existing features, Ma et al. (2019a) proposed to automatically learn disentangled features from data for recommendation, which not only improved the explainability but also enable users to better control the recommendation results.
Maら（2019a）は、既存の特徴を用いる代わりに、推薦のためにデータから分離された特徴を自動的に学習することを提案し、説明可能性を改善するだけでなく、ユーザが推薦結果をよりよく制御できるようにした。

Different from highlighting the review words as explanations, Costa et al. (2018) proposed a method for automatically generating natural language explanations based on character-level RNN.
レビューの単語を説明として強調するのとは異なり、Costaら（2018）は、文字レベルのRNNに基づいて自然言語の説明を自動生成する手法を提案した。
The model concatenates the user ratings into the input component as auxiliary information, so that the model can generate reviews according to the expected rating (sentiment).
このモデルでは、ユーザーの評価を補助情報として入力成分に連結することで、期待される評価（センチメント）に従ってレビューを生成することができる。
Different from many explainable recommendation models, whose explanation is generated based on predefined templates, the model can automatically generate explanations in a natural language manner.
説明可能なレコメンデーションモデルの多くは、あらかじめ定義されたテンプレートに基づいて説明が生成されるが、本モデルは自然言語による説明を自動的に生成することができる。
By choosing different parameters, the model can generate different explanations to attract users, as shown in Figure 3.9(a).
異なるパラメータを選択することで，図 3.9(a) に示すように，このモデルはユーザーを惹きつけるために異なる説明を生成することができる．
Li et al. (2017) proposed a more comprehensive model to generate tips in review systems, where each tip is a short summarization sentence for a long review.
Liら(2017)はレビューシステムにおけるtipを生成するためのより包括的なモデルを提案し、各tipは長いレビューに対する短い要約文である。
The tips also serve as recommendation explanations.
また、tip は推薦説明の役割も果たす。
Chen et al. (2019a) integrated the natural language generation approach and the feature word approach, and proposed a topic sensitive generation model to generate explanations about particular feature words.
Chenら（2019a）は、自然言語生成アプローチと特徴語アプローチを統合し、特定の特徴語に関する説明を生成するトピックセンシティブ生成モデルを提案した。
To some extent, the model can control the item aspect that the generated explanation talks about.
このモデルは、ある程度、生成された説明が語る項目の側面を制御することができる。
Inspired by human’s informationprocessing model in cognitive psychology, Chen et al. (2019d) developed an encoder-selector-decoder architecture for explainable recommendation, which exploits the correlations between the recommendation task and the explanation task through co-attentive multi-task learning.
認知心理学における人間の情報処理モデルに触発されて、Chenら（2019d）は説明可能な推薦のためのエンコーダ-セレクタ-デコーダアーキテクチャを開発し、共同注意マルチタスク学習によって推薦タスクと説明タスクの間の相関を利用した。
The model enhances the accuracy of the recommendation task, and generates linguistic explanations that are fluent, useful, and highly personalized.
このモデルは、推薦タスクの精度を高め、流暢で、有用で、高度にパーソナライズされた言語的説明を生成する。

Chang et al. (2016) proposed another approach to generating natural language explanations, which is based on human users and crowdsourcing.
Changら（2016）は、人間のユーザーとクラウドソーシングに基づく自然言語説明の生成という別のアプローチを提案した。
The authors argued that algorithm generated explanations can be overly simplistic and unconvincing, while humans can overcome these limitations.
著者らは、アルゴリズムで生成された説明は過度に単純化され、説得力を欠く可能性がある一方、人間はこれらの限界を克服できると主張した。
Inspired by how people explain word-of-mouth recommendations, the authors designed a process to combine crowdsourcing and computation for generating explanations.
著者らは、人がどのように口コミの推薦文を説明するかにヒントを得て、クラウドソーシングと計算を組み合わせた説明文生成プロセスを設計した。
They first extract the topical aspects of movies based on an unsupervised learning approach, and then, generate natural language explanations for the topical aspects.
彼らはまず、教師なし学習アプローチに基づいて映画の話題性を抽出し、次に、話題性のある側面に対する自然言語の説明を生成する。
More specifically, the authors collect relevant review quotes for each aspect, and then ask crowd workers to synthesize the quotes into explanations.
具体的には、それぞれの話題について、関連するレビューの引用を集め、クラウドワーカーに引用を合成して説明文を生成するよう依頼する。
Finally, the authors model users’ preferences based on their activities and present explanations in a personalized fashion (Figure 3.9(b)).
最後に，ユーザの行動からユーザの嗜好をモデル化し，パーソナライズされた説明を提示する（図3.9（b））．
Controlled experiments with 220 MovieLens users were conducted to evaluate the efficiency, effectiveness, trust, and satisfaction of the personalized natural language explanations, in comparison with personalized tag-based explanations.
220人のMovieLensユーザーを対象とした対照実験を行い、パーソナライズされた自然言語による説明の効率、効果、信頼度、満足度を、パーソナライズされたタグベースの説明と比較して評価した。

Instead of generating explanations, Chen et al. (2018a) selects appropriate user reviews as explanations.
説明を生成するのではなく、Chenら(2018a)は適切なユーザーレビューを説明として選択する。
The authors designed an attention mechanism over the user and item reviews for rating prediction.
著者らは、評価予測のために、ユーザーとアイテムのレビューの上に注目メカニズムを設計した。
In this research, the authors believe that reviews written by others are critical reference information for a user to make decisions in e-commerce.
この研究において、著者らは、他の人が書いたレビューは、ユーザーがeコマースで意思決定をするために重要な参考情報であると考えている。
However, the huge amount of reviews for each product makes it difficult for consumers to examine all the reviews to evaluate a product.
しかし、商品ごとに膨大な量のレビューが存在するため、消費者がすべてのレビューを吟味して商品を評価することは困難である。
As a result, selecting and providing high-quality reviews for each product is an important approach to generate explanations.
そのため、商品ごとに質の高いレビューを選別して提供することが、説明文を生成するための重要なアプローチとなる。
Specifically, the authors introduced an attention mechanism to learn the usefulness of reviews.
具体的には、レビューの有用性を学習するためのアテンション機構を導入した。
Therefore, highly-useful reviews can be adopted as explanations, which help users to make faster and better decisions.
そのため、有用性の高いレビューを説明文として採用することで、ユーザがより早く、より良い意思決定を行えるようになる。

Chen et al. (2019b) proposed visually explainable recommendation by jointly modeling visual images and textual reviews.
Chenら（2019b）は、視覚的画像とテキストレビューを共同でモデル化することで、視覚的に説明可能なレコメンデーションを提案した。
It highlights the image region-of-interest for a user as recommendation explanations, as shown in Figure 2.10.
これは、図2.10に示すように、ユーザにとって興味のある画像領域を推薦説明としてハイライトするものである。
By jointly modeling images and reviews, the proposed model can also generate a natural language explanation to accompany the visual explanations by describing the highlighted regions.
提案モデルは、画像とレビューを共同モデル化することで、ハイライトされた領域を説明することで、視覚的説明に付随する自然言語の説明も生成することができる。

With the natural language explanations, users can better understand why the particular image regions are highlighted as visual explanations.
自然言語による説明により、ユーザーは特定の画像領域が視覚的な説明として強調される理由をより良く理解することができる。
With the advantage of reasoning over explicit memory slots, memory networks have been explored in explainable recommendation tasks.
明示的なメモリスロットを超える推論の利点により、メモリネットワークは説明可能な推薦タスクで研究されてきた。
For example, Chen et al. (2018c) studied explainable sequential recommendation based on memory networks.
例えば、Chenら（2018c）は、メモリネットワークに基づく説明可能な逐次推薦を研究している。
It considers each item in a user’s interaction history as a memory slot, and develops an attention mechanism over the slots to predict the subsequent user behaviors.
これは、ユーザーの対話履歴の各項目をメモリスロットとみなし、スロット上の注意メカニズムを開発して、その後のユーザーの行動を予測するものである。
Explanations are provided by showing how and which of the user’s previous item(s) influenced the current prediction.
そして、ユーザの過去の行動履歴のうち、どの項目がどのように現在の予測に影響を与えたかを示すことにより、説明を行う。
The authors further proposed Dynamic Explainable Recommendation (Chen et al., 2019c) based on time-aware gated recurrent units.
著者らはさらに、時間認識ゲート付きリカレントユニットに基づく動的説明可能レコメンデーション(Chen et al., 2019c)を提案した。
Tao et al. (2019b) proposed a Log2Intent framework for interpretable user modeling.
Taoら(2019b)は、解釈可能なユーザーモデリングのためのLog2Intentフレームワークを提案した。
It focuses on modeling user behaviors, as well as predicting and interpreting user intents from the unstructured software log-trace data.
これは、ユーザー行動のモデリングに加え、非構造化ソフトウェアログトレースデータからユーザーインテントを予測し、解釈することに焦点を当てている。
Technically, the authors incorporate auxiliary knowledge with memory networks for sequence to sequence modeling.
技術的には、著者らはシーケンス間のモデリングのために、メモリネットワークを用いて補助知識を組み込んでいる。
The attention mechanism produces attended annotations over memory slots to interpret the user log data.
注目メカニズムは、ユーザーログデータを解釈するために、メモリスロット上の注目された注釈を生成する。

Li et al. (2019) developed a capsule network approach to explainable recommendation.
Liら（2019）は、説明可能な推薦のためのカプセルネットワークアプローチを開発した。
It considers an “item aspect – user viewpoint” pair as a logic unit, which is used to reason the user rating behaviors.
これは、「アイテムの側面-ユーザーの視点」のペアをロジックユニットとみなし、ユーザーの評価行動を推論するために使用するものである。
The model discovers the logic units from reviews and resolves their sentiments for explanations.
このモデルは、レビューから論理ユニットを発見し、説明のためにそのセンチメントを解決する。
A sentiment capsule architecture with a Routing by Bi-Agreement mechanism is proposed to identify the informative logic units for rating prediction, while the informativeness of each unit helps to produce explanations for the predictions.
評価予測のための情報量の多い論理ユニットを特定するために、Routing by Bi-Agreement メカニズムを用いた感情カプセルアーキテクチャを提案し、各ユニットの情報量は予測に対する説明の生成に役立つとする。
Developing capsule logic units for explainable reasoning shows a promising approach towards explainable recommendation systems.
説明可能な推論のためのカプセル論理ユニットの開発は、説明可能な推薦システムに向けた有望なアプローチであることを示している。

We should note that the scope and literature of deep learning for explainable recommendation is not limited to the research introduced in this subsection.
説明可能な推薦のための深層学習の範囲と文献は、この小節で紹介した研究に限定されないことに注意する必要がある。
Except for deep learning over text or image for explainable recommendations, research efforts in the explainable
説明可能な推薦のためのテキストや画像に対する深層学習を除けば、説明可能な推薦のための深層学習の研究活動は

Another important yet less explored question is the fidelity of the deep explainable models.
もう一つの重要な、しかしあまり調査されていない問題は、深層説明可能なモデルの忠実度である。
Deep learning models are usually complex in nature, and sometimes it could be difficult to decide if the explanations provided by the model truly reflect the real mechanism that generated the recommendations or decisions.
深層学習モデルは通常、その性質上複雑であり、モデルによって提供される説明が、推奨や決定を生成した実際のメカニズムを本当に反映しているかどうかを判断することが難しい場合がある。
The community has different opinions on the explanation fidelity problem.
説明の忠実性の問題については、コミュニティによって様々な意見がある。
For example, attention mechanism is a frequently used technique to design explainable decision making models.
例えば、アテンションメカニズムは、説明可能な意思決定モデルを設計するために頻繁に使用される手法である。
However, Jain and Wallace (2019) argued that standard attention modules do not provide meaningful explanations and should not be treated as though they do, while Wiegreffe and Pinter (2019) later challenged many of the assumptions underlying the prior work, arguing that such a claim depends on one’s definition of explanation, and showed that the prior work does not disprove the usefulness of attention mechanisms for explainability.
しかし、Jain and Wallace（2019）は、標準的なアテンションモジュールは意味のある説明を提供せず、あたかもそうであるかのように扱うべきではないと主張し、Wiegreffe and Pinter（2019）はその後、先行研究の基礎となる多くの前提に挑戦し、そのような主張は説明に関する人の定義に依存すると主張して、先行研究が説明可能性に対するアテンションメカニズムの有用性を否定するものでないことを示している。
Overall, the explainability of deep models is still an important open problem to explore, and more advanced explanation models are needed to understand the behavior of neural networks.
全体として、深層モデルの説明可能性はまだ探求すべき重要な未解決問題であり、神経ネットワークの振る舞いを理解するためには、より高度な説明モデルが必要です。
We will further discuss this problem in the following section of evaluating explainable recommendations.
この問題については、次の説明可能なレコメンデーションの評価のセクションでさらに議論する予定である。

## 3.6. Knowledge Graph-based Explainable Recommendation 3.6. 知識グラフに基づく説明可能なレコメンデーション

Knowledge graph (KG, or knowledge base) contains rich information about the users and items, which can help to generate intuitive and more tailored explanations for the recommended items.
知識グラフ（KG, knowledge base）には、ユーザやアイテムに関する豊富な情報が含まれており、推薦されたアイテムに対して、直感的でよりカスタマイズされた説明を生成するのに役立つと考えられる。
Recently, researchers have been exploring knowledge graphs for explainable recommendations.
近年、研究者は説明可能なレコメンデーションのための知識グラフを研究している。

Catherine et al. (2017) proposed a method to jointly rank items and knowledge graph entities using a Personalized PageRank procedure, which produces recommendations together with their explanations.
Catherineら（2017）は、Personalized PageRankの手順を用いてアイテムと知識グラフエンティティを共同でランク付けし、その説明とともに推薦文を生成する方法を提案した。
The paper works on the movie recommendation scenario.
この論文では、映画の推薦シナリオを扱っている。
It produces a ranked list of entities as explanations by jointly ranking them with the corresponding movies.
それは、対応する映画と共同でランク付けすることにより、説明としてエンティティのランク付けされたリストを生成する。

Different from Catherine et al. (2017) that adopts rules and programs on KG for explainable recommendations, Ai et al. (2018) proposed to adopt KG embeddings for explainable recommendation, as shown in Figure 3.10.
説明可能な推薦のためにKG上のルールやプログラムを採用するCatherineら（2017）とは異なり，Aiら（2018）は，図3.10に示すように説明可能な推薦のためにKGエンベッディングを採用することを提案している。
The authors constructed a user-item knowledge graph, which contains various user, item, and entity relations, such as “user purchase item”, and “item belong to category”.
著者らは、「ユーザがアイテムを購入する」、「アイテムがカテゴリに属する」など、様々なユーザ、アイテム、エンティティの関係を含むユーザ・アイテム知識グラフを構築した。
KG embeddings are learned over the graph to obtain the embeddings of each user, item, entity, and relation.
このグラフに対してKG埋め込みを学習し、各ユーザ、アイテム、エンティティ、関係の埋め込みを得る。
To decide recommendations for a user, the model finds the most similar item under the purchase relation.
ユーザへの推薦を決定するために、このモデルは購入関係の下で最も類似したアイテムを見つける。
Besides, explanations can be provided by finding the shortest path from the user to the recommended item through the KG.
また、ユーザから推薦されたアイテムまでの最短経路をKGで求めることにより、説明を提供することができる。
By incorporating explicit user queries, the model can be further extended to conduct explainable search over knowledge graphs (Ai et al., 2019).
明示的なユーザークエリを組み込むことで、このモデルは知識グラフ上で説明可能な検索を行うためにさらに拡張することができる（Ai et al.，2019）。

Wang et al. (2018a) proposed the Ripple Network, an end-to-end framework to incorporate KG into recommender systems.
Wangら（2018a）は、KGをレコメンダーシステムに組み込むためのエンドツーエンドのフレームワークであるRipple Networkを提案した。
Similar to ripples propagating on the surface of the water, the Ripple Network stimulates the propagation of user preferences over the knowledge entities.
水面を伝播する波紋と同様に、Ripple Networkは、知識エンティティ上のユーザーの嗜好の伝播を刺激する。
It automatically and iteratively extends a user’s potential interests through the links in the KG.
リップルネットワークは、KGのリンクを通じて、ユーザーの潜在的な興味関心を自動的に、かつ反復的に拡張する。
The multiple “ripples” activated by a user’s historically clicked items are thus superposed to form the preference distribution of the user for a candidate item, which can be used to predict the final click probability.
ユーザーが過去にクリックしたアイテムによって活性化された複数の「波紋」を重ね合わせ、候補となるアイテムに対するユーザーの嗜好分布を形成し、最終的なクリック確率の予測に利用することができる。
Explanations can also be provided by finding a path from the user and the recommended item over the knowledge graph.
また、ユーザと推奨アイテムの経路を知識グラフ上で求めることで、説明を行うことも可能である。

Huang et al. (2018) leveraged KG for recommendation with better explainability in a sequential recommendation setting.
Huangら（2018）は、逐次推薦の設定において、より良い説明可能性を持つ推薦のためにKGを活用しました。
The authors bridged Recurrent Neural Network (RNN) with Key-Value Memory Networks (KV-MN) for sequential recommendation.
著者らは、逐次推薦のためにRecurrent Neural Network (RNN) とKey-Value Memory Networks (KV-MN) を橋渡ししました。
The RNN component is used to capture a user’s sequential preference on items, while the memory network component is enhanced with knowledge of items to capture the users’ attribute-based preferences.
RNNのコンポーネントは、ユーザーのアイテムに対する逐次的な嗜好を捉えるために用いられ、一方、メモリネットワークのコンポーネントは、ユーザーの属性ベースの嗜好を捉えるためにアイテムに関する知識で拡張される。
Finally, the sequential preferences, together with the attribute-level preferences, are combined as the final representation of user preference.
最後に、逐次的な嗜好と属性レベルの嗜好を合わせて、ユーザーの嗜好の最終的な表現とする。
To explain the recommendations, the model detects those attributes that are taking effect when predicting the recommended item.
推薦を説明するために、モデルは推薦されたアイテムを予測する際に影響を及ぼしている属性を検出する。
For a particular music recommendation as an example, it can detect whether the album attribute is more important or the singer attribute is more important, where the attributes come from an external knowledge graph.
例えば、ある音楽を推薦する場合、アルバム属性がより重要なのか、歌手属性がより重要なのかを検出することができる（属性は外部の知識グラフに由来する）。
The model further enhances the explainability by providing value-level interpretability, i.e., suppose we already know that some attributes (e.g., album) play a critical role in determining the recommendation, the model further predicts the importance of different values for that attribute.
このモデルは、値レベルの解釈可能性を提供することで説明可能性をさらに高める、すなわち、ある属性（例えば、アルバム）が推薦を決定する上で重要な役割を果たすことが既に分かっているとすると、このモデルはさらにその属性に対する異なる値の重要性を予測するのである。
Huang et al. (2019) further incorporated multi-modality knowledge graph for explainable sequential recommendation.
Huangら（2019）は、説明可能な逐次推薦のために、さらにマルチモダリティ知識グラフを取り入れた。
Different from conventional item-level sequential modeling methods, the proposed method captured user dynamic preferences on user-item interaction-level by modeling the sequential interactions over knowledge graphs.
従来のアイテムレベルの逐次モデリング手法とは異なり、提案手法は知識グラフ上で逐次インタラクションをモデリングすることで、ユーザーとアイテムのインタラクションレベルでユーザーの動的プリファレンスを捕捉した。

To combine the power of machine learning and inductive rule learning, Ma et al. (2019b) proposed a joint learning framework to integrate explainable rule induction in KG with a rule-guided neural recommendation model.
機械学習と帰納的ルール学習の力を組み合わせるために、Maら（2019b）は、KGにおける説明可能なルール誘導をルール誘導型ニューラル推薦モデルと統合する共同学習フレームワークを提案しました。
The framework encourages two modules to complement each other in generating explainable recommendations.
このフレームワークでは、説明可能なレコメンデーションの生成において、2つのモジュールが互いに補完し合うように促している。
One module is based on inductive rules mined from item knowledge graphs.
1 つのモジュールは、アイテム知識グラフからマイニングされた帰納的ルールに基づく。
The rules summarize common multi-hop relational patterns for inferring the item associations, and they provide human-readable explanations for model prediction.
このルールはアイテムの関連性を推論するために一般的なマルチホップ関係パターンを要約し、モデル予測のために人間が読める説明を提供する。
The second module is a recommendation module, which is augmented by the induced rules.
第二のモジュールは推薦モジュールであり、誘導されたルールによって拡張される。
The KG inductive rules are translated into explanations, which connect the recommended item with the user’s purchase history.
KGの帰納的ルールは説明文に変換され、推薦されたアイテムとユーザの購買履歴を結びつける。

Real-world knowledge graphs are usually huge.
実世界の知識グラフは通常巨大である。
Enumerating all the paths between a user-item node pair for similarity calculation is usually computationally prohibitive.
類似度計算のためにユーザーとアイテムのノードペア間のすべてのパスを列挙することは、通常、計算上禁止されている。
To solve the problem, Xian et al. (2019) proposed a reinforcement reasoning approach over knowledge graphs for explainable recommendations, as shown in Figure 3.11.
この問題を解決するために、Xianら（2019）は、図3.11に示すように、説明可能な推薦のための知識グラフ上の強化推論アプローチを提案した。
The key idea is to train a reinforcement learning agent for pathfinding.
重要な考え方は、経路探索のための強化学習エージェントを訓練することである。
In the training stage, the agent starts from a user and is trained to reach the correct items with high rewards.
学習段階では，エージェントはユーザから出発し，報酬の高い正しいアイテムに到達するように訓練される．
In the inference stage, the agent will thus directly walk to correct items for recommendations, without having to enumerate all the paths between user-item pairs.
推論段階では、エージェントはユーザとアイテムのペアの間のすべての経路を列挙することなく、推薦のために正しいアイテムまで直接歩くことになる。

Knowledge graphs can also help to explain a blank-box recommendation model.
知識グラフは、ブランクボックスの推薦モデルを説明するのにも役立つ。
Zhang et al. (2020) proposed a knowledge distillation approach to explain black-box models for recommendation.
Zhang ら (2020) は推薦のためのブラックボックスモデルを説明するための知識蒸留法を提案した。
The authors proposed an end-to-end joint learning framework to combine the advantages of embedding-based recommendation models and path-based recommendation models.
著者らは、埋め込み型推薦モデルと経路型推薦モデルの長所を組み合わせるために、エンドツーエンドの共同学習フレームワークを提案した。
Given an embedding-based model that produces black-box recommendations, the proposed approach interprets its recommendation results based on differentiable paths on knowledge graphs; the differentiable paths, on the other hand, regularize the blackbox model with structured information encoded in knowledge graph for better performance.
ブラックボックス推薦を生成する埋め込み型モデルが与えられたとき、提案アプローチは知識グラフ上の微分可能なパスに基づいてその推薦結果を解釈する。一方、微分可能なパスは、より良いパフォーマンスのために、知識グラフに符号化された構造化情報でブラックボックスモデルを正則化する。

## 3.7. Rule Mining for Explainable Recommendation 3.7. 説明可能なレコメンデーションのためのルールマイニング

Rule mining approaches are essential for recommendation research.
ルールマイニングのアプローチは推薦の研究に不可欠である。
They usually have special advantages for explainable recommendations, because in many cases, they can generate very straightforward explanations for users.
ルールマイニングは説明可能なレコメンデーションに特化した手法であり、多くの場合、ユーザーに対して非常にわかりやすい説明を生成することができるからである。
The most frequently used rule mining technique for explainable recommendation is association rule mining (Agrawal et al., 1993, 1994).
説明可能なレコメンデーションに最もよく使われるルールマイニング技術は、アソシエーションルールマイニング（Agrawalら、1993、1994）である。
A very classic example is the “beer-diaper” recommendation originated from data mining research.
その典型的な例が、データマイニングの研究から生まれた「ビールとおむすび」の推薦である。

For example, Mobasher et al. (2001) leveraged association rule mining for efficient web page recommendation at large-scale.
例えば，Mobasher ら(2001)は，大規模な Web ページ推薦を効率的に行うために，アソシエーションルールマイニングを活用した．
Cho et al. (2002) combined decision tree and association rule mining for a webbased shop recommender system.
Cho ら（2002）は、決定木とアソシエーションルールマイニングを組み合わせて、ウェブベースの店舗推薦システムを構築した。
Smyth et al. (2005) adopted apriori association rule mining to help calculate item-item similarities, and applied association rule mining for the conversational recommendation task.
Smyth et al. (2005) は、項目と項目の類似性を計算するためにアプリオリ・アソシエーションルールマイニングを採用し、会話型推薦タスクにアソシエーションルールマイニングを適用した。
Sandvig et al. (2007) studied the robustness of collaborative recommendation algorithms based on association rule mining.
Sandvigら（2007）は、アソシエーションルールマイニングに基づく協調推薦アルゴリズムの頑健性を研究した。
Zhang et al. (2015a) defined a sequence of user demands as a web browsing task, by analyzing user browsing logs, they leveraged frequent pattern mining for task-based recommendations.
Zhangら（2015a）は、ユーザーの一連の要求をウェブ閲覧タスクとして定義し、ユーザーの閲覧ログを分析することで、タスクベースの推薦のために頻出パターンマイニングを活用した。
More comprehensively, Amatriain and Pujol (2015) provided a survey of data mining for personalized recommendation systems.
より包括的には、Amatriain and Pujol (2015)は、パーソナライズされた推薦システムのためのデータマイニングのサーベイを提供した。

In terms of explainable recommendation, Lin et al. (2000, 2002) investigated association rules for recommendation systems.
説明可能な推薦という点では、Linら（2000, 2002）が推薦システムにおけるアソシエーションルールについて研究している。
In particular, the authors proposed a “personalized” association rule mining technique, which extracts association rules for a target user.
特に、著者らは、ターゲットユーザに対するアソシエーションルールを抽出する「パーソナライズド」アソシエーションルールマイニング技術を提案した。
The associations between users and items are employed to make recommendations, which are usually self-explainable by the association rules that produced them, for example, “90% of the articles liked by user A and user B are also liked by user C”.
ユーザとアイテムの間の関連性を利用して推薦を行うが，その推薦文は，例えば，「ユーザAとユーザBが好きな記事の90%はユーザCも好き」というように，推薦文を生成した関連性ルールによって自己説明可能であることが一般的である．

Davidson et al. (2010) introduced the YouTube Video Recommendation System.
Davidson ら (2010) は，YouTube 動画推薦システムを紹介した．
The authors considered the sessions of user watch behaviors on the site.
著者らは，サイト上でのユーザの視聴行動のセッショ ンを考慮した．
For a given period (usually 24 hours), the authors adopted association rule mining to count how often each pair of videos (vi , vj ) were co-watched within the same session, which helps to calculate the relatedness score for each pair of videos.
そして，ある期間（通常は 24 時間）において，同じセッション内で各ビデオのペア（vi , vj ）がどれだけ多く co-watch されたかをカウントし，各ビデオのペアの関連性スコアを計算するために，アソシエーション・ルール・マイニングを採用している．
To provide personalized recommendations, the authors consider a video seed set for each user, which includes videos the user watched recently, and videos the user explicitly favorited, liked, rated, or added to playlists.
このビデオには，ユーザが最近視聴したビデオや，ユーザが明示的に「お気に入り」，「いいね」，「評価」，「プレイリストへの追加」を行ったビデオなどが含まれる．
Related videos of these seed videos are recommendations, while the seed video, as well as the association rules that triggered the recommendation, are taken as explanations, as shown in Figure 3.12.
これらの種ビデオの関連動画がレコメンデーションとなり，図3.12に示すように，種ビデオとレコメンデーションのきっかけとなった関連ルールが説明として扱われる。

Recently, Balog et al. (2019) proposed a set-based approach for transparent, scrutable, and explainable recommendations.
最近、Balog ら (2019) は、透明で精査可能な説明可能な推薦のためのセットベースのアプローチを提案した。
Please note that although we discuss this work in this section of rule mining for explainable recommendation, the proposed approach is a framework that can be generalized to machine learning models depending on how item priors are estimated.
この研究では、説明可能な推薦のためのルールマイニングのセクションで議論しているが、提案されたアプローチは、項目プリオールの推定方法によって機械学習モデルに一般化できるフレームワークであることに留意してほしい。
The proposed model assumes that user preferences can be characterized by a set of tags or keywords.
提案モデルは、ユーザーの嗜好がタグやキーワードの集合によって特徴付けられることを想定している。
These tags may be provided by users (social tagging) or extracted automatically.
これらのタグはユーザから提供されたもの（ソーシャルタギング）、あるいは自動的に抽出されたものである。
Given explicit ratings of specific items, it infers set-based preferences by aggregating over items associated with a tag.
特定のアイテムの評価が与えられた場合、タグに関連付けられたアイテムについて集計することにより、セットベースの嗜好を推論することができる。
This set-based user preference model enables us to generate item recommendations transparently and provide sentence-level textual explanations.
このセットベースのユーザー嗜好モデルにより、透明性のあるアイテム推薦を生成し、文レベルのテキストによる説明を提供することができる。
A significant advantage of this explainable recommendation model is that it provides scrutability by letting users provide feedback on individual sentences.
この説明可能な推薦モデルの大きな利点は、ユーザーに個々の文章に対するフィードバックを提供させることで、精査可能性を提供することである。
Any change to the user’s preferences has an immediate impact, thereby endowing users with more direct control over the recommendations they receive.
また、ユーザーの嗜好を変更すると即座に反映されるため、ユーザーが受け取る推薦文をより直接的にコントロールすることが可能となる。

## 3.8. Model Agnostic and Post Hoc Explainable Recommendation 3.8. モデル不可知論とポストホック説明可能な推奨事項

Sometimes the recommendation mechanism may be too complex to explain.
レコメンデーションの仕組みが複雑すぎて説明できない場合がある。
In such cases, we rely on post-hoc or model-agnostic approaches to explainable the recommendations.
このような場合、レコメンデーションを説明可能にするために、ポストホックアプローチやモデルアグノスティックアプローチに頼ることになる。
In these methods, recommendations and explanations are generated from different models – an explanation model (independent from the recommendation mechanism) provides explanations for the recommendation model after the recommendations have been provided (thus “post-hoc”).
これらの方法では、推薦と説明は異なるモデルから生成される。（推薦メカニズムから独立した）説明モデルは、推薦が行われた後に推薦モデルに対する説明を行う（したがって「ポストホック」である）。

For example, in many e-commerce systems, the items are recommended based on very sophisticated hybrid models, but after an item is recommended, we can provide some simple statistical information as explanations, such as “70% of your friends bought this item”.
例えば、多くのeコマースシステムでは、非常に高度なハイブリッドモデルに基づいて商品を推奨しているが、商品が推奨された後に、「あなたの友人の70%がこの商品を買いました」というような簡単な統計情報を説明として提供することが可能である。
Usually, we pre-define several possible explanation templates based on data mining methods, such as frequent itemset mining and association rule mining, and then decide which explanation(s) to display based on post-hoc statistics such as maximum confidence.
通常、頻出アイテムセットマイニングやアソシエーションルールマイニングなどのデータマイニング手法により、説明のテンプレートをあらかじめ複数定義しておき、最大信頼度などのポストホック統計に基づいて、どの説明を表示するかを決定する。
It should be noted that just because the explanations are post-hoc does not mean that they are fake, i.e., the statistical explanations should be true information, they are just decoupled from the recommendation model.
ここで注意すべきは、説明がポストホックだからといって、それが偽物であるとは限らないことである。つまり、統計的な説明は真の情報であるべきで、推薦モデルから切り離されているだけなのである。

Peake and Wang (2018) provided an association rule mining approach to post-hoc explainable recommendations.
Peake and Wang (2018) は、事後的に説明可能なレコメンデーションに対するアソシエーション・ルール・マイニングのアプローチを提供した。
The authors treated an arbitrary recommendation model – in this paper, a matrix factorization model – as a black box.
著者らは、任意のレコメンデーションモデル（本稿では、行列分解モデル）をブラックボックスとして扱った。
Given any user, the recommendation model takes the user history as input and outputs the recommendations.
任意のユーザが与えられると、推薦モデルはユーザの履歴を入力とし、推薦を出力する。
The input and output constitute a transaction, and transactions of all users are used to extract association rules.
入力と出力は1つのトランザクションを構成し、全ユーザーのトランザクションを使用してアソシエーションルールを抽出する。
The association rules can then be used to explain the recommendations produced by the black-box model – if an item recommended by the black-box model can also be recommended out of the association rules, we thus say that this item is explainable by the rules, such as “{X ⇒ Y }:
ブラックボックスモデルが推薦する項目が、アソシエーションルールからも推薦できる場合、その項目は「{X ⇒ Y }」のようにルールで説明可能である、と言うのである。
Because you watched X, we recommend Y”.
Xを見たからYを薦める」というように。
The authors also adopted fidelity to evaluate the post-hoc explanation model, which shows what percentage of items can be explained by the explanation model.
また、著者らは、説明モデルで説明できる項目が何％あるかを示すfidelityを採用し、ポストホック説明モデルの評価を行っている。

Singh and Anand (2018) studied the post-hoc explanations of learning-to-rank algorithms in terms of web search.
Singh and Anand (2018) は、ウェブ検索の観点から Learning-to-rank アルゴリズムのポストホック説明を研究した。
In this work, the authors focused on understanding the ranker decisions in a model agnostic manner, and the rankings explainability is based on an interpretable feature space.
この作品では、著者らはモデルにとらわれない方法でランカーの決定を理解することに焦点を当て、ランキングの説明可能性は解釈可能な特徴空間に基づいている。
Technically, the authors first train a blackbox ranker, and then use the ranking labels produced by the ranker as secondary training data to train an explainable tree-based model.
技術的には、まずブラックボックスランカーを訓練し、次にランカーが生成したランキングラベルを二次訓練データとして用いて、説明可能なツリーベースモデルを訓練する。
The tree-based model is the post-hoc explanation model to generate explanations for the ranking list.
このツリーベースモデルは、ランキングリストに対する説明を生成するためのポストホック説明モデルである。
In this sense, Peake and Wang (2018) can be considered as a point-wise post-hoc explanation model, while Singh and Anand (2018) is a pair-wise post-hoc explanation model.
この意味で、Peake and Wang (2018) はポイントワイズ型ポストホック説明モデル、Singh and Anand (2018) はペアワイズ型ポストホック説明モデルと考えることができる。

In general machine learning context, a prominent idea of modelagnostic explanation is using simple models to approximate a complex model around a sample, so that the simple models help to understand the complex model locally.
一般的な機械学習の文脈では、サンプル周辺の複雑なモデルを単純なモデルで近似し、単純なモデルが局所的に複雑なモデルの理解を助けるというmodelagnostic explanationの考え方が著名である。
For example, Ribeiro et al. (2016) proposed LIME (Local Interpretable Model-agnostic Explanation), which adopts sparse linear models to approximate a complex (non-linear) classifier around a sample, and the linear model can thus explain to us which feature(s) of the sample contributed to its predicted label.
例えば、Ribeiroら（2016）はLIME（Local Interpretable Model-agnostic Explanation）を提案し、サンプルの周りの複雑な（非線形）分類器を近似するためにスパース線形モデルを採用し、このようにして線形モデルはサンプルのどの特徴（複数）がその予測ラベルに貢献したかを我々に説明できるようにしました。
Singh and Anand (2019) extended the idea to explore the local explainability of ranking models.
Singh and Anand (2019) は、このアイデアを拡張して、ランキングモデルの局所的な説明可能性を探った。
In particular, the authors converted the ranking problem over query-document pairs into a binary classification problem over relevant
特に、著者らは、クエリとドキュメントのペアに関するランキング問題を、関連する以下のようなバイナリ分類問題に変換した。

McInerney et al. (2018) developed a bandit approach to explainable recommendation.
McInerneyら(2018)は、説明可能な推薦のためのバンディットアプローチを開発した。
The authors proposed that users would respond to explanations differently and dynamically, and thus, a bandit-based approach for exploitation-exploration trade-off would help to find the best explanation orderings for each user.
著者らは、ユーザーは説明に対して異なる動的な反応を示すため、バンディットベースで搾取-探索のトレードオフを行うことで、各ユーザーにとって最適な説明の順序を見つけることができると提案した。
In particular, they proposed methods to jointly learn which explanations each user responds to, which are the best contents to recommend for each user, and how to balance exploration with exploitation to deal with uncertainty.
特に、各ユーザーがどの説明に反応するか、各ユーザーに推奨する最適なコンテンツはどれか、不確実性に対処するために探索と探索のバランスをどのようにとるかを共同で学習する方法を提案した。
Experiments show that explanations affect the way users respond to recommendations, and the proposed method outperforms the best static explanations ordering.
実験により、説明がユーザの推薦への反応に影響を与えることが示され、提案手法は最良の静的説明順序を凌駕することが示された。
This work shows that just as exploitation-exploration is beneficial to recommendation tasks, it is also beneficial to explanation tasks.
この研究は、exploitation-explorationが推薦タスクに有益であるのと同様に、説明タスクにも有益であることを示している。

Wang et al. (2018d) proposed a model-agnostic reinforcement learning framework to generate sentence explanations for any recommendation model (Figure 3.13).
Wangら(2018d)は、任意のレコメンデーションモデルに対する文章説明を生成するモデル不可知論的強化学習フレームワークを提案した（図3.13）。
In this design, the recommendation model to be explained is a part of the environment, while the agents are responsible for generating explanations and predicting the output ratings of the recommendation model based on the explanations.
この設計では、説明すべきレコメンデーションモデルは環境の一部であり、エージェントは説明文の生成と説明文に基づくレコメンデーションモデルの出力評価の予測を担当する。
The agents treat the recommendation model as a black box (model-agnostic) and interact with the environment.
エージェントはレコメンデーションモデルをブラックボックスとして扱い（モデル不可知論）、環境と対話する。
The environment rewards the agents if they can correctly predict the output ratings of the recommendation model (model-explainability).
環境はエージェントがレコメンデーションモデルの出力評価を正しく予測できた場合に報酬を与える（モデル説明可能性）。
Based on some prior knowledge about desirable explanations (e.g., the desirable length), the environment also rewards the agents if the explanations have good presentation quality (explanation quality control).
また、望ましい説明文（例えば、望ましい長さ）に関する事前知識に基づいて、説明文のプレゼンテーション品質が良ければ、環境はエージェントに報酬を与える（説明文品質管理）。
The agents learn to generate explanations with good explainability and presentation quality by optimizing the expected reward of their actions.
エージェントは、自分の行動の期待報酬を最適化することで、説明性と提示品質の良い説明を生成するように学習する。
In this way, the recommendation model reinforces the explanation model towards better post-hoc explanations.
このように、推薦モデルは、より良い事後説明に向けて説明モデルを強化する。

Cheng et al. (2019a) contributed mathematical understandings to post-hoc explainable recommendations based on influence analysis.
Chengら（2019a）は、影響度分析に基づく事後説明可能なレコメンデーションに数学的理解を貢献した。
Influence functions, which stem from robust statistics, have been used to understand the effect of training points on the predictions of black-box models.
ロバスト統計に由来する影響関数は、ブラックボックスモデルの予測に対する学習点の影響を理解するために使用されてきた。
Inspired by this, the authors propose an explanation method named FIA (Fast Influence Analysis), which helps to understand the prediction of trained latent factor models by tracing back to the training data with influence functions.
これに触発された著者らは、FIA (Fast Influence Analysis) と名付けた説明手法を提案し、影響関数を用いて学習データに遡り、学習済み潜在的因子モデルの予測値を理解することを支援する。
They presented how to employ influence functions to measure the impact of historical user-item interactions on the prediction results of LFMs, and provided intuitive neighbor-style explanations based on the most influential interactions.
彼らは、影響関数を用いて、過去のユーザとアイテムの相互作用がLFMの予測結果に与える影響を測定し、最も影響力のある相互作用に基づいて直感的な隣人風の説明を提供する方法を提示しました。

Overall, post-hoc explainable recommendation approaches attempt to develop an explanation model to explain a black-box prediction model.
全体として、ポストホック説明可能なレコメンデーションアプローチは、ブラックボックス予測モデルを説明するために説明モデルを開発しようとするものである。
Though the explanations may not strictly follow the exact mechanism that produced the recommendations (i.e., explanation fidelity may be limited), they have advantages in the flexibility to be applied in many different recommendation models.
しかし、説明の忠実度は低く、様々な推薦モデルに適用できる柔軟性がある。

## 3.9. Summary 3.9. まとめ

In this section, we introduced different machine learning models for explainable recommendations.
本節では、説明可能なレコメンデーションのためのさまざまな機械学習モデルを紹介した。
We first provided an overview of machine learning for recommender systems, and then, we focused on different types of explainable recommendation methods, including matrix
まず、推薦システムのための機械学習の概要を説明し、次に、説明可能な推薦方法の様々なタイプに焦点を当てた。

Explainable recommendation research can consider the explainability of either the recommendation methods or the recommendation results, corresponding to model-intrinsic and model-agnostic approaches (Lipton, 2018).
説明可能な推薦研究は、推薦方法と推薦結果のどちらかの説明可能性を考慮することができ、モデル内在的アプローチとモデル不可知論的アプローチに相当する（Lipton, 2018）。
It is interesting to see that both modeling philosophies have their roots in human cognitive science (Miller, 2019).
どちらのモデリング哲学も、そのルーツが人間の認知科学にあることは興味深い（Miller, 2019）。
Sometimes, human-beings make decisions based on careful logical reasoning, so they can clearly explain how a decision is made by showing the reasoning process step by step (Lipton, 2018).
人間は慎重な論理的推論に基づいて意思決定を行うことがあるので、推論過程を段階的に示すことで、意思決定の方法を明確に説明できる（Lipton, 2018）。
In this case, the decision model is transparent and the explanations can be naturally provided.
この場合、意思決定モデルは透明であり、説明も自然に行うことができる。
Other times, people make intuition decisions first, and then “seek” an explanation for the decision, which belongs to the post-hoc explanation approach (Miller, 2019).
他にも、まず直感的に意思決定し、その後に説明を「求める」場合もあり、これは事後的説明アプローチに属する（Miller, 2019）。
It is difficult to say which research philosophy towards explainable recommendation – and explainable AI in a broader sense – is the correct approach (maybe both).
説明可能なレコメンデーション、そして広い意味での説明可能なAIに向けた研究理念は、どちらが正しいアプローチなのか（もしかしたら両方かもしれません）、なかなか言い切れないのが現状です。
Answering this question requires significant breakthroughs in human cognitive science and our understanding about how the human brain works.
この問いに答えるには、人間の認知科学と、人間の脳の働きに関する理解において、大きなブレークスルーが必要です。

# 4. Evaluation of Explainable Recommendation 4. 説明可能なレコメンデーションの評価

In this section, we provide a review of the evaluation methods for explainable recommendations.
本節では、説明可能な推薦の評価方法について概説する。
It would be desirable if an explainable recommendation model can achieve comparable or even better recommendation performance than conventional “non-explainable” methods, and meanwhile, achieve better explainability.
説明可能な推薦モデルが、従来の「説明不可能な」手法と同等かそれ以上の推薦性能を達成し、一方でより優れた説明可能性を達成できれば望ましい。
To evaluate the recommendation performance, we can adopt the same measures as evaluating conventional recommendation algorithms.
推薦性能の評価には、従来の推薦アルゴリズムの評価と同じ尺度を採用することができる。
For rating prediction tasks, we can use mean absolute error (MAE) or root mean square error (RMSE), while for top-n recommendation, we can adopt standard ranking measures such as precision, recall, Fmeasure, and normalized discounted cumulative gain (NDCG).
評価予測タスクでは、平均絶対誤差（MAE）や二乗平均平方根誤差（RMSE）、トップNレコメンデーションでは、精度、再現率、Fmeasure、正規化割引累積利益（NDCG）などの標準的なランキング尺度を採用することが可能である。
We can also conduct online evaluations with real users based on online measures such as click-through rate (CTR) and conversion rate, which are frequently used to evaluate ranking performance.
また、ランキングの性能評価によく用いられるクリックスルー率（CTR）やコンバージョン率などのオンライン指標に基づき、実ユーザによるオンライン評価を行うことも可能である。
In this section, we mainly focus on the evaluation of explanations.
ここでは、主に説明文の評価について述べる。
Similarly, explanations can also be evaluated both online and offline.
説明文の評価には、オンラインとオフラインの両方がある。
Usually, offline evaluation is easier to implement, since online evaluation and user studies would depend on the availability of data and users in real-world systems, which are not always accessible to researchers.
オンライン評価やユーザ調査は、実世界のシステムにおけるデータやユーザの有無に依存し、研究者が常にアクセスできるとは限らないため、通常、オフライン評価の方が実施しやすい。
As a result, online evaluation is encouraged but not always required for
そのため、オンライン評価は推奨されますが、必ずしも必要ではありません。

explainable recommendation research.
説明可能なレコメンデーション研究。

## 4.1. User Study 4.1. ユーザー調査

A straightforward approach to evaluating explanations is through user study based on volunteers or paid experiment subjects.
説明を評価するための簡単なアプローチは、ボランティアや有償の実験被験者に基づくユーザー調査である。
The volunteers or paid subjects can either be directly recruited by the researchers or through online crowdsourcing platforms such as Amazon Mechanical Turk1 and CrowdFlower.2 Usually, the study will design some questions or tasks for the subjects to answer or complete, and conclusions will be derived from the responses of the subjects (Kittur et al., 2008).
ボランティアや有償の被験者は、研究者が直接募集する場合と、Amazon Mechanical Turk1やCrowdFlower2などのオンラインクラウドソーシングプラットフォームを通じて募集する場合がある。通常、研究では被験者が回答または完了するためのいくつかの質問またはタスクを設計し、被験者の回答から結論を導く（Kittur et al.、2008）。

For example, Herlocker et al. (2000) studied the effectiveness of different explanation styles in user-based collaborative filtering.
例えば、Herlocker ら (2000) はユーザーベースの協調フィルタリングにおける異なる説明スタイルの有効性を研究した。
In this research, the study was performed as a survey, and study participants were presented with the following hypothetical situation:
この研究では、調査はアンケートとして行われ、調査参加者は以下のような仮想的な状況を提示された。

> Imagine that you have $7 and a free evening coming up.
> 7ドルと自由な夜が迫っていると想像してください。
> You are considering going to the theater to see a movie, but only if there is a movie worth seeing.
> あなたは映画館に映画を見に行こうと考えていますが、それは見る価値のある映画がある場合だけです。
> To determine if there is a movie worth seeing, you consult MovieLens for a personalized movie recommendation.
> 見る価値のある映画があるかどうかを判断するために、あなたはMovieLensに相談し、個人的に映画を推薦してもらいます。
> MovieLens recommends one movie, and provides some justification.
> MovieLensは、1本の映画を推薦し、その理由を説明します。

Each participant was then provided with 21 individual movie recommendations, each with a different explanation component (see Figure 2.2 for two examples), and asked to rate on a scale of one to seven how likely they would be to go and see the movie.
次に、各被験者に、それぞれ異なる説明要素を持つ21の個別のおすすめ映画を提供し（2つの例は図2.2参照）、その映画を見に行く可能性を1～7で評価するよう求めた。
The subject’s average responses on each explanation are thus calculated to evaluate the effectiveness the explanation.
このように、各説明に対する被験者の平均的な回答を算出することで、説明の効果を評価している。

Vig et al. (2009) conducted a user study for four explanation interfaces based on the MovieLens website, as shown in Figure 4.1.
Vig ら（2009）は、図 4.1 に示すように、MovieLens の Web サイトをベースとした 4 つの説明インターフェイスのユーザ調査を実施した。
Subjects complete an online survey, in which they evaluate each interface about how well it helps them to:
被験者は、オンラインサーベイに参加し、各インター フェースがどの程度役立つかを評価する。

1. understand why an item is recommended (justification), 2) decide if they like the recommended item (effectiveness), and 3) determine if the recommended item matches their mood (mood compatibility).
   この調査では、被験者がそれぞれのインタフェースについて、1) なぜそのアイテムが勧められるのかを理解すること（正当化）、2) そのアイテムが好きかどうかを判断すること（有効性）、3) そのアイテムが自分の気分に合っているかどうか（気分適合性）、について評価しています。
   The survey responses help the authors to conclude the role of tag preference and tag relevance in promoting justification, effectiveness, and mood compatibility.
   この調査から、タグの嗜好性と関連性が、正当性、有効性、気分の適合性を促進する上でどのような役割を果たすかを結論付けることができました。

User study is also used to evaluate recent machine learning approaches to explainable recommendation.
説明可能なレコメンデーションに対する最近の機械学習アプローチの評価には、ユーザー調査も利用されている。
For example, Wang et al. (2018b) recruited participants through Amazon Mechanical Turk to evaluate with a diverse population of users.
例えば、Wangら（2018b）は、多様なユーザー集団で評価するために、Amazon Mechanical Turkを通じて参加者を募集しました。
The study is based on the review data in Amazon and Yelp datasets.
この研究は、AmazonとYelpのデータセットのレビューデータに基づいている。
For each participant, the authors randomly selected a user from the dataset, and showed this user’s reviews to the participant, so that the participant can get familiar with the user.
各参加者に対し、著者らはデータセットからランダムにユーザーを選び、このユーザーのレビューを参加者に見せ、参加者がこのユーザーに親しみを持てるようにしました。
Participants are then asked to infer the user’s preference based on these reviews.
そして、参加者はこれらのレビューに基づいてユーザーの好みを推論するよう求められる。
Then they will be asked to evaluate the recommendations and explanations provided to the user by answering several survey questions from this user’s perspective.
そして、このユーザーの視点から、いくつかの調査項目に答えることで、ユーザーに提供された推奨事項や説明を評価してもらいます。
Except for textual explanations, user study is also used to evaluate visual explanations, for example, Chen et al. (2019b) generated visual explanations by highlighting image region-of-interest to users, and leveraged Amazon MTurk to hire freelancers to label the ground-truth images for evaluation.
文字による説明以外では、視覚的な説明の評価にもユーザー調査が利用されており、例えば、Chenら（2019b）は、ユーザーに画像のregion-of-interestを強調することで視覚的説明を生成し、Amazon MTurkを活用してフリーランスを雇い、評価のためのグランドトルース画像にラベル付けをさせたという。

Besides large-scale online workers, we may also conduct user studies with relative small-scale volunteers, paid subjects, or manually labeling the explanations.
大規模なネットワーカー以外にも、比較的小規模なボランティアや有償の被験者、あるいは手動でラベリングした説明文を用いてユーザー調査を実施することも考えられる。
For example, Wang and Benbasat (2007) adopted a survey-based user study approach to investigate the trust and understandability of content-based explanations.
例えば、Wang and Benbasat（2007）は、調査ベースのユーザー研究アプローチを採用し、コンテンツベースの説明の信頼性と理解可能性を調査している。
They examined the effects of three explanation types – how, why, and trade-off explanations – on consumers’ trusting beliefs in competence, benevolence, and integrity.
彼らは、3種類の説明（方法、理由、トレードオフ説明）が、消費者の能力、善意、誠実さに対する信頼信念に与える影響を調査した。
The authors built a recommendation system experimental platform, and results confirmed the critical role of explanation in enhancing consumers’ initial trusting beliefs.
著者らは、推薦システムの実験プラットフォームを構築し、結果は、消費者の初期の信頼信念を高めるために説明が重要な役割を果たすことを確認した。
Ren et al. (2017) took a random sample of 100 recommendations, and manually evaluated their explanations regarding the accuracy of sentiment labels, which helped to verify that the proposed viewpoint-based explanations are more informative than topic labels in prior work.
Renら（2017）は、100のレコメンデーションのランダムサンプルを取り、センチメントラベルの精度に関する説明を手動で評価し、提案した視点ベースの説明が先行研究におけるトピックラベルよりも有益であることを検証するのに役立った。

## 4.2. Online Evaluation 4.2. オンライン評価

Another approach to evaluating explainable recommendation is through online experiments.
説明可能なレコメンデーションを評価するもう一つのアプローチとして、オンライン実験があります。
There could be several different perspectives to consider, including persuasiveness, effectiveness, efficiency, and satisfaction of the explanations.
説得力、効果、効率、説明の満足度など、いくつかの異なる視点が考えられる。

Due to the limited type of information that one can collect in online systems, it is usually easier to evaluate the persuasiveness of the explanations, i.e., to see if the explanations can help to make users accept the recommendations.
オンラインシステムで収集できる情報の種類が限られているため、通常は説明の説得力を評価すること、すなわち、説明がユーザーに推薦を受け入れさせるのに役立つかどうかを確認することが容易である。
For example, Zhang et al. (2014a) conducted online experiments focusing on how the explanations affect user acceptance.
例えば、Zhangら（2014a）は、説明がユーザーの受容にどのように影響するかに焦点を当てたオンライン実験を行った。
The authors conducted A
著者らが行ったのは、A

We should note that the evaluation measures in online scenarios could vary depending on the availability of the resources in the testing environment.
オンラインシナリオにおける評価指標は、テスト環境におけるリソースの利用可能性に応じて変化し得ることに留意する必要がある。
For example, one may evaluate based on click-throughrate (CTR) when user click information is available, or calculate the purchase rate if user purchase actions can be tracked, or even calculate the gross profit if product price information is available.
例えば、ユーザーのクリック情報があればクリックスルー率（CTR）を、ユーザーの購買行動が追跡できれば購買率を、商品価格情報があれば粗利を算出することができます。

Online evaluation and user study may be concurrently performed, i.e., sometimes user study can be performed in online platforms, however, they also have significant differences regardless the operating platform.
オンライン評価とユーザースタディは同時に実施されることもあり、ユーザースタディがオンラインプラットフォームで実施されることもあるが、操作プラットフォームに関係なく大きな違いがあるのも事実である。
User study usually asks participants to complete certain questions or tasks under given experimental instructions, as a result, participants usually know that they are being investigated.
ユーザースタディは、通常、与えられた実験的な指示のもとで、特定の質問やタスクに答えてもらうものであり、その結果、参加者は自分が調査されていることを通常知ることになる。
Online evaluation such as A
のようなオンライン評価もあります。

## 4.3. Offline Evaluation 4.3. オフライン評価

In general, there are two approaches to evaluating recommendation explanations offline.
一般に，オフラインでのレコメンデーション説明の評価には，2つのアプローチがある．
One is to evaluate the percentage of recommendations that can be explained by the explanation model, regardless of the explanation quality; and the second approach is to evaluate the explanation quality directly.
一つは、説明の質に関係なく、説明モデルで説明できるレコメンデーションの割合を評価する方法、もう一つは、説明の質を直接評価する方法である。
However, we have to note that more offline evaluation measures
しかし、よりオフラインでの評価手段である

For the first approach, Abdollahi and Nasraoui (2017) adopted mean explainability precision (MEP) and mean explainability recall (MER).
最初のアプローチとして、Abdollahi and Nasraoui（2017）は、平均説明可能精度（MEP）と平均説明可能リコール（MER）を採用しました。
More specifically, explainability precision (EP) is defined as the proportion of explainable items in the top-n recommendation list, relative to the total number of recommended (top-n) items for each user.
具体的には、説明可能精度（EP）は、各ユーザーの推奨項目（トップn）の総数に対する、トップnの推奨リストにおける説明可能な項目の割合として定義されます。
Explainability recall (ER), on the other hand, is the proportion of explainable items in the top-n recommendation list, relative to the total number of explainable items for a given user.
一方、説明可能性再現率（ER）は、各ユーザーの説明可能なアイテムの総数に対する、上位n個の推薦リストにおける説明可能なアイテムの割合である。
Finally, mean explainability precision (MEP) and mean explainability recall (MER) are EP and ER averaged across all testing users, respectively.
最後に、平均説明可能精度（MEP）および平均説明可能リコール（MER）は、それぞれ全テストユーザーで平均化したEPおよびERである。
Peake and Wang (2018) further generalized the idea and proposed model Fidelity as a measure to evaluate explainable recommendation algorithms, which is defined as the percentage of explainable items in the recommended items:
Peake and Wang (2018)はさらにアイデアを一般化し、説明可能な推薦アルゴリズムを評価する指標としてモデルFidelityを提案し、これは推薦項目における説明可能な項目の割合として定義される。

$$
\text{Model Fidelity} = \frac{|\text{explainable items} \cap \text{recommended items}|}{|\text{recommended items}|}
$$

For the second approach, evaluating the quality of the explanations usually depends on the type of explanations.
2つ目のアプローチでは、説明の質を評価するには、通常、説明の種類に依存する。
One commonly used explanation type is a piece of explanation sentence.
よく使われる説明のタイプとして、説明文の断片がある。
In this case, offline evaluation can be conducted with text-based measures.
この場合、オフラインでの評価は、テキストベースの測定で行うことができる。
For example, in many online review websites (such as e-commerce), we can consider a user’s true review for an item as the ground-truth explanation for the user to purchase the item.
例えば、多くのオンラインレビューサイト（eコマースなど）において、ある商品に対するユーザーの真偽のレビューを、ユーザーがその商品を購入するための根拠となる説明文と考えることができる。
If our explanation is a textual sentence, we can take frequently used text generation measures for evaluation, such as BLEU score (bilingual evaluation understudy, Papineni et al., 2002) and ROUGE score (recall-oriented understudy for gisting evaluation, Lin, 2004).
説明がテキスト文の場合、BLEU score (bilingual evaluation understudy, Papineni et al., 2002) やROUGE score (recall-oriented understudy for gisting evaluation, Lin, 2004) など、頻繁に用いられるテキスト生成指標を評価指標とすることが可能である。
The explanation quality can also be evaluated in terms of readability measures, such as Gunning Fog Index (Gunning, 1952), Flesch Reading Ease (Flesch, 1948), Flesch Kincaid Grade Level (Kincaid et al., 1975), Automated Readability Index (Senter and Smith, 1967), and Smog Index (Mc Laughlin, 1969).
また、説明の質は、Gunning Fog Index (Gunning, 1952), Flesch Reading Ease (Flesch, 1948), Flesch Kincaid Grade Level (Kincaid et al., 1975), Automated Readability Index (Senter and Smith, 1967), Smog Index (Mc Laughlin, 1969) など、読みやすさを表す指標で評価することが可能である。

Overall, regardless of the explanation style (text or image or others), offline explanation quality evaluation would be easy if we have (small scale) ground-truth explanations.
全体として、説明のスタイル（テキスト、画像、その他）に関わらず、（小規模の）真実の説明があれば、オフラインでの説明の品質評価は容易であろう。
In this way, we can evaluate how well the generated explanations match with the ground-truth, in terms of precision, recall, and their variants.
このように、生成された説明がどの程度真実に適合しているかを、精度、再現率、およびその変化率の観点から評価することができる。

## 4.4. Qualitative Evaluation by Case Study 4.4. ケーススタディによる定性的評価

Case study as the qualitative analysis is also frequently used for explainable recommendation research.
説明可能なレコメンデーション研究では、定性分析としてのケーススタディもよく利用される。
Providing case studies can help to understand the intuition behind the explainable recommendation model and the effectiveness of explanations.
事例を提供することで、説明可能なレコメンデーションモデルの背後にある直感や説明の有効性を理解することができる。
Providing case studies as qualitative analysis also helps to understand when the proposed approach works and when it does not work.
また、質的分析として事例を提供することで、提案されたアプローチがどのような場合に有効で、どのような場合に有効でないかを理解することができます。

For example, Chen et al. (2018c) provided case study to explain the sequential recommendations, as shown in Figure 4.3.
例えば、Chen ら（2018c）は、図 4.3 に示すように、逐次推薦を説明するためのケーススタディを提供している。
Through case studies, the authors found that many sequential recommendations can be explained by “one-to-multiple” or “one-to-one” user behavior patterns.
事例研究を通じて、著者らは、多くのシーケンシャル・レコメンデーションは、"one-to-multiple" または "one-to-one" のユーザー行動パターンによって説明できることを発見しました。
“One-to-multiple” means that a series of subsequent purchases are triggered by the same item, while “one-to-one” means that each of the subsequent purchases is triggered by its preceding item.
「一対多」とは、同じ商品をきっかけに次々と買い物をすることであり、「一対一」とは、前の商品をきっかけに次々と買い物をすることである。
These explanations can help users to understand why an item is recommended and how the recommended items match their already purchased items.
これらの説明により、ユーザーは、なぜそのアイテムがおすすめされるのか、おすすめされたアイテムがすでに購入したアイテムとどのようにマッチするのかを理解することができます。

Hou et al. (2018) adopted case studies to analyze the user preference, item quality, and explainability of the hotel recommendations.
Houら(2018)は、ケーススタディを採用し、ホテル推薦のユーザー嗜好、項目品質、説明可能性を分析した。
The authors first proposed a metric called Satisfaction Degree on Aspects (SDA) to measure the user satisfaction on item aspects, and then conducted case studies to show how the model explains the recommendations, as shown in Figure 4.4.
著者らはまず、アイテムの側面に対するユーザーの満足度を測るSDA（Satisfaction Degree on Aspects）という指標を提案し、図4.4に示すように、このモデルがどのようにレコメンドを説明するかを示すケーススタディを実施した。
In this example, item 1 is recommended instead of item 2 for the target user.
この例では、対象ユーザーに対して、アイテム2の代わりにアイテム1が推薦されている。
By examining the user preference and item quality, this recommendation is explained by the fact that item 1 satisfies user preferences over most aspects.
ユーザの嗜好とアイテムの品質を検討した結果，アイテム1がほとんどの側面でユーザの嗜好を満たしていることから，この推薦が説明される．

## 4.5. summary 4.5. まとめ

In this section, we introduced the evaluation methods for explainable recommendation research.
本節では、説明可能な推薦研究の評価手法を紹介した。
A desirable explainable recommendation model would not only be able to provide high-quality recommendations but also high-quality explanations.
説明可能なレコメンデーションモデルとは、質の高い推薦を行うだけでなく、質の高い説明も行えることが望ましい。
As a result, an explainable recommendation model would better be evaluated in terms of both perspectives.
そのため、説明可能な推薦モデルは、両者の観点から評価することが望ましい。

In this section, we first presented frequently used evaluation methods for recommendation systems, including both online and offline approaches.
本節では、まず、推薦システムの評価方法として、オンライン・オフラインを問わず、よく利用される方法を紹介した。
We further introduced methods particularly for explanation evaluation, including both quantitative and qualitative methods.
さらに、特に説明文の評価方法として、定量的方法と定性的方法を紹介した。
More specifically, quantitative methods include online, offline, and user study approaches, while qualitative evaluation is usually implemented by case studies over the generated explanations.
定量的評価には、オンライン、オフライン、ユーザスタディなどの手法があり、定性的評価には、生成された説明文に対するケーススタディがある。

# 5. Explainable Recommendation in Different Applications 5. さまざまな用途で説明可能なレコメンデーション

The research and application of explainable recommendation methods span across many different scenarios, such as explainable e-commerce recommendation, explainable social recommendation, and explainable multimedia recommendation.
説明可能な推薦手法の研究と応用は、説明可能な電子商取引推薦、説明可能な社会的推薦、説明可能なマルチメディア推薦など、さまざまなシナリオにまたがっている。

In this section, we provide a review of explainable recommendation methods in different applications.
本節では、様々なアプリケーションにおける説明可能な推薦手法のレビューを行う。
Most of the research papers in this section have already been introduced in previous sections.
このセクションの研究論文のほとんどはすでに前のセクションで紹介されている。
Instead, we organize them based on their application scenario to help readers better understand the current scope of explainable recommendation research and how it helps in different applications.
その代わりに、読者が説明可能な推薦の研究の現在の範囲と異なるアプリケーションでどのように役立つかについてよりよく理解できるように、アプリケーションシナリオに基づいてそれらを整理している。

## 5.1. Explainable E-commerce Recommendation 5.1. 説明可能な電子商取引のススメ

Product recommendation in e-commerce is one of the most widely adopted scenarios for explainable recommendations.
電子商取引における商品推奨は、説明可能な推奨のための最も広く採用されているシナリオの1つである。
It has been a standard test setting for explainable recommendation research.
説明可能なレコメンデーション研究の標準的なテスト設定となっている。

As an example of this scenario, Zhang et al. (2014a) proposed explainable recommendation based on the explicit factor model, and conducted online experiments to evaluate the explainable recommendations based on a commercial e-commerce website (JD.com).
このシナリオの例として，Zhangら（2014a）は明示的要因モデルに基づく説明可能な推薦を提案し，商用ECサイト（JD.com）に基づく説明可能な推薦を評価するオンライン実験を実施した．
Later, many explainable recommendation models are proposed for e-commerce recommendation.
その後、電子商取引推薦のための説明可能な推薦モデルが多く提案されている。
For instance, He et al. (2015) introduced a tripartite graph ranking algorithm for explainable recommendation of electronics products; Chen et al. (2016) proposed a learning to rank approach to cross-category explainable recommendation of the products; Seo et al. (2017) and Wu et al.
例えば、Heら（2015）はエレクトロニクス製品の説明可能な推薦のための三分割グラフランキングアルゴリズムを、Chenら（2016）は商品のカテゴリ横断的な説明可能な推薦のためのランク付け学習アプローチを、Seoら（2017）およびWuら（2017）は商品のカテゴリ横断的な説明可能な推薦のためのランク付け学習アプローチを、それぞれ紹介している。
(2019) conducted explainable recommendation for multiple product categories in Amazon, and highlighted important words in user reviews based on attention mechanism; Heckel et al. (2017) adopted overlapping co-clustering to provide scalable and interpretable product recommendations; Chen et al. (2019b) proposed a visually explainable recommendation model to provide visual explanations for fashion products; Hou et al.
(2019)はAmazonの複数の商品カテゴリに対して説明可能な推薦を実施し、注目メカニズムに基づいてユーザーレビューの重要語を強調した、Heckelら(2017)は重複コクラスタリングを採用して拡張可能で解釈可能な商品推薦を提供した、Chenら(2019b)はファッション商品の視覚的な説明を提供するために視覚的説明可能推薦モデルを提案した、Houら(2017)は商品カテゴリを横断して説明可能な推薦を実施し、Houら.
(2018) used product aspects to conduct explainable video game recommendation in Amazon; Chen et al. (2018a) leveraged neural attention regression based on reviews to conduct rating prediction on three Amazon product categories; Chen et al. (2018c) adopted memory networks to provide explainable sequential recommendations in Amazon; Wang et al. (2018b) leveraged multi-task learning with tensor factorization to learn textual explanations for Amazon product recommendation; By incorporating explicit queries, explainable recommendation can also be extended to explainable product search in e-commerce systems (Ai et al.,
(2018)は商品アスペクトを用いてAmazonで説明可能なビデオゲームレコメンデーションを実施した、Chenら(2018a)はレビューに基づくニューラルアテンション回帰を活用して3つのAmazon商品カテゴリで評価予測を実施した、Chenら(2018c)はメモリーネットワークを採用してAmazonで説明可能な逐次推薦を提供した、Wangら(2018b)はテンソル分解によるマルチタスキング学習を活用してAmazon商品推奨のテキスト説明を学んだ、明解な問い合わせを組み込むことにより説明可能な推薦もECシステムで説明可能な製品探索に拡張できる(Ai et al,
2019).
2019).

Explainable recommendations are essential for e-commerce systems, not only because it helps to increase the persuasiveness of the recommendations, but also because it helps users to make efficient and informed decisions (Schafer et al., 2001).
説明可能な推奨は、推奨の説得力を高めるだけでなく、ユーザが効率的かつ十分な情報を得た上で意思決定できるようにするため、電子商取引システムには不可欠である（Schafer et al.）
Since more and more consumer purchases are made in the online economy, it becomes essential for e-commerce systems to be socially responsible by achieving commercial profits and benefiting consumers with the right decisions simultaneously.
オンライン経済において、より多くの消費者の購買が行われるようになったため、電子商取引システムは、商業的利益を達成すると同時に、正しい判断で消費者に利益をもたらすという社会的責任を果たすことが不可欠になった。
Explainable recommendation – as a way to help users understand why or why not a product is the right choice – is an important technical approach to achieving the ultimate goal of socially responsible recommendations.
説明可能な推薦-ある商品がなぜ正しい選択なのか、あるいはなぜ正しくないのかをユーザに理解させる方法として-は、社会的責任ある推薦という最終目標を達成するための重要な技術的アプローチである。

## 5.2. Explainable Point-of-Interest Recommendation 5.2. 説明可能な関心事に関する推奨事項

Point-of-Interest (POI) recommendation – or location recommendation in a broader sense – tries to recommend users with potential locations of interest, such as hotels, restaurants, or museums.
POI（Point-of-Interest）推薦とは、広い意味での位置推薦であり、ホテル、レストラン、美術館など、ユーザーが興味を持ちそうな場所を推薦することを目的としている。
Explainable POI recommendation gained considerable interest in recent years.
近年、説明可能なPOI推薦に大きな関心が集まっている。
Most of the research is based on datasets from POI review websites, such as Yelp1 and TripAdvisor.2
この研究の多くは、Yelp1 や TripAdvisor2 などの POI レビューサイトからのデータセットに基づくものである。

By providing appropriate explanations in POI recommendation systems, it helps users to save time and minimize the opportunity cost of making wrong decisions, because traveling from one place to another usually means extensive efforts in time and money.
POI推薦システムにおいて適切な説明を提供することで、ユーザーは、ある場所から別の場所へ移動することは、通常、時間とお金に多大な努力を要するため、時間を節約し、誤った判断をする機会コストを最小化することができるようになる。
Besides, providing explanations in travel planning applications (such as TripAdvisor) helps users better understand the relationship between different places, which could help users to plan better trip routes in advance.
また、旅行計画アプリケーション（TripAdvisorなど）において説明を提供することで、ユーザーは異なる場所間の関係をよりよく理解できるようになり、より良い旅行経路を事前に計画することができるようになります。

In terms of explainable POI recommendation research, Wu and Ester (2015) conducted Yelp restaurant recommendation and TripAdvisor hotel recommendation.
説明可能な POI 推薦の研究では，Wu and Ester (2015) が Yelp のレストラン推薦と TripAdvisor のホテル推薦を実施した．
The authors proposed a probabilistic model combining aspect-based opinion mining and collaborative filtering to provide explainable recommendations, and the recommended locations are explained by a word cloud of location aspects.
著者らは説明可能な推薦を提供するために、アスペクトベースの意見マイニングと協調フィルタリングを組み合わせた確率的モデルを提案し、推薦された場所は場所のアスペクトのワードクラウドによって説明される。
Bauman et al. (2017) developed models to extract the most valuable aspects from reviews for the restaurant, hotel, and beauty&spa recommendations on Yelp.
Baumanら（2017）は、Yelpのレストラン、ホテル、beauty&spaの推薦のために、レビューから最も価値のあるアスペクトを抽出するモデルを開発した。
Seo et al. (2017) also conducted explainable restaurant recommendations on Yelp.
Seoら（2017）も、Yelp上の説明可能なレストラン推薦を行った。
The authors proposed interpretable convolutional neural networks to highlight informative review words as explanations.
著者らは解釈可能な畳み込みニューラルネットワークを提案し、情報量の多いレビューワードを説明として強調した。
Zhao et al. (2015) conducted POI recommendation based on Yelp data in the Phoenix city and Singapore, respectively, and the authors proposed a joint sentimentaspect-region modeling approach to generating recommendations.
Zhaoら（2015）は、フェニックス市とシンガポールでそれぞれYelpデータに基づくPOI推薦を実施し、著者らは推薦を生成するためのsentimentaspect-region joint modelingのアプローチを提案した。
Wang et al. (2018c) proposed a tree-enhanced embedding model for explainable tourist and restaurant recommendation based on TripAdvisor data in London and New York.
Wangら（2018c）は、ロンドンとニューヨークのTripAdvisorデータに基づく説明可能な観光客とレストランの推薦のためのツリー強化された埋め込みモデルを提案した。
Baral et al. (2018) proposed a dense subgraph extraction model based on user-aspect bipartite graphs for explainable location recommendation in location-based social networks.
Baralら（2018）は、ロケーションベースのソーシャルネットワークにおける説明可能なロケーション推薦のために、ユーザーアスペクトの二部グラフに基づく密なサブグラフ抽出モデルを提案した。
The results have shown that providing appropriate explanations increases the user acceptance on the location recommendations.
その結果、適切な説明を提供することで、位置推薦に対するユーザーの受容性が向上することが示された。

## 5.3. Explainable Social Recommendation 5.3. 説明可能なソーシャルレコメンデーション

Explainable recommendations also apply to social environments.
説明可能なレコメンデーションは、社会環境にも適用される。
Prominent examples include friend recommendations, news feeding recommendations, and the recommendation of blogs, news, music, travel plans, web pages, images, or tags in social environments.
例えば、友人の推薦、ニュース配信の推薦、ブログ、ニュース、音楽、旅行プラン、ウェブページ、画像、タグの推薦など、社会環境における推薦が代表的である。

Explainability of the social recommender systems is vitally important to the users’ trustworthiness in the recommendations, and trustworthiness is fundamental to maintain the sustainability of social networks (Sherchan et al., 2013).
ソーシャルレコメンダーシステムの説明可能性は，ユーザが推薦を信頼するために極めて重要であり，信頼性はソーシャルネットワークの持続可能性を維持するための基本である（Sherchan et al.，2013）．
For example, by providing the overlapping friends as explanations for friend recommendations on Facebook, it helps users to understand why an unknown person is related to them and why the recommended friend would be trusted.
例えば，Facebook の友達推薦において，重複する友達を説明として提供することで，未知の人物がなぜ自分と関係があるのか，推薦された友達がなぜ信頼されるのかをユーザが理解できるようにする．
By telling the user which of his or her friends have twitted a piece of news as explanations in Twitter, it helps the user to understand why the recommended news could be important for herself.
Twitterでは、あるニュースをどの友人がツイートしたかを説明として伝えることで、なぜそのおすすめニュースが自分にとって重要な可能性があるのかをユーザーに理解させることができます。
It also helps users to quickly identify useful information to save time in the era of information overload.
また、情報過多の時代において、ユーザーが有用な情報を素早く見極め、時間を短縮することができます。

Explainable recommendations in social environments are also important to the credibility of news recommendations (Bountouridis et al., 2018).
社会環境における説明可能なレコメンデーションは、ニュースレコメンデーションの信頼性にも重要である（Bountouridis et al, 2018）。
Since any individual can post and re-post news articles in the social environment, the system may be exploited to spread fake news or make unjustified influences on our society.
社会環境では、個人が誰でもニュース記事を投稿・再投稿できるため、そのシステムを悪用してフェイクニュースを拡散したり、社会に不当な影響を与えたりする可能性があります。
By explaining the credibility of news articles based on cross-referencing (Bountouridis et al., 2018), we can help users to identify credible vs. fake information in social environments, which is critical for national security.
相互参照に基づいてニュース記事の信頼性を説明することで (Bountouridis et al., 2018) 、ユーザーが社会環境において信頼できる情報とフェイク情報を識別できるようになり、国家安全保障にとって重要な役割を果たすことができるようになります。

In terms of the research on social explainable recommendation, Ren et al. (2017) proposed a social collaborative viewpoint regression model for rating prediction based on user opinions and social relations.
社会的説明可能な推薦に関する研究として、Renら（2017）は、ユーザーの意見と社会的関係に基づく評価予測のための社会的協調視点回帰モデルを提案しました。
The social relations not only help to improve the recommendation performance, but also the explainability of the recommendations.
社会的関係は、レコメンデーション性能の向上だけでなく、レコメンデーションの説明可能性の向上にも役立つ。
Quijano-Sanchez et al. (2017) developed a social explanation system applied to group recommendations.
Quijano-Sanchezら（2017）は、グループレコメンデーションに適用される社会的説明システムを開発した。
It integrates explanations about the group recommendations and explanations about the group’s social reality, which gives better perceptions of the group recommendations.
これは、グループ推薦に関する説明とグループの社会的現実に関する説明を統合し、グループ推薦のより良い認知を与えるものである。
Tsai and Brusilovsky (2018) studied how to design explanation interfaces for casual (nonexpert) users to achieve different explanatory goals.
Tsai and Brusilovsky (2018) は、カジュアル（非専門家）なユーザーに対して、異なる説明の目標を達成するために、どのように説明インターフェースを設計するかについて研究した。
In particular, the authors conducted an international online survey of a social recommender system – based on 14 active users and across 13 countries – to capture user feedback and frame it in terms of design principles of explainable social recommender systems.
特に、著者らは、ソーシャル・レコメンダー・システムの国際的なオンライン調査-14人のアクティブユーザーをベースに、13カ国にまたがる-を行い、ユーザーのフィードバックを把握し、説明可能なソーシャル・レコメンダー・システムの設計原則の観点からフレームを作成しました。
The research results have shown that explanations in social networks help to benefit social network users in terms of transparency, scrutability, trust, persuasiveness, effectiveness, efficiency and satisfaction.
調査の結果、ソーシャルネットワークにおける説明は、透明性、精査性、信頼性、説得力、有効性、効率性、満足度の面でソーシャルネットワーク利用者の利益につながることが示された。

## 5.4. Explainable Multimedia Recommendation 5.4. 説明可能なマルチメディアの推奨

Explainable multimedia recommendation broadly includes the explainable recommendation of books (Wang et al., 2018a), news
説明可能なマルチメディア推薦には、広くは書籍の説明可能な推薦（Wang et al, 2018a）、ニュース

The MovieLens dataset3 is one of the most frequently used datasets for movie recommendation (Herlocker et al., 2000).
MovieLens データセット3 は，映画推薦に最も頻繁に使用されるデータセットの一つである (Herlocker et al., 2000)．
Based on this dataset, Abdollahi and Nasraoui (2016) proposed explainable matrix factorization by learning the rating distribution of the active user’s neighborhood.
このデータセットに基づき、Abdollahi and Nasraoui (2016) はアクティブユーザーの近傍の評価分布を学習することにより、説明可能な行列分解を提案した。
In Abdollahi and Nasraoui (2017), the authors further extended the idea to the explainability of constrained matrix factorization.
Abdollahi and Nasraoui (2017)では、著者らはさらにこのアイデアを制約付き行列分解の説明可能性にまで拡張した。
Chang et al. (2016) adopted crowd-sourcing to generate crowd-based natural language explanations for movie recommendations in MovieLens.
Changら（2016）は、MovieLensにおける映画推薦のための群衆ベースの自然言語説明を生成するために、クラウドソーシングを採用した。
Lee and Jung (2018) provided story-based explanations for movie recommendation systems, achieved by a multi-aspect explanation and narrative analysis method.
Lee and Jung (2018)は、多面的説明と物語分析手法によって実現された、映画推薦システムのための物語に基づく説明を提供した。

Based on a knowledge-base of the movies, such as the genre, type, actor, and director, recent research has been trying to provide knowledgeaware explainable recommendations.
最近の研究では，映画のジャンル，種類，俳優，監督などの知識ベースに基づいて，知識を考慮した説明可能な推薦を行うことが試みられている．
For example, Catherine et al. (2017) proposed explainable entity-based recommendation with knowledge graphs for movie recommendation.
例えば、Catherineら（2017）は、映画の推薦のために、知識グラフを用いた説明可能なエンティティベースレコメンデーションを提案した。
It provides explanations by reasoning over the knowledge graph entities about the movies.
これは，映画に関する知識グラフのエンティティを推論することで説明を提供するものである．
Wang et al. (2018a) proposed the ripple network model to propagate user preferences on knowledge graphs for recommendations.
Wangら（2018a）は、推薦のために知識グラフ上でユーザの嗜好を伝播させるリップルネットワークモデルを提案した。
It provides explanations based on knowledge paths from the user to the recommended movie, book, or news.
これは，ユーザから推薦された映画，書籍，ニュースまでの知識経路を基に説明を行うものである．

Zhao et al. (2019a) studied personalized reason generation for explainable song recommendation in conversational agents (e.g., Microsoft XiaoIce4 ).
Zhao ら（2019a）は、会話型エージェント（Microsoft XiaoIce4 など）における説明可能な楽曲推薦のためのパーソナライズされた理由生成について研究した。
The authors proposed a solution that generates a natural language explanation of the reason for recommending a song to a particular user, and showed that the generated explanations significantly outperform manually selected reasons in terms of click-through rate in large-scale online environments.
著者らは、特定のユーザーに曲を推薦する理由を自然言語で生成するソリューションを提案し、生成された説明は、大規模なオンライン環境において、クリックスルー率の面で手動で選択した理由を大幅に上回ることを示しました。
Davidson et al. (2010) introduced the YouTube Video Recommendation System, which leveraged association rule mining to find the related videos as explanations of the recommended video.
Davidsonら(2010)は、YouTube Video Recommendation Systemを紹介し、推奨されたビデオの説明として関連するビデオを見つけるために、アソシエーション・ルール・マイニングを活用した。
Online media frequently provide news article recommendations to users.
オンラインメディアでは，ユーザにニュース記事を推薦することが頻繁に行われている．
Recently, such recommendations have been integrated into independent news feeding applications on the phone, such as the Apple News.
最近では、このようなレコメンデーションは、Apple Newsなど、スマホの独立したニュース配信アプリケーションに統合されている。
Kraus (2016) studied how news feeds can be explained based on political topics.
Kraus (2016) は、政治的なトピックに基づいてニュースフィードをどのように説明できるかを研究した。

## 5.5. Other Explainable Recommendation Applications 5.5. その他の説明可能なレコメンデーションアプリケーション

Explainable recommendation is also essential to many other applications, such as academic recommendation, citation recommendation, legal recommendation, and healthcare recommendation.
また、学術推薦、引用推薦、法律推薦、医療推薦など、他の多くのアプリケーションにおいても、説明可能な推薦が不可欠である。
Though direct explainable recommendation work on these topics is still limited, researchers have begun to consider the explainability issues within these systems.
これらのトピックに関する直接的な説明可能な推薦の研究はまだ限られているが、研究者はこれらのシステム内の説明可能性の問題を検討し始めている。
For example, Gao et al. (2017) studied the explainability of text classification in online healthcare forums, where each sentence is classified into three types: medication, symptom, or background.
例えば、Gaoら（2017）は、オンラインヘルスケアフォーラムにおけるテキスト分類の説明可能性を研究し、各文章を薬、症状、背景の3種類に分類しています。
An interpretation method is developed, which explicitly extracts the decision rules to gain insights about the useful information in texts.
テキストに含まれる有用な情報についての洞察を得るために、決定ルールを明示的に抽出する解釈方法が開発されています。
Liu et al. (2018) further studied interpretable outlier detection for health monitoring.
Liuら（2018）はさらに、健康モニタリングのための解釈可能な外れ値検出を研究しました。
In healthcare practice, it is usually important for doctors and patients to understand why data-driven systems recommend a certain treatment, and thus, it is important to study the explainability of healthcare recommendation systems.
ヘルスケアの実践では、通常、医師や患者にとって、データ駆動型システムが特定の治療を推奨する理由を理解することが重要であり、したがって、ヘルスケア推奨システムの説明可能性を研究することが重要である。
It is also worth noting that explainability perspectives have also been integrated into other intelligent systems beyond recommendation, such as explainable search (Singh and Anand, 2019), question answering (Zhao et al., 2019b), and credibility analysis of news articles (Bountouridis et al., 2018).
また、説明可能な検索（Singh and Anand, 2019）、質問応答（Zhao et al., 2019b）、ニュース記事の信頼性分析（Bountouridis et al., 2018）など、推薦以外の他の知的システムにも説明可能性の観点が取り入れられていることは注目に値します。

## 5.6. Summary 5.6. まとめ

In this section, we introduced several applications of explainable recommendation to help readers understand how the key idea of explainability works in different recommendation scenarios.
このセクションでは、説明可能な推薦のいくつかの応用例を紹介し、説明可能性というキーアイデアがさまざまな推薦シナリオでどのように機能するかを読者に理解してもらうことにした。
In particular, we introduced explainable e-commerce, POI, social, and multimedia recommendations.
特に、電子商取引、POI、ソーシャル、マルチメディアの各分野における説明可能なレコメンデーションについて紹介した。
We also briefly touched some new explainable recommendation tasks such as explainable academic, educational, and healthcare recommendations, which have been attracting increasing attention recently.
また、最近注目されている説明可能な学術・教育・医療推薦などの新しい説明可能な推薦タスクについても簡単に触れた。

It is also beneficial to discuss the potential limitations of explainable recommendation.
また、説明可能なレコメンデーションの潜在的な限界について議論することも有益である。
Although explanations can be helpful to many recommendation scenarios, there could exist scenarios where explanations are not needed or could even hurt.
説明は多くのレコメンデーションシナリオに役立つが、説明が不要なシナリオや、逆に損をするシナリオも存在しうる。
These include time-critical cases where decisions should be made in real-time, and users are not expected to spend time evaluating the decisions.
例えば、リアルタイムで意思決定を行う必要があり、ユーザーが意思決定の評価に時間をかけることが想定されないタイムクリティカルなケースなどです。
For example, while driving on highways, users may want to know the correct exit directly without spending time listening to the explanations.
例えば、高速道路を運転中、ユーザーは説明を聞くのに時間をかけずに、正しい出口を直接知りたいと思うかもしれません。
Even more critical scenarios include emergency medical decisions or battlefield decisions, where spending time for evaluation may not be permitted.
さらに重要なシナリオとして、緊急医療判断や戦場での判断など、評価のための時間をかけることが許されない場合もある。
Depending on the scenario, explainable recommendation systems may need to avoid providing too much explanation, and avoid repeated explanations, explaining the obvious, or explaining in too many details, which may hurt rather than improve the user experience.
シナリオによっては、説明可能なレコメンデーションシステムは、説明のしすぎを避け、繰り返し説明したり、当たり前のことを説明したり、詳細に説明しすぎたりして、ユーザー体験を向上させるどころか、傷つけてしまうようなことは避ける必要がある。
The system also needs to be especially careful not to provide obviously misleading or even wrong explanations, because people may lose confidence in algorithms after seeing them trying to mistakenly convince others (Dietvorst et al., 2015).
また、明らかに誤解を招くような説明や、間違った説明をしないように特に注意する必要があります。人々は、誤って他人を説得しようとしているのを見て、アルゴリズムへの信頼を失う可能性があるからです（Dietvorst et al.、2015）。

# 6. Open Directions and New Perspectives 6. 開かれた方向性と新しい視点

We discuss some open research directions and new research perspectives of explainable recommendation in this section.
本節では、説明可能なレコメンデーションに関する研究の方向性と新たな研究視角について議論する。
We make discussion on four broad perspectives: methodology, evaluation, cognitive foundation, and broader impacts.
方法論、評価、認知的基盤、そしてより広範な影響という 4 つの広範な観点で議論を行う。

## 6.1. Methods and New Applications 6.1. メソッドと新しいアプリケーション

### 6.1.1. Explainable Deep Learning for Recommendation 6.1.1. レコメンデーションのための説明可能なディープラーニング

The research community has been developing explainable deep learning models for explainable recommendations.
研究コミュニティでは、説明可能なレコメンデーションのための説明可能な深層学習モデルの開発が進められています。
Current approaches focus on designing deep models to generate explanations accompanying the recommendation results.
現在のアプローチは、推薦結果に付随する説明を生成するためのディープモデルを設計することに焦点を当てている。
The explanations could come from attention weights over texts, images, or video frames.
説明は、テキスト、画像、またはビデオフレームに対する注目度から来る可能性がある。
However, the research of explainable deep learning is still in its initial stage, and there is still much to explore in the future (Gunning, 2017).
しかし、説明可能な深層学習の研究はまだ初期段階であり、今後探求すべきことはまだたくさんある（Gunning, 2017）。

Except for designing deep models for explainable recommendations, the explainability of the deep model itself also needs further research.
説明可能な推薦のための深層モデルの設計を除けば、深層モデル自体の説明可能性についてもさらなる研究が必要である。
In most cases, the recommendation and explanation models are still black boxes, and we do not fully understand how an item is recommended out of other alternatives.
多くの場合、推薦モデルや説明モデルはまだブラックボックスであり、あるアイテムが他の選択肢の中からどのように推薦されるのか、完全には理解されていない。
This is mostly because the hidden layers in most deep neural networks do not possess intuitive meanings.
これは、ほとんどのディープニューラルネットワークの隠れ層が直感的な意味を持っていないことが主な原因である。
As a result, an important task is to make the deep models explainable for recommendations.
そのため、推薦のためにディープモデルを説明可能にすることが重要な課題である。
This will benefit not only the personalized recommendation research, but also many other research areas such as computer vision and natural language processing, as well as their application in healthcare, education, chatbots, and autonomous systems, etc.
これは、パーソナライズド・レコメンデーション研究だけでなく、コンピュータビジョンや自然言語処理など他の多くの研究分野や、ヘルスケア、教育、チャットボット、自律システムなどへの応用にも役立つと思われます。

Recent advances in machine learning have shed light on this problem, for example, Koh and Liang (2017) provided a framework to analyze deep neural networks based on influence analyses, while Pei et al. (2017) proposed a white-box testing mechanism to help understand the nature of deep learning systems.
近年の機械学習の進歩によりこの問題に光が当てられ、例えばKoh and Liang（2017）は影響力分析に基づいて深層ニューラルネットワークを分析するフレームワークを提供し、Peiら（2017）は深層学習システムの性質を理解するためにホワイトボックステスト機構を提案しました。
Regarding explainable recommendation, this will help us to understand what are the meanings of each latent component in a neural network, and how they interact with each other to generate the final results.
説明可能なレコメンデーションについては、ニューラルネットワークの各潜在成分がどのような意味を持ち、それらがどのように相互作用して最終的な結果を生成しているのかを理解するのに役立つと思われます。

### 6.1.2. Knowledge-enhanced Explainable Recommendation 6.1.2. 知識で強化された説明可能なレコメンデーション

Most of the explainable recommendation research is based on unstructured data, such as texts or images.
説明可能な推薦の研究のほとんどは、テキストや画像などの非構造化データに基づくものである。
However, if the recommendation system possesses specific knowledge about the recommendation domain, it will help to generate more tailored recommendations and explanations.
しかし、推薦システムが推薦領域に関する特定の知識を有していれば、よりカスタマイズされた推薦や説明の生成に役立つ。
For example, with the knowledge graph about movies, actors, and directors, the system can explain to users precisely that “a movie is recommended because he has watched many movies starred by an actor”.
例えば、映画、俳優、監督に関する知識グラフがあれば、「ある俳優が主演した映画をたくさん見ているので、ある映画をおすすめします」とユーザに的確に説明することができる。
Such explanations usually have high fidelity scores.
このような説明は、通常、高い忠実度を持ちます。
Previous work based on this idea dates back to the content-based recommendation, which is effective, but lacks serendipity and requires extensive manual efforts to match the user interests with the content profiles.
この考え方に基づく従来の研究は、コンテンツに基づく推薦にまでさかのぼる。これは効果的ではあるが、セレンディピティに欠け、ユーザーの興味とコンテンツプロファイルをマッチングさせるために大規模な手作業を必要とする。

With the fast progress of (knowledge) graph embedding techniques, it has been possible for us to integrate the learning of graph embeddings and recommendation models for explainable recommendation, so that the system can make recommendations with specific domain knowledge, and tell the user why such items are recommended based on knowledge reasoning, similar to what humans do when asked to make recommendations.
(知識)グラフ埋め込み技術の急速な進歩により、グラフ埋め込みと推薦モデルの学習を統合して説明可能な推薦を行うことが可能となり、人間が推薦を求められたときに行うのと同様に、特定のドメイン知識を持った推薦を行い、知識推論に基づいてなぜその項目が推薦されるかをユーザに伝えることができるようになった。
It will also help to construct conversational recommendation systems, which communicate with users to provide explainable recommendations based on knowledge.
また、知識に基づいて説明可能な推薦を行うために、ユーザーとコミュニケーションをとる会話型推薦システムの構築にも役立つだろう。
Moreover, in a more general sense, this represents an important future direction for intelligent systems research, i.e., to integrate rational and empirical approaches for agent modeling.
さらに、より一般的な意味では、エージェントモデリングのための合理的アプローチと経験的アプローチを統合するという、知的システム研究の重要な将来の方向性を示すものである。

### 6.1.3. Multi-Modality and Heterogenous Information Modeling 6.1.3. マルチモダリティと異質な情報モデリング

Modern information retrieval and recommendation systems work on many heterogeneous multi-modal information sources.
現代の情報検索・推薦システムは、多くの異質なマルチモーダル情報源に対して動作する。
For example, web search engines have access to documents, images, videos, and audios as candidate search results; e-commerce recommendation system works on user numerical ratings, textual reviews, product images, demographic information and others for user personalization and recommendation; social networks leverage user social relations and contextual information such as time and location for search and recommendation.
例えば、ウェブ検索エンジンは文書、画像、動画、音声を検索結果の候補として利用し、電子商取引推薦システムはユーザの数値評価、テキストレビュー、商品画像、デモグラフィック情報などを利用してユーザの個人化と推薦を行い、ソーシャルネットワークはユーザの社会関係や時間、場所などの文脈情報を検索と推薦に利用する。

Current systems mostly leverage heterogeneous information sources to improve search and recommendation performance, while many research efforts are needed to use heterogeneous information for explainability.
現在のシステムでは、検索や推薦の性能を向上させるために異種情報源を活用することがほとんどであるが、説明可能性のために異種情報を活用するためには多くの研究努力が必要である。
These include a wide range of research tasks such as multi-modal explanations by aligning two or more different information sources, transfer learning over heterogeneous information sources for explainable recommendations, cross-domain explanation in information retrieval and recommendation systems, and how the different information modalities influence user receptiveness on the explanations.
例えば、2つ以上の異なる情報源を連携させたマルチモーダルな説明、説明可能な推薦のための異種情報源上での転移学習、情報検索・推薦システムにおけるクロスドメイン説明、異なる情報様式が説明に対するユーザの受容性にどのように影響するか、などの幅広い研究課題がある。

### 6.1.4. Context-aware Explanations 6.1.4. 文脈を考慮した説明

User preferences or item profiles may change along with context information such as time and location, and thus personalized recommendations could be context-aware (Adomavicius and Tuzhilin, 2011).
ユーザーの嗜好やアイテムのプロフィールは、時間や場所などのコンテキスト情報とともに変化する可能性があるため、パーソナライズされたレコメンデーションはコンテキストを意識したものとなりうる（Adomavicius and Tuzhilin, 2011）。
The same idea applies to explainable recommendations.
同じ考え方が説明可能なレコメンデーションにも適用される．
Because user preferences may change over context, the explanations could also be context-aware, so that recommendations can be explained in the most appropriate way.
ユーザーの好みは文脈によって変化するため，説明も文脈に応じたものとすることで，最適な方法でレコメンデーションを説明することができる．
Most of the current explainable recommendation models are static, i.e., users are profiled based on a training dataset, and explanations are generated accordingly, while context-aware explainable recommendation needs extensive exploration in the future.
現在の説明可能なレコメンデーションモデルの多くは、学習データに基づいてユーザーをプロファイリングし、それに応じて説明を生成する静的なモデルである。

### 6.1.5. Aggregation of Different Explanations 6.1.5. 異なる説明の集約

Different explainable recommendation models may generate different explanations, and the explanations may highly depend on the specific model.
説明可能なレコメンデーションモデルが異なると、異なる説明を生成する可能性があり、その説明は特定のモデルに大きく依存する場合がある。
As a result, we usually have to design different explainable models to generate different explanations for different purposes.
その結果、我々は通常、目的に応じて異なる説明を生成するために、異なる説明可能なモデルを設計しなければならない。
On one hand, researchers have shown that providing diversified explanations is beneficial to user satisfaction in recommender systems (Tsukuda and Goto, 2019).
一方では、研究者は、多様な説明を提供することが推薦システムにおけるユーザ満足度に有益であることを示している（Tsukuda and Goto, 2019）。
While on the other hand, different explanations may not be logically consistent in explaining one item, and according to cognitive science research, having a complete set of explanations may not be what we need in many cases (Miller, 2019).
一方で、異なる説明は1つの項目を説明する上で論理的に一貫していない可能性があり、認知科学の研究によれば、完全な説明のセットを持つことは多くの場合、必要なことではない可能性がある（Miller, 2019）。
When the system generates many candidate explanations for a search or recommendation result, a significant challenge is how to select the best combination of the explanations to display, and how to aggregate different explanations into a logically consistent unified explanation.
システムが検索や推薦の結果について多くの説明候補を生成する場合、表示する説明の最適な組み合わせをどのように選択するか、異なる説明をどのように論理的に一貫性のある統一的な説明に集約するかは重要な課題である。
Solving this problem may require extensive efforts to integrate statistical and logical reasoning approaches to machine learning, so that the decision-making system is equipped with the ability of logical inference to explain the results.
この問題を解決するには、統計的推論と論理的推論のアプローチを機械学習に統合し、意思決定システムが結果を説明するための論理的推論の能力を備えるようにするための広範な取り組みが必要かもしれない。

### 6.1.6. Explainable Recommendation as Reasoning 6.1.6. 推論としての説明可能なレコメンデーション

Early approaches to AI, such as Logical
ロジカルなど、初期のAIへのアプローチ

As a representative branch of AI research, the advancement of collaborative filtering for recommendation followed a similar path.
AI研究の代表的な一分野として、推薦のための協調フィルタリングの発展も同様の道をたどってきた。
Early approaches to CF adopted straightforward yet transparent methods, such as user-based (Resnick et al., 1994) or item-based (Sarwar et al., 2001) methods, which find similar users or items first, and then calculate the weighted average ratings for prediction.
初期の協調フィルタリングは、ユーザベース（Resnick et al., 1994）やアイテムベース（Sarwar et al., 2001）のように、類似ユーザやアイテムを最初に発見し、その加重平均評価を予測する、わかりやすく透明性の高い手法を採用していた。
Later approaches to CF, however, more and more advanced to less transparent “latent” machine learning approaches, beginning from shallow latent factor models such as matrix factorization to deep learning approaches.
しかし、その後のCFのアプローチは、行列分解などの浅い潜在因子モデルから深層学習アプローチに至るまで、より透明性の低い「潜在的」機械学習アプローチにどんどん進化している。
Though effective in ranking and rating prediction, the key philosophy of these approaches is to learn user
ランキングや視聴率予測に有効ではあるが、これらのアプローチの重要な思想は、ユーザー

### 6.1.7. NLP and Explainable Recommendation 6.1.7. NLPと説明可能なレコメンデーション

Most explainable recommendation models are designed to generate some predefined types of explanations, e.g., based on sentence templates, specific association rules, or word clouds.
説明可能な推薦モデルの多くは、文型、特定のアソシエーションルール、ワードクラウドなど、あらかじめ定義されたタイプの説明を生成するように設計されている。
A more natural explanation form could be free-text explanations based on natural language.
より自然な説明として、自然言語に基づくフリーテキストの説明も考えられる。

There has been some work trying to generate natural language explanations.
自然言語による説明を生成しようとする研究はいくつかある。
The basic idea is to train sentence generation models based on user reviews and generate “review-like” sentences as explanations, such as Li et al. (2017), Costa et al. (2018), Chen et al. (2019d), and Ni et al. (2019).
基本的な考え方は、Liら（2017）、Costaら（2018）、Chenら（2019d）、Niら（2019）など、ユーザーのレビューをもとに文章生成モデルを学習し、説明として「レビュー風」の文章を生成することである。
The research of generating natural language explanation is still in its early stage, and much needs to be done so that machines can explain themselves using natural language.
自然言語による説明を生成する研究はまだ初期段階であり、機械が自然言語を使って説明できるようにするためには多くのことが必要である。
For example, not all of the review contents are of explanation purpose, and it is challenging to cope with various noise for generating explanations.
例えば、レビュー内容の全てが説明目的ではなく、説明生成のための様々なノイズに対処することは困難である。
Since explanations should be personalized, it is important to adapt pre-trained language models such as BERT (Devlin et al., 2018) to personalized per-training models.
説明はパーソナライズされるべきなので、BERT (Devlin et al., 2018) などの事前学習済みの言語モデルをパーソナライズされたパーレーニングモデルに適応させることが重要である。
Explanations should also be generated beyond textual reviews, e.g., we can integrate visual images, knowledge graphs, sentiments, and other external information to generate more informed natural language explanations, such as explanation with specific sentiment orientations.
説明はまた、テキストレビューを超えて生成されるべきである、例えば、我々は、特定のセンチメントの方向性を持つ説明など、より情報に基づいた自然言語の説明を生成するために、視覚的な画像、知識グラフ、センチメント、および他の外部情報を統合することができます。
Natural language explanations are also crucial for explainable conversational systems, which we will discuss in the following subsections.
自然言語による説明は、説明可能な会話システムにとっても重要であり、これについては以下のサブセクションで説明する。

### 6.1.8. Answering the “Why” in Conversations 6.1.8. 会話の中で「なぜ」に答える

The research of recommendation system has extended itself to multiple perspectives, including what to recommend (user
推薦システムの研究は、何を推薦するのか（ユーザ

Based on different application scenarios, users can receive recommendation explanations either passively or actively.
レコメンデーションの説明には、受動的なものと能動的なものがある。
In conventional web-based systems such as online e-commerce, the explanations can be displayed together with the recommended item, so that the users passively receive the explanations for each recommendation.
eコマースのような従来のウェブベースのシステムでは、推薦された商品と一緒に説明が表示されるため、ユーザーは受動的に各推薦商品の説明を受け取ることができる。
In the emerging environment of conversational recommendation based on smart agent devices, users can ask “why-related” questions to actively seek for explanations when a recommendation is not intuitive.
一方、スマートエージェントによる会話型レコメンデーションでは、直感的でないレコメンデーションに対して、ユーザが「なぜ」と問いかけ、能動的に説明を求めることができる。
In this case, explainable recommendations will significantly increase the scope of queries that intelligent systems can process.
この場合、説明可能なレコメンデーションは、知的システムが処理できるクエリの範囲を大幅に拡大することになる。

## 6.2. Evaluation and User Behavior Analysis 6.2. 評価とユーザー行動分析

### 6.2.1. Evaluation of Explainable Recommendations 6.2.1. 説明可能な推奨事項の評価

Evaluation of explainable recommendation systems remains a significant problem.
説明可能なレコメンデーションシステムの評価は、依然として重要な問題である。
For recommendation performance, explainable recommendations can be easily evaluated based on traditional rating prediction or top-n ranking measures, while for explanation performance, a reliable protocol is to test explainable vs. non-explainable recommendations based on real-world user studies, such as A
推薦性能については、説明可能な推薦を従来の評価予測やトップNランキングの尺度に基づいて容易に評価することができる。一方、説明性能については、信頼できるプロトコルは、実際のユーザー調査に基づいて説明可能な推薦と説明不可能な推薦を比較するテストであり、例えば、A

Evaluation of the explanations is related to both user perspective and algorithm perspective.
説明文の評価は、ユーザの視点とアルゴリズムの視点の両方が関係する。
On user perspective, the evaluation should reflect how the explanations influence users, in terms of, e.g., persuasiveness, effectiveness, efficiency, transparency, trustworthiness, and user satisfaction.
ユーザー視点での評価は、説明がユーザーにどのような影響を与えるかを、説得力、有効性、効率性、透明性、信頼性、ユーザー満足度などの観点から反映させる必要がある。
On algorithm perspective, the evaluation should reflect to what degree the explanations reveal the real mechanism that generated the recommendations (sometimes called explanation fidelity).
アルゴリズムの観点からは、説明文がどの程度、推薦文を生成した実際のメカニズムを明らかにしているか（説明の忠実度ということもある）を評価する必要がある。
The evaluation may also be related to the form of explanations, e.g., visual and textual explanations could be evaluated in different ways.
また、視覚的な説明と文字による説明では評価が異なるなど、説明の形態に関連した評価も考えられる。
Developing reliable and readily usable evaluation measures for different evaluation perspectives will save many efforts for offline evaluation of explainable recommendation systems.
このように、説明可能な推薦システムのオフライン評価において、信頼性が高く、容易に利用可能な評価指標を開発することは、多くの労力を節約することになる。

### 6.2.2. User Behavior Perspectives 6.2.2. ユーザー行動の視点

Though early research explored a lot about how users interact with explanations (Herlocker et al., 2000), many recent research on explainable recommendation is mostly model-driven, which designs new explainable models to generate recommendations and explanations.
初期の研究では、ユーザが説明とどのように相互作用するかについて多くの研究がなされたが (Herlocker et al., 2000)、最近の説明可能な推薦に関する研究の多くは、新しい説明可能なモデルを設計して推薦と説明を生成するモデル駆動型のものである。
However, since recommender systems are inherently human-computer interaction systems, it is also essential to study explainable recommendations from user behavior perspectives, where the “user” could either be recommender system designers or normal users of the system.
しかし、推薦システムは本質的に人間とコンピュータのインタラクションシステムであるため、「ユーザ」が推薦システムの設計者であったり、システムの一般ユーザであったりする、ユーザ行動の観点から説明可能な推薦を研究することも必要不可欠である。
There exist a broad scope of problems to explore, including but not limited to how users interact with explanations, and the user receptiveness on different types of explanations.
ユーザが説明とどのように関わるか、異なるタイプの説明に対するユーザの受容性など、探求すべき問題は広範に存在する。
Research on user behavior perspectives for explainable recommendation will also benefit the evaluation of explainable recommendation systems.
説明可能な推薦を行うためのユーザ行動の視点に関する研究は、説明可能な推薦システムの評価にも役立つと思われる。

## 6.3. Explanation for Broader Impacts 6.3. 広範な影響についての説明

Existing explainable recommendations mostly focus on generating explanations to persuade users to accept the explanations (Nanou et al., 2010).
既存の説明可能なレコメンデーションは、そのほとんどがユーザーを説得するための説明を生成することに焦点を当てている（Nanou et al.、2010）。
However, explanations could have broader impacts beyond persuasiveness.
しかし、説明は説得力だけでなく、より広範な影響を与える可能性がある。
It is worthwhile to explore how explanations can help to improve the trustworthiness (Cramer et al., 2008), efficiency (Tintarev and Masthoff, 2011), diversity (Yu et al., 2009), satisfaction (Bilgic and Mooney, 2005), and scrutability of the system (Balog et al., 2019; Knijnenburg et al., 2012).
説明が、信頼性（Cramer et al., 2008）、効率性（Tintarev and Masthoff, 2011）、多様性（Yu et al., 2009）、満足度（Bilgic and Mooney, 2005）、システムの精査性（Balog et al., 2019; Knijnenburg et al., 2012）を改善するために役立つことを探る価値がある。
For example, by letting the user know why not to buy a certain product, the system can help to save time for the users and to win the user’s trust in the system (Zhang et al., 2014a).
例えば、ある商品を買わない理由をユーザーに知らせることで、ユーザーの時間を節約し、ユーザーのシステムに対する信頼を獲得することができる（Zhang et al.）

Another important problem is the relationship between explainability and fairness.
もう一つの重要な問題は、説明可能性と公正さの関係である。
Though researchers have shown that transparency helps to increase the fairness in economic (Cowgill and Tucker, 2019), political (Fine Licht, 2014) and legal (Burke and Leben, 2007) systems, we are yet to see if and how transparency and fairness relate with each other in information systems.
経済（Cowgill and Tucker, 2019）、政治（Fine Licht, 2014）、法律（Burke and Leben, 2007）システムにおいて透明性が公平性を高めるのに役立つことは研究者によって示されているものの、情報システムにおいて透明性と公平性が互いに関連するか、どのように関連するかはまだ確認されていない。
One example is that if the system inevitably has to output unfair rankings for a user, explaining to the user why this happens could help to gain user’s understanding.
一例として、システムがどうしてもユーザーにとって不公平なランキングを出力しなければならない場合、なぜそうなるのかをユーザーに説明することで、ユーザーの理解を得ることができるかもしれません。

## 6.4. Cognitive Science Foundations 6.4. 認知科学の基礎

There are two research philosophies towards explainable recommendation – and more broadly explainable decision making or explainable AI (Lipton, 2018).
説明可能なレコメンデーション、より広くは説明可能な意思決定や説明可能なAIに向けた研究哲学は2つある（Lipton, 2018）。
One is to design transparent
1 つは、透明な

It is interesting to see that both research philosophies have their roots in human cognitive science (Miller, 2019).
どちらの研究哲学も、そのルーツが人間の認知科学にあることは興味深い（Miller, 2019）。
Sometimes, human-beings make decisions based on careful reasoning, and they can clearly explain how a decision is made by showing the reasoning process step by step.
人間は時に、慎重な推論に基づいて意思決定を行い、その推論過程を段階的に示すことで、意思決定がどのように行われたかを明確に説明することができます。
Other times, people make intuition decisions first and then “seek” an explanation for the decision, which belongs to the post-hoc explanation approach.
また、人間はまず直感的に判断し、その後に説明を「求める」こともあり、これは事後的説明アプローチに属します。
It is challenging to decide which research philosophy towards explainable recommendation – and explainable AI in a broader sense – is the correct approach (or both).
説明可能な推薦、そして広い意味での説明可能なAIに向けた研究理念は、どちらが正しいアプローチなのか（あるいは両方なのか）、判断に迷うところです。
Answering this question requires significant breakthroughs in human cognitive science as well as our understanding of how the human brain works.
この問いに答えるには、人間の認知科学と、人間の脳の働きに関する理解において、大きなブレークスルーが必要である。

# 7. Conclusions 7. 結論

Early recommendation models – such as user
初期のレコメンデーションモデル（ユーザーなど

The lack of explainability mainly exists in terms of two perspectives:
説明可能性の欠如は、主に以下の2つの観点から存在する。

1. the outputs of the recommendation system (i.e., recommendation results) are hardly explainable to system users, and 2) the mechanism of the recommendation model (i.e., recommendation algorithm) is hardly explainable to system designers.
   1）推薦システムの出力（推薦結果）が利用者に説明しにくい、2）推薦モデルの仕組み（推薦アルゴリズム）がシステム設計者に説明しにくい、である。
   This lack of explainability for recommendation algorithms leads to many problems: without letting the users know why specific results are provided, the system may be less effective in persuading the users to accept the results, which may further decrease the system’s trustworthiness.
   このような推薦アルゴリズムの説明可能性の欠如は、なぜ特定の結果が提供されるのかをユーザーに知らせなければ、その結果をユーザーが受け入れるための説得力が低下し、システムの信頼性をさらに低下させる可能性があるなど、多くの問題を引き起こす。
   More importantly, many recommendation systems nowadays are not only useful for information seeking – by providing supportive information and evidence, they are also crucial for complicated decision making.
   さらに重要なことは、最近の多くの推薦システムは、情報探索に役立つだけでなく、裏付けとなる情報や証拠を提供することで、複雑な意思決定にも欠かせない存在になっていることです。
   For example, medical workers may need comprehensive healthcare document recommendations or retrieval to make medical diagnoses.
   例えば、医療従事者は、医療診断を行うために、包括的な医療文書の推薦や検索を必要とする場合がある。
   In these decision making tasks, the explainability of the results and systems is extremely important, so that system users can understand why a particular result is provided, and how to leverage the result to take actions.
   このような意思決定において、なぜそのような結果が得られたのか、また、その結果をどのように活用すればよいのかをシステム利用者が理解できるように、結果やシステムの説明可能性が非常に重要である。

Recently, deep neural models have been used in many information retrieval and recommendation systems.
近年、多くの情報検索・推薦システムでディープニューラルモデルが利用されています。
The complexity and inexplainability of many neural models have further highlighted the importance of explainable recommendation and search, and there is a wide range of research topics for the community to address in the coming years.
多くのニューラルモデルが複雑で説明不可能であることから、説明可能な推薦・検索の重要性がさらに強調されており、今後、コミュニティが取り組むべき研究テーマは多岐にわたります。

In this survey, we provided a brief history of explainable recommendation research ever since the early stage of recommendation systems, towards the very recent research achievements.
本サーベイでは、説明可能な推薦システムの初期段階から最近の研究成果まで、説明可能な推薦研究の歴史を簡単に紹介した。
We introduced some different types of explanations, including user
また、説明文の種類として、ユーザ名、住所、氏名、電話番号、メールアドレスなどを紹介した。

In a broader sense, researchers in the broader AI community have also realized the importance of Explainable AI, which aims to address a wide range of AI explainability problems in deep learning, computer vision, autonomous driving systems, and natural language processing tasks.
広い意味でのAIコミュニティの研究者も、深層学習、コンピュータビジョン、自律走行システム、自然言語処理タスクなど、AIの説明可能性の問題に幅広く対応することを目指す「説明可能なAI」の重要性に気づいています。
As an essential branch of AI research, this highlights the importance of the IR
AI研究の本質的な一分野として、これはIRの重要性を浮き彫りにしています。
