## refs 審判

- https://dl.acm.org/doi/fullHtml/10.1145/3178876.3186175 https://dl.acm.org/doi/fullHtml/10.1145/3178876.3186175

## title タイトル

DKN: Deep Knowledge-Aware Network for News Recommendation
DKN： ニュース推薦のためのディープ・ナレッジ・アウェア・ネットワーク

## abstruct abstruct

Online news recommender systems aim to address the information explosion of news and make personalized recommendation for users.
オンライン・ニュース推薦システムは、ニュースの情報爆発に対処し、ユーザーにパーソナライズされた推薦を行うことを目的としている。
In general, news language is highly condensed, full of knowledge entities and common sense.
一般的に、ニュース言語は非常に凝縮され、knowledge entities(i.e. 固有名詞)とcommon sense(常識)に満ちている。
However, existing methods are unaware of such external knowledge and cannot fully discover latent knowledge-level connections among news.
しかし、既存の方法(=テキストに基づく方法?)ではそのような**外部知識には気づかず、ニュース間の潜在的な知識レベルのつながりを完全に発見することはできない**。
The recommended results for a user are consequently limited to simple patterns and cannot be extended reasonably.
その結果、ユーザに推薦される結果は単純なパターンに限られ、合理的に拡張することはできない。
To solve the above problem, in this paper, we propose a deep knowledge-aware network (DKN) that incorporates knowledge graph representation into news recommendation.
上記の問題を解決するために、本論文では、**知識グラフ表現をニュース推薦に組み込むディープ・ナレッジ・アウェア・ネットワーク（DKN）**を提案する。
DKN is a content-based deep recommendation framework for click-through rate prediction.
DKNは、クリック率予測のためのコンテンツベースのディープ・レコメンデーション・フレームワークである。
The key component of DKN is a multi-channel and word-entity-aligned knowledge-aware convolutional neural network (KCNN) that fuses semantic-level and knowledge-level representations of news.
DKNの主要な構成要素は、**ニュースのsemantic-levelとknowledge-levelレベルの表現を融合する**、マルチチャンネル(=sequenceの各要素が2つのチャンネルを持つってこと?)でword-entity-alignedでknowledge-awareな畳み込みニューラルネットワーク（KCNN）である。
KCNN treats words and entities as multiple channels, and explicitly keeps their alignment relationship during convolution.
KCNNは単語とentityを複数のチャンネルとして扱い、畳み込み中にその**alignment(整列)関係**を明示的に保持する。
In addition, to address users’ diverse interests, we also design an attention module in DKN to dynamically aggregate a user's history with respect to current candidate news.
さらに、ユーザの多様な関心に対応するため、DKNでは、現在の候補ニュースに関するユーザの履歴を動的に集約するアテンション・モジュールも設計している。
Through extensive experiments on a real online news platform, we demonstrate that DKN achieves substantial gains over state-of-the-art deep recommendation models.
実際のオンラインニュースプラットフォームを用いた広範な実験を通じて、DKNが最先端のディープ・レコメンデーションモデルを大幅に上回ることを実証する。(お、ABテストか...??)
We also validate the efficacy of the usage of knowledge in DKN.
また、DKNにおける知識の活用の有効性も検証している。

# Introduction はじめに

With the advance of the World Wide Web, people's news reading habits have gradually shifted from traditional media such as newspapers and TV to the Internet.
ワールド・ワイド・ウェブの進展に伴い、人々のニュースを読む習慣は、新聞やテレビといった従来のメディアからインターネットへと徐々にシフトしている。
Online news websites, such as Google News1 and Bing News2, collect news from various sources and provide an aggregate view of news for readers.
グーグルニュース1やビングニュース2などのオンラインニュースサイトは、さまざまな情報源からニュースを収集し、読者にニュースの集約的なビューを提供する。
A notorious problem with online news platforms is that the volume of articles can be overwhelming to users.
オンライン・ニュース・プラットフォームで悪名高い問題は、記事の量がユーザを圧倒してしまうことだ。
To alleviate the impact of information overloading, it is critical to help users target their reading interests and make personalized recommendations [2, 25, 27, 32, 34, 39].
情報過多の影響を軽減するためには、利用者が読書の関心に的を絞り、パーソナライズされたレコメンデーションを行えるようにすることが重要である[2, 25, 27, 32, 34, 39]。

Generally, news recommendation is quite difficult as it poses three major challenges.
一般的に、ニュース推薦には**3つの大きな課題**があり、非常に難しい。
First, unlike other items such as movies [9] and restaurants [12], news articles are highly time-sensitive and their relevance expires quickly within a short period (see Section 5.1).
第一に、映画[9]やレストラン[12]のような他のアイテムとは異なり、ニュース記事は非常に時間に敏感であり、その関連性は短期間ですぐに失効する（セクション5.1参照）。
Out-of-date news are substituted by newer ones frequently, which makes traditional ID-based methods such as collaborative filtering (CF) [41] less effective.
古いニュースは頻繁に新しいニュースに置き換えられるため、協調フィルタリング（CF）[41]のような**従来のIDベースの手法はあまり有効ではない**。

Second, people are topic-sensitive in news reading as they are usually interested in multiple specific news categories (see Section 5.5).
第二に、人々はニュースの読み方において**トピックに敏感**であり、複数の特定のニュースカテゴリに関心を持つのが普通である（セクション5.5参照）。
How to dynamically measure a user's interest based on his diversified reading history for current candidate news is key to news recommender systems.
ニュース推薦システムでは、現在の候補ニュースに対する多様な読書履歴に基づいて、**ユーザの関心をいかに動的に測定するかが鍵**となる。

![figure1]()

Third, news language is usually highly condensed and comprised of a large amount of knowledge entities and common sense.
第三に、ニュース言語は通常、非常に凝縮されており、大量のknowledge entitiesとcommon senseで構成されている。
For example, as shown in Figure 1, a user clicks a piece of news with title “Boris Johnson Has Warned Donald Trump To Stick To The Iran Nuclear Deal” that contains four knowledge entities: “Boris Johnson”, “Donald Trump”, “Iran” and “Nuclear”.
例えば、図1に示すように、ユーザは「Boris Johnson Has Warned Donald Trump To Stick To The Iran Nuclear Deal」というタイトルのニュースをクリックするが、**このニュースには「Boris Johnson」、「Donald Trump」、「Iran」、「Nuclear」という4つのknowledge entitiesが含まれている**。
In fact, the user may also be interested in another piece of news with title “North Korean EMP Attack Would Cause Mass U.S.Starvation, Says Congressional Report” with high probability, which shares a great deal of contextual knowledge and is strongly connected with the previous one in terms of commonsense reasoning.
実際、ユーザは、高い確率で「North Korean EMP Attack Would Cause Mass U.S.Starvation, Says Congressional Report」というタイトルの別のニュースにも興味を持っているかもしれない。このニュースは、大量のcontextual knowledgeを共有しており、**common senseの理由から、前者と強くつながっている**。
However, traditional semantic models [30] or topic models [3] can only find their relatedness based on co-occurrence or clustering structure of words, but are hardly able to discover their latent knowledge-level connection.
しかし、従来のsemanticモデル[30]やtopicモデル[3]は、単語の共起やクラスタリング構造に基づいて関連性を見つけることしかできず、**潜在的な知識レベルのつながりを発見することはほとんどできない**。(要は単にテキストの埋め込み表現ではこれらの繋がりを表現できないってことか...!:thinking:)
As a result, a user's reading pattern will be narrowed down to a limited circle and cannot be reasonably extended based on existing recommendation methods.
その結果、**ユーザの読書パターンは限られた範囲に狭められ、既存の推薦手法に基づいていてはユーザの読書パターンを合理的に拡張することはできない。**

To extract deep logical connections among news, it is necessary to introduce additional knowledge graph information into news recommendations.
ニュース間の深い論理的つながりを抽出するためには、ニュース推薦にknowledge graph情報を追加する必要がある。
A knowledge graph is a type of directed heterogeneous graph in which nodes correspond to entities and edges correspond to relations.
**knowledge graphは、ノードがentityに対応し、エッジが関係に対応する、有向異種グラフの一種である**。
Recently, researchers have proposed several academic knowledge graphs such as NELL3 and DBpedia4, as well as commercial ones such as Google Knowledge Graph5 and Microsoft Satori6.
最近では、NELL3やDBpedia4といった学術的な知識グラフや、Google Knowledge Graph5やMicrosoft Satori6といった商業的なknowledge graphがいくつか提案されている。
These knowledge graphs are successfully applied in scenarios of machine reading[51], text classification[46], and word embedding[49].
これらのknowledge graphは、機械読み取り[51]、テキスト分類[46]、単語埋め込み[49]のシナリオで成功裏に適用されている。

