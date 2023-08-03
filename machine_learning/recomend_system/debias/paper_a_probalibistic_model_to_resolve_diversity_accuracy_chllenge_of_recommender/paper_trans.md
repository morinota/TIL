## link リンク

https://elicit.org/search?q=Are+there+any+papers+that+discuss+deterministic+vs.+probabilistic+recommendation+models%3F&token=01H6WQAYZY4SKEKCCAETZQATBM&paper=d61732dbdbd4cddb6c02ebee5b257bbb805b28f9&column=title&s-pr=citations
https://elicit.org/search?q=Are+there+any+papers+that+discuss+deterministic+vs+probabilistic+recommendation+models%3F&token=01H6WQAYZY4SKEKCCAETZQATBM&paper=d61732dbd4cddb6c02ebee5b257bbb805b28f9&column=title&s-pr=citations

## title タイトル

A probabilistic model to resolve diversity–accuracy challenge of recommendation systems
推薦システムの多様性と精度の課題を解決する確率モデル

## Abstract 

Recommendation systems have wide-spread applications in both academia and industry.
レコメンデーション・システムは、学界と産業界の両方に広く応用されている。
Traditionally, performance of recommendation systems has been measured by their precision.
従来、推薦システムの性能はその精度で測定されてきた。
By introducing novelty and diversity as key qualities in recommender systems, recently increasing attention has been focused on this topic.
レコメンダーシステムにおける重要な資質として新規性と多様性が導入され、近年このトピックに注目が集まっている。
Precision and novelty of recommendation are not in the same direction, and practical systems should make a trade-off between these two quantities.
推薦の精度と新規性は同じ方向にはなく、実用的なシステムはこの2つの量の間でトレードオフを行うべきである。
Thus, it is an important feature of a recommender system to make it possible to adjust diversity and accuracy of the recommendations by tuning the model.
したがって、モデルをチューニングすることによって、推薦の多様性と精度を調整できるようにすることは、推薦システムの重要な機能である。
In this paper, we introduce a probabilistic structure to resolve the diversity–accuracy dilemma in recommender systems.
本稿では、推薦システムにおける多様性と精度のジレンマを解決するために、確率的構造を導入する。
We propose a hybrid model with adjustable level of diversity and precision such that one can perform this by tuning a single parameter.
我々は、多様性と精度のレベルを調整可能なハイブリッドモデルを提案する。
The proposed recommendation model consists of two models: one for maximization of the accuracy and the other one for specification of the recommendation list to tastes of users.
提案する推薦モデルは、精度を最大化するモデルと、ユーザの嗜好に合わせた推薦リストを指定するモデルの2つから構成される。
Our experiments on two real datasets show the functionality of the model in resolving accuracy–diversity dilemma and outperformance of the model over other classic models.
2つの実際のデータセットを用いた実験により、精度と多様性のジレンマを解決するモデルの機能性と、他の古典的モデルに対するモデルの優位性が示された。
The proposed method could be extensively applied to real commercial systems due to its low computational complexity and significant performance.
提案された方法は、計算の複雑さが少なく、性能が高いため、実際の商用システムに広く適用できる。

# 1. INTRODUCTION 1. はじめに

In many e-commerce systems, users confront millions of options which they may purchase.
多くのeコマース・システムでは、ユーザーは購入する可能性のある何百万もの選択肢に直面する。
Exploring such large item spaces is time consuming and is not manageable for most of users in many situations.
このような大きなアイテムスペースを探索するのは時間がかかり、多くの状況においてほとんどのユーザーにとって管理しにくい。
Due to this reason, recommender systems have become a core component for many e-commerce applications and attracted many researches in recent years [1][2][3].
このような理由から、レコメンダー・システムは多くの電子商取引アプリケーションの中核的な構成要素となっており、近年多くの研究が行われている[1][2][3]。
Although recommender systems work like an information retrieval system, there is no direct request for information in them.
レコメンダー・システムは情報検索システムのように機能するが、そこには情報の直接的な要求はない。
The major task of a recommender system is to use previous interactions recorded in the system in order to extract users' taste, and thus, provide a proper list of items to recommend.
レコメンダー・システムの主要なタスクは、システムに記録された過去のインタラクションを利用して、ユーザーの好みを抽出し、推奨するアイテムの適切なリストを提供することである。
Recommender systems can be categorized into three classes based on the type of information used for recommendation: content-based, collaborative filtering and hybrid methods.
推薦システムは、推薦に使われる情報の種類によって、コンテンツベース、協調フィルタリング、ハイブリッド方式の3つに分類される。
Contentbased recommenders work based on the content of the items and recommend items which have similar contents with those that a user has already purchased [4].
コンテンツベースのレコメンダーは、アイテムのコンテンツに基づいて動作し、ユーザーが既に購入したものと類似したコンテンツを持つアイテムを推薦する[4]。
Algorithms based on collaborative filtering make recommendations for any user by the help of collective preferences of other users [5].
協調フィルタリングに基づくアルゴリズムは、他のユーザーの集合的な嗜好の助けを借りて、任意のユーザーに推奨を行う[5]。
Hybrid methods use both the information available from previous user-item interactions and contents of the purchased items [1,6].
ハイブリッド手法は、過去のユーザーとアイテムのインタラクションから得られる情報と、購入したアイテムのコンテンツの両方を使用する[1,6]。
In many applications, content-based features are not easy to extract, and thus collaborative filtering approaches are the preferred ones.
多くのアプリケーションでは、コンテンツベースの特徴を抽出するのは容易ではないため、協調フィルタリングアプローチが好まれる。

Recommendation problem can be formulated as follows.
推薦問題は次のように定式化できる。
There are a set of users U, a set of items I and a set of possible ratings R from U to I.
ユーザーの集合U、アイテムの集合I、UからIへの可能な評価の集合Rがある。
Each user gives ratings on some items, which represents its utility value on the items.
各ユーザは、項目に対する効用値を表すいくつかの項目に評価を与える。
Since each user just experienced a small sector of the item space, the goal of a recommender system is to recommend a set of items for that user such that the user is likely to purchase them in near future and is satisfied by them.
各ユーザーはアイテム空間の小さな領域を経験しただけなので、レコメンダー・システムの目標は、そのユーザーが近い将来に購入する可能性が高く、満足するようなアイテム・セットをそのユーザーに推薦することである。
In some basic settings of the problem, the ratings have just values 0 or 1 that are extracted based on co-occurrence of users and items, i.e., if the user has purchased the item, the rating is 1, and 0 otherwise.
この問題のいくつかの基本的な設定では、評価は、ユーザーとアイテムの共起に基づいて抽出される値0または1を持つだけである。つまり、ユーザーがアイテムを購入した場合、評価は1となり、そうでない場合は0となる。
For example, users' click on items in a website can be considered as co-occurrence.
例えば、ユーザーがウェブサイト内の項目をクリックすることは、共起とみなすことができる。
In some other cases, users represent their feedback on items through explicit ratings they give.
また、明示的なレーティングによってアイテムに対するフィードバックを表現するケースもある。
Based on this framework, various recommendation algorithms have been introduced.
このフレームワークに基づいて、様々な推薦アルゴリズムが導入されている。
One can mention correlation-based algorithms such as user-based and item-based collaborative filtering [7][8][9], spectral analysis techniques [10] and probabilistic models such as latent semantic model [11], Bayesian networks and Markov chain models [12,13].
ユーザーベースやアイテムベースの協調フィルタリング[7][8][9]、スペクトル分析技術[10]、潜在意味モデル[11]、ベイジアンネットワーク、マルコフ連鎖モデル[12,13]などの確率論的モデル[11]などの相関ベースのアルゴリズムを挙げることができる。

Collaborative filtering algorithm and its variants are the most frequently used recommendation algorithms in both academia and industry [14][15][16].
協調フィルタリングアルゴリズムとその亜種は、学界と産業界の両方で最も頻繁に使用される推薦アルゴリズムである[14][15][16]。
Many of collaborative filtering approaches do not take into account the sequence by which the items have been purchased by the users.
協調フィルタリングアプローチの多くは、ユーザーがアイテムを購入した順序を考慮していない。
The way users purchase items often has a sequential manner.
ユーザーが商品を購入する方法は、多くの場合、順を追って行われる。
For example, when a user watches a movie directed by a particular person and likes it, it is likely that the same user watches other movies from the same director.
例えば、あるユーザーが特定の人物が監督した映画を見て気に入った場合、同じユーザーが同じ監督の他の映画も見る可能性が高い。
Markov chain (MC) based recommender is class of collaborative filtering based recommenders, which utilizes these sequential dependencies in their recommendations [16][17][18][19].
マルコフ連鎖(MC)ベースのレコメンダーは協調フィルタリングベースのレコメンダーのクラスであり、レコメンデーションにおいてこれらのシーケンシャルな依存関係を利用する[16][17][18][19]。
In MC models, the recommendation is modeled as a sequential prediction problem, and the goal is to predict items that a user will purchase in near future based on the user's last actions.
MCモデルでは、推薦を逐次予測問題としてモデル化し、ユーザーの直近の行動に基づいて、ユーザーが近い将来に購入するアイテムを予測することを目標としている。
To this end, first, a proper state space is defined and transition between states is estimated.
そのためにまず、適切な状態空間を定義し、状態間の遷移を推定する。
Then, the recommendation for a target user is provided by applying the user's last actions on transition function.
そして、ユーザーの最後の行動を遷移関数に適用することで、対象ユーザーへの推薦を行う。
MC models consider the recommendation problem as a prediction problem and their task is to maximize accuracy of recommendation lists.
MCモデルは推薦問題を予測問題として考え、そのタスクは推薦リストの精度を最大化することである。
However, systems which provide accurate recommendations do not necessarily satisfy users [20][21][22].
しかし、正確なレコメンデーションを提供するシステムが必ずしもユーザーを満足させるとは限らない[20][21][22]。

