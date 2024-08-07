## link リンク

- https://dl.acm.org/doi/pdf/10.1145/3178876.3185994 https://dl.acm.org/doi/pdf/10.1145/3178876.3185994

## title タイトル

DRN: A Deep Reinforcement Learning Framework for News Recommendation
DRN：ニュース推薦のための深層強化学習フレームワーク

## abstract アブストラクト

In this paper, we propose a novel Deep Reinforcement Learning framework for news recommendation
本論文では、ニュース推薦のための新しいDeep Reinforcement Learningのフレームワークを提案する
Online personalized news recommendation is a highly challenging problem due to the dynamic nature of news features and user preferences
オンラインパーソナライズドニュースレコメンデーションは、ニュースの特徴やユーザーの好みがダイナミックに変化するため、非常に難しい問題である
Although some online recommendation models have been proposed to address the dynamic nature of news recommendation, these methods have three major issues
ニュース推薦の動的な性質に対応するために、いくつかのオンライン推薦モデルが提案されているが、これらの方法には次の3つの大きな問題がある。
First, they only try to model current reward (e.g., Click Through Rate)
まず、現在の報酬（クリックスルー率など）をモデル化しようとするだけである
Second, very few studies consider to use user feedback other than click / no click labels (e.g., how frequent user returns) to help improve recommendation
第二に、レコメンデーションの改善に、クリック/クリックなしラベル以外のユーザーフィードバック（例えば、ユーザーの再訪頻度）を利用することを検討した研究はほとんどありません。
Third, these methods tend to keep recommending similar news to users, which may cause users to get bored
第三に、これらの方法は、ユーザーに似たようなニュースを推薦し続ける傾向があり、ユーザーが飽きてしまう可能性がある。
Therefore, to address the aforementioned challenges, we propose a Deep Q-Learning based recommendation framework, which can model future reward explicitly
そこで、本研究では、将来の報酬を明示的にモデル化できるDeep Q-Learningを用いた推薦フレームワークを提案することで、前述の課題を解決する。
We further consider user return pattern as a supplement to click / no click label in order to capture more user feedback information
さらに、クリック/クリックなしのラベルを補完するものとして、ユーザーのリターンパターンを考慮することで、より多くのユーザーフィードバック情報を取得することができます。
In addition, an effective exploration strategy is incorporated to find new attractive news for users
さらに、ユーザーにとって魅力的なニュースを新たに発見するために、効果的な探索戦略を取り入れています
Extensive experiments are conducted on the offline dataset and online production environment of a commercial news recommendation application and have shown the superior performance of our methods.
商業用ニュース推薦アプリケーションのオフラインデータセットとオンライン制作環境において広範な実験を行い、本手法の優れた性能を示しました。

# Introduction 序章

The explosive growth of online content and services has provided tons of choices for users
オンラインコンテンツやサービスの爆発的な増加により、ユーザーの選択肢は膨大になりました。
For instance, one of the most popular online services, news aggregation services, such as Google News [15] can provide overwhelming volume of content than the amount that users can digest
例えば、最も人気のあるオンラインサービスの一つであるGoogle News [15]のようなニュースアグリゲーションサービスは、ユーザーが消化できる量よりも圧倒的な量のコンテンツを提供します。
Therefore, personalized online content recommendation are necessary to improve user experience.
そのため、ユーザー体験を向上させるために、パーソナライズされたオンラインコンテンツの推奨が必要です。

Several groups of methods are proposed to solve the online personalized news recommendation problem, including content based methods [19, 22, 33], collaborative filtering based methods [11, 28,34], and hybrid methods [12, 24, 25]
オンラインパーソナライズドニュースの推薦問題を解決するために、コンテンツベースの手法[19, 22, 33]、協調フィルタリングに基づく手法[11, 28, 34]、ハイブリッド手法[12, 24, 25]など、いくつかの手法群が提案されている。
Recently, as an extension and integration of previous methods, deep learning models [8, 45, 52] have become the new state-of-art methods due to its capability of modeling complex user item (i.e., news) interactions
近年、従来の手法の拡張・統合として、ディープラーニングモデル[8, 45, 52]が、複雑なユーザーアイテム（ニュースなど）のやり取りをモデル化できることから、新たな最先端手法となっています
However, these methods can not effectively address the following three challenges in news recommendation.
しかし、これらの方法は、ニュース推薦における以下の3つの課題を効果的に解決することはできません。

First, the dynamic changes in news recommendations are difficult to handle
第一に、ニュースのレコメンデーションの動的な変化を扱うのは難しい
The dynamic change of news recommendation can be shown in two folds
ニュースレコメンデーションのダイナミックな変化は、2つの側面から示すことができる。
First, news become outdated very fast
第一に、ニュースはすぐに古くなる
In our dataset, the average time between the time that one piece of news is published and the time of its last click is 4.1 hours
私たちのデータセットでは、1つのニュースが公開されてから最後にクリックされるまでの平均時間は4.1時間である
Therefore, news features and news candidate set are changing rapidly
そのため、ニュースの特徴やニュース候補のセットもどんどん変化しています
Second, users’ interest on different news might evolve during time
第二に、ユーザーの様々なニュースに対する興味は、時間の経過とともに変化する可能性がある。
For instance, Figure 1 displays the categories of news that one user has read in 10 weeks
例えば、図1は、あるユーザーが10週間に読んだニュースのカテゴリーを表示したものです。
During the first few weeks, this user prefers to read about “Politics” (green bar in Figure 1), but his interest gradually moves to “Entertainment” (purple bar in Figure 1) and “Technology” (grey bar in Figure 1) over time
このユーザーは、最初の数週間は「政治」（図1の緑のバー）を好んで読んでいるが、時間の経過とともに「エンターテインメント」（図1の紫のバー）や「テクノロジー」（図1のグレーのバー）に徐々に関心が移っていく
Therefore, it is necessary to update the model periodically
そのため、定期的にモデルを更新する必要があります
Although there are some online recommendation methods [11, 24] that can capture the dynamic change of news features and user preference through online model updates, they only try to optimize the current reward (e.g., Click Through Rate), and hence ignore what effect the current recommendation might bring to the future
オンライン推薦手法の中には、オンラインモデル更新によってニュースの特徴やユーザーの嗜好の動的変化を捉えることができるものもありますが [11, 24] 、それらは現在の報酬（例えば、クリックスルー率）を最適化しようとするだけで、現在の推薦が将来にもたらすであろう影響を無視しています。
An example showing the necessity of considering future is given in Example 1.1.
未来を考える必要性を示す例として、例1.1を示します。

Example 1.1
例1.1
When a user Mike requests for news, the recommendation agent foresees that he has almost the same probability to click on two pieces of news: one about a thunderstorm alert, and the other about a basketball player Kobe Bryant
ユーザMikeがニュースを要求したとき、推薦エージェントは、雷雨警報に関するニュースと、バスケットボール選手Kobe Bryantに関するニュースの2つをクリックする確率がほぼ同じであることを予見しています
However, according to Mike’s reading preference, features of the news, and reading patterns of other users, our agent speculates that, after reading about the thunderstorm, Mike will not need to read news about this alert anymore, but he will probably read more about basketball after reading the news about Kobe
しかし、マイクの読書嗜好、ニュースの特徴、他のユーザーの読書パターンによると、雷雨のニュースを読んだ後、マイクはこの警報に関するニュースを読む必要はなくなったが、コービーに関するニュースを読んだ後は、バスケットボールについてもっと読むだろうと、我々のエージェントは推測している
This suggests, recommending the latter piece of news will introduce larger future reward
これは、後者のニュースを推薦することで、より大きな報酬を得られることを示唆しています。
Therefore, considering future rewards will help to improve recommendation performance in the long run.
そのため、将来の報酬を考慮することで、長期的にレコメンデーションパフォーマンスを向上させることができるのです。

Second, current recommendation methods [23, 35, 36, 43] usually only consider the click / no click labels or ratings as users’ feedback
第二に、現在の推薦手法[23, 35, 36, 43]は、通常、クリック/クリックなしのラベルや評価をユーザーのフィードバックとして考慮するだけである。
However, how soon one user will return to this service [48] will also indicate how satisfied this user is with the recommendation
しかし、あるユーザーがどれだけ早くこのサービスに戻ってくるか[48]は、このユーザーが推薦にどれだけ満足しているかを示すことにもなる
Nevertheless, there has been little work in trying to incorporate user return pattern to help improve recommendation.
とはいえ、ユーザーの帰省パターンを取り入れてレコメンデーションの向上に役立てようという試みは、これまでほとんど行われてきませんでした。

