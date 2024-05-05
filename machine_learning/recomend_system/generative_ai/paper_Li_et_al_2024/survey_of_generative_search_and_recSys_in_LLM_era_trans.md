## 0.1. refs: refs：

- https://arxiv.org/abs/2404.16924 https://arxiv.org/abs/2404.16924

## 0.2. title タイトル

A Survey of Generative Search and Recommendation in the Era of Large Language Models
大規模言語モデル時代の生成的検索と推薦のサーベイ

## 0.3. abstract 抄録

With the information explosion on the Web, search and recommendation are foundational infrastructures to satisfying users' information needs.
**ウェブ上の情報爆発に伴い、検索とレコメンデーションはユーザの情報ニーズを満たすための基盤インフラ**となっている。
As the two sides of the same coin, both revolve around the same core research problem, matching queries with documents or users with items.
同じコインの表と裏のように、**どちらもクエリとドキュメント、あるいはユーザとアイテムのマッチングという同じ核となる研究問題**を中心に展開している。
In the recent few decades, search and recommendation have experienced synchronous technological paradigm shifts, including machine learning-based and deep learning-based paradigms.
ここ数十年、検索とレコメンデーションは、機械学習ベースやディープラーニングベースのパラダイムを含む、同期的な技術的パラダイムシフトを経験してきた。(検索と推薦が同期的に発展してきたってこと...?)
Recently, the superintelligent generative large language models have sparked a new paradigm in search and recommendation, i.e., generative search (retrieval) and recommendation, which aims to address the matching problem in a generative manner.
近年、超知的な生成的大規模言語モデルによって、検索と推薦における新しいパラダイム、すなわち、**生成的にマッチング問題に取り組むことを目的としたgenerative search (retrieval) and recommendation**が生まれた。
In this paper, we provide a comprehensive survey of the emerging paradigm in information systems and summarize the developments in generative search and recommendation from a unified perspective.
本稿では、**information systems(情報システム)における新たなパラダイム**の包括的なサーベイを提供し、統一的な観点から生成的検索と推薦の発展を要約する。(情報検索・推薦システムにおける新たなparadigm、なるほど...!:thinking_face:)
Rather than simply categorizing existing works, we abstract a unified framework for the generative paradigm and break down the existing works into different stages within this framework to highlight the strengths and weaknesses.
既存の作品を単純に分類するのではなく、生成パラダイムの統一されたフレームワークを抽象化し、そのフレームワークの中で既存の作品をさまざまな段階に分解することで、**長所と短所**を浮き彫りにする。
And then, we distinguish generative search and recommendation with their unique challenges, identify open problems and future directions, and envision the next information-seeking paradigm.
そして、生成的検索とレコメンデーションをそれぞれのユニークな課題とともに区別し、未解決の問題と将来の方向性を明らかにし、次の情報検索のパラダイムを構想する。

# 1. Introduction はじめに

With the information explosion on the Web, a fundamental problem in information science gains increasing significance: sifting relevant information from vast pools to meet user needs.
ウェブにおける情報の爆発的な増加に伴い、情報科学における基本的な問題がますます重要になってきている：**膨大な情報の中から関連する情報を選別し、ユーザのニーズに応えること**。
Nowadays, two information access modes — search and recommendation — serve as foundational infrastructures for information delivery.
今日では、**検索と推薦という2つのinformation access modes**が、情報提供の基盤インフラとして機能している。
The objective of search is to retrieve a list of documents (e.g., Web documents, Twitter posts, and answers) given the user’s explicit query [57].
検索の目的は、ユーザの明示的なクエリ[57]から、文書（ウェブ文書、ツイッターの投稿、回答など）のリストを検索することである。
By contrast, recommendation systems aim to recommend the items (e.g., E-commerce products, micro-videos, and news) by implicitly inferring user interest from the user’s profile and historical interactions [1].
これとは対照的に、推薦システムは、ユーザのプロフィールと過去のインタラクションからユーザの興味を暗黙的に推測し、アイテム（電子商取引製品、マイクロビデオ、ニュースなど）を推薦することを目指している[1]。
Currently, search and recommendation systems are extensively employed across diverse scenarios and domains, including E-commerce, social media, healthcare, and education.
現在、検索・推薦システムは、電子商取引、ソーシャルメディア、医療、教育など、さまざまなシナリオやドメインで広く利用されている。

Search and recommendation are the two sides of the same coin [6].
検索とレコメンデーションは同じコインの裏表である[6]。
Search is users’ active information retrieval with explicit queries while recommendation is passive information filtering for users.
検索とは、ユーザが明示的なクエリを使って情報を取得する**能動的な情報検索**であり、推薦は**ユーザのための受動的な情報フィルタリング**である。(ふむふむ...!:thinking_face:)
Despite the distinct objectives, search and recommendation can be unified as the “matching” problem from a technical perspective [32].
**目的が異なるにもかかわらず、検索と推薦は技術的な観点から「マッチング」問題として統一することができる**[32]。
Search can be formulated as a matching between queries and documents, and recommendation can be considered a matching between users and items.
検索はクエリと文書のマッチングとして定式化することができ、推薦はユーザとアイテムのマッチングと考えることができる。
The common matching property has spurred synchronous technological paradigm shifts in both search and recommendation systems.
共通のマッチング特性は、検索システムと推薦システムの両方において、同期的な技術的パラダイムシフトに拍車をかけた。(なるほど、目的は違うけど両方ともマッチング問題とみなせるから、同期的に成長できたってことね:thinking_face:)
Specifically,
具体的には

- Machine learning-based search and recommendation.
  機械学習ベースの検索と推薦。
  Related works, generalized “learning to match” [156], learn a matching function using machine learning techniques (e.g., learning to ranks [65, 89] and Matrix Factorization [61]) to estimate the relevance scores on query-document pairs or user-item pairs.
  関連作品として、一般化された“learning to match (マッチングのための学習?)”[156]は、機械学習技術（例えば、ランク付け学習[65, 89]や行列因数分解[61]など）を用いてマッチング関数を学習し、クエリとドキュメントのペアやユーザとアイテムのペアの関連性スコアを推定する。

- Deep learning-based search and recommendation.
  ディープラーニングに基づく検索と推薦。
  With the significant advancements in various neural networks such as CNN [59], RNN [41], GNN [118], and Transformer [138], search and recommendation have transitioned into the deep learningbased paradigm.
  CNN[59]、RNN[41]、GNN[118]、Transformer[138]など、様々なニューラルネットワークの著しい進歩により、検索と推薦がディープラーニングベースのパラダイムに移行している。
  This paradigm leverages the powerful representation ability of deep learning-based methods to encode inputs (i.e., queries, documents, users, and items) into dense vectors in a latent space [55] and learn the non-linear matching functions.
  このパラダイムは、入力(i.e. クエリ、文書、ユーザ、アイテム)を**潜在空間の密なベクトルに符号化[55]**し、非線形のマッチング関数を学習するために、ディープラーニングベースの方法の強力な表現能力を活用している。

- Generative search and recommendation.
  生成的検索と推薦。
  With the recent surge of generative large language models (LLMs), a new paradigm emerges in search and recommendation: generative search (retrieval)1 and recommendation.
  近年の生成的大規模言語モデル(LLM)の急増に伴い、検索と推薦に新しいパラダイムが出現している： 生成的検索&推薦である。
  Distinguished from previous discriminative matching paradigms, generative search and recommendation aim to directly generate the target document or item to satisfy users’ information needs.
  **これまでの識別的マッチングパラダイムとは異なり、生成的検索&推薦は、ユーザの情報ニーズを満たすために、直接的にターゲットの文書やアイテムを生成することを目指している**。

Embracing generative search and recommendation brings new benefits and opportunities for the field of search and recommendation.
生成的検索&推薦を受け入れることで、検索と推薦の分野に新たな利点と機会がもたらされる。
In particular, 1) LLMs inherently possess formidable capabilities, such as vast knowledge, semantic understanding, interactive skills, and instruction following.
特に、第一に、LLMsは、広範な知識、意味理解、対話スキル、指示に従う能力など、強力な能力を持っている。
These inherent abilities can be transferred or directly applied to search and recommendation, thereby enhancing information retrieval tasks.
これらの固有の能力は、検索と推薦に転送されるか、直接適用されることで、情報検索タスクが向上する。
2)The tremendous success of LLMs stems from their generative learning.
第二に、LLMsの驚異的な成功は、その生成的学習に由来している。
A profound consideration to apply generative learning to search and recommendation, fundamentally revolutionizing the methods of information retrieval rather than only utilization of LLMs.
LLMsを単に利用するのではなく、情報検索の方法を根本的に革新するために、生成的学習を検索と推薦に適用することを深く考慮する。
3)LLMs-based generative AI applications, such as ChatGPT, are gradually becoming a new gateway for users to access Web content.
第三に、ChatGPTなどのLLMsベースの生成的AIアプリケーションは、徐々にユーザがウェブコンテンツにアクセスするための新しいゲートウェイとなっている。(gatewayってinterface的な意味合いでOK...?:thinking)
Developing generative search and recommendation could be better integrated into these generative AI applications.
生成的検索&推薦の開発は、これらの生成的AIアプリケーションによりよく統合されるかもしれない。

<!-- ここまで読んだ! -->

In this survey, we aim to provide a comprehensive review of generative search and recommendation from a technical perspective.
このサーベイでは、技術的な観点から生成的検索&推薦の包括的なレビューを提供することを目的とする。
We will not simply list and classify the current works, but instead abstract a unified framework for generative search and recommendation.
我々は、単に現在の作品を列挙し分類するのではなく、生成的検索&推薦のための統一されたフレームワークを抽象化する。
Within the unified framework, we highlight the objectives of each stage and categorize existing works into different stages from a technical viewpoint.
統一されたフレームワークの中で、各ステージの目的を強調し、技術的な観点から既存の作品を異なるステージに分類する。
From the unified perspective, we could better highlight their commonalities and present their developments.
統一された視点から、それぞれの共通点を浮き彫りにし、その発展を示すことができるだろう。
In addition, we will delve into deeper discussions, including contrasting generative search and recommendation, identifying open problems of the generative paradigm, and envisioning future information-seeking paradigms.
さらに、生成的検索&推薦を対比し、生成的パラダイムの未解決の問題を特定し、将来のinformation-seeking (=情報を探し求める?) パラダイムを構想するなど、より深い議論に入る。

There are several key points that set our survey apart from existing ones.
この調査には、既存の調査とは異なるいくつかの重要なポイントがある。
First and most important, we are the first to summarize and analyze the developments in generation search.
まず、最も重要なことは、私たちが初めて生成的検索の発展を要約し分析していることである。
Second, compared with existing generation recommendation surveys [25, 81, 139, 152], we focus on the fundamental generative paradigms for recommendation rather than incorporating LLM-enhanced discriminative methods.
第二に、既存の世代推薦の調査[25, 81, 139, 152]と比較して、**私たちはLLMを強化した識別的な方法を取り入れるのではなく、推薦のための基本的な生成的パラダイムに焦点を当てている**。
Besides, we examine existing works from a technical perspective, using an abstract framework to categorize generation recommendation works into different stages.
さらに、世代推薦作品を異なる段階に分類する抽象的な枠組みを用いて、技術的な観点から既存の作品を検証する。
Third, we highlight the close relationship between generative search and generation recommendation, where many works in the two areas mutually inform and promote each other.
第三に、生成的検索と生成的推薦の間の密接な関係を強調し、両分野の多くの作品が互いに情報を提供し合い、促進し合っている。
By taking a unified view and comparing the respective developments, we are able to identify potential research directions.
統一的な視野に立ち、それぞれの発展を比較することで、潜在的な研究の方向性を見出すことができる。

The survey is structured as follows: Chapter 2 summarizes the previous paradigms in search and recommendation.
本調査の構成は以下の通りである： 第2章では、検索と推薦における以前のパラダイムを要約する。(いいね!)
Chapter 3 provides an overview of the generative paradigm for search and recommendation.
第3章では、検索と推薦のための生成的パラダイムについて概観する。
In Chapters 4 and 5, we delve into the specific details of the generative paradigm in search and recommendation, respectively.
第4章と第5章では、それぞれ検索と推薦における生成パラダイムの具体的な詳細について掘り下げる。
Chapter 6 focuses on deep discussions, including the comparison of generative search and recommendation, open problems, and the next information-seeking paradigm.
第6章では、生成的検索と推薦の比較、未解決の問題、次の情報検索パラダイムなど、深い議論に焦点を当てる。
Finally, in Chapter 7, we give a conclusion of this survey.
最後に第7章で、この調査の結論を述べる。

<!-- ここまで読んだ! -->

# 2. Traditional Paradigms 伝統的パラダイム

## 2.1. Machine Learning based Search and Recommendation 機械学習に基づく検索と推薦

### Machine learning-based search.

機械学習ベースの検索。
In the era of machine learning, the core problem for search is to learn an effective function to predict the relevance scores between queries and documents.
機械学習の時代において、検索の核となる問題は、クエリと文書の間の関連性スコアを予測するための効果的な関数を学習することである。(効果的な関数って、目的関数? もしくは教師ありモデル自体??)
A series of classical works, such as Regularized Matching in Latent Space (RMLS) [153] and Supervised Semantic Indexing (SSI) [2, 3], explored mapping functions to transform features from queries and documents into a “latent space”.
正則化潜在空間マッチング（RMLS）[153]や教師ありセマンティックインデックス（SSI）[2, 3]などの一連の古典的な研究は、クエリと文書からの特徴を「潜在空間」に変換するマッピング関数を探求した。(特徴量を埋め込みベクトルにmappingする関数??)
The series of “learning to rank” algorithms [65, 89] were also proposed to develop effective rank losses for machine learning based search methods:
機械学習ベースの検索手法のための効果的なランク損失を開発するために、 **「ランク付け学習」アルゴリズムの一連の提案**も行われた (こレラの提案って、基本的にはモデルアーキテクチャではなく、目的関数やサンプリング方法の提案、という印象...!:thinking:):
the pointwise approaches [19, 102, 119] transform ranking into regression or classification on single documents; the pairwise approaches [10, 107, 135] regard the ranking into classification on the pairs of documents; the listwise approaches [12, 30, 106, 146, 155] aim to model the ranking problem in a straightforward fashion and overcome the drawbacks of the aforementioned two approaches by tackling the ranking problem directly.
ポイントワイズアプロー[19, 102, 119]は、ランキングを単一のドキュメントに対する回帰または分類に変換する; ペアワイズアプローチ[10, 107, 135]は、ランキングをドキュメントのペアに対する分類に変換する; リストワイズアプローチ[12, 30, 106, 146, 155]は、ランキング問題を直接的な方法でモデル化し、ランキング問題に直接取り組むことで、前述の2つのアプローチの欠点を克服することを目指している。

<!-- ここまで読んだ! -->

### Machine learning-based recommendation.

