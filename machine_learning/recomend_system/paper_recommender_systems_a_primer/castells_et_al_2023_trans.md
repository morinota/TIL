## 0.1. link 0.1. リンク

- https://paperswithcode.com/paper/recommender-systems-a-primer httpsを使用しています。

- [pdf](https://arxiv.org/pdf/2302.02579v1.pdf) pdf](https:

## 0.2. title 0.2. タイトル

Recommender Systems:
リコメンダーシステム。
A Primer
入門編

## 0.3. abstract 0.3. 抽象的

Personalized recommendations have become a common feature of modern online services, including most major e-commerce sites, media platforms and social networks.
パーソナライズされたレコメンデーションは、ほとんどの主要なeコマースサイト、メディアプラットフォーム、ソーシャルネットワークなど、現代のオンラインサービスにおいて一般的な機能になっている.
Today, due to their high practical relevance, research in the area of recommender systems is flourishing more than ever.
今日、その実用的な関連性の高さから、レコメンダーシステム分野の研究はかつてないほど盛んになっている.
However, with the new application scenarios of recommender systems that we observe today, constantly new challenges arise as well, both in terms of algorithmic requirements and with respect to the evaluation of such systems.
しかしながら、**レコメンダーシステムの新たな応用シナリオの出現に伴い、アルゴリズムへの要求やシステムの評価に関しても常に新たな課題が発生**している.
In this paper, we first provide an overview of the traditional formulation of the recommendation problem.
本論文では、まず、推薦問題の伝統的な定式化について概観する.
We then review the classical algorithmic paradigms for item retrieval and ranking and elaborate how such systems can be evaluated.
次に，項目検索とランキングのための古典的なアルゴリズムパラダイムを概観し，そのようなシステムがどのように評価されるかを詳しく説明する.
Afterwards, we discuss a number of recent developments in recommender systems research, including research on session-based recommendation, biases in recommender systems, and questions regarding the impact and value of recommender systems in practice.
その後、**session-based recommendation**(=sequential hogehoge~の話??)に関する研究、推薦システムにおけるバイアス、および推薦システムの実際の影響と価値に関する疑問など、推薦システム研究における最近のいくつかの発展について議論する.

# 1. Basic Concepts 1. 基本コンセプト

## 1.1. Introduction 1.1. はじめに

Automated and often personalized recommendations are omnipresent in today’s online world.
今日のオンライン社会では、自動化され、しばしばパーソナライズされたレコメンデーションが広く普及しています。
Nowadays, whenever we go online, there is a good chance that we will very soon receive recommendations about more things to shop, trending apps to download, or new music or artists to discover.
今日、私たちがオンラインを利用するときはいつでも、もっと買い物をしたい、流行のアプリをダウンロードしたい、新しい音楽やアーティストを発掘したいといったおすすめ情報をすぐに受け取ることができる可能性が高いのです。
These personalized suggestions are provided to us by recommender systems, which are software components that determine—based on statistics and machine learning models—the most suitable items that should be presented to an individual user.
レコメンダーシステムは、統計学と機械学習モデルに基づいて、個々のユーザーに最適な情報を提供するソフトウェアコンポーネントです。
Due to their widespread use in practice and their demonstrated capabilities of creating value both for consumers and businesses, recommender systems can be seen as one of the most visible success stories of artificial intelligence.
レコメンダーシステムは、統計学と機械学習モデルに基づいて、個々のユーザーに最適な商品を提示するソフトウェアコンポーネントであり、広く実用化され、消費者と企業の両方に価値をもたらすことが実証されているため、人工知能の最も顕著な成功例の一つと見なすことができる。
Today, research in this area is flourishing more than ever, both due to the practical relevance of such systems and due to the ongoing rapid developments in machine learning.
現在、この分野の研究は、システムの実用的な意義と機械学習の急速な発展により、かつてないほど盛んになっている。

Historically, the area of recommender systems has various relationships to the field of information retrieval (IR).
歴史的に、推薦システムの分野は、情報検索（IR）の分野と様々な関係をもっている。
The problem of retrieving and ranking a set of items from a larger collection, for example, is central both in recommendation and search tasks.
例えば、より大きなコレクションからアイテムのセットを検索し、ランキングする問題は、推薦と検索タスクの両方において中心的なものである。
The two areas furthermore oftentimes rely on similar algorithms and machine learning models and they use the same or similar evaluation methodology to assess the performance of these models.
さらに、この2つの分野は、しばしば類似のアルゴリズムや機械学習モデルに依存し、これらのモデルの性能を評価するために、同一または類似の評価方法を用いている。
Recommendation is however also different from IR in a number of ways.
しかし、レコメンデーションはIRとは多くの点で異なっている。
The selection of items in recommendation scenarios, for example, is typically based on individual user profiles and not on interactive queries.
例えば、推薦シナリオにおけるアイテムの選択は、一般的に個々のユーザープロファイルに基づいており、インタラクティブなクエリに基づいているわけではない。
From an IR perspective, one way to look at recommendation therefore is to see it as a problem setting where the item retrieval is based on an implicit query—which may also depend on the user’s context—rather than on explicit queries.
IRの観点から見ると、推薦とは、明示的なクエリではなく、ユーザーのコンテキストに依存する暗黙的なクエリに基づいてアイテムを検索する問題設定であると考えることができる。
Moreover, recommendation is more often a push communication, whereas IR systems are typically reactive applications.
さらに、推薦とはプッシュ型のコミュニケーションであるのに対し、IRシステムはリアクティブなアプリケーションであることが多い。

The roots of information retrieval can be traced to as far back as the 1950s [Sanderson and Croft 2012].
情報検索のルーツは 1950 年代までさかのぼることができる [Sanderson and Croft 2012]。
The foundations of modern-day recommender systems, in contrast, were mainly laid in the 1990s.
これに対して、現代のレコメンダーシステムの基礎が築かれたのは主に1990年代である。
In 1992, Tapestry, a prototype of a personalized email filtering system, was developed at Xerox PARC [Goldberg et al. 1992].
1992 年、Xerox PARC でパーソナライズされた電子メールフィルタリングシステムのプロトタイプである Tapestry が開発されました [Goldberg et al. 1992]。
One main innovative idea of this system was to leverage the opinion of others (ratings) in the filtering process, and the term collaborative filtering (CF) was popularized with this system.
このシステムの主な革新的なアイデアは、フィルタリングの過程で他者の意見（評価）を活用することであり、協調フィルタリング（CF）という言葉はこのシステムで一般化した。
Soon later, several research groups worked on automating Tapestry’s rule-based approach, and in 1994, the highly influential GroupLens system was proposed [Resnick et al. 1994].
その後、いくつかの研究グループがTapestryのルールベースのアプローチの自動化に取り組み、1994年に大きな影響力を持つGroupLensシステムが提案された[Resnick et al.］
The main idea in this system was to automatically determine like-minded “neighbors” of a user and to recommend those news items to a user that these neighbors have rated highly.
このシステムの主なアイデアは、あるユーザーと同じ考えを持つ「隣人」を自動的に特定し、その隣人が高く評価したニュースアイテムをユーザーに推薦することでした。
In the context of this early work, the recommendation problem was operationalized as a “matrix filling” problem, where the input to a recommendation algorithm is a user-item rating matrix and the goal is to predict the missing entries in this matrix.
この初期の研究において、推薦問題は「行列充填」問題として運用され、推薦アルゴリズムへの入力はユーザーと項目の評価行列であり、目標はこの行列に欠けている項目を予測することであった。
This research operationalization and the use of collaborative filtering techniques is still predominant in today’s research and practice.
この研究運用と協調フィルタリング技術の利用は、今日の研究と実践でまだ主流となっています。
Over the last almost three decades, however, many more elaborate machine learning algorithms were designed or applied for recommendation problems, including various matrix factorization techniques— which were also used first in the 1990s [Billsus and Pazzani 1998]—and, most recently, sophisticated deep learning techniques, e.g., [Liang et al. 2018].
しかし、この約30年の間に、より精巧な多くの機械学習アルゴリズムが推薦問題用に設計されたり、適用されたりしました。これには、様々な行列分解技術-これも1990年代に初めて用いられました[Billsus and Pazzani 1998]-や、最も最近では、高度な深層学習技術、例えば[Liang et al. 2018]が含まれています。

An alternative to using collaborative preference signals is to rank and filter documents in a personalized way by looking at their content.
協調的な嗜好信号を使う代わりに、文書の内容を見てパーソナライズされた方法で文書をランク付けし、フィルタリングすることができます。
The corresponding content-based filtering techniques were also investigated in the 1990s, often under the terms information filtering or personalized information filtering [Foltz and Dumais 1992].
これに対応するコンテンツベースのフィルタリング技術も1990年代に研究され、しばしば情報フィルタリングやパーソナライズド情報フィルタリングという用語で呼ばれています [Foltz and Dumais 1992]。
These systems are often largely based on known IR techniques like TF-IDF encodings1 of the documents.
これらのシステムは、文書のTF-IDFエンコーディング1 のような既知のIR技術に大きく基づいていることが多い。
In pure contentbased recommender systems, the main idea is to suggest items to the users that are similar to those that they liked in the past, i.e., without considering the opinions of others.
純粋なコンテンツベース・レコメンダーシステムでは、ユーザが過去に気に入ったものと類似したアイテムを提案すること、つまり、他の人の意見を考慮しないことが主なアイデアである。
Nowadays, however, we very often observe that hybrid systems are used in practice that combine different recommendation techniques and types of data.
しかし、現在では、異なる推薦手法やデータの種類を組み合わせたハイブリッド型のシステムが実際に使用されることが非常に多くなっている。
An early example of such a system is Fab [Balabanovic and Shoham 1997], a content-based collaborative system designed for web page ´ recommendation at Stanford.
このようなシステムの初期の例として、スタンフォード大学でウェブページ推薦のために設計されたコンテンツベースの協調システム Fab [Balabanovic and Shoham 1997]がある。

Most of the early systems discussed here were developed as research prototypes and mostly used in academic settings.
ここで取り上げた初期のシステムのほとんどは、研究用のプロトタイプとして開発され、そのほとんどが学術的な環境で使用されていた。
However, already before the end of the 1990s a number of successful deployments of recommendation techniques were reported for domains such as of e-commerce or music, see, e.g., [Schafer et al. 1999].
しかし、1990 年代末以前には、電子商取引や音楽などの分野で、推薦技術の導入に成功した例が多数報告されている [Schafer et al.1999] 。
Later on, Amazon was probably one of the first organizations that relied on recommendation technology at scale [Linden et al. 2003].
その後，Amazon がレコメンデーション技術を大規模に利用した最初の組織のひとつとなった [Linden et al.2003].
Nowadays, as mentioned above, there are many online services where recommendations are central to the user experience, e.g., at Netflix [Gomez-Uribe and Hunt 2015], Spotify [Semerci et al. 2019], or YouTube [Covington et al. 2016].
現在では，上述のように，Netflix [Gomez-Uribe and Hunt 2015]，Spotify [Semerci et al. 2019]，あるいは YouTube [Covington et al. 2016] などで，推薦がユーザー体験の中心となるオンラインサービスが多く存在します．
Over the years, also a number of success stories can be found in the literature, where the potential business value of recommender systems is documented, see [Jannach and Jugovac 2019] for an overview.
長年にわたり、推薦システムの潜在的なビジネス価値が文書化された多くの成功例も文献で見つけることができ、概要については[Jannach and Jugovac 2019]を参照。

Overall, the field has reached a certain level of maturity and standardization, in particular with respect to the operationalization of the research problem and the evaluation methodology.
全体として、この分野は、特に研究問題の運用と評価方法に関して、一定の成熟度と標準化に達している。
However, the recommendation problem is far from being solved, as there is a constant stream of new application scenarios that have not been adequately addressed so far in the research community.
しかし、研究コミュニティでこれまで適切に対処されてこなかった新しいアプリケーションシナリオが絶え間なく存在するため、推奨問題は解決には程遠い。
This paper reflects this situation and consists of two main parts.
本論文はこのような状況を反映し、2つの主要な部分から構成されている。
In the first part, in Sections 1.2 to 1.4, we provide an overview on the basic concepts of recommender systems and how recommender systems are commonly evaluated.
第1部では、1.2節から1.4節において、推薦システムの基本概念と推薦システムの一般的な評価方法について概観を行う。
Afterwards, from Section 2.1 on, we discuss a number of current and future topics in recommender systems research.
その後、セクション 2.1 以降では、推薦システム研究における現在および将来のトピックについて議論する。

## 1.2. The Recommendation Task 1.2. レコメンデーションタスク

The main computational task2 of any recommender system is to determine which items to show to a user in a given situation.
レコメンダーシステムの主な計算タスク2 は、与えられた状況下でユーザーにどのアイテムを表示するかを決定することである。
Therefore, in any individual application setting, before an algorithm is implemented and evaluated, the question has to be answered based on which criteria the items should be selected and ranked.
そのため、アルゴリズムを実装し評価する前に、どのような基準で項目を選択し、ランク付けすべきかという問題に答えなければならない。
At the most general level, any recommender system is designed to create a certain value or utility for one or more of the involved stakeholders [Jannach and Adomavicius 2016].
最も一般的なレベルでは、どんなレコメンダーシステムも、関係する1人以上のステークホルダーに一定の価値や効用を生み出すように設計されている [Jannach and Adomavicius 2016]。
In practice, there are many ways of how value can be created.
実際には、どのように価値が創造されるかは多くの方法があります。
From the perspective of a consumer, for example, a recommender system is usually assumed to reduce problems of information overload.
例えば、消費者の視点からは、レコメンダーシステムは通常、情報過多の問題を軽減することが想定される。
From the perspective of the provider, on the other hand, providing personalized recommendations can help to increase business-related key-performance indicators (KPIs) such as sales numbers or customer retention.
一方、提供者の観点からは、パーソナライズされたレコメンデーションを提供することで、販売数や顧客維持率といったビジネスに関連するKPI（Key Performance Indicator）を高めることができる。
We will discuss related questions of the impact and the value of recommender systems in more depth later in Section 2.3.
レコメンダーシステムの影響と価値に関する関連する問題については、2.3節で後ほど詳しく説明します。

Academic research often aims to abstract from the specifics of individual domains, particular applications, or business models of recommendation providers.
学術的な研究では、個々のドメイン、特定のアプリケーション、あるいは推薦プロバイダのビジネスモデルなどの特殊性を抽象化することがしばしば目指される。
The main computational task is therefore often framed in a correspondingly abstract way, usually to compute an estimate of the absolute or relative relevance of individual items for a given user.
そのため、主要な計算タスクはそれに応じて抽象化され、通常、与えられたユーザーに対する個々のアイテムの絶対的または相対的関連性の推定値を計算することになります。
On a general level, this problem can be formalized as follows, see [Adomavicius and Tuzhilin 2005].
一般的には，この問題は次のように定式化することができます[Adomavicius and Tuzhilin 2005]．
Given
与えられた

- a set of users U, ユーザUの集合である。

- a set of items I and 一組のアイテムIと

- a utility function $f :U\times I -> R$, which maps user and items to a utility value taken from a totally ordered set R (e.g., of nonnegative real numbers), 効用関数 $f :Utimes I -> R$, ユーザとアイテムを全順序集合R (例えば、非負の実数) から取った効用値に対応させるもの。

recommend the item $i' \in I$, which maximizes the utility function, more formally:
は、より正式には効用関数を最大化する項目 $i' \in I$ を推奨する。

$$
\tag{1.1}
$$

Typically, we are interested in recommending more than one item.
一般に、我々は複数のアイテムを推薦することに興味がある。
This can be done by returning those N items that have the highest utility values.
これは、最も高い効用値を持つ N 個の項目を返すことによって実現できる。
Using this definition, algorithmic research in recommender systems (see Section 1.3) amounts to defining or learning the utility function f , where f can be based on different types of additional information.
この定義を用いると、レコメンダー・システム（セクション 1.3 参照）のアルゴリズム研究は、効用関数 f を定義または学習することに等しく、f は異なるタイプの追加情報 に基づくことができる。

In the collaborative-filtering GroupLens system from 1994 mentioned earlier and in countless subsequent works, for example, the utility function f was designed to return a rating prediction.
例えば、先に述べた1994年の協調フィルタリングシステムGroupLensや、その後の無数の作品において、効用関数fは評価予測を返すように設計されていた。
The additional information that is used within f was the user-item matrix of known ratings.
fの中で使用される追加情報は、既知の評価のユーザー項目マトリックスであった。
Table 1.1 shows an example of such a rating matrix, where the specific task that is highlighted in the table is to make a recommendation for user u1.
表1.1はこのような評価行列の例で，表中で強調されている具体的なタスクは，ユーザu1に対する推薦を行うことである．
This is accomplished by predicting the ratings of user u1 for the so far unrated items i4 and i5.
これは、まだ評価されていない項目i4とi5に対するユーザーu1の評価を予測することによって達成される。

The specific implementation of f in the GroupLens system was a nearest-neighbor method.
GroupLens における f の具体的な実装は、最近傍法であった。
In pure content-based recommendation approaches, in contrast, f is not based on the useritem rating matrix, but on the observed past behavior of an individual user and additional information about the items in I. In hybrid approaches, finally, the implementation of f might simultaneously consider the rating matrix, item meta-data, and other sources of information including demographics, various other types of observed user behavior beyond past ratings, or the users’ embedding in a social network, see also Section 1.3.6.
一方、純粋なコンテンツベースの推薦アプローチでは、fはユーザとアイテムの評価行列ではなく、個々のユーザの過去の行動とIのアイテムに関する追加的な情報に基づいている。ハイブリッドアプローチでは、fの実装は、評価行列、アイテムメタデータ、および、デモグラフィックス、過去の評価以外の他のタイプのユーザ行動の観察、またはユーザのソーシャルネットワークへの埋め込みなどの情報源を同時に考慮するかもしれません（1.3.6節も参照ください）。

Collaborative filtering is the most frequently addressed problem setting in the literature and a large body of the literature aims at learning f from the usually noisy data in the user-item matrix.
協調フィルタリングは文献上最も頻繁に扱われる問題設定であり、文献の大部分は、ユーザ項目行列の通常ノイズの多いデータからfを学習することを目的としている。
Correspondingly, all sorts of machine learning algorithms were applied over the years to learn f .
それに応じて、f を学習するためにあらゆる種類の機械学習アルゴリズムが長年にわたって適用されてきた。
Historically, the user-item rating matrix was considered to contain explicit, userspecified item ratings.
歴史的には、ユーザ項目評価行列は、ユーザが指定した明示的な項目評価を含むと考えられていた。
Nowadays, research is more focused on situations where only implicit user feedback is available.
しかし、現在では、暗黙的なユーザフィードバックしか得られない状況に注目が集まっている。
In such cases, the entries in the rating matrix are not values ranging, e.g., from one to five stars, but unary.
このような場合、評価行列のエントリは、例えば星1つから星5つまでの値ではなく、単項である。
A positive value, usually represented as a 1, in the matrix therefore expresses that a user has for example viewed or purchased an item in the past.
したがって、マトリックス内の正の値（通常は1として表される）は、ユーザーが例えば過去にアイテムを閲覧または購入したことを表現する。
Most commonly, implicit feedback datasets do not contain negative feedback values, i.e., a value is either 1 or it is missing.
通常、暗黙のフィードバックデータには負のフィードバック値は含まれない。つまり、値は1であるか欠落している。
Clearly, a past purchase not necessarily means that a user has liked a certain item, and implicit feedback, i.e., observed past user behavior, can be more noisy than explicit item ratings.
また、暗黙のフィードバック、すなわち、観察された過去のユーザーの行動は、明示的な項目評価よりもノイズが多い可能性があります。

In principle, all sorts of information can be incorporated in the utility function f .
原理的には、効用関数f にはあらゆる種類の情報を取り込むことができる。
One piece of information that received special interest in the literature is that of context, which refers to the particular situation in which a recommendation is made.
その中で、特に注目されているのが、推薦が行われる特定の状況を指す「文脈」の情報である。
The current context can have a major impact on the usefulness of a particular recommendation.
この文脈は、ある推薦の有用性に大きな影響を与えることがある。
One restaurant might, for example, be a good recommendation during summer but not in winter.
例えば、あるレストランは、夏にはお勧めできるが、冬にはお勧めできないかもしれない。
Considering the time of the year as context may therefore be crucial.
そのため、1年のうちでどの時期にレコメンドされるかを考えることは、非常に重要である。
Overall, the difference to other types of side information is that the utility of an item i can be different for a specific user u, depending on the current situation.
このように、他のサイド情報との違いは、特定のユーザーuにとって、あるアイテムiの有用性が、現在の状況に応じて異なる可能性があることである。
One proposal therefore is to extend the signature of f accordingly, to make this aspect explicit [Adomavicius et al. 2022].
したがって、1つの提案は、この側面を明示するために、それに応じてfの署名を拡張することである[Adomavicius et al.2022]。
Correspondingly, we may have
これに対応する形で、我々は

$$
f : U \times I \times C \rightarrow R
$$

as an extended utility function, where C denotes the context in which a recommendation should be made.
を拡張効用関数とする。ここで、C は推薦を行うべき文脈を表す。

Generally, utility functions that make individual relevance predictions—with or without considering context—are widely used in the literature.
一般に、文脈を考慮するしないに関わらず、個人の関連性を予測する効用関数は広く文献で使用されている。
Nowadays, however, predicting individual ratings on an absolute scale, as was done in the Netflix Prize competition [Bennett et al. 2007], is not considered the most relevant problem in practice anymore.
しかし、Netflix Prize competition [Bennett et al. 2007]で行われたような絶対的な尺度で個人の評価を予測することは、現在では実務上最も重要な問題とは考えられていない。
Instead, more focus is put on creating ranked lists of suggestions, leading to the top-N recommendation task.
その代わりに、より多くの焦点は、トップN推薦タスクにつながる提案のランクリストを作成することに置かれている。
Technically, one can use the same algorithms that were designed for rating prediction problems, and rank the items based on the predicted rating.
技術的には、評価予測問題のために設計されたのと同じアルゴリズムを使用し、予測された評価に基づいて項目をランク付けすることができる。
Alternatively, learning-to-rank algorithms can be used, which do not consider the recommendable items individually, but directly aim to optimize the ranking.
また、学習型ランク付けアルゴリズムを用いることもできる。これは推薦可能な項目を個別に考慮せず、直接的にランク付けを最適化することを目的としたものである。

As a result of this changed problem setting—creating a top-N list of items instead of making point-wise predictions—an alternative utility function f of the form
このように問題設定を変更した結果、点ごとの予測ではなく、上位N個のリストを作成することになったので、代替効用関数fは次のような形になる。

$$
f: U \times L* \rightarrow R
$$

can be defined, where L ∗ is the set of all permutations up to the length of N of the powerset of I, see also [Quadrana et al. 2018].
を定義することができ、ここでL∗はIの冪集合のNの長さまでのすべての並べ換えの集合であり、[Quadrana et al. 2018]も参照されたい。
Given this function, we then recommend the list of items that maximizes the utility value R. Correspondingly, the problem when designing an algorithm is to define or learn a function that predicts the utility of length-restricted ranked lists of items.
この関数が与えられると、次に効用値Rを最大化するアイテムのリストを推奨する。 これに対応して、アルゴリズムを設計する際の問題は、長さ制限されたアイテムのランク付けリストの効用を予測する関数を定義または学習することである。

Regarding the concept of utility, note that we so far have not made any assumptions regarding how utility should be defined or measured.
実用性の概念については、これまでのところ、実用性をどのように定義し、測定すべきかについて、何ら想定していないことに留意してください。
In the past, starting with the GroupLens system, ratings were considered as proxies for utility.
過去には、GroupLensシステムから、レーティングが効用のプロキシとして考慮されていた。
The goal was to predict how a user would rate a yet unseen item and to then recommend the items with the highest predicted ratings, assuming that these items are the most useful ones.
その目的は、まだ見ぬアイテムに対してユーザーがどのような評価を下すかを予測し、予測された評価が最も高いアイテムを、最も有用なアイテムであると仮定して推薦することであった。
Note, however, that our definitions are not generally limited to consumer value, and a utility function might consider the provider profit as well, and thus consider the value perspective of more than one stakeholder, see also [Abdollahpouri et al. 2020a, Mehrotra et al. 2018b].
ただし、我々の定義は一般に消費者価値に限定されるものではなく、効用関数は提供者の利益も考慮する可能性があり、したがって複数の利害関係者の価値観も考慮することに留意されたい、［Abdollahpouri et al.2020a, Mehrotra et al.2018b］ も参照されたい。

In traditional settings, mostly utility functions of the form $f :
従来の設定においては，$f :
U×I \rightarrow R$ were considered, where each item’s utility is considered independently from other items that might be shown to a user in a single recommendation list.
U×I \rightarrow R$ という形の効用関数が検討され，各項目の効用は一つの推薦リストでユーザに表示される可能性のある他の項目から独立して考慮される．
Such an approach however does not allow us to assess the quality of top-N item lists as a whole, e.g., in terms of their diversity.
しかし，このような方法では，上位N項目リスト全体の品質，例えば，多様性の観点から評価することはできない．
Therefore, utility functions—and corresponding evaluation metrics—are nowadays commonly used that consider more than point-wise utility estimates, see also Section 1.4 on the evaluation of recommender systems.
そのため，最近では，点数化された効用推定値以上のものを考慮した効用関数とそれに対応する評価指標が一般的に用いられている（推薦システムの評価については，1.4節も参照されたい）．

## 1.3. Recommendation Algorithms 1.3. レコメンデーションアルゴリズム

The development of recommendation algorithms has naturally mirrored the evolution of the task definition, hand in hand with the design of evaluation procedures and metrics (which we discuss later in Section 1.4) suited to the task.
推薦アルゴリズムの開発は、当然ながらタスクの定義の変遷を反映し ており、タスクに適した評価手順と評価指標（これはセクション 1.4 で後述）の設計と密接に関連している。
Recommendation can be addressed, in essence, as a supervised learning problem: given examples of observed user choices, we aim to predict present or future (yet unobserved) user interests.
レコメンデーションは、本質的に教師あり学習問題として取り組むことができる。すなわち、観察されたユーザーの選択の例から、現在または将来の（まだ観察されていない）ユーザーの興味を予測することを目的とする。
Variations in the task formulation give rise to different algorithmic approaches—and different metrics are appropriate to evaluate for different tasks.
このように、タスクの定式化が異なれば、アルゴリズム のアプローチも異なり、また、タスクごとに評価するのに適したメトリッ クも異なる。

As a machine learning problem, recommendation is quite unique.
機械学習の問題としては、レコメンデーションは非常にユニークである。
What makes recommendation singular in this field is, in essence, the human factor at the core of recommendation tasks.
この分野で推薦が特異なのは、要するに推薦タスクの中核にある人間的な要素である。
In these tasks, both the input signal and the prediction target consist of or involve user behavior at their core.
この分野では、入力信号と予測対象の両方が、ユーザーの行動で構成されている、あるいは、その行動が中核にある。
This brings about a specific level of complexity compared to, for instance, recognizing shapes in an image or diagnosing a medical condition from medical tests.
これは、例えば画像中の形状を認識したり、医療検査から病状を診断したりするのとは異なる複雑さをもたらす。
Furthermore, recommendation is often not just about predicting people’s actions, but about enhancing (and hence changing) such actions by bringing awareness about potentially better choices.
さらに、推薦とは、単に人々の行動を予測するだけでなく、より良い選択であることを認識させ、その行動を向上させる（つまり、変化させる）ことである場合が多い。
What makes a recommendation good (and therefore the algorithm that produces it) thus involves a great deal of subjectivity and is a challenging question, that we discuss later in Section 1.4.
このように、何が推薦を良いものとするか（したがって、それを生成するアルゴリズム）は、非常に主観的であり、難しい問題である（1.4節で後述）。

Recommendation algorithms have been traditionally classified into collaborative and content-based [Adomavicius et al. 2022].
推薦アルゴリズムは従来、協調型とコンテンツ型に分類されてきた [Adomavicius et al. 2022]。
The latter follow the principle that people’s tastes are related to inherent item characteristics and tend to persist over time.
後者は、人々の嗜好は固有のアイテム特性に関連し、時間の経過とともに持続する傾向があるという原則に従います。
The former build, in a myriad different ways, on the presumed existence of regularities and structure in the distribution of user preferences and choices over the user-item space.
前者は、ユーザーアイテム空間におけるユーザーの嗜好と選択の分布に規則性と構造が存在すると推定し、無数の異なる方法で構築します。
For instance, some users may have non-random similarities to other users in their personal interests.
例えば、あるユーザーは、個人的な興味において、他のユーザーと非ランダムな類似性を持っている可能性がある。
Again, such structures are assumed to persist over time.
この場合も、そのような構造は時間の経過とともに持続すると仮定される。

Different algorithmic approaches have different strengths and weaknesses.
アルゴリズムによるアプローチには、それぞれ異なる長所と短所がある。
Robust and effective recommender systems therefore combine elements or entire components from different such approaches.
そのため、頑健で効果的な推薦システムは、そのような異なるアプローチの要素または全体のコンポーネントを組み合わせている。
In an aim to make algorithm categorization exhaustive, such compound solutions have been often referred to as hybrid systems.
アルゴリズム分類を網羅的に行うために、このような複合的な解決策はしばしばハイブリッドシステムと呼ばれる。
As with many machine learning or information retrieval systems, production recommender systems typically combine a core initial (commonly hybrid) algorithm that produces base item rankings, followed by post-processing algorithms, business rules (e.g. implementing marketing constraints) and fine enhancements to further improve the final recommendation ranking quality and optimizing for additional objectives [Amatriain and Basilico 2015, Covington et al. 2016].
多くの機械学習システムや情報検索システムと同様に、生産型レコメンダーシステムは一般的に、基本アイテムランキングを生成するコア初期（一般的にハイブリッド）アルゴリズムを組み合わせ、その後、後処理アルゴリズム、ビジネスルール（例えば、マーケティング制約の実装）、最終レコメンデーションランキングの品質をさらに改善し追加目的に対して最適化するための細かい拡張を行います［Amatriain and Basilico 2015, Covington et al.2016］.

### 1.3.1. Recommendation as a Machine Learning Problem 1.3.1. 機械学習問題としてのレコメンデーション

Modern recommendation algorithms tend to be formulated explicitly as a supervised machine learning task: a utility function f (in some of the aforementioned forms in the previous section) is learnt that minimizes a cost function, which involves the utility function within its definition.
現代の推薦アルゴリズムは、教師あり機械学習のタスクとして明示的に定式化される傾向がある：効用関数f（前節で述べたいくつかの形式）は、効用関数をその定義の一部として含むコスト関数を最小化するように学習される。
Cost can be, for instance, the sum of squared prediction error over available training ratings (the latter playing the part of labels in supervised machine learning terminology), or the binary cross-entropy loss of a sigmoid function, or the amount (measured through some monotonic function) of item pairs incorrectly ranked by the utility function to be learned.
コストとは，たとえば，利用可能な学習評価に対する予測誤差の二乗和（後者は教師あり機械学習用語でいうラベルの役割を果たす），シグモイド関数の二値クロスエントロピー損失，あるいは学習される効用関数によって誤ってランク付けされる項目ペアの量（何らかの単調関数によって測定），とすることが可能である．
In this formulation, recommendation algorithms are distinguished from each other in the form the utility function takes (a parameterized model), the cost function, and the procedure to minimize the latter.
この定式化において、推薦アルゴリズムは、効用関数の形式（パラメータ化されたモデル）、コスト関数、および後者を最小化する手順において互いに区別される。

An example utility function is the dot product of user and item embedding vectors3 , where the coordinates of such vectors are the parameters of the model to be learned, as we shall see in Section 1.3.3.2 below.
効用関数の例としては，ユーザとアイテムの埋め込みベクトルの内積3 があり，後述の 1.3.3.2 節で述べるように，その座標は学習するモデルのパラメータである．
The function therefore involves some arbitrary choice (of a family of functions often referred to as the hypothesis space), and learning the function typically means learning its parameters (a “model”) by fitting them to the training data (through minimization of the cost function on training labels).
したがって，関数は（仮説空間と呼ばれる関数群から）任意に選択され，関数の学習は，通常，（学習ラベルのコスト関数を最小化することにより）学習データに適合させてそのパラメータ（「モデル」）を学習することを意味する．
Some algorithms however do not express an explicit cost function, and the utility function is defined heuristically rather than learned.
しかし、アルゴリズムによっては、明示的なコスト関数を表現せず、効用関数は学習ではなく、発見的に定義される。
This is the case, for instance, of the common nearest-neighbors collaborative filtering formulation that we overview later in Section 1.3.3.1.
これは例えば、後述のセクション1.3.3.1で概観する一般的な最近傍協調フィルタリングの定式化のケースである。
In either case, the utility function has hyperparameters that need to be optimized, usually taking a separate validation subset out of the training data.
いずれの場合も、効用関数は最適化する必要のあるハイパーパラメータを持ち、通常は学習データから別の検証サブセットを取り出します。
The ultimate goal of all algorithms is to maximize some final metric(s) of interest, such as precision, recall, or revenue—this is why some algorithms take the final metric, or a more tractable approximation thereof, as the objective function to be optimized.
すべてのアルゴリズムの最終目標は、精度、再現率、収益などの最終的な評価指標を最大化することです。

Next, we provide an overview of the main algorithmic approaches and principles in the recommendation field.
次に、推薦分野における主なアルゴリズムアプローチと原理を概観する。
We start by briefly discussing different types of input data for recommendation, which determine broad differences in the algorithmic approaches developed thereupon.
まず，推薦のためのさまざまな入力データについて簡単に説明し，そこから開発されるアルゴリズムアプローチの大きな違いを明らかにする．
Each algorithmic family may deserve a paper (or an entire book) by itself.
各アルゴリズムはそれ自体で1つの論文（あるいは1冊の本）に値するかもしれない．
Therefore, we will provide only a broad overview here and focus on some main highlights.
そこで，ここでは大まかな概要のみを説明し，いくつかの主要なハイライトに焦点を当てることにする．

### 1.3.2. Characterizing Approaches Based on their Input Data 1.3.2. 入力データによるアプローチの特徴づけ

Recommendation algorithms can be based on input data of different nature.
レコメンデーションアルゴリズムは、さまざまな性質の入力データに基づくことができる。
Probably the most common data source for recommendation—and we might add, the one enabling the most powerful approaches—are records of logged user-item interactions: the rating matrix, as already discussed.
おそらく最も一般的な推薦のためのデータソース、そして最も強力なアプローチを可能にするものは、すでに議論したように、記録されたユーザーとアイテムの相互作用の記録、つまり評価行列である。
When this is the only input of an algorithm we say the algorithm follows a collaborative filtering approach [Adomavicius and Tuzhilin 2005].
これがあるアルゴリズムの唯一の入力であるとき、そのアルゴリズムは協調フィルタリングのアプローチに従っていると言います[Adomavicius and Tuzhilin 2005]。
Collaborative filtering is based on the abstract principle that people can benefit from the experience and discoveries of other people, and not just their own, in making future choices.
協調フィルタリングは，人々が将来の選択をする際に，自分の経験だけでなく，他の人々の経験と発見から利益を得ることができるという抽象的な原理に基づいている．
The simplicity of this principle and the high potential of collective data as a source for prediction are also the Achilles heel of collaborative filtering as a pure approach: where the interaction matrix is sparse, the algorithm struggles to produce reliable predictions, due to a lack of sufficient input information.
この原理の単純さと予測のためのソースとしての集合データの高い可能性は、純粋なアプローチとしての協調フィルタリングのアキレス腱でもある：相互作用行列が疎である場合、アルゴリズムは十分な入力情報の欠如のために、信頼できる予測を生成するのに苦労する。
Collaborative techniques may fail to deliver proper recommendations in cold start situations where little interaction has yet been recorded, as is the case at the early stages of a new deployed system, or whenever a new user or a new item enter the system.
協調技術は、新しいシステムの初期段階や、新しいユーザーやアイテムがシステムに入るときのように、相互作用がほとんど記録されていないコールドスタート状況では、適切な推奨を提供できないかもしれません。
However, when sufficient interaction records are available, collaborative filtering is one of the most effective and powerful approaches.
しかし、十分なインタラクションの記録がある場合には、協調フィルタリングは最も効果的で強力なアプローチの1つである。

All other input that a recommendation algorithm can take beyond user-item interactions is often referred to as side information, see Section 1.3.6.
推薦アルゴリズムがユーザーアイテム間の相互作用を超えて取り得る他のすべての入力は、しばしばサイド情報と呼ばれます（セクション1.3.6参照）。
Using such information is a good complement to collaborative filtering, particularly in sparse regions of the user-item matrix.
このような情報を利用することは、特にユーザー・アイテム行列の疎な領域において、協調フィルタリングを補完するのに適しています。
A most common type of side information is any available data and metadata directly associated to the items, to which we may refer as item features: taxonomic classifications (e.g., movie genre, music style, online store section), tags, free text associated to the items (e.g., product descriptions and reviews), etc.
サイド情報の最も一般的なタイプは、アイテムに直接関連する利用可能なデータとメタデータで、アイテムの特徴と呼ぶことがあります：分類学的分類（例：映画のジャンル、音楽のスタイル、オンラインストアのセクション）、タグ、アイテムに関連するフリーテキスト（例：製品の説明やレビュー）などです。
Algorithms that solely use such data are referred to as being content-based [Pazzani and Billsus 2007].
このようなデータのみを利用するアルゴリズムは、コンテンツベースと呼ばれる[Pazzani and Billsus 2007]。
Instead of turning to other users for hints on what a customer might like, pure content-based approaches just focus on one user at a time, considering the interaction records of the target user4—in particular, the features of the items the user engaged with, and the features of the items to be recommended.
コンテンツベースのアプローチは、他のユーザーを参考にするのではなく、一度に一人のユーザーに焦点を当て、ターゲットユーザーの対話記録4、特にユーザーが関与したアイテムの特徴、推奨されるアイテムの特徴を検討します。
Several other information sources can be effectively exploited by a recommender system to enhance the effectiveness and value of recommendation, such as social interactions between users [Guy 2022], data about the user (e.g., demographic information), contextual information (e.g., user and
このほかにも、推薦の有効性と価値を高めるために、推薦システムが有効に活用できる情報源がいくつかあります。たとえば、ユーザー間の社会的相互作用 [Guy 2022] 、ユーザーに関するデータ（たとえば、デモグラフィック情報）、文脈情報（たとえば、ユーザーと

When substantial interaction data is available, collaborative filtering can be more effective than other approaches as a base algorithmic core, not just in terms of delivering accurate predictions, but also in providing users with rich options beyond their individual prior experience [Vargas and Castells 2011].
このような場合，協調フィルタリングは，単に正確な予測を行うだけでなく，ユーザに個々の過去の経験を超えた豊かな選択肢を提供するという点で，アルゴリズムの基本的なコアとして他のアプローチよりも効果的です [Vargas and Castells 2011]．
These algorithms are moreover fairly general and domainagnostic, as they make no assumption about what the items are.
また、これらのアルゴリズムは、アイテムが何であるかを仮定しないため、かなり一般的であり、ドメインにとらわれないものである。

### 1.3.3. Collaborative Filtering 1.3.3. 協調フィルタリング

#### 1.3.3.1. Nearest Neighbors 1.3.3.1. ニアレストネイバーズ

The earliest collaborative algorithms were inspired by a typical word-of-mouth human behavior where a person takes advice from trusted friends when making a decision—one of the main sources for guidance when people make decisions and choices.
初期の協調アルゴリズムは、人が意思決定を行う際に信頼できる友人から助言を得るという典型的な人間の口コミ行動（人が意思決定や選択を行う際の主な指針の1つ）から着想を得ていた。
Following this metaphor, socalled k-nearest-neighbor (kNN) algorithms suggest choices defined as the weighted average of the advice of the target user’s friends.
このメタファーに基づき、k-nearest-neighbor (kNN) アルゴリズムと呼ばれるものは、対象となるユーザーの友人のアドバイスの加重平均として定義される選択肢を提案する。

Following this heuristic intuition, recommendation may be viewed as a regression problem, where a kNN algorithm predicts the level of preference of a user u for an item i as a linear combination of the observed preferences for i in a subset of selected users: the target user’s neighbors N[u].
この発見的直観に従うと、推薦を回帰問題とみなすことができる。kNNアルゴリズムは、あるユーザーuのアイテムiに対する嗜好レベルを、選択されたユーザーの部分集合（ターゲットユーザーの近隣N[u]）におけるiに対する観測値の線形結合として予測するものである。
Following the notation in the previous section, items are ranked by the following utility function:
前節の表記法に従い、アイテムは以下の効用関数によってランク付けされる。

$$
\tag{1.2}
$$

where Ci is a normalizing term, and r(v,i) 6= 0
ここで、Ci は正規化項であり、r(v,i) 6= 0

The neighborhood N[u] is usually picked as the top k most similar users to u, where k becomes a hyperparameter of the algorithm.
近傍領域N[u]は通常，uに最も類似する上位k人のユーザーを選択し，ここでkはアルゴリズムのハイパーパラメータとなる．
Neighborhood selection is nonetheless a modular operation that has been the object of multiple variations and enhancements.
しかし，近傍探索はモジュール化された操作であるため，様々なバリエーションや拡張が行われてきました．
When recommendation was addressed as rating prediction, the kNN score in Equation 1.2 above was normalized by Ci = 1
レコメンデーションが視聴率予測として扱われたとき、上記の式 1.2 の kNN スコアは Ci = 1 で正規化されました。

Multiple further variations of the kNN scheme arise from here, such as the widely used item-based version (which roughly swaps the role of users and items), multiple similarity functions, different neighbor selection approaches, and so forth.
ここから、広く使われているアイテムベースのバージョン（ユーザーとアイテムの役割を大まかに入れ替える）、複数の類似性関数、異なる近傍選択アプローチなど、kNN スキームの複数のさらなるバリエーションが生じる。
Though kNN has been developed as a heuristic scheme, Canamares and Castells [Ca ˜ namares and Castells 2017] showed ˜ that kNN can be given a probabilistic formalization where the ranking function is derived from an objective function to be maximized: the expected number of recommended items the user will like.
kNN は発見的なスキームとして開発されてきたが，Canamares and Castells [Ca ˜ namares and Castells 2017] は kNN が最大化されるべき目的関数：ユーザーが好むであろう推奨アイテムの期待数からランキング関数が導かれる確率的形式化を与えられることを示した〜。
For a more comprehensive review of kNN variants see [Nikolakopoulos et al. 2022].
kNN の変種のより包括的なレビューについては [Nikolakopoulos et al. 2022] を参照のこと。

kNN is an old idea [Linden et al. 2003] yet it remains a competitive approach today [Ferrari Dacrema et al. 2021, Ludewig et al. 2021].
kNNは古いアイデア[Linden et al. 2003]であるが、今日でも競争力のあるアプローチである[Ferrari Dacrema et al. 2021, Ludewig et al. 2021]。
It is very easy to understand, simple to implement, and computationally inexpensive compared to other recent, more complex approaches.
他の最近の複雑なアプローチと比較して、非常に理解しやすく、実装も簡単で、計算も安価である。
As such, it is an advisable reference baseline to include in experimental recommender systems research [Canamares and Castells 2018, Cremonesi et al. 2010].
そのため、実験的なレコメンダーシステム研究に含めるべき参考ベースラインとして推奨される[Canamares and Castells 2018, Cremonesi et al.］

#### 1.3.3.2. Matrix Factorization 1.3.3.2. 行列の因数分解

By the mid 2000s matrix factorization became popular in the field and very soon became the preferred collaborative filtering approach, due to its empirical effectiveness, relative simplicity, and flexibility as a framework enabling multiple algorithmic developments and variations.
2000年代半ばになると，行列因子法はこの分野で人気を博し，経験則に基づく有効性，比較的単純であること，複数のアルゴリズムの開発とバリエーションを可能にするフレームワークとしての柔軟性から，すぐに協調フィルタリングのアプローチとして好まれるようになりました．
Matrix factorization is based on the assumption that the interests of users can be described in a low-dimensional space of latent factors that synthesize the subjacent properties of items that determine why a person may like them [Koren et al. 2009].
行列分解は、ユーザーの興味は、人がなぜそのアイテムを好むかを決定するアイテムの隣接する特性を合成する潜在的要因の低次元空間で記述できるという仮定に基づいている[Koren et al.］
In this perspective, users and items are assumed to be describable as vectors in a common latent factor vector space, in such a way that users with similar tastes would have similar factor vectors, and so would items that please similar users.
この観点から、ユーザーとアイテムは共通の潜在的因子ベクトル空間におけるベクトルとして記述可能であると仮定する。
These low-dimensional vectors have come to be referred to as embeddings in the recent literature, making a connection to similar techniques in fields such as natural language processing and information retrieval [Mikolov et al. 2013, Pennington et al. 2014].
このような低次元ベクトルは最近の文献では埋め込みと呼ばれるようになり、自然言語処理や情報検索などの分野における同様の技術との関連性が指摘されている[Mikolov et al.］

The latent factors do not necessarily correspond to actual properties of items or user traits as we would probably represent them in our human understanding.
潜在的な要因は、私たちが人間の理解の中でおそらく表現するであろうアイテムの実際の特性やユーザーの特徴に必ずしも対応していない。
They are handled as abstract dimensions for which users and items are given values by an algorithmic approach, and are usually not interpretable by eye inspection or a clear natural intuition.
それらは、アルゴリズム的アプローチによってユーザーやアイテムに値が与えられる抽象的な次元として扱われ、通常、目視や明確な自然な直感では解釈することができないものである。
Matrix factorization algorithms only require deciding how many factors we wish consider—which becomes a hyperparameter of the approach—but not what these factors are, other than axes of a multidimensional vector space.
行列分解アルゴリズムでは、考慮したい要素の数を決めることだけが必要で、これはアプローチのハイパーパラメータになりますが、これらの要素が何であるかは、多次元ベクトル空間の軸以外のものではありません。

Formally, for a k-dimensional factor space, users u ∈ U and items i ∈ I are represented by vectors pu ∈ Rk , qi ∈ Rk , where the coordinates pu,z ∈ R, pi,z ∈ R represent how interested user u is in factor z,
形式的には、k 次元因子空間において、ユーザ u（U）とアイテム i（I）は、ベクトル pu∈Rk , qi∈Rk で表され、座標 pu,z∈R, pi,z∈R は、ユーザ u が因子 z にどれだけ興味があるかを表している。
and how much of factor z is present in item i, respectively—the higher the z coordinate value, the more the user interests are about this factor, and the more important the factor is in the nature of the item.
z座標の値が高いほど、その因子に対するユーザーの関心が高く、その因子がアイテムの性質においてより重要であることを表している。
Based on this representation, an additional assumption is made: that the interest of a user u for an item i can be captured by the dot product of their latent vectors—following our utility function notation, f(u,i) = q t i pu.
この表現に基づき、ある項目iに対するユーザuの興味は、両者の潜在ベクトルの内積で捉えることができる（効用関数表記に従えば、f（u，i）＝q t i pu）、という追加の仮定がなされる。

The common approach to produce the latent vectors is by minimization of a cost function R (also referred to as risk or expected loss in the empirical risk minimization machine learning framework [Vapnik 1998]), which generally involves the error in predicting the training data with some regularization.
潜在ベクトルを生成する一般的なアプローチは、コスト関数R（経験的リスク最小化機械学習フレームワーク[Vapnik 1998]ではリスクまたは期待損失とも呼ばれる）の最小化であり、一般的には学習データを予測する際の誤差を何らかの正則化で含むものです。
For instance, a basic formulation would be:
例えば、基本的な定式化は以下のようになる。

$$
\tag{1.3}
$$

The term added to the squared difference is a common regularization factor to avoid overfitting, where k · k represents the L2 norm, and λ is a hyperparameter that is tuned by cross validation.
二乗差に加える項はオーバーフィッティングを避けるための一般的な正則化係数で、k - k は L2 ノルムを表し、λ はクロスバリデーションによって調整されるハイパーパラメーターである。
The minimization is often solved for by stochastic gradient descent or alternating least squares, resulting in easy implementations [Koren et al. 2009].
この最小化は、しばしば確率的勾配降下法または交互最小二乗法により解かれ、その結果、実装が容易になる[Koren et al.］
Once the latent vectors are learned by the algorithm, the dot product f(u,i) = q t i pu is used as the ranking function for recommendation.
アルゴリズムによって潜在ベクトルが学習されると、推薦のためのランキング関数として、ドットプロダクト f(u,i) = q t i pu が用いられる。

The summation in the cost function can be limited to the user-item pairs for which training data are available, but it is common to extend the sum to all or a sample subset of unobserved user-item preferences [Koren et al. 2009].
コスト関数の総和は，学習データが利用可能なユーザー項目ペアに限定することができますが，観察されていないユーザー項目嗜好のすべてまたはサンプルサブセットに拡張することが一般的です [Koren et al.2009]．
In the latter case, a value needs to be imputed to the missing preference observations, which can be done in different ways (such as a constant parameter value or a randomized value).
後者の場合，欠落した選好オブザベーションに値をインプットする必要があり，これはさまざまな方法（定数パラメータ値や無作為化値など）で行うことができる．
The error term in Equation 1.3 can be weighted differently for every user-item pair, often representing confidence in the corresponding (observed or imputed) preference data point.
式1.3の誤差項は、ユーザー-アイテム・ペアごとに異なる重みづけが可能で、多くの場合、対応する（観測または帰属された）嗜好データ・ポイントに対する信頼性を表します。
Most usually, two different weight values are used for pairs having and not having training data [Hu et al. 2008].
ほとんどの場合、学習データを持つペアと持たないペアで2つの異なる重み付け値が使用されます[Hu et al.2008]。
The combination of error weighting and missing value imputation reflect different nuances in the recommendation task and result in different algorithmic behavior (see e.g. [Steck 2013]).
誤差の重み付けと欠損値のインピュテーションの組み合わせは，推薦タスクの異なるニュアンスを反映し，異なるアルゴリズム動作をもたらします（例えば，[Steck 2013]を参照してください）．
Besides these configuration options, matrix factorization has been rich in a myriad of further variations, such as summing item, user and global bias terms as additional parameters in the rating representation q t i pu [Koren et al. 2009], temporal awareness [Koren 2009], probabilistic formulations [Hofmann 2004, Salakhutdinov and Mnih 2007], and many other elaborations.
これらの構成オプションに加え，行列分解は，評価表現q t i puの追加パラメータとして項目，ユーザ，グローバルバイアス項の合計[Koren et al. 2009]，時間認識[Koren 2009]，確率的定式化[Hofmann 2004, Salakhutdinov and Mnih 2007] など，無数の更なるバリエーションを豊富に有している．
In particular, variations in the cost function have given rise to entire new approaches, which we summarize next.
特に、コスト関数のバリエーションによって、全く新しいアプローチが生み出されており、次にその概要を述べる。

### 1.3.4. Learning to Rank 1.3.4. ランク付けの学習

With the realization that the effectiveness of recommendation in real scenarios relies more on item ranking than on point-wise rating prediction, a shift emerged in the field towards addressing recommendation as a learning to rank (LTR) problem, drawing from a similar earlier trend in the information retrieval field [Joachims 2002].
このような背景のもと、情報検索の分野と同様に、推薦の有効性を評価するために、項目順位を学習する問題(LTR)が提案された [Joachims 2002]．
Broadly speaking, LTR involves the introduction of loss functions that explicitly involve item ordering rather than rating error or interaction prediction error [Rendle et al. 2009].
LTRは大まかに言えば、評価誤差や相互作用予測誤差ではなく、項目順序に明示的に関与する損失関数を導入するものである [Rendle et al.2009]。
In different possible ways, the cost functions typically represent the amount of “contradiction” between the rankings produced by the model to be learned, and how items should be ranked according to the training preference values.
様々な可能性がある中で、コスト関数は一般的に、学習されるモデルによって生成されるランキングと、学習されたプリファレンス値に従ってアイテムがどのようにランク付けされるべきかの間の「矛盾」の量を表す。
In other words, the model is trained to maximize order-wise agreement with the available observations.
言い換えれば、モデルは利用可能なオブザベーションとの順序的な一致を最大化するように学習される。
Most methods take a pairwise approach, where the “ranking error” is defined in terms of incorrectly ranked item pairs:
ほとんどの方法はペアワイズアプローチをとり、「ランキングエラー」は間違ってランク付けされた項目ペアの観点から定義される。

$$
R(\theta) = \sum_{u} \sum_i \sum_j l(u,i,j|\theta)
$$

where θ are the parameters of the recommendation model, and the loss $l(u,i, j
θ)$ quantifies how much in contradiction to the available observations the model θ ranks i and j for u (and $l$ involves the utility function f—the model—to be learned). This is summed over all pairs of items i, j that u has available training data for.

A representative and effective example in this area is Bayesian Personalized Ranking (BPR) [Rendle et al. 2009], which has become a common reference and baseline in the literature. Ranking inconsistency in BPR is expressed and developed in terms of the probability that the scores predicted by the learned model θ rank pairs of items in contradiction to the training rating data: essentially, and omitting details, $l(u,i, j) = 1_{r(u,i)>r(u, j)}P(\text{j is ranked above i for u}
θ)P(θ)$. The probability of ranking precedence is smoothed (for differentiability) as a logistic sigmoid of the ranking score difference.

Many alternatives to such a scheme have been proposed on a similar principle.
このようなスキームに対して、同様の原理で多くの代替案が提案されています。
For instance, also in a pairwise approach, RankALS [Takacs and Tikk 2012] essentially takes $l(u,i, j) = ((r(u,i) − r(u, j))
例えば、同じくペアワイズアプローチのRankALS [Takacs and Tikk 2012] は、基本的に$l(u,i,j) = ((r(u,i) - r(u,j)))
− (q^t_i p_u − q^t_j p_u))^2$ as the core pairwise ordering error to be minimized, and alternating least squares instead of gradient descent as the minimization procedure.

- (q^t_i p_u - q^t_j p_u))^2$ を最小化すべきペアワイズ順序誤差のコアとし、最小化手順として勾配降下の代わりに交互最小二乗法を採用しています。
  Other approaches introduce a target ranking evaluation metric—such as nDCG, Mean Average Precision (MAP) or Mean Reciprocal Rank (MRR)—in the objective function, i.e., the objective approximates how much is lost in the metric by a suboptimal item ordering.
  他のアプローチでは、nDCG、平均平均精度（MAP）、平均逆順位（MRR）などの目標順位評価指標を目的関数に導入し、すなわち、最適でない項目の順序付けによって指標内でどれだけ失われるかを目的関数で近似している。
  For instance, CLiMF [Shi et al. 2012] defines the objective function as a smooth lowerbound approximation of MRR.
  例えば，CLiMF [Shi et al. 2012]は，目的関数をMRRの滑らかな下界近似として定義している．
  These methods are referred to as listwise in the LTR literature [Liu 2009], because even though the loss function is still often evolved into pairwise form, it reflects a ranking goodness function (the target evaluation metric) rather than a metricagnostic item pair classification error in a binary order.
  これらの方法はLTRの文献[Liu 2009]ではリストワイズと呼ばれている．なぜなら，損失関数は依然としてペアワイズ形式に発展することが多いが，それは2値順のメトリックにとらわれない項目ペア分類誤差ではなく，ランキングの良さ関数（目標評価メトリック）を反映するからである．

### 1.3.5. Neural Recommendation 1.3.5. ニューラル・レコメンデーション

While matrix factorization assumes the dot product of latent vectors as the scoring function, one may consider more complex, not necessarily linear5 utility scoring for recommendation.
行列分解は潜在的なベクトルの内積をスコアリング関数として想定しているが、推薦のために、より複雑で、必ずしも線形5ではない効用スコアリングを考慮することもできる。
One such possibility is to use neural networks as a particular family of non-linear functions that have well-studied properties and training techniques [He et al. 2017, Zhang et al. 2022].
そのような可能性の1つは、特性や学習技術がよく研究されている非線形関数の特定のファミリーとしてニューラルネットワークを使用することである［He et al.2017, Zhang et al.2022］ 。
After revolutionizing machine learning application domains such as computer vision, speech recognition, or natural language processing, deep learning has gained blazing popularity in recent years as a basis for devising a wide variety of recommendation approaches.
コンピュータビジョン、音声認識、または自然言語処理などの機械学習応用領域に革命をもたらした後、深層学習は、多種多様な推薦アプローチを考案するための基礎として、近年、輝かしい人気を獲得している。
A comprehensive coverage of this area exceeds the scope of this paper—we provide instead a summarized overview; the reader is referred to e.g., [Zhang et al. 2022] for a wider survey.
本論文では、この分野を包括的にカバーすることはできないので、その代わりに概要を説明する。

Several technical and strategic reasons motivate an optimistic prospect for deep learning as an approach to recommendation: the ability to approximate any prediction function; efficient training (in comparison to other machine learning approaches at comparable complexity); smooth integration of heterogeneous data sources (including unstructured content), data dimensions and predictive signals; feature engineering effort savings; proved empirical effectiveness in other machine learning domains; and a growing availability of software resources and knowledge derived from a thriving activity in deep learning in many domains and fields.
それは、あらゆる予測関数を近似できること、（同等の複雑さの他の機械学習アプローチと比較して）効率的なトレーニング、（非構造化コンテンツを含む）異種データソース、データ次元、予測信号の円滑な統合、特徴工学の労力削減、他の機械学習領域における実証済みの効果、多くのドメインや分野における深層学習の活発な活動から得られるソフトウェアリソースや知識の増大、といった技術的・戦略的理由である。
Furthermore, as universal function approximators, neural networks can be seen as a smooth generalization of virtually any simpler model (such as dot-product in matrix factorization as described earlier).
さらに、普遍的な関数近似器であるニューラルネットワークは、事実上あらゆる単純なモデル（前述の行列分解におけるドットプロダクトなど）の滑らかな一般化と見なすことができます。
From this perspective, a neural vs. non-neural dichotomy may become moot, strictly speaking.
このような観点から、ニューラルか非ニューラルかという二分法は、厳密に言えば無意味になるかもしれない。
“Depth” in deep learning suggests however that the opportunity to grow and handle complexity is actually being leveraged by “bigger” layered models.
しかし、深層学習における「深さ」は、複雑さを成長させて処理する機会が、実際には「より大きな」レイヤーモデルによって活用されていることを示唆している。

Neural networks provide arbitrarily high expressive power to capture complex relations in the user-item space, that matrix factor models may fail to grasp.
ニューラルネットワークは、行列因子モデルが把握できない可能性のある、ユーザー・アイテム空間における複雑な関係を捉えるために、任意に高い表現力を提供する。
At the top layer (the output layer), the loss function can involve a pointwise (rating or binary prediction error) [He et al. 2017] or pairwise (ranking error) element [Song et al. 2018] similar to other matrix factorization and LTR approaches discussed earlier.
最上層（出力層）において、損失関数は、先に議論した他の行列因子法及びLTRアプローチと同様に、ポイントワイズ（評価又はバイナリ予測誤差）［He et al. 2017］又はペアワイズ（ランキング誤差）要素［Song et al.2018］を含むことができる。
The generality of neural architectures further enables the smooth integration of side information in addition to user-item interaction.
ニューラル・アーキテクチャの一般性は、さらに、ユーザー・アイテムの相互作用に加えて、サイド情報の円滑な統合を可能にする。
We discuss the use of side-information in recommendation more generally later in Section 1.3.6.3.
推薦におけるサイド情報の利用については、後ほどセクション 1.3.6.3 でより一般的に説明します。
The elaborations and combinations that can be developed in this area are as wide as imagination can afford.
この分野で開発できる精巧さと組み合わせは、想像力の許す限り広い範囲に及ぶ。
A huge variety of complex network architectures have been proposed in the literature using network structures such as autoencoders [Liang et al. 2018], convolutional neural networks [Tang and Wang 2018, Yuan et al. 2019], recurrent neural networks [Hidasi and Karatzoglou 2018, Wu et al. 2017], and attention layers [Kang and McAuley 2018], to name just a few.
オートエンコーダ［Liang et al. 2018］、畳み込みニューラルネットワーク［Tang and Wang 2018, Yuan et al. 2019］、リカレントニューラルネットワーク［Hidasi and Karatzoglou 2018, Wu et al. 2017］、および注意層［Kang and McAuley 2018］などのネットワーク構造を使って膨大な種類の複合ネットワークアーキテクチャが文献で提案されています。
Particular architectures have been developed for specific tasks, such as session-based recommendation discussed later in Section 2.1.
特定のアーキテクチャは、セクション 2.1 で後述するセッションベースの推薦のような特定のタスクのために開発されている。
Interestingly, the best performance in recommendation is sometimes achieved with shallower neural models compared other domains [Anelli et al. 2022, Steck 2019].
興味深いことに、推薦における最高のパフォーマンスは、他のドメインと比較してより浅いニューラルモデルで達成されることがある[Anelli et al. 2022, Steck 2019]。

Deep learning has proved to be empirically effective in recommendation, and steps have been taken towards its adoption in industry [Covington et al. 2016, Okura et al. 2017, Wu and Grbovic 2020].
ディープラーニングは推薦において経験的に有効であることが証明され、産業界への採用に向けて歩みを進めている［Covington et al.2016、Okura et al.2017、Wu and Grbovic 2020］。
A certain hype in this domain may have also induced a degree of noise and haste in early empirical analyses that sometimes make it difficult to get a precise perception of the actual effectiveness of neural approaches, or any conditions for which they may be best suited [Ferrari Dacrema et al. 2021, Garg et al. 2019, Kouki et al. 2020, Ludewig et al. 2021, Rendle et al. 2020, Steck 2019].
この領域におけるある種の誇大広告は、初期の実証分析にある程度のノイズや焦りを誘発し、ニューラルアプローチの実際の効果や、それらが最も適していると思われる条件について正確な認識を得ることを困難にすることもある［Ferrari Dacrema et al.2021, Garg et al.2019, Kouki et al.2020, Ludewig et al.2021, Rendle et al.2020, Steck 2019］。
Clear effectiveness improvements have been found in specific tasks such as sequential recommendation [Sun et al. 2019b], and for specific conditions when, for instance, side information or massive data are available.
逐次推薦のような特定のタスクや、例えば側面情報や膨大なデータが利用可能な場合の特定の条件において、明確な効果向上が見出されている[Sun et al. 2019b]。

Deep learning can often also simplify and reduce feature engineering efforts.
また、深層学習は、しばしば、特徴量エンジニアリングの作業を簡略化し、削減することができる。
See [Steck et al. 2021] for a discussion of deep learning for recommendations at Netflix.
Netflix における推薦のためのディープラーニングの議論については [Steck et al.
Deep learning faces similar challenges in recommendation as it does in other domains: a large number of hyperparameters to tune, a heavy training cost tradeoff to reach the effectiveness potential, the need for massive data availability, and a black box nature involving interpretability and explainability challenges [Afchar and Hennequin 2020].
ディープラーニングはレコメンデーションにおいても他の領域と同様の課題に直面しています：チューニングすべきハイパーパラメータの数が多いこと、有効性の可能性に到達するための重い学習コストのトレードオフ、大量のデータ利用の必要性、解釈可能性と説明可能性の課題を含むブラックボックス的性質[Afchar and Hennequin 2020]などです。
As a result, the cost and complexity of neural approaches may not necessarily always pay off in enhanced effectiveness as a universal solution for all recommendation settings and problems [Ferrari Dacrema et al. 2021, Rendle et al. 2020].
その結果、ニューラルアプローチのコストと複雑さは、すべての推薦設定や問題に対する普遍的な解決策として、必ずしも有効性の向上で報われるとは限らない［Ferrari Dacrema et al.2021, Rendle et al.2020］ 。
On the other hand, the data richness and volume often required to make the best of deep recommendation architectures is not always within reach of research outside corporate boundaries.
一方、深層レコメンデーションアーキテクチャを最大限に活用するために必要なデータの豊富さや量は、企業の枠を超えた研究では必ずしも手の届くものではありません。
Neural recommendation is nonetheless a thriving area where a profuse stream of work is being published in top tier research outlets as we speak, and industry is striving to leverage its potential [Cen et al. 2020, Covington et al. 2016, Feng et al. 2020, Steck et al. 2021].
しかし、ニューラル・レコメンデーションは盛んな分野であり、多くの研究が一流の研究機関で発表されており、産業界はその潜在能力を活用しようと努力しています[Cen et al.］
We suggest the reader to follow through recent literature and surveys [Zhang et al. 2022] and to stay tuned to ongoing developments and future potential breakthroughs.
我々は、読者が最近の文献や調査[Zhang et al. 2022]をフォローし、進行中の開発と将来の潜在的なブレークスルーに注目することをお勧めします。

### 1.3.6. Content-based and Hybrid Recommender Systems 1.3.6. コンテンツベース・ハイブリッドレコメンダーシステム

Collaborative filtering (CF) methods, as discussed in the previous section, are highly effective in many application scenarios due to their ability to detect and utilize preference or behavior patterns in a user community.
前節で述べたように、協調フィルタリング（CF）手法は、ユーザコミュニティの嗜好や行動パターンを検出し、活用することができるため、多くの応用場面で非常に有効である。
Furthermore, they are particularly good at helping users to discover types of content that were previously unknown to them, e.g., by considering preferences of like-minded users.
さらに、同じ考えを持つユーザーの嗜好を考慮することで、ユーザーがそれまで知らなかったタイプのコンテンツを発見することを特に得意とする。
One intriguing aspect of CF methods is that they are able to accomplish this even without knowing anything about the items themselves, for example, an item’s category in an e-commerce store.
また、CF手法は、例えばECショップの商品カテゴリなど、商品そのものについて何も知らなくても、これを実現することができる点が魅力的である。

However, in cases where we dispose of such knowledge about the items and a user’s preference towards such individual item properties, it may of course make sense to consider it in the recommendation processes.
しかし、このようなアイテムに関する知識や、そのようなアイテムに対するユーザーの嗜好を捨てれば、推薦プロセスで考慮することはもちろん意味がある。
For example, if we know that a user usually prefers certain movie genres or types of news, it is only intuitive to recommend more content of the same type.
例えば、ある映画のジャンルやニュースの種類を好むと分かれば、同じようなコンテンツをより多く推薦することは直感的です。
Moreover, in case we do not have logged transaction or rating data yet, i.e., if the user has not rated many items yet (user cold-start) or if there are new items in the catalog without purchase history (item cold-start), collaborative filtering methods may not work well.
また、取引や評価のログがまだない場合、つまり、ユーザーがまだ多くのアイテムを評価していない場合（ユーザーコールドスタート）や、カタログに購入履歴のない新しいアイテムがある場合（アイテムコールドスタート）、協調フィルタリング手法がうまく機能しない可能性がある。

#### 1.3.6.1. Pure Content-based Systems 1.3.6.1. 純粋なコンテンツベースのシステム

In such cases, when there is little or no collaborative information available, one option is to match user-individual past preferences with knowledge about item features.
このような場合、連携情報がほとんどないときには、ユーザ個人の過去の嗜好とアイテムの特徴に関する知識を照合することが一つの選択肢となる。
Historically, this process is called content-based filtering6 .
歴史的に、このプロセスはコンテンツベースフィルタリングと呼ばれている6 。
Technically, many early content-based filtering methods were based on ideas and techniques from information retrieval.
技術的には、初期のコンテンツベースフィルタリングの多くは、情報検索のアイデアと技術に基づいていた。
Both in recommendation and retrieval scenarios, the goal is to identify and rank a set of relevant documents.
推薦や検索のシナリオでは、関連する文書の集合を特定し、ランク付けすることが目標とされる。
While in the IR case the starting point is a (search) query, the retrieval process in a recommender system is based on a content-based user profile.
IR の場合、出発点は（検索）クエリであるが、推薦システムにおける検索プロセスは、コンテンツに基づくユーザープロファイルに基づくものである。

On a general level, content-based recommendation can be characterized as follows [Adomavicius and Tuzhilin 2005]:
一般的なレベルでは、コンテンツベースの推薦を次のように特徴づけることができる [Adomavicius and Tuzhilin 2005]。

$$
\tag{1.4}
$$

where the predicted relevance f for a given user u and item i is based on a scoring function score which matches a content-based profile of u with the content features of an item i.
ここで、与えられたユーザuとアイテムiの予測される関連性fは、uのコンテンツベースのプロファイルとアイテムiのコンテンツの特徴をマッチングさせるスコアリング関数スコアに基づくものである。

Various ways of implementing the details of such a content-based approach are possible.
このようなコンテンツベースのアプローチの詳細を実装する方法は、様々なものが考えられる。
In case where textual descriptions of an item i are available, a traditional way would be to represent the items using a TF-IDF (Term-Frequency Inverse Document Frequency) encoding.
項目iについてテキストによる記述がある場合、従来はTF-IDF（Term-Frequency Inverse Document Frequency）符号化を使って表現する方法がある。
In such an implementation, the function Content(i) would return a vector of real values, where each element of the vector corresponds to a term (word), and the value indicates the importance of the term.
このような実装では、関数Content(i)は実数値のベクトルを返し、ベクトルの各要素は用語（単語）に対応し、値は用語の重要度を示す。
The importance values in a TF-IDF encoding are determined by multiplying two relatively simple counting statistics, TF and IDF.
TF-IDF符号化における重要度の値は、TFとIDFという二つの比較的単純な計数統計の掛け算で決定される。
The term frequency TF corresponds to the number of times a word appears in the given document i, usually normalized to account for different document lengths.
用語頻度TFは、与えられた文書iに単語が出現する回数に相当し、通常は異なる文書の長さを考慮して正規化される。
The Inverse Document Frequency IDF in contrast indicates how “informative” a term is in the given document collection.
これに対して逆文書頻度IDFは、ある用語が与えられた文書集合の中でどれだけ「情報量が多い」かを示す。
The underlying logic is that if there is a term that appears in almost all documents, it carries little information to distinguish one document from each other.
基本的な論理は、ほとんどすべての文書に出現する用語がある場合、その用語はある文書と他の文書を区別するための情報をほとんど持っていないということである。

The next question is how to represent the interest profile of a user u, i.e., how to implement the function ContentBasedProfile.
次の問題は、ユーザ u の興味プロファイルをどのように表現するか、すなわち、関数 ContentBasedProfile をどのように実装するかである。
A common goal is to use a representation that can be easily matched with the content representation of individual items.
一般的な目的は、個々のアイテムのコンテンツ表現と容易にマッチングできる表現を使用することである。
In the case of text documents, one could for example first encode all items which the user liked in the past with TF-IDF.
例えば、テキスト文書の場合、まずユーザが過去に気に入った項目をすべてTF-IDFで符号化することができる。
Then, the ContentBasedProfile could be defined as being the average of the vectors of the liked items.
次に、ContentBasedProfileを、気に入ったアイテムのベクトルの平均として定義することができる。
Finally, now that the user profile and the items are represented in a compatible way, the function score can for example be implemented through the cosine similarity function.
最後に、ユーザプロファイルとアイテムが互換性のある形で表現されているので、関数スコアは例えば余弦類似度関数で実装することができる。

Various alternative implementations of the different functions are of course possible.
もちろん、さまざまな関数の代替実装が可能である。
The options range from even more simple approaches, e.g., by counting overlapping features such as actors in a movie recommender systems, to more elaborate embeddings, which aim to better capture the semantics of the documents.7 The prediction function can of course be learned in a supervised approach, with input features based on item content information, and any sort of suitable shallow or deep model.
例えば、映画推薦システムにおける俳優のような重複する特徴を数えるという単純なものから、文書のセマンティクスをよりよく捉えることを目的としたより精巧な埋め込みまで、様々な選択肢がある7。予測機能はもちろん、項目内容情報に基づく入力特徴や、任意の種類の適した浅いモデルや深いモデルを用いて教師ありアプローチで学習することが可能である。
Furthermore, a variety of additional pieces of information beyond the document itself were considered in the past decades to better understand the similarity or relations between different items.
さらに、異なる項目間の類似性や関係性をよりよく理解するために、過去数十年間、文書そのもの以外の様々な追加情報が検討されてきた。
Besides item meta-data, various forms of exogenous information about the items, e.g., from Wikipedia, have been incorporated into content-based (or: semantics-aware) recommender systems, see [Musto et al. 2022] for an in-depth discussion.
アイテムのメタデータに加えて、例えば Wikipedia のようなアイテムに関する様々な外来情報がコンテンツベース（あるいはセマンティクスを考慮した）推薦システムに取り入れられてきた、詳細な議論については [Musto et al.2022]を参照。

In terms of application areas, pure content-based systems are often used when there is not sufficient collaborative information available.
アプリケーションの分野では、十分なコラボレーション情報がない場合、純粋なコンテンツベースシステムがよく使われます。
A typical use case is the recommendation of news, where we have to deal with a constant stream of new items, see [Kirshenbaum et al. 2012] for a case study from industry.
典型的なユースケースはニュースの推薦で、絶え間ない新しいアイテムの流れに対処する必要があります。
Content-based systems have however also been applied in practice in other domains such as movies or mobile apps [Bambini et al. 2011, Jannach and Hegelich 2009], where the user preferences can be relatively stable, e.g., in terms of the preferred genres.
しかし、コンテンツベースシステムは、映画やモバイルアプリなど、ユーザーの嗜好が比較的安定している分野でも実際に適用されています [Bambini et al.2011, Jannach and Hegelich 2009]。
A special use case of content-based methods are “similar item” recommendations, where the reference point to making a recommendation is not a user profile, but a specific item.
コンテンツに基づく手法の特殊な使用例として、「類似アイテム」レコメンデーションがあります。ここでは、レコメンデーションを行うための基準点が、ユーザープロファイルではなく、特定のアイテムになります。
Similar item recommendations are common on video streaming platforms, e.g., to recommend movies that are similar to the user just has watched, see [Trattner and Jannach 2019, Yao and Harper 2018].
類似アイテム推奨は、ビデオストリーミングプラットフォームで一般的であり、例えば、ユーザーがちょうど見ていた映画に似ているものを推奨する、[Trattner and Jannach 2019, Yao and Harper 2018]を参照してください。

#### 1.3.6.2. Hybrid Recommender Systems 1.3.6.2. ハイブリッド推薦システム

Pure content-based systems can have certain limitations.
純粋なコンテンツベースのシステムには、ある種の限界があります。
An intrinsic feature of these systems is that they recommend “more of the same” by design, thus limiting the support for discovery of new types of content for users.
これらのシステムの本質的な特徴は、デザイン上「同じものの繰り返し」を推奨するため、ユーザーにとって新しいタイプのコンテンツの発見をサポートすることが制限されることです。
In addition, content-based systems might surface content that is too niche.
さらに、コンテンツベースシステムは、ニッチすぎるコンテンツを推薦する可能性もある。
A movie recommender system that for example only considers the genre or plot descriptions may miss important quality aspects of a movie.
例えば、映画のジャンルやあらすじだけを考慮した映画推薦システムは、映画の重要な品質を見落とす可能性がある。
It may thus return movies which are content-wise related to those that the user liked in the past, but in the end are not recommendations that the user will like.
そのため、ユーザーが過去に気に入った映画と内容的に関連する映画を返すかもしれないが、結局はユーザーが気に入るような推薦文にはならない。

A common solution to deal with such problems is to build hybrid systems, i.e., systems that not only rely on one single paradigm, e.g., collaborative filtering, but combine different approaches.
このような問題に対処するための一般的な解決策は、ハイブリッドシステム、つまり、協調フィルタリングなどの単一のパラダイムに依存するだけでなく、異なるアプローチを組み合わせたシステムを構築することである。
This way, the shortcomings of individual methods should be avoided while the advantages are combined.
この方法では、個々の手法の欠点を避けつつ、利点を組み合わせることができるはずです。
In our example of content-based movie recommendations, one could apply some quality filters before the recommendations are returned, e.g., by removing all movies that have a low average community rating.
例えば、コンテンツに基づく映画推薦の例では、推薦が返される前に、例えば、コミュニティの平均評価が低い映画をすべて削除するなど、いくつかの品質フィルタを適用することができる。

In the literature, a variety of ways of building hybrid recommender systems have been identified.
文献上では、ハイブリッド推薦システムを構築する様々な方法が確認されています。
In [Burke 2002], Burke identified seven such ways, which were later organized in three larger categories in [Jannach et al. 2010] as follows:
Burke 2002] では、Burke はそのような7つの方法を特定し、後に [Jannach et al. 2010] で以下のように3つの大きなカテゴリーに整理されました。

- Monolithic: In such a design, aspects of different recommendation strategies are implemented in one algorithm. A very common realization of such an approach is to design a machine learning model that includes both collaborative signals and content-based features (“side information”). モノリシック：このような設計では、異なる推薦戦略の側面が1つのアルゴリズムに実装される。 このようなアプローチでは、協調信号とコンテンツベースの特徴（「サイド情報」）の両方を含む機械学習モデルを設計することが非常に一般的な実現方法です。

- Parallelized: In parallelized designs, the outcomes of two or more algorithms are first determined independently and then combined in some way. The combination could for example be done on the user interface level, where users are presented a list that contains personalized recommendations as well as recently trending items. Or, some weighted approach can be applied where each item receives a score from each recommender. An extreme case of such a weighting approach would be a switching hybrid, where the recommendations are always taken from one particular algorithm, depending on the situation.8 並列化。 並列化された設計では、2つ以上のアルゴリズムの結果がまず独立して決定され、その後何らかの方法で組み合わされます。 この組み合わせは、例えばユーザーインターフェースレベルで行われ、ユーザーにはパーソナライズされたレコメンデーションと最近トレンドのアイテムを含むリストが提示されます。 また、各アイテムが各レコメンダーからスコアを受け取るような、重み付けアプローチを適用することも可能です。 このような重み付けアプローチの極端な例としては、状況に応じて常に特定のアルゴリズムからレコメンデーションを取得する、スイッチング・ハイブリッドがあります8。

- Pipelined: In this design, one algorithm uses the outputs from another one as an input. In practice, one could for example retrieve a number of recommendation candidates based on popularity, and then only rank these items according to the assumed user preferences in a personalized way.9 パイプライン化。 この設計では、あるアルゴリズムが別のアルゴリズムからの出力を入力として使用します。 実際には、例えば、人気度に基づいて多数の推薦候補を取得し、想定されるユーザーの好みに応じて、これらの項目のみをパーソナライズしてランク付けすることができます9。

#### 1.3.6.3. Collaborative Filtering with Side Information 1.3.6.3. 側面情報を用いた協調フィルタリング

Probably the most common hybrid approach is to enhance the power of collaborative filtering with various forms of side information.
おそらく最も一般的なハイブリッドアプローチは、様々な形式のサイドインフォメーションで協調フィルタリングの力を強化することである。
Such side information is however not limited to item-related information as in content-based filtering approaches.
しかし、このようなサイド情報は、コンテンツベースのフィルタリングアプローチのようにアイテムに関連する情報に限定されない。
Wu et al. [Wu et al. 2022] categorize side information into the following categories of information that a recommender system can use in addition to the observed user-item interaction data.
Wuら[Wu et al. 2022]は、サイド情報を、観測されたユーザーとアイテムの相互作用データに加え、推薦システムが利用できる情報の以下のカテゴリーに分類している。
Figure 1.1 visualizes the different forms of information.
図 1.1 は、さまざまな形式の情報を視覚化したものである。

- User data: These are static or slowly changing features of the user, such as age, gender, or nationality. Historically, systems that leverage such information were called demographic recommender systems. In addition, researchers have also explored the consideration of personality traits in the recommendation process, see [Dhelim et al. 2022]. ユーザーデータ。 年齢、性別、国籍など、静的または緩やかに変化するユーザーの特徴である。 歴史的には、このような情報を活用するシステムは人口統計学的推薦システムと呼ばれていた。 また、推薦プロセスにおいて性格特性を考慮することも研究されており、[Dhelim et al. 2022]を参照。

- Item data: These are aspects that are tied to specific items. Various forms of domain specific item-related features has been considered in the literature, including pre-structured ones like categories, unstructured ones like textual item descriptions, reviews or images, or community-provided semi-structured information in the form of tags. 項目データ。 これらは、特定のアイテムに結びついた側面である。 カテゴリなどの事前構造化されたもの、テキストによるアイテム説明、レビュー、画像などの非構造化されたもの、コミュニティが提供するタグ形式の半構造化情報など、ドメイン固有のアイテム関連機能のさまざまな形式が文献で検討されている。

- Context data: Various forms of comparably frequently changing context information have been explored in the literature, most importantly the geographical location of users, the time of the day, weather conditions or the end user device, see [Adomavicius et al. 2022]. コンテキストデータ。 最も重要なのは、ユーザーの地理的位置、1日の時間、天候、またはエンドユーザーデバイスです。

In terms of the user-item interaction data, research has historically focused on ratings as the only form of interaction.
ユーザーとアイテムのインタラクションデータに関しては、歴史的にインタラクションの唯一の形態であるレーティングに研究が集中してきた。
In more recent years, recommending based on implicit feedback signals has been become predominant, see [Jannach et al. 2018] for a survey.
近年では、暗黙のフィードバック信号に基づくレコメンデーションが主流になってきており、その調査については[Jannach et al.
In most published research works, only one type of implicit feedback is assumed, indicating, e.g., if a user has interacted with an item or not.
発表されたほとんどの研究成果では、1種類の暗黙のフィードバックのみが想定されており、例えば、ユーザーがアイテムとインタラクションしたかどうかを示しています。
In reality, multiple types of interactions are available and could be used.
現実には、複数のタイプのインタラクションが利用可能であり、利用される可能性があります。
In an e-commerce shop, the available signals may included item views, add-to-cart-events, purchases, category navigation events, search actions and even later item returns etc.
eコマースショップでは、利用可能なシグナルは、アイテムビュー、カートへの追加イベント、購入、カテゴリーナビゲーションイベント、検索アクション、さらにその後のアイテムの返却などを含むかもしれない。
Research on leveraging combinations of such types of interaction data is somewhat limited today, probably due to the application specific nature of the interaction events.
このようなタイプのインタラクションデータの組み合わせを活用する研究は、今日ではやや限られています。
Moreover, in real-world interaction logs, information is often stored about the point in time when an interaction happened.
さらに、実世界のインタラクションログには、インタラクションが発生した時点に関する情報が保存されていることが多い。
With that information, time-aware recommender systems [Campos et al. 2014] and sequence-aware based approaches can be implemented, see also Section 2.1.
その情報があれば、時間を考慮した推薦システム[Campos et al. 2014]やシーケンスを考慮したアプローチを実装することができます。

Finally, as mentioned above, various approaches exist in the literature that aim to incorporate exogenous information into the recommendation process.
最後に、前述したように、推薦プロセスに外来情報を組み込むことを目的とした様々なアプローチが文献上存在する。
Examples of such information (including “world knowledge”) are Wikipedia articles, publicly accessible domain ontologies and knowledge graphs, or data that can be accessed or queried through Linked Open Data endpoints, see [Musto et al. 2022] for a discussion.
このような情報（「世界の知識」を含む）の例としては、Wikipedia の記事、公にアクセス可能なドメインオントロジーやナレッジグラフ、あるいは Linked Open Data のエンドポイントを介してアクセスまたはクエリ可能なデータなどが挙げられます（議論は [Musto et al.
Besides such types of information that refer mostly to the items, exogenous information that is tied to individual users has been explored in the literature as well, for instance, the users’ social network, their trust relationships, or reviews written by them, see [Chen et al. 2015, Dong et al. 2022, He and Chu 2010].
このような、主にアイテムに言及するタイプの情報の他に、個々のユーザーに結びついた外生的な情報も文献で研究されており、例えば、ユーザーのソーシャルネットワーク、彼らの信頼関係、または彼らによって書かれたレビューなどがある。

Recent surveys on technical approaches to build “information-rich” collaborative filtering systems can be found in [Wu et al. 2022]. and [Sun et al. 2019c].
情報量豊富な」協調フィルタリングシステムを構築するための技術的アプローチに関する最近の調査は、[Wu et al. 2022]と[Sun et al. 2019c]で見ることができます。
In particular the latter work provides an overview of how various types of deep learning models incorporate side information of different types, including flat features, hierarchical features, knowledge graphs, image features and so forth.
特に後者の著作では、様々なタイプの深層学習モデルが、フラット特徴、階層的特徴、知識グラフ、画像特徴などを含む様々なタイプのサイド情報をどのように取り込むかについて概観している。

### 1.3.7. Discussion 1.3.7. ディスカッション

We have reviewed a selection of important algorithmic approaches to recommendation in this section.
このセクションでは、推薦のための重要なアルゴリズム的アプローチについてレビューしています。
We emphasize that this is only a high-level rundown and the reader can find a myriad of other algorithms and variations in the literature.
しかし、これはあくまでもハイレベルな概説で あり、読者は他のアルゴリズムやそのバリエーションを無 数の文献から探し出すことができることを強調したい。
For instance, Rendle [2010, 2012] developed the factorization machines framework, generalizing several factor models including matrix factorization.
例えば、Rendle [2010, 2012]は因子分解マシンのフレームワークを開発し、行列因子分解を含むいくつかの因子モデルを一般化した。
Like neural approaches, factorization machines can smoothly leverage user and item side information in the framework for an integrated hybrid recommendation approach.
ニューラルアプローチと同様に、因子分解マシンは、統合されたハイブリッド推薦アプローチのためのフレームワークで、ユーザーとアイテム側の情報をスムーズに活用することができます。
Around that time and in the scope of linear models, Ning and Karypis [2011] proposed SLIM, a generalization of item-item collaborative filtering that, in a way, learns the similarity matrix as a regularized optimization problem akin to Equation 1.3 for matrix factorization in Section 1.3.3.2.
その頃、Ning and Karypis [2011]は、線形モデルの範囲内で、ある意味で1.3.3.2節の行列分解に対する式1.3のような正則化最適化問題として類似度行列を学習するアイテムアイテム協調フィルタリングの一般化であるSLIMを提案しました。
This algorithm has become a common baseline in the recommender systems literature for its empirical effectiveness.
このアルゴリズムは、その経験的な有効性から、レコメンダーシステムの文献で一般的なベースラインとなった。
Later on, Steck [2019] derived a closed form solution for computing a very similar model to SLIM.
その後、Steck [2019]は、SLIMと非常によく似たモデルを計算するための閉形式解を導出した。
By removing the need for a costly iterative optimization procedure, the method is considerably more efficient.
コストのかかる反復最適化手順の必要性を排除することで、この方法はかなり効率的になっている。

Other algorithmic developments are targeted at specific recommendation scenarios such as sequential recommendation [Quadrana et al. 2018], discussed later in Section 2.1, and
その他のアルゴリズム開発は、2.1 節で後述する逐次推薦 [Quadrana et al. 2018] など、特定の推薦シナリオをターゲットにしており

Generally, despite the success of in particular of collaborative filtering approaches in practice, recommendation is far from a solved problem: we suggest the reader to retrospect on their own experience as a recommender system user, and form their own opinion.
一般に、特に協調フィルタリングのアプローチは実際に成功しているものの、推薦というのは解決された問題とは言い難い。
Many elements are involved in bringing the recommendation experience anywhere near, for instance, the effectiveness of modern search engines.
例えば、検索エンジンのような効果を発揮するためには、多くの要素が関わってきます。
Strictly speaking, this is not exactly possible—such a comparison is unfair, as search systems receive an explicit expression of intent from the user: the query.
なぜなら、検索システムはユーザーから明示的な意思表示、つまりクエリーを受け取るからです。
Competing against search would anyway misrepresent the purpose of recommendation: recommendation brings value in areas that search cannot solve, or for which search should not be needed.
検索と競合することは、推薦の目的を誤らせることになります。推薦の価値は、検索では解決できない分野、あるいは検索が必要とされない分野で発揮されます。
Be that as it may, room for improvement of current recommendation technology certainly remains, and different angles need to be addressed to achieve it, as we cover in the rest of this paper.
とはいえ、現在の推薦技術に改善の余地があることは確かであり、そのためには、本稿の残りの部分で取り上げるように、さまざまな角度から取り組む必要がある。
The development of better algorithms is certainly one of them, and a major focus of attention and efforts in the field.
より良いアルゴリズムの開発はその一つであり、この分野での注目と努力の大きな焦点であることは間違いない。

## 1.4. Evaluation of Recommender Systems 1.4. レコメンダーシステムの評価

As discussed in the previous section, there is a myriad of choices available when one wants to deploy a recommender system, including a multitude of algorithms, their variants and specific configurations.
前節で述べたように、レコメンダーシステムを導入しようとする場合、多数のアルゴリズムやその亜種、特定の構成など、無数の選択肢が存在する。
Making an informed choice requires suitable and reliable evaluation methodologies.
十分な情報に基づいた選択をするためには、適切で信頼できる評価方法が必要である。
The design and selection of such reliable evaluation methodologies is therefore a central piece in recommendation technology development and research.
このような信頼性の高い評価手法を設計・選択することは、推薦技術の開発・研究において中心的な役割を果たす。
At the same time, these evaluation methodologies drive algorithmic evolution in the field—as a fitness function, they shape the state of the art.
同時に，これらの評価手法はアルゴリズムの進化を促進するものであり，フィットネス関数として，技術の現状を形成しています．

Evaluation generally involves a comparison between two or more recommender systems or variants.
評価には一般的に2つ以上のレコメンダーシステムまたはその亜種を比較することが含まれます。
The most direct approach to compare systems in a production setting is online A
本番環境でシステムを比較するための最も直接的なアプローチは、オンラインA

In the sections that follow we summarize the main lines of approach to recommender system evaluation.
この後の節では、推薦システムの評価に関する主要なアプローチを要約する。
We briefly address online approaches (a perspective that will find further elaboration later in Section 2.3) to then focus on offline evaluation.
まず、オンライン評価について簡単に説明し、次にオフライン評価について述べる。
More specific evaluation methodologies in the context of session-based recommendation are also discussed in Section 2.1.3.
また、セッションベース推薦の文脈におけるより具体的な評価方法については、セクション 2.1.3 で議論する。

### 1.4.1. Online Evaluation 1.4.1. オンライン評価

Recommendation technologies as we experience them on Spotify, Netflix, Amazon, YouTube, Booking, Twitter, Facebook—you name it—have undergone a filtering funnel from the early conception of an algorithmic idea (perhaps in an academic research context) to the final production system [Amatriain and Basilico 2015].
私たちが Spotify，Netflix，Amazon，YouTube，Booking，Twitter，Facebook などで体験しているレコメンデーション技術は，アルゴリズムのアイデアの初期構想から（おそらく学術研究の文脈で）最終的な生産システムに至るまで，フィルタリング・ファネルを経てきました [Amatriain and Basilico 2015]．
This pipeline involves a combination of offline and online experimentation where new ideas are compared to each other, to established baselines, and finally, to the recommendation algorithms currently operating in a live application.
このパイプラインでは、オフライン実験とオンライン実験を組み合わせて、新しいアイデアを互いに比較し、確立されたベースラインと比較し、最終的に、実際のアプリケーションで現在動作している推薦アルゴリズムと比較します。
By and large, offline experimentation precedes online evaluation, given the cost and bandwidth constraints of live testing [Gruson et al. 2019].
ライブテストのコストと帯域幅の制約を考えると、オフライン実験がオンライン評価に先行するのが一般的です[Gruson et al.］
The final test in validating a new idea consists in launching it in the production platform alongside the current version, driving a fraction of user traffic to it, and comparing its performance to that of the present system— whichever wins takes over or remains the working system version.
新しいアイデアを検証するための最終的なテストは、現行バージョンと一緒に本番プラットフォームで起動し、ユーザー・トラフィックの一部を駆動し、現行システムのパフォーマンスと比較することであり、どちらか勝った方が現行システムのバージョンを引き継ぐか残る。

This is called an A
これをA

In addition to testing ideas in the most realistic possible conditions, A
最も現実的な条件でアイデアを検証することに加え、A

A
A

One open challenge to this respect is the weak or missing correlation often observed between the outcome of offline and online comparisons [Garcin et al. 2014, Gomez-Uribe and Hunt 2015, Jannach and Jugovac 2019, Kouki et al. 2020].
この点に関する未解決の課題として、オフラインとオンラインの比較の結果の間にしばしば観察される弱い相関や欠落がある[Garcin et al. 2014, Gomez-Uribe and Hunt 2015, Jannach and Jugovac 2019, Kouki et al. 2020]。
While this remains a major open research question in the field [Gilotte et al. 2018, Jannach and Bauer 2020, Rossetti et al. 2016], offline evaluation is routinely practiced as a selection yardstick before online testing in industry, and is by far the main resource for empirical observation in academic research.
このことは、この分野における主要な未解決の研究課題として残っていますが [Gilotte et al. 2018, Jannach and Bauer 2020, Rossetti et al. 2016] 、オフライン評価は、産業界ではオンラインテストの前の選択基準として日常的に行われており、学術研究においても経験観察のための主要リソースとして圧倒的に利用されています。

Besides A
A以外に

### 1.4.2. Offline Evaluation 1.4.2. オフライン評価

An offline experiment can be seen as a simulation of the system interacting with users, where different proxies—i.e., offline metrics—for system effectiveness are measured [Castells and Moffat 2022].
オフライン実験とは、システムがユーザーと相互作用するシミュレーションとみなすことができ、そこでは、システムの有効性に関するさまざまなプロキシ、つまりオフラインの測定基準が測定される [Castells and Moffat 2022]。
The most informative offline experiment is the one that best simulates and represents the production setting.
最も有益なオフライン実験は、生産設定を最もよくシミュレートし、表現するものである。
In industrial developments, very specific production settings may be required.
産業開発では、非常に特殊な生産設定が要求されることがある。
Therefore, in general research, a number of abstractions are usually made.
そのため、一般的な研究では、多くの抽象化が行われるのが普通である。

The difference between online and offline evaluation can be neatly defined as follows: whereas online evaluation acquires user feedback data (for metric computation) after recommendations are delivered to users—from these same users—in offline evaluation the test data is collected before recommendations are produced—and users are in fact never delivered the evaluated recommendations.
オンライン評価とオフライン評価の違いを簡単に説明すると、オンライン評価では、ユーザーに推薦文を配信した後に、同じユーザーからフィードバックデータを取得するのに対し、オフライン評価では、推薦文を作成する前にテストデータを収集し、実際にはユーザーに評価済みの推薦文を配信することはない、ということである。

Setting up a basic offline experiment for evaluating a recommendation algorithm may seem a straightforward endeavor at first sight, given the wide body of well established methodologies and experimental design principles, in fields such as machine learning and information retrieval, to draw upon.
機械学習や情報検索などの分野では、確立された方法論や実験設計の原則が幅広く存在するため、推薦アルゴリズムを評価するための基本的なオフライン実験の設定は、一見すると簡単なことのように思われるかもしれません。
The recommendation task has however peculiarities of its own that result in a fair degree of hidden complexity and pitfalls, that can produce inconsistent evaluation outcomes more easily than one might think [Canamares et al. 2020].
しかし、推薦タスクにはそれなりの複雑さと落とし穴が隠されており、人が考える以上に簡単に一貫性のない評価結果を生み出してしまうという特殊性がある [Canamares et al.2020]。
˜ The experimenter is advised to carefully consider, understand and report the detailed design choices made in an experiment and their implications.
実験者は、実験におけるデザインの詳細な選択とその意味を注意深く検討し、理解し、報告することが望まれる。
We overview some of them in the following sections.
以下のセクションでそのいくつかを概観する。

### 1.4.3. Offline Data 1.4.3. オフラインデータ

Offline evaluation generally distinguishes training data and test data, which should be strictly disjoint [Guy 2022].
オフライン評価では一般的にトレーニングデータとテストデータを区別し、厳密に分離する必要がある[Guy 2022]。
Training data is supplied as input to the recommender system being evaluated, whereas test data is hidden from the system and is used to compute metrics on the returned recommendations.
トレーニングデータは評価対象のレコメンダーシステムへの入力として供給され、一方テストデータはシステムから隠され、返されたレコメンダーのメトリックを計算するために使用される。
Training data in an offline experiment can be similar to the data that a production system may have available (the more similar the better), whereas test data is used in the experiment to simulate user feedback in reaction to the delivered recommendations.
オフライン実験におけるトレーニングデータは、本番システムが利用可能なデータと類似している（類似しているほど良い）ことがあり、一方、テストデータは、配信された推薦に対するユーザーの反応をシミュレートするために実験に使用される。
The training and test data for recommendation usually reflect user-item interactions as one of their major components—that is, they can be seen as disjoint subsets of the rating matrix.
レコメンデーションのためのトレーニングデータとテストデータは通常、ユーザーとアイテムの相互作用を主要な構成要素の一つとして反映している。
Training data can however also include additional side-information that specific recommendation algorithms may consume.
しかし、学習データには、特定の推薦アルゴリズムが消費する可能性のある付加的な副次的情報を含めることができる。

Training and test data can be acquired in many different ways.
トレーニングデータとテストデータは様々な方法で取得することができます。
A good approach for the training set is to export a subset of the input data that a real recommender system is using at a certain point in time.
学習セットのための良いアプローチは、実際の推薦システムがある時点で使用している入力データのサブセットをエクスポートすることである。
Over the years, a number of such datasets were made publicly available, most prominently the datasets from the non-commercial MovieLens system10.
長年にわたり、そのようなデータセットが数多く公開されてきました。最も顕著なのは、非商業的なMovieLensシステムからのデータセットです10。
Various other datasets are nowadays used by researchers containing items rating, purchase information or listening events, see also [Harper and Konstan 2015]11.
現在では、アイテムの評価、購入情報、視聴イベントなどを含む様々な他のデータセットが研究者によって利用されている（[Harper and Konstan 2015]11も参照）。
Most recently, several datasets were also published that do not contain a matrix of user-item interactions, but sequential logs of recorded interactions, which can be used to evaluate session-based recommendation algorithms, see Section 2.1.
最近では，ユーザとアイテムのインタラクションの行列ではなく，記録されたインタラクションの逐次ログを含むいくつかのデータセットも公開され，セッションベースの推薦アルゴリズムを評価するために使用することができます（セクション2.1参照）．
Unfortunately, for many of the datasets it is not clear under which particular circumstances they were collected.
残念ながら、多くのデータセットでは、どのような特定の状況下で収集されたものであるかが明確ではありません。
For example, when an e-commerce or music streaming platform already has a recommender in place at the point in time of data collection, what we observe in the logs may be to certain extent be biased by the existing recommendation algorithm.
例えば、電子商取引や音楽ストリーミングのプラットフォームが、データ収集の時点ですでにレコメンダーを持っている場合、ログで観察されるものは、ある程度、既存の推薦アルゴリズムによって偏っている可能性があります。
In any case, given such a dataset of logged interactions, a trivial means to obtain test data is to subsample from the training set.
いずれにせよ、このようなインタラクションログのデータセットがある場合、テストデータを得るための簡単な方法は、トレーニングセットからサブサンプリングすることである。
This is usually referred to as splitting the data, and can be carried out in different ways, which we discuss in the next subsection.
これは通常，データの分割と呼ばれ，様々な方法で行うことができるため，次のサブセクションで説明する．

The data typically collected for recommender system experimentation displays heavy sampling biases, originated by the working system (its algorithms, user interface and business rules) through which it was collected, external biases (marketing, fashion, social influence, etc.) and behavioral biases in user engagement.
レコメンダーシステムの実験用に収集されたデータは、収集されたシステム（アルゴリズム、ユーザインタフェース、ビジネスルール）に起因するサンプリングバイアス、外部バイアス（マーケティング、ファッション、社会的影響など）、ユーザエンゲージメントの行動バイアスが大きく現れる。
This raises issues in evaluation that we discuss later in Section 2.2.
このことは、2.2 節で後述する評価上の問題を引き起こす。
Test data can however also be obtained from a separate source from the training set.
しかし、テストデータはトレーニングセットとは別のソースから取得することも可能である。
For instance, the Yahoo! R3 dataset [Marlin and Zemel 2009] includes a test set consisting of randomly sampled ratings from users for music—which means users were required to rate music that was uniformly sampled for them—whereas the training set was collected from free user interaction with music.
例えば，Yahoo! R3 dataset [Marlin and Zemel 2009]では，ユーザからランダムに抽出された音楽に対する評価からなるテストセット（つまり，ユーザは一様に抽出された音楽を評価する必要がある）が含まれており，トレーニングセットはユーザの音楽に対する自由な対話から収集されたものであった．
The Coat dataset [Swaminathan et al. 2017] was built in a similar way in the clothing domain.
Coatデータセット[Swaminathan et al. 2017]は、衣服のドメインで同様の方法で構築されました。
The CM100k dataset [Canamares and Castells 2018] collected user ratings for music entirely at random, and provides a complementary label for user familiarity with the music, which is suggested as a proxy for non-uniformly distributed input training data.
CM100k dataset [Canamares and Castells 2018]は音楽に対するユーザの評価を完全にランダムに収集し、音楽に対するユーザの親しみに関する補完的なラベルを提供し、これは不均一に分布する入力訓練データの代理として示唆されている。

#### 1.4.3.1. Data Splitting 1.4.3.1. データ分割

When the data collected for offline evaluation does not include a separate test subset, the latter is usually subsampled from the available dataset.
オフライン評価のために収集されたデータに個別のテスト用サブセットが含まれていない場合、後者は通常、利用可能なデータセットからサブサンプリングされる。
The sampling—referred to as splitting— procedure can be carried out in different ways.
サンプリング-分割と呼ばれる-手順は、さまざまな方法で実施することができる。
A first parameter of the procedure is the split ratio, i.e. the proportion of train-to-test data, typically expressed as a percentage or a ratio in [0,1].
この手順の最初のパラメータは、分割比率、すなわち訓練データとテストデータの比率であり、通常、パーセンテージまたは [0,1] の比率で表現される。
It is common to allocate a larger data share for training (e.g. ≥ 80%) than test, given the usual data sparsity challenges when training recommendation models.
推薦モデルを学習する際、通常データの疎密の問題を考慮し、テストよりもトレーニングに大きなデータシェア（例えば80%以上）を割り当てることが一般的です。

A second dimension of choice in the sampling procedure is random sampling vs. temporal splitting.
サンプリング手順の選択における第二の側面は、ランダムサンプリングと時間的分割の比較である。
For a chosen point in time, a temporal split places all the data produced prior to that point in the training subset, and the rest in the test subset [Koren 2009].
時間的分割は、ある時点において、その時点以前のすべてのデータをトレーニングサブセットに、残りをテストサブセットに配置します[Koren 2009]。
The time point is sometimes chosen in terms of meaningful time units (a number of weeks, months, etc., worth of data), or in such a way as to obtain a specific split ratio (a proportion between the amount of training and test data).
時点は、意味のある時間単位（数週間、数ヶ月などのデータ）で選ばれることもあれば、特定の分割比率（学習データとテストデータの量の比率）を得るような方法で選ばれることもあります。
More elaborate variants involving segmentation into multiple time windows have also been explored [Lathia 2010].
また，複数の時間窓への分割を含むより複雑な方法も検討されている [Lathia 2010]．
A temporal split generally adds to the soundness of the evaluation methodology, as it better represents a real recommendation task: predicting future (or present) usefulness based on past observed user behavior.
時間軸の分割は、過去のユーザー行動から将来（または現在）の有用性を予測するという、実際の推薦タスクをより適切に表現するため、一般に評価手法の健全性を高めます。
Furthermore, it provides a cleaner data separation, since mixing past and future records can be seen as a form of data leakage.
さらに、過去と未来の記録を混在させることはデータ漏洩の一形態とみなされるため、よりクリーンなデータ分離を実現する。
To this respect, a global time split point can be cleaner than different points for different users (as per e.g., a leave-last-out approach).
この点で、グローバルな時間分割ポイントは、ユーザーごとに異なるポイントよりもクリーンである（例えば、リーブ・ラスト・アウト・アプローチのように）。
Otherwise we might be predicting that a user will like some item in the “future” based on a leakage of foresight information that, for instance, the item would become popular or trendy by then (according to the training records of users with a later split time point), when in fact the item might not have even been created yet during the training period for that user.
そうでないと、例えば、あるアイテムがそのころには人気や流行になっているという先見性のある情報に基づいて、あるユーザーが「未来」にあるアイテムを好きになると予測することになるかもしれません（後の分割点を持つユーザーの学習記録によれば、実際にはそのユーザーの学習期間中にはまだそのアイテムは作成されていないかもしれませんが）。

Temporal splitting can however not always be possible, or not strictly required.
しかし、時間的な分割は常に可能とは限らず、また厳密には必要ない場合もある。
For instance, meaningful data timestamps might not be available, or user needs might be relatively stable, or the experimenter might aim to focus on a specific problem where time is not a priority variable.
例えば、意味のあるデータのタイムスタンプが利用できない場合や、ユーザーのニーズが比較的安定している場合、あるいは実験者が時間を優先しない特定の問題に焦点を当てようとする場合などである。
The common alternative is to sample test and training data randomly, based on the split ratio.
一般的な代替案は、テストデータとトレーニングデータを分割比率に基づいてランダムにサンプリングすることです。
Random sampling is more flexible than a temporal split and enables, for instance, n-fold cross-validation, where n = 5 is a typical number (n = 10, for instance, is also usual).
ランダムサンプリングは時間的分割よりも柔軟性があり、例えば、n = 5が典型的な数であるn-foldクロスバリデーションが可能です（例えば、n = 10も典型的です）。

A natural implementation of a random split is by i.i.d. Bernoulli sampling (coin flip) B(1, p) of data records with p = the split ratio.
乱数分割の自然な実装は、ベルヌーイサンプリング（コインフリップ）B(1, p)によるデータレコードのサンプリングで、p = 分割比率である。
Other implementations have been documented that sample an exact number of data records uniformly at random without replacement, sometimes separately for each user or each item.
他の実装としては、データレコードの正確な数を置換なしで一様にランダムにサンプリングするものがあり、各ユーザーまたは各アイテムごとに別々にサンプリングすることもある。
Other authors have explored sampling an equal amount (rather than an equal ratio) of test data per item or per user, as a way to reduce evaluation biases [Bellog´ın et al. 2017].
他の著者は、評価バイアスを減らす方法として、項目ごとまたはユーザーごとに（等しい比率ではなく）等しい量のテストデータをサンプリングすることを検討している［Bellog´ın et al.2017］。
Research on specific problems can also deploy orthogonal variations of the split procedure to simulate specific conditions such as cold-start or long-tail by placing the items or users of interest in the test set [Hurley and Zhang 2011].
また、特定の問題に関する研究では、関心のあるアイテムやユーザーをテストセットに配置することで、コールドスタートやロングテールなどの特定の条件をシミュレートするために、分割手順の直交するバリエーションを展開することもできる[Hurley and Zhang 2011]。

#### 1.4.3.2. Candidate Item Sampling 1.4.3.2. 候補アイテムのサンプリング

A somewhat hidden option in the design of offline experiments is selecting the set of candidate items (sometimes referred to as target items [Canamares and Castells 2020, Sarwar et al. ˜ 2001]) that the evaluated system should rank for each target user.
オフライン実験の設計におけるやや隠れたオプションは、評価システムが各ターゲット・ユーザーに対してランク付けすべき候補アイテムのセット（ターゲット・アイテムと呼ばれることもある [Canamares and Castells 2020, Sarwar et al.〜2001]）を選択することです。
A natural setting for this option might consider selecting all the items in the catalog.
このオプションのための自然な設定は、カタログ内のすべてのアイテムを選択することを考慮するかもしれません。
This is not the case however when recommendation is viewed as a matrix completion problem: the known matrix cells need not be completed.
しかし、推薦を行列補完問題として捉えた場合、これは当てはまらない：既知の行列セルが補完される必要はない。
In other words, an item is not included in the recommendations to users who have the item in their training records when discovery is part of the aim of recommendation, as is the case of most of the literature.
つまり、多くの文献にあるように、発見が推薦の目的の一部である場合、学習記録にその項目があるユーザへの推薦には、その項目は含まれないことになる。

Experimenters may consider restricting candidate items to an even smaller set.
実験者は、候補となる項目をさらに小さなセットに制限することを検討することができる。
Koren [2008] was the first to suggest a fixed number of target items per user.
Koren [2008]は、ユーザごとに一定の数のターゲット項目を提案した最初の人である。
The idea caught up and is still common nowadays in the research literature [Canamares and Castells 2020, Krichene ˜ and Rendle 2020].
このアイデアは、現在でも研究文献で一般的である [Canamares and Castells 2020, Krichene ˜ and Rendle 2020]。
When small candidate sets are used, some authors refer to this option as computing sampled metrics [Krichene and Rendle 2020].
小さな候補セットを使用する場合、一部の著者はこのオプションをサンプリングされたメトリックの計算と呼んでいます[Krichene and Rendle 2020]。
An extreme, often called condensed rankings [Buckley and Voorhees. 2004], consists in taking only the items with test ratings in the candidate set—this is the option when the error metrics are used (see Section 1.4.4.1 above), as it is not possible to compute a rating error where no rating is available.
極端な例として、condensed rankings [Buckley and Voorhees. 2004]と呼ばれる、候補集合の中からテスト評価を持つ項目のみを取り出す方法がある-これは誤差メトリックを用いる場合の選択肢である（上記セクション1.4.4.1参照）、評価がない場合は評価誤差を計算できないためである。

Recent studies show that candidate sampling can have a deep impact on the outcome of offline evaluation and should be better understood [Canamares and Castells 2020, Krichene ˜ and Rendle 2020, Steck 2013].
最近の研究では，候補のサンプリングがオフライン評価の結果に深い影響を与えることが示されており，よりよく理解されるべきである[Canamares and Castells 2020, Krichene ˜ and Rendle 2020, Steck 2013]．
Authors unanimously report disagreements in system comparisons arising when all vs. no test-unrated items are included in the candidate set.
著者らは一致して，テスト未評価の項目がすべて候補セットに含まれる場合と含まれない場合に生じる，システム比較の不一致を報告している．
Canamares ˜ and Castells [2020] further show that the extremes in this settings have each their own shortcomings, and suggest that some point in between condensed and full rankings might optimize the informativeness of offline evaluation.
Canamares 〜とCastells [2020]はさらに、この設定における両極端がそれぞれ欠点があることを示し、凝縮されたランキングと完全なランキングの間のある点が、オフライン評価の情報量を最適化するかもしれないことを示唆している。

### 1.4.4. Recommendation Task and Metrics 1.4.4. レコメンデーションタスクと評価指標

In practice, every recommender system is designed to fulfil a certain purpose in order to create value for users and organizations, see also Section 2.3.
実際には、すべてのレコメンダーシステムは、ユーザーと組織の価値を創造するために、ある目的を果たすように設計されている（セクション2.3も参照）。
Depending on the purpose, different computational tasks have to be implemented in the system [Jannach and Adomavicius 2016].
その目的に応じて、システムには異なる計算タスクが実装されなければならない[Jannach and Adomavicius 2016]。
In their seminal work on recommender systems evaluation, Herlocker et al. [2004] identified tasks such as “find good items”, “annotation in context” (predict ratings), or “recommend sequence”.
Herlockerら[2004]はレコメンダーシステムの評価に関する彼らの代表的な研究で、「良いアイテムを見つける」、「コンテキストでのアノテーション」（評価の予測）、または「シーケンスを推奨する」といったタスクを特定しました。
When designing new algorithms, the main question is to understand how effective this new algorithm is in terms of fulfilling these tasks.
新しいアルゴリズムを設計する場合、主な問題は、これらのタスクを満たすという点で、この新しいアルゴリズムがどの程度効果的であるかを理解することである。
In offline experiments, this assessment is done with the help of computational metrics, which serve as proxies for the effectiveness of the system in its context of use.
オフライン実験では、この評価は計算メトリクスの助けを借りて行われる。計算メトリクスは、その使用コンテキストにおけるシステムの有効性のプロキシとして機能する。

Traditionally, the most important general aim of recommendation has been understood to involve an accurate grasp of user needs.
従来、推薦の一般的な目的として最も重要なのは、ユーザーのニーズを正確に把握することであると理解されてきた。
Metrics devised to assess this have therefore been broadly referred to as accuracy metrics.
そのため、これを評価するために考案された指標は、広く精度指標と呼ばれてきた。
Recommendation accuracy is nowadays understood as a synonym for ranking quality—metrics and evaluation protocols have therefore been borrowed and adapted from the information retrieval field [Bellog´ın et al. 2017], as we discuss next in Section 1.4.4.2.
レコメンデーション精度は，今日ではランキング品質メトリクスと同義語として理解されており，評価プロトコルは，次にセクション1.4.4.2で述べるように，情報検索分野［Bellog´ın et al.2017］ から借りて適応させたものである。
We nonetheless first discuss earlier perspectives based on rating prediction, for historical interest.
それにもかかわらず、歴史的な興味から、評価予測に基づく以前の展望を最初に議論する。

#### 1.4.4.1. Rating prediction 1.4.4.1. 評価予測

As mentioned in Section 1.2, the recommendation task was initially understood as a rating
1.2節で述べたように、推薦タスクは当初、格付けとして理解されていた

prediction problem—that is, a regression task where a function f : U ×I → R is to be learned
予測問題-すなわち、関数f : U ×I → Rを学習する回帰課題

from examples.
を例示している。
As such, it seemed natural to evaluate recommendation by error metrics
そのため、エラーメトリクスで推薦を評価するのは自然なことだと思われます。

such as Mean Average Error (MAE) and Root Mean Squared Error (RMSE).
平均平均誤差（MAE）、二乗平均誤差（RMSE）など。
The error was
誤差は

measured across the test data in the rating matrix:
レーティングマトリックスのテストデータを横断して測定した。

$$
\text{MAE}
\\
\text{RMSE}
$$

where T ⊂ U × I denotes the subset of test data records, and the lower the value of these metrics, the better the recommender system is considered.
ここで、T⊂U×Iはテストデータのレコードの部分集合を示し、これらの指標の値が低いほど、優れた推薦システムであるとみなされる。

Such metrics were used for almost two decades in the recommender systems literature, and were the basis for such an important initiative in the growth of the field as the Netflix Prize [Liu et al. 2007].
このような指標はレコメンダーシステムの文献で20年近く使われ、Netflix Prize [Liu et al. 2007] のようなこの分野の成長における重要なイニシアティブの基礎となったものです。
The community has moved beyond rating prediction nonetheless, and nowadays tends to see and address recommendation as a ranking task, also in line with business models that are prominent in industry [Cremonesi et al. 2010].
しかし，このコミュニティは格付け予測を超えて，今日では推薦をランキングタスクとして捉え，取り組む傾向にあり，また，産業界で顕著なビジネスモデルとも一致しています [Cremonesi et al.］
Many recommendation algorithms, on the other hand, output scores for user-item pairs that do not have a meaningful interpretation as ratings, but are highly effective to select lists of top-scored items to recommend—error metrics are not meaningful when applied to such scores.
一方、多くの推薦アルゴリズムでは、ユーザとアイテムのペアに対して、評価として意味のないスコアを出力しますが、推薦するトップスコアアイテムのリストを選択するためには非常に有効であり、このようなスコアにエラーメトリクスを適用しても意味がありません。

#### 1.4.4.2. Ranking Quality: Recommendation as an IR Task 1.4.4.2. ランキングの質 IRタスクとしてのレコメンデーション

During the 2000’s the view that delivering recommendations has many commonalities with delivering search results grew stronger in the community [Herlocker et al. 2004].
2000 年代には、推薦を行うことは検索結果を提供することと多くの共通点があるという見解がコミュニティで強まった [Herlocker et al.2004]。
Both recommendation and search systems assist users in accessing relevant information or products from a large collection.
推薦システムも検索システムも、ユーザーが大規模なコレクションから関連する情報や製品にアクセスするのを支援する。
One main difference lies in the absence of an explicit query in the recommendation task—still the problem can be understood to involve a user need to be satisfied, even if it is not explicitly conveyed by the user.
しかし、推薦タスクには明示的なクエリがないため、たとえユーザから明示的な要求がなくても、ユーザが満足すべきニーズがあると理解できる。
In fact, search and recommendation often work together and complement each other in many applications.
実際、多くのアプリケーションにおいて、検索と推薦が連携し、互いに補完しあうことが多い。
This view was recognized time before [Belkin and Croft 1992] but did not seem to catch up community-wide as—to some degree—a paradigm change in evaluation until the 2010’s [Bellog´ın et al. 2017, Cremonesi et al. 2010].
このような考え方は以前から認識されていましたが [Belkin and Croft 1992] 、2010年代になるまで、評価のパラダイムチェンジとしてコミュニティ全体にある程度浸透しなかったようです [Bellog´ın et al.2017, Cremonesi et al.2010] 。

In this realization, the key for recommendation effectiveness is in the returned ranking: effective recommendations should return as many relevant items as early as possible in the ranking, and as few non-relevant items as possible in the top positions.
つまり、できるだけ早い段階で関連性の高いアイテムを返し、上位にはできるだけ関連性の低いアイテムを返さないことが、効果的なレコメンデーションを実現するための鍵である。
The ranking determines what items the user will see, and how soon, when browsing recommendations.
ランキングは、ユーザーがレコメンドを閲覧する際に、どのアイテムをどの程度早く目にすることができるかを決定する。
The interpretation of the system scores, by which items are ranked, as accurate rating predictions becomes irrelevant.
順位付けされた項目のシステムスコアを、正確な評価予測として解釈することは無意味である。
The notion of ranking can be naturally generalized to other, not necessarily linear displays of recommendations (e.g. a “shelve” matrix), where some regions in the screen layout—equivalent to the top rank notion—are more likely than others to be examined by users.
ランキングの概念は、必ずしも線形ではない他のレコメンデーション表示（例えば、「棚上げ」マトリックス）にも自然に一般化することができ、画面レイアウトのある領域（トップランクの概念に相当）は、ユーザーによって検討される可能性が他の領域よりも高くなる。

Ranking evaluation naturally motivated researchers to borrow concepts and methodologies from the information retrieval field, where offline evaluation procedures and metrics had been researched and developed for half a century.
ランキングの評価は、半世紀にわたってオフラインの評価手順や評価基準が研究・開発されてきた情報検索の分野から、コンセプトや方法論を借りてくるのが自然な流れであった。
The adaptation is however not straightforward and involves subtleties that need to be handled with care.
しかし、この適応は一筋縄ではいかず、注意深く扱わなければならない微妙な問題を含んでいる。
We discuss this adaptation through the main elements involved in offline evaluation practice in the information retrieval field [Sanderson 2010].
ここでは、情報検索分野におけるオフライン評価の主な要素を通して、この適応を議論する [Sanderson 2010]。

- Collection. The set of items I can be considered an equivalent of the set of all “documents” in the IR literature. Item collections—often referred to as “item catalogs”—are in fact often the retrieval space for complementary search and recommendation functionalities in most recommender system applications. コレクションである。 アイテムIの集合は、IRの文献にあるすべての「文書」の集合と等価であると考えることができる。 アイテムコレクションは、しばしば「アイテムカタログ」と呼ばれ、実際、ほとんどのレコメンダーシステムアプリケーションにおいて、検索と推薦の機能を補完する検索空間であることが多い。

- Query and Information Need. Search and recommendation are both motivated by a need on the user side that the system aims to help satisfy. Whereas users actively describe their need with explicit queries to a search engine, recommender systems derive user needs from observed user activity and interactions with the items. The information need representation in a recommender system is therefore considerably vague and incomplete compared to a search engine, and calls for different retrieval techniques. Search queries can have different degrees of vagueness too, and recommendation can be seen as the endpoint in a continuous spectrum of query specificity for a retrieval task, where the query is just empty. クエリーと情報の必要性。 検索と推薦の両方は、システムが満たすことを支援することを目的としたユーザー側のニーズによって動機づけられている。 検索エンジンでは、ユーザーは積極的に自分のニーズを明示的なクエリで表現するが、レコメンダーシステムでは、観察されたユーザーの活動やアイテムとのインタラクションからユーザーのニーズを導き出す。 したがって、レコメンダーシステムにおける情報ニーズの表現は、検索エンジンに比べてかなり曖昧で不完全であり、異なる検索技術を必要とする。 検索クエリも様々な曖昧さを持ち、推薦文は検索タスクのクエリ特異性の連続スペクトルの終点と見なすことができる（クエリは単に空である）。

- Relevance. The notion of relevance, central to IR, is just as meaningful in recommendation, and can be taken in quite the same sense: a recommended item is relevant to a user if they like, enjoy, are pleased by, are interested in, etc., the item. Relevance can be considered as a necessary condition for a recommendation to bring any value to the user. If a recommended item is not relevant the user will ignore it and no gain will be derived. 関連性（Relevance）。 IRの中心的な概念である関連性は、推薦においても同様に重要であり、全く同じ意味でとらえることができる。推薦されたアイテムは、ユーザーがそのアイテムを好き、楽しい、嬉しい、興味がある、などの場合に関連性があるといえる。 つまり、「好き」「楽しい」「嬉しい」「興味がある」など、ユーザーにとって関連性のあるものを推薦することが、推薦がユーザーに価値をもたらすための必要条件と考えることができる。 もし、関連性がなければ、ユーザーはその推薦を無視することになり、何の利益も得られない。

A major difference should be noted though as to how relevance is handled in offline experiments: while relevance is often assumed to be objectifiable—i.e. user-independent—in face of a query as a reasonable simplification, this assumption is not reasonable in recommendation, where relevance is acknowledged to be highly user-dependent, and this is typically an intrinsic characteristic of the recommendation task.
しかし、オフライン実験において関連性がどのように扱われるかについては、大きな違いに注意する必要があります。関連性はしばしば合理的な単純化として、問い合わせに対して客観的、すなわちユーザ非依存的であると仮定されますが、関連性がユーザ依存性が高いと認められている推薦ではこの仮定は合理的ではないし、これは典型的に推薦タスクの本質的特性であるといえます。
This has important consequences in offline evaluation when it comes to eliciting relevance judgments: delegating item labeling as relevant or non-relevant to assessors on behalf of users is too far a stretch to enable any kind of meaningful evaluation of personalized recommendations.
このことは、オフライン評価において、関連性の判断を引き出す際に重要な結果をもたらします。ユーザーに代わって評価者にアイテムの関連性または非関連性のラベル付けを委任することは、個人化された推薦のいかなる種類の意味のある評価も可能にするには、あまりにも行き過ぎたことなのです。
Offline evaluation is therefore not separable from actual end users in the way search evaluation can be.
オフライン評価は、検索評価のように実際のエンドユーザーから切り離すことができません。

In offline recommendation experiments, test data obtained from target users play the role of relevance judgments in IR evaluation.
オフライン推薦実験では、対象ユーザから取得したテストデータがIR評価における関連性判定の役割を果たす。
Compared to judgment pooling in IR [Sanderson 2010], test data can introduce extremely sharp selection biases in evaluation when data are collected in the wild, and
IRにおける判定プーリング[Sanderson 2010]と比較すると、テストデータが野放しで収集された場合、評価において極めて鋭い選択バイアスが発生する可能性があり

Metrics.
指標
Once an equivalent of relevance judgments is defined and obtained, any IR metric can be applied to the output of a recommender system: precision, recall, mean average precision (MAP), mean reciprocal rank (MRR), normalized discounted cumulative gain (nDCG), are commonly used to assess the ranking quality of recommendations.
一旦関連性判断の等価物が定義され、得られると、どんなIRメトリックでも推薦システムの出力に適用できる：精度、リコール、平均平均精度（MAP）、平均相互ランク（MRR）、正規化割引累積利益（nDCG）は推薦のランキング品質を評価するために一般的に使用されている。
Since precision and recall are rank-insensitive metrics, they are usually measured on a subset of top-n recommended items—a ranking cutoff—as P@n and Recall@n.
精度とリコールは順位に影響されない指標なので、通常、上位n個の推薦項目のサブセット、つまり、P@nとRecall@nとしてランキングのカットオフで測定される。
Cutoffs can also be taken in rank-sensitive metrics such as nDCG, MAP and MRR, to further focus measurements on the ranking top.
また、nDCG、MAP、MRRのようなランクに敏感なメトリクスでもカットオフを取ることができ、ランキング上位にさらに焦点を当てた測定が可能である。

The Area Under the ROC Curve (AUC) [Bamber 1975] can also be considered a ranking metric inasmuch as it provides a perspective of the relevant vs. non-relevant recommended items tradeoff across the ranking.
AUC (Area Under the ROC Curve) [Bamber 1975] は、ランキング全体における推奨項目の関連性対非関連性のトレードオフの視点を提供する限り、ランキングメトリックとみなすこともできる。
AUC is commonly used as a metric for classifier evaluation, but then so are precision and recall: they view recommender systems as binary classifiers into the relevant and non-relevant classes.
AUC は一般的に分類器の評価指標として使われますが、精度や再現率も同様で、推薦システムを関連するクラスと関連しないクラスへの二値分類器として見なします。
Focusing the measurements on top n rank positions does the trick for such measures, turning them into informative ranking metrics.
このような指標は、上位 n ランクの位置に焦点を当てることで、有益なランキング指標に変わります。

Compared to search experiments, bias and user-dependence in relevance judgments for recommendation exacerbate the sparsity of relevance labels in the ranking tops to be evaluated in offline recommendation experiments.
検索実験と比較して、推薦のための関連性判断における偏りやユーザ依存性は、オフライン推薦実験において評価すべきランキング上位の関連性ラベルの疎密を悪化させる。
Deciding how to handle the missing judgments becomes a key issue when importing IR ranking metrics, as discussed earlier in Section 1.4.3.2.
このような欠測をどのように処理するかは、1.4.3.2節で述べたように、IRランキングメトリクスをインポートする際に重要な課題となる。
An additional challenge is the non-random nature of the missing data, and the resulting bias in evaluation results.
さらに、欠損データの非ランダム性、および、その結果生じる評価結果のバイアスも課題となる。
We discuss this further in Section 2.2.
これについては、セクション2.2で詳しく説明します。

### 1.4.5. Beyond Accuracy 1.4.5. 精度を超えて

While accuracy was the primary perspective on algorithmic evaluation for a long time, it eventually became apparent that this is an incomplete view of what makes a recommendation useful and profitable for consumers and providers [Ge et al. 2010, McNee et al. 2006].
しかし、これは消費者やプロバイダにとっ て、何がレコメンデーションを有用で有益なものにする のかについての不完全な見方であることが、やがて明ら かになってきました [Ge et al.2010、McNee et al.］
For example, a fan of the Beatles would very likely love the song ‘Yesterday’—the song is highly relevant in the IR sense—but how useful would this be as a recommendation?
例えば、ビートルズのファンなら「Yesterday」という曲が大好きでしょう。この曲はIR的に非常に関連性が高いのですが、これが推薦としてどの程度役に立つのでしょうか。
The song is a most widely known music piece worldwide, more so for a Beatles fan.
この曲は、世界中で最も広く知られている音楽作品であり、ビートルズファンにとってはなおさらである。
The user might as well search for it when they fancy.
ビートルズファンならなおさらだ。
The song might make sense as a convenience recommendation in some scenarios, e.g., in an automatic playlist while driving on a trip, but the added-value of such a recommendation (e.g., with respect to searching and browsing) is clearly more restricted than might be, for instance, the discovery of new music or a new band or a new taste the user was not aware of and can now enjoy.
しかし、このような推薦の付加価値（例えば、検索やブラウジング）は、例えば、ユーザーが知らなかった新しい音楽、新しいバンド、新しい味を発見し、それを楽しむことに比べると、明らかに制限されたものであろう。

Likewise, when a streaming platform lists movies and series the user might enjoy, it may be wise to include movies from a variety of genres and directors, to better represent the diversity of interests people have—and the varying mood.
同様に、ストリーミングプラットフォームが、ユーザーが楽しめそうな映画やシリーズをリストアップするとき、人々が持つ興味の多様性や様々な気分をよりよく表現するために、様々なジャンルや監督の映画を含めることが賢明かもしれません。
While people’s tastes can be stable, we may feel like watching comedy one day and a documentary the next day, and those changes are very difficult to guess.
人の好みは安定していますが、ある日はコメディを見たくなり、次の日はドキュメンタリーを見たくなることもあり、その変化を推測することは非常に困難です。
Rather than risking a double-or-nothing bet on all-comedy or alldocumentary recommendation, a diversified offering of potential favorites would seem a more sensible approach considering this.
コメディばかり、ドキュメンタリーばかりと二者択一で推薦するよりも、好みの作品を分散して推薦する方が、より理にかなった方法だと思います。
Moreover, by diversifying recommendations the system takes opportunities to explore unseen user interests and learn about them to keep improving in the future.
また、レコメンドを多様化することで、システムはユーザーの未知の興味を探り、それを学習する機会を得て、将来的に改良を続けていくことができるのです。

Novelty and diversity are just two dimensions in the objectives beyond accuracy that can maximize the value of recommendation, and we focus on them here.
新規性と多様性は、推薦の価値を最大化することができる精度を超えた目標の中の2つの次元に過ぎず、ここではそれらに焦点を当てることにする。
It is useful to distinguish between novelty and diversity as highly related but different perspectives, a distinction we reflect in the summary that follows.
新規性と多様性は、関連性が高いが異なる視点であると区別することが有効であり、この区別を以下の要約に反映させた。
Broader perspectives on the direct key measures of the value, user satisfaction, business performance and the impact at large that recommendation has on the involved stakeholders, are discussed in Section 2.3.
また、推薦が関係者に与える直接的な価値、ユーザー満足度、ビジネスパフォーマンス、インパクトに関する広範な視点については、2.3節で議論する。
A recommender system finds several motivations to enhance novelty and diversity, and different angles to these general notions, that can be operationalized into metrics and algorithms that enhance and measure them, as we discuss next.
レコメンダーシステムは、次に述べるように、新規性と多様性を強化するいくつかの動機と、これらの一般的な概念に対する異なる角度を見出し、それらを強化し測定するメトリックとアルゴリズムに運用することができる。
For a more extensive review of novelty and diversity in recommender systems, the reader is referred to [Castells et al. 2022].
レコメンダーシステムにおける新規性と多様性に関するより広範なレビューについては、読者は[Castells et al.］

#### 1.4.5.1. Novelty 1.4.5.1. ノベルティ

At an abstract level, recommendation novelty can defined as the difference between the recommended items and a certain context of reference [Vargas and Castells 2011].
このように，レコメンデーションの新規性は，レコメンデ ーション対象者とある参照コンテキストとの差異として定義され る [Vargas and Castells 2011]。
The context can typically be the past experience of the person to whom a recommendation is delivered or, considering the sparse and partial system knowledge about that, the aggregated experience of all users in the system.
このコンテキストは，推薦を受けた人の過去の経験，あるいは，システム内の全ユーザーの経験を集約したもので，それに関する知識がまばらで部分的であることを考慮すれば，典型的なものです．
In the latter case, novelty equates to rarity: a recommended item is novel if it is in the long-tail of the interaction frequency distribution [Celma and Herrera 2008].
後者の場合、新規性は希少性と等しく、推薦されたアイテムが相互作用頻度分布のロングテールであれば新規性があるといえます [Celma and Herrera 2008]。
Personalized novelty, often referred to as unexpectedness [Adamopoulos and Tuzhilin 2014], would reflect how different a recommendation is from the items the target user was observed interacting with in the past.
パーソナライズされた新規性は、しばしば意外性[Adamopoulos and Tuzhilin 2014]と呼ばれ、ターゲットユーザが過去に対話したことが観察されたアイテムとは異なる推薦を反映することになります。
Long-tail novelty and unexpectedness can be quantified in different ways, which we summarize next.
ロングテールの新規性と意外性は様々な方法で定量化することが可能であり、次にその概要を説明します。

##### 1.4.5.1.1.

##### 1.4.5.1.1.

Long-tail novelty.
ロングテールの新しさ

This dimension can be measured, for instance, as the average of a monotonically decreasing function φ on the amount of past engagement Li with each recommended
この次元は、例えば、各推薦された人との過去のエンゲージメント量Liに関する単調減少関数φの平均値として測定することができます

$$
LT(R) =
$$

where R is the returned recommendation and Li denotes the set of observed interactions involving item i. The φ function has been defined in the literature, for instance, as the complement or the negative log of the ratio of observed interactions involving the item [Vargas and Castells 2011]:
ここで、R は返されたレコメンデーション、Li は項目 i を含む観測された相互作用のセットを示す。φ関数は、例えば、項目を含む観測された相互作用の比率の補数または負対数として文献で定義されている [Vargas and Castells 2011]。

$$
(x) = 1 -\frac{x}{|L|}
$$

where L represents the set of all observed interactions.
ここで，L は観測されたすべてのインタラクションの集合を表す．
With the first definition, novelty can be read as the probability that a random user has never interacted in the past with a recommended item in R. When repeated interaction is ignored (i.e., each user-item pair is counted at most once in the above equations), the second definition is equivalent to inverse document frequency as defined in IR models for document retrieval, users being here the equivalent of documents—hence sometimes referred to asinverse user frequency [Breese et al. 1998].
最初の定義では、新規性はランダムなユーザが過去にRの推奨項目と相互作用したことがない確率と読むことができる。繰り返しの相互作用を無視する場合（すなわち、各ユーザと項目のペアは上記の式で最大一度だけ数えられる）、第2の定義は、文書検索のIRモデルで定義される逆文書頻度と同等で、ユーザはここでは文書と同等であるため逆ユーザ頻度と呼ぶことができる [Breese et al.1998]。
When measured this way, novelty can be seen as a condition of coldness (lack of data) or unpopularity.
このように測定すると、新規性は冷淡さ（データの欠如）あるいは不人気さの条件とみなすことができる。

##### 1.4.5.1.2.

##### 1.4.5.1.2.

Unexpectedness.
予期せぬ事態

This notion is typically quantified as:
この概念は、通常、次のように定量化されます。

$$
Unex(R)
$$

where d denotes a set dissimilarity operator and $E_u \in I$ is a reference set of items representing “the expected” for each user u ∈U.
ここで、dは集合非類似度演算子を表し、$E_u \in I$は各ユーザーu∈Uの「期待される」を表すアイテムの参照集合である。
The expected set can be, for instance, the items that the target user has interacted with, or the recommendations delivered by a supposedly conventional algorithm, or any other proxy for an unsurprising experience [Adamopoulos and Tuzhilin 2014].
期待される集合は、例えば、ターゲット・ユーザーが相互作用したアイテムや、従来型のアルゴリズムによって配信された推奨品、あるいは、意外性のない経験の他の代理となり得る[Adamopoulos and Tuzhilin 2014]。
Set dissimilarity can be any conventional measure such as Jaccard, Hausdorff, average item-wise distance, or other meaningful elaborations to quantify how different the two sets are.
セットの非類似度は、Jaccard、Hausdorff、平均アイテムワイズ距離、または2つのセットがどれだけ異なるかを定量化する他の意味のある精緻化など、任意の従来の測定値を使用することができます。
When pairwise item distance is used, feature-based dissimilarity (measured e.g., by the cosine or Jaccard distance between feature vectors
ペアワイズ項目距離が使用される場合、特徴ベースの非類似度（例えば、特徴ベクトル間のコサインまたはジャカール距離によって測定される。

##### 1.4.5.1.3.

##### 1.4.5.1.3.

Serendipity.
セレンディピティ

An additional important notion in the scope of novelty is serendipity.
新規性の範囲における追加の重要な概念は、セレンディピティ（serendipity）です。
While the definitions slightly vary in the literature, the dominant convention considers a recommendation as serendipitous if it is surprising (i.e. novel) and valuable [Chen et al. 2019].
文献によって定義は若干異なりますが、支配的な慣習では、推薦が意外で（つまり新規性があり）価値がある場合にセレンディピティと見なします[Chen et al.2019]。
If we equate value, in this sense, to relevance, a straightforward way to measure serendipity is to restrict the computation of the above novelty metrics to the recommended items that are relevant to the target user (according to the available test data), and ignore the rest.
この意味で価値を関連性と同一視すると、セレンディピティを測定する簡単な方法は、上記の新規性メトリックの計算を、ターゲットユーザーに関連する（利用可能なテストデータによる）推奨アイテムに限定し、残りを無視することです。

##### 1.4.5.1.4.

##### 1.4.5.1.4.

Further notions.
さらなる概念

The above novelty notions are probably the most common in the literature but they are not meant to be exhaustive [Castells et al. 2022].
上記の新規性の概念は、おそらく文献上最も一般的なものですが、網羅的なものではありません [Castells et al. 2022]。
Freshness (how recently a recommended item was created), for instance, is often an important property by itself, and typically a signal that correlates with the above notions.
例えば、新鮮さ（推奨アイテムがどれだけ最近作成されたか）は、しばしばそれ自体で重要な特性であり、典型的には上記の概念と相関する信号である。
Lathia and Amatriain [Lathia et al. 2010] explored finer temporal notions of novelty and diversity, involving the history of past recommendations—capturing, broadly speaking, how much a recommender system is repeating itself.
Lathia と Amatriain [Lathia et al. 2010] は、過去の推薦履歴を含む新規性と多様性に関するより細かい時間的概念を探求し、広義には、推薦システムがどれだけ繰り返しているかを捕捉しています。

#### 1.4.5.2. Diversity 1.4.5.2. 多様性

Related to but different from novelty notions, diversity is generally defined as the amount of variety covered within recommendations.
新規性とは異なりますが、多様性とは、一般的にレコメンデーションに含まれる多様性の量と定義されます。
For instance, ‘Orinoco Flow’ by Enya and ‘Highway to Hell’ by AC
例えば、Enyaの「Orinoco Flow」とACの「Highway to Hell」。

#### 1.4.5.3. Enhancing Novelty and Diversity 1.4.5.3. 新規性・多様性の向上

Enhancing novelty and diversity can be addressed as the maximization of the measure of interest, taking metrics such as the ones discussed above as the target for maximization.
新規性や多様性を高めることは、上述したような指標を最大化の対象として、関心のある指標の最大化として取り組むことができる。
This finds two main problems.
これには、主に2つの問題がある。
The first and perhaps most important is that maximizing for novelty or diversity is not aligned with maximizing relevance, in the IR sense.
まず、おそらく最も重要なのは、新規性や多様性を最大化することは、IR的な意味での関連性を最大化することと一致しないことである。
In fact, both objectives sometimes display a tradeoff—for example, random recommendations typically score extremely high on novelty and diversity, and extremely low on relevance.
例えば、ランダム・レコメンデーションは新規性と多様性が極めて高く、関連性が極めて低い。
Rather than a single optimum the problem displays a Pareto front.
この問題は、単一の最適値ではなく、パレート面を示す。
As a multi-objective problem, diversity and novelty enhancement can be addressed by common strategies: scalarization, evolutionary algorithms, etc.
このような多目的の問題として、多様性と新規性の向上は、スカラリゼーション、進化的アルゴリズムなどの一般的な戦略によって対処することができる。
[Veloso et al. 2014].
[Veloso et al.2014〕。］
Since state of the art recommendation algorithms do not necessarily lie on the Pareto front, some works report improvements in both directions [Jannach et al. 2015a, Vargas and Castells 2014].
最新の推薦アルゴリズムが必ずしもパレートフロント上にあるとは限らないため，いくつかの著作では両方向の改善が報告されている[Jannach et al.2015a, Vargas and Castells 2014]．

In doing so, a top-level distinction can be made between diversification strategies: intrinsic or extrinsic.
その際、多様化戦略を内在的か外在的かで区別することができる。
Extrinsic approaches re-rank an initial relevance-oriented recommendation, seeking to improve the relevance-diversity (and
外発的アプローチは，最初の関連性重視の推薦を再ランク付けし，関連性多様性（および，関連性多様性を向上させようとするものである．

A second difficulty arises when the diversity metric is not defined separately for each user and aggregated or averaged afterwards, but is defined on the set of all recommendations— as is the case of coverage, explained earlier.
第二の問題は、多様性指標が各ユーザーに対して個別に定義され、その後集約または平均化されるのではなく、先に説明したカバレッジの場合のように、すべてのレコメンデーションの集合に対して定義される場合に生じます。
In those cases the relevance-diversity tradeoff cannot be optimized on each user independently, and the problem space becomes even larger: recommendations become interdependent in their contribution to the global diversity, and should ideally be optimized at the same time.
このような場合、関連性と多様性のトレードオフは各ユーザーに対して独立して最適化することができず、問題空間はさらに大きくなります。推奨はグローバルな多様性への貢献において相互依存関係にあり、理想的には同時に最適化されるべきです。
Different levels of greediness in the approach are still possible, though an additional tradeoff needs then to be withstood between cost and optimality [Sanz-Cruzado and Castells 2018].
アプローチにおける異なるレベルの貪欲さはまだ可能ですが、その場合、コストと最適性の間で追加のトレードオフに耐える必要があります[Sanz-Cruzado and Castells 2018]。

In most recent years, diversification approaches that operate on the user-individual level have become more popular.
近年では，ユーザ個人レベルで動作する多様化アプローチ が人気を集めている．
In an earlier work, Oh et al. [2011] proposed to adapt the novelty of the recommendations according the past popularity tendencies of individual users.
以前の研究では、Ohら[2011]は、個々のユーザーの過去の人気傾向に従って推薦の新規性を適応させることを提案しました。
A similar and more generic re-ranking approach was later proposed in [Jugovac et al. 2017], which also supports the consideration of multiple optimization objectives per user in parallel.
その後、[Jugovac et al. 2017]では、より汎用的な同様の再ランキング手法が提案され、ユーザーごとに複数の最適化目的を並行して考慮することもサポートされています。
Today, such approaches are known as calibrated recommendation [Steck 2018].
今日、このようなアプローチはキャリブレーテッド・レコメンデーション[Steck 2018]として知られている。
An important aspect of calibrated recommendations that is currently not covered in depth so far is that a user’s diversity of novelty preferences may change over time and depending on the context, see [Kapoor et al. 2015] for an analysis of such phenomena in the music domain.
現在のところこれまで深く取り上げられていない較正された推薦の重要な側面は、ユーザーの新規性嗜好の多様性が時間の経過や文脈によって変化する可能性があることであり、音楽領域におけるそのような現象の分析については[Kapoor et al.2015]を参照してください。

#### 1.4.5.4. User Perceptions of Diversity and Novelty 1.4.5.4. 多様性と新しさに関するユーザーの認識

Over the last decade, a multitude of algorithmic approaches were proposed to create more novel and diverse recommendations by optimizing the list of suggestions according to corresponding computational metrics.
過去10年以上、アルゴリズムによる多くのアプローチが提案され、対応する計算上のメトリックに従って推薦リストを最適化することにより、より新規で多様な推薦を作成することができる。
As with any computational metric, it is however important to ensure that these metrics are actually valid proxies of the users’ perceptions, e.g., of the novelty and diversity of the recommendations.
しかし、どのような計算上のメトリックでもそうであるように、これらのメトリックが実際にユーザーの認識、例えば、レコメンデーションの新規性や多様性の有効なプロキシであることを確認することが重要である。
Moreover, it is crucial to understand how these perceptions then impact the users’ satisfaction with the system.
さらに、これらの認識がユーザーのシステムに対する満足度にどのような影響を与えるかを理解することが重要である。

Intra-list dissimilarity, as mentioned above, is widely used in the literature to express the diversity of a recommendation list.
リスト内非類似度は，前述のとおり，推薦リストの多様性を表現するために，文献上広く用いられている．
In [Ziegler et al. 2005], the impact of topic diversification on user satisfaction was explored with the help of a user study13.
Ziegler et al. 2005]では、トピックの多様化がユーザーの満足度に与える影響について、ユーザー調査13の助けを借りて調査しています。
Different levels of diversifications were tried and the obtained peak value in satisfaction indicated that the participants preferred a certain degree of diversification in their book recommendations.
さまざまなレベルの多様化が試され、得られた満足度のピーク値は、参加者が書籍の推薦においてある程度の多様化を好むことを示しました。
Similar observations were made in [Castagnos et al. 2013] in the context of movie recommendations.
同様の観察は，映画推薦の文脈で[Castagnos et al.2013]で行われた．
In their study, the authors also presented study participants with recommendation lists that had different degrees of diversity.
彼らの研究では、著者らは、多様性の程度が異なる推薦リストを研究参加者に提示しました。
The authors found that (i) participants notice the different diversity levels and (ii) that diversity may positively influence user satisfaction.
著者らは、(i)参加者が多様性のレベルの違いに気づくこと、(ii)多様性がユーザー満足度にポジティブな影響を与える可能性があることを発見しています。
However, in case of diversified lists it was observed that providing additional explanations may be advisable so that users can better link the recommendations with their preferences.
しかし、多様性のあるレコメンデーションリストの場合、ユーザーがレコメンデーションと自分の好みをよりよく結びつけることができるように、追加の説明を提供することが望ましい場合があることが観察された。
Positive effects of diversity on user satisfaction in the movie domain was also reported in [Ekstrand et al. 2014]; however, in this study it also turned out that increased levels of novelty—e.g., when too many unfamiliar items are recommended—may negatively impact user satisfaction.
映画領域における多様性のユーザー満足度への正の効果は[Ekstrand et al. 2014]でも報告されていますが，この研究では，新規性のレベルが高くなると，例えば，知らないアイテムが多く推薦されると，ユーザー満足度に負の影響を与える可能性があることも判明しています．

In the mentioned studies in the book and movie domains, the used similarity functions were based on topic categories and movie attributes and proved effective in the experiments.
書籍や映画に関する研究では，トピックのカテゴリや映画の属性に基づく類似性関数が用いられ，実験において有効であることが示された．
Such a validation of the particular similarity function is however often missing in other works.
しかし、このような特定の類似性関数の検証は、他の研究においてはしばしば欠落している。
More work is therefore required to understand which features of an item are determining the similarity perceptions of users, see [Trattner and Jannach 2019, Yao and Harper 2018] for studies in the movies and food domain.
したがって、アイテムのどの特徴がユーザーの類似性認識を決定しているかを理解するためにさらなる研究が必要であり、映画や食品ドメインでの研究については[Trattner and Jannach 2019, Yao and Harper 2018]を参照されたい。
Moreover, in the traditional intra-list dissimilarity measure, the position of the diverse elements does not matter when assessing the overall diversity of a given list.
さらに、従来のリスト内非類似度測定では、与えられたリストの全体的な多様性を評価する際に、多様な要素の位置は重要ではありません。
In reality, indications exist that the ordering of the items may impact user perceptions [Ge et al. 2012].
現実には、項目の順序がユーザの知覚に影響を与える可能性があるという指摘が存在する[Ge et al.2012]。
In this direction, drawing from earlier work on IR metrics built upon user models (e.g., [Moffat and Zobel 2008]), Vargas and Castells [2011] propose a probabilistic metric framework where a wide variety of novelty and diversity metrics— including the ones mentioned in this section—can be endowed with rank sensitivity.
この方向で、ユーザーモデルに基づいて構築されたIRメトリックに関する以前の仕事（例えば、[Moffat and Zobel 2008]）から、Vargas and Castells [2011]は、このセクションで述べたものを含む様々な新規性と多様性のメトリックに順位感度を与えることができる確率的メトリックの枠組みを提案します。

Instead of varying the positions of the items in one recommendation list, as done in [Ge et al. 2012], Hu and Pu [2011] suggested to organize the items in groups.
Hu and Pu [2011]は、[Ge et al. 2012]のように一つの推薦リスト内の項目の位置を変える代わりに、項目をグループに分けて整理することを提案しました。
In a user study, in which also the participants’ eye movements were tracked, they then found that the “organization” interface helped to increase the diversity perception of users.
そして、被験者の目の動きを追跡したユーザー調査により、「整理」インタフェースがユーザーの多様性知覚の向上に役立つことを発見しました。
Finally, in a more recent work, Chen et al. [2019] report the outcome of a large-scale user study on the quality perception of recommendations on an e-commerce platform.
最後に、より最近の研究として、Chenら[2019]は、eコマースプラットフォームにおけるレコメンデーションの品質認識に関する大規模ユーザー調査の結果を報告している。
The study revealed that serendipity plays a decisive role for user satisfaction and is more important than diversity and novelty alone.
この研究により、セレンディピティがユーザーの満足度に対して決定的な役割を果たし、多様性や新規性だけよりも重要であることが明らかになった。

# 2. Recent Topics 2. 最近のトピックス

## 2.1. Sequential and Session-based Recommendation 2.1. シーケンシャルレコメンデーションとセッションベースレコメンデーション

The traditional problem formulation of recommender systems, as described in Section 1.2, is designed for making non-contextual item suggestions based on stable long-term user preferences.
セクション 1.2 で述べたような従来のレコメンダーシステムの問題定式化は、**長期的に安定したユーザーのpreferenceに基づいて**、**非context的な(i.e.文脈を考慮しない)アイテム提案**を行うように設計されている.
Such an approach is for example meaningful to present landing-page recommendations to a frequent user of a media streaming site.
このようなアプローチは、例えば、メディアストリーミングサイトを頻繁に利用するユーザーに対して、ランディングページの推薦を提示するのに有意義である.
However, there are many other important application scenarios where we cannot assume to have long-term preference information available.
しかし、**長期的な嗜好情報が利用可能であると仮定できない重要なアプリケーションシナリオ**は、他にも数多く存在する.
Think, for example, of visitors of an e-commerce shop who are not logged in or who are first time users.
例えば、Eコマースショップの訪問者で、ログインしていない人や初めて利用する人を考えてみよう.
Moreover, on an e-commerce site, a user’s interests and needs might change from shopping session to shopping session.
また、ECサイトでは、**ユーザーの興味やニーズは、ショッピングセッションごとに変化する可能性**がある.
Therefore, even if we would know the identity of the user it is important to consider the user’s short-term history and current intents when we determine what we should recommend to the user next.
そのため、たとえユーザーの身元がわかっても、**短期的な履歴と現在の意思を考慮**した上で、次に何を勧めるべきかを判断することが重要なのである.

### 2.1.1. Problem Definition and Terminology 2.1.1. 問題の定義と用語

These requirements, which cannot be easily addressed with the traditional matrix completion abstraction, led to the development of different types of sequence-aware recommender systems [Quadrana et al. 2018].
従来の行列補完の抽象化では容易に対応できないこれらの要件から、様々なタイプのsequenceを考慮したレコメンダーシステムが開発されました [Quadrana et al. 2018].
Instead of a user-item rating matrix, the main input to this type of recommenders consists of a sequence of logged interactions.
ユーザアイテムの評価行列の代わりに、このタイプのレコメンダーへの主な入力は、**ログに記録されたinteractionのsequence(=系列データのイメージ?)**で構成されている.
The entries of these logs are typically collected through the application, e.g., a web store, and they can have different types.
これらのログのエントリは、典型的にはアプリケーション、例えばウェブショップを通じて収集され、それらは異なるタイプを持つことができる.
A web shop might for example record item views, add-to-cart events, or purchases.
例えば、ウェブショップでは、アイテムビュー、カートに入れるイベント、または購入が記録されるかもしれない.
Moreover, each log entry is usually associated with an individual user.
さらに、各ログ・エントリーは、通常、個々のユーザーに関連付けられている.(そりゃそう.)
This can be a known user, who is logged in to the web shop, or an anonymous one which is only identified through a cookie or IP address.
これは、ウェブショップにログインしている既知のユーザーであることもあれば、クッキーや IP アドレスを通してのみ識別される匿名のユーザーであることもある.(なるほど...確かに.匿名ユーザの場合はshort-termの嗜好しか考慮できない.)
Finally, a last difference to the user-item rating matrix is that the interaction log may contain multiple user-item interaction pairs, for example, when the user viewed an item multiple times before a purchase.
最後に、ユーザ-アイテム評価マトリックスとの違いは、例えば、ユーザが購入前にアイテムを複数回見た場合、interaction logは、**同一のユーザ-アイテムinteraction pairを複数、ログに含むことができる**ということである.(一方でrating matrixの場合は、同一のuser-itemペアでログは一つ...!)
In addition, a log entry may have additional types of meta-data attached such as a time stamp.
さらに、ログにはタイムスタンプなどのメタデータが付加されている場合がある.
Overall, while the inputs are different from the matrix-completion problem, the output of a sequence-aware recommender is usually a ranked list of items.
全体として、入力は行列補完問題とは異なるが、sequenceを考慮したレコメンダーの出力は通常、アイテムのランク付けされたリストである.
Figure 2.1 shows an overview of the problem setting.
図 2.1 に問題設定の概要を示す.

Within the family of sequence-aware recommender systems, two related terms can be identified in the literature: (i) sequential recommendation and (ii) session-based recommendation.
**sequence-aware recommender systems** には、(i) **sequential recommendation** と (ii) **session-based recommendation** という2つの関連する用語が存在する.
Sequential recommendation refers to the more general problem of making next-item recommendations.
sequential recommendationとは、"**次のアイテムを推薦する**"という、より一般的な問題である.
A typical example is the problem of recommending the next Point-Of-Interest (POI) to a user in a tourism scenario or to recommend an entire next shopping basket in an ecommerce scenario.
典型的な例としては、観光の場面で**次のPOI(Point-Of-Interest)**をユーザに推薦する問題や、eコマースの場面で次の買い物かご全体を推薦する問題がある.
In session-based recommendation scenarios, the problem is also to make next-item predictions, but the underlying assumptions are that (a) the past interaction log is organized in usage sessions and that (b) recommendations are made in the context of an ongoing session.
session-based recommendationのシナリオでも、問題は"次のアイテムを予測すること"であるが、その基礎となる仮定は、（a）過去のinteraction logが使用セッション(usage session. ??)で整理されていること、（b）推薦が進行中のセッション(ongoing session = 短期的なセッション?)のcontextで行われることである.(sequential recommendationとどう違うんだろう...?)
Another underlying assumption of session-based approaches typically is that the user’s interests and needs can change from session to session.
session-basedのアプローチのもう一つの基本的な前提は、一般的に、"**ユーザーの興味やニーズがセッションごとに変化しうる**"ということである.
Furthermore, in many practical problem settings, no long-term preference information is available at all for the current user, which means that the recommendations must be based on a small set of interactions—e.g., a few item view events—that are observed in an ongoing session.
さらに、多くの実用的な問題設定において、現在のユーザーについて**長期的な嗜好情報が全く利用できない**. これは、推薦が、進行中のセッションで観察される小さなinteractionのセット、例えば、いくつかのアイテムビューイベントに基づく必要があることを意味する.
(sequential recommendationよりも、short-termなcontextを前提にしてる??)

In the literature, two alternative situations are considered when recommendations have to be made in the context of an ongoing session.
この文献では、進行中のsessionのコンテキストで推薦を行わなければならない場合、**2つの代替的な状況**が検討されている.
In one case, nothing is known about the current user but the interactions that are observed in the session.
1つは、現在のユーザーについて、**セッションで観察されるinteraction以外、何も知らない場合**である.(session-basedアプローチは、**IPアドレスやcookieのみでshort-termのinteraction logが得られるケース**??)
In the other case, also information about past sessions of the same user is available.
もう1つは、同じユーザの過去のセッションに関する情報も利用可能なケース(session-basedは、short-termだけではないのか...).
This second scenario is often referred to as personalized session-based recommendation or session-aware recommendation.
この2つ目のシナリオは、**personalized session-based recommendation**または**session-aware recommendation**と呼ばれることが多い。
Figure 2.2 visualizes the differences between (pure) session-based and session-aware recommendation problems.
図2.2に、pureなsession-based recommendation(シナリオ1)と session-aware recommendation(シナリオ2)の違いを示す.

### 2.1.2. Algorithms for Sequential and Session-based Recommendation 2.1.2. 逐次推薦とセッションベースの推薦のためのアルゴリズム

Various algorithmic approaches were explored for sequence-aware recommendation problems.
sequenceを考慮した推薦問題に対して、様々なアルゴリズム的アプローチが検討された.
The following main types of technical approaches were identified in [Quadrana et al. 2018]: (i) Sequence Learning Approaches (ii) Sequence-Aware Matrix Factorization (iii) Hybrid Approaches, and (iv) Nearest Neighbors and Other Methods.
Quadrana et al. 2018]では、技術的アプローチの主な種類として、（i）シーケンス学習アプローチ（ii）シーケンスを考慮した行列因子分解（iii）ハイブリッドアプローチ、および（iv）最近傍と他の方法、が挙げられた。

#### Sequence Learning Approaches. シーケンス学習のアプローチ。

Approaches in this category can be subdivided into several main paradigms.
このカテゴリのアプローチは、いくつかの主要なパラダイムに細分化することができます。

- Frequent Pattern Mining techniques were historically often applied for the problem of detecting (unexpected) patterns in shopping baskets, e.g., in the form of association rules. Later, these techniques were extended to consider sequential patterns, in which the order of the elements is relevant. 頻出パターンマイニング技術は、歴史的にしばしば買い物かごの中の（予期しない）パターンを検出する問題に適用されてきた（例えば、関連ルールの形で）。 その後、これらの技術は、要素の順序が関連するシーケンシャルなパターンを考慮するように拡張された。

- Sequence Modeling approaches try to go beyond mined patterns and aim to learn models from past time-ordered data to predict future events. A large variety of corresponding machine learning models were proposed over the years. The predominant approaches in the literature are based on Markov Models, Reinforcement Learning, or Deep Learning, in particular in the form of Recurrent Neural Networks (RNNs). Often, modern sequential models are based on ideas from Natural Language Processing to model the sequences in the interaction data, see e.g., [Sun et al. 2019a]. シーケンスモデリングのアプローチは、採掘されたパターンを超えて、過去の時間順のデータからモデルを学習し、将来のイベントを予測することを目的としている。 対応する機械学習モデルは、長年にわたって多種多様なものが提案されてきた。 文献上の主要なアプローチは、マルコフモデル、強化学習、またはディープラーニング、特にリカレントニューラルネットワーク（RNNs）の形式に基づいている。 多くの場合、現代のシーケンシャルモデルは、自然言語処理からのアイデアに基づいて、相互作用データのシーケンスをモデル化するものであり、例えば、[Sun et al. 2019a]を参照。

- Distributed Item Representations are another form of encoding sequential information. These representations (embeddings) are projections from sequences of item-related events (e.g., views) into a lower-dimensional representation in which the transition between items is preserved. 分散アイテム表現はシーケンシャルな情報を符号化するもう一つの形式である。 これらの表現（埋め込み）は、アイテムに関連するイベントのシーケンス（例えば、ビュー）から、アイテム間の遷移が保持された低次元の表現に投影されたものである。

- Supervised Learning with Sliding Windows, finally, is a rather specific approach, where the idea is to reframe the next-item prediction problem to a supervised learning problem by moving a sliding window over the sequence of events and to derive the corresponding feature values from this sliding window to predict the next event. スライディングウィンドウを用いた教師あり学習は、イベントのシーケンス上でスライディングウィンドウを移動させることによって、次アイテム予測問題を教師あり学習問題に再構成し、このスライディングウィンドウから対応する特徴量を導き出して次のイベントを予測するという、かなり特殊なアプローチである。

#### Sequence-Aware Matrix Factorization. 配列に配慮した行列因子分解。

A few examples exist in the literature that extend matrix factorization approaches to consider sequential information, usually derived from timestamps that are available for the entries in the user-item rating matrix.
行列分解アプローチを拡張して、連続的な情報、通常はユーザー-アイテム評価行列のエントリに利用可能なタイムスタンプから得られる情報を考慮するいくつかの例が文献に存在する。
These approaches are conceptually related to time-aware recommender systems [Campos et al. 2014], which aim to identify changes in user preferences over larger time spans.
これらのアプローチは、概念的には、より大きな時間スパンでのユーザー嗜好の変化を識別することを目的とした時間考慮型推薦システム[Campos et al.

#### Hybrid Approaches. ハイブリッド・アプローチ

A more common approach in the literature is to combine sequence modeling with the power of latent factor models.
文献上のより一般的なアプローチは、シーケンス・モデリングと潜在因子モデルのパワーを組み合わせることである。
One of the earlier approaches of that type is the Factorized Personalized Markov Chain (FPMC) method [Rendle et al. 2010].
このタイプの初期のアプローチの1つは，FPMC（Factorized Personalized Markov Chain）法である [Rendle et al.］
This method jointly factorizes a first-order Markov Chain, which models user-specific item transitions, and a traditional user-item rating matrix to make next-item predictions.
この方法は，ユーザ固有の項目遷移をモデル化した一次マルコフ連鎖と，従来のユーザ項目評価行列を合同で因子分解し，次の項目予測を行うものである．
Similar approaches were proposed later on, e.g., in [He and McAuley 2016].
同様のアプローチは、その後、例えば[He and McAuley 2016]で提案された。
More recently, methods that combine neural techniques (e.g., RNNs, Convolutional Neural Networks, or Attention) with matrix factorization layers, have become more popular, e.g., [Kang and McAuley 2018, Tang and Wang 2018].
最近では、ニューラル技術（RNN、Convolutional Neural Networks、Attentionなど）と行列分解層を組み合わせた手法が普及しており、例えば[Kang and McAuley 2018, Tang and Wang 2018]などである。

#### Nearest-Neighbors and Other Methods. 近傍界とその他の方法。

In particular in the context of session-based recommendation, a simple yet effective method is often to apply neighborhood-based techniques.
特にセッションベースの推薦の文脈では、シンプルかつ効果的な方法として、近傍ベースの技術を適用することがよくあります。
In [Jannach and Ludewig 2017] and subsequent works, the idea was explored to use those past sessions in the data as a basis for predicting the next event, which are most similar to the ongoing one.
Jannach and Ludewig 2017]とそれに続く作品では、現在進行中のイベントに最も類似している次のイベントを予測するための基礎として、データ内のそれらの過去のセッションを使用するというアイデアが検討されました。
Despite the conceptual simplicity of the approach, it turned out to be competitive or even superior to much more complex models.
このアプローチの概念的な単純さにもかかわらず、それははるかに複雑なモデルに対して競争力があるか、あるいは優れていることが判明した。
Finally, a number of alternative proposals were identified in [Quadrana et al. 2018], including methods that rely on (non-neural) graphbased models or techniques from discrete optimization, where the latter class of problems may however suffer from scalability problems given the usually high number of recommendable items.
最後に、多くの代替案が[Quadrana et al. 2018]で確認され、（非ニューラル）グラフベースのモデルや離散最適化の技術に依存する方法などがあり、後者のクラスの問題はしかし、通常推奨できるアイテムの数が多いことを考えるとスケーラビリティ問題に苦しむかもしれません。

### 2.1.3. Evaluation of Sequential and Session-based Recommender Systems 2.1.3. 逐次型推薦システムおよびセッション型推薦システムの評価

In practical applications, recommender systems are evaluated with respect to the organizational goals and purpose they should fulfill (e.g., increase customer retention) and the specific computational tasks they implement that serve this purpose (e.g., help users find novel content) [Jannach and Adomavicius 2016].
実際の応用では、レコメンダーシステムは、それらが果たすべき組織的な目標や目的（例えば、顧客維持率の向上）と、この目的を果たすために実装する特定の計算タスク（例えば、ユーザーが新規コンテンツを見つけるのを助ける）に関して評価される［Jannach and Adomavicius 2016］。
While the general goals of sequence-aware recommender systems are usually not very different from traditional ones, sequential and sessionbased recommenders often implement a number of computational tasks based on the particular nature of their input data, as identified in [Quadrana et al. 2018]:
シーケンスを考慮したレコメンダーシステムの一般的な目標は、通常、従来のものとあまり変わらないが、シーケンシャルおよびセッションベースのレコメンダーは、[Quadrana et al. 2018]で確認したように、入力データの特定の性質に基づく多くの計算タスクを実装することが多い。

- Context Adaptation is the fundamental problem of session-based algorithms, i.e., to guess the user’s situation and intents from the interactions observed in an ongoing session. The observed user behavior thus represents a form of interactional context [Adomavicius et al. 2022]. コンテキスト適応はセッションベースのアルゴリズムの基本的な問題であり、すなわち、進行中のセッションで観察された相互作用からユーザーの状況や意図を推測することである。 このように、観測されたユーザー行動は相互作用コンテキストの一形態を表す[Adomavicius et al.2022]。

- Trend Detection is a still under-explored topic in academic research and relates both to individual trends (e.g., interest drift) and community trends that might, for example, depend on seasonal patterns or popularity peaks of items. トレンドの検出は、学術的な研究においてまだ十分に検討されていないテーマであり、個々のトレンド（例えば、興味ドリフト）と、例えば、季節パターンやアイテムの人気ピークに依存するかもしれないコミュニティのトレンドの両方に関連する。

- Repeated Recommendations, which are usually not considered in matrix-completion problems, can both be valuable in the context of consumable items (e.g., printer ink) and for the sake of reminding users of items they liked in the past (e.g., a past favorite artist). 通常、行列補完問題では考慮されない「繰り返し推奨」は、消耗品（例えば、プリンターインク）の文脈でも、ユーザーが過去に好きだったもの（例えば、過去の好きなアーティスト）を思い出すためにも、どちらも価値があります。

- Consideration of Order Constraints and Patterns: In a number of domains, there is a strict order in which items should or must be recommended (e.g., learning course recommendation); in other domains, there might be a “natural” order in which things should be recommended (e.g., in the case of movie sequels). Sequence-aware recommenders can learn and/or enforce such patterns as a computational task. 順序の制約とパターンに関する考察。 多くの領域では、推奨されるべき、あるいはされなければならない順序が厳然として存在する（例：学習コースの推奨）。他の領域では、推奨されるべき「自然な」順序が存在する場合がある（例：映画の続編の場合）。 順序を意識したレコメンダーは、学習と

In principle, all evaluation approaches outlined in Section 1.4 can be applied for the evaluation of sequential and session-based recommender systems, including offline experiments, user studies, and field tests (A
逐次型およびセッション型レコメンダーシステムの評価には、オフライン実験、ユーザースタディ、フィールドテストなど、原則として1.4節で示したすべての評価手法が適用可能である（A

#### 2.1.3.1. Offline Evaluation 2.1.3.1. オフライン評価

Remember from above that the output of a sequence-aware recommender system as usual is a ranked list of item suggestions.
シーケンスを考慮した推薦システムの出力は、通常、アイテム提案のランク付けされたリストであることを、上記から思い出してほしい。
Following the usual “hide-and-predict” evaluation approach in offline experiments, common evaluation measures from information retrieval for ranking accuracy such as precision and recall can be applied.
オフライン実験での通常の「隠して予測する」評価方法に従って、精度や再現率といったランキング精度に関する情報検索の一般的な評価尺度を適用することができる。
The evaluation procedure of sequenceaware recommender systems therefore involves the hiding of a number of interactions in a given sequence of events and the subsequent measurement of how good an algorithm is to predict the hidden interaction(s).
したがって、シーケンス認識型レコメンダーシステムの評価方法は、与えられたイベントのシーケンスにおけるいくつかのインタラクションを隠し、その後、隠されたインタラクションを予測するアルゴリズムがどの程度優れているかを測定することになる。

In evaluations of traditional matrix completion problem settings, the selection of the hidden elements (i.e. the test set) is often done in a randomized way, e.g., by randomly selecting 20 % of the data for testing.
伝統的な行列補完問題設定の評価では、隠れ要素（すなわちテストセット）の選択は、例えば、テスト用にデータの20 %をランダムに選択するなど、ランダムな方法で行われることが多い。
Moreover, cross-validation is in many cases applied to increase the confidence in the observed results.
さらに、観測結果の信頼性を高めるためにクロスバリデーションが適用されるケースも多い。
Such an entirely randomized approach is not meaningful for sequence-aware recommendation problems, and alternative procedures have to be applied.
このような完全にランダム化されたアプローチはシーケンスを考慮した推薦問題では意味がなく、別の手順を適用する必要がある。

##### Data Splitting.

##### データ分割

When splitting the data into training, validation, and test data sets, the sequential order must be considered, and the held-out interactions to be predicted must happen after those that are used for training.
データをトレーニング、検証、テストデータセットに分割する際、順序を考慮する必要があり、予測するための保留された相互作用は、トレーニングに使用された相互作用の後に発生する必要があります。
Different strategies are possible in the data splitting process.
データ分割のプロセスでは、様々な戦略が可能である。
The following are relatively common.
以下は比較的一般的なものである。

- In sequential problem settings, often the splitting of the data is done per user. Commonly, the very last interaction of each user is hidden and put in the test set.1 逐次問題の設定では、多くの場合、データの分割はユーザーごとに行われる。 一般に、各ユーザーの最後のインタラクションは隠され、テストセットに入れられる1。

- In session-based scenarios, it is, in contrast, more common to apply a time-based split. Commonly, research datasets cover an extended period of time, e.g., a few weeks. Often, the sessions of the very last or the last few days are used for testing (and one or more preceding days for validation). 一方、セッションベースのシナリオでは、時間ベースの分割を適用することがより一般的です。 一般に、研究データセットは、数週間といった長期間をカバーする。 多くの場合、直近または数日前のセッションがテストに使用される（そして、1日以上前のセッションが検証に使用される）。

##### Making the Measurement.

##### 測定を行う。

In sequential recommendation problems, when the last interaction of each user is hidden, the making the measurement amounts to determining if and at which position an algorithm was ranking the hidden interaction within a top-n list.
逐次推薦問題では、各ユーザーの最後のインタラクションが隠されている場合、測定はアルゴリズムがトップNリスト内で隠されたインタラクションをランキングしていたか、どの位置にあるかを決定することになる。
Common evaluation measures therefore include the Hit Rate, the NDCG or the MRR at a certain cut-off length.
したがって、一般的な評価指標には、あるカットオフ長におけるHit Rate、NDCG、MRRが含まれる。

For session-based problems, these measures can be applied as well, but the evaluation procedure is slightly different.
セッションベースの問題についても、これらの測定方法を適用することができますが、 評価方法は若干異なります。
Remember that the test dataset typically contains entire user sessions and that the specific problem in session-based recommendation is to predict the next interaction(s) given the session beginning.
テストデータセットには通常、ユーザーセッション全体が含まれ、セッションベースの推薦における特定の問題は、セッションの始まりから次のインタラクションを予測することであることを思い出してください。
The options reported in the literature are to “reveal” all but the last interaction in a session, to reveal the first k elements, or to incrementally reveal one interaction after the other when measuring.
文献で報告されているオプションは、セッションの最後のインタラクションを除いたすべてを「明らかにする」、最初のk個の要素を明らかにする、または測定時に他の後に1つのインタラクションを増分的に明らかにすることです。
Different variants also exist how the accuracy measures are applied.
また、精度測定の適用方法にも様々なバリエーションが存在する。
One can, for example, measure how good an algorithm is to predict the immediate next item in a session, using the Hit Rate, NDCG, and MRR as typical measures for a given cut-off threshold.
例えば、あるカットオフ閾値の典型的な測定値としてヒット率、NDCG、MRRを使用して、アルゴリズムがセッションのすぐ次のアイテムを予測することがどれほど優れているかを測定することができます。
Alternatively, and probably more importantly, one can measure how many of the subsequent (and hidden) interactions in the session are contained in the top-n list returned by a recommender.
あるいは、おそらくもっと重要なことですが、セッションの後続の（そして隠れた）インタラクションが、レコメンダーが返すトップNリストにどれくらい含まれているかを測定することもできます。
In that case, measures like precision and recall are often used.
この場合、精度やリコールのような尺度がしばしば使われます。

Note that like in traditional recommendation scenarios, quality factors other than accuracy can be considered.
従来の推薦シナリオと同様に、精度以外の品質要因も考慮されることに注意してください。
Beyond-accuracy aspects considered in the literature in particular include the diversity of the recommendation lists, catalog coverage, popularity biases, or scalability.
特に文献上では、推薦リストの多様性、カタログの網羅性、人気の偏り、あるいはスケーラビリティなど、精度を超えた側面が考慮されています。

Generally, observe that while we hide interactions in the data, we are usually making predictions for items.
一般に、我々はデータ中のインタラクションを隠しているが、通常、アイテムの予測を行っていることを観察する。
In case there is only one type of interactions in the logs, e.g., listening events on a music streaming site, an item prediction corresponds to predicting a listening event.
ログに含まれるインタラクションが1種類しかない場合、例えば音楽ストリーミングサイトの試聴イベントであれば、アイテム予測は試聴イベントの予測に相当する。
However, real-world datasets often consist of interactions of different types, e.g., item views, add-to-cart actions, or purchases on an e-commerce site.
しかし、実世界のデータセットには、アイテム閲覧、カートへの追加、ECサイトでの購入など、異なるタイプのインタラクションが含まれることが多い。
In many academic research works, only the most frequent type of interactions is considered, for example item views.
多くの学術的な研究成果では、最も頻度の高いタイプのインタラクション、例えばアイテムビューのみが考慮されている。
In reality, however, it might be much more important to predict item purchases, and to use all available types of interactions in the training and prediction process.
しかし、現実には商品購入を予測することの方がはるかに重要であり、学習と予測プロセスにおいて利用可能なすべてのタイプのインタラクションを使用する必要があるかもしれない。

##### Cross-Validation.

##### クロスバリデーション

Given the sequential nature of the data, performing cross-validation based on random splits is not meaningful.
データの連続性を考えると、ランダムな分割に基づくクロスバリデーションは意味がない。
In the literature, often only one single train-test split is applied, which, however, bears a certain risk that the obtained results are specific to that split.
文献では、しばしば1つの訓練とテストの分割のみが適用されますが、これは得られた結果がその分割に特有であるというリスクを伴います。
An alternative approach therefore is to create multiple overlapping or non-overlapping timebased splits of the data, and to repeat the measurement on these splits, see [Ludewig et al. 2021].
したがって，代替的なアプローチとして，複数の重複するまたは重複しない時間ベースのデータ分割を作成し，これらの分割で測定を繰り返す方法があります．

#### 2.1.3.2. User-Centric Evaluation 2.1.3.2. ユーザーを中心とした評価

User-centric research, while not uncommon in the recommender systems literature in general, is still very rare in the context of sequential and session-based recommendation.
ユーザー中心の研究は、推薦システムの文献全般では珍しくないものの、順次推薦やセッションベースの推薦の文脈ではまだ非常に稀です。
In one study in the music domain [Kamehkhosh and Jannach 2017], researchers compared different techniques for next-track music recommendations.
音楽ドメインにおけるある研究 [Kamehkhosh and Jannach 2017] では、研究者は次のトラックの音楽推薦のためのさまざまな技術を比較しました。
In this study, participants were presented with a number of alternative continuations for a given playlist.
この研究では，参加者は与えられたプレイリストに対していくつかの代替的な継続を提示されました．
In another study [Ludewig and Jannach 2019], an online interactive radio station was created for the purpose of the experiment.
別の研究[Ludewig and Jannach 2019]では、実験のためにオンラインのインタラクティブなラジオ局が作成された。
Different algorithms were used to create playlist based on the a start track provided by the user and based on the feedback during the radio listening session.
ユーザーによって提供された開始トラックに基づいて、またラジオ聴取セッション中のフィードバックに基づいてプレイリストを作成するために、異なるアルゴリズムが使用されました。
Both mentioned studies led to interesting insights regarding the quality perceptions of users and investigated to what extent offline accuracy measures align with user perceptions.
これらの研究は、ユーザーの品質認識に関する興味深い洞察をもたらし、オフラインの精度測定がユーザーの認識とどの程度一致しているかを調査しました。
Besides such specific research setups, the use of general frameworks for the user-centric evaluation of recommender systems can be applied, e.g., [Pu et al. 2011] or [Knijnenburg et al. 2012].
このような特定の研究セットアップの他に、推薦システムのユーザ中心的な評価のための一般的なフレームワークを使用することができます。

#### 2.1.3.3. Real-World Evaluation 2.1.3.3. 実世界での評価

For more traditional recommendation problems, a number of success stories from real-world deployments of recommender systems exist, see [Jannach and Jugovac 2019].
より伝統的な推薦問題については、推薦システムの実世界での展開から多くの成功事例が存在する[Jannach and Jugovac 2019]を参照。
In the area of sequential and session-based recommendations, such reports are rare.
逐次推薦やセッションベースの推薦の分野では、そのような報告は稀である。
An exception is the work in [Kouki et al. 2020], which reports on the use of session-based recommendation technology for an online shop in the home improvement domain.
例外は[Kouki et al. 2020]の研究で、ホームセンター領域のオンラインショップにセッションベースの推薦技術を使用したことが報告されています。
Ultimately, the use of a modern neural approach led to a significant increase in relevant business KPIs when compared to an existing commercial software for retail recommendation.2
最終的に、最新のニューラルアプローチの使用により、既存の小売推薦のための商用ソフトウェアと比較して、関連するビジネスKPIを大幅に増加させることができました2。

Another interesting aspect of this work lies in how the decision was made which of several existing session-based algorithms should be put in practice.
この研究のもう一つの興味深い点は、いくつかの既存のセッションベースのアルゴリズムのうち、どれを実用化すべきかをどのように決定したかにある。
First of all, the authors benchmarked a number of techniques, including conceptually simple and more complex ones, through an offline evaluation.
まず、著者らはオフライン評価を通じて、概念的に単純なものからより複雑なものまで、多くの手法をベンチマークした。
Reproducing previous offline experiments [Ludewig et al. 2021], they found that simple methods in many cases outperform the latest neural techniques in terms of typical accuracy measures.
以前のオフライン実験[Ludewig et al. 2021]を再現し、彼らは多くの場合、単純な手法が典型的な精度指標の点で最新のニューラル技術より優れていることを見いだした。
A subsequent evaluation with human experts however revealed that the well-performing nearest-neighbor technique might not be the best choice in the given application domain.
しかし、その後の人間の専門家による評価では、よく機能する最近傍技術は、与えられたアプリケーションドメインでは最良の選択ではない可能性があることが明らかになった。
While it is often able to correctly predict a single hidden element, other algorithms turned out to be more successful in recommending more than one possibly relevant item.
このアルゴリズムは、1つの隠し要素を正しく予測できることが多いのですが、複数の関連する可能性のある項目を推薦する場合には、他のアルゴリズムの方がより成功することがわかりました。
In particular, other algorithms often returned items that are similar to the hidden one, which could therefore represent purchase alternatives for the customers.
特に、他のアルゴリズムでは、隠されたアイテムと類似したアイテムを返すことが多く、そのため、顧客にとって購入の選択肢となり得るものであった。
As a result, this study emphasizes not only the possible limitations of offline evaluations, it also stresses that in practice it is important to understand the specifics of a particular application and how a recommender is expected to create value.
この結果、本研究は、オフライン評価の限界だけでなく、実際には、特定のアプリケーションの詳細と、レコメンダーがどのように価値を生み出すかを理解することが重要であることを強調している。

### 2.1.4. Discussion and Outlook 2.1.4. 考察と展望

In particular session-based and session-aware are highly relevant practical problems for which we have seen a number of technical proposals in recent years.3 However, despite the many complex algorithms that are developed, it is surprising to see that in many cases very simple techniques based on nearest-neighbors are competitive or even outperform the latest neural techniques in offline evaluations [Garg et al. 2019, Kouki et al. 2020, Ludewig et al. 2021].
しかし、多くの複雑なアルゴリズムが開発されているにもかかわらず、多くの場合、最近傍に基づいて非常に単純な技術が、オフライン評価において最新のニューラル技術に勝るとも劣らない、あるいは勝っていることは驚くべきことです[Garg et al.2019, Kouki et al.2020, Ludewig et al.2021]．
Such phenomena are however not specific to session-based recommendation problems, see [Ferrari Dacrema et al. 2021] for a discussion of similar problems that were observed for traditional top-n recommendation scenarios.
しかし、このような現象はセッションベースの推薦問題に特有のものではなく、従来のトップN推薦シナリオで観察された同様の問題については[Ferrari Dacrema et al. 2021]を参照してください。
Overall, this points to certain methodological issues that may hamper progress in the field.
全体として、これはこの分野の進歩を妨げる可能性のある特定の方法論的問題を指摘している。

On the other hand, these observations also indicate that there is huge potential for the development of even better algorithms for session-based and sequential recommendation.
一方、これらの考察は、セッションベース推薦や逐次推薦のためのさらに優れたアルゴリズムの開発には大きな可能性があることも示している。
In particular, the use of side information, e.g., in the form of item meta-data, the use of contextual information, and the consideration of multiple types of interactions in parallel seem to be promising areas for future work.
特に、アイテムのメタデータなどの側面情報の利用、文脈情報の利用、複数種類のインタラクションを並行して考慮することなどは、今後の有望な分野であると思われる。

## 2.2. Popularity, Bias and Recurrence in Recommendation 2.2. レコメンデーションにおける人気度、偏り、再現性

As the view of recommendation shifted from rating prediction to item ranking, an new phenomenon was observed: offline evaluation tends to reward the recommendation of popular items, that is, items involved in frequent interaction with users [Cremonesi et al. 2010].
レコメンデーションが評価予測から項目ランキングへと移行するにつれて，オフライン評価では人気項目，すなわちユーザと頻繁にやりとりする項目が推奨されやすいという新しい現象が観察された [Cremonesi et al.2010]．
This becomes a strong bias to the same extent that the data distribution over items—the so-called popularity distribution—is heavily skewed in a long-tail shape.
これは，人気度分布がロングテール型に大きく歪んでいるのと同様に，強いバイアスとなる．
With a random data split, the popularity effect in evaluation is a clear self-fulfilling prophecy: the items with most training data—the popular items—have the most test data, which are used as relevance judgments, as discussed in Section 1.4.3.
ランダムなデータ分割の場合、評価における人気度効果は明確な自己成就予言となる：学習データの多い項目（人気項目）が、関連性判断に用いられるテストデータを多く持つ、これは1.4.3節で述べたとおりである。
Hence, by ranking popular items highly in recommendations, we get fewer missing ratings in the ranking top, resulting in improved chances of producing high relevance metric values [Bellog´ın et al. 2017, Canamares and Castells 2018].
したがって、レコメンデーションで人気のあるアイテムを高くランク付けすることで、ランキングトップでの欠落評価が少なくなり、結果として高い関連性メトリック値を生成するチャンスが向上します[Bellog´ın et al.2017, Canamares and Castells 2018]。
Even with ˜ temporal splits, the popularity distributions on the respective sides of the split point are usually correlated (to the extent that item popularity persists over time), whereby the popularity bias remains [Bellog´ın et al. 2017, Mena-Maldonado et al. 2021].
また、〜時間的な分割があっても、分割点のそれぞれの側の人気分布は通常（アイテムの人気が時間と共に持続する程度に）相関があり、それによって人気バイアスが残る［Bellog´ın et al.2017, Mena-Maldonado et al.2021］.

Given this effect, it seems not surprising that state of the art collaborative filtering algorithms are also heavily biased to recommend popular items, as researchers have found systematically [Canamares and Castells 2017, Jannach et al. 2015b].
この効果を考えると、研究者が体系的に発見しているように、最先端の協調フィルタリングアルゴリズムも人気のあるアイテムを推奨するように大きく偏っていることは驚くことではないようです[Canamares and Castells 2017, Jannach et al. 2015b]。
This realization has fueled ˜ research in two directions: a) avoiding or countering the biases in both evaluation and algorithms, under an implicit view of bias as a potential distortion of learning and evaluation [Bellog´ın et al. 2017, Jadidinejad et al. 2021, Steck 2010, 2011]; and b) better understanding where the bias may come from, and wondering whether it might be harmless or even useful to some extent [Canamares and Castells 2018].
この認識は2つの方向で〜研究を促進した：a）学習と評価の潜在的な歪みとしてのバイアスの暗黙の見解の下、評価とアルゴリズムの両方でバイアスを回避または対抗する［Bellog´ın et al.2017, Jadidinejad et al.2021, Steck 2010, 2011］、b）バイアスがどこから来るのか、よりよく理解し、ある程度は無害または有用かもしれないという疑問［Canamares and Castells 2018］.
An additional fundamental perspective has re- ˜ cently gained momentum that considers the dual role of recommendation in satisfying users, on one side, and learning from their interactions with the delivered recommendations, on the other.
追加の基本的な視点は、一方ではユーザーを満足させ、他方では配信された推薦との相互作用から学習するという推薦の二重の役割を考慮する再〜最近勢いを増しています。
We briefly discuss these perspectives in the following paragraphs.
以下の段落で、これらの視点について簡単に説明します。

### 2.2.1. Countering Bias 2.2.1. バイアスへの対応

From a certain angle, popularity can be considered intrinsically undesirable from an addedvalue perspective that, as such, should be avoided.
ある角度から見れば，人気は付加価値の観点からは本質的に好ましくないものであり，避けるべきものであるとも考えられる。
This is the viewpoint of novelty as a complementary goal of recommendation as discussed in Section 1.4.5.1.
これは 1.4.5.1 節で述べた推薦の補完目標としての新規性という観点である。
Even from this perspective, novelty should still be combined with relevance, and relevance needs to be evaluated; the relevance-seeking component, and its evaluation, are likely to be affected by popularity biases.
この観点からも、新規性と関連性を両立させ、関連性を評価する必要があるが、関連性追求の要素やその評価は人気バイアスに影響される可能性が高い。
Specific evaluation procedures have been researched aiming to remove the popularity bias from the metrics [Bellog´ın et al. 2017, Schnabel et al. 2016, Steck 2010, 2011] and the algorithms [Hernandez-Lobato et al. 2014, Jannach et al. 2017, Liu ´ et al. 2020].
メトリクスやアルゴリズムから人気度バイアスを取り除くことを目的とした具体的な評価方法が研究されている [Bellog´ın et al.2017, Schnabel et al.2016, Steck 2010, 2011] [Hernandez-Lobato et al.2014, Jannach et al.2017, Liu´ et al.2020].
Among them, counterfactual reasoning approaches for off-policy learning and evaluation are being actively researched, using techniques such as inverse propensity scoring (IPS) [Jadidinejad et al. 2021, Schnabel et al. 2016, Swaminathan et al. 2017].
その中でも、政策外学習・評価のための反実仮想推論アプローチは、逆性向スコアリング（IPS）[Jadidinejad et al. 2021, Schnabel et al. 2016, Swaminathan et al. 2017]などの技術を用いて、活発に研究されている。
IPS produces unbiased estimators for metrics and objective functions by modeling the distribution of observations over the user-item space, and compensating for it in the evaluation metrics and the learning algorithms, by downweighting observed preferences by the probability of observing them.
IPSは、ユーザー・アイテム空間上の観測値の分布をモデル化し、観測された嗜好を観測する確率で重み付けすることにより、評価指標と学習アルゴリズムにおいてそれを補正することで、指標と目的関数に対する不偏推定量を生成する。
Challenges involved in the application of IPS in this context include modeling the propensity bias from biased samples, and the boundless variance of IPS weights when observation probability can be indefinitely small.
この文脈でのIPSの適用に関わる課題として、偏ったサンプルからの傾向バイアスのモデル化、および観測確率が無限に小さくなり得る場合のIPS重みの無限の分散が挙げられる。

### 2.2.2. Understanding Bias 2.2.2. バイアスを理解する

Beyond the capability to remove or harness biases, some authors argued for a better understanding of popularity distributions and their potential harm or innocuity as a distorting factor in evaluation [Canamares and Castells 2018].
バイアスを除去または利用する機能を超えて、一部の著者は人気分布と評価における歪曲要因としての潜在的な害または無害性についてよりよく理解することを主張しました[Canamares and Castells 2018]。
After all, recommender system applications ˜ make deliberate use of popularity signals [Amatriain and Basilico 2015], where popularity is not necessarily an entirely bad property—whereas naive popularity countering in evaluation might assess this signal as equivalent to random recommendation.
結局のところ、推薦システムアプリケーション〜は人気シグナルを意図的に利用し[Amatriain and Basilico 2015]、ここで人気は必ずしも完全に悪い特性ではない-一方、評価における素朴な人気カウンターリングはこのシグナルをランダム推薦と同等と評価するかもしれません。
Canamares and Castells ˜ [2018] theorized about the formation of popularity distributions, and found out specific conditions that determine whether or not system comparisons are preserved in evaluation under popularity biases.
Canamares and Castells 〜 [2018]は、人気度分布の形成について理論化し、人気度バイアス下での評価においてシステム比較が保たれるかどうかを決定する具体的条件を見いだした。
The key to the answer lies in the conditional dependencies between observation, relevance and items as random variables, which explain why majority choices and majority tastes can be useful in delivering effective suggestions.
その答えの鍵は、観測、関連性、ランダム変数としてのアイテムの間の条件依存性にあり、これにより、なぜ多数決や多数派嗜好が効果的な提案を行うのに有用であるかが説明されています。
These findings have been extended later in experiments showing a high degree of agreement in evaluation with biased and unbiased data [Mena-Maldonado et al. 2021].
これらの知見は後に、偏ったデータと偏らないデータを用いた評価で高い一致を示す実験で拡張されている[Mena-Maldonado et al. 2021]。
In other words, the general findings in this line are that feedback loops and Matthew effects [Merton 1968] can sometimes have a virtuous component [Ciampaglia et al. 2018].
つまり、この系統の一般的な知見は、フィードバックループやマシュー効果［Merton 1968］は、時に好循環的な要素を持ちうるというものである［Ciampaglia et al.2018］。
Acting upon this awareness, Zhang et al. [2021] explore a finer handling of popularity at training and inference time, seeking to mitigate distortion while leveraging the useful signal.
この認識に基づいて行動するZhangら[2021]は、有用な信号を活用しながら歪みを軽減することを目指し、学習時および推論時における人気度のより細かい取り扱いを探求しています。

### 2.2.3. The Feedback Loop 2.2.3. フィードバックループ

A major source of bias in offline data is the production system through which the interaction data—the input for recommendation—are collected.
オフラインデータにおけるバイアスの主な原因は、推薦のための入力であるインタラクションデータが収集される生産システムにある。
Recommender systems are commonly integrated in multi-component applications where items are exposed to user feedback through different pathways: search, browsing, recommendation, front page, etc.
推薦システムは、検索、ブラウジング、推薦、フロントページなど、さまざまな経路でユーザーのフィードバックにさらされる、マルチコンポーネント・アプリケーションに統合されるのが一般的です。
Each of such components introduces bias of its own.
このような構成要素は、それぞれ独自のバイアスをもたらします。
To the extent that a recommendation component feeds on user interaction with its own output, we have a feedback loop [Chaney et al. 2018b, Fleder and Hosanagar 2009].
推薦コンポーネントが自身の出力とユーザーとのインタラクションを餌にする範囲では、フィードバックループが発生します[Chaney et al.］
This loop, in combination with offline evaluation, creates a magnification effect (also known as snowball, Matthew effect, rich-gets-richer), where the data collected for evaluation reward and reinforce the hypotheses ingrained in the production system, making popular items ever more popular, and penalizing change [Chaney et al. 2018a].
このループは、オフライン評価との組み合わせで、拡大効果（スノーボール、マシュー効果、リッチゲットリッチャーとも呼ばれる）を生み出し、評価のために収集したデータが生産システムに染み付いた仮説に報酬を与えて強化し、人気アイテムをますます人気にして、変化にペナルティを与えます［Chaney et al.2018a］.
As a result the system can get stuck in its own assumptions and miss out on value and opportunities that remain hidden in unobserved choices.
その結果、システムは自身の仮定に囚われてしまい、観察されていない選択肢に隠れたままの価値や機会を逃してしまうことがあります。

Furthermore, perverse incentives can arise from such loops, where user engagement, sometimes tightly associated to short-term revenue, is blindly targeted by the recommendation strategy—recommendation might then be inducing compulsive or toxic behavior, rather than (or mixed with) serving a constructive purpose [Whittaker et al. 2021].
さらに，このようなループから逆インセンティブが発生する可能性があり，短期的な収益と密接に関連することもあるユーザーエンゲージメントが，推薦戦略によってやみくもに目標とされ，推薦が建設的な目的を果たすのではなく（あるいは混合して）強制的または有害な行動を誘発する可能性があります [Whittaker et al.2021]．
Such rabbit hole traps may result in suboptimal long-term business performance at best, or unwillingly contribute to toxic phenomena such as misinformation spreading, polarization, and radicalization, at worst.
そのようなラビットホールの罠は、よく言えば長期的なビジネスパフォーマンスを最適化しない結果になり、悪く言えば誤報の拡散、分極化、過激化といった有害な現象を不本意ながら助長してしまうかもしれません。
Preventing such risks and harmful effects is not all that simple, and to a great extent requires continual monitoring and direct specialized intervention, a revision of the business model and incentives, and dealing with non-trivial ethical questions [Stray 2020, Zuckerberg 2018].
このようなリスクや有害な影響を防ぐことは、それほど単純ではなく、かなりの程度、継続的な監視と直接的な専門的介入、ビジネスモデルやインセンティブの見直し、そして自明ではない倫理的問題への対処が必要となります［Stray 2020, Zuckerberg 2018］。

From a more generic and algorithmic viewpoint, a promising approach to breaking feedback loops is the reinforcement learning perspective, where the algorithm is understood to be an agent that aims to please and learn simultaneously [Sutton and Barto 2021].
より一般的でアルゴリズム的な観点からは、フィードバックループを断ち切るための有望なアプローチは強化学習の観点であり、アルゴリズムは喜びと学習を同時に目指すエージェントであると理解されている[Sutton and Barto 2021]。
A recommendation is seen as an opportunity to match user interests to the best of the current system knowledge (immediate optimization), but also to extend this knowledge by exploring yet unknown or uncertain areas, so as to produce better recommendations in the future.
推薦とは、ユーザーの興味を現在のシステム知識のベストに合わせる（即時最適化）機会であると同時に、将来より良い推薦を行うために、まだ未知の領域や不確実な領域を探索し、この知識を拡張する機会でもあると考えられている。
Optimal solutions care for both the long and short term (exploration and exploitation), striving to achieve a subtle balance.
最適なソリューションは、長期と短期の両方（探索と開拓）を考慮し、微妙なバランスを達成しようとするものです。
After all, the mission of a recommender system is not circumscribed to a single recommendation for every user, but hopefully a recurrent, cyclic, mutually beneficial relationship with the customer over an extended time span.
結局のところ、レコメンダーシステムの使命は、すべてのユーザーに対して1回の推薦を行うことではなく、長期間に渡って顧客と反復的、循環的、互恵的な関係を築くことなのです。
Much of the literature in the field builds however implicitly on the view of a once-in-a-lifetime interaction with the user.
しかし、この分野の文献の多くは、ユーザーとのやりとりは一生に一度という考えを暗黙のうちに持っています。

Developments in this area have adapted so-called multi-armed bandit (MAB) approaches [Sutton and Barto 2021], where items are seen as actions to be selected (choices to be recommended) [Hill et al. 2017].
この分野の開発は、いわゆる多腕バンディット（MAB）アプローチ［Sutton and Barto 2021］を適応しており、ここでアイテムは選択されるべきアクション（推奨されるべき選択肢）として見られる［Hill et al.2017］．
When chosen, actions return a reward (a utility or value for the user), drawn from an unknown distribution, and the goal of the system is to maximize the cumulative rewards over time.
選択されたとき、アクションは未知の分布から引き出された報酬（ユーザーにとっての効用または値）を返し、システムの目標は時間の経過とともに累積報酬を最大化することである。
MAB algorithms break the feedback loop by injecting a controlled degree of guided stochastic exploration beyond local maxima (a controlled bit of informed randomness, to put it simply), seeking a better explore vs. exploit balance than traditional, pure exploitation approaches (which include all the algorithms discussed in Section 1.3).
MABアルゴリズムは、局所最大値を超える制御された程度のガイド付き確率的探索を注入することによってフィードバックループを断ち切り、従来の純粋な探索アプローチ（セクション1.3で議論したすべてのアルゴリズムを含む）よりも優れた探索対開発のバランスを追求するものである。
In order to define personalized solutions, so-called contextual variants of MAB are developed, where the context fundamentally includes the user, and the reward depends on the context [Li et al. 2016].
個人化された解決策を定義するために、いわゆる文脈的なMABの変種が開発されており、文脈は基本的にユーザを含み、報酬は文脈に依存する[Li et al.］

Further generalization beyond contextual MAB considers the effect that recommendations have on the user state, thus representing the interaction of users with the system as a Markov Decision Process (MDP) [Xin et al. 2020].
さらに、文脈的 MAB を超えて一般化すると、推薦がユーザの状態に与える影響を考慮し、ユーザとシステムの相互作用を Markov Decision Process (MDP) として表現する [Xin et al.2020] 。
MDP are also applied as a natural fit to represent sequential recommendation [Xin et al. 2022a], that we discussed earlier in Section 2.1.
MDP はまた、セクション 2.1 で述べた逐次レコメンデーション [Xin et al. 2022a] を表現するために自然に適用される。
MDPoriented solutions typically require large amounts of online interaction in order to be effective, which may take more time to start producing good recommendations than is affordable [Afsar et al. 2022].
MDP指向のソリューションは、一般的に効果的であるために大量のオンライン対話を必要とし、良い推薦を生成し始めるまでに手頃な時間よりも多くの時間がかかるかもしれない[Afsar et al.2022]。
This can be mitigated by complementary offline training using more abundant logged interaction data, which then introduces bias from the logging policy [Xin et al. 2022b], that needs to be dealt with as discussed earlier.
これは、より豊富なログを取得したインタラクションデータを用いた補完的なオフライン学習によって軽減することができますが、その場合、ロギングポリシーからバイアスが発生し [Xin et al. 2022b] 、先に述べたように対処する必要があります。
Reinforcement learning in recommendation is a rapidly growing area, with tight connections to counterfactual learning and evaluation; the reader may find a good starting point towards more in-depth readings in the survey by Afsar et al. [2022].
推薦における強化学習は、反実仮想学習や評価と密接に関連し、急速に成長している分野です。読者はAfsarらによる調査[2022]でより深い読書への良い出発点を見つけることができるかもしれません。

As a final note from a broader abstract perspective, popularity biases can be seen as arising from a compound feedback loop involving manifold channels of user-item discovery and feedback, interacting with and mutually reinforcing each other.
最後に、より広い抽象的な視点から、人気度バイアスは、ユーザーアイテムの発見とフィードバックの多様なチャンネルを含む複合フィードバックループから生じ、相互に作用し、相互に補強し合っていると見ることができる。
Direct novelty enhancement, bias-countering techniques, and reinforcement learning can be seen as multiple solutions in a common direction seeking a degree of healthy exploration in recommendations.
直接的な新規性向上、バイアスカウンター技術、および強化学習は、推薦における健全な探索の度合いを求める共通の方向性を持つ複数のソリューションと見なすことができる。

## 2.3. Impact and Value of Recommender Systems 2.3. リコメンダーシステムの影響と価値

Over the last thirty years, recommender systems have been successfully deployed in many application domains, and their value both for consumers and businesses is undisputed [Jannach and Jugovac 2019].
過去 30 年以上にわたって、推薦システムは多くのアプリケーション領域で成功裏に展開され、消費者と企業の両方にとってその価値は議論の余地がない [Jannach and Jugovac 2019]。
However, like many other areas of applied machine learning—including various subfields of information retrieval—academic research in recommender systems is mostly not based on studies with deployed systems, but largely relies on a data-centric approach.
しかし、情報検索の様々なサブフィールドを含む応用機械学習の他の多くの分野と同様に、推薦システムの学術研究は、ほとんどが展開されたシステムでの研究に基づいておらず、主にデータ中心アプローチに依存しています。
Moreover, differently from observational and analytical types of data-based research, where the goal for example is to understand certain phenomena from recorded data, recommender systems research almost exclusively focuses on developing novel prediction models.
また、記録されたデータからある現象を理解することを目的とした観測的・分析的なデータベース研究とは異なり、レコメンダーシステムの研究は、ほとんどが新しい予測モデルの開発に焦点を当てたものです。
The research question in such experiments is therefore mostly not “What made a recommendation successful?”
したがって、このような実験における研究課題は、ほとんどの場合、"何がレコメンデーションを成功させたのか？"ではありません。
[Jannach et al. 2017] or “Are popular items, when recommended, more likely to be purchased by users?”, but almost exclusively if a new prediction model is able to more accurately predict the held-out past data.
[Jannach et al. 2017]や "人気のある商品は、推薦されると、ユーザーが購入する可能性が高いのか？"ではなく、ほとんど、新しい予測モデルが、保持している過去のデータをより正確に予測できるかどうかにかかっています。

The holy grail in recommender systems research today therefore is to improve the prediction accuracy of algorithms.
したがって、今日のレコメンダーシステム研究の聖杯は、アルゴリズムの予測精度を向上させることです。
The underlying and generally plausible assumption is that better accuracy leads to the effect that more relevant items appear at higher positions in the recommendation lists.
一般に、精度を向上させると、より関連性の高いアイテムが推薦リストの上位に表示されるようになる、というのがその根底にある、もっともらしい仮説です。
As a result, the more relevant items are easier to discover by the users, thereby reducing information overload.
その結果、より関連性の高い項目がユーザーによって発見されやすくなり、情報過多を軽減することができる。
In this context, one central feature of almost any recommender system lies in the personalization of the item suggestions.4 As such, recommender systems can seen as strategies to implement digital one-to-one marketing and hyper-segmentation.
このように、レコメンダーシステムは、デジタルOne to Oneマーケティングやハイパーセグメンテーションを実現するための戦略として位置づけられることが多い。

Unfortunately, the assumed correspondence of higher prediction accuracy on past data with better overall value for the user or the provider of the recommendations is less than certain.
しかし、残念ながら、過去のデータに対する予測精度が高いほど、ユーザーやレコメンデーションの提供者にとっての総合的な価値が高くなるという想定は、あまり確実ではありません。
A number of academic research works for example report that higher prediction accuracy only sometimes lead to a better quality perception by users, as obtained through user studies.
例えば、多くの学術的な研究成果では、ユーザー調査により、予測精度が高いほどユーザーによる品質認識が向上する場合があると報告されています。
Also various works from industry, e.g., by Netflix, report that the offline experimentation is often not predictive of online success [Gomez-Uribe and Hunt 2015].
また，Netflixなどの産業界からの様々な研究は，オフラインでの実験がオンラインでの成功を予測できないことが多いと報告しています[Gomez-Uribe and Hunt 2015]．
The limitations of relying solely on accuracy measures can be easily illustrated.
精度の指標だけに頼ることの限界は、簡単に説明することができます。
Imagine a user who liked the first two “Avengers” movies and rated them highly on an online video rental platform.
オンラインビデオレンタルプラットフォームで、最初の2つの「アベンジャーズ」映画を気に入り、高い評価をしたユーザーを想像してください。
An algorithm that then recommends three additional Avengers films along with related superhero movies, might even reach an accuracy of 100 %.
すると、アベンジャーズ3作品と関連するスーパーヒーロー映画を追加で推薦するアルゴリズムでは、100%の精度に達するかもしれません。
While being 100 % accurate, the recommendation might be of little value both for the user—as the recommendation list is obvious and maybe too monotone—and the provider, because the user would have rented these movies anyway.
しかし、100％の精度で推薦されても、ユーザーにとっては、推薦リストが明白であり、単調すぎるため、またプロバイダーにとっては、ユーザーがこれらの映画をレンタルしてしまうため、あまり価値がない可能性があります。
Recommending these movies can therefore even represent a missed opportunity to promote other items.
このような映画の推薦は、他の商品を宣伝する機会を逸することになります。

Given these observations, it is pivotal that the field of recommender systems moves beyond research that is solely based on offline experiments and abstract accuracy measures.
これらのことから、推薦システムの分野では、オフラインの実験や抽象的な精度指標のみに基づいた研究を乗り越えることが極めて重要です。
Such a change is highly important, in particular because it is not clear if small improvements on a specific accuracy measure for a given dataset—such things are commonly reported in published research—would even matter in practice.
このような変化は非常に重要です。特に、あるデータセットに対する特定の精度指標の小さな改善（研究発表でよく報告されるもの）が、実際には重要かどうかさえも明らかではないからです。

In this section, we therefore first emphasize the importance of considering the human in the loop when proposing new algorithms or user interfaces for recommender systems (Section 2.3.1).
そこで、本節では、まず、推薦システムの新しいアルゴリズムやユーザインタフェースを提案する際に、人間をループ内に考慮することの重要性を強調する（2.3.1節）。
Then, we discuss the various ways in which recommender systems can create value, both for consumers and recommendation providers, and why it is important to evaluate recommender systems with respect to their intended purpose (Section 2.3.2).
次に、推薦システムが消費者と推薦提供者の双方にとってどのような価値を生み出すことができるのか、また、なぜ推薦システムをその目的に応じて評価することが重要なのかについて述べる（2.3.2項）。

### 2.3.1. Understanding the Impact of Recommendations with the Human in the Loop 2.3.1. 人間をループに入れたレコメンデーションの影響を理解する

There are a number of relevant questions one might have to address when building a recommender system in practice, for example:
例えば、実際にレコメンダーシステムを構築する際には、多くの関連する問題に取り組まなければならないことがあります。

- Would users find the recommendations provided by a system useful? • Would they find them novel, diverse, or entertaining, and would they ultimately be satisfied with the recommendations? ユーザーは、システムから提供される推薦文が役に立つと感じるだろうか？ - また、そのレコメンデーションに満足するでしょうか？

- Would they believe that the system’s recommendations are trustworthy, would they like to see an explanation? システムの提案は信頼に足ると思うか、説明が欲しいか。

- Will they consider the system’s recommendations in their decisions in the future? 今後、このシステムの提言を考慮して意思決定を行うのでしょうか？

All these aspects might have an impact on the ultimate success of a recommender system, which depends on whether or not users adopt the system’s recommendations.
これらの側面はすべて、レコメンダーシステムの最終的な成功に影響を与える可能性があり、それはユーザーがシステムの推奨事項を採用するかどうかにかかっている。
Unfortunately, none of these questions can be answered with typical offline experiments.
残念ながら、これらの疑問は典型的なオフライン実験では答えることができない。
Ultimately, recommending online—to a large extent—is a problem of human-computer interaction, where a computerized, interactive system is designed to support its users in an information-finding or decision-making task.
結局のところ、オンラインでのレコメンデーションは、人間とコンピュータの相互作用の問題であり、コンピュータ化されたインタラクティブなシステムは、情報検索や意思決定タスクにおいてユーザーを支援するように設計されている。
Thus, studies that involve users are a necessary means to explore questions like those mentioned above.
したがって、ユーザーを対象とした研究は、上記のような疑問を解決するために必要な手段である。

The most common form of such studies are experiments in the form of a randomized controlled trial, where the study participants are randomly assigned to either one or more treatment groups or to a control group.
このような研究の最も一般的な形態は、無作為化比較試験の形式をとる実験で、研究参加者は1つ以上の治療群または対照群のいずれかに無作為に割り付けられる。
In many such studies, the participants interact with different versions of a prototype system in a controlled environment, often in a lab.
このような研究の多くでは、研究参加者は、制御された環境、しばしば研究室において、異なるバージョンのプロトタイプシステムと相互作用する。
For example, in an experiment on effects of providing explanations to users, one participant group would interact with a system that provides explanations, and the other one with one that does not.
たとえば、ユーザーへの説明の効果に関する実験では、ある参加者グループは説明を提供するシステム、他のグループは説明を提供しないシステムと相互作用することになる。
The existence of the explanations would therefore be the manipulated independent variable in the experiment.
したがって、説明の有無が実験における操作対象である独立変数となる。
Depending on the specific research question, various dependent variables can be measured.
具体的な研究課題に応じて、さまざまな従属変数を測定することができる。
These dependent variables can either be objectively measured, e.g., by recording the participants’ behavior like mouse clicks or interaction time, or they can be obtained by asking participants to self-report their perceptions in a questionnaire.
これらの従属変数は、例えば、マウスクリックやインタラクション時間のような参加者の行動を記録することによって客観的に測定することもできるし、参加者にアンケートで認識を自己申告してもらうことによって得ることもできる。
If the research question, for example, is if explanations help reducing the user’s decision effort, one can both measure the time needed to make a choice from the given recommendations, and ask participants about the perceived effort of the task.
例えば、説明がユーザーの意思決定の労力を減らすのに役立つかどうかという研究課題であれば、与えられた推奨事項から選択を行うのに必要な時間を測定し、タスクの労力の認識について参加者に尋ねることができる。
After the experiment, various statistical analyses can be made to assess if the existence of explanations may have caused or is at least correlated with the observations for decision effort.
実験後、様々な統計分析を行い、説明の有無が意思決定努力の観察結果を引き起こしたか、少なくとも相関があるかどうかを評価することができる。

Differently from typical offline experiments, such user studies are guided by explicit research questions or hypotheses, which are commonly derived from theoretical considerations.
一般的なオフライン実験とは異なり、このようなユーザー研究は明確なリサーチクエスチョンや仮説に導かれており、それらは一般的に理論的考察から導き出されるものである。
As a consequence, each user study requires a specific experimental design that is suited to answer these research questions.
その結果、各ユーザースタディでは、これらのリサーチクエスチョンに答えるのに適した特定の実験デザインが必要となる。
This fact and the need to recruit participants for the study, which are representative for at least a subset of the target population, makes user studies typically more effortful than offline experiments, which are often not based on theoretical considerations or explicit research questions.
この事実と、少なくともターゲット集団のサブセットを代表する研究参加者を募集する必要性から、ユーザー研究は、理論的考察や明確なリサーチクエスチョンに基づかないことが多いオフライン実験よりも一般的に労力がかかる。

User-centric evaluation frameworks, as proposed in [Pu et al. 2011] or [Knijnenburg et al. 2012] are one way of standardizing such user experiments at least to some extent.
Pu et al. 2011] や [Knijnenburg et al. 2012] で提案されているユーザ中心評価フレームワークは、このようなユーザ実験を少なくともある程度まで標準化する方法の一つです。
These frameworks include a number of general quality factors and the potential effects of recommender systems on user behavior.
これらのフレームワークでは、一般的な品質要因や推薦システムがユーザー行動に及ぼす潜在的な影響などが多く含まれています。
Figure 2.3 provides an overview of the ResQue framework [Pu et al. 2011], which—partly inspired by the Technology Acceptance Model—proposes to assess the potential impact of user quality perceptions on their beliefs, attitudes and future behavioral intentions.
図 2.3 は、ResQue フレームワーク [Pu et al. 2011] の概要を示しており、一部 Technology Acceptance Model に触発され、ユーザの品質認識がユーザの信念、態度、将来の行動意図に与えうる影響を評価することを提案し ている。
Besides the identification of the relevant constructs (variables) in the model, the framework furthermore provides a set of questionnaire items that can be used to measure the participants’ subjective perceptions in an experiment.
このフレームワークは、モデルにおける関連する構成要素（変数）の特定に加えて、実験において参加者の主観的な知覚を測定するために使用できる一連のアンケート項目を提供しています。

Generally, controlled experiments with users are much more common in the Information Systems literature than in the Computer Science literature on recommender systems.
一般的に、推薦システムに関するコンピュータサイエンスの文献よりも、情報システムの文献の方が、ユーザーを使った統制された実験がはるかに一般的である。
Given that many important questions—in particular also regarding the user interface of recommenders [Jugovac and Jannach 2017]—cannot be answered with the predominant but narrow focus on improving prediction models, it is important that research in recommender systems more often considers evaluations with users in the loop.
多くの重要な疑問、特にレコメンダーのユーザーインターフェースに関しても[Jugovac and Jannach 2017]、予測モデルの改善に関する優勢だが狭い焦点では答えられないことを考えると、レコメンダーシステムの研究がより頻繁にユーザーとのループで評価を検討することは重要である。
Clearly, user studies also have their limitations, e.g., that the study participants are not interacting with a real system or are typically not making real purchase decisions.
明らかに、ユーザー研究は、例えば、研究参加者が実際のシステムと相互作用していない、または一般的に実際の購入の意思決定をしていないなどの制限があります。
Nonetheless, such studies can provide us with relevant indications of what might matter for users in the real world.
しかし、このような研究は、実世界のユーザーにとって何が重要であるかについて、適切な示唆を与えることができます。

Finally, note that controlled experiments are not the only form of evaluations with the human in the loop.
最後に、制御された実験だけが、人間を使った評価ではないことに注意してください。
Various other types of observational studies as well as qualitative research methods, such as focus groups or interviews, are commonly applied in academia and in industry.
フォーカスグループやインタビューなどの定性的な研究手法だけでなく、他のさまざまなタイプの観察研究が、学界や産業界で一般的に適用されています。

### 2.3.2. Consumer and Business Value of Recommender Systems 2.3.2. リコメンダーシステムの消費者価値とビジネス価値

Ultimately, any recommender system is designed to create utility or value for one or more of the involved stakeholders.
最終的に、どのようなレコメンダーシステムも、関係する一人以上のステークホルダーに対して効用や価値を生み出すように設計されている。
The academic literature historically focuses on the consumer value, at least implicitly.
学術的な文献では、歴史的に少なくとも暗黙のうちに消費者価値に焦点が当てられている。
One underlying assumption often is that if a recommender system is able to create value for consumers, e.g., by helping them to discover novel items, this at least indirectly leads to value for the business or organization that provides the recommendations.
例えば、レコメンダーシステムが消費者に新しいアイテムを発見させるなどして価値を生み出すことができれば、少なくとも間接的にはレコメンダーを提供するビジネスや組織の価値につながるというのが、一つの基礎となる仮定であることが多い。
Such considerations seem plausible, for example, for music or video streaming services that are based on flat-rate subscription rates.
例えば、定額制の音楽・映像ストリーミングサービスでは、このような配慮が必要と思われる。
The more the consumers are engaged with the service—due to the constant discovery of new content—the more likely they might be to renew their subscription at the end of the month.
消費者は、常に新しいコンテンツを発見することによって、そのサービスに夢中になればなるほど、月末に契約を更新する可能性が高くなるかもしれません。
However, the goals of the provider might not always be fully aligned with the value perspective of consumers, leading to multi-stakeholder recommendation problems.
しかし、サービス提供者の目標と消費者の価値観が必ずしも一致しない場合があり、マルチステークホルダー推奨の問題が発生する。

#### 2.3.2.1. Recommendation as a Multi-Stakeholder Optimization Problem 2.3.2.1. マルチステークホルダー最適化問題としてのレコメンデーション

Different types of entities can be involved in the recommendation process [Abdollahpouri et al. 2020a, Jannach and Bauer 2020].
推薦プロセスには、さまざまな種類のエンティティが関与することができる[Abdollahpouri et al 2020a, Jannach and Bauer 2020]．

- Consumers or End Users are the recipients of the recommendations. This can be individual users or groups of users. In the latter group recommendation setting, see [Masthoff and Delic 2022], typically the needs and preferences of different group members must ´ be balanced, i.e., there can be multiple stakeholders in the group. 消費者またはエンドユーザーは、レコメンデーションの受信者です。 これは個々のユーザーである場合もあれば、ユーザーのグループである場合もあります。 後者のグループ推薦の設定（[Masthoff and Delic 2022]を参照）では、通常、異なるグループメンバーのニーズと好みのバランスをとる必要があり、すなわち、グループ内に複数の利害関係者が存在する可能性があります。

- Recommendation Service Providers are the organizations that are in the control of the recommender system, which they run as part of their business. Typical examples include large online retailers or media streaming providers. レコメンデーションサービスプロバイダとは、レコメンデーションシステムをコントロールする組織で、ビジネスの一環として運営されている。 典型的な例としては、大規模なオンライン小売業者やメディアストリーミングプロバイダーが挙げられる。

- Suppliers are the entities that create or provide the items that are offered through the recommendation services. In the e-commerce example, this could be the manufacturers; in the media domain, it could be artists or labels, or other content providers. Note that the recommendation service providers can also be the suppliers of the items they offer. サプライヤーとは、レコメンデーションサービスを通じて提供されるアイテムを作成・提供する主体である。 電子商取引の例では製造業者、メディア領域ではアーティストやレーベル、その他のコンテンツプロバイダーが該当する可能性があります。 なお、レコメンデーションサービスプロバイダーは、提供するアイテムのサプライヤーである場合もある。

- Society: In case a recommendation service affects a large portion of a society, e.g., feed recommendations on a social media site, recommender systems can also have a societal impact, e.g., when the recommender system reinforces certain political opinions in an unbalanced way. 社会 推薦サービスが社会の大部分に影響を与える場合、例えば、ソーシャルメディアサイトのフィード推薦のように、推薦システムが特定の政治的意見を偏った形で強化する場合、推薦システムは社会的影響を与えることもある。

Consider the following example, which illustrates the potential challenges of considering multiple stakeholders interests [Jannach and Bauer 2020].
複数の利害関係者の利益を考慮することの潜在的な課題を示す次の例について考えてみましょう [Jannach and Bauer 2020]。
Imagine an online hotel search service which charges a commission fee to hotel owners for each booking that is made through the site.
オンラインホテル検索サービスでは、サイトを通じて予約されるごとにホテルオーナーに手数料が課金されるとします。
From the consumer’s perspective, the best recommendation is one that satisfies their needs, usually given certain budget constraints.
消費者の視点に立てば，最良のレコメンデーションとは，自分のニーズを満たすものであり，通常，一定の予算制約がある．
The recommendation service provider, on the other hand, might try to maximize its short-term profit (commission).
一方、推薦サービス提供者は、短期的な利益（手数料）を最大化しようとするかもしれない。
A recommender system might therefore select items that represent a reasonable match for the consumer, but lead to higher profit for the platform.
そのため、レコメンデーションシステムは、消費者にとっては合理的なマッチングであっても、プラットフォームにとってはより高い利益につながるアイテムを選択する可能性がある。
At the same time, the hotel platform might also try to ensure that all hotel suppliers are recommended from time to time, so that the platform remains attractive for the suppliers.
同時に、ホテル・プラットフォームは、サプライヤーにとって魅力的なプラットフォームであり続けるために、すべてのホテル・サプライヤーが随時推薦されるようにしようとするかもしれない。
The hotel chains, finally, might have an interest that the recommender system pushes a certain subset of the offerings through recommendations, for example, the more expensive ones.
ホテルチェーンは、レコメンダーシステムが特定のサブセット（例えば、より高価なもの）を推奨することに関心を持つかもしれない。

Today, research in multi-stakeholder recommender systems is still limited.
今日、マルチステークホルダー・レコメンダーシステムの研究はまだ限定的である。
Works exist, for example, for the specific problems of reciprocal recommendation [Palomares et al. 2021], price and profit aware recommender systems [Jannach and Adomavicius 2017], or in the area of algorithmic fairness and biases, e.g., [Abdollahpouri et al. 2020b, Mehrotra et al. 2018b].
例えば、相互推薦 [Palomares et al. 2021]、価格と利益を考慮した推薦システム [Jannach and Adomavicius 2017]、あるいはアルゴリズムの公平性とバイアスの領域など、特定の問題に対する研究が存在します [Abdollahpouri et al. 2020b, Mehrotra et al. 2018b]．
Generally, a particular challenge in the context of multi-stakeholder recommendation lies in the fact that the most common evaluation approach—accuracy evaluation on historical datasets—are typically not sufficient to investigate these problems.
一般に、マルチステークホルダー推薦の文脈における特定の課題は、最も一般的な評価アプローチ（過去のデータセットにおける精度評価）が、一般的にこれらの問題を調査するには不十分であるという事実にある。
Instead, alternative methodological approaches are needed, e.g., based on simulation techniques [Ghanem et al. 2022, Zhang et al. 2020].
その代わりに、例えばシミュレーション技術に基づく代替的な方法論的アプローチが必要である[Ghanem et al.］
This is particularly important because balancing multiple stakeholder goals often requires longitudinal analyses that are able to uncover the long-term effects on the involved stakeholders.
複数のステークホルダーの目標のバランスをとるには、関係するステークホルダーへの長期的な影響を明らかにすることができる縦断的な分析が必要な場合が多いため、これは特に重要なことである。

#### 2.3.2.2. Impact and Value Oriented Recommender Systems Evaluation 2.3.2.2. インパクト・価値志向の推薦システム評価

In practical deployments, the performance of recommender systems is determined in terms of Key Performance Indicators (KPIs) that are selected or defined by responsible organizational units.
レコメンダーシステムを実際に導入する場合、そのパフォーマンスは、担当する組織単位で選択または定義されるKPI（Key Performance Indicator）の観点から決定される。
What is actually being measured primarily depends on the purpose that is intended to achieve with the recommender system.
実際に測定されるものは、主にレコメンダーシステムで達成しようとする目的に依存する。
Therefore, the particular choice or design of the KPI also depends on the specific business model of the provider.
したがって、KPI の特定の選択または設計は、プロバイダの特定のビジネスモデルにも依存する。

A survey of real-world success stories of recommender systems [Jannach and Jugovac 2019] identified the following main types of measurements that are taken in practice:
レコメンダーシステムの実際の成功事例に関する調査[Jannach and Jugovac 2019]では、実際に行われている主な計測の種類を次のように特定しました。

- Click-Through-Rates (CTR): The CTR is traditionally most suitable in ad-based business models, i.e., where page impressions matter. In recommendation scenarios, optimizing for click-rates may however be too short-sighted in many applications. クリックスルー・レート（CTR）。 CTRは、広告ベースのビジネスモデル、すなわちページインプレッションが重要な場合に伝統的に最も適しています。 しかし、レコメンデーションのシナリオでは、クリック率を最適化することは、多くのアプリケーションで近視眼的すぎる可能性があります。

- Adoption and Conversion Measures: These measures go beyond counting click events. They, for example, only count a recommendation as successful, if there are signs that it was truly useful for consumers, e.g., when they watched a recommended movie. アドプションとコンバージョンの測定。 これらの指標は、クリック数をカウントする以上のものである。 例えば、レコメンデーションが消費者にとって本当に有益であった場合（例えば、レコメンデーションされた映画を観た場合など）にのみ、成功としてカウントされる。

- Sales and Revenue: This is the most direct measurement and can, for example, consist of determining how much additional sales was stimulated by a recommender. 売上と収益。 これは最も直接的な測定で、例えばレコメンダーによってどれだけ売上が増加したかを決定することができます。

- Effects on Sales Distributions: Measures of that type are useful to assess the impact of the recommendations on consumer behavior, e.g., if they could be persuaded to select different options compared to a situation with no recommender. 売上分布への影響。 この種の測定は、消費者の行動に対する推薦の影響を評価するのに有用である。例えば、推薦者がいない状況と比較して、異なる選択肢を選択するように説得できたかどうかなどである。

- User Engagement: This measure is often considered to be related with long-term customer loyalty. When consumers interact more with a service, this is considered a sign that they will come back for purchases in the future or that they will continue or renew their subscription. ユーザーエンゲージメント。 この指標は、しばしば長期的な顧客ロイヤリティと関連していると考えられている。 消費者がサービスとのインタラクションを深めることで、将来的に購入に訪れたり、購読を継続・更新したりする兆しと見なされる。

The specific choice of these KPIs, as discussed, can be strongly tied to the specific market situation and individual business models of the recommendation providers.
これらの KPI の具体的な選択は、議論されているように、特定の市場状況や推薦プロバイダーの個々のビジネ スモデルに強く結びついている可能性がある。
Academic research typically does not target at the idiosyncrasies of such specific situations but aims at providing generalizable insights.
学術的な研究は、このような特殊な状況を対象とするのではなく、一般化できる知見を提供することを目的としているのが一般的です。
Nonetheless, it is important—also in academia–which kinds of value recommender systems can generate, both for consumers and providers.
しかし、推薦システムが消費者と提供者の双方にとってどのような価値を生み出すことができるかは、学術的にも重要である。

Today’s research, as outlined above, is largely (implicitly) focused on the value for consumers, which is often circumscribed as helping users to find items of interest (or: “Find good items” [Herlocker et al. 2004]).
今日の研究は、上記のように、主に（暗黙のうちに）消費者にとっての価値に焦点を当てており、それはしばしば、ユーザーが興味のあるアイテムを見つけるのを助けること（または：「良いアイテムを見つける」 [Herlocker et al. 2004]）として包含されます。
Commonly, prediction accuracy metrics are used as proxies to measure this value by determining how good an algorithm is at predicting previously recorded and held-out positive interactions between a user and an item (see Section 1.4).
一般に、予測精度メトリクスは、ユーザーとアイテムの間の以前に記録され、保持された肯定的な相互作用を予測する際にアルゴリズムがどれだけ優れているかを決定することによって、この価値を測定するプロキシとして使用されます（セクション1.4参照）。
While this abstraction is generally useful and provides as with a standardized way of operationalizing the research problem, it may represent an oversimplification of the problem and even misguide our research efforts, as discussed above.
この抽象化は一般的に有用であり、研究問題を操作する標準的な方法を提供するが、上述のように、問題の過度な単純化を表し、研究努力を誤らせる可能性さえある。
In reality, there are many different ways in which recommender systems can create value, see [Jannach and Bauer 2020].
現実には、レコメンダーシステムが価値を生み出すには様々な方法がある [Jannach and Bauer 2020] 。

To overcome this somewhat narrow research operationalization, researchers have proposed a purpose- and value-oriented framework for the evaluation of recommender systems [Jannach and Adomavicius 2016].
このやや狭い研究運用を克服するために、研究者はレコメンダーシステムの評価のための目的・価値志向のフレームワークを提案している[Jannach and Adomavicius 2016]。
The main goal of this conceptual framework is to guide researchers—both in academia and industry—in terms of how they measure the success of a recommender system.
この概念的枠組みの主な目的は、学術界と産業界の両方の研究者が、レコメンダーシステムの成功をどのように測定するかを導くことである。
Specifically, the framework aims to ensure that what is measured, i.e., the KPIs or metrics that are used, is aligned with the intended purpose of the system.
特に、このフレームワークは、測定されるもの、すなわち、使用されるKPIまたはメトリックが、システムの意図された目的に沿っていることを保証することを目的としています。

The proposed framework, which considers both the consumer and provider perspective, has four layers: (i) Overarching Goals, (ii) Purpose of the Recommender, (iii) Computational Task, (iv) Evaluation Approach.
消費者と提供者の両方の視点を考慮した提案フレームワークは、(i) 包括的な目標、(ii) 推薦者の目的、(iii) 計算タスク、(iv) 評価アプローチの4層から構成されています。
To understand how the framework works, consider the case of an online media streaming service.
このフレームワークがどのように機能するかを理解するために、オンラインメディアストリーミングサービスのケースを考えてみる。
The overarching goal from a business perspective— which can be entirely independent of any recommendation technology—might be to ensure the long-term profitability of the service.
ビジネスの観点からは、レコメンデーション技術とは全く関係なく、サービスの長期的な収益性を確保することが大きな目標になります。
The specific purpose of a recommender in that context that serves this goal might be to increase user engagement.
このような状況でレコメンダーが果たすべき具体的な目的は、ユーザーのエンゲージメントを高めることかもしれません。
One way to achieve this increased engagement can be to provide consumers with a mix of familiar and novel recommendations to support discovery.
このエンゲージメントを高める方法のひとつは、消費者に馴染みのあるレコメンデーションと新しいレコメンデーションをミックスして提供し、発見をサポートすることであろう。
The computational task of the recommender system therefore is to determine such a mix.
したがって、レコメンダーシステムの計算タスクは、そのようなミックスを決定することである。
Finally, the evaluation approach must be chosen that it is aligned with the original overarching goals In the example, it could be a mixed methods approach, where (a) offline evaluations is used to gauge the accuracy and novelty levels of alternative algorithms, where (b) user studies are conducted to assess the intention of potential consumers to use the service in the future and where (c) field studies determine the impact of the recommendations on the user’s media streaming activity.
この例では、（a）オフライン評価で代替アルゴリズムの精度と新規性を評価し、（b）ユーザー調査で潜在的な消費者が将来サービスを利用する意図を評価し、（c）フィールド調査でユーザーのメディアストリーミング活動に対する推薦の影響を判断する、という混合手法のアプローチが可能です。

The most important point in this context—which should become obvious when using the proposed framework—is that relying solely on computational measures (such as prediction accuracy), can be too limiting.
この文脈で最も重要なことは、提案するフレームワークを使えばわかると思いますが、計算上の尺度（予測精度など）だけに頼っていては限界があることです。
In practice, there are probably not too many cases where measures like accuracy strictly correlate with aspects that matter more in practice, such as customer retention or customer satisfaction.
実際には、精度のような尺度が、顧客維持や顧客満足のような、より重要な側面と厳密に相関するケースはあまり多くないと思われます。
Therefore, as discussed in more depth in [Jannach and Bauer 2020], a paradigm shift seems needed in terms of how we evaluate recommender systems.
したがって、[Jannach and Bauer 2020] で詳しく述べられているように、レコメンダーシステムの評価方法についてパラダイムシフトが必要であると思われる。
Such a paradigm shift should ultimately lead to more impactful research in this area.
このようなパラダイムシフトは、最終的にこの領域でよりインパクトのある研究につながるはずです。
To achieve this progress researchers should, for example:
この進歩を達成するために、研究者は、例えば、以下のことを行う必要があります。

- more often adopt a purpose-oriented evaluation approach, as described, where goals and evaluation measures are ensured to be better aligned; のように、目的志向の評価アプローチを採用することが多く、目標と評価尺度の整合性をより確実にすることができます。

- consider a multi-method research approach, which also includes human-in-the-loop evaluations both in terms of controlled experiments and qualitative research; また、制御された実験や質的研究によるヒューマンインザループの評価も含む、多方面にわたる研究アプローチを検討します。

- expand their methodological repertoire also in terms of improved data-based evaluations, considering for example simulation-based approaches to investigate longitudinal effects; 例えば、縦断的効果を調査するためのシミュレーションベースのアプローチなどを検討し、データに基づく評価の改善という点でも、方法論のレパートリーを広げる。

- consider domain- and application specifics more often where appropriate, acknowledging that there is no “best model” and that the same set of recommendations might be good in one situation and sub-optimal in another one. 最適なモデル」は存在せず、同じ推奨事項がある状況では有効でも、別の状況では最適でない可能性があることを認識し、適切な場合にはドメインやアプリケーションの特定をより頻繁に考慮します。

Following such advice might ultimately help to avoid a dead end in algorithms research, which is not only heavily focused on abstract metrics, but is also suffering from certain methodological problems [Ferrari Dacrema et al. 2021], which may limit the impact of current recommender research in practice.
このようなアドバイスに従うことで、最終的にアルゴリズム研究の行き詰まりを回避できるかもしれません。この研究は抽象的な指標に重きを置いているだけでなく、特定の方法論の問題に悩まされており［Ferrari Dacrema et al. 2021］、現在の推薦者研究の実践における影響を制限してしまう可能性があるのです。

## 2.4. Summary and Future Directions 2.4. まとめと今後の方向性

We conclude this paper with a brief summary, pointers to further readings, and an outlook on
本稿の最後に、簡単なまとめと参考文献の紹介、そして今後の展望を述べます。

important future directions in this area.
は、この分野における重要な将来の方向性を示しています。

### 2.4.1. Summary 2.4.1. 概要

Today, personalized recommendations are a central component of many online services, and various success stories are reported in the literature how such systems create value both for users and organizations.
今日、パーソナライズド・レコメンデーションは多くのオンラインサービスの中心的な要素であり、このようなシステムがユーザーと組織の両方に価値をもたらすという様々な成功事例が文献で報告されている。
Due to their wide success in practice, research interest has correspondingly been continuously growing over the past twenty-five years.
そのため、過去25年にわたり、レコメンダーシステムに対する研究者の関心も高まり続けています。
Ultimately, this led to the development an own recommender systems research field, which is historically strongly rooted in information retrieval, machine learning, and human-computer interaction.
その結果、情報検索、機械学習、ヒューマンコンピュータインタラクションに歴史的に強く根ざしている推薦システム研究分野独自の発展を遂げるに至った。
In this paper, we have first characterized the recommendation problem on an abstract and application-independent level and then reviewed the most common way of operationalizing the research problem as a matrix completion problem.
本論文では、まず、推薦問題を抽象的かつアプリケーションに依存しないレベルで特徴づけ、次に、この研究問題を行列補完問題として運用する最も一般的な方法を検討した。
After discussing the most common types of recommendation algorithms, we elaborated on how to evaluate recommender systems “in the lab” and “in the wild”.
また、最も一般的な推薦アルゴリズムの種類を説明した後、推薦システムを「実験室で」「実際に」評価する方法について詳しく説明した。
Finally, we reviewed recent technical developments in the area of session-based recommendation and approaches based on reinforcement learning.
最後に、セッションベースの推薦と強化学習に基づくアプローチの分野における最近の技術開発について概説した。

### 2.4.2. Further Readings and Future Directions 2.4.2. 参考文献と今後の方向性

In this paper, we largely focused on algorithmic aspects of recommender systems, which traditionally is also the most active area of research.
本論文では、伝統的に最も研究が盛んな分野でもあるレコメンダーシステムのアルゴリズム的な側面に大きく焦点を当てました。
However, building a recommender systems in practice requires much more than just a clever algorithm [Jannach et al. 2016b, Xiao and Benbasat 2007].
しかし、実際にレコメンダーシステムを構築するには、巧妙なアルゴリズムだけでなく、それ以上のものが必要です [Jannach et al.2016b, Xiao and Benbasat 2007]。
Questions of the user experience of recommender systems— the HCI perspective—and the impact of recommenders on users—the Information Systems perspective—seem to be underexplored compared to the large amount of algorithmic research that we observe today.
レコメンダーシステムのユーザーエクスペリエンスに関する問題（HCIの視点）、レコメンダーがユーザーに与える影響（情報システムの視点）は、今日見られる大量のアルゴリズム研究と比較して、未解明であるように思われます。
More research often seems also required regarding the idiosyncrasies of particular application domains of recommender systems, acknowledging that there is no “best” application-independent algorithm and that the success of a recommender can only be evaluated relative to its intended purpose.
また、アプリケーションに依存しない「最高の」アルゴリズムは存在せず、レコメンダーの成功はその意図された目的に対してのみ評価されることを認識し、レコメンダーシステムの特定のアプリケーションドメインの特異性に関して、より多くの研究が必要であると思われることが多い。
As a result, an algorithm that works well for predicting movie relevance scores based on long-term user preferences might not be suited well for the recommendation of possible short-lived news articles or the context-dependent recommendation of music or points-of-interest in the tourism domain.
その結果、長期的なユーザーの好みに基づいて映画の関連性スコアを予測するアルゴリズムが、短期的なニュース記事の推薦や、文脈に依存した音楽や観光地のポイントの推薦には適していないかもしれない。
Various applications of recommender systems are discussed in more depth in the Recommender Systems Handbook [Ricci et al. 2022].
レコメンダーシステムのさまざまな応用は、レコメンダーシステムハンドブック [Ricci et al. 2022] でより深く議論されている。

In the same handbook, a variety of other timely research topics in recommender systems are discussed, which were not considered here, including the recent algorithmic developments, context-awareness, attacks on recommender systems, privacy aspects, or human factors in the evaluation process.
このハンドブックでは、推薦システムに関するタイムリーな研究テーマが数多く取り上げられているが、ここでは取り上げなかったアルゴリズム開発、コンテキストアウェアネス、推薦システムに対する攻撃、プライバシー面、評価プロセスにおけるヒューマンファクターなど、他にも様々なトピックがある。
In the remainder of this paper, we would like to discuss a small set of additional promising topics of which we believe that they require more research in the future.
本論文の残りの部分では、今後さらに研究が必要であると思われる有望なトピックを追加して議論したいと思う。

#### Conversational Recommender Systems. 会話型推薦システム。

Most of today’s online recommender system have a rather simple user interaction model.
今日のオンライン・レコメンダーシステムのほとんどは、ユーザーとのインタラクションモデルがかなり単純である。
At defined places in the application, the system presents users with recommendations, and often the only available user action is to inspect or accept these recommendations.5 With the recent developments in natural language processing, the current progress in machine learning in general, and the increased spread of voice-enabled devices, more interactive forms of information retrieval and recommendation [Radlinski and Craswell 2017] have received renewed interest in recent years.
アプリケーション内の定義された場所で、システムはユーザーに推薦を提示し、多くの場合、利用可能なユーザーアクションはこれらの推薦を検査するか受け入れるかのみです5。近年の自然言語処理の発展、機械学習全般における現在の進歩、および音声対応デバイスの普及の増加に伴い、よりインタラクティブな形の情報検索と推薦 [Radlinski and Craswell 2017] は近年再び関心を集めてきています。
One vision of such conversational recommender systems (CRS) is that they are able to act like a human and engage in a “natural” conversation with their users, see [Jannach et al. 2021] for a survey.
このような会話型推薦システム（CRS）の一つのビジョンは、人間のように振る舞い、ユーザーと「自然な」会話ができることであり、その調査については [Jannach et al. 2021] を参照されたい。
Correspondingly, such future systems will be able to support a variety of user intents [Cai and Chen 2019], thus supporting interactive preference elicitation and revision, explanation, and also chit-chat.
そのため、このような将来のシステムは、ユーザの様々な意図をサポートすることができ[Cai and Chen 2019]、したがって、対話的な好みの引き出しと修正、説明、さらに雑談をサポートすることができる。
While historically such CRS were often built based on engineered knowledge, e.g., about possible dialog states, many of today’s approaches also consider “end-to-end learning” as their main approach, where a machine learning model is trained on larger collections of dialogues between humans.
歴史的にそのようなCRSは、例えば可能な対話状態についての工学的知識に基づいて構築されることが多かったが、今日の多くのアプローチは、人間同士の対話のより大きなコレクションで機械学習モデルを訓練する「エンドツーエンド学習」を主要アプローチとして考慮することも多い。
Considerable progress was made in that context in recent years.
近年、その文脈でかなりの進展があった。
Still, pure learning-based approaches still have their limitations, and it is expected that future CRS will be often based on a mix of explicit domain and inference knowledge and of learning components.
しかし、純粋な学習ベースのアプローチにはまだ限界があり、将来のCRSはしばしば、明示的なドメインと推論知識、および学習コンポーネントの混合に基づくことが予想される。

#### Fairness in Recommender Systems. 推薦システムにおける公平性

Fairness and ethical concerns have grown around the exponential development of artificial intelligence and technology, permeating and transforming all realms of modern societies—and recommendation technologies are no exception to these matters.
人工知能やテクノロジーの急激な発達に伴い、現代社会のあらゆる領域に浸透し、変容していく中で、公正さや倫理に関する懸念が高まっており、推薦技術もこれらの問題の例外ではありません。
Recommendation functionalities can determine the success of a music artist on Spotify, a seller on Amazon, a job candidate or a recruiter through LinkedIn, a research author on Google Scholar, a hotel owner on Booking.com, an Internet celebrity on YouTube, Instagram or TikTok, a political party or a world view or a value system through online news and online media.
レコメンデーション機能は、Spotifyの音楽アーティスト、Amazonの販売者、LinkedInの求職者や採用担当者、Google Scholarの研究者、Booking.comのホテルオーナー、YouTubeやInstagram、TikTokのインターネットセレブ、ネットニュースやネットメディアの政党や世界観、価値観の成功を決定することが可能である。
As mediators between providers and consumers, recommender systems, willingly or not, get laded with a burden of responsibility they can hardly let go of.
提供者と消費者の仲介役であるレコメンダーシステムは、好むと好まざるとにかかわらず、手放しでは喜べない重荷を背負わされているのである。

Fairness, and more generally, responsible AI, has indeed become a pressing issue in recommender systems research that finds reflection in the recent research literature [Mehrotra et al. 2018a], keynote talks [Baeza-Yates 2020], new dedicated research outlets [Elish et al. 2021], and public debate.
公平性、そしてより一般的には責任あるAIは、確かにレコメンダーシステム研究における緊急の課題となっており、最近の研究文献［Mehrotra et al. 2018a］、基調講演［Baeza-Yates 2020］、新しい専用の研究アウトレット［Elish et al. 2021］、および公開討論に反映されていることが分かっている。
Metrics are being proposed to measure fairness, and algorithms and enhancements are being researched to avoid unfair treatment of groups [Yao and Huang 2017], minorities or individuals, as both providers and consumers of recommended choices [Patro et al. 2020].
公平性を測る指標が提案され、推奨される選択肢の提供者と消費者の両方として、グループ[Yao and Huang 2017]、マイノリティや個人の不当な扱いを避けるためのアルゴリズムや機能拡張が研究されている[Patro et al. 2020]。
A first realization with the onset of this new research area is the complexity of fairness as a concept and the difficulty of achieving universal solutions.
この新しい研究分野の開始とともに最初に気づいたことは、概念としての公正さの複雑さと普遍的な解決策の達成の難しさである。
Studies are unanimous in stressing the importance of bias awareness and understanding as a key step (and possibly a considerable part of the solution) to prevent or mitigate unfairness.
不公正を防止・緩和するための重要なステップ（そしておそらく解決策のかなりの部分）として、偏見に対する認識と理解の重要性を強調する研究は一致している。
An ample strand of reflection and research efforts can be expected to continue in the times to come.
このような考察と研究の努力は、今後も継続されることが期待される。

#### Offline / Online Misalignment in Evaluation. オフライン

As mentioned in Section 1.4.1, offline evaluation results are often weakly aligned with the outcomes of online A
1.4.1 節で述べたように、オフラインの評価結果は、しばしばオンラインの A