The third major issue of current recommendation methods is its tendency to keep recommending similar items to users, which might decrease users’ interest in similar topics
現在の推薦手法の3つ目の大きな問題は、ユーザーに似たようなものを推薦し続ける傾向があるため、ユーザーの類似した話題への興味を低下させる可能性があることです
In the literature, some reinforcement learning methods have already proposed to add some randomness (i.e., exploration) into the decision to find new items
文献では、すでにいくつかの強化学習法が、新しいアイテムを見つける判断にランダム性（すなわち探索）を加えることを提案している
State-of-art reinforcement learning methods usually apply the simple ϵ-greedy strategy [31] or Upper Confidence Bound (UCB) [23, 43] (mainly for Multi-Armed Bandit methods)
最先端の強化学習法では、通常、単純な?グリーディ戦略 [31] またはUCB (Upper Confidence Bound) [23, 43] (主に多腕バンディット法) を適用します。
However, both strategies could harm the recommendation performance to some extent in a short period
しかし、どちらの戦略も、短期間では、推薦者のパフォーマンスをある程度損なう可能性があります。
ϵ-greedy strategy may recommend the customer with totally unrelated items, while UCB can not get a relatively accurate reward estimation for an item until this item has been tried several times
ϵグリーディ戦略では、全く関係のないアイテムを顧客に勧めることがあるが、UCBでは、そのアイテムが何度か試されるまでは、比較的正確な報酬推定を得ることができない。
Hence, it is necessary to do more effective exploration.
したがって、より効果的な探索を行う必要があるのです。

Therefore, in this paper, we propose a Deep Reinforcement Learning framework that can help to address these three challenges in online personalized news recommendation
そこで本論文では、オンラインパーソナライズドニュース推薦におけるこれら3つの課題を解決するのに役立つDeep Reinforcement Learningフレームワークを提案します。
First, in order to better model the dynamic nature of news characteristics and user preference, we propose to use Deep Q-Learning (DQN) [31] framework
まず、ニュースの特性やユーザーの嗜好の動的な性質をより適切にモデル化するために、Deep Q-Learning (DQN) [31] のフレームワークを使用することを提案します。
This framework can consider current reward and future reward simultaneously
このフレームワークは、現在の報酬と将来の報酬を同時に考慮することができる
Some recent attempts using reinforcement learning in recommendation either do not model the future reward explicitly (MAB-based works [23, 43]), or use discrete user log to represent state and hence can not be scaled to large systems (MDP-based works [35, 36])
強化学習を推薦に用いる最近の試みは、将来の報酬を明示的にモデル化していない（MABベースの作品[23, 43]）、あるいは、状態を表すために離散的なユーザログを用いるため、大規模システムに拡張できない（MDPベースの作品 [35, 36]）というものである。
In contrast, our framework uses a DQN structure and can easily scale up
一方、我々のフレームワークはDQN構造を採用しており、容易にスケールアップすることが可能です。
Second, we consider user return as another form of user feedback information, by maintaining an activeness score for each user
第二に、ユーザーリターンをユーザーフィードバック情報のもう一つの形態と考え、各ユーザーのアクティブネスコアを保持することである
Different from existing work [48] that can only consider the most recent return interval, we consider multiple historical return interval information to better measure the user feedback
最新のリターン間隔しか考慮できない既存の研究[48]とは異なり、我々は複数の過去のリターン間隔情報を考慮し、より適切にユーザーのフィードバックを測定することができます。
In addition, different from [48], our model can estimate user activeness at any time (not just when user returns)
また、[48]とは異なり、本モデルでは、ユーザーの活性度を（ユーザーが戻った時だけでなく）いつでも推定することができる
This property enables the experience replay update used in DQN
このプロパティは、DQN で使用される経験値再生アップデートを有効にします。
Third, we propose to apply a Dueling Bandit Gradient Descent (DBGD) method [16, 17, 49] for exploration, by choosing random item candidates in the neighborhood of the current recommender
第三に、Dueling Bandit Gradient Descent (DBGD) 法 [16, 17, 49] を適用して、現在のレコメンダーの近傍にあるアイテム候補をランダムに選び、探索することを提案する。
This exploration strategy can avoid recommending totally unrelated items and hence maintain better recommendation accuracy.
この探索戦略により、全く関係のないものを推薦することを避け、より良い推薦精度を維持することができます。

Our deep reinforcement recommender system can be shown as Figure 2
私たちの深層強化レコメンダーシステムは、図2のように示すことができます。
We follow the common terminologies in reinforcement learning [37] to describe the system
強化学習[37]の一般的な用語に従って、システムを説明する。
In our system, user pool and news pool make up the environment, and our recommendation algorithms play the role of agent
本システムでは、ユーザープールとニュースプールが環境を構成し、推薦アルゴリズムがエージェントの役割を果たします。
The state is defined as feature representation for users and action is defined as feature representation for news
状態はユーザーの特徴表現、アクションはニュースの特徴表現として定義される
Each time when a user requests for news, a state representation (i.e., features of users) and a set of action representations (i.e., features of news candidates) are passed to the agent
ユーザーがニュースを要求するたびに、状態表現（ユーザーの特徴）と行動表現のセット（ニュース候補の特徴）がエージェントに渡される
The agent will select the best action (i.e., recommending a list of news to user) and fetch user feedback as reward
エージェントは、最適なアクション（すなわち、ユーザーにニュースのリストを推薦する）を選択し、報酬としてユーザーのフィードバックを取得します。
Specifically, the reward is composed of click labels and estimation of user activeness
具体的には、報酬はクリックラベルとユーザーの活性度の推定値で構成される
All these recommendation and feedback log will be stored in the memory of the agent
これらの推奨事項やフィードバックログはすべてエージェントのメモリに保存されます。
Every one hour, the agent will use the log in the memory to update its recommendation algorithm.
1時間ごとに、エージェントはメモリ内のログを利用して推薦アルゴリズムを更新する。

Our contribution can be summarized as below:
私たちの貢献は、以下のようにまとめられます：

- We propose a reinforcement learning framework to do online personalized news recommendation. Unlike previous studies, this framework applies a DQN structure and can take care of both immediate and future reward. Although we focus on news recommendation, our framework can be generalized to many other recommendation problems. 強化学習によるオンラインパーソナライズドニュース推薦のフレームワークを提案する。 従来の研究とは異なり、このフレームワークはDQN構造を適用し、即時報酬と将来報酬の両方をケアすることができます。 ここではニュース推薦に焦点を当てているが、本フレームワークは他の多くの推薦問題に一般化することができる。

- We consider user activeness to help improve recommendation accuracy, which can provide extra information than simply using user click labels. 私たちは、推薦精度を向上させるために、単にユーザーのクリックラベルを使用するよりも余分な情報を提供することができる、ユーザーの活性度を考慮しています。

- A more effective exploration method Dueling Bandit Gradient Descent is applied, which avoids the recommendation accuracy drop induced by classical exploration methods, e.g., ϵ-greedy and Upper Confidence Bound. より効果的な探索手法であるDueling Bandit Gradient Descentを適用することで、ϵ-greedyやUpper Confidence Boundといった従来の探索手法で引き起こされる推薦精度の低下を回避しています。

- Our system has been deployed online in a commercial news recommendation application. Extensive offline and online experiments have shown the superior performance of our methods. 本システムは、商用ニュース推薦アプリケーションでオンライン展開されました。 オフラインとオンラインの広範な実験により、本手法の優れた性能が示されました。

The rest of the paper is organized as follows
本稿の残りの部分は、以下のように構成されています。
Related work is discussed in Section 2
関連作品については第2節で説明します。
Then, in Section 3 we present the problem definitions
そして、第3節では、問題定義を示す
Our method is introduced in Section 4
私たちの方法は、セクション4で紹介されています。
After that, the experimental results are shown in Section 5
その後、第5節で実験結果を示す。
Finally, brief conclusions are given in Section 6.
最後に、セクション6で簡単な結論が述べられている。

# Related Work 関連作品

## News recommendation algorithms ニュース推薦アルゴリズム