Considering the above challenges in news recommendation and inspired by the wide success of leveraging knowledge graphs, in this paper, we propose a novel framework that takes advantage of external knowledge for news recommendation, namely the deep knowledge-aware network (DKN).
本稿では、上記のようなニュース推薦における課題を考慮し、knowledge graphの活用の広範な成功に触発されて、ニュース推薦において外部知識を活用する新しいフレームワーク、すなわちディープ・ナレッジ・アウェア・ネットワーク（DKN）を提案する。
DKN is a content-based model for click-through rate (CTR) prediction, which takes one piece of candidate news and one user's click history as input, and outputs the probability of the user clicking the news.
**DKNは、クリック率（CTR）予測のためのコンテンツベースのモデルであり、1つのニュース候補と1人のユーザのクリック履歴を入力とし、ユーザがそのニュースをクリックする確率を出力する**。(まさにこの振る舞いは、一般的なコンテンツベースの推薦モデル...!:thinking:)
Specifically, for a piece of input news, we first enrich its information by associating each word in the news content with a relevant entity in the knowledge graph.
具体的には、入力されたニュースに対して、まず、ニュース内容の各単語をknowledge graphの関連するエンティティに関連付けることで、その情報を豊かにする。
We also search and use the set of contextual entities of each entity (i.e., its immediate neighbors in the knowledge graph) to provide more complementary and distinguishable information.
また、**各entityのcontextual entitiesのセット(i.e. knowledge graphの直接の隣接ノード)**を検索して使用し、より補完的で識別可能な情報を提供する。
Then we design a key component in DKN, namely knowledge-aware convolutional neural networks (KCNN), to fuse the word-level and knowledge-level representations of news and generate a knowledge-aware embedding vector.
次に、DKNの主要な構成要素である、knowledge-aware convolutional neural networks（KCNN）を設計し、ニュースの単語レベルと知識レベルの表現を融合させ、知識認識埋め込みベクトルを生成する。
Finally, we use an attention module to dynamically aggregate a user's history with respect to current candidate news, and feed the user's embedding and the candidate news’ embedding into a deep neural network (DNN) for CTR prediction.
最後に、**アテンション・モジュールを使用して、現在の候補ニュースに関するユーザの履歴を動的に集約**し(=これはNRMSのみならず王道アプローチなのかも...!)、ユーザの埋め込みと候補ニュースの埋め込みを、CTR予測のためのディープニューラルネットワーク（DNN）に入力する。
Distinct from existing work [46], KCNN is: 1) multi-channel, as it treats word embedding, entity embedding, and contextual entity embedding of news as multiple stacked channels just like colored images; 2) word-entity-aligned, as it aligns a word and its associated entity in multiple channels and applies a transformation function to eliminate the heterogeneity of the word embedding and entity embedding spaces.
既存の研究[46]とは異なり、**KCNNは以下の2つの特徴を持つ**： 1) ニュースの単語埋め込み、entity埋め込み、contextual entity埋め込みを、カラー画像のように複数のスタックされたチャンネルとして扱うため、マルチチャンネル(3つ?)である。 2) ニュースの単語と関連するentityを複数のチャンネルで整列させ、単語埋め込みとentity埋め込み空間の異質性を除去するために変換関数を適用するため、word-entity-alignedである。

Using KCNN, we obtain a knowledge-aware representation vector for each piece of news.
KCNNを使うことで、各ニュースのknowledge-awareな表現ベクトルを得る。
To get a dynamic representation of a user with respect to current candidate news, we use an attention module to automatically match candidate news to each piece of clicked news, and aggregate the user's history with different weights.
現在の候補ニュースに関するユーザの動的な表現を得るために、アテンション・モジュールを使用して、クリックされた各ニュースに候補ニュースを自動的にマッチさせ、異なる重みでユーザの履歴を集約する。(候補ニュースによって、ユーザ履歴から得るユーザ表現が変わるってことかな??:thinking:)
The user's embedding and the candidate news’ embedding are finally processed by a deep neural network (DNN) for CTR prediction.
ユーザの埋め込みと候補ニュースの埋め込みは、最終的にCTR予測のためのディープニューラルネットワーク(DNN)によって処理される。(score prediction moduleは内積ではないんだ...!)

Empirically, we apply DKN to a real-world dataset from Bing News with extensive experiments.
経験的に、DKNをBing Newsからの実世界データセットに適用し、広範な実験を行った。(オフライン実験っぽい??)
The results show that DKN achieves substantial gains over state-of-the-art deep-learning-based methods for recommendation.
その結果、DKNは最新のディープラーニングに基づく推薦手法と比較して、大幅な向上を達成した。
Specifically, DKN significantly outperforms baselines by 2.8% to 17.0% on F1 and 2.6% to 16.1% on AUC with a significance level of 0.1.The results also prove that the usage of knowledge and an attention module can bring additional 3.5% and 1.4% in improvement, respectively, in the DKN framework.
具体的には、DKNは、有意水準0.1で、F1で2.8％から17.0％、AUCで2.6％から16.1％、ベースラインを有意に上回った。結果はまた、DKNフレームワークにおいて、知識と注意モジュールの使用が、それぞれ3.5％と1.4％の追加改善をもたらすことが証明された。
Moreover, we present a visualization result of attention values to intuitively demonstrate the efficacy of the usage of the knowledge graph in Section 5.5.
さらに、セクション5.5では、知識グラフの活用の有効性を直感的に示すために、attention valuesの視覚化結果を示す。

# Preliminaries 予備知識

In this section, we present several concepts and models related to this work, including knowledge graph embedding and convolutional neural networks for sentence representation learning.
このセクションでは、知識グラフ埋め込みや文表現学習のための畳み込みニューラルネットワークなど、この研究に関連するいくつかの概念とモデルを紹介する。

## Knowledge Graph Embedding 知識グラフの埋め込み

A typical knowledge graph consists of millions of entity-relation-entity triples (h, r, t), in which h, r and t represent the head, the relation, and the tail of a triple, respectively.
典型的な知識グラフは、数百万の実体-関係-実体のトリプル（h、r、t）から構成され、h、r、tはそれぞれトリプルの先頭、関係、末尾を表す。
Given all the triples in a knowledge graph, the goal of knowledge graph embedding is to learn a low-dimensional representation vector for each entity and relation that preserves the structural information of the original knowledge graph.
知識グラフのすべてのトリプルが与えられたとき、知識グラフ埋め込みの目標は、元の知識グラフの構造情報を保持する各エンティティと関係の低次元表現ベクトルを学習することである。
Recently, translation-based knowledge graph embedding methods have received great attention due to their concise models and superior performance.
近年、翻訳ベースの知識グラフ埋め込み手法は、その簡潔なモデルと優れた性能により、大きな注目を集めている。
To be self-contained, we briefly review these translation-based methods in the following.
自己完結するために、以下にこれらの翻訳ベースの手法を簡単にレビューする。

TransE [4] wants h + r ≈ t when (h, r, t) holds, where h , r and t are the corresponding representation vector of h, r and t.
ここで、h、r、tは、h、r、tの対応する表現ベクトルである。
Therefore, TransE assumes the score function
したがって、TransEはスコア関数

$$
\tag{}
$$

is low if (h, r, t) holds, and high otherwise.
は、(h, r, t)が成立していれば低く、そうでなければ高い。

TransH [48] allows entities to have different representations when involved in different relations by projecting the entity embeddings into relation hyperplanes:
TransH [48]は、エンティティの埋め込みを関係超平面に投影することで、異なる関係に関与するエンティティが異なる表現を持つことを可能にする：

$$
\tag{2}
$$

where h ⊥ = h − w ⊤ r h w r and t ⊥ = t − w ⊤ r t w r are the projections of h and t to the hyperplane w r , respectively, and ‖w r ‖2 = 1.
ここで、h ⊥ = h - w ⊤ r h w r と t ⊥ = t - w ⊤ t w r はそれぞれ、h と t の超平面 w r への投影であり、‖w r‖2 = 1 である。

TransR [26] introduces a projection matrix M r for each relation r to map entity embeddings to the corresponding relation space.
TransR[26]は、各関係rに対して射影行列M rを導入し、エンティティの埋め込みを対応する関係空間にマッピングする。
The score function in TransR is defined as
TransRのスコア関数は次のように定義される。

$$
\tag{3}
$$

where h r = h M r and t r = t M r .
ここで、h r = h M r、t r = t M r とする。

TransD [18] replaces the projection matrix in TransR by the product of two projection vectors of an entity-relation pair:
TransD [18]は、TransRの射影行列を、実体-関係ペアの2つの射影ベクトルの積で置き換える：

$$
\tag{4}
$$

where h ⊥ = ( r p h ⊤ p + I ) h , t ⊥ = ( r p t ⊤ p + I ) t , h p , r p and t p are another set of vectors for entities and relations, and I is the identity matrix.
ここで、h ⊥ = ( r p h ⊤ p + I ) h、t ⊥ = ( r p t ⊤ p + I ) t、h p、r p、t p は、実体と関係を表す別のベクトル集合であり、I は恒等行列である。

To encourage the discrimination between correct triples and incorrect triples, for all the methods above, the following margin-based ranking loss is used for training:
正しいトリプルと正しくないトリプルの識別を促進するために、上記のすべてのメソッドにおいて、以下のマージンベースのランキングロスがトレーニングに使用される：