機械学習ベースの推薦。
In the context of recommender systems, the user-item matching typically leverages Collaborative Filtering (CF), which assumes users with similar interactions (e.g., ratings or clicks) share similar preferences on items [39].
レコメンダーシステムの文脈では、ユーザとアイテムのマッチングは、通常、協調フィルタリング(CF)を活用している。**CFは、類似したインタラクション（例：評価やクリック）を持つユーザは、アイテムに対して類似した嗜好を持つと仮定**している。(CFを説明する際にわかりやすそう...!:thinking:)
To achieve CF, early effort has been made to develop memory-based methods, which predict the user interactions by memorizing similar user’s or item’s ratings [9, 40, 84, 117].
CFを実現するために、類似のユーザやアイテムの評価を記憶することで、ユーザーのインタラクションを予測する **memory-based な方法**が初期に開発された[9, 40, 84, 117]。 (item-kNNとかはmemory-basedな手法に含まれる...?:thinking:)
Later on, popularized by the Netflix Prize, Matrix Factorization (MF) [116] has emerged as one of the most representative CF approaches.
その後、ネットフリックス賞によって人気を博したMatrix Factorization (MF) [116]は、最も代表的なCFアプローチの1つとして登場した。
MF decomposes user-item interactions into latent factors for users and items in a latent space.
MFは、ユーザとアイテムの相互作用を、潜在空間におけるユーザとアイテムのlatent factorsに分解する。(=latent factor vectors...!:thinking:)
It then predicts user-item interactions by matching these latent factors through inner product computations.
そして、内積計算によってこれらのlatent factorsをマッチングし、ユーザとアイテムの相互作用を予測する。
Following MF, other notable methods have been proposed that also perform matching in the latent space, such as BMF [58] and FISM [53].
MFに続いて、BMF[58]やFISM[53]など、潜在空間でもマッチングを行う注目すべき手法が提案されている。
In addition to the CF-based methods, an orthogonal line of research focuses on content-based techniques, aiming to encode user/item features for user-item matching.
CFベースの手法に加えて、**ユーザとアイテムの特徴をencodeしてユーザとアイテムのマッチングを行うコンテンツベースの技術**に焦点を当てた、直交する研究ラインもある。(ここで"直交する研究ライン"って、異なるアプローチや視点からの研究、みたいな意味合いの比喩表現っぽい...!!:thinking:)
Factorization Machine [115] is a prominent content-based method that represents user and item features as latent factors and models their high-order interactions to match between users and items.
因数分解マシン[115]は、ユーザとアイテムの特徴をlatent factorsとして表現し、ユーザとアイテムの間のマッチングを行うために、その高次の相互作用をモデル化する突出したコンテンツベースの手法である。(あ、factorization machineはcontent-basedな手法に分類されるのか...! ハイブリッド的なアプローチとみなしていたけど...!:thinking:)

<!-- ここまで読んだ! -->

## 2.2. Deep Learning based Search and Recommendation ディープラーニングに基づく検索と推薦

### Deep learning-based Search. ディープラーニングに基づく検索。

Deep learning-based search mainly relies on various neural architectures to represent queries and documents effectively.
ディープラーニングに基づく検索は、主にクエリと文書を効果的に表現するために、さまざまなニューラルアーキテクチャに依存している。
Feedforward neural networks are the first used to create semantic representations of queries and documents.
フィードフォワード・ニューラル・ネットワークは、クエリや文書の意味的表現を作成するために最初に使用された。
Deep Structured Semantic Models were proposed to represent queries and documents with deep neural networks [49].
Deep Structured Semantic Modelsは、ディープニューラルネットワークを使って**クエリとドキュメントを表現**するために提案された[49]。(この場合の成果物はクエリとドキュメントのsemanticな埋め込み表現になるっぽい...???:thinking:)
The popular Convolutional Neural Networks are also explored for the application in capturing semantic embeddings [44, 48, 121, 123].
一般的な畳み込みニューラルネットワークも、**semantic埋め込みを捕捉するための応用**が検討されている[44, 48, 121, 123]。
Given the fact that both queries and documents are sequential texts, it is natural to apply Recurrent Neural Networks to represent the queries and documents [103].
クエリも文書もシーケンシャルなテキストであるという事実を考えると、クエリと文書を表現するために Recurrent Neural Networks (RNN) を適用するのは自然である[103]。
Later, with the rise of the Transformer architecture [138] and pretrained BERT model [26], the Bert-based dense retrievers show advanced performance in large-scale scenarios [55, 110].
その後、Transformerアーキテクチャ[138]と事前訓練されたBERTモデル[26]の台頭により、**Bertベースの密な検索器は、大規模なシナリオで高度な性能を示すようになった**[55, 110]。(情報検索の歴史はNLPの歴史、みたいなイメージ...!:thinking:)

<!-- ここまで読んだ! -->

### Deep learning-based recommendation. ディープラーニングに基づく推薦

As deep neural networks have demonstrated exceptional learning capabilities across various domains, there emerges a trend in leveraging deep learning methodologies to tackle complex interaction patterns for user-item matching in recommendation systems [17, 54].
ディープ・ニューラル・ネットワークが様々な領域で卓越した学習能力を発揮していることから、推薦システムにおけるユーザとアイテムのマッチングのための複雑なインタラクション・パターンに取り組むために、ディープ・ラーニングの方法論を活用する傾向が現れている[17, 54]。
Deep learning-based user-item matching can be broadly classified into two research directions.
**ディープラーニングに基づくユーザとアイテムのマッチングは、大きく2つの研究方向に分類できる**。

One research line focuses on matching function learning, which utilizes deep learning techniques to learn intricate user-item matching function [170].
一つの研究ラインは、ユーザーとアイテムの複雑なマッチング関数を学習するために深層学習技術を利用するマッチング関数学習に焦点を当てている[170]。
Notably, Neural Collaborative Filtering (NCF) [39] leverages Multi-Layer Perceptrons (MLP) to achieve expressive and complicated matching functions.
特に、ニューラル協調フィルタリング（NCF）[39]は、多層パーセプトロン（MLP）を活用して、表現力豊かで複雑なマッチング関数を実現している。
This approach effectively models noisy implicit feedback data and enhances the recommendation performance.
このアプローチは、ノイズの多い暗黙のフィードバックデータを効果的にモデル化し、推薦性能を向上させる。
(sequential recommendationも、どちらかというとこっちの研究ラインに含まれそう...! 色んなモデルアーキテクチャでマッチング関数の改良を頑張ってるイメージ...!:thinking:)
(あ、マッチング関数って、DNNを使ってscore prediction module周りを頑張ってるってことかも...!:thinking:)

Another line of work lies in representation learning [158], which harnesses neural networks to transform user and item features into latent space conducive to matching.
**別の研究分野は representation learning(表現学習)**[158]にあり、これはニューラルネットワークを利用して、**ユーザとアイテムの特徴をマッチングに適した潜在空間に変換する**。(うんうん、two-tower architectureとかもこっちの研究ラインに含まれそう...!:thinking:)
For instance, Bert4Rec [124] employs deep bidirectional self-attention mechanisms to transform user’s historical sequences into latent space for sequential recommendation tasks.
例えば、Bert4Rec [124]は、sequential recommendationタスクのために、ユーザの歴史的なシーケンスを潜在空間に変換するために、深い双方向セルフアテンションメカニズムを利用している。(そうか、BERT4Recのscore prediction moduleは内積だっけ...!まあ内積じゃないにしろ、この研究ラインはユーザモデリングとアイテムモデリングに焦点を当ててるってことか...!:thinking:)
Caser [130] proposes a convolutional sequence model, which leverages both horizontal and vertical convolutional filters to identify complex historical interaction sequences.
Caser [130]は、複雑な歴史的interactionシーケンスを特定するために、水平と垂直の畳み込みフィルタを両方活用する畳み込みシーケンスモデルを提案している。(attention系じゃなくCNN系の手法か)
Subsequently, motivated by the graphical structure inherent in user-item interactions, researchers have explored the application of graph neural networks for recommendation tasks.
その後、**ユーザとアイテムのインタラクションに内在するグラフィカルな構造に動機づけられ**、研究者は推薦タスクへのグラフ・ニューラル・ネットワークの応用を模索してきた。(ほうほう...! アイテム表現にentityのknowledge graph使うやつしか認識してないけど、**interaction graph使うver.**もあるか...!:thinking:)
This research direction has enabled the utilization of high-order neighbor information to enhance the representation of users and items for the user-item matching, as exemplified by NGCF [145] and LightGCN [38].
この研究の方向性は、NGCF [145]やLightGCN [38]に代表されるように、ユーザとアイテムの表現を強化するために高次の隣接情報を利用することを可能にしている。

<!-- ここまで読んだ! -->

# 3. Generative Paradigm for Search and Recommendation 検索と推薦のための生成パラダイム

In this section, we first clarify the scope of generative search and recommendation, including comparison with previous paradigms and comparison with other LLM-based methods.
本節では、まず、従来のパラダイムとの比較や他のLLMベースの手法との比較を含め、生成的検索と推薦の範囲を明らかにする。
And then we abstract a unified framework for generative search and recommendation.
そして、生成的検索と推薦のための統一されたフレームワークを抽象化する。

## 3.1. Scope Clarification スコープの明確化

Comparison with previous paradigms.
従来のパラダイムとの比較。
As depicted in Figure 1, we present a summary of the three distinct paradigms in search and recommendation.
図1に示すように、検索と推薦における3つの異なるパラダイムの概要を示す。
Each paradigm employs different techniques to achieve the same goal of providing relevant documents/items for a given query/user.
それぞれのパラダイムは、与えられたクエリ／ユーザーに対して関連する文書／アイテムを提供するという同じ目標を達成するために、異なる技術を採用している。
The machine learning and deep learning paradigms approach the search/recommendation task as a discriminative problem, focusing on calculating similarities between queries/users and documents/items.
機械学習とディープラーニングのパラダイムは、検索／レコメンデーションタスクを識別問題としてアプローチしており、クエリ／ユーザーと文書／アイテムの類似性を計算することに焦点を当てている。
In contrast, the generative paradigm formulates the task as a generation problem, aiming to directly generate the documents/items based on the queries/users.
対照的に、生成パラダイムはタスクを生成問題として定式化し、クエリ/ユーザに基づいて文書/項目を直接生成することを目指す。
We need to address two specific issues for the three paradigms.1) Deep learning is a subset of machine learning, and neural generative models are a subset of deep learning.
1）ディープラーニングは機械学習のサブセットであり、ニューラル生成モデルはディープラーニングのサブセットである。
While there are sub-concepts within these paradigms, they have clear boundaries and distinct development directions.
これらのパラダイムにはサブコンセプトが存在するが、明確な境界線と明確な発展の方向性がある。
For instance, with the emergence of deep learning, new methods have been developed to apply neural networks for feature extraction in search and recommendation systems, despite deep learning being a part of machine learning.
例えば、ディープラーニングの登場により、ディープラーニングは機械学習の一部であるにもかかわらず、検索や推薦システムにおける特徴抽出にニューラルネットワークを応用する新しい手法が開発されている。
Similarly, generative models have gained popularity, with numerous works focusing on generative search and recommendation.2) We use the term “paradigm shift” to indicate potential community interest rather than actual trends.
同様に、生成モデルも人気を博しており、生成検索と推薦に焦点を当てた多くの作品がある。
Both generative search and recommendation are relatively new approaches in the research community, and their effectiveness has not been fully verified historically.
生成的検索も推薦も、研究コミュニティでは比較的新しいアプローチであり、その有効性は歴史的に十分に検証されていない。
Comparison with LLM-based discriminative methods.
LLMベースの識別手法との比較。
In this study, we define generative search and generative recommendation as methods that fully accomplish search and recommendation tasks using generative models.
本研究では、生成的検索と生成的推薦を、生成モデルを用いて検索と推薦のタスクを完全に達成する手法と定義する。
This is a specific definition that may exclude certain works.
これは具体的な定義であり、特定の作品を除外する可能性がある。
For example, some approaches [97, 100] may use generative language models to extract features from queries/users and documents/items.
例えば、いくつかのアプローチ[97, 100]は、クエリ/ユーザーと文書/アイテムから特徴を抽出するために、生成言語モデルを使用することができる。
While these works also utilize generative language models, the overall paradigm is not significantly different from previous methods, as they simply replace the original encoder with a generative language model.
これらの作品も生成言語モデルを利用しているが、全体的なパラダイムは、元のエンコーダーを生成言語モデルに置き換えただけで、以前の手法と大きな違いはない。
In our study, we focus on presenting works that completely utilize generative paradigms to accomplish search or recommendation tasks.
我々の研究では、検索や推薦タスクを達成するために生成的パラダイムを完全に利用した作品を紹介することに焦点を当てる。

## 3.2. Unified Framework ユニファイド・フレームワーク

Benefiting from the simplicity of the generative paradigm, we could summarize the generative search and generative recommendation into a unified framework.
生成的パラダイムのシンプルさから、我々は生成的検索と生成的推薦を統一的なフレームワークにまとめることができた。
To accomplish search and recommendation tasks in a generative manner, there are four essential steps: 1) Query/User Formulation: This step aims to determine the input of the generative model.
検索と推薦のタスクを生成的な方法で達成するためには、4つの重要なステップがある： 1) クエリー／ユーザーの定式化： このステップは生成モデルの入力を決定することを目的とする。
For search, complex query formulation is not necessary; for recommendation, user formulation is vital to transform user information into textual sequences.2) Document/Item Identifiers: In practice, directly generating the document or item is almost impossible.
検索では、複雑なクエリの定式化は必要ない。推薦では、ユーザー情報をテキストシーケンスに変換するために、ユーザー定式化が不可欠である： 実際には、文書やアイテムを直接生成することはほとんど不可能である。
Therefore, a short text sequence, known as the identifier, is used to represent the document or item.3) Training: Once the input (query/user formulation) and output (document/item identifiers) of the generative model are determined, training is easily achieved via the generation loss.4) Inference: After the training, the generative model can receive the query/user to predict the document/item identifier, and the document/item identifier can correspond to the document or item.
そのため、識別子として知られる短いテキスト列が、文書やアイテムを表すのに使われる： 学習：生成モデルの入力（クエリ／ユーザー定式化）と出力（文書／アイテム識別子）が決定されると、学習は生成ロスを介して簡単に達成される： 学習後、生成モデルはクエリ/ユーザから文書/項目識別子を予測し、文書/項目識別子は文書または項目に対応することができる。
While the entire process may seem simple, achieving effective generative search and recommendation is not trivial.
プロセス全体は単純に見えるかもしれないが、効果的なジェネレーティブ検索と推薦を実現するのは些細なことではない。
Numerous details need to be considered and balanced within the four steps mentioned above.
上記の4つのステップの中で、数多くの詳細を考慮し、バランスを取る必要がある。
In Sections 4 and 5, we will summarize generative search and generative recommendation methods, emphasizing their focus on specific aspects within the framework.
セクション4と5では、生成的検索と生成的推薦の方法を要約し、フレームワークの中で特定の側面に焦点を当てていることを強調する。

# 4. Generative Search ジェネレーティブ・サーチ

## 4.1. Overview 概要

Generative search endeavors to leverage generative models, specifically generative language models, to complete the conventional search and retrieval process.
生成検索は、生成モデル、特に生成言語モデルを活用して、従来の検索と検索のプロセスを完成させようとするものである。
The target is still the matching between documents and a given query.
ターゲットはやはり、文書と与えられたクエリとのマッチングである。
Different from previous paradigms, generative search aims to directly generate the desired target document when presented with a query.
これまでのパラダイムとは異なり、生成検索は、クエリが提示されたときに、目的のターゲット文書を直接生成することを目的としている。

## 4.2. Query Formulation クエリ策定

In search, users typically express their information needs through textual queries.
検索では、ユーザーは通常、テキストクエリを通じて情報ニーズを表現する。
This is in contrast to generative recommendation, which involves a “user formulation” step to convert user history into a textual sequence.
これは、ユーザーの履歴をテキストシーケンスに変換する「ユーザー定式化」ステップを含む生成的推薦とは対照的である。
In most retrieval tasks, the textual query can be directly inputted into the generative language model, sometimes with simple prefixes like “query: ”.
ほとんどの検索タスクでは、テキストクエリを生成言語モデルに直接入力することができる： ".
However, in certain retrieval tasks such as conversational QA and multi-hop QA, the query must be combined with the conversation context [74] or previous-hop answers [62].
しかし、会話QAやマルチホップQAのような特定の検索タスクでは、クエリを会話コンテキスト[74]や前ホップ回答[62]と組み合わせる必要がある。

