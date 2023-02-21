## 0.1. link

- [元論文](https://arxiv.org/abs/1811.12591)

## 0.2. title

Active Learning in Recommendation Systems with Multi-level User Preferences

## 0.3. abstract

While recommendation systems generally observe user behavior passively, there has been an increased interest in directly querying users to learn their specific preferences. In such settings, considering queries at different levels of granularity to optimize user information acquisition is crucial to efficiently providing a good user experience. In this work, we study the active learning problem with multi-level user preferences within the collective matrix factorization (CMF) framework. CMF jointly captures multi-level user preferences with respect to items and relations between items (e.g., book genre, cuisine type), generally resulting in improved predictions. Motivated by finite-sample analysis of the CMF model, we propose a theoretically optimal active learning strategy based on the Fisher information matrix and use this to derive a realizable approximation algorithm for practical recommendations. Experiments are conducted using both the Yelp dataset directly and an illustrative synthetic dataset in the three settings of personalized active learning, cold-start recommendations, and noisy data -- demonstrating strong improvements over several widely used active learning methods.
推薦システムは一般的にユーザーの行動を受動的に観察するが、ユーザーの具体的な嗜好を知るために直接クエリを発行することに関心が高まっている. このような設定において、ユーザ情報の取得を最適化するために、異なる粒度での問い合わせを考慮することは、効率的に良いユーザ体験を提供するために極めて重要である. 本研究では、集合的行列分解(CMF)の枠組みで、複数レベルのユーザ嗜好を持つ能動学習問題を研究する. CMFは、項目と項目間の関係（例えば、本のジャンル、料理の種類）に関して、多レベルのユーザの嗜好を共同で捉え、一般に予測精度を向上させることができる. CMFモデルの有限サンプル解析に基づき、フィッシャー情報行列に基づく理論的に最適な能動学習戦略を提案し、これを用いて実用的な推薦のための実現可能な近似アルゴリズムを導出する. Yelpのデータセットと合成データセットを用いて、個人化能動学習、コールドスタート推薦、ノイズデータという3つの設定で実験を行った結果、広く用いられているいくつかの能動学習手法よりも強い改善効果があることが示された.

# 1. Introduction

Recommendation systems are widely studied in both academic and commercial settings. Most existing work considers the passive, item-level feedback scenario where the recommendation system observes historical user feedback for a set of items with respect to a population of users and estimates unobserved user-item utility to make recommendations. However, exclusively considering item-level feedback disregards frequently available information regarding relations (i.e., cuisine type, product substitutability (McAuley, Pandey, and Leskovec 2015)) between entities (i.e., items, users, cuisines, etc.) in the database. Additionally, standard recommendation systems only observe historical user-item responses to estimate model parameters, unlike active learning systems that are able to directly query the user to more efficiently learn user preferences. Noting these shortcomings, online recommendation systems (Bresler, Chen, and Shah 2014), preference elicitation methods (Chen and Karger 2006), and interactive recommendation systems (Mahmood and Ricci 2009) all provide directions to mitigate these issues.
推薦システムは、学術的、商業的に広く研究されている。ほとんどの既存研究は、推薦システムがユーザ集団に関するアイテムセットに対する過去のユーザフィードバックを観察し、未観測のユーザアイテム効用を推定して推薦を行う、受動的なアイテムレベルのフィードバックシナリオを考慮している。しかし、アイテムレベルのフィードバックのみを考慮すると、データベース内のエンティティ（すなわち、アイテム、ユーザー、料理など）間の関係（すなわち、料理の種類、製品の代替性（McAuley、Pandey、およびLescovec 2015））に関する頻繁に利用できる情報を無視することになる。さらに、標準的な推薦システムは、モデルパラメータを推定するために過去のユーザー・アイテムの反応を観察するだけであり、ユーザーの嗜好をより効率的に学習するためにユーザーに直接問い合わせることができる能動学習システムとは異なります。これらの欠点に着目し、オンライン推薦システム（Bresler, Chen, and Shah 2014）、嗜好抽出手法（Chen and Karger 2006）、対話型推薦システム（Mahmood and Ricci 2009）はいずれもこれらの問題を軽減するための方向性を示している。

In this work, we are specifically interested in adding system-initiative capabilities with respect to querying the user. As motivation, suppose you are interested in purchasing book to read during an upcoming vacation. A standard recommendation system would observe your past purchases/ratings and select a book expected to align with learned preferences. However, a multi-turn dialogue agent may be able to ask preference questions of varying types and levels of granularity (i.e., Did you like G.K. Chesterton’s ‘The Man Who Was Thursday’? [item utility elicitation], Are you looking for light reading? [use case information], Do you like science fiction novels? [category information]). These query families result in greater flexibility than simply making recommendations and allow asking questions that can more quickly improve the model for making session-specific recommendations.
この作業では、特に、ユーザーへの問い合わせに関して、システム主導の機能を追加することに関心があります。例えば、あなたが今度の休暇に読む本を買おうとしているとする。標準的な推薦システムは、あなたの過去の購入履歴や評価を観察し、学習した嗜好に合うと思われる本を選択する。しかし、多回答型対話エージェントは、様々な種類と粒度の嗜好質問をすることができるかもしれない（例えば、G.K. Chestertonの「木曜日になった男」が好きですか？[項目実用性誘発]、軽い読書をお探しですか？[ユースケース情報]、「SF小説は好きですか？[カテゴリ情報])。これらのクエリファミリは、単に推薦を行うよりも大きな柔軟性をもたらし、セッション固有の推薦を行うためのモデルをより迅速に改善できるような質問を行うことを可能にする。