$$
\tag{5}
$$

where γ is the margin, Δ and Δ′ are the set of correct triples and incorrect triples.
ここで、γはマージン、ΔとΔ′は正しいトリプルと正しくないトリプルの集合である。

## CNN for Sentence Representation Learning 文章表現学習のためのCNN

Traditional methods [1, 43] usually represent sentences using the bag-of-words (BOW) technique, i.e., taking word counting statistics as the feature of sentences.
伝統的な手法[1, 43]では、通常、BOW（Bag of Words）手法、つまり単語数の統計を文の特徴として用いて文を表現する。
However, BOW-based methods ignore word orders in sentences and are vulnerable to the sparsity problem, which leads to poor generalization performance.
しかし、BOWベースの手法は文中の語順を無視し、スパース性の問題に弱いため、汎化性能が低い。
A more effective way to model sentences is to represent each sentence in a given corpus as a distributed low-dimensional vector.
文章をモデル化するより効果的な方法は、与えられたコーパスの各文章を分散低次元ベクトルとして表現することである。
Recently, inspired by the success of applying convolutional neural networks (CNN) in the filed of computer vision [23], researchers have proposed many CNN-based models for sentence representation learning [7, 19, 20, 53] 7.
近年、コンピュータ・ビジョン[23]の分野で畳み込みニューラルネットワーク(CNN)を応用した成功に触発され、研究者たちは文表現学習のために多くのCNNベースのモデルを提案している[7, 19, 20, 53] 7。
In this subsection, we introduce a typical type of CNN architecture, namely Kim CNN [20].
この小節では、典型的なタイプのCNNアーキテクチャであるKim CNN [20]を紹介する。
Figure 2 illustrates the architecture of Kim CNN.
図2はキムCNNのアーキテクチャを示す。
Let w 1: n be the raw input of a sentence of length n, and w 1 : n = [ w 1 w 2 … w n ] ∈ R d × n be the word embedding matrix of the input sentence, where w i ∈ R d × 1 is the embedding of the i-th word in the sentence and d is the dimension of word embeddings.
w 1： nを長さnの生の入力文とし、w 1 ： n = [ w 1 w 2 ... w n ] ∈ R d × n は入力文の単語埋め込み行列であり、w i ∈ R d × 1 は文中のi番目の単語の埋め込み、dは単語埋め込み次元である。
A convolution operation with filter h ∈ R d × l is then applied to the word embedding matrix w 1: n , where l (l ≤ n) is the window size of the filter.
次に、フィルタh∈R d×l による畳み込み演算が、単語埋め込み行列w 1： ここで、l（l≦n）はフィルタのウィンドウサイズである。
Specifically, a feature ci is generated from a sub-matrix w i: i + l − 1 by
具体的には、特徴 ci は部分行列 w i から生成される： によって生成される。

$$
\tag{6}
$$

where f is a non-linear function, \* is the convolution operator, and b ∈ R is a bias.
ここで、fは非線形関数、◎は畳み込み演算子、b（R）はバイアスである。
After applying the filter to every possible position in the word embedding matrix, a feature map
単語埋め込み行列のすべての可能な位置にフィルタを適用した後、特徴マップを作成する。

$$
\tag{7}
$$

is obtained, then a max-over-time pooling operation is used on feature map c to identify the most significant feature:
が得られると、特徴マップcに対して最大時間プーリング演算が行われ、最も重要な特徴が特定される：

$$
\tag{8}
$$

One can use multiple filters (with varying window sizes) to obtain multiple features, and these features are concatenated together to form the final sentence representation.
複数の特徴量を得るために複数のフィルター（ウィンドウの大きさを変える）を使用することができ、これらの特徴量を連結して最終的な文表現を形成する。

# Problem Formulation 問題の定式化

We formulate the news recommendation problem in this paper as follows.
本稿では、ニュース推薦問題を以下のように定式化する。
For a given user i in the online news platform, we denote his click history as { t i 1 , t i 2 , … , t i N i } , where t i j (j = 1, …, Ni ) is the title8 of the j-th news clicked by user i, and Ni is the total number of user i’s clicked news.
オンライン・ニュース・プラットフォームにおけるあるユーザ i について、そのクリック履歴を { t i 1 , t i 2 , ... , t i N i } とする。ここで，t i j (j = 1, ..., Ni ) はユーザiがクリックしたj番目のニュースのタイトル8であり，Niはユーザiがクリックしたニュースの総数である．
Each news title t is composed of a sequence of words, i.e., t = [w 1, w 2, …], where each word w may be associated with an entity e in the knowledge graph.
各ニュースのタイトルtは単語の列、すなわちt＝[w 1, w 2, ...]で構成され、各単語wは知識グラフのエンティティeに関連付けられる。
For example, in the title “Trump praises Las Vegas medical team”, “Trump” is linked with the entity “Donald Trump”, while “Las” and “Vegas” are linked with the entity “Las Vegas”.
例えば、"Trump praises Las Vegas medical team "というタイトルでは、"Trump "は "Donald Trump "というエンティティとリンクしているが、"Las "と "Vegas "は "Las Vegas "というエンティティとリンクしている。
Given users’ click history as well as the connection between words in news titles and entities in the knowledge graph, we aim to predict whether user i will click a candidate news tj that he has not seen before.
ユーザーのクリック履歴と、ニュースタイトルの単語と知識グラフのエンティティの結びつきがあれば、ユーザーiが見たことのないニュース候補tjをクリックするかどうかを予測することを目的とする。

# Deep Knowledge-Aware Network ディープ・ナレッジ・アウェア・ネットワーク

In this section, we present the proposed DKN model in detail.
このセクションでは、提案するDKNモデルの詳細を示す。
We first introduce the overall framework of DKN, then discuss the process of knowledge distillation from a knowledge graph, the design of knowledge-aware convolutional neural networks (KCNN), and the attention-based user interest extraction, respectively.
まずDKNの全体的な枠組みを紹介し、次に知識グラフからの知識抽出プロセス、知識認識畳み込みニューラルネットワーク（KCNN）の設計、注意に基づくユーザーの興味抽出についてそれぞれ論じる。

## DKN Framework DKNフレームワーク

The framework of DKN is illustrated in Figure 3.
DKNのフレームワークを図3に示す。
We introduce the architecture of DKN from the bottom up.
DKNのアーキテクチャをボトムアップで紹介する。
As shown in Figure 3, DKN takes one piece of candidate news and one piece of a user's clicked news as input.
図3に示すように、DKNは1つの候補ニュースと1つのユーザーがクリックしたニュースを入力として受け取る。
For each piece of news, a specially designed KCNN is used to process its title and generate an embedding vector.
各ニュースに対して、特別に設計されたKCNNがそのタイトルを処理し、埋め込みベクトルを生成する。
KCNN is an extension of traditional CNN that allows flexibility in incorporating symbolic knowledge from a knowledge graph into sentence representation learning.
KCNNは従来のCNNを拡張したもので、知識グラフからの記号的知識を文表現学習に柔軟に取り入れることができる。
We will detail the process of knowledge distillation in Section 4.2 and the KCNN module in Section 4.3, respectively.
セクション4.2では知識抽出のプロセスについて、セクション4.3ではKCNNモジュールについて、それぞれ詳しく説明する。
By KCNN, we obtain a set of embedding vectors for a user's clicked history.
KCNNによって、ユーザのクリック履歴の埋め込みベクトル集合が得られる。
To get final embedding of the user with respect to the current candidate news, we use an attention-based method to automatically match the candidate news to each piece of his clicked news, and aggregate the user's historical interests with different weights.
現在の候補ニュースに対するユーザーの最終的な埋め込みを得るために、アテンション・ベースの手法を用いて、候補ニュースとクリックされた各ニュースを自動的にマッチングさせ、ユーザーの過去の関心を異なる重みで集約する。
The details of attention-based user interest extraction are presented in Section 4.4.The candidate news embedding and the user embedding are concatenated and fed into a deep neural network (DNN) to calculate the predicted probability that the user will click the candidate news.
候補ニュースの埋め込みとユーザーの埋め込みは連結され、ユーザーが候補ニュースをクリックする予測確率を計算するためにディープニューラルネットワーク（DNN）に供給される。

## Knowledge Distillation ♪知識の蒸留