Recommender systems [3, 4] have been investigated extensively because of its direct connection to profits of products
レコメンダーシステム[3,4]は、商品の利益に直結するため、広く研究されています。
Recently, due to the explosive grow of online content, more and more attention has been drawn to a special application of recommendation – online personalized news recommendation
近年、オンラインコンテンツの爆発的な増加に伴い、推薦の特殊なアプリケーションであるオンラインパーソナライズドニュースレコメンデーションが注目されています。
Conventional news recommendation methods can be divided into three categories
従来のニュース推薦手法は、以下の3つに分類されます。
Content-based methods [19, 22, 33] will maintain news term frequency features (e.g., TF-IDF) and user profiles (based on historical news)
コンテンツベースの手法[19, 22, 33]は、ニュースの用語頻度特徴（例：TF-IDF）とユーザープロファイル（過去のニュースに基づく）を保持します。
Then, recommender will select news that is more similar to user profile
そして、レコメンダーは、ユーザーのプロファイルに近いニュースを選択します。
In contrast, collaborative filtering methods [11] usually make rating prediction utilizing the past ratings of current user or similar users [28, 34], or the combination of these two [11]
一方、協調フィルタリング法[11]は、通常、現在のユーザーや類似のユーザーの過去の評価[28, 34]、またはこれらの組み合わせ[11]を利用して評価予測を行う。
To combine the advantages of the former two groups of methods, hybrid methods [12, 24, 25] are further proposed to improve the user profile modeling
前者の2つの手法の長所を組み合わせるために、ユーザープロファイルのモデリングを改善するハイブリッド手法 [12, 24, 25] がさらに提案されています。
Recently, as an extension and integration of previous methods, deep learning models [8, 45, 52] have shown much superior performance than previous three categories of models due to its capability of modeling complex user-item relationship
近年、従来の手法を拡張・統合した深層学習モデル[8, 45, 52]は、複雑なユーザーとアイテムの関係をモデル化できるため、従来の3種類のモデルよりはるかに優れた性能を示しています。
Different from the effort for modeling the complex interaction between user and item, our algorithm focuses on dealing with the dynamic nature of online news recommendation, and modeling of future reward
ユーザーとアイテムの複雑な相互作用をモデル化する努力とは異なり、我々のアルゴリズムはオンラインニュース推薦の動的な性質に対処し、将来の報酬をモデル化することに重点を置いています。
However, these feature construction and user-item modeling techniques can be easily integrated into our methods.
しかし、これらの特徴構築技術やユーザーアイテムモデリング技術は、我々の手法に容易に統合することができる。

## Reinforcement learning in recommendation レコメンデーションにおける強化学習

### Contextual Multi-Armed Bandit models. 文脈的多腕バンディットモデル。

A group of work [5, 7, 23, 40, 44, 50] begin to formulate the problem as a Contextual Multi-Armed Bandit (MAB) problem, where the context contains user and item features
ある研究グループ [5, 7, 23, 40, 44, 50] は、コンテキストにユーザーとアイテムの特徴を含むコンテキスト型マルチアームドバンディット (MAB) 問題として問題を定式化し始めた。
[23] assumes the expected reward is a linear function of the context
[23]では、期待報酬がコンテキストの線形関数であると仮定しています。
[39] uses an ensemble of bandits to improve the performance, [40] proposes a parameter-free model, and [50] addresses the time-varying interest of users
[39]ではバンディットのアンサンブルを使用して性能を向上させ、[40]ではパラメータフリーモデルを提案し、[50]ではユーザーの時間的に変化する興味に対処しています
Recently, some people try to combine bandit with clustering based collaborative filtering [14], and matrix factorization [6, 21, 32, 42, 43, 51], in order to model more complex user and item relationship, and utilize the social network relationship in determining the reward function
最近、バンディットとクラスタリングベースの協調フィルタリング[14]、行列分解[6, 21, 32, 42, 43, 51]を組み合わせて、より複雑なユーザーとアイテムの関係をモデル化し、報酬関数の決定に社会ネットワークの関係を利用しようとする人たちがいる。
However, our model is significantly different from these works, because by applying Markov Decision Process, our model is able to explicitly model future rewards
しかし、我々のモデルは、マルコフ決定過程を適用することで、将来の報酬を明示的にモデル化することができるため、これらの作品とは大きく異なる。
This will benefit the recommendation accuracy significantly in the long run.
これは、長い目で見れば、推薦精度に大きなメリットをもたらします。

### Markov Decision Process models. マルコフ決定過程モデル。

There are also some literature trying to use Markov Decision Process to model the recommendation process
また、マルコフ決定過程を用いて推薦プロセスをモデル化しようとする文献もあります。
In contrast to MAB-based methods, MDP-based methods can not only capture the reward of current iteration, but also the potential reward in the future iterations
MABベースの手法とは対照的に、MDPベースの手法は、現在の反復の報酬だけでなく、将来の反復における潜在的な報酬も把握することができます。
[26, 27, 35, 36, 38] try to model the item or n-gram of items as state (or observation in Partially Observed MDP), and the transition between items (recommendation for the next item) as the action
[26, 27, 35, 36, 38] は、アイテムまたはアイテムの n-gram を状態（Partially Observed MDP では観測）、アイテム間の遷移（次のアイテムへの推薦）をアクションとしてモデル化することを試みています。
However, this can not scale to large dataset, because when the item candidate set becomes larger, the size of state space will grow exponentially
しかし、アイテム候補が大きくなると、状態空間のサイズが指数関数的に大きくなるため、大規模なデータセットに対応することはできません。
In addition, the state transitions data is usually very sparse, and can only be used to learn the model parameters corresponding to certain state transitions
また、状態遷移のデータは通常非常に疎なため、特定の状態遷移に対応するモデルパラメータを学習するためにのみ使用することができる
Therefore, the model is really hard to learn
そのため、モデルの学習は本当に難しい
Different from the literature, we propose a MDP framework with continuous state and action representation, which enables the system to scale up and the effective learning of model parameters by using all the state, action, reward tuples.
本論文では、連続的な状態・行動表現を持つMDPフレームワークを提案し、システムのスケールアップと、状態・行動・報酬のタプルをすべて使用することによるモデルパラメータの効果的な学習を可能にする。

# Problem Definition 問題の定義

We define our problem as follows:
問題を以下のように定義する：

When a user u sends a news request to the recommendation agent G at time t, given a candidate set I of news, our algorithm is going to select a list L of top-k appropriate news for this user
時刻tにユーザuが推薦エージェントGにニュース要求を送信したとき、ニュースの候補セットIが与えられると、我々のアルゴリズムは、このユーザにとって適切なニュースのトップkのリストLを選択しようとするものです
The notations used in this paper are summarized in Table 1.
本稿で使用する表記を表1にまとめた。

# Method メソッド

Personalized news recommendation has attracted a lot of attention in recent years [11, 23, 45]
近年、パーソナライズされたニュース推薦が注目されています[11, 23, 45] 。
The current methods can be generally categorized as content based methods [19, 22, 33], collaborative filtering based methods [11, 28, 34], and hybrid methods [12, 24, 25]
現在の方法は、一般的にコンテンツベースの方法[19、22、33]、協調フィルタリングベースの方法[11、28、34]、ハイブリッド方法[12、24、25]に分類することができます。
Recently, many deep learning models [8, 45, 52] are further proposed in order to model more complex user item interactions
近年、より複雑なユーザーアイテムのインタラクションをモデル化するために、多くの深層学習モデル[8, 45, 52]がさらに提案されている
News recommendation problem becomes even more challenging when it happens in an online scenario due to three reasons
ニュース推薦の問題は、オンラインシナリオで発生した場合、以下の3つの理由により、さらに困難となります。
First, online learning are needed due to the highly dynamic nature of news characteristics and user preference
第一に、ニュースの特性やユーザーの嗜好が非常に動的であるため、オンライン学習が必要であること
Second, only using click / no click labels will not capture users’ full feedback towards news
第二に、クリック/クリックなしのラベルを使用するだけでは、ニュースに対するユーザーのフィードバックを完全に把握することはできません。
Third, traditional recommendation methods tend to recommend similar items and will narrow down user’s reading choices
第三に、従来の推薦方法は、類似したものを推薦する傾向があり、ユーザーの読書の選択肢を狭めることになる
This will make users bored and lead to decrease of user satisfaction in the long run.
これでは、ユーザーは飽きてしまい、長期的にはユーザー満足度の低下につながってしまいます。