The core of our proposed method is an active learning extension to the collective matrix factorization (CMF) model. CMF produces a low-dimensional embedding that is shared across each relation for which the item/user participates and jointly represents all available sources of information on different levels (Gupta and Singh 2015). By enabling active learning within CMF, we can generate a personalized active learning session to efficiently estimate the CMF parameters and make high-quality recommendations. Our primary contributions include: (1) framing the question selection problem for multi-level user preferences in a system-initiative active recommendation system within the CMF framework (2) providing a theoretical analysis of an optimal active learning strategy for CMF and corresponding realizable approximation and (3) demonstrating that the proposed algorithm outperforms strong baselines on real-world Yelp data and an illustrative synthetic dataset that explicitly satisfies the CMF assumptions in standard, cold start, and noisy data settings.
我々の提案する手法の中核は、集団的行列分解（CMF）モデルの能動的学習による拡張である。CMFは、アイテム／ユーザーが参加する各関係にわたって共有される低次元の埋め込みを生成し、異なるレベルのすべての利用可能な情報源を共同で表現する（Gupta and Singh 2015）。CMF内で能動学習を可能にすることで、パーソナライズされた能動学習セッションを生成し、CMFパラメータを効率的に推定し、高品質のレコメンデーションを行うことができます。我々の主な貢献は以下の通りである。(1)システム起動型能動推薦システムにおけるマルチレベルのユーザー嗜好に対する質問選択問題をCMFフレームワーク内で構成すること (2)CMFに対する最適な能動学習戦略と対応する実現可能な近似についての理論分析を提供し、 (3)提案アルゴリズムが実世界Yelpデータおよび標準、コールドスタート、ノイズデータ設定においてCMF仮定を明示的に満足する例示合成データにおいて強力なベースラインより優れていることを実証すること。

# 2. Related Works

This work draws upon several existing research areas. Below, we itemize some of the most relevant related work.
この研究は、いくつかの既存の研究領域を利用している。以下に、最も関連性の高い研究分野を列挙する。

## 2.1. Recommendation Systems:

Recommendation systems are frequently categorized as content-based (Pazzani and Billsus 2007) or collaborative filtering (Koren, Bell, and Volinsky 2009) methods. This work builds upon the collective matrix factorization (CMF) model (Singh and Gordon 2008; Gupta and Singh 2015), a collaborative filtering method that generalizes matrix factorization to also account for different levels of relations between entities. Within the collaborative filtering approach, observation sparsity is the primary limitation, particularly in the cold start setting (i.e., where a new item has a small number of ratings or a new user has rated a small number of items). Approaches to ameliorate this issues include user preference elicitation (Rashid, Karypis, and Riedl 2008), interview construction (Zhou, Yang, and Zha 2011; Sun et al. 2013), and optimal experimental design (Anava et al. 2015). The distinguishing aspect of our work is that we develop an active and personalized querying strategy that jointly accounts for several types of questions based on item preferences and other relationships between entities.
推薦システムはコンテンツベース（Pazzani and Billsus 2007）や協調フィルタリング（Koren, Bell, and Volinsky 2009）方式に分類されることが多い。この作品は、エンティティ間の関係の異なるレベルも考慮するために行列分解を一般化する協調フィルタリング法である集団行列分解（CMF）モデル（Singh and Gordon 2008; Gupta and Singh 2015）をベースにしている。協調フィルタリングアプローチの中で、観測のスパース性は、特にコールドスタート設定（すなわち、新しいアイテムが少数の評価を有するか、新しいユーザーが少数のアイテムを評価した場合）において、主要な制限となる。この問題を改善するアプローチとして、ユーザーの嗜好の引き出し（Rashid, Karypis, and Riedl 2008）、インタビューの構築（Zhou, Yang, and Zha 2011; Sun et al.2013）、最適実験デザイン（Anava et al.2015）などがある。我々の研究の特徴は、項目の嗜好やエンティティ間の他の関係に基づいて、いくつかのタイプの質問を共同で説明する能動的かつパーソナライズされたクエリ戦略を開発することである。

## 2.2. Active Learning:

Active learning has been widely studied (e.g., (Settles 2009) for a general survey, (Rubens, Kaplan, and Sugiyama 2011; Elahi, Ricci, and Rubens 2016) in the context of recommendation systems), describing when a learning algorithm observes a large set (or stream) of unlabeled examples and can choose a subset for labeling – attempting to maximize performance while minimizing annotation effort. The most closely related work within the recommendation systems setting is active learning in the matrix completion scenario (Bhargava, Ganti, and Nowak 2017). While related, this differs from our work as we use the CMF setting to jointly estimate a representation for several levels of relationships. From a methodological perspective, our work draws upon recent results for active learning with Fisher information based querying functions (Sourati et al. 2017) and convergence properties of active learning for maximum likelihood estimation (Chaudhuri et al. 2015). We expand upon these results for the CMF setting.
能動学習は広く研究されており（例えば、一般的な調査として（Settles 2009）、推薦システムの文脈では（Rubens, Kaplan, and Sugiyama 2011; Elahi, Ricci, and Rubens 2016））、学習アルゴリズムがラベルのない例の大きなセット（またはストリーム）を観察し、ラベルのためのサブセットを選択できる場合について記述し、注釈作業を最小化しながら性能を最大化しようとするものである。推薦システムの設定内で最も密接に関連する仕事は、行列補完シナリオにおける能動学習です（Bhargava, Ganti, and Nowak 2017）。関連はしているが、これは、CMF設定を使用して、いくつかのレベルの関係の表現を共同で推定するため、我々の仕事とは異なる。方法論の観点から、我々の仕事は、フィッシャー情報ベースのクエリ関数を用いた能動学習に関する最近の結果（Sourati et al.2017） と、最尤推定に関する能動学習の収束特性（Chaudhuri et al.2015） を利用している。これらの結果をCMFの設定に拡張する。

## 2.3. Conversational Agents: 会話型エージェント

One potential motivation for this work is conversational recommendations (Mahmood and Ricci 2009; Christakopoulou, Radlinski, and Hofmann 2016), where questions are determined by modeling different relationship types within a unified framework and a theoretically well-motivated active learning strategy. However, it should be noted that developing goal-oriented conversational agents (e.g., (Young et al. 2013)) and specifically dialogue managers is a very mature AI subfield. We are only considering the restricted setting of asking a personalized set of questions to provide an optimized recommendation.
この研究の潜在的な動機の一つは、会話型推薦（Mahmood and Ricci 2009; Christakopoulou, Radlinski, and Hofmann 2016）で、質問は、統一フレームワークと理論的によく動機付けられた能動学習戦略内の異なる関係タイプのモデル化によって決定される。しかし、目標指向の会話エージェント（例えば、（Young et al. 2013））、特に対話マネージャの開発は、非常に成熟したAIサブフィールドであることに留意する必要があります。我々は、最適化された推薦を提供するために、個人化された質問セットを尋ねるという限定的な設定のみを考えている。