## 4.3. Document Identifiers ドキュメント識別子

Ideally, generative search aims to directly generate the complete target document in response to a given query.
理想的には、生成検索は、与えられたクエリに応答して、完全なターゲット文書を直接生成することを目指している。
However, in practice, this task proves to be extremely challenging for LLMs due to the length and inclusion of irrelevant information in the document’s content.
しかし、実際には、このタスクは、文書の内容の長さと無関係な情報が含まれているために、LLMにとって非常に困難であることが判明した。
Consequently, current generative search approaches often rely on the use of identifiers to represent documents.
その結果、現在の生成的検索アプローチは、しばしば文書を表現するための識別子の使用に依存している。
These identifiers are concise strings that effectively capture the essence of a document’s content.
これらの識別子は、文書の内容の本質を効果的に捉える簡潔な文字列である。
We summarize the current identifiers in generative search methods, and analyze their advantages and disadvantages as follows.
生成的検索法における現在の識別子を要約し、その長所と短所を以下のように分析する。
Numeric ID [70, 101, 133, 147, 177, 179].
数値ID [70, 101, 133, 147, 177, 179]。
Each document in the corpus can be assigned a unique numeric ID, such as “12138”.
コーパスの各文書には、"12138 "のようなユニークな数字IDを割り当てることができる。
During the inference stage, the LLM can receive the query as input and generate either a single numeric ID or a list of numeric IDs using beam search.
推論段階では、LLMはクエリーを入力として受け取り、ビームサーチを使って単一の数値IDまたは数値IDのリストを生成することができる。
Since each document corresponds to a numeric ID, the predicted numeric ID can represent a retrieved document.
各文書は数値IDに対応しているので、予測された数値IDは検索された文書を表すことができる。
However, it is important to note that the numeric ID itself does not have any semantic relation to the content of the document.
しかし、数値ID自体は、文書の内容とは意味的な関係を持たないことに注意することが重要である。
There are several methods to establish correlations between semantic text and numeric IDs.1) Document-to-numeric ID training.
意味論的テキストと数値IDの相関を確立するには、いくつかの方法がある。
During the training phase, an LLM can be trained to take a document’s content as input and generate the corresponding numeric ID as the target.
学習段階において、LLMは文書の内容を入力とし、対応する数値IDをターゲットとして生成するように学習させることができる。
This training approach compels the LLM to memorize the relationships between documents and their numeric IDs.
この学習方法は、LLMに文書間の関係とその数値IDを記憶させる。
Once trained effectively, the LLM is expected to recall the numeric IDs of the documents accurately.2) Clustered numeric IDs.
いったん効果的に学習されれば、LLMは文書の数字IDを正確に想起することが期待される。
In [133], the authors explored the concept of clustering document embeddings and assigning numeric IDs based on the cluster results.
133]では、文書埋め込みをクラスタリングし、クラスタ結果に基づいて数値IDを割り当てるというコンセプトを探求している。
This approach allows similar documents with comparable content to be grouped into the same clusters, resulting in similar numeric IDs for these documents.
このアプローチにより、同等の内容を持つ類似文書を同じクラスターにグループ化することができ、その結果、これらの文書に類似した数値IDが付与される。
Unlike randomly assigned numeric IDs, the clustered IDs are determined based on the content of the documents and are consistent with their semantics.
ランダムに割り当てられた数値のIDとは異なり、クラスタ化されたIDは文書の内容に基づいて決定され、文書のセマンティクスと一致している。
Numeric IDs pose challenges in generative search for the following reasons.1) Generalization.
数値IDは、以下の理由により、ジェネレーティブ・サーチに課題をもたらす。
The inability to generalize is a significant issue for numeric IDs.
一般化できないことは、数値IDにとって重大な問題である。
Previous studies [133] have shown that the Language Model can effectively memorize numeric IDs of passages in the training set.
先行研究[133]では、言語モデルが学習セット内のパッセージの数字IDを効果的に記憶できることが示されている。
However, when it comes to the test set, the LLM’s performance deteriorates.
しかし、テストセットになると、LLMの性能は悪化する。
This can be attributed to the fact that numeric IDs lack semantic meaning, making it difficult for the model to generalize to unseen data.
これは、数値のIDには意味的な意味がないため、モデルが未見のデータに一般化しにくいことに起因している。
To address this problem, NCI [147] proposed the inclusion of pseudo-queries on test set passages, which helps alleviate the issue.2) Corpus update.
この問題に対処するため、NCI [147]はテストセットのパッセージに擬似クエリを含めることを提案した。
Updating poses a challenge for generative search methods based on numeric IDs.
更新は、数値IDに基づく生成的検索方法にとって難題となる。
Unlike dense retrieval methods that can easily update passages by modifying the embedding vectors in the corpus, the LLM struggles with updating passages.
コーパスの埋め込みベクトルを修正することで簡単にパッセージを更新できる高密度検索手法とは異なり、LLMはパッセージの更新に苦労する。
This is because the LLM stores the passages in its parameters, and accurately editing these parameters is not feasible.
これは、LLMがパラメータにパッセージを保存しているためで、これらのパラメータを正確に編集することは不可能である。
In [98], the authors introduced incremental learning to solve the passage-adding problem partially.3) Large-scale corpus.
98]では、パッセージ追加問題を部分的に解決するためにインクリメンタル学習を導入した。
Since generative search models must memorize the associations between documents and their numeric IDs, the memorization difficulty increases as the document corpus sizes increase.
生成検索モデルは、文書とその数値IDとの関連を記憶しなければならないので、文書コーパスのサイズが大きくなるにつれて、記憶の難易度は高くなる。
The work [105] explored to scaling up numeric ID based generative search.
105]は、数値IDに基づく生成的検索をスケールアップすることを探求した。
It is found that while generative search is competitive with state-of-the-art dual encoders on small corpora, scaling to millions of passages remains an important and unsolved challenge.
生成的検索は、小規模なコーパスでは最新のデュアルエンコーダと競合するものの、数百万パッセージへのスケーリングは重要かつ未解決の課題であることがわかった。
Document titles [15, 24, 62, 74].
文書のタイトル [15, 24, 62, 74]。
In certain specific scenarios, documents possess titles that can serve as effective identifiers.
特定のシナリオでは、文書は効果的な識別子として機能するタイトルを持つ。
For instance, in Wikipedia, each page is assigned a unique title that succinctly summarizes its content.
例えば、ウィキペディアでは、各ページにはその内容を簡潔に要約したユニークなタイトルが付けられている。
These titles are semantically linked to the documents and establish a one-to-one correspondence, making them ideal identifiers.
これらのタイトルは文書と意味的にリンクされ、1対1の対応を確立するため、理想的な識別子となる。
In 2021, Cao et al.investigated the utilization of titles as identifiers in entity retrieval and document retrieval [24].
2021年、Caoらは、エンティティ検索と文書検索における識別子としてのタイトルの利用について調査した[24]。
Besides, there are some title-like identifiers, including URLs [113, 178, 180], keywords [63], and summaries [176].
さらに、URL[113, 178, 180]、キーワード[63]、要約[176]など、タイトルのような識別子もある。
However, document titles are only effective in certain retrieval domains and prove ineffective in the following aspects.1) Firstly, in passage-level retrieval, documents are often divided into smaller retrieval units known as passages.
1）まず、パッセージ・レベルの検索では、文書はパッセージと呼ばれる小さな検索単位に分割されることが多い。
It is hard to design effective passage identifiers even based on the document titles, which makes title-based generative search perform badly in passage retrieval.
文書のタイトルに基づいても、効果的なパッセージ識別子を設計することは困難であり、そのため、タイトルに基づく生成検索はパッセージ検索において悪い結果をもたらす。
In 2023, Li et al.employed document titles plus section titles as passage identifiers, but this approach was limited to the Wikipedia corpus [74].2) Secondly, web pages differ from Wikipedia in web retrieval as they lack high-quality titles.
2023年、Liらは文書タイトルとセクションタイトルを通路識別子として採用したが、このアプローチはWikipediaコーパスに限定されていた[74]。2) 次に、ウェブ検索においてウェブページはWikipediaと異なり、高品質のタイトルがない。
These titles may not accurately represent the content of the document, and multiple web pages may share the same title.3) Additionally, numerous pages do not have any titles at all.
これらのタイトルは文書の内容を正確に表しているとは限らず、複数のウェブページが同じタイトルを共有している場合がある。
These factors contribute to generative search lagging behind traditional retrieval methods.
これらの要因は、生成検索が従来の検索手法に遅れをとる一因となっている。
N-grams [7, 14, 150, 169].
Nグラム [7, 14, 150, 169]。
The document itself is semantic but cannot serve as a reliable identifier.
文書自体はセマンティックだが、信頼できる識別子としては機能しない。
This is because not all of its content is necessarily related to the user query, making it difficult for the LLM to generate irrelevant content based solely on the user query.
これは、LLMのすべてのコンテンツが必ずしもユーザーのクエリに関連しているわけではないため、LLMがユーザーのクエリのみに基づいて無関係なコンテンツを生成することが難しいためである。
However, inspired by this limitation, the N-grams within the document that are semantically related to the user query could be regarded as potential identifiers.
しかし、この制限に触発され、ユーザークエリに意味的に関連する文書内のN-gramを潜在的な識別子とみなすことができる。
In 2022, the authors in [7] trained an LLM to generate target N-grams using a user query as input.
2022年、[7]の著者らは、ユーザークエリーを入力として、ターゲットN-gramを生成するLLMを訓練した。
These N-grams were selected based on the word overlap between the user query and the N-grams.
これらのN-gramは、ユーザークエリとN-gramの間の単語の重複に基づいて選択された。
Once trained, the LLM was able to predict relevant N-grams given a query.
一度訓練されると、LLMはクエリが与えられたときに関連するN-gramを予測することができた。
These predicted N-grams were then transformed into a passage rank list using a heuristic function.
これらの予測されたN-gramは、ヒューリスティック関数を使ってパッセージ順位リストに変換された。
The proposed method was evaluated on commonly used datasets, including NQ and TriviaQA, rather than some specifically designed subsets of datasets.
提案手法は、特別に設計されたデータセットのサブセットではなく、NQやTriviaQAを含む一般的に使用されているデータセットで評価された。
However, N-gram identifiers have certain limitations.1).
しかし、N-gram識別子には一定の限界がある1)。
Firstly, they are not as discriminative as numeric IDs.
第一に、数値IDほど識別性が高くない。
Unlike numeric IDs, N-grams cannot directly correspond to specific documents on a oneto-one basis.
数値IDとは異なり、N-gramは特定の文書に一対一で直接対応することはできない。
This means that the LLM must rely on a transformation function to convert the predicted N-grams into a document ranking list.
つまり、LLMは予測されたN-gramを文書ランキングリストに変換する変換関数に頼らなければならない。
In SEAL [7], for example, the transformation function calculates a document’s score by summarizing the scores of the N-grams it contains.
例えばSEAL [7]では、変換関数は文書が含むN-gramのスコアを要約することで文書のスコアを計算する。
In a way, this transformation function acts as a simple retrieval approach, preventing N-gram-based generative search from achieving end-to-end document retrieval.2) Secondly, the selection of N-grams in the training phase is a crucial aspect.
ある意味で、この変換機能は単純な検索アプローチとして機能し、N-gramベースの生成検索がエンド・ツー・エンドの文書検索を達成することを妨げている。
A document may contain numerous N-grams, and it is necessary to select those that are semantically relevant to the query.
文書には多数のN-gramが含まれている可能性があり、クエリに意味的に関連するものを選択する必要がある。
However, the number of N-grams to be selected and the method used for selection are adjustable and can vary largely.
ただし、選択するN-gramの数や選択方法は調整可能であり、大きく変化する可能性がある。
Codebook [125, 159, 164, 166].
コードブック [125, 159, 164, 166]。
The text codebook, also known as tokens, plays a fundamental role in LLMs.
トークンとも呼ばれるテキストコードブックは、LLMにおいて基本的な役割を果たす。
Text is inherently discrete, allowing LLMs to acquire knowledge through tasks like predicting the next token.
テキストは本質的に離散的であるため、LLMは次のトークンを予測するようなタスクを通じて知識を獲得することができる。
Some studies [60, 137] have also focused on developing visual codebooks for discrete images.
いくつかの研究[60, 137]は、離散画像の視覚的コードブックの開発にも焦点を当てている。
As mentioned earlier, while a document can be represented as a list of tokens, it is not suitable as an identifier due to its lengthiness.
前述したように、文書はトークンのリストとして表現できるが、その長さから識別子としては適していない。
Therefore, an alternative approach is to learn a new codebook specifically for documents, which can represent them more efficiently than natural text tokens.
そのため、別のアプローチとして、文書に特化した新しいコードブックを学習することで、自然なテキストトークンよりも効率的に文書を表現することができる。
In 2023, Sun et al.proposed a method to learn a codebook for documents in generative search [125].
2023年、Sunらは、生成的検索における文書のコードブックを学習する方法を提案した[125]。
The work [159] proposed an end-to-end framework to automatically search best identifiers according to the document’s content.
159]は、文書の内容に応じて最適な識別子を自動的に検索するエンド・ツー・エンドのフレームワークを提案した。
However, learning a codebook for documents is a complex process.
しかし、文書のコードブックを学習するのは複雑なプロセスである。
It typically involves encoding documents into dense vectors using an encoder network, discretizing these vectors, and then using a decoder network to reconstruct the original document.
通常、エンコーダー・ネットワークを使って文書を密なベクトルにエンコードし、これらのベクトルを離散化し、デコーダー・ネットワークを使って元の文書を再構築する。
The size of the codebook and the length of the sequence required to represent a document must be carefully adjusted.
コードブックのサイズと、文書を表現するのに必要なシーケンスの長さは、慎重に調整する必要がある。
Additionally, compared to titles and n-grams, the codebook lacks interpretability.
さらに、タイトルやn-gramと比べると、コードブックは解釈性に欠ける。
Multiview identifiers [75–77].
マルチビュー識別子[75-77]。
The above identifiers are limited in different aspects: numeric IDs require extra memorization steps and are ineffective in the large-scale corpus, while titles and substrings are only pieces of passages and thus lack contextualized information.
上記の識別子はさまざまな面で限界がある： 数値IDは余分な暗記ステップを必要とし、大規模なコーパスでは効果がない。一方、タイトルと部分文字列はパッセージの一部でしかないため、文脈情報に欠ける。
More importantly, a passage should answer potential queries from different views, but one type of identifier only represents a passage from one perspective.
さらに重要なのは、パッセージはさまざまな視点から潜在的なクエリに答えなければならないが、1つのタイプの識別子は1つの視点からしかパッセージを表現できないことである。
Therefore, a natural idea is to combine different identifiers to exploit their advantages.
したがって、異なる識別子を組み合わせてそれぞれの利点を生かすというのは自然な発想である。
In 2023, Li et al.[76] proposed a generative search framework, MINDER, to unify different identities, including titles, N-grams, pseudo queries, and numeric IDs.
2023年、Liら[76]は、タイトル、N-gram、擬似クエリ、数値IDなどの異なるIDを統一するための生成的検索フレームワーク、MINDERを提案した。
Any other identifiers could also be included in this framework.
その他の識別子もこの枠組みに含めることができる。
The experiments on three common datasets verify the effectiveness and robustness of different retrieval domains benefiting from the multiview identifiers.
3つの一般的なデータセットを用いた実験により、マルチビュー識別子の恩恵を受けるさまざまな検索ドメインの有効性と頑健性が検証された。
Similar to the N-grams, multiview identifiers cannot correspond to documents one-to-one and thus require the transformation function.
N-gramと同様に、マルチビュー識別子は文書と一対一に対応できないため、変換関数が必要となる。
Besides, in the inference stage, the LLM needs to generate different types of identifiers, decreasing the inference efficiency.
その上、推論段階でLLMは異なるタイプの識別子を生成する必要があり、推論効率が低下する。