To address these three challenges, we propose a DQN-based Deep Reinforcement Learning framework to do online personalized news recommendation
これら3つの課題を解決するために、我々はDQNベースの深層強化学習フレームワークを提案し、オンラインパーソナライズドニュース推薦を行う。
Specifically, we use a continuous state feature representation of users and continuous action feature representation of items as the input to a multi-layer Deep Q-Network to predict the potential reward (e.g., whether user will click on this piece of news)
具体的には、ユーザーの連続状態特徴表現とアイテムの連続行動特徴表現を多層Deep Q-Networkの入力として、潜在的な報酬（例えば、ユーザーがこのニュースをクリックするかどうか）を予測します。
First, this framework can deal with the highly dynamic nature of news recommendation due to the online update of DQN
第一に、このフレームワークは、DQNのオンラインアップデートにより、ニュース推薦の非常にダイナミックな性質に対応することができます。
Meanwhile, DQN is different from common online methods, because of its capability to speculate future interaction between user and news
一方、DQNは一般的なオンライン手法とは異なり、ユーザーとニュースとの間の将来の相互作用を推測する機能を備えている。
Second, we propose to combine user activeness (i.e., how frequent a user returns to the App after one recommendation) and click labels as the feedback from users
次に、ユーザーからのフィードバックとして、ユーザーのアクティブ度（1回のレコメンデーション後にアプリに戻る頻度）とクリックラベルを組み合わせることを提案します。
Third, we propose to apply Dueling Bandit Gradient Descent exploration strategy [16, 49] to our algorithm which can both improve recommendation diversity and avoid the harm to recommendation accuracy induced by classical exploration strategies like ϵ-greedy [31] and Upper Confidence Bound [23].
これは、推薦の多様性を向上させ、?-greedy [31] や Upper Confidence Bound [23] のような古典的な探索戦略によって引き起こされる推薦精度への害を回避することができます。

Our method is significantly different from the MAB group of methods [5, 7, 23, 40, 44, 50] due to its explicit modeling of future rewards, and different from previous MDP methods [27, 35, 36, 38] using user log due to its continuous representation of state and action, and the capability to scale to large systems.
本手法は、将来の報酬を明示的にモデル化しているため、MABグループの手法 [5, 7, 23, 40, 44, 50] とは大きく異なり、状態と行動を連続的に表現し、大規模システムに拡張できるため、ユーザログを用いた従来のMDP手法 [27, 35, 36, 38] とも異なる。

In this section, we will first introduce the model framework in Section 4.1
本節では、まず、4.1 節でモデルの枠組みを紹介し
Then, we will illustrate the feature construction in Section 4.2 and the deep reinforcement learning model in Section 4.3
そして、4.2節で特徴量の構築、4.3節で深層強化学習モデルの説明を行う。
After that, the design of user activeness consideration is discussed in Section 4.4
その後、ユーザーの活性度を考慮したデザインについて、4.4節で
Finally, the exploration module is introduced in Section 4.5.
最後に、4.5節で探査モジュールを紹介する。

## Model framework モデルフレームワーク

As shown in Figure 3, our model is composed of offline part and online part
図3に示すように、我々のモデルはオフラインパートとオンラインパートで構成されている。
In offline stage, four kinds of features (will be discussed in Section 4.2) are extracted from news and users
オフラインの段階では、ニュースやユーザーから4種類の特徴（4.2節で説明します）を抽出します。
A multi-layer Deep Q-Network is used to predict the reward (i.e., a combination of user-news click label and user activeness) from these four kinds of features
多層のDeep Q-Networkを用いて、これら4種類の特徴量から報酬（ユーザーニュースのクリックラベルとユーザーの活性度の組み合わせ）を予測する。
This network is trained using the offline user-news click logs
このネットワークは、オフラインのユーザー・ニュースのクリックログを利用して学習されます
Then, during the online learning part, our recommendation agent G will interact with users and update the network in the following way:
そして、オンライン学習パートでは、推薦エージェントGがユーザーと対話し、次のようにネットワークを更新します：

- (1) PUSH: In each timestamp (t1, t2, t3, t4, t5, ...), when a user sends a news request to the system, the recommendation agent G will take the feature representation of the current user and news candidates as input, and generate a top-k list of news to recommend L. L is generated by combining the exploitation of current model (will be discussed in Section 4.3) and exploration of novel items (will be discussed in Section 4.5). (1) PUSH：各タイムスタンプ（t1, t2, t3, t4, t5, ...）において、ユーザーがシステムにニュース要求を送信すると、推薦エージェントGは、現在のユーザーの特徴表現とニュース候補を入力として、推薦すべきニュースのトップkリストを生成するL Lは、現在のモデルの活用（4.3節で説明）と新規アイテムの探索（4.5節で説明）を組み合わせて生成されます。

- (2) FEEDBACK: User u who has received recommended news L will give their feedback B by his clicks on this set of news. (2) フィードバック：推薦ニュースLを受け取ったユーザuは、このニュースセットをクリックすることで、フィードバックBを行う。

- (3) MINOR UPDATE: After each timestamp (e.g., after timestamp t1), with the feature representation of the previous user u and news list L, and the feedback B, agent G will update the model by comparing the recommendation performance of exploitation network Q and exploration network Q˜ (will be discussed in Section 4.5). If Q˜ gives better recommendation result, the current network will be updated towards Q˜ . Otherwise, Q will be kept unchanged. Minor update can happen after every recommendation impression happens. (3) MINOR UPDATE：各タイムスタンプ後（例えば、タイムスタンプt1後）、前のユーザuとニュースリストLの特徴表現とフィードバックBを用いて、エージェントGは、搾取ネットワークQと探索ネットワークQ〜の推薦性能を比較することでモデルを更新する（4.5節で説明する予定）。 Q〜がより良い推薦結果を与えた場合、現在のネットワークはQ〜に更新されます。 そうでない場合は、Qは変更されずに維持されます マイナーアップデートは、レコメンドインプレッションが発生するたびに行われます。

- (4) MAJOR UPDATE: After certain period of timeTR(e.g., after timestamp t3), agent G will use the user feedback B and user activeness stored in the memory to update the network Q. Here, we use the experience replay technique [31] to update the network. Specifically, agent G maintains a memory with recent historical click and user activeness records. When each update happens, agent G will sample a batch of records to update the model. Major update usually happens after a certain time interval, like one hour, during which thousands of recommendation impressions are conducted and their feedbacks are collected. (4) MAJOR UPDATE：一定時間TR後（例えば、タイムスタンプt3後）、エージェントGは、メモリに格納されたユーザフィードバックBとユーザアクティブネスを用いて、ネットワークQを更新する。 ここでは、経験値再生技術[31]を用いて、ネットワークの更新を行う 具体的には、エージェントGは、最近の過去のクリック記録とユーザの活性化記録をメモリに保持する。 各更新が起こると、エージェントGは、モデルを更新するためにレコードのバッチをサンプリングする メジャーアップデートは通常、1時間など一定の時間間隔をおいて行われ、その間に何千もの推薦インプレッションが実施され、そのフィードバックが収集されます。

- (5) Repeat step (1)-(4). (5) 手順(1)～(4)を繰り返す。

## Feature construction 特徴のある作り

In order to predict whether user will click one specific piece of news or not, we construct four categories of features:
ユーザーがある特定のニュースをクリックするかどうかを予測するために、4つのカテゴリーの特徴を構築する：

- News features includes 417 dimension one hot features that describe whether certain property appears in this piece of news, including headline, provider, ranking, entity name, category, topic category, and click counts in last 1 hour, 6 hours, 24 hours, 1 week, and 1 year respectively. ニュースの特徴には、見出し、提供者、ランキング、エンティティ名、カテゴリ、トピックカテゴリ、過去1時間、6時間、24時間、1週間、1年のクリック数など、このニュースに特定のプロパティが表示されているかどうかを表す417次元1ホットフィーチャーが含まれています。

- User features mainly describes the features (i.e., headline, provider, ranking, entity name, category, and topic category) of the news that the user clicked in 1 hour, 6 hours, 24 hours, 1 week, and 1 year respectively. There is also a total click count for each time granularity. Therefore, there will be totally 413 × 5 = 2065 dimensions. ユーザー特徴とは、主にユーザーが1時間、6時間、24時間、1週間、1年にそれぞれクリックしたニュースの特徴（見出し、提供者、ランキング、エンティティ名、カテゴリ、トピックカテゴリ）を記述したものです また、各時間粒度の総クリック数もあります したがって、413×5＝2065の次元が存在することになる。