The process of knowledge distillation is illustrated in Figure 4, which consists of four steps.
知識の蒸留のプロセスは図4に示されており、4つのステップから構成されている。
First, to distinguish knowledge entities in news content, we utilize the technique of entity linking [31, 36] to disambiguate mentions in texts by associating them with predefined entities in a knowledge graph.
まず、ニュース・コンテンツ内の知識エンティティを区別するために、エンティティ・リンク[31, 36]の技術を利用し、知識グラフ内の事前定義されたエンティティに関連付けることで、テキスト内の言及を曖昧さをなくす。
Based on these identified entities, we construct a sub-graph and extract all relational links among them from the original knowledge graph.
これらの識別されたエンティティに基づいて、サブグラフを構築し、元の知識グラフからエンティティ間のすべての関係リンクを抽出する。
Note that the relations among identified entities only may be sparse and lack diversity.
識別されたエンティティ間の関係のみが疎で多様性に欠ける可能性があることに注意。
Therefore, we expand the knowledge sub-graph to all entities within one hop of identified ones.
したがって、知識サブグラフを、識別されたエンティティから1ホップ以内のすべてのエンティティに拡張する。
Given the extracted knowledge graph, a great many knowledge graph embedding methods, such as TransE [4], TransH [48], TransR [26], and TransD [18], can be utilized for entity representation learning.
抽出された知識グラフがあれば、TransE [4]、TransH [48]、TransR [26]、TransD [18]など、非常に多くの知識グラフ埋め込み手法をエンティティ表現学習に利用することができる。
Learned entity embeddings are taken as the input for KCNN in the DKN framework.
学習されたエンティティの埋め込みは、DKNフレームワークのKCNNの入力となる。

It should be noted that though state-of-the-art knowledge graph embedding methods could generally preserve the structural information in the original graph, we find that the information of learned embedding for a single entity is still limited when used in subsequent recommendations.
最先端の知識グラフ埋め込み手法は、一般的に元のグラフの構造情報を保持することができるが、学習された1つのエンティティの埋め込み情報は、その後のレコメンデーションに使用する場合、まだ限定的であることに注意すべきである。
To help identify the position of entities in the knowledge graph, we propose extracting additional contextual information for each entity.
知識グラフにおけるエンティティの位置を特定するために、各エンティティの追加的な文脈情報を抽出することを提案する。
The “context” of entity e is defined as the set of its immediate neighbors in the knowledge graph, i.e.,
エンティティeの "コンテキスト "は、知識グラフにおけるその近傍の集合として定義される、

$$
\tag{9}
$$

where r is a relation and G is the knowledge graph.
ここでrは関係、Gは知識グラフである。
Since the contextual entities are usually closely related to the current entity with respect to semantics and logic, the usage of context could provide more complementary information and assist in improving the identifiability of entities.
文脈上のエンティティは通常、意味論と論理に関して現在のエンティティと密接に関連しているため、文脈の使用は、より補足的な情報を提供し、エンティティの識別可能性を向上させるのに役立つ可能性がある。
Figure 5 illustrates an example of context.
図5にコンテキストの例を示す。
In addition to use the embedding of “Fight Club” itself to represent the entity, we also include its contexts, such as “Suspense” (genre), “Brad Pitt” (actor), “United States” (country) and “Oscars” (award), as its identifiers.
エンティティを表現するために「ファイト・クラブ」自体の埋め込みを使用するだけでなく、「サスペンス」（ジャンル）、「ブラッド・ピット」（俳優）、「アメリカ合衆国」（国）、「アカデミー賞」（賞）といったコンテキストも識別子として含める。
Given the context of entity e, the context embedding is calculated as the average of its contextual entities:
エンティティeの文脈が与えられると、文脈埋め込みはその文脈エンティティの平均として計算される：

$$
\tag{10}
$$

where e i is the entity embedding of ei learned by knowledge graph embedding.
ここで、e i は知識グラフ埋め込みによって学習された ei のエンティティ埋め込みである。
We empirically demonstrate the efficacy of context embedding in the experiment section.
私たちは、実験セクションでコンテキスト埋め込みの有効性を実証している。

## Knowledge-aware CNN 知識認識CNN

Following the notations used in Section 2.2, we use t = w 1: n = [w 1, w 2, …, wn ] to denote the raw input sequence of a news title t of length n, and w 1 : n = [ w 1 w 2 … w n ] ∈ R d × n to denote the word embedding matrix of the title, which can be pre-learned from a large corpus or randomly initialized.
セクション2.2で使用した表記法に従い、t = w 1： n = [w 1, w 2, ..., wn ]は長さ n のニュースタイトル t の生の入力列を表し、 w 1 ： n = [ w 1 w 2 ... w n ] ∈ R d × n をタイトルの単語埋め込み行列とし、大規模なコーパスから事前学習するか、ランダムに初期化する。
After the knowledge distillation introduced in Section 4.2, each word wi may also be associated with an entity embedding e i ∈ R k × 1 and the corresponding context embedding ¯¯¯ e i ∈ R k × 1 , where k is the dimension of entity embedding.
セクション4.2で導入された知識蒸留の後、各単語wiは、エンティティ埋め込みe i∈R k×1および対応するコンテキスト埋め込み¯¯ e i∈R k×1（kはエンティティ埋め込みの次元）に関連付けられることもある。
Given the input above, a straightforward way to combine words and associated entities is to treat the entities as “pseudo words” and concatenate them to the word sequence [46], i.e.,
上記の入力が与えられた場合、単語と関連するエンティティを組み合わせる簡単な方法は、エンティティを「擬似単語」として扱い、単語列に連結することである[46]、

$$
\tag{11}
$$

where { e t j } is the set of entity embeddings associated with this news title.
ここで{ e t j }は、このニュースのタイトルに関連するエンティティの埋め込み集合である。
The obtained new sentence W is fed into CNN [ 20] for further processing.
得られた新しい文WはCNN[20]に入力され、さらに処理される。
However, we argue that this simple concatenating strategy has the following limitations: 1) The concatenating strategy breaks up the connection between words and associated entities and is unaware of their alignment.2) Word embeddings and entity embeddings are learned by different methods, meaning it is not suitable to convolute them together in a single vector space.3) The concatenating strategy implicitly forces word embeddings and entity embeddings to have the same dimension, which may not be optimal in practical settings since the optimal dimensions for word and entity embeddings may differ from each other.
しかし、この単純な連結戦略には以下の限界がある： 1) 単語の埋め込みとエンティティの埋め込みは異なる手法で学習されるため、それらを単一のベクトル空間で畳み込むのは適していない。3) 単語の埋め込みとエンティティの埋め込みは暗黙のうちに同じ次元を持つように強制されるが、単語とエンティティの埋め込みに最適な次元は互いに異なる可能性があるため、実用的な設定では最適ではないかもしれない。
Being aware of the above limitations, we propose a multi-channel and word-entity-aligned KCNN for combining word semantics and knowledge information.
上記の限界を意識して、我々は単語の意味と知識情報を結合するための、マルチチャンネルかつ単語固有性整合KCNNを提案する。
The architecture of KCNN is illustrated in the left lower part of Figure 3.
KCNNのアーキテクチャは図3の左下に示されている。
For each news title t = [w 1, w 2, …, wn ], in addition to use its word embeddings w 1: n = [w 1  w 2 … w n ] as input, we also introduce the transformed entity embeddings
各ニュースタイトル t = [w 1, w 2, ..., wn ]に対して、単語埋め込み w 1： n = [w 1 w 2 ... w n ] を入力とし、変換されたエンティティ埋め込みを導入する。

$$
\tag{12}
$$

and transformed context embeddings
と変換されたコンテキスト埋め込み

$$
\tag{13}
$$

as source of input 9, where g is the transformation function.
gは変換関数である。
In KCNN, g can be either linear
KCNNでは、gは線形である。

$$
\tag{14}
$$

or non-linear
または非線形

$$
\tag{15}
$$

where M ∈ R d × k is the trainable transformation matrix and b ∈ R d × 1 is the trainable bias.
ここで、M（R d × k）は学習可能な変換行列であり、b（R d × 1）は学習可能なバイアスである。
Since the transformation function is continuous, it can map the entity embeddings and context embeddings from the entity space to the word space while preserving their original spatial relationship.
変換関数は連続的であるため、エンティティの埋め込みとコンテキストの埋め込みを、元の空間的関係を保ったままエンティティ空間から単語空間にマッピングすることができる。
Note that word embeddings w 1: n , transformed entity embeddings g( e 1: n ) and transformed context embeddings g ( ¯¯¯ e 1 : n ) are the same size and serve as the multiple channels analogous to colored images.
単語埋め込み w 1： n 、変換された実体の埋め込み g( e 1： n ) と変換されたコンテキスト埋め込み g ( ¯¯¯ e 1 ： n ) は同じサイズであり、カラー画像に類似した複数のチャンネルとして機能する。
We therefore align and stack the three embedding matrices as
したがって、3つの埋め込み行列を次のように整列して積み重ねる。

$$
\tag{16}
$$

After getting the multi-channel input W, similar to Kim CNN [20], we apply multiple filters h ∈ R d × l × 3 with varying window sizes l to extract specific local patterns in the news title.
多チャンネル入力Wを得た後、Kim CNN [20]と同様に、ニュースのタイトル中の特定の局所パターンを抽出するために、ウィンドウサイズlを変化させながら複数のフィルターh∈R d×l×3を適用する。
The local activation of sub-matrix W i: i + l − 1 with respect to h can be written as
部分行列W iの局所活性化： i + l - 1のhに対する局所活性化は次のように書ける。

$$
\tag{17}
$$