Document identifier summary.
文書識別子の概要。
To better illustrate the characteristics of different document identifiers, we summarize Table 1 from the aspects of semantic, distinctiveness, update, training, and applicable retrieval domains.
異なる文書識別子の特徴をよりよく説明するために、意味、識別性、更新、訓練、および適用可能な検索ドメインの側面から表1を要約する。
Among the various types of identifiers, the codebook shows great potential in all dimensions.
さまざまなタイプの識別子の中で、コードブックはあらゆる次元で大きな可能性を示している。
However, it does have a drawback in that it requires a complex training process.
しかし、複雑なトレーニングプロセスを必要とするという欠点がある。
The multiview identifier has a simpler training process, but it lacks distinctiveness and requires a transform function from identifiers to documents.
マルチビュー識別子は学習プロセスが単純だが、識別性に欠け、識別子から文書への変換関数が必要である。

## 4.4. Training トレーニング

In contrast to traditional retrieval methods, the training for generative search is notably simpler.
従来の検索手法とは対照的に、生成検索のトレーニングは格段にシンプルだ。
We categorize the training into generative and discriminative training two categories.
我々は、トレーニングを生成的トレーニングと識別的トレーニングの2つに分類している。
Generative training.
ジェネレーショントレーニング。
Once the input and output are determined, the LLM can be trained to predict the next token.
入力と出力が決まれば、次のトークンを予測するためにLLMを学習させることができる。
There are two main training directions.1) Query-to-identifier training.
1）クエリから識別子への学習。
This involves training the LLM to generate the corresponding identifier for a given query.
これは、与えられたクエリに対応する識別子を生成するためにLLMを訓練することを含む。
Most identifier types require this training, with some, such as document titles, N-grams, and multiview identifiers, only needing this query-to-identifier training direction.2) Documentto-identifier training.
ほとんどの識別子タイプはこのトレーニングを必要とするが、文書タイトル、N-gram、マルチビュー識別子など、このクエリから識別子へのトレーニングの方向性だけを必要とするものもある。
In this approach, the LLM learns to predict the corresponding identifier when given a document as input.
このアプローチでは、LLMは入力として文書が与えられたときに、対応する識別子を予測するように学習する。
This training is crucial for certain identifiers, such as numeric IDs and the codebook, as they need to align with the semantics of documents, and codebook training could be regarded as the special document-to-identifier training.
この訓練は、数値IDやコードブックのような特定の識別子にとっては、文書のセマンティクスと一致させる必要があるため極めて重要であり、コードブックの訓練は、文書から識別子への特別な訓練とみなすことができる。
It is noted that not all documents in a search have labels (queries), making it challenging for the LLM to memorize these documents.
検索に含まれるすべての文書にラベル（クエリー）があるとは限らないため、LLMがこれらの文書を記憶するのは困難である。
To address this, some generative search methods [105, 179] utilize pseudo pairs to expand the training samples and enhance document memorization.
これに対処するため、いくつかの生成的検索手法[105, 179]は、擬似ペアを利用して学習サンプルを拡大し、文書の記憶性を高めている。
Discriminative training.
識別トレーニング。
Generative search presents a new paradigm for retrieval, as it transforms the original discriminative methods into the generative methods and could train the retrieval model (generative language model) via generation loss.
生成的検索は、検索の新しいパラダイムを提示するものである。なぜなら、本来の識別的手法を生成的手法に変換し、生成損失によって検索モデル（生成的言語モデル）を訓練することができるからである。
However, the work [75] has highlighted the importance of discriminative training in generative search.
しかし、[75]の研究は、生成的探索における識別トレーニングの重要性を強調している。
It has been observed that discriminative training can further improve a well-trained generative model.
識別トレーニングは、よく訓練された生成モデルをさらに向上させることができることが観察されている。
This finding is meaningful for both generative search and the traditional retrieval paradigm.
この発見は、生成検索と従来の検索パラダイムの双方にとって有意義である。
Previous retrieval studies have developed numerous discriminative losses (rank losses) and negative sample mining methods, which is a big treasure for the retrieval field.
これまでの検索研究では、数多くの識別損失（ランク損失）やネガティブサンプルマイニング法が開発されており、これは検索分野にとって大きな宝である。
As the finding illustrates, the previous research approaches could be adjusted to enhance the current generative search.
この発見が示すように、これまでの研究アプローチは、現在のジェネレーティブ・サーチを強化するために調整することができる。
The following works [132, 164] further verified the effectiveness of introducing discriminative training in generative search.
次の研究[132, 164]は、生成的探索に識別学習を導入することの有効性をさらに検証している。

## 4.5. Inference 推論

After completing the training process, the generative search model can be used for retrieval purposes.
学習プロセスが完了すると、生成検索モデルを検索目的で使用することができる。
Free generation.
フリー世代。
During the inference stage, the trained LLM is able to predict identifiers based on a user query, similar to the training process.
推論段階では、訓練されたLLMは、訓練プロセスと同様に、ユーザークエリに基づいて識別子を予測することができる。
This generation process is free, as the LLM could generate any text without any constraints.
この生成プロセスは自由であり、LLMは制約なしにどんなテキストでも生成することができる。
These predicted identifiers may correspond directly to specific documents, or they may be determined through a heuristic function based on the type of identifier.
これらの予測識別子は、特定の文書に直接対応する場合もあれば、識別子の種類に基づくヒューリスティック関数によって決定される場合もある。
This is the unique aspect of generative search, as it allows for direct document retrieval through generation.
これが生成検索のユニークな点で、生成によって直接文書を検索することができる。
However, in practical applications, only a few generative approaches [159, 180] actually utilize the free generation method.
しかし、実用的な応用において、実際に自由生成法を利用する生成的アプローチ[159, 180]はわずかである。
Because the scope of identifiers is limited, the potential for generation is infinite.
識別子の範囲は限られているため、生成の可能性は無限である。
This means that the LLM may generate identifiers that could not belong to any document within the corpus.
これは、LLMがコーパス内のどの文書にも属さない識別子を生成する可能性があることを意味する。
Constrained generation.
制約された世代。
Most generative search approaches employ constrained generation to guarantee the LLM generates valid identifiers.
ほとんどの生成的検索アプローチは、LLMが有効な識別子を生成することを保証するために、制約付き生成を採用している。
This technique involves post-processing to mask any invalid tokens and only allows the generation of valid tokens that belong to identifiers.
この手法では、無効なトークンをマスクするための後処理が行われ、識別子に属する有効なトークンのみが生成される。
To achieve this, special data structures such as Trie and FM_index [29] are utilized.
これを実現するために、TrieやFM_index [29]のような特別なデータ構造が利用される。
The FM_index enables the LLM to generate valid tokens from any position within the identifier, while the Trie only supports generation from the first token of an identifier.
FM_indexは、LLMが識別子のどの位置からでも有効なトークンを生成することを可能にするが、Trieは識別子の最初のトークンからの生成しかサポートしない。
These data structures play a key role in enabling the LLM to accurately generate valid identifiers.
これらのデータ構造は、LLMが有効な識別子を正確に生成するために重要な役割を果たしている。
The predicted identifiers could correspond directly to specific documents, or they may be determined through a heuristic function based on the type of identifier.
予測される識別子は、特定の文書に直接対応することもできるし、識別子の種類に基づくヒューリスティック関数によって決定されることもある。
Finally, generative search methods could give a final document ranking list in a generative way.
最後に、生成的検索方法は、生成的な方法で最終的な文書ランキングリストを与えることができる。

## 4.6. Summary 要約

Methods summary.
方法の要約。
We summarize the current generative search methods in Table 2, from the aspects of identifier, backbone, constrained generation, and datasets.1) Identifier.
現在の生成検索法を、識別子、バックボーン、制約付き生成、データセットの側面から表2にまとめる。
We have fully discussed the characteristics and problems of different identifiers in the previous sections and Table 1.
前節と表1で、さまざまな識別子の特徴と問題点を十分に論じた。
Different identifiers usually require different training strategies and inference processes.2) Backbone.
異なる識別子は通常、異なるトレーニング戦略と推論プロセスを必要とする。
Almost all methods employ pretrained language models, like BART [64] and T5 [111], as the backbone, due to their extensive language knowledge.
ほとんどの手法は、BART [64]やT5 [111]のような、事前に学習された言語モデルをバックボーンとして採用している。
However, it is also noted that few current approaches apply advanced large foundation models, like ChatGPT and LLaMA.
しかし、現在のアプローチでは、ChatGPTやLLaMAのような先進的な大規模基礎モデルを適用しているものはほとんどないことも指摘されている。
On the one hand, increasing the model size alone may not lead to significant research contributions; on the other hand, closed-source models cannot be adjusted for constrained generation.3) Constrained generation.
一方では、モデルサイズを大きくするだけでは、大きな研究貢献にはつながらないかもしれない。他方では、クローズドソースのモデルは、制約付き生成のために調整することができない。
Almost all methods adopt the constrained generation to guarantee the valid identifier generation.
ほとんどの方法は、有効な識別子の生成を保証するために制約付き生成を採用している。
The multiview identifier and N-gram identifier require the FM_index structure, while others need the Trie structure to facilitate the constrained generation.4) Datasets are primarily focused on document-level and passage-level retrieval tasks, with some also designed for conversational QA, multi-hop QA, and cross-lingual retrieval tasks.
マルチビュー識別子とN-gram識別子はFM_index構造を必要とし、その他は制約付き生成を容易にするためにTrie構造を必要とする。4) データセットは主に文書レベルとパッセージレベルの検索タスクに焦点を当てているが、会話QA、マルチホップQA、言語横断検索タスク用に設計されたものもある。
However, due to limitations in identifier types, some methods have had to reformulate certain datasets for evaluation, such as NQ320k, TriviaQA (subset), and MSMARCO (subset).
しかし、識別子の種類に制限があるため、NQ320k、TriviaQA（サブセット）、MSMARCO（サブセット）のように、評価のために特定のデータセットを再構成しなければならない手法もある。
While these reformulated datasets may highlight the advantages of generative search, they may not align with real-world applications.
これらの再定式化されたデータセットは、ジェネレーティブ・サーチの利点を強調するかもしれないが、実世界のアプリケーションとは一致しないかもしれない。
Multiview identifiers based methods [75–77] have a significant advantage in general retrieval datasets.
マルチビュー識別子に基づく手法[75-77]は、一般的な検索データセットにおいて大きな優位性を持つ。

Timeline summary.
タイムラインの要約。
We also provide a brief overview of the development of generative search based on the timeline, as depicted in Figure 2.
また、図2に描かれているように、時系列に基づいたジェネレーティブ・サーチの発展についても簡単に説明する。
We specifically highlight the works that first introduced a new identifier type or training scheme in generative search.
特に、生成的探索において新しい識別子のタイプや学習スキームを最初に導入した作品に焦点を当てる。
The credit for the first generative search work goes to GENRE [24].
最初のジェネレーティブ・サーチの功績はGENRE [24]にある。
While GENRE’s primary focus is on entity retrieval rather than document retrieval, it was the first to employ the autoregressive generation paradigm to accomplish the retrieval task and introduce constrained beam search.
GENREの主な焦点は文書検索ではなく実体検索であるが、検索タスクを達成するために自己回帰生成パラダイムを採用し、制約付きビーム検索を導入した最初のものである。
Starting from 2022, there has been a continuous introduction of new identifier types [7, 76, 125, 133].
2022年以降、新しいタイプの識別子が継続的に導入されている[7, 76, 125, 133]。
In 2023, discriminative training [75] was introduced in generative search, followed by the latest works [132, 164].
2023年には、判別学習[75]が生成的探索に導入され、最新の研究[132, 164]がそれに続いた。

## 4.7. LLMs for Retrieval beyond Generative Search 生成的検索を超えた検索のためのLLM

There have been efforts to investigate the potential applications of LLMs in text retrieval beyond generative search.
テキスト検索におけるLLMの応用の可能性を、生成的検索以外にも調査しようとする努力がなされてきた。
These studies have concentrated on leveraging LLMs to improve existing retrieval pipelines by substituting smaller language models with larger ones.1) LLMs for query expansion.
これらの研究は、LLMを活用して、より小さな言語モデルをより大きな言語モデルに置き換えることで、既存の検索パイプラインを改善することに集中している。
Some works [50, 143] utilized LLMs to expand the queries.
いくつかの研究 [50, 143]では、クエリを拡張するためにLLMを利用している。
For instance, Query2Doc [143] employs LLMs to generate synthetic documents, which can then be integrated into traditional document retrieval systems to enhance their performance.2) LLMs as feature extractors.
例えば、Query2Doc [143]は、合成文書を生成するためにLLMを採用しており、これを従来の文書検索システムに統合することで、パフォーマンスを向上させることができる。
Dense retrievers are usually conducted based on encoder-only language models, like BERT.
高密度検索は通常、BERTのようなエンコーダのみの言語モデルに基づいて行われる。
Recently, some work [97, 100] has focused on leveraging generative large language models to improve document representations.3) LLMs based rankers.
最近では、生成的な大規模言語モデルを活用して文書表現を改善する研究 [97, 100]も行われている。
Rankers should further refine the order of the retrieved candidates to improve output quality, and LLMs have also been applied to refine the ranking of retrieved documents, as demonstrated in studies [108, 126].
ランカーは出力品質を向上させるために、検索された候補の順序をさらに洗練させる必要があり、研究[108, 126]で実証されているように、LLMは検索された文書のランキングを洗練させるためにも適用されている。

# 5. Generative Recommendation 生成的推薦

## 5.1. Overview 概要

Since recommendation systems aim to filter out the items that are relevant to the user interests, two crucial components are required to achieve matching in the natural language space, i.e., user formulation, and item identifiers.
推薦システムは、ユーザーの興味に関連するアイテムをフィルタリングすることを目的としているため、自然言語空間におけるマッチングを実現するためには、2つの重要な要素、すなわち、ユーザーの定式化とアイテムの識別子が必要となる。
The user formulation and item identifiers are analogous to the query formulation and document identifier in generative search, respectively.
ユーザの定式化とアイテムの識別子は、それぞれ生成検索におけるクエリの定式化と文書の識別子に類似している。
Specifically, as the input for generative model, the user formulation contains diverse information (e.g., user’s historical interactions, and user profile) to represent a user in the natural language for modeling the user interests.
具体的には、生成モデルの入力として、ユーザー定式化には、ユーザーの興味をモデル化するために、ユーザーを自然言語で表現するための多様な情報（例えば、ユーザーの過去のやりとりやユーザープロファイル）が含まれる。
To match the user interests in natural language, generative recommendation system will generate item identifier of the relevant items.
自然言語でユーザーの興味にマッチするように、生成的推薦システムは関連するアイテムの識別子を生成する。

## 5.2. User Formulation ユーザー処方