- User news features. These 25-dimensional features describe the interaction between user and one certain piece of news, i.e., the frequency for the entity (also category, topic category and provider) to appear in the history of the user’s readings. ユーザーニュース機能 この25次元の特徴は、ユーザーとあるニュースとの相互作用、すなわち、ユーザーの読書履歴にそのエンティティ（カテゴリ、トピックカテゴリ、プロバイダも）が出現する頻度を表現しています。

- Context features. These 32-dimensional features describe the context when a news request happens, including time, weekday, and the freshness of the news (the gap between request time and news publish time). コンテキスト機能 この32次元の特徴量は、時間、曜日、ニュースの鮮度（リクエスト時刻とニュース公開時刻のずれ）など、ニュースリクエストが発生したときの文脈を表現しています。

In order to focus on the analysis of the reinforcement learning recommendation framework, we did not try to add more features, e.g., textual features [45]
強化学習レコメンデーションフレームワークの分析に集中するため、より多くの特徴、例えばテキスト的な特徴を追加することは試みなかった[45]。
But they can be easily integrated into our framework for better performance.
しかし、それらは、より良いパフォーマンスのために、我々のフレームワークに簡単に統合することができます。

## Deep Reinforcement Recommendation ディープ強化のすすめ

Considering the previous mentioned dynamic feature of news recommendation and the need to estimate future reward, we apply a Deep Q-Network (DQN) [31] to model the probability that one user may click on one specific piece of news
前述したニュース推薦の動的な特徴と将来の報酬を推定する必要性を考慮し、Deep Q-Network（DQN）[31]を適用して、あるユーザーがある特定のニュースをクリックする確率をモデル化する。
Under the setting of reinforcement learning, the probability for a user to click on a piece of news (and future recommended news) is essentially the reward that our agent can get
強化学習の設定では、ユーザーがニュース（および将来のおすすめニュース）をクリックする確率は、基本的に我々のエージェントが得ることができる報酬である
Therefore, we can model the total reward as Equation 1.
したがって、総報酬を式1のようにモデル化することができる。

$$
\tag{1}
$$

where state s is represented by context features and user features, action a is represented by news features and user-news interaction features, rimmed iate represents the rewards (e.g., whether user click on this piece of news) for current situation, and rf utur e represents the agent’s projection of future rewards
ここで、状態sはコンテキスト特徴とユーザ特徴、行動aはニュース特徴とユーザとニュースのインタラクション特徴、rimmed iateは現在の状況に対する報酬（例えば、ユーザがこのニュースをクリックしたかどうか）、rf utur eはエージェントの将来の報酬の予測を表している。
γ is a discount factor to balance the relative importance of immediate rewards and future rewards
γは、即時の報酬と将来の報酬の相対的な重要性をバランスさせるための割引係数である。
Specifically, given s as the current state, we use the DDQN [41] target to predict the total reward by taking action a at timestamp t as in Equation 2
具体的には、現在の状態としてsが与えられたとき、DDQN[41]ターゲットを用いて、式2のように、タイムスタンプtでアクションaを起こすことによる報酬総額を予測することができる。

$$
\tag{2}
$$

where ra,t+1 represents the immediate reward by taking action a (the subscript t + 1 is because the reward is always delayed 1 timeslot than the action)
ここで、ra,t+1 は行動 a をとることによる即時の報酬を表す（添字 t + 1 は、報酬が常に行動より1タイムスロット遅れるため）。
Here, Wt and W′ t are two different sets of parameters of the DQN
ここで、WtとW′tは、DQNの2つの異なるパラメータセットである。
In this formulation, our agent G will speculate the next state sa,t+1, given action a is selected
この定式化では、エージェントGは、行動aが選択された場合、次の状態sa,t+1を推測することになる
Based on this, given a candidate set of actions {a ′ }, the action a ′ that gives the maximum future reward is selected according to parameter Wt 
これに基づき、アクションの候補セット{a ′ }が与えられると、パラメータWtに従って、将来の報酬が最大となるアクションa ′が選択される
After this, the estimated future reward given state sa,t+1 is calculated based on W′ t 
この後、状態sa,t+1が与えられた将来の報酬の推定値をW′tに基づき算出する。
Every a few iterations, Wt and W′ t will be switched
数回繰り返すごとに、WtとW′tが入れ替わります。
This strategy has been proven to eliminate the overoptimistic value estimates of Q [41]
この戦略により、Qの過大な値推定を排除できることが証明されている[41]。
Through this process, DQN will be able to make decision considering both immediate and future situations.
このようなプロセスを経て、DQNは現在と未来の状況を考慮して意思決定を行うことができるようになるのです。

As shown in Figure 4, we feed the four categories of features into the network
図4に示すように、4つのカテゴリーの特徴をネットワークに投入します。
User features and Context features are used as state features, while User news features and Context features are used as action features
ユーザー特徴量とコンテキスト特徴量を状態特徴量として、ユーザーニュース特徴量とコンテキスト特徴量を行動特徴量として使用する。
On one hand, the reward for taking action a at certain state s is closely related to all the features
一方、ある状態sでアクションaを起こしたときの報酬は、すべての特徴量と密接に関係している。
On the other hand, the reward that determined by the characteristics of the user himself (e.g., whether this user is active, whether this user has read enough news today) is more impacted by the status of the user and the context only
一方、ユーザー自身の特性によって決まる報酬（例えば、このユーザーはアクティブかどうか、このユーザーは今日のニュースを十分に読んだかどうか）は、ユーザーのステータスや文脈のみに影響される。
Based on this observation, like [47], we divide the Q-function into value function V (s) and advantage function A(s, a), whereV (s) is only determined by the state features, and A(s, a) is determined by both the state features and the action features.
この観察に基づき、[47]と同様に、Q関数を価値関数V（s）と優位関数A（s，a）に分け、V（s）は状態特徴のみ、A（s，a）は状態特徴と行動特徴の両方によって決定されるようにする。

## User Activeness ユーザーの行動力

Traditional recommender systems only focus on optimizing CTRlike metrics (i.e., only utilizing click / no click labels), which only depicts part of the feedback information from users
従来のレコメンダーシステムは、CTRのような指標の最適化（クリック/クリックなしのラベルの活用）にのみ注力しており、ユーザーからのフィードバック情報の一部しか描かれていない
The performance of recommendation might also influence whether users want to use the application again, i.e., better recommendation will increase the frequency for users to interact with the application
レコメンデーションの性能は、ユーザーが再びアプリケーションを使いたいと思うかどうかにも影響するかもしれません。つまり、より良いレコメンデーションは、ユーザーがアプリケーションと対話する頻度を高めることになります
Therefore, the change of user activeness should also be considered properly
したがって、ユーザーの活性度の変化も適切に考慮する必要がある
Users request for news in a non-uniform pattern.
ユーザーのニュースに対するリクエストは、一様ではありません。

Users usually read news for a short period (e.g., 30 minutes), during which they will request or click news with high frequency
ユーザーは通常、短時間（例えば30分）ニュースを読み、その間に高い頻度でニュースのリクエストやクリックを行う
Then they might leave the application and return to the application when they want to read more news after several hours
そして、一度アプリケーションから離れ、数時間後にもっとニュースを読みたくなったときにアプリケーションに戻るかもしれません
A user return happens when a user requests for news (users will always request for news before they click on news, therefore, user click is also implicitly considered).
ユーザーリターンとは、ユーザーがニュースを要求したときに発生するものです（ユーザーはニュースをクリックする前に必ずニュースを要求するので、ユーザークリックも暗黙のうちに考慮されます）。

We use survival models [18, 30] to model user return and user activeness
生存モデル[18, 30]を用いて、ユーザーの再訪とユーザーの活性化をモデル化する。
Survival analysis [18, 30] has been applied in the field of estimating user return time [20]
生存時間分析[18, 30]は、ユーザーの復帰時間を推定する分野で応用されています[20]。
Suppose T is the time until next event (i.e., user return) happens, then the hazard function (i.e., instantaneous rate for the event to happen) can be defined as Equation 3 [1, 30]
次のイベント（＝ユーザーリターン）が起こるまでの時間をTとすると、ハザード関数（＝イベントが起こる瞬間の割合）は、式3として定義できる[1, 30] 。

$$
\tag{3}
$$