and we use a max-over-time pooling operation on the output feature map to choose the largest feature:
そして、出力特徴マップの最大時間プーリング演算を使って、最大の特徴を選択する：

$$
\tag{18}
$$

All features ~ c h i are concatenated together and taken as the final representation e( t) of the input news title t, i.e.,
すべての特徴〜c h iを連結し、入力ニュースタイトルtの最終的な表現e( t)とする、

$$
\tag{19}
$$

where m is the number of filters.
ここで、mはフィルターの数である。

## Attention-based User Interest Extraction 注意に基づくユーザーの興味抽出

Given user i with clicked history { t i 1 , t i 2 , … , t i N i } , the embeddings of his clicked news can be written as e ( t i 1 ) , e ( t i 2 ) , … , e ( t i N i ) .
クリックされた履歴{ t i 1 , t i 2 , ... , t i N i }を持つユーザiが与えられると、彼のクリックされたニュースの埋め込みはe ( t i 1 ) , e ( t i 2 ) , ... , e ( t i N i ) と書くことができる。彼のクリックしたニュースの埋め込みは、e ( t i 1 ) , e ( t i 2 ) , ... , e ( t i N i ) と書くことができる。
To represent user i for the current candidate news tj , one can simply average all the embeddings of his clicked news titles:
現在の候補ニュースtjについてユーザーiを表現するには、単純に彼のクリックしたニュースのタイトルの埋め込みをすべて平均すればよい：

$$
\tag{20}
$$

However, as discussed in the introduction, a user's interest in news topics may be various, and user i’s clicked items are supposed to have different impacts on the candidate news tj when considering whether user i will click tj .
しかし、冒頭で述べたように、ユーザーのニュース・トピックに対する興味は様々であり、ユーザーiがtjをクリックするかどうかを考える場合、ユーザーiがクリックした項目がニュース候補tjに与える影響は異なると考えられる。
To characterize user's diverse interests, we use an attention network [ 47, 54] to model the different impacts of the user's clicked news on the candidate news.
ユーザーの多様な関心を特徴づけるために、アテンション・ネットワーク[47, 54]を用いて、ユーザーがクリックしたニュースが候補ニュースに与えるさまざまな影響をモデル化する。
The attention network is illustrated in the left upper part of Figure 3.
アテンション・ネットワークは図3の左上に示されている。
Specifically, for user i’s clicked news t i k and candidate news tj , we first concatenate their embeddings, then apply a DNN H as the attention network and the softmax function to calculate the normalized impact weight:
具体的には、ユーザーiがクリックしたニュースt i kと候補ニュースtjに対して、まずそれらの埋め込みを連結し、次に注目ネットワークとしてDNN Hを適用し、正規化影響度重みを計算するためにソフトマックス関数を適用する：

$$
\tag{21}
$$

The attention network H receives embeddings of two news titles as input and outputs the impact weight.
アテンション・ネットワークHは、2つのニュースのエンベッディングを入力として受け取り、インパクトの重みを出力する。
The embedding of user i with respect to the candidate news tj can thus be calculated as the weighted sum of his clicked news title embeddings:
したがって、候補ニュースtjに関するユーザーiの埋め込みは、彼のクリックしたニュースのタイトルの埋め込みの重み付き合計として計算することができる：

$$
\tag{22}
$$

Finally, given user i’s embedding e(i) and candidate news tj ’s embedding e(tj ), the probability of user i clicking news tj is predicted by another DNN G :
最後に、ユーザーiの埋め込みe(i)と候補ニュースtjの埋め込みe(tj )が与えられると、ユーザーiがニュースtjをクリックする確率が別のDNN Gによって予測される：

$$
\tag{23}
$$

We will demonstrate the efficacy of the attention network in the experiment section.
アテンション・ネットワークの有効性は、実験のセクションで実証する。

# Experiments 実験

In this section, we present our experiments and the corresponding results, including dataset analysis and comparison of models.
このセクションでは、データセットの分析とモデルの比較を含む、我々の実験とそれに対応する結果を示す。
We also give a case study about user's reading interests and make discussions on tuning hyper-parameters.
また、ユーザーの読書に対する興味についてのケーススタディを行い、ハイパーパラメータのチューニングについて議論する。

## Dataset Description データセットの説明

Our dataset comes from the server logs of Bing News.
我々のデータセットは、ビング・ニュースのサーバー・ログから得たものである。
Each piece of log mainly contains the timestamp, user id, news url, news title, and click count (0 for no click and 1 for click).
各ログには主に、タイムスタンプ、ユーザーID、ニュースのURL、ニュースのタイトル、クリックカウント（クリックがない場合は0、クリックがある場合は1）が含まれる。
We collect a randomly sampled and balanced dataset from October 16, 2016 to June 11, 2017 as the training set, and from June 12, 2017 to August 11, 2017 as the test set.
訓練セットとして2016年10月16日から2017年6月11日まで、テストセットとして2017年6月12日から2017年8月11日まで、ランダムにサンプリングされたバランスのとれたデータセットを収集する。
Additionally, we search all occurred entities in the dataset as well as the ones within their one hop in the Microsoft Satori knowledge graph, and extract all edges (triples) among them with confidence greater than 0.8.The basic statistics and distributions of the news dataset and the extracted knowledge graph are shown in Table 1 and Figure 6, respectively.
さらに、データセット内のすべての発生エンティティと、その1ホップ以内のエンティティをMicrosoft Satori知識グラフで検索し、それらの間のすべてのエッジ（トリプル）を信頼度0.8以上で抽出する。ニュースデータセットと抽出された知識グラフの基本統計量と分布をそれぞれ表1と図6に示す。

Figure 6a illustrates the distribution of the length of the news life cycle, where we define the life cycle of a piece of news as the period from its publication date to the date of its last received click.
図6aは、ニュースのライフサイクルの長さの分布を示している。ここでは、ニュースのライフサイクルを、掲載日から最後にクリックされた日までの期間と定義する。
We observe that about 90% of news are clicked within two days, which proves that online news is extremely time-sensitive and are substituted by newer ones with high frequency.
約90％のニュースが2日以内にクリックされていることが観察され、これはオンラインニュースが非常に時間に対して敏感であり、高い頻度で新しいものに置き換えられていることを証明している。
Figure 6b illustrates the distribution of the number of clicked pieces of news for a user.77.9% of users clicked no more than five pieces of news, which demonstrates the data sparsity in the news recommendation scenario.
図6bは、1人のユーザーがクリックしたニュース数の分布を示している。77.9％のユーザーは5つ以上のニュースをクリックしておらず、ニュース推薦シナリオにおけるデータの希少性を示している。

Figures 6c and 6d illustrate the distributions of the number of words (without stop words) and entities in a news title, respectively.
図6cと図6dは、それぞれニュースのタイトルに含まれる単語（ストップワードは含まない）とエンティティの数の分布を示す。
The average number per title is 7.9 for words and 3.7 for entities, showing that there is one entity in almost every two words in news titles on average.
タイトルあたりの平均数は、単語が7.9、実体が3.7であり、ニュースタイトルのほぼ2単語に1つの実体が含まれていることがわかる。
The high density of the occurrence of entities also empirically justifies the design of KCNN.
エンティティの出現密度が高いことも、経験的にKCNNの設計を正当化している。

Figures 6e and 6f present the distribution of occurrence times of an entity in the news dataset and the distribution of the number of contextual entities of an entity in extracted knowledge graph, respectively.
図6eと図6fは、それぞれニュースデータセットにおけるエンティティの出現時間の分布と、抽出された知識グラフにおけるエンティティの文脈エンティティ数の分布を示す。
We can conclude from the two figures that the occurrence pattern of entities in online news is sparse and has a long tail (80.4% of entities occur no more than ten times), but entities generally have abundant contexts in the knowledge graph: the average number of context entities per entity is 42.5 and the maximum is 140,737.
この2つの図から、オンライン・ニュースにおけるエンティティの出現パターンはまばらでロングテール（エンティティの80.4%は10回以下しか出現しない）であるが、エンティティは一般に知識グラフに豊富なコンテキストを持っていると結論づけることができる： エンティティあたりのコンテキスト・エンティティの平均数は42.5、最大数は140,737である。
Therefore, contextual entities can greatly enrich the representations for a single entity in news recommendation.
したがって、文脈上のエンティティは、ニュース推薦における単一のエンティティの表現を大いに豊かにすることができる。

## Baselines ベースライン

We use the following state-of-the-art methods as baselines in our experiments:
実験では、ベースラインとして以下の最先端手法を使用した：

LibFM [35] is a state-of-the-art feature-based factorization model and widely used in CTR scenarios.
LibFM [35]は、最先端の特徴ベースの因数分解モデルであり、CTRシナリオで広く使用されている。
In this paper, the input feature of each piece of news for LibFM is comprised of two parts: TF-IDF features and averaged entity embeddings.
本稿では、LibFMのための各ニュースの入力特徴量は2つの部分から構成される： TF-IDF特徴と平均化されたエンティティ埋め込みである。
We concatenate the feature of a user and candidate news to feed into LibFM.
LibFMにフィードするために、ユーザーの特徴と候補となるニュースを連結します。