Since there is no specific “query” for each user in recommendation systems, user formulation is a crucial step to represent a user for personalized recommendation.
推薦システムでは、各ユーザに対する特定の「クエリ」が存在しないため、パーソナライズされた推薦のためにユーザを表現するためのユーザ定式化が重要なステップとなる。
In generative recommendation systems, the user2 is primarily formulated based on four distinct components: the task description, user-associated information, context information, and external knowledge expressed in natural language.
生成的推薦システムでは、ユーザー2は主に4つの異なる要素に基づいて定式化される： タスク記述、ユーザー関連情報、コンテキスト情報、そして自然言語で表現された外部知識である。
In particular, the user-associated information mainly consists of user’s historical interactions and user profile (e.g., age and gender).
特に、ユーザー関連情報は、主にユーザーの過去のインタラクションとユーザープロファイル（年齢や性別など）から構成される。
Based on the availability of the data, previous work formulates the user by encompassing one or multiple components through pre-defined prompt templates for each user.
データの利用可能性に基づいて、以前の研究では、各ユーザーのために事前に定義されたプロンプトテンプレートを通じて、1つまたは複数のコンポーネントを包含することによってユーザーを定式化する。
Task description [33].
タスクの説明[33]。
To leverage the strong comprehension ability of the powerful generative models, task description is employed to guide the generative models to accomplish the recommendation task, i.e., next-item prediction.
強力な生成モデルの強力な理解能力を活用するために、生成モデルが推薦タスク、すなわち次項目予測を達成するように導くタスク記述が採用される。
For instance, in [4], the task description for movie recommendation is articulated as “Given ten movies that the user watched recently, please recommend a new movie that the user likes to the user.”.It is noted that the task description can also serve as the prompt template, where various components are inserted into the template to formulate the user.
例えば、[4]では、映画推薦のタスク記述は、「ユーザが最近見た10本の映画が与えられたら、ユーザが好きな新しい映画をユーザに推薦してください」と表現されている。タスク記述はプロンプトテンプレートとしても機能し、様々なコンポーネントがテンプレートに挿入され、ユーザを定式化することができる。
For example, [33] uses “I find the purchase history of ..., I wonder what is the next item to recommend to the user.
例えば、[33]は「...の購入履歴を見つけたら、次にユーザーに勧めるべきアイテムは何だろう？
Can you help me decide?” as the task description to instruct the generative models, where the user’s historical interactions will be utilized for user formulation.
をタスク記述として生成モデルに指示し、ユーザーの過去のやりとりがユーザー定式化に利用される。
In [168], “Here is the historical interactions of a user: ..., his preferences are as follows: ..., please provide recommendations.” is used to guide the generative models, where historical interactions and user preference are incorporated to formulate the user.
168]では、「ここにあるユーザーの過去のやりとりがある： ...、彼の好みは以下の通りです： ...、推奨を提供してください。"は、生成モデルを導くために使用され、過去の相互作用とユーザーの好みがユーザーを定式化するために組み込まれる。
User’s historical interactions [56, 172].
ユーザーの過去の交流 [56, 172]。
Serving as the implicit user feedback on items, user’s historical interactions play a crucial role in representing user behavior [38] in recommender systems, which implicitly conveys user preference over items.
アイテムに対する暗黙のユーザーフィードバックとして機能し、ユーザーの過去のインタラクションは、アイテムに対するユーザーの嗜好を暗黙的に伝える推薦システムにおいて、ユーザーの行動[38]を表現する上で重要な役割を果たす。
To present the historical interactions, i.e., the sequence of interacted items, one common practice is to utilize the item ID to form the interaction sequence [33, 47].
過去のインタラクション、すなわちインタラクションされたアイテムのシーケンスを表示するために、一般的なプラクティスの1つは、インタラクションシーケンスを形成するためにアイテムIDを利用することである[33, 47]。
Nevertheless, as pointed out by [161], generative models face limitations in capturing collaborative information while excelling in capturing nuanced item semantics.
とはいえ、[161]によって指摘されているように、生成モデルは、ニュアンスに富んだアイテムのセマンティクスを捉えることに優れている一方で、コラボレーション情報を捉えることには限界がある。
Therefore, two categories of work emerge to further improve the recommendation accuracy.1) To better leverage the strong semantics understanding of LLMs, a line of work [18, 22, 43, 56, 90] attempts to integrate rich side information of items in historical interactions.
1)LLMの強力なセマンティクス理解をより活用するために、一連の研究[18, 22, 43, 56, 90]は、過去の相互作用におけるアイテムの豊富な側面情報を統合することを試みている。
In particular, [22, 87] incorporates item descriptions when listing the user’s historical interactions.
特に、[22, 87]は、ユーザーの過去のインタラクションをリストアップする際に、アイテムの説明を組み込んでいる。
[82] utilizes item titles and item attributes to exploit the rich semantics of items for a better understanding of user preference.2) To strengthen the collaborative information understanding of LLMs, another line of work aims to incorporate ID embeddings of the interacted items for LLMs to understand user behavior.
[2）LLMの協調的な情報理解を強化するために、LLMの対話アイテムのIDエンベッディングを組み込んでユーザーの行動を理解することを目的とした別の研究がある。
For example, LLaRA [79] additionally includes ID embedding after the title’s token embedding to represent each item in historical interactions.
例えば、LLaRA [79]は、タイトルのトークン埋込みの後にID埋込みを追加して、過去のインタラクションの各アイテムを表現している。
Moreover, with the advancements in multimodal LLMs, some work [34, 90] attempts to incorporate multimodal feature of the item, e.g., visual features, to complement the textual user’s historical interactions.
さらに、マルチモーダルLLMの進歩に伴い、いくつかの研究[34, 90]では、テキストによるユーザーの歴史的インタラクションを補完するために、アイテムのマルチモーダル特徴、例えば視覚的特徴を組み込むことを試みている。
User profile [31, 92].
ユーザープロファイル [31, 92]。
To enhance the user modeling, integrating user profile (e.g., demographic and preference information about the user) is an effective way to model the user characteristics in recommender systems [136].
ユーザーモデリングを強化するために、ユーザープロファイル（例えば、ユーザーに関する人口統計学的情報や嗜好情報）を統合することは、推薦システムにおいてユーザー特性をモデル化する効果的な方法である[136]。
In most cases, user’s demographic information (e.g., gender) can be obtained directly from the online recommendation platform.
ほとんどの場合、ユーザーの人口統計学的情報（性別など）は、オンライン・レコメンデーション・プラットフォームから直接得ることができる。
Such user information is then combined with descriptional text, e.g., “User description: female, 25-34, and in sales/marketing” [154].
このようなユーザー情報は、記述的なテキストと組み合わされる： 女性、25～34歳、営業/マーケティング」[154]。
For instance, [31] utilizes user’s age and gender to prompt ChatGPT to enhance its comprehension of user characteristics based on encoded prior knowledge.
例えば、[31]はユーザーの年齢と性別を利用し、エンコードされた事前知識に基づいて、ChatGPTがユーザーの特性を理解するよう促しています。
Although demographic information can implicitly reflect the general preference within specific user groups (e.g., teenagers), it can further enrich models’ comprehension of the user by explicitly detailing user’s general preference and current intention during user formulation.
人口統計学的情報は、特定のユーザーグループ（例えば、ティーンエイジャー）における一般的な嗜好を暗黙的に反映することができますが、ユーザーの一般的な嗜好と現在の意図を明示的に詳細化することで、ユーザーに対するモデルの理解をさらに深めることができます。
To obtain the explicit general preference and current intention, [168] proposes to leverage LLMs to infer the user intention and the general preference based on the user’s historical interactions using tailored prompts.
明示的な一般的嗜好と現在の意図を得るために、[168]はLLMを活用し、テーラードプロンプトを使用したユーザーの過去のインタラクションに基づいて、ユーザーの意図と一般的嗜好を推測することを提案している。
Besides, [174] uses LLMs to summarize user preference based on the user’s historical interactions.
さらに、[174]はLLMを使って、ユーザーの過去のインタラクションに基づいてユーザーの嗜好を要約している。
However, acquiring user profiles can be challenging due to user privacy concerns, leading some studies to employ user ID to capture the collaborative information [33] or discard user profile for user formulation [112].
しかし、ユーザープロファイルを取得することは、ユーザーのプライバシーの懸念のために困難である可能性があり、いくつかの研究は、協調情報をキャプチャするためにユーザーIDを採用したり[33]、ユーザー定式化のためにユーザープロファイルを破棄したりする[112]。
Context information [88, 161].
コンテキスト情報 [88, 161]。
In addition to user’s historical interactions and profile, environmental context information (e.g., location and time), which can influence user decisions, is also advantageous for models to better match the users with appropriate items.
ユーザーの過去のインタラクションやプロファイルに加え、ユーザーの意思決定に影響を与える可能性のある環境コンテキスト情報（例えば、場所や時間）も、適切なアイテムとユーザーをより良くマッチングさせるモデルにとって有利である。
For example, users may prefer to purchase a coat rather than a T-shirt in winter in clothing recommendation.
例えば、ユーザーは冬にTシャツを購入するよりも、コートを購入したがるかもしれない。
Therefore, incorporating context information such as time, can achieve effective user understanding in real-world application scenarios.
したがって、時間などのコンテキスト情報を組み込むことで、実世界のアプリケーションシナリオにおいて効果的なユーザー理解を実現することができる。
For instance, [88] harnesses diagnosis and procedures for medication recommendation while [161] incorporates context information via learnable soft prompt to capture unobserved context signals.
例えば、[88]は診断と手順を薬の推薦に利用し、[161]は学習可能なソフトプロンプトを介してコンテキスト情報を組み込み、未観測のコンテキスト信号を捕捉する。
External knowledge [28].
外部の知識[28]。
Although generative models have demonstrated promising performance in recommendation tasks based on user-associated information, recent research has explored leveraging external knowledge to enhance the performance of generative recommender models.
生成モデルは、ユーザー関連情報に基づく推薦タスクにおいて有望な性能を示してきたが、最近の研究では、生成推薦モデルの性能を向上させるために外部知識を活用することが検討されている。
To harness structured information from user-item graph, [28] integrates the graph data in natural language and further propagates higher-order neighbor’s information to capture complex relations between users and items.
ユーザーとアイテムのグラフから構造化された情報を利用するために、[28]はグラフデータを自然言語で統合し、さらに高次の近傍情報を伝播して、ユーザーとアイテムの間の複雑な関係を捕捉する。
Additionally, [93] leverages external knowledge from conventional recommender models by incorporating prediction from these models in natural language, showcasing collaborative efforts from both conventional models and generative models.
さらに、[93]は、従来のレコメンダーモデルからの予測を自然言語に組み込むことによって、従来のレコメンダーモデルからの外部知識を活用し、従来のモデルと生成モデルの両方からの協調的な取り組みを示している。
Some work also incorporates an item candidate set to reduce the searching space of the whole item set, thus alleviating the hallucination problem and improving the accuracy [23, 168].
また、項目候補集合を組み込んで、項目集合全体の検索空間を縮小することで、幻覚問題を緩和し、精度を向上させた研究もある[23, 168]。

## 5.3. Item Identifiers アイテム識別子

Similar to generative search, the generative recommender models are expected to generate relevant items given the user formulation.
生成的検索と同様に、生成的レコメンダーモデルは、ユーザーの定式化によって関連するアイテムを生成することが期待される。
Nevertheless, items in recommendation platforms usually consist of various side information from different modalities, e.g., thumbnails of the micro-videos, audios of the music, and titles of the news.
とはいえ、レコメンデーション・プラットフォームのアイテムは通常、マイクロビデオのサムネイル、音楽のオーディオ、ニュースのタイトルなど、異なるモダリティからのさまざまなサイド情報で構成されている。
As such, the complex data from the items in recommendation necessitates item identifiers to present each item’s characteristics in the language space for generative recommendation.
このように、レコメンデーションにおけるアイテムからの複雑なデータは、生成的レコメンデーションのための言語空間における各アイテムの特徴を提示するためのアイテム識別子を必要とする。
It is highlighted that a good item identifier should at least meet two criteria as pointed out in [82]: 1) distinctiveness to emphasize the salient item features learned from user behaviors.
良いアイテム識別子は、[82]で指摘されているように、少なくとも2つの基準を満たすべきであることが強調されている： 1) ユーザーの行動から学んだ顕著なアイテムの特徴を強調する識別性。
And 2) semantics to focus on the utilization of prior knowledge in pre-trained language models, which facilitates strong generalization to cold-start and cross-domain recommendation.
また、2）セマンティクスは、事前に訓練された言語モデルにおける事前知識の活用に焦点を当て、コールドスタートやクロスドメイン推薦への強力な汎化を促進する。
Existing work usually constructs the item identifiers in the following four strategies, meeting different criteria accordingly.
既存の研究は通常、以下の4つの戦略でアイテム識別子を構築し、それに応じて異なる基準を満たす。
Numeric ID [11, 13, 33, 45, 67, 104, 109, 122, 149, 165].
数値ID [11、13、33、45、67、104、109、122、149、165]。
Given the widely demonstrated efficacy of numeric IDs for capturing collaborative information in traditional recommendation models [172], a straightforward strategy in generative recommendation frameworks is to adopt the strategy of using numeric IDs to represent items [33, 78].
従来の推薦モデル[172]において、協調情報を捕捉するための数値IDの有効性が広く実証されていることを考えると、生成的推薦フレームワークにおける単純な戦略は、アイテムを表現するために数値IDを使用する戦略を採用することである[33, 78]。
However, directly adopting the ID setting in traditional recommender models is infeasible in generative recommender models.
しかし、従来の推薦モデルにおけるID設定を直接採用することは、生成的推薦モデルでは不可能である。
Because traditional recommender models consider each item as an independent “token”, which cannot be further tokenized and strictly refers to one independent embedding.
というのも、従来のレコメンダー・モデルは、各アイテムを独立した「トークン」とみなしており、さらにトークン化することはできず、厳密には1つの独立した埋め込みを指すからである。
This requires adding all the independent tokens into the model, which requires 1) large memory to store every item embedding, and 2) sufficient interactions for training the item embedding.
これは、すべての独立したトークンをモデルに追加する必要があり、1）すべてのアイテム埋め込みを格納するための大きなメモリと、2）アイテム埋め込みのトレーニングのための十分なインタラクションを必要とする。
To combat these issues, generative recommender models offer a promising solution by designing the item identifier as a token sequence, where the numeric IDs can be further tokenized and are associated with several token embeddings.
これらの問題に対処するために、生成レコメンダーモデルは、アイテム識別子をトークン列として設計することによって、有望な解決策を提供する。
As such, a token sequence as a numeric ID makes it possible to use finite tokens to represent infinite items [46, 68].
このように、トークン列を数値IDとして使用することで、有限のトークンを使用して無限のアイテムを表現することが可能になる[46, 68]。
To effectively represent an item with a numeric ID in a token sequence, previous work explores different strategies for ID assignment [47].
トークンシーケンスで数値IDを持つアイテムを効果的に表現するために、先行研究ではID割り当てのためのさまざまな戦略が研究されている[47]。
In [33], sequential indexing is utilized to capture the collaborative information in an intuitive way.
33]では、直感的な方法で協調情報を捕捉するために逐次索引付けが利用されている。
Specifically, sequential indexing represents the user’s items in chronological order by consecutive numeric IDs, (e.g., “11138”, “11139”, .
具体的には、シーケンシャル・インデックスは、連続する数字IDによって、ユーザーのアイテムを時系列に表す（例えば、"11138"、"11139"、...）。
..
..
, “11405”), which could capture the co-occurrence of items that are interacted with the same user.
11405")、同じユーザーとやりとりされたアイテムの共起を捕らえることができる。
However, such sequential indexing might suffer from the potential data leakage issue [47, 112].
しかし、このような逐次インデックス付けは、潜在的なデータ漏洩の問題に悩まされるかもしれない[47, 112]。
[47] fixes this potential issue and explores other non-trivial indexing methods that incorporate prior information on the items, such as semantics and collaborative knowledge.
[47]は、この潜在的な問題を修正し、セマンティクスや協調的知識などのアイテムに関する事前情報を組み込んだ、他の自明でないインデックス作成方法を探求している。
By constructing IDs based on item categories in a hierarchical structure, the items belonging to the same categories will have similar IDs and are validated to be effective in generative recommendation.
アイテムのカテゴリを階層構造にしてIDを構成することで、同じカテゴリに属するアイテムは類似したIDを持つことになり、生成推薦に有効であることが検証されている。
Similarly, SEATER [122] proposes a tree-based hierarchical identifier with numeric IDs, where items with similar interactions will have similar IDs.
同様に、SEATER [122]は、数値IDを持つツリーベースの階層識別子を提案しており、類似した相互作用を持つアイテムは類似したIDを持つことになる。
In addition, [47] also attempts to construct IDs based on the item co-occurance matrix, where items that co-occur more times will have more similar IDs, which is assessed to be beneficial in generating appropriate recommendation.
さらに、[47]では、アイテムの共起行列に基づいてIDを構成することも試みられており、共起回数が多いアイテムはより類似したIDを持つことになり、適切な推薦を生成する上で有益であると評価されている。
Despite the effectiveness of distinctive numeric IDs in generative recommendation, it usually lacks semantic information, thus suffering from the cold-start problem [82] and failing to leverage the world knowledge encoded in the recently emerged powerful generative models, e.g., LLMs.
生成的推薦における特徴的な数値IDの有効性にもかかわらず、それは通常、意味的情報を欠いているため、コールドスタート問題[82]に悩まされ、最近出現した強力な生成モデル、例えばLLMにエンコードされた世界知識を活用することができない。
Item’s textual meta data [4, 27, 37, 80, 85, 94, 127, 140, 148, 160, 162, 167].
アイテムのテキスト・メタデータ [4, 27, 37, 80, 85, 94, 127, 140, 148, 160, 162, 167]。
To overcome the absence of semantics in numeric IDs, other work [4, 56] utilizes the item’s textual metadata, e.g., item title, leveraging the LLMs’ world knowledge encoded in the parameters to better comprehend the item characteristics based on the semantics in the item’s textual descriptions.
数値IDのセマンティクスの欠如を克服するために、他の研究[4, 56]では、アイテムのテキストメタデータ、例えばアイテムのタイトルを利用し、アイテムのテキスト記述のセマンティクスに基づいてアイテムの特性をより良く理解するために、パラメータにエンコードされたLLMの世界知識を活用している。
For instance, [4, 43, 51, 79, 142, 171] use movie title, [18, 51, 66, 86, 90, 168] use the product name, [175] utilizes book name, [71, 72] adopt news title, [23] uses song title, [129] employs abstractive text of items, and [22] includes both title and descriptions of online products, as the item identifier for recommendation.
例えば、[4, 43, 51, 79, 142, 171]は映画のタイトルを、[18, 51, 66, 86, 90, 168]は商品名を、[175]は書籍名を、[71, 72]はニュースのタイトルを、[23]は曲名を、[129]はアイテムの抽象的なテキストを、[22]はオンライン商品のタイトルと説明文の両方をアイテム識別子としてレコメンデーションに利用している。
Although leveraging an item’s textual metadata significantly alleviates the cold-start issue [4, 82], it is still suboptimal for effective recommendation.
アイテムのテキストメタデータを活用することで、コールドスタートの問題はかなり軽減されるが [4, 82]、それでも効果的な推薦には最適ではない。
The textual metadata, especially the descriptions could be very lengthy, which would cause out-of-corpus issues, i.e., the generated token sequence could not match any valid item identifier.
テキストのメタデータ、特に説明文は非常に長くなる可能性があり、コーパス外の問題、つまり生成されたトークン列が有効なアイテム識別子にマッチしない可能性がある。
Although grounding the generated tokens to existing items via distance-based methods is a potential solution to address this problem [4], it would take us back to deep learning-based recommendation since we need to calculate the matching score between the generated item and each in-corpus item [68].
生成されたトークンを距離ベースの手法で既存のアイテムに接地することは、この問題に対処するための潜在的な解決策ではあるが[4]、生成されたアイテムとコーパス内の各アイテムのマッチングスコアを計算する必要があるため、ディープラーニングベースの推薦に戻ることになる[68]。
Codebook [112].
コードブック[112]。
To simultaneously leverage the semantics while pursuing a unique short token sequence, [112] proposes to learn a codebook to construct the item identifier in generative recommendation.
ユニークな短いトークン列を追求しながら同時にセマンティクスを活用するために、[112]は生成的推薦においてアイテム識別子を構築するコードブックを学習することを提案している。
Similar to the codebook for document identifier in generative search, related work in recommendation [42, 42, 112] focuses on developing a codebook specifically for items.
生成的検索における文書識別子のコードブックと同様に、推薦[42, 42, 112]における関連研究は、アイテムに特化したコードブックの開発に焦点を当てている。
Typically, RQ-VAEs [163] are utilized to learn the codebook, where the input is the item’s semantic representation extracted from a pre-trained language model (e.g., LLaMA [134]) and the output is the generated token sequence.
典型的には、RQ-VAE [163]がコードブックの学習に利用され、入力は事前に学習された言語モデル（例えば、LLaMA [134]）から抽出されたアイテムの意味表現であり、出力は生成されたトークン列である。
The overall process of training codebook is similar to that in generative search, as discussed in Section 4.3.Along this line, TIGER [112] is a representative work that generates an item’s semantic ID based on the item’s textual descriptions via the codebook.
コードブックを学習する全体的なプロセスは、4.3節で議論したように、生成的検索におけるプロセスと似ている。このラインに沿って、TIGER [112]は、コードブックを介してアイテムのテキスト記述に基づいてアイテムのセマンティックIDを生成する代表的な作品である。
LC-Rec [173] further enhances the generated ID’s representation to align with user preference and semantics of the item’s textual descriptions.
LC-Rec [173]はさらに、生成されたIDの表現をユーザーの好みとアイテムのテキスト記述のセマンティクスに沿うように強化する。
However, while codebook-based identifiers meet both semantics and distinctiveness, they suffer from the misalignment between the semantics correlation and interaction correlation.
しかし、コードブックベースの識別子は、意味性と識別性の両方を満たす反面、意味相関と相互作用相関のズレに悩まされる。
Specifically, the codebooks essentially capture the correlation of the item semantics into the identifier, i.e., items with similar semantics will have similar identifiers.
具体的には、コードブックは本質的に、アイテムのセマンティクスと識別子の相関をキャプチャする。
The identifier representations will then be optimized to capture interaction correlation by training on recommendation data.
その後、推薦データで訓練することにより、相互作用の相関を捉えるように識別子表現を最適化する。
Nevertheless, the items with similar codes might not necessarily have similar interactions, thereby hurting the learning of user behavior.
とはいえ、似たようなコードを持つアイテムが必ずしも似たようなインタラクションを持つとは限らないため、ユーザー行動の学習に支障をきたす。
Multi-facet identifier [82].
多面的識別子[82]。
To overcome the issues in previous identifier strategies, the multi-facet identifier is proposed.
これまでの識別子戦略の問題点を克服するために、多面的な識別子が提案されている。
Multifacet identifier aims to pursue both semantics and distinctiveness while mitigating the misalignment between semantics correlation and interaction correlation.
多面的識別子は、意味相関と相互作用相関のずれを緩和しながら、意味性と識別性の両方を追求することを目指している。
While incorporating semantics (e.g., item title) exploits the world knowledge encoded in generative models, utilizing unique numeric IDs ensures distinctiveness for capturing the essential collaborative information.
セマンティクス（アイテムのタイトルなど）を組み込むことで、生成モデルにエンコードされた世界の知識を利用することができる一方、一意の数値IDを利用することで、本質的なコラボレーション情報をキャプチャするための識別性を確保することができる。
Additionally, to avoid the lengthy issue of textual metadata, TransRec [82] allows the generation of the substring of metadata.
さらに、テキストメタデータの長い問題を避けるために、TransRec [82]ではメタデータの部分文字列の生成が可能である。
The utilization of substring follows the one-to-many corresponding as discussed in Section 4.3, thus might decrease the inference efficiency.
部分文字列の利用は、セクション4.3で議論したように、一対多の対応に従うため、推論効率を低下させる可能性がある。
Item identifier summary.
項目識別子の概要。
We summarize the characteristics of different types of item identifiers in Table 3 from different aspects, including semantics, distinctiveness, update, and the involved training process.
異なるタイプのアイテム識別子の特徴を、セマンティクス、識別性、更新、学習プロセスなど、さまざまな側面から表3にまとめる。
From the summary, we can find that 1) Incorporating semantics enables better utilization of world knowledge in generative language models and easier identifier update.
要約から、1）意味論を取り入れることで、生成言語モデルにおいて世界の知識をより有効に活用でき、識別子の更新が容易になる。
This can contribute to improved generalization and practicality in real-world deployments.2) Codebook and multi-facet identifiers achieve both semantics and distinctiveness, showing the potential to leverage semantics in pre-trained generative language models and learn collaborative information from user-item interactions.
2）コードブックとマルチファセット識別子は、セマンティクスと識別性の両方を実現し、事前に訓練された生成言語モデルでセマンティクスを活用し、ユーザーとアイテムの相互作用から協調情報を学習する可能性を示している。
Nevertheless, while codebook requires additional item-to-identifier training and auxiliary alignment to endow the generated identifier with the semantics in language models, multi-facet identifier is naturally advantageous to leverage both numeric ID and descriptions for improved generative recommendation.
とはいえ、コードブックでは、生成された識別子に言語モデルのセマンティクスを付与するために、項目間の学習や補助的なアラインメントを追加する必要がある。