Then the probability for the event to happen after t can be defined as Equation 4 [1, 30]
すると、t以降に事象が発生する確率は、式4で定義できる[1, 30] 。

$$
\tag{4}
$$

and the expected life span T0 can be calculated as [1, 30]
であり、期待寿命T0は次のように計算できる[1, 30]。

$$
\tag{5}
$$

In our problem, we simply set λ(t) = λ0, which means each user has a constant probability to return
この問題では、単純にλ(t)=λ0とし、各ユーザーが一定の確率で帰還することを意味します。
Every time we detect a return of user, we will set S(t) = S(t) + Sa for this particular user
ユーザーの復帰を検知するたびに、この特定のユーザーについて、S(t)=S(t)+Saとする
The user activeness score will not exceed 1
ユーザー活性度スコアが1を超えないこと
For instance, as shown in Figure 5, user activeness for this specific user starts to decay from S0 at time 0
例えば、図5に示すように、この特定のユーザーのユーザー活性度は、時刻0のS0から減衰し始め
At timestamp t1, the user returns and this results in a Sa increase in the user activeness
タイムスタンプt1において、ユーザーが復帰し、その結果、ユーザーの活性度がSa上昇する。
Then, the user activeness continues to decay after t1
そして、t1以降、ユーザーの活性度は減衰し続ける。
Similar things happen at t2, t3, t4 and t5
t2、t3、t4、t5で同様のことが起こる
Note that, although this user has a relatively high request frequency during t4 to t9, the maximum user activeness is truncated to 1.
なお、このユーザーはt4～t9の間は比較的要求頻度が高いが、ユーザーの活性度の最大値は1に切り捨てられている。

The parameters S0, Sa, λ0, T0 are determined according to the real user pattern in our dataset
パラメータS0、Sa、λ0、T0は、データセットに含まれる実際のユーザーパターンに応じて決定される
S0 is set to 0.5 to represent the random initial state of a user (i.e., he or she can be either active or inactive)
S0は、ユーザーのランダムな初期状態を表すために0.5に設定される（すなわち、ユーザーはアクティブまたは非アクティブのいずれかになる）。
We can observe the histogram of the time interval between every two consecutive requests of users as shown in Figure 6
図6に示すように、ユーザーの連続した2つのリクエストの間の時間間隔のヒストグラムを観察することができます。
We observe that besides reading news multiple times in a day, people usually return to the application on a daily regular basis
1日に何度もニュースを読む以外に、毎日定期的にアプリケーションに戻るのが普通であることが観察される
So we set T0 to 24 hours
そこで、T0を24時間に設定
The decaying parameter λ0 is set to 1.2 × 10−5 second−1 according to Equation 4 and Equation 5
減衰パラメータλ0は、式4と式5により、1.2×10-5秒-1に設定されています。
In addition, the user activeness increase Sa for each click is set to 0.32 to make sure user will return to the initial state after one daily basis request, i.e., S0e −λ0T0 + Sa = S0.
また、1回のクリックに対するユーザの活性度増加量Saは、ユーザが1日単位の要求で初期状態に戻るように、すなわちS0e -λ0T0 + Sa = S0となるように0.32に設定した。

The click / no click label rcl ick and the user activeness ract ive are combined as in Equation 6.
クリック／クリックなしラベルrcl ickとユーザー活性度ractiveを式6のように組み合わせています。

$$
\tag{6}
$$

Although we use survival models here to estimate the user activeness, other alternatives like Poisson point process [13] can also be applied and should serve similar function.
ここでは、生存モデルを用いてユーザーの活性度を推定しているが、ポアソン点過程 [13] などの他の選択肢も適用でき、同様の機能を果たすはずである。

## Explore Explore

The most straightforward strategies to do exploration in reinforcement learning are ϵ-greedy [31] and UCB [23]
強化学習で探索を行う最も簡単な戦略は、?グリーディ[31]とUCB[23]です。
ϵ-greedy will randomly recommend new items with a probability of ϵ, while UCB will pick items that have not been explored for many times (because these items may have larger variance)
ϵグリーディは新しいアイテムをϵの確率でランダムに推薦し、UCBは何度も探索されていないアイテムを選ぶ（これらのアイテムは分散が大きいかもしれないため）
It is evident that these trivial exploration techniques will harm the recommendation performance in a short period
このような些細な探索技術が、短期間で推薦性能を低下させることは明らかである
Therefore, rather than doing random exploration, we apply a Dueling Bandit Gradient Descent algorithm [16, 17, 49] to do the exploration
そこで、ランダムな探索を行うのではなく、Dueling Bandit Gradient Descentアルゴリズム [16, 17, 49] を適用して、探索を行うことにしました
Intuitively, as shown in Figure 7, the agent G is going to generate a recommendation list L using the current network Q and another list L˜ using an explore network Q˜ 
直感的には、図7に示すように、エージェントGは、現在のネットワークQを用いた推薦リストLと、探索ネットワークQ〜を用いた別のリストL〜を生成しようとする。
The parameters W˜ of network Q˜ can be obtained by adding a small disturb ∆W (Equation 7) to the parameters W of the current network
ネットワークQ〜のパラメータW〜は、現在のネットワークのパラメータWに小さな外乱ΔW（式7）を加えることで得ることができる

$$
\tag{7}
$$

where α is the explore coefficient, and rand(−1, 1) is a random number between -1 and 1
ここで、αは探索係数、rand(-1, 1)は-1〜1の乱数である
Then, the agent G will do a probabilistic interleave [16] to generate the merged recommendation list Lˆ using L and L˜ 
次に、エージェントGは、確率的インターリーブ[16]を行い、LとL〜を用いてマージされた推薦リストLˆを生成することになります。
To determine the item for each position in the recommendation list Lˆ, the probabilistic interleave approach basically will first randomly select between list L and L˜ 
推薦リストLˆの各位置の項目を決定するために、確率的インターリーブアプローチは基本的に、まずリストLとL〜の間をランダムに選択します。
Suppose L is selected, then an item i from L will be put into Lˆ with a probability determined by its ranking in L (items with top rankings will be selected with higher probability)
Lが選択されたとすると、Lのアイテムiは、Lでの順位によって決まる確率でLˆに入れられる（順位が上位のアイテムが高い確率で選択される）。
Then, list Lˆ will be recommended to user u and agent G will obtain the feedback B
そして、リストLˆがユーザuに推薦され、エージェントGはフィードバックBを得る。
If the items recommended by the explore network Q˜ receive a better feedback, the agent G will update the network Q towards Q˜ , with the parameters of the network being updated as Equation 8
探索ネットワークQ〜が推奨するアイテムがより良いフィードバックを受けた場合、エージェントGはネットワークQをQ〜に向けて更新し、ネットワークのパラメータは式8のように更新される。

$$
\tag{8}
$$

Otherwise, the agent G will keep network Q unchanged
そうでない場合、エージェントGはネットワークQを変更せずに維持する
Through this kind of exploration, the agent can do more effective exploration without losing too much recommendation accuracy.
このような探索を行うことで、エージェントは推薦の精度をあまり落とさずに、より効果的な探索を行うことができます。

# Experiment 実験

## Dataset データセット

We conduct experiment on a sampled offline dataset collected from a commercial news recommendation application and deploy our system online to the App for one month
商用ニュース推薦アプリケーションから収集したオフラインデータセットで実験を行い、本システムを1ヶ月間Appにオンライン展開する。
Each recommendation algorithm will give out its recommendation when a news request arrives and user feedback will be recorded (click or not)
各レコメンドアルゴリズムは、ニュースリクエストが来たときにレコメンドを行い、ユーザーのフィードバック（クリックするかしないか）を記録する。
The basic statistics for the sampled data is as in Table 2
サンプリングされたデータの基本統計量は表2の通りである。
In the first offline stage, the training data and testing data are separated by time order (the last two weeks are used as testing data), to enable the online models to learn the sequential information between different sessions better
最初のオフラインステージでは、トレーニングデータとテストデータを時間順で分離し（最後の2週間をテストデータとして使用）、オンラインモデルが異なるセッション間の連続した情報を学習できるようにするためである。
During the second online deploying stage, we use the offline data to pre-train the model, and run all the compared methods in the real production environment.
2回目のオンライン展開の段階では、オフラインのデータを使ってモデルを事前に訓練し、実際の生産環境で比較したすべての方法を実行します。