KPCNN [46] attaches the contained entities to the word sequence of a news title and uses Kim CNN to learn representations of news, as introduced in Section 4.3.
KPCNN [46]は、セクション4.3で紹介したように、ニュースのタイトルの単語列に含まれるエンティティを付加し、Kim CNNを使ってニュースの表現を学習する。

DSSM [16] is a deep structured semantic model for document ranking using word hashing and multiple fully-connected layers.
DSSM[16]は、単語ハッシュと複数の完全連結レイヤーを用いた、文書ランキングのための深層構造化セマンティックモデルである。
In this paper, the user's clicked news is treated as the query and the candidate news are treated as the documents.
本稿では、ユーザがクリックしたニュースをクエリとして扱い、候補となるニュースを文書として扱う。

DeepWide [6] is a general deep model for recommendation, combining a (wide) linear channel with a (deep) non-linear channel.
DeepWide[6]は、推薦のための一般的な深いモデルで、（広い）線形チャネルと（深い）非線形チャネルを組み合わせている。
Similar to LibFM, we use the concatenated TF-IDF features and averaged entity embeddings as input to feed both channels.
LibFM と同様に、TF-IDF 特徴と平均化されたエンティティの埋め込みを連結したものを、両チャンネルへの入力として使用する。

DeepFM [13] is also a general deep model for recommendation, which combines a component of factorization machines and a component of deep neural networks that share the input.
DeepFM [13]も推薦のための一般的なディープモデルであり、入力を共有する因数分解マシンのコンポーネントとディープニューラルネットワークのコンポーネントを組み合わせている。
We use the same input as in LibFM for DeepFM.
DeepFMにはLibFMと同じ入力を使用します。

YouTubeNet [8] is proposed to recommend videos from a large-scale candidate set in YouTube using a deep candidate generation network and a deep ranking network.
YouTubeNet[8]は、深層候補生成ネットワークと深層ランキングネットワークを用いて、YouTubeの大規模な候補集合から動画を推薦することを提案している。
In this paper, we adapt the deep raking network to the news recommendation scenario.
本稿では、ディープ・レイキング・ネットワークをニュース推薦のシナリオに適応させる。

DMF [50] is a deep matrix factorization model for recommender systems which uses multiple non-linear layers to process raw rating vectors of users and items.
DMF [50]は推薦システムのための深層行列分解モデルであり、ユーザーとアイテムの生の評価ベクトルを処理するために複数の非線形レイヤーを使用する。
We ignore the content of news and take the implicit feedback as input for DMF.
ニュースの内容は無視し、暗黙のフィードバックをDMFの入力とする。

Note that except for LibFM, other baselines are all based on deep neural networks since we aim to compare our approach with state-of-the-art deep learning models.
LibFMを除き、他のベースラインはすべてディープニューラルネットワークをベースにしている。
Additionally, except for DMF which is based on collaborative filtering, other baselines are all content-based or hybrid methods.
さらに、協調フィルタリングに基づくDMFを除き、他のベースラインはすべてコンテンツベースまたはハイブリッド手法である。

## Experiment Setup 実験セットアップ

We choose TransD [18] to process the knowledge graph and learn entity embeddings, and use the non-linear transformation function in Eq.(15) in KCNN.
知識グラフの処理とエンティティの埋め込み学習にはTransD [18]を選択し、KCNNでは式(15)の非線形変換関数を使用する。
The dimension of both word embeddings and entity embeddings are set as 100.
単語埋め込み、実体埋め込みともに次元は100とした。
The number of filters are set as 100 for each of the window sizes 1, 2, 3, 4.
フィルター数は、ウィンドウサイズ1、2、3、4それぞれについて100とした。
We use Adam [21] to train DKN by optimizing the log loss.
Adam [21]を使い、対数損失を最適化することでDKNを訓練する。
We will further study the variants of DKN and the sensitivity of key parameters in Sections 5.4 and 5.6, respectively.
セクション5.4と5.6では、それぞれDKNの変種と主要パラメーターの感度をさらに研究する。
To compare DKN with baselines, we use F1 and AUC value as the evaluation metrics.
DKNをベースラインと比較するために、評価指標としてF1とAUC値を用いる。

The key parameter settings for baselines are as follows.
ベースラインの主なパラメータ設定は以下の通り。
For KPCNN, the dimensions of word embeddings and entity embeddings are both set as 100.
KPCNNでは、単語埋め込みと実体埋め込みの次元はともに100に設定されている。
For DSSM, the dimension of semantic feature is set as 100.
DSSMでは、意味特徴の次元を100とする。
For DeepWide, the final representations for deep and wide components are both set as 100.
DeepWideの場合、ディープコンポーネントとワイドコンポーネントの最終的な表現はどちらも100に設定されている。
For YouTubeNet, the dimension of final layer is set as 100.
YouTubeNetの場合、最終層の次元は100に設定されている。
For LibFM and DeepFM, the dimensionality of the factorization machine is set as {1, 1, 0}.
LibFMとDeepFMでは、因数分解マシンの次元を{1, 1, 0}とする。
For DMF, the dimension of latent representation for users and items is set as 100.
DMFでは、ユーザーとアイテムの潜在表現の次元を100とする。
The above settings are for fair consideration.
上記の設定は公正な検討のためのものである。
Other parameters in the baselines are set as default.
ベースラインのその他のパラメーターはデフォルトで設定されている。
Each experiment is repeated five times, and we report the average and maximum deviation as results.
各実験は5回繰り返され、結果として平均値と最大偏差を報告する。

## Results 結果

In this subsection, we present the results of comparison of different models and the comparison among variants of DKN.
この小節では、異なるモデルの比較とDKNの変種間の比較の結果を示す。

5.4.1 Comparison of different models..
5.4.1 各モデルの比較....
The results of comparison of different models are shown in Table 2.
異なるモデルの比較結果を表2に示す。
For each baseline in which the input contains entity embedding, we also remove the entity embedding from input to see how its performance changes (denoted by “(-)”).
入力にエンティティの埋め込みが含まれる各ベースラインについて、入力からエンティティの埋め込みを削除し、パフォーマンスがどのように変化するかを確認する（"(-) "で示す）。
Additionally, we list the improvements of baselines compared with DKN in brackets and calculate the p-value of statistical significance by t-test.
さらに、DKNと比較したベースラインの改善点を括弧内に記載し、t検定によって統計的有意性のp値を算出した。
Several observations stand out from Table 2:
表2からは、いくつかの観察が目立つ：

The usage of entity embedding could boost the performance of most baselines.
エンティティの埋め込みを使用することで、ほとんどのベースラインのパフォーマンスを向上させることができる。
For example, the AUC of KPCNN, DeepWide, and YouTubeNet increases by 1.1%, 1.8% and 1.1%, respectively.
例えば、KPCNN、DeepWide、YouTubeNetのAUCは、それぞれ1.1%、1.8%、1.1%増加する。
However, the improvement for DeepFM is less obvious.
しかし、DeepFMの改善はそれほど顕著ではない。
We try different parameter settings for DeepFM and find that if the AUC drops to about 0.6, the improvement brought by the usage of knowledge could be up to 0.5%.
DeepFMのさまざまなパラメータ設定を試した結果、AUCが約0.6まで低下した場合、知識の利用によってもたらされる改善は最大0.5%になることがわかった。
The results show that FM-based method cannot take advantage of entity embedding stably in news recommendation.
その結果、FMベースの手法では、ニュース推薦においてエンティティの埋め込みを安定的に利用できないことがわかった。

DMF performs worst among all methods.
DMFはすべての手法の中で最悪の結果だった。
This is because DMF is a CF-based method, but news is generally highly time-sensitive with a short life cycle.
DMFはCFベースの手法だが、ニュースは一般的にライフサイクルが短く、時間的制約が大きいからだ。
The result proves our aforementioned claim that CF methods cannot work well in the news recommendation scenario.
この結果は、CF手法はニュース推薦のシナリオではうまく機能しないという前述の主張を証明するものである。

Except for DMF, other deep-learning-based baselines outperform LibFM by 2.0% to 5.2% on F1 and by 1.5% to 4.5% on AUC, which suggests that deep models are effective in capturing the non-linear relations and dependencies in news data.
DMFを除き、他のディープラーニングベースのベースラインは、F1で2.0%から5.2%、AUCで1.5%から4.5%LibFMを上回っている。これは、ディープモデルがニュースデータの非線形な関係や依存関係を捉えるのに効果的であることを示唆している。

The architecture of DeepWide and YouTubeNet is similar in the news recommendation scenario, thus we can observe comparable performance of the two methods.
DeepWideとYouTubeNetのアーキテクチャは、ニュース推薦シナリオにおいて類似している。
DSSM outperforms DeepWide and YouTubeNet, the reason for which might be that DSSM models raw texts directly with word hashing.
DSSMはDeepWideとYouTubeNetを上回っているが、その理由はDSSMが生のテキストを直接単語ハッシュでモデル化しているからかもしれない。