A practical recommender system should not only have a good accuracy but also provide proper novelty and diversity of items for the users [23,24].
実用的な推薦システムは、精度が高いだけでなく、ユーザーに適切な新規性とアイテムの多様性を提供しなければならない[23,24]。
Novelty and diversity of recommendations describes the ability of the recommender models to suggest items which the users would not discover them by themselves [22].
レコメンデーションの新規性と多様性は、ユーザーが自分では発見しないようなアイテムを提案するレコメンダーモデルの能力を表す[22]。
In contrast to content-based algorithms which almost do not suffer from low diversity problem, most of the algorithms based on crowd preferences are biased towards popular items.
多様性の低い問題にほとんど悩まされないコンテンツベースのアルゴリズムとは対照的に、群衆の嗜好に基づくアルゴリズムのほとんどは、人気のあるアイテムに偏っている。
This focus of recommendations on a small set of items happens since the classic recommendation models are designed to maximize precision of recommendations.
古典的な推薦モデルは、推薦の精度を最大化するように設計されているため、このような小さなアイテムセットへの推薦の集中が起こる。
Recommendation of popular items has lower risk in terms of precision [22].
人気アイテムの推奨は、精度の点でリスクが低い[22]。
On the other hand, regarding the diversity problem, we are interested to give same chance for all items to appear in the recommendation list.
一方、多様性の問題については、すべてのアイテムが推薦リストに表示されるチャンスを同じにすることに関心がある。
Thus, it could be argued that maximizing accuracy and diversity of the recommendation list are not in the same direction.
このように、精度の最大化と推薦リストの多様性は同じ方向ではないと言える。
Higher accuracy can be obtained by recommending some popular items; whereas personalized and diverse recommendations can be achieved by covering homogenously the whole items set without any focus on items with specific popularity interval.
一方、パーソナライズされた多様なレコメンデーションは、特定の人気区間を持つアイテムに焦点を当てることなく、アイテムセット全体を均質にカバーすることで達成できる。
Thus, there should be a tradeoff between accuracy and diversity in recommendations [24].
したがって、推奨の精度と多様性はトレードオフの関係にあるはずである[24]。
Obviously, different frameworks may expect different levels of accuracy and diversity from their recommender systems.
明らかに、異なるフレームワークは、推薦システムに異なるレベルの精度と多様性を期待するかもしれない。
In other words, importance of accuracy and diversity may change in each framework.
言い換えれば、正確さと多様性の重要性は、それぞれのフレームワークで変わる可能性がある。
Therefore, capability of a recommender model to adjust diversity and accuracy level of recommendations is an important feature of a recommender system.
したがって、推薦モデルが推薦の多様性と精度レベルを調整する能力は、推薦システムの重要な特徴である。

Given that MC-based recommender systems are model-based algorithms with proper functionality and low computational complexity [16,19], in this paper, we introduce a novel probabilistic model that overcomes some drawbacks of classic MC-based methods.
MCベースの推薦システムは、適切な機能と低い計算複雑性を持つモデルベースのアルゴリズムであることを踏まえ[16,19]、本稿では、古典的なMCベースの手法のいくつかの欠点を克服する新しい確率モデルを紹介する。
Furthermore, we propose a structure to approach the dilemma of accuracy-diversity by introducing a hybrid model, which can balance two recommendation algorithms: One specialized for high accuracy and the other one for high novelty.
さらに、2つの推薦アルゴリズムをバランスさせることができるハイブリッドモデルを導入することで、精度と多様性のジレンマにアプローチする構造を提案する： 1つは高い精度に特化し、もう1つは高い新規性に特化する。
The individual algorithms are not optimal regarding to their diversity.
個々のアルゴリズムは、その多様性に関して最適ではない。
By combination these two basic algorithms, we build a recommender system with not only good accuracy but also high diversity.
この2つの基本アルゴリズムを組み合わせることで、精度が高いだけでなく、多様性の高いレコメンダーシステムを構築する。
The structure we introduce to resolve diversity-accuracy dilemma can be applied on all MC-based recommenders without increasing computational complexity of the models.
多様性と精度のジレンマを解決するために導入した構造は、モデルの計算量を増やすことなく、すべてのMCベースの推薦者に適用することができる。
Our results on two real datasets (Netflix and Movielens) show the effectiveness of the proposed algorithm in handling the accuracy-diversity challenge of the recommendation list as well as its superior performance over some classic algorithms.
2つの実際のデータセット（NetflixとMovielens）を用いた我々の結果は、推薦リストの精度と多様性の課題に対する提案アルゴリズムの有効性と、いくつかの古典的アルゴリズムに対する優れた性能を示している。

# 2. Related works 2. 関連作品