As shown in Figure 8, the dataset is very skewed
図8に示すように、データセットは非常に歪んでいます
The number of requests for each user follows a long tail distribution and most users only request news for less than 500 times
各ユーザーのリクエスト数はロングテール分布をしており、ほとんどのユーザーは500回以下のニュースしかリクエストしていない
The number of times each news are pushed also follow a long tail distribution and most news are pushed to user less than 200 times.
また、各ニュースのプッシュ回数もロングテール分布をしており、ほとんどのニュースが200回未満でユーザーにプッシュされています。

## Evaluation measures 評価指標

- CTR. [10] Click through rate is calculated as Equation 9. CTR [10] クリック率は、式9のように計算されます。

$$
\tag{9}
$$

- Precision@k [10]. Precision at k is calculated as Equation 10 Precision@kさん【10件 kでの精度は、式10で計算されます。

$$
\tag{10}
$$

- nDCG. We apply the standard Normalized Discounted Cumulative Gain proved in [46] as Equation 11, where r is the rank of items in the recommendation list, n is the length of the recommendation list, f is the ranking function or algorithm, y f r is the 1 or 0 indicating whether a click happens and D(r) is the discount. 正規化装置 ここで、rは推薦リストのアイテムのランク、nは推薦リストの長さ、fはランキング関数またはアルゴリズム、y f rはクリックの有無を示す1または0、D（r）は割引であるとして、［46］で証明された標準正規化割引累積利得を式11として適用する。

$$
\tag{11}
$$

with
と

$$
\tag{12}
$$

## Experiment setting 実験設定

In our experiment, the parameters are determined by grid search of parameter space to find the ones with best CTR
本実験では、パラメータ空間をグリッド検索して、CTRが最も良くなるパラメータを決定しています
The detailed settings are shown in Table 3.
詳細な設定内容は、表3に示すとおりです。

## Compared methods 比較対象方法

Variations of our model.
当社モデルのバリエーション。

Our basic model is named as “DN”, which uses a dueling-structure [47] Double Deep Q-network [41] without considering future reward
我々の基本モデルは「DN」と名付けられ、将来の報酬を考慮せずに、デュエル構造[47]ダブルQネットワーク[41]を使用する。
Then, by adding future reward into consideration, this becomes “DDQN”
そして、将来の報酬を考慮することで、"DDQN "となります。
After that, we add more components to “DDQN”
その後、"DDQN "にさらにコンポーネントを追加していきます。
“U” stands for user activeness, “EG” stands for ϵ-greedy, and “DBGD” stands for Dueling Bandit Gradient Descent.
"U "はユーザー活性度、"EG "はϵ-greedy、"DBGD "はDueling Bandit Gradient Descentを表しています。

Baseline algorithms.
ベースライン・アルゴリズム

We compared our algorithms with following five baseline methods
私たちのアルゴリズムを、以下の5つのベースライン手法と比較しました。
All these five methods will conduct online update during the testing stage
これら5つの方式は、いずれもテスト段階でオンラインアップデートを実施します
Some state-of-art methods can not be applied due to their inapplicability to our problem, like [43] (user graph and item graph is oversized and can not be updated incrementally), [45] (similar with W&D when textual features are removed), and [48] (user return is not applicable to experience replay update).
例えば、[43]（ユーザーグラフとアイテムグラフが巨大化し、インクリメンタルに更新できない）、[45]（テキスト特徴を削除するとW&Dと同様）、[48]（ユーザーリターンは体験リプレイ更新に適用できない）など、我々の問題には適用できない最新の手法もあります。

- LR. Logistic Regression is widely used in industry as baseline methods due to its easy implementation and high efficiency. It takes all the four categories of features as input. It is implemented using Keras [9]. LR ロジスティック回帰は、その容易な実装と高い効率性から、ベースライン手法として産業界で広く利用されている 4つのカテゴリの特徴をすべて入力とします。 Keras（ケラス）[9]を用いて実装されています。

- FM [29, 34]. Factorization Machines is a state-of-art contextaware recommendation methods. It takes all the four categories of features as input, use the combination of features and their interactions to do the click prediction. FM【29、34 因数分解マシンは、最先端のコンテクストウェア型推薦法 4種類の特徴量をすべて入力とし、特徴量の組み合わせとその相互作用を利用してクリック予測を行います。

- W&D [8]. Wide & Deep is a widely used state-of-art deep learning model combining the memorization (through a logistic regression on wide combinations of categorical features) and generalization (through a deep neural network embedding of the raw features) to predict the click label. W&D【8 Wide & Deepは、クリックラベルを予測するために、記憶（カテゴリー特徴の幅広い組み合わせに対するロジスティック回帰による）と汎化（生の特徴のディープニューラルネットワークによる埋め込み）を組み合わせた、広く使われている最先端の深層学習モデルです。

- LinUCB [23]. Linear Upper Confidence Bound [23] can select an arm (i.e., recommend a piece of news) according to the estimated upper confidence bound of the potential reward. Due to the long tail distribution of news request and click counts, we apply the same set of parameters for different news, which actually performs better than the original setting in [23] on our dataset.(An improved version of the original LinUCB– HLinUCB will also be compared.) LinUCB【23 Linear Upper Confidence Bound [23]は、潜在的な報酬の推定上方信頼限界に従って腕を選択する（すなわち、ニュースの一部を推薦する）ことができます。 ニュースのリクエストとクリック数のロングテール分布のため，異なるニュースに対して同じパラメータセットを適用し，実際に我々のデータセットでは[23]のオリジナル設定よりも良い結果を得た(オリジナルのLinUCB- HLinUCBの改良版も比較される)。

- HLinUCB [42] is another state-of-art bandit-based approach in recommendation problem. Hidden Linear Upper Confidence Bound [42] further allows learned hidden feature to model the reward. We follow the original setting of keeping different sets of parameters for different users and different news. However, under this case, only News features introduced in Section 4.2 can be directly applied, while the other features describing the interaction between user and news are expected to be learned in the hidden features. HLinUCB [42]も推薦問題における最先端のバンディットベースのアプローチである。 隠れ線形上信頼境界[42]では、さらに、学習された隠れ特徴で報酬をモデル化することができます。 ユーザーやニュースによって異なるパラメータを保持するという当初の設定を踏襲しています しかし、この場合、4.2節で紹介したニュース特徴だけが直接適用でき、ユーザーとニュースの相互作用を記述する他の特徴は、隠れ特徴で学習することが期待される。

For all compared algorithms, the recommendation list is generated by selecting the items with top-k estimated potential reward (for LinUCB, HLinUCB and our methods) or probability of click (for LR, FM and W&D) of each item.
すべての比較アルゴリズムにおいて，各アイテムの潜在報酬（LinUCB，HLinUCBおよび我々の手法）またはクリック確率（LR，FMおよびW&D）の推定値が上位k個のアイテムを選択することによって推薦リストを生成する．

## Offline evaluation オフライン評価

We first compare our methods with other baselines on the offline dataset
まず、オフラインデータセットにおいて、我々の手法を他のベースラインと比較します。
The offline dataset is static and only certain pairs of usernews interaction have been recorded
オフラインデータセットは静的なものであり、ユーザニュースのインタラクションの特定のペアのみが記録されている
As a result, we can not observe the change of user activeness due to different recommendation decisions
そのため、推薦判断の違いによるユーザーの活性度の変化を観察することができない
Similarly, the exploration strategy can not explore well due to the limited candidate news set (i.e., only the click labels of a few candidate news are recorded)
同様に、候補となるニュースセットが限られているため（つまり、いくつかの候補ニュースのクリックラベルしか記録されていない）、探索戦略はうまく探索することができません。
Hence, the benefit of considering user activeness and exploration is not very evident in the offline setting
したがって、ユーザーの能動性や探索性を考慮するメリットは、オフライン環境ではあまり感じられない
Therefore, we only show the comparison of recommendation accuracy under this situation.
そのため、ここではこの状況下での推薦精度の比較のみを示します。

For the offline experiment, we down-sample the click / no-click to approximately 1:11 for better model fitting purpose.
オフライン実験では、より良いモデルフィッティングのために、クリック／ノークリックを約1：11にダウンサンプリングしています。

We design the algorithm to recommend the top-5 news, and show the results in terms of CTR and nDCG (we omit top-5 precision because it will be the same with CTR).
トップ5のニュースを推薦するようにアルゴリズムを設計し、CTRとnDCGで結果を示す（トップ5の精度はCTRと同じになるため省略）。