KPCNN performs best in all baselines.
KPCNNはすべてのベースラインで最高のパフォーマンスを示した。
This is because KPCNN uses CNN to process input texts and can better extract the specific local patterns in sentences.
これは、KPCNNがCNNを使って入力テキストを処理し、文中の特定の局所パターンをよりよく抽出できるからである。

Finally, compared with KPCNN, DKN can still have a 1.7% AUC increase.
最後に、KPCNNと比較して、DKNはまだ1.7％のAUCを増加させることができる。
We attribute the superiority of DKN to its two properties: 1) DKN uses word-entity-aligned KCNN for sentence representation learning, which could better preserve the relatedness between words and entities; 2) DKN uses an attention network to treat users’ click history discriminatively, which better captures users’ diverse reading interests.
我々は、DKNの優位性を次の2つの特性に求める： 1)DKNは文の表現学習に単語と実体の整列したKCNNを用いることで、単語と実体の間の関連性をよりよく保持できること、2)DKNはユーザーのクリック履歴を識別的に扱うためにアテンション・ネットワークを用いることで、ユーザーの多様な読書興味をよりよく捉えることができること、である。

Figure 7 presents the AUC score of DKN and baselines for additional ten test days.
図7は、DKNとベースラインのAUCスコアを10日間追加したものである。
We can observe that the curve of DKN is consistently above baselines over ten days, which strongly proves the competitiveness of DKN.
DKNのカーブは10日間一貫してベースラインを上回っており、DKNの競争力を強く証明している。
Moreover, the performance of DKN is also with low variance compared with baselines, which suggests that DKN is also robust and stable in practical application.
さらに、DKNの性能はベースラインと比較して分散も小さく、これはDKNが実用的なアプリケーションにおいてもロバストで安定していることを示唆している。

5.4.2 Comparison among DKN variants..
5.4.2 DKN変種間の比較....
Further, we compare among the variants of DKN with respect to the following four aspects to demonstrate the efficacy of the design of the DKN framework: the usage of knowledge, the choice of knowledge graph embedding method, the choice of transformation function, and the usage of an attention network.
さらに、DKNフレームワークの設計の有効性を示すために、以下の4つの側面に関してDKNのバリエーション間を比較する： 知識の使い方、知識グラフの埋め込み方法の選択、変換関数の選択、注意ネットワークの使い方。
The results are shown in Table 3, from which we can conclude that:
結果は表3の通りで、そこから次のように結論づけられる：

The usage of entity embedding and contextual embedding can improve AUC by 1.3% and 0.7%, respectively, and we can achieve even better performance by combining them together.
エンティティ埋め込みと文脈埋め込みを利用することで、AUCをそれぞれ1.3%と0.7%向上させることができ、これらを組み合わせることで、さらに優れた性能を達成することができる。
This finding confirms the efficacy of using a knowledge graph in the DKN model.
この発見は、DKNモデルで知識グラフを使用することの有効性を裏付けている。

DKN+TransD outperforms other combinations.
DKN+TransDは他の組み合わせよりも優れている。
This is probably because, as presented in Section 2.1, TransD is the most complicated model among the four embedding methods, which is able to better capture non-linear relationships among the knowledge graph for news recommendation.
これは、2.1節で示したように、TransDが4つの埋め込み手法の中で最も複雑なモデルであり、ニュース推薦のための知識グラフ間の非線形関係をよりよく捉えることができるからであろう。

DKN with mapping is better than DKN without mapping, and the non-linear function is superior to the linear one.
マッピングありのDKNはマッピングなしのDKNより優れており、非線形関数は線形関数より優れている。
The results prove that the transformation function can alleviate the heterogeneity between word and entity spaces by self learning, and the non-linear function can achieve better performance.
その結果、変換関数は自己学習によって単語空間と実体空間の間の異質性を緩和することができ、非線形関数はより良い性能を達成できることが証明された。

The attention network brings a 1.7% gain on F1 and 0.9% gain on AUC for the DKN model.
アテンション・ネットワークは、DKNモデルに対してF1で1.7%、AUCで0.9%の利得をもたらした。
We will give a more intuitive demonstration on the attention network in the next subsection.
次のサブセクションでは、注意ネットワークについてより直感的なデモンストレーションを行う。

## Case Study ケーススタディ

To intuitively demonstrate the efficacy of the usage of the knowledge graph as well as the the attention network, we randomly sample a user and extract all his logs from the training set and the test set (training logs with label 0 are omitted for simplicity).
アテンション・ネットワークと同様に知識グラフの使用法の有効性を直感的に示すために、ランダムにユーザーをサンプリングし、トレーニング・セットとテスト・セットからすべてのログを抽出する（簡単のため、ラベル0のトレーニング・ログは省略する）。
As shown in Table 4, the clicked news clearly exhibits his points of interest: No.1-3 concern cars and No.4-6 concern politics (categories are not contained in the original dataset but manually tagged by us).
表4に示すように、クリックされたニュースには、彼の関心がはっきりと表れている： No.1-3は自動車に関するもの、No.4-6は政治に関するものである（カテゴリーは元のデータセットには含まれておらず、われわれが手作業でタグ付けした）。
We use the whole training data to train DKN with full features and DKN without entity nor context embedding, then feed each possible pair of training logs and test logs of this user to the two trained models and obtain the output value of their attention networks.
全トレーニングデータを用いて、完全な特徴量を持つDKNと、エンティティもコンテキストも埋め込まないDKNをトレーニングし、このユーザのトレーニングログとテストログの可能な各ペアを2つのトレーニングモデルに与え、それぞれのアテンションネットワークの出力値を求める。
The results are visualized in Figure 8, in which the darker shade of blue indicates larger attention values.
結果は図8に可視化されており、青が濃いほど注目度が高いことを示している。
From Figure 8a we observe that, the first title in test logs gets high attention values with “Cars” in the training logs since they share the same word “Tesla”, but the results for the second title are less satisfactory, since the second title shares no explicit word-similarity with any title in the training set, including No.1-3.
図8aから、テスト・ログの最初のタイトルは、同じ単語「Tesla」を共有しているため、トレーニング・ログの「Cars」と高いアテンション値を得ているが、2番目のタイトルは、No.1-3を含むトレーニング・セットのどのタイトルとも明確な単語の類似性を共有していないため、2番目のタイトルの結果は満足のいくものではない。
The case is similar for the third title in test logs.
テストログの3つ目のタイトルも同様のケースである。
In contrast, in Figure 8b we see that the attention network precisely captures the relatedness within the two categories “Cars” and “Politics”.
対照的に、図8bでは、注目ネットワークが「車」と「政治」という2つのカテゴリー内の関連性を正確に捉えていることがわかる。
This is because in the knowledge graph, “General Motors” and “Ford Inc.” share a large amount of context with “Tesla Inc.” and “Elon Musk”, moreover, “Jeh Johnson” and “Russian” are also highly connected to “Donald Trump”.
ナレッジグラフでは、「ゼネラルモーターズ」や「フォード社」は「テスラ社」や「イーロン・マスク」と多くの文脈を共有しており、さらに「ジェ・ジョンソン」や「ロシア人」も「ドナルド・トランプ」と強い結びつきがあるからだ。
The difference in the response of the attention network also affects the final predicted results: DKN with knowledge graph (Figure 8b) accurately predicts all the test logs, while DKN without knowledge graph (Figure 8a) fails on the third one.
注意ネットワークの反応の違いは、最終的な予測結果にも影響する： 知識グラフありのDKN（図8b）はすべてのテストログを正確に予測したが、知識グラフなしのDKN（図8a）は3つ目のテストログで失敗した。

## Parameter Sensitivity パラメーター感度

DKN involves a number of hyper-parameters.
DKNは多くのハイパーパラメーターを含んでいる。
In this subsection, we examine how different choices of hyper-parameters affect the performance of DKN.
この小節では、ハイパーパラメータの選択の違いがDKNの性能にどのような影響を与えるかを検証する。
In the following experiments, expect for the parameter being tested, all other parameters are set as introduced in Section 5.3.
以下の実験では、テストされるパラメータを除き、他のすべてのパラメータはセクション5.3で紹介したように設定される。

### Dimension of word embedding d and dimension of entity embedding k. 単語の埋め込み次元dとエンティティの埋め込み次元k。