# 3. Preliminaries and Model

We first briefly review the probabilistic collective matrix factorization model (Singh and Gordon 2008) and concretely formalize our active learning extension.
まず、確率的集団的行列分解モデル(Singh and Gordon 2008)を簡単にレビューし、我々の能動学習拡張を具体的に形式的に説明する。

## 3.1. General Notation

We use lower case letters to denote scalars and vectors, upper case letters to denote matrices and sets. I is an appropriately sized identity matrix. Superscript $^T$ denotes a vector or matrix transpose and $|·|$ denotes the support size of a set. The $l_2-norm$ of a vector $x \in R^k$ is defined as $|x|^2 = \sqrt{\sum_{i=1}^k x_i^2}$ where $|x|_A=\sqrt{x^T Ax}$ is defined for a vector x and a matrix A of appropriate dimensions. The Frobenius norm of a matrix $A \in R^{m\times n}$ is defined as $|A|_F = \sqrt{\sum_{i=1}^{m} \sum_{j=1}^{n}|A_{ij}|^2}$.
スカラーやベクトルは小文字で、行列や集合は大文字で表します。I は適当な大きさの単位行列である. 上付き文字$^T$はベクトルまたは行列の転置、$|-|$は集合のサポートサイズであることを表す。ベクトル $x \in R^k$ の $l_2-norm$ は $|x|^2 = \sqrt{sum_{i=1}^k x_i^2}$ で定義され、 $|x|_A=theirsqrt{x^T Ax}$ はベクトル x と適当な次元の行列 A に対して定義されます。また、行列$A \in R^{m}times n}$のフロベニウスノルムは$|A|_F = \sqrt{{sum_{i=1}^{m}} で定義されます。\sum_{j=1}^{n}|A_{ij}|^2}$.

## 3.2. Relational Data

We represent the set of entities by $E$ and the set of relations between them by R, respectively. Denote the observed database by D, which consists of tuples of the form ${r_i , e^{(1)}_i , e^{(2)}_i, y_i}_{i=1}^N$, where $r_i \in R$ is a relation between two different types of entities, $e^{(1)}_i , e^{(2)}_i \in E$ are a pair of different entities, $y_i \in {±1}$ is the label denoting whether $r_i(e^{(1)}_i , e^{(2)}_i)$ holds (or not), and N is the total number of observed relations in database D.
実体の集合を$E$、実体の間の関係の集合をRでそれぞれ表現する。観測されたデータベースをDとすると、Dは${r_i , e^{(1)}_i , e^{(2)}_i, y_i}_{i=1}^N$ の形のタプルからなり、$r_i \in R$は2種類の異なる実体間の関係、$e^{(1)}_i , e^{(2)}_i \in E$は異なる実体の組、$y_i \in {±1}$ は $r_i(e^{(1)}_i , e^{(2)}_i)$ が成り立つかどうかを示すラベル、NはデータベースDで観測される関係の総数である。

For example, a simple database that consists only of the user ratings for restaurants would contain users and businesses as the entities, and only a single relation r ∈ R, such that $r(e^{(U)}_i, e^{(B)}_i) = 1$ if the user $e^{(U)}_i$ liked the business $e^{(B)}_i$. As in this example, many real-life databases are sparse (i.e., only a very small subset of possible relations are observed) and the goal of modeling is to be able to complete this database such that we can make recommendation based on the prediction. Specifically, given any query $r_q(e^{(1)}_q, e^{(2)}_q)$ that is absent from the observed database, we would like to predict whether the relation holds.
例えば、レストランに対するユーザの評価のみからなる単純なデータベースは、ユーザと企業を実体として含み、ユーザ$e^{(U)}_i$が企業$e^{(B)}_i$を好きなら$r(e^{(U)}_i, e^{(B)}_i) = 1$という単一の関係 r∈R のみである。この例のように、現実の多くのデータベースは疎であり（すなわち、可能な関係の非常に小さなサブセットしか観測されない）、モデリングの目標は、予測に基づいて推薦を行うことができるように、このデータベースを完成させることができるようになることである。具体的には、観測されたデータベースに存在しない任意のクエリ $r_q(e^{(1)}_q, e^{(2)}_q)$ が与えられたとき、その関係が成立するかどうかを予測したいと思う。