## 5.4. Training トレーニング

Training the generative recommender models on the recommendation data involves two main steps, i.e., textual data construction and model optimization.
推薦データに対する生成的推薦モデルの学習には、主に2つのステップ、すなわちテキストデータの構築とモデルの最適化が含まれる。
The textual data construction converts the recommendation data into samples with textual input and output, where the choice of input and output depends on the learning objectives.
テキストデータ構築は、推薦データをテキスト入力とテキスト出力のサンプルに変換するもので、入力と出力の選択は学習目的に依存する。
While most of the methods can directly construct the textual data based on the pre-defined item identifier, codebookbased methods necessitate the item-to-identifier training prior to textual data construction.
ほとんどの手法は、事前に定義された項目識別子に基づいて直接テキストデータを構築することができるが、コードブックベースの手法は、テキストデータを構築する前に項目対識別子の学習が必要である。
The item-to-identifier training typically utilizes RQ-VAE to map the item content representation into the quantized code words [112] as the item identifier.
項目から識別子への学習は、通常、RQ-VAEを利用して、項目の内容表現を項目識別子として量子化された符号語[112]にマッピングする。
As for model optimization, literature typically utilizes generative training in language modeling [64] to optimize the model.
モデルの最適化に関しては、言語モデリングにおける生成学習[64]を利用してモデルを最適化する文献が一般的である。
Specifically, given the constructed samples with the textual input and output, the generative training maximizes the log-likelihood of the target output tokens conditioned on the input.
具体的には、テキストの入力と出力で構成されたサンプルが与えられると、生成学習は、入力を条件としてターゲット出力トークンの対数尤度を最大化する。
According to the learning objectives, we divide the generative training into two groups for generative recommendation.
学習目的に応じて、生成トレーニングは生成推薦のための2つのグループに分けられる。
To recommend the item relevant to the user preference, 1) user-to-identifier training is employed for generative models to learn the matching ability.
ユーザーの嗜好に合ったアイテムを推薦するために、1)マッチング能力を学習するための生成モデルに、ユーザー対識別子の学習を採用する。
For each constructed training sample, the input is the user formulation, and the output is the next-item identifier.
構築された各訓練サンプルについて、入力はユーザーの定式化であり、出力は次の項目の識別子である。
The user-to-identifier training plays a crucial role in the generative recommendation and is utilized across all generative recommendation methods for item retrieval.
ユーザー対識別子の学習は、生成的推薦において重要な役割を果たし、アイテム検索のためのすべての生成的推薦手法に利用されている。
As for the methods that utilize codebooks to learn semanticaware item identifiers, they might suffer from the semantic gap between the quantized codewords and the semantics in natural language.
意味を意識した項目識別子を学習するためにコードブックを利用する方法については、量子化されたコードワードと自然言語の意味との間の意味的ギャップに悩まされるかもしれない。
To combat this issue, 2) auxiliary alignment is additionally used by the methods to strengthen the alignment between the item content and the item identifier.
この問題に対処するため、2)補助的アライメントが追加的に使用され、項目内容と項目識別子の間のアライメントが強化される。
To achieve the alignment, extra training sample construction is required, which can be broadly divided into two groups.
アライメントを達成するためには、余分なトレーニングサンプルの構築が必要であり、それは大きく2つのグループに分けられる。
(i) Content-to-identifier or identifier-to-content.
(i) コンテンツ対識別子、または識別子対コンテンツ。
For each constructed training sample, the input-output pair comprises the identifier and textual content of the same item, each serving interchangeably as input or output.
構築された各トレーニングサンプルについて、入力と出力のペアは、同じ項目の識別子とテキストコンテンツで構成され、それぞれが入力または出力として交換可能に機能する。
In addition to the item-wise alignment, (ii) user-to-content is another strategy to implicitly align the item identifier and the item content by pairing the user formulation with the next-item content [173].
項目ごとの整列に加え、(ii)ユーザー対コンテンツは、ユーザー定式化と次の項目コンテンツを対にすることで、項目識別子と項目コンテンツを暗黙的に整列させるもう一つの戦略である[173]。
Despite the effectiveness of various training strategies in adapting the generative models to recommendation tasks, the training costs are usually unaffordable, especially for LLMs such as LLaMA.
生成モデルを推薦タスクに適応させるために様々な学習戦略が有効であるにもかかわらず、特にLLaMAのようなLLMの場合、学習コストは通常手が出ない。
To improve training efficiency, recent efforts have focused on model architecture modification [99] and data pruning for LLM-based recommendation [83, 93].
学習効率を向上させるために、最近ではモデル・アーキテクチャの修正[99]やLLMベースの推薦のためのデータ刈り込み[83, 93]に焦点が当てられている。

## 5.5. Inference 推論

To achieve item recommendation, the generative models perform generation grounding during the inference stage [82].
項目推薦を実現するために、生成モデルは推論段階で世代グラウンディングを行う[82]。
Given the user formulation in natural language, the generative models first generate the item identifier autoregressively via beam search.
自然言語によるユーザー定式化が与えられると、生成モデルはまず、ビーム探索によって項目識別子を自己回帰的に生成する。
Here, we divide the generation into two types, i.e., free generation and constrained generation.
ここでは、自由生成と制約生成の2種類に分けている。
As for the free generation, for each generation step, the model searches over the whole vocabulary and selects the top-𝐾 tokens with high probability as the subsequent input for the next step’s generation.
自由生成に関しては、各生成ステップで語彙全体を検索し、次のステップの生成のための入力として、高い確率で上位ᵃトークンを選択する。
However, searching over the whole vocabulary would probably result in out-of-corpus identifier [47, 68], making the recommendation invalid.
しかし、語彙全体を検索すると、おそらくコーパス外の識別子が見つかり [47, 68]、推奨が無効になる。