Among different classes of collaborative filtering recommender systems, in this paper, we focus on MC-based models.
協調フィルタリング推薦システムの様々なクラスの中で、本稿ではMCベースのモデルに注目する。
Such models have many applications in analyzing users' behavior [25][26][27][28].
このようなモデルは、ユーザーの行動分析に多くの応用がある[25][26][27][28]。
A number of works have applied Markov models in the context of recommender systems [17,19,[29][30][31].
リコメンダーシステムの文脈でマルコフモデルを適用した研究は数多くある[17,19,[29][30][31]。
For example, Shani et.
例えば、Shani et.
al.
アル。
used Markov decision processes (MDP) for modeling the recommendation problem, by defining utility function for item set as a sequential optimization problem [13].
はマルコフ決定過程(MDP)を用いて推薦問題をモデル化し、項目集合に対する効用関数を逐次最適化問題として定義している[13]。
Garcin et.
ガルシンら。
al.
アル。
introduced a recommendation model based on evolving context trees, where context trees can be considered as variable order Markov models.
は、進化するコンテキストツリーに基づく推薦モデルを紹介した。コンテキストツリーは、可変オーダーのマルコフモデルとして考えることができる。

Although MC and MDP have been used in many real-world applications [17,19,[29][30][31], there are some restrictions to employ them for recommendation.
MCやMDPは多くの実世界アプリケーションで利用されているが[17,19,[29][30][31]、推薦に採用するにはいくつかの制約がある。
These models do not consider users' ratings on items.
これらのモデルでは、アイテムに対するユーザーの評価は考慮されていない。
They do the recommendations based on the sequence of the items purchased by the user.
彼らは、ユーザーが購入したアイテムの順序に基づいて推薦を行う。
The value of the ratings of the users is an important information resource which can be utilized to provide better recommendations.
ユーザーの評価値は、より良いレコメンデーションを提供するために活用できる重要な情報資源である。
In this work, we utilize this information resource by defining a new state space.
この研究では、新しい状態空間を定義することで、この情報資源を活用する。
The diversity and accuracy dilemma has not been previously studied in MC-based models.
多様性と精度のジレンマは、MCベースのモデルではこれまで研究されてこなかった。

Novelty and diversity in recommender systems recently received much attention [21,[32][33][34][35].
推薦システムにおける新規性と多様性は最近注目されている[21,[32][33][34][35]。
It has been shown that performance of the recommender systems should be evaluated in terms of not only accuracy but also diversity and novelty [22,36,37].
レコメンダー・システムの性能は、正確さだけでなく、多様性や新規性の観点からも評価されるべきであることが示されている[22,36,37]。
Concerning this issue, different strategies have been introduced for diversification of recommendation lists [6,38].
この問題に関しては、推薦リストの多様化のために様々な戦略が導入されている[6,38]。
Typically, these models addressed the problem based on contextual or semantic information resources; for example, item-item similarities and user generated tags can be used to answer this problem [38,39].
一般的に、これらのモデルは文脈的または意味的な情報資源に基づいて問題に取り組んでいる。例えば、項目と項目の類似性やユーザーが生成したタグは、この問題に答えるために使用することができる[38,39]。
However, these models cannot be tuned to provide a desired level of diversity and accuracy and some of them also rely on more information resources.
しかし、これらのモデルは、望ましいレベルの多様性と精度を提供するように調整することはできず、また、より多くの情報資源に依存しているものもある。
Recommendation algorithms may be used in different frameworks with different requirements.
レコメンデーション・アルゴリズムは、異なる要件を持つ異なるフレームワークで使用される可能性がある。
Flexible level of diversity and accuracy for a recommendation algorithm is an important capability for recommender systems.
推薦アルゴリズムの多様性と精度の柔軟なレベルは、推薦システムにとって重要な能力である。
Zhou et.
Zhou et.
al.
アル。
[24] proposed a model to address the challenge of diversity and accuracy dilemma which can be tuned to obtain arbitrary level of diversity and accuracy.
[24]は、多様性と精度のジレンマに対処するために、任意のレベルの多様性と精度を得るように調整できるモデルを提案した。
Their recommendation process works based on the idea of heat diffusion across the bipartite users-items network.
彼らの推薦プロセスは、二分割されたユーザーとアイテムのネットワークを横切る熱拡散のアイデアに基づいて機能する。
Although the model does not rely on any contextual or semantic information resources, their baseline model (HeatS) is not a widely used method.
このモデルは文脈や意味的な情報資源に依存していないが、彼らのベースラインモデル（HeatS）は広く使われている手法ではない。
The model relies on a transition matrix between users and items.
このモデルは、ユーザーとアイテムの間の遷移行列に依存している。
Real-world systems may contain millions of users which restricts scalability of the model for commercial applications.
実世界のシステムには数百万人のユーザーが含まれる可能性があり、商用アプリケーションではモデルのスケーラビリティが制限される。
Apparently, the model proposed in [24] cannot be applied on other recommendation algorithms; it is indeed specific to the "HeatS" algorithm.
どうやら、[24]で提案されたモデルは、他の推薦アルゴリズムには適用できないようだ。
However, our proposed models can provide a flexible level of diversity and precision for a widely recommendation algorithm.
しかし、我々の提案するモデルは、広く推薦アルゴリズムに柔軟なレベルの多様性と精度を提供することができる。
In this work, our baseline model is a probabilistic model based on Markov chains, and we introduce a structure that resolves the accuracy-diversity dilemma in this class of recommendations.
本研究では、マルコフ連鎖に基づく確率モデルをベースラインとし、このクラスの推薦における精度と多様性のジレンマを解決する構造を導入する。
Markov-based recommenders is a class of well-known and widely used techniques in real-world applications [16,18,19,40].
マルコフベースの推薦者は、よく知られたクラスであり、実世界のアプリケーションで広く使われている技術である[16,18,19,40]。
The probabilistic structure introduced in this paper is flexible and can be applied on any Markov-based recommender.
本稿で導入した確率的構造は柔軟であり、どのようなマルコフベースのレコメンダーにも適用できる。

# 3. Methods 3. 方法

In this section, we give the details of the proposed recommender system that is based on Markov model.
本節では、マルコフモデルに基づく推薦システムの詳細を述べる。
The performance of this novel model is compared with three traditional recommender systems that have found stable application in commercial recommendation systems: memory-based collaborative filtering (CF), popularity-based recommendation algorithms and a classic Markov based recommender.
この新しいモデルの性能を、商業的推薦システムにおいて安定した応用を見出した3つの伝統的推薦システム、すなわち記憶ベースの協調フィルタリング（CF）、人気ベースの推薦アルゴリズム、および古典的マルコフベースの推薦システムと比較する。
Memory-based CF is one of the most successful techniques in recommender systems, which has been used in many commercial systems since introduction.
メモリベースCFはレコメンダーシステムにおいて最も成功した技術の一つであり、導入以来多くの商用システムで使用されている。
This is mainly because of its simple implementation and stable inference.
これは主に、シンプルな実装と安定した推論のためである。

## 3.1 Collaborative Filtering 3.1 協調フィルタリング

In recommendation systems based on memory-based CF, in order to recommend a list of potential items to a target user, first, the model produces predictions for ratings of the target user on candidate items, and then, the items which have been predicted to receive high ratings from the user are recommender.
記憶ベースCFに基づく推薦システムでは、まず、対象ユーザに対して候補アイテムのリストを推薦するために、候補アイテムに対する対象ユーザの評価予測をモデルが作成し、次に、ユーザから高い評価を受けると予測されたアイテムを推薦する。
Memory-based CF is often implemented in two forms: user based and item based.
メモリベースのCFは、ユーザーベースとアイテムベースの2つの形態で実装されることが多い。
User-based CF works by, first, computing the similarities between the users based on pattern of their ratings to the items, and then, using these similarity values to predict the ratings on a target item.
ユーザーベースのCFは、まず、アイテムに対する評価のパターンに基づいてユーザー間の類似性を計算し、次に、これらの類似性値を使用してターゲットアイテムの評価を予測することによって機能する。
Item-based CF considers similarities between the items.
項目ベースのCFは、項目間の類似性を考慮する。
In this manuscript, we take into account both these models.
この原稿では、これら両方のモデルを考慮に入れている。
In order to compute similarities between the users, one can use metrics such as Pearson correlation coefficient or cosine similarity index.
ユーザー間の類似性を計算するために、ピアソン相関係数やコサイン類似度指数などの指標を使用することができる。
Using Pearson correlation coefficient, the similarity between users i and j can be obtained as:
ピアソン相関係数を用いると、ユーザーiとjの間の類似度は次のように求められる：

where R i,h indicates the vote of user i on item h and R i is average ratings made by user i.
ここで、R i,hはアイテムhに対するユーザーiの投票を示し、R iはユーザーiによる平均評価である。
n is the number of items rated by both users i and j.
nは、ユーザーiとjの両方によって評価されたアイテムの数である。
In the same way, similarities between items can be extracted based on the ratings of the users on items [8].
同様に、アイテムに対するユーザーの評価に基づいて、アイテム間の類似性を抽出することができる[8]。

By extracting similarities between users, predicted value for the rate of user u on item o can be obtained as:
ユーザー間の類似性を抽出することで、アイテムoに対するユーザーuの割合の予測値は次のように求められる：

where S pearson is the Pearson similarity of user u with h, R h,o is the rating item o received from user h and m indicates the number of ratings item o received from different users.
ここで、S pearsonはユーザーuとhのピアソン類似度、R h,oはユーザーhから受け取った評価項目o、mは異なるユーザーから受け取った評価項目oの数を示す。
In item-based CF after extraction of similarities between the items, P(u,o) can be obtained as:
項目ベースのCFでは、項目間の類似性を抽出した後、P(u,o)は次のように求められる：

where Sim(o,i) is the similarity of the item o with item i and n is the number of ratings user u gave to items.
ここで、Sim(o,i)はアイテムoとアイテムiの類似度、nはユーザーuがアイテムに与えた評価の数である。

## 3.2 Markov models 3.2 マルコフモデル

Unlike traditional CF algorithms, which only use recently purchased items for recommendation, methods based on Markov chain not only use that information but also take into account the information about the order in which users purchase items.
マルコフ連鎖に基づく方法は、最近購入されたアイテムのみを推薦に使用する従来のCFアルゴリズムとは異なり、その情報を使用するだけでなく、ユーザーがアイテムを購入する順序に関する情報も考慮に入れる。
Users often purchase items in a sequential manner such that a particular item is purchased first, and then, another item is purchased and so on.
ユーザーは、ある商品を最初に購入し、次に別の商品を購入するというように、商品を順次購入することが多い。
Markov models use this information and give different weights for the items based on the order in which they have been purchased by users.
マルコフモデルはこの情報を利用し、ユーザーが購入した順番に基づいてアイテムに異なる重みを与える。

In order to employ Markov chain for recommendation, appropriate state space and transition function should be first defined.
マルコフ連鎖を推薦に用いるには、まず適切な状態空間と遷移関数を定義する必要がある。
State of each user can be represented by the set of the items which have already been purchased (or rated) by the user.
各ユーザーの状態は、そのユーザーが既に購入した（または評価した）アイテムの集合で表すことができる。
It is well-known that in order to have an acceptable performance for a recommender system, the constructed connectivity matrices should be sparse [5].
推薦システムとして許容できる性能を持つためには、構築される接続性行列はスパースであるべきであることはよく知られている[5]。
Different users may purchase different number of items and due to the sparsity problem, only a sequence of at most m items is considered as a particular user's state [13].
異なるユーザーは異なる数のアイテムを購入する可能性があり、スパース性の問題により、最大m個のアイテムのシーケンスのみが特定のユーザーの状態として考慮される[13]。
Let us consider the vector S u = <I m , I m-1 ,...,I 1 > as state of user u, which denotes the user's last m purchased items in a sequential manner.
ここで、ユーザuの状態としてベクトルS u = <I m , I m-1 ,...,I 1>を考える。
As the state space is defined, the transition function should be estimated.
状態空間が定義されると、遷移関数を推定する必要がある。
The transition function describes the probability that a target user that has purchased items I m , I m-1 ,...,I 1 will select item I m+1 in the next step.
遷移関数は、アイテムI m、I m-1、...、I 1を購入したターゲットユーザが、次のステップでアイテムI m+1を選択する確率を記述する。
According to the train dataset which consists of different users' ratings on the item and based on maximum likelihood estimation, the transition function between two states can be estimated as:
項目に対する異なるユーザーの評価からなる訓練データセットによれば、最尤推定に基づき、2つの状態間の遷移関数は以下のように推定できる：

where N(<I m ,I m-1 ,…,I 1 >) indicates the number of users visiting the state <I m ,I m-1 ,…,I 1 > in their rating sequences in training dataset.
ここで、N(<I m ,I m-1 ,...,I 1 >)は、訓練データセットの評価シーケンスにおいて、状態<I m ,I m-1 ,...,I 1 >を訪れたユーザの数を示す。

## 3.3 State automata-based recommender system 3.3 状態オートマトンに基づく推薦システム

The recommendation method proposed in this paper, similar to the one based on Markov chain, uses the sequential manner of users' ratings.
本論文で提案する推薦方法は、マルコフ連鎖に基づく推薦方法と同様に、ユーザーの評価の逐次的な方法を用いる。
However, in our proposed method, we define the states and the prediction model in a way different from previous Markov chain models.
しかし、我々の提案する方法では、従来のマルコフ連鎖モデルとは異なる方法で状態と予測モデルを定義する。
Furthermore, we introduce two prediction models to solve accuracy and discovery dilemma in recommender systems.
さらに、推薦システムにおける精度と発見のジレンマを解決するために、2つの予測モデルを紹介する。
It is well know that accuracy and diversity of the prediction list are not in the same direction; often, when accuracy improves, the diversity of the recommendation list worsens and vice versa [22].
予測リストの精度と多様性は同じ方向には向かないことはよく知られており、精度が向上すると推奨リストの多様性は悪化し、その逆もよくある[22]。
To the best of our knowledge, there is no Markov-based recommendation algorithm that gives the full power to control the accuracy and diversity of the recommendation list.
我々の知る限り、マルコフベースの推薦アルゴリズムで、推薦リストの精度と多様性をコントロールできるものは存在しない。
Here, we introduce a hybrid model that has a single parameter controlling desired levels of accuracy and diversity of the system.
ここでは、システムの精度と多様性の望ましいレベルを制御する単一のパラメータを持つハイブリッドモデルを紹介する。
We separate the proposed method into two parts.
我々は提案する方法を2つの部分に分けている。
In the first part of the algorithm, two primary graphs are extracted from training dataset.
アルゴリズムの最初の部分では、訓練データセットから2つの主要なグラフが抽出される。
In the second part, the recommendation is performed based on two separate prediction models.
第2部では、2つの予測モデルに基づいて推薦が行われる。
In the next sections, we articulate each part in details.
次のセクションでは、各パートの詳細を説明する。

### 3.3.1 Extraction of aggregated transition graph and aggregated co-occurrence graph 3.3.1 集約された遷移グラフと集約された共起グラフの抽出

By considering each item as a state, users' sequential ratings can be modeled as transition between different states.
各アイテムを1つの状態とみなすことで、ユーザーの逐次的な評価を異なる状態間の遷移としてモデル化することができる。
However, in order to include the value of ratings in the transition probabilities, we model each item by two states: positive (like) state and negative (dislike) state which we indicate in the rest of the paper by L-state and D-state, respectively.
ただし、遷移確率に評価の値を含めるために、各項目を2つの状態、つまりポジティブ（好き）な状態とネガティブ（嫌い）な状態でモデル化する。
L-state indicates that the target user rates the item positively, whereas negative ratings are indicated by D-state.
L状態は、ターゲットユーザーがそのアイテムを肯定的に評価していることを示し、否定的な評価はD状態で示される。
Let us denote L-states and D-states of item i by s i,L and s i,D , respectively.
アイテムiのL状態をs i,L、D状態をs i,Dとする。
In other words, we model the item space in 2I states and users' ratings as transitions between these states where I is number of items.
つまり、アイテム空間を2Iの状態でモデル化し、ユーザーの評価をこれらの状態間の遷移としてモデル化する。
Each edge (s i,L , s j,D ) in this transition graph represents consecutive ratings.
この遷移グラフの各辺（s i,L , s j,D ）は、連続した評価を表す。
For example, ratings of a specific user in table 1 can be transformed to state transition model shown in figure 1 .
例えば、表1の特定ユーザーの評価は、図1の状態遷移モデルに変換することができる。

Figure 1 : Rating history of a specific user (Table ) and the state transition model of the same user's ratings (Figure) .
図1 : 特定のユーザーのレーティング履歴（表）と、同じユーザーのレーティングの状態遷移モデル（図）。

In order to aggregate the information about users' behavior and their sequential ratings, we use statistics extracted from the transitions in the state space.
ユーザーの行動と逐次的な評価に関する情報を集約するために、状態空間の遷移から抽出した統計量を使用する。
In this way, we introduce an aggregated transition (AT) graph, which is a state space with 2I states.
このようにして、2I個の状態を持つ状態空間である集約遷移グラフ（AT graph）を導入する。
In this graph, the weight of connection between two states s i,L and s j,D is defined as the number of users who have the edge (s i,L , s j,D ) in their transitions.
このグラフにおいて、2つの状態s i,Lとs j,D間の接続の重みは、その遷移にエッジ(s i,L , s j,D )を持つユーザーの数として定義される。
Indeed, we count the number of users who visit item j after item i and have similar tastes on these two items (i.e., all liked item i and dislikes item j).
実際に、アイテムiの後にアイテムjを訪問し、これら2つのアイテムに関する嗜好が似ている（すなわち、全員がアイテムiを好きで、アイテムjを嫌いである）ユーザーの数をカウントする。

Essentially, in order to implement our proposed model, the datasets should have a time tag for all ratings.
基本的に、我々の提案するモデルを実装するためには、データセットにすべての評価の時間タグが必要である。
For datasets without such labels, we define aggregated cooccurrence (AC) graph.
このようなラベルを持たないデータセットについては、集約された共起グラフ（AC）を定義する。
In this work, we define weight of the connection from state s i,L to state s j,D as the number of users who have rated both items i and j and given similar ratings to them regardless of rating sequence.
この研究では、状態s i,Lから状態s j,Dへの接続の重みを、評価順序に関係なく、アイテムiとjの両方を評価し、それらに同様の評価を与えたユーザーの数と定義する。
Although in this way we lose some information about the rating sequence, it makes the algorithm a general one and makes it possible to compare with other algorithms that do not consider the rating sequences (e.g., user-based CF).
こうすることで、評価シーケンスに関する情報が失われるものの、アルゴリズムが一般的なものになり、評価シーケンスを考慮しない他のアルゴリズム（ユーザーベースのCFなど）との比較が可能になる。
AC graph suffers less than AT graph in terms of sparsity problems.
ACグラフはATグラフよりもスパース性の問題が少ない。
The sum of the edge weights in AT graph is N, where N is number of ratings in training dataset, whereas AC graph, in average, has the sum of edge weight as ̅ , where U is number of users in training dataset and ̅ is the average number of ratings for each user.
ATグラフのエッジ重みの合計はNであり、Nは訓練データセットの評価数である。一方、ACグラフの平均的なエッジ重みの合計は̅であり、Uは訓練データセットのユーザー数、̅は各ユーザーの平均評価数である。
By considering ̅ as N/U, the sum of edge weight becomes N 2 /U, and thus, the sparsity is much less in AC graph as compared to AT graph.
をN/Uと考えると、エッジの重みの和はN 2 /Uとなり、ACグラフではATグラフに比べてスパース性が非常に小さくなる。

### 3.3.2 Recommendation 3.3.2 推奨

Based on the aggregated transition graph introduced above, in this section, we introduce two probabilistic recommendation models.
上で紹介した集約された遷移グラフに基づき、このセクションでは2つの確率的推薦モデルを紹介する。
One of the models aims at providing a recommendation list with high levels of precisions, while the other model tries to recommend items that have the best fit to the target user's taste.
一方のモデルは、精度の高い推薦リストを提供することを目的とし、もう一方のモデルは、対象ユーザーの嗜好に最も適合するアイテムを推薦しようとするものである。
In order to perform the recommendation based on these probabilistic models, we first extract the state of the target user.
これらの確率モデルに基づく推薦を行うために、まず対象ユーザーの状態を抽出する。
We define state of each user as its previous ratings on the items.
各ユーザーの状態を、アイテムに対する過去の評価と定義する。
As mentioned above, users' ratings can be considered as nodes in AT or AC graphs.
上述したように、ユーザーの評価はATグラフやACグラフのノードとみなすことができる。
Thus, the state of the users is a vector of nodes' identification (ID) numbers.
したがって、ユーザーの状態は、ノードの識別（ID）番号のベクトルである。
In other words, the state of users consists of some sub-sates where each node in AT or AC graphs indicates a sub-state.
言い換えれば、ユーザーの状態は、ATまたはACグラフの各ノードがサブ状態を示すいくつかのサブ状態から構成される。
For example, state of user with ratings as indicated in Figure 1 can be defined as <23D, 532L, 43L, 389D>.
例えば、図1に示すような評価を受けたユーザーの状態は、＜23D, 532L, 43L, 389D＞と定義できる。
Unlike traditional Markov models, we do not consider sequence of ratings in the vector of users' state.
従来のマルコフモデルとは異なり、ユーザーの状態を表すベクトルにおいて、評価の順序は考慮しない。
The definition we have considered for the state of users has high flexibility.
私たちがユーザーの状態について考えた定義は、高い柔軟性を持っている。
Using this method, it is possible to filter out some certain nodes with special characteristics in defining the state for a specific user.
この方法を使用すると、特定のユーザーの状態を定義する際に、特別な特性を持つ特定のノードをフィルタリングすることができる。
It is also possible to set the state of a user as weighted vectors of sub-states.
また、ユーザーの状態をサブ状態の重み付きベクトルとして設定することも可能だ。
For example, the items purchased recently might be more informative about taste of the users than those purchased previously; our definition allows intensifying the weights of nodes that belong to recently purchased items.
例えば、最近購入されたアイテムは、以前に購入されたアイテムよりも、ユーザーの嗜好についてより多くの情報を持っているかもしれない。我々の定義では、最近購入されたアイテムに属するノードの重みを強めることができる。

Recommendation based on precision maximization
精度最大化に基づく推薦

In traditional prediction models based on Markov chain, the purpose is to recommend items that are likely to be purchased in near future by the target user.
マルコフ連鎖に基づく従来の予測モデルでは、対象ユーザーが近い将来に購入する可能性の高いアイテムを推薦することが目的であった。
Here, we introduce a similar method that not only predicts the items which the user is likely to purchase them in future but also predicts the items that the user will like them.
ここでは、ユーザが将来購入しそうな商品を予測するだけでなく、ユーザが気に入りそうな商品を予測する同様の手法を紹介する。
The classic Markov chain models take into account only information about users' purchased items, but our model also considers the value of ratings.
古典的なマルコフ連鎖モデルは、ユーザーが購入したアイテムに関する情報のみを考慮するが、我々のモデルは評価の価値も考慮する。
This is performed with the help of separating each item into two distinct states.
これは、各アイテムを2つの異なる状態に分離する助けを借りて実行される。
In order to provide the recommendation list, we first produce probabilities about users' interest on each item, and then, we recommend items with the highest probability values.
レコメンデーションリストを提供するために、まず、各アイテムに対するユーザーの興味についての確率を生成し、次に、最も高い確率値のアイテムをレコメンデーションする。
The probability of the interest of user u on item i, P(I i |S u ), is obtained as:
ユーザーuがアイテムiに興味を持つ確率P(I i |S u )は次のように求められる：

where S u is the state of the user u, P(s i,L |S u ) is the probability of transition from the state of user u to L-state of item i and P(s i,D |S u ) is the probability of transition to D-state of the item i.
S u ) is the probability of transition from the state of user u to L-state of item i and P(s i,D |S u ) is the probability of transition to D-state of the item i.
According to this equation, recommendation score for item i is the probability that user u likes this item minus the probability that it dislikes the item.
この式によれば、アイテムiの推薦スコアは、ユーザーuがこのアイテムを好きである確率から、そのアイテムを嫌いである確率を引いたものである。
Indeed, the purpose of this model is to recommend items with the highest predicted value of popularity and the lowest predicted value of being uninterested.
実際、このモデルの目的は、人気の予測値が最も高く、興味のない予測値が最も低いアイテムを推薦することである。
The probability of the interest of user u in item i can be obtained as:
ユーザーuがアイテムiに興味を持つ確率は次のように求められる：

where m denotes the size of the state vector for user u and P(S u (k)) indicates the weight of sub-state k.
ここで、mはユーザーuの状態ベクトルのサイズを示し、P（S u（k））はサブ状態kの重みを示す。
P(S u (k)) is a tunable parameter that can be optimized to have good performance.
P(S u (k))は調整可能なパラメータであり、良好なパフォーマンスを得るために最適化することができる。
It this work, we did not aim at optimizing this parameter and set the value of P(S u (k)) for all sub-states equal to 1/m.
本研究では、このパラメーターの最適化を目的とせず、すべてのサブ状態に対するP(S u (k))の値を1/mに等しく設定した。
P(s i,L |S u (k)) is the probability of transition from sub-state k of user u to s i,L .
P(s i,L |S u (k))は、ユーザーuのサブ状態kからs i,L に遷移する確率である。
This transition probability can be extracted using maximum likelihood estimation method.
この遷移確率は、最尤推定法を用いて抽出することができる。
Based on the maximum likelihood estimation, the transition probability between node i and j is the weight of the edge (i,j) in AT or AC graphs divided by out-degree of node i.
最尤推定に基づくと、ノードiとjの間の遷移確率は、ATグラフまたはACグラフのエッジ(i,j)の重みをノードiのアウトディグリーで割ったものになる。
P(s i,D |S u (k)) can also be obtained in the same way.
P(s i,D |S u (k))も同様に求めることができる。
Indeed, equation ( 6) indicates the probability that user u will like item i (i.e., will transit to the sub-state s i,L in the next step), if user u has visited a vector of sub-states, S u .
実際、式( 6)は、ユーザーuがサブ状態のベクトルS uを訪問した場合、ユーザーuがアイテムiを気に入る（つまり、次のステップでサブ状態s i,Lに遷移する）確率を示している。
To find the transition probability of user u to the sub-state s i,L , we first obtain the probability of transition (dependency) from sub-states visited by user u to s i,L , and then aggregate the obtained values in a weighted manner.
ユーザuのサブ状態s i,Lへの遷移確率を求めるには、まず、ユーザuが訪問したサブ状態からs i,Lへの遷移確率（依存関係）を求め、得られた値を重み付けして集計する。
We obtain the probability of transition (or dependency) between the sub-states based on the users' behavior in the training dataset.
訓練データセットにおけるユーザーの行動に基づいて、サブ状態間の遷移（または依存）確率を求める。
The weight of each sub-state indicates the importance of the sub-state in describing the behavior of the target user.
各サブステートの重みは、ターゲットユーザーの行動を記述する上でのサブステートの重要性を示す。
For example, in a new recommendation framework, we may define the weights of sub-states (i.e., news items visited by the target user) based on the time the user spent on the news.
例えば、新しい推薦フレームワークでは、ユーザーがニュースに費やした時間に基づいて、サブ状態（つまり、ターゲットユーザーが訪問したニュース項目）の重みを定義することができる。
As the user spent more time on a news item, it means that the item better describes the user's interests.
ユーザーがあるニュース項目に費やした時間が長いほど、その項目がユーザーの興味をよりよく表していることを意味する。
However, in this paper, we do not consider this issue and set the weights of sub-state equal to 1/m.
しかし、本稿ではこの問題を考慮せず、サブステートの重みを1/mに等しく設定する。

In order to provide the recommendation list, we first, compute the above probabilities for all candidate items and then recommend top-L items with the highest predicted values, where L is the basket size of the recommendation list.
推薦リストを提供するために、まず、すべての候補項目について上記の確率を計算し、次に、最も高い予測値を持つ上位L個の項目を推薦する。
Although this prediction model provides a list with good precision, it often has a tendency to recommend high-degree and popular items.
この予測モデルは精度の高いリストを提供するが、度数の高いもの、人気のあるものを推奨する傾向がしばしば見られる。
This makes the model suffer from novelty and diversity problems, i.e., the recommendation list does not often provide diverse and novel items to the users.
つまり、レコメンデーションリストが多様で新しいアイテムをユーザーに提供することはあまりない。
Let us denote this model as PM model.
このモデルをPMモデルと呼ぼう。

In order to show that PM model is biased toward recommending high-degree items, we model each item with one state and extract the item's transition function regardless of the rating values.
PMモデルが高次のアイテムを推奨する方向に偏っていることを示すために、各アイテムを1つの状態でモデル化し、評価値に関係なくアイテムの遷移関数を抽出する。
Like most of real datasets, let us consider the item space consists of items with different popularities (e.g., in-degrees).
実際のデータセットの多くと同様に、アイテム空間は異なる人気度（例えば、度数）を持つアイテムで構成されていると考えよう。
If we obtain the expected value of the target user's transition to different items, it is easy to show that the items with higher popularity would gain higher expected value and the items' probability to be recommended would be related to their popularity.
異なるアイテムに対するターゲットユーザーの遷移の期待値を求めると、人気の高いアイテムほど期待値が高くなり、推奨される確率はその人気度と関係していることが容易にわかる。
Thus, in general, PM model is often biased to select items with low novelty (high degree).
したがって、一般的に、PMモデルは新規性の低い（程度の高い）項目を選択するように偏りがちである。
Next, we introduce another model, which takes into account the novelty and diversity of the recommendation list.
次に、推薦リストの新規性と多様性を考慮した別のモデルを紹介する。

Recommendation based on specification maximization
スペック最大化に基づく推薦

The model we introduce in this section tries to recommend items that are specific to the target user.
このセクションで紹介するモデルは、ターゲットユーザーに特化したアイテムを推薦しようとするものである。
This model extracts the recommendation list in a different way than PM model and tries to complement it.
このモデルは、PMモデルとは異なる方法で推薦リストを抽出し、それを補完しようとするものである。
Let us denote this model as specification maximizer (SM) model.
このモデルをスペック・マキシマイザー（SM）モデルと呼ぼう。
The goal of SM model is to find a list of items that is specific to the target user with the hope that maximum user satisfaction is obtained.
SMモデルの目標は、ユーザーの満足度が最大になるように、ターゲットユーザーに特化したアイテムリストを見つけることである。
SM model, first, extracts specification probability for all candidate items with respect to a target user and then recommends items with the highest probability values.
SMモデルは、まず、ターゲットユーザーに対する全候補アイテムの仕様確率を抽出し、最も高い確率値のアイテムを推薦する。
The probability of specification can be obtained as:
仕様の確率は次のように求められる：

where P(S u (k)|s i,L ) is the probability of conditional transition from S u (k) to s i,L .
ここで、P(S u (k)|s i,L ) は、S u (k) から s i,L への条件付き移行の確率である。
Supposing that user u has been visited s i,L , P(S u (k)|s i,L ) indicates that in which probability the previous sub-state visited by u is S u (k).
ユーザuがs i,Lを訪問したと仮定すると、P(S u (k)|s i,L )は、どの確率でuが前に訪問したサブ状態がS u (k)であるかを示す。
According to this equation, when an item is relevant to the state of a target user and unpopular for other users, it would have higher chance to be recommended to this user.
この式によれば、あるアイテムがターゲットユーザーの状態に関連し、他のユーザーには不人気である場合、そのユーザーに推薦される可能性が高くなる。
It could be discussed that equation (8) indicates that to how much extent item i is specific to user u.
式(8)は、項目iがどの程度ユーザーuに特有であるかを示していると論じることができる。
Personalized recommendations for each user contains items which are relevant to the target user and are less relevant for the users with different profiles that user u.
各ユーザーにパーソナライズされたレコメンデーションは、ターゲットユーザーに関連し、ユーザーuと異なるプロファイルを持つユーザーには関連性の低いアイテムを含んでいます。
In other words, items that are common interests for users with different profiles are not good candidates for personalized recommendations.
言い換えれば、異なるプロフィールを持つユーザーにとって共通の関心事であるアイテムは、パーソナライズされたレコメンデーションには適さないということだ。
In general, low-degree items provide higher levels of specification.
一般的に、程度の低い項目は、より高い仕様レベルを提供する。
Therefore, we expect SM model to give higher scores to items with lower degrees.
したがって、SMモデルは度数の低い項目ほど高い得点を与えると予想される。

Transition function for SM model can be extracted from AT or AC graphs based on maximum likelihood estimation method.
SMモデルの遷移関数は、最尤推定法に基づいてATまたはACグラフから抽出することができる。
Thus, in SM model, the transition function from node i to j is defined as the weight of the edge (i,j) in AT or AC graphs divided by the indegree of node j.
したがって、SMモデルでは、ノードiからjへの遷移関数は、ATまたはACグラフのエッジ(i,j)の重みをノードjのインデグリーで割ったものとして定義される。
Compared with PM model, SM model provides a recommendation list that is biased toward low-degree items.
PMモデルと比較すると、SMモデルは程度の低い項目に偏った推薦リストを提供する。
It is intuitive that, often, items with high degrees provide less specification than low-degree items.
直感的には、度数の高い項目は度数の低い項目よりもスペックが低いことが多い。
Items with high popularity (e.g., degree) have better chance than those with low popularity to be attended, and thus, less popular items are likely to be specific to users.
人気の高い項目（例えば学位）は、人気の低い項目よりも参加される確率が高いので、人気の低い項目はユーザーにとって特定の項目である可能性が高い。

Let us further explain PM and SM models by an example.
PMモデルとSMモデルを例にとってさらに説明しよう。
Suppose that item i has high dependency on the profile of user u and the most of the users with similar tastes as user u have purchased item i.
アイテムiはユーザーuのプロフィールへの依存度が高く、ユーザーuと同じような嗜好を持つユーザーのほとんどがアイテムiを購入しているとします。
Therefore, based on equation ( 6), the item would get a high score of recommendation for user u.
したがって、式( 6)に基づき、その項目はユーザーuにとって高い推奨スコアを得ることになる。
On the other hand, suppose that users with different interests as compared to user u also have high probability of transition to this item, which means that the interest in item i is not specific to the profile of user u.
一方、ユーザーuと異なる興味を持つユーザーも、このアイテムに移行する確率が高いとする。これは、アイテムiへの興味がユーザーuのプロファイルに特有ではないことを意味する。
Therefore, based on equation (8), this item would get a low score of recommendation.
したがって、（8）式に基づけば、この項目の推奨度は低いことになる。
In an example from movie recommendation framework, consider a movie which wins an Academy Award.
映画推薦のフレームワークの例として、アカデミー賞を受賞した映画を考えてみよう。
In general, a large group of users are probable to visit this item in the future.
一般的に、多くのユーザーが将来このアイテムを訪れる可能性がある。
Therefore, recommending this item is favorable regarding the precision criterion.
したがって、この項目を推薦することは、精度基準に関して有利である。
However, since this item is a common interest of users with different profiles, recommending the item would not satisfy the personalization.
しかし、このアイテムは異なるプロフィールを持つユーザーの共通の関心事であるため、このアイテムを推薦してもパーソナライゼーションは満たされない。

We investigate structure of SM and PM models in an example shown in Fig.2 .
図2の例でSMモデルとPMモデルの構造を調べる。
Let us consider two sets of states A and B which form a small state space.
小さな状態空間を形成する2つの状態A、Bの集合を考えてみよう。
Weight of the edges between any A i and B j is the number of users that are transmitted from A i to B j .
任意のA iとB jの間のエッジの重みは、A iからB jに送信されたユーザーの数である。
Based on these weights and maximum likelihood estimation, probability of transition for a user from A 1 to B 1 , B 2 and B 3 in the next step is 0.80, 0.20 and 0, respectively.
これらの重みと最尤推定に基づき、あるユーザーが次のステップでA 1からB 1、B 2、B 3に移行する確率は、それぞれ0.80、0.20、0となる。
Thus, the highest transition probability is from A 1 to B 1 .
したがって、最も高い遷移確率はA 1からB 1への遷移である。
It is also possible to determine the most probable origin.
また、最も可能性の高い起源を特定することも可能である。
Let us suppose we are at state B 1 , B2 or B 3 .
B 1 、 B 2 、 B 3 の 状 態 に あ る と し ま し ょ う 。
Based on maximum likelihood estimation strategy, the probability that the user in the previous step was started at A 1 is 0.40, 0.5 and 0 for B 1 , B2 and B 3 , respectively.
最尤推定戦略に基づき、前のステップのユーザーがA 1で開始された確率は、B 1、B 2、B 3についてそれぞれ0.40、0.5、0である。
Thus, A 1 is the most probable start point if the state is B 2 .
したがって、状態がB 2の場合、A 1が最も可能性の高いスタート地点となる。
SM and PM models perform in the same manner as this example.
SMとPMのモデルは、この例と同じように機能する。
PM model recommends items, which a user u has the highest probability to transmit their L-state from S u .
PM モデルでは、ユーザ u が S u から L 状態を送信する確率が最も高いアイテムを推薦する。
Whereas, SM model recommends items, which if the user stated at its L-state (i.e., if we recommend the item to the user and he/she becomes satisfied with the item), it has the highest probability that the user was transmitted from S u .
一方、SM モデルでは、ユーザが L 状態になった場合（ユーザがそのアイテムを推奨し、満足した場合）、そのユーザが S u から送信された確率が最も高いアイテムを推奨する。
If we investigate PM and SM models based on the popularity of items in their recommended lists, in average, both of them recommend items which are relevant to the target user; however, PM model recommends items with almost high degree (popularity), while SM model introduces items with almost low degree.
PMモデルとSMモデルを、推薦リストに含まれるアイテムの人気度に基づいて調べると、平均的には、両モデルとも対象ユーザに関連性の高いアイテムを推薦するが、PMモデルは、ほぼ高い度合い（人気度）のアイテムを推薦し、SMモデルは、ほぼ低い度合いのアイテムを紹介する。
It is clear that items with high degree are likely to attract users' attention in near future, which would result in high precision for the model.
度数の高い項目は、近い将来ユーザーの注目を集める可能性が高く、モデルの精度が高くなることは明らかである。
On the other hand, this type of recommendation often results in low novelty and can be considered as obvious recommendations.
一方、このタイプの推薦は新規性が低く、自明な推薦とみなされることが多い。
Unlike to PM, SM recommends the items with low degree which increases the risk of recommendations and makes the lists more informative.
PMとは異なり、SMは程度の低い項目を推奨するため、推奨のリスクが高まり、リストがより有益になる。
We introduce a hybrid model in the next section in order to integrate these two models to construct a recommender with controllable levels of precision and novelty.
この2つのモデルを統合し、精度と新規性のレベルを制御可能なレコメンダーを構築するために、次のセクションでハイブリッドモデルを紹介する。

## Hybrid recommender ハイブリッド・レコメンダー

We articulated that SM and PM models provide the recommendation lists by producing a vector of probabilities on items set.
我々は、SMモデルとPMモデルが、アイテムセットに対する確率のベクトルを生成することによって、推薦リストを提供することを明確にした。
Here, we introduce a hybrid model, which uses both SM and PM model aiming at providing a recommendation list that is user-specific with good precision as much as possible.
ここでは、SMモデルとPMモデルのハイブリッドモデルを紹介する。
The hybrid model is simple model that linearly combines the outputs of SM and PM models.
ハイブリッドモデルは、SMモデルとPMモデルの出力を線形結合したシンプルなモデルである。
The probability vector of our proposed hybrid model, P CP , is obtained as:
我々の提案するハイブリッドモデルの確率ベクトルP CP は次のように求められる：

where P SM and P PM are the probability vectors extracted by PM and SM models, respectively.
ここで、P SMとP PMはそれぞれPMモデルとSMモデルによって抽出された確率ベクトルである。
α is a parameter in the range [0, 1] that is tuned by the system owner depending on the performance he/she is looking for.
αは[0, 1]の範囲のパラメータで、システムオーナーが求める性能に応じて調整する。
As α increases, the final recommendation list has a tendency to SM model, whereas small value of α dominates the PM model and gives more weight to the precision of the recommendation list.
αが大きくなるにつれて、最終的な推薦リストはSMモデルに傾くが、αの値が小さいとPMモデルが優位となり、推薦リストの精度が重視される。
SM and PM models could be combined in other ways.
SMとPMのモデルは他の方法で組み合わせることもできる。
For example, items can be ranked based on P SM and P PM , leading to a ranking vector obtained from each of the models which we call them R PM and R SM .
例えば、アイテムは P SM と P PM に基づいてランク付けすることができ、それぞれのモデルから得られるランク付けベクトルを R PM と R SM と呼ぶ。
The vector of the rankings can be linearly combined as
ランキングのベクトルは、次のように線形結合できる。

The obtained vector, R CP , could be used to do the final recommendations.
得られたベクトルR CPは、最終的な推薦に使用することができる。

### 3.3.2 Structural analysis of the proposed model 3.3.2 提案モデルの構造分析

One of the main problems of Markov chain model is how to determine the size of the state.
マルコフ連鎖モデルの主な問題の一つは、状態の大きさをどのように決定するかということである。
By increasing the size, and due of the sparsity problem, the extracted transition function would become unreliable.
サイズが大きくなり、スパース性の問題により、抽出された遷移関数は信頼できなくなる。
On the other hand, small number of chains is not able to appropriately represent users' state.
一方、鎖の数が少ないと、ユーザーの状態を適切に表現できない。
Since a user's states in such models consider only the previously purchased items by the user, it does not take into account user's ratings value.
このようなモデルにおけるユーザーの状態は、ユーザーが過去に購入したアイテムのみを考慮するため、ユーザーの評価値は考慮されない。
Also as mentioned, models based on Markov chain often result in good precision by recommending popular items, while its novelty is often low.
また、前述のように、マルコフ連鎖に基づくモデルは、人気のあるアイテムを推奨することで精度が高くなることが多いが、その一方で新規性は低いことが多い。
Our proposed model tries to tackle these challenges by new definition for the state of users and modifying the prediction model.
我々の提案するモデルは、ユーザーの状態を新たに定義し、予測モデルを修正することで、これらの課題に取り組もうとしている。
Since state vector of each user consists of all items purchased by the user, we do not ignore any data in the state definition and the statesas weighted vectors provide flexibility for the model to add more information about each item.
各ユーザーの状態ベクトルは、ユーザーが購入したすべてのアイテムから構成されるため、状態の定義においてデータを無視することはなく、また、状態として重み付けされたベクトルは、各アイテムに関するより多くの情報をモデルに追加する柔軟性を提供する。
For example, it is possible to give higher weights for items recently purchased by the user.
例えば、ユーザーが最近購入した商品により高いウェイトを与えることが可能である。
Also, separating each item into two states makes our model be able to take into account rating values.
また、各アイテムを2つの状態に分けることで、評価値を考慮したモデルになる。

The most significant contribution we have in our proposed model is to solve the novelty problem of traditional Markov models by introducing a hybrid model which is able to address the novelty and precision challenge by tuning a hybridization parameter.
我々が提案するモデルで最も重要な貢献は、ハイブリッド化パラメータを調整することにより、新規性と精度の課題に対処できるハイブリッドモデルを導入することで、従来のマルコフモデルの新規性の問題を解決することである。
Markov-based methods are model-based algorithms for recommendation systems which have computational complexity of O(n) where n is the number of ratings in the training dataset.
マルコフベースの手法は、推薦システムのためのモデルベースのアルゴリズムであり、計算量はO(n)である。
Compared with other recommendation algorithms, they have considerably better computational complexity.
他の推薦アルゴリズムと比較して、計算複雑性がかなり優れている。
Also, these models outperform other traditional models in terms of precision.
また、これらのモデルは、精度の面でも他の従来のモデルを凌駕している。
However, the main problem that restricts the usage of Markov models in commercial systems is low novelty of their recommended lists.
しかし、商用システムでマルコフモデルの使用を制限する主な問題は、推奨リストの新規性が低いことである。
Our proposed model has the same computational complexity with the original Markov model, while the novelty of its recommendation list is much higher.
我々の提案するモデルの計算量はオリジナルのマルコフモデルと同じであるが、推薦リストの新規性ははるかに高い。

# 4. RESULTS 4. 結果

In order to compare the performance of the proposed recommendation algorithm with that of some classic algorithms, we applied them on Netflix and Movielens datasets, which are frequently considered as benchmarks in recommendation problems.
提案する推薦アルゴリズムといくつかの古典的アルゴリズムの性能を比較するために、推薦問題のベンチマークとして頻繁に考慮されるNetflixとMovielensデータセットに適用した。

## 4.1 Datasets 4.1 データセット

Two datasets (Netflix and Movielens) were employed to evaluate performance of the proposed method.
提案手法の性能を評価するために、2つのデータセット（NetflixとMovielens）を採用した。
Both datasets are ratings of users to set of movies on a scale of 1-5.
どちらのデータセットも、一連の映画に対するユーザーの評価を1～5の尺度で表したものである。
The Netflix dataset used in the experiments is a random subset of the original Netflix dataset and is with 9,983 users, 6,533 items and 2,041,247 ratings.
実験に使用したNetflixデータセットは、オリジナルのNetflixデータセットのランダムなサブセットで、9,983ユーザー、6,533アイテム、2,041,247レーティングからなる。
Movielens dataset is with 6,040 users, 3,952 items and 1,000,209 ratings.
Movielensデータセットには、6,040人のユーザー、3,952のアイテム、1,000,209の評価が含まれています。
Table 1 summarizes the statistics of the datasets.
表1にデータセットの統計をまとめた。
For Netflix dataset, only the date of the ratings is available, while for Movielens dataset, the time label of ratings is available in seconds.
Netflixデータセットでは、評価の日付のみが利用可能であるが、Movielensデータセットでは、評価の時間ラベルが秒単位で利用可能である。
According to the structure of our model and since in many applications explicit ratings are not available, we transformed rating values from scale of 1-5 to ratings with Like or Dislike form.
私たちのモデルの構造に従い、また多くのアプリケーションでは明示的なレーティングが利用できないため、私たちはレーティング値を1～5のスケールからLikeまたはDislike形式のレーティングに変換した。
In order to do this, we defined value of 2.5 as a threshold and considered ratings above the threshold as Like and ratings below the threshold as Dislike.
そのため、2.5を閾値とし、閾値以上の評価を「いいね！」、閾値未満の評価を「嫌い」と見なした。

## 4.2 Performance Metrics 4.2 パフォーマンス指標

To test recommendation models, we divided the datasets into two parts: training and test datasets.
レコメンデーション・モデルをテストするために、データセットをトレーニング・データセットとテスト・データセットの2つに分けた。
Datasets were sorted based on time label of ratings, and the first 90% of the ratings were considered as training dataset and the rest as test dataset.
データセットは、評価の時間ラベルに基づいてソートされ、評価の最初の90％がトレーニングデータセット、残りがテストデータセットとみなされた。
In order to test the recommendation algorithms, we used users who had at least one rating in the training dataset and their number of ratings in test dataset was above the size of the recommendation list.
推薦アルゴリズムをテストするために、トレーニングデータセットに少なくとも1つの評価があり、テストデータセットの評価数が推薦リストのサイズ以上のユーザーを使用した。
Among five measures we employed to test the performance of the algorithms, four of them concern the recommended lists with size N and one concerns the whole items ranked by the recommendation algorithm.
アルゴリズムの性能をテストするために採用した5つの尺度のうち、4つはサイズNの推奨リストに関するもので、1つは推奨アルゴリズムによってランク付けされたアイテム全体に関するものである。
In our experiments, we used an off-line evaluation.
私たちの実験では、オフライン評価を使用した。
For each test user, we hided test dataset and asked the recommender algorithms to perform the recommendations based on the user's ratings in training dataset.
各テストユーザーについて、テストデータセットを隠し、推薦アルゴリズムにトレーニングデータセットのユーザーの評価に基づいて推薦を実行するように依頼した。
The quality of the recommendations was evaluated based on the items the test user has already purchased in the test dataset.
レコメンデーションの品質は、テストデータセットに含まれるテストユーザーが既に購入したアイテムに基づいて評価された。

### 4.2.1 Recovery 4.2.1 回復

In order to evaluate performance of recommender algorithms in giving a proper ranking to whole item set, we employed the recovery metric.
アイテムセット全体に適切なランキングを与える推薦アルゴリズムの性能を評価するために、回復指標を採用した。
We prefer systems that give higher rank for items that are relevant to the target user.
私たちは、ターゲットユーザーに関連性の高いアイテムに高いランクを与えるシステムを好みます。
Relevant items to each user can be extracted based on her/his ratings in test dataset.
各ユーザに関連する項目は、テストデータセットにおけるそのユーザの評価に基づいて抽出される。
We considered items purchased by a test user and get Like rating in the test dataset as relevant items to the target user.
テスト・データセットにおいて、テスト・ユーザーが購入し、「いいね！」評価を得たアイテムを、ターゲット・ユーザーに関連するアイテムとみなした。
Hence, recovery R can be obtained as:
したがって、回復Rは次のように求められる：

where C u is the number of candidate items for recommendation in item set, L u is the number of relevant items to user u, r i is the place for item i in the ranked list for user u and |u TestSet | is the number of users in the test dataset.
u TestSet
According to this definition of recovery, the lower R u is, the more accurate the system.
このリカバリーの定義によれば、R uが低いほど、より正確なシステムということになる。

### 4.2.2 Precision 4.2.2 精度

Many applications are designed so that they recommend N items to users.
多くのアプリケーションは、ユーザーにN個のアイテムを推薦するように設計されている。
Precision for the list recommended to user u, P u (N) is defined as the percentage of the relevant items to user u in the list recommended to the user.
ユーザーuに推奨されるリストの精度、P u (N)は、ユーザーに推奨されるリスト内のユーザーuに関連する項目の割合として定義されます。
We considered items purchased by the target user in test dataset and received Like rating as relevant items to the target user.
テストデータセットでターゲットユーザーが購入し、「いいね！」を獲得したアイテムを、ターゲットユーザーに関連するアイテムとみなした。
Precision of the systems on a recommendation list with N items can be defined as: () ()
N個の項目を持つ推薦リストのシステムの精度は次のように定義できる： () ()

### 4.2.3 Item space coverage 4.2.3 アイテム・スペース・カバレッジ

A good recommendation method supports large part of item space in its recommendation list.
優れた推薦方法は、その推薦リストに含まれるアイテム空間の大部分をサポートする。
In other words, we are interested in methods which can recommend large proportion of items in their recommendations.
言い換えれば、私たちは、推薦の中で大きな割合を占めるアイテムを推薦できる手法に興味がある。
To measure this property, the percentage of items that are recommended to test users can be extracted.
この特性を測定するために、テストユーザーに推奨されるアイテムの割合を抽出することができる。
However, this measure does not take into account the number of times each item appears in recommendation lists.
しかし、この指標では、各項目が推薦リストに登場する回数は考慮されていない。
Some items may appear in the lists frequently, whereas some others might be recommended only once.
リストには頻繁に登場するものもあれば、一度しか推薦されないものもある。
In order to have a metric without such a problem, item space coverage is given by Shannon entropy as:
このような問題のない指標を持つために、アイテム空間のカバレッジはシャノンエントロピーで与えられる：

where p i is the percentage of recommendation lists that contains item I and L is the number of candidate items.
ここで、p iはアイテムIを含む推薦リストの割合、Lは候補アイテムの数である。

### 4.2.4 Diversity 4.2.4 多様性

One of the measures which concerns about personalization in recommender systems is inter list diversity measure.
推薦システムにおけるパーソナライゼーションに関係する尺度のひとつに、リスト間の多様性尺度がある。
It is desirable in recommender systems to recommend an item set which is unique for the target user and fits her/his interests.
レコメンダーシステムでは、ターゲットユーザーにとってユニークで、そのユーザーの興味に合ったアイテムセットを推薦することが望ましい。
For two users i and j, the distance between their lists (d i,j ) can be obtained as:
2人のユーザーiとjについて、そのリスト間の距離（d i,j ）は次のように求めることができる：

, ,
, ,

where c i,j is the number of common items in the lists recommended to these users, and N is size of the recommended lists.
ここで、c i,jは、これらのユーザーに推奨されるリストに共通する項目の数であり、Nは推奨リストのサイズである。
Inter list diversity D(N) is the average distance (as defined above) between all test users.
リスト間多様性D(N)は、すべてのテストユーザー間の平均距離（上記で定義）である。
As D is higher, the method recommends more personalized recommendation lists.
Dが高いほど、この方法はよりパーソナライズされた推薦リストを推薦する。

### 4.2.5 Novelty 4.2.5 新規性

A recommendation list becomes more informative and novel as the target user is less likely to know the existence of the items form the recommended list.
レコメンデーションリストは、ターゲットユーザーがレコメンデーションリストのアイテムの存在を知る可能性が低くなるため、より有益で斬新なものになる。
Various methods have been introduced to evaluate novel recommendations [37].
新しい推奨を評価するために、様々な方法が導入されている[37]。
Self-information based novelty is a measure for novelty relative to popularity of items [33].
自己情報に基づく新規性は、アイテムの人気度に対する新規性の尺度である[33]。
According to this measure, popular items provide less novelty.
この尺度によれば、人気のあるアイテムは目新しさが少ない。
Self-information based novelty can be obtained as:
自己情報に基づく新規性は、次のように求めることができる：

where |u| is the number of test users and rels i indicates the number of users that have purchased item i.
u

4.3 Experimental results and discussion
4.3 実験結果と考察

The proposed hybrid model has a parameter α, which largely influences its performance.
提案するハイブリッドモデルには、その性能に大きく影響するパラメータαがある。
This parameter can be customized depending on the desired performance.
このパラメーターは、希望するパフォーマンスに応じてカスタマイズできる。

In our experiments, we evaluated performance of the hybrid model as a function of hybridization parameter α.
実験では、ハイブリッドモデルの性能をハイブリッド化パラメータαの関数として評価した。
We compared the performance of the proposed model with that of three well-known recommendation algorithms: memory-based CF (item based CF and user based CF), classic Markov model and popularity-based recommender.
提案モデルの性能を、メモリベースCF（アイテムベースCFとユーザベースCF）、古典的マルコフモデル、人気度ベース推薦器の3つのよく知られた推薦アルゴリズムの性能と比較した。
We also compared two forms of the proposed algorithm: time aware (known time tags of the ratings) and time unaware (unknown time tags).
また、提案アルゴリズムの2つの形式を比較した：時間認識（評価の時間タグが既知）と時間非認識（時間タグが未知）。

### 4.3.1 Dependence of the performance measures on α 4.3.1 パフォーマンス尺度のα依存性

Figure 3 shows the performance of the proposed method (as compared to user-based CF and popularity-based method) in terms of different metrics in Netflix and Movielens datasets.
図3は、NetflixとMovielensのデータセットにおける、提案手法のパフォーマンス（ユーザーベースCFと人気度ベース手法との比較）を、さまざまなメトリクスの観点から示している。
In both datasets in sequence aware (SA) version of the model, the value of α = 0 (PM model) results in the highest precision and the lowest novelty, whereas the value of α = 1 (SM model) results in the highest novelty and the lowest precision.
シーケンス認識（SA）モデルの両データセットにおいて、α=0（PMモデル）は最も精度が高く、新規性が低いのに対し、α=1（SMモデル）は新規性が高く、精度が低い。
These two metrics have a monotonic performance (decreasing for precision and increasing for novelty) as α increases from 0 to 1.
これらの2つのメトリクスは、αが0から1に増加するにつれて単調なパフォーマンス（精度は低下し、新規性は増加する）を示す。
However, in Sequence Unaware (SU) form of the model in both datasets α = 0.1 results in highest precision.
しかし、シーケンス非認識（SU）モデルの場合、どちらのデータセットでもα = 0.1が最も高い精度となる。
Depending on the performance one would like to have (precision might be more important in some application and less in some others), α can be tuned so that the desired performance is obtained.
求める性能に応じて（ある用途では精度がより重要かもしれないし、他の用途ではそれほど重要ではないかもしれない）、αは望ましい性能が得られるように調整することができる。
In our experiments, we could always find a value of α such that both precision and novelty of the proposed recommendation algorithm is higher than user-based CF and popularitybased methods.
我々の実験では、提案する推薦アルゴリズムの精度と新規性の両方が、ユーザーベースのCFや人気度ベースの手法よりも高くなるようなαの値を常に見つけることができた。
In terms of recovery metric, both SM and PM algorithms give higher ranks to items that are relevant to taste of the target user, with recovery rates always below 0.5.Note that the value of the recovery rate as 0.5 for a recommendation algorithm indicates that the algorithm works like a random machine in producing ranked list of items for a target user.
回復率という指標で見ると、SMアルゴリズムもPMアルゴリズムも、対象ユーザの嗜好に関連するアイテムにより高いランクを与えており、回復率は常に0.5以下である。推薦アルゴリズムにおいて回復率が0.5という値は、そのアルゴリズムが対象ユーザに対してランク付けされたアイテムのリストを生成する際にランダムマシンのように動作することを示している。

Given the time series of items' popularity, their popularity in near future is predictable [41].
アイテムの人気の時系列を考えると、近い将来の人気は予測可能である[41]。
It can easily be shown that items with low popularity are unlikely to become popular in a short time horizon such as 1-2 weeks.
人気のないアイテムが1-2週間といった短い時間軸で人気になる可能性は低いことは、簡単に示すことができる。
Hence, recommendation of popular items has a low risk in terms of precision measure, while recommending unpopular items increases the risk of hit ratio and often results in low precision.
それゆえ、人気のあるアイテムを推薦することは、精度測定においてリスクが低く、一方、不人気のアイテムを推薦することは、ヒット率のリスクを高め、しばしば精度が低くなる。
In order to have good precision of recommendation, users should purchase items with the highest popularity more than those with lower popularity.
レコメンデーションの精度を高くするためには、ユーザーは人気の高いアイテムを人気の低いアイテムよりも多く購入する必要がある。
As mentioned, SM favors items with low degree, while PM is biased toward items with high degree.
前述したように、SMは度数の低い項目を好むが、PMは度数の高い項目に偏る。
These specifications of SM and PM models justify the higher precision and also better recovery rate of PM model as compared to SM model.
SMモデルとPMモデルのこれらの仕様は、SMモデルに比べてPMモデルの方が精度が高く、回収率も高いことを裏付けている。
The proposed hybrid recommendation method has by far better performance than memory-based CF models (both item-based and user-based forms), and popularitybased methods in terms of diversity and coverage measures.
提案するハイブリッド推薦法は、多様性と網羅性の尺度の点で、記憶ベースのCFモデル（項目ベースとユーザーベースの両方の形式）、および人気ベースの方法よりもはるかに優れた性能を持つ。
Also, there is optimal value of α for these metrics.
また、これらのメトリクスには最適なαの値がある。
In other words, for the optimal value of α, the proposed hybrid model has better coverage and diversity than individual PM and SM models.
言い換えれば、αの最適値に対して、提案されたハイブリッドモデルは、個々のPMモデルとSMモデルよりも優れたカバレージと多様性を持つ。
Each of PM and SM models has focus on only particular part of item space and their recommendations partially cover the item space.
PMとSMの各モデルは、アイテム空間の特定の部分のみに焦点を当て、それらの推奨はアイテム空間を部分的にカバーしている。
This restriction causes these models to have low coverage.
この制限により、これらのモデルはカバー率が低い。
The hybrid model overcomes this restriction and makes it possible to cover whole item space in recommendations.
ハイブリッドモデルはこの制約を克服し、レコメンデーションにおけるアイテム空間全体をカバーすることを可能にする。
Indeed, the proposed hybrid model considers items with different degrees in recommendation while SM supports items with low degree and PM supports high-degree items.
実際、提案されたハイブリッドモデルは、SMが程度の低い項目をサポートし、PMが程度の高い項目をサポートする一方で、推薦において程度の異なる項目を考慮する。
Figure 4 shows the degree distribution of recommendations of hybrid model for different value of α on Netflix and Movielens datasets.
図4は、NetflixとMovielensのデータセットにおいて、αの値を変えた場合のハイブリッドモデルの推奨度分布を示す。
The proposed model with α = 0.7 and α = 0.4 gives chance to items with different degrees to appear in recommendation lists, where α = 0 or α = 0.9 only consider items with special degree characteristics in their recommendations.
α＝0.7とα＝0.4の提案モデルは、α＝0またはα＝0.9の場合、特別な度数の特徴を持つアイテムのみを推薦リストに考慮するのに対し、異なる度数のアイテムに推薦リストに表示されるチャンスを与える。
Our results show that for both datasets, diversity and coverage measures reached their maximum for α ~ 0.9.
その結果、両データセットとも、α～0.9で多様性とカバレッジが最大になった。

Figure 5 demonstrates the degree distribution of Movielens and Netflix dataset.
図5は、MovielensとNetflixのデータセットの度数分布を示している。
As the distributions show, about 20 percent of the items attract 80 percent of users' ratings in both datasets.
分布が示すように、どちらのデータセットでも、約20％のアイテムが80％のユーザーの評価を集めている。
Thus, a large number of items in the item space have low degrees and, thus, low popularity values.
したがって、アイテム空間内の多くのアイテムは度数が低く、したがって人気値も低い。
When we focus on items with low degree (α ~ 0.9), the model covers large number of items in its recommendations and the coverage becomes maximum.
次数の低い項目（α～0.9）に注目した場合、モデルは推薦の中で多くの項目をカバーし、カバレッジは最大となる。
However, the bias toward very low-degree items for the values α > 0.95 causes the model to lose coverage and diversity.
しかし、α＞0.95の場合、非常に次数の低い項目に偏るため、モデルの網羅性と多様性が失われる。
Overall, hybridizing SM and PM models not only is a mean to resolve accuracy and novelty dilemma, but also significantly improves diversity and coverage as compared to individual SM and PM models as well as user-based CF and popularity-based recommendation methods.
SMモデルとPMモデルのハイブリッドは、精度と新規性のジレンマを解決する手段であるだけでなく、個々のSMモデルやPMモデル、ユーザーベースのCFや人気度ベースの推薦手法と比較して、多様性と網羅性を大幅に向上させる。
To better analyze the behavior of the model as a function of the hybridization parameter, let us give a toy example.
ハイブリダイゼーション・パラメーターの関数としてのモデルの挙動をよりよく分析するために、おもちゃの例を挙げてみよう。
Suppose that we have three classes of items with different popularity intervals: very unpopular (A), unpopular (B) and popular (C).
異なる人気間隔を持つ3つのクラスのアイテムがあるとする：非常に不人気（A）、不人気（B）、人気（C）。
These three classes contain 20%, 60% and 20% of items, respectively.
この3つのクラスには、それぞれ20％、60％、20％のアイテムが含まれている。
Intuitively, we may say that SM model gives higher score for items that are relevant to the target user and also belong to class A.
直感的には、SMモデルは、ターゲット・ユーザーに関連し、かつクラスAに属する項目に対して高いスコアを与える、と言えるかもしれない。
PM model has a bias toward items that are relevant to the target user's taste and belong to C.
PMモデルは、ターゲットユーザーの嗜好に関連し、Cに属するアイテムにバイアスをかける。
Thus, in general, PM model recommends items in class C and SM covers items in class A; each of these models eliminate about 80% of the item space in their recommendations.
一般的に、PMモデルはクラスCのアイテムを推薦し、SMモデルはクラスAのアイテムを推薦する。
As we mentioned, hybridization of PM and SM models overcomes this restriction and the hybrid model considers the items from the all three classes in its recommendations.
前述のように、PMモデルとSMモデルのハイブリッド化はこの制約を克服し、ハイブリッドモデルはその推薦において3つのクラス全ての項目を考慮する。

### 4.3.2 Sequence aware (SA) and sequence unaware (SU) forms of the model 4.3.2 シーケンス認識モデル(SA)とシーケンス非認識モデル(SU)

In general, SA and SU forms of the proposed recommendation algorithm have almost similar behavior as a function of α.
一般に、提案された推薦アルゴリズムのSA形式とSU形式は、αの関数としてほぼ同様の振る舞いをする。
SU form of PM model as compared to SA form of the same model is more biased toward high-degree items, whereas SU form of SM model is more biased toward low-degree items than SA form of the model.
PMモデルのSU型はSA型に比べて高次の項目に偏っているのに対し、SMモデルのSU型はSA型に比べて低次の項目に偏っている。
Due to this property of SA models, SU form of PM model provides higher precision compared to SA form of PM model.
SAモデルのこの特性により、SU形式のPMモデルはSA形式のPMモデルよりも高い精度を提供する。
Similarly, higher novelty can be achieved by SU form of SM model than SA form of the same model.
同様に、同じモデルのSA型よりも、SMモデルのSU型の方が高い新規性を達成できる。
Related to this characteristic, SU form of our proposed hybrid model has lower diversity and coverage.
この特徴に関連して、我々の提案するハイブリッドモデルのSU型は、多様性とカバレッジが低い。
This is due to the fact that the sector of item space that is covered by SU model is smaller than the one covered by SA models.
これは、SUモデルがカバーするアイテム空間の領域が、SAモデルがカバーする領域よりも小さいためである。

### 4.3.3 The proposed model versus classic baseline models 4.3.3 提案モデルと古典的ベースラインモデルとの比較

In the implementation of user-based CF, we used weighted average of 50 users that have rated the target item and have had the highest similarity with the target user.
ユーザーベースCFの実装では、対象アイテムを評価したユーザーのうち、対象ユーザーとの類似度が最も高い50人の加重平均を使用した。
Also, in the classic Markov-based model we used Markov chain of order 2.
また、古典的なマルコフベースのモデルでは、次数2のマルコフ連鎖を使用した。
Popularity-based model recommends items to the target user which has the highest popularity among those items that have not yet purchased by the user.
人気度ベースのモデルは、ユーザーがまだ購入していないアイテムの中で最も人気の高いアイテムをターゲットユーザーに推薦する。
Although popularity-based recommender has proper performance on precision and recovery parameters and outperforms the proposed hybrid models for some value of α, it has low novelty.
人気度ベースのレコメンダーは精度と回復パラメータにおいて適切な性能を持ち、αの値によっては提案されたハイブリッドモデルを凌駕するが、新規性は低い。
Moreover, since the popularity-based model only covers items with high popularity, its performance in terms of coverage and diversity measures is low as compared to other models.
さらに、人気度ベースのモデルは人気度の高いアイテムしかカバーしないため、カバー率と多様性の指標における性能は他のモデルに比べて低い。
This makes this method have little applicable in many cases.
そのため、この方法は多くの場合、ほとんど適用できない。

Almost for all value of α, the proposed model (in both SA and SU forms) outperformed memory-based CF in terms of diversity and coverage.
ほぼすべてのαの値において、提案モデル（SAとSUの両形態）は、多様性とカバレッジの点でメモリベースのCFを上回った。
Memory-based CF, in average, gives about 15 and 20 percent lower diversity compared with SU and SA models, respectively.
メモリベースのCFは、SUモデルやSAモデルと比較して、平均してそれぞれ約15％、20％低い多様性を与える。
In terms of precision and novelty measures, for some values of α, memory-based CF outperformed the proposed model.
精度と新規性の指標において、αの値によってはメモリベースCFが提案モデルを上回った。
However, there exist some values for α for which the proposed model outperforms CF in all evaluation measures.
しかし、提案モデルがすべての評価指標でCFを上回るαの値が存在する。
For example, in Netflix dataset, SA outperformed CF for the values of α in the range [0.75, 0.85] and SU outperformed CF for α > 0.98.
例えば、Netflixデータセットでは、αの値が[0.75, 0.85]の範囲ではSAがCFを上回り、α>0.98ではSUがCFを上回った。
According to the results, it can be said that CMR provides more accurate and diverse recommendations than memory-based models.
この結果によれば、CMRは記憶に基づくモデルよりも正確で多様なレコメンデーションを提供すると言える。
However, SU compared with CMR has better performance in terms of the all metrics for 0.2 < α < 0.5.Furthermore, for the range of 0.6 < α < 0.9, SU outperforms CMR in terms of all evaluation metrics, while having almost the same novelty.
さらに、0.6 < α < 0.9の範囲では、新規性はほとんど変わらないが、すべての評価指標でSUがCMRを上回る。

# 5. CONCLUSION 5. 結論

Recommendation systems are increasingly being used in various applications such as online stores.
レコメンデーションシステムは、オンラインショップなど様々なアプリケーションで利用されるようになってきている。
The aim of a recommender system is to use historical data about the users' behavior (e.g., their purchases as well as ratings on purchased items) and provide a list of items to each user such that they are likely to be purchased by the user in near future.
レコメンダーシステムの目的は、ユーザーの行動に関する過去のデータ（例えば、購入品や購入品に対する評価）を利用し、近い将来にユーザーが購入する可能性の高いアイテムのリストを各ユーザーに提供することである。
Traditionally, performance of recommender systems has been evaluated by their precision.
従来、推薦システムの性能はその精度で評価されてきた。
However, in order to find a practical application in real commercial systems, a recommender is needed to provide a recommendation list not only with high precision, but also with high levels of novelty and diversity.
しかし、実際の商用システムで実用化するためには、レコメンダーは高い精度を持つだけでなく、高い新規性と多様性を持つ推薦リストを提供する必要がある。
Often, the users would like to have novel and diverse recommendation list and such recommendations results in better user satisfaction.
多くの場合、ユーザーは斬新で多様なレコメンデーションリストを持ちたいと思うし、そのようなレコメンデーションはユーザーの満足度を向上させる。

In this manuscript, we introduced a probabilistic model, which has a full control on the level of precision, novelty and diversity.
この原稿では、精度、新規性、多様性のレベルを完全に制御できる確率的モデルを導入した。
The model is a hybrid one as a linear integration of two state-automata based prediction models: specification maximizer and precision maximizer prediction models.
このモデルは、スペック最大化予測モデルと精度最大化予測モデルという、2つの状態オートマタに基づく予測モデルを線形統合したハイブリッドモデルである。
The goal for specification maximizer model is to recommend items that are most specific to tastes of target users.
スペック・マキシマイザー・モデルの目標は、ターゲット・ユーザーの嗜好に最も特化したアイテムを推薦することである。
The precision maximizer model aims at recommending items that have the highest probability to satisfy the target users.
精度最大化モデルは、ターゲットユーザーを満足させる確率が最も高いアイテムを推薦することを目的としている。
In order to construct the models, we took into account the sequence by which the items are purchased by the users.
モデルを構築するために、ユーザーがアイテムを購入する順序を考慮した。
Our experiments showed that the proposed model could successfully deal with the dilemma of novelty-precision in recommendation systems and could result in better performance than classic recommenders such as user-based collaborative filtering and popularity-based algorithms.
我々の実験により、提案モデルは推薦システムにおける新規性-精度のジレンマにうまく対処でき、ユーザーベースの協調フィルタリングや人気度ベースのアルゴリズムなどの古典的な推薦器よりも優れた性能をもたらすことが示された。