### Accuracy. アキュラシー

The accuracy result is shown in Table 4
精度の結果を表4に示します。
As expected, our algorithms outperform all the baseline algorithms
予想通り、我々のアルゴリズムはすべてのベースラインアルゴリズムを上回った
Our base model DN already achieves very good results compared with the baselines
ベースモデルDNは、すでにベースラインと比較して非常に優れた結果を達成している
This is because the dueling network structure can better model the interaction between user and news
これは、決闘ネットワーク構造が、ユーザーとニュースの間の相互作用をよりよくモデル化できるためです
Adding future reward consideration (DDQN), we achieve another significant improvement
将来の報酬を考慮する（DDQN）ことで、さらに大幅な改善を実現しました
Then, incorporating user activeness and exploration do not necessarily improve the performance under the offline setting, which might because under offline setting, the algorithm can not make the best interaction with user due to the limited static set of candidate news
これは、オフライン環境では、候補となるニュースの静的な集合が限られているため、アルゴリズムがユーザーと最適な対話を行うことができないためと考えられる。
(It is possible that our agent G want to recommend user u a news i for user activeness or exploration consideration, but actually the information about whether user u will click on news i or not does not exist in the offline log.) In addition, naive random exploration like ϵ-greedy will harm the recommendation accuracy
(エージェントGは、ユーザの能動性や探索を考慮してユーザuにニュースiを推薦したいが、実際にはユーザuがニュースiをクリックするかどうかの情報はオフラインログに存在しない可能性がある)。また、ϵ-greedyのような素朴なランダム探索は、推薦精度を低下させる。

### Model converge process. モデルの収束処理。

We further show the cumulative CTR of different methods in Figure 9 to illustrate the convergence process
さらに、図9に異なる手法の累積CTRを示し、収束の過程を説明する
The offline data are ordered by time and simulate the process that users send news request as time goes by
オフラインのデータを時間順に並べ、時間の経過とともにユーザーがニュースリクエストを送信する過程をシミュレートしている
All the compared methods will update their models every 100 request sessions
比較されたすべてのメソッドは、100リクエストセッションごとにモデルを更新します。
As expected, our algorithm (DDQN + U + DBGD) converges to a better CTR faster than other methods.
予想通り、我々のアルゴリズム（DDQN + U + DBGD）は、他の方法よりも早く、より良いCTRに収束する。

## Online evaluation 

In the online evaluation stage, we deployed our models and compared algorithms on a commercial news recommendation application
オンライン評価段階では、市販のニュース推薦アプリケーションにモデルを導入し、アルゴリズムを比較しました。
Users are divided evenly to different algorithms
ユーザーはアルゴリズムごとに均等に振り分けられる
In online setting, we can not only measure the accuracy of recommendation, but also observe the recommendation diversity for different algorithms
オンライン設定では、推薦の精度を測定するだけでなく、異なるアルゴリズムによる推薦の多様性を観察することができます
All the algorithms are designed to recommend the top-20 news to a user when a news request is received.
いずれのアルゴリズムも、ニュースリクエストがあった際に、上位20位までのニュースをユーザーに推薦するように設計されています。

### Accuracy. アキュラシー

We compare different algorithms in terms of CTR, Precision@5, and nDCG
CTR、Precision@5、nDCGの観点から異なるアルゴリズムを比較する。
As shown in Table 5, our full model DDQN + U + DBGD outperforms all the other models significantly in terms of CTR, Precision@5 and nDCG
表5に示すように、我々のフルモデルDDQN + U + DBGDは、CTR、Precision@5、nDCGの点で他のすべてのモデルを大きく上回った。
Here are the observations for adding each component
以下は、各コンポーネントの追加に関する観測結果です。
Adding future reward (DDQN) does improve the recommendation accuracy over basic DN
未来報酬（DDQN）を追加することで、基本DNよりも推薦精度を向上させることができる
However, further adding user activeness consideration U seems not very helpful in terms of recommendation accuracy
しかし、さらにユーザーの活性度を考慮したUを加えることは、推薦精度の観点からはあまり意味がないように思われる
(But this component is helpful for improving user activeness and recommendation diversity
(ただし、このコンポーネントはユーザーの能動性やレコメンデーションの多様性を向上させるために有用です。
This will be demonstrated later.) In addition, using DBGD as exploration methods will help avoid the performance loss induced by classic ϵ-greedy methods.
これは後ほど実証する)。また、探索手法としてDBGDを用いることで、古典的なϵグリーディ法が引き起こす性能低下を回避することができます。

### Recommendation diversity. 推奨する多様性

Finally, in order to evaluate the effectiveness of exploration, we calculate the recommendation diversity of different algorithms using ILS
最後に、探索の効果を評価するために、ILSを用いた様々なアルゴリズムの推薦多様性を計算する
[2, 53]
[2, 53]
It is calculated by Equation 13
式13で算出されます。

$$
\tag{13}
$$

where S(bi ,bj) represents the cosine similarity between item bi and item bj 
ここで、S(bi ,bj) は項目 bi と項目 bj のコサイン類似度を表す。
We show the diversity for the news clicked by users as in Table 6
ユーザーがクリックしたニュースの多様性を表6のように示す。
In general, users in our algorithm DDQN + U + DBGD achieves the best click diversity
一般に、我々のアルゴリズムDDQN + U + DBGDのユーザーは、最高のクリック多様性を達成します。
Interestingly, adding EG seems not improving the recommendation diversity
興味深いことに、EGを追加しても推薦の多様性は改善されないようです。
This is probably because, when random exploration (i.e., EG) is conducted, the recommender might recommend some totally unrelated items to users
これは、ランダム探索（EG）を行った場合、レコメンダーがユーザーに全く関係のないものを推薦してしまう可能性があるためと思われます
Although these items have high diversity, users might be not interested in reading them and turn back to read more about the items that fit their interest better
これらの項目は多様性が高いが、ユーザーは読むことに興味を持たず、より自分の興味に合った項目の続きを読むために引き返すかもしれない
This way, this exploration will not help improve the recommendation diversity
このように、この探索は推薦の多様性を向上させるのに役立つことはありません
To our surprise, some baseline methods, like HLinUCB, also achieve comparable recommendation diversity, which indicates that UCB can also achieve reasonable exploration result (but this kind of unguided exploration will harm the recommendation accuracy).
驚いたことに、HLinUCBのようないくつかのベースライン手法も同等の推薦多様性を達成しており、これはUCBも妥当な探索結果を達成できることを示しています（ただし、この種のガイドなし探索は推薦精度に害を及ぼします）。

# Conclusion 結論

In this paper, we propose a DQN-based reinforcement learning framework to do online personalized news recommendation
本論文では、DQNに基づく強化学習フレームワークを提案し、オンラインパーソナライズドニュースの推薦を行う。
Different from previous methods, our method can effectively model the dynamic news features and user preferences, and plan for future explicitly, in order to achieve higher reward (e.g., CTR) in the long run
従来の手法とは異なり、本手法はダイナミックなニュースの特徴やユーザーの嗜好を効果的にモデル化し、将来の計画を明示的に立てることで、長期的に高い報酬（例：CTR）を達成することができます
We further consider user return pattern as a supplement to click / no click label in order to capture more user feedback information
さらに、クリック/クリックなしのラベルを補完するものとして、ユーザーのリターンパターンを考慮することで、より多くのユーザーフィードバック情報を取得することができます。
In addition, we apply an effective exploration strategy into our framework to improve the recommendation diversity and look for potential more rewarding recommendations
さらに、推薦の多様性を向上させ、より報酬の高い推薦を探すために、効果的な探索戦略をフレームワークに適用しています。
Experiments have shown that our method can improve the recommendation accuracy and recommendation diversity significantly
実験により、本手法が推薦精度と推薦多様性を大幅に改善できることが示された
Our method can be generalized to many other recommendation problems.
この方法は、他の多くの推薦問題に一般化することができる。

For the future work, it will be more meaningful to design models for different users correspondingly (e.g., heavy users and one-time users), especially the user-activeness measure
今後の課題としては、ヘビーユーザーと一度きりのユーザーなど、異なるユーザーに対応したモデル設計を行うことがより有意義であり、特にユーザー活性度指標
It can bring more insights if different patterns are observed for different groups of users.
ユーザーグループによって異なるパターンが観察されれば、より多くの洞察を得ることができます。