To address this problem, early studies utilize exact matching for grounding, which conducts free generation and simply discards the invalid identifier.
この問題に対処するため、初期の研究では、自由な生成を行い、単に無効な識別子を破棄する、接地用の完全一致を利用していた。
Nevertheless, they still have poor accuracy caused by the invalid identifier, especially for the textual metadatabased identifier.
それにもかかわらず、特にテキストメタデータに基づく識別子の場合、無効な識別子に起因する精度の低さが依然として残っている。
To improve the accuracy, BIGRec [4] proposes to ground the generated identifier to the valid items via L2 distance between the generated token sequences’ representations and the item representation.
精度を向上させるために、BIGRec [4]は、生成された識別子を、生成されたトークン列の表現とアイテムの表現との間のL2距離によって、有効なアイテムに接地することを提案している。
As such, each generated identifier is ensured to be grounded to valid item identifiers.
このように、生成された各識別子は、有効なアイテム識別子に接地していることが保証される。
In the same period, constrained generation is also explored in generation grounding [20, 47, 82, 112, 173].
同時期に、制約付き発電は、発電の接地においても検討されている[20, 47, 82, 112, 173]。
[20] and [47] propose to utilize Trie for constrained generation, where the generated identifier is guaranteed to be valid identifiers.
[20]と[47]は、生成された識別子が有効な識別子であることを保証する制約付き生成にTrieを利用することを提案している。
However, Trie strictly generates the valid identifier from the first token, where the accuracy of the recommendation depends highly on the accuracy of the first several generated tokens.
しかし、Trieは厳密に最初のトークンから有効な識別子を生成するため、推薦の精度は最初に生成されたトークンの精度に大きく依存する。
To combat this issue, TransRec [82] utilizes FM-index to achieve position-free constrained generation, which allows the generated token from any position of the valid identifier.
この問題に対処するために、TransRec [82]はFM-indexを利用して、有効な識別子の任意の位置から生成されたトークンを許可する、位置の制約のない生成を実現している。
The generated valid tokens will then be grounded to the valid identifiers through aggregations from different views.
生成された有効なトークンは、異なるビューからの集約によって有効な識別子にグラウンディングされる。
In addition to the typical recommendation that requires valid generation to recommend the existing items to the users, another research direction capitalizes on the generative capabilities of models to create entirely new item [22, 151, 157].
既存のアイテムをユーザーに推薦するために有効な生成を必要とする典型的な推薦に加えて、別の研究方向は、全く新しいアイテムを作成するためにモデルの生成能力を利用する[22, 151, 157]。
For example, [157] generates personalized outfits, which can serve as guidance for fashion factories.
例えば、[157]はパーソナライズされた服装を生成し、ファッション工場のガイダンスとして機能させることができる。
Consequently, within this research line, free generation is employed, enabling recommender systems to fully exploit the generative potential.
その結果、この研究ラインでは自由な生成が採用され、レコメンダー・システムが生成の可能性を十分に活用できるようになっている。

## 5.6. Summary 要約

Methods summary.
方法の要約。
We summarize current generative recommendation methods in Table 4, from the aspects of user formulation, item identifier, backbone, generation, dataset, and recommendation domain.1) User formulation.
現在の生成的推薦法を、ユーザー定式化、アイテム識別子、バックボーン、生成、データセット、推薦ドメインの側面から表4にまとめる。
Different components in user formulation have been discussed in Section 5.2.It is noticed that existing methods usually incorporate task description and user’s historical interactions, while some methods also leverage user profile, context information, and external knowledge as additional components to formulate user.2) Item identifier.
既存の方法は通常、タスク記述とユーザーの過去のインタラクションを組み込んでいるが、いくつかの方法はユーザープロファイル、コンテキスト情報、外部知識もユーザーを定式化する追加コンポーネントとして活用している。
We summarize the characteristics of item identifiers in Table 3, where each type of identifier meets different criteria of the item identifier as discussed in Section 5.3.In addition, as shown in Table 4, we can find that methods that employ LLMs of larger size would usually utilize textual metadata as item identifier.
さらに、表4に示すように、より大きなサイズのLLMを採用する方法は、通常、アイテム識別子としてテキストメタデータを利用することがわかる。
This is to leverage the rich world knowledge encoded in the LLMs, for a better understanding of user behavior and item characteristics.
これは、LLMにエンコードされた豊富な世界知識を活用し、ユーザーの行動やアイテムの特性をより深く理解するためである。
With the exploration on various recommendation datasets across different domains, generative recommendation methods show great applicability and generalization ability for real-world applications.
様々な領域にわたる様々な推薦データセットでの調査により、生成的推薦手法は実世界のアプリケーションに大きな適用性と汎化能力を示している。
Timeline summary.
タイムラインの要約。
As discussed in Section 5.1, item identifier is a pivotal component in generative recommendation.
セクション5.1で述べたように、アイテム識別子は生成的推薦において極めて重要な要素である。
To elucidate the evolution of item identifiers in the context of generative recommendation, we provide a brief timeline to outline significant milestones across four distinct types of identifiers.
生成的推薦の文脈におけるアイテム識別子の進化を明らかにするために、4つの異なるタイプの識別子における重要なマイルストーンを概説する簡単な年表を提供する。
For each type of identifier, we highlight the first work and enumerate several subsequent endeavors for further improvements in another dimension such as training strategies.
各タイプの識別子について、最初の研究に焦点を当て、トレーニング戦略など別の次元でのさらなる改良のためのその後の試みをいくつか列挙する。
The earliest effort in generative recommendation is LMRecSys, which employs the generative paradigm for recommendation and utilizes the item’s textual metadata, i.e., title, as the item identifier.
生成的レコメンデーションにおける最も初期の取り組みはLMRecSysであり、レコメンデーションに生成的パラダイムを採用し、アイテムの識別子としてアイテムのテキストメタデータ、すなわちタイトルを利用している。
In the year 2022, P5 introduces the numeric ID identifier and proposes a unified generative recommendation framework with multi-task training.
2022年、P5は数値ID識別子を導入し、マルチタスク学習による統一的な生成推薦フレームワークを提案する。
Subsequently, the year 2023 has witnessed various investigations of improved numeric ID-based identifiers, such as RecSysLLM with masked language modeling [20], and SEATER with tree-based numeric IDs [122].
その後、2023年には、マスクされた言語モデリングを用いたRecSysLLM[20]や、ツリーベースの数値IDを用いたSEATER[122]など、数値IDベースの識別子の改良に関するさまざまな研究が行われている。
In late 2023, [82] introduces multi-facet identifier to pursue both semantics and distinctiveness.
2023年後半、[82]はセマンティクスと識別性の両方を追求するためにマルチファセット識別子を導入する。
It is highlighted that from year 2023 onwards, especially after the birth of ChatGPT, generative recommendation has garnered increased attention.
特にChatGPTが誕生した2023年以降、ジェネレーティブ・レコメンデーションへの注目が高まっていることが浮き彫りになった。
In this period, there has been extensive research work to enhance generative recommendation with the four different identifier types, including training strategies (e.g., GenRec [51] and BIGRec [4]), user formulation (e.g., InstructRec [168]), constrained generation (e.g., TransRec [82]), and training efficiency (e.g., DEALRec [83]).
この間、GenRec[51]やBIGRec[4]のような学習戦略、InstructRec[168]のようなユーザー定式化、TransRec[82]のような制約生成、DEALRec[83]のような学習効率といった4つの異なる識別子を用いた生成的推薦を強化するための研究が幅広く行われてきた。

## 5.7. LLMs for Recommendation beyond Generative Recommendation 生成的レコメンデーションを超えるレコメンデーションのためのLLM

LLMs as feature extractors.
特徴抽出器としてのLLM。
In addition to the generative recommendation that autoregressively generates the item identifier, another concurrent line of research work focuses on the utilization of LLMs in data representation [96, 114, 141].
項目識別子を自己回帰的に生成する生成的推薦に加えて、同時並行的に行われているもう一つの研究ラインは、データ表現におけるLLMの活用に焦点を当てている[96, 114, 141]。
Two approaches are commonly used in this line of work.1) Utilization of LLMs to obtain augmented features for traditional recommender models [8, 95, 128, 154], and 2) incorporation of a linear projector at the last token to predict the probability scores of all items [36, 69, 141], which is equivalent to using the LLMs’ hidden states as user representation.
これはLLMの隠れ状態をユーザ表現として使用することと同じである[36, 69, 141]。
Although item identifier is not explicitly utilized, it is highlighted that this line of work constructs user formulation to obtain the user representation or augmented features.
項目識別子は明示的に利用されていないが、この研究では、ユーザー表現または拡張機能を得るためにユーザー定式化を構築していることが強調されている。
We also include the related work into the discussion of user formulation in Section 5.2.LLMs for CTR tasks.
また、セクション5.2.CTRタスクのためのLLMのユーザー定式化の議論に関連研究を含める。
While extensive effort has been made to explore next-item generation, researchers have also investigated utilizing LLMs for the Click Through Rate (CTR) task.
ネクストアイテム生成の研究にも多大な努力が払われているが、研究者はクリック率（CTR）タスクにLLMを利用することも研究している。
The CTR task aims to predict the user-item interaction in a pointwise manner [23], i.e., the input is the information of the user and the target item.
CTRタスクの目的は、ユーザーとアイテムの相互作用をポイントワイズで予測することである[23]。
To leverage LLMs for CTR tasks, existing work usually takes the user formulation and the information of target item as the input, and the target output will be set as “yes” or “no”, for the positive and negative samples, respectively.
CTRタスクにLLMを活用するために、既存の研究では通常、ユーザの定式化と対象アイテムの情報を入力とし、肯定的なサンプルと否定的なサンプルに対してそれぞれ「はい」または「いいえ」と設定する。
During inference, these methods will perform softmax on the two tokens at the output layer, “yes” and “no”, and take the probability score of “yes” as the final prediction score [5, 172].
推論中、これらの方法は出力層で "yes "と "no "の2つのトークンに対してソフトマックスを実行し、"yes "の確率スコアを最終的な予測スコアとする[5, 172]。
In this survey, we mainly focus on the next item generation because of its practical promise in industrial recommender systems.
本調査では、産業用レコメンダーシステムにおける実用的な有望性から、主に次の項目生成に焦点を当てる。
It has the potential to reduce the typical multiple-stage item ranking into one stage, i.e., directly generating items to recommend.
これは、典型的な複数段階のアイテム・ランキングを1段階、つまり推薦するアイテムを直接生成する段階に減らす可能性がある。
As for the LLMs for CTR tasks, we also discuss them in user formulation in Section 5.2.
CTRタスクのLLMに関しては、セクション5.2のユーザー定式化でも議論する。

# 6. Discussion 議論

## 6.1. Difference Between Generative Search and Recommendation 生成的検索と推薦の違い

In the preceding sections, we primarily outline the commonalities between generative search and generative recommendation, and summarize a universal framework to present the current works.
前節では、主に生成的検索と生成的推薦の共通点を概説し、普遍的なフレームワークをまとめ、現在の研究成果を紹介する。
However, given the distinct nature of their tasks, there are also numerous points of differentiation between the two and unique challenges to address, respectively.
しかし、両者の任務の性質が異なることから、両者には多くの相違点があり、それぞれ取り組むべき独自の課題も存在する。
Varied input length of generative search and recommendation.
生成的検索と推薦の多様な入力長。
Generative search typically involves short queries and minimal additional processes, while generative recommendation requires a crucial "user formulation" step.
生成的検索は通常、短いクエリーと最小限の追加プロセスを含むが、生成的推薦には重要な「ユーザー定式化」ステップが必要である。
This presents unique challenges for generative recommendation.
これは、生成的推薦にとってユニークな課題を提示している。
Firstly, it is necessary to convert user information, such as task descriptions, historical interactions, and user profiles, into a textual sequence that preserves the original information as much as possible.
まず、タスクの説明、過去のやりとり、ユーザープロファイルなどのユーザー情報を、元の情報をできるだけ保存したテキストシーケンスに変換する必要がある。
Secondly, the user formulation often involves lengthy inputs.
第二に、ユーザー策定はしばしば長い入力を伴う。
We statistics the average input length for generative search and recommendation on typical datasets, respectively.
代表的なデータセットについて、生成的検索と推薦の平均入力長をそれぞれ統計した。
As shown in Figure 4 (a), the input tokens for generative recommendation are significantly greater than those for generative search.
図4(a)に示すように、生成的推薦の入力トークンは、生成的検索の入力トークンよりも有意に多い。
The lengthy input in generative recommendation demands significant computing resources for training and poses inference difficulties, particularly with large language models [83].
生成的推薦における長時間の入力は、トレーニングのために多大な計算資源を必要とし、特に大規模な言語モデルにおいては、推論に困難をもたらす[83]。
Consequently, the generative recommendation must confront the challenges posed by the extensive length of the input, which is different from generative search.
その結果、生成的推薦では、生成的探索とは異なる、入力の膨大な長さがもたらす課題に立ち向かわなければならない。

Differing interaction density in generative search and recommendation.
生成的検索と推薦における相互作用密度の違い。
One important distinction between search and recommendation tasks is the difference in interaction density.
検索タスクと推薦タスクの重要な違いの一つは、相互作用密度の違いである。
In search datasets, only a portion of documents are labeled with queries, while almost all items are interacted with by users (except for cold-start items).
検索データセットでは、クエリでラベル付けされるのは文書の一部だけで、ほとんどすべてのアイテムがユーザーによって操作される（コールドスタートアイテムを除く）。
According to the statistics in Figure 4 (b), each document is associated with less than one query, while items typically have more than ten interactions on average.
図4 (b)の統計によると、各文書が関連するクエリは1つ以下であるのに対し、アイテムは平均して10以上の相互作用を持っている。
As previously mentioned, the generative paradigm involves memorizing documents or items in their parameters and then generating them based on input queries or users.
前述したように、生成パラダイムは、文書や項目をパラメータに記憶し、入力クエリやユーザーに基づいてそれらを生成する。
In recommendation, the high interaction density ensures that each item can be trained, while most documents are not exposed to the generative search model.
レコメンデーションでは、相互作用密度が高いため、各項目の学習が可能である一方、ほとんどの文書は生成検索モデルにさらされない。
Consequently, generative recommendation can easily achieve comparable performance with traditional recommendation methods, whereas generative search struggles with low interaction density.
その結果、生成的レコメンデーションは従来のレコメンデーション手法に匹敵するパフォーマンスを容易に達成できるが、生成的サーチは低い相互作用密度で苦戦する。
The low interaction density presents unique challenges for generative search.
相互作用の密度が低いため、ジェネレーティブ・サーチには独特の課題がある。
Different “semantic” meanings in generative search and recommendation.
生成的検索と推薦における異なる「意味」。
In search, the relevance between a query and a document is closely tied to their semantic similarity.
検索において、クエリと文書の関連性は、その意味的類似性と密接に結びついている。
However, for recommendation, an item’s content is less significant compared to search, while collaborative information holds greater importance.
しかし、レコメンデーションにおいては、アイテムのコンテンツは検索に比べて重要度が低く、コラボレーション情報の重要度が高い。
In essence, there are distinct “semantic” implications in search and recommendation, leading to different requirements for identifiers in generative search and recommendation.
要するに、検索と推薦にはそれぞれ異なる「セマンティック」な意味合いがあり、生成的検索と推薦における識別子の要件は異なる。
In generative search, identifiers must accurately represent the document’s content, while in generative recommendation, they should emphasize the item’s collaborative information.
生成的検索では、識別子は文書の内容を正確に表現しなければならない。一方、生成的推薦では、識別子はアイテムの協調情報を強調しなければならない。
For instance, “learning to tokenize” a document’s content is effective in generative search [125], but additional collaborative information must be incorporated during the tokenization stage in generative recommendation.
例えば、文書の内容を「トークン化する学習」は生成的検索では効果的だが[125]、生成的推薦ではトークン化の段階でさらに協調的情報を組み込まなければならない。
This may be an expected research direction to further explore in generative recommendation.
これは、生成的レコメンデーションにおいてさらに探求すべき、期待される研究の方向性かもしれない。