We first investigate how the dimension of word embedding d and dimension of entity embedding k affect performance by testing all combinations of d and k in set {20, 50, 100, 200}.
まず、セット{20, 50, 100, 200}におけるdとkのすべての組み合わせをテストすることにより、単語埋め込みdの次元と実体埋め込みkの次元がパフォーマンスにどのように影響するかを調べる。
The results are shown in Figure 9a, from which we can observe that, given dimension of entity embedding k, performance initially improves with the increase of dimension of word embedding d.
図9aに示すように、エンティティ埋め込みkの次元が与えられた場合、単語埋め込みdの次元が大きくなるにつれて、最初に性能が向上することがわかる。
This is because more bits in word embedding can encode more useful information of word semantics.
これは、単語の埋め込みビットを増やすことで、単語の意味についてのより有用な情報をエンコードできるからである。
However, the performance drops when d further increases, as a too large d (e.g., d = 200) may introduce noises which mislead the subsequent prediction.
しかし、dがさらに大きくなると性能は低下する。dが大きすぎる（たとえばd = 200）と、その後の予測を誤らせるノイズが混入する可能性があるからだ。
The case is similar for k when d is given.
dが与えられたときのkについても、ケースは同様である。

### Window sizes of filters and the number of filters m. フィルターのウィンドウサイズとフィルター数 m.

We further investigate the choice of windows sizes of filters and the number of filters for KCNN in the DKN model.
さらに、DKNモデルにおけるKCNNのフィルターのウィンドウサイズとフィルター数の選択について調べる。
As shown in Figure 9b, given windows sizes, the AUC score generally increases as the number of filters m gets larger, since more filters are able to capture more local patterns in input sentences and enhance model capability.
図9bに示すように、ウィンドウのサイズが与えられた場合、フィルタの数mが大きくなるにつれてAUCスコアは一般的に増加する。
However, the trend changes when m is too large (m = 200) due to probable overfitting.
しかし、mが大きすぎる場合（m = 200）、オーバーフィッティングの可能性が高いため、傾向が変化する。
Likewise, we can observe similar rules for window sizes given m: a small window size cannot capture long-distance patterns in sentences, while a too large window size may easily suffer from overfitting the noisy patterns.
同様に、mを指定した場合の窓の大きさについても同様の規則がある： 小さいウィンドウサイズでは文の長距離パターンを捉えることができず、大きすぎるウィンドウサイズではノイズの多いパターンをオーバーフィットしてしまう。

# Related Work 関連作品

## News Recommendation ニュース推薦

News recommendation has previously been widely studied.
ニュース推薦については、以前から広く研究されてきた。
Non-personalized news recommendation aims to model relatedness among news [29] or learn human editors’ demonstration [47].
非パーソナライズド・ニュースレコメンデーションは、ニュース間の関連性をモデル化したり[29]、人間の編集者のデモンストレーションを学習したりすることを目的としている[47]。
In personalized news recommendation, CF-based methods [41] often suffer from the cold-start problem since news items are substituted frequently.
パーソナライズド・ニュースレコメンデーションにおいて、CFベースの手法[41]は、ニュースアイテムが頻繁に入れ替わるため、しばしばコールドスタート問題に悩まされる。
Therefore, a large amount of content-based or hybrid methods have been proposed [2, 22, 27, 34, 39].
そのため、コンテンツに基づく手法やハイブリッド手法が大量に提案されている[2, 22, 27, 34, 39]。
For example, [34] proposes a Bayesian method for predicting users’ current news interests based on their click behavior, and [39] proposes an explicit localized sentiment analysis method for location-based news recommendation.
例えば、[34]は、クリック行動に基づいてユーザーの現在のニュース関心を予測するベイズ法を提案し、[39]は、ロケーションベースのニュース推薦のための明示的なローカライズされたセンチメント分析法を提案している。
Recently, researchers have also tried to combine other features into news recommendation, for example, contextual-bandit [25], topic models [28], and recurrent neural networks [32].
最近、研究者はまた、例えば、文脈バンディット[25]、トピックモデル[28]、リカレントニューラルネットワーク[32]など、他の特徴をニュース推薦に組み合わせることを試みている。
The major difference between prior work and ours is that we use a knowledge graph to extract latent knowledge-level connections among news for better exploration in news recommendation.
先行研究とわれわれの研究の大きな違いは、ニュース推薦におけるより良い探索のために、知識グラフを使ってニュース間の潜在的な知識レベルのつながりを抽出することである。

## Knowledge Graph ナレッジグラフ

Knowledge graph representation aims to learn a low-dimensional vector for each entity and relation in the knowledge graph, while preserving the original graph structure.
知識グラフ表現は、元のグラフ構造を保持しながら、知識グラフの各エンティティと関係に対して低次元のベクトルを学習することを目的としている。
In addition to translation-based methods [4, 18, 26, 48] used in DKN, researchers have also proposed many other models such as Structured Embedding [5], Latent Factor Model [17], Neural Tensor Network [37] and GraphGAN [42].
DKNで使用されている翻訳ベースの手法[4, 18, 26, 48]に加え、研究者は構造化埋め込み[5]、潜在因子モデル[17]、ニューラルテンソルネットワーク[37]、GraphGAN[42]など、他の多くのモデルも提案している。
Recently, the knowledge graph has also been used in many applications, such as movie recommendation[52], top-N recommendation [33], machine reading[51], text classification[46] word embedding[49], and question answering [10].
近年、知識グラフは、映画推薦[52]、トップN推薦[33]、機械読書[51]、テキスト分類[46]、単語埋め込み[49]、質問応答[10]など、多くのアプリケーションでも利用されている。
To the best of our knowledge, this paper is the first work that proposes leveraging knowledge graph embedding in news recommendation.
我々の知る限り、本稿はニュース推薦において知識グラフの埋め込みを活用することを提案した最初の研究である。

## Deep Recommender Systems ディープ・レコメンダー・システム

Recently, deep learning has been revolutionizing recommender systems and achieves better performance in many recommendation scenarios.
近年、ディープラーニングは推薦システムに革命をもたらし、多くの推薦シナリオでより良いパフォーマンスを達成している。
Roughly speaking, deep recommender systems can be classified into two categories: using deep neural networks to process the raw features of users or items, or using deep neural networks to model the interaction among users and items.
大まかに言えば、ディープ・レコメンダー・システムは2つのカテゴリーに分類できる： ユーザーやアイテムの生の特徴を処理するためにディープニューラルネットワークを使う場合と、ユーザーやアイテム間の相互作用をモデル化するためにディープニューラルネットワークを使う場合である。
In addition to the aforementioned DSSM [16], DeepWide [6], DeepFM [13], YouTubeNet [8] and DMF [50], other popular deep-learning-based recommender systems include Collaborative Deep Learning [44], SHINE [45], Multi-view Deep Learning [11], and Neural Collaborative Filtering [14].
前述のDSSM [16]、DeepWide [6]、DeepFM [13]、YouTubeNet [8]、DMF [50]に加え、他の一般的なディープラーニングベースのレコメンダーシステムには、協調ディープラーニング [44]、SHINE [45]、マルチビュー・ディープラーニング [11]、ニューラル協調フィルタリング [14]などがある。
The major difference between these methods and ours is that DKN specializes in news recommendation and could achieve better performance than other generic deep recommender systems.
これらの手法と我々の手法の大きな違いは、DKNがニュース推薦に特化しており、他の一般的なディープ・レコメンダー・システムよりも優れたパフォーマンスを達成できることである。

# Conclusion 結論

In this paper, we propose DKN, a deep knowledge-aware network that takes advantage of knowledge graph representation in news recommendation.
本論文では、知識グラフ表現をニュース推薦に活用するディープ・ナレッジ・アウェア・ネットワーク、DKNを提案する。
DKN addresses three major challenges in news recommendation: 1) Different from ID-based methods such as collaborative filtering, DKN is a content-based deep model for click-through rate prediction that are suitable for highly time-sensitive news.2) To make use of knowledge entities and common sense in news content, we design a KCNN module in DKN to jointly learn from semantic-level and knowledge-level representations of news.
DKNは、ニュース推薦における3つの主要な課題を解決する： 1)協調フィルタリングのようなIDベースの手法とは異なり、DKNはクリック率予測のためのコンテンツベースのディープモデルであり、非常にタイムセンシティブなニュースに適している。2)ニュースコンテンツに含まれる知識エンティティや常識を利用するために、DKNのKCNNモジュールを設計し、ニュースの意味レベルと知識レベルの表現から共同で学習する。
The multiple channels and alignment of words and entities enable KCNN to combine information from heterogeneous sources and maintain the correspondence of different embeddings for each word.3) To model the different impacts of a user's diverse historical interests on current candidate news, DKN uses an attention module to dynamically calculate a user's aggregated historical representation.
単語とエンティティの複数のチャネルとアライメントにより、KCNNは異種ソースからの情報を結合し、各単語の異なる埋め込みの対応関係を維持することができる。3) ユーザーの多様な歴史的関心が現在の候補ニュースに与えるさまざまな影響をモデル化するために、DKNはアテンション・モジュールを使用して、ユーザーの集約された歴史的表現を動的に計算する。
We conduct extensive experiments on a dataset from Bing News.
ビング・ニュースのデータセットで大規模な実験を行った。
The results demonstrate the significant superiority of DKN compared with strong baselines, as well as the efficacy of the usage of knowledge entity embedding and the attention module.
その結果、DKNが強力なベースラインと比較して有意に優れていること、また知識エンティティの埋め込みとアテンション・モジュールの利用が有効であることが実証された。