## 3.3. Collective Factorization Model

The collective matrix factorization model (Singh and Gordon 2008; Gupta and Singh 2015) extends the commonly used matrix factorization model to multiple matrices by assigning each entity a low-dimensional latent vector that is shared across all relations where the entity appears. Formally, we assign each entity $e \in E$ in our database a kdimensional latent vector $\phi_e \in R^k$, and denote the matrix of all such latent vectors by $\Phi \in R^{k×|E|}$. We model the probability that $r_i(e^{(1)}_i, e^{(2)}_i)$ equals to $y_i$ by:
集団的行列分解モデル（Singh and Gordon 2008; Gupta and Singh 2015）は、各エンティティに、そのエンティティが出現する全ての関係で共有される低次元の潜在ベクトルを割り当てることで、一般的に用いられる行列分解モデルを複数の行列に拡張したものである。具体的には、データベース内の各実体$e \in E$にk次元の潜在ベクトル$phi_e \in R^k$を割り当て、その潜在ベクトル全ての行列を$Phi \in R^{k×|E}$と表現する。r_i(e^{(1)}\_i, e^{(2)}\_i)$ が $y_i$ と等しくなる確率を以下のようにモデル化する。

$$
P_{\Phi}[r_i(e_i^{(1)}, e_i^{(2)}) = y_i] = \sigma(y_i \cdot \phi_{e_i}^{(1)T} \cdot \phi_{e_i}^{(2)})
\tag{1}
$$

where σ is the sigmoid function.

The CMF model presents a number of advantages in our setting. By sharing the entity factors amongst all the relations, we are able to produce a joint representation based on all sources of information on different levels. For example, the factors used predict user ratings will leverage information from other ratings in a collaborative filtering fashion, from business categories via the set inclusion relationships, and even from words that appear in the reviews (the details of the model as applied to the Yelp data are described in Section 5.1). By developing this joint representation, it also allows the active learning algorithm to query different type of personalized questions to different users in multi-turn recommendation system settings. A further advantage of learning CMF model is that all the entities are effectively embedded in the same k-dimensional space, and thus similarities and distances can be computed and analyzed for any set of entities. Finally, test-time inference takes constant time and thus is very efficient: we only require a dot-product between low-dimensional vectors for estimating the probability of a relation existing between a pair of entities.
CMFモデルは、我々の設定において多くの利点を提供する。すべての関係間でエンティティファクターを共有することで、異なるレベルのすべての情報源に基づく共同表現を生成することができる。例えば、ユーザー評価を予測するために使用される要因は、協調フィルタリング方式で他の評価から、セット包含関係を通じてビジネスカテゴリから、さらにはレビューに現れる単語から情報を活用する（Yelpデータに適用したモデルの詳細は、セクション5.1で説明されている）。このような共同表現を開発することで、アクティブラーニングアルゴリズムは、マルチターン推薦システムの設定において、異なるユーザーに対して異なるタイプのパーソナライズされた質問を問い合わせることも可能となる。さらに、CMFモデルの学習の利点は、すべての実体が同じk次元空間に効果的に埋め込まれるため、任意の実体の集合に対して類似性と距離を計算し、分析することができることである。最後に、テスト時推論は一定の時間を要するため、非常に効率的である。我々は、一対の実体の間に関係が存在する確率を推定するために、低次元ベクトル間のドットプロッドを必要とするだけである。

## 3.4. Problem Definition

$$
L_{S_u}(\Phi) = E_{\Phi}
$$

# 4. Algorithm and Analysis

## 4.1. Maximum Likelihood Estimation

## 4.2. Active Learning Based on Error Bound Minimization

# 5. Experimental setup

## 5.1. Yelp Datase

## 5.2. CMF Generated Synthetic Dataset

## 5.3. Baseline Algorithms

## 5.4. Active Learning Setup

# 6. Experimental Results

## 6.1. Personalized Active Learning

## 6.2. Cold Start Setting

## 6.3. Noise Tolerance

# 7. Conclusions