## 6.2. Open Problems in Generative Search and Recommendation 生成的探索と推薦における未解決の問題

• Document and item update in LLMs.

- LLMの文書とアイテムの更新。
  After being trained on query-doc and use-item pairs, the LLM is capable of retrieving documents or recommending items to users by generating the corresponding identifiers.
  LLMは、クエリ・ドキュメントとユース・アイテムのペアで学習された後、対応する識別子を生成することで、ドキュメントを検索したり、ユーザーにアイテムを推薦したりすることができる。
  However, this functionality is dependent on the LLM having been trained to memorize the associations between the documents or items and their identifiers.
  しかし、この機能は、LLMが文書やアイテムとその識別子との関連を記憶するように訓練されていることに依存している。
  Consequently, the LLM is hard to retrieve or recommend new documents and items that it has not encountered during training.
  その結果、LLMはトレーニング中に出会ったことのない新しい文書やアイテムを検索したり推薦したりすることが難しくなる。
  While retraining the LLM on newly added documents or items is a potential solution, it necessitates a significant amount of computing resources.
  新しく追加された文書やアイテムに対してLLMを再トレーニングすることは、潜在的な解決策ではあるが、かなりの量のコンピューティング・リソースを必要とする。
  Given the vast number of new documents and items that are introduced daily in search and recommendation systems, it is crucial to develop effective and efficient methods for updating the LLM’s memory in order to ensure optimal generative search and recommendation performance [13, 98].
  検索や推薦システムにおいて、日々膨大な数の新しい文書やアイテムが導入されることを考えると、最適な生成的検索や推薦のパフォーマンスを確保するためには、LLMのメモリを更新するための効果的で効率的な方法を開発することが極めて重要である[13, 98]。
  • Multimodal and cross-modal generative search and recommendation.
- マルチモーダルおよびクロスモーダルな生成的検索と推薦。
  Only textual information cannot satisfy users’ various information needs well.
  文字情報だけでは、ユーザーのさまざまな情報ニーズを十分に満たすことはできない。
  To enhance the search experience, it is crucial to incorporate multimodal resources such as images, tables, audio, and videos alongside textual documents.
  検索体験を向上させるためには、テキスト文書とともに、画像、表、音声、動画などのマルチモーダルなリソースを組み込むことが極めて重要である。
  Similarly, recommendations should encompass various types of content, like micro-videos, which necessitate a comprehensive understanding of multimodal elements.
  同様に、レコメンデーションは、マルチモーダルな要素を包括的に理解する必要があるマイクロビデオのような様々なタイプのコンテンツを包含すべきである。
  Unfortunately, the current generative paradigm predominantly relies on language models and falls short in addressing multimodal information-seeking scenarios.
  残念なことに、現在の生成パラダイムは言語モデルに頼ることが多く、マルチモーダルな情報探索シナリオに対応するには不十分である。
  These scenarios include retrieving images, videos, or audio based on a query, performing generative multimodal retrieval by retrieving web pages containing both text and images, and providing multimodal recommendations that incorporate diverse features.
  これらのシナリオには、クエリに基づいて画像、ビデオ、またはオーディオを検索すること、テキストと画像の両方を含むウェブページを検索することによって生成的なマルチモーダル検索を実行すること、多様な特徴を組み込んだマルチモーダル推薦を提供することなどが含まれる。
  Some recent works [34, 73, 91] have made an initial attempt, and further works are anticipated.
  最近のいくつかの研究[34, 73, 91]が最初の試みを行っており、さらなる研究が期待されている。
  • In-context learning for generative search and recommendation.
- 生成的な検索と推薦のためのコンテキスト内学習。
  One notable advantage of Language Models (LLMs) is their ability to learn in-context.
  言語モデル（LLM）の特筆すべき利点のひとつは、イン・コンテキストで学習できることだ。
  With just a few examples (few-shot) or even no examples (zero-shot) provided in the prompt, LLMs can effectively solve specific tasks without the need for fine-tuning.
  LLMは、プロンプトで提供されるわずかな例（数ショット）、あるいは例がない（ゼロショット）だけで、微調整の必要なく、特定のタスクを効果的に解くことができる。
  In-context learning plays a crucial role in enabling LLMs to encompass a wider range of tasks within the same generative paradigm.
  インコンテクスト学習は、LLMが同じ生成パラダイムの中でより幅広いタスクを網羅できるようにする上で、重要な役割を果たしている。
  However, current generative search and recommendation methods still rely on fine-tuning LLMs using domain-specific data, including query-document pairs and user-item pairs.
  しかし、現在の生成的検索や推薦の手法は、クエリとドキュメントのペアやユーザーとアイテムのペアなど、ドメイン固有のデータを使ってLLMを微調整することに依存している。
  As the size of LLMs increases, the process of fine-tuning becomes computationally expensive.
  LLMのサイズが大きくなると、微調整のプロセスに計算コストがかかるようになる。
  Consequently, the challenge lies in finding ways to incorporate LLMs into search and recommendation domains using zero-shot or few-shot approaches, thereby reducing the need for extensive fine-tuning.
  その結果、LLMをゼロショットまたは数ショットのアプローチを使って検索や推薦のドメインに組み込む方法を見つけることが課題となり、それによって大規模な微調整の必要性を減らすことができる。
  • Large-scale recall.
- 大規模なリコール。
  Regardless of whether the objective is to provide users with a list of documents or items, generative search and recommendation methods typically employ beam search in autoregressive decoding to generate such lists instead of just a single result.
  ユーザーに文書やアイテムのリストを提供することが目的であろうとなかろうと、生成的検索や推薦の手法では、単一の結果ではなく、そのようなリストを生成するために、一般的に自己回帰復号におけるビーム検索を採用している。
  To illustrate, if the beam search has a size of 𝑘, generative search and recommendation systems can produce a list containing 𝑘 elements.
  例えるなら、ビーム検索がᑘのサイズを持つ場合、生成検索と推薦システムはᑘの要素を含むリストを生成することができる。
  However, the efficiency of autoregressive generation diminishes as the beam size 𝑘 increases.
  しかし、ビームサイズ↪L_1458↩が大きくなるにつれて、自己回帰生成の効率は低下する。
  Consequently, current generative search and recommendation systems are unable to achieve large-scale recall due to this limitation.
  その結果、現在の生成的検索・推薦システムは、この制限のために大規模な想起を達成することができない。
  Therefore, it is necessary to explore additional decoding strategies to enhance the performance of generative search and recommendation methods.
  そのため、生成的検索・推薦手法のパフォーマンスを向上させるためには、さらなるデコーディング戦略を探求する必要がある。

## 6.3. Envision Next Information-seeking Paradigm: Content Generation Envision Next Information-seeking Paradigm： コンテンツ生成

Search and recommendation systems aim to fulfill users’ information needs by retrieving or recommending a list of documents or items from a finite set.
検索・推薦システムは、有限の集合から文書やアイテムのリストを検索したり推薦したりすることで、ユーザーの情報ニーズを満たすことを目的としている。
In previous discussions, we have explored paradigm shifts in search and recommendation, particularly focusing on the latest generative paradigm.
これまでの議論では、検索とレコメンデーションにおけるパラダイムシフトを、特に最新のジェネレイティブパラダイムに焦点を当てながら探ってきた。
Regardless of whether the approach is based on deep learning or generative learning, the ultimate goal remains the same: matching the available content (documents or items) to users.
ディープラーニング（深層学習）に基づくアプローチであろうと、ジェネレーティブラーニング（生成学習）に基づくアプローチであろうと、最終的なゴールは変わらない： 利用可能なコンテンツ（ドキュメントやアイテム）をユーザーにマッチングさせること。
However, there has been a recent surge in the development of generative AI and models, which has introduced a novel way for users to obtain information from the Web.
しかし、最近ではジェネレーティブAIやモデルの開発が急ピッチで進められており、ユーザーがウェブから情報を得るための斬新な方法が導入されている。
Instead of merely matching existing content, generative AI models now have the capability to directly generate content.
既存のコンテンツを単にマッチングさせるのではなく、ジェネレーティブAIモデルは現在、コンテンツを直接生成する機能を備えている。
This means that the generated content, such as a document, may not have previously existed on the Web.
つまり、文書のような生成されたコンテンツは、以前はウェブ上に存在しなかったかもしれない。
• Search engines vs generative language models.

- 検索エンジンと生成言語モデルの比較。
  Search engines, such as Google3 , are widely used text retrieval applications that can efficiently retrieve relevant web pages from billions of websites based on user queries.
  Google3 などの検索エンジンは、広く使われているテキスト検索アプリケーションであり、ユーザーのクエリに基づいて何十億ものウェブサイトから関連するウェブページを効率的に検索することができる。
  Generative language models like ChatGPT 4 and Gemini 5 are trained on vast amounts of web documents to imbibe knowledge into their parameters.
  ChatGPT 4やGemini 5のような生成言語モデルは、膨大な量のウェブ文書で訓練され、そのパラメータに知識を染み込ませる。
  These models can then generate responses to user queries based on the instructions provided.
  これらのモデルは、提供された指示に基づいて、ユーザーのクエリに対する応答を生成することができる。

As a result, users now have the option to input their queries directly into generative language models to seek information.
その結果、ユーザーは生成言語モデルに直接クエリを入力して情報を求めることができるようになった。
In comparison to search engines, generative language models offer several advantages.1) They can provide more accurate responses, as they are not limited to presenting an entire web page.2) They can summarize content from multiple pages, which is particularly useful for complex queries.3) Additionally, generative language models can understand users’ information needs in multi-turn conversations.
検索エンジンと比較して、生成言語モデルにはいくつかの利点がある。1) ウェブページ全体の提示に限定されないため、より正確な回答を提供できる。2) 複数のページのコンテンツを要約できるため、複雑なクエリに特に有効である。3) さらに、生成言語モデルは、複数回にわたる会話でユーザーの情報ニーズを理解できる。
However, generative language models do face certain challenges.
しかし、生成言語モデルにはある課題がある。
One such challenge is the issue of information updating.
そのような課題のひとつが、情報更新の問題である。
Since these models are not trained on the latest documents, they may not be able to answer queries related to up-to-date information.
これらのモデルは最新の文書で訓練されていないため、最新の情報に関連するクエリに答えることができない可能性がある。
Consequently, they may lack the corresponding knowledge.
その結果、対応する知識が不足している可能性がある。
Furthermore, generative language models are prone to generating incorrect responses, a phenomenon known as hallucination [52].
さらに、生成言語モデルは、幻覚として知られる現象である誤った応答を生成しやすい[52]。
Overall, while generative language models offer unique advantages in information retrieval, they also have limitations, including information updating and hallucinations, that need to be addressed.
全体として、生成言語モデルは情報検索においてユニークな利点を提供する一方で、情報の更新や幻覚など、対処すべき限界もある。
• Image search vs image generation.

- 画像検索と画像生成。
  People have become accustomed to searching for images on the internet to fulfill their visual requirements.
  人々は、視覚的な要求を満たすためにインターネットで画像を検索することに慣れてしまった。
  However, the advancements in image generation, such as the GAN [35] and diffusion models [21], now enable individuals to directly acquire the desired images through generation rather than relying on web searches.
  しかし、GAN[35]や拡散モデル[21]などの画像生成の進歩により、個人がウェブ検索に頼るのではなく、生成によって目的の画像を直接取得できるようになった。
  This is especially beneficial for creative endeavors, as image generation has the potential to produce distinctive and unique visuals.
  画像生成には、独特でユニークなビジュアルを生み出す可能性があるため、これはクリエイティブな活動にとって特に有益である。
  Compared to image search, image generation models offer more personalized services and can create unique images based on users’ specific requirements.
  画像検索と比較して、画像生成モデルはよりパーソナライズされたサービスを提供し、ユーザーの特定の要件に基づいてユニークな画像を作成することができます。
  However, these models are also prone to the issue of generating images that do not adhere to physical rules.
  しかし、これらのモデルは、物理的な規則に従わない画像を生成してしまうという問題も抱えやすい。
  This means that the generated images may not accurately represent real-world objects or scenes.
  つまり、生成された画像は現実世界の物体やシーンを正確に表現していない可能性がある。
  • Item generation in recommendation.
- レコメンデーションにおけるアイテム生成。
  Traditional recommendation systems retrieve existing items from item corpus, which may not always meet users’ diverse information needs.
  従来のレコメンデーションシステムは、アイテムコーパスから既存のアイテムを取得するため、必ずしもユーザーの多様な情報ニーズを満たすとは限らない。
  Nevertheless, the boom of generative models offers a promising solution to supplement human-generated content in the traditional recommendation and foster personalized AI-Generated Content (AIGC) Specifically, item generation in recommendation can be achieved in two approaches.1) Content repurposing, which edits the existing items tailored to individual user preference for personalized recommendation [144], e.g., transfer a micro-video in a cartoon style.2) Content creation, which generates personalized new items to satisfy user-specific preference and intent [22, 120, 151, 157].
  具体的には、推薦におけるアイテム生成は、2つのアプローチで実現できる。1）コンテンツ再利用（Content repurposing）、これは、パーソナライズされた推薦のために、個々のユーザーの好みに合わせて既存のアイテムを編集するものである[144]。
  By leveraging these two approaches, personalized item generation enhances information seeking by providing personalized open-world content that aligns closely with individual user preferences.
  これら2つのアプローチを活用することで、パーソナライズされたアイテム生成は、個々のユーザーの嗜好に密接に沿ったパーソナライズされたオープンワールドコンテンツを提供することで、情報探索を強化する。

# 7. Conclusion 結論

Bridging the semantic gap between two matching entities is a fundamental and challenging issue in search and recommendation.
2つの一致するエンティティ間のセマンティックギャップを埋めることは、検索と推薦における基本的かつ挑戦的な問題である。
In this survey, we provide an overview of three paradigms aimed at solving this core research problem from a unified perspective.
このサーベイでは、この中心的な研究課題を統一的な視点から解決することを目的とした3つのパラダイムについて概観する。
Our focus is primarily on the recent generative paradigm for search and recommendation, known as generative search and recommendation.
私たちは主に、生成的検索と推薦として知られる、検索と推薦のための最近の生成的パラダイムに焦点を当てている。
We provide a comprehensive overview of a unified framework for generative search and recommendation, and discuss the current research contributions within this framework.
我々は、生成的検索と推薦のための統一されたフレームワークの包括的な概要を提供し、このフレームワークの中での現在の研究貢献について議論する。
In addition to categorizing the current works, we offer valuable insights into the generative paradigm, including an analysis of the strengths and weaknesses of various designs, such as different identifiers, training methods, and inference approaches.
現在の作品を分類するだけでなく、さまざまな識別子、学習方法、推論アプローチなど、さまざまなデザインの長所と短所の分析など、生成パラダイムに関する貴重な洞察を提供する。
By adopting a unified view of search and recommendation, we highlight the commonalities and unique challenges of generative search and recommendation.
検索と推薦の統一的な見方を採用することで、生成的検索と推薦の共通点とユニークな課題を浮き彫りにする。
Furthermore, we engage in a thorough discussion about the future outlook of the next information-seeking paradigm and the open problems in this field.
さらに、次の情報探索パラダイムの将来展望と、この分野における未解決の問題についても徹底的に議論